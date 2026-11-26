# Fairness benchmark: app1-flood-moderate (uni310-l2-r1-uni161-app1-flood-128)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 31.4 points

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-flood-moderate` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-85c4448547-467rc` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T03:06:08Z` |
| Run end | `2026-11-26T03:10:36Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 28 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/28 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 94.50 | 2.9531 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 30.0 | 128 | 1827 | 200=1827 | 17.7 | 20.6 | 2368560.0 | 30.0% | 57.1% | 27.1 | 33.2% | 3.2 | 33.8% | 3.8 | 72.2s | 98.9% | 1827.0 |
| app2 | 10.0 | 32 | 598 | 200=598 | 13.4 | 16.0 | 788588.0 | 10.0% | 14.3% | 4.3 | 11.1% | 1.1 | 11.1% | 1.1 | 72.2s | 98.9% | 598.0 |
| end-users | 60.0 | 64 | 2974 | 200=2974 | 4.8 | 8.0 | 3967894.0 | 60.0% | 28.6% | -31.4 | 55.7% | -4.3 | 55.1% | -4.9 | 69.0s | 98.9% | 2974.0 |
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
| 0.0 | 211.0 | 211.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 8124.0 | 30.0% | 15.0% | -15.0 |
| 0.0 | 10.0 | app2 | True | False | 2704.0 | 10.0% | 5.0% | -5.0 |
| 0.0 | 10.0 | end-users | True | False | 43268.0 | 60.0% | 80.0% | 20.0 |
| 10.0 | 20.0 | app1 | True | False | 52782.0 | 30.0% | 18.6% | -11.4 |
| 10.0 | 20.0 | app2 | True | False | 27092.0 | 10.0% | 9.5% | -0.5 |
| 10.0 | 20.0 | end-users | True | False | 204160.0 | 60.0% | 71.9% | 11.9 |
| 20.0 | 30.0 | app1 | True | False | 95966.0 | 30.0% | 31.3% | 1.3 |
| 20.0 | 30.0 | app2 | True | False | 29714.0 | 10.0% | 9.7% | -0.3 |
| 20.0 | 30.0 | end-users | True | False | 181188.0 | 60.0% | 59.0% | -1.0 |
| 30.0 | 40.0 | app1 | True | False | 87944.0 | 30.0% | 28.4% | -1.6 |
| 30.0 | 40.0 | app2 | True | False | 28412.0 | 10.0% | 9.2% | -0.8 |
| 30.0 | 40.0 | end-users | True | False | 193412.0 | 60.0% | 62.4% | 2.4 |
| 40.0 | 50.0 | app1 | True | False | 100120.0 | 30.0% | 32.6% | 2.6 |
| 40.0 | 50.0 | app2 | True | False | 33802.0 | 10.0% | 11.0% | 1.0 |
| 40.0 | 50.0 | end-users | True | False | 173104.0 | 60.0% | 56.4% | -3.6 |
| 50.0 | 61.0 | app1 | True | False | 92006.0 | 30.0% | 30.0% | -0.0 |
| 50.0 | 61.0 | app2 | True | False | 28408.0 | 10.0% | 9.3% | -0.7 |
| 50.0 | 61.0 | end-users | True | False | 186518.0 | 60.0% | 60.8% | 0.8 |
| 61.0 | 71.0 | app1 | True | False | 89262.0 | 30.0% | 29.1% | -0.9 |
| 61.0 | 71.0 | app2 | True | False | 29750.0 | 10.0% | 9.7% | -0.3 |
| 61.0 | 71.0 | end-users | True | False | 188030.0 | 60.0% | 61.2% | 1.2 |
| 71.0 | 81.0 | app1 | True | False | 90660.0 | 30.0% | 29.7% | -0.3 |
| 71.0 | 81.0 | app2 | True | False | 32498.0 | 10.0% | 10.6% | 0.6 |
| 71.0 | 81.0 | end-users | True | False | 182490.0 | 60.0% | 59.7% | -0.3 |
| 81.0 | 91.0 | app1 | True | False | 89236.0 | 30.0% | 29.7% | -0.3 |
| 81.0 | 91.0 | app2 | True | False | 31110.0 | 10.0% | 10.4% | 0.4 |
| 81.0 | 91.0 | end-users | True | False | 180008.0 | 60.0% | 59.9% | -0.1 |
| 91.0 | 101.0 | app1 | True | False | 104082.0 | 30.0% | 33.8% | 3.8 |
| 91.0 | 101.0 | app2 | True | False | 32466.0 | 10.0% | 10.5% | 0.5 |
| 91.0 | 101.0 | end-users | True | False | 171820.0 | 60.0% | 55.7% | -4.3 |
| 101.0 | 111.0 | app1 | True | False | 90494.0 | 30.0% | 29.7% | -0.3 |
| 101.0 | 111.0 | app2 | True | False | 29698.0 | 10.0% | 9.8% | -0.2 |
| 101.0 | 111.0 | end-users | True | False | 184142.0 | 60.0% | 60.5% | 0.5 |
| 111.0 | 121.0 | app1 | True | False | 112316.0 | 30.0% | 40.9% | 10.9 |
| 111.0 | 121.0 | app2 | True | False | 39080.0 | 10.0% | 14.2% | 4.2 |
| 111.0 | 121.0 | end-users | True | False | 123000.0 | 60.0% | 44.8% | -15.2 |
| 121.0 | 131.0 | app1 | True | False | 96024.0 | 30.0% | 31.5% | 1.5 |
| 121.0 | 131.0 | app2 | True | False | 32518.0 | 10.0% | 10.7% | 0.7 |
| 121.0 | 131.0 | end-users | True | False | 175862.0 | 60.0% | 57.8% | -2.2 |
| 131.0 | 141.0 | app1 | True | False | 87798.0 | 30.0% | 38.7% | 8.7 |
| 131.0 | 141.0 | app2 | True | False | 29798.0 | 10.0% | 13.1% | 3.1 |
| 131.0 | 141.0 | end-users | True | False | 109468.0 | 60.0% | 48.2% | -11.8 |
| 141.0 | 151.0 | app1 | True | False | 108326.0 | 30.0% | 38.7% | 8.7 |
| 141.0 | 151.0 | app2 | True | False | 37852.0 | 10.0% | 13.5% | 3.5 |
| 141.0 | 151.0 | end-users | True | False | 133854.0 | 60.0% | 47.8% | -12.2 |
| 151.0 | 161.0 | app1 | True | False | 93248.0 | 30.0% | 30.4% | 0.4 |
| 151.0 | 161.0 | app2 | True | False | 28400.0 | 10.0% | 9.3% | -0.7 |
| 151.0 | 161.0 | end-users | True | False | 185288.0 | 60.0% | 60.4% | 0.4 |
| 161.0 | 171.0 | app1 | True | False | 105326.0 | 30.0% | 46.4% | 16.4 |
| 161.0 | 171.0 | app2 | True | False | 35142.0 | 10.0% | 15.5% | 5.5 |
| 161.0 | 171.0 | end-users | True | False | 86546.0 | 60.0% | 38.1% | -21.9 |
| 171.0 | 181.0 | app1 | True | False | 127240.0 | 30.0% | 45.9% | 15.9 |
| 171.0 | 181.0 | app2 | True | False | 35124.0 | 10.0% | 12.7% | 2.7 |
| 171.0 | 181.0 | end-users | True | False | 114984.0 | 60.0% | 41.5% | -18.5 |
| 181.0 | 191.0 | app1 | True | False | 79860.0 | 30.0% | 26.0% | -4.0 |
| 181.0 | 191.0 | app2 | True | False | 33832.0 | 10.0% | 11.0% | 1.0 |
| 181.0 | 191.0 | end-users | True | False | 193190.0 | 60.0% | 63.0% | 3.0 |
| 191.0 | 201.0 | app1 | True | False | 96074.0 | 30.0% | 31.4% | 1.4 |
| 191.0 | 201.0 | app2 | True | False | 32518.0 | 10.0% | 10.6% | 0.6 |
| 191.0 | 201.0 | end-users | True | False | 177224.0 | 60.0% | 58.0% | -2.0 |
| 201.0 | 211.0 | app1 | True | False | 115052.0 | 30.0% | 40.3% | 10.3 |
| 201.0 | 211.0 | app2 | True | False | 37938.0 | 10.0% | 13.3% | 3.3 |
| 201.0 | 211.0 | end-users | True | False | 132580.0 | 60.0% | 46.4% | -13.6 |
| 211.0 | 221.0 | app1 | True | False | 94708.0 | 30.0% | 31.4% | 1.4 |
| 211.0 | 221.0 | app2 | True | False | 31148.0 | 10.0% | 10.3% | 0.3 |
| 211.0 | 221.0 | end-users | True | False | 175796.0 | 60.0% | 58.3% | -1.7 |
| 221.0 | 231.0 | app1 | True | False | 78466.0 | 30.0% | 25.2% | -4.8 |
| 221.0 | 231.0 | app2 | True | False | 24374.0 | 10.0% | 7.8% | -2.2 |
| 221.0 | 231.0 | end-users | True | False | 208104.0 | 60.0% | 66.9% | 6.9 |
| 231.0 | 241.0 | app1 | True | False | 98778.0 | 30.0% | 32.6% | 2.6 |
| 231.0 | 241.0 | app2 | True | False | 32504.0 | 10.0% | 10.7% | 0.7 |
| 231.0 | 241.0 | end-users | True | False | 171866.0 | 60.0% | 56.7% | -3.3 |
| 241.0 | 251.0 | app1 | False | n/a | 129994.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 44612.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 91992.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 44674.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 8094.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 268.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 268.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 268.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 113 | 0ms | 897ms | 990ms |
| 0.0 | 10.0 | app2 | ok | 36 | 500ms | 900ms | 990ms |
| 0.0 | 10.0 | end-users | ok | 82 | 150ms | 859ms | 986ms |
| 10.0 | 20.0 | app1 | ok | 43 | 11304ms | 26261ms | 29626ms |
| 10.0 | 20.0 | app2 | ok | 17 | 7344ms | 9469ms | 9947ms |
| 10.0 | 20.0 | end-users | ok | 164 | 1665ms | 3959ms | 4957ms |
| 20.0 | 30.0 | app1 | ok | 65 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app2 | ok | 21 | 7917ms | 16000ms | 28600ms |
| 20.0 | 30.0 | end-users | ok | 161 | 1331ms | 2369ms | 4497ms |
| 30.0 | 40.0 | app1 | ok | 72 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | app2 | ok | 24 | 7500ms | 9500ms | 9950ms |
| 30.0 | 40.0 | end-users | ok | 135 | 1132ms | 2226ms | 2473ms |
| 40.0 | 50.0 | app1 | ok | 83 | 17971ms | 27594ms | 29759ms |
| 40.0 | 50.0 | app2 | ok | 28 | 7308ms | 9462ms | 9946ms |
| 40.0 | 50.0 | end-users | ok | 137 | 1375ms | 2377ms | 4511ms |
| 50.0 | 61.0 | app1 | ok | 51 | 18667ms | 27733ms | 29773ms |
| 50.0 | 61.0 | app2 | ok | 17 | 7344ms | 9469ms | 9947ms |
| 50.0 | 61.0 | end-users | ok | 128 | 1527ms | 3000ms | 4800ms |
| 61.0 | 71.0 | app1 | ok | 69 | 16200ms | 27240ms | 29724ms |
| 61.0 | 71.0 | app2 | ok | 23 | 7125ms | 9425ms | 9942ms |
| 61.0 | 71.0 | end-users | ok | 130 | 1542ms | 3289ms | 4829ms |
| 71.0 | 81.0 | app1 | ok | 56 | 20000ms | 28000ms | 29800ms |
| 71.0 | 81.0 | app2 | ok | 18 | 7500ms | 9500ms | 9950ms |
| 71.0 | 81.0 | end-users | ok | 139 | 1270ms | 2382ms | 4566ms |
| 81.0 | 91.0 | app1 | ok | 70 | 19552ms | 27910ms | 29791ms |
| 81.0 | 91.0 | app2 | ok | 24 | 7391ms | 9478ms | 9948ms |
| 81.0 | 91.0 | end-users | ok | 141 | 1207ms | 2320ms | 4295ms |
| 91.0 | 101.0 | app1 | ok | 83 | 19494ms | 27899ms | 29790ms |
| 91.0 | 101.0 | app2 | ok | 28 | 7407ms | 9481ms | 9948ms |
| 91.0 | 101.0 | end-users | ok | 140 | 1308ms | 2459ms | 4708ms |
| 101.0 | 111.0 | app1 | ok | 64 | 9571ms | 25586ms | 29559ms |
| 101.0 | 111.0 | app2 | ok | 21 | 5962ms | 9192ms | 9919ms |
| 101.0 | 111.0 | end-users | ok | 127 | 1254ms | 2483ms | 4735ms |
| 111.0 | 121.0 | app1 | ok | 86 | 8125ms | 23120ms | 29312ms |
| 111.0 | 121.0 | app2 | ok | 28 | 5882ms | 9176ms | 9918ms |
| 111.0 | 121.0 | end-users | ok | 88 | 3472ms | 8000ms | 9800ms |
| 121.0 | 131.0 | app1 | ok | 98 | 9362ms | 25442ms | 29544ms |
| 121.0 | 131.0 | app2 | ok | 31 | 5921ms | 9184ms | 9918ms |
| 121.0 | 131.0 | end-users | ok | 108 | 1132ms | 2268ms | 3650ms |
| 131.0 | 141.0 | app1 | ok | 73 | 6570ms | 9965ms | 27914ms |
| 131.0 | 141.0 | app2 | ok | 16 | 5556ms | 9111ms | 9911ms |
| 131.0 | 141.0 | end-users | ok | 64 | 5152ms | 9030ms | 9903ms |
| 141.0 | 151.0 | app1 | ok | 45 | 7583ms | 18750ms | 28875ms |
| 141.0 | 151.0 | app2 | ok | 26 | 5000ms | 9000ms | 9900ms |
| 141.0 | 151.0 | end-users | ok | 143 | 2841ms | 7021ms | 9702ms |
| 151.0 | 161.0 | app1 | ok | 135 | 8929ms | 25500ms | 29550ms |
| 151.0 | 161.0 | app2 | ok | 34 | 5278ms | 9056ms | 9906ms |
| 151.0 | 161.0 | end-users | ok | 118 | 1363ms | 2542ms | 4754ms |
| 161.0 | 171.0 | app1 | ok | 67 | 4191ms | 8804ms | 9880ms |
| 161.0 | 171.0 | app2 | ok | 22 | 4000ms | 8778ms | 9878ms |
| 161.0 | 171.0 | end-users | ok | 64 | 7241ms | 9448ms | 9945ms |
| 171.0 | 181.0 | app1 | ok | 43 | 6641ms | 9328ms | 9933ms |
| 171.0 | 181.0 | app2 | ok | 25 | 3542ms | 8611ms | 9861ms |
| 171.0 | 181.0 | end-users | ok | 115 | 3449ms | 7604ms | 9760ms |
| 181.0 | 191.0 | app1 | ok | 41 | 14815ms | 26963ms | 29696ms |
| 181.0 | 191.0 | app2 | ok | 14 | 7500ms | 9500ms | 9950ms |
| 181.0 | 191.0 | end-users | ok | 122 | 1287ms | 2363ms | 4492ms |
| 191.0 | 201.0 | app1 | ok | 77 | 20000ms | 28000ms | 29800ms |
| 191.0 | 201.0 | app2 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 191.0 | 201.0 | end-users | ok | 126 | 1000ms | 2239ms | 3425ms |
| 201.0 | 211.0 | app1 | ok | 84 | 7766ms | 22000ms | 29200ms |
| 201.0 | 211.0 | app2 | ok | 28 | 4643ms | 8923ms | 9892ms |
| 201.0 | 211.0 | end-users | ok | 95 | 3138ms | 5682ms | 9568ms |
| 211.0 | 221.0 | app1 | ok | 82 | 12553ms | 26511ms | 29651ms |
| 211.0 | 221.0 | app2 | ok | 28 | 6500ms | 9300ms | 9930ms |
| 211.0 | 221.0 | end-users | ok | 160 | 1696ms | 3857ms | 4886ms |
| 221.0 | 231.0 | app1 | ok | 49 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app2 | ok | 17 | 7500ms | 9500ms | 9950ms |
| 221.0 | 231.0 | end-users | ok | 119 | 1230ms | 2381ms | 4575ms |
| 231.0 | 241.0 | app1 | ok | 82 | 18767ms | 27753ms | 29775ms |
| 231.0 | 241.0 | app2 | ok | 26 | 7400ms | 9480ms | 9948ms |
| 231.0 | 241.0 | end-users | ok | 141 | 1337ms | 2421ms | 4648ms |
| 241.0 | 251.0 | app1 | ok | 96 | 8250ms | 22889ms | 29289ms |
| 241.0 | 251.0 | app2 | ok | 21 | 5625ms | 9125ms | 9912ms |
| 241.0 | 251.0 | end-users | ok | 27 | 1829ms | 3650ms | 4865ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 268.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 268.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 268.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2247210 | 111994 | 2359204.0 | 0.0% | 2368560.0 | 2471198.0 | -4.2% | True |
| app2 | 735540 | 36666 | 772206.0 | 0.0% | 788588.0 | 808872.0 | -2.5% | True |
| end-users | 3658020 | 182014 | 3840034.0 | 0.0% | 3967894.0 | 4022048.0 | -1.3% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1827 | 0 | 0 | 0 (never shed) | 0.00% | 30.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 598 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2974 | 0 | 0 | 0 (never shed) | 0.00% | 60.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5399). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5399 | 0.051ms | 0.102ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 254303 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1827 | 17367ms | 24925ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 598 | 12820ms | 18474ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 2974 | 4809ms | 7943ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5399 | 7078ms | 19698ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (27 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 3400ms | 5167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2500ms | 4675ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2233ms | 4665ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 8583ms | 14515ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 7778ms | 14250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 4333ms | 7647ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 17958ms | 26773ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 16765ms | 19676ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 4283ms | 5853ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 22614ms | 29261ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 15227ms | 19523ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 4593ms | 5868ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 17643ms | 20750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 12841ms | 17917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 4625ms | 5884ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 61.0 | app1 | ok | 17576ms | 19894ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 61.0 | app2 | ok | 12763ms | 17375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 61.0 | end-users | ok | 4622ms | 6275ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app1 | ok | 17750ms | 24500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app2 | ok | 13056ms | 18625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | end-users | ok | 4616ms | 5855ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app1 | ok | 18284ms | 27906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app2 | ok | 13750ms | 19250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | end-users | ok | 4432ms | 7206ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 17538ms | 19823ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app2 | ok | 12614ms | 14966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 4727ms | 5855ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 18056ms | 27250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 13158ms | 18800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 4491ms | 5898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 18098ms | 27906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 13000ms | 18900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 5280ms | 7728ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 17782ms | 27036ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 13021ms | 18550ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 5500ms | 7776ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 4853ms | 8375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 14583ms | 19450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 8093ms | 9809ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 16970ms | 19697ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 6698ms | 8889ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 12625ms | 14988ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 4616ms | 5868ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 12708ms | 16750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 8000ms | 12333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 15804ms | 19580ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 7667ms | 14336ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 15391ms | 19539ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 12159ms | 14716ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 4777ms | 6856ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 17731ms | 24083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 12609ms | 14957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 5015ms | 7591ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 17911ms | 26458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 12692ms | 16500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 5594ms | 7770ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 17177ms | 19718ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 12386ms | 14739ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 5083ms | 7962ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 18085ms | 27364ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 13462ms | 19100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 3939ms | 6075ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 18093ms | 27393ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 15000ms | 19500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 4845ms | 7577ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 16364ms | 23667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 12596ms | 17937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 5133ms | 7150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 15658ms | 19566ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 12000ms | 14700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 268.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 268.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 268.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
