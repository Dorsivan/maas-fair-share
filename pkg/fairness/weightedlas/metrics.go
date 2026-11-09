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
	"github.com/prometheus/client_golang/prometheus"
	compbasemetrics "k8s.io/component-base/metrics"

	metricsutil "github.com/llm-d/llm-d-router/pkg/common/observability/metrics"
	eppmetrics "github.com/llm-d/llm-d-router/pkg/epp/metrics"
)

// These are deliberately only the series that are not already derivable from
// the EPP's own fairness_id-labelled core metrics (llm_d_epp_request_input_tokens,
// _output_tokens, _cached_tokens, flow_control_queue_size,
// _request_queue_duration_seconds). Do not duplicate those here.
//
// Every fairness_id label value is routed through metricsutil.BoundFairnessID so
// this plugin shares the process-wide cardinality cap.
const metricPrefix = "maas_fairness_"

func help(msg string) string {
	return metricsutil.HelpMsgWithStability(msg, compbasemetrics.ALPHA)
}

var (
	// contendedServiceTokens and contendedSeconds are the numerator and
	// denominator of the real SLI. A raw throughput ratio is meaningless --
	// a group holding weight 20 while sending 5% of the traffic is behaving
	// correctly -- so the share is only counted over the time a group actually
	// had a queue while someone else did too.
	contendedServiceTokens = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "contended_service_tokens_total",
			Help:      help("Weighted service cost charged to a group while its priority band was contended."),
		}, []string{"fairness_id"})

	contendedSeconds = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "contended_seconds_total",
			Help:      help("Seconds during which a group was backlogged while at least one other group in its band was too."),
		}, []string{"fairness_id"})

	// normalizedService converges across backlogged groups when the policy is
	// healthy. A persistent outlier is being starved or is monopolising.
	normalizedService = prometheus.NewGaugeVec(
		prometheus.GaugeOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "normalized_service",
			Help:      help("Decayed attained service divided by configured weight. Equal across backlogged groups means the policy is converged."),
		}, []string{"fairness_id"})

	normalizedServiceObserved = prometheus.NewGaugeVec(
		prometheus.GaugeOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "normalized_service_observed",
			Help:      help("Normalized service accounted through an additional half-life that does not drive decisions."),
		}, []string{"fairness_id", "half_life_seconds"})

	configuredWeight = prometheus.NewGaugeVec(
		prometheus.GaugeOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "configured_weight",
			Help:      help("The group's weight as configured, echoed so dashboards compute expected-vs-observed without hand-copying it."),
		}, []string{"fairness_id"})

	dispatchTotal = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "dispatch_total",
			Help:      help("Requests dispatched per group. Divergence from the token share diagnoses the ordering-versus-floor caveat."),
		}, []string{"fairness_id"})

	// A high steady clamp rate means halfLifeSeconds is short relative to how
	// bursty the traffic is, not that the clamp is misbehaving.
	newcomerClamps = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "newcomer_clamps_total",
			Help:      help("Times a returning-idle group's tab was raised to the current band minimum."),
		}, []string{"fairness_id"})

	// Deliberately unlabelled by subscription string: that value is
	// attacker-controlled cardinality. The values go to the rate-limited log
	// line and the state dump instead.
	unmatchedSubscriptions = prometheus.NewCounter(
		prometheus.CounterOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "unmatched_subscriptions_total",
			Help:      help("Requests whose subscription ID matched no group rule and fell through to the catch-all."),
		})

	// Symmetric noise here is fine and self-correcting. A persistent per-group
	// bias is the signal: it means bytes-per-token is wrong for that group's
	// content (CJK runs 1-2 bytes/token; multimodal token counts have no
	// relation to JSON size at all).
	truingError = prometheus.NewHistogramVec(
		prometheus.HistogramOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "truing_error_tokens",
			Help:      help("Actual minus estimated request cost, in the configured cost unit."),
			Buckets:   []float64{-100000, -10000, -1000, -100, 0, 100, 1000, 10000, 100000},
		}, []string{"fairness_id"})

	// A regression detector, not a gauge of normal operation. With
	// --enable-force-include-usage set on every model server this is flat zero
	// forever; non-zero means a server shipped without it and that group's tab
	// is an estimate rather than a measurement. Alert on > 0.
	requestsWithoutUsage = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "requests_without_usage_total",
			Help:      help("Completed requests whose response carried no usage block, so no true-up was possible."),
		}, []string{"fairness_id"})

	// UNI-190: context-length rejections (HTTP 400, no usage block) are exempt
	// from provisional charging by board decision -- see responseStatusKey and
	// contextLengthStatusCode. This counts the reversed holds so the exemption
	// is visible in metrics rather than only inferable from a ledger that stops
	// leaking.
	provisionalChargesExempted = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "provisional_charges_exempted_total",
			Help:      help("Provisional charges reversed because the backend terminally rejected the request (context-length 400) before generating anything."),
		}, []string{"fairness_id"})

	// The headline shadow-mode reading: it decides whether
	// cachedInputTokenWeight is a real lever and in whose favour. A flat zero
	// across all groups means --enable-prompt-tokens-details is missing, not
	// that the cache is cold.
	cachedRatio = prometheus.NewGaugeVec(
		prometheus.GaugeOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "prompt_tokens_cached_ratio",
			Help:      help("Cumulative cached prompt tokens divided by total prompt tokens, per group."),
		}, []string{"fairness_id"})

	enforcingGauge = prometheus.NewGauge(
		prometheus.GaugeOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "enforcing",
			Help:      help("1 when the policy's pick is honoured, 0 in shadow mode."),
		})
)

func collectors() []prometheus.Collector {
	return []prometheus.Collector{
		contendedServiceTokens,
		contendedSeconds,
		normalizedService,
		normalizedServiceObserved,
		configuredWeight,
		dispatchTotal,
		newcomerClamps,
		unmatchedSubscriptions,
		truingError,
		requestsWithoutUsage,
		provisionalChargesExempted,
		cachedRatio,
		enforcingGauge,
	}
}

// boundID caps the label value against the process-wide fairness_id limit.
func boundID(id string) string { return metricsutil.BoundFairnessID(id) }
