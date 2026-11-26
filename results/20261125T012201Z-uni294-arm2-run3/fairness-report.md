# Fairness benchmark: equal-workers-control (uni294-arm2-run3)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-576d856b9-k6vp5` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-25T01:23:18Z` |
| Run end | `2026-11-25T01:27:37Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 27 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/27 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 39.50 | 1.2344 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1163 | 200=1163 | 6.7 | 7.3 | 1528238.0 | 21.1% | 33.3% | 12.3 | 21.0% | -0.0 | 21.2% | 0.2 | 4.0s | 98.9% | 1163.0 |
| app2 | 10.0 | 32 | 594 | 200=594 | 13.4 | 14.3 | 759836.0 | 10.5% | 33.3% | 22.8 | 10.4% | -0.1 | 10.8% | 0.3 | 3.7s | 98.9% | 594.0 |
| end-users | 65.0 | 32 | 3720 | 200=3720 | 2.0 | 2.5 | 4985092.0 | 68.4% | 33.3% | -35.1 | 68.5% | 0.1 | 67.9% | -0.5 | 3.1s | 98.9% | 3720.0 |
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
| 0.0 | 10.0 | end-users | True | 90616.0 | 68.4% | 100.0% | 31.6 |
| 10.0 | 20.0 | app1 | True | 59510.0 | 21.1% | 20.9% | -0.2 |
| 10.0 | 20.0 | app2 | True | 4046.0 | 10.5% | 1.4% | -9.1 |
| 10.0 | 20.0 | end-users | True | 221802.0 | 68.4% | 77.7% | 9.3 |
| 20.0 | 30.0 | app1 | True | 63516.0 | 21.1% | 20.7% | -0.4 |
| 20.0 | 30.0 | app2 | True | 33840.0 | 10.5% | 11.0% | 0.5 |
| 20.0 | 30.0 | end-users | True | 209750.0 | 68.4% | 68.3% | -0.1 |
| 30.0 | 40.0 | app1 | True | 64934.0 | 21.1% | 21.2% | 0.2 |
| 30.0 | 40.0 | app2 | True | 31124.0 | 10.5% | 10.2% | -0.3 |
| 30.0 | 40.0 | end-users | True | 209650.0 | 68.4% | 68.6% | 0.2 |
| 40.0 | 50.0 | app1 | True | 63586.0 | 21.1% | 20.9% | -0.2 |
| 40.0 | 50.0 | app2 | True | 32464.0 | 10.5% | 10.7% | 0.1 |
| 40.0 | 50.0 | end-users | True | 208282.0 | 68.4% | 68.4% | 0.0 |
| 50.0 | 60.0 | app1 | True | 64976.0 | 21.1% | 21.3% | 0.2 |
| 50.0 | 60.0 | app2 | True | 31080.0 | 10.5% | 10.2% | -0.4 |
| 50.0 | 60.0 | end-users | True | 209590.0 | 68.4% | 68.6% | 0.2 |
| 60.0 | 70.0 | app1 | True | 66202.0 | 21.1% | 21.6% | 0.5 |
| 60.0 | 70.0 | app2 | True | 32486.0 | 10.5% | 10.6% | 0.1 |
| 60.0 | 70.0 | end-users | True | 208418.0 | 68.4% | 67.9% | -0.6 |
| 70.0 | 80.0 | app1 | True | 62220.0 | 21.1% | 20.5% | -0.6 |
| 70.0 | 80.0 | app2 | True | 32472.0 | 10.5% | 10.7% | 0.1 |
| 70.0 | 80.0 | end-users | True | 209550.0 | 68.4% | 68.9% | 0.5 |
| 80.0 | 90.0 | app1 | True | 64904.0 | 21.1% | 21.1% | 0.0 |
| 80.0 | 90.0 | app2 | True | 32506.0 | 10.5% | 10.5% | 0.0 |
| 80.0 | 90.0 | end-users | True | 210816.0 | 68.4% | 68.4% | -0.0 |
| 90.0 | 101.0 | app1 | True | 63592.0 | 21.1% | 21.2% | 0.1 |
| 90.0 | 101.0 | app2 | True | 32400.0 | 10.5% | 10.8% | 0.3 |
| 90.0 | 101.0 | end-users | True | 204358.0 | 68.4% | 68.0% | -0.4 |
| 101.0 | 111.0 | app1 | True | 66282.0 | 21.1% | 21.7% | 0.6 |
| 101.0 | 111.0 | app2 | True | 32458.0 | 10.5% | 10.6% | 0.1 |
| 101.0 | 111.0 | end-users | True | 206924.0 | 68.4% | 67.7% | -0.7 |
| 111.0 | 121.0 | app1 | True | 63436.0 | 21.1% | 20.9% | -0.2 |
| 111.0 | 121.0 | app2 | True | 31026.0 | 10.5% | 10.2% | -0.3 |
| 111.0 | 121.0 | end-users | True | 209660.0 | 68.4% | 68.9% | 0.5 |
| 121.0 | 131.0 | app1 | True | 63456.0 | 21.1% | 20.6% | -0.5 |
| 121.0 | 131.0 | app2 | True | 33852.0 | 10.5% | 11.0% | 0.5 |
| 121.0 | 131.0 | end-users | True | 211050.0 | 68.4% | 68.4% | 0.0 |
| 131.0 | 141.0 | app1 | True | 64946.0 | 21.1% | 21.3% | 0.3 |
| 131.0 | 141.0 | app2 | True | 32450.0 | 10.5% | 10.7% | 0.1 |
| 131.0 | 141.0 | end-users | True | 206956.0 | 68.4% | 68.0% | -0.4 |
| 141.0 | 151.0 | app1 | True | 64868.0 | 21.1% | 21.2% | 0.2 |
| 141.0 | 151.0 | app2 | True | 29730.0 | 10.5% | 9.7% | -0.8 |
| 141.0 | 151.0 | end-users | True | 210988.0 | 68.4% | 69.0% | 0.6 |
| 151.0 | 161.0 | app1 | True | 62208.0 | 21.1% | 20.4% | -0.7 |
| 151.0 | 161.0 | app2 | True | 33790.0 | 10.5% | 11.1% | 0.5 |
| 151.0 | 161.0 | end-users | True | 209608.0 | 68.4% | 68.6% | 0.2 |
| 161.0 | 171.0 | app1 | True | 64902.0 | 21.1% | 21.2% | 0.2 |
| 161.0 | 171.0 | app2 | True | 32516.0 | 10.5% | 10.6% | 0.1 |
| 161.0 | 171.0 | end-users | True | 208346.0 | 68.4% | 68.1% | -0.3 |
| 171.0 | 181.0 | app1 | True | 64866.0 | 21.1% | 21.2% | 0.2 |
| 171.0 | 181.0 | app2 | True | 31092.0 | 10.5% | 10.2% | -0.3 |
| 171.0 | 181.0 | end-users | True | 209494.0 | 68.4% | 68.6% | 0.2 |
| 181.0 | 191.0 | app1 | True | 64950.0 | 21.1% | 21.2% | 0.1 |
| 181.0 | 191.0 | app2 | True | 33768.0 | 10.5% | 11.0% | 0.5 |
| 181.0 | 191.0 | end-users | True | 208306.0 | 68.4% | 67.8% | -0.6 |
| 191.0 | 201.0 | app1 | True | 64944.0 | 21.1% | 21.2% | 0.1 |
| 191.0 | 201.0 | app2 | True | 31102.0 | 10.5% | 10.1% | -0.4 |
| 191.0 | 201.0 | end-users | True | 210856.0 | 68.4% | 68.7% | 0.3 |
| 201.0 | 211.0 | app1 | True | 63654.0 | 21.1% | 20.8% | -0.2 |
| 201.0 | 211.0 | app2 | True | 30992.0 | 10.5% | 10.1% | -0.4 |
| 201.0 | 211.0 | end-users | True | 210868.0 | 68.4% | 69.0% | 0.6 |
| 211.0 | 221.0 | app1 | True | 65040.0 | 21.1% | 21.4% | 0.3 |
| 211.0 | 221.0 | app2 | True | 32360.0 | 10.5% | 10.6% | 0.1 |
| 211.0 | 221.0 | end-users | True | 207022.0 | 68.4% | 68.0% | -0.4 |
| 221.0 | 231.0 | app1 | True | 63572.0 | 21.1% | 20.7% | -0.3 |
| 221.0 | 231.0 | app2 | True | 32476.0 | 10.5% | 10.6% | 0.1 |
| 221.0 | 231.0 | end-users | True | 210802.0 | 68.4% | 68.7% | 0.3 |
| 231.0 | 241.0 | app1 | True | 64930.0 | 21.1% | 21.3% | 0.3 |
| 231.0 | 241.0 | app2 | True | 32500.0 | 10.5% | 10.7% | 0.2 |
| 231.0 | 241.0 | end-users | True | 206916.0 | 68.4% | 68.0% | -0.4 |
| 241.0 | 251.0 | app1 | False | 52744.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 47306.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 74464.0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 259.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 58 | 0ms | 467ms | 942ms |
| 0.0 | 10.0 | app2 | ok | 44 | 0ms | 475ms | 945ms |
| 0.0 | 10.0 | end-users | ok | 123 | 185ms | 824ms | 982ms |
| 10.0 | 20.0 | app1 | ok | 50 | 250ms | 750ms | 975ms |
| 10.0 | 20.0 | app2 | ok | 23 | 482ms | 895ms | 990ms |
| 10.0 | 20.0 | end-users | ok | 173 | 314ms | 816ms | 982ms |
| 20.0 | 30.0 | app1 | ok | 47 | 368ms | 832ms | 983ms |
| 20.0 | 30.0 | app2 | ok | 23 | 521ms | 904ms | 990ms |
| 20.0 | 30.0 | end-users | ok | 150 | 296ms | 786ms | 979ms |
| 30.0 | 40.0 | app1 | ok | 48 | 317ms | 815ms | 982ms |
| 30.0 | 40.0 | app2 | ok | 25 | 304ms | 821ms | 982ms |
| 30.0 | 40.0 | end-users | ok | 152 | 321ms | 789ms | 979ms |
| 40.0 | 50.0 | app1 | ok | 48 | 306ms | 859ms | 986ms |
| 40.0 | 50.0 | app2 | ok | 24 | 292ms | 829ms | 983ms |
| 40.0 | 50.0 | end-users | ok | 163 | 304ms | 796ms | 980ms |
| 50.0 | 60.0 | app1 | ok | 46 | 472ms | 895ms | 990ms |
| 50.0 | 60.0 | app2 | ok | 23 | 396ms | 872ms | 987ms |
| 50.0 | 60.0 | end-users | ok | 151 | 391ms | 870ms | 987ms |
| 60.0 | 70.0 | app1 | ok | 49 | 320ms | 812ms | 981ms |
| 60.0 | 70.0 | app2 | ok | 23 | 275ms | 836ms | 984ms |
| 60.0 | 70.0 | end-users | ok | 152 | 304ms | 810ms | 981ms |
| 70.0 | 80.0 | app1 | ok | 48 | 324ms | 800ms | 980ms |
| 70.0 | 80.0 | app2 | ok | 24 | 375ms | 850ms | 985ms |
| 70.0 | 80.0 | end-users | ok | 156 | 288ms | 800ms | 980ms |
| 80.0 | 90.0 | app1 | ok | 46 | 262ms | 492ms | 942ms |
| 80.0 | 90.0 | app2 | ok | 23 | 385ms | 808ms | 981ms |
| 80.0 | 90.0 | end-users | ok | 153 | 278ms | 768ms | 977ms |
| 90.0 | 101.0 | app1 | ok | 47 | 337ms | 843ms | 984ms |
| 90.0 | 101.0 | app2 | ok | 25 | 175ms | 484ms | 938ms |
| 90.0 | 101.0 | end-users | ok | 154 | 315ms | 821ms | 982ms |
| 101.0 | 111.0 | app1 | ok | 47 | 365ms | 862ms | 986ms |
| 101.0 | 111.0 | app2 | ok | 22 | 417ms | 890ms | 989ms |
| 101.0 | 111.0 | end-users | ok | 150 | 269ms | 712ms | 971ms |
| 111.0 | 121.0 | app1 | ok | 47 | 260ms | 804ms | 980ms |
| 111.0 | 121.0 | app2 | ok | 25 | 385ms | 821ms | 982ms |
| 111.0 | 121.0 | end-users | ok | 153 | 284ms | 781ms | 978ms |
| 121.0 | 131.0 | app1 | ok | 51 | 287ms | 768ms | 977ms |
| 121.0 | 131.0 | app2 | ok | 26 | 250ms | 870ms | 987ms |
| 121.0 | 131.0 | end-users | ok | 164 | 315ms | 818ms | 982ms |
| 131.0 | 141.0 | app1 | ok | 47 | 272ms | 706ms | 971ms |
| 131.0 | 141.0 | app2 | ok | 24 | 250ms | 829ms | 983ms |
| 131.0 | 141.0 | end-users | ok | 155 | 292ms | 828ms | 983ms |
| 141.0 | 151.0 | app1 | ok | 45 | 368ms | 827ms | 983ms |
| 141.0 | 151.0 | app2 | ok | 21 | 325ms | 850ms | 985ms |
| 141.0 | 151.0 | end-users | ok | 146 | 347ms | 841ms | 984ms |
| 151.0 | 161.0 | app1 | ok | 48 | 347ms | 815ms | 982ms |
| 151.0 | 161.0 | app2 | ok | 24 | 393ms | 867ms | 987ms |
| 151.0 | 161.0 | end-users | ok | 153 | 326ms | 841ms | 984ms |
| 161.0 | 171.0 | app1 | ok | 49 | 397ms | 837ms | 984ms |
| 161.0 | 171.0 | app2 | ok | 25 | 268ms | 792ms | 979ms |
| 161.0 | 171.0 | end-users | ok | 160 | 332ms | 795ms | 979ms |
| 171.0 | 181.0 | app1 | ok | 45 | 336ms | 812ms | 981ms |
| 171.0 | 181.0 | app2 | ok | 23 | 352ms | 770ms | 977ms |
| 171.0 | 181.0 | end-users | ok | 152 | 312ms | 795ms | 979ms |
| 181.0 | 191.0 | app1 | ok | 51 | 403ms | 884ms | 988ms |
| 181.0 | 191.0 | app2 | ok | 25 | 266ms | 750ms | 975ms |
| 181.0 | 191.0 | end-users | ok | 163 | 294ms | 840ms | 984ms |
| 191.0 | 201.0 | app1 | ok | 45 | 266ms | 850ms | 985ms |
| 191.0 | 201.0 | app2 | ok | 22 | 225ms | 862ms | 986ms |
| 191.0 | 201.0 | end-users | ok | 149 | 297ms | 804ms | 980ms |
| 201.0 | 211.0 | app1 | ok | 47 | 392ms | 862ms | 986ms |
| 201.0 | 211.0 | app2 | ok | 25 | 312ms | 844ms | 984ms |
| 201.0 | 211.0 | end-users | ok | 150 | 293ms | 817ms | 982ms |
| 211.0 | 221.0 | app1 | ok | 50 | 433ms | 881ms | 988ms |
| 211.0 | 221.0 | app2 | ok | 24 | 333ms | 850ms | 985ms |
| 211.0 | 221.0 | end-users | ok | 160 | 302ms | 810ms | 981ms |
| 221.0 | 231.0 | app1 | ok | 49 | 309ms | 755ms | 975ms |
| 221.0 | 231.0 | app2 | ok | 24 | 229ms | 800ms | 980ms |
| 221.0 | 231.0 | end-users | ok | 160 | 360ms | 846ms | 985ms |
| 231.0 | 241.0 | app1 | ok | 48 | 308ms | 829ms | 983ms |
| 231.0 | 241.0 | app2 | ok | 24 | 212ms | 700ms | 970ms |
| 231.0 | 241.0 | end-users | ok | 152 | 310ms | 783ms | 978ms |
| 241.0 | 251.0 | app1 | ok | 7 | 650ms | 930ms | 993ms |
| 241.0 | 251.0 | app2 | ok | 3 | 375ms | 850ms | 985ms |
| 241.0 | 251.0 | end-users | ok | 26 | 472ms | 892ms | 989ms |
| 251.0 | 259.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 259.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1430490 | 71196 | 1501686.0 | 0.0% | 1528238.0 | 1572882.0 | -2.8% | True |
| app2 | 730620 | 36225 | 766845.0 | 0.0% | 759836.0 | 803070.0 | -5.4% | True |
| end-users | 4575600 | 227735 | 4803335.0 | 0.0% | 4985092.0 | 5031070.0 | -0.9% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1163 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 594 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3720 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5477). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5477 | 0.053ms | 0.197ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 247223 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1163 | 6918ms | 7892ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 594 | 12367ms | 14811ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3720 | 1994ms | 2902ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5477 | 2459ms | 12579ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 3500ms | 6900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 3000ms | 6600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 1642ms | 2734ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 6977ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 10750ms | 17375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 1903ms | 2891ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 6932ms | 7893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 13472ms | 19107ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 1997ms | 2899ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 2043ms | 2904ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 2083ms | 2908ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 2019ms | 2902ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 6979ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 2049ms | 2905ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 6955ms | 7895ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 1983ms | 2897ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 6979ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 2013ms | 2901ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 101.0 | app1 | ok | 6825ms | 7882ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 101.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 101.0 | end-users | ok | 1966ms | 2947ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 6957ms | 7896ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 2056ms | 2906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 6978ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 1977ms | 2895ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 6978ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 2060ms | 2906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 6909ms | 7891ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 2056ms | 2906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 6957ms | 7896ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 2082ms | 2908ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 2006ms | 2901ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 6979ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 2105ms | 2910ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 6979ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 2055ms | 2905ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 2013ms | 2901ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 6979ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 2013ms | 2901ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 7000ms | 7900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 1981ms | 2896ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 6979ms | 7898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 2019ms | 2902ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 6956ms | 7896ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 1944ms | 2887ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 6769ms | 7877ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 1929ms | 2898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 6143ms | 7814ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 10625ms | 14562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 2141ms | 2914ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
