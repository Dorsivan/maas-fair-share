# Fairness benchmark: full-contention (uni310-l3-r1-b4-long-idle)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 6.1 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'
Schedule-aware expected share (UNI-222): app1, app2, end-users scored against a time-weighted entitlement from the declared join/leave or duty-cycle schedule, not the flat whole-run weight ratio -- see docs/design.md "Whole-run scoring with a declared schedule".

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 6.1 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

**Caveat (UNI-163): the EPP restarted mid-run in a way this verdict did not catch.** The windowed series below shows a counter going backwards between two in-run scrapes, but the single before/after snapshot pair this verdict is built from happened to read monotonically end-to-end (a near-zero start and a lower-but-still-higher-than-zero end look the same as no restart at all). Every before/after delta above -- the verdict and the ledger cross-check below -- is computed from the post-restart pod's fresh counters alone and undercounts real traffic; read them as a measurement of the time since the restart, not the whole run.

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `890` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5d57688bf8-99hv8` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T07:30:48Z` |
| Run end | `2026-11-26T07:50:44Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 120 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/120 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 83.50 | 2.6094 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1410 | 200=1410 | 6.6 | 9.0 | 1858836.0 | 6.7% | 16.7% | -4.4 | 6.7% | -0.0 | 7.1% | -14.0 | 89.0s | 98.8% | 1410.0 |
| app2 | 10.0 | 32 | 2481 | 200=2480, 503=1 | 11.4 | 15.0 | 3318106.0 | 12.4% | 16.7% | 6.1 | 12.4% | -0.0 | 12.4% | 1.9 | 217.1s | 98.9% | 2481.0 |
| end-users | 65.0 | 128 | 16038 | 000=12, 200=16026 | 6.8 | 9.6 | 21483110.0 | 80.8% | 66.7% | -1.8 | 80.9% | 0.0 | 80.5% | 12.1 | 217.1s | 98.9% | 16038.0 |
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
| 150.0 | 151.0 | 1.0 |
| 750.0 | 753.0 | 3.0 |
| 890.0 | n/a (never converged in this phase) | n/a |

**Windows** (120 total, EPP restart detected mid-window at least once):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 5416.0 | 21.1% | 22.2% | 1.2 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | False | 18936.0 | 68.4% | 77.8% | 9.3 |
| 10.0 | 20.0 | app1 | True | False | 62234.0 | 21.1% | 21.9% | 0.8 |
| 10.0 | 20.0 | app2 | True | False | 14828.0 | 10.5% | 5.2% | -5.3 |
| 10.0 | 20.0 | end-users | True | False | 207142.0 | 68.4% | 72.9% | 4.5 |
| 20.0 | 30.0 | app1 | True | False | 63642.0 | 21.1% | 21.1% | 0.0 |
| 20.0 | 30.0 | app2 | True | False | 31168.0 | 10.5% | 10.3% | -0.2 |
| 20.0 | 30.0 | end-users | True | False | 206906.0 | 68.4% | 68.6% | 0.2 |
| 30.0 | 40.0 | app1 | True | False | 71644.0 | 21.1% | 23.1% | 2.1 |
| 30.0 | 40.0 | app2 | True | False | 28422.0 | 10.5% | 9.2% | -1.3 |
| 30.0 | 40.0 | end-users | True | False | 209500.0 | 68.4% | 67.7% | -0.7 |
| 40.0 | 50.0 | app1 | True | False | 55526.0 | 21.1% | 18.2% | -2.8 |
| 40.0 | 50.0 | app2 | True | False | 43294.0 | 10.5% | 14.2% | 3.7 |
| 40.0 | 50.0 | end-users | True | False | 205694.0 | 68.4% | 67.5% | -0.9 |
| 50.0 | 60.0 | app1 | True | False | 66306.0 | 21.1% | 22.0% | 0.9 |
| 50.0 | 60.0 | app2 | True | False | 25690.0 | 10.5% | 8.5% | -2.0 |
| 50.0 | 60.0 | end-users | True | False | 209608.0 | 68.4% | 69.5% | 1.1 |
| 60.0 | 70.0 | app1 | True | False | 63622.0 | 21.1% | 20.8% | -0.2 |
| 60.0 | 70.0 | app2 | True | False | 32448.0 | 10.5% | 10.6% | 0.1 |
| 60.0 | 70.0 | end-users | True | False | 209572.0 | 68.4% | 68.6% | 0.1 |
| 70.0 | 80.0 | app1 | True | False | 63406.0 | 21.1% | 20.7% | -0.4 |
| 70.0 | 80.0 | app2 | True | False | 32470.0 | 10.5% | 10.6% | 0.1 |
| 70.0 | 80.0 | end-users | True | False | 210986.0 | 68.4% | 68.8% | 0.3 |
| 80.0 | 90.0 | app1 | True | False | 64836.0 | 21.1% | 21.3% | 0.3 |
| 80.0 | 90.0 | app2 | True | False | 32428.0 | 10.5% | 10.7% | 0.1 |
| 80.0 | 90.0 | end-users | True | False | 206986.0 | 68.4% | 68.0% | -0.4 |
| 90.0 | 100.0 | app1 | True | False | 63616.0 | 21.1% | 21.3% | 0.2 |
| 90.0 | 100.0 | app2 | True | False | 27100.0 | 10.5% | 9.1% | -1.5 |
| 90.0 | 100.0 | end-users | True | False | 208328.0 | 68.4% | 69.7% | 1.2 |
| 100.0 | 110.0 | app1 | True | False | 60988.0 | 21.1% | 20.5% | -0.6 |
| 100.0 | 110.0 | app2 | True | False | 36534.0 | 10.5% | 12.3% | 1.7 |
| 100.0 | 110.0 | end-users | True | False | 200346.0 | 68.4% | 67.3% | -1.2 |
| 110.0 | 120.0 | app1 | True | False | 63530.0 | 21.1% | 20.7% | -0.4 |
| 110.0 | 120.0 | app2 | True | False | 32458.0 | 10.5% | 10.6% | 0.0 |
| 110.0 | 120.0 | end-users | True | False | 210924.0 | 68.4% | 68.7% | 0.3 |
| 120.0 | 131.0 | app1 | True | False | 66302.0 | 21.1% | 21.9% | 0.8 |
| 120.0 | 131.0 | app2 | True | False | 29782.0 | 10.5% | 9.8% | -0.7 |
| 120.0 | 131.0 | end-users | True | False | 206894.0 | 68.4% | 68.3% | -0.1 |
| 131.0 | 141.0 | app1 | True | False | 60914.0 | 21.1% | 20.6% | -0.5 |
| 131.0 | 141.0 | app2 | True | False | 32418.0 | 10.5% | 10.9% | 0.4 |
| 131.0 | 141.0 | end-users | True | False | 202900.0 | 68.4% | 68.5% | 0.1 |
| 141.0 | 151.0 | app1 | True | False | 62230.0 | 21.1% | 20.5% | -0.5 |
| 141.0 | 151.0 | app2 | True | False | 32454.0 | 10.5% | 10.7% | 0.2 |
| 141.0 | 151.0 | end-users | True | False | 208442.0 | 68.4% | 68.8% | 0.3 |
| 151.0 | 161.0 | app1 | False | n/a | 50110.0 | n/a | n/a | n/a |
| 151.0 | 161.0 | app2 | True | False | 36560.0 | 13.3% | 14.5% | 1.2 |
| 151.0 | 161.0 | end-users | True | False | 215022.0 | 86.7% | 85.5% | -1.2 |
| 161.0 | 171.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 161.0 | 171.0 | app2 | True | False | 33810.0 | 13.3% | 11.4% | -2.0 |
| 161.0 | 171.0 | end-users | True | False | 263930.0 | 86.7% | 88.6% | 2.0 |
| 171.0 | 181.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 171.0 | 181.0 | app2 | True | False | 35178.0 | 13.3% | 12.0% | -1.3 |
| 171.0 | 181.0 | end-users | True | False | 256960.0 | 86.7% | 88.0% | 1.3 |
| 181.0 | 191.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 181.0 | 191.0 | app2 | True | False | 42032.0 | 13.3% | 13.9% | 0.5 |
| 181.0 | 191.0 | end-users | True | False | 261042.0 | 86.7% | 86.1% | -0.5 |
| 191.0 | 201.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app2 | True | False | 43246.0 | 13.3% | 14.3% | 1.0 |
| 191.0 | 201.0 | end-users | True | False | 258268.0 | 86.7% | 85.7% | -1.0 |
| 201.0 | 211.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 201.0 | 211.0 | app2 | True | False | 31100.0 | 13.3% | 10.9% | -2.4 |
| 201.0 | 211.0 | end-users | True | False | 254366.0 | 86.7% | 89.1% | 2.4 |
| 211.0 | 221.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 211.0 | 221.0 | app2 | True | False | 48658.0 | 13.3% | 16.1% | 2.8 |
| 211.0 | 221.0 | end-users | True | False | 253032.0 | 86.7% | 83.9% | -2.8 |
| 221.0 | 231.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app2 | True | False | 39258.0 | 13.3% | 12.9% | -0.4 |
| 221.0 | 231.0 | end-users | True | False | 264982.0 | 86.7% | 87.1% | 0.4 |
| 231.0 | 241.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app2 | True | False | 42002.0 | 13.3% | 14.2% | 0.8 |
| 231.0 | 241.0 | end-users | True | False | 254516.0 | 86.7% | 85.8% | -0.8 |
| 241.0 | 251.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | True | False | 40596.0 | 13.3% | 13.5% | 0.1 |
| 241.0 | 251.0 | end-users | True | False | 261216.0 | 86.7% | 86.5% | -0.1 |
| 251.0 | 261.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | True | False | 44682.0 | 13.3% | 15.0% | 1.7 |
| 251.0 | 261.0 | end-users | True | False | 252970.0 | 86.7% | 85.0% | -1.7 |
| 261.0 | 271.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | True | False | 35178.0 | 13.3% | 11.7% | -1.6 |
| 261.0 | 271.0 | end-users | True | False | 265222.0 | 86.7% | 88.3% | 1.6 |
| 271.0 | 281.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | True | False | 41908.0 | 13.3% | 13.8% | 0.4 |
| 271.0 | 281.0 | end-users | True | False | 262362.0 | 86.7% | 86.2% | -0.4 |
| 281.0 | 291.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | True | False | 39260.0 | 13.3% | 13.2% | -0.1 |
| 281.0 | 291.0 | end-users | True | False | 258534.0 | 86.7% | 86.8% | 0.1 |
| 291.0 | 301.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | True | False | 37882.0 | 13.3% | 12.5% | -0.8 |
| 291.0 | 301.0 | end-users | True | False | 265004.0 | 86.7% | 87.5% | 0.8 |
| 301.0 | 311.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | True | False | 43350.0 | 13.3% | 14.4% | 1.1 |
| 301.0 | 311.0 | end-users | True | False | 256992.0 | 86.7% | 85.6% | -1.1 |
| 311.0 | 321.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | True | False | 40616.0 | 13.3% | 13.4% | 0.1 |
| 311.0 | 321.0 | end-users | True | False | 262420.0 | 86.7% | 86.6% | -0.1 |
| 321.0 | 331.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | True | False | 36546.0 | 13.3% | 12.1% | -1.2 |
| 321.0 | 331.0 | end-users | True | False | 264900.0 | 86.7% | 87.9% | 1.2 |
| 331.0 | 341.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | True | False | 41960.0 | 13.3% | 13.9% | 0.6 |
| 331.0 | 341.0 | end-users | True | False | 259766.0 | 86.7% | 86.1% | -0.6 |
| 341.0 | 351.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | True | False | 40578.0 | 13.3% | 13.6% | 0.3 |
| 341.0 | 351.0 | end-users | True | False | 256932.0 | 86.7% | 86.4% | -0.3 |
| 351.0 | 361.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | True | False | 31168.0 | 13.3% | 10.5% | -2.8 |
| 351.0 | 361.0 | end-users | True | False | 265280.0 | 86.7% | 89.5% | 2.8 |
| 361.0 | 371.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | True | False | 45848.0 | 13.3% | 15.5% | 2.1 |
| 361.0 | 371.0 | end-users | True | False | 250342.0 | 86.7% | 84.5% | -2.1 |
| 371.0 | 382.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 382.0 | app2 | True | False | 43336.0 | 13.3% | 14.3% | 1.0 |
| 371.0 | 382.0 | end-users | True | False | 259544.0 | 86.7% | 85.7% | -1.0 |
| 382.0 | 392.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app2 | True | False | 35174.0 | 13.3% | 11.7% | -1.7 |
| 382.0 | 392.0 | end-users | True | False | 266482.0 | 86.7% | 88.3% | 1.7 |
| 392.0 | 402.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app2 | True | False | 48698.0 | 13.3% | 16.2% | 2.9 |
| 392.0 | 402.0 | end-users | True | False | 251560.0 | 86.7% | 83.8% | -2.9 |
| 402.0 | 412.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app2 | True | False | 37848.0 | 13.3% | 12.5% | -0.8 |
| 402.0 | 412.0 | end-users | True | False | 263790.0 | 86.7% | 87.5% | 0.8 |
| 412.0 | 422.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | True | False | 36526.0 | 13.3% | 12.0% | -1.4 |
| 412.0 | 422.0 | end-users | True | False | 269082.0 | 86.7% | 88.0% | 1.4 |
| 422.0 | 432.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app2 | True | False | 41900.0 | 13.3% | 14.1% | 0.7 |
| 422.0 | 432.0 | end-users | True | False | 255826.0 | 86.7% | 85.9% | -0.7 |
| 432.0 | 442.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | True | False | 40518.0 | 13.3% | 13.6% | 0.3 |
| 432.0 | 442.0 | end-users | True | False | 257174.0 | 86.7% | 86.4% | -0.3 |
| 442.0 | 452.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | True | False | 36522.0 | 13.3% | 12.0% | -1.3 |
| 442.0 | 452.0 | end-users | True | False | 266584.0 | 86.7% | 88.0% | 1.3 |
| 452.0 | 462.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | True | False | 48630.0 | 13.3% | 16.6% | 3.3 |
| 452.0 | 462.0 | end-users | True | False | 243504.0 | 86.7% | 83.4% | -3.3 |
| 462.0 | 472.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | True | False | 33790.0 | 13.3% | 11.4% | -2.0 |
| 462.0 | 472.0 | end-users | True | False | 263738.0 | 86.7% | 88.6% | 2.0 |
| 472.0 | 482.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | True | False | 46074.0 | 13.3% | 15.2% | 1.9 |
| 472.0 | 482.0 | end-users | True | False | 256784.0 | 86.7% | 84.8% | -1.9 |
| 482.0 | 492.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | True | False | 35184.0 | 13.3% | 12.0% | -1.3 |
| 482.0 | 492.0 | end-users | True | False | 258398.0 | 86.7% | 88.0% | 1.3 |
| 492.0 | 502.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | True | False | 37880.0 | 13.3% | 12.6% | -0.7 |
| 492.0 | 502.0 | end-users | True | False | 262460.0 | 86.7% | 87.4% | 0.7 |
| 502.0 | 512.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app2 | True | False | 44598.0 | 13.3% | 14.8% | 1.5 |
| 502.0 | 512.0 | end-users | True | False | 257028.0 | 86.7% | 85.2% | -1.5 |
| 512.0 | 522.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app2 | True | False | 40492.0 | 13.3% | 13.2% | -0.1 |
| 512.0 | 522.0 | end-users | True | False | 266506.0 | 86.7% | 86.8% | 0.1 |
| 522.0 | 532.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app2 | True | False | 40588.0 | 13.3% | 13.6% | 0.2 |
| 522.0 | 532.0 | end-users | True | False | 258336.0 | 86.7% | 86.4% | -0.2 |
| 532.0 | 542.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app2 | True | False | 43182.0 | 13.3% | 14.7% | 1.4 |
| 532.0 | 542.0 | end-users | True | False | 250388.0 | 86.7% | 85.3% | -1.4 |
| 542.0 | 552.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 542.0 | 552.0 | app2 | True | False | 36560.0 | 13.3% | 12.0% | -1.4 |
| 542.0 | 552.0 | end-users | True | False | 268912.0 | 86.7% | 88.0% | 1.4 |
| 552.0 | 562.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 552.0 | 562.0 | app2 | True | False | 40600.0 | 13.3% | 13.3% | 0.0 |
| 552.0 | 562.0 | end-users | True | False | 263738.0 | 86.7% | 86.7% | -0.0 |
| 562.0 | 572.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 562.0 | 572.0 | app2 | True | False | 36538.0 | 13.3% | 12.3% | -1.1 |
| 562.0 | 572.0 | end-users | True | False | 261360.0 | 86.7% | 87.7% | 1.1 |
| 572.0 | 582.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 572.0 | 582.0 | app2 | True | False | 43264.0 | 13.3% | 14.4% | 1.1 |
| 572.0 | 582.0 | end-users | True | False | 257032.0 | 86.7% | 85.6% | -1.1 |
| 582.0 | 592.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 582.0 | 592.0 | app2 | True | False | 41970.0 | 13.3% | 13.8% | 0.5 |
| 582.0 | 592.0 | end-users | True | False | 261270.0 | 86.7% | 86.2% | -0.5 |
| 592.0 | 602.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 592.0 | 602.0 | app2 | True | False | 39210.0 | 13.3% | 13.3% | -0.0 |
| 592.0 | 602.0 | end-users | True | False | 255520.0 | 86.7% | 86.7% | 0.0 |
| 602.0 | 612.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 602.0 | 612.0 | app2 | True | False | 41928.0 | 13.3% | 13.8% | 0.5 |
| 602.0 | 612.0 | end-users | True | False | 261188.0 | 86.7% | 86.2% | -0.5 |
| 612.0 | 622.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 612.0 | 622.0 | app2 | True | False | 37904.0 | 13.3% | 12.6% | -0.7 |
| 612.0 | 622.0 | end-users | True | False | 262222.0 | 86.7% | 87.4% | 0.7 |
| 622.0 | 633.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 622.0 | 633.0 | app2 | True | False | 40632.0 | 13.3% | 13.3% | 0.0 |
| 622.0 | 633.0 | end-users | True | False | 263850.0 | 86.7% | 86.7% | -0.0 |
| 633.0 | 643.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 633.0 | 643.0 | app2 | True | False | 40488.0 | 13.3% | 13.4% | 0.0 |
| 633.0 | 643.0 | end-users | True | False | 262526.0 | 86.7% | 86.6% | -0.0 |
| 643.0 | 653.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 643.0 | 653.0 | app2 | True | False | 40540.0 | 13.3% | 13.4% | 0.1 |
| 643.0 | 653.0 | end-users | True | False | 261046.0 | 86.7% | 86.6% | -0.1 |
| 653.0 | 663.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 653.0 | 663.0 | app2 | True | False | 39258.0 | 13.3% | 12.8% | -0.5 |
| 653.0 | 663.0 | end-users | True | False | 266380.0 | 86.7% | 87.2% | 0.5 |
| 663.0 | 673.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 663.0 | 673.0 | app2 | True | False | 36508.0 | 13.3% | 12.5% | -0.8 |
| 663.0 | 673.0 | end-users | True | False | 255724.0 | 86.7% | 87.5% | 0.8 |
| 673.0 | 683.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 673.0 | 683.0 | app2 | True | False | 44626.0 | 13.3% | 14.6% | 1.3 |
| 673.0 | 683.0 | end-users | True | False | 261034.0 | 86.7% | 85.4% | -1.3 |
| 683.0 | 693.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 683.0 | 693.0 | app2 | True | False | 41904.0 | 13.3% | 13.8% | 0.5 |
| 683.0 | 693.0 | end-users | True | False | 261024.0 | 86.7% | 86.2% | -0.5 |
| 693.0 | 703.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 693.0 | 703.0 | app2 | True | False | 37830.0 | 13.3% | 12.6% | -0.7 |
| 693.0 | 703.0 | end-users | True | False | 262508.0 | 86.7% | 87.4% | 0.7 |
| 703.0 | 713.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 703.0 | 713.0 | app2 | True | False | 37970.0 | 13.3% | 13.0% | -0.3 |
| 703.0 | 713.0 | end-users | True | False | 252988.0 | 86.7% | 87.0% | 0.3 |
| 713.0 | 723.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 713.0 | 723.0 | app2 | True | False | 43246.0 | 13.3% | 14.5% | 1.2 |
| 713.0 | 723.0 | end-users | True | False | 254308.0 | 86.7% | 85.5% | -1.2 |
| 723.0 | 733.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 723.0 | 733.0 | app2 | True | False | 36526.0 | 13.3% | 12.0% | -1.3 |
| 723.0 | 733.0 | end-users | True | False | 266636.0 | 86.7% | 88.0% | 1.3 |
| 733.0 | 743.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 733.0 | 743.0 | app2 | True | False | 37804.0 | 13.3% | 12.5% | -0.9 |
| 733.0 | 743.0 | end-users | True | False | 265292.0 | 86.7% | 87.5% | 0.9 |
| 743.0 | 753.0 | app1 | False | n/a | 2706.0 | n/a | n/a | n/a |
| 743.0 | 753.0 | app2 | True | False | 48790.0 | 13.3% | 16.0% | 2.6 |
| 743.0 | 753.0 | end-users | True | False | 256694.0 | 86.7% | 84.0% | -2.6 |
| 753.0 | 763.0 | app1 | True | False | 70368.0 | 21.1% | 23.3% | 2.3 |
| 753.0 | 763.0 | app2 | True | False | 29782.0 | 10.5% | 9.9% | -0.7 |
| 753.0 | 763.0 | end-users | True | False | 201642.0 | 68.4% | 66.8% | -1.6 |
| 763.0 | 773.0 | app1 | True | False | 54106.0 | 21.1% | 19.2% | -1.8 |
| 763.0 | 773.0 | app2 | True | False | 35158.0 | 10.5% | 12.5% | 2.0 |
| 763.0 | 773.0 | end-users | True | False | 192104.0 | 68.4% | 68.3% | -0.1 |
| 773.0 | 783.0 | app1 | True | False | 63562.0 | 21.1% | 21.1% | 0.0 |
| 773.0 | 783.0 | app2 | True | False | 27012.0 | 10.5% | 9.0% | -1.6 |
| 773.0 | 783.0 | end-users | True | False | 210998.0 | 68.4% | 70.0% | 1.5 |
| 783.0 | 793.0 | app1 | True | False | 63576.0 | 21.1% | 20.7% | -0.3 |
| 783.0 | 793.0 | app2 | True | False | 32428.0 | 10.5% | 10.6% | 0.0 |
| 783.0 | 793.0 | end-users | True | False | 210876.0 | 68.4% | 68.7% | 0.3 |
| 793.0 | 803.0 | app1 | True | False | 64916.0 | 21.1% | 21.6% | 0.6 |
| 793.0 | 803.0 | app2 | True | False | 32500.0 | 10.5% | 10.8% | 0.3 |
| 793.0 | 803.0 | end-users | True | False | 202756.0 | 68.4% | 67.5% | -0.9 |
| 803.0 | 813.0 | app1 | True | False | 63636.0 | 21.1% | 20.7% | -0.3 |
| 803.0 | 813.0 | app2 | True | False | 28364.0 | 10.5% | 9.2% | -1.3 |
| 803.0 | 813.0 | end-users | True | False | 214922.0 | 68.4% | 70.0% | 1.6 |
| 813.0 | 823.0 | app1 | True | False | 60916.0 | 21.1% | 20.3% | -0.8 |
| 813.0 | 823.0 | app2 | True | False | 33802.0 | 10.5% | 11.3% | 0.7 |
| 813.0 | 823.0 | end-users | True | False | 205668.0 | 68.4% | 68.5% | 0.0 |
| 823.0 | 833.0 | app1 | True | False | 67534.0 | 21.1% | 23.0% | 2.0 |
| 823.0 | 833.0 | app2 | True | False | 31186.0 | 10.5% | 10.6% | 0.1 |
| 823.0 | 833.0 | end-users | True | False | 194662.0 | 68.4% | 66.4% | -2.1 |
| 833.0 | 843.0 | app1 | True | False | 56874.0 | 21.1% | 18.7% | -2.4 |
| 833.0 | 843.0 | app2 | True | False | 32430.0 | 10.5% | 10.7% | 0.1 |
| 833.0 | 843.0 | end-users | True | False | 215086.0 | 68.4% | 70.7% | 2.2 |
| 843.0 | 853.0 | app1 | True | False | 62298.0 | 21.1% | 20.9% | -0.1 |
| 843.0 | 853.0 | app2 | True | False | 32526.0 | 10.5% | 10.9% | 0.4 |
| 843.0 | 853.0 | end-users | True | False | 202898.0 | 68.4% | 68.2% | -0.3 |
| 853.0 | 863.0 | app1 | True | False | 64930.0 | 21.1% | 21.1% | 0.0 |
| 853.0 | 863.0 | app2 | True | False | 32454.0 | 10.5% | 10.5% | 0.0 |
| 853.0 | 863.0 | end-users | True | False | 210790.0 | 68.4% | 68.4% | -0.0 |
| 863.0 | 873.0 | app1 | True | False | 66134.0 | 21.1% | 21.8% | 0.7 |
| 863.0 | 873.0 | app2 | True | False | 27030.0 | 10.5% | 8.9% | -1.6 |
| 863.0 | 873.0 | end-users | True | False | 210884.0 | 68.4% | 69.4% | 0.9 |
| 873.0 | 884.0 | app1 | True | False | 58242.0 | 21.1% | 19.4% | -1.7 |
| 873.0 | 884.0 | app2 | True | False | 36514.0 | 10.5% | 12.2% | 1.6 |
| 873.0 | 884.0 | end-users | True | False | 205482.0 | 68.4% | 68.4% | 0.0 |
| 884.0 | 894.0 | app1 | True | False | 64952.0 | 21.1% | 21.5% | 0.5 |
| 884.0 | 894.0 | app2 | True | False | 31116.0 | 10.5% | 10.3% | -0.2 |
| 884.0 | 894.0 | end-users | True | False | 205598.0 | 68.4% | 68.2% | -0.3 |
| 894.0 | 904.0 | app1 | False | n/a | 29764.0 | n/a | n/a | n/a |
| 894.0 | 904.0 | app2 | False | n/a | 37858.0 | n/a | n/a | n/a |
| 894.0 | 904.0 | end-users | False | n/a | 123086.0 | n/a | n/a | n/a |
| 904.0 | 914.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 904.0 | 914.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 904.0 | 914.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 914.0 | 924.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 914.0 | 924.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 914.0 | 924.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 924.0 | 934.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 924.0 | 934.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 924.0 | 934.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 934.0 | 944.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 934.0 | 944.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 934.0 | 944.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 944.0 | 954.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 944.0 | 954.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 944.0 | 954.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 954.0 | 964.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 954.0 | 964.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 954.0 | 964.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 964.0 | 975.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 964.0 | 975.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 964.0 | 975.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 975.0 | 985.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 975.0 | 985.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 975.0 | 985.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 985.0 | 995.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 985.0 | 995.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 985.0 | 995.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 995.0 | 1005.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 995.0 | 1005.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 995.0 | 1005.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1005.0 | 1015.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1005.0 | 1015.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1005.0 | 1015.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1015.0 | 1025.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1015.0 | 1025.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1015.0 | 1025.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1025.0 | 1035.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1025.0 | 1035.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1025.0 | 1035.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1035.0 | 1045.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1035.0 | 1045.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1035.0 | 1045.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1045.0 | 1055.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1045.0 | 1055.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1045.0 | 1055.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1055.0 | 1065.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1055.0 | 1065.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1055.0 | 1065.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1065.0 | 1075.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1065.0 | 1075.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1065.0 | 1075.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1075.0 | 1085.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1075.0 | 1085.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1075.0 | 1085.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1085.0 | 1095.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1085.0 | 1095.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1085.0 | 1095.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1095.0 | 1105.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1095.0 | 1105.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1095.0 | 1105.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1105.0 | 1115.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1105.0 | 1115.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1105.0 | 1115.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1115.0 | 1125.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1115.0 | 1125.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1115.0 | 1125.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1125.0 | 1135.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1125.0 | 1135.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1125.0 | 1135.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1135.0 | 1145.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1135.0 | 1145.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1135.0 | 1145.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1145.0 | 1155.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1145.0 | 1155.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1145.0 | 1155.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1155.0 | 1165.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1155.0 | 1165.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1155.0 | 1165.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1165.0 | 1175.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1165.0 | 1175.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1165.0 | 1175.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1175.0 | 1186.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1175.0 | 1186.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1175.0 | 1186.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1186.0 | 1196.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1186.0 | 1196.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 1186.0 | 1196.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 1196.0 | 1196.0 | app1 | False | n/a | 1858836.0 | n/a | n/a | n/a |
| 1196.0 | 1196.0 | app2 | False | n/a | 3318106.0 | n/a | n/a | n/a |
| 1196.0 | 1196.0 | end-users | False | n/a | 21483110.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`, EPP restart detected mid-window at least once):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 57 | 750ms | 2384ms | 4644ms |
| 0.0 | 10.0 | app2 | ok | 29 | 0ms | 0ms | 9275ms |
| 0.0 | 10.0 | end-users | ok | 182 | 1238ms | 3803ms | 4880ms |
| 10.0 | 20.0 | app1 | ok | 40 | 1600ms | 3750ms | 4875ms |
| 10.0 | 20.0 | app2 | ok | 20 | 7632ms | 9737ms | 26000ms |
| 10.0 | 20.0 | end-users | ok | 132 | 3472ms | 4694ms | 4969ms |
| 20.0 | 30.0 | app1 | ok | 49 | 1925ms | 4058ms | 4906ms |
| 20.0 | 30.0 | app2 | ok | 24 | 7857ms | 14000ms | 28400ms |
| 20.0 | 30.0 | end-users | ok | 160 | 3639ms | 4728ms | 4973ms |
| 30.0 | 40.0 | app1 | ok | 41 | 2050ms | 4359ms | 4936ms |
| 30.0 | 40.0 | app2 | ok | 37 | 3750ms | 8458ms | 9846ms |
| 30.0 | 40.0 | end-users | ok | 157 | 2397ms | 4503ms | 4981ms |
| 40.0 | 50.0 | app1 | ok | 48 | 3182ms | 4636ms | 4964ms |
| 40.0 | 50.0 | app2 | ok | 9 | 7500ms | 9500ms | 9950ms |
| 40.0 | 50.0 | end-users | ok | 132 | 3545ms | 4745ms | 6700ms |
| 50.0 | 60.0 | app1 | ok | 54 | 1750ms | 3962ms | 4896ms |
| 50.0 | 60.0 | app2 | ok | 26 | 8095ms | 19600ms | 28960ms |
| 50.0 | 60.0 | end-users | ok | 175 | 3355ms | 4671ms | 4967ms |
| 60.0 | 70.0 | app1 | ok | 49 | 1991ms | 4183ms | 4918ms |
| 60.0 | 70.0 | app2 | ok | 24 | 7857ms | 14000ms | 28400ms |
| 60.0 | 70.0 | end-users | ok | 159 | 3580ms | 4716ms | 4972ms |
| 70.0 | 80.0 | app1 | ok | 46 | 2050ms | 4179ms | 4918ms |
| 70.0 | 80.0 | app2 | ok | 23 | 7738ms | 9929ms | 27700ms |
| 70.0 | 80.0 | end-users | ok | 149 | 3688ms | 4738ms | 4974ms |
| 80.0 | 90.0 | app1 | ok | 43 | 1679ms | 3925ms | 4892ms |
| 80.0 | 90.0 | app2 | ok | 21 | 7500ms | 9500ms | 9950ms |
| 80.0 | 90.0 | end-users | ok | 139 | 3420ms | 4684ms | 4968ms |
| 90.0 | 100.0 | app1 | ok | 49 | 2076ms | 4319ms | 4932ms |
| 90.0 | 100.0 | app2 | ok | 24 | 5417ms | 9417ms | 25200ms |
| 90.0 | 100.0 | end-users | ok | 157 | 3255ms | 4669ms | 4987ms |
| 100.0 | 110.0 | app1 | ok | 49 | 2240ms | 4388ms | 4939ms |
| 100.0 | 110.0 | app2 | ok | 26 | 7708ms | 9875ms | 27400ms |
| 100.0 | 110.0 | end-users | ok | 163 | 3534ms | 4707ms | 4971ms |
| 110.0 | 120.0 | app1 | ok | 51 | 1905ms | 4089ms | 4909ms |
| 110.0 | 120.0 | app2 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 110.0 | 120.0 | end-users | ok | 168 | 3521ms | 4704ms | 4970ms |
| 120.0 | 131.0 | app1 | ok | 46 | 1717ms | 3955ms | 4895ms |
| 120.0 | 131.0 | app2 | ok | 24 | 7500ms | 9500ms | 9950ms |
| 120.0 | 131.0 | end-users | ok | 155 | 3172ms | 4634ms | 4963ms |
| 131.0 | 141.0 | app1 | ok | 40 | 2333ms | 4444ms | 4944ms |
| 131.0 | 141.0 | app2 | ok | 19 | 7639ms | 9750ms | 26200ms |
| 131.0 | 141.0 | end-users | ok | 121 | 3625ms | 4725ms | 4972ms |
| 141.0 | 151.0 | app1 | ok | 58 | 1750ms | 4033ms | 4903ms |
| 141.0 | 151.0 | app2 | ok | 47 | 6544ms | 9309ms | 9931ms |
| 141.0 | 151.0 | end-users | ok | 218 | 3108ms | 4622ms | 4962ms |
| 151.0 | 161.0 | app1 | ok | 7 | 3750ms | 4750ms | 4975ms |
| 151.0 | 161.0 | app2 | ok | 18 | 2250ms | 4438ms | 4944ms |
| 151.0 | 161.0 | end-users | ok | 147 | 2155ms | 4407ms | 4941ms |
| 161.0 | 171.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 17 | 3942ms | 7167ms | 9717ms |
| 161.0 | 171.0 | end-users | ok | 162 | 1742ms | 3734ms | 4873ms |
| 171.0 | 181.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 26 | 4000ms | 8556ms | 9856ms |
| 171.0 | 181.0 | end-users | ok | 180 | 1725ms | 3953ms | 4895ms |
| 181.0 | 191.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 40 | 3947ms | 8333ms | 9833ms |
| 181.0 | 191.0 | end-users | ok | 238 | 1686ms | 3918ms | 4892ms |
| 191.0 | 201.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 23 | 3393ms | 8357ms | 9836ms |
| 191.0 | 201.0 | end-users | ok | 172 | 1911ms | 4189ms | 4919ms |
| 201.0 | 211.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 34 | 2679ms | 5750ms | 9575ms |
| 201.0 | 211.0 | end-users | ok | 197 | 1902ms | 4242ms | 4924ms |
| 211.0 | 221.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 29 | 3162ms | 4868ms | 9275ms |
| 211.0 | 221.0 | end-users | ok | 176 | 1669ms | 3952ms | 4895ms |
| 221.0 | 231.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 29 | 3688ms | 6375ms | 9638ms |
| 221.0 | 231.0 | end-users | ok | 182 | 1657ms | 3890ms | 4889ms |
| 231.0 | 241.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 30 | 5000ms | 9000ms | 9900ms |
| 231.0 | 241.0 | end-users | ok | 186 | 1479ms | 3397ms | 4840ms |
| 241.0 | 251.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 35 | 3917ms | 8409ms | 9841ms |
| 241.0 | 251.0 | end-users | ok | 217 | 1670ms | 3821ms | 4882ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 32 | 1857ms | 4727ms | 9200ms |
| 251.0 | 261.0 | end-users | ok | 190 | 1874ms | 4167ms | 4917ms |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | ok | 22 | 7105ms | 9421ms | 9942ms |
| 261.0 | 271.0 | end-users | ok | 216 | 1517ms | 3313ms | 4831ms |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | ok | 28 | 7083ms | 9417ms | 9942ms |
| 271.0 | 281.0 | end-users | ok | 184 | 1610ms | 2909ms | 4791ms |
| 281.0 | 291.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | ok | 42 | 6250ms | 9250ms | 9925ms |
| 281.0 | 291.0 | end-users | ok | 212 | 1508ms | 3107ms | 4811ms |
| 291.0 | 301.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | ok | 17 | 4583ms | 8786ms | 9879ms |
| 291.0 | 301.0 | end-users | ok | 169 | 1609ms | 3757ms | 4876ms |
| 301.0 | 311.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | ok | 31 | 6477ms | 9295ms | 9930ms |
| 301.0 | 311.0 | end-users | ok | 196 | 1583ms | 2958ms | 4796ms |
| 311.0 | 321.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | ok | 30 | 5833ms | 9167ms | 9917ms |
| 311.0 | 321.0 | end-users | ok | 209 | 1604ms | 3463ms | 4846ms |
| 321.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | ok | 34 | 3269ms | 7875ms | 9787ms |
| 321.0 | 331.0 | end-users | ok | 169 | 1623ms | 3826ms | 4883ms |
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | ok | 34 | 4265ms | 8583ms | 9858ms |
| 331.0 | 341.0 | end-users | ok | 225 | 1530ms | 3295ms | 4830ms |
| 341.0 | 351.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | ok | 18 | 6250ms | 9250ms | 9925ms |
| 341.0 | 351.0 | end-users | ok | 172 | 1622ms | 3613ms | 4861ms |
| 351.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | ok | 39 | 2339ms | 4850ms | 9350ms |
| 351.0 | 361.0 | end-users | ok | 198 | 1688ms | 4066ms | 4907ms |
| 361.0 | 371.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | ok | 34 | 3452ms | 5750ms | 9575ms |
| 361.0 | 371.0 | end-users | ok | 184 | 1528ms | 3686ms | 4869ms |
| 371.0 | 382.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 382.0 | app2 | ok | 26 | 4412ms | 8556ms | 9856ms |
| 371.0 | 382.0 | end-users | ok | 217 | 1554ms | 3493ms | 4849ms |
| 382.0 | 392.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app2 | ok | 33 | 3438ms | 8167ms | 9817ms |
| 382.0 | 392.0 | end-users | ok | 177 | 1435ms | 3298ms | 4830ms |
| 392.0 | 402.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app2 | ok | 17 | 2125ms | 7167ms | 9717ms |
| 392.0 | 402.0 | end-users | ok | 185 | 1805ms | 4036ms | 4904ms |
| 402.0 | 412.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app2 | ok | 44 | 3707ms | 6857ms | 9686ms |
| 402.0 | 412.0 | end-users | ok | 223 | 1472ms | 3258ms | 4826ms |
| 412.0 | 422.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | ok | 30 | 3864ms | 8500ms | 9850ms |
| 412.0 | 422.0 | end-users | ok | 156 | 1448ms | 2706ms | 4771ms |
| 422.0 | 432.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app2 | ok | 33 | 3688ms | 7250ms | 9725ms |
| 422.0 | 432.0 | end-users | ok | 229 | 1523ms | 3364ms | 4836ms |
| 432.0 | 442.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | ok | 13 | 5357ms | 9071ms | 9907ms |
| 432.0 | 442.0 | end-users | ok | 164 | 1532ms | 3136ms | 4814ms |
| 442.0 | 452.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | ok | 35 | 3812ms | 7812ms | 9781ms |
| 442.0 | 452.0 | end-users | ok | 173 | 1420ms | 2940ms | 4794ms |
| 452.0 | 462.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | ok | 22 | 1000ms | 3625ms | 4863ms |
| 452.0 | 462.0 | end-users | ok | 198 | 1794ms | 4161ms | 4916ms |
| 462.0 | 472.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | ok | 38 | 2639ms | 4750ms | 9050ms |
| 462.0 | 472.0 | end-users | ok | 197 | 1542ms | 3799ms | 4880ms |
| 472.0 | 482.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | ok | 26 | 2227ms | 4409ms | 4941ms |
| 472.0 | 482.0 | end-users | ok | 185 | 1694ms | 3899ms | 4890ms |
| 482.0 | 492.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | ok | 33 | 1938ms | 5875ms | 9588ms |
| 482.0 | 492.0 | end-users | ok | 200 | 1636ms | 3936ms | 4894ms |
| 492.0 | 502.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | ok | 32 | 3977ms | 7714ms | 9771ms |
| 492.0 | 502.0 | end-users | ok | 177 | 1605ms | 3771ms | 4877ms |
| 502.0 | 512.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app2 | ok | 22 | 4500ms | 8778ms | 9878ms |
| 502.0 | 512.0 | end-users | ok | 228 | 1465ms | 3417ms | 4842ms |
| 512.0 | 522.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app2 | ok | 35 | 4904ms | 8971ms | 9897ms |
| 512.0 | 522.0 | end-users | ok | 214 | 1582ms | 3514ms | 4851ms |
| 522.0 | 532.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app2 | ok | 36 | 4423ms | 8800ms | 9880ms |
| 522.0 | 532.0 | end-users | ok | 164 | 1452ms | 2588ms | 4759ms |
| 532.0 | 542.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app2 | ok | 18 | 2812ms | 5500ms | 9550ms |
| 532.0 | 542.0 | end-users | ok | 196 | 1802ms | 4155ms | 4916ms |
| 542.0 | 552.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 542.0 | 552.0 | app2 | ok | 34 | 3864ms | 7571ms | 9757ms |
| 542.0 | 552.0 | end-users | ok | 218 | 1553ms | 3527ms | 4853ms |
| 552.0 | 562.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 552.0 | 562.0 | app2 | ok | 32 | 6923ms | 9385ms | 9938ms |
| 552.0 | 562.0 | end-users | ok | 202 | 1592ms | 3422ms | 4842ms |
| 562.0 | 572.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 562.0 | 572.0 | app2 | ok | 33 | 4732ms | 8900ms | 9890ms |
| 562.0 | 572.0 | end-users | ok | 172 | 1388ms | 3130ms | 4813ms |
| 572.0 | 582.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 572.0 | 582.0 | app2 | ok | 19 | 4479ms | 8643ms | 9864ms |
| 572.0 | 582.0 | end-users | ok | 175 | 1503ms | 3589ms | 4859ms |
| 582.0 | 592.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 582.0 | 592.0 | app2 | ok | 34 | 4667ms | 8867ms | 9887ms |
| 582.0 | 592.0 | end-users | ok | 224 | 1711ms | 3902ms | 4890ms |
| 592.0 | 602.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 592.0 | 602.0 | app2 | ok | 26 | 4545ms | 8818ms | 9882ms |
| 592.0 | 602.0 | end-users | ok | 169 | 1509ms | 3637ms | 4864ms |
| 602.0 | 612.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 602.0 | 612.0 | app2 | ok | 34 | 6852ms | 9370ms | 9937ms |
| 602.0 | 612.0 | end-users | ok | 214 | 1401ms | 2568ms | 4757ms |
| 612.0 | 622.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 612.0 | 622.0 | app2 | ok | 31 | 6630ms | 9326ms | 9933ms |
| 612.0 | 622.0 | end-users | ok | 204 | 1582ms | 3355ms | 4835ms |
| 622.0 | 633.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 622.0 | 633.0 | app2 | ok | 35 | 5139ms | 9028ms | 9903ms |
| 622.0 | 633.0 | end-users | ok | 159 | 1588ms | 3471ms | 4847ms |
| 633.0 | 643.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 633.0 | 643.0 | app2 | ok | 21 | 6719ms | 9344ms | 9934ms |
| 633.0 | 643.0 | end-users | ok | 206 | 1788ms | 3880ms | 4888ms |
| 643.0 | 653.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 643.0 | 653.0 | app2 | ok | 37 | 4141ms | 8577ms | 9858ms |
| 643.0 | 653.0 | end-users | ok | 169 | 1575ms | 3543ms | 4854ms |
| 653.0 | 663.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 653.0 | 663.0 | app2 | ok | 20 | 5455ms | 9091ms | 9909ms |
| 653.0 | 663.0 | end-users | ok | 210 | 1816ms | 4009ms | 4901ms |
| 663.0 | 673.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 663.0 | 673.0 | app2 | ok | 41 | 2829ms | 4987ms | 9487ms |
| 663.0 | 673.0 | end-users | ok | 174 | 1688ms | 3939ms | 4894ms |
| 673.0 | 683.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 673.0 | 683.0 | app2 | ok | 37 | 3512ms | 6917ms | 9692ms |
| 673.0 | 683.0 | end-users | ok | 255 | 1612ms | 3938ms | 4894ms |
| 683.0 | 693.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 683.0 | 693.0 | app2 | ok | 18 | 3500ms | 8500ms | 9850ms |
| 683.0 | 693.0 | end-users | ok | 153 | 1812ms | 3993ms | 4899ms |
| 693.0 | 703.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 693.0 | 703.0 | app2 | ok | 41 | 4312ms | 8633ms | 9863ms |
| 693.0 | 703.0 | end-users | ok | 229 | 1381ms | 2489ms | 4740ms |
| 703.0 | 713.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 703.0 | 713.0 | app2 | ok | 13 | 1562ms | 4188ms | 4919ms |
| 703.0 | 713.0 | end-users | ok | 138 | 1941ms | 4266ms | 4927ms |
| 713.0 | 723.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 713.0 | 723.0 | app2 | ok | 38 | 4250ms | 8812ms | 9881ms |
| 713.0 | 723.0 | end-users | ok | 241 | 1545ms | 3690ms | 4869ms |
| 723.0 | 733.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 723.0 | 733.0 | app2 | ok | 26 | 2679ms | 4536ms | 4954ms |
| 723.0 | 733.0 | end-users | ok | 190 | 1688ms | 4031ms | 4903ms |
| 733.0 | 743.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 733.0 | 743.0 | app2 | ok | 27 | 3229ms | 7300ms | 9730ms |
| 733.0 | 743.0 | end-users | ok | 180 | 1661ms | 3953ms | 4895ms |
| 743.0 | 753.0 | app1 | ok | 24 | 225ms | 600ms | 960ms |
| 743.0 | 753.0 | app2 | ok | 29 | 6375ms | 9275ms | 9928ms |
| 743.0 | 753.0 | end-users | ok | 182 | 1841ms | 3863ms | 4886ms |
| 753.0 | 763.0 | app1 | ok | 43 | 2125ms | 4368ms | 4937ms |
| 753.0 | 763.0 | app2 | ok | 32 | 6190ms | 9238ms | 9924ms |
| 753.0 | 763.0 | end-users | ok | 128 | 2395ms | 4475ms | 4948ms |
| 763.0 | 773.0 | app1 | ok | 58 | 2661ms | 4532ms | 4953ms |
| 763.0 | 773.0 | app2 | ok | 16 | 7667ms | 9800ms | 26800ms |
| 763.0 | 773.0 | end-users | ok | 187 | 3545ms | 4880ms | 9221ms |
| 773.0 | 783.0 | app1 | ok | 43 | 2066ms | 4328ms | 4933ms |
| 773.0 | 783.0 | app2 | ok | 20 | 8333ms | 22000ms | 29200ms |
| 773.0 | 783.0 | end-users | ok | 132 | 3472ms | 4694ms | 4969ms |
| 783.0 | 793.0 | app1 | ok | 47 | 1930ms | 4161ms | 4916ms |
| 783.0 | 793.0 | app2 | ok | 24 | 7609ms | 9696ms | 25200ms |
| 783.0 | 793.0 | end-users | ok | 154 | 3574ms | 4715ms | 4971ms |
| 793.0 | 803.0 | app1 | ok | 31 | 1635ms | 4031ms | 4903ms |
| 793.0 | 803.0 | app2 | ok | 33 | 5658ms | 9132ms | 9913ms |
| 793.0 | 803.0 | end-users | ok | 127 | 2699ms | 4540ms | 4954ms |
| 803.0 | 813.0 | app1 | ok | 51 | 2462ms | 4490ms | 4949ms |
| 803.0 | 813.0 | app2 | ok | 23 | 5208ms | 9042ms | 9904ms |
| 803.0 | 813.0 | end-users | ok | 164 | 3084ms | 4617ms | 4962ms |
| 813.0 | 823.0 | app1 | ok | 56 | 2667ms | 4533ms | 4953ms |
| 813.0 | 823.0 | app2 | ok | 27 | 5500ms | 9100ms | 9910ms |
| 813.0 | 823.0 | end-users | ok | 175 | 2936ms | 4587ms | 4959ms |
| 823.0 | 833.0 | app1 | ok | 44 | 3043ms | 4957ms | 9450ms |
| 823.0 | 833.0 | app2 | ok | 11 | 3036ms | 4607ms | 4961ms |
| 823.0 | 833.0 | end-users | ok | 126 | 3082ms | 4808ms | 9100ms |
| 833.0 | 843.0 | app1 | ok | 45 | 2042ms | 4338ms | 4934ms |
| 833.0 | 843.0 | app2 | ok | 20 | 7500ms | 9500ms | 9950ms |
| 833.0 | 843.0 | end-users | ok | 153 | 3125ms | 4625ms | 4962ms |
| 843.0 | 853.0 | app1 | ok | 51 | 2025ms | 4203ms | 4920ms |
| 843.0 | 853.0 | app2 | ok | 25 | 7604ms | 9688ms | 25000ms |
| 843.0 | 853.0 | end-users | ok | 160 | 3438ms | 4688ms | 4969ms |
| 853.0 | 863.0 | app1 | ok | 41 | 1671ms | 3975ms | 4897ms |
| 853.0 | 863.0 | app2 | ok | 37 | 6300ms | 9260ms | 9926ms |
| 853.0 | 863.0 | end-users | ok | 157 | 2956ms | 4591ms | 4959ms |
| 863.0 | 873.0 | app1 | ok | 63 | 2306ms | 4438ms | 4944ms |
| 863.0 | 873.0 | app2 | ok | 26 | 6000ms | 9467ms | 24800ms |
| 863.0 | 873.0 | end-users | ok | 201 | 3205ms | 4641ms | 4964ms |
| 873.0 | 884.0 | app1 | ok | 45 | 2057ms | 4297ms | 4930ms |
| 873.0 | 884.0 | app2 | ok | 12 | 7500ms | 9500ms | 9950ms |
| 873.0 | 884.0 | end-users | ok | 129 | 3534ms | 4707ms | 4971ms |
| 884.0 | 894.0 | app1 | ok | 41 | 1989ms | 4212ms | 4921ms |
| 884.0 | 894.0 | app2 | ok | 20 | 8333ms | 22000ms | 29200ms |
| 884.0 | 894.0 | end-users | ok | 130 | 3452ms | 4690ms | 4969ms |
| 894.0 | 904.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 894.0 | 904.0 | app2 | ok | 16 | 6364ms | 9273ms | 9927ms |
| 894.0 | 904.0 | end-users | ok | 20 | 3750ms | 4750ms | 4975ms |
| 904.0 | 914.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 904.0 | 914.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 904.0 | 914.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 914.0 | 924.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 914.0 | 924.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 914.0 | 924.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 924.0 | 934.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 924.0 | 934.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 924.0 | 934.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 934.0 | 944.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 934.0 | 944.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 934.0 | 944.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 944.0 | 954.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 944.0 | 954.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 944.0 | 954.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 954.0 | 964.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 954.0 | 964.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 954.0 | 964.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 964.0 | 975.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 964.0 | 975.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 964.0 | 975.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 975.0 | 985.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 975.0 | 985.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 975.0 | 985.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 985.0 | 995.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 985.0 | 995.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 985.0 | 995.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 995.0 | 1005.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 995.0 | 1005.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 995.0 | 1005.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1005.0 | 1015.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1005.0 | 1015.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1005.0 | 1015.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1015.0 | 1025.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1015.0 | 1025.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1015.0 | 1025.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1025.0 | 1035.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1025.0 | 1035.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1025.0 | 1035.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1035.0 | 1045.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1035.0 | 1045.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1035.0 | 1045.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1045.0 | 1055.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1045.0 | 1055.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1045.0 | 1055.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1055.0 | 1065.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1055.0 | 1065.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1055.0 | 1065.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1065.0 | 1075.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1065.0 | 1075.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1065.0 | 1075.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1075.0 | 1085.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1075.0 | 1085.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1075.0 | 1085.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1085.0 | 1095.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1085.0 | 1095.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1085.0 | 1095.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1095.0 | 1105.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1095.0 | 1105.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1095.0 | 1105.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1105.0 | 1115.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1105.0 | 1115.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1105.0 | 1115.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1115.0 | 1125.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1115.0 | 1125.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1115.0 | 1125.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1125.0 | 1135.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1125.0 | 1135.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1125.0 | 1135.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1135.0 | 1145.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1135.0 | 1145.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1135.0 | 1145.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1145.0 | 1155.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1145.0 | 1155.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1145.0 | 1155.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1155.0 | 1165.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1155.0 | 1165.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1155.0 | 1165.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1165.0 | 1175.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1165.0 | 1175.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1165.0 | 1175.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1175.0 | 1186.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1175.0 | 1186.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1175.0 | 1186.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1186.0 | 1196.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1186.0 | 1196.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1186.0 | 1196.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 1196.0 | 1196.0 | app1 | ok | 683 | 2106ms | 4391ms | 4973ms |
| 1196.0 | 1196.0 | app2 | ok | 2481 | 4752ms | 9042ms | 14494ms |
| 1196.0 | 1196.0 | end-users | ok | 16038 | 1966ms | 4288ms | 4938ms |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1734300 | 86584 | 1820884.0 | 0.0% | 1858836.0 | 1907468.0 | -2.5% | True |
| app2 | 3050400 | 152162 | 3202562.0 | 0.0% | 3318106.0 | 3354724.0 | -1.1% | True |
| end-users | 19711980 | 982969 | 20694949.0 | 0.0% | 21483110.0 | 21677918.0 | -0.9% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1410 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | 0.0% | 0.00 |
| app2 | 2481 | 0 | 1 | 1 | 0.04% | 10.5% | 100.0% | 9.50 |
| end-users | 16038 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | 0.0% | 0.00 |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=19929). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 19929 | 0.051ms | 0.112ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 1131291 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1410 | 6621ms | 9459ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 2480 | 11931ms | 14997ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 16026 | 6828ms | 9801ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 19916 | 7105ms | 13110ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (120 windows, EPP restart detected mid-window at least once):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2667ms | 5650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2250ms | 5450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 3188ms | 5635ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 6640ms | 9314ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 10500ms | 14550ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 7688ms | 11523ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 6724ms | 9060ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 12875ms | 18083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 8244ms | 10219ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 6269ms | 8675ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 12625ms | 14988ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 8322ms | 9872ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 6667ms | 9400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 12400ms | 17333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 8354ms | 11545ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 6913ms | 9736ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 12794ms | 17625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 8268ms | 13664ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 6806ms | 7981ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 13158ms | 18800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 8278ms | 9828ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 6680ms | 9329ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 12727ms | 17000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 8442ms | 11455ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 6636ms | 9467ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 13158ms | 18800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 8214ms | 12268ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 6400ms | 9600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 13125ms | 18750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 8459ms | 13717ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 6967ms | 9357ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 13553ms | 19156ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 8337ms | 9834ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 6962ms | 9530ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 12727ms | 17000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 8494ms | 12706ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 131.0 | app1 | ok | 6586ms | 8775ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 131.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 131.0 | end-users | ok | 8300ms | 9830ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 6739ms | 9438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 13333ms | 19000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 8567ms | 13611ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 7200ms | 9729ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 13529ms | 19143ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 8255ms | 13931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 6625ms | 9525ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 12935ms | 18312ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 8000ms | 13182ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 12283ms | 14728ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 6448ms | 9179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 12174ms | 14717ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 6654ms | 9556ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 11125ms | 14612ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 6491ms | 8614ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 11923ms | 14692ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 6352ms | 9492ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 12386ms | 14739ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 6569ms | 9560ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 9579ms | 14357ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 6817ms | 9183ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 11375ms | 14638ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 6296ms | 9324ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 11771ms | 14677ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 6295ms | 9050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 11429ms | 14643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 6221ms | 9035ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 11827ms | 14683ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 6452ms | 9503ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | ok | 10357ms | 14536ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | ok | 6371ms | 8485ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | ok | 11771ms | 14677ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | end-users | ok | 6423ms | 7842ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | ok | 12100ms | 14710ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | end-users | ok | 6416ms | 7937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | ok | 11111ms | 14611ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | end-users | ok | 6375ms | 7966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app2 | ok | 11800ms | 14680ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | end-users | ok | 6479ms | 7940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app2 | ok | 11875ms | 14688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | end-users | ok | 6277ms | 7844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app2 | ok | 12065ms | 14707ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | end-users | ok | 6316ms | 7832ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app2 | ok | 12232ms | 14723ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | end-users | ok | 5964ms | 8713ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app2 | ok | 11429ms | 14643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | end-users | ok | 6224ms | 9566ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app2 | ok | 10893ms | 14589ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | end-users | ok | 6367ms | 9421ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app2 | ok | 11136ms | 14614ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | end-users | ok | 6351ms | 9377ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 382.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 382.0 | app2 | ok | 11522ms | 14652ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 382.0 | end-users | ok | 6474ms | 9196ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app2 | ok | 10357ms | 14536ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | end-users | ok | 6215ms | 7889ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | app2 | ok | 11897ms | 14690ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | end-users | ok | 6247ms | 9016ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | app2 | ok | 9333ms | 14125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | end-users | ok | 6470ms | 9426ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app2 | ok | 11786ms | 14679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | end-users | ok | 6214ms | 7961ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app2 | ok | 12417ms | 14742ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | end-users | ok | 6054ms | 7923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app2 | ok | 11250ms | 14625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | end-users | ok | 6138ms | 7967ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app2 | ok | 11786ms | 14679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | end-users | ok | 6154ms | 9267ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app2 | ok | 11087ms | 14609ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | end-users | ok | 6356ms | 9085ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app2 | ok | 11528ms | 14653ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | end-users | ok | 6187ms | 9347ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app2 | ok | 9667ms | 14433ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | end-users | ok | 6309ms | 9311ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app2 | ok | 12400ms | 14740ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | end-users | ok | 6321ms | 9258ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app2 | ok | 8333ms | 14222ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | end-users | ok | 6134ms | 9443ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app2 | ok | 12054ms | 14705ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | end-users | ok | 6284ms | 9403ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app2 | ok | 10312ms | 14531ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | end-users | ok | 6231ms | 8906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app2 | ok | 11875ms | 14688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | end-users | ok | 6146ms | 7946ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | app2 | ok | 11923ms | 14692ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | end-users | ok | 6586ms | 9403ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 552.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 552.0 | app2 | ok | 9267ms | 14156ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 552.0 | end-users | ok | 6459ms | 9535ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 552.0 | 562.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 552.0 | 562.0 | app2 | ok | 12222ms | 14722ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 552.0 | 562.0 | end-users | ok | 6361ms | 7836ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 562.0 | 572.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 562.0 | 572.0 | app2 | ok | 11786ms | 14679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 562.0 | 572.0 | end-users | ok | 6397ms | 7840ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 572.0 | 582.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 572.0 | 582.0 | app2 | ok | 12241ms | 14724ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 572.0 | 582.0 | end-users | ok | 6504ms | 7865ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 582.0 | 592.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 582.0 | 592.0 | app2 | ok | 12417ms | 14742ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 582.0 | 592.0 | end-users | ok | 6462ms | 8859ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 592.0 | 602.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 592.0 | 602.0 | app2 | ok | 10735ms | 14574ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 592.0 | 602.0 | end-users | ok | 6243ms | 9367ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 602.0 | 612.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 602.0 | 612.0 | app2 | ok | 9938ms | 14483ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 602.0 | 612.0 | end-users | ok | 6566ms | 9076ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 612.0 | 622.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 612.0 | 622.0 | app2 | ok | 12200ms | 14720ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 612.0 | 622.0 | end-users | ok | 6430ms | 7969ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 622.0 | 633.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 622.0 | 633.0 | app2 | ok | 11875ms | 14688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 622.0 | 633.0 | end-users | ok | 6471ms | 7921ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 633.0 | 643.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 633.0 | 643.0 | app2 | ok | 11739ms | 14674ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 633.0 | 643.0 | end-users | ok | 6392ms | 7854ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 643.0 | 653.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 643.0 | 653.0 | app2 | ok | 11875ms | 14688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 643.0 | 653.0 | end-users | ok | 6431ms | 7858ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 653.0 | 663.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 653.0 | 663.0 | app2 | ok | 12212ms | 14721ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 653.0 | 663.0 | end-users | ok | 6278ms | 8687ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 663.0 | 673.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 663.0 | 673.0 | app2 | ok | 10781ms | 14578ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 663.0 | 673.0 | end-users | ok | 6523ms | 9390ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 673.0 | 683.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 673.0 | 683.0 | app2 | ok | 11250ms | 14625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 673.0 | 683.0 | end-users | ok | 6414ms | 9536ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 683.0 | 693.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 683.0 | 693.0 | app2 | ok | 11771ms | 14677ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 683.0 | 693.0 | end-users | ok | 6324ms | 8375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 693.0 | 703.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 693.0 | 703.0 | app2 | ok | 10882ms | 14588ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 693.0 | 703.0 | end-users | ok | 6442ms | 7988ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 703.0 | 713.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 703.0 | 713.0 | app2 | ok | 12308ms | 14731ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 703.0 | 713.0 | end-users | ok | 6750ms | 9550ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 713.0 | 723.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 713.0 | 723.0 | app2 | ok | 9600ms | 14333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 713.0 | 723.0 | end-users | ok | 6433ms | 8546ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 723.0 | 733.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 723.0 | 733.0 | app2 | ok | 12065ms | 14707ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 723.0 | 733.0 | end-users | ok | 6431ms | 7872ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 733.0 | 743.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 733.0 | 743.0 | app2 | ok | 12083ms | 14708ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 733.0 | 743.0 | end-users | ok | 6462ms | 7952ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 743.0 | 753.0 | app1 | ok | 1375ms | 1488ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 743.0 | 753.0 | app2 | ok | 11538ms | 14654ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 743.0 | 753.0 | end-users | ok | 6549ms | 9095ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 753.0 | 763.0 | app1 | ok | 5154ms | 6700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 753.0 | 763.0 | app2 | ok | 11765ms | 14676ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 753.0 | 763.0 | end-users | ok | 8141ms | 9860ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 763.0 | 773.0 | app1 | ok | 7000ms | 9685ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 763.0 | 773.0 | app2 | ok | 13824ms | 19278ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 763.0 | 773.0 | end-users | ok | 8538ms | 12464ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 773.0 | 783.0 | app1 | ok | 7118ms | 9706ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 773.0 | 783.0 | app2 | ok | 12692ms | 18750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 773.0 | 783.0 | end-users | ok | 8550ms | 14204ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 783.0 | 793.0 | app1 | ok | 6684ms | 9573ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 783.0 | 793.0 | app2 | ok | 13000ms | 18500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 783.0 | 793.0 | end-users | ok | 7970ms | 13227ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 793.0 | 803.0 | app1 | ok | 6500ms | 9600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 793.0 | 803.0 | app2 | ok | 13000ms | 18500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 793.0 | 803.0 | end-users | ok | 8133ms | 13026ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 803.0 | 813.0 | app1 | ok | 6710ms | 8800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 803.0 | 813.0 | app2 | ok | 13281ms | 18950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 803.0 | 813.0 | end-users | ok | 8178ms | 11942ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 813.0 | 823.0 | app1 | ok | 6348ms | 8850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 813.0 | 823.0 | app2 | ok | 13676ms | 19219ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 813.0 | 823.0 | end-users | ok | 8341ms | 10250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 823.0 | 833.0 | app1 | ok | 6696ms | 9527ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 823.0 | 833.0 | app2 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 823.0 | 833.0 | end-users | ok | 8492ms | 13435ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 833.0 | 843.0 | app1 | ok | 7133ms | 9475ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 833.0 | 843.0 | app2 | ok | 13333ms | 19000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 833.0 | 843.0 | end-users | ok | 8090ms | 9924ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 843.0 | 853.0 | app1 | ok | 6538ms | 8850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 843.0 | 853.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 843.0 | 853.0 | end-users | ok | 8247ms | 11591ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 853.0 | 863.0 | app1 | ok | 6923ms | 9520ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 853.0 | 863.0 | app2 | ok | 12609ms | 14957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 853.0 | 863.0 | end-users | ok | 8095ms | 12833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 863.0 | 873.0 | app1 | ok | 6250ms | 8750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 863.0 | 873.0 | app2 | ok | 14545ms | 19444ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 863.0 | 873.0 | end-users | ok | 8203ms | 9980ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 873.0 | 884.0 | app1 | ok | 7176ms | 9969ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 873.0 | 884.0 | app2 | ok | 13929ms | 19438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 873.0 | 884.0 | end-users | ok | 7903ms | 13882ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 884.0 | 894.0 | app1 | ok | 6444ms | 9689ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 884.0 | 894.0 | app2 | ok | 12386ms | 14739ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 884.0 | 894.0 | end-users | ok | 8226ms | 13190ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 894.0 | 904.0 | app1 | ok | 7600ms | 9756ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 894.0 | 904.0 | app2 | ok | 12059ms | 18250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 894.0 | 904.0 | end-users | ok | 8559ms | 13917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 904.0 | 914.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 904.0 | 914.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 904.0 | 914.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 914.0 | 924.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 914.0 | 924.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 914.0 | 924.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 924.0 | 934.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 924.0 | 934.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 924.0 | 934.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 934.0 | 944.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 934.0 | 944.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 934.0 | 944.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 944.0 | 954.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 944.0 | 954.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 944.0 | 954.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 954.0 | 964.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 954.0 | 964.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 954.0 | 964.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 964.0 | 975.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 964.0 | 975.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 964.0 | 975.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 975.0 | 985.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 975.0 | 985.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 975.0 | 985.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 985.0 | 995.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 985.0 | 995.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 985.0 | 995.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 995.0 | 1005.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 995.0 | 1005.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 995.0 | 1005.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1005.0 | 1015.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1005.0 | 1015.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1005.0 | 1015.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1015.0 | 1025.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1015.0 | 1025.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1015.0 | 1025.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1025.0 | 1035.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1025.0 | 1035.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1025.0 | 1035.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1035.0 | 1045.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1035.0 | 1045.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1035.0 | 1045.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1045.0 | 1055.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1045.0 | 1055.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1045.0 | 1055.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1055.0 | 1065.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1055.0 | 1065.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1055.0 | 1065.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1065.0 | 1075.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1065.0 | 1075.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1065.0 | 1075.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1075.0 | 1085.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1075.0 | 1085.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1075.0 | 1085.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1085.0 | 1095.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1085.0 | 1095.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1085.0 | 1095.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1095.0 | 1105.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1095.0 | 1105.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1095.0 | 1105.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1105.0 | 1115.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1105.0 | 1115.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1105.0 | 1115.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1115.0 | 1125.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1115.0 | 1125.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1115.0 | 1125.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1125.0 | 1135.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1125.0 | 1135.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1125.0 | 1135.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1135.0 | 1145.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1135.0 | 1145.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1135.0 | 1145.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1145.0 | 1155.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1145.0 | 1155.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1145.0 | 1155.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1155.0 | 1165.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1155.0 | 1165.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1155.0 | 1165.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1165.0 | 1175.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1165.0 | 1175.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1165.0 | 1175.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1175.0 | 1186.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1175.0 | 1186.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1175.0 | 1186.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1186.0 | 1196.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1186.0 | 1196.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1186.0 | 1196.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1196.0 | 1196.0 | app1 | ok | 6621ms | 9459ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1196.0 | 1196.0 | app2 | ok | 11931ms | 14997ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 1196.0 | 1196.0 | end-users | ok | 6828ms | 9801ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
