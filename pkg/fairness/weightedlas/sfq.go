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

// UNI-293: start-time fair queueing, stamped into the vLLM request body.
//
// The tab above orders what the EPP releases. But UNI-288 showed that under
// closed-loop load the EPP holds ~8 requests while vLLM's FIFO holds ~88, so
// FIFO decides most of the order. This moves the decision to where the queue
// is. Every dispatched request carries an SFQ start tag as its vLLM `priority`
// (lower is served first). vLLM 0.24 with --scheduling-policy priority reorders
// its waiting queue on that tag and does not preempt on it. That is the model
// the UNI-290 round-2 sim assumed.
//
// Per group g with weight w, a request costing c (the dispatch estimate) gets
//
//	S = max(F_g, V)    F_g = S + c/w
//
// and settles at completion by F_g += (actual - charged)/w. A tag never
// decays, so the true-up is undecayed by construction. See
// Config.UndecayedTrueUp for the equivalent fix on the tab.
//
// The two halves do different jobs and both have to be right. The dispatch
// estimate c sets THIS request's position: its own tag S is fixed the moment
// it is stamped. The completion true-up corrects the group's FUTURE
// positions, by moving F_g before its next request is tagged. The UNI-283
// gaming vector lives entirely in the second: an under-estimate that is never
// trued up keeps every later tag too low.
//
// The cost inputs are unchanged from the tab: inputTokenWeight 1.0,
// outputTokenWeight 2.0, the same group resolution. But outputTokenWeight is
// still the uncalibrated placeholder it has always been, and here it sets
// the tag step directly instead of feeding a decaying average that smooths
// errors away over a half-life. A mis-set output weight is a standing bias in
// every output-heavy group's queue position, not a transient. Calibrating it
// is out of scope for UNI-293; it is called out so it does not slip into
// this new role unnoticed.
//
// What this retires when the stamp is on (see Plugin.Pick): the tab stops
// being a dispatch input and is kept for observability only; newcomerClamp
// stops running, because max(F_g, V) is its exact form; the bandState
// virtualTime ratchet stops advancing, because its only reader was the
// clamp. sfqState.v is the one V.
//
// V is the minimum, over the endpoints that are serving, of the newest start
// tag each one has begun serving. UNI-291 tested the max-tag definition: its
// error with uneven endpoints grows ~1.5 pt per doubling of N (5.3 at N=8, 9.3
// at N=64). The min definition measured 0.0 at every N. See sfqState.serving
// for what "serving" means and why an idle endpoint must be left out.

import (
	"fmt"
	"math"
	"os"
	"sort"
	"sync"
	"sync/atomic"
	"time"

	"github.com/spf13/pflag"
	"sigs.k8s.io/yaml"

	fwkplugin "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/plugin"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

// sfqTagScale quantises a tag to integer milli-cost-units. vLLM 0.24 parses
// `priority` as a strict int. The UNI-291 probe got a 400 int_from_float for
// 3.5, so a fractional tag does not degrade gracefully, it fails the request.
const sfqTagScale = 1000

// maxStampedPriority is the largest priority vLLM accepts. UNI-300 probed
// 0.24.0+rhaiv.9: `priority` is declared `int` with le=2^63-1, so 2^63-1 is
// served and 2^63 is a 400. Integer literals survive its parse, its msgpack
// hop to the engine and its heap compare exactly, 2^53+1 included. A stamp
// that ever reached this would be clamped, every group would then tie, and
// ties go by arrival: FIFO, with no error anywhere. sfqState.rebase is what
// keeps the stamp from getting there.
const maxStampedPriority = int64(math.MaxInt64)

// maxQuantisedTag keeps the float64 half of a stamp inside float64's
// exact-integer range, so the float to int64 conversion can neither round nor
// overflow. The threshold rebase keeps internal tags near zero, so this guard
// should never bind.
const maxQuantisedTag = int64(1) << 53

// sfqRebaseThreshold is the V, in tag units, at which the internal clock is
// rebased. It is low enough that a tag is far inside float64's exact range,
// at ~2^-22 resolution, and high enough that the rebase is rare: ~39 days at
// the 320 tag units/s UNI-294 measured on 16 slots, ~85 s at the fastest
// rate UNI-300 estimated (vramtime, 800 slots, 50k-token prompts). The
// rebase is O(groups + endpoints + pending tickets).
const sfqRebaseThreshold = float64(1 << 30)

// sfqTicketKey holds the request's SFQ ledger entry. It is a pointer so that
// the dispatch, first-byte and completion hooks all update the same entry.
var sfqTicketKey = fwkplugin.NewDataKey("sfq-ticket", PluginType)

// quantiseTag converts a start tag to the integer vLLM is sent. The return
// type is the guarantee that no fractional value can reach the wire. The
// guards cover the inputs a float can hold that an int cannot.
func quantiseTag(tag float64) int64 {
	if math.IsNaN(tag) || tag <= 0 {
		return 0
	}
	q := math.Round(tag * sfqTagScale)
	if q >= float64(maxQuantisedTag) {
		return maxQuantisedTag
	}
	return int64(q)
}

// addSaturating returns a+b, clamped to maxStampedPriority. Both are >= 0.
func addSaturating(a, b int64) int64 {
	if a > maxStampedPriority-b {
		return maxStampedPriority
	}
	return a + b
}

// sfqTicket is one dispatched request's entry in the SFQ ledger.
type sfqTicket struct {
	group    string
	endpoint string
	weight   float64
	start    float64 // S, in tag units (cost / weight), on the internal clock at dispatch
	priority int64   // the value actually stamped
	at       time.Time
	epoch    uint64 // sfqState.epoch at dispatch; an idle reset starts a new one
	// base is sfqState.wireBase at dispatch. start is never rewritten, since
	// it is read without the lock; a rebase since dispatch is applied by
	// subtracting the difference. See observeStartLocked.
	base int64
	// charged is the cost currently booked to the group's finish tag for this
	// request. The dispatch estimate first, then worst if reaped, then the
	// measured actual if a usage block arrives.
	charged float64
	// worst is the request's cost if every allowed token is generated. It is
	// what a request is charged when its completion is never observed.
	worst float64

	started bool // a response byte has come back, so vLLM has begun serving it
	// startSeen mirrors started for the lock-free fast path in observeStart,
	// which runs on every streamed chunk.
	startSeen atomic.Bool
	settled   bool // ResponseBody's end-of-stream ran
	reaped    bool // settleTimeout passed with no completion, so worst was charged
}

// sfqEndpoint is the ledger's view of one model server.
type sfqEndpoint struct {
	inFlight    int       // tickets dispatched here, not yet settled or reaped
	newestStart float64   // highest start tag observed beginning service here
	lastStartAt time.Time // when the most recent start was observed
	haveStart   bool      // a start has been observed since the endpoint last went idle
}

// An endpoint exists in sfqState.endpoints only while it has work in flight.
// See release.

// sfqState is the shared virtual clock. One per plugin. The EPP is a single
// replica, so this is the one clock every request on the pool is tagged
// against. Two EPP replicas would each run their own clock and stamp tags that
// cannot be compared. That is recorded as a limitation in docs/design.md, not
// handled here.
type sfqState struct {
	mu        sync.Mutex
	v         float64
	nServing  int // endpoints in the min as of the last advanceV, for the gauge
	finish    map[string]float64
	endpoints map[string]*sfqEndpoint
	// pending is every unreaped ticket in dispatch order. Tickets are
	// appended at dispatch and dropped from the front once settled or reaped,
	// so the length is bounded by dispatch rate times settleTimeout.
	pending []*sfqTicket

	// wireBase is what the threshold rebase has subtracted from the internal
	// clock, in stamped (milli-tag) units. A stamp is wireBase plus the
	// quantised internal tag, so a rebase leaves every stamp exactly where it
	// would have been. See rebase.
	wireBase int64
	// epoch counts idle resets. A ticket from an earlier epoch settles
	// without touching the new epoch's finish tags.
	epoch uint64
	// lostUntil holds off the idle reset while a request presumed lost may
	// still be queued in vLLM with an old stamp. See resetIfIdle.
	lostUntil time.Time
	rebaseAt  float64

	settleTimeout time.Duration
	staleAfter    time.Duration
	// noTrueUp disables the completion true-up on the finish tag, and vMax
	// swaps V to the max-tag definition UNI-291 rejected. Tests only: they
	// exist so the CI sim can show each case it passes would fail without
	// the design choice it is guarding.
	noTrueUp bool
	vMax     bool
	// tabPick makes Pick order the EPP-held queue by the decayed tab, with the
	// newcomer clamp and the virtualTime ratchet, as it did before UNI-293's
	// review. Tests only: it is the "both notions live" arm the sim measures
	// against.
	tabPick bool
	// noIdleReset keeps V and F_g across an idle pool, as before UNI-300.
	// naiveRebase makes the threshold rebase move the stamp too, which is
	// what a rebase that forgot the tags already in vLLM's queue would do.
	// Tests only, for the same reason as noTrueUp.
	noIdleReset bool
	naiveRebase bool
}

func newSFQState(cfg *Config) *sfqState {
	return &sfqState{
		finish:        make(map[string]float64),
		endpoints:     make(map[string]*sfqEndpoint),
		rebaseAt:      sfqRebaseThreshold,
		settleTimeout: time.Duration(cfg.SFQSettleTimeoutSeconds * float64(time.Second)),
		staleAfter:    time.Duration(cfg.SFQEndpointStaleSeconds * float64(time.Second)),
	}
}

func (s *sfqState) endpoint(name string) *sfqEndpoint {
	ep, ok := s.endpoints[name]
	if !ok {
		ep = &sfqEndpoint{}
		s.endpoints[name] = ep
	}
	return ep
}

// serving reports whether an endpoint takes part in V.
//
// An endpoint counts only if it has work outstanding AND has been seen to
// start a request within staleAfter. Both conditions exist because the
// alternative is a V that stops advancing:
//
//   - Idle (nothing in flight): an endpoint with no work starts nothing, so
//     its newest start tag stays where it was. Left in the min, it would pin V
//     there until traffic returned to it. While V is pinned, every newly
//     dispatched tag is just its own group's F_g. A group returning from idle
//     would then restart from its old F_g, far behind everyone, and win every
//     queue position until it caught up. That is the burst the newcomer clamp
//     exists to stop on the tab.
//   - Stale (in flight but no start observed for staleAfter): an endpoint
//     that is wedged, or whose responses never reach the EPP. PreStop fails
//     100% on this cluster, and UNI-193 lost ~80% of dispatch accounting on
//     one path, so "never hear back" is an expected mode here, not a
//     hypothetical. The same freeze would follow.
//
// Leaving an endpoint out can never move V backwards: V only ever takes the
// max of itself and the min over serving endpoints. The cost of a stale
// window set too short is a slow but healthy endpoint dropping out between
// starts. V then advances on the faster endpoints alone, which moves the
// result toward the max-tag definition's heterogeneous error. The cost of a
// window set too long is that a wedged endpoint holds V that long. Either
// way the freeze is bounded.
//
// An endpoint going idle is dropped from the ledger entirely (see release),
// so it forgets its newest start. When work returns to it, it stays out of
// the min until it is seen to start something, rather than coming back with
// a stale tag.
func (s *sfqState) serving(ep *sfqEndpoint, now time.Time) bool {
	return ep.inFlight > 0 && ep.haveStart && now.Sub(ep.lastStartAt) <= s.staleAfter
}

// advanceV moves V up to the min over serving endpoints, if any serve. Caller
// holds s.mu.
func (s *sfqState) advanceV(now time.Time) {
	lo, n := math.Inf(1), 0
	for _, ep := range s.endpoints {
		if s.serving(ep, now) {
			if s.vMax && n > 0 {
				lo = math.Max(lo, ep.newestStart)
			} else {
				lo = math.Min(lo, ep.newestStart)
			}
			n++
		}
	}
	s.nServing = n
	if n > 0 && lo > s.v {
		s.v = lo
	}
}

// reap drops settled tickets from the front of pending, and charges worst
// for any ticket older than settleTimeout that never completed. Caller holds
// s.mu.
//
// This is the conservative failure the ticket asks for. A request whose
// completion is lost would otherwise keep only its dispatch estimate on the
// group's finish tag. The estimate is exactly what the tight-max_tokens
// vector drives low, so losing completions would make a group cheaper.
// Charging worst makes a lost completion cost at least as much as any
// completion could have. If the completion turns up after all, settle trues
// it down to the measured actual.
//
// Returns the groups charged, for the metric.
func (s *sfqState) reap(now time.Time) []string {
	var reaped []string
	i := 0
	for ; i < len(s.pending); i++ {
		t := s.pending[i]
		if t.settled {
			continue
		}
		if now.Sub(t.at) < s.settleTimeout {
			break
		}
		if extra := t.worst - t.charged; extra > 0 {
			s.finish[t.group] += extra / t.weight
			t.charged = t.worst
		}
		t.reaped = true
		s.release(t)
		reaped = append(reaped, t.group)
		s.lostUntil = now.Add(s.settleTimeout)
	}
	if i > 0 {
		s.pending = s.pending[i:]
	}
	return reaped
}

// rebase subtracts the integer part of V from V, from every finish tag and
// from every endpoint's newest start, and adds it to wireBase. In-flight
// tickets keep the wireBase they were tagged at, and observeStartLocked
// shifts their start by the difference. Caller holds s.mu. UNI-300.
//
// Every difference between tags is unchanged, so no group gains or loses
// anything. The stamp is unchanged too. That is the half that matters: vLLM
// already holds requests stamped on the old numbering, and it cannot be told
// to renumber them. Had the stamp dropped back towards zero, every request
// dispatched after the rebase would sort ahead of every request already
// waiting, and under sustained saturation those would wait until the
// saturation ended. TestSFQSimRebaseIsInvisible measures that arm.
//
// What the rebase buys is that the float64 tags stay small and exact, so the
// stamp can run on to vLLM's real ceiling, 2^63-1, rather than to the 2^53
// float64 can hold exactly. That is 1024 times the headroom. The subtraction
// is exact: d is an integer no greater than any live tag, and both sit far
// inside float64's integer range.
func (s *sfqState) rebase() {
	d := math.Floor(s.v)
	if d <= 0 {
		return
	}
	s.v -= d
	for g := range s.finish {
		s.finish[g] -= d
	}
	for _, ep := range s.endpoints {
		ep.newestStart -= d
	}
	s.wireBase = addSaturating(s.wireBase, int64(d)*sfqTagScale)
	sfqRebases.WithLabelValues("threshold").Inc()
}

// resetIfIdle starts a new epoch, V = 0 and every F_g = 0, once nothing is in
// flight anywhere. Caller holds s.mu. UNI-300.
//
// This is the busy-period rule of start-time fair queueing as published
// (Goyal, Vin and Cheng, 1996): at the end of a busy period V is set to the
// largest finish tag issued, which puts every flow level. Rebasing that to
// zero is the board's "numbers go back to 0". Without it V froze across the
// idle, and max(F_g, V) erased a group's stale credit but kept its stale
// debt: a group that was ahead when the pool went quiet started the next
// saturation episode behind. TestSFQSimIdleResetsTheLedger measures both
// arms.
//
// "Nothing in flight" is the ledger's own view: no endpoint has an unsettled,
// unreaped ticket. A request presumed lost holds the reset off for one more
// settleTimeout after it was reaped. It may still be queued in vLLM with an
// old, high stamp, and a fresh epoch would sort every new request ahead of
// it. The hold also keeps a lost request's worst-case charge on the books
// across a short idle, so losing completions stays unprofitable.
//
// The reset is also when the stamp returns to zero. Nothing is queued in
// vLLM to compare it against.
func (s *sfqState) resetIfIdle(now time.Time) {
	if s.noIdleReset || len(s.endpoints) > 0 || now.Before(s.lostUntil) {
		return
	}
	if s.v == 0 && s.wireBase == 0 && len(s.finish) == 0 {
		return
	}
	s.v, s.wireBase = 0, 0
	s.finish = make(map[string]float64)
	// Everything left in pending is settled or reaped, or an endpoint would
	// still be in flight.
	s.pending = nil
	s.epoch++
	sfqRebases.WithLabelValues("idle").Inc()
}

// release takes a ticket off its endpoint's in-flight count. Caller holds
// s.mu. An endpoint that drops to zero is deleted outright. That is the
// "forget the newest start on going idle" rule from serving, and it also
// keeps the map from accumulating every pod name a rollout ever produced.
func (s *sfqState) release(t *sfqTicket) {
	ep, ok := s.endpoints[t.endpoint]
	if !ok {
		return
	}
	if ep.inFlight--; ep.inFlight <= 0 {
		delete(s.endpoints, t.endpoint)
	}
}

// dispatch tags a request. est is the dispatch cost estimate and worst its
// bound.
func (s *sfqState) dispatch(now time.Time, group, endpoint string, weight, est, worst float64) (*sfqTicket, []string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	reaped := s.reap(now)
	s.resetIfIdle(now)
	s.advanceV(now)
	if s.v >= s.rebaseAt {
		s.rebase()
	}
	start := math.Max(s.finish[group], s.v)
	s.finish[group] = start + est/weight
	priority := addSaturating(s.wireBase, quantiseTag(start))
	if s.naiveRebase {
		priority = quantiseTag(start)
	}
	t := &sfqTicket{
		group: group, endpoint: endpoint, weight: weight,
		start: start, priority: priority, at: now,
		charged: est, worst: math.Max(worst, est), epoch: s.epoch, base: s.wireBase,
	}
	s.endpoint(endpoint).inFlight++
	s.pending = append(s.pending, t)
	return t, reaped
}

// nextStarts returns, for each group, the start tag its next dispatch would
// get: max(F_g, V). With the stamp on, this is what Pick orders the EPP-held
// queue by, so the EPP and vLLM's waiting queue rank requests by the same
// number. Both are then layers of one SFQ queue, not two policies stacked.
func (s *sfqState) nextStarts(now time.Time, groups []string) []float64 {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.resetIfIdle(now)
	s.advanceV(now)
	out := make([]float64, len(groups))
	for i, g := range groups {
		out[i] = math.Max(s.finish[g], s.v)
	}
	return out
}

// observeStart records that vLLM has begun serving t: the first response byte
// came back. For a streaming response that is the first token. For a
// non-streaming one it arrives with the completion, which is the "V from
// completions" variant UNI-290 round 2 found equally robust.
func (s *sfqState) observeStart(t *sfqTicket, now time.Time) {
	// Every streamed chunk lands here. Only the first one does anything, so
	// the rest must not contend on the pool-wide lock.
	if t.startSeen.Load() {
		return
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	s.observeStartLocked(t, now)
}

func (s *sfqState) observeStartLocked(t *sfqTicket, now time.Time) {
	if t.started {
		return
	}
	t.started = true
	t.startSeen.Store(true)
	if t.reaped || t.epoch != s.epoch {
		// Already off its endpoint's in-flight count; a start this late says
		// nothing about where the endpoint is now.
		return
	}
	ep, ok := s.endpoints[t.endpoint]
	if !ok {
		return
	}
	start := t.start - float64(s.wireBase-t.base)/sfqTagScale
	ep.newestStart = math.Max(ep.newestStart, start)
	ep.lastStartAt = now
	ep.haveStart = true
	s.advanceV(now)
}

// settle closes t at end of stream. With a measured actual, the finish tag is
// trued up by (actual - charged)/w, in either direction. A downward
// correction cannot buy priority over anyone, because S = max(F_g, V) never
// lets a group's next tag fall behind V. Without a usage block (an error
// status, a reset, a cancel, a server missing --enable-force-include-usage),
// whatever was charged stands. That is deliberately not the tab's UNI-213
// refund. A client that disconnects after receiving most of a stream must
// not get the tag back.
func (s *sfqState) settle(t *sfqTicket, now time.Time, actual float64, haveActual bool) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if t.settled {
		return
	}
	s.observeStartLocked(t, now)
	if haveActual && !s.noTrueUp && t.epoch == s.epoch {
		s.finish[t.group] += (actual - t.charged) / t.weight
		t.charged = actual
	}
	t.settled = true
	if !t.reaped {
		s.release(t)
	}
	s.advanceV(now)
}

// gauges reads what the per-request metric refresh needs, without building a
// full view: that runs on every dispatch and completion.
func (s *sfqState) gauges(group string) (v, finish float64, serving int) {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.v, s.finish[group], s.nServing
}

// sfqView is the ledger as seen by metrics, the debug dump and the flight
// recorder.
type sfqView struct {
	VirtualTime float64            `json:"virtualTime"`
	WireBase    int64              `json:"wireBase"`
	Epoch       uint64             `json:"epoch"`
	FinishTags  map[string]float64 `json:"finishTags"`
	Endpoints   []sfqEndpointView  `json:"endpoints"`
	Pending     int                `json:"pendingTickets"`
	Settings    map[string]float64 `json:"settings"`
}

type sfqEndpointView struct {
	Name        string  `json:"name"`
	InFlight    int     `json:"inFlight"`
	NewestStart float64 `json:"newestStart"`
	Serving     bool    `json:"serving"`
}

func (s *sfqState) view(now time.Time) sfqView {
	s.mu.Lock()
	defer s.mu.Unlock()
	v := sfqView{
		VirtualTime: s.v,
		WireBase:    s.wireBase,
		Epoch:       s.epoch,
		FinishTags:  make(map[string]float64, len(s.finish)),
		Pending:     len(s.pending),
		Settings: map[string]float64{
			"settleTimeoutSeconds": s.settleTimeout.Seconds(),
			"endpointStaleSeconds": s.staleAfter.Seconds(),
			"tagScale":             sfqTagScale,
			"rebaseThreshold":      s.rebaseAt,
		},
	}
	for g, f := range s.finish {
		v.FinishTags[g] = f
	}
	for name, ep := range s.endpoints {
		v.Endpoints = append(v.Endpoints, sfqEndpointView{
			Name: name, InFlight: ep.inFlight, NewestStart: ep.newestStart, Serving: s.serving(ep, now),
		})
	}
	sort.Slice(v.Endpoints, func(i, j int) bool { return v.Endpoints[i].Name < v.Endpoints[j].Name })
	return v
}

// targetEndpoint names the endpoint the scheduler picked: the primary
// profile's first target. "" when there is no result (a direct unit test). It
// is tracked like any other endpoint.
func targetEndpoint(result *fwksched.SchedulingResult) string {
	if result == nil {
		return ""
	}
	pr, ok := result.ProfileResults[result.PrimaryProfileName]
	if !ok || pr == nil || len(pr.TargetEndpoints) == 0 || pr.TargetEndpoints[0] == nil {
		return ""
	}
	md := pr.TargetEndpoints[0].GetMetadata()
	if md == nil {
		return ""
	}
	return md.GetNamespacedName().String()
}

// ---------------------------------------------------------------------------
// Startup assertion: requestHandler.propagatePriority must be off
// ---------------------------------------------------------------------------

// propagatePriorityProbe reports whether the EPP was configured with
// requestHandler.propagatePriority, and where it read that from. It is a
// variable so tests can stand in for the EPP's flag set.
var propagatePriorityProbe = probePropagatePriorityFromFlags

// probePropagatePriorityFromFlags re-reads the EndpointPickerConfig the runner
// itself loaded. The framework's plugin Handle does not expose
// propagatePriority, and the runner has already parsed the global flag set by
// the time any plugin Factory runs (runner.Run calls pflag.Parse before
// parseConfigurationPhaseOne). An unlocatable config is an error, not a pass:
// a check that cannot run must not report that it succeeded.
func probePropagatePriorityFromFlags() (bool, string, error) {
	var raw []byte
	var source string
	if f := pflag.CommandLine.Lookup("config-text"); f != nil && f.Value.String() != "" {
		raw, source = []byte(f.Value.String()), "--config-text"
	} else if f := pflag.CommandLine.Lookup("config-file"); f != nil && f.Value.String() != "" {
		b, err := os.ReadFile(f.Value.String())
		if err != nil {
			return false, f.Value.String(), fmt.Errorf("reading %s: %w", f.Value.String(), err)
		}
		raw, source = b, f.Value.String()
	} else {
		return false, "", fmt.Errorf("neither --config-file nor --config-text is set on this process")
	}
	return parsePropagatePriority(raw, source)
}

func parsePropagatePriority(raw []byte, source string) (bool, string, error) {
	var doc struct {
		RequestHandler *struct {
			PropagatePriority bool `json:"propagatePriority"`
		} `json:"requestHandler"`
	}
	if err := yaml.Unmarshal(raw, &doc); err != nil {
		return false, source, fmt.Errorf("parsing %s: %w", source, err)
	}
	return doc.RequestHandler != nil && doc.RequestHandler.PropagatePriority, source, nil
}

// checkPropagatePriorityOff is the startup assertion. propagatePriority runs
// in the director after PreRequest and rewrites `priority` to the
// InferenceObjective's static value, silently overwriting every tag this
// plugin stamps. Fairness would then switch off with no error anywhere. So
// with the stamp enabled, the EPP refuses to start instead.
func checkPropagatePriorityOff() (string, error) {
	on, source, err := propagatePriorityProbe()
	if err != nil {
		return source, fmt.Errorf("sfqPriorityStamp is on but requestHandler.propagatePriority could not be verified off: %w", err)
	}
	if on {
		return source, fmt.Errorf("sfqPriorityStamp is on but %s sets requestHandler.propagatePriority: true, "+
			"which overwrites every stamped tag after PreRequest; turn one of them off", source)
	}
	return source, nil
}
