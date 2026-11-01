# Fairness benchmark: end-users-idle (uni139-end-users-idle-r2)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `end-users-idle` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T20:10:25Z` |
| Run end | `2026-11-01T20:19:30Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 64 | 2412 | 200=2394, 500=18 | 7.2 | 8.6 | 3115348.0 | 66.7% | 70.7% | 4.1 | 1.5s | 98.5% | 2394.0 |
| app2 | 10.0 | 32 | 985 | 000=1, 200=967, 500=17 | 7.5 | 11.4 | 1288657.0 | 33.3% | 29.3% | -4.1 | 1.5s | 96.8% | 968.0 |
| end-users | 65.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 98.9% | 0.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 90.2% | 0.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 231.0 | 231.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (55 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 86618.0 | 66.7% | 56.6% | -10.1 |
| 0.0 | 10.0 | app2 | True | 66392.0 | 33.3% | 43.4% | 10.1 |
| 10.0 | 20.0 | app1 | True | 133878.0 | 66.7% | 80.5% | 13.8 |
| 10.0 | 20.0 | app2 | True | 32476.0 | 33.3% | 19.5% | -13.8 |
| 20.0 | 30.0 | app1 | True | 129842.0 | 66.7% | 69.1% | 2.4 |
| 20.0 | 30.0 | app2 | True | 58144.0 | 33.3% | 30.9% | -2.4 |
| 30.0 | 40.0 | app1 | True | 148722.0 | 66.7% | 77.4% | 10.8 |
| 30.0 | 40.0 | app2 | True | 43354.0 | 33.3% | 22.6% | -10.8 |
| 40.0 | 50.0 | app1 | True | 134062.0 | 66.7% | 75.6% | 8.9 |
| 40.0 | 50.0 | app2 | True | 43288.0 | 33.3% | 24.4% | -8.9 |
| 50.0 | 60.0 | app1 | True | 117512.0 | 66.7% | 64.9% | -1.8 |
| 50.0 | 60.0 | app2 | True | 63610.0 | 33.3% | 35.1% | 1.8 |
| 60.0 | 70.0 | app1 | True | 146214.0 | 66.7% | 77.7% | 11.0 |
| 60.0 | 70.0 | app2 | True | 41962.0 | 33.3% | 22.3% | -11.0 |
| 70.0 | 80.0 | app1 | True | 120310.0 | 66.7% | 65.4% | -1.2 |
| 70.0 | 80.0 | app2 | True | 63544.0 | 33.3% | 34.6% | 1.2 |
| 80.0 | 90.0 | app1 | True | 127334.0 | 66.7% | 74.0% | 7.4 |
| 80.0 | 90.0 | app2 | True | 44688.0 | 33.3% | 26.0% | -7.4 |
| 90.0 | 100.0 | app1 | True | 147394.0 | 66.7% | 77.9% | 11.2 |
| 90.0 | 100.0 | app2 | True | 41900.0 | 33.3% | 22.1% | -11.2 |
| 100.0 | 110.0 | app1 | True | 98820.0 | 66.7% | 53.7% | -13.0 |
| 100.0 | 110.0 | app2 | True | 85290.0 | 33.3% | 46.3% | 13.0 |
| 110.0 | 120.0 | app1 | True | 137914.0 | 66.7% | 76.7% | 10.0 |
| 110.0 | 120.0 | app2 | True | 41972.0 | 33.3% | 23.3% | -10.0 |
| 120.0 | 130.0 | app1 | True | 148768.0 | 66.7% | 85.3% | 18.6 |
| 120.0 | 130.0 | app2 | True | 25702.0 | 33.3% | 14.7% | -18.6 |
| 130.0 | 140.0 | app1 | True | 129750.0 | 66.7% | 68.0% | 1.4 |
| 130.0 | 140.0 | app2 | True | 60942.0 | 33.3% | 32.0% | -1.4 |
| 140.0 | 150.0 | app1 | True | 105626.0 | 66.7% | 57.8% | -8.9 |
| 140.0 | 150.0 | app2 | True | 77120.0 | 33.3% | 42.2% | 8.9 |
| 150.0 | 160.0 | app1 | True | 148844.0 | 66.7% | 86.6% | 19.9 |
| 150.0 | 160.0 | app2 | True | 23040.0 | 33.3% | 13.4% | -19.9 |
| 160.0 | 170.0 | app1 | True | 97452.0 | 66.7% | 50.7% | -15.9 |
| 160.0 | 170.0 | app2 | True | 94696.0 | 33.3% | 49.3% | 15.9 |
| 170.0 | 180.0 | app1 | True | 123058.0 | 66.7% | 66.4% | -0.3 |
| 170.0 | 180.0 | app2 | True | 62318.0 | 33.3% | 33.6% | 0.3 |
| 180.0 | 190.0 | app1 | True | 146150.0 | 66.7% | 85.7% | 19.1 |
| 180.0 | 190.0 | app2 | True | 24346.0 | 33.3% | 14.3% | -19.1 |
| 190.0 | 200.0 | app1 | True | 125848.0 | 66.7% | 66.9% | 0.2 |
| 190.0 | 200.0 | app2 | True | 62280.0 | 33.3% | 33.1% | -0.2 |
| 200.0 | 211.0 | app1 | True | 143444.0 | 66.7% | 77.4% | 10.7 |
| 200.0 | 211.0 | app2 | True | 41880.0 | 33.3% | 22.6% | -10.7 |
| 211.0 | 221.0 | app1 | True | 117640.0 | 66.7% | 65.4% | -1.3 |
| 211.0 | 221.0 | app2 | True | 62246.0 | 33.3% | 34.6% | 1.3 |
| 221.0 | 231.0 | app1 | True | 148702.0 | 66.7% | 84.0% | 17.3 |
| 221.0 | 231.0 | app2 | True | 28388.0 | 33.3% | 16.0% | -17.3 |
| 231.0 | 241.0 | app1 | True | 129834.0 | 66.7% | 70.0% | 3.4 |
| 231.0 | 241.0 | app2 | True | 55530.0 | 33.3% | 30.0% | -3.4 |
| 241.0 | 251.0 | app1 | False | 21612.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 41926.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 511.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 511.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 511.0 | 521.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 511.0 | 521.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 521.0 | 531.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 521.0 | 531.0 | app2 | False | 1623.0 | n/a | n/a | n/a |
| 531.0 | 541.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 531.0 | 541.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 541.0 | 545.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 541.0 | 545.0 | app2 | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2944620 | 146958 | 3091578.0 | 0.0% | 3115348.0 | 3238536.0 | -3.8% | True |
| app2 | 1189410 | 59640 | 1249050.0 | 0.0% | 1288657.0 | 1308690.0 | -1.5% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
