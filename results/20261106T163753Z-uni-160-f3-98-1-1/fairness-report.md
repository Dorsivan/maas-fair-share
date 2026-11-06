# Fairness benchmark: full-contention (uni-160-f3-98-1-1)

**Verdict: FAIL** (threshold: 10 points)

- app1 deviated -78.9 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-76d64c7b87-mjr67` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-06T16:39:04Z` |
| Run end | `2026-11-06T16:43:27Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 98.0 | 32 | 607 | 200=591, 500=16 | 13.9 | 22.4 | 788410.0 | 98.0% | 19.1% | -78.9 | 18.8% | -79.2 | 3.8s | 98.9% | 590.0 |
| app2 | 1.0 | 32 | 489 | 200=473, 500=16 | 14.5 | 27.3 | 621724.0 | 1.0% | 15.0% | 14.0 | 15.2% | 14.2 | 4.2s | 98.9% | 470.0 |
| end-users | 1.0 | 128 | 2126 | 200=2066, 500=60 | 15.6 | 19.7 | 2727980.0 | 1.0% | 65.9% | 64.9 | 66.0% | 65.0 | 4.3s | 98.9% | 2049.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 28432.0 | n/a | n/a | n/a | n/a | n/a | 0.0s | 98.9% | 21.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 10800.0 | 98.0% | 18.6% | -79.4 |
| 0.0 | 10.0 | app2 | True | 8116.0 | 1.0% | 14.0% | 13.0 |
| 0.0 | 10.0 | end-users | True | 39176.0 | 1.0% | 67.4% | 66.4 |
| 10.0 | 20.0 | app1 | True | 47340.0 | 98.0% | 27.6% | -70.4 |
| 10.0 | 20.0 | app2 | True | 43270.0 | 1.0% | 25.2% | 24.2 |
| 10.0 | 20.0 | end-users | True | 81016.0 | 1.0% | 47.2% | 46.2 |
| 20.0 | 30.0 | app1 | True | 45966.0 | 98.0% | 26.6% | -71.4 |
| 20.0 | 30.0 | app2 | True | 18904.0 | 1.0% | 10.9% | 9.9 |
| 20.0 | 30.0 | end-users | True | 107994.0 | 1.0% | 62.5% | 61.5 |
| 30.0 | 40.0 | app1 | True | 0.0 | 98.0% | 0.0% | -98.0 |
| 30.0 | 40.0 | app2 | True | 24368.0 | 1.0% | 14.3% | 13.3 |
| 30.0 | 40.0 | end-users | True | 146114.0 | 1.0% | 85.7% | 84.7 |
| 40.0 | 50.0 | app1 | True | 43304.0 | 98.0% | 28.1% | -69.9 |
| 40.0 | 50.0 | app2 | True | 43190.0 | 1.0% | 28.0% | 27.0 |
| 40.0 | 50.0 | end-users | True | 67544.0 | 1.0% | 43.8% | 42.8 |
| 50.0 | 60.0 | app1 | True | 43196.0 | 98.0% | 25.4% | -72.6 |
| 50.0 | 60.0 | app2 | True | 20252.0 | 1.0% | 11.9% | 10.9 |
| 50.0 | 60.0 | end-users | True | 106776.0 | 1.0% | 62.7% | 61.7 |
| 60.0 | 70.0 | app1 | True | 12122.0 | 98.0% | 7.1% | -90.9 |
| 60.0 | 70.0 | app2 | True | 24366.0 | 1.0% | 14.2% | 13.2 |
| 60.0 | 70.0 | end-users | True | 135102.0 | 1.0% | 78.7% | 77.7 |
| 70.0 | 80.0 | app1 | True | 31072.0 | 98.0% | 18.1% | -79.9 |
| 70.0 | 80.0 | app2 | True | 41784.0 | 1.0% | 24.4% | 23.4 |
| 70.0 | 80.0 | end-users | True | 98690.0 | 1.0% | 57.5% | 56.5 |
| 80.0 | 90.0 | app1 | True | 43312.0 | 98.0% | 28.6% | -69.4 |
| 80.0 | 90.0 | app2 | True | 31062.0 | 1.0% | 20.5% | 19.5 |
| 80.0 | 90.0 | end-users | True | 77056.0 | 1.0% | 50.9% | 49.9 |
| 90.0 | 100.0 | app1 | True | 40634.0 | 98.0% | 23.8% | -74.2 |
| 90.0 | 100.0 | app2 | True | 9420.0 | 1.0% | 5.5% | 4.5 |
| 90.0 | 100.0 | end-users | True | 120330.0 | 1.0% | 70.6% | 69.6 |
| 100.0 | 110.0 | app1 | True | 2702.0 | 98.0% | 1.6% | -96.4 |
| 100.0 | 110.0 | app2 | True | 39210.0 | 1.0% | 23.2% | 22.2 |
| 100.0 | 110.0 | end-users | True | 127004.0 | 1.0% | 75.2% | 74.2 |
| 110.0 | 120.0 | app1 | True | 43168.0 | 98.0% | 25.1% | -72.9 |
| 110.0 | 120.0 | app2 | True | 32440.0 | 1.0% | 18.9% | 17.9 |
| 110.0 | 120.0 | end-users | True | 96052.0 | 1.0% | 56.0% | 55.0 |
| 120.0 | 130.0 | app1 | True | 43324.0 | 98.0% | 28.4% | -69.6 |
| 120.0 | 130.0 | app2 | True | 16126.0 | 1.0% | 10.6% | 9.6 |
| 120.0 | 130.0 | end-users | True | 93220.0 | 1.0% | 61.1% | 60.1 |
| 130.0 | 140.0 | app1 | True | 0.0 | 98.0% | 0.0% | -98.0 |
| 130.0 | 140.0 | app2 | True | 51430.0 | 1.0% | 30.0% | 29.0 |
| 130.0 | 140.0 | end-users | True | 120274.0 | 1.0% | 70.0% | 69.0 |
| 140.0 | 150.0 | app1 | True | 43252.0 | 98.0% | 25.8% | -72.2 |
| 140.0 | 150.0 | app2 | True | 1358.0 | 1.0% | 0.8% | -0.2 |
| 140.0 | 150.0 | end-users | True | 123026.0 | 1.0% | 73.4% | 72.4 |
| 150.0 | 160.0 | app1 | True | 43328.0 | 98.0% | 26.3% | -71.7 |
| 150.0 | 160.0 | app2 | True | 25698.0 | 1.0% | 15.6% | 14.6 |
| 150.0 | 160.0 | end-users | True | 95968.0 | 1.0% | 58.2% | 57.2 |
| 160.0 | 170.0 | app1 | True | 10784.0 | 98.0% | 6.7% | -91.3 |
| 160.0 | 170.0 | app2 | True | 33834.0 | 1.0% | 21.0% | 20.0 |
| 160.0 | 170.0 | end-users | True | 116232.0 | 1.0% | 72.3% | 71.3 |
| 170.0 | 180.0 | app1 | True | 32494.0 | 98.0% | 19.2% | -78.8 |
| 170.0 | 180.0 | app2 | True | 1344.0 | 1.0% | 0.8% | -0.2 |
| 170.0 | 180.0 | end-users | True | 135268.0 | 1.0% | 80.0% | 79.0 |
| 180.0 | 191.0 | app1 | True | 63512.0 | 98.0% | 37.6% | -60.4 |
| 180.0 | 191.0 | app2 | True | 56828.0 | 1.0% | 33.6% | 32.6 |
| 180.0 | 191.0 | end-users | True | 48672.0 | 1.0% | 28.8% | 27.8 |
| 191.0 | 201.0 | app1 | True | 22984.0 | 98.0% | 15.0% | -83.0 |
| 191.0 | 201.0 | app2 | True | 1358.0 | 1.0% | 0.9% | -0.1 |
| 191.0 | 201.0 | end-users | True | 128480.0 | 1.0% | 84.1% | 83.1 |
| 201.0 | 211.0 | app1 | True | 0.0 | 98.0% | 0.0% | -98.0 |
| 201.0 | 211.0 | app2 | True | 0.0 | 1.0% | 0.0% | -1.0 |
| 201.0 | 211.0 | end-users | True | 169022.0 | 1.0% | 100.0% | 99.0 |
| 211.0 | 221.0 | app1 | True | 86688.0 | 98.0% | 52.1% | -45.9 |
| 211.0 | 221.0 | app2 | True | 50052.0 | 1.0% | 30.1% | 29.1 |
| 211.0 | 221.0 | end-users | True | 29680.0 | 1.0% | 17.8% | 16.8 |
| 221.0 | 231.0 | app1 | True | 0.0 | 98.0% | 0.0% | -98.0 |
| 221.0 | 231.0 | app2 | True | 4044.0 | 1.0% | 2.5% | 1.5 |
| 221.0 | 231.0 | end-users | True | 159650.0 | 1.0% | 97.5% | 96.5 |
| 231.0 | 241.0 | app1 | True | 20268.0 | 98.0% | 13.1% | -84.9 |
| 231.0 | 241.0 | app2 | True | 1358.0 | 1.0% | 0.9% | -0.1 |
| 231.0 | 241.0 | end-users | True | 132586.0 | 1.0% | 86.0% | 85.0 |
| 241.0 | 251.0 | app1 | False | 58160.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 41912.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 70254.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 102794.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 726930 | 36162 | 761800.0 | -0.2% | 788410.0 | 799254.0 | -1.4% | True |
| app2 | 581790 | 28772 | 606680.0 | -0.6% | 621724.0 | 639334.0 | -2.8% | True |
| end-users | 2541180 | 125892 | 2645115.0 | -0.8% | 2727980.0 | 2792964.0 | -2.3% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 607 | 0 | 0 | 0 (never shed) | 0.00% | 98.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 489 | 0 | 0 | 0 (never shed) | 0.00% | 1.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2126 | 0 | 0 | 0 (never shed) | 0.00% | 1.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=3130). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 252472 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
