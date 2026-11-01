# Fairness benchmark: app2-idle (uni139-app2-idle-r3)

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
| Run start | `2026-11-01T21:28:31Z` |
| Run end | `2026-11-01T21:32:54Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 672 | 200=671, 500=1 | 10.8 | 18.3 | 842738.0 | 23.5% | 20.2% | -3.4 | 1.4s | 98.8% | 671.0 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 97.3% | 0.0 |
| end-users | 65.0 | 104 | 2511 | 200=2497, 500=14 | 10.9 | 12.3 | 3337380.0 | 76.5% | 79.8% | 3.4 | 1.4s | 98.9% | 2497.0 |
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
| 0.0 | 231.0 | 231.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 9454.0 | 23.5% | 9.3% | -14.2 |
| 0.0 | 10.0 | end-users | True | 92018.0 | 76.5% | 90.7% | 14.2 |
| 10.0 | 20.0 | app1 | True | 44626.0 | 23.5% | 26.8% | 3.3 |
| 10.0 | 20.0 | end-users | True | 121742.0 | 76.5% | 73.2% | -3.3 |
| 20.0 | 30.0 | app1 | True | 41990.0 | 23.5% | 24.8% | 1.3 |
| 20.0 | 30.0 | end-users | True | 127156.0 | 76.5% | 75.2% | -1.3 |
| 30.0 | 40.0 | app1 | True | 13550.0 | 23.5% | 8.2% | -15.3 |
| 30.0 | 40.0 | end-users | True | 151518.0 | 76.5% | 91.8% | 15.3 |
| 40.0 | 50.0 | app1 | True | 32382.0 | 23.5% | 18.9% | -4.7 |
| 40.0 | 50.0 | end-users | True | 139388.0 | 76.5% | 81.1% | 4.7 |
| 50.0 | 60.0 | app1 | True | 41972.0 | 23.5% | 25.0% | 1.5 |
| 50.0 | 60.0 | end-users | True | 125768.0 | 76.5% | 75.0% | -1.5 |
| 60.0 | 70.0 | app1 | True | 47318.0 | 23.5% | 26.3% | 2.8 |
| 60.0 | 70.0 | end-users | True | 132560.0 | 76.5% | 73.7% | -2.8 |
| 70.0 | 80.0 | app1 | True | 37904.0 | 23.5% | 21.2% | -2.3 |
| 70.0 | 80.0 | end-users | True | 140520.0 | 76.5% | 78.8% | 2.3 |
| 80.0 | 90.0 | app1 | True | 20298.0 | 23.5% | 11.9% | -11.6 |
| 80.0 | 90.0 | end-users | True | 150106.0 | 76.5% | 88.1% | 11.6 |
| 90.0 | 100.0 | app1 | True | 60906.0 | 23.5% | 36.6% | 13.1 |
| 90.0 | 100.0 | end-users | True | 105478.0 | 76.5% | 63.4% | -13.1 |
| 100.0 | 110.0 | app1 | True | 1346.0 | 23.5% | 0.8% | -22.7 |
| 100.0 | 110.0 | end-users | True | 163824.0 | 76.5% | 99.2% | 22.7 |
| 110.0 | 120.0 | app1 | True | 43218.0 | 23.5% | 25.0% | 1.4 |
| 110.0 | 120.0 | end-users | True | 129940.0 | 76.5% | 75.0% | -1.4 |
| 120.0 | 131.0 | app1 | True | 43232.0 | 23.5% | 25.4% | 1.8 |
| 120.0 | 131.0 | end-users | True | 127218.0 | 76.5% | 74.6% | -1.8 |
| 131.0 | 141.0 | app1 | True | 41976.0 | 23.5% | 25.7% | 2.1 |
| 131.0 | 141.0 | end-users | True | 121668.0 | 76.5% | 74.3% | -2.1 |
| 141.0 | 151.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 141.0 | 151.0 | end-users | True | 171874.0 | 76.5% | 100.0% | 23.5 |
| 151.0 | 161.0 | app1 | True | 63546.0 | 23.5% | 38.2% | 14.7 |
| 151.0 | 161.0 | end-users | True | 102692.0 | 76.5% | 61.8% | -14.7 |
| 161.0 | 171.0 | app1 | True | 2716.0 | 23.5% | 1.6% | -21.9 |
| 161.0 | 171.0 | end-users | True | 165130.0 | 76.5% | 98.4% | 21.9 |
| 171.0 | 181.0 | app1 | True | 60888.0 | 23.5% | 35.7% | 12.2 |
| 171.0 | 181.0 | end-users | True | 109580.0 | 76.5% | 64.3% | -12.2 |
| 181.0 | 191.0 | app1 | True | 41902.0 | 23.5% | 25.4% | 1.9 |
| 181.0 | 191.0 | end-users | True | 123200.0 | 76.5% | 74.6% | -1.9 |
| 191.0 | 201.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 191.0 | 201.0 | end-users | True | 170450.0 | 76.5% | 100.0% | 23.5 |
| 201.0 | 211.0 | app1 | True | 63578.0 | 23.5% | 37.6% | 14.1 |
| 201.0 | 211.0 | end-users | True | 105456.0 | 76.5% | 62.4% | -14.1 |
| 211.0 | 221.0 | app1 | True | 41974.0 | 23.5% | 24.4% | 0.9 |
| 211.0 | 221.0 | end-users | True | 129944.0 | 76.5% | 75.6% | -0.9 |
| 221.0 | 231.0 | app1 | True | 16236.0 | 23.5% | 9.8% | -13.8 |
| 221.0 | 231.0 | end-users | True | 149992.0 | 76.5% | 90.2% | 13.8 |
| 231.0 | 241.0 | app1 | True | 29756.0 | 23.5% | 17.6% | -5.9 |
| 231.0 | 241.0 | end-users | True | 139480.0 | 76.5% | 82.4% | 5.9 |
| 241.0 | 251.0 | app1 | False | 41970.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 127100.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 13578.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 825330 | 41166 | 866496.0 | 0.0% | 842738.0 | 907662.0 | -7.2% | True |
| end-users | 3071310 | 153310 | 3224620.0 | 0.0% | 3337380.0 | 3377930.0 | -1.2% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
