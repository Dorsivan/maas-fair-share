# Fairness benchmark: app1-idle-discriminating (uni-225-app1-idle-discriminating)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 24.8 points

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-idle-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-85575669d6-cvcqq` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-10T14:48:35Z` |
| Run end | `2026-11-10T14:56:16Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| app2 | 10.0 | 128 | 927 | 200=906, 500=21 | 42.1 | 46.1 | 1068662.0 | 13.3% | 38.1% | 24.8 | 15.0% | 1.6 | 16.7% | 3.4 | 72.3s | 98.9% | 904.0 |
| end-users | 65.0 | 208 | 4613 | 000=2, 200=4570, 500=41 | 10.6 | 13.6 | 6065174.0 | 86.7% | 61.9% | -24.8 | 85.0% | -1.6 | 83.3% | -3.4 | 72.3s | 98.9% | 4571.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 3.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app2: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 20.0 | 20.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (46 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 0.0 | 10.0 | end-users | True | 0.0 | 86.7% | 0.0% | -86.7 |
| 10.0 | 20.0 | app2 | True | 82402.0 | 13.3% | 33.9% | 20.6 |
| 10.0 | 20.0 | end-users | True | 160740.0 | 86.7% | 66.1% | -20.6 |
| 20.0 | 30.0 | app2 | True | 62336.0 | 13.3% | 20.5% | 7.1 |
| 20.0 | 30.0 | end-users | True | 242112.0 | 86.7% | 79.5% | -7.1 |
| 30.0 | 40.0 | app2 | True | 39304.0 | 13.3% | 13.3% | -0.0 |
| 30.0 | 40.0 | end-users | True | 255554.0 | 86.7% | 86.7% | 0.0 |
| 40.0 | 50.0 | app2 | True | 40582.0 | 13.3% | 13.3% | -0.1 |
| 40.0 | 50.0 | end-users | True | 265240.0 | 86.7% | 86.7% | 0.1 |
| 50.0 | 60.0 | app2 | True | 39272.0 | 13.3% | 12.9% | -0.4 |
| 50.0 | 60.0 | end-users | True | 265092.0 | 86.7% | 87.1% | 0.4 |
| 60.0 | 70.0 | app2 | True | 41898.0 | 13.3% | 14.0% | 0.7 |
| 60.0 | 70.0 | end-users | True | 256786.0 | 86.7% | 86.0% | -0.7 |
| 70.0 | 80.0 | app2 | True | 37800.0 | 13.3% | 12.4% | -0.9 |
| 70.0 | 80.0 | end-users | True | 266434.0 | 86.7% | 87.6% | 0.9 |
| 80.0 | 90.0 | app2 | True | 43290.0 | 13.3% | 14.0% | 0.7 |
| 80.0 | 90.0 | end-users | True | 265070.0 | 86.7% | 86.0% | -0.7 |
| 90.0 | 100.0 | app2 | True | 39260.0 | 13.3% | 13.6% | 0.2 |
| 90.0 | 100.0 | end-users | True | 250398.0 | 86.7% | 86.4% | -0.2 |
| 100.0 | 110.0 | app2 | True | 39238.0 | 13.3% | 13.0% | -0.4 |
| 100.0 | 110.0 | end-users | True | 263640.0 | 86.7% | 87.0% | 0.4 |
| 110.0 | 120.0 | app2 | True | 43290.0 | 13.3% | 14.1% | 0.8 |
| 110.0 | 120.0 | end-users | True | 263650.0 | 86.7% | 85.9% | -0.8 |
| 120.0 | 131.0 | app2 | True | 39228.0 | 13.3% | 12.8% | -0.5 |
| 120.0 | 131.0 | end-users | True | 266364.0 | 86.7% | 87.2% | 0.5 |
| 131.0 | 141.0 | app2 | True | 40572.0 | 13.3% | 13.4% | 0.1 |
| 131.0 | 141.0 | end-users | True | 262408.0 | 86.7% | 86.6% | -0.1 |
| 141.0 | 151.0 | app2 | True | 39158.0 | 13.3% | 14.3% | 1.0 |
| 141.0 | 151.0 | end-users | True | 233984.0 | 86.7% | 85.7% | -1.0 |
| 151.0 | 161.0 | app2 | True | 39220.0 | 13.3% | 12.8% | -0.6 |
| 151.0 | 161.0 | end-users | True | 267804.0 | 86.7% | 87.2% | 0.6 |
| 161.0 | 171.0 | app2 | True | 43314.0 | 13.3% | 14.2% | 0.8 |
| 161.0 | 171.0 | end-users | True | 262212.0 | 86.7% | 85.8% | -0.8 |
| 171.0 | 181.0 | app2 | True | 37912.0 | 13.3% | 12.4% | -0.9 |
| 171.0 | 181.0 | end-users | True | 267840.0 | 86.7% | 87.6% | 0.9 |
| 181.0 | 191.0 | app2 | True | 32360.0 | 13.3% | 13.4% | 0.0 |
| 181.0 | 191.0 | end-users | True | 209678.0 | 86.7% | 86.6% | -0.0 |
| 191.0 | 201.0 | app2 | True | 40602.0 | 13.3% | 13.2% | -0.1 |
| 191.0 | 201.0 | end-users | True | 266560.0 | 86.7% | 86.8% | 0.1 |
| 201.0 | 211.0 | app2 | True | 41956.0 | 13.3% | 13.8% | 0.5 |
| 201.0 | 211.0 | end-users | True | 262222.0 | 86.7% | 86.2% | -0.5 |
| 211.0 | 221.0 | app2 | True | 40534.0 | 13.3% | 13.3% | -0.1 |
| 211.0 | 221.0 | end-users | True | 264964.0 | 86.7% | 86.7% | 0.1 |
| 221.0 | 231.0 | app2 | True | 37886.0 | 13.3% | 13.0% | -0.3 |
| 221.0 | 231.0 | end-users | True | 252810.0 | 86.7% | 87.0% | 0.3 |
| 231.0 | 241.0 | app2 | True | 32506.0 | 13.3% | 13.4% | 0.1 |
| 231.0 | 241.0 | end-users | True | 209696.0 | 86.7% | 86.6% | -0.1 |
| 241.0 | 251.0 | app2 | False | 35174.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 227230.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 59568.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 56686.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app2 | ok | 83 | 0ms | 623ms | 962ms |
| 0.0 | 10.0 | end-users | ok | 119 | 0ms | 504ms | 950ms |
| 10.0 | 20.0 | app2 | ok | 62 | 1908ms | 4031ms | 4903ms |
| 10.0 | 20.0 | end-users | ok | 179 | 1580ms | 3508ms | 4851ms |
| 20.0 | 30.0 | app2 | ok | 29 | 9028ms | 24727ms | 29473ms |
| 20.0 | 30.0 | end-users | ok | 168 | 3549ms | 4724ms | 4988ms |
| 30.0 | 40.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | end-users | ok | 211 | 6232ms | 9246ms | 9925ms |
| 40.0 | 50.0 | app2 | ok | 28 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | end-users | ok | 177 | 6373ms | 9275ms | 9927ms |
| 50.0 | 60.0 | app2 | ok | 28 | 39000ms | 55800ms | 59580ms |
| 50.0 | 60.0 | end-users | ok | 185 | 6442ms | 9288ms | 9929ms |
| 60.0 | 70.0 | app2 | ok | 40 | 45000ms | 57000ms | 59700ms |
| 60.0 | 70.0 | end-users | ok | 261 | 5094ms | 9019ms | 9902ms |
| 70.0 | 80.0 | app2 | ok | 19 | 45000ms | 57000ms | 59700ms |
| 70.0 | 80.0 | end-users | ok | 120 | 6629ms | 9326ms | 9933ms |
| 80.0 | 90.0 | app2 | ok | 33 | 45000ms | 57000ms | 59700ms |
| 80.0 | 90.0 | end-users | ok | 212 | 6864ms | 9373ms | 9937ms |
| 90.0 | 100.0 | app2 | ok | 34 | 45000ms | 57000ms | 59700ms |
| 90.0 | 100.0 | end-users | ok | 218 | 6079ms | 9216ms | 9922ms |
| 100.0 | 110.0 | app2 | ok | 25 | 45000ms | 57000ms | 59700ms |
| 100.0 | 110.0 | end-users | ok | 167 | 6813ms | 9363ms | 9936ms |
| 110.0 | 120.0 | app2 | ok | 32 | 45000ms | 57000ms | 59700ms |
| 110.0 | 120.0 | end-users | ok | 202 | 7047ms | 9409ms | 9941ms |
| 120.0 | 131.0 | app2 | ok | 32 | 45000ms | 57000ms | 59700ms |
| 120.0 | 131.0 | end-users | ok | 217 | 6790ms | 9358ms | 9936ms |
| 131.0 | 141.0 | app2 | ok | 34 | 45000ms | 57000ms | 59700ms |
| 131.0 | 141.0 | end-users | ok | 221 | 5544ms | 9109ms | 9911ms |
| 141.0 | 151.0 | app2 | ok | 17 | 45000ms | 57000ms | 59700ms |
| 141.0 | 151.0 | end-users | ok | 104 | 6000ms | 9200ms | 9920ms |
| 151.0 | 161.0 | app2 | ok | 35 | 45000ms | 57000ms | 59700ms |
| 151.0 | 161.0 | end-users | ok | 228 | 6460ms | 9292ms | 9929ms |
| 161.0 | 171.0 | app2 | ok | 26 | 45000ms | 57000ms | 59700ms |
| 161.0 | 171.0 | end-users | ok | 172 | 6387ms | 9277ms | 9928ms |
| 171.0 | 181.0 | app2 | ok | 40 | 45000ms | 57000ms | 59700ms |
| 171.0 | 181.0 | end-users | ok | 258 | 5943ms | 9189ms | 9919ms |
| 181.0 | 191.0 | app2 | ok | 15 | 45000ms | 57000ms | 59700ms |
| 181.0 | 191.0 | end-users | ok | 101 | 6921ms | 9384ms | 9938ms |
| 191.0 | 201.0 | app2 | ok | 34 | 45000ms | 57000ms | 59700ms |
| 191.0 | 201.0 | end-users | ok | 216 | 6667ms | 9333ms | 9933ms |
| 201.0 | 211.0 | app2 | ok | 29 | 45000ms | 57000ms | 59700ms |
| 201.0 | 211.0 | end-users | ok | 186 | 6125ms | 9225ms | 9922ms |
| 211.0 | 221.0 | app2 | ok | 34 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | end-users | ok | 224 | 5556ms | 9111ms | 9911ms |
| 221.0 | 231.0 | app2 | ok | 24 | 45000ms | 57000ms | 59700ms |
| 221.0 | 231.0 | end-users | ok | 153 | 5032ms | 9006ms | 9901ms |
| 231.0 | 241.0 | app2 | ok | 22 | 45000ms | 57000ms | 59700ms |
| 231.0 | 241.0 | end-users | ok | 144 | 5862ms | 9172ms | 9917ms |
| 241.0 | 251.0 | app2 | ok | 57 | 44732ms | 56946ms | 59695ms |
| 241.0 | 251.0 | end-users | ok | 128 | 6559ms | 9312ms | 9931ms |
| 251.0 | 261.0 | app2 | ok | 60 | 20980ms | 34286ms | 57429ms |
| 251.0 | 261.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -12.8%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app2 | 1114380 | 55468 | 1167260.0 | -0.2% | 1068662.0 | 1225316.0 | -12.8% | False |
| end-users | 5621100 | 279603 | 5899416.0 | -0.0% | 6065174.0 | 6180306.0 | -1.9% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app2 | 927 | 0 | 0 | 0 (never shed) | 0.00% | 13.3% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 4613 | 0 | 0 | 0 (never shed) | 0.00% | 86.7% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5478). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5478 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 440553 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
