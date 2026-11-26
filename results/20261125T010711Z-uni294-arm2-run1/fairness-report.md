# Fairness benchmark: equal-workers-control (uni294-arm2-run1)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-576d856b9-sqm6k` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-25T01:08:42Z` |
| Run end | `2026-11-25T01:13:01Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 27 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/27 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 39.00 | 1.2188 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1163 | 200=1163 | 6.7 | 7.4 | 1529718.0 | 21.1% | 33.3% | 12.3 | 21.1% | 0.1 | 21.3% | 0.3 | 4.6s | 98.9% | 1163.0 |
| app2 | 10.0 | 32 | 594 | 200=594 | 13.5 | 14.4 | 760234.0 | 10.5% | 33.3% | 22.8 | 10.5% | -0.0 | 10.9% | 0.4 | 4.2s | 98.9% | 594.0 |
| end-users | 65.0 | 32 | 3699 | 200=3699 | 2.0 | 2.6 | 4956700.0 | 68.4% | 33.3% | -35.1 | 68.4% | -0.0 | 67.8% | -0.6 | 3.7s | 98.8% | 3699.0 |
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

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 81148.0 | 68.4% | 100.0% | 31.6 |
| 10.0 | 20.0 | app1 | True | 64942.0 | 21.1% | 23.0% | 1.9 |
| 10.0 | 20.0 | app2 | True | 4074.0 | 10.5% | 1.4% | -9.1 |
| 10.0 | 20.0 | end-users | True | 213896.0 | 68.4% | 75.6% | 7.2 |
| 20.0 | 31.0 | app1 | True | 62224.0 | 21.1% | 20.4% | -0.6 |
| 20.0 | 31.0 | app2 | True | 32492.0 | 10.5% | 10.7% | 0.1 |
| 20.0 | 31.0 | end-users | True | 209650.0 | 68.4% | 68.9% | 0.5 |
| 31.0 | 41.0 | app1 | True | 64898.0 | 21.1% | 21.1% | 0.1 |
| 31.0 | 41.0 | app2 | True | 33766.0 | 10.5% | 11.0% | 0.5 |
| 31.0 | 41.0 | end-users | True | 208234.0 | 68.4% | 67.9% | -0.6 |
| 41.0 | 51.0 | app1 | True | 62208.0 | 21.1% | 20.7% | -0.3 |
| 41.0 | 51.0 | app2 | True | 31158.0 | 10.5% | 10.4% | -0.1 |
| 41.0 | 51.0 | end-users | True | 206796.0 | 68.4% | 68.9% | 0.5 |
| 51.0 | 61.0 | app1 | True | 66288.0 | 21.1% | 20.9% | -0.2 |
| 51.0 | 61.0 | app2 | True | 33764.0 | 10.5% | 10.6% | 0.1 |
| 51.0 | 61.0 | end-users | True | 217612.0 | 68.4% | 68.5% | 0.1 |
| 61.0 | 71.0 | app1 | True | 66252.0 | 21.1% | 21.6% | 0.5 |
| 61.0 | 71.0 | app2 | True | 32502.0 | 10.5% | 10.6% | 0.1 |
| 61.0 | 71.0 | end-users | True | 208218.0 | 68.4% | 67.8% | -0.6 |
| 71.0 | 81.0 | app1 | True | 63576.0 | 21.1% | 21.0% | -0.1 |
| 71.0 | 81.0 | app2 | True | 31106.0 | 10.5% | 10.3% | -0.3 |
| 71.0 | 81.0 | end-users | True | 208350.0 | 68.4% | 68.8% | 0.3 |
| 81.0 | 91.0 | app1 | True | 63620.0 | 21.1% | 21.0% | -0.1 |
| 81.0 | 91.0 | app2 | True | 32454.0 | 10.5% | 10.7% | 0.2 |
| 81.0 | 91.0 | end-users | True | 207108.0 | 68.4% | 68.3% | -0.1 |
| 91.0 | 101.0 | app1 | True | 64812.0 | 21.1% | 21.0% | -0.0 |
| 91.0 | 101.0 | app2 | True | 32498.0 | 10.5% | 10.5% | 0.0 |
| 91.0 | 101.0 | end-users | True | 210882.0 | 68.4% | 68.4% | 0.0 |
| 101.0 | 111.0 | app1 | True | 63470.0 | 21.1% | 21.0% | -0.0 |
| 101.0 | 111.0 | app2 | True | 31108.0 | 10.5% | 10.3% | -0.2 |
| 101.0 | 111.0 | end-users | True | 206946.0 | 68.4% | 68.6% | 0.2 |
| 111.0 | 121.0 | app1 | True | 63602.0 | 21.1% | 20.8% | -0.3 |
| 111.0 | 121.0 | app2 | True | 32516.0 | 10.5% | 10.6% | 0.1 |
| 111.0 | 121.0 | end-users | True | 209672.0 | 68.4% | 68.6% | 0.1 |
| 121.0 | 131.0 | app1 | True | 66380.0 | 21.1% | 21.6% | 0.6 |
| 121.0 | 131.0 | app2 | True | 32408.0 | 10.5% | 10.6% | 0.0 |
| 121.0 | 131.0 | end-users | True | 208182.0 | 68.4% | 67.8% | -0.6 |
| 131.0 | 141.0 | app1 | True | 60828.0 | 21.1% | 20.2% | -0.9 |
| 131.0 | 141.0 | app2 | True | 32450.0 | 10.5% | 10.8% | 0.2 |
| 131.0 | 141.0 | end-users | True | 208228.0 | 68.4% | 69.1% | 0.6 |
| 141.0 | 151.0 | app1 | True | 66320.0 | 21.1% | 21.9% | 0.8 |
| 141.0 | 151.0 | app2 | True | 31122.0 | 10.5% | 10.3% | -0.3 |
| 141.0 | 151.0 | end-users | True | 205694.0 | 68.4% | 67.9% | -0.6 |
| 151.0 | 161.0 | app1 | True | 62258.0 | 21.1% | 20.4% | -0.6 |
| 151.0 | 161.0 | app2 | True | 32486.0 | 10.5% | 10.7% | 0.1 |
| 151.0 | 161.0 | end-users | True | 209808.0 | 68.4% | 68.9% | 0.5 |
| 161.0 | 171.0 | app1 | True | 66328.0 | 21.1% | 21.5% | 0.5 |
| 161.0 | 171.0 | app2 | True | 31106.0 | 10.5% | 10.1% | -0.4 |
| 161.0 | 171.0 | end-users | True | 210798.0 | 68.4% | 68.4% | -0.0 |
| 171.0 | 181.0 | app1 | True | 64982.0 | 21.1% | 21.4% | 0.4 |
| 171.0 | 181.0 | app2 | True | 33736.0 | 10.5% | 11.1% | 0.6 |
| 171.0 | 181.0 | end-users | True | 204292.0 | 68.4% | 67.4% | -1.0 |
| 181.0 | 191.0 | app1 | True | 62140.0 | 21.1% | 20.1% | -1.0 |
| 181.0 | 191.0 | app2 | True | 31070.0 | 10.5% | 10.0% | -0.5 |
| 181.0 | 191.0 | end-users | True | 216360.0 | 68.4% | 69.9% | 1.5 |
| 191.0 | 201.0 | app1 | True | 63576.0 | 21.1% | 21.1% | 0.0 |
| 191.0 | 201.0 | app2 | True | 32488.0 | 10.5% | 10.8% | 0.3 |
| 191.0 | 201.0 | end-users | True | 205404.0 | 68.4% | 68.1% | -0.3 |
| 201.0 | 211.0 | app1 | True | 67610.0 | 21.1% | 21.8% | 0.8 |
| 201.0 | 211.0 | app2 | True | 32434.0 | 10.5% | 10.5% | -0.0 |
| 201.0 | 211.0 | end-users | True | 209532.0 | 68.4% | 67.7% | -0.7 |
| 211.0 | 221.0 | app1 | True | 62288.0 | 21.1% | 20.6% | -0.4 |
| 211.0 | 221.0 | app2 | True | 31148.0 | 10.5% | 10.3% | -0.2 |
| 211.0 | 221.0 | end-users | True | 208354.0 | 68.4% | 69.0% | 0.6 |
| 221.0 | 231.0 | app1 | True | 62254.0 | 21.1% | 20.6% | -0.4 |
| 221.0 | 231.0 | app2 | True | 32546.0 | 10.5% | 10.8% | 0.3 |
| 221.0 | 231.0 | end-users | True | 206980.0 | 68.4% | 68.6% | 0.2 |
| 231.0 | 241.0 | app1 | True | 64900.0 | 21.1% | 21.0% | -0.1 |
| 231.0 | 241.0 | app2 | True | 32490.0 | 10.5% | 10.5% | -0.0 |
| 231.0 | 241.0 | end-users | True | 212318.0 | 68.4% | 68.6% | 0.1 |
| 241.0 | 251.0 | app1 | False | 53962.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 47312.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 62238.0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 259.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 62 | 0ms | 793ms | 979ms |
| 0.0 | 10.0 | app2 | ok | 48 | 0ms | 733ms | 973ms |
| 0.0 | 10.0 | end-users | ok | 115 | 165ms | 617ms | 962ms |
| 10.0 | 20.0 | app1 | ok | 50 | 306ms | 861ms | 986ms |
| 10.0 | 20.0 | app2 | ok | 18 | 278ms | 478ms | 910ms |
| 10.0 | 20.0 | end-users | ok | 158 | 317ms | 828ms | 983ms |
| 20.0 | 31.0 | app1 | ok | 43 | 337ms | 835ms | 983ms |
| 20.0 | 31.0 | app2 | ok | 24 | 312ms | 867ms | 987ms |
| 20.0 | 31.0 | end-users | ok | 156 | 324ms | 814ms | 981ms |
| 31.0 | 41.0 | app1 | ok | 51 | 326ms | 804ms | 980ms |
| 31.0 | 41.0 | app2 | ok | 26 | 333ms | 740ms | 974ms |
| 31.0 | 41.0 | end-users | ok | 163 | 309ms | 767ms | 977ms |
| 41.0 | 51.0 | app1 | ok | 43 | 298ms | 805ms | 980ms |
| 41.0 | 51.0 | app2 | ok | 22 | 346ms | 633ms | 963ms |
| 41.0 | 51.0 | end-users | ok | 146 | 352ms | 845ms | 984ms |
| 51.0 | 61.0 | app1 | ok | 51 | 244ms | 804ms | 980ms |
| 51.0 | 61.0 | app2 | ok | 24 | 500ms | 900ms | 990ms |
| 51.0 | 61.0 | end-users | ok | 160 | 266ms | 771ms | 977ms |
| 61.0 | 71.0 | app1 | ok | 47 | 284ms | 832ms | 983ms |
| 61.0 | 71.0 | app2 | ok | 23 | 241ms | 808ms | 981ms |
| 61.0 | 71.0 | end-users | ok | 155 | 339ms | 832ms | 983ms |
| 71.0 | 81.0 | app1 | ok | 47 | 233ms | 664ms | 966ms |
| 71.0 | 81.0 | app2 | ok | 25 | 292ms | 750ms | 975ms |
| 71.0 | 81.0 | end-users | ok | 150 | 299ms | 821ms | 982ms |
| 81.0 | 91.0 | app1 | ok | 49 | 322ms | 777ms | 978ms |
| 81.0 | 91.0 | app2 | ok | 25 | 268ms | 792ms | 979ms |
| 81.0 | 91.0 | end-users | ok | 164 | 314ms | 800ms | 980ms |
| 91.0 | 101.0 | app1 | ok | 46 | 271ms | 808ms | 981ms |
| 91.0 | 101.0 | app2 | ok | 23 | 241ms | 808ms | 981ms |
| 91.0 | 101.0 | end-users | ok | 146 | 283ms | 779ms | 978ms |
| 101.0 | 111.0 | app1 | ok | 47 | 296ms | 706ms | 971ms |
| 101.0 | 111.0 | app2 | ok | 23 | 362ms | 808ms | 981ms |
| 101.0 | 111.0 | end-users | ok | 152 | 322ms | 805ms | 981ms |
| 111.0 | 121.0 | app1 | ok | 48 | 160ms | 760ms | 976ms |
| 111.0 | 121.0 | app2 | ok | 25 | 352ms | 792ms | 979ms |
| 111.0 | 121.0 | end-users | ok | 153 | 347ms | 813ms | 981ms |
| 121.0 | 131.0 | app1 | ok | 50 | 304ms | 821ms | 982ms |
| 121.0 | 131.0 | app2 | ok | 24 | 375ms | 867ms | 987ms |
| 121.0 | 131.0 | end-users | ok | 166 | 238ms | 811ms | 981ms |
| 131.0 | 141.0 | app1 | ok | 45 | 438ms | 882ms | 988ms |
| 131.0 | 141.0 | app2 | ok | 23 | 347ms | 808ms | 981ms |
| 131.0 | 141.0 | end-users | ok | 155 | 264ms | 772ms | 977ms |
| 141.0 | 151.0 | app1 | ok | 45 | 392ms | 859ms | 986ms |
| 141.0 | 151.0 | app2 | ok | 22 | 389ms | 843ms | 984ms |
| 141.0 | 151.0 | end-users | ok | 144 | 319ms | 782ms | 978ms |
| 151.0 | 161.0 | app1 | ok | 50 | 359ms | 844ms | 984ms |
| 151.0 | 161.0 | app2 | ok | 26 | 306ms | 783ms | 978ms |
| 151.0 | 161.0 | end-users | ok | 164 | 288ms | 778ms | 978ms |
| 161.0 | 171.0 | app1 | ok | 46 | 292ms | 823ms | 982ms |
| 161.0 | 171.0 | app2 | ok | 23 | 205ms | 712ms | 971ms |
| 161.0 | 171.0 | end-users | ok | 144 | 378ms | 864ms | 986ms |
| 171.0 | 181.0 | app1 | ok | 45 | 488ms | 898ms | 990ms |
| 171.0 | 181.0 | app2 | ok | 23 | 225ms | 872ms | 987ms |
| 171.0 | 181.0 | end-users | ok | 155 | 458ms | 891ms | 989ms |
| 181.0 | 191.0 | app1 | ok | 51 | 243ms | 804ms | 980ms |
| 181.0 | 191.0 | app2 | ok | 24 | 417ms | 891ms | 989ms |
| 181.0 | 191.0 | end-users | ok | 158 | 332ms | 812ms | 981ms |
| 191.0 | 201.0 | app1 | ok | 46 | 333ms | 791ms | 979ms |
| 191.0 | 201.0 | app2 | ok | 23 | 339ms | 836ms | 984ms |
| 191.0 | 201.0 | end-users | ok | 151 | 303ms | 771ms | 977ms |
| 201.0 | 211.0 | app1 | ok | 52 | 462ms | 892ms | 989ms |
| 201.0 | 211.0 | app2 | ok | 26 | 500ms | 900ms | 990ms |
| 201.0 | 211.0 | end-users | ok | 164 | 391ms | 866ms | 987ms |
| 211.0 | 221.0 | app1 | ok | 47 | 233ms | 786ms | 979ms |
| 211.0 | 221.0 | app2 | ok | 23 | 344ms | 872ms | 987ms |
| 211.0 | 221.0 | end-users | ok | 153 | 310ms | 822ms | 982ms |
| 221.0 | 231.0 | app1 | ok | 45 | 284ms | 827ms | 983ms |
| 221.0 | 231.0 | app2 | ok | 23 | 396ms | 872ms | 987ms |
| 221.0 | 231.0 | end-users | ok | 143 | 439ms | 885ms | 988ms |
| 231.0 | 241.0 | app1 | ok | 46 | 354ms | 856ms | 986ms |
| 231.0 | 241.0 | app2 | ok | 23 | 406ms | 885ms | 988ms |
| 231.0 | 241.0 | end-users | ok | 161 | 342ms | 836ms | 984ms |
| 241.0 | 251.0 | app1 | ok | 11 | 375ms | 890ms | 989ms |
| 241.0 | 251.0 | app2 | ok | 5 | 583ms | 917ms | 992ms |
| 241.0 | 251.0 | end-users | ok | 23 | 304ms | 808ms | 981ms |
| 251.0 | 259.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 259.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1430490 | 71285 | 1501775.0 | 0.0% | 1529718.0 | 1573060.0 | -2.8% | True |
| app2 | 730620 | 36414 | 767034.0 | 0.0% | 760234.0 | 803448.0 | -5.4% | True |
| end-users | 4549770 | 226471 | 4776241.0 | 0.0% | 4956700.0 | 5002712.0 | -0.9% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1163 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 594 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3699 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5456). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5456 | 0.052ms | 0.196ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 246329 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1163 | 6881ms | 7893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 594 | 12363ms | 14802ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3699 | 1990ms | 2900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5456 | 2457ms | 12584ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 3429ms | 4950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 3250ms | 5600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 1864ms | 2874ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 6780ms | 7878ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 11136ms | 15250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 1848ms | 2854ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 31.0 | app1 | ok | 6865ms | 7984ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 31.0 | app2 | ok | 13529ms | 19143ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 31.0 | end-users | ok | 1907ms | 2892ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 31.0 | 41.0 | app1 | ok | 6933ms | 7893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 31.0 | 41.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 31.0 | 41.0 | end-users | ok | 2013ms | 2901ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | app1 | ok | 6930ms | 7893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | end-users | ok | 1996ms | 2899ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app1 | ok | 6957ms | 7896ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | end-users | ok | 1985ms | 2897ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app1 | ok | 6911ms | 7891ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | end-users | ok | 2025ms | 2903ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | end-users | ok | 1993ms | 2899ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 6978ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 2110ms | 2911ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 6957ms | 7896ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 1993ms | 2899ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 6978ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 1989ms | 2898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 6933ms | 7893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 2066ms | 2907ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 6979ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 2061ms | 2906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 1975ms | 2895ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 2062ms | 2906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 1997ms | 2899ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 6979ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 1986ms | 2897ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 6829ms | 7883ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 1989ms | 2936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 6872ms | 7933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 1944ms | 2889ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 1987ms | 2897ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 6958ms | 7896ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 2043ms | 2904ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 6722ms | 7872ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 1945ms | 2890ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 6722ms | 7872ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 1996ms | 2899ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 6979ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 2108ms | 2911ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 5700ms | 7765ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 10625ms | 14562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 2207ms | 2921ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 259.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 259.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 259.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
