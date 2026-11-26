# Fairness benchmark: full-contention-2x (uni310-l2-r1-full-contention-2x)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 6.1 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 6.1 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-8448f688f-lsrxp` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T04:09:44Z` |
| Run end | `2026-11-26T04:14:13Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 28 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/28 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 84.00 | 2.6250 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 64 | 1159 | 200=1159 | 13.6 | 16.2 | 1543326.0 | 21.1% | 16.7% | -4.4 | 20.8% | -0.2 | 20.7% | -0.3 | 79.5s | 98.9% | 1159.0 |
| app2 | 10.0 | 64 | 612 | 200=612 | 27.1 | 30.9 | 798048.0 | 10.5% | 16.7% | 6.1 | 10.8% | 0.2 | 11.0% | 0.4 | 80.5s | 98.9% | 612.0 |
| end-users | 65.0 | 256 | 3818 | 200=3818 | 16.7 | 19.8 | 5069616.0 | 68.4% | 66.7% | -1.8 | 68.4% | -0.0 | 68.3% | -0.1 | 80.5s | 98.9% | 3818.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 10.0 | 10.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 8086.0 | 21.1% | 75.1% | 54.0 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | False | 2682.0 | 68.4% | 24.9% | -43.5 |
| 10.0 | 20.0 | app1 | True | False | 64934.0 | 21.1% | 21.8% | 0.8 |
| 10.0 | 20.0 | app2 | True | False | 13466.0 | 10.5% | 4.5% | -6.0 |
| 10.0 | 20.0 | end-users | True | False | 218940.0 | 68.4% | 73.6% | 5.2 |
| 20.0 | 30.0 | app1 | True | False | 59552.0 | 21.1% | 20.4% | -0.7 |
| 20.0 | 30.0 | app2 | True | False | 35178.0 | 10.5% | 12.0% | 1.5 |
| 20.0 | 30.0 | end-users | True | False | 197554.0 | 68.4% | 67.6% | -0.8 |
| 30.0 | 40.0 | app1 | True | False | 66288.0 | 21.1% | 21.8% | 0.7 |
| 30.0 | 40.0 | app2 | True | False | 32498.0 | 10.5% | 10.7% | 0.2 |
| 30.0 | 40.0 | end-users | True | False | 205436.0 | 68.4% | 67.5% | -0.9 |
| 40.0 | 50.0 | app1 | True | False | 64922.0 | 21.1% | 20.9% | -0.2 |
| 40.0 | 50.0 | app2 | True | False | 32460.0 | 10.5% | 10.4% | -0.1 |
| 40.0 | 50.0 | end-users | True | False | 213572.0 | 68.4% | 68.7% | 0.3 |
| 50.0 | 60.0 | app1 | True | False | 64816.0 | 21.1% | 21.1% | 0.1 |
| 50.0 | 60.0 | app2 | True | False | 32448.0 | 10.5% | 10.6% | 0.0 |
| 50.0 | 60.0 | end-users | True | False | 209702.0 | 68.4% | 68.3% | -0.1 |
| 60.0 | 70.0 | app1 | True | False | 63538.0 | 21.1% | 21.0% | -0.1 |
| 60.0 | 70.0 | app2 | True | False | 32450.0 | 10.5% | 10.7% | 0.2 |
| 60.0 | 70.0 | end-users | True | False | 206974.0 | 68.4% | 68.3% | -0.1 |
| 70.0 | 80.0 | app1 | True | False | 64902.0 | 21.1% | 21.0% | -0.1 |
| 70.0 | 80.0 | app2 | True | False | 31134.0 | 10.5% | 10.1% | -0.5 |
| 70.0 | 80.0 | end-users | True | False | 213638.0 | 68.4% | 69.0% | 0.6 |
| 80.0 | 90.0 | app1 | True | False | 64960.0 | 21.1% | 21.5% | 0.4 |
| 80.0 | 90.0 | app2 | True | False | 32474.0 | 10.5% | 10.7% | 0.2 |
| 80.0 | 90.0 | end-users | True | False | 205356.0 | 68.4% | 67.8% | -0.6 |
| 90.0 | 101.0 | app1 | True | False | 60858.0 | 21.1% | 20.1% | -1.0 |
| 90.0 | 101.0 | app2 | True | False | 32540.0 | 10.5% | 10.7% | 0.2 |
| 90.0 | 101.0 | end-users | True | False | 209618.0 | 68.4% | 69.2% | 0.8 |
| 101.0 | 111.0 | app1 | True | False | 66226.0 | 21.1% | 21.6% | 0.5 |
| 101.0 | 111.0 | app2 | True | False | 31086.0 | 10.5% | 10.1% | -0.4 |
| 101.0 | 111.0 | end-users | True | False | 209536.0 | 68.4% | 68.3% | -0.1 |
| 111.0 | 121.0 | app1 | True | False | 64898.0 | 21.1% | 21.3% | 0.3 |
| 111.0 | 121.0 | app2 | True | False | 33856.0 | 10.5% | 11.1% | 0.6 |
| 111.0 | 121.0 | end-users | True | False | 205550.0 | 68.4% | 67.5% | -0.9 |
| 121.0 | 131.0 | app1 | True | False | 62212.0 | 21.1% | 20.8% | -0.2 |
| 121.0 | 131.0 | app2 | True | False | 31154.0 | 10.5% | 10.4% | -0.1 |
| 121.0 | 131.0 | end-users | True | False | 205462.0 | 68.4% | 68.8% | 0.3 |
| 131.0 | 141.0 | app1 | True | False | 63546.0 | 21.1% | 20.7% | -0.3 |
| 131.0 | 141.0 | app2 | True | False | 32520.0 | 10.5% | 10.6% | 0.1 |
| 131.0 | 141.0 | end-users | True | False | 210782.0 | 68.4% | 68.7% | 0.3 |
| 141.0 | 151.0 | app1 | True | False | 64990.0 | 21.1% | 21.4% | 0.4 |
| 141.0 | 151.0 | app2 | True | False | 32444.0 | 10.5% | 10.7% | 0.2 |
| 141.0 | 151.0 | end-users | True | False | 205790.0 | 68.4% | 67.9% | -0.6 |
| 151.0 | 161.0 | app1 | True | False | 62210.0 | 21.1% | 20.5% | -0.5 |
| 151.0 | 161.0 | app2 | True | False | 31068.0 | 10.5% | 10.3% | -0.3 |
| 151.0 | 161.0 | end-users | True | False | 209474.0 | 68.4% | 69.2% | 0.8 |
| 161.0 | 171.0 | app1 | True | False | 59608.0 | 21.1% | 21.2% | 0.1 |
| 161.0 | 171.0 | app2 | True | False | 28390.0 | 10.5% | 10.1% | -0.4 |
| 161.0 | 171.0 | end-users | True | False | 193398.0 | 68.4% | 68.7% | 0.3 |
| 171.0 | 181.0 | app1 | True | False | 65026.0 | 21.1% | 21.3% | 0.2 |
| 171.0 | 181.0 | app2 | True | False | 33744.0 | 10.5% | 11.0% | 0.5 |
| 171.0 | 181.0 | end-users | True | False | 206822.0 | 68.4% | 67.7% | -0.7 |
| 181.0 | 191.0 | app1 | True | False | 60896.0 | 21.1% | 21.1% | 0.1 |
| 181.0 | 191.0 | app2 | True | False | 29810.0 | 10.5% | 10.3% | -0.2 |
| 181.0 | 191.0 | end-users | True | False | 197602.0 | 68.4% | 68.5% | 0.1 |
| 191.0 | 201.0 | app1 | True | False | 50034.0 | 21.1% | 20.7% | -0.4 |
| 191.0 | 201.0 | app2 | True | False | 25686.0 | 10.5% | 10.6% | 0.1 |
| 191.0 | 201.0 | end-users | True | False | 166212.0 | 68.4% | 68.7% | 0.3 |
| 201.0 | 211.0 | app1 | True | False | 55520.0 | 21.1% | 21.2% | 0.1 |
| 201.0 | 211.0 | app2 | True | False | 27016.0 | 10.5% | 10.3% | -0.2 |
| 201.0 | 211.0 | end-users | True | False | 179916.0 | 68.4% | 68.6% | 0.1 |
| 211.0 | 221.0 | app1 | True | False | 63526.0 | 21.1% | 20.9% | -0.2 |
| 211.0 | 221.0 | app2 | True | False | 32444.0 | 10.5% | 10.7% | 0.1 |
| 211.0 | 221.0 | end-users | True | False | 208440.0 | 68.4% | 68.5% | 0.1 |
| 221.0 | 231.0 | app1 | True | False | 60908.0 | 21.1% | 21.1% | 0.1 |
| 221.0 | 231.0 | app2 | True | False | 29730.0 | 10.5% | 10.3% | -0.2 |
| 221.0 | 231.0 | end-users | True | False | 197442.0 | 68.4% | 68.5% | 0.1 |
| 231.0 | 241.0 | app1 | True | False | 64988.0 | 21.1% | 21.1% | 0.0 |
| 231.0 | 241.0 | app2 | True | False | 32488.0 | 10.5% | 10.5% | 0.0 |
| 231.0 | 241.0 | end-users | True | False | 210986.0 | 68.4% | 68.4% | -0.0 |
| 241.0 | 251.0 | app1 | False | n/a | 63458.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 31092.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 202768.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 32424.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 60872.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | n/a | 175964.0 | n/a | n/a | n/a |
| 261.0 | 269.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 269.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 269.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 49 | 156ms | 4388ms | 4939ms |
| 0.0 | 10.0 | app2 | ok | 35 | 0ms | 325ms | 482ms |
| 0.0 | 10.0 | end-users | ok | 154 | 0ms | 4125ms | 4913ms |
| 10.0 | 20.0 | app1 | ok | 42 | 6912ms | 9382ms | 9938ms |
| 10.0 | 20.0 | app2 | ok | 10 | 7500ms | 9500ms | 9950ms |
| 10.0 | 20.0 | end-users | ok | 135 | 7500ms | 9500ms | 9950ms |
| 20.0 | 30.0 | app1 | ok | 48 | 8158ms | 20400ms | 29040ms |
| 20.0 | 30.0 | app2 | ok | 25 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | end-users | ok | 161 | 17222ms | 27444ms | 29744ms |
| 30.0 | 40.0 | app1 | ok | 54 | 7500ms | 9500ms | 9950ms |
| 30.0 | 40.0 | app2 | ok | 28 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | end-users | ok | 174 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app1 | ok | 52 | 7347ms | 9469ms | 9947ms |
| 40.0 | 50.0 | app2 | ok | 25 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | end-users | ok | 173 | 16270ms | 27254ms | 29725ms |
| 50.0 | 60.0 | app1 | ok | 39 | 7500ms | 9608ms | 22200ms |
| 50.0 | 60.0 | app2 | ok | 19 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | end-users | ok | 125 | 16842ms | 27368ms | 29737ms |
| 60.0 | 70.0 | app1 | ok | 49 | 7552ms | 9594ms | 20200ms |
| 60.0 | 70.0 | app2 | ok | 25 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | end-users | ok | 156 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app1 | ok | 48 | 7553ms | 9596ms | 20400ms |
| 70.0 | 80.0 | app2 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | end-users | ok | 160 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app1 | ok | 40 | 7564ms | 9615ms | 22000ms |
| 80.0 | 90.0 | app2 | ok | 19 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | end-users | ok | 128 | 20000ms | 28000ms | 29800ms |
| 90.0 | 101.0 | app1 | ok | 46 | 7556ms | 9600ms | 20800ms |
| 90.0 | 101.0 | app2 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 90.0 | 101.0 | end-users | ok | 152 | 20000ms | 28000ms | 29800ms |
| 101.0 | 111.0 | app1 | ok | 57 | 7591ms | 9664ms | 24300ms |
| 101.0 | 111.0 | app2 | ok | 28 | 20000ms | 28000ms | 29800ms |
| 101.0 | 111.0 | end-users | ok | 183 | 19661ms | 27932ms | 29793ms |
| 111.0 | 121.0 | app1 | ok | 40 | 7564ms | 9615ms | 22000ms |
| 111.0 | 121.0 | app2 | ok | 20 | 20000ms | 28000ms | 29800ms |
| 111.0 | 121.0 | end-users | ok | 131 | 19435ms | 27887ms | 29789ms |
| 121.0 | 131.0 | app1 | ok | 54 | 7647ms | 9765ms | 26400ms |
| 121.0 | 131.0 | app2 | ok | 28 | 20000ms | 28000ms | 29800ms |
| 121.0 | 131.0 | end-users | ok | 175 | 17847ms | 27569ms | 29757ms |
| 131.0 | 141.0 | app1 | ok | 39 | 7635ms | 9743ms | 26100ms |
| 131.0 | 141.0 | app2 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 131.0 | 141.0 | end-users | ok | 126 | 19920ms | 27984ms | 29798ms |
| 141.0 | 151.0 | app1 | ok | 49 | 7552ms | 9594ms | 20200ms |
| 141.0 | 151.0 | app2 | ok | 25 | 20000ms | 28000ms | 29800ms |
| 141.0 | 151.0 | end-users | ok | 162 | 20000ms | 28000ms | 29800ms |
| 151.0 | 161.0 | app1 | ok | 48 | 7553ms | 9596ms | 20400ms |
| 151.0 | 161.0 | app2 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 151.0 | 161.0 | end-users | ok | 155 | 17795ms | 27559ms | 29756ms |
| 161.0 | 171.0 | app1 | ok | 51 | 8643ms | 23625ms | 29363ms |
| 161.0 | 171.0 | app2 | ok | 27 | 20000ms | 28000ms | 29800ms |
| 161.0 | 171.0 | end-users | ok | 168 | 20000ms | 28000ms | 29800ms |
| 171.0 | 181.0 | app1 | ok | 39 | 7635ms | 9743ms | 26100ms |
| 171.0 | 181.0 | app2 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 171.0 | 181.0 | end-users | ok | 126 | 20000ms | 28000ms | 29800ms |
| 181.0 | 191.0 | app1 | ok | 50 | 7391ms | 9565ms | 20000ms |
| 181.0 | 191.0 | app2 | ok | 25 | 20000ms | 28000ms | 29800ms |
| 181.0 | 191.0 | end-users | ok | 160 | 16667ms | 27333ms | 29733ms |
| 191.0 | 201.0 | app1 | ok | 34 | 9048ms | 24769ms | 29477ms |
| 191.0 | 201.0 | app2 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 191.0 | 201.0 | end-users | ok | 111 | 18065ms | 27613ms | 29761ms |
| 201.0 | 211.0 | app1 | ok | 54 | 9333ms | 25304ms | 29530ms |
| 201.0 | 211.0 | app2 | ok | 26 | 20000ms | 28000ms | 29800ms |
| 201.0 | 211.0 | end-users | ok | 175 | 19329ms | 27866ms | 29787ms |
| 211.0 | 221.0 | app1 | ok | 38 | 7500ms | 9500ms | 9950ms |
| 211.0 | 221.0 | app2 | ok | 19 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | end-users | ok | 126 | 19756ms | 27951ms | 29795ms |
| 221.0 | 231.0 | app1 | ok | 42 | 7625ms | 9725ms | 25800ms |
| 221.0 | 231.0 | app2 | ok | 21 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | end-users | ok | 133 | 17685ms | 27537ms | 29754ms |
| 231.0 | 241.0 | app1 | ok | 53 | 7650ms | 9770ms | 26467ms |
| 231.0 | 241.0 | app2 | ok | 27 | 20000ms | 28000ms | 29800ms |
| 231.0 | 241.0 | end-users | ok | 176 | 19827ms | 27965ms | 29797ms |
| 241.0 | 251.0 | app1 | ok | 44 | 7619ms | 9714ms | 25600ms |
| 241.0 | 251.0 | app2 | ok | 27 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | end-users | ok | 168 | 14299ms | 26860ms | 29686ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 27 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | end-users | ok | 25 | 20000ms | 28000ms | 29800ms |
| 261.0 | 269.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 269.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 269.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1425570 | 71028 | 1496598.0 | 0.0% | 1543326.0 | 1567626.0 | -1.6% | True |
| app2 | 752760 | 37523 | 790283.0 | 0.0% | 798048.0 | 827806.0 | -3.6% | True |
| end-users | 4696140 | 233389 | 4929529.0 | 0.0% | 5069616.0 | 5162918.0 | -1.8% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1159 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 612 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3818 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5589). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5589 | 0.051ms | 0.102ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 255185 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1159 | 12999ms | 18773ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 612 | 24950ms | 36500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3818 | 17148ms | 19958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5589 | 16864ms | 26610ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (27 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 1583ms | 3770ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2750ms | 4600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2173ms | 3746ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 8214ms | 13979ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 10000ms | 14500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 8162ms | 14138ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 13056ms | 18625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 17727ms | 28375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 16350ms | 19635ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 13311ms | 18979ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 17379ms | 19738ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 12667ms | 16000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 17008ms | 19701ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 13333ms | 19000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 16824ms | 19682ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 12798ms | 17650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 17167ms | 19717ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 12553ms | 14851ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 17206ms | 19721ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 101.0 | app1 | ok | 12744ms | 17188ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 101.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 101.0 | end-users | ok | 17151ms | 19715ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 12663ms | 15917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 17434ms | 19743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 12727ms | 17000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 17379ms | 19738ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 13026ms | 18562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 16724ms | 19672ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 13264ms | 18932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 25217ms | 29913ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 17174ms | 19717ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 12667ms | 16000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 12556ms | 14856ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 13438ms | 19083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 17378ms | 19994ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 13636ms | 19200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 25952ms | 40312ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 17398ms | 19740ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 13041ms | 18594ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 25238ms | 29952ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 17214ms | 19721ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 16442ms | 19644ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 27308ms | 42625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 18455ms | 28191ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 16518ms | 19812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 33462ms | 43846ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 21474ms | 29147ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 14896ms | 19489ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 33750ms | 43875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 18532ms | 28289ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 13214ms | 18875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 27857ms | 42938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 16826ms | 19683ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 13529ms | 19143ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 25714ms | 39000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 17210ms | 19754ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 13672ms | 19217ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 25476ms | 36375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 16976ms | 19698ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 13333ms | 19000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 23750ms | 29375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 16905ms | 19690ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 269.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 269.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 269.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
