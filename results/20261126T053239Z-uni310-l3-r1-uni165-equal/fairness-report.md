# Fairness benchmark: six-group-board-case (uni310-l3-r1-uni165-equal)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-56676bd7d4-g57zw` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T05:33:50Z` |
| Run end | `2026-11-26T05:42:55Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 56 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/56 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 73.00 | 2.2812 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 16.7 | 32 | 917 | 200=917 | 8.5 | 10.9 | 1210618.0 | 16.7% | 16.7% | 0.0 | 16.7% | 0.0 | 16.7% | 0.0 | 78.4s | 98.9% | 917.0 |
| app2 | 16.7 | 32 | 918 | 200=918 | 8.5 | 10.9 | 1210108.0 | 16.7% | 16.7% | 0.0 | 16.7% | 0.0 | 16.7% | 0.0 | 78.4s | 98.9% | 918.0 |
| app3 | 16.7 | 32 | 918 | 000=1, 200=917 | 8.5 | 10.9 | 1210316.0 | 16.7% | 16.7% | 0.0 | 16.7% | 0.0 | 16.7% | 0.0 | 78.4s | 98.9% | 918.0 |
| app4 | 16.7 | 32 | 918 | 200=918 | 8.5 | 10.9 | 1207286.0 | 16.7% | 16.7% | 0.0 | 16.7% | -0.0 | 16.7% | 0.0 | 78.4s | 98.9% | 918.0 |
| app5 | 16.7 | 32 | 915 | 000=1, 200=914 | 8.3 | 10.8 | 1199632.0 | 16.7% | 16.7% | 0.0 | 16.5% | -0.1 | 16.6% | -0.0 | 78.4s | 98.9% | 915.0 |
| app6 | 16.7 | 32 | 916 | 200=916 | 8.5 | 10.9 | 1210666.0 | 16.7% | 16.7% | 0.0 | 16.7% | 0.0 | 16.6% | -0.0 | 78.4s | 98.9% | 916.0 |
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
| 0.0 | 10.0 | app1 | True | False | 2704.0 | 16.7% | 20.0% | 3.3 |
| 0.0 | 10.0 | app2 | True | False | 1352.0 | 16.7% | 10.0% | -6.7 |
| 0.0 | 10.0 | app3 | True | False | 2682.0 | 16.7% | 19.8% | 3.2 |
| 0.0 | 10.0 | app4 | True | False | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app5 | True | False | 2708.0 | 16.7% | 20.0% | 3.4 |
| 0.0 | 10.0 | app6 | True | False | 4074.0 | 16.7% | 30.1% | 13.5 |
| 10.0 | 20.0 | app1 | True | False | 47434.0 | 16.7% | 16.5% | -0.1 |
| 10.0 | 20.0 | app2 | True | False | 48736.0 | 16.7% | 17.0% | 0.3 |
| 10.0 | 20.0 | app3 | True | False | 48720.0 | 16.7% | 17.0% | 0.3 |
| 10.0 | 20.0 | app4 | True | False | 47274.0 | 16.7% | 16.5% | -0.2 |
| 10.0 | 20.0 | app5 | True | False | 45892.0 | 16.7% | 16.0% | -0.7 |
| 10.0 | 20.0 | app6 | True | False | 48726.0 | 16.7% | 17.0% | 0.3 |
| 20.0 | 30.0 | app1 | True | False | 52794.0 | 16.7% | 17.3% | 0.6 |
| 20.0 | 30.0 | app2 | True | False | 51358.0 | 16.7% | 16.8% | 0.1 |
| 20.0 | 30.0 | app3 | True | False | 48736.0 | 16.7% | 15.9% | -0.7 |
| 20.0 | 30.0 | app4 | True | False | 51452.0 | 16.7% | 16.8% | 0.2 |
| 20.0 | 30.0 | app5 | True | False | 51262.0 | 16.7% | 16.8% | 0.1 |
| 20.0 | 30.0 | app6 | True | False | 49978.0 | 16.7% | 16.4% | -0.3 |
| 30.0 | 40.0 | app1 | True | False | 50070.0 | 16.7% | 16.6% | -0.1 |
| 30.0 | 40.0 | app2 | True | False | 48698.0 | 16.7% | 16.1% | -0.5 |
| 30.0 | 40.0 | app3 | True | False | 52780.0 | 16.7% | 17.5% | 0.8 |
| 30.0 | 40.0 | app4 | True | False | 50014.0 | 16.7% | 16.6% | -0.1 |
| 30.0 | 40.0 | app5 | True | False | 48768.0 | 16.7% | 16.2% | -0.5 |
| 30.0 | 40.0 | app6 | True | False | 51432.0 | 16.7% | 17.0% | 0.4 |
| 40.0 | 50.0 | app1 | True | False | 50114.0 | 16.7% | 16.5% | -0.2 |
| 40.0 | 50.0 | app2 | True | False | 51308.0 | 16.7% | 16.9% | 0.2 |
| 40.0 | 50.0 | app3 | True | False | 49952.0 | 16.7% | 16.4% | -0.2 |
| 40.0 | 50.0 | app4 | True | False | 49988.0 | 16.7% | 16.4% | -0.2 |
| 40.0 | 50.0 | app5 | True | False | 52818.0 | 16.7% | 17.4% | 0.7 |
| 40.0 | 50.0 | app6 | True | False | 50060.0 | 16.7% | 16.5% | -0.2 |
| 50.0 | 60.0 | app1 | True | False | 51308.0 | 16.7% | 16.8% | 0.1 |
| 50.0 | 60.0 | app2 | True | False | 51476.0 | 16.7% | 16.8% | 0.2 |
| 50.0 | 60.0 | app3 | True | False | 51420.0 | 16.7% | 16.8% | 0.2 |
| 50.0 | 60.0 | app4 | True | False | 51304.0 | 16.7% | 16.8% | 0.1 |
| 50.0 | 60.0 | app5 | True | False | 48722.0 | 16.7% | 15.9% | -0.7 |
| 50.0 | 60.0 | app6 | True | False | 51336.0 | 16.7% | 16.8% | 0.1 |
| 60.0 | 70.0 | app1 | True | False | 50062.0 | 16.7% | 16.4% | -0.2 |
| 60.0 | 70.0 | app2 | True | False | 49954.0 | 16.7% | 16.4% | -0.3 |
| 60.0 | 70.0 | app3 | True | False | 51430.0 | 16.7% | 16.9% | 0.2 |
| 60.0 | 70.0 | app4 | True | False | 51432.0 | 16.7% | 16.9% | 0.2 |
| 60.0 | 70.0 | app5 | True | False | 51396.0 | 16.7% | 16.9% | 0.2 |
| 60.0 | 70.0 | app6 | True | False | 50112.0 | 16.7% | 16.5% | -0.2 |
| 70.0 | 80.0 | app1 | True | False | 51318.0 | 16.7% | 16.9% | 0.2 |
| 70.0 | 80.0 | app2 | True | False | 52720.0 | 16.7% | 17.3% | 0.7 |
| 70.0 | 80.0 | app3 | True | False | 48734.0 | 16.7% | 16.0% | -0.6 |
| 70.0 | 80.0 | app4 | True | False | 50024.0 | 16.7% | 16.4% | -0.2 |
| 70.0 | 80.0 | app5 | True | False | 51354.0 | 16.7% | 16.9% | 0.2 |
| 70.0 | 80.0 | app6 | True | False | 50084.0 | 16.7% | 16.5% | -0.2 |
| 80.0 | 90.0 | app1 | True | False | 50054.0 | 16.7% | 16.9% | 0.2 |
| 80.0 | 90.0 | app2 | True | False | 47298.0 | 16.7% | 16.0% | -0.7 |
| 80.0 | 90.0 | app3 | True | False | 50058.0 | 16.7% | 16.9% | 0.2 |
| 80.0 | 90.0 | app4 | True | False | 50004.0 | 16.7% | 16.9% | 0.2 |
| 80.0 | 90.0 | app5 | True | False | 48654.0 | 16.7% | 16.4% | -0.2 |
| 80.0 | 90.0 | app6 | True | False | 49962.0 | 16.7% | 16.9% | 0.2 |
| 90.0 | 100.0 | app1 | True | False | 48720.0 | 16.7% | 16.1% | -0.6 |
| 90.0 | 100.0 | app2 | True | False | 50088.0 | 16.7% | 16.5% | -0.1 |
| 90.0 | 100.0 | app3 | True | False | 52690.0 | 16.7% | 17.4% | 0.7 |
| 90.0 | 100.0 | app4 | True | False | 50002.0 | 16.7% | 16.5% | -0.2 |
| 90.0 | 100.0 | app5 | True | False | 50074.0 | 16.7% | 16.5% | -0.1 |
| 90.0 | 100.0 | app6 | True | False | 51466.0 | 16.7% | 17.0% | 0.3 |
| 100.0 | 111.0 | app1 | True | False | 51402.0 | 16.7% | 16.9% | 0.2 |
| 100.0 | 111.0 | app2 | True | False | 52712.0 | 16.7% | 17.3% | 0.7 |
| 100.0 | 111.0 | app3 | True | False | 48640.0 | 16.7% | 16.0% | -0.7 |
| 100.0 | 111.0 | app4 | True | False | 50050.0 | 16.7% | 16.4% | -0.2 |
| 100.0 | 111.0 | app5 | True | False | 51420.0 | 16.7% | 16.9% | 0.2 |
| 100.0 | 111.0 | app6 | True | False | 50036.0 | 16.7% | 16.4% | -0.2 |
| 111.0 | 121.0 | app1 | True | False | 51374.0 | 16.7% | 17.0% | 0.3 |
| 111.0 | 121.0 | app2 | True | False | 50090.0 | 16.7% | 16.5% | -0.1 |
| 111.0 | 121.0 | app3 | True | False | 48750.0 | 16.7% | 16.1% | -0.6 |
| 111.0 | 121.0 | app4 | True | False | 51328.0 | 16.7% | 16.9% | 0.3 |
| 111.0 | 121.0 | app5 | True | False | 50052.0 | 16.7% | 16.5% | -0.1 |
| 111.0 | 121.0 | app6 | True | False | 51342.0 | 16.7% | 16.9% | 0.3 |
| 121.0 | 131.0 | app1 | True | False | 47356.0 | 16.7% | 16.1% | -0.6 |
| 121.0 | 131.0 | app2 | True | False | 50018.0 | 16.7% | 17.0% | 0.3 |
| 121.0 | 131.0 | app3 | True | False | 51370.0 | 16.7% | 17.4% | 0.8 |
| 121.0 | 131.0 | app4 | True | False | 48766.0 | 16.7% | 16.5% | -0.1 |
| 121.0 | 131.0 | app5 | True | False | 48736.0 | 16.7% | 16.5% | -0.1 |
| 121.0 | 131.0 | app6 | True | False | 48696.0 | 16.7% | 16.5% | -0.2 |
| 131.0 | 141.0 | app1 | True | False | 52748.0 | 16.7% | 17.0% | 0.3 |
| 131.0 | 141.0 | app2 | True | False | 51366.0 | 16.7% | 16.5% | -0.1 |
| 131.0 | 141.0 | app3 | True | False | 51294.0 | 16.7% | 16.5% | -0.2 |
| 131.0 | 141.0 | app4 | True | False | 52706.0 | 16.7% | 17.0% | 0.3 |
| 131.0 | 141.0 | app5 | True | False | 51356.0 | 16.7% | 16.5% | -0.1 |
| 131.0 | 141.0 | app6 | True | False | 51314.0 | 16.7% | 16.5% | -0.2 |
| 141.0 | 151.0 | app1 | True | False | 51352.0 | 16.7% | 17.2% | 0.5 |
| 141.0 | 151.0 | app2 | True | False | 49988.0 | 16.7% | 16.7% | 0.1 |
| 141.0 | 151.0 | app3 | True | False | 50062.0 | 16.7% | 16.7% | 0.1 |
| 141.0 | 151.0 | app4 | True | False | 48760.0 | 16.7% | 16.3% | -0.4 |
| 141.0 | 151.0 | app5 | True | False | 48714.0 | 16.7% | 16.3% | -0.4 |
| 141.0 | 151.0 | app6 | True | False | 50126.0 | 16.7% | 16.8% | 0.1 |
| 151.0 | 161.0 | app1 | True | False | 51402.0 | 16.7% | 16.8% | 0.2 |
| 151.0 | 161.0 | app2 | True | False | 51374.0 | 16.7% | 16.8% | 0.1 |
| 151.0 | 161.0 | app3 | True | False | 51386.0 | 16.7% | 16.8% | 0.1 |
| 151.0 | 161.0 | app4 | True | False | 51432.0 | 16.7% | 16.8% | 0.2 |
| 151.0 | 161.0 | app5 | True | False | 49984.0 | 16.7% | 16.4% | -0.3 |
| 151.0 | 161.0 | app6 | True | False | 50054.0 | 16.7% | 16.4% | -0.3 |
| 161.0 | 171.0 | app1 | True | False | 48766.0 | 16.7% | 16.2% | -0.4 |
| 161.0 | 171.0 | app2 | True | False | 49998.0 | 16.7% | 16.6% | -0.0 |
| 161.0 | 171.0 | app3 | True | False | 50130.0 | 16.7% | 16.7% | 0.0 |
| 161.0 | 171.0 | app4 | True | False | 50008.0 | 16.7% | 16.6% | -0.0 |
| 161.0 | 171.0 | app5 | True | False | 51452.0 | 16.7% | 17.1% | 0.5 |
| 161.0 | 171.0 | app6 | True | False | 50078.0 | 16.7% | 16.7% | 0.0 |
| 171.0 | 181.0 | app1 | True | False | 50052.0 | 16.7% | 16.6% | -0.1 |
| 171.0 | 181.0 | app2 | True | False | 49948.0 | 16.7% | 16.6% | -0.1 |
| 171.0 | 181.0 | app3 | True | False | 52696.0 | 16.7% | 17.5% | 0.8 |
| 171.0 | 181.0 | app4 | True | False | 49998.0 | 16.7% | 16.6% | -0.1 |
| 171.0 | 181.0 | app5 | True | False | 47334.0 | 16.7% | 15.7% | -1.0 |
| 171.0 | 181.0 | app6 | True | False | 51520.0 | 16.7% | 17.1% | 0.4 |
| 181.0 | 191.0 | app1 | True | False | 50076.0 | 16.7% | 16.4% | -0.3 |
| 181.0 | 191.0 | app2 | True | False | 51346.0 | 16.7% | 16.8% | 0.1 |
| 181.0 | 191.0 | app3 | True | False | 48632.0 | 16.7% | 15.9% | -0.8 |
| 181.0 | 191.0 | app4 | True | False | 51294.0 | 16.7% | 16.8% | 0.1 |
| 181.0 | 191.0 | app5 | True | False | 52844.0 | 16.7% | 17.3% | 0.6 |
| 181.0 | 191.0 | app6 | True | False | 51422.0 | 16.7% | 16.8% | 0.2 |
| 191.0 | 201.0 | app1 | True | False | 52694.0 | 16.7% | 17.2% | 0.6 |
| 191.0 | 201.0 | app2 | True | False | 50060.0 | 16.7% | 16.4% | -0.3 |
| 191.0 | 201.0 | app3 | True | False | 50006.0 | 16.7% | 16.4% | -0.3 |
| 191.0 | 201.0 | app4 | True | False | 51434.0 | 16.7% | 16.8% | 0.2 |
| 191.0 | 201.0 | app5 | True | False | 50032.0 | 16.7% | 16.4% | -0.3 |
| 191.0 | 201.0 | app6 | True | False | 51374.0 | 16.7% | 16.8% | 0.1 |
| 201.0 | 211.0 | app1 | True | False | 50086.0 | 16.7% | 16.4% | -0.3 |
| 201.0 | 211.0 | app2 | True | False | 51386.0 | 16.7% | 16.8% | 0.1 |
| 201.0 | 211.0 | app3 | True | False | 51528.0 | 16.7% | 16.9% | 0.2 |
| 201.0 | 211.0 | app4 | True | False | 49978.0 | 16.7% | 16.3% | -0.3 |
| 201.0 | 211.0 | app5 | True | False | 51354.0 | 16.7% | 16.8% | 0.1 |
| 201.0 | 211.0 | app6 | True | False | 51344.0 | 16.7% | 16.8% | 0.1 |
| 211.0 | 221.0 | app1 | True | False | 51432.0 | 16.7% | 17.1% | 0.4 |
| 211.0 | 221.0 | app2 | True | False | 50022.0 | 16.7% | 16.6% | -0.1 |
| 211.0 | 221.0 | app3 | True | False | 50060.0 | 16.7% | 16.6% | -0.1 |
| 211.0 | 221.0 | app4 | True | False | 51314.0 | 16.7% | 17.0% | 0.3 |
| 211.0 | 221.0 | app5 | True | False | 50008.0 | 16.7% | 16.6% | -0.1 |
| 211.0 | 221.0 | app6 | True | False | 48730.0 | 16.7% | 16.2% | -0.5 |
| 221.0 | 231.0 | app1 | True | False | 49966.0 | 16.7% | 16.1% | -0.5 |
| 221.0 | 231.0 | app2 | True | False | 51466.0 | 16.7% | 16.6% | -0.0 |
| 221.0 | 231.0 | app3 | True | False | 51280.0 | 16.7% | 16.6% | -0.1 |
| 221.0 | 231.0 | app4 | True | False | 52790.0 | 16.7% | 17.1% | 0.4 |
| 221.0 | 231.0 | app5 | True | False | 52686.0 | 16.7% | 17.0% | 0.4 |
| 221.0 | 231.0 | app6 | True | False | 51392.0 | 16.7% | 16.6% | -0.1 |
| 231.0 | 241.0 | app1 | True | False | 47286.0 | 16.7% | 17.1% | 0.5 |
| 231.0 | 241.0 | app2 | True | False | 46030.0 | 16.7% | 16.7% | 0.0 |
| 231.0 | 241.0 | app3 | True | False | 47384.0 | 16.7% | 17.2% | 0.5 |
| 231.0 | 241.0 | app4 | True | False | 44620.0 | 16.7% | 16.2% | -0.5 |
| 231.0 | 241.0 | app5 | True | False | 43268.0 | 16.7% | 15.7% | -1.0 |
| 231.0 | 241.0 | app6 | True | False | 47316.0 | 16.7% | 17.1% | 0.5 |
| 241.0 | 251.0 | app1 | False | n/a | 47352.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 47280.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | n/a | 45848.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app4 | False | n/a | 47252.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app5 | False | n/a | 47386.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app6 | False | n/a | 47334.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 2696.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 4036.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | False | n/a | 4048.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | False | n/a | 4062.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | False | n/a | 1358.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | False | n/a | 1358.0 | n/a | n/a | n/a |
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
| 311.0 | 322.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 322.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 322.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 322.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 322.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 322.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
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
| 532.0 | 543.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 543.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 543.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 543.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 543.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 543.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 543.0 | 545.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 543.0 | 545.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 543.0 | 545.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 543.0 | 545.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 543.0 | 545.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 543.0 | 545.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 43 | 1058ms | 3969ms | 7850ms |
| 0.0 | 10.0 | app2 | ok | 43 | 0ms | 3656ms | 4866ms |
| 0.0 | 10.0 | app3 | ok | 42 | 0ms | 3688ms | 4869ms |
| 0.0 | 10.0 | app4 | ok | 42 | 0ms | 3500ms | 4850ms |
| 0.0 | 10.0 | app5 | ok | 43 | 0ms | 3656ms | 4866ms |
| 0.0 | 10.0 | app6 | ok | 43 | 1058ms | 3806ms | 4881ms |
| 10.0 | 20.0 | app1 | ok | 34 | 3587ms | 5750ms | 9575ms |
| 10.0 | 20.0 | app2 | ok | 34 | 3462ms | 4769ms | 8300ms |
| 10.0 | 20.0 | app3 | ok | 35 | 3616ms | 4866ms | 9125ms |
| 10.0 | 20.0 | app4 | ok | 34 | 3482ms | 4696ms | 4970ms |
| 10.0 | 20.0 | app5 | ok | 35 | 3413ms | 4760ms | 8250ms |
| 10.0 | 20.0 | app6 | ok | 34 | 3704ms | 4963ms | 9433ms |
| 20.0 | 30.0 | app1 | ok | 43 | 3319ms | 4802ms | 8925ms |
| 20.0 | 30.0 | app2 | ok | 42 | 3417ms | 4817ms | 8950ms |
| 20.0 | 30.0 | app3 | ok | 41 | 3102ms | 4620ms | 4962ms |
| 20.0 | 30.0 | app4 | ok | 43 | 3208ms | 4642ms | 4964ms |
| 20.0 | 30.0 | app5 | ok | 37 | 2989ms | 4598ms | 4960ms |
| 20.0 | 30.0 | app6 | ok | 42 | 3214ms | 4714ms | 7900ms |
| 30.0 | 40.0 | app1 | ok | 31 | 3650ms | 4890ms | 9225ms |
| 30.0 | 40.0 | app2 | ok | 33 | 3281ms | 4656ms | 4966ms |
| 30.0 | 40.0 | app3 | ok | 33 | 3510ms | 4779ms | 8350ms |
| 30.0 | 40.0 | app4 | ok | 33 | 3616ms | 4795ms | 8350ms |
| 30.0 | 40.0 | app5 | ok | 37 | 3405ms | 4681ms | 4968ms |
| 30.0 | 40.0 | app6 | ok | 34 | 3365ms | 4673ms | 4967ms |
| 40.0 | 50.0 | app1 | ok | 41 | 3646ms | 4785ms | 7950ms |
| 40.0 | 50.0 | app2 | ok | 41 | 3493ms | 4699ms | 4970ms |
| 40.0 | 50.0 | app3 | ok | 42 | 3684ms | 4789ms | 7900ms |
| 40.0 | 50.0 | app4 | ok | 41 | 3615ms | 4723ms | 4972ms |
| 40.0 | 50.0 | app5 | ok | 40 | 3603ms | 4779ms | 8000ms |
| 40.0 | 50.0 | app6 | ok | 40 | 3716ms | 4797ms | 8000ms |
| 50.0 | 60.0 | app1 | ok | 33 | 3664ms | 4802ms | 8350ms |
| 50.0 | 60.0 | app2 | ok | 33 | 3527ms | 4705ms | 4971ms |
| 50.0 | 60.0 | app3 | ok | 32 | 3611ms | 4796ms | 8400ms |
| 50.0 | 60.0 | app4 | ok | 33 | 3472ms | 4694ms | 4969ms |
| 50.0 | 60.0 | app5 | ok | 34 | 3365ms | 4673ms | 4967ms |
| 50.0 | 60.0 | app6 | ok | 33 | 3578ms | 4716ms | 4972ms |
| 60.0 | 70.0 | app1 | ok | 43 | 3715ms | 4910ms | 9283ms |
| 60.0 | 70.0 | app2 | ok | 42 | 3581ms | 4716ms | 4972ms |
| 60.0 | 70.0 | app3 | ok | 43 | 3586ms | 4717ms | 4972ms |
| 60.0 | 70.0 | app4 | ok | 43 | 3622ms | 4724ms | 4972ms |
| 60.0 | 70.0 | app5 | ok | 43 | 3419ms | 4684ms | 4968ms |
| 60.0 | 70.0 | app6 | ok | 42 | 3611ms | 4778ms | 7900ms |
| 70.0 | 80.0 | app1 | ok | 30 | 3661ms | 4732ms | 4973ms |
| 70.0 | 80.0 | app2 | ok | 31 | 3664ms | 4733ms | 4973ms |
| 70.0 | 80.0 | app3 | ok | 30 | 3661ms | 4732ms | 4973ms |
| 70.0 | 80.0 | app4 | ok | 30 | 3704ms | 4815ms | 8500ms |
| 70.0 | 80.0 | app5 | ok | 29 | 3550ms | 4710ms | 4971ms |
| 70.0 | 80.0 | app6 | ok | 31 | 3565ms | 4713ms | 4971ms |
| 80.0 | 90.0 | app1 | ok | 54 | 3355ms | 4776ms | 8650ms |
| 80.0 | 90.0 | app2 | ok | 54 | 3333ms | 4833ms | 9100ms |
| 80.0 | 90.0 | app3 | ok | 53 | 3365ms | 4724ms | 7350ms |
| 80.0 | 90.0 | app4 | ok | 54 | 3311ms | 4770ms | 8650ms |
| 80.0 | 90.0 | app5 | ok | 54 | 3176ms | 4635ms | 4964ms |
| 80.0 | 90.0 | app6 | ok | 53 | 3412ms | 4845ms | 9117ms |
| 90.0 | 100.0 | app1 | ok | 21 | 3819ms | 4986ms | 9475ms |
| 90.0 | 100.0 | app2 | ok | 21 | 3542ms | 4708ms | 4971ms |
| 90.0 | 100.0 | app3 | ok | 22 | 3594ms | 4969ms | 9450ms |
| 90.0 | 100.0 | app4 | ok | 20 | 3684ms | 4737ms | 4974ms |
| 90.0 | 100.0 | app5 | ok | 21 | 3542ms | 4708ms | 4971ms |
| 90.0 | 100.0 | app6 | ok | 21 | 3750ms | 4855ms | 8950ms |
| 100.0 | 111.0 | app1 | ok | 39 | 3380ms | 4824ms | 9025ms |
| 100.0 | 111.0 | app2 | ok | 38 | 3173ms | 4635ms | 4963ms |
| 100.0 | 111.0 | app3 | ok | 40 | 3387ms | 4677ms | 4968ms |
| 100.0 | 111.0 | app4 | ok | 40 | 3333ms | 4815ms | 9000ms |
| 100.0 | 111.0 | app5 | ok | 39 | 3050ms | 4610ms | 4961ms |
| 100.0 | 111.0 | app6 | ok | 39 | 3221ms | 4721ms | 8050ms |
| 111.0 | 121.0 | app1 | ok | 42 | 3643ms | 4843ms | 8950ms |
| 111.0 | 121.0 | app2 | ok | 42 | 3716ms | 4851ms | 8950ms |
| 111.0 | 121.0 | app3 | ok | 40 | 3561ms | 4773ms | 8000ms |
| 111.0 | 121.0 | app4 | ok | 41 | 3719ms | 4744ms | 4974ms |
| 111.0 | 121.0 | app5 | ok | 41 | 3536ms | 4707ms | 4971ms |
| 111.0 | 121.0 | app6 | ok | 42 | 3611ms | 4778ms | 7900ms |
| 121.0 | 131.0 | app1 | ok | 40 | 3304ms | 4732ms | 8000ms |
| 121.0 | 131.0 | app2 | ok | 41 | 3380ms | 4898ms | 9317ms |
| 121.0 | 131.0 | app3 | ok | 41 | 3405ms | 4819ms | 8975ms |
| 121.0 | 131.0 | app4 | ok | 41 | 3458ms | 4825ms | 8975ms |
| 121.0 | 131.0 | app5 | ok | 41 | 3194ms | 4713ms | 7950ms |
| 121.0 | 131.0 | app6 | ok | 40 | 3269ms | 4808ms | 9000ms |
| 131.0 | 141.0 | app1 | ok | 30 | 2941ms | 4706ms | 8500ms |
| 131.0 | 141.0 | app2 | ok | 30 | 2794ms | 4559ms | 4956ms |
| 131.0 | 141.0 | app3 | ok | 30 | 2941ms | 4706ms | 8500ms |
| 131.0 | 141.0 | app4 | ok | 30 | 2656ms | 4531ms | 4953ms |
| 131.0 | 141.0 | app5 | ok | 30 | 2917ms | 4583ms | 4958ms |
| 131.0 | 141.0 | app6 | ok | 31 | 3062ms | 4613ms | 4961ms |
| 141.0 | 151.0 | app1 | ok | 41 | 3785ms | 4924ms | 9317ms |
| 141.0 | 151.0 | app2 | ok | 41 | 3607ms | 4779ms | 7950ms |
| 141.0 | 151.0 | app3 | ok | 41 | 3682ms | 4791ms | 7950ms |
| 141.0 | 151.0 | app4 | ok | 40 | 3571ms | 4714ms | 4971ms |
| 141.0 | 151.0 | app5 | ok | 41 | 3615ms | 4723ms | 4972ms |
| 141.0 | 151.0 | app6 | ok | 41 | 3536ms | 4707ms | 4971ms |
| 151.0 | 161.0 | app1 | ok | 32 | 3667ms | 4733ms | 4973ms |
| 151.0 | 161.0 | app2 | ok | 31 | 3616ms | 4723ms | 4972ms |
| 151.0 | 161.0 | app3 | ok | 31 | 3705ms | 4812ms | 8450ms |
| 151.0 | 161.0 | app4 | ok | 32 | 3661ms | 4804ms | 8400ms |
| 151.0 | 161.0 | app5 | ok | 31 | 3450ms | 4690ms | 4969ms |
| 151.0 | 161.0 | app6 | ok | 30 | 3654ms | 4808ms | 8500ms |
| 161.0 | 171.0 | app1 | ok | 38 | 3426ms | 4833ms | 9050ms |
| 161.0 | 171.0 | app2 | ok | 38 | 3448ms | 4759ms | 8100ms |
| 161.0 | 171.0 | app3 | ok | 38 | 3365ms | 4827ms | 9050ms |
| 161.0 | 171.0 | app4 | ok | 38 | 3241ms | 4648ms | 4965ms |
| 161.0 | 171.0 | app5 | ok | 38 | 3241ms | 4648ms | 4965ms |
| 161.0 | 171.0 | app6 | ok | 38 | 3269ms | 4731ms | 8100ms |
| 171.0 | 181.0 | app1 | ok | 40 | 3561ms | 4773ms | 8000ms |
| 171.0 | 181.0 | app2 | ok | 40 | 3714ms | 4857ms | 9000ms |
| 171.0 | 181.0 | app3 | ok | 41 | 3682ms | 4791ms | 7950ms |
| 171.0 | 181.0 | app4 | ok | 40 | 3611ms | 4722ms | 4972ms |
| 171.0 | 181.0 | app5 | ok | 40 | 3643ms | 4786ms | 8000ms |
| 171.0 | 181.0 | app6 | ok | 41 | 3607ms | 4779ms | 7950ms |
| 181.0 | 191.0 | app1 | ok | 41 | 3615ms | 4723ms | 4972ms |
| 181.0 | 191.0 | app2 | ok | 42 | 3618ms | 4724ms | 4972ms |
| 181.0 | 191.0 | app3 | ok | 41 | 3750ms | 4858ms | 8975ms |
| 181.0 | 191.0 | app4 | ok | 42 | 3500ms | 4700ms | 4970ms |
| 181.0 | 191.0 | app5 | ok | 42 | 3542ms | 4708ms | 4971ms |
| 181.0 | 191.0 | app6 | ok | 41 | 3646ms | 4785ms | 7950ms |
| 191.0 | 201.0 | app1 | ok | 35 | 3380ms | 4676ms | 4968ms |
| 191.0 | 201.0 | app2 | ok | 35 | 3380ms | 4676ms | 4968ms |
| 191.0 | 201.0 | app3 | ok | 35 | 3472ms | 4769ms | 8250ms |
| 191.0 | 201.0 | app4 | ok | 36 | 3269ms | 4654ms | 4965ms |
| 191.0 | 201.0 | app5 | ok | 35 | 3317ms | 4663ms | 4966ms |
| 191.0 | 201.0 | app6 | ok | 35 | 3510ms | 4856ms | 9125ms |
| 201.0 | 211.0 | app1 | ok | 44 | 3716ms | 4905ms | 9267ms |
| 201.0 | 211.0 | app2 | ok | 43 | 3615ms | 4777ms | 7850ms |
| 201.0 | 211.0 | app3 | ok | 44 | 3456ms | 4750ms | 7800ms |
| 201.0 | 211.0 | app4 | ok | 42 | 3571ms | 4771ms | 7900ms |
| 201.0 | 211.0 | app5 | ok | 43 | 3320ms | 4664ms | 4966ms |
| 201.0 | 211.0 | app6 | ok | 43 | 3646ms | 4840ms | 8925ms |
| 211.0 | 221.0 | app1 | ok | 33 | 3413ms | 4683ms | 4968ms |
| 211.0 | 221.0 | app2 | ok | 34 | 3482ms | 4696ms | 4970ms |
| 211.0 | 221.0 | app3 | ok | 34 | 3519ms | 4778ms | 8300ms |
| 211.0 | 221.0 | app4 | ok | 34 | 3482ms | 4696ms | 4970ms |
| 211.0 | 221.0 | app5 | ok | 35 | 3177ms | 4635ms | 4964ms |
| 211.0 | 221.0 | app6 | ok | 35 | 3542ms | 4708ms | 4971ms |
| 221.0 | 231.0 | app1 | ok | 31 | 3616ms | 4723ms | 4972ms |
| 221.0 | 231.0 | app2 | ok | 30 | 3661ms | 4732ms | 4973ms |
| 221.0 | 231.0 | app3 | ok | 30 | 3661ms | 4732ms | 4973ms |
| 221.0 | 231.0 | app4 | ok | 30 | 3750ms | 4750ms | 4975ms |
| 221.0 | 231.0 | app5 | ok | 30 | 3500ms | 4700ms | 4970ms |
| 221.0 | 231.0 | app6 | ok | 30 | 3646ms | 4896ms | 9250ms |
| 231.0 | 241.0 | app1 | ok | 42 | 3523ms | 7375ms | 9737ms |
| 231.0 | 241.0 | app2 | ok | 43 | 3490ms | 6929ms | 9693ms |
| 231.0 | 241.0 | app3 | ok | 42 | 3500ms | 6500ms | 9650ms |
| 231.0 | 241.0 | app4 | ok | 43 | 3490ms | 6929ms | 9693ms |
| 231.0 | 241.0 | app5 | ok | 42 | 3261ms | 5800ms | 9580ms |
| 231.0 | 241.0 | app6 | ok | 42 | 3333ms | 5800ms | 9580ms |
| 241.0 | 251.0 | app1 | ok | 16 | 3833ms | 4900ms | 9200ms |
| 241.0 | 251.0 | app2 | ok | 16 | 3833ms | 4900ms | 9200ms |
| 241.0 | 251.0 | app3 | ok | 17 | 3750ms | 4883ms | 9150ms |
| 241.0 | 251.0 | app4 | ok | 16 | 3750ms | 4750ms | 4975ms |
| 241.0 | 251.0 | app5 | ok | 14 | 3654ms | 4731ms | 4973ms |
| 241.0 | 251.0 | app6 | ok | 15 | 3661ms | 4732ms | 4973ms |
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
| 311.0 | 322.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 322.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 322.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 322.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 322.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 322.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 532.0 | 543.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 543.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 543.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 543.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 543.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 543.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 543.0 | 545.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 543.0 | 545.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 543.0 | 545.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 543.0 | 545.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 543.0 | 545.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 543.0 | 545.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1127910 | 56226 | 1184136.0 | 0.0% | 1210618.0 | 1240362.0 | -2.4% | True |
| app2 | 1129140 | 56011 | 1185151.0 | 0.0% | 1210108.0 | 1241162.0 | -2.5% | True |
| app3 | 1127910 | 56119 | 1184029.0 | 0.0% | 1210316.0 | 1240148.0 | -2.4% | True |
| app4 | 1129140 | 55999 | 1185139.0 | 0.0% | 1207286.0 | 1241138.0 | -2.7% | True |
| app5 | 1124220 | 55964 | 1180184.0 | 0.0% | 1199632.0 | 1236148.0 | -3.0% | True |
| app6 | 1126680 | 56164 | 1182844.0 | 0.0% | 1210666.0 | 1239008.0 | -2.3% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 917 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 918 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 918 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app4 | 918 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app5 | 915 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app6 | 916 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5502). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5502 | 0.050ms | 0.100ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 512330 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 917 | 8530ms | 13705ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 918 | 8496ms | 13658ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app3 | ok | 917 | 8510ms | 13659ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app4 | ok | 918 | 8514ms | 13696ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app5 | ok | 914 | 8230ms | 13282ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app6 | ok | 916 | 8516ms | 13721ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5500 | 8468ms | 13635ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (55 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2625ms | 5617ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 3100ms | 5475ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app3 | ok | 3000ms | 5450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app4 | ok | 3000ms | 5000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app5 | ok | 2750ms | 5725ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app6 | ok | 3125ms | 5425ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 7750ms | 12000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 7526ms | 11750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app3 | ok | 7700ms | 12625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app4 | ok | 7684ms | 13000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app5 | ok | 7667ms | 12000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app6 | ok | 7706ms | 11917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 8385ms | 13917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 8400ms | 13643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app3 | ok | 8714ms | 14000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app4 | ok | 8267ms | 13417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app5 | ok | 8615ms | 14050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app6 | ok | 8643ms | 13972ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 8882ms | 13972ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 9000ms | 14100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app3 | ok | 8812ms | 14025ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app4 | ok | 8812ms | 13972ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app5 | ok | 7824ms | 13150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app6 | ok | 8769ms | 14136ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 8538ms | 13972ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 8571ms | 13944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app3 | ok | 8579ms | 13150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app4 | ok | 8467ms | 13679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app5 | ok | 8652ms | 12562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app6 | ok | 8500ms | 13150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 8222ms | 11833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 8381ms | 10250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app3 | ok | 8667ms | 13100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app4 | ok | 8571ms | 12625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app5 | ok | 8222ms | 10500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app6 | ok | 8444ms | 13100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 8722ms | 13679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 8684ms | 13458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app3 | ok | 8588ms | 13643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app4 | ok | 8556ms | 13417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app5 | ok | 8533ms | 13812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app6 | ok | 8765ms | 13844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 8727ms | 13100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 8389ms | 13050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app3 | ok | 8667ms | 12750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app4 | ok | 8652ms | 11917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app5 | ok | 8273ms | 9827ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app6 | ok | 8650ms | 13150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 8455ms | 14075ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 8700ms | 14205ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app3 | ok | 8583ms | 14075ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app4 | ok | 8692ms | 14075ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app5 | ok | 8364ms | 14000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app6 | ok | 8692ms | 14075ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 8571ms | 13875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 8538ms | 13972ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app3 | ok | 8583ms | 14114ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app4 | ok | 8538ms | 13972ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app5 | ok | 8091ms | 13844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app6 | ok | 8429ms | 13812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | app1 | ok | 8533ms | 13812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | app2 | ok | 8611ms | 13607ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | app3 | ok | 8333ms | 12000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | app4 | ok | 8312ms | 13150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | app5 | ok | 8067ms | 13050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | app6 | ok | 8647ms | 13679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 8667ms | 13643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 8412ms | 13150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app3 | ok | 8824ms | 13875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app4 | ok | 8500ms | 13643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app5 | ok | 8176ms | 11917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app6 | ok | 8667ms | 13643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 8818ms | 14205ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 8818ms | 14229ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app3 | ok | 8364ms | 14050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app4 | ok | 9000ms | 14250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app5 | ok | 8400ms | 14100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app6 | ok | 8769ms | 14100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 8529ms | 13607ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 8556ms | 13417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app3 | ok | 8706ms | 13812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app4 | ok | 8647ms | 13781ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app5 | ok | 8278ms | 12562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app6 | ok | 8556ms | 13417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 8471ms | 13417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 8600ms | 13844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app3 | ok | 8562ms | 13679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app4 | ok | 8667ms | 13875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app5 | ok | 8429ms | 13714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app6 | ok | 8733ms | 13972ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 8500ms | 13643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 8375ms | 13417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app3 | ok | 8364ms | 14050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app4 | ok | 8429ms | 13812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app5 | ok | 8077ms | 13458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app6 | ok | 8385ms | 13844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 8750ms | 13875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 8529ms | 13458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app3 | ok | 8333ms | 13458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app4 | ok | 8583ms | 14075ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app5 | ok | 8312ms | 13375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app6 | ok | 8438ms | 13458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 8647ms | 13679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 8500ms | 13150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app3 | ok | 8529ms | 13607ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app4 | ok | 8412ms | 13150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app5 | ok | 8278ms | 10625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app6 | ok | 8625ms | 13812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 8385ms | 13844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 8625ms | 13812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app3 | ok | 8588ms | 13500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app4 | ok | 8571ms | 13944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app5 | ok | 8250ms | 13917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app6 | ok | 8625ms | 13812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 8438ms | 13607ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 8647ms | 13679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app3 | ok | 8562ms | 13679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app4 | ok | 8714ms | 13375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app5 | ok | 8333ms | 13458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app6 | ok | 8353ms | 13100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 8722ms | 13679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 8667ms | 13944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app3 | ok | 8533ms | 13812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app4 | ok | 8750ms | 13875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app5 | ok | 8400ms | 13643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app6 | ok | 8857ms | 14136ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 8696ms | 12625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 8450ms | 11917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app3 | ok | 8350ms | 10375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app4 | ok | 8400ms | 11833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app5 | ok | 8333ms | 9919ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app6 | ok | 8222ms | 10500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 8652ms | 11917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 8720ms | 11833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app3 | ok | 8640ms | 10250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app4 | ok | 8429ms | 11750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app5 | ok | 8053ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app6 | ok | 8667ms | 13100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 8556ms | 14205ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 8444ms | 14150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app3 | ok | 8700ms | 14205ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app4 | ok | 8778ms | 14250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app5 | ok | 8500ms | 14083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app6 | ok | 8500ms | 14125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 9308ms | 14327ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 9300ms | 14375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app3 | ok | 9143ms | 14227ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app4 | ok | 9417ms | 14375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app5 | ok | 8733ms | 13906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app6 | ok | 9308ms | 14327ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app3 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app4 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app5 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app6 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 311.0 | 322.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 322.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 322.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 322.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 322.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 322.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 532.0 | 543.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 543.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 543.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 543.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 543.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 543.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 543.0 | 545.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 543.0 | 545.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 543.0 | 545.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 543.0 | 545.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 543.0 | 545.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 543.0 | 545.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
