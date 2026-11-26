# Fairness benchmark: full-contention-2x (uni310-l3-r1-f3-98-1-1)

**Verdict: FAIL** (threshold: 10 points)
**Secondary (priority) verdict: PRIORITY-OK** -- see "Per-tenant TTFT / ITL and the priority verdict (UNI-226)" below for detail.
Worker-share vs. weight-share gap (UNI-225): 81.3 points

- app1 deviated -41.8 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58ffc845cf-fl4lv` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T02:51:42Z` |
| Run end | `2026-11-26T02:57:45Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 38 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/38 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 101.50 | 3.1719 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 98.0 | 64 | 2903 | 200=2903 | 4.8 | 8.2 | 3883248.0 | 98.0% | 16.7% | -81.3 | 56.2% | -41.8 | 53.5% | -44.5 | 53.9s | 98.9% | 2903.0 |
| app2 | 1.0 | 64 | 1131 | 000=2, 200=1129 | 13.0 | 20.0 | 1508852.0 | 1.0% | 16.7% | 15.7 | 21.8% | 20.8 | 20.9% | 19.9 | 56.0s | 98.9% | 1131.0 |
| end-users | 1.0 | 256 | 1388 | 200=1388 | 52.3 | 65.1 | 1516096.0 | 1.0% | 66.7% | 65.7 | 21.9% | 20.9 | 25.6% | 24.6 | 56.0s | 98.9% | 1388.0 |
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

**Windows** (37 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 43266.0 | 98.0% | 97.0% | -1.0 |
| 0.0 | 10.0 | app2 | True | False | 1340.0 | 1.0% | 3.0% | 2.0 |
| 0.0 | 10.0 | end-users | True | False | 0.0 | 1.0% | 0.0% | -1.0 |
| 10.0 | 20.0 | app1 | True | False | 36540.0 | 98.0% | 22.9% | -75.1 |
| 10.0 | 20.0 | app2 | True | False | 52690.0 | 1.0% | 33.0% | 32.0 |
| 10.0 | 20.0 | end-users | True | False | 70280.0 | 1.0% | 44.1% | 43.1 |
| 20.0 | 30.0 | app1 | True | False | 97308.0 | 98.0% | 38.7% | -59.3 |
| 20.0 | 30.0 | app2 | True | False | 85050.0 | 1.0% | 33.8% | 32.8 |
| 20.0 | 30.0 | end-users | True | False | 69022.0 | 1.0% | 27.5% | 26.5 |
| 30.0 | 40.0 | app1 | True | False | 140772.0 | 98.0% | 47.7% | -50.3 |
| 30.0 | 40.0 | app2 | True | False | 75728.0 | 1.0% | 25.7% | 24.7 |
| 30.0 | 40.0 | end-users | True | False | 78376.0 | 1.0% | 26.6% | 25.6 |
| 40.0 | 50.0 | app1 | True | False | 147484.0 | 98.0% | 50.1% | -47.9 |
| 40.0 | 50.0 | app2 | True | False | 70252.0 | 1.0% | 23.8% | 22.8 |
| 40.0 | 50.0 | end-users | True | False | 76936.0 | 1.0% | 26.1% | 25.1 |
| 50.0 | 60.0 | app1 | True | False | 171882.0 | 98.0% | 57.0% | -41.0 |
| 50.0 | 60.0 | app2 | True | False | 70364.0 | 1.0% | 23.3% | 22.3 |
| 50.0 | 60.0 | end-users | True | False | 59518.0 | 1.0% | 19.7% | 18.7 |
| 60.0 | 70.0 | app1 | True | False | 144724.0 | 98.0% | 53.0% | -45.0 |
| 60.0 | 70.0 | app2 | True | False | 64780.0 | 1.0% | 23.7% | 22.7 |
| 60.0 | 70.0 | end-users | True | False | 63528.0 | 1.0% | 23.3% | 22.3 |
| 70.0 | 80.0 | app1 | True | False | 201428.0 | 98.0% | 65.3% | -32.7 |
| 70.0 | 80.0 | app2 | True | False | 51366.0 | 1.0% | 16.7% | 15.7 |
| 70.0 | 80.0 | end-users | True | False | 55574.0 | 1.0% | 18.0% | 17.0 |
| 80.0 | 90.0 | app1 | True | False | 154236.0 | 98.0% | 51.9% | -46.1 |
| 80.0 | 90.0 | app2 | True | False | 72992.0 | 1.0% | 24.5% | 23.5 |
| 80.0 | 90.0 | end-users | True | False | 70200.0 | 1.0% | 23.6% | 22.6 |
| 90.0 | 100.0 | app1 | True | False | 111086.0 | 98.0% | 48.0% | -50.0 |
| 90.0 | 100.0 | app2 | True | False | 59484.0 | 1.0% | 25.7% | 24.7 |
| 90.0 | 100.0 | end-users | True | False | 60830.0 | 1.0% | 26.3% | 25.3 |
| 100.0 | 110.0 | app1 | True | False | 150164.0 | 98.0% | 49.3% | -48.7 |
| 100.0 | 110.0 | app2 | True | False | 75834.0 | 1.0% | 24.9% | 23.9 |
| 100.0 | 110.0 | end-users | True | False | 78476.0 | 1.0% | 25.8% | 24.8 |
| 110.0 | 120.0 | app1 | True | False | 154126.0 | 98.0% | 51.8% | -46.2 |
| 110.0 | 120.0 | app2 | True | False | 73046.0 | 1.0% | 24.5% | 23.5 |
| 110.0 | 120.0 | end-users | True | False | 70404.0 | 1.0% | 23.7% | 22.7 |
| 120.0 | 130.0 | app1 | True | False | 192092.0 | 98.0% | 66.4% | -31.6 |
| 120.0 | 130.0 | app2 | True | False | 50064.0 | 1.0% | 17.3% | 16.3 |
| 120.0 | 130.0 | end-users | True | False | 47350.0 | 1.0% | 16.4% | 15.4 |
| 130.0 | 140.0 | app1 | True | False | 162304.0 | 98.0% | 53.4% | -44.6 |
| 130.0 | 140.0 | app2 | True | False | 68918.0 | 1.0% | 22.7% | 21.7 |
| 130.0 | 140.0 | end-users | True | False | 72924.0 | 1.0% | 24.0% | 23.0 |
| 140.0 | 150.0 | app1 | True | False | 220350.0 | 98.0% | 72.8% | -25.2 |
| 140.0 | 150.0 | app2 | True | False | 41924.0 | 1.0% | 13.8% | 12.8 |
| 140.0 | 150.0 | end-users | True | False | 40582.0 | 1.0% | 13.4% | 12.4 |
| 150.0 | 160.0 | app1 | True | False | 220388.0 | 98.0% | 72.4% | -25.6 |
| 150.0 | 160.0 | app2 | True | False | 41962.0 | 1.0% | 13.8% | 12.8 |
| 150.0 | 160.0 | end-users | True | False | 41948.0 | 1.0% | 13.8% | 12.8 |
| 160.0 | 170.0 | app1 | True | False | 189348.0 | 98.0% | 64.8% | -33.2 |
| 160.0 | 170.0 | app2 | True | False | 51302.0 | 1.0% | 17.6% | 16.6 |
| 160.0 | 170.0 | end-users | True | False | 51426.0 | 1.0% | 17.6% | 16.6 |
| 170.0 | 180.0 | app1 | True | False | 187998.0 | 98.0% | 61.8% | -36.2 |
| 170.0 | 180.0 | app2 | True | False | 58140.0 | 1.0% | 19.1% | 18.1 |
| 170.0 | 180.0 | end-users | True | False | 58266.0 | 1.0% | 19.1% | 18.1 |
| 180.0 | 191.0 | app1 | True | False | 167724.0 | 98.0% | 54.9% | -43.1 |
| 180.0 | 191.0 | app2 | True | False | 68920.0 | 1.0% | 22.5% | 21.5 |
| 180.0 | 191.0 | end-users | True | False | 69106.0 | 1.0% | 22.6% | 21.6 |
| 191.0 | 201.0 | app1 | True | False | 200220.0 | 98.0% | 66.4% | -31.6 |
| 191.0 | 201.0 | app2 | True | False | 48688.0 | 1.0% | 16.1% | 15.1 |
| 191.0 | 201.0 | end-users | True | False | 52736.0 | 1.0% | 17.5% | 16.5 |
| 201.0 | 211.0 | app1 | True | False | 205746.0 | 98.0% | 67.6% | -30.4 |
| 201.0 | 211.0 | app2 | True | False | 52804.0 | 1.0% | 17.3% | 16.3 |
| 201.0 | 211.0 | end-users | True | False | 45950.0 | 1.0% | 15.1% | 14.1 |
| 211.0 | 221.0 | app1 | True | False | 123052.0 | 98.0% | 44.8% | -53.2 |
| 211.0 | 221.0 | app2 | True | False | 66210.0 | 1.0% | 24.1% | 23.1 |
| 211.0 | 221.0 | end-users | True | False | 85264.0 | 1.0% | 31.1% | 30.1 |
| 221.0 | 231.0 | app1 | True | False | 221678.0 | 98.0% | 72.2% | -25.8 |
| 221.0 | 231.0 | app2 | True | False | 50026.0 | 1.0% | 16.3% | 15.3 |
| 221.0 | 231.0 | end-users | True | False | 35156.0 | 1.0% | 11.5% | 10.5 |
| 231.0 | 241.0 | app1 | True | False | 142004.0 | 98.0% | 51.0% | -47.0 |
| 231.0 | 241.0 | app2 | True | False | 69064.0 | 1.0% | 24.8% | 23.8 |
| 231.0 | 241.0 | end-users | True | False | 67620.0 | 1.0% | 24.3% | 23.3 |
| 241.0 | 251.0 | app1 | False | n/a | 97328.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 73036.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 72990.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 14868.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | n/a | 21634.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 363.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 363.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 363.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 58 | 50ms | 485ms | 942ms |
| 0.0 | 10.0 | app2 | ok | 52 | 127ms | 740ms | 974ms |
| 0.0 | 10.0 | end-users | ok | 170 | 280ms | 793ms | 979ms |
| 10.0 | 20.0 | app1 | ok | 64 | 9706ms | 25733ms | 29573ms |
| 10.0 | 20.0 | app2 | ok | 64 | 7500ms | 25077ms | 29508ms |
| 10.0 | 20.0 | end-users | ok | 43 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app1 | ok | 64 | 6000ms | 9200ms | 9920ms |
| 20.0 | 30.0 | app2 | ok | 36 | 1618ms | 4333ms | 9100ms |
| 20.0 | 30.0 | end-users | ok | 13 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | app1 | ok | 114 | 3113ms | 6647ms | 9665ms |
| 30.0 | 40.0 | app2 | ok | 72 | 3364ms | 4673ms | 4967ms |
| 30.0 | 40.0 | end-users | ok | 68 | 21148ms | 30857ms | 57086ms |
| 40.0 | 50.0 | app1 | ok | 130 | 1980ms | 4323ms | 4932ms |
| 40.0 | 50.0 | app2 | ok | 64 | 3667ms | 8000ms | 9800ms |
| 40.0 | 50.0 | end-users | ok | 64 | 45000ms | 57000ms | 59700ms |
| 50.0 | 60.0 | app1 | ok | 127 | 1804ms | 4320ms | 4984ms |
| 50.0 | 60.0 | app2 | ok | 29 | 6705ms | 9341ms | 9934ms |
| 50.0 | 60.0 | end-users | ok | 21 | 45000ms | 57000ms | 59700ms |
| 60.0 | 70.0 | app1 | ok | 104 | 3061ms | 6286ms | 9629ms |
| 60.0 | 70.0 | app2 | ok | 58 | 4375ms | 8885ms | 9888ms |
| 60.0 | 70.0 | end-users | ok | 58 | 45000ms | 57000ms | 59700ms |
| 70.0 | 80.0 | app1 | ok | 127 | 1474ms | 3132ms | 4813ms |
| 70.0 | 80.0 | app2 | ok | 13 | 7500ms | 9500ms | 9950ms |
| 70.0 | 80.0 | end-users | ok | 14 | 45000ms | 57000ms | 59700ms |
| 80.0 | 90.0 | app1 | ok | 123 | 2365ms | 4470ms | 4947ms |
| 80.0 | 90.0 | app2 | ok | 58 | 5735ms | 9147ms | 9915ms |
| 80.0 | 90.0 | end-users | ok | 57 | 45000ms | 57000ms | 59700ms |
| 90.0 | 100.0 | app1 | ok | 96 | 4010ms | 8345ms | 9834ms |
| 90.0 | 100.0 | app2 | ok | 72 | 2935ms | 7882ms | 9788ms |
| 90.0 | 100.0 | end-users | ok | 79 | 45000ms | 57000ms | 59700ms |
| 100.0 | 110.0 | app1 | ok | 58 | 2734ms | 4547ms | 4955ms |
| 100.0 | 110.0 | app2 | ok | 29 | 2768ms | 4839ms | 9275ms |
| 100.0 | 110.0 | end-users | ok | 41 | 45000ms | 57000ms | 59700ms |
| 110.0 | 120.0 | app1 | ok | 150 | 2404ms | 4659ms | 8750ms |
| 110.0 | 120.0 | app2 | ok | 61 | 4602ms | 8870ms | 9887ms |
| 110.0 | 120.0 | end-users | ok | 41 | 45000ms | 57000ms | 59700ms |
| 120.0 | 130.0 | app1 | ok | 134 | 1508ms | 3712ms | 4871ms |
| 120.0 | 130.0 | app2 | ok | 30 | 7500ms | 9500ms | 9950ms |
| 120.0 | 130.0 | end-users | ok | 31 | 45000ms | 57000ms | 59700ms |
| 130.0 | 140.0 | app1 | ok | 138 | 1820ms | 4138ms | 4914ms |
| 130.0 | 140.0 | app2 | ok | 47 | 6328ms | 9266ms | 9927ms |
| 130.0 | 140.0 | end-users | ok | 48 | 45000ms | 57000ms | 59700ms |
| 140.0 | 150.0 | app1 | ok | 153 | 1266ms | 2474ms | 4727ms |
| 140.0 | 150.0 | app2 | ok | 34 | 7258ms | 9452ms | 9945ms |
| 140.0 | 150.0 | end-users | ok | 34 | 45000ms | 57000ms | 59700ms |
| 150.0 | 160.0 | app1 | ok | 171 | 1286ms | 2344ms | 4389ms |
| 150.0 | 160.0 | app2 | ok | 42 | 9038ms | 24750ms | 29475ms |
| 150.0 | 160.0 | end-users | ok | 42 | 45000ms | 57000ms | 59700ms |
| 160.0 | 170.0 | app1 | ok | 123 | 1553ms | 3663ms | 4866ms |
| 160.0 | 170.0 | app2 | ok | 45 | 6797ms | 9609ms | 25500ms |
| 160.0 | 170.0 | end-users | ok | 44 | 45000ms | 57000ms | 59700ms |
| 170.0 | 180.0 | app1 | ok | 172 | 1416ms | 3346ms | 4835ms |
| 170.0 | 180.0 | app2 | ok | 52 | 7045ms | 9409ms | 9941ms |
| 170.0 | 180.0 | end-users | ok | 53 | 45588ms | 58059ms | 60000ms |
| 180.0 | 191.0 | app1 | ok | 109 | 1942ms | 4319ms | 4932ms |
| 180.0 | 191.0 | app2 | ok | 34 | 5526ms | 9105ms | 9911ms |
| 180.0 | 191.0 | end-users | ok | 34 | 45455ms | 57818ms | 60000ms |
| 191.0 | 201.0 | app1 | ok | 141 | 1462ms | 2446ms | 4680ms |
| 191.0 | 201.0 | app2 | ok | 22 | 7500ms | 9500ms | 9950ms |
| 191.0 | 201.0 | end-users | ok | 21 | 45000ms | 57000ms | 59700ms |
| 201.0 | 211.0 | app1 | ok | 116 | 1311ms | 3188ms | 4819ms |
| 201.0 | 211.0 | app2 | ok | 61 | 6438ms | 9488ms | 23900ms |
| 201.0 | 211.0 | end-users | ok | 73 | 45870ms | 58565ms | 60000ms |
| 211.0 | 221.0 | app1 | ok | 129 | 2786ms | 7068ms | 9707ms |
| 211.0 | 221.0 | app2 | ok | 44 | 5600ms | 9120ms | 9912ms |
| 211.0 | 221.0 | end-users | ok | 33 | 45000ms | 57000ms | 59700ms |
| 221.0 | 231.0 | app1 | ok | 168 | 1395ms | 2456ms | 4700ms |
| 221.0 | 231.0 | app2 | ok | 49 | 6938ms | 9388ms | 9939ms |
| 221.0 | 231.0 | end-users | ok | 48 | 45000ms | 57000ms | 59700ms |
| 231.0 | 241.0 | app1 | ok | 120 | 2941ms | 4706ms | 8500ms |
| 231.0 | 241.0 | app2 | ok | 33 | 3295ms | 8167ms | 9817ms |
| 231.0 | 241.0 | end-users | ok | 34 | 45000ms | 57000ms | 59700ms |
| 241.0 | 251.0 | app1 | ok | 14 | 1750ms | 2350ms | 2485ms |
| 241.0 | 251.0 | app2 | ok | 30 | 4423ms | 8750ms | 9875ms |
| 241.0 | 251.0 | end-users | ok | 154 | 41066ms | 56213ms | 59621ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 70 | 20000ms | 28000ms | 29800ms |
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
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 363.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 363.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 363.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- end-users exceeded the 10% ledger tolerance: cost -19.2%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 3570690 | 177882 | 3748572.0 | 0.0% | 3883248.0 | 3926454.0 | -1.1% | True |
| app2 | 1388670 | 68886 | 1457556.0 | 0.0% | 1508852.0 | 1526442.0 | -1.2% | True |
| end-users | 1707240 | 84986 | 1792226.0 | 0.0% | 1516096.0 | 1877212.0 | -19.2% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2903 | 0 | 0 | 0 (never shed) | 0.00% | 98.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1131 | 0 | 0 | 0 (never shed) | 0.00% | 1.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1388 | 0 | 0 | 0 (never shed) | 0.00% | 1.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5422). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5422 | 0.051ms | 0.121ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 342580 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 2903 | 4883ms | 8551ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1129 | 13031ms | 20096ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 1388 | 49576ms | 105338ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5420 | 7522ms | 62746ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: PRIORITY-OK** -- the share verdict above is FAIL, so this is the board's second, independent success criterion (2026-11-10): did the policy nonetheless order tenants by weight? Top-weighted group: `app1` (TTFT p50 4883ms, p95 8551ms, strictly lowest among distinctly-weighted groups: p50=True/p95=True; no rank inversion among any distinctly-weighted pair: True -- this, not raw rank correlation, is what gates the verdict, since a genuine weight tie (e.g. 98/1/1's app2==end-users) makes exact correlation 1.0 unreachable by construction even when ordering is otherwise perfect). Rank correlation 0.87 (1.00 = exact agreement, informational only) shown for reference. Separation from the next distinctly-weighted group: 8148ms against a noise floor of not given (separation check skipped).

**Windowed TTFT/ITL** (37 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2100ms | 3796ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 1625ms | 2300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2056ms | 4592ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 11957ms | 14696ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 7786ms | 9888ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 11154ms | 14615ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 10549ms | 14555ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 14257ms | 19394ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 17578ms | 27450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 6250ms | 9669ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 9514ms | 14263ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 29355ms | 43389ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 5887ms | 7771ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 4979ms | 7702ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 12234ms | 14723ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 37674ms | 44581ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 4350ms | 7465ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 12558ms | 18000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 51402ms | 59140ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 4843ms | 7734ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 12794ms | 17625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 4652ms | 5827ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 14821ms | 19854ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 52647ms | 59529ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 6719ms | 8340ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 12558ms | 14860ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 52670ms | 59574ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 6093ms | 9253ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 5822ms | 7755ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 4784ms | 5887ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 4514ms | 5769ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 15096ms | 19510ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 4266ms | 7373ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 13100ms | 27417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | end-users | ok | 54375ms | 105000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 3776ms | 4869ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 18452ms | 28278ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | end-users | ok | 54688ms | 106714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 4600ms | 5825ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 18913ms | 28643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | end-users | ok | 72500ms | 115250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 4330ms | 5839ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 13707ms | 19558ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | end-users | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app1 | ok | 4741ms | 7612ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app2 | ok | 13643ms | 27450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | end-users | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 4308ms | 6150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 12727ms | 17000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 4356ms | 5738ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 16711ms | 27214ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 7000ms | 9671ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 12905ms | 18639ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 73902ms | 115390ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 3760ms | 5544ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 12803ms | 17688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 58000ms | 112909ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 5944ms | 7798ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 15900ms | 24900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 58393ms | 113182ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 5402ms | 5988ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 12547ms | 14840ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 51000ms | 59871ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 32561ms | 52125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 321.0 | 331.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 363.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 363.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 363.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
