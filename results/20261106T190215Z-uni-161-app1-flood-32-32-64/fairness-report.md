# Fairness benchmark: app1-flood-light (uni-161-app1-flood-32-32-64)

**Verdict: FAIL** (threshold: 10 points)

- app2 deviated +12.6 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-flood-light` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-796bc55c4b-5rzv9` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-06T19:03:26Z` |
| Run end | `2026-11-06T19:07:49Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 30.0 | 32 | 834 | 200=825, 500=9 | 9.8 | 14.4 | 1100578.0 | 30.0% | 25.8% | -4.2 | 25.7% | -4.3 | 2.7s | 98.9% | 825.0 |
| app2 | 10.0 | 32 | 742 | 200=732, 500=10 | 10.1 | 16.4 | 962896.0 | 10.0% | 22.6% | 12.6 | 22.8% | 12.8 | 2.3s | 98.9% | 732.0 |
| end-users | 60.0 | 64 | 1673 | 200=1644, 500=29 | 9.4 | 13.0 | 2197462.0 | 60.0% | 51.6% | -8.4 | 51.5% | -8.5 | 2.5s | 98.9% | 1642.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 2668.0 | n/a | n/a | n/a | n/a | n/a | 0.0s | 98.9% | 2.0 |

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
| 0.0 | 10.0 | app1 | True | 33720.0 | 30.0% | 26.8% | -3.2 |
| 0.0 | 10.0 | app2 | True | 32524.0 | 10.0% | 25.9% | 15.9 |
| 0.0 | 10.0 | end-users | True | 59506.0 | 60.0% | 47.3% | -12.7 |
| 10.0 | 20.0 | app1 | True | 49982.0 | 30.0% | 28.2% | -1.8 |
| 10.0 | 20.0 | app2 | True | 37830.0 | 10.0% | 21.3% | 11.3 |
| 10.0 | 20.0 | end-users | True | 89420.0 | 60.0% | 50.5% | -9.5 |
| 20.0 | 30.0 | app1 | True | 43306.0 | 30.0% | 25.8% | -4.2 |
| 20.0 | 30.0 | app2 | True | 31160.0 | 10.0% | 18.6% | 8.6 |
| 20.0 | 30.0 | end-users | True | 93140.0 | 60.0% | 55.6% | -4.4 |
| 30.0 | 40.0 | app1 | True | 44716.0 | 30.0% | 26.9% | -3.1 |
| 30.0 | 40.0 | app2 | True | 39278.0 | 10.0% | 23.6% | 13.6 |
| 30.0 | 40.0 | end-users | True | 82538.0 | 60.0% | 49.6% | -10.4 |
| 40.0 | 50.0 | app1 | True | 44632.0 | 30.0% | 25.8% | -4.2 |
| 40.0 | 50.0 | app2 | True | 32500.0 | 10.0% | 18.8% | 8.8 |
| 40.0 | 50.0 | end-users | True | 95928.0 | 60.0% | 55.4% | -4.6 |
| 50.0 | 61.0 | app1 | True | 45998.0 | 30.0% | 27.2% | -2.8 |
| 50.0 | 61.0 | app2 | True | 40584.0 | 10.0% | 24.0% | 14.0 |
| 50.0 | 61.0 | end-users | True | 82488.0 | 60.0% | 48.8% | -11.2 |
| 61.0 | 71.0 | app1 | True | 41804.0 | 30.0% | 23.8% | -6.2 |
| 61.0 | 71.0 | app2 | True | 40568.0 | 10.0% | 23.1% | 13.1 |
| 61.0 | 71.0 | end-users | True | 93298.0 | 60.0% | 53.1% | -6.9 |
| 71.0 | 81.0 | app1 | True | 41960.0 | 30.0% | 23.0% | -7.0 |
| 71.0 | 81.0 | app2 | True | 58210.0 | 10.0% | 31.9% | 21.9 |
| 71.0 | 81.0 | end-users | True | 82406.0 | 60.0% | 45.1% | -14.9 |
| 81.0 | 91.0 | app1 | True | 37850.0 | 30.0% | 22.7% | -7.3 |
| 81.0 | 91.0 | app2 | True | 17592.0 | 10.0% | 10.6% | 0.6 |
| 81.0 | 91.0 | end-users | True | 110958.0 | 60.0% | 66.7% | 6.7 |
| 91.0 | 101.0 | app1 | True | 36488.0 | 30.0% | 21.2% | -8.8 |
| 91.0 | 101.0 | app2 | True | 36480.0 | 10.0% | 21.2% | 11.2 |
| 91.0 | 101.0 | end-users | True | 98756.0 | 60.0% | 57.5% | -2.5 |
| 101.0 | 111.0 | app1 | True | 62152.0 | 30.0% | 36.2% | 6.2 |
| 101.0 | 111.0 | app2 | True | 52748.0 | 10.0% | 30.7% | 20.7 |
| 101.0 | 111.0 | end-users | True | 56826.0 | 60.0% | 33.1% | -26.9 |
| 111.0 | 121.0 | app1 | True | 36498.0 | 30.0% | 21.2% | -8.8 |
| 111.0 | 121.0 | app2 | True | 40534.0 | 10.0% | 23.6% | 13.6 |
| 111.0 | 121.0 | end-users | True | 94792.0 | 60.0% | 55.2% | -4.8 |
| 121.0 | 131.0 | app1 | True | 48702.0 | 30.0% | 29.0% | -1.0 |
| 121.0 | 131.0 | app2 | True | 18924.0 | 10.0% | 11.3% | 1.3 |
| 121.0 | 131.0 | end-users | True | 100102.0 | 60.0% | 59.7% | -0.3 |
| 131.0 | 141.0 | app1 | True | 41848.0 | 30.0% | 23.4% | -6.6 |
| 131.0 | 141.0 | app2 | True | 54140.0 | 10.0% | 30.3% | 20.3 |
| 131.0 | 141.0 | end-users | True | 82488.0 | 60.0% | 46.2% | -13.8 |
| 141.0 | 151.0 | app1 | True | 66232.0 | 30.0% | 37.4% | 7.4 |
| 141.0 | 151.0 | app2 | True | 32484.0 | 10.0% | 18.3% | 8.3 |
| 141.0 | 151.0 | end-users | True | 78390.0 | 60.0% | 44.3% | -15.7 |
| 151.0 | 161.0 | app1 | True | 6790.0 | 30.0% | 4.0% | -26.0 |
| 151.0 | 161.0 | app2 | True | 43166.0 | 10.0% | 25.6% | 15.6 |
| 151.0 | 161.0 | end-users | True | 118968.0 | 60.0% | 70.4% | 10.4 |
| 161.0 | 171.0 | app1 | True | 55426.0 | 30.0% | 32.8% | 2.8 |
| 161.0 | 171.0 | app2 | True | 54104.0 | 10.0% | 32.0% | 22.0 |
| 161.0 | 171.0 | end-users | True | 59482.0 | 60.0% | 35.2% | -24.8 |
| 171.0 | 181.0 | app1 | True | 36514.0 | 30.0% | 21.4% | -8.6 |
| 171.0 | 181.0 | app2 | True | 5432.0 | 10.0% | 3.2% | -6.8 |
| 171.0 | 181.0 | end-users | True | 128448.0 | 60.0% | 75.4% | 15.4 |
| 181.0 | 191.0 | app1 | True | 55520.0 | 30.0% | 32.6% | 2.6 |
| 181.0 | 191.0 | app2 | True | 58106.0 | 10.0% | 34.1% | 24.1 |
| 181.0 | 191.0 | end-users | True | 56756.0 | 60.0% | 33.3% | -26.7 |
| 191.0 | 201.0 | app1 | True | 50042.0 | 30.0% | 29.4% | -0.6 |
| 191.0 | 201.0 | app2 | True | 21606.0 | 10.0% | 12.7% | 2.7 |
| 191.0 | 201.0 | end-users | True | 98618.0 | 60.0% | 57.9% | -2.1 |
| 201.0 | 211.0 | app1 | True | 43266.0 | 30.0% | 23.9% | -6.1 |
| 201.0 | 211.0 | app2 | True | 52762.0 | 10.0% | 29.1% | 19.1 |
| 201.0 | 211.0 | end-users | True | 85280.0 | 60.0% | 47.0% | -13.0 |
| 211.0 | 221.0 | app1 | True | 31120.0 | 30.0% | 18.3% | -11.7 |
| 211.0 | 221.0 | app2 | True | 21620.0 | 10.0% | 12.7% | 2.7 |
| 211.0 | 221.0 | end-users | True | 117654.0 | 60.0% | 69.0% | 9.0 |
| 221.0 | 231.0 | app1 | True | 43282.0 | 30.0% | 25.2% | -4.8 |
| 221.0 | 231.0 | app2 | True | 43286.0 | 10.0% | 25.2% | 15.2 |
| 221.0 | 231.0 | end-users | True | 85094.0 | 60.0% | 49.6% | -10.4 |
| 231.0 | 241.0 | app1 | True | 58172.0 | 30.0% | 34.1% | 4.1 |
| 231.0 | 241.0 | app2 | True | 54004.0 | 10.0% | 31.7% | 21.7 |
| 231.0 | 241.0 | end-users | True | 58224.0 | 60.0% | 34.2% | -25.8 |
| 241.0 | 251.0 | app1 | False | 44558.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 35128.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 87902.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 8126.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1014750 | 50356 | 1065106.0 | 0.0% | 1100578.0 | 1115462.0 | -1.3% | True |
| app2 | 900360 | 44784 | 945144.0 | 0.0% | 962896.0 | 989928.0 | -2.7% | True |
| end-users | 2022120 | 100527 | 2120083.0 | -0.1% | 2197462.0 | 2223174.0 | -1.2% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 834 | 0 | 0 | 0 (never shed) | 0.00% | 30.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 742 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1673 | 0 | 0 | 0 (never shed) | 0.00% | 60.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=3201). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 252574 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
