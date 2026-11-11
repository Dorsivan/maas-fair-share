# Fairness benchmark: full-contention-2x-discriminating (uni231-aa-T3b-lane2)

**Verdict: FAIL** (threshold: 10 points)
**Secondary (priority) verdict: PRIORITY-FAIL** -- see "Per-tenant TTFT / ITL and the priority verdict (UNI-226)" below for detail.
Worker-share vs. weight-share gap (UNI-225): 35.1 points

- end-users deviated -30.1 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:c8a088203f6dc6c48c158d21b6295172a78f18646b06c334e5310a0caedb259f` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-54b55dbd48-pc2st` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-11T14:36:27Z` |
| Run end | `2026-11-11T14:43:02Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 256 | 1927 | 000=1, 200=1918, 500=8 | 10.9 | 21.3 | 1485092.0 | 21.1% | 33.3% | 12.3 | 37.4% | 16.4 | 35.3% | 14.3 | 27.9s | 98.9% | 1919.0 |
| app2 | 10.0 | 256 | 1542 | 000=1, 200=1536, 500=5 | 11.7 | 45.8 | 961646.0 | 10.5% | 33.3% | 22.8 | 24.2% | 13.7 | 28.3% | 17.7 | 28.1s | 98.9% | 1537.0 |
| end-users | 65.0 | 256 | 1988 | 200=1982, 500=6 | 10.1 | 16.2 | 1521682.0 | 68.4% | 33.3% | -35.1 | 38.3% | -30.1 | 36.4% | -32.0 | 26.7s | 98.9% | 1981.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 1328.0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.0s | 98.9% | 1.0 |

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

**Windows** (40 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 10.0 | 20.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 10.0 | 20.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 10.0 | 20.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 20.0 | 30.0 | app1 | True | 31044.0 | 21.1% | 18.7% | -2.4 |
| 20.0 | 30.0 | app2 | True | 27070.0 | 10.5% | 16.3% | 5.8 |
| 20.0 | 30.0 | end-users | True | 108188.0 | 68.4% | 65.1% | -3.4 |
| 30.0 | 40.0 | app1 | True | 120320.0 | 21.1% | 38.7% | 17.6 |
| 30.0 | 40.0 | app2 | True | 20290.0 | 10.5% | 6.5% | -4.0 |
| 30.0 | 40.0 | end-users | True | 170334.0 | 68.4% | 54.8% | -13.6 |
| 40.0 | 50.0 | app1 | True | 129830.0 | 21.1% | 42.1% | 21.0 |
| 40.0 | 50.0 | app2 | True | 60844.0 | 10.5% | 19.7% | 9.2 |
| 40.0 | 50.0 | end-users | True | 117696.0 | 68.4% | 38.2% | -30.3 |
| 50.0 | 60.0 | app1 | True | 134004.0 | 21.1% | 45.9% | 24.8 |
| 50.0 | 60.0 | app2 | True | 56818.0 | 10.5% | 19.4% | 8.9 |
| 50.0 | 60.0 | end-users | True | 101426.0 | 68.4% | 34.7% | -33.7 |
| 60.0 | 70.0 | app1 | True | 131172.0 | 21.1% | 44.7% | 23.6 |
| 60.0 | 70.0 | app2 | True | 79854.0 | 10.5% | 27.2% | 16.7 |
| 60.0 | 70.0 | end-users | True | 82506.0 | 68.4% | 28.1% | -40.3 |
| 70.0 | 80.0 | app1 | True | 60944.0 | 21.1% | 20.0% | -1.0 |
| 70.0 | 80.0 | app2 | True | 48592.0 | 10.5% | 16.0% | 5.4 |
| 70.0 | 80.0 | end-users | True | 194760.0 | 68.4% | 64.0% | -4.4 |
| 80.0 | 90.0 | app1 | True | 151314.0 | 21.1% | 49.1% | 28.0 |
| 80.0 | 90.0 | app2 | True | 66290.0 | 10.5% | 21.5% | 11.0 |
| 80.0 | 90.0 | end-users | True | 90718.0 | 68.4% | 29.4% | -39.0 |
| 90.0 | 100.0 | app1 | True | 135246.0 | 21.1% | 44.2% | 23.2 |
| 90.0 | 100.0 | app2 | True | 85202.0 | 10.5% | 27.9% | 17.3 |
| 90.0 | 100.0 | end-users | True | 85272.0 | 68.4% | 27.9% | -40.5 |
| 100.0 | 110.0 | app1 | True | 74408.0 | 21.1% | 24.9% | 3.8 |
| 100.0 | 110.0 | app2 | True | 74424.0 | 10.5% | 24.9% | 14.4 |
| 100.0 | 110.0 | end-users | True | 150204.0 | 68.4% | 50.2% | -18.2 |
| 110.0 | 120.0 | app1 | True | 116250.0 | 21.1% | 38.0% | 17.0 |
| 110.0 | 120.0 | app2 | True | 85212.0 | 10.5% | 27.9% | 17.4 |
| 110.0 | 120.0 | end-users | True | 104144.0 | 68.4% | 34.1% | -34.3 |
| 120.0 | 130.0 | app1 | True | 109558.0 | 21.1% | 36.5% | 15.4 |
| 120.0 | 130.0 | app2 | True | 104192.0 | 10.5% | 34.7% | 24.2 |
| 120.0 | 130.0 | end-users | True | 86602.0 | 68.4% | 28.8% | -39.6 |
| 130.0 | 140.0 | app1 | True | 64960.0 | 21.1% | 31.6% | 10.5 |
| 130.0 | 140.0 | app2 | True | 91978.0 | 10.5% | 44.7% | 34.2 |
| 130.0 | 140.0 | end-users | True | 48678.0 | 68.4% | 23.7% | -44.7 |
| 140.0 | 151.0 | app1 | True | 56852.0 | 21.1% | 37.2% | 16.2 |
| 140.0 | 151.0 | app2 | True | 31066.0 | 10.5% | 20.3% | 9.8 |
| 140.0 | 151.0 | end-users | True | 64874.0 | 68.4% | 42.5% | -26.0 |
| 151.0 | 161.0 | app1 | True | 111020.0 | 21.1% | 43.0% | 21.9 |
| 151.0 | 161.0 | app2 | True | 79720.0 | 10.5% | 30.9% | 20.3 |
| 151.0 | 161.0 | end-users | True | 67648.0 | 68.4% | 26.2% | -42.2 |
| 161.0 | 171.0 | app1 | True | 12172.0 | 21.1% | 25.0% | 3.9 |
| 161.0 | 171.0 | app2 | True | 23024.0 | 10.5% | 47.2% | 36.7 |
| 161.0 | 171.0 | end-users | True | 13542.0 | 68.4% | 27.8% | -40.6 |
| 171.0 | 181.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 171.0 | 181.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 171.0 | 181.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 181.0 | 191.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 181.0 | 191.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 181.0 | 191.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 191.0 | 201.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 191.0 | 201.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 191.0 | 201.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 201.0 | 211.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 201.0 | 211.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 201.0 | 211.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 211.0 | 221.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 211.0 | 221.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 211.0 | 221.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 221.0 | 231.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 221.0 | 231.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 221.0 | 231.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 231.0 | 241.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 231.0 | 241.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 231.0 | 241.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 241.0 | 251.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 32482.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 23010.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 31032.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 13516.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 4060.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 4058.0 | n/a | n/a | n/a |
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
| 321.0 | 332.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 332.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 332.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 392.0 | 395.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 392.0 | 395.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 392.0 | 395.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 50 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app2 | ok | 55 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | end-users | ok | 40 | 0ms | 0ms | 8ms |
| 20.0 | 30.0 | app1 | ok | 43 | 38ms | 346ms | 485ms |
| 20.0 | 30.0 | app2 | ok | 42 | 127ms | 413ms | 491ms |
| 20.0 | 30.0 | end-users | ok | 172 | 1463ms | 2952ms | 4795ms |
| 30.0 | 40.0 | app1 | ok | 144 | 8333ms | 22000ms | 29200ms |
| 30.0 | 40.0 | app2 | ok | 31 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | end-users | ok | 71 | 1554ms | 3028ms | 4803ms |
| 40.0 | 50.0 | app1 | ok | 88 | 6094ms | 20737ms | 29074ms |
| 40.0 | 50.0 | app2 | ok | 43 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | end-users | ok | 102 | 1134ms | 2227ms | 2473ms |
| 50.0 | 60.0 | app1 | ok | 58 | 2500ms | 7100ms | 9710ms |
| 50.0 | 60.0 | app2 | ok | 66 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | end-users | ok | 72 | 1938ms | 4857ms | 9400ms |
| 60.0 | 70.0 | app1 | ok | 127 | 1635ms | 3779ms | 4878ms |
| 60.0 | 70.0 | app2 | ok | 49 | 45000ms | 57000ms | 59700ms |
| 60.0 | 70.0 | end-users | ok | 115 | 4178ms | 8722ms | 9872ms |
| 70.0 | 80.0 | app1 | ok | 58 | 3807ms | 6375ms | 9638ms |
| 70.0 | 80.0 | app2 | ok | 13 | 45000ms | 57000ms | 59700ms |
| 70.0 | 80.0 | end-users | ok | 78 | 1500ms | 3974ms | 4897ms |
| 80.0 | 90.0 | app1 | ok | 104 | 1469ms | 2444ms | 4675ms |
| 80.0 | 90.0 | app2 | ok | 67 | 41727ms | 56345ms | 59635ms |
| 80.0 | 90.0 | end-users | ok | 67 | 1358ms | 2272ms | 2477ms |
| 90.0 | 100.0 | app1 | ok | 94 | 1062ms | 2238ms | 2650ms |
| 90.0 | 100.0 | app2 | ok | 58 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | end-users | ok | 105 | 1069ms | 2236ms | 2499ms |
| 100.0 | 110.0 | app1 | ok | 52 | 722ms | 2013ms | 2451ms |
| 100.0 | 110.0 | app2 | ok | 84 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | end-users | ok | 92 | 914ms | 2163ms | 2466ms |
| 110.0 | 120.0 | app1 | ok | 99 | 1519ms | 2433ms | 4646ms |
| 110.0 | 120.0 | app2 | ok | 54 | 18511ms | 27702ms | 29770ms |
| 110.0 | 120.0 | end-users | ok | 62 | 1375ms | 2408ms | 4613ms |
| 120.0 | 130.0 | app1 | ok | 67 | 1536ms | 3477ms | 4848ms |
| 120.0 | 130.0 | app2 | ok | 85 | 7917ms | 24333ms | 29433ms |
| 120.0 | 130.0 | end-users | ok | 69 | 712ms | 2206ms | 4138ms |
| 130.0 | 140.0 | app1 | ok | 56 | 0ms | 55ms | 720ms |
| 130.0 | 140.0 | app2 | ok | 58 | 0ms | 30ms | 855ms |
| 130.0 | 140.0 | end-users | ok | 71 | 0ms | 64ms | 645ms |
| 140.0 | 151.0 | app1 | ok | 91 | 231ms | 1880ms | 2438ms |
| 140.0 | 151.0 | app2 | ok | 69 | 212ms | 1983ms | 2448ms |
| 140.0 | 151.0 | end-users | ok | 93 | 134ms | 1803ms | 2430ms |
| 151.0 | 161.0 | app1 | ok | 74 | 232ms | 664ms | 966ms |
| 151.0 | 161.0 | app2 | ok | 58 | 344ms | 888ms | 2065ms |
| 151.0 | 161.0 | end-users | ok | 57 | 235ms | 810ms | 981ms |
| 161.0 | 171.0 | app1 | ok | 59 | 0ms | 0ms | 1ms |
| 161.0 | 171.0 | app2 | ok | 90 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | end-users | ok | 68 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | app1 | ok | 71 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | app2 | ok | 66 | 0ms | 0ms | 2ms |
| 171.0 | 181.0 | end-users | ok | 82 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | app1 | ok | 88 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | app2 | ok | 53 | 0ms | 0ms | 4ms |
| 181.0 | 191.0 | end-users | ok | 72 | 0ms | 0ms | 4ms |
| 191.0 | 201.0 | app1 | ok | 62 | 0ms | 0ms | 7ms |
| 191.0 | 201.0 | app2 | ok | 93 | 0ms | 0ms | 5ms |
| 191.0 | 201.0 | end-users | ok | 65 | 0ms | 0ms | 1ms |
| 201.0 | 211.0 | app1 | ok | 71 | 0ms | 0ms | 1ms |
| 201.0 | 211.0 | app2 | ok | 65 | 0ms | 0ms | 0ms |
| 201.0 | 211.0 | end-users | ok | 67 | 0ms | 0ms | 4ms |
| 211.0 | 221.0 | app1 | ok | 78 | 0ms | 0ms | 2ms |
| 211.0 | 221.0 | app2 | ok | 73 | 0ms | 0ms | 2ms |
| 211.0 | 221.0 | end-users | ok | 80 | 0ms | 0ms | 2ms |
| 221.0 | 231.0 | app1 | ok | 71 | 0ms | 0ms | 1ms |
| 221.0 | 231.0 | app2 | ok | 56 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | end-users | ok | 78 | 0ms | 0ms | 1ms |
| 231.0 | 241.0 | app1 | ok | 79 | 0ms | 0ms | 2ms |
| 231.0 | 241.0 | app2 | ok | 104 | 0ms | 0ms | 1ms |
| 231.0 | 241.0 | end-users | ok | 66 | 0ms | 0ms | 2ms |
| 241.0 | 251.0 | app1 | ok | 74 | 0ms | 0ms | 2ms |
| 241.0 | 251.0 | app2 | ok | 67 | 0ms | 0ms | 7ms |
| 241.0 | 251.0 | end-users | ok | 85 | 0ms | 0ms | 2ms |
| 251.0 | 261.0 | app1 | ok | 61 | 0ms | 695ms | 970ms |
| 251.0 | 261.0 | app2 | ok | 38 | 0ms | 525ms | 952ms |
| 251.0 | 261.0 | end-users | ok | 52 | 0ms | 825ms | 1720ms |
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
| 321.0 | 332.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 332.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 332.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 395.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 395.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 395.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -42.8%
- app2 exceeded the 10% ledger tolerance: cost -53.7%
- end-users exceeded the 10% ledger tolerance: cost -43.2%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2359140 | 117862 | 2477002.0 | 0.0% | 1485092.0 | 2594864.0 | -42.8% | False |
| app2 | 1889280 | 94377 | 1983657.0 | 0.0% | 961646.0 | 2078034.0 | -53.7% | False |
| end-users | 2437860 | 121345 | 2557926.0 | -0.0% | 1521682.0 | 2680550.0 | -43.2% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1927 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1542 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1988 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5438). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5438 | 0.057ms | 0.499ms | (0, 0.1]ms | (0.2, 0.5]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 315457 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1918 | 4237ms | 13889ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1536 | 3033ms | 40447ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 1981 | 3453ms | 8900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5436 | 3604ms | 28832ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: PRIORITY-FAIL** -- the share verdict above is FAIL, so this is the board's second, independent success criterion (2026-11-10): did the policy nonetheless order tenants by weight? Top-weighted group: `end-users` (TTFT p50 3453ms, p95 8900ms, strictly lowest among distinctly-weighted groups: p50=False/p95=True; no rank inversion among any distinctly-weighted pair: False -- this, not raw rank correlation, is what gates the verdict, since a genuine weight tie (e.g. 98/1/1's app2==end-users) makes exact correlation 1.0 unreachable by construction even when ordering is otherwise perfect). Rank correlation -0.50 (1.00 = exact agreement, informational only) shown for reference. Separation from the next distinctly-weighted group: -420ms against a noise floor of not given (separation check skipped).

**Windowed TTFT/ITL** (40 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 724ms | 1225ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 734ms | 1202ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 726ms | 1225ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 2912ms | 7485ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 3450ms | 9183ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 3829ms | 5720ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 12528ms | 14804ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 9667ms | 19375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 6500ms | 7850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 15000ms | 19500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 20217ms | 29022ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 5160ms | 5993ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 10455ms | 14545ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 32400ms | 43740ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 4528ms | 5688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 5198ms | 7307ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 10878ms | 14588ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 7188ms | 9719ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 7305ms | 14194ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 7349ms | 13833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 4455ms | 7150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 5800ms | 7778ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 4196ms | 5768ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 5773ms | 7780ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 28088ms | 43036ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 4276ms | 5811ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 5582ms | 7427ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 24836ms | 29484ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 4032ms | 5729ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 5841ms | 7883ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 18775ms | 28519ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 3661ms | 5814ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 3883ms | 7043ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 9286ms | 15450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 3574ms | 5125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 151.0 | app1 | ok | 4361ms | 7211ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 151.0 | app2 | ok | 3625ms | 7678ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 151.0 | end-users | ok | 3492ms | 5329ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 4090ms | 4981ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 4674ms | 6883ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 3615ms | 4733ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 1659ms | 3864ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 1830ms | 5394ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 1673ms | 3831ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 2223ms | 2922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 2148ms | 2915ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 2220ms | 2922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 1320ms | 1986ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 1367ms | 2375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 1333ms | 2627ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 1081ms | 1485ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 1079ms | 1483ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 1079ms | 1496ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 1442ms | 2240ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 1332ms | 1980ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 1354ms | 1929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 1188ms | 2659ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 1062ms | 2622ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 1320ms | 2635ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 1258ms | 1957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 1130ms | 1935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 1315ms | 1911ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 1700ms | 2870ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 1737ms | 2866ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 1578ms | 2816ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 2155ms | 2915ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 2281ms | 2928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 2107ms | 2911ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 2985ms | 5617ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 3139ms | 7060ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 2941ms | 6560ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 321.0 | 332.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 332.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 332.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 395.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 395.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 395.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
