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
