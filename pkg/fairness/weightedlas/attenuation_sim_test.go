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

// UNI-288: reproduce UNI-282 Arm A's ~10% weight attenuation.
//
// Arm A: 32 closed-loop workers per tenant (equal offered load), weights
// 20/10/65 (+ idle unclassified 5), queueDepthThreshold 32, two vLLM replicas
// at --max-num-seqs 8, short non-streaming requests. Observed live 32.3/30.9/36.7
// at ~22.5 req/s with per-tenant e2e p50 4.41/4.57/3.86 s.
//
// The UNI-283 harness keeps every tenant infinitely backlogged. This one closes
// the loop: each worker has exactly one request outstanding, which sits in the
// tenant's EPP flow queue, then (once Picked) in an endpoint's FIFO waiting
// queue, then in a slot, and is resubmitted the instant it completes. The EPP
// dispatches only while the saturation gate is open: mean per-endpoint waiting
// below queueDepthThreshold, read from a metrics snapshot that refreshes every
// `staleness` seconds. Skipped unless UNI283_SIM=1.

import (
	"context"
	"fmt"
	"math"
	"math/rand"
	"os"
	"sort"
	"testing"
	"time"

	"github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol"
	fwkfcmocks "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol/mocks"
	fwkrc "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requestcontrol"
	fwkrh "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requesthandling"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

type clParams struct {
	workers    map[string]int // closed-loop workers per tenant; <=0 = infinite backlog
	endpoints  int
	seqs       int     // --max-num-seqs per endpoint
	threshold  float64 // queueDepthThreshold (mean waiting per endpoint)
	staleness  float64 // seconds between saturation-metric refreshes
	service    float64 // mean slot-holding time, seconds
	duration   float64
	tick       float64
	seed       int64
	halfLife   float64
	promptToks int
	outToks    int
	maxTokens  int64

	// UNI-290 extensions; zero values reproduce UNI-288 exactly.
	admission    string                // "" depth gate only; "comp-epp" / "comp" / "comp-cost": weighted in-flight cap (see compEligible)
	compFloor    int                   // "comp", "comp-cost": release regardless while total released < compFloor (GPU-level work conservation)
	vllmPriority bool                  // vLLM waiting queue ordered by a priority stamped at dispatch (normalized service), not FCFS
	serviceMul   map[string]float64    // per-tenant multiplier on slot-hold time and output tokens (default 1)
	idle         map[string][2]float64 // tenant stops submitting during [from,to), then returns with its full worker count

	// UNI-290 round 2: the saturation detector decides only whether the cap
	// is active; it never blocks dispatch by itself (threshold still can).
	detector                string           // "pool" or "endpoint"; "" keeps the round-1 paths
	capThr                  float64          // queue limb: waiting per endpoint at which an endpoint counts as saturated
	kvThr                   float64          // KV limb: kv utilisation at which an endpoint counts as saturated (0 = limb off)
	kvCaps                  []float64        // per-endpoint KV capacity in tokens (0 = unlimited); vLLM admits only what fits
	affinity                map[string][]int // tenant -> home endpoints (prefix-cache affinity)
	affSlack                float64          // extra waiting a non-home endpoint must save to win
	capUnit                 string           // "" / "count": requests; "oracle": true output tokens; "ewma": min(max_tokens, per-tenant output EWMA 1/64)
	gamer                   string           // tenant sending 3 short (0.05x) requests per long (gamerLong x) one
	gamerLong               float64
	staleOnly               bool   // detector reads only the 50 ms snapshot, no EPP-local count of dispatches since
	prioStamp               string // "" = tenant's normalized service at dispatch; "sfq" = start-time fair queueing tag (monotone per tenant)
	sfqCost                 string // SFQ tag increment: "" = 1/w per request; "oracle" = true tokens/w; "ewma" = dispatch estimate/w
	sfqVFrom                string // SFQ virtual time advances on "" = request start (needs a first-token signal); "complete" = completion
	underCapIgnoresAffinity bool   // route a request from a tenant under its cap share by queue depth alone
	gamerTightMax           bool   // the gamer's short requests carry max_tokens = their true output (UNI-283's vector)
	sfqTrueUp               bool   // at completion, move the tenant's SFQ tag by (true cost - estimate)/w, undecayed
}

type clDecision struct {
	at      float64
	winner  string
	norm    map[string]float64 // normalized service of every queued group, read just before Pick
	argmin  string
	spread  float64 // (max-min)/min of norm over queued groups
	queued  int
	eppHeld int
}

type clResult struct {
	dispatch    map[string]int
	share       map[string]float64
	firstThird  map[string]float64
	lastThird   map[string]float64
	latency     map[string]float64 // mean e2e seconds
	meanEPPHeld float64
	heldBy      map[string]float64 // time-averaged EPP flow-queue depth per tenant
	zeroFrac    map[string]float64 // fraction of samples with that tenant's queue empty
	meanBackend float64
	throughput  float64
	decisions   []clDecision

	completedBy map[string]int
	compShare   map[string]float64 // share of completions (what the tenants were actually served)
	eppWait     map[string]float64 // mean seconds held at the EPP
	vllmWait    map[string]float64 // mean seconds in vLLM's waiting queue
	meanWaiting float64            // time-averaged vLLM waiting, summed over endpoints
	meanRunning float64            // time-averaged running, summed over endpoints
	slotDipFrac float64            // % of samples with a free slot while the EPP held requests
	slotShare   map[string]float64 // share of slot-seconds served (GPU-time composition)
	p99Lat      map[string]float64 // e2e seconds
	maxLat      map[string]float64
	series      []clWindow
}

// clWindow is one 1-second sample of the time series.
type clWindow struct {
	at        float64
	completed map[string]int
	waiting   float64 // mean over the window
	running   float64
	held      map[string]float64
}

type clReq struct {
	tenant   string
	req      *fwksched.InferenceRequest
	arrived  float64
	enqueued time.Time
	service  float64
	endAt    float64
	released float64 // when the EPP forwarded it
	started  float64 // when it got a slot
	prio     float64 // vLLM priority stamp (lower is served first)
	mul      float64 // slot-hold and output-token multiplier for this request
	est      float64 // cap load charged while in flight
	kv       float64 // KV tokens held while running
	maxTok   float64 // max_tokens the client sent
	inc      float64 // SFQ tag increment charged at dispatch
}

var armAWeights = map[string]float64{"app1": 20, "app2": 10, "end-users": 65}

// compEligible implements UNI-290's weighted in-flight admission. A tenant
// with queued requests may be released while released_i/Σreleased <= w_i,
// with w normalized over tenants that have demand (queued or in flight).
// If no queued tenant qualifies, "comp-epp" releases anyway (work
// conservation at the EPP queue: bind only while an under-cap tenant is
// waiting); "comp" releases anyway only while Σreleased < floor (work
// conservation at the GPU: bind while the backend has enough work).
//
// load is what the cap counts per tenant: released requests, or (comp-cost)
// their expected slot-time.
func compEligible(mode string, floor int, eppQ map[string][]*clReq, released map[string]int, load map[string]float64) map[string]bool {
	var wsum, ltot float64
	tot := 0
	for _, tn := range armATenants {
		ltot += load[tn]
		if len(eppQ[tn]) > 0 || released[tn] > 0 {
			wsum += armAWeights[tn]
		}
		tot += released[tn]
	}
	out := map[string]bool{}
	for _, tn := range armATenants {
		if len(eppQ[tn]) > 0 && (tot == 0 || load[tn] <= armAWeights[tn]/wsum*ltot) {
			out[tn] = true
		}
	}
	if len(out) > 0 {
		return out
	}
	if mode == "comp-epp" || tot < floor {
		for _, tn := range armATenants {
			if len(eppQ[tn]) > 0 {
				out[tn] = true
			}
		}
	}
	return out
}

var armATenants = []string{"app1", "app2", "end-users"}

func armAConfig(halfLife float64) Config {
	cfg := DefaultConfig()
	cfg.NewcomerClamp = os.Getenv("UNI288_NOCLAMP") != "1"
	if os.Getenv("UNI288_NOPROV") == "1" {
		cfg.ProvisionalCharge = false
	}
	cfg.Enforce = true
	cfg.StateLogIntervalSeconds = 0
	cfg.HalfLifeSeconds = halfLife
	cfg.Groups = []GroupConfig{
		{Name: "app1", Weight: 20, Match: GroupMatch{Exact: []string{"app1"}}},
		{Name: "app2", Weight: 10, Match: GroupMatch{Exact: []string{"app2"}}},
		{Name: "end-users", Weight: 65, Match: GroupMatch{Exact: []string{"end-users"}}},
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "unclassified", Weight: 5}
	return cfg
}

func runClosedLoop(t *testing.T, prm clParams) clResult {
	t.Helper()
	p, clock := newTestPlugin(t, armAConfig(prm.halfLife))
	state := p.NewState(context.Background())
	ctx := context.Background()
	rng := rand.New(rand.NewSource(prm.seed))
	start := clock.now()
	tsec := func() float64 { return clock.now().Sub(start).Seconds() }

	eppQ := map[string][]*clReq{}
	waiting := make([][]*clReq, prm.endpoints)
	running := make([][]*clReq, prm.endpoints)
	seq := 0
	nthReq := map[string]int{}
	newReq := func(tenant string) *clReq {
		seq++
		nthReq[tenant]++
		m := 1.0
		if v, ok := prm.serviceMul[tenant]; ok {
			m = v
		}
		if tenant == prm.gamer {
			m = 0.05
			if nthReq[tenant]%4 == 0 {
				m = prm.gamerLong
			}
		}
		mt := prm.maxTokens
		body := &fwkrh.InferenceRequestBody{}
		if mt > 0 {
			body.MaxOutputTokens = &mt
		}
		maxTok := float64(prm.maxTokens)
		if tenant == prm.gamer && prm.gamerTightMax && m < 1 {
			maxTok = math.Ceil(float64(prm.outToks) * m)
		}
		return &clReq{tenant: tenant, arrived: tsec(), enqueued: clock.now(), mul: m, maxTok: maxTok,
			req: &fwksched.InferenceRequest{RequestID: fmt.Sprintf("%s-%d", tenant, seq), FairnessID: tenant,
				Body: body, RequestSizeBytes: prm.promptToks * 4}}
	}
	infinite := map[string]bool{}
	for _, tn := range armATenants {
		n := prm.workers[tn]
		if n <= 0 {
			infinite[tn] = true
			n = 1
		}
		for i := 0; i < n; i++ {
			eppQ[tn] = append(eppQ[tn], newReq(tn))
		}
	}

	accessor := func(eligible map[string]bool) flowcontrol.PriorityBandAccessor {
		var active []flowcontrol.FlowQueueAccessor
		for _, tn := range armATenants {
			if len(eppQ[tn]) == 0 || (eligible != nil && !eligible[tn]) {
				continue
			}
			active = append(active, &fwkfcmocks.MockFlowQueueAccessor{
				LenV: len(eppQ[tn]), FlowKeyV: flowcontrol.FlowKey{ID: tn},
				PeekV: &fwkfcmocks.MockQueueItemAccessor{EnqueueTimeV: eppQ[tn][0].enqueued},
			})
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

	res := clResult{dispatch: map[string]int{}, share: map[string]float64{}, firstThird: map[string]float64{},
		lastThird: map[string]float64{}, latency: map[string]float64{}}
	third := map[int]map[string]float64{0: {}, 2: {}}
	latSum := map[string]float64{}
	latN := map[string]float64{}
	var heldSum, backendSum, samples float64
	heldBy := map[string]float64{}
	zeroN := map[string]float64{}
	nextRefresh := 0.0
	gateMean := 0.0
	completed := 0
	released := map[string]int{}
	res.completedBy = map[string]int{}
	eppWaitSum, vllmWaitSum := map[string]float64{}, map[string]float64{}
	lats := map[string][]float64{}
	slotSec := map[string]float64{}
	kvUsed := make([]float64, prm.endpoints)
	kvCap := func(e int) float64 {
		if e < len(prm.kvCaps) && prm.kvCaps[e] > 0 {
			return prm.kvCaps[e]
		}
		return math.Inf(1)
	}
	fits := func(e int, r *clReq) bool { return len(running[e]) < prm.seqs && kvUsed[e]+r.kv <= kvCap(e) }
	releasedLoad := map[string]float64{}
	ewma := map[string]float64{}
	for _, tn := range armATenants {
		ewma[tn] = float64(prm.outToks)
	}
	snapW, snapKV, since := make([]float64, prm.endpoints), make([]float64, prm.endpoints), make([]float64, prm.endpoints)
	snapFree := make([]float64, prm.endpoints)
	// estWaiting: the EPP's view of an endpoint's waiting queue: the last
	// scrape, plus what it dispatched there since, less the slots that
	// scrape showed free (num_requests_running). It cannot see KV room.
	estWaiting := func(e int) float64 {
		if prm.staleOnly {
			return snapW[e]
		}
		return math.Max(0, snapW[e]+since[e]-snapFree[e])
	}
	typical := float64(prm.promptToks + prm.outToks)
	wEst := 0.0 // EWMA of vLLM queue wait, seconds (what an EPP can measure as TTFT minus prefill)
	sfqLast, sfqV := map[string]float64{}, 0.0
	var waitingSum, runningSum, dipN float64
	var win *clWindow
	var winN float64
	active := func(tn string, now float64) bool {
		w, ok := prm.idle[tn]
		return !ok || now < w[0] || now >= w[1]
	}

	for now := 0.0; now < prm.duration; now = tsec() {
		// completions, then resubmission by the same closed-loop worker
		for e := range running {
			keep := running[e][:0]
			for _, r := range running[e] {
				if r.endAt > now {
					keep = append(keep, r)
					continue
				}
				p.ResponseBody(ctx, r.req, &fwkrc.Response{
					EndOfStream: true, TerminationCause: fwkrc.TerminationCauseNatural,
					Usage: fwkrh.Usage{PromptTokens: prm.promptToks, CompletionTokens: int(float64(prm.outToks) * r.mul),
						TotalTokens:        prm.promptToks + int(float64(prm.outToks)*r.mul),
						PromptTokenDetails: &fwkrh.PromptTokenDetails{}},
				}, nil)
				latSum[r.tenant] += now - r.arrived
				latN[r.tenant]++
				completed++
				released[r.tenant]--
				releasedLoad[r.tenant] -= r.est
				kvUsed[e] -= r.kv
				ewma[r.tenant] += (float64(prm.outToks)*r.mul - ewma[r.tenant]) / 64
				wEst += (r.started - r.released - wEst) / 64
				if prm.sfqVFrom == "complete" {
					sfqV = math.Max(sfqV, r.prio)
				}
				if prm.sfqTrueUp {
					sfqLast[r.tenant] += (r.mul - r.inc) / armAWeights[r.tenant]
				}
				slotSec[r.tenant] += r.service
				lats[r.tenant] = append(lats[r.tenant], now-r.arrived)
				res.completedBy[r.tenant]++
				eppWaitSum[r.tenant] += r.released - r.arrived
				vllmWaitSum[r.tenant] += r.started - r.released
				if win != nil {
					win.completed[r.tenant]++
				}
				if !infinite[r.tenant] && active(r.tenant, now) {
					eppQ[r.tenant] = append(eppQ[r.tenant], newReq(r.tenant))
				}
			}
			running[e] = keep
			for len(waiting[e]) > 0 {
				i := 0
				if prm.vllmPriority {
					for j, w := range waiting[e] {
						if w.prio < waiting[e][i].prio {
							i = j
						}
					}
				}
				r := waiting[e][i]
				if !fits(e, r) {
					break // vLLM stops admitting at the first request that does not fit
				}
				waiting[e] = append(waiting[e][:i], waiting[e][i+1:]...)
				kvUsed[e] += r.kv
				r.endAt = now + r.service
				r.started = now
				if prm.sfqVFrom == "" {
					sfqV = math.Max(sfqV, r.prio)
				}
				running[e] = append(running[e], r)
			}
		}
		// a tenant returning from idle comes back with its full worker count
		for tn := range prm.idle {
			if infinite[tn] || !active(tn, now) {
				continue
			}
			for n := len(eppQ[tn]) + released[tn]; n < prm.workers[tn]; n++ {
				eppQ[tn] = append(eppQ[tn], newReq(tn))
			}
		}
		if now >= nextRefresh {
			tot := 0
			for e := range waiting {
				tot += len(waiting[e])
			}
			gateMean = float64(tot) / float64(prm.endpoints)
			nextRefresh = now + prm.staleness
			for e := range waiting {
				snapW[e], since[e] = float64(len(waiting[e])), 0
				snapFree[e] = float64(prm.seqs - len(running[e]))
				snapKV[e] = 0
				if c := kvCap(e); !math.IsInf(c, 1) {
					snapKV[e] = kvUsed[e] / c
				}
			}
		}
		if prm.detector != "" {
			satOf := func(e int) float64 {
				s := estWaiting(e) / prm.capThr
				if prm.kvThr > 0 {
					s = math.Max(s, snapKV[e]/prm.kvThr)
				}
				return s
			}
			for n := 0; gateMean < prm.threshold && float64(n) < prm.tick/0.001; n++ {
				var cands []int
				capActive := false
				if prm.detector == "endpoint" {
					for e := range waiting {
						if satOf(e) < 1 {
							cands = append(cands, e)
						}
					}
					capActive = len(cands) == 0
				} else {
					// pool-wide mean of each limb, as the current detector reads it
					var mw, mk float64
					for e := range waiting {
						mw += estWaiting(e) / float64(prm.endpoints)
						mk += snapKV[e] / float64(prm.endpoints)
					}
					pool := mw / prm.capThr
					if prm.kvThr > 0 {
						pool = math.Max(pool, mk/prm.kvThr)
					}
					capActive = pool >= 1
				}
				if len(cands) == 0 {
					for e := range waiting {
						cands = append(cands, e)
					}
				}
				var eligible map[string]bool
				if capActive {
					load := map[string]float64{}
					for _, tn := range armATenants {
						load[tn] = float64(released[tn])
						if prm.capUnit != "" && prm.capUnit != "count" {
							load[tn] = releasedLoad[tn]
						}
					}
					eligible = compEligible("comp", 0, eppQ, released, load)
				}
				norm := map[string]float64{}
				queued := 0
				for _, tn := range armATenants {
					if len(eppQ[tn]) > 0 && (eligible == nil || eligible[tn]) {
						norm[tn] = p.stateFor(tn).normalizedService(clock.now())
						queued++
					}
				}
				if queued == 0 {
					break
				}
				q, err := p.Pick(ctx, accessor(eligible))
				if err != nil || q == nil {
					t.Fatalf("pick: %v %v", q, err)
				}
				id := q.FlowKey().ID
				r := eppQ[id][0]
				if infinite[id] {
					eppQ[id][0] = newReq(id)
				} else {
					eppQ[id] = eppQ[id][1:]
				}
				r.prio = norm[id]
				if prm.prioStamp == "sfq" {
					inc := 1.0
					switch prm.sfqCost {
					case "oracle":
						inc = r.mul
					case "ewma":
						inc = math.Min(r.maxTok, ewma[id]) / float64(prm.outToks)
					}
					r.inc = inc
					r.prio = math.Max(sfqLast[id], sfqV)
					sfqLast[id] = r.prio + inc/armAWeights[id]
				}
				if err := p.PreRequest(ctx, r.req, nil); err != nil {
					t.Fatal(err)
				}
				res.dispatch[id]++
				released[id]++
				r.released = now
				tok := float64(prm.outToks) * r.mul
				r.kv = float64(prm.promptToks) + tok
				switch prm.capUnit {
				case "oracle":
					r.est = tok
				case "ewma":
					r.est = math.Min(r.maxTok, ewma[id])
				case "sojourn": // expected time in vLLM: queue wait + oracle service
					r.est = wEst + prm.service*r.mul
				case "sojourn-ewma":
					r.est = wEst + prm.service*math.Min(float64(prm.maxTokens), ewma[id])/float64(prm.outToks)
				default:
					r.est = 1
				}
				releasedLoad[id] += r.est
				home := map[int]bool{}
				for _, e := range prm.affinity[id] {
					home[e] = true
				}
				if prm.underCapIgnoresAffinity {
					load := map[string]float64{}
					for _, tn := range armATenants {
						load[tn] = float64(released[tn])
					}
					if compEligible("comp", 0, eppQ, released, load)[id] || len(eppQ[id]) == 0 {
						home = nil
					}
				}
				score := func(e int) float64 {
					v := estWaiting(e)
					if len(home) > 0 && !home[e] {
						v += prm.affSlack
					}
					return v + 0.01*float64(len(running[e]))/float64(prm.seqs)
				}
				best := cands[0]
				for _, e := range cands[1:] {
					if score(e) < score(best) {
						best = e
					}
				}
				since[best]++
				r.service = r.mul * prm.service * math.Exp(0.15*rng.NormFloat64()-0.5*0.15*0.15)
				if len(waiting[best]) == 0 && fits(best, r) {
					kvUsed[best] += r.kv
					r.endAt = now + r.service
					r.started = now
					running[best] = append(running[best], r)
				} else {
					waiting[best] = append(waiting[best], r)
				}
			}
		}
		// EPP dispatch while the (possibly stale) saturation gate is open.
		// Each dispatch in the same staleness window bumps the local estimate
		// by nothing: that is exactly the overshoot a 50ms scrape produces.
		// The dispatch loop runs on a ~1ms cadence, so at most tick/1ms Picks.
		for n := 0; prm.detector == "" && gateMean < prm.threshold && float64(n) < prm.tick/0.001; n++ {
			var eligible map[string]bool
			if prm.admission != "" {
				load := map[string]float64{}
				for _, tn := range armATenants {
					load[tn] = float64(released[tn])
					if prm.admission == "comp-cost" {
						if m, ok := prm.serviceMul[tn]; ok {
							load[tn] *= m
						}
					}
				}
				eligible = compEligible(prm.admission, prm.compFloor, eppQ, released, load)
			}
			acc := accessor(eligible)
			norm := map[string]float64{}
			queued := 0
			for _, tn := range armATenants {
				if len(eppQ[tn]) > 0 && (eligible == nil || eligible[tn]) {
					norm[tn] = p.stateFor(tn).normalizedService(clock.now())
					queued++
				}
			}
			if queued == 0 {
				break
			}
			q, err := p.Pick(ctx, acc)
			if err != nil || q == nil {
				t.Fatalf("pick: %v %v", q, err)
			}
			id := q.FlowKey().ID
			r := eppQ[id][0]
			if infinite[id] {
				eppQ[id][0] = newReq(id)
			} else {
				eppQ[id] = eppQ[id][1:]
			}
			r.prio = norm[id]
			if err := p.PreRequest(ctx, r.req, nil); err != nil {
				t.Fatal(err)
			}
			res.dispatch[id]++
			released[id]++
			r.released = now
			if b := int(3 * now / prm.duration); b == 0 || b == 2 {
				third[b][id]++
			}
			if queued > 1 {
				d := clDecision{at: now, winner: id, norm: norm, queued: queued}
				lo, hi := math.Inf(1), math.Inf(-1)
				for tn, v := range norm {
					if v < lo || (v == lo && tn < d.argmin) {
						lo, d.argmin = v, tn
					}
					hi = math.Max(hi, v)
				}
				if lo > 0 {
					d.spread = (hi - lo) / lo
				}
				for _, tn := range armATenants {
					d.eppHeld += len(eppQ[tn])
				}
				res.decisions = append(res.decisions, d)
			}
			// queue-scorer endpoint pick: shortest waiting, then fewest running
			best := 0
			for e := 1; e < prm.endpoints; e++ {
				if len(waiting[e])+len(running[e]) < len(waiting[best])+len(running[best]) {
					best = e
				}
			}
			r.kv = float64(prm.promptToks) + float64(prm.outToks)*r.mul
			r.service = r.mul * prm.service * math.Exp(0.15*rng.NormFloat64()-0.5*0.15*0.15)
			if len(waiting[best]) == 0 && fits(best, r) {
				kvUsed[best] += r.kv
				r.endAt = now + r.service
				r.started = now
				running[best] = append(running[best], r)
			} else {
				waiting[best] = append(waiting[best], r)
			}
			if prm.staleness <= 0 {
				tot := 0
				for e := range waiting {
					tot += len(waiting[e])
				}
				gateMean = float64(tot) / float64(prm.endpoints)
			}
		}
		if now > prm.duration/10 {
			for _, tn := range armATenants {
				if !infinite[tn] {
					heldSum += float64(len(eppQ[tn]))
					heldBy[tn] += float64(len(eppQ[tn]))
					if len(eppQ[tn]) == 0 {
						zeroN[tn]++
					}
				}
			}
			held, nw, nr := 0, 0, 0
			for _, tn := range armATenants {
				held += len(eppQ[tn])
			}
			for e := range waiting {
				backendSum += float64(len(waiting[e]) + len(running[e]))
				nw += len(waiting[e])
				nr += len(running[e])
			}
			waitingSum += float64(nw)
			runningSum += float64(nr)
			// idle capacity: an endpoint with nothing waiting and room for a
			// typical request while the EPP is holding work
			if held > 0 {
				for e := range waiting {
					if len(waiting[e]) == 0 && len(running[e]) < prm.seqs && kvUsed[e]+typical <= kvCap(e) {
						dipN++
						break
					}
				}
			}
			samples++
		}
		// 1-second time series from t=0 (includes warm-up, for convergence)
		if win == nil || now >= win.at+1 {
			if win != nil {
				win.waiting /= winN
				win.running /= winN
				for tn := range win.held {
					win.held[tn] /= winN
				}
				res.series = append(res.series, *win)
			}
			win = &clWindow{at: math.Floor(now), completed: map[string]int{}, held: map[string]float64{}}
			winN = 0
		}
		for e := range waiting {
			win.waiting += float64(len(waiting[e]))
			win.running += float64(len(running[e]))
		}
		for _, tn := range armATenants {
			win.held[tn] += float64(len(eppQ[tn]))
		}
		winN++
		clock.advance(time.Duration(prm.tick * float64(time.Second)))
	}
	total := 0
	for _, n := range res.dispatch {
		total += n
	}
	pct := func(m map[string]float64) map[string]float64 {
		var s float64
		for _, v := range m {
			s += v
		}
		out := map[string]float64{}
		for k, v := range m {
			out[k] = 100 * v / s
		}
		return out
	}
	for _, tn := range armATenants {
		res.share[tn] = 100 * float64(res.dispatch[tn]) / float64(total)
		if latN[tn] > 0 {
			res.latency[tn] = latSum[tn] / latN[tn]
		}
	}
	res.firstThird = pct(third[0])
	res.lastThird = pct(third[2])
	res.meanEPPHeld = heldSum / samples
	res.heldBy, res.zeroFrac = map[string]float64{}, map[string]float64{}
	for _, tn := range armATenants {
		res.heldBy[tn] = heldBy[tn] / samples
		res.zeroFrac[tn] = 100 * zeroN[tn] / samples
	}
	res.meanBackend = backendSum / samples
	res.meanWaiting, res.meanRunning, res.slotDipFrac = waitingSum/samples, runningSum/samples, 100*dipN/samples
	res.compShare, res.eppWait, res.vllmWait = map[string]float64{}, map[string]float64{}, map[string]float64{}
	res.p99Lat, res.maxLat = map[string]float64{}, map[string]float64{}
	res.slotShare = pctOf(slotSec)
	for _, tn := range armATenants {
		if l := lats[tn]; len(l) > 0 {
			sort.Float64s(l)
			res.p99Lat[tn], res.maxLat[tn] = l[int(0.99*float64(len(l)-1))], l[len(l)-1]
		}
		res.compShare[tn] = 100 * float64(res.completedBy[tn]) / float64(completed)
		if c := float64(res.completedBy[tn]); c > 0 {
			res.eppWait[tn], res.vllmWait[tn] = eppWaitSum[tn]/c, vllmWaitSum[tn]/c
		}
	}
	res.throughput = float64(completed) / prm.duration
	return res
}

// travelled is UNI-282's attenuation metric: the fraction of the way each
// group moved from the equal-worker share toward its weight share.
func travelled(share map[string]float64, workerShare map[string]float64) map[string]float64 {
	target := map[string]float64{"app1": 100 * 20.0 / 95, "app2": 100 * 10.0 / 95, "end-users": 100 * 65.0 / 95}
	out := map[string]float64{}
	for _, tn := range armATenants {
		out[tn] = 100 * (share[tn] - workerShare[tn]) / (target[tn] - workerShare[tn])
	}
	return out
}

func fmt3(m map[string]float64) string {
	return fmt.Sprintf("%.1f/%.1f/%.1f", m["app1"], m["app2"], m["end-users"])
}

func armAParams(workers int) clParams {
	return clParams{
		workers:   map[string]int{"app1": workers, "app2": workers, "end-users": workers},
		endpoints: 2, seqs: 8, threshold: 32, staleness: 0.05,
		// 16 slots at ~22.5 req/s live => ~0.71 s per slot-hold.
		service: 0.71, duration: 900, tick: 0.005, seed: 1, halfLife: 60,
		promptToks: 1600, outToks: 64, maxTokens: 64,
	}
}

var equalThirds = map[string]float64{"app1": 100.0 / 3, "app2": 100.0 / 3, "end-users": 100.0 / 3}

// TestUNI288ArmA: step 1. Infinite backlog (the UNI-283 harness's assumption)
// versus 32 closed-loop workers per tenant (what Arm A actually offered).
func TestUNI288ArmA(t *testing.T) {
	skipUnlessSim(t)
	fmt.Println("| offered load | share app1/app2/end-users | % travelled toward weights | e2e latency s | mean EPP-held | mean in backend | req/s |")
	fmt.Println("|---|---|---|---|---|---|---|")
	for _, c := range []struct {
		name    string
		workers int
	}{{"infinite backlog", 0}, {"32 workers/tenant (Arm A)", 32}, {"128 workers/tenant", 128}, {"256 workers/tenant", 256}} {
		r := runClosedLoop(t, armAParams(c.workers))
		fmt.Printf("| %s | %s | %s | %s | %.1f | %.1f | %.1f |\n", c.name, fmt3(r.share),
			fmt3(travelled(r.share, equalThirds)), fmt3(r.latency), r.meanEPPHeld, r.meanBackend, r.throughput)
	}
}

// TestUNI288Decisions: step 3. Argmin match rate and ranking spread, plus the
// warm-up cut, at the Arm A shape.
func TestUNI288Decisions(t *testing.T) {
	skipUnlessSim(t)
	r := runClosedLoop(t, armAParams(32))
	match := 0
	var spreads []float64
	queuedHist := map[int]int{}
	winsWhenQueued := map[string][2]int{}
	for _, d := range r.decisions {
		if d.winner == d.argmin {
			match++
		}
		spreads = append(spreads, d.spread)
		queuedHist[d.queued]++
		for tn := range d.norm {
			w := winsWhenQueued[tn]
			w[1]++
			if tn == d.winner {
				w[0]++
			}
			winsWhenQueued[tn] = w
		}
	}
	sort.Float64s(spreads)
	q := func(f float64) float64 { return spreads[int(f*float64(len(spreads)-1))] }
	total := 0
	for _, n := range r.dispatch {
		total += n
	}
	fmt.Printf("dispatches %d, contended decisions (>1 group queued) %d (%.1f%%)\n", total, len(r.decisions), 100*float64(len(r.decisions))/float64(total))
	fmt.Printf("argmin match %d/%d = %.2f%%\n", match, len(r.decisions), 100*float64(match)/float64(len(r.decisions)))
	fmt.Printf("ranking spread (max-min)/min over queued groups: p10 %.3f p50 %.3f p90 %.3f\n", q(0.1), q(0.5), q(0.9))
	fmt.Printf("groups queued at contended decisions: 2=%d 3=%d\n", queuedHist[2], queuedHist[3])
	for _, tn := range armATenants {
		w := winsWhenQueued[tn]
		fmt.Printf("  %s: queued at %d contended decisions, won %d\n", tn, w[1], w[0])
	}
	fmt.Printf("time-averaged EPP-held per tenant %s (total %.1f), queue empty %% of time %s\n", fmt3(r.heldBy), r.meanEPPHeld, fmt3(r.zeroFrac))
	fmt.Printf("warm-up cut: first third %s, last third %s, whole %s\n", fmt3(r.firstThird), fmt3(r.lastThird), fmt3(r.share))
}

// TestUNI288Levers: seed spread at Arm A, then the knobs that change how much
// of the closed-loop population the EPP holds.
func TestUNI288Levers(t *testing.T) {
	skipUnlessSim(t)
	fmt.Println("| variant | share app1/app2/end-users | % travelled | mean EPP-held / 96 | mean in backend | req/s |")
	fmt.Println("|---|---|---|---|---|---|")
	row := func(name string, prm clParams) {
		r := runClosedLoop(t, prm)
		fmt.Printf("| %s | %s | %s | %.1f | %.1f | %.1f |\n", name, fmt3(r.share),
			fmt3(travelled(r.share, equalThirds)), r.meanEPPHeld, r.meanBackend, r.throughput)
	}
	for s := int64(1); s <= 5; s++ {
		prm := armAParams(32)
		prm.seed = s
		row(fmt.Sprintf("Arm A seed %d", s), prm)
	}
	for _, h := range []float64{60, 300, 900} {
		prm := armAParams(32)
		prm.halfLife = h
		row(fmt.Sprintf("halfLife %.0f", h), prm)
	}
	for _, st := range []float64{0, 0.05, 0.2} {
		prm := armAParams(32)
		prm.staleness = st
		row(fmt.Sprintf("staleness %.2fs", st), prm)
	}
	for _, thr := range []float64{32, 16, 8, 4, 2, 1} {
		prm := armAParams(32)
		prm.threshold = thr
		row(fmt.Sprintf("queueDepthThreshold %.0f", thr), prm)
	}
}

func pctOf(m map[string]float64) map[string]float64 {
	var s float64
	for _, v := range m {
		s += v
	}
	out := map[string]float64{}
	for k, v := range m {
		out[k] = 100 * v / s
	}
	return out
}
