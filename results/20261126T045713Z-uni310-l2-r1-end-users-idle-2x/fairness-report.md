# Fairness benchmark: end-users-idle (uni310-l2-r1-end-users-idle-2x)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-8448f688f-z74j5` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T04:58:43Z` |
| Run end | `2026-11-26T05:03:02Z` |

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
| app1 | 20.0 | 64 | 3643 | 200=3643 | 4.2 | 4.8 | 4838756.0 | 66.7% | 66.7% | 0.0 | 66.7% | 0.0 | 66.7% | -0.0 | 4.1s | 98.9% | 3643.0 |
| app2 | 10.0 | 32 | 1822 | 200=1822 | 4.2 | 4.8 | 2419342.0 | 33.3% | 33.3% | 0.0 | 33.3% | -0.0 | 33.3% | 0.0 | 4.1s | 98.9% | 1822.0 |
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
| 0.0 | 10.0 | app1 | True | False | 41820.0 | 66.7% | 68.8% | 2.1 |
| 0.0 | 10.0 | app2 | True | False | 18956.0 | 33.3% | 31.2% | -2.1 |
| 10.0 | 20.0 | app1 | True | False | 202836.0 | 66.7% | 66.1% | -0.6 |
| 10.0 | 20.0 | app2 | True | False | 104200.0 | 33.3% | 33.9% | 0.6 |
| 20.0 | 30.0 | app1 | True | False | 204410.0 | 66.7% | 66.8% | 0.2 |
| 20.0 | 30.0 | app2 | True | False | 101504.0 | 33.3% | 33.2% | -0.2 |
| 30.0 | 40.0 | app1 | True | False | 206950.0 | 66.7% | 66.8% | 0.2 |
| 30.0 | 40.0 | app2 | True | False | 102730.0 | 33.3% | 33.2% | -0.2 |
| 40.0 | 50.0 | app1 | True | False | 205524.0 | 66.7% | 67.0% | 0.3 |
| 40.0 | 50.0 | app2 | True | False | 101434.0 | 33.3% | 33.0% | -0.3 |
| 50.0 | 60.0 | app1 | True | False | 200192.0 | 66.7% | 66.1% | -0.6 |
| 50.0 | 60.0 | app2 | True | False | 102866.0 | 33.3% | 33.9% | 0.6 |
| 60.0 | 71.0 | app1 | True | False | 205648.0 | 66.7% | 67.6% | 0.9 |
| 60.0 | 71.0 | app2 | True | False | 98728.0 | 33.3% | 32.4% | -0.9 |
| 71.0 | 81.0 | app1 | True | False | 202842.0 | 66.7% | 66.1% | -0.6 |
| 71.0 | 81.0 | app2 | True | False | 104246.0 | 33.3% | 33.9% | 0.6 |
| 81.0 | 91.0 | app1 | True | False | 204108.0 | 66.7% | 66.2% | -0.4 |
| 81.0 | 91.0 | app2 | True | False | 104082.0 | 33.3% | 33.8% | 0.4 |
| 91.0 | 101.0 | app1 | True | False | 206906.0 | 66.7% | 67.4% | 0.7 |
| 91.0 | 101.0 | app2 | True | False | 100160.0 | 33.3% | 32.6% | -0.7 |
| 101.0 | 111.0 | app1 | True | False | 204080.0 | 66.7% | 66.5% | -0.1 |
| 101.0 | 111.0 | app2 | True | False | 102668.0 | 33.3% | 33.5% | 0.1 |
| 111.0 | 121.0 | app1 | True | False | 202686.0 | 66.7% | 66.3% | -0.3 |
| 111.0 | 121.0 | app2 | True | False | 102894.0 | 33.3% | 33.7% | 0.3 |
| 121.0 | 131.0 | app1 | True | False | 204176.0 | 66.7% | 66.8% | 0.2 |
| 121.0 | 131.0 | app2 | True | False | 101380.0 | 33.3% | 33.2% | -0.2 |
| 131.0 | 141.0 | app1 | True | False | 209380.0 | 66.7% | 67.1% | 0.4 |
| 131.0 | 141.0 | app2 | True | False | 102614.0 | 33.3% | 32.9% | -0.4 |
| 141.0 | 151.0 | app1 | True | False | 201666.0 | 66.7% | 66.6% | -0.1 |
| 141.0 | 151.0 | app2 | True | False | 101352.0 | 33.3% | 33.4% | 0.1 |
| 151.0 | 161.0 | app1 | True | False | 200230.0 | 66.7% | 66.4% | -0.3 |
| 151.0 | 161.0 | app2 | True | False | 101438.0 | 33.3% | 33.6% | 0.3 |
| 161.0 | 171.0 | app1 | True | False | 204022.0 | 66.7% | 66.8% | 0.1 |
| 161.0 | 171.0 | app2 | True | False | 101542.0 | 33.3% | 33.2% | -0.1 |
| 171.0 | 181.0 | app1 | True | False | 200416.0 | 66.7% | 66.4% | -0.3 |
| 171.0 | 181.0 | app2 | True | False | 101422.0 | 33.3% | 33.6% | 0.3 |
| 181.0 | 191.0 | app1 | True | False | 202898.0 | 66.7% | 67.0% | 0.3 |
| 181.0 | 191.0 | app2 | True | False | 100014.0 | 33.3% | 33.0% | -0.3 |
| 191.0 | 201.0 | app1 | True | False | 205364.0 | 66.7% | 66.6% | -0.0 |
| 191.0 | 201.0 | app2 | True | False | 102796.0 | 33.3% | 33.4% | 0.0 |
| 201.0 | 211.0 | app1 | True | False | 198956.0 | 66.7% | 66.2% | -0.4 |
| 201.0 | 211.0 | app2 | True | False | 101402.0 | 33.3% | 33.8% | 0.4 |
| 211.0 | 221.0 | app1 | True | False | 204246.0 | 66.7% | 67.1% | 0.4 |
| 211.0 | 221.0 | app2 | True | False | 100084.0 | 33.3% | 32.9% | -0.4 |
| 221.0 | 231.0 | app1 | True | False | 205550.0 | 66.7% | 66.4% | -0.3 |
| 221.0 | 231.0 | app2 | True | False | 103942.0 | 33.3% | 33.6% | 0.3 |
| 231.0 | 241.0 | app1 | True | False | 203004.0 | 66.7% | 66.7% | 0.0 |
| 231.0 | 241.0 | app2 | True | False | 101460.0 | 33.3% | 33.3% | -0.0 |
| 241.0 | 251.0 | app1 | False | n/a | 110846.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 55428.0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 156 | 10ms | 700ms | 970ms |
| 0.0 | 10.0 | app2 | ok | 78 | 100ms | 700ms | 970ms |
| 10.0 | 20.0 | app1 | ok | 149 | 302ms | 804ms | 980ms |
| 10.0 | 20.0 | app2 | ok | 74 | 233ms | 782ms | 978ms |
| 20.0 | 30.0 | app1 | ok | 152 | 307ms | 783ms | 978ms |
| 20.0 | 30.0 | app2 | ok | 77 | 338ms | 797ms | 980ms |
| 30.0 | 40.0 | app1 | ok | 145 | 288ms | 618ms | 962ms |
| 30.0 | 40.0 | app2 | ok | 72 | 336ms | 760ms | 976ms |
| 40.0 | 50.0 | app1 | ok | 159 | 340ms | 806ms | 981ms |
| 40.0 | 50.0 | app2 | ok | 81 | 307ms | 816ms | 982ms |
| 50.0 | 60.0 | app1 | ok | 151 | 336ms | 811ms | 981ms |
| 50.0 | 60.0 | app2 | ok | 75 | 319ms | 792ms | 979ms |
| 60.0 | 71.0 | app1 | ok | 152 | 309ms | 810ms | 981ms |
| 60.0 | 71.0 | app2 | ok | 73 | 359ms | 841ms | 984ms |
| 71.0 | 81.0 | app1 | ok | 148 | 246ms | 715ms | 972ms |
| 71.0 | 81.0 | app2 | ok | 75 | 322ms | 803ms | 980ms |
| 81.0 | 91.0 | app1 | ok | 147 | 301ms | 796ms | 980ms |
| 81.0 | 91.0 | app2 | ok | 75 | 247ms | 803ms | 980ms |
| 91.0 | 101.0 | app1 | ok | 152 | 296ms | 789ms | 979ms |
| 91.0 | 101.0 | app2 | ok | 76 | 278ms | 729ms | 973ms |
| 101.0 | 111.0 | app1 | ok | 149 | 302ms | 787ms | 979ms |
| 101.0 | 111.0 | app2 | ok | 74 | 321ms | 832ms | 983ms |
| 111.0 | 121.0 | app1 | ok | 150 | 362ms | 826ms | 983ms |
| 111.0 | 121.0 | app2 | ok | 75 | 290ms | 803ms | 980ms |
| 121.0 | 131.0 | app1 | ok | 158 | 333ms | 832ms | 983ms |
| 121.0 | 131.0 | app2 | ok | 79 | 310ms | 820ms | 982ms |
| 131.0 | 141.0 | app1 | ok | 156 | 267ms | 795ms | 979ms |
| 131.0 | 141.0 | app2 | ok | 77 | 335ms | 840ms | 984ms |
| 141.0 | 151.0 | app1 | ok | 142 | 300ms | 797ms | 980ms |
| 141.0 | 151.0 | app2 | ok | 71 | 303ms | 763ms | 976ms |
| 151.0 | 161.0 | app1 | ok | 147 | 323ms | 796ms | 980ms |
| 151.0 | 161.0 | app2 | ok | 75 | 338ms | 812ms | 981ms |
| 161.0 | 171.0 | app1 | ok | 160 | 339ms | 843ms | 984ms |
| 161.0 | 171.0 | app2 | ok | 79 | 292ms | 768ms | 977ms |
| 171.0 | 181.0 | app1 | ok | 145 | 358ms | 835ms | 984ms |
| 171.0 | 181.0 | app2 | ok | 73 | 365ms | 841ms | 984ms |
| 181.0 | 191.0 | app1 | ok | 146 | 333ms | 791ms | 979ms |
| 181.0 | 191.0 | app2 | ok | 75 | 292ms | 750ms | 975ms |
| 191.0 | 201.0 | app1 | ok | 151 | 317ms | 828ms | 983ms |
| 191.0 | 201.0 | app2 | ok | 73 | 338ms | 808ms | 981ms |
| 201.0 | 211.0 | app1 | ok | 149 | 301ms | 799ms | 980ms |
| 201.0 | 211.0 | app2 | ok | 77 | 312ms | 797ms | 980ms |
| 211.0 | 221.0 | app1 | ok | 149 | 318ms | 818ms | 982ms |
| 211.0 | 221.0 | app2 | ok | 73 | 304ms | 818ms | 982ms |
| 221.0 | 231.0 | app1 | ok | 154 | 306ms | 780ms | 978ms |
| 221.0 | 231.0 | app2 | ok | 79 | 379ms | 828ms | 983ms |
| 231.0 | 241.0 | app1 | ok | 151 | 308ms | 796ms | 980ms |
| 231.0 | 241.0 | app2 | ok | 73 | 322ms | 719ms | 972ms |
| 241.0 | 251.0 | app1 | ok | 25 | 403ms | 861ms | 986ms |
| 241.0 | 251.0 | app2 | ok | 13 | 438ms | 870ms | 987ms |
| 251.0 | 259.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 259.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 4480890 | 222908 | 4703798.0 | 0.0% | 4838756.0 | 4926706.0 | -1.8% | True |
| app2 | 2241060 | 111399 | 2352459.0 | 0.0% | 2419342.0 | 2463858.0 | -1.8% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 3643 | 0 | 0 | 0 (never shed) | 0.00% | 66.7% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1822 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5465). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5465 | 0.051ms | 0.118ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 245196 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 3643 | 4276ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1822 | 4268ms | 4945ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5465 | 4273ms | 4939ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2850ms | 5578ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2808ms | 5530ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 4242ms | 4924ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 4230ms | 4923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 4294ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 4250ms | 4925ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 4278ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 4283ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 4224ms | 4922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 4240ms | 4943ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 4226ms | 4942ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 4182ms | 4959ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 71.0 | app1 | ok | 4149ms | 4936ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 71.0 | app2 | ok | 4291ms | 5392ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app1 | ok | 4315ms | 4940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app2 | ok | 4298ms | 4964ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 4294ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app2 | ok | 4292ms | 4946ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 4311ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 4315ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 4260ms | 4926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 4283ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 4245ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 4239ms | 4983ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 4326ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 4318ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 4262ms | 4926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 4208ms | 4921ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 4319ms | 4958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 4270ms | 4945ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 4288ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 4235ms | 4923ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 4314ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 4318ms | 4932ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 4339ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 4279ms | 4928ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 4298ms | 4947ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 4300ms | 4966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 4284ms | 4955ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 4260ms | 4944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 4286ms | 4929ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 4330ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 4314ms | 4931ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 4302ms | 4930ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 4333ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 4274ms | 4927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 4342ms | 4934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 4395ms | 4940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 4328ms | 4933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 4268ms | 4927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 259.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 259.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
