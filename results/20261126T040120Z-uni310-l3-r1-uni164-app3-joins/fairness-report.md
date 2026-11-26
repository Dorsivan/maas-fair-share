# Fairness benchmark: app3-joins-at-saturation (uni310-l3-r1-uni164-app3-joins)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-6bdbdf5bf6-6q965` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T04:02:30Z` |
| Run end | `2026-11-26T04:09:56Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 46 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/46 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 85.00 | 2.6562 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 30.0 | 96 | 2877 | 200=2877 | 6.1 | 16.3 | 3745224.0 | 51.8% | 37.5% | 7.5 | 52.9% | 1.1 | 52.4% | 22.4 | 41.3s | 98.9% | 2877.0 |
| app2 | 10.0 | 32 | 959 | 200=959 | 6.1 | 16.1 | 1238356.0 | 17.3% | 12.5% | 2.5 | 17.5% | 0.2 | 17.5% | 7.5 | 41.3s | 98.9% | 959.0 |
| end-users | 60.0 | 128 | 1650 | 000=1, 200=1649 | 9.6 | 12.4 | 2227782.0 | 31.0% | 50.0% | -10.0 | 29.6% | -1.4 | 30.1% | -29.9 | 38.7s | 98.9% | 1650.0 |
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
| 120.0 | 130.0 | 10.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (45 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 4064.0 | 75.0% | 75.0% | -0.0 |
| 0.0 | 10.0 | app2 | True | False | 1358.0 | 25.0% | 25.0% | 0.0 |
| 0.0 | 10.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | True | False | 213784.0 | 75.0% | 75.6% | 0.6 |
| 10.0 | 20.0 | app2 | True | False | 68850.0 | 25.0% | 24.4% | -0.6 |
| 10.0 | 20.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | True | False | 226012.0 | 75.0% | 74.9% | -0.1 |
| 20.0 | 30.0 | app2 | True | False | 75584.0 | 25.0% | 25.1% | 0.1 |
| 20.0 | 30.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | True | False | 228432.0 | 75.0% | 75.8% | 0.8 |
| 30.0 | 40.0 | app2 | True | False | 72924.0 | 25.0% | 24.2% | -0.8 |
| 30.0 | 40.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | True | False | 224498.0 | 75.0% | 75.1% | 0.1 |
| 40.0 | 50.0 | app2 | True | False | 74358.0 | 25.0% | 24.9% | -0.1 |
| 40.0 | 50.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | True | False | 228476.0 | 75.0% | 75.1% | 0.1 |
| 50.0 | 60.0 | app2 | True | False | 75740.0 | 25.0% | 24.9% | -0.1 |
| 50.0 | 60.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | True | False | 221832.0 | 75.0% | 74.6% | -0.4 |
| 60.0 | 70.0 | app2 | True | False | 75666.0 | 25.0% | 25.4% | 0.4 |
| 60.0 | 70.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | True | False | 222018.0 | 75.0% | 75.6% | 0.6 |
| 70.0 | 80.0 | app2 | True | False | 71726.0 | 25.0% | 24.4% | -0.6 |
| 70.0 | 80.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | True | False | 227256.0 | 75.0% | 75.4% | 0.4 |
| 80.0 | 90.0 | app2 | True | False | 74302.0 | 25.0% | 24.6% | -0.4 |
| 80.0 | 90.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app1 | True | False | 227274.0 | 75.0% | 75.3% | 0.3 |
| 90.0 | 100.0 | app2 | True | False | 74434.0 | 25.0% | 24.7% | -0.3 |
| 90.0 | 100.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 100.0 | 110.0 | app1 | True | False | 221824.0 | 75.0% | 74.5% | -0.5 |
| 100.0 | 110.0 | app2 | True | False | 75812.0 | 25.0% | 25.5% | 0.5 |
| 100.0 | 110.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app1 | True | False | 223292.0 | 75.0% | 75.0% | 0.0 |
| 110.0 | 120.0 | app2 | True | False | 74402.0 | 25.0% | 25.0% | -0.0 |
| 110.0 | 120.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | True | False | 179764.0 | 30.0% | 59.1% | 29.1 |
| 120.0 | 130.0 | app2 | True | False | 55552.0 | 10.0% | 18.3% | 8.3 |
| 120.0 | 130.0 | end-users | True | False | 68882.0 | 60.0% | 22.6% | -37.4 |
| 130.0 | 140.0 | app1 | True | False | 73068.0 | 30.0% | 24.1% | -5.9 |
| 130.0 | 140.0 | app2 | True | False | 28392.0 | 10.0% | 9.4% | -0.6 |
| 130.0 | 140.0 | end-users | True | False | 201462.0 | 60.0% | 66.5% | 6.5 |
| 140.0 | 150.0 | app1 | True | False | 83776.0 | 30.0% | 30.4% | 0.4 |
| 140.0 | 150.0 | app2 | True | False | 25698.0 | 10.0% | 9.3% | -0.7 |
| 140.0 | 150.0 | end-users | True | False | 166432.0 | 60.0% | 60.3% | 0.3 |
| 150.0 | 160.0 | app1 | True | False | 91902.0 | 30.0% | 30.2% | 0.2 |
| 150.0 | 160.0 | app2 | True | False | 29700.0 | 10.0% | 9.8% | -0.2 |
| 150.0 | 160.0 | end-users | True | False | 182652.0 | 60.0% | 60.0% | 0.0 |
| 160.0 | 170.0 | app1 | True | False | 77120.0 | 30.0% | 29.4% | -0.6 |
| 160.0 | 170.0 | app2 | True | False | 28382.0 | 10.0% | 10.8% | 0.8 |
| 160.0 | 170.0 | end-users | True | False | 156816.0 | 60.0% | 59.8% | -0.2 |
| 170.0 | 180.0 | app1 | True | False | 71734.0 | 30.0% | 29.8% | -0.2 |
| 170.0 | 180.0 | app2 | True | False | 24318.0 | 10.0% | 10.1% | 0.1 |
| 170.0 | 180.0 | end-users | True | False | 144674.0 | 60.0% | 60.1% | 0.1 |
| 180.0 | 190.0 | app1 | True | False | 87864.0 | 30.0% | 29.9% | -0.1 |
| 180.0 | 190.0 | app2 | True | False | 29734.0 | 10.0% | 10.1% | 0.1 |
| 180.0 | 190.0 | end-users | True | False | 176016.0 | 60.0% | 59.9% | -0.1 |
| 190.0 | 200.0 | app1 | True | False | 92020.0 | 30.0% | 30.4% | 0.4 |
| 190.0 | 200.0 | app2 | True | False | 29714.0 | 10.0% | 9.8% | -0.2 |
| 190.0 | 200.0 | end-users | True | False | 181350.0 | 60.0% | 59.8% | -0.2 |
| 200.0 | 211.0 | app1 | True | False | 91960.0 | 30.0% | 30.4% | 0.4 |
| 200.0 | 211.0 | app2 | True | False | 29682.0 | 10.0% | 9.8% | -0.2 |
| 200.0 | 211.0 | end-users | True | False | 181272.0 | 60.0% | 59.8% | -0.2 |
| 211.0 | 221.0 | app1 | True | False | 89220.0 | 30.0% | 29.1% | -0.9 |
| 211.0 | 221.0 | app2 | True | False | 32462.0 | 10.0% | 10.6% | 0.6 |
| 211.0 | 221.0 | end-users | True | False | 185108.0 | 60.0% | 60.3% | 0.3 |
| 221.0 | 231.0 | app1 | True | False | 93230.0 | 30.0% | 30.8% | 0.8 |
| 221.0 | 231.0 | app2 | True | False | 27058.0 | 10.0% | 8.9% | -1.1 |
| 221.0 | 231.0 | end-users | True | False | 182688.0 | 60.0% | 60.3% | 0.3 |
| 231.0 | 241.0 | app1 | True | False | 90614.0 | 30.0% | 29.8% | -0.2 |
| 231.0 | 241.0 | app2 | True | False | 32434.0 | 10.0% | 10.7% | 0.7 |
| 231.0 | 241.0 | end-users | True | False | 181224.0 | 60.0% | 59.6% | -0.4 |
| 241.0 | 251.0 | app1 | False | n/a | 89268.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 29752.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 177198.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 64922.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 20322.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | n/a | 42008.0 | n/a | n/a | n/a |
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
| 361.0 | 371.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 441.0 | 446.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 441.0 | 446.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 441.0 | 446.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 156 | 0ms | 1200ms | 2370ms |
| 0.0 | 10.0 | app2 | ok | 53 | 0ms | 1705ms | 2420ms |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 151 | 1136ms | 2227ms | 2473ms |
| 10.0 | 20.0 | app2 | ok | 49 | 1030ms | 2206ms | 2471ms |
| 10.0 | 20.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 185 | 1084ms | 2217ms | 2472ms |
| 20.0 | 30.0 | app2 | ok | 62 | 1000ms | 2200ms | 2470ms |
| 20.0 | 30.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 187 | 1024ms | 2205ms | 2470ms |
| 30.0 | 40.0 | app2 | ok | 63 | 1150ms | 2230ms | 2473ms |
| 30.0 | 40.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 147 | 1010ms | 2202ms | 2470ms |
| 40.0 | 50.0 | app2 | ok | 49 | 1139ms | 2228ms | 2473ms |
| 40.0 | 50.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 185 | 1039ms | 2208ms | 2471ms |
| 50.0 | 60.0 | app2 | ok | 62 | 1047ms | 2209ms | 2471ms |
| 50.0 | 60.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 151 | 1010ms | 2202ms | 2470ms |
| 60.0 | 70.0 | app2 | ok | 50 | 857ms | 2143ms | 2464ms |
| 60.0 | 70.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 184 | 1106ms | 2221ms | 2472ms |
| 70.0 | 80.0 | app2 | ok | 63 | 1188ms | 2238ms | 2474ms |
| 70.0 | 80.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 151 | 1048ms | 2210ms | 2471ms |
| 80.0 | 90.0 | app2 | ok | 48 | 1000ms | 2200ms | 2470ms |
| 80.0 | 90.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 185 | 1112ms | 2222ms | 2472ms |
| 90.0 | 100.0 | app2 | ok | 62 | 1132ms | 2226ms | 2473ms |
| 90.0 | 100.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 149 | 1067ms | 2213ms | 2471ms |
| 100.0 | 110.0 | app2 | ok | 50 | 1111ms | 2222ms | 2472ms |
| 100.0 | 110.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 185 | 917ms | 2174ms | 2467ms |
| 110.0 | 120.0 | app2 | ok | 62 | 1047ms | 2209ms | 2471ms |
| 110.0 | 120.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 73 | 1268ms | 2311ms | 8175ms |
| 120.0 | 130.0 | app2 | ok | 23 | 1062ms | 2212ms | 2471ms |
| 120.0 | 130.0 | end-users | ok | 133 | 3153ms | 4631ms | 4963ms |
| 130.0 | 140.0 | app1 | ok | 73 | 8202ms | 20875ms | 29087ms |
| 130.0 | 140.0 | app2 | ok | 26 | 7778ms | 19600ms | 28960ms |
| 130.0 | 140.0 | end-users | ok | 156 | 3810ms | 7214ms | 9721ms |
| 140.0 | 150.0 | app1 | ok | 53 | 8681ms | 23765ms | 29376ms |
| 140.0 | 150.0 | app2 | ok | 17 | 8542ms | 23200ms | 29320ms |
| 140.0 | 150.0 | end-users | ok | 103 | 4736ms | 8880ms | 9888ms |
| 150.0 | 160.0 | app1 | ok | 58 | 9028ms | 24727ms | 29473ms |
| 150.0 | 160.0 | app2 | ok | 19 | 8654ms | 23667ms | 29367ms |
| 150.0 | 160.0 | end-users | ok | 116 | 4359ms | 8474ms | 9847ms |
| 160.0 | 170.0 | app1 | ok | 57 | 8032ms | 18600ms | 28860ms |
| 160.0 | 170.0 | app2 | ok | 20 | 7812ms | 16667ms | 28667ms |
| 160.0 | 170.0 | end-users | ok | 116 | 3690ms | 7680ms | 9768ms |
| 170.0 | 180.0 | app1 | ok | 66 | 8143ms | 23400ms | 29340ms |
| 170.0 | 180.0 | app2 | ok | 22 | 7500ms | 21200ms | 29120ms |
| 170.0 | 180.0 | end-users | ok | 85 | 4866ms | 8963ms | 9896ms |
| 180.0 | 190.0 | app1 | ok | 66 | 16250ms | 27250ms | 29725ms |
| 180.0 | 190.0 | app2 | ok | 21 | 16000ms | 27200ms | 29720ms |
| 180.0 | 190.0 | end-users | ok | 178 | 6292ms | 9258ms | 9926ms |
| 190.0 | 200.0 | app1 | ok | 75 | 7930ms | 16364ms | 28636ms |
| 190.0 | 200.0 | app2 | ok | 26 | 7955ms | 17000ms | 28700ms |
| 190.0 | 200.0 | end-users | ok | 149 | 4420ms | 8567ms | 9857ms |
| 200.0 | 211.0 | app1 | ok | 54 | 8375ms | 22286ms | 29229ms |
| 200.0 | 211.0 | app2 | ok | 17 | 8269ms | 21500ms | 29150ms |
| 200.0 | 211.0 | end-users | ok | 105 | 4274ms | 8306ms | 9831ms |
| 211.0 | 221.0 | app1 | ok | 67 | 8418ms | 22556ms | 29256ms |
| 211.0 | 221.0 | app2 | ok | 23 | 8382ms | 22333ms | 29233ms |
| 211.0 | 221.0 | end-users | ok | 139 | 4368ms | 8489ms | 9849ms |
| 221.0 | 231.0 | app1 | ok | 70 | 8571ms | 23333ms | 29333ms |
| 221.0 | 231.0 | app2 | ok | 23 | 8026ms | 18500ms | 28850ms |
| 221.0 | 231.0 | end-users | ok | 138 | 4417ms | 8562ms | 9856ms |
| 231.0 | 241.0 | app1 | ok | 58 | 8085ms | 19455ms | 28945ms |
| 231.0 | 241.0 | app2 | ok | 20 | 7812ms | 16667ms | 28667ms |
| 231.0 | 241.0 | end-users | ok | 117 | 3691ms | 7660ms | 9766ms |
| 241.0 | 251.0 | app1 | ok | 91 | 8160ms | 20421ms | 29042ms |
| 241.0 | 251.0 | app2 | ok | 29 | 8021ms | 18400ms | 28840ms |
| 241.0 | 251.0 | end-users | ok | 115 | 3819ms | 8203ms | 9820ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 446.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 446.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 446.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 3538710 | 176322 | 3715032.0 | 0.0% | 3745224.0 | 3891354.0 | -3.8% | True |
| app2 | 1179570 | 58501 | 1238071.0 | 0.0% | 1238356.0 | 1296572.0 | -4.5% | True |
| end-users | 2028270 | 101097 | 2129367.0 | 0.0% | 2227782.0 | 2230464.0 | -0.1% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2877 | 0 | 0 | 0 (never shed) | 0.00% | 30.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 959 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1650 | 0 | 0 | 0 (never shed) | 0.00% | 60.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5486). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5486 | 0.050ms | 0.100ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 420072 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 2877 | 6164ms | 17719ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 959 | 6106ms | 17695ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 1649 | 9472ms | 14329ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5485 | 7554ms | 16720ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (45 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2094ms | 3962ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2062ms | 3938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 5419ms | 7628ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 5550ms | 7705ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 5545ms | 7655ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 5481ms | 7631ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 5623ms | 7698ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 5554ms | 7633ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 5563ms | 7683ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 5554ms | 7644ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 5651ms | 7698ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 5667ms | 7710ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 5653ms | 7710ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 5643ms | 7689ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 5692ms | 7726ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 5537ms | 7633ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 5619ms | 7687ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 5739ms | 7745ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 5655ms | 7718ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 5667ms | 7720ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 5718ms | 7737ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 5667ms | 7733ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 5703ms | 7728ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 5574ms | 7665ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 5939ms | 7942ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 5971ms | 8633ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 4045ms | 5890ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 7877ms | 9840ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 14844ms | 19638ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 15250ms | 19525ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | end-users | ok | 10269ms | 14527ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 14474ms | 19586ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 15000ms | 19500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | end-users | ok | 9500ms | 14266ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 13562ms | 19162ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 13281ms | 18950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | end-users | ok | 9433ms | 14256ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 16768ms | 19677ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 16786ms | 19679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | end-users | ok | 11777ms | 14678ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app1 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app2 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | end-users | ok | 11684ms | 14668ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app1 | ok | 15143ms | 19514ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app2 | ok | 14231ms | 19389ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | end-users | ok | 9714ms | 14402ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 211.0 | app1 | ok | 12982ms | 18455ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 211.0 | app2 | ok | 13235ms | 18900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 211.0 | end-users | ok | 9318ms | 14118ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 13667ms | 19214ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 13333ms | 19000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 9464ms | 14315ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 13026ms | 18562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 13333ms | 19000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 9240ms | 13795ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 13564ms | 19162ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 13750ms | 19250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 9397ms | 14256ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 13929ms | 19312ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 13667ms | 19214ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 9222ms | 14318ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 12927ms | 18286ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 12885ms | 18125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 10156ms | 14516ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 361.0 | 371.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 431.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 431.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 431.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 431.0 | 441.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 431.0 | 441.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 431.0 | 441.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 441.0 | 446.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 441.0 | 446.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 441.0 | 446.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
