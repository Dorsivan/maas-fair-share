# Fairness benchmark: end-users-idle (uni139-end-users-idle-r3)

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
| Run start | `2026-11-01T20:19:32Z` |
| Run end | `2026-11-01T20:23:44Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 64 | 2364 | 200=2357, 500=7 | 7.2 | 8.7 | 3043576.0 | 66.7% | 70.1% | 3.4 | 1.5s | 98.6% | 2357.0 |
| app2 | 10.0 | 32 | 997 | 200=985, 500=12 | 7.4 | 11.3 | 1301012.0 | 33.3% | 29.9% | -3.4 | 1.5s | 97.0% | 985.0 |
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
| 0.0 | 230.0 | 230.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 85144.0 | 66.7% | 78.7% | 12.1 |
| 0.0 | 10.0 | app2 | True | 22994.0 | 33.3% | 21.3% | -12.1 |
| 10.0 | 20.0 | app1 | True | 132596.0 | 66.7% | 74.3% | 7.6 |
| 10.0 | 20.0 | app2 | True | 45908.0 | 33.3% | 25.7% | -7.6 |
| 20.0 | 30.0 | app1 | True | 132594.0 | 66.7% | 75.4% | 8.7 |
| 20.0 | 30.0 | app2 | True | 43338.0 | 33.3% | 24.6% | -8.7 |
| 30.0 | 40.0 | app1 | True | 105412.0 | 66.7% | 55.7% | -11.0 |
| 30.0 | 40.0 | app2 | True | 83842.0 | 33.3% | 44.3% | 11.0 |
| 40.0 | 50.0 | app1 | True | 142052.0 | 66.7% | 76.6% | 10.0 |
| 40.0 | 50.0 | app2 | True | 43312.0 | 33.3% | 23.4% | -10.0 |
| 50.0 | 60.0 | app1 | True | 124388.0 | 66.7% | 72.4% | 5.8 |
| 50.0 | 60.0 | app2 | True | 47360.0 | 33.3% | 27.6% | -5.8 |
| 60.0 | 70.0 | app1 | True | 128442.0 | 66.7% | 67.3% | 0.7 |
| 60.0 | 70.0 | app2 | True | 62290.0 | 33.3% | 32.7% | -0.7 |
| 70.0 | 80.0 | app1 | True | 140642.0 | 66.7% | 76.5% | 9.8 |
| 70.0 | 80.0 | app2 | True | 43254.0 | 33.3% | 23.5% | -9.8 |
| 80.0 | 90.0 | app1 | True | 116354.0 | 66.7% | 65.2% | -1.5 |
| 80.0 | 90.0 | app2 | True | 62148.0 | 33.3% | 34.8% | 1.5 |
| 90.0 | 100.0 | app1 | True | 112248.0 | 66.7% | 63.3% | -3.3 |
| 90.0 | 100.0 | app2 | True | 65012.0 | 33.3% | 36.7% | 3.3 |
| 100.0 | 110.0 | app1 | True | 145902.0 | 66.7% | 77.1% | 10.4 |
| 100.0 | 110.0 | app2 | True | 43308.0 | 33.3% | 22.9% | -10.4 |
| 110.0 | 120.0 | app1 | True | 143308.0 | 66.7% | 77.4% | 10.7 |
| 110.0 | 120.0 | app2 | True | 41954.0 | 33.3% | 22.6% | -10.7 |
| 120.0 | 130.0 | app1 | True | 109640.0 | 66.7% | 63.8% | -2.9 |
| 120.0 | 130.0 | app2 | True | 62274.0 | 33.3% | 36.2% | 2.9 |
| 130.0 | 140.0 | app1 | True | 144914.0 | 66.7% | 77.5% | 10.9 |
| 130.0 | 140.0 | app2 | True | 41976.0 | 33.3% | 22.5% | -10.9 |
| 140.0 | 150.0 | app1 | True | 97250.0 | 66.7% | 53.3% | -13.4 |
| 140.0 | 150.0 | app2 | True | 85218.0 | 33.3% | 46.7% | 13.4 |
| 150.0 | 160.0 | app1 | True | 131208.0 | 66.7% | 77.0% | 10.4 |
| 150.0 | 160.0 | app2 | True | 39136.0 | 33.3% | 23.0% | -10.4 |
| 160.0 | 170.0 | app1 | True | 117816.0 | 66.7% | 64.0% | -2.7 |
| 160.0 | 170.0 | app2 | True | 66254.0 | 33.3% | 36.0% | 2.7 |
| 170.0 | 180.0 | app1 | True | 127164.0 | 66.7% | 67.1% | 0.5 |
| 170.0 | 180.0 | app2 | True | 62222.0 | 33.3% | 32.9% | -0.5 |
| 180.0 | 190.0 | app1 | True | 133968.0 | 66.7% | 76.2% | 9.5 |
| 180.0 | 190.0 | app2 | True | 41892.0 | 33.3% | 23.8% | -9.5 |
| 190.0 | 200.0 | app1 | True | 119110.0 | 66.7% | 65.2% | -1.4 |
| 190.0 | 200.0 | app2 | True | 63490.0 | 33.3% | 34.8% | 1.4 |
| 200.0 | 210.0 | app1 | True | 125800.0 | 66.7% | 66.9% | 0.2 |
| 200.0 | 210.0 | app2 | True | 62218.0 | 33.3% | 33.1% | -0.2 |
| 210.0 | 220.0 | app1 | True | 127252.0 | 66.7% | 70.7% | 4.1 |
| 210.0 | 220.0 | app2 | True | 52658.0 | 33.3% | 29.3% | -4.1 |
| 220.0 | 230.0 | app1 | True | 148784.0 | 66.7% | 85.9% | 19.3 |
| 220.0 | 230.0 | app2 | True | 24386.0 | 33.3% | 14.1% | -19.3 |
| 230.0 | 240.0 | app1 | True | 133980.0 | 66.7% | 72.3% | 5.6 |
| 230.0 | 240.0 | app2 | True | 51314.0 | 33.3% | 27.7% | -5.6 |
| 240.0 | 250.0 | app1 | False | 17608.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 43254.0 | n/a | n/a | n/a |
| 250.0 | 252.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 252.0 | app2 | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2899110 | 144651 | 3043761.0 | 0.0% | 3043576.0 | 3188412.0 | -4.5% | True |
| app2 | 1211550 | 60303 | 1271853.0 | 0.0% | 1301012.0 | 1332156.0 | -2.3% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
