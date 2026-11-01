# Fairness benchmark: end-users-idle (uni139-end-users-idle-r1)

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
| Run start | `2026-11-01T20:05:08Z` |
| Run end | `2026-11-01T20:10:24Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 64 | 2320 | 000=1, 200=2304, 500=15 | 7.2 | 8.4 | 3031319.0 | 66.7% | 69.2% | 2.5 | 1.5s | 98.5% | 2305.0 |
| app2 | 10.0 | 32 | 1038 | 200=1020, 500=18 | 7.2 | 10.7 | 1349658.0 | 33.3% | 30.8% | -2.5 | 1.5s | 96.6% | 1019.0 |
| end-users | 65.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 98.9% | 0.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 1348.0 | n/a | n/a | n/a | 0.0s | 90.2% | 1.0 |

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

**Windows** (32 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 59544.0 | 66.7% | 66.7% | 0.0 |
| 0.0 | 10.0 | app2 | True | 29752.0 | 33.3% | 33.3% | -0.0 |
| 10.0 | 20.0 | app1 | True | 114928.0 | 66.7% | 68.0% | 1.3 |
| 10.0 | 20.0 | app2 | True | 54120.0 | 33.3% | 32.0% | -1.3 |
| 20.0 | 31.0 | app1 | True | 142142.0 | 66.7% | 76.7% | 10.0 |
| 20.0 | 31.0 | app2 | True | 43266.0 | 33.3% | 23.3% | -10.0 |
| 31.0 | 41.0 | app1 | True | 112446.0 | 66.7% | 58.9% | -7.8 |
| 31.0 | 41.0 | app2 | True | 78420.0 | 33.3% | 41.1% | 7.8 |
| 41.0 | 51.0 | app1 | True | 129882.0 | 66.7% | 78.7% | 12.0 |
| 41.0 | 51.0 | app2 | True | 35232.0 | 33.3% | 21.3% | -12.0 |
| 51.0 | 61.0 | app1 | True | 124554.0 | 66.7% | 68.1% | 1.5 |
| 51.0 | 61.0 | app2 | True | 58216.0 | 33.3% | 31.9% | -1.5 |
| 61.0 | 71.0 | app1 | True | 125840.0 | 66.7% | 66.5% | -0.2 |
| 61.0 | 71.0 | app2 | True | 63510.0 | 33.3% | 33.5% | 0.2 |
| 71.0 | 81.0 | app1 | True | 130032.0 | 66.7% | 74.4% | 7.8 |
| 71.0 | 81.0 | app2 | True | 44650.0 | 33.3% | 25.6% | -7.8 |
| 81.0 | 91.0 | app1 | True | 112272.0 | 66.7% | 63.9% | -2.8 |
| 81.0 | 91.0 | app2 | True | 63534.0 | 33.3% | 36.1% | 2.8 |
| 91.0 | 101.0 | app1 | True | 148756.0 | 66.7% | 78.0% | 11.4 |
| 91.0 | 101.0 | app2 | True | 41900.0 | 33.3% | 22.0% | -11.4 |
| 101.0 | 111.0 | app1 | True | 94726.0 | 66.7% | 52.3% | -14.4 |
| 101.0 | 111.0 | app2 | True | 86566.0 | 33.3% | 47.7% | 14.4 |
| 111.0 | 121.0 | app1 | True | 128596.0 | 66.7% | 75.4% | 8.7 |
| 111.0 | 121.0 | app2 | True | 41942.0 | 33.3% | 24.6% | -8.7 |
| 121.0 | 131.0 | app1 | True | 145948.0 | 66.7% | 77.1% | 10.5 |
| 121.0 | 131.0 | app2 | True | 43274.0 | 33.3% | 22.9% | -10.5 |
| 131.0 | 141.0 | app1 | True | 136652.0 | 66.7% | 75.4% | 8.7 |
| 131.0 | 141.0 | app2 | True | 44566.0 | 33.3% | 24.6% | -8.7 |
| 141.0 | 151.0 | app1 | True | 108170.0 | 66.7% | 59.7% | -7.0 |
| 141.0 | 151.0 | app2 | True | 73042.0 | 33.3% | 40.3% | 7.0 |
| 151.0 | 161.0 | app1 | True | 135224.0 | 66.7% | 76.3% | 9.7 |
| 151.0 | 161.0 | app2 | True | 41930.0 | 33.3% | 23.7% | -9.7 |
| 161.0 | 171.0 | app1 | True | 108222.0 | 66.7% | 58.4% | -8.3 |
| 161.0 | 171.0 | app2 | True | 77078.0 | 33.3% | 41.6% | 8.3 |
| 171.0 | 181.0 | app1 | True | 146248.0 | 66.7% | 77.8% | 11.1 |
| 171.0 | 181.0 | app2 | True | 41802.0 | 33.3% | 22.2% | -11.1 |
| 181.0 | 191.0 | app1 | True | 121802.0 | 66.7% | 72.6% | 6.0 |
| 181.0 | 191.0 | app2 | True | 45914.0 | 33.3% | 27.4% | -6.0 |
| 191.0 | 201.0 | app1 | True | 101402.0 | 66.7% | 54.7% | -11.9 |
| 191.0 | 201.0 | app2 | True | 83854.0 | 33.3% | 45.3% | 11.9 |
| 201.0 | 211.0 | app1 | True | 144806.0 | 66.7% | 77.0% | 10.3 |
| 201.0 | 211.0 | app2 | True | 43294.0 | 33.3% | 23.0% | -10.3 |
| 211.0 | 221.0 | app1 | True | 120426.0 | 66.7% | 73.5% | 6.9 |
| 211.0 | 221.0 | app2 | True | 43320.0 | 33.3% | 26.5% | -6.9 |
| 221.0 | 231.0 | app1 | True | 143506.0 | 66.7% | 76.3% | 9.6 |
| 221.0 | 231.0 | app2 | True | 44686.0 | 33.3% | 23.7% | -9.6 |
| 231.0 | 241.0 | app1 | True | 98804.0 | 66.7% | 54.1% | -12.6 |
| 231.0 | 241.0 | app2 | True | 83816.0 | 33.3% | 45.9% | 12.6 |
| 241.0 | 251.0 | app1 | False | 94770.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 41974.0 | n/a | n/a | n/a |
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
| 301.0 | 311.0 | app1 | False | 1621.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 316.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 316.0 | app2 | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2833920 | 141836 | 2975756.0 | 0.0% | 3031319.0 | 3117592.0 | -2.8% | True |
| app2 | 1254600 | 62428 | 1315739.0 | -0.1% | 1349658.0 | 1379456.0 | -2.2% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
