# Fairness benchmark: full-contention-2x-discriminating (uni231-aa-T3a-inst1)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5fbdd988df-dwxqm` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-11T22:33:30Z` |
| Run end | `2026-11-11T22:39:25Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 256 | 1226 | 000=2, 200=1224 | 56.5 | 72.9 | 1600592.0 | 21.1% | 33.3% | 12.3 | 23.8% | 2.8 | 24.0% | 2.9 | 41.1s | 98.9% | 1226.0 |
| app2 | 10.0 | 256 | 834 | 200=834 | 92.5 | 134.2 | 1064192.0 | 10.5% | 33.3% | 22.8 | 15.8% | 5.3 | 16.3% | 5.8 | 41.1s | 98.9% | 834.0 |
| end-users | 65.0 | 256 | 3049 | 000=5, 200=3044 | 17.1 | 49.5 | 4055984.0 | 68.4% | 33.3% | -35.1 | 60.4% | -8.1 | 59.7% | -8.7 | 40.3s | 98.9% | 3049.0 |
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
| 0.0 | 141.0 | 141.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (36 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 10.0 | 20.0 | app1 | True | 39142.0 | 21.1% | 20.5% | -0.5 |
| 10.0 | 20.0 | app2 | True | 39120.0 | 10.5% | 20.5% | 10.0 |
| 10.0 | 20.0 | end-users | True | 112296.0 | 68.4% | 58.9% | -9.5 |
| 20.0 | 30.0 | app1 | True | 106914.0 | 21.1% | 68.7% | 47.7 |
| 20.0 | 30.0 | app2 | True | 6780.0 | 10.5% | 4.4% | -6.2 |
| 20.0 | 30.0 | end-users | True | 41896.0 | 68.4% | 26.9% | -41.5 |
| 30.0 | 41.0 | app1 | True | 17610.0 | 21.1% | 7.3% | -13.7 |
| 30.0 | 41.0 | app2 | True | 127270.0 | 10.5% | 53.1% | 42.6 |
| 30.0 | 41.0 | end-users | True | 94718.0 | 68.4% | 39.5% | -28.9 |
| 41.0 | 51.0 | app1 | True | 2710.0 | 21.1% | 1.1% | -19.9 |
| 41.0 | 51.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 41.0 | 51.0 | end-users | True | 240696.0 | 68.4% | 98.9% | 30.5 |
| 51.0 | 61.0 | app1 | True | 55410.0 | 21.1% | 19.3% | -1.7 |
| 51.0 | 61.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 51.0 | 61.0 | end-users | True | 231206.0 | 68.4% | 80.7% | 12.2 |
| 61.0 | 71.0 | app1 | True | 52800.0 | 21.1% | 23.0% | 1.9 |
| 61.0 | 71.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 61.0 | 71.0 | end-users | True | 177222.0 | 68.4% | 77.0% | 8.6 |
| 71.0 | 81.0 | app1 | True | 35126.0 | 21.1% | 22.6% | 1.5 |
| 71.0 | 81.0 | app2 | True | 6738.0 | 10.5% | 4.3% | -6.2 |
| 71.0 | 81.0 | end-users | True | 113746.0 | 68.4% | 73.1% | 4.7 |
| 81.0 | 91.0 | app1 | True | 101376.0 | 21.1% | 65.2% | 44.2 |
| 81.0 | 91.0 | app2 | True | 50036.0 | 10.5% | 32.2% | 21.7 |
| 81.0 | 91.0 | end-users | True | 4052.0 | 68.4% | 2.6% | -65.8 |
| 91.0 | 101.0 | app1 | True | 102768.0 | 21.1% | 67.2% | 46.2 |
| 91.0 | 101.0 | app2 | True | 48734.0 | 10.5% | 31.9% | 21.4 |
| 91.0 | 101.0 | end-users | True | 1350.0 | 68.4% | 0.9% | -67.5 |
| 101.0 | 111.0 | app1 | True | 35188.0 | 21.1% | 17.8% | -3.2 |
| 101.0 | 111.0 | app2 | True | 108054.0 | 10.5% | 54.7% | 44.2 |
| 101.0 | 111.0 | end-users | True | 54160.0 | 68.4% | 27.4% | -41.0 |
| 111.0 | 121.0 | app1 | True | 2706.0 | 21.1% | 1.2% | -19.9 |
| 111.0 | 121.0 | app2 | True | 35178.0 | 10.5% | 15.0% | 4.5 |
| 111.0 | 121.0 | end-users | True | 196184.0 | 68.4% | 83.8% | 15.4 |
| 121.0 | 131.0 | app1 | True | 17584.0 | 21.1% | 7.7% | -13.3 |
| 121.0 | 131.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 121.0 | 131.0 | end-users | True | 209620.0 | 68.4% | 92.3% | 23.8 |
| 131.0 | 141.0 | app1 | True | 60888.0 | 21.1% | 23.7% | 2.6 |
| 131.0 | 141.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 131.0 | 141.0 | end-users | True | 196050.0 | 68.4% | 76.3% | 7.9 |
| 141.0 | 151.0 | app1 | True | 66252.0 | 21.1% | 21.8% | 0.7 |
| 141.0 | 151.0 | app2 | True | 14840.0 | 10.5% | 4.9% | -5.7 |
| 141.0 | 151.0 | end-users | True | 223302.0 | 68.4% | 73.4% | 4.9 |
| 151.0 | 161.0 | app1 | True | 56704.0 | 21.1% | 20.4% | -0.7 |
| 151.0 | 161.0 | app2 | True | 31118.0 | 10.5% | 11.2% | 0.6 |
| 151.0 | 161.0 | end-users | True | 190798.0 | 68.4% | 68.5% | 0.1 |
| 161.0 | 171.0 | app1 | True | 67528.0 | 21.1% | 22.4% | 1.4 |
| 161.0 | 171.0 | app2 | True | 31080.0 | 10.5% | 10.3% | -0.2 |
| 161.0 | 171.0 | end-users | True | 202684.0 | 68.4% | 67.3% | -1.1 |
| 171.0 | 181.0 | app1 | True | 62244.0 | 21.1% | 20.4% | -0.7 |
| 171.0 | 181.0 | app2 | True | 31104.0 | 10.5% | 10.2% | -0.4 |
| 171.0 | 181.0 | end-users | True | 212416.0 | 68.4% | 69.5% | 1.0 |
| 181.0 | 191.0 | app1 | True | 64906.0 | 21.1% | 21.2% | 0.2 |
| 181.0 | 191.0 | app2 | True | 32510.0 | 10.5% | 10.6% | 0.1 |
| 181.0 | 191.0 | end-users | True | 208308.0 | 68.4% | 68.1% | -0.3 |
| 191.0 | 201.0 | app1 | True | 63392.0 | 21.1% | 20.8% | -0.2 |
| 191.0 | 201.0 | app2 | True | 32466.0 | 10.5% | 10.7% | 0.1 |
| 191.0 | 201.0 | end-users | True | 208354.0 | 68.4% | 68.5% | 0.1 |
| 201.0 | 211.0 | app1 | True | 66316.0 | 21.1% | 21.7% | 0.6 |
| 201.0 | 211.0 | app2 | True | 32502.0 | 10.5% | 10.6% | 0.1 |
| 201.0 | 211.0 | end-users | True | 206976.0 | 68.4% | 67.7% | -0.7 |
| 211.0 | 221.0 | app1 | True | 60906.0 | 21.1% | 21.1% | 0.1 |
| 211.0 | 221.0 | app2 | True | 31130.0 | 10.5% | 10.8% | 0.3 |
| 211.0 | 221.0 | end-users | True | 196102.0 | 68.4% | 68.1% | -0.4 |
| 221.0 | 231.0 | app1 | True | 47240.0 | 21.1% | 19.6% | -1.4 |
| 221.0 | 231.0 | app2 | True | 24330.0 | 10.5% | 10.1% | -0.4 |
| 221.0 | 231.0 | end-users | True | 169052.0 | 68.4% | 70.3% | 1.8 |
| 231.0 | 241.0 | app1 | True | 66260.0 | 21.1% | 22.3% | 1.2 |
| 231.0 | 241.0 | app2 | True | 32490.0 | 10.5% | 10.9% | 0.4 |
| 231.0 | 241.0 | end-users | True | 198684.0 | 68.4% | 66.8% | -1.6 |
| 241.0 | 252.0 | app1 | False | 55458.0 | n/a | n/a | n/a |
| 241.0 | 252.0 | app2 | False | 29706.0 | n/a | n/a | n/a |
| 241.0 | 252.0 | end-users | False | 193152.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | app1 | False | 43200.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | app2 | False | 17582.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | end-users | False | 127094.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | app1 | False | 71712.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | app2 | False | 37812.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | end-users | False | 45866.0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app1 | False | 106650.0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app2 | False | 51434.0 | n/a | n/a | n/a |
| 272.0 | 282.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 282.0 | 292.0 | app1 | False | 71602.0 | n/a | n/a | n/a |
| 282.0 | 292.0 | app2 | False | 79740.0 | n/a | n/a | n/a |
| 282.0 | 292.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 292.0 | 302.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 292.0 | 302.0 | app2 | False | 132438.0 | n/a | n/a | n/a |
| 292.0 | 302.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 302.0 | 312.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 302.0 | 312.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 302.0 | 312.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 312.0 | 322.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 312.0 | 322.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 312.0 | 322.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 352.0 | 355.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 352.0 | 355.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 352.0 | 355.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 65 | 0ms | 536ms | 954ms |
| 0.0 | 10.0 | app2 | ok | 73 | 0ms | 481ms | 948ms |
| 0.0 | 10.0 | end-users | ok | 59 | 0ms | 579ms | 958ms |
| 10.0 | 20.0 | app1 | ok | 96 | 1471ms | 2294ms | 2479ms |
| 10.0 | 20.0 | app2 | ok | 102 | 1375ms | 2275ms | 2478ms |
| 10.0 | 20.0 | end-users | ok | 102 | 1391ms | 2278ms | 2478ms |
| 20.0 | 30.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 41.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 41.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 41.0 | end-users | ok | 161 | 20000ms | 28000ms | 29800ms |
| 41.0 | 51.0 | app1 | ok | 21 | 20000ms | 28000ms | 29800ms |
| 41.0 | 51.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 41.0 | 51.0 | end-users | ok | 145 | 14239ms | 26848ms | 29685ms |
| 51.0 | 61.0 | app1 | ok | 268 | 39900ms | 55980ms | 59598ms |
| 51.0 | 61.0 | app2 | ok | 184 | 42532ms | 56506ms | 59651ms |
| 51.0 | 61.0 | end-users | ok | 345 | 6723ms | 21977ms | 29198ms |
| 61.0 | 71.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 61.0 | 71.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 61.0 | 71.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 71.0 | 81.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 71.0 | 81.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 71.0 | 81.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 81.0 | 91.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 81.0 | 91.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 81.0 | 91.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 91.0 | 101.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 91.0 | 101.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 91.0 | 101.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 101.0 | 111.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 101.0 | 111.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 184 | 45000ms | 57000ms | 59700ms |
| 111.0 | 121.0 | app1 | ok | 26 | 45000ms | 57000ms | 59700ms |
| 111.0 | 121.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 166 | 8438ms | 51107ms | 59111ms |
| 121.0 | 131.0 | app1 | ok | 33 | 60000ms | 60000ms | 60000ms |
| 121.0 | 131.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 130 | 8495ms | 22973ms | 29297ms |
| 131.0 | 141.0 | app1 | ok | 31 | 47885ms | 60000ms | 60000ms |
| 131.0 | 141.0 | app2 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | end-users | ok | 101 | 11296ms | 26259ms | 29626ms |
| 141.0 | 151.0 | app1 | ok | 37 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | app2 | ok | 16 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | end-users | ok | 118 | 16118ms | 27224ms | 29722ms |
| 151.0 | 161.0 | app1 | ok | 51 | 60000ms | 60000ms | 60000ms |
| 151.0 | 161.0 | app2 | ok | 26 | 60000ms | 60000ms | 60000ms |
| 151.0 | 161.0 | end-users | ok | 168 | 16341ms | 27268ms | 29727ms |
| 161.0 | 171.0 | app1 | ok | 41 | 60000ms | 60000ms | 60000ms |
| 161.0 | 171.0 | app2 | ok | 20 | 60000ms | 60000ms | 60000ms |
| 161.0 | 171.0 | end-users | ok | 135 | 17019ms | 27404ms | 29740ms |
| 171.0 | 181.0 | app1 | ok | 52 | 60000ms | 60000ms | 60000ms |
| 171.0 | 181.0 | app2 | ok | 26 | 60000ms | 60000ms | 60000ms |
| 171.0 | 181.0 | end-users | ok | 173 | 17185ms | 27437ms | 29744ms |
| 181.0 | 191.0 | app1 | ok | 51 | 45000ms | 57000ms | 59700ms |
| 181.0 | 191.0 | app2 | ok | 25 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | end-users | ok | 157 | 20000ms | 28000ms | 29800ms |
| 191.0 | 201.0 | app1 | ok | 46 | 45000ms | 57000ms | 59700ms |
| 191.0 | 201.0 | app2 | ok | 24 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | end-users | ok | 152 | 16667ms | 27333ms | 29733ms |
| 201.0 | 211.0 | app1 | ok | 48 | 45000ms | 57000ms | 59700ms |
| 201.0 | 211.0 | app2 | ok | 24 | 60000ms | 60000ms | 60000ms |
| 201.0 | 211.0 | end-users | ok | 157 | 19320ms | 27864ms | 29786ms |
| 211.0 | 221.0 | app1 | ok | 43 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | app2 | ok | 21 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | end-users | ok | 139 | 17130ms | 27426ms | 29743ms |
| 221.0 | 231.0 | app1 | ok | 28 | 45000ms | 57000ms | 59700ms |
| 221.0 | 231.0 | app2 | ok | 15 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | end-users | ok | 94 | 17297ms | 27459ms | 29746ms |
| 231.0 | 241.0 | app1 | ok | 50 | 45000ms | 57000ms | 59700ms |
| 231.0 | 241.0 | app2 | ok | 24 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | end-users | ok | 160 | 17097ms | 27419ms | 29742ms |
| 241.0 | 252.0 | app1 | ok | 239 | 33444ms | 54689ms | 59469ms |
| 241.0 | 252.0 | app2 | ok | 249 | 60000ms | 60000ms | 60000ms |
| 241.0 | 252.0 | end-users | ok | 203 | 12500ms | 26500ms | 29650ms |
| 252.0 | 262.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 252.0 | 262.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 252.0 | 262.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 262.0 | 272.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 262.0 | 272.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 262.0 | 272.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 272.0 | 282.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 282.0 | 292.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 282.0 | 292.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 282.0 | 292.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 292.0 | 302.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 292.0 | 302.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 292.0 | 302.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 302.0 | 312.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 302.0 | 312.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 302.0 | 312.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 312.0 | 322.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 312.0 | 322.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 312.0 | 322.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 355.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 355.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 355.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1505520 | 74587 | 1580107.0 | 0.0% | 1600592.0 | 1654694.0 | -3.3% | True |
| app2 | 1025820 | 50922 | 1076742.0 | 0.0% | 1064192.0 | 1127664.0 | -5.6% | True |
| end-users | 3744120 | 186370 | 3930490.0 | 0.0% | 4055984.0 | 4116860.0 | -1.5% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1226 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 834 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3049 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5109). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5109 | 0.054ms | 0.276ms | (0, 0.1]ms | (0.2, 0.5]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 330333 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1224 | 56381ms | 112366ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 834 | 86692ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3044 | 17724ms | 48232ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5102 | 20108ms | 112248ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (36 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 792ms | 1442ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 763ms | 1435ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 764ms | 1479ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 4158ms | 7080ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 4444ms | 7500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 5038ms | 8317ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 15707ms | 19571ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 16875ms | 19688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 9550ms | 14295ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 41.0 | app1 | ok | 18250ms | 27833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 41.0 | app2 | ok | 24891ms | 29489ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 41.0 | end-users | ok | 24929ms | 29493ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | end-users | ok | 25894ms | 40056ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app1 | ok | 38542ms | 53850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | end-users | ok | 14362ms | 19883ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | end-users | ok | 16076ms | 19835ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app1 | ok | 68000ms | 114800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app2 | ok | 82500ms | 116250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | end-users | ok | 24750ms | 29475ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 86957ms | 116696ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 52826ms | 81000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 50705ms | 59071ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 19271ms | 56858ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 16644ms | 19664ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 17053ms | 21750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 16706ms | 19671ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 17355ms | 19801ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 16957ms | 19696ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 54231ms | 104000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 16870ms | 19687ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 16737ms | 19674ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 17102ms | 19710ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 17190ms | 19719ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 18094ms | 27396ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 17456ms | 25406ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 252.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 252.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 252.0 | end-users | ok | 17962ms | 26891ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | app1 | ok | 57000ms | 112000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | end-users | ok | 19018ms | 28694ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | app1 | ok | 73235ms | 115324ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | app2 | ok | 100000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | end-users | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 272.0 | 282.0 | app1 | ok | 55042ms | 108150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 272.0 | 282.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 272.0 | 282.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 282.0 | 292.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 282.0 | 292.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 282.0 | 292.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 292.0 | 302.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 292.0 | 302.0 | app2 | ok | 87692ms | 116769ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 292.0 | 302.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 302.0 | 312.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 302.0 | 312.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 302.0 | 312.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 355.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 355.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 355.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
