# Fairness benchmark: end-users-idle (uni139-end-users-idle-r5)

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
| Run start | `2026-11-01T20:27:59Z` |
| Run end | `2026-11-01T20:37:09Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 64 | 2363 | 000=1, 200=2337, 500=25 | 7.2 | 8.7 | 3073501.0 | 66.7% | 69.5% | 2.8 | 1.5s | 98.7% | 2338.0 |
| app2 | 10.0 | 32 | 1060 | 200=1034, 500=26 | 7.2 | 11.1 | 1349988.0 | 33.3% | 30.5% | -2.8 | 1.5s | 97.3% | 1034.0 |
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
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (55 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 79796.0 | 66.7% | 75.6% | 9.0 |
| 0.0 | 10.0 | app2 | True | 25730.0 | 33.3% | 24.4% | -9.0 |
| 10.0 | 20.0 | app1 | True | 136736.0 | 66.7% | 81.5% | 14.8 |
| 10.0 | 20.0 | app2 | True | 31040.0 | 33.3% | 18.5% | -14.8 |
| 20.0 | 30.0 | app1 | True | 109518.0 | 66.7% | 57.0% | -9.6 |
| 20.0 | 30.0 | app2 | True | 82476.0 | 33.3% | 43.0% | 9.6 |
| 30.0 | 40.0 | app1 | True | 145982.0 | 66.7% | 77.1% | 10.5 |
| 30.0 | 40.0 | app2 | True | 43314.0 | 33.3% | 22.9% | -10.5 |
| 40.0 | 50.0 | app1 | True | 124378.0 | 66.7% | 70.8% | 4.1 |
| 40.0 | 50.0 | app2 | True | 51408.0 | 33.3% | 29.2% | -4.1 |
| 50.0 | 60.0 | app1 | True | 136484.0 | 66.7% | 75.4% | 8.7 |
| 50.0 | 60.0 | app2 | True | 44638.0 | 33.3% | 24.6% | -8.7 |
| 60.0 | 70.0 | app1 | True | 109660.0 | 66.7% | 59.6% | -7.1 |
| 60.0 | 70.0 | app2 | True | 74426.0 | 33.3% | 40.4% | 7.1 |
| 70.0 | 80.0 | app1 | True | 145960.0 | 66.7% | 77.1% | 10.4 |
| 70.0 | 80.0 | app2 | True | 43408.0 | 33.3% | 22.9% | -10.4 |
| 80.0 | 90.0 | app1 | True | 127168.0 | 66.7% | 74.7% | 8.0 |
| 80.0 | 90.0 | app2 | True | 43166.0 | 33.3% | 25.3% | -8.0 |
| 90.0 | 100.0 | app1 | True | 140726.0 | 66.7% | 76.5% | 9.8 |
| 90.0 | 100.0 | app2 | True | 43272.0 | 33.3% | 23.5% | -9.8 |
| 100.0 | 110.0 | app1 | True | 116378.0 | 66.7% | 64.2% | -2.5 |
| 100.0 | 110.0 | app2 | True | 65020.0 | 33.3% | 35.8% | 2.5 |
| 110.0 | 120.0 | app1 | True | 131242.0 | 66.7% | 75.8% | 9.1 |
| 110.0 | 120.0 | app2 | True | 41888.0 | 33.3% | 24.2% | -9.1 |
| 120.0 | 130.0 | app1 | True | 101354.0 | 66.7% | 55.1% | -11.5 |
| 120.0 | 130.0 | app2 | True | 82434.0 | 33.3% | 44.9% | 11.5 |
| 130.0 | 140.0 | app1 | True | 125768.0 | 66.7% | 66.4% | -0.3 |
| 130.0 | 140.0 | app2 | True | 63606.0 | 33.3% | 33.6% | 0.3 |
| 140.0 | 150.0 | app1 | True | 139190.0 | 66.7% | 76.8% | 10.2 |
| 140.0 | 150.0 | app2 | True | 41992.0 | 33.3% | 23.2% | -10.2 |
| 150.0 | 160.0 | app1 | True | 129862.0 | 66.7% | 75.0% | 8.3 |
| 150.0 | 160.0 | app2 | True | 43322.0 | 33.3% | 25.0% | -8.3 |
| 160.0 | 170.0 | app1 | True | 147378.0 | 66.7% | 76.7% | 10.1 |
| 160.0 | 170.0 | app2 | True | 44704.0 | 33.3% | 23.3% | -10.1 |
| 170.0 | 180.0 | app1 | True | 123226.0 | 66.7% | 66.0% | -0.7 |
| 170.0 | 180.0 | app2 | True | 63514.0 | 33.3% | 34.0% | 0.7 |
| 180.0 | 190.0 | app1 | True | 102896.0 | 66.7% | 61.8% | -4.9 |
| 180.0 | 190.0 | app2 | True | 63672.0 | 33.3% | 38.2% | 4.9 |
| 190.0 | 200.0 | app1 | True | 131166.0 | 66.7% | 68.3% | 1.7 |
| 190.0 | 200.0 | app2 | True | 60794.0 | 33.3% | 31.7% | -1.7 |
| 200.0 | 210.0 | app1 | True | 138094.0 | 66.7% | 75.6% | 9.0 |
| 200.0 | 210.0 | app2 | True | 44516.0 | 33.3% | 24.4% | -9.0 |
| 210.0 | 220.0 | app1 | True | 108150.0 | 66.7% | 63.5% | -3.2 |
| 210.0 | 220.0 | app2 | True | 62192.0 | 33.3% | 36.5% | 3.2 |
| 220.0 | 230.0 | app1 | True | 148860.0 | 66.7% | 78.0% | 11.3 |
| 220.0 | 230.0 | app2 | True | 41946.0 | 33.3% | 22.0% | -11.3 |
| 230.0 | 240.0 | app1 | True | 86626.0 | 66.7% | 47.4% | -19.3 |
| 230.0 | 240.0 | app2 | True | 96138.0 | 33.3% | 52.6% | 19.3 |
| 240.0 | 250.0 | app1 | False | 85280.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 51372.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 330.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 330.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 330.0 | 340.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 330.0 | 340.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 340.0 | 350.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 340.0 | 350.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 350.0 | 360.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 350.0 | 360.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 360.0 | 371.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 360.0 | 371.0 | app2 | False | 0.0 | n/a | n/a | n/a |
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
| 521.0 | 531.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 531.0 | 541.0 | app1 | False | 1623.0 | n/a | n/a | n/a |
| 531.0 | 541.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 541.0 | 550.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 541.0 | 550.0 | app2 | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2874510 | 143297 | 3017807.0 | 0.0% | 3073501.0 | 3161104.0 | -2.8% | True |
| app2 | 1271820 | 63446 | 1335266.0 | 0.0% | 1349988.0 | 1398712.0 | -3.5% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
