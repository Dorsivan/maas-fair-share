# Fairness benchmark: six-group-board-case (uni310-l2-r1-uni165-pow2)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 24.2 points

## Run metadata

| field | value |
|---|---|
| Scenario | `six-group-board-case` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-8577fbc9fb-lx2ch` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T03:27:49Z` |
| Run end | `2026-11-26T03:34:58Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 44 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/44 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 77.50 | 2.4219 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 32.0 | 58 | 2624 | 000=1, 200=2623 | 5.0 | 7.9 | 3510992.0 | 50.8% | 26.6% | -24.2 | 48.1% | -2.7 | 47.8% | -3.0 | 80.8s | 98.9% | 2624.0 |
| app2 | 16.0 | 32 | 1324 | 200=1324 | 5.7 | 8.1 | 1767552.0 | 25.4% | 14.7% | -10.7 | 24.2% | -1.2 | 24.1% | -1.3 | 81.0s | 98.9% | 1324.0 |
| app3 | 8.0 | 32 | 751 | 200=751 | 10.6 | 14.2 | 996292.0 | 12.7% | 14.7% | 2.0 | 13.7% | 1.0 | 13.7% | 1.0 | 82.0s | 98.9% | 751.0 |
| app4 | 4.0 | 32 | 426 | 200=426 | 19.1 | 25.9 | 561368.0 | 6.3% | 14.7% | 8.3 | 7.7% | 1.3 | 7.8% | 1.4 | 82.3s | 98.9% | 426.0 |
| app5 | 2.0 | 32 | 232 | 200=232 | 35.5 | 54.7 | 294714.0 | 3.2% | 14.7% | 11.5 | 4.0% | 0.9 | 4.2% | 1.1 | 83.4s | 98.9% | 232.0 |
| app6 | 1.0 | 32 | 133 | 200=133 | 58.9 | 97.8 | 163672.0 | 1.6% | 14.7% | 13.1 | 2.2% | 0.7 | 2.4% | 0.8 | 83.4s | 98.9% | 133.0 |
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
| 0.0 | 211.0 | 211.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (43 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 36458.0 | 50.8% | 77.1% | 26.3 |
| 0.0 | 10.0 | app2 | True | False | 10812.0 | 25.4% | 22.9% | -2.5 |
| 0.0 | 10.0 | app3 | True | False | 0.0 | 12.7% | 0.0% | -12.7 |
| 0.0 | 10.0 | app4 | True | False | 0.0 | 6.3% | 0.0% | -6.3 |
| 0.0 | 10.0 | app5 | True | False | 0.0 | 3.2% | 0.0% | -3.2 |
| 0.0 | 10.0 | app6 | True | False | 0.0 | 1.6% | 0.0% | -1.6 |
| 10.0 | 20.0 | app1 | True | False | 155504.0 | 50.8% | 51.6% | 0.8 |
| 10.0 | 20.0 | app2 | True | False | 85250.0 | 25.4% | 28.3% | 2.9 |
| 10.0 | 20.0 | app3 | True | False | 44560.0 | 12.7% | 14.8% | 2.1 |
| 10.0 | 20.0 | app4 | True | False | 16218.0 | 6.3% | 5.4% | -1.0 |
| 10.0 | 20.0 | app5 | True | False | 0.0 | 3.2% | 0.0% | -3.2 |
| 10.0 | 20.0 | app6 | True | False | 0.0 | 1.6% | 0.0% | -1.6 |
| 20.0 | 30.0 | app1 | True | False | 157006.0 | 50.8% | 51.8% | 1.0 |
| 20.0 | 30.0 | app2 | True | False | 73008.0 | 25.4% | 24.1% | -1.3 |
| 20.0 | 30.0 | app3 | True | False | 40556.0 | 12.7% | 13.4% | 0.7 |
| 20.0 | 30.0 | app4 | True | False | 24386.0 | 6.3% | 8.0% | 1.7 |
| 20.0 | 30.0 | app5 | True | False | 8142.0 | 3.2% | 2.7% | -0.5 |
| 20.0 | 30.0 | app6 | True | False | 0.0 | 1.6% | 0.0% | -1.6 |
| 30.0 | 40.0 | app1 | True | False | 169104.0 | 50.8% | 55.3% | 4.5 |
| 30.0 | 40.0 | app2 | True | False | 82570.0 | 25.4% | 27.0% | 1.6 |
| 30.0 | 40.0 | app3 | True | False | 32434.0 | 12.7% | 10.6% | -2.1 |
| 30.0 | 40.0 | app4 | True | False | 12192.0 | 6.3% | 4.0% | -2.4 |
| 30.0 | 40.0 | app5 | True | False | 6764.0 | 3.2% | 2.2% | -1.0 |
| 30.0 | 40.0 | app6 | True | False | 2716.0 | 1.6% | 0.9% | -0.7 |
| 40.0 | 50.0 | app1 | True | False | 116238.0 | 50.8% | 44.5% | -6.3 |
| 40.0 | 50.0 | app2 | True | False | 63574.0 | 25.4% | 24.4% | -1.0 |
| 40.0 | 50.0 | app3 | True | False | 43366.0 | 12.7% | 16.6% | 3.9 |
| 40.0 | 50.0 | app4 | True | False | 23018.0 | 6.3% | 8.8% | 2.5 |
| 40.0 | 50.0 | app5 | True | False | 10776.0 | 3.2% | 4.1% | 1.0 |
| 40.0 | 50.0 | app6 | True | False | 4074.0 | 1.6% | 1.6% | -0.0 |
| 50.0 | 60.0 | app1 | True | False | 147456.0 | 50.8% | 47.8% | -3.0 |
| 50.0 | 60.0 | app2 | True | False | 74324.0 | 25.4% | 24.1% | -1.3 |
| 50.0 | 60.0 | app3 | True | False | 28416.0 | 12.7% | 9.2% | -3.5 |
| 50.0 | 60.0 | app4 | True | False | 25648.0 | 6.3% | 8.3% | 2.0 |
| 50.0 | 60.0 | app5 | True | False | 21676.0 | 3.2% | 7.0% | 3.9 |
| 50.0 | 60.0 | app6 | True | False | 10820.0 | 1.6% | 3.5% | 1.9 |
| 60.0 | 70.0 | app1 | True | False | 172988.0 | 50.8% | 55.9% | 5.1 |
| 60.0 | 70.0 | app2 | True | False | 87984.0 | 25.4% | 28.4% | 3.0 |
| 60.0 | 70.0 | app3 | True | False | 43286.0 | 12.7% | 14.0% | 1.3 |
| 60.0 | 70.0 | app4 | True | False | 5382.0 | 6.3% | 1.7% | -4.6 |
| 60.0 | 70.0 | app5 | True | False | 0.0 | 3.2% | 0.0% | -3.2 |
| 60.0 | 70.0 | app6 | True | False | 0.0 | 1.6% | 0.0% | -1.6 |
| 70.0 | 80.0 | app1 | True | False | 159706.0 | 50.8% | 52.7% | 1.9 |
| 70.0 | 80.0 | app2 | True | False | 79746.0 | 25.4% | 26.3% | 0.9 |
| 70.0 | 80.0 | app3 | True | False | 39212.0 | 12.7% | 12.9% | 0.2 |
| 70.0 | 80.0 | app4 | True | False | 22980.0 | 6.3% | 7.6% | 1.2 |
| 70.0 | 80.0 | app5 | True | False | 1342.0 | 3.2% | 0.4% | -2.7 |
| 70.0 | 80.0 | app6 | True | False | 0.0 | 1.6% | 0.0% | -1.6 |
| 80.0 | 90.0 | app1 | True | False | 152804.0 | 50.8% | 49.8% | -1.0 |
| 80.0 | 90.0 | app2 | True | False | 74354.0 | 25.4% | 24.2% | -1.2 |
| 80.0 | 90.0 | app3 | True | False | 37810.0 | 12.7% | 12.3% | -0.4 |
| 80.0 | 90.0 | app4 | True | False | 20318.0 | 6.3% | 6.6% | 0.3 |
| 80.0 | 90.0 | app5 | True | False | 14852.0 | 3.2% | 4.8% | 1.7 |
| 80.0 | 90.0 | app6 | True | False | 6754.0 | 1.6% | 2.2% | 0.6 |
| 90.0 | 100.0 | app1 | True | False | 154098.0 | 50.8% | 50.0% | -0.8 |
| 90.0 | 100.0 | app2 | True | False | 75862.0 | 25.4% | 24.6% | -0.8 |
| 90.0 | 100.0 | app3 | True | False | 40552.0 | 12.7% | 13.1% | 0.4 |
| 90.0 | 100.0 | app4 | True | False | 20326.0 | 6.3% | 6.6% | 0.2 |
| 90.0 | 100.0 | app5 | True | False | 10850.0 | 3.2% | 3.5% | 0.3 |
| 90.0 | 100.0 | app6 | True | False | 6766.0 | 1.6% | 2.2% | 0.6 |
| 100.0 | 111.0 | app1 | True | False | 158334.0 | 50.8% | 52.0% | 1.3 |
| 100.0 | 111.0 | app2 | True | False | 76998.0 | 25.4% | 25.3% | -0.1 |
| 100.0 | 111.0 | app3 | True | False | 37800.0 | 12.7% | 12.4% | -0.3 |
| 100.0 | 111.0 | app4 | True | False | 18914.0 | 6.3% | 6.2% | -0.1 |
| 100.0 | 111.0 | app5 | True | False | 8114.0 | 3.2% | 2.7% | -0.5 |
| 100.0 | 111.0 | app6 | True | False | 4056.0 | 1.6% | 1.3% | -0.3 |
| 111.0 | 121.0 | app1 | True | False | 143404.0 | 50.8% | 47.0% | -3.8 |
| 111.0 | 121.0 | app2 | True | False | 74214.0 | 25.4% | 24.3% | -1.1 |
| 111.0 | 121.0 | app3 | True | False | 47344.0 | 12.7% | 15.5% | 2.8 |
| 111.0 | 121.0 | app4 | True | False | 22958.0 | 6.3% | 7.5% | 1.2 |
| 111.0 | 121.0 | app5 | True | False | 12092.0 | 3.2% | 4.0% | 0.8 |
| 111.0 | 121.0 | app6 | True | False | 5410.0 | 1.6% | 1.8% | 0.2 |
| 121.0 | 131.0 | app1 | True | False | 156954.0 | 50.8% | 51.6% | 0.8 |
| 121.0 | 131.0 | app2 | True | False | 82420.0 | 25.4% | 27.1% | 1.7 |
| 121.0 | 131.0 | app3 | True | False | 35136.0 | 12.7% | 11.5% | -1.1 |
| 121.0 | 131.0 | app4 | True | False | 16176.0 | 6.3% | 5.3% | -1.0 |
| 121.0 | 131.0 | app5 | True | False | 8122.0 | 3.2% | 2.7% | -0.5 |
| 121.0 | 131.0 | app6 | True | False | 5432.0 | 1.6% | 1.8% | 0.2 |
| 131.0 | 141.0 | app1 | True | False | 132518.0 | 50.8% | 46.7% | -4.1 |
| 131.0 | 141.0 | app2 | True | False | 67694.0 | 25.4% | 23.8% | -1.6 |
| 131.0 | 141.0 | app3 | True | False | 43168.0 | 12.7% | 15.2% | 2.5 |
| 131.0 | 141.0 | app4 | True | False | 22992.0 | 6.3% | 8.1% | 1.7 |
| 131.0 | 141.0 | app5 | True | False | 12172.0 | 3.2% | 4.3% | 1.1 |
| 131.0 | 141.0 | app6 | True | False | 5432.0 | 1.6% | 1.9% | 0.3 |
| 141.0 | 151.0 | app1 | True | False | 101438.0 | 50.8% | 37.0% | -13.8 |
| 141.0 | 151.0 | app2 | True | False | 47254.0 | 25.4% | 17.2% | -8.2 |
| 141.0 | 151.0 | app3 | True | False | 33812.0 | 12.7% | 12.3% | -0.4 |
| 141.0 | 151.0 | app4 | True | False | 28354.0 | 6.3% | 10.3% | 4.0 |
| 141.0 | 151.0 | app5 | True | False | 35102.0 | 3.2% | 12.8% | 9.6 |
| 141.0 | 151.0 | app6 | True | False | 28446.0 | 1.6% | 10.4% | 8.8 |
| 151.0 | 161.0 | app1 | True | False | 131192.0 | 50.8% | 44.1% | -6.7 |
| 151.0 | 161.0 | app2 | True | False | 70324.0 | 25.4% | 23.6% | -1.8 |
| 151.0 | 161.0 | app3 | True | False | 41890.0 | 12.7% | 14.1% | 1.4 |
| 151.0 | 161.0 | app4 | True | False | 41910.0 | 6.3% | 14.1% | 7.7 |
| 151.0 | 161.0 | app5 | True | False | 1358.0 | 3.2% | 0.5% | -2.7 |
| 151.0 | 161.0 | app6 | True | False | 10828.0 | 1.6% | 3.6% | 2.1 |
| 161.0 | 171.0 | app1 | True | False | 152758.0 | 50.8% | 49.3% | -1.5 |
| 161.0 | 171.0 | app2 | True | False | 71686.0 | 25.4% | 23.1% | -2.3 |
| 161.0 | 171.0 | app3 | True | False | 55520.0 | 12.7% | 17.9% | 5.2 |
| 161.0 | 171.0 | app4 | True | False | 20302.0 | 6.3% | 6.6% | 0.2 |
| 161.0 | 171.0 | app5 | True | False | 9506.0 | 3.2% | 3.1% | -0.1 |
| 161.0 | 171.0 | app6 | True | False | 0.0 | 1.6% | 0.0% | -1.6 |
| 171.0 | 181.0 | app1 | True | False | 151370.0 | 50.8% | 49.5% | -1.3 |
| 171.0 | 181.0 | app2 | True | False | 83900.0 | 25.4% | 27.5% | 2.1 |
| 171.0 | 181.0 | app3 | True | False | 47292.0 | 12.7% | 15.5% | 2.8 |
| 171.0 | 181.0 | app4 | True | False | 17564.0 | 6.3% | 5.7% | -0.6 |
| 171.0 | 181.0 | app5 | True | False | 5426.0 | 3.2% | 1.8% | -1.4 |
| 171.0 | 181.0 | app6 | True | False | 0.0 | 1.6% | 0.0% | -1.6 |
| 181.0 | 191.0 | app1 | True | False | 160966.0 | 50.8% | 52.7% | 1.9 |
| 181.0 | 191.0 | app2 | True | False | 74314.0 | 25.4% | 24.3% | -1.1 |
| 181.0 | 191.0 | app3 | True | False | 39226.0 | 12.7% | 12.8% | 0.1 |
| 181.0 | 191.0 | app4 | True | False | 18930.0 | 6.3% | 6.2% | -0.2 |
| 181.0 | 191.0 | app5 | True | False | 12132.0 | 3.2% | 4.0% | 0.8 |
| 181.0 | 191.0 | app6 | True | False | 0.0 | 1.6% | 0.0% | -1.6 |
| 191.0 | 201.0 | app1 | True | False | 148690.0 | 50.8% | 50.0% | -0.8 |
| 191.0 | 201.0 | app2 | True | False | 78528.0 | 25.4% | 26.4% | 1.0 |
| 191.0 | 201.0 | app3 | True | False | 39152.0 | 12.7% | 13.2% | 0.5 |
| 191.0 | 201.0 | app4 | True | False | 20340.0 | 6.3% | 6.8% | 0.5 |
| 191.0 | 201.0 | app5 | True | False | 9486.0 | 3.2% | 3.2% | 0.0 |
| 191.0 | 201.0 | app6 | True | False | 1358.0 | 1.6% | 0.5% | -1.1 |
| 201.0 | 211.0 | app1 | True | False | 112290.0 | 50.8% | 36.4% | -14.4 |
| 201.0 | 211.0 | app2 | True | False | 56746.0 | 25.4% | 18.4% | -7.0 |
| 201.0 | 211.0 | app3 | True | False | 48740.0 | 12.7% | 15.8% | 3.1 |
| 201.0 | 211.0 | app4 | True | False | 37890.0 | 6.3% | 12.3% | 5.9 |
| 201.0 | 211.0 | app5 | True | False | 37792.0 | 3.2% | 12.3% | 9.1 |
| 201.0 | 211.0 | app6 | True | False | 14854.0 | 1.6% | 4.8% | 3.2 |
| 211.0 | 221.0 | app1 | True | False | 127124.0 | 50.8% | 42.7% | -8.1 |
| 211.0 | 221.0 | app2 | True | False | 66244.0 | 25.4% | 22.3% | -3.1 |
| 211.0 | 221.0 | app3 | True | False | 54066.0 | 12.7% | 18.2% | 5.5 |
| 211.0 | 221.0 | app4 | True | False | 40632.0 | 6.3% | 13.7% | 7.3 |
| 211.0 | 221.0 | app5 | True | False | 5404.0 | 3.2% | 1.8% | -1.4 |
| 211.0 | 221.0 | app6 | True | False | 4038.0 | 1.6% | 1.4% | -0.2 |
| 221.0 | 231.0 | app1 | True | False | 155448.0 | 50.8% | 50.6% | -0.1 |
| 221.0 | 231.0 | app2 | True | False | 78492.0 | 25.4% | 25.6% | 0.2 |
| 221.0 | 231.0 | app3 | True | False | 40536.0 | 12.7% | 13.2% | 0.5 |
| 221.0 | 231.0 | app4 | True | False | 18912.0 | 6.3% | 6.2% | -0.2 |
| 221.0 | 231.0 | app5 | True | False | 9468.0 | 3.2% | 3.1% | -0.1 |
| 221.0 | 231.0 | app6 | True | False | 4064.0 | 1.6% | 1.3% | -0.3 |
| 231.0 | 241.0 | app1 | True | False | 157060.0 | 50.8% | 51.8% | 1.0 |
| 231.0 | 241.0 | app2 | True | False | 75686.0 | 25.4% | 25.0% | -0.4 |
| 231.0 | 241.0 | app3 | True | False | 33792.0 | 12.7% | 11.1% | -1.5 |
| 231.0 | 241.0 | app4 | True | False | 21696.0 | 6.3% | 7.2% | 0.8 |
| 231.0 | 241.0 | app5 | True | False | 9444.0 | 3.2% | 3.1% | -0.1 |
| 231.0 | 241.0 | app6 | True | False | 5396.0 | 1.6% | 1.8% | 0.2 |
| 241.0 | 251.0 | app1 | False | n/a | 100084.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 55568.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | n/a | 48626.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app4 | False | n/a | 41972.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app5 | False | n/a | 31140.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app6 | False | n/a | 24306.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | False | n/a | 1358.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | False | n/a | 13554.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | False | n/a | 18922.0 | n/a | n/a | n/a |
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
| 331.0 | 342.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 342.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 342.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 342.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 342.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 342.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
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
| 422.0 | 429.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 429.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 429.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 429.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 429.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 429.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 99 | 225ms | 2750ms | 4775ms |
| 0.0 | 10.0 | app2 | ok | 52 | 175ms | 2275ms | 4675ms |
| 0.0 | 10.0 | app3 | ok | 43 | 288ms | 3208ms | 4821ms |
| 0.0 | 10.0 | app4 | ok | 23 | 275ms | 4179ms | 4918ms |
| 0.0 | 10.0 | app5 | ok | 14 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app6 | ok | 12 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 108 | 1492ms | 2545ms | 4755ms |
| 10.0 | 20.0 | app2 | ok | 55 | 1375ms | 3281ms | 4828ms |
| 10.0 | 20.0 | app3 | ok | 26 | 1600ms | 4071ms | 4907ms |
| 10.0 | 20.0 | app4 | ok | 14 | 8500ms | 23000ms | 29300ms |
| 10.0 | 20.0 | app5 | ok | 5 | 13333ms | 26667ms | 29667ms |
| 10.0 | 20.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 130 | 1380ms | 2479ms | 4729ms |
| 20.0 | 30.0 | app2 | ok | 65 | 1469ms | 2444ms | 4675ms |
| 20.0 | 30.0 | app3 | ok | 36 | 3214ms | 7750ms | 9775ms |
| 20.0 | 30.0 | app4 | ok | 17 | 17857ms | 27571ms | 29757ms |
| 20.0 | 30.0 | app5 | ok | 9 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app6 | ok | 1 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | app1 | ok | 113 | 1536ms | 3234ms | 4823ms |
| 30.0 | 40.0 | app2 | ok | 56 | 1462ms | 3600ms | 4860ms |
| 30.0 | 40.0 | app3 | ok | 22 | 2500ms | 4944ms | 9450ms |
| 30.0 | 40.0 | app4 | ok | 13 | 19167ms | 27833ms | 29783ms |
| 30.0 | 40.0 | app5 | ok | 5 | 22500ms | 45000ms | 58500ms |
| 30.0 | 40.0 | app6 | ok | 4 | 40000ms | 56000ms | 59600ms |
| 40.0 | 50.0 | app1 | ok | 95 | 2792ms | 7738ms | 9774ms |
| 40.0 | 50.0 | app2 | ok | 49 | 2566ms | 5917ms | 9592ms |
| 40.0 | 50.0 | app3 | ok | 30 | 3036ms | 6250ms | 9625ms |
| 40.0 | 50.0 | app4 | ok | 29 | 4583ms | 20333ms | 29033ms |
| 40.0 | 50.0 | app5 | ok | 24 | 26000ms | 52000ms | 59200ms |
| 40.0 | 50.0 | app6 | ok | 12 | 45000ms | 57000ms | 59700ms |
| 50.0 | 60.0 | app1 | ok | 110 | 1573ms | 3690ms | 4869ms |
| 50.0 | 60.0 | app2 | ok | 54 | 1600ms | 4100ms | 4910ms |
| 50.0 | 60.0 | app3 | ok | 21 | 3906ms | 8500ms | 9850ms |
| 50.0 | 60.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 117 | 1176ms | 2273ms | 3537ms |
| 60.0 | 70.0 | app2 | ok | 61 | 1199ms | 2275ms | 3475ms |
| 60.0 | 70.0 | app3 | ok | 27 | 4485ms | 8650ms | 9865ms |
| 60.0 | 70.0 | app4 | ok | 6 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 124 | 1258ms | 2420ms | 4656ms |
| 70.0 | 80.0 | app2 | ok | 62 | 1364ms | 2491ms | 4742ms |
| 70.0 | 80.0 | app3 | ok | 29 | 4312ms | 8389ms | 9839ms |
| 70.0 | 80.0 | app4 | ok | 15 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app5 | ok | 1 | 45000ms | 57000ms | 59700ms |
| 70.0 | 80.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 95 | 1345ms | 2485ms | 4736ms |
| 80.0 | 90.0 | app2 | ok | 46 | 1288ms | 2350ms | 4425ms |
| 80.0 | 90.0 | app3 | ok | 27 | 3688ms | 5500ms | 9550ms |
| 80.0 | 90.0 | app4 | ok | 14 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app5 | ok | 7 | 45000ms | 57000ms | 59700ms |
| 80.0 | 90.0 | app6 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 90.0 | 100.0 | app1 | ok | 117 | 1239ms | 2302ms | 4025ms |
| 90.0 | 100.0 | app2 | ok | 58 | 1364ms | 2418ms | 4638ms |
| 90.0 | 100.0 | app3 | ok | 28 | 3846ms | 4923ms | 9300ms |
| 90.0 | 100.0 | app4 | ok | 14 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app5 | ok | 8 | 45000ms | 57000ms | 59700ms |
| 90.0 | 100.0 | app6 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 100.0 | 111.0 | app1 | ok | 132 | 1271ms | 2371ms | 4529ms |
| 100.0 | 111.0 | app2 | ok | 65 | 1421ms | 2372ms | 4458ms |
| 100.0 | 111.0 | app3 | ok | 28 | 3889ms | 7667ms | 9767ms |
| 100.0 | 111.0 | app4 | ok | 14 | 20000ms | 28000ms | 29800ms |
| 100.0 | 111.0 | app5 | ok | 7 | 45000ms | 57000ms | 59700ms |
| 100.0 | 111.0 | app6 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 111.0 | 121.0 | app1 | ok | 102 | 1233ms | 3038ms | 4804ms |
| 111.0 | 121.0 | app2 | ok | 55 | 1575ms | 3472ms | 4847ms |
| 111.0 | 121.0 | app3 | ok | 37 | 3015ms | 6300ms | 9630ms |
| 111.0 | 121.0 | app4 | ok | 18 | 19412ms | 27882ms | 29788ms |
| 111.0 | 121.0 | app5 | ok | 9 | 40714ms | 56143ms | 59614ms |
| 111.0 | 121.0 | app6 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 121.0 | 131.0 | app1 | ok | 105 | 1439ms | 3250ms | 4825ms |
| 121.0 | 131.0 | app2 | ok | 52 | 1288ms | 2488ms | 4740ms |
| 121.0 | 131.0 | app3 | ok | 28 | 3056ms | 4611ms | 4961ms |
| 121.0 | 131.0 | app4 | ok | 18 | 12000ms | 26400ms | 29640ms |
| 121.0 | 131.0 | app5 | ok | 8 | 40000ms | 56000ms | 59600ms |
| 121.0 | 131.0 | app6 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | app1 | ok | 68 | 1375ms | 2571ms | 4757ms |
| 131.0 | 141.0 | app2 | ok | 33 | 1375ms | 3625ms | 4863ms |
| 131.0 | 141.0 | app3 | ok | 23 | 2604ms | 4521ms | 4952ms |
| 131.0 | 141.0 | app4 | ok | 23 | 7188ms | 23429ms | 29343ms |
| 131.0 | 141.0 | app5 | ok | 28 | 18571ms | 46000ms | 58600ms |
| 131.0 | 141.0 | app6 | ok | 30 | 40909ms | 60000ms | 60000ms |
| 141.0 | 151.0 | app1 | ok | 116 | 3125ms | 8432ms | 9843ms |
| 141.0 | 151.0 | app2 | ok | 59 | 3417ms | 8525ms | 9852ms |
| 141.0 | 151.0 | app3 | ok | 44 | 4167ms | 8625ms | 9862ms |
| 141.0 | 151.0 | app4 | ok | 30 | 8684ms | 24000ms | 29400ms |
| 141.0 | 151.0 | app5 | ok | 1 | 20000ms | 28000ms | 29800ms |
| 141.0 | 151.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 101 | 1806ms | 4211ms | 4921ms |
| 151.0 | 161.0 | app2 | ok | 50 | 1692ms | 3864ms | 4886ms |
| 151.0 | 161.0 | app3 | ok | 32 | 3056ms | 4833ms | 9200ms |
| 151.0 | 161.0 | app4 | ok | 7 | 7500ms | 23000ms | 29300ms |
| 151.0 | 161.0 | app5 | ok | 3 | 20000ms | 28000ms | 29800ms |
| 151.0 | 161.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 120 | 1413ms | 2457ms | 4700ms |
| 161.0 | 171.0 | app2 | ok | 62 | 1234ms | 2397ms | 4613ms |
| 161.0 | 171.0 | app3 | ok | 35 | 2066ms | 4271ms | 4927ms |
| 161.0 | 171.0 | app4 | ok | 17 | 4271ms | 21500ms | 29150ms |
| 161.0 | 171.0 | app5 | ok | 8 | 20000ms | 28000ms | 29800ms |
| 161.0 | 171.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 91 | 1286ms | 2279ms | 2725ms |
| 171.0 | 181.0 | app2 | ok | 43 | 946ms | 2239ms | 3925ms |
| 171.0 | 181.0 | app3 | ok | 31 | 1911ms | 4225ms | 4922ms |
| 171.0 | 181.0 | app4 | ok | 15 | 19286ms | 27857ms | 29786ms |
| 171.0 | 181.0 | app5 | ok | 8 | 36000ms | 55200ms | 59520ms |
| 171.0 | 181.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 128 | 1358ms | 2538ms | 4754ms |
| 181.0 | 191.0 | app2 | ok | 65 | 1581ms | 2969ms | 4797ms |
| 181.0 | 191.0 | app3 | ok | 29 | 2250ms | 4442ms | 4944ms |
| 181.0 | 191.0 | app4 | ok | 15 | 20000ms | 28000ms | 29800ms |
| 181.0 | 191.0 | app5 | ok | 7 | 45000ms | 57000ms | 59700ms |
| 181.0 | 191.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 99 | 1559ms | 3763ms | 4876ms |
| 191.0 | 201.0 | app2 | ok | 52 | 1312ms | 3143ms | 4814ms |
| 191.0 | 201.0 | app3 | ok | 32 | 1794ms | 4500ms | 9200ms |
| 191.0 | 201.0 | app4 | ok | 32 | 9167ms | 25429ms | 29543ms |
| 191.0 | 201.0 | app5 | ok | 30 | 21765ms | 48750ms | 58875ms |
| 191.0 | 201.0 | app6 | ok | 12 | 46364ms | 59455ms | 60000ms |
| 201.0 | 211.0 | app1 | ok | 82 | 2959ms | 4633ms | 5900ms |
| 201.0 | 211.0 | app2 | ok | 45 | 2933ms | 4663ms | 7750ms |
| 201.0 | 211.0 | app3 | ok | 30 | 2050ms | 4375ms | 4938ms |
| 201.0 | 211.0 | app4 | ok | 14 | 1600ms | 4125ms | 4912ms |
| 201.0 | 211.0 | app5 | ok | 2 | 7500ms | 9500ms | 9950ms |
| 201.0 | 211.0 | app6 | ok | 2 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | app1 | ok | 103 | 2043ms | 4340ms | 4934ms |
| 211.0 | 221.0 | app2 | ok | 49 | 2550ms | 4510ms | 4951ms |
| 211.0 | 221.0 | app3 | ok | 34 | 3036ms | 7167ms | 9717ms |
| 211.0 | 221.0 | app4 | ok | 32 | 4167ms | 8933ms | 9893ms |
| 211.0 | 221.0 | app5 | ok | 22 | 9583ms | 25600ms | 29560ms |
| 211.0 | 221.0 | app6 | ok | 12 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | app1 | ok | 126 | 1320ms | 2900ms | 4790ms |
| 221.0 | 231.0 | app2 | ok | 65 | 1556ms | 3750ms | 4875ms |
| 221.0 | 231.0 | app3 | ok | 46 | 5000ms | 9000ms | 9900ms |
| 221.0 | 231.0 | app4 | ok | 19 | 7500ms | 9500ms | 9950ms |
| 221.0 | 231.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 103 | 1418ms | 3161ms | 4816ms |
| 231.0 | 241.0 | app2 | ok | 53 | 1375ms | 3675ms | 4868ms |
| 231.0 | 241.0 | app3 | ok | 21 | 4844ms | 8950ms | 9895ms |
| 231.0 | 241.0 | app4 | ok | 6 | 20000ms | 28000ms | 29800ms |
| 231.0 | 241.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 40 | 1457ms | 2500ms | 4750ms |
| 241.0 | 251.0 | app2 | ok | 18 | 1300ms | 2380ms | 4550ms |
| 241.0 | 251.0 | app3 | ok | 12 | 4375ms | 8500ms | 9850ms |
| 241.0 | 251.0 | app4 | ok | 21 | 13846ms | 26769ms | 29677ms |
| 241.0 | 251.0 | app5 | ok | 26 | 24118ms | 50250ms | 59025ms |
| 241.0 | 251.0 | app6 | ok | 28 | 44000ms | 60000ms | 60000ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 331.0 | 342.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 342.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 342.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 342.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 342.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 342.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 422.0 | 429.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 429.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 429.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 429.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 429.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 429.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 3226290 | 160576 | 3386866.0 | 0.0% | 3510992.0 | 3547442.0 | -1.0% | True |
| app2 | 1628520 | 81016 | 1709536.0 | 0.0% | 1767552.0 | 1790552.0 | -1.3% | True |
| app3 | 923730 | 45750 | 969480.0 | 0.0% | 996292.0 | 1015230.0 | -1.9% | True |
| app4 | 523980 | 26095 | 550075.0 | 0.0% | 561368.0 | 576170.0 | -2.6% | True |
| app5 | 285360 | 14163 | 299523.0 | 0.0% | 294714.0 | 313686.0 | -6.0% | True |
| app6 | 163590 | 8160 | 171750.0 | 0.0% | 163672.0 | 179910.0 | -9.0% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2624 | 0 | 0 | 0 (never shed) | 0.00% | 50.8% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1324 | 0 | 0 | 0 (never shed) | 0.00% | 25.4% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 751 | 0 | 0 | 0 (never shed) | 0.00% | 12.7% | n/a (nothing shed) | n/a (nothing shed) |
| app4 | 426 | 0 | 0 | 0 (never shed) | 0.00% | 6.3% | n/a (nothing shed) | n/a (nothing shed) |
| app5 | 232 | 0 | 0 | 0 (never shed) | 0.00% | 3.2% | n/a (nothing shed) | n/a (nothing shed) |
| app6 | 133 | 0 | 0 | 0 (never shed) | 0.00% | 1.6% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5490). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5490 | 0.051ms | 0.104ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 402786 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 2623 | 4999ms | 7937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1324 | 5627ms | 8084ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app3 | ok | 751 | 10902ms | 14691ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app4 | ok | 426 | 18720ms | 29126ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app5 | ok | 232 | 33866ms | 56854ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app6 | ok | 133 | 60448ms | 114045ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5489 | 5813ms | 29343ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (43 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2136ms | 4558ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2312ms | 4375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app3 | ok | 2167ms | 4350ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app4 | ok | 3167ms | 3917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app5 | ok | 3750ms | 4887ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app6 | ok | 4300ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 4892ms | 7574ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 5375ms | 7668ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app3 | ok | 8000ms | 13300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app4 | ok | 9857ms | 14458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app5 | ok | 7000ms | 9700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app6 | ok | 8000ms | 14500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 4736ms | 7318ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 5400ms | 7640ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app3 | ok | 7667ms | 14167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app4 | ok | 18214ms | 27750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app5 | ok | 24286ms | 29429ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 4500ms | 6864ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 5214ms | 7564ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app3 | ok | 13158ms | 18800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app4 | ok | 22500ms | 29250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app5 | ok | 28333ms | 43125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app6 | ok | 35625ms | 44062ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 5500ms | 7713ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 5816ms | 7765ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app3 | ok | 12391ms | 18000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app4 | ok | 23929ms | 29393ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app5 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app6 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 5878ms | 9670ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 7033ms | 9577ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app3 | ok | 11250ms | 14625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app4 | ok | 17083ms | 28417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app5 | ok | 35455ms | 48000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app6 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 4509ms | 5854ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 4768ms | 6917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app3 | ok | 11667ms | 14667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app4 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 4742ms | 5880ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 5318ms | 7157ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app3 | ok | 10469ms | 14547ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app4 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app5 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 4883ms | 5985ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 5468ms | 7500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app3 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app4 | ok | 28125ms | 43125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app5 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 5151ms | 7050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 5667ms | 7705ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app3 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app4 | ok | 23750ms | 29375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app5 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | app1 | ok | 5142ms | 5928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | app2 | ok | 5500ms | 7562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | app3 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | app4 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | app5 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 4870ms | 6940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 5342ms | 7633ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app3 | ok | 11500ms | 14650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app4 | ok | 24333ms | 29433ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app5 | ok | 52500ms | 111000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 4767ms | 7637ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 5500ms | 7695ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app3 | ok | 10938ms | 14594ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app4 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app5 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 4875ms | 7510ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 5588ms | 7722ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app3 | ok | 10000ms | 14800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app4 | ok | 21500ms | 29150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app5 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 9579ms | 14441ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 10395ms | 14539ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app3 | ok | 11324ms | 14632ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app4 | ok | 16250ms | 26500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app5 | ok | 28000ms | 43227ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app6 | ok | 58929ms | 113700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 5256ms | 7879ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 5810ms | 12833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app3 | ok | 11771ms | 14677ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app4 | ok | 17328ms | 19733ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app5 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app6 | ok | 30000ms | 43500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 4902ms | 7610ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 6048ms | 9117ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app3 | ok | 10119ms | 14512ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app4 | ok | 12679ms | 16250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app5 | ok | 28750ms | 43250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 4905ms | 7680ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 5778ms | 7786ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app3 | ok | 8818ms | 14205ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app4 | ok | 18929ms | 28700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app5 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 4734ms | 7150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 5583ms | 7725ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app3 | ok | 9615ms | 14396ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app4 | ok | 23636ms | 29364ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app5 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 4853ms | 7421ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 5350ms | 7637ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app3 | ok | 11375ms | 14638ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app4 | ok | 22500ms | 29250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app5 | ok | 51250ms | 59125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 6932ms | 9539ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 6917ms | 9475ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app3 | ok | 9000ms | 14437ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app4 | ok | 15000ms | 28600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app5 | ok | 31500ms | 55800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 5549ms | 8120ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 6781ms | 9020ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app3 | ok | 10652ms | 14565ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app4 | ok | 13043ms | 18750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app5 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 5417ms | 7946ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 6333ms | 8550ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app3 | ok | 8947ms | 13500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app4 | ok | 9556ms | 18250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app5 | ok | 17917ms | 26500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 4841ms | 6945ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 5583ms | 7689ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app3 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app4 | ok | 16500ms | 22000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app5 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 5360ms | 7648ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 5773ms | 7772ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app3 | ok | 10500ms | 14550ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app4 | ok | 18636ms | 28769ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app5 | ok | 34219ms | 43922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app6 | ok | 45000ms | 113250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app5 | ok | 28333ms | 43125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app6 | ok | 30000ms | 99000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 331.0 | 342.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 342.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 342.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 342.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 342.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 342.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 422.0 | 429.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 429.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 429.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 429.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 429.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 429.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
