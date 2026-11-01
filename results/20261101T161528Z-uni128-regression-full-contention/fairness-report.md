# Fairness benchmark: full-contention (uni128-regression-full-contention)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T16:15:29Z` |
| Run end | `2026-11-01T16:19:53Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 546 | 200=546 | 15.7 | 22.5 | 701058.0 | 21.1% | 16.9% | -4.2 |
| app2 | 10.0 | 32 | 443 | 200=438, 500=5 | 24.6 | 27.9 | 568446.0 | 10.5% | 13.7% | 3.2 |
| end-users | 65.0 | 128 | 2164 | 200=2141, 500=23 | 15.3 | 19.8 | 2881186.0 | 68.4% | 69.4% | 1.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a |

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
| 0.0 | 10.0 | app1 | True | 4040.0 | 21.1% | 3.8% | -17.2 |
| 0.0 | 10.0 | app2 | True | 23026.0 | 10.5% | 21.8% | 11.3 |
| 0.0 | 10.0 | end-users | True | 78486.0 | 68.4% | 74.4% | 5.9 |
| 10.0 | 20.0 | app1 | True | 31118.0 | 21.1% | 19.5% | -1.6 |
| 10.0 | 20.0 | app2 | True | 29790.0 | 10.5% | 18.6% | 8.1 |
| 10.0 | 20.0 | end-users | True | 98914.0 | 68.4% | 61.9% | -6.5 |
| 20.0 | 30.0 | app1 | True | 12170.0 | 21.1% | 7.2% | -13.8 |
| 20.0 | 30.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 20.0 | 30.0 | end-users | True | 156782.0 | 68.4% | 92.8% | 24.4 |
| 30.0 | 40.0 | app1 | True | 46024.0 | 21.1% | 27.2% | 6.1 |
| 30.0 | 40.0 | app2 | True | 58224.0 | 10.5% | 34.4% | 23.9 |
| 30.0 | 40.0 | end-users | True | 64982.0 | 68.4% | 38.4% | -30.0 |
| 40.0 | 50.0 | app1 | True | 29794.0 | 21.1% | 19.6% | -1.4 |
| 40.0 | 50.0 | app2 | True | 1348.0 | 10.5% | 0.9% | -9.6 |
| 40.0 | 50.0 | end-users | True | 120536.0 | 68.4% | 79.5% | 11.0 |
| 50.0 | 60.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.3 |
| 50.0 | 60.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 50.0 | 60.0 | end-users | True | 171762.0 | 68.4% | 99.2% | 30.8 |
| 60.0 | 70.0 | app1 | True | 58074.0 | 21.1% | 33.8% | 12.8 |
| 60.0 | 70.0 | app2 | True | 63670.0 | 10.5% | 37.1% | 26.5 |
| 60.0 | 70.0 | end-users | True | 50018.0 | 68.4% | 29.1% | -39.3 |
| 70.0 | 80.0 | app1 | True | 27110.0 | 21.1% | 16.0% | -5.0 |
| 70.0 | 80.0 | app2 | True | 1338.0 | 10.5% | 0.8% | -9.7 |
| 70.0 | 80.0 | end-users | True | 140716.0 | 68.4% | 83.2% | 14.8 |
| 80.0 | 90.0 | app1 | True | 12204.0 | 21.1% | 8.1% | -13.0 |
| 80.0 | 90.0 | app2 | True | 6782.0 | 10.5% | 4.5% | -6.1 |
| 80.0 | 90.0 | end-users | True | 132614.0 | 68.4% | 87.5% | 19.1 |
| 90.0 | 100.0 | app1 | True | 50080.0 | 21.1% | 30.6% | 9.5 |
| 90.0 | 100.0 | app2 | True | 55382.0 | 10.5% | 33.8% | 23.3 |
| 90.0 | 100.0 | end-users | True | 58262.0 | 68.4% | 35.6% | -32.8 |
| 100.0 | 111.0 | app1 | True | 21682.0 | 21.1% | 12.6% | -8.4 |
| 100.0 | 111.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 100.0 | 111.0 | end-users | True | 150160.0 | 68.4% | 87.4% | 19.0 |
| 111.0 | 121.0 | app1 | True | 32508.0 | 21.1% | 21.8% | 0.8 |
| 111.0 | 121.0 | app2 | True | 17640.0 | 10.5% | 11.8% | 1.3 |
| 111.0 | 121.0 | end-users | True | 98798.0 | 68.4% | 66.3% | -2.1 |
| 121.0 | 131.0 | app1 | True | 36476.0 | 21.1% | 21.4% | 0.4 |
| 121.0 | 131.0 | app2 | True | 45990.0 | 10.5% | 27.0% | 16.5 |
| 121.0 | 131.0 | end-users | True | 87894.0 | 68.4% | 51.6% | -16.8 |
| 131.0 | 141.0 | app1 | True | 14910.0 | 21.1% | 8.8% | -12.3 |
| 131.0 | 141.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 131.0 | 141.0 | end-users | True | 155320.0 | 68.4% | 91.2% | 22.8 |
| 141.0 | 151.0 | app1 | True | 43282.0 | 21.1% | 25.2% | 4.2 |
| 141.0 | 151.0 | app2 | True | 56802.0 | 10.5% | 33.1% | 22.6 |
| 141.0 | 151.0 | end-users | True | 71640.0 | 68.4% | 41.7% | -26.7 |
| 151.0 | 161.0 | app1 | True | 35210.0 | 21.1% | 23.3% | 2.2 |
| 151.0 | 161.0 | app2 | True | 4074.0 | 10.5% | 2.7% | -7.8 |
| 151.0 | 161.0 | end-users | True | 112138.0 | 68.4% | 74.1% | 5.6 |
| 161.0 | 171.0 | app1 | True | 4074.0 | 21.1% | 2.5% | -18.6 |
| 161.0 | 171.0 | app2 | True | 1348.0 | 10.5% | 0.8% | -9.7 |
| 161.0 | 171.0 | end-users | True | 158368.0 | 68.4% | 96.7% | 28.3 |
| 171.0 | 181.0 | app1 | True | 44664.0 | 21.1% | 25.8% | 4.7 |
| 171.0 | 181.0 | app2 | True | 62270.0 | 10.5% | 36.0% | 25.4 |
| 171.0 | 181.0 | end-users | True | 66260.0 | 68.4% | 38.3% | -30.2 |
| 181.0 | 191.0 | app1 | True | 35256.0 | 21.1% | 22.9% | 1.8 |
| 181.0 | 191.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 181.0 | 191.0 | end-users | True | 119006.0 | 68.4% | 77.1% | 8.7 |
| 191.0 | 201.0 | app1 | True | 21642.0 | 21.1% | 12.9% | -8.1 |
| 191.0 | 201.0 | app2 | True | 41946.0 | 10.5% | 25.0% | 14.5 |
| 191.0 | 201.0 | end-users | True | 104098.0 | 68.4% | 62.1% | -6.3 |
| 201.0 | 211.0 | app1 | True | 24334.0 | 21.1% | 14.5% | -6.5 |
| 201.0 | 211.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 201.0 | 211.0 | end-users | True | 143404.0 | 68.4% | 85.5% | 17.1 |
| 211.0 | 221.0 | app1 | True | 39272.0 | 21.1% | 24.0% | 2.9 |
| 211.0 | 221.0 | app2 | True | 29788.0 | 10.5% | 18.2% | 7.7 |
| 211.0 | 221.0 | end-users | True | 94794.0 | 68.4% | 57.9% | -10.6 |
| 221.0 | 231.0 | app1 | True | 31148.0 | 21.1% | 20.4% | -0.7 |
| 221.0 | 231.0 | app2 | True | 25734.0 | 10.5% | 16.8% | 6.3 |
| 221.0 | 231.0 | end-users | True | 96140.0 | 68.4% | 62.8% | -5.6 |
| 231.0 | 241.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.2 |
| 231.0 | 241.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 231.0 | 241.0 | end-users | True | 166340.0 | 68.4% | 98.4% | 30.0 |
| 241.0 | 251.0 | app1 | False | 43270.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 41936.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 85272.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 98482.0 | n/a | n/a | n/a |
| 261.0 | 264.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 264.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 264.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation.
