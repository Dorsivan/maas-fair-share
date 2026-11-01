# Fairness benchmark: app2-idle (uni139-app2-idle-r4)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app2-idle` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T21:32:55Z` |
| Run end | `2026-11-01T21:37:18Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 670 | 200=670 | 10.9 | 18.1 | 853114.0 | 23.5% | 20.7% | -2.9 | 1.5s | 98.8% | 670.0 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 97.3% | 0.0 |
| end-users | 65.0 | 104 | 2528 | 200=2490, 500=38 | 10.8 | 12.5 | 3272508.0 | 76.5% | 79.3% | 2.9 | 1.5s | 98.9% | 2490.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 91.3% | 0.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 35256.0 | 23.5% | 29.6% | 6.1 |
| 0.0 | 10.0 | end-users | True | 83718.0 | 76.5% | 70.4% | -6.1 |
| 10.0 | 20.0 | app1 | True | 13564.0 | 23.5% | 8.2% | -15.3 |
| 10.0 | 20.0 | end-users | True | 151534.0 | 76.5% | 91.8% | 15.3 |
| 20.0 | 30.0 | app1 | True | 43268.0 | 23.5% | 25.2% | 1.7 |
| 20.0 | 30.0 | end-users | True | 128372.0 | 76.5% | 74.8% | -1.7 |
| 30.0 | 40.0 | app1 | True | 55468.0 | 23.5% | 33.6% | 10.0 |
| 30.0 | 40.0 | end-users | True | 109766.0 | 76.5% | 66.4% | -10.0 |
| 40.0 | 50.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 40.0 | 50.0 | end-users | True | 173032.0 | 76.5% | 100.0% | 23.5 |
| 50.0 | 60.0 | app1 | True | 64946.0 | 23.5% | 37.8% | 14.3 |
| 50.0 | 60.0 | end-users | True | 106750.0 | 76.5% | 62.2% | -14.3 |
| 60.0 | 70.0 | app1 | True | 41968.0 | 23.5% | 25.4% | 1.9 |
| 60.0 | 70.0 | end-users | True | 123162.0 | 76.5% | 74.6% | -1.9 |
| 70.0 | 80.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 70.0 | 80.0 | end-users | True | 171752.0 | 76.5% | 100.0% | 23.5 |
| 80.0 | 90.0 | app1 | True | 63586.0 | 23.5% | 37.9% | 14.3 |
| 80.0 | 90.0 | end-users | True | 104288.0 | 76.5% | 62.1% | -14.3 |
| 90.0 | 100.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 90.0 | 100.0 | end-users | True | 165258.0 | 76.5% | 100.0% | 23.5 |
| 100.0 | 110.0 | app1 | True | 43148.0 | 23.5% | 25.5% | 2.0 |
| 100.0 | 110.0 | end-users | True | 125844.0 | 76.5% | 74.5% | -2.0 |
| 110.0 | 120.0 | app1 | True | 43284.0 | 23.5% | 25.4% | 1.9 |
| 110.0 | 120.0 | end-users | True | 127018.0 | 76.5% | 74.6% | -1.9 |
| 120.0 | 131.0 | app1 | True | 9472.0 | 23.5% | 5.6% | -18.0 |
| 120.0 | 131.0 | end-users | True | 161084.0 | 76.5% | 94.4% | 18.0 |
| 131.0 | 141.0 | app1 | True | 52666.0 | 23.5% | 31.9% | 8.4 |
| 131.0 | 141.0 | end-users | True | 112380.0 | 76.5% | 68.1% | -8.4 |
| 141.0 | 151.0 | app1 | True | 41882.0 | 23.5% | 24.8% | 1.2 |
| 141.0 | 151.0 | end-users | True | 127250.0 | 76.5% | 75.2% | -1.2 |
| 151.0 | 161.0 | app1 | True | 31054.0 | 23.5% | 18.2% | -5.3 |
| 151.0 | 161.0 | end-users | True | 139268.0 | 76.5% | 81.8% | 5.3 |
| 161.0 | 171.0 | app1 | True | 33766.0 | 23.5% | 20.5% | -3.1 |
| 161.0 | 171.0 | end-users | True | 131290.0 | 76.5% | 79.5% | 3.1 |
| 171.0 | 181.0 | app1 | True | 41854.0 | 23.5% | 24.0% | 0.5 |
| 171.0 | 181.0 | end-users | True | 132502.0 | 76.5% | 76.0% | -0.5 |
| 181.0 | 191.0 | app1 | True | 40532.0 | 23.5% | 23.6% | 0.0 |
| 181.0 | 191.0 | end-users | True | 131402.0 | 76.5% | 76.4% | -0.0 |
| 191.0 | 201.0 | app1 | True | 40546.0 | 23.5% | 23.8% | 0.3 |
| 191.0 | 201.0 | end-users | True | 129812.0 | 76.5% | 76.2% | -0.3 |
| 201.0 | 211.0 | app1 | True | 28434.0 | 23.5% | 16.8% | -6.7 |
| 201.0 | 211.0 | end-users | True | 140624.0 | 76.5% | 83.2% | 6.7 |
| 211.0 | 221.0 | app1 | True | 20284.0 | 23.5% | 11.7% | -11.8 |
| 211.0 | 221.0 | end-users | True | 152714.0 | 76.5% | 88.3% | 11.8 |
| 221.0 | 231.0 | app1 | True | 62110.0 | 23.5% | 36.7% | 13.2 |
| 221.0 | 231.0 | end-users | True | 106958.0 | 76.5% | 63.3% | -13.2 |
| 231.0 | 241.0 | app1 | True | 2682.0 | 23.5% | 1.6% | -21.9 |
| 231.0 | 241.0 | end-users | True | 164952.0 | 76.5% | 98.4% | 21.9 |
| 241.0 | 251.0 | app1 | False | 43344.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 71778.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 824100 | 40901 | 865001.0 | 0.0% | 853114.0 | 905902.0 | -5.8% | True |
| end-users | 3062700 | 152899 | 3215599.0 | 0.0% | 3272508.0 | 3368498.0 | -2.8% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
