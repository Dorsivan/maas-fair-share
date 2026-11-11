# Fairness benchmark: full-contention-2x-discriminating (uni226-98-1-1-equal-load-priority-v2)

**Verdict: FAIL** (threshold: 10 points)
**Secondary (priority) verdict: PRIORITY-OK** -- see "Per-tenant TTFT / ITL and the priority verdict (UNI-226)" below for detail.
Worker-share vs. weight-share gap (UNI-225): 64.7 points

- app1 deviated -36.2 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-68597964f-4chmd` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-10T23:13:10Z` |
| Run end | `2026-11-10T23:21:23Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 98.0 | 256 | 3086 | 000=6, 200=3059, 500=20, 503=1 | 15.6 | 41.9 | 4005920.0 | 98.0% | 33.3% | -64.7 | 61.8% | -36.2 | 60.2% | -37.8 | 28.9s | 0.0% | 3062.0 |
| app2 | 1.0 | 256 | 1013 | 000=1, 200=993, 500=19 | 64.6 | 114.7 | 1225778.0 | 1.0% | 33.3% | 32.3 | 18.9% | 17.9 | 19.8% | 18.8 | 32.9s | 0.0% | 994.0 |
| end-users | 1.0 | 256 | 1023 | 000=1, 200=1002, 500=20 | 63.8 | 115.0 | 1246198.0 | 1.0% | 33.3% | 32.3 | 19.2% | 18.2 | 20.0% | 19.0 | 32.9s | 0.0% | 1001.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 8142.0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.0s | 0.0% | 6.0 |

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
| 0.0 | 231.0 | 231.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (50 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 98.0% | 0.0% | -98.0 |
| 0.0 | 10.0 | app2 | True | 0.0 | 1.0% | 0.0% | -1.0 |
| 0.0 | 10.0 | end-users | True | 0.0 | 1.0% | 0.0% | -1.0 |
| 10.0 | 20.0 | app1 | True | 24288.0 | 98.0% | 64.3% | -33.7 |
| 10.0 | 20.0 | app2 | True | 2712.0 | 1.0% | 7.2% | 6.2 |
| 10.0 | 20.0 | end-users | True | 10784.0 | 1.0% | 28.5% | 27.5 |
| 20.0 | 30.0 | app1 | True | 120216.0 | 98.0% | 40.6% | -57.4 |
| 20.0 | 30.0 | app2 | True | 82368.0 | 1.0% | 27.8% | 26.8 |
| 20.0 | 30.0 | end-users | True | 93268.0 | 1.0% | 31.5% | 30.5 |
| 30.0 | 41.0 | app1 | True | 98684.0 | 98.0% | 40.8% | -57.2 |
| 30.0 | 41.0 | app2 | True | 70240.0 | 1.0% | 29.0% | 28.0 |
| 30.0 | 41.0 | end-users | True | 73102.0 | 1.0% | 30.2% | 29.2 |
| 41.0 | 51.0 | app1 | True | 52630.0 | 98.0% | 21.5% | -76.5 |
| 41.0 | 51.0 | app2 | True | 95936.0 | 1.0% | 39.2% | 38.2 |
| 41.0 | 51.0 | end-users | True | 96050.0 | 1.0% | 39.3% | 38.3 |
| 51.0 | 61.0 | app1 | True | 264618.0 | 98.0% | 88.3% | -9.7 |
| 51.0 | 61.0 | app2 | True | 17620.0 | 1.0% | 5.9% | 4.9 |
| 51.0 | 61.0 | end-users | True | 17476.0 | 1.0% | 5.8% | 4.8 |
| 61.0 | 71.0 | app1 | True | 228266.0 | 98.0% | 74.4% | -23.6 |
| 61.0 | 71.0 | app2 | True | 39206.0 | 1.0% | 12.8% | 11.8 |
| 61.0 | 71.0 | end-users | True | 39192.0 | 1.0% | 12.8% | 11.8 |
| 71.0 | 81.0 | app1 | True | 125790.0 | 98.0% | 52.8% | -45.2 |
| 71.0 | 81.0 | app2 | True | 55540.0 | 1.0% | 23.3% | 22.3 |
| 71.0 | 81.0 | end-users | True | 56746.0 | 1.0% | 23.8% | 22.8 |
| 81.0 | 91.0 | app1 | True | 249938.0 | 98.0% | 96.9% | -1.1 |
| 81.0 | 91.0 | app2 | True | 4044.0 | 1.0% | 1.6% | 0.6 |
| 81.0 | 91.0 | end-users | True | 4054.0 | 1.0% | 1.6% | 0.6 |
| 91.0 | 101.0 | app1 | True | 237516.0 | 98.0% | 98.3% | 0.3 |
| 91.0 | 101.0 | app2 | True | 2714.0 | 1.0% | 1.1% | 0.1 |
| 91.0 | 101.0 | end-users | True | 1358.0 | 1.0% | 0.6% | -0.4 |
| 101.0 | 111.0 | app1 | True | 249840.0 | 98.0% | 97.9% | -0.1 |
| 101.0 | 111.0 | app2 | True | 2710.0 | 1.0% | 1.1% | 0.1 |
| 101.0 | 111.0 | end-users | True | 2716.0 | 1.0% | 1.1% | 0.1 |
| 111.0 | 121.0 | app1 | True | 197396.0 | 98.0% | 97.3% | -0.7 |
| 111.0 | 121.0 | app2 | True | 2690.0 | 1.0% | 1.3% | 0.3 |
| 111.0 | 121.0 | end-users | True | 2716.0 | 1.0% | 1.3% | 0.3 |
| 121.0 | 131.0 | app1 | True | 62260.0 | 98.0% | 40.7% | -57.3 |
| 121.0 | 131.0 | app2 | True | 43266.0 | 1.0% | 28.3% | 27.3 |
| 121.0 | 131.0 | end-users | True | 47370.0 | 1.0% | 31.0% | 30.0 |
| 131.0 | 141.0 | app1 | True | 0.0 | 98.0% | 0.0% | -98.0 |
| 131.0 | 141.0 | app2 | True | 98700.0 | 1.0% | 52.1% | 51.1 |
| 131.0 | 141.0 | end-users | True | 90640.0 | 1.0% | 47.9% | 46.9 |
| 141.0 | 151.0 | app1 | True | 32466.0 | 98.0% | 11.9% | -86.1 |
| 141.0 | 151.0 | app2 | True | 117348.0 | 1.0% | 43.0% | 42.0 |
| 141.0 | 151.0 | end-users | True | 122856.0 | 1.0% | 45.1% | 44.1 |
| 151.0 | 161.0 | app1 | True | 222768.0 | 98.0% | 81.3% | -16.7 |
| 151.0 | 161.0 | app2 | True | 25636.0 | 1.0% | 9.4% | 8.4 |
| 151.0 | 161.0 | end-users | True | 25650.0 | 1.0% | 9.4% | 8.4 |
| 161.0 | 171.0 | app1 | True | 237710.0 | 98.0% | 97.2% | -0.8 |
| 161.0 | 171.0 | app2 | True | 2708.0 | 1.0% | 1.1% | 0.1 |
| 161.0 | 171.0 | end-users | True | 4074.0 | 1.0% | 1.7% | 0.7 |
| 171.0 | 181.0 | app1 | True | 236180.0 | 98.0% | 98.3% | 0.3 |
| 171.0 | 181.0 | app2 | True | 2700.0 | 1.0% | 1.1% | 0.1 |
| 171.0 | 181.0 | end-users | True | 1358.0 | 1.0% | 0.6% | -0.4 |
| 181.0 | 191.0 | app1 | True | 237882.0 | 98.0% | 97.8% | -0.2 |
| 181.0 | 191.0 | app2 | True | 2704.0 | 1.0% | 1.1% | 0.1 |
| 181.0 | 191.0 | end-users | True | 2692.0 | 1.0% | 1.1% | 0.1 |
| 191.0 | 201.0 | app1 | True | 236072.0 | 98.0% | 97.8% | -0.2 |
| 191.0 | 201.0 | app2 | True | 2706.0 | 1.0% | 1.1% | 0.1 |
| 191.0 | 201.0 | end-users | True | 2716.0 | 1.0% | 1.1% | 0.1 |
| 201.0 | 211.0 | app1 | True | 105232.0 | 98.0% | 42.6% | -55.4 |
| 201.0 | 211.0 | app2 | True | 71544.0 | 1.0% | 29.0% | 28.0 |
| 201.0 | 211.0 | end-users | True | 70216.0 | 1.0% | 28.4% | 27.4 |
| 211.0 | 221.0 | app1 | True | 12132.0 | 98.0% | 5.9% | -92.1 |
| 211.0 | 221.0 | app2 | True | 98688.0 | 1.0% | 47.7% | 46.7 |
| 211.0 | 221.0 | end-users | True | 96052.0 | 1.0% | 46.4% | 45.4 |
| 221.0 | 231.0 | app1 | True | 202370.0 | 98.0% | 74.2% | -23.8 |
| 221.0 | 231.0 | app2 | True | 33852.0 | 1.0% | 12.4% | 11.4 |
| 221.0 | 231.0 | end-users | True | 36520.0 | 1.0% | 13.4% | 12.4 |
| 231.0 | 241.0 | app1 | True | 228326.0 | 98.0% | 96.0% | -2.0 |
| 231.0 | 241.0 | app2 | True | 5432.0 | 1.0% | 2.3% | 1.3 |
| 231.0 | 241.0 | end-users | True | 4066.0 | 1.0% | 1.7% | 0.7 |
| 241.0 | 251.0 | app1 | False | 237808.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 1358.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 2716.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 105532.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 67620.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 67470.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 90556.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 94616.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 133718.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | False | 125656.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | 51462.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | False | 54068.0 | n/a | n/a | n/a |
| 291.0 | 302.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 302.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 302.0 | end-users | False | 0.0 | n/a | n/a | n/a |
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
| 392.0 | 402.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | end-users | False | 0.0 | n/a | n/a | n/a |
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
| 492.0 | 493.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 492.0 | 493.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 492.0 | 493.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 20 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 27 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 27 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 123 | 0ms | 1529ms | 2403ms |
| 10.0 | 20.0 | app2 | ok | 121 | 0ms | 1521ms | 2481ms |
| 10.0 | 20.0 | end-users | ok | 117 | 4ms | 1802ms | 2489ms |
| 20.0 | 30.0 | app1 | ok | 66 | 2380ms | 4468ms | 4947ms |
| 20.0 | 30.0 | app2 | ok | 35 | 3380ms | 4676ms | 4968ms |
| 20.0 | 30.0 | end-users | ok | 44 | 3036ms | 4607ms | 4961ms |
| 30.0 | 41.0 | app1 | ok | 66 | 3304ms | 7643ms | 9764ms |
| 30.0 | 41.0 | app2 | ok | 58 | 7500ms | 9500ms | 9950ms |
| 30.0 | 41.0 | end-users | ok | 61 | 6453ms | 9291ms | 9929ms |
| 41.0 | 51.0 | app1 | ok | 109 | 6250ms | 9364ms | 19100ms |
| 41.0 | 51.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 41.0 | 51.0 | end-users | ok | 34 | 18667ms | 27733ms | 29773ms |
| 51.0 | 61.0 | app1 | ok | 348 | 5925ms | 9405ms | 23673ms |
| 51.0 | 61.0 | app2 | ok | 41 | 20000ms | 28000ms | 29800ms |
| 51.0 | 61.0 | end-users | ok | 38 | 20000ms | 28000ms | 29800ms |
| 61.0 | 71.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 61.0 | 71.0 | app2 | ok | 21 | 45000ms | 57000ms | 59700ms |
| 61.0 | 71.0 | end-users | ok | 23 | 45000ms | 57000ms | 59700ms |
| 71.0 | 81.0 | app1 | ok | 258 | 11029ms | 26206ms | 29621ms |
| 71.0 | 81.0 | app2 | ok | 24 | 45000ms | 57000ms | 59700ms |
| 71.0 | 81.0 | end-users | ok | 23 | 45000ms | 57000ms | 59700ms |
| 81.0 | 91.0 | app1 | ok | 173 | 6016ms | 9819ms | 27529ms |
| 81.0 | 91.0 | app2 | ok | 2 | 45000ms | 57000ms | 59700ms |
| 81.0 | 91.0 | end-users | ok | 3 | 45000ms | 57000ms | 59700ms |
| 91.0 | 101.0 | app1 | ok | 164 | 6682ms | 9748ms | 27018ms |
| 91.0 | 101.0 | app2 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 91.0 | 101.0 | end-users | ok | 2 | 45000ms | 57000ms | 59700ms |
| 101.0 | 111.0 | app1 | ok | 183 | 5467ms | 9489ms | 25933ms |
| 101.0 | 111.0 | app2 | ok | 110 | 60000ms | 60000ms | 60000ms |
| 101.0 | 111.0 | end-users | ok | 111 | 60000ms | 60000ms | 60000ms |
| 111.0 | 121.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 111.0 | 121.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 111.0 | 121.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 121.0 | 131.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 121.0 | 131.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 121.0 | 131.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 131.0 | 141.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 81 | 60000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | end-users | ok | 80 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | app1 | ok | 91 | 45000ms | 57000ms | 59700ms |
| 141.0 | 151.0 | app2 | ok | 14 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | end-users | ok | 13 | 60000ms | 60000ms | 60000ms |
| 151.0 | 161.0 | app1 | ok | 192 | 40800ms | 56160ms | 59616ms |
| 151.0 | 161.0 | app2 | ok | 9 | 60000ms | 60000ms | 60000ms |
| 151.0 | 161.0 | end-users | ok | 10 | 60000ms | 60000ms | 60000ms |
| 161.0 | 171.0 | app1 | ok | 167 | 6829ms | 9921ms | 27773ms |
| 161.0 | 171.0 | app2 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 161.0 | 171.0 | end-users | ok | 2 | 60000ms | 60000ms | 60000ms |
| 171.0 | 181.0 | app1 | ok | 158 | 5957ms | 9319ms | 19467ms |
| 171.0 | 181.0 | app2 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 171.0 | 181.0 | end-users | ok | 2 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | app1 | ok | 178 | 5500ms | 9456ms | 25550ms |
| 181.0 | 191.0 | app2 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | end-users | ok | 2 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | app1 | ok | 183 | 5920ms | 9373ms | 22680ms |
| 191.0 | 201.0 | app2 | ok | 14 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | end-users | ok | 13 | 60000ms | 60000ms | 60000ms |
| 201.0 | 211.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 109 | 60000ms | 60000ms | 60000ms |
| 201.0 | 211.0 | end-users | ok | 110 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | app1 | ok | 115 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app2 | ok | 21 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | end-users | ok | 20 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | app1 | ok | 163 | 18102ms | 27620ms | 29762ms |
| 221.0 | 231.0 | app2 | ok | 10 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | end-users | ok | 11 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | app1 | ok | 122 | 5000ms | 9000ms | 9900ms |
| 231.0 | 241.0 | app2 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | end-users | ok | 1 | 60000ms | 60000ms | 60000ms |
| 241.0 | 251.0 | app1 | ok | 183 | 6185ms | 9341ms | 17800ms |
| 241.0 | 251.0 | app2 | ok | 17 | 60000ms | 60000ms | 60000ms |
| 241.0 | 251.0 | end-users | ok | 19 | 60000ms | 60000ms | 60000ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 112 | 60000ms | 60000ms | 60000ms |
| 251.0 | 261.0 | end-users | ok | 110 | 60000ms | 60000ms | 60000ms |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | ok | 86 | 45542ms | 57976ms | 60000ms |
| 261.0 | 271.0 | end-users | ok | 86 | 46125ms | 59025ms | 60000ms |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | ok | 40 | 45000ms | 57000ms | 59700ms |
| 271.0 | 281.0 | end-users | ok | 39 | 45000ms | 57000ms | 59700ms |
| 281.0 | 291.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 302.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 302.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 302.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 392.0 | 402.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 492.0 | 493.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 493.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 493.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens +4525.8%
- app2 exceeded the 10% ledger tolerance: raw tokens +4640.2%
- end-users exceeded the 10% ledger tolerance: raw tokens +4572.6%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 3762570 | 186838 | 182693022.0 | 4525.8% | 4005920.0 | 4136246.0 | -3.2% | False |
| app2 | 1221390 | 60793 | 60777970.0 | 4640.2% | 1225778.0 | 1342976.0 | -8.7% | False |
| end-users | 1232460 | 61219 | 60448038.0 | 4572.6% | 1246198.0 | 1354898.0 | -8.0% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 3086 | 0 | 1 | 1 | 0.03% | 98.0% | 100.0% | 1.02 |
| app2 | 1013 | 0 | 0 | 0 (never shed) | 0.00% | 1.0% | 0.0% | 0.00 |
| end-users | 1023 | 0 | 0 | 0 (never shed) | 0.00% | 1.0% | 0.0% | 0.00 |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5063). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5063 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 472095 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 3055 | 14459ms | 39258ms | ok | 141791 | 15ms | 36ms |
| app2 | ok | 993 | 70196ms | 117902ms | ok | 47188 | 15ms | 35ms |
| end-users | ok | 1000 | 69840ms | 117968ms | ok | 46917 | 15ms | 36ms |
| **pool (all groups)** | ok | 5054 | 17189ms | 109758ms | ok | 236181 | 15ms | 36ms |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: PRIORITY-OK** -- the share verdict above is FAIL, so this is the board's second, independent success criterion (2026-11-10): did the policy nonetheless order tenants by weight? Top-weighted group: `app1` (TTFT p50 14459ms, p95 39258ms, strictly lowest among distinctly-weighted groups: p50=True/p95=True; no rank inversion among any distinctly-weighted pair: True -- this, not raw rank correlation, is what gates the verdict, since a genuine weight tie (e.g. 98/1/1's app2==end-users) makes exact correlation 1.0 unreachable by construction even when ordering is otherwise perfect). Rank correlation 0.87 (1.00 = exact agreement, informational only) shown for reference. Separation from the next distinctly-weighted group: 55381ms against a noise floor of not given (separation check skipped).

**Windowed TTFT/ITL** (50 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 64ms | 460ms | ok | 14ms | 34ms |
| 0.0 | 10.0 | app2 | ok | 82ms | 543ms | ok | 15ms | 36ms |
| 0.0 | 10.0 | end-users | ok | 75ms | 610ms | ok | 14ms | 35ms |
| 10.0 | 20.0 | app1 | ok | 2023ms | 2986ms | ok | 16ms | 44ms |
| 10.0 | 20.0 | app2 | ok | 1679ms | 3490ms | ok | 16ms | 44ms |
| 10.0 | 20.0 | end-users | ok | 1929ms | 3633ms | ok | 16ms | 43ms |
| 20.0 | 30.0 | app1 | ok | 5423ms | 7821ms | ok | 15ms | 38ms |
| 20.0 | 30.0 | app2 | ok | 6600ms | 9531ms | ok | 15ms | 38ms |
| 20.0 | 30.0 | end-users | ok | 6571ms | 9792ms | ok | 15ms | 39ms |
| 30.0 | 41.0 | app1 | ok | 8860ms | 10437ms | ok | 14ms | 33ms |
| 30.0 | 41.0 | app2 | ok | 12024ms | 14810ms | ok | 16ms | 39ms |
| 30.0 | 41.0 | end-users | ok | 11029ms | 14603ms | ok | 15ms | 39ms |
| 41.0 | 51.0 | app1 | ok | 15568ms | 19557ms | ok | 14ms | 30ms |
| 41.0 | 51.0 | app2 | ok | 18008ms | 27042ms | ok | 15ms | 37ms |
| 41.0 | 51.0 | end-users | ok | 16056ms | 19606ms | ok | 15ms | 38ms |
| 51.0 | 61.0 | app1 | ok | 13451ms | 19222ms | ok | 16ms | 38ms |
| 51.0 | 61.0 | app2 | ok | 24091ms | 29409ms | ok | 17ms | 48ms |
| 51.0 | 61.0 | end-users | ok | 18611ms | 28375ms | ok | 17ms | 39ms |
| 61.0 | 71.0 | app1 | ok | 11782ms | 17183ms | ok | 16ms | 37ms |
| 61.0 | 71.0 | app2 | ok | 37232ms | 44223ms | ok | 16ms | 37ms |
| 61.0 | 71.0 | end-users | ok | 36944ms | 44194ms | ok | 16ms | 37ms |
| 71.0 | 81.0 | app1 | ok | 17165ms | 19716ms | ok | 14ms | 34ms |
| 71.0 | 81.0 | app2 | ok | 37500ms | 44250ms | ok | 14ms | 34ms |
| 71.0 | 81.0 | end-users | ok | 37500ms | 44250ms | ok | 15ms | 35ms |
| 81.0 | 91.0 | app1 | ok | 17907ms | 27431ms | ok | 14ms | 35ms |
| 81.0 | 91.0 | app2 | ok | 48750ms | 58875ms | ok | 15ms | 36ms |
| 81.0 | 91.0 | end-users | ok | 48750ms | 58875ms | ok | 14ms | 34ms |
| 91.0 | 101.0 | app1 | ok | 13577ms | 19170ms | ok | 14ms | 34ms |
| 91.0 | 101.0 | app2 | ok | 52500ms | 59250ms | ok | 13ms | 26ms |
| 91.0 | 101.0 | end-users | ok | 52500ms | 59250ms | ok | 14ms | 36ms |
| 101.0 | 111.0 | app1 | ok | 13611ms | 19288ms | ok | 15ms | 38ms |
| 101.0 | 111.0 | app2 | ok | 90000ms | 117000ms | ok | 14ms | 38ms |
| 101.0 | 111.0 | end-users | ok | 60000ms | 114000ms | ok | 14ms | 26ms |
| 111.0 | 121.0 | app1 | ok | 14101ms | 19360ms | ok | 15ms | 35ms |
| 111.0 | 121.0 | app2 | ok | 90000ms | 117000ms | ok | 14ms | 33ms |
| 111.0 | 121.0 | end-users | ok | 90000ms | 117000ms | ok | 16ms | 47ms |
| 121.0 | 131.0 | app1 | ok | 17500ms | 19750ms | ok | 14ms | 19ms |
| 121.0 | 131.0 | app2 | ok | 90000ms | 117000ms | ok | 14ms | 20ms |
| 121.0 | 131.0 | end-users | ok | 90000ms | 117000ms | ok | 14ms | 20ms |
| 131.0 | 141.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 90000ms | 117000ms | ok | 14ms | 27ms |
| 131.0 | 141.0 | end-users | ok | 90000ms | 117000ms | ok | 14ms | 29ms |
| 141.0 | 151.0 | app1 | ok | 37500ms | 44250ms | ok | 15ms | 38ms |
| 141.0 | 151.0 | app2 | ok | 90000ms | 117000ms | ok | 14ms | 36ms |
| 141.0 | 151.0 | end-users | ok | 90000ms | 117000ms | ok | 15ms | 36ms |
| 151.0 | 161.0 | app1 | ok | 37500ms | 44250ms | ok | 15ms | 37ms |
| 151.0 | 161.0 | app2 | ok | 90000ms | 117000ms | ok | 15ms | 36ms |
| 151.0 | 161.0 | end-users | ok | 90000ms | 117000ms | ok | 15ms | 37ms |
| 161.0 | 171.0 | app1 | ok | 16167ms | 42905ms | ok | 15ms | 36ms |
| 161.0 | 171.0 | app2 | ok | 90000ms | 117000ms | ok | 16ms | 38ms |
| 161.0 | 171.0 | end-users | ok | 90000ms | 117000ms | ok | 14ms | 26ms |
| 171.0 | 181.0 | app1 | ok | 13460ms | 19232ms | ok | 14ms | 34ms |
| 171.0 | 181.0 | app2 | ok | 90000ms | 117000ms | ok | 14ms | 35ms |
| 171.0 | 181.0 | end-users | ok | 90000ms | 117000ms | ok | 14ms | 29ms |
| 181.0 | 191.0 | app1 | ok | 13014ms | 18533ms | ok | 14ms | 33ms |
| 181.0 | 191.0 | app2 | ok | 90000ms | 117000ms | ok | 13ms | 27ms |
| 181.0 | 191.0 | end-users | ok | 90000ms | 117000ms | ok | 15ms | 37ms |
| 191.0 | 201.0 | app1 | ok | 13393ms | 19069ms | ok | 14ms | 36ms |
| 191.0 | 201.0 | app2 | ok | 120000ms | 120000ms | ok | 13ms | 20ms |
| 191.0 | 201.0 | end-users | ok | 120000ms | 120000ms | ok | 13ms | 32ms |
| 201.0 | 211.0 | app1 | ok | 16098ms | 24429ms | ok | 15ms | 38ms |
| 201.0 | 211.0 | app2 | ok | 120000ms | 120000ms | ok | 15ms | 36ms |
| 201.0 | 211.0 | end-users | ok | 120000ms | 120000ms | ok | 15ms | 36ms |
| 211.0 | 221.0 | app1 | ok | 25000ms | 29500ms | ok | 16ms | 38ms |
| 211.0 | 221.0 | app2 | ok | 90000ms | 117000ms | ok | 14ms | 31ms |
| 211.0 | 221.0 | end-users | ok | 90000ms | 117000ms | ok | 14ms | 30ms |
| 221.0 | 231.0 | app1 | ok | 33971ms | 43897ms | ok | 15ms | 37ms |
| 221.0 | 231.0 | app2 | ok | 90000ms | 117000ms | ok | 15ms | 37ms |
| 221.0 | 231.0 | end-users | ok | 90000ms | 117000ms | ok | 15ms | 36ms |
| 231.0 | 241.0 | app1 | ok | 21413ms | 42183ms | ok | 15ms | 36ms |
| 231.0 | 241.0 | app2 | ok | 90000ms | 117000ms | ok | 14ms | 34ms |
| 231.0 | 241.0 | end-users | ok | 90000ms | 117000ms | ok | 15ms | 37ms |
| 241.0 | 251.0 | app1 | ok | 12881ms | 18167ms | ok | 14ms | 31ms |
| 241.0 | 251.0 | app2 | ok | 90000ms | 117000ms | ok | 15ms | 29ms |
| 241.0 | 251.0 | end-users | ok | 90000ms | 117000ms | ok | 14ms | 25ms |
| 251.0 | 261.0 | app1 | ok | 17365ms | 19736ms | ok | 14ms | 29ms |
| 251.0 | 261.0 | app2 | ok | 90000ms | 117000ms | ok | 15ms | 36ms |
| 251.0 | 261.0 | end-users | ok | 90000ms | 117000ms | ok | 15ms | 36ms |
| 261.0 | 271.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 261.0 | 271.0 | app2 | ok | 89545ms | 116955ms | ok | 14ms | 28ms |
| 261.0 | 271.0 | end-users | ok | 90000ms | 117000ms | ok | 14ms | 30ms |
| 271.0 | 281.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 271.0 | 281.0 | app2 | ok | 83333ms | 116333ms | ok | 14ms | 31ms |
| 271.0 | 281.0 | end-users | ok | 84231ms | 116423ms | ok | 14ms | 32ms |
| 281.0 | 291.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 281.0 | 291.0 | app2 | ok | 57955ms | 112875ms | ok | 14ms | 33ms |
| 281.0 | 291.0 | end-users | ok | 57500ms | 112500ms | ok | 14ms | 34ms |
| 291.0 | 302.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 291.0 | 302.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 291.0 | 302.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 302.0 | 312.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 302.0 | 312.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 302.0 | 312.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 312.0 | 322.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 312.0 | 322.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 312.0 | 322.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 322.0 | 332.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 322.0 | 332.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 322.0 | 332.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 332.0 | 342.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 332.0 | 342.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 332.0 | 342.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 342.0 | 352.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 342.0 | 352.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 342.0 | 352.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 352.0 | 362.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 352.0 | 362.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 352.0 | 362.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 362.0 | 372.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 362.0 | 372.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 362.0 | 372.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 372.0 | 382.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 372.0 | 382.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 372.0 | 382.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 382.0 | 392.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 382.0 | 392.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 382.0 | 392.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 392.0 | 402.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 392.0 | 402.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 392.0 | 402.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 402.0 | 412.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 402.0 | 412.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 402.0 | 412.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 412.0 | 422.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 412.0 | 422.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 412.0 | 422.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 422.0 | 432.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 422.0 | 432.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 422.0 | 432.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 432.0 | 442.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 432.0 | 442.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 432.0 | 442.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 442.0 | 452.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 442.0 | 452.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 442.0 | 452.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 452.0 | 462.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 452.0 | 462.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 452.0 | 462.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 462.0 | 472.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 462.0 | 472.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 462.0 | 472.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 472.0 | 482.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 472.0 | 482.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 472.0 | 482.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 482.0 | 492.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 482.0 | 492.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 482.0 | 492.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 492.0 | 493.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 492.0 | 493.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 492.0 | 493.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
