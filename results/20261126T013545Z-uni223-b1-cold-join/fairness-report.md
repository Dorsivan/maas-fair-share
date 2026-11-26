# Fairness benchmark: full-contention (uni223-b1-cold-join)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-76bc77c99b-cqhl4` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-26T01:37:09Z` |
| Run end | `2026-11-26T01:41:29Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 27 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/27 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 66.00 | 2.0625 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 2373 | 200=2373 | 2.1 | 7.9 | 738538.0 | 21.1% | 16.7% | -4.4 | 20.8% | -0.2 | 43.4% | 22.4 | 30.4s | 98.9% | 2373.0 |
| app2 | 10.0 | 32 | 1197 | 200=1197 | 4.3 | 15.6 | 369436.0 | 10.5% | 16.7% | 6.1 | 9.8% | -0.8 | 21.9% | 11.4 | 31.6s | 98.9% | 1197.0 |
| end-users | 65.0 | 128 | 1895 | 200=1895 | 8.4 | 10.9 | 2499294.0 | 68.4% | 66.7% | -1.8 | 69.4% | 1.0 | 34.7% | -33.7 | 31.6s | 98.9% | 1895.0 |
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
| 120.0 | 131.0 | 11.0 |
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
| 80.0 | 91.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 80.0 | 91.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 80.0 | 91.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 91.0 | 101.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 91.0 | 101.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 91.0 | 101.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 101.0 | 111.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 101.0 | 111.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 101.0 | 111.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 111.0 | 121.0 | app1 | True | True | 0.0 | 66.7% | n/a | n/a |
| 111.0 | 121.0 | app2 | True | True | 0.0 | 33.3% | n/a | n/a |
| 111.0 | 121.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 121.0 | 131.0 | app1 | True | False | 14870.0 | 21.1% | 13.1% | -7.9 |
| 121.0 | 131.0 | app2 | True | False | 0.0 | 10.5% | 0.0% | -10.5 |
| 121.0 | 131.0 | end-users | True | False | 98576.0 | 68.4% | 86.9% | 18.5 |
| 131.0 | 141.0 | app1 | True | False | 63556.0 | 21.1% | 21.8% | 0.7 |
| 131.0 | 141.0 | app2 | True | False | 23026.0 | 10.5% | 7.9% | -2.6 |
| 131.0 | 141.0 | end-users | True | False | 205588.0 | 68.4% | 70.4% | 1.9 |
| 141.0 | 151.0 | app1 | True | False | 64990.0 | 21.1% | 21.4% | 0.4 |
| 141.0 | 151.0 | app2 | True | False | 25708.0 | 10.5% | 8.5% | -2.0 |
| 141.0 | 151.0 | end-users | True | False | 212310.0 | 68.4% | 70.1% | 1.6 |
| 151.0 | 161.0 | app1 | True | False | 59460.0 | 21.1% | 20.7% | -0.4 |
| 151.0 | 161.0 | app2 | True | False | 35190.0 | 10.5% | 12.2% | 1.7 |
| 151.0 | 161.0 | end-users | True | False | 193286.0 | 68.4% | 67.1% | -1.3 |
| 161.0 | 171.0 | app1 | True | False | 63432.0 | 21.1% | 20.6% | -0.5 |
| 161.0 | 171.0 | app2 | True | False | 32462.0 | 10.5% | 10.5% | 0.0 |
| 161.0 | 171.0 | end-users | True | False | 212194.0 | 68.4% | 68.9% | 0.5 |
| 171.0 | 181.0 | app1 | True | False | 63422.0 | 21.1% | 20.8% | -0.2 |
| 171.0 | 181.0 | app2 | True | False | 32548.0 | 10.5% | 10.7% | 0.2 |
| 171.0 | 181.0 | end-users | True | False | 208300.0 | 68.4% | 68.5% | 0.0 |
| 181.0 | 191.0 | app1 | True | False | 63576.0 | 21.1% | 20.8% | -0.3 |
| 181.0 | 191.0 | app2 | True | False | 31148.0 | 10.5% | 10.2% | -0.3 |
| 181.0 | 191.0 | end-users | True | False | 210936.0 | 68.4% | 69.0% | 0.6 |
| 191.0 | 201.0 | app1 | True | False | 64902.0 | 21.1% | 21.1% | 0.1 |
| 191.0 | 201.0 | app2 | True | False | 33830.0 | 10.5% | 11.0% | 0.5 |
| 191.0 | 201.0 | end-users | True | False | 208426.0 | 68.4% | 67.9% | -0.6 |
| 201.0 | 211.0 | app1 | True | False | 56882.0 | 21.1% | 21.9% | 0.8 |
| 201.0 | 211.0 | app2 | True | False | 22962.0 | 10.5% | 8.8% | -1.7 |
| 201.0 | 211.0 | end-users | True | False | 179980.0 | 68.4% | 69.3% | 0.8 |
| 211.0 | 221.0 | app1 | True | False | 56916.0 | 21.1% | 23.4% | 2.3 |
| 211.0 | 221.0 | app2 | True | False | 27070.0 | 10.5% | 11.1% | 0.6 |
| 211.0 | 221.0 | end-users | True | False | 159542.0 | 68.4% | 65.5% | -2.9 |
| 221.0 | 231.0 | app1 | True | False | 54186.0 | 21.1% | 18.0% | -3.1 |
| 221.0 | 231.0 | app2 | True | False | 31054.0 | 10.5% | 10.3% | -0.2 |
| 221.0 | 231.0 | end-users | True | False | 216296.0 | 68.4% | 71.7% | 3.3 |
| 231.0 | 241.0 | app1 | True | False | 63608.0 | 21.1% | 22.5% | 1.4 |
| 231.0 | 241.0 | app2 | True | False | 28422.0 | 10.5% | 10.0% | -0.5 |
| 231.0 | 241.0 | end-users | True | False | 190782.0 | 68.4% | 67.5% | -1.0 |
| 241.0 | 251.0 | app1 | False | n/a | 48738.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 46016.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 203078.0 | n/a | n/a | n/a |
| 251.0 | 260.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 260.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 260.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 130 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 78 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 150 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app2 | ok | 76 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 153 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app2 | ok | 77 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 154 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app2 | ok | 76 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 149 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 153 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app2 | ok | 76 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 151 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app2 | ok | 75 | 0ms | 0ms | 1ms |
| 60.0 | 70.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 149 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 80.0 | 91.0 | app1 | ok | 153 | 0ms | 0ms | 0ms |
| 80.0 | 91.0 | app2 | ok | 76 | 0ms | 0ms | 0ms |
| 80.0 | 91.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 148 | 0ms | 0ms | 0ms |
| 91.0 | 101.0 | app2 | ok | 76 | 0ms | 0ms | 0ms |
| 91.0 | 101.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 153 | 0ms | 0ms | 0ms |
| 101.0 | 111.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 101.0 | 111.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 149 | 0ms | 0ms | 0ms |
| 111.0 | 121.0 | app2 | ok | 74 | 0ms | 0ms | 0ms |
| 111.0 | 121.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 57 | 0ms | 2136ms | 4644ms |
| 121.0 | 131.0 | app2 | ok | 16 | 0ms | 0ms | 4600ms |
| 121.0 | 131.0 | end-users | ok | 183 | 591ms | 3911ms | 4891ms |
| 131.0 | 141.0 | app1 | ok | 48 | 1825ms | 4200ms | 4920ms |
| 131.0 | 141.0 | app2 | ok | 39 | 5761ms | 9152ms | 9915ms |
| 131.0 | 141.0 | end-users | ok | 169 | 3044ms | 4609ms | 4961ms |
| 141.0 | 151.0 | app1 | ok | 62 | 2446ms | 4483ms | 4948ms |
| 141.0 | 151.0 | app2 | ok | 15 | 7500ms | 9500ms | 9950ms |
| 141.0 | 151.0 | end-users | ok | 178 | 3517ms | 4703ms | 4970ms |
| 151.0 | 161.0 | app1 | ok | 40 | 2393ms | 4474ms | 4947ms |
| 151.0 | 161.0 | app2 | ok | 22 | 6429ms | 9571ms | 25600ms |
| 151.0 | 161.0 | end-users | ok | 137 | 2865ms | 4767ms | 9021ms |
| 161.0 | 171.0 | app1 | ok | 45 | 2094ms | 4297ms | 4930ms |
| 161.0 | 171.0 | app2 | ok | 21 | 7500ms | 9500ms | 9950ms |
| 161.0 | 171.0 | end-users | ok | 137 | 3369ms | 4674ms | 4967ms |
| 171.0 | 181.0 | app1 | ok | 54 | 1871ms | 4036ms | 4904ms |
| 171.0 | 181.0 | app2 | ok | 26 | 7600ms | 9680ms | 24800ms |
| 171.0 | 181.0 | end-users | ok | 172 | 3464ms | 4693ms | 4969ms |
| 181.0 | 191.0 | app1 | ok | 36 | 1868ms | 4100ms | 4910ms |
| 181.0 | 191.0 | app2 | ok | 19 | 7500ms | 9500ms | 9950ms |
| 181.0 | 191.0 | end-users | ok | 122 | 3575ms | 4715ms | 4971ms |
| 191.0 | 201.0 | app1 | ok | 42 | 1717ms | 3833ms | 4883ms |
| 191.0 | 201.0 | app2 | ok | 37 | 6300ms | 9260ms | 9926ms |
| 191.0 | 201.0 | end-users | ok | 157 | 3149ms | 4630ms | 4963ms |
| 201.0 | 211.0 | app1 | ok | 50 | 3043ms | 6429ms | 9643ms |
| 201.0 | 211.0 | app2 | ok | 8 | 8333ms | 22000ms | 29200ms |
| 201.0 | 211.0 | end-users | ok | 138 | 4051ms | 8231ms | 9823ms |
| 211.0 | 221.0 | app1 | ok | 41 | 2981ms | 7950ms | 9795ms |
| 211.0 | 221.0 | app2 | ok | 37 | 4519ms | 9731ms | 27533ms |
| 211.0 | 221.0 | end-users | ok | 161 | 3173ms | 7561ms | 9756ms |
| 221.0 | 231.0 | app1 | ok | 41 | 2772ms | 4554ms | 4955ms |
| 221.0 | 231.0 | app2 | ok | 4 | 6667ms | 9333ms | 9933ms |
| 221.0 | 231.0 | end-users | ok | 107 | 3250ms | 4677ms | 4998ms |
| 231.0 | 241.0 | app1 | ok | 51 | 2290ms | 4512ms | 7450ms |
| 231.0 | 241.0 | app2 | ok | 25 | 6094ms | 9219ms | 9922ms |
| 231.0 | 241.0 | end-users | ok | 159 | 3387ms | 4746ms | 8012ms |
| 241.0 | 251.0 | app1 | ok | 14 | 2071ms | 4300ms | 4930ms |
| 241.0 | 251.0 | app2 | ok | 19 | 7206ms | 9441ms | 9944ms |
| 241.0 | 251.0 | end-users | ok | 75 | 3125ms | 4625ms | 4962ms |
| 251.0 | 260.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 260.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 260.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -77.0%
- app2 exceeded the 10% ledger tolerance: cost -77.2%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2918790 | 145033 | 3063823.0 | 0.0% | 738538.0 | 3208856.0 | -77.0% | False |
| app2 | 1472310 | 73334 | 1545644.0 | 0.0% | 369436.0 | 1618978.0 | -77.2% | False |
| end-users | 2330850 | 115992 | 2446842.0 | 0.0% | 2499294.0 | 2562834.0 | -2.5% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2373 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1197 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1895 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5465). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5465 | 0.051ms | 0.159ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 247070 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 2373 | 2420ms | 7962ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1197 | 4557ms | 16437ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 1895 | 8392ms | 13447ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5465 | 4846ms | 13123ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 1638ms | 2884ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 3615ms | 4872ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 2000ms | 2900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 4230ms | 4923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 2100ms | 2910ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 4296ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 2146ms | 2915ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 4300ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 2138ms | 2914ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 4414ms | 4941ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 2183ms | 2918ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 4333ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 2202ms | 2920ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 4362ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 2116ms | 2912ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 4367ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 91.0 | app1 | ok | 2224ms | 2922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 91.0 | app2 | ok | 4395ms | 4940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 91.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 2300ms | 2930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 4387ms | 4939ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 2100ms | 2910ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 4377ms | 4938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 2219ms | 2922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 4373ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 2883ms | 5606ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 4875ms | 9486ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 2619ms | 5812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 6500ms | 7910ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 12188ms | 14719ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 7868ms | 9786ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 6478ms | 9517ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 8319ms | 12819ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 7273ms | 9967ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 14643ms | 19458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 8600ms | 13917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 5880ms | 8800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 8235ms | 9979ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 7042ms | 9608ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 12619ms | 17000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 8260ms | 11150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 6862ms | 9329ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 12614ms | 14966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 8357ms | 10667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 6800ms | 9467ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 12976ms | 18438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 8416ms | 12594ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 7129ms | 9462ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 16731ms | 19673ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 9218ms | 14076ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 7640ms | 9747ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 16667ms | 19667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 9302ms | 14330ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 7087ms | 9767ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 16806ms | 19681ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 9950ms | 14494ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 7087ms | 13042ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 15625ms | 19562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 8768ms | 14021ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 7391ms | 9673ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 12917ms | 18786ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 8215ms | 12794ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 260.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 260.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 260.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
