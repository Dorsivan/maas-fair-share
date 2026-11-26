# Fairness benchmark: end-users-idle (uni310-l3-r1-end-users-idle)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 0.0 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 0.0 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

## Run metadata

| field | value |
|---|---|
| Scenario | `end-users-idle` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5d57688bf8-7n2t5` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T05:18:22Z` |
| Run end | `2026-11-26T05:22:41Z` |

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
| app1 | 20.0 | 64 | 3627 | 200=3627 | 4.2 | 4.7 | 4818282.0 | 66.7% | 66.7% | 0.0 | 66.7% | 0.0 | 66.6% | -0.0 | 4.1s | 98.9% | 3627.0 |
| app2 | 10.0 | 32 | 1815 | 200=1815 | 4.2 | 4.8 | 2408080.0 | 33.3% | 33.3% | 0.0 | 33.3% | -0.0 | 33.4% | 0.0 | 4.1s | 98.9% | 1815.0 |
| end-users | 65.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 0.0 | 0.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 24324.0 | 66.7% | 69.3% | 2.6 |
| 0.0 | 10.0 | app2 | True | False | 10798.0 | 33.3% | 30.7% | -2.6 |
| 10.0 | 20.0 | app1 | True | False | 201506.0 | 66.7% | 66.5% | -0.1 |
| 10.0 | 20.0 | app2 | True | False | 101386.0 | 33.3% | 33.5% | 0.1 |
| 20.0 | 30.0 | app1 | True | False | 209558.0 | 66.7% | 67.1% | 0.4 |
| 20.0 | 30.0 | app2 | True | False | 102726.0 | 33.3% | 32.9% | -0.4 |
| 30.0 | 40.0 | app1 | True | False | 202780.0 | 66.7% | 66.7% | 0.0 |
| 30.0 | 40.0 | app2 | True | False | 101328.0 | 33.3% | 33.3% | -0.0 |
| 40.0 | 50.0 | app1 | True | False | 204136.0 | 66.7% | 66.5% | -0.1 |
| 40.0 | 50.0 | app2 | True | False | 102658.0 | 33.3% | 33.5% | 0.1 |
| 50.0 | 60.0 | app1 | True | False | 202868.0 | 66.7% | 66.4% | -0.3 |
| 50.0 | 60.0 | app2 | True | False | 102834.0 | 33.3% | 33.6% | 0.3 |
| 60.0 | 70.0 | app1 | True | False | 200220.0 | 66.7% | 67.0% | 0.3 |
| 60.0 | 70.0 | app2 | True | False | 98790.0 | 33.3% | 33.0% | -0.3 |
| 70.0 | 80.0 | app1 | True | False | 205434.0 | 66.7% | 66.7% | 0.0 |
| 70.0 | 80.0 | app2 | True | False | 102686.0 | 33.3% | 33.3% | -0.0 |
| 80.0 | 90.0 | app1 | True | False | 202984.0 | 66.7% | 66.7% | 0.0 |
| 80.0 | 90.0 | app2 | True | False | 101404.0 | 33.3% | 33.3% | -0.0 |
| 90.0 | 100.0 | app1 | True | False | 200208.0 | 66.7% | 66.6% | -0.0 |
| 90.0 | 100.0 | app2 | True | False | 100200.0 | 33.3% | 33.4% | 0.0 |
| 100.0 | 110.0 | app1 | True | False | 201486.0 | 66.7% | 67.1% | 0.4 |
| 100.0 | 110.0 | app2 | True | False | 98796.0 | 33.3% | 32.9% | -0.4 |
| 110.0 | 120.0 | app1 | True | False | 204142.0 | 66.7% | 66.2% | -0.4 |
| 110.0 | 120.0 | app2 | True | False | 104076.0 | 33.3% | 33.8% | 0.4 |
| 120.0 | 130.0 | app1 | True | False | 202706.0 | 66.7% | 66.9% | 0.3 |
| 120.0 | 130.0 | app2 | True | False | 100110.0 | 33.3% | 33.1% | -0.3 |
| 130.0 | 140.0 | app1 | True | False | 201404.0 | 66.7% | 66.2% | -0.5 |
| 130.0 | 140.0 | app2 | True | False | 102790.0 | 33.3% | 33.8% | 0.5 |
| 140.0 | 150.0 | app1 | True | False | 202820.0 | 66.7% | 66.7% | 0.0 |
| 140.0 | 150.0 | app2 | True | False | 101308.0 | 33.3% | 33.3% | -0.0 |
| 150.0 | 160.0 | app1 | True | False | 204444.0 | 66.7% | 67.1% | 0.5 |
| 150.0 | 160.0 | app2 | True | False | 100084.0 | 33.3% | 32.9% | -0.5 |
| 160.0 | 170.0 | app1 | True | False | 201372.0 | 66.7% | 66.2% | -0.5 |
| 160.0 | 170.0 | app2 | True | False | 102770.0 | 33.3% | 33.8% | 0.5 |
| 170.0 | 180.0 | app1 | True | False | 200240.0 | 66.7% | 66.1% | -0.6 |
| 170.0 | 180.0 | app2 | True | False | 102712.0 | 33.3% | 33.9% | 0.6 |
| 180.0 | 190.0 | app1 | True | False | 205296.0 | 66.7% | 66.9% | 0.3 |
| 180.0 | 190.0 | app2 | True | False | 101426.0 | 33.3% | 33.1% | -0.3 |
| 190.0 | 200.0 | app1 | True | False | 203178.0 | 66.7% | 67.6% | 0.9 |
| 190.0 | 200.0 | app2 | True | False | 97436.0 | 33.3% | 32.4% | -0.9 |
| 200.0 | 210.0 | app1 | True | False | 202666.0 | 66.7% | 66.1% | -0.6 |
| 200.0 | 210.0 | app2 | True | False | 104108.0 | 33.3% | 33.9% | 0.6 |
| 210.0 | 220.0 | app1 | True | False | 201606.0 | 66.7% | 66.6% | -0.1 |
| 210.0 | 220.0 | app2 | True | False | 101270.0 | 33.3% | 33.4% | 0.1 |
| 220.0 | 230.0 | app1 | True | False | 203046.0 | 66.7% | 67.0% | 0.3 |
| 220.0 | 230.0 | app2 | True | False | 100062.0 | 33.3% | 33.0% | -0.3 |
| 230.0 | 240.0 | app1 | True | False | 204060.0 | 66.7% | 66.8% | 0.1 |
| 230.0 | 240.0 | app2 | True | False | 101414.0 | 33.3% | 33.2% | -0.1 |
| 240.0 | 250.0 | app1 | False | n/a | 125798.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | n/a | 64908.0 | n/a | n/a | n/a |
| 250.0 | 259.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 250.0 | 259.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 136 | 0ms | 757ms | 976ms |
| 0.0 | 10.0 | app2 | ok | 69 | 0ms | 686ms | 969ms |
| 10.0 | 20.0 | app1 | ok | 152 | 326ms | 827ms | 983ms |
| 10.0 | 20.0 | app2 | ok | 76 | 324ms | 854ms | 985ms |
| 20.0 | 30.0 | app1 | ok | 151 | 295ms | 796ms | 980ms |
| 20.0 | 30.0 | app2 | ok | 75 | 288ms | 792ms | 979ms |
| 30.0 | 40.0 | app1 | ok | 160 | 317ms | 795ms | 979ms |
| 30.0 | 40.0 | app2 | ok | 80 | 352ms | 833ms | 983ms |
| 40.0 | 50.0 | app1 | ok | 149 | 311ms | 834ms | 983ms |
| 40.0 | 50.0 | app2 | ok | 73 | 285ms | 757ms | 976ms |
| 50.0 | 60.0 | app1 | ok | 150 | 366ms | 837ms | 984ms |
| 50.0 | 60.0 | app2 | ok | 78 | 261ms | 783ms | 978ms |
| 60.0 | 70.0 | app1 | ok | 142 | 349ms | 831ms | 983ms |
| 60.0 | 70.0 | app2 | ok | 71 | 281ms | 803ms | 980ms |
| 70.0 | 80.0 | app1 | ok | 154 | 321ms | 836ms | 984ms |
| 70.0 | 80.0 | app2 | ok | 75 | 287ms | 837ms | 984ms |
| 80.0 | 90.0 | app1 | ok | 149 | 331ms | 793ms | 979ms |
| 80.0 | 90.0 | app2 | ok | 76 | 344ms | 835ms | 983ms |
| 90.0 | 100.0 | app1 | ok | 152 | 346ms | 827ms | 983ms |
| 90.0 | 100.0 | app2 | ok | 73 | 322ms | 797ms | 980ms |
| 100.0 | 110.0 | app1 | ok | 146 | 378ms | 860ms | 986ms |
| 100.0 | 110.0 | app2 | ok | 74 | 324ms | 794ms | 979ms |
| 110.0 | 120.0 | app1 | ok | 151 | 302ms | 790ms | 979ms |
| 110.0 | 120.0 | app2 | ok | 76 | 295ms | 747ms | 975ms |
| 120.0 | 130.0 | app1 | ok | 155 | 307ms | 815ms | 982ms |
| 120.0 | 130.0 | app2 | ok | 78 | 337ms | 838ms | 984ms |
| 130.0 | 140.0 | app1 | ok | 150 | 320ms | 808ms | 981ms |
| 130.0 | 140.0 | app2 | ok | 75 | 318ms | 812ms | 981ms |
| 140.0 | 150.0 | app1 | ok | 151 | 331ms | 806ms | 981ms |
| 140.0 | 150.0 | app2 | ok | 75 | 329ms | 803ms | 980ms |
| 150.0 | 160.0 | app1 | ok | 138 | 301ms | 818ms | 982ms |
| 150.0 | 160.0 | app2 | ok | 70 | 297ms | 841ms | 984ms |
| 160.0 | 170.0 | app1 | ok | 155 | 337ms | 820ms | 982ms |
| 160.0 | 170.0 | app2 | ok | 77 | 312ms | 825ms | 983ms |
| 170.0 | 180.0 | app1 | ok | 150 | 351ms | 840ms | 984ms |
| 170.0 | 180.0 | app2 | ok | 73 | 310ms | 808ms | 981ms |
| 180.0 | 190.0 | app1 | ok | 151 | 292ms | 778ms | 978ms |
| 180.0 | 190.0 | app2 | ok | 78 | 320ms | 814ms | 981ms |
| 190.0 | 200.0 | app1 | ok | 152 | 356ms | 835ms | 983ms |
| 190.0 | 200.0 | app2 | ok | 75 | 351ms | 850ms | 985ms |
| 200.0 | 210.0 | app1 | ok | 152 | 321ms | 823ms | 982ms |
| 200.0 | 210.0 | app2 | ok | 77 | 397ms | 867ms | 987ms |
| 210.0 | 220.0 | app1 | ok | 141 | 297ms | 793ms | 979ms |
| 210.0 | 220.0 | app2 | ok | 70 | 310ms | 816ms | 982ms |
| 220.0 | 230.0 | app1 | ok | 152 | 380ms | 857ms | 986ms |
| 220.0 | 230.0 | app2 | ok | 78 | 273ms | 795ms | 979ms |
| 230.0 | 240.0 | app1 | ok | 151 | 312ms | 816ms | 982ms |
| 230.0 | 240.0 | app2 | ok | 73 | 256ms | 757ms | 976ms |
| 240.0 | 250.0 | app1 | ok | 37 | 337ms | 815ms | 982ms |
| 240.0 | 250.0 | app2 | ok | 20 | 429ms | 875ms | 988ms |
| 250.0 | 259.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 250.0 | 259.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 4461210 | 221869 | 4683079.0 | 0.0% | 4818282.0 | 4904948.0 | -1.8% | True |
| app2 | 2232450 | 110808 | 2343258.0 | 0.0% | 2408080.0 | 2454066.0 | -1.9% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 3627 | 0 | 0 | 0 (never shed) | 0.00% | 66.7% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1815 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5442). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5442 | 0.051ms | 0.135ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 246863 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 3627 | 4323ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1815 | 4305ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5442 | 4318ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2750ms | 4744ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 3188ms | 4854ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 4369ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 4116ms | 4912ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 4282ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 4255ms | 4925ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 4286ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 4330ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 4294ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 4269ms | 4927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 4353ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 4296ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 4373ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 4360ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 4262ms | 4926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 4255ms | 4925ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 4348ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 4405ms | 4940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 4345ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 4373ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 4369ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 4360ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 4349ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 4312ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 4375ms | 4938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 4327ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 4335ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 4345ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 4299ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 4250ms | 4925ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 4363ms | 4944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 4333ms | 4950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 4346ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 4367ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 4357ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 4345ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app1 | ok | 4321ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app2 | ok | 4292ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app1 | ok | 4373ms | 4945ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app2 | ok | 4340ms | 4951ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app1 | ok | 4324ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app2 | ok | 4300ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 220.0 | app1 | ok | 4363ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 220.0 | app2 | ok | 4330ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 220.0 | 230.0 | app1 | ok | 4359ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 220.0 | 230.0 | app2 | ok | 4362ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 230.0 | 240.0 | app1 | ok | 4232ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 230.0 | 240.0 | app2 | ok | 4276ms | 4964ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 240.0 | 250.0 | app1 | ok | 4294ms | 4958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 240.0 | 250.0 | app2 | ok | 4154ms | 4985ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 250.0 | 259.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 250.0 | 259.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
