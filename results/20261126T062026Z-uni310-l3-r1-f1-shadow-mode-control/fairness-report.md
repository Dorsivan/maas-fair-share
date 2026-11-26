# Fairness benchmark: shadow-mode-control (uni310-l3-r1-f1-shadow-mode-control)

**Verdict: INFO** -- named negative control, not scored against the 10-point threshold. Expected to NOT reproduce the configured weights; see docs/runbook.md.
Worker-share vs. weight-share gap (UNI-225): 6.1 points

- negative control, not scored against the 10-point threshold: max deviation was 0.0 points. This scenario is expected to compress toward equal shares, not reproduce the configured weights -- see docs/runbook.md's 'Per-tenant worker sizing and the saturation check'

## Run metadata

| field | value |
|---|---|
| Scenario | `shadow-mode-control` |
| Generator | `closed-loop` |
| Enforce | `False` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-d8bf49777-vxxs4` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T06:20:28Z` |
| Run end | `2026-11-26T06:24:46Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 27 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/27 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 65.50 | 2.0469 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1149 | 200=1149 | 6.7 | 8.5 | 1532296.0 | 21.1% | 16.7% | -4.4 | 21.1% | 0.0 | 20.9% | -0.2 | 79.5s | 98.9% | 1149.0 |
| app2 | 10.0 | 32 | 591 | 200=591 | 13.2 | 17.3 | 769708.0 | 10.5% | 16.7% | 6.1 | 10.6% | 0.0 | 10.7% | 0.2 | 79.4s | 98.9% | 591.0 |
| end-users | 65.0 | 128 | 3768 | 200=3767, 503=1 | 8.3 | 10.3 | 4976396.0 | 68.4% | 66.7% | -1.8 | 68.4% | -0.0 | 68.4% | -0.0 | 79.5s | 98.9% | 3768.0 |
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

**Windows** (26 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 24352.0 | 21.1% | 54.6% | 33.5 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | False | 20262.0 | 68.4% | 45.4% | -23.0 |
| 10.0 | 20.0 | app1 | True | False | 62184.0 | 21.1% | 20.8% | -0.2 |
| 10.0 | 20.0 | app2 | True | False | 21624.0 | 10.5% | 7.2% | -3.3 |
| 10.0 | 20.0 | end-users | True | False | 214844.0 | 68.4% | 71.9% | 3.5 |
| 20.0 | 30.0 | app1 | True | False | 66148.0 | 21.1% | 21.6% | 0.5 |
| 20.0 | 30.0 | app2 | True | False | 31126.0 | 10.5% | 10.1% | -0.4 |
| 20.0 | 30.0 | end-users | True | False | 209534.0 | 68.4% | 68.3% | -0.1 |
| 30.0 | 40.0 | app1 | True | False | 59560.0 | 21.1% | 19.3% | -1.7 |
| 30.0 | 40.0 | app2 | True | False | 32458.0 | 10.5% | 10.5% | -0.0 |
| 30.0 | 40.0 | end-users | True | False | 216414.0 | 68.4% | 70.2% | 1.7 |
| 40.0 | 50.0 | app1 | True | False | 74424.0 | 21.1% | 24.6% | 3.5 |
| 40.0 | 50.0 | app2 | True | False | 31134.0 | 10.5% | 10.3% | -0.2 |
| 40.0 | 50.0 | end-users | True | False | 197360.0 | 68.4% | 65.2% | -3.3 |
| 50.0 | 60.0 | app1 | True | False | 56806.0 | 21.1% | 19.0% | -2.1 |
| 50.0 | 60.0 | app2 | True | False | 33900.0 | 10.5% | 11.3% | 0.8 |
| 50.0 | 60.0 | end-users | True | False | 208246.0 | 68.4% | 69.7% | 1.2 |
| 60.0 | 70.0 | app1 | True | False | 62096.0 | 21.1% | 20.2% | -0.8 |
| 60.0 | 70.0 | app2 | True | False | 31144.0 | 10.5% | 10.1% | -0.4 |
| 60.0 | 70.0 | end-users | True | False | 213692.0 | 68.4% | 69.6% | 1.2 |
| 70.0 | 80.0 | app1 | True | False | 64956.0 | 21.1% | 21.3% | 0.3 |
| 70.0 | 80.0 | app2 | True | False | 32462.0 | 10.5% | 10.7% | 0.1 |
| 70.0 | 80.0 | end-users | True | False | 206952.0 | 68.4% | 68.0% | -0.4 |
| 80.0 | 90.0 | app1 | True | False | 64980.0 | 21.1% | 21.5% | 0.4 |
| 80.0 | 90.0 | app2 | True | False | 33828.0 | 10.5% | 11.2% | 0.6 |
| 80.0 | 90.0 | end-users | True | False | 204128.0 | 68.4% | 67.4% | -1.0 |
| 90.0 | 100.0 | app1 | True | False | 60890.0 | 21.1% | 20.1% | -1.0 |
| 90.0 | 100.0 | app2 | True | False | 32342.0 | 10.5% | 10.7% | 0.2 |
| 90.0 | 100.0 | end-users | True | False | 209670.0 | 68.4% | 69.2% | 0.8 |
| 100.0 | 110.0 | app1 | True | False | 67582.0 | 21.1% | 22.0% | 1.0 |
| 100.0 | 110.0 | app2 | True | False | 28320.0 | 10.5% | 9.2% | -1.3 |
| 100.0 | 110.0 | end-users | True | False | 210954.0 | 68.4% | 68.7% | 0.3 |
| 110.0 | 120.0 | app1 | True | False | 64992.0 | 21.1% | 21.3% | 0.2 |
| 110.0 | 120.0 | app2 | True | False | 32472.0 | 10.5% | 10.6% | 0.1 |
| 110.0 | 120.0 | end-users | True | False | 207958.0 | 68.4% | 68.1% | -0.3 |
| 120.0 | 130.0 | app1 | True | False | 63464.0 | 21.1% | 20.7% | -0.4 |
| 120.0 | 130.0 | app2 | True | False | 39238.0 | 10.5% | 12.8% | 2.3 |
| 120.0 | 130.0 | end-users | True | False | 204086.0 | 68.4% | 66.5% | -1.9 |
| 130.0 | 140.0 | app1 | True | False | 56834.0 | 21.1% | 19.1% | -2.0 |
| 130.0 | 140.0 | app2 | True | False | 40650.0 | 10.5% | 13.7% | 3.1 |
| 130.0 | 140.0 | end-users | True | False | 200168.0 | 68.4% | 67.2% | -1.2 |
| 140.0 | 151.0 | app1 | True | False | 69030.0 | 21.1% | 22.8% | 1.7 |
| 140.0 | 151.0 | app2 | True | False | 20288.0 | 10.5% | 6.7% | -3.8 |
| 140.0 | 151.0 | end-users | True | False | 213464.0 | 68.4% | 70.5% | 2.1 |
| 151.0 | 161.0 | app1 | True | False | 62324.0 | 21.1% | 20.6% | -0.5 |
| 151.0 | 161.0 | app2 | True | False | 28394.0 | 10.5% | 9.4% | -1.1 |
| 151.0 | 161.0 | end-users | True | False | 212090.0 | 68.4% | 70.0% | 1.6 |
| 161.0 | 171.0 | app1 | True | False | 66270.0 | 21.1% | 21.9% | 0.8 |
| 161.0 | 171.0 | app2 | True | False | 32386.0 | 10.5% | 10.7% | 0.2 |
| 161.0 | 171.0 | end-users | True | False | 204412.0 | 68.4% | 67.4% | -1.0 |
| 171.0 | 181.0 | app1 | True | False | 59530.0 | 21.1% | 19.6% | -1.5 |
| 171.0 | 181.0 | app2 | True | False | 39144.0 | 10.5% | 12.9% | 2.3 |
| 171.0 | 181.0 | end-users | True | False | 205440.0 | 68.4% | 67.6% | -0.9 |
| 181.0 | 191.0 | app1 | True | False | 64882.0 | 21.1% | 22.1% | 1.1 |
| 181.0 | 191.0 | app2 | True | False | 24342.0 | 10.5% | 8.3% | -2.2 |
| 181.0 | 191.0 | end-users | True | False | 203874.0 | 68.4% | 69.6% | 1.1 |
| 191.0 | 201.0 | app1 | True | False | 63630.0 | 21.1% | 21.6% | 0.5 |
| 191.0 | 201.0 | app2 | True | False | 32496.0 | 10.5% | 11.0% | 0.5 |
| 191.0 | 201.0 | end-users | True | False | 198898.0 | 68.4% | 67.4% | -1.0 |
| 201.0 | 211.0 | app1 | True | False | 62188.0 | 21.1% | 21.2% | 0.1 |
| 201.0 | 211.0 | app2 | True | False | 40612.0 | 10.5% | 13.8% | 3.3 |
| 201.0 | 211.0 | end-users | True | False | 190662.0 | 68.4% | 65.0% | -3.5 |
| 211.0 | 221.0 | app1 | True | False | 63606.0 | 21.1% | 21.0% | -0.0 |
| 211.0 | 221.0 | app2 | True | False | 29698.0 | 10.5% | 9.8% | -0.7 |
| 211.0 | 221.0 | end-users | True | False | 209528.0 | 68.4% | 69.2% | 0.8 |
| 221.0 | 231.0 | app1 | True | False | 62144.0 | 21.1% | 20.5% | -0.5 |
| 221.0 | 231.0 | app2 | True | False | 21710.0 | 10.5% | 7.2% | -3.4 |
| 221.0 | 231.0 | end-users | True | False | 218944.0 | 68.4% | 72.3% | 3.9 |
| 231.0 | 241.0 | app1 | True | False | 64824.0 | 21.1% | 20.9% | -0.1 |
| 231.0 | 241.0 | app2 | True | False | 33900.0 | 10.5% | 11.0% | 0.4 |
| 231.0 | 241.0 | end-users | True | False | 210806.0 | 68.4% | 68.1% | -0.3 |
| 241.0 | 251.0 | app1 | False | n/a | 44600.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 33866.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 177244.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | False | n/a | 12174.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | end-users | False | n/a | 6766.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 40 | 1500ms | 4000ms | 4900ms |
| 0.0 | 10.0 | app2 | ok | 41 | 0ms | 3292ms | 4829ms |
| 0.0 | 10.0 | end-users | ok | 162 | 0ms | 3875ms | 4887ms |
| 10.0 | 20.0 | app1 | ok | 57 | 3681ms | 4736ms | 4974ms |
| 10.0 | 20.0 | app2 | ok | 23 | 2946ms | 4589ms | 4959ms |
| 10.0 | 20.0 | end-users | ok | 162 | 3613ms | 4723ms | 4972ms |
| 20.0 | 30.0 | app1 | ok | 57 | 3451ms | 4690ms | 4969ms |
| 20.0 | 30.0 | app2 | ok | 29 | 3490ms | 4698ms | 4970ms |
| 20.0 | 30.0 | end-users | ok | 183 | 3498ms | 4727ms | 5425ms |
| 30.0 | 40.0 | app1 | ok | 34 | 2219ms | 4393ms | 4939ms |
| 30.0 | 40.0 | app2 | ok | 19 | 2406ms | 4472ms | 4947ms |
| 30.0 | 40.0 | end-users | ok | 144 | 3043ms | 4609ms | 4961ms |
| 40.0 | 50.0 | app1 | ok | 49 | 2888ms | 4578ms | 4958ms |
| 40.0 | 50.0 | app2 | ok | 21 | 2425ms | 4475ms | 4948ms |
| 40.0 | 50.0 | end-users | ok | 162 | 3430ms | 4686ms | 4969ms |
| 50.0 | 60.0 | app1 | ok | 46 | 3456ms | 4809ms | 8850ms |
| 50.0 | 60.0 | app2 | ok | 23 | 3203ms | 4641ms | 4964ms |
| 50.0 | 60.0 | end-users | ok | 125 | 2784ms | 4678ms | 8438ms |
| 60.0 | 70.0 | app1 | ok | 52 | 3725ms | 4745ms | 4975ms |
| 60.0 | 70.0 | app2 | ok | 28 | 3704ms | 4741ms | 4974ms |
| 60.0 | 70.0 | end-users | ok | 161 | 3666ms | 4747ms | 4990ms |
| 70.0 | 80.0 | app1 | ok | 46 | 3778ms | 4800ms | 7700ms |
| 70.0 | 80.0 | app2 | ok | 25 | 3750ms | 4750ms | 4975ms |
| 70.0 | 80.0 | end-users | ok | 148 | 3724ms | 4759ms | 4992ms |
| 80.0 | 90.0 | app1 | ok | 44 | 3750ms | 4750ms | 4975ms |
| 80.0 | 90.0 | app2 | ok | 24 | 3750ms | 4750ms | 4975ms |
| 80.0 | 90.0 | end-users | ok | 145 | 3741ms | 4792ms | 7583ms |
| 90.0 | 100.0 | app1 | ok | 52 | 3673ms | 4735ms | 4973ms |
| 90.0 | 100.0 | app2 | ok | 22 | 3625ms | 4725ms | 4972ms |
| 90.0 | 100.0 | end-users | ok | 175 | 3624ms | 4725ms | 4972ms |
| 100.0 | 110.0 | app1 | ok | 50 | 3776ms | 4796ms | 7500ms |
| 100.0 | 110.0 | app2 | ok | 24 | 3571ms | 4714ms | 4971ms |
| 100.0 | 110.0 | end-users | ok | 165 | 3668ms | 4747ms | 4989ms |
| 110.0 | 120.0 | app1 | ok | 38 | 3716ms | 4743ms | 4974ms |
| 110.0 | 120.0 | app2 | ok | 16 | 3667ms | 4733ms | 4973ms |
| 110.0 | 120.0 | end-users | ok | 120 | 3647ms | 4748ms | 4995ms |
| 120.0 | 130.0 | app1 | ok | 47 | 3634ms | 4727ms | 4973ms |
| 120.0 | 130.0 | app2 | ok | 24 | 3333ms | 4667ms | 4967ms |
| 120.0 | 130.0 | end-users | ok | 164 | 3651ms | 4730ms | 4973ms |
| 130.0 | 140.0 | app1 | ok | 64 | 3673ms | 4980ms | 9467ms |
| 130.0 | 140.0 | app2 | ok | 46 | 1706ms | 4179ms | 4918ms |
| 130.0 | 140.0 | end-users | ok | 211 | 3438ms | 4790ms | 8681ms |
| 140.0 | 151.0 | app1 | ok | 27 | 3650ms | 4730ms | 4973ms |
| 140.0 | 151.0 | app2 | ok | 10 | 1938ms | 3750ms | 4875ms |
| 140.0 | 151.0 | end-users | ok | 92 | 3661ms | 4756ms | 5400ms |
| 151.0 | 161.0 | app1 | ok | 50 | 3264ms | 4653ms | 4965ms |
| 151.0 | 161.0 | app2 | ok | 16 | 3571ms | 4714ms | 4971ms |
| 151.0 | 161.0 | end-users | ok | 157 | 3419ms | 4717ms | 6075ms |
| 161.0 | 171.0 | app1 | ok | 46 | 3226ms | 4710ms | 7700ms |
| 161.0 | 171.0 | app2 | ok | 27 | 3594ms | 4719ms | 4972ms |
| 161.0 | 171.0 | end-users | ok | 154 | 3355ms | 4671ms | 4967ms |
| 171.0 | 181.0 | app1 | ok | 45 | 3520ms | 4704ms | 4970ms |
| 171.0 | 181.0 | app2 | ok | 21 | 3456ms | 4691ms | 4969ms |
| 171.0 | 181.0 | end-users | ok | 136 | 3556ms | 4728ms | 4992ms |
| 181.0 | 191.0 | app1 | ok | 50 | 3812ms | 5833ms | 9583ms |
| 181.0 | 191.0 | app2 | ok | 32 | 3250ms | 4850ms | 9200ms |
| 181.0 | 191.0 | end-users | ok | 173 | 3820ms | 5447ms | 9545ms |
| 191.0 | 201.0 | app1 | ok | 49 | 3750ms | 6500ms | 9650ms |
| 191.0 | 201.0 | app2 | ok | 15 | 1188ms | 7500ms | 9750ms |
| 191.0 | 201.0 | end-users | ok | 159 | 3494ms | 4797ms | 8675ms |
| 201.0 | 211.0 | app1 | ok | 53 | 3508ms | 6688ms | 9669ms |
| 201.0 | 211.0 | app2 | ok | 38 | 2125ms | 4367ms | 4937ms |
| 201.0 | 211.0 | end-users | ok | 169 | 3408ms | 4853ms | 9155ms |
| 211.0 | 221.0 | app1 | ok | 47 | 3368ms | 4674ms | 4967ms |
| 211.0 | 221.0 | app2 | ok | 18 | 2125ms | 4250ms | 4925ms |
| 211.0 | 221.0 | end-users | ok | 153 | 3478ms | 4712ms | 4989ms |
| 221.0 | 231.0 | app1 | ok | 41 | 3576ms | 4715ms | 4972ms |
| 221.0 | 231.0 | app2 | ok | 12 | 3636ms | 4727ms | 4973ms |
| 221.0 | 231.0 | end-users | ok | 128 | 3654ms | 4748ms | 4994ms |
| 231.0 | 241.0 | app1 | ok | 46 | 3226ms | 4710ms | 7700ms |
| 231.0 | 241.0 | app2 | ok | 28 | 3333ms | 4667ms | 4967ms |
| 231.0 | 241.0 | end-users | ok | 139 | 3536ms | 4724ms | 4992ms |
| 241.0 | 251.0 | app1 | ok | 19 | 3472ms | 7625ms | 9762ms |
| 241.0 | 251.0 | app2 | ok | 9 | 1938ms | 4250ms | 4925ms |
| 241.0 | 251.0 | end-users | ok | 81 | 3250ms | 5500ms | 9550ms |
| 251.0 | 258.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1413270 | 70369 | 1483639.0 | 0.0% | 1532296.0 | 1554008.0 | -1.4% | True |
| app2 | 726930 | 36260 | 763190.0 | 0.0% | 769708.0 | 799450.0 | -3.7% | True |
| end-users | 4633410 | 229587 | 4862997.0 | 0.0% | 4976396.0 | 5092584.0 | -2.3% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1149 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | 0.0% | 0.00 |
| app2 | 591 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | 0.0% | 0.00 |
| end-users | 3768 | 0 | 1 | 1 | 0.03% | 68.4% | 100.0% | 1.46 |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5508). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5508 | 0.051ms | 0.102ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 246479 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1149 | 6678ms | 9191ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 591 | 13100ms | 18981ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3767 | 8240ms | 12332ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5507 | 8052ms | 14132ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2611ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 788ms | 5812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2867ms | 5456ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 6348ms | 8850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 9308ms | 14179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 7593ms | 9829ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 6536ms | 8775ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 13594ms | 19179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 8177ms | 13155ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 6696ms | 9371ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 12857ms | 18000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 8051ms | 9897ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 6160ms | 9100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 13833ms | 19281ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 8265ms | 9848ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 6462ms | 9618ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 13289ms | 18958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 8413ms | 12847ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 6759ms | 9080ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 8423ms | 13283ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 6606ms | 7915ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 13333ms | 19000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 8200ms | 12875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 6522ms | 9314ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 12750ms | 19219ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 8269ms | 10281ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 6677ms | 7984ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 14000ms | 19333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 8218ms | 9822ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 6757ms | 7973ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 13500ms | 19125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 8227ms | 9823ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 6833ms | 8400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 13000ms | 18500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 8444ms | 9844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 6679ms | 9060ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 12262ms | 17583ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 8224ms | 9822ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 6692ms | 8950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 12586ms | 14914ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 8556ms | 13318ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 151.0 | app1 | ok | 6852ms | 9490ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 151.0 | app2 | ok | 12885ms | 18125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 151.0 | end-users | ok | 8333ms | 12662ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 6545ms | 9343ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 15227ms | 19523ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 8172ms | 13038ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 6840ms | 9510ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 13571ms | 19250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 8220ms | 13359ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 6815ms | 9267ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 14028ms | 19341ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 8328ms | 13100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 7103ms | 9564ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 13077ms | 18875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 8561ms | 13652ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 6821ms | 9329ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 12727ms | 17000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 8652ms | 13639ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 6686ms | 7869ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 15588ms | 19559ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 7986ms | 11475ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 6778ms | 9329ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 12750ms | 17250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 8618ms | 14025ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 7034ms | 9489ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 16364ms | 19636ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 8154ms | 13071ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 6710ms | 8800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 15536ms | 19554ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 8212ms | 9864ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 7292ms | 9814ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 12375ms | 16875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 8831ms | 13635ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | end-users | ok | 10833ms | 14583ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
