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
	"testing"

	"github.com/stretchr/testify/assert"

	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

// failGen returns a generator that fails the test if called, for assertions
// that a fallback id must not be minted when a real one is available.
func failGen(t *testing.T) func() string {
	t.Helper()
	return func() string {
		t.Fatal("generateFallbackID called when a request id was already available")
		return ""
	}
}

func TestResolveCorrelationCapturesXRequestIDHeader(t *testing.T) {
	t.Parallel()
	req := &fwksched.InferenceRequest{Headers: map[string]string{"x-request-id": "abc-123"}}
	c := resolveCorrelation(req, testBasis, failGen(t))
	assert.Equal(t, "abc-123", c.requestID)
}

func TestResolveCorrelationHeaderLookupIsCaseInsensitive(t *testing.T) {
	t.Parallel()
	req := &fwksched.InferenceRequest{Headers: map[string]string{"X-Request-ID": "abc-123"}}
	c := resolveCorrelation(req, testBasis, failGen(t))
	assert.Equal(t, "abc-123", c.requestID,
		"a test or future parser that does not lowercase headers must still resolve")
}

// A client that sends x-request-id must win over whatever InferenceRequest.RequestID
// upstream populated -- this plugin's own extraction should not depend on
// upstream's, even though in practice the two already agree.
func TestResolveCorrelationHeaderWinsOverUpstreamRequestID(t *testing.T) {
	t.Parallel()
	req := &fwksched.InferenceRequest{
		RequestID: "upstream-value",
		Headers:   map[string]string{"x-request-id": "header-value"},
	}
	c := resolveCorrelation(req, testBasis, failGen(t))
	assert.Equal(t, "header-value", c.requestID)
}

// The upstream llm-d-router ext_proc server already extracts x-request-id (and
// generates one if absent) into InferenceRequest.RequestID. When the header is
// for some reason not present on request.Headers but RequestID is, reuse it
// rather than minting a second, different fallback.
func TestResolveCorrelationFallsBackToUpstreamRequestID(t *testing.T) {
	t.Parallel()
	req := &fwksched.InferenceRequest{RequestID: "upstream-generated-id"}
	c := resolveCorrelation(req, testBasis, failGen(t))
	assert.Equal(t, "upstream-generated-id", c.requestID)
}

// Done-when criterion: the id falls back to a generated one when the header
// (and any upstream-populated RequestID) is absent, rather than dropping the
// field.
func TestResolveCorrelationGeneratesFallbackWhenAbsentEverywhere(t *testing.T) {
	t.Parallel()
	req := &fwksched.InferenceRequest{}
	c := resolveCorrelation(req, testBasis, func() string { return "generated-xyz" })
	assert.Equal(t, "generated-xyz", c.requestID)
	assert.NotEmpty(t, c.requestID)
}

func TestResolveCorrelationExtractsTraceIDFromTraceparent(t *testing.T) {
	t.Parallel()
	req := &fwksched.InferenceRequest{Headers: map[string]string{
		"x-request-id": "req-1",
		"traceparent":  "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
	}}
	c := resolveCorrelation(req, testBasis, failGen(t))
	assert.Equal(t, "4bf92f3577b34da6a3ce929d0e0e4736", c.traceID)
}

// The ticket is explicit: do not generate a trace id if traceparent is absent.
func TestResolveCorrelationDoesNotGenerateTraceID(t *testing.T) {
	t.Parallel()
	req := &fwksched.InferenceRequest{}
	c := resolveCorrelation(req, testBasis, func() string { return "generated" })
	assert.Empty(t, c.traceID)
}

func TestResolveCorrelationIgnoresMalformedTraceparent(t *testing.T) {
	t.Parallel()
	cases := map[string]string{
		"wrong shape":       "not-a-traceparent",
		"short trace id":    "00-deadbeef-00f067aa0ba902b7-01",
		"non-hex trace id":  "00-zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz-00f067aa0ba902b7-01",
		"all-zero trace id": "00-00000000000000000000000000000000-00f067aa0ba902b7-01",
	}
	for name, tp := range cases {
		t.Run(name, func(t *testing.T) {
			t.Parallel()
			req := &fwksched.InferenceRequest{Headers: map[string]string{
				"x-request-id": "req-1",
				"traceparent":  tp,
			}}
			c := resolveCorrelation(req, testBasis, failGen(t))
			assert.Empty(t, c.traceID)
		})
	}
}

func TestGenerateFallbackIDNeverEmpty(t *testing.T) {
	t.Parallel()
	seen := make(map[string]bool)
	for range 100 {
		id := generateFallbackID()
		assert.NotEmpty(t, id)
		assert.False(t, seen[id], "fallback ids must not collide")
		seen[id] = true
	}
}
