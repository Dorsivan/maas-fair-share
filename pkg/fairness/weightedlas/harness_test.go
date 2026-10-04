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
	"testing"
	"time"

	"github.com/stretchr/testify/require"

	"github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol"
	fwkfcmocks "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol/mocks"
	fwkrc "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requestcontrol"
	fwkrh "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requesthandling"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

// testBasis is a fixed, non-zero wall clock. Decay is anchored on the first
// touch of each accumulator, so the absolute value never matters -- but a zero
// time would make IsZero() checks fire.
var testBasis = time.Date(2026, 10, 4, 12, 0, 0, 0, time.UTC)

// fakeClock lets decay tests advance time instantly rather than sleeping. The
// clock is the only reason halfLifeSeconds stays a real knob: nothing else in
// the package may derive a duration from it.
type fakeClock struct{ t time.Time }

func newFakeClock() *fakeClock             { return &fakeClock{t: testBasis} }
func (c *fakeClock) now() time.Time        { return c.t }
func (c *fakeClock) advance(d time.Duration) { c.t = c.t.Add(d) }

// testConfig is two explicit groups plus a prefix group and a catch-all, which
// exercises every matching path the production config uses.
func testConfig() Config {
	cfg := DefaultConfig()
	cfg.Groups = []GroupConfig{
		{Name: "app1", Weight: 20, Match: GroupMatch{Exact: []string{"app1-production"}}},
		{Name: "app2", Weight: 10, Match: GroupMatch{Exact: []string{"app2-batch"}}},
		{Name: "end-users", Weight: 65, Match: GroupMatch{Prefix: []string{"end-user-"}}},
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "unclassified", Weight: 5}
	cfg.StateLogIntervalSeconds = 0
	return cfg
}

// twoGroupConfig is the minimal shape for the ratio tests: two groups with the
// given weights and nothing else competing.
func twoGroupConfig(weightA, weightB float64) Config {
	cfg := DefaultConfig()
	cfg.Groups = []GroupConfig{
		{Name: "a-group", Weight: weightA, Match: GroupMatch{Exact: []string{"a"}}},
		{Name: "b-group", Weight: weightB, Match: GroupMatch{Exact: []string{"b"}}},
	}
	cfg.DefaultGroup = DefaultGroupConfig{Name: "unclassified", Weight: 1}
	cfg.StateLogIntervalSeconds = 0
	return cfg
}

func newTestPlugin(t *testing.T, cfg Config) (*Plugin, *fakeClock) {
	t.Helper()
	p, err := newPlugin("test", cfg)
	require.NoError(t, err)
	clock := newFakeClock()
	p.now = clock.now
	return p, clock
}

// ---------------------------------------------------------------------------
// A band simulator
// ---------------------------------------------------------------------------

// simFlow is one tenant's queue in the simulation.
type simFlow struct {
	id       string
	depth    int
	headAt   time.Time
	promptIn int
	cached   int
	output   int
	// maxTokens, when non-zero, is sent as the client's max_tokens cap.
	maxTokens int64
	// sizeBytes drives the prompt-token estimate when provisional charging is on.
	sizeBytes int
}

// simBand wires a set of simFlows into the PriorityBandAccessor the policy sees.
// It reproduces the one property that matters most: IterateQueues visits only
// non-empty queues, which is what makes work conservation structural.
type simBand struct {
	flows []*simFlow
	state any
}

func newSimBand(p *Plugin, flows ...*simFlow) *simBand {
	return &simBand{flows: flows, state: p.NewState(context.Background())}
}

func (b *simBand) accessor() flowcontrol.PriorityBandAccessor {
	byID := make(map[string]flowcontrol.FlowQueueAccessor, len(b.flows))
	var active []flowcontrol.FlowQueueAccessor
	for _, f := range b.flows {
		q := &fwkfcmocks.MockFlowQueueAccessor{
			LenV:     f.depth,
			FlowKeyV: flowcontrol.FlowKey{ID: f.id},
		}
		if f.depth > 0 {
			q.PeekV = &fwkfcmocks.MockQueueItemAccessor{EnqueueTimeV: f.headAt}
			active = append(active, q)
		}
		byID[f.id] = q
	}
	return &fwkfcmocks.MockPriorityBandAccessor{
		PolicyStateV: b.state,
		FlowKeysFunc: func() []flowcontrol.FlowKey {
			keys := make([]flowcontrol.FlowKey, 0, len(byID))
			for id := range byID {
				keys = append(keys, flowcontrol.FlowKey{ID: id})
			}
			return keys
		},
		QueueFunc: func(id string) flowcontrol.FlowQueueAccessor { return byID[id] },
		IterateQueuesFunc: func(cb func(flowcontrol.FlowQueueAccessor) bool) {
			for _, q := range active {
				if !cb(q) {
					return
				}
			}
		},
	}
}

func (b *simBand) flow(id string) *simFlow {
	for _, f := range b.flows {
		if f.id == id {
			return f
		}
	}
	return nil
}

// request builds the InferenceRequest a dispatch from this flow would carry.
func (f *simFlow) request(seq int) *fwksched.InferenceRequest {
	body := &fwkrh.InferenceRequestBody{}
	if f.maxTokens > 0 {
		mt := f.maxTokens
		body.MaxOutputTokens = &mt
	}
	return &fwksched.InferenceRequest{
		RequestID:        f.id + "-" + time.Duration(seq).String(),
		FairnessID:       f.id,
		Body:             body,
		RequestSizeBytes: f.sizeBytes,
	}
}

// response builds the terminal usage block the model server would return.
func (f *simFlow) response() *fwkrc.Response {
	return &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseNatural,
		Usage: fwkrh.Usage{
			PromptTokens:       f.promptIn,
			CompletionTokens:   f.output,
			TotalTokens:        f.promptIn + f.output,
			PromptTokenDetails: &fwkrh.PromptTokenDetails{CachedTokens: f.cached},
		},
	}
}

// simResult records what a simulation run delivered to each group.
type simResult struct {
	picks  map[string]int
	tokens map[string]float64
	order  []string
}

func newSimResult() *simResult {
	return &simResult{picks: map[string]int{}, tokens: map[string]float64{}}
}

// run executes n dispatch cycles. Each cycle picks a winner, immediately
// completes one request from that flow, and advances the clock by step.
//
// Completing instantly is deliberate for the ratio tests: it removes in-flight
// blindness so the test measures the allocator, not the estimator. Tests 8 and
// 8b exercise the in-flight path explicitly.
func (b *simBand) run(t *testing.T, p *Plugin, n int, step time.Duration, clock *fakeClock) *simResult {
	t.Helper()
	ctx := context.Background()
	res := newSimResult()
	for i := range n {
		q, err := p.Pick(ctx, b.accessor())
		require.NoError(t, err)
		if q == nil {
			clock.advance(step)
			continue
		}
		id := q.FlowKey().ID
		f := b.flow(id)
		require.NotNil(t, f, "picked a flow the simulation does not know: %s", id)

		req := f.request(i)
		require.NoError(t, p.PreRequest(ctx, req, nil))
		p.ResponseBody(ctx, req, f.response(), nil)

		res.picks[id]++
		res.tokens[id] += p.cost(f.promptIn, f.cached, f.output)
		res.order = append(res.order, id)
		clock.advance(step)
	}
	return res
}
