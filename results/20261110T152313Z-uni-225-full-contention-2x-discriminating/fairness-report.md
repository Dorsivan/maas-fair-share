# Fairness benchmark: full-contention-2x-discriminating (uni-225-full-contention-2x-discriminating)

**Verdict: FAIL** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 35.1 points

- end-users deviated -10.8 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-85575669d6-8hbxv` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-10T15:24:28Z` |
| Run end | `2026-11-10T15:31:38Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 256 | 1617 | 200=1538, 500=79 | 34.6 | 58.4 | 1957666.0 | 21.1% | 33.3% | 12.3 | 26.9% | 5.8 | 26.8% | 5.7 | 66.2s | 98.9% | 1537.0 |
| app2 | 10.0 | 256 | 1136 | 200=1052, 500=84 | 41.4 | 113.0 | 1130582.0 | 10.5% | 33.3% | 22.8 | 15.5% | 5.0 | 18.8% | 8.3 | 66.3s | 98.9% | 1052.0 |
| end-users | 65.0 | 256 | 3285 | 000=2, 200=3210, 500=73 | 16.5 | 20.2 | 4199836.0 | 68.4% | 33.3% | -35.1 | 57.6% | -10.8 | 54.4% | -14.0 | 63.8s | 98.9% | 3212.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 1358.0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.0s | 98.9% | 1.0 |

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
| 0.0 | 91.0 | 91.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (43 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 10.0 | 20.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 10.0 | 20.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 10.0 | 20.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 20.0 | 30.0 | app1 | True | 95944.0 | 21.1% | 34.4% | 13.4 |
| 20.0 | 30.0 | app2 | True | 58136.0 | 10.5% | 20.9% | 10.3 |
| 20.0 | 30.0 | end-users | True | 124584.0 | 68.4% | 44.7% | -23.7 |
| 30.0 | 40.0 | app1 | True | 114762.0 | 21.1% | 37.3% | 16.2 |
| 30.0 | 40.0 | app2 | True | 120378.0 | 10.5% | 39.1% | 28.6 |
| 30.0 | 40.0 | end-users | True | 72834.0 | 68.4% | 23.6% | -44.8 |
| 40.0 | 50.0 | app1 | True | 63660.0 | 21.1% | 21.1% | 0.0 |
| 40.0 | 50.0 | app2 | True | 102844.0 | 10.5% | 34.1% | 23.5 |
| 40.0 | 50.0 | end-users | True | 135380.0 | 68.4% | 44.8% | -23.6 |
| 50.0 | 60.0 | app1 | True | 106968.0 | 21.1% | 35.0% | 13.9 |
| 50.0 | 60.0 | app2 | True | 54072.0 | 10.5% | 17.7% | 7.2 |
| 50.0 | 60.0 | end-users | True | 144848.0 | 68.4% | 47.4% | -21.1 |
| 60.0 | 71.0 | app1 | True | 106722.0 | 21.1% | 34.9% | 13.9 |
| 60.0 | 71.0 | app2 | True | 52766.0 | 10.5% | 17.3% | 6.7 |
| 60.0 | 71.0 | end-users | True | 146122.0 | 68.4% | 47.8% | -20.6 |
| 71.0 | 81.0 | app1 | True | 54118.0 | 21.1% | 22.1% | 1.1 |
| 71.0 | 81.0 | app2 | True | 25686.0 | 10.5% | 10.5% | -0.0 |
| 71.0 | 81.0 | end-users | True | 164954.0 | 68.4% | 67.4% | -1.0 |
| 81.0 | 91.0 | app1 | True | 143320.0 | 21.1% | 48.6% | 27.6 |
| 81.0 | 91.0 | app2 | True | 70294.0 | 10.5% | 23.8% | 13.3 |
| 81.0 | 91.0 | end-users | True | 81142.0 | 68.4% | 27.5% | -40.9 |
| 91.0 | 101.0 | app1 | True | 66318.0 | 21.1% | 22.2% | 1.1 |
| 91.0 | 101.0 | app2 | True | 35174.0 | 10.5% | 11.8% | 1.2 |
| 91.0 | 101.0 | end-users | True | 197568.0 | 68.4% | 66.1% | -2.4 |
| 101.0 | 111.0 | app1 | True | 58174.0 | 21.1% | 20.5% | -0.6 |
| 101.0 | 111.0 | app2 | True | 29786.0 | 10.5% | 10.5% | -0.0 |
| 101.0 | 111.0 | end-users | True | 196082.0 | 68.4% | 69.0% | 0.6 |
| 111.0 | 121.0 | app1 | True | 64868.0 | 21.1% | 21.7% | 0.7 |
| 111.0 | 121.0 | app2 | True | 32478.0 | 10.5% | 10.9% | 0.3 |
| 111.0 | 121.0 | end-users | True | 201448.0 | 68.4% | 67.4% | -1.0 |
| 121.0 | 131.0 | app1 | True | 62164.0 | 21.1% | 21.4% | 0.3 |
| 121.0 | 131.0 | app2 | True | 28432.0 | 10.5% | 9.8% | -0.7 |
| 121.0 | 131.0 | end-users | True | 200068.0 | 68.4% | 68.8% | 0.4 |
| 131.0 | 141.0 | app1 | True | 63548.0 | 21.1% | 20.7% | -0.3 |
| 131.0 | 141.0 | app2 | True | 31146.0 | 10.5% | 10.2% | -0.4 |
| 131.0 | 141.0 | end-users | True | 212138.0 | 68.4% | 69.1% | 0.7 |
| 141.0 | 151.0 | app1 | True | 63538.0 | 21.1% | 21.3% | 0.3 |
| 141.0 | 151.0 | app2 | True | 33810.0 | 10.5% | 11.4% | 0.8 |
| 141.0 | 151.0 | end-users | True | 200338.0 | 68.4% | 67.3% | -1.1 |
| 151.0 | 161.0 | app1 | True | 66246.0 | 21.1% | 21.3% | 0.2 |
| 151.0 | 161.0 | app2 | True | 32426.0 | 10.5% | 10.4% | -0.1 |
| 151.0 | 161.0 | end-users | True | 212424.0 | 68.4% | 68.3% | -0.1 |
| 161.0 | 171.0 | app1 | True | 51356.0 | 21.1% | 20.6% | -0.4 |
| 161.0 | 171.0 | app2 | True | 25694.0 | 10.5% | 10.3% | -0.2 |
| 161.0 | 171.0 | end-users | True | 171758.0 | 68.4% | 69.0% | 0.6 |
| 171.0 | 181.0 | app1 | True | 56744.0 | 21.1% | 22.1% | 1.0 |
| 171.0 | 181.0 | app2 | True | 28320.0 | 10.5% | 11.0% | 0.5 |
| 171.0 | 181.0 | end-users | True | 171870.0 | 68.4% | 66.9% | -1.5 |
| 181.0 | 191.0 | app1 | True | 62222.0 | 21.1% | 20.2% | -0.9 |
| 181.0 | 191.0 | app2 | True | 32416.0 | 10.5% | 10.5% | -0.0 |
| 181.0 | 191.0 | end-users | True | 213734.0 | 68.4% | 69.3% | 0.9 |
| 191.0 | 201.0 | app1 | True | 62268.0 | 21.1% | 21.3% | 0.2 |
| 191.0 | 201.0 | app2 | True | 31096.0 | 10.5% | 10.6% | 0.1 |
| 191.0 | 201.0 | end-users | True | 199012.0 | 68.4% | 68.1% | -0.4 |
| 201.0 | 211.0 | app1 | True | 63594.0 | 21.1% | 21.1% | 0.0 |
| 201.0 | 211.0 | app2 | True | 31118.0 | 10.5% | 10.3% | -0.2 |
| 201.0 | 211.0 | end-users | True | 207106.0 | 68.4% | 68.6% | 0.2 |
| 211.0 | 221.0 | app1 | True | 64850.0 | 21.1% | 21.0% | -0.0 |
| 211.0 | 221.0 | app2 | True | 33798.0 | 10.5% | 11.0% | 0.4 |
| 211.0 | 221.0 | end-users | True | 209516.0 | 68.4% | 68.0% | -0.4 |
| 221.0 | 231.0 | app1 | True | 63560.0 | 21.1% | 20.9% | -0.2 |
| 221.0 | 231.0 | app2 | True | 29722.0 | 10.5% | 9.8% | -0.8 |
| 221.0 | 231.0 | end-users | True | 210992.0 | 68.4% | 69.3% | 0.9 |
| 231.0 | 241.0 | app1 | True | 55390.0 | 21.1% | 21.6% | 0.5 |
| 231.0 | 241.0 | app2 | True | 27036.0 | 10.5% | 10.5% | 0.0 |
| 231.0 | 241.0 | end-users | True | 174402.0 | 68.4% | 67.9% | -0.5 |
| 241.0 | 251.0 | app1 | False | 62272.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 32446.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 208188.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 105364.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 56746.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 143328.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 179696.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 93404.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 1358.0 | n/a | n/a | n/a |
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
| 421.0 | 430.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 430.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 430.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 29 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 22 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 25 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 84 | 0ms | 340ms | 790ms |
| 10.0 | 20.0 | app2 | ok | 85 | 0ms | 175ms | 894ms |
| 10.0 | 20.0 | end-users | ok | 102 | 0ms | 180ms | 458ms |
| 20.0 | 30.0 | app1 | ok | 95 | 3125ms | 4763ms | 8812ms |
| 20.0 | 30.0 | app2 | ok | 52 | 5667ms | 9133ms | 9913ms |
| 20.0 | 30.0 | end-users | ok | 91 | 1375ms | 2386ms | 4545ms |
| 30.0 | 40.0 | app1 | ok | 68 | 1750ms | 4275ms | 6600ms |
| 30.0 | 40.0 | app2 | ok | 124 | 4000ms | 8870ms | 17600ms |
| 30.0 | 40.0 | end-users | ok | 87 | 1765ms | 3855ms | 4886ms |
| 40.0 | 50.0 | app1 | ok | 62 | 7019ms | 9404ms | 9940ms |
| 40.0 | 50.0 | app2 | ok | 40 | 6296ms | 9259ms | 9926ms |
| 40.0 | 50.0 | end-users | ok | 110 | 2417ms | 4481ms | 4948ms |
| 50.0 | 60.0 | app1 | ok | 71 | 8622ms | 23545ms | 29355ms |
| 50.0 | 60.0 | app2 | ok | 36 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | end-users | ok | 87 | 2089ms | 4320ms | 4932ms |
| 60.0 | 71.0 | app1 | ok | 68 | 17857ms | 27571ms | 29757ms |
| 60.0 | 71.0 | app2 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 60.0 | 71.0 | end-users | ok | 146 | 1625ms | 3479ms | 4848ms |
| 71.0 | 81.0 | app1 | ok | 49 | 19792ms | 27958ms | 29796ms |
| 71.0 | 81.0 | app2 | ok | 25 | 20000ms | 28000ms | 29800ms |
| 71.0 | 81.0 | end-users | ok | 59 | 1684ms | 3659ms | 4866ms |
| 81.0 | 91.0 | app1 | ok | 102 | 20000ms | 28000ms | 29800ms |
| 81.0 | 91.0 | app2 | ok | 51 | 22750ms | 46091ms | 58609ms |
| 81.0 | 91.0 | end-users | ok | 135 | 8214ms | 21000ms | 29100ms |
| 91.0 | 101.0 | app1 | ok | 54 | 20000ms | 28000ms | 29800ms |
| 91.0 | 101.0 | app2 | ok | 27 | 45000ms | 57000ms | 59700ms |
| 91.0 | 101.0 | end-users | ok | 172 | 17353ms | 27471ms | 29747ms |
| 101.0 | 111.0 | app1 | ok | 27 | 20000ms | 28000ms | 29800ms |
| 101.0 | 111.0 | app2 | ok | 14 | 45000ms | 57000ms | 59700ms |
| 101.0 | 111.0 | end-users | ok | 88 | 14828ms | 26966ms | 29697ms |
| 111.0 | 121.0 | app1 | ok | 54 | 44118ms | 56824ms | 59682ms |
| 111.0 | 121.0 | app2 | ok | 27 | 45000ms | 57000ms | 59700ms |
| 111.0 | 121.0 | end-users | ok | 177 | 17793ms | 27559ms | 29756ms |
| 121.0 | 131.0 | app1 | ok | 54 | 45000ms | 57000ms | 59700ms |
| 121.0 | 131.0 | app2 | ok | 27 | 49286ms | 60000ms | 60000ms |
| 121.0 | 131.0 | end-users | ok | 174 | 17746ms | 27549ms | 29755ms |
| 131.0 | 141.0 | app1 | ok | 32 | 45000ms | 57000ms | 59700ms |
| 131.0 | 141.0 | app2 | ok | 16 | 60000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | end-users | ok | 99 | 19794ms | 27959ms | 29796ms |
| 141.0 | 151.0 | app1 | ok | 47 | 45000ms | 57000ms | 59700ms |
| 141.0 | 151.0 | app2 | ok | 23 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | end-users | ok | 157 | 19936ms | 27987ms | 29799ms |
| 151.0 | 161.0 | app1 | ok | 53 | 45000ms | 57000ms | 59700ms |
| 151.0 | 161.0 | app2 | ok | 26 | 60000ms | 60000ms | 60000ms |
| 151.0 | 161.0 | end-users | ok | 171 | 20000ms | 28000ms | 29800ms |
| 161.0 | 171.0 | app1 | ok | 37 | 45000ms | 57000ms | 59700ms |
| 161.0 | 171.0 | app2 | ok | 19 | 60000ms | 60000ms | 60000ms |
| 161.0 | 171.0 | end-users | ok | 119 | 13239ms | 26648ms | 29665ms |
| 171.0 | 181.0 | app1 | ok | 44 | 45000ms | 57000ms | 59700ms |
| 171.0 | 181.0 | app2 | ok | 22 | 60000ms | 60000ms | 60000ms |
| 171.0 | 181.0 | end-users | ok | 143 | 16881ms | 27376ms | 29738ms |
| 181.0 | 191.0 | app1 | ok | 43 | 45000ms | 57000ms | 59700ms |
| 181.0 | 191.0 | app2 | ok | 22 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | end-users | ok | 139 | 20000ms | 28000ms | 29800ms |
| 191.0 | 201.0 | app1 | ok | 50 | 45000ms | 57000ms | 59700ms |
| 191.0 | 201.0 | app2 | ok | 25 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | end-users | ok | 164 | 18451ms | 27690ms | 29769ms |
| 201.0 | 211.0 | app1 | ok | 40 | 45000ms | 57000ms | 59700ms |
| 201.0 | 211.0 | app2 | ok | 20 | 60000ms | 60000ms | 60000ms |
| 201.0 | 211.0 | end-users | ok | 129 | 15824ms | 27165ms | 29716ms |
| 211.0 | 221.0 | app1 | ok | 54 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | app2 | ok | 27 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | end-users | ok | 176 | 16963ms | 27393ms | 29739ms |
| 221.0 | 231.0 | app1 | ok | 57 | 45000ms | 57000ms | 59700ms |
| 221.0 | 231.0 | app2 | ok | 29 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | end-users | ok | 186 | 16619ms | 27324ms | 29732ms |
| 231.0 | 241.0 | app1 | ok | 26 | 45000ms | 57000ms | 59700ms |
| 231.0 | 241.0 | app2 | ok | 13 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | end-users | ok | 85 | 18514ms | 27703ms | 29770ms |
| 241.0 | 251.0 | app1 | ok | 54 | 45000ms | 57000ms | 59700ms |
| 241.0 | 251.0 | app2 | ok | 26 | 60000ms | 60000ms | 60000ms |
| 241.0 | 251.0 | end-users | ok | 173 | 19702ms | 27940ms | 29794ms |
| 251.0 | 261.0 | app1 | ok | 120 | 45000ms | 57000ms | 59700ms |
| 251.0 | 261.0 | app2 | ok | 61 | 60000ms | 60000ms | 60000ms |
| 251.0 | 261.0 | end-users | ok | 18 | 20000ms | 28000ms | 29800ms |
| 261.0 | 271.0 | app1 | ok | 63 | 27027ms | 52731ms | 59273ms |
| 261.0 | 271.0 | app2 | ok | 156 | 60000ms | 60000ms | 60000ms |
| 261.0 | 271.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | ok | 4 | 45000ms | 57000ms | 59700ms |
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
| 421.0 | 430.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 430.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 430.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -20.5%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1891740 | 93864 | 1984310.0 | -0.1% | 1957666.0 | 2079468.0 | -5.9% | True |
| app2 | 1293960 | 64273 | 1358233.0 | 0.0% | 1130582.0 | 1422506.0 | -20.5% | False |
| end-users | 3948300 | 196752 | 4145052.0 | 0.0% | 4199836.0 | 4341804.0 | -3.3% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1617 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1136 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3285 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5802). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5802 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 412291 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
