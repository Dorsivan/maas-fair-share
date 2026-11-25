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

	// UNI-190 exempted context-length rejections (HTTP 400, no usage block)
	// from provisional charging; UNI-213 extended that to every no-usage
	// completion that never actually delivered anything -- any error status,
	// a stream reset, or a cancelled context. See responseStatusKey and
	// exemptionReason. The "reason" label tells the three apart so a ledger
	// that stops leaking doesn't hide which path did it.
	provisionalChargesExempted = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "provisional_charges_exempted_total",
			Help:      help("Provisional charges reversed because the request ended without ever delivering anything: an error status, a stream reset, or a cancelled context."),
		}, []string{"fairness_id", "reason"})

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

	// UNI-293 SFQ priority stamp. UNI-282 lost a day because the enforce
	// state could not be seen in the output. Every input to the stamp is
	// exported here so a live run can be debugged without a rebuild.
	sfqEnabledGauge = prometheus.NewGauge(
		prometheus.GaugeOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "sfq_enabled",
			Help:      help("1 when every request's vLLM priority is stamped with its SFQ start tag."),
		})

	sfqVirtualTime = prometheus.NewGauge(
		prometheus.GaugeOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "sfq_virtual_time",
			Help:      help("SFQ virtual time V in tag units (cost/weight): min over serving endpoints of the newest start tag. A flat line under load means V froze."),
		})

	sfqServingEndpoints = prometheus.NewGauge(
		prometheus.GaugeOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "sfq_serving_endpoints",
			Help:      help("Endpoints currently taking part in V: work in flight and a start observed within sfqEndpointStaleSeconds."),
		})

	sfqFinishTag = prometheus.NewGaugeVec(
		prometheus.GaugeOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "sfq_finish_tag",
			Help:      help("The group's SFQ finish tag F, in tag units. Its next request starts at max(F, V)."),
		}, []string{"fairness_id"})

	sfqLag = prometheus.NewGaugeVec(
		prometheus.GaugeOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "sfq_lag",
			Help:      help("Finish tag minus virtual time: how far ahead of the clock the group has been served. Negative means its next request starts at V."),
		}, []string{"fairness_id"})

	sfqStampedPriority = prometheus.NewGaugeVec(
		prometheus.GaugeOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "sfq_stamped_priority",
			Help:      help("The integer priority most recently written into a request body for the group (start tag x 1000, plus what threshold rebases have subtracted from the internal clock)."),
		}, []string{"fairness_id"})

	// Lost completions, charged at worst case. On a cluster where PreStop
	// always fails, this measures how much of the ledger runs on presumption.
	sfqUnsettled = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "sfq_unsettled_total",
			Help:      help("Requests with no completion observed within sfqSettleTimeoutSeconds, charged their worst-case cost on the finish tag."),
		}, []string{"fairness_id"})

	// UNI-300. Divided by sfq_unsettled_total, the share of reaped requests
	// that were not lost at all, only slower than sfqSettleTimeoutSeconds.
	sfqLateCompletions = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "sfq_late_completions_total",
			Help:      help("Requests charged worst-case by the reaper that then completed with a usage block: reaped while still legitimately queued or running."),
		}, []string{"fairness_id"})

	// UNI-300. Healthy endpoints land here between starts when
	// sfqEndpointStaleSeconds is short against mean service time over
	// effective concurrency.
	sfqStaleDropouts = prometheus.NewCounter(
		prometheus.CounterOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "sfq_stale_dropouts_total",
			Help:      help("Times an endpoint with work in flight left the virtual-time minimum because no start was observed within sfqEndpointStaleSeconds."),
		})

	// UNI-300. threshold: the internal clock was rebased, stamps unchanged.
	// idle: the pool emptied and a new epoch started from zero.
	sfqRebases = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "sfq_rebases_total",
			Help:      help("Virtual-clock rebases, by reason: threshold (internal clock rebased, stamps unchanged) or idle (the pool emptied, so V and every finish tag restarted at 0)."),
		}, []string{"reason"})

	sfqUnstampable = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "sfq_unstampable_total",
			Help:      help("Requests rejected because their body could not be rewritten to carry the priority stamp."),
		}, []string{"fairness_id"})

	// Non-zero means a client is setting `priority` itself, whether out of
	// ignorance or as an attempt. Either way it was removed or overwritten.
	clientPriorityOverwritten = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Subsystem: eppmetrics.LLMDRouterEndpointPickerSubsystem,
			Name:      metricPrefix + "client_priority_overwritten_total",
			Help:      help("Requests that arrived with a client-supplied priority field, which was stripped or overwritten."),
		}, []string{"fairness_id"})
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
		sfqEnabledGauge,
		sfqVirtualTime,
		sfqServingEndpoints,
		sfqFinishTag,
		sfqLag,
		sfqStampedPriority,
		sfqUnsettled,
		sfqRebases,
		sfqLateCompletions,
		sfqStaleDropouts,
		sfqUnstampable,
		clientPriorityOverwritten,
	}
}

// boundID caps the label value against the process-wide fairness_id limit.
func boundID(id string) string { return metricsutil.BoundFairnessID(id) }
