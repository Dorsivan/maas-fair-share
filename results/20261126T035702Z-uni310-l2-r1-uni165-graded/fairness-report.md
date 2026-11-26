# Fairness benchmark: six-group-board-case (uni310-l2-r1-uni165-graded)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 8.6 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 8.6 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

## Run metadata

| field | value |
|---|---|
| Scenario | `six-group-board-case` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-69f447fbb4-pkb6c` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T03:58:24Z` |
| Run end | `2026-11-26T04:05:22Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 43 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/43 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 82.00 | 2.5625 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 40.0 | 75 | 2195 | 000=1, 200=2194 | 8.2 | 10.1 | 2912068.0 | 40.0% | 31.9% | -8.1 | 39.7% | -0.3 | 39.6% | -0.4 | 88.3s | 98.9% | 2195.0 |
| app2 | 20.0 | 32 | 1093 | 000=1, 200=1092 | 6.8 | 8.8 | 1461912.0 | 20.0% | 13.6% | -6.4 | 19.9% | -0.1 | 19.7% | -0.3 | 87.1s | 98.9% | 1093.0 |
| app3 | 15.0 | 32 | 828 | 200=828 | 9.4 | 11.4 | 1098120.0 | 15.0% | 13.6% | -1.4 | 15.0% | -0.0 | 14.9% | -0.1 | 88.4s | 98.9% | 828.0 |
| app4 | 10.0 | 32 | 563 | 200=563 | 14.1 | 16.2 | 738252.0 | 10.0% | 13.6% | 3.6 | 10.1% | 0.1 | 10.2% | 0.2 | 89.4s | 98.9% | 563.0 |
| app5 | 10.0 | 32 | 563 | 200=563 | 14.1 | 16.2 | 748292.0 | 10.0% | 13.6% | 3.6 | 10.2% | 0.2 | 10.2% | 0.2 | 89.4s | 98.9% | 563.0 |
| app6 | 5.0 | 32 | 298 | 200=298 | 28.2 | 30.7 | 381744.0 | 5.0% | 13.6% | 8.6 | 5.2% | 0.2 | 5.4% | 0.4 | 89.4s | 98.9% | 298.0 |
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
| 0.0 | 10.0 | 10.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (42 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 1358.0 | 40.0% | 7.7% | -32.3 |
| 0.0 | 10.0 | app2 | True | False | 14862.0 | 20.0% | 84.6% | 64.6 |
| 0.0 | 10.0 | app3 | True | False | 0.0 | 15.0% | 0.0% | -15.0 |
| 0.0 | 10.0 | app4 | True | False | 0.0 | 10.0% | 0.0% | -10.0 |
| 0.0 | 10.0 | app5 | True | False | 1356.0 | 10.0% | 7.7% | -2.3 |
| 0.0 | 10.0 | app6 | True | False | 0.0 | 5.0% | 0.0% | -5.0 |
| 10.0 | 20.0 | app1 | True | False | 121738.0 | 40.0% | 43.3% | 3.3 |
| 10.0 | 20.0 | app2 | True | False | 59440.0 | 20.0% | 21.1% | 1.1 |
| 10.0 | 20.0 | app3 | True | False | 46044.0 | 15.0% | 16.4% | 1.4 |
| 10.0 | 20.0 | app4 | True | False | 21608.0 | 10.0% | 7.7% | -2.3 |
| 10.0 | 20.0 | app5 | True | False | 28410.0 | 10.0% | 10.1% | 0.1 |
| 10.0 | 20.0 | app6 | True | False | 4074.0 | 5.0% | 1.4% | -3.6 |
| 20.0 | 30.0 | app1 | True | False | 121856.0 | 40.0% | 40.0% | 0.0 |
| 20.0 | 30.0 | app2 | True | False | 60948.0 | 20.0% | 20.0% | 0.0 |
| 20.0 | 30.0 | app3 | True | False | 45996.0 | 15.0% | 15.1% | 0.1 |
| 20.0 | 30.0 | app4 | True | False | 31146.0 | 10.0% | 10.2% | 0.2 |
| 20.0 | 30.0 | app5 | True | False | 32468.0 | 10.0% | 10.7% | 0.7 |
| 20.0 | 30.0 | app6 | True | False | 12172.0 | 5.0% | 4.0% | -1.0 |
| 30.0 | 40.0 | app1 | True | False | 125666.0 | 40.0% | 40.9% | 0.9 |
| 30.0 | 40.0 | app2 | True | False | 62152.0 | 20.0% | 20.3% | 0.3 |
| 30.0 | 40.0 | app3 | True | False | 44682.0 | 15.0% | 14.6% | -0.4 |
| 30.0 | 40.0 | app4 | True | False | 29776.0 | 10.0% | 9.7% | -0.3 |
| 30.0 | 40.0 | app5 | True | False | 29766.0 | 10.0% | 9.7% | -0.3 |
| 30.0 | 40.0 | app6 | True | False | 14864.0 | 5.0% | 4.8% | -0.2 |
| 40.0 | 50.0 | app1 | True | False | 119062.0 | 40.0% | 38.9% | -1.1 |
| 40.0 | 50.0 | app2 | True | False | 59466.0 | 20.0% | 19.5% | -0.5 |
| 40.0 | 50.0 | app3 | True | False | 47352.0 | 15.0% | 15.5% | 0.5 |
| 40.0 | 50.0 | app4 | True | False | 32434.0 | 10.0% | 10.6% | 0.6 |
| 40.0 | 50.0 | app5 | True | False | 31154.0 | 10.0% | 10.2% | 0.2 |
| 40.0 | 50.0 | app6 | True | False | 16230.0 | 5.0% | 5.3% | 0.3 |
| 50.0 | 60.0 | app1 | True | False | 123206.0 | 40.0% | 40.5% | 0.5 |
| 50.0 | 60.0 | app2 | True | False | 60896.0 | 20.0% | 20.0% | -0.0 |
| 50.0 | 60.0 | app3 | True | False | 46028.0 | 15.0% | 15.1% | 0.1 |
| 50.0 | 60.0 | app4 | True | False | 29728.0 | 10.0% | 9.8% | -0.2 |
| 50.0 | 60.0 | app5 | True | False | 31186.0 | 10.0% | 10.2% | 0.2 |
| 50.0 | 60.0 | app6 | True | False | 13498.0 | 5.0% | 4.4% | -0.6 |
| 60.0 | 70.0 | app1 | True | False | 123010.0 | 40.0% | 39.9% | -0.1 |
| 60.0 | 70.0 | app2 | True | False | 62158.0 | 20.0% | 20.2% | 0.2 |
| 60.0 | 70.0 | app3 | True | False | 45950.0 | 15.0% | 14.9% | -0.1 |
| 60.0 | 70.0 | app4 | True | False | 31104.0 | 10.0% | 10.1% | 0.1 |
| 60.0 | 70.0 | app5 | True | False | 29732.0 | 10.0% | 9.6% | -0.4 |
| 60.0 | 70.0 | app6 | True | False | 16264.0 | 5.0% | 5.3% | 0.3 |
| 70.0 | 80.0 | app1 | True | False | 122972.0 | 40.0% | 40.4% | 0.4 |
| 70.0 | 80.0 | app2 | True | False | 59450.0 | 20.0% | 19.5% | -0.5 |
| 70.0 | 80.0 | app3 | True | False | 43282.0 | 15.0% | 14.2% | -0.8 |
| 70.0 | 80.0 | app4 | True | False | 31082.0 | 10.0% | 10.2% | 0.2 |
| 70.0 | 80.0 | app5 | True | False | 31112.0 | 10.0% | 10.2% | 0.2 |
| 70.0 | 80.0 | app6 | True | False | 16232.0 | 5.0% | 5.3% | 0.3 |
| 80.0 | 90.0 | app1 | True | False | 113590.0 | 40.0% | 41.2% | 1.2 |
| 80.0 | 90.0 | app2 | True | False | 56820.0 | 20.0% | 20.6% | 0.6 |
| 80.0 | 90.0 | app3 | True | False | 44588.0 | 15.0% | 16.2% | 1.2 |
| 80.0 | 90.0 | app4 | True | False | 24340.0 | 10.0% | 8.8% | -1.2 |
| 80.0 | 90.0 | app5 | True | False | 24338.0 | 10.0% | 8.8% | -1.2 |
| 80.0 | 90.0 | app6 | True | False | 12188.0 | 5.0% | 4.4% | -0.6 |
| 90.0 | 100.0 | app1 | True | False | 117686.0 | 40.0% | 38.8% | -1.2 |
| 90.0 | 100.0 | app2 | True | False | 66238.0 | 20.0% | 21.9% | 1.9 |
| 90.0 | 100.0 | app3 | True | False | 41924.0 | 15.0% | 13.8% | -1.2 |
| 90.0 | 100.0 | app4 | True | False | 31198.0 | 10.0% | 10.3% | 0.3 |
| 90.0 | 100.0 | app5 | True | False | 31116.0 | 10.0% | 10.3% | 0.3 |
| 90.0 | 100.0 | app6 | True | False | 14898.0 | 5.0% | 4.9% | -0.1 |
| 100.0 | 110.0 | app1 | True | False | 120454.0 | 40.0% | 39.6% | -0.4 |
| 100.0 | 110.0 | app2 | True | False | 55450.0 | 20.0% | 18.2% | -1.8 |
| 100.0 | 110.0 | app3 | True | False | 47266.0 | 15.0% | 15.5% | 0.5 |
| 100.0 | 110.0 | app4 | True | False | 32516.0 | 10.0% | 10.7% | 0.7 |
| 100.0 | 110.0 | app5 | True | False | 32528.0 | 10.0% | 10.7% | 0.7 |
| 100.0 | 110.0 | app6 | True | False | 16226.0 | 5.0% | 5.3% | 0.3 |
| 110.0 | 120.0 | app1 | True | False | 123042.0 | 40.0% | 40.1% | 0.1 |
| 110.0 | 120.0 | app2 | True | False | 59464.0 | 20.0% | 19.4% | -0.6 |
| 110.0 | 120.0 | app3 | True | False | 45962.0 | 15.0% | 15.0% | -0.0 |
| 110.0 | 120.0 | app4 | True | False | 29810.0 | 10.0% | 9.7% | -0.3 |
| 110.0 | 120.0 | app5 | True | False | 31148.0 | 10.0% | 10.1% | 0.1 |
| 110.0 | 120.0 | app6 | True | False | 17596.0 | 5.0% | 5.7% | 0.7 |
| 120.0 | 130.0 | app1 | True | False | 121738.0 | 40.0% | 40.0% | -0.0 |
| 120.0 | 130.0 | app2 | True | False | 62268.0 | 20.0% | 20.5% | 0.5 |
| 120.0 | 130.0 | app3 | True | False | 47292.0 | 15.0% | 15.5% | 0.5 |
| 120.0 | 130.0 | app4 | True | False | 29740.0 | 10.0% | 9.8% | -0.2 |
| 120.0 | 130.0 | app5 | True | False | 29776.0 | 10.0% | 9.8% | -0.2 |
| 120.0 | 130.0 | app6 | True | False | 13542.0 | 5.0% | 4.4% | -0.6 |
| 130.0 | 140.0 | app1 | True | False | 118846.0 | 40.0% | 39.1% | -0.9 |
| 130.0 | 140.0 | app2 | True | False | 60934.0 | 20.0% | 20.0% | 0.0 |
| 130.0 | 140.0 | app3 | True | False | 44632.0 | 15.0% | 14.7% | -0.3 |
| 130.0 | 140.0 | app4 | True | False | 31120.0 | 10.0% | 10.2% | 0.2 |
| 130.0 | 140.0 | app5 | True | False | 32514.0 | 10.0% | 10.7% | 0.7 |
| 130.0 | 140.0 | app6 | True | False | 16286.0 | 5.0% | 5.4% | 0.4 |
| 140.0 | 150.0 | app1 | True | False | 124378.0 | 40.0% | 40.2% | 0.2 |
| 140.0 | 150.0 | app2 | True | False | 62226.0 | 20.0% | 20.1% | 0.1 |
| 140.0 | 150.0 | app3 | True | False | 45966.0 | 15.0% | 14.8% | -0.2 |
| 140.0 | 150.0 | app4 | True | False | 31098.0 | 10.0% | 10.0% | 0.0 |
| 140.0 | 150.0 | app5 | True | False | 29786.0 | 10.0% | 9.6% | -0.4 |
| 140.0 | 150.0 | app6 | True | False | 16258.0 | 5.0% | 5.2% | 0.2 |
| 150.0 | 160.0 | app1 | True | False | 120226.0 | 40.0% | 39.5% | -0.5 |
| 150.0 | 160.0 | app2 | True | False | 60878.0 | 20.0% | 20.0% | 0.0 |
| 150.0 | 160.0 | app3 | True | False | 45954.0 | 15.0% | 15.1% | 0.1 |
| 150.0 | 160.0 | app4 | True | False | 31060.0 | 10.0% | 10.2% | 0.2 |
| 150.0 | 160.0 | app5 | True | False | 31060.0 | 10.0% | 10.2% | 0.2 |
| 150.0 | 160.0 | app6 | True | False | 14910.0 | 5.0% | 4.9% | -0.1 |
| 160.0 | 171.0 | app1 | True | False | 127242.0 | 40.0% | 41.1% | 1.1 |
| 160.0 | 171.0 | app2 | True | False | 60786.0 | 20.0% | 19.6% | -0.4 |
| 160.0 | 171.0 | app3 | True | False | 45906.0 | 15.0% | 14.8% | -0.2 |
| 160.0 | 171.0 | app4 | True | False | 31066.0 | 10.0% | 10.0% | 0.0 |
| 160.0 | 171.0 | app5 | True | False | 31020.0 | 10.0% | 10.0% | 0.0 |
| 160.0 | 171.0 | app6 | True | False | 13520.0 | 5.0% | 4.4% | -0.6 |
| 171.0 | 181.0 | app1 | True | False | 120282.0 | 40.0% | 39.5% | -0.5 |
| 171.0 | 181.0 | app2 | True | False | 62268.0 | 20.0% | 20.5% | 0.5 |
| 171.0 | 181.0 | app3 | True | False | 47426.0 | 15.0% | 15.6% | 0.6 |
| 171.0 | 181.0 | app4 | True | False | 29700.0 | 10.0% | 9.8% | -0.2 |
| 171.0 | 181.0 | app5 | True | False | 29762.0 | 10.0% | 9.8% | -0.2 |
| 171.0 | 181.0 | app6 | True | False | 14886.0 | 5.0% | 4.9% | -0.1 |
| 181.0 | 191.0 | app1 | True | False | 121716.0 | 40.0% | 40.0% | -0.0 |
| 181.0 | 191.0 | app2 | True | False | 59526.0 | 20.0% | 19.6% | -0.4 |
| 181.0 | 191.0 | app3 | True | False | 44676.0 | 15.0% | 14.7% | -0.3 |
| 181.0 | 191.0 | app4 | True | False | 31090.0 | 10.0% | 10.2% | 0.2 |
| 181.0 | 191.0 | app5 | True | False | 31130.0 | 10.0% | 10.2% | 0.2 |
| 181.0 | 191.0 | app6 | True | False | 16246.0 | 5.0% | 5.3% | 0.3 |
| 191.0 | 201.0 | app1 | True | False | 119064.0 | 40.0% | 40.2% | 0.2 |
| 191.0 | 201.0 | app2 | True | False | 60748.0 | 20.0% | 20.5% | 0.5 |
| 191.0 | 201.0 | app3 | True | False | 44598.0 | 15.0% | 15.1% | 0.1 |
| 191.0 | 201.0 | app4 | True | False | 29720.0 | 10.0% | 10.0% | 0.0 |
| 191.0 | 201.0 | app5 | True | False | 28448.0 | 10.0% | 9.6% | -0.4 |
| 191.0 | 201.0 | app6 | True | False | 13566.0 | 5.0% | 4.6% | -0.4 |
| 201.0 | 211.0 | app1 | True | False | 123126.0 | 40.0% | 40.1% | 0.1 |
| 201.0 | 211.0 | app2 | True | False | 59528.0 | 20.0% | 19.4% | -0.6 |
| 201.0 | 211.0 | app3 | True | False | 45958.0 | 15.0% | 15.0% | -0.0 |
| 201.0 | 211.0 | app4 | True | False | 31068.0 | 10.0% | 10.1% | 0.1 |
| 201.0 | 211.0 | app5 | True | False | 31112.0 | 10.0% | 10.1% | 0.1 |
| 201.0 | 211.0 | app6 | True | False | 16228.0 | 5.0% | 5.3% | 0.3 |
| 211.0 | 221.0 | app1 | True | False | 121764.0 | 40.0% | 40.2% | 0.2 |
| 211.0 | 221.0 | app2 | True | False | 60882.0 | 20.0% | 20.1% | 0.1 |
| 211.0 | 221.0 | app3 | True | False | 44724.0 | 15.0% | 14.8% | -0.2 |
| 211.0 | 221.0 | app4 | True | False | 29770.0 | 10.0% | 9.8% | -0.2 |
| 211.0 | 221.0 | app5 | True | False | 29742.0 | 10.0% | 9.8% | -0.2 |
| 211.0 | 221.0 | app6 | True | False | 16210.0 | 5.0% | 5.3% | 0.3 |
| 221.0 | 231.0 | app1 | True | False | 120480.0 | 40.0% | 39.9% | -0.1 |
| 221.0 | 231.0 | app2 | True | False | 60858.0 | 20.0% | 20.2% | 0.2 |
| 221.0 | 231.0 | app3 | True | False | 45896.0 | 15.0% | 15.2% | 0.2 |
| 221.0 | 231.0 | app4 | True | False | 28376.0 | 10.0% | 9.4% | -0.6 |
| 221.0 | 231.0 | app5 | True | False | 31172.0 | 10.0% | 10.3% | 0.3 |
| 221.0 | 231.0 | app6 | True | False | 14926.0 | 5.0% | 4.9% | -0.1 |
| 231.0 | 241.0 | app1 | True | False | 120502.0 | 40.0% | 39.6% | -0.4 |
| 231.0 | 241.0 | app2 | True | False | 62238.0 | 20.0% | 20.4% | 0.4 |
| 231.0 | 241.0 | app3 | True | False | 45964.0 | 15.0% | 15.1% | 0.1 |
| 231.0 | 241.0 | app4 | True | False | 31094.0 | 10.0% | 10.2% | 0.2 |
| 231.0 | 241.0 | app5 | True | False | 29780.0 | 10.0% | 9.8% | -0.2 |
| 231.0 | 241.0 | app6 | True | False | 14938.0 | 5.0% | 4.9% | -0.1 |
| 241.0 | 251.0 | app1 | False | n/a | 115018.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 51428.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | n/a | 48696.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app4 | False | n/a | 36462.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app5 | False | n/a | 35188.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app6 | False | n/a | 17570.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 4046.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | False | n/a | 1358.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | False | n/a | 12146.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | False | n/a | 13488.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | False | n/a | 28416.0 | n/a | n/a | n/a |
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
| 371.0 | 382.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 382.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 382.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 382.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 382.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 382.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
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
| 412.0 | 418.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 418.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 418.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 418.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 418.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 418.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 90 | 611ms | 3977ms | 4898ms |
| 0.0 | 10.0 | app2 | ok | 45 | 776ms | 3393ms | 4839ms |
| 0.0 | 10.0 | app3 | ok | 34 | 600ms | 3938ms | 4894ms |
| 0.0 | 10.0 | app4 | ok | 24 | 0ms | 4000ms | 4900ms |
| 0.0 | 10.0 | app5 | ok | 23 | 1281ms | 3850ms | 4885ms |
| 0.0 | 10.0 | app6 | ok | 16 | 0ms | 0ms | 1ms |
| 10.0 | 20.0 | app1 | ok | 78 | 2969ms | 4594ms | 4959ms |
| 10.0 | 20.0 | app2 | ok | 34 | 2227ms | 4433ms | 4943ms |
| 10.0 | 20.0 | app3 | ok | 33 | 3750ms | 7643ms | 9764ms |
| 10.0 | 20.0 | app4 | ok | 24 | 7391ms | 9478ms | 9948ms |
| 10.0 | 20.0 | app5 | ok | 25 | 7024ms | 9405ms | 9940ms |
| 10.0 | 20.0 | app6 | ok | 9 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app1 | ok | 104 | 3692ms | 4901ms | 9257ms |
| 20.0 | 30.0 | app2 | ok | 58 | 2389ms | 4538ms | 7100ms |
| 20.0 | 30.0 | app3 | ok | 36 | 4038ms | 7750ms | 9775ms |
| 20.0 | 30.0 | app4 | ok | 21 | 7917ms | 16000ms | 28600ms |
| 20.0 | 30.0 | app5 | ok | 20 | 8125ms | 20000ms | 29000ms |
| 20.0 | 30.0 | app6 | ok | 9 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | app1 | ok | 90 | 3661ms | 4732ms | 4973ms |
| 30.0 | 40.0 | app2 | ok | 44 | 2062ms | 4267ms | 4927ms |
| 30.0 | 40.0 | app3 | ok | 33 | 4464ms | 8625ms | 9862ms |
| 30.0 | 40.0 | app4 | ok | 22 | 7895ms | 15333ms | 28533ms |
| 30.0 | 40.0 | app5 | ok | 23 | 7875ms | 14667ms | 28467ms |
| 30.0 | 40.0 | app6 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app1 | ok | 76 | 3538ms | 4708ms | 4971ms |
| 40.0 | 50.0 | app2 | ok | 38 | 2109ms | 4269ms | 4927ms |
| 40.0 | 50.0 | app3 | ok | 29 | 4076ms | 7583ms | 9758ms |
| 40.0 | 50.0 | app4 | ok | 19 | 8167ms | 20500ms | 29050ms |
| 40.0 | 50.0 | app5 | ok | 19 | 8393ms | 22400ms | 29240ms |
| 40.0 | 50.0 | app6 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app1 | ok | 98 | 3588ms | 4741ms | 5100ms |
| 50.0 | 60.0 | app2 | ok | 49 | 2067ms | 4279ms | 4928ms |
| 50.0 | 60.0 | app3 | ok | 37 | 4350ms | 8458ms | 9846ms |
| 50.0 | 60.0 | app4 | ok | 24 | 8158ms | 20400ms | 29040ms |
| 50.0 | 60.0 | app5 | ok | 24 | 8750ms | 24000ms | 29400ms |
| 50.0 | 60.0 | app6 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app1 | ok | 95 | 3552ms | 4710ms | 4971ms |
| 60.0 | 70.0 | app2 | ok | 48 | 2056ms | 4250ms | 4925ms |
| 60.0 | 70.0 | app3 | ok | 35 | 4489ms | 8654ms | 9865ms |
| 60.0 | 70.0 | app4 | ok | 24 | 9000ms | 24667ms | 29467ms |
| 60.0 | 70.0 | app5 | ok | 24 | 8529ms | 23143ms | 29314ms |
| 60.0 | 70.0 | app6 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app1 | ok | 99 | 3066ms | 4613ms | 4961ms |
| 70.0 | 80.0 | app2 | ok | 42 | 1714ms | 3950ms | 4895ms |
| 70.0 | 80.0 | app3 | ok | 41 | 3750ms | 7722ms | 9772ms |
| 70.0 | 80.0 | app4 | ok | 33 | 7500ms | 19000ms | 28900ms |
| 70.0 | 80.0 | app5 | ok | 32 | 7500ms | 19333ms | 28933ms |
| 70.0 | 80.0 | app6 | ok | 16 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app1 | ok | 65 | 4107ms | 8375ms | 9837ms |
| 80.0 | 90.0 | app2 | ok | 41 | 2596ms | 7437ms | 9744ms |
| 80.0 | 90.0 | app3 | ok | 20 | 5000ms | 9000ms | 9900ms |
| 80.0 | 90.0 | app4 | ok | 9 | 9500ms | 25500ms | 29550ms |
| 80.0 | 90.0 | app5 | ok | 9 | 8750ms | 24000ms | 29400ms |
| 80.0 | 90.0 | app6 | ok | 5 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app1 | ok | 95 | 3420ms | 4740ms | 7625ms |
| 90.0 | 100.0 | app2 | ok | 48 | 2263ms | 4429ms | 4943ms |
| 90.0 | 100.0 | app3 | ok | 36 | 3750ms | 7750ms | 9775ms |
| 90.0 | 100.0 | app4 | ok | 23 | 8026ms | 18500ms | 28850ms |
| 90.0 | 100.0 | app5 | ok | 23 | 8088ms | 20800ms | 29080ms |
| 90.0 | 100.0 | app6 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app1 | ok | 80 | 3529ms | 4706ms | 4971ms |
| 100.0 | 110.0 | app2 | ok | 38 | 2500ms | 4500ms | 4950ms |
| 100.0 | 110.0 | app3 | ok | 30 | 4375ms | 8500ms | 9850ms |
| 100.0 | 110.0 | app4 | ok | 20 | 7941ms | 16667ms | 28667ms |
| 100.0 | 110.0 | app5 | ok | 21 | 7917ms | 16000ms | 28600ms |
| 100.0 | 110.0 | app6 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app1 | ok | 96 | 3554ms | 4711ms | 4971ms |
| 110.0 | 120.0 | app2 | ok | 49 | 2067ms | 4279ms | 4928ms |
| 110.0 | 120.0 | app3 | ok | 36 | 4231ms | 8200ms | 9820ms |
| 110.0 | 120.0 | app4 | ok | 24 | 8333ms | 22000ms | 29200ms |
| 110.0 | 120.0 | app5 | ok | 24 | 8158ms | 20400ms | 29040ms |
| 110.0 | 120.0 | app6 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app1 | ok | 90 | 3480ms | 4696ms | 4970ms |
| 120.0 | 130.0 | app2 | ok | 44 | 1944ms | 4083ms | 4908ms |
| 120.0 | 130.0 | app3 | ok | 34 | 4271ms | 8300ms | 9830ms |
| 120.0 | 130.0 | app4 | ok | 22 | 8056ms | 19000ms | 28900ms |
| 120.0 | 130.0 | app5 | ok | 22 | 7895ms | 15333ms | 28533ms |
| 120.0 | 130.0 | app6 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 130.0 | 140.0 | app1 | ok | 113 | 3234ms | 4647ms | 4965ms |
| 130.0 | 140.0 | app2 | ok | 55 | 1894ms | 4191ms | 4919ms |
| 130.0 | 140.0 | app3 | ok | 43 | 4375ms | 8567ms | 9857ms |
| 130.0 | 140.0 | app4 | ok | 29 | 8152ms | 20333ms | 29033ms |
| 130.0 | 140.0 | app5 | ok | 28 | 8500ms | 23000ms | 29300ms |
| 130.0 | 140.0 | app6 | ok | 14 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app1 | ok | 79 | 3381ms | 4676ms | 4968ms |
| 140.0 | 150.0 | app2 | ok | 41 | 1964ms | 4212ms | 4921ms |
| 140.0 | 150.0 | app3 | ok | 28 | 4167ms | 8000ms | 9800ms |
| 140.0 | 150.0 | app4 | ok | 19 | 7969ms | 17333ms | 28733ms |
| 140.0 | 150.0 | app5 | ok | 21 | 8281ms | 21600ms | 29160ms |
| 140.0 | 150.0 | app6 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 150.0 | 160.0 | app1 | ok | 88 | 3625ms | 4725ms | 4972ms |
| 150.0 | 160.0 | app2 | ok | 44 | 2212ms | 4353ms | 4935ms |
| 150.0 | 160.0 | app3 | ok | 35 | 4323ms | 8409ms | 9841ms |
| 150.0 | 160.0 | app4 | ok | 22 | 7895ms | 15333ms | 28533ms |
| 150.0 | 160.0 | app5 | ok | 21 | 8281ms | 21600ms | 29160ms |
| 150.0 | 160.0 | app6 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 160.0 | 171.0 | app1 | ok | 105 | 3399ms | 4680ms | 4968ms |
| 160.0 | 171.0 | app2 | ok | 53 | 1853ms | 4054ms | 4905ms |
| 160.0 | 171.0 | app3 | ok | 38 | 4259ms | 8273ms | 9827ms |
| 160.0 | 171.0 | app4 | ok | 27 | 8553ms | 23250ms | 29325ms |
| 160.0 | 171.0 | app5 | ok | 27 | 8214ms | 21000ms | 29100ms |
| 160.0 | 171.0 | app6 | ok | 13 | 20000ms | 28000ms | 29800ms |
| 171.0 | 181.0 | app1 | ok | 69 | 3631ms | 4726ms | 4973ms |
| 171.0 | 181.0 | app2 | ok | 33 | 2013ms | 4175ms | 4918ms |
| 171.0 | 181.0 | app3 | ok | 26 | 4531ms | 8700ms | 9870ms |
| 171.0 | 181.0 | app4 | ok | 17 | 7833ms | 13000ms | 28300ms |
| 171.0 | 181.0 | app5 | ok | 17 | 8036ms | 18667ms | 28867ms |
| 171.0 | 181.0 | app6 | ok | 8 | 20000ms | 28000ms | 29800ms |
| 181.0 | 191.0 | app1 | ok | 88 | 3281ms | 4656ms | 4966ms |
| 181.0 | 191.0 | app2 | ok | 45 | 2036ms | 4297ms | 4930ms |
| 181.0 | 191.0 | app3 | ok | 33 | 4562ms | 8731ms | 9873ms |
| 181.0 | 191.0 | app4 | ok | 22 | 8667ms | 23714ms | 29371ms |
| 181.0 | 191.0 | app5 | ok | 23 | 8194ms | 20800ms | 29080ms |
| 181.0 | 191.0 | app6 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 191.0 | 201.0 | app1 | ok | 94 | 2864ms | 4573ms | 4957ms |
| 191.0 | 201.0 | app2 | ok | 41 | 1788ms | 4068ms | 4907ms |
| 191.0 | 201.0 | app3 | ok | 40 | 3571ms | 7500ms | 9750ms |
| 191.0 | 201.0 | app4 | ok | 27 | 7935ms | 16500ms | 28650ms |
| 191.0 | 201.0 | app5 | ok | 25 | 7738ms | 13333ms | 28333ms |
| 191.0 | 201.0 | app6 | ok | 13 | 20000ms | 28000ms | 29800ms |
| 201.0 | 211.0 | app1 | ok | 92 | 3562ms | 4712ms | 4971ms |
| 201.0 | 211.0 | app2 | ok | 52 | 2903ms | 4581ms | 4958ms |
| 201.0 | 211.0 | app3 | ok | 31 | 4115ms | 7786ms | 9779ms |
| 201.0 | 211.0 | app4 | ok | 19 | 9318ms | 25250ms | 29525ms |
| 201.0 | 211.0 | app5 | ok | 21 | 8281ms | 21600ms | 29160ms |
| 201.0 | 211.0 | app6 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app1 | ok | 93 | 3613ms | 4747ms | 5350ms |
| 211.0 | 221.0 | app2 | ok | 47 | 2125ms | 4309ms | 4931ms |
| 211.0 | 221.0 | app3 | ok | 34 | 4200ms | 8111ms | 9811ms |
| 211.0 | 221.0 | app4 | ok | 24 | 8333ms | 22000ms | 29200ms |
| 211.0 | 221.0 | app5 | ok | 22 | 8056ms | 19000ms | 28900ms |
| 211.0 | 221.0 | app6 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app1 | ok | 88 | 3553ms | 4711ms | 4971ms |
| 221.0 | 231.0 | app2 | ok | 44 | 1964ms | 4083ms | 4908ms |
| 221.0 | 231.0 | app3 | ok | 33 | 4464ms | 8625ms | 9862ms |
| 221.0 | 231.0 | app4 | ok | 22 | 9583ms | 25600ms | 29560ms |
| 221.0 | 231.0 | app5 | ok | 22 | 8667ms | 23714ms | 29371ms |
| 221.0 | 231.0 | app6 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 231.0 | 241.0 | app1 | ok | 77 | 3369ms | 4674ms | 4967ms |
| 231.0 | 241.0 | app2 | ok | 36 | 2105ms | 4308ms | 4931ms |
| 231.0 | 241.0 | app3 | ok | 29 | 4338ms | 8550ms | 9855ms |
| 231.0 | 241.0 | app4 | ok | 19 | 8393ms | 22400ms | 29240ms |
| 231.0 | 241.0 | app5 | ok | 20 | 8846ms | 24286ms | 29429ms |
| 231.0 | 241.0 | app6 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | app1 | ok | 53 | 3590ms | 4718ms | 4972ms |
| 241.0 | 251.0 | app2 | ok | 24 | 2364ms | 4455ms | 4945ms |
| 241.0 | 251.0 | app3 | ok | 24 | 4375ms | 8500ms | 9850ms |
| 241.0 | 251.0 | app4 | ok | 27 | 7614ms | 12000ms | 28200ms |
| 241.0 | 251.0 | app5 | ok | 27 | 8125ms | 21000ms | 29100ms |
| 241.0 | 251.0 | app6 | ok | 30 | 18462ms | 27692ms | 29769ms |
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
| 371.0 | 382.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 382.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 382.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 382.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 382.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 382.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 412.0 | 418.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 418.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 418.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 418.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 418.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 418.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2698620 | 134420 | 2833040.0 | 0.0% | 2912068.0 | 2967460.0 | -1.9% | True |
| app2 | 1343160 | 66823 | 1409983.0 | 0.0% | 1461912.0 | 1476806.0 | -1.0% | True |
| app3 | 1018440 | 50678 | 1069118.0 | 0.0% | 1098120.0 | 1119796.0 | -1.9% | True |
| app4 | 692490 | 34373 | 726863.0 | 0.0% | 738252.0 | 761236.0 | -3.0% | True |
| app5 | 692490 | 34682 | 727172.0 | 0.0% | 748292.0 | 761854.0 | -1.8% | True |
| app6 | 366540 | 18423 | 384963.0 | 0.0% | 381744.0 | 403386.0 | -5.4% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2195 | 0 | 0 | 0 (never shed) | 0.00% | 40.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1093 | 0 | 0 | 0 (never shed) | 0.00% | 20.0% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 828 | 0 | 0 | 0 (never shed) | 0.00% | 15.0% | n/a (nothing shed) | n/a (nothing shed) |
| app4 | 563 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| app5 | 563 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| app6 | 298 | 0 | 0 | 0 (never shed) | 0.00% | 5.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5540). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5540 | 0.051ms | 0.114ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 393240 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 2194 | 8241ms | 10103ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1092 | 6844ms | 9351ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app3 | ok | 828 | 9325ms | 14195ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app4 | ok | 563 | 13219ms | 18987ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app5 | ok | 563 | 13195ms | 18965ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app6 | ok | 298 | 24978ms | 38426ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5538 | 8823ms | 19756ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (42 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2571ms | 4650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2000ms | 3950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app3 | ok | 2000ms | 4200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app4 | ok | 2750ms | 4862ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app5 | ok | 2500ms | 4450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app6 | ok | 800ms | 4850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 7179ms | 9960ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 6714ms | 9662ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app3 | ok | 7846ms | 13583ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app4 | ok | 9600ms | 14450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app5 | ok | 9250ms | 14417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app6 | ok | 10357ms | 14536ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 8167ms | 13125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 6542ms | 9100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app3 | ok | 9600ms | 14393ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app4 | ok | 13833ms | 19281ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app5 | ok | 14615ms | 19455ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app6 | ok | 22500ms | 29250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 8396ms | 9975ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 7067ms | 9675ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app3 | ok | 9211ms | 14083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app4 | ok | 13235ms | 18900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app5 | ok | 13056ms | 18625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app6 | ok | 25500ms | 36750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 8385ms | 9908ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 6938ms | 9120ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app3 | ok | 9409ms | 14205ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app4 | ok | 13000ms | 18500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app5 | ok | 13026ms | 18562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app6 | ok | 28571ms | 43200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 8315ms | 9831ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 6879ms | 8875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app3 | ok | 9304ms | 14056ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app4 | ok | 12895ms | 18167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app5 | ok | 13026ms | 18562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 8327ms | 9902ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 6875ms | 9080ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app3 | ok | 9182ms | 13937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app4 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app5 | ok | 13056ms | 18625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app6 | ok | 26000ms | 40500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 8375ms | 9838ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 6788ms | 7988ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app3 | ok | 9154ms | 13400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app4 | ok | 13026ms | 18562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app5 | ok | 13382ms | 19042ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 8708ms | 13091ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 7032ms | 9300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app3 | ok | 10147ms | 14515ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app4 | ok | 15909ms | 19591ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app5 | ok | 15000ms | 19500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app6 | ok | 25625ms | 38250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 8595ms | 13446ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 6958ms | 10917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app3 | ok | 9625ms | 14446ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app4 | ok | 16167ms | 19617ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app5 | ok | 16167ms | 19617ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app6 | ok | 26875ms | 42250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 8475ms | 13411ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 7080ms | 9544ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app3 | ok | 9438ms | 14327ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app4 | ok | 13158ms | 18800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app5 | ok | 13333ms | 19000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app6 | ok | 28571ms | 43200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 8344ms | 13803ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 7130ms | 9633ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app3 | ok | 9579ms | 14346ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app4 | ok | 13438ms | 19083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app5 | ok | 13594ms | 19179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app6 | ok | 25909ms | 40125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 8364ms | 9836ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 6759ms | 9080ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app3 | ok | 9136ms | 13906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app4 | ok | 13056ms | 18625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app5 | ok | 13438ms | 19083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 8204ms | 9820ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 6767ms | 8875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app3 | ok | 9381ms | 14175ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app4 | ok | 13594ms | 19179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app5 | ok | 13000ms | 18500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 8174ms | 9974ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 6720ms | 9343ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app3 | ok | 9529ms | 14346ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app4 | ok | 13594ms | 19179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app5 | ok | 13056ms | 18625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app6 | ok | 26000ms | 40500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 8184ms | 9818ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 6879ms | 8875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app3 | ok | 9304ms | 14056ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app4 | ok | 12875ms | 18083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app5 | ok | 13382ms | 19042ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 171.0 | app1 | ok | 8192ms | 9819ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 171.0 | app2 | ok | 6833ms | 9100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 171.0 | app3 | ok | 9333ms | 14056ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 171.0 | app4 | ok | 13026ms | 18562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 171.0 | app5 | ok | 13026ms | 18562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 171.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 8152ms | 9893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 6857ms | 9343ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app3 | ok | 9190ms | 14028ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app4 | ok | 13235ms | 18900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app5 | ok | 13235ms | 18900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app6 | ok | 25500ms | 36750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 8364ms | 9836ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 6800ms | 8900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app3 | ok | 9409ms | 14175ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app4 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app5 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app6 | ok | 25455ms | 36000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 8089ms | 9849ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 6826ms | 9500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app3 | ok | 9438ms | 14312ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app4 | ok | 13056ms | 18625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app5 | ok | 13281ms | 18950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app6 | ok | 25556ms | 37500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 8088ms | 13250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 6640ms | 9120ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app3 | ok | 9875ms | 14469ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app4 | ok | 14792ms | 19477ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app5 | ok | 14107ms | 19361ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app6 | ok | 27500ms | 42750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 8267ms | 11250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 7192ms | 9625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app3 | ok | 9318ms | 14083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app4 | ok | 13056ms | 18625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app5 | ok | 13235ms | 18900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app6 | ok | 26667ms | 42000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 8260ms | 9862ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 6900ms | 9250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app3 | ok | 9217ms | 13937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app4 | ok | 13088ms | 18688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app5 | ok | 12875ms | 18083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 8327ms | 9867ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 6909ms | 9080ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app3 | ok | 9545ms | 14292ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app4 | ok | 13833ms | 19281ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app5 | ok | 12750ms | 17250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 8347ms | 9908ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 6880ms | 9240ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app3 | ok | 9400ms | 14250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app4 | ok | 13214ms | 18875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app5 | ok | 13421ms | 19071ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app6 | ok | 26500ms | 41750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app3 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app4 | ok | 12500ms | 17750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app5 | ok | 12500ms | 17500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app6 | ok | 18214ms | 28688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 371.0 | 382.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 382.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 382.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 382.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 382.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 382.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 412.0 | 418.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 418.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 418.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 418.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 418.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 418.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
