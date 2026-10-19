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

// 9. Abort. A stream that ends with no usage block keeps its estimate.
// Refunding would make abort-spam free.
func TestAbortKeepsTheEstimate(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(1, 1)
	cfg.ProvisionalCharge = true
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()
	gs := p.states["a-group"]

	req := &fwksched.InferenceRequest{FairnessID: "a-group", RequestSizeBytes: 4000}
	require.NoError(t, p.PreRequest(ctx, req, nil))
	charged := gs.normalizedService(clock.now())
	require.Positive(t, charged)

	p.ResponseBody(ctx, req, &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseClientDisconnect,
	}, nil)

	assert.InDelta(t, charged, gs.normalizedService(clock.now()), 1e-9,
		"an aborted request must not be refunded")
	assert.Zero(t, gs.inFlight, "in-flight accounting must still be released")

	// The charge is not permanent: it decays away on its own.
	clock.advance(10 * time.Minute)
	assert.Less(t, gs.normalizedService(clock.now()), charged*0.01)
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
