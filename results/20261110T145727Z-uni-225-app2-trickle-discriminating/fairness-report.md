# Fairness benchmark: app2-trickle-discriminating (uni-225-app2-trickle-discriminating)

**Verdict: FAIL** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 31.6 points

- end-users deviated -26.2 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `app2-trickle-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-85575669d6-xsvx5` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-10T14:58:39Z` |
| Run end | `2026-11-10T15:07:11Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 128 | 2636 | 000=3, 200=2573, 500=60 | 11.1 | 17.7 | 3236962.0 | 23.5% | 55.2% | 31.6 | 48.6% | 25.1 | 49.3% | 25.8 | 38.4s | 98.9% | 2563.0 |
| app2 | 10.0 | 2 | 57 | 200=57 | 8.3 | 12.8 | 73150.0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 21.9s | 98.9% | 57.0 |
| end-users | 65.0 | 104 | 2655 | 000=4, 200=2610, 500=41 | 8.4 | 14.9 | 3349568.0 | 76.5% | 44.8% | -31.6 | 50.3% | -26.2 | 49.6% | -26.8 | 37.2s | 98.9% | 2605.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 22.0 |

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

**Windows** (52 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 10.0 | 20.0 | app1 | True | 32318.0 | 21.1% | 39.9% | 18.8 |
| 10.0 | 20.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 10.0 | 20.0 | end-users | True | 48712.0 | 68.4% | 60.1% | -8.3 |
| 20.0 | 30.0 | app1 | True | 144728.0 | 21.1% | 47.4% | 26.3 |
| 20.0 | 30.0 | app2 | True | 2708.0 | 10.5% | 0.9% | -9.6 |
| 20.0 | 30.0 | end-users | True | 158120.0 | 68.4% | 51.7% | -16.7 |
| 30.0 | 40.0 | app1 | True | 110874.0 | 21.1% | 36.4% | 15.4 |
| 30.0 | 40.0 | app2 | True | 8134.0 | 10.5% | 2.7% | -7.9 |
| 30.0 | 40.0 | end-users | True | 185286.0 | 68.4% | 60.9% | -7.5 |
| 40.0 | 50.0 | app1 | True | 90664.0 | 21.1% | 30.2% | 9.1 |
| 40.0 | 50.0 | app2 | True | 2708.0 | 10.5% | 0.9% | -9.6 |
| 40.0 | 50.0 | end-users | True | 207114.0 | 68.4% | 68.9% | 0.5 |
| 50.0 | 60.0 | app1 | True | 151484.0 | 21.1% | 50.5% | 29.4 |
| 50.0 | 60.0 | app2 | True | 2716.0 | 10.5% | 0.9% | -9.6 |
| 50.0 | 60.0 | end-users | True | 146064.0 | 68.4% | 48.6% | -19.8 |
| 60.0 | 70.0 | app1 | True | 96024.0 | 21.1% | 31.8% | 10.8 |
| 60.0 | 70.0 | app2 | True | 2716.0 | 10.5% | 0.9% | -9.6 |
| 60.0 | 70.0 | end-users | True | 202906.0 | 68.4% | 67.3% | -1.2 |
| 70.0 | 80.0 | app1 | True | 90568.0 | 21.1% | 31.3% | 10.2 |
| 70.0 | 80.0 | app2 | True | 2716.0 | 10.5% | 0.9% | -9.6 |
| 70.0 | 80.0 | end-users | True | 196116.0 | 68.4% | 67.8% | -0.7 |
| 80.0 | 90.0 | app1 | True | 158018.0 | 21.1% | 66.8% | 45.8 |
| 80.0 | 90.0 | app2 | True | 2716.0 | 10.5% | 1.1% | -9.4 |
| 80.0 | 90.0 | end-users | True | 75772.0 | 68.4% | 32.0% | -36.4 |
| 90.0 | 100.0 | app1 | True | 148654.0 | 21.1% | 50.0% | 28.9 |
| 90.0 | 100.0 | app2 | True | 2716.0 | 10.5% | 0.9% | -9.6 |
| 90.0 | 100.0 | end-users | True | 146178.0 | 68.4% | 49.1% | -19.3 |
| 100.0 | 110.0 | app1 | True | 104106.0 | 21.1% | 46.9% | 25.9 |
| 100.0 | 110.0 | app2 | True | 2712.0 | 10.5% | 1.2% | -9.3 |
| 100.0 | 110.0 | end-users | True | 115002.0 | 68.4% | 51.8% | -16.6 |
| 110.0 | 120.0 | app1 | True | 164994.0 | 21.1% | 62.3% | 41.2 |
| 110.0 | 120.0 | app2 | True | 2706.0 | 10.5% | 1.0% | -9.5 |
| 110.0 | 120.0 | end-users | True | 97308.0 | 68.4% | 36.7% | -31.7 |
| 120.0 | 130.0 | app1 | True | 174476.0 | 21.1% | 66.5% | 45.5 |
| 120.0 | 130.0 | app2 | True | 2716.0 | 10.5% | 1.0% | -9.5 |
| 120.0 | 130.0 | end-users | True | 85160.0 | 68.4% | 32.5% | -36.0 |
| 130.0 | 140.0 | app1 | True | 170526.0 | 21.1% | 63.4% | 42.3 |
| 130.0 | 140.0 | app2 | True | 4072.0 | 10.5% | 1.5% | -9.0 |
| 130.0 | 140.0 | end-users | True | 94558.0 | 68.4% | 35.1% | -33.3 |
| 140.0 | 150.0 | app1 | True | 136578.0 | 21.1% | 44.9% | 23.8 |
| 140.0 | 150.0 | app2 | True | 4074.0 | 10.5% | 1.3% | -9.2 |
| 140.0 | 150.0 | end-users | True | 163682.0 | 68.4% | 53.8% | -14.6 |
| 150.0 | 160.0 | app1 | True | 156704.0 | 21.1% | 53.9% | 32.9 |
| 150.0 | 160.0 | app2 | True | 2674.0 | 10.5% | 0.9% | -9.6 |
| 150.0 | 160.0 | end-users | True | 131136.0 | 68.4% | 45.1% | -23.3 |
| 160.0 | 170.0 | app1 | True | 139370.0 | 21.1% | 45.6% | 24.5 |
| 160.0 | 170.0 | app2 | True | 4048.0 | 10.5% | 1.3% | -9.2 |
| 160.0 | 170.0 | end-users | True | 162274.0 | 68.4% | 53.1% | -15.3 |
| 170.0 | 180.0 | app1 | True | 112260.0 | 21.1% | 36.7% | 15.7 |
| 170.0 | 180.0 | app2 | True | 4060.0 | 10.5% | 1.3% | -9.2 |
| 170.0 | 180.0 | end-users | True | 189252.0 | 68.4% | 61.9% | -6.5 |
| 180.0 | 190.0 | app1 | True | 153998.0 | 21.1% | 58.5% | 37.4 |
| 180.0 | 190.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 180.0 | 190.0 | end-users | True | 109280.0 | 68.4% | 41.5% | -26.9 |
| 190.0 | 200.0 | app1 | True | 97412.0 | 21.1% | 36.8% | 15.7 |
| 190.0 | 200.0 | app2 | True | 2716.0 | 10.5% | 1.0% | -9.5 |
| 190.0 | 200.0 | end-users | True | 164856.0 | 68.4% | 62.2% | -6.2 |
| 200.0 | 210.0 | app1 | True | 173232.0 | 21.1% | 61.6% | 40.5 |
| 200.0 | 210.0 | app2 | True | 2706.0 | 10.5% | 1.0% | -9.6 |
| 200.0 | 210.0 | end-users | True | 105424.0 | 68.4% | 37.5% | -31.0 |
| 210.0 | 220.0 | app1 | True | 121662.0 | 21.1% | 40.3% | 19.3 |
| 210.0 | 220.0 | app2 | True | 2708.0 | 10.5% | 0.9% | -9.6 |
| 210.0 | 220.0 | end-users | True | 177306.0 | 68.4% | 58.8% | -9.6 |
| 220.0 | 230.0 | app1 | True | 190490.0 | 21.1% | 63.5% | 42.4 |
| 220.0 | 230.0 | app2 | True | 4058.0 | 10.5% | 1.4% | -9.2 |
| 220.0 | 230.0 | end-users | True | 105508.0 | 68.4% | 35.2% | -33.3 |
| 230.0 | 240.0 | app1 | True | 155524.0 | 21.1% | 50.7% | 29.6 |
| 230.0 | 240.0 | app2 | True | 4066.0 | 10.5% | 1.3% | -9.2 |
| 230.0 | 240.0 | end-users | True | 147364.0 | 68.4% | 48.0% | -20.4 |
| 240.0 | 250.0 | app1 | False | 152834.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 2704.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 135190.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 9464.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 0.0 | n/a | n/a | n/a |
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
| 320.0 | 331.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 331.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 331.0 | end-users | False | 0.0 | n/a | n/a | n/a |
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
| 501.0 | 511.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 511.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 511.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 511.0 | 512.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 511.0 | 512.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 511.0 | 512.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 60 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 2 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 63 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 170 | 25ms | 920ms | 2304ms |
| 10.0 | 20.0 | app2 | ok | 3 | 0ms | 425ms | 492ms |
| 10.0 | 20.0 | end-users | ok | 136 | 100ms | 785ms | 2092ms |
| 20.0 | 30.0 | app1 | ok | 85 | 5573ms | 9115ms | 9911ms |
| 20.0 | 30.0 | app2 | ok | 2 | 1000ms | 2200ms | 2470ms |
| 20.0 | 30.0 | end-users | ok | 168 | 2000ms | 4263ms | 4926ms |
| 30.0 | 40.0 | app1 | ok | 81 | 12000ms | 26400ms | 29640ms |
| 30.0 | 40.0 | app2 | ok | 4 | 1750ms | 2350ms | 2485ms |
| 30.0 | 40.0 | end-users | ok | 147 | 1938ms | 4279ms | 4928ms |
| 40.0 | 50.0 | app1 | ok | 86 | 9388ms | 25351ms | 29535ms |
| 40.0 | 50.0 | app2 | ok | 2 | 3750ms | 4750ms | 4975ms |
| 40.0 | 50.0 | end-users | ok | 94 | 1606ms | 3531ms | 4853ms |
| 50.0 | 60.0 | app1 | ok | 85 | 7674ms | 11111ms | 28111ms |
| 50.0 | 60.0 | app2 | ok | 4 | 4167ms | 8000ms | 9800ms |
| 50.0 | 60.0 | end-users | ok | 156 | 2669ms | 6609ms | 9661ms |
| 60.0 | 70.0 | app1 | ok | 65 | 12895ms | 26579ms | 29658ms |
| 60.0 | 70.0 | app2 | ok | 2 | 1750ms | 2350ms | 2485ms |
| 60.0 | 70.0 | end-users | ok | 135 | 1650ms | 3650ms | 4865ms |
| 70.0 | 80.0 | app1 | ok | 108 | 10364ms | 26073ms | 29607ms |
| 70.0 | 80.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 94 | 1341ms | 3192ms | 4819ms |
| 80.0 | 90.0 | app1 | ok | 68 | 6000ms | 9886ms | 27733ms |
| 80.0 | 90.0 | app2 | ok | 2 | 7500ms | 9500ms | 9950ms |
| 80.0 | 90.0 | end-users | ok | 94 | 4412ms | 8795ms | 9879ms |
| 90.0 | 100.0 | app1 | ok | 160 | 6460ms | 9292ms | 9929ms |
| 90.0 | 100.0 | app2 | ok | 4 | 1000ms | 4500ms | 4950ms |
| 90.0 | 100.0 | end-users | ok | 146 | 3841ms | 8220ms | 9822ms |
| 100.0 | 110.0 | app1 | ok | 102 | 7035ms | 9407ms | 9941ms |
| 100.0 | 110.0 | app2 | ok | 2 | 7500ms | 9500ms | 9950ms |
| 100.0 | 110.0 | end-users | ok | 59 | 3312ms | 8156ms | 9816ms |
| 110.0 | 120.0 | app1 | ok | 95 | 4755ms | 8895ms | 9890ms |
| 110.0 | 120.0 | app2 | ok | 2 | 1750ms | 2350ms | 2485ms |
| 110.0 | 120.0 | end-users | ok | 63 | 5078ms | 9016ms | 9902ms |
| 120.0 | 130.0 | app1 | ok | 107 | 4410ms | 8695ms | 9870ms |
| 120.0 | 130.0 | app2 | ok | 2 | 1000ms | 2200ms | 2470ms |
| 120.0 | 130.0 | end-users | ok | 53 | 5583ms | 9117ms | 9912ms |
| 130.0 | 140.0 | app1 | ok | 112 | 5758ms | 9152ms | 9915ms |
| 130.0 | 140.0 | app2 | ok | 2 | 3750ms | 4750ms | 4975ms |
| 130.0 | 140.0 | end-users | ok | 85 | 7123ms | 15833ms | 28583ms |
| 140.0 | 150.0 | app1 | ok | 179 | 6438ms | 9421ms | 21050ms |
| 140.0 | 150.0 | app2 | ok | 4 | 4167ms | 8000ms | 9800ms |
| 140.0 | 150.0 | end-users | ok | 151 | 3438ms | 5806ms | 9581ms |
| 150.0 | 160.0 | app1 | ok | 68 | 5278ms | 9056ms | 9906ms |
| 150.0 | 160.0 | app2 | ok | 2 | 1000ms | 2200ms | 2470ms |
| 150.0 | 160.0 | end-users | ok | 53 | 4116ms | 7792ms | 9779ms |
| 160.0 | 170.0 | app1 | ok | 88 | 6884ms | 9435ms | 12400ms |
| 160.0 | 170.0 | app2 | ok | 2 | 1750ms | 2350ms | 2485ms |
| 160.0 | 170.0 | end-users | ok | 162 | 3347ms | 7975ms | 9798ms |
| 170.0 | 180.0 | app1 | ok | 114 | 8600ms | 23667ms | 29367ms |
| 170.0 | 180.0 | app2 | ok | 2 | 5000ms | 9000ms | 9900ms |
| 170.0 | 180.0 | end-users | ok | 127 | 1922ms | 4294ms | 4929ms |
| 180.0 | 190.0 | app1 | ok | 87 | 7159ms | 9795ms | 27100ms |
| 180.0 | 190.0 | app2 | ok | 2 | 5000ms | 9000ms | 9900ms |
| 180.0 | 190.0 | end-users | ok | 43 | 7500ms | 9500ms | 9950ms |
| 190.0 | 200.0 | app1 | ok | 104 | 4821ms | 8917ms | 9892ms |
| 190.0 | 200.0 | app2 | ok | 2 | 1750ms | 2350ms | 2485ms |
| 190.0 | 200.0 | end-users | ok | 87 | 3798ms | 8597ms | 9860ms |
| 200.0 | 210.0 | app1 | ok | 109 | 6373ms | 9444ms | 22733ms |
| 200.0 | 210.0 | app2 | ok | 2 | 1750ms | 2350ms | 2485ms |
| 200.0 | 210.0 | end-users | ok | 130 | 6264ms | 9253ms | 9925ms |
| 210.0 | 220.0 | app1 | ok | 114 | 8860ms | 24818ms | 29482ms |
| 210.0 | 220.0 | app2 | ok | 2 | 3750ms | 4750ms | 4975ms |
| 210.0 | 220.0 | end-users | ok | 146 | 1872ms | 4131ms | 4913ms |
| 220.0 | 230.0 | app1 | ok | 96 | 5385ms | 9077ms | 9908ms |
| 220.0 | 230.0 | app2 | ok | 2 | 750ms | 950ms | 995ms |
| 220.0 | 230.0 | end-users | ok | 74 | 4459ms | 8724ms | 9872ms |
| 230.0 | 240.0 | app1 | ok | 123 | 7500ms | 9500ms | 9950ms |
| 230.0 | 240.0 | app2 | ok | 2 | 3750ms | 4750ms | 4975ms |
| 230.0 | 240.0 | end-users | ok | 115 | 3687ms | 6406ms | 9641ms |
| 240.0 | 250.0 | app1 | ok | 97 | 6585ms | 9317ms | 9932ms |
| 240.0 | 250.0 | app2 | ok | 2 | 3750ms | 4750ms | 4975ms |
| 240.0 | 250.0 | end-users | ok | 24 | 4643ms | 8800ms | 9880ms |
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
| 320.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 320.0 | 331.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 320.0 | 331.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 501.0 | 511.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 501.0 | 511.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 501.0 | 511.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 511.0 | 512.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 511.0 | 512.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 511.0 | 512.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 3164790 | 157061 | 3305085.0 | -0.5% | 3236962.0 | 3478912.0 | -7.0% | True |
| app2 | 70110 | 3534 | 73644.0 | 0.0% | 73150.0 | 77178.0 | -5.2% | True |
| end-users | 3210300 | 159530 | 3358200.0 | -0.3% | 3349568.0 | 3529360.0 | -5.1% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2636 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 57 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2655 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5247). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5247 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 489237 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
