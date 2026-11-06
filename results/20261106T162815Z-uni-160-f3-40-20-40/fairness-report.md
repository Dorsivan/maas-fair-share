# Fairness benchmark: full-contention (uni-160-f3-40-20-40)

**Verdict: FAIL** (threshold: 10 points)

- end-users deviated +26.2 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-656748bc54-5n28c` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-06T16:29:27Z` |
| Run end | `2026-11-06T16:33:49Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 40.0 | 32 | 576 | 200=568, 500=8 | 14.8 | 24.1 | 761398.0 | 40.0% | 18.4% | -21.6 | 18.2% | -21.8 | 4.1s | 98.9% | 567.0 |
| app2 | 20.0 | 32 | 488 | 200=483, 500=5 | 17.1 | 27.6 | 635386.0 | 20.0% | 15.4% | -4.6 | 15.4% | -4.6 | 4.0s | 98.9% | 483.0 |
| end-users | 40.0 | 128 | 2107 | 200=2064, 500=43 | 15.4 | 19.9 | 2738262.0 | 40.0% | 66.2% | 26.2 | 66.4% | 26.4 | 4.1s | 98.9% | 2062.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 4060.0 | n/a | n/a | n/a | n/a | n/a | 0.0s | 98.9% | 3.0 |

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
| 0.0 | 10.0 | app1 | True | 24340.0 | 40.0% | 29.0% | -11.0 |
| 0.0 | 10.0 | app2 | True | 21582.0 | 20.0% | 25.8% | 5.8 |
| 0.0 | 10.0 | end-users | True | 37870.0 | 40.0% | 45.2% | 5.2 |
| 10.0 | 20.0 | app1 | True | 44636.0 | 40.0% | 27.0% | -13.0 |
| 10.0 | 20.0 | app2 | True | 27026.0 | 20.0% | 16.4% | -3.6 |
| 10.0 | 20.0 | end-users | True | 93370.0 | 40.0% | 56.6% | 16.6 |
| 20.0 | 30.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 20.0 | 30.0 | app2 | True | 20272.0 | 20.0% | 12.0% | -8.0 |
| 20.0 | 30.0 | end-users | True | 148740.0 | 40.0% | 88.0% | 48.0 |
| 30.0 | 40.0 | app1 | True | 43300.0 | 40.0% | 27.6% | -12.4 |
| 30.0 | 40.0 | app2 | True | 39146.0 | 20.0% | 24.9% | 4.9 |
| 30.0 | 40.0 | end-users | True | 74526.0 | 40.0% | 47.5% | 7.5 |
| 40.0 | 50.0 | app1 | True | 31056.0 | 40.0% | 18.4% | -21.6 |
| 40.0 | 50.0 | app2 | True | 21628.0 | 20.0% | 12.8% | -7.2 |
| 40.0 | 50.0 | end-users | True | 116170.0 | 40.0% | 68.8% | 28.8 |
| 50.0 | 60.0 | app1 | True | 13484.0 | 40.0% | 8.0% | -32.0 |
| 50.0 | 60.0 | app2 | True | 22982.0 | 20.0% | 13.7% | -6.3 |
| 50.0 | 60.0 | end-users | True | 131136.0 | 40.0% | 78.2% | 38.2 |
| 60.0 | 70.0 | app1 | True | 41982.0 | 40.0% | 24.8% | -15.2 |
| 60.0 | 70.0 | app2 | True | 39222.0 | 20.0% | 23.2% | 3.2 |
| 60.0 | 70.0 | end-users | True | 87856.0 | 40.0% | 52.0% | 12.0 |
| 70.0 | 80.0 | app1 | True | 27076.0 | 40.0% | 17.3% | -22.7 |
| 70.0 | 80.0 | app2 | True | 31172.0 | 20.0% | 19.9% | -0.1 |
| 70.0 | 80.0 | end-users | True | 98642.0 | 40.0% | 62.9% | 22.9 |
| 80.0 | 90.0 | app1 | True | 25740.0 | 40.0% | 15.5% | -24.5 |
| 80.0 | 90.0 | app2 | True | 4062.0 | 20.0% | 2.4% | -17.6 |
| 80.0 | 90.0 | end-users | True | 136528.0 | 40.0% | 82.1% | 42.1 |
| 90.0 | 100.0 | app1 | True | 43204.0 | 40.0% | 26.0% | -14.0 |
| 90.0 | 100.0 | app2 | True | 59448.0 | 20.0% | 35.8% | 15.8 |
| 90.0 | 100.0 | end-users | True | 63596.0 | 40.0% | 38.3% | -1.7 |
| 100.0 | 110.0 | app1 | True | 29748.0 | 40.0% | 17.5% | -22.5 |
| 100.0 | 110.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 100.0 | 110.0 | end-users | True | 140540.0 | 40.0% | 82.5% | 42.5 |
| 110.0 | 120.0 | app1 | True | 13518.0 | 40.0% | 8.7% | -31.3 |
| 110.0 | 120.0 | app2 | True | 6764.0 | 20.0% | 4.4% | -15.6 |
| 110.0 | 120.0 | end-users | True | 135204.0 | 40.0% | 87.0% | 47.0 |
| 120.0 | 130.0 | app1 | True | 54124.0 | 40.0% | 31.8% | -8.2 |
| 120.0 | 130.0 | app2 | True | 50046.0 | 20.0% | 29.4% | 9.4 |
| 120.0 | 130.0 | end-users | True | 66224.0 | 40.0% | 38.9% | -1.1 |
| 130.0 | 140.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 130.0 | 140.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 130.0 | 140.0 | end-users | True | 170468.0 | 40.0% | 100.0% | 60.0 |
| 140.0 | 150.0 | app1 | True | 43290.0 | 40.0% | 27.8% | -12.2 |
| 140.0 | 150.0 | app2 | True | 27022.0 | 20.0% | 17.4% | -2.6 |
| 140.0 | 150.0 | end-users | True | 85172.0 | 40.0% | 54.8% | 14.8 |
| 150.0 | 160.0 | app1 | True | 37906.0 | 40.0% | 22.8% | -17.2 |
| 150.0 | 160.0 | app2 | True | 35230.0 | 20.0% | 21.2% | 1.2 |
| 150.0 | 160.0 | end-users | True | 93330.0 | 40.0% | 56.1% | 16.1 |
| 160.0 | 170.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 160.0 | 170.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 160.0 | 170.0 | end-users | True | 167690.0 | 40.0% | 100.0% | 60.0 |
| 170.0 | 180.0 | app1 | True | 51394.0 | 40.0% | 30.9% | -9.1 |
| 170.0 | 180.0 | app2 | True | 60768.0 | 20.0% | 36.6% | 16.6 |
| 170.0 | 180.0 | end-users | True | 54060.0 | 40.0% | 32.5% | -7.5 |
| 180.0 | 190.0 | app1 | True | 33776.0 | 40.0% | 21.5% | -18.5 |
| 180.0 | 190.0 | app2 | True | 2716.0 | 20.0% | 1.7% | -18.3 |
| 180.0 | 190.0 | end-users | True | 120270.0 | 40.0% | 76.7% | 36.7 |
| 190.0 | 200.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 190.0 | 200.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 190.0 | 200.0 | end-users | True | 165080.0 | 40.0% | 100.0% | 60.0 |
| 200.0 | 210.0 | app1 | True | 63602.0 | 40.0% | 37.0% | -3.0 |
| 200.0 | 210.0 | app2 | True | 59498.0 | 20.0% | 34.6% | 14.6 |
| 200.0 | 210.0 | end-users | True | 48694.0 | 40.0% | 28.3% | -11.7 |
| 210.0 | 220.0 | app1 | True | 17558.0 | 40.0% | 11.5% | -28.5 |
| 210.0 | 220.0 | app2 | True | 1358.0 | 20.0% | 0.9% | -19.1 |
| 210.0 | 220.0 | end-users | True | 133878.0 | 40.0% | 87.6% | 47.6 |
| 220.0 | 230.0 | app1 | True | 2682.0 | 40.0% | 1.6% | -38.4 |
| 220.0 | 230.0 | app2 | True | 2716.0 | 20.0% | 1.6% | -18.4 |
| 220.0 | 230.0 | end-users | True | 162282.0 | 40.0% | 96.8% | 56.8 |
| 230.0 | 240.0 | app1 | True | 75742.0 | 40.0% | 44.8% | 4.8 |
| 230.0 | 240.0 | app2 | True | 59452.0 | 20.0% | 35.2% | 15.2 |
| 230.0 | 240.0 | end-users | True | 33776.0 | 40.0% | 20.0% | -20.0 |
| 240.0 | 250.0 | app1 | False | 2702.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 167732.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 40538.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 43276.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 5428.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 698640 | 34747 | 732100.0 | -0.2% | 761398.0 | 768134.0 | -0.9% | True |
| app2 | 594090 | 29445 | 623535.0 | 0.0% | 635386.0 | 652980.0 | -2.7% | True |
| end-users | 2538720 | 126137 | 2662269.0 | -0.1% | 2738262.0 | 2790994.0 | -1.9% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 576 | 0 | 0 | 0 (never shed) | 0.00% | 40.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 488 | 0 | 0 | 0 (never shed) | 0.00% | 20.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2107 | 0 | 0 | 0 (never shed) | 0.00% | 40.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=3115). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 252232 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
