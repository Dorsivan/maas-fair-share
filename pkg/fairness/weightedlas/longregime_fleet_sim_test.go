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

// UNI-283 review round: the same slot model as longregime_sim_test.go,
// generalised to (a) an ~800-slot fleet, (b) a tenant joining mid-run, and
// (c) several EPP replicas, each with its own plugin instance and tabs,
// dispatching into one shared backend. Skipped unless UNI283_SIM=1.
//
// Multi-EPP model: every dispatch opportunity (the shared model-server queue
// is below the gate) goes to one EPP chosen uniformly at random among those
// that currently hold backlog -- independent EPPs racing the same saturation
// signal. Each EPP then picks among only the tenants whose traffic reaches it.

import (
	"context"
	"fmt"
	"math"
	"math/rand"
	"strings"
	"testing"
	"time"

	"github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol"
	fwkfcmocks "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol/mocks"
	fwkrc "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requestcontrol"
	fwkrh "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requesthandling"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

type flTenant struct {
	lrTenant
	joinAt float64 // seconds; backlogged from then on
	epps   []int   // EPP replicas this tenant's traffic reaches; nil = all
}

type flParams struct {
	slots      int
	queueRatio float64 // model-server waiting-queue gate as a multiple of slots (thr/max-num-seqs); 0 = feed slots directly
	epps       int
	halfLife   float64
	costModel  string
	warmup     float64
	window     float64
	seed       int64
	tenants    []flTenant
	// trackJoin, when set, records per-minute occupancy of that tenant after it joins.
	trackJoin string
}

type flResult struct {
	share      map[string]float64
	maxDev     float64
	longSlotS  map[string]float64
	firstStart float64   // seconds from trackJoin's join to its first request starting
	joinOcc    []float64 // per-minute mean slots held by trackJoin after joining
}

type flEPP struct {
	p     *Plugin
	clock *fakeClock
	state any
}

func runFleet(t *testing.T, prm flParams) flResult {
	t.Helper()
	ctx := context.Background()
	var wsum float64
	for _, tn := range prm.tenants {
		wsum += tn.weight
	}
	epps := make([]flEPP, prm.epps)
	for i := range epps {
		cfg := DefaultConfig()
		cfg.Enforce = true
		cfg.StateLogIntervalSeconds = 0
		cfg.HalfLifeSeconds = prm.halfLife
		if prm.costModel != "" {
			cfg.CostModel = prm.costModel
		}
		for _, tn := range prm.tenants {
			cfg.Groups = append(cfg.Groups, GroupConfig{Name: tn.id, Weight: tn.weight, Match: GroupMatch{Exact: []string{tn.id}}})
		}
		cfg.DefaultGroup = DefaultGroupConfig{Name: "unclassified", Weight: 1}
		p, clock := newTestPlugin(t, cfg)
		epps[i] = flEPP{p: p, clock: clock, state: p.NewState(ctx)}
	}
	reaches := func(tn flTenant, e int) bool {
		if tn.epps == nil {
			return true
		}
		for _, x := range tn.epps {
			if x == e {
				return true
			}
		}
		return false
	}
	present := func(e int, now float64) []flTenant {
		var out []flTenant
		for _, tn := range prm.tenants {
			if now >= tn.joinAt && reaches(tn, e) {
				out = append(out, tn)
			}
		}
		return out
	}
	accessor := func(e int, now float64) flowcontrol.PriorityBandAccessor {
		var active []flowcontrol.FlowQueueAccessor
		for _, tn := range present(e, now) {
			active = append(active, &fwkfcmocks.MockFlowQueueAccessor{
				LenV: 1000, FlowKeyV: flowcontrol.FlowKey{ID: tn.id},
				PeekV: &fwkfcmocks.MockQueueItemAccessor{EnqueueTimeV: epps[e].clock.now()},
			})
		}
		return &fwkfcmocks.MockPriorityBandAccessor{
			PolicyStateV: epps[e].state,
			IterateQueuesFunc: func(cb func(flowcontrol.FlowQueueAccessor) bool) {
				for _, q := range active {
					if !cb(q) {
						return
					}
				}
			},
		}
	}
	byID := map[string]flTenant{}
	for _, tn := range prm.tenants {
		byID[tn.id] = tn
	}
	type req struct {
		lrReq
		epp int
	}
	rng := rand.New(rand.NewSource(prm.seed))
	var running, waiting []*req
	occ, occLong := map[string]float64{}, map[string]float64{}
	res := flResult{share: map[string]float64{}, firstStart: -1}
	var joinAt float64
	if prm.trackJoin != "" {
		joinAt = byID[prm.trackJoin].joinAt
	}
	var minuteAcc float64
	seq := 0
	gate := int(prm.queueRatio * float64(prm.slots))
	end := prm.warmup + prm.window
	for now := 0.0; now < end; now++ {
		keep := running[:0]
		for _, r := range running {
			if r.endAt <= now {
				epps[r.epp].p.ResponseBody(ctx, r.req, &fwkrc.Response{
					EndOfStream: true, TerminationCause: fwkrc.TerminationCauseNatural,
					Usage: fwkrh.Usage{PromptTokens: 200, CompletionTokens: r.output,
						TotalTokens: 200 + r.output, PromptTokenDetails: &fwkrh.PromptTokenDetails{}},
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
				if r.tenant == prm.trackJoin && res.firstStart < 0 && now >= joinAt {
					res.firstStart = now - joinAt
				}
			}
		}
		startFIFO()
		var withBacklog []int
		for e := range epps {
			if len(present(e, now)) > 0 {
				withBacklog = append(withBacklog, e)
			}
		}
		for len(withBacklog) > 0 {
			if gate == 0 && len(running)+len(waiting) >= prm.slots {
				break
			}
			if gate > 0 && len(waiting) >= gate {
				break
			}
			e := withBacklog[rng.Intn(len(withBacklog))]
			q, err := epps[e].p.Pick(ctx, accessor(e, now))
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
			ir := &fwksched.InferenceRequest{RequestID: fmt.Sprintf("%s-%d", id, seq), FairnessID: id,
				Body: body, RequestSizeBytes: 800}
			if err := epps[e].p.PreRequest(ctx, ir, nil); err != nil {
				t.Fatal(err)
			}
			waiting = append(waiting, &req{lrReq: lrReq{tenant: id, req: ir, service: s, output: out}, epp: e})
			startFIFO()
		}
		if now >= prm.warmup {
			for _, r := range running {
				occ[r.tenant]++
				if r.service > 1 {
					occLong[r.tenant]++
				}
			}
		}
		if prm.trackJoin != "" && now >= joinAt {
			for _, r := range running {
				if r.tenant == prm.trackJoin {
					minuteAcc++
				}
			}
			if int(now-joinAt)%60 == 59 {
				res.joinOcc = append(res.joinOcc, minuteAcc/60)
				minuteAcc = 0
			}
		}
		for i := range epps {
			epps[i].clock.advance(time.Second)
		}
	}
	var total float64
	for _, v := range occ {
		total += v
	}
	for _, tn := range prm.tenants {
		res.share[tn.id] = 100 * occ[tn.id] / total
		if d := math.Abs(res.share[tn.id] - 100*tn.weight/wsum); d > res.maxDev {
			res.maxDev = d
		}
	}
	res.longSlotS = occLong
	return res
}

func boardFleetTenants(median, p95 float64) []flTenant {
	var out []flTenant
	for _, tn := range boardTenants(func() func(*rand.Rand) (float64, int, int64) { return lognormalService(median, p95) }) {
		out = append(out, flTenant{lrTenant: tn})
	}
	return out
}

func fmtShares(m map[string]float64) string {
	keys := []string{"app1", "app2", "end-users"}
	parts := make([]string, 0, len(keys))
	for _, k := range keys {
		parts = append(parts, fmt.Sprintf("%.1f", m[k]))
	}
	return strings.Join(parts, "/")
}

// TestUNI283Scale: does the dispatch-gap bias vanish at ~800 slots?
func TestUNI283Scale(t *testing.T) {
	skipUnlessSim(t)
	fmt.Println("| slots | H (s) | queue gate (x slots) | app2 dispatch gap (s) | split app1/app2/end-users (ideal 21.1/10.5/68.4) | mean max-dev | seeds within 10 pts | seeds within 5 pts |")
	fmt.Println("|---|---|---|---|---|---|---|---|")
	for _, slots := range []int{16, 800} {
		seeds := 20
		if slots == 800 {
			seeds = 5
		}
		for _, h := range []float64{60, 300} {
			for _, qr := range []float64{0, 3} {
				share := map[string]float64{}
				var dev float64
				pass10, pass5 := 0, 0
				for s := 0; s < seeds; s++ {
					r := runFleet(t, flParams{slots: slots, queueRatio: qr, epps: 1, halfLife: h,
						warmup: 4 * 3600, window: 1800, seed: int64(2000 + s), tenants: boardFleetTenants(60, 720)})
					for k, v := range r.share {
						share[k] += v / float64(seeds)
					}
					dev += r.maxDev / float64(seeds)
					if r.maxDev <= 10 {
						pass10++
					}
					if r.maxDev <= 5 {
						pass5++
					}
				}
				gap := 187.8 / (0.1053 * float64(slots))
				fmt.Printf("| %d | %.0f | %.0f | %.1f | %s | %.1f | %d/%d | %d/%d |\n", slots, h, qr, gap, fmtShares(share), dev, pass10, seeds, pass5, seeds)
			}
		}
	}
}

// TestUNI283Gaming800: the EWMA-gaming case on an 800-slot pool.
func TestUNI283Gaming800(t *testing.T) {
	skipUnlessSim(t)
	fmt.Println("| slots | cost model | long S (s) | H (s) | cheap per long | gamer long-request slot-time / honest slot-time |")
	fmt.Println("|---|---|---|---|---|---|")
	for _, slots := range []int{16, 800} {
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
					r := runFleet(t, flParams{slots: slots, epps: 1, halfLife: 60, costModel: cm, warmup: 2 * 3600, window: 3600, seed: 7,
						tenants: []flTenant{
							{lrTenant: lrTenant{id: "honest", weight: 50, next: fixedService(s)}},
							{lrTenant: lrTenant{id: "gamer", weight: 50, next: gamer}},
						}})
					fmt.Printf("| %d | %s | %.0f | 60 | %d | %.2fx |\n", slots, cm, s, cheap, r.longSlotS["gamer"]/r.longSlotS["honest"])
				}
			}
		}
	}
}

// TestUNI283Newcomer: app2 joins a saturated pool; how long until its first
// request starts, and until it holds its entitlement?
func TestUNI283Newcomer(t *testing.T) {
	skipUnlessSim(t)
	fmt.Println("| slots | queue gate (x slots) | H (s) | first request starts after (s, median of seeds) | minutes to reach 50% of entitlement | minutes to reach 90% |")
	fmt.Println("|---|---|---|---|---|---|")
	for _, slots := range []int{16, 800} {
		seeds := 9
		if slots == 800 {
			seeds = 3
		}
		for _, qr := range []float64{0, 0.25, 2, 4} {
			for _, h := range []float64{60, 300} {
				var firsts []float64
				var curve []float64
				for s := 0; s < seeds; s++ {
					ten := boardFleetTenants(60, 720)
					ten[1].joinAt = 3 * 3600 // app2
					r := runFleet(t, flParams{slots: slots, queueRatio: qr, epps: 1, halfLife: h,
						warmup: 3 * 3600, window: 3600, seed: int64(3000 + s), tenants: ten, trackJoin: "app2"})
					firsts = append(firsts, r.firstStart)
					if curve == nil {
						curve = make([]float64, len(r.joinOcc))
					}
					for i, v := range r.joinOcc {
						if i < len(curve) {
							curve[i] += v / float64(seeds)
						}
					}
				}
				ent := 0.1053 * float64(slots)
				reach := func(frac float64) string {
					for i, v := range curve {
						if v >= frac*ent {
							return fmt.Sprintf("%d", i+1)
						}
					}
					return ">60"
				}
				med := medianOf(firsts)
				fmt.Printf("| %d | %.2f | %.0f | %.0f | %s | %s |\n", slots, qr, h, med, reach(0.5), reach(0.9))
			}
		}
	}
}

func medianOf(xs []float64) float64 {
	c := append([]float64(nil), xs...)
	for i := range c {
		for j := i + 1; j < len(c); j++ {
			if c[j] < c[i] {
				c[i], c[j] = c[j], c[i]
			}
		}
	}
	return c[len(c)/2]
}

// TestUNI283MultiEPP: several EPP replicas, each with its own tabs, sharing
// one 800-slot backend.
func TestUNI283MultiEPP(t *testing.T) {
	skipUnlessSim(t)
	fmt.Println("| EPPs | traffic placement | split app1/app2/end-users (ideal 21.1/10.5/68.4) | max-dev pts |")
	fmt.Println("|---|---|---|---|")
	type placement struct {
		name string
		set  func(ten []flTenant, k int)
	}
	places := []placement{
		{"every tenant reaches every EPP (per-request load balancing)", func([]flTenant, int) {}},
		{"app2 sticky to EPP 0, others everywhere", func(ten []flTenant, _ int) { ten[1].epps = []int{0} }},
		{"app2 alone on EPP 0, others on the rest", func(ten []flTenant, k int) {
			ten[1].epps = []int{0}
			var rest []int
			for i := 1; i < k; i++ {
				rest = append(rest, i)
			}
			ten[0].epps, ten[2].epps = rest, rest
		}},
		{"end-users sticky to EPP 0, others everywhere", func(ten []flTenant, _ int) { ten[2].epps = []int{0} }},
	}
	for _, k := range []int{1, 2, 4} {
		for _, pl := range places {
			if k == 1 && pl.name != places[0].name {
				continue
			}
			ten := boardFleetTenants(60, 720)
			pl.set(ten, k)
			r := runFleet(t, flParams{slots: 800, queueRatio: 0, epps: k, halfLife: 60,
				warmup: 2 * 3600, window: 1800, seed: 11, tenants: ten})
			fmt.Printf("| %d | %s | %s | %.1f |\n", k, pl.name, fmtShares(r.share), r.maxDev)
		}
	}
}
