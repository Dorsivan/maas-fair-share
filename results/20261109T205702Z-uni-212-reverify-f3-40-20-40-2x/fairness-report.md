# Fairness benchmark: full-contention-2x (uni-212-reverify-f3-40-20-40-2x)

**Verdict: FAIL** (threshold: 10 points)

- end-users deviated +27.0 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-85b4699458-6vrgn` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T20:58:16Z` |
| Run end | `2026-11-09T21:06:29Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 40.0 | 64 | 943 | 000=2, 200=915, 500=26 | 16.6 | 19.1 | 1118196.0 | 40.0% | 16.7% | -23.3 | 16.4% | -23.6 | 10.2s | 98.9% | 913.0 |
| app2 | 20.0 | 64 | 945 | 200=914, 500=31 | 17.0 | 19.8 | 1093884.0 | 20.0% | 16.3% | -3.7 | 16.4% | -3.6 | 10.3s | 98.9% | 907.0 |
| end-users | 40.0 | 256 | 3868 | 000=3, 200=3759, 500=106 | 16.5 | 19.1 | 4483048.0 | 40.0% | 67.0% | 27.0 | 67.2% | 27.2 | 10.3s | 98.9% | 3745.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 28.0 |

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

**Windows** (50 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 0.0 | 10.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 0.0 | 10.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 10.0 | 20.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 10.0 | 20.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 10.0 | 20.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 20.0 | 30.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 20.0 | 30.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 20.0 | 30.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 30.0 | 40.0 | app1 | True | 36506.0 | 40.0% | 17.9% | -22.1 |
| 30.0 | 40.0 | app2 | True | 25706.0 | 20.0% | 12.6% | -7.4 |
| 30.0 | 40.0 | end-users | True | 141996.0 | 40.0% | 69.5% | 29.5 |
| 40.0 | 50.0 | app1 | True | 54102.0 | 40.0% | 17.6% | -22.4 |
| 40.0 | 50.0 | app2 | True | 58068.0 | 20.0% | 18.9% | -1.1 |
| 40.0 | 50.0 | end-users | True | 195798.0 | 40.0% | 63.6% | 23.6 |
| 50.0 | 60.0 | app1 | True | 58190.0 | 40.0% | 19.0% | -21.0 |
| 50.0 | 60.0 | app2 | True | 40622.0 | 20.0% | 13.2% | -6.8 |
| 50.0 | 60.0 | end-users | True | 207976.0 | 40.0% | 67.8% | 27.8 |
| 60.0 | 70.0 | app1 | True | 33780.0 | 40.0% | 11.3% | -28.7 |
| 60.0 | 70.0 | app2 | True | 58208.0 | 20.0% | 19.4% | -0.6 |
| 60.0 | 70.0 | end-users | True | 208240.0 | 40.0% | 69.4% | 29.4 |
| 70.0 | 80.0 | app1 | True | 67520.0 | 40.0% | 22.5% | -17.5 |
| 70.0 | 80.0 | app2 | True | 66210.0 | 20.0% | 22.1% | 2.1 |
| 70.0 | 80.0 | end-users | True | 166386.0 | 40.0% | 55.4% | 15.4 |
| 80.0 | 90.0 | app1 | True | 51330.0 | 40.0% | 16.7% | -23.3 |
| 80.0 | 90.0 | app2 | True | 18948.0 | 20.0% | 6.2% | -13.8 |
| 80.0 | 90.0 | end-users | True | 236670.0 | 40.0% | 77.1% | 37.1 |
| 90.0 | 100.0 | app1 | True | 44518.0 | 40.0% | 14.9% | -25.1 |
| 90.0 | 100.0 | app2 | True | 67576.0 | 20.0% | 22.6% | 2.6 |
| 90.0 | 100.0 | end-users | True | 186496.0 | 40.0% | 62.5% | 22.5 |
| 100.0 | 110.0 | app1 | True | 47328.0 | 40.0% | 15.5% | -24.5 |
| 100.0 | 110.0 | app2 | True | 32480.0 | 20.0% | 10.6% | -9.4 |
| 100.0 | 110.0 | end-users | True | 225766.0 | 40.0% | 73.9% | 33.9 |
| 110.0 | 120.0 | app1 | True | 45990.0 | 40.0% | 15.4% | -24.6 |
| 110.0 | 120.0 | app2 | True | 55494.0 | 20.0% | 18.6% | -1.4 |
| 110.0 | 120.0 | end-users | True | 196220.0 | 40.0% | 65.9% | 25.9 |
| 120.0 | 130.0 | app1 | True | 66330.0 | 40.0% | 22.1% | -17.9 |
| 120.0 | 130.0 | app2 | True | 45944.0 | 20.0% | 15.3% | -4.7 |
| 120.0 | 130.0 | end-users | True | 188026.0 | 40.0% | 62.6% | 22.6 |
| 130.0 | 140.0 | app1 | True | 36544.0 | 40.0% | 12.2% | -27.8 |
| 130.0 | 140.0 | app2 | True | 48768.0 | 20.0% | 16.3% | -3.7 |
| 130.0 | 140.0 | end-users | True | 213528.0 | 40.0% | 71.5% | 31.5 |
| 140.0 | 150.0 | app1 | True | 56852.0 | 40.0% | 18.8% | -21.2 |
| 140.0 | 150.0 | app2 | True | 71574.0 | 20.0% | 23.6% | 3.6 |
| 140.0 | 150.0 | end-users | True | 174472.0 | 40.0% | 57.6% | 17.6 |
| 150.0 | 160.0 | app1 | True | 52722.0 | 40.0% | 17.7% | -22.3 |
| 150.0 | 160.0 | app2 | True | 26994.0 | 20.0% | 9.1% | -10.9 |
| 150.0 | 160.0 | end-users | True | 217794.0 | 40.0% | 73.2% | 33.2 |
| 160.0 | 170.0 | app1 | True | 51412.0 | 40.0% | 17.0% | -23.0 |
| 160.0 | 170.0 | app2 | True | 58188.0 | 20.0% | 19.3% | -0.7 |
| 160.0 | 170.0 | end-users | True | 192102.0 | 40.0% | 63.7% | 23.7 |
| 170.0 | 181.0 | app1 | True | 50004.0 | 40.0% | 16.4% | -23.6 |
| 170.0 | 181.0 | app2 | True | 52634.0 | 20.0% | 17.3% | -2.7 |
| 170.0 | 181.0 | end-users | True | 201390.0 | 40.0% | 66.2% | 26.2 |
| 181.0 | 191.0 | app1 | True | 36480.0 | 40.0% | 12.1% | -27.9 |
| 181.0 | 191.0 | app2 | True | 40588.0 | 20.0% | 13.5% | -6.5 |
| 181.0 | 191.0 | end-users | True | 224550.0 | 40.0% | 74.4% | 34.4 |
| 191.0 | 201.0 | app1 | True | 70268.0 | 40.0% | 23.2% | -16.8 |
| 191.0 | 201.0 | app2 | True | 60850.0 | 20.0% | 20.1% | 0.1 |
| 191.0 | 201.0 | end-users | True | 171784.0 | 40.0% | 56.7% | 16.7 |
| 201.0 | 211.0 | app1 | True | 50018.0 | 40.0% | 16.4% | -23.6 |
| 201.0 | 211.0 | app2 | True | 36508.0 | 20.0% | 12.0% | -8.0 |
| 201.0 | 211.0 | end-users | True | 217654.0 | 40.0% | 71.6% | 31.6 |
| 211.0 | 221.0 | app1 | True | 41920.0 | 40.0% | 13.9% | -26.1 |
| 211.0 | 221.0 | app2 | True | 51336.0 | 20.0% | 17.0% | -3.0 |
| 211.0 | 221.0 | end-users | True | 209402.0 | 40.0% | 69.2% | 29.2 |
| 221.0 | 231.0 | app1 | True | 63626.0 | 40.0% | 21.4% | -18.6 |
| 221.0 | 231.0 | app2 | True | 41838.0 | 20.0% | 14.1% | -5.9 |
| 221.0 | 231.0 | end-users | True | 191970.0 | 40.0% | 64.5% | 24.5 |
| 231.0 | 241.0 | app1 | True | 20226.0 | 40.0% | 6.6% | -33.4 |
| 231.0 | 241.0 | app2 | True | 47342.0 | 20.0% | 15.4% | -4.6 |
| 231.0 | 241.0 | end-users | True | 240480.0 | 40.0% | 78.1% | 38.1 |
| 241.0 | 251.0 | app1 | False | 66318.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 55542.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 183950.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 16212.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 32466.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 90398.0 | n/a | n/a | n/a |
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
| 491.0 | 493.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 493.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 493.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 18 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 16 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 91 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 62 | 0ms | 0ms | 204ms |
| 10.0 | 20.0 | app2 | ok | 64 | 0ms | 0ms | 154ms |
| 10.0 | 20.0 | end-users | ok | 245 | 0ms | 0ms | 76ms |
| 20.0 | 30.0 | app1 | ok | 45 | 817ms | 2103ms | 2460ms |
| 20.0 | 30.0 | app2 | ok | 38 | 1000ms | 2200ms | 2470ms |
| 20.0 | 30.0 | end-users | ok | 160 | 961ms | 2346ms | 4556ms |
| 30.0 | 40.0 | app1 | ok | 41 | 804ms | 2258ms | 4487ms |
| 30.0 | 40.0 | app2 | ok | 42 | 1911ms | 3950ms | 4895ms |
| 30.0 | 40.0 | end-users | ok | 177 | 1712ms | 3804ms | 4880ms |
| 40.0 | 50.0 | app1 | ok | 32 | 1125ms | 3400ms | 4840ms |
| 40.0 | 50.0 | app2 | ok | 39 | 1781ms | 3781ms | 4878ms |
| 40.0 | 50.0 | end-users | ok | 130 | 1403ms | 2969ms | 4797ms |
| 50.0 | 60.0 | app1 | ok | 46 | 1341ms | 3083ms | 4808ms |
| 50.0 | 60.0 | app2 | ok | 33 | 1550ms | 3821ms | 4882ms |
| 50.0 | 60.0 | end-users | ok | 182 | 1628ms | 3662ms | 4866ms |
| 60.0 | 70.0 | app1 | ok | 30 | 1711ms | 3500ms | 4850ms |
| 60.0 | 70.0 | app2 | ok | 41 | 854ms | 2950ms | 4795ms |
| 60.0 | 70.0 | end-users | ok | 134 | 1634ms | 3712ms | 4871ms |
| 70.0 | 80.0 | app1 | ok | 44 | 864ms | 2460ms | 4725ms |
| 70.0 | 80.0 | app2 | ok | 26 | 1250ms | 2833ms | 4783ms |
| 70.0 | 80.0 | end-users | ok | 124 | 1841ms | 4061ms | 4906ms |
| 80.0 | 90.0 | app1 | ok | 34 | 1955ms | 4346ms | 4935ms |
| 80.0 | 90.0 | app2 | ok | 42 | 1316ms | 3250ms | 4825ms |
| 80.0 | 90.0 | end-users | ok | 188 | 1671ms | 3694ms | 4869ms |
| 90.0 | 100.0 | app1 | ok | 42 | 1794ms | 4192ms | 4919ms |
| 90.0 | 100.0 | app2 | ok | 52 | 1250ms | 2833ms | 4783ms |
| 90.0 | 100.0 | end-users | ok | 107 | 1623ms | 3592ms | 4859ms |
| 100.0 | 110.0 | app1 | ok | 39 | 1458ms | 3607ms | 4861ms |
| 100.0 | 110.0 | app2 | ok | 22 | 1955ms | 4214ms | 4921ms |
| 100.0 | 110.0 | end-users | ok | 183 | 1423ms | 2592ms | 4759ms |
| 110.0 | 120.0 | app1 | ok | 27 | 1562ms | 3875ms | 4888ms |
| 110.0 | 120.0 | app2 | ok | 44 | 1635ms | 3429ms | 4843ms |
| 110.0 | 120.0 | end-users | ok | 128 | 1415ms | 3118ms | 4812ms |
| 120.0 | 130.0 | app1 | ok | 44 | 1500ms | 3167ms | 4817ms |
| 120.0 | 130.0 | app2 | ok | 31 | 2050ms | 4295ms | 4930ms |
| 120.0 | 130.0 | end-users | ok | 173 | 1422ms | 3198ms | 4820ms |
| 130.0 | 140.0 | app1 | ok | 40 | 1500ms | 3333ms | 4833ms |
| 130.0 | 140.0 | app2 | ok | 43 | 1607ms | 3806ms | 4881ms |
| 130.0 | 140.0 | end-users | ok | 174 | 1387ms | 2463ms | 4710ms |
| 140.0 | 150.0 | app1 | ok | 40 | 1094ms | 3000ms | 4800ms |
| 140.0 | 150.0 | app2 | ok | 45 | 1536ms | 3750ms | 4875ms |
| 140.0 | 150.0 | end-users | ok | 113 | 1464ms | 2827ms | 4783ms |
| 150.0 | 160.0 | app1 | ok | 42 | 958ms | 3500ms | 4850ms |
| 150.0 | 160.0 | app2 | ok | 29 | 1812ms | 4194ms | 4919ms |
| 150.0 | 160.0 | end-users | ok | 179 | 1498ms | 2966ms | 4797ms |
| 160.0 | 170.0 | app1 | ok | 30 | 1474ms | 2421ms | 4625ms |
| 160.0 | 170.0 | app2 | ok | 42 | 1727ms | 2491ms | 4737ms |
| 160.0 | 170.0 | end-users | ok | 126 | 1223ms | 3630ms | 4863ms |
| 170.0 | 181.0 | app1 | ok | 39 | 1625ms | 3917ms | 4892ms |
| 170.0 | 181.0 | app2 | ok | 36 | 1750ms | 2470ms | 4700ms |
| 170.0 | 181.0 | end-users | ok | 174 | 1505ms | 3327ms | 4833ms |
| 181.0 | 191.0 | app1 | ok | 32 | 1618ms | 3667ms | 4867ms |
| 181.0 | 191.0 | app2 | ok | 31 | 1906ms | 3708ms | 4871ms |
| 181.0 | 191.0 | end-users | ok | 134 | 1310ms | 3405ms | 4840ms |
| 191.0 | 201.0 | app1 | ok | 45 | 1475ms | 2375ms | 4437ms |
| 191.0 | 201.0 | app2 | ok | 43 | 1519ms | 4173ms | 4917ms |
| 191.0 | 201.0 | end-users | ok | 143 | 1528ms | 3118ms | 4812ms |
| 201.0 | 211.0 | app1 | ok | 37 | 1307ms | 2316ms | 4075ms |
| 201.0 | 211.0 | app2 | ok | 36 | 1477ms | 2459ms | 4700ms |
| 201.0 | 211.0 | end-users | ok | 181 | 1218ms | 2385ms | 4589ms |
| 211.0 | 221.0 | app1 | ok | 41 | 1607ms | 3719ms | 4872ms |
| 211.0 | 221.0 | app2 | ok | 41 | 2219ms | 4461ms | 4946ms |
| 211.0 | 221.0 | end-users | ok | 143 | 1440ms | 2426ms | 4642ms |
| 221.0 | 231.0 | app1 | ok | 22 | 1462ms | 2477ms | 4725ms |
| 221.0 | 231.0 | app2 | ok | 21 | 1750ms | 4344ms | 4934ms |
| 221.0 | 231.0 | end-users | ok | 144 | 1456ms | 2882ms | 4788ms |
| 231.0 | 241.0 | app1 | ok | 40 | 1672ms | 2500ms | 4750ms |
| 231.0 | 241.0 | app2 | ok | 43 | 1750ms | 3806ms | 4881ms |
| 231.0 | 241.0 | end-users | ok | 174 | 1214ms | 2457ms | 4710ms |
| 241.0 | 251.0 | app1 | ok | 1 | 3750ms | 4750ms | 4975ms |
| 241.0 | 251.0 | app2 | ok | 7 | 1875ms | 3250ms | 4825ms |
| 241.0 | 251.0 | end-users | ok | 38 | 1964ms | 3944ms | 4894ms |
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
| 491.0 | 493.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 493.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 493.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -11.5%
- end-users exceeded the 10% ledger tolerance: cost -11.8%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1125450 | 55804 | 1176084.0 | -0.4% | 1118196.0 | 1237058.0 | -9.6% | True |
| app2 | 1124220 | 55774 | 1170944.0 | -0.8% | 1093884.0 | 1235768.0 | -11.5% | False |
| end-users | 4623570 | 229179 | 4830773.0 | -0.5% | 4483048.0 | 5081928.0 | -11.8% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 943 | 0 | 0 | 0 (never shed) | 0.00% | 40.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 945 | 0 | 0 | 0 (never shed) | 0.00% | 20.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3868 | 0 | 0 | 0 (never shed) | 0.00% | 40.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5593). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5593 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 472326 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
