# Fairness benchmark: full-contention (uni-162-f2-clamp-off-cold-join)

**Verdict: FAIL** (threshold: 10 points)

- end-users deviated -33.8 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5859d5b679-blf4c` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-06T19:38:30Z` |
| Run end | `2026-11-06T19:42:52Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 404 | 200=394, 500=10 | 14.4 | 74.1 | 1365234.0 | 21.1% | 32.2% | 11.2 | 24.7% | 3.7 | 7.5s | 98.9% | 981.0 |
| app2 | 10.0 | 32 | 69 | 200=58, 500=11 | 29.4 | 249.0 | 1403484.0 | 10.5% | 33.1% | 22.6 | 4.2% | -6.3 | 7.5s | 98.9% | 1022.0 |
| end-users | 65.0 | 128 | 1160 | 200=1095, 500=65 | 13.8 | 18.6 | 1467304.0 | 68.4% | 34.6% | -33.8 | 71.0% | 2.6 | 1.1s | 98.9% | 1095.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- end-users: active 120s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 120.0 | 210.0 | 90.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 112132.0 | 66.7% | 66.9% | 0.2 |
| 0.0 | 10.0 | app2 | True | 55498.0 | 33.3% | 33.1% | -0.2 |
| 0.0 | 10.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | True | 110874.0 | 66.7% | 66.1% | -0.5 |
| 10.0 | 20.0 | app2 | True | 56774.0 | 33.3% | 33.9% | 0.5 |
| 10.0 | 20.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | True | 108178.0 | 66.7% | 67.2% | 0.6 |
| 20.0 | 30.0 | app2 | True | 52722.0 | 33.3% | 32.8% | -0.6 |
| 20.0 | 30.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | True | 109424.0 | 66.7% | 66.9% | 0.2 |
| 30.0 | 40.0 | app2 | True | 54106.0 | 33.3% | 33.1% | -0.2 |
| 30.0 | 40.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | True | 112218.0 | 66.7% | 66.4% | -0.3 |
| 40.0 | 50.0 | app2 | True | 56854.0 | 33.3% | 33.6% | 0.3 |
| 40.0 | 50.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | True | 113426.0 | 66.7% | 66.1% | -0.5 |
| 50.0 | 60.0 | app2 | True | 58046.0 | 33.3% | 33.9% | 0.5 |
| 50.0 | 60.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | True | 112248.0 | 66.7% | 66.9% | 0.3 |
| 60.0 | 70.0 | app2 | True | 55452.0 | 33.3% | 33.1% | -0.3 |
| 60.0 | 70.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | True | 101386.0 | 66.7% | 65.2% | -1.5 |
| 70.0 | 80.0 | app2 | True | 54118.0 | 33.3% | 34.8% | 1.5 |
| 70.0 | 80.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | True | 41878.0 | 66.7% | 25.0% | -41.7 |
| 80.0 | 90.0 | app2 | True | 125756.0 | 33.3% | 75.0% | 41.7 |
| 80.0 | 90.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app1 | True | 41916.0 | 66.7% | 25.0% | -41.7 |
| 90.0 | 100.0 | app2 | True | 125746.0 | 33.3% | 75.0% | 41.7 |
| 90.0 | 100.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 100.0 | 110.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 100.0 | 110.0 | app2 | True | 151568.0 | 33.3% | 100.0% | 66.7 |
| 100.0 | 110.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app1 | True | 42000.0 | 66.7% | 24.9% | -41.8 |
| 110.0 | 120.0 | app2 | True | 126936.0 | 33.3% | 75.1% | 41.8 |
| 110.0 | 120.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | True | 39192.0 | 21.1% | 23.4% | 2.3 |
| 120.0 | 130.0 | app2 | True | 74336.0 | 10.5% | 44.3% | 33.8 |
| 120.0 | 130.0 | end-users | True | 54178.0 | 68.4% | 32.3% | -36.1 |
| 130.0 | 140.0 | app1 | True | 4038.0 | 21.1% | 2.5% | -18.6 |
| 130.0 | 140.0 | app2 | True | 127248.0 | 10.5% | 77.7% | 67.2 |
| 130.0 | 140.0 | end-users | True | 32484.0 | 68.4% | 19.8% | -48.6 |
| 140.0 | 150.0 | app1 | True | 10790.0 | 21.1% | 6.8% | -14.2 |
| 140.0 | 150.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 140.0 | 150.0 | end-users | True | 147314.0 | 68.4% | 93.2% | 24.8 |
| 150.0 | 160.0 | app1 | True | 32482.0 | 21.1% | 19.7% | -1.4 |
| 150.0 | 160.0 | app2 | True | 14886.0 | 10.5% | 9.0% | -1.5 |
| 150.0 | 160.0 | end-users | True | 117740.0 | 68.4% | 71.3% | 2.9 |
| 160.0 | 170.0 | app1 | True | 36456.0 | 21.1% | 21.9% | 0.9 |
| 160.0 | 170.0 | app2 | True | 10838.0 | 10.5% | 6.5% | -4.0 |
| 160.0 | 170.0 | end-users | True | 119030.0 | 68.4% | 71.6% | 3.1 |
| 170.0 | 180.0 | app1 | True | 35148.0 | 21.1% | 22.2% | 1.2 |
| 170.0 | 180.0 | app2 | True | 16166.0 | 10.5% | 10.2% | -0.3 |
| 170.0 | 180.0 | end-users | True | 106822.0 | 68.4% | 67.6% | -0.9 |
| 180.0 | 190.0 | app1 | True | 2680.0 | 21.1% | 1.6% | -19.5 |
| 180.0 | 190.0 | app2 | True | 70248.0 | 10.5% | 41.6% | 31.1 |
| 180.0 | 190.0 | end-users | True | 96032.0 | 68.4% | 56.8% | -11.6 |
| 190.0 | 200.0 | app1 | True | 40594.0 | 21.1% | 24.8% | 3.7 |
| 190.0 | 200.0 | app2 | True | 25686.0 | 10.5% | 15.7% | 5.2 |
| 190.0 | 200.0 | end-users | True | 97498.0 | 68.4% | 59.5% | -8.9 |
| 200.0 | 210.0 | app1 | True | 6748.0 | 21.1% | 4.3% | -16.8 |
| 200.0 | 210.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 200.0 | 210.0 | end-users | True | 150088.0 | 68.4% | 95.7% | 27.3 |
| 210.0 | 220.0 | app1 | True | 36558.0 | 21.1% | 21.8% | 0.8 |
| 210.0 | 220.0 | app2 | True | 12126.0 | 10.5% | 7.2% | -3.3 |
| 210.0 | 220.0 | end-users | True | 118980.0 | 68.4% | 71.0% | 2.5 |
| 220.0 | 230.0 | app1 | True | 32490.0 | 21.1% | 18.8% | -2.3 |
| 220.0 | 230.0 | app2 | True | 18892.0 | 10.5% | 10.9% | 0.4 |
| 220.0 | 230.0 | end-users | True | 121580.0 | 68.4% | 70.3% | 1.9 |
| 230.0 | 240.0 | app1 | True | 39158.0 | 21.1% | 23.9% | 2.9 |
| 230.0 | 240.0 | app2 | True | 12206.0 | 10.5% | 7.5% | -3.1 |
| 230.0 | 240.0 | end-users | True | 112146.0 | 68.4% | 68.6% | 0.2 |
| 240.0 | 250.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 4074.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 154214.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 43220.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 43202.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 39198.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens +157.1%, cost +156.3%
- app2 exceeded the 10% ledger tolerance: raw tokens +1690.2%, cost +1690.8%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 484620 | 24043 | 1307641.0 | 157.1% | 1365234.0 | 532706.0 | 156.3% | False |
| app2 | 71340 | 3517 | 1340112.0 | 1690.2% | 1403484.0 | 78374.0 | 1690.8% | False |
| end-users | 1346850 | 66961 | 1413811.0 | 0.0% | 1467304.0 | 1480772.0 | -0.9% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 404 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 69 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1160 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 309 requests refused by the EPP (Dispatched=3098, EvictedTTL=309). Client saw 0 x 429; at most 309 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 249861 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
