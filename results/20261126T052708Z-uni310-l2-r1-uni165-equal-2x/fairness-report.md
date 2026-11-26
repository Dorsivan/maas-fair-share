# Fairness benchmark: six-group-board-case (uni310-l2-r1-uni165-equal-2x)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-79f9bbd5f9-w7qq2` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T05:28:17Z` |
| Run end | `2026-11-26T05:33:59Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 36 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/36 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 66.00 | 2.0625 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 16.7 | 64 | 937 | 200=937 | 17.1 | 19.7 | 1242748.0 | 16.7% | 16.7% | 0.0 | 16.7% | 0.0 | 16.7% | 0.0 | 86.7s | 98.9% | 937.0 |
| app2 | 16.7 | 64 | 936 | 200=936 | 17.1 | 19.8 | 1243834.0 | 16.7% | 16.7% | 0.0 | 16.7% | 0.1 | 16.7% | 0.0 | 86.7s | 98.9% | 936.0 |
| app3 | 16.7 | 64 | 935 | 200=935 | 17.1 | 19.6 | 1236712.0 | 16.7% | 16.7% | 0.0 | 16.6% | -0.0 | 16.7% | -0.0 | 86.7s | 98.9% | 935.0 |
| app4 | 16.7 | 64 | 937 | 200=937 | 17.1 | 19.6 | 1233382.0 | 16.7% | 16.7% | 0.0 | 16.6% | -0.1 | 16.7% | 0.0 | 86.7s | 98.9% | 937.0 |
| app5 | 16.7 | 64 | 936 | 200=936 | 17.1 | 19.8 | 1234156.0 | 16.7% | 16.7% | 0.0 | 16.6% | -0.1 | 16.7% | 0.0 | 86.7s | 98.9% | 936.0 |
| app6 | 16.7 | 64 | 934 | 000=1, 200=933 | 16.9 | 19.5 | 1244786.0 | 16.7% | 16.7% | 0.0 | 16.7% | 0.1 | 16.6% | -0.0 | 86.7s | 98.9% | 934.0 |
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

**Windows** (35 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app3 | True | False | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app4 | True | False | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app5 | True | False | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app6 | True | False | 2710.0 | 16.7% | 100.0% | 83.3 |
| 10.0 | 20.0 | app1 | True | False | 43280.0 | 16.7% | 17.7% | 1.0 |
| 10.0 | 20.0 | app2 | True | False | 45940.0 | 16.7% | 18.8% | 2.1 |
| 10.0 | 20.0 | app3 | True | False | 40600.0 | 16.7% | 16.6% | -0.1 |
| 10.0 | 20.0 | app4 | True | False | 32420.0 | 16.7% | 13.2% | -3.4 |
| 10.0 | 20.0 | app5 | True | False | 36390.0 | 16.7% | 14.9% | -1.8 |
| 10.0 | 20.0 | app6 | True | False | 46094.0 | 16.7% | 18.8% | 2.2 |
| 20.0 | 30.0 | app1 | True | False | 50032.0 | 16.7% | 16.2% | -0.4 |
| 20.0 | 30.0 | app2 | True | False | 51344.0 | 16.7% | 16.7% | -0.0 |
| 20.0 | 30.0 | app3 | True | False | 49958.0 | 16.7% | 16.2% | -0.5 |
| 20.0 | 30.0 | app4 | True | False | 52788.0 | 16.7% | 17.1% | 0.5 |
| 20.0 | 30.0 | app5 | True | False | 51390.0 | 16.7% | 16.7% | 0.0 |
| 20.0 | 30.0 | app6 | True | False | 52800.0 | 16.7% | 17.1% | 0.5 |
| 30.0 | 40.0 | app1 | True | False | 50076.0 | 16.7% | 16.5% | -0.2 |
| 30.0 | 40.0 | app2 | True | False | 49924.0 | 16.7% | 16.4% | -0.3 |
| 30.0 | 40.0 | app3 | True | False | 51430.0 | 16.7% | 16.9% | 0.2 |
| 30.0 | 40.0 | app4 | True | False | 51410.0 | 16.7% | 16.9% | 0.2 |
| 30.0 | 40.0 | app5 | True | False | 51348.0 | 16.7% | 16.9% | 0.2 |
| 30.0 | 40.0 | app6 | True | False | 50102.0 | 16.7% | 16.5% | -0.2 |
| 40.0 | 50.0 | app1 | True | False | 51378.0 | 16.7% | 16.8% | 0.2 |
| 40.0 | 50.0 | app2 | True | False | 51360.0 | 16.7% | 16.8% | 0.1 |
| 40.0 | 50.0 | app3 | True | False | 49986.0 | 16.7% | 16.4% | -0.3 |
| 40.0 | 50.0 | app4 | True | False | 51362.0 | 16.7% | 16.8% | 0.1 |
| 40.0 | 50.0 | app5 | True | False | 49982.0 | 16.7% | 16.4% | -0.3 |
| 40.0 | 50.0 | app6 | True | False | 51390.0 | 16.7% | 16.8% | 0.2 |
| 50.0 | 60.0 | app1 | True | False | 52808.0 | 16.7% | 17.2% | 0.5 |
| 50.0 | 60.0 | app2 | True | False | 51324.0 | 16.7% | 16.7% | 0.1 |
| 50.0 | 60.0 | app3 | True | False | 51454.0 | 16.7% | 16.8% | 0.1 |
| 50.0 | 60.0 | app4 | True | False | 51402.0 | 16.7% | 16.7% | 0.1 |
| 50.0 | 60.0 | app5 | True | False | 51312.0 | 16.7% | 16.7% | 0.0 |
| 50.0 | 60.0 | app6 | True | False | 48676.0 | 16.7% | 15.9% | -0.8 |
| 60.0 | 70.0 | app1 | True | False | 51424.0 | 16.7% | 16.6% | -0.1 |
| 60.0 | 70.0 | app2 | True | False | 52792.0 | 16.7% | 17.0% | 0.4 |
| 60.0 | 70.0 | app3 | True | False | 52726.0 | 16.7% | 17.0% | 0.4 |
| 60.0 | 70.0 | app4 | True | False | 50022.0 | 16.7% | 16.1% | -0.5 |
| 60.0 | 70.0 | app5 | True | False | 50046.0 | 16.7% | 16.2% | -0.5 |
| 60.0 | 70.0 | app6 | True | False | 52726.0 | 16.7% | 17.0% | 0.4 |
| 70.0 | 80.0 | app1 | True | False | 52702.0 | 16.7% | 17.2% | 0.6 |
| 70.0 | 80.0 | app2 | True | False | 49982.0 | 16.7% | 16.4% | -0.3 |
| 70.0 | 80.0 | app3 | True | False | 47414.0 | 16.7% | 15.5% | -1.2 |
| 70.0 | 80.0 | app4 | True | False | 51408.0 | 16.7% | 16.8% | 0.2 |
| 70.0 | 80.0 | app5 | True | False | 52686.0 | 16.7% | 17.2% | 0.6 |
| 70.0 | 80.0 | app6 | True | False | 51394.0 | 16.7% | 16.8% | 0.2 |
| 80.0 | 90.0 | app1 | True | False | 45984.0 | 16.7% | 15.5% | -1.1 |
| 80.0 | 90.0 | app2 | True | False | 49984.0 | 16.7% | 16.9% | 0.2 |
| 80.0 | 90.0 | app3 | True | False | 52826.0 | 16.7% | 17.8% | 1.2 |
| 80.0 | 90.0 | app4 | True | False | 49924.0 | 16.7% | 16.9% | 0.2 |
| 80.0 | 90.0 | app5 | True | False | 48624.0 | 16.7% | 16.4% | -0.2 |
| 80.0 | 90.0 | app6 | True | False | 48732.0 | 16.7% | 16.5% | -0.2 |
| 90.0 | 100.0 | app1 | True | False | 52684.0 | 16.7% | 17.1% | 0.4 |
| 90.0 | 100.0 | app2 | True | False | 50092.0 | 16.7% | 16.2% | -0.4 |
| 90.0 | 100.0 | app3 | True | False | 51440.0 | 16.7% | 16.7% | 0.0 |
| 90.0 | 100.0 | app4 | True | False | 51336.0 | 16.7% | 16.6% | -0.0 |
| 90.0 | 100.0 | app5 | True | False | 51412.0 | 16.7% | 16.7% | 0.0 |
| 90.0 | 100.0 | app6 | True | False | 51364.0 | 16.7% | 16.7% | -0.0 |
| 100.0 | 110.0 | app1 | True | False | 51340.0 | 16.7% | 16.8% | 0.1 |
| 100.0 | 110.0 | app2 | True | False | 51410.0 | 16.7% | 16.8% | 0.2 |
| 100.0 | 110.0 | app3 | True | False | 50050.0 | 16.7% | 16.4% | -0.3 |
| 100.0 | 110.0 | app4 | True | False | 51498.0 | 16.7% | 16.8% | 0.2 |
| 100.0 | 110.0 | app5 | True | False | 51304.0 | 16.7% | 16.8% | 0.1 |
| 100.0 | 110.0 | app6 | True | False | 50036.0 | 16.7% | 16.4% | -0.3 |
| 110.0 | 120.0 | app1 | True | False | 49962.0 | 16.7% | 16.3% | -0.3 |
| 110.0 | 120.0 | app2 | True | False | 50036.0 | 16.7% | 16.4% | -0.3 |
| 110.0 | 120.0 | app3 | True | False | 51358.0 | 16.7% | 16.8% | 0.1 |
| 110.0 | 120.0 | app4 | True | False | 48682.0 | 16.7% | 15.9% | -0.7 |
| 110.0 | 120.0 | app5 | True | False | 52772.0 | 16.7% | 17.3% | 0.6 |
| 110.0 | 120.0 | app6 | True | False | 52824.0 | 16.7% | 17.3% | 0.6 |
| 120.0 | 130.0 | app1 | True | False | 51366.0 | 16.7% | 16.9% | 0.2 |
| 120.0 | 130.0 | app2 | True | False | 52752.0 | 16.7% | 17.3% | 0.7 |
| 120.0 | 130.0 | app3 | True | False | 50060.0 | 16.7% | 16.4% | -0.2 |
| 120.0 | 130.0 | app4 | True | False | 52804.0 | 16.7% | 17.3% | 0.7 |
| 120.0 | 130.0 | app5 | True | False | 48696.0 | 16.7% | 16.0% | -0.7 |
| 120.0 | 130.0 | app6 | True | False | 48770.0 | 16.7% | 16.0% | -0.6 |
| 130.0 | 140.0 | app1 | True | False | 48652.0 | 16.7% | 16.5% | -0.2 |
| 130.0 | 140.0 | app2 | True | False | 48640.0 | 16.7% | 16.5% | -0.2 |
| 130.0 | 140.0 | app3 | True | False | 48768.0 | 16.7% | 16.5% | -0.1 |
| 130.0 | 140.0 | app4 | True | False | 50008.0 | 16.7% | 17.0% | 0.3 |
| 130.0 | 140.0 | app5 | True | False | 49976.0 | 16.7% | 17.0% | 0.3 |
| 130.0 | 140.0 | app6 | True | False | 48706.0 | 16.7% | 16.5% | -0.1 |
| 140.0 | 150.0 | app1 | True | False | 51462.0 | 16.7% | 16.9% | 0.2 |
| 140.0 | 150.0 | app2 | True | False | 49984.0 | 16.7% | 16.4% | -0.2 |
| 140.0 | 150.0 | app3 | True | False | 51438.0 | 16.7% | 16.9% | 0.2 |
| 140.0 | 150.0 | app4 | True | False | 48692.0 | 16.7% | 16.0% | -0.7 |
| 140.0 | 150.0 | app5 | True | False | 50054.0 | 16.7% | 16.4% | -0.2 |
| 140.0 | 150.0 | app6 | True | False | 52748.0 | 16.7% | 17.3% | 0.7 |
| 150.0 | 160.0 | app1 | True | False | 52688.0 | 16.7% | 17.4% | 0.7 |
| 150.0 | 160.0 | app2 | True | False | 51382.0 | 16.7% | 17.0% | 0.3 |
| 150.0 | 160.0 | app3 | True | False | 48692.0 | 16.7% | 16.1% | -0.6 |
| 150.0 | 160.0 | app4 | True | False | 50058.0 | 16.7% | 16.5% | -0.1 |
| 150.0 | 160.0 | app5 | True | False | 50034.0 | 16.7% | 16.5% | -0.1 |
| 150.0 | 160.0 | app6 | True | False | 50016.0 | 16.7% | 16.5% | -0.2 |
| 160.0 | 170.0 | app1 | True | False | 47382.0 | 16.7% | 16.0% | -0.7 |
| 160.0 | 170.0 | app2 | True | False | 48802.0 | 16.7% | 16.5% | -0.2 |
| 160.0 | 170.0 | app3 | True | False | 50108.0 | 16.7% | 16.9% | 0.2 |
| 160.0 | 170.0 | app4 | True | False | 51410.0 | 16.7% | 17.3% | 0.7 |
| 160.0 | 170.0 | app5 | True | False | 50110.0 | 16.7% | 16.9% | 0.2 |
| 160.0 | 170.0 | app6 | True | False | 48738.0 | 16.7% | 16.4% | -0.2 |
| 170.0 | 180.0 | app1 | True | False | 49920.0 | 16.7% | 16.6% | -0.0 |
| 170.0 | 180.0 | app2 | True | False | 49918.0 | 16.7% | 16.6% | -0.0 |
| 170.0 | 180.0 | app3 | True | False | 51376.0 | 16.7% | 17.1% | 0.5 |
| 170.0 | 180.0 | app4 | True | False | 48774.0 | 16.7% | 16.3% | -0.4 |
| 170.0 | 180.0 | app5 | True | False | 49972.0 | 16.7% | 16.7% | -0.0 |
| 170.0 | 180.0 | app6 | True | False | 50034.0 | 16.7% | 16.7% | 0.0 |
| 180.0 | 191.0 | app1 | True | False | 51440.0 | 16.7% | 16.8% | 0.1 |
| 180.0 | 191.0 | app2 | True | False | 51364.0 | 16.7% | 16.7% | 0.1 |
| 180.0 | 191.0 | app3 | True | False | 51436.0 | 16.7% | 16.8% | 0.1 |
| 180.0 | 191.0 | app4 | True | False | 51386.0 | 16.7% | 16.7% | 0.1 |
| 180.0 | 191.0 | app5 | True | False | 50014.0 | 16.7% | 16.3% | -0.4 |
| 180.0 | 191.0 | app6 | True | False | 51438.0 | 16.7% | 16.8% | 0.1 |
| 191.0 | 201.0 | app1 | True | False | 43264.0 | 16.7% | 16.5% | -0.2 |
| 191.0 | 201.0 | app2 | True | False | 43308.0 | 16.7% | 16.5% | -0.2 |
| 191.0 | 201.0 | app3 | True | False | 43278.0 | 16.7% | 16.5% | -0.2 |
| 191.0 | 201.0 | app4 | True | False | 41988.0 | 16.7% | 16.0% | -0.7 |
| 191.0 | 201.0 | app5 | True | False | 46004.0 | 16.7% | 17.5% | 0.9 |
| 191.0 | 201.0 | app6 | True | False | 44666.0 | 16.7% | 17.0% | 0.3 |
| 201.0 | 211.0 | app1 | True | False | 52692.0 | 16.7% | 17.2% | 0.6 |
| 201.0 | 211.0 | app2 | True | False | 51404.0 | 16.7% | 16.8% | 0.2 |
| 201.0 | 211.0 | app3 | True | False | 51424.0 | 16.7% | 16.8% | 0.2 |
| 201.0 | 211.0 | app4 | True | False | 51388.0 | 16.7% | 16.8% | 0.1 |
| 201.0 | 211.0 | app5 | True | False | 48640.0 | 16.7% | 15.9% | -0.8 |
| 201.0 | 211.0 | app6 | True | False | 50090.0 | 16.7% | 16.4% | -0.3 |
| 211.0 | 221.0 | app1 | True | False | 50118.0 | 16.7% | 16.3% | -0.4 |
| 211.0 | 221.0 | app2 | True | False | 50086.0 | 16.7% | 16.3% | -0.4 |
| 211.0 | 221.0 | app3 | True | False | 48738.0 | 16.7% | 15.9% | -0.8 |
| 211.0 | 221.0 | app4 | True | False | 54086.0 | 16.7% | 17.6% | 0.9 |
| 211.0 | 221.0 | app5 | True | False | 52774.0 | 16.7% | 17.2% | 0.5 |
| 211.0 | 221.0 | app6 | True | False | 51360.0 | 16.7% | 16.7% | 0.1 |
| 221.0 | 231.0 | app1 | True | False | 50066.0 | 16.7% | 16.4% | -0.3 |
| 221.0 | 231.0 | app2 | True | False | 51488.0 | 16.7% | 16.8% | 0.2 |
| 221.0 | 231.0 | app3 | True | False | 52790.0 | 16.7% | 17.3% | 0.6 |
| 221.0 | 231.0 | app4 | True | False | 47342.0 | 16.7% | 15.5% | -1.2 |
| 221.0 | 231.0 | app5 | True | False | 52732.0 | 16.7% | 17.2% | 0.6 |
| 221.0 | 231.0 | app6 | True | False | 51330.0 | 16.7% | 16.8% | 0.1 |
| 231.0 | 241.0 | app1 | True | False | 47310.0 | 16.7% | 17.0% | 0.3 |
| 231.0 | 241.0 | app2 | True | False | 45952.0 | 16.7% | 16.5% | -0.2 |
| 231.0 | 241.0 | app3 | True | False | 47318.0 | 16.7% | 17.0% | 0.3 |
| 231.0 | 241.0 | app4 | True | False | 48620.0 | 16.7% | 17.5% | 0.8 |
| 231.0 | 241.0 | app5 | True | False | 44604.0 | 16.7% | 16.0% | -0.6 |
| 231.0 | 241.0 | app6 | True | False | 44650.0 | 16.7% | 16.0% | -0.6 |
| 241.0 | 251.0 | app1 | False | n/a | 50154.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 52648.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | n/a | 51384.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app4 | False | n/a | 50000.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app5 | False | n/a | 49976.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app6 | False | n/a | 51438.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 44564.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 41918.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | False | n/a | 40660.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | False | n/a | 44574.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | False | n/a | 43304.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | False | n/a | 41954.0 | n/a | n/a | n/a |
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
| 341.0 | 342.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 342.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 342.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 342.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 342.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 342.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 35 | 0ms | 449ms | 495ms |
| 0.0 | 10.0 | app2 | ok | 35 | 275ms | 562ms | 956ms |
| 0.0 | 10.0 | app3 | ok | 35 | 0ms | 438ms | 494ms |
| 0.0 | 10.0 | app4 | ok | 36 | 0ms | 640ms | 964ms |
| 0.0 | 10.0 | app5 | ok | 36 | 0ms | 700ms | 970ms |
| 0.0 | 10.0 | app6 | ok | 36 | 312ms | 462ms | 496ms |
| 10.0 | 20.0 | app1 | ok | 35 | 8646ms | 23636ms | 29364ms |
| 10.0 | 20.0 | app2 | ok | 34 | 8542ms | 23200ms | 29320ms |
| 10.0 | 20.0 | app3 | ok | 34 | 8542ms | 23200ms | 29320ms |
| 10.0 | 20.0 | app4 | ok | 32 | 8478ms | 22889ms | 29289ms |
| 10.0 | 20.0 | app5 | ok | 33 | 8438ms | 22667ms | 29267ms |
| 10.0 | 20.0 | app6 | ok | 32 | 8478ms | 22889ms | 29289ms |
| 20.0 | 30.0 | app1 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app2 | ok | 34 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app3 | ok | 34 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app4 | ok | 35 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app5 | ok | 34 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app6 | ok | 35 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | app1 | ok | 42 | 18649ms | 27730ms | 29773ms |
| 30.0 | 40.0 | app2 | ok | 42 | 18649ms | 27730ms | 29773ms |
| 30.0 | 40.0 | app3 | ok | 42 | 18649ms | 27730ms | 29773ms |
| 30.0 | 40.0 | app4 | ok | 42 | 18649ms | 27730ms | 29773ms |
| 30.0 | 40.0 | app5 | ok | 42 | 18649ms | 27730ms | 29773ms |
| 30.0 | 40.0 | app6 | ok | 42 | 18649ms | 27730ms | 29773ms |
| 40.0 | 50.0 | app1 | ok | 39 | 19737ms | 27947ms | 29795ms |
| 40.0 | 50.0 | app2 | ok | 40 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app3 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app4 | ok | 40 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app5 | ok | 41 | 19750ms | 27950ms | 29795ms |
| 40.0 | 50.0 | app6 | ok | 39 | 19737ms | 27947ms | 29795ms |
| 50.0 | 60.0 | app1 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app2 | ok | 38 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app3 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app4 | ok | 38 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app5 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app6 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app1 | ok | 29 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app2 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app3 | ok | 29 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app4 | ok | 31 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app5 | ok | 28 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app6 | ok | 29 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app1 | ok | 38 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app2 | ok | 37 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app3 | ok | 38 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app4 | ok | 36 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app5 | ok | 38 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app6 | ok | 38 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app1 | ok | 41 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app2 | ok | 41 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app3 | ok | 41 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app4 | ok | 41 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app5 | ok | 40 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app6 | ok | 40 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app1 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app2 | ok | 40 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app3 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app4 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app5 | ok | 40 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app6 | ok | 40 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app1 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app2 | ok | 38 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app3 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app4 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app5 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app6 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app1 | ok | 34 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app2 | ok | 34 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app3 | ok | 34 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app4 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app5 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app6 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app1 | ok | 36 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app2 | ok | 36 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app3 | ok | 35 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app4 | ok | 37 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app5 | ok | 36 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app6 | ok | 36 | 20000ms | 28000ms | 29800ms |
| 130.0 | 140.0 | app1 | ok | 49 | 18049ms | 27610ms | 29761ms |
| 130.0 | 140.0 | app2 | ok | 49 | 18333ms | 27667ms | 29767ms |
| 130.0 | 140.0 | app3 | ok | 50 | 18095ms | 27619ms | 29762ms |
| 130.0 | 140.0 | app4 | ok | 49 | 18049ms | 27610ms | 29761ms |
| 130.0 | 140.0 | app5 | ok | 49 | 18333ms | 27667ms | 29767ms |
| 130.0 | 140.0 | app6 | ok | 49 | 16757ms | 27351ms | 29735ms |
| 140.0 | 150.0 | app1 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app2 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app3 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app4 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app5 | ok | 31 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app6 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 150.0 | 160.0 | app1 | ok | 34 | 20000ms | 28000ms | 29800ms |
| 150.0 | 160.0 | app2 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 150.0 | 160.0 | app3 | ok | 34 | 19697ms | 27939ms | 29794ms |
| 150.0 | 160.0 | app4 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 150.0 | 160.0 | app5 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 150.0 | 160.0 | app6 | ok | 35 | 19394ms | 27879ms | 29788ms |
| 160.0 | 170.0 | app1 | ok | 45 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | app2 | ok | 46 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | app3 | ok | 45 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | app4 | ok | 46 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | app5 | ok | 46 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | app6 | ok | 45 | 20000ms | 28000ms | 29800ms |
| 170.0 | 180.0 | app1 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 170.0 | 180.0 | app2 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 170.0 | 180.0 | app3 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 170.0 | 180.0 | app4 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 170.0 | 180.0 | app5 | ok | 31 | 20000ms | 28000ms | 29800ms |
| 170.0 | 180.0 | app6 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 180.0 | 191.0 | app1 | ok | 39 | 18529ms | 27706ms | 29771ms |
| 180.0 | 191.0 | app2 | ok | 39 | 18529ms | 27706ms | 29771ms |
| 180.0 | 191.0 | app3 | ok | 39 | 18529ms | 27706ms | 29771ms |
| 180.0 | 191.0 | app4 | ok | 39 | 18529ms | 27706ms | 29771ms |
| 180.0 | 191.0 | app5 | ok | 40 | 18571ms | 27714ms | 29771ms |
| 180.0 | 191.0 | app6 | ok | 39 | 17812ms | 27562ms | 29756ms |
| 191.0 | 201.0 | app1 | ok | 30 | 19655ms | 27931ms | 29793ms |
| 191.0 | 201.0 | app2 | ok | 32 | 19333ms | 27867ms | 29787ms |
| 191.0 | 201.0 | app3 | ok | 31 | 19667ms | 27933ms | 29793ms |
| 191.0 | 201.0 | app4 | ok | 30 | 19655ms | 27931ms | 29793ms |
| 191.0 | 201.0 | app5 | ok | 31 | 19310ms | 27862ms | 29786ms |
| 191.0 | 201.0 | app6 | ok | 31 | 18929ms | 27786ms | 29779ms |
| 201.0 | 211.0 | app1 | ok | 40 | 20000ms | 28000ms | 29800ms |
| 201.0 | 211.0 | app2 | ok | 38 | 19730ms | 27946ms | 29795ms |
| 201.0 | 211.0 | app3 | ok | 40 | 20000ms | 28000ms | 29800ms |
| 201.0 | 211.0 | app4 | ok | 40 | 20000ms | 28000ms | 29800ms |
| 201.0 | 211.0 | app5 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 201.0 | 211.0 | app6 | ok | 40 | 19744ms | 27949ms | 29795ms |
| 211.0 | 221.0 | app1 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app2 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app3 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app4 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app5 | ok | 31 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app6 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app1 | ok | 43 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app2 | ok | 43 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app3 | ok | 43 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app4 | ok | 43 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app5 | ok | 43 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app6 | ok | 43 | 20000ms | 28000ms | 29800ms |
| 231.0 | 241.0 | app1 | ok | 40 | 17879ms | 27576ms | 29758ms |
| 231.0 | 241.0 | app2 | ok | 40 | 17097ms | 27419ms | 29742ms |
| 231.0 | 241.0 | app3 | ok | 41 | 16333ms | 27267ms | 29727ms |
| 231.0 | 241.0 | app4 | ok | 40 | 17500ms | 27500ms | 29750ms |
| 231.0 | 241.0 | app5 | ok | 40 | 17097ms | 27419ms | 29742ms |
| 231.0 | 241.0 | app6 | ok | 39 | 16071ms | 27214ms | 29721ms |
| 241.0 | 251.0 | app1 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | app2 | ok | 31 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | app3 | ok | 28 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | app4 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | app5 | ok | 29 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | app6 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app1 | ok | 15 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app2 | ok | 13 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app3 | ok | 14 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app4 | ok | 15 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app5 | ok | 14 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app6 | ok | 13 | 20000ms | 28000ms | 29800ms |
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
| 341.0 | 342.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 342.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 342.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 342.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 342.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 342.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1152510 | 57276 | 1209786.0 | 0.0% | 1242748.0 | 1267062.0 | -1.9% | True |
| app2 | 1151280 | 57120 | 1208400.0 | 0.0% | 1243834.0 | 1265520.0 | -1.7% | True |
| app3 | 1150050 | 57537 | 1207587.0 | 0.0% | 1236712.0 | 1265124.0 | -2.2% | True |
| app4 | 1152510 | 57363 | 1209873.0 | 0.0% | 1233382.0 | 1267236.0 | -2.7% | True |
| app5 | 1151280 | 56965 | 1208245.0 | 0.0% | 1234156.0 | 1265210.0 | -2.5% | True |
| app6 | 1147590 | 57415 | 1205005.0 | 0.0% | 1244786.0 | 1262420.0 | -1.4% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 937 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 936 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 935 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app4 | 937 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app5 | 936 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app6 | 934 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5615). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5615 | 0.050ms | 0.100ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 323480 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 937 | 17273ms | 19895ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 936 | 17232ms | 19888ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app3 | ok | 935 | 17243ms | 19876ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app4 | ok | 937 | 17224ms | 19869ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app5 | ok | 936 | 17235ms | 19864ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app6 | ok | 933 | 17130ms | 19829ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5614 | 17223ms | 19870ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (35 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 1438ms | 3250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 1500ms | 3733ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app3 | ok | 1875ms | 3625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app4 | ok | 2125ms | 3812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app5 | ok | 1833ms | 3733ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app6 | ok | 1438ms | 2812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 7889ms | 14028ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 8286ms | 14227ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app3 | ok | 8000ms | 14182ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app4 | ok | 8222ms | 14056ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app5 | ok | 8250ms | 14150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app6 | ok | 8250ms | 14150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 16354ms | 19823ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 15870ms | 19587ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app3 | ok | 16635ms | 19837ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app4 | ok | 16300ms | 19810ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app5 | ok | 16481ms | 19648ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app6 | ok | 16196ms | 20250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 17500ms | 23833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 17054ms | 20750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app3 | ok | 16964ms | 20500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app4 | ok | 17167ms | 20500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app5 | ok | 16964ms | 20500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app6 | ok | 17155ms | 20750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 17500ms | 19875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 17432ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app3 | ok | 17279ms | 19728ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app4 | ok | 17361ms | 19736ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app5 | ok | 17357ms | 19736ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app6 | ok | 17429ms | 19871ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 17045ms | 19705ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 17031ms | 19703ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app3 | ok | 17031ms | 19703ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app4 | ok | 17031ms | 19703ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app5 | ok | 17206ms | 19721ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app6 | ok | 17000ms | 19700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 17206ms | 19721ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 16953ms | 19695ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app3 | ok | 17292ms | 19729ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app4 | ok | 17279ms | 19728ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app5 | ok | 17279ms | 19728ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app6 | ok | 17132ms | 19713ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 17292ms | 19729ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 17431ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app3 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app4 | ok | 17286ms | 19729ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app5 | ok | 17214ms | 19721ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app6 | ok | 17206ms | 19721ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 17344ms | 19734ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 17422ms | 20750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app3 | ok | 17292ms | 19729ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app4 | ok | 17109ms | 19711ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app5 | ok | 17097ms | 19710ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app6 | ok | 17097ms | 19710ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 17500ms | 19872ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app3 | ok | 17286ms | 19729ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app4 | ok | 17361ms | 19736ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app5 | ok | 17432ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app6 | ok | 17206ms | 19721ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app3 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app4 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app5 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app6 | ok | 17431ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 17431ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app3 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app4 | ok | 17429ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app5 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app6 | ok | 17434ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app3 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app4 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app5 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app6 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 17429ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 17273ms | 19727ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app3 | ok | 17353ms | 19735ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app4 | ok | 17431ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app5 | ok | 17357ms | 19736ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app6 | ok | 17353ms | 19735ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 17568ms | 19878ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 17500ms | 19879ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app3 | ok | 17647ms | 23667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app4 | ok | 17571ms | 19886ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app5 | ok | 17426ms | 19875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app6 | ok | 17357ms | 19864ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 17197ms | 19856ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 17188ms | 19859ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app3 | ok | 17333ms | 21000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app4 | ok | 17083ms | 19858ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app5 | ok | 17339ms | 20750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app6 | ok | 16917ms | 19692ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 17266ms | 19727ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 17000ms | 19700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app3 | ok | 17279ms | 19728ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app4 | ok | 17000ms | 19850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app5 | ok | 17422ms | 20750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app6 | ok | 16897ms | 19690ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 17823ms | 26300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 17500ms | 23833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app3 | ok | 17241ms | 23667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app4 | ok | 17500ms | 24000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app5 | ok | 17426ms | 19875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app6 | ok | 17500ms | 23833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app1 | ok | 16833ms | 19683ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app2 | ok | 17344ms | 20500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app3 | ok | 17206ms | 19721ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app4 | ok | 17273ms | 19864ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app5 | ok | 17250ms | 20750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app6 | ok | 16724ms | 19672ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 17963ms | 26800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 18077ms | 27333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app3 | ok | 17963ms | 26800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app4 | ok | 17981ms | 26900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app5 | ok | 17931ms | 26600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app6 | ok | 17845ms | 25875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 17984ms | 27214ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 18167ms | 27625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app3 | ok | 18065ms | 27286ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app4 | ok | 18167ms | 27625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app5 | ok | 17727ms | 24000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app6 | ok | 17803ms | 25375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 17431ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 17431ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app3 | ok | 17353ms | 19735ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app4 | ok | 17297ms | 19730ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app5 | ok | 17357ms | 19864ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app6 | ok | 17206ms | 19721ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 17432ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app3 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app4 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app5 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app6 | ok | 17432ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app3 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app4 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app5 | ok | 17422ms | 19742ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app6 | ok | 17339ms | 19734ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 17891ms | 26300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 17786ms | 25125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app3 | ok | 17794ms | 25250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app4 | ok | 17721ms | 23833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app5 | ok | 17984ms | 26917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app6 | ok | 17714ms | 23667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app3 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app4 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app5 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app6 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 341.0 | 342.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 342.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 342.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 342.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 342.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 342.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
