# Fairness benchmark: app1-idle (uni310-l2-r1-a4-app1-idle)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 0.0 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 0.0 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-idle` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-8448f688f-2lk4p` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T04:24:36Z` |
| Run end | `2026-11-26T04:28:53Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 27 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/27 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 71.00 | 2.2188 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| app2 | 10.0 | 32 | 729 | 200=729 | 10.7 | 13.3 | 964198.0 | 13.3% | 13.3% | 0.0 | 13.3% | 0.0 | 13.3% | 0.0 | 77.5s | 98.9% | 729.0 |
| end-users | 65.0 | 208 | 4738 | 200=4738 | 10.7 | 13.3 | 6259254.0 | 86.7% | 86.7% | 0.0 | 86.7% | -0.0 | 86.7% | -0.0 | 77.5s | 98.9% | 4738.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app2: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 0.0 | 0.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app2 | True | False | 4054.0 | 13.3% | 23.1% | 9.7 |
| 0.0 | 10.0 | end-users | True | False | 13522.0 | 86.7% | 76.9% | -9.7 |
| 10.0 | 20.0 | app2 | True | False | 36548.0 | 13.3% | 12.9% | -0.4 |
| 10.0 | 20.0 | end-users | True | False | 245954.0 | 86.7% | 87.1% | 0.4 |
| 20.0 | 30.0 | app2 | True | False | 37884.0 | 13.3% | 13.5% | 0.1 |
| 20.0 | 30.0 | end-users | True | False | 243372.0 | 86.7% | 86.5% | -0.1 |
| 30.0 | 40.0 | app2 | True | False | 40564.0 | 13.3% | 13.4% | 0.0 |
| 30.0 | 40.0 | end-users | True | False | 262536.0 | 86.7% | 86.6% | -0.0 |
| 40.0 | 50.0 | app2 | True | False | 41930.0 | 13.3% | 13.5% | 0.2 |
| 40.0 | 50.0 | end-users | True | False | 267716.0 | 86.7% | 86.5% | -0.2 |
| 50.0 | 60.0 | app2 | True | False | 39280.0 | 13.3% | 12.9% | -0.5 |
| 50.0 | 60.0 | end-users | True | False | 266384.0 | 86.7% | 87.1% | 0.5 |
| 60.0 | 70.0 | app2 | True | False | 40612.0 | 13.3% | 13.3% | -0.0 |
| 60.0 | 70.0 | end-users | True | False | 265062.0 | 86.7% | 86.7% | 0.0 |
| 70.0 | 80.0 | app2 | True | False | 41884.0 | 13.3% | 13.7% | 0.4 |
| 70.0 | 80.0 | end-users | True | False | 263554.0 | 86.7% | 86.3% | -0.4 |
| 80.0 | 90.0 | app2 | True | False | 39250.0 | 13.3% | 12.9% | -0.4 |
| 80.0 | 90.0 | end-users | True | False | 263874.0 | 86.7% | 87.1% | 0.4 |
| 90.0 | 100.0 | app2 | True | False | 39178.0 | 13.3% | 13.2% | -0.1 |
| 90.0 | 100.0 | end-users | True | False | 256784.0 | 86.7% | 86.8% | 0.1 |
| 100.0 | 110.0 | app2 | True | False | 43216.0 | 13.3% | 14.1% | 0.8 |
| 100.0 | 110.0 | end-users | True | False | 263520.0 | 86.7% | 85.9% | -0.8 |
| 110.0 | 120.0 | app2 | True | False | 40484.0 | 13.3% | 13.3% | -0.0 |
| 110.0 | 120.0 | end-users | True | False | 263772.0 | 86.7% | 86.7% | 0.0 |
| 120.0 | 130.0 | app2 | True | False | 39192.0 | 13.3% | 13.2% | -0.1 |
| 120.0 | 130.0 | end-users | True | False | 256754.0 | 86.7% | 86.8% | 0.1 |
| 130.0 | 140.0 | app2 | True | False | 37888.0 | 13.3% | 12.4% | -0.9 |
| 130.0 | 140.0 | end-users | True | False | 267710.0 | 86.7% | 87.6% | 0.9 |
| 140.0 | 150.0 | app2 | True | False | 41954.0 | 13.3% | 13.9% | 0.5 |
| 140.0 | 150.0 | end-users | True | False | 260960.0 | 86.7% | 86.1% | -0.5 |
| 150.0 | 160.0 | app2 | True | False | 40678.0 | 13.3% | 13.9% | 0.5 |
| 150.0 | 160.0 | end-users | True | False | 253002.0 | 86.7% | 86.1% | -0.5 |
| 160.0 | 170.0 | app2 | True | False | 40496.0 | 13.3% | 13.5% | 0.2 |
| 160.0 | 170.0 | end-users | True | False | 259540.0 | 86.7% | 86.5% | -0.2 |
| 170.0 | 181.0 | app2 | True | False | 39238.0 | 13.3% | 12.8% | -0.5 |
| 170.0 | 181.0 | end-users | True | False | 266534.0 | 86.7% | 87.2% | 0.5 |
| 181.0 | 191.0 | app2 | True | False | 40644.0 | 13.3% | 13.4% | 0.1 |
| 181.0 | 191.0 | end-users | True | False | 262538.0 | 86.7% | 86.6% | -0.1 |
| 191.0 | 201.0 | app2 | True | False | 39114.0 | 13.3% | 13.0% | -0.3 |
| 191.0 | 201.0 | end-users | True | False | 261112.0 | 86.7% | 87.0% | 0.3 |
| 201.0 | 211.0 | app2 | True | False | 40616.0 | 13.3% | 13.4% | 0.1 |
| 201.0 | 211.0 | end-users | True | False | 262486.0 | 86.7% | 86.6% | -0.1 |
| 211.0 | 221.0 | app2 | True | False | 32396.0 | 13.3% | 13.0% | -0.3 |
| 211.0 | 221.0 | end-users | True | False | 216240.0 | 86.7% | 87.0% | 0.3 |
| 221.0 | 231.0 | app2 | True | False | 40632.0 | 13.3% | 13.8% | 0.5 |
| 221.0 | 231.0 | end-users | True | False | 252808.0 | 86.7% | 86.2% | -0.5 |
| 231.0 | 241.0 | app2 | True | False | 40512.0 | 13.3% | 13.2% | -0.1 |
| 231.0 | 241.0 | end-users | True | False | 266376.0 | 86.7% | 86.8% | 0.1 |
| 241.0 | 251.0 | app2 | False | n/a | 40522.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 266096.0 | n/a | n/a | n/a |
| 251.0 | 257.0 | app2 | False | n/a | 5432.0 | n/a | n/a | n/a |
| 251.0 | 257.0 | end-users | False | n/a | 31048.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app2 | ok | 30 | 0ms | 2200ms | 2470ms |
| 0.0 | 10.0 | end-users | ok | 189 | 0ms | 2158ms | 2466ms |
| 10.0 | 20.0 | app2 | ok | 30 | 6591ms | 9318ms | 9932ms |
| 10.0 | 20.0 | end-users | ok | 198 | 6439ms | 9288ms | 9929ms |
| 20.0 | 30.0 | app2 | ok | 39 | 5357ms | 9071ms | 9907ms |
| 20.0 | 30.0 | end-users | ok | 254 | 5559ms | 9112ms | 9911ms |
| 30.0 | 40.0 | app2 | ok | 17 | 6964ms | 9393ms | 9939ms |
| 30.0 | 40.0 | end-users | ok | 111 | 7016ms | 9403ms | 9940ms |
| 40.0 | 50.0 | app2 | ok | 33 | 6944ms | 9389ms | 9939ms |
| 40.0 | 50.0 | end-users | ok | 214 | 6777ms | 9355ms | 9936ms |
| 50.0 | 60.0 | app2 | ok | 28 | 6500ms | 9300ms | 9930ms |
| 50.0 | 60.0 | end-users | ok | 175 | 6414ms | 9283ms | 9928ms |
| 60.0 | 70.0 | app2 | ok | 32 | 6522ms | 9304ms | 9930ms |
| 60.0 | 70.0 | end-users | ok | 211 | 6933ms | 9387ms | 9939ms |
| 70.0 | 80.0 | app2 | ok | 30 | 5588ms | 9118ms | 9912ms |
| 70.0 | 80.0 | end-users | ok | 190 | 6169ms | 9234ms | 9923ms |
| 80.0 | 90.0 | app2 | ok | 36 | 5714ms | 9143ms | 9914ms |
| 80.0 | 90.0 | end-users | ok | 236 | 6776ms | 9355ms | 9936ms |
| 90.0 | 100.0 | app2 | ok | 22 | 6071ms | 9214ms | 9921ms |
| 90.0 | 100.0 | end-users | ok | 151 | 6262ms | 9252ms | 9925ms |
| 100.0 | 110.0 | app2 | ok | 32 | 6364ms | 9273ms | 9927ms |
| 100.0 | 110.0 | end-users | ok | 207 | 6920ms | 9384ms | 9938ms |
| 110.0 | 120.0 | app2 | ok | 31 | 6125ms | 9225ms | 9922ms |
| 110.0 | 120.0 | end-users | ok | 196 | 6016ms | 9203ms | 9920ms |
| 120.0 | 130.0 | app2 | ok | 33 | 6250ms | 9250ms | 9925ms |
| 120.0 | 130.0 | end-users | ok | 222 | 6036ms | 9207ms | 9921ms |
| 130.0 | 140.0 | app2 | ok | 33 | 4338ms | 8625ms | 9862ms |
| 130.0 | 140.0 | end-users | ok | 214 | 4588ms | 8824ms | 9882ms |
| 140.0 | 150.0 | app2 | ok | 19 | 6042ms | 9208ms | 9921ms |
| 140.0 | 150.0 | end-users | ok | 116 | 6506ms | 9301ms | 9930ms |
| 150.0 | 160.0 | app2 | ok | 33 | 6413ms | 9283ms | 9928ms |
| 150.0 | 160.0 | end-users | ok | 224 | 6387ms | 9277ms | 9928ms |
| 160.0 | 170.0 | app2 | ok | 32 | 7037ms | 9407ms | 9941ms |
| 160.0 | 170.0 | end-users | ok | 207 | 6725ms | 9345ms | 9934ms |
| 170.0 | 181.0 | app2 | ok | 25 | 7283ms | 9457ms | 9946ms |
| 170.0 | 181.0 | end-users | ok | 158 | 6865ms | 9373ms | 9937ms |
| 181.0 | 191.0 | app2 | ok | 26 | 6750ms | 9350ms | 9935ms |
| 181.0 | 191.0 | end-users | ok | 173 | 6594ms | 9319ms | 9932ms |
| 191.0 | 201.0 | app2 | ok | 32 | 6190ms | 9238ms | 9924ms |
| 191.0 | 201.0 | end-users | ok | 209 | 6130ms | 9226ms | 9923ms |
| 201.0 | 211.0 | app2 | ok | 41 | 6204ms | 9241ms | 9924ms |
| 201.0 | 211.0 | end-users | ok | 264 | 6048ms | 9210ms | 9921ms |
| 211.0 | 221.0 | app2 | ok | 16 | 6667ms | 9333ms | 9933ms |
| 211.0 | 221.0 | end-users | ok | 105 | 6759ms | 9352ms | 9935ms |
| 221.0 | 231.0 | app2 | ok | 34 | 6304ms | 9261ms | 9926ms |
| 221.0 | 231.0 | end-users | ok | 216 | 6143ms | 9229ms | 9923ms |
| 231.0 | 241.0 | app2 | ok | 23 | 7125ms | 9425ms | 9942ms |
| 231.0 | 241.0 | end-users | ok | 150 | 7093ms | 9419ms | 9942ms |
| 241.0 | 251.0 | app2 | ok | 22 | 6765ms | 9353ms | 9935ms |
| 241.0 | 251.0 | end-users | ok | 148 | 7063ms | 9413ms | 9941ms |
| 251.0 | 257.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 257.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app2 | 896670 | 44600 | 941270.0 | 0.0% | 964198.0 | 985870.0 | -2.2% | True |
| end-users | 5827740 | 289416 | 6117156.0 | 0.0% | 6259254.0 | 6406572.0 | -2.3% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app2 | 729 | 0 | 0 | 0 (never shed) | 0.00% | 13.3% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 4738 | 0 | 0 | 0 (never shed) | 0.00% | 86.7% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5467). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5467 | 0.051ms | 0.101ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 243616 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app2 | ok | 729 | 11141ms | 14624ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 4738 | 11184ms | 14633ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5467 | 11178ms | 14632ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app2 | ok | 2833ms | 5050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2895ms | 5312ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 9875ms | 14481ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 9178ms | 14266ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 11667ms | 14667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 11763ms | 14676ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 11250ms | 14625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 11240ms | 14624ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 10921ms | 14592ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 11008ms | 14601ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 11184ms | 14618ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 10896ms | 14590ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 11591ms | 14659ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 11449ms | 14645ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 10921ms | 14592ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 10903ms | 14590ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 10735ms | 14574ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 10971ms | 14597ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 11375ms | 14638ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 11138ms | 14614ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 11190ms | 14619ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 11638ms | 14664ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 10833ms | 14583ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 11161ms | 14616ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 11375ms | 14638ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 11346ms | 14635ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 10882ms | 14588ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 11133ms | 14613ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 10921ms | 14592ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | end-users | ok | 10804ms | 14580ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 11053ms | 14605ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | end-users | ok | 11168ms | 14617ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 10588ms | 14559ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | end-users | ok | 11308ms | 14631ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 181.0 | app2 | ok | 10469ms | 14547ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 181.0 | end-users | ok | 10963ms | 14596ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 11591ms | 14659ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 10855ms | 14585ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 10735ms | 14574ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 11201ms | 14620ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 11429ms | 14643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 11486ms | 14649ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 12143ms | 14714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 12222ms | 14722ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 12200ms | 14900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 12391ms | 15325ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 11591ms | 14659ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 11650ms | 14665ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 11591ms | 14659ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 11403ms | 14640ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 257.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 257.0 | end-users | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
