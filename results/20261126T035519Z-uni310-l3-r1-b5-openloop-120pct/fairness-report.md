# Fairness benchmark: uni310-l3-r1-b5-openloop-120pct (uni310-l3-r1-b5-openloop-120pct)

**Verdict: FAIL** (threshold: 10 points)
**Secondary (priority) verdict: PRIORITY-FAIL** -- see "Per-tenant TTFT / ITL and the priority verdict (UNI-226)" below for detail.
Worker-share vs. weight-share gap (UNI-225): 35.1 points

- end-users deviated -32.8 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `uni310-l3-r1-b5-openloop-120pct` |
| Generator | `open-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5d57688bf8-7zczh` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T03:55:19Z` |
| Run end | `2026-11-26T03:59:27Z` |

## Saturation limb (UNI-224)

Not evaluated: no `--metrics-timeseries` was captured for this run (pre-UNI-224 shape).

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered req/s | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 8.4 | 2019 | 0=458, 200=1560, 503=1 | 4.9 | 37.0 | 1530966.0 | 21.1% | 33.3% | 12.3 | 32.0% | 11.0 | 33.6% | 12.5 | 11.3s | 98.9% | 1561.0 |
| app2 | 10.0 | 8.4 | 2010 | 0=464, 200=1542, 503=4 | 17.3 | 50.0 | 1544614.0 | 10.5% | 33.3% | 22.8 | 32.3% | 21.8 | 33.4% | 22.9 | 11.3s | 98.9% | 1546.0 |
| end-users | 65.0 | 8.4 | 1984 | 0=293, 200=1691 | 3.1 | 36.6 | 1702996.0 | 68.4% | 33.3% | -35.1 | 35.6% | -32.8 | 33.0% | -35.4 | 10.3s | 98.9% | 1817.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

N/A: no `--metrics-timeseries` recorded for this run (older report, or the benchmark script predates UNI-127).

## Ledger cross-check (UNI-138/G2)

N/A: no `--client-record-jsonl` recorded for this run (older report, or the benchmark script predates UNI-138).

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2019 | 0 | 1 | 1 | 0.05% | 21.1% | 20.0% | 0.95 |
| app2 | 2010 | 0 | 4 | 4 | 0.20% | 10.5% | 80.0% | 7.60 |
| end-users | 1984 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | 0.0% | 0.00 |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=4924, EvictedContextCancelled=869). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 235341 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1560 | 4083ms | 27057ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1542 | 13227ms | 54972ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 1691 | 2901ms | 35743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 4793 | 5206ms | 44437ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: PRIORITY-FAIL** -- the share verdict above is FAIL, so this is the board's second, independent success criterion (2026-11-10): did the policy nonetheless order tenants by weight? Top-weighted group: `end-users` (TTFT p50 2901ms, p95 35743ms, strictly lowest among distinctly-weighted groups: p50=True/p95=False; no rank inversion among any distinctly-weighted pair: True -- this, not raw rank correlation, is what gates the verdict, since a genuine weight tie (e.g. 98/1/1's app2==end-users) makes exact correlation 1.0 unreachable by construction even when ordering is otherwise perfect). Rank correlation 1.00 (1.00 = exact agreement, informational only) shown for reference. Separation from the next distinctly-weighted group: 1182ms against a noise floor of not given (separation check skipped).

N/A: no `--metrics-timeseries` recorded for this run, whole-run numbers above only.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/13-loadgen-poisson.py's own stdout (UNI-137/B5): the 'load: open-loop Poisson arrivals rate ...' line for each offered group's Poisson arrival rate in req/s -- NOT a worker count, this generator is open-loop -- and each group's own 'sent=... completion_tokens=... p50=...s p95=...s p99=...s codes=[...]' summary line for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
