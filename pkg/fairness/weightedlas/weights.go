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
	"fmt"
	"strings"
)

// Cost model identifiers accepted by Config.CostModel.
const (
	// CostModelTokens denominates the tab in weighted tokens. It matches the unit
	// Kuadrant's TokenRateLimitPolicy counts in and the unit every vLLM dashboard
	// reports, which is why it is the default.
	CostModelTokens = "tokens"
	// CostModelVRAMTime denominates the tab in token-steps of KV residency,
	// O*(P+O/2). Specified but not recommended; see docs/design.md Part 3 item 9.
	CostModelVRAMTime = "vramtime"
)

// GroupMatch selects subscription IDs for a group. Exact matches are tested
// before prefixes, across all groups, so an explicitly named subscription can
// never be captured by another group's prefix.
type GroupMatch struct {
	Exact  []string `json:"exact,omitempty"`
	Prefix []string `json:"prefix,omitempty"`
}

// GroupConfig is one weighted group: a name, a share, and the subscription IDs
// that resolve to it.
type GroupConfig struct {
	Name   string     `json:"name"`
	Weight float64    `json:"weight"`
	Match  GroupMatch `json:"match,omitempty"`
}

// DefaultGroupConfig is the catch-all for subscription IDs that match no group,
// including the empty ID of unauthenticated traffic. It is the reason the
// fairness_id label has bounded cardinality: every possible input collapses onto
// one of the configured names.
type DefaultGroupConfig struct {
	Name   string  `json:"name"`
	Weight float64 `json:"weight"`
}

// Config is the plugin's `parameters` block in the EndpointPickerConfig. The
// framework decodes it with DisallowUnknownFields, so a typo in a key is a
// startup failure rather than a silently defaulted value.
type Config struct {
	// IdentityHeader is the request header carrying the authenticated
	// subscription ID. Matched case-insensitively.
	IdentityHeader string `json:"identityHeader,omitempty"`

	Groups       []GroupConfig      `json:"groups,omitempty"`
	DefaultGroup DefaultGroupConfig `json:"defaultGroup,omitempty"`

	// Enforce false is shadow mode: classify, account and publish every metric,
	// but return the FCFS pick so live dispatch order is unchanged.
	Enforce bool `json:"enforce"`

	// StateLogIntervalSeconds is the flight-recorder cadence. The line is emitted
	// only while contended, so an idle cluster stays silent. 0 disables.
	StateLogIntervalSeconds float64 `json:"stateLogIntervalSeconds,omitempty"`

	// HalfLifeSeconds is the decay constant of the tab. 0 disables decay, which
	// makes the tab cumulative since process start -- almost never what you want.
	HalfLifeSeconds float64 `json:"halfLifeSeconds,omitempty"`

	// ObservedHalfLivesSeconds are additional half-lives accounted and reported
	// but never acted on. They observe the actual request stream through a
	// different smoothing window; they do not simulate what that window would
	// have decided.
	ObservedHalfLivesSeconds []float64 `json:"observedHalfLivesSeconds,omitempty"`

	CostModel              string  `json:"costModel,omitempty"`
	InputTokenWeight       float64 `json:"inputTokenWeight,omitempty"`
	OutputTokenWeight      float64 `json:"outputTokenWeight,omitempty"`
	CachedInputTokenWeight float64 `json:"cachedInputTokenWeight,omitempty"`

	// NewcomerClamp raises a returning-idle group's tab to the current minimum on
	// the empty->non-empty queue edge. Exposed as a flag only so the load test can
	// be run both ways; turning it off re-couples fairness to idleness.
	NewcomerClamp bool `json:"newcomerClamp"`

	// NewcomerClampIdleSeconds is the minimum wall-clock time a group must have
	// been absent from Pick candidacy before its return counts as an "edge" for
	// the newcomer clamp above. UNI-212: without this gate, the edge was keyed
	// to the shared Pick-call sequence alone, which advances on every Pick call
	// (a ~1ms ticker, plus every enqueue from any group) rather than once per
	// this group's own request -- so a group efficiently served enough to drain
	// its own queue between bursts registered as "away" on a millisecond
	// timescale, and got its earned tab overwritten with the current floor every
	// time. 2s is comfortably above that kind of dispatch-driven churn and
	// comfortably below the tens-of-seconds absence the clamp exists to catch
	// (one halfLifeSeconds is 60s by default). <= 0 reproduces the previous
	// (buggy) seq-only behavior exactly.
	NewcomerClampIdleSeconds float64 `json:"newcomerClampIdleSeconds,omitempty"`

	// ProvisionalCharge charges an estimate at dispatch and trues it up against
	// the response's usage block. Without it the policy is blind for the whole
	// duration of a generation.
	ProvisionalCharge            bool    `json:"provisionalCharge"`
	DefaultEstimatedOutputTokens float64 `json:"defaultEstimatedOutputTokens,omitempty"`
	EstimatedBytesPerToken       float64 `json:"estimatedBytesPerToken,omitempty"`

	// AgingTokensPerSecond subtracts head-of-line wait from the score in raw
	// units. 0 is pure proportional ordering.
	AgingTokensPerSecond float64 `json:"agingTokensPerSecond,omitempty"`

	// EmitAttributionHeaders controls whether x-request-id, x-maas-fairness-group
	// and x-maas-fairness-queue-ms are set on the response. It is a tenant's own
	// classification at zero log volume and no cluster access, but it is also
	// internal detail some deployments may not want to expose -- see
	// docs/design.md "Per-request attribution".
	EmitAttributionHeaders bool `json:"emitAttributionHeaders"`

	// RequestTierV4SampleEvery turns on the V(4) per-request tier (group
	// resolved, estimate charged, true-up delta -- see docs/design.md "V(4)
	// per-request tier") and sets its sample rate: one line is emitted for
	// every RequestTierV4SampleEvery-th settlement, the rest are skipped
	// entirely. 0 (the default) means the tier never emits, regardless of
	// process verbosity -- Pick runs on a ~1ms ticker and unsampled per-request
	// logging is out of scope for this plugin, always. This field is read once
	// from the static `parameters` block at plugin construction (see Factory)
	// and cannot be changed without a redeploy; the line still requires `-v=4`
	// or higher on the EPP process, which is set the same, redeploy-only way.
	RequestTierV4SampleEvery uint64 `json:"requestTierV4SampleEvery,omitempty"`

	// RequestTierV4TimeBoxSeconds bounds how long after this plugin starts
	// sampling the V(4) tier may keep emitting at all. Once the window
	// elapses the tier goes silent on its own -- even if RequestTierV4SampleEvery
	// and -v=4 are both still set -- so raising verbosity for one debugging
	// session cannot be left on by accident indefinitely. Required (> 0) when
	// RequestTierV4SampleEvery is set.
	RequestTierV4TimeBoxSeconds float64 `json:"requestTierV4TimeBoxSeconds,omitempty"`
}

// DefaultConfig is what the plugin does with an empty parameters block: shadow
// mode, undiscounted tokens, a 60s half-life, and a single catch-all group. The
// zero-valued booleans in Config are deliberately not `omitempty`, so an explicit
// `enforce: false` is indistinguishable from omission -- which is the safe
// direction for all three of them.
func DefaultConfig() Config {
	return Config{
		IdentityHeader:               "x-maas-subscription-id",
		DefaultGroup:                 DefaultGroupConfig{Name: "unclassified", Weight: 1},
		Enforce:                      false,
		StateLogIntervalSeconds:      30,
		HalfLifeSeconds:              60,
		CostModel:                    CostModelTokens,
		InputTokenWeight:             1.0,
		OutputTokenWeight:            2.0,
		CachedInputTokenWeight:       1.0,
		NewcomerClamp:                true,
		NewcomerClampIdleSeconds:     2.0,
		ProvisionalCharge:            true,
		DefaultEstimatedOutputTokens: 512,
		EstimatedBytesPerToken:       4,
		AgingTokensPerSecond:         0,
		EmitAttributionHeaders:       true,
	}
}

func (c *Config) validate() error {
	if c.IdentityHeader == "" {
		return fmt.Errorf("identityHeader must not be empty")
	}
	if c.DefaultGroup.Name == "" {
		return fmt.Errorf("defaultGroup.name must not be empty")
	}
	if c.DefaultGroup.Weight <= 0 {
		return fmt.Errorf("defaultGroup.weight must be > 0, got %v", c.DefaultGroup.Weight)
	}

	seen := map[string]bool{c.DefaultGroup.Name: true}
	for i, g := range c.Groups {
		if g.Name == "" {
			return fmt.Errorf("groups[%d].name must not be empty", i)
		}
		if seen[g.Name] {
			return fmt.Errorf("groups[%d]: duplicate group name %q", i, g.Name)
		}
		seen[g.Name] = true
		// A zero weight is not "never serve me", it is a division by zero. Reject
		// it rather than let it become +Inf and silently starve the group forever.
		if g.Weight <= 0 {
			return fmt.Errorf("groups[%d] (%s): weight must be > 0, got %v", i, g.Name, g.Weight)
		}
		if len(g.Match.Exact) == 0 && len(g.Match.Prefix) == 0 {
			return fmt.Errorf("groups[%d] (%s): match must set at least one of exact or prefix", i, g.Name)
		}
		for _, p := range g.Match.Prefix {
			if p == "" {
				return fmt.Errorf("groups[%d] (%s): empty prefix matches everything", i, g.Name)
			}
		}
	}

	if c.HalfLifeSeconds < 0 {
		return fmt.Errorf("halfLifeSeconds must be >= 0, got %v", c.HalfLifeSeconds)
	}
	for i, h := range c.ObservedHalfLivesSeconds {
		if h <= 0 {
			return fmt.Errorf("observedHalfLivesSeconds[%d] must be > 0, got %v", i, h)
		}
	}
	if c.StateLogIntervalSeconds < 0 {
		return fmt.Errorf("stateLogIntervalSeconds must be >= 0, got %v", c.StateLogIntervalSeconds)
	}

	switch c.CostModel {
	case CostModelTokens, CostModelVRAMTime:
	default:
		return fmt.Errorf("costModel must be %q or %q, got %q", CostModelTokens, CostModelVRAMTime, c.CostModel)
	}
	if c.InputTokenWeight < 0 {
		return fmt.Errorf("inputTokenWeight must be >= 0, got %v", c.InputTokenWeight)
	}
	if c.OutputTokenWeight < 0 {
		return fmt.Errorf("outputTokenWeight must be >= 0, got %v", c.OutputTokenWeight)
	}
	// 0 is an exemption, not a discount: unlimited cached-prefix traffic at zero
	// tab cost. Prefill slots are real even when the compute is skipped.
	if c.CachedInputTokenWeight <= 0 {
		return fmt.Errorf("cachedInputTokenWeight must be > 0 (0 is an exemption, not a discount), got %v",
			c.CachedInputTokenWeight)
	}
	if c.DefaultEstimatedOutputTokens < 0 {
		return fmt.Errorf("defaultEstimatedOutputTokens must be >= 0, got %v", c.DefaultEstimatedOutputTokens)
	}
	if c.EstimatedBytesPerToken <= 0 {
		return fmt.Errorf("estimatedBytesPerToken must be > 0, got %v", c.EstimatedBytesPerToken)
	}
	if c.AgingTokensPerSecond < 0 {
		return fmt.Errorf("agingTokensPerSecond must be >= 0, got %v", c.AgingTokensPerSecond)
	}
	if c.RequestTierV4TimeBoxSeconds < 0 {
		return fmt.Errorf("requestTierV4TimeBoxSeconds must be >= 0, got %v", c.RequestTierV4TimeBoxSeconds)
	}
	if c.RequestTierV4SampleEvery > 0 && c.RequestTierV4TimeBoxSeconds <= 0 {
		return fmt.Errorf("requestTierV4TimeBoxSeconds must be > 0 when requestTierV4SampleEvery is set, got %v",
			c.RequestTierV4TimeBoxSeconds)
	}
	return nil
}

// groupTable resolves a subscription ID to a group name and a weight.
//
// The resolution is what collapses many subscriptions onto one weight: without
// it, each end-user subscription would own a separate flow queue holding a
// separate copy of the end-user weight, and the group's total share would grow
// with every subscription added.
type groupTable struct {
	exact    map[string]string // subscription ID -> group name
	prefixes []prefixRule      // longest prefix first
	weights  map[string]float64
	order    []string // config order, default group last; stable output ordering
	fallback string
}

type prefixRule struct {
	prefix string
	group  string
}

func newGroupTable(c *Config) (*groupTable, error) {
	t := &groupTable{
		exact:    make(map[string]string, len(c.Groups)),
		weights:  make(map[string]float64, len(c.Groups)+1),
		fallback: c.DefaultGroup.Name,
	}
	for _, g := range c.Groups {
		t.weights[g.Name] = g.Weight
		t.order = append(t.order, g.Name)
		for _, id := range g.Match.Exact {
			if prev, dup := t.exact[id]; dup {
				return nil, fmt.Errorf("subscription %q is claimed by both %q and %q", id, prev, g.Name)
			}
			t.exact[id] = g.Name
		}
		for _, p := range g.Match.Prefix {
			t.prefixes = append(t.prefixes, prefixRule{prefix: p, group: g.Name})
		}
	}
	t.weights[c.DefaultGroup.Name] = c.DefaultGroup.Weight
	t.order = append(t.order, c.DefaultGroup.Name)

	// Longest prefix wins, so "end-user-vip-" can carve a group out of
	// "end-user-" regardless of the order the two appear in the ConfigMap.
	for i := 1; i < len(t.prefixes); i++ {
		for j := i; j > 0 && len(t.prefixes[j].prefix) > len(t.prefixes[j-1].prefix); j-- {
			t.prefixes[j], t.prefixes[j-1] = t.prefixes[j-1], t.prefixes[j]
		}
	}
	for i := 1; i < len(t.prefixes); i++ {
		if t.prefixes[i].prefix == t.prefixes[i-1].prefix {
			return nil, fmt.Errorf("prefix %q is claimed by both %q and %q",
				t.prefixes[i].prefix, t.prefixes[i-1].group, t.prefixes[i].group)
		}
	}
	return t, nil
}

// resolve maps a subscription ID to a group name. The second return value
// reports whether a rule matched; false means the ID fell through to the
// catch-all, which is the signal that a subscription was added without a
// matching rule (or that its name has a typo).
func (t *groupTable) resolve(subscriptionID string) (string, bool) {
	if subscriptionID == "" {
		return t.fallback, false
	}
	if name, ok := t.exact[subscriptionID]; ok {
		return name, true
	}
	for _, r := range t.prefixes {
		if strings.HasPrefix(subscriptionID, r.prefix) {
			return r.group, true
		}
	}
	return t.fallback, false
}

// weight returns the configured weight for a group name. Flow IDs reaching Pick
// should always be names this table knows, but flow control will happily create
// a queue for any ID -- including one set by a plugin we do not control -- so an
// unknown name gets the catch-all weight rather than a zero that would divide by
// zero and starve it permanently.
func (t *groupTable) weight(name string) float64 {
	if w, ok := t.weights[name]; ok {
		return w
	}
	return t.weights[t.fallback]
}

func (t *groupTable) names() []string { return t.order }
