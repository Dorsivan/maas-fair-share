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
	_ flowcontrol.FairnessPolicy   = &Plugin{}
	_ fwkrc.RequestHeaderProcessor = &Plugin{}
	_ fwkrc.PreRequest             = &Plugin{}
	_ fwkrc.ResponseBodyProcessor  = &Plugin{}
	_ fwkplugin.StateDumper        = &Plugin{}
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

	unmatchedMu     sync.Mutex
	unmatchedSample map[string]struct{}
	unmatchedCount  uint64

	// lastContendedUnixNano gates the flight recorder: it logs only while
	// contention is recent, so an idle cluster produces no output at all.
	lastContendedUnixNano atomic.Int64
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

	if !matched && sub != "" {
		unmatchedSubscriptions.Inc()
		p.recordUnmatched(ctx, sub)
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

func (p *Plugin) recordUnmatched(ctx context.Context, sub string) {
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
	if first {
		log.FromContext(ctx).Info("subscription matched no fairness group; using catch-all",
			"plugin", p.name, "subscription", sub, "group", p.groups.fallback)
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
	id := p.fairnessIDFor(request)
	gs := p.stateFor(id)
	dispatchTotal.WithLabelValues(boundID(id)).Inc()

	if !p.cfg.ProvisionalCharge {
		gs.addInFlight(1, 0)
		return nil
	}

	now := p.now()
	est := p.estimateCost(request, gs)
	contended := p.isContended(now)
	request.PutAttribute(provisionalChargeKey, provisionalCharge{cost: est, at: now, contended: contended})
	gs.charge(now, est)
	gs.addInFlight(1, est)
	if contended {
		addContendedService(id, est)
	}
	return nil
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
			log.FromContext(ctx).V(1).Info("response completed with no usage block; check --enable-force-include-usage",
				"plugin", p.name, "group", id, "requestID", response.RequestID)
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
	// Reuse the gate decided at dispatch (see provisionalCharge.contended)
	// rather than checking contention again at this, later, moment. The
	// provisional estimate and this correction are one logical charge; gating
	// them independently at two different times can count only one of the two,
	// so their sum stops equalling the cost actually charged.
	if charge.contended {
		addContendedService(id, delta)
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
// Counters cannot move backwards, so a non-positive amount -- a true-up that
// corrects an overestimate -- is silently dropped rather than recorded.
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

// runFlightRecorder emits the same table to the log on a fixed cadence, but only
// while contention is recent. Pick runs on a ~1ms ticker so per-decision logging
// is out of the question; this gives a flight recorder in Loki for clusters with
// no Prometheus, and stays completely silent when nothing is competing.
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
			log.FromContext(ctx).Info("fairness state", "plugin", p.name, "state", p.dump())
		}
	}
}
