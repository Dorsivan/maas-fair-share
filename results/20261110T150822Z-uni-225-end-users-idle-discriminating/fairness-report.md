# Fairness benchmark: end-users-idle-discriminating (uni-225-end-users-idle-discriminating)

**Verdict: FAIL** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 33.3 points

- app1 deviated -32.8 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `end-users-idle-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-85575669d6-dvn87` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-10T15:09:36Z` |
| Run end | `2026-11-10T15:13:58Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 64 | 1915 | 000=126, 200=1746, 500=43 | 7.8 | 12.7 | 2130194.0 | 66.7% | 33.3% | -33.3 | 33.8% | -32.8 | 33.7% | -33.0 | 24.5s | 98.9% | 1766.0 |
| app2 | 10.0 | 128 | 3769 | 000=246, 200=3437, 500=84, 503=2 | 7.9 | 12.0 | 4166562.0 | 33.3% | 66.7% | 33.3 | 66.2% | 32.8 | 66.3% | 33.0 | 24.5s | 98.9% | 3499.0 |
| end-users | 65.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 10.0 |

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

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 0.0 | 10.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 10.0 | 20.0 | app1 | True | 58094.0 | 66.7% | 38.0% | -28.6 |
| 10.0 | 20.0 | app2 | True | 94650.0 | 33.3% | 62.0% | 28.6 |
| 20.0 | 30.0 | app1 | True | 109568.0 | 66.7% | 36.0% | -30.7 |
| 20.0 | 30.0 | app2 | True | 194844.0 | 33.3% | 64.0% | 30.7 |
| 30.0 | 40.0 | app1 | True | 96084.0 | 66.7% | 32.3% | -34.4 |
| 30.0 | 40.0 | app2 | True | 201482.0 | 33.3% | 67.7% | 34.4 |
| 40.0 | 50.0 | app1 | True | 98804.0 | 66.7% | 32.2% | -34.5 |
| 40.0 | 50.0 | app2 | True | 208142.0 | 33.3% | 67.8% | 34.5 |
| 50.0 | 60.0 | app1 | True | 137926.0 | 66.7% | 45.3% | -21.4 |
| 50.0 | 60.0 | app2 | True | 166498.0 | 33.3% | 54.7% | 21.4 |
| 60.0 | 70.0 | app1 | True | 40526.0 | 66.7% | 16.6% | -50.1 |
| 60.0 | 70.0 | app2 | True | 204296.0 | 33.3% | 83.4% | 50.1 |
| 70.0 | 80.0 | app1 | True | 79692.0 | 66.7% | 38.8% | -27.9 |
| 70.0 | 80.0 | app2 | True | 125842.0 | 33.3% | 61.2% | 27.9 |
| 80.0 | 90.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 80.0 | 90.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 90.0 | 100.0 | app1 | True | 64884.0 | 66.7% | 48.5% | -18.2 |
| 90.0 | 100.0 | app2 | True | 68966.0 | 33.3% | 51.5% | 18.2 |
| 100.0 | 110.0 | app1 | True | 75686.0 | 66.7% | 26.3% | -40.4 |
| 100.0 | 110.0 | app2 | True | 212392.0 | 33.3% | 73.7% | 40.4 |
| 110.0 | 120.0 | app1 | True | 113492.0 | 66.7% | 37.5% | -29.2 |
| 110.0 | 120.0 | app2 | True | 189390.0 | 33.3% | 62.5% | 29.2 |
| 120.0 | 130.0 | app1 | True | 89392.0 | 66.7% | 34.7% | -31.9 |
| 120.0 | 130.0 | app2 | True | 167884.0 | 33.3% | 65.3% | 31.9 |
| 130.0 | 140.0 | app1 | True | 106864.0 | 66.7% | 37.1% | -29.6 |
| 130.0 | 140.0 | app2 | True | 181362.0 | 33.3% | 62.9% | 29.6 |
| 140.0 | 150.0 | app1 | True | 125708.0 | 66.7% | 41.7% | -25.0 |
| 140.0 | 150.0 | app2 | True | 175846.0 | 33.3% | 58.3% | 25.0 |
| 150.0 | 160.0 | app1 | True | 66292.0 | 66.7% | 22.8% | -43.9 |
| 150.0 | 160.0 | app2 | True | 224440.0 | 33.3% | 77.2% | 43.9 |
| 160.0 | 170.0 | app1 | True | 85162.0 | 66.7% | 33.0% | -33.7 |
| 160.0 | 170.0 | app2 | True | 173262.0 | 33.3% | 67.0% | 33.7 |
| 170.0 | 180.0 | app1 | True | 123156.0 | 66.7% | 40.3% | -26.4 |
| 170.0 | 180.0 | app2 | True | 182590.0 | 33.3% | 59.7% | 26.4 |
| 180.0 | 190.0 | app1 | True | 106916.0 | 66.7% | 35.1% | -31.5 |
| 180.0 | 190.0 | app2 | True | 197538.0 | 33.3% | 64.9% | 31.5 |
| 190.0 | 201.0 | app1 | True | 108234.0 | 66.7% | 35.9% | -30.8 |
| 190.0 | 201.0 | app2 | True | 193454.0 | 33.3% | 64.1% | 30.8 |
| 201.0 | 211.0 | app1 | True | 86594.0 | 66.7% | 29.0% | -37.7 |
| 201.0 | 211.0 | app2 | True | 212378.0 | 33.3% | 71.0% | 37.7 |
| 211.0 | 221.0 | app1 | True | 90558.0 | 66.7% | 34.2% | -32.5 |
| 211.0 | 221.0 | app2 | True | 174608.0 | 33.3% | 65.8% | 32.5 |
| 221.0 | 231.0 | app1 | True | 87996.0 | 66.7% | 28.9% | -37.8 |
| 221.0 | 231.0 | app2 | True | 216384.0 | 33.3% | 71.1% | 37.8 |
| 231.0 | 241.0 | app1 | True | 75714.0 | 66.7% | 25.4% | -41.2 |
| 231.0 | 241.0 | app2 | True | 221806.0 | 33.3% | 74.6% | 41.2 |
| 241.0 | 251.0 | app1 | False | 92028.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 167682.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 10824.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 10826.0 | n/a | n/a | n/a |
| 261.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 54 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 115 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 118 | 500ms | 3361ms | 4836ms |
| 10.0 | 20.0 | app2 | ok | 201 | 658ms | 2990ms | 4799ms |
| 20.0 | 30.0 | app1 | ok | 76 | 2350ms | 4457ms | 4946ms |
| 20.0 | 30.0 | app2 | ok | 148 | 3506ms | 6636ms | 9664ms |
| 30.0 | 40.0 | app1 | ok | 87 | 3549ms | 6045ms | 9605ms |
| 30.0 | 40.0 | app2 | ok | 167 | 3181ms | 4834ms | 9165ms |
| 40.0 | 50.0 | app1 | ok | 72 | 3686ms | 4907ms | 9280ms |
| 40.0 | 50.0 | app2 | ok | 105 | 3589ms | 4718ms | 4972ms |
| 50.0 | 60.0 | app1 | ok | 71 | 1664ms | 3891ms | 4889ms |
| 50.0 | 60.0 | app2 | ok | 165 | 3859ms | 8382ms | 9838ms |
| 60.0 | 70.0 | app1 | ok | 51 | 5750ms | 9150ms | 9915ms |
| 60.0 | 70.0 | app2 | ok | 74 | 3276ms | 7824ms | 9782ms |
| 70.0 | 80.0 | app1 | ok | 29 | 3550ms | 4710ms | 4971ms |
| 70.0 | 80.0 | app2 | ok | 131 | 3022ms | 4680ms | 7817ms |
| 80.0 | 90.0 | app1 | ok | 65 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app2 | ok | 121 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | app1 | ok | 126 | 636ms | 2238ms | 4550ms |
| 90.0 | 100.0 | app2 | ok | 217 | 441ms | 2454ms | 4729ms |
| 100.0 | 110.0 | app1 | ok | 64 | 2692ms | 6000ms | 9600ms |
| 100.0 | 110.0 | app2 | ok | 114 | 3544ms | 4797ms | 8575ms |
| 110.0 | 120.0 | app1 | ok | 64 | 1397ms | 2714ms | 4771ms |
| 110.0 | 120.0 | app2 | ok | 122 | 3679ms | 7458ms | 9746ms |
| 120.0 | 130.0 | app1 | ok | 60 | 2812ms | 4688ms | 8500ms |
| 120.0 | 130.0 | app2 | ok | 115 | 3285ms | 4760ms | 8562ms |
| 130.0 | 140.0 | app1 | ok | 80 | 2050ms | 4712ms | 9200ms |
| 130.0 | 140.0 | app2 | ok | 167 | 4274ms | 8425ms | 9842ms |
| 140.0 | 150.0 | app1 | ok | 101 | 1483ms | 3738ms | 4874ms |
| 140.0 | 150.0 | app2 | ok | 152 | 4167ms | 8480ms | 9848ms |
| 150.0 | 160.0 | app1 | ok | 53 | 3977ms | 8795ms | 9880ms |
| 150.0 | 160.0 | app2 | ok | 125 | 2395ms | 4470ms | 4947ms |
| 160.0 | 170.0 | app1 | ok | 64 | 3043ms | 7714ms | 9771ms |
| 160.0 | 170.0 | app2 | ok | 138 | 3889ms | 7909ms | 9791ms |
| 170.0 | 180.0 | app1 | ok | 71 | 2724ms | 4545ms | 4954ms |
| 170.0 | 180.0 | app2 | ok | 129 | 3849ms | 4980ms | 9462ms |
| 180.0 | 190.0 | app1 | ok | 66 | 3602ms | 4720ms | 4972ms |
| 180.0 | 190.0 | app2 | ok | 177 | 3742ms | 4938ms | 9368ms |
| 190.0 | 201.0 | app1 | ok | 129 | 2705ms | 4631ms | 7850ms |
| 190.0 | 201.0 | app2 | ok | 175 | 3720ms | 6196ms | 9620ms |
| 201.0 | 211.0 | app1 | ok | 64 | 2304ms | 4448ms | 4945ms |
| 201.0 | 211.0 | app2 | ok | 128 | 3140ms | 4701ms | 7867ms |
| 211.0 | 221.0 | app1 | ok | 35 | 972ms | 2191ms | 2469ms |
| 211.0 | 221.0 | app2 | ok | 155 | 3468ms | 4988ms | 9483ms |
| 221.0 | 231.0 | app1 | ok | 64 | 5556ms | 9111ms | 9911ms |
| 221.0 | 231.0 | app2 | ok | 134 | 2255ms | 4422ms | 4942ms |
| 231.0 | 241.0 | app1 | ok | 55 | 1750ms | 4141ms | 4914ms |
| 231.0 | 241.0 | app2 | ok | 182 | 3256ms | 4667ms | 4984ms |
| 241.0 | 251.0 | app1 | ok | 47 | 3352ms | 8583ms | 26867ms |
| 241.0 | 251.0 | app2 | ok | 42 | 3500ms | 4900ms | 9300ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 262.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 262.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -10.4%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2147580 | 106916 | 2250640.0 | -0.2% | 2130194.0 | 2361412.0 | -9.8% | True |
| app2 | 4227510 | 210950 | 4429407.0 | -0.2% | 4166562.0 | 4649410.0 | -10.4% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1915 | 0 | 0 | 0 (never shed) | 0.00% | 66.7% | 0.0% | 0.00 |
| app2 | 3769 | 0 | 2 | 2 | 0.05% | 33.3% | 100.0% | 3.00 |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5275, EvictedContextCancelled=100). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5275 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 253223 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
