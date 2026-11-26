# Fairness benchmark: end-users-idle (uni310-l2-r1-end-users-idle)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-8448f688f-fjjwl` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T04:51:17Z` |
| Run end | `2026-11-26T04:55:35Z` |

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
| app1 | 20.0 | 64 | 3631 | 200=3631 | 4.2 | 4.8 | 4823108.0 | 66.7% | 66.7% | 0.0 | 66.6% | -0.0 | 66.6% | -0.0 | 5.4s | 98.9% | 3631.0 |
| app2 | 10.0 | 32 | 1818 | 200=1818 | 4.2 | 4.8 | 2415352.0 | 33.3% | 33.3% | 0.0 | 33.4% | 0.0 | 33.4% | 0.0 | 5.4s | 98.9% | 1818.0 |
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
| 0.0 | 10.0 | app1 | True | False | 25706.0 | 66.7% | 63.3% | -3.3 |
| 0.0 | 10.0 | app2 | True | False | 14882.0 | 33.3% | 36.7% | 3.3 |
| 10.0 | 20.0 | app1 | True | False | 205590.0 | 66.7% | 67.0% | 0.3 |
| 10.0 | 20.0 | app2 | True | False | 101374.0 | 33.3% | 33.0% | -0.3 |
| 20.0 | 30.0 | app1 | True | False | 204246.0 | 66.7% | 66.2% | -0.4 |
| 20.0 | 30.0 | app2 | True | False | 104118.0 | 33.3% | 33.8% | 0.4 |
| 30.0 | 40.0 | app1 | True | False | 205642.0 | 66.7% | 67.6% | 0.9 |
| 30.0 | 40.0 | app2 | True | False | 98674.0 | 33.3% | 32.4% | -0.9 |
| 40.0 | 50.0 | app1 | True | False | 200222.0 | 66.7% | 66.1% | -0.6 |
| 40.0 | 50.0 | app2 | True | False | 102804.0 | 33.3% | 33.9% | 0.6 |
| 50.0 | 60.0 | app1 | True | False | 205650.0 | 66.7% | 66.7% | 0.0 |
| 50.0 | 60.0 | app2 | True | False | 102696.0 | 33.3% | 33.3% | -0.0 |
| 60.0 | 70.0 | app1 | True | False | 208172.0 | 66.7% | 66.7% | 0.0 |
| 60.0 | 70.0 | app2 | True | False | 104036.0 | 33.3% | 33.3% | -0.0 |
| 70.0 | 80.0 | app1 | True | False | 201608.0 | 66.7% | 66.5% | -0.1 |
| 70.0 | 80.0 | app2 | True | False | 101454.0 | 33.3% | 33.5% | 0.1 |
| 80.0 | 90.0 | app1 | True | False | 201588.0 | 66.7% | 66.8% | 0.2 |
| 80.0 | 90.0 | app2 | True | False | 100098.0 | 33.3% | 33.2% | -0.2 |
| 90.0 | 100.0 | app1 | True | False | 204074.0 | 66.7% | 66.5% | -0.1 |
| 90.0 | 100.0 | app2 | True | False | 102720.0 | 33.3% | 33.5% | 0.1 |
| 100.0 | 110.0 | app1 | True | False | 205638.0 | 66.7% | 67.0% | 0.3 |
| 100.0 | 110.0 | app2 | True | False | 101340.0 | 33.3% | 33.0% | -0.3 |
| 110.0 | 120.0 | app1 | True | False | 205550.0 | 66.7% | 67.3% | 0.6 |
| 110.0 | 120.0 | app2 | True | False | 100006.0 | 33.3% | 32.7% | -0.6 |
| 120.0 | 130.0 | app1 | True | False | 200146.0 | 66.7% | 65.8% | -0.9 |
| 120.0 | 130.0 | app2 | True | False | 104218.0 | 33.3% | 34.2% | 0.9 |
| 130.0 | 140.0 | app1 | True | False | 201496.0 | 66.7% | 66.5% | -0.2 |
| 130.0 | 140.0 | app2 | True | False | 101548.0 | 33.3% | 33.5% | 0.2 |
| 140.0 | 151.0 | app1 | True | False | 204352.0 | 66.7% | 67.4% | 0.8 |
| 140.0 | 151.0 | app2 | True | False | 98648.0 | 33.3% | 32.6% | -0.8 |
| 151.0 | 161.0 | app1 | True | False | 205348.0 | 66.7% | 66.9% | 0.3 |
| 151.0 | 161.0 | app2 | True | False | 101378.0 | 33.3% | 33.1% | -0.3 |
| 161.0 | 171.0 | app1 | True | False | 197514.0 | 66.7% | 65.7% | -0.9 |
| 161.0 | 171.0 | app2 | True | False | 102922.0 | 33.3% | 34.3% | 0.9 |
| 171.0 | 181.0 | app1 | True | False | 204198.0 | 66.7% | 67.1% | 0.4 |
| 171.0 | 181.0 | app2 | True | False | 100188.0 | 33.3% | 32.9% | -0.4 |
| 181.0 | 191.0 | app1 | True | False | 203906.0 | 66.7% | 66.8% | 0.1 |
| 181.0 | 191.0 | app2 | True | False | 101530.0 | 33.3% | 33.2% | -0.1 |
| 191.0 | 201.0 | app1 | True | False | 201628.0 | 66.7% | 66.2% | -0.4 |
| 191.0 | 201.0 | app2 | True | False | 102794.0 | 33.3% | 33.8% | 0.4 |
| 201.0 | 211.0 | app1 | True | False | 202978.0 | 66.7% | 67.0% | 0.3 |
| 201.0 | 211.0 | app2 | True | False | 100088.0 | 33.3% | 33.0% | -0.3 |
| 211.0 | 221.0 | app1 | True | False | 198972.0 | 66.7% | 65.6% | -1.0 |
| 211.0 | 221.0 | app2 | True | False | 104206.0 | 33.3% | 34.4% | 1.0 |
| 221.0 | 231.0 | app1 | True | False | 206964.0 | 66.7% | 67.1% | 0.5 |
| 221.0 | 231.0 | app2 | True | False | 101360.0 | 33.3% | 32.9% | -0.5 |
| 231.0 | 241.0 | app1 | True | False | 202908.0 | 66.7% | 67.0% | 0.3 |
| 231.0 | 241.0 | app2 | True | False | 100068.0 | 33.3% | 33.0% | -0.3 |
| 241.0 | 251.0 | app1 | False | n/a | 119012.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 62202.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 142 | 62ms | 691ms | 969ms |
| 0.0 | 10.0 | app2 | ok | 71 | 8ms | 727ms | 973ms |
| 10.0 | 20.0 | app1 | ok | 147 | 309ms | 840ms | 984ms |
| 10.0 | 20.0 | app2 | ok | 73 | 352ms | 865ms | 986ms |
| 20.0 | 30.0 | app1 | ok | 157 | 287ms | 776ms | 978ms |
| 20.0 | 30.0 | app2 | ok | 81 | 343ms | 807ms | 981ms |
| 30.0 | 40.0 | app1 | ok | 151 | 343ms | 836ms | 984ms |
| 30.0 | 40.0 | app2 | ok | 74 | 341ms | 839ms | 984ms |
| 40.0 | 50.0 | app1 | ok | 145 | 397ms | 858ms | 986ms |
| 40.0 | 50.0 | app2 | ok | 72 | 395ms | 871ms | 987ms |
| 50.0 | 60.0 | app1 | ok | 160 | 351ms | 826ms | 983ms |
| 50.0 | 60.0 | app2 | ok | 80 | 380ms | 857ms | 986ms |
| 60.0 | 70.0 | app1 | ok | 150 | 389ms | 864ms | 986ms |
| 60.0 | 70.0 | app2 | ok | 75 | 345ms | 830ms | 983ms |
| 70.0 | 80.0 | app1 | ok | 149 | 288ms | 804ms | 980ms |
| 70.0 | 80.0 | app2 | ok | 75 | 342ms | 837ms | 984ms |
| 80.0 | 90.0 | app1 | ok | 149 | 299ms | 831ms | 983ms |
| 80.0 | 90.0 | app2 | ok | 75 | 358ms | 850ms | 985ms |
| 90.0 | 100.0 | app1 | ok | 149 | 315ms | 774ms | 977ms |
| 90.0 | 100.0 | app2 | ok | 74 | 317ms | 794ms | 979ms |
| 100.0 | 110.0 | app1 | ok | 156 | 368ms | 838ms | 984ms |
| 100.0 | 110.0 | app2 | ok | 77 | 363ms | 857ms | 986ms |
| 110.0 | 120.0 | app1 | ok | 148 | 338ms | 800ms | 980ms |
| 110.0 | 120.0 | app2 | ok | 74 | 375ms | 839ms | 984ms |
| 120.0 | 130.0 | app1 | ok | 152 | 289ms | 800ms | 980ms |
| 120.0 | 130.0 | app2 | ok | 75 | 321ms | 821ms | 982ms |
| 130.0 | 140.0 | app1 | ok | 143 | 248ms | 702ms | 970ms |
| 130.0 | 140.0 | app2 | ok | 73 | 293ms | 757ms | 976ms |
| 140.0 | 151.0 | app1 | ok | 148 | 294ms | 820ms | 982ms |
| 140.0 | 151.0 | app2 | ok | 75 | 256ms | 792ms | 979ms |
| 151.0 | 161.0 | app1 | ok | 161 | 321ms | 776ms | 978ms |
| 151.0 | 161.0 | app2 | ok | 77 | 404ms | 857ms | 986ms |
| 161.0 | 171.0 | app1 | ok | 141 | 342ms | 840ms | 984ms |
| 161.0 | 171.0 | app2 | ok | 72 | 289ms | 820ms | 982ms |
| 171.0 | 181.0 | app1 | ok | 148 | 269ms | 800ms | 980ms |
| 171.0 | 181.0 | app2 | ok | 75 | 332ms | 830ms | 983ms |
| 181.0 | 191.0 | app1 | ok | 154 | 377ms | 836ms | 984ms |
| 181.0 | 191.0 | app2 | ok | 77 | 335ms | 786ms | 979ms |
| 191.0 | 201.0 | app1 | ok | 148 | 352ms | 846ms | 985ms |
| 191.0 | 201.0 | app2 | ok | 75 | 337ms | 766ms | 977ms |
| 201.0 | 211.0 | app1 | ok | 149 | 345ms | 838ms | 984ms |
| 201.0 | 211.0 | app2 | ok | 72 | 350ms | 829ms | 983ms |
| 211.0 | 221.0 | app1 | ok | 149 | 342ms | 827ms | 983ms |
| 211.0 | 221.0 | app2 | ok | 73 | 353ms | 818ms | 982ms |
| 221.0 | 231.0 | app1 | ok | 159 | 338ms | 831ms | 983ms |
| 221.0 | 231.0 | app2 | ok | 84 | 398ms | 865ms | 986ms |
| 231.0 | 241.0 | app1 | ok | 145 | 307ms | 731ms | 973ms |
| 231.0 | 241.0 | app2 | ok | 72 | 243ms | 640ms | 964ms |
| 241.0 | 251.0 | app1 | ok | 31 | 243ms | 613ms | 961ms |
| 241.0 | 251.0 | app2 | ok | 17 | 339ms | 788ms | 979ms |
| 251.0 | 258.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 4466130 | 222388 | 4688518.0 | 0.0% | 4823108.0 | 4910906.0 | -1.8% | True |
| app2 | 2236140 | 111252 | 2347392.0 | 0.0% | 2415352.0 | 2458644.0 | -1.8% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 3631 | 0 | 0 | 0 (never shed) | 0.00% | 66.7% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1818 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5449). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5449 | 0.051ms | 0.137ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 244488 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 3631 | 4297ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1818 | 4288ms | 4943ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5449 | 4294ms | 4937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2647ms | 4800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2944ms | 4975ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 4315ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 4250ms | 4984ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 4326ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 4198ms | 4920ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 4296ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 4336ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 4351ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 4377ms | 4938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 4339ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 4345ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 4294ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 4260ms | 4926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 4341ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 4318ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 4358ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 4315ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 4281ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 4224ms | 4922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 4327ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 4342ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 4333ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 4315ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 4267ms | 4927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 4343ms | 4984ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 4310ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 4360ms | 4952ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 151.0 | app1 | ok | 4343ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 151.0 | app2 | ok | 4360ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 4232ms | 4923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 4240ms | 4943ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 4354ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 4333ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 4349ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 4351ms | 4935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 4326ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 4279ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 4317ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 4283ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 4245ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 4271ms | 4965ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 4309ms | 4957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 4260ms | 4926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 4214ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 4226ms | 5250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 4222ms | 4972ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 4209ms | 4984ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 4343ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 4303ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
