# Fairness benchmark: full-contention-2x (uni-212-reverify-f3-33-33-33-2x)

**Verdict: FAIL** (threshold: 10 points)

- end-users deviated +33.3 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-6fdcd48b9d-qpwtv` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T21:24:42Z` |
| Run end | `2026-11-09T21:33:05Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 33.0 | 64 | 951 | 200=935, 500=16 | 16.9 | 19.4 | 1128810.0 | 33.3% | 16.9% | -16.5 | 16.6% | -16.7 | 8.1s | 98.9% | 934.0 |
| app2 | 33.0 | 64 | 948 | 000=2, 200=922, 500=24 | 16.9 | 19.7 | 1106436.0 | 33.3% | 16.5% | -16.8 | 16.6% | -16.8 | 8.1s | 98.9% | 924.0 |
| end-users | 33.0 | 256 | 3828 | 000=3, 200=3767, 500=58 | 16.6 | 19.0 | 4454960.0 | 33.3% | 66.6% | 33.3 | 66.8% | 33.5 | 8.1s | 98.9% | 3768.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 3.0 |

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
| 0.0 | 10.0 | app1 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 0.0 | 10.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 0.0 | 10.0 | end-users | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 10.0 | 20.0 | app1 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 10.0 | 20.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 10.0 | 20.0 | end-users | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 20.0 | 30.0 | app1 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 20.0 | 30.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 20.0 | 30.0 | end-users | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 30.0 | 40.0 | app1 | True | 31058.0 | 33.3% | 16.2% | -17.2 |
| 30.0 | 40.0 | app2 | True | 35202.0 | 33.3% | 18.3% | -15.0 |
| 30.0 | 40.0 | end-users | True | 125726.0 | 33.3% | 65.5% | 32.2 |
| 40.0 | 50.0 | app1 | True | 52606.0 | 33.3% | 17.1% | -16.3 |
| 40.0 | 50.0 | app2 | True | 47292.0 | 33.3% | 15.3% | -18.0 |
| 40.0 | 50.0 | end-users | True | 208204.0 | 33.3% | 67.6% | 34.2 |
| 50.0 | 60.0 | app1 | True | 40572.0 | 33.3% | 13.5% | -19.9 |
| 50.0 | 60.0 | app2 | True | 50058.0 | 33.3% | 16.6% | -16.7 |
| 50.0 | 60.0 | end-users | True | 210854.0 | 33.3% | 69.9% | 36.6 |
| 60.0 | 70.0 | app1 | True | 66310.0 | 33.3% | 21.8% | -11.5 |
| 60.0 | 70.0 | app2 | True | 56814.0 | 33.3% | 18.7% | -14.7 |
| 60.0 | 70.0 | end-users | True | 181234.0 | 33.3% | 59.5% | 26.2 |
| 70.0 | 80.0 | app1 | True | 40502.0 | 33.3% | 13.4% | -19.9 |
| 70.0 | 80.0 | app2 | True | 51360.0 | 33.3% | 17.0% | -16.4 |
| 70.0 | 80.0 | end-users | True | 210750.0 | 33.3% | 69.6% | 36.3 |
| 80.0 | 90.0 | app1 | True | 60730.0 | 33.3% | 20.1% | -13.3 |
| 80.0 | 90.0 | app2 | True | 47356.0 | 33.3% | 15.6% | -17.7 |
| 80.0 | 90.0 | end-users | True | 194682.0 | 33.3% | 64.3% | 31.0 |
| 90.0 | 100.0 | app1 | True | 41938.0 | 33.3% | 13.8% | -19.6 |
| 90.0 | 100.0 | app2 | True | 45992.0 | 33.3% | 15.1% | -18.2 |
| 90.0 | 100.0 | end-users | True | 216358.0 | 33.3% | 71.1% | 37.8 |
| 100.0 | 110.0 | app1 | True | 49902.0 | 33.3% | 16.5% | -16.8 |
| 100.0 | 110.0 | app2 | True | 48820.0 | 33.3% | 16.2% | -17.1 |
| 100.0 | 110.0 | end-users | True | 202884.0 | 33.3% | 67.3% | 33.9 |
| 110.0 | 120.0 | app1 | True | 47374.0 | 33.3% | 15.8% | -17.6 |
| 110.0 | 120.0 | app2 | True | 44562.0 | 33.3% | 14.8% | -18.5 |
| 110.0 | 120.0 | end-users | True | 208314.0 | 33.3% | 69.4% | 36.0 |
| 120.0 | 130.0 | app1 | True | 62278.0 | 33.3% | 20.8% | -12.6 |
| 120.0 | 130.0 | app2 | True | 55346.0 | 33.3% | 18.4% | -14.9 |
| 120.0 | 130.0 | end-users | True | 182446.0 | 33.3% | 60.8% | 27.5 |
| 130.0 | 140.0 | app1 | True | 54030.0 | 33.3% | 17.8% | -15.5 |
| 130.0 | 140.0 | app2 | True | 60818.0 | 33.3% | 20.1% | -13.3 |
| 130.0 | 140.0 | end-users | True | 188034.0 | 33.3% | 62.1% | 28.7 |
| 140.0 | 150.0 | app1 | True | 31102.0 | 33.3% | 10.3% | -23.1 |
| 140.0 | 150.0 | app2 | True | 33830.0 | 33.3% | 11.2% | -22.2 |
| 140.0 | 150.0 | end-users | True | 237968.0 | 33.3% | 78.6% | 45.2 |
| 150.0 | 160.0 | app1 | True | 56784.0 | 33.3% | 19.1% | -14.3 |
| 150.0 | 160.0 | app2 | True | 52836.0 | 33.3% | 17.7% | -15.6 |
| 150.0 | 160.0 | end-users | True | 188144.0 | 33.3% | 63.2% | 29.9 |
| 160.0 | 170.0 | app1 | True | 44644.0 | 33.3% | 14.9% | -18.5 |
| 160.0 | 170.0 | app2 | True | 51376.0 | 33.3% | 17.1% | -16.2 |
| 160.0 | 170.0 | end-users | True | 204178.0 | 33.3% | 68.0% | 34.7 |
| 170.0 | 180.0 | app1 | True | 60886.0 | 33.3% | 20.1% | -13.2 |
| 170.0 | 180.0 | app2 | True | 52800.0 | 33.3% | 17.4% | -15.9 |
| 170.0 | 180.0 | end-users | True | 189244.0 | 33.3% | 62.5% | 29.1 |
| 180.0 | 190.0 | app1 | True | 36496.0 | 33.3% | 12.2% | -21.2 |
| 180.0 | 190.0 | app2 | True | 43226.0 | 33.3% | 14.4% | -18.9 |
| 180.0 | 190.0 | end-users | True | 220332.0 | 33.3% | 73.4% | 40.1 |
| 190.0 | 200.0 | app1 | True | 55330.0 | 33.3% | 21.8% | -11.6 |
| 190.0 | 200.0 | app2 | True | 51500.0 | 33.3% | 20.2% | -13.1 |
| 190.0 | 200.0 | end-users | True | 147540.0 | 33.3% | 58.0% | 24.7 |
| 200.0 | 210.0 | app1 | True | 69002.0 | 33.3% | 26.4% | -6.9 |
| 200.0 | 210.0 | app2 | True | 45992.0 | 33.3% | 17.6% | -15.7 |
| 200.0 | 210.0 | end-users | True | 146022.0 | 33.3% | 55.9% | 22.6 |
| 210.0 | 220.0 | app1 | True | 21646.0 | 33.3% | 7.1% | -26.2 |
| 210.0 | 220.0 | app2 | True | 54086.0 | 33.3% | 17.7% | -15.6 |
| 210.0 | 220.0 | end-users | True | 229742.0 | 33.3% | 75.2% | 41.9 |
| 220.0 | 230.0 | app1 | True | 70422.0 | 33.3% | 23.7% | -9.7 |
| 220.0 | 230.0 | app2 | True | 54106.0 | 33.3% | 18.2% | -15.1 |
| 220.0 | 230.0 | end-users | True | 172846.0 | 33.3% | 58.1% | 24.8 |
| 230.0 | 240.0 | app1 | True | 37890.0 | 33.3% | 12.5% | -20.9 |
| 230.0 | 240.0 | app2 | True | 40538.0 | 33.3% | 13.3% | -20.0 |
| 230.0 | 240.0 | end-users | True | 225748.0 | 33.3% | 74.2% | 40.9 |
| 240.0 | 250.0 | app1 | False | 54014.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 40534.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 206840.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 43294.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 41992.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 156870.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 330.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 330.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 330.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 330.0 | 340.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 330.0 | 340.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 330.0 | 340.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 340.0 | 350.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 340.0 | 350.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 340.0 | 350.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 350.0 | 361.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 350.0 | 361.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 350.0 | 361.0 | end-users | False | 0.0 | n/a | n/a | n/a |
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
| 411.0 | 421.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 501.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 503.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 503.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 503.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 26 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 27 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 128 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 63 | 0ms | 0ms | 84ms |
| 10.0 | 20.0 | app2 | ok | 66 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | end-users | ok | 242 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app1 | ok | 39 | 725ms | 2082ms | 2458ms |
| 20.0 | 30.0 | app2 | ok | 42 | 556ms | 2100ms | 3950ms |
| 20.0 | 30.0 | end-users | ok | 169 | 821ms | 2312ms | 4531ms |
| 30.0 | 40.0 | app1 | ok | 46 | 1100ms | 3722ms | 4872ms |
| 30.0 | 40.0 | app2 | ok | 44 | 1569ms | 2479ms | 4725ms |
| 30.0 | 40.0 | end-users | ok | 171 | 1658ms | 3779ms | 4878ms |
| 40.0 | 50.0 | app1 | ok | 34 | 1400ms | 3583ms | 4858ms |
| 40.0 | 50.0 | app2 | ok | 32 | 1500ms | 3000ms | 4800ms |
| 40.0 | 50.0 | end-users | ok | 131 | 1606ms | 3511ms | 4851ms |
| 50.0 | 60.0 | app1 | ok | 36 | 1450ms | 2750ms | 4775ms |
| 50.0 | 60.0 | app2 | ok | 42 | 1438ms | 2488ms | 4737ms |
| 50.0 | 60.0 | end-users | ok | 188 | 1538ms | 3657ms | 4866ms |
| 60.0 | 70.0 | app1 | ok | 42 | 1714ms | 3950ms | 4895ms |
| 60.0 | 70.0 | app2 | ok | 28 | 1346ms | 3250ms | 4825ms |
| 60.0 | 70.0 | end-users | ok | 119 | 1576ms | 3250ms | 4825ms |
| 70.0 | 80.0 | app1 | ok | 36 | 1188ms | 2750ms | 4775ms |
| 70.0 | 80.0 | app2 | ok | 51 | 1583ms | 3583ms | 4858ms |
| 70.0 | 80.0 | end-users | ok | 178 | 1526ms | 3288ms | 4829ms |
| 80.0 | 90.0 | app1 | ok | 42 | 1944ms | 4045ms | 4905ms |
| 80.0 | 90.0 | app2 | ok | 28 | 1750ms | 3250ms | 4825ms |
| 80.0 | 90.0 | end-users | ok | 122 | 1255ms | 3206ms | 4821ms |
| 90.0 | 100.0 | app1 | ok | 35 | 1434ms | 2812ms | 4781ms |
| 90.0 | 100.0 | app2 | ok | 43 | 1750ms | 4104ms | 4910ms |
| 90.0 | 100.0 | end-users | ok | 172 | 1557ms | 3280ms | 4828ms |
| 100.0 | 110.0 | app1 | ok | 33 | 1434ms | 2476ms | 4725ms |
| 100.0 | 110.0 | app2 | ok | 30 | 1643ms | 4318ms | 4932ms |
| 100.0 | 110.0 | end-users | ok | 130 | 1434ms | 2461ms | 4705ms |
| 110.0 | 120.0 | app1 | ok | 39 | 1542ms | 3781ms | 4878ms |
| 110.0 | 120.0 | app2 | ok | 38 | 1167ms | 2433ms | 4683ms |
| 110.0 | 120.0 | end-users | ok | 192 | 1510ms | 3500ms | 4850ms |
| 120.0 | 130.0 | app1 | ok | 44 | 1500ms | 3625ms | 4863ms |
| 120.0 | 130.0 | app2 | ok | 37 | 1650ms | 4075ms | 4908ms |
| 120.0 | 130.0 | end-users | ok | 114 | 1531ms | 3100ms | 4810ms |
| 130.0 | 140.0 | app1 | ok | 24 | 833ms | 3500ms | 4850ms |
| 130.0 | 140.0 | app2 | ok | 35 | 893ms | 2250ms | 4125ms |
| 130.0 | 140.0 | end-users | ok | 144 | 1494ms | 3105ms | 4811ms |
| 140.0 | 150.0 | app1 | ok | 44 | 1300ms | 2356ms | 4450ms |
| 140.0 | 150.0 | app2 | ok | 43 | 1630ms | 3464ms | 4846ms |
| 140.0 | 150.0 | end-users | ok | 167 | 1430ms | 3330ms | 4833ms |
| 150.0 | 160.0 | app1 | ok | 43 | 850ms | 2191ms | 3925ms |
| 150.0 | 160.0 | app2 | ok | 39 | 975ms | 2258ms | 4025ms |
| 150.0 | 160.0 | end-users | ok | 117 | 1588ms | 3670ms | 4867ms |
| 160.0 | 170.0 | app1 | ok | 33 | 893ms | 2350ms | 4588ms |
| 160.0 | 170.0 | app2 | ok | 36 | 1115ms | 3500ms | 4850ms |
| 160.0 | 170.0 | end-users | ok | 196 | 1504ms | 2870ms | 4787ms |
| 170.0 | 180.0 | app1 | ok | 34 | 1536ms | 3938ms | 4894ms |
| 170.0 | 180.0 | app2 | ok | 29 | 1519ms | 3792ms | 4879ms |
| 170.0 | 180.0 | end-users | ok | 135 | 1418ms | 3015ms | 4801ms |
| 180.0 | 190.0 | app1 | ok | 40 | 1300ms | 2500ms | 4750ms |
| 180.0 | 190.0 | app2 | ok | 47 | 1359ms | 3042ms | 4804ms |
| 180.0 | 190.0 | end-users | ok | 177 | 1425ms | 2671ms | 4767ms |
| 190.0 | 200.0 | app1 | ok | 42 | 1708ms | 2408ms | 4475ms |
| 190.0 | 200.0 | app2 | ok | 32 | 1250ms | 2317ms | 4200ms |
| 190.0 | 200.0 | end-users | ok | 109 | 1447ms | 3486ms | 4849ms |
| 200.0 | 210.0 | app1 | ok | 35 | 775ms | 2295ms | 4562ms |
| 200.0 | 210.0 | app2 | ok | 36 | 1450ms | 2750ms | 4775ms |
| 200.0 | 210.0 | end-users | ok | 177 | 1484ms | 2450ms | 4684ms |
| 210.0 | 220.0 | app1 | ok | 29 | 1716ms | 2583ms | 4758ms |
| 210.0 | 220.0 | app2 | ok | 33 | 1685ms | 2937ms | 4794ms |
| 210.0 | 220.0 | end-users | ok | 127 | 898ms | 2235ms | 3942ms |
| 220.0 | 230.0 | app1 | ok | 58 | 1512ms | 2361ms | 4275ms |
| 220.0 | 230.0 | app2 | ok | 44 | 1667ms | 2400ms | 4450ms |
| 220.0 | 230.0 | end-users | ok | 158 | 1172ms | 3420ms | 4842ms |
| 230.0 | 240.0 | app1 | ok | 27 | 1312ms | 3313ms | 4831ms |
| 230.0 | 240.0 | app2 | ok | 42 | 1750ms | 2413ms | 4475ms |
| 230.0 | 240.0 | end-users | ok | 158 | 1506ms | 3589ms | 4859ms |
| 240.0 | 250.0 | app1 | ok | 10 | 1750ms | 2350ms | 2485ms |
| 240.0 | 250.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | ok | 47 | 1491ms | 2464ms | 4706ms |
| 250.0 | 260.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 270.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 280.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 280.0 | 290.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 290.0 | 300.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 300.0 | 310.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 310.0 | 320.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 320.0 | 330.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 320.0 | 330.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 320.0 | 330.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 330.0 | 340.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 330.0 | 340.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 330.0 | 340.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 340.0 | 350.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 340.0 | 350.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 340.0 | 350.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 350.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 350.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 350.0 | 361.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 411.0 | 421.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 501.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 501.0 | 503.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 501.0 | 503.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 501.0 | 503.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -10.7%
- app2 exceeded the 10% ledger tolerance: cost -11.3%
- end-users exceeded the 10% ledger tolerance: cost -12.5%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1150050 | 56854 | 1205625.0 | -0.1% | 1128810.0 | 1263758.0 | -10.7% | False |
| app2 | 1134060 | 56469 | 1190529.0 | 0.0% | 1106436.0 | 1246998.0 | -11.3% | False |
| end-users | 4633410 | 229925 | 4860747.0 | -0.1% | 4454960.0 | 5093260.0 | -12.5% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 951 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 948 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3828 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5629). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5629 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 481063 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
