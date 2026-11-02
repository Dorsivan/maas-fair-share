# Fairness benchmark: full-contention (uni-148-c6-context-length-errors)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-nnc8m` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-02T15:38:33Z` |
| Run end | `2026-11-02T15:43:47Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 545 | 200=535, 500=10 | 17.5 | 22.8 | 695296.0 | 21.1% | 15.2% | -5.9 | 16.8% | -4.3 | 1.6s | 98.9% | 532.0 |
| app2 | 10.0 | 32 | 49 | 000=32, 400=3, 500=14 | 300.4 | 300.8 | 423612.0 | 10.5% | 9.3% | -1.3 | 1.5% | -9.0 | 0.2s | n/a | 32.0 |
| end-users | 65.0 | 128 | 2650 | 200=2604, 500=46 | 12.6 | 14.5 | 3457242.0 | 68.4% | 75.5% | 7.1 | 81.7% | 13.3 | 1.7s | 98.9% | 2595.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 61607.0 | n/a | n/a | n/a | n/a | n/a | 0.1s | 98.9% | 15.0 |

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

**Windows** (32 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 9470.0 | 21.1% | 3.1% | -18.0 |
| 0.0 | 10.0 | app2 | True | 242064.0 | 10.5% | 79.2% | 68.7 |
| 0.0 | 10.0 | end-users | True | 54156.0 | 68.4% | 17.7% | -50.7 |
| 10.0 | 20.0 | app1 | True | 29774.0 | 21.1% | 8.4% | -12.7 |
| 10.0 | 20.0 | app2 | True | 181548.0 | 10.5% | 51.0% | 40.5 |
| 10.0 | 20.0 | end-users | True | 144798.0 | 68.4% | 40.7% | -27.8 |
| 20.0 | 30.0 | app1 | True | 44606.0 | 21.1% | 25.6% | 4.5 |
| 20.0 | 30.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 20.0 | 30.0 | end-users | True | 129768.0 | 68.4% | 74.4% | 6.0 |
| 30.0 | 40.0 | app1 | True | 12120.0 | 21.1% | 7.1% | -13.9 |
| 30.0 | 40.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 30.0 | 40.0 | end-users | True | 158160.0 | 68.4% | 92.9% | 24.5 |
| 40.0 | 50.0 | app1 | True | 60984.0 | 21.1% | 35.5% | 14.4 |
| 40.0 | 50.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 40.0 | 50.0 | end-users | True | 110992.0 | 68.4% | 64.5% | -3.9 |
| 50.0 | 60.0 | app1 | True | 2716.0 | 21.1% | 1.6% | -19.5 |
| 50.0 | 60.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 50.0 | 60.0 | end-users | True | 169042.0 | 68.4% | 98.4% | 30.0 |
| 60.0 | 70.0 | app1 | True | 22960.0 | 21.1% | 15.1% | -5.9 |
| 60.0 | 70.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 60.0 | 70.0 | end-users | True | 128648.0 | 68.4% | 84.9% | 16.4 |
| 70.0 | 80.0 | app1 | True | 41956.0 | 21.1% | 24.6% | 3.6 |
| 70.0 | 80.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 70.0 | 80.0 | end-users | True | 128322.0 | 68.4% | 75.4% | 6.9 |
| 80.0 | 90.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 80.0 | 90.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 80.0 | 90.0 | end-users | True | 167646.0 | 68.4% | 100.0% | 31.6 |
| 90.0 | 100.0 | app1 | True | 43252.0 | 21.1% | 25.6% | 4.5 |
| 90.0 | 100.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 90.0 | 100.0 | end-users | True | 125770.0 | 68.4% | 74.4% | 6.0 |
| 100.0 | 110.0 | app1 | True | 43296.0 | 21.1% | 25.2% | 4.2 |
| 100.0 | 110.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 100.0 | 110.0 | end-users | True | 128344.0 | 68.4% | 74.8% | 6.4 |
| 110.0 | 120.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 110.0 | 120.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 110.0 | 120.0 | end-users | True | 171688.0 | 68.4% | 100.0% | 31.6 |
| 120.0 | 130.0 | app1 | True | 43254.0 | 21.1% | 25.6% | 4.5 |
| 120.0 | 130.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 120.0 | 130.0 | end-users | True | 125852.0 | 68.4% | 74.4% | 6.0 |
| 130.0 | 140.0 | app1 | True | 14868.0 | 21.1% | 9.6% | -11.4 |
| 130.0 | 140.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 130.0 | 140.0 | end-users | True | 139328.0 | 68.4% | 90.4% | 21.9 |
| 140.0 | 150.0 | app1 | True | 29780.0 | 21.1% | 17.9% | -3.1 |
| 140.0 | 150.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 140.0 | 150.0 | end-users | True | 136556.0 | 68.4% | 82.1% | 13.7 |
| 150.0 | 160.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 150.0 | 160.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 150.0 | 160.0 | end-users | True | 167834.0 | 68.4% | 100.0% | 31.6 |
| 160.0 | 170.0 | app1 | True | 62224.0 | 21.1% | 36.5% | 15.5 |
| 160.0 | 170.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 160.0 | 170.0 | end-users | True | 108140.0 | 68.4% | 63.5% | -4.9 |
| 170.0 | 180.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 170.0 | 180.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 170.0 | 180.0 | end-users | True | 170472.0 | 68.4% | 100.0% | 31.6 |
| 180.0 | 190.0 | app1 | True | 62270.0 | 21.1% | 37.4% | 16.4 |
| 180.0 | 190.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 180.0 | 190.0 | end-users | True | 104178.0 | 68.4% | 62.6% | -5.8 |
| 190.0 | 200.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 190.0 | 200.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 190.0 | 200.0 | end-users | True | 166438.0 | 68.4% | 100.0% | 31.6 |
| 200.0 | 210.0 | app1 | True | 45954.0 | 21.1% | 27.9% | 6.8 |
| 200.0 | 210.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 200.0 | 210.0 | end-users | True | 119002.0 | 68.4% | 72.1% | 3.7 |
| 210.0 | 220.0 | app1 | True | 18958.0 | 21.1% | 12.0% | -9.1 |
| 210.0 | 220.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 210.0 | 220.0 | end-users | True | 139328.0 | 68.4% | 88.0% | 19.6 |
| 220.0 | 230.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 220.0 | 230.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 220.0 | 230.0 | end-users | True | 166388.0 | 68.4% | 100.0% | 31.6 |
| 230.0 | 240.0 | app1 | True | 63554.0 | 21.1% | 37.9% | 16.8 |
| 230.0 | 240.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 230.0 | 240.0 | end-users | True | 104216.0 | 68.4% | 62.1% | -6.3 |
| 240.0 | 250.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 170520.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 43300.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 21656.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 314.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 314.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 314.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: raw tokens n/a, cost n/a

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 658050 | 32821 | 686998.0 | -0.6% | 695296.0 | 723692.0 | -3.9% | True |
| app2 | 0 | 0 | n/a | n/a | 423612.0 | 0.0 | n/a | False |
| end-users | 3202920 | 159678 | 3350981.0 | -0.3% | 3457242.0 | 3522276.0 | -1.8% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 545 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 49 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2650 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

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
