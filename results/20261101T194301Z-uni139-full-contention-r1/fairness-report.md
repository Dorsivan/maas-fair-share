# Fairness benchmark: full-contention (uni139-full-contention-r1)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T19:43:02Z` |
| Run end | `2026-11-01T19:47:25Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 543 | 200=543 | 15.9 | 23.3 | 703508.0 | 21.1% | 17.1% | -4.0 | 2.6s | 98.2% | 543.0 |
| app2 | 10.0 | 32 | 440 | 200=436, 500=4 | 24.2 | 27.5 | 557456.0 | 10.5% | 13.5% | 3.0 | 1.6s | 95.5% | 436.0 |
| end-users | 65.0 | 128 | 2154 | 200=2132, 500=22 | 15.8 | 19.8 | 2864000.0 | 68.4% | 69.4% | 1.0 | 2.1s | 98.9% | 2131.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 1346.0 | n/a | n/a | n/a | 0.0s | 77.7% | 1.0 |

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
| 0.0 | 10.0 | app1 | True | 12190.0 | 21.1% | 13.7% | -7.4 |
| 0.0 | 10.0 | app2 | True | 17554.0 | 10.5% | 19.7% | 9.2 |
| 0.0 | 10.0 | end-users | True | 59462.0 | 68.4% | 66.7% | -1.8 |
| 10.0 | 20.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 10.0 | 20.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 10.0 | 20.0 | end-users | True | 170432.0 | 68.4% | 100.0% | 31.6 |
| 20.0 | 30.0 | app1 | True | 47394.0 | 21.1% | 28.7% | 7.7 |
| 20.0 | 30.0 | app2 | True | 60856.0 | 10.5% | 36.9% | 26.3 |
| 20.0 | 30.0 | end-users | True | 56806.0 | 68.4% | 34.4% | -34.0 |
| 30.0 | 40.0 | app1 | True | 33774.0 | 21.1% | 21.9% | 0.8 |
| 30.0 | 40.0 | app2 | True | 1344.0 | 10.5% | 0.9% | -9.7 |
| 30.0 | 40.0 | end-users | True | 119112.0 | 68.4% | 77.2% | 8.8 |
| 40.0 | 50.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.3 |
| 40.0 | 50.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 40.0 | 50.0 | end-users | True | 169028.0 | 68.4% | 99.2% | 30.8 |
| 50.0 | 60.0 | app1 | True | 55418.0 | 21.1% | 32.5% | 11.5 |
| 50.0 | 60.0 | app2 | True | 63600.0 | 10.5% | 37.3% | 26.8 |
| 50.0 | 60.0 | end-users | True | 51446.0 | 68.4% | 30.2% | -38.2 |
| 60.0 | 70.0 | app1 | True | 27064.0 | 21.1% | 15.9% | -5.2 |
| 60.0 | 70.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 60.0 | 70.0 | end-users | True | 143352.0 | 68.4% | 84.1% | 15.7 |
| 70.0 | 80.0 | app1 | True | 17654.0 | 21.1% | 11.7% | -9.3 |
| 70.0 | 80.0 | app2 | True | 5398.0 | 10.5% | 3.6% | -6.9 |
| 70.0 | 80.0 | end-users | True | 127270.0 | 68.4% | 84.7% | 16.2 |
| 80.0 | 90.0 | app1 | True | 44592.0 | 21.1% | 27.2% | 6.2 |
| 80.0 | 90.0 | app2 | True | 55500.0 | 10.5% | 33.9% | 23.4 |
| 80.0 | 90.0 | end-users | True | 63602.0 | 68.4% | 38.9% | -29.6 |
| 90.0 | 100.0 | app1 | True | 16272.0 | 21.1% | 9.6% | -11.5 |
| 90.0 | 100.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 90.0 | 100.0 | end-users | True | 152716.0 | 68.4% | 89.7% | 21.2 |
| 100.0 | 110.0 | app1 | True | 37862.0 | 21.1% | 24.6% | 3.5 |
| 100.0 | 110.0 | app2 | True | 21616.0 | 10.5% | 14.0% | 3.5 |
| 100.0 | 110.0 | end-users | True | 94730.0 | 68.4% | 61.4% | -7.0 |
| 110.0 | 120.0 | app1 | True | 35120.0 | 21.1% | 21.3% | 0.2 |
| 110.0 | 120.0 | app2 | True | 37928.0 | 10.5% | 23.0% | 12.5 |
| 110.0 | 120.0 | end-users | True | 92004.0 | 68.4% | 55.7% | -12.7 |
| 120.0 | 130.0 | app1 | True | 5432.0 | 21.1% | 3.2% | -17.9 |
| 120.0 | 130.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 120.0 | 130.0 | end-users | True | 163810.0 | 68.4% | 96.0% | 27.6 |
| 130.0 | 140.0 | app1 | True | 47344.0 | 21.1% | 28.0% | 6.9 |
| 130.0 | 140.0 | app2 | True | 62232.0 | 10.5% | 36.8% | 26.3 |
| 130.0 | 140.0 | end-users | True | 59540.0 | 68.4% | 35.2% | -33.2 |
| 140.0 | 150.0 | app1 | True | 35090.0 | 21.1% | 23.2% | 2.1 |
| 140.0 | 150.0 | app2 | True | 1358.0 | 10.5% | 0.9% | -9.6 |
| 140.0 | 150.0 | end-users | True | 114910.0 | 68.4% | 75.9% | 7.5 |
| 150.0 | 160.0 | app1 | True | 4046.0 | 21.1% | 2.4% | -18.7 |
| 150.0 | 160.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 150.0 | 160.0 | end-users | True | 165120.0 | 68.4% | 97.6% | 29.2 |
| 160.0 | 170.0 | app1 | True | 50104.0 | 21.1% | 30.1% | 9.0 |
| 160.0 | 170.0 | app2 | True | 60862.0 | 10.5% | 36.6% | 26.0 |
| 160.0 | 170.0 | end-users | True | 55534.0 | 68.4% | 33.4% | -35.1 |
| 170.0 | 180.0 | app1 | True | 32490.0 | 21.1% | 21.5% | 0.4 |
| 170.0 | 180.0 | app2 | True | 1348.0 | 10.5% | 0.9% | -9.6 |
| 170.0 | 180.0 | end-users | True | 117588.0 | 68.4% | 77.7% | 9.2 |
| 180.0 | 191.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.2 |
| 180.0 | 191.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 180.0 | 191.0 | end-users | True | 167756.0 | 68.4% | 99.2% | 30.8 |
| 191.0 | 201.0 | app1 | True | 58106.0 | 21.1% | 34.9% | 13.9 |
| 191.0 | 201.0 | app2 | True | 60878.0 | 10.5% | 36.6% | 26.1 |
| 191.0 | 201.0 | end-users | True | 47310.0 | 68.4% | 28.4% | -40.0 |
| 201.0 | 211.0 | app1 | True | 20284.0 | 21.1% | 11.9% | -9.2 |
| 201.0 | 211.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 201.0 | 211.0 | end-users | True | 148862.0 | 68.4% | 87.3% | 18.9 |
| 211.0 | 221.0 | app1 | True | 27138.0 | 21.1% | 18.1% | -3.0 |
| 211.0 | 221.0 | app2 | True | 14912.0 | 10.5% | 9.9% | -0.6 |
| 211.0 | 221.0 | end-users | True | 108172.0 | 68.4% | 72.0% | 3.6 |
| 221.0 | 231.0 | app1 | True | 43266.0 | 21.1% | 25.0% | 3.9 |
| 221.0 | 231.0 | app2 | True | 45994.0 | 10.5% | 26.6% | 16.0 |
| 221.0 | 231.0 | end-users | True | 83820.0 | 68.4% | 48.4% | -20.0 |
| 231.0 | 241.0 | app1 | True | 6790.0 | 21.1% | 4.0% | -17.0 |
| 231.0 | 241.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 231.0 | 241.0 | end-users | True | 161082.0 | 68.4% | 96.0% | 27.5 |
| 241.0 | 251.0 | app1 | False | 43362.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 42002.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 85172.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 85364.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 667890 | 33349 | 701239.0 | 0.0% | 703508.0 | 734588.0 | -4.2% | True |
| app2 | 536280 | 26833 | 563113.0 | 0.0% | 557456.0 | 589946.0 | -5.5% | True |
| end-users | 2622360 | 130955 | 2752027.0 | -0.0% | 2864000.0 | 2884270.0 | -0.7% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
