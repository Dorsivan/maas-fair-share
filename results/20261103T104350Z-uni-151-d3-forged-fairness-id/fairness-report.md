# Fairness benchmark: full-contention (uni-151-d3-forged-fairness-id)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-4w2hw` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-03T10:45:03Z` |
| Run end | `2026-11-03T10:49:25Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 568 | 200=558, 500=10 | 12.4 | 23.0 | 746448.0 | 21.1% | 17.9% | -3.1 | 17.9% | -3.2 | 3.7s | 98.9% | 558.0 |
| app2 | 10.0 | 32 | 452 | 200=442, 500=10 | 23.0 | 27.7 | 579162.0 | 10.5% | 13.9% | 3.4 | 14.2% | 3.7 | 2.9s | 98.9% | 441.0 |
| end-users | 65.0 | 128 | 2162 | 200=2128, 500=34 | 15.2 | 19.5 | 2835058.0 | 68.4% | 68.1% | -0.3 | 67.9% | -0.5 | 3.3s | 98.9% | 2126.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 4074.0 | n/a | n/a | n/a | n/a | n/a | 0.0s | 98.9% | 3.0 |

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
| 0.0 | 10.0 | app1 | True | 14888.0 | 21.1% | 15.3% | -5.7 |
| 0.0 | 10.0 | app2 | True | 12144.0 | 10.5% | 12.5% | 2.0 |
| 0.0 | 10.0 | end-users | True | 70120.0 | 68.4% | 72.2% | 3.8 |
| 10.0 | 20.0 | app1 | True | 39298.0 | 21.1% | 23.4% | 2.3 |
| 10.0 | 20.0 | app2 | True | 24414.0 | 10.5% | 14.5% | 4.0 |
| 10.0 | 20.0 | end-users | True | 104264.0 | 68.4% | 62.1% | -6.4 |
| 20.0 | 30.0 | app1 | True | 37866.0 | 21.1% | 21.7% | 0.6 |
| 20.0 | 30.0 | app2 | True | 18898.0 | 10.5% | 10.8% | 0.3 |
| 20.0 | 30.0 | end-users | True | 117740.0 | 68.4% | 67.5% | -0.9 |
| 30.0 | 40.0 | app1 | True | 22974.0 | 21.1% | 14.0% | -7.0 |
| 30.0 | 40.0 | app2 | True | 37886.0 | 10.5% | 23.1% | 12.6 |
| 30.0 | 40.0 | end-users | True | 102890.0 | 68.4% | 62.8% | -5.6 |
| 40.0 | 50.0 | app1 | True | 32518.0 | 21.1% | 21.3% | 0.2 |
| 40.0 | 50.0 | app2 | True | 14924.0 | 10.5% | 9.8% | -0.8 |
| 40.0 | 50.0 | end-users | True | 105498.0 | 68.4% | 69.0% | 0.6 |
| 50.0 | 60.0 | app1 | True | 10816.0 | 21.1% | 6.4% | -14.6 |
| 50.0 | 60.0 | app2 | True | 4058.0 | 10.5% | 2.4% | -8.1 |
| 50.0 | 60.0 | end-users | True | 152886.0 | 68.4% | 91.1% | 22.7 |
| 60.0 | 70.0 | app1 | True | 46026.0 | 21.1% | 27.2% | 6.1 |
| 60.0 | 70.0 | app2 | True | 56844.0 | 10.5% | 33.6% | 23.1 |
| 60.0 | 70.0 | end-users | True | 66328.0 | 68.4% | 39.2% | -29.2 |
| 70.0 | 80.0 | app1 | True | 28486.0 | 21.1% | 17.7% | -3.4 |
| 70.0 | 80.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 70.0 | 80.0 | end-users | True | 132474.0 | 68.4% | 82.3% | 13.9 |
| 80.0 | 90.0 | app1 | True | 5426.0 | 21.1% | 3.4% | -17.7 |
| 80.0 | 90.0 | app2 | True | 4044.0 | 10.5% | 2.5% | -8.0 |
| 80.0 | 90.0 | end-users | True | 151402.0 | 68.4% | 94.1% | 25.7 |
| 90.0 | 100.0 | app1 | True | 56906.0 | 21.1% | 33.4% | 12.3 |
| 90.0 | 100.0 | app2 | True | 55472.0 | 10.5% | 32.5% | 22.0 |
| 90.0 | 100.0 | end-users | True | 58156.0 | 68.4% | 34.1% | -34.3 |
| 100.0 | 110.0 | app1 | True | 14868.0 | 21.1% | 9.1% | -12.0 |
| 100.0 | 110.0 | app2 | True | 1352.0 | 10.5% | 0.8% | -9.7 |
| 100.0 | 110.0 | end-users | True | 147454.0 | 68.4% | 90.1% | 21.7 |
| 110.0 | 120.0 | app1 | True | 31064.0 | 21.1% | 19.8% | -1.3 |
| 110.0 | 120.0 | app2 | True | 16240.0 | 10.5% | 10.4% | -0.2 |
| 110.0 | 120.0 | end-users | True | 109596.0 | 68.4% | 69.9% | 1.4 |
| 120.0 | 130.0 | app1 | True | 40536.0 | 21.1% | 24.0% | 3.0 |
| 120.0 | 130.0 | app2 | True | 43264.0 | 10.5% | 25.6% | 15.1 |
| 120.0 | 130.0 | end-users | True | 85080.0 | 68.4% | 50.4% | -18.0 |
| 130.0 | 140.0 | app1 | True | 6730.0 | 21.1% | 4.0% | -17.0 |
| 130.0 | 140.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 130.0 | 140.0 | end-users | True | 161082.0 | 68.4% | 96.0% | 27.6 |
| 140.0 | 150.0 | app1 | True | 44558.0 | 21.1% | 25.7% | 4.7 |
| 140.0 | 150.0 | app2 | True | 58218.0 | 10.5% | 33.6% | 23.1 |
| 140.0 | 150.0 | end-users | True | 70336.0 | 68.4% | 40.6% | -27.8 |
| 150.0 | 160.0 | app1 | True | 35098.0 | 21.1% | 22.6% | 1.5 |
| 150.0 | 160.0 | app2 | True | 1358.0 | 10.5% | 0.9% | -9.7 |
| 150.0 | 160.0 | end-users | True | 118948.0 | 68.4% | 76.5% | 8.1 |
| 160.0 | 170.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 160.0 | 170.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 160.0 | 170.0 | end-users | True | 163876.0 | 68.4% | 100.0% | 31.6 |
| 170.0 | 180.0 | app1 | True | 52738.0 | 21.1% | 31.2% | 10.1 |
| 170.0 | 180.0 | app2 | True | 60982.0 | 10.5% | 36.1% | 25.5 |
| 170.0 | 180.0 | end-users | True | 55428.0 | 68.4% | 32.8% | -35.7 |
| 180.0 | 190.0 | app1 | True | 29754.0 | 21.1% | 20.0% | -1.0 |
| 180.0 | 190.0 | app2 | True | 1358.0 | 10.5% | 0.9% | -9.6 |
| 180.0 | 190.0 | end-users | True | 117620.0 | 68.4% | 79.1% | 10.7 |
| 190.0 | 200.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 190.0 | 200.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 190.0 | 200.0 | end-users | True | 167908.0 | 68.4% | 100.0% | 31.6 |
| 200.0 | 210.0 | app1 | True | 58166.0 | 21.1% | 34.4% | 13.4 |
| 200.0 | 210.0 | app2 | True | 62206.0 | 10.5% | 36.8% | 26.3 |
| 200.0 | 210.0 | end-users | True | 48658.0 | 68.4% | 28.8% | -39.6 |
| 210.0 | 220.0 | app1 | True | 22998.0 | 21.1% | 13.4% | -7.7 |
| 210.0 | 220.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 210.0 | 220.0 | end-users | True | 148826.0 | 68.4% | 86.6% | 18.2 |
| 220.0 | 230.0 | app1 | True | 22986.0 | 21.1% | 15.0% | -6.0 |
| 220.0 | 230.0 | app2 | True | 12176.0 | 10.5% | 8.0% | -2.6 |
| 220.0 | 230.0 | end-users | True | 117608.0 | 68.4% | 77.0% | 8.6 |
| 230.0 | 240.0 | app1 | True | 44518.0 | 21.1% | 26.0% | 4.9 |
| 230.0 | 240.0 | app2 | True | 50010.0 | 10.5% | 29.2% | 18.6 |
| 230.0 | 240.0 | end-users | True | 76920.0 | 68.4% | 44.9% | -23.6 |
| 240.0 | 251.0 | app1 | False | 13428.0 | n/a | n/a | n/a |
| 240.0 | 251.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 251.0 | end-users | False | 156938.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 33802.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 43314.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 27022.0 | n/a | n/a | n/a |
| 261.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 686340 | 34098 | 720438.0 | 0.0% | 746448.0 | 754536.0 | -1.1% | True |
| app2 | 543660 | 27216 | 569582.0 | -0.2% | 579162.0 | 598092.0 | -3.2% | True |
| end-users | 2617440 | 130448 | 2745300.0 | -0.1% | 2835058.0 | 2878336.0 | -1.5% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 568 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 452 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2162 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide):** not recorded -- `llm_d_epp_flow_control_requests_total` is absent from both snapshots, so whether the EPP or something in front of it (Kuadrant) produced the client's 429s is unknown.

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
