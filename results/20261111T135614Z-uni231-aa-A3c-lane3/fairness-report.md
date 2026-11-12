# Fairness benchmark: full-contention-2x-discriminating (uni231-aa-A3c-lane3)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 35.1 points

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:c8a088203f6dc6c48c158d21b6295172a78f18646b06c334e5310a0caedb259f` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-6668d94f5f-tgf48` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-11T13:57:25Z` |
| Run end | `2026-11-11T14:02:10Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 256 | 1356 | 200=1356 | 51.8 | 56.7 | 1745230.0 | 21.1% | 33.3% | 12.3 | 23.2% | 2.1 | 23.1% | 2.1 | 91.7s | 98.9% | 1356.0 |
| app2 | 10.0 | 256 | 809 | 200=809 | 90.1 | 110.8 | 892066.0 | 10.5% | 33.3% | 22.8 | 11.8% | 1.3 | 13.8% | 3.3 | 91.7s | 98.9% | 809.0 |
| end-users | 65.0 | 256 | 3702 | 200=3702 | 15.9 | 18.9 | 4893202.0 | 68.4% | 33.3% | -35.1 | 65.0% | -3.4 | 63.1% | -5.3 | 86.1s | 98.9% | 3702.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

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
| 0.0 | 70.0 | 70.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (29 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 10.0 | 20.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 10.0 | 20.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 10.0 | 20.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 20.0 | 30.0 | app1 | True | 44690.0 | 21.1% | 16.0% | -5.1 |
| 20.0 | 30.0 | app2 | True | 25650.0 | 10.5% | 9.2% | -1.4 |
| 20.0 | 30.0 | end-users | True | 209564.0 | 68.4% | 74.9% | 6.4 |
| 30.0 | 40.0 | app1 | True | 132538.0 | 21.1% | 43.0% | 21.9 |
| 30.0 | 40.0 | app2 | True | 32422.0 | 10.5% | 10.5% | -0.0 |
| 30.0 | 40.0 | end-users | True | 143412.0 | 68.4% | 46.5% | -21.9 |
| 40.0 | 50.0 | app1 | True | 45984.0 | 21.1% | 15.1% | -6.0 |
| 40.0 | 50.0 | app2 | True | 23008.0 | 10.5% | 7.5% | -3.0 |
| 40.0 | 50.0 | end-users | True | 236532.0 | 68.4% | 77.4% | 9.0 |
| 50.0 | 60.0 | app1 | True | 86652.0 | 21.1% | 28.5% | 7.4 |
| 50.0 | 60.0 | app2 | True | 45894.0 | 10.5% | 15.1% | 4.6 |
| 50.0 | 60.0 | end-users | True | 171808.0 | 68.4% | 56.5% | -12.0 |
| 60.0 | 70.0 | app1 | True | 13526.0 | 21.1% | 4.4% | -16.7 |
| 60.0 | 70.0 | app2 | True | 5412.0 | 10.5% | 1.7% | -8.8 |
| 60.0 | 70.0 | end-users | True | 290540.0 | 68.4% | 93.9% | 25.5 |
| 70.0 | 80.0 | app1 | True | 63468.0 | 21.1% | 20.8% | -0.3 |
| 70.0 | 80.0 | app2 | True | 31040.0 | 10.5% | 10.2% | -0.4 |
| 70.0 | 80.0 | end-users | True | 210796.0 | 68.4% | 69.0% | 0.6 |
| 80.0 | 90.0 | app1 | True | 60786.0 | 21.1% | 19.8% | -1.2 |
| 80.0 | 90.0 | app2 | True | 35122.0 | 10.5% | 11.4% | 0.9 |
| 80.0 | 90.0 | end-users | True | 210848.0 | 68.4% | 68.7% | 0.3 |
| 90.0 | 100.0 | app1 | True | 66392.0 | 21.1% | 22.2% | 1.2 |
| 90.0 | 100.0 | app2 | True | 31062.0 | 10.5% | 10.4% | -0.1 |
| 90.0 | 100.0 | end-users | True | 201484.0 | 68.4% | 67.4% | -1.0 |
| 100.0 | 110.0 | app1 | True | 64836.0 | 21.1% | 21.0% | -0.1 |
| 100.0 | 110.0 | app2 | True | 31060.0 | 10.5% | 10.0% | -0.5 |
| 100.0 | 110.0 | end-users | True | 213582.0 | 68.4% | 69.0% | 0.6 |
| 110.0 | 120.0 | app1 | True | 64932.0 | 21.1% | 21.3% | 0.3 |
| 110.0 | 120.0 | app2 | True | 31096.0 | 10.5% | 10.2% | -0.3 |
| 110.0 | 120.0 | end-users | True | 208150.0 | 68.4% | 68.4% | 0.0 |
| 120.0 | 131.0 | app1 | True | 64734.0 | 21.1% | 21.0% | -0.0 |
| 120.0 | 131.0 | app2 | True | 33756.0 | 10.5% | 11.0% | 0.4 |
| 120.0 | 131.0 | end-users | True | 209492.0 | 68.4% | 68.0% | -0.4 |
| 131.0 | 141.0 | app1 | True | 62204.0 | 21.1% | 20.6% | -0.4 |
| 131.0 | 141.0 | app2 | True | 31098.0 | 10.5% | 10.3% | -0.2 |
| 131.0 | 141.0 | end-users | True | 208138.0 | 68.4% | 69.0% | 0.6 |
| 141.0 | 151.0 | app1 | True | 64834.0 | 21.1% | 21.1% | 0.1 |
| 141.0 | 151.0 | app2 | True | 32498.0 | 10.5% | 10.6% | 0.1 |
| 141.0 | 151.0 | end-users | True | 209526.0 | 68.4% | 68.3% | -0.1 |
| 151.0 | 161.0 | app1 | True | 59508.0 | 21.1% | 21.0% | -0.1 |
| 151.0 | 161.0 | app2 | True | 28298.0 | 10.5% | 10.0% | -0.6 |
| 151.0 | 161.0 | end-users | True | 196174.0 | 68.4% | 69.1% | 0.7 |
| 161.0 | 171.0 | app1 | True | 64992.0 | 21.1% | 21.2% | 0.1 |
| 161.0 | 171.0 | app2 | True | 33710.0 | 10.5% | 11.0% | 0.5 |
| 161.0 | 171.0 | end-users | True | 208274.0 | 68.4% | 67.8% | -0.6 |
| 171.0 | 181.0 | app1 | True | 64888.0 | 21.1% | 21.4% | 0.4 |
| 171.0 | 181.0 | app2 | True | 31050.0 | 10.5% | 10.2% | -0.3 |
| 171.0 | 181.0 | end-users | True | 207142.0 | 68.4% | 68.3% | -0.1 |
| 181.0 | 191.0 | app1 | True | 64850.0 | 21.1% | 21.2% | 0.2 |
| 181.0 | 191.0 | app2 | True | 33758.0 | 10.5% | 11.0% | 0.5 |
| 181.0 | 191.0 | end-users | True | 206996.0 | 68.4% | 67.7% | -0.7 |
| 191.0 | 201.0 | app1 | True | 62186.0 | 21.1% | 20.4% | -0.6 |
| 191.0 | 201.0 | app2 | True | 31118.0 | 10.5% | 10.2% | -0.3 |
| 191.0 | 201.0 | end-users | True | 211022.0 | 68.4% | 69.3% | 0.9 |
| 201.0 | 211.0 | app1 | True | 63446.0 | 21.1% | 20.8% | -0.2 |
| 201.0 | 211.0 | app2 | True | 31186.0 | 10.5% | 10.2% | -0.3 |
| 201.0 | 211.0 | end-users | True | 209726.0 | 68.4% | 68.9% | 0.5 |
| 211.0 | 221.0 | app1 | True | 64886.0 | 21.1% | 21.4% | 0.4 |
| 211.0 | 221.0 | app2 | True | 32474.0 | 10.5% | 10.7% | 0.2 |
| 211.0 | 221.0 | end-users | True | 205362.0 | 68.4% | 67.8% | -0.6 |
| 221.0 | 231.0 | app1 | True | 60874.0 | 21.1% | 21.4% | 0.4 |
| 221.0 | 231.0 | app2 | True | 31086.0 | 10.5% | 11.0% | 0.4 |
| 221.0 | 231.0 | end-users | True | 191862.0 | 68.4% | 67.6% | -0.8 |
| 231.0 | 241.0 | app1 | True | 52774.0 | 21.1% | 20.9% | -0.2 |
| 231.0 | 241.0 | app2 | True | 27064.0 | 10.5% | 10.7% | 0.2 |
| 231.0 | 241.0 | end-users | True | 173102.0 | 68.4% | 68.4% | 0.0 |
| 241.0 | 251.0 | app1 | False | 64970.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 32540.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 213566.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 105398.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 51328.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 146104.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 180882.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 127116.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 12220.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 285.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 285.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 285.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 4 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 2 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 5 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 94 | 0ms | 1758ms | 2426ms |
| 10.0 | 20.0 | app2 | ok | 75 | 0ms | 128ms | 312ms |
| 10.0 | 20.0 | end-users | ok | 140 | 0ms | 1776ms | 2428ms |
| 20.0 | 30.0 | app1 | ok | 55 | 7500ms | 9500ms | 9950ms |
| 20.0 | 30.0 | app2 | ok | 7 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | end-users | ok | 118 | 1750ms | 4078ms | 4908ms |
| 30.0 | 40.0 | app1 | ok | 65 | 12895ms | 26579ms | 29658ms |
| 30.0 | 40.0 | app2 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | end-users | ok | 159 | 1361ms | 2792ms | 4779ms |
| 40.0 | 50.0 | app1 | ok | 47 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app2 | ok | 22 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | end-users | ok | 126 | 1500ms | 2900ms | 4790ms |
| 50.0 | 60.0 | app1 | ok | 29 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app2 | ok | 16 | 23333ms | 48000ms | 58800ms |
| 50.0 | 60.0 | end-users | ok | 181 | 2017ms | 4220ms | 4922ms |
| 60.0 | 70.0 | app1 | ok | 30 | 45000ms | 57000ms | 59700ms |
| 60.0 | 70.0 | app2 | ok | 14 | 45000ms | 57000ms | 59700ms |
| 60.0 | 70.0 | end-users | ok | 204 | 2419ms | 4474ms | 4947ms |
| 70.0 | 80.0 | app1 | ok | 47 | 45000ms | 57000ms | 59700ms |
| 70.0 | 80.0 | app2 | ok | 23 | 45000ms | 57000ms | 59700ms |
| 70.0 | 80.0 | end-users | ok | 151 | 4384ms | 8720ms | 9872ms |
| 80.0 | 90.0 | app1 | ok | 54 | 45000ms | 57000ms | 59700ms |
| 80.0 | 90.0 | app2 | ok | 28 | 60000ms | 60000ms | 60000ms |
| 80.0 | 90.0 | end-users | ok | 178 | 7602ms | 9684ms | 24914ms |
| 90.0 | 100.0 | app1 | ok | 38 | 45000ms | 57000ms | 59700ms |
| 90.0 | 100.0 | app2 | ok | 19 | 60000ms | 60000ms | 60000ms |
| 90.0 | 100.0 | end-users | ok | 120 | 15185ms | 27037ms | 29704ms |
| 100.0 | 110.0 | app1 | ok | 53 | 45000ms | 57000ms | 59700ms |
| 100.0 | 110.0 | app2 | ok | 26 | 60000ms | 60000ms | 60000ms |
| 100.0 | 110.0 | end-users | ok | 175 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app1 | ok | 49 | 45000ms | 57000ms | 59700ms |
| 110.0 | 120.0 | app2 | ok | 24 | 60000ms | 60000ms | 60000ms |
| 110.0 | 120.0 | end-users | ok | 157 | 19936ms | 27987ms | 29799ms |
| 120.0 | 131.0 | app1 | ok | 41 | 45000ms | 57000ms | 59700ms |
| 120.0 | 131.0 | app2 | ok | 21 | 60000ms | 60000ms | 60000ms |
| 120.0 | 131.0 | end-users | ok | 133 | 19924ms | 27985ms | 29798ms |
| 131.0 | 141.0 | app1 | ok | 49 | 45000ms | 57000ms | 59700ms |
| 131.0 | 141.0 | app2 | ok | 24 | 60000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | end-users | ok | 156 | 19935ms | 27987ms | 29799ms |
| 141.0 | 151.0 | app1 | ok | 51 | 45000ms | 57000ms | 59700ms |
| 141.0 | 151.0 | app2 | ok | 26 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | end-users | ok | 168 | 19940ms | 27988ms | 29799ms |
| 151.0 | 161.0 | app1 | ok | 41 | 45000ms | 57000ms | 59700ms |
| 151.0 | 161.0 | app2 | ok | 21 | 60000ms | 60000ms | 60000ms |
| 151.0 | 161.0 | end-users | ok | 133 | 18018ms | 27604ms | 29760ms |
| 161.0 | 171.0 | app1 | ok | 50 | 45000ms | 57000ms | 59700ms |
| 161.0 | 171.0 | app2 | ok | 24 | 60000ms | 60000ms | 60000ms |
| 161.0 | 171.0 | end-users | ok | 162 | 20000ms | 28000ms | 29800ms |
| 171.0 | 181.0 | app1 | ok | 48 | 45000ms | 57000ms | 59700ms |
| 171.0 | 181.0 | app2 | ok | 25 | 60000ms | 60000ms | 60000ms |
| 171.0 | 181.0 | end-users | ok | 157 | 20000ms | 28000ms | 29800ms |
| 181.0 | 191.0 | app1 | ok | 48 | 45000ms | 57000ms | 59700ms |
| 181.0 | 191.0 | app2 | ok | 24 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | end-users | ok | 154 | 20000ms | 28000ms | 29800ms |
| 191.0 | 201.0 | app1 | ok | 47 | 45000ms | 57000ms | 59700ms |
| 191.0 | 201.0 | app2 | ok | 23 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | end-users | ok | 153 | 20000ms | 28000ms | 29800ms |
| 201.0 | 211.0 | app1 | ok | 46 | 45000ms | 57000ms | 59700ms |
| 201.0 | 211.0 | app2 | ok | 23 | 60000ms | 60000ms | 60000ms |
| 201.0 | 211.0 | end-users | ok | 147 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app1 | ok | 48 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | app2 | ok | 24 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | end-users | ok | 160 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app1 | ok | 72 | 45000ms | 57000ms | 59700ms |
| 221.0 | 231.0 | app2 | ok | 37 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | end-users | ok | 234 | 14400ms | 26880ms | 29688ms |
| 231.0 | 241.0 | app1 | ok | 25 | 45000ms | 57000ms | 59700ms |
| 231.0 | 241.0 | app2 | ok | 12 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | end-users | ok | 83 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | app1 | ok | 37 | 45000ms | 57000ms | 59700ms |
| 241.0 | 251.0 | app2 | ok | 18 | 60000ms | 60000ms | 60000ms |
| 241.0 | 251.0 | end-users | ok | 113 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app1 | ok | 129 | 45000ms | 57000ms | 59700ms |
| 251.0 | 261.0 | app2 | ok | 65 | 60000ms | 60000ms | 60000ms |
| 251.0 | 261.0 | end-users | ok | 35 | 20000ms | 28000ms | 29800ms |
| 261.0 | 271.0 | app1 | ok | 59 | 26389ms | 52304ms | 59230ms |
| 261.0 | 271.0 | app2 | ok | 156 | 60000ms | 60000ms | 60000ms |
| 261.0 | 271.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 285.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 285.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 285.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -18.4%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1667880 | 82595 | 1750475.0 | 0.0% | 1745230.0 | 1833070.0 | -4.8% | True |
| app2 | 995070 | 49290 | 1044360.0 | 0.0% | 892066.0 | 1093650.0 | -18.4% | False |
| end-users | 4553460 | 225957 | 4779417.0 | 0.0% | 4893202.0 | 5005374.0 | -2.2% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1356 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 809 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3702 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5867). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5867 | 0.053ms | 0.197ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 264493 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1356 | 48188ms | 58819ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 809 | 77196ms | 115720ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3702 | 15910ms | 19708ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5867 | 17747ms | 88958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (29 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 700ms | 790ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 700ms | 790ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 700ms | 790ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 1229ms | 3083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 1292ms | 3470ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 1141ms | 2803ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 7750ms | 9795ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 5450ms | 7617ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 5636ms | 7737ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 13657ms | 19210ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 17857ms | 26000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 4833ms | 7337ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 22609ms | 29261ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 25667ms | 38625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 5661ms | 7693ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 6046ms | 7805ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 7030ms | 9488ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 7815ms | 9888ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 37670ms | 44574ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 84545ms | 116455ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 12132ms | 14713ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 52181ms | 59218ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 13028ms | 18567ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 17295ms | 19729ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 17416ms | 19742ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 131.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 131.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 131.0 | end-users | ok | 16900ms | 19690ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 17433ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 17042ms | 19704ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 16848ms | 19685ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 17516ms | 19781ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 17362ms | 19736ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 17484ms | 19748ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 17434ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 17086ms | 19709ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 17415ms | 19741ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 17284ms | 19767ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 18657ms | 28420ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 17621ms | 19981ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | ok | 39529ms | 57208ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | ok | 55909ms | 112683ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 285.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 285.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 285.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
