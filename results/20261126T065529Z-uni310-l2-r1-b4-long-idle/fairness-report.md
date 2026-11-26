# Fairness benchmark: full-contention (uni310-l2-r1-b4-long-idle)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 6.1 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'
Schedule-aware expected share (UNI-222): app1, app2, end-users scored against a time-weighted entitlement from the declared join/leave or duty-cycle schedule, not the flat whole-run weight ratio -- see docs/design.md "Whole-run scoring with a declared schedule".

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 6.1 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `890` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-8448f688f-xhg6g` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T06:56:51Z` |
| Run end | `2026-11-26T07:16:28Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 119 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/119 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 83.00 | 2.5938 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1386 | 000=2, 200=1384 | 6.7 | 8.8 | 1829882.0 | 6.7% | 16.7% | -4.4 | 6.7% | -0.0 | 7.0% | -14.1 | 74.7s | 98.9% | 1386.0 |
| app2 | 10.0 | 32 | 2477 | 000=1, 200=2476 | 11.3 | 15.0 | 3321460.0 | 12.4% | 16.7% | 6.1 | 12.4% | 0.0 | 12.5% | 1.9 | 212.1s | 98.9% | 2477.0 |
| end-users | 65.0 | 128 | 16019 | 000=11, 200=16007, 503=1 | 6.9 | 9.5 | 21454666.0 | 80.9% | 66.7% | -1.8 | 80.9% | 0.0 | 80.6% | 12.1 | 212.1s | 98.9% | 16019.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-890s, 150s on / 600s off
- app2: active 0s-890s, no duty cycle
- end-users: active 0s-890s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 10.0 | 10.0 |
| 150.0 | 150.0 | 0.0 |
| 750.0 | 753.0 | 3.0 |
| 890.0 | n/a (never converged in this phase) | n/a |

**Windows** (118 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 9448.0 | 21.1% | 100.0% | 78.9 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | False | 0.0 | 68.4% | 0.0% | -68.4 |
| 10.0 | 20.0 | app1 | True | False | 70330.0 | 21.1% | 23.2% | 2.2 |
| 10.0 | 20.0 | app2 | True | False | 22950.0 | 10.5% | 7.6% | -3.0 |
| 10.0 | 20.0 | end-users | True | False | 209658.0 | 68.4% | 69.2% | 0.8 |
| 20.0 | 30.0 | app1 | True | False | 66148.0 | 21.1% | 21.9% | 0.9 |
| 20.0 | 30.0 | app2 | True | False | 27116.0 | 10.5% | 9.0% | -1.5 |
| 20.0 | 30.0 | end-users | True | False | 208286.0 | 68.4% | 69.1% | 0.7 |
| 30.0 | 40.0 | app1 | True | False | 60904.0 | 21.1% | 19.7% | -1.3 |
| 30.0 | 40.0 | app2 | True | False | 37896.0 | 10.5% | 12.3% | 1.8 |
| 30.0 | 40.0 | end-users | True | False | 209714.0 | 68.4% | 68.0% | -0.4 |
| 40.0 | 50.0 | app1 | True | False | 63552.0 | 21.1% | 20.6% | -0.4 |
| 40.0 | 50.0 | app2 | True | False | 32452.0 | 10.5% | 10.5% | -0.0 |
| 40.0 | 50.0 | end-users | True | False | 212398.0 | 68.4% | 68.9% | 0.4 |
| 50.0 | 60.0 | app1 | True | False | 64970.0 | 21.1% | 21.4% | 0.4 |
| 50.0 | 60.0 | app2 | True | False | 31134.0 | 10.5% | 10.3% | -0.3 |
| 50.0 | 60.0 | end-users | True | False | 206906.0 | 68.4% | 68.3% | -0.1 |
| 60.0 | 70.0 | app1 | True | False | 56830.0 | 21.1% | 20.6% | -0.5 |
| 60.0 | 70.0 | app2 | True | False | 25696.0 | 10.5% | 9.3% | -1.2 |
| 60.0 | 70.0 | end-users | True | False | 193374.0 | 68.4% | 70.1% | 1.7 |
| 70.0 | 80.0 | app1 | True | False | 66326.0 | 21.1% | 21.5% | 0.4 |
| 70.0 | 80.0 | app2 | True | False | 36516.0 | 10.5% | 11.8% | 1.3 |
| 70.0 | 80.0 | end-users | True | False | 205640.0 | 68.4% | 66.7% | -1.8 |
| 80.0 | 90.0 | app1 | True | False | 57996.0 | 21.1% | 22.3% | 1.3 |
| 80.0 | 90.0 | app2 | True | False | 21634.0 | 10.5% | 8.3% | -2.2 |
| 80.0 | 90.0 | end-users | True | False | 180106.0 | 68.4% | 69.3% | 0.9 |
| 90.0 | 100.0 | app1 | True | False | 58174.0 | 21.1% | 19.0% | -2.0 |
| 90.0 | 100.0 | app2 | True | False | 37894.0 | 10.5% | 12.4% | 1.9 |
| 90.0 | 100.0 | end-users | True | False | 209722.0 | 68.4% | 68.6% | 0.2 |
| 100.0 | 110.0 | app1 | True | False | 67626.0 | 21.1% | 22.1% | 1.1 |
| 100.0 | 110.0 | app2 | True | False | 31042.0 | 10.5% | 10.2% | -0.4 |
| 100.0 | 110.0 | end-users | True | False | 207032.0 | 68.4% | 67.7% | -0.7 |
| 110.0 | 120.0 | app1 | True | False | 59480.0 | 21.1% | 19.6% | -1.4 |
| 110.0 | 120.0 | app2 | True | False | 33860.0 | 10.5% | 11.2% | 0.6 |
| 110.0 | 120.0 | end-users | True | False | 209816.0 | 68.4% | 69.2% | 0.8 |
| 120.0 | 130.0 | app1 | True | False | 64928.0 | 21.1% | 21.0% | -0.1 |
| 120.0 | 130.0 | app2 | True | False | 33862.0 | 10.5% | 10.9% | 0.4 |
| 120.0 | 130.0 | end-users | True | False | 210812.0 | 68.4% | 68.1% | -0.3 |
| 130.0 | 140.0 | app1 | True | False | 66286.0 | 21.1% | 21.4% | 0.4 |
| 130.0 | 140.0 | app2 | True | False | 31110.0 | 10.5% | 10.0% | -0.5 |
| 130.0 | 140.0 | end-users | True | False | 212166.0 | 68.4% | 68.5% | 0.1 |
| 140.0 | 150.0 | app1 | True | False | 63554.0 | 21.1% | 21.0% | -0.1 |
| 140.0 | 150.0 | app2 | True | False | 31174.0 | 10.5% | 10.3% | -0.2 |
| 140.0 | 150.0 | end-users | True | False | 208468.0 | 68.4% | 68.8% | 0.3 |
| 150.0 | 160.0 | app1 | False | n/a | 48734.0 | n/a | n/a | n/a |
| 150.0 | 160.0 | app2 | True | False | 33866.0 | 13.3% | 13.8% | 0.5 |
| 150.0 | 160.0 | end-users | True | False | 211168.0 | 86.7% | 86.2% | -0.5 |
| 160.0 | 170.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 160.0 | 170.0 | app2 | True | False | 40656.0 | 13.3% | 13.2% | -0.1 |
| 160.0 | 170.0 | end-users | True | False | 267706.0 | 86.7% | 86.8% | 0.1 |
| 170.0 | 181.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 170.0 | 181.0 | app2 | True | False | 40602.0 | 13.3% | 13.3% | 0.0 |
| 170.0 | 181.0 | end-users | True | False | 263886.0 | 86.7% | 86.7% | -0.0 |
| 181.0 | 191.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 181.0 | 191.0 | app2 | True | False | 39216.0 | 13.3% | 12.8% | -0.5 |
| 181.0 | 191.0 | end-users | True | False | 266302.0 | 86.7% | 87.2% | 0.5 |
| 191.0 | 201.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app2 | True | False | 40564.0 | 13.3% | 13.2% | -0.2 |
| 191.0 | 201.0 | end-users | True | False | 267530.0 | 86.7% | 86.8% | 0.2 |
| 201.0 | 211.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 201.0 | 211.0 | app2 | True | False | 43244.0 | 13.3% | 14.1% | 0.8 |
| 201.0 | 211.0 | end-users | True | False | 263696.0 | 86.7% | 85.9% | -0.8 |
| 211.0 | 221.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 211.0 | 221.0 | app2 | True | False | 43294.0 | 13.3% | 14.1% | 0.8 |
| 211.0 | 221.0 | end-users | True | False | 263724.0 | 86.7% | 85.9% | -0.8 |
| 221.0 | 231.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app2 | True | False | 36484.0 | 13.3% | 12.0% | -1.3 |
| 221.0 | 231.0 | end-users | True | False | 267826.0 | 86.7% | 88.0% | 1.3 |
| 231.0 | 241.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app2 | True | False | 40650.0 | 13.3% | 13.5% | 0.1 |
| 231.0 | 241.0 | end-users | True | False | 261058.0 | 86.7% | 86.5% | -0.1 |
| 241.0 | 251.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | True | False | 39230.0 | 13.3% | 13.1% | -0.2 |
| 241.0 | 251.0 | end-users | True | False | 259658.0 | 86.7% | 86.9% | 0.2 |
| 251.0 | 261.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | True | False | 39156.0 | 13.3% | 13.0% | -0.3 |
| 251.0 | 261.0 | end-users | True | False | 261078.0 | 86.7% | 87.0% | 0.3 |
| 261.0 | 271.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | True | False | 44672.0 | 13.3% | 14.4% | 1.1 |
| 261.0 | 271.0 | end-users | True | False | 264990.0 | 86.7% | 85.6% | -1.1 |
| 271.0 | 281.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | True | False | 31146.0 | 13.3% | 10.5% | -2.8 |
| 271.0 | 281.0 | end-users | True | False | 265296.0 | 86.7% | 89.5% | 2.8 |
| 281.0 | 291.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | True | False | 48744.0 | 13.3% | 16.0% | 2.7 |
| 281.0 | 291.0 | end-users | True | False | 255590.0 | 86.7% | 84.0% | -2.7 |
| 291.0 | 301.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | True | False | 40662.0 | 13.3% | 13.5% | 0.2 |
| 291.0 | 301.0 | end-users | True | False | 259670.0 | 86.7% | 86.5% | -0.2 |
| 301.0 | 311.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | True | False | 40524.0 | 13.3% | 13.3% | -0.1 |
| 301.0 | 311.0 | end-users | True | False | 265162.0 | 86.7% | 86.7% | 0.1 |
| 311.0 | 321.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | True | False | 41884.0 | 13.3% | 13.6% | 0.3 |
| 311.0 | 321.0 | end-users | True | False | 266268.0 | 86.7% | 86.4% | -0.3 |
| 321.0 | 331.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | True | False | 37954.0 | 13.3% | 12.5% | -0.9 |
| 321.0 | 331.0 | end-users | True | False | 266384.0 | 86.7% | 87.5% | 0.9 |
| 331.0 | 341.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | True | False | 44650.0 | 13.3% | 14.6% | 1.3 |
| 331.0 | 341.0 | end-users | True | False | 260982.0 | 86.7% | 85.4% | -1.3 |
| 341.0 | 351.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | True | False | 43360.0 | 13.3% | 14.2% | 0.9 |
| 341.0 | 351.0 | end-users | True | False | 261026.0 | 86.7% | 85.8% | -0.9 |
| 351.0 | 361.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | True | False | 35156.0 | 13.3% | 11.7% | -1.7 |
| 351.0 | 361.0 | end-users | True | False | 266516.0 | 86.7% | 88.3% | 1.7 |
| 361.0 | 371.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | True | False | 43290.0 | 13.3% | 14.2% | 0.8 |
| 361.0 | 371.0 | end-users | True | False | 262408.0 | 86.7% | 85.8% | -0.8 |
| 371.0 | 381.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | True | False | 33832.0 | 13.3% | 11.3% | -2.1 |
| 371.0 | 381.0 | end-users | True | False | 266450.0 | 86.7% | 88.7% | 2.1 |
| 381.0 | 391.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | True | False | 41956.0 | 13.3% | 13.6% | 0.2 |
| 381.0 | 391.0 | end-users | True | False | 267638.0 | 86.7% | 86.4% | -0.2 |
| 391.0 | 401.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | True | False | 39158.0 | 13.3% | 12.9% | -0.4 |
| 391.0 | 401.0 | end-users | True | False | 263894.0 | 86.7% | 87.1% | 0.4 |
| 401.0 | 411.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | True | False | 47410.0 | 13.3% | 15.5% | 2.2 |
| 401.0 | 411.0 | end-users | True | False | 258218.0 | 86.7% | 84.5% | -2.2 |
| 411.0 | 421.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | True | False | 39220.0 | 13.3% | 12.7% | -0.7 |
| 411.0 | 421.0 | end-users | True | False | 270318.0 | 86.7% | 87.3% | 0.7 |
| 421.0 | 432.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 432.0 | app2 | True | False | 41956.0 | 13.3% | 13.7% | 0.4 |
| 421.0 | 432.0 | end-users | True | False | 263836.0 | 86.7% | 86.3% | -0.4 |
| 432.0 | 442.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | True | False | 40584.0 | 13.3% | 13.2% | -0.1 |
| 432.0 | 442.0 | end-users | True | False | 266430.0 | 86.7% | 86.8% | 0.1 |
| 442.0 | 452.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | True | False | 41994.0 | 13.3% | 13.8% | 0.5 |
| 442.0 | 452.0 | end-users | True | False | 262560.0 | 86.7% | 86.2% | -0.5 |
| 452.0 | 462.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | True | False | 40578.0 | 13.3% | 13.2% | -0.1 |
| 452.0 | 462.0 | end-users | True | False | 266640.0 | 86.7% | 86.8% | 0.1 |
| 462.0 | 472.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | True | False | 40562.0 | 13.3% | 13.5% | 0.1 |
| 462.0 | 472.0 | end-users | True | False | 260964.0 | 86.7% | 86.5% | -0.1 |
| 472.0 | 482.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | True | False | 39134.0 | 13.3% | 12.6% | -0.7 |
| 472.0 | 482.0 | end-users | True | False | 271728.0 | 86.7% | 87.4% | 0.7 |
| 482.0 | 492.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | True | False | 37918.0 | 13.3% | 12.8% | -0.5 |
| 482.0 | 492.0 | end-users | True | False | 258522.0 | 86.7% | 87.2% | 0.5 |
| 492.0 | 502.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | True | False | 39196.0 | 13.3% | 12.9% | -0.4 |
| 492.0 | 502.0 | end-users | True | False | 263816.0 | 86.7% | 87.1% | 0.4 |
| 502.0 | 512.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app2 | True | False | 47380.0 | 13.3% | 15.5% | 2.2 |
| 502.0 | 512.0 | end-users | True | False | 258596.0 | 86.7% | 84.5% | -2.2 |
| 512.0 | 522.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app2 | True | False | 35170.0 | 13.3% | 12.0% | -1.3 |
| 512.0 | 522.0 | end-users | True | False | 256892.0 | 86.7% | 88.0% | 1.3 |
| 522.0 | 532.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app2 | True | False | 43342.0 | 13.3% | 16.1% | 2.8 |
| 522.0 | 532.0 | end-users | True | False | 225968.0 | 86.7% | 83.9% | -2.8 |
| 532.0 | 542.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app2 | True | False | 17612.0 | 13.3% | 9.6% | -3.8 |
| 532.0 | 542.0 | end-users | True | False | 166462.0 | 86.7% | 90.4% | 3.8 |
| 542.0 | 552.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 542.0 | 552.0 | app2 | True | False | 35206.0 | 13.3% | 11.7% | -1.7 |
| 542.0 | 552.0 | end-users | True | False | 266442.0 | 86.7% | 88.3% | 1.7 |
| 552.0 | 562.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 552.0 | 562.0 | app2 | True | False | 51408.0 | 13.3% | 17.1% | 3.8 |
| 552.0 | 562.0 | end-users | True | False | 248944.0 | 86.7% | 82.9% | -3.8 |
| 562.0 | 572.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 562.0 | 572.0 | app2 | True | False | 37910.0 | 13.3% | 12.6% | -0.8 |
| 562.0 | 572.0 | end-users | True | False | 263810.0 | 86.7% | 87.4% | 0.8 |
| 572.0 | 582.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 572.0 | 582.0 | app2 | True | False | 35200.0 | 13.3% | 12.2% | -1.1 |
| 572.0 | 582.0 | end-users | True | False | 252940.0 | 86.7% | 87.8% | 1.1 |
| 582.0 | 592.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 582.0 | 592.0 | app2 | True | False | 39216.0 | 13.3% | 12.9% | -0.4 |
| 582.0 | 592.0 | end-users | True | False | 265138.0 | 86.7% | 87.1% | 0.4 |
| 592.0 | 602.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 592.0 | 602.0 | app2 | True | False | 41922.0 | 13.3% | 14.0% | 0.6 |
| 592.0 | 602.0 | end-users | True | False | 258436.0 | 86.7% | 86.0% | -0.6 |
| 602.0 | 612.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 602.0 | 612.0 | app2 | True | False | 43250.0 | 13.3% | 14.6% | 1.3 |
| 602.0 | 612.0 | end-users | True | False | 253002.0 | 86.7% | 85.4% | -1.3 |
| 612.0 | 622.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 612.0 | 622.0 | app2 | True | False | 47340.0 | 13.3% | 15.6% | 2.2 |
| 612.0 | 622.0 | end-users | True | False | 256892.0 | 86.7% | 84.4% | -2.2 |
| 622.0 | 632.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 622.0 | 632.0 | app2 | True | False | 29744.0 | 13.3% | 9.9% | -3.5 |
| 622.0 | 632.0 | end-users | True | False | 271804.0 | 86.7% | 90.1% | 3.5 |
| 632.0 | 642.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 632.0 | 642.0 | app2 | True | False | 44604.0 | 13.3% | 14.6% | 1.3 |
| 632.0 | 642.0 | end-users | True | False | 260848.0 | 86.7% | 85.4% | -1.3 |
| 642.0 | 652.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 642.0 | 652.0 | app2 | True | False | 47278.0 | 13.3% | 16.0% | 2.7 |
| 642.0 | 652.0 | end-users | True | False | 247366.0 | 86.7% | 84.0% | -2.7 |
| 652.0 | 662.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 652.0 | 662.0 | app2 | True | False | 24386.0 | 13.3% | 8.1% | -5.2 |
| 652.0 | 662.0 | end-users | True | False | 275884.0 | 86.7% | 91.9% | 5.2 |
| 662.0 | 672.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 662.0 | 672.0 | app2 | True | False | 48724.0 | 13.3% | 16.1% | 2.8 |
| 662.0 | 672.0 | end-users | True | False | 252978.0 | 86.7% | 83.9% | -2.8 |
| 672.0 | 683.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 672.0 | 683.0 | app2 | True | False | 40546.0 | 13.3% | 13.4% | 0.1 |
| 672.0 | 683.0 | end-users | True | False | 261088.0 | 86.7% | 86.6% | -0.1 |
| 683.0 | 693.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 683.0 | 693.0 | app2 | True | False | 43280.0 | 13.3% | 14.3% | 1.0 |
| 683.0 | 693.0 | end-users | True | False | 258532.0 | 86.7% | 85.7% | -1.0 |
| 693.0 | 703.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 693.0 | 703.0 | app2 | True | False | 36596.0 | 13.3% | 12.0% | -1.3 |
| 693.0 | 703.0 | end-users | True | False | 267840.0 | 86.7% | 88.0% | 1.3 |
| 703.0 | 713.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 703.0 | 713.0 | app2 | True | False | 40634.0 | 13.3% | 13.4% | 0.1 |
| 703.0 | 713.0 | end-users | True | False | 262410.0 | 86.7% | 86.6% | -0.1 |
| 713.0 | 723.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 713.0 | 723.0 | app2 | True | False | 40650.0 | 13.3% | 13.5% | 0.1 |
| 713.0 | 723.0 | end-users | True | False | 261078.0 | 86.7% | 86.5% | -0.1 |
| 723.0 | 733.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 723.0 | 733.0 | app2 | True | False | 41910.0 | 13.3% | 13.8% | 0.5 |
| 723.0 | 733.0 | end-users | True | False | 261074.0 | 86.7% | 86.2% | -0.5 |
| 733.0 | 743.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 733.0 | 743.0 | app2 | True | False | 40550.0 | 13.3% | 13.3% | -0.0 |
| 733.0 | 743.0 | end-users | True | False | 263664.0 | 86.7% | 86.7% | 0.0 |
| 743.0 | 753.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 743.0 | 753.0 | app2 | True | False | 35130.0 | 13.3% | 11.5% | -1.8 |
| 743.0 | 753.0 | end-users | True | False | 269186.0 | 86.7% | 88.5% | 1.8 |
| 753.0 | 763.0 | app1 | True | False | 48778.0 | 21.1% | 16.5% | -4.5 |
| 753.0 | 763.0 | app2 | True | False | 36484.0 | 10.5% | 12.4% | 1.8 |
| 753.0 | 763.0 | end-users | True | False | 209552.0 | 68.4% | 71.1% | 2.7 |
| 763.0 | 773.0 | app1 | True | False | 59452.0 | 21.1% | 20.4% | -0.6 |
| 763.0 | 773.0 | app2 | True | False | 32462.0 | 10.5% | 11.2% | 0.6 |
| 763.0 | 773.0 | end-users | True | False | 198984.0 | 68.4% | 68.4% | -0.0 |
| 773.0 | 783.0 | app1 | True | False | 59574.0 | 21.1% | 20.4% | -0.7 |
| 773.0 | 783.0 | app2 | True | False | 31102.0 | 10.5% | 10.6% | 0.1 |
| 773.0 | 783.0 | end-users | True | False | 201650.0 | 68.4% | 69.0% | 0.6 |
| 783.0 | 793.0 | app1 | True | False | 63516.0 | 21.1% | 21.1% | 0.0 |
| 783.0 | 793.0 | app2 | True | False | 31120.0 | 10.5% | 10.3% | -0.2 |
| 783.0 | 793.0 | end-users | True | False | 206874.0 | 68.4% | 68.6% | 0.2 |
| 793.0 | 803.0 | app1 | True | False | 68808.0 | 21.1% | 22.2% | 1.2 |
| 793.0 | 803.0 | app2 | True | False | 35184.0 | 10.5% | 11.4% | 0.8 |
| 793.0 | 803.0 | end-users | True | False | 205444.0 | 68.4% | 66.4% | -2.0 |
| 803.0 | 813.0 | app1 | True | False | 59492.0 | 21.1% | 19.6% | -1.4 |
| 803.0 | 813.0 | app2 | True | False | 27048.0 | 10.5% | 8.9% | -1.6 |
| 803.0 | 813.0 | end-users | True | False | 216350.0 | 68.4% | 71.4% | 3.0 |
| 813.0 | 823.0 | app1 | True | False | 67698.0 | 21.1% | 22.1% | 1.0 |
| 813.0 | 823.0 | app2 | True | False | 35160.0 | 10.5% | 11.5% | 0.9 |
| 813.0 | 823.0 | end-users | True | False | 204120.0 | 68.4% | 66.5% | -1.9 |
| 823.0 | 833.0 | app1 | True | False | 56736.0 | 21.1% | 19.6% | -1.5 |
| 823.0 | 833.0 | app2 | True | False | 31174.0 | 10.5% | 10.8% | 0.2 |
| 823.0 | 833.0 | end-users | True | False | 201700.0 | 68.4% | 69.6% | 1.2 |
| 833.0 | 843.0 | app1 | True | False | 59610.0 | 21.1% | 21.6% | 0.5 |
| 833.0 | 843.0 | app2 | True | False | 25718.0 | 10.5% | 9.3% | -1.2 |
| 833.0 | 843.0 | end-users | True | False | 190698.0 | 68.4% | 69.1% | 0.7 |
| 843.0 | 853.0 | app1 | True | False | 64826.0 | 21.1% | 21.2% | 0.2 |
| 843.0 | 853.0 | app2 | True | False | 35232.0 | 10.5% | 11.5% | 1.0 |
| 843.0 | 853.0 | end-users | True | False | 205640.0 | 68.4% | 67.3% | -1.2 |
| 853.0 | 863.0 | app1 | True | False | 58148.0 | 21.1% | 19.6% | -1.5 |
| 853.0 | 863.0 | app2 | True | False | 32480.0 | 10.5% | 10.9% | 0.4 |
| 853.0 | 863.0 | end-users | True | False | 206736.0 | 68.4% | 69.5% | 1.1 |
| 863.0 | 873.0 | app1 | True | False | 62292.0 | 21.1% | 20.4% | -0.7 |
| 863.0 | 873.0 | app2 | True | False | 33764.0 | 10.5% | 11.0% | 0.5 |
| 863.0 | 873.0 | end-users | True | False | 209542.0 | 68.4% | 68.6% | 0.1 |
| 873.0 | 883.0 | app1 | True | False | 66324.0 | 21.1% | 22.2% | 1.1 |
| 873.0 | 883.0 | app2 | True | False | 29826.0 | 10.5% | 10.0% | -0.6 |
| 873.0 | 883.0 | end-users | True | False | 202906.0 | 68.4% | 67.8% | -0.6 |
| 883.0 | 893.0 | app1 | True | False | 62278.0 | 21.1% | 20.6% | -0.4 |
| 883.0 | 893.0 | app2 | True | False | 29698.0 | 10.5% | 9.8% | -0.7 |
| 883.0 | 893.0 | end-users | True | False | 209694.0 | 68.4% | 69.5% | 1.1 |
| 893.0 | 903.0 | app1 | False | n/a | 27064.0 | n/a | n/a | n/a |
| 893.0 | 903.0 | app2 | False | n/a | 39182.0 | n/a | n/a | n/a |
| 893.0 | 903.0 | end-users | False | n/a | 124466.0 | n/a | n/a | n/a |
| 903.0 | 913.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 903.0 | 913.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 903.0 | 913.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 913.0 | 923.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 913.0 | 923.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 913.0 | 923.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 923.0 | 933.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 923.0 | 933.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 923.0 | 933.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 933.0 | 944.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 933.0 | 944.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 933.0 | 944.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 944.0 | 954.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 944.0 | 954.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 944.0 | 954.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 954.0 | 964.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 954.0 | 964.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 954.0 | 964.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 964.0 | 974.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 964.0 | 974.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 964.0 | 974.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 974.0 | 984.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 974.0 | 984.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 974.0 | 984.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 984.0 | 994.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 984.0 | 994.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 984.0 | 994.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 994.0 | 1004.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 994.0 | 1004.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 994.0 | 1004.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1004.0 | 1014.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1004.0 | 1014.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1004.0 | 1014.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1014.0 | 1024.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1014.0 | 1024.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1014.0 | 1024.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1024.0 | 1034.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1024.0 | 1034.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1024.0 | 1034.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1034.0 | 1044.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1034.0 | 1044.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1034.0 | 1044.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1044.0 | 1054.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1044.0 | 1054.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1044.0 | 1054.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1054.0 | 1064.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1054.0 | 1064.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1054.0 | 1064.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1064.0 | 1074.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1064.0 | 1074.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1064.0 | 1074.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1074.0 | 1084.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1074.0 | 1084.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1074.0 | 1084.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1084.0 | 1094.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1084.0 | 1094.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1084.0 | 1094.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1094.0 | 1104.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1094.0 | 1104.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1094.0 | 1104.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1104.0 | 1114.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1104.0 | 1114.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1104.0 | 1114.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1114.0 | 1124.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1114.0 | 1124.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1114.0 | 1124.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1124.0 | 1134.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1124.0 | 1134.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1124.0 | 1134.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1134.0 | 1144.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1134.0 | 1144.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1134.0 | 1144.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1144.0 | 1154.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1144.0 | 1154.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1144.0 | 1154.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1154.0 | 1164.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1154.0 | 1164.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1154.0 | 1164.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1164.0 | 1174.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1164.0 | 1174.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1164.0 | 1174.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1174.0 | 1177.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1174.0 | 1177.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1174.0 | 1177.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`, EPP restart detected mid-window at least once):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 51 | 1219ms | 2494ms | 4745ms |
| 0.0 | 10.0 | app2 | ok | 27 | 0ms | 3875ms | 4888ms |
| 0.0 | 10.0 | end-users | ok | 171 | 0ms | 3526ms | 4853ms |
| 10.0 | 20.0 | app1 | ok | 42 | 1643ms | 2900ms | 4790ms |
| 10.0 | 20.0 | app2 | ok | 21 | 7500ms | 9500ms | 9950ms |
| 10.0 | 20.0 | end-users | ok | 135 | 3452ms | 4690ms | 4969ms |
| 20.0 | 30.0 | app1 | ok | 53 | 2193ms | 4398ms | 4940ms |
| 20.0 | 30.0 | app2 | ok | 25 | 5682ms | 13333ms | 28333ms |
| 20.0 | 30.0 | end-users | ok | 164 | 3153ms | 4631ms | 4963ms |
| 30.0 | 40.0 | app1 | ok | 49 | 2240ms | 4388ms | 4939ms |
| 30.0 | 40.0 | app2 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 30.0 | 40.0 | end-users | ok | 162 | 3543ms | 4709ms | 4971ms |
| 40.0 | 50.0 | app1 | ok | 53 | 1775ms | 3896ms | 4890ms |
| 40.0 | 50.0 | app2 | ok | 26 | 7500ms | 9500ms | 9950ms |
| 40.0 | 50.0 | end-users | ok | 174 | 3389ms | 4678ms | 4968ms |
| 50.0 | 60.0 | app1 | ok | 30 | 1536ms | 3750ms | 4875ms |
| 50.0 | 60.0 | app2 | ok | 31 | 5694ms | 9139ms | 9914ms |
| 50.0 | 60.0 | end-users | ok | 114 | 2935ms | 4587ms | 4959ms |
| 60.0 | 70.0 | app1 | ok | 52 | 2609ms | 4870ms | 9350ms |
| 60.0 | 70.0 | app2 | ok | 10 | 8571ms | 23333ms | 29333ms |
| 60.0 | 70.0 | end-users | ok | 150 | 3796ms | 7917ms | 9792ms |
| 70.0 | 80.0 | app1 | ok | 56 | 1840ms | 4176ms | 4918ms |
| 70.0 | 80.0 | app2 | ok | 44 | 6500ms | 9433ms | 21200ms |
| 70.0 | 80.0 | end-users | ok | 205 | 3208ms | 4642ms | 4964ms |
| 80.0 | 90.0 | app1 | ok | 25 | 3750ms | 8214ms | 9821ms |
| 80.0 | 90.0 | app2 | ok | 2 | 7500ms | 9500ms | 9950ms |
| 80.0 | 90.0 | end-users | ok | 81 | 3849ms | 8239ms | 9824ms |
| 90.0 | 100.0 | app1 | ok | 59 | 2695ms | 4539ms | 4954ms |
| 90.0 | 100.0 | app2 | ok | 24 | 7750ms | 14000ms | 28400ms |
| 90.0 | 100.0 | end-users | ok | 165 | 3309ms | 4662ms | 4966ms |
| 100.0 | 110.0 | app1 | ok | 44 | 1778ms | 3778ms | 4878ms |
| 100.0 | 110.0 | app2 | ok | 22 | 7500ms | 9500ms | 9950ms |
| 100.0 | 110.0 | end-users | ok | 145 | 3188ms | 4638ms | 4964ms |
| 110.0 | 120.0 | app1 | ok | 51 | 1825ms | 3938ms | 4894ms |
| 110.0 | 120.0 | app2 | ok | 26 | 7500ms | 9500ms | 9950ms |
| 110.0 | 120.0 | end-users | ok | 170 | 3313ms | 4663ms | 4966ms |
| 120.0 | 130.0 | app1 | ok | 48 | 1692ms | 3800ms | 4880ms |
| 120.0 | 130.0 | app2 | ok | 24 | 7500ms | 9500ms | 9950ms |
| 120.0 | 130.0 | end-users | ok | 155 | 3510ms | 4702ms | 4970ms |
| 130.0 | 140.0 | app1 | ok | 50 | 1643ms | 3611ms | 4861ms |
| 130.0 | 140.0 | app2 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 130.0 | 140.0 | end-users | ok | 162 | 3500ms | 4700ms | 4970ms |
| 140.0 | 150.0 | app1 | ok | 49 | 1750ms | 3775ms | 4877ms |
| 140.0 | 150.0 | app2 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 140.0 | 150.0 | end-users | ok | 167 | 3369ms | 4674ms | 4967ms |
| 150.0 | 160.0 | app1 | ok | 9 | 3125ms | 4625ms | 4962ms |
| 150.0 | 160.0 | app2 | ok | 24 | 7609ms | 9696ms | 25200ms |
| 150.0 | 160.0 | end-users | ok | 152 | 2457ms | 4486ms | 4949ms |
| 160.0 | 170.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 30 | 6739ms | 9348ms | 9935ms |
| 160.0 | 170.0 | end-users | ok | 199 | 1562ms | 3157ms | 4816ms |
| 170.0 | 181.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 170.0 | 181.0 | app2 | ok | 36 | 6538ms | 9308ms | 9931ms |
| 170.0 | 181.0 | end-users | ok | 223 | 1415ms | 2677ms | 4768ms |
| 181.0 | 191.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 22 | 6944ms | 9389ms | 9939ms |
| 181.0 | 191.0 | end-users | ok | 156 | 1560ms | 3143ms | 4814ms |
| 191.0 | 201.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 38 | 6481ms | 9296ms | 9930ms |
| 191.0 | 201.0 | end-users | ok | 242 | 1586ms | 2914ms | 4791ms |
| 201.0 | 211.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 28 | 4444ms | 8833ms | 9883ms |
| 201.0 | 211.0 | end-users | ok | 169 | 1514ms | 3375ms | 4838ms |
| 211.0 | 221.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 30 | 6429ms | 9286ms | 9929ms |
| 211.0 | 221.0 | end-users | ok | 207 | 1649ms | 3383ms | 4838ms |
| 221.0 | 231.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 32 | 2917ms | 7333ms | 9733ms |
| 221.0 | 231.0 | end-users | ok | 189 | 1585ms | 3788ms | 4879ms |
| 231.0 | 241.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 29 | 6705ms | 9341ms | 9934ms |
| 231.0 | 241.0 | end-users | ok | 210 | 1612ms | 3456ms | 4846ms |
| 241.0 | 251.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 40 | 3000ms | 8333ms | 9833ms |
| 241.0 | 251.0 | end-users | ok | 175 | 1783ms | 4006ms | 4901ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 15 | 875ms | 4688ms | 9250ms |
| 251.0 | 261.0 | end-users | ok | 184 | 1806ms | 4061ms | 4906ms |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | ok | 33 | 5417ms | 9083ms | 9908ms |
| 261.0 | 271.0 | end-users | ok | 213 | 1591ms | 3336ms | 4834ms |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | ok | 36 | 4118ms | 8500ms | 9850ms |
| 271.0 | 281.0 | end-users | ok | 168 | 1805ms | 4087ms | 4909ms |
| 281.0 | 291.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | ok | 26 | 4615ms | 8818ms | 9882ms |
| 281.0 | 291.0 | end-users | ok | 226 | 1802ms | 4042ms | 4904ms |
| 291.0 | 301.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | ok | 23 | 6167ms | 9233ms | 9923ms |
| 291.0 | 301.0 | end-users | ok | 156 | 1839ms | 4049ms | 4905ms |
| 301.0 | 311.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | ok | 31 | 6125ms | 9225ms | 9922ms |
| 301.0 | 311.0 | end-users | ok | 204 | 1610ms | 3406ms | 4841ms |
| 311.0 | 321.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | ok | 42 | 4688ms | 8895ms | 9889ms |
| 311.0 | 321.0 | end-users | ok | 223 | 1618ms | 3533ms | 4853ms |
| 321.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | ok | 23 | 5208ms | 9042ms | 9904ms |
| 321.0 | 331.0 | end-users | ok | 206 | 1781ms | 3856ms | 4886ms |
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | ok | 24 | 6250ms | 9250ms | 9925ms |
| 331.0 | 341.0 | end-users | ok | 151 | 1637ms | 3548ms | 4855ms |
| 341.0 | 351.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | ok | 36 | 4000ms | 8500ms | 9850ms |
| 341.0 | 351.0 | end-users | ok | 230 | 1782ms | 4009ms | 4901ms |
| 351.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | ok | 31 | 5441ms | 9088ms | 9909ms |
| 351.0 | 361.0 | end-users | ok | 202 | 1750ms | 3902ms | 4890ms |
| 361.0 | 371.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | ok | 23 | 6618ms | 9324ms | 9932ms |
| 361.0 | 371.0 | end-users | ok | 153 | 1619ms | 3529ms | 4853ms |
| 371.0 | 381.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | ok | 46 | 3906ms | 8562ms | 9856ms |
| 371.0 | 381.0 | end-users | ok | 230 | 1685ms | 3894ms | 4889ms |
| 381.0 | 391.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | ok | 15 | 4375ms | 8500ms | 9850ms |
| 381.0 | 391.0 | end-users | ok | 168 | 1911ms | 4176ms | 4918ms |
| 391.0 | 401.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | ok | 35 | 3984ms | 8409ms | 9841ms |
| 391.0 | 401.0 | end-users | ok | 233 | 1731ms | 3960ms | 4896ms |
| 401.0 | 411.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | ok | 26 | 5938ms | 9188ms | 9919ms |
| 401.0 | 411.0 | end-users | ok | 164 | 1750ms | 3861ms | 4886ms |
| 411.0 | 421.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | ok | 34 | 4773ms | 8938ms | 9894ms |
| 411.0 | 421.0 | end-users | ok | 222 | 1713ms | 3819ms | 4882ms |
| 421.0 | 432.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 432.0 | app2 | ok | 33 | 6700ms | 9340ms | 9934ms |
| 421.0 | 432.0 | end-users | ok | 207 | 1718ms | 3768ms | 4877ms |
| 432.0 | 442.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | ok | 24 | 6842ms | 9368ms | 9937ms |
| 432.0 | 442.0 | end-users | ok | 160 | 1613ms | 3400ms | 4840ms |
| 442.0 | 452.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | ok | 37 | 4896ms | 8972ms | 9897ms |
| 442.0 | 452.0 | end-users | ok | 226 | 1620ms | 3655ms | 4865ms |
| 452.0 | 462.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | ok | 26 | 4167ms | 8700ms | 9870ms |
| 452.0 | 462.0 | end-users | ok | 181 | 1724ms | 4016ms | 4902ms |
| 462.0 | 472.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | ok | 32 | 3542ms | 8222ms | 9822ms |
| 462.0 | 472.0 | end-users | ok | 189 | 1618ms | 3848ms | 4885ms |
| 472.0 | 482.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | ok | 36 | 2500ms | 6400ms | 9640ms |
| 472.0 | 482.0 | end-users | ok | 197 | 1579ms | 3827ms | 4883ms |
| 482.0 | 492.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | ok | 33 | 2279ms | 4558ms | 8350ms |
| 482.0 | 492.0 | end-users | ok | 214 | 1332ms | 3379ms | 4838ms |
| 492.0 | 502.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | ok | 17 | 3229ms | 4646ms | 4965ms |
| 492.0 | 502.0 | end-users | ok | 172 | 1815ms | 4122ms | 4912ms |
| 502.0 | 512.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app2 | ok | 48 | 4239ms | 8588ms | 9859ms |
| 502.0 | 512.0 | end-users | ok | 224 | 1588ms | 3444ms | 4844ms |
| 512.0 | 522.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app2 | ok | 28 | 2364ms | 5333ms | 9533ms |
| 512.0 | 522.0 | end-users | ok | 204 | 1826ms | 4177ms | 4918ms |
| 522.0 | 532.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app2 | ok | 31 | 2750ms | 4817ms | 9225ms |
| 522.0 | 532.0 | end-users | ok | 169 | 2604ms | 6870ms | 9687ms |
| 532.0 | 542.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app2 | ok | 8 | 2000ms | 6000ms | 9600ms |
| 532.0 | 542.0 | end-users | ok | 80 | 4196ms | 8710ms | 9871ms |
| 542.0 | 552.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 542.0 | 552.0 | app2 | ok | 21 | 1812ms | 3950ms | 4895ms |
| 542.0 | 552.0 | end-users | ok | 207 | 1584ms | 3985ms | 4899ms |
| 552.0 | 562.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 552.0 | 562.0 | app2 | ok | 35 | 2639ms | 8056ms | 9806ms |
| 552.0 | 562.0 | end-users | ok | 191 | 1637ms | 3863ms | 4886ms |
| 562.0 | 572.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 562.0 | 572.0 | app2 | ok | 35 | 2812ms | 7500ms | 9750ms |
| 562.0 | 572.0 | end-users | ok | 192 | 1603ms | 3909ms | 4891ms |
| 572.0 | 582.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 572.0 | 582.0 | app2 | ok | 28 | 2269ms | 6500ms | 9650ms |
| 572.0 | 582.0 | end-users | ok | 194 | 1923ms | 4218ms | 4922ms |
| 582.0 | 592.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 582.0 | 592.0 | app2 | ok | 18 | 3571ms | 4857ms | 9100ms |
| 582.0 | 592.0 | end-users | ok | 178 | 1694ms | 4033ms | 4903ms |
| 592.0 | 602.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 592.0 | 602.0 | app2 | ok | 32 | 3500ms | 6000ms | 9600ms |
| 592.0 | 602.0 | end-users | ok | 180 | 1717ms | 3953ms | 4895ms |
| 602.0 | 612.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 602.0 | 612.0 | app2 | ok | 35 | 2393ms | 6500ms | 9650ms |
| 602.0 | 612.0 | end-users | ok | 207 | 1709ms | 4059ms | 4906ms |
| 612.0 | 622.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 612.0 | 622.0 | app2 | ok | 41 | 1592ms | 3861ms | 4886ms |
| 612.0 | 622.0 | end-users | ok | 206 | 1714ms | 4127ms | 4913ms |
| 622.0 | 632.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 622.0 | 632.0 | app2 | ok | 13 | 2125ms | 8917ms | 9892ms |
| 622.0 | 632.0 | end-users | ok | 179 | 1718ms | 3881ms | 4888ms |
| 632.0 | 642.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 632.0 | 642.0 | app2 | ok | 41 | 4453ms | 8794ms | 9879ms |
| 632.0 | 642.0 | end-users | ok | 220 | 1607ms | 3553ms | 4855ms |
| 642.0 | 652.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 642.0 | 652.0 | app2 | ok | 21 | 2406ms | 4475ms | 4948ms |
| 642.0 | 652.0 | end-users | ok | 199 | 1895ms | 4223ms | 4922ms |
| 652.0 | 662.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 652.0 | 662.0 | app2 | ok | 33 | 2417ms | 4768ms | 9175ms |
| 652.0 | 662.0 | end-users | ok | 189 | 1784ms | 4108ms | 4911ms |
| 662.0 | 672.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 662.0 | 672.0 | app2 | ok | 29 | 2589ms | 4661ms | 8550ms |
| 662.0 | 672.0 | end-users | ok | 195 | 1678ms | 3940ms | 4894ms |
| 672.0 | 683.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 672.0 | 683.0 | app2 | ok | 38 | 2364ms | 6833ms | 9683ms |
| 672.0 | 683.0 | end-users | ok | 182 | 1519ms | 3863ms | 4886ms |
| 683.0 | 693.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 683.0 | 693.0 | app2 | ok | 15 | 4250ms | 8750ms | 9875ms |
| 683.0 | 693.0 | end-users | ok | 181 | 1629ms | 3869ms | 4887ms |
| 693.0 | 703.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 693.0 | 703.0 | app2 | ok | 37 | 2812ms | 7688ms | 9769ms |
| 693.0 | 703.0 | end-users | ok | 237 | 1652ms | 3791ms | 4879ms |
| 703.0 | 713.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 703.0 | 713.0 | app2 | ok | 25 | 3942ms | 8214ms | 9821ms |
| 703.0 | 713.0 | end-users | ok | 160 | 1527ms | 3095ms | 4810ms |
| 713.0 | 723.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 713.0 | 723.0 | app2 | ok | 46 | 3587ms | 7700ms | 9770ms |
| 713.0 | 723.0 | end-users | ok | 227 | 1486ms | 3169ms | 4817ms |
| 723.0 | 733.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 723.0 | 733.0 | app2 | ok | 15 | 4062ms | 7500ms | 9750ms |
| 723.0 | 733.0 | end-users | ok | 176 | 1554ms | 3743ms | 4874ms |
| 733.0 | 743.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 733.0 | 743.0 | app2 | ok | 34 | 5278ms | 9056ms | 9906ms |
| 733.0 | 743.0 | end-users | ok | 217 | 1502ms | 2740ms | 4774ms |
| 743.0 | 753.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 743.0 | 753.0 | app2 | ok | 36 | 3214ms | 7750ms | 9775ms |
| 743.0 | 753.0 | end-users | ok | 171 | 1556ms | 3417ms | 4842ms |
| 753.0 | 763.0 | app1 | ok | 61 | 3227ms | 4645ms | 4965ms |
| 753.0 | 763.0 | app2 | ok | 14 | 6818ms | 9364ms | 9936ms |
| 753.0 | 763.0 | end-users | ok | 155 | 2798ms | 4560ms | 4956ms |
| 763.0 | 773.0 | app1 | ok | 28 | 2038ms | 4300ms | 4930ms |
| 763.0 | 773.0 | app2 | ok | 25 | 5962ms | 9808ms | 27500ms |
| 763.0 | 773.0 | end-users | ok | 108 | 2857ms | 4571ms | 4957ms |
| 773.0 | 783.0 | app1 | ok | 68 | 2778ms | 4667ms | 8300ms |
| 773.0 | 783.0 | app2 | ok | 25 | 5833ms | 9167ms | 9917ms |
| 773.0 | 783.0 | end-users | ok | 216 | 2415ms | 4691ms | 8920ms |
| 783.0 | 793.0 | app1 | ok | 40 | 2167ms | 4375ms | 4938ms |
| 783.0 | 793.0 | app2 | ok | 20 | 6875ms | 9375ms | 9938ms |
| 783.0 | 793.0 | end-users | ok | 133 | 2591ms | 4518ms | 4952ms |
| 793.0 | 803.0 | app1 | ok | 41 | 2145ms | 4359ms | 4936ms |
| 793.0 | 803.0 | app2 | ok | 21 | 7237ms | 9447ms | 9945ms |
| 793.0 | 803.0 | end-users | ok | 130 | 2200ms | 4430ms | 4943ms |
| 803.0 | 813.0 | app1 | ok | 57 | 2125ms | 4352ms | 4935ms |
| 803.0 | 813.0 | app2 | ok | 26 | 7174ms | 9435ms | 9943ms |
| 803.0 | 813.0 | end-users | ok | 172 | 2584ms | 4517ms | 4952ms |
| 813.0 | 823.0 | app1 | ok | 47 | 1958ms | 4309ms | 4931ms |
| 813.0 | 823.0 | app2 | ok | 30 | 6739ms | 9348ms | 9935ms |
| 813.0 | 823.0 | end-users | ok | 175 | 2487ms | 4497ms | 4950ms |
| 823.0 | 833.0 | app1 | ok | 36 | 2750ms | 4550ms | 4955ms |
| 823.0 | 833.0 | app2 | ok | 14 | 7308ms | 9462ms | 9946ms |
| 823.0 | 833.0 | end-users | ok | 97 | 2795ms | 4559ms | 4956ms |
| 833.0 | 843.0 | app1 | ok | 48 | 3148ms | 4926ms | 9400ms |
| 833.0 | 843.0 | app2 | ok | 22 | 5000ms | 9000ms | 9900ms |
| 833.0 | 843.0 | end-users | ok | 152 | 3584ms | 4929ms | 9367ms |
| 843.0 | 853.0 | app1 | ok | 56 | 2429ms | 4481ms | 4948ms |
| 843.0 | 853.0 | app2 | ok | 27 | 6447ms | 9289ms | 9929ms |
| 843.0 | 853.0 | end-users | ok | 183 | 2327ms | 4455ms | 4946ms |
| 853.0 | 863.0 | app1 | ok | 37 | 1865ms | 4288ms | 4929ms |
| 853.0 | 863.0 | app2 | ok | 20 | 7500ms | 9500ms | 9950ms |
| 853.0 | 863.0 | end-users | ok | 128 | 2778ms | 4556ms | 4956ms |
| 863.0 | 873.0 | app1 | ok | 55 | 1802ms | 4018ms | 4902ms |
| 863.0 | 873.0 | app2 | ok | 39 | 6750ms | 9350ms | 9935ms |
| 863.0 | 873.0 | end-users | ok | 198 | 2955ms | 4591ms | 4959ms |
| 873.0 | 883.0 | app1 | ok | 46 | 2500ms | 4500ms | 4950ms |
| 873.0 | 883.0 | app2 | ok | 11 | 7250ms | 9450ms | 9945ms |
| 873.0 | 883.0 | end-users | ok | 135 | 2065ms | 4363ms | 4936ms |
| 883.0 | 893.0 | app1 | ok | 41 | 2266ms | 4431ms | 4943ms |
| 883.0 | 893.0 | app2 | ok | 26 | 5000ms | 9000ms | 9900ms |
| 883.0 | 893.0 | end-users | ok | 134 | 2033ms | 4368ms | 4937ms |
| 893.0 | 903.0 | app1 | ok | 4 | 3750ms | 4750ms | 4975ms |
| 893.0 | 903.0 | app2 | ok | 11 | 6071ms | 9214ms | 9921ms |
| 893.0 | 903.0 | end-users | ok | 17 | 3750ms | 4750ms | 4975ms |
| 903.0 | 913.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 903.0 | 913.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 903.0 | 913.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 913.0 | 923.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 913.0 | 923.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 913.0 | 923.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 923.0 | 933.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 923.0 | 933.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 923.0 | 933.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 933.0 | 944.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 933.0 | 944.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 933.0 | 944.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 944.0 | 954.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 944.0 | 954.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 944.0 | 954.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 954.0 | 964.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 954.0 | 964.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 954.0 | 964.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 964.0 | 974.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 964.0 | 974.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 964.0 | 974.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 974.0 | 984.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 974.0 | 984.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 974.0 | 984.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 984.0 | 994.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 984.0 | 994.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 984.0 | 994.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 994.0 | 1004.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 994.0 | 1004.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 994.0 | 1004.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1004.0 | 1014.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1004.0 | 1014.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1004.0 | 1014.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1014.0 | 1024.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1014.0 | 1024.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1014.0 | 1024.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1024.0 | 1034.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1024.0 | 1034.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1024.0 | 1034.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1034.0 | 1044.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1034.0 | 1044.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1034.0 | 1044.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1044.0 | 1054.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1044.0 | 1054.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1044.0 | 1054.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1054.0 | 1064.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1054.0 | 1064.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1054.0 | 1064.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1064.0 | 1074.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1064.0 | 1074.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1064.0 | 1074.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1074.0 | 1084.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1074.0 | 1084.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1074.0 | 1084.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1084.0 | 1094.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1084.0 | 1094.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1084.0 | 1094.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1094.0 | 1104.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1094.0 | 1104.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1094.0 | 1104.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1104.0 | 1114.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1104.0 | 1114.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1104.0 | 1114.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1114.0 | 1124.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1114.0 | 1124.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1114.0 | 1124.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1124.0 | 1134.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1124.0 | 1134.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1124.0 | 1134.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1134.0 | 1144.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1134.0 | 1144.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1134.0 | 1144.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1144.0 | 1154.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1144.0 | 1154.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1144.0 | 1154.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1154.0 | 1164.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1154.0 | 1164.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1154.0 | 1164.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1164.0 | 1174.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1164.0 | 1174.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1164.0 | 1174.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1174.0 | 1177.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1174.0 | 1177.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1174.0 | 1177.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1702320 | 84737 | 1787057.0 | 0.0% | 1829882.0 | 1871794.0 | -2.2% | True |
| app2 | 3045480 | 152201 | 3197681.0 | 0.0% | 3321460.0 | 3349882.0 | -0.8% | True |
| end-users | 19688610 | 981152 | 20669762.0 | 0.0% | 21454666.0 | 21650914.0 | -0.9% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1386 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | 0.0% | 0.00 |
| app2 | 2477 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | 0.0% | 0.00 |
| end-users | 16019 | 0 | 1 | 1 | 0.01% | 68.4% | 100.0% | 1.46 |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=19882). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 19882 | 0.051ms | 0.126ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 1121295 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1384 | 6675ms | 9398ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 2476 | 11786ms | 14995ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 16007 | 6871ms | 9760ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 19867 | 7124ms | 13002ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (118 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 1833ms | 5700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 4250ms | 5840ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2690ms | 4808ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 6000ms | 9350ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 10769ms | 14577ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 7538ms | 12019ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 6222ms | 9444ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 13125ms | 18750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 8381ms | 13519ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 6829ms | 7986ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 13333ms | 19000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 7890ms | 9812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 6833ms | 9217ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 12609ms | 14957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 8239ms | 9844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 6688ms | 8400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 12614ms | 14966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 8200ms | 9820ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 7031ms | 9283ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 16042ms | 19604ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 8973ms | 13917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 7074ms | 9592ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 13750ms | 19250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 8114ms | 11200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 7143ms | 9560ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 13333ms | 19000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 8972ms | 13892ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 6875ms | 8900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 15625ms | 19562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 8522ms | 13616ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 6522ms | 9375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 7857ms | 9785ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 6786ms | 9120ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 12841ms | 17917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 8074ms | 11771ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 6581ms | 7974ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 12604ms | 14948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 7902ms | 9789ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 6559ms | 7856ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 7987ms | 9799ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 6464ms | 7975ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 12614ms | 14966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | end-users | ok | 7917ms | 9842ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 6667ms | 9640ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 13472ms | 19107ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | end-users | ok | 8080ms | 13700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 12222ms | 14722ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | end-users | ok | 6565ms | 9400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 181.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 181.0 | app2 | ok | 11250ms | 14625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 181.0 | end-users | ok | 6452ms | 7845ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 11848ms | 14685ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 6246ms | 7825ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 11250ms | 14625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 6453ms | 7845ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 11364ms | 14636ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 6452ms | 7845ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 11667ms | 14667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 6126ms | 8781ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 9833ms | 14481ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 6233ms | 9431ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 12000ms | 14700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 6602ms | 8700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 12100ms | 14710ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 6435ms | 8392ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 12315ms | 14731ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 6500ms | 9307ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | ok | 9941ms | 14484ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | ok | 6449ms | 8693ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | ok | 10208ms | 14521ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | end-users | ok | 6149ms | 9343ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | ok | 11897ms | 14690ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | end-users | ok | 6479ms | 9136ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | ok | 10588ms | 14559ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | end-users | ok | 6493ms | 9564ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app2 | ok | 10833ms | 14583ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | end-users | ok | 6496ms | 7986ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app2 | ok | 12019ms | 14702ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | end-users | ok | 6298ms | 8958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app2 | ok | 11500ms | 14650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | end-users | ok | 6267ms | 8209ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app2 | ok | 9923ms | 14484ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | end-users | ok | 6670ms | 9464ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app2 | ok | 12143ms | 14714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | end-users | ok | 6287ms | 8794ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app2 | ok | 10000ms | 14500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | end-users | ok | 6511ms | 9317ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app2 | ok | 10789ms | 14579ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | end-users | ok | 6617ms | 7929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app2 | ok | 11711ms | 14671ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | end-users | ok | 6322ms | 7832ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app2 | ok | 11900ms | 14690ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | end-users | ok | 6491ms | 8894ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app2 | ok | 9706ms | 14396ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | end-users | ok | 6530ms | 7867ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | app2 | ok | 11635ms | 14663ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | end-users | ok | 6512ms | 9421ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | app2 | ok | 11375ms | 14638ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | end-users | ok | 6524ms | 7952ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 432.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 432.0 | app2 | ok | 11630ms | 14663ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 432.0 | end-users | ok | 6630ms | 8781ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app2 | ok | 11250ms | 14625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | end-users | ok | 6476ms | 9015ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app2 | ok | 11477ms | 14648ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | end-users | ok | 6505ms | 8614ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app2 | ok | 12000ms | 14700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | end-users | ok | 6466ms | 7969ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app2 | ok | 10833ms | 14583ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | end-users | ok | 6513ms | 8218ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app2 | ok | 12315ms | 14731ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | end-users | ok | 6238ms | 7961ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app2 | ok | 11667ms | 14667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | end-users | ok | 6304ms | 8979ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app2 | ok | 9933ms | 14482ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | end-users | ok | 6471ms | 9418ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app2 | ok | 9667ms | 14417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | end-users | ok | 6733ms | 9132ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app2 | ok | 11750ms | 14675ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | end-users | ok | 6586ms | 8538ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app2 | ok | 11364ms | 14636ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | end-users | ok | 6875ms | 9350ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | app2 | ok | 12955ms | 18375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | end-users | ok | 9717ms | 14420ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 552.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 552.0 | app2 | ok | 16389ms | 19639ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 552.0 | end-users | ok | 7203ms | 13010ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 552.0 | 562.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 552.0 | 562.0 | app2 | ok | 9636ms | 14367ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 552.0 | 562.0 | end-users | ok | 6690ms | 8906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 562.0 | 572.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 562.0 | 572.0 | app2 | ok | 11667ms | 14667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 562.0 | 572.0 | end-users | ok | 6500ms | 8375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 572.0 | 582.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 572.0 | 582.0 | app2 | ok | 11905ms | 14690ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 572.0 | 582.0 | end-users | ok | 6530ms | 8110ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 582.0 | 592.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 582.0 | 592.0 | app2 | ok | 11548ms | 14655ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 582.0 | 592.0 | end-users | ok | 6646ms | 9418ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 592.0 | 602.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 592.0 | 602.0 | app2 | ok | 10694ms | 14569ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 592.0 | 602.0 | end-users | ok | 6608ms | 9334ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 602.0 | 612.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 602.0 | 612.0 | app2 | ok | 12419ms | 14742ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 602.0 | 612.0 | end-users | ok | 6403ms | 9427ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 612.0 | 622.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 612.0 | 622.0 | app2 | ok | 9045ms | 13750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 612.0 | 622.0 | end-users | ok | 6505ms | 9081ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 622.0 | 632.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 622.0 | 632.0 | app2 | ok | 11071ms | 14607ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 622.0 | 632.0 | end-users | ok | 6310ms | 8806ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 632.0 | 642.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 632.0 | 642.0 | app2 | ok | 11250ms | 14625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 632.0 | 642.0 | end-users | ok | 6075ms | 9030ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 642.0 | 652.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 642.0 | 652.0 | app2 | ok | 10395ms | 14539ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 642.0 | 652.0 | end-users | ok | 6610ms | 9196ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 652.0 | 662.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 652.0 | 662.0 | app2 | ok | 10000ms | 14500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 652.0 | 662.0 | end-users | ok | 6184ms | 9382ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 662.0 | 672.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 662.0 | 672.0 | app2 | ok | 10263ms | 14526ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 662.0 | 672.0 | end-users | ok | 6654ms | 9145ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 672.0 | 683.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 672.0 | 683.0 | app2 | ok | 11429ms | 14643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 672.0 | 683.0 | end-users | ok | 6398ms | 7886ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 683.0 | 693.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 683.0 | 693.0 | app2 | ok | 11190ms | 14619ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 683.0 | 693.0 | end-users | ok | 6359ms | 7836ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 693.0 | 703.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 693.0 | 703.0 | app2 | ok | 10500ms | 14550ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 693.0 | 703.0 | end-users | ok | 6395ms | 7840ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 703.0 | 713.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 703.0 | 713.0 | app2 | ok | 11739ms | 14674ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 703.0 | 713.0 | end-users | ok | 6375ms | 7838ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 713.0 | 723.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 713.0 | 723.0 | app2 | ok | 11591ms | 14659ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 713.0 | 723.0 | end-users | ok | 6421ms | 9118ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 723.0 | 733.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 723.0 | 733.0 | app2 | ok | 9917ms | 14483ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 723.0 | 733.0 | end-users | ok | 6269ms | 7877ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 733.0 | 743.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 733.0 | 743.0 | app2 | ok | 11429ms | 14643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 733.0 | 743.0 | end-users | ok | 6296ms | 7930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 743.0 | 753.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 743.0 | 753.0 | app2 | ok | 10667ms | 14567ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 743.0 | 753.0 | end-users | ok | 6262ms | 7944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 753.0 | 763.0 | app1 | ok | 5417ms | 9383ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 753.0 | 763.0 | app2 | ok | 12188ms | 14719ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 753.0 | 763.0 | end-users | ok | 7308ms | 9663ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 763.0 | 773.0 | app1 | ok | 7290ms | 9956ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 763.0 | 773.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 763.0 | 773.0 | end-users | ok | 7861ms | 9784ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 773.0 | 783.0 | app1 | ok | 6409ms | 9100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 773.0 | 783.0 | app2 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 773.0 | 783.0 | end-users | ok | 8477ms | 13510ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 783.0 | 793.0 | app1 | ok | 6636ms | 9467ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 783.0 | 793.0 | app2 | ok | 13500ms | 19179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 783.0 | 793.0 | end-users | ok | 7859ms | 12268ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 793.0 | 803.0 | app1 | ok | 6389ms | 9690ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 793.0 | 803.0 | app2 | ok | 12609ms | 16750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 793.0 | 803.0 | end-users | ok | 8000ms | 12286ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 803.0 | 813.0 | app1 | ok | 6750ms | 9550ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 803.0 | 813.0 | app2 | ok | 12632ms | 15000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 803.0 | 813.0 | end-users | ok | 7908ms | 11923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 813.0 | 823.0 | app1 | ok | 6909ms | 9286ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 813.0 | 823.0 | app2 | ok | 12826ms | 17833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 813.0 | 823.0 | end-users | ok | 8127ms | 10806ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 823.0 | 833.0 | app1 | ok | 6522ms | 8950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 823.0 | 833.0 | app2 | ok | 12262ms | 14726ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 823.0 | 833.0 | end-users | ok | 8157ms | 11275ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 833.0 | 843.0 | app1 | ok | 7368ms | 11167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 833.0 | 843.0 | app2 | ok | 15250ms | 19525ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 833.0 | 843.0 | end-users | ok | 8833ms | 14096ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 843.0 | 853.0 | app1 | ok | 6762ms | 9564ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 843.0 | 853.0 | app2 | ok | 12727ms | 17833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 843.0 | 853.0 | end-users | ok | 8088ms | 11545ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 853.0 | 863.0 | app1 | ok | 6500ms | 7914ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 853.0 | 863.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 853.0 | 863.0 | end-users | ok | 8070ms | 10219ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 863.0 | 873.0 | app1 | ok | 7111ms | 11167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 863.0 | 873.0 | app2 | ok | 12976ms | 18438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 863.0 | 873.0 | end-users | ok | 8085ms | 13155ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 873.0 | 883.0 | app1 | ok | 5975ms | 9150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 873.0 | 883.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 873.0 | 883.0 | end-users | ok | 7892ms | 9789ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 883.0 | 893.0 | app1 | ok | 6278ms | 9412ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 883.0 | 893.0 | app2 | ok | 12619ms | 14976ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 883.0 | 893.0 | end-users | ok | 7883ms | 10156ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 893.0 | 903.0 | app1 | ok | 7091ms | 9600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 893.0 | 903.0 | app2 | ok | 11375ms | 14638ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 893.0 | 903.0 | end-users | ok | 8122ms | 9812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 903.0 | 913.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 903.0 | 913.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 903.0 | 913.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 913.0 | 923.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 913.0 | 923.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 913.0 | 923.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 923.0 | 933.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 923.0 | 933.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 923.0 | 933.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 933.0 | 944.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 933.0 | 944.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 933.0 | 944.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 944.0 | 954.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 944.0 | 954.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 944.0 | 954.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 954.0 | 964.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 954.0 | 964.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 954.0 | 964.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 964.0 | 974.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 964.0 | 974.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 964.0 | 974.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 974.0 | 984.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 974.0 | 984.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 974.0 | 984.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 984.0 | 994.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 984.0 | 994.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 984.0 | 994.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 994.0 | 1004.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 994.0 | 1004.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 994.0 | 1004.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1004.0 | 1014.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1004.0 | 1014.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1004.0 | 1014.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1014.0 | 1024.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1014.0 | 1024.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1014.0 | 1024.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1024.0 | 1034.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1024.0 | 1034.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1024.0 | 1034.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1034.0 | 1044.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1034.0 | 1044.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1034.0 | 1044.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1044.0 | 1054.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1044.0 | 1054.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1044.0 | 1054.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1054.0 | 1064.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1054.0 | 1064.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1054.0 | 1064.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1064.0 | 1074.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1064.0 | 1074.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1064.0 | 1074.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1074.0 | 1084.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1074.0 | 1084.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1074.0 | 1084.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1084.0 | 1094.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1084.0 | 1094.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1084.0 | 1094.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1094.0 | 1104.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1094.0 | 1104.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1094.0 | 1104.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1104.0 | 1114.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1104.0 | 1114.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1104.0 | 1114.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1114.0 | 1124.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1114.0 | 1124.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1114.0 | 1124.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1124.0 | 1134.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1124.0 | 1134.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1124.0 | 1134.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1134.0 | 1144.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1134.0 | 1144.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1134.0 | 1144.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1144.0 | 1154.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1144.0 | 1154.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1144.0 | 1154.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1154.0 | 1164.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1154.0 | 1164.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1154.0 | 1164.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1164.0 | 1174.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1164.0 | 1174.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1164.0 | 1174.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1174.0 | 1177.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1174.0 | 1177.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1174.0 | 1177.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
