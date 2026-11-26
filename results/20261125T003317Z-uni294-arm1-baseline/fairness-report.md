# Fairness benchmark: equal-workers-control (uni294-arm1-baseline)

**Verdict: INFO** -- named negative control, not scored against the 10-point threshold. Expected to NOT reproduce the configured weights; see docs/runbook.md.
Worker-share vs. weight-share gap (UNI-225): 35.1 points

- negative control, not scored against the 10-point threshold: max deviation was 31.8 points. This scenario is expected to compress toward equal shares, not reproduce the configured weights -- see docs/runbook.md's 'Per-tenant worker sizing and the saturation check'

## Run metadata

| field | value |
|---|---|
| Scenario | `equal-workers-control` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:7e406c43a57fd444b8930d00d3d8423b48fbc743e9abaf32ca624e97b2f76df7` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5c94b46865-2l8p9` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-25T00:34:41Z` |
| Run end | `2026-11-25T00:39:00Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 27 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/27 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 38.50 | 1.2031 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1775 | 200=1775 | 4.3 | 4.9 | 2357776.0 | 21.1% | 33.3% | 12.3 | 32.4% | 11.4 | 32.4% | 11.4 | 2.8s | 98.9% | 1775.0 |
| app2 | 10.0 | 32 | 1696 | 200=1696 | 4.5 | 5.0 | 2249844.0 | 10.5% | 33.3% | 22.8 | 31.0% | 20.4 | 31.0% | 20.5 | 2.8s | 98.9% | 1696.0 |
| end-users | 65.0 | 32 | 2002 | 200=2002 | 3.8 | 4.5 | 2660184.0 | 68.4% | 33.3% | -35.1 | 36.6% | -31.8 | 36.6% | -31.8 | 1.5s | 98.9% | 2002.0 |
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
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 20270.0 | 21.1% | 26.8% | 5.7 |
| 0.0 | 10.0 | app2 | True | 20280.0 | 10.5% | 26.8% | 16.3 |
| 0.0 | 10.0 | end-users | True | 35110.0 | 68.4% | 46.4% | -22.0 |
| 10.0 | 20.0 | app1 | True | 101424.0 | 21.1% | 32.8% | 11.7 |
| 10.0 | 20.0 | app2 | True | 94622.0 | 10.5% | 30.6% | 20.0 |
| 10.0 | 20.0 | end-users | True | 113576.0 | 68.4% | 36.7% | -31.7 |
| 20.0 | 30.0 | app1 | True | 98732.0 | 21.1% | 32.3% | 11.2 |
| 20.0 | 30.0 | app2 | True | 100162.0 | 10.5% | 32.7% | 22.2 |
| 20.0 | 30.0 | end-users | True | 106988.0 | 68.4% | 35.0% | -33.4 |
| 30.0 | 40.0 | app1 | True | 97534.0 | 21.1% | 31.8% | 10.7 |
| 30.0 | 40.0 | app2 | True | 89270.0 | 10.5% | 29.1% | 18.5 |
| 30.0 | 40.0 | end-users | True | 120348.0 | 68.4% | 39.2% | -29.2 |
| 40.0 | 51.0 | app1 | True | 96030.0 | 21.1% | 31.8% | 10.8 |
| 40.0 | 51.0 | app2 | True | 100056.0 | 10.5% | 33.2% | 22.6 |
| 40.0 | 51.0 | end-users | True | 105568.0 | 68.4% | 35.0% | -33.4 |
| 51.0 | 61.0 | app1 | True | 97276.0 | 21.1% | 31.6% | 10.5 |
| 51.0 | 61.0 | app2 | True | 94480.0 | 10.5% | 30.7% | 20.1 |
| 51.0 | 61.0 | end-users | True | 116474.0 | 68.4% | 37.8% | -30.6 |
| 61.0 | 71.0 | app1 | True | 101364.0 | 21.1% | 32.6% | 11.6 |
| 61.0 | 71.0 | app2 | True | 94514.0 | 10.5% | 30.4% | 19.9 |
| 61.0 | 71.0 | end-users | True | 114974.0 | 68.4% | 37.0% | -31.4 |
| 71.0 | 81.0 | app1 | True | 101414.0 | 21.1% | 33.0% | 12.0 |
| 71.0 | 81.0 | app2 | True | 93374.0 | 10.5% | 30.4% | 19.9 |
| 71.0 | 81.0 | end-users | True | 112184.0 | 68.4% | 36.5% | -31.9 |
| 81.0 | 91.0 | app1 | True | 93458.0 | 21.1% | 31.1% | 10.1 |
| 81.0 | 91.0 | app2 | True | 93304.0 | 10.5% | 31.1% | 20.5 |
| 81.0 | 91.0 | end-users | True | 113672.0 | 68.4% | 37.8% | -30.6 |
| 91.0 | 101.0 | app1 | True | 97418.0 | 21.1% | 31.9% | 10.8 |
| 91.0 | 101.0 | app2 | True | 97296.0 | 10.5% | 31.8% | 21.3 |
| 91.0 | 101.0 | end-users | True | 110938.0 | 68.4% | 36.3% | -32.1 |
| 101.0 | 111.0 | app1 | True | 100204.0 | 21.1% | 33.2% | 12.1 |
| 101.0 | 111.0 | app2 | True | 89292.0 | 10.5% | 29.6% | 19.1 |
| 101.0 | 111.0 | end-users | True | 112360.0 | 68.4% | 37.2% | -31.2 |
| 111.0 | 121.0 | app1 | True | 104140.0 | 21.1% | 34.2% | 13.2 |
| 111.0 | 121.0 | app2 | True | 90674.0 | 10.5% | 29.8% | 19.3 |
| 111.0 | 121.0 | end-users | True | 109624.0 | 68.4% | 36.0% | -32.4 |
| 121.0 | 131.0 | app1 | True | 95954.0 | 21.1% | 31.6% | 10.5 |
| 121.0 | 131.0 | app2 | True | 95916.0 | 10.5% | 31.5% | 21.0 |
| 121.0 | 131.0 | end-users | True | 112230.0 | 68.4% | 36.9% | -31.5 |
| 131.0 | 141.0 | app1 | True | 98740.0 | 21.1% | 32.2% | 11.1 |
| 131.0 | 141.0 | app2 | True | 97312.0 | 10.5% | 31.7% | 21.2 |
| 131.0 | 141.0 | end-users | True | 110876.0 | 68.4% | 36.1% | -32.3 |
| 141.0 | 151.0 | app1 | True | 101378.0 | 21.1% | 33.0% | 12.0 |
| 141.0 | 151.0 | app2 | True | 93344.0 | 10.5% | 30.4% | 19.9 |
| 141.0 | 151.0 | end-users | True | 112286.0 | 68.4% | 36.6% | -31.8 |
| 151.0 | 161.0 | app1 | True | 96076.0 | 21.1% | 31.6% | 10.5 |
| 151.0 | 161.0 | app2 | True | 93110.0 | 10.5% | 30.6% | 20.1 |
| 151.0 | 161.0 | end-users | True | 115090.0 | 68.4% | 37.8% | -30.6 |
| 161.0 | 171.0 | app1 | True | 105492.0 | 21.1% | 34.8% | 13.8 |
| 161.0 | 171.0 | app2 | True | 96120.0 | 10.5% | 31.7% | 21.2 |
| 161.0 | 171.0 | end-users | True | 101282.0 | 68.4% | 33.4% | -35.0 |
| 171.0 | 181.0 | app1 | True | 94654.0 | 21.1% | 30.7% | 9.7 |
| 171.0 | 181.0 | app2 | True | 105536.0 | 10.5% | 34.2% | 23.7 |
| 171.0 | 181.0 | end-users | True | 107974.0 | 68.4% | 35.0% | -33.4 |
| 181.0 | 191.0 | app1 | True | 94712.0 | 21.1% | 30.7% | 9.7 |
| 181.0 | 191.0 | app2 | True | 91948.0 | 10.5% | 29.8% | 19.3 |
| 181.0 | 191.0 | end-users | True | 121746.0 | 68.4% | 39.5% | -28.9 |
| 191.0 | 201.0 | app1 | True | 112412.0 | 21.1% | 37.3% | 16.2 |
| 191.0 | 201.0 | app2 | True | 86528.0 | 10.5% | 28.7% | 18.2 |
| 191.0 | 201.0 | end-users | True | 102690.0 | 68.4% | 34.0% | -34.4 |
| 201.0 | 211.0 | app1 | True | 97324.0 | 21.1% | 31.9% | 10.8 |
| 201.0 | 211.0 | app2 | True | 94746.0 | 10.5% | 31.0% | 20.5 |
| 201.0 | 211.0 | end-users | True | 113474.0 | 68.4% | 37.1% | -31.3 |
| 211.0 | 221.0 | app1 | True | 97444.0 | 21.1% | 31.8% | 10.7 |
| 211.0 | 221.0 | app2 | True | 97282.0 | 10.5% | 31.7% | 21.2 |
| 211.0 | 221.0 | end-users | True | 112130.0 | 68.4% | 36.5% | -31.9 |
| 221.0 | 231.0 | app1 | True | 98698.0 | 21.1% | 32.2% | 11.1 |
| 221.0 | 231.0 | app2 | True | 94678.0 | 10.5% | 30.8% | 20.3 |
| 221.0 | 231.0 | end-users | True | 113598.0 | 68.4% | 37.0% | -31.4 |
| 231.0 | 241.0 | app1 | True | 104216.0 | 21.1% | 34.1% | 13.0 |
| 231.0 | 241.0 | app2 | True | 89272.0 | 10.5% | 29.2% | 18.7 |
| 231.0 | 241.0 | end-users | True | 112278.0 | 68.4% | 36.7% | -31.7 |
| 241.0 | 251.0 | app1 | False | 51412.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 56728.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 52714.0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 259.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 72 | 0ms | 775ms | 978ms |
| 0.0 | 10.0 | app2 | ok | 78 | 5ms | 740ms | 974ms |
| 0.0 | 10.0 | end-users | ok | 83 | 0ms | 782ms | 978ms |
| 10.0 | 20.0 | app1 | ok | 82 | 312ms | 795ms | 979ms |
| 10.0 | 20.0 | app2 | ok | 71 | 349ms | 852ms | 985ms |
| 10.0 | 20.0 | end-users | ok | 90 | 310ms | 804ms | 980ms |
| 20.0 | 30.0 | app1 | ok | 73 | 325ms | 860ms | 986ms |
| 20.0 | 30.0 | app2 | ok | 72 | 269ms | 850ms | 985ms |
| 20.0 | 30.0 | end-users | ok | 81 | 336ms | 855ms | 986ms |
| 30.0 | 40.0 | app1 | ok | 71 | 351ms | 822ms | 982ms |
| 30.0 | 40.0 | app2 | ok | 68 | 402ms | 864ms | 986ms |
| 30.0 | 40.0 | end-users | ok | 86 | 259ms | 713ms | 971ms |
| 40.0 | 51.0 | app1 | ok | 71 | 297ms | 704ms | 970ms |
| 40.0 | 51.0 | app2 | ok | 72 | 312ms | 829ms | 983ms |
| 40.0 | 51.0 | end-users | ok | 81 | 337ms | 873ms | 987ms |
| 51.0 | 61.0 | app1 | ok | 68 | 308ms | 757ms | 976ms |
| 51.0 | 61.0 | app2 | ok | 69 | 375ms | 828ms | 983ms |
| 51.0 | 61.0 | end-users | ok | 84 | 318ms | 767ms | 977ms |
| 61.0 | 71.0 | app1 | ok | 79 | 317ms | 792ms | 979ms |
| 61.0 | 71.0 | app2 | ok | 68 | 333ms | 788ms | 979ms |
| 61.0 | 71.0 | end-users | ok | 79 | 312ms | 803ms | 980ms |
| 71.0 | 81.0 | app1 | ok | 68 | 321ms | 821ms | 982ms |
| 71.0 | 81.0 | app2 | ok | 69 | 375ms | 818ms | 982ms |
| 71.0 | 81.0 | end-users | ok | 89 | 273ms | 778ms | 978ms |
| 81.0 | 91.0 | app1 | ok | 77 | 292ms | 759ms | 976ms |
| 81.0 | 91.0 | app2 | ok | 74 | 375ms | 846ms | 985ms |
| 81.0 | 91.0 | end-users | ok | 85 | 230ms | 764ms | 976ms |
| 91.0 | 101.0 | app1 | ok | 72 | 375ms | 811ms | 981ms |
| 91.0 | 101.0 | app2 | ok | 69 | 360ms | 862ms | 986ms |
| 91.0 | 101.0 | end-users | ok | 81 | 255ms | 775ms | 977ms |
| 101.0 | 111.0 | app1 | ok | 72 | 357ms | 820ms | 982ms |
| 101.0 | 111.0 | app2 | ok | 67 | 280ms | 777ms | 978ms |
| 101.0 | 111.0 | end-users | ok | 84 | 269ms | 753ms | 975ms |
| 111.0 | 121.0 | app1 | ok | 71 | 353ms | 813ms | 981ms |
| 111.0 | 121.0 | app2 | ok | 68 | 382ms | 864ms | 986ms |
| 111.0 | 121.0 | end-users | ok | 77 | 351ms | 807ms | 981ms |
| 121.0 | 131.0 | app1 | ok | 78 | 397ms | 856ms | 986ms |
| 121.0 | 131.0 | app2 | ok | 72 | 272ms | 760ms | 976ms |
| 121.0 | 131.0 | end-users | ok | 86 | 306ms | 774ms | 977ms |
| 131.0 | 141.0 | app1 | ok | 70 | 370ms | 841ms | 984ms |
| 131.0 | 141.0 | app2 | ok | 64 | 265ms | 800ms | 980ms |
| 131.0 | 141.0 | end-users | ok | 83 | 343ms | 756ms | 976ms |
| 141.0 | 151.0 | app1 | ok | 71 | 355ms | 831ms | 983ms |
| 141.0 | 151.0 | app2 | ok | 77 | 375ms | 852ms | 985ms |
| 141.0 | 151.0 | end-users | ok | 75 | 290ms | 803ms | 980ms |
| 151.0 | 161.0 | app1 | ok | 78 | 350ms | 814ms | 981ms |
| 151.0 | 161.0 | app2 | ok | 69 | 323ms | 754ms | 975ms |
| 151.0 | 161.0 | end-users | ok | 93 | 349ms | 821ms | 982ms |
| 161.0 | 171.0 | app1 | ok | 76 | 362ms | 827ms | 983ms |
| 161.0 | 171.0 | app2 | ok | 62 | 325ms | 818ms | 982ms |
| 161.0 | 171.0 | end-users | ok | 73 | 267ms | 772ms | 977ms |
| 171.0 | 181.0 | app1 | ok | 73 | 310ms | 719ms | 972ms |
| 171.0 | 181.0 | app2 | ok | 85 | 321ms | 837ms | 984ms |
| 171.0 | 181.0 | end-users | ok | 84 | 274ms | 817ms | 982ms |
| 181.0 | 191.0 | app1 | ok | 69 | 284ms | 862ms | 986ms |
| 181.0 | 191.0 | app2 | ok | 70 | 308ms | 767ms | 977ms |
| 181.0 | 191.0 | end-users | ok | 89 | 293ms | 807ms | 981ms |
| 191.0 | 201.0 | app1 | ok | 71 | 342ms | 831ms | 983ms |
| 191.0 | 201.0 | app2 | ok | 64 | 337ms | 812ms | 981ms |
| 191.0 | 201.0 | end-users | ok | 73 | 387ms | 865ms | 986ms |
| 201.0 | 211.0 | app1 | ok | 85 | 284ms | 788ms | 979ms |
| 201.0 | 211.0 | app2 | ok | 70 | 272ms | 750ms | 975ms |
| 201.0 | 211.0 | end-users | ok | 87 | 302ms | 771ms | 977ms |
| 211.0 | 221.0 | app1 | ok | 71 | 366ms | 873ms | 987ms |
| 211.0 | 221.0 | app2 | ok | 71 | 414ms | 882ms | 988ms |
| 211.0 | 221.0 | end-users | ok | 84 | 352ms | 838ms | 984ms |
| 221.0 | 231.0 | app1 | ok | 72 | 304ms | 800ms | 980ms |
| 221.0 | 231.0 | app2 | ok | 68 | 365ms | 830ms | 983ms |
| 221.0 | 231.0 | end-users | ok | 81 | 273ms | 747ms | 975ms |
| 231.0 | 241.0 | app1 | ok | 76 | 333ms | 864ms | 986ms |
| 231.0 | 241.0 | app2 | ok | 68 | 371ms | 821ms | 982ms |
| 231.0 | 241.0 | end-users | ok | 84 | 343ms | 832ms | 983ms |
| 241.0 | 251.0 | app1 | ok | 9 | 312ms | 850ms | 985ms |
| 241.0 | 251.0 | app2 | ok | 11 | 458ms | 890ms | 989ms |
| 241.0 | 251.0 | end-users | ok | 10 | 400ms | 833ms | 983ms |
| 251.0 | 259.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 259.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2183250 | 108906 | 2292156.0 | 0.0% | 2357776.0 | 2401062.0 | -1.8% | True |
| app2 | 2086080 | 103547 | 2189627.0 | 0.0% | 2249844.0 | 2293174.0 | -1.9% | True |
| end-users | 2462460 | 122522 | 2584982.0 | 0.0% | 2660184.0 | 2707504.0 | -1.7% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1775 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1696 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2002 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5473). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5473 | 0.053ms | 0.193ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 247052 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1775 | 4390ms | 4951ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1696 | 4485ms | 4972ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 2002 | 3712ms | 4838ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5473 | 4258ms | 4941ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 3346ms | 5530ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 3227ms | 5217ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2875ms | 4262ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 4385ms | 4939ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 4493ms | 4949ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 3636ms | 4767ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 4411ms | 4941ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 4500ms | 4962ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 3627ms | 4753ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 4424ms | 4973ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 4475ms | 4978ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 3781ms | 4861ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 51.0 | app1 | ok | 4370ms | 5113ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 51.0 | app2 | ok | 4479ms | 4948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 51.0 | end-users | ok | 4049ms | 4905ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app1 | ok | 4352ms | 4952ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app2 | ok | 4444ms | 4944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | end-users | ok | 3837ms | 4877ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app1 | ok | 4449ms | 4945ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app2 | ok | 4478ms | 4948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | end-users | ok | 3728ms | 4843ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app1 | ok | 4342ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app2 | ok | 4507ms | 4964ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | end-users | ok | 3728ms | 4840ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 4458ms | 4976ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app2 | ok | 4485ms | 4949ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 3952ms | 4895ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 4419ms | 4942ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 4500ms | 4976ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 3804ms | 4868ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 4448ms | 4945ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 4541ms | 5340ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 3724ms | 4838ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 4450ms | 4945ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 4508ms | 4964ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 3690ms | 4818ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 4398ms | 4940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 4522ms | 4992ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 3561ms | 4539ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 4471ms | 4947ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 4514ms | 4977ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 3603ms | 4707ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 4306ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 4452ms | 5425ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 3964ms | 4896ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 4434ms | 4958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 4500ms | 4950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 3664ms | 4798ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 4328ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 4492ms | 5113ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 3809ms | 4869ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 4424ms | 4958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 4480ms | 4948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 3925ms | 4892ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 4426ms | 4943ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 4500ms | 4950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 3643ms | 4775ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 4259ms | 4926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 4525ms | 4997ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 3704ms | 4827ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 4390ms | 4939ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 4507ms | 4964ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 3802ms | 4867ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 4410ms | 4941ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 4493ms | 4949ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 3638ms | 4769ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 4368ms | 4988ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 4492ms | 5300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 3690ms | 4861ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 4398ms | 4940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 4508ms | 4965ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 3593ms | 4681ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 4367ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 4429ms | 4969ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 3886ms | 4885ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
