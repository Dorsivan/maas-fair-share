# Fairness benchmark: b5-open-loop-above-saturation (uni-137-b5-above-saturation)

**Verdict: FAIL** (threshold: 10 points)

- end-users deviated -18.8 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `b5-open-loop-above-saturation` |
| Generator | `open-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T19:06:13Z` |
| Run end | `2026-11-01T19:11:36Z` |

## Per-group result

| group | weight | offered req/s | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 8.4 | 2052 | 0=1316, 200=736 | 50.0 | 50.0 | 1723692.0 | 21.1% | 32.4% | 11.3 | 23.9s | 98.0% | 1394.0 |
| app2 | 10.0 | 8.4 | 1976 | 0=1572, 200=404 | 50.0 | 50.0 | 959058.0 | 10.5% | 18.0% | 7.5 | 24.0s | 93.6% | 781.0 |
| end-users | 65.0 | 8.4 | 1982 | 0=932, 200=1050 | 46.8 | 50.0 | 2643480.0 | 68.4% | 49.6% | -18.8 | 21.5s | 98.9% | 1982.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 23.3% | 0.0 |

## Timeline (UNI-127)

N/A: no `--metrics-timeseries` recorded for this run (older report, or the benchmark script predates UNI-127).

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/13-loadgen-poisson.py's own stdout (UNI-137/B5): the 'load: open-loop Poisson arrivals rate ...' line for each offered group's Poisson arrival rate in req/s -- NOT a worker count, this generator is open-loop -- and each group's own 'sent=... completion_tokens=... p50=...s p95=...s p99=...s codes=[...]' summary line for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
