# Fairness benchmark: full-contention-2x-discriminating (uni231-aa-A2b-lane2)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-54b55dbd48-98wcq` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-11T12:57:22Z` |
| Run end | `2026-11-11T13:03:22Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 256 | 1365 | 200=1365 | 51.9 | 58.8 | 1741728.0 | 21.1% | 33.3% | 12.3 | 23.5% | 2.5 | 23.5% | 2.4 | 81.7s | 98.9% | 1365.0 |
| app2 | 10.0 | 256 | 821 | 200=821 | 87.3 | 113.9 | 871166.0 | 10.5% | 33.3% | 22.8 | 11.8% | 1.2 | 14.1% | 3.6 | 81.7s | 98.9% | 821.0 |
| end-users | 65.0 | 256 | 3623 | 000=1, 200=3622 | 15.6 | 19.8 | 4793680.0 | 68.4% | 33.3% | -35.1 | 64.7% | -3.7 | 62.4% | -6.1 | 77.8s | 98.9% | 3623.0 |
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
| 0.0 | 100.0 | 100.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (36 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 10.0 | 20.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 10.0 | 20.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 10.0 | 20.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 20.0 | 30.0 | app1 | True | 75760.0 | 21.1% | 28.1% | 7.1 |
| 20.0 | 30.0 | app2 | True | 60994.0 | 10.5% | 22.6% | 12.1 |
| 20.0 | 30.0 | end-users | True | 132632.0 | 68.4% | 49.2% | -19.2 |
| 30.0 | 40.0 | app1 | True | 86498.0 | 21.1% | 27.8% | 6.8 |
| 30.0 | 40.0 | app2 | True | 13534.0 | 10.5% | 4.4% | -6.2 |
| 30.0 | 40.0 | end-users | True | 210944.0 | 68.4% | 67.8% | -0.6 |
| 40.0 | 50.0 | app1 | True | 94612.0 | 21.1% | 31.0% | 9.9 |
| 40.0 | 50.0 | app2 | True | 33822.0 | 10.5% | 11.1% | 0.5 |
| 40.0 | 50.0 | end-users | True | 177168.0 | 68.4% | 58.0% | -10.4 |
| 50.0 | 60.0 | app1 | True | 74366.0 | 21.1% | 24.0% | 3.0 |
| 50.0 | 60.0 | app2 | True | 35148.0 | 10.5% | 11.3% | 0.8 |
| 50.0 | 60.0 | end-users | True | 200252.0 | 68.4% | 64.6% | -3.8 |
| 60.0 | 70.0 | app1 | True | 70318.0 | 21.1% | 22.9% | 1.8 |
| 60.0 | 70.0 | app2 | True | 36540.0 | 10.5% | 11.9% | 1.4 |
| 60.0 | 70.0 | end-users | True | 200218.0 | 68.4% | 65.2% | -3.2 |
| 70.0 | 80.0 | app1 | True | 24330.0 | 21.1% | 8.0% | -13.1 |
| 70.0 | 80.0 | app2 | True | 12152.0 | 10.5% | 4.0% | -6.5 |
| 70.0 | 80.0 | end-users | True | 269028.0 | 68.4% | 88.1% | 19.6 |
| 80.0 | 90.0 | app1 | True | 66366.0 | 21.1% | 22.1% | 1.0 |
| 80.0 | 90.0 | app2 | True | 32442.0 | 10.5% | 10.8% | 0.3 |
| 80.0 | 90.0 | end-users | True | 201650.0 | 68.4% | 67.1% | -1.3 |
| 90.0 | 100.0 | app1 | True | 32458.0 | 21.1% | 11.2% | -9.8 |
| 90.0 | 100.0 | app2 | True | 21634.0 | 10.5% | 7.5% | -3.0 |
| 90.0 | 100.0 | end-users | True | 235190.0 | 68.4% | 81.3% | 12.9 |
| 100.0 | 110.0 | app1 | True | 67612.0 | 21.1% | 22.1% | 1.1 |
| 100.0 | 110.0 | app2 | True | 29704.0 | 10.5% | 9.7% | -0.8 |
| 100.0 | 110.0 | end-users | True | 208368.0 | 68.4% | 68.2% | -0.3 |
| 110.0 | 121.0 | app1 | True | 60890.0 | 21.1% | 20.3% | -0.8 |
| 110.0 | 121.0 | app2 | True | 29778.0 | 10.5% | 9.9% | -0.6 |
| 110.0 | 121.0 | end-users | True | 209738.0 | 68.4% | 69.8% | 1.4 |
| 121.0 | 131.0 | app1 | True | 52720.0 | 21.1% | 20.8% | -0.2 |
| 121.0 | 131.0 | app2 | True | 27038.0 | 10.5% | 10.7% | 0.2 |
| 121.0 | 131.0 | end-users | True | 173196.0 | 68.4% | 68.5% | 0.0 |
| 131.0 | 141.0 | app1 | True | 64834.0 | 21.1% | 21.4% | 0.3 |
| 131.0 | 141.0 | app2 | True | 33800.0 | 10.5% | 11.2% | 0.6 |
| 131.0 | 141.0 | end-users | True | 204390.0 | 68.4% | 67.5% | -1.0 |
| 141.0 | 151.0 | app1 | True | 63622.0 | 21.1% | 20.8% | -0.3 |
| 141.0 | 151.0 | app2 | True | 31104.0 | 10.5% | 10.2% | -0.4 |
| 141.0 | 151.0 | end-users | True | 211126.0 | 68.4% | 69.0% | 0.6 |
| 151.0 | 161.0 | app1 | True | 66200.0 | 21.1% | 21.5% | 0.4 |
| 151.0 | 161.0 | app2 | True | 31104.0 | 10.5% | 10.1% | -0.4 |
| 151.0 | 161.0 | end-users | True | 210812.0 | 68.4% | 68.4% | -0.0 |
| 161.0 | 171.0 | app1 | True | 66174.0 | 21.1% | 21.6% | 0.6 |
| 161.0 | 171.0 | app2 | True | 32458.0 | 10.5% | 10.6% | 0.1 |
| 161.0 | 171.0 | end-users | True | 207056.0 | 68.4% | 67.7% | -0.7 |
| 171.0 | 181.0 | app1 | True | 63510.0 | 21.1% | 20.9% | -0.2 |
| 171.0 | 181.0 | app2 | True | 32474.0 | 10.5% | 10.7% | 0.1 |
| 171.0 | 181.0 | end-users | True | 208302.0 | 68.4% | 68.5% | 0.0 |
| 181.0 | 191.0 | app1 | True | 44686.0 | 21.1% | 19.7% | -1.4 |
| 181.0 | 191.0 | app2 | True | 25722.0 | 10.5% | 11.3% | 0.8 |
| 181.0 | 191.0 | end-users | True | 156970.0 | 68.4% | 69.0% | 0.6 |
| 191.0 | 201.0 | app1 | True | 64884.0 | 21.1% | 22.4% | 1.4 |
| 191.0 | 201.0 | app2 | True | 29764.0 | 10.5% | 10.3% | -0.2 |
| 191.0 | 201.0 | end-users | True | 194778.0 | 68.4% | 67.3% | -1.1 |
| 201.0 | 211.0 | app1 | True | 63568.0 | 21.1% | 20.5% | -0.5 |
| 201.0 | 211.0 | app2 | True | 33802.0 | 10.5% | 10.9% | 0.4 |
| 201.0 | 211.0 | end-users | True | 212194.0 | 68.4% | 68.5% | 0.1 |
| 211.0 | 221.0 | app1 | True | 62236.0 | 21.1% | 20.4% | -0.7 |
| 211.0 | 221.0 | app2 | True | 29764.0 | 10.5% | 9.7% | -0.8 |
| 211.0 | 221.0 | end-users | True | 213620.0 | 68.4% | 69.9% | 1.5 |
| 221.0 | 231.0 | app1 | True | 64956.0 | 21.1% | 22.8% | 1.7 |
| 221.0 | 231.0 | app2 | True | 31052.0 | 10.5% | 10.9% | 0.4 |
| 221.0 | 231.0 | end-users | True | 189398.0 | 68.4% | 66.4% | -2.1 |
| 231.0 | 241.0 | app1 | True | 62234.0 | 21.1% | 20.2% | -0.9 |
| 231.0 | 241.0 | app2 | True | 31048.0 | 10.5% | 10.1% | -0.5 |
| 231.0 | 241.0 | end-users | True | 214994.0 | 68.4% | 69.7% | 1.3 |
| 241.0 | 251.0 | app1 | False | 64934.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 35166.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 208208.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 104198.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 50050.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 143448.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 160822.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 82630.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 18940.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 28442.0 | n/a | n/a | n/a |
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
| 331.0 | 342.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 342.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 342.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 352.0 | 360.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 352.0 | 360.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 352.0 | 360.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 5 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 2 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 4 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 129 | 0ms | 878ms | 2285ms |
| 10.0 | 20.0 | app2 | ok | 117 | 0ms | 939ms | 2324ms |
| 10.0 | 20.0 | end-users | ok | 117 | 0ms | 786ms | 2061ms |
| 20.0 | 30.0 | app1 | ok | 2 | 7500ms | 9500ms | 9950ms |
| 20.0 | 30.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 125 | 2158ms | 4399ms | 4940ms |
| 30.0 | 40.0 | app1 | ok | 104 | 13750ms | 26750ms | 29675ms |
| 30.0 | 40.0 | app2 | ok | 14 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | end-users | ok | 114 | 1587ms | 3500ms | 9050ms |
| 40.0 | 50.0 | app1 | ok | 65 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app2 | ok | 28 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | end-users | ok | 156 | 1463ms | 3227ms | 4823ms |
| 50.0 | 60.0 | app1 | ok | 45 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app2 | ok | 23 | 45000ms | 57000ms | 59700ms |
| 50.0 | 60.0 | end-users | ok | 162 | 1439ms | 2421ms | 4632ms |
| 60.0 | 70.0 | app1 | ok | 37 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app2 | ok | 19 | 45000ms | 57000ms | 59700ms |
| 60.0 | 70.0 | end-users | ok | 191 | 1352ms | 2498ms | 4749ms |
| 70.0 | 80.0 | app1 | ok | 54 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app2 | ok | 27 | 45000ms | 57000ms | 59700ms |
| 70.0 | 80.0 | end-users | ok | 109 | 1439ms | 3397ms | 4840ms |
| 80.0 | 90.0 | app1 | ok | 17 | 45000ms | 57000ms | 59700ms |
| 80.0 | 90.0 | app2 | ok | 9 | 60000ms | 60000ms | 60000ms |
| 80.0 | 90.0 | end-users | ok | 214 | 2942ms | 4588ms | 4959ms |
| 90.0 | 100.0 | app1 | ok | 28 | 45000ms | 57000ms | 59700ms |
| 90.0 | 100.0 | app2 | ok | 14 | 60000ms | 60000ms | 60000ms |
| 90.0 | 100.0 | end-users | ok | 157 | 3590ms | 7383ms | 9738ms |
| 100.0 | 110.0 | app1 | ok | 54 | 45000ms | 57000ms | 59700ms |
| 100.0 | 110.0 | app2 | ok | 28 | 60000ms | 60000ms | 60000ms |
| 100.0 | 110.0 | end-users | ok | 175 | 7636ms | 9744ms | 26111ms |
| 110.0 | 121.0 | app1 | ok | 38 | 45000ms | 57000ms | 59700ms |
| 110.0 | 121.0 | app2 | ok | 19 | 60000ms | 60000ms | 60000ms |
| 110.0 | 121.0 | end-users | ok | 122 | 13056ms | 26611ms | 29661ms |
| 121.0 | 131.0 | app1 | ok | 52 | 45000ms | 57000ms | 59700ms |
| 121.0 | 131.0 | app2 | ok | 25 | 60000ms | 60000ms | 60000ms |
| 121.0 | 131.0 | end-users | ok | 168 | 16341ms | 27268ms | 29727ms |
| 131.0 | 141.0 | app1 | ok | 47 | 45000ms | 57000ms | 59700ms |
| 131.0 | 141.0 | app2 | ok | 24 | 60000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | end-users | ok | 152 | 20000ms | 28000ms | 29800ms |
| 141.0 | 151.0 | app1 | ok | 40 | 45000ms | 57000ms | 59700ms |
| 141.0 | 151.0 | app2 | ok | 20 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | end-users | ok | 131 | 20000ms | 28000ms | 29800ms |
| 151.0 | 161.0 | app1 | ok | 51 | 45000ms | 57000ms | 59700ms |
| 151.0 | 161.0 | app2 | ok | 25 | 60000ms | 60000ms | 60000ms |
| 151.0 | 161.0 | end-users | ok | 160 | 20000ms | 28000ms | 29800ms |
| 161.0 | 171.0 | app1 | ok | 49 | 45000ms | 57000ms | 59700ms |
| 161.0 | 171.0 | app2 | ok | 26 | 60000ms | 60000ms | 60000ms |
| 161.0 | 171.0 | end-users | ok | 163 | 20000ms | 28000ms | 29800ms |
| 171.0 | 181.0 | app1 | ok | 64 | 45000ms | 57000ms | 59700ms |
| 171.0 | 181.0 | app2 | ok | 30 | 60000ms | 60000ms | 60000ms |
| 171.0 | 181.0 | end-users | ok | 206 | 17044ms | 27409ms | 29741ms |
| 181.0 | 191.0 | app1 | ok | 31 | 45000ms | 57000ms | 59700ms |
| 181.0 | 191.0 | app2 | ok | 16 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | end-users | ok | 104 | 18444ms | 27689ms | 29769ms |
| 191.0 | 201.0 | app1 | ok | 27 | 45000ms | 57000ms | 59700ms |
| 191.0 | 201.0 | app2 | ok | 14 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | end-users | ok | 84 | 19756ms | 27951ms | 29795ms |
| 201.0 | 211.0 | app1 | ok | 46 | 45000ms | 57000ms | 59700ms |
| 201.0 | 211.0 | app2 | ok | 23 | 60000ms | 60000ms | 60000ms |
| 201.0 | 211.0 | end-users | ok | 150 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app1 | ok | 50 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | app2 | ok | 25 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | end-users | ok | 163 | 19551ms | 27910ms | 29791ms |
| 221.0 | 231.0 | app1 | ok | 50 | 45000ms | 57000ms | 59700ms |
| 221.0 | 231.0 | app2 | ok | 25 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | end-users | ok | 162 | 20000ms | 28000ms | 29800ms |
| 231.0 | 241.0 | app1 | ok | 42 | 45000ms | 57000ms | 59700ms |
| 231.0 | 241.0 | app2 | ok | 21 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | end-users | ok | 136 | 19032ms | 27806ms | 29781ms |
| 241.0 | 251.0 | app1 | ok | 61 | 45000ms | 57000ms | 59700ms |
| 241.0 | 251.0 | app2 | ok | 31 | 60000ms | 60000ms | 60000ms |
| 241.0 | 251.0 | end-users | ok | 198 | 19688ms | 27938ms | 29794ms |
| 251.0 | 261.0 | app1 | ok | 111 | 44725ms | 56945ms | 59694ms |
| 251.0 | 261.0 | app2 | ok | 54 | 60000ms | 60000ms | 60000ms |
| 251.0 | 261.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | ok | 66 | 27368ms | 52929ms | 59293ms |
| 261.0 | 271.0 | app2 | ok | 162 | 60000ms | 60000ms | 60000ms |
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
| 331.0 | 342.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 342.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 342.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 360.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 360.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 360.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -21.6%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1678950 | 83517 | 1762467.0 | 0.0% | 1741728.0 | 1845984.0 | -5.6% | True |
| app2 | 1009830 | 50343 | 1060173.0 | 0.0% | 871166.0 | 1110516.0 | -21.6% | False |
| end-users | 4455060 | 222055 | 4677115.0 | 0.0% | 4793680.0 | 4899170.0 | -2.2% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1365 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 821 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3623 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5809). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5809 | 0.054ms | 0.198ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 328185 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1365 | 47546ms | 58837ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 821 | 74219ms | 115422ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3622 | 15356ms | 19921ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5808 | 17480ms | 87912ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (36 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 700ms | 790ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 700ms | 790ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 700ms | 790ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 1875ms | 3600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 1750ms | 3672ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 1350ms | 2981ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 6500ms | 9157ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 5933ms | 14368ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 5531ms | 7767ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 14000ms | 19333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 5935ms | 13607ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 19487ms | 28871ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 4711ms | 6908ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 21406ms | 29141ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 36875ms | 44188ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 6103ms | 7810ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 25306ms | 32000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 44464ms | 58442ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 5149ms | 7565ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 33750ms | 43875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 5500ms | 7703ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 58846ms | 113455ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 7121ms | 9519ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 47143ms | 58714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 8233ms | 11045ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 11562ms | 14656ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 121.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 121.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 121.0 | end-users | ok | 13229ms | 18893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 17176ms | 19843ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 52660ms | 59553ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 18401ms | 28112ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 17131ms | 20250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 17400ms | 19740ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 17433ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 17467ms | 19747ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 19286ms | 28800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 52663ms | 59560ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 18278ms | 28131ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 16985ms | 19698ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 53000ms | 72000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 16930ms | 19693ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 17314ms | 19731ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 17484ms | 19748ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | ok | 41297ms | 57769ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | ok | 58571ms | 113571ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 342.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 342.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 342.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 360.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 360.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 360.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
