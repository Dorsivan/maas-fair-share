/*
Copyright 2026 The maas-fair-share Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package weightedlas

// UNI-283 review round 2: what changes when ~800 slots are many ENDPOINTS
// behind one EPP. Skipped unless UNI283_SIM=1.
//
// Admission order comes from the real plugin (Pick/PreRequest/ResponseBody).
// Everything around it re-implements llm-d-router v0.11.0 formula-for-formula,
// read from the module source:
//
//   - utilization-detector Saturation: mean over endpoints of
//     max(waiting/queueDepthThreshold, kv/0.8); dispatch HoL-blocks at >= 1.0
//     (static usage limit). saturationdetector/utilization/detector.go,
//     usagelimits/usagelimitpolicy.go, controller/internal/processor.go.
//   - the same detector as an auto-injected scheduling Filter: drops endpoints
//     with waiting >= thr*(1+headroom) or kv >= 0.8*(1+headroom), unless that
//     drops all of them. config/loader/defaults.go injectFilterIntoProfiles.
//   - queue-scorer (max-q)/(max-q_min) over candidates, kv-cache-utilization
//     scorer 1-kv, prefix-cache-scorer matchBlocks/totalBlocks; weights
//     3.0 / 2.0 / 3.0 as in deploy/poc/00-config.yaml; max-score-picker.
//   - one dispatch per processor cycle, cycles on a 1ms ticker; endpoint
//     metrics (waiting, kv) refreshed every 50ms (datalayer defaultRefreshInterval),
//     so saturation, the filter and queue-scorer all read a snapshot up to
//     50ms old. The prefix index is EPP-side and updates immediately.
//
// Each endpoint runs max-num-seqs sequences and a FIFO waiting queue. Service
// time is drawn per request; decode rate is constant (batch effects ignored);
// no preemption is modelled -- kv above 1.0 is reported, not acted on.

import (
	"context"
	"fmt"
	"math"
	"math/rand"
	"sort"
	"testing"
	"time"

	"github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol"
	fwkfcmocks "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol/mocks"
	fwkrc "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requestcontrol"
	fwkrh "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requesthandling"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

type epTenant struct {
	id       string
	weight   float64
	prefixes int     // distinct shared prompt prefixes this tenant uses
	joinAt   float64 // seconds
}

type epParams struct {
	endpoints   int
	maxSeqs     int
	thr         float64
	headroom    float64
	wQueue      float64
	wKV         float64
	wPrefix     float64
	prefixRatio float64 // matchBlocks/totalBlocks on a prefix hit
	cacheK      int     // prefixes an endpoint's cache holds (LRU)
	kvCapacity  float64 // tokens per endpoint
	promptToks  float64
	tokPerSec   float64
	median, p95 float64
	halfLife    float64
	warmup      float64
	window      float64
	seed        int64
	tenants     []epTenant
	trackJoin   string
	noClamp     bool
	// kvThr is the detector's kvCacheUtilThreshold (0 = library default 0.8).
	kvThr float64
	// preempt models vLLM's KV exhaustion: a start needs free KV for its
	// context, and when an endpoint's KV exceeds capacity the most recently
	// started sequence is preempted and later re-prefilled (recompute).
	preempt          bool
	prefillTokPerSec float64
}

type epEndpoint struct {
	running []*epReq
	waiting []*epReq
	cache   []int // most recent last
	// snapshot
	snapWaiting int
	snapKV      float64
}

type epReq struct {
	tenant   string
	prefix   int
	req      *fwksched.InferenceRequest
	service  float64
	output   int
	enqAt    float64
	startAt  float64
	endAt    float64
	genBase  float64 // tokens generated before the current run (preemption)
	decodeAt float64 // when decoding (re)starts after any recompute
}

type epResult struct {
	share          map[string]float64
	maxDev         float64
	gateOpenFrac   float64
	meanStd        float64 // mean over snapshots of std-dev of per-endpoint waiting
	meanMaxWaiting float64
	p99Waiting     float64 // p99 of per-endpoint waiting across snapshots
	strandedFrac   float64 // idle slot-time while another endpoint has a waiting queue
	topEndpointPct float64 // share of all slot-time on the busiest 10% of endpoints
	fifoWaitMean   float64 // dispatch -> start
	fifoWaitP95    float64
	meanQRatio     float64
	meanKVRatio    float64
	peakKVRatio    float64
	firstStart     float64
	firstPick      float64 // seconds from trackJoin's join to its first dispatch
	toNinety       float64 // minutes until trackJoin holds 90% of entitlement (1-min buckets)
	meanRunning    float64 // effective concurrency: mean running sequences, pool-wide
	preemptions    map[string]float64
	dispatches     map[string]float64
	recomputeS     map[string]float64 // slot-seconds spent re-prefilling preempted work
	slotS          map[string]float64
}

func runEndpoints(t *testing.T, prm epParams) epResult {
	t.Helper()
	ctx := context.Background()
	cfg := DefaultConfig()
	cfg.Enforce = true
	cfg.StateLogIntervalSeconds = 0
	cfg.HalfLifeSeconds = prm.halfLife
	cfg.NewcomerClamp = !prm.noClamp
	var wsum float64
	for _, tn := range prm.tenants {
		cfg.Groups = append(cfg.Groups, GroupConfig{Name: tn.id, Weight: tn.weight, Match: GroupMatch{Exact: []string{tn.id}}})
		wsum += tn.weight
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "unclassified", Weight: 1}
	p, clock := newTestPlugin(t, cfg)
	state := p.NewState(ctx)
	rng := rand.New(rand.NewSource(prm.seed))
	kvThr := prm.kvThr
	if kvThr == 0 {
		kvThr = 0.8
	}
	sigma := math.Log(prm.p95/prm.median) / 1.6449

	eps := make([]*epEndpoint, prm.endpoints)
	for i := range eps {
		eps[i] = &epEndpoint{}
	}
	byID := map[string]epTenant{}
	for _, tn := range prm.tenants {
		byID[tn.id] = tn
	}
	accessor := func(now float64) flowcontrol.PriorityBandAccessor {
		var active []flowcontrol.FlowQueueAccessor
		for _, tn := range prm.tenants {
			if now >= tn.joinAt {
				active = append(active, &fwkfcmocks.MockFlowQueueAccessor{
					LenV: 1000, FlowKeyV: flowcontrol.FlowKey{ID: tn.id},
					PeekV: &fwkfcmocks.MockQueueItemAccessor{EnqueueTimeV: clock.now()},
				})
			}
		}
		return &fwkfcmocks.MockPriorityBandAccessor{
			PolicyStateV: state,
			IterateQueuesFunc: func(cb func(flowcontrol.FlowQueueAccessor) bool) {
				for _, q := range active {
					if !cb(q) {
						return
					}
				}
			},
		}
	}
	kvOf := func(e *epEndpoint, now float64) float64 {
		var used float64
		for _, r := range e.running {
			used += prm.promptToks + r.genBase + math.Max(0, math.Min(now, r.endAt)-r.decodeAt)*prm.tokPerSec
		}
		return used / prm.kvCapacity
	}
	hasPrefix := func(e *epEndpoint, px int) bool {
		for _, c := range e.cache {
			if c == px {
				return true
			}
		}
		return false
	}
	touch := func(e *epEndpoint, px int) {
		for i, c := range e.cache {
			if c == px {
				e.cache = append(e.cache[:i], e.cache[i+1:]...)
				break
			}
		}
		e.cache = append(e.cache, px)
		if len(e.cache) > prm.cacheK {
			e.cache = e.cache[1:]
		}
	}
	prefixID := func(tn epTenant) int {
		base := 0
		for _, x := range prm.tenants {
			if x.id == tn.id {
				break
			}
			base += x.prefixes
		}
		return base + rng.Intn(tn.prefixes)
	}

	const tick = 0.001
	const snapEvery = 50 // ms
	occ := map[string]float64{}
	var res epResult
	res.preemptions, res.dispatches, res.recomputeS, res.slotS = map[string]float64{}, map[string]float64{}, map[string]float64{}, map[string]float64{}
	res.firstStart = -1
	res.firstPick = -1
	var joinAt float64
	if prm.trackJoin != "" {
		joinAt = byID[prm.trackJoin].joinAt
	}
	var joinMinute float64
	var joinCurve []float64
	var snaps, gateOpenSnaps int
	var waitSamples []float64
	var fifoWaits []float64
	var stranded, slotTotal float64
	epBusy := make([]float64, prm.endpoints)
	seq := 0
	slots := prm.endpoints * prm.maxSeqs
	end := prm.warmup + prm.window
	step := 0
	for now := 0.0; now < end; now += tick {
		step++
		inWin := now >= prm.warmup
		// completions + FIFO starts, per endpoint (checked every ms)
		for _, e := range eps {
			keep := e.running[:0]
			for _, r := range e.running {
				if r.endAt <= now {
					p.ResponseBody(ctx, r.req, &fwkrc.Response{
						EndOfStream: true, TerminationCause: fwkrc.TerminationCauseNatural,
						Usage: fwkrh.Usage{PromptTokens: int(prm.promptToks), CompletionTokens: r.output,
							TotalTokens: int(prm.promptToks) + r.output, PromptTokenDetails: &fwkrh.PromptTokenDetails{}},
					}, nil)
					continue
				}
				keep = append(keep, r)
			}
			e.running = keep
			for len(e.running) < prm.maxSeqs && len(e.waiting) > 0 {
				r := e.waiting[0]
				if prm.preempt && kvOf(e, now)+(prm.promptToks+r.genBase)/prm.kvCapacity > 1.0 {
					break
				}
				e.waiting = e.waiting[1:]
				r.startAt = now
				recompute := 0.0
				if r.genBase > 0 {
					recompute = (prm.promptToks + r.genBase) / prm.prefillTokPerSec
					if inWin {
						res.recomputeS[r.tenant] += recompute
					}
				}
				r.decodeAt = now + recompute
				r.endAt = r.decodeAt + r.service - r.genBase/prm.tokPerSec
				e.running = append(e.running, r)
				if inWin {
					fifoWaits = append(fifoWaits, now-r.enqAt)
				}
				if r.tenant == prm.trackJoin && res.firstStart < 0 && now >= joinAt {
					res.firstStart = now - joinAt
				}
			}
		}
		// vLLM KV exhaustion: preempt the most recently started sequence
		if prm.preempt && step%snapEvery == 0 {
			for _, e := range eps {
				for len(e.running) > 1 && kvOf(e, now) > 1.0 {
					vi := 0
					for i, r := range e.running {
						if r.startAt > e.running[vi].startAt {
							vi = i
						}
					}
					v := e.running[vi]
					v.genBase += math.Max(0, now-v.decodeAt) * prm.tokPerSec
					e.running = append(e.running[:vi], e.running[vi+1:]...)
					e.waiting = append([]*epReq{v}, e.waiting...)
					if inWin {
						res.preemptions[v.tenant]++
					}
				}
			}
		}
		// metrics refresh
		if step%snapEvery == 0 {
			var sum, sumsq, mx, qsum, kvsum float64
			for _, e := range eps {
				e.snapWaiting = len(e.waiting)
				e.snapKV = kvOf(e, now)
				w := float64(e.snapWaiting)
				sum += w
				sumsq += w * w
				if w > mx {
					mx = w
				}
				qsum += w / prm.thr
				kvsum += e.snapKV / kvThr
				if inWin && e.snapKV/kvThr > res.peakKVRatio {
					res.peakKVRatio = e.snapKV / kvThr
				}
				if inWin && step%(snapEvery*20) == 0 {
					waitSamples = append(waitSamples, w)
				}
			}
			if inWin {
				n := float64(len(eps))
				mean := sum / n
				snaps++
				res.meanStd += math.Sqrt(math.Max(0, sumsq/n-mean*mean))
				res.meanMaxWaiting += mx
				res.meanQRatio += qsum / n
				res.meanKVRatio += kvsum / n
			}
		}
		// saturation from the snapshot
		var sat float64
		for _, e := range eps {
			sat += math.Max(float64(e.snapWaiting)/prm.thr, e.snapKV/kvThr)
		}
		sat /= float64(len(eps))
		if inWin && step%snapEvery == 0 && sat < 1 {
			gateOpenSnaps++
		}
		if sat < 1 {
			// one dispatch per cycle
			q, err := p.Pick(ctx, accessor(now))
			if err != nil {
				t.Fatal(err)
			}
			if q != nil {
				id := q.FlowKey().ID
				tn := byID[id]
				if id == prm.trackJoin && res.firstPick < 0 {
					res.firstPick = now - joinAt
				}
				px := prefixID(tn)
				// filter
				qLimit := prm.thr * (1 + prm.headroom)
				kvLimit := kvThr * (1 + prm.headroom)
				var cands []*epEndpoint
				for _, e := range eps {
					if float64(e.snapWaiting) < qLimit && e.snapKV < kvLimit {
						cands = append(cands, e)
					}
				}
				if len(cands) == 0 {
					cands = eps
				}
				minQ, maxQ := math.MaxInt, math.MinInt
				for _, e := range cands {
					minQ = min(minQ, e.snapWaiting)
					maxQ = max(maxQ, e.snapWaiting)
				}
				var best []*epEndpoint
				bestScore := math.Inf(-1)
				for _, e := range cands {
					qs := 1.0
					if maxQ != minQ {
						qs = float64(maxQ-e.snapWaiting) / float64(maxQ-minQ)
					}
					ps := 0.0
					if hasPrefix(e, px) {
						ps = prm.prefixRatio
					}
					s := prm.wQueue*qs + prm.wKV*(1-e.snapKV) + prm.wPrefix*ps
					if s > bestScore+1e-12 {
						bestScore, best = s, []*epEndpoint{e}
					} else if math.Abs(s-bestScore) <= 1e-12 {
						best = append(best, e)
					}
				}
				e := best[rng.Intn(len(best))]
				touch(e, px)
				s := prm.median * math.Exp(sigma*rng.NormFloat64())
				if s < 1 {
					s = 1
				}
				seq++
				ir := &fwksched.InferenceRequest{RequestID: fmt.Sprintf("%s-%d", id, seq), FairnessID: id,
					Body: &fwkrh.InferenceRequestBody{}, RequestSizeBytes: int(prm.promptToks * 4)}
				if err := p.PreRequest(ctx, ir, nil); err != nil {
					t.Fatal(err)
				}
				if now >= prm.warmup {
					res.dispatches[id]++
				}
				e.waiting = append(e.waiting, &epReq{tenant: id, prefix: px, req: ir, service: s,
					output: int(s * prm.tokPerSec), enqAt: now})
			}
		}
		// accounting, sampled every 100ms to keep it cheap
		if step%100 == 0 {
			if inWin {
				anyWaiting := false
				for _, e := range eps {
					if len(e.waiting) > 0 {
						anyWaiting = true
						break
					}
				}
				for i, e := range eps {
					for _, r := range e.running {
						occ[r.tenant] += 0.1
						res.slotS[r.tenant] += 0.1
					}
					res.meanRunning += float64(len(e.running))
					epBusy[i] += float64(len(e.running))
					idle := float64(prm.maxSeqs - len(e.running))
					slotTotal += float64(prm.maxSeqs)
					if anyWaiting && len(e.waiting) == 0 {
						stranded += idle
					}
				}
			}
			if prm.trackJoin != "" && now >= joinAt {
				for _, e := range eps {
					for _, r := range e.running {
						if r.tenant == prm.trackJoin {
							joinMinute += 0.1
						}
					}
				}
				if int((now-joinAt)*10)%600 == 599 {
					joinCurve = append(joinCurve, joinMinute/60)
					joinMinute = 0
				}
			}
		}
		clock.advance(time.Millisecond)
	}
	var total float64
	for _, v := range occ {
		total += v
	}
	res.share = map[string]float64{}
	for _, tn := range prm.tenants {
		res.share[tn.id] = 100 * occ[tn.id] / total
		if d := math.Abs(res.share[tn.id] - 100*tn.weight/wsum); d > res.maxDev {
			res.maxDev = d
		}
	}
	res.meanRunning /= prm.window * 10
	if snaps > 0 {
		res.gateOpenFrac = float64(gateOpenSnaps) / float64(snaps)
		res.meanStd /= float64(snaps)
		res.meanMaxWaiting /= float64(snaps)
		res.meanQRatio /= float64(snaps)
		res.meanKVRatio /= float64(snaps)
	}
	sort.Float64s(waitSamples)
	if len(waitSamples) > 0 {
		res.p99Waiting = waitSamples[int(0.99*float64(len(waitSamples)-1))]
	}
	if slotTotal > 0 {
		res.strandedFrac = stranded / slotTotal
	}
	sort.Float64s(epBusy)
	var busyAll, busyTop float64
	topN := max(1, prm.endpoints/10)
	for i, b := range epBusy {
		busyAll += b
		if i >= len(epBusy)-topN {
			busyTop += b
		}
	}
	if busyAll > 0 {
		res.topEndpointPct = 100 * busyTop / busyAll
	}
	sort.Float64s(fifoWaits)
	if len(fifoWaits) > 0 {
		var s float64
		for _, w := range fifoWaits {
			s += w
		}
		res.fifoWaitMean = s / float64(len(fifoWaits))
		res.fifoWaitP95 = fifoWaits[int(0.95*float64(len(fifoWaits)-1))]
	}
	res.toNinety = -1
	if prm.trackJoin != "" {
		ent := 0.9 * byID[prm.trackJoin].weight / wsum * float64(slots)
		for i, v := range joinCurve {
			if v >= ent {
				res.toNinety = float64(i + 1)
				break
			}
		}
	}
	return res
}

type epShape struct {
	name      string
	endpoints int
	maxSeqs   int
}

var epShapes = []epShape{
	{"POC today: 2 x 8", 2, 8},
	{"many small: 100 x 8", 100, 8},
	{"few large: 6 x 128", 6, 128},
}

func epBase(sh epShape) epParams {
	return epParams{
		endpoints: sh.endpoints, maxSeqs: sh.maxSeqs, thr: 32, headroom: 0.3,
		wQueue: 3, wKV: 2, wPrefix: 3, prefixRatio: 0.8, cacheK: 4 * sh.maxSeqs,
		kvCapacity: 1074224, promptToks: 200, tokPerSec: 27,
		median: 60, p95: 720, halfLife: 60, warmup: 1800, window: 1800, seed: 1,
		tenants: []epTenant{
			{id: "app1", weight: 20, prefixes: 1},
			{id: "app2", weight: 10, prefixes: 1},
			{id: "end-users", weight: 65, prefixes: 40},
		},
	}
}

// TestUNI283EndpointShapes: items (a), (b), (d) -- saturation signal,
// endpoint routing and KV pressure for each decomposition of ~800 slots.
func TestUNI283EndpointShapes(t *testing.T) {
	skipUnlessSim(t)
	fmt.Println("| shape | scorer q/kv/prefix | split app1/app2/end-users | max-dev | gate open | mean std(waiting) | mean max waiting | p99 waiting | stranded idle slots | busiest 10% endpoints' load | vLLM FIFO wait mean / p95 (s) | qRatio | kvRatio mean / peak |")
	fmt.Println("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
	for _, sh := range epShapes {
		for _, w := range [][3]float64{{3, 2, 3}, {2, 2, 3}} {
			prm := epBase(sh)
			prm.wQueue, prm.wKV, prm.wPrefix = w[0], w[1], w[2]
			r := runEndpoints(t, prm)
			fmt.Printf("| %s | %.0f/%.0f/%.0f | %s | %.1f | %.0f%% | %.1f | %.1f | %.0f | %.1f%% | %.1f%% | %.0f / %.0f | %.2f | %.3f / %.3f |\n",
				sh.name, w[0], w[1], w[2], fmtShares(r.share), r.maxDev, 100*r.gateOpenFrac, r.meanStd, r.meanMaxWaiting,
				r.p99Waiting, 100*r.strandedFrac, r.topEndpointPct, r.fifoWaitMean, r.fifoWaitP95, r.meanQRatio, r.meanKVRatio, r.peakKVRatio)
		}
	}
}

// TestUNI283EndpointNewcomer: item (c) -- app2 joins a saturated pool.
func TestUNI283EndpointNewcomer(t *testing.T) {
	skipUnlessSim(t)
	fmt.Println("| shape | thr / max-num-seqs | clamp | first app2 dispatch (s, median of 5) | first app2 request starts (s, median of 5) | minutes to 90% of entitlement (median) | vLLM FIFO wait mean (s) |")
	fmt.Println("|---|---|---|---|---|---|---|")
	for _, sh := range epShapes {
		for _, clamp := range []bool{true, false} {
			var picks, starts, ninetys, fifo []float64
			for seed := int64(1); seed <= 5; seed++ {
				prm := epBase(sh)
				prm.seed = seed
				prm.tenants[1].joinAt = prm.warmup
				prm.trackJoin = "app2"
				prm.window = 2400
				prm.noClamp = !clamp
				r := runEndpoints(t, prm)
				picks = append(picks, r.firstPick)
				starts = append(starts, r.firstStart)
				n := r.toNinety
				if n < 0 {
					n = 99
				}
				ninetys = append(ninetys, n)
				fifo = append(fifo, r.fifoWaitMean)
			}
			fmt.Printf("| %s | %.2f | %v | %.0f | %.0f | %.0f | %.0f |\n", sh.name, 32/float64(sh.maxSeqs), clamp,
				medianOf(picks), medianOf(starts), medianOf(ninetys), medianOf(fifo))
		}
	}
}

// TestUNI283Preemption: KV-bound endpoints with vLLM-style preemption, across
// kvCacheUtilThreshold values. Token usage blocks never report recompute, so
// the plugin's charge is blind to it; this measures who pays it in GPU time.
func TestUNI283Preemption(t *testing.T) {
	skipUnlessSim(t)
	fmt.Println("| shape | kvCacheUtilThreshold | effective concurrency (configured) | split app1/app2/end-users | max-dev | kvRatio mean / peak | preemptions per 100 dispatches app1/app2/end-users | recompute share of slot-time app1/app2/end-users |")
	fmt.Println("|---|---|---|---|---|---|---|---|")
	for _, sh := range []epShape{epShapes[1], epShapes[2]} {
		for _, kt := range []float64{0.8, 0.6, 0.5} {
			prm := epBase(sh)
			prm.preempt, prm.prefillTokPerSec, prm.kvThr = true, 5000, kt
			prm.warmup, prm.window = 3600, 1800
			r := runEndpoints(t, prm)
			pp, rc := "", ""
			for i, id := range []string{"app1", "app2", "end-users"} {
				if i > 0 {
					pp += "/"
					rc += "/"
				}
				pp += fmt.Sprintf("%.1f", 100*r.preemptions[id]/math.Max(1, r.dispatches[id]))
				rc += fmt.Sprintf("%.2f%%", 100*r.recomputeS[id]/math.Max(1e-9, r.slotS[id]))
			}
			fmt.Printf("| %s | %.1f | %.0f (%d) | %s | %.1f | %.2f / %.2f | %s | %s |\n", sh.name, kt, r.meanRunning, sh.endpoints*sh.maxSeqs,
				fmtShares(r.share), r.maxDev, r.meanKVRatio, r.peakKVRatio, pp, rc)
		}
	}
}
