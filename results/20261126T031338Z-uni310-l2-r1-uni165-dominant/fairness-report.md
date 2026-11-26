# Fairness benchmark: six-group-board-case (uni310-l2-r1-uni165-dominant)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-98689c64b-dv86c` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T03:14:44Z` |
| Run end | `2026-11-26T03:23:38Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 55 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/55 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 93.50 | 2.9219 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 90.0 | 181 | 4875 | 000=361, 200=4514 | 8.6 | 11.6 | 5927592.0 | 90.0% | 53.1% | -36.9 | 86.6% | -3.4 | 81.5% | -8.5 | 74.0s | 98.9% | 4595.0 |
| app2 | 2.0 | 32 | 223 | 000=64, 200=159 | 32.7 | 72.6 | 185108.0 | 2.0% | 9.4% | 7.4 | 2.7% | 0.7 | 3.7% | 1.7 | 77.3s | 98.9% | 159.0 |
| app3 | 2.0 | 32 | 222 | 000=64, 200=158 | 33.2 | 78.0 | 175782.0 | 2.0% | 9.4% | 7.4 | 2.6% | 0.6 | 3.7% | 1.7 | 77.4s | 98.9% | 159.0 |
| app4 | 2.0 | 32 | 221 | 000=63, 200=158 | 32.1 | 72.8 | 186824.0 | 2.0% | 9.4% | 7.4 | 2.7% | 0.7 | 3.7% | 1.7 | 77.4s | 98.9% | 158.0 |
| app5 | 2.0 | 32 | 220 | 000=62, 200=158 | 33.1 | 75.4 | 180002.0 | 2.0% | 9.4% | 7.4 | 2.6% | 0.6 | 3.7% | 1.7 | 77.4s | 98.9% | 158.0 |
| app6 | 2.0 | 32 | 222 | 000=63, 200=159 | 33.4 | 72.5 | 191950.0 | 2.0% | 9.4% | 7.4 | 2.8% | 0.8 | 3.7% | 1.7 | 77.4s | 98.9% | 159.0 |
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
| 0.0 | 150.0 | 150.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (54 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 27010.0 | 90.0% | 100.0% | 10.0 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 0.0 | 10.0 | app3 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 0.0 | 10.0 | app4 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 0.0 | 10.0 | app5 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 0.0 | 10.0 | app6 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 10.0 | 20.0 | app1 | True | False | 287852.0 | 90.0% | 98.2% | 8.2 |
| 10.0 | 20.0 | app2 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 10.0 | 20.0 | app3 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 10.0 | 20.0 | app4 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 10.0 | 20.0 | app5 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 10.0 | 20.0 | app6 | True | False | 5400.0 | 2.0% | 1.8% | -0.2 |
| 20.0 | 30.0 | app1 | True | False | 293274.0 | 90.0% | 95.2% | 5.2 |
| 20.0 | 30.0 | app2 | True | False | 4070.0 | 2.0% | 1.3% | -0.7 |
| 20.0 | 30.0 | app3 | True | False | 1358.0 | 2.0% | 0.4% | -1.6 |
| 20.0 | 30.0 | app4 | True | False | 4068.0 | 2.0% | 1.3% | -0.7 |
| 20.0 | 30.0 | app5 | True | False | 2716.0 | 2.0% | 0.9% | -1.1 |
| 20.0 | 30.0 | app6 | True | False | 2716.0 | 2.0% | 0.9% | -1.1 |
| 30.0 | 40.0 | app1 | True | False | 273010.0 | 90.0% | 86.7% | -3.3 |
| 30.0 | 40.0 | app2 | True | False | 8094.0 | 2.0% | 2.6% | 0.6 |
| 30.0 | 40.0 | app3 | True | False | 8134.0 | 2.0% | 2.6% | 0.6 |
| 30.0 | 40.0 | app4 | True | False | 8132.0 | 2.0% | 2.6% | 0.6 |
| 30.0 | 40.0 | app5 | True | False | 8148.0 | 2.0% | 2.6% | 0.6 |
| 30.0 | 40.0 | app6 | True | False | 9474.0 | 2.0% | 3.0% | 1.0 |
| 40.0 | 50.0 | app1 | True | False | 274448.0 | 90.0% | 89.8% | -0.2 |
| 40.0 | 50.0 | app2 | True | False | 6734.0 | 2.0% | 2.2% | 0.2 |
| 40.0 | 50.0 | app3 | True | False | 5402.0 | 2.0% | 1.8% | -0.2 |
| 40.0 | 50.0 | app4 | True | False | 6790.0 | 2.0% | 2.2% | 0.2 |
| 40.0 | 50.0 | app5 | True | False | 6782.0 | 2.0% | 2.2% | 0.2 |
| 40.0 | 50.0 | app6 | True | False | 5400.0 | 2.0% | 1.8% | -0.2 |
| 50.0 | 60.0 | app1 | True | False | 281084.0 | 90.0% | 90.8% | 0.8 |
| 50.0 | 60.0 | app2 | True | False | 6760.0 | 2.0% | 2.2% | 0.2 |
| 50.0 | 60.0 | app3 | True | False | 5426.0 | 2.0% | 1.8% | -0.2 |
| 50.0 | 60.0 | app4 | True | False | 5406.0 | 2.0% | 1.7% | -0.3 |
| 50.0 | 60.0 | app5 | True | False | 5432.0 | 2.0% | 1.8% | -0.2 |
| 50.0 | 60.0 | app6 | True | False | 5382.0 | 2.0% | 1.7% | -0.3 |
| 60.0 | 70.0 | app1 | True | False | 270392.0 | 90.0% | 88.9% | -1.1 |
| 60.0 | 70.0 | app2 | True | False | 5420.0 | 2.0% | 1.8% | -0.2 |
| 60.0 | 70.0 | app3 | True | False | 6776.0 | 2.0% | 2.2% | 0.2 |
| 60.0 | 70.0 | app4 | True | False | 8148.0 | 2.0% | 2.7% | 0.7 |
| 60.0 | 70.0 | app5 | True | False | 6756.0 | 2.0% | 2.2% | 0.2 |
| 60.0 | 70.0 | app6 | True | False | 6772.0 | 2.0% | 2.2% | 0.2 |
| 70.0 | 80.0 | app1 | True | False | 277240.0 | 90.0% | 91.1% | 1.1 |
| 70.0 | 80.0 | app2 | True | False | 6728.0 | 2.0% | 2.2% | 0.2 |
| 70.0 | 80.0 | app3 | True | False | 5400.0 | 2.0% | 1.8% | -0.2 |
| 70.0 | 80.0 | app4 | True | False | 4072.0 | 2.0% | 1.3% | -0.7 |
| 70.0 | 80.0 | app5 | True | False | 5432.0 | 2.0% | 1.8% | -0.2 |
| 70.0 | 80.0 | app6 | True | False | 5374.0 | 2.0% | 1.8% | -0.2 |
| 80.0 | 90.0 | app1 | True | False | 274528.0 | 90.0% | 89.4% | -0.6 |
| 80.0 | 90.0 | app2 | True | False | 5416.0 | 2.0% | 1.8% | -0.2 |
| 80.0 | 90.0 | app3 | True | False | 6780.0 | 2.0% | 2.2% | 0.2 |
| 80.0 | 90.0 | app4 | True | False | 6760.0 | 2.0% | 2.2% | 0.2 |
| 80.0 | 90.0 | app5 | True | False | 6790.0 | 2.0% | 2.2% | 0.2 |
| 80.0 | 90.0 | app6 | True | False | 6774.0 | 2.0% | 2.2% | 0.2 |
| 90.0 | 100.0 | app1 | True | False | 275920.0 | 90.0% | 90.3% | 0.3 |
| 90.0 | 100.0 | app2 | True | False | 6746.0 | 2.0% | 2.2% | 0.2 |
| 90.0 | 100.0 | app3 | True | False | 5432.0 | 2.0% | 1.8% | -0.2 |
| 90.0 | 100.0 | app4 | True | False | 6780.0 | 2.0% | 2.2% | 0.2 |
| 90.0 | 100.0 | app5 | True | False | 5430.0 | 2.0% | 1.8% | -0.2 |
| 90.0 | 100.0 | app6 | True | False | 5380.0 | 2.0% | 1.8% | -0.2 |
| 100.0 | 110.0 | app1 | True | False | 274570.0 | 90.0% | 89.8% | -0.2 |
| 100.0 | 110.0 | app2 | True | False | 5364.0 | 2.0% | 1.8% | -0.2 |
| 100.0 | 110.0 | app3 | True | False | 6782.0 | 2.0% | 2.2% | 0.2 |
| 100.0 | 110.0 | app4 | True | False | 5372.0 | 2.0% | 1.8% | -0.2 |
| 100.0 | 110.0 | app5 | True | False | 6790.0 | 2.0% | 2.2% | 0.2 |
| 100.0 | 110.0 | app6 | True | False | 6746.0 | 2.0% | 2.2% | 0.2 |
| 110.0 | 120.0 | app1 | True | False | 274486.0 | 90.0% | 89.8% | -0.2 |
| 110.0 | 120.0 | app2 | True | False | 6760.0 | 2.0% | 2.2% | 0.2 |
| 110.0 | 120.0 | app3 | True | False | 6758.0 | 2.0% | 2.2% | 0.2 |
| 110.0 | 120.0 | app4 | True | False | 5400.0 | 2.0% | 1.8% | -0.2 |
| 110.0 | 120.0 | app5 | True | False | 5396.0 | 2.0% | 1.8% | -0.2 |
| 110.0 | 120.0 | app6 | True | False | 6778.0 | 2.0% | 2.2% | 0.2 |
| 120.0 | 130.0 | app1 | True | False | 171744.0 | 90.0% | 84.1% | -5.9 |
| 120.0 | 130.0 | app2 | True | False | 6770.0 | 2.0% | 3.3% | 1.3 |
| 120.0 | 130.0 | app3 | True | False | 5424.0 | 2.0% | 2.7% | 0.7 |
| 120.0 | 130.0 | app4 | True | False | 6762.0 | 2.0% | 3.3% | 1.3 |
| 120.0 | 130.0 | app5 | True | False | 6766.0 | 2.0% | 3.3% | 1.3 |
| 120.0 | 130.0 | app6 | True | False | 6776.0 | 2.0% | 3.3% | 1.3 |
| 130.0 | 140.0 | app1 | True | False | 64954.0 | 90.0% | 30.0% | -60.0 |
| 130.0 | 140.0 | app2 | True | False | 29790.0 | 2.0% | 13.8% | 11.8 |
| 130.0 | 140.0 | app3 | True | False | 29698.0 | 2.0% | 13.7% | 11.7 |
| 130.0 | 140.0 | app4 | True | False | 31124.0 | 2.0% | 14.4% | 12.4 |
| 130.0 | 140.0 | app5 | True | False | 31164.0 | 2.0% | 14.4% | 12.4 |
| 130.0 | 140.0 | app6 | True | False | 29708.0 | 2.0% | 13.7% | 11.7 |
| 140.0 | 150.0 | app1 | True | False | 64868.0 | 90.0% | 72.7% | -17.3 |
| 140.0 | 150.0 | app2 | True | False | 5432.0 | 2.0% | 6.1% | 4.1 |
| 140.0 | 150.0 | app3 | True | False | 5400.0 | 2.0% | 6.1% | 4.1 |
| 140.0 | 150.0 | app4 | True | False | 4074.0 | 2.0% | 4.6% | 2.6 |
| 140.0 | 150.0 | app5 | True | False | 4064.0 | 2.0% | 4.6% | 2.6 |
| 140.0 | 150.0 | app6 | True | False | 5392.0 | 2.0% | 6.0% | 4.0 |
| 150.0 | 160.0 | app1 | True | False | 72976.0 | 90.0% | 100.0% | 10.0 |
| 150.0 | 160.0 | app2 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 150.0 | 160.0 | app3 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 150.0 | 160.0 | app4 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 150.0 | 160.0 | app5 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 150.0 | 160.0 | app6 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 160.0 | 170.0 | app1 | True | False | 285410.0 | 90.0% | 100.0% | 10.0 |
| 160.0 | 170.0 | app2 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 160.0 | 170.0 | app3 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 160.0 | 170.0 | app4 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 160.0 | 170.0 | app5 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 160.0 | 170.0 | app6 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 170.0 | 180.0 | app1 | True | False | 285410.0 | 90.0% | 95.9% | 5.9 |
| 170.0 | 180.0 | app2 | True | False | 1358.0 | 2.0% | 0.5% | -1.5 |
| 170.0 | 180.0 | app3 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 170.0 | 180.0 | app4 | True | False | 5402.0 | 2.0% | 1.8% | -0.2 |
| 170.0 | 180.0 | app5 | True | False | 0.0 | 2.0% | 0.0% | -2.0 |
| 170.0 | 180.0 | app6 | True | False | 5412.0 | 2.0% | 1.8% | -0.2 |
| 180.0 | 190.0 | app1 | True | False | 258142.0 | 90.0% | 92.7% | 2.7 |
| 180.0 | 190.0 | app2 | True | False | 5366.0 | 2.0% | 1.9% | -0.1 |
| 180.0 | 190.0 | app3 | True | False | 2684.0 | 2.0% | 1.0% | -1.0 |
| 180.0 | 190.0 | app4 | True | False | 4062.0 | 2.0% | 1.5% | -0.5 |
| 180.0 | 190.0 | app5 | True | False | 4074.0 | 2.0% | 1.5% | -0.5 |
| 180.0 | 190.0 | app6 | True | False | 4058.0 | 2.0% | 1.5% | -0.5 |
| 190.0 | 200.0 | app1 | True | False | 269300.0 | 90.0% | 88.9% | -1.1 |
| 190.0 | 200.0 | app2 | True | False | 6776.0 | 2.0% | 2.2% | 0.2 |
| 190.0 | 200.0 | app3 | True | False | 6746.0 | 2.0% | 2.2% | 0.2 |
| 190.0 | 200.0 | app4 | True | False | 6780.0 | 2.0% | 2.2% | 0.2 |
| 190.0 | 200.0 | app5 | True | False | 6766.0 | 2.0% | 2.2% | 0.2 |
| 190.0 | 200.0 | app6 | True | False | 6724.0 | 2.0% | 2.2% | 0.2 |
| 200.0 | 211.0 | app1 | True | False | 267828.0 | 90.0% | 90.0% | 0.0 |
| 200.0 | 211.0 | app2 | True | False | 6730.0 | 2.0% | 2.3% | 0.3 |
| 200.0 | 211.0 | app3 | True | False | 5390.0 | 2.0% | 1.8% | -0.2 |
| 200.0 | 211.0 | app4 | True | False | 4060.0 | 2.0% | 1.4% | -0.6 |
| 200.0 | 211.0 | app5 | True | False | 6778.0 | 2.0% | 2.3% | 0.3 |
| 200.0 | 211.0 | app6 | True | False | 6758.0 | 2.0% | 2.3% | 0.3 |
| 211.0 | 221.0 | app1 | True | False | 281262.0 | 90.0% | 91.6% | 1.6 |
| 211.0 | 221.0 | app2 | True | False | 5414.0 | 2.0% | 1.8% | -0.2 |
| 211.0 | 221.0 | app3 | True | False | 5364.0 | 2.0% | 1.7% | -0.3 |
| 211.0 | 221.0 | app4 | True | False | 6762.0 | 2.0% | 2.2% | 0.2 |
| 211.0 | 221.0 | app5 | True | False | 4074.0 | 2.0% | 1.3% | -0.7 |
| 211.0 | 221.0 | app6 | True | False | 4064.0 | 2.0% | 1.3% | -0.7 |
| 221.0 | 231.0 | app1 | True | False | 274414.0 | 90.0% | 88.3% | -1.7 |
| 221.0 | 231.0 | app2 | True | False | 6756.0 | 2.0% | 2.2% | 0.2 |
| 221.0 | 231.0 | app3 | True | False | 8094.0 | 2.0% | 2.6% | 0.6 |
| 221.0 | 231.0 | app4 | True | False | 6748.0 | 2.0% | 2.2% | 0.2 |
| 221.0 | 231.0 | app5 | True | False | 6758.0 | 2.0% | 2.2% | 0.2 |
| 221.0 | 231.0 | app6 | True | False | 8132.0 | 2.0% | 2.6% | 0.6 |
| 231.0 | 241.0 | app1 | True | False | 279792.0 | 90.0% | 90.4% | 0.4 |
| 231.0 | 241.0 | app2 | True | False | 5406.0 | 2.0% | 1.7% | -0.3 |
| 231.0 | 241.0 | app3 | True | False | 5420.0 | 2.0% | 1.8% | -0.2 |
| 231.0 | 241.0 | app4 | True | False | 6756.0 | 2.0% | 2.2% | 0.2 |
| 231.0 | 241.0 | app5 | True | False | 6704.0 | 2.0% | 2.2% | 0.2 |
| 231.0 | 241.0 | app6 | True | False | 5430.0 | 2.0% | 1.8% | -0.2 |
| 241.0 | 251.0 | app1 | False | n/a | 262256.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 8102.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | n/a | 9494.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app4 | False | n/a | 9506.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app5 | False | n/a | 8080.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app6 | False | n/a | 9490.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 5422.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 35116.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | False | n/a | 33820.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | False | n/a | 33860.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | False | n/a | 35102.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | False | n/a | 33810.0 | n/a | n/a | n/a |
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
| 341.0 | 351.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 432.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 432.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 432.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 432.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 432.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 432.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
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
| 532.0 | 534.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 534.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 534.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 534.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 534.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 534.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 192 | 384ms | 4422ms | 4942ms |
| 0.0 | 10.0 | app2 | ok | 14 | 0ms | 475ms | 930ms |
| 0.0 | 10.0 | app3 | ok | 15 | 0ms | 375ms | 487ms |
| 0.0 | 10.0 | app4 | ok | 14 | 0ms | 430ms | 493ms |
| 0.0 | 10.0 | app5 | ok | 14 | 0ms | 412ms | 491ms |
| 0.0 | 10.0 | app6 | ok | 14 | 281ms | 456ms | 496ms |
| 10.0 | 20.0 | app1 | ok | 195 | 4435ms | 8587ms | 9859ms |
| 10.0 | 20.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 231 | 3983ms | 6878ms | 9688ms |
| 20.0 | 30.0 | app2 | ok | 2 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app3 | ok | 1 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app4 | ok | 2 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app5 | ok | 2 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app6 | ok | 2 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | app1 | ok | 182 | 3776ms | 5667ms | 9567ms |
| 30.0 | 40.0 | app2 | ok | 5 | 26667ms | 52500ms | 59250ms |
| 30.0 | 40.0 | app3 | ok | 4 | 23333ms | 48000ms | 58800ms |
| 30.0 | 40.0 | app4 | ok | 5 | 26667ms | 52500ms | 59250ms |
| 30.0 | 40.0 | app5 | ok | 4 | 23333ms | 48000ms | 58800ms |
| 30.0 | 40.0 | app6 | ok | 4 | 23333ms | 48000ms | 58800ms |
| 40.0 | 50.0 | app1 | ok | 211 | 3880ms | 6232ms | 9623ms |
| 40.0 | 50.0 | app2 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 40.0 | 50.0 | app3 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 40.0 | 50.0 | app4 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 40.0 | 50.0 | app5 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 40.0 | 50.0 | app6 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 50.0 | 60.0 | app1 | ok | 229 | 3830ms | 4964ms | 9428ms |
| 50.0 | 60.0 | app2 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 50.0 | 60.0 | app3 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 50.0 | 60.0 | app4 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 50.0 | 60.0 | app5 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 50.0 | 60.0 | app6 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 60.0 | 70.0 | app1 | ok | 195 | 3960ms | 6518ms | 9652ms |
| 60.0 | 70.0 | app2 | ok | 5 | 55000ms | 60000ms | 60000ms |
| 60.0 | 70.0 | app3 | ok | 5 | 55000ms | 60000ms | 60000ms |
| 60.0 | 70.0 | app4 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 60.0 | 70.0 | app5 | ok | 5 | 48750ms | 60000ms | 60000ms |
| 60.0 | 70.0 | app6 | ok | 5 | 55000ms | 60000ms | 60000ms |
| 70.0 | 80.0 | app1 | ok | 167 | 3901ms | 5361ms | 9536ms |
| 70.0 | 80.0 | app2 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 70.0 | 80.0 | app3 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 70.0 | 80.0 | app4 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 70.0 | 80.0 | app5 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 70.0 | 80.0 | app6 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 80.0 | 90.0 | app1 | ok | 224 | 3802ms | 4969ms | 9440ms |
| 80.0 | 90.0 | app2 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 80.0 | 90.0 | app3 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 80.0 | 90.0 | app4 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 80.0 | 90.0 | app5 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 80.0 | 90.0 | app6 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 90.0 | 100.0 | app1 | ok | 237 | 3657ms | 4911ms | 9303ms |
| 90.0 | 100.0 | app2 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 90.0 | 100.0 | app3 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 90.0 | 100.0 | app4 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 90.0 | 100.0 | app5 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 90.0 | 100.0 | app6 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 100.0 | 110.0 | app1 | ok | 179 | 3681ms | 4916ms | 9312ms |
| 100.0 | 110.0 | app2 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 100.0 | 110.0 | app3 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 100.0 | 110.0 | app4 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 100.0 | 110.0 | app5 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 100.0 | 110.0 | app6 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 110.0 | 120.0 | app1 | ok | 227 | 3324ms | 4934ms | 9403ms |
| 110.0 | 120.0 | app2 | ok | 33 | 35357ms | 60000ms | 60000ms |
| 110.0 | 120.0 | app3 | ok | 34 | 36429ms | 60000ms | 60000ms |
| 110.0 | 120.0 | app4 | ok | 32 | 35000ms | 60000ms | 60000ms |
| 110.0 | 120.0 | app5 | ok | 33 | 38077ms | 60000ms | 60000ms |
| 110.0 | 120.0 | app6 | ok | 33 | 35357ms | 60000ms | 60000ms |
| 120.0 | 130.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 169 | 17388ms | 27478ms | 29748ms |
| 130.0 | 140.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 130.0 | 140.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 130.0 | 140.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 130.0 | 140.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 130.0 | 140.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 187 | 479ms | 964ms | 5325ms |
| 150.0 | 160.0 | app2 | ok | 13 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | app3 | ok | 16 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | app4 | ok | 11 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | app5 | ok | 15 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | app6 | ok | 11 | 0ms | 0ms | 0ms |
| 160.0 | 170.0 | app1 | ok | 264 | 4245ms | 8286ms | 9829ms |
| 160.0 | 170.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 160.0 | 170.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 160.0 | 170.0 | app4 | ok | 1 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 160.0 | 170.0 | app6 | ok | 1 | 20000ms | 28000ms | 29800ms |
| 170.0 | 180.0 | app1 | ok | 220 | 3354ms | 4695ms | 4997ms |
| 170.0 | 180.0 | app2 | ok | 4 | 20000ms | 28000ms | 29800ms |
| 170.0 | 180.0 | app3 | ok | 2 | 20000ms | 28000ms | 29800ms |
| 170.0 | 180.0 | app4 | ok | 5 | 20000ms | 28000ms | 29800ms |
| 170.0 | 180.0 | app5 | ok | 3 | 20000ms | 28000ms | 29800ms |
| 170.0 | 180.0 | app6 | ok | 5 | 20000ms | 28000ms | 29800ms |
| 180.0 | 190.0 | app1 | ok | 167 | 3874ms | 7803ms | 9780ms |
| 180.0 | 190.0 | app2 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 180.0 | 190.0 | app3 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 180.0 | 190.0 | app4 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 180.0 | 190.0 | app5 | ok | 2 | 45000ms | 57000ms | 59700ms |
| 180.0 | 190.0 | app6 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 190.0 | 200.0 | app1 | ok | 180 | 3368ms | 6786ms | 9679ms |
| 190.0 | 200.0 | app2 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 190.0 | 200.0 | app3 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 190.0 | 200.0 | app4 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 190.0 | 200.0 | app5 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 190.0 | 200.0 | app6 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 200.0 | 211.0 | app1 | ok | 235 | 3908ms | 6908ms | 9691ms |
| 200.0 | 211.0 | app2 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 200.0 | 211.0 | app3 | ok | 6 | 45000ms | 57000ms | 59700ms |
| 200.0 | 211.0 | app4 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 200.0 | 211.0 | app5 | ok | 6 | 45000ms | 57000ms | 59700ms |
| 200.0 | 211.0 | app6 | ok | 5 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | app1 | ok | 184 | 3896ms | 6167ms | 9617ms |
| 211.0 | 221.0 | app2 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | app3 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | app4 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | app5 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | app6 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | app1 | ok | 209 | 3971ms | 7176ms | 9718ms |
| 221.0 | 231.0 | app2 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | app3 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | app4 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | app5 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | app6 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | app1 | ok | 216 | 3855ms | 5846ms | 9585ms |
| 231.0 | 241.0 | app2 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | app3 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | app4 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | app5 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 231.0 | 241.0 | app6 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 241.0 | 251.0 | app1 | ok | 95 | 3897ms | 5250ms | 9525ms |
| 241.0 | 251.0 | app2 | ok | 24 | 46000ms | 60000ms | 60000ms |
| 241.0 | 251.0 | app3 | ok | 24 | 47143ms | 60000ms | 60000ms |
| 241.0 | 251.0 | app4 | ok | 23 | 47000ms | 60000ms | 60000ms |
| 241.0 | 251.0 | app5 | ok | 23 | 47000ms | 60000ms | 60000ms |
| 241.0 | 251.0 | app6 | ok | 22 | 46000ms | 60000ms | 60000ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 6 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app3 | ok | 6 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app4 | ok | 7 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app5 | ok | 7 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app6 | ok | 7 | 20000ms | 28000ms | 29800ms |
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
| 341.0 | 351.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 432.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 432.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 432.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 432.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 432.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 432.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 532.0 | 534.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 534.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 534.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 534.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 534.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 534.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -13.8%
- app3 exceeded the 10% ledger tolerance: cost -17.7%
- app4 exceeded the 10% ledger tolerance: cost -12.6%
- app5 exceeded the 10% ledger tolerance: cost -15.8%
- app6 exceeded the 10% ledger tolerance: cost -10.7%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 5552220 | 275651 | 5827871.0 | 0.0% | 5927592.0 | 6103522.0 | -2.9% | True |
| app2 | 195570 | 9633 | 205203.0 | 0.0% | 185108.0 | 214836.0 | -13.8% | False |
| app3 | 194340 | 9626 | 203966.0 | 0.0% | 175782.0 | 213592.0 | -17.7% | False |
| app4 | 194340 | 9763 | 204103.0 | 0.0% | 186824.0 | 213866.0 | -12.6% | False |
| app5 | 194340 | 9732 | 204072.0 | 0.0% | 180002.0 | 213804.0 | -15.8% | False |
| app6 | 195570 | 9687 | 205257.0 | 0.0% | 191950.0 | 214944.0 | -10.7% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 4875 | 0 | 0 | 0 (never shed) | 0.00% | 90.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 223 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 222 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |
| app4 | 221 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |
| app5 | 220 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |
| app6 | 222 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5388, EvictedContextCancelled=260). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5388 | 0.051ms | 0.120ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 504176 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 4514 | 8701ms | 13982ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 159 | 48250ms | 111482ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app3 | ok | 158 | 48281ms | 111222ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app4 | ok | 158 | 48103ms | 111536ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app5 | ok | 158 | 49138ms | 111828ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app6 | ok | 159 | 48629ms | 111482ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5306 | 8958ms | 63150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (54 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 1875ms | 3936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 3000ms | 4700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app3 | ok | 3333ms | 4833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app4 | ok | 3250ms | 4600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app5 | ok | 3500ms | 4850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app6 | ok | 2500ms | 3750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 7754ms | 10159ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app3 | ok | 5000ms | 9800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app4 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app5 | ok | 8000ms | 9800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app6 | ok | 9000ms | 14375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 8120ms | 9929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 18750ms | 28500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app3 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app4 | ok | 18750ms | 28500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app5 | ok | 20000ms | 29000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app6 | ok | 20000ms | 29000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 8899ms | 13317ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 26000ms | 40500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app3 | ok | 27500ms | 42750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app4 | ok | 27500ms | 42750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app5 | ok | 26000ms | 40500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app6 | ok | 27000ms | 42375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 8836ms | 11096ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app3 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app4 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app5 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app6 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 8826ms | 12739ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app3 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app4 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app5 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app6 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 8891ms | 13864ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 55000ms | 108000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app3 | ok | 54375ms | 105000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app4 | ok | 56250ms | 111000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app5 | ok | 54375ms | 105000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app6 | ok | 54375ms | 105000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 8750ms | 11583ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 8814ms | 12970ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 8693ms | 12316ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 8711ms | 12329ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 8495ms | 12885ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 10189ms | 14519ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 50000ms | 106800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app3 | ok | 48750ms | 106800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app4 | ok | 49688ms | 108500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app5 | ok | 51562ms | 110143ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app6 | ok | 50000ms | 106800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 24667ms | 29467ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 26667ms | 42000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app3 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app4 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app5 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 2312ms | 5773ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 4500ms | 6900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app3 | ok | 4750ms | 6800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app4 | ok | 4100ms | 4910ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app5 | ok | 4500ms | 5862ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app6 | ok | 2500ms | 5650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 8885ms | 13986ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app3 | ok | 10000ms | 14500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app4 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app5 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app6 | ok | 11250ms | 14625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 8524ms | 9852ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 20000ms | 29000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app3 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app4 | ok | 23750ms | 29375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app5 | ok | 20000ms | 29000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app6 | ok | 23750ms | 29375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app1 | ok | 9063ms | 14064ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app2 | ok | 35000ms | 44000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app3 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app4 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app5 | ok | 33750ms | 43875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app6 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app1 | ok | 9081ms | 14299ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app2 | ok | 39375ms | 56250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app3 | ok | 42500ms | 58125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app4 | ok | 39375ms | 56250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app5 | ok | 39375ms | 56250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app6 | ok | 39375ms | 56250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 211.0 | app1 | ok | 8638ms | 14048ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 211.0 | app2 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 211.0 | app3 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 211.0 | app4 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 211.0 | app5 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 211.0 | app6 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 8829ms | 14175ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 80000ms | 116000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app3 | ok | 60000ms | 114000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app4 | ok | 57500ms | 112500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app5 | ok | 75000ms | 115500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app6 | ok | 75000ms | 115500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 8847ms | 13308ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 8736ms | 9995ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 8882ms | 10958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 40000ms | 100500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app3 | ok | 39643ms | 82500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app4 | ok | 38438ms | 95000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app5 | ok | 40714ms | 104400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app6 | ok | 39643ms | 95000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 341.0 | 351.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 432.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 432.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 432.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 432.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 432.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 432.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 532.0 | 534.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 534.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 534.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 534.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 534.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 534.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
