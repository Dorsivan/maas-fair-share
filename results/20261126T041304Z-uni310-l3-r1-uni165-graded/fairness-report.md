# Fairness benchmark: six-group-board-case (uni310-l3-r1-uni165-graded)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-748b4c899c-2swrb` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T04:14:15Z` |
| Run end | `2026-11-26T04:23:00Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 54 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/54 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 62.50 | 1.9531 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 40.0 | 75 | 2188 | 000=2, 200=2186 | 8.2 | 10.2 | 2887522.0 | 40.0% | 31.9% | -8.1 | 39.8% | -0.2 | 39.7% | -0.3 | 84.4s | 98.9% | 2188.0 |
| app2 | 20.0 | 32 | 1090 | 200=1090 | 7.1 | 9.0 | 1444564.0 | 20.0% | 13.6% | -6.4 | 19.9% | -0.1 | 19.8% | -0.2 | 84.3s | 98.9% | 1090.0 |
| app3 | 15.0 | 32 | 825 | 200=825 | 9.4 | 11.6 | 1092668.0 | 15.0% | 13.6% | -1.4 | 15.1% | 0.1 | 15.0% | -0.0 | 84.4s | 98.9% | 825.0 |
| app4 | 10.0 | 32 | 559 | 000=1, 200=558 | 13.8 | 16.1 | 720948.0 | 10.0% | 13.6% | 3.6 | 9.9% | -0.1 | 10.1% | 0.1 | 84.5s | 98.9% | 559.0 |
| app5 | 10.0 | 32 | 560 | 200=560 | 14.2 | 16.4 | 727486.0 | 10.0% | 13.6% | 3.6 | 10.0% | 0.0 | 10.1% | 0.1 | 85.5s | 98.9% | 560.0 |
| app6 | 5.0 | 32 | 296 | 200=296 | 28.2 | 31.0 | 376102.0 | 5.0% | 13.6% | 8.6 | 5.2% | 0.2 | 5.4% | 0.4 | 85.5s | 98.9% | 296.0 |
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

**Windows** (53 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 9474.0 | 40.0% | 34.9% | -5.1 |
| 0.0 | 10.0 | app2 | True | False | 10844.0 | 20.0% | 40.0% | 20.0 |
| 0.0 | 10.0 | app3 | True | False | 6790.0 | 15.0% | 25.0% | 10.0 |
| 0.0 | 10.0 | app4 | True | False | 0.0 | 10.0% | 0.0% | -10.0 |
| 0.0 | 10.0 | app5 | True | False | 0.0 | 10.0% | 0.0% | -10.0 |
| 0.0 | 10.0 | app6 | True | False | 0.0 | 5.0% | 0.0% | -5.0 |
| 10.0 | 20.0 | app1 | True | False | 117634.0 | 40.0% | 46.3% | 6.3 |
| 10.0 | 20.0 | app2 | True | False | 58176.0 | 20.0% | 22.9% | 2.9 |
| 10.0 | 20.0 | app3 | True | False | 41944.0 | 15.0% | 16.5% | 1.5 |
| 10.0 | 20.0 | app4 | True | False | 16190.0 | 10.0% | 6.4% | -3.6 |
| 10.0 | 20.0 | app5 | True | False | 18900.0 | 10.0% | 7.4% | -2.6 |
| 10.0 | 20.0 | app6 | True | False | 1358.0 | 5.0% | 0.5% | -4.5 |
| 20.0 | 30.0 | app1 | True | False | 123046.0 | 40.0% | 40.1% | 0.1 |
| 20.0 | 30.0 | app2 | True | False | 60962.0 | 20.0% | 19.9% | -0.1 |
| 20.0 | 30.0 | app3 | True | False | 47404.0 | 15.0% | 15.4% | 0.4 |
| 20.0 | 30.0 | app4 | True | False | 29770.0 | 10.0% | 9.7% | -0.3 |
| 20.0 | 30.0 | app5 | True | False | 31060.0 | 10.0% | 10.1% | 0.1 |
| 20.0 | 30.0 | app6 | True | False | 14834.0 | 5.0% | 4.8% | -0.2 |
| 30.0 | 40.0 | app1 | True | False | 121826.0 | 40.0% | 40.2% | 0.2 |
| 30.0 | 40.0 | app2 | True | False | 60930.0 | 20.0% | 20.1% | 0.1 |
| 30.0 | 40.0 | app3 | True | False | 44714.0 | 15.0% | 14.7% | -0.3 |
| 30.0 | 40.0 | app4 | True | False | 29736.0 | 10.0% | 9.8% | -0.2 |
| 30.0 | 40.0 | app5 | True | False | 31120.0 | 10.0% | 10.3% | 0.3 |
| 30.0 | 40.0 | app6 | True | False | 14864.0 | 5.0% | 4.9% | -0.1 |
| 40.0 | 50.0 | app1 | True | False | 120410.0 | 40.0% | 39.4% | -0.6 |
| 40.0 | 50.0 | app2 | True | False | 60732.0 | 20.0% | 19.9% | -0.1 |
| 40.0 | 50.0 | app3 | True | False | 47334.0 | 15.0% | 15.5% | 0.5 |
| 40.0 | 50.0 | app4 | True | False | 31062.0 | 10.0% | 10.2% | 0.2 |
| 40.0 | 50.0 | app5 | True | False | 29730.0 | 10.0% | 9.7% | -0.3 |
| 40.0 | 50.0 | app6 | True | False | 16254.0 | 5.0% | 5.3% | 0.3 |
| 50.0 | 60.0 | app1 | True | False | 123102.0 | 40.0% | 40.1% | 0.1 |
| 50.0 | 60.0 | app2 | True | False | 62264.0 | 20.0% | 20.3% | 0.3 |
| 50.0 | 60.0 | app3 | True | False | 46014.0 | 15.0% | 15.0% | -0.0 |
| 50.0 | 60.0 | app4 | True | False | 29750.0 | 10.0% | 9.7% | -0.3 |
| 50.0 | 60.0 | app5 | True | False | 31058.0 | 10.0% | 10.1% | 0.1 |
| 50.0 | 60.0 | app6 | True | False | 14926.0 | 5.0% | 4.9% | -0.1 |
| 60.0 | 70.0 | app1 | True | False | 120338.0 | 40.0% | 39.9% | -0.1 |
| 60.0 | 70.0 | app2 | True | False | 59626.0 | 20.0% | 19.8% | -0.2 |
| 60.0 | 70.0 | app3 | True | False | 45940.0 | 15.0% | 15.2% | 0.2 |
| 60.0 | 70.0 | app4 | True | False | 29808.0 | 10.0% | 9.9% | -0.1 |
| 60.0 | 70.0 | app5 | True | False | 31142.0 | 10.0% | 10.3% | 0.3 |
| 60.0 | 70.0 | app6 | True | False | 14924.0 | 5.0% | 4.9% | -0.1 |
| 70.0 | 80.0 | app1 | True | False | 121698.0 | 40.0% | 39.8% | -0.2 |
| 70.0 | 80.0 | app2 | True | False | 62174.0 | 20.0% | 20.3% | 0.3 |
| 70.0 | 80.0 | app3 | True | False | 45996.0 | 15.0% | 15.0% | 0.0 |
| 70.0 | 80.0 | app4 | True | False | 31106.0 | 10.0% | 10.2% | 0.2 |
| 70.0 | 80.0 | app5 | True | False | 28456.0 | 10.0% | 9.3% | -0.7 |
| 70.0 | 80.0 | app6 | True | False | 16270.0 | 5.0% | 5.3% | 0.3 |
| 80.0 | 90.0 | app1 | True | False | 122942.0 | 40.0% | 40.4% | 0.4 |
| 80.0 | 90.0 | app2 | True | False | 60808.0 | 20.0% | 20.0% | -0.0 |
| 80.0 | 90.0 | app3 | True | False | 47332.0 | 15.0% | 15.6% | 0.6 |
| 80.0 | 90.0 | app4 | True | False | 29786.0 | 10.0% | 9.8% | -0.2 |
| 80.0 | 90.0 | app5 | True | False | 29756.0 | 10.0% | 9.8% | -0.2 |
| 80.0 | 90.0 | app6 | True | False | 13560.0 | 5.0% | 4.5% | -0.5 |
| 90.0 | 100.0 | app1 | True | False | 121692.0 | 40.0% | 39.8% | -0.2 |
| 90.0 | 100.0 | app2 | True | False | 59516.0 | 20.0% | 19.5% | -0.5 |
| 90.0 | 100.0 | app3 | True | False | 44624.0 | 15.0% | 14.6% | -0.4 |
| 90.0 | 100.0 | app4 | True | False | 31042.0 | 10.0% | 10.2% | 0.2 |
| 90.0 | 100.0 | app5 | True | False | 33778.0 | 10.0% | 11.1% | 1.1 |
| 90.0 | 100.0 | app6 | True | False | 14854.0 | 5.0% | 4.9% | -0.1 |
| 100.0 | 110.0 | app1 | True | False | 106920.0 | 40.0% | 41.6% | 1.6 |
| 100.0 | 110.0 | app2 | True | False | 55468.0 | 20.0% | 21.6% | 1.6 |
| 100.0 | 110.0 | app3 | True | False | 39228.0 | 15.0% | 15.3% | 0.3 |
| 100.0 | 110.0 | app4 | True | False | 21606.0 | 10.0% | 8.4% | -1.6 |
| 100.0 | 110.0 | app5 | True | False | 21628.0 | 10.0% | 8.4% | -1.6 |
| 100.0 | 110.0 | app6 | True | False | 12168.0 | 5.0% | 4.7% | -0.3 |
| 110.0 | 120.0 | app1 | True | False | 118970.0 | 40.0% | 38.8% | -1.2 |
| 110.0 | 120.0 | app2 | True | False | 58088.0 | 20.0% | 18.9% | -1.1 |
| 110.0 | 120.0 | app3 | True | False | 44664.0 | 15.0% | 14.6% | -0.4 |
| 110.0 | 120.0 | app4 | True | False | 33868.0 | 10.0% | 11.0% | 1.0 |
| 110.0 | 120.0 | app5 | True | False | 33830.0 | 10.0% | 11.0% | 1.0 |
| 110.0 | 120.0 | app6 | True | False | 17514.0 | 5.0% | 5.7% | 0.7 |
| 120.0 | 130.0 | app1 | True | False | 119010.0 | 40.0% | 40.0% | -0.0 |
| 120.0 | 130.0 | app2 | True | False | 59556.0 | 20.0% | 20.0% | 0.0 |
| 120.0 | 130.0 | app3 | True | False | 44716.0 | 15.0% | 15.0% | 0.0 |
| 120.0 | 130.0 | app4 | True | False | 31104.0 | 10.0% | 10.5% | 0.5 |
| 120.0 | 130.0 | app5 | True | False | 29738.0 | 10.0% | 10.0% | -0.0 |
| 120.0 | 130.0 | app6 | True | False | 13472.0 | 5.0% | 4.5% | -0.5 |
| 130.0 | 141.0 | app1 | True | False | 121854.0 | 40.0% | 39.7% | -0.3 |
| 130.0 | 141.0 | app2 | True | False | 62216.0 | 20.0% | 20.3% | 0.3 |
| 130.0 | 141.0 | app3 | True | False | 44538.0 | 15.0% | 14.5% | -0.5 |
| 130.0 | 141.0 | app4 | True | False | 31048.0 | 10.0% | 10.1% | 0.1 |
| 130.0 | 141.0 | app5 | True | False | 31108.0 | 10.0% | 10.1% | 0.1 |
| 130.0 | 141.0 | app6 | True | False | 16198.0 | 5.0% | 5.3% | 0.3 |
| 141.0 | 151.0 | app1 | True | False | 121694.0 | 40.0% | 40.0% | -0.0 |
| 141.0 | 151.0 | app2 | True | False | 60918.0 | 20.0% | 20.0% | 0.0 |
| 141.0 | 151.0 | app3 | True | False | 47288.0 | 15.0% | 15.5% | 0.5 |
| 141.0 | 151.0 | app4 | True | False | 29810.0 | 10.0% | 9.8% | -0.2 |
| 141.0 | 151.0 | app5 | True | False | 29694.0 | 10.0% | 9.8% | -0.2 |
| 141.0 | 151.0 | app6 | True | False | 14858.0 | 5.0% | 4.9% | -0.1 |
| 151.0 | 161.0 | app1 | True | False | 121772.0 | 40.0% | 39.8% | -0.2 |
| 151.0 | 161.0 | app2 | True | False | 60848.0 | 20.0% | 19.9% | -0.1 |
| 151.0 | 161.0 | app3 | True | False | 46014.0 | 15.0% | 15.0% | 0.0 |
| 151.0 | 161.0 | app4 | True | False | 31142.0 | 10.0% | 10.2% | 0.2 |
| 151.0 | 161.0 | app5 | True | False | 31098.0 | 10.0% | 10.2% | 0.2 |
| 151.0 | 161.0 | app6 | True | False | 14898.0 | 5.0% | 4.9% | -0.1 |
| 161.0 | 171.0 | app1 | True | False | 119170.0 | 40.0% | 40.4% | 0.4 |
| 161.0 | 171.0 | app2 | True | False | 58188.0 | 20.0% | 19.7% | -0.3 |
| 161.0 | 171.0 | app3 | True | False | 43302.0 | 15.0% | 14.7% | -0.3 |
| 161.0 | 171.0 | app4 | True | False | 28440.0 | 10.0% | 9.6% | -0.4 |
| 161.0 | 171.0 | app5 | True | False | 29812.0 | 10.0% | 10.1% | 0.1 |
| 161.0 | 171.0 | app6 | True | False | 16258.0 | 5.0% | 5.5% | 0.5 |
| 171.0 | 181.0 | app1 | True | False | 117724.0 | 40.0% | 39.4% | -0.6 |
| 171.0 | 181.0 | app2 | True | False | 63546.0 | 20.0% | 21.3% | 1.3 |
| 171.0 | 181.0 | app3 | True | False | 44570.0 | 15.0% | 14.9% | -0.1 |
| 171.0 | 181.0 | app4 | True | False | 29786.0 | 10.0% | 10.0% | -0.0 |
| 171.0 | 181.0 | app5 | True | False | 29790.0 | 10.0% | 10.0% | -0.0 |
| 171.0 | 181.0 | app6 | True | False | 13536.0 | 5.0% | 4.5% | -0.5 |
| 181.0 | 191.0 | app1 | True | False | 122976.0 | 40.0% | 40.6% | 0.6 |
| 181.0 | 191.0 | app2 | True | False | 58160.0 | 20.0% | 19.2% | -0.8 |
| 181.0 | 191.0 | app3 | True | False | 47340.0 | 15.0% | 15.6% | 0.6 |
| 181.0 | 191.0 | app4 | True | False | 29746.0 | 10.0% | 9.8% | -0.2 |
| 181.0 | 191.0 | app5 | True | False | 29692.0 | 10.0% | 9.8% | -0.2 |
| 181.0 | 191.0 | app6 | True | False | 14904.0 | 5.0% | 4.9% | -0.1 |
| 191.0 | 201.0 | app1 | True | False | 121692.0 | 40.0% | 39.8% | -0.2 |
| 191.0 | 201.0 | app2 | True | False | 60820.0 | 20.0% | 19.9% | -0.1 |
| 191.0 | 201.0 | app3 | True | False | 44670.0 | 15.0% | 14.6% | -0.4 |
| 191.0 | 201.0 | app4 | True | False | 31090.0 | 10.0% | 10.2% | 0.2 |
| 191.0 | 201.0 | app5 | True | False | 31126.0 | 10.0% | 10.2% | 0.2 |
| 191.0 | 201.0 | app6 | True | False | 16206.0 | 5.0% | 5.3% | 0.3 |
| 201.0 | 211.0 | app1 | True | False | 121714.0 | 40.0% | 39.8% | -0.2 |
| 201.0 | 211.0 | app2 | True | False | 60788.0 | 20.0% | 19.9% | -0.1 |
| 201.0 | 211.0 | app3 | True | False | 45848.0 | 15.0% | 15.0% | 0.0 |
| 201.0 | 211.0 | app4 | True | False | 31142.0 | 10.0% | 10.2% | 0.2 |
| 201.0 | 211.0 | app5 | True | False | 29746.0 | 10.0% | 9.7% | -0.3 |
| 201.0 | 211.0 | app6 | True | False | 16254.0 | 5.0% | 5.3% | 0.3 |
| 211.0 | 221.0 | app1 | True | False | 121698.0 | 40.0% | 39.7% | -0.3 |
| 211.0 | 221.0 | app2 | True | False | 62234.0 | 20.0% | 20.3% | 0.3 |
| 211.0 | 221.0 | app3 | True | False | 45876.0 | 15.0% | 15.0% | -0.0 |
| 211.0 | 221.0 | app4 | True | False | 31056.0 | 10.0% | 10.1% | 0.1 |
| 211.0 | 221.0 | app5 | True | False | 31094.0 | 10.0% | 10.1% | 0.1 |
| 211.0 | 221.0 | app6 | True | False | 14878.0 | 5.0% | 4.8% | -0.2 |
| 221.0 | 231.0 | app1 | True | False | 122956.0 | 40.0% | 40.4% | 0.4 |
| 221.0 | 231.0 | app2 | True | False | 60878.0 | 20.0% | 20.0% | 0.0 |
| 221.0 | 231.0 | app3 | True | False | 46004.0 | 15.0% | 15.1% | 0.1 |
| 221.0 | 231.0 | app4 | True | False | 29748.0 | 10.0% | 9.8% | -0.2 |
| 221.0 | 231.0 | app5 | True | False | 29782.0 | 10.0% | 9.8% | -0.2 |
| 221.0 | 231.0 | app6 | True | False | 14872.0 | 5.0% | 4.9% | -0.1 |
| 231.0 | 241.0 | app1 | True | False | 121752.0 | 40.0% | 39.8% | -0.2 |
| 231.0 | 241.0 | app2 | True | False | 60808.0 | 20.0% | 19.9% | -0.1 |
| 231.0 | 241.0 | app3 | True | False | 45992.0 | 15.0% | 15.0% | 0.0 |
| 231.0 | 241.0 | app4 | True | False | 31154.0 | 10.0% | 10.2% | 0.2 |
| 231.0 | 241.0 | app5 | True | False | 31120.0 | 10.0% | 10.2% | 0.2 |
| 231.0 | 241.0 | app6 | True | False | 14902.0 | 5.0% | 4.9% | -0.1 |
| 241.0 | 251.0 | app1 | False | n/a | 105458.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 46016.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | n/a | 44526.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app4 | False | n/a | 37884.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app5 | False | n/a | 39156.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app6 | False | n/a | 28448.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | False | n/a | 4074.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | False | n/a | 4072.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | False | n/a | 14892.0 | n/a | n/a | n/a |
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
| 351.0 | 362.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 362.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 362.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 362.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 362.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 362.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
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
| 522.0 | 525.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 525.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 525.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 525.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 525.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 525.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 87 | 0ms | 4275ms | 4928ms |
| 0.0 | 10.0 | app2 | ok | 44 | 0ms | 4000ms | 4900ms |
| 0.0 | 10.0 | app3 | ok | 33 | 2574ms | 4515ms | 4951ms |
| 0.0 | 10.0 | app4 | ok | 25 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app5 | ok | 22 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app6 | ok | 18 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 99 | 3574ms | 4738ms | 5050ms |
| 10.0 | 20.0 | app2 | ok | 50 | 2596ms | 4519ms | 4952ms |
| 10.0 | 20.0 | app3 | ok | 37 | 4511ms | 8679ms | 9868ms |
| 10.0 | 20.0 | app4 | ok | 22 | 7895ms | 15333ms | 28533ms |
| 10.0 | 20.0 | app5 | ok | 25 | 7604ms | 9688ms | 25000ms |
| 10.0 | 20.0 | app6 | ok | 6 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app1 | ok | 108 | 3430ms | 4686ms | 4969ms |
| 20.0 | 30.0 | app2 | ok | 54 | 2080ms | 4325ms | 4932ms |
| 20.0 | 30.0 | app3 | ok | 41 | 4208ms | 8136ms | 9814ms |
| 20.0 | 30.0 | app4 | ok | 27 | 7700ms | 9860ms | 27300ms |
| 20.0 | 30.0 | app5 | ok | 27 | 8214ms | 21000ms | 29100ms |
| 20.0 | 30.0 | app6 | ok | 13 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | app1 | ok | 75 | 3535ms | 4707ms | 4971ms |
| 30.0 | 40.0 | app2 | ok | 37 | 2145ms | 4339ms | 4934ms |
| 30.0 | 40.0 | app3 | ok | 27 | 4188ms | 8071ms | 9807ms |
| 30.0 | 40.0 | app4 | ok | 19 | 8167ms | 20500ms | 29050ms |
| 30.0 | 40.0 | app5 | ok | 19 | 8958ms | 24571ms | 29457ms |
| 30.0 | 40.0 | app6 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app1 | ok | 96 | 3500ms | 4700ms | 4970ms |
| 40.0 | 50.0 | app2 | ok | 48 | 2167ms | 4333ms | 4933ms |
| 40.0 | 50.0 | app3 | ok | 37 | 4350ms | 8458ms | 9846ms |
| 40.0 | 50.0 | app4 | ok | 23 | 8594ms | 23429ms | 29343ms |
| 40.0 | 50.0 | app5 | ok | 23 | 8194ms | 20800ms | 29080ms |
| 40.0 | 50.0 | app6 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app1 | ok | 81 | 3254ms | 4651ms | 4965ms |
| 50.0 | 60.0 | app2 | ok | 41 | 2066ms | 4317ms | 4932ms |
| 50.0 | 60.0 | app3 | ok | 30 | 4375ms | 8500ms | 9850ms |
| 50.0 | 60.0 | app4 | ok | 22 | 7895ms | 15333ms | 28533ms |
| 50.0 | 60.0 | app5 | ok | 22 | 8235ms | 21200ms | 29120ms |
| 50.0 | 60.0 | app6 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app1 | ok | 103 | 3467ms | 4693ms | 4969ms |
| 60.0 | 70.0 | app2 | ok | 52 | 2125ms | 4316ms | 4932ms |
| 60.0 | 70.0 | app3 | ok | 40 | 4500ms | 8667ms | 9867ms |
| 60.0 | 70.0 | app4 | ok | 24 | 7857ms | 14000ms | 28400ms |
| 60.0 | 70.0 | app5 | ok | 25 | 8125ms | 20000ms | 29000ms |
| 60.0 | 70.0 | app6 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app1 | ok | 86 | 3238ms | 4648ms | 4965ms |
| 70.0 | 80.0 | app2 | ok | 42 | 1975ms | 4250ms | 4925ms |
| 70.0 | 80.0 | app3 | ok | 31 | 4188ms | 8278ms | 9828ms |
| 70.0 | 80.0 | app4 | ok | 22 | 7895ms | 15333ms | 28533ms |
| 70.0 | 80.0 | app5 | ok | 22 | 8235ms | 21200ms | 29120ms |
| 70.0 | 80.0 | app6 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app1 | ok | 94 | 3074ms | 4615ms | 4961ms |
| 80.0 | 90.0 | app2 | ok | 42 | 2125ms | 4344ms | 4934ms |
| 80.0 | 90.0 | app3 | ok | 35 | 4148ms | 8250ms | 9825ms |
| 80.0 | 90.0 | app4 | ok | 23 | 7738ms | 9929ms | 27700ms |
| 80.0 | 90.0 | app5 | ok | 22 | 7895ms | 15333ms | 28533ms |
| 80.0 | 90.0 | app6 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app1 | ok | 90 | 2955ms | 4591ms | 4959ms |
| 90.0 | 100.0 | app2 | ok | 46 | 2333ms | 4452ms | 4945ms |
| 90.0 | 100.0 | app3 | ok | 39 | 3897ms | 8375ms | 9837ms |
| 90.0 | 100.0 | app4 | ok | 33 | 6705ms | 9705ms | 26700ms |
| 90.0 | 100.0 | app5 | ok | 33 | 7024ms | 13500ms | 28350ms |
| 90.0 | 100.0 | app6 | ok | 16 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app1 | ok | 64 | 5152ms | 9030ms | 9903ms |
| 100.0 | 110.0 | app2 | ok | 36 | 3824ms | 8200ms | 9820ms |
| 100.0 | 110.0 | app3 | ok | 18 | 7188ms | 9438ms | 9944ms |
| 100.0 | 110.0 | app4 | ok | 7 | 9375ms | 25333ms | 29533ms |
| 100.0 | 110.0 | app5 | ok | 6 | 15000ms | 27000ms | 29700ms |
| 100.0 | 110.0 | app6 | ok | 3 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app1 | ok | 99 | 3173ms | 4696ms | 7525ms |
| 110.0 | 120.0 | app2 | ok | 44 | 2324ms | 4450ms | 4945ms |
| 110.0 | 120.0 | app3 | ok | 42 | 3700ms | 7375ms | 9737ms |
| 110.0 | 120.0 | app4 | ok | 28 | 7941ms | 22000ms | 29200ms |
| 110.0 | 120.0 | app5 | ok | 30 | 8529ms | 24000ms | 29400ms |
| 110.0 | 120.0 | app6 | ok | 15 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app1 | ok | 77 | 3585ms | 4717ms | 4972ms |
| 120.0 | 130.0 | app2 | ok | 43 | 3050ms | 4770ms | 8925ms |
| 120.0 | 130.0 | app3 | ok | 25 | 4712ms | 8864ms | 9886ms |
| 120.0 | 130.0 | app4 | ok | 15 | 7679ms | 9821ms | 27000ms |
| 120.0 | 130.0 | app5 | ok | 14 | 8182ms | 20667ms | 29067ms |
| 120.0 | 130.0 | app6 | ok | 7 | 20000ms | 28000ms | 29800ms |
| 130.0 | 141.0 | app1 | ok | 93 | 3315ms | 4663ms | 4966ms |
| 130.0 | 141.0 | app2 | ok | 47 | 2145ms | 4382ms | 4938ms |
| 130.0 | 141.0 | app3 | ok | 35 | 4219ms | 8250ms | 9825ms |
| 130.0 | 141.0 | app4 | ok | 23 | 7738ms | 9929ms | 27700ms |
| 130.0 | 141.0 | app5 | ok | 25 | 7976ms | 17500ms | 28750ms |
| 130.0 | 141.0 | app6 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 141.0 | 151.0 | app1 | ok | 86 | 3396ms | 4679ms | 4968ms |
| 141.0 | 151.0 | app2 | ok | 45 | 2193ms | 4375ms | 4938ms |
| 141.0 | 151.0 | app3 | ok | 32 | 4239ms | 8222ms | 9822ms |
| 141.0 | 151.0 | app4 | ok | 22 | 7895ms | 15333ms | 28533ms |
| 141.0 | 151.0 | app5 | ok | 20 | 8333ms | 22000ms | 29200ms |
| 141.0 | 151.0 | app6 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 151.0 | 161.0 | app1 | ok | 112 | 3205ms | 4641ms | 4964ms |
| 151.0 | 161.0 | app2 | ok | 54 | 1879ms | 4100ms | 4910ms |
| 151.0 | 161.0 | app3 | ok | 42 | 4310ms | 8385ms | 9838ms |
| 151.0 | 161.0 | app4 | ok | 28 | 8043ms | 18800ms | 28880ms |
| 151.0 | 161.0 | app5 | ok | 28 | 7917ms | 16000ms | 28600ms |
| 151.0 | 161.0 | app6 | ok | 14 | 20000ms | 28000ms | 29800ms |
| 161.0 | 171.0 | app1 | ok | 79 | 3411ms | 4750ms | 8025ms |
| 161.0 | 171.0 | app2 | ok | 40 | 2324ms | 4444ms | 4944ms |
| 161.0 | 171.0 | app3 | ok | 30 | 4559ms | 8750ms | 9875ms |
| 161.0 | 171.0 | app4 | ok | 19 | 8393ms | 22400ms | 29240ms |
| 161.0 | 171.0 | app5 | ok | 21 | 8500ms | 23000ms | 29300ms |
| 161.0 | 171.0 | app6 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 171.0 | 181.0 | app1 | ok | 72 | 2750ms | 4550ms | 4955ms |
| 171.0 | 181.0 | app2 | ok | 37 | 2172ms | 4383ms | 4938ms |
| 171.0 | 181.0 | app3 | ok | 27 | 3897ms | 7750ms | 9775ms |
| 171.0 | 181.0 | app4 | ok | 19 | 7794ms | 11000ms | 28100ms |
| 171.0 | 181.0 | app5 | ok | 17 | 8542ms | 23200ms | 29320ms |
| 171.0 | 181.0 | app6 | ok | 8 | 20000ms | 28000ms | 29800ms |
| 181.0 | 191.0 | app1 | ok | 97 | 3484ms | 4697ms | 4970ms |
| 181.0 | 191.0 | app2 | ok | 48 | 2260ms | 4400ms | 4940ms |
| 181.0 | 191.0 | app3 | ok | 36 | 4457ms | 8615ms | 9862ms |
| 181.0 | 191.0 | app4 | ok | 24 | 7727ms | 9909ms | 27600ms |
| 181.0 | 191.0 | app5 | ok | 24 | 8158ms | 20400ms | 29040ms |
| 181.0 | 191.0 | app6 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 191.0 | 201.0 | app1 | ok | 97 | 3446ms | 4689ms | 4969ms |
| 191.0 | 201.0 | app2 | ok | 48 | 2188ms | 4368ms | 4937ms |
| 191.0 | 201.0 | app3 | ok | 37 | 4350ms | 8458ms | 9846ms |
| 191.0 | 201.0 | app4 | ok | 24 | 7500ms | 9500ms | 9950ms |
| 191.0 | 201.0 | app5 | ok | 25 | 8676ms | 23750ms | 29375ms |
| 191.0 | 201.0 | app6 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 201.0 | 211.0 | app1 | ok | 85 | 3136ms | 4627ms | 4963ms |
| 201.0 | 211.0 | app2 | ok | 44 | 2000ms | 4267ms | 4927ms |
| 201.0 | 211.0 | app3 | ok | 31 | 3920ms | 7417ms | 9742ms |
| 201.0 | 211.0 | app4 | ok | 21 | 7763ms | 9974ms | 27900ms |
| 201.0 | 211.0 | app5 | ok | 21 | 8088ms | 19500ms | 28950ms |
| 201.0 | 211.0 | app6 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app1 | ok | 91 | 3560ms | 4712ms | 4971ms |
| 211.0 | 221.0 | app2 | ok | 44 | 2239ms | 4389ms | 4939ms |
| 211.0 | 221.0 | app3 | ok | 35 | 4323ms | 8409ms | 9841ms |
| 211.0 | 221.0 | app4 | ok | 23 | 7500ms | 9500ms | 9950ms |
| 211.0 | 221.0 | app5 | ok | 22 | 8438ms | 22667ms | 29267ms |
| 211.0 | 221.0 | app6 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app1 | ok | 85 | 3168ms | 4634ms | 4963ms |
| 221.0 | 231.0 | app2 | ok | 42 | 2000ms | 4250ms | 4925ms |
| 221.0 | 231.0 | app3 | ok | 31 | 4345ms | 8450ms | 9845ms |
| 221.0 | 231.0 | app4 | ok | 21 | 7763ms | 9974ms | 27900ms |
| 221.0 | 231.0 | app5 | ok | 21 | 8500ms | 23000ms | 29300ms |
| 221.0 | 231.0 | app6 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 231.0 | 241.0 | app1 | ok | 92 | 3403ms | 4681ms | 4968ms |
| 231.0 | 241.0 | app2 | ok | 47 | 2306ms | 4413ms | 4941ms |
| 231.0 | 241.0 | app3 | ok | 35 | 4688ms | 8833ms | 9883ms |
| 231.0 | 241.0 | app4 | ok | 24 | 7727ms | 9909ms | 27600ms |
| 231.0 | 241.0 | app5 | ok | 24 | 8750ms | 24000ms | 29400ms |
| 231.0 | 241.0 | app6 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | app1 | ok | 40 | 3387ms | 4677ms | 4968ms |
| 241.0 | 251.0 | app2 | ok | 15 | 2125ms | 4375ms | 4938ms |
| 241.0 | 251.0 | app3 | ok | 19 | 4875ms | 8944ms | 9894ms |
| 241.0 | 251.0 | app4 | ok | 21 | 7344ms | 9969ms | 27900ms |
| 241.0 | 251.0 | app5 | ok | 22 | 7778ms | 15333ms | 28533ms |
| 241.0 | 251.0 | app6 | ok | 27 | 18261ms | 27652ms | 29765ms |
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
| 351.0 | 362.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 362.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 362.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 362.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 362.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 362.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 522.0 | 525.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 525.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 525.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 525.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 525.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 525.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2688780 | 133858 | 2822638.0 | 0.0% | 2887522.0 | 2956496.0 | -2.3% | True |
| app2 | 1340700 | 66814 | 1407514.0 | 0.0% | 1444564.0 | 1474328.0 | -2.0% | True |
| app3 | 1014750 | 50479 | 1065229.0 | 0.0% | 1092668.0 | 1115708.0 | -2.1% | True |
| app4 | 686340 | 34232 | 720572.0 | 0.0% | 720948.0 | 754804.0 | -4.5% | True |
| app5 | 688800 | 34204 | 723004.0 | 0.0% | 727486.0 | 757208.0 | -3.9% | True |
| app6 | 364080 | 18171 | 382251.0 | 0.0% | 376102.0 | 400422.0 | -6.1% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2188 | 0 | 0 | 0 (never shed) | 0.00% | 40.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1090 | 0 | 0 | 0 (never shed) | 0.00% | 20.0% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 825 | 0 | 0 | 0 (never shed) | 0.00% | 15.0% | n/a (nothing shed) | n/a (nothing shed) |
| app4 | 559 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| app5 | 560 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| app6 | 296 | 0 | 0 | 0 (never shed) | 0.00% | 5.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5518). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5518 | 0.051ms | 0.114ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 493369 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 2186 | 8243ms | 11205ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1090 | 7055ms | 9570ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app3 | ok | 825 | 9343ms | 14225ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app4 | ok | 558 | 12977ms | 18671ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app5 | ok | 560 | 13273ms | 19041ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app6 | ok | 296 | 25185ms | 39955ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5515 | 8880ms | 19701ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (53 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2500ms | 4893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 3000ms | 4944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app3 | ok | 3125ms | 4992ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app4 | ok | 2600ms | 3850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app5 | ok | 2375ms | 5350ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app6 | ok | 2750ms | 5650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 7558ms | 9736ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 6906ms | 8925ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app3 | ok | 8706ms | 13400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app4 | ok | 10536ms | 14554ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app5 | ok | 9750ms | 14477ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app6 | ok | 10417ms | 14542ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 8265ms | 9937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 7147ms | 9438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app3 | ok | 9350ms | 14205ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app4 | ok | 12895ms | 18167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app5 | ok | 13382ms | 19042ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app6 | ok | 20000ms | 29000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 8333ms | 10500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 7065ms | 9438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app3 | ok | 9450ms | 14250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app4 | ok | 12750ms | 17250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app5 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 8333ms | 9904ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 6885ms | 9438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app3 | ok | 9000ms | 13750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app4 | ok | 13382ms | 19042ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app5 | ok | 13056ms | 18625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 8283ms | 9828ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 7056ms | 9233ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app3 | ok | 9304ms | 14056ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app4 | ok | 13056ms | 18625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app5 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 8167ms | 11292ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 7154ms | 9600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app3 | ok | 9429ms | 14227ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app4 | ok | 13056ms | 18625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app5 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app6 | ok | 26111ms | 40875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 8200ms | 9820ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 7133ms | 9540ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app3 | ok | 9455ms | 14227ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app4 | ok | 12738ms | 17125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app5 | ok | 13088ms | 18688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app6 | ok | 26000ms | 40500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 8220ms | 12472ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 6840ms | 9438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app3 | ok | 9125ms | 14150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app4 | ok | 12895ms | 18167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app5 | ok | 13667ms | 19214ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 8478ms | 12750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 7111ms | 9560ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app3 | ok | 9556ms | 14346ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app4 | ok | 13382ms | 19042ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app5 | ok | 13676ms | 19219ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app6 | ok | 26111ms | 40875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 9000ms | 13589ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 7519ms | 9707ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app3 | ok | 11848ms | 14685ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app4 | ok | 15000ms | 19500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app5 | ok | 15000ms | 19500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app6 | ok | 29000ms | 43312ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 8774ms | 14120ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 7353ms | 9979ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app3 | ok | 9000ms | 14411ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app4 | ok | 16324ms | 19632ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app5 | ok | 16324ms | 19632ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app6 | ok | 32812ms | 43781ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 8061ms | 13167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 6909ms | 9733ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app3 | ok | 9824ms | 14450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app4 | ok | 13382ms | 19042ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app5 | ok | 15000ms | 19500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app6 | ok | 34286ms | 43929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 141.0 | app1 | ok | 8440ms | 11250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 141.0 | app2 | ok | 7391ms | 9712ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 141.0 | app3 | ok | 9450ms | 14250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 141.0 | app4 | ok | 13026ms | 18562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 141.0 | app5 | ok | 13833ms | 19281ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 141.0 | app6 | ok | 26667ms | 42000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 8150ms | 12188ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 7042ms | 9591ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app3 | ok | 9211ms | 14125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app4 | ok | 12750ms | 17250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app5 | ok | 13235ms | 18900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app6 | ok | 25500ms | 36750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 8311ms | 11786ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 7233ms | 9591ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app3 | ok | 9333ms | 14150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app4 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app5 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app6 | ok | 25500ms | 36750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 8340ms | 10600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 6964ms | 9386ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app3 | ok | 9647ms | 14385ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app4 | ok | 12917ms | 18250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app5 | ok | 13438ms | 19083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app6 | ok | 26000ms | 40500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 8394ms | 13721ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 7050ms | 9942ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app3 | ok | 9929ms | 14484ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app4 | ok | 13929ms | 19312ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app5 | ok | 14231ms | 19389ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app6 | ok | 27143ms | 42500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 8109ms | 9889ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 7250ms | 9609ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app3 | ok | 9136ms | 13906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app4 | ok | 12895ms | 18167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app5 | ok | 13235ms | 18900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app6 | ok | 26111ms | 40875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 8333ms | 9833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 7121ms | 9438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app3 | ok | 9292ms | 13969ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app4 | ok | 12738ms | 17125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app5 | ok | 12875ms | 18083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app6 | ok | 26000ms | 40500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 8250ms | 12750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 7000ms | 9625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app3 | ok | 9429ms | 14346ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app4 | ok | 13594ms | 19179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app5 | ok | 13235ms | 18900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app6 | ok | 26000ms | 40500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 8280ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 7000ms | 9233ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app3 | ok | 9091ms | 13786ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app4 | ok | 12875ms | 18083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app5 | ok | 13382ms | 19042ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 8180ms | 9818ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 7065ms | 9438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app3 | ok | 9333ms | 14056ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app4 | ok | 12750ms | 17250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app5 | ok | 13235ms | 18900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app6 | ok | 26250ms | 41250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 8400ms | 9873ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 7033ms | 9438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app3 | ok | 9304ms | 14056ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app4 | ok | 12738ms | 17125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app5 | ok | 13026ms | 18562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 8000ms | 9800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 7333ms | 9660ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app3 | ok | 9550ms | 14312ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app4 | ok | 12800ms | 17667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app5 | ok | 12935ms | 18550ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app6 | ok | 24412ms | 29971ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app4 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app5 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app6 | ok | 14583ms | 27250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 351.0 | 362.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 362.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 362.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 362.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 362.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 362.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 522.0 | 525.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 525.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 525.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 525.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 525.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 525.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
