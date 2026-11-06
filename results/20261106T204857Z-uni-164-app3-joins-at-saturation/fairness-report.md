# Fairness benchmark: app3-joins-at-saturation (uni-164-app3-joins-at-saturation)

**Verdict: FAIL** (threshold: 10 points)

- end-users deviated -32.3 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `app3-joins-at-saturation` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-796bc55c4b-4zdmn` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-06T20:50:08Z` |
| Run end | `2026-11-06T20:54:41Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 30.0 | 96 | 1850 | 200=1840, 500=10 | 10.2 | 27.4 | 2379794.0 | 30.0% | 55.2% | 25.2 | 55.8% | 25.8 | 6.0s | 98.9% | 1840.0 |
| app2 | 10.0 | 32 | 564 | 200=555, 500=9 | 14.9 | 24.3 | 739632.0 | 10.0% | 17.1% | 7.1 | 17.0% | 7.0 | 6.4s | 98.9% | 555.0 |
| end-users | 60.0 | 128 | 900 | 200=883, 500=17 | 21.3 | 22.6 | 1194036.0 | 60.0% | 27.7% | -32.3 | 27.2% | -32.8 | 5.4s | 98.9% | 883.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- end-users: active 120s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 90.0 | 90.0 |
| 120.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (28 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 58168.0 | 75.0% | 72.9% | -2.1 |
| 0.0 | 10.0 | app2 | True | 21678.0 | 25.0% | 27.1% | 2.1 |
| 0.0 | 10.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | True | 136524.0 | 75.0% | 73.2% | -1.8 |
| 10.0 | 20.0 | app2 | True | 49952.0 | 25.0% | 26.8% | 1.8 |
| 10.0 | 20.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | True | 147316.0 | 75.0% | 85.2% | 10.2 |
| 20.0 | 30.0 | app2 | True | 25652.0 | 25.0% | 14.8% | -10.2 |
| 20.0 | 30.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | True | 113650.0 | 75.0% | 66.7% | -8.3 |
| 30.0 | 40.0 | app2 | True | 56798.0 | 25.0% | 33.3% | 8.3 |
| 30.0 | 40.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | True | 160888.0 | 75.0% | 93.7% | 18.7 |
| 40.0 | 50.0 | app2 | True | 10790.0 | 25.0% | 6.3% | -18.7 |
| 40.0 | 50.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | True | 118890.0 | 75.0% | 69.8% | -5.2 |
| 50.0 | 60.0 | app2 | True | 51360.0 | 25.0% | 30.2% | 5.2 |
| 50.0 | 60.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | True | 136578.0 | 75.0% | 76.5% | 1.5 |
| 60.0 | 70.0 | app2 | True | 41900.0 | 25.0% | 23.5% | -1.5 |
| 60.0 | 70.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | True | 127146.0 | 75.0% | 71.7% | -3.3 |
| 70.0 | 80.0 | app2 | True | 50110.0 | 25.0% | 28.3% | 3.3 |
| 70.0 | 80.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | True | 169032.0 | 75.0% | 100.0% | 25.0 |
| 80.0 | 90.0 | app2 | True | 0.0 | 25.0% | 0.0% | -25.0 |
| 80.0 | 90.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app1 | True | 124288.0 | 75.0% | 74.2% | -0.8 |
| 90.0 | 100.0 | app2 | True | 43246.0 | 25.0% | 25.8% | 0.8 |
| 90.0 | 100.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 100.0 | 110.0 | app1 | True | 124430.0 | 75.0% | 74.2% | -0.8 |
| 100.0 | 110.0 | app2 | True | 43242.0 | 25.0% | 25.8% | 0.8 |
| 100.0 | 110.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app1 | True | 131122.0 | 75.0% | 75.8% | 0.8 |
| 110.0 | 120.0 | app2 | True | 41942.0 | 25.0% | 24.2% | -0.8 |
| 110.0 | 120.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | True | 140736.0 | 30.0% | 82.5% | 52.5 |
| 120.0 | 130.0 | app2 | True | 18916.0 | 10.0% | 11.1% | 1.1 |
| 120.0 | 130.0 | end-users | True | 10838.0 | 60.0% | 6.4% | -53.6 |
| 130.0 | 141.0 | app1 | True | 43200.0 | 30.0% | 19.5% | -10.5 |
| 130.0 | 141.0 | app2 | True | 37904.0 | 10.0% | 17.1% | 7.1 |
| 130.0 | 141.0 | end-users | True | 140768.0 | 60.0% | 63.4% | 3.4 |
| 141.0 | 151.0 | app1 | True | 117768.0 | 30.0% | 70.7% | 40.7 |
| 141.0 | 151.0 | app2 | True | 16252.0 | 10.0% | 9.8% | -0.2 |
| 141.0 | 151.0 | end-users | True | 32526.0 | 60.0% | 19.5% | -40.5 |
| 151.0 | 161.0 | app1 | True | 39180.0 | 30.0% | 23.8% | -6.2 |
| 151.0 | 161.0 | app2 | True | 20238.0 | 10.0% | 12.3% | 2.3 |
| 151.0 | 161.0 | end-users | True | 105360.0 | 60.0% | 63.9% | 3.9 |
| 161.0 | 171.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 161.0 | 171.0 | app2 | True | 21626.0 | 10.0% | 13.8% | 3.8 |
| 161.0 | 171.0 | end-users | True | 135126.0 | 60.0% | 86.2% | 26.2 |
| 171.0 | 181.0 | app1 | True | 132482.0 | 30.0% | 79.7% | 49.7 |
| 171.0 | 181.0 | app2 | True | 17582.0 | 10.0% | 10.6% | 0.6 |
| 171.0 | 181.0 | end-users | True | 16264.0 | 60.0% | 9.8% | -50.2 |
| 181.0 | 191.0 | app1 | True | 10848.0 | 30.0% | 6.4% | -23.6 |
| 181.0 | 191.0 | app2 | True | 22966.0 | 10.0% | 13.6% | 3.6 |
| 181.0 | 191.0 | end-users | True | 135312.0 | 60.0% | 80.0% | 20.0 |
| 191.0 | 201.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 191.0 | 201.0 | app2 | True | 31038.0 | 10.0% | 19.8% | 9.8 |
| 191.0 | 201.0 | end-users | True | 125748.0 | 60.0% | 80.2% | 20.2 |
| 201.0 | 211.0 | app1 | True | 137964.0 | 30.0% | 82.9% | 52.9 |
| 201.0 | 211.0 | app2 | True | 8128.0 | 10.0% | 4.9% | -5.1 |
| 201.0 | 211.0 | end-users | True | 20242.0 | 60.0% | 12.2% | -47.8 |
| 211.0 | 221.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 211.0 | 221.0 | app2 | True | 24340.0 | 10.0% | 14.3% | 4.3 |
| 211.0 | 221.0 | end-users | True | 146006.0 | 60.0% | 85.7% | 25.7 |
| 221.0 | 231.0 | app1 | True | 35174.0 | 30.0% | 21.7% | -8.3 |
| 221.0 | 231.0 | app2 | True | 31106.0 | 10.0% | 19.2% | 9.2 |
| 221.0 | 231.0 | end-users | True | 95950.0 | 60.0% | 59.1% | -0.9 |
| 231.0 | 241.0 | app1 | True | 106724.0 | 30.0% | 65.8% | 35.8 |
| 231.0 | 241.0 | app2 | True | 9488.0 | 10.0% | 5.9% | -4.1 |
| 231.0 | 241.0 | end-users | True | 45936.0 | 60.0% | 28.3% | -31.7 |
| 241.0 | 251.0 | app1 | False | 1358.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 23044.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 143414.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 66328.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 20334.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 40546.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 273.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 273.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 273.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 86 | 591ms | 2121ms | 2462ms |
| 0.0 | 10.0 | app2 | ok | 23 | 607ms | 1925ms | 2442ms |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 149 | 2483ms | 6079ms | 9608ms |
| 10.0 | 20.0 | app2 | ok | 47 | 2453ms | 6643ms | 9664ms |
| 10.0 | 20.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 80 | 4286ms | 8824ms | 9882ms |
| 20.0 | 30.0 | app2 | ok | 32 | 6000ms | 9200ms | 9920ms |
| 20.0 | 30.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 95 | 5343ms | 9069ms | 9907ms |
| 30.0 | 40.0 | app2 | ok | 16 | 2500ms | 4500ms | 4950ms |
| 30.0 | 40.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 79 | 3292ms | 7921ms | 9792ms |
| 40.0 | 50.0 | app2 | ok | 32 | 7500ms | 9500ms | 9950ms |
| 40.0 | 50.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 175 | 4329ms | 8801ms | 9880ms |
| 50.0 | 60.0 | app2 | ok | 40 | 6000ms | 9200ms | 9920ms |
| 50.0 | 60.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 96 | 5714ms | 9143ms | 9914ms |
| 60.0 | 70.0 | app2 | ok | 26 | 917ms | 7400ms | 9740ms |
| 60.0 | 70.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 93 | 4491ms | 8866ms | 9887ms |
| 70.0 | 80.0 | app2 | ok | 18 | 6538ms | 9308ms | 9931ms |
| 70.0 | 80.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 81 | 3259ms | 8071ms | 9807ms |
| 80.0 | 90.0 | app2 | ok | 32 | 7500ms | 9500ms | 9950ms |
| 80.0 | 90.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 95 | 5682ms | 9136ms | 9914ms |
| 90.0 | 100.0 | app2 | ok | 17 | 917ms | 2181ms | 2468ms |
| 90.0 | 100.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 96 | 4352ms | 8829ms | 9883ms |
| 100.0 | 110.0 | app2 | ok | 17 | 7167ms | 9433ms | 9943ms |
| 100.0 | 110.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 80 | 3214ms | 8000ms | 9800ms |
| 110.0 | 120.0 | app2 | ok | 31 | 7500ms | 9500ms | 9950ms |
| 110.0 | 120.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 74 | 3611ms | 8318ms | 9832ms |
| 120.0 | 130.0 | app2 | ok | 32 | 7500ms | 9500ms | 9950ms |
| 120.0 | 130.0 | end-users | ok | 10 | 44ms | 100ms | 235ms |
| 130.0 | 141.0 | app1 | ok | 64 | 4924ms | 8968ms | 9897ms |
| 130.0 | 141.0 | app2 | ok | 22 | 688ms | 1950ms | 2445ms |
| 130.0 | 141.0 | end-users | ok | 126 | 6881ms | 9376ms | 9938ms |
| 141.0 | 151.0 | app1 | ok | 85 | 15088ms | 27018ms | 29702ms |
| 141.0 | 151.0 | app2 | ok | 13 | 20000ms | 28000ms | 29800ms |
| 141.0 | 151.0 | end-users | ok | 75 | 12955ms | 26591ms | 29659ms |
| 151.0 | 161.0 | app1 | ok | 27 | 20000ms | 28000ms | 29800ms |
| 151.0 | 161.0 | app2 | ok | 31 | 13684ms | 26737ms | 29674ms |
| 151.0 | 161.0 | end-users | ok | 115 | 8125ms | 25660ms | 29566ms |
| 161.0 | 171.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 161.0 | 171.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 161.0 | 171.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 80 | 18406ms | 27681ms | 29768ms |
| 171.0 | 181.0 | app2 | ok | 13 | 13750ms | 26750ms | 29675ms |
| 171.0 | 181.0 | end-users | ok | 78 | 14082ms | 26816ms | 29682ms |
| 181.0 | 191.0 | app1 | ok | 23 | 20000ms | 28000ms | 29800ms |
| 181.0 | 191.0 | app2 | ok | 30 | 14211ms | 26842ms | 29684ms |
| 181.0 | 191.0 | end-users | ok | 115 | 7321ms | 25400ms | 29540ms |
| 191.0 | 201.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 80 | 19041ms | 27808ms | 29781ms |
| 201.0 | 211.0 | app2 | ok | 14 | 12500ms | 26500ms | 29650ms |
| 201.0 | 211.0 | end-users | ok | 81 | 12766ms | 26553ms | 29655ms |
| 211.0 | 221.0 | app1 | ok | 26 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app2 | ok | 30 | 13333ms | 26667ms | 29667ms |
| 211.0 | 221.0 | end-users | ok | 114 | 7222ms | 25149ms | 29515ms |
| 221.0 | 231.0 | app1 | ok | 81 | 18429ms | 27686ms | 29769ms |
| 221.0 | 231.0 | app2 | ok | 14 | 12500ms | 26500ms | 29650ms |
| 221.0 | 231.0 | end-users | ok | 81 | 13469ms | 26694ms | 29669ms |
| 231.0 | 241.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 49 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | app2 | ok | 25 | 16111ms | 27222ms | 29722ms |
| 241.0 | 251.0 | end-users | ok | 88 | 11277ms | 26255ms | 29626ms |
| 251.0 | 261.0 | app1 | ok | 46 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 273.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 273.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 273.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2263200 | 112328 | 2375528.0 | 0.0% | 2379794.0 | 2487856.0 | -4.3% | True |
| app2 | 682650 | 33901 | 716551.0 | 0.0% | 739632.0 | 750452.0 | -1.4% | True |
| end-users | 1086090 | 53973 | 1140063.0 | 0.0% | 1194036.0 | 1194036.0 | 0.0% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1850 | 0 | 0 | 0 (never shed) | 0.00% | 30.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 564 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 900 | 0 | 0 | 0 (never shed) | 0.00% | 60.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=3278). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 263034 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
