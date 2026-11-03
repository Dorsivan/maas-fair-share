# Fairness benchmark: misclassified-prefix (uni-153-d2-misclassified-prefix)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `misclassified-prefix` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `420` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-hp9rr` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-03T11:07:56Z` |
| Run end | `2026-11-03T11:15:26Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 889 | 200=877, 500=12 | 16.3 | 25.4 | 1171670.0 | 21.1% | 17.2% | -3.8 | 17.2% | -3.9 | 13.0s | 98.9% | 874.0 |
| app2 | 10.0 | 32 | 737 | 200=724, 500=13 | 23.9 | 27.7 | 963268.0 | 10.5% | 14.2% | 3.6 | 14.2% | 3.7 | 12.6s | 98.9% | 724.0 |
| end-users | 65.0 | 128 | 3553 | 200=3496, 500=57 | 16.6 | 20.6 | 4669446.0 | 68.4% | 68.6% | 0.2 | 68.6% | 0.2 | 13.0s | 98.9% | 3491.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 313898.0 | n/a | n/a | n/a | n/a | n/a | 13.4s | 98.9% | 235.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-420s, no duty cycle
- app2: active 0s-420s, no duty cycle
- end-users: active 0s-420s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 420.0 | n/a (never converged in this phase) | n/a |

**Windows** (45 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 13552.0 | 21.1% | 15.4% | -5.6 |
| 0.0 | 10.0 | app2 | True | 17618.0 | 10.5% | 20.0% | 9.5 |
| 0.0 | 10.0 | end-users | True | 56758.0 | 68.4% | 64.6% | -3.9 |
| 10.0 | 20.0 | app1 | True | 28392.0 | 21.1% | 15.0% | -6.1 |
| 10.0 | 20.0 | app2 | True | 24326.0 | 10.5% | 12.8% | 2.3 |
| 10.0 | 20.0 | end-users | True | 136628.0 | 68.4% | 72.2% | 3.7 |
| 20.0 | 30.0 | app1 | True | 31186.0 | 21.1% | 20.0% | -1.0 |
| 20.0 | 30.0 | app2 | True | 16214.0 | 10.5% | 10.4% | -0.1 |
| 20.0 | 30.0 | end-users | True | 108366.0 | 68.4% | 69.6% | 1.1 |
| 30.0 | 40.0 | app1 | True | 25676.0 | 21.1% | 15.9% | -5.1 |
| 30.0 | 40.0 | app2 | True | 17600.0 | 10.5% | 10.9% | 0.4 |
| 30.0 | 40.0 | end-users | True | 117738.0 | 68.4% | 73.1% | 4.7 |
| 40.0 | 50.0 | app1 | True | 10850.0 | 21.1% | 7.1% | -14.0 |
| 40.0 | 50.0 | app2 | True | 20270.0 | 10.5% | 13.3% | 2.7 |
| 40.0 | 50.0 | end-users | True | 121788.0 | 68.4% | 79.6% | 11.2 |
| 50.0 | 60.0 | app1 | True | 55420.0 | 21.1% | 34.1% | 13.1 |
| 50.0 | 60.0 | app2 | True | 37942.0 | 10.5% | 23.4% | 12.8 |
| 50.0 | 60.0 | end-users | True | 69000.0 | 68.4% | 42.5% | -25.9 |
| 60.0 | 70.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 60.0 | 70.0 | app2 | True | 10828.0 | 10.5% | 6.6% | -3.9 |
| 60.0 | 70.0 | end-users | True | 152954.0 | 68.4% | 93.4% | 25.0 |
| 70.0 | 80.0 | app1 | True | 31156.0 | 21.1% | 21.9% | 0.9 |
| 70.0 | 80.0 | app2 | True | 14908.0 | 10.5% | 10.5% | -0.0 |
| 70.0 | 80.0 | end-users | True | 96036.0 | 68.4% | 67.6% | -0.8 |
| 80.0 | 90.0 | app1 | True | 40562.0 | 21.1% | 25.0% | 3.9 |
| 80.0 | 90.0 | app2 | True | 40592.0 | 10.5% | 25.0% | 14.5 |
| 80.0 | 90.0 | end-users | True | 81116.0 | 68.4% | 50.0% | -18.4 |
| 90.0 | 100.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.2 |
| 90.0 | 100.0 | app2 | True | 2702.0 | 10.5% | 1.6% | -8.9 |
| 90.0 | 100.0 | end-users | True | 163460.0 | 68.4% | 97.6% | 29.2 |
| 100.0 | 110.0 | app1 | True | 69058.0 | 21.1% | 42.6% | 21.5 |
| 100.0 | 110.0 | app2 | True | 36432.0 | 10.5% | 22.5% | 11.9 |
| 100.0 | 110.0 | end-users | True | 56790.0 | 68.4% | 35.0% | -33.4 |
| 110.0 | 120.0 | app1 | True | 4070.0 | 21.1% | 2.8% | -18.2 |
| 110.0 | 120.0 | app2 | True | 21650.0 | 10.5% | 15.0% | 4.4 |
| 110.0 | 120.0 | end-users | True | 118934.0 | 68.4% | 82.2% | 13.8 |
| 120.0 | 130.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 120.0 | 130.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 120.0 | 130.0 | end-users | True | 167952.0 | 68.4% | 100.0% | 31.6 |
| 130.0 | 140.0 | app1 | True | 52758.0 | 21.1% | 34.5% | 13.5 |
| 130.0 | 140.0 | app2 | True | 58196.0 | 10.5% | 38.1% | 27.6 |
| 130.0 | 140.0 | end-users | True | 41858.0 | 68.4% | 27.4% | -41.0 |
| 140.0 | 150.0 | app1 | True | 24322.0 | 21.1% | 14.9% | -6.2 |
| 140.0 | 150.0 | app2 | True | 1348.0 | 10.5% | 0.8% | -9.7 |
| 140.0 | 150.0 | end-users | True | 138052.0 | 68.4% | 84.3% | 15.9 |
| 150.0 | 160.0 | app1 | True | 10836.0 | 21.1% | 7.3% | -13.7 |
| 150.0 | 160.0 | app2 | True | 5428.0 | 10.5% | 3.7% | -6.8 |
| 150.0 | 160.0 | end-users | True | 131176.0 | 68.4% | 89.0% | 20.5 |
| 160.0 | 171.0 | app1 | True | 62254.0 | 21.1% | 39.7% | 18.6 |
| 160.0 | 171.0 | app2 | True | 54064.0 | 10.5% | 34.5% | 23.9 |
| 160.0 | 171.0 | end-users | True | 40524.0 | 68.4% | 25.8% | -42.6 |
| 171.0 | 181.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 171.0 | 181.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 171.0 | 181.0 | end-users | True | 163674.0 | 68.4% | 100.0% | 31.6 |
| 181.0 | 191.0 | app1 | True | 37896.0 | 21.1% | 25.0% | 3.9 |
| 181.0 | 191.0 | app2 | True | 20328.0 | 10.5% | 13.4% | 2.9 |
| 181.0 | 191.0 | end-users | True | 93458.0 | 68.4% | 61.6% | -6.8 |
| 191.0 | 201.0 | app1 | True | 32518.0 | 21.1% | 21.5% | 0.4 |
| 191.0 | 201.0 | app2 | True | 36586.0 | 10.5% | 24.1% | 13.6 |
| 191.0 | 201.0 | end-users | True | 82480.0 | 68.4% | 54.4% | -14.0 |
| 201.0 | 211.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 201.0 | 211.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 201.0 | 211.0 | end-users | True | 167536.0 | 68.4% | 100.0% | 31.6 |
| 211.0 | 221.0 | app1 | True | 70432.0 | 21.1% | 44.1% | 23.0 |
| 211.0 | 221.0 | app2 | True | 37916.0 | 10.5% | 23.7% | 13.2 |
| 211.0 | 221.0 | end-users | True | 51432.0 | 68.4% | 32.2% | -36.2 |
| 221.0 | 231.0 | app1 | True | 4044.0 | 21.1% | 2.8% | -18.2 |
| 221.0 | 231.0 | app2 | True | 21694.0 | 10.5% | 15.1% | 4.6 |
| 221.0 | 231.0 | end-users | True | 117560.0 | 68.4% | 82.0% | 13.6 |
| 231.0 | 241.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 231.0 | 241.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 231.0 | 241.0 | end-users | True | 169154.0 | 68.4% | 100.0% | 31.6 |
| 241.0 | 251.0 | app1 | True | 50084.0 | 21.1% | 33.1% | 12.0 |
| 241.0 | 251.0 | app2 | True | 63548.0 | 10.5% | 42.0% | 31.4 |
| 241.0 | 251.0 | end-users | True | 37834.0 | 68.4% | 25.0% | -43.4 |
| 251.0 | 261.0 | app1 | True | 32410.0 | 21.1% | 22.4% | 1.4 |
| 251.0 | 261.0 | app2 | True | 2704.0 | 10.5% | 1.9% | -8.7 |
| 251.0 | 261.0 | end-users | True | 109444.0 | 68.4% | 75.7% | 7.3 |
| 261.0 | 271.0 | app1 | True | 4060.0 | 21.1% | 2.4% | -18.7 |
| 261.0 | 271.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 261.0 | 271.0 | end-users | True | 166386.0 | 68.4% | 97.6% | 29.2 |
| 271.0 | 281.0 | app1 | True | 71754.0 | 21.1% | 46.1% | 25.1 |
| 271.0 | 281.0 | app2 | True | 56804.0 | 10.5% | 36.5% | 26.0 |
| 271.0 | 281.0 | end-users | True | 27014.0 | 68.4% | 17.4% | -51.1 |
| 281.0 | 291.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 281.0 | 291.0 | app2 | True | 1322.0 | 10.5% | 0.8% | -9.7 |
| 281.0 | 291.0 | end-users | True | 159702.0 | 68.4% | 99.2% | 30.8 |
| 291.0 | 301.0 | app1 | True | 21668.0 | 21.1% | 14.4% | -6.6 |
| 291.0 | 301.0 | app2 | True | 10800.0 | 10.5% | 7.2% | -3.3 |
| 291.0 | 301.0 | end-users | True | 117618.0 | 68.4% | 78.4% | 9.9 |
| 301.0 | 311.0 | app1 | True | 43278.0 | 21.1% | 27.4% | 6.3 |
| 301.0 | 311.0 | app2 | True | 48680.0 | 10.5% | 30.8% | 20.2 |
| 301.0 | 311.0 | end-users | True | 66262.0 | 68.4% | 41.9% | -26.5 |
| 311.0 | 321.0 | app1 | True | 12176.0 | 21.1% | 7.5% | -13.6 |
| 311.0 | 321.0 | app2 | True | 1346.0 | 10.5% | 0.8% | -9.7 |
| 311.0 | 321.0 | end-users | True | 148792.0 | 68.4% | 91.7% | 23.2 |
| 321.0 | 331.0 | app1 | True | 31040.0 | 21.1% | 21.6% | 0.6 |
| 321.0 | 331.0 | app2 | True | 16266.0 | 10.5% | 11.3% | 0.8 |
| 321.0 | 331.0 | end-users | True | 96156.0 | 68.4% | 67.0% | -1.4 |
| 331.0 | 341.0 | app1 | True | 37850.0 | 21.1% | 23.7% | 2.7 |
| 331.0 | 341.0 | app2 | True | 43220.0 | 10.5% | 27.1% | 16.6 |
| 331.0 | 341.0 | end-users | True | 78544.0 | 68.4% | 49.2% | -19.2 |
| 341.0 | 351.0 | app1 | True | 9470.0 | 21.1% | 5.8% | -15.2 |
| 341.0 | 351.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 341.0 | 351.0 | end-users | True | 152926.0 | 68.4% | 94.2% | 25.7 |
| 351.0 | 361.0 | app1 | True | 43316.0 | 21.1% | 28.1% | 7.0 |
| 351.0 | 361.0 | app2 | True | 46034.0 | 10.5% | 29.8% | 19.3 |
| 351.0 | 361.0 | end-users | True | 64936.0 | 68.4% | 42.1% | -26.3 |
| 361.0 | 371.0 | app1 | True | 31116.0 | 21.1% | 21.5% | 0.4 |
| 361.0 | 371.0 | app2 | True | 13580.0 | 10.5% | 9.4% | -1.1 |
| 361.0 | 371.0 | end-users | True | 100084.0 | 68.4% | 69.1% | 0.7 |
| 371.0 | 381.0 | app1 | True | 4044.0 | 21.1% | 2.4% | -18.6 |
| 371.0 | 381.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 371.0 | 381.0 | end-users | True | 161092.0 | 68.4% | 97.6% | 29.1 |
| 381.0 | 391.0 | app1 | True | 47298.0 | 21.1% | 29.9% | 8.8 |
| 381.0 | 391.0 | app2 | True | 56820.0 | 10.5% | 35.9% | 25.4 |
| 381.0 | 391.0 | end-users | True | 54204.0 | 68.4% | 34.2% | -34.2 |
| 391.0 | 401.0 | app1 | True | 28418.0 | 21.1% | 19.6% | -1.4 |
| 391.0 | 401.0 | app2 | True | 1358.0 | 10.5% | 0.9% | -9.6 |
| 391.0 | 401.0 | end-users | True | 114946.0 | 68.4% | 79.4% | 11.0 |
| 401.0 | 411.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 401.0 | 411.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 401.0 | 411.0 | end-users | True | 167742.0 | 68.4% | 100.0% | 31.6 |
| 411.0 | 421.0 | app1 | True | 55458.0 | 21.1% | 36.0% | 14.9 |
| 411.0 | 421.0 | app2 | True | 60886.0 | 10.5% | 39.5% | 29.0 |
| 411.0 | 421.0 | end-users | True | 37852.0 | 68.4% | 24.5% | -43.9 |
| 421.0 | 431.0 | app1 | False | 20252.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | end-users | False | 139178.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | False | 21638.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | False | 43258.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | end-users | False | 24310.0 | n/a | n/a | n/a |
| 441.0 | 450.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 450.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 450.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1078710 | 53911 | 1128745.0 | -0.3% | 1171670.0 | 1186532.0 | -1.3% | True |
| app2 | 890520 | 44493 | 935013.0 | 0.0% | 963268.0 | 979506.0 | -1.7% | True |
| end-users | 4300080 | 214421 | 4508039.0 | -0.1% | 4669446.0 | 4728922.0 | -1.3% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 889 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 737 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3553 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide):** not recorded -- `llm_d_epp_flow_control_requests_total` is absent from both snapshots, so whether the EPP or something in front of it (Kuadrant) produced the client's 429s is unknown.

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
