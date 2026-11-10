# Fairness benchmark: full-contention-discriminating (uni-225-full-contention-discriminating)

**Verdict: FAIL** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 35.1 points

- end-users deviated -21.4 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-85575669d6-vzbm8` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-10T15:16:23Z` |
| Run end | `2026-11-10T15:21:59Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 128 | 1695 | 000=1, 200=1677, 500=17 | 17.8 | 28.0 | 2218784.0 | 21.1% | 33.3% | 12.3 | 33.4% | 12.4 | 33.0% | 11.9 | 49.9s | 98.9% | 1678.0 |
| app2 | 10.0 | 128 | 1073 | 200=1059, 500=14 | 33.4 | 41.7 | 1299724.0 | 10.5% | 33.3% | 22.8 | 19.6% | 9.0 | 20.9% | 10.4 | 49.9s | 98.9% | 1059.0 |
| end-users | 65.0 | 128 | 2369 | 000=3, 200=2353, 500=13 | 11.3 | 24.1 | 3121868.0 | 68.4% | 33.3% | -35.1 | 47.0% | -21.4 | 46.1% | -22.3 | 48.4s | 98.9% | 2356.0 |
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
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (34 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 10.0 | 20.0 | app1 | True | 104088.0 | 21.1% | 40.3% | 19.3 |
| 10.0 | 20.0 | app2 | True | 49952.0 | 10.5% | 19.3% | 8.8 |
| 10.0 | 20.0 | end-users | True | 104180.0 | 68.4% | 40.3% | -28.1 |
| 20.0 | 30.0 | app1 | True | 81114.0 | 21.1% | 27.0% | 6.0 |
| 20.0 | 30.0 | app2 | True | 37972.0 | 10.5% | 12.6% | 2.1 |
| 20.0 | 30.0 | end-users | True | 181226.0 | 68.4% | 60.3% | -8.1 |
| 30.0 | 40.0 | app1 | True | 64872.0 | 21.1% | 28.1% | 7.0 |
| 30.0 | 40.0 | app2 | True | 37918.0 | 10.5% | 16.4% | 5.9 |
| 30.0 | 40.0 | end-users | True | 128352.0 | 68.4% | 55.5% | -12.9 |
| 40.0 | 50.0 | app1 | True | 82246.0 | 21.1% | 51.7% | 30.6 |
| 40.0 | 50.0 | app2 | True | 37802.0 | 10.5% | 23.7% | 13.2 |
| 40.0 | 50.0 | end-users | True | 39166.0 | 68.4% | 24.6% | -43.8 |
| 50.0 | 60.0 | app1 | True | 35138.0 | 21.1% | 14.6% | -6.5 |
| 50.0 | 60.0 | app2 | True | 173236.0 | 10.5% | 72.0% | 61.4 |
| 50.0 | 60.0 | end-users | True | 32388.0 | 68.4% | 13.5% | -55.0 |
| 60.0 | 70.0 | app1 | True | 47396.0 | 21.1% | 19.5% | -1.6 |
| 60.0 | 70.0 | app2 | True | 43176.0 | 10.5% | 17.7% | 7.2 |
| 60.0 | 70.0 | end-users | True | 152842.0 | 68.4% | 62.8% | -5.6 |
| 70.0 | 80.0 | app1 | True | 128620.0 | 21.1% | 53.7% | 32.6 |
| 70.0 | 80.0 | app2 | True | 66250.0 | 10.5% | 27.7% | 17.1 |
| 70.0 | 80.0 | end-users | True | 44658.0 | 68.4% | 18.6% | -49.8 |
| 80.0 | 90.0 | app1 | True | 77054.0 | 21.1% | 25.2% | 4.2 |
| 80.0 | 90.0 | app2 | True | 40552.0 | 10.5% | 13.3% | 2.8 |
| 80.0 | 90.0 | end-users | True | 187808.0 | 68.4% | 61.5% | -6.9 |
| 90.0 | 100.0 | app1 | True | 78466.0 | 21.1% | 25.7% | 4.6 |
| 90.0 | 100.0 | app2 | True | 39230.0 | 10.5% | 12.8% | 2.3 |
| 90.0 | 100.0 | end-users | True | 187992.0 | 68.4% | 61.5% | -6.9 |
| 100.0 | 110.0 | app1 | True | 118890.0 | 21.1% | 39.4% | 18.4 |
| 100.0 | 110.0 | app2 | True | 58128.0 | 10.5% | 19.3% | 8.8 |
| 100.0 | 110.0 | end-users | True | 124462.0 | 68.4% | 41.3% | -27.1 |
| 110.0 | 120.0 | app1 | True | 59538.0 | 21.1% | 21.7% | 0.6 |
| 110.0 | 120.0 | app2 | True | 29808.0 | 10.5% | 10.9% | 0.3 |
| 110.0 | 120.0 | end-users | True | 185280.0 | 68.4% | 67.5% | -1.0 |
| 120.0 | 130.0 | app1 | True | 120336.0 | 21.1% | 41.6% | 20.5 |
| 120.0 | 130.0 | app2 | True | 59514.0 | 10.5% | 20.6% | 10.0 |
| 120.0 | 130.0 | end-users | True | 109568.0 | 68.4% | 37.9% | -30.6 |
| 130.0 | 140.0 | app1 | True | 100092.0 | 21.1% | 33.0% | 12.0 |
| 130.0 | 140.0 | app2 | True | 50044.0 | 10.5% | 16.5% | 6.0 |
| 130.0 | 140.0 | end-users | True | 152748.0 | 68.4% | 50.4% | -18.0 |
| 140.0 | 151.0 | app1 | True | 63618.0 | 21.1% | 25.3% | 4.2 |
| 140.0 | 151.0 | app2 | True | 32466.0 | 10.5% | 12.9% | 2.4 |
| 140.0 | 151.0 | end-users | True | 155434.0 | 68.4% | 61.8% | -6.6 |
| 151.0 | 161.0 | app1 | True | 121576.0 | 21.1% | 48.4% | 27.3 |
| 151.0 | 161.0 | app2 | True | 59532.0 | 10.5% | 23.7% | 13.2 |
| 151.0 | 161.0 | end-users | True | 70200.0 | 68.4% | 27.9% | -40.5 |
| 161.0 | 171.0 | app1 | True | 59468.0 | 21.1% | 24.4% | 3.4 |
| 161.0 | 171.0 | app2 | True | 32444.0 | 10.5% | 13.3% | 2.8 |
| 161.0 | 171.0 | end-users | True | 151438.0 | 68.4% | 62.2% | -6.2 |
| 171.0 | 181.0 | app1 | True | 156558.0 | 21.1% | 57.1% | 36.0 |
| 171.0 | 181.0 | app2 | True | 77170.0 | 10.5% | 28.1% | 17.6 |
| 171.0 | 181.0 | end-users | True | 40612.0 | 68.4% | 14.8% | -53.6 |
| 181.0 | 191.0 | app1 | True | 64978.0 | 21.1% | 21.4% | 0.3 |
| 181.0 | 191.0 | app2 | True | 33838.0 | 10.5% | 11.1% | 0.6 |
| 181.0 | 191.0 | end-users | True | 205442.0 | 68.4% | 67.5% | -0.9 |
| 191.0 | 201.0 | app1 | True | 52814.0 | 21.1% | 21.8% | 0.8 |
| 191.0 | 201.0 | app2 | True | 29774.0 | 10.5% | 12.3% | 1.8 |
| 191.0 | 201.0 | end-users | True | 159458.0 | 68.4% | 65.9% | -2.5 |
| 201.0 | 211.0 | app1 | True | 144752.0 | 21.1% | 56.6% | 35.6 |
| 201.0 | 211.0 | app2 | True | 67582.0 | 10.5% | 26.4% | 15.9 |
| 201.0 | 211.0 | end-users | True | 43242.0 | 68.4% | 16.9% | -51.5 |
| 211.0 | 221.0 | app1 | True | 70402.0 | 21.1% | 23.1% | 2.1 |
| 211.0 | 221.0 | app2 | True | 36494.0 | 10.5% | 12.0% | 1.5 |
| 211.0 | 221.0 | end-users | True | 197418.0 | 68.4% | 64.9% | -3.5 |
| 221.0 | 231.0 | app1 | True | 63540.0 | 21.1% | 20.4% | -0.6 |
| 221.0 | 231.0 | app2 | True | 32456.0 | 10.5% | 10.4% | -0.1 |
| 221.0 | 231.0 | end-users | True | 215036.0 | 68.4% | 69.1% | 0.7 |
| 231.0 | 241.0 | app1 | True | 140702.0 | 21.1% | 48.8% | 27.8 |
| 231.0 | 241.0 | app2 | True | 69016.0 | 10.5% | 24.0% | 13.4 |
| 231.0 | 241.0 | end-users | True | 78436.0 | 68.4% | 27.2% | -41.2 |
| 241.0 | 251.0 | app1 | False | 102732.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 51310.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 152850.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 79794.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 54060.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 21632.0 | n/a | n/a | n/a |
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
| 331.0 | 336.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 336.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 336.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 46 | 0ms | 40ms | 385ms |
| 0.0 | 10.0 | app2 | ok | 58 | 0ms | 190ms | 471ms |
| 0.0 | 10.0 | end-users | ok | 63 | 0ms | 275ms | 477ms |
| 10.0 | 20.0 | app1 | ok | 100 | 1900ms | 4342ms | 4934ms |
| 10.0 | 20.0 | app2 | ok | 36 | 4375ms | 8615ms | 9862ms |
| 10.0 | 20.0 | end-users | ok | 123 | 1536ms | 3536ms | 4854ms |
| 20.0 | 30.0 | app1 | ok | 79 | 6409ms | 9282ms | 9928ms |
| 20.0 | 30.0 | app2 | ok | 40 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | end-users | ok | 185 | 2346ms | 4449ms | 4945ms |
| 30.0 | 40.0 | app1 | ok | 76 | 5000ms | 9000ms | 9900ms |
| 30.0 | 40.0 | app2 | ok | 103 | 11607ms | 26321ms | 29632ms |
| 30.0 | 40.0 | end-users | ok | 12 | 500ms | 900ms | 990ms |
| 40.0 | 50.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 50.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 25 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app2 | ok | 65 | 8958ms | 25667ms | 29567ms |
| 50.0 | 60.0 | end-users | ok | 80 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app1 | ok | 58 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app2 | ok | 43 | 7500ms | 9500ms | 9950ms |
| 60.0 | 70.0 | end-users | ok | 77 | 12500ms | 26500ms | 29650ms |
| 70.0 | 80.0 | app1 | ok | 104 | 15352ms | 27070ms | 29707ms |
| 70.0 | 80.0 | app2 | ok | 54 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | end-users | ok | 132 | 8554ms | 23714ms | 29371ms |
| 80.0 | 90.0 | app1 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app2 | ok | 16 | 30000ms | 54000ms | 59400ms |
| 80.0 | 90.0 | end-users | ok | 98 | 3281ms | 4812ms | 9020ms |
| 90.0 | 100.0 | app1 | ok | 83 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app2 | ok | 42 | 32609ms | 54522ms | 59452ms |
| 90.0 | 100.0 | end-users | ok | 73 | 2259ms | 4430ms | 4943ms |
| 100.0 | 110.0 | app1 | ok | 56 | 18085ms | 27617ms | 29762ms |
| 100.0 | 110.0 | app2 | ok | 28 | 23333ms | 48000ms | 58800ms |
| 100.0 | 110.0 | end-users | ok | 133 | 7229ms | 9446ms | 9945ms |
| 110.0 | 120.0 | app1 | ok | 53 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app2 | ok | 26 | 45000ms | 57000ms | 59700ms |
| 110.0 | 120.0 | end-users | ok | 121 | 2844ms | 4598ms | 4992ms |
| 120.0 | 130.0 | app1 | ok | 102 | 19485ms | 27897ms | 29790ms |
| 120.0 | 130.0 | app2 | ok | 52 | 38333ms | 55667ms | 59567ms |
| 120.0 | 130.0 | end-users | ok | 148 | 6651ms | 9367ms | 9978ms |
| 130.0 | 140.0 | app1 | ok | 66 | 18621ms | 27724ms | 29772ms |
| 130.0 | 140.0 | app2 | ok | 33 | 45000ms | 57000ms | 59700ms |
| 130.0 | 140.0 | end-users | ok | 82 | 7372ms | 9474ms | 9947ms |
| 140.0 | 151.0 | app1 | ok | 44 | 15806ms | 27161ms | 29716ms |
| 140.0 | 151.0 | app2 | ok | 22 | 34615ms | 54923ms | 59492ms |
| 140.0 | 151.0 | end-users | ok | 72 | 3889ms | 8714ms | 9871ms |
| 151.0 | 161.0 | app1 | ok | 137 | 13690ms | 26738ms | 29674ms |
| 151.0 | 161.0 | app2 | ok | 68 | 25814ms | 51840ms | 59184ms |
| 151.0 | 161.0 | end-users | ok | 140 | 7418ms | 17826ms | 28783ms |
| 161.0 | 171.0 | app1 | ok | 75 | 12955ms | 26591ms | 29659ms |
| 161.0 | 171.0 | app2 | ok | 38 | 29000ms | 53667ms | 59367ms |
| 161.0 | 171.0 | end-users | ok | 45 | 7500ms | 9500ms | 9950ms |
| 171.0 | 181.0 | app1 | ok | 37 | 8304ms | 21778ms | 29178ms |
| 171.0 | 181.0 | app2 | ok | 18 | 22857ms | 46500ms | 58650ms |
| 171.0 | 181.0 | end-users | ok | 74 | 15769ms | 27154ms | 29715ms |
| 181.0 | 191.0 | app1 | ok | 44 | 20000ms | 28000ms | 29800ms |
| 181.0 | 191.0 | app2 | ok | 22 | 36429ms | 55286ms | 59529ms |
| 181.0 | 191.0 | end-users | ok | 133 | 3365ms | 4827ms | 25567ms |
| 191.0 | 201.0 | app1 | ok | 123 | 17449ms | 27490ms | 29749ms |
| 191.0 | 201.0 | app2 | ok | 62 | 30000ms | 54000ms | 59400ms |
| 191.0 | 201.0 | end-users | ok | 102 | 3409ms | 8300ms | 9830ms |
| 201.0 | 211.0 | app1 | ok | 32 | 8810ms | 24182ms | 29418ms |
| 201.0 | 211.0 | app2 | ok | 16 | 45000ms | 57000ms | 59700ms |
| 201.0 | 211.0 | end-users | ok | 68 | 15833ms | 27167ms | 29717ms |
| 211.0 | 221.0 | app1 | ok | 45 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app2 | ok | 22 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | end-users | ok | 130 | 3716ms | 16316ms | 28632ms |
| 221.0 | 231.0 | app1 | ok | 53 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app2 | ok | 28 | 45000ms | 57000ms | 59700ms |
| 221.0 | 231.0 | end-users | ok | 125 | 2668ms | 4534ms | 4953ms |
| 231.0 | 241.0 | app1 | ok | 115 | 9830ms | 25893ms | 29589ms |
| 231.0 | 241.0 | app2 | ok | 56 | 26471ms | 52364ms | 59236ms |
| 231.0 | 241.0 | end-users | ok | 81 | 8616ms | 23520ms | 29352ms |
| 241.0 | 251.0 | app1 | ok | 93 | 8229ms | 21143ms | 29114ms |
| 241.0 | 251.0 | app2 | ok | 57 | 25833ms | 51857ms | 59186ms |
| 241.0 | 251.0 | end-users | ok | 59 | 9417ms | 25462ms | 29546ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 54 | 20000ms | 28000ms | 29800ms |
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
| 331.0 | 336.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 336.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 336.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2062710 | 102380 | 2165090.0 | 0.0% | 2218784.0 | 2267470.0 | -2.1% | True |
| app2 | 1302570 | 64883 | 1367453.0 | 0.0% | 1299724.0 | 1432336.0 | -9.3% | True |
| end-users | 2894190 | 143604 | 3037794.0 | 0.0% | 3121868.0 | 3181398.0 | -1.9% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1695 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1073 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2369 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5093). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5093 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 322012 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
