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

// UNI-283 desk audit: the long-request regime.
//
// This drives the REAL plugin (Pick / PreRequest / ResponseBody, fake clock)
// against a slot model of the backend, to ask one question the corpus cannot:
// what split does the policy deliver when requests hold a slot for minutes
// rather than seconds? Nothing here is a regression test; every case is
// skipped unless UNI283_SIM=1, and it prints tables rather than asserting.
//
// Slot model: `slots` concurrent sequences (2 replicas x --max-num-seqs 8 =
// 16), fed FIFO from a model-server waiting queue of depth `vllmQueue`. The
// EPP dispatches (Pick + PreRequest) only while that waiting queue is below
// vllmQueue -- the utilization-detector gate, reduced to its queue limb.
// vllmQueue=0 is the ideal case where the EPP feeds slots directly.
// Every tenant is continuously backlogged with an identical request-size
// distribution, so the ideal slot-time share is exactly the weight share.

import (
	"context"
	"fmt"
	"math"
	"math/rand"
	"os"
	"strings"
	"testing"
	"time"

	"github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol"
	fwkfcmocks "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol/mocks"
	fwkrc "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requestcontrol"
	fwkrh "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requesthandling"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

const decodeTokPerSec = 27.0 // UNI-150: ~8100 tokens over ~300s at full batch

type lrTenant struct {
	id     string
	weight float64
	// next returns (service seconds, output tokens, max_tokens or 0) for the
	// next request this tenant sends.
	next func(r *rand.Rand) (float64, int, int64)
}

type lrReq struct {
	tenant  string
	req     *fwksched.InferenceRequest
	service float64
	output  int
	endAt   float64
}

type lrParams struct {
	slots      int
	vllmQueue  int
	halfLife   float64
	costModel  string
	warmup     float64 // seconds before the scoring window opens
	window     float64 // scoring window length, seconds
	tick       float64
	seed       int64
	tenants    []lrTenant
	promptToks int
}

type lrResult struct {
	share     map[string]float64 // slot-seconds share inside the window
	longSlotS map[string]float64 // slot-seconds on requests longer than 1s
	decisions int                // Picks taken inside the window
	maxDev    float64            // max |share - weight share|, points
}

func runLongRegime(t *testing.T, prm lrParams) lrResult {
	t.Helper()
	cfg := DefaultConfig()
	cfg.Enforce = true
	cfg.StateLogIntervalSeconds = 0
	cfg.HalfLifeSeconds = prm.halfLife
	if prm.costModel != "" {
		cfg.CostModel = prm.costModel
	}
	var wsum float64
	for _, tn := range prm.tenants {
		cfg.Groups = append(cfg.Groups, GroupConfig{Name: tn.id, Weight: tn.weight, Match: GroupMatch{Exact: []string{tn.id}}})
		wsum += tn.weight
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "unclassified", Weight: 1}
	p, clock := newTestPlugin(t, cfg)
	state := p.NewState(context.Background())
	rng := rand.New(rand.NewSource(prm.seed))
	ctx := context.Background()

	accessor := func() flowcontrol.PriorityBandAccessor {
		var active []flowcontrol.FlowQueueAccessor
		for _, tn := range prm.tenants {
			active = append(active, &fwkfcmocks.MockFlowQueueAccessor{
				LenV: 1000, FlowKeyV: flowcontrol.FlowKey{ID: tn.id},
				PeekV: &fwkfcmocks.MockQueueItemAccessor{EnqueueTimeV: clock.now()},
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
	byID := map[string]lrTenant{}
	for _, tn := range prm.tenants {
		byID[tn.id] = tn
	}

	var running []*lrReq
	var waiting []*lrReq
	occ := map[string]float64{}
	occLong := map[string]float64{}
	decisions := 0
	seq := 0
	end := prm.warmup + prm.window
	for now := 0.0; now < end; now += prm.tick {
		inWin := now >= prm.warmup
		// completions
		keep := running[:0]
		for _, r := range running {
			if r.endAt <= now {
				p.ResponseBody(ctx, r.req, &fwkrc.Response{
					EndOfStream: true, TerminationCause: fwkrc.TerminationCauseNatural,
					Usage: fwkrh.Usage{PromptTokens: prm.promptToks, CompletionTokens: r.output,
						TotalTokens:        prm.promptToks + r.output,
						PromptTokenDetails: &fwkrh.PromptTokenDetails{}},
				}, nil)
				continue
			}
			keep = append(keep, r)
		}
		running = keep
		startFIFO := func() {
			for len(running) < prm.slots && len(waiting) > 0 {
				r := waiting[0]
				waiting = waiting[1:]
				r.endAt = now + r.service
				running = append(running, r)
			}
		}
		startFIFO()
		// EPP dispatch: while the model server's waiting queue is below the
		// gate (or, with vllmQueue=0, while a slot is free), Pick and charge.
		for {
			if prm.vllmQueue == 0 && len(running)+len(waiting) >= prm.slots {
				break
			}
			if prm.vllmQueue > 0 && len(waiting) >= prm.vllmQueue {
				break
			}
			q, err := p.Pick(ctx, accessor())
			if err != nil || q == nil {
				t.Fatalf("pick: %v %v", q, err)
			}
			id := q.FlowKey().ID
			s, out, mt := byID[id].next(rng)
			body := &fwkrh.InferenceRequestBody{}
			if mt > 0 {
				body.MaxOutputTokens = &mt
			}
			seq++
			req := &fwksched.InferenceRequest{RequestID: fmt.Sprintf("%s-%d", id, seq), FairnessID: id,
				Body: body, RequestSizeBytes: prm.promptToks * 4}
			if err := p.PreRequest(ctx, req, nil); err != nil {
				t.Fatal(err)
			}
			if inWin {
				decisions++
			}
			waiting = append(waiting, &lrReq{tenant: id, req: req, service: s, output: out})
			startFIFO()
		}
		if inWin {
			for _, r := range running {
				occ[r.tenant] += prm.tick
				if r.service > 1 {
					occLong[r.tenant] += prm.tick
				}
			}
		}
		clock.advance(time.Duration(prm.tick * float64(time.Second)))
	}
	var total float64
	for _, v := range occ {
		total += v
	}
	res := lrResult{share: map[string]float64{}, longSlotS: occLong, decisions: decisions}
	for _, tn := range prm.tenants {
		res.share[tn.id] = 100 * occ[tn.id] / total
		d := math.Abs(res.share[tn.id] - 100*tn.weight/wsum)
		if d > res.maxDev {
			res.maxDev = d
		}
	}
	return res
}

func fixedService(s float64) func(*rand.Rand) (float64, int, int64) {
	return func(*rand.Rand) (float64, int, int64) { return s, int(s * decodeTokPerSec), 0 }
}

// lognormal with the given median and p95 service time.
func lognormalService(median, p95 float64) func(*rand.Rand) (float64, int, int64) {
	sigma := math.Log(p95/median) / 1.6449
	return func(r *rand.Rand) (float64, int, int64) {
		s := median * math.Exp(sigma*r.NormFloat64())
		if s < 1 {
			s = 1
		}
		return s, int(s * decodeTokPerSec), 0
	}
}

func boardTenants(gen func() func(*rand.Rand) (float64, int, int64)) []lrTenant {
	return []lrTenant{
		{id: "app1", weight: 20, next: gen()},
		{id: "app2", weight: 10, next: gen()},
		{id: "end-users", weight: 65, next: gen()},
	}
}

func skipUnlessSim(t *testing.T) {
	if os.Getenv("UNI283_SIM") != "1" {
		t.Skip("UNI-283 desk simulation; set UNI283_SIM=1 to run")
	}
}

type lrSummary struct {
	meanShare map[string]float64
	meanDev   float64
	passFrac  float64
	decisions float64
}

func sweep(t *testing.T, base lrParams, seeds int) lrSummary {
	sum := lrSummary{meanShare: map[string]float64{}}
	pass := 0
	for s := 0; s < seeds; s++ {
		prm := base
		prm.seed = int64(1000 + s)
		r := runLongRegime(t, prm)
		for k, v := range r.share {
			sum.meanShare[k] += v / float64(seeds)
		}
		sum.meanDev += r.maxDev / float64(seeds)
		sum.decisions += float64(r.decisions) / float64(seeds)
		if r.maxDev <= 10 {
			pass++
		}
	}
	sum.passFrac = float64(pass) / float64(seeds)
	return sum
}

func fmtLongregimeShare(m map[string]float64) string {
	keys := []string{"app1", "app2", "end-users"}
	parts := make([]string, 0, 3)
	for _, k := range keys {
		parts = append(parts, fmt.Sprintf("%.1f", m[k]))
	}
	return strings.Join(parts, "/")
}

// TestUNI283FixedServiceSweep: every request holds its slot for exactly S.
func TestUNI283FixedServiceSweep(t *testing.T) {
	skipUnlessSim(t)
	fmt.Println("| S (s) | H (s) | vLLM queue | window | decisions/min | share app1/app2/end-users (ideal 21.1/10.5/68.4) | mean max-dev pts | seeds within 10 pts |")
	fmt.Println("|---|---|---|---|---|---|---|---|")
	for _, s := range []float64{15, 60, 120, 300, 720} {
		for _, h := range []float64{60, 300, 1800} {
			for _, vq := range []int{0, 48} {
				for _, win := range []struct {
					name   string
					warmup float64
				}{{"cold 0-30m", 0}, {"steady 30m", 4 * 3600}} {
					prm := lrParams{slots: 16, vllmQueue: vq, halfLife: h, warmup: win.warmup, window: 1800,
						tick: 1, promptToks: 200, tenants: boardTenants(func() func(*rand.Rand) (float64, int, int64) { return fixedService(s) })}
					// fixed service is deterministic apart from phase; 3 seeds suffice
					r := sweep(t, prm, 3)
					fmt.Printf("| %.0f | %.0f | %d | %s | %.1f | %s | %.1f | %.0f%% |\n", s, h, vq, win.name,
						r.decisions/30, fmtLongregimeShare(r.meanShare), r.meanDev, 100*r.passFrac)
				}
			}
		}
	}
}

// TestUNI283BoardDistribution: lognormal, median 60s, p95 6 or 12 minutes.
func TestUNI283BoardDistribution(t *testing.T) {
	skipUnlessSim(t)
	fmt.Println("| median/p95 (s) | H (s) | vLLM queue | window | decisions/min | share app1/app2/end-users | mean max-dev pts | seeds within 10 pts |")
	fmt.Println("|---|---|---|---|---|---|---|---|")
	for _, p95 := range []float64{360, 720} {
		for _, h := range []float64{60, 300, 1800} {
			for _, vq := range []int{0, 48} {
				for _, win := range []struct {
					name   string
					warmup float64
				}{{"cold 0-30m", 0}, {"steady 30m", 4 * 3600}} {
					pp := p95
					prm := lrParams{slots: 16, vllmQueue: vq, halfLife: h, warmup: win.warmup, window: 1800,
						tick: 1, promptToks: 200, tenants: boardTenants(func() func(*rand.Rand) (float64, int, int64) { return lognormalService(60, pp) })}
					r := sweep(t, prm, 20)
					fmt.Printf("| 60/%.0f | %.0f | %d | %s | %.1f | %s | %.1f | %.0f%% |\n", p95, h, vq, win.name,
						r.decisions/30, fmtLongregimeShare(r.meanShare), r.meanDev, 100*r.passFrac)
				}
			}
		}
	}
}

// TestUNI283EWMAGaming: two equal-weight tenants. "honest" sends only long
// requests. "gamer" sends the same long requests but interleaves cheap
// one-token requests to drag its per-group output EWMA down, and omits
// max_tokens throughout so the EWMA is the whole estimate. Measures the
// share of slot-time each gets.
func TestUNI283EWMAGaming(t *testing.T) {
	skipUnlessSim(t)
	fmt.Println("| long S (s) | H (s) | cheap per long | honest share | gamer share | gamer long-request slot-time / honest slot-time |")
	fmt.Println("|---|---|---|---|---|---|")
	for _, s := range []float64{60, 300, 720} {
		for _, h := range []float64{60, 300, 1800} {
			for _, cheap := range []int{0, 3, 15, 63} {
				ss, cc := s, cheap
				n := 0
				gamer := func(*rand.Rand) (float64, int, int64) {
					n++
					if cc > 0 && n%(cc+1) != 0 {
						return 1, 1, 0
					}
					return ss, int(ss * decodeTokPerSec), 0
				}
				prm := lrParams{slots: 16, vllmQueue: 0, halfLife: h, warmup: 4 * 3600, window: 3600, tick: 1, promptToks: 200,
					tenants: []lrTenant{
						{id: "honest", weight: 50, next: fixedService(s)},
						{id: "gamer", weight: 50, next: gamer},
					}}
				r := runLongRegime(t, prm)
				fmt.Printf("| %.0f | %.0f | %d | %.1f | %.1f | %.2fx |\n", s, h, cheap, r.share["honest"], r.share["gamer"],
					r.longSlotS["gamer"]/r.longSlotS["honest"])
			}
		}
	}
}

// TestUNI283BoardWindows: does a longer scoring window or a longer half-life
// resolve the split for the median-60s / p95-720s distribution?
func TestUNI283BoardWindows(t *testing.T) {
	skipUnlessSim(t)
	fmt.Println("| H (s) | vLLM queue | window (min) | decisions in window | share app1/app2/end-users | mean max-dev pts | seeds within 10 pts |")
	fmt.Println("|---|---|---|---|---|---|---|")
	for _, h := range []float64{60, 300, 1800, 3600} {
		for _, vq := range []int{0, 48} {
			for _, win := range []float64{1800, 7200} {
				prm := lrParams{slots: 16, vllmQueue: vq, halfLife: h, warmup: 4 * 3600, window: win,
					tick: 1, promptToks: 200, tenants: boardTenants(func() func(*rand.Rand) (float64, int, int64) { return lognormalService(60, 720) })}
				r := sweep(t, prm, 20)
				fmt.Printf("| %.0f | %d | %.0f | %.0f | %s | %.1f | %.0f%% |\n", h, vq, win/60, r.decisions,
					fmtLongregimeShare(r.meanShare), r.meanDev, 100*r.passFrac)
			}
		}
	}
}

// TestUNI283GamingVRAMTime: the EWMA-gaming case under costModel vramtime.
func TestUNI283GamingVRAMTime(t *testing.T) {
	skipUnlessSim(t)
	fmt.Println("| cost model | long S (s) | H (s) | cheap per long | gamer long-request slot-time / honest slot-time |")
	fmt.Println("|---|---|---|---|---|")
	for _, cm := range []string{CostModelTokens, CostModelVRAMTime} {
		for _, s := range []float64{300, 720} {
			for _, cheap := range []int{0, 3, 15} {
				ss, cc := s, cheap
				n := 0
				gamer := func(*rand.Rand) (float64, int, int64) {
					n++
					if cc > 0 && n%(cc+1) != 0 {
						return 1, 1, 0
					}
					return ss, int(ss * decodeTokPerSec), 0
				}
				prm := lrParams{slots: 16, vllmQueue: 0, halfLife: 60, costModel: cm, warmup: 4 * 3600, window: 3600, tick: 1, promptToks: 200,
					tenants: []lrTenant{
						{id: "honest", weight: 50, next: fixedService(s)},
						{id: "gamer", weight: 50, next: gamer},
					}}
				r := runLongRegime(t, prm)
				fmt.Printf("| %s | %.0f | 60 | %d | %.2fx |\n", cm, s, cheap, r.longSlotS["gamer"]/r.longSlotS["honest"])
			}
		}
	}
}
