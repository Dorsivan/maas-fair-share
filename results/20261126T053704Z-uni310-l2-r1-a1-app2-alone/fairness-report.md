# Fairness benchmark: app2-alone (uni310-l2-r1-a1-app2-alone)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app2-alone` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-8448f688f-pssbr` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T05:38:22Z` |
| Run end | `2026-11-26T05:42:29Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 26 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/26 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 8.00 | 0.2500 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| app2 | 10.0 | 32 | 5391 | 200=5391 | 1.4 | 1.6 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 5391.0 |
| end-users | 65.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app2: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 0.0 (uncontended -- no group delivered contended tokens from here on, nothing was being arbitrated) | 0.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (25 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 10.0 | 20.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 20.0 | 30.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 30.0 | 40.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 40.0 | 50.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 50.0 | 60.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 60.0 | 70.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 70.0 | 80.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 80.0 | 90.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 90.0 | 100.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 100.0 | 110.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 110.0 | 120.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 120.0 | 130.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 130.0 | 140.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 140.0 | 150.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 150.0 | 160.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 160.0 | 170.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 170.0 | 180.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 180.0 | 190.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 190.0 | 200.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 200.0 | 210.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 210.0 | 220.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 220.0 | 230.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 230.0 | 241.0 | app2 | True | True | 0.0 | 100.0% | n/a | n/a |
| 241.0 | 247.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app2 | ok | 172 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app2 | ok | 226 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app2 | ok | 230 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app2 | ok | 225 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | app2 | ok | 228 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app2 | ok | 227 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app2 | ok | 227 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app2 | ok | 227 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app2 | ok | 225 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | app2 | ok | 228 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | app2 | ok | 222 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | app2 | ok | 225 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | app2 | ok | 222 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | app2 | ok | 228 | 0ms | 0ms | 0ms |
| 140.0 | 150.0 | app2 | ok | 226 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | app2 | ok | 226 | 0ms | 0ms | 0ms |
| 160.0 | 170.0 | app2 | ok | 225 | 0ms | 0ms | 0ms |
| 170.0 | 180.0 | app2 | ok | 225 | 0ms | 0ms | 0ms |
| 180.0 | 190.0 | app2 | ok | 225 | 0ms | 0ms | 0ms |
| 190.0 | 200.0 | app2 | ok | 227 | 0ms | 0ms | 0ms |
| 200.0 | 210.0 | app2 | ok | 227 | 0ms | 0ms | 0ms |
| 210.0 | 220.0 | app2 | ok | 226 | 0ms | 0ms | 0ms |
| 220.0 | 230.0 | app2 | ok | 223 | 0ms | 0ms | 0ms |
| 230.0 | 241.0 | app2 | ok | 225 | 0ms | 0ms | 0ms |
| 241.0 | 247.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost n/a

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app2 | 6630930 | 330088 | 6961018.0 | 0.0% | n/a | 7291106.0 | n/a | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app2 | 5391 | 0 | 0 | 0 (never shed) | 0.00% | 100.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5391). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5391 | 0.051ms | 0.147ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 235792 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app2 | ok | 5391 | 1358ms | 1639ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5391 | 1358ms | 1639ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (25 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app2 | ok | 1344ms | 2493ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 1358ms | 1527ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 1357ms | 1499ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 1357ms | 1647ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 1360ms | 1622ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 1353ms | 1500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 1351ms | 1665ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 1351ms | 1645ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 1366ms | 1669ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 1359ms | 1562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 1359ms | 1498ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 1364ms | 1758ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 1368ms | 1652ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 1354ms | 1500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 1344ms | 1668ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 1355ms | 1685ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 1364ms | 1567ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 1367ms | 1625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app2 | ok | 1359ms | 1625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app2 | ok | 1355ms | 1498ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app2 | ok | 1361ms | 1531ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 220.0 | app2 | ok | 1358ms | 1642ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 220.0 | 230.0 | app2 | ok | 1368ms | 1708ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 230.0 | 241.0 | app2 | ok | 1356ms | 1700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 247.0 | app2 | ok | 1354ms | 1745ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
