# Fairness benchmark: six-group-board-case (uni310-l2-r1-uni165-equal)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 0.0 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 0.0 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

## Run metadata

| field | value |
|---|---|
| Scenario | `six-group-board-case` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-79f9bbd5f9-q6w69` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T05:06:14Z` |
| Run end | `2026-11-26T05:15:20Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 56 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/56 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 83.50 | 2.6094 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 16.7 | 32 | 919 | 200=919 | 8.4 | 10.7 | 1207514.0 | 16.7% | 16.7% | 0.0 | 16.7% | -0.0 | 16.7% | 0.0 | 78.4s | 98.9% | 919.0 |
| app2 | 16.7 | 32 | 914 | 000=4, 200=910 | 8.2 | 10.4 | 1197022.0 | 16.7% | 16.7% | 0.0 | 16.5% | -0.1 | 16.6% | -0.1 | 78.3s | 98.9% | 914.0 |
| app3 | 16.7 | 32 | 917 | 000=2, 200=915 | 8.3 | 10.6 | 1210180.0 | 16.7% | 16.7% | 0.0 | 16.7% | 0.0 | 16.7% | -0.0 | 78.4s | 98.9% | 917.0 |
| app4 | 16.7 | 32 | 918 | 000=1, 200=917 | 8.3 | 10.5 | 1205072.0 | 16.7% | 16.7% | 0.0 | 16.6% | -0.0 | 16.7% | 0.0 | 78.4s | 98.9% | 918.0 |
| app5 | 16.7 | 32 | 917 | 000=2, 200=915 | 8.5 | 10.7 | 1209036.0 | 16.7% | 16.7% | 0.0 | 16.7% | 0.0 | 16.7% | -0.0 | 78.4s | 98.9% | 917.0 |
| app6 | 16.7 | 32 | 919 | 200=919 | 8.4 | 10.7 | 1216790.0 | 16.7% | 16.7% | 0.0 | 16.8% | 0.1 | 16.7% | 0.0 | 78.4s | 98.9% | 919.0 |
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

**Windows** (55 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app2 | True | False | 2712.0 | 16.7% | 18.2% | 1.5 |
| 0.0 | 10.0 | app3 | True | False | 4072.0 | 16.7% | 27.3% | 10.6 |
| 0.0 | 10.0 | app4 | True | False | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app5 | True | False | 2716.0 | 16.7% | 18.2% | 1.5 |
| 0.0 | 10.0 | app6 | True | False | 5432.0 | 16.7% | 36.4% | 19.7 |
| 10.0 | 20.0 | app1 | True | False | 43240.0 | 16.7% | 15.2% | -1.4 |
| 10.0 | 20.0 | app2 | True | False | 48768.0 | 16.7% | 17.2% | 0.5 |
| 10.0 | 20.0 | app3 | True | False | 48656.0 | 16.7% | 17.1% | 0.5 |
| 10.0 | 20.0 | app4 | True | False | 47342.0 | 16.7% | 16.7% | 0.0 |
| 10.0 | 20.0 | app5 | True | False | 47328.0 | 16.7% | 16.7% | 0.0 |
| 10.0 | 20.0 | app6 | True | False | 48578.0 | 16.7% | 17.1% | 0.4 |
| 20.0 | 30.0 | app1 | True | False | 51380.0 | 16.7% | 17.3% | 0.6 |
| 20.0 | 30.0 | app2 | True | False | 50094.0 | 16.7% | 16.8% | 0.2 |
| 20.0 | 30.0 | app3 | True | False | 48666.0 | 16.7% | 16.4% | -0.3 |
| 20.0 | 30.0 | app4 | True | False | 47328.0 | 16.7% | 15.9% | -0.8 |
| 20.0 | 30.0 | app5 | True | False | 50048.0 | 16.7% | 16.8% | 0.2 |
| 20.0 | 30.0 | app6 | True | False | 50018.0 | 16.7% | 16.8% | 0.1 |
| 30.0 | 40.0 | app1 | True | False | 50070.0 | 16.7% | 16.1% | -0.6 |
| 30.0 | 40.0 | app2 | True | False | 51436.0 | 16.7% | 16.5% | -0.1 |
| 30.0 | 40.0 | app3 | True | False | 52648.0 | 16.7% | 16.9% | 0.3 |
| 30.0 | 40.0 | app4 | True | False | 52782.0 | 16.7% | 17.0% | 0.3 |
| 30.0 | 40.0 | app5 | True | False | 52720.0 | 16.7% | 16.9% | 0.3 |
| 30.0 | 40.0 | app6 | True | False | 51434.0 | 16.7% | 16.5% | -0.1 |
| 40.0 | 50.0 | app1 | True | False | 52806.0 | 16.7% | 17.1% | 0.4 |
| 40.0 | 50.0 | app2 | True | False | 50014.0 | 16.7% | 16.2% | -0.5 |
| 40.0 | 50.0 | app3 | True | False | 51426.0 | 16.7% | 16.6% | -0.1 |
| 40.0 | 50.0 | app4 | True | False | 54080.0 | 16.7% | 17.5% | 0.8 |
| 40.0 | 50.0 | app5 | True | False | 50034.0 | 16.7% | 16.2% | -0.5 |
| 40.0 | 50.0 | app6 | True | False | 51214.0 | 16.7% | 16.5% | -0.1 |
| 50.0 | 60.0 | app1 | True | False | 49970.0 | 16.7% | 16.3% | -0.3 |
| 50.0 | 60.0 | app2 | True | False | 51396.0 | 16.7% | 16.8% | 0.1 |
| 50.0 | 60.0 | app3 | True | False | 51394.0 | 16.7% | 16.8% | 0.1 |
| 50.0 | 60.0 | app4 | True | False | 48754.0 | 16.7% | 16.0% | -0.7 |
| 50.0 | 60.0 | app5 | True | False | 52768.0 | 16.7% | 17.3% | 0.6 |
| 50.0 | 60.0 | app6 | True | False | 51346.0 | 16.7% | 16.8% | 0.1 |
| 60.0 | 70.0 | app1 | True | False | 51452.0 | 16.7% | 16.7% | 0.0 |
| 60.0 | 70.0 | app2 | True | False | 52758.0 | 16.7% | 17.1% | 0.4 |
| 60.0 | 70.0 | app3 | True | False | 51314.0 | 16.7% | 16.6% | -0.0 |
| 60.0 | 70.0 | app4 | True | False | 50046.0 | 16.7% | 16.2% | -0.4 |
| 60.0 | 70.0 | app5 | True | False | 51448.0 | 16.7% | 16.7% | 0.0 |
| 60.0 | 70.0 | app6 | True | False | 51376.0 | 16.7% | 16.7% | -0.0 |
| 70.0 | 80.0 | app1 | True | False | 51440.0 | 16.7% | 17.0% | 0.3 |
| 70.0 | 80.0 | app2 | True | False | 50028.0 | 16.7% | 16.5% | -0.2 |
| 70.0 | 80.0 | app3 | True | False | 50106.0 | 16.7% | 16.5% | -0.1 |
| 70.0 | 80.0 | app4 | True | False | 51416.0 | 16.7% | 17.0% | 0.3 |
| 70.0 | 80.0 | app5 | True | False | 51440.0 | 16.7% | 17.0% | 0.3 |
| 70.0 | 80.0 | app6 | True | False | 48652.0 | 16.7% | 16.1% | -0.6 |
| 80.0 | 90.0 | app1 | True | False | 51342.0 | 16.7% | 16.6% | -0.0 |
| 80.0 | 90.0 | app2 | True | False | 51440.0 | 16.7% | 16.7% | 0.0 |
| 80.0 | 90.0 | app3 | True | False | 51422.0 | 16.7% | 16.7% | 0.0 |
| 80.0 | 90.0 | app4 | True | False | 51416.0 | 16.7% | 16.7% | 0.0 |
| 80.0 | 90.0 | app5 | True | False | 49998.0 | 16.7% | 16.2% | -0.5 |
| 80.0 | 90.0 | app6 | True | False | 52790.0 | 16.7% | 17.1% | 0.5 |
| 90.0 | 100.0 | app1 | True | False | 50022.0 | 16.7% | 16.4% | -0.2 |
| 90.0 | 100.0 | app2 | True | False | 49986.0 | 16.7% | 16.4% | -0.2 |
| 90.0 | 100.0 | app3 | True | False | 51422.0 | 16.7% | 16.9% | 0.2 |
| 90.0 | 100.0 | app4 | True | False | 51414.0 | 16.7% | 16.9% | 0.2 |
| 90.0 | 100.0 | app5 | True | False | 49980.0 | 16.7% | 16.4% | -0.2 |
| 90.0 | 100.0 | app6 | True | False | 51318.0 | 16.7% | 16.9% | 0.2 |
| 100.0 | 110.0 | app1 | True | False | 51370.0 | 16.7% | 16.7% | 0.0 |
| 100.0 | 110.0 | app2 | True | False | 52676.0 | 16.7% | 17.1% | 0.4 |
| 100.0 | 110.0 | app3 | True | False | 51292.0 | 16.7% | 16.6% | -0.0 |
| 100.0 | 110.0 | app4 | True | False | 50038.0 | 16.7% | 16.2% | -0.4 |
| 100.0 | 110.0 | app5 | True | False | 51334.0 | 16.7% | 16.7% | -0.0 |
| 100.0 | 110.0 | app6 | True | False | 51414.0 | 16.7% | 16.7% | 0.0 |
| 110.0 | 120.0 | app1 | True | False | 50108.0 | 16.7% | 16.5% | -0.2 |
| 110.0 | 120.0 | app2 | True | False | 51438.0 | 16.7% | 16.9% | 0.2 |
| 110.0 | 120.0 | app3 | True | False | 51326.0 | 16.7% | 16.9% | 0.2 |
| 110.0 | 120.0 | app4 | True | False | 50040.0 | 16.7% | 16.4% | -0.2 |
| 110.0 | 120.0 | app5 | True | False | 51358.0 | 16.7% | 16.9% | 0.2 |
| 110.0 | 120.0 | app6 | True | False | 50072.0 | 16.7% | 16.5% | -0.2 |
| 120.0 | 130.0 | app1 | True | False | 50102.0 | 16.7% | 17.7% | 1.1 |
| 120.0 | 130.0 | app2 | True | False | 41874.0 | 16.7% | 14.8% | -1.9 |
| 120.0 | 130.0 | app3 | True | False | 45962.0 | 16.7% | 16.3% | -0.4 |
| 120.0 | 130.0 | app4 | True | False | 47348.0 | 16.7% | 16.8% | 0.1 |
| 120.0 | 130.0 | app5 | True | False | 48710.0 | 16.7% | 17.2% | 0.6 |
| 120.0 | 130.0 | app6 | True | False | 48660.0 | 16.7% | 17.2% | 0.5 |
| 130.0 | 140.0 | app1 | True | False | 51388.0 | 16.7% | 16.5% | -0.1 |
| 130.0 | 140.0 | app2 | True | False | 51382.0 | 16.7% | 16.5% | -0.1 |
| 130.0 | 140.0 | app3 | True | False | 51320.0 | 16.7% | 16.5% | -0.2 |
| 130.0 | 140.0 | app4 | True | False | 52636.0 | 16.7% | 16.9% | 0.3 |
| 130.0 | 140.0 | app5 | True | False | 51298.0 | 16.7% | 16.5% | -0.2 |
| 130.0 | 140.0 | app6 | True | False | 52788.0 | 16.7% | 17.0% | 0.3 |
| 140.0 | 150.0 | app1 | True | False | 51364.0 | 16.7% | 16.7% | 0.1 |
| 140.0 | 150.0 | app2 | True | False | 49984.0 | 16.7% | 16.3% | -0.4 |
| 140.0 | 150.0 | app3 | True | False | 51338.0 | 16.7% | 16.7% | 0.1 |
| 140.0 | 150.0 | app4 | True | False | 51402.0 | 16.7% | 16.8% | 0.1 |
| 140.0 | 150.0 | app5 | True | False | 49958.0 | 16.7% | 16.3% | -0.4 |
| 140.0 | 150.0 | app6 | True | False | 52698.0 | 16.7% | 17.2% | 0.5 |
| 150.0 | 160.0 | app1 | True | False | 51414.0 | 16.7% | 17.1% | 0.5 |
| 150.0 | 160.0 | app2 | True | False | 50022.0 | 16.7% | 16.7% | -0.0 |
| 150.0 | 160.0 | app3 | True | False | 50054.0 | 16.7% | 16.7% | 0.0 |
| 150.0 | 160.0 | app4 | True | False | 51388.0 | 16.7% | 17.1% | 0.5 |
| 150.0 | 160.0 | app5 | True | False | 51312.0 | 16.7% | 17.1% | 0.4 |
| 150.0 | 160.0 | app6 | True | False | 45976.0 | 16.7% | 15.3% | -1.3 |
| 160.0 | 170.0 | app1 | True | False | 48656.0 | 16.7% | 16.1% | -0.6 |
| 160.0 | 170.0 | app2 | True | False | 51412.0 | 16.7% | 17.0% | 0.3 |
| 160.0 | 170.0 | app3 | True | False | 51322.0 | 16.7% | 16.9% | 0.3 |
| 160.0 | 170.0 | app4 | True | False | 47292.0 | 16.7% | 15.6% | -1.0 |
| 160.0 | 170.0 | app5 | True | False | 52714.0 | 16.7% | 17.4% | 0.7 |
| 160.0 | 170.0 | app6 | True | False | 51418.0 | 16.7% | 17.0% | 0.3 |
| 170.0 | 180.0 | app1 | True | False | 50096.0 | 16.7% | 16.5% | -0.2 |
| 170.0 | 180.0 | app2 | True | False | 50056.0 | 16.7% | 16.4% | -0.2 |
| 170.0 | 180.0 | app3 | True | False | 51476.0 | 16.7% | 16.9% | 0.2 |
| 170.0 | 180.0 | app4 | True | False | 51316.0 | 16.7% | 16.9% | 0.2 |
| 170.0 | 180.0 | app5 | True | False | 50136.0 | 16.7% | 16.5% | -0.2 |
| 170.0 | 180.0 | app6 | True | False | 51378.0 | 16.7% | 16.9% | 0.2 |
| 180.0 | 191.0 | app1 | True | False | 53980.0 | 16.7% | 17.7% | 1.0 |
| 180.0 | 191.0 | app2 | True | False | 51464.0 | 16.7% | 16.8% | 0.2 |
| 180.0 | 191.0 | app3 | True | False | 48656.0 | 16.7% | 15.9% | -0.7 |
| 180.0 | 191.0 | app4 | True | False | 49994.0 | 16.7% | 16.4% | -0.3 |
| 180.0 | 191.0 | app5 | True | False | 50004.0 | 16.7% | 16.4% | -0.3 |
| 180.0 | 191.0 | app6 | True | False | 51350.0 | 16.7% | 16.8% | 0.1 |
| 191.0 | 201.0 | app1 | True | False | 48684.0 | 16.7% | 16.1% | -0.6 |
| 191.0 | 201.0 | app2 | True | False | 50126.0 | 16.7% | 16.5% | -0.1 |
| 191.0 | 201.0 | app3 | True | False | 51446.0 | 16.7% | 17.0% | 0.3 |
| 191.0 | 201.0 | app4 | True | False | 51436.0 | 16.7% | 17.0% | 0.3 |
| 191.0 | 201.0 | app5 | True | False | 51492.0 | 16.7% | 17.0% | 0.3 |
| 191.0 | 201.0 | app6 | True | False | 50136.0 | 16.7% | 16.5% | -0.1 |
| 201.0 | 211.0 | app1 | True | False | 48706.0 | 16.7% | 16.5% | -0.2 |
| 201.0 | 211.0 | app2 | True | False | 47398.0 | 16.7% | 16.1% | -0.6 |
| 201.0 | 211.0 | app3 | True | False | 50142.0 | 16.7% | 17.0% | 0.3 |
| 201.0 | 211.0 | app4 | True | False | 50022.0 | 16.7% | 17.0% | 0.3 |
| 201.0 | 211.0 | app5 | True | False | 47414.0 | 16.7% | 16.1% | -0.6 |
| 201.0 | 211.0 | app6 | True | False | 51360.0 | 16.7% | 17.4% | 0.7 |
| 211.0 | 221.0 | app1 | True | False | 52752.0 | 16.7% | 17.2% | 0.5 |
| 211.0 | 221.0 | app2 | True | False | 49982.0 | 16.7% | 16.3% | -0.4 |
| 211.0 | 221.0 | app3 | True | False | 49996.0 | 16.7% | 16.3% | -0.4 |
| 211.0 | 221.0 | app4 | True | False | 51466.0 | 16.7% | 16.8% | 0.1 |
| 211.0 | 221.0 | app5 | True | False | 51456.0 | 16.7% | 16.8% | 0.1 |
| 211.0 | 221.0 | app6 | True | False | 51326.0 | 16.7% | 16.7% | 0.1 |
| 221.0 | 231.0 | app1 | True | False | 48576.0 | 16.7% | 16.5% | -0.2 |
| 221.0 | 231.0 | app2 | True | False | 50020.0 | 16.7% | 17.0% | 0.3 |
| 221.0 | 231.0 | app3 | True | False | 48698.0 | 16.7% | 16.5% | -0.1 |
| 221.0 | 231.0 | app4 | True | False | 50024.0 | 16.7% | 17.0% | 0.3 |
| 221.0 | 231.0 | app5 | True | False | 48692.0 | 16.7% | 16.5% | -0.1 |
| 221.0 | 231.0 | app6 | True | False | 48662.0 | 16.7% | 16.5% | -0.2 |
| 231.0 | 241.0 | app1 | True | False | 52650.0 | 16.7% | 17.3% | 0.6 |
| 231.0 | 241.0 | app2 | True | False | 48594.0 | 16.7% | 16.0% | -0.7 |
| 231.0 | 241.0 | app3 | True | False | 51504.0 | 16.7% | 16.9% | 0.3 |
| 231.0 | 241.0 | app4 | True | False | 50106.0 | 16.7% | 16.5% | -0.2 |
| 231.0 | 241.0 | app5 | True | False | 50004.0 | 16.7% | 16.4% | -0.2 |
| 231.0 | 241.0 | app6 | True | False | 51356.0 | 16.7% | 16.9% | 0.2 |
| 241.0 | 251.0 | app1 | False | n/a | 43254.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 41962.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | n/a | 43164.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app4 | False | n/a | 44628.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app5 | False | n/a | 43316.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app6 | False | n/a | 43322.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 2692.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | False | n/a | 1358.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | False | n/a | 1358.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | False | n/a | 1358.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | False | n/a | 2716.0 | n/a | n/a | n/a |
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
| 411.0 | 422.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 422.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 422.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 422.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 422.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 422.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
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
| 532.0 | 542.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 35 | 0ms | 1917ms | 2442ms |
| 0.0 | 10.0 | app2 | ok | 35 | 0ms | 2125ms | 2462ms |
| 0.0 | 10.0 | app3 | ok | 36 | 0ms | 2162ms | 2466ms |
| 0.0 | 10.0 | app4 | ok | 35 | 0ms | 2023ms | 2452ms |
| 0.0 | 10.0 | app5 | ok | 35 | 0ms | 2125ms | 2462ms |
| 0.0 | 10.0 | app6 | ok | 35 | 0ms | 2191ms | 2469ms |
| 10.0 | 20.0 | app1 | ok | 42 | 3468ms | 4823ms | 8950ms |
| 10.0 | 20.0 | app2 | ok | 42 | 3750ms | 4917ms | 9300ms |
| 10.0 | 20.0 | app3 | ok | 41 | 3607ms | 4779ms | 7950ms |
| 10.0 | 20.0 | app4 | ok | 41 | 3447ms | 4689ms | 4969ms |
| 10.0 | 20.0 | app5 | ok | 42 | 3603ms | 4838ms | 8950ms |
| 10.0 | 20.0 | app6 | ok | 42 | 3684ms | 4789ms | 7900ms |
| 20.0 | 30.0 | app1 | ok | 44 | 3125ms | 4696ms | 7800ms |
| 20.0 | 30.0 | app2 | ok | 44 | 3190ms | 4707ms | 7800ms |
| 20.0 | 30.0 | app3 | ok | 43 | 3170ms | 4705ms | 7850ms |
| 20.0 | 30.0 | app4 | ok | 44 | 3214ms | 4786ms | 8900ms |
| 20.0 | 30.0 | app5 | ok | 43 | 3194ms | 4787ms | 8925ms |
| 20.0 | 30.0 | app6 | ok | 44 | 3056ms | 4685ms | 7800ms |
| 30.0 | 40.0 | app1 | ok | 32 | 3462ms | 4692ms | 4969ms |
| 30.0 | 40.0 | app2 | ok | 32 | 3571ms | 4714ms | 4971ms |
| 30.0 | 40.0 | app3 | ok | 34 | 3534ms | 4707ms | 4971ms |
| 30.0 | 40.0 | app4 | ok | 33 | 3578ms | 4716ms | 4972ms |
| 30.0 | 40.0 | app5 | ok | 33 | 3616ms | 4795ms | 8350ms |
| 30.0 | 40.0 | app6 | ok | 32 | 3571ms | 4714ms | 4971ms |
| 40.0 | 50.0 | app1 | ok | 32 | 3519ms | 4704ms | 4970ms |
| 40.0 | 50.0 | app2 | ok | 33 | 3472ms | 4694ms | 4969ms |
| 40.0 | 50.0 | app3 | ok | 32 | 3462ms | 4692ms | 4969ms |
| 40.0 | 50.0 | app4 | ok | 32 | 3571ms | 4714ms | 4971ms |
| 40.0 | 50.0 | app5 | ok | 32 | 3462ms | 4692ms | 4969ms |
| 40.0 | 50.0 | app6 | ok | 32 | 3571ms | 4714ms | 4971ms |
| 50.0 | 60.0 | app1 | ok | 40 | 3750ms | 4750ms | 4975ms |
| 50.0 | 60.0 | app2 | ok | 38 | 3603ms | 4721ms | 4972ms |
| 50.0 | 60.0 | app3 | ok | 39 | 3682ms | 4736ms | 4974ms |
| 50.0 | 60.0 | app4 | ok | 40 | 3824ms | 5000ms | 9500ms |
| 50.0 | 60.0 | app5 | ok | 39 | 3646ms | 4729ms | 4973ms |
| 50.0 | 60.0 | app6 | ok | 40 | 3750ms | 4861ms | 9000ms |
| 60.0 | 70.0 | app1 | ok | 38 | 3643ms | 4729ms | 4973ms |
| 60.0 | 70.0 | app2 | ok | 40 | 3649ms | 4730ms | 4973ms |
| 60.0 | 70.0 | app3 | ok | 39 | 3682ms | 4736ms | 4974ms |
| 60.0 | 70.0 | app4 | ok | 38 | 3716ms | 4743ms | 4974ms |
| 60.0 | 70.0 | app5 | ok | 39 | 3783ms | 4809ms | 8050ms |
| 60.0 | 70.0 | app6 | ok | 39 | 3715ms | 4799ms | 8050ms |
| 70.0 | 80.0 | app1 | ok | 39 | 3566ms | 4713ms | 4971ms |
| 70.0 | 80.0 | app2 | ok | 39 | 3646ms | 4729ms | 4973ms |
| 70.0 | 80.0 | app3 | ok | 39 | 3785ms | 4868ms | 9025ms |
| 70.0 | 80.0 | app4 | ok | 40 | 3611ms | 4722ms | 4972ms |
| 70.0 | 80.0 | app5 | ok | 40 | 3889ms | 5000ms | 9500ms |
| 70.0 | 80.0 | app6 | ok | 39 | 3682ms | 4736ms | 4974ms |
| 80.0 | 90.0 | app1 | ok | 43 | 3464ms | 4693ms | 4969ms |
| 80.0 | 90.0 | app2 | ok | 42 | 3571ms | 4771ms | 7900ms |
| 80.0 | 90.0 | app3 | ok | 44 | 3542ms | 4764ms | 7800ms |
| 80.0 | 90.0 | app4 | ok | 42 | 3500ms | 4700ms | 4970ms |
| 80.0 | 90.0 | app5 | ok | 43 | 3674ms | 4977ms | 9462ms |
| 80.0 | 90.0 | app6 | ok | 44 | 3542ms | 4764ms | 7800ms |
| 90.0 | 100.0 | app1 | ok | 32 | 3621ms | 4724ms | 4972ms |
| 90.0 | 100.0 | app2 | ok | 31 | 3616ms | 4723ms | 4972ms |
| 90.0 | 100.0 | app3 | ok | 29 | 3702ms | 4817ms | 8550ms |
| 90.0 | 100.0 | app4 | ok | 31 | 3565ms | 4713ms | 4971ms |
| 90.0 | 100.0 | app5 | ok | 31 | 3705ms | 4812ms | 8450ms |
| 90.0 | 100.0 | app6 | ok | 30 | 3707ms | 4741ms | 4974ms |
| 100.0 | 110.0 | app1 | ok | 36 | 3676ms | 4735ms | 4974ms |
| 100.0 | 110.0 | app2 | ok | 36 | 3712ms | 4803ms | 8200ms |
| 100.0 | 110.0 | app3 | ok | 37 | 3713ms | 4801ms | 8150ms |
| 100.0 | 110.0 | app4 | ok | 36 | 3714ms | 4743ms | 4974ms |
| 100.0 | 110.0 | app5 | ok | 35 | 3711ms | 4805ms | 8250ms |
| 100.0 | 110.0 | app6 | ok | 36 | 3676ms | 4735ms | 4974ms |
| 110.0 | 120.0 | app1 | ok | 40 | 3241ms | 4722ms | 8000ms |
| 110.0 | 120.0 | app2 | ok | 39 | 3319ms | 4664ms | 4966ms |
| 110.0 | 120.0 | app3 | ok | 40 | 3304ms | 4732ms | 8000ms |
| 110.0 | 120.0 | app4 | ok | 42 | 3276ms | 4724ms | 7900ms |
| 110.0 | 120.0 | app5 | ok | 41 | 3102ms | 4620ms | 4962ms |
| 110.0 | 120.0 | app6 | ok | 41 | 3259ms | 4723ms | 7950ms |
| 120.0 | 130.0 | app1 | ok | 40 | 3269ms | 4808ms | 9000ms |
| 120.0 | 130.0 | app2 | ok | 42 | 3500ms | 4900ms | 9300ms |
| 120.0 | 130.0 | app3 | ok | 41 | 3348ms | 4812ms | 8975ms |
| 120.0 | 130.0 | app4 | ok | 39 | 3073ms | 4698ms | 8050ms |
| 120.0 | 130.0 | app5 | ok | 41 | 3287ms | 4806ms | 8975ms |
| 120.0 | 130.0 | app6 | ok | 40 | 3241ms | 4722ms | 8000ms |
| 130.0 | 140.0 | app1 | ok | 42 | 3250ms | 4650ms | 4965ms |
| 130.0 | 140.0 | app2 | ok | 39 | 3050ms | 4610ms | 4961ms |
| 130.0 | 140.0 | app3 | ok | 39 | 3125ms | 4625ms | 4962ms |
| 130.0 | 140.0 | app4 | ok | 41 | 3029ms | 4606ms | 4961ms |
| 130.0 | 140.0 | app5 | ok | 40 | 3214ms | 4643ms | 4964ms |
| 130.0 | 140.0 | app6 | ok | 40 | 3241ms | 4722ms | 8000ms |
| 140.0 | 150.0 | app1 | ok | 29 | 3606ms | 4721ms | 4972ms |
| 140.0 | 150.0 | app2 | ok | 31 | 3450ms | 4690ms | 4969ms |
| 140.0 | 150.0 | app3 | ok | 31 | 3565ms | 4713ms | 4971ms |
| 140.0 | 150.0 | app4 | ok | 29 | 3424ms | 4685ms | 4968ms |
| 140.0 | 150.0 | app5 | ok | 30 | 3611ms | 4722ms | 4972ms |
| 140.0 | 150.0 | app6 | ok | 30 | 3661ms | 4732ms | 4973ms |
| 150.0 | 160.0 | app1 | ok | 39 | 3221ms | 4721ms | 8050ms |
| 150.0 | 160.0 | app2 | ok | 40 | 3000ms | 4600ms | 4960ms |
| 150.0 | 160.0 | app3 | ok | 39 | 3125ms | 4625ms | 4962ms |
| 150.0 | 160.0 | app4 | ok | 40 | 3148ms | 4630ms | 4963ms |
| 150.0 | 160.0 | app5 | ok | 40 | 3148ms | 4630ms | 4963ms |
| 150.0 | 160.0 | app6 | ok | 39 | 3259ms | 4652ms | 4965ms |
| 160.0 | 170.0 | app1 | ok | 39 | 3679ms | 4793ms | 8050ms |
| 160.0 | 170.0 | app2 | ok | 39 | 3375ms | 4675ms | 4968ms |
| 160.0 | 170.0 | app3 | ok | 40 | 3571ms | 4714ms | 4971ms |
| 160.0 | 170.0 | app4 | ok | 39 | 3427ms | 4685ms | 4969ms |
| 160.0 | 170.0 | app5 | ok | 39 | 3646ms | 4729ms | 4973ms |
| 160.0 | 170.0 | app6 | ok | 40 | 3529ms | 4706ms | 4971ms |
| 170.0 | 180.0 | app1 | ok | 33 | 3472ms | 4694ms | 4969ms |
| 170.0 | 180.0 | app2 | ok | 33 | 3413ms | 4683ms | 4968ms |
| 170.0 | 180.0 | app3 | ok | 33 | 3450ms | 4770ms | 8350ms |
| 170.0 | 180.0 | app4 | ok | 33 | 3413ms | 4683ms | 4968ms |
| 170.0 | 180.0 | app5 | ok | 34 | 3571ms | 4786ms | 8300ms |
| 170.0 | 180.0 | app6 | ok | 33 | 3413ms | 4683ms | 4968ms |
| 180.0 | 191.0 | app1 | ok | 42 | 3618ms | 4724ms | 4972ms |
| 180.0 | 191.0 | app2 | ok | 40 | 3387ms | 4677ms | 4968ms |
| 180.0 | 191.0 | app3 | ok | 39 | 3523ms | 4705ms | 4970ms |
| 180.0 | 191.0 | app4 | ok | 40 | 3571ms | 4714ms | 4971ms |
| 180.0 | 191.0 | app5 | ok | 39 | 3646ms | 4729ms | 4973ms |
| 180.0 | 191.0 | app6 | ok | 40 | 3714ms | 4857ms | 9000ms |
| 191.0 | 201.0 | app1 | ok | 36 | 3786ms | 4814ms | 8200ms |
| 191.0 | 201.0 | app2 | ok | 38 | 3417ms | 4683ms | 4968ms |
| 191.0 | 201.0 | app3 | ok | 39 | 3523ms | 4705ms | 4970ms |
| 191.0 | 201.0 | app4 | ok | 38 | 3643ms | 4729ms | 4973ms |
| 191.0 | 201.0 | app5 | ok | 38 | 3857ms | 4943ms | 9367ms |
| 191.0 | 201.0 | app6 | ok | 38 | 3750ms | 4750ms | 4975ms |
| 201.0 | 211.0 | app1 | ok | 42 | 3200ms | 4880ms | 9300ms |
| 201.0 | 211.0 | app2 | ok | 40 | 2727ms | 4545ms | 4955ms |
| 201.0 | 211.0 | app3 | ok | 41 | 2969ms | 4677ms | 7950ms |
| 201.0 | 211.0 | app4 | ok | 41 | 3029ms | 4606ms | 4961ms |
| 201.0 | 211.0 | app5 | ok | 42 | 3000ms | 4680ms | 7900ms |
| 201.0 | 211.0 | app6 | ok | 42 | 3125ms | 4625ms | 4962ms |
| 211.0 | 221.0 | app1 | ok | 30 | 3661ms | 4732ms | 4973ms |
| 211.0 | 221.0 | app2 | ok | 31 | 2961ms | 4592ms | 4959ms |
| 211.0 | 221.0 | app3 | ok | 30 | 3370ms | 4674ms | 4967ms |
| 211.0 | 221.0 | app4 | ok | 31 | 3616ms | 4723ms | 4972ms |
| 211.0 | 221.0 | app5 | ok | 28 | 3478ms | 4696ms | 4970ms |
| 211.0 | 221.0 | app6 | ok | 29 | 3657ms | 4731ms | 4973ms |
| 221.0 | 231.0 | app1 | ok | 43 | 3170ms | 4705ms | 7850ms |
| 221.0 | 231.0 | app2 | ok | 42 | 2717ms | 4543ms | 4954ms |
| 221.0 | 231.0 | app3 | ok | 42 | 2900ms | 4580ms | 4958ms |
| 221.0 | 231.0 | app4 | ok | 42 | 3077ms | 4692ms | 7900ms |
| 221.0 | 231.0 | app5 | ok | 43 | 2850ms | 4570ms | 4957ms |
| 221.0 | 231.0 | app6 | ok | 42 | 3173ms | 4788ms | 8950ms |
| 231.0 | 241.0 | app1 | ok | 31 | 3510ms | 4702ms | 4970ms |
| 231.0 | 241.0 | app2 | ok | 32 | 2895ms | 4579ms | 4958ms |
| 231.0 | 241.0 | app3 | ok | 32 | 3182ms | 4636ms | 4964ms |
| 231.0 | 241.0 | app4 | ok | 32 | 3333ms | 4667ms | 4967ms |
| 231.0 | 241.0 | app5 | ok | 33 | 3207ms | 4641ms | 4964ms |
| 231.0 | 241.0 | app6 | ok | 32 | 3462ms | 4692ms | 4969ms |
| 241.0 | 251.0 | app1 | ok | 20 | 3750ms | 4750ms | 4975ms |
| 241.0 | 251.0 | app2 | ok | 16 | 3182ms | 4636ms | 4964ms |
| 241.0 | 251.0 | app3 | ok | 18 | 3393ms | 4679ms | 4968ms |
| 241.0 | 251.0 | app4 | ok | 19 | 3516ms | 4703ms | 4970ms |
| 241.0 | 251.0 | app5 | ok | 17 | 3482ms | 4696ms | 4970ms |
| 241.0 | 251.0 | app6 | ok | 20 | 3750ms | 4750ms | 4975ms |
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
| 411.0 | 422.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 422.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 422.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 422.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 422.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 422.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 532.0 | 542.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1130370 | 56175 | 1186545.0 | 0.0% | 1207514.0 | 1242720.0 | -2.8% | True |
| app2 | 1119300 | 55748 | 1175048.0 | 0.0% | 1197022.0 | 1230796.0 | -2.7% | True |
| app3 | 1125450 | 55869 | 1181319.0 | 0.0% | 1210180.0 | 1237188.0 | -2.2% | True |
| app4 | 1127910 | 56146 | 1184056.0 | 0.0% | 1205072.0 | 1240202.0 | -2.8% | True |
| app5 | 1125450 | 56015 | 1181465.0 | 0.0% | 1209036.0 | 1237480.0 | -2.3% | True |
| app6 | 1130370 | 56057 | 1186427.0 | 0.0% | 1216790.0 | 1242484.0 | -2.1% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 919 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 914 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 917 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app4 | 918 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app5 | 917 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app6 | 919 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5504). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5504 | 0.051ms | 0.121ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 512765 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 919 | 8474ms | 13085ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 910 | 8148ms | 12156ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app3 | ok | 915 | 8276ms | 12666ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app4 | ok | 917 | 8356ms | 12730ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app5 | ok | 915 | 8410ms | 12993ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app6 | ok | 919 | 8485ms | 13101ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5495 | 8362ms | 12833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (55 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2500ms | 5550ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 3100ms | 4975ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app3 | ok | 2833ms | 4770ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app4 | ok | 2333ms | 5100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app5 | ok | 2700ms | 5475ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app6 | ok | 2625ms | 4850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 7600ms | 10000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 7684ms | 12000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app3 | ok | 7778ms | 12750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app4 | ok | 7350ms | 9992ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app5 | ok | 7421ms | 9858ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app6 | ok | 7765ms | 12000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 8556ms | 13417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 8643ms | 13972ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app3 | ok | 8364ms | 14000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app4 | ok | 8308ms | 13714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app5 | ok | 8583ms | 14075ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app6 | ok | 8600ms | 13844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 8600ms | 13844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 8900ms | 13812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app3 | ok | 8438ms | 13607ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app4 | ok | 8722ms | 13781ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app5 | ok | 8562ms | 13781ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app6 | ok | 8588ms | 13643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 8318ms | 9914ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 8474ms | 12687ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app3 | ok | 8571ms | 12625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app4 | ok | 8286ms | 10000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app5 | ok | 8542ms | 9929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app6 | ok | 8455ms | 10250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 8409ms | 9923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 8455ms | 10250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app3 | ok | 8593ms | 9859ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app4 | ok | 8522ms | 9930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app5 | ok | 8318ms | 9914ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app6 | ok | 8583ms | 10250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 8640ms | 10250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 8238ms | 9910ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app3 | ok | 8286ms | 9914ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app4 | ok | 8808ms | 11917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app5 | ok | 8435ms | 9922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app6 | ok | 8480ms | 9848ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 8560ms | 9928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 8520ms | 9852ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app3 | ok | 8458ms | 9846ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app4 | ok | 8417ms | 9842ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app5 | ok | 8538ms | 9854ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app6 | ok | 8615ms | 9862ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 8455ms | 10250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 8593ms | 9859ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app3 | ok | 8593ms | 9859ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app4 | ok | 8538ms | 9854ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app5 | ok | 8760ms | 11917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app6 | ok | 8577ms | 9927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 8350ms | 10375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 8429ms | 10375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app3 | ok | 8609ms | 11833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app4 | ok | 8636ms | 12625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app5 | ok | 8409ms | 9923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app6 | ok | 8522ms | 10250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 8560ms | 9928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 8440ms | 9844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app3 | ok | 8286ms | 9914ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app4 | ok | 8458ms | 9846ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app5 | ok | 8417ms | 9842ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app6 | ok | 8500ms | 9925ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 8625ms | 10375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 8741ms | 10250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app3 | ok | 8609ms | 11833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app4 | ok | 8652ms | 11917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app5 | ok | 8583ms | 10250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app6 | ok | 8429ms | 10375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 8688ms | 13844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 8385ms | 13625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app3 | ok | 8667ms | 13786ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app4 | ok | 8867ms | 14028ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app5 | ok | 8750ms | 13875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app6 | ok | 8800ms | 14000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 8471ms | 13417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 8462ms | 13944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app3 | ok | 8571ms | 13944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app4 | ok | 7706ms | 13050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app5 | ok | 8533ms | 13812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app6 | ok | 8438ms | 13607ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 8824ms | 13944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 7600ms | 12625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app3 | ok | 8133ms | 13100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app4 | ok | 8588ms | 13643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app5 | ok | 8600ms | 13844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app6 | ok | 8600ms | 13917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 8182ms | 13944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 7933ms | 11917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app3 | ok | 8214ms | 13458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app4 | ok | 8000ms | 13417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app5 | ok | 8308ms | 13812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app6 | ok | 8308ms | 13583ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 8533ms | 13714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 7875ms | 12625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app3 | ok | 8125ms | 12625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app4 | ok | 8133ms | 12750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app5 | ok | 8389ms | 13050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app6 | ok | 8750ms | 13944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 8438ms | 13458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 7923ms | 12687ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app3 | ok | 8286ms | 13643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app4 | ok | 8143ms | 13417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app5 | ok | 8273ms | 13972ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app6 | ok | 8375ms | 13417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app1 | ok | 8167ms | 13889ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app2 | ok | 8000ms | 13100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app3 | ok | 8308ms | 13714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app4 | ok | 8214ms | 13458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app5 | ok | 8600ms | 13844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app6 | ok | 8400ms | 13643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 8857ms | 13500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 8176ms | 11917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app3 | ok | 8125ms | 12625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app4 | ok | 8421ms | 12625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app5 | ok | 8500ms | 12625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app6 | ok | 8684ms | 13458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 8533ms | 13714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 8062ms | 10625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app3 | ok | 8389ms | 12687ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app4 | ok | 8312ms | 13150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app5 | ok | 8765ms | 13750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app6 | ok | 8571ms | 13944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 8722ms | 13781ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 7500ms | 13417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app3 | ok | 7833ms | 13458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app4 | ok | 8400ms | 13643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app5 | ok | 8857ms | 14136ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app6 | ok | 8889ms | 13944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 8625ms | 13714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 7588ms | 10375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app3 | ok | 7765ms | 12750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app4 | ok | 8188ms | 12687ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app5 | ok | 7778ms | 9893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app6 | ok | 8500ms | 13500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 8600ms | 13917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 7158ms | 9822ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app3 | ok | 7889ms | 11833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app4 | ok | 8562ms | 13679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app5 | ok | 8357ms | 13679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app6 | ok | 8571ms | 13944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 8636ms | 9945ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 7786ms | 9779ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app3 | ok | 8118ms | 9812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app4 | ok | 8450ms | 9935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app5 | ok | 8444ms | 11000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app6 | ok | 8609ms | 9861ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app3 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app4 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app5 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app6 | ok | 10000ms | 14500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 411.0 | 422.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 422.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 422.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 422.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 422.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 422.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 532.0 | 542.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 546.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 546.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 546.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 546.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 546.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 546.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
