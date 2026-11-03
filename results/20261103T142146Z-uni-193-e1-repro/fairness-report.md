# Fairness benchmark: full-contention (uni-193-e1-repro)

**Verdict: FAIL** (threshold: 10 points)

- end-users deviated -62.8 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `360` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-jzvg5` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-03T14:22:57Z` |
| Run end | `2026-11-03T14:30:07Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 2732 | 000=16, 200=2702, 500=14 | 1.6 | 15.7 | 2838590.0 | 21.1% | 45.1% | 24.1 | 38.4% | 17.3 | 1.8s | 98.9% | 2111.0 |
| app2 | 10.0 | 32 | 2896 | 000=14, 200=2868, 500=14 | 1.6 | 13.8 | 3100542.0 | 10.5% | 49.3% | 38.7 | 40.7% | 30.1 | 1.9s | 98.9% | 2305.0 |
| end-users | 65.0 | 128 | 1494 | 000=126, 200=1305, 500=63 | 11.5 | 300.0 | 353312.0 | 68.4% | 5.6% | -62.8 | 21.0% | -47.4 | 0.8s | 98.9% | 261.0 |
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

**Windows** (13 total, EPP restart detected mid-window at least once):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 8148.0 | 21.1% | 15.4% | -5.6 |
| 0.0 | 10.0 | app2 | True | 6760.0 | 10.5% | 12.8% | 2.3 |
| 0.0 | 10.0 | end-users | True | 37832.0 | 68.4% | 71.7% | 3.3 |
| 10.0 | 20.0 | app1 | True | 40646.0 | 21.1% | 22.2% | 1.2 |
| 10.0 | 20.0 | app2 | True | 20270.0 | 10.5% | 11.1% | 0.6 |
| 10.0 | 20.0 | end-users | True | 121782.0 | 68.4% | 66.7% | -1.8 |
| 20.0 | 30.0 | app1 | True | 14884.0 | 21.1% | 8.8% | -12.3 |
| 20.0 | 30.0 | app2 | True | 21646.0 | 10.5% | 12.8% | 2.3 |
| 20.0 | 30.0 | end-users | True | 132766.0 | 68.4% | 78.4% | 10.0 |
| 30.0 | 40.0 | app1 | True | 60934.0 | 21.1% | 35.2% | 14.1 |
| 30.0 | 40.0 | app2 | True | 32476.0 | 10.5% | 18.7% | 8.2 |
| 30.0 | 40.0 | end-users | True | 79808.0 | 68.4% | 46.1% | -22.3 |
| 40.0 | 50.0 | app1 | True | 8136.0 | 21.1% | 5.4% | -15.7 |
| 40.0 | 50.0 | app2 | True | 22976.0 | 10.5% | 15.2% | 4.7 |
| 40.0 | 50.0 | end-users | True | 120276.0 | 68.4% | 79.4% | 11.0 |
| 50.0 | 60.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 50.0 | 60.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 50.0 | 60.0 | end-users | True | 170474.0 | 68.4% | 100.0% | 31.6 |
| 60.0 | 70.0 | app1 | True | 52602.0 | 21.1% | 31.6% | 10.6 |
| 60.0 | 70.0 | app2 | True | 60856.0 | 10.5% | 36.6% | 26.1 |
| 60.0 | 70.0 | end-users | True | 52806.0 | 68.4% | 31.8% | -36.7 |
| 70.0 | 80.0 | app1 | True | 29794.0 | 21.1% | 18.4% | -2.7 |
| 70.0 | 80.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 70.0 | 80.0 | end-users | True | 131144.0 | 68.4% | 80.8% | 12.4 |
| 80.0 | 90.0 | app1 | True | 9376.0 | 21.1% | 5.7% | -15.4 |
| 80.0 | 90.0 | app2 | True | 5386.0 | 10.5% | 3.3% | -7.3 |
| 80.0 | 90.0 | end-users | True | 150014.0 | 68.4% | 91.0% | 22.6 |
| 90.0 | 100.0 | app1 | True | 51414.0 | 21.1% | 30.4% | 9.4 |
| 90.0 | 100.0 | app2 | True | 58154.0 | 10.5% | 34.4% | 23.9 |
| 90.0 | 100.0 | end-users | True | 59508.0 | 68.4% | 35.2% | -33.2 |
| 100.0 | 110.0 | app1 | True | 25692.0 | 21.1% | 15.2% | -5.9 |
| 100.0 | 110.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 100.0 | 110.0 | end-users | True | 143454.0 | 68.4% | 84.8% | 16.4 |
| 110.0 | 120.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 110.0 | 120.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 110.0 | 120.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 120.0 | 430.0 | app1 | True | 2838590.0 | 21.1% | 45.1% | 24.1 |
| 120.0 | 430.0 | app2 | True | 3100542.0 | 10.5% | 49.3% | 38.7 |
| 120.0 | 430.0 | end-users | True | 353312.0 | 68.4% | 5.6% | -62.8 |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens -21.9%, cost -22.3%
- app2 exceeded the 10% ledger tolerance: raw tokens -19.6%, cost -20.1%
- end-users exceeded the 10% ledger tolerance: raw tokens -80.0%, cost -80.0%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 3323460 | 165456 | 2725670.0 | -21.9% | 2838590.0 | 3654372.0 | -22.3% | False |
| app2 | 3527640 | 175870 | 2976638.0 | -19.6% | 3100542.0 | 3879380.0 | -20.1% | False |
| end-users | 1605150 | 80178 | 337171.0 | -80.0% | 353312.0 | 1765506.0 | -80.0% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2732 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 2896 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1494 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=4677). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 265309 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
