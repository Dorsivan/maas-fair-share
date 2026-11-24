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

// UNI-290: instead of holding more of the queue so the EPP owns its order,
// control the mix of what the EPP has released to vLLM (weighted in-flight
// admission, compEligible) and let vLLM's FIFO preserve that mix. Also models
// vLLM's priority scheduling policy with a priority stamped at dispatch.
// Same closed-loop harness and Arm A shape as UNI-288. Skipped unless UNI283_SIM=1.

import (
	"fmt"
	"math"
	"testing"
)

const noDepthGate = 1e9

func targetShare(active []string) map[string]float64 {
	var s float64
	for _, tn := range active {
		s += armAWeights[tn]
	}
	out := map[string]float64{}
	for _, tn := range active {
		out[tn] = 100 * armAWeights[tn] / s
	}
	return out
}

func maxDev(share, target map[string]float64) float64 {
	d := 0.0
	for tn, v := range target {
		d = math.Max(d, math.Abs(share[tn]-v))
	}
	return d
}

type uni290Variant struct {
	name string
	set  func(*clParams)
}

var uni290Variants = []uni290Variant{
	{"today: depth gate thr32, FCFS vLLM", func(p *clParams) {}},
	{"threshold lever: thr8", func(p *clParams) { p.threshold = 8 }},
	{"comp-epp (cap binds only while an under-cap tenant is queued at the EPP) + thr32", func(p *clParams) { p.admission = "comp-epp" }},
	{"comp (GPU-level work conservation, floor 16) + thr32", func(p *clParams) { p.admission, p.compFloor = "comp", 16 }},
	{"comp floor 16, no depth gate", func(p *clParams) { p.admission, p.compFloor, p.threshold = "comp", 16, noDepthGate }},
	{"comp floor 24, no depth gate", func(p *clParams) { p.admission, p.compFloor, p.threshold = "comp", 24, noDepthGate }},
	{"vLLM priority policy + thr32", func(p *clParams) { p.vllmPriority = true }},
	{"vLLM priority policy, no depth gate", func(p *clParams) { p.vllmPriority, p.threshold = true, noDepthGate }},
	{"comp floor 16 + vLLM priority, no depth gate", func(p *clParams) {
		p.admission, p.compFloor, p.threshold, p.vllmPriority = "comp", 16, noDepthGate, true
	}},
}

func uni290Row(name string, r clResult, target map[string]float64, slots int) {
	fmt.Printf("| %s | %s | %.1f | %.1f | %.1f | %.1f/%d | %.1f | %s | %s | %s | %s | %s |\n", name, fmt3(r.compShare),
		maxDev(r.compShare, target), r.throughput, r.meanWaiting, r.meanRunning, slots, r.slotDipFrac,
		fmt3(r.heldBy), fmt3(r.eppWait), fmt3(r.latency), fmt3(r.p99Lat), fmt3(r.maxLat))
}

const uni290Header = "| variant | served app1/app2/end-users | max dev pt | req/s | vLLM waiting | running | slot-dip % | EPP-held per tenant | EPP wait s | e2e mean s | e2e p99 s | e2e max s |\n|---|---|---|---|---|---|---|---|---|---|---|---|"

// TestUNI290Composition: measurements 1-4 at the Arm A shape, every variant, seeds 1-3.
func TestUNI290Composition(t *testing.T) {
	skipUnlessSim(t)
	target := targetShare(armATenants)
	fmt.Println(uni290Header)
	for _, v := range uni290Variants {
		for s := int64(1); s <= 3; s++ {
			prm := armAParams(32)
			prm.seed = s
			v.set(&prm)
			uni290Row(fmt.Sprintf("%s (seed %d)", v.name, s), runClosedLoop(t, prm), target, prm.endpoints*prm.seqs)
		}
	}
}

// TestUNI290Shapes: unequal and light offered load, where a cap could starve
// the GPU or a flood could defeat it.
func TestUNI290Shapes(t *testing.T) {
	skipUnlessSim(t)
	target := targetShare(armATenants)
	fmt.Println(uni290Header)
	for _, w := range [][3]int{{32, 32, 4}, {128, 32, 32}, {32, 32, 128}, {8, 8, 8}, {4, 4, 4}, {2, 2, 2}} {
		for _, v := range []uni290Variant{uni290Variants[0], uni290Variants[4], uni290Variants[7]} {
			prm := armAParams(32)
			prm.workers = map[string]int{"app1": w[0], "app2": w[1], "end-users": w[2]}
			v.set(&prm)
			uni290Row(fmt.Sprintf("%d/%d/%d workers: %s", w[0], w[1], w[2], v.name), runClosedLoop(t, prm), target, prm.endpoints*prm.seqs)
		}
	}
}

func windowShare(series []clWindow, from, to float64) (map[string]float64, float64, float64) {
	c := map[string]float64{}
	var tot, run, wait, n float64
	for _, w := range series {
		if w.at < from || w.at >= to {
			continue
		}
		for tn, k := range w.completed {
			c[tn] += float64(k)
			tot += float64(k)
		}
		run += w.running
		wait += w.waiting
		n++
	}
	for tn := range c {
		c[tn] = 100 * c[tn] / tot
	}
	return c, run / n, wait / n
}

// convergedAt: first window start after `from` from which every following
// 10-second window stays within tol of target until `to`.
func convergedAt(series []clWindow, target map[string]float64, from, to, tol float64) float64 {
	last := math.NaN()
	for s := to - 10; s >= from; s-- {
		sh, _, _ := windowShare(series, s, s+10)
		if maxDev(sh, target) > tol {
			break
		}
		last = s
	}
	return last - from
}

// TestUNI290Convergence: measurement 5. Cold start, then one tenant idles
// for 150 s and returns (the work-conservation path).
func TestUNI290Convergence(t *testing.T) {
	skipUnlessSim(t)
	full := targetShare(armATenants)
	fmt.Println("| variant | idle tenant | settle from cold s | pre-idle served | idle-phase served (target) | settle after return s | post-return served | running pre/idle/post | vLLM waiting pre/idle/post |")
	fmt.Println("|---|---|---|---|---|---|---|---|---|")
	for _, v := range []uni290Variant{uni290Variants[0], uni290Variants[4], uni290Variants[7]} {
		for _, idle := range []string{"end-users", "app1"} {
			prm := armAParams(32)
			prm.duration = 600
			prm.idle = map[string][2]float64{idle: {300, 450}}
			v.set(&prm)
			r := runClosedLoop(t, prm)
			var rest []string
			for _, tn := range armATenants {
				if tn != idle {
					rest = append(rest, tn)
				}
			}
			idleT := targetShare(rest)
			pre, rp, wp := windowShare(r.series, 100, 300)
			// skip the first 10 s of the idle phase while the idle tenant's in-flight drains
			mid, rm, wm := windowShare(r.series, 310, 450)
			post, rq, wq := windowShare(r.series, 500, 600)
			fmt.Printf("| %s | %s | %.0f | %s (dev %.1f) | %s (%s, dev %.1f) | %.0f | %s (dev %.1f) | %.1f/%.1f/%.1f | %.1f/%.1f/%.1f |\n",
				v.name, idle, convergedAt(r.series, full, 0, 300, 3), fmt3(pre), maxDev(pre, full),
				fmt3(mid), fmt3(idleT), maxDev(mid, idleT), convergedAt(r.series, full, 450, 600, 3),
				fmt3(post), maxDev(post, full), rp, rm, rq, wp, wm, wq)
		}
	}
	// cold-start timeline, 5 s windows
	for _, v := range []uni290Variant{uni290Variants[0], uni290Variants[4]} {
		prm := armAParams(32)
		prm.duration = 60
		v.set(&prm)
		r := runClosedLoop(t, prm)
		fmt.Printf("cold start, %s:", v.name)
		for s := 0.0; s < 60; s += 5 {
			sh, run, _ := windowShare(r.series, s, s+5)
			fmt.Printf(" [%2.0fs %s run %.1f]", s, fmt3(sh), run)
		}
		fmt.Println()
	}
}

// TestUNI290Heterogeneous: app1's requests hold a slot 3x longer. The cap
// counts requests, so check composition in GPU-time as well as in requests.
func TestUNI290Heterogeneous(t *testing.T) {
	skipUnlessSim(t)
	target := targetShare(armATenants)
	fmt.Println("| variant | requests served | slot-seconds served | slot-time max dev pt | req/s | running | vLLM waiting | e2e p99 s |")
	fmt.Println("|---|---|---|---|---|---|---|---|")
	for _, v := range []uni290Variant{uni290Variants[0], uni290Variants[4], uni290Variants[7],
		{"comp-cost (cap on expected slot-time, oracle estimate), floor 16, no depth gate", func(p *clParams) {
			p.admission, p.compFloor, p.threshold = "comp-cost", 16, noDepthGate
		}}} {
		prm := armAParams(32)
		prm.serviceMul = map[string]float64{"app1": 3}
		v.set(&prm)
		r := runClosedLoop(t, prm)
		fmt.Printf("| %s | %s | %s | %.1f | %.1f | %.1f | %.1f | %s |\n", v.name, fmt3(r.compShare), fmt3(r.slotShare),
			maxDev(r.slotShare, target), r.throughput, r.meanRunning, r.meanWaiting, fmt3(r.p99Lat))
	}
}

// ---- UNI-290 round 2 (Zeratul/board, 2026-11-24): the detector, not a slot
// count, decides whether the cap is active; per-endpoint vs pool-wide; cost vs
// count units; cap with and without vLLM priority.

func r2Row(name string, r clResult, target map[string]float64) {
	held := r.heldBy["app1"] + r.heldBy["app2"] + r.heldBy["end-users"]
	fmt.Printf("| %s | %s | %.1f | %.1f | %.1f | %.1f | %.1f | %.1f (%s) | %s | %s | %s |\n", name, fmt3(r.compShare),
		maxDev(r.compShare, target), r.throughput, r.meanRunning, r.slotDipFrac, r.meanWaiting, held, fmt3(r.heldBy),
		fmt3(r.latency), fmt3(r.p99Lat), fmt3(r.maxLat))
}

const r2Header = "| variant | served app1/app2/end-users | max dev | req/s | running | idle-capacity % | vLLM waiting | EPP-held (per tenant) | e2e mean s | e2e p99 s | e2e max s |\n|---|---|---|---|---|---|---|---|---|---|---|"

func detParams(workers int, det string, thr float64) clParams {
	p := armAParams(workers)
	p.detector, p.capThr, p.threshold = det, thr, noDepthGate
	return p
}

// TestUNI290R2Detector: change 1 at N=2. Detector-gated cap across the queue
// threshold; KV-limited endpoints; floors mis-sized in both directions.
func TestUNI290R2Detector(t *testing.T) {
	skipUnlessSim(t)
	target := targetShare(armATenants)
	typical := float64(1600 + 64)
	fmt.Println("### A. Arm A (slot-bound), per-endpoint vs pool detector across capThr\n" + r2Header)
	r2Row("round 1: slot floor 16", runClosedLoop(t, func() clParams { p := armAParams(32); uni290Variants[4].set(&p); return p }()), target)
	for _, thr := range []float64{1, 2, 4, 8, 16, 32} {
		for _, det := range []string{"endpoint", "pool"} {
			r2Row(fmt.Sprintf("%s detector, capThr %.0f", det, thr), runClosedLoop(t, detParams(32, det, thr)), target)
		}
	}
	p := detParams(32, "endpoint", 1)
	p.staleOnly = true
	r2Row("endpoint detector, capThr 1, 50 ms snapshot only (no EPP-local count)", runClosedLoop(t, p), target)

	fmt.Println("\n### B. KV-limited endpoints: kvCap = 5.5 typical requests, so 5 run per endpoint (10 effective of 16 configured)\n" + r2Header)
	kv := []float64{5.5 * typical, 5.5 * typical}
	for _, w := range [][3]int{{32, 32, 32}, {32, 32, 8}} {
		base := func() clParams {
			p := armAParams(32)
			p.workers = map[string]int{"app1": w[0], "app2": w[1], "end-users": w[2]}
			p.kvCaps = kv
			return p
		}
		lbl := fmt.Sprintf("%d/%d/%d workers: ", w[0], w[1], w[2])
		p := base()
		r2Row(lbl+"today thr32", runClosedLoop(t, p), target)
		p = base()
		uni290Variants[4].set(&p)
		r2Row(lbl+"slot floor 16 (> 10 effective)", runClosedLoop(t, p), target)
		for _, c := range []struct {
			name       string
			capThr, kv float64
		}{{"queue limb only, capThr 1", 1, 0}, {"KV limb only, kvThr 0.8", noDepthGate, 0.8},
			{"KV limb only, kvThr 1.04 (today's effective Filter limit)", noDepthGate, 1.04}, {"both limbs, capThr 1 + kvThr 0.8", 1, 0.8}} {
			p = base()
			p.detector, p.capThr, p.kvThr, p.threshold = "endpoint", c.capThr, c.kv, noDepthGate
			r2Row(lbl+"endpoint detector, "+c.name, runClosedLoop(t, p), target)
		}
	}

	fmt.Println("\n### B2. KV limb sizing, 32/32/8 workers, KV-limited (max achievable util 5/5.5 = 0.91), capThr 1\n" + r2Header)
	for _, k := range []float64{0.5, 0.6, 0.7, 0.8, 0.9, 0.95} {
		p := armAParams(32)
		p.workers = map[string]int{"app1": 32, "app2": 32, "end-users": 8}
		p.kvCaps = kv
		p.detector, p.capThr, p.kvThr, p.threshold = "endpoint", 1, k, noDepthGate
		r2Row(fmt.Sprintf("kvThr %.2f", k), runClosedLoop(t, p), target)
	}
	fmt.Println("\n### C. Floor sized too LOW: instances run 32 seqs (64 effective), floor still 16\n" + r2Header)
	p = armAParams(32)
	p.seqs = 32
	r2Row("today thr32", runClosedLoop(t, p), target)
	p = armAParams(32)
	p.seqs = 32
	uni290Variants[4].set(&p)
	r2Row("slot floor 16 (< 64 effective)", runClosedLoop(t, p), target)
	p = detParams(32, "endpoint", 1)
	p.seqs = 32
	r2Row("endpoint detector, capThr 1", runClosedLoop(t, p), target)
}

// TestUNI290R2Uneven: change 2. N=8 with uneven endpoint saturation, from
// heterogeneous KV capacity and from prefix-cache affinity.
func TestUNI290R2Uneven(t *testing.T) {
	skipUnlessSim(t)
	target := targetShare(armATenants)
	typical := float64(1600 + 64)
	n8 := func(det string, thr float64) clParams {
		p := detParams(128, det, thr)
		p.endpoints = 8
		if det == "" {
			p.threshold = 32
		}
		return p
	}
	fmt.Println("### N=8, heterogeneous KV: endpoints 0-3 slot-bound (8 run), 4-7 KV-bound (3 run); 44 effective; 128 workers/tenant\n" + r2Header)
	kv := []float64{0, 0, 0, 0, 3.5 * typical, 3.5 * typical, 3.5 * typical, 3.5 * typical}
	for _, c := range []struct {
		det     string
		thr, kv float64
	}{{"", 0, 0}, {"pool", 1, 0}, {"endpoint", 1, 0}, {"pool", 4, 0}, {"endpoint", 4, 0}, {"pool", noDepthGate, 0.8}, {"endpoint", noDepthGate, 0.8},
		{"pool", 1, 0.8}, {"endpoint", 1, 0.8}} {
		p := n8(c.det, c.thr)
		p.kvCaps, p.kvThr = kv, c.kv
		name := "today thr32"
		if c.det != "" {
			name = fmt.Sprintf("%s detector, capThr %g, kvThr %g", c.det, c.thr, c.kv)
		}
		r2Row(name, runClosedLoop(t, p), target)
	}
	fmt.Println("\n### N=8, prefix affinity: end-users home {0,1}, app1 {2,3,4}, app2 {5,6,7}; a non-home endpoint must be 8 waiting shorter to win\n" + r2Header)
	aff := map[string][]int{"end-users": {0, 1}, "app1": {2, 3, 4}, "app2": {5, 6, 7}}
	for _, c := range []struct {
		det string
		thr float64
	}{{"pool", 1}, {"endpoint", 1}, {"pool", 4}, {"endpoint", 4}} {
		p := n8(c.det, c.thr)
		p.affinity, p.affSlack = aff, 8
		r2Row(fmt.Sprintf("%s detector, capThr %g", c.det, c.thr), runClosedLoop(t, p), target)
	}
	fmt.Println("\n### N=8, shared prefix: every tenant's home is {0,1}; a non-home endpoint must be 16 waiting shorter to win\n" + r2Header)
	for _, w := range []int{64, 24} {
		for _, c := range []struct {
			det string
			thr float64
		}{{"pool", 1}, {"endpoint", 1}, {"pool", 4}, {"endpoint", 4}} {
			p := n8(c.det, c.thr)
			p.workers = map[string]int{"app1": w, "app2": w, "end-users": w}
			p.affinity, p.affSlack = map[string][]int{"end-users": {0, 1}, "app1": {0, 1}, "app2": {0, 1}}, 16
			r2Row(fmt.Sprintf("%d workers/tenant: %s detector, capThr %g", w, c.det, c.thr), runClosedLoop(t, p), target)
		}
	}
}

// TestUNI290R2Cost: change 3. Count vs cost units for the cap, honest and
// gamed workloads, across the vLLM queue depth the detector threshold allows.
func TestUNI290R2Cost(t *testing.T) {
	skipUnlessSim(t)
	target := targetShare(armATenants)
	fmt.Println("| workload | capThr | cap unit | requests served | slot-seconds served | slot-time max dev | vLLM waiting | running | idle-capacity % |")
	fmt.Println("|---|---|---|---|---|---|---|---|---|")
	for _, wl := range []string{"app1 3x longer (honest)", "app1 games: 3 short (0.05x) per long (10x)"} {
		for _, thr := range []float64{1, 4, 16} {
			for _, unit := range []string{"count", "oracle", "ewma", "sojourn", "sojourn-ewma"} {
				p := detParams(32, "endpoint", thr)
				p.capUnit, p.maxTokens = unit, 1024
				if wl[5] == '3' {
					p.serviceMul = map[string]float64{"app1": 3}
				} else {
					p.gamer, p.gamerLong = "app1", 10
				}
				r := runClosedLoop(t, p)
				fmt.Printf("| %s | %g | %s | %s | %s | %.1f | %.1f | %.1f | %.1f |\n", wl, thr, unit, fmt3(r.compShare), fmt3(r.slotShare),
					maxDev(r.slotShare, target), r.meanWaiting, r.meanRunning, r.slotDipFrac)
			}
		}
		for _, blk := range []float64{4, 1} {
			for _, unit := range []string{"count", "oracle", "sojourn"} {
				p := detParams(32, "endpoint", 1)
				p.capUnit, p.maxTokens, p.threshold = unit, 1024, blk
				if wl[5] == '3' {
					p.serviceMul = map[string]float64{"app1": 3}
				} else {
					p.gamer, p.gamerLong = "app1", 10
				}
				r := runClosedLoop(t, p)
				fmt.Printf("| %s | 1 + depth bound thr%g | %s | %s | %s | %.1f | %.1f | %.1f | %.1f |\n", wl, blk, unit, fmt3(r.compShare), fmt3(r.slotShare),
					maxDev(r.slotShare, target), r.meanWaiting, r.meanRunning, r.slotDipFrac)
			}
		}
		p := armAParams(32)
		p.maxTokens = 1024
		if wl[5] == '3' {
			p.serviceMul = map[string]float64{"app1": 3}
		} else {
			p.gamer, p.gamerLong = "app1", 10
		}
		r := runClosedLoop(t, p)
		fmt.Printf("| %s | today thr32 gate | none | %s | %s | %.1f | %.1f | %.1f | %.1f |\n", wl, fmt3(r.compShare), fmt3(r.slotShare),
			maxDev(r.slotShare, target), r.meanWaiting, r.meanRunning, r.slotDipFrac)
	}
}

// TestUNI290R2Priority: cap alone vs cap + vLLM priority as the detector
// threshold rises (higher threshold = the EPP holds less).
func TestUNI290R2Priority(t *testing.T) {
	skipUnlessSim(t)
	target := targetShare(armATenants)
	fmt.Println(r2Header)
	for _, thr := range []float64{1, 4, 8, 16, 24, 32, 48} {
		for _, mode := range []string{"", "norm", "sfq"} {
			for s := int64(1); s <= 2; s++ {
				p := detParams(32, "endpoint", thr)
				p.vllmPriority, p.seed = mode != "", s
				if mode == "sfq" {
					p.prioStamp = "sfq"
				}
				name := map[string]string{"": "cap alone", "norm": "cap + vLLM priority (normalized-service stamp)", "sfq": "cap + vLLM priority (SFQ start-tag stamp)"}[mode]
				r2Row(fmt.Sprintf("%s, capThr %g (seed %d)", name, thr, s), runClosedLoop(t, p), target)
			}
		}
	}
}

// sfqAlone: vLLM priority with an SFQ start tag stamped by the EPP, cap never
// active (capThr unreachable), optional depth gate.
func sfqAlone(workers int, depth float64) clParams {
	p := detParams(workers, "endpoint", noDepthGate)
	p.vllmPriority, p.prioStamp, p.threshold = true, "sfq", depth
	return p
}

// TestUNI290R2SFQ: stress the SFQ-stamped vLLM priority policy with no cap.
func TestUNI290R2SFQ(t *testing.T) {
	skipUnlessSim(t)
	target := targetShare(armATenants)
	typical := float64(1600 + 64)
	fmt.Println("### Arm A\n" + r2Header)
	for s := int64(1); s <= 3; s++ {
		p := sfqAlone(32, noDepthGate)
		p.seed = s
		r2Row(fmt.Sprintf("SFQ alone, no depth gate (seed %d)", s), runClosedLoop(t, p), target)
	}
	p := sfqAlone(32, 32)
	r2Row("SFQ alone + today's thr32 depth gate", runClosedLoop(t, p), target)
	p = sfqAlone(32, noDepthGate)
	p.sfqVFrom = "complete"
	r2Row("SFQ alone, virtual time from completions (no first-token signal)", runClosedLoop(t, p), target)
	p = sfqAlone(32, noDepthGate)
	p.staleOnly = true
	for _, w := range [][3]int{{32, 32, 4}, {128, 32, 32}, {8, 8, 8}, {256, 256, 256}} {
		p = sfqAlone(32, noDepthGate)
		p.workers = map[string]int{"app1": w[0], "app2": w[1], "end-users": w[2]}
		r2Row(fmt.Sprintf("SFQ alone, %d/%d/%d workers", w[0], w[1], w[2]), runClosedLoop(t, p), target)
	}
	p = sfqAlone(32, noDepthGate)
	p.kvCaps = []float64{5.5 * typical, 5.5 * typical}
	r2Row("SFQ alone, KV-limited (10 effective of 16)", runClosedLoop(t, p), target)
	p = sfqAlone(128, noDepthGate)
	p.endpoints = 8
	p.kvCaps = []float64{0, 0, 0, 0, 3.5 * typical, 3.5 * typical, 3.5 * typical, 3.5 * typical}
	r2Row("SFQ alone, N=8 heterogeneous KV, 128 workers", runClosedLoop(t, p), target)
	for _, w := range []int{64, 24} {
		p = sfqAlone(w, noDepthGate)
		p.endpoints = 8
		p.affinity, p.affSlack = map[string][]int{"end-users": {0, 1}, "app1": {0, 1}, "app2": {0, 1}}, 16
		r2Row(fmt.Sprintf("SFQ alone, N=8 shared prefix, %d workers", w), runClosedLoop(t, p), target)
	}

	fmt.Println("\n### Cap fix for affinity: a tenant under its cap share ignores prefix affinity (N=8 shared prefix)\n" + r2Header)
	for _, w := range []int{64, 24} {
		p = detParams(w, "endpoint", 1)
		p.endpoints = 8
		p.affinity, p.affSlack = map[string][]int{"end-users": {0, 1}, "app1": {0, 1}, "app2": {0, 1}}, 16
		p.underCapIgnoresAffinity = true
		r2Row(fmt.Sprintf("%d workers: endpoint detector capThr 1 + under-cap ignores affinity", w), runClosedLoop(t, p), target)
	}

	fmt.Println("\n### Unequal lengths: SFQ tag increment by request vs by cost\n| workload | tag increment | requests served | slot-seconds served | slot-time max dev | vLLM waiting | e2e p99 s | e2e max s |\n|---|---|---|---|---|---|---|---|")
	for _, wl := range []string{"app1 3x longer (honest)", "app1 games: 3 short (0.05x) per long (10x)"} {
		for _, c := range []string{"", "oracle", "ewma"} {
			p := sfqAlone(32, noDepthGate)
			p.sfqCost, p.maxTokens = c, 1024
			if wl[5] == '3' {
				p.serviceMul = map[string]float64{"app1": 3}
			} else {
				p.gamer, p.gamerLong = "app1", 10
			}
			r := runClosedLoop(t, p)
			name := map[string]string{"": "1/w per request", "oracle": "true cost/w", "ewma": "EWMA estimate/w"}[c]
			fmt.Printf("| %s | %s | %s | %s | %.1f | %.1f | %s | %s |\n", wl, name, fmt3(r.compShare), fmt3(r.slotShare),
				maxDev(r.slotShare, target), r.meanWaiting, fmt3(r.p99Lat), fmt3(r.maxLat))
		}
	}

	fmt.Println("\n### UNI-283 gaming vector: gamer's short requests send max_tokens = true output, dragging the EWMA used for its long ones\n| design | estimate | slot-seconds served | slot-time max dev | gamer gets vs 21.1 target |\n|---|---|---|---|---|")
	for _, c := range []struct {
		name, cost string
		trueUp     bool
	}{{"SFQ alone", "oracle", false}, {"SFQ alone", "ewma", false}, {"SFQ alone", "ewma", true}} {
		p := sfqAlone(32, noDepthGate)
		p.sfqCost, p.sfqTrueUp, p.maxTokens = c.cost, c.trueUp, 1024
		p.gamer, p.gamerLong, p.gamerTightMax = "app1", 10, true
		r := runClosedLoop(t, p)
		est := c.cost
		if c.trueUp {
			est += " + completion true-up (charging fix)"
		}
		fmt.Printf("| %s | %s | %s | %.1f | %.1f |\n", c.name, est, fmt3(r.slotShare), maxDev(r.slotShare, target), r.slotShare["app1"])
	}
	for _, unit := range []string{"count", "oracle", "ewma"} {
		p := detParams(32, "endpoint", 1)
		p.capUnit, p.maxTokens = unit, 1024
		p.gamer, p.gamerLong, p.gamerTightMax = "app1", 10, true
		r := runClosedLoop(t, p)
		fmt.Printf("| cap, endpoint detector capThr 1 | %s | %s | %.1f | %.1f |\n", unit, fmt3(r.slotShare), maxDev(r.slotShare, target), r.slotShare["app1"])
	}

	fmt.Println("\n### Idle/return and newcomer\n| variant | idle tenant | pre | idle phase (target) | post | settle after return s | running pre/idle/post | e2e max s |\n|---|---|---|---|---|---|---|---|")
	for _, idle := range []string{"end-users", "app1"} {
		p := sfqAlone(32, noDepthGate)
		p.duration = 600
		p.idle = map[string][2]float64{idle: {300, 450}}
		r := runClosedLoop(t, p)
		var rest []string
		for _, tn := range armATenants {
			if tn != idle {
				rest = append(rest, tn)
			}
		}
		pre, rp, _ := windowShare(r.series, 100, 300)
		mid, rm, _ := windowShare(r.series, 310, 450)
		post, rq, _ := windowShare(r.series, 500, 600)
		fmt.Printf("| SFQ alone | %s | %s | %s (%s) | %s | %.0f | %.1f/%.1f/%.1f | %s |\n", idle, fmt3(pre), fmt3(mid), fmt3(targetShare(rest)),
			fmt3(post), convergedAt(r.series, target, 450, 600, 3), rp, rm, rq, fmt3(r.maxLat))
	}
	for _, blk := range []float64{noDepthGate, 32} {
		p := sfqAlone(256, blk)
		p.duration = 600
		p.idle = map[string][2]float64{"app2": {0, 300}}
		r := runClosedLoop(t, p)
		j, _, _ := windowShare(r.series, 300, 330)
		sh, _, _ := windowShare(r.series, 450, 600)
		fmt.Printf("| SFQ alone, 256 workers/tenant, depth gate %g | app2 joins at 300 s | first 30 s after join %s | – | 450-600 s %s | %.0f | vLLM waiting %.1f | %s |\n",
			blk, fmt3(j), fmt3(sh), convergedAt(r.series, target, 300, 600, 3), r.meanWaiting, fmt3(r.maxLat))
	}
}

// TestUNI290R2Flood: with the detector only switching the cap, nothing bounds
// how much is released when every tenant floods. Newcomer app2 joins at 300 s.
func TestUNI290R2Flood(t *testing.T) {
	skipUnlessSim(t)
	target := targetShare(armATenants)
	fmt.Println("| variant | served 450-600 s | dev | served 300-330 s (first 30 s after app2 joins) | vLLM waiting | EPP-held | e2e p99 s | app2 settle after join s (3 pt / 5 pt) |")
	fmt.Println("|---|---|---|---|---|---|---|---|")
	for _, blk := range []float64{noDepthGate, 32, 8} {
		p := detParams(256, "endpoint", 2)
		p.threshold, p.duration = blk, 600
		p.idle = map[string][2]float64{"app2": {0, 300}}
		r := runClosedLoop(t, p)
		sh, _, _ := windowShare(r.series, 450, 600)
		j, _, _ := windowShare(r.series, 300, 330)
		name := "endpoint detector capThr 2, no depth bound"
		if blk < noDepthGate {
			name = fmt.Sprintf("endpoint detector capThr 2 + depth bound thr%g", blk)
		}
		fmt.Printf("| %s | %s | %.1f | %s | %.1f | %.1f | %s | %.0f / %.0f |\n", name, fmt3(sh), maxDev(sh, target), fmt3(j), r.meanWaiting,
			r.heldBy["app1"]+r.heldBy["app2"]+r.heldBy["end-users"], fmt3(r.p99Lat), convergedAt(r.series, target, 300, 600, 3),
			convergedAt(r.series, target, 300, 600, 5))
	}
}
