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
	"strings"
	"testing"
	"time"

	"github.com/go-logr/logr/funcr"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"sigs.k8s.io/controller-runtime/pkg/log"

	fwkrc "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requestcontrol"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

// capturingContext returns a context whose logger renders each call as one
// JSON object, collected into the returned slice -- the same shape the EPP's
// real `--zap-encoder json` produces, so these tests assert on exactly what a
// `grep '"requestID":"..."'` against the live log would find. Verbosity: 1
// admits this plugin's V(1) line as well as its default-level ones.
func capturingContext() (context.Context, *[]string) {
	var lines []string
	logger := funcr.NewJSON(func(obj string) { lines = append(lines, obj) }, funcr.Options{Verbosity: 1})
	return log.IntoContext(context.Background(), logger), &lines
}

func logFieldString(t *testing.T, line, key string) string {
	t.Helper()
	var obj map[string]any
	require.NoError(t, json.Unmarshal([]byte(line), &obj))
	v, ok := obj[key]
	require.True(t, ok, "field %q not present in log line: %s", key, line)
	s, ok := v.(string)
	require.True(t, ok, "field %q is not a string in log line: %s", key, line)
	return s
}

func findLine(lines []string, substr string) (string, bool) {
	for _, l := range lines {
		if strings.Contains(l, substr) {
			return l, true
		}
	}
	return "", false
}

// Done-when: "Unit tests show the id is captured from x-request-id ... and
// appears on every request-scoped line." This covers the unmatched-subscription
// line, which previously carried no correlation key at all.
func TestUnmatchedSubscriptionLogCarriesRequestID(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, testConfig())
	ctx, lines := capturingContext()

	req := &fwksched.InferenceRequest{
		Headers: map[string]string{
			"x-request-id":           "req-unmatched-1",
			"x-maas-subscription-id": "totally-unknown-subscription",
		},
	}
	require.NoError(t, p.RequestHeader(ctx, req))

	line, ok := findLine(*lines, "subscription matched no fairness group")
	require.True(t, ok, "expected an unmatched-subscription log line, got: %v", *lines)
	assert.Equal(t, "req-unmatched-1", logFieldString(t, line, "requestID"))
}

// Done-when: falls back when x-request-id is absent, rather than dropping the
// field -- a line with no key is a line nobody can find.
func TestUnmatchedSubscriptionLogFallsBackWhenHeaderAbsent(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, testConfig())
	p.genID = func() string { return "fallback-id-42" }
	ctx, lines := capturingContext()

	req := &fwksched.InferenceRequest{
		Headers: map[string]string{"x-maas-subscription-id": "another-unknown-one"},
	}
	require.NoError(t, p.RequestHeader(ctx, req))

	line, ok := findLine(*lines, "subscription matched no fairness group")
	require.True(t, ok)
	assert.Equal(t, "fallback-id-42", logFieldString(t, line, "requestID"))
}

// The pre-existing no-usage-block warning (ResponseBody) must carry the same
// correlation id RequestHeader resolved, not response.RequestID directly --
// so every request-scoped line agrees even if the two ever diverge.
func TestNoUsageBlockLogCarriesRequestID(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, twoGroupConfig(1, 1))
	ctx, lines := capturingContext()

	req := &fwksched.InferenceRequest{
		FairnessID: "a-group",
		Headers:    map[string]string{"x-request-id": "req-no-usage"},
	}
	require.NoError(t, p.RequestHeader(ctx, req))
	require.NoError(t, p.PreRequest(ctx, req, nil))

	resp := &fwkrc.Response{
		EndOfStream:      true,
		TerminationCause: fwkrc.TerminationCauseNatural,
		// No Usage block set.
	}
	p.ResponseBody(ctx, req, resp, nil)

	line, ok := findLine(*lines, "no usage block")
	require.True(t, ok, "expected a no-usage-block log line, got: %v", *lines)
	assert.Equal(t, "req-no-usage", logFieldString(t, line, "requestID"))
}

func TestUnmatchedSubscriptionLogCarriesTraceIDWhenPresent(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, testConfig())
	ctx, lines := capturingContext()

	req := &fwksched.InferenceRequest{
		Headers: map[string]string{
			"x-request-id":           "req-traced",
			"traceparent":            "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
			"x-maas-subscription-id": "yet-another-unknown",
		},
	}
	require.NoError(t, p.RequestHeader(ctx, req))

	line, ok := findLine(*lines, "subscription matched no fairness group")
	require.True(t, ok)
	assert.Equal(t, "4bf92f3577b34da6a3ce929d0e0e4736", logFieldString(t, line, "traceId"))
}

// ---------------------------------------------------------------------------
// Response headers -- D6
// ---------------------------------------------------------------------------

func TestResponseHeaderSurfacesGroupQueueMsAndRequestID(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(1, 1)
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()

	req := &fwksched.InferenceRequest{Headers: map[string]string{
		"x-request-id":           "req-headers-1",
		"x-maas-subscription-id": "a",
	}}
	require.NoError(t, p.RequestHeader(ctx, req))
	require.Equal(t, "a-group", req.FairnessID)

	// Give PreRequest something measurable to report as queue time.
	clock.advance(37 * time.Millisecond)
	require.NoError(t, p.PreRequest(ctx, req, nil))

	resp := &fwkrc.Response{}
	p.ResponseHeader(ctx, req, resp, nil)

	assert.Equal(t, "req-headers-1", resp.Headers[requestIDHeader])
	assert.Equal(t, req.FairnessID, resp.Headers[fairnessGroupHeader])
	assert.Equal(t, "37.0", resp.Headers[fairnessQueueMsHeader])
}

func TestResponseHeaderSuppressedByConfig(t *testing.T) {
	t.Parallel()
	cfg := twoGroupConfig(1, 1)
	cfg.EmitAttributionHeaders = false
	p, _ := newTestPlugin(t, cfg)
	ctx := context.Background()

	req := &fwksched.InferenceRequest{Headers: map[string]string{"x-request-id": "req-suppressed"}}
	require.NoError(t, p.RequestHeader(ctx, req))
	require.NoError(t, p.PreRequest(ctx, req, nil))

	resp := &fwkrc.Response{}
	p.ResponseHeader(ctx, req, resp, nil)

	assert.Empty(t, resp.Headers, "EmitAttributionHeaders: false must suppress every attribution header")
}

func TestResponseHeaderRequestIDMatchesLogLine(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, testConfig())
	ctx, lines := capturingContext()

	req := &fwksched.InferenceRequest{
		Headers: map[string]string{
			"x-request-id":           "req-end-to-end",
			"x-maas-subscription-id": "an-unmatched-id",
		},
	}
	require.NoError(t, p.RequestHeader(ctx, req))
	require.NoError(t, p.PreRequest(ctx, req, nil))

	resp := &fwkrc.Response{}
	p.ResponseHeader(ctx, req, resp, nil)

	line, ok := findLine(*lines, "subscription matched no fairness group")
	require.True(t, ok)
	assert.Equal(t, resp.Headers[requestIDHeader], logFieldString(t, line, "requestID"),
		"the id in the response header must match the id in the EPP's own log line")
}

// Defence in depth: ResponseHeader must still emit a well-formed id even if
// RequestHeader never ran for this request (e.g. a future ordering change),
// rather than sending an empty x-request-id.
func TestResponseHeaderWithoutPrecedingRequestHeaderStillEmitsID(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, testConfig())
	p.genID = func() string { return "late-fallback-id" }
	ctx := context.Background()

	req := &fwksched.InferenceRequest{FairnessID: "unclassified"}
	resp := &fwkrc.Response{}
	p.ResponseHeader(ctx, req, resp, nil)

	assert.Equal(t, "late-fallback-id", resp.Headers[requestIDHeader])
	assert.Equal(t, "unclassified", resp.Headers[fairnessGroupHeader])
	_, haveQueueMs := resp.Headers[fairnessQueueMsHeader]
	assert.False(t, haveQueueMs, "queue-ms has no meaning without a PreRequest dispatch to measure to")
}
