# Fairness benchmark: app3-joins-at-saturation (uni310-l2-r1-uni164-app3-joins)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 10.0 points
Schedule-aware expected share (UNI-222): app1, app2, end-users scored against a time-weighted entitlement from the declared join/leave or duty-cycle schedule, not the flat whole-run weight ratio -- see docs/design.md "Whole-run scoring with a declared schedule".

## Run metadata

| field | value |
|---|---|
| Scenario | `app3-joins-at-saturation` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-85c4448547-nztjz` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T03:48:33Z` |
| Run end | `2026-11-26T03:52:51Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 27 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/27 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 74.50 | 2.3281 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 30.0 | 96 | 2875 | 200=2875 | 6.0 | 16.5 | 3730480.0 | 52.2% | 37.5% | 7.5 | 52.9% | 0.7 | 52.7% | 22.7 | 42.2s | 98.9% | 2875.0 |
| app2 | 10.0 | 32 | 959 | 200=959 | 6.0 | 16.4 | 1240188.0 | 17.4% | 12.5% | 2.5 | 17.6% | 0.2 | 17.6% | 7.6 | 42.2s | 98.9% | 959.0 |
| end-users | 60.0 | 128 | 1626 | 200=1626 | 9.6 | 12.9 | 2197322.0 | 30.4% | 50.0% | -10.0 | 29.5% | -0.9 | 29.8% | -30.2 | 37.6s | 98.9% | 1626.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

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
| 0.0 | 0.0 | 0.0 |
| 120.0 | 131.0 | 11.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 20300.0 | 75.0% | 79.0% | 4.0 |
| 0.0 | 10.0 | app2 | True | False | 5386.0 | 25.0% | 21.0% | -4.0 |
| 0.0 | 10.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | True | False | 220316.0 | 75.0% | 74.4% | -0.6 |
| 10.0 | 20.0 | app2 | True | False | 75676.0 | 25.0% | 25.6% | 0.6 |
| 10.0 | 20.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | True | False | 224484.0 | 75.0% | 75.1% | 0.1 |
| 20.0 | 30.0 | app2 | True | False | 74420.0 | 25.0% | 24.9% | -0.1 |
| 20.0 | 30.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | True | False | 227226.0 | 75.0% | 74.7% | -0.3 |
| 30.0 | 40.0 | app2 | True | False | 77034.0 | 25.0% | 25.3% | 0.3 |
| 30.0 | 40.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | True | False | 228706.0 | 75.0% | 75.5% | 0.5 |
| 40.0 | 50.0 | app2 | True | False | 74334.0 | 25.0% | 24.5% | -0.5 |
| 40.0 | 50.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | True | False | 227088.0 | 75.0% | 75.0% | -0.0 |
| 50.0 | 60.0 | app2 | True | False | 75820.0 | 25.0% | 25.0% | 0.0 |
| 50.0 | 60.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | True | False | 231040.0 | 75.0% | 75.7% | 0.7 |
| 60.0 | 70.0 | app2 | True | False | 74334.0 | 25.0% | 24.3% | -0.7 |
| 60.0 | 70.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 70.0 | 81.0 | app1 | True | False | 224376.0 | 75.0% | 74.8% | -0.2 |
| 70.0 | 81.0 | app2 | True | False | 75746.0 | 25.0% | 25.2% | 0.2 |
| 70.0 | 81.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 81.0 | 91.0 | app1 | True | False | 232296.0 | 75.0% | 75.1% | 0.1 |
| 81.0 | 91.0 | app2 | True | False | 77106.0 | 25.0% | 24.9% | -0.1 |
| 81.0 | 91.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 91.0 | 101.0 | app1 | True | False | 220424.0 | 75.0% | 75.1% | 0.1 |
| 91.0 | 101.0 | app2 | True | False | 73088.0 | 25.0% | 24.9% | -0.1 |
| 91.0 | 101.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 101.0 | 111.0 | app1 | True | False | 231116.0 | 75.0% | 75.7% | 0.7 |
| 101.0 | 111.0 | app2 | True | False | 74354.0 | 25.0% | 24.3% | -0.7 |
| 101.0 | 111.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 111.0 | 121.0 | app1 | True | False | 224524.0 | 75.0% | 75.1% | 0.1 |
| 111.0 | 121.0 | app2 | True | False | 74416.0 | 25.0% | 24.9% | -0.1 |
| 111.0 | 121.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 121.0 | 131.0 | app1 | True | False | 143330.0 | 30.0% | 47.5% | 17.5 |
| 121.0 | 131.0 | app2 | True | False | 48728.0 | 10.0% | 16.2% | 6.2 |
| 121.0 | 131.0 | end-users | True | False | 109624.0 | 60.0% | 36.3% | -23.7 |
| 131.0 | 141.0 | app1 | True | False | 83846.0 | 30.0% | 27.8% | -2.2 |
| 131.0 | 141.0 | app2 | True | False | 28432.0 | 10.0% | 9.4% | -0.6 |
| 131.0 | 141.0 | end-users | True | False | 189616.0 | 60.0% | 62.8% | 2.8 |
| 141.0 | 151.0 | app1 | True | False | 75710.0 | 30.0% | 29.6% | -0.4 |
| 141.0 | 151.0 | app2 | True | False | 25682.0 | 10.0% | 10.1% | 0.1 |
| 141.0 | 151.0 | end-users | True | False | 154134.0 | 60.0% | 60.3% | 0.3 |
| 151.0 | 161.0 | app1 | True | False | 93302.0 | 30.0% | 30.3% | 0.3 |
| 151.0 | 161.0 | app2 | True | False | 32506.0 | 10.0% | 10.5% | 0.5 |
| 151.0 | 161.0 | end-users | True | False | 182366.0 | 60.0% | 59.2% | -0.8 |
| 161.0 | 171.0 | app1 | True | False | 93362.0 | 30.0% | 30.4% | 0.4 |
| 161.0 | 171.0 | app2 | True | False | 28434.0 | 10.0% | 9.3% | -0.7 |
| 161.0 | 171.0 | end-users | True | False | 185024.0 | 60.0% | 60.3% | 0.3 |
| 171.0 | 181.0 | app1 | True | False | 90654.0 | 30.0% | 29.7% | -0.3 |
| 171.0 | 181.0 | app2 | True | False | 32374.0 | 10.0% | 10.6% | 0.6 |
| 171.0 | 181.0 | end-users | True | False | 182622.0 | 60.0% | 59.7% | -0.3 |
| 181.0 | 191.0 | app1 | True | False | 74392.0 | 30.0% | 29.9% | -0.1 |
| 181.0 | 191.0 | app2 | True | False | 24310.0 | 10.0% | 9.8% | -0.2 |
| 181.0 | 191.0 | end-users | True | False | 150030.0 | 60.0% | 60.3% | 0.3 |
| 191.0 | 201.0 | app1 | True | False | 73012.0 | 30.0% | 30.2% | 0.2 |
| 191.0 | 201.0 | app2 | True | False | 24380.0 | 10.0% | 10.1% | 0.1 |
| 191.0 | 201.0 | end-users | True | False | 144602.0 | 60.0% | 59.8% | -0.2 |
| 201.0 | 211.0 | app1 | True | False | 89250.0 | 30.0% | 29.4% | -0.6 |
| 201.0 | 211.0 | app2 | True | False | 29756.0 | 10.0% | 9.8% | -0.2 |
| 201.0 | 211.0 | end-users | True | False | 184140.0 | 60.0% | 60.7% | 0.7 |
| 211.0 | 221.0 | app1 | True | False | 77156.0 | 30.0% | 30.3% | 0.3 |
| 211.0 | 221.0 | app2 | True | False | 24324.0 | 10.0% | 9.6% | -0.4 |
| 211.0 | 221.0 | end-users | True | False | 152890.0 | 60.0% | 60.1% | 0.1 |
| 221.0 | 231.0 | app1 | True | False | 93348.0 | 30.0% | 30.3% | 0.3 |
| 221.0 | 231.0 | app2 | True | False | 31120.0 | 10.0% | 10.1% | 0.1 |
| 221.0 | 231.0 | end-users | True | False | 183754.0 | 60.0% | 59.6% | -0.4 |
| 231.0 | 241.0 | app1 | True | False | 90548.0 | 30.0% | 29.6% | -0.4 |
| 231.0 | 241.0 | app2 | True | False | 31072.0 | 10.0% | 10.2% | 0.2 |
| 231.0 | 241.0 | end-users | True | False | 183782.0 | 60.0% | 60.2% | 0.2 |
| 241.0 | 251.0 | app1 | False | n/a | 91976.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 29780.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 181204.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app1 | False | n/a | 48698.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | False | n/a | 17576.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | end-users | False | n/a | 13534.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 167 | 0ms | 1763ms | 2426ms |
| 0.0 | 10.0 | app2 | ok | 56 | 0ms | 1736ms | 2424ms |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 184 | 1032ms | 2206ms | 2471ms |
| 10.0 | 20.0 | app2 | ok | 62 | 1091ms | 2218ms | 2472ms |
| 10.0 | 20.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 154 | 1157ms | 2231ms | 2473ms |
| 20.0 | 30.0 | app2 | ok | 51 | 1181ms | 2236ms | 2474ms |
| 20.0 | 30.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 176 | 1111ms | 2222ms | 2472ms |
| 30.0 | 40.0 | app2 | ok | 58 | 1050ms | 2210ms | 2471ms |
| 30.0 | 40.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 186 | 1146ms | 2229ms | 2473ms |
| 40.0 | 50.0 | app2 | ok | 61 | 1154ms | 2231ms | 2473ms |
| 40.0 | 50.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 148 | 1095ms | 2219ms | 2472ms |
| 50.0 | 60.0 | app2 | ok | 50 | 1161ms | 2232ms | 2473ms |
| 50.0 | 60.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 186 | 1016ms | 2203ms | 2470ms |
| 60.0 | 70.0 | app2 | ok | 63 | 983ms | 2195ms | 2470ms |
| 60.0 | 70.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 70.0 | 81.0 | app1 | ok | 150 | 1058ms | 2212ms | 2471ms |
| 70.0 | 81.0 | app2 | ok | 50 | 1000ms | 2200ms | 2470ms |
| 70.0 | 81.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 185 | 1084ms | 2217ms | 2472ms |
| 81.0 | 91.0 | app2 | ok | 63 | 986ms | 2195ms | 2470ms |
| 81.0 | 91.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 187 | 994ms | 2198ms | 2470ms |
| 91.0 | 101.0 | app2 | ok | 60 | 1094ms | 2219ms | 2472ms |
| 91.0 | 101.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 148 | 912ms | 2169ms | 2467ms |
| 101.0 | 111.0 | app2 | ok | 49 | 904ms | 2166ms | 2467ms |
| 101.0 | 111.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 185 | 1039ms | 2208ms | 2471ms |
| 111.0 | 121.0 | app2 | ok | 63 | 1188ms | 2238ms | 2474ms |
| 111.0 | 121.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 59 | 1862ms | 8595ms | 9860ms |
| 121.0 | 131.0 | app2 | ok | 19 | 1964ms | 8643ms | 9864ms |
| 121.0 | 131.0 | end-users | ok | 164 | 2404ms | 4559ms | 7267ms |
| 131.0 | 141.0 | app1 | ok | 59 | 12121ms | 26424ms | 29642ms |
| 131.0 | 141.0 | app2 | ok | 20 | 10000ms | 26000ms | 29600ms |
| 131.0 | 141.0 | end-users | ok | 120 | 4005ms | 7391ms | 9739ms |
| 141.0 | 151.0 | app1 | ok | 67 | 8807ms | 24174ms | 29417ms |
| 141.0 | 151.0 | app2 | ok | 22 | 8667ms | 23714ms | 29371ms |
| 141.0 | 151.0 | end-users | ok | 136 | 4241ms | 8667ms | 9867ms |
| 151.0 | 161.0 | app1 | ok | 60 | 16364ms | 27273ms | 29727ms |
| 151.0 | 161.0 | app2 | ok | 20 | 17500ms | 27500ms | 29750ms |
| 151.0 | 161.0 | end-users | ok | 118 | 4958ms | 8983ms | 9898ms |
| 161.0 | 171.0 | app1 | ok | 66 | 8235ms | 21200ms | 29120ms |
| 161.0 | 171.0 | app2 | ok | 22 | 8438ms | 22667ms | 29267ms |
| 161.0 | 171.0 | end-users | ok | 135 | 4485ms | 8650ms | 9865ms |
| 171.0 | 181.0 | app1 | ok | 77 | 8208ms | 20941ms | 29094ms |
| 171.0 | 181.0 | app2 | ok | 26 | 8421ms | 22571ms | 29257ms |
| 171.0 | 181.0 | end-users | ok | 150 | 4356ms | 8469ms | 9847ms |
| 181.0 | 191.0 | app1 | ok | 38 | 7727ms | 11000ms | 28100ms |
| 181.0 | 191.0 | app2 | ok | 13 | 7708ms | 9875ms | 27400ms |
| 181.0 | 191.0 | end-users | ok | 80 | 3071ms | 6923ms | 9692ms |
| 191.0 | 201.0 | app1 | ok | 65 | 8561ms | 24348ms | 29435ms |
| 191.0 | 201.0 | app2 | ok | 21 | 8125ms | 23000ms | 29300ms |
| 191.0 | 201.0 | end-users | ok | 85 | 5573ms | 9115ms | 9911ms |
| 201.0 | 211.0 | app1 | ok | 81 | 9632ms | 25737ms | 29574ms |
| 201.0 | 211.0 | app2 | ok | 28 | 9545ms | 25692ms | 29569ms |
| 201.0 | 211.0 | end-users | ok | 207 | 4705ms | 8887ms | 9889ms |
| 211.0 | 221.0 | app1 | ok | 37 | 8700ms | 23833ms | 29383ms |
| 211.0 | 221.0 | app2 | ok | 12 | 8750ms | 24000ms | 29400ms |
| 211.0 | 221.0 | end-users | ok | 73 | 5068ms | 9014ms | 9901ms |
| 221.0 | 231.0 | app1 | ok | 77 | 9278ms | 25188ms | 29519ms |
| 221.0 | 231.0 | app2 | ok | 25 | 9464ms | 25455ms | 29545ms |
| 221.0 | 231.0 | end-users | ok | 153 | 4291ms | 8372ms | 9837ms |
| 231.0 | 241.0 | app1 | ok | 62 | 8100ms | 19667ms | 28967ms |
| 231.0 | 241.0 | app2 | ok | 21 | 8281ms | 21600ms | 29160ms |
| 231.0 | 241.0 | end-users | ok | 123 | 4330ms | 8423ms | 9842ms |
| 241.0 | 251.0 | app1 | ok | 71 | 8008ms | 18167ms | 28817ms |
| 241.0 | 251.0 | app2 | ok | 24 | 7857ms | 14000ms | 28400ms |
| 241.0 | 251.0 | end-users | ok | 82 | 4884ms | 8949ms | 9895ms |
| 251.0 | 258.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 3536250 | 175559 | 3711809.0 | 0.0% | 3730480.0 | 3887368.0 | -4.0% | True |
| app2 | 1179570 | 58747 | 1238317.0 | 0.0% | 1240188.0 | 1297064.0 | -4.4% | True |
| end-users | 1999980 | 99350 | 2099330.0 | 0.0% | 2197322.0 | 2198680.0 | -0.1% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2875 | 0 | 0 | 0 (never shed) | 0.00% | 30.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 959 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1626 | 0 | 0 | 0 (never shed) | 0.00% | 60.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5460). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5460 | 0.051ms | 0.105ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 245115 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 2875 | 5959ms | 18048ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 959 | 5968ms | 17993ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 1626 | 9540ms | 14353ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5460 | 7495ms | 17179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2711ms | 5192ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2643ms | 5175ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 5482ms | 7607ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 5500ms | 7631ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 5535ms | 7622ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 5574ms | 7656ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 5585ms | 7707ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 5646ms | 7715ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 5623ms | 7705ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 5521ms | 7665ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 5619ms | 7679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 5500ms | 7620ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 5494ms | 7607ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 5550ms | 7705ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 81.0 | app1 | ok | 5616ms | 7700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 81.0 | app2 | ok | 5614ms | 7715ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 81.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 5542ms | 7640ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app2 | ok | 5536ms | 7637ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 5612ms | 7691ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 5580ms | 7676ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 5554ms | 7675ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 5455ms | 7650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 5638ms | 7695ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 5596ms | 7683ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 5673ms | 7806ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 5789ms | 7877ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 4952ms | 7453ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 12727ms | 17417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 12625ms | 14988ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 8475ms | 11111ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 16585ms | 19659ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 16042ms | 19604ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 9556ms | 14305ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 16250ms | 19625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 16000ms | 19600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 10833ms | 14583ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 13255ms | 18922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 13281ms | 18950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 9378ms | 14099ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 13284ms | 18953ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 13529ms | 19143ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 9375ms | 14250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 13716ms | 19236ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 13750ms | 19250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 9500ms | 14323ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 16932ms | 19693ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 17000ms | 19700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 12124ms | 14712ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 17281ms | 19886ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 17500ms | 26333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 10143ms | 14514ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 16524ms | 19652ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 15909ms | 19591ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 10654ms | 14565ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 16406ms | 19641ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 16406ms | 19641ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 9903ms | 14477ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 13221ms | 18883ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 13026ms | 18562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 9416ms | 14190ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 13036ms | 18583ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 12895ms | 18167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 9255ms | 13953ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app1 | ok | 12727ms | 17000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app2 | ok | 12708ms | 16750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | end-users | ok | 10833ms | 14583ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
