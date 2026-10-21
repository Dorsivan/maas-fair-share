#!/usr/bin/env python3
"""Diff two llm_d_epp_maas_fairness_* /metrics snapshots (Prometheus text
format, comment lines already stripped) and print the per-series delta.
Used by 13-loadgen-poisson.sh to isolate one run's contribution from the
cumulative counters. Counters only increase, so a negative delta means the
EPP restarted between snapshots and the comparison is invalid."""
import sys


# Only these are true monotonic counters (modulo a histogram's own negative
# observations, which this plugin deliberately allows for truing_error_tokens
# -- see metrics.go). A negative delta on one of THESE means the EPP
# restarted between snapshots, not legitimate movement. normalized_service*,
# configured_weight, enforcing and prompt_tokens_cached_ratio are gauges and
# move in both directions normally; truing_error_tokens_sum is a running sum
# of signed values and is not monotonic either.
MONOTONIC_PREFIXES = (
    "llm_d_epp_maas_fairness_dispatch_total",
    "llm_d_epp_maas_fairness_contended_service_tokens_total",
    "llm_d_epp_maas_fairness_contended_seconds_total",
    "llm_d_epp_maas_fairness_newcomer_clamps_total",
    "llm_d_epp_maas_fairness_unmatched_subscriptions_total",
    "llm_d_epp_maas_fairness_requests_without_usage_total",
    "llm_d_epp_maas_fairness_truing_error_tokens_bucket",
    "llm_d_epp_maas_fairness_truing_error_tokens_count",
)


def parse(path):
    out = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name_labels, val = line.rsplit(" ", 1)
            out[name_labels] = float(val)
    return out


def main():
    before_path, after_path = sys.argv[1], sys.argv[2]
    before = parse(before_path)
    after = parse(after_path)
    for key in sorted(after):
        if key not in before:
            print(f"{key} NEW={after[key]:g}")
            continue
        d = after[key] - before[key]
        if d != 0:
            is_monotonic = key.startswith(MONOTONIC_PREFIXES)
            flag = " (NEGATIVE -- EPP likely restarted)" if (d < 0 and is_monotonic) else ""
            print(f"{key} {d:g}{flag}")


if __name__ == "__main__":
    main()
