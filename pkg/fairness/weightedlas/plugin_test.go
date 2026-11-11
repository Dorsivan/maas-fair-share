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

import (
	"context"
	"encoding/json"
	"math"
	"testing"
	"time"

	"github.com/prometheus/client_golang/prometheus/testutil"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	fwkplugin "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/plugin"
	fwkrc "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requestcontrol"
	fwkrh "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requesthandling"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

// 1. Proportionality -- the headline claim. Two permanently backlogged groups
// at weights 2:1 must converge on a 2:1 split of delivered tokens.
func TestProportionality(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(2, 1)
	cfg.Enforce = true
	cfg.ProvisionalCharge = false
	p, clock := newTestPlugin(t, cfg)

	band := newSimBand(p,
		&simFlow{id: "a-group", depth: 1000, promptIn: 500, output: 100},
		&simFlow{id: "b-group", depth: 1000, promptIn: 500, output: 100},
	)
	res := band.run(t, p, 10000, time.Millisecond, clock)

	ratio := res.tokens["a-group"] / res.tokens["b-group"]
	assert.InEpsilon(t, 2.0, ratio, 0.02, "token ratio should converge on the weight ratio")
}

// 2. Unequal request sizes -- this is what distinguishes token-LAS from
// round-robin. At equal weights, a group whose requests are 10x larger must
// receive a tenth as many dispatches, so that the TOKEN split stays 1:1.
func TestUnequalRequestSizes(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(1, 1)
	cfg.Enforce = true
	cfg.ProvisionalCharge = false
	cfg.OutputTokenWeight = 1
	p, clock := newTestPlugin(t, cfg)

	band := newSimBand(p,
		&simFlow{id: "a-group", depth: 10000, promptIn: 100, output: 0},
		&simFlow{id: "b-group", depth: 10000, promptIn: 1000, output: 0},
	)
	res := band.run(t, p, 10000, time.Millisecond, clock)

	tokenRatio := res.tokens["a-group"] / res.tokens["b-group"]
	assert.InEpsilon(t, 1.0, tokenRatio, 0.02, "token share should be equal")

	requestRatio := float64(res.picks["a-group"]) / float64(res.picks["b-group"])
	assert.InEpsilon(t, 10.0, requestRatio, 0.05, "the small-request group should get 10x the dispatches")
}

// 3. Work conservation. With B idle, A must receive 100% -- not its weighted
// fraction. This is structural rather than implemented: IterateQueues never
// offers an empty queue, so there is nothing for the policy to split.
func TestWorkConservation(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(2, 1)
	cfg.Enforce = true
	cfg.ProvisionalCharge = false
	p, clock := newTestPlugin(t, cfg)

	band := newSimBand(p,
		&simFlow{id: "a-group", depth: 1000, promptIn: 500, output: 100},
		&simFlow{id: "b-group", depth: 0},
	)
	res := band.run(t, p, 1000, time.Millisecond, clock)

	assert.Equal(t, 1000, res.picks["a-group"], "the only backlogged group must get everything")
	assert.Zero(t, res.picks["b-group"])
}

// 4. The returning-idle tenant, run BOTH ways.
//
// The assertion that matters is on the INCUMBENT, not the newcomer: the cost of
// omitting the clamp lands on everyone else, as a stall while the returning
// tenant catches up. Running the no-clamp case and asserting it fails is what
// makes this a test of the mechanism rather than of the absence of load.
func TestReturningIdleTenant(t *testing.T) {
	t.Parallel()

	run := func(t *testing.T, clamp bool) (newcomerStreak, incumbentStall int) {
		t.Helper()
		cfg := twoGroupConfig(1, 1)
		cfg.Enforce = true
		cfg.ProvisionalCharge = false
		cfg.NewcomerClamp = clamp
		cfg.HalfLifeSeconds = 60
		p, clock := newTestPlugin(t, cfg)

		incumbent := &simFlow{id: "a-group", depth: 100000, promptIn: 1000, output: 500}
		newcomer := &simFlow{id: "b-group", depth: 0}
		band := newSimBand(p, incumbent, newcomer)

		// Phase 1: the incumbent runs alone long enough to reach a steady tab,
		// while the newcomer's tab decays through ten half-lives to ~0.
		band.run(t, p, 2000, 5*time.Millisecond, clock)

		// Phase 2: the newcomer returns.
		newcomer.depth = 100000
		newcomer.promptIn = 1000
		newcomer.output = 500
		newcomer.headAt = clock.now()
		res := band.run(t, p, 400, 5*time.Millisecond, clock)

		for _, id := range res.order {
			if id == "b-group" {
				newcomerStreak++
				incumbentStall++
			} else {
				newcomerStreak = 0
			}
			if id == "a-group" {
				break
			}
		}
		// Recompute the longest streak over the whole phase, not just the head.
		newcomerStreak, cur := 0, 0
		for _, id := range res.order {
			if id == "b-group" {
				cur++
				newcomerStreak = max(newcomerStreak, cur)
			} else {
				cur = 0
			}
		}
		return newcomerStreak, incumbentStall
	}

	withStreak, withStall := run(t, true)
	withoutStreak, withoutStall := run(t, false)

	assert.LessOrEqual(t, withStreak, 2,
		"with the clamp, the returning tenant goes first once, not a thousand times")
	assert.LessOrEqual(t, withStall, 2,
		"with the clamp, the incumbent is not stalled")

	// The same scenario must genuinely fail without the mechanism, otherwise the
	// assertions above are only measuring that the load was too light.
	assert.Greater(t, withoutStreak, 20,
		"without the clamp the returning tenant should monopolise -- if it does not, this test proves nothing")
	assert.Greater(t, withoutStall, 20,
		"without the clamp the incumbent should be starved through the transition")
}

// 4b. UNI-212: isBacklogEdge must distinguish a group that drained its own
// queue to empty for a few milliseconds (served efficiently, not absent) from
// one that was genuinely away for seconds. The old version keyed the edge to
// the shared Pick-call sequence alone, which advances on every Pick call --
// any group's enqueue, or the ~1ms dispatch ticker -- not once per this
// group's own request, so both gaps looked identical to it.
func TestNewcomerClampIdleGate(t *testing.T) {
	t.Parallel()
	bs := newBandState()
	t0 := testBasis

	// Cold start: always an edge, regardless of threshold.
	require.True(t, bs.isBacklogEdge("g", 1, t0, 2*time.Second))

	// Present on the literal immediately-preceding Pick call (seq 1 -> 2):
	// never an edge, however the clock moved -- the continuously-backlogged
	// case must stay free of the time check entirely.
	require.False(t, bs.isBacklogEdge("g", 2, t0.Add(500*time.Millisecond), 2*time.Second))

	// A seq gap (candidate absent at seq 3) opens, then returns at seq 4 after
	// only 20ms of real time: far short of the 2s gate, so not an edge.
	short := t0.Add(500*time.Millisecond + 20*time.Millisecond)
	require.False(t, bs.isBacklogEdge("g", 4, short, 2*time.Second),
		"a millisecond-scale drain must not count as a returning-idle newcomer")

	// Another seq gap, this time with 3s of real elapsed time: at or past the
	// gate, so this is a genuine return from idle.
	long := short.Add(3 * time.Second)
	require.True(t, bs.isBacklogEdge("g", 6, long, 2*time.Second),
		"a multi-second absence must still count as a returning-idle newcomer")

	// idleThreshold <= 0 reproduces the previous (buggy) behavior exactly: any
	// seq gap at all is an edge, however little real time elapsed.
	bs2 := newBandState()
	require.True(t, bs2.isBacklogEdge("g", 1, t0, 0))
	require.False(t, bs2.isBacklogEdge("g", 2, t0.Add(time.Millisecond), 0),
		"consecutive seq is never an edge, even with idleThreshold disabled")
	require.True(t, bs2.isBacklogEdge("g", 4, t0.Add(2*time.Millisecond), 0),
		"idleThreshold <= 0 means any seq gap counts, even a 1ms one")
}

// 4c. The same distinction, exercised through Pick(): a higher-weight group
// that is served well enough to fully drain its queue between bursts of its
// own traffic must not have its earned (favorably low) tab overwritten by the
// clamp every time, which is what let a continuously-flooding, lower-weight
// rival dominate despite the weight disadvantage (UNI-160/UNI-161's
// worker-ratio overshoot). This does not assert a specific equilibrium share
// -- the bursty group's duty cycle genuinely caps how much of the pool it can
// claim, independent of the clamp -- only that fixing the edge gate measurably
// moves its share toward its weight and away from the legacy floor, and fires
// far fewer clamps doing it.
func TestNewcomerClampGateImprovesBurstyShare(t *testing.T) {
	t.Parallel()

	run := func(t *testing.T, idleSeconds float64) (share float64, clamps float64) {
		t.Helper()
		cfg := twoGroupConfig(1, 3)
		cfg.Enforce = true
		cfg.ProvisionalCharge = false
		cfg.NewcomerClamp = true
		cfg.NewcomerClampIdleSeconds = idleSeconds
		cfg.HalfLifeSeconds = 60
		p, clock := newTestPlugin(t, cfg)

		flooder := &simFlow{id: "a-group", depth: 100000, promptIn: 500, output: 100}
		bursty := &simFlow{id: "b-group", depth: 0, promptIn: 500, output: 100}
		band := newSimBand(p, flooder, bursty)

		before := testutil.ToFloat64(newcomerClamps.WithLabelValues(boundID("b-group")))
		step := time.Millisecond
		totals := map[string]float64{}
		for burst := 0; burst < 200; burst++ {
			bursty.depth = 5
			bursty.headAt = clock.now()
			r := band.run(t, p, 5, step, clock)
			for id, v := range r.tokens {
				totals[id] += v
			}
			// A 20ms gap: far shorter than any meaningful fraction of the 60s
			// half-life, modeling a group drained by being served promptly,
			// not one that went away.
			bursty.depth = 0
			r = band.run(t, p, 20, step, clock)
			for id, v := range r.tokens {
				totals[id] += v
			}
		}
		after := testutil.ToFloat64(newcomerClamps.WithLabelValues(boundID("b-group")))
		return totals["b-group"] / (totals["a-group"] + totals["b-group"]), after - before
	}

	legacyShare, legacyClamps := run(t, 0)
	fixedShare, fixedClamps := run(t, 2.0)

	assert.Greater(t, fixedShare, legacyShare,
		"gating the edge on real elapsed time should move bursty's share up from the legacy seq-only baseline")
	assert.Less(t, fixedClamps, legacyClamps,
		"a 20ms inter-burst gap should clamp far less often once it must also clear the 2s idle gate")
	assert.Zero(t, fixedClamps,
		"a 20ms gap should never clear a 2s idle gate")
	assert.Greater(t, legacyClamps, float64(0),
		"the legacy path must actually exercise the clamp on every burst return, or this test proves nothing")
}

// 4d. UNI-220: a group with a dispatched-but-not-yet-completed request has not
// actually left, even on a Pick call where its own FlowQueue is momentarily
// empty and the wall-clock idle gate alone would call the return an edge.
// Live evidence (UNI-218's app1-flood at the settled config) found the clamp
// firing 28 times on the starved, concurrency-limited end-users group against
// 0 times on the continuously-flooding app1 -- almost every firing was this
// case, not a genuine multi-second absence. hasInFlight() adds a second,
// independent condition to the existing wall-clock gate; it does not relax it.
func TestNewcomerClampDoesNotFireWhileInFlight(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(1, 1)
	cfg.Enforce = true
	cfg.NewcomerClamp = true
	cfg.NewcomerClampIdleSeconds = 2.0
	cfg.HalfLifeSeconds = 60
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()

	gsA, gsB := p.states["a-group"], p.states["b-group"]
	gsA.charge(clock.now(), 1000)
	gsB.charge(clock.now(), 100) // b-group's earned advantage: below a-group's tab

	flooder := &simFlow{id: "a-group", depth: 1, headAt: clock.now()}
	starved := &simFlow{id: "b-group", depth: 0}
	band := newSimBand(p, flooder, starved)

	// b-group has a request dispatched a moment ago and still being served --
	// simulated directly on groupState rather than through PreRequest, so this
	// test exercises only the clamp gate, not the provisional-charge path.
	gsB.addInFlight(1, 0)
	for i := 0; i < 5; i++ {
		_, err := p.Pick(ctx, band.accessor())
		require.NoError(t, err)
		clock.advance(time.Second)
	}
	before := gsB.normalizedService(clock.now())

	// b-group returns as a candidate after a 5s absence -- ordinarily a
	// clamp-qualifying edge (past the 2s idle gate).
	starved.depth, starved.headAt = 1, clock.now()
	_, err := p.Pick(ctx, band.accessor())
	require.NoError(t, err)
	assert.Equal(t, before, gsB.normalizedService(clock.now()),
		"a group with an in-flight request must not be clamped on this edge -- it never left")

	// Complete the in-flight request and repeat the identical absence shape
	// with zero in-flight: this time the edge must still clamp, exactly as
	// before UNI-220 -- the gate is additive, not a relaxation.
	gsB.addInFlight(-1, 0)
	starved.depth = 0
	for i := 0; i < 5; i++ {
		_, err := p.Pick(ctx, band.accessor())
		require.NoError(t, err)
		clock.advance(time.Second)
	}
	starved.depth, starved.headAt = 1, clock.now()
	_, err = p.Pick(ctx, band.accessor())
	require.NoError(t, err)
	assert.Greater(t, gsB.normalizedService(clock.now()), before,
		"the same absence shape with no in-flight request must still clamp")
}

// 5. Decay. The tab measures recent usage, not all-time: one half-life after a
// charge, half of it must be gone.
func TestDecay(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(1, 1)
	cfg.HalfLifeSeconds = 60
	p, clock := newTestPlugin(t, cfg)

	gs := p.states["a-group"]
	gs.charge(clock.now(), 1000)
	require.InDelta(t, 1000.0, gs.normalizedService(clock.now()), 1e-9)

	clock.advance(60 * time.Second)
	assert.InDelta(t, 500.0, gs.normalizedService(clock.now()), 1e-9)

	clock.advance(120 * time.Second)
	assert.InDelta(t, 125.0, gs.normalizedService(clock.now()), 1e-9,
		"a half-life is not a window: a quarter of the tab survives two more of them")
}

// 6. Grouping. Many subscriptions must collapse onto ONE flow ID, or the
// end-user group's share grows with every subscription added.
func TestGrouping(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, testConfig())
	ctx := context.Background()

	resolve := func(sub string) string {
		req := &fwksched.InferenceRequest{Headers: map[string]string{"x-maas-subscription-id": sub}}
		require.NoError(t, p.RequestHeader(ctx, req))
		return req.FairnessID
	}

	assert.Equal(t, "end-users", resolve("end-user-a"))
	assert.Equal(t, "end-users", resolve("end-user-b"),
		"two end-user subscriptions must share one flow, not hold two copies of the weight")
	assert.Equal(t, "app1", resolve("app1-production"))
	assert.Equal(t, "app2", resolve("app2-batch"))

	// The fragility the design calls out: a typo falls into the catch-all
	// silently, so it must be counted.
	assert.Equal(t, "unclassified", resolve("enduser-foo"))
	assert.Equal(t, "unclassified", resolve(""))

	d := p.dump()
	assert.Equal(t, uint64(1), d.UnmatchedTotal, "the typo must be counted; the empty ID is not a typo")
	assert.Equal(t, []string{"enduser-foo"}, d.UnmatchedSample)
}

// 6b. Exact matches beat prefixes, and a longer prefix beats a shorter one, no
// matter what order the rules appear in the ConfigMap.
func TestExactBeatsPrefix(t *testing.T) {
	t.Parallel()
	cfg := DefaultConfig()
	cfg.StateLogIntervalSeconds = 0
	cfg.Groups = []GroupConfig{
		{Name: "pool", Weight: 10, Match: GroupMatch{Prefix: []string{"end-user-"}}},
		{Name: "vip", Weight: 10, Match: GroupMatch{
			Exact:  []string{"end-user-whale"},
			Prefix: []string{"end-user-gold-"},
		}},
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "unclassified", Weight: 1}
	p, _ := newTestPlugin(t, cfg)

	name, matched := p.groups.resolve("end-user-whale")
	assert.True(t, matched)
	assert.Equal(t, "vip", name, "an exact match must beat another group's prefix")

	name, _ = p.groups.resolve("end-user-gold-7")
	assert.Equal(t, "vip", name, "the longer prefix must win")

	name, _ = p.groups.resolve("end-user-7")
	assert.Equal(t, "pool", name)
}

// 7. Spoof resistance. A client naming its own queue must be ignored. The
// director's own fallback only fills FairnessID in when it is EMPTY, so
// defaulting rather than overwriting would be exploitable.
func TestSpoofResistance(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, testConfig())

	req := &fwksched.InferenceRequest{
		// Both the spoofed header and a FairnessID already set by an upstream
		// identity plugin, which is the worse of the two cases.
		FairnessID: "app1",
		Headers: map[string]string{
			"x-llm-d-inference-fairness-id": "app1",
			"x-maas-subscription-id":        "end-user-mallory",
		},
	}
	require.NoError(t, p.RequestHeader(context.Background(), req))
	assert.Equal(t, "end-users", req.FairnessID,
		"the authenticated subscription must override anything the client set")
}

// 8. Provisional true-up. The net effect on the tab must equal the real cost,
// not the estimate.
func TestProvisionalTrueUp(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(1, 1)
	cfg.ProvisionalCharge = true
	cfg.HalfLifeSeconds = 60
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()
	gs := p.states["a-group"]

	maxTokens := int64(1000)
	req := &fwksched.InferenceRequest{
		FairnessID:       "a-group",
		RequestSizeBytes: 4000,
		Body:             &fwkrh.InferenceRequestBody{MaxOutputTokens: &maxTokens},
	}
	require.NoError(t, p.PreRequest(ctx, req, nil))

	// Mid-flight the tab must already reflect the estimate -- that is the whole
	// point of charging at dispatch.
	estimated := gs.normalizedService(clock.now())
	assert.Positive(t, estimated, "the tab must move before the response arrives")
	assert.Equal(t, int64(1), gs.inFlight)

	resp := &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseNatural,
		Usage:            fwkrh.Usage{PromptTokens: 950, CompletionTokens: 100, TotalTokens: 1050},
	}
	p.ResponseBody(ctx, req, resp, nil)

	want := p.cost(950, 0, 100)
	assert.InDelta(t, want, gs.normalizedService(clock.now()), 1e-9,
		"after true-up the tab must equal the real cost")
	assert.Zero(t, gs.inFlight)
	assert.Zero(t, gs.provisionalTotal)
}

// 8a2. UNI-190: a context-length rejection (HTTP 400, no usage block) must be
// fully reversed, not booked -- the board's decision was to exempt it
// entirely, not cap it. Before this fix, ResponseBody's no-usage branch
// treated every no-usage completion the same way and permanently booked the
// oversized prompt's own dispatch-time estimate.
func TestContextLengthRejectionIsExemptFromProvisionalCharge(t *testing.T) {
	t.Parallel()
	// A dedicated, unused group name: contendedServiceTokens and
	// provisionalChargesExempted are package-global CounterVecs shared across
	// every parallel test in this package, so reusing "a-group"/"b-group" here
	// would make the ledger assertion below flaky against unrelated tests'
	// charges. See TestContendedServiceTokensEqualChargedCost for the same
	// convention.
	const group = "ctx-length-exempt-group"
	cfg := DefaultConfig()
	cfg.Groups = []GroupConfig{
		{Name: group, Weight: 1, Match: GroupMatch{Exact: []string{group}}},
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "ctx-length-exempt-fallback", Weight: 1}
	cfg.ProvisionalCharge = true
	cfg.HalfLifeSeconds = 60
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()
	gs := p.states[group]

	// Contended at dispatch, same as UNI-148's C6 run -- otherwise this test
	// cannot distinguish the fix from "never contended, so never booked anyway."
	p.lastContendedUnixNano.Store(clock.now().UnixNano())

	maxTokens := int64(1000)
	req := &fwksched.InferenceRequest{
		FairnessID:       group,
		RequestSizeBytes: 80000, // a deliberately oversized prompt, like UNI-148's C6
		Body:             &fwkrh.InferenceRequestBody{MaxOutputTokens: &maxTokens},
	}
	require.NoError(t, p.PreRequest(ctx, req, nil))
	assert.Positive(t, gs.normalizedService(clock.now()), "the hold must land on the tab at dispatch")
	assert.Equal(t, int64(1), gs.inFlight)

	clock.advance(30 * time.Second)

	// The backend rejects the request before generating anything: status 400,
	// no usage block. ResponseHeader runs first, same as in production.
	p.ResponseHeader(ctx, req, &fwkrc.Response{Headers: map[string]string{":status": "400"}}, nil)
	resp := &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseNatural,
	}
	p.ResponseBody(ctx, req, resp, nil)

	assert.InDelta(t, 0, gs.normalizedService(clock.now()), 1e-9,
		"the hold must be fully reversed, leaving the tab exactly as if it had never been charged")
	assert.Zero(t, gs.inFlight)
	assert.Zero(t, gs.provisionalTotal)

	got := testutil.ToFloat64(contendedServiceTokens.WithLabelValues(group))
	assert.Zero(t, got, "an exempted request must never reach the SLI ledger")

	exempted := testutil.ToFloat64(provisionalChargesExempted.WithLabelValues(group, "error_status"))
	assert.Equal(t, float64(1), exempted)
}

// 8a3. UNI-213 (board follow-up to UNI-190): a backend error status other
// than 400 -- e.g. a 500 -- must be refunded the same way. UNI-148's C6 run
// found 14 of app2's 49 oversized-prompt requests came back 500 rather than
// 400, and those stayed charged under UNI-190's 400-only scope; this widens
// the exemption to any non-2xx status.
func TestGenericErrorStatusIsRefunded(t *testing.T) {
	t.Parallel()
	const group = "error-status-exempt-group"
	cfg := DefaultConfig()
	cfg.Groups = []GroupConfig{
		{Name: group, Weight: 1, Match: GroupMatch{Exact: []string{group}}},
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "error-status-exempt-fallback", Weight: 1}
	cfg.ProvisionalCharge = true
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()
	gs := p.states[group]

	p.lastContendedUnixNano.Store(clock.now().UnixNano())

	req := &fwksched.InferenceRequest{FairnessID: group, RequestSizeBytes: 4000}
	require.NoError(t, p.PreRequest(ctx, req, nil))
	require.Positive(t, gs.normalizedService(clock.now()))

	p.ResponseHeader(ctx, req, &fwkrc.Response{Headers: map[string]string{":status": "500"}}, nil)
	p.ResponseBody(ctx, req, &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseNatural,
	}, nil)

	assert.InDelta(t, 0, gs.normalizedService(clock.now()), 1e-9,
		"a 500, like a 400, delivered nothing and must be fully reversed")
	assert.Zero(t, gs.inFlight)

	got := testutil.ToFloat64(contendedServiceTokens.WithLabelValues(group))
	assert.Zero(t, got, "an exempted request must never reach the SLI ledger")

	exempted := testutil.ToFloat64(provisionalChargesExempted.WithLabelValues(group, "error_status"))
	assert.Equal(t, float64(1), exempted)
}

// 8a4. A completion that reports no usage but carries no error status at all
// (TerminationCauseNatural, status 200 or no status captured) is a model
// server genuinely missing --enable-force-include-usage -- real generation
// happened and real GPU time was spent. This must stay charged; it is the one
// no-usage case UNI-190 and UNI-213 both deliberately leave alone, and a
// regression here would silently undercharge every tenant hitting that
// misconfiguration.
func TestMissingUsageFlagStillBooksTheEstimate(t *testing.T) {
	t.Parallel()
	const group = "missing-usage-flag-group"
	cfg := DefaultConfig()
	cfg.Groups = []GroupConfig{
		{Name: group, Weight: 1, Match: GroupMatch{Exact: []string{group}}},
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "missing-usage-flag-fallback", Weight: 1}
	cfg.ProvisionalCharge = true
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()

	p.lastContendedUnixNano.Store(clock.now().UnixNano())

	req := &fwksched.InferenceRequest{FairnessID: group, RequestSizeBytes: 4000}
	require.NoError(t, p.PreRequest(ctx, req, nil))
	est := p.estimateCost(req, p.states[group])

	p.ResponseHeader(ctx, req, &fwkrc.Response{Headers: map[string]string{":status": "200"}}, nil)
	p.ResponseBody(ctx, req, &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseNatural,
	}, nil)

	got := testutil.ToFloat64(contendedServiceTokens.WithLabelValues(group))
	assert.InDelta(t, est, got, 1e-9,
		"a 200 with no usage block is a real, served request -- it must still book the estimate")

	exempted := testutil.ToFloat64(provisionalChargesExempted.WithLabelValues(group, "error_status"))
	assert.Zero(t, exempted, "a served (2xx) request must never be counted as exempted")
}

// 8a5. UNI-213: a cancelled context (TerminationCauseError -- an EPP-side
// failure, or a cancellation that reached the EPP before its propagation
// completed) must be refunded, same as an error status or a stream reset.
func TestContextCancelIsRefunded(t *testing.T) {
	t.Parallel()
	const group = "context-cancel-exempt-group"
	cfg := DefaultConfig()
	cfg.Groups = []GroupConfig{
		{Name: group, Weight: 1, Match: GroupMatch{Exact: []string{group}}},
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "context-cancel-exempt-fallback", Weight: 1}
	cfg.ProvisionalCharge = true
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()
	gs := p.states[group]

	p.lastContendedUnixNano.Store(clock.now().UnixNano())

	req := &fwksched.InferenceRequest{FairnessID: group, RequestSizeBytes: 4000}
	require.NoError(t, p.PreRequest(ctx, req, nil))
	require.Positive(t, gs.normalizedService(clock.now()))

	// No ResponseHeader call: a cancelled context never got as far as a backend
	// status.
	p.ResponseBody(ctx, req, &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseError,
	}, nil)

	assert.InDelta(t, 0, gs.normalizedService(clock.now()), 1e-9,
		"a cancelled context delivered nothing and must be fully reversed")
	assert.Zero(t, gs.inFlight)

	got := testutil.ToFloat64(contendedServiceTokens.WithLabelValues(group))
	assert.Zero(t, got, "an exempted request must never reach the SLI ledger")

	exempted := testutil.ToFloat64(provisionalChargesExempted.WithLabelValues(group, "context_cancel"))
	assert.Equal(t, float64(1), exempted)
}

// 8a6. TerminationCauseEvicted is deliberately NOT exempted -- an eviction is
// the EPP's own capacity-reclaim decision, a different question UNI-213 does
// not address, so it must keep booking the estimate exactly like it did
// before this ticket.
func TestEvictedStreamStillBooksTheEstimate(t *testing.T) {
	t.Parallel()
	const group = "evicted-group"
	cfg := DefaultConfig()
	cfg.Groups = []GroupConfig{
		{Name: group, Weight: 1, Match: GroupMatch{Exact: []string{group}}},
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "evicted-fallback", Weight: 1}
	cfg.ProvisionalCharge = true
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()

	p.lastContendedUnixNano.Store(clock.now().UnixNano())

	req := &fwksched.InferenceRequest{FairnessID: group, RequestSizeBytes: 4000}
	require.NoError(t, p.PreRequest(ctx, req, nil))
	est := p.estimateCost(req, p.states[group])

	p.ResponseBody(ctx, req, &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseEvicted,
	}, nil)

	got := testutil.ToFloat64(contendedServiceTokens.WithLabelValues(group))
	assert.InDelta(t, est, got, 1e-9, "an eviction is out of this ticket's scope and must still book the estimate")

	exempted := testutil.ToFloat64(provisionalChargesExempted.WithLabelValues(group, "context_cancel"))
	assert.Zero(t, exempted)
}

// 8b. Estimator independence -- the decisive test for the DECAYED correction.
//
// The provisional charge decays for the whole generation. Adding the raw
// (actual - charged) delta at completion would attribute the estimate to
// dispatch time and the correction to completion time, leaving the final tab
// dependent on how wrong the estimate was. Decaying the correction by the
// in-flight time makes the result exactly identical to charging the true value
// at dispatch -- so estimation can only ever affect in-flight ordering.
func TestTrueUpIsIndependentOfEstimatorQuality(t *testing.T) {
	t.Parallel()

	const (
		actualPrompt     = 2000
		actualCompletion = 500
		inflight         = 30 * time.Second // half of the half-life
		halfLife         = 60.0
	)

	finalTab := func(t *testing.T, sizeBytes int, maxTokens int64) float64 {
		t.Helper()
		cfg := twoGroupConfig(1, 1)
		cfg.ProvisionalCharge = true
		cfg.HalfLifeSeconds = halfLife
		p, clock := newTestPlugin(t, cfg)
		ctx := context.Background()

		mt := maxTokens
		req := &fwksched.InferenceRequest{
			FairnessID:       "a-group",
			RequestSizeBytes: sizeBytes,
			Body:             &fwkrh.InferenceRequestBody{MaxOutputTokens: &mt},
		}
		require.NoError(t, p.PreRequest(ctx, req, nil))
		clock.advance(inflight)
		p.ResponseBody(ctx, req, &fwkrc.Response{
			EndOfStream:      true,
			TerminationCause: fwkrc.TerminationCauseNatural,
			Usage: fwkrh.Usage{
				PromptTokens:     actualPrompt,
				CompletionTokens: actualCompletion,
				TotalTokens:      actualPrompt + actualCompletion,
			},
		}, nil)
		return p.states["a-group"].normalizedService(clock.now())
	}

	// Roughly 10x over and 10x under the truth.
	over := finalTab(t, 80000, 5000)
	under := finalTab(t, 800, 50)

	assert.InDelta(t, over, under, 1e-6,
		"the final tab must not depend on the estimate; the correction is being added undecayed")

	// And it must equal what charging the true cost at dispatch would have left.
	p, _ := newTestPlugin(t, twoGroupConfig(1, 1))
	reference := p.cost(actualPrompt, 0, actualCompletion) * math.Exp2(-inflight.Seconds()/halfLife)
	assert.InDelta(t, reference, over, 1e-6)
}

// 8c. The SLI numerator must equal the cost actually charged. The provisional
// estimate and its true-up are one logical charge; gating each independently,
// at its own later moment, can accept one half and drop the other, so the
// metric stops equalling what the tab was actually charged.
func TestContendedServiceTokensEqualChargedCost(t *testing.T) {
	t.Parallel()
	cfg := DefaultConfig()
	cfg.Groups = []GroupConfig{
		{Name: "contend-fix-group", Weight: 1, Match: GroupMatch{Exact: []string{"contend-fix-group"}}},
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "contend-fix-fallback", Weight: 1}
	cfg.ProvisionalCharge = true
	cfg.HalfLifeSeconds = 60
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()

	// The band is contended only at dispatch. By the time the response lands,
	// contention is long gone -- a gate re-checked at completion would see no
	// contention and drop the true-up, leaving the metric at the estimate
	// instead of the real cost.
	p.lastContendedUnixNano.Store(clock.now().UnixNano())

	maxTokens := int64(1000)
	req := &fwksched.InferenceRequest{
		FairnessID:       "contend-fix-group",
		RequestSizeBytes: 4000,
		Body:             &fwkrh.InferenceRequestBody{MaxOutputTokens: &maxTokens},
	}
	require.NoError(t, p.PreRequest(ctx, req, nil))

	clock.advance(2 * maxContendedStep)

	resp := &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseNatural,
		Usage:            fwkrh.Usage{PromptTokens: 1000, CompletionTokens: 2000, TotalTokens: 3000},
	}
	p.ResponseBody(ctx, req, resp, nil)

	actual := p.cost(1000, 0, 2000)
	got := testutil.ToFloat64(contendedServiceTokens.WithLabelValues("contend-fix-group"))
	assert.InDelta(t, actual, got, 1e-9,
		"the SLI numerator must equal the real cost charged for a request contended at dispatch")
}

// 8d. Same invariant, the other direction: the estimator OVERSHOOTS, so the
// true-up at completion is a negative delta. A gate that booked the estimate
// at dispatch and the (now negative) delta separately would have to drop the
// delta -- a counter cannot move backwards -- leaving the metric stuck at the
// estimate, permanently overstating the group's real cost. Booking the real
// cost once, at completion, has no such asymmetry.
func TestContendedServiceTokensEqualChargedCostOnOverestimate(t *testing.T) {
	t.Parallel()
	cfg := DefaultConfig()
	cfg.Groups = []GroupConfig{
		{Name: "contend-fix-group-over", Weight: 1, Match: GroupMatch{Exact: []string{"contend-fix-group-over"}}},
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "contend-fix-fallback-over", Weight: 1}
	cfg.ProvisionalCharge = true
	cfg.HalfLifeSeconds = 60
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()

	p.lastContendedUnixNano.Store(clock.now().UnixNano())

	// RequestSizeBytes=4000 and MaxOutputTokens=1000 put the estimate at
	// roughly 2x the actual 50-token completion below, so the true-up delta is
	// negative.
	maxTokens := int64(1000)
	req := &fwksched.InferenceRequest{
		FairnessID:       "contend-fix-group-over",
		RequestSizeBytes: 4000,
		Body:             &fwkrh.InferenceRequestBody{MaxOutputTokens: &maxTokens},
	}
	require.NoError(t, p.PreRequest(ctx, req, nil))

	clock.advance(2 * maxContendedStep)

	resp := &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseNatural,
		Usage:            fwkrh.Usage{PromptTokens: 1000, CompletionTokens: 50, TotalTokens: 1050},
	}
	p.ResponseBody(ctx, req, resp, nil)

	actual := p.cost(1000, 0, 50)
	got := testutil.ToFloat64(contendedServiceTokens.WithLabelValues("contend-fix-group-over"))
	assert.InDelta(t, actual, got, 1e-9,
		"the SLI numerator must equal the real (lower) cost, not the estimate it overshot")
}

// 9. Stream reset (UNI-213, reversing the prior abort-spam-prevention design
// that this test asserted before: see git history for
// "TestAbortKeepsTheEstimate"). A client disconnect, an Envoy drain/restart,
// or an upstream reset all surface as TerminationCauseClientDisconnect, and
// the framework cannot tell them apart from the EPP's side of the stream; the
// board's UNI-213 decision was that none of them delivered anything to the
// tenant, so none of them should be booked.
func TestStreamResetIsRefunded(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(1, 1)
	cfg.ProvisionalCharge = true
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()
	gs := p.states["a-group"]

	req := &fwksched.InferenceRequest{FairnessID: "a-group", RequestSizeBytes: 4000}
	require.NoError(t, p.PreRequest(ctx, req, nil))
	require.Positive(t, gs.normalizedService(clock.now()))

	p.ResponseBody(ctx, req, &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseClientDisconnect,
	}, nil)

	assert.InDelta(t, 0, gs.normalizedService(clock.now()), 1e-9,
		"a stream reset delivered nothing and must be fully reversed")
	assert.Zero(t, gs.inFlight, "in-flight accounting must still be released")
}

// 9b. A refunded stream reset must never reach the SLI numerator either --
// same assertion shape as TestContextLengthRejectionIsExemptFromProvisionalCharge,
// for the path this test used to assert stayed charged
// (TestAbortedRequestStillBooksContendedService, pre-UNI-213).
func TestStreamResetNeverReachesContendedService(t *testing.T) {
	t.Parallel()
	const group = "stream-reset-exempt-group"
	cfg := DefaultConfig()
	cfg.Groups = []GroupConfig{
		{Name: group, Weight: 1, Match: GroupMatch{Exact: []string{group}}},
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "stream-reset-exempt-fallback", Weight: 1}
	cfg.ProvisionalCharge = true
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()

	p.lastContendedUnixNano.Store(clock.now().UnixNano())

	req := &fwksched.InferenceRequest{FairnessID: group, RequestSizeBytes: 4000}
	require.NoError(t, p.PreRequest(ctx, req, nil))

	p.ResponseBody(ctx, req, &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseClientDisconnect,
	}, nil)

	got := testutil.ToFloat64(contendedServiceTokens.WithLabelValues(group))
	assert.Zero(t, got, "an exempted request must never reach the SLI ledger")

	exempted := testutil.ToFloat64(provisionalChargesExempted.WithLabelValues(group, "stream_reset"))
	assert.Equal(t, float64(1), exempted)
}

// 10. Non-final chunks must not move the tab.
func TestNonFinalChunksAreNoOps(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(1, 1)
	cfg.ProvisionalCharge = false
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()
	gs := p.states["a-group"]

	req := &fwksched.InferenceRequest{FairnessID: "a-group"}
	p.ResponseBody(ctx, req, &fwkrc.Response{
		EndOfStream: false,
		Usage:       fwkrh.Usage{PromptTokens: 1000, CompletionTokens: 1000},
	}, nil)
	assert.Zero(t, gs.normalizedService(clock.now()))

	p.ResponseBody(ctx, req, &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseNatural,
		Usage:            fwkrh.Usage{PromptTokens: 1000, CompletionTokens: 1000},
	}, nil)
	assert.InDelta(t, p.cost(1000, 0, 1000), gs.normalizedService(clock.now()), 1e-9,
		"exactly one charge, on the terminal chunk")
}

// 11. Shadow mode. Accounting and metrics are identical; only the returned pick
// differs. This is the whole rollout strategy, so it has to be exact.
func TestShadowMode(t *testing.T) {
	t.Parallel()

	// b-group's head has waited longer, so FCFS prefers it; a-group has the
	// lower tab, so the policy prefers it. The two answers are distinguishable.
	build := func(t *testing.T, enforce bool) (string, map[string]float64) {
		t.Helper()
		cfg := twoGroupConfig(1, 1)
		cfg.Enforce = enforce
		cfg.ProvisionalCharge = false
		p, clock := newTestPlugin(t, cfg)

		gs := p.states["b-group"]
		gs.charge(clock.now(), 0) // touch, so both accumulators share an anchor
		p.states["a-group"].charge(clock.now(), 0)

		band := newSimBand(p,
			&simFlow{id: "a-group", depth: 10, headAt: clock.now(), promptIn: 100, output: 10},
			&simFlow{id: "b-group", depth: 10, headAt: clock.now().Add(-time.Minute), promptIn: 100, output: 10},
		)
		// Give b-group a tab so LAS prefers a-group, while FCFS still prefers
		// b-group on head wait.
		gs.charge(clock.now(), 10000)

		q, err := p.Pick(context.Background(), band.accessor())
		require.NoError(t, err)
		require.NotNil(t, q)

		tabs := map[string]float64{}
		for name, s := range p.states {
			tabs[name] = s.normalizedService(clock.now())
		}
		return q.FlowKey().ID, tabs
	}

	shadowPick, shadowTabs := build(t, false)
	enforcePick, enforceTabs := build(t, true)

	assert.Equal(t, "b-group", shadowPick, "shadow mode must return the FCFS pick")
	assert.Equal(t, "a-group", enforcePick, "enforcing must return the weighted-LAS pick")
	assert.Equal(t, enforceTabs, shadowTabs, "accounting must be identical across the cut")
}

// 12. Determinism. IterateQueues order is unspecified and backing
// implementations range a Go map, so without an explicit sort the tie-break
// would drift run to run.
func TestDeterminism(t *testing.T) {
	t.Parallel()
	var reference []string
	for run := range 100 {
		cfg := twoGroupConfig(3, 2)
		cfg.Enforce = true
		cfg.ProvisionalCharge = false
		p, clock := newTestPlugin(t, cfg)
		band := newSimBand(p,
			&simFlow{id: "a-group", depth: 1000, promptIn: 300, output: 50},
			&simFlow{id: "b-group", depth: 1000, promptIn: 300, output: 50},
		)
		res := band.run(t, p, 200, time.Millisecond, clock)
		if run == 0 {
			reference = res.order
			continue
		}
		require.Equal(t, reference, res.order, "pick sequence drifted on run %d", run)
	}
}

// 13. Factory validation. The framework hands the factory a
// DisallowUnknownFields decoder, so a typo in a key must be a startup failure
// rather than a silently defaulted value.
func TestFactoryValidation(t *testing.T) {
	t.Parallel()

	valid := `{
      "groups": [{"name":"app1","weight":20,"match":{"exact":["app1-production"]}}],
      "defaultGroup": {"name":"unclassified","weight":5}
    }`

	cases := []struct {
		name    string
		params  string
		wantErr string
	}{
		{"valid", valid, ""},
		{"nil parameters uses defaults", "", ""},
		// Note that encoding/json matches field names case-INSENSITIVELY, so
		// "halflifeSeconds" would be accepted as halfLifeSeconds. Only a key
		// that is genuinely absent from the struct is rejected.
		{"unknown key", `{"halfLifeSecond": 60}`, "unknown field"},
		{"plausible typo", `{"outputTokensWeight": 8}`, "unknown field"},
		{"negative weight", `{"groups":[{"name":"a","weight":-1,"match":{"exact":["a"]}}],
            "defaultGroup":{"name":"d","weight":1}}`, "weight must be > 0"},
		{"zero weight", `{"groups":[{"name":"a","weight":0,"match":{"exact":["a"]}}],
            "defaultGroup":{"name":"d","weight":1}}`, "weight must be > 0"},
		{"group with no match rule", `{"groups":[{"name":"a","weight":1}],
            "defaultGroup":{"name":"d","weight":1}}`, "at least one of exact or prefix"},
		{"empty prefix matches everything", `{"groups":[{"name":"a","weight":1,"match":{"prefix":[""]}}],
            "defaultGroup":{"name":"d","weight":1}}`, "empty prefix"},
		{"duplicate group name", `{"groups":[
            {"name":"a","weight":1,"match":{"exact":["x"]}},
            {"name":"a","weight":1,"match":{"exact":["y"]}}],
            "defaultGroup":{"name":"d","weight":1}}`, "duplicate group name"},
		{"subscription claimed twice", `{"groups":[
            {"name":"a","weight":1,"match":{"exact":["x"]}},
            {"name":"b","weight":1,"match":{"exact":["x"]}}],
            "defaultGroup":{"name":"d","weight":1}}`, "claimed by both"},
		{"zero cached weight is an exemption", `{"cachedInputTokenWeight": 0}`, "0 is an exemption"},
		{"negative half-life", `{"halfLifeSeconds": -1}`, "halfLifeSeconds must be >= 0"},
		{"unknown cost model", `{"costModel": "flops"}`, "costModel must be"},
		{"zero bytes per token", `{"estimatedBytesPerToken": 0}`, "estimatedBytesPerToken must be > 0"},
		{"empty identity header", `{"identityHeader": ""}`, "identityHeader must not be empty"},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			t.Parallel()
			var dec *json.Decoder
			if tc.params != "" {
				dec = fwkplugin.StrictDecoder(json.RawMessage(tc.params))
			}
			plug, err := Factory("maas-fairness", dec, nil)
			if tc.wantErr == "" {
				require.NoError(t, err)
				require.NotNil(t, plug)
				assert.Equal(t, PluginType, plug.TypedName().Type)
				assert.Equal(t, "maas-fairness", plug.TypedName().Name)
				return
			}
			require.Error(t, err)
			assert.Contains(t, err.Error(), tc.wantErr)
		})
	}
}

// The output estimator: max_tokens is a cap, never the central value, and the
// per-group observed mean is only trusted after warm-up.
func TestOutputEstimator(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(1, 1)
	cfg.DefaultEstimatedOutputTokens = 512
	p, _ := newTestPlugin(t, cfg)
	gs := p.states["a-group"]

	withCap := func(c int64) *fwksched.InferenceRequest {
		return &fwksched.InferenceRequest{Body: &fwkrh.InferenceRequestBody{MaxOutputTokens: &c}}
	}

	assert.Equal(t, 512, p.estimateOutputTokens(&fwksched.InferenceRequest{}, gs),
		"no history and no cap falls back to the configured default")
	assert.Equal(t, 100, p.estimateOutputTokens(withCap(100), gs),
		"a cap below the default binds")
	assert.Equal(t, 512, p.estimateOutputTokens(withCap(4096), gs),
		"a cap above the default must not become the estimate")

	// Below warm-up the observations are ignored.
	for range ewmaWarmupSamples - 1 {
		gs.recordCompletion(50, 1000, 0)
	}
	assert.Equal(t, 512, p.estimateOutputTokens(&fwksched.InferenceRequest{}, gs))

	gs.recordCompletion(50, 1000, 0)
	assert.Equal(t, 50, p.estimateOutputTokens(&fwksched.InferenceRequest{}, gs),
		"once warm, the group's own history beats the global default")
}

// The cost model is the one place a unit is chosen; everything downstream is
// unit-agnostic.
func TestCostModels(t *testing.T) {
	t.Parallel()

	cfg := twoGroupConfig(1, 1)
	cfg.InputTokenWeight = 1
	cfg.OutputTokenWeight = 2
	cfg.CachedInputTokenWeight = 1
	p, _ := newTestPlugin(t, cfg)
	assert.InDelta(t, 10000.0+2*500, p.cost(10000, 9000, 500), 1e-9,
		"at cachedInputTokenWeight 1.0 the cached term drops out entirely")

	cfg.CachedInputTokenWeight = 0.1
	discounted, _ := newTestPlugin(t, cfg)
	assert.InDelta(t, 1000.0+0.1*9000+2*500, discounted.cost(10000, 9000, 500), 1e-9)

	// A server reporting more cached than prompt tokens must not produce a
	// negative uncached term.
	assert.GreaterOrEqual(t, p.cost(100, 500, 0), 0.0)

	cfg.CostModel = CostModelVRAMTime
	vram, _ := newTestPlugin(t, cfg)
	assert.InDelta(t, 500.0*(10000+250), vram.cost(10000, 9000, 500), 1e-9)
}

// The identity header is matched case-insensitively: the framework lowercases
// header keys, but a parser or a test may not have.
func TestIdentityHeaderCaseInsensitive(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, testConfig())
	req := &fwksched.InferenceRequest{Headers: map[string]string{"X-MaaS-Subscription-ID": " app1-production "}}
	require.NoError(t, p.RequestHeader(context.Background(), req))
	assert.Equal(t, "app1", req.FairnessID)
}

// The observed half-lives account the same charges through other windows
// without affecting the one that drives decisions.
func TestObservedHalfLives(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(1, 1)
	cfg.HalfLifeSeconds = 60
	cfg.ObservedHalfLivesSeconds = []float64{20, 120}
	p, clock := newTestPlugin(t, cfg)

	gs := p.states["a-group"]
	gs.charge(clock.now(), 1000)
	clock.advance(60 * time.Second)

	assert.InDelta(t, 500.0, gs.normalizedService(clock.now()), 1e-9)
	observed := gs.observedNormalized(clock.now())
	require.Len(t, observed, 2)
	assert.InDelta(t, 1000*math.Exp2(-3), observed[0], 1e-9, "the 20s window has forgotten more")
	assert.InDelta(t, 1000*math.Exp2(-0.5), observed[1], 1e-9, "the 120s window has forgotten less")
}

// A zero half-life disables decay entirely: the tab becomes cumulative since
// process start. Supported, but it means this morning's heavy group starves all
// afternoon -- so it must at least behave exactly as documented.
func TestZeroHalfLifeDisablesDecay(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(1, 1)
	cfg.HalfLifeSeconds = 0
	p, clock := newTestPlugin(t, cfg)

	gs := p.states["a-group"]
	gs.charge(clock.now(), 1000)
	clock.advance(24 * time.Hour)
	assert.InDelta(t, 1000.0, gs.normalizedService(clock.now()), 1e-9)
}

// An unrecognised flow ID -- flow control will create a queue for any ID -- must
// fold into the catch-all rather than mint unbounded state or divide by a zero
// weight.
func TestUnknownFlowIDFoldsIntoCatchAll(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, testConfig())
	assert.Same(t, p.states["unclassified"], p.stateFor("some-flow-nobody-configured"))
	assert.Len(t, p.states, 4, "state must not be created for unconfigured flow IDs")
}

func TestDumpStateIsBoundedAndSanitized(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, testConfig())
	ctx := context.Background()

	for i := range 100 {
		req := &fwksched.InferenceRequest{
			Headers: map[string]string{"x-maas-subscription-id": "bogus-" + time.Duration(i).String()},
		}
		require.NoError(t, p.RequestHeader(ctx, req))
	}

	raw, err := p.DumpState()
	require.NoError(t, err)
	var d dumpState
	require.NoError(t, json.Unmarshal(raw, &d))

	assert.Equal(t, uint64(100), d.UnmatchedTotal)
	assert.LessOrEqual(t, len(d.UnmatchedSample), maxLoggedUnmatched,
		"the unmatched sample is client-controlled and must stay bounded")
	assert.True(t, d.Truncated)
	assert.Len(t, d.Groups, 4)
	assert.False(t, d.Enforcing)
}
