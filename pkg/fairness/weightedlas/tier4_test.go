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
	"strings"
	"testing"
	"time"

	"github.com/go-logr/logr/funcr"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"sigs.k8s.io/controller-runtime/pkg/log"

	fwkrc "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requestcontrol"
	fwkrh "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requesthandling"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

// capturingContextV is capturingContext (attribution_test.go) generalised to
// an arbitrary verbosity, so these tests can exercise the V(4) tier's gate on
// the process's own verbosity flag directly rather than only on this
// plugin's config.
func capturingContextV(verbosity int) (context.Context, *[]string) {
	var lines []string
	logger := funcr.NewJSON(func(obj string) { lines = append(lines, obj) }, funcr.Options{Verbosity: verbosity})
	return log.IntoContext(context.Background(), logger), &lines
}

// v4Config is twoGroupConfig plus the V(4) tier enabled at the given sample
// rate and time box.
func v4Config(sampleEvery uint64, timeBoxSeconds float64) Config {
	cfg := twoGroupConfig(1, 1)
	cfg.RequestTierV4SampleEvery = sampleEvery
	cfg.RequestTierV4TimeBoxSeconds = timeBoxSeconds
	return cfg
}

// runSettledRequest drives one request through the full classify -> dispatch
// -> settle lifecycle, ending in the branch that has a group, an estimate and
// a true-up delta to report -- the one place the V(4) tier can fire from.
func runSettledRequest(t *testing.T, p *Plugin, ctx context.Context, reqID string) {
	t.Helper()
	req := &fwksched.InferenceRequest{
		Headers: map[string]string{
			"x-request-id":        reqID,
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
}

// Done-when: "off by default emits nothing."
func TestV4TierOffByDefaultEmitsNothing(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, twoGroupConfig(1, 1)) // RequestTierV4SampleEvery is the zero value
	ctx, lines := capturingContextV(4)

	for i := range 10 {
		runSettledRequest(t, p, ctx, "req-default-"+time.Duration(i).String())
	}

	_, found := findLine(*lines, "per-request fairness tier")
	assert.False(t, found, "V(4) tier must not emit with RequestTierV4SampleEvery unset, got: %v", *lines)
}

// Done-when: "off by default" also holds when the tier is configured but the
// process verbosity does not actually reach V(4) -- the fallback the ticket
// calls for when the plugin's own config has no live-reload path.
func TestV4TierGatedOnProcessVerbosity(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, v4Config(1, 3600))
	ctx, lines := capturingContextV(1) // same as every other test in this package: V(1) only

	for i := range 5 {
		runSettledRequest(t, p, ctx, "req-lowv-"+time.Duration(i).String())
	}

	_, found := findLine(*lines, "per-request fairness tier")
	assert.False(t, found, "V(4) tier must stay silent below V(4) process verbosity, got: %v", *lines)
}

// Done-when: "the sample rate is honoured."
func TestV4TierSampleRateHonoured(t *testing.T) {
	t.Parallel()
	const sampleEvery = 3
	p, _ := newTestPlugin(t, v4Config(sampleEvery, 3600))
	ctx, lines := capturingContextV(4)

	const requests = 9
	for i := range requests {
		runSettledRequest(t, p, ctx, "req-sample-"+time.Duration(i).String())
	}

	var tierLines int
	for _, l := range *lines {
		if strings.Contains(l, "per-request fairness tier") {
			tierLines++
		}
	}
	assert.Equal(t, requests/sampleEvery, tierLines,
		"expected exactly 1-in-%d of %d requests sampled, got lines: %v", sampleEvery, requests, *lines)
}

// Done-when: "the time box disables emission."
func TestV4TierTimeBoxDisablesEmission(t *testing.T) {
	t.Parallel()
	const timeBoxSeconds = 10
	p, clock := newTestPlugin(t, v4Config(1, timeBoxSeconds)) // sample every request
	ctx, lines := capturingContextV(4)

	runSettledRequest(t, p, ctx, "req-before-box-1")
	runSettledRequest(t, p, ctx, "req-before-box-2")
	before := len(*lines)
	assert.Equal(t, 2, before, "expected both pre-deadline requests to emit, got: %v", *lines)

	clock.advance((timeBoxSeconds + 1) * time.Second)
	runSettledRequest(t, p, ctx, "req-after-box-1")
	runSettledRequest(t, p, ctx, "req-after-box-2")

	assert.Len(t, *lines, before, "expected no further V(4) lines once the time box elapses, got: %v", *lines)
}

// The join key the board asked for: every V(4) line must carry the
// correlation id, exactly like every other request-scoped line in this
// package.
func TestV4TierLineCarriesCorrelationIDAndFields(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, v4Config(1, 3600))
	ctx, lines := capturingContextV(4)

	runSettledRequest(t, p, ctx, "req-fields-1")

	line, ok := findLine(*lines, "per-request fairness tier")
	require.True(t, ok, "expected a V(4) tier line, got: %v", *lines)
	assert.Equal(t, "req-fields-1", logFieldString(t, line, "requestID"))
	assert.Equal(t, "a-group", logFieldString(t, line, "group"))
	assert.Contains(t, line, `"estimateCharged"`)
	assert.Contains(t, line, `"trueUpDelta"`)
	// Never the raw, client-controlled subscription string -- see
	// docs/design.md's cardinality warning on unmatched_subscriptions_total,
	// which applies equally here.
	assert.NotContains(t, line, `"a"`, "must not label by the raw subscription string")
}

// Validation: the time box is required once sampling is turned on, so the
// tier can never be configured to run forever.
func TestV4TierRequiresTimeBoxWhenSampling(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(1, 1)
	cfg.RequestTierV4SampleEvery = 1
	cfg.RequestTierV4TimeBoxSeconds = 0
	require.Error(t, cfg.validate())
}
