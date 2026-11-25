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
	fwkrh "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requesthandling"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"

	errcommon "github.com/llm-d/llm-d-router/pkg/common/error"
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

// responseStatusKey holds the backend's HTTP status header, captured at
// ResponseHeader so ResponseBody's no-usage branch (which runs on the body
// phase, where Response.Headers is nil) can tell a terminally-unservable
// rejection from a stream that was simply torn down. See UNI-190: a
// context-length rejection (HTTP 400) sends no usage block, by design, so
// without this the no-usage branch cannot distinguish "backend said no" from
// "we never found out."
var responseStatusKey = fwkplugin.NewDataKey("response-status", PluginType)

// isErrorStatus reports whether a captured backend HTTP status means the
// backend rejected or failed the request rather than serving it. UNI-190
// scoped this to exactly "400" (context-length rejections only); UNI-213
// widened it to any non-2xx status -- the board's follow-up decision that a
// request charged at dispatch and then rejected by the backend for *any*
// reason, having delivered nothing, should not be booked at ~9-10x a served
// request's cost either. A status that is missing entirely (never reached
// ResponseHeader, or the backend never set one) is not an error by this
// check -- see the comment in ResponseBody for why that case must stay
// charged.
func isErrorStatus(status string) bool {
	return len(status) > 0 && status[0] != '2'
}

// exemptionReason classifies why a no-usage completion in ResponseBody
// should be refunded rather than booked, for the "reason" label on
// provisionalChargesExempted. Returns "" when the completion should NOT be
// exempted -- a real request the model server simply didn't report usage
// for (see ResponseBody).
func exemptionReason(cause fwkrc.TerminationCause, status string, haveStatus bool) string {
	switch {
	case cause == fwkrc.TerminationCauseClientDisconnect:
		// A stream reset: torn down somewhere between the client and the EPP
		// (client disconnect, Envoy drain/restart, an upstream reset). The
		// framework cannot tell these apart from the EPP's side of the
		// stream, and neither can this plugin.
		return "stream_reset"
	case cause == fwkrc.TerminationCauseError:
		// An EPP-side failure or a cancellation that reached the EPP before
		// its propagation completed -- a context cancel, from the tenant's
		// point of view.
		return "context_cancel"
	case cause == fwkrc.TerminationCauseNatural && haveStatus && isErrorStatus(status):
		// The backend responded, but with an error -- UNI-190's original
		// context-length-400 case, generalized to any error status.
		return "error_status"
	default:
		return ""
	}
}

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

	// configuredEstimateSeedOnly is a test knob: a group's estimatedOutputTokens
	// is only a cold-start seed and its warm EWMA takes over. It is the UNI-299
	// alternative that was not shipped; it exists so the sim can measure it.
	configuredEstimateSeedOnly bool

	// now is injected so decay tests can advance time instead of sleeping.
	now func() time.Time

	// genID mints a fallback correlation id when a request carries neither an
	// x-request-id header nor an upstream-populated InferenceRequest.RequestID.
	// Injected so tests get a deterministic value instead of a random one.
	genID func() string

	unmatchedMu     sync.Mutex
	unmatchedSample map[string]struct{}
	unmatchedCount  uint64

	// identityMu guards the tumbling window observeIdentity uses to decide
	// whether the identity header is missing from nearly all recent traffic.
	identityMu          sync.Mutex
	identityWindowStart time.Time
	identityTotal       uint64
	identityMissing     uint64
	identityAbsent      uint64

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

	// sfq is the SFQ priority-stamp ledger, nil unless cfg.SFQPriorityStamp.
	sfq *sfqState
	// sfqLog is cfg.SFQDecisionLog; always off without the stamp.
	sfqLog sfqLogLevel
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
	if cfg.SFQPriorityStamp {
		source, err := checkPropagatePriorityOff()
		if err != nil {
			return nil, fmt.Errorf("%s plugin %q: %w", PluginType, name, err)
		}
		ctx := context.Background()
		if handle != nil {
			ctx = handle.Context()
		}
		log.FromContext(ctx).Info("SFQ priority stamp enabled; requestHandler.propagatePriority verified off",
			"plugin", name, "config", source,
			"tabRole", "observability only", "newcomerClampInert", cfg.NewcomerClamp,
			"endpointStaleSeconds", cfg.SFQEndpointStaleSeconds, "settleTimeoutSeconds", cfg.SFQSettleTimeoutSeconds,
			"decisionLog", p.sfqLog.String())
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
		gs := newGroupState(gname, table.weight(gname), cfg.HalfLifeSeconds, cfg.ObservedHalfLivesSeconds)
		gs.configuredOutput, gs.haveConfiguredOutput = table.estOutput[gname]
		p.states[gname] = gs
	}
	if cfg.SFQPriorityStamp {
		p.sfq = newSFQState(&cfg)
		p.sfqLog = parseSFQLogLevel(cfg.SFQDecisionLog)
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
	if p.cfg.SFQPriorityStamp {
		sfqEnabledGauge.Set(1)
	} else {
		sfqEnabledGauge.Set(0)
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
	sub, present := p.subscriptionID(request)
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
	if sub == "" {
		reason := "empty"
		if !present {
			reason = "absent"
		}
		identityHeaderMissing.WithLabelValues(reason).Inc()
	}
	p.observeIdentity(ctx, sub == "", !present)
	return nil
}

// subscriptionID returns the trimmed identity header value and whether the
// header was present at all. The distinction matters: present-but-empty is the
// AuthPolicy's non-API-key path, absent on every request is a misnamed header.
func (p *Plugin) subscriptionID(request *fwksched.InferenceRequest) (string, bool) {
	if request.Headers == nil {
		return "", false
	}
	if v, ok := request.Headers[p.identityHeader]; ok {
		return strings.TrimSpace(v), true
	}
	// The framework lowercases header keys, but a custom parser or a test may
	// not have. The map is small enough that the fallback scan is free.
	for k, v := range request.Headers {
		if strings.EqualFold(k, p.identityHeader) {
			return strings.TrimSpace(v), true
		}
	}
	return "", false
}

// The identity-miss warning is judged over a tumbling window rather than per
// request: a few unauthenticated callers are normal, and a startup check cannot
// see a misnamed header at all -- it only shows under traffic.
const (
	identityMissWindow      = time.Minute
	identityMissMinRequests = 20
	identityMissWarnShare   = 0.9
)

// observeIdentity counts this request into the current window and, when the
// window closes, warns if the identity header was missing from nearly all of
// it. That is the one signature of a wrong identityHeader (UNI-306): every
// request quietly lands in the catch-all, nothing mis-matches, and fairness
// does nothing with no error. At most one line per window, so it cannot flood.
//
// The window closes on the first request after it expires, so an idle plugin
// emits nothing -- the right behaviour, since an idle split is not broken.
func (p *Plugin) observeIdentity(ctx context.Context, missing, absent bool) {
	now := p.now()
	p.identityMu.Lock()
	if p.identityWindowStart.IsZero() {
		p.identityWindowStart = now
	}
	var total, miss, abs uint64
	var span time.Duration
	closed := now.Sub(p.identityWindowStart) >= identityMissWindow
	if closed {
		total, miss, abs = p.identityTotal, p.identityMissing, p.identityAbsent
		span = now.Sub(p.identityWindowStart)
		p.identityWindowStart = now
		p.identityTotal, p.identityMissing, p.identityAbsent = 0, 0, 0
	}
	p.identityTotal++
	if missing {
		p.identityMissing++
	}
	if absent {
		p.identityAbsent++
	}
	p.identityMu.Unlock()

	if !closed || total < identityMissMinRequests || float64(miss) < identityMissWarnShare*float64(total) {
		return
	}
	log.FromContext(ctx).Info("identity header missing from most requests; fairness is treating them all as the catch-all group",
		"plugin", p.name, "identityHeader", p.identityHeader, "group", p.groups.fallback,
		"enforcing", p.cfg.Enforce, "windowSeconds", span.Seconds(),
		"requests", total, "missing", miss, "absent", abs,
		"hint", "absent ~= requests means identityHeader names a header the gateway never sends; the MaaS AuthPolicy injects "+DefaultIdentityHeader)
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
	// tag is the SFQ start tag this group's next dispatch would get. Set, and
	// used as the score, only when the stamp is on. See Pick.
	tag        float64
	headWait   float64
	enqueuedAt time.Time
}

// Pick selects the backlogged group with the lowest tab/weight, or, with the
// SFQ stamp on, the lowest next start tag.
//
// UNI-293: with the stamp on, the tab is not an input to this decision. The
// tab is a decaying average of service and the SFQ finish tag is an
// undecaying virtual finish time. They are two answers to "how much has this
// group had", and ranking the EPP-held queue by one while vLLM's waiting
// queue is ranked by the other would run two policies in series. So under
// the stamp:
//
//   - Order: by max(F_g, V), the tag the group's next request will be
//     stamped with. The EPP and vLLM then rank by the same number.
//   - The tab: still charged, trued up and decayed exactly as before, but
//     read only by metrics (maas_fairness_normalized_service), the flight
//     recorder and the state dump. halfLifeSeconds and undecayedTrueUp then
//     shape only that observability series.
//   - newcomerClamp: does not run. The max(F_g, V) term is the exact form of
//     the same rule: a group returning from idle cannot claim credit from
//     before V. The clamp writes only to the tab, so leaving it on would
//     change nothing this function decides; skipping it also stops the
//     clamp counter reporting firings that had no effect. The sim case
//     TestSFQSimHoldReturnNeedsNoClamp measures both arms.
//   - The virtualTime ratchet: not advanced. Its only reader is the clamp
//     floor. sfqState.v is the one V.
//   - agingTokensPerSecond: rejected by validate. It is in tab units.
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
	//
	// UNI-220: the edge test alone is not enough to mean "gone." A group whose
	// own offered concurrency is below the pool's capacity cycles its FlowQueue
	// between empty and non-empty on the timescale of one request's latency --
	// not because it stopped wanting service, but because the request it does
	// have outstanding is still being served. hasInFlight() excludes exactly
	// this case: a group with a dispatched-but-not-yet-completed request has
	// never actually left, so clamping it to the floor on every such gap
	// discards the deficit its weight earned it, over and over, for as long as
	// it keeps cycling. Live evidence (UNI-218's app1-flood at the settled
	// config): the clamp fired 28 times on the starved, concurrency-limited
	// end-users group and 0 times on the continuously-flooding app1 -- almost
	// every firing was this false case, not a genuine return from idle. A
	// group that is truly gone -- zero queue depth AND zero in-flight -- is
	// unaffected: this adds a condition to when the clamp may fire, it does
	// not relax the wall-clock gate that already decides genuine absence.
	sfqPick := p.sfq != nil && !p.sfq.tabPick
	idleThreshold := time.Duration(p.cfg.NewcomerClampIdleSeconds * float64(time.Second))
	if p.cfg.NewcomerClamp && !sfqPick {
		floor := math.Max(bs.virtualTime, minNormalized)
		for i := range candidates {
			edge := bs.isBacklogEdge(candidates[i].id, seq, now, idleThreshold)
			if edge && candidates[i].normalized < floor && !candidates[i].state.hasInFlight() {
				candidates[i].state.setNormalizedService(now, floor)
				candidates[i].normalized = floor
				newcomerClamps.WithLabelValues(boundID(candidates[i].id)).Inc()
			}
		}
	} else {
		for i := range candidates {
			bs.isBacklogEdge(candidates[i].id, seq, now, idleThreshold)
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

	if sfqPick {
		groups := make([]string, len(candidates))
		for i := range candidates {
			groups[i] = candidates[i].state.name
		}
		for i, tag := range p.sfq.nextStarts(now, groups) {
			candidates[i].tag = tag
		}
	}

	best := 0
	bestScore := math.Inf(1)
	for i := range candidates {
		if sfqPick {
			if candidates[i].tag < bestScore {
				bestScore, best = candidates[i].tag, i
			}
			continue
		}
		// Aging is applied in raw units, not range-normalized against the
		// currently-backlogged set: rescaling would change the mapping every
		// cycle, leaving the equilibrium with no fixed point corresponding to
		// any allocation ratio.
		score := candidates[i].normalized - p.cfg.AgingTokensPerSecond*candidates[i].headWait
		if score < bestScore {
			bestScore, best = score, i
		}
	}

	if !sfqPick {
		bs.mu.Lock()
		if candidates[best].normalized > bs.virtualTime {
			bs.virtualTime = candidates[best].normalized
		}
		bs.mu.Unlock()
	}

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
func (p *Plugin) PreRequest(ctx context.Context, request *fwksched.InferenceRequest, result *fwksched.SchedulingResult) error {
	if request == nil {
		return nil
	}
	now := p.now()
	id := p.fairnessIDFor(request)
	gs := p.stateFor(id)
	// First, before any path below can return early. UNI-293: the priority
	// field is a security boundary, not a tuning knob.
	if err := p.stampPriority(ctx, request, result, id, gs, now); err != nil {
		return err
	}
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

// stampPriority owns the outbound request's `priority` field. UNI-293.
//
// vLLM reads `priority` straight from the request body, and with
// requestHandler.propagatePriority off (it must be; see
// checkPropagatePriorityOff) nothing else in the EPP touches it. So a
// client's own `priority` passes through to vLLM unchanged. Under today's
// --scheduling-policy fcfs vLLM accepts and ignores it. The day a pool flips
// to priority scheduling, it becomes a direct queue jump for anyone who
// guesses the field name. That is the same class of defect as the
// client-controlled fairness ID flagged on upstream PR #3471, and the reason
// RequestHeader overwrites FairnessID unconditionally.
//
// So the field is always this plugin's, flag or no flag:
//   - stamp off: a client-supplied priority is deleted. Under fcfs that
//     changes nothing vLLM does. It just stops the spoof from going live when
//     the pool's policy changes.
//   - stamp on: the field is overwritten with the request's SFQ start tag.
//     A body this plugin cannot rewrite (a raw or proto payload) is rejected,
//     not forwarded, because forwarding it would pass through whatever
//     priority it carries.
func (p *Plugin) stampPriority(ctx context.Context, request *fwksched.InferenceRequest, result *fwksched.SchedulingResult,
	id string, gs *groupState, now time.Time,
) error {
	body := request.Body
	if body == nil {
		// Nothing is forwarded from here that could carry a priority.
		return nil
	}
	m, isMap := body.Payload.(fwkrh.PayloadMap)
	if isMap {
		if _, had := m["priority"]; had {
			clientPriorityOverwritten.WithLabelValues(boundID(id)).Inc()
		}
	}
	if p.sfq == nil {
		if isMap {
			if _, had := m["priority"]; had {
				body.MutatePayloadMap(func(m fwkrh.PayloadMap) { delete(m, "priority") })
			}
		}
		return nil
	}
	if !isMap {
		sfqUnstampable.WithLabelValues(boundID(id)).Inc()
		return errcommon.Error{Code: errcommon.BadRequest,
			Msg: "maas-weighted-fairness: request body cannot carry a priority stamp"}
	}

	est := p.estimateCost(request, gs)
	worstOut := p.cfg.SFQUnboundedOutputTokens
	if body.MaxOutputTokens != nil && *body.MaxOutputTokens >= 0 {
		worstOut = float64(*body.MaxOutputTokens)
	}
	worst := p.cost(p.estimatePromptTokens(request), 0, int(worstOut))
	var corr correlation
	if p.sfqLog != sfqLogOff {
		corr = p.correlationFor(request, now)
	}
	ticket, rec := p.sfq.dispatch(now, corr.requestID, gs.name, targetEndpoint(result), gs.weight, est, worst)
	body.MutatePayloadMap(func(m fwkrh.PayloadMap) { m["priority"] = ticket.priority })
	request.PutAttribute(sfqTicketKey, ticket)

	for _, r := range rec.Reaped {
		sfqUnsettled.WithLabelValues(boundID(r.Group)).Inc()
	}
	if rec.Rank == 1 {
		sfqDispatchedAtFront.WithLabelValues(boundID(gs.name)).Inc()
	}
	sfqStampedPriority.WithLabelValues(boundID(gs.name)).Set(float64(ticket.priority))
	if rec.Rebased || rec.IdleReset() {
		// Every group's finish tag moved, not just this one's.
		for name := range p.states {
			p.publishSFQ(name)
		}
	} else {
		p.publishSFQ(gs.name)
		for _, r := range rec.Reaped {
			if r.Group != gs.name {
				p.publishSFQ(r.Group)
			}
		}
	}
	if p.sfqLog != sfqLogOff {
		p.logSFQDispatch(ctx, request, corr, gs, ticket, est, &rec)
	}
	return nil
}

// sfqLogLevel is Config.SFQDecisionLog, parsed once.
type sfqLogLevel int

const (
	sfqLogOff sfqLogLevel = iota
	sfqLogInfo
	sfqLogDebug
)

func parseSFQLogLevel(s string) sfqLogLevel {
	switch s {
	case SFQDecisionLogInfo:
		return sfqLogInfo
	case SFQDecisionLogDebug:
		return sfqLogDebug
	default:
		return sfqLogOff
	}
}

func (l sfqLogLevel) String() string {
	switch l {
	case sfqLogInfo:
		return SFQDecisionLogInfo
	case sfqLogDebug:
		return SFQDecisionLogDebug
	default:
		return SFQDecisionLogOff
	}
}

// correlationFor returns the request's correlation, resolving and storing it
// if RequestHeader did not, so every later line carries the same id.
func (p *Plugin) correlationFor(request *fwksched.InferenceRequest, now time.Time) correlation {
	corr, ok := fwksched.ReadRequestAttribute[correlation](request, correlationKey)
	if !ok {
		corr = resolveCorrelation(request, now, p.genID)
		request.PutAttribute(correlationKey, corr)
	}
	return corr
}

// logSFQDispatch writes the UNI-302 per-request lines. It runs after the
// ledger lock is released: rec is a snapshot. See docs/log-field-contract.md
// §3.4 for the fields.
func (p *Plugin) logSFQDispatch(ctx context.Context, request *fwksched.InferenceRequest, corr correlation,
	gs *groupState, t *sfqTicket, est float64, rec *sfqDispatchRecord,
) {
	logger := log.FromContext(ctx)
	fields := append([]any{"plugin", p.name, "group", gs.name,
		"band", request.Objectives.Priority, "enforcing", p.cfg.Enforce,
		"weight", gs.weight, "priority", t.priority,
		"tag", t.start, "rank", fmt.Sprintf("%d/%d", rec.Rank, rec.Groups), "rankPos", rec.Rank, "rankOf", rec.Groups,
		"virtualTime", rec.V, "tagAboveV", t.start - rec.V,
		"finishTag", rec.FinishAfter, "finishAboveV", rec.FinishAfter - rec.V,
	}, corr.logFields()...)
	logger.Info("sfq priority", fields...)
	if p.sfqLog < sfqLogDebug {
		return
	}
	reaped := rec.Reaped
	if reaped == nil {
		reaped = []sfqReaped{}
	}
	fields = append([]any{"plugin", p.name, "group", gs.name,
		"band", request.Objectives.Priority, "enforcing", p.cfg.Enforce,
		"weight", gs.weight, "est", est, "worst", t.worst, "endpoint", t.endpoint,
		"vBefore", rec.VBefore, "virtualTime", rec.V, "vFrom", rec.VFrom, "servingEndpoints", rec.Serving,
		"idleReset", rec.IdleReset(), "rebased", rec.Rebased, "epoch", rec.Epoch,
		"finishBefore", rec.FinishBefore, "start", t.start, "finishAfter", rec.FinishAfter,
		"tagScale", sfqTagScale, "quantisedTag", rec.Tag, "wireBase", rec.WireBase, "priority", t.priority,
		"rankPos", rec.Rank, "rankOf", rec.Groups,
		"finishTags", rec.FinishTags, "endpoints", rec.Endpoints,
		"reapedTimeout", len(rec.Reaped), "reapedCompleted", rec.SettledDropped, "reaped", reaped,
	}, corr.logFields()...)
	logger.Info("sfq decision", fields...)
}

// logSFQSettle writes the UNI-302 true-up record. Debug only.
func (p *Plugin) logSFQSettle(ctx context.Context, request *fwksched.InferenceRequest, t *sfqTicket, rec *sfqSettleRecord) {
	corr, ok := fwksched.ReadRequestAttribute[correlation](request, correlationKey)
	if !ok {
		corr = correlation{requestID: t.id}
	}
	fields := append([]any{"plugin", p.name, "group", t.group,
		"band", request.Objectives.Priority, "enforcing", p.cfg.Enforce,
		"weight", t.weight, "priority", t.priority, "start", t.start,
		"charged", rec.Charged, "actual", rec.Actual, "haveActual", rec.HaveActual,
		"reaped", rec.Reaped, "staleEpoch", rec.StaleEpoch,
		"finishBefore", rec.FinishBefore, "finishCorrection", rec.FinishCorrection, "finishAfter", rec.FinishAfter,
		"virtualTime", rec.V,
	}, corr.logFields()...)
	log.FromContext(ctx).Info("sfq settle", fields...)
}

// publishSFQ refreshes the virtual-time gauges and one group's finish tag.
func (p *Plugin) publishSFQ(group string) {
	v, f, serving := p.sfq.gauges(group)
	sfqVirtualTime.Set(v)
	sfqServingEndpoints.Set(float64(serving))
	sfqFinishTag.WithLabelValues(boundID(group)).Set(f)
	sfqLag.WithLabelValues(boundID(group)).Set(f - v)
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
	if request == nil || response == nil {
		return
	}
	ticket, haveTicket := fwksched.ReadRequestAttribute[*sfqTicket](request, sfqTicketKey)
	haveTicket = haveTicket && ticket != nil && p.sfq != nil
	if haveTicket && !response.EndOfStream {
		// The first response byte is the EPP's view of vLLM starting this
		// request -- the signal V advances on.
		p.sfq.observeStart(ticket, p.now())
	}
	if !response.EndOfStream {
		return
	}
	id := p.fairnessIDFor(request)
	gs := p.stateFor(id)
	now := p.now()
	// Every exit below settles the ticket. Only the usage branch sets an
	// actual; every other branch leaves the charge standing (see settle).
	var sfqActual float64
	sfqHaveActual := false
	if haveTicket {
		defer func() {
			rec, ok := p.sfq.settle(ticket, now, sfqActual, sfqHaveActual)
			p.publishSFQ(ticket.group)
			if ok && p.sfqLog == sfqLogDebug {
				p.logSFQSettle(ctx, request, ticket, &rec)
			}
		}()
	}
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
		// --enable-force-include-usage (a real completion that just didn't
		// report usage), or the request never delivered anything: the backend
		// rejected it outright (an error status), the stream was torn down
		// before the final chunk (a reset somewhere between the client and the
		// EPP), or its context was cancelled (an EPP-side failure or a
		// cancellation that reached the EPP first). Only the first case keeps
		// the provisional charge -- real generation work was measurably
		// performed, so refunding it would undercharge, not correct a leak.
		// UNI-148 (C6) found the second case charged ~9-10x a served request's
		// cost, permanently, for exactly this reason; UNI-190 exempted the
		// context-length-400 instance of it, and UNI-213 (board follow-up)
		// widened that to every case below where nothing was ever delivered.
		// TerminationCauseEvicted is deliberately NOT exempted here: that is
		// the EPP's own capacity-reclaim decision, a different question this
		// ticket doesn't address, so it stays charged, unchanged.
		requestsWithoutUsage.WithLabelValues(boundID(id)).Inc()
		status, haveStatus := fwksched.ReadRequestAttribute[string](request, responseStatusKey)
		reason := exemptionReason(response.TerminationCause, status, haveStatus)
		if reason == "" {
			if response.TerminationCause == fwkrc.TerminationCauseNatural {
				fields := append([]any{"plugin", p.name, "group", id,
					"band", request.Objectives.Priority, "enforcing", p.cfg.Enforce}, corr.logFields()...)
				log.FromContext(ctx).V(1).Info("response completed with no usage block; check --enable-force-include-usage", fields...)
			}
			// No true-up will ever follow this charge, so the estimate IS the
			// cost actually charged -- book it now, under the contention
			// decided at dispatch, or it is never counted at all.
			if charged && charge.contended {
				addContendedService(id, charge.cost)
			}
			return
		}
		// Reverse the hold with the same decayed true-up chargeInflight uses
		// for a measured actual of zero, rather than booking it, so the tab
		// ends up exactly as if PreRequest had never charged it.
		if charged {
			gs.chargeInflight(now, -charge.cost, now.Sub(charge.at).Seconds())
		}
		provisionalChargesExempted.WithLabelValues(boundID(id), reason).Inc()
		return
	}

	actual := p.cost(prompt, cached, completion)
	sfqActual, sfqHaveActual = actual, true
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
	if p.cfg.UndecayedTrueUp && delta > 0 {
		// UNI-293: an under-estimate lands at full weight, as of now. See
		// Config.UndecayedTrueUp. That makes the final tab depend on when the
		// cost became known, not only on the cost. That is the intent: the
		// decayed form below lets a long request's real cost evaporate before
		// it is ever charged.
		gs.charge(now, delta)
	} else {
		// The correction is decayed by the time the hold has already spent decaying,
		// which makes the tab exactly what it would have been had the true value
		// been charged at dispatch. Adding the raw delta instead would leave the
		// accumulated tab dependent on estimator quality rather than on consumption.
		gs.chargeInflight(now, delta, inflight)
	}
	truingError.WithLabelValues(boundID(id)).Observe(delta)
	if v4, ok := p.v4Logger(ctx, now); ok {
		fields := append([]any{"plugin", p.name, "group", id,
			"band", request.Objectives.Priority, "enforcing", p.cfg.Enforce,
			"estimateCharged", charge.cost, "trueUpDelta", delta,
			"recorderTick", p.flightRecorderTick.Load()}, corr.logFields()...)
		if haveTicket {
			fields = append(fields, "sfqPriority", ticket.priority, "sfqStartTag", ticket.start)
		}
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
//
// Also records the backend status (see responseStatusKey) regardless of
// EmitAttributionHeaders -- that flag only governs what goes back to the
// caller, and this is internal bookkeeping ResponseBody needs for the
// provisional-charge exemption, not an attribution header.
//
// UNI-213 live verification (2026-11-09) found this read ":status" as
// "status" (no colon) from UNI-190 onward, so it never once matched real
// traffic: handlers/response.go populates response.Headers verbatim from
// Envoy's ext_proc HeaderMap, whose internal model is HTTP/2-based and
// represents the response status line as the pseudo-header ":status" even
// for an HTTP/1.1 upstream -- there is no plain "status" key. The unit test
// this ticket inherited constructed its fixture with the same wrong key, so
// it passed without ever exercising the real header shape. Confirmed via a
// live C6 re-run: `response completed with no usage block; check
// --enable-force-include-usage` fired for every one of app2's oversized-
// prompt completions (the fallback log, gated on an unmatched status) and
// provisional_charges_exempted_total never incremented, despite
// requests_without_usage_total{app2} and the EPP's own lifecycle log
// confirming a backend 400 was received and processed normally
// (TerminationCauseNatural) for each one.
func (p *Plugin) ResponseHeader(
	_ context.Context,
	request *fwksched.InferenceRequest,
	response *fwkrc.Response,
	_ *datalayer.EndpointMetadata,
) {
	if request == nil || response == nil {
		return
	}
	if status, ok := response.Headers[":status"]; ok {
		request.PutAttribute(responseStatusKey, status)
	}
	if !p.cfg.EmitAttributionHeaders {
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
	if t, ok := fwksched.ReadRequestAttribute[*sfqTicket](request, sfqTicketKey); ok && t != nil {
		response.Headers[fairnessPriorityHeader] = strconv.FormatInt(t.priority, 10)
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
	UndecayedTrueUp bool       `json:"undecayedTrueUp"`
	SFQ             *sfqView   `json:"sfq,omitempty"`
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
		UndecayedTrueUp: p.cfg.UndecayedTrueUp,
		HalfLifeSeconds: p.cfg.HalfLifeSeconds,
		CostModel:       p.cfg.CostModel,
		Groups:          make([]snapshot, 0, len(p.states)),
	}
	for _, name := range p.groups.names() {
		if gs, ok := p.states[name]; ok {
			d.Groups = append(d.Groups, gs.snapshot(now))
		}
	}
	if p.sfq != nil {
		v := p.sfq.view(now)
		d.SFQ = &v
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
	var sfqv sfqView
	if p.sfq != nil {
		sfqv = p.sfq.view(now)
	}
	for _, name := range p.groups.names() {
		gs, ok := p.states[name]
		if !ok {
			continue
		}
		s := gs.snapshot(now)
		var sfqFields []any
		if p.sfq != nil {
			// UNI-293: the clock and this group's place on it, so a live run
			// can be debugged from the log without a rebuild.
			sfqFields = []any{"sfqVirtualTime", sfqv.VirtualTime, "sfqFinishTag", sfqv.FinishTags[name]}
		}
		logger.Info("fairness state", append([]any{
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
		}, sfqFields...)...)
	}
}
