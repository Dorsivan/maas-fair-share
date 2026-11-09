# Fairness benchmark: cache-heavy-vs-cache-cold (uni-214-c8-baseline-q2p3)

**Verdict: FAIL** -- named negative control, not scored against the 10-point threshold. Expected to NOT reproduce the configured weights; see docs/runbook.md.

- offered groups delivered zero contended service tokens -- the EPP accounted nothing for this run
- negative control, not scored against the 10-point threshold: max deviation was 66.7 points. This scenario is expected to compress toward equal shares, not reproduce the configured weights -- see docs/runbook.md's 'Per-tenant worker sizing and the saturation check'

## Run metadata

| field | value |
|---|---|
| Scenario | `cache-heavy-vs-cache-cold` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-84dd99f8bb-wrwlw` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T23:27:33Z` |
| Run end | `2026-11-09T23:31:45Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 64 | 3804 | 200=3748, 500=56 | 4.1 | 4.3 | n/a | 66.7% | 0.0% | -66.7 | 67.1% | 0.5 | n/a | 87.7% | 3738.0 |
| app2 | 10.0 | 32 | 1863 | 200=1831, 500=32 | 4.2 | 4.4 | n/a | 33.3% | 0.0% | -33.3 | 32.9% | -0.5 | n/a | 6.3% | 1829.0 |
| end-users | 65.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 70.9% | 12.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 0.0 | 10.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 10.0 | 20.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 10.0 | 20.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 20.0 | 30.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 20.0 | 30.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 30.0 | 40.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 30.0 | 40.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 40.0 | 50.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 40.0 | 50.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 50.0 | 60.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 50.0 | 60.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 60.0 | 70.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 60.0 | 70.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 70.0 | 80.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 70.0 | 80.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 80.0 | 90.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 80.0 | 90.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 90.0 | 100.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 90.0 | 100.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 100.0 | 110.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 100.0 | 110.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 110.0 | 120.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 110.0 | 120.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 120.0 | 130.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 120.0 | 130.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 130.0 | 140.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 130.0 | 140.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 140.0 | 150.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 140.0 | 150.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 150.0 | 160.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 150.0 | 160.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 160.0 | 170.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 160.0 | 170.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 170.0 | 180.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 170.0 | 180.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 180.0 | 190.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 180.0 | 190.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 190.0 | 200.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 190.0 | 200.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 200.0 | 210.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 200.0 | 210.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 210.0 | 221.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 210.0 | 221.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 221.0 | 231.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 221.0 | 231.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 231.0 | 241.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 231.0 | 241.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 241.0 | 251.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 252.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 252.0 | app2 | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 140 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 67 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 160 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app2 | ok | 74 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app1 | ok | 154 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app2 | ok | 79 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app1 | ok | 158 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | app1 | ok | 156 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | app2 | ok | 79 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app1 | ok | 151 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app2 | ok | 76 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app1 | ok | 162 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app2 | ok | 73 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app1 | ok | 150 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app2 | ok | 82 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app1 | ok | 158 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app2 | ok | 73 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | app1 | ok | 154 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | app2 | ok | 76 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | app1 | ok | 156 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | app2 | ok | 76 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | app1 | ok | 160 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | app1 | ok | 149 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | app2 | ok | 79 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | app1 | ok | 161 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | app2 | ok | 74 | 0ms | 0ms | 0ms |
| 140.0 | 150.0 | app1 | ok | 156 | 0ms | 0ms | 0ms |
| 140.0 | 150.0 | app2 | ok | 77 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | app1 | ok | 156 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 160.0 | 170.0 | app1 | ok | 154 | 0ms | 0ms | 0ms |
| 160.0 | 170.0 | app2 | ok | 77 | 0ms | 0ms | 0ms |
| 170.0 | 180.0 | app1 | ok | 152 | 0ms | 0ms | 0ms |
| 170.0 | 180.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 180.0 | 190.0 | app1 | ok | 156 | 0ms | 0ms | 0ms |
| 180.0 | 190.0 | app2 | ok | 75 | 0ms | 0ms | 0ms |
| 190.0 | 200.0 | app1 | ok | 150 | 0ms | 0ms | 0ms |
| 190.0 | 200.0 | app2 | ok | 81 | 0ms | 0ms | 0ms |
| 200.0 | 210.0 | app1 | ok | 159 | 0ms | 0ms | 0ms |
| 200.0 | 210.0 | app2 | ok | 74 | 0ms | 0ms | 0ms |
| 210.0 | 221.0 | app1 | ok | 155 | 0ms | 0ms | 0ms |
| 210.0 | 221.0 | app2 | ok | 76 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | app1 | ok | 159 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | app2 | ok | 78 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | app1 | ok | 158 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | app2 | ok | 76 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | app1 | ok | 14 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | app2 | ok | 7 | 0ms | 0ms | 0ms |
| 251.0 | 252.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 252.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost n/a
- app2 exceeded the 10% ledger tolerance: cost n/a

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 754592 | 210337 | 962331.0 | -0.3% | n/a | 1175266.0 | n/a | False |
| app2 | 469453 | 116414 | 585226.0 | -0.1% | n/a | 702281.0 | n/a | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 3804 | 0 | 0 | 0 (never shed) | 0.00% | 66.7% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1863 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5579). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5579 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 243377 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
