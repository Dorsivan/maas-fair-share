# Fairness benchmark: six-group-board-case (uni310-l3-r1-uni165-subset-3-idle)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-56676bd7d4-lttb6` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T05:47:02Z` |
| Run end | `2026-11-26T05:51:20Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 27 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/27 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 40.00 | 1.2500 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 16.7 | 32 | 1819 | 200=1819 | 4.2 | 4.8 | 2415618.0 | 33.3% | 33.3% | 0.0 | 33.3% | -0.0 | 33.3% | 0.0 | 4.1s | 98.9% | 1819.0 |
| app2 | 16.7 | 32 | 1819 | 200=1819 | 4.2 | 4.8 | 2416036.0 | 33.3% | 33.3% | 0.0 | 33.3% | 0.0 | 33.3% | 0.0 | 4.1s | 98.9% | 1819.0 |
| app3 | 16.7 | 32 | 1818 | 200=1818 | 4.2 | 4.8 | 2415550.0 | 33.3% | 33.3% | 0.0 | 33.3% | -0.0 | 33.3% | -0.0 | 4.1s | 98.9% | 1818.0 |
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
| 0.0 | 10.0 | app1 | True | False | 14910.0 | 33.3% | 30.6% | -2.7 |
| 0.0 | 10.0 | app2 | True | False | 16220.0 | 33.3% | 33.3% | -0.1 |
| 0.0 | 10.0 | app3 | True | False | 17620.0 | 33.3% | 36.1% | 2.8 |
| 10.0 | 20.0 | app1 | True | False | 101494.0 | 33.3% | 33.1% | -0.3 |
| 10.0 | 20.0 | app2 | True | False | 102742.0 | 33.3% | 33.5% | 0.1 |
| 10.0 | 20.0 | app3 | True | False | 102762.0 | 33.3% | 33.5% | 0.1 |
| 20.0 | 30.0 | app1 | True | False | 104216.0 | 33.3% | 33.8% | 0.5 |
| 20.0 | 30.0 | app2 | True | False | 102540.0 | 33.3% | 33.3% | -0.1 |
| 20.0 | 30.0 | app3 | True | False | 101460.0 | 33.3% | 32.9% | -0.4 |
| 30.0 | 40.0 | app1 | True | False | 101568.0 | 33.3% | 33.5% | 0.2 |
| 30.0 | 40.0 | app2 | True | False | 100052.0 | 33.3% | 33.0% | -0.3 |
| 30.0 | 40.0 | app3 | True | False | 101530.0 | 33.3% | 33.5% | 0.2 |
| 40.0 | 50.0 | app1 | True | False | 102752.0 | 33.3% | 33.5% | 0.1 |
| 40.0 | 50.0 | app2 | True | False | 102682.0 | 33.3% | 33.5% | 0.1 |
| 40.0 | 50.0 | app3 | True | False | 101506.0 | 33.3% | 33.1% | -0.3 |
| 50.0 | 60.0 | app1 | True | False | 101462.0 | 33.3% | 33.1% | -0.3 |
| 50.0 | 60.0 | app2 | True | False | 102758.0 | 33.3% | 33.5% | 0.2 |
| 50.0 | 60.0 | app3 | True | False | 102664.0 | 33.3% | 33.5% | 0.1 |
| 60.0 | 70.0 | app1 | True | False | 101454.0 | 33.3% | 33.0% | -0.3 |
| 60.0 | 70.0 | app2 | True | False | 102782.0 | 33.3% | 33.5% | 0.1 |
| 60.0 | 70.0 | app3 | True | False | 102736.0 | 33.3% | 33.5% | 0.1 |
| 70.0 | 80.0 | app1 | True | False | 100000.0 | 33.3% | 32.9% | -0.4 |
| 70.0 | 80.0 | app2 | True | False | 101352.0 | 33.3% | 33.3% | -0.0 |
| 70.0 | 80.0 | app3 | True | False | 102752.0 | 33.3% | 33.8% | 0.5 |
| 80.0 | 90.0 | app1 | True | False | 105552.0 | 33.3% | 34.4% | 1.0 |
| 80.0 | 90.0 | app2 | True | False | 101378.0 | 33.3% | 33.0% | -0.3 |
| 80.0 | 90.0 | app3 | True | False | 100078.0 | 33.3% | 32.6% | -0.7 |
| 90.0 | 100.0 | app1 | True | False | 99950.0 | 33.3% | 32.7% | -0.6 |
| 90.0 | 100.0 | app2 | True | False | 104178.0 | 33.3% | 34.1% | 0.8 |
| 90.0 | 100.0 | app3 | True | False | 101418.0 | 33.3% | 33.2% | -0.1 |
| 100.0 | 110.0 | app1 | True | False | 101606.0 | 33.3% | 33.7% | 0.4 |
| 100.0 | 110.0 | app2 | True | False | 97302.0 | 33.3% | 32.3% | -1.1 |
| 100.0 | 110.0 | app3 | True | False | 102728.0 | 33.3% | 34.1% | 0.7 |
| 110.0 | 120.0 | app1 | True | False | 100084.0 | 33.3% | 33.0% | -0.3 |
| 110.0 | 120.0 | app2 | True | False | 102654.0 | 33.3% | 33.9% | 0.6 |
| 110.0 | 120.0 | app3 | True | False | 100190.0 | 33.3% | 33.1% | -0.3 |
| 120.0 | 130.0 | app1 | True | False | 101416.0 | 33.3% | 33.3% | -0.0 |
| 120.0 | 130.0 | app2 | True | False | 101472.0 | 33.3% | 33.3% | 0.0 |
| 120.0 | 130.0 | app3 | True | False | 101428.0 | 33.3% | 33.3% | -0.0 |
| 130.0 | 140.0 | app1 | True | False | 99992.0 | 33.3% | 33.3% | -0.0 |
| 130.0 | 140.0 | app2 | True | False | 99980.0 | 33.3% | 33.3% | -0.0 |
| 130.0 | 140.0 | app3 | True | False | 100322.0 | 33.3% | 33.4% | 0.1 |
| 140.0 | 150.0 | app1 | True | False | 102828.0 | 33.3% | 33.5% | 0.2 |
| 140.0 | 150.0 | app2 | True | False | 102858.0 | 33.3% | 33.5% | 0.2 |
| 140.0 | 150.0 | app3 | True | False | 101360.0 | 33.3% | 33.0% | -0.3 |
| 150.0 | 160.0 | app1 | True | False | 100078.0 | 33.3% | 33.2% | -0.1 |
| 150.0 | 160.0 | app2 | True | False | 102798.0 | 33.3% | 34.1% | 0.8 |
| 150.0 | 160.0 | app3 | True | False | 98676.0 | 33.3% | 32.7% | -0.6 |
| 160.0 | 170.0 | app1 | True | False | 101454.0 | 33.3% | 32.9% | -0.4 |
| 160.0 | 170.0 | app2 | True | False | 101346.0 | 33.3% | 32.9% | -0.4 |
| 160.0 | 170.0 | app3 | True | False | 105388.0 | 33.3% | 34.2% | 0.9 |
| 170.0 | 180.0 | app1 | True | False | 102616.0 | 33.3% | 33.5% | 0.1 |
| 170.0 | 180.0 | app2 | True | False | 102864.0 | 33.3% | 33.5% | 0.2 |
| 170.0 | 180.0 | app3 | True | False | 101286.0 | 33.3% | 33.0% | -0.3 |
| 180.0 | 190.0 | app1 | True | False | 101492.0 | 33.3% | 33.5% | 0.2 |
| 180.0 | 190.0 | app2 | True | False | 98774.0 | 33.3% | 32.6% | -0.7 |
| 180.0 | 190.0 | app3 | True | False | 102678.0 | 33.3% | 33.9% | 0.6 |
| 190.0 | 200.0 | app1 | True | False | 101508.0 | 33.3% | 33.6% | 0.3 |
| 190.0 | 200.0 | app2 | True | False | 100094.0 | 33.3% | 33.2% | -0.2 |
| 190.0 | 200.0 | app3 | True | False | 100082.0 | 33.3% | 33.2% | -0.2 |
| 200.0 | 210.0 | app1 | True | False | 101348.0 | 33.3% | 33.4% | 0.1 |
| 200.0 | 210.0 | app2 | True | False | 102832.0 | 33.3% | 33.9% | 0.6 |
| 200.0 | 210.0 | app3 | True | False | 98814.0 | 33.3% | 32.6% | -0.7 |
| 210.0 | 221.0 | app1 | True | False | 99994.0 | 33.3% | 32.7% | -0.6 |
| 210.0 | 221.0 | app2 | True | False | 101378.0 | 33.3% | 33.2% | -0.2 |
| 210.0 | 221.0 | app3 | True | False | 104218.0 | 33.3% | 34.1% | 0.8 |
| 221.0 | 231.0 | app1 | True | False | 104208.0 | 33.3% | 34.1% | 0.7 |
| 221.0 | 231.0 | app2 | True | False | 100078.0 | 33.3% | 32.7% | -0.6 |
| 221.0 | 231.0 | app3 | True | False | 101516.0 | 33.3% | 33.2% | -0.1 |
| 231.0 | 241.0 | app1 | True | False | 101484.0 | 33.3% | 33.5% | 0.2 |
| 231.0 | 241.0 | app2 | True | False | 101346.0 | 33.3% | 33.5% | 0.1 |
| 231.0 | 241.0 | app3 | True | False | 100104.0 | 33.3% | 33.0% | -0.3 |
| 241.0 | 251.0 | app1 | False | n/a | 62152.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 63576.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | n/a | 62234.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 70 | 0ms | 708ms | 971ms |
| 0.0 | 10.0 | app2 | ok | 69 | 0ms | 784ms | 978ms |
| 0.0 | 10.0 | app3 | ok | 71 | 0ms | 677ms | 968ms |
| 10.0 | 20.0 | app1 | ok | 78 | 370ms | 856ms | 986ms |
| 10.0 | 20.0 | app2 | ok | 78 | 346ms | 830ms | 983ms |
| 10.0 | 20.0 | app3 | ok | 77 | 283ms | 825ms | 983ms |
| 20.0 | 30.0 | app1 | ok | 75 | 275ms | 844ms | 984ms |
| 20.0 | 30.0 | app2 | ok | 79 | 246ms | 803ms | 980ms |
| 20.0 | 30.0 | app3 | ok | 77 | 304ms | 743ms | 974ms |
| 30.0 | 40.0 | app1 | ok | 76 | 312ms | 854ms | 985ms |
| 30.0 | 40.0 | app2 | ok | 75 | 309ms | 837ms | 984ms |
| 30.0 | 40.0 | app3 | ok | 76 | 262ms | 789ms | 979ms |
| 40.0 | 50.0 | app1 | ok | 78 | 365ms | 850ms | 985ms |
| 40.0 | 50.0 | app2 | ok | 75 | 331ms | 844ms | 984ms |
| 40.0 | 50.0 | app3 | ok | 75 | 331ms | 844ms | 984ms |
| 50.0 | 60.0 | app1 | ok | 76 | 369ms | 859ms | 986ms |
| 50.0 | 60.0 | app2 | ok | 77 | 322ms | 807ms | 981ms |
| 50.0 | 60.0 | app3 | ok | 77 | 335ms | 825ms | 983ms |
| 60.0 | 70.0 | app1 | ok | 76 | 288ms | 819ms | 982ms |
| 60.0 | 70.0 | app2 | ok | 77 | 392ms | 880ms | 988ms |
| 60.0 | 70.0 | app3 | ok | 76 | 333ms | 854ms | 985ms |
| 70.0 | 80.0 | app1 | ok | 71 | 335ms | 763ms | 976ms |
| 70.0 | 80.0 | app2 | ok | 70 | 298ms | 806ms | 981ms |
| 70.0 | 80.0 | app3 | ok | 70 | 330ms | 825ms | 982ms |
| 80.0 | 90.0 | app1 | ok | 76 | 352ms | 827ms | 983ms |
| 80.0 | 90.0 | app2 | ok | 76 | 350ms | 835ms | 983ms |
| 80.0 | 90.0 | app3 | ok | 77 | 341ms | 825ms | 983ms |
| 90.0 | 100.0 | app1 | ok | 75 | 322ms | 803ms | 980ms |
| 90.0 | 100.0 | app2 | ok | 75 | 338ms | 812ms | 981ms |
| 90.0 | 100.0 | app3 | ok | 75 | 301ms | 812ms | 981ms |
| 100.0 | 110.0 | app1 | ok | 75 | 375ms | 861ms | 986ms |
| 100.0 | 110.0 | app2 | ok | 76 | 400ms | 864ms | 986ms |
| 100.0 | 110.0 | app3 | ok | 76 | 396ms | 864ms | 986ms |
| 110.0 | 120.0 | app1 | ok | 75 | 315ms | 803ms | 980ms |
| 110.0 | 120.0 | app2 | ok | 74 | 292ms | 782ms | 978ms |
| 110.0 | 120.0 | app3 | ok | 74 | 348ms | 839ms | 984ms |
| 120.0 | 130.0 | app1 | ok | 73 | 349ms | 808ms | 981ms |
| 120.0 | 130.0 | app2 | ok | 74 | 310ms | 794ms | 979ms |
| 120.0 | 130.0 | app3 | ok | 74 | 317ms | 794ms | 979ms |
| 130.0 | 140.0 | app1 | ok | 78 | 320ms | 814ms | 981ms |
| 130.0 | 140.0 | app2 | ok | 77 | 370ms | 852ms | 985ms |
| 130.0 | 140.0 | app3 | ok | 76 | 348ms | 842ms | 984ms |
| 140.0 | 150.0 | app1 | ok | 74 | 306ms | 839ms | 984ms |
| 140.0 | 150.0 | app2 | ok | 74 | 359ms | 846ms | 985ms |
| 140.0 | 150.0 | app3 | ok | 75 | 315ms | 803ms | 980ms |
| 150.0 | 160.0 | app1 | ok | 75 | 299ms | 803ms | 980ms |
| 150.0 | 160.0 | app2 | ok | 76 | 333ms | 842ms | 984ms |
| 150.0 | 160.0 | app3 | ok | 74 | 357ms | 852ms | 985ms |
| 160.0 | 170.0 | app1 | ok | 74 | 250ms | 805ms | 981ms |
| 160.0 | 170.0 | app2 | ok | 75 | 308ms | 766ms | 977ms |
| 160.0 | 170.0 | app3 | ok | 76 | 289ms | 827ms | 983ms |
| 170.0 | 180.0 | app1 | ok | 74 | 312ms | 805ms | 981ms |
| 170.0 | 180.0 | app2 | ok | 75 | 332ms | 812ms | 981ms |
| 170.0 | 180.0 | app3 | ok | 76 | 327ms | 810ms | 981ms |
| 180.0 | 190.0 | app1 | ok | 77 | 305ms | 797ms | 980ms |
| 180.0 | 190.0 | app2 | ok | 75 | 356ms | 830ms | 983ms |
| 180.0 | 190.0 | app3 | ok | 75 | 312ms | 821ms | 982ms |
| 190.0 | 200.0 | app1 | ok | 76 | 302ms | 800ms | 980ms |
| 190.0 | 200.0 | app2 | ok | 75 | 321ms | 821ms | 982ms |
| 190.0 | 200.0 | app3 | ok | 77 | 328ms | 825ms | 983ms |
| 200.0 | 210.0 | app1 | ok | 75 | 274ms | 732ms | 973ms |
| 200.0 | 210.0 | app2 | ok | 76 | 333ms | 827ms | 983ms |
| 200.0 | 210.0 | app3 | ok | 74 | 380ms | 846ms | 985ms |
| 210.0 | 221.0 | app1 | ok | 75 | 356ms | 830ms | 983ms |
| 210.0 | 221.0 | app2 | ok | 74 | 375ms | 852ms | 985ms |
| 210.0 | 221.0 | app3 | ok | 74 | 348ms | 815ms | 982ms |
| 221.0 | 231.0 | app1 | ok | 75 | 335ms | 803ms | 980ms |
| 221.0 | 231.0 | app2 | ok | 77 | 361ms | 840ms | 984ms |
| 221.0 | 231.0 | app3 | ok | 76 | 331ms | 776ms | 978ms |
| 231.0 | 241.0 | app1 | ok | 75 | 322ms | 803ms | 980ms |
| 231.0 | 241.0 | app2 | ok | 73 | 278ms | 785ms | 979ms |
| 231.0 | 241.0 | app3 | ok | 75 | 310ms | 812ms | 981ms |
| 241.0 | 251.0 | app1 | ok | 17 | 411ms | 858ms | 986ms |
| 241.0 | 251.0 | app2 | ok | 17 | 339ms | 788ms | 979ms |
| 241.0 | 251.0 | app3 | ok | 15 | 281ms | 812ms | 981ms |
| 251.0 | 258.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2237370 | 111473 | 2348843.0 | 0.0% | 2415618.0 | 2460316.0 | -1.8% | True |
| app2 | 2237370 | 111022 | 2348392.0 | 0.0% | 2416036.0 | 2459414.0 | -1.8% | True |
| app3 | 2236140 | 111271 | 2347411.0 | 0.0% | 2415550.0 | 2458682.0 | -1.8% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1819 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1819 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 1818 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5456). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5456 | 0.051ms | 0.131ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 245645 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1819 | 4302ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1819 | 4299ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app3 | ok | 1818 | 4293ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5456 | 4298ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2818ms | 5450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2773ms | 5283ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app3 | ok | 2455ms | 5267ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 4292ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 4306ms | 4947ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app3 | ok | 4306ms | 4947ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 4330ms | 4949ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 4269ms | 4927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app3 | ok | 4219ms | 4922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 4318ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 4315ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app3 | ok | 4364ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 4240ms | 4924ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 4321ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app3 | ok | 4279ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 4202ms | 4920ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 4240ms | 4924ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app3 | ok | 4269ms | 4927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 4353ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 4309ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app3 | ok | 4321ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 4275ms | 4927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 4279ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app3 | ok | 4269ms | 4927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 4264ms | 4926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 4330ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app3 | ok | 4260ms | 4926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 4288ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 4336ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app3 | ok | 4364ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 4364ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 4333ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app3 | ok | 4309ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 4339ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 4345ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app3 | ok | 4351ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 4375ms | 4938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 4395ms | 4940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app3 | ok | 4342ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 4393ms | 4939ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 4315ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app3 | ok | 4351ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 4315ms | 4948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 4296ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app3 | ok | 4330ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 4315ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 4309ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app3 | ok | 4255ms | 4926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 4279ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 4219ms | 4922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app3 | ok | 4264ms | 4926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 4159ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 4196ms | 4939ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app3 | ok | 4240ms | 4943ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app1 | ok | 4361ms | 4986ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app2 | ok | 4336ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app3 | ok | 4321ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app1 | ok | 4318ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app2 | ok | 4362ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app3 | ok | 4339ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app1 | ok | 4364ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app2 | ok | 4321ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app3 | ok | 4270ms | 4927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 221.0 | app1 | ok | 4302ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 221.0 | app2 | ok | 4342ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 221.0 | app3 | ok | 4358ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 4300ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 4327ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app3 | ok | 4306ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 4353ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 4330ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app3 | ok | 4288ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 4324ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 4242ms | 4924ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app3 | ok | 4281ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
