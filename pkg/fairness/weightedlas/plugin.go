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

// Package weightedlas implements a weighted least-attained-service fairness
// policy for the llm-d Router's flow-control subsystem.
//
// Each configured group carries a decaying tab of recently consumed token cost;
// the group with the lowest tab/weight is served next. Equalising tab/weight is
// proportional sharing, so the delivered ratios converge on the configured
// weights without any constant describing how fast the pool is -- the policy is
// scale-free.
//
// Work conservation is structural rather than implemented: the framework only
// calls Pick when a dispatch slot is free, and IterateQueues visits only
// non-empty queues. A single active group is therefore picked every time and
// receives the whole pool. There is deliberately no saturation check anywhere in
// this package; writing one would be a bug.
//
// See docs/design.md for the full rationale.
package weightedlas

import (
	"context"
	"encoding/json"
	"fmt"
	"math"
	"sort"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
	"time"

	"github.com/go-logr/logr"
	"sigs.k8s.io/controller-runtime/pkg/log"

	"github.com/llm-d/llm-d-router/pkg/epp/framework/interface/datalayer"
	"github.com/llm-d/llm-d-router/pkg/epp/framework/interface/flowcontrol"
	fwkplugin "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/plugin"
	fwkrc "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requestcontrol"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

// PluginType is the `type` to name in the EndpointPickerConfig plugins list.
const PluginType = "maas-weighted-fairness"

// maxContendedStep caps how much contended time a single Pick may credit. Pick
// runs on a roughly 1ms cadence, so anything larger than this means the band was
// idle in between and the gap is not contention.
const maxContendedStep = time.Second

// maxLoggedUnmatched bounds the unmatched-subscription sample retained for the
// state dump and the flight recorder. The values are client-controlled, so the
// set they are drawn from is not bounded by anything we own.
const maxLoggedUnmatched = 16

// provisionalChargeKey is the per-request attribute holding what PreRequest
// charged and when. It lives on the request rather than in a per-tenant counter
// because concurrent requests from one group must reconcile independently, and
// because attribute lifetime tracks the request so an abandoned one cannot leak.
var provisionalChargeKey = fwkplugin.NewDataKey("provisional-cost", PluginType)

type provisionalCharge struct {
	cost float64
	at   time.Time
	// contended is whether the band was contended at dispatch, when the charge
	// was actually incurred. The true-up at completion reuses this instead of
	// re-checking contention at its own, later moment -- see recordContendedService.
	contended bool
}

var (
	_ flowcontrol.FairnessPolicy    = &Plugin{}
	_ fwkrc.RequestHeaderProcessor  = &Plugin{}
	_ fwkrc.PreRequest              = &Plugin{}
	_ fwkrc.ResponseHeaderProcessor = &Plugin{}
	_ fwkrc.ResponseBodyProcessor   = &Plugin{}
	_ fwkplugin.StateDumper         = &Plugin{}
)

// Plugin is a singleton shared across every priority band. All band-scoped
// mutable state lives in the object returned by NewState; everything here is
// either immutable configuration or keyed by group.
type Plugin struct {
	name   string
	cfg    Config
	groups *groupTable

	// states is keyed by group name and fully populated at construction. The
	// group set is closed by configuration, so there is nothing to evict and the
	// metric label cardinality is bounded by construction.
	states map[string]*groupState

	// identityHeader is the lowercased header name, matching how the framework
	// normalizes request headers.
	identityHeader string

	// now is injected so decay tests can advance time instead of sleeping.
	now func() time.Time

	// genID mints a fallback correlation id when a request carries neither an
	// x-request-id header nor an upstream-populated InferenceRequest.RequestID.
	// Injected so tests get a deterministic value instead of a random one.
	genID func() string

	unmatchedMu     sync.Mutex
	unmatchedSample map[string]struct{}
	unmatchedCount  uint64

	// lastContendedUnixNano gates the flight recorder: it logs only while
	// contention is recent, so an idle cluster produces no output at all.
	lastContendedUnixNano atomic.Int64

	// v4Once starts the V(4) per-request tier's time box on the first eligible
	// completion this plugin ever evaluates, rather than at construction --
	// see v4WithinTimeBox.
	v4Once     sync.Once
	v4Deadline time.Time
	// v4Counter drives the 1-in-N sample: it is incremented only for
	// completions that already passed the config and verbosity gates, so the
	// sample rate is relative to eligible lines, not to total traffic.
	v4Counter atomic.Uint64

	// flightRecorderTick increments once per emitted flight-recorder tick, not
	// once per group line, so every per-group line from the same tick shares one
	// id and a consumer can reassemble the table -- see docs/log-field-contract.md.
	// Also read (never incremented) from the V(4) per-request line as
	// recorderTick: the most recently assigned tick id as of that request's
	// settlement (the counter is incremented before its per-group lines are
	// emitted, so a request settling mid-emission reads that in-progress tick,
	// not a completed one). This is the join the board's "whole story from a
	// response header" query uses to find the recorder's view of the cluster
	// around the same time. It is a recency marker, not an exact interval
	// membership test -- a request can settle between two ticks.
	flightRecorderTick atomic.Uint64
}

// Factory builds the plugin from its `parameters` block.
func Factory(name string, parameters *json.Decoder, handle fwkplugin.Handle) (fwkplugin.Plugin, error) {
	cfg := DefaultConfig()
	if parameters != nil {
		if err := parameters.Decode(&cfg); err != nil {
			return nil, fmt.Errorf("invalid config for %s plugin %q: %w", PluginType, name, err)
		}
	}
	p, err := newPlugin(name, cfg)
	if err != nil {
		return nil, fmt.Errorf("%s plugin %q: %w", PluginType, name, err)
	}

	if handle != nil {
		if reg := handle.Metrics(); reg != nil {
			for _, c := range collectors() {
				reg.MustRegister(c)
			}
			p.publishStaticMetrics()
		}
		if cfg.StateLogIntervalSeconds > 0 {
			go p.runFlightRecorder(handle.Context(),
				time.Duration(cfg.StateLogIntervalSeconds*float64(time.Second)))
		}
	}
	return p, nil
}

// newPlugin builds a validated plugin without touching the handle, so tests can
// construct one from a Config literal rather than round-tripping through JSON
// (where `omitempty` would silently re-default any field set to its zero value).
func newPlugin(name string, cfg Config) (*Plugin, error) {
	if err := cfg.validate(); err != nil {
		return nil, err
	}
	table, err := newGroupTable(&cfg)
	if err != nil {
		return nil, err
	}
	p := &Plugin{
		name:            name,
		cfg:             cfg,
		groups:          table,
		states:          make(map[string]*groupState, len(table.names())),
		identityHeader:  strings.ToLower(cfg.IdentityHeader),
		now:             time.Now,
		genID:           generateFallbackID,
		unmatchedSample: make(map[string]struct{}, maxLoggedUnmatched),
	}
	for _, gname := range table.names() {
		p.states[gname] = newGroupState(gname, table.weight(gname), cfg.HalfLifeSeconds, cfg.ObservedHalfLivesSeconds)
	}
	return p, nil
}

func (p *Plugin) publishStaticMetrics() {
	for name, gs := range p.states {
		configuredWeight.WithLabelValues(boundID(name)).Set(gs.weight)
	}
	if p.cfg.Enforce {
		enforcingGauge.Set(1)
	} else {
		enforcingGauge.Set(0)
	}
}

// TypedName returns the type and name tuple of this plugin instance.
func (p *Plugin) TypedName() fwkplugin.TypedName {
	return fwkplugin.TypedName{Type: PluginType, Name: p.name}
}

// stateFor returns the group state for a flow ID. Flow control will create a
// queue for any ID, including one some other component set, so an unrecognised
// ID is folded into the catch-all group rather than minting unbounded state.
func (p *Plugin) stateFor(id string) *groupState {
	if gs, ok := p.states[id]; ok {
		return gs
	}
	return p.states[p.groups.fallback]
}

// ---------------------------------------------------------------------------
// Identity: subscription -> group, before the FlowKey is chosen
// ---------------------------------------------------------------------------

// RequestHeader resolves the authenticated subscription into a group name and
// writes it to request.FairnessID.
//
// The overwrite is unconditional, and that is the point. The director's own
// fallback only fills FairnessID in when it is empty, so a client sending
// x-llm-d-inference-fairness-id: app1 would otherwise inherit app1's weight.
// Running here, before that fallback, and overwriting rather than defaulting is
// what makes the spoof inert even if the gateway forgets to strip the header.
//
// Collapsing many subscriptions onto one name here, rather than keying queues by
// subscription, is also what keeps the end-user group at one shared weight
// instead of one weight per subscription.
func (p *Plugin) RequestHeader(ctx context.Context, request *fwksched.InferenceRequest) error {
	if request == nil {
		return nil
	}
	sub := p.subscriptionID(request)
	name, matched := p.groups.resolve(sub)
	request.FairnessID = name

	// Resolved once, here, and stored on the request so every later hook --
	// PreRequest, ResponseBody, ResponseHeader -- logs and surfaces the same
	// id rather than re-deriving (and potentially re-generating) it. See
	// docs/design.md "Per-request attribution".
	corr := resolveCorrelation(request, p.now(), p.genID)
	request.PutAttribute(correlationKey, corr)

	if !matched && sub != "" {
		unmatchedSubscriptions.Inc()
		p.recordUnmatched(ctx, sub, corr, request.Objectives.Priority)
	}
	return nil
}

func (p *Plugin) subscriptionID(request *fwksched.InferenceRequest) string {
	if request.Headers == nil {
		return ""
	}
	if v, ok := request.Headers[p.identityHeader]; ok {
		return strings.TrimSpace(v)
	}
	// The framework lowercases header keys, but a custom parser or a test may
	// not have. The map is small enough that the fallback scan is free.
	for k, v := range request.Headers {
		if strings.EqualFold(k, p.identityHeader) {
			return strings.TrimSpace(v)
		}
	}
	return ""
}

func (p *Plugin) recordUnmatched(ctx context.Context, sub string, corr correlation, band int) {
	p.unmatchedMu.Lock()
	p.unmatchedCount++
	first := false
	if len(p.unmatchedSample) < maxLoggedUnmatched {
		if _, seen := p.unmatchedSample[sub]; !seen {
			p.unmatchedSample[sub] = struct{}{}
			first = true
		}
	}
	p.unmatchedMu.Unlock()

	// Only the first sighting of each distinct value is logged: the value is
	// client-controlled, so logging every occurrence is a log-flood primitive.
	// The request id is still this specific request's, even though the
	// dedup gate is keyed on the subscription string.
	if first {
		fields := append([]any{"plugin", p.name, "subscription", sub, "group", p.groups.fallback,
			"band", band, "enforcing", p.cfg.Enforce}, corr.logFields()...)
		log.FromContext(ctx).Info("subscription matched no fairness group; using catch-all", fields...)
	}
}

// ---------------------------------------------------------------------------
// FairnessPolicy
// ---------------------------------------------------------------------------

// NewState creates the per-priority-band state.
func (p *Plugin) NewState(_ context.Context) any { return newBandState() }

type candidate struct {
	queue      flowcontrol.FlowQueueAccessor
	state      *groupState
	id         string
	normalized float64
	headWait   float64
	enqueuedAt time.Time
}

// Pick selects the backlogged group with the lowest tab/weight.
func (p *Plugin) Pick(
	ctx context.Context,
	flowGroup flowcontrol.PriorityBandAccessor,
) (flowcontrol.FlowQueueAccessor, error) {
	if flowGroup == nil {
		return nil, nil //nolint:nilnil
	}
	raw := flowGroup.PolicyState()
	bs, ok := raw.(*bandState)
	if !ok {
		return nil, fmt.Errorf("%s: invalid band state: expected *bandState, got %T", PluginType, raw)
	}

	now := p.now()
	candidates := make([]candidate, 0, 8)
	flowGroup.IterateQueues(func(q flowcontrol.FlowQueueAccessor) bool {
		// The accessor view is eventually consistent, so a visited queue may
		// report zero. Treating it as a candidate would let an empty flow win a
		// dispatch opportunity that then has nothing to dispatch.
		if q == nil || q.Len() == 0 {
			return true
		}
		id := q.FlowKey().ID
		c := candidate{queue: q, state: p.stateFor(id), id: id}
		if head := q.Peek(); head != nil {
			c.enqueuedAt = head.EnqueueTime()
			if !c.enqueuedAt.IsZero() {
				c.headWait = now.Sub(c.enqueuedAt).Seconds()
			}
		}
		candidates = append(candidates, c)
		return true
	})
	if len(candidates) == 0 {
		return nil, nil //nolint:nilnil
	}

	// IterateQueues order is unspecified and backing implementations range a Go
	// map, so without this the tie-break would differ run to run.
	sort.Slice(candidates, func(i, j int) bool { return candidates[i].id < candidates[j].id })

	bs.mu.Lock()
	seq := bs.beginPick()

	minNormalized := math.Inf(1)
	for i := range candidates {
		candidates[i].normalized = candidates[i].state.normalizedService(now)
		if candidates[i].normalized < minNormalized {
			minNormalized = candidates[i].normalized
		}
	}

	// The newcomer clamp. A group away long enough for its tab to decay to zero
	// would otherwise win every decision until it caught up, stalling everyone
	// else for tens of seconds. Raising it to the current floor still lets it go
	// first -- a returning tenant should get low latency -- but it goes first
	// once rather than a thousand times.
	//
	// Both terms of the floor are needed: virtualTime is the textbook V(t) and
	// handles the cold start where every group legitimately begins at zero;
	// the minimum over current candidates handles a band that went fully empty
	// and left virtualTime stale.
	if p.cfg.NewcomerClamp {
		floor := math.Max(bs.virtualTime, minNormalized)
		for i := range candidates {
			edge := bs.isBacklogEdge(candidates[i].id, seq)
			if edge && candidates[i].normalized < floor {
				candidates[i].state.setNormalizedService(now, floor)
				candidates[i].normalized = floor
				newcomerClamps.WithLabelValues(boundID(candidates[i].id)).Inc()
			}
		}
	} else {
		for i := range candidates {
			bs.isBacklogEdge(candidates[i].id, seq)
		}
	}
	bs.pruneLastSeen(seq, len(candidates))

	// Contended time: the SLI denominator. A group is only competing when at
	// least one other group in its band is backlogged at the same moment.
	var contendedStep float64
	if len(candidates) > 1 {
		contendedStep = bs.contendedDelta(now, maxContendedStep)
	} else {
		bs.lastContendedAt = time.Time{}
	}
	bs.mu.Unlock()

	if contendedStep > 0 {
		p.lastContendedUnixNano.Store(now.UnixNano())
		for i := range candidates {
			contendedSeconds.WithLabelValues(boundID(candidates[i].id)).Add(contendedStep)
		}
	}

	best := 0
	bestScore := math.Inf(1)
	for i := range candidates {
		// Aging is applied in raw units, not range-normalized against the
		// currently-backlogged set: rescaling would change the mapping every
		// cycle, leaving the equilibrium with no fixed point corresponding to
		// any allocation ratio.
		score := candidates[i].normalized - p.cfg.AgingTokensPerSecond*candidates[i].headWait
		if score < bestScore {
			bestScore, best = score, i
		}
	}

	bs.mu.Lock()
	if candidates[best].normalized > bs.virtualTime {
		bs.virtualTime = candidates[best].normalized
	}
	bs.mu.Unlock()

	p.publishNormalized(now, candidates)

	if !p.cfg.Enforce {
		// Shadow mode: everything above still happened -- classification,
		// clamping, accounting, metrics -- but the dispatch order the cluster
		// actually experiences is the one it had before this plugin existed.
		return fcfsPick(candidates), nil
	}
	return candidates[best].queue, nil
}

// fcfsPick returns the candidate whose head request has waited longest, which
// is what the stock ordering would have produced. Candidates are already sorted
// by ID, so a tie resolves deterministically.
func fcfsPick(candidates []candidate) flowcontrol.FlowQueueAccessor {
	best := 0
	for i := 1; i < len(candidates); i++ {
		switch {
		case candidates[best].enqueuedAt.IsZero():
			best = i
		case candidates[i].enqueuedAt.IsZero():
		case candidates[i].enqueuedAt.Before(candidates[best].enqueuedAt):
			best = i
		}
	}
	return candidates[best].queue
}

func (p *Plugin) publishNormalized(now time.Time, candidates []candidate) {
	for i := range candidates {
		id := boundID(candidates[i].id)
		normalizedService.WithLabelValues(id).Set(candidates[i].normalized)
		if len(p.cfg.ObservedHalfLivesSeconds) == 0 {
			continue
		}
		observed := candidates[i].state.observedNormalized(now)
		for j, v := range observed {
			normalizedServiceObserved.WithLabelValues(
				id, strconv.FormatFloat(p.cfg.ObservedHalfLivesSeconds[j], 'f', -1, 64),
			).Set(v)
		}
	}
}

// ---------------------------------------------------------------------------
// Accounting
// ---------------------------------------------------------------------------

// PreRequest charges a provisional estimate at dispatch.
//
// Without this the policy is blind for the whole duration of a generation: the
// real token count only arrives 10-40s later, while scheduling decisions happen
// every millisecond, so a group would dispatch thousands of requests before any
// of them landed on its tab. The estimate is a hold, settled by ResponseBody.
func (p *Plugin) PreRequest(_ context.Context, request *fwksched.InferenceRequest, _ *fwksched.SchedulingResult) error {
	if request == nil {
		return nil
	}
	now := p.now()
	id := p.fairnessIDFor(request)
	gs := p.stateFor(id)
	dispatchTotal.WithLabelValues(boundID(id)).Inc()
	p.recordQueueWait(request, now)

	if !p.cfg.ProvisionalCharge {
		gs.addInFlight(1, 0)
		return nil
	}

	est := p.estimateCost(request, gs)
	contended := p.isContended(now)
	request.PutAttribute(provisionalChargeKey, provisionalCharge{cost: est, at: now, contended: contended})
	gs.charge(now, est)
	gs.addInFlight(1, est)
	// The SLI numerator is booked once, at completion, against the real cost --
	// see ResponseBody. Booking the estimate here too would require later
	// subtracting it out again when the real cost turns out lower, and a
	// Prometheus counter cannot move backwards.
	return nil
}

// recordQueueWait finishes the correlation attribute RequestHeader started,
// recording the time between classification and dispatch -- the
// x-maas-fairness-queue-ms value ResponseHeader surfaces to the caller. It is
// an approximation of time spent under flow-control admission, not that
// subsystem's own internal clock; see docs/design.md "Per-request attribution".
func (p *Plugin) recordQueueWait(request *fwksched.InferenceRequest, now time.Time) {
	corr, ok := fwksched.ReadRequestAttribute[correlation](request, correlationKey)
	if !ok {
		// PreRequest without a preceding RequestHeader call -- a direct unit
		// test, or a future change to extension-point ordering. Derive a fresh
		// correlation rather than silently skipping the field.
		corr = resolveCorrelation(request, now, p.genID)
	}
	corr.queueMs = now.Sub(corr.arrivedAt).Seconds() * 1000
	corr.haveQueueMs = true
	request.PutAttribute(correlationKey, corr)
}

// ResponseBody settles the hold against the real usage block.
//
// Only the end-of-stream call does anything; intermediate chunks are no-ops for
// both streaming and non-streaming responses.
func (p *Plugin) ResponseBody(
	ctx context.Context,
	request *fwksched.InferenceRequest,
	response *fwkrc.Response,
	_ *datalayer.EndpointMetadata,
) {
	if request == nil || response == nil || !response.EndOfStream {
		return
	}
	id := p.fairnessIDFor(request)
	gs := p.stateFor(id)
	now := p.now()
	corr, haveCorr := fwksched.ReadRequestAttribute[correlation](request, correlationKey)
	if !haveCorr {
		corr = resolveCorrelation(request, now, p.genID)
	}

	charge, charged := fwksched.ReadRequestAttribute[provisionalCharge](request, provisionalChargeKey)
	if charged {
		gs.addInFlight(-1, -charge.cost)
	} else {
		gs.addInFlight(-1, 0)
	}

	var cachedPtr *int
	if response.Usage.PromptTokens != 0 && response.Usage.PromptTokenDetails != nil {
		cachedPtr = &response.Usage.PromptTokenDetails.CachedTokens
	}
	prompt, cached, completion, ok := usageTokens(
		response.Usage.PromptTokens, response.Usage.CompletionTokens, cachedPtr)

	if !ok {
		// No usage block. Either a model server is missing
		// --enable-force-include-usage, or the stream was torn down before the
		// final chunk. Either way the provisional charge stays: refunding would
		// make abort-spam free, and the charge decays away on its own over a few
		// half-lives if the request genuinely never ran.
		requestsWithoutUsage.WithLabelValues(boundID(id)).Inc()
		if response.TerminationCause == fwkrc.TerminationCauseNatural {
			fields := append([]any{"plugin", p.name, "group", id,
				"band", request.Objectives.Priority, "enforcing", p.cfg.Enforce}, corr.logFields()...)
			log.FromContext(ctx).V(1).Info("response completed with no usage block; check --enable-force-include-usage", fields...)
		}
		// No true-up will ever follow this charge, so the estimate IS the cost
		// actually charged -- book it now, under the contention decided at
		// dispatch, or it is never counted at all.
		if charged && charge.contended {
			addContendedService(id, charge.cost)
		}
		return
	}

	actual := p.cost(prompt, cached, completion)
	gs.recordCompletion(completion, prompt, cached)
	if r, has := gs.cachedRatio(); has {
		cachedRatio.WithLabelValues(boundID(id)).Set(r)
	}

	if !charged {
		// Provisional charging disabled, or the request never passed through
		// PreRequest. Charge the measured cost outright.
		gs.charge(now, actual)
		p.recordContendedService(id, actual)
		return
	}

	delta := actual - charge.cost
	inflight := now.Sub(charge.at).Seconds()
	// The correction is decayed by the time the hold has already spent decaying,
	// which makes the tab exactly what it would have been had the true value
	// been charged at dispatch. Adding the raw delta instead would leave the
	// accumulated tab dependent on estimator quality rather than on consumption.
	gs.chargeInflight(now, delta, inflight)
	truingError.WithLabelValues(boundID(id)).Observe(delta)
	if v4, ok := p.v4Logger(ctx, now); ok {
		fields := append([]any{"plugin", p.name, "group", id,
			"band", request.Objectives.Priority, "enforcing", p.cfg.Enforce,
			"estimateCharged", charge.cost, "trueUpDelta", delta,
			"recorderTick", p.flightRecorderTick.Load()}, corr.logFields()...)
		v4.Info("per-request fairness tier", fields...)
	}
	// Book the full real cost, not the delta, under the gate decided at dispatch
	// (see provisionalCharge.contended) rather than re-checking contention at
	// this, later, moment. Booking only the delta would silently drop an
	// overestimate -- a negative delta -- since a counter cannot move backwards;
	// booking the actual cost in one shot keeps the metric equal to the real
	// cost regardless of which way the estimator missed.
	if charge.contended {
		addContendedService(id, actual)
	}
}

// ResponseHeader surfaces the request's own classification back to the caller
// -- item D6 of docs/design.md's plan: a tenant's own fairness group and
// queue wait, plus the id that ties it to the EPP's own log line, at zero log
// volume and no cluster access.
//
// Verified against this extension point on llm-d-router v0.11.0: response.Headers
// is the same map reqCtx.Response.Headers, and the director writes it into the
// ext_proc HeaderMutation unconditionally for any key that is not in
// request.IsSystemOwnedHeader -- none of the three keys here are. The session
// affinity plugin that ships with llm-d-router relies on the same mechanism
// to set its own response header, which is why the design doc's "unverified"
// note is resolved rather than carried forward.
//
// Suppressible via cfg.EmitAttributionHeaders: this is a tenant's own
// classification, but it is also internal detail some deployments may not
// want on the wire.
func (p *Plugin) ResponseHeader(
	_ context.Context,
	request *fwksched.InferenceRequest,
	response *fwkrc.Response,
	_ *datalayer.EndpointMetadata,
) {
	if !p.cfg.EmitAttributionHeaders || request == nil || response == nil {
		return
	}
	corr, ok := fwksched.ReadRequestAttribute[correlation](request, correlationKey)
	if !ok {
		corr = resolveCorrelation(request, p.now(), p.genID)
	}
	if response.Headers == nil {
		response.Headers = make(map[string]string)
	}
	response.Headers[requestIDHeader] = corr.requestID
	response.Headers[fairnessGroupHeader] = p.fairnessIDFor(request)
	if corr.haveQueueMs {
		response.Headers[fairnessQueueMsHeader] = strconv.FormatFloat(corr.queueMs, 'f', 1, 64)
	}
}

// recordContendedService books a one-shot charge against the SLI numerator --
// used only where the charge and the gate decision happen at the same moment
// (no later true-up follows). Charges that are later corrected must decide
// contention once, at dispatch, and reuse it; see provisionalCharge.contended.
func (p *Plugin) recordContendedService(id string, amount float64) {
	if !p.isContended(p.now()) {
		return
	}
	addContendedService(id, amount)
}

// isContended reports whether the band was contended recently enough, as of
// now, to count service toward the SLI numerator.
func (p *Plugin) isContended(now time.Time) bool {
	last := p.lastContendedUnixNano.Load()
	return last != 0 && now.Sub(time.Unix(0, last)) <= maxContendedStep
}

// addContendedService is the metric write shared by every gated charge site.
// Every caller passes a real, measured cost (never a provisional estimate or a
// true-up delta -- see PreRequest and ResponseBody), so amount is non-positive
// only for a degenerate zero-token request; the counter cannot move backwards,
// so that case is dropped rather than recorded.
func addContendedService(id string, amount float64) {
	if amount <= 0 {
		return
	}
	contendedServiceTokens.WithLabelValues(boundID(id)).Add(amount)
}

func (p *Plugin) fairnessIDFor(request *fwksched.InferenceRequest) string {
	if request.FairnessID == "" {
		return p.groups.fallback
	}
	return request.FairnessID
}

// ---------------------------------------------------------------------------
// Observability
// ---------------------------------------------------------------------------

type dumpState struct {
	Enforcing       bool       `json:"enforcing"`
	HalfLifeSeconds float64    `json:"halfLifeSeconds"`
	CostModel       string     `json:"costModel"`
	Groups          []snapshot `json:"groups"`
	// Unmatched subscription IDs are client-controlled strings, so only a
	// bounded sample is retained and reported.
	UnmatchedTotal  uint64   `json:"unmatchedSubscriptionsTotal"`
	UnmatchedSample []string `json:"recentUnmatchedSubscriptions"`
	Truncated       bool     `json:"truncated"`
}

// DumpState serves the live tab table on the admin debug endpoint. Equal
// normalizedService across backlogged groups is the whole policy working,
// visible at a glance.
func (p *Plugin) DumpState() (json.RawMessage, error) {
	return json.Marshal(p.dump())
}

func (p *Plugin) dump() dumpState {
	now := p.now()
	d := dumpState{
		Enforcing:       p.cfg.Enforce,
		HalfLifeSeconds: p.cfg.HalfLifeSeconds,
		CostModel:       p.cfg.CostModel,
		Groups:          make([]snapshot, 0, len(p.states)),
	}
	for _, name := range p.groups.names() {
		if gs, ok := p.states[name]; ok {
			d.Groups = append(d.Groups, gs.snapshot(now))
		}
	}
	p.unmatchedMu.Lock()
	d.UnmatchedTotal = p.unmatchedCount
	for s := range p.unmatchedSample {
		d.UnmatchedSample = append(d.UnmatchedSample, s)
	}
	d.Truncated = len(p.unmatchedSample) >= maxLoggedUnmatched
	p.unmatchedMu.Unlock()
	sort.Strings(d.UnmatchedSample)
	return d
}

// v4Logger reports whether this particular settlement should emit the V(4)
// per-request tier line, and the logger to emit it with if so.
//
// See docs/design.md "V(4) per-request tier": the tier is off by default,
// sampled, and time-boxed because Pick runs on a ~1ms ticker and unsampled
// per-request logging is out of scope for this plugin's hot path, always.
// This plugin's `parameters` block has no live-reload path (Factory decodes
// it once, at construction) and the EPP process's own -v flag is parsed once
// at startup with no exposed dynamic endpoint either (see
// github.com/llm-d/llm-d-router/pkg/common/observability/logging.Options) --
// so neither knob can be changed without a redeploy, and this gates on both
// rather than on a dynamically reloadable path: cfg.RequestTierV4SampleEvery
// (this plugin's own switch and sample rate) AND the process's existing V(4)
// verbosity flag.
//
// Cheapest checks first: the config gate and the logr level check are a field
// load and an interface call, so a disabled tier (the default) never reaches
// the atomic counter this method also updates.
func (p *Plugin) v4Logger(ctx context.Context, now time.Time) (logr.Logger, bool) {
	if p.cfg.RequestTierV4SampleEvery == 0 {
		return logr.Logger{}, false
	}
	l := log.FromContext(ctx).V(4)
	if !l.Enabled() {
		return logr.Logger{}, false
	}
	if !p.v4WithinTimeBox(now) {
		return logr.Logger{}, false
	}
	if p.v4Counter.Add(1)%p.cfg.RequestTierV4SampleEvery != 0 {
		return logr.Logger{}, false
	}
	return l, true
}

// v4WithinTimeBox reports whether the V(4) tier's self-disable window is
// still open. The window starts at the first call -- effectively pod start
// for a live EPP, since real traffic arrives immediately -- rather than at
// plugin construction, so tests can control "now" before any window begins.
// Once cfg.RequestTierV4TimeBoxSeconds has elapsed since that first call, the
// tier stays silent even if the config and verbosity gates are still open,
// which is what makes it impossible to leave on by accident past a redeploy.
func (p *Plugin) v4WithinTimeBox(now time.Time) bool {
	p.v4Once.Do(func() {
		p.v4Deadline = now.Add(time.Duration(p.cfg.RequestTierV4TimeBoxSeconds * float64(time.Second)))
	})
	return now.Before(p.v4Deadline)
}

// runFlightRecorder emits the group table to the log on a fixed cadence, but
// only while contention is recent. Pick runs on a ~1ms ticker so per-decision
// logging is out of the question; this gives a flight recorder in Loki for
// clusters with no Prometheus, and stays completely silent when nothing is
// competing.
func (p *Plugin) runFlightRecorder(ctx context.Context, interval time.Duration) {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()
	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			last := p.lastContendedUnixNano.Load()
			if last == 0 || p.now().Sub(time.Unix(0, last)) > interval {
				continue
			}
			p.logFlightRecorderTick(ctx)
		}
	}
}

// logFlightRecorderTick emits one "fairness state" line per configured group,
// rather than the whole table as a single line with a nested `groups` array.
//
// A JSON array inside one log field does not unroll into a time series: Loki's
// `| json` only flattens nested *objects* (with `_`) and skips arrays entirely
// (see docs/logging-install-spec.md §7), and Elasticsearch has the same
// problem under its default dynamic mapping. Either way, per-group trends --
// one tenant's normalizedService climbing while another's falls -- were not
// directly queryable from the old shape; a query first had to pull the whole
// array out as a string and re-parse it. One line per group makes `group` and
// the per-group numbers first-class fields a LogQL/Elastic query can select,
// filter, and chart on without that detour.
//
// The shared `tick` field is what lets a consumer reassemble every group's row
// from the same recording pass -- see docs/log-field-contract.md and the
// "what did the recorder see at time T" query in docs/logql-queries.md.
//
// This intentionally does not include `band`: unlike a request-scoped line,
// where `band` is read straight off that one request's own
// InferenceRequest.Objectives.Priority, a group's accounting state
// (groupState) is shared across whatever priority bands route requests into
// it -- it is not itself scoped to one band. On this POC's configuration there
// is exactly one priority band (`priority: 0`, see deploy/poc/00-config.yaml),
// so every line here is implicitly that band, but asserting a `band` field
// here would be encoding that single-band assumption into the contract rather
// than describing what the code actually tracks. A deployment that configures
// more than one band would need groupState itself split per band before this
// line could carry the field honestly -- out of scope here, recorded as a gap
// in docs/log-field-contract.md rather than silently assumed away.
func (p *Plugin) logFlightRecorderTick(ctx context.Context) {
	now := p.now()
	tick := p.flightRecorderTick.Add(1)
	logger := log.FromContext(ctx)
	for _, name := range p.groups.names() {
		gs, ok := p.states[name]
		if !ok {
			continue
		}
		s := gs.snapshot(now)
		logger.Info("fairness state",
			"plugin", p.name,
			"tick", tick,
			"group", s.Name,
			"enforcing", p.cfg.Enforce,
			"weight", s.Weight,
			"attainedService", s.AttainedService,
			"normalizedService", s.NormalizedService,
			"inFlight", s.InFlight,
			"provisionalCharge", s.ProvisionalCharge,
			"ewmaOutputTokens", s.EWMAOutputTokens,
			"ewmaWarm", s.EWMAWarm,
		)
	}
}
