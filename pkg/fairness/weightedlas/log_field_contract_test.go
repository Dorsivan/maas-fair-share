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

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	fwkrc "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requestcontrol"
	fwkrh "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requesthandling"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

// Done-when (field contract): `band` and `enforcing` belong to the stable key
// set docs/log-field-contract.md defines for every line this plugin emits,
// not only the ones UNI-53 already covered with a correlation id. `band` is
// read straight off the request's own InferenceRequest.Objectives.Priority --
// not a hardcoded 0 -- so a non-default value here proves it threads through
// rather than being coincidentally right at the POC's single-band default.
func TestUnmatchedSubscriptionLogCarriesBandAndEnforcing(t *testing.T) {
	t.Parallel()
	cfg := testConfig()
	cfg.Enforce = true
	p, _ := newTestPlugin(t, cfg)
	ctx, lines := capturingContext()

	req := &fwksched.InferenceRequest{
		Objectives: fwksched.RequestObjectives{Priority: 7},
		Headers: map[string]string{
			"x-request-id":        "req-band-1",
			"x-maas-subscription": "totally-unknown-subscription",
		},
	}
	require.NoError(t, p.RequestHeader(ctx, req))

	line, ok := findLine(*lines, "subscription matched no fairness group")
	require.True(t, ok, "expected an unmatched-subscription log line, got: %v", *lines)
	assert.Equal(t, float64(7), logFieldNumber(t, line, "band"))
	assert.True(t, logFieldBool(t, line, "enforcing"))
}

func TestNoUsageBlockLogCarriesBandAndEnforcing(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(1, 1)
	cfg.Enforce = true
	p, _ := newTestPlugin(t, cfg)
	ctx, lines := capturingContext()

	req := &fwksched.InferenceRequest{
		Objectives: fwksched.RequestObjectives{Priority: 3},
		FairnessID: "a-group",
		Headers:    map[string]string{"x-request-id": "req-band-2"},
	}
	require.NoError(t, p.RequestHeader(ctx, req))
	require.NoError(t, p.PreRequest(ctx, req, nil))

	resp := &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseNatural,
	}
	p.ResponseBody(ctx, req, resp, nil)

	line, ok := findLine(*lines, "no usage block")
	require.True(t, ok, "expected a no-usage-block log line, got: %v", *lines)
	assert.Equal(t, float64(3), logFieldNumber(t, line, "band"))
	assert.True(t, logFieldBool(t, line, "enforcing"))
}

// Done-when (the board's headline query): a V(4) per-request line must carry
// `band`, `enforcing`, and `recorderTick` -- the last flight-recorder tick
// completed as of this request's settlement -- so "given a request id off a
// response header, return its whole story" can jump from this line straight
// to the matching "fairness state" tick in docs/logql-queries.md.
func TestV4TierLineCarriesBandEnforcingAndRecorderTick(t *testing.T) {
	t.Parallel()
	cfg := v4Config(1, 3600)
	cfg.Enforce = true
	p, clock := newTestPlugin(t, cfg)
	ctx, lines := capturingContextV(4)

	// Advance the recorder by one tick before the request settles, so
	// recorderTick has a non-zero value to assert against.
	p.lastContendedUnixNano.Store(clock.now().UnixNano())
	p.logFlightRecorderTick(context.Background())

	req := &fwksched.InferenceRequest{
		Objectives: fwksched.RequestObjectives{Priority: 2},
		Headers: map[string]string{
			"x-request-id":        "req-recorder-tick",
			"x-maas-subscription": "a",
		},
	}
	require.NoError(t, p.RequestHeader(ctx, req))
	require.NoError(t, p.PreRequest(ctx, req, nil))
	resp := &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseNatural,
		Usage: fwkrh.Usage{
			PromptTokens:     100,
			CompletionTokens: 50,
		},
	}
	p.ResponseBody(ctx, req, resp, nil)

	line, ok := findLine(*lines, "per-request fairness tier")
	require.True(t, ok, "expected a V(4) tier line, got: %v", *lines)
	assert.Equal(t, float64(2), logFieldNumber(t, line, "band"))
	assert.True(t, logFieldBool(t, line, "enforcing"))
	assert.Equal(t, float64(1), logFieldNumber(t, line, "recorderTick"),
		"recorderTick must reflect the most recently completed flight-recorder tick")
}
