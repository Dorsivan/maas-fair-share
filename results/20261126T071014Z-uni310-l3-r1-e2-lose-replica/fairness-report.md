# Fairness benchmark: full-contention (uni310-l3-r1-e2-lose-replica)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 6.1 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 6.1 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `360` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5d57688bf8-58kzn` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T07:11:32Z` |
| Run end | `2026-11-26T07:22:04Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 64 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/64 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 135.00 | 4.2188 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1215 | 200=1215 | 8.1 | 13.9 | 1604076.0 | 21.1% | 16.7% | -4.4 | 21.0% | -0.1 | 20.9% | -0.1 | 89.5s | 98.9% | 1215.0 |
| app2 | 10.0 | 32 | 624 | 200=624 | 15.5 | 27.5 | 808970.0 | 10.5% | 16.7% | 6.1 | 10.6% | 0.1 | 10.7% | 0.2 | 90.7s | 98.9% | 624.0 |
| end-users | 65.0 | 128 | 3969 | 000=1, 200=3968 | 9.9 | 17.0 | 5224856.0 | 68.4% | 66.7% | -1.8 | 68.4% | -0.0 | 68.3% | -0.1 | 90.7s | 98.9% | 3969.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events (scheduled):**
- t+120s: scale_down (target=maas-vllm-gpu, to=1)
- t+360s: scale_restore (target=maas-vllm-gpu)

**Per-tenant schedule:**
- app1: active 0s-360s, no duty cycle
- app2: active 0s-360s, no duty cycle
- end-users: active 0s-360s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 10.0 | 10.0 |
| 120.0 | 121.0 | 1.0 |
| 360.0 | n/a (never converged in this phase) | n/a |

**Windows** (63 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 12134.0 | 21.1% | 53.0% | 31.9 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | False | 10778.0 | 68.4% | 47.0% | -21.4 |
| 10.0 | 20.0 | app1 | True | False | 55392.0 | 21.1% | 21.5% | 0.4 |
| 10.0 | 20.0 | app2 | True | False | 17504.0 | 10.5% | 6.8% | -3.7 |
| 10.0 | 20.0 | end-users | True | False | 185200.0 | 68.4% | 71.8% | 3.3 |
| 20.0 | 30.0 | app1 | True | False | 66292.0 | 21.1% | 21.6% | 0.5 |
| 20.0 | 30.0 | app2 | True | False | 32410.0 | 10.5% | 10.6% | 0.0 |
| 20.0 | 30.0 | end-users | True | False | 208200.0 | 68.4% | 67.8% | -0.6 |
| 30.0 | 40.0 | app1 | True | False | 64946.0 | 21.1% | 21.0% | -0.1 |
| 30.0 | 40.0 | app2 | True | False | 31122.0 | 10.5% | 10.0% | -0.5 |
| 30.0 | 40.0 | end-users | True | False | 213692.0 | 68.4% | 69.0% | 0.6 |
| 40.0 | 50.0 | app1 | True | False | 63604.0 | 21.1% | 20.8% | -0.2 |
| 40.0 | 50.0 | app2 | True | False | 33836.0 | 10.5% | 11.1% | 0.5 |
| 40.0 | 50.0 | end-users | True | False | 208168.0 | 68.4% | 68.1% | -0.3 |
| 50.0 | 60.0 | app1 | True | False | 64950.0 | 21.1% | 21.2% | 0.2 |
| 50.0 | 60.0 | app2 | True | False | 31096.0 | 10.5% | 10.2% | -0.4 |
| 50.0 | 60.0 | end-users | True | False | 209780.0 | 68.4% | 68.6% | 0.2 |
| 60.0 | 70.0 | app1 | True | False | 64872.0 | 21.1% | 21.2% | 0.2 |
| 60.0 | 70.0 | app2 | True | False | 32456.0 | 10.5% | 10.6% | 0.1 |
| 60.0 | 70.0 | end-users | True | False | 208196.0 | 68.4% | 68.1% | -0.3 |
| 70.0 | 80.0 | app1 | True | False | 63580.0 | 21.1% | 20.9% | -0.2 |
| 70.0 | 80.0 | app2 | True | False | 31174.0 | 10.5% | 10.2% | -0.3 |
| 70.0 | 80.0 | end-users | True | False | 209694.0 | 68.4% | 68.9% | 0.5 |
| 80.0 | 91.0 | app1 | True | False | 67666.0 | 21.1% | 22.3% | 1.3 |
| 80.0 | 91.0 | app2 | True | False | 32462.0 | 10.5% | 10.7% | 0.2 |
| 80.0 | 91.0 | end-users | True | False | 202850.0 | 68.4% | 67.0% | -1.5 |
| 91.0 | 101.0 | app1 | True | False | 60898.0 | 21.1% | 20.2% | -0.9 |
| 91.0 | 101.0 | app2 | True | False | 29796.0 | 10.5% | 9.9% | -0.7 |
| 91.0 | 101.0 | end-users | True | False | 211010.0 | 68.4% | 69.9% | 1.5 |
| 101.0 | 111.0 | app1 | True | False | 63682.0 | 21.1% | 21.7% | 0.6 |
| 101.0 | 111.0 | app2 | True | False | 28370.0 | 10.5% | 9.7% | -0.9 |
| 101.0 | 111.0 | end-users | True | False | 201500.0 | 68.4% | 68.6% | 0.2 |
| 111.0 | 121.0 | app1 | True | False | 58104.0 | 21.1% | 19.5% | -1.5 |
| 111.0 | 121.0 | app2 | True | False | 36530.0 | 10.5% | 12.3% | 1.8 |
| 111.0 | 121.0 | end-users | True | False | 202880.0 | 68.4% | 68.2% | -0.2 |
| 121.0 | 131.0 | app1 | True | False | 63524.0 | 21.1% | 21.1% | 0.0 |
| 121.0 | 131.0 | app2 | True | False | 31038.0 | 10.5% | 10.3% | -0.2 |
| 121.0 | 131.0 | end-users | True | False | 206952.0 | 68.4% | 68.6% | 0.2 |
| 131.0 | 141.0 | app1 | True | False | 62236.0 | 21.1% | 20.4% | -0.7 |
| 131.0 | 141.0 | app2 | True | False | 33756.0 | 10.5% | 11.0% | 0.5 |
| 131.0 | 141.0 | end-users | True | False | 209620.0 | 68.4% | 68.6% | 0.2 |
| 141.0 | 151.0 | app1 | True | False | 52800.0 | 21.1% | 21.7% | 0.6 |
| 141.0 | 151.0 | app2 | True | False | 21696.0 | 10.5% | 8.9% | -1.6 |
| 141.0 | 151.0 | end-users | True | False | 169024.0 | 68.4% | 69.4% | 1.0 |
| 151.0 | 161.0 | app1 | True | False | 31036.0 | 21.1% | 20.5% | -0.6 |
| 151.0 | 161.0 | app2 | True | False | 16250.0 | 10.5% | 10.7% | 0.2 |
| 151.0 | 161.0 | end-users | True | False | 104224.0 | 68.4% | 68.8% | 0.4 |
| 161.0 | 171.0 | app1 | True | False | 32466.0 | 21.1% | 21.3% | 0.2 |
| 161.0 | 171.0 | app2 | True | False | 18946.0 | 10.5% | 12.4% | 1.9 |
| 161.0 | 171.0 | end-users | True | False | 101364.0 | 68.4% | 66.3% | -2.1 |
| 171.0 | 181.0 | app1 | True | False | 32352.0 | 21.1% | 21.0% | -0.0 |
| 171.0 | 181.0 | app2 | True | False | 16284.0 | 10.5% | 10.6% | 0.0 |
| 171.0 | 181.0 | end-users | True | False | 105384.0 | 68.4% | 68.4% | 0.0 |
| 181.0 | 191.0 | app1 | True | False | 31158.0 | 21.1% | 20.4% | -0.7 |
| 181.0 | 191.0 | app2 | True | False | 16206.0 | 10.5% | 10.6% | 0.1 |
| 181.0 | 191.0 | end-users | True | False | 105482.0 | 68.4% | 69.0% | 0.6 |
| 191.0 | 201.0 | app1 | True | False | 32440.0 | 21.1% | 21.2% | 0.2 |
| 191.0 | 201.0 | app2 | True | False | 14898.0 | 10.5% | 9.8% | -0.8 |
| 191.0 | 201.0 | end-users | True | False | 105380.0 | 68.4% | 69.0% | 0.6 |
| 201.0 | 211.0 | app1 | True | False | 31150.0 | 21.1% | 20.7% | -0.3 |
| 201.0 | 211.0 | app2 | True | False | 17608.0 | 10.5% | 11.7% | 1.2 |
| 201.0 | 211.0 | end-users | True | False | 101470.0 | 68.4% | 67.5% | -0.9 |
| 211.0 | 221.0 | app1 | True | False | 31146.0 | 21.1% | 20.9% | -0.1 |
| 211.0 | 221.0 | app2 | True | False | 14916.0 | 10.5% | 10.0% | -0.5 |
| 211.0 | 221.0 | end-users | True | False | 102694.0 | 68.4% | 69.0% | 0.6 |
| 221.0 | 231.0 | app1 | True | False | 32506.0 | 21.1% | 21.4% | 0.4 |
| 221.0 | 231.0 | app2 | True | False | 16216.0 | 10.5% | 10.7% | 0.2 |
| 221.0 | 231.0 | end-users | True | False | 102860.0 | 68.4% | 67.9% | -0.6 |
| 231.0 | 241.0 | app1 | True | False | 32466.0 | 21.1% | 21.2% | 0.2 |
| 231.0 | 241.0 | app2 | True | False | 14902.0 | 10.5% | 9.8% | -0.8 |
| 231.0 | 241.0 | end-users | True | False | 105452.0 | 68.4% | 69.0% | 0.6 |
| 241.0 | 251.0 | app1 | True | False | 32394.0 | 21.1% | 21.2% | 0.2 |
| 241.0 | 251.0 | app2 | True | False | 16238.0 | 10.5% | 10.6% | 0.1 |
| 241.0 | 251.0 | end-users | True | False | 104078.0 | 68.4% | 68.2% | -0.3 |
| 251.0 | 261.0 | app1 | True | False | 31130.0 | 21.1% | 20.5% | -0.5 |
| 251.0 | 261.0 | app2 | True | False | 16244.0 | 10.5% | 10.7% | 0.2 |
| 251.0 | 261.0 | end-users | True | False | 104208.0 | 68.4% | 68.7% | 0.3 |
| 261.0 | 271.0 | app1 | True | False | 33770.0 | 21.1% | 22.1% | 1.1 |
| 261.0 | 271.0 | app2 | True | False | 16266.0 | 10.5% | 10.6% | 0.1 |
| 261.0 | 271.0 | end-users | True | False | 102728.0 | 68.4% | 67.2% | -1.2 |
| 271.0 | 281.0 | app1 | True | False | 31180.0 | 21.1% | 20.6% | -0.5 |
| 271.0 | 281.0 | app2 | True | False | 16244.0 | 10.5% | 10.7% | 0.2 |
| 271.0 | 281.0 | end-users | True | False | 104066.0 | 68.4% | 68.7% | 0.3 |
| 281.0 | 291.0 | app1 | True | False | 31056.0 | 21.1% | 20.1% | -0.9 |
| 281.0 | 291.0 | app2 | True | False | 16260.0 | 10.5% | 10.5% | 0.0 |
| 281.0 | 291.0 | end-users | True | False | 106840.0 | 68.4% | 69.3% | 0.9 |
| 291.0 | 301.0 | app1 | True | False | 32512.0 | 21.1% | 21.5% | 0.4 |
| 291.0 | 301.0 | app2 | True | False | 16290.0 | 10.5% | 10.7% | 0.2 |
| 291.0 | 301.0 | end-users | True | False | 102752.0 | 68.4% | 67.8% | -0.6 |
| 301.0 | 311.0 | app1 | True | False | 32458.0 | 21.1% | 21.4% | 0.4 |
| 301.0 | 311.0 | app2 | True | False | 14842.0 | 10.5% | 9.8% | -0.7 |
| 301.0 | 311.0 | end-users | True | False | 104172.0 | 68.4% | 68.8% | 0.4 |
| 311.0 | 321.0 | app1 | True | False | 31098.0 | 21.1% | 20.5% | -0.5 |
| 311.0 | 321.0 | app2 | True | False | 16214.0 | 10.5% | 10.7% | 0.2 |
| 311.0 | 321.0 | end-users | True | False | 104144.0 | 68.4% | 68.8% | 0.3 |
| 321.0 | 331.0 | app1 | True | False | 32488.0 | 21.1% | 21.1% | 0.0 |
| 321.0 | 331.0 | app2 | True | False | 16224.0 | 10.5% | 10.5% | -0.0 |
| 321.0 | 331.0 | end-users | True | False | 105502.0 | 68.4% | 68.4% | -0.0 |
| 331.0 | 341.0 | app1 | True | False | 33756.0 | 21.1% | 21.9% | 0.9 |
| 331.0 | 341.0 | app2 | True | False | 16230.0 | 10.5% | 10.5% | 0.0 |
| 331.0 | 341.0 | end-users | True | False | 104076.0 | 68.4% | 67.6% | -0.9 |
| 341.0 | 352.0 | app1 | True | False | 31162.0 | 21.1% | 20.6% | -0.5 |
| 341.0 | 352.0 | app2 | True | False | 17526.0 | 10.5% | 11.6% | 1.1 |
| 341.0 | 352.0 | end-users | True | False | 102646.0 | 68.4% | 67.8% | -0.6 |
| 352.0 | 362.0 | app1 | True | False | 33762.0 | 21.1% | 21.7% | 0.7 |
| 352.0 | 362.0 | app2 | True | False | 14880.0 | 10.5% | 9.6% | -0.9 |
| 352.0 | 362.0 | end-users | True | False | 106616.0 | 68.4% | 68.7% | 0.2 |
| 362.0 | 372.0 | app1 | False | n/a | 31066.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app2 | False | n/a | 17582.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | end-users | False | n/a | 105422.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app1 | False | n/a | 14844.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app2 | False | n/a | 28458.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | end-users | False | n/a | 75752.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
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
| 602.0 | 613.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 602.0 | 613.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 602.0 | 613.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 613.0 | 623.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 613.0 | 623.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 613.0 | 623.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 623.0 | 632.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 623.0 | 632.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 623.0 | 632.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 48 | 0ms | 3667ms | 4867ms |
| 0.0 | 10.0 | app2 | ok | 26 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 154 | 0ms | 3987ms | 4899ms |
| 10.0 | 20.0 | app1 | ok | 54 | 2000ms | 4250ms | 4925ms |
| 10.0 | 20.0 | app2 | ok | 26 | 7600ms | 9680ms | 24800ms |
| 10.0 | 20.0 | end-users | ok | 177 | 3420ms | 4684ms | 4968ms |
| 20.0 | 30.0 | app1 | ok | 48 | 1931ms | 4077ms | 4908ms |
| 20.0 | 30.0 | app2 | ok | 23 | 7500ms | 9500ms | 9950ms |
| 20.0 | 30.0 | end-users | ok | 154 | 3605ms | 4721ms | 4972ms |
| 30.0 | 40.0 | app1 | ok | 48 | 1871ms | 3909ms | 4891ms |
| 30.0 | 40.0 | app2 | ok | 24 | 7500ms | 9500ms | 9950ms |
| 30.0 | 40.0 | end-users | ok | 158 | 3619ms | 4724ms | 4972ms |
| 40.0 | 50.0 | app1 | ok | 39 | 1893ms | 4114ms | 4911ms |
| 40.0 | 50.0 | app2 | ok | 20 | 7632ms | 9737ms | 26000ms |
| 40.0 | 50.0 | end-users | ok | 127 | 3530ms | 4706ms | 4971ms |
| 50.0 | 60.0 | app1 | ok | 51 | 1875ms | 4019ms | 4902ms |
| 50.0 | 60.0 | app2 | ok | 25 | 7604ms | 9688ms | 25000ms |
| 50.0 | 60.0 | end-users | ok | 164 | 3566ms | 4713ms | 4971ms |
| 60.0 | 70.0 | app1 | ok | 49 | 1905ms | 4058ms | 4906ms |
| 60.0 | 70.0 | app2 | ok | 25 | 7717ms | 9891ms | 27500ms |
| 60.0 | 70.0 | end-users | ok | 159 | 3600ms | 4720ms | 4972ms |
| 70.0 | 80.0 | app1 | ok | 50 | 1978ms | 4265ms | 4926ms |
| 70.0 | 80.0 | app2 | ok | 25 | 7604ms | 9688ms | 25000ms |
| 70.0 | 80.0 | end-users | ok | 168 | 3489ms | 4698ms | 4970ms |
| 80.0 | 91.0 | app1 | ok | 51 | 1893ms | 4250ms | 4925ms |
| 80.0 | 91.0 | app2 | ok | 42 | 6429ms | 9429ms | 21600ms |
| 80.0 | 91.0 | end-users | ok | 187 | 2931ms | 4586ms | 4959ms |
| 91.0 | 101.0 | app1 | ok | 37 | 2812ms | 4663ms | 8150ms |
| 91.0 | 101.0 | app2 | ok | 1 | 7500ms | 9500ms | 9950ms |
| 91.0 | 101.0 | end-users | ok | 93 | 3363ms | 4673ms | 4967ms |
| 101.0 | 111.0 | app1 | ok | 51 | 2458ms | 4573ms | 7450ms |
| 101.0 | 111.0 | app2 | ok | 26 | 6000ms | 9467ms | 24800ms |
| 101.0 | 111.0 | end-users | ok | 165 | 3245ms | 4759ms | 8625ms |
| 111.0 | 121.0 | app1 | ok | 40 | 2312ms | 4444ms | 4944ms |
| 111.0 | 121.0 | app2 | ok | 21 | 7500ms | 9500ms | 9950ms |
| 111.0 | 121.0 | end-users | ok | 133 | 3461ms | 4692ms | 4969ms |
| 121.0 | 131.0 | app1 | ok | 47 | 1821ms | 4161ms | 4916ms |
| 121.0 | 131.0 | app2 | ok | 26 | 8095ms | 19600ms | 28960ms |
| 121.0 | 131.0 | end-users | ok | 175 | 3120ms | 4641ms | 4984ms |
| 131.0 | 141.0 | app1 | ok | 55 | 1562ms | 3625ms | 4863ms |
| 131.0 | 141.0 | app2 | ok | 40 | 6296ms | 9259ms | 9926ms |
| 131.0 | 141.0 | end-users | ok | 180 | 2973ms | 4595ms | 4959ms |
| 141.0 | 151.0 | app1 | ok | 35 | 4345ms | 8542ms | 9854ms |
| 141.0 | 151.0 | app2 | ok | 2 | 20000ms | 28000ms | 29800ms |
| 141.0 | 151.0 | end-users | ok | 91 | 6445ms | 9289ms | 9929ms |
| 151.0 | 161.0 | app1 | ok | 13 | 7955ms | 17000ms | 28700ms |
| 151.0 | 161.0 | app2 | ok | 5 | 20000ms | 28000ms | 29800ms |
| 151.0 | 161.0 | end-users | ok | 39 | 9062ms | 24800ms | 29480ms |
| 161.0 | 171.0 | app1 | ok | 36 | 6304ms | 9435ms | 22800ms |
| 161.0 | 171.0 | app2 | ok | 20 | 20000ms | 28000ms | 29800ms |
| 161.0 | 171.0 | end-users | ok | 120 | 9510ms | 25636ms | 29564ms |
| 171.0 | 181.0 | app1 | ok | 16 | 6667ms | 9333ms | 9933ms |
| 171.0 | 181.0 | app2 | ok | 7 | 20000ms | 28000ms | 29800ms |
| 171.0 | 181.0 | end-users | ok | 53 | 9417ms | 25391ms | 29539ms |
| 181.0 | 191.0 | app1 | ok | 26 | 7391ms | 9652ms | 24800ms |
| 181.0 | 191.0 | app2 | ok | 14 | 20000ms | 28000ms | 29800ms |
| 181.0 | 191.0 | end-users | ok | 81 | 12766ms | 26553ms | 29655ms |
| 191.0 | 201.0 | app1 | ok | 25 | 7396ms | 9479ms | 9948ms |
| 191.0 | 201.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 191.0 | 201.0 | end-users | ok | 84 | 13846ms | 26769ms | 29677ms |
| 201.0 | 211.0 | app1 | ok | 15 | 7292ms | 9792ms | 27000ms |
| 201.0 | 211.0 | app2 | ok | 7 | 20000ms | 28000ms | 29800ms |
| 201.0 | 211.0 | end-users | ok | 49 | 10400ms | 26080ms | 29608ms |
| 211.0 | 221.0 | app1 | ok | 27 | 7500ms | 9848ms | 27300ms |
| 211.0 | 221.0 | app2 | ok | 14 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | end-users | ok | 86 | 12083ms | 26417ms | 29642ms |
| 221.0 | 231.0 | app1 | ok | 25 | 7283ms | 9457ms | 9946ms |
| 221.0 | 231.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | end-users | ok | 83 | 13400ms | 26680ms | 29668ms |
| 231.0 | 241.0 | app1 | ok | 22 | 7619ms | 9714ms | 25600ms |
| 231.0 | 241.0 | app2 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 231.0 | 241.0 | end-users | ok | 70 | 16000ms | 27200ms | 29720ms |
| 241.0 | 251.0 | app1 | ok | 23 | 7500ms | 9500ms | 9950ms |
| 241.0 | 251.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | end-users | ok | 75 | 14043ms | 26809ms | 29681ms |
| 251.0 | 261.0 | app1 | ok | 24 | 7500ms | 9682ms | 25200ms |
| 251.0 | 261.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | end-users | ok | 78 | 14400ms | 26880ms | 29688ms |
| 261.0 | 271.0 | app1 | ok | 26 | 7292ms | 9458ms | 9946ms |
| 261.0 | 271.0 | app2 | ok | 13 | 20000ms | 28000ms | 29800ms |
| 261.0 | 271.0 | end-users | ok | 83 | 13061ms | 26612ms | 29661ms |
| 271.0 | 281.0 | app1 | ok | 24 | 7391ms | 9478ms | 9948ms |
| 271.0 | 281.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 271.0 | 281.0 | end-users | ok | 81 | 13800ms | 26760ms | 29676ms |
| 281.0 | 291.0 | app1 | ok | 21 | 7500ms | 9500ms | 9950ms |
| 281.0 | 291.0 | app2 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 281.0 | 291.0 | end-users | ok | 69 | 15625ms | 27125ms | 29713ms |
| 291.0 | 301.0 | app1 | ok | 26 | 7400ms | 9480ms | 9948ms |
| 291.0 | 301.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 291.0 | 301.0 | end-users | ok | 84 | 12857ms | 26571ms | 29657ms |
| 301.0 | 311.0 | app1 | ok | 17 | 6458ms | 9292ms | 9929ms |
| 301.0 | 311.0 | app2 | ok | 9 | 20000ms | 28000ms | 29800ms |
| 301.0 | 311.0 | end-users | ok | 54 | 9500ms | 25500ms | 29550ms |
| 311.0 | 321.0 | app1 | ok | 36 | 7429ms | 9486ms | 9949ms |
| 311.0 | 321.0 | app2 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 311.0 | 321.0 | end-users | ok | 116 | 14324ms | 26865ms | 29686ms |
| 321.0 | 331.0 | app1 | ok | 15 | 6875ms | 9375ms | 9938ms |
| 321.0 | 331.0 | app2 | ok | 7 | 20000ms | 28000ms | 29800ms |
| 321.0 | 331.0 | end-users | ok | 49 | 11154ms | 26231ms | 29623ms |
| 331.0 | 341.0 | app1 | ok | 25 | 7283ms | 9457ms | 9946ms |
| 331.0 | 341.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 331.0 | 341.0 | end-users | ok | 81 | 12766ms | 26553ms | 29655ms |
| 341.0 | 352.0 | app1 | ok | 24 | 7391ms | 9478ms | 9948ms |
| 341.0 | 352.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 341.0 | 352.0 | end-users | ok | 77 | 12093ms | 26419ms | 29642ms |
| 352.0 | 362.0 | app1 | ok | 24 | 7391ms | 9478ms | 9948ms |
| 352.0 | 362.0 | app2 | ok | 13 | 20000ms | 28000ms | 29800ms |
| 352.0 | 362.0 | end-users | ok | 80 | 12609ms | 26522ms | 29652ms |
| 362.0 | 372.0 | app1 | ok | 22 | 7500ms | 9500ms | 9950ms |
| 362.0 | 372.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 362.0 | 372.0 | end-users | ok | 77 | 12500ms | 26500ms | 29650ms |
| 372.0 | 382.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app2 | ok | 15 | 20000ms | 28000ms | 29800ms |
| 372.0 | 382.0 | end-users | ok | 15 | 20000ms | 28000ms | 29800ms |
| 382.0 | 392.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 602.0 | 613.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 602.0 | 613.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 602.0 | 613.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 613.0 | 623.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 613.0 | 623.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 613.0 | 623.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 623.0 | 632.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 623.0 | 632.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 623.0 | 632.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1494450 | 74408 | 1568858.0 | 0.0% | 1604076.0 | 1643266.0 | -2.4% | True |
| app2 | 767520 | 38315 | 805835.0 | 0.0% | 808970.0 | 844150.0 | -4.2% | True |
| end-users | 4880640 | 242487 | 5123127.0 | 0.0% | 5224856.0 | 5365614.0 | -2.6% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1215 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 624 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3969 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5808). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5808 | 0.051ms | 0.113ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 599437 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1215 | 8344ms | 14425ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 624 | 16774ms | 28853ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3968 | 9925ms | 19408ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5807 | 10801ms | 19947ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (63 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 3250ms | 4875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 1750ms | 5400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2889ms | 5719ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 6760ms | 9180ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 10781ms | 14578ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 7543ms | 9726ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 6735ms | 8367ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 8167ms | 9817ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 6872ms | 7979ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 8225ms | 9822ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 6676ms | 7921ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 8289ms | 9829ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 6857ms | 8800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 12614ms | 14966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 8307ms | 9892ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 6786ms | 9314ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 12727ms | 17000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 8333ms | 9983ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 6758ms | 8433ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 12875ms | 18083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 8337ms | 9959ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 91.0 | app1 | ok | 6600ms | 8750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 91.0 | app2 | ok | 12857ms | 18000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 91.0 | end-users | ok | 8395ms | 9965ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 6769ms | 9343ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 13667ms | 19214ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 8406ms | 13556ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 6846ms | 9886ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 14773ms | 19475ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 8391ms | 13039ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 6958ms | 9522ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 12976ms | 18650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 8467ms | 13707ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 7154ms | 9739ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 13594ms | 19179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 8614ms | 14168ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 6727ms | 9489ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 13289ms | 18958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 7901ms | 13239ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 6714ms | 9636ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 13636ms | 19200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 8811ms | 13992ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 11618ms | 14662ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 18750ms | 28500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 12641ms | 16150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 17400ms | 19740ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 352.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 352.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 352.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app2 | ok | 23438ms | 29344ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 602.0 | 613.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 602.0 | 613.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 602.0 | 613.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 613.0 | 623.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 613.0 | 623.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 613.0 | 623.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 623.0 | 632.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 623.0 | 632.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 623.0 | 632.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
