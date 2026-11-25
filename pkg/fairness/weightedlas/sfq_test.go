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
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"math"
	"math/rand"
	"regexp"
	"strconv"
	"strings"
	"testing"
	"time"

	"github.com/prometheus/client_golang/prometheus/testutil"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"k8s.io/apimachinery/pkg/types"

	fwkdl "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/datalayer"
	fwkrc "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requestcontrol"
	fwkrh "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requesthandling"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

// UNI-293 items 2-4: the SFQ start tag, endpoint-min V, the stamp and its
// three non-negotiables.

func sfqConfig() Config {
	cfg := twoGroupConfig(2, 1)
	cfg.SFQPriorityStamp = true
	return cfg
}

// sfqRequest is a chat request whose body is a real PayloadMap, so the stamp
// lands where the director's repackage would marshal it from.
func sfqRequest(group string, payload fwkrh.PayloadMap, maxTokens int64) *fwksched.InferenceRequest {
	if payload == nil {
		payload = fwkrh.PayloadMap{"model": "m", "messages": []any{}}
	}
	body := &fwkrh.InferenceRequestBody{Payload: payload}
	if maxTokens > 0 {
		mt := maxTokens
		body.MaxOutputTokens = &mt
	}
	return &fwksched.InferenceRequest{FairnessID: group, RequestSizeBytes: 400, Body: body}
}

func onEndpoint(name string) *fwksched.SchedulingResult {
	ep := fwksched.NewEndpoint(&fwkdl.EndpointMetadata{ID: types.NamespacedName{Namespace: "ns", Name: name}}, nil, nil)
	return &fwksched.SchedulingResult{
		PrimaryProfileName: "default",
		ProfileResults:     map[string]*fwksched.ProfileRunResult{"default": {TargetEndpoints: []fwksched.Endpoint{ep}}},
	}
}

func complete(p *Plugin, req *fwksched.InferenceRequest, prompt, completion int) {
	p.ResponseBody(context.Background(), req, &fwkrc.Response{
		EndOfStream: true, TerminationCause: fwkrc.TerminationCauseNatural,
		Usage: fwkrh.Usage{PromptTokens: prompt, CompletionTokens: completion, TotalTokens: prompt + completion},
	}, nil)
}

func firstByte(p *Plugin, req *fwksched.InferenceRequest) {
	p.ResponseBody(context.Background(), req, &fwkrc.Response{}, nil)
}

func stamped(t *testing.T, req *fwksched.InferenceRequest) int64 {
	t.Helper()
	v, ok := req.Body.Payload.(fwkrh.PayloadMap)["priority"]
	require.True(t, ok, "priority must be stamped")
	n, ok := v.(int64)
	require.True(t, ok, "priority must be an int64, got %T", v)
	return n
}

// ---------------------------------------------------------------------------
// Non-negotiable 1: the field is always ours
// ---------------------------------------------------------------------------

func TestClientPriorityIsOverwrittenOnEveryPath(t *testing.T) {
	t.Parallel()
	for _, c := range []struct {
		name  string
		cfg   func(*Config)
		group string
	}{
		{"default path", func(*Config) {}, "a-group"},
		{"provisional charging off", func(c *Config) { c.ProvisionalCharge = false }, "a-group"},
		{"unknown group folds into catch-all", func(*Config) {}, "not-a-configured-group"},
		{"empty fairness id", func(*Config) {}, ""},
		{"shadow and enforcing alike", func(c *Config) { c.Enforce = true }, "b-group"},
	} {
		t.Run(c.name, func(t *testing.T) {
			cfg := sfqConfig()
			c.cfg(&cfg)
			p, _ := newTestPlugin(t, cfg)
			req := sfqRequest(c.group, fwkrh.PayloadMap{"model": "m", "priority": -1000000}, 64)
			require.NoError(t, p.PreRequest(context.Background(), req, onEndpoint("e0")))
			assert.GreaterOrEqual(t, stamped(t, req), int64(0), "a client's -1e6 must never survive")
			assert.True(t, req.Body.Mutated, "repackage only re-marshals a Mutated body")
		})
	}
}

func TestClientPriorityIsStrippedWhenStampIsOff(t *testing.T) {
	t.Parallel()
	// Its own group name: the counter is process-global and other parallel
	// tests send client priorities as a-group.
	cfg := DefaultConfig()
	cfg.Groups = []GroupConfig{{Name: "strip-only", Weight: 1, Match: GroupMatch{Exact: []string{"s"}}}}
	cfg.StateLogIntervalSeconds = 0
	p, _ := newTestPlugin(t, cfg)
	before := testutil.ToFloat64(clientPriorityOverwritten.WithLabelValues("strip-only"))
	req := sfqRequest("strip-only", fwkrh.PayloadMap{"model": "m", "priority": -5}, 64)
	require.NoError(t, p.PreRequest(context.Background(), req, nil))
	_, has := req.Body.Payload.(fwkrh.PayloadMap)["priority"]
	assert.False(t, has, "with the stamp off a client priority is deleted, not forwarded")
	assert.True(t, req.Body.Mutated)
	assert.Equal(t, before+1, testutil.ToFloat64(clientPriorityOverwritten.WithLabelValues("strip-only")))

	// A body with no priority is left byte-identical: no re-marshal.
	clean := sfqRequest("strip-only", nil, 64)
	require.NoError(t, p.PreRequest(context.Background(), clean, nil))
	assert.False(t, clean.Body.Mutated)
}

func TestUnstampableBodyIsRejectedNotForwarded(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, sfqConfig())
	for name, payload := range map[string]fwkrh.RequestPayload{
		"raw bytes":   fwkrh.RawPayload(`{"priority":-1000000}`),
		"no payload":  nil,
		"proto (nil)": fwkrh.PayloadProto{},
	} {
		req := &fwksched.InferenceRequest{FairnessID: "a-group", Body: &fwkrh.InferenceRequestBody{Payload: payload}}
		err := p.PreRequest(context.Background(), req, nil)
		require.Error(t, err, name)
		assert.Contains(t, err.Error(), "cannot carry a priority stamp", name)
		assert.Zero(t, p.states["a-group"].inFlight, "%s: a rejected request must not be booked", name)
	}
	// With the stamp off the same bodies pass untouched: the flag is what
	// makes them unacceptable.
	off, _ := newTestPlugin(t, twoGroupConfig(1, 1))
	req := &fwksched.InferenceRequest{FairnessID: "a-group",
		Body: &fwkrh.InferenceRequestBody{Payload: fwkrh.RawPayload(`{}`)}}
	require.NoError(t, off.PreRequest(context.Background(), req, nil))
}

// ---------------------------------------------------------------------------
// Non-negotiable 2: integer tags only
// ---------------------------------------------------------------------------

var jsonIntegerPriority = regexp.MustCompile(`"priority":(\d+)[,}]`)

// vLLM answers a fractional priority with 400 int_from_float. Whatever the
// tag, the bytes the director forwards must hold a bare integer.
func TestStampedPriorityIsNeverFractional(t *testing.T) {
	t.Parallel()
	for _, tag := range []float64{0, 1e-9, 0.0004, 0.0005, 3.5, 3.5e-3, 1.0 / 3, 12345.6789, 1e9 + 0.5,
		1e12, 1e15, 1e300, math.Inf(1), math.NaN(), -7.25, math.MaxFloat64} {
		q := quantiseTag(tag)
		assert.GreaterOrEqual(t, q, int64(0), "tag %v", tag)
		assert.LessOrEqual(t, q, maxStampedPriority, "tag %v", tag)
		b, err := fwkrh.PayloadMap{"priority": q}.Marshal()
		require.NoError(t, err)
		assert.Regexp(t, jsonIntegerPriority, string(b), "tag %v marshalled as %s", tag, b)
	}

	// End to end through PreRequest, with costs and weights chosen so the raw
	// tags are non-integral at every step.
	cfg := twoGroupConfig(3, 7)
	cfg.SFQPriorityStamp = true
	cfg.OutputTokenWeight = 1.7
	cfg.InputTokenWeight = 0.3
	p, clock := newTestPlugin(t, cfg)
	rng := rand.New(rand.NewSource(1))
	for i := 0; i < 2000; i++ {
		g := []string{"a-group", "b-group"}[i%2]
		req := sfqRequest(g, nil, int64(1+rng.Intn(997)))
		req.RequestSizeBytes = 1 + rng.Intn(9999)
		require.NoError(t, p.PreRequest(context.Background(), req, onEndpoint("e0")))
		b, err := req.Body.Payload.(fwkrh.PayloadMap).Marshal()
		require.NoError(t, err)
		require.Regexp(t, jsonIntegerPriority, string(b))
		require.False(t, bytes.Contains(b, []byte("e+")), "no exponent form: %s", b)
		firstByte(p, req)
		complete(p, req, 1+rng.Intn(3000), 1+rng.Intn(997))
		clock.advance(time.Duration(rng.Intn(50)) * time.Millisecond)
	}
}

// ---------------------------------------------------------------------------
// Non-negotiable 3: propagatePriority must be off, verified at startup
// ---------------------------------------------------------------------------

// Not parallel: these swap the package-level probe.
func TestFactoryRefusesToStartWithPropagatePriority(t *testing.T) {
	orig := propagatePriorityProbe
	t.Cleanup(func() { propagatePriorityProbe = orig })
	params := `{"sfqPriorityStamp": true}`

	propagatePriorityProbe = func() (bool, string, error) { return true, "/etc/epp/config.yaml", nil }
	_, err := Factory("t", json.NewDecoder(strings.NewReader(params)), nil)
	require.Error(t, err)
	assert.Contains(t, err.Error(), "propagatePriority: true")

	propagatePriorityProbe = func() (bool, string, error) { return false, "", errors.New("no config flag") }
	_, err = Factory("t", json.NewDecoder(strings.NewReader(params)), nil)
	require.Error(t, err, "a check that could not run must not pass")
	assert.Contains(t, err.Error(), "could not be verified off")

	propagatePriorityProbe = func() (bool, string, error) { return false, "/etc/epp/config.yaml", nil }
	_, err = Factory("t", json.NewDecoder(strings.NewReader(params)), nil)
	require.NoError(t, err)

	// Stamp off: the probe is never consulted, so an EPP without the stamp
	// cannot be broken by this check.
	propagatePriorityProbe = func() (bool, string, error) { t.Fatal("probe called with the stamp off"); return false, "", nil }
	_, err = Factory("t", json.NewDecoder(strings.NewReader(`{}`)), nil)
	require.NoError(t, err)
}

func TestParsePropagatePriority(t *testing.T) {
	t.Parallel()
	for _, c := range []struct {
		doc  string
		want bool
	}{
		{"apiVersion: llm-d.ai/v1alpha1\nkind: EndpointPickerConfig\nrequestHandler:\n  propagatePriority: true\n", true},
		{"requestHandler:\n  propagatePriority: false\n", false},
		{"requestHandler:\n  parsers: []\n", false},
		{"plugins: []\n", false},
	} {
		got, _, err := parsePropagatePriority([]byte(c.doc), "test")
		require.NoError(t, err)
		assert.Equal(t, c.want, got, c.doc)
	}
	_, _, err := parsePropagatePriority([]byte("requestHandler: [unterminated"), "test")
	assert.Error(t, err)
}

// ---------------------------------------------------------------------------
// The tag and the clock
// ---------------------------------------------------------------------------

func TestStartTagsAdvanceByCostOverWeight(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, sfqConfig()) // a-group weight 2, b-group weight 1
	ctx := context.Background()
	var a, b []int64
	for i := 0; i < 3; i++ {
		ra, rb := sfqRequest("a-group", nil, 64), sfqRequest("b-group", nil, 64)
		require.NoError(t, p.PreRequest(ctx, ra, onEndpoint("e0")))
		require.NoError(t, p.PreRequest(ctx, rb, onEndpoint("e0")))
		a, b = append(a, stamped(t, ra)), append(b, stamped(t, rb))
	}
	est := p.cost(100, 0, 64) // 400 bytes / 4, max_tokens 64
	assert.Equal(t, []int64{0, quantiseTag(est / 2), quantiseTag(est)}, a)
	assert.Equal(t, []int64{0, quantiseTag(est), quantiseTag(2 * est)}, b,
		"half the weight, twice the tag step")
}

func TestVirtualTimeIsMinOverServingEndpoints(t *testing.T) {
	t.Parallel()
	cfg := sfqConfig()
	cfg.SFQEndpointStaleSeconds = 10
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()
	v := func() float64 { return p.sfq.view(clock.now()).VirtualTime }

	// a-group runs far ahead on fast e0; b-group's one request sits on slow e1.
	var fast []*fwksched.InferenceRequest
	for i := 0; i < 5; i++ {
		r := sfqRequest("a-group", nil, 64)
		require.NoError(t, p.PreRequest(ctx, r, onEndpoint("e0")))
		fast = append(fast, r)
	}
	slow := sfqRequest("b-group", nil, 64)
	require.NoError(t, p.PreRequest(ctx, slow, onEndpoint("e1")))
	firstByte(p, slow)
	for _, r := range fast[:4] {
		firstByte(p, r)
	}
	assert.Equal(t, 0.0, v(), "e1's newest start is tag 0, and the min holds V there")

	// e1 starts nothing more and goes stale: it stops holding V back...
	clock.advance(11 * time.Second)
	firstByte(p, fast[4])
	assert.Equal(t, fast[4].Body.Payload.(fwkrh.PayloadMap)["priority"].(int64), quantiseTag(v()),
		"a stale endpoint drops out of the min; V follows e0")

	// ...and V never moves backwards when it rejoins.
	before := v()
	late := sfqRequest("b-group", nil, 64)
	require.NoError(t, p.PreRequest(ctx, late, onEndpoint("e1")))
	firstByte(p, late)
	assert.GreaterOrEqual(t, v(), before)
}

// The freeze the ticket warns about. An endpoint that stops getting traffic
// must not pin V, or a group that goes idle returns at its old finish tag and
// wins every queue slot until it catches up.
func TestIdleEndpointDoesNotFreezeVirtualTime(t *testing.T) {
	t.Parallel()
	p, clock := newTestPlugin(t, sfqConfig())
	ctx := context.Background()

	// e1 serves one b-group request, then goes idle.
	once := sfqRequest("b-group", nil, 64)
	require.NoError(t, p.PreRequest(ctx, once, onEndpoint("e1")))
	firstByte(p, once)
	complete(p, once, 100, 64)

	// a-group keeps e0 busy for a long time.
	for i := 0; i < 200; i++ {
		r := sfqRequest("a-group", nil, 64)
		require.NoError(t, p.PreRequest(ctx, r, onEndpoint("e0")))
		firstByte(p, r)
		complete(p, r, 100, 64)
		clock.advance(100 * time.Millisecond)
	}
	vNow := p.sfq.view(clock.now()).VirtualTime
	require.Greater(t, vNow, 0.0, "V must advance on the endpoint that is working")

	// b-group returns: it starts at V, not at its stale finish tag.
	back := sfqRequest("b-group", nil, 64)
	require.NoError(t, p.PreRequest(ctx, back, onEndpoint("e1")))
	assert.Equal(t, quantiseTag(vNow), stamped(t, back))
}

// ---------------------------------------------------------------------------
// Completion never observed: the conservative failure
// ---------------------------------------------------------------------------

// Not parallel: it reads the process-global sfq_unsettled_total{a-group},
// which other parallel tests also increment.
func TestLostCompletionIsChargedWorstCase(t *testing.T) {
	cfg := sfqConfig()
	cfg.SFQSettleTimeoutSeconds = 60
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()
	w := p.states["a-group"].weight

	lost := sfqRequest("a-group", nil, 1024)
	require.NoError(t, p.PreRequest(ctx, lost, onEndpoint("e0")))
	est := p.sfq.view(clock.now()).FinishTags["a-group"] * w
	worst := p.cost(100, 0, 1024)
	require.Less(t, est, worst)

	before := testutil.ToFloat64(sfqUnsettled.WithLabelValues("a-group"))
	clock.advance(61 * time.Second)
	next := sfqRequest("b-group", nil, 64)
	require.NoError(t, p.PreRequest(ctx, next, onEndpoint("e0"))) // reaping runs on dispatch
	view := p.sfq.view(clock.now())
	assert.InDelta(t, worst/w, view.FinishTags["a-group"], 1e-9,
		"a lost completion costs its full max_tokens, never just the estimate")
	assert.Equal(t, before+1, testutil.ToFloat64(sfqUnsettled.WithLabelValues("a-group")))
	assert.Equal(t, 1, view.Endpoints[0].InFlight, "the reaped request is off e0's in-flight count")

	// It completes after all: trued down to the measured cost, and e0's count
	// is not decremented a second time.
	complete(p, lost, 100, 200)
	view = p.sfq.view(clock.now())
	assert.InDelta(t, p.cost(100, 0, 200)/w, view.FinishTags["a-group"], 1e-9)
	assert.Equal(t, 1, view.Endpoints[0].InFlight)
}

func TestLostCompletionWithoutMaxTokensUsesTheUnboundedLength(t *testing.T) {
	t.Parallel()
	cfg := sfqConfig()
	cfg.SFQSettleTimeoutSeconds = 1
	cfg.SFQUnboundedOutputTokens = 8000
	p, clock := newTestPlugin(t, cfg)
	require.NoError(t, p.PreRequest(context.Background(), sfqRequest("a-group", nil, 0), nil))
	clock.advance(2 * time.Second)
	require.NoError(t, p.PreRequest(context.Background(), sfqRequest("b-group", nil, 0), nil))
	assert.InDelta(t, p.cost(100, 0, 8000)/2, p.sfq.view(clock.now()).FinishTags["a-group"], 1e-9)
}

// A no-usage completion leaves the estimate on the tag. The tab refunds a
// stream reset (UNI-213); the tag must not, or a client could take most of a
// stream and disconnect to have its place in the queue back.
func TestNoUsageCompletionKeepsTheTagCharge(t *testing.T) {
	t.Parallel()
	for _, cause := range []fwkrc.TerminationCause{
		fwkrc.TerminationCauseClientDisconnect, fwkrc.TerminationCauseError, fwkrc.TerminationCauseNatural,
	} {
		p, clock := newTestPlugin(t, sfqConfig())
		req := sfqRequest("a-group", nil, 64)
		require.NoError(t, p.PreRequest(context.Background(), req, onEndpoint("e0")))
		charged := p.sfq.view(clock.now()).FinishTags["a-group"]
		p.ResponseBody(context.Background(), req, &fwkrc.Response{EndOfStream: true, TerminationCause: cause}, nil)
		view := p.sfq.view(clock.now())
		assert.Equal(t, charged, view.FinishTags["a-group"], "cause %v", cause)
		assert.Empty(t, view.Endpoints, "cause %v: the request is still settled, and an idle endpoint leaves the ledger", cause)
	}
}

func TestCompletionTrueUpMovesTheFinishTag(t *testing.T) {
	t.Parallel()
	p, clock := newTestPlugin(t, sfqConfig())
	req := sfqRequest("a-group", nil, 1024)
	require.NoError(t, p.PreRequest(context.Background(), req, onEndpoint("e0")))
	complete(p, req, 100, 1000)
	assert.InDelta(t, p.cost(100, 0, 1000)/2, p.sfq.view(clock.now()).FinishTags["a-group"], 1e-9,
		"the finish tag carries the measured cost, undecayed")
}

// ---------------------------------------------------------------------------
// Observability
// ---------------------------------------------------------------------------

func TestSFQStateIsVisible(t *testing.T) {
	t.Parallel()
	cfg := sfqConfig()
	cfg.EmitAttributionHeaders = true
	p, _ := newTestPlugin(t, cfg)
	ctx := context.Background()
	est := p.cost(100, 0, 64) // b-group weight 1
	req := sfqRequest("b-group", nil, 64)
	require.NoError(t, p.PreRequest(ctx, req, onEndpoint("e0")))
	req2 := sfqRequest("b-group", nil, 64)
	require.NoError(t, p.PreRequest(ctx, req2, onEndpoint("e0")))

	resp := &fwkrc.Response{Headers: map[string]string{":status": "200"}}
	p.ResponseHeader(ctx, req2, resp, nil)
	assert.Equal(t, strconv.FormatInt(quantiseTag(est), 10), resp.Headers[fairnessPriorityHeader],
		"the caller sees its own stamped priority")

	raw, err := p.DumpState()
	require.NoError(t, err)
	var d struct {
		SFQ *sfqView `json:"sfq"`
	}
	require.NoError(t, json.Unmarshal(raw, &d))
	require.NotNil(t, d.SFQ, "the debug dump must carry the SFQ ledger")
	assert.InDelta(t, 2*est, d.SFQ.FinishTags["b-group"], 1e-9)
	assert.Equal(t, 2, d.SFQ.Pending)

	logCtx, lines := capturingContext()
	p.logFlightRecorderTick(logCtx)
	line, ok := findLine(*lines, `"group":"b-group"`)
	require.True(t, ok)
	assert.InDelta(t, 2*est, logFieldNumber(t, line, "sfqFinishTag"), 1e-9)
	assert.Equal(t, 0.0, logFieldNumber(t, line, "sfqVirtualTime"))

	// Stamp off: no SFQ section, no header, no flight-recorder fields.
	off, _ := newTestPlugin(t, twoGroupConfig(1, 1))
	raw, err = off.DumpState()
	require.NoError(t, err)
	assert.NotContains(t, string(raw), `"sfq"`)
}

// UNI-293 review: under the stamp, Pick ranks the EPP-held queue by the next
// start tag, max(F_g, V), and the tab, the newcomer clamp and the virtualTime
// ratchet take no part. The tab and the tag are set to disagree: a-group has
// dispatched (F_a > 0) but has a near-zero tab; b-group has never dispatched
// (F_b = 0) but a huge tab. The tag picks b-group. The pre-review path
// (tabPick) picks a-group, so the test discriminates.
func TestPickUnderStampRanksByTagNotTab(t *testing.T) {
	t.Parallel()
	pick := func(tabPick bool) (string, *Plugin, *bandState, float64) {
		cfg := sfqConfig()
		cfg.Enforce = true
		p, clock := newTestPlugin(t, cfg)
		p.sfq.tabPick = tabPick
		ctx := context.Background()
		for i := 0; i < 3; i++ {
			require.NoError(t, p.PreRequest(ctx, sfqRequest("a-group", nil, 64), onEndpoint("e0")))
		}
		p.states["a-group"].setNormalizedService(clock.now(), 0)
		p.states["b-group"].setNormalizedService(clock.now(), 1e9)
		band := newSimBand(p,
			&simFlow{id: "a-group", depth: 5, headAt: clock.now()},
			&simFlow{id: "b-group", depth: 5, headAt: clock.now()})
		q, err := p.Pick(ctx, band.accessor())
		require.NoError(t, err)
		return q.FlowKey().ID, p, band.state.(*bandState), p.states["b-group"].normalizedService(clock.now())
	}

	got, _, bs, bTab := pick(false)
	assert.Equal(t, "b-group", got, "lowest next start tag wins, whatever the tab says")
	assert.Zero(t, bs.virtualTime, "the ratchet must not advance under the stamp; sfqState.v is the one V")
	assert.InDelta(t, 1e9, bTab, 1e3, "nothing under the stamp may write the tab from Pick")

	got, _, _, _ = pick(true)
	assert.Equal(t, "a-group", got, "the tab path must disagree, or this test proves nothing")
}

func TestAgingIsRejectedUnderTheStamp(t *testing.T) {
	t.Parallel()
	cfg := sfqConfig()
	cfg.AgingTokensPerSecond = 1
	_, err := newPlugin("x", cfg)
	require.ErrorContains(t, err, "agingTokensPerSecond must be 0 when sfqPriorityStamp is on")
	cfg.SFQPriorityStamp = false
	_, err = newPlugin("x", cfg)
	require.NoError(t, err)
}
