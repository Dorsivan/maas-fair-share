# Fairness benchmark: app1-flood-3x (uni-247-3x-rep2)

**Verdict: FAIL** (threshold: 10 points)
**Secondary (priority) verdict: PRIORITY-OK** -- see "Per-tenant TTFT / ITL and the priority verdict (UNI-226)" below for detail.
Worker-share vs. weight-share gap (UNI-225): 26.7 points

- end-users deviated -10.5 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-flood-3x` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:c8a088203f6dc6c48c158d21b6295172a78f18646b06c334e5310a0caedb259f` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-6988b67749-dfcwc` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-12T09:47:01Z` |
| Run end | `2026-11-12T09:51:25Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 28 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/28 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 78.00 | 2.4375 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 30.0 | 96 | 2047 | 200=2047 | 11.8 | 14.2 | 2684160.0 | 30.0% | 50.0% | 20.0 | 37.9% | 7.9 | 38.1% | 8.1 | 66.4s | 98.9% | 2047.0 |
| app2 | 10.0 | 32 | 684 | 200=684 | 11.8 | 14.1 | 895338.0 | 10.0% | 16.7% | 6.7 | 12.6% | 2.6 | 12.7% | 2.7 | 66.4s | 98.9% | 684.0 |
| end-users | 60.0 | 64 | 2647 | 200=2647 | 5.5 | 9.1 | 3508964.0 | 60.0% | 33.3% | -26.7 | 49.5% | -10.5 | 49.2% | -10.8 | 62.9s | 98.9% | 2647.0 |
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
| 0.0 | 221.0 | 221.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 0.0 | 10.0 | end-users | True | 22976.0 | 60.0% | 100.0% | 40.0 |
| 10.0 | 20.0 | app1 | True | 90702.0 | 30.0% | 32.7% | 2.7 |
| 10.0 | 20.0 | app2 | True | 29748.0 | 10.0% | 10.7% | 0.7 |
| 10.0 | 20.0 | end-users | True | 156726.0 | 60.0% | 56.5% | -3.5 |
| 20.0 | 30.0 | app1 | True | 93318.0 | 30.0% | 36.7% | 6.7 |
| 20.0 | 30.0 | app2 | True | 29774.0 | 10.0% | 11.7% | 1.7 |
| 20.0 | 30.0 | end-users | True | 131136.0 | 60.0% | 51.6% | -8.4 |
| 30.0 | 40.0 | app1 | True | 118992.0 | 30.0% | 38.1% | 8.1 |
| 30.0 | 40.0 | app2 | True | 40600.0 | 10.0% | 13.0% | 3.0 |
| 30.0 | 40.0 | end-users | True | 152758.0 | 60.0% | 48.9% | -11.1 |
| 40.0 | 50.0 | app1 | True | 101302.0 | 30.0% | 36.2% | 6.2 |
| 40.0 | 50.0 | app2 | True | 35196.0 | 10.0% | 12.6% | 2.6 |
| 40.0 | 50.0 | end-users | True | 143246.0 | 60.0% | 51.2% | -8.8 |
| 50.0 | 60.0 | app1 | True | 112220.0 | 30.0% | 36.7% | 6.7 |
| 50.0 | 60.0 | app2 | True | 37926.0 | 10.0% | 12.4% | 2.4 |
| 50.0 | 60.0 | end-users | True | 155626.0 | 60.0% | 50.9% | -9.1 |
| 60.0 | 70.0 | app1 | True | 87892.0 | 30.0% | 32.0% | 2.0 |
| 60.0 | 70.0 | app2 | True | 28400.0 | 10.0% | 10.3% | 0.3 |
| 60.0 | 70.0 | end-users | True | 158244.0 | 60.0% | 57.6% | -2.4 |
| 70.0 | 81.0 | app1 | True | 110840.0 | 30.0% | 40.6% | 10.6 |
| 70.0 | 81.0 | app2 | True | 35208.0 | 10.0% | 12.9% | 2.9 |
| 70.0 | 81.0 | end-users | True | 127178.0 | 60.0% | 46.5% | -13.5 |
| 81.0 | 91.0 | app1 | True | 91938.0 | 30.0% | 29.7% | -0.3 |
| 81.0 | 91.0 | app2 | True | 33768.0 | 10.0% | 10.9% | 0.9 |
| 81.0 | 91.0 | end-users | True | 183920.0 | 60.0% | 59.4% | -0.6 |
| 91.0 | 101.0 | app1 | True | 115044.0 | 30.0% | 37.8% | 7.8 |
| 91.0 | 101.0 | app2 | True | 36524.0 | 10.0% | 12.0% | 2.0 |
| 91.0 | 101.0 | end-users | True | 152758.0 | 60.0% | 50.2% | -9.8 |
| 101.0 | 111.0 | app1 | True | 120564.0 | 30.0% | 39.4% | 9.4 |
| 101.0 | 111.0 | app2 | True | 40502.0 | 10.0% | 13.2% | 3.2 |
| 101.0 | 111.0 | end-users | True | 144706.0 | 60.0% | 47.3% | -12.7 |
| 111.0 | 121.0 | app1 | True | 95968.0 | 30.0% | 31.4% | 1.4 |
| 111.0 | 121.0 | app2 | True | 31106.0 | 10.0% | 10.2% | 0.2 |
| 111.0 | 121.0 | end-users | True | 178544.0 | 60.0% | 58.4% | -1.6 |
| 121.0 | 131.0 | app1 | True | 97136.0 | 30.0% | 35.6% | 5.6 |
| 121.0 | 131.0 | app2 | True | 33760.0 | 10.0% | 12.4% | 2.4 |
| 121.0 | 131.0 | end-users | True | 142050.0 | 60.0% | 52.0% | -8.0 |
| 131.0 | 141.0 | app1 | True | 113670.0 | 30.0% | 38.2% | 8.2 |
| 131.0 | 141.0 | app2 | True | 36454.0 | 10.0% | 12.3% | 2.3 |
| 131.0 | 141.0 | end-users | True | 147388.0 | 60.0% | 49.5% | -10.5 |
| 141.0 | 151.0 | app1 | True | 161046.0 | 30.0% | 53.6% | 23.6 |
| 141.0 | 151.0 | app2 | True | 52734.0 | 10.0% | 17.6% | 7.6 |
| 141.0 | 151.0 | end-users | True | 86526.0 | 60.0% | 28.8% | -31.2 |
| 151.0 | 161.0 | app1 | True | 109542.0 | 30.0% | 37.9% | 7.9 |
| 151.0 | 161.0 | app2 | True | 37778.0 | 10.0% | 13.1% | 3.1 |
| 151.0 | 161.0 | end-users | True | 141990.0 | 60.0% | 49.1% | -10.9 |
| 161.0 | 171.0 | app1 | True | 108252.0 | 30.0% | 36.5% | 6.5 |
| 161.0 | 171.0 | app2 | True | 36554.0 | 10.0% | 12.3% | 2.3 |
| 161.0 | 171.0 | end-users | True | 151664.0 | 60.0% | 51.2% | -8.8 |
| 171.0 | 181.0 | app1 | True | 87936.0 | 30.0% | 28.3% | -1.7 |
| 171.0 | 181.0 | app2 | True | 31160.0 | 10.0% | 10.0% | 0.0 |
| 171.0 | 181.0 | end-users | True | 192028.0 | 60.0% | 61.7% | 1.7 |
| 181.0 | 191.0 | app1 | True | 198538.0 | 30.0% | 65.0% | 35.0 |
| 181.0 | 191.0 | app2 | True | 59512.0 | 10.0% | 19.5% | 9.5 |
| 181.0 | 191.0 | end-users | True | 47298.0 | 60.0% | 15.5% | -44.5 |
| 191.0 | 201.0 | app1 | True | 89210.0 | 30.0% | 30.3% | 0.3 |
| 191.0 | 201.0 | app2 | True | 33830.0 | 10.0% | 11.5% | 1.5 |
| 191.0 | 201.0 | end-users | True | 171608.0 | 60.0% | 58.2% | -1.8 |
| 201.0 | 211.0 | app1 | True | 125804.0 | 30.0% | 40.5% | 10.5 |
| 201.0 | 211.0 | app2 | True | 41858.0 | 10.0% | 13.5% | 3.5 |
| 201.0 | 211.0 | end-users | True | 143166.0 | 60.0% | 46.1% | -13.9 |
| 211.0 | 221.0 | app1 | True | 117560.0 | 30.0% | 38.5% | 8.5 |
| 211.0 | 221.0 | app2 | True | 40646.0 | 10.0% | 13.3% | 3.3 |
| 211.0 | 221.0 | end-users | True | 147400.0 | 60.0% | 48.2% | -11.8 |
| 221.0 | 231.0 | app1 | True | 105514.0 | 30.0% | 34.8% | 4.8 |
| 221.0 | 231.0 | app2 | True | 35120.0 | 10.0% | 11.6% | 1.6 |
| 221.0 | 231.0 | end-users | True | 162266.0 | 60.0% | 53.6% | -6.4 |
| 231.0 | 241.0 | app1 | True | 90498.0 | 30.0% | 30.0% | 0.0 |
| 231.0 | 241.0 | app2 | True | 29784.0 | 10.0% | 9.9% | -0.1 |
| 231.0 | 241.0 | end-users | True | 181262.0 | 60.0% | 60.1% | 0.1 |
| 241.0 | 251.0 | app1 | False | 140674.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 47396.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 86500.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 264.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 264.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 264.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 114 | 0ms | 4109ms | 4911ms |
| 0.0 | 10.0 | app2 | ok | 39 | 0ms | 4114ms | 4911ms |
| 0.0 | 10.0 | end-users | ok | 117 | 346ms | 1961ms | 3537ms |
| 10.0 | 20.0 | app1 | ok | 48 | 7500ms | 9500ms | 9950ms |
| 10.0 | 20.0 | app2 | ok | 15 | 7500ms | 9500ms | 9950ms |
| 10.0 | 20.0 | end-users | ok | 100 | 1481ms | 3214ms | 4821ms |
| 20.0 | 30.0 | app1 | ok | 107 | 3872ms | 8471ms | 9847ms |
| 20.0 | 30.0 | app2 | ok | 36 | 3667ms | 8200ms | 9820ms |
| 20.0 | 30.0 | end-users | ok | 97 | 2566ms | 8383ms | 9838ms |
| 30.0 | 40.0 | app1 | ok | 96 | 4207ms | 8629ms | 9863ms |
| 30.0 | 40.0 | app2 | ok | 32 | 4231ms | 8667ms | 9867ms |
| 30.0 | 40.0 | end-users | ok | 122 | 1663ms | 4047ms | 4905ms |
| 40.0 | 50.0 | app1 | ok | 52 | 3500ms | 8143ms | 9814ms |
| 40.0 | 50.0 | app2 | ok | 17 | 3393ms | 7875ms | 9787ms |
| 40.0 | 50.0 | end-users | ok | 114 | 3182ms | 4909ms | 9367ms |
| 50.0 | 60.0 | app1 | ok | 87 | 6250ms | 9250ms | 9925ms |
| 50.0 | 60.0 | app2 | ok | 29 | 6184ms | 9237ms | 9924ms |
| 50.0 | 60.0 | end-users | ok | 100 | 1312ms | 2917ms | 4792ms |
| 60.0 | 70.0 | app1 | ok | 64 | 5000ms | 9000ms | 9900ms |
| 60.0 | 70.0 | app2 | ok | 22 | 4643ms | 8900ms | 9890ms |
| 60.0 | 70.0 | end-users | ok | 89 | 1701ms | 3888ms | 4889ms |
| 70.0 | 81.0 | app1 | ok | 68 | 6222ms | 9244ms | 9924ms |
| 70.0 | 81.0 | app2 | ok | 22 | 6765ms | 9353ms | 9935ms |
| 70.0 | 81.0 | end-users | ok | 137 | 2633ms | 7146ms | 9715ms |
| 81.0 | 91.0 | app1 | ok | 73 | 7316ms | 9463ms | 9946ms |
| 81.0 | 91.0 | app2 | ok | 25 | 7396ms | 9479ms | 9948ms |
| 81.0 | 91.0 | end-users | ok | 142 | 1274ms | 2313ms | 4113ms |
| 91.0 | 101.0 | app1 | ok | 101 | 7098ms | 9420ms | 9942ms |
| 91.0 | 101.0 | app2 | ok | 33 | 7155ms | 9431ms | 9943ms |
| 91.0 | 101.0 | end-users | ok | 114 | 1269ms | 2290ms | 3575ms |
| 101.0 | 111.0 | app1 | ok | 57 | 7361ms | 9472ms | 9947ms |
| 101.0 | 111.0 | app2 | ok | 18 | 7353ms | 9471ms | 9947ms |
| 101.0 | 111.0 | end-users | ok | 102 | 1580ms | 3938ms | 4894ms |
| 111.0 | 121.0 | app1 | ok | 91 | 5708ms | 9142ms | 9914ms |
| 111.0 | 121.0 | app2 | ok | 32 | 6000ms | 9200ms | 9920ms |
| 111.0 | 121.0 | end-users | ok | 106 | 1000ms | 2247ms | 3675ms |
| 121.0 | 131.0 | app1 | ok | 84 | 4535ms | 8765ms | 9876ms |
| 121.0 | 131.0 | app2 | ok | 28 | 4464ms | 8727ms | 9873ms |
| 121.0 | 131.0 | end-users | ok | 141 | 2144ms | 4712ms | 9119ms |
| 131.0 | 141.0 | app1 | ok | 92 | 2685ms | 7810ms | 9781ms |
| 131.0 | 141.0 | app2 | ok | 31 | 2432ms | 7786ms | 9779ms |
| 131.0 | 141.0 | end-users | ok | 52 | 2059ms | 4694ms | 9133ms |
| 141.0 | 151.0 | app1 | ok | 97 | 3365ms | 4858ms | 9192ms |
| 141.0 | 151.0 | app2 | ok | 32 | 3289ms | 4974ms | 9467ms |
| 141.0 | 151.0 | end-users | ok | 83 | 6422ms | 9284ms | 9928ms |
| 151.0 | 161.0 | app1 | ok | 79 | 4440ms | 8803ms | 9880ms |
| 151.0 | 161.0 | app2 | ok | 27 | 4062ms | 8500ms | 9850ms |
| 151.0 | 161.0 | end-users | ok | 144 | 2059ms | 4368ms | 4937ms |
| 161.0 | 171.0 | app1 | ok | 72 | 6727ms | 9345ms | 9935ms |
| 161.0 | 171.0 | app2 | ok | 25 | 6324ms | 9265ms | 9926ms |
| 161.0 | 171.0 | end-users | ok | 90 | 1616ms | 3125ms | 4812ms |
| 171.0 | 181.0 | app1 | ok | 100 | 5283ms | 9057ms | 9906ms |
| 171.0 | 181.0 | app2 | ok | 31 | 5441ms | 9088ms | 9909ms |
| 171.0 | 181.0 | end-users | ok | 101 | 1434ms | 2497ms | 4747ms |
| 181.0 | 191.0 | app1 | ok | 134 | 2080ms | 4368ms | 4937ms |
| 181.0 | 191.0 | app2 | ok | 46 | 1978ms | 4233ms | 4923ms |
| 181.0 | 191.0 | end-users | ok | 76 | 5476ms | 9095ms | 9910ms |
| 191.0 | 201.0 | app1 | ok | 55 | 7011ms | 9402ms | 9940ms |
| 191.0 | 201.0 | app2 | ok | 18 | 6538ms | 9308ms | 9931ms |
| 191.0 | 201.0 | end-users | ok | 128 | 1676ms | 4111ms | 4911ms |
| 201.0 | 211.0 | app1 | ok | 79 | 6274ms | 9255ms | 9925ms |
| 201.0 | 211.0 | app2 | ok | 26 | 6176ms | 9235ms | 9924ms |
| 201.0 | 211.0 | end-users | ok | 101 | 1496ms | 2428ms | 4639ms |
| 211.0 | 221.0 | app1 | ok | 99 | 6360ms | 9272ms | 9927ms |
| 211.0 | 221.0 | app2 | ok | 34 | 6136ms | 9227ms | 9923ms |
| 211.0 | 221.0 | end-users | ok | 129 | 1581ms | 3464ms | 4846ms |
| 221.0 | 231.0 | app1 | ok | 64 | 7091ms | 9418ms | 9942ms |
| 221.0 | 231.0 | app2 | ok | 22 | 7250ms | 9450ms | 9945ms |
| 221.0 | 231.0 | end-users | ok | 128 | 1389ms | 2337ms | 4200ms |
| 231.0 | 241.0 | app1 | ok | 90 | 6121ms | 9224ms | 9922ms |
| 231.0 | 241.0 | app2 | ok | 29 | 5972ms | 9194ms | 9919ms |
| 231.0 | 241.0 | end-users | ok | 71 | 1703ms | 4343ms | 4934ms |
| 241.0 | 251.0 | app1 | ok | 44 | 4397ms | 8533ms | 9853ms |
| 241.0 | 251.0 | app2 | ok | 15 | 4583ms | 8750ms | 9875ms |
| 241.0 | 251.0 | end-users | ok | 63 | 2928ms | 4586ms | 4959ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 264.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 264.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 264.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2517810 | 125014 | 2642824.0 | 0.0% | 2684160.0 | 2767838.0 | -3.0% | True |
| app2 | 841320 | 41909 | 883229.0 | 0.0% | 895338.0 | 925138.0 | -3.2% | True |
| end-users | 3255810 | 161732 | 3417542.0 | 0.0% | 3508964.0 | 3579274.0 | -2.0% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2047 | 0 | 0 | 0 (never shed) | 0.00% | 30.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 684 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2647 | 0 | 0 | 0 (never shed) | 0.00% | 60.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5378). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5378 | 0.052ms | 0.178ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 250072 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 2047 | 11982ms | 14730ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 684 | 12005ms | 14749ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 2647 | 5511ms | 8941ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5378 | 7748ms | 14467ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: PRIORITY-OK** -- the share verdict above is FAIL, so this is the board's second, independent success criterion (2026-11-10): did the policy nonetheless order tenants by weight? Top-weighted group: `end-users` (TTFT p50 5511ms, p95 8941ms, strictly lowest among distinctly-weighted groups: p50=True/p95=True; no rank inversion among any distinctly-weighted pair: True -- this, not raw rank correlation, is what gates the verdict, since a genuine weight tie (e.g. 98/1/1's app2==end-users) makes exact correlation 1.0 unreachable by construction even when ordering is otherwise perfect). Rank correlation 1.00 (1.00 = exact agreement, informational only) shown for reference. Separation from the next distinctly-weighted group: 6471ms against a noise floor of not given (separation check skipped).

**Windowed TTFT/ITL** (27 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2237ms | 4150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 1750ms | 3300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 3190ms | 4758ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 9765ms | 14472ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 9000ms | 14341ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 4930ms | 5925ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 5564ms | 8383ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 12471ms | 14747ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 5911ms | 7930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 12466ms | 14747ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 6161ms | 7880ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 5257ms | 7617ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 5242ms | 6830ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 81.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 81.0 | app2 | ok | 12600ms | 14940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 81.0 | end-users | ok | 6776ms | 7901ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 5240ms | 7547ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 5518ms | 7671ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 4982ms | 6240ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 4954ms | 7633ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 12604ms | 14948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 5669ms | 7673ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 5207ms | 7505ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 7158ms | 14250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 7000ms | 14304ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 12091ms | 14709ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 12065ms | 14707ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 12200ms | 14720ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 5481ms | 7970ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 5568ms | 7697ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 5240ms | 7727ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 10067ms | 14507ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 10312ms | 14531ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 11759ms | 14676ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 9840ms | 14468ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 9909ms | 14479ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 5574ms | 13897ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 12703ms | 16679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 12589ms | 16125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 5556ms | 7784ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 11106ms | 14870ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 11389ms | 16250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 5717ms | 7811ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 12466ms | 14870ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 12292ms | 14729ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 6182ms | 7818ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 4882ms | 6511ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 11438ms | 14644ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 11500ms | 14650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 6968ms | 7897ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 264.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 264.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 264.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
