# Fairness benchmark: six-group-board-case (uni310-l2-r1-uni165-subset-3-idle)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 0.0 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 0.0 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

## Run metadata

| field | value |
|---|---|
| Scenario | `six-group-board-case` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-79f9bbd5f9-nkg5v` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T05:19:37Z` |
| Run end | `2026-11-26T05:23:55Z` |

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
| app1 | 16.7 | 32 | 1822 | 200=1822 | 4.2 | 4.8 | 2418422.0 | 33.3% | 33.3% | 0.0 | 33.3% | -0.0 | 33.3% | 0.0 | 6.0s | 98.9% | 1822.0 |
| app2 | 16.7 | 32 | 1821 | 200=1821 | 4.2 | 4.8 | 2419468.0 | 33.3% | 33.3% | 0.0 | 33.3% | 0.0 | 33.3% | -0.0 | 6.1s | 98.9% | 1821.0 |
| app3 | 16.7 | 32 | 1821 | 200=1821 | 4.2 | 4.8 | 2419418.0 | 33.3% | 33.3% | 0.0 | 33.3% | 0.0 | 33.3% | -0.0 | 6.1s | 98.9% | 1821.0 |
| app4 | 16.7 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| app5 | 16.7 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| app6 | 16.7 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| end-users | n/a | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- app3: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 0.0 | 0.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 20294.0 | 33.3% | 31.3% | -2.0 |
| 0.0 | 10.0 | app2 | True | False | 21574.0 | 33.3% | 33.3% | -0.0 |
| 0.0 | 10.0 | app3 | True | False | 22926.0 | 33.3% | 35.4% | 2.0 |
| 10.0 | 20.0 | app1 | True | False | 102760.0 | 33.3% | 33.8% | 0.4 |
| 10.0 | 20.0 | app2 | True | False | 101442.0 | 33.3% | 33.3% | 0.0 |
| 10.0 | 20.0 | app3 | True | False | 100088.0 | 33.3% | 32.9% | -0.4 |
| 20.0 | 30.0 | app1 | True | False | 102654.0 | 33.3% | 32.6% | -0.7 |
| 20.0 | 30.0 | app2 | True | False | 106728.0 | 33.3% | 33.9% | 0.6 |
| 20.0 | 30.0 | app3 | True | False | 105564.0 | 33.3% | 33.5% | 0.2 |
| 30.0 | 40.0 | app1 | True | False | 105402.0 | 33.3% | 34.2% | 0.8 |
| 30.0 | 40.0 | app2 | True | False | 100076.0 | 33.3% | 32.5% | -0.9 |
| 30.0 | 40.0 | app3 | True | False | 102866.0 | 33.3% | 33.4% | 0.0 |
| 40.0 | 50.0 | app1 | True | False | 101342.0 | 33.3% | 33.4% | 0.1 |
| 40.0 | 50.0 | app2 | True | False | 101484.0 | 33.3% | 33.5% | 0.2 |
| 40.0 | 50.0 | app3 | True | False | 100164.0 | 33.3% | 33.1% | -0.3 |
| 50.0 | 60.0 | app1 | True | False | 100024.0 | 33.3% | 32.4% | -0.9 |
| 50.0 | 60.0 | app2 | True | False | 104172.0 | 33.3% | 33.8% | 0.5 |
| 50.0 | 60.0 | app3 | True | False | 104072.0 | 33.3% | 33.8% | 0.4 |
| 60.0 | 70.0 | app1 | True | False | 105442.0 | 33.3% | 33.9% | 0.6 |
| 60.0 | 70.0 | app2 | True | False | 102778.0 | 33.3% | 33.1% | -0.3 |
| 60.0 | 70.0 | app3 | True | False | 102656.0 | 33.3% | 33.0% | -0.3 |
| 70.0 | 80.0 | app1 | True | False | 101404.0 | 33.3% | 33.3% | -0.0 |
| 70.0 | 80.0 | app2 | True | False | 101520.0 | 33.3% | 33.4% | 0.0 |
| 70.0 | 80.0 | app3 | True | False | 101372.0 | 33.3% | 33.3% | -0.0 |
| 80.0 | 90.0 | app1 | True | False | 100014.0 | 33.3% | 33.0% | -0.3 |
| 80.0 | 90.0 | app2 | True | False | 101400.0 | 33.3% | 33.5% | 0.1 |
| 80.0 | 90.0 | app3 | True | False | 101540.0 | 33.3% | 33.5% | 0.2 |
| 90.0 | 100.0 | app1 | True | False | 100082.0 | 33.3% | 32.8% | -0.6 |
| 90.0 | 100.0 | app2 | True | False | 101362.0 | 33.3% | 33.2% | -0.2 |
| 90.0 | 100.0 | app3 | True | False | 104102.0 | 33.3% | 34.1% | 0.7 |
| 100.0 | 110.0 | app1 | True | False | 102600.0 | 33.3% | 34.0% | 0.7 |
| 100.0 | 110.0 | app2 | True | False | 101570.0 | 33.3% | 33.7% | 0.3 |
| 100.0 | 110.0 | app3 | True | False | 97564.0 | 33.3% | 32.3% | -1.0 |
| 110.0 | 120.0 | app1 | True | False | 101404.0 | 33.3% | 33.2% | -0.2 |
| 110.0 | 120.0 | app2 | True | False | 104080.0 | 33.3% | 34.1% | 0.7 |
| 110.0 | 120.0 | app3 | True | False | 100142.0 | 33.3% | 32.8% | -0.6 |
| 120.0 | 130.0 | app1 | True | False | 101598.0 | 33.3% | 33.5% | 0.2 |
| 120.0 | 130.0 | app2 | True | False | 97324.0 | 33.3% | 32.1% | -1.2 |
| 120.0 | 130.0 | app3 | True | False | 103942.0 | 33.3% | 34.3% | 1.0 |
| 130.0 | 140.0 | app1 | True | False | 106688.0 | 33.3% | 34.0% | 0.7 |
| 130.0 | 140.0 | app2 | True | False | 105332.0 | 33.3% | 33.6% | 0.3 |
| 130.0 | 140.0 | app3 | True | False | 101496.0 | 33.3% | 32.4% | -1.0 |
| 140.0 | 150.0 | app1 | True | False | 98694.0 | 33.3% | 32.4% | -0.9 |
| 140.0 | 150.0 | app2 | True | False | 101428.0 | 33.3% | 33.3% | 0.0 |
| 140.0 | 150.0 | app3 | True | False | 104064.0 | 33.3% | 34.2% | 0.9 |
| 150.0 | 160.0 | app1 | True | False | 101544.0 | 33.3% | 33.4% | 0.0 |
| 150.0 | 160.0 | app2 | True | False | 101504.0 | 33.3% | 33.3% | 0.0 |
| 150.0 | 160.0 | app3 | True | False | 101370.0 | 33.3% | 33.3% | -0.0 |
| 160.0 | 170.0 | app1 | True | False | 102806.0 | 33.3% | 33.9% | 0.6 |
| 160.0 | 170.0 | app2 | True | False | 102850.0 | 33.3% | 33.9% | 0.6 |
| 160.0 | 170.0 | app3 | True | False | 97294.0 | 33.3% | 32.1% | -1.2 |
| 170.0 | 180.0 | app1 | True | False | 101404.0 | 33.3% | 33.2% | -0.2 |
| 170.0 | 180.0 | app2 | True | False | 98688.0 | 33.3% | 32.3% | -1.0 |
| 170.0 | 180.0 | app3 | True | False | 105574.0 | 33.3% | 34.5% | 1.2 |
| 180.0 | 190.0 | app1 | True | False | 101302.0 | 33.3% | 33.1% | -0.2 |
| 180.0 | 190.0 | app2 | True | False | 102888.0 | 33.3% | 33.7% | 0.3 |
| 180.0 | 190.0 | app3 | True | False | 101488.0 | 33.3% | 33.2% | -0.1 |
| 190.0 | 201.0 | app1 | True | False | 101366.0 | 33.3% | 33.2% | -0.2 |
| 190.0 | 201.0 | app2 | True | False | 101354.0 | 33.3% | 33.2% | -0.2 |
| 190.0 | 201.0 | app3 | True | False | 102822.0 | 33.3% | 33.7% | 0.3 |
| 201.0 | 211.0 | app1 | True | False | 101312.0 | 33.3% | 33.4% | 0.1 |
| 201.0 | 211.0 | app2 | True | False | 101576.0 | 33.3% | 33.5% | 0.2 |
| 201.0 | 211.0 | app3 | True | False | 100194.0 | 33.3% | 33.1% | -0.3 |
| 211.0 | 221.0 | app1 | True | False | 102744.0 | 33.3% | 33.2% | -0.1 |
| 211.0 | 221.0 | app2 | True | False | 102692.0 | 33.3% | 33.2% | -0.2 |
| 211.0 | 221.0 | app3 | True | False | 104048.0 | 33.3% | 33.6% | 0.3 |
| 221.0 | 231.0 | app1 | True | False | 102792.0 | 33.3% | 33.4% | 0.0 |
| 221.0 | 231.0 | app2 | True | False | 104084.0 | 33.3% | 33.8% | 0.4 |
| 221.0 | 231.0 | app3 | True | False | 101344.0 | 33.3% | 32.9% | -0.5 |
| 231.0 | 241.0 | app1 | True | False | 101374.0 | 33.3% | 33.2% | -0.2 |
| 231.0 | 241.0 | app2 | True | False | 101518.0 | 33.3% | 33.2% | -0.1 |
| 231.0 | 241.0 | app3 | True | False | 102668.0 | 33.3% | 33.6% | 0.3 |
| 241.0 | 251.0 | app1 | False | n/a | 51376.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 50044.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | n/a | 50058.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 79 | 0ms | 753ms | 975ms |
| 0.0 | 10.0 | app2 | ok | 78 | 0ms | 795ms | 979ms |
| 0.0 | 10.0 | app3 | ok | 79 | 23ms | 781ms | 978ms |
| 10.0 | 20.0 | app1 | ok | 74 | 320ms | 805ms | 981ms |
| 10.0 | 20.0 | app2 | ok | 74 | 355ms | 805ms | 981ms |
| 10.0 | 20.0 | app3 | ok | 74 | 315ms | 815ms | 982ms |
| 20.0 | 30.0 | app1 | ok | 75 | 236ms | 531ms | 953ms |
| 20.0 | 30.0 | app2 | ok | 75 | 270ms | 812ms | 981ms |
| 20.0 | 30.0 | app3 | ok | 75 | 239ms | 732ms | 973ms |
| 30.0 | 40.0 | app1 | ok | 76 | 260ms | 747ms | 975ms |
| 30.0 | 40.0 | app2 | ok | 76 | 260ms | 729ms | 973ms |
| 30.0 | 40.0 | app3 | ok | 75 | 307ms | 803ms | 980ms |
| 40.0 | 50.0 | app1 | ok | 78 | 317ms | 805ms | 980ms |
| 40.0 | 50.0 | app2 | ok | 80 | 298ms | 789ms | 979ms |
| 40.0 | 50.0 | app3 | ok | 80 | 320ms | 818ms | 982ms |
| 50.0 | 60.0 | app1 | ok | 75 | 375ms | 837ms | 984ms |
| 50.0 | 60.0 | app2 | ok | 74 | 333ms | 805ms | 981ms |
| 50.0 | 60.0 | app3 | ok | 74 | 287ms | 736ms | 974ms |
| 60.0 | 70.0 | app1 | ok | 74 | 288ms | 815ms | 982ms |
| 60.0 | 70.0 | app2 | ok | 75 | 304ms | 821ms | 982ms |
| 60.0 | 70.0 | app3 | ok | 73 | 289ms | 841ms | 984ms |
| 70.0 | 80.0 | app1 | ok | 80 | 307ms | 826ms | 983ms |
| 70.0 | 80.0 | app2 | ok | 78 | 250ms | 771ms | 977ms |
| 70.0 | 80.0 | app3 | ok | 80 | 318ms | 833ms | 983ms |
| 80.0 | 90.0 | app1 | ok | 74 | 330ms | 832ms | 983ms |
| 80.0 | 90.0 | app2 | ok | 75 | 338ms | 792ms | 979ms |
| 80.0 | 90.0 | app3 | ok | 74 | 263ms | 805ms | 981ms |
| 90.0 | 100.0 | app1 | ok | 73 | 280ms | 797ms | 980ms |
| 90.0 | 100.0 | app2 | ok | 73 | 310ms | 772ms | 977ms |
| 90.0 | 100.0 | app3 | ok | 75 | 299ms | 803ms | 980ms |
| 100.0 | 110.0 | app1 | ok | 75 | 328ms | 821ms | 982ms |
| 100.0 | 110.0 | app2 | ok | 75 | 325ms | 812ms | 981ms |
| 100.0 | 110.0 | app3 | ok | 74 | 330ms | 815ms | 982ms |
| 110.0 | 120.0 | app1 | ok | 74 | 368ms | 863ms | 986ms |
| 110.0 | 120.0 | app2 | ok | 76 | 331ms | 776ms | 978ms |
| 110.0 | 120.0 | app3 | ok | 73 | 351ms | 826ms | 983ms |
| 120.0 | 130.0 | app1 | ok | 74 | 344ms | 832ms | 983ms |
| 120.0 | 130.0 | app2 | ok | 74 | 300ms | 782ms | 978ms |
| 120.0 | 130.0 | app3 | ok | 76 | 312ms | 810ms | 981ms |
| 130.0 | 140.0 | app1 | ok | 79 | 358ms | 828ms | 983ms |
| 130.0 | 140.0 | app2 | ok | 78 | 340ms | 830ms | 983ms |
| 130.0 | 140.0 | app3 | ok | 77 | 344ms | 817ms | 982ms |
| 140.0 | 150.0 | app1 | ok | 75 | 347ms | 844ms | 984ms |
| 140.0 | 150.0 | app2 | ok | 73 | 327ms | 834ms | 983ms |
| 140.0 | 150.0 | app3 | ok | 73 | 338ms | 808ms | 981ms |
| 150.0 | 160.0 | app1 | ok | 73 | 338ms | 808ms | 981ms |
| 150.0 | 160.0 | app2 | ok | 74 | 306ms | 769ms | 977ms |
| 150.0 | 160.0 | app3 | ok | 75 | 366ms | 830ms | 983ms |
| 160.0 | 170.0 | app1 | ok | 75 | 341ms | 803ms | 980ms |
| 160.0 | 170.0 | app2 | ok | 74 | 327ms | 805ms | 981ms |
| 160.0 | 170.0 | app3 | ok | 75 | 356ms | 830ms | 983ms |
| 170.0 | 180.0 | app1 | ok | 77 | 304ms | 743ms | 974ms |
| 170.0 | 180.0 | app2 | ok | 79 | 302ms | 737ms | 974ms |
| 170.0 | 180.0 | app3 | ok | 79 | 332ms | 803ms | 980ms |
| 180.0 | 190.0 | app1 | ok | 79 | 379ms | 848ms | 985ms |
| 180.0 | 190.0 | app2 | ok | 76 | 296ms | 763ms | 976ms |
| 180.0 | 190.0 | app3 | ok | 76 | 352ms | 827ms | 983ms |
| 190.0 | 201.0 | app1 | ok | 74 | 365ms | 839ms | 984ms |
| 190.0 | 201.0 | app2 | ok | 76 | 352ms | 827ms | 983ms |
| 190.0 | 201.0 | app3 | ok | 76 | 350ms | 810ms | 981ms |
| 201.0 | 211.0 | app1 | ok | 74 | 357ms | 852ms | 985ms |
| 201.0 | 211.0 | app2 | ok | 73 | 353ms | 841ms | 984ms |
| 201.0 | 211.0 | app3 | ok | 71 | 365ms | 839ms | 984ms |
| 211.0 | 221.0 | app1 | ok | 73 | 307ms | 797ms | 980ms |
| 211.0 | 221.0 | app2 | ok | 74 | 243ms | 769ms | 977ms |
| 211.0 | 221.0 | app3 | ok | 78 | 236ms | 771ms | 977ms |
| 221.0 | 231.0 | app1 | ok | 76 | 236ms | 763ms | 976ms |
| 221.0 | 231.0 | app2 | ok | 75 | 280ms | 803ms | 980ms |
| 221.0 | 231.0 | app3 | ok | 74 | 261ms | 769ms | 977ms |
| 231.0 | 241.0 | app1 | ok | 77 | 358ms | 825ms | 983ms |
| 231.0 | 241.0 | app2 | ok | 79 | 394ms | 859ms | 986ms |
| 231.0 | 241.0 | app3 | ok | 76 | 350ms | 835ms | 983ms |
| 241.0 | 251.0 | app1 | ok | 9 | 212ms | 888ms | 989ms |
| 241.0 | 251.0 | app2 | ok | 7 | 562ms | 912ms | 991ms |
| 241.0 | 251.0 | app3 | ok | 9 | 375ms | 850ms | 985ms |
| 251.0 | 258.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2241060 | 110985 | 2352045.0 | 0.0% | 2418422.0 | 2463030.0 | -1.8% | True |
| app2 | 2239830 | 111462 | 2351292.0 | 0.0% | 2419468.0 | 2462754.0 | -1.8% | True |
| app3 | 2239830 | 111430 | 2351260.0 | 0.0% | 2419418.0 | 2462690.0 | -1.8% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1822 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1821 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 1821 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5464). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5464 | 0.051ms | 0.162ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 245385 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1822 | 4260ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1821 | 4269ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app3 | ok | 1821 | 4265ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5464 | 4265ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 3000ms | 4956ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 3000ms | 4964ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app3 | ok | 3026ms | 4887ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 4309ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 4250ms | 4925ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app3 | ok | 4229ms | 4923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 4208ms | 4921ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 4240ms | 4924ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app3 | ok | 4240ms | 4942ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 4204ms | 4920ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 4250ms | 4944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app3 | ok | 4283ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 4292ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 4279ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app3 | ok | 4302ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 4302ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 4287ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app3 | ok | 4312ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 4235ms | 4924ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 4245ms | 4943ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app3 | ok | 4224ms | 4922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 4284ms | 4946ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 4265ms | 4926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app3 | ok | 4279ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 4288ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 4279ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app3 | ok | 4353ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 4178ms | 4918ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 4270ms | 4945ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app3 | ok | 4181ms | 4918ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 4280ms | 4964ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 4279ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app3 | ok | 4308ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 4170ms | 4938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 4185ms | 4938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app3 | ok | 4190ms | 4983ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 4279ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 4255ms | 4945ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app3 | ok | 4260ms | 4926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 4295ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 4278ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app3 | ok | 4364ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 4255ms | 4926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 4364ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app3 | ok | 4230ms | 4923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 4342ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 4342ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app3 | ok | 4317ms | 4966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 4296ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 4315ms | 4948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app3 | ok | 4321ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 4318ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 4298ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app3 | ok | 4304ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app1 | ok | 4292ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app2 | ok | 4321ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app3 | ok | 4330ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 201.0 | app1 | ok | 4330ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 201.0 | app2 | ok | 4306ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 201.0 | app3 | ok | 4255ms | 4925ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 4240ms | 4943ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 4235ms | 4923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app3 | ok | 4255ms | 4964ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 4213ms | 4940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 4260ms | 4944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app3 | ok | 4230ms | 4923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 4321ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 4274ms | 4927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app3 | ok | 4318ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 4279ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 4235ms | 4923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app3 | ok | 4269ms | 4927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 4269ms | 4927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 4422ms | 4942ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app3 | ok | 4339ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
