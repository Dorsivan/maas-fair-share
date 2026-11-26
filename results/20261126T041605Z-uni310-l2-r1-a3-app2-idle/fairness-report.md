# Fairness benchmark: app2-idle (uni310-l2-r1-a3-app2-idle)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 0.0 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 0.0 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

## Run metadata

| field | value |
|---|---|
| Scenario | `app2-idle` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-8448f688f-2qdhv` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T04:17:14Z` |
| Run end | `2026-11-26T04:21:32Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 27 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/27 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 57.00 | 1.7812 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1289 | 200=1289 | 6.0 | 7.2 | 1678510.0 | 23.5% | 23.5% | 0.0 | 23.5% | -0.1 | 23.5% | -0.0 | 29.1s | 98.9% | 1289.0 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| end-users | 65.0 | 104 | 4191 | 200=4191 | 6.0 | 7.2 | 5474448.0 | 76.5% | 76.5% | 0.0 | 76.5% | 0.1 | 76.5% | 0.0 | 29.1s | 98.9% | 4191.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 0.0 | 0.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 4074.0 | 23.5% | 23.2% | -0.3 |
| 0.0 | 10.0 | end-users | True | False | 13476.0 | 76.5% | 76.8% | 0.3 |
| 10.0 | 21.0 | app1 | True | False | 62204.0 | 23.5% | 22.5% | -1.0 |
| 10.0 | 21.0 | end-users | True | False | 213860.0 | 76.5% | 77.5% | 1.0 |
| 21.0 | 31.0 | app1 | True | False | 73142.0 | 23.5% | 24.1% | 0.6 |
| 21.0 | 31.0 | end-users | True | False | 230024.0 | 76.5% | 75.9% | -0.6 |
| 31.0 | 41.0 | app1 | True | False | 69048.0 | 23.5% | 23.1% | -0.4 |
| 31.0 | 41.0 | end-users | True | False | 229760.0 | 76.5% | 76.9% | 0.4 |
| 41.0 | 51.0 | app1 | True | False | 69004.0 | 23.5% | 22.9% | -0.7 |
| 41.0 | 51.0 | end-users | True | False | 232644.0 | 76.5% | 77.1% | 0.7 |
| 51.0 | 61.0 | app1 | True | False | 71688.0 | 23.5% | 23.5% | 0.0 |
| 51.0 | 61.0 | end-users | True | False | 232790.0 | 76.5% | 76.5% | -0.0 |
| 61.0 | 71.0 | app1 | True | False | 70374.0 | 23.5% | 23.2% | -0.3 |
| 61.0 | 71.0 | end-users | True | False | 232640.0 | 76.5% | 76.8% | 0.3 |
| 71.0 | 81.0 | app1 | True | False | 74430.0 | 23.5% | 24.6% | 1.0 |
| 71.0 | 81.0 | end-users | True | False | 228412.0 | 76.5% | 75.4% | -1.0 |
| 81.0 | 91.0 | app1 | True | False | 70266.0 | 23.5% | 23.2% | -0.3 |
| 81.0 | 91.0 | end-users | True | False | 232518.0 | 76.5% | 76.8% | 0.3 |
| 91.0 | 101.0 | app1 | True | False | 71616.0 | 23.5% | 23.8% | 0.2 |
| 91.0 | 101.0 | end-users | True | False | 229718.0 | 76.5% | 76.2% | -0.2 |
| 101.0 | 111.0 | app1 | True | False | 70170.0 | 23.5% | 23.5% | -0.1 |
| 101.0 | 111.0 | end-users | True | False | 228798.0 | 76.5% | 76.5% | 0.1 |
| 111.0 | 121.0 | app1 | True | False | 68996.0 | 23.5% | 23.0% | -0.6 |
| 111.0 | 121.0 | end-users | True | False | 231354.0 | 76.5% | 77.0% | 0.6 |
| 121.0 | 131.0 | app1 | True | False | 73008.0 | 23.5% | 24.2% | 0.7 |
| 121.0 | 131.0 | end-users | True | False | 228386.0 | 76.5% | 75.8% | -0.7 |
| 131.0 | 141.0 | app1 | True | False | 68968.0 | 23.5% | 22.6% | -1.0 |
| 131.0 | 141.0 | end-users | True | False | 236486.0 | 76.5% | 77.4% | 1.0 |
| 141.0 | 151.0 | app1 | True | False | 70360.0 | 23.5% | 23.6% | 0.1 |
| 141.0 | 151.0 | end-users | True | False | 227352.0 | 76.5% | 76.4% | -0.1 |
| 151.0 | 161.0 | app1 | True | False | 70352.0 | 23.5% | 23.4% | -0.1 |
| 151.0 | 161.0 | end-users | True | False | 229860.0 | 76.5% | 76.6% | 0.1 |
| 161.0 | 171.0 | app1 | True | False | 71674.0 | 23.5% | 23.7% | 0.1 |
| 161.0 | 171.0 | end-users | True | False | 231228.0 | 76.5% | 76.3% | -0.1 |
| 171.0 | 181.0 | app1 | True | False | 71602.0 | 23.5% | 23.8% | 0.3 |
| 171.0 | 181.0 | end-users | True | False | 228634.0 | 76.5% | 76.2% | -0.3 |
| 181.0 | 191.0 | app1 | True | False | 73022.0 | 23.5% | 24.2% | 0.7 |
| 181.0 | 191.0 | end-users | True | False | 228626.0 | 76.5% | 75.8% | -0.7 |
| 191.0 | 201.0 | app1 | True | False | 69086.0 | 23.5% | 22.8% | -0.7 |
| 191.0 | 201.0 | end-users | True | False | 233966.0 | 76.5% | 77.2% | 0.7 |
| 201.0 | 211.0 | app1 | True | False | 73034.0 | 23.5% | 23.8% | 0.3 |
| 201.0 | 211.0 | end-users | True | False | 233950.0 | 76.5% | 76.2% | -0.3 |
| 211.0 | 221.0 | app1 | True | False | 71734.0 | 23.5% | 23.8% | 0.2 |
| 211.0 | 221.0 | end-users | True | False | 229956.0 | 76.5% | 76.2% | -0.2 |
| 221.0 | 231.0 | app1 | True | False | 70352.0 | 23.5% | 23.0% | -0.5 |
| 221.0 | 231.0 | end-users | True | False | 235228.0 | 76.5% | 77.0% | 0.5 |
| 231.0 | 241.0 | app1 | True | False | 71562.0 | 23.5% | 23.7% | 0.2 |
| 231.0 | 241.0 | end-users | True | False | 229912.0 | 76.5% | 76.3% | -0.2 |
| 241.0 | 251.0 | app1 | False | n/a | 48744.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 164870.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 60 | 0ms | 2059ms | 3500ms |
| 0.0 | 10.0 | end-users | ok | 195 | 0ms | 1941ms | 2563ms |
| 10.0 | 21.0 | app1 | ok | 47 | 1325ms | 2265ms | 2476ms |
| 10.0 | 21.0 | end-users | ok | 152 | 1306ms | 2287ms | 3100ms |
| 21.0 | 31.0 | app1 | ok | 54 | 1200ms | 2280ms | 3650ms |
| 21.0 | 31.0 | end-users | ok | 174 | 1235ms | 2259ms | 2489ms |
| 31.0 | 41.0 | app1 | ok | 53 | 1295ms | 2259ms | 2476ms |
| 31.0 | 41.0 | end-users | ok | 174 | 1230ms | 2295ms | 3912ms |
| 41.0 | 51.0 | app1 | ok | 54 | 1318ms | 2300ms | 3650ms |
| 41.0 | 51.0 | end-users | ok | 174 | 1238ms | 2271ms | 2825ms |
| 51.0 | 61.0 | app1 | ok | 51 | 1305ms | 2261ms | 2476ms |
| 51.0 | 61.0 | end-users | ok | 168 | 1309ms | 2297ms | 3600ms |
| 61.0 | 71.0 | app1 | ok | 52 | 1281ms | 2256ms | 2476ms |
| 61.0 | 71.0 | end-users | ok | 170 | 1274ms | 2255ms | 2475ms |
| 71.0 | 81.0 | app1 | ok | 55 | 1169ms | 2234ms | 2473ms |
| 71.0 | 81.0 | end-users | ok | 176 | 1218ms | 2244ms | 2474ms |
| 81.0 | 91.0 | app1 | ok | 54 | 1242ms | 2287ms | 3650ms |
| 81.0 | 91.0 | end-users | ok | 174 | 1230ms | 2295ms | 3912ms |
| 91.0 | 101.0 | app1 | ok | 53 | 1258ms | 2252ms | 2475ms |
| 91.0 | 101.0 | end-users | ok | 177 | 1226ms | 2257ms | 2489ms |
| 101.0 | 111.0 | app1 | ok | 54 | 1200ms | 2280ms | 3650ms |
| 101.0 | 111.0 | end-users | ok | 172 | 1255ms | 2287ms | 3567ms |
| 111.0 | 121.0 | app1 | ok | 54 | 1234ms | 2247ms | 2475ms |
| 111.0 | 121.0 | end-users | ok | 174 | 1260ms | 2263ms | 2489ms |
| 121.0 | 131.0 | app1 | ok | 53 | 1295ms | 2259ms | 2476ms |
| 121.0 | 131.0 | end-users | ok | 178 | 1280ms | 2279ms | 2775ms |
| 131.0 | 141.0 | app1 | ok | 51 | 1363ms | 2350ms | 4363ms |
| 131.0 | 141.0 | end-users | ok | 163 | 1290ms | 2258ms | 2476ms |
| 141.0 | 151.0 | app1 | ok | 53 | 1175ms | 2235ms | 2474ms |
| 141.0 | 151.0 | end-users | ok | 172 | 1265ms | 2276ms | 2850ms |
| 151.0 | 161.0 | app1 | ok | 54 | 1150ms | 2230ms | 2473ms |
| 151.0 | 161.0 | end-users | ok | 177 | 1292ms | 2355ms | 4447ms |
| 161.0 | 171.0 | app1 | ok | 54 | 1234ms | 2247ms | 2475ms |
| 161.0 | 171.0 | end-users | ok | 174 | 1223ms | 2256ms | 2489ms |
| 171.0 | 181.0 | app1 | ok | 53 | 1218ms | 2244ms | 2474ms |
| 171.0 | 181.0 | end-users | ok | 167 | 1209ms | 2242ms | 2474ms |
| 181.0 | 191.0 | app1 | ok | 52 | 1290ms | 2297ms | 3700ms |
| 181.0 | 191.0 | end-users | ok | 171 | 1321ms | 2299ms | 3575ms |
| 191.0 | 201.0 | app1 | ok | 52 | 1200ms | 2240ms | 2474ms |
| 191.0 | 201.0 | end-users | ok | 169 | 1260ms | 2264ms | 2490ms |
| 201.0 | 211.0 | app1 | ok | 53 | 1352ms | 2345ms | 4337ms |
| 201.0 | 211.0 | end-users | ok | 174 | 1277ms | 2290ms | 3550ms |
| 211.0 | 221.0 | app1 | ok | 52 | 1242ms | 2248ms | 2475ms |
| 211.0 | 221.0 | end-users | ok | 173 | 1245ms | 2273ms | 2838ms |
| 221.0 | 231.0 | app1 | ok | 52 | 1353ms | 2271ms | 2477ms |
| 221.0 | 231.0 | end-users | ok | 166 | 1306ms | 2273ms | 2490ms |
| 231.0 | 241.0 | app1 | ok | 52 | 1207ms | 2283ms | 3700ms |
| 231.0 | 241.0 | end-users | ok | 170 | 1324ms | 2324ms | 4150ms |
| 241.0 | 251.0 | app1 | ok | 17 | 1477ms | 2405ms | 4575ms |
| 241.0 | 251.0 | end-users | ok | 57 | 1414ms | 2314ms | 3575ms |
| 251.0 | 258.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1585470 | 79027 | 1664497.0 | 0.0% | 1678510.0 | 1743524.0 | -3.7% | True |
| end-users | 5154930 | 256447 | 5411377.0 | 0.0% | 5474448.0 | 5667824.0 | -3.4% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1289 | 0 | 0 | 0 (never shed) | 0.00% | 23.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 4191 | 0 | 0 | 0 (never shed) | 0.00% | 76.5% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5480). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5480 | 0.051ms | 0.108ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 245018 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1289 | 5934ms | 7795ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 4191 | 5943ms | 7793ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5480 | 5941ms | 7793ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2875ms | 5225ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2964ms | 5394ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 21.0 | app1 | ok | 5909ms | 7783ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 21.0 | end-users | ok | 5864ms | 7776ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 21.0 | 31.0 | app1 | ok | 5917ms | 7784ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 21.0 | 31.0 | end-users | ok | 5934ms | 7788ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 31.0 | 41.0 | app1 | ok | 5972ms | 7796ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 31.0 | 41.0 | end-users | ok | 5926ms | 7788ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | app1 | ok | 5929ms | 7788ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | end-users | ok | 5957ms | 7793ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app1 | ok | 6037ms | 7804ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | end-users | ok | 5905ms | 7781ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app1 | ok | 5891ms | 7779ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | end-users | ok | 5967ms | 7794ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app1 | ok | 5976ms | 7796ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | end-users | ok | 5970ms | 7795ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 5921ms | 7788ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 5892ms | 7780ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 6107ms | 7811ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 5959ms | 7794ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 5820ms | 7759ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 5950ms | 7791ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 6074ms | 7807ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 6011ms | 7801ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 6000ms | 7800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 5971ms | 7795ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 5880ms | 7774ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 5965ms | 7794ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 6143ms | 7814ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 5986ms | 7798ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 5975ms | 7796ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 6067ms | 7807ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 5905ms | 7784ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 5992ms | 7799ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 5976ms | 7796ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 5971ms | 7795ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 6138ms | 7814ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 5970ms | 7795ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 5929ms | 7865ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 6023ms | 7802ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 5952ms | 7792ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 6011ms | 7801ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 5952ms | 7792ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 6023ms | 7802ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 5870ms | 7774ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 6011ms | 7801ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 5895ms | 7784ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 6000ms | 7800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 6478ms | 7926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 6265ms | 7879ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
