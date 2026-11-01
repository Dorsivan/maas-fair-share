# Fairness benchmark: app2-trickle (uni139-app2-trickle-r2)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app2-trickle` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T22:09:02Z` |
| Run end | `2026-11-01T22:13:25Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 655 | 200=655 | 11.2 | 18.9 | 850842.0 | 23.5% | 20.3% | -3.2 | 1.5s | 98.8% | 655.0 |
| app2 | 10.0 | 2 | 52 | 200=52 | 10.8 | 16.1 | 67542.0 | n/a | n/a | n/a | 1.5s | 97.4% | 52.0 |
| end-users | 65.0 | 104 | 2442 | 200=2442 | 11.1 | 12.9 | 3270624.0 | 76.5% | 78.1% | 1.6 | 1.5s | 98.9% | 2442.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 98.1% | 0.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 20312.0 | 21.1% | 18.3% | -2.7 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 90616.0 | 68.4% | 81.7% | 13.3 |
| 10.0 | 20.0 | app1 | True | 43298.0 | 21.1% | 26.2% | 5.2 |
| 10.0 | 20.0 | app2 | True | 4030.0 | 10.5% | 2.4% | -8.1 |
| 10.0 | 20.0 | end-users | True | 117628.0 | 68.4% | 71.3% | 2.9 |
| 20.0 | 30.0 | app1 | True | 41936.0 | 21.1% | 25.2% | 4.2 |
| 20.0 | 30.0 | app2 | True | 4074.0 | 10.5% | 2.4% | -8.1 |
| 20.0 | 30.0 | end-users | True | 120332.0 | 68.4% | 72.3% | 3.9 |
| 30.0 | 40.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 30.0 | 40.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 30.0 | 40.0 | end-users | True | 163726.0 | 68.4% | 100.0% | 31.6 |
| 40.0 | 50.0 | app1 | True | 43276.0 | 21.1% | 26.0% | 4.9 |
| 40.0 | 50.0 | app2 | True | 2690.0 | 10.5% | 1.6% | -8.9 |
| 40.0 | 50.0 | end-users | True | 120480.0 | 68.4% | 72.4% | 4.0 |
| 50.0 | 60.0 | app1 | True | 46034.0 | 21.1% | 27.7% | 6.6 |
| 50.0 | 60.0 | app2 | True | 5402.0 | 10.5% | 3.2% | -7.3 |
| 50.0 | 60.0 | end-users | True | 114952.0 | 68.4% | 69.1% | 0.7 |
| 60.0 | 70.0 | app1 | True | 43266.0 | 21.1% | 25.4% | 4.4 |
| 60.0 | 70.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 60.0 | 70.0 | end-users | True | 124290.0 | 68.4% | 73.0% | 4.6 |
| 70.0 | 80.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 70.0 | 80.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 70.0 | 80.0 | end-users | True | 170556.0 | 68.4% | 100.0% | 31.6 |
| 80.0 | 90.0 | app1 | True | 62226.0 | 21.1% | 36.0% | 14.9 |
| 80.0 | 90.0 | app2 | True | 5386.0 | 10.5% | 3.1% | -7.4 |
| 80.0 | 90.0 | end-users | True | 105410.0 | 68.4% | 60.9% | -7.5 |
| 90.0 | 100.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 90.0 | 100.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 90.0 | 100.0 | end-users | True | 169236.0 | 68.4% | 100.0% | 31.6 |
| 100.0 | 110.0 | app1 | True | 62230.0 | 21.1% | 37.4% | 16.3 |
| 100.0 | 110.0 | app2 | True | 5402.0 | 10.5% | 3.2% | -7.3 |
| 100.0 | 110.0 | end-users | True | 98830.0 | 68.4% | 59.4% | -9.1 |
| 110.0 | 120.0 | app1 | True | 41980.0 | 21.1% | 24.8% | 3.8 |
| 110.0 | 120.0 | app2 | True | 2708.0 | 10.5% | 1.6% | -8.9 |
| 110.0 | 120.0 | end-users | True | 124340.0 | 68.4% | 73.6% | 5.1 |
| 120.0 | 130.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 120.0 | 130.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 120.0 | 130.0 | end-users | True | 170462.0 | 68.4% | 100.0% | 31.6 |
| 130.0 | 140.0 | app1 | True | 62230.0 | 21.1% | 36.8% | 15.8 |
| 130.0 | 140.0 | app2 | True | 5366.0 | 10.5% | 3.2% | -7.4 |
| 130.0 | 140.0 | end-users | True | 101476.0 | 68.4% | 60.0% | -8.4 |
| 140.0 | 150.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 140.0 | 150.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 140.0 | 150.0 | end-users | True | 167718.0 | 68.4% | 100.0% | 31.6 |
| 150.0 | 160.0 | app1 | True | 64952.0 | 21.1% | 39.7% | 18.6 |
| 150.0 | 160.0 | app2 | True | 5422.0 | 10.5% | 3.3% | -7.2 |
| 150.0 | 160.0 | end-users | True | 93270.0 | 68.4% | 57.0% | -11.4 |
| 160.0 | 170.0 | app1 | True | 41954.0 | 21.1% | 24.2% | 3.2 |
| 160.0 | 170.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -9.0 |
| 160.0 | 170.0 | end-users | True | 128378.0 | 68.4% | 74.2% | 5.8 |
| 170.0 | 180.0 | app1 | True | 6778.0 | 21.1% | 4.0% | -17.1 |
| 170.0 | 180.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 170.0 | 180.0 | end-users | True | 162254.0 | 68.4% | 95.2% | 26.8 |
| 180.0 | 190.0 | app1 | True | 59472.0 | 21.1% | 35.4% | 14.4 |
| 180.0 | 190.0 | app2 | True | 4060.0 | 10.5% | 2.4% | -8.1 |
| 180.0 | 190.0 | end-users | True | 104266.0 | 68.4% | 62.1% | -6.3 |
| 190.0 | 200.0 | app1 | True | 4064.0 | 21.1% | 2.5% | -18.6 |
| 190.0 | 200.0 | app2 | True | 2670.0 | 10.5% | 1.6% | -8.9 |
| 190.0 | 200.0 | end-users | True | 156916.0 | 68.4% | 95.9% | 27.5 |
| 200.0 | 210.0 | app1 | True | 59510.0 | 21.1% | 34.9% | 13.9 |
| 200.0 | 210.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 200.0 | 210.0 | end-users | True | 108168.0 | 68.4% | 63.5% | -4.9 |
| 210.0 | 220.0 | app1 | True | 13506.0 | 21.1% | 8.1% | -12.9 |
| 210.0 | 220.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 210.0 | 220.0 | end-users | True | 150240.0 | 68.4% | 90.3% | 21.8 |
| 220.0 | 230.0 | app1 | True | 50010.0 | 21.1% | 29.8% | 8.8 |
| 220.0 | 230.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 220.0 | 230.0 | end-users | True | 114912.0 | 68.4% | 68.5% | 0.1 |
| 230.0 | 240.0 | app1 | True | 21612.0 | 21.1% | 13.0% | -8.1 |
| 230.0 | 240.0 | app2 | True | 2688.0 | 10.5% | 1.6% | -8.9 |
| 230.0 | 240.0 | end-users | True | 142062.0 | 68.4% | 85.4% | 17.0 |
| 240.0 | 250.0 | app1 | False | 35114.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 2706.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 139308.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 27082.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 10798.0 | n/a | n/a | n/a |
| 260.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 263.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 805650 | 40197 | 845847.0 | 0.0% | 850842.0 | 886044.0 | -4.0% | True |
| app2 | 63960 | 3149 | 67109.0 | 0.0% | 67542.0 | 70258.0 | -3.9% | True |
| end-users | 3003660 | 149721 | 3153381.0 | 0.0% | 3270624.0 | 3303102.0 | -1.0% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
