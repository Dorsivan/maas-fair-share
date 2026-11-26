# Fairness benchmark: full-contention-2x (uni310-l2-r1-f3-98-1-1)

**Verdict: FAIL** (threshold: 10 points)
**Secondary (priority) verdict: PRIORITY-OK** -- see "Per-tenant TTFT / ITL and the priority verdict (UNI-226)" below for detail.
Worker-share vs. weight-share gap (UNI-225): 81.3 points

- app1 deviated -39.7 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-bc8ffb568-xtns9` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T02:48:55Z` |
| Run end | `2026-11-26T02:53:23Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 28 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/28 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 127.00 | 3.9688 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 98.0 | 64 | 2979 | 200=2979 | 4.2 | 8.0 | 3998820.0 | 98.0% | 16.7% | -81.3 | 58.3% | -39.7 | 55.5% | -42.5 | 64.0s | 98.9% | 2979.0 |
| app2 | 1.0 | 64 | 1023 | 200=1023 | 14.1 | 24.7 | 1356172.0 | 1.0% | 16.7% | 15.7 | 19.8% | 18.8 | 19.0% | 18.0 | 65.8s | 98.9% | 1023.0 |
| end-users | 1.0 | 256 | 1369 | 200=1369 | 47.9 | 71.1 | 1500160.0 | 1.0% | 66.7% | 65.7 | 21.9% | 20.9 | 25.5% | 24.5 | 65.8s | 98.9% | 1369.0 |
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

**Windows** (27 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 35180.0 | 98.0% | 100.0% | 2.0 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 1.0% | 0.0% | -1.0 |
| 0.0 | 10.0 | end-users | True | False | 0.0 | 1.0% | 0.0% | -1.0 |
| 10.0 | 20.0 | app1 | True | False | 155450.0 | 98.0% | 68.8% | -29.2 |
| 10.0 | 20.0 | app2 | True | False | 64966.0 | 1.0% | 28.8% | 27.8 |
| 10.0 | 20.0 | end-users | True | False | 5392.0 | 1.0% | 2.4% | 1.4 |
| 20.0 | 30.0 | app1 | True | False | 174348.0 | 98.0% | 58.1% | -39.9 |
| 20.0 | 30.0 | app2 | True | False | 71702.0 | 1.0% | 23.9% | 22.9 |
| 20.0 | 30.0 | end-users | True | False | 54028.0 | 1.0% | 18.0% | 17.0 |
| 30.0 | 40.0 | app1 | True | False | 162220.0 | 98.0% | 53.3% | -44.7 |
| 30.0 | 40.0 | app2 | True | False | 68976.0 | 1.0% | 22.7% | 21.7 |
| 30.0 | 40.0 | end-users | True | False | 73050.0 | 1.0% | 24.0% | 23.0 |
| 40.0 | 50.0 | app1 | True | False | 228380.0 | 98.0% | 74.4% | -23.6 |
| 40.0 | 50.0 | app2 | True | False | 40602.0 | 1.0% | 13.2% | 12.2 |
| 40.0 | 50.0 | end-users | True | False | 37916.0 | 1.0% | 12.4% | 11.4 |
| 50.0 | 60.0 | app1 | True | False | 224638.0 | 98.0% | 72.8% | -25.2 |
| 50.0 | 60.0 | app2 | True | False | 43244.0 | 1.0% | 14.0% | 13.0 |
| 50.0 | 60.0 | end-users | True | False | 40624.0 | 1.0% | 13.2% | 12.2 |
| 60.0 | 70.0 | app1 | True | False | 185200.0 | 98.0% | 60.6% | -37.4 |
| 60.0 | 70.0 | app2 | True | False | 59500.0 | 1.0% | 19.5% | 18.5 |
| 60.0 | 70.0 | end-users | True | False | 60786.0 | 1.0% | 19.9% | 18.9 |
| 70.0 | 80.0 | app1 | True | False | 216566.0 | 98.0% | 71.1% | -26.9 |
| 70.0 | 80.0 | app2 | True | False | 44562.0 | 1.0% | 14.6% | 13.6 |
| 70.0 | 80.0 | end-users | True | False | 43384.0 | 1.0% | 14.2% | 13.2 |
| 80.0 | 90.0 | app1 | True | False | 225788.0 | 98.0% | 73.3% | -24.7 |
| 80.0 | 90.0 | app2 | True | False | 41868.0 | 1.0% | 13.6% | 12.6 |
| 80.0 | 90.0 | end-users | True | False | 40564.0 | 1.0% | 13.2% | 12.2 |
| 90.0 | 100.0 | app1 | True | False | 200110.0 | 98.0% | 65.5% | -32.5 |
| 90.0 | 100.0 | app2 | True | False | 52776.0 | 1.0% | 17.3% | 16.3 |
| 90.0 | 100.0 | end-users | True | False | 52726.0 | 1.0% | 17.3% | 16.3 |
| 100.0 | 110.0 | app1 | True | False | 179778.0 | 98.0% | 58.8% | -39.2 |
| 100.0 | 110.0 | app2 | True | False | 63698.0 | 1.0% | 20.8% | 19.8 |
| 100.0 | 110.0 | end-users | True | False | 62252.0 | 1.0% | 20.4% | 19.4 |
| 110.0 | 120.0 | app1 | True | False | 226002.0 | 98.0% | 75.6% | -22.4 |
| 110.0 | 120.0 | app2 | True | False | 37854.0 | 1.0% | 12.7% | 11.7 |
| 110.0 | 120.0 | end-users | True | False | 35158.0 | 1.0% | 11.8% | 10.8 |
| 120.0 | 130.0 | app1 | True | False | 86564.0 | 98.0% | 38.6% | -59.4 |
| 120.0 | 130.0 | app2 | True | False | 68842.0 | 1.0% | 30.7% | 29.7 |
| 120.0 | 130.0 | end-users | True | False | 68876.0 | 1.0% | 30.7% | 29.7 |
| 130.0 | 140.0 | app1 | True | False | 0.0 | 98.0% | 0.0% | -98.0 |
| 130.0 | 140.0 | app2 | True | False | 17588.0 | 1.0% | 11.6% | 10.6 |
| 130.0 | 140.0 | end-users | True | False | 134016.0 | 1.0% | 88.4% | 87.4 |
| 140.0 | 150.0 | app1 | True | False | 85306.0 | 98.0% | 35.6% | -62.4 |
| 140.0 | 150.0 | app2 | True | False | 10794.0 | 1.0% | 4.5% | 3.5 |
| 140.0 | 150.0 | end-users | True | False | 143416.0 | 1.0% | 59.9% | 58.9 |
| 150.0 | 160.0 | app1 | True | False | 129908.0 | 98.0% | 46.9% | -51.1 |
| 150.0 | 160.0 | app2 | True | False | 94480.0 | 1.0% | 34.1% | 33.1 |
| 150.0 | 160.0 | end-users | True | False | 52614.0 | 1.0% | 19.0% | 18.0 |
| 160.0 | 170.0 | app1 | True | False | 200118.0 | 98.0% | 67.0% | -31.0 |
| 160.0 | 170.0 | app2 | True | False | 47316.0 | 1.0% | 15.8% | 14.8 |
| 160.0 | 170.0 | end-users | True | False | 51454.0 | 1.0% | 17.2% | 16.2 |
| 170.0 | 180.0 | app1 | True | False | 167608.0 | 98.0% | 55.8% | -42.2 |
| 170.0 | 180.0 | app2 | True | False | 66242.0 | 1.0% | 22.1% | 21.1 |
| 170.0 | 180.0 | end-users | True | False | 66274.0 | 1.0% | 22.1% | 21.1 |
| 180.0 | 190.0 | app1 | True | False | 221808.0 | 98.0% | 72.2% | -25.8 |
| 180.0 | 190.0 | app2 | True | False | 41932.0 | 1.0% | 13.7% | 12.7 |
| 180.0 | 190.0 | end-users | True | False | 43282.0 | 1.0% | 14.1% | 13.1 |
| 190.0 | 200.0 | app1 | True | False | 215012.0 | 98.0% | 71.0% | -27.0 |
| 190.0 | 200.0 | app2 | True | False | 44670.0 | 1.0% | 14.7% | 13.7 |
| 190.0 | 200.0 | end-users | True | False | 43266.0 | 1.0% | 14.3% | 13.3 |
| 200.0 | 210.0 | app1 | True | False | 177346.0 | 98.0% | 59.0% | -39.0 |
| 200.0 | 210.0 | app2 | True | False | 60898.0 | 1.0% | 20.3% | 19.3 |
| 200.0 | 210.0 | end-users | True | False | 62258.0 | 1.0% | 20.7% | 19.7 |
| 210.0 | 221.0 | app1 | True | False | 148638.0 | 98.0% | 51.6% | -46.4 |
| 210.0 | 221.0 | app2 | True | False | 67596.0 | 1.0% | 23.5% | 22.5 |
| 210.0 | 221.0 | end-users | True | False | 71740.0 | 1.0% | 24.9% | 23.9 |
| 221.0 | 231.0 | app1 | True | False | 65006.0 | 98.0% | 25.8% | -72.2 |
| 221.0 | 231.0 | app2 | True | False | 83776.0 | 1.0% | 33.3% | 32.3 |
| 221.0 | 231.0 | end-users | True | False | 102828.0 | 1.0% | 40.9% | 39.9 |
| 231.0 | 241.0 | app1 | True | False | 177096.0 | 98.0% | 58.2% | -39.8 |
| 231.0 | 241.0 | app2 | True | False | 75776.0 | 1.0% | 24.9% | 23.9 |
| 231.0 | 241.0 | end-users | True | False | 51388.0 | 1.0% | 16.9% | 15.9 |
| 241.0 | 251.0 | app1 | False | n/a | 110750.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 86514.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 101510.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | n/a | 1358.0 | n/a | n/a | n/a |
| 261.0 | 268.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 268.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 268.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 66 | 120ms | 700ms | 970ms |
| 0.0 | 10.0 | app2 | ok | 64 | 220ms | 787ms | 979ms |
| 0.0 | 10.0 | end-users | ok | 112 | 0ms | 859ms | 1940ms |
| 10.0 | 20.0 | app1 | ok | 146 | 2079ms | 7192ms | 9719ms |
| 10.0 | 20.0 | app2 | ok | 39 | 5125ms | 9025ms | 9902ms |
| 10.0 | 20.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 74 | 1375ms | 3150ms | 4815ms |
| 20.0 | 30.0 | app2 | ok | 59 | 4676ms | 8865ms | 9887ms |
| 20.0 | 30.0 | end-users | ok | 65 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | app1 | ok | 179 | 1779ms | 4172ms | 4961ms |
| 30.0 | 40.0 | app2 | ok | 45 | 4323ms | 8594ms | 9859ms |
| 30.0 | 40.0 | end-users | ok | 30 | 27647ms | 53077ms | 59308ms |
| 40.0 | 50.0 | app1 | ok | 170 | 1247ms | 2368ms | 4528ms |
| 40.0 | 50.0 | app2 | ok | 29 | 11875ms | 26375ms | 29638ms |
| 40.0 | 50.0 | end-users | ok | 29 | 45000ms | 57000ms | 59700ms |
| 50.0 | 60.0 | app1 | ok | 122 | 1326ms | 2387ms | 4564ms |
| 50.0 | 60.0 | app2 | ok | 39 | 7431ms | 9597ms | 22200ms |
| 50.0 | 60.0 | end-users | ok | 40 | 45000ms | 57000ms | 59700ms |
| 60.0 | 70.0 | app1 | ok | 177 | 1343ms | 2473ms | 4723ms |
| 60.0 | 70.0 | app2 | ok | 39 | 7500ms | 9500ms | 9950ms |
| 60.0 | 70.0 | end-users | ok | 38 | 45000ms | 57000ms | 59700ms |
| 70.0 | 80.0 | app1 | ok | 138 | 1380ms | 2377ms | 4507ms |
| 70.0 | 80.0 | app2 | ok | 23 | 8194ms | 20800ms | 29080ms |
| 70.0 | 80.0 | end-users | ok | 24 | 60000ms | 60000ms | 60000ms |
| 80.0 | 90.0 | app1 | ok | 195 | 1196ms | 2250ms | 2487ms |
| 80.0 | 90.0 | app2 | ok | 49 | 11154ms | 26231ms | 29623ms |
| 80.0 | 90.0 | end-users | ok | 48 | 60000ms | 60000ms | 60000ms |
| 90.0 | 100.0 | app1 | ok | 127 | 1652ms | 3016ms | 4802ms |
| 90.0 | 100.0 | app2 | ok | 25 | 7969ms | 21667ms | 29167ms |
| 90.0 | 100.0 | end-users | ok | 24 | 60000ms | 60000ms | 60000ms |
| 100.0 | 110.0 | app1 | ok | 125 | 1602ms | 3641ms | 4864ms |
| 100.0 | 110.0 | app2 | ok | 43 | 6532ms | 9306ms | 9931ms |
| 100.0 | 110.0 | end-users | ok | 46 | 60000ms | 60000ms | 60000ms |
| 110.0 | 120.0 | app1 | ok | 198 | 1191ms | 2356ms | 4505ms |
| 110.0 | 120.0 | app2 | ok | 66 | 7368ms | 19846ms | 28985ms |
| 110.0 | 120.0 | end-users | ok | 234 | 36881ms | 60000ms | 60000ms |
| 120.0 | 130.0 | app1 | ok | 1 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 20 | 4167ms | 8750ms | 9875ms |
| 130.0 | 140.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 130.0 | 140.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 130.0 | 140.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 64 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app2 | ok | 64 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | end-users | ok | 30 | 20000ms | 28000ms | 29800ms |
| 150.0 | 160.0 | app1 | ok | 144 | 2941ms | 7600ms | 9760ms |
| 150.0 | 160.0 | app2 | ok | 49 | 3750ms | 8886ms | 9889ms |
| 150.0 | 160.0 | end-users | ok | 47 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | app1 | ok | 134 | 1500ms | 3759ms | 4876ms |
| 160.0 | 170.0 | app2 | ok | 59 | 6218ms | 9244ms | 9924ms |
| 160.0 | 170.0 | end-users | ok | 60 | 30968ms | 54194ms | 59419ms |
| 170.0 | 180.0 | app1 | ok | 141 | 1829ms | 4217ms | 4922ms |
| 170.0 | 180.0 | app2 | ok | 21 | 6250ms | 9250ms | 9925ms |
| 170.0 | 180.0 | end-users | ok | 19 | 45000ms | 57000ms | 59700ms |
| 180.0 | 190.0 | app1 | ok | 159 | 1255ms | 2304ms | 4006ms |
| 180.0 | 190.0 | app2 | ok | 32 | 8478ms | 22889ms | 29289ms |
| 180.0 | 190.0 | end-users | ok | 33 | 45000ms | 57000ms | 59700ms |
| 190.0 | 200.0 | app1 | ok | 169 | 1271ms | 2316ms | 4155ms |
| 190.0 | 200.0 | app2 | ok | 32 | 12222ms | 26444ms | 29644ms |
| 190.0 | 200.0 | end-users | ok | 33 | 45000ms | 57000ms | 59700ms |
| 200.0 | 210.0 | app1 | ok | 77 | 1558ms | 3625ms | 4863ms |
| 200.0 | 210.0 | app2 | ok | 61 | 5521ms | 16444ms | 28644ms |
| 200.0 | 210.0 | end-users | ok | 67 | 45000ms | 57000ms | 59700ms |
| 210.0 | 221.0 | app1 | ok | 134 | 2466ms | 4729ms | 9043ms |
| 210.0 | 221.0 | app2 | ok | 64 | 4143ms | 8400ms | 9840ms |
| 210.0 | 221.0 | end-users | ok | 114 | 45000ms | 57000ms | 59700ms |
| 221.0 | 231.0 | app1 | ok | 64 | 7500ms | 9500ms | 9950ms |
| 221.0 | 231.0 | app2 | ok | 57 | 3967ms | 8500ms | 9850ms |
| 221.0 | 231.0 | end-users | ok | 3 | 45000ms | 57000ms | 59700ms |
| 231.0 | 241.0 | app1 | ok | 123 | 1683ms | 4008ms | 4901ms |
| 231.0 | 241.0 | app2 | ok | 30 | 3654ms | 8125ms | 9812ms |
| 231.0 | 241.0 | end-users | ok | 30 | 45000ms | 57000ms | 59700ms |
| 241.0 | 251.0 | app1 | ok | 52 | 964ms | 2350ms | 4567ms |
| 241.0 | 251.0 | app2 | ok | 34 | 6600ms | 9320ms | 9932ms |
| 241.0 | 251.0 | end-users | ok | 176 | 33600ms | 54720ms | 59472ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 47 | 20000ms | 28000ms | 29800ms |
| 261.0 | 268.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 268.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 268.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- end-users exceeded the 10% ledger tolerance: cost -19.0%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 3664170 | 182189 | 3846359.0 | 0.0% | 3998820.0 | 4028548.0 | -0.7% | True |
| app2 | 1258290 | 62495 | 1320785.0 | 0.0% | 1356172.0 | 1383280.0 | -2.0% | True |
| end-users | 1683870 | 83976 | 1767846.0 | 0.0% | 1500160.0 | 1851822.0 | -19.0% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2979 | 0 | 0 | 0 (never shed) | 0.00% | 98.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1023 | 0 | 0 | 0 (never shed) | 0.00% | 1.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1369 | 0 | 0 | 0 (never shed) | 0.00% | 1.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5371). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5371 | 0.051ms | 0.121ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 254835 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 2979 | 4276ms | 7934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1023 | 14179ms | 26806ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 1369 | 46695ms | 108299ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5371 | 6375ms | 74094ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: PRIORITY-OK** -- the share verdict above is FAIL, so this is the board's second, independent success criterion (2026-11-10): did the policy nonetheless order tenants by weight? Top-weighted group: `app1` (TTFT p50 4276ms, p95 7934ms, strictly lowest among distinctly-weighted groups: p50=True/p95=True; no rank inversion among any distinctly-weighted pair: True -- this, not raw rank correlation, is what gates the verdict, since a genuine weight tie (e.g. 98/1/1's app2==end-users) makes exact correlation 1.0 unreachable by construction even when ordering is otherwise perfect). Rank correlation 0.87 (1.00 = exact agreement, informational only) shown for reference. Separation from the next distinctly-weighted group: 9903ms against a noise floor of not given (separation check skipped).

**Windowed TTFT/ITL** (27 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 1844ms | 2997ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 1714ms | 2833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2000ms | 4267ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 6188ms | 7819ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 8783ms | 13800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 5917ms | 12500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 3992ms | 5821ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 11121ms | 17250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 18571ms | 28333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 5438ms | 7784ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 12216ms | 14824ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 27500ms | 42750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 3658ms | 5296ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 15588ms | 19559ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 4141ms | 5481ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 18333ms | 28667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 51667ms | 59167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 3935ms | 6288ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 16591ms | 26857ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 57054ms | 112059ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 4141ms | 4988ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 17396ms | 27833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 3770ms | 4891ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 18100ms | 27417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 4123ms | 5692ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 19861ms | 28974ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 4640ms | 6522ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 14700ms | 19466ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 3812ms | 5652ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 14667ms | 23000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 3562ms | 4709ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 18176ms | 27875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 14062ms | 19350ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 61765ms | 114176ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | end-users | ok | 39304ms | 56543ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 6566ms | 9109ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 23750ms | 29375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 4721ms | 5881ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 11875ms | 14688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 5118ms | 7736ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 14375ms | 19638ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app1 | ok | 3786ms | 5369ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app2 | ok | 13100ms | 24833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | end-users | ok | 47368ms | 58737ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app1 | ok | 3723ms | 4977ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app2 | ok | 18690ms | 28500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | end-users | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app1 | ok | 4466ms | 5807ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app2 | ok | 18796ms | 28594ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | end-users | ok | 57321ms | 112333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 221.0 | app1 | ok | 6238ms | 7824ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 221.0 | app2 | ok | 13049ms | 18611ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 221.0 | end-users | ok | 57045ms | 112050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 8429ms | 14355ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 12459ms | 14746ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 55364ms | 109143ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 5643ms | 14138ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 4148ms | 5772ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 11522ms | 14652ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 46534ms | 58653ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 28119ms | 43243ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 268.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 268.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 268.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
