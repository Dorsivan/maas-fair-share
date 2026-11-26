# Fairness benchmark: end-users-idle (uni310-l3-r1-end-users-idle-2x)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5d57688bf8-x7247` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T05:26:29Z` |
| Run end | `2026-11-26T05:30:47Z` |

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
| app1 | 20.0 | 64 | 3635 | 200=3635 | 4.2 | 4.8 | 4829054.0 | 66.7% | 66.7% | 0.0 | 66.7% | 0.0 | 66.7% | 0.0 | 4.1s | 98.9% | 3635.0 |
| app2 | 10.0 | 32 | 1816 | 200=1816 | 4.2 | 4.8 | 2411664.0 | 33.3% | 33.3% | 0.0 | 33.3% | -0.0 | 33.3% | -0.0 | 4.1s | 98.9% | 1816.0 |
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
| 0.0 | 10.0 | app1 | True | False | 41892.0 | 66.7% | 65.9% | -0.7 |
| 0.0 | 10.0 | app2 | True | False | 21654.0 | 33.3% | 34.1% | 0.7 |
| 10.0 | 20.0 | app1 | True | False | 205578.0 | 66.7% | 66.7% | 0.0 |
| 10.0 | 20.0 | app2 | True | False | 102772.0 | 33.3% | 33.3% | -0.0 |
| 20.0 | 30.0 | app1 | True | False | 205406.0 | 66.7% | 67.2% | 0.6 |
| 20.0 | 30.0 | app2 | True | False | 100146.0 | 33.3% | 32.8% | -0.6 |
| 30.0 | 40.0 | app1 | True | False | 204156.0 | 66.7% | 66.5% | -0.2 |
| 30.0 | 40.0 | app2 | True | False | 102888.0 | 33.3% | 33.5% | 0.2 |
| 40.0 | 50.0 | app1 | True | False | 205454.0 | 66.7% | 66.7% | 0.0 |
| 40.0 | 50.0 | app2 | True | False | 102710.0 | 33.3% | 33.3% | -0.0 |
| 50.0 | 60.0 | app1 | True | False | 202804.0 | 66.7% | 66.4% | -0.3 |
| 50.0 | 60.0 | app2 | True | False | 102778.0 | 33.3% | 33.6% | 0.3 |
| 60.0 | 70.0 | app1 | True | False | 202822.0 | 66.7% | 67.2% | 0.6 |
| 60.0 | 70.0 | app2 | True | False | 98796.0 | 33.3% | 32.8% | -0.6 |
| 70.0 | 80.0 | app1 | True | False | 201554.0 | 66.7% | 66.2% | -0.4 |
| 70.0 | 80.0 | app2 | True | False | 102826.0 | 33.3% | 33.8% | 0.4 |
| 80.0 | 90.0 | app1 | True | False | 201672.0 | 66.7% | 66.8% | 0.2 |
| 80.0 | 90.0 | app2 | True | False | 100022.0 | 33.3% | 33.2% | -0.2 |
| 90.0 | 100.0 | app1 | True | False | 202922.0 | 66.7% | 67.0% | 0.3 |
| 90.0 | 100.0 | app2 | True | False | 100092.0 | 33.3% | 33.0% | -0.3 |
| 100.0 | 110.0 | app1 | True | False | 202864.0 | 66.7% | 66.4% | -0.3 |
| 100.0 | 110.0 | app2 | True | False | 102710.0 | 33.3% | 33.6% | 0.3 |
| 110.0 | 120.0 | app1 | True | False | 204188.0 | 66.7% | 66.5% | -0.1 |
| 110.0 | 120.0 | app2 | True | False | 102716.0 | 33.3% | 33.5% | 0.1 |
| 120.0 | 130.0 | app1 | True | False | 201594.0 | 66.7% | 66.8% | 0.1 |
| 120.0 | 130.0 | app2 | True | False | 100142.0 | 33.3% | 33.2% | -0.1 |
| 130.0 | 140.0 | app1 | True | False | 205508.0 | 66.7% | 67.3% | 0.6 |
| 130.0 | 140.0 | app2 | True | False | 99936.0 | 33.3% | 32.7% | -0.6 |
| 140.0 | 150.0 | app1 | True | False | 200216.0 | 66.7% | 66.1% | -0.6 |
| 140.0 | 150.0 | app2 | True | False | 102704.0 | 33.3% | 33.9% | 0.6 |
| 150.0 | 160.0 | app1 | True | False | 201584.0 | 66.7% | 66.8% | 0.1 |
| 150.0 | 160.0 | app2 | True | False | 100184.0 | 33.3% | 33.2% | -0.1 |
| 160.0 | 171.0 | app1 | True | False | 200034.0 | 66.7% | 65.5% | -1.2 |
| 160.0 | 171.0 | app2 | True | False | 105502.0 | 33.3% | 34.5% | 1.2 |
| 171.0 | 181.0 | app1 | True | False | 204084.0 | 66.7% | 67.4% | 0.7 |
| 171.0 | 181.0 | app2 | True | False | 98704.0 | 33.3% | 32.6% | -0.7 |
| 181.0 | 191.0 | app1 | True | False | 205398.0 | 66.7% | 66.9% | 0.3 |
| 181.0 | 191.0 | app2 | True | False | 101546.0 | 33.3% | 33.1% | -0.3 |
| 191.0 | 201.0 | app1 | True | False | 201368.0 | 66.7% | 66.8% | 0.1 |
| 191.0 | 201.0 | app2 | True | False | 100170.0 | 33.3% | 33.2% | -0.1 |
| 201.0 | 211.0 | app1 | True | False | 201568.0 | 66.7% | 66.2% | -0.4 |
| 201.0 | 211.0 | app2 | True | False | 102798.0 | 33.3% | 33.8% | 0.4 |
| 211.0 | 221.0 | app1 | True | False | 204140.0 | 66.7% | 67.4% | 0.7 |
| 211.0 | 221.0 | app2 | True | False | 98806.0 | 33.3% | 32.6% | -0.7 |
| 221.0 | 231.0 | app1 | True | False | 200234.0 | 66.7% | 66.4% | -0.3 |
| 221.0 | 231.0 | app2 | True | False | 101518.0 | 33.3% | 33.6% | 0.3 |
| 231.0 | 241.0 | app1 | True | False | 201634.0 | 66.7% | 66.2% | -0.4 |
| 231.0 | 241.0 | app2 | True | False | 102822.0 | 33.3% | 33.8% | 0.4 |
| 241.0 | 251.0 | app1 | False | n/a | 120380.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 56722.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 150 | 1ms | 722ms | 972ms |
| 0.0 | 10.0 | app2 | ok | 75 | 18ms | 712ms | 971ms |
| 10.0 | 20.0 | app1 | ok | 154 | 321ms | 825ms | 983ms |
| 10.0 | 20.0 | app2 | ok | 78 | 348ms | 844ms | 984ms |
| 20.0 | 30.0 | app1 | ok | 152 | 290ms | 805ms | 981ms |
| 20.0 | 30.0 | app2 | ok | 75 | 290ms | 803ms | 980ms |
| 30.0 | 40.0 | app1 | ok | 152 | 341ms | 848ms | 985ms |
| 30.0 | 40.0 | app2 | ok | 76 | 330ms | 819ms | 982ms |
| 40.0 | 50.0 | app1 | ok | 155 | 341ms | 828ms | 983ms |
| 40.0 | 50.0 | app2 | ok | 77 | 315ms | 807ms | 981ms |
| 50.0 | 60.0 | app1 | ok | 144 | 325ms | 805ms | 981ms |
| 50.0 | 60.0 | app2 | ok | 72 | 340ms | 820ms | 982ms |
| 60.0 | 70.0 | app1 | ok | 151 | 341ms | 832ms | 983ms |
| 60.0 | 70.0 | app2 | ok | 75 | 280ms | 803ms | 980ms |
| 70.0 | 80.0 | app1 | ok | 152 | 297ms | 815ms | 981ms |
| 70.0 | 80.0 | app2 | ok | 78 | 302ms | 805ms | 980ms |
| 80.0 | 90.0 | app1 | ok | 149 | 323ms | 831ms | 983ms |
| 80.0 | 90.0 | app2 | ok | 75 | 325ms | 812ms | 981ms |
| 90.0 | 100.0 | app1 | ok | 152 | 380ms | 854ms | 985ms |
| 90.0 | 100.0 | app2 | ok | 75 | 319ms | 792ms | 979ms |
| 100.0 | 110.0 | app1 | ok | 152 | 317ms | 823ms | 982ms |
| 100.0 | 110.0 | app2 | ok | 76 | 370ms | 848ms | 985ms |
| 110.0 | 120.0 | app1 | ok | 147 | 305ms | 796ms | 980ms |
| 110.0 | 120.0 | app2 | ok | 73 | 321ms | 818ms | 982ms |
| 120.0 | 130.0 | app1 | ok | 145 | 305ms | 842ms | 984ms |
| 120.0 | 130.0 | app2 | ok | 72 | 298ms | 811ms | 981ms |
| 130.0 | 140.0 | app1 | ok | 153 | 358ms | 841ms | 984ms |
| 130.0 | 140.0 | app2 | ok | 77 | 316ms | 743ms | 974ms |
| 140.0 | 150.0 | app1 | ok | 152 | 330ms | 819ms | 982ms |
| 140.0 | 150.0 | app2 | ok | 78 | 361ms | 838ms | 984ms |
| 150.0 | 160.0 | app1 | ok | 151 | 281ms | 828ms | 983ms |
| 150.0 | 160.0 | app2 | ok | 73 | 355ms | 834ms | 983ms |
| 160.0 | 171.0 | app1 | ok | 150 | 345ms | 817ms | 982ms |
| 160.0 | 171.0 | app2 | ok | 78 | 298ms | 823ms | 982ms |
| 171.0 | 181.0 | app1 | ok | 142 | 325ms | 803ms | 980ms |
| 171.0 | 181.0 | app2 | ok | 69 | 338ms | 797ms | 980ms |
| 181.0 | 191.0 | app1 | ok | 151 | 328ms | 843ms | 984ms |
| 181.0 | 191.0 | app2 | ok | 77 | 339ms | 833ms | 983ms |
| 191.0 | 201.0 | app1 | ok | 153 | 344ms | 834ms | 983ms |
| 191.0 | 201.0 | app2 | ok | 72 | 356ms | 829ms | 983ms |
| 201.0 | 211.0 | app1 | ok | 148 | 333ms | 832ms | 983ms |
| 201.0 | 211.0 | app2 | ok | 78 | 405ms | 874ms | 987ms |
| 211.0 | 221.0 | app1 | ok | 150 | 362ms | 830ms | 983ms |
| 211.0 | 221.0 | app2 | ok | 74 | 312ms | 832ms | 983ms |
| 221.0 | 231.0 | app1 | ok | 154 | 362ms | 849ms | 985ms |
| 221.0 | 231.0 | app2 | ok | 75 | 275ms | 750ms | 975ms |
| 231.0 | 241.0 | app1 | ok | 149 | 326ms | 799ms | 980ms |
| 231.0 | 241.0 | app2 | ok | 76 | 352ms | 827ms | 983ms |
| 241.0 | 251.0 | app1 | ok | 27 | 218ms | 775ms | 978ms |
| 241.0 | 251.0 | app2 | ok | 12 | 250ms | 850ms | 985ms |
| 251.0 | 258.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 4471050 | 222296 | 4693346.0 | 0.0% | 4829054.0 | 4915642.0 | -1.8% | True |
| app2 | 2233680 | 111284 | 2344964.0 | 0.0% | 2411664.0 | 2456248.0 | -1.8% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 3635 | 0 | 0 | 0 (never shed) | 0.00% | 66.7% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1816 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5451). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5451 | 0.051ms | 0.165ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 245397 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 3635 | 4311ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1816 | 4301ms | 4946ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5451 | 4308ms | 4940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 3086ms | 4812ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 3179ms | 4879ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 4232ms | 4952ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 4250ms | 4962ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 4183ms | 4918ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 4227ms | 4984ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 4289ms | 4955ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 4220ms | 5367ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 4333ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 4269ms | 4927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 4370ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 4296ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 4336ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 4324ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 4379ms | 4938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 4296ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 4384ms | 4938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 4383ms | 4938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 4336ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 4351ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 4370ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 4309ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 4349ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 4321ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 4384ms | 4938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 4327ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 4309ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 4339ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 4339ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 4296ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 4262ms | 4926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 4250ms | 4944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 171.0 | app1 | ok | 4207ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 171.0 | app2 | ok | 4271ms | 5025ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 4317ms | 4940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 4298ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 4339ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 4364ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 4229ms | 4942ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 4213ms | 4921ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 4316ms | 4967ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 4298ms | 5240ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 4360ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 4392ms | 4939ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 4345ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 4395ms | 4940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 4355ms | 4943ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 4351ms | 4951ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 4355ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 4382ms | 4938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
