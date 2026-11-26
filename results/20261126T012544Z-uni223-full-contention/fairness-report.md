# Fairness benchmark: full-contention (uni223-full-contention)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 6.1 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 6.1 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-76bc77c99b-b97dc` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-26T01:27:13Z` |
| Run end | `2026-11-26T01:34:23Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 44 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/44 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 80.50 | 2.5156 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1129 | 200=1129 | 6.7 | 9.2 | 1487130.0 | 21.1% | 16.7% | -4.4 | 21.0% | -0.1 | 20.9% | -0.1 | 58.6s | 98.9% | 1129.0 |
| app2 | 10.0 | 32 | 580 | 200=580 | 13.8 | 16.4 | 751826.0 | 10.5% | 16.7% | 6.1 | 10.6% | 0.1 | 10.8% | 0.2 | 60.1s | 98.9% | 580.0 |
| end-users | 65.0 | 128 | 3686 | 000=2, 200=3683, 503=1 | 8.3 | 10.6 | 4859380.0 | 68.4% | 66.7% | -1.8 | 68.5% | 0.0 | 68.3% | -0.1 | 60.1s | 98.8% | 3686.0 |
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
| 0.0 | 10.0 | 10.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (43 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 6732.0 | 21.1% | 100.0% | 78.9 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | False | 0.0 | 68.4% | 0.0% | -68.4 |
| 10.0 | 20.0 | app1 | True | False | 68944.0 | 21.1% | 24.1% | 3.0 |
| 10.0 | 20.0 | app2 | True | False | 16214.0 | 10.5% | 5.7% | -4.9 |
| 10.0 | 20.0 | end-users | True | False | 201358.0 | 68.4% | 70.3% | 1.9 |
| 20.0 | 30.0 | app1 | True | False | 64920.0 | 21.1% | 21.2% | 0.2 |
| 20.0 | 30.0 | app2 | True | False | 32512.0 | 10.5% | 10.6% | 0.1 |
| 20.0 | 30.0 | end-users | True | False | 208336.0 | 68.4% | 68.1% | -0.3 |
| 30.0 | 40.0 | app1 | True | False | 59436.0 | 21.1% | 20.3% | -0.7 |
| 30.0 | 40.0 | app2 | True | False | 29740.0 | 10.5% | 10.2% | -0.3 |
| 30.0 | 40.0 | end-users | True | False | 203012.0 | 68.4% | 69.5% | 1.1 |
| 40.0 | 50.0 | app1 | True | False | 63566.0 | 21.1% | 20.7% | -0.3 |
| 40.0 | 50.0 | app2 | True | False | 35124.0 | 10.5% | 11.4% | 0.9 |
| 40.0 | 50.0 | end-users | True | False | 208340.0 | 68.4% | 67.9% | -0.6 |
| 50.0 | 60.0 | app1 | True | False | 66204.0 | 21.1% | 21.5% | 0.4 |
| 50.0 | 60.0 | app2 | True | False | 31128.0 | 10.5% | 10.1% | -0.4 |
| 50.0 | 60.0 | end-users | True | False | 210980.0 | 68.4% | 68.4% | 0.0 |
| 60.0 | 70.0 | app1 | True | False | 64940.0 | 21.1% | 21.3% | 0.3 |
| 60.0 | 70.0 | app2 | True | False | 33820.0 | 10.5% | 11.1% | 0.6 |
| 60.0 | 70.0 | end-users | True | False | 205552.0 | 68.4% | 67.5% | -0.9 |
| 70.0 | 80.0 | app1 | True | False | 66172.0 | 21.1% | 21.4% | 0.3 |
| 70.0 | 80.0 | app2 | True | False | 32434.0 | 10.5% | 10.5% | -0.0 |
| 70.0 | 80.0 | end-users | True | False | 210886.0 | 68.4% | 68.1% | -0.3 |
| 80.0 | 90.0 | app1 | True | False | 63486.0 | 21.1% | 21.0% | -0.1 |
| 80.0 | 90.0 | app2 | True | False | 28428.0 | 10.5% | 9.4% | -1.1 |
| 80.0 | 90.0 | end-users | True | False | 211110.0 | 68.4% | 69.7% | 1.2 |
| 90.0 | 100.0 | app1 | True | False | 68936.0 | 21.1% | 23.0% | 1.9 |
| 90.0 | 100.0 | app2 | True | False | 33708.0 | 10.5% | 11.2% | 0.7 |
| 90.0 | 100.0 | end-users | True | False | 197464.0 | 68.4% | 65.8% | -2.6 |
| 100.0 | 110.0 | app1 | True | False | 54042.0 | 21.1% | 18.5% | -2.6 |
| 100.0 | 110.0 | app2 | True | False | 28400.0 | 10.5% | 9.7% | -0.8 |
| 100.0 | 110.0 | end-users | True | False | 209844.0 | 68.4% | 71.8% | 3.4 |
| 110.0 | 120.0 | app1 | True | False | 64872.0 | 21.1% | 21.2% | 0.2 |
| 110.0 | 120.0 | app2 | True | False | 35164.0 | 10.5% | 11.5% | 1.0 |
| 110.0 | 120.0 | end-users | True | False | 205612.0 | 68.4% | 67.3% | -1.2 |
| 120.0 | 130.0 | app1 | True | False | 56666.0 | 21.1% | 22.1% | 1.0 |
| 120.0 | 130.0 | app2 | True | False | 21610.0 | 10.5% | 8.4% | -2.1 |
| 120.0 | 130.0 | end-users | True | False | 178448.0 | 68.4% | 69.5% | 1.1 |
| 130.0 | 140.0 | app1 | True | False | 56870.0 | 21.1% | 18.8% | -2.3 |
| 130.0 | 140.0 | app2 | True | False | 35202.0 | 10.5% | 11.6% | 1.1 |
| 130.0 | 140.0 | end-users | True | False | 210860.0 | 68.4% | 69.6% | 1.2 |
| 140.0 | 150.0 | app1 | True | False | 66260.0 | 21.1% | 21.7% | 0.6 |
| 140.0 | 150.0 | app2 | True | False | 33784.0 | 10.5% | 11.1% | 0.5 |
| 140.0 | 150.0 | end-users | True | False | 205426.0 | 68.4% | 67.2% | -1.2 |
| 150.0 | 160.0 | app1 | True | False | 63566.0 | 21.1% | 21.3% | 0.2 |
| 150.0 | 160.0 | app2 | True | False | 32526.0 | 10.5% | 10.9% | 0.4 |
| 150.0 | 160.0 | end-users | True | False | 202824.0 | 68.4% | 67.9% | -0.6 |
| 160.0 | 170.0 | app1 | True | False | 58130.0 | 21.1% | 20.8% | -0.3 |
| 160.0 | 170.0 | app2 | True | False | 25662.0 | 10.5% | 9.2% | -1.4 |
| 160.0 | 170.0 | end-users | True | False | 195988.0 | 68.4% | 70.1% | 1.6 |
| 170.0 | 180.0 | app1 | True | False | 60758.0 | 21.1% | 22.2% | 1.2 |
| 170.0 | 180.0 | app2 | True | False | 31098.0 | 10.5% | 11.4% | 0.9 |
| 170.0 | 180.0 | end-users | True | False | 181250.0 | 68.4% | 66.4% | -2.1 |
| 180.0 | 190.0 | app1 | True | False | 59474.0 | 21.1% | 19.8% | -1.2 |
| 180.0 | 190.0 | app2 | True | False | 32436.0 | 10.5% | 10.8% | 0.3 |
| 180.0 | 190.0 | end-users | True | False | 207928.0 | 68.4% | 69.3% | 0.9 |
| 190.0 | 200.0 | app1 | True | False | 56770.0 | 21.1% | 20.0% | -1.1 |
| 190.0 | 200.0 | app2 | True | False | 31164.0 | 10.5% | 11.0% | 0.5 |
| 190.0 | 200.0 | end-users | True | False | 195948.0 | 68.4% | 69.0% | 0.6 |
| 200.0 | 211.0 | app1 | True | False | 62266.0 | 21.1% | 20.3% | -0.8 |
| 200.0 | 211.0 | app2 | True | False | 36524.0 | 10.5% | 11.9% | 1.4 |
| 200.0 | 211.0 | end-users | True | False | 208124.0 | 68.4% | 67.8% | -0.6 |
| 211.0 | 221.0 | app1 | True | False | 60874.0 | 21.1% | 20.9% | -0.1 |
| 211.0 | 221.0 | app2 | True | False | 25718.0 | 10.5% | 8.8% | -1.7 |
| 211.0 | 221.0 | end-users | True | False | 204184.0 | 68.4% | 70.2% | 1.8 |
| 221.0 | 231.0 | app1 | True | False | 60970.0 | 21.1% | 21.0% | -0.1 |
| 221.0 | 231.0 | app2 | True | False | 31048.0 | 10.5% | 10.7% | 0.1 |
| 221.0 | 231.0 | end-users | True | False | 198870.0 | 68.4% | 68.4% | -0.1 |
| 231.0 | 241.0 | app1 | True | False | 66262.0 | 21.1% | 21.3% | 0.3 |
| 231.0 | 241.0 | app2 | True | False | 33720.0 | 10.5% | 10.9% | 0.3 |
| 231.0 | 241.0 | end-users | True | False | 210704.0 | 68.4% | 67.8% | -0.6 |
| 241.0 | 251.0 | app1 | False | n/a | 46014.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 41946.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 186332.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 2716.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
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
| 421.0 | 430.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 430.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 430.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 54 | 1196ms | 3071ms | 4807ms |
| 0.0 | 10.0 | app2 | ok | 27 | 0ms | 5500ms | 9550ms |
| 0.0 | 10.0 | end-users | ok | 175 | 1ms | 3674ms | 4867ms |
| 10.0 | 20.0 | app1 | ok | 39 | 1750ms | 3607ms | 4861ms |
| 10.0 | 20.0 | app2 | ok | 21 | 7763ms | 9974ms | 27900ms |
| 10.0 | 20.0 | end-users | ok | 124 | 3538ms | 4708ms | 4971ms |
| 20.0 | 30.0 | app1 | ok | 55 | 1806ms | 4083ms | 4908ms |
| 20.0 | 30.0 | app2 | ok | 42 | 6379ms | 9276ms | 9928ms |
| 20.0 | 30.0 | end-users | ok | 205 | 3170ms | 4634ms | 4963ms |
| 30.0 | 40.0 | app1 | ok | 44 | 3333ms | 4963ms | 9450ms |
| 30.0 | 40.0 | app2 | ok | 5 | 7500ms | 9500ms | 9950ms |
| 30.0 | 40.0 | end-users | ok | 118 | 3172ms | 4933ms | 9410ms |
| 40.0 | 50.0 | app1 | ok | 53 | 2152ms | 4338ms | 4934ms |
| 40.0 | 50.0 | app2 | ok | 28 | 7800ms | 11333ms | 28133ms |
| 40.0 | 50.0 | end-users | ok | 173 | 3488ms | 4698ms | 4970ms |
| 50.0 | 60.0 | app1 | ok | 41 | 1880ms | 4068ms | 4907ms |
| 50.0 | 60.0 | app2 | ok | 20 | 7500ms | 9500ms | 9950ms |
| 50.0 | 60.0 | end-users | ok | 131 | 3498ms | 4700ms | 4970ms |
| 60.0 | 70.0 | app1 | ok | 41 | 1750ms | 4068ms | 4907ms |
| 60.0 | 70.0 | app2 | ok | 22 | 7619ms | 9714ms | 25600ms |
| 60.0 | 70.0 | end-users | ok | 145 | 3306ms | 4661ms | 4966ms |
| 70.0 | 80.0 | app1 | ok | 55 | 1853ms | 4083ms | 4908ms |
| 70.0 | 80.0 | app2 | ok | 26 | 7600ms | 9680ms | 24800ms |
| 70.0 | 80.0 | end-users | ok | 168 | 3421ms | 4684ms | 4968ms |
| 80.0 | 90.0 | app1 | ok | 54 | 1823ms | 3962ms | 4896ms |
| 80.0 | 90.0 | app2 | ok | 27 | 7596ms | 9673ms | 24600ms |
| 80.0 | 90.0 | end-users | ok | 175 | 3449ms | 4690ms | 4969ms |
| 90.0 | 100.0 | app1 | ok | 37 | 2232ms | 4422ms | 4942ms |
| 90.0 | 100.0 | app2 | ok | 25 | 5227ms | 9773ms | 27500ms |
| 90.0 | 100.0 | end-users | ok | 123 | 2956ms | 4618ms | 4992ms |
| 100.0 | 110.0 | app1 | ok | 38 | 1947ms | 4208ms | 4921ms |
| 100.0 | 110.0 | app2 | ok | 16 | 7500ms | 9786ms | 26800ms |
| 100.0 | 110.0 | end-users | ok | 141 | 2824ms | 4565ms | 4956ms |
| 110.0 | 120.0 | app1 | ok | 62 | 2339ms | 4446ms | 4945ms |
| 110.0 | 120.0 | app2 | ok | 43 | 6417ms | 9283ms | 9928ms |
| 110.0 | 120.0 | end-users | ok | 203 | 3161ms | 4632ms | 4963ms |
| 120.0 | 130.0 | app1 | ok | 25 | 3977ms | 8438ms | 9844ms |
| 120.0 | 130.0 | app2 | ok | 13 | 4250ms | 8700ms | 9870ms |
| 120.0 | 130.0 | end-users | ok | 81 | 3953ms | 8380ms | 9838ms |
| 130.0 | 140.0 | app1 | ok | 58 | 2661ms | 4532ms | 4953ms |
| 130.0 | 140.0 | app2 | ok | 13 | 7500ms | 9500ms | 9950ms |
| 130.0 | 140.0 | end-users | ok | 168 | 3467ms | 4693ms | 4969ms |
| 140.0 | 150.0 | app1 | ok | 45 | 1671ms | 4062ms | 4906ms |
| 140.0 | 150.0 | app2 | ok | 22 | 7500ms | 9500ms | 9950ms |
| 140.0 | 150.0 | end-users | ok | 145 | 3151ms | 4630ms | 4963ms |
| 150.0 | 160.0 | app1 | ok | 46 | 1833ms | 4233ms | 4923ms |
| 150.0 | 160.0 | app2 | ok | 39 | 6518ms | 9304ms | 9930ms |
| 150.0 | 160.0 | end-users | ok | 169 | 3007ms | 4601ms | 4960ms |
| 160.0 | 170.0 | app1 | ok | 41 | 2066ms | 4317ms | 4932ms |
| 160.0 | 170.0 | app2 | ok | 17 | 3958ms | 8583ms | 9858ms |
| 160.0 | 170.0 | end-users | ok | 114 | 3149ms | 4630ms | 4963ms |
| 170.0 | 180.0 | app1 | ok | 59 | 2550ms | 4910ms | 9410ms |
| 170.0 | 180.0 | app2 | ok | 17 | 4375ms | 8786ms | 9879ms |
| 170.0 | 180.0 | end-users | ok | 186 | 3679ms | 7486ms | 9749ms |
| 180.0 | 190.0 | app1 | ok | 38 | 2350ms | 4472ms | 4947ms |
| 180.0 | 190.0 | app2 | ok | 22 | 5769ms | 9154ms | 9915ms |
| 180.0 | 190.0 | end-users | ok | 127 | 2795ms | 4559ms | 4956ms |
| 190.0 | 200.0 | app1 | ok | 52 | 2500ms | 4667ms | 8700ms |
| 190.0 | 200.0 | app2 | ok | 39 | 3750ms | 8607ms | 9861ms |
| 190.0 | 200.0 | end-users | ok | 194 | 3050ms | 4830ms | 9192ms |
| 200.0 | 211.0 | app1 | ok | 45 | 3125ms | 4625ms | 4962ms |
| 200.0 | 211.0 | app2 | ok | 7 | 2125ms | 4417ms | 4942ms |
| 200.0 | 211.0 | end-users | ok | 122 | 2540ms | 4508ms | 4951ms |
| 211.0 | 221.0 | app1 | ok | 34 | 2125ms | 4346ms | 4935ms |
| 211.0 | 221.0 | app2 | ok | 27 | 7300ms | 9460ms | 9946ms |
| 211.0 | 221.0 | end-users | ok | 132 | 2740ms | 4548ms | 4955ms |
| 221.0 | 231.0 | app1 | ok | 50 | 2239ms | 4405ms | 4940ms |
| 221.0 | 231.0 | app2 | ok | 16 | 7857ms | 14000ms | 28400ms |
| 221.0 | 231.0 | end-users | ok | 143 | 3404ms | 4681ms | 4968ms |
| 231.0 | 241.0 | app1 | ok | 55 | 2179ms | 4402ms | 4940ms |
| 231.0 | 241.0 | app2 | ok | 31 | 6125ms | 9225ms | 9922ms |
| 231.0 | 241.0 | end-users | ok | 176 | 3005ms | 4619ms | 4983ms |
| 241.0 | 251.0 | app1 | ok | 8 | 3000ms | 4600ms | 4960ms |
| 241.0 | 251.0 | app2 | ok | 15 | 6875ms | 9375ms | 9938ms |
| 241.0 | 251.0 | end-users | ok | 48 | 3571ms | 4714ms | 4971ms |
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
| 421.0 | 430.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 430.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 430.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1388670 | 68831 | 1457501.0 | 0.0% | 1487130.0 | 1526332.0 | -2.6% | True |
| app2 | 713400 | 35454 | 748854.0 | 0.0% | 751826.0 | 784308.0 | -4.1% | True |
| end-users | 4530090 | 224837 | 4754927.0 | 0.0% | 4859380.0 | 4979764.0 | -2.4% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1129 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | 0.0% | 0.00 |
| app2 | 580 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | 0.0% | 0.00 |
| end-users | 3686 | 0 | 1 | 1 | 0.03% | 68.4% | 100.0% | 1.46 |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5395). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5395 | 0.051ms | 0.123ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 405122 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1129 | 6723ms | 9587ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 580 | 13215ms | 19027ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3683 | 8308ms | 12963ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5392 | 8157ms | 14306ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (43 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2083ms | 4962ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 1950ms | 4675ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 3136ms | 4942ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 6346ms | 8725ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 10208ms | 14521ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 7512ms | 9726ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 6667ms | 7976ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 12609ms | 14957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 8146ms | 9837ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 6556ms | 8500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 13438ms | 19083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 8605ms | 13295ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 6862ms | 9329ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 12955ms | 18375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 8229ms | 12433ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 6760ms | 9456ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 12614ms | 14966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 8211ms | 11100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 6581ms | 7974ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 12604ms | 14948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 8253ms | 9825ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 6469ms | 7847ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 12609ms | 14957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 8217ms | 9908ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 6750ms | 9573ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 12917ms | 18250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 8109ms | 13500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 6833ms | 9779ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 13676ms | 19219ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 8444ms | 13823ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 6400ms | 9000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 13750ms | 19250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 8171ms | 10156ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 6778ms | 11937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 13333ms | 19071ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 8582ms | 13100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 7414ms | 9669ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 13636ms | 19200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 9172ms | 14214ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 7000ms | 9522ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 16905ms | 19690ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 8473ms | 13917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 6767ms | 9183ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 12841ms | 17917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | end-users | ok | 8233ms | 9823ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 6708ms | 9412ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 12609ms | 14957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | end-users | ok | 8225ms | 11875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 6571ms | 9371ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 14318ms | 19406ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | end-users | ok | 8470ms | 13352ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 8000ms | 13357ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 17262ms | 19726ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | end-users | ok | 9654ms | 14422ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app1 | ok | 7107ms | 9938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app2 | ok | 15000ms | 19500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | end-users | ok | 8000ms | 13833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app1 | ok | 6692ms | 8950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app2 | ok | 12738ms | 17125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | end-users | ok | 8210ms | 9821ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 211.0 | app1 | ok | 6625ms | 9329ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 211.0 | app2 | ok | 13375ms | 19036ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 211.0 | end-users | ok | 8613ms | 13460ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 6900ms | 9617ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 12794ms | 17625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 8288ms | 13013ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 6769ms | 12125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 14792ms | 19477ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 8443ms | 13066ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 6846ms | 11937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 13676ms | 19219ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 8408ms | 14000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 6429ms | 7929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 12344ms | 18893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 8405ms | 11550ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 421.0 | 430.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 430.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 430.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
