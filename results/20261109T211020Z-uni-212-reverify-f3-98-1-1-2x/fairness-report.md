# Fairness benchmark: full-contention-2x (uni-212-reverify-f3-98-1-1-2x)

**Verdict: FAIL** (threshold: 10 points)

- app1 deviated -80.2 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-946d96bdc-vtrjl` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T21:11:33Z` |
| Run end | `2026-11-09T21:19:57Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 98.0 | 64 | 967 | 200=948, 500=19 | 16.6 | 18.8 | 1157436.0 | 98.0% | 17.8% | -80.2 | 16.9% | -81.1 | 6.7s | 98.9% | 947.0 |
| app2 | 1.0 | 64 | 939 | 000=2, 200=915, 500=22 | 16.9 | 19.4 | 1099234.0 | 1.0% | 16.9% | 15.9 | 16.4% | 15.4 | 7.2s | 98.9% | 916.0 |
| end-users | 1.0 | 256 | 3806 | 000=4, 200=3721, 500=81 | 16.5 | 19.0 | 4253068.0 | 1.0% | 65.3% | 64.3 | 66.6% | 65.6 | 7.1s | 98.9% | 3719.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 8.0 |

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

**Windows** (51 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 98.0% | 0.0% | -98.0 |
| 0.0 | 10.0 | app2 | True | 0.0 | 1.0% | 0.0% | -1.0 |
| 0.0 | 10.0 | end-users | True | 0.0 | 1.0% | 0.0% | -1.0 |
| 10.0 | 20.0 | app1 | True | 0.0 | 98.0% | 0.0% | -98.0 |
| 10.0 | 20.0 | app2 | True | 0.0 | 1.0% | 0.0% | -1.0 |
| 10.0 | 20.0 | end-users | True | 0.0 | 1.0% | 0.0% | -1.0 |
| 20.0 | 30.0 | app1 | True | 0.0 | 98.0% | 0.0% | -98.0 |
| 20.0 | 30.0 | app2 | True | 0.0 | 1.0% | 0.0% | -1.0 |
| 20.0 | 30.0 | end-users | True | 0.0 | 1.0% | 0.0% | -1.0 |
| 30.0 | 41.0 | app1 | True | 37902.0 | 98.0% | 18.9% | -79.1 |
| 30.0 | 41.0 | app2 | True | 31086.0 | 1.0% | 15.5% | 14.5 |
| 30.0 | 41.0 | end-users | True | 131226.0 | 1.0% | 65.5% | 64.5 |
| 41.0 | 51.0 | app1 | True | 59398.0 | 98.0% | 19.4% | -78.6 |
| 41.0 | 51.0 | app2 | True | 44640.0 | 1.0% | 14.6% | 13.6 |
| 41.0 | 51.0 | end-users | True | 201572.0 | 1.0% | 66.0% | 65.0 |
| 51.0 | 61.0 | app1 | True | 46018.0 | 98.0% | 15.1% | -82.9 |
| 51.0 | 61.0 | app2 | True | 64858.0 | 1.0% | 21.3% | 20.3 |
| 51.0 | 61.0 | end-users | True | 193312.0 | 1.0% | 63.6% | 62.6 |
| 61.0 | 71.0 | app1 | True | 67682.0 | 98.0% | 22.4% | -75.6 |
| 61.0 | 71.0 | app2 | True | 43346.0 | 1.0% | 14.4% | 13.4 |
| 61.0 | 71.0 | end-users | True | 190670.0 | 1.0% | 63.2% | 62.2 |
| 71.0 | 81.0 | app1 | True | 21664.0 | 98.0% | 7.2% | -90.8 |
| 71.0 | 81.0 | app2 | True | 49956.0 | 1.0% | 16.5% | 15.5 |
| 71.0 | 81.0 | end-users | True | 231158.0 | 1.0% | 76.3% | 75.3 |
| 81.0 | 91.0 | app1 | True | 65014.0 | 98.0% | 21.4% | -76.6 |
| 81.0 | 91.0 | app2 | True | 52638.0 | 1.0% | 17.3% | 16.3 |
| 81.0 | 91.0 | end-users | True | 186566.0 | 1.0% | 61.3% | 60.3 |
| 91.0 | 101.0 | app1 | True | 59526.0 | 98.0% | 19.7% | -78.3 |
| 91.0 | 101.0 | app2 | True | 35162.0 | 1.0% | 11.7% | 10.7 |
| 91.0 | 101.0 | end-users | True | 206878.0 | 1.0% | 68.6% | 67.6 |
| 101.0 | 111.0 | app1 | True | 37884.0 | 98.0% | 12.5% | -85.5 |
| 101.0 | 111.0 | app2 | True | 52826.0 | 1.0% | 17.4% | 16.4 |
| 101.0 | 111.0 | end-users | True | 212142.0 | 1.0% | 70.0% | 69.0 |
| 111.0 | 121.0 | app1 | True | 71594.0 | 98.0% | 23.7% | -74.3 |
| 111.0 | 121.0 | app2 | True | 64938.0 | 1.0% | 21.5% | 20.5 |
| 111.0 | 121.0 | end-users | True | 166190.0 | 1.0% | 54.9% | 53.9 |
| 121.0 | 131.0 | app1 | True | 36430.0 | 98.0% | 12.1% | -85.9 |
| 121.0 | 131.0 | app2 | True | 39250.0 | 1.0% | 13.0% | 12.0 |
| 121.0 | 131.0 | end-users | True | 225830.0 | 1.0% | 74.9% | 73.9 |
| 131.0 | 141.0 | app1 | True | 54052.0 | 98.0% | 17.8% | -80.2 |
| 131.0 | 141.0 | app2 | True | 54082.0 | 1.0% | 17.8% | 16.8 |
| 131.0 | 141.0 | end-users | True | 195928.0 | 1.0% | 64.4% | 63.4 |
| 141.0 | 151.0 | app1 | True | 54084.0 | 98.0% | 18.1% | -79.9 |
| 141.0 | 151.0 | app2 | True | 52724.0 | 1.0% | 17.7% | 16.7 |
| 141.0 | 151.0 | end-users | True | 191850.0 | 1.0% | 64.2% | 63.2 |
| 151.0 | 161.0 | app1 | True | 33906.0 | 98.0% | 11.3% | -86.7 |
| 151.0 | 161.0 | app2 | True | 31004.0 | 1.0% | 10.4% | 9.4 |
| 151.0 | 161.0 | end-users | True | 234074.0 | 1.0% | 78.3% | 77.3 |
| 161.0 | 171.0 | app1 | True | 75746.0 | 98.0% | 24.9% | -73.1 |
| 161.0 | 171.0 | app2 | True | 69006.0 | 1.0% | 22.7% | 21.7 |
| 161.0 | 171.0 | end-users | True | 159632.0 | 1.0% | 52.4% | 51.4 |
| 171.0 | 181.0 | app1 | True | 36438.0 | 98.0% | 12.2% | -85.8 |
| 171.0 | 181.0 | app2 | True | 17616.0 | 1.0% | 5.9% | 4.9 |
| 171.0 | 181.0 | end-users | True | 244810.0 | 1.0% | 81.9% | 80.9 |
| 181.0 | 191.0 | app1 | True | 58058.0 | 98.0% | 19.3% | -78.7 |
| 181.0 | 191.0 | app2 | True | 74420.0 | 1.0% | 24.7% | 23.7 |
| 181.0 | 191.0 | end-users | True | 168970.0 | 1.0% | 56.1% | 55.1 |
| 191.0 | 201.0 | app1 | True | 28428.0 | 98.0% | 9.3% | -88.7 |
| 191.0 | 201.0 | app2 | True | 54114.0 | 1.0% | 17.8% | 16.8 |
| 191.0 | 201.0 | end-users | True | 221676.0 | 1.0% | 72.9% | 71.9 |
| 201.0 | 211.0 | app1 | True | 58154.0 | 98.0% | 19.2% | -78.8 |
| 201.0 | 211.0 | app2 | True | 29742.0 | 1.0% | 9.8% | 8.8 |
| 201.0 | 211.0 | end-users | True | 214900.0 | 1.0% | 71.0% | 70.0 |
| 211.0 | 221.0 | app1 | True | 75640.0 | 98.0% | 24.9% | -73.1 |
| 211.0 | 221.0 | app2 | True | 58128.0 | 1.0% | 19.1% | 18.1 |
| 211.0 | 221.0 | end-users | True | 170058.0 | 1.0% | 56.0% | 55.0 |
| 221.0 | 231.0 | app1 | True | 29710.0 | 98.0% | 13.5% | -84.5 |
| 221.0 | 231.0 | app2 | True | 55378.0 | 1.0% | 25.1% | 24.1 |
| 221.0 | 231.0 | end-users | True | 135304.0 | 1.0% | 61.4% | 60.4 |
| 231.0 | 241.0 | app1 | True | 64908.0 | 98.0% | 23.5% | -74.5 |
| 231.0 | 241.0 | app2 | True | 41876.0 | 1.0% | 15.2% | 14.2 |
| 231.0 | 241.0 | end-users | True | 168916.0 | 1.0% | 61.3% | 60.3 |
| 241.0 | 251.0 | app1 | False | 32494.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 62150.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 144664.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 52706.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 20294.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 56742.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 422.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 422.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 422.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 502.0 | 504.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 502.0 | 504.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 502.0 | 504.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 28 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 29 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 115 | 0ms | 0ms | 1ms |
| 10.0 | 20.0 | app1 | ok | 59 | 0ms | 0ms | 161ms |
| 10.0 | 20.0 | app2 | ok | 61 | 0ms | 0ms | 159ms |
| 10.0 | 20.0 | end-users | ok | 228 | 0ms | 0ms | 14ms |
| 20.0 | 30.0 | app1 | ok | 43 | 594ms | 2459ms | 4731ms |
| 20.0 | 30.0 | app2 | ok | 38 | 812ms | 2307ms | 4525ms |
| 20.0 | 30.0 | end-users | ok | 163 | 863ms | 2389ms | 4660ms |
| 30.0 | 41.0 | app1 | ok | 49 | 804ms | 2958ms | 4796ms |
| 30.0 | 41.0 | app2 | ok | 43 | 1679ms | 3925ms | 4892ms |
| 30.0 | 41.0 | end-users | ok | 166 | 1719ms | 3742ms | 4874ms |
| 41.0 | 51.0 | app1 | ok | 26 | 900ms | 3917ms | 4892ms |
| 41.0 | 51.0 | app2 | ok | 29 | 1685ms | 2441ms | 4638ms |
| 41.0 | 51.0 | end-users | ok | 135 | 1659ms | 3702ms | 4870ms |
| 51.0 | 61.0 | app1 | ok | 52 | 1180ms | 2428ms | 4675ms |
| 51.0 | 61.0 | app2 | ok | 39 | 1250ms | 2364ms | 4512ms |
| 51.0 | 61.0 | end-users | ok | 164 | 1521ms | 2950ms | 4795ms |
| 61.0 | 71.0 | app1 | ok | 50 | 1360ms | 2917ms | 4792ms |
| 61.0 | 71.0 | app2 | ok | 46 | 1750ms | 4115ms | 4912ms |
| 61.0 | 71.0 | end-users | ok | 151 | 1375ms | 2428ms | 4657ms |
| 71.0 | 81.0 | app1 | ok | 16 | 500ms | 1700ms | 2420ms |
| 71.0 | 81.0 | app2 | ok | 29 | 1488ms | 2358ms | 4275ms |
| 71.0 | 81.0 | end-users | ok | 146 | 1463ms | 2853ms | 4785ms |
| 81.0 | 91.0 | app1 | ok | 48 | 906ms | 2350ms | 4600ms |
| 81.0 | 91.0 | app2 | ok | 49 | 1543ms | 2958ms | 4796ms |
| 81.0 | 91.0 | end-users | ok | 163 | 1340ms | 2477ms | 4728ms |
| 91.0 | 101.0 | app1 | ok | 26 | 714ms | 2833ms | 4783ms |
| 91.0 | 101.0 | app2 | ok | 16 | 1000ms | 2371ms | 4600ms |
| 91.0 | 101.0 | end-users | ok | 146 | 1643ms | 3262ms | 4826ms |
| 101.0 | 111.0 | app1 | ok | 42 | 1389ms | 2322ms | 3950ms |
| 101.0 | 111.0 | app2 | ok | 49 | 1630ms | 3775ms | 4877ms |
| 101.0 | 111.0 | end-users | ok | 158 | 1388ms | 2531ms | 4753ms |
| 111.0 | 121.0 | app1 | ok | 45 | 1330ms | 2410ms | 4625ms |
| 111.0 | 121.0 | app2 | ok | 32 | 409ms | 2133ms | 4200ms |
| 111.0 | 121.0 | end-users | ok | 112 | 1697ms | 3444ms | 4844ms |
| 121.0 | 131.0 | app1 | ok | 29 | 1141ms | 2228ms | 2473ms |
| 121.0 | 131.0 | app2 | ok | 36 | 1643ms | 4100ms | 4910ms |
| 121.0 | 131.0 | end-users | ok | 179 | 1502ms | 2869ms | 4787ms |
| 131.0 | 141.0 | app1 | ok | 50 | 1574ms | 2456ms | 4688ms |
| 131.0 | 141.0 | app2 | ok | 50 | 1692ms | 4306ms | 4931ms |
| 131.0 | 141.0 | end-users | ok | 143 | 1343ms | 2402ms | 4603ms |
| 141.0 | 151.0 | app1 | ok | 21 | 1312ms | 2362ms | 4475ms |
| 141.0 | 151.0 | app2 | ok | 19 | 1281ms | 3417ms | 4842ms |
| 141.0 | 151.0 | end-users | ok | 152 | 1488ms | 2889ms | 4789ms |
| 151.0 | 161.0 | app1 | ok | 44 | 964ms | 2383ms | 4633ms |
| 151.0 | 161.0 | app2 | ok | 48 | 1750ms | 3667ms | 4867ms |
| 151.0 | 161.0 | end-users | ok | 171 | 1266ms | 2369ms | 4525ms |
| 161.0 | 171.0 | app1 | ok | 40 | 1300ms | 2260ms | 2476ms |
| 161.0 | 171.0 | app2 | ok | 39 | 1250ms | 3607ms | 4861ms |
| 161.0 | 171.0 | end-users | ok | 111 | 1375ms | 2449ms | 4692ms |
| 171.0 | 181.0 | app1 | ok | 33 | 458ms | 2323ms | 4588ms |
| 171.0 | 181.0 | app2 | ok | 26 | 1136ms | 2833ms | 4783ms |
| 171.0 | 181.0 | end-users | ok | 203 | 1548ms | 3048ms | 4805ms |
| 181.0 | 191.0 | app1 | ok | 53 | 1683ms | 2390ms | 4337ms |
| 181.0 | 191.0 | app2 | ok | 55 | 574ms | 2125ms | 4542ms |
| 181.0 | 191.0 | end-users | ok | 86 | 1467ms | 3208ms | 4821ms |
| 191.0 | 201.0 | app1 | ok | 22 | 1667ms | 2400ms | 4450ms |
| 191.0 | 201.0 | app2 | ok | 43 | 1393ms | 3208ms | 4821ms |
| 191.0 | 201.0 | end-users | ok | 199 | 1278ms | 2472ms | 4724ms |
| 201.0 | 211.0 | app1 | ok | 43 | 1450ms | 2482ms | 4731ms |
| 201.0 | 211.0 | app2 | ok | 22 | 778ms | 2029ms | 2453ms |
| 201.0 | 211.0 | end-users | ok | 129 | 1365ms | 2440ms | 4677ms |
| 211.0 | 221.0 | app1 | ok | 46 | 1062ms | 2212ms | 2471ms |
| 211.0 | 221.0 | app2 | ok | 40 | 1562ms | 3000ms | 4800ms |
| 211.0 | 221.0 | end-users | ok | 164 | 1337ms | 2443ms | 4685ms |
| 221.0 | 231.0 | app1 | ok | 30 | 955ms | 2500ms | 4750ms |
| 221.0 | 231.0 | app2 | ok | 47 | 1284ms | 2257ms | 2476ms |
| 221.0 | 231.0 | end-users | ok | 178 | 1429ms | 2658ms | 4766ms |
| 231.0 | 241.0 | app1 | ok | 52 | 1387ms | 2394ms | 4567ms |
| 231.0 | 241.0 | app2 | ok | 31 | 1708ms | 3708ms | 4871ms |
| 231.0 | 241.0 | end-users | ok | 92 | 1368ms | 2409ms | 4617ms |
| 241.0 | 251.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 65 | 1250ms | 2432ms | 4675ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 422.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 422.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 422.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 504.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 504.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 504.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -11.1%
- end-users exceeded the 10% ledger tolerance: cost -15.4%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1166040 | 57911 | 1222663.0 | -0.1% | 1157436.0 | 1281862.0 | -9.7% | True |
| app2 | 1125450 | 55842 | 1180000.0 | -0.1% | 1099234.0 | 1237134.0 | -11.1% | False |
| end-users | 4576830 | 226597 | 4795691.0 | -0.2% | 4253068.0 | 5030024.0 | -15.4% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 967 | 0 | 0 | 0 (never shed) | 0.00% | 98.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 939 | 0 | 0 | 0 (never shed) | 0.00% | 1.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3806 | 0 | 0 | 0 (never shed) | 0.00% | 1.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5590). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5590 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 481568 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
