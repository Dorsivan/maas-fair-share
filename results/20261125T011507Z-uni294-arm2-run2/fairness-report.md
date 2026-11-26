# Fairness benchmark: equal-workers-control (uni294-arm2-run2)

**Verdict: INFO** -- named negative control, not scored against the 10-point threshold. Expected to NOT reproduce the configured weights; see docs/runbook.md.
Worker-share vs. weight-share gap (UNI-225): 35.1 points

- negative control, not scored against the 10-point threshold: max deviation was 0.1 points. This scenario is expected to compress toward equal shares, not reproduce the configured weights -- see docs/runbook.md's 'Per-tenant worker sizing and the saturation check'

## Run metadata

| field | value |
|---|---|
| Scenario | `equal-workers-control` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:7e406c43a57fd444b8930d00d3d8423b48fbc743e9abaf32ca624e97b2f76df7` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-576d856b9-dpk2k` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-25T01:16:31Z` |
| Run end | `2026-11-25T01:20:42Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 26 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/26 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 39.50 | 1.2344 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1157 | 200=1157 | 6.7 | 7.5 | 1521460.0 | 21.1% | 33.3% | 12.3 | 21.0% | -0.0 | 21.2% | 0.2 | 4.6s | 98.9% | 1157.0 |
| app2 | 10.0 | 32 | 592 | 200=592 | 13.4 | 14.5 | 757106.0 | 10.5% | 33.3% | 22.8 | 10.5% | -0.1 | 10.9% | 0.3 | 4.3s | 98.9% | 592.0 |
| end-users | 65.0 | 32 | 3704 | 200=3704 | 2.0 | 2.6 | 4962478.0 | 68.4% | 33.3% | -35.1 | 68.5% | 0.1 | 67.9% | -0.5 | 3.7s | 98.9% | 3704.0 |
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

**Windows** (25 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 91948.0 | 68.4% | 100.0% | 31.6 |
| 10.0 | 20.0 | app1 | True | 59602.0 | 21.1% | 21.6% | 0.5 |
| 10.0 | 20.0 | app2 | True | 4074.0 | 10.5% | 1.5% | -9.1 |
| 10.0 | 20.0 | end-users | True | 212388.0 | 68.4% | 76.9% | 8.5 |
| 20.0 | 30.0 | app1 | True | 63532.0 | 21.1% | 20.4% | -0.6 |
| 20.0 | 30.0 | app2 | True | 32398.0 | 10.5% | 10.4% | -0.1 |
| 20.0 | 30.0 | end-users | True | 215062.0 | 68.4% | 69.2% | 0.7 |
| 30.0 | 40.0 | app1 | True | 66194.0 | 21.1% | 21.8% | 0.7 |
| 30.0 | 40.0 | app2 | True | 32402.0 | 10.5% | 10.7% | 0.1 |
| 30.0 | 40.0 | end-users | True | 205528.0 | 68.4% | 67.6% | -0.8 |
| 40.0 | 50.0 | app1 | True | 67546.0 | 21.1% | 22.0% | 0.9 |
| 40.0 | 50.0 | app2 | True | 29804.0 | 10.5% | 9.7% | -0.8 |
| 40.0 | 50.0 | end-users | True | 209720.0 | 68.4% | 68.3% | -0.1 |
| 50.0 | 60.0 | app1 | True | 62246.0 | 21.1% | 20.4% | -0.7 |
| 50.0 | 60.0 | app2 | True | 35226.0 | 10.5% | 11.5% | 1.0 |
| 50.0 | 60.0 | end-users | True | 208266.0 | 68.4% | 68.1% | -0.3 |
| 60.0 | 70.0 | app1 | True | 62202.0 | 21.1% | 20.3% | -0.7 |
| 60.0 | 70.0 | app2 | True | 32490.0 | 10.5% | 10.6% | 0.1 |
| 60.0 | 70.0 | end-users | True | 211098.0 | 68.4% | 69.0% | 0.6 |
| 70.0 | 80.0 | app1 | True | 64920.0 | 21.1% | 21.3% | 0.3 |
| 70.0 | 80.0 | app2 | True | 32466.0 | 10.5% | 10.7% | 0.2 |
| 70.0 | 80.0 | end-users | True | 206700.0 | 68.4% | 68.0% | -0.4 |
| 80.0 | 90.0 | app1 | True | 64872.0 | 21.1% | 21.4% | 0.4 |
| 80.0 | 90.0 | app2 | True | 29734.0 | 10.5% | 9.8% | -0.7 |
| 80.0 | 90.0 | end-users | True | 208492.0 | 68.4% | 68.8% | 0.4 |
| 90.0 | 100.0 | app1 | True | 64902.0 | 21.1% | 21.0% | -0.1 |
| 90.0 | 100.0 | app2 | True | 33828.0 | 10.5% | 10.9% | 0.4 |
| 90.0 | 100.0 | end-users | True | 210956.0 | 68.4% | 68.1% | -0.3 |
| 100.0 | 110.0 | app1 | True | 63630.0 | 21.1% | 21.1% | 0.0 |
| 100.0 | 110.0 | app2 | True | 31070.0 | 10.5% | 10.3% | -0.2 |
| 100.0 | 110.0 | end-users | True | 207000.0 | 68.4% | 68.6% | 0.2 |
| 110.0 | 120.0 | app1 | True | 63600.0 | 21.1% | 20.9% | -0.2 |
| 110.0 | 120.0 | app2 | True | 32438.0 | 10.5% | 10.7% | 0.1 |
| 110.0 | 120.0 | end-users | True | 208282.0 | 68.4% | 68.4% | 0.0 |
| 120.0 | 130.0 | app1 | True | 63648.0 | 21.1% | 21.1% | 0.0 |
| 120.0 | 130.0 | app2 | True | 32454.0 | 10.5% | 10.8% | 0.2 |
| 120.0 | 130.0 | end-users | True | 205678.0 | 68.4% | 68.2% | -0.3 |
| 130.0 | 140.0 | app1 | True | 63532.0 | 21.1% | 20.8% | -0.3 |
| 130.0 | 140.0 | app2 | True | 31116.0 | 10.5% | 10.2% | -0.3 |
| 130.0 | 140.0 | end-users | True | 211098.0 | 68.4% | 69.0% | 0.6 |
| 140.0 | 150.0 | app1 | True | 66306.0 | 21.1% | 21.5% | 0.5 |
| 140.0 | 150.0 | app2 | True | 32298.0 | 10.5% | 10.5% | -0.0 |
| 140.0 | 150.0 | end-users | True | 209508.0 | 68.4% | 68.0% | -0.4 |
| 150.0 | 160.0 | app1 | True | 62162.0 | 21.1% | 20.4% | -0.6 |
| 150.0 | 160.0 | app2 | True | 31032.0 | 10.5% | 10.2% | -0.3 |
| 150.0 | 160.0 | end-users | True | 211156.0 | 68.4% | 69.4% | 1.0 |
| 160.0 | 171.0 | app1 | True | 64918.0 | 21.1% | 21.2% | 0.1 |
| 160.0 | 171.0 | app2 | True | 33746.0 | 10.5% | 11.0% | 0.5 |
| 160.0 | 171.0 | end-users | True | 208194.0 | 68.4% | 67.8% | -0.6 |
| 171.0 | 181.0 | app1 | True | 64874.0 | 21.1% | 21.3% | 0.3 |
| 171.0 | 181.0 | app2 | True | 31110.0 | 10.5% | 10.2% | -0.3 |
| 171.0 | 181.0 | end-users | True | 208096.0 | 68.4% | 68.4% | 0.0 |
| 181.0 | 191.0 | app1 | True | 63526.0 | 21.1% | 20.8% | -0.3 |
| 181.0 | 191.0 | app2 | True | 33866.0 | 10.5% | 11.1% | 0.6 |
| 181.0 | 191.0 | end-users | True | 208332.0 | 68.4% | 68.1% | -0.3 |
| 191.0 | 201.0 | app1 | True | 63444.0 | 21.1% | 20.6% | -0.5 |
| 191.0 | 201.0 | app2 | True | 29706.0 | 10.5% | 9.6% | -0.9 |
| 191.0 | 201.0 | end-users | True | 215206.0 | 68.4% | 69.8% | 1.4 |
| 201.0 | 211.0 | app1 | True | 66332.0 | 21.1% | 21.8% | 0.7 |
| 201.0 | 211.0 | app2 | True | 33816.0 | 10.5% | 11.1% | 0.6 |
| 201.0 | 211.0 | end-users | True | 204206.0 | 68.4% | 67.1% | -1.3 |
| 211.0 | 221.0 | app1 | True | 64904.0 | 21.1% | 21.1% | 0.0 |
| 211.0 | 221.0 | app2 | True | 32502.0 | 10.5% | 10.5% | 0.0 |
| 211.0 | 221.0 | end-users | True | 210854.0 | 68.4% | 68.4% | -0.0 |
| 221.0 | 231.0 | app1 | True | 63528.0 | 21.1% | 20.8% | -0.3 |
| 221.0 | 231.0 | app2 | True | 31114.0 | 10.5% | 10.2% | -0.3 |
| 221.0 | 231.0 | end-users | True | 210948.0 | 68.4% | 69.0% | 0.6 |
| 231.0 | 241.0 | app1 | True | 64990.0 | 21.1% | 21.3% | 0.2 |
| 231.0 | 241.0 | app2 | True | 33780.0 | 10.5% | 11.0% | 0.5 |
| 231.0 | 241.0 | end-users | True | 206942.0 | 68.4% | 67.7% | -0.7 |
| 241.0 | 251.0 | app1 | False | 46050.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 44636.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 56820.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 59 | 0ms | 448ms | 902ms |
| 0.0 | 10.0 | app2 | ok | 46 | 0ms | 450ms | 923ms |
| 0.0 | 10.0 | end-users | ok | 131 | 244ms | 802ms | 980ms |
| 10.0 | 20.0 | app1 | ok | 48 | 294ms | 760ms | 976ms |
| 10.0 | 20.0 | app2 | ok | 21 | 438ms | 895ms | 989ms |
| 10.0 | 20.0 | end-users | ok | 152 | 369ms | 827ms | 983ms |
| 20.0 | 30.0 | app1 | ok | 48 | 212ms | 840ms | 984ms |
| 20.0 | 30.0 | app2 | ok | 23 | 239ms | 808ms | 981ms |
| 20.0 | 30.0 | end-users | ok | 165 | 230ms | 788ms | 979ms |
| 30.0 | 40.0 | app1 | ok | 48 | 345ms | 782ms | 978ms |
| 30.0 | 40.0 | app2 | ok | 25 | 239ms | 844ms | 984ms |
| 30.0 | 40.0 | end-users | ok | 148 | 312ms | 745ms | 974ms |
| 40.0 | 50.0 | app1 | ok | 50 | 212ms | 792ms | 979ms |
| 40.0 | 50.0 | app2 | ok | 22 | 229ms | 817ms | 982ms |
| 40.0 | 50.0 | end-users | ok | 158 | 327ms | 816ms | 982ms |
| 50.0 | 60.0 | app1 | ok | 45 | 244ms | 750ms | 975ms |
| 50.0 | 60.0 | app2 | ok | 25 | 347ms | 821ms | 982ms |
| 50.0 | 60.0 | end-users | ok | 155 | 337ms | 820ms | 982ms |
| 60.0 | 70.0 | app1 | ok | 48 | 346ms | 850ms | 985ms |
| 60.0 | 70.0 | app2 | ok | 24 | 357ms | 850ms | 985ms |
| 60.0 | 70.0 | end-users | ok | 152 | 339ms | 800ms | 980ms |
| 70.0 | 80.0 | app1 | ok | 44 | 286ms | 780ms | 978ms |
| 70.0 | 80.0 | app2 | ok | 23 | 297ms | 770ms | 977ms |
| 70.0 | 80.0 | end-users | ok | 150 | 335ms | 837ms | 984ms |
| 80.0 | 90.0 | app1 | ok | 51 | 296ms | 745ms | 975ms |
| 80.0 | 90.0 | app2 | ok | 23 | 292ms | 872ms | 987ms |
| 80.0 | 90.0 | end-users | ok | 151 | 355ms | 839ms | 984ms |
| 90.0 | 100.0 | app1 | ok | 49 | 298ms | 825ms | 982ms |
| 90.0 | 100.0 | app2 | ok | 25 | 266ms | 750ms | 975ms |
| 90.0 | 100.0 | end-users | ok | 167 | 364ms | 858ms | 986ms |
| 100.0 | 110.0 | app1 | ok | 43 | 348ms | 835ms | 983ms |
| 100.0 | 110.0 | app2 | ok | 23 | 268ms | 770ms | 977ms |
| 100.0 | 110.0 | end-users | ok | 145 | 332ms | 839ms | 984ms |
| 110.0 | 120.0 | app1 | ok | 47 | 317ms | 832ms | 983ms |
| 110.0 | 120.0 | app2 | ok | 23 | 198ms | 617ms | 962ms |
| 110.0 | 120.0 | end-users | ok | 155 | 310ms | 811ms | 981ms |
| 120.0 | 130.0 | app1 | ok | 48 | 350ms | 840ms | 984ms |
| 120.0 | 130.0 | app2 | ok | 23 | 328ms | 808ms | 981ms |
| 120.0 | 130.0 | end-users | ok | 155 | 314ms | 811ms | 981ms |
| 130.0 | 140.0 | app1 | ok | 48 | 286ms | 800ms | 980ms |
| 130.0 | 140.0 | app2 | ok | 25 | 312ms | 844ms | 984ms |
| 130.0 | 140.0 | end-users | ok | 158 | 330ms | 824ms | 982ms |
| 140.0 | 150.0 | app1 | ok | 47 | 365ms | 862ms | 986ms |
| 140.0 | 150.0 | app2 | ok | 25 | 359ms | 844ms | 984ms |
| 140.0 | 150.0 | end-users | ok | 151 | 327ms | 832ms | 983ms |
| 150.0 | 160.0 | app1 | ok | 50 | 250ms | 821ms | 982ms |
| 150.0 | 160.0 | app2 | ok | 23 | 262ms | 492ms | 942ms |
| 150.0 | 160.0 | end-users | ok | 159 | 235ms | 759ms | 976ms |
| 160.0 | 171.0 | app1 | ok | 46 | 281ms | 744ms | 974ms |
| 160.0 | 171.0 | app2 | ok | 24 | 500ms | 900ms | 990ms |
| 160.0 | 171.0 | end-users | ok | 152 | 322ms | 805ms | 981ms |
| 171.0 | 181.0 | app1 | ok | 48 | 375ms | 850ms | 985ms |
| 171.0 | 181.0 | app2 | ok | 24 | 417ms | 880ms | 988ms |
| 171.0 | 181.0 | end-users | ok | 157 | 253ms | 769ms | 977ms |
| 181.0 | 191.0 | app1 | ok | 48 | 300ms | 850ms | 985ms |
| 181.0 | 191.0 | app2 | ok | 23 | 297ms | 770ms | 977ms |
| 181.0 | 191.0 | end-users | ok | 145 | 348ms | 835ms | 984ms |
| 191.0 | 201.0 | app1 | ok | 47 | 352ms | 832ms | 983ms |
| 191.0 | 201.0 | app2 | ok | 24 | 321ms | 829ms | 983ms |
| 191.0 | 201.0 | end-users | ok | 165 | 350ms | 832ms | 983ms |
| 201.0 | 211.0 | app1 | ok | 48 | 286ms | 800ms | 980ms |
| 201.0 | 211.0 | app2 | ok | 24 | 375ms | 880ms | 988ms |
| 201.0 | 211.0 | end-users | ok | 152 | 338ms | 805ms | 981ms |
| 211.0 | 221.0 | app1 | ok | 46 | 339ms | 836ms | 984ms |
| 211.0 | 221.0 | app2 | ok | 24 | 438ms | 880ms | 988ms |
| 211.0 | 221.0 | end-users | ok | 153 | 317ms | 775ms | 978ms |
| 221.0 | 231.0 | app1 | ok | 50 | 317ms | 821ms | 982ms |
| 221.0 | 231.0 | app2 | ok | 24 | 344ms | 829ms | 983ms |
| 221.0 | 231.0 | end-users | ok | 164 | 318ms | 836ms | 984ms |
| 231.0 | 241.0 | app1 | ok | 47 | 323ms | 843ms | 984ms |
| 231.0 | 241.0 | app2 | ok | 24 | 292ms | 829ms | 983ms |
| 231.0 | 241.0 | end-users | ok | 152 | 386ms | 864ms | 986ms |
| 241.0 | 251.0 | app1 | ok | 4 | 500ms | 900ms | 990ms |
| 241.0 | 251.0 | app2 | ok | 2 | 750ms | 950ms | 995ms |
| 241.0 | 251.0 | end-users | ok | 12 | 175ms | 700ms | 970ms |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1423110 | 70839 | 1493949.0 | 0.0% | 1521460.0 | 1564788.0 | -2.8% | True |
| app2 | 728160 | 36105 | 764265.0 | 0.0% | 757106.0 | 800370.0 | -5.4% | True |
| end-users | 4555920 | 226938 | 4782858.0 | 0.0% | 4962478.0 | 5009796.0 | -0.9% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1157 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 592 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3704 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5453). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5453 | 0.052ms | 0.194ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 239426 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1157 | 6885ms | 7897ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 592 | 12385ms | 14829ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3704 | 1980ms | 2898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5453 | 2442ms | 12600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (25 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2591ms | 5807ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2250ms | 7250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 1657ms | 2636ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 6911ms | 7891ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 11667ms | 17500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 1902ms | 2873ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 6854ms | 7885ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 14000ms | 19333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 1958ms | 2891ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 6935ms | 7893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 1992ms | 2899ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 6750ms | 7875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 2119ms | 2912ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 6824ms | 8467ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 1970ms | 2908ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 6923ms | 7985ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 2037ms | 2904ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 1961ms | 2892ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 6979ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 2038ms | 2904ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 6933ms | 7893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 2013ms | 2901ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 6932ms | 7893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 1996ms | 2899ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 6956ms | 7896ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 1978ms | 2896ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 6854ms | 7885ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 2062ms | 2906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 6978ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 1973ms | 2895ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | end-users | ok | 1972ms | 2894ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 6978ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | end-users | ok | 2071ms | 2907ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 171.0 | app1 | ok | 6979ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 171.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 171.0 | end-users | ok | 2025ms | 2903ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 1968ms | 2893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 6854ms | 7885ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 1986ms | 2922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 6907ms | 7891ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 1990ms | 2898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 6833ms | 7883ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 1983ms | 2897ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 6979ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 2071ms | 2907ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 1936ms | 2884ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 6769ms | 7877ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 1977ms | 2895ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 6300ms | 7830ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 10417ms | 14542ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 2192ms | 2919ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
