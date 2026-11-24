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

// maxStampedPriority keeps the quantised tag inside float64's exact-integer
// range, so the conversion to int64 can neither round nor overflow. At
// sfqTagScale this is ~9e12 tag units. That is centuries of virtual time at
// any plausible pool throughput.
const maxStampedPriority = int64(1) << 53

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
	if q >= float64(maxStampedPriority) {
		return maxStampedPriority
	}
	return int64(q)
}

// sfqTicket is one dispatched request's entry in the SFQ ledger.
type sfqTicket struct {
	group    string
	endpoint string
	weight   float64
	start    float64 // S, in tag units (cost / weight)
	priority int64   // the value actually stamped
	at       time.Time
	// charged is the cost currently booked to the group's finish tag for this
	// request. The dispatch estimate first, then worst if reaped, then the
	// measured actual if a usage block arrives.
	charged float64
	// worst is the request's cost if every allowed token is generated. It is
	// what a request is charged when its completion is never observed.
	worst float64

	started bool // a response byte has come back, so vLLM has begun serving it
	settled bool // ResponseBody's end-of-stream ran
	reaped  bool // settleTimeout passed with no completion, so worst was charged
}

// sfqEndpoint is the ledger's view of one model server.
type sfqEndpoint struct {
	inFlight    int       // tickets dispatched here, not yet settled or reaped
	newestStart float64   // highest start tag observed beginning service here
	lastStartAt time.Time // when the most recent start was observed
	haveStart   bool      // a start has been observed since the endpoint last went idle
}

// sfqState is the shared virtual clock. One per plugin. The EPP is a single
// replica, so this is the one clock every request on the pool is tagged
// against. Two EPP replicas would each run their own clock and stamp tags that
// cannot be compared. That is recorded as a limitation in docs/design.md, not
// handled here.
type sfqState struct {
	mu        sync.Mutex
	v         float64
	finish    map[string]float64
	endpoints map[string]*sfqEndpoint
	// pending is every unreaped ticket in dispatch order. Tickets are
	// appended at dispatch and dropped from the front once settled or reaped,
	// so the length is bounded by dispatch rate times settleTimeout.
	pending []*sfqTicket

	settleTimeout time.Duration
	staleAfter    time.Duration
	// noTrueUp disables the completion true-up on the finish tag. Tests only:
	// it exists so the CI sim can show the tight-max_tokens vector is real.
	noTrueUp bool
}

func newSFQState(cfg *Config) *sfqState {
	return &sfqState{
		finish:        make(map[string]float64),
		endpoints:     make(map[string]*sfqEndpoint),
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
// An endpoint going idle also forgets its newest start (haveStart false).
// When work returns to it, it stays out of the min until it is seen to start
// something, rather than coming back with a stale tag.
func (s *sfqState) serving(ep *sfqEndpoint, now time.Time) bool {
	return ep.inFlight > 0 && ep.haveStart && now.Sub(ep.lastStartAt) <= s.staleAfter
}

// advanceV moves V up to the min over serving endpoints, if any serve. Caller
// holds s.mu.
func (s *sfqState) advanceV(now time.Time) {
	lo, found := math.Inf(1), false
	for _, ep := range s.endpoints {
		if s.serving(ep, now) {
			lo, found = math.Min(lo, ep.newestStart), true
		}
	}
	if found && lo > s.v {
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
	}
	if i > 0 {
		s.pending = s.pending[i:]
	}
	return reaped
}

// release takes a ticket off its endpoint's in-flight count. Caller holds s.mu.
func (s *sfqState) release(t *sfqTicket) {
	ep := s.endpoint(t.endpoint)
	if ep.inFlight > 0 {
		ep.inFlight--
	}
	if ep.inFlight == 0 {
		ep.haveStart = false
	}
}

// dispatch tags a request. est is the dispatch cost estimate and worst its
// bound.
func (s *sfqState) dispatch(now time.Time, group, endpoint string, weight, est, worst float64) (*sfqTicket, []string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	reaped := s.reap(now)
	s.advanceV(now)
	start := math.Max(s.finish[group], s.v)
	s.finish[group] = start + est/weight
	t := &sfqTicket{
		group: group, endpoint: endpoint, weight: weight,
		start: start, priority: quantiseTag(start), at: now,
		charged: est, worst: math.Max(worst, est),
	}
	s.endpoint(endpoint).inFlight++
	s.pending = append(s.pending, t)
	return t, reaped
}

// observeStart records that vLLM has begun serving t: the first response byte
// came back. For a streaming response that is the first token. For a
// non-streaming one it arrives with the completion, which is the "V from
// completions" variant UNI-290 round 2 found equally robust.
func (s *sfqState) observeStart(t *sfqTicket, now time.Time) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.observeStartLocked(t, now)
}

func (s *sfqState) observeStartLocked(t *sfqTicket, now time.Time) {
	if t.started {
		return
	}
	t.started = true
	if t.reaped {
		// Already off its endpoint's in-flight count; a start this late says
		// nothing about where the endpoint is now.
		return
	}
	ep := s.endpoint(t.endpoint)
	ep.newestStart = math.Max(ep.newestStart, t.start)
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
	if haveActual && !s.noTrueUp {
		s.finish[t.group] += (actual - t.charged) / t.weight
		t.charged = actual
	}
	t.settled = true
	if !t.reaped {
		s.release(t)
	}
	s.advanceV(now)
}

// sfqView is the ledger as seen by metrics, the debug dump and the flight
// recorder.
type sfqView struct {
	VirtualTime float64            `json:"virtualTime"`
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
		FinishTags:  make(map[string]float64, len(s.finish)),
		Pending:     len(s.pending),
		Settings: map[string]float64{
			"settleTimeoutSeconds": s.settleTimeout.Seconds(),
			"endpointStaleSeconds": s.staleAfter.Seconds(),
			"tagScale":             sfqTagScale,
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
