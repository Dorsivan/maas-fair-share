# Fairness benchmark: full-contention (uni-155-e1-epp-restart-mid-run)

**Verdict: FAIL** (threshold: 10 points)

- end-users deviated -68.4 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `360` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-jqczv` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-03T13:47:42Z` |
| Run end | `2026-11-03T13:54:51Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 3075 | 000=12, 200=3052, 500=11 | 1.7 | 12.9 | 3240288.0 | 21.1% | 52.2% | 31.2 | 43.5% | 22.5 | 2.6s | 98.9% | 2416.0 |
| app2 | 10.0 | 32 | 2795 | 000=13, 200=2769, 500=13 | 1.8 | 16.2 | 2966660.0 | 10.5% | 47.8% | 37.3 | 39.6% | 29.0 | 2.6s | 98.9% | 2209.0 |
| end-users | 65.0 | 128 | 1196 | 000=128, 200=1019, 500=49 | 14.5 | 300.0 | n/a | 68.4% | 0.0% | -68.4 | 16.9% | -51.5 | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events (scheduled):**
- t+120s: epp_delete

**Per-tenant schedule:**
- app1: active 0s-360s, no duty cycle
- app2: active 0s-360s, no duty cycle
- end-users: active 0s-360s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 120.0 | n/a (never converged in this phase) | n/a |
| 360.0 | n/a (never converged in this phase) | n/a |

**Windows** (14 total, EPP restart detected mid-window at least once):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 10812.0 | 21.1% | 12.7% | -8.4 |
| 0.0 | 10.0 | app2 | True | 8068.0 | 10.5% | 9.5% | -1.1 |
| 0.0 | 10.0 | end-users | True | 66268.0 | 68.4% | 77.8% | 9.4 |
| 10.0 | 20.0 | app1 | True | 33812.0 | 21.1% | 18.1% | -2.9 |
| 10.0 | 20.0 | app2 | True | 26990.0 | 10.5% | 14.5% | 3.9 |
| 10.0 | 20.0 | end-users | True | 125870.0 | 68.4% | 67.4% | -1.0 |
| 20.0 | 30.0 | app1 | True | 36510.0 | 21.1% | 21.2% | 0.2 |
| 20.0 | 30.0 | app2 | True | 17552.0 | 10.5% | 10.2% | -0.3 |
| 20.0 | 30.0 | end-users | True | 117782.0 | 68.4% | 68.5% | 0.1 |
| 30.0 | 40.0 | app1 | True | 24342.0 | 21.1% | 14.5% | -6.6 |
| 30.0 | 40.0 | app2 | True | 29812.0 | 10.5% | 17.8% | 7.2 |
| 30.0 | 40.0 | end-users | True | 113732.0 | 68.4% | 67.7% | -0.7 |
| 40.0 | 50.0 | app1 | True | 32414.0 | 21.1% | 21.4% | 0.4 |
| 40.0 | 50.0 | app2 | True | 16238.0 | 10.5% | 10.7% | 0.2 |
| 40.0 | 50.0 | end-users | True | 102748.0 | 68.4% | 67.9% | -0.6 |
| 50.0 | 60.0 | app1 | True | 9498.0 | 21.1% | 5.6% | -15.4 |
| 50.0 | 60.0 | app2 | True | 22966.0 | 10.5% | 13.6% | 3.0 |
| 50.0 | 60.0 | end-users | True | 136710.0 | 68.4% | 80.8% | 12.4 |
| 60.0 | 70.0 | app1 | True | 48714.0 | 21.1% | 28.4% | 7.3 |
| 60.0 | 70.0 | app2 | True | 44684.0 | 10.5% | 26.0% | 15.5 |
| 60.0 | 70.0 | end-users | True | 78426.0 | 68.4% | 45.6% | -22.8 |
| 70.0 | 80.0 | app1 | True | 21706.0 | 21.1% | 14.6% | -6.5 |
| 70.0 | 80.0 | app2 | True | 10808.0 | 10.5% | 7.3% | -3.3 |
| 70.0 | 80.0 | end-users | True | 116362.0 | 68.4% | 78.2% | 9.7 |
| 80.0 | 90.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 80.0 | 90.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 80.0 | 90.0 | end-users | True | 169118.0 | 68.4% | 100.0% | 31.6 |
| 90.0 | 100.0 | app1 | True | 55458.0 | 21.1% | 32.6% | 11.5 |
| 90.0 | 100.0 | app2 | True | 63556.0 | 10.5% | 37.3% | 26.8 |
| 90.0 | 100.0 | end-users | True | 51322.0 | 68.4% | 30.1% | -38.3 |
| 100.0 | 110.0 | app1 | True | 31156.0 | 21.1% | 18.9% | -2.2 |
| 100.0 | 110.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 100.0 | 110.0 | end-users | True | 132626.0 | 68.4% | 80.3% | 11.9 |
| 110.0 | 120.0 | app1 | True | 10812.0 | 21.1% | 7.1% | -14.0 |
| 110.0 | 120.0 | app2 | True | 6784.0 | 10.5% | 4.4% | -6.1 |
| 110.0 | 120.0 | end-users | True | 135334.0 | 68.4% | 88.5% | 20.1 |
| 120.0 | 130.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 120.0 | 130.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 120.0 | 130.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 130.0 | 429.0 | app1 | True | 3240288.0 | 21.1% | 52.2% | 31.2 |
| 130.0 | 429.0 | app2 | True | 2966660.0 | 10.5% | 47.8% | 37.3 |
| 130.0 | 429.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens -20.8%, cost -21.5%
- app2 exceeded the 10% ledger tolerance: raw tokens -20.2%, cost -20.8%
- end-users exceeded the 10% ledger tolerance: raw tokens n/a, cost n/a

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 3753960 | 187686 | 3120201.0 | -20.8% | 3240288.0 | 4129332.0 | -21.5% | False |
| app2 | 3405870 | 169904 | 2852715.0 | -20.2% | 2966660.0 | 3745678.0 | -20.8% | False |
| end-users | 1253370 | 62714 | n/a | n/a | n/a | 1378798.0 | n/a | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 3075 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 2795 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1196 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

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
