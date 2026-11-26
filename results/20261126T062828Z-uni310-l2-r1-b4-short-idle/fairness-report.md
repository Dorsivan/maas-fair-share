# Fairness benchmark: full-contention (uni310-l2-r1-b4-short-idle)

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
| Duration (s) | `320` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-8448f688f-c5kj8` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T06:29:48Z` |
| Run end | `2026-11-26T06:40:20Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 64 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/64 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 60.00 | 1.8750 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1413 | 200=1413 | 6.7 | 8.9 | 1881368.0 | 19.1% | 16.7% | -4.4 | 18.9% | -0.2 | 19.3% | -1.8 | 101.3s | 98.9% | 1413.0 |
| app2 | 10.0 | 32 | 800 | 200=800 | 13.2 | 15.8 | 1062948.0 | 10.8% | 16.7% | 6.1 | 10.8% | 0.0 | 10.9% | 0.4 | 109.3s | 98.9% | 800.0 |
| end-users | 65.0 | 128 | 5115 | 000=5, 200=5110 | 8.0 | 10.4 | 6808302.0 | 70.1% | 66.7% | -1.8 | 70.3% | 0.2 | 69.8% | 1.4 | 109.3s | 98.9% | 5115.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-320s, 150s on / 30s off
- app2: active 0s-320s, no duty cycle
- end-users: active 0s-320s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 10.0 | 10.0 |
| 150.0 | 151.0 | 1.0 |
| 180.0 | 181.0 | 1.0 |
| 320.0 | n/a (never converged in this phase) | n/a |

**Windows** (63 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 12190.0 | 21.1% | 39.2% | 18.1 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | False | 18920.0 | 68.4% | 60.8% | -7.6 |
| 10.0 | 20.0 | app1 | True | False | 66312.0 | 21.1% | 21.4% | 0.4 |
| 10.0 | 20.0 | app2 | True | False | 31120.0 | 10.5% | 10.1% | -0.5 |
| 10.0 | 20.0 | end-users | True | False | 212184.0 | 68.4% | 68.5% | 0.1 |
| 20.0 | 30.0 | app1 | True | False | 59612.0 | 21.1% | 23.4% | 2.4 |
| 20.0 | 30.0 | app2 | True | False | 27102.0 | 10.5% | 10.6% | 0.1 |
| 20.0 | 30.0 | end-users | True | False | 167802.0 | 68.4% | 65.9% | -2.5 |
| 30.0 | 40.0 | app1 | True | False | 58254.0 | 21.1% | 18.6% | -2.5 |
| 30.0 | 40.0 | app2 | True | False | 33834.0 | 10.5% | 10.8% | 0.3 |
| 30.0 | 40.0 | end-users | True | False | 221706.0 | 68.4% | 70.7% | 2.2 |
| 40.0 | 50.0 | app1 | True | False | 64954.0 | 21.1% | 21.4% | 0.4 |
| 40.0 | 50.0 | app2 | True | False | 32430.0 | 10.5% | 10.7% | 0.2 |
| 40.0 | 50.0 | end-users | True | False | 205618.0 | 68.4% | 67.9% | -0.6 |
| 50.0 | 60.0 | app1 | True | False | 63582.0 | 21.1% | 20.9% | -0.2 |
| 50.0 | 60.0 | app2 | True | False | 31112.0 | 10.5% | 10.2% | -0.3 |
| 50.0 | 60.0 | end-users | True | False | 209554.0 | 68.4% | 68.9% | 0.5 |
| 60.0 | 70.0 | app1 | True | False | 64884.0 | 21.1% | 21.0% | -0.1 |
| 60.0 | 70.0 | app2 | True | False | 33862.0 | 10.5% | 10.9% | 0.4 |
| 60.0 | 70.0 | end-users | True | False | 210832.0 | 68.4% | 68.1% | -0.3 |
| 70.0 | 80.0 | app1 | True | False | 64934.0 | 21.1% | 21.2% | 0.2 |
| 70.0 | 80.0 | app2 | True | False | 31096.0 | 10.5% | 10.2% | -0.4 |
| 70.0 | 80.0 | end-users | True | False | 209640.0 | 68.4% | 68.6% | 0.2 |
| 80.0 | 90.0 | app1 | True | False | 63582.0 | 21.1% | 20.7% | -0.3 |
| 80.0 | 90.0 | app2 | True | False | 33766.0 | 10.5% | 11.0% | 0.5 |
| 80.0 | 90.0 | end-users | True | False | 209562.0 | 68.4% | 68.3% | -0.1 |
| 90.0 | 100.0 | app1 | True | False | 64824.0 | 21.1% | 21.3% | 0.3 |
| 90.0 | 100.0 | app2 | True | False | 31180.0 | 10.5% | 10.2% | -0.3 |
| 90.0 | 100.0 | end-users | True | False | 208230.0 | 68.4% | 68.4% | 0.0 |
| 100.0 | 110.0 | app1 | True | False | 66198.0 | 21.1% | 21.3% | 0.2 |
| 100.0 | 110.0 | app2 | True | False | 31078.0 | 10.5% | 10.0% | -0.5 |
| 100.0 | 110.0 | end-users | True | False | 213760.0 | 68.4% | 68.7% | 0.3 |
| 110.0 | 120.0 | app1 | True | False | 62180.0 | 21.1% | 20.4% | -0.6 |
| 110.0 | 120.0 | app2 | True | False | 32500.0 | 10.5% | 10.7% | 0.2 |
| 110.0 | 120.0 | end-users | True | False | 209630.0 | 68.4% | 68.9% | 0.5 |
| 120.0 | 130.0 | app1 | True | False | 66258.0 | 21.1% | 21.7% | 0.6 |
| 120.0 | 130.0 | app2 | True | False | 32430.0 | 10.5% | 10.6% | 0.1 |
| 120.0 | 130.0 | end-users | True | False | 206802.0 | 68.4% | 67.7% | -0.7 |
| 130.0 | 140.0 | app1 | True | False | 64904.0 | 21.1% | 21.2% | 0.1 |
| 130.0 | 140.0 | app2 | True | False | 33826.0 | 10.5% | 11.0% | 0.5 |
| 130.0 | 140.0 | end-users | True | False | 208076.0 | 68.4% | 67.8% | -0.6 |
| 140.0 | 151.0 | app1 | True | False | 62234.0 | 21.1% | 20.7% | -0.3 |
| 140.0 | 151.0 | app2 | True | False | 31102.0 | 10.5% | 10.4% | -0.2 |
| 140.0 | 151.0 | end-users | True | False | 206880.0 | 68.4% | 68.9% | 0.5 |
| 151.0 | 161.0 | app1 | False | n/a | 55388.0 | n/a | n/a | n/a |
| 151.0 | 161.0 | app2 | True | False | 31112.0 | 13.3% | 12.2% | -1.1 |
| 151.0 | 161.0 | end-users | True | False | 223100.0 | 86.7% | 87.8% | 1.1 |
| 161.0 | 171.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 161.0 | 171.0 | app2 | True | False | 43272.0 | 13.3% | 14.0% | 0.6 |
| 161.0 | 171.0 | end-users | True | False | 266246.0 | 86.7% | 86.0% | -0.6 |
| 171.0 | 181.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 171.0 | 181.0 | app2 | True | False | 41888.0 | 13.3% | 13.7% | 0.4 |
| 171.0 | 181.0 | end-users | True | False | 263516.0 | 86.7% | 86.3% | -0.4 |
| 181.0 | 191.0 | app1 | True | False | 37900.0 | 21.1% | 12.6% | -8.5 |
| 181.0 | 191.0 | app2 | True | False | 36542.0 | 10.5% | 12.1% | 1.6 |
| 181.0 | 191.0 | end-users | True | False | 227194.0 | 68.4% | 75.3% | 6.9 |
| 191.0 | 201.0 | app1 | True | False | 67634.0 | 21.1% | 21.9% | 0.9 |
| 191.0 | 201.0 | app2 | True | False | 31122.0 | 10.5% | 10.1% | -0.4 |
| 191.0 | 201.0 | end-users | True | False | 209614.0 | 68.4% | 68.0% | -0.4 |
| 201.0 | 211.0 | app1 | True | False | 63446.0 | 21.1% | 20.7% | -0.4 |
| 201.0 | 211.0 | app2 | True | False | 32380.0 | 10.5% | 10.6% | 0.0 |
| 201.0 | 211.0 | end-users | True | False | 211082.0 | 68.4% | 68.8% | 0.4 |
| 211.0 | 221.0 | app1 | True | False | 64988.0 | 21.1% | 21.0% | -0.1 |
| 211.0 | 221.0 | app2 | True | False | 32378.0 | 10.5% | 10.5% | -0.1 |
| 211.0 | 221.0 | end-users | True | False | 212202.0 | 68.4% | 68.5% | 0.1 |
| 221.0 | 231.0 | app1 | True | False | 62204.0 | 21.1% | 20.6% | -0.4 |
| 221.0 | 231.0 | app2 | True | False | 32532.0 | 10.5% | 10.8% | 0.3 |
| 221.0 | 231.0 | end-users | True | False | 207008.0 | 68.4% | 68.6% | 0.2 |
| 231.0 | 241.0 | app1 | True | False | 64982.0 | 21.1% | 21.2% | 0.1 |
| 231.0 | 241.0 | app2 | True | False | 31100.0 | 10.5% | 10.1% | -0.4 |
| 231.0 | 241.0 | end-users | True | False | 211050.0 | 68.4% | 68.7% | 0.3 |
| 241.0 | 251.0 | app1 | True | False | 70364.0 | 21.1% | 23.2% | 2.2 |
| 241.0 | 251.0 | app2 | True | False | 29774.0 | 10.5% | 9.8% | -0.7 |
| 241.0 | 251.0 | end-users | True | False | 202938.0 | 68.4% | 67.0% | -1.5 |
| 251.0 | 261.0 | app1 | True | False | 58144.0 | 21.1% | 18.9% | -2.1 |
| 251.0 | 261.0 | app2 | True | False | 36414.0 | 10.5% | 11.9% | 1.3 |
| 251.0 | 261.0 | end-users | True | False | 212310.0 | 68.4% | 69.2% | 0.8 |
| 261.0 | 271.0 | app1 | True | False | 70330.0 | 21.1% | 23.1% | 2.1 |
| 261.0 | 271.0 | app2 | True | False | 27058.0 | 10.5% | 8.9% | -1.6 |
| 261.0 | 271.0 | end-users | True | False | 206888.0 | 68.4% | 68.0% | -0.4 |
| 271.0 | 281.0 | app1 | True | False | 52714.0 | 21.1% | 18.1% | -2.9 |
| 271.0 | 281.0 | app2 | True | False | 31114.0 | 10.5% | 10.7% | 0.2 |
| 271.0 | 281.0 | end-users | True | False | 206744.0 | 68.4% | 71.2% | 2.7 |
| 281.0 | 291.0 | app1 | True | False | 63566.0 | 21.1% | 20.5% | -0.5 |
| 281.0 | 291.0 | app2 | True | False | 35088.0 | 10.5% | 11.3% | 0.8 |
| 281.0 | 291.0 | end-users | True | False | 211034.0 | 68.4% | 68.1% | -0.3 |
| 291.0 | 301.0 | app1 | True | False | 64844.0 | 21.1% | 20.9% | -0.1 |
| 291.0 | 301.0 | app2 | True | False | 33776.0 | 10.5% | 10.9% | 0.4 |
| 291.0 | 301.0 | end-users | True | False | 210958.0 | 68.4% | 68.1% | -0.3 |
| 301.0 | 311.0 | app1 | True | False | 67696.0 | 21.1% | 22.0% | 1.0 |
| 301.0 | 311.0 | app2 | True | False | 31144.0 | 10.5% | 10.1% | -0.4 |
| 301.0 | 311.0 | end-users | True | False | 208254.0 | 68.4% | 67.8% | -0.6 |
| 311.0 | 321.0 | app1 | True | False | 62202.0 | 21.1% | 20.7% | -0.3 |
| 311.0 | 321.0 | app2 | True | False | 32436.0 | 10.5% | 10.8% | 0.3 |
| 311.0 | 321.0 | end-users | True | False | 205602.0 | 68.4% | 68.5% | 0.1 |
| 321.0 | 331.0 | app1 | False | n/a | 50064.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | n/a | 35198.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | False | n/a | 167656.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | n/a | 12182.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | False | n/a | 25710.0 | n/a | n/a | n/a |
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
| 391.0 | 402.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 402.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 402.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 542.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 542.0 | 552.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 542.0 | 552.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 542.0 | 552.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 552.0 | 562.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 552.0 | 562.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 552.0 | 562.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 562.0 | 572.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 562.0 | 572.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 562.0 | 572.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 572.0 | 582.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 572.0 | 582.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 572.0 | 582.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 582.0 | 592.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 582.0 | 592.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 582.0 | 592.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 592.0 | 602.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 592.0 | 602.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 592.0 | 602.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 602.0 | 612.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 602.0 | 612.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 602.0 | 612.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 612.0 | 622.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 612.0 | 622.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 612.0 | 622.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 622.0 | 632.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 622.0 | 632.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 622.0 | 632.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 53 | 569ms | 2069ms | 4558ms |
| 0.0 | 10.0 | app2 | ok | 27 | 0ms | 4036ms | 4904ms |
| 0.0 | 10.0 | end-users | ok | 170 | 611ms | 3786ms | 4879ms |
| 10.0 | 20.0 | app1 | ok | 48 | 2071ms | 4250ms | 4925ms |
| 10.0 | 20.0 | app2 | ok | 24 | 7609ms | 9696ms | 25200ms |
| 10.0 | 20.0 | end-users | ok | 156 | 3587ms | 4717ms | 4972ms |
| 20.0 | 30.0 | app1 | ok | 41 | 2917ms | 7437ms | 9744ms |
| 20.0 | 30.0 | app2 | ok | 24 | 5000ms | 9000ms | 9900ms |
| 20.0 | 30.0 | end-users | ok | 148 | 3400ms | 7154ms | 9715ms |
| 30.0 | 40.0 | app1 | ok | 53 | 2634ms | 4527ms | 4953ms |
| 30.0 | 40.0 | app2 | ok | 24 | 9286ms | 25200ms | 29520ms |
| 30.0 | 40.0 | end-users | ok | 167 | 3467ms | 4771ms | 8330ms |
| 40.0 | 50.0 | app1 | ok | 42 | 2214ms | 4382ms | 4938ms |
| 40.0 | 50.0 | app2 | ok | 20 | 7500ms | 9500ms | 9950ms |
| 40.0 | 50.0 | end-users | ok | 130 | 3536ms | 4707ms | 4971ms |
| 50.0 | 60.0 | app1 | ok | 48 | 2062ms | 4294ms | 4929ms |
| 50.0 | 60.0 | app2 | ok | 24 | 7500ms | 9500ms | 9950ms |
| 50.0 | 60.0 | end-users | ok | 154 | 3553ms | 4711ms | 4971ms |
| 60.0 | 70.0 | app1 | ok | 41 | 1784ms | 3975ms | 4897ms |
| 60.0 | 70.0 | app2 | ok | 20 | 7500ms | 9500ms | 9950ms |
| 60.0 | 70.0 | end-users | ok | 133 | 3370ms | 4674ms | 4967ms |
| 70.0 | 80.0 | app1 | ok | 50 | 1938ms | 4219ms | 4922ms |
| 70.0 | 80.0 | app2 | ok | 26 | 7500ms | 9500ms | 9950ms |
| 70.0 | 80.0 | end-users | ok | 163 | 3456ms | 4691ms | 4969ms |
| 80.0 | 90.0 | app1 | ok | 46 | 1711ms | 4115ms | 4912ms |
| 80.0 | 90.0 | app2 | ok | 22 | 7750ms | 9950ms | 27800ms |
| 80.0 | 90.0 | end-users | ok | 145 | 3290ms | 4658ms | 4966ms |
| 90.0 | 100.0 | app1 | ok | 52 | 1964ms | 4188ms | 4919ms |
| 90.0 | 100.0 | app2 | ok | 27 | 7596ms | 9673ms | 24600ms |
| 90.0 | 100.0 | end-users | ok | 175 | 3426ms | 4685ms | 4969ms |
| 100.0 | 110.0 | app1 | ok | 48 | 2179ms | 4333ms | 4933ms |
| 100.0 | 110.0 | app2 | ok | 23 | 7614ms | 9705ms | 25400ms |
| 100.0 | 110.0 | end-users | ok | 155 | 3596ms | 4719ms | 4972ms |
| 110.0 | 120.0 | app1 | ok | 49 | 1905ms | 4058ms | 4906ms |
| 110.0 | 120.0 | app2 | ok | 24 | 7500ms | 9500ms | 9950ms |
| 110.0 | 120.0 | end-users | ok | 158 | 3666ms | 4733ms | 4973ms |
| 120.0 | 130.0 | app1 | ok | 40 | 1571ms | 3571ms | 4857ms |
| 120.0 | 130.0 | app2 | ok | 21 | 7500ms | 9500ms | 9950ms |
| 120.0 | 130.0 | end-users | ok | 130 | 3422ms | 4684ms | 4968ms |
| 130.0 | 140.0 | app1 | ok | 51 | 1830ms | 4019ms | 4902ms |
| 130.0 | 140.0 | app2 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 130.0 | 140.0 | end-users | ok | 167 | 3498ms | 4700ms | 4970ms |
| 140.0 | 151.0 | app1 | ok | 56 | 1889ms | 4176ms | 4918ms |
| 140.0 | 151.0 | app2 | ok | 42 | 6774ms | 9484ms | 21600ms |
| 140.0 | 151.0 | end-users | ok | 207 | 3191ms | 4638ms | 4964ms |
| 151.0 | 161.0 | app1 | ok | 11 | 3750ms | 4750ms | 4975ms |
| 151.0 | 161.0 | app2 | ok | 12 | 7500ms | 9500ms | 9950ms |
| 151.0 | 161.0 | end-users | ok | 150 | 2500ms | 4500ms | 4950ms |
| 161.0 | 171.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 40 | 3594ms | 8182ms | 9818ms |
| 161.0 | 171.0 | end-users | ok | 182 | 1628ms | 3890ms | 4889ms |
| 171.0 | 181.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 21 | 5625ms | 9125ms | 9912ms |
| 171.0 | 181.0 | end-users | ok | 209 | 1814ms | 3975ms | 4898ms |
| 181.0 | 191.0 | app1 | ok | 45 | 1772ms | 3125ms | 4812ms |
| 181.0 | 191.0 | app2 | ok | 22 | 7250ms | 9450ms | 9945ms |
| 181.0 | 191.0 | end-users | ok | 132 | 2213ms | 4377ms | 4938ms |
| 191.0 | 201.0 | app1 | ok | 49 | 2470ms | 4490ms | 4949ms |
| 191.0 | 201.0 | app2 | ok | 20 | 7778ms | 10000ms | 28000ms |
| 191.0 | 201.0 | end-users | ok | 141 | 3612ms | 4722ms | 4972ms |
| 201.0 | 211.0 | app1 | ok | 49 | 2089ms | 4234ms | 4923ms |
| 201.0 | 211.0 | app2 | ok | 25 | 7604ms | 9688ms | 25000ms |
| 201.0 | 211.0 | end-users | ok | 163 | 3479ms | 4696ms | 4970ms |
| 211.0 | 221.0 | app1 | ok | 52 | 2000ms | 4235ms | 4924ms |
| 211.0 | 221.0 | app2 | ok | 26 | 7500ms | 9500ms | 9950ms |
| 211.0 | 221.0 | end-users | ok | 168 | 3385ms | 4677ms | 4968ms |
| 221.0 | 231.0 | app1 | ok | 42 | 1786ms | 4045ms | 4905ms |
| 221.0 | 231.0 | app2 | ok | 21 | 7625ms | 9725ms | 25800ms |
| 221.0 | 231.0 | end-users | ok | 135 | 3346ms | 4669ms | 4967ms |
| 231.0 | 241.0 | app1 | ok | 58 | 2042ms | 4194ms | 4919ms |
| 231.0 | 241.0 | app2 | ok | 30 | 7679ms | 9821ms | 27000ms |
| 231.0 | 241.0 | end-users | ok | 189 | 3542ms | 4708ms | 4971ms |
| 241.0 | 251.0 | app1 | ok | 51 | 2281ms | 4420ms | 4942ms |
| 241.0 | 251.0 | app2 | ok | 23 | 5208ms | 9042ms | 9904ms |
| 241.0 | 251.0 | end-users | ok | 159 | 3155ms | 4669ms | 6025ms |
| 251.0 | 261.0 | app1 | ok | 41 | 2078ms | 4359ms | 4936ms |
| 251.0 | 261.0 | app2 | ok | 23 | 7500ms | 9500ms | 9950ms |
| 251.0 | 261.0 | end-users | ok | 140 | 3196ms | 4639ms | 4964ms |
| 261.0 | 271.0 | app1 | ok | 41 | 2050ms | 4359ms | 4936ms |
| 261.0 | 271.0 | app2 | ok | 36 | 3864ms | 8615ms | 9862ms |
| 261.0 | 271.0 | end-users | ok | 154 | 2438ms | 4487ms | 4949ms |
| 271.0 | 281.0 | app1 | ok | 49 | 3024ms | 4605ms | 4960ms |
| 271.0 | 281.0 | app2 | ok | 8 | 7500ms | 9500ms | 9950ms |
| 271.0 | 281.0 | end-users | ok | 138 | 3500ms | 4700ms | 4970ms |
| 281.0 | 291.0 | app1 | ok | 52 | 1923ms | 4188ms | 4919ms |
| 281.0 | 291.0 | app2 | ok | 27 | 7596ms | 9673ms | 24600ms |
| 281.0 | 291.0 | end-users | ok | 168 | 3511ms | 4702ms | 4970ms |
| 291.0 | 301.0 | app1 | ok | 41 | 1679ms | 3861ms | 4886ms |
| 291.0 | 301.0 | app2 | ok | 20 | 7500ms | 9500ms | 9950ms |
| 291.0 | 301.0 | end-users | ok | 136 | 3300ms | 4660ms | 4966ms |
| 301.0 | 311.0 | app1 | ok | 51 | 1750ms | 3938ms | 4894ms |
| 301.0 | 311.0 | app2 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 301.0 | 311.0 | end-users | ok | 165 | 3401ms | 4680ms | 4968ms |
| 311.0 | 321.0 | app1 | ok | 43 | 1852ms | 4104ms | 4910ms |
| 311.0 | 321.0 | app2 | ok | 39 | 6300ms | 9420ms | 22200ms |
| 311.0 | 321.0 | end-users | ok | 167 | 3031ms | 4606ms | 4961ms |
| 321.0 | 331.0 | app1 | ok | 20 | 3214ms | 4643ms | 4964ms |
| 321.0 | 331.0 | app2 | ok | 9 | 2750ms | 4550ms | 4955ms |
| 321.0 | 331.0 | end-users | ok | 61 | 3045ms | 4609ms | 4961ms |
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
| 391.0 | 402.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 402.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 402.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 492.0 | 502.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 542.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 542.0 | 552.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 542.0 | 552.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 542.0 | 552.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 552.0 | 562.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 552.0 | 562.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 552.0 | 562.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 562.0 | 572.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 562.0 | 572.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 562.0 | 572.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 572.0 | 582.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 572.0 | 582.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 572.0 | 582.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 582.0 | 592.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 582.0 | 592.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 582.0 | 592.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 592.0 | 602.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 592.0 | 602.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 592.0 | 602.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 602.0 | 612.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 602.0 | 612.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 602.0 | 612.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 612.0 | 622.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 612.0 | 622.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 612.0 | 622.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 622.0 | 632.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 622.0 | 632.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 622.0 | 632.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1737990 | 86545 | 1824535.0 | 0.0% | 1881368.0 | 1911080.0 | -1.6% | True |
| app2 | 984000 | 48913 | 1032913.0 | 0.0% | 1062948.0 | 1081826.0 | -1.7% | True |
| end-users | 6285300 | 312145 | 6597445.0 | 0.0% | 6808302.0 | 6909590.0 | -1.5% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1413 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 800 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 5115 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=7328). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 7328 | 0.051ms | 0.109ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 593495 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1413 | 6642ms | 9449ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 800 | 12729ms | 18148ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 5110 | 7944ms | 12288ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 7323 | 7898ms | 13845ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (63 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2583ms | 4662ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 3000ms | 4825ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2719ms | 4876ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 6188ms | 9510ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 10208ms | 14521ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 7416ms | 11075ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 7000ms | 9511ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 12778ms | 17500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 8712ms | 13708ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 7240ms | 9642ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 16711ms | 19671ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 9148ms | 14305ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 6667ms | 9200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 12857ms | 18000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 8314ms | 12765ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 6611ms | 9573ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 8164ms | 13565ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 6762ms | 9564ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 12841ms | 17917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 8125ms | 12833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 6667ms | 9200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 8338ms | 11477ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 6714ms | 9530ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 12976ms | 18438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 8197ms | 12847ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 6636ms | 9467ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 12738ms | 17125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 8229ms | 12433ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 6708ms | 9456ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 13382ms | 19042ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 8098ms | 13119ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 6815ms | 9343ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 13158ms | 18800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 8262ms | 10156ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 6750ms | 9300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 12609ms | 14957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 8269ms | 10750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 6800ms | 8400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 12841ms | 17917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 8326ms | 9937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 151.0 | app1 | ok | 6667ms | 9343ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 151.0 | app2 | ok | 12738ms | 17125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 151.0 | end-users | ok | 8338ms | 12038ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 5933ms | 9533ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 8147ms | 12842ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 11800ms | 14680ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 6658ms | 9588ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 12130ms | 14713ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 6356ms | 7851ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 5091ms | 7300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 11250ms | 14625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 6784ms | 7994ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 6533ms | 8333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 8039ms | 9851ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 6844ms | 9060ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 12609ms | 14957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 8000ms | 9847ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 6643ms | 9040ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 12609ms | 14957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 8131ms | 9813ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 6625ms | 9617ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 13000ms | 18500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 8208ms | 13681ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 6737ms | 9600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 8154ms | 12833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 6478ms | 9411ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 13056ms | 18625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 8119ms | 11875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 6650ms | 9462ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 12935ms | 18312ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 8195ms | 10639ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | ok | 6353ms | 9567ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | ok | 12778ms | 17500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | ok | 7987ms | 11175ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | ok | 6692ms | 8667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | ok | 13594ms | 19179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | end-users | ok | 8195ms | 9983ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | ok | 7312ms | 12062ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | ok | 14333ms | 19409ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | end-users | ok | 8255ms | 13946ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | ok | 6333ms | 9467ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | ok | 12386ms | 14943ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | end-users | ok | 7966ms | 13227ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app1 | ok | 6788ms | 9000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app2 | ok | 12614ms | 14966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | end-users | ok | 8182ms | 9982ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app1 | ok | 6737ms | 9582ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app2 | ok | 13333ms | 19000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | end-users | ok | 8036ms | 13273ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app1 | ok | 7120ms | 9525ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app2 | ok | 12391ms | 14935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | end-users | ok | 8479ms | 11125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | end-users | ok | 11042ms | 14604ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 391.0 | 402.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 402.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 402.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 552.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 552.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 552.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 552.0 | 562.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 552.0 | 562.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 552.0 | 562.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 562.0 | 572.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 562.0 | 572.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 562.0 | 572.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 572.0 | 582.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 572.0 | 582.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 572.0 | 582.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 582.0 | 592.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 582.0 | 592.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 582.0 | 592.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 592.0 | 602.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 592.0 | 602.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 592.0 | 602.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 602.0 | 612.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 602.0 | 612.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 602.0 | 612.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 612.0 | 622.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 612.0 | 622.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 612.0 | 622.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 622.0 | 632.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 622.0 | 632.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 622.0 | 632.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
