# Fairness benchmark: full-contention (uni310-l3-r1-b1-cold-join)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5d57688bf8-p8h8f` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T06:40:40Z` |
| Run end | `2026-11-26T06:44:58Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 27 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/27 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 62.00 | 1.9375 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 2365 | 200=2365 | 2.2 | 7.8 | 738660.0 | 21.1% | 16.7% | -4.4 | 20.7% | -0.3 | 43.3% | 22.2 | 30.3s | 98.9% | 2365.0 |
| app2 | 10.0 | 32 | 1198 | 200=1198 | 4.3 | 15.3 | 373246.0 | 10.5% | 16.7% | 6.1 | 9.9% | -0.6 | 21.9% | 11.4 | 31.6s | 98.9% | 1198.0 |
| end-users | 65.0 | 128 | 1904 | 200=1904 | 8.4 | 10.7 | 2495810.0 | 68.4% | 66.7% | -1.8 | 69.4% | 0.9 | 34.8% | -33.6 | 31.6s | 98.9% | 1904.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- end-users: active 120s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 0.0 (uncontended -- no group delivered contended tokens from here on, nothing was being arbitrated) | 0.0 |
| 120.0 | 130.0 | 10.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 0.0 | 10.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 0.0 | 10.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 10.0 | 20.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 10.0 | 20.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 20.0 | 30.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 20.0 | 30.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 30.0 | 40.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 30.0 | 40.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 40.0 | 50.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 40.0 | 50.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 50.0 | 60.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 50.0 | 60.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 60.0 | 70.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 60.0 | 70.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 70.0 | 80.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 70.0 | 80.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 80.0 | 90.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 80.0 | 90.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 90.0 | 100.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 90.0 | 100.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 100.0 | 110.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 100.0 | 110.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 100.0 | 110.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 110.0 | 120.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 110.0 | 120.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | True | False | 9496.0 | 21.1% | 11.7% | -9.4 |
| 120.0 | 130.0 | app2 | True | False | 0.0 | 10.5% | 0.0% | -10.5 |
| 120.0 | 130.0 | end-users | True | False | 71668.0 | 68.4% | 88.3% | 19.9 |
| 130.0 | 140.0 | app1 | True | False | 63624.0 | 21.1% | 22.2% | 1.1 |
| 130.0 | 140.0 | app2 | True | False | 16234.0 | 10.5% | 5.7% | -4.9 |
| 130.0 | 140.0 | end-users | True | False | 206804.0 | 68.4% | 72.1% | 3.7 |
| 140.0 | 150.0 | app1 | True | False | 64954.0 | 21.1% | 23.3% | 2.3 |
| 140.0 | 150.0 | app2 | True | False | 27062.0 | 10.5% | 9.7% | -0.8 |
| 140.0 | 150.0 | end-users | True | False | 186540.0 | 68.4% | 67.0% | -1.5 |
| 150.0 | 160.0 | app1 | True | False | 59556.0 | 21.1% | 19.9% | -1.1 |
| 150.0 | 160.0 | app2 | True | False | 36566.0 | 10.5% | 12.2% | 1.7 |
| 150.0 | 160.0 | end-users | True | False | 202672.0 | 68.4% | 67.8% | -0.6 |
| 160.0 | 170.0 | app1 | True | False | 59528.0 | 21.1% | 19.5% | -1.6 |
| 160.0 | 170.0 | app2 | True | False | 27040.0 | 10.5% | 8.9% | -1.7 |
| 160.0 | 170.0 | end-users | True | False | 218906.0 | 68.4% | 71.7% | 3.2 |
| 170.0 | 180.0 | app1 | True | False | 64976.0 | 21.1% | 21.4% | 0.4 |
| 170.0 | 180.0 | app2 | True | False | 31044.0 | 10.5% | 10.2% | -0.3 |
| 170.0 | 180.0 | end-users | True | False | 206962.0 | 68.4% | 68.3% | -0.1 |
| 180.0 | 191.0 | app1 | True | False | 62190.0 | 21.1% | 20.4% | -0.7 |
| 180.0 | 191.0 | app2 | True | False | 36500.0 | 10.5% | 11.9% | 1.4 |
| 180.0 | 191.0 | end-users | True | False | 206862.0 | 68.4% | 67.7% | -0.7 |
| 191.0 | 201.0 | app1 | True | False | 62182.0 | 21.1% | 20.6% | -0.4 |
| 191.0 | 201.0 | app2 | True | False | 31152.0 | 10.5% | 10.3% | -0.2 |
| 191.0 | 201.0 | end-users | True | False | 208352.0 | 68.4% | 69.1% | 0.6 |
| 201.0 | 211.0 | app1 | True | False | 60916.0 | 21.1% | 24.2% | 3.2 |
| 201.0 | 211.0 | app2 | True | False | 24322.0 | 10.5% | 9.7% | -0.9 |
| 201.0 | 211.0 | end-users | True | False | 166446.0 | 68.4% | 66.1% | -2.3 |
| 211.0 | 221.0 | app1 | True | False | 58108.0 | 21.1% | 18.9% | -2.2 |
| 211.0 | 221.0 | app2 | True | False | 35118.0 | 10.5% | 11.4% | 0.9 |
| 211.0 | 221.0 | end-users | True | False | 214940.0 | 68.4% | 69.7% | 1.3 |
| 221.0 | 231.0 | app1 | True | False | 56792.0 | 21.1% | 20.9% | -0.2 |
| 221.0 | 231.0 | app2 | True | False | 21634.0 | 10.5% | 8.0% | -2.6 |
| 221.0 | 231.0 | end-users | True | False | 193398.0 | 68.4% | 71.1% | 2.7 |
| 231.0 | 241.0 | app1 | True | False | 60852.0 | 21.1% | 20.0% | -1.0 |
| 231.0 | 241.0 | app2 | True | False | 40498.0 | 10.5% | 13.3% | 2.8 |
| 231.0 | 241.0 | end-users | True | False | 202742.0 | 68.4% | 66.7% | -1.7 |
| 241.0 | 251.0 | app1 | False | n/a | 55486.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 42016.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 187890.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | False | n/a | 4060.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | end-users | False | n/a | 21628.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 119 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 74 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 154 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 150 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app2 | ok | 77 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 149 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app2 | ok | 76 | 0ms | 0ms | 1ms |
| 30.0 | 40.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 154 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 151 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 151 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 149 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 152 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 146 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | app2 | ok | 76 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 152 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | app2 | ok | 73 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 149 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | app2 | ok | 76 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 62 | 0ms | 2786ms | 4779ms |
| 120.0 | 130.0 | app2 | ok | 20 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | end-users | ok | 183 | 690ms | 4005ms | 4901ms |
| 130.0 | 140.0 | app1 | ok | 56 | 2111ms | 4333ms | 4933ms |
| 130.0 | 140.0 | app2 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 130.0 | 140.0 | end-users | ok | 165 | 3612ms | 4750ms | 5875ms |
| 140.0 | 150.0 | app1 | ok | 40 | 2071ms | 4643ms | 9000ms |
| 140.0 | 150.0 | app2 | ok | 34 | 5750ms | 9150ms | 9915ms |
| 140.0 | 150.0 | end-users | ok | 153 | 2723ms | 4818ms | 9235ms |
| 150.0 | 160.0 | app1 | ok | 49 | 3086ms | 4617ms | 4962ms |
| 150.0 | 160.0 | app2 | ok | 26 | 2917ms | 5667ms | 9567ms |
| 150.0 | 160.0 | end-users | ok | 158 | 2217ms | 4485ms | 6050ms |
| 160.0 | 170.0 | app1 | ok | 53 | 2792ms | 4558ms | 4956ms |
| 160.0 | 170.0 | app2 | ok | 24 | 5556ms | 18000ms | 28800ms |
| 160.0 | 170.0 | end-users | ok | 175 | 3069ms | 4632ms | 4983ms |
| 170.0 | 180.0 | app1 | ok | 47 | 2650ms | 4530ms | 4953ms |
| 170.0 | 180.0 | app2 | ok | 11 | 7500ms | 9500ms | 9950ms |
| 170.0 | 180.0 | end-users | ok | 131 | 3425ms | 4685ms | 4969ms |
| 180.0 | 191.0 | app1 | ok | 39 | 2125ms | 4350ms | 4935ms |
| 180.0 | 191.0 | app2 | ok | 19 | 7500ms | 9500ms | 9950ms |
| 180.0 | 191.0 | end-users | ok | 124 | 3565ms | 4713ms | 4971ms |
| 191.0 | 201.0 | app1 | ok | 50 | 2062ms | 4306ms | 4931ms |
| 191.0 | 201.0 | app2 | ok | 26 | 7500ms | 9500ms | 9950ms |
| 191.0 | 201.0 | end-users | ok | 162 | 3537ms | 4737ms | 5950ms |
| 201.0 | 211.0 | app1 | ok | 41 | 2917ms | 7437ms | 9744ms |
| 201.0 | 211.0 | app2 | ok | 23 | 6167ms | 9233ms | 9923ms |
| 201.0 | 211.0 | end-users | ok | 156 | 3239ms | 7214ms | 9721ms |
| 211.0 | 221.0 | app1 | ok | 48 | 2857ms | 4571ms | 4957ms |
| 211.0 | 221.0 | app2 | ok | 36 | 5500ms | 22000ms | 29200ms |
| 211.0 | 221.0 | end-users | ok | 156 | 2903ms | 4581ms | 4958ms |
| 221.0 | 231.0 | app1 | ok | 36 | 3000ms | 7000ms | 9700ms |
| 221.0 | 231.0 | app2 | ok | 2 | 7500ms | 9500ms | 9950ms |
| 221.0 | 231.0 | end-users | ok | 89 | 4408ms | 8565ms | 9856ms |
| 231.0 | 241.0 | app1 | ok | 46 | 2227ms | 4395ms | 4939ms |
| 231.0 | 241.0 | app2 | ok | 24 | 8750ms | 24000ms | 29400ms |
| 231.0 | 241.0 | end-users | ok | 156 | 3655ms | 4731ms | 4973ms |
| 241.0 | 251.0 | app1 | ok | 22 | 2071ms | 4214ms | 4921ms |
| 241.0 | 251.0 | app2 | ok | 26 | 7400ms | 9480ms | 9948ms |
| 241.0 | 251.0 | end-users | ok | 96 | 3462ms | 4692ms | 4969ms |
| 251.0 | 258.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -76.9%
- app2 exceeded the 10% ledger tolerance: cost -77.0%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2908950 | 144876 | 3053826.0 | 0.0% | 738660.0 | 3198702.0 | -76.9% | False |
| app2 | 1473540 | 73220 | 1546760.0 | 0.0% | 373246.0 | 1619980.0 | -77.0% | False |
| end-users | 2341920 | 116176 | 2458096.0 | 0.0% | 2495810.0 | 2574272.0 | -3.0% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2365 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1198 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1904 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5467). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5467 | 0.051ms | 0.150ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 245661 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 2365 | 2472ms | 7838ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1198 | 4604ms | 15782ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 1904 | 8441ms | 13088ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5467 | 4903ms | 12801ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 1700ms | 2984ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2950ms | 4850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 2200ms | 2920ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 4446ms | 4958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 2288ms | 2929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 4406ms | 4941ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 2149ms | 2915ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 4208ms | 4921ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 2201ms | 2920ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 4446ms | 4958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 2170ms | 2917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 4397ms | 4940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 2279ms | 2928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 4431ms | 4943ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 2255ms | 2926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 4405ms | 4940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 2230ms | 2923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 4457ms | 4946ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 2311ms | 2931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 4433ms | 4943ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 2168ms | 2917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 4411ms | 4941ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 2292ms | 2929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 4465ms | 4946ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 2721ms | 5925ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 4750ms | 8767ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 2646ms | 5653ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 6556ms | 8825ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 12300ms | 14730ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 8205ms | 9864ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 6633ms | 8775ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | end-users | ok | 8527ms | 9892ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 6846ms | 9425ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 14821ms | 19481ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | end-users | ok | 8963ms | 14202ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 6828ms | 9120ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 12941ms | 18333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | end-users | ok | 8043ms | 12089ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 6692ms | 9840ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 13088ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | end-users | ok | 8381ms | 13480ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app1 | ok | 7034ms | 9489ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app2 | ok | 12700ms | 16625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | end-users | ok | 8291ms | 9892ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 6875ms | 9080ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 8490ms | 9849ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 7091ms | 9646ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 13750ms | 19250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 8839ms | 13940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 7000ms | 9386ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 16750ms | 19675ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 9660ms | 14440ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 7321ms | 9642ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 13636ms | 19200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 8844ms | 13676ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 7179ms | 9591ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 15312ms | 19531ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 8302ms | 9872ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 6964ms | 9317ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 11630ms | 14663ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 8639ms | 12327ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app2 | ok | 13750ms | 19250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | end-users | ok | 12143ms | 14714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
