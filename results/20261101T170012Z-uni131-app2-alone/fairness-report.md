# Fairness benchmark: app2-alone (uni131-app2-alone)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app2-alone` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T17:00:13Z` |
| Run end | `2026-11-01T17:04:26Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a |
| app2 | 10.0 | 32 | 5403 | 200=5385, 500=18 | 1.4 | 1.7 | 0.0 | n/a | n/a | n/a |
| end-users | 65.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app2: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 10.0 | 20.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 20.0 | 30.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 30.0 | 40.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 40.0 | 50.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 50.0 | 60.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 60.0 | 70.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 70.0 | 80.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 80.0 | 90.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 90.0 | 100.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 100.0 | 110.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 110.0 | 120.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 120.0 | 130.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 130.0 | 140.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 140.0 | 150.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 150.0 | 160.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 160.0 | 170.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 170.0 | 180.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 180.0 | 190.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 190.0 | 200.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 200.0 | 210.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 210.0 | 220.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 220.0 | 230.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 230.0 | 240.0 | app2 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 240.0 | 251.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 253.0 | app2 | False | 0.0 | n/a | n/a | n/a |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation.
