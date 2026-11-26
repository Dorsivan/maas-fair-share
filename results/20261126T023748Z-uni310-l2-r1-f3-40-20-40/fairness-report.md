# Fairness benchmark: full-contention-2x (uni310-l2-r1-f3-40-20-40)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 26.7 points

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-6fcfcd8949-h67zg` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T02:39:08Z` |
| Run end | `2026-11-26T02:44:51Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 36 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/36 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 94.00 | 2.9375 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 40.0 | 64 | 2108 | 200=2108 | 7.2 | 9.5 | 2814404.0 | 40.0% | 16.7% | -23.3 | 39.0% | -1.0 | 38.0% | -2.0 | 76.8s | 98.9% | 2108.0 |
| app2 | 20.0 | 64 | 1103 | 200=1103 | 14.2 | 17.4 | 1460406.0 | 20.0% | 16.7% | -3.3 | 20.2% | 0.2 | 19.9% | -0.1 | 79.3s | 98.9% | 1103.0 |
| end-users | 40.0 | 256 | 2333 | 000=1, 200=2332 | 28.5 | 32.1 | 2945210.0 | 40.0% | 66.7% | 26.7 | 40.8% | 0.8 | 42.1% | 2.1 | 79.3s | 98.9% | 2333.0 |
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
| 0.0 | 20.0 | 20.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (35 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 24326.0 | 40.0% | 100.0% | 60.0 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 20.0% | 0.0% | -20.0 |
| 0.0 | 10.0 | end-users | True | False | 0.0 | 40.0% | 0.0% | -40.0 |
| 10.0 | 20.0 | app1 | True | False | 125822.0 | 40.0% | 49.5% | 9.5 |
| 10.0 | 20.0 | app2 | True | False | 62160.0 | 20.0% | 24.4% | 4.4 |
| 10.0 | 20.0 | end-users | True | False | 66264.0 | 40.0% | 26.1% | -13.9 |
| 20.0 | 30.0 | app1 | True | False | 120400.0 | 40.0% | 39.2% | -0.8 |
| 20.0 | 30.0 | app2 | True | False | 62244.0 | 20.0% | 20.3% | 0.3 |
| 20.0 | 30.0 | end-users | True | False | 124244.0 | 40.0% | 40.5% | 0.5 |
| 30.0 | 40.0 | app1 | True | False | 123194.0 | 40.0% | 40.4% | 0.4 |
| 30.0 | 40.0 | app2 | True | False | 62304.0 | 20.0% | 20.5% | 0.5 |
| 30.0 | 40.0 | end-users | True | False | 119080.0 | 40.0% | 39.1% | -0.9 |
| 40.0 | 50.0 | app1 | True | False | 98862.0 | 40.0% | 39.7% | -0.3 |
| 40.0 | 50.0 | app2 | True | False | 48726.0 | 20.0% | 19.6% | -0.4 |
| 40.0 | 50.0 | end-users | True | False | 101462.0 | 40.0% | 40.7% | 0.7 |
| 50.0 | 60.0 | app1 | True | False | 127154.0 | 40.0% | 42.2% | 2.2 |
| 50.0 | 60.0 | app2 | True | False | 56802.0 | 20.0% | 18.8% | -1.2 |
| 50.0 | 60.0 | end-users | True | False | 117688.0 | 40.0% | 39.0% | -1.0 |
| 60.0 | 70.0 | app1 | True | False | 112352.0 | 40.0% | 37.7% | -2.3 |
| 60.0 | 70.0 | app2 | True | False | 62194.0 | 20.0% | 20.9% | 0.9 |
| 60.0 | 70.0 | end-users | True | False | 123122.0 | 40.0% | 41.4% | 1.4 |
| 70.0 | 80.0 | app1 | True | False | 123134.0 | 40.0% | 40.5% | 0.5 |
| 70.0 | 80.0 | app2 | True | False | 60882.0 | 20.0% | 20.0% | 0.0 |
| 70.0 | 80.0 | end-users | True | False | 120336.0 | 40.0% | 39.5% | -0.5 |
| 80.0 | 90.0 | app1 | True | False | 124412.0 | 40.0% | 40.0% | 0.0 |
| 80.0 | 90.0 | app2 | True | False | 63526.0 | 20.0% | 20.4% | 0.4 |
| 80.0 | 90.0 | end-users | True | False | 122936.0 | 40.0% | 39.5% | -0.5 |
| 90.0 | 100.0 | app1 | True | False | 121606.0 | 40.0% | 40.2% | 0.2 |
| 90.0 | 100.0 | app2 | True | False | 60806.0 | 20.0% | 20.1% | 0.1 |
| 90.0 | 100.0 | end-users | True | False | 120380.0 | 40.0% | 39.8% | -0.2 |
| 100.0 | 110.0 | app1 | True | False | 116032.0 | 40.0% | 39.9% | -0.1 |
| 100.0 | 110.0 | app2 | True | False | 56848.0 | 20.0% | 19.6% | -0.4 |
| 100.0 | 110.0 | end-users | True | False | 117702.0 | 40.0% | 40.5% | 0.5 |
| 110.0 | 120.0 | app1 | True | False | 68898.0 | 40.0% | 33.5% | -6.5 |
| 110.0 | 120.0 | app2 | True | False | 47332.0 | 20.0% | 23.0% | 3.0 |
| 110.0 | 120.0 | end-users | True | False | 89272.0 | 40.0% | 43.4% | 3.4 |
| 120.0 | 130.0 | app1 | True | False | 95924.0 | 40.0% | 35.8% | -4.2 |
| 120.0 | 130.0 | app2 | True | False | 56756.0 | 20.0% | 21.2% | 1.2 |
| 120.0 | 130.0 | end-users | True | False | 114932.0 | 40.0% | 42.9% | 2.9 |
| 130.0 | 140.0 | app1 | True | False | 117502.0 | 40.0% | 38.3% | -1.7 |
| 130.0 | 140.0 | app2 | True | False | 62224.0 | 20.0% | 20.3% | 0.3 |
| 130.0 | 140.0 | end-users | True | False | 127158.0 | 40.0% | 41.4% | 1.4 |
| 140.0 | 150.0 | app1 | True | False | 123076.0 | 40.0% | 39.9% | -0.1 |
| 140.0 | 150.0 | app2 | True | False | 60734.0 | 20.0% | 19.7% | -0.3 |
| 140.0 | 150.0 | end-users | True | False | 124352.0 | 40.0% | 40.4% | 0.4 |
| 150.0 | 160.0 | app1 | True | False | 120458.0 | 40.0% | 39.8% | -0.2 |
| 150.0 | 160.0 | app2 | True | False | 60866.0 | 20.0% | 20.1% | 0.1 |
| 150.0 | 160.0 | end-users | True | False | 121694.0 | 40.0% | 40.2% | 0.2 |
| 160.0 | 171.0 | app1 | True | False | 123138.0 | 40.0% | 40.3% | 0.3 |
| 160.0 | 171.0 | app2 | True | False | 60828.0 | 20.0% | 19.9% | -0.1 |
| 160.0 | 171.0 | end-users | True | False | 121584.0 | 40.0% | 39.8% | -0.2 |
| 171.0 | 181.0 | app1 | True | False | 121816.0 | 40.0% | 40.2% | 0.2 |
| 171.0 | 181.0 | app2 | True | False | 62182.0 | 20.0% | 20.5% | 0.5 |
| 171.0 | 181.0 | end-users | True | False | 119010.0 | 40.0% | 39.3% | -0.7 |
| 181.0 | 191.0 | app1 | True | False | 122978.0 | 40.0% | 39.9% | -0.1 |
| 181.0 | 191.0 | app2 | True | False | 60796.0 | 20.0% | 19.7% | -0.3 |
| 181.0 | 191.0 | end-users | True | False | 124458.0 | 40.0% | 40.4% | 0.4 |
| 191.0 | 201.0 | app1 | True | False | 121694.0 | 40.0% | 40.2% | 0.2 |
| 191.0 | 201.0 | app2 | True | False | 60806.0 | 20.0% | 20.1% | 0.1 |
| 191.0 | 201.0 | end-users | True | False | 120590.0 | 40.0% | 39.8% | -0.2 |
| 201.0 | 211.0 | app1 | True | False | 131298.0 | 40.0% | 43.5% | 3.5 |
| 201.0 | 211.0 | app2 | True | False | 56728.0 | 20.0% | 18.8% | -1.2 |
| 201.0 | 211.0 | end-users | True | False | 113606.0 | 40.0% | 37.7% | -2.3 |
| 211.0 | 221.0 | app1 | True | False | 109584.0 | 40.0% | 36.2% | -3.8 |
| 211.0 | 221.0 | app2 | True | False | 64922.0 | 20.0% | 21.4% | 1.4 |
| 211.0 | 221.0 | end-users | True | False | 128506.0 | 40.0% | 42.4% | 2.4 |
| 221.0 | 231.0 | app1 | True | False | 121600.0 | 40.0% | 40.3% | 0.3 |
| 221.0 | 231.0 | app2 | True | False | 59624.0 | 20.0% | 19.8% | -0.2 |
| 221.0 | 231.0 | end-users | True | False | 120274.0 | 40.0% | 39.9% | -0.1 |
| 231.0 | 241.0 | app1 | True | False | 124378.0 | 40.0% | 40.9% | 0.9 |
| 231.0 | 241.0 | app2 | True | False | 59502.0 | 20.0% | 19.6% | -0.4 |
| 231.0 | 241.0 | end-users | True | False | 120320.0 | 40.0% | 39.6% | -0.4 |
| 241.0 | 251.0 | app1 | False | n/a | 94766.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 70346.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 140616.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 20268.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | n/a | 125624.0 | n/a | n/a | n/a |
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
| 0.0 | 10.0 | app1 | ok | 81 | 477ms | 2108ms | 2461ms |
| 0.0 | 10.0 | app2 | ok | 42 | 0ms | 2168ms | 2467ms |
| 0.0 | 10.0 | end-users | ok | 89 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 105 | 2082ms | 4309ms | 4931ms |
| 10.0 | 20.0 | app2 | ok | 52 | 7051ms | 9718ms | 26533ms |
| 10.0 | 20.0 | end-users | ok | 100 | 9717ms | 25745ms | 29574ms |
| 20.0 | 30.0 | app1 | ok | 95 | 2234ms | 4391ms | 4939ms |
| 20.0 | 30.0 | app2 | ok | 48 | 7791ms | 10800ms | 28080ms |
| 20.0 | 30.0 | end-users | ok | 94 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | app1 | ok | 72 | 2275ms | 4400ms | 4940ms |
| 30.0 | 40.0 | app2 | ok | 36 | 8214ms | 21000ms | 29100ms |
| 30.0 | 40.0 | end-users | ok | 72 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app1 | ok | 53 | 2057ms | 4338ms | 4934ms |
| 40.0 | 50.0 | app2 | ok | 38 | 7857ms | 19143ms | 28914ms |
| 40.0 | 50.0 | end-users | ok | 76 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app1 | ok | 119 | 3585ms | 7167ms | 9717ms |
| 50.0 | 60.0 | app2 | ok | 46 | 12308ms | 26462ms | 29646ms |
| 50.0 | 60.0 | end-users | ok | 92 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app1 | ok | 93 | 2675ms | 4535ms | 4954ms |
| 60.0 | 70.0 | app2 | ok | 47 | 8013ms | 18250ms | 28825ms |
| 60.0 | 70.0 | end-users | ok | 96 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app1 | ok | 90 | 2286ms | 4408ms | 4941ms |
| 70.0 | 80.0 | app2 | ok | 46 | 8286ms | 21636ms | 29164ms |
| 70.0 | 80.0 | end-users | ok | 92 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app1 | ok | 94 | 2324ms | 4427ms | 4943ms |
| 80.0 | 90.0 | app2 | ok | 47 | 8264ms | 21455ms | 29145ms |
| 80.0 | 90.0 | end-users | ok | 92 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app1 | ok | 85 | 1938ms | 4183ms | 4918ms |
| 90.0 | 100.0 | app2 | ok | 42 | 7917ms | 16000ms | 28600ms |
| 90.0 | 100.0 | end-users | ok | 85 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app1 | ok | 55 | 2031ms | 4312ms | 4931ms |
| 100.0 | 110.0 | app2 | ok | 61 | 6048ms | 9984ms | 27967ms |
| 100.0 | 110.0 | end-users | ok | 123 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app1 | ok | 64 | 8000ms | 22889ms | 29289ms |
| 110.0 | 120.0 | app2 | ok | 34 | 7500ms | 21500ms | 29150ms |
| 110.0 | 120.0 | end-users | ok | 66 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app1 | ok | 93 | 4215ms | 8591ms | 9859ms |
| 120.0 | 130.0 | app2 | ok | 28 | 7692ms | 9846ms | 27200ms |
| 120.0 | 130.0 | end-users | ok | 57 | 20000ms | 28000ms | 29800ms |
| 130.0 | 140.0 | app1 | ok | 73 | 3016ms | 4603ms | 4960ms |
| 130.0 | 140.0 | app2 | ok | 38 | 8654ms | 23667ms | 29367ms |
| 130.0 | 140.0 | end-users | ok | 75 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app1 | ok | 111 | 1958ms | 4229ms | 4923ms |
| 140.0 | 150.0 | app2 | ok | 55 | 7806ms | 11667ms | 28167ms |
| 140.0 | 150.0 | end-users | ok | 112 | 20000ms | 28000ms | 29800ms |
| 150.0 | 160.0 | app1 | ok | 74 | 2171ms | 4339ms | 4934ms |
| 150.0 | 160.0 | app2 | ok | 37 | 8190ms | 20750ms | 29075ms |
| 150.0 | 160.0 | end-users | ok | 73 | 20000ms | 28000ms | 29800ms |
| 160.0 | 171.0 | app1 | ok | 97 | 2165ms | 4362ms | 4936ms |
| 160.0 | 171.0 | app2 | ok | 49 | 8141ms | 20200ms | 29020ms |
| 160.0 | 171.0 | end-users | ok | 98 | 20000ms | 28000ms | 29800ms |
| 171.0 | 181.0 | app1 | ok | 84 | 2134ms | 4344ms | 4934ms |
| 171.0 | 181.0 | app2 | ok | 42 | 8281ms | 21600ms | 29160ms |
| 171.0 | 181.0 | end-users | ok | 86 | 20000ms | 28000ms | 29800ms |
| 181.0 | 191.0 | app1 | ok | 97 | 2228ms | 4362ms | 4936ms |
| 181.0 | 191.0 | app2 | ok | 48 | 8243ms | 21273ms | 29127ms |
| 181.0 | 191.0 | end-users | ok | 94 | 20000ms | 28000ms | 29800ms |
| 191.0 | 201.0 | app1 | ok | 78 | 2176ms | 4371ms | 4937ms |
| 191.0 | 201.0 | app2 | ok | 40 | 8333ms | 22000ms | 29200ms |
| 191.0 | 201.0 | end-users | ok | 79 | 20000ms | 28000ms | 29800ms |
| 201.0 | 211.0 | app1 | ok | 100 | 2267ms | 4562ms | 8333ms |
| 201.0 | 211.0 | app2 | ok | 48 | 8026ms | 19333ms | 28933ms |
| 201.0 | 211.0 | end-users | ok | 96 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app1 | ok | 75 | 2917ms | 4583ms | 4958ms |
| 211.0 | 221.0 | app2 | ok | 39 | 8145ms | 20250ms | 29025ms |
| 211.0 | 221.0 | end-users | ok | 79 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app1 | ok | 115 | 2125ms | 4564ms | 8562ms |
| 221.0 | 231.0 | app2 | ok | 70 | 7456ms | 9912ms | 27667ms |
| 221.0 | 231.0 | end-users | ok | 140 | 20000ms | 28000ms | 29800ms |
| 231.0 | 241.0 | app1 | ok | 88 | 3456ms | 4750ms | 7800ms |
| 231.0 | 241.0 | app2 | ok | 32 | 8077ms | 19333ms | 28933ms |
| 231.0 | 241.0 | end-users | ok | 62 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | app1 | ok | 17 | 3365ms | 4673ms | 4967ms |
| 241.0 | 251.0 | app2 | ok | 38 | 7500ms | 9500ms | 9950ms |
| 241.0 | 251.0 | end-users | ok | 140 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 65 | 20000ms | 28000ms | 29800ms |
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

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2592840 | 129039 | 2721879.0 | 0.0% | 2814404.0 | 2850918.0 | -1.3% | True |
| app2 | 1356690 | 67424 | 1424114.0 | 0.0% | 1460406.0 | 1491538.0 | -2.1% | True |
| end-users | 2868360 | 142552 | 3010912.0 | 0.0% | 2945210.0 | 3153464.0 | -6.6% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2108 | 0 | 0 | 0 (never shed) | 0.00% | 40.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1103 | 0 | 0 | 0 (never shed) | 0.00% | 20.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2333 | 0 | 0 | 0 (never shed) | 0.00% | 40.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5544). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5544 | 0.051ms | 0.125ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 323795 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 2108 | 7179ms | 9894ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1103 | 13704ms | 19269ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 2332 | 25895ms | 41731ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5543 | 13682ms | 37229ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (35 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 1917ms | 3795ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2071ms | 3962ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2107ms | 4592ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 5983ms | 7798ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 8600ms | 14281ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 9211ms | 14399ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 6985ms | 9191ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 12674ms | 16167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 18854ms | 28686ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 6980ms | 9545ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 25116ms | 29721ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 7324ms | 9708ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 13750ms | 19250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 26048ms | 40673ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 7586ms | 10300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 17308ms | 19731ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 34805ms | 43980ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 8128ms | 10850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 15000ms | 19500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 33026ms | 43803ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 7075ms | 9567ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 13125ms | 18750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 29889ms | 43483ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 6905ms | 9600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 13561ms | 19161ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 25353ms | 33625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 7070ms | 9640ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 13516ms | 19135ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 25633ms | 38325ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 7111ms | 9427ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 13088ms | 18688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 11458ms | 14646ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 17348ms | 19735ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 36000ms | 44100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 9651ms | 14366ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 17237ms | 19724ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 36930ms | 44193ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 7750ms | 9777ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 15400ms | 19540ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 36897ms | 44190ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 7324ms | 9724ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 12812ms | 17750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | end-users | ok | 27667ms | 42844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 7000ms | 9407ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 13125ms | 18750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | end-users | ok | 25114ms | 29716ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 171.0 | app1 | ok | 7117ms | 9521ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 171.0 | app2 | ok | 13125ms | 18750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 171.0 | end-users | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 6982ms | 9471ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 13286ms | 18955ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 25176ms | 29835ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 7078ms | 9431ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 13125ms | 18750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 25227ms | 29932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 6957ms | 9571ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 13409ms | 19062ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 25361ms | 33875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 6795ms | 9559ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 14565ms | 19447ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 26269ms | 41294ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 7270ms | 9700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 14286ms | 19400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 25655ms | 38523ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 7400ms | 9853ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 14074ms | 19353ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 26953ms | 42330ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 6475ms | 7878ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 15417ms | 19542ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 25361ms | 33875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 8600ms | 9860ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 13171ms | 18818ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 25417ms | 35250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 13409ms | 19062ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 21573ms | 29562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
