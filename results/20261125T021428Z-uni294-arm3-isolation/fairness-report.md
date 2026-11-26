# Fairness benchmark: equal-workers-control (uni294-arm3-isolation)

**Verdict: INFO** -- named negative control, not scored against the 10-point threshold. Expected to NOT reproduce the configured weights; see docs/runbook.md.
Worker-share vs. weight-share gap (UNI-225): 35.1 points

- negative control, not scored against the 10-point threshold: max deviation was 32.5 points. This scenario is expected to compress toward equal shares, not reproduce the configured weights -- see docs/runbook.md's 'Per-tenant worker sizing and the saturation check'

## Run metadata

| field | value |
|---|---|
| Scenario | `equal-workers-control` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:7e406c43a57fd444b8930d00d3d8423b48fbc743e9abaf32ca624e97b2f76df7` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-576d856b9-8mt5n` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-25T02:15:56Z` |
| Run end | `2026-11-25T02:20:15Z` |

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
| app1 | 20.0 | 32 | 1793 | 200=1793 | 4.3 | 4.9 | 2382692.0 | 21.1% | 33.3% | 12.3 | 33.1% | 12.1 | 33.1% | 12.0 | 3.4s | 98.9% | 1793.0 |
| app2 | 10.0 | 32 | 1676 | 200=1676 | 4.6 | 5.0 | 2225074.0 | 10.5% | 33.3% | 22.8 | 30.9% | 20.4 | 30.9% | 20.4 | 3.3s | 98.9% | 1676.0 |
| end-users | 65.0 | 32 | 1949 | 200=1949 | 4.0 | 4.6 | 2587206.0 | 68.4% | 33.3% | -35.1 | 36.0% | -32.5 | 36.0% | -32.4 | 2.4s | 98.8% | 1949.0 |
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
| 0.0 | 10.0 | app1 | True | 16228.0 | 21.1% | 29.3% | 8.2 |
| 0.0 | 10.0 | app2 | True | 13538.0 | 10.5% | 24.4% | 13.9 |
| 0.0 | 10.0 | end-users | True | 25648.0 | 68.4% | 46.3% | -22.1 |
| 10.0 | 20.0 | app1 | True | 100246.0 | 21.1% | 32.9% | 11.9 |
| 10.0 | 20.0 | app2 | True | 96068.0 | 10.5% | 31.5% | 21.0 |
| 10.0 | 20.0 | end-users | True | 108202.0 | 68.4% | 35.5% | -32.9 |
| 20.0 | 30.0 | app1 | True | 100086.0 | 21.1% | 32.7% | 11.7 |
| 20.0 | 30.0 | app2 | True | 96016.0 | 10.5% | 31.4% | 20.9 |
| 20.0 | 30.0 | end-users | True | 109682.0 | 68.4% | 35.9% | -32.6 |
| 30.0 | 40.0 | app1 | True | 100146.0 | 21.1% | 32.7% | 11.7 |
| 30.0 | 40.0 | app2 | True | 94790.0 | 10.5% | 31.0% | 20.5 |
| 30.0 | 40.0 | end-users | True | 110888.0 | 68.4% | 36.3% | -32.2 |
| 40.0 | 50.0 | app1 | True | 104026.0 | 21.1% | 33.9% | 12.8 |
| 40.0 | 50.0 | app2 | True | 92128.0 | 10.5% | 30.0% | 19.5 |
| 40.0 | 50.0 | end-users | True | 110998.0 | 68.4% | 36.1% | -32.3 |
| 50.0 | 60.0 | app1 | True | 109400.0 | 21.1% | 35.3% | 14.3 |
| 50.0 | 60.0 | app2 | True | 93396.0 | 10.5% | 30.2% | 19.6 |
| 50.0 | 60.0 | end-users | True | 106776.0 | 68.4% | 34.5% | -33.9 |
| 60.0 | 70.0 | app1 | True | 94600.0 | 21.1% | 31.4% | 10.3 |
| 60.0 | 70.0 | app2 | True | 96120.0 | 10.5% | 31.9% | 21.3 |
| 60.0 | 70.0 | end-users | True | 111018.0 | 68.4% | 36.8% | -31.6 |
| 70.0 | 80.0 | app1 | True | 102892.0 | 21.1% | 33.8% | 12.7 |
| 70.0 | 80.0 | app2 | True | 93390.0 | 10.5% | 30.7% | 20.1 |
| 70.0 | 80.0 | end-users | True | 108228.0 | 68.4% | 35.5% | -32.9 |
| 80.0 | 90.0 | app1 | True | 98916.0 | 21.1% | 32.7% | 11.7 |
| 80.0 | 90.0 | app2 | True | 96176.0 | 10.5% | 31.8% | 21.3 |
| 80.0 | 90.0 | end-users | True | 106952.0 | 68.4% | 35.4% | -33.0 |
| 90.0 | 100.0 | app1 | True | 98756.0 | 21.1% | 32.7% | 11.7 |
| 90.0 | 100.0 | app2 | True | 88012.0 | 10.5% | 29.2% | 18.6 |
| 90.0 | 100.0 | end-users | True | 115052.0 | 68.4% | 38.1% | -30.3 |
| 100.0 | 110.0 | app1 | True | 94600.0 | 21.1% | 30.8% | 9.8 |
| 100.0 | 110.0 | app2 | True | 104156.0 | 10.5% | 33.9% | 23.4 |
| 100.0 | 110.0 | end-users | True | 108150.0 | 68.4% | 35.2% | -33.2 |
| 110.0 | 120.0 | app1 | True | 98856.0 | 21.1% | 32.9% | 11.8 |
| 110.0 | 120.0 | app2 | True | 87962.0 | 10.5% | 29.3% | 18.7 |
| 110.0 | 120.0 | end-users | True | 113796.0 | 68.4% | 37.9% | -30.6 |
| 120.0 | 130.0 | app1 | True | 108178.0 | 21.1% | 35.4% | 14.3 |
| 120.0 | 130.0 | app2 | True | 93364.0 | 10.5% | 30.5% | 20.0 |
| 120.0 | 130.0 | end-users | True | 104212.0 | 68.4% | 34.1% | -34.3 |
| 130.0 | 141.0 | app1 | True | 101468.0 | 21.1% | 33.5% | 12.4 |
| 130.0 | 141.0 | app2 | True | 86556.0 | 10.5% | 28.6% | 18.0 |
| 130.0 | 141.0 | end-users | True | 114988.0 | 68.4% | 37.9% | -30.5 |
| 141.0 | 151.0 | app1 | True | 102908.0 | 21.1% | 33.5% | 12.4 |
| 141.0 | 151.0 | app2 | True | 102882.0 | 10.5% | 33.5% | 23.0 |
| 141.0 | 151.0 | end-users | True | 101486.0 | 68.4% | 33.0% | -35.4 |
| 151.0 | 161.0 | app1 | True | 96140.0 | 21.1% | 32.0% | 10.9 |
| 151.0 | 161.0 | app2 | True | 100212.0 | 10.5% | 33.3% | 22.8 |
| 151.0 | 161.0 | end-users | True | 104172.0 | 68.4% | 34.7% | -33.8 |
| 161.0 | 171.0 | app1 | True | 96186.0 | 21.1% | 31.9% | 10.8 |
| 161.0 | 171.0 | app2 | True | 90698.0 | 10.5% | 30.0% | 19.5 |
| 161.0 | 171.0 | end-users | True | 115072.0 | 68.4% | 38.1% | -30.3 |
| 171.0 | 181.0 | app1 | True | 109606.0 | 21.1% | 36.2% | 15.1 |
| 171.0 | 181.0 | app2 | True | 87962.0 | 10.5% | 29.0% | 18.5 |
| 171.0 | 181.0 | end-users | True | 105620.0 | 68.4% | 34.8% | -33.6 |
| 181.0 | 191.0 | app1 | True | 101532.0 | 21.1% | 33.5% | 12.5 |
| 181.0 | 191.0 | app2 | True | 92040.0 | 10.5% | 30.4% | 19.8 |
| 181.0 | 191.0 | end-users | True | 109448.0 | 68.4% | 36.1% | -32.3 |
| 191.0 | 201.0 | app1 | True | 104116.0 | 21.1% | 33.9% | 12.8 |
| 191.0 | 201.0 | app2 | True | 94768.0 | 10.5% | 30.9% | 20.3 |
| 191.0 | 201.0 | end-users | True | 108220.0 | 68.4% | 35.2% | -33.2 |
| 201.0 | 211.0 | app1 | True | 96058.0 | 21.1% | 31.3% | 10.2 |
| 201.0 | 211.0 | app2 | True | 106780.0 | 10.5% | 34.8% | 24.3 |
| 201.0 | 211.0 | end-users | True | 104108.0 | 68.4% | 33.9% | -34.5 |
| 211.0 | 221.0 | app1 | True | 97494.0 | 21.1% | 32.4% | 11.4 |
| 211.0 | 221.0 | app2 | True | 86686.0 | 10.5% | 28.8% | 18.3 |
| 211.0 | 221.0 | end-users | True | 116376.0 | 68.4% | 38.7% | -29.7 |
| 221.0 | 231.0 | app1 | True | 105630.0 | 21.1% | 34.7% | 13.6 |
| 221.0 | 231.0 | app2 | True | 92046.0 | 10.5% | 30.2% | 19.7 |
| 221.0 | 231.0 | end-users | True | 107034.0 | 68.4% | 35.1% | -33.3 |
| 231.0 | 241.0 | app1 | True | 95996.0 | 21.1% | 31.7% | 10.6 |
| 231.0 | 241.0 | app2 | True | 91996.0 | 10.5% | 30.4% | 19.8 |
| 231.0 | 241.0 | end-users | True | 115086.0 | 68.4% | 38.0% | -30.4 |
| 241.0 | 251.0 | app1 | False | 48628.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 47332.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 45994.0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 259.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 73 | 0ms | 739ms | 974ms |
| 0.0 | 10.0 | app2 | ok | 70 | 0ms | 682ms | 968ms |
| 0.0 | 10.0 | end-users | ok | 85 | 0ms | 717ms | 972ms |
| 10.0 | 20.0 | app1 | ok | 76 | 441ms | 888ms | 989ms |
| 10.0 | 20.0 | app2 | ok | 73 | 340ms | 854ms | 985ms |
| 10.0 | 20.0 | end-users | ok | 83 | 375ms | 852ms | 985ms |
| 20.0 | 30.0 | app1 | ok | 73 | 228ms | 719ms | 972ms |
| 20.0 | 30.0 | app2 | ok | 71 | 315ms | 791ms | 979ms |
| 20.0 | 30.0 | end-users | ok | 79 | 346ms | 812ms | 981ms |
| 30.0 | 40.0 | app1 | ok | 72 | 312ms | 829ms | 983ms |
| 30.0 | 40.0 | app2 | ok | 72 | 269ms | 700ms | 970ms |
| 30.0 | 40.0 | end-users | ok | 82 | 286ms | 759ms | 976ms |
| 40.0 | 50.0 | app1 | ok | 80 | 361ms | 840ms | 984ms |
| 40.0 | 50.0 | app2 | ok | 63 | 327ms | 815ms | 981ms |
| 40.0 | 50.0 | end-users | ok | 80 | 375ms | 826ms | 983ms |
| 50.0 | 60.0 | app1 | ok | 73 | 295ms | 772ms | 977ms |
| 50.0 | 60.0 | app2 | ok | 71 | 392ms | 863ms | 986ms |
| 50.0 | 60.0 | end-users | ok | 79 | 329ms | 792ms | 979ms |
| 60.0 | 70.0 | app1 | ok | 74 | 289ms | 824ms | 982ms |
| 60.0 | 70.0 | app2 | ok | 67 | 273ms | 824ms | 982ms |
| 60.0 | 70.0 | end-users | ok | 83 | 278ms | 811ms | 981ms |
| 70.0 | 80.0 | app1 | ok | 76 | 263ms | 810ms | 981ms |
| 70.0 | 80.0 | app2 | ok | 71 | 355ms | 831ms | 983ms |
| 70.0 | 80.0 | end-users | ok | 77 | 308ms | 774ms | 977ms |
| 80.0 | 90.0 | app1 | ok | 75 | 307ms | 688ms | 969ms |
| 80.0 | 90.0 | app2 | ok | 72 | 375ms | 843ms | 984ms |
| 80.0 | 90.0 | end-users | ok | 79 | 382ms | 873ms | 987ms |
| 90.0 | 100.0 | app1 | ok | 72 | 300ms | 820ms | 982ms |
| 90.0 | 100.0 | app2 | ok | 68 | 386ms | 858ms | 986ms |
| 90.0 | 100.0 | end-users | ok | 84 | 284ms | 753ms | 975ms |
| 100.0 | 110.0 | app1 | ok | 74 | 271ms | 753ms | 975ms |
| 100.0 | 110.0 | app2 | ok | 78 | 307ms | 675ms | 968ms |
| 100.0 | 110.0 | end-users | ok | 87 | 231ms | 811ms | 981ms |
| 110.0 | 120.0 | app1 | ok | 69 | 335ms | 808ms | 981ms |
| 110.0 | 120.0 | app2 | ok | 65 | 424ms | 880ms | 988ms |
| 110.0 | 120.0 | end-users | ok | 75 | 332ms | 812ms | 981ms |
| 120.0 | 130.0 | app1 | ok | 81 | 265ms | 762ms | 976ms |
| 120.0 | 130.0 | app2 | ok | 65 | 325ms | 852ms | 985ms |
| 120.0 | 130.0 | end-users | ok | 85 | 292ms | 858ms | 986ms |
| 130.0 | 141.0 | app1 | ok | 74 | 264ms | 815ms | 982ms |
| 130.0 | 141.0 | app2 | ok | 68 | 357ms | 869ms | 987ms |
| 130.0 | 141.0 | end-users | ok | 82 | 321ms | 842ms | 984ms |
| 141.0 | 151.0 | app1 | ok | 72 | 356ms | 829ms | 983ms |
| 141.0 | 151.0 | app2 | ok | 70 | 325ms | 833ms | 983ms |
| 141.0 | 151.0 | end-users | ok | 75 | 355ms | 837ms | 984ms |
| 151.0 | 161.0 | app1 | ok | 79 | 379ms | 848ms | 985ms |
| 151.0 | 161.0 | app2 | ok | 76 | 250ms | 763ms | 976ms |
| 151.0 | 161.0 | end-users | ok | 79 | 280ms | 812ms | 981ms |
| 161.0 | 171.0 | app1 | ok | 70 | 385ms | 854ms | 985ms |
| 161.0 | 171.0 | app2 | ok | 71 | 384ms | 878ms | 988ms |
| 161.0 | 171.0 | end-users | ok | 85 | 358ms | 858ms | 986ms |
| 171.0 | 181.0 | app1 | ok | 82 | 380ms | 863ms | 986ms |
| 171.0 | 181.0 | app2 | ok | 65 | 292ms | 675ms | 967ms |
| 171.0 | 181.0 | end-users | ok | 78 | 356ms | 838ms | 984ms |
| 181.0 | 191.0 | app1 | ok | 70 | 298ms | 806ms | 981ms |
| 181.0 | 191.0 | app2 | ok | 68 | 350ms | 845ms | 985ms |
| 181.0 | 191.0 | end-users | ok | 81 | 338ms | 807ms | 981ms |
| 191.0 | 201.0 | app1 | ok | 79 | 326ms | 803ms | 980ms |
| 191.0 | 201.0 | app2 | ok | 69 | 257ms | 784ms | 978ms |
| 191.0 | 201.0 | end-users | ok | 77 | 327ms | 743ms | 974ms |
| 201.0 | 211.0 | app1 | ok | 73 | 288ms | 785ms | 979ms |
| 201.0 | 211.0 | app2 | ok | 71 | 347ms | 839ms | 984ms |
| 201.0 | 211.0 | end-users | ok | 81 | 310ms | 798ms | 980ms |
| 211.0 | 221.0 | app1 | ok | 69 | 293ms | 735ms | 973ms |
| 211.0 | 221.0 | app2 | ok | 73 | 467ms | 893ms | 989ms |
| 211.0 | 221.0 | end-users | ok | 84 | 284ms | 817ms | 982ms |
| 221.0 | 231.0 | app1 | ok | 80 | 370ms | 846ms | 985ms |
| 221.0 | 231.0 | app2 | ok | 67 | 348ms | 866ms | 987ms |
| 221.0 | 231.0 | end-users | ok | 82 | 347ms | 814ms | 981ms |
| 231.0 | 241.0 | app1 | ok | 71 | 375ms | 885ms | 989ms |
| 231.0 | 241.0 | app2 | ok | 69 | 424ms | 881ms | 988ms |
| 231.0 | 241.0 | end-users | ok | 80 | 297ms | 852ms | 985ms |
| 241.0 | 251.0 | app1 | ok | 6 | 375ms | 850ms | 985ms |
| 241.0 | 251.0 | app2 | ok | 3 | 175ms | 425ms | 492ms |
| 241.0 | 251.0 | end-users | ok | 7 | 650ms | 930ms | 993ms |
| 251.0 | 259.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 259.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2205390 | 110310 | 2315700.0 | 0.0% | 2382692.0 | 2426010.0 | -1.8% | True |
| app2 | 2061480 | 103427 | 2164907.0 | 0.0% | 2225074.0 | 2268334.0 | -1.9% | True |
| end-users | 2397270 | 120013 | 2517283.0 | 0.0% | 2587206.0 | 2637296.0 | -1.9% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1793 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1676 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1949 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5418). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5418 | 0.053ms | 0.213ms | (0, 0.1]ms | (0.2, 0.5]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 245664 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1793 | 4321ms | 4943ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1676 | 4492ms | 4981ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 1949 | 3881ms | 4886ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5418 | 4284ms | 4946ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 3182ms | 4900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2700ms | 4700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2722ms | 4312ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 4339ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 4500ms | 4950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 3698ms | 4824ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 4373ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 4500ms | 4950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 3844ms | 4877ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 4245ms | 4924ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 4500ms | 4977ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 3683ms | 4814ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 4358ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 4515ms | 4979ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 3683ms | 4814ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 4221ms | 4922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 4493ms | 4949ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 3859ms | 4880ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 4304ms | 4989ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 4533ms | 5493ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 3929ms | 4892ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 4321ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 4500ms | 4950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 3889ms | 4886ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 4266ms | 4965ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 4507ms | 4964ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 4160ms | 4916ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 4360ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 4508ms | 4996ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 3904ms | 4888ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 4327ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 4515ms | 5358ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 4184ms | 4918ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 4415ms | 4972ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 4516ms | 4996ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 3977ms | 4898ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 4350ms | 4950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 4507ms | 4964ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 3962ms | 4896ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 141.0 | app1 | ok | 4330ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 141.0 | app2 | ok | 4500ms | 4965ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 141.0 | end-users | ok | 4034ms | 4903ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 4321ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 4478ms | 4974ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 4085ms | 4909ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 4366ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 4435ms | 4973ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 4037ms | 4904ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 4355ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 4523ms | 4995ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 4056ms | 4906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 4325ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 4516ms | 4980ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 3722ms | 4837ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 4292ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 4500ms | 4964ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 3698ms | 4824ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 4300ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 4515ms | 4978ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 3755ms | 4852ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 4317ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 4458ms | 4958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 3939ms | 4893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 4390ms | 4939ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 4533ms | 5200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 4125ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 4409ms | 4941ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 4507ms | 4964ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 3859ms | 4880ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 4267ms | 5113ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 4544ms | 5575ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 3883ms | 4885ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 4250ms | 5400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 4466ms | 5125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 4370ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
