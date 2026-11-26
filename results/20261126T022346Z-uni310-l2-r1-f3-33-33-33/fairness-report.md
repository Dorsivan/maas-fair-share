# Fairness benchmark: full-contention-2x (uni310-l2-r1-f3-33-33-33)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 33.3 points

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58db447685-m64f8` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T02:24:57Z` |
| Run end | `2026-11-26T02:33:53Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 55 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/55 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 83.00 | 2.5938 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 33.0 | 64 | 1714 | 000=1, 200=1713 | 8.6 | 11.5 | 2286262.0 | 33.3% | 16.7% | -16.7 | 32.4% | -0.9 | 31.5% | -1.8 | 69.1s | 98.9% | 1714.0 |
| app2 | 33.0 | 64 | 1720 | 200=1720 | 8.7 | 11.8 | 2303062.0 | 33.3% | 16.7% | -16.7 | 32.7% | -0.7 | 31.6% | -1.7 | 69.1s | 98.9% | 1720.0 |
| end-users | 33.0 | 256 | 2009 | 000=1, 200=2008 | 34.1 | 37.9 | 2458508.0 | 33.3% | 66.7% | 33.3 | 34.9% | 1.5 | 36.9% | 3.6 | 69.1s | 98.9% | 2009.0 |
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
| 0.0 | 30.0 | 30.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (54 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 16232.0 | 33.3% | 50.0% | 16.6 |
| 0.0 | 10.0 | app2 | True | False | 16252.0 | 33.3% | 50.0% | 16.7 |
| 0.0 | 10.0 | end-users | True | False | 0.0 | 33.3% | 0.0% | -33.3 |
| 10.0 | 20.0 | app1 | True | False | 27034.0 | 33.3% | 22.2% | -11.1 |
| 10.0 | 20.0 | app2 | True | False | 35160.0 | 33.3% | 28.9% | -4.4 |
| 10.0 | 20.0 | end-users | True | False | 59518.0 | 33.3% | 48.9% | 15.6 |
| 20.0 | 30.0 | app1 | True | False | 66242.0 | 33.3% | 27.1% | -6.3 |
| 20.0 | 30.0 | app2 | True | False | 66208.0 | 33.3% | 27.0% | -6.3 |
| 20.0 | 30.0 | end-users | True | False | 112366.0 | 33.3% | 45.9% | 12.6 |
| 30.0 | 40.0 | app1 | True | False | 101432.0 | 33.3% | 32.7% | -0.6 |
| 30.0 | 40.0 | app2 | True | False | 104216.0 | 33.3% | 33.6% | 0.3 |
| 30.0 | 40.0 | end-users | True | False | 104096.0 | 33.3% | 33.6% | 0.3 |
| 40.0 | 50.0 | app1 | True | False | 105494.0 | 33.3% | 33.9% | 0.6 |
| 40.0 | 50.0 | app2 | True | False | 101446.0 | 33.3% | 32.6% | -0.7 |
| 40.0 | 50.0 | end-users | True | False | 104148.0 | 33.3% | 33.5% | 0.1 |
| 50.0 | 61.0 | app1 | True | False | 101370.0 | 33.3% | 32.9% | -0.4 |
| 50.0 | 61.0 | app2 | True | False | 102684.0 | 33.3% | 33.3% | -0.0 |
| 50.0 | 61.0 | end-users | True | False | 104182.0 | 33.3% | 33.8% | 0.5 |
| 61.0 | 71.0 | app1 | True | False | 104130.0 | 33.3% | 33.8% | 0.5 |
| 61.0 | 71.0 | app2 | True | False | 104102.0 | 33.3% | 33.8% | 0.4 |
| 61.0 | 71.0 | end-users | True | False | 99930.0 | 33.3% | 32.4% | -0.9 |
| 71.0 | 81.0 | app1 | True | False | 98762.0 | 33.3% | 32.9% | -0.5 |
| 71.0 | 81.0 | app2 | True | False | 100134.0 | 33.3% | 33.3% | 0.0 |
| 71.0 | 81.0 | end-users | True | False | 101446.0 | 33.3% | 33.8% | 0.4 |
| 81.0 | 91.0 | app1 | True | False | 100132.0 | 33.3% | 32.9% | -0.4 |
| 81.0 | 91.0 | app2 | True | False | 101436.0 | 33.3% | 33.3% | 0.0 |
| 81.0 | 91.0 | end-users | True | False | 102708.0 | 33.3% | 33.8% | 0.4 |
| 91.0 | 101.0 | app1 | True | False | 103948.0 | 33.3% | 33.6% | 0.3 |
| 91.0 | 101.0 | app2 | True | False | 101424.0 | 33.3% | 32.8% | -0.6 |
| 91.0 | 101.0 | end-users | True | False | 104082.0 | 33.3% | 33.6% | 0.3 |
| 101.0 | 111.0 | app1 | True | False | 100004.0 | 33.3% | 33.3% | 0.0 |
| 101.0 | 111.0 | app2 | True | False | 102656.0 | 33.3% | 34.2% | 0.9 |
| 101.0 | 111.0 | end-users | True | False | 97310.0 | 33.3% | 32.4% | -0.9 |
| 111.0 | 121.0 | app1 | True | False | 101528.0 | 33.3% | 32.9% | -0.4 |
| 111.0 | 121.0 | app2 | True | False | 102710.0 | 33.3% | 33.3% | -0.0 |
| 111.0 | 121.0 | end-users | True | False | 104142.0 | 33.3% | 33.8% | 0.4 |
| 121.0 | 131.0 | app1 | True | False | 87852.0 | 33.3% | 33.8% | 0.5 |
| 121.0 | 131.0 | app2 | True | False | 86486.0 | 33.3% | 33.3% | -0.0 |
| 121.0 | 131.0 | end-users | True | False | 85230.0 | 33.3% | 32.8% | -0.5 |
| 131.0 | 141.0 | app1 | True | False | 99990.0 | 33.3% | 32.6% | -0.7 |
| 131.0 | 141.0 | app2 | True | False | 101376.0 | 33.3% | 33.0% | -0.3 |
| 131.0 | 141.0 | end-users | True | False | 105438.0 | 33.3% | 34.4% | 1.0 |
| 141.0 | 151.0 | app1 | True | False | 101338.0 | 33.3% | 33.5% | 0.1 |
| 141.0 | 151.0 | app2 | True | False | 100146.0 | 33.3% | 33.1% | -0.3 |
| 141.0 | 151.0 | end-users | True | False | 101380.0 | 33.3% | 33.5% | 0.1 |
| 151.0 | 161.0 | app1 | True | False | 98748.0 | 33.3% | 32.7% | -0.6 |
| 151.0 | 161.0 | app2 | True | False | 102770.0 | 33.3% | 34.1% | 0.7 |
| 151.0 | 161.0 | end-users | True | False | 100164.0 | 33.3% | 33.2% | -0.1 |
| 161.0 | 171.0 | app1 | True | False | 100072.0 | 33.3% | 33.9% | 0.6 |
| 161.0 | 171.0 | app2 | True | False | 97418.0 | 33.3% | 33.0% | -0.3 |
| 161.0 | 171.0 | end-users | True | False | 97344.0 | 33.3% | 33.0% | -0.3 |
| 171.0 | 181.0 | app1 | True | False | 98674.0 | 33.3% | 33.3% | -0.0 |
| 171.0 | 181.0 | app2 | True | False | 97454.0 | 33.3% | 32.9% | -0.4 |
| 171.0 | 181.0 | end-users | True | False | 100208.0 | 33.3% | 33.8% | 0.5 |
| 181.0 | 191.0 | app1 | True | False | 99890.0 | 33.3% | 33.3% | -0.0 |
| 181.0 | 191.0 | app2 | True | False | 100162.0 | 33.3% | 33.4% | 0.0 |
| 181.0 | 191.0 | end-users | True | False | 100010.0 | 33.3% | 33.3% | -0.0 |
| 191.0 | 201.0 | app1 | True | False | 101438.0 | 33.3% | 33.0% | -0.3 |
| 191.0 | 201.0 | app2 | True | False | 104116.0 | 33.3% | 33.9% | 0.6 |
| 191.0 | 201.0 | end-users | True | False | 101528.0 | 33.3% | 33.1% | -0.3 |
| 201.0 | 211.0 | app1 | True | False | 102790.0 | 33.3% | 33.5% | 0.2 |
| 201.0 | 211.0 | app2 | True | False | 101348.0 | 33.3% | 33.0% | -0.3 |
| 201.0 | 211.0 | end-users | True | False | 102756.0 | 33.3% | 33.5% | 0.1 |
| 211.0 | 221.0 | app1 | True | False | 100138.0 | 33.3% | 33.0% | -0.3 |
| 211.0 | 221.0 | app2 | True | False | 101480.0 | 33.3% | 33.5% | 0.2 |
| 211.0 | 221.0 | end-users | True | False | 101442.0 | 33.3% | 33.5% | 0.1 |
| 221.0 | 231.0 | app1 | True | False | 81076.0 | 33.3% | 34.7% | 1.4 |
| 221.0 | 231.0 | app2 | True | False | 81032.0 | 33.3% | 34.7% | 1.3 |
| 221.0 | 231.0 | end-users | True | False | 71584.0 | 33.3% | 30.6% | -2.7 |
| 231.0 | 241.0 | app1 | True | False | 89190.0 | 33.3% | 31.9% | -1.5 |
| 231.0 | 241.0 | app2 | True | False | 92030.0 | 33.3% | 32.9% | -0.5 |
| 231.0 | 241.0 | end-users | True | False | 98730.0 | 33.3% | 35.3% | 1.9 |
| 241.0 | 251.0 | app1 | False | n/a | 96052.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 92026.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 94640.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 2706.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 6790.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | n/a | 104126.0 | n/a | n/a | n/a |
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
| 301.0 | 312.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 312.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 312.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 312.0 | 322.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 312.0 | 322.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 312.0 | 322.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 536.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 536.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 532.0 | 536.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 50 | 50ms | 477ms | 938ms |
| 0.0 | 10.0 | app2 | ok | 55 | 132ms | 694ms | 969ms |
| 0.0 | 10.0 | end-users | ok | 201 | 103ms | 543ms | 954ms |
| 10.0 | 20.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 10.0 | 20.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 95 | 10208ms | 26042ms | 29604ms |
| 20.0 | 30.0 | app2 | ok | 95 | 9295ms | 25476ms | 29548ms |
| 20.0 | 30.0 | end-users | ok | 50 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | app1 | ok | 59 | 4016ms | 7318ms | 9732ms |
| 30.0 | 40.0 | app2 | ok | 60 | 4010ms | 7273ms | 9727ms |
| 30.0 | 40.0 | end-users | ok | 58 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app1 | ok | 83 | 3718ms | 4795ms | 7925ms |
| 40.0 | 50.0 | app2 | ok | 82 | 3633ms | 4727ms | 4973ms |
| 40.0 | 50.0 | end-users | ok | 82 | 20000ms | 28000ms | 29800ms |
| 50.0 | 61.0 | app1 | ok | 81 | 3698ms | 4823ms | 8650ms |
| 50.0 | 61.0 | app2 | ok | 81 | 3533ms | 4707ms | 4971ms |
| 50.0 | 61.0 | end-users | ok | 82 | 27447ms | 52971ms | 59297ms |
| 61.0 | 71.0 | app1 | ok | 65 | 3575ms | 4715ms | 4971ms |
| 61.0 | 71.0 | app2 | ok | 65 | 3618ms | 4759ms | 6750ms |
| 61.0 | 71.0 | end-users | ok | 65 | 20156ms | 28281ms | 40500ms |
| 71.0 | 81.0 | app1 | ok | 78 | 3681ms | 4764ms | 6100ms |
| 71.0 | 81.0 | app2 | ok | 78 | 3659ms | 4790ms | 8050ms |
| 71.0 | 81.0 | end-users | ok | 78 | 21143ms | 30750ms | 57075ms |
| 81.0 | 91.0 | app1 | ok | 72 | 3302ms | 4660ms | 4966ms |
| 81.0 | 91.0 | app2 | ok | 73 | 3403ms | 4755ms | 8175ms |
| 81.0 | 91.0 | end-users | ok | 72 | 21803ms | 40364ms | 58036ms |
| 91.0 | 101.0 | app1 | ok | 85 | 3414ms | 4683ms | 4968ms |
| 91.0 | 101.0 | app2 | ok | 84 | 3600ms | 4720ms | 4972ms |
| 91.0 | 101.0 | end-users | ok | 85 | 21806ms | 40385ms | 58038ms |
| 101.0 | 111.0 | app1 | ok | 80 | 3259ms | 4688ms | 6000ms |
| 101.0 | 111.0 | app2 | ok | 79 | 3371ms | 4781ms | 8683ms |
| 101.0 | 111.0 | end-users | ok | 78 | 21818ms | 40500ms | 58050ms |
| 111.0 | 121.0 | app1 | ok | 78 | 3643ms | 4757ms | 6100ms |
| 111.0 | 121.0 | app2 | ok | 80 | 3699ms | 4795ms | 8000ms |
| 111.0 | 121.0 | end-users | ok | 80 | 22698ms | 45882ms | 58588ms |
| 121.0 | 131.0 | app1 | ok | 57 | 2829ms | 7625ms | 9762ms |
| 121.0 | 131.0 | app2 | ok | 57 | 2708ms | 7625ms | 9762ms |
| 121.0 | 131.0 | end-users | ok | 57 | 23571ms | 48600ms | 58860ms |
| 131.0 | 141.0 | app1 | ok | 75 | 3733ms | 4774ms | 6250ms |
| 131.0 | 141.0 | app2 | ok | 74 | 3733ms | 4747ms | 4975ms |
| 131.0 | 141.0 | end-users | ok | 74 | 40179ms | 56036ms | 59604ms |
| 141.0 | 151.0 | app1 | ok | 83 | 3474ms | 4695ms | 4969ms |
| 141.0 | 151.0 | app2 | ok | 85 | 3438ms | 4688ms | 4969ms |
| 141.0 | 151.0 | end-users | ok | 84 | 37500ms | 55500ms | 59550ms |
| 151.0 | 161.0 | app1 | ok | 76 | 3250ms | 4770ms | 8733ms |
| 151.0 | 161.0 | app2 | ok | 74 | 3221ms | 4644ms | 4964ms |
| 151.0 | 161.0 | end-users | ok | 75 | 24423ms | 50217ms | 59022ms |
| 161.0 | 171.0 | app1 | ok | 67 | 3588ms | 4829ms | 8883ms |
| 161.0 | 171.0 | app2 | ok | 67 | 3705ms | 4923ms | 9330ms |
| 161.0 | 171.0 | end-users | ok | 68 | 25814ms | 51840ms | 59184ms |
| 171.0 | 181.0 | app1 | ok | 71 | 3514ms | 4854ms | 9113ms |
| 171.0 | 181.0 | app2 | ok | 70 | 3611ms | 4907ms | 9300ms |
| 171.0 | 181.0 | end-users | ok | 71 | 29189ms | 53735ms | 59374ms |
| 181.0 | 191.0 | app1 | ok | 67 | 2812ms | 4674ms | 8325ms |
| 181.0 | 191.0 | app2 | ok | 68 | 2778ms | 4667ms | 8300ms |
| 181.0 | 191.0 | end-users | ok | 66 | 26500ms | 52385ms | 59238ms |
| 191.0 | 201.0 | app1 | ok | 73 | 3278ms | 4656ms | 4966ms |
| 191.0 | 201.0 | app2 | ok | 73 | 3341ms | 4668ms | 4967ms |
| 191.0 | 201.0 | end-users | ok | 74 | 26087ms | 52071ms | 59207ms |
| 201.0 | 211.0 | app1 | ok | 73 | 3678ms | 4736ms | 4974ms |
| 201.0 | 211.0 | app2 | ok | 73 | 3714ms | 4772ms | 6350ms |
| 201.0 | 211.0 | end-users | ok | 72 | 25000ms | 51000ms | 59100ms |
| 211.0 | 221.0 | app1 | ok | 82 | 3066ms | 4613ms | 4961ms |
| 211.0 | 221.0 | app2 | ok | 84 | 3170ms | 4670ms | 5800ms |
| 211.0 | 221.0 | end-users | ok | 95 | 21585ms | 38077ms | 57808ms |
| 221.0 | 231.0 | app1 | ok | 44 | 5000ms | 9000ms | 9900ms |
| 221.0 | 231.0 | app2 | ok | 44 | 4808ms | 8952ms | 9895ms |
| 221.0 | 231.0 | end-users | ok | 66 | 23469ms | 48353ms | 58835ms |
| 231.0 | 241.0 | app1 | ok | 87 | 4289ms | 8500ms | 9850ms |
| 231.0 | 241.0 | app2 | ok | 85 | 4222ms | 8365ms | 9837ms |
| 231.0 | 241.0 | end-users | ok | 54 | 42391ms | 56478ms | 59648ms |
| 241.0 | 251.0 | app1 | ok | 33 | 3664ms | 4802ms | 8350ms |
| 241.0 | 251.0 | app2 | ok | 34 | 3833ms | 4967ms | 9433ms |
| 241.0 | 251.0 | end-users | ok | 105 | 28421ms | 53438ms | 59344ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 117 | 20000ms | 28000ms | 29800ms |
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
| 301.0 | 312.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 312.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 312.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 312.0 | 322.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 312.0 | 322.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 312.0 | 322.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 536.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 536.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 536.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2106990 | 104507 | 2211497.0 | 0.0% | 2286262.0 | 2316004.0 | -1.3% | True |
| app2 | 2115600 | 105199 | 2220799.0 | 0.0% | 2303062.0 | 2325998.0 | -1.0% | True |
| end-users | 2469840 | 122766 | 2592606.0 | 0.0% | 2458508.0 | 2715372.0 | -9.5% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1714 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1720 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2009 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5443). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5443 | 0.051ms | 0.156ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 501774 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1713 | 8663ms | 14585ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1720 | 8757ms | 14617ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 2008 | 35727ms | 44073ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5441 | 9971ms | 42487ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (54 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 1375ms | 3500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 1550ms | 3637ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2500ms | 3869ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 5800ms | 7778ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 6333ms | 9133ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 10366ms | 14537ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 17278ms | 19728ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 17278ms | 19728ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 16737ms | 19903ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 9157ms | 18750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 9135ms | 18717ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 26638ms | 41961ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 8698ms | 13227ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 8721ms | 13125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 36979ms | 44198ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 61.0 | app1 | ok | 8628ms | 12656ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 61.0 | app2 | ok | 8711ms | 12889ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 61.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app1 | ok | 8419ms | 13625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app2 | ok | 8281ms | 13250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | end-users | ok | 37071ms | 44207ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app1 | ok | 8657ms | 13596ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app2 | ok | 8686ms | 13679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 8240ms | 13767ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app2 | ok | 8208ms | 13828ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 8406ms | 13519ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 8531ms | 13661ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 8280ms | 13828ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 8480ms | 14000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 8514ms | 13125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 8438ms | 13538ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 8647ms | 13350ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 8909ms | 13857ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 9111ms | 14260ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 9250ms | 14306ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 8233ms | 13295ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 8452ms | 13577ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 8409ms | 14039ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 8667ms | 14136ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 8444ms | 13844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 8552ms | 13800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 8375ms | 13926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 8545ms | 14100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 8435ms | 14026ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 8800ms | 14159ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 8371ms | 12917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 8459ms | 13075ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 8381ms | 10250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 8523ms | 11250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 8500ms | 12357ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 8689ms | 12656ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 9649ms | 14365ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 9875ms | 14464ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 9469ms | 14330ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 9600ms | 14393ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 8906ms | 14014ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 8941ms | 13937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 28763ms | 43266ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 312.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 312.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 312.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 536.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 536.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 536.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
