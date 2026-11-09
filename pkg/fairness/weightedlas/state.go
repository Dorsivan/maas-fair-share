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
	"math"
	"sync"
	"time"
)

// accumulator is a single exponentially-decaying total.
//
// Decay is lazy: nothing ticks, the value is simply aged to "now" whenever it is
// read or written. That is O(1), needs no bucket array, and composes -- adding a
// charge now and aging later gives the same answer as aging first.
type accumulator struct {
	value    float64
	halfLife float64 // seconds; 0 disables decay
	at       time.Time
}

// decayFactor is 2^(-elapsed/halfLife): the fraction of a charge placed
// `elapsed` seconds ago that still remains.
func (a *accumulator) decayFactor(elapsed float64) float64 {
	if a.halfLife <= 0 || elapsed <= 0 {
		return 1
	}
	return math.Exp2(-elapsed / a.halfLife)
}

func (a *accumulator) ageTo(now time.Time) {
	if a.at.IsZero() {
		a.at = now
		return
	}
	elapsed := now.Sub(a.at).Seconds()
	if elapsed <= 0 {
		// A non-monotonic clock must not inflate a tab.
		return
	}
	a.value *= a.decayFactor(elapsed)
	a.at = now
}

func (a *accumulator) read(now time.Time) float64 {
	a.ageTo(now)
	return a.value
}

func (a *accumulator) add(now time.Time, amount float64) {
	a.ageTo(now)
	a.value += amount
	if a.value < 0 {
		// A negative correction larger than what remains of the charge it
		// corrects can only come from double-counting. Clamping to zero keeps a
		// group from accruing credit it could spend later.
		a.value = 0
	}
}

func (a *accumulator) set(now time.Time, value float64) {
	a.ageTo(now)
	a.value = value
}

// groupState is everything the policy tracks per weighted group.
//
// There is exactly one of these per configured group, allocated at startup and
// never evicted: the group set is closed by configuration, every possible
// subscription ID resolves into it, and the states are a few hundred bytes each.
// That is also what bounds the fairness_id metric label by construction.
type groupState struct {
	name   string
	weight float64

	mu sync.Mutex
	// primary is the tab the policy actually orders on.
	primary accumulator
	// observed are the same charges accounted through other half-lives, reported
	// but never acted on. Parallel to Config.ObservedHalfLivesSeconds.
	observed []accumulator

	// ewmaOutput is a count-based mean of observed completion tokens; the mean
	// rather than the median because output lengths are right-skewed and often
	// bimodal, and we are estimating expected cost.
	ewmaOutput  float64
	ewmaSamples int

	inFlight         int64
	provisionalTotal float64

	promptTokensTotal float64
	cachedTokensTotal float64

	lastActivity time.Time
}

func newGroupState(name string, weight float64, halfLife float64, observedHalfLives []float64) *groupState {
	gs := &groupState{
		name:    name,
		weight:  weight,
		primary: accumulator{halfLife: halfLife},
	}
	for _, h := range observedHalfLives {
		gs.observed = append(gs.observed, accumulator{halfLife: h})
	}
	return gs
}

// charge adds `amount` to every accumulator as of `now`.
func (gs *groupState) charge(now time.Time, amount float64) {
	gs.mu.Lock()
	defer gs.mu.Unlock()
	gs.primary.add(now, amount)
	for i := range gs.observed {
		gs.observed[i].add(now, amount)
	}
	gs.lastActivity = now
}

// chargeInflight applies a true-up correction raised `inflight` seconds ago.
//
// The correction is decayed by the time the provisional charge has already spent
// decaying, which makes the resulting tab exactly identical to having charged
// the true value at dispatch. Adding the raw delta instead would attribute the
// estimate to dispatch time and the correction to completion time, so the final
// tab would depend on how wrong the estimate was -- estimator quality would leak
// into long-run fairness rather than affecting only in-flight ordering.
//
// Each accumulator decays the correction by its own half-life, so the observed
// windows stay exactly as self-consistent as the primary one.
func (gs *groupState) chargeInflight(now time.Time, delta, inflightSeconds float64) {
	gs.mu.Lock()
	defer gs.mu.Unlock()
	gs.primary.add(now, delta*gs.primary.decayFactor(inflightSeconds))
	for i := range gs.observed {
		gs.observed[i].add(now, delta*gs.observed[i].decayFactor(inflightSeconds))
	}
	gs.lastActivity = now
}

// normalizedService is A_i / w_i -- the quantity the policy equalises. The tab
// is stored raw and divided on read so that editing a weight does not
// retroactively rewrite history.
func (gs *groupState) normalizedService(now time.Time) float64 {
	gs.mu.Lock()
	defer gs.mu.Unlock()
	return gs.primary.read(now) / gs.weight
}

// setNormalizedService raises the tab so that A_i/w_i equals s. Used only by the
// newcomer clamp.
func (gs *groupState) setNormalizedService(now time.Time, s float64) {
	gs.mu.Lock()
	defer gs.mu.Unlock()
	gs.primary.set(now, s*gs.weight)
}

func (gs *groupState) observedNormalized(now time.Time) []float64 {
	gs.mu.Lock()
	defer gs.mu.Unlock()
	out := make([]float64, len(gs.observed))
	for i := range gs.observed {
		out[i] = gs.observed[i].read(now) / gs.weight
	}
	return out
}

// outputEWMA reports the group's observed mean output length, and whether it has
// seen enough completions to be trusted over the configured default.
func (gs *groupState) outputEWMA() (float64, bool) {
	gs.mu.Lock()
	defer gs.mu.Unlock()
	return gs.ewmaOutput, gs.ewmaSamples >= ewmaWarmupSamples
}

func (gs *groupState) recordCompletion(outputTokens, promptTokens, cachedTokens int) {
	gs.mu.Lock()
	defer gs.mu.Unlock()
	if gs.ewmaSamples == 0 {
		gs.ewmaOutput = float64(outputTokens)
	} else {
		gs.ewmaOutput += (float64(outputTokens) - gs.ewmaOutput) / ewmaAlphaDenominator
	}
	// Saturating: the counter only gates the warm-up test, so it must not wrap.
	if gs.ewmaSamples < ewmaWarmupSamples {
		gs.ewmaSamples++
	}
	gs.promptTokensTotal += float64(promptTokens)
	gs.cachedTokensTotal += float64(cachedTokens)
}

func (gs *groupState) cachedRatio() (float64, bool) {
	gs.mu.Lock()
	defer gs.mu.Unlock()
	if gs.promptTokensTotal <= 0 {
		return 0, false
	}
	return gs.cachedTokensTotal / gs.promptTokensTotal, true
}

func (gs *groupState) addInFlight(delta int64, provisional float64) {
	gs.mu.Lock()
	defer gs.mu.Unlock()
	gs.inFlight += delta
	if gs.inFlight < 0 {
		gs.inFlight = 0
	}
	gs.provisionalTotal += provisional
	if gs.provisionalTotal < 0 {
		gs.provisionalTotal = 0
	}
}

// snapshot is the per-group row in the debug dump and the flight-recorder log.
type snapshot struct {
	Name              string  `json:"name"`
	Weight            float64 `json:"weight"`
	AttainedService   float64 `json:"attainedService"`
	NormalizedService float64 `json:"normalizedService"`
	InFlight          int64   `json:"inFlight"`
	ProvisionalCharge float64 `json:"provisionalCharge"`
	EWMAOutputTokens  float64 `json:"ewmaOutputTokens"`
	EWMAWarm          bool    `json:"ewmaWarm"`
}

func (gs *groupState) snapshot(now time.Time) snapshot {
	gs.mu.Lock()
	defer gs.mu.Unlock()
	a := gs.primary.read(now)
	return snapshot{
		Name:              gs.name,
		Weight:            gs.weight,
		AttainedService:   a,
		NormalizedService: a / gs.weight,
		InFlight:          gs.inFlight,
		ProvisionalCharge: gs.provisionalTotal,
		EWMAOutputTokens:  gs.ewmaOutput,
		EWMAWarm:          gs.ewmaSamples >= ewmaWarmupSamples,
	}
}

// bandState is the per-priority-band state the Flyweight pattern requires. The
// plugin instance is a singleton shared across bands, so anything band-scoped
// lives here and is handed back through PriorityBandAccessor.PolicyState().
type bandState struct {
	mu sync.Mutex

	// virtualTime is the textbook V(t): the normalized service of the most
	// recent winner. It is half of the newcomer clamp floor, and the half that
	// handles a cold start where every group legitimately begins at zero.
	virtualTime float64

	// seq increments once per Pick. lastSeen records the seq at which each group
	// was last a candidate, which is how the empty->non-empty queue edge is
	// detected without scanning every group on every call.
	seq      int64
	lastSeen map[string]int64
	// lastSeenAt records the wall-clock time at which each group was last a
	// candidate, parallel to lastSeen. seq alone cannot tell a group that
	// returned after a genuine multi-second absence from one that returned on
	// the very next Pick call a millisecond later -- seq advances on every
	// Pick call, which the processor invokes on a ~1ms ticker and on every
	// enqueue from any group, not once per this group's own request (see
	// UNI-212, docs/design.md "UNI-212: the backlog edge was Pick-cadence-blind").
	lastSeenAt map[string]time.Time

	// lastContendedAt anchors the contended-seconds accounting: the SLI's
	// denominator is only the time a group actually had competition.
	lastContendedAt time.Time
}

func newBandState() *bandState {
	return &bandState{lastSeen: make(map[string]int64), lastSeenAt: make(map[string]time.Time)}
}

// beginPick advances the sequence and returns it.
func (bs *bandState) beginPick() int64 {
	bs.seq++
	return bs.seq
}

// isBacklogEdge reports whether this group's return counts as coming back
// from idle, for the newcomer clamp, and records it as present at (seq, now).
//
// A group present on the literal immediately-preceding Pick call is never an
// edge, regardless of timing -- this is the continuously-backlogged case, and
// it costs nothing to check first. Otherwise this is an edge only if at least
// idleThreshold of real wall-clock time has elapsed since the group was last
// a candidate, not merely "at least one Pick call": seq advances on every
// Pick call, which fires on a ~1ms ticker and on every enqueue from *any*
// group, so a gap of a few Pick calls can be a few milliseconds of real time,
// far short of a genuine return from idle. UNI-212 found the pure seq-based
// version firing on exactly that -- a well-served, higher-weight group
// draining its own queue to empty between bursts -- discarding the credit its
// weight had just earned it every time. idleThreshold <= 0 reproduces that
// previous behavior exactly (any seq gap at all is an edge), kept as an
// escape hatch rather than removed.
func (bs *bandState) isBacklogEdge(id string, seq int64, now time.Time, idleThreshold time.Duration) bool {
	prevSeq, seenBefore := bs.lastSeen[id]
	prevAt, hadTime := bs.lastSeenAt[id]
	bs.lastSeen[id] = seq
	bs.lastSeenAt[id] = now
	if !seenBefore {
		return true
	}
	if prevSeq == seq-1 {
		return false
	}
	if !hadTime {
		return true
	}
	return now.Sub(prevAt) >= idleThreshold
}

// pruneLastSeen drops groups that have been absent for a while. The map is
// bounded by the configured group count regardless, so this only keeps the
// iteration cheap; it is not a correctness requirement.
func (bs *bandState) pruneLastSeen(seq int64, candidates int) {
	if len(bs.lastSeen) <= 4*candidates+16 {
		return
	}
	for id, s := range bs.lastSeen {
		if s < seq-1 {
			delete(bs.lastSeen, id)
			delete(bs.lastSeenAt, id)
		}
	}
}

// contendedDelta returns the seconds to credit toward contended time for each
// backlogged group, and advances the anchor.
//
// maxContendedStep caps the credit from any single call so that a band resuming
// after an idle gap does not book the whole gap as contention.
func (bs *bandState) contendedDelta(now time.Time, maxStep time.Duration) float64 {
	if bs.lastContendedAt.IsZero() {
		bs.lastContendedAt = now
		return 0
	}
	d := now.Sub(bs.lastContendedAt)
	bs.lastContendedAt = now
	if d <= 0 {
		return 0
	}
	if d > maxStep {
		d = maxStep
	}
	return d.Seconds()
}
