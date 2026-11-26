# Fairness benchmark: full-contention (uni310-l3-r3-e1-epp-restart)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 6.1 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 6.1 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

**Caveat (UNI-230): a mid-run metrics scrape failed outright, not an EPP restart.** At least one windowed delta below was clamped to zero because its closing `/metrics` scrape itself failed (the benchmark's own recorded curl exit code was nonzero), not because a group's counter genuinely went backwards. A connection-level scrape failure and a real restart produce identical zero-line output once grepped, so this is flagged separately from `epp_restarted_in_windows_but_not_snapshot_pair` rather than folded into it or into `epp_restarted_mid_run`. The affected window's own numbers still undercount real traffic for that window, but this is evidence of a dropped scrape, not of a process restart -- check for corroborating restart evidence (pod identity change, k8s restart events, container restart count) before treating it as one.

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `360` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5d57688bf8-f5ksb` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T08:22:16Z` |
| Run end | `2026-11-26T08:29:24Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 40 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/40 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 72.50 | 2.2656 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1730 | 000=10, 200=1720 | 4.4 | 8.4 | 1292124.0 | 21.1% | 16.7% | -4.4 | 21.0% | -0.1 | 21.3% | 0.2 | 3.8s | 98.9% | 984.0 |
| app2 | 10.0 | 32 | 855 | 000=21, 200=834 | 4.4 | 16.5 | 625204.0 | 10.5% | 16.7% | 6.1 | 10.1% | -0.4 | 10.5% | -0.0 | 3.1s | 98.9% | 492.0 |
| end-users | 65.0 | 128 | 5554 | 000=57, 200=5497 | 4.4 | 10.3 | 4244312.0 | 68.4% | 66.7% | -1.8 | 68.9% | 0.5 | 68.2% | -0.2 | 4.0s | 98.9% | 3197.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events (scheduled):**
- t+120s: epp_delete

**Per-tenant schedule:**
- app1: active 0s-360s, no duty cycle
- app2: active 0s-360s, no duty cycle
- end-users: active 0s-360s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 10.0 | 10.0 |
| 120.0 | 120.0 | 0.0 |
| 360.0 | n/a (never converged in this phase) | n/a |

**Windows** (43 total, a metrics scrape failed mid-window at least once (UNI-230, not a restart)):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 2680.0 | 21.1% | 18.0% | -3.0 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | False | 12190.0 | 68.4% | 82.0% | 13.6 |
| 10.0 | 20.0 | app1 | True | False | 54052.0 | 21.1% | 21.7% | 0.7 |
| 10.0 | 20.0 | app2 | True | False | 13538.0 | 10.5% | 5.4% | -5.1 |
| 10.0 | 20.0 | end-users | True | False | 181354.0 | 68.4% | 72.8% | 4.4 |
| 20.0 | 30.0 | app1 | True | False | 70374.0 | 21.1% | 23.3% | 2.3 |
| 20.0 | 30.0 | app2 | True | False | 29798.0 | 10.5% | 9.9% | -0.7 |
| 20.0 | 30.0 | end-users | True | False | 201592.0 | 68.4% | 66.8% | -1.6 |
| 30.0 | 40.0 | app1 | True | False | 55456.0 | 21.1% | 18.1% | -3.0 |
| 30.0 | 40.0 | app2 | True | False | 32414.0 | 10.5% | 10.6% | 0.0 |
| 30.0 | 40.0 | end-users | True | False | 219028.0 | 68.4% | 71.4% | 2.9 |
| 40.0 | 50.0 | app1 | True | False | 66348.0 | 21.1% | 21.9% | 0.8 |
| 40.0 | 50.0 | app2 | True | False | 32450.0 | 10.5% | 10.7% | 0.2 |
| 40.0 | 50.0 | end-users | True | False | 204212.0 | 68.4% | 67.4% | -1.0 |
| 50.0 | 60.0 | app1 | True | False | 60894.0 | 21.1% | 20.6% | -0.5 |
| 50.0 | 60.0 | app2 | True | False | 25712.0 | 10.5% | 8.7% | -1.8 |
| 50.0 | 60.0 | end-users | True | False | 209700.0 | 68.4% | 70.8% | 2.4 |
| 60.0 | 70.0 | app1 | True | False | 63684.0 | 21.1% | 21.0% | -0.0 |
| 60.0 | 70.0 | app2 | True | False | 31142.0 | 10.5% | 10.3% | -0.3 |
| 60.0 | 70.0 | end-users | True | False | 208362.0 | 68.4% | 68.7% | 0.3 |
| 70.0 | 80.0 | app1 | True | False | 62064.0 | 21.1% | 21.2% | 0.2 |
| 70.0 | 80.0 | app2 | True | False | 37932.0 | 10.5% | 13.0% | 2.5 |
| 70.0 | 80.0 | end-users | True | False | 192178.0 | 68.4% | 65.8% | -2.6 |
| 80.0 | 90.0 | app1 | True | False | 60936.0 | 21.1% | 20.4% | -0.7 |
| 80.0 | 90.0 | app2 | True | False | 32504.0 | 10.5% | 10.9% | 0.3 |
| 80.0 | 90.0 | end-users | True | False | 205590.0 | 68.4% | 68.8% | 0.3 |
| 90.0 | 100.0 | app1 | True | False | 59604.0 | 21.1% | 23.2% | 2.1 |
| 90.0 | 100.0 | app2 | True | False | 20332.0 | 10.5% | 7.9% | -2.6 |
| 90.0 | 100.0 | end-users | True | False | 177180.0 | 68.4% | 68.9% | 0.5 |
| 100.0 | 110.0 | app1 | True | False | 56892.0 | 21.1% | 18.8% | -2.3 |
| 100.0 | 110.0 | app2 | True | False | 36472.0 | 10.5% | 12.0% | 1.5 |
| 100.0 | 110.0 | end-users | True | False | 209552.0 | 68.4% | 69.2% | 0.8 |
| 110.0 | 120.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 110.0 | 120.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 110.0 | 120.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 120.0 | 130.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 120.0 | 130.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 120.0 | 130.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 130.0 | 140.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 130.0 | 140.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 130.0 | 140.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 140.0 | 150.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 140.0 | 150.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 140.0 | 150.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 150.0 | 161.0 | app1 | True | False | 29746.0 | 21.1% | 21.1% | 0.1 |
| 150.0 | 161.0 | app2 | True | False | 13510.0 | 10.5% | 9.6% | -0.9 |
| 150.0 | 161.0 | end-users | True | False | 97498.0 | 68.4% | 69.3% | 0.8 |
| 161.0 | 171.0 | app1 | True | False | 59600.0 | 21.1% | 21.3% | 0.2 |
| 161.0 | 171.0 | app2 | True | False | 27052.0 | 10.5% | 9.7% | -0.9 |
| 161.0 | 171.0 | end-users | True | False | 193374.0 | 68.4% | 69.1% | 0.6 |
| 171.0 | 181.0 | app1 | True | False | 60908.0 | 21.1% | 20.8% | -0.2 |
| 171.0 | 181.0 | app2 | True | False | 29744.0 | 10.5% | 10.2% | -0.4 |
| 171.0 | 181.0 | end-users | True | False | 201790.0 | 68.4% | 69.0% | 0.6 |
| 181.0 | 191.0 | app1 | True | False | 59442.0 | 21.1% | 20.1% | -1.0 |
| 181.0 | 191.0 | app2 | True | False | 31142.0 | 10.5% | 10.5% | -0.0 |
| 181.0 | 191.0 | end-users | True | False | 205556.0 | 68.4% | 69.4% | 1.0 |
| 191.0 | 201.0 | app1 | True | False | 60852.0 | 21.1% | 20.9% | -0.1 |
| 191.0 | 201.0 | app2 | True | False | 28406.0 | 10.5% | 9.8% | -0.8 |
| 191.0 | 201.0 | end-users | True | False | 201488.0 | 68.4% | 69.3% | 0.9 |
| 201.0 | 211.0 | app1 | True | False | 62344.0 | 21.1% | 20.9% | -0.1 |
| 201.0 | 211.0 | app2 | True | False | 32528.0 | 10.5% | 10.9% | 0.4 |
| 201.0 | 211.0 | end-users | True | False | 202878.0 | 68.4% | 68.1% | -0.3 |
| 211.0 | 221.0 | app1 | True | False | 63640.0 | 21.1% | 21.3% | 0.2 |
| 211.0 | 221.0 | app2 | True | False | 29740.0 | 10.5% | 9.9% | -0.6 |
| 211.0 | 221.0 | end-users | True | False | 205568.0 | 68.4% | 68.8% | 0.3 |
| 221.0 | 231.0 | app1 | True | False | 59446.0 | 21.1% | 20.1% | -1.0 |
| 221.0 | 231.0 | app2 | True | False | 32484.0 | 10.5% | 11.0% | 0.4 |
| 221.0 | 231.0 | end-users | True | False | 204192.0 | 68.4% | 69.0% | 0.5 |
| 231.0 | 241.0 | app1 | True | False | 60860.0 | 21.1% | 20.6% | -0.4 |
| 231.0 | 241.0 | app2 | True | False | 29804.0 | 10.5% | 10.1% | -0.4 |
| 231.0 | 241.0 | end-users | True | False | 204234.0 | 68.4% | 69.3% | 0.8 |
| 241.0 | 251.0 | app1 | True | False | 58204.0 | 21.1% | 19.6% | -1.5 |
| 241.0 | 251.0 | app2 | True | False | 31072.0 | 10.5% | 10.4% | -0.1 |
| 241.0 | 251.0 | end-users | True | False | 208174.0 | 68.4% | 70.0% | 1.6 |
| 251.0 | 261.0 | app1 | True | False | 60934.0 | 21.1% | 20.7% | -0.4 |
| 251.0 | 261.0 | app2 | True | False | 27070.0 | 10.5% | 9.2% | -1.3 |
| 251.0 | 261.0 | end-users | True | False | 206762.0 | 68.4% | 70.1% | 1.7 |
| 261.0 | 271.0 | app1 | True | False | 62194.0 | 21.1% | 21.3% | 0.2 |
| 261.0 | 271.0 | app2 | True | False | 28438.0 | 10.5% | 9.7% | -0.8 |
| 261.0 | 271.0 | end-users | True | False | 201696.0 | 68.4% | 69.0% | 0.6 |
| 271.0 | 281.0 | app1 | True | False | 50080.0 | 21.1% | 20.2% | -0.8 |
| 271.0 | 281.0 | app2 | True | False | 24366.0 | 10.5% | 9.8% | -0.7 |
| 271.0 | 281.0 | end-users | True | False | 173104.0 | 68.4% | 69.9% | 1.5 |
| 281.0 | 291.0 | app1 | True | False | 63656.0 | 21.1% | 21.3% | 0.2 |
| 281.0 | 291.0 | app2 | True | False | 31056.0 | 10.5% | 10.4% | -0.1 |
| 281.0 | 291.0 | end-users | True | False | 204192.0 | 68.4% | 68.3% | -0.1 |
| 291.0 | 301.0 | app1 | True | False | 62256.0 | 21.1% | 20.6% | -0.4 |
| 291.0 | 301.0 | app2 | True | False | 32542.0 | 10.5% | 10.8% | 0.3 |
| 291.0 | 301.0 | end-users | True | False | 206744.0 | 68.4% | 68.6% | 0.1 |
| 301.0 | 311.0 | app1 | True | False | 63656.0 | 21.1% | 21.7% | 0.6 |
| 301.0 | 311.0 | app2 | True | False | 28488.0 | 10.5% | 9.7% | -0.8 |
| 301.0 | 311.0 | end-users | True | False | 201598.0 | 68.4% | 68.6% | 0.2 |
| 311.0 | 321.0 | app1 | True | False | 60874.0 | 21.1% | 20.8% | -0.2 |
| 311.0 | 321.0 | app2 | True | False | 28434.0 | 10.5% | 9.7% | -0.8 |
| 311.0 | 321.0 | end-users | True | False | 202820.0 | 68.4% | 69.4% | 1.0 |
| 321.0 | 331.0 | app1 | True | False | 67542.0 | 21.1% | 22.8% | 1.7 |
| 321.0 | 331.0 | app2 | True | False | 28404.0 | 10.5% | 9.6% | -0.9 |
| 321.0 | 331.0 | end-users | True | False | 200298.0 | 68.4% | 67.6% | -0.8 |
| 331.0 | 341.0 | app1 | True | False | 63562.0 | 21.1% | 21.4% | 0.3 |
| 331.0 | 341.0 | app2 | True | False | 31124.0 | 10.5% | 10.5% | -0.1 |
| 331.0 | 341.0 | end-users | True | False | 202846.0 | 68.4% | 68.2% | -0.2 |
| 341.0 | 351.0 | app1 | True | False | 62302.0 | 21.1% | 20.9% | -0.1 |
| 341.0 | 351.0 | app2 | True | False | 32438.0 | 10.5% | 10.9% | 0.4 |
| 341.0 | 351.0 | end-users | True | False | 202818.0 | 68.4% | 68.2% | -0.3 |
| 351.0 | 361.0 | app1 | True | False | 63524.0 | 21.1% | 21.9% | 0.9 |
| 351.0 | 361.0 | app2 | True | False | 28444.0 | 10.5% | 9.8% | -0.7 |
| 351.0 | 361.0 | end-users | True | False | 197696.0 | 68.4% | 68.3% | -0.2 |
| 361.0 | 371.0 | app1 | False | n/a | 36502.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | n/a | 18918.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | False | n/a | 118986.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 412.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 428.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 428.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 428.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`, a metrics scrape failed mid-window at least once (UNI-230, not a restart)):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 46 | 0ms | 3850ms | 4885ms |
| 0.0 | 10.0 | app2 | ok | 28 | 0ms | 0ms | 4ms |
| 0.0 | 10.0 | end-users | ok | 149 | 0ms | 4358ms | 4936ms |
| 10.0 | 20.0 | app1 | ok | 53 | 1775ms | 3896ms | 4890ms |
| 10.0 | 20.0 | app2 | ok | 29 | 7188ms | 9604ms | 24200ms |
| 10.0 | 20.0 | end-users | ok | 200 | 3173ms | 4712ms | 8000ms |
| 20.0 | 30.0 | app1 | ok | 44 | 3103ms | 4621ms | 4962ms |
| 20.0 | 30.0 | app2 | ok | 21 | 4375ms | 8833ms | 9883ms |
| 20.0 | 30.0 | end-users | ok | 110 | 3106ms | 4773ms | 8900ms |
| 30.0 | 40.0 | app1 | ok | 51 | 2110ms | 4329ms | 4933ms |
| 30.0 | 40.0 | app2 | ok | 20 | 7778ms | 10000ms | 28000ms |
| 30.0 | 40.0 | end-users | ok | 172 | 3527ms | 4705ms | 4971ms |
| 40.0 | 50.0 | app1 | ok | 33 | 1838ms | 4083ms | 4908ms |
| 40.0 | 50.0 | app2 | ok | 31 | 6250ms | 9694ms | 26900ms |
| 40.0 | 50.0 | end-users | ok | 123 | 2865ms | 4573ms | 4957ms |
| 50.0 | 60.0 | app1 | ok | 52 | 2250ms | 4409ms | 4941ms |
| 50.0 | 60.0 | app2 | ok | 24 | 6000ms | 9200ms | 9920ms |
| 50.0 | 60.0 | end-users | ok | 178 | 3188ms | 4671ms | 5550ms |
| 60.0 | 70.0 | app1 | ok | 60 | 2190ms | 4457ms | 7000ms |
| 60.0 | 70.0 | app2 | ok | 17 | 7500ms | 9500ms | 9950ms |
| 60.0 | 70.0 | end-users | ok | 179 | 3484ms | 4754ms | 7763ms |
| 70.0 | 80.0 | app1 | ok | 44 | 2385ms | 4476ms | 4948ms |
| 70.0 | 80.0 | app2 | ok | 22 | 5833ms | 9500ms | 25600ms |
| 70.0 | 80.0 | end-users | ok | 130 | 2911ms | 4692ms | 8375ms |
| 80.0 | 90.0 | app1 | ok | 48 | 2043ms | 4294ms | 4929ms |
| 80.0 | 90.0 | app2 | ok | 34 | 7037ms | 9556ms | 23200ms |
| 80.0 | 90.0 | end-users | ok | 180 | 3295ms | 4659ms | 4966ms |
| 90.0 | 100.0 | app1 | ok | 35 | 3698ms | 6500ms | 9650ms |
| 90.0 | 100.0 | app2 | ok | 7 | 8500ms | 23000ms | 29300ms |
| 90.0 | 100.0 | end-users | ok | 91 | 4089ms | 8104ms | 9810ms |
| 100.0 | 110.0 | app1 | ok | 42 | 1955ms | 4192ms | 4919ms |
| 100.0 | 110.0 | app2 | ok | 21 | 8750ms | 24000ms | 29400ms |
| 100.0 | 110.0 | end-users | ok | 137 | 3443ms | 4689ms | 4969ms |
| 110.0 | 120.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 120.0 | 130.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 120.0 | 130.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 130.0 | 140.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 130.0 | 140.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 130.0 | 140.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 140.0 | 150.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 140.0 | 150.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 140.0 | 150.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 150.0 | 161.0 | app1 | ok | 34 | 500ms | 925ms | 1990ms |
| 150.0 | 161.0 | app2 | ok | 15 | 475ms | 958ms | 2275ms |
| 150.0 | 161.0 | end-users | ok | 106 | 531ms | 973ms | 2301ms |
| 161.0 | 171.0 | app1 | ok | 48 | 525ms | 1060ms | 2356ms |
| 161.0 | 171.0 | app2 | ok | 26 | 500ms | 973ms | 2305ms |
| 161.0 | 171.0 | end-users | ok | 157 | 449ms | 913ms | 1911ms |
| 171.0 | 181.0 | app1 | ok | 41 | 482ms | 918ms | 1885ms |
| 171.0 | 181.0 | app2 | ok | 22 | 438ms | 890ms | 989ms |
| 171.0 | 181.0 | end-users | ok | 139 | 561ms | 958ms | 2239ms |
| 181.0 | 191.0 | app1 | ok | 49 | 489ms | 934ms | 2132ms |
| 181.0 | 191.0 | app2 | ok | 23 | 562ms | 946ms | 2155ms |
| 181.0 | 191.0 | end-users | ok | 157 | 525ms | 967ms | 2286ms |
| 191.0 | 201.0 | app1 | ok | 47 | 491ms | 1090ms | 2359ms |
| 191.0 | 201.0 | app2 | ok | 23 | 589ms | 918ms | 992ms |
| 191.0 | 201.0 | end-users | ok | 154 | 514ms | 954ms | 2243ms |
| 201.0 | 211.0 | app1 | ok | 50 | 562ms | 979ms | 2312ms |
| 201.0 | 211.0 | app2 | ok | 26 | 438ms | 1200ms | 2370ms |
| 201.0 | 211.0 | end-users | ok | 160 | 558ms | 974ms | 2300ms |
| 211.0 | 221.0 | app1 | ok | 44 | 575ms | 1180ms | 2368ms |
| 211.0 | 221.0 | app2 | ok | 22 | 625ms | 992ms | 2335ms |
| 211.0 | 221.0 | end-users | ok | 141 | 573ms | 1090ms | 2359ms |
| 221.0 | 231.0 | app1 | ok | 46 | 479ms | 935ms | 2155ms |
| 221.0 | 231.0 | app2 | ok | 24 | 333ms | 922ms | 2140ms |
| 221.0 | 231.0 | end-users | ok | 153 | 489ms | 933ms | 2117ms |
| 231.0 | 241.0 | app1 | ok | 49 | 461ms | 975ms | 2316ms |
| 231.0 | 241.0 | app2 | ok | 24 | 538ms | 908ms | 991ms |
| 231.0 | 241.0 | end-users | ok | 161 | 504ms | 964ms | 2280ms |
| 241.0 | 251.0 | app1 | ok | 49 | 534ms | 980ms | 2316ms |
| 241.0 | 251.0 | app2 | ok | 25 | 469ms | 932ms | 2125ms |
| 241.0 | 251.0 | end-users | ok | 162 | 500ms | 932ms | 2095ms |
| 251.0 | 261.0 | app1 | ok | 44 | 548ms | 967ms | 2280ms |
| 251.0 | 261.0 | app2 | ok | 21 | 575ms | 995ms | 2342ms |
| 251.0 | 261.0 | end-users | ok | 142 | 508ms | 945ms | 2196ms |
| 261.0 | 271.0 | app1 | ok | 49 | 536ms | 1030ms | 2353ms |
| 261.0 | 271.0 | app2 | ok | 25 | 614ms | 1562ms | 2406ms |
| 261.0 | 271.0 | end-users | ok | 156 | 459ms | 962ms | 2287ms |
| 271.0 | 281.0 | app1 | ok | 48 | 483ms | 933ms | 2140ms |
| 271.0 | 281.0 | app2 | ok | 23 | 475ms | 935ms | 2155ms |
| 271.0 | 281.0 | end-users | ok | 155 | 504ms | 966ms | 2289ms |
| 281.0 | 291.0 | app1 | ok | 48 | 523ms | 959ms | 2260ms |
| 281.0 | 291.0 | app2 | ok | 25 | 583ms | 917ms | 992ms |
| 281.0 | 291.0 | end-users | ok | 159 | 563ms | 987ms | 2330ms |
| 291.0 | 301.0 | app1 | ok | 48 | 524ms | 981ms | 2320ms |
| 291.0 | 301.0 | app2 | ok | 24 | 500ms | 980ms | 2320ms |
| 291.0 | 301.0 | end-users | ok | 153 | 504ms | 935ms | 2117ms |
| 301.0 | 311.0 | app1 | ok | 45 | 513ms | 987ms | 2331ms |
| 301.0 | 311.0 | app2 | ok | 23 | 425ms | 981ms | 2327ms |
| 301.0 | 311.0 | end-users | ok | 145 | 541ms | 974ms | 2302ms |
| 311.0 | 321.0 | app1 | ok | 50 | 524ms | 1000ms | 2350ms |
| 311.0 | 321.0 | app2 | ok | 23 | 596ms | 950ms | 2155ms |
| 311.0 | 321.0 | end-users | ok | 165 | 511ms | 1044ms | 2354ms |
| 321.0 | 331.0 | app1 | ok | 46 | 543ms | 943ms | 2155ms |
| 321.0 | 331.0 | app2 | ok | 23 | 531ms | 1637ms | 2414ms |
| 321.0 | 331.0 | end-users | ok | 144 | 565ms | 1300ms | 2380ms |
| 331.0 | 341.0 | app1 | ok | 44 | 553ms | 1180ms | 2368ms |
| 331.0 | 341.0 | app2 | ok | 23 | 525ms | 985ms | 2327ms |
| 331.0 | 341.0 | end-users | ok | 147 | 556ms | 995ms | 2343ms |
| 341.0 | 351.0 | app1 | ok | 51 | 538ms | 1407ms | 2391ms |
| 341.0 | 351.0 | app2 | ok | 25 | 683ms | 1250ms | 2375ms |
| 341.0 | 351.0 | end-users | ok | 165 | 511ms | 989ms | 2335ms |
| 351.0 | 361.0 | app1 | ok | 45 | 544ms | 1536ms | 2404ms |
| 351.0 | 361.0 | app2 | ok | 23 | 614ms | 1350ms | 2385ms |
| 351.0 | 361.0 | end-users | ok | 150 | 527ms | 1477ms | 2398ms |
| 361.0 | 371.0 | app1 | ok | 9 | 688ms | 1825ms | 2432ms |
| 361.0 | 371.0 | app2 | ok | 4 | 500ms | 1900ms | 2440ms |
| 361.0 | 371.0 | end-users | ok | 26 | 679ms | 1525ms | 2402ms |
| 371.0 | 381.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 412.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 428.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 428.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 428.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens -42.8%, cost -44.5%
- app2 exceeded the 10% ledger tolerance: raw tokens -41.0%, cost -44.6%
- end-users exceeded the 10% ledger tolerance: raw tokens -41.8%, cost -42.9%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2115600 | 105871 | 1270834.0 | -42.8% | 1292124.0 | 2327342.0 | -44.5% | False |
| app2 | 1025820 | 51342 | 635474.0 | -41.0% | 625204.0 | 1128504.0 | -44.6% | False |
| end-users | 6761310 | 336990 | 4128255.0 | -41.8% | 4244312.0 | 7435290.0 | -42.9% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1730 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 855 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 5554 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=4673). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 4673 | 0.051ms | 0.117ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 256630 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 984 | 3635ms | 5598ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 492 | 3550ms | 5555ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3197 | 3654ms | 5419ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 4673 | 3640ms | 5483ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (43 windows, a metrics scrape failed mid-window at least once (UNI-230, not a restart)):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2250ms | 5350ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2750ms | 5450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2886ms | 5444ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 6700ms | 8500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 10179ms | 14518ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 7609ms | 9990ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 5870ms | 9575ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 12750ms | 17250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 8594ms | 13567ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 7036ms | 9414ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 13529ms | 19143ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 8145ms | 13650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 5950ms | 9420ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 12727ms | 17000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 8196ms | 13490ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 6417ms | 8850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 15250ms | 19525ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 8230ms | 11771ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 6500ms | 11083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 14107ms | 19361ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 8649ms | 13574ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 6957ms | 9582ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 13182ms | 18833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 8444ms | 14014ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 6348ms | 8850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 8289ms | 9937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 7350ms | 9719ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 13750ms | 19250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 8952ms | 14008ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 7000ms | 9160ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 16625ms | 19662ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 8895ms | 13708ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 161.0 | app1 | ok | 2500ms | 3712ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 161.0 | app2 | ok | 1958ms | 2890ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 161.0 | end-users | ok | 2500ms | 3100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 2635ms | 3827ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 2409ms | 3962ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 2663ms | 3856ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 3062ms | 3944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 2944ms | 3895ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 3048ms | 3991ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 2760ms | 3865ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 2900ms | 3891ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 2980ms | 3898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 2938ms | 3893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 2864ms | 3885ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 3007ms | 3925ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 2904ms | 3888ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 3042ms | 3979ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 2981ms | 3923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 2774ms | 3859ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 2885ms | 3885ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 3055ms | 3905ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 2885ms | 3885ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 2750ms | 3850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 2933ms | 3892ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 2885ms | 3886ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 2719ms | 3836ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 3019ms | 3902ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 2786ms | 3865ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 2857ms | 3880ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 2994ms | 3899ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 2828ms | 3874ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 2885ms | 3885ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 2981ms | 3898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | ok | 2875ms | 3883ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | ok | 2750ms | 3850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | ok | 3090ms | 3909ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | ok | 4250ms | 5729ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | ok | 3938ms | 5050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | end-users | ok | 4172ms | 5345ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | ok | 4559ms | 5733ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | ok | 4618ms | 5792ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | end-users | ok | 4545ms | 5704ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | ok | 4472ms | 5520ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | ok | 4636ms | 5850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | end-users | ok | 4539ms | 5736ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app1 | ok | 4597ms | 5739ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app2 | ok | 4600ms | 5843ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | end-users | ok | 4579ms | 5753ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app1 | ok | 4661ms | 5827ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app2 | ok | 4433ms | 5617ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | end-users | ok | 4557ms | 5743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app1 | ok | 4833ms | 5881ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app2 | ok | 4615ms | 5967ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | end-users | ok | 4575ms | 5805ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app1 | ok | 4648ms | 5896ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app2 | ok | 4533ms | 5760ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | end-users | ok | 4517ms | 5774ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app1 | ok | 4733ms | 5847ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app2 | ok | 4667ms | 5829ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | end-users | ok | 4558ms | 5723ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app1 | ok | 4821ms | 5874ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app2 | ok | 4577ms | 5808ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | end-users | ok | 4606ms | 5740ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app1 | ok | 4750ms | 5850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app2 | ok | 4700ms | 5825ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | end-users | ok | 4623ms | 5763ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 412.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 412.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 412.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 428.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 428.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 428.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
