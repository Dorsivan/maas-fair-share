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

// UNI-293: the UNI-290 round-2 / UNI-291 SFQ sim cases, ported to run in CI.
//
// The round-2 sim (branch uni290-composition, attenuation_sim_test.go)
// computed its SFQ tags inside the sim. Here the tag is the real plugin's.
// Every request goes through PreRequest, and the vLLM model reads `priority`
// back out of the rewritten body. Every first byte and completion goes
// through ResponseBody. So these cases test the code that ships: the stamp,
// endpoint-min V with its serving rule, the true-up and the reaper.
//
// The vLLM model is the one UNI-291 confirmed for 0.24 under
// --scheduling-policy priority. Each endpoint has a waiting queue ordered by
// (priority, arrival) and --max-num-seqs slots. A request is admitted only if
// its KV fits, and admission stops at the first request that does not fit.
// No preemption. Routing is the queue scorer's, from a metrics scrape that
// refreshes every 50 ms: the scraped waiting depth, plus what the EPP has sent
// there since, less the slots the scrape showed free (num_requests_running).
// The router cannot see KV room. That is the real EPP's view, and it is what
// sends extra work to KV-bound endpoints in the heterogeneous cases.
// Workers are closed-loop with zero think time. By default there is no EPP
// depth gate, which is the round-2 "SFQ alone, no depth gate" configuration:
// everything is released at once and ordering happens entirely in vLLM. With
// `hold` set, the EPP holds requests in per-tenant FIFO flow queues while
// vLLM's pool-wide waiting depth is at or above `hold`, and releases them one
// at a time through the real plugin's Pick, as flow control does at
// queueDepthThreshold. That is how the hold cases measure what the tab, the
// newcomer clamp and the virtualTime ratchet do once the stamp is on.
//
// Scored on slot-seconds served (GPU-time composition) after warm-up, against
// weights 20/10/65 normalised over the tenants present. It is an event-driven
// model, not a live run. See docs/design.md "UNI-293: SFQ priority stamp".

import (
	"container/heap"
	"context"
	"fmt"
	"math"
	"math/rand"
	"sort"
	"strings"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol"
	fwkfcmocks "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol/mocks"
	fwkrc "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requestcontrol"
	fwkrh "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requesthandling"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

var sfqSimWeights = map[string]float64{"app1": 20, "app2": 10, "end-users": 65}
var sfqSimTenants = []string{"app1", "app2", "end-users"}

// sfqSimTenant is one tenant of a sim run. UNI-305: the tenant set is a
// parameter (sfqSimParams.tenants), so the sim runs any N; unset, it is the
// POC's three above and every case behaves exactly as before.
type sfqSimTenant struct {
	name   string
	weight float64
}

func sfqSimDefaultTenants() []sfqSimTenant {
	out := make([]sfqSimTenant, len(sfqSimTenants))
	for i, tn := range sfqSimTenants {
		out[i] = sfqSimTenant{tn, sfqSimWeights[tn]}
	}
	return out
}

type sfqSimParams struct {
	tenants   []sfqSimTenant // nil = sfqSimDefaultTenants()
	workers   map[string]int
	endpoints int
	seqs      int
	kvCaps    []float64 // per endpoint, tokens; 0 or missing = unlimited
	service   float64   // mean slot-hold seconds for a 1x request
	staleness float64   // seconds between the router's metric scrapes; 0 = exact live counts
	duration  float64
	warmup    float64
	seed      int64

	promptToks int
	outToks    int
	maxTokens  int64

	// idle: tenant submits nothing during [from, to), then returns with its
	// full worker count. from 0 is a newcomer joining at `to`.
	idle map[string][2]float64

	// gamer sends 3 short (0.05x) requests per long (gamerLong x) one. With
	// gamerTightMax its shorts carry max_tokens = their true output: the
	// UNI-283 vector that drags the output EWMA down.
	gamer         string
	gamerLong     float64
	gamerTightMax bool

	noTrueUp bool // disable the finish-tag true-up (shows the vector is real)
	vMax     bool // V = max start tag, the rejected definition (shows the min matters)

	// hold > 0 gates the EPP at that pool-wide vLLM waiting depth and orders
	// the held requests with Pick. tabPick makes Pick rank by the tab with the
	// newcomer clamp and ratchet (the pre-review behaviour); noClamp turns the
	// clamp off.
	hold    int
	tabPick bool
	noClamp bool

	// snapAt > 0 records each tenant's lag (F_g - V) as the first event at or
	// after snapAt is about to be processed. UNI-300 uses it to read the
	// state a second saturation episode inherits.
	snapAt float64
	// noIdleReset keeps V and every F_g across a fully idle pool, as before
	// UNI-300.
	noIdleReset bool
	// rebaseAt overrides the threshold rebase (tag units); 0 keeps the
	// default. naiveRebase subtracts V from the stamp too, which is what a
	// rebase would do if it ignored the tags already queued in vLLM.
	rebaseAt    float64
	naiveRebase bool

	// staleAfter and settleTimeout override sfqEndpointStaleSeconds and
	// sfqSettleTimeoutSeconds (sim seconds); 0 keeps the defaults. sigma is the
	// log-normal spread of service time; 0 keeps 0.15.
	staleAfter    float64
	settleTimeout float64
	sigma         float64

	// UNI-302: decisionLog sets sfqDecisionLog, ctx carries the logger it
	// writes to, and onEvent runs at each event's sim time, before it is
	// processed.
	decisionLog string
	ctx         context.Context
	onEvent     func(at float64)
}

func sfqSimBase(workers int) sfqSimParams {
	w := map[string]int{}
	for _, tn := range sfqSimTenants {
		w[tn] = workers
	}
	// Arm A: 2 endpoints x --max-num-seqs 8, ~0.71 s per slot-hold (16 slots
	// at ~22.5 req/s live). The prompt is kept small so the plugin's token
	// cost, like the modelled service time, is dominated by output.
	return sfqSimParams{
		workers: w, endpoints: 2, seqs: 8, service: 0.71, staleness: 0.05, duration: 300, warmup: 30, seed: 1,
		promptToks: 16, outToks: 64, maxTokens: 64,
	}
}

type sfqSimReq struct {
	tenant     string
	req        *fwksched.InferenceRequest
	prio       int64
	seq        int
	arrived    float64
	started    float64
	dispatched float64
	service    float64
	out        int
	kv         float64
}

type sfqSimEvent struct {
	at  float64
	ep  int // completion on endpoint ep, or -1 for a tenant returning from idle
	r   *sfqSimReq
	tn  string
	seq int
}

type sfqSimEvents []sfqSimEvent

func (h sfqSimEvents) Len() int { return len(h) }
func (h sfqSimEvents) Less(i, j int) bool {
	if h[i].at != h[j].at {
		return h[i].at < h[j].at
	}
	return h[i].seq < h[j].seq
}
func (h sfqSimEvents) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *sfqSimEvents) Push(x any)   { *h = append(*h, x.(sfqSimEvent)) }
func (h *sfqSimEvents) Pop() any {
	old := *h
	x := old[len(old)-1]
	*h = old[:len(old)-1]
	return x
}

// sfqSimServed is one completed request, for windowed shares.
type sfqSimServed struct {
	tenant  string
	started float64
	service float64
	e2e     float64
	settle  float64 // dispatch to completion: what the reaper's clock sees
}

type sfqSimResult struct {
	tenants    []string // in submission order
	served     []sfqSimServed
	starts     [][]float64 // per endpoint, every service start time
	throughput float64
	reqs       map[string]int
	lag        map[string]float64 // F_g - V at snapAt
	prios      []int64            // every stamped priority, in dispatch order
	epochs     uint64             // idle resets over the run
}

// firstStart is when tn's first request starting at or after from began
// service, relative to from. -1 if none did.
func (r sfqSimResult) firstStart(tn string, from float64) float64 {
	best := -1.0
	for _, s := range r.served {
		if s.tenant == tn && s.started >= from && (best < 0 || s.started-from < best) {
			best = s.started - from
		}
	}
	return best
}

// share is the slot-second composition of requests that started in [from, to).
func (r sfqSimResult) share(from, to float64) map[string]float64 {
	sum := map[string]float64{}
	var tot float64
	for _, s := range r.served {
		if s.started >= from && s.started < to {
			sum[s.tenant] += s.service
			tot += s.service
		}
	}
	out := map[string]float64{}
	for _, tn := range r.tenants {
		if tot > 0 {
			out[tn] = 100 * sum[tn] / tot
		}
	}
	return out
}

func (r sfqSimResult) maxE2E(from, to float64) float64 {
	m := 0.0
	for _, s := range r.served {
		if s.started >= from && s.started < to {
			m = math.Max(m, s.e2e)
		}
	}
	return m
}

func sfqSimTarget(present []string) map[string]float64 {
	ts := make([]sfqSimTenant, len(present))
	for i, tn := range present {
		ts[i] = sfqSimTenant{tn, sfqSimWeights[tn]}
	}
	return sfqSimTargetOf(ts)
}

// sfqSimTargetOf is each tenant's weight share, in percent.
func sfqSimTargetOf(ts []sfqSimTenant) map[string]float64 {
	var s float64
	for _, t := range ts {
		s += t.weight
	}
	out := map[string]float64{}
	for _, t := range ts {
		out[t.name] = 100 * t.weight / s
	}
	return out
}

func sfqSimDev(share, target map[string]float64) float64 {
	d := 0.0
	for tn, v := range target {
		d = math.Max(d, math.Abs(share[tn]-v))
	}
	return d
}

func fmtShare(m map[string]float64) string {
	return fmtShareOf(sfqSimTenants, m)
}

// fmtShareOf prints m's shares in the given tenant order, "a/b/c/...".
func fmtShareOf(names []string, m map[string]float64) string {
	parts := make([]string, len(names))
	for i, tn := range names {
		parts[i] = fmt.Sprintf("%.1f", m[tn])
	}
	return strings.Join(parts, "/")
}

func runSFQSim(t *testing.T, prm sfqSimParams) sfqSimResult {
	t.Helper()
	cfg := DefaultConfig()
	cfg.StateLogIntervalSeconds = 0
	cfg.SFQPriorityStamp = true
	tenantSet := prm.tenants
	if tenantSet == nil {
		tenantSet = sfqSimDefaultTenants()
	}
	tenants := make([]string, len(tenantSet))
	cfg.Groups = nil
	for i, ts := range tenantSet {
		tenants[i] = ts.name
		cfg.Groups = append(cfg.Groups, GroupConfig{Name: ts.name, Weight: ts.weight, Match: GroupMatch{Exact: []string{ts.name}}})
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "unclassified", Weight: 5}
	cfg.Enforce = true
	cfg.NewcomerClamp = !prm.noClamp
	if prm.staleAfter > 0 {
		cfg.SFQEndpointStaleSeconds = prm.staleAfter
	}
	if prm.settleTimeout > 0 {
		cfg.SFQSettleTimeoutSeconds = prm.settleTimeout
	}
	cfg.SFQDecisionLog = prm.decisionLog
	p, clock := newTestPlugin(t, cfg)
	p.sfq.noTrueUp, p.sfq.vMax, p.sfq.tabPick = prm.noTrueUp, prm.vMax, prm.tabPick
	p.sfq.noIdleReset, p.sfq.naiveRebase = prm.noIdleReset, prm.naiveRebase
	if prm.rebaseAt > 0 {
		p.sfq.rebaseAt = prm.rebaseAt
	}
	ctx := context.Background()
	if prm.ctx != nil {
		ctx = prm.ctx
	}
	rng := rand.New(rand.NewSource(prm.seed))
	at := func(s float64) { clock.t = testBasis.Add(time.Duration(s * float64(time.Second))) }

	results := make([]*fwksched.SchedulingResult, prm.endpoints)
	for e := range results {
		results[e] = onEndpoint(fmt.Sprintf("vllm-%d", e))
	}
	kvCap := func(e int) float64 {
		if e < len(prm.kvCaps) && prm.kvCaps[e] > 0 {
			return prm.kvCaps[e]
		}
		return math.Inf(1)
	}
	waiting := make([][]*sfqSimReq, prm.endpoints)
	running := make([]int, prm.endpoints)
	snapW, snapFree, since := make([]float64, prm.endpoints), make([]float64, prm.endpoints), make([]float64, prm.endpoints)
	nextScrape := 0.0
	kvUsed := make([]float64, prm.endpoints)
	events := &sfqSimEvents{}
	evSeq, reqSeq := 0, 0
	push := func(ev sfqSimEvent) { evSeq++; ev.seq = evSeq; heap.Push(events, ev) }
	nth := map[string]int{}
	outstanding := map[string]int{}
	res := sfqSimResult{tenants: tenants, reqs: map[string]int{}, starts: make([][]float64, prm.endpoints)}
	active := func(tn string, now float64) bool {
		w, ok := prm.idle[tn]
		return !ok || now < w[0] || now >= w[1]
	}

	admit := func(e int, now float64) {
		for len(waiting[e]) > 0 {
			i := 0
			for j, w := range waiting[e] {
				if w.prio < waiting[e][i].prio || (w.prio == waiting[e][i].prio && w.seq < waiting[e][i].seq) {
					i = j
				}
			}
			r := waiting[e][i]
			if running[e] >= prm.seqs || kvUsed[e]+r.kv > kvCap(e) {
				return
			}
			waiting[e] = append(waiting[e][:i], waiting[e][i+1:]...)
			running[e]++
			kvUsed[e] += r.kv
			r.started = now
			res.starts[e] = append(res.starts[e], now)
			// First token: the signal the plugin advances V on.
			p.ResponseBody(ctx, r.req, &fwkrc.Response{}, nil)
			push(sfqSimEvent{at: now + r.service, ep: e, r: r})
		}
	}

	dispatch := func(r *sfqSimReq, now float64) {
		if prm.staleness <= 0 || now >= nextScrape {
			for e := range waiting {
				snapW[e], snapFree[e], since[e] = float64(len(waiting[e])), float64(prm.seqs-running[e]), 0
			}
			nextScrape = now + prm.staleness
		}
		score := func(e int) float64 {
			return math.Max(0, snapW[e]+since[e]-snapFree[e]) + 0.01*(float64(prm.seqs)-snapFree[e])/float64(prm.seqs)
		}
		best := 0
		for e := 1; e < prm.endpoints; e++ {
			if score(e) < score(best) {
				best = e
			}
		}
		since[best]++
		require.NoError(t, p.PreRequest(ctx, r.req, results[best]))
		r.prio = r.req.Body.Payload.(fwkrh.PayloadMap)["priority"].(int64)
		r.dispatched = now
		res.prios = append(res.prios, r.prio)
		waiting[best] = append(waiting[best], r)
		admit(best, now)
	}

	// The EPP's flow queues, one FIFO per tenant, drained through Pick.
	held := map[string][]*sfqSimReq{}
	band := p.NewState(ctx)
	release := func(now float64) {
		for {
			depth := 0
			for e := range waiting {
				depth += len(waiting[e])
			}
			if depth >= prm.hold {
				return
			}
			var active []flowcontrol.FlowQueueAccessor
			for _, tn := range tenants {
				if q := held[tn]; len(q) > 0 {
					active = append(active, &fwkfcmocks.MockFlowQueueAccessor{
						LenV: len(q), FlowKeyV: flowcontrol.FlowKey{ID: tn},
						PeekV: &fwkfcmocks.MockQueueItemAccessor{
							EnqueueTimeV: testBasis.Add(time.Duration(q[0].arrived * float64(time.Second)))},
					})
				}
			}
			if len(active) == 0 {
				return
			}
			q, err := p.Pick(ctx, &fwkfcmocks.MockPriorityBandAccessor{
				PolicyStateV: band,
				IterateQueuesFunc: func(cb func(flowcontrol.FlowQueueAccessor) bool) {
					for _, q := range active {
						if !cb(q) {
							return
						}
					}
				},
			})
			require.NoError(t, err)
			tn := q.FlowKey().ID
			r := held[tn][0]
			held[tn] = held[tn][1:]
			dispatch(r, now)
		}
	}

	sigma := prm.sigma
	if sigma == 0 {
		sigma = 0.15
	}
	submit := func(tn string, now float64) {
		reqSeq++
		nth[tn]++
		m := 1.0
		maxTok := prm.maxTokens
		if tn == prm.gamer {
			m = 0.05
			if nth[tn]%4 == 0 {
				m = prm.gamerLong
			}
		}
		out := int(float64(prm.outToks) * m)
		if tn == prm.gamer && prm.gamerTightMax && m < 1 {
			maxTok = int64(out)
		}
		body := &fwkrh.InferenceRequestBody{Payload: fwkrh.PayloadMap{"model": "m"}}
		if maxTok > 0 {
			mt := maxTok
			body.MaxOutputTokens = &mt
		}
		r := &sfqSimReq{
			tenant: tn, seq: reqSeq, arrived: now, out: out,
			service: m * prm.service * math.Exp(sigma*rng.NormFloat64()-0.5*sigma*sigma),
			kv:      float64(prm.promptToks + out),
			req: &fwksched.InferenceRequest{RequestID: fmt.Sprintf("%s-%d", tn, reqSeq), FairnessID: tn,
				Body: body, RequestSizeBytes: prm.promptToks * 4},
		}
		outstanding[tn]++
		res.reqs[tn]++
		if prm.hold > 0 {
			held[tn] = append(held[tn], r)
			release(now)
			return
		}
		dispatch(r, now)
	}

	at(0)
	for _, tn := range tenants {
		if w, ok := prm.idle[tn]; ok && w[0] <= 0 {
			push(sfqSimEvent{at: w[1], ep: -1, tn: tn})
			continue
		}
		for i := 0; i < prm.workers[tn]; i++ {
			submit(tn, 0)
		}
	}
	// In tenant order, not map order: tenants returning at the same instant
	// must submit in the same order every run.
	for _, tn := range tenants {
		if w, ok := prm.idle[tn]; ok && w[0] > 0 {
			push(sfqSimEvent{at: w[1], ep: -1, tn: tn})
		}
	}

	completed := 0
	for events.Len() > 0 {
		ev := heap.Pop(events).(sfqSimEvent)
		if ev.at >= prm.duration {
			break
		}
		at(ev.at)
		if prm.onEvent != nil {
			prm.onEvent(ev.at)
		}
		if prm.snapAt > 0 && res.lag == nil && ev.at >= prm.snapAt {
			v := p.sfq.view(clock.t)
			res.lag = map[string]float64{}
			for _, tn := range tenants {
				res.lag[tn] = v.FinishTags[tn] - v.VirtualTime
			}
		}
		if ev.ep < 0 {
			for n := outstanding[ev.tn]; n < prm.workers[ev.tn]; n++ {
				submit(ev.tn, ev.at)
			}
			continue
		}
		r, e := ev.r, ev.ep
		running[e]--
		kvUsed[e] -= r.kv
		p.ResponseBody(ctx, r.req, &fwkrc.Response{
			EndOfStream: true, TerminationCause: fwkrc.TerminationCauseNatural,
			Usage: fwkrh.Usage{PromptTokens: prm.promptToks, CompletionTokens: r.out, TotalTokens: prm.promptToks + r.out},
		}, nil)
		outstanding[r.tenant]--
		completed++
		res.served = append(res.served, sfqSimServed{tenant: r.tenant, started: r.started, service: r.service, e2e: ev.at - r.arrived, settle: ev.at - r.dispatched})
		if active(r.tenant, ev.at) {
			submit(r.tenant, ev.at)
		}
		admit(e, ev.at)
		if prm.hold > 0 {
			release(ev.at)
		}
	}
	res.throughput = float64(completed) / prm.duration
	res.epochs = p.sfq.view(clock.t).Epoch
	return res
}

func sfqSimLog(t *testing.T, name string, r sfqSimResult, share, target map[string]float64) {
	t.Helper()
	t.Logf("%-58s served %s target %s dev %.1f pt, %.1f req/s", name, fmtShare(share), fmtShare(target),
		sfqSimDev(share, target), r.throughput)
}

// Arm A: equal offered load (32 workers per tenant), weights 20/10/65.
// Round 2 measured the SFQ stamp exact here. FIFO lands at ~33/33/33.
func TestSFQSimArmAComposition(t *testing.T) {
	t.Parallel()
	target := sfqSimTarget(sfqSimTenants)
	for s := int64(1); s <= 2; s++ {
		prm := sfqSimBase(32)
		prm.seed = s
		r := runSFQSim(t, prm)
		sh := r.share(prm.warmup, prm.duration)
		sfqSimLog(t, fmt.Sprintf("Arm A seed %d", s), r, sh, target)
		assert.Less(t, sfqSimDev(sh, target), 2.0, "seed %d", s)
		assert.Greater(t, r.throughput, 20.0, "work conservation: the stamp must not idle slots")
	}
}

// Flood: 256 workers per tenant, so vLLM's waiting queue is ~750 deep and
// every position in it is decided by the stamp.
func TestSFQSimFlood(t *testing.T) {
	t.Parallel()
	prm := sfqSimBase(256)
	r := runSFQSim(t, prm)
	target := sfqSimTarget(sfqSimTenants)
	sh := r.share(prm.warmup, prm.duration)
	sfqSimLog(t, "flood, 256 workers/tenant", r, sh, target)
	assert.Less(t, sfqSimDev(sh, target), 2.0)
}

// Unequal worker counts: the stamp composes by weight, not by who sends more,
// as long as everyone is backlogged.
func TestSFQSimUnequalWorkers(t *testing.T) {
	t.Parallel()
	target := sfqSimTarget(sfqSimTenants)
	for _, w := range [][3]int{{128, 32, 32}, {32, 32, 128}} {
		prm := sfqSimBase(0)
		prm.workers = map[string]int{"app1": w[0], "app2": w[1], "end-users": w[2]}
		r := runSFQSim(t, prm)
		sh := r.share(prm.warmup, prm.duration)
		sfqSimLog(t, fmt.Sprintf("%d/%d/%d workers", w[0], w[1], w[2]), r, sh, target)
		assert.Less(t, sfqSimDev(sh, target), 2.0, "%v", w)
	}
}

// Idle and return: the remaining tenants re-split by weight while one is
// away. The returning tenant starts at V, not at its stale finish tag, so it
// neither takes a burst nor queues behind everyone.
func TestSFQSimIdleReturn(t *testing.T) {
	t.Parallel()
	for _, idle := range []string{"end-users", "app1"} {
		prm := sfqSimBase(32)
		prm.duration = 450
		prm.idle = map[string][2]float64{idle: {150, 300}}
		r := runSFQSim(t, prm)
		var rest []string
		for _, tn := range sfqSimTenants {
			if tn != idle {
				rest = append(rest, tn)
			}
		}
		all := sfqSimTarget(sfqSimTenants)
		pre, mid, post := r.share(prm.warmup, 150), r.share(170, 300), r.share(310, 450)
		sfqSimLog(t, idle+" idle: before", r, pre, all)
		sfqSimLog(t, idle+" idle: away", r, mid, sfqSimTarget(rest))
		sfqSimLog(t, idle+" idle: after return", r, post, all)
		assert.Less(t, sfqSimDev(pre, all), 2.0, idle)
		assert.Less(t, sfqSimDev(mid, sfqSimTarget(rest)), 2.0, idle)
		assert.Less(t, sfqSimDev(post, all), 2.0, idle)
		// No burst on return: the first 10 s must not hand the returner more
		// than its weight by a wide margin.
		first := r.share(300, 310)
		assert.Less(t, first[idle], all[idle]+15, "%s took a burst on return: %s", idle, fmtShare(first))
	}
}

// Newcomer behind a deep backlog: app2 joins at 150 s into a pool where 512
// requests are already queued in vLLM. A FIFO newcomer would wait behind
// all of them. Under the stamp it starts at V and is served at its weight
// almost immediately.
func TestSFQSimNewcomerBehindDeepBacklog(t *testing.T) {
	t.Parallel()
	prm := sfqSimBase(256)
	prm.duration = 300
	prm.idle = map[string][2]float64{"app2": {0, 150}}
	r := runSFQSim(t, prm)
	all := sfqSimTarget(sfqSimTenants)
	join, settled := r.share(150, 180), r.share(180, 300)
	sfqSimLog(t, "app2 joins at 150 s: first 30 s", r, join, all)
	sfqSimLog(t, "app2 joins at 150 s: 180-300 s", r, settled, all)
	assert.Greater(t, join["app2"], all["app2"]-4, "the newcomer must not queue behind the backlog")
	assert.Less(t, join["app2"], all["app2"]+15, "nor take a burst")
	assert.Less(t, sfqSimDev(settled, all), 2.0)
	assert.Less(t, r.maxE2E(150, 300), 120.0)
}

// KV-limited: only 10 of 16 slots' worth of requests fit in KV. vLLM stops
// admitting at the first request that does not fit, so the waiting order
// still decides who gets the room.
func TestSFQSimKVLimited(t *testing.T) {
	t.Parallel()
	prm := sfqSimBase(32)
	typical := float64(prm.promptToks + prm.outToks)
	prm.kvCaps = []float64{5.5 * typical, 5.5 * typical}
	r := runSFQSim(t, prm)
	target := sfqSimTarget(sfqSimTenants)
	sh := r.share(prm.warmup, prm.duration)
	sfqSimLog(t, "KV-limited (10 effective of 16)", r, sh, target)
	assert.Less(t, sfqSimDev(sh, target), 2.0)
}

// Heterogeneous endpoints: a share of the endpoints are KV-bound to 3
// concurrent requests, so they serve slower. This is the case where
// V = max-tag error grows with N (5.3 pt at N=8, 9.3 at N=64) and
// V = endpoint-min held 0.0 pt (UNI-291). Offered load per endpoint is held
// constant: 16 workers per tenant per endpoint.
func TestSFQSimHeterogeneousEndpoints(t *testing.T) {
	t.Parallel()
	target := sfqSimTarget(sfqSimTenants)
	for _, n := range []int{8, 64} {
		for _, frac := range []int{2, 4} {
			prm := sfqSimBase(16 * n)
			prm.endpoints = n
			prm.duration = 150
			if n == 64 {
				prm.duration = 90
			}
			typical := float64(prm.promptToks + prm.outToks)
			prm.kvCaps = make([]float64, n)
			for e := n - n/frac; e < n; e++ {
				prm.kvCaps[e] = 3.5 * typical
			}
			r := runSFQSim(t, prm)
			sh := r.share(prm.warmup, prm.duration)
			sfqSimLog(t, fmt.Sprintf("N=%d, 1/%d of endpoints KV-bound", n, frac), r, sh, target)
			assert.Less(t, sfqSimDev(sh, target), 2.0, "N=%d 1/%d", n, frac)
		}
	}
	// Power check. Under the max-tag V the same case must fail, and fail
	// worse at larger N, or this test is not testing the V definition. That
	// needs the stale-scrape router: with exact routing V never binds and
	// both definitions pass (found while porting; see the commit message).
	devMax := map[int]float64{}
	for _, n := range []int{8, 64} {
		prm := sfqSimBase(16 * n)
		prm.endpoints, prm.duration, prm.vMax = n, 90, true
		typical := float64(prm.promptToks + prm.outToks)
		prm.kvCaps = make([]float64, n)
		for e := n / 2; e < n; e++ {
			prm.kvCaps[e] = 3.5 * typical
		}
		r := runSFQSim(t, prm)
		sh := r.share(prm.warmup, prm.duration)
		sfqSimLog(t, fmt.Sprintf("V=max (rejected), N=%d, 1/2 KV-bound", n), r, sh, target)
		devMax[n] = sfqSimDev(sh, target)
	}
	assert.Greater(t, devMax[8], 2.0, "V=max must fail at N=8")
	assert.Greater(t, devMax[64], devMax[8], "and its error must grow with N")
}

// The UNI-283 tight-max_tokens vector against the stamp. app1 sends three
// tiny requests with max_tokens equal to their true output, then one long
// request. The shorts drag app1's output EWMA down, so the long one is
// estimated low and tagged too early. Round 2: 50.1% against a 21.1% target
// without the true-up, exactly 21.1% with it.
func TestSFQSimGamingVector(t *testing.T) {
	t.Parallel()
	target := sfqSimTarget(sfqSimTenants)
	run := func(noTrueUp bool) map[string]float64 {
		prm := sfqSimBase(32)
		prm.maxTokens = 1024
		prm.gamer, prm.gamerLong, prm.gamerTightMax = "app1", 10, true
		prm.noTrueUp = noTrueUp
		r := runSFQSim(t, prm)
		sh := r.share(prm.warmup, prm.duration)
		name := "gamer, with completion true-up"
		if noTrueUp {
			name = "gamer, true-up disabled"
		}
		sfqSimLog(t, name, r, sh, target)
		return sh
	}
	without := run(true)
	assert.Greater(t, without["app1"], target["app1"]+10,
		"the vector must be real without the true-up, or this test proves nothing")
	with := run(false)
	assert.Less(t, sfqSimDev(with, target), 2.0, "the true-up must close the vector")
}

// Lost completions must not make a group cheaper. a-group sends three tiny
// requests with max_tokens equal to their true output, then one long one
// (max_tokens 1024, generates 640). Only the long ones' completions are lost:
// vLLM serves them, but no ResponseBody ever arrives, which is the UNI-193
// failure. Their dispatch estimate comes from an EWMA that has only ever seen
// the tiny ones, so without the reaper a-group would keep a ~4x under-charge
// on exactly its expensive requests. One slot, served strictly in stamped
// order, equal weights. Scored on token-seconds of slot time.
func TestSFQSimLostCompletionsAreConservative(t *testing.T) {
	t.Parallel()
	run := func(settleTimeout float64) float64 {
		cfg := DefaultConfig()
		cfg.SFQPriorityStamp = true
		cfg.SFQSettleTimeoutSeconds = settleTimeout
		cfg.StateLogIntervalSeconds = 0
		cfg.Groups = []GroupConfig{
			{Name: "a-group", Weight: 1, Match: GroupMatch{Exact: []string{"a"}}},
			{Name: "b-group", Weight: 1, Match: GroupMatch{Exact: []string{"b"}}},
		}
		p, clock := newTestPlugin(t, cfg)
		ctx := context.Background()
		type item struct {
			g        string
			req      *fwksched.InferenceRequest
			prio     int64
			seq, out int
			lost     bool
		}
		var q []item
		seq, nA := 0, 0
		enqueue := func(g string) {
			seq++
			mt, out, lost := int64(1024), 64, false
			if g == "a-group" {
				nA++
				mt, out = 4, 4
				if nA%4 == 0 {
					mt, out, lost = 1024, 640, true
				}
			}
			req := &fwksched.InferenceRequest{FairnessID: g, RequestSizeBytes: 64,
				Body: &fwkrh.InferenceRequestBody{Payload: fwkrh.PayloadMap{}, MaxOutputTokens: &mt}}
			require.NoError(t, p.PreRequest(ctx, req, onEndpoint("e0")))
			q = append(q, item{g, req, req.Body.Payload.(fwkrh.PayloadMap)["priority"].(int64), seq, out, lost})
		}
		for i := 0; i < 16; i++ {
			enqueue("a-group")
			enqueue("b-group")
		}
		served := map[string]float64{}
		for step := 0; step < 20000; step++ {
			sort.Slice(q, func(i, j int) bool {
				if q[i].prio != q[j].prio {
					return q[i].prio < q[j].prio
				}
				return q[i].seq < q[j].seq
			})
			it := q[0]
			q = q[1:]
			p.ResponseBody(ctx, it.req, &fwkrc.Response{}, nil)
			clock.advance(time.Duration(it.out) * 10 * time.Millisecond)
			if step > 2000 {
				served[it.g] += float64(it.out)
			}
			if !it.lost {
				complete(p, it.req, 16, it.out)
			}
			enqueue(it.g)
		}
		return 100 * served["a-group"] / (served["a-group"] + served["b-group"])
	}
	noReaper := run(1e9)
	reaped := run(30)
	t.Logf("a-group's long completions lost: served %.1f%% with no reaper, %.1f%% with a 30 s reaper (equal weights, 50%% target)",
		noReaper, reaped)
	assert.Greater(t, noReaper, 60.0, "without the reaper the lost completions must show up as an under-charge, or this test proves nothing")
	assert.LessOrEqual(t, reaped, 50.0, "losing completions must never buy a group extra service")
}

// UNI-293 review: with the stamp on, the tab must not also rank the EPP-held
// queue. Behind an EPP hold, the gaming vector is replayed with Pick ranking by
// the SFQ tag (what ships) and by the decayed tab (the pre-review behaviour,
// tabPick). The tab's true-up decays, so it under-charges the gamer's long
// requests, and Pick lets that back in ahead of a stamp that has it right.
// Measured: ~21.4% against the 21.1% target by tag, ~23.7% by tab.
func TestSFQSimHoldOneNotionOfService(t *testing.T) {
	t.Parallel()
	target := sfqSimTarget(sfqSimTenants)
	run := func(tabPick bool) map[string]float64 {
		prm := sfqSimBase(32)
		prm.hold = 4
		prm.maxTokens = 1024
		prm.gamer, prm.gamerLong, prm.gamerTightMax = "app1", 10, true
		prm.tabPick = tabPick
		r := runSFQSim(t, prm)
		sh := r.share(prm.warmup, prm.duration)
		name := "gamer behind EPP hold 4, Pick by SFQ tag"
		if tabPick {
			name = "gamer behind EPP hold 4, Pick by decayed tab"
		}
		sfqSimLog(t, name, r, sh, target)
		return sh
	}
	byTab := run(true)
	assert.Greater(t, byTab["app1"], target["app1"]+1.5,
		"ranking by the tab must leak the vector, or this test proves nothing")
	byTag := run(false)
	assert.Less(t, sfqSimDev(byTag, target), 1.0)
}

// UNI-293 review: newcomerClamp is redundant under the stamp. A tenant returns
// from 150 s idle, and then a newcomer joins, behind an EPP hold. With Pick
// ranking by tag and the clamp skipped, neither gets a burst: max(F_g, V) does
// the clamp's job exactly. The tab arm without the clamp shows the burst that
// job exists to stop (~30% against a 10.5% target), so the absence of one
// under the tag is the tag's doing. With the tab arm's clamp on, the burst is
// also gone. UNI-283's joiner delay via the ratchet (315 s vs 77 s) did not
// reproduce in this model in either arm; this case does not claim it.
func TestSFQSimHoldReturnNeedsNoClamp(t *testing.T) {
	t.Parallel()
	all := sfqSimTarget(sfqSimTenants)
	for _, sc := range []struct {
		name string
		idle [2]float64
	}{{"returns", [2]float64{100, 250}}, {"joins", [2]float64{0, 250}}} {
		run := func(tabPick, noClamp bool) sfqSimResult {
			prm := sfqSimBase(128)
			prm.hold = 4
			prm.duration = 400
			prm.idle = map[string][2]float64{"app2": sc.idle}
			prm.tabPick, prm.noClamp = tabPick, noClamp
			return runSFQSim(t, prm)
		}
		tag := run(false, false)
		first := tag.share(250, 280)
		sfqSimLog(t, "app2 "+sc.name+" at 250 s behind EPP hold, Pick by tag: first 30 s", tag, first, all)
		assert.Less(t, sfqSimDev(first, all), 3.0, sc.name)
		assert.Less(t, sfqSimDev(tag.share(280, 400), all), 2.0, sc.name)

		bare := run(true, true)
		bfirst := bare.share(250, 280)
		sfqSimLog(t, "app2 "+sc.name+" at 250 s behind EPP hold, Pick by tab, no clamp: first 30 s", bare, bfirst, all)
		assert.Greater(t, bfirst["app2"], all["app2"]+10,
			"%s: the tab without a clamp must burst, or this test proves nothing", sc.name)
	}
}

// ---------------------------------------------------------------------------
// UNI-300: rebasing, and resetting the clock when the pool goes idle
// ---------------------------------------------------------------------------

// Part 4: a threshold rebase leaves every stamp where it was. rebaseAt 50 tag
// units rebases the internal clock every ~1.5 s (hundreds of times a run);
// the stamped priorities must match the no-rebase run exactly, request for
// request, so the composition is the same run, not a similar one. The power
// check is a rebase that also drops the stamp back towards zero, ignoring
// the requests already queued in vLLM on the old numbering: every request
// after it sorts ahead of all of them. Measured: in the flood, max e2e 110 s
// -> 257 s and app2 4-6% against 10.5%.
func TestSFQSimRebaseIsInvisible(t *testing.T) {
	t.Parallel()
	all := sfqSimTarget(sfqSimTenants)
	for _, workers := range []int{32, 256} {
		ref := runSFQSim(t, sfqSimBase(workers))
		prm := sfqSimBase(workers)
		prm.rebaseAt = 50
		r := runSFQSim(t, prm)
		refSh, sh := ref.share(30, 300), r.share(30, 300)
		sfqSimLog(t, fmt.Sprintf("%d workers, no rebase", workers), ref, refSh, all)
		sfqSimLog(t, fmt.Sprintf("%d workers, internal clock rebased every 50 tag units", workers), r, sh, all)
		require.Equal(t, ref.prios, r.prios, "%d workers: a rebase must not move any stamp", workers)
		assert.Equal(t, refSh, sh)
		assert.Greater(t, ref.prios[len(ref.prios)-1], int64(50*sfqTagScale*100),
			"the run must go far past the threshold, or nothing was rebased")
	}

	ref := runSFQSim(t, sfqSimBase(256))
	prm := sfqSimBase(256)
	prm.rebaseAt, prm.naiveRebase = 2000, true
	naive := runSFQSim(t, prm)
	sh := naive.share(30, 300)
	sfqSimLog(t, "256 workers, rebase that also drops the stamp (rejected)", naive, sh, all)
	t.Logf("max e2e: %.1f s without a rebase, %.1f s with the rejected rebase", ref.maxE2E(30, 300), naive.maxE2E(30, 300))
	assert.Greater(t, naive.maxE2E(30, 300), 2*ref.maxE2E(30, 300),
		"dropping the stamp must strand the requests already queued, or this test proves nothing")
	assert.Greater(t, sfqSimDev(sh, all), 2.0)
}

// Part 5: should the ledger reset when saturation ends? All tenants saturate,
// then app2 and end-users stop at 100 s and app1 runs alone to 150 s: the
// heavy morning tenant. Then the pool is fully idle until 450 s, far past
// every endpoint dropping out. End-users and app2 return at 450 s and app1 at
// 451 s, so app1 arrives into a queue it has to compete for.
//
// Before UNI-300, V froze across the idle and every F_g kept its value. The
// returning tenants with F_g below V restart at V: their stale credit is
// erased. A tenant with F_g above V keeps the difference: its stale debt
// carries into the next episode.
//
// How much debt there is depends on what was in flight when traffic stopped.
// With every request costing what it was estimated at ("fixed"), app1 goes
// idle one request ahead (7.2 tag units) and nothing measurable happens.
// The asymmetry is real but self-correcting. With variable output
// ("variable": three 0.05x requests to one 10x, estimated from the average),
// the requests still running when traffic stopped are the long ones. They
// were estimated low and trued up on completion, after V had stopped
// moving. Measured: app1 went idle 709 tag units ahead and, without the
// reset, waited 13.3 s for its first request against ~0.6 s for the others,
// and served 0% of the first 10 s. The delay is the debt over V's rate, not
// the length of the idle. At production sizes it scales with request
// duration and with total weight over the tenant's weight.
//
// With the reset it waited 0.17 s.
func TestSFQSimIdleResetsTheLedger(t *testing.T) {
	t.Parallel()
	all := sfqSimTarget(sfqSimTenants)
	run := func(variable, noReset bool) sfqSimResult {
		prm := sfqSimBase(32)
		prm.duration, prm.snapAt, prm.noIdleReset = 600, 450, noReset
		prm.idle = map[string][2]float64{"app1": {150, 451}, "app2": {100, 450}, "end-users": {100, 450}}
		if variable {
			prm.maxTokens = 1024
			prm.gamer, prm.gamerLong = "app1", 10
		}
		return runSFQSim(t, prm)
	}
	for _, variable := range []bool{false, true} {
		name := "fixed"
		if variable {
			name = "variable"
		}
		for _, noReset := range []bool{true, false} {
			r := run(variable, noReset)
			arm := "idle reset"
			if noReset {
				arm = "no reset (before UNI-300)"
			}
			t.Logf("%s, %s: lag at idle %.1f/%.1f/%.1f, first start after return app1 %.2f s, app2 %.2f s, end-users %.2f s, %d resets",
				name, arm, r.lag["app1"], r.lag["app2"], r.lag["end-users"],
				r.firstStart("app1", 451), r.firstStart("app2", 450), r.firstStart("end-users", 450), r.epochs)
			sfqSimLog(t, fmt.Sprintf("  %s, %s: first 10 s", name, arm), r, r.share(451, 461), all)
			sfqSimLog(t, fmt.Sprintf("  %s, %s: 481-600 s", name, arm), r, r.share(481, 600), all)
			assert.Less(t, sfqSimDev(r.share(481, 600), all), 3.0, "%s %s", name, arm)
			switch {
			case noReset && variable:
				assert.Greater(t, r.lag["app1"], 100.0, "app1 must go idle in debt, or this test proves nothing")
				assert.Greater(t, r.firstStart("app1", 451), 5.0, "the stale debt must delay app1, or this test proves nothing")
			case !noReset:
				assert.EqualValues(t, 1, r.epochs)
				assert.Less(t, r.firstStart("app1", 451), 1.0, "%s: no debt survives the reset", name)
			}
		}
	}
}

// sfqSimGaps returns the mean inter-start gap over endpoints eps after from,
// and the share of gaps longer than tau.
func sfqSimGaps(r sfqSimResult, eps []int, from, tau float64) (mean, over float64) {
	var n, sum, long float64
	for _, e := range eps {
		st := r.starts[e]
		for i := 1; i < len(st); i++ {
			if st[i-1] < from {
				continue
			}
			g := st[i] - st[i-1]
			n++
			sum += g
			if g > tau {
				long++
			}
		}
	}
	return sum / n, long / n
}

// UNI-300 review (Zeratul): is sfqEndpointStaleSeconds too short for long
// requests? An endpoint counts toward V only if it started something within
// staleAfter, and its mean gap between starts is S/N_eff: mean service time
// over the concurrency it actually runs. That is KV-derived and can sit well
// below max_num_seqs; here half the endpoints are KV-bound to 3 of 8. Gaps are
// near-exponential (cv 0.7-1.1), so a healthy endpoint drops out of the min
// with probability ~exp(-k) per gap, k = staleAfter * N_eff / S.
//
// What a drop-out costs is smaller than the rule suggests. The error needs
// the whole slow cohort out of the min at once. Measured, with half of 8
// endpoints slow, k in units of the slow endpoints' gap: k 0.67 within noise
// (0.3-1.2 pt), k 0.5 ~2.5 pt, k 0.25 4-7 pt, as bad as the rejected max-tag
// V. At N=64 there are 32 slow endpoints, one of them has always started
// recently, and k 0.25 is within noise too. A single slow endpoint costs
// little even under max-tag. So the error falls with fleet size; it does not
// grow.
func TestSFQSimStaleWindowRule(t *testing.T) {
	t.Parallel()
	all := sfqSimTarget(sfqSimTenants)
	const slowN = 3.0
	run := func(n int, k, sigma float64, seed int64) (sfqSimResult, sfqSimParams) {
		prm := sfqSimBase(16 * n)
		prm.endpoints, prm.duration, prm.sigma, prm.seed = n, 90, sigma, seed
		typical := float64(prm.promptToks + prm.outToks)
		prm.kvCaps = make([]float64, n)
		for e := n / 2; e < n; e++ {
			prm.kvCaps[e] = (slowN + 0.5) * typical
		}
		prm.staleAfter = k * prm.service / slowN
		return runSFQSim(t, prm), prm
	}
	devAt := func(n int, k float64) float64 {
		d := 0.0
		for seed := int64(1); seed <= 3; seed++ {
			r, prm := run(n, k, 0.15, seed)
			d += sfqSimDev(r.share(prm.warmup, prm.duration), all) / 3
		}
		return d
	}

	for _, sigma := range []float64{0.15, 1.0} {
		r, prm := run(8, 2, sigma, 1)
		fast, slow := []int{0, 1, 2, 3}, []int{4, 5, 6, 7}
		mf, _ := sfqSimGaps(r, fast, prm.warmup, math.Inf(1))
		ms, over := sfqSimGaps(r, slow, prm.warmup, 2*prm.service/slowN)
		t.Logf("sigma %.2f: mean gap %.4f s on 8-slot endpoints (S/N %.4f), %.4f s on KV-bound ones (S/N_eff %.4f); P(gap > 2 S/N_eff) %.3f (exp(-2) = 0.135)",
			sigma, mf, prm.service/8, ms, prm.service/slowN, over)
		assert.InEpsilon(t, prm.service/8, mf, 0.1, "the gap is S/N")
		assert.InEpsilon(t, prm.service/slowN, ms, 0.1, "with N the effective concurrency, not max_num_seqs")
		assert.InDelta(t, math.Exp(-2), over, 0.07, "gaps are near-exponential")
	}

	d067, d025, d64 := devAt(8, 0.67), devAt(8, 0.25), devAt(64, 0.25)
	t.Logf("half of N=8 slow: dev %.1f pt at k 0.67, %.1f pt at k 0.25; half of N=64 slow, k 0.25: %.1f pt", d067, d025, d64)
	assert.Less(t, d067, 2.0)
	assert.Greater(t, d025, 2.5, "a window well under the gap must cost something, or this test proves nothing")
	assert.Less(t, d64, 2.0, "many slow endpoints keep the min covered")
}

// UNI-300 review: sfqSettleTimeoutSeconds is measured from dispatch, so its
// clock includes the wait in vLLM's queue, not just service. Under the stamp,
// that wait is long by design for whoever is behind. A request reaped while
// still legitimately queued or running is charged worst-case and trued down
// when it completes. The reaps fall unevenly across groups, so the
// composition moves. Measured, 32 workers per tenant, service spread
// sigma 0.6, max_tokens 1024 against 64 generated:
//
//   - EPP gate at pool depth 8: settle 1.25 S reaps 52% and costs 6-7 pt;
//     2 S reaps 20% for 2-3 pt; 2.8 S reaps 5-6% and is clean.
//   - No gate (vLLM holds ~80): the low-weight tenant's median dispatch to
//     completion is ~19 S, and even 4 S reaps ~30% for 5-7 pt.
func TestSFQSimSettleTimeoutCountsQueueWait(t *testing.T) {
	t.Parallel()
	all := sfqSimTarget(sfqSimTenants)
	run := func(hold int, settle float64) (dev, reaped float64) {
		prm := sfqSimBase(32)
		prm.hold, prm.sigma, prm.maxTokens = hold, 0.6, 1024
		prm.settleTimeout = settle * prm.service
		r := runSFQSim(t, prm)
		n, over := 0, 0
		for _, s := range r.served {
			if s.started >= prm.warmup {
				n++
				if s.settle > prm.settleTimeout {
					over++
				}
			}
		}
		dev, reaped = sfqSimDev(r.share(prm.warmup, prm.duration), all), 100*float64(over)/float64(n)
		t.Logf("EPP gate %d, settle %.3g S: %.0f%% of completed requests outlived it, dev %.1f pt", hold, settle, reaped, dev)
		return dev, reaped
	}
	devShort, reapedShort := run(8, 1.25)
	assert.Greater(t, reapedShort, 40.0)
	assert.Greater(t, devShort, 3.0, "false reaps must move the composition, or this test proves nothing")
	devOK, reapedOK := run(8, 2.8)
	assert.Less(t, reapedOK, 10.0)
	assert.Less(t, devOK, 2.0)
	devDeep, _ := run(0, 4)
	assert.Greater(t, devDeep, 3.0, "without a gate the queue wait outlives even 4 S")
}
