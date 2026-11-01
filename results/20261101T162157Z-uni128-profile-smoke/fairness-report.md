# Fairness benchmark: app1-alone (uni128-profile-smoke)

**Verdict: FAIL** (threshold: 10 points)

- app1 is the only offered group this run (no contention is possible, so contended_service_tokens_total is correctly zero -- not evaluated as a share) but only 61.9% of its 454 requests succeeded, short of the 90% bar for 'receives ~100% of the pool'

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-alone` |
| Enforce | `True` |
| Duration (s) | `90` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T16:21:59Z` |
| Run end | `2026-11-01T16:25:40Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 454 | 000=32, 200=281, 400=33, 500=17 | 0.8 | 120.0 | 0.0 | n/a | n/a | n/a |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a |
| end-users | 65.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-90s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 90.0 | n/a (never converged in this phase) | n/a |

**Windows** (23 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 10.0 | 20.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 20.0 | 30.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 30.0 | 40.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 40.0 | 50.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 50.0 | 60.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 60.0 | 70.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 70.0 | 80.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 80.0 | 90.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 90.0 | 100.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 100.0 | 110.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 130.0 | 140.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 140.0 | 150.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 150.0 | 160.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 160.0 | 170.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 170.0 | 180.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 180.0 | 190.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 190.0 | 200.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 200.0 | 210.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 210.0 | 220.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 220.0 | 221.0 | app1 | False | 0.0 | n/a | n/a | n/a |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation.
