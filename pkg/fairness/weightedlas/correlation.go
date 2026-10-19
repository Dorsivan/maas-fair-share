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
	"crypto/rand"
	"encoding/hex"
	"strings"
	"time"

	fwkplugin "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/plugin"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

// Header names this plugin reads for correlation and writes back for
// attribution. See docs/design.md "Per-request attribution".
const (
	requestIDHeader       = "x-request-id"
	traceparentHeader     = "traceparent"
	fairnessGroupHeader   = "x-maas-fairness-group"
	fairnessQueueMsHeader = "x-maas-fairness-queue-ms"
)

// correlationKey holds the correlation{} attribute RequestHeader resolves once
// per request. Every later hook (PreRequest, ResponseBody, ResponseHeader)
// reads it back rather than re-deriving it, so one id is used end to end even
// in the fallback-generation case.
var correlationKey = fwkplugin.NewDataKey("correlation", PluginType)

// correlation is the identifying information carried on every request-scoped
// log line this plugin emits and surfaced back to the caller on the response.
type correlation struct {
	// requestID is x-request-id from the inbound request, the upstream
	// framework's own already-resolved InferenceRequest.RequestID, or a
	// generated fallback -- in that preference order. Never empty: a
	// request-scoped line with no key is a line nobody can find.
	requestID string
	// traceID is the trace-id field of an inbound traceparent header, or empty
	// if the header was absent or malformed. Never generated -- a fabricated
	// trace id would not correlate with anything.
	traceID string
	// arrivedAt is when RequestHeader resolved this correlation, used to
	// compute queueMs once the request is dispatched.
	arrivedAt time.Time
	// queueMs is the elapsed time between RequestHeader and PreRequest --
	// classification to dispatch. Set by recordQueueWait; haveQueueMs is false
	// until then (e.g. a request rejected by admission never reaches PreRequest).
	queueMs     float64
	haveQueueMs bool
}

// logFields renders the correlation as structured log key-values, appended
// after whatever the caller already built. traceId is included only when
// present, so an idle cluster's logs are not padded with an empty field on
// every line.
func (c correlation) logFields() []any {
	fields := []any{"requestID", c.requestID}
	if c.traceID != "" {
		fields = append(fields, "traceId", c.traceID)
	}
	return fields
}

// resolveCorrelation extracts the request id and trace id from the inbound
// request headers. It is a pure function of its inputs so it can be unit
// tested without standing up the director/server chain that normally
// populates request.Headers and request.RequestID.
//
// genID supplies the fallback request id when x-request-id is absent and the
// framework has not already backfilled one either; tests inject a
// deterministic one.
func resolveCorrelation(request *fwksched.InferenceRequest, now time.Time, genID func() string) correlation {
	c := correlation{arrivedAt: now}
	if id, ok := lookupHeader(request.Headers, requestIDHeader); ok && id != "" {
		c.requestID = id
	} else if request.RequestID != "" {
		// The llm-d-router ext_proc server already extracts x-request-id and
		// backfills a generated uuid into the header if the client sent none
		// (pkg/epp/handlers/server.go) -- reuse that value before minting a
		// second, different fallback of our own.
		c.requestID = request.RequestID
	} else {
		c.requestID = genID()
	}
	if tp, ok := lookupHeader(request.Headers, traceparentHeader); ok {
		c.traceID = traceIDFromTraceparent(tp)
	}
	return c
}

// lookupHeader looks up key case-insensitively. Production headers arrive
// pre-lowercased from the framework; the scan covers a test or future parser
// that does not lowercase them, matching the tolerance subscriptionID already
// applies to the identity header.
func lookupHeader(headers map[string]string, key string) (string, bool) {
	if headers == nil {
		return "", false
	}
	if v, ok := headers[key]; ok {
		return strings.TrimSpace(v), true
	}
	for k, v := range headers {
		if strings.EqualFold(k, key) {
			return strings.TrimSpace(v), true
		}
	}
	return "", false
}

// traceIDFromTraceparent extracts the trace-id field from a W3C traceparent
// header ("version-traceid-parentid-flags"). It returns "" for anything that
// does not parse as one, including the all-zero trace id the spec reserves as
// invalid -- a malformed value is not a trace id, and this plugin does not
// generate one to replace it.
func traceIDFromTraceparent(v string) string {
	parts := strings.Split(strings.TrimSpace(v), "-")
	if len(parts) != 4 || len(parts[1]) != 32 || !isLowerHex(parts[1]) {
		return ""
	}
	if parts[1] == "00000000000000000000000000000000" {
		return ""
	}
	return parts[1]
}

func isLowerHex(s string) bool {
	for _, r := range s {
		if !((r >= '0' && r <= '9') || (r >= 'a' && r <= 'f')) {
			return false
		}
	}
	return true
}

// generateFallbackID mints a correlation id for a request that arrived with
// neither an x-request-id header nor an upstream-populated
// InferenceRequest.RequestID. The "generated-" prefix marks it as synthetic in
// logs, distinguishing it from an id Envoy actually assigned.
func generateFallbackID() string {
	var b [16]byte
	if _, err := rand.Read(b[:]); err != nil {
		// crypto/rand failing is system entropy exhaustion, not something this
		// plugin can recover from -- a fixed marker still beats an empty field.
		return "generated-unavailable"
	}
	return "generated-" + hex.EncodeToString(b[:])
}
