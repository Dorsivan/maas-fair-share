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
	"math"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	fwkrc "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requestcontrol"
	fwkrh "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requesthandling"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

// UNI-293 item 1: the undecayed completion true-up.

// settle dispatches one request for a-group, holds it for inflight, and
// completes it with the given usage.
func settle(t *testing.T, p *Plugin, clock *fakeClock, maxTokens int64, inflight time.Duration, prompt, completion int) {
	t.Helper()
	ctx := context.Background()
	mt := maxTokens
	req := &fwksched.InferenceRequest{
		FairnessID:       "a-group",
		RequestSizeBytes: prompt * 4,
		Body:             &fwkrh.InferenceRequestBody{MaxOutputTokens: &mt},
	}
	require.NoError(t, p.PreRequest(ctx, req, nil))
	clock.advance(inflight)
	p.ResponseBody(ctx, req, &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseNatural,
		Usage:            fwkrh.Usage{PromptTokens: prompt, CompletionTokens: completion, TotalTokens: prompt + completion},
	}, nil)
}

// The gaming vector from UNI-283, on the tab: tight-max_tokens short requests
// warm the output EWMA to ~4 tokens, so a long request is estimated at 4 and
// generates 1024. Decayed, two half-lives in flight leave a quarter of the
// correction. Undecayed, the real cost lands in full.
func TestUndecayedTrueUpClosesTheTightMaxTokensVector(t *testing.T) {
	t.Parallel()
	const (
		halfLife = 60.0
		inflight = 120 * time.Second
		prompt   = 100
		long     = 1024
	)
	longTab := func(undecayed bool) (got, est, actual float64) {
		cfg := twoGroupConfig(1, 1)
		cfg.HalfLifeSeconds = halfLife
		cfg.UndecayedTrueUp = undecayed
		p, clock := newTestPlugin(t, cfg)
		for i := 0; i < ewmaWarmupSamples; i++ {
			settle(t, p, clock, 4, 0, prompt, 4)
		}
		gs := p.states["a-group"]
		ewma, warm := gs.outputEWMA()
		require.True(t, warm)
		require.InDelta(t, 4, ewma, 1e-9, "the shorts must have dragged the estimate down")
		// Park the warm-up tab far in the past so only the long request is left.
		clock.advance(time.Hour)
		before := gs.normalizedService(clock.now())
		settle(t, p, clock, 1024, inflight, prompt, long)
		return gs.normalizedService(clock.now()) - before*math.Exp2(-inflight.Seconds()/halfLife),
			p.cost(prompt, 0, 4), p.cost(prompt, 0, long)
	}

	decayed, est, actual := longTab(false)
	assert.InDelta(t, actual*0.25, decayed, 1e-6, "decayed: the long request is charged a quarter of its cost")

	full, _, _ := longTab(true)
	assert.InDelta(t, est*0.25+(actual-est), full, 1e-6,
		"undecayed: the under-estimate lands at full weight on completion")
}

// Over-estimates must not refund more than what is left of the hold, flag or
// no flag: a full-weight refund would cancel charges that belong to other
// requests.
func TestUndecayedTrueUpRefundsOverestimatesDecayed(t *testing.T) {
	t.Parallel()
	tab := func(undecayed bool) float64 {
		cfg := twoGroupConfig(1, 1)
		cfg.HalfLifeSeconds = 60
		cfg.UndecayedTrueUp = undecayed
		p, clock := newTestPlugin(t, cfg)
		// 80000 bytes / 4 = 20000-token prompt estimate against a real 2000.
		ctx := context.Background()
		mt := int64(5000)
		req := &fwksched.InferenceRequest{FairnessID: "a-group", RequestSizeBytes: 80000,
			Body: &fwkrh.InferenceRequestBody{MaxOutputTokens: &mt}}
		require.NoError(t, p.PreRequest(ctx, req, nil))
		clock.advance(60 * time.Second)
		p.ResponseBody(ctx, req, &fwkrc.Response{EndOfStream: true, TerminationCause: fwkrc.TerminationCauseNatural,
			Usage: fwkrh.Usage{PromptTokens: 2000, CompletionTokens: 500, TotalTokens: 2500}}, nil)
		return p.states["a-group"].normalizedService(clock.now())
	}
	off, on := tab(false), tab(true)
	assert.InDelta(t, off, on, 1e-9)
	p, _ := newTestPlugin(t, twoGroupConfig(1, 1))
	assert.InDelta(t, p.cost(2000, 0, 500)*0.5, on, 1e-6)
}

// Default off: an empty parameters block must keep today's decayed true-up.
func TestUndecayedTrueUpDefaultsOff(t *testing.T) {
	t.Parallel()
	assert.False(t, DefaultConfig().UndecayedTrueUp)
}
