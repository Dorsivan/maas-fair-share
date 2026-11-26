# Fairness benchmark: full-contention (uni310-l2-r1-e2-lose-replica)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 6.1 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 6.1 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `360` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-8448f688f-56rbs` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T06:43:19Z` |
| Run end | `2026-11-26T06:49:47Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 40 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/40 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 88.00 | 2.7500 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1234 | 200=1234 | 7.9 | 13.8 | 1633152.0 | 21.1% | 16.7% | -4.4 | 21.0% | -0.1 | 20.9% | -0.1 | 91.6s | 98.9% | 1234.0 |
| app2 | 10.0 | 32 | 633 | 000=1, 200=632 | 14.8 | 26.6 | 823430.0 | 10.5% | 16.7% | 6.1 | 10.6% | 0.1 | 10.7% | 0.2 | 92.8s | 98.9% | 633.0 |
| end-users | 65.0 | 128 | 4030 | 200=4030 | 9.6 | 16.9 | 5326182.0 | 68.4% | 66.7% | -1.8 | 68.4% | 0.0 | 68.3% | -0.1 | 92.8s | 98.9% | 4030.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events (scheduled):**
- t+120s: scale_down (target=maas-vllm-gpu, to=1)
- t+360s: scale_restore (target=maas-vllm-gpu)

**Per-tenant schedule:**
- app1: active 0s-360s, no duty cycle
- app2: active 0s-360s, no duty cycle
- end-users: active 0s-360s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 10.0 | 10.0 |
| 120.0 | 121.0 | 1.0 |
| 360.0 | n/a (never converged in this phase) | n/a |

**Windows** (39 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 13580.0 | 21.1% | 43.6% | 22.5 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | False | 17586.0 | 68.4% | 56.4% | -12.0 |
| 10.0 | 20.0 | app1 | True | False | 54050.0 | 21.1% | 21.5% | 0.4 |
| 10.0 | 20.0 | app2 | True | False | 18900.0 | 10.5% | 7.5% | -3.0 |
| 10.0 | 20.0 | end-users | True | False | 178502.0 | 68.4% | 71.0% | 2.6 |
| 20.0 | 30.0 | app1 | True | False | 63608.0 | 21.1% | 20.8% | -0.2 |
| 20.0 | 30.0 | app2 | True | False | 32462.0 | 10.5% | 10.6% | 0.1 |
| 20.0 | 30.0 | end-users | True | False | 209634.0 | 68.4% | 68.6% | 0.2 |
| 30.0 | 41.0 | app1 | True | False | 64800.0 | 21.1% | 20.9% | -0.1 |
| 30.0 | 41.0 | app2 | True | False | 33788.0 | 10.5% | 10.9% | 0.4 |
| 30.0 | 41.0 | end-users | True | False | 210858.0 | 68.4% | 68.1% | -0.3 |
| 41.0 | 51.0 | app1 | True | False | 66238.0 | 21.1% | 21.4% | 0.3 |
| 41.0 | 51.0 | app2 | True | False | 31036.0 | 10.5% | 10.0% | -0.5 |
| 41.0 | 51.0 | end-users | True | False | 212454.0 | 68.4% | 68.6% | 0.2 |
| 51.0 | 61.0 | app1 | True | False | 62212.0 | 21.1% | 20.4% | -0.7 |
| 51.0 | 61.0 | app2 | True | False | 32408.0 | 10.5% | 10.6% | 0.1 |
| 51.0 | 61.0 | end-users | True | False | 211040.0 | 68.4% | 69.0% | 0.6 |
| 61.0 | 71.0 | app1 | True | False | 67542.0 | 21.1% | 21.8% | 0.8 |
| 61.0 | 71.0 | app2 | True | False | 31178.0 | 10.5% | 10.1% | -0.5 |
| 61.0 | 71.0 | end-users | True | False | 210910.0 | 68.4% | 68.1% | -0.3 |
| 71.0 | 81.0 | app1 | True | False | 62178.0 | 21.1% | 20.3% | -0.8 |
| 71.0 | 81.0 | app2 | True | False | 31096.0 | 10.5% | 10.1% | -0.4 |
| 71.0 | 81.0 | end-users | True | False | 213738.0 | 68.4% | 69.6% | 1.2 |
| 81.0 | 91.0 | app1 | True | False | 63620.0 | 21.1% | 20.9% | -0.1 |
| 81.0 | 91.0 | app2 | True | False | 33772.0 | 10.5% | 11.1% | 0.6 |
| 81.0 | 91.0 | end-users | True | False | 206922.0 | 68.4% | 68.0% | -0.4 |
| 91.0 | 101.0 | app1 | True | False | 63530.0 | 21.1% | 21.1% | 0.0 |
| 91.0 | 101.0 | app2 | True | False | 31058.0 | 10.5% | 10.3% | -0.2 |
| 91.0 | 101.0 | end-users | True | False | 207112.0 | 68.4% | 68.6% | 0.2 |
| 101.0 | 111.0 | app1 | True | False | 58084.0 | 21.1% | 21.8% | 0.7 |
| 101.0 | 111.0 | app2 | True | False | 21682.0 | 10.5% | 8.1% | -2.4 |
| 101.0 | 111.0 | end-users | True | False | 186690.0 | 68.4% | 70.1% | 1.6 |
| 111.0 | 121.0 | app1 | True | False | 63552.0 | 21.1% | 20.7% | -0.3 |
| 111.0 | 121.0 | app2 | True | False | 39224.0 | 10.5% | 12.8% | 2.3 |
| 111.0 | 121.0 | end-users | True | False | 203938.0 | 68.4% | 66.5% | -1.9 |
| 121.0 | 131.0 | app1 | True | False | 63648.0 | 21.1% | 20.8% | -0.2 |
| 121.0 | 131.0 | app2 | True | False | 32426.0 | 10.5% | 10.6% | 0.1 |
| 121.0 | 131.0 | end-users | True | False | 209712.0 | 68.4% | 68.6% | 0.2 |
| 131.0 | 141.0 | app1 | True | False | 64912.0 | 21.1% | 21.1% | 0.1 |
| 131.0 | 141.0 | app2 | True | False | 31122.0 | 10.5% | 10.1% | -0.4 |
| 131.0 | 141.0 | end-users | True | False | 210958.0 | 68.4% | 68.7% | 0.3 |
| 141.0 | 151.0 | app1 | True | False | 67614.0 | 21.1% | 21.9% | 0.9 |
| 141.0 | 151.0 | app2 | True | False | 33802.0 | 10.5% | 11.0% | 0.4 |
| 141.0 | 151.0 | end-users | True | False | 207046.0 | 68.4% | 67.1% | -1.3 |
| 151.0 | 161.0 | app1 | True | False | 44594.0 | 21.1% | 19.6% | -1.4 |
| 151.0 | 161.0 | app2 | True | False | 24328.0 | 10.5% | 10.7% | 0.2 |
| 151.0 | 161.0 | end-users | True | False | 158172.0 | 68.4% | 69.7% | 1.2 |
| 161.0 | 171.0 | app1 | True | False | 32472.0 | 21.1% | 21.4% | 0.4 |
| 161.0 | 171.0 | app2 | True | False | 14900.0 | 10.5% | 9.8% | -0.7 |
| 161.0 | 171.0 | end-users | True | False | 104196.0 | 68.4% | 68.7% | 0.3 |
| 171.0 | 181.0 | app1 | True | False | 31018.0 | 21.1% | 20.3% | -0.7 |
| 171.0 | 181.0 | app2 | True | False | 16220.0 | 10.5% | 10.6% | 0.1 |
| 171.0 | 181.0 | end-users | True | False | 105370.0 | 68.4% | 69.0% | 0.6 |
| 181.0 | 191.0 | app1 | True | False | 33840.0 | 21.1% | 22.1% | 1.1 |
| 181.0 | 191.0 | app2 | True | False | 14876.0 | 10.5% | 9.7% | -0.8 |
| 181.0 | 191.0 | end-users | True | False | 104246.0 | 68.4% | 68.2% | -0.3 |
| 191.0 | 201.0 | app1 | True | False | 31102.0 | 21.1% | 20.5% | -0.6 |
| 191.0 | 201.0 | app2 | True | False | 17644.0 | 10.5% | 11.6% | 1.1 |
| 191.0 | 201.0 | end-users | True | False | 102958.0 | 68.4% | 67.9% | -0.6 |
| 201.0 | 211.0 | app1 | True | False | 33748.0 | 21.1% | 22.1% | 1.0 |
| 201.0 | 211.0 | app2 | True | False | 14874.0 | 10.5% | 9.7% | -0.8 |
| 201.0 | 211.0 | end-users | True | False | 104118.0 | 68.4% | 68.2% | -0.3 |
| 211.0 | 221.0 | app1 | True | False | 31134.0 | 21.1% | 20.4% | -0.7 |
| 211.0 | 221.0 | app2 | True | False | 16214.0 | 10.5% | 10.6% | 0.1 |
| 211.0 | 221.0 | end-users | True | False | 105366.0 | 68.4% | 69.0% | 0.6 |
| 221.0 | 231.0 | app1 | True | False | 31024.0 | 21.1% | 20.5% | -0.6 |
| 221.0 | 231.0 | app2 | True | False | 16210.0 | 10.5% | 10.7% | 0.2 |
| 221.0 | 231.0 | end-users | True | False | 104150.0 | 68.4% | 68.8% | 0.4 |
| 231.0 | 241.0 | app1 | True | False | 32426.0 | 21.1% | 21.2% | 0.2 |
| 231.0 | 241.0 | app2 | True | False | 17564.0 | 10.5% | 11.5% | 1.0 |
| 231.0 | 241.0 | end-users | True | False | 102826.0 | 68.4% | 67.3% | -1.1 |
| 241.0 | 251.0 | app1 | True | False | 32450.0 | 21.1% | 21.0% | -0.0 |
| 241.0 | 251.0 | app2 | True | False | 14904.0 | 10.5% | 9.7% | -0.9 |
| 241.0 | 251.0 | end-users | True | False | 106818.0 | 68.4% | 69.3% | 0.9 |
| 251.0 | 261.0 | app1 | True | False | 32448.0 | 21.1% | 21.1% | 0.0 |
| 251.0 | 261.0 | app2 | True | False | 16270.0 | 10.5% | 10.6% | 0.0 |
| 251.0 | 261.0 | end-users | True | False | 105408.0 | 68.4% | 68.4% | -0.0 |
| 261.0 | 271.0 | app1 | True | False | 32446.0 | 21.1% | 21.2% | 0.2 |
| 261.0 | 271.0 | app2 | True | False | 16198.0 | 10.5% | 10.6% | 0.1 |
| 261.0 | 271.0 | end-users | True | False | 104066.0 | 68.4% | 68.1% | -0.3 |
| 271.0 | 281.0 | app1 | True | False | 32452.0 | 21.1% | 20.9% | -0.2 |
| 271.0 | 281.0 | app2 | True | False | 14856.0 | 10.5% | 9.6% | -1.0 |
| 271.0 | 281.0 | end-users | True | False | 108158.0 | 68.4% | 69.6% | 1.1 |
| 281.0 | 291.0 | app1 | True | False | 31178.0 | 21.1% | 20.8% | -0.3 |
| 281.0 | 291.0 | app2 | True | False | 16270.0 | 10.5% | 10.8% | 0.3 |
| 281.0 | 291.0 | end-users | True | False | 102784.0 | 68.4% | 68.4% | -0.0 |
| 291.0 | 302.0 | app1 | True | False | 32486.0 | 21.1% | 21.2% | 0.2 |
| 291.0 | 302.0 | app2 | True | False | 17586.0 | 10.5% | 11.5% | 1.0 |
| 291.0 | 302.0 | end-users | True | False | 102844.0 | 68.4% | 67.3% | -1.2 |
| 302.0 | 312.0 | app1 | True | False | 31128.0 | 21.1% | 20.7% | -0.3 |
| 302.0 | 312.0 | app2 | True | False | 14922.0 | 10.5% | 9.9% | -0.6 |
| 302.0 | 312.0 | end-users | True | False | 104270.0 | 68.4% | 69.4% | 0.9 |
| 312.0 | 322.0 | app1 | True | False | 32344.0 | 21.1% | 21.2% | 0.1 |
| 312.0 | 322.0 | app2 | True | False | 16196.0 | 10.5% | 10.6% | 0.1 |
| 312.0 | 322.0 | end-users | True | False | 104136.0 | 68.4% | 68.2% | -0.2 |
| 322.0 | 332.0 | app1 | True | False | 33796.0 | 21.1% | 21.7% | 0.7 |
| 322.0 | 332.0 | app2 | True | False | 16142.0 | 10.5% | 10.4% | -0.1 |
| 322.0 | 332.0 | end-users | True | False | 105544.0 | 68.4% | 67.9% | -0.5 |
| 332.0 | 342.0 | app1 | True | False | 31066.0 | 21.1% | 20.5% | -0.5 |
| 332.0 | 342.0 | app2 | True | False | 16212.0 | 10.5% | 10.7% | 0.2 |
| 332.0 | 342.0 | end-users | True | False | 104154.0 | 68.4% | 68.8% | 0.4 |
| 342.0 | 352.0 | app1 | True | False | 32440.0 | 21.1% | 21.0% | -0.0 |
| 342.0 | 352.0 | app2 | True | False | 16240.0 | 10.5% | 10.5% | 0.0 |
| 342.0 | 352.0 | end-users | True | False | 105490.0 | 68.4% | 68.4% | 0.0 |
| 352.0 | 362.0 | app1 | True | False | 32408.0 | 21.1% | 21.0% | -0.0 |
| 352.0 | 362.0 | app2 | True | False | 16202.0 | 10.5% | 10.5% | -0.0 |
| 352.0 | 362.0 | end-users | True | False | 105448.0 | 68.4% | 68.4% | 0.0 |
| 362.0 | 372.0 | app1 | False | n/a | 32536.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app2 | False | n/a | 16190.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | end-users | False | n/a | 104178.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app1 | False | n/a | 13448.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app2 | False | n/a | 28458.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | end-users | False | n/a | 74382.0 | n/a | n/a | n/a |
| 382.0 | 388.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 388.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 388.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 43 | 0ms | 2161ms | 2466ms |
| 0.0 | 10.0 | app2 | ok | 23 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 138 | 0ms | 2050ms | 2455ms |
| 10.0 | 20.0 | app1 | ok | 57 | 2031ms | 4321ms | 4932ms |
| 10.0 | 20.0 | app2 | ok | 30 | 6053ms | 9211ms | 9921ms |
| 10.0 | 20.0 | end-users | ok | 185 | 2917ms | 4583ms | 4958ms |
| 20.0 | 30.0 | app1 | ok | 39 | 2162ms | 4350ms | 4935ms |
| 20.0 | 30.0 | app2 | ok | 17 | 7500ms | 9500ms | 9950ms |
| 20.0 | 30.0 | end-users | ok | 127 | 3488ms | 4698ms | 4970ms |
| 30.0 | 41.0 | app1 | ok | 55 | 1802ms | 4018ms | 4902ms |
| 30.0 | 41.0 | app2 | ok | 27 | 7500ms | 9500ms | 9950ms |
| 30.0 | 41.0 | end-users | ok | 179 | 3424ms | 4685ms | 4968ms |
| 41.0 | 51.0 | app1 | ok | 50 | 1857ms | 4038ms | 4904ms |
| 41.0 | 51.0 | app2 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 41.0 | 51.0 | end-users | ok | 163 | 3524ms | 4705ms | 4970ms |
| 51.0 | 61.0 | app1 | ok | 38 | 1786ms | 3944ms | 4894ms |
| 51.0 | 61.0 | app2 | ok | 20 | 7500ms | 9500ms | 9950ms |
| 51.0 | 61.0 | end-users | ok | 124 | 3495ms | 4699ms | 4970ms |
| 61.0 | 71.0 | app1 | ok | 53 | 2162ms | 4398ms | 4940ms |
| 61.0 | 71.0 | app2 | ok | 32 | 5789ms | 9158ms | 9916ms |
| 61.0 | 71.0 | end-users | ok | 170 | 2937ms | 4587ms | 4959ms |
| 71.0 | 81.0 | app1 | ok | 52 | 2239ms | 4409ms | 4941ms |
| 71.0 | 81.0 | app2 | ok | 20 | 7500ms | 9500ms | 9950ms |
| 71.0 | 81.0 | end-users | ok | 172 | 3497ms | 4699ms | 4970ms |
| 81.0 | 91.0 | app1 | ok | 41 | 1788ms | 4068ms | 4907ms |
| 81.0 | 91.0 | app2 | ok | 20 | 7500ms | 9500ms | 9950ms |
| 81.0 | 91.0 | end-users | ok | 133 | 3446ms | 4689ms | 4969ms |
| 91.0 | 101.0 | app1 | ok | 51 | 1798ms | 3841ms | 4884ms |
| 91.0 | 101.0 | app2 | ok | 42 | 6500ms | 9300ms | 9930ms |
| 91.0 | 101.0 | end-users | ok | 195 | 3271ms | 4654ms | 4965ms |
| 101.0 | 111.0 | app1 | ok | 45 | 3831ms | 7188ms | 9719ms |
| 101.0 | 111.0 | app2 | ok | 6 | 8750ms | 24000ms | 29400ms |
| 101.0 | 111.0 | end-users | ok | 115 | 3652ms | 7500ms | 9750ms |
| 111.0 | 121.0 | app1 | ok | 51 | 2219ms | 4393ms | 4939ms |
| 111.0 | 121.0 | app2 | ok | 26 | 7708ms | 9875ms | 27400ms |
| 111.0 | 121.0 | end-users | ok | 170 | 3426ms | 4685ms | 4969ms |
| 121.0 | 131.0 | app1 | ok | 40 | 2023ms | 4231ms | 4923ms |
| 121.0 | 131.0 | app2 | ok | 20 | 7500ms | 9500ms | 9950ms |
| 121.0 | 131.0 | end-users | ok | 128 | 3545ms | 4709ms | 4971ms |
| 131.0 | 141.0 | app1 | ok | 51 | 1957ms | 4150ms | 4915ms |
| 131.0 | 141.0 | app2 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 131.0 | 141.0 | end-users | ok | 163 | 3575ms | 4715ms | 4972ms |
| 141.0 | 151.0 | app1 | ok | 44 | 1886ms | 4154ms | 4915ms |
| 141.0 | 151.0 | app2 | ok | 21 | 7500ms | 9500ms | 9950ms |
| 141.0 | 151.0 | end-users | ok | 139 | 3313ms | 4663ms | 4966ms |
| 151.0 | 161.0 | app1 | ok | 23 | 3304ms | 4946ms | 9425ms |
| 151.0 | 161.0 | app2 | ok | 13 | 8250ms | 21333ms | 29133ms |
| 151.0 | 161.0 | end-users | ok | 81 | 4137ms | 8442ms | 9844ms |
| 161.0 | 171.0 | app1 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 161.0 | 171.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 161.0 | 171.0 | end-users | ok | 80 | 8704ms | 23846ms | 29385ms |
| 171.0 | 181.0 | app1 | ok | 25 | 7396ms | 9479ms | 9948ms |
| 171.0 | 181.0 | app2 | ok | 13 | 20000ms | 28000ms | 29800ms |
| 171.0 | 181.0 | end-users | ok | 82 | 12917ms | 26583ms | 29658ms |
| 181.0 | 191.0 | app1 | ok | 24 | 7500ms | 9500ms | 9950ms |
| 181.0 | 191.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 181.0 | 191.0 | end-users | ok | 76 | 14167ms | 26833ms | 29683ms |
| 191.0 | 201.0 | app1 | ok | 25 | 7283ms | 9457ms | 9946ms |
| 191.0 | 201.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 191.0 | 201.0 | end-users | ok | 83 | 13725ms | 26745ms | 29675ms |
| 201.0 | 211.0 | app1 | ok | 25 | 7396ms | 9479ms | 9948ms |
| 201.0 | 211.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 201.0 | 211.0 | end-users | ok | 79 | 13191ms | 26638ms | 29664ms |
| 211.0 | 221.0 | app1 | ok | 28 | 7083ms | 9417ms | 9942ms |
| 211.0 | 221.0 | app2 | ok | 14 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | end-users | ok | 92 | 10000ms | 26000ms | 29600ms |
| 221.0 | 231.0 | app1 | ok | 24 | 7391ms | 9478ms | 9948ms |
| 221.0 | 231.0 | app2 | ok | 14 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | end-users | ok | 77 | 13958ms | 26792ms | 29679ms |
| 231.0 | 241.0 | app1 | ok | 13 | 7292ms | 9458ms | 9946ms |
| 231.0 | 241.0 | app2 | ok | 5 | 20000ms | 28000ms | 29800ms |
| 231.0 | 241.0 | end-users | ok | 44 | 11667ms | 26333ms | 29633ms |
| 241.0 | 251.0 | app1 | ok | 37 | 7279ms | 9456ms | 9946ms |
| 241.0 | 251.0 | app2 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | end-users | ok | 119 | 13699ms | 26740ms | 29674ms |
| 251.0 | 261.0 | app1 | ok | 21 | 7500ms | 9500ms | 9950ms |
| 251.0 | 261.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | end-users | ok | 68 | 15217ms | 27043ms | 29704ms |
| 261.0 | 271.0 | app1 | ok | 15 | 7321ms | 9464ms | 9946ms |
| 261.0 | 271.0 | app2 | ok | 8 | 20000ms | 28000ms | 29800ms |
| 261.0 | 271.0 | end-users | ok | 49 | 9900ms | 25917ms | 29592ms |
| 271.0 | 281.0 | app1 | ok | 24 | 7500ms | 9500ms | 9950ms |
| 271.0 | 281.0 | app2 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 271.0 | 281.0 | end-users | ok | 80 | 12979ms | 26596ms | 29660ms |
| 281.0 | 291.0 | app1 | ok | 27 | 7404ms | 9481ms | 9948ms |
| 281.0 | 291.0 | app2 | ok | 13 | 20000ms | 28000ms | 29800ms |
| 281.0 | 291.0 | end-users | ok | 86 | 12083ms | 26417ms | 29642ms |
| 291.0 | 302.0 | app1 | ok | 28 | 7083ms | 9417ms | 9942ms |
| 291.0 | 302.0 | app2 | ok | 14 | 20000ms | 28000ms | 29800ms |
| 291.0 | 302.0 | end-users | ok | 90 | 11633ms | 26327ms | 29633ms |
| 302.0 | 312.0 | app1 | ok | 21 | 7500ms | 9500ms | 9950ms |
| 302.0 | 312.0 | app2 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 302.0 | 312.0 | end-users | ok | 70 | 16000ms | 27200ms | 29720ms |
| 312.0 | 322.0 | app1 | ok | 31 | 6630ms | 9326ms | 9933ms |
| 312.0 | 322.0 | app2 | ok | 15 | 20000ms | 28000ms | 29800ms |
| 312.0 | 322.0 | end-users | ok | 100 | 9717ms | 25745ms | 29574ms |
| 322.0 | 332.0 | app1 | ok | 21 | 7500ms | 9500ms | 9950ms |
| 322.0 | 332.0 | app2 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 322.0 | 332.0 | end-users | ok | 68 | 15532ms | 27106ms | 29711ms |
| 332.0 | 342.0 | app1 | ok | 14 | 6818ms | 9364ms | 9936ms |
| 332.0 | 342.0 | app2 | ok | 8 | 20000ms | 28000ms | 29800ms |
| 332.0 | 342.0 | end-users | ok | 45 | 9891ms | 25909ms | 29591ms |
| 342.0 | 352.0 | app1 | ok | 25 | 7396ms | 9479ms | 9948ms |
| 342.0 | 352.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 342.0 | 352.0 | end-users | ok | 82 | 12917ms | 26583ms | 29658ms |
| 352.0 | 362.0 | app1 | ok | 25 | 7396ms | 9479ms | 9948ms |
| 352.0 | 362.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 352.0 | 362.0 | end-users | ok | 80 | 12222ms | 26444ms | 29644ms |
| 362.0 | 372.0 | app1 | ok | 23 | 7500ms | 9500ms | 9950ms |
| 362.0 | 372.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 362.0 | 372.0 | end-users | ok | 74 | 13913ms | 26783ms | 29678ms |
| 372.0 | 382.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app2 | ok | 16 | 20000ms | 28000ms | 29800ms |
| 372.0 | 382.0 | end-users | ok | 24 | 20000ms | 28000ms | 29800ms |
| 382.0 | 388.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 388.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 388.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1517820 | 75263 | 1593083.0 | 0.0% | 1633152.0 | 1668346.0 | -2.1% | True |
| app2 | 777360 | 38572 | 815932.0 | 0.0% | 823430.0 | 854504.0 | -3.6% | True |
| end-users | 4956900 | 246925 | 5203825.0 | 0.0% | 5326182.0 | 5450750.0 | -2.3% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1234 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 633 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 4030 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5897). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5897 | 0.051ms | 0.118ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 368505 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1234 | 7941ms | 14396ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 632 | 14849ms | 28761ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 4030 | 9756ms | 19375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5896 | 10232ms | 19880ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (39 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 3091ms | 4733ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2500ms | 4450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2778ms | 4938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 6955ms | 11583ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 9600ms | 14458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 7507ms | 12819ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 6480ms | 9300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 13000ms | 18500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 8120ms | 9980ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 41.0 | app1 | ok | 6562ms | 7912ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 41.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 41.0 | end-users | ok | 8207ms | 9821ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | app1 | ok | 6719ms | 8775ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | end-users | ok | 8179ms | 9861ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app1 | ok | 6757ms | 7876ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app2 | ok | 12609ms | 14957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | end-users | ok | 8247ms | 9825ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app1 | ok | 6455ms | 9375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app2 | ok | 13026ms | 18562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | end-users | ok | 8235ms | 12833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app1 | ok | 6912ms | 9060ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app2 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | end-users | ok | 7985ms | 9976ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 6467ms | 9608ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app2 | ok | 12763ms | 18438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 8262ms | 13396ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 6810ms | 9573ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 12614ms | 14966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 8379ms | 13337ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 7226ms | 9560ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 13636ms | 19200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 9247ms | 14138ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 6844ms | 9060ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 14028ms | 19341ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 8396ms | 13980ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 6682ms | 9478ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 7986ms | 9979ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 6645ms | 8400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 8344ms | 9854ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 6733ms | 9167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 12604ms | 14948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 8210ms | 9910ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 7136ms | 9529ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 12647ms | 15500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 8840ms | 13050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 12143ms | 14714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 12873ms | 18075ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 302.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 302.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 302.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 302.0 | 312.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 302.0 | 312.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 302.0 | 312.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app2 | ok | 23824ms | 29382ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 388.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 388.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 388.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
