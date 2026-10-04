/*
Copyright 2025 The Kubernetes Authors.
Copyright 2026 The llm-d Authors.
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

// The four table cases below are adapted from the upstream FairnessPolicy
// conformance suite at
// pkg/epp/framework/plugins/flowcontrol/fairness/functional_test.go in
// github.com/llm-d/llm-d-router.
//
// They are COPIED rather than imported because runPickConformanceTests lives in
// a _test.go file and therefore cannot cross a module boundary. Upstreaming it
// into a non-test `fairness/conformance` package would let this file shrink to
// a single call; see docs/design.md, "Worth doing upstream".
//
// Keep them in sync when re-pinning llm-d-router.

package weightedlas

import (
	"context"
	"sync"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol"
	fwkfcmocks "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol/mocks"
)

// TestFairnessPolicyConformance covers the cases a new policy gets wrong: all
// four must return (nil, nil) with no error, rather than panicking or
// manufacturing a winner out of an empty band.
func TestFairnessPolicyConformance(t *testing.T) {
	t.Parallel()

	plug, err := Factory(PluginType, nil, nil)
	require.NoError(t, err)
	require.NotNil(t, plug)

	policy, ok := plug.(flowcontrol.FairnessPolicy)
	require.True(t, ok, "the plugin must implement FairnessPolicy")
	assert.Equal(t, PluginType, policy.TypedName().Name)

	ctx := context.Background()
	state := policy.NewState(ctx)

	flowIDEmpty := "flow-empty"
	mockQueueEmpty := &fwkfcmocks.MockFlowQueueAccessor{
		LenV:     0,
		PeekV:    nil,
		FlowKeyV: flowcontrol.FlowKey{ID: flowIDEmpty},
	}

	testCases := []struct {
		name string
		band flowcontrol.PriorityBandAccessor
	}{
		{
			name: "With a nil priority band accessor",
			band: nil,
		},
		{
			name: "With an empty priority band accessor",
			band: &fwkfcmocks.MockPriorityBandAccessor{
				PolicyStateV:      state,
				FlowKeysFunc:      func() []flowcontrol.FlowKey { return []flowcontrol.FlowKey{} },
				IterateQueuesFunc: func(callback func(flow flowcontrol.FlowQueueAccessor) bool) { /* no-op */ },
			},
		},
		{
			// The eventually-consistent case: a queue may be visited and still
			// report zero. Treating it as a candidate would hand a dispatch
			// opportunity to a flow with nothing to dispatch.
			name: "With a band that has one empty queue",
			band: &fwkfcmocks.MockPriorityBandAccessor{
				PolicyStateV: state,
				FlowKeysFunc: func() []flowcontrol.FlowKey { return []flowcontrol.FlowKey{{ID: flowIDEmpty}} },
				QueueFunc: func(fID string) flowcontrol.FlowQueueAccessor {
					if fID == flowIDEmpty {
						return mockQueueEmpty
					}
					return nil
				},
				IterateQueuesFunc: func(callback func(flow flowcontrol.FlowQueueAccessor) bool) {
					callback(mockQueueEmpty)
				},
			},
		},
		{
			name: "With a band that has multiple empty queues",
			band: &fwkfcmocks.MockPriorityBandAccessor{
				PolicyStateV: state,
				FlowKeysFunc: func() []flowcontrol.FlowKey {
					return []flowcontrol.FlowKey{{ID: flowIDEmpty}, {ID: "flow-empty-2"}}
				},
				QueueFunc: func(fID string) flowcontrol.FlowQueueAccessor { return mockQueueEmpty },
				IterateQueuesFunc: func(callback func(flow flowcontrol.FlowQueueAccessor) bool) {
					if !callback(mockQueueEmpty) {
						return
					}
					callback(mockQueueEmpty)
				},
			},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			t.Parallel()
			selected, err := policy.Pick(ctx, tc.band)
			require.NoError(t, err, "Pick() should not return an error")
			assert.Nil(t, selected, "Pick() should return a nil queue")
		})
	}

	// Added beyond the upstream four: a state object of the wrong concrete type
	// must be an error, not a panic. The Flyweight contract guarantees the
	// object came from our own NewState, so this only fires on a framework bug
	// or a misconfiguration -- which is exactly when a panic is worst.
	t.Run("With a policy state of the wrong type", func(t *testing.T) {
		t.Parallel()
		band := &fwkfcmocks.MockPriorityBandAccessor{
			PolicyStateV: "not a bandState",
			IterateQueuesFunc: func(callback func(flow flowcontrol.FlowQueueAccessor) bool) {
				callback(&fwkfcmocks.MockFlowQueueAccessor{LenV: 1, FlowKeyV: flowcontrol.FlowKey{ID: "x"}})
			},
		}
		selected, err := policy.Pick(ctx, band)
		require.Error(t, err)
		assert.Nil(t, selected)
	})
}

// Conformance requires every method to be goroutine-safe. Run under -race.
func TestPickIsGoroutineSafe(t *testing.T) {
	t.Parallel()

	cfg := twoGroupConfig(2, 1)
	cfg.Enforce = true
	p, _ := newTestPlugin(t, cfg)
	// The real clock, not the fake one: concurrent access to fakeClock would
	// itself be a data race and would mask the thing under test.
	p.now = time.Now

	band := newSimBand(p,
		&simFlow{id: "a-group", depth: 100, promptIn: 100, output: 10},
		&simFlow{id: "b-group", depth: 100, promptIn: 100, output: 10},
	)
	accessor := band.accessor()

	ctx := context.Background()
	var wg sync.WaitGroup
	for range 50 {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for range 100 {
				q, err := p.Pick(ctx, accessor)
				assert.NoError(t, err)
				assert.NotNil(t, q)
			}
		}()
	}
	wg.Wait()
}
