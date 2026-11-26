# Fairness benchmark: six-group-board-case (uni310-l3-r1-uni165-dominant)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 36.9 points

## Run metadata

| field | value |
|---|---|
| Scenario | `six-group-board-case` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5b867694ff-hxs6v` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T03:30:18Z` |
| Run end | `2026-11-26T03:39:13Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 55 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/55 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 100.50 | 3.1406 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 90.0 | 181 | 4642 | 000=3, 200=4639 | 9.0 | 12.3 | 6148834.0 | 90.0% | 53.1% | -36.9 | 87.1% | -2.9 | 86.2% | -3.8 | 72.0s | 98.9% | 4642.0 |
| app2 | 2.0 | 32 | 149 | 200=149 | 54.9 | 78.3 | 183944.0 | 2.0% | 9.4% | 7.4 | 2.6% | 0.6 | 2.8% | 0.8 | 73.3s | 98.9% | 149.0 |
| app3 | 2.0 | 32 | 149 | 200=149 | 54.8 | 78.6 | 188058.0 | 2.0% | 9.4% | 7.4 | 2.7% | 0.7 | 2.8% | 0.8 | 73.3s | 98.9% | 149.0 |
| app4 | 2.0 | 32 | 150 | 200=150 | 55.0 | 78.8 | 178420.0 | 2.0% | 9.4% | 7.4 | 2.5% | 0.5 | 2.8% | 0.8 | 73.3s | 98.9% | 150.0 |
| app5 | 2.0 | 32 | 149 | 200=149 | 55.0 | 78.2 | 182522.0 | 2.0% | 9.4% | 7.4 | 2.6% | 0.6 | 2.8% | 0.8 | 73.3s | 98.9% | 149.0 |
| app6 | 2.0 | 32 | 149 | 200=149 | 55.4 | 79.0 | 181322.0 | 2.0% | 9.4% | 7.4 | 2.6% | 0.6 | 2.8% | 0.8 | 73.3s | 98.9% | 149.0 |
| end-users | n/a | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- app3: active 0s-240s, no duty cycle
- app4: active 0s-240s, no duty cycle
- app5: active 0s-240s, no duty cycle
- app6: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 70.0 | 70.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (54 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | True | 0.0 | 90.0% | n/a | n/a |
| 0.0 | 10.0 | app2 | True | True | 0.0 | 2.0% | n/a | n/a |
| 0.0 | 10.0 | app3 | True | True | 0.0 | 2.0% | n/a | n/a |
| 0.0 | 10.0 | app4 | True | True | 0.0 | 2.0% | n/a | n/a |
| 0.0 | 10.0 | app5 | True | True | 0.0 | 2.0% | n/a | n/a |
| 0.0 | 10.0 | app6 | True | True | 0.0 | 2.0% | n/a | n/a |
| 10.0 | 20.0 | app1 | True | False | 186840.0 | 90.0% | 100.0% | 10.0 |
| 10.0 | 20.0 | app2 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 10.0 | 20.0 | app3 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 10.0 | 20.0 | app4 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 10.0 | 20.0 | app5 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 10.0 | 20.0 | app6 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 20.0 | 30.0 | app1 | True | False | 288002.0 | 90.0% | 99.5% | 9.5 |
| 20.0 | 30.0 | app2 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 20.0 | 30.0 | app3 | True | False | 1358.0 | 2.0% | 0.5% | -1.5 |
| 20.0 | 30.0 | app4 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 20.0 | 30.0 | app5 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 20.0 | 30.0 | app6 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 30.0 | 40.0 | app1 | True | False | 294540.0 | 90.0% | 96.0% | 6.0 |
| 30.0 | 40.0 | app2 | True | False | 4042.0 | 2.0% | 1.3% | -0.7 |
| 30.0 | 40.0 | app3 | True | False | 6784.0 | 2.0% | 2.2% | 0.2 |
| 30.0 | 40.0 | app4 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 30.0 | 40.0 | app5 | True | False | 1340.0 | 2.0% | 0.4% | -1.6 |
| 30.0 | 40.0 | app6 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 40.0 | 50.0 | app1 | True | False | 275758.0 | 90.0% | 90.7% | 0.7 |
| 40.0 | 50.0 | app2 | True | False | 4060.0 | 2.0% | 1.3% | -0.7 |
| 40.0 | 50.0 | app3 | True | False | 6756.0 | 2.0% | 2.2% | 0.2 |
| 40.0 | 50.0 | app4 | True | False | 4058.0 | 2.0% | 1.3% | -0.7 |
| 40.0 | 50.0 | app5 | True | False | 6766.0 | 2.0% | 2.2% | 0.2 |
| 40.0 | 50.0 | app6 | True | False | 6762.0 | 2.0% | 2.2% | 0.2 |
| 50.0 | 60.0 | app1 | True | False | 157002.0 | 90.0% | 83.5% | -6.5 |
| 50.0 | 60.0 | app2 | True | False | 8136.0 | 2.0% | 4.3% | 2.3 |
| 50.0 | 60.0 | app3 | True | False | 5418.0 | 2.0% | 2.9% | 0.9 |
| 50.0 | 60.0 | app4 | True | False | 5408.0 | 2.0% | 2.9% | 0.9 |
| 50.0 | 60.0 | app5 | True | False | 5374.0 | 2.0% | 2.9% | 0.9 |
| 50.0 | 60.0 | app6 | True | False | 6756.0 | 2.0% | 3.6% | 1.6 |
| 60.0 | 70.0 | app1 | True | False | 63570.0 | 90.0% | 29.4% | -60.6 |
| 60.0 | 70.0 | app2 | True | False | 31046.0 | 2.0% | 14.3% | 12.3 |
| 60.0 | 70.0 | app3 | True | False | 29752.0 | 2.0% | 13.8% | 11.8 |
| 60.0 | 70.0 | app4 | True | False | 31122.0 | 2.0% | 14.4% | 12.4 |
| 60.0 | 70.0 | app5 | True | False | 31064.0 | 2.0% | 14.4% | 12.4 |
| 60.0 | 70.0 | app6 | True | False | 29824.0 | 2.0% | 13.8% | 11.8 |
| 70.0 | 80.0 | app1 | True | False | 239428.0 | 90.0% | 90.8% | 0.8 |
| 70.0 | 80.0 | app2 | True | False | 4074.0 | 2.0% | 1.5% | -0.5 |
| 70.0 | 80.0 | app3 | True | False | 5406.0 | 2.0% | 2.0% | 0.0 |
| 70.0 | 80.0 | app4 | True | False | 4054.0 | 2.0% | 1.5% | -0.5 |
| 70.0 | 80.0 | app5 | True | False | 5408.0 | 2.0% | 2.1% | 0.1 |
| 70.0 | 80.0 | app6 | True | False | 5408.0 | 2.0% | 2.1% | 0.1 |
| 80.0 | 90.0 | app1 | True | False | 306964.0 | 90.0% | 100.0% | 10.0 |
| 80.0 | 90.0 | app2 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 80.0 | 90.0 | app3 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 80.0 | 90.0 | app4 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 80.0 | 90.0 | app5 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 80.0 | 90.0 | app6 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 90.0 | 100.0 | app1 | True | False | 263774.0 | 90.0% | 90.7% | 0.7 |
| 90.0 | 100.0 | app2 | True | False | 5394.0 | 2.0% | 1.9% | -0.1 |
| 90.0 | 100.0 | app3 | True | False | 5408.0 | 2.0% | 1.9% | -0.1 |
| 90.0 | 100.0 | app4 | True | False | 5418.0 | 2.0% | 1.9% | -0.1 |
| 90.0 | 100.0 | app5 | True | False | 5402.0 | 2.0% | 1.9% | -0.1 |
| 90.0 | 100.0 | app6 | True | False | 5416.0 | 2.0% | 1.9% | -0.1 |
| 100.0 | 110.0 | app1 | True | False | 276194.0 | 90.0% | 90.7% | 0.7 |
| 100.0 | 110.0 | app2 | True | False | 5432.0 | 2.0% | 1.8% | -0.2 |
| 100.0 | 110.0 | app3 | True | False | 5396.0 | 2.0% | 1.8% | -0.2 |
| 100.0 | 110.0 | app4 | True | False | 5404.0 | 2.0% | 1.8% | -0.2 |
| 100.0 | 110.0 | app5 | True | False | 6742.0 | 2.0% | 2.2% | 0.2 |
| 100.0 | 110.0 | app6 | True | False | 5398.0 | 2.0% | 1.8% | -0.2 |
| 110.0 | 120.0 | app1 | True | False | 270658.0 | 90.0% | 90.1% | 0.1 |
| 110.0 | 120.0 | app2 | True | False | 5402.0 | 2.0% | 1.8% | -0.2 |
| 110.0 | 120.0 | app3 | True | False | 6790.0 | 2.0% | 2.3% | 0.3 |
| 110.0 | 120.0 | app4 | True | False | 6788.0 | 2.0% | 2.3% | 0.3 |
| 110.0 | 120.0 | app5 | True | False | 5432.0 | 2.0% | 1.8% | -0.2 |
| 110.0 | 120.0 | app6 | True | False | 5418.0 | 2.0% | 1.8% | -0.2 |
| 120.0 | 131.0 | app1 | True | False | 229930.0 | 90.0% | 90.9% | 0.9 |
| 120.0 | 131.0 | app2 | True | False | 5418.0 | 2.0% | 2.1% | 0.1 |
| 120.0 | 131.0 | app3 | True | False | 4038.0 | 2.0% | 1.6% | -0.4 |
| 120.0 | 131.0 | app4 | True | False | 4074.0 | 2.0% | 1.6% | -0.4 |
| 120.0 | 131.0 | app5 | True | False | 4036.0 | 2.0% | 1.6% | -0.4 |
| 120.0 | 131.0 | app6 | True | False | 5432.0 | 2.0% | 2.1% | 0.1 |
| 131.0 | 141.0 | app1 | True | False | 273334.0 | 90.0% | 89.8% | -0.2 |
| 131.0 | 141.0 | app2 | True | False | 6760.0 | 2.0% | 2.2% | 0.2 |
| 131.0 | 141.0 | app3 | True | False | 5424.0 | 2.0% | 1.8% | -0.2 |
| 131.0 | 141.0 | app4 | True | False | 6702.0 | 2.0% | 2.2% | 0.2 |
| 131.0 | 141.0 | app5 | True | False | 6784.0 | 2.0% | 2.2% | 0.2 |
| 131.0 | 141.0 | app6 | True | False | 5404.0 | 2.0% | 1.8% | -0.2 |
| 141.0 | 151.0 | app1 | True | False | 273334.0 | 90.0% | 89.8% | -0.2 |
| 141.0 | 151.0 | app2 | True | False | 6740.0 | 2.0% | 2.2% | 0.2 |
| 141.0 | 151.0 | app3 | True | False | 5432.0 | 2.0% | 1.8% | -0.2 |
| 141.0 | 151.0 | app4 | True | False | 6774.0 | 2.0% | 2.2% | 0.2 |
| 141.0 | 151.0 | app5 | True | False | 6790.0 | 2.0% | 2.2% | 0.2 |
| 141.0 | 151.0 | app6 | True | False | 5402.0 | 2.0% | 1.8% | -0.2 |
| 151.0 | 161.0 | app1 | True | False | 263682.0 | 90.0% | 89.0% | -1.0 |
| 151.0 | 161.0 | app2 | True | False | 5428.0 | 2.0% | 1.8% | -0.2 |
| 151.0 | 161.0 | app3 | True | False | 8138.0 | 2.0% | 2.7% | 0.7 |
| 151.0 | 161.0 | app4 | True | False | 5428.0 | 2.0% | 1.8% | -0.2 |
| 151.0 | 161.0 | app5 | True | False | 5408.0 | 2.0% | 1.8% | -0.2 |
| 151.0 | 161.0 | app6 | True | False | 8134.0 | 2.0% | 2.7% | 0.7 |
| 161.0 | 171.0 | app1 | True | False | 276012.0 | 90.0% | 91.1% | 1.1 |
| 161.0 | 171.0 | app2 | True | False | 5418.0 | 2.0% | 1.8% | -0.2 |
| 161.0 | 171.0 | app3 | True | False | 5414.0 | 2.0% | 1.8% | -0.2 |
| 161.0 | 171.0 | app4 | True | False | 5400.0 | 2.0% | 1.8% | -0.2 |
| 161.0 | 171.0 | app5 | True | False | 5416.0 | 2.0% | 1.8% | -0.2 |
| 161.0 | 171.0 | app6 | True | False | 5412.0 | 2.0% | 1.8% | -0.2 |
| 171.0 | 181.0 | app1 | True | False | 270442.0 | 90.0% | 89.3% | -0.7 |
| 171.0 | 181.0 | app2 | True | False | 6754.0 | 2.0% | 2.2% | 0.2 |
| 171.0 | 181.0 | app3 | True | False | 6732.0 | 2.0% | 2.2% | 0.2 |
| 171.0 | 181.0 | app4 | True | False | 6742.0 | 2.0% | 2.2% | 0.2 |
| 171.0 | 181.0 | app5 | True | False | 6746.0 | 2.0% | 2.2% | 0.2 |
| 171.0 | 181.0 | app6 | True | False | 5412.0 | 2.0% | 1.8% | -0.2 |
| 181.0 | 191.0 | app1 | True | False | 275976.0 | 90.0% | 90.7% | 0.7 |
| 181.0 | 191.0 | app2 | True | False | 5422.0 | 2.0% | 1.8% | -0.2 |
| 181.0 | 191.0 | app3 | True | False | 5414.0 | 2.0% | 1.8% | -0.2 |
| 181.0 | 191.0 | app4 | True | False | 5414.0 | 2.0% | 1.8% | -0.2 |
| 181.0 | 191.0 | app5 | True | False | 5432.0 | 2.0% | 1.8% | -0.2 |
| 181.0 | 191.0 | app6 | True | False | 6760.0 | 2.0% | 2.2% | 0.2 |
| 191.0 | 201.0 | app1 | True | False | 274462.0 | 90.0% | 90.6% | 0.6 |
| 191.0 | 201.0 | app2 | True | False | 5412.0 | 2.0% | 1.8% | -0.2 |
| 191.0 | 201.0 | app3 | True | False | 5422.0 | 2.0% | 1.8% | -0.2 |
| 191.0 | 201.0 | app4 | True | False | 5422.0 | 2.0% | 1.8% | -0.2 |
| 191.0 | 201.0 | app5 | True | False | 5398.0 | 2.0% | 1.8% | -0.2 |
| 191.0 | 201.0 | app6 | True | False | 6744.0 | 2.0% | 2.2% | 0.2 |
| 201.0 | 211.0 | app1 | True | False | 272994.0 | 90.0% | 89.4% | -0.6 |
| 201.0 | 211.0 | app2 | True | False | 6752.0 | 2.0% | 2.2% | 0.2 |
| 201.0 | 211.0 | app3 | True | False | 6768.0 | 2.0% | 2.2% | 0.2 |
| 201.0 | 211.0 | app4 | True | False | 6708.0 | 2.0% | 2.2% | 0.2 |
| 201.0 | 211.0 | app5 | True | False | 6750.0 | 2.0% | 2.2% | 0.2 |
| 201.0 | 211.0 | app6 | True | False | 5368.0 | 2.0% | 1.8% | -0.2 |
| 211.0 | 221.0 | app1 | True | False | 271816.0 | 90.0% | 88.9% | -1.1 |
| 211.0 | 221.0 | app2 | True | False | 6752.0 | 2.0% | 2.2% | 0.2 |
| 211.0 | 221.0 | app3 | True | False | 6742.0 | 2.0% | 2.2% | 0.2 |
| 211.0 | 221.0 | app4 | True | False | 6762.0 | 2.0% | 2.2% | 0.2 |
| 211.0 | 221.0 | app5 | True | False | 6762.0 | 2.0% | 2.2% | 0.2 |
| 211.0 | 221.0 | app6 | True | False | 6790.0 | 2.0% | 2.2% | 0.2 |
| 221.0 | 231.0 | app1 | True | False | 275966.0 | 90.0% | 91.5% | 1.5 |
| 221.0 | 231.0 | app2 | True | False | 5432.0 | 2.0% | 1.8% | -0.2 |
| 221.0 | 231.0 | app3 | True | False | 5400.0 | 2.0% | 1.8% | -0.2 |
| 221.0 | 231.0 | app4 | True | False | 5432.0 | 2.0% | 1.8% | -0.2 |
| 221.0 | 231.0 | app5 | True | False | 5432.0 | 2.0% | 1.8% | -0.2 |
| 221.0 | 231.0 | app6 | True | False | 4058.0 | 2.0% | 1.3% | -0.7 |
| 231.0 | 241.0 | app1 | True | False | 254394.0 | 90.0% | 88.2% | -1.8 |
| 231.0 | 241.0 | app2 | True | False | 6760.0 | 2.0% | 2.3% | 0.3 |
| 231.0 | 241.0 | app3 | True | False | 6780.0 | 2.0% | 2.4% | 0.4 |
| 231.0 | 241.0 | app4 | True | False | 6790.0 | 2.0% | 2.4% | 0.4 |
| 231.0 | 241.0 | app5 | True | False | 6790.0 | 2.0% | 2.4% | 0.4 |
| 231.0 | 241.0 | app6 | True | False | 6784.0 | 2.0% | 2.4% | 0.4 |
| 241.0 | 251.0 | app1 | False | n/a | 280034.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 5412.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | n/a | 4062.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app4 | False | n/a | 5394.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app5 | False | n/a | 4074.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app6 | False | n/a | 6770.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 33728.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 37898.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | False | n/a | 39224.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | False | n/a | 39126.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | False | n/a | 39176.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | False | n/a | 37870.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 352.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 352.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 352.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 352.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 352.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 352.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 535.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 535.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 535.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 535.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 535.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 535.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 219 | 1264ms | 2620ms | 4762ms |
| 0.0 | 10.0 | app2 | ok | 13 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app3 | ok | 10 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app4 | ok | 18 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app5 | ok | 14 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app6 | ok | 15 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 118 | 5845ms | 9169ms | 9917ms |
| 10.0 | 20.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 222 | 3725ms | 4846ms | 8890ms |
| 20.0 | 30.0 | app2 | ok | 2 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app3 | ok | 3 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 196 | 3419ms | 4684ms | 4968ms |
| 30.0 | 40.0 | app2 | ok | 3 | 37500ms | 55500ms | 59550ms |
| 30.0 | 40.0 | app3 | ok | 4 | 23333ms | 48000ms | 58800ms |
| 30.0 | 40.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app5 | ok | 4 | 30000ms | 54000ms | 59400ms |
| 30.0 | 40.0 | app6 | ok | 3 | 25000ms | 51000ms | 59100ms |
| 40.0 | 50.0 | app1 | ok | 226 | 3367ms | 4905ms | 9335ms |
| 40.0 | 50.0 | app2 | ok | 33 | 39375ms | 55875ms | 59588ms |
| 40.0 | 50.0 | app3 | ok | 34 | 37826ms | 55565ms | 59557ms |
| 40.0 | 50.0 | app4 | ok | 33 | 40962ms | 56192ms | 59619ms |
| 40.0 | 50.0 | app5 | ok | 33 | 40200ms | 56040ms | 59604ms |
| 40.0 | 50.0 | app6 | ok | 33 | 41667ms | 56333ms | 59633ms |
| 50.0 | 60.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 166 | 18227ms | 27645ms | 29765ms |
| 60.0 | 70.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 165 | 4058ms | 9812ms | 27800ms |
| 70.0 | 80.0 | app2 | ok | 1 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 255 | 3313ms | 4663ms | 4966ms |
| 80.0 | 90.0 | app2 | ok | 2 | 45000ms | 57000ms | 59700ms |
| 80.0 | 90.0 | app3 | ok | 2 | 45000ms | 57000ms | 59700ms |
| 80.0 | 90.0 | app4 | ok | 2 | 45000ms | 57000ms | 59700ms |
| 80.0 | 90.0 | app5 | ok | 2 | 45000ms | 57000ms | 59700ms |
| 80.0 | 90.0 | app6 | ok | 2 | 45000ms | 57000ms | 59700ms |
| 90.0 | 100.0 | app1 | ok | 153 | 3454ms | 5974ms | 9597ms |
| 90.0 | 100.0 | app2 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 90.0 | 100.0 | app3 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 90.0 | 100.0 | app4 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 90.0 | 100.0 | app5 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 90.0 | 100.0 | app6 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 100.0 | 110.0 | app1 | ok | 246 | 3961ms | 7490ms | 9749ms |
| 100.0 | 110.0 | app2 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 100.0 | 110.0 | app3 | ok | 6 | 45000ms | 57000ms | 59700ms |
| 100.0 | 110.0 | app4 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 100.0 | 110.0 | app5 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 100.0 | 110.0 | app6 | ok | 6 | 45000ms | 57000ms | 59700ms |
| 110.0 | 120.0 | app1 | ok | 164 | 3905ms | 6273ms | 9627ms |
| 110.0 | 120.0 | app2 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 110.0 | 120.0 | app3 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 110.0 | 120.0 | app4 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 110.0 | 120.0 | app5 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 110.0 | 120.0 | app6 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 120.0 | 131.0 | app1 | ok | 223 | 3647ms | 8110ms | 9811ms |
| 120.0 | 131.0 | app2 | ok | 5 | 55000ms | 60000ms | 60000ms |
| 120.0 | 131.0 | app3 | ok | 5 | 48750ms | 60000ms | 60000ms |
| 120.0 | 131.0 | app4 | ok | 5 | 55000ms | 60000ms | 60000ms |
| 120.0 | 131.0 | app5 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 120.0 | 131.0 | app6 | ok | 5 | 55000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | app1 | ok | 130 | 3881ms | 6389ms | 9639ms |
| 131.0 | 141.0 | app2 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | app3 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | app4 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | app5 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | app6 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | app1 | ok | 231 | 3777ms | 5558ms | 9556ms |
| 141.0 | 151.0 | app2 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | app3 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | app4 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | app5 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | app6 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 151.0 | 161.0 | app1 | ok | 219 | 3725ms | 6779ms | 9678ms |
| 151.0 | 161.0 | app2 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 151.0 | 161.0 | app3 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 151.0 | 161.0 | app4 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 151.0 | 161.0 | app5 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 151.0 | 161.0 | app6 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 161.0 | 171.0 | app1 | ok | 150 | 4000ms | 7000ms | 9700ms |
| 161.0 | 171.0 | app2 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 161.0 | 171.0 | app3 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 161.0 | 171.0 | app4 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 161.0 | 171.0 | app5 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 161.0 | 171.0 | app6 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 171.0 | 181.0 | app1 | ok | 228 | 3947ms | 6323ms | 9632ms |
| 171.0 | 181.0 | app2 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 171.0 | 181.0 | app3 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 171.0 | 181.0 | app4 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 171.0 | 181.0 | app5 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 171.0 | 181.0 | app6 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | app1 | ok | 234 | 3874ms | 6226ms | 9623ms |
| 181.0 | 191.0 | app2 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | app3 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | app4 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | app5 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | app6 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | app1 | ok | 193 | 3708ms | 4995ms | 9492ms |
| 191.0 | 201.0 | app2 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | app3 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | app4 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | app5 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | app6 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 201.0 | 211.0 | app1 | ok | 202 | 3922ms | 6115ms | 9612ms |
| 201.0 | 211.0 | app2 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 201.0 | 211.0 | app3 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 201.0 | 211.0 | app4 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 201.0 | 211.0 | app5 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 201.0 | 211.0 | app6 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | app1 | ok | 166 | 3862ms | 6227ms | 9623ms |
| 211.0 | 221.0 | app2 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | app3 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | app4 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | app5 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | app6 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | app1 | ok | 190 | 3775ms | 5476ms | 9548ms |
| 221.0 | 231.0 | app2 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | app3 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | app4 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | app5 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | app6 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | app1 | ok | 219 | 3802ms | 7329ms | 9733ms |
| 231.0 | 241.0 | app2 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | app3 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | app4 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | app5 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | app6 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 241.0 | 251.0 | app1 | ok | 127 | 4041ms | 7354ms | 9735ms |
| 241.0 | 251.0 | app2 | ok | 21 | 50357ms | 60000ms | 60000ms |
| 241.0 | 251.0 | app3 | ok | 22 | 49286ms | 60000ms | 60000ms |
| 241.0 | 251.0 | app4 | ok | 21 | 47308ms | 60000ms | 60000ms |
| 241.0 | 251.0 | app5 | ok | 21 | 48214ms | 60000ms | 60000ms |
| 241.0 | 251.0 | app6 | ok | 22 | 50769ms | 60000ms | 60000ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 9 | 21250ms | 33000ms | 57300ms |
| 251.0 | 261.0 | app3 | ok | 9 | 21250ms | 33000ms | 57300ms |
| 251.0 | 261.0 | app4 | ok | 10 | 21111ms | 30000ms | 57000ms |
| 251.0 | 261.0 | app5 | ok | 9 | 21250ms | 33000ms | 57300ms |
| 251.0 | 261.0 | app6 | ok | 9 | 21250ms | 33000ms | 57300ms |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 352.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 352.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 352.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 352.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 352.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 352.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 535.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 535.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 535.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 535.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 535.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 535.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app4 exceeded the 10% ledger tolerance: cost -12.0%
- app6 exceeded the 10% ledger tolerance: cost -10.1%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 5705970 | 284238 | 5990208.0 | 0.0% | 6148834.0 | 6274446.0 | -2.0% | True |
| app2 | 183270 | 9109 | 192379.0 | 0.0% | 183944.0 | 201488.0 | -8.7% | True |
| app3 | 183270 | 9178 | 192448.0 | 0.0% | 188058.0 | 201626.0 | -6.7% | True |
| app4 | 184500 | 9129 | 193629.0 | 0.0% | 178420.0 | 202758.0 | -12.0% | False |
| app5 | 183270 | 9111 | 192381.0 | 0.0% | 182522.0 | 201492.0 | -9.4% | True |
| app6 | 183270 | 9184 | 192454.0 | 0.0% | 181322.0 | 201638.0 | -10.1% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 4642 | 0 | 0 | 0 (never shed) | 0.00% | 90.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 149 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 149 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |
| app4 | 150 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |
| app5 | 149 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |
| app6 | 149 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5388). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5388 | 0.051ms | 0.107ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 502380 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 4639 | 8928ms | 14763ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 149 | 55793ms | 112905ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app3 | ok | 149 | 55338ms | 112905ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app4 | ok | 150 | 55610ms | 112857ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app5 | ok | 149 | 55427ms | 112790ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app6 | ok | 149 | 55536ms | 112790ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5385 | 9249ms | 68387ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (54 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 1667ms | 2966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 750ms | 3850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app3 | ok | 750ms | 1462ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app4 | ok | 733ms | 3800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app5 | ok | 800ms | 3800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app6 | ok | 1000ms | 3800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 8439ms | 14128ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 5167ms | 7300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app3 | ok | 4833ms | 5875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app4 | ok | 6667ms | 7867ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app5 | ok | 5625ms | 7650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app6 | ok | 5833ms | 7775ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 10023ms | 14502ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 16250ms | 19625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app3 | ok | 18750ms | 28500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app4 | ok | 20000ms | 29000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app5 | ok | 18750ms | 28500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app6 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 8248ms | 9869ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 27500ms | 42750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app3 | ok | 28333ms | 43125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app4 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app5 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 8520ms | 13179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app3 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app4 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app5 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app6 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 10972ms | 14597ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 51000ms | 59100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app3 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app4 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app5 | ok | 50000ms | 59000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app6 | ok | 50625ms | 59062ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 19000ms | 28667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 51375ms | 59137ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app3 | ok | 50294ms | 59029ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app4 | ok | 51786ms | 59179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app5 | ok | 51786ms | 59179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app6 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 22168ms | 29217ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app3 | ok | 26667ms | 42000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app4 | ok | 33750ms | 43875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app5 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 8034ms | 13620ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 8415ms | 9841ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 40000ms | 57000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app3 | ok | 40000ms | 57000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app4 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app5 | ok | 40000ms | 57000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app6 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 9324ms | 14338ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 45000ms | 58500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app3 | ok | 45000ms | 58500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app4 | ok | 50000ms | 59000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app5 | ok | 47500ms | 58750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app6 | ok | 45000ms | 58500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 8804ms | 13718ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app3 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app4 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app5 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app6 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 131.0 | app1 | ok | 8975ms | 13229ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 131.0 | app2 | ok | 80000ms | 116000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 131.0 | app3 | ok | 75000ms | 115500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 131.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 131.0 | app5 | ok | 75000ms | 115500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 131.0 | app6 | ok | 60000ms | 114000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 10000ms | 14500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 8782ms | 13948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 8906ms | 13917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 9116ms | 14203ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 8899ms | 13750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 8850ms | 13622ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 8692ms | 12793ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 8812ms | 13768ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 8702ms | 13908ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 8731ms | 14261ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 9000ms | 14217ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 8873ms | 13152ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 11711ms | 14671ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 45000ms | 106000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app3 | ok | 46071ms | 109125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app4 | ok | 43750ms | 105500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app5 | ok | 45938ms | 107571ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app6 | ok | 45000ms | 106000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 352.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 352.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 352.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 352.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 352.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 352.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 535.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 535.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 535.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 535.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 535.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 535.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
