# Fairness benchmark: full-contention (uni-160-f3-33-33-33)

**Verdict: FAIL** (threshold: 10 points)

- end-users deviated +34.3 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-659bd5cc7d-cvjvv` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-06T16:48:47Z` |
| Run end | `2026-11-06T16:53:09Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 33.0 | 32 | 530 | 200=509, 500=21 | 14.1 | 25.1 | 665264.0 | 33.3% | 16.1% | -17.2 | 16.2% | -17.1 | 9.1s | 98.9% | 508.0 |
| app2 | 33.0 | 32 | 529 | 200=511, 500=18 | 14.8 | 25.2 | 669582.0 | 33.3% | 16.2% | -17.1 | 16.2% | -17.2 | 9.2s | 98.9% | 510.0 |
| end-users | 33.0 | 128 | 2211 | 200=2143, 500=68 | 15.5 | 19.4 | 2791030.0 | 33.3% | 67.6% | 34.3 | 67.6% | 34.3 | 9.2s | 98.9% | 2139.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 1344.0 | n/a | n/a | n/a | n/a | n/a | 0.0s | 98.9% | 6.0 |

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
| 0.0 | 10.0 | app1 | True | 6734.0 | 33.3% | 13.8% | -19.5 |
| 0.0 | 10.0 | app2 | True | 8148.0 | 33.3% | 16.7% | -16.6 |
| 0.0 | 10.0 | end-users | True | 33868.0 | 33.3% | 69.5% | 36.1 |
| 10.0 | 20.0 | app1 | True | 37782.0 | 33.3% | 21.0% | -12.3 |
| 10.0 | 20.0 | app2 | True | 41992.0 | 33.3% | 23.3% | -10.0 |
| 10.0 | 20.0 | end-users | True | 100194.0 | 33.3% | 55.7% | 22.3 |
| 20.0 | 30.0 | app1 | True | 27098.0 | 33.3% | 16.2% | -17.2 |
| 20.0 | 30.0 | app2 | True | 21660.0 | 33.3% | 12.9% | -20.4 |
| 20.0 | 30.0 | end-users | True | 119020.0 | 33.3% | 70.9% | 37.6 |
| 30.0 | 40.0 | app1 | True | 23024.0 | 33.3% | 13.3% | -20.0 |
| 30.0 | 40.0 | app2 | True | 24354.0 | 33.3% | 14.1% | -19.3 |
| 30.0 | 40.0 | end-users | True | 125710.0 | 33.3% | 72.6% | 39.3 |
| 40.0 | 50.0 | app1 | True | 43232.0 | 33.3% | 28.6% | -4.8 |
| 40.0 | 50.0 | app2 | True | 43202.0 | 33.3% | 28.5% | -4.8 |
| 40.0 | 50.0 | end-users | True | 64934.0 | 33.3% | 42.9% | 9.6 |
| 50.0 | 60.0 | app1 | True | 24280.0 | 33.3% | 14.2% | -19.2 |
| 50.0 | 60.0 | app2 | True | 24324.0 | 33.3% | 14.2% | -19.2 |
| 50.0 | 60.0 | end-users | True | 122948.0 | 33.3% | 71.7% | 38.3 |
| 60.0 | 70.0 | app1 | True | 25680.0 | 33.3% | 15.2% | -18.1 |
| 60.0 | 70.0 | app2 | True | 25708.0 | 33.3% | 15.2% | -18.1 |
| 60.0 | 70.0 | end-users | True | 117636.0 | 33.3% | 69.6% | 36.3 |
| 70.0 | 80.0 | app1 | True | 31070.0 | 33.3% | 18.7% | -14.7 |
| 70.0 | 80.0 | app2 | True | 31086.0 | 33.3% | 18.7% | -14.6 |
| 70.0 | 80.0 | end-users | True | 104188.0 | 33.3% | 62.6% | 29.3 |
| 80.0 | 90.0 | app1 | True | 35140.0 | 33.3% | 22.2% | -11.1 |
| 80.0 | 90.0 | app2 | True | 35074.0 | 33.3% | 22.2% | -11.1 |
| 80.0 | 90.0 | end-users | True | 87742.0 | 33.3% | 55.5% | 22.2 |
| 90.0 | 100.0 | app1 | True | 14824.0 | 33.3% | 9.0% | -24.3 |
| 90.0 | 100.0 | app2 | True | 13508.0 | 33.3% | 8.2% | -25.1 |
| 90.0 | 100.0 | end-users | True | 136610.0 | 33.3% | 82.8% | 49.5 |
| 100.0 | 110.0 | app1 | True | 58256.0 | 33.3% | 34.4% | 1.1 |
| 100.0 | 110.0 | app2 | True | 33836.0 | 33.3% | 20.0% | -13.3 |
| 100.0 | 110.0 | end-users | True | 77070.0 | 33.3% | 45.6% | 12.2 |
| 110.0 | 120.0 | app1 | True | 10824.0 | 33.3% | 6.3% | -27.1 |
| 110.0 | 120.0 | app2 | True | 36514.0 | 33.3% | 21.1% | -12.2 |
| 110.0 | 120.0 | end-users | True | 125754.0 | 33.3% | 72.7% | 39.3 |
| 120.0 | 130.0 | app1 | True | 10846.0 | 33.3% | 7.2% | -26.1 |
| 120.0 | 130.0 | app2 | True | 31150.0 | 33.3% | 20.7% | -12.6 |
| 120.0 | 130.0 | end-users | True | 108166.0 | 33.3% | 72.0% | 38.7 |
| 130.0 | 140.0 | app1 | True | 63612.0 | 33.3% | 37.9% | 4.6 |
| 130.0 | 140.0 | app2 | True | 1358.0 | 33.3% | 0.8% | -32.5 |
| 130.0 | 140.0 | end-users | True | 102670.0 | 33.3% | 61.2% | 27.9 |
| 140.0 | 150.0 | app1 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 140.0 | 150.0 | app2 | True | 41976.0 | 33.3% | 25.4% | -7.9 |
| 140.0 | 150.0 | end-users | True | 123102.0 | 33.3% | 74.6% | 41.2 |
| 150.0 | 160.0 | app1 | True | 17526.0 | 33.3% | 11.5% | -21.9 |
| 150.0 | 160.0 | app2 | True | 16222.0 | 33.3% | 10.6% | -22.7 |
| 150.0 | 160.0 | end-users | True | 119108.0 | 33.3% | 77.9% | 44.6 |
| 160.0 | 170.0 | app1 | True | 47392.0 | 33.3% | 27.2% | -6.1 |
| 160.0 | 170.0 | app2 | True | 49946.0 | 33.3% | 28.6% | -4.7 |
| 160.0 | 170.0 | end-users | True | 77002.0 | 33.3% | 44.2% | 10.8 |
| 170.0 | 180.0 | app1 | True | 1352.0 | 33.3% | 0.8% | -32.5 |
| 170.0 | 180.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 170.0 | 180.0 | end-users | True | 164928.0 | 33.3% | 99.2% | 65.9 |
| 180.0 | 190.0 | app1 | True | 40616.0 | 33.3% | 25.0% | -8.3 |
| 180.0 | 190.0 | app2 | True | 40602.0 | 33.3% | 25.0% | -8.3 |
| 180.0 | 190.0 | end-users | True | 81148.0 | 33.3% | 50.0% | 16.6 |
| 190.0 | 200.0 | app1 | True | 29734.0 | 33.3% | 18.6% | -14.7 |
| 190.0 | 200.0 | app2 | True | 32498.0 | 33.3% | 20.4% | -13.0 |
| 190.0 | 200.0 | end-users | True | 97308.0 | 33.3% | 61.0% | 27.7 |
| 200.0 | 211.0 | app1 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 200.0 | 211.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 200.0 | 211.0 | end-users | True | 168996.0 | 33.3% | 100.0% | 66.7 |
| 211.0 | 221.0 | app1 | True | 59518.0 | 33.3% | 34.9% | 1.6 |
| 211.0 | 221.0 | app2 | True | 62250.0 | 33.3% | 36.5% | 3.2 |
| 211.0 | 221.0 | end-users | True | 48744.0 | 33.3% | 28.6% | -4.7 |
| 221.0 | 231.0 | app1 | True | 9430.0 | 33.3% | 6.1% | -27.3 |
| 221.0 | 231.0 | app2 | True | 8148.0 | 33.3% | 5.2% | -28.1 |
| 221.0 | 231.0 | end-users | True | 137862.0 | 33.3% | 88.7% | 55.4 |
| 231.0 | 241.0 | app1 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 231.0 | 241.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 231.0 | 241.0 | end-users | True | 165078.0 | 33.3% | 100.0% | 66.7 |
| 241.0 | 251.0 | app1 | False | 47294.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 46026.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 78574.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 102670.0 | n/a | n/a | n/a |
| 261.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 626070 | 31093 | 655876.0 | -0.2% | 665264.0 | 688256.0 | -3.3% | True |
| app2 | 628530 | 31352 | 658592.0 | -0.2% | 669582.0 | 691234.0 | -3.1% | True |
| end-users | 2635890 | 131025 | 2761741.0 | -0.2% | 2791030.0 | 2897940.0 | -3.7% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 530 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 529 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2211 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=3163). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 252533 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
