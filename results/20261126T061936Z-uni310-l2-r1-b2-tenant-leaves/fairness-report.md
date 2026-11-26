# Fairness benchmark: full-contention (uni310-l2-r1-b2-tenant-leaves)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 6.1 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'
Schedule-aware expected share (UNI-222): app1, app2, end-users scored against a time-weighted entitlement from the declared join/leave or duty-cycle schedule, not the flat whole-run weight ratio -- see docs/design.md "Whole-run scoring with a declared schedule".

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 6.1 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-8448f688f-hnmrw` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T06:21:03Z` |
| Run end | `2026-11-26T06:26:46Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 36 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/36 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 76.50 | 2.3906 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 2310 | 000=1, 200=2309 | 2.1 | 7.9 | 814246.0 | 23.4% | 16.7% | -4.4 | 22.9% | -0.4 | 42.6% | 21.5 | 38.6s | 98.9% | 2310.0 |
| app2 | 10.0 | 32 | 1169 | 200=1169 | 4.3 | 15.0 | 415054.0 | 11.7% | 16.7% | 6.1 | 11.7% | 0.0 | 21.6% | 11.0 | 38.8s | 98.9% | 1169.0 |
| end-users | 65.0 | 128 | 1945 | 200=1945 | 8.1 | 10.6 | 2535936.0 | 65.0% | 66.7% | -1.8 | 65.4% | 0.4 | 35.9% | -32.6 | 38.7s | 98.9% | 1945.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- end-users: active 0s-120s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 10.0 | 10.0 |
| 120.0 | 141.0 (uncontended -- no group delivered contended tokens from here on, nothing was being arbitrated) | 21.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (35 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 6762.0 | 21.1% | 31.2% | 10.1 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | False | 14922.0 | 68.4% | 68.8% | 0.4 |
| 10.0 | 20.0 | app1 | True | False | 64888.0 | 21.1% | 22.1% | 1.1 |
| 10.0 | 20.0 | app2 | True | False | 16234.0 | 10.5% | 5.5% | -5.0 |
| 10.0 | 20.0 | end-users | True | False | 212298.0 | 68.4% | 72.4% | 3.9 |
| 20.0 | 30.0 | app1 | True | False | 60810.0 | 21.1% | 20.0% | -1.1 |
| 20.0 | 30.0 | app2 | True | False | 41972.0 | 10.5% | 13.8% | 3.3 |
| 20.0 | 30.0 | end-users | True | False | 201608.0 | 68.4% | 66.2% | -2.2 |
| 30.0 | 40.0 | app1 | True | False | 67586.0 | 21.1% | 21.7% | 0.7 |
| 30.0 | 40.0 | app2 | True | False | 22988.0 | 10.5% | 7.4% | -3.1 |
| 30.0 | 40.0 | end-users | True | False | 220310.0 | 68.4% | 70.9% | 2.4 |
| 40.0 | 50.0 | app1 | True | False | 63508.0 | 21.1% | 20.8% | -0.3 |
| 40.0 | 50.0 | app2 | True | False | 35152.0 | 10.5% | 11.5% | 1.0 |
| 40.0 | 50.0 | end-users | True | False | 206872.0 | 68.4% | 67.7% | -0.7 |
| 50.0 | 60.0 | app1 | True | False | 64894.0 | 21.1% | 21.2% | 0.2 |
| 50.0 | 60.0 | app2 | True | False | 25658.0 | 10.5% | 8.4% | -2.1 |
| 50.0 | 60.0 | end-users | True | False | 215140.0 | 68.4% | 70.4% | 2.0 |
| 60.0 | 70.0 | app1 | True | False | 60902.0 | 21.1% | 20.0% | -1.1 |
| 60.0 | 70.0 | app2 | True | False | 36506.0 | 10.5% | 12.0% | 1.5 |
| 60.0 | 70.0 | end-users | True | False | 207124.0 | 68.4% | 68.0% | -0.4 |
| 70.0 | 80.0 | app1 | True | False | 66202.0 | 21.1% | 21.5% | 0.4 |
| 70.0 | 80.0 | app2 | True | False | 33818.0 | 10.5% | 11.0% | 0.4 |
| 70.0 | 80.0 | end-users | True | False | 208234.0 | 68.4% | 67.6% | -0.9 |
| 80.0 | 90.0 | app1 | True | False | 65084.0 | 21.1% | 21.7% | 0.6 |
| 80.0 | 90.0 | app2 | True | False | 31044.0 | 10.5% | 10.3% | -0.2 |
| 80.0 | 90.0 | end-users | True | False | 204140.0 | 68.4% | 68.0% | -0.4 |
| 90.0 | 100.0 | app1 | True | False | 62312.0 | 21.1% | 20.5% | -0.6 |
| 90.0 | 100.0 | app2 | True | False | 32486.0 | 10.5% | 10.7% | 0.1 |
| 90.0 | 100.0 | end-users | True | False | 209636.0 | 68.4% | 68.9% | 0.4 |
| 100.0 | 110.0 | app1 | True | False | 64912.0 | 21.1% | 21.2% | 0.2 |
| 100.0 | 110.0 | app2 | True | False | 28418.0 | 10.5% | 9.3% | -1.2 |
| 100.0 | 110.0 | end-users | True | False | 212314.0 | 68.4% | 69.5% | 1.0 |
| 110.0 | 121.0 | app1 | True | False | 62240.0 | 21.1% | 20.4% | -0.7 |
| 110.0 | 121.0 | app2 | True | False | 35116.0 | 10.5% | 11.5% | 1.0 |
| 110.0 | 121.0 | end-users | True | False | 208284.0 | 68.4% | 68.1% | -0.3 |
| 121.0 | 131.0 | app1 | True | False | 68986.0 | 66.7% | 66.3% | -0.4 |
| 121.0 | 131.0 | app2 | True | False | 35098.0 | 33.3% | 33.7% | 0.4 |
| 121.0 | 131.0 | end-users | False | n/a | 204224.0 | n/a | n/a | n/a |
| 131.0 | 141.0 | app1 | True | False | 35160.0 | 66.7% | 46.4% | -20.2 |
| 131.0 | 141.0 | app2 | True | False | 40564.0 | 33.3% | 53.6% | 20.2 |
| 131.0 | 141.0 | end-users | False | n/a | 10830.0 | n/a | n/a | n/a |
| 141.0 | 151.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 141.0 | 151.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 141.0 | 151.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 151.0 | 161.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 151.0 | 161.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 151.0 | 161.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 161.0 | 171.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 161.0 | 171.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 161.0 | 171.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 171.0 | 181.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 171.0 | 181.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 171.0 | 181.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 181.0 | 191.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 181.0 | 191.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 181.0 | 191.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 191.0 | 201.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 191.0 | 201.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 201.0 | 211.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 201.0 | 211.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 201.0 | 211.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 211.0 | 221.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 211.0 | 221.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 211.0 | 221.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 221.0 | 231.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 221.0 | 231.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 231.0 | 241.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 231.0 | 241.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 343.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 343.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 343.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 51 | 958ms | 2421ms | 4681ms |
| 0.0 | 10.0 | app2 | ok | 25 | 0ms | 0ms | 4375ms |
| 0.0 | 10.0 | end-users | ok | 163 | 1319ms | 3955ms | 4896ms |
| 10.0 | 20.0 | app1 | ok | 43 | 1908ms | 4232ms | 4923ms |
| 10.0 | 20.0 | app2 | ok | 39 | 6300ms | 9420ms | 22200ms |
| 10.0 | 20.0 | end-users | ok | 166 | 3096ms | 4619ms | 4962ms |
| 20.0 | 30.0 | app1 | ok | 48 | 2500ms | 4500ms | 4950ms |
| 20.0 | 30.0 | app2 | ok | 8 | 7857ms | 14000ms | 28400ms |
| 20.0 | 30.0 | end-users | ok | 130 | 3542ms | 4745ms | 6750ms |
| 30.0 | 40.0 | app1 | ok | 50 | 2105ms | 4375ms | 4938ms |
| 30.0 | 40.0 | app2 | ok | 31 | 6771ms | 9354ms | 9935ms |
| 30.0 | 40.0 | end-users | ok | 161 | 3065ms | 4613ms | 4961ms |
| 40.0 | 50.0 | app1 | ok | 50 | 2275ms | 4432ms | 4943ms |
| 40.0 | 50.0 | app2 | ok | 28 | 4375ms | 9250ms | 24400ms |
| 40.0 | 50.0 | end-users | ok | 167 | 3119ms | 4624ms | 4962ms |
| 50.0 | 60.0 | app1 | ok | 43 | 2036ms | 4283ms | 4928ms |
| 50.0 | 60.0 | app2 | ok | 11 | 11667ms | 26333ms | 29633ms |
| 50.0 | 60.0 | end-users | ok | 137 | 3369ms | 4674ms | 4967ms |
| 60.0 | 70.0 | app1 | ok | 49 | 1750ms | 3775ms | 4877ms |
| 60.0 | 70.0 | app2 | ok | 25 | 7717ms | 9891ms | 27500ms |
| 60.0 | 70.0 | end-users | ok | 163 | 3585ms | 4717ms | 4972ms |
| 70.0 | 80.0 | app1 | ok | 54 | 1650ms | 3650ms | 4865ms |
| 70.0 | 80.0 | app2 | ok | 29 | 7589ms | 9661ms | 24200ms |
| 70.0 | 80.0 | end-users | ok | 174 | 3401ms | 4680ms | 4968ms |
| 80.0 | 90.0 | app1 | ok | 41 | 1908ms | 4212ms | 4921ms |
| 80.0 | 90.0 | app2 | ok | 19 | 7639ms | 9750ms | 26200ms |
| 80.0 | 90.0 | end-users | ok | 134 | 3463ms | 4693ms | 4969ms |
| 90.0 | 100.0 | app1 | ok | 51 | 2088ms | 4362ms | 4936ms |
| 90.0 | 100.0 | app2 | ok | 32 | 6000ms | 9200ms | 9920ms |
| 90.0 | 100.0 | end-users | ok | 165 | 3108ms | 4622ms | 4962ms |
| 100.0 | 110.0 | app1 | ok | 39 | 2162ms | 4350ms | 4935ms |
| 100.0 | 110.0 | app2 | ok | 13 | 7708ms | 9875ms | 27400ms |
| 100.0 | 110.0 | end-users | ok | 128 | 3462ms | 4692ms | 4969ms |
| 110.0 | 121.0 | app1 | ok | 49 | 1853ms | 3979ms | 4898ms |
| 110.0 | 121.0 | app2 | ok | 24 | 7500ms | 9500ms | 9950ms |
| 110.0 | 121.0 | end-users | ok | 153 | 3614ms | 4723ms | 4972ms |
| 121.0 | 131.0 | app1 | ok | 63 | 1028ms | 2428ms | 4685ms |
| 121.0 | 131.0 | app2 | ok | 49 | 4844ms | 8979ms | 9898ms |
| 121.0 | 131.0 | end-users | ok | 104 | 3646ms | 4729ms | 4973ms |
| 131.0 | 141.0 | app1 | ok | 149 | 0ms | 0ms | 0ms |
| 131.0 | 141.0 | app2 | ok | 70 | 0ms | 0ms | 0ms |
| 131.0 | 141.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 151 | 0ms | 0ms | 0ms |
| 141.0 | 151.0 | app2 | ok | 77 | 0ms | 0ms | 0ms |
| 141.0 | 151.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 152 | 0ms | 0ms | 0ms |
| 151.0 | 161.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 151.0 | 161.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 149 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | app2 | ok | 76 | 0ms | 0ms | 2ms |
| 161.0 | 171.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 152 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | app2 | ok | 74 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 149 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | app2 | ok | 76 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 151 | 0ms | 0ms | 0ms |
| 191.0 | 201.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 191.0 | 201.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 151 | 0ms | 0ms | 0ms |
| 201.0 | 211.0 | app2 | ok | 77 | 0ms | 0ms | 1ms |
| 201.0 | 211.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 151 | 0ms | 0ms | 0ms |
| 211.0 | 221.0 | app2 | ok | 74 | 0ms | 0ms | 0ms |
| 211.0 | 221.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 149 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 153 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | app2 | ok | 76 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 22 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | app2 | ok | 11 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 343.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 343.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 343.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -73.9%
- app2 exceeded the 10% ledger tolerance: cost -73.7%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2840070 | 141241 | 2981311.0 | 0.0% | 814246.0 | 3122552.0 | -73.9% | False |
| app2 | 1437870 | 71493 | 1509363.0 | 0.0% | 415054.0 | 1580856.0 | -73.7% | False |
| end-users | 2392350 | 119144 | 2511494.0 | 0.0% | 2535936.0 | 2630638.0 | -3.6% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2310 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1169 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1945 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5424). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5424 | 0.051ms | 0.148ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 324946 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 2309 | 2319ms | 7836ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1169 | 4605ms | 14946ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 1945 | 8097ms | 12913ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5423 | 4963ms | 12677ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (35 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2200ms | 4350ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2833ms | 4812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2525ms | 4711ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 6519ms | 8800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 10227ms | 14523ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 7431ms | 9738ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 6400ms | 9343ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 12981ms | 18450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 8425ms | 12809ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 7077ms | 9909ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 12833ms | 17875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 8274ms | 13545ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 6542ms | 9217ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 13750ms | 19278ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 8292ms | 12450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 6292ms | 9033ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 12969ms | 18417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 8014ms | 10031ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 6591ms | 9357ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 14792ms | 19481ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 8164ms | 12450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 6200ms | 9555ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 12717ms | 16875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 8327ms | 13758ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 6533ms | 9631ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 13382ms | 19042ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 8340ms | 13890ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 6375ms | 9540ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 13333ms | 19000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 8300ms | 13893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 6440ms | 9020ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 13088ms | 18688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 8250ms | 11729ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 121.0 | app1 | ok | 6583ms | 9233ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 121.0 | app2 | ok | 13095ms | 18700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 121.0 | end-users | ok | 8154ms | 12735ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 6391ms | 9271ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 8338ms | 12304ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 2042ms | 5394ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 4894ms | 13583ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 12143ms | 14714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 1952ms | 2888ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 4333ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 1947ms | 2887ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 4356ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 1993ms | 2899ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 4333ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 2000ms | 2900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 4411ms | 4941ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 2013ms | 2901ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 4377ms | 4938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 2038ms | 2904ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 4387ms | 4939ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 1946ms | 2886ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 4379ms | 4938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 1990ms | 2898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 4422ms | 4942ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 1960ms | 2891ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 4414ms | 4941ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 2095ms | 2910ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 4405ms | 4940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 1882ms | 2856ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 4204ms | 4920ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 343.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 343.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 343.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
