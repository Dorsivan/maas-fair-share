# Fairness benchmark: e3-queue-ttl-shedding (uni-166-g1-shedding)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `e3-queue-ttl-shedding` |
| Generator | `open-loop` |
| Enforce | `True` |
| Duration (s) | `1200` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-z7nql` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T07:59:11Z` |
| Run end | `2026-11-09T08:20:03Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered req/s | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 12.0 | 14297 | 0=8317, 200=1424, 429=1282, 500=25, 502=1817, 503=1432 | 50.0 | 50.0 | 4668856.0 | 21.1% | 23.7% | 2.6 | 33.4% | 12.4 | 88.4s | 98.9% | 3536.0 |
| app2 | 10.0 | 12.0 | 14156 | 0=8710, 200=950, 429=1238, 500=28, 502=1819, 503=1411 | 50.0 | 50.0 | 2685308.0 | 10.5% | 13.6% | 3.1 | 33.1% | 22.6 | 88.4s | 98.9% | 2053.0 |
| end-users | 65.0 | 12.0 | 14344 | 0=6012, 200=3929, 429=1267, 500=35, 502=1699, 503=1402 | 46.8 | 50.0 | 12356077.0 | 68.4% | 62.7% | -5.7 | 33.5% | -34.9 | 88.1s | 98.9% | 9182.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 1358.0 | n/a | n/a | n/a | n/a | n/a | 6.1s | 98.9% | 1.0 |

## Timeline (UNI-127)

N/A: no `--metrics-timeseries` recorded for this run (older report, or the benchmark script predates UNI-127).

## Ledger cross-check (UNI-138/G2)

N/A: no `--client-record-jsonl` recorded for this run (older report, or the benchmark script predates UNI-138).

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 14297 | 1282 | 1432 | 2714 | 18.98% | 21.1% | 33.8% | 1.61 |
| app2 | 14156 | 1238 | 1411 | 2649 | 18.71% | 10.5% | 33.0% | 3.13 |
| end-users | 14344 | 1267 | 1402 | 2669 | 18.61% | 68.4% | 33.2% | 0.49 |

**EPP-side shed (pool-wide, no per-group label exists):** 4069 requests refused by the EPP (Dispatched=14772, EvictedContextCancelled=16316, EvictedTTL=282, RejectedCapacity=3787). Client saw 3787 x 429; at most 4069 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 1226722 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/13-loadgen-poisson.py's own stdout (UNI-137/B5): the 'load: open-loop Poisson arrivals rate ...' line for each offered group's Poisson arrival rate in req/s -- NOT a worker count, this generator is open-loop -- and each group's own 'sent=... completion_tokens=... p50=...s p95=...s p99=...s codes=[...]' summary line for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
