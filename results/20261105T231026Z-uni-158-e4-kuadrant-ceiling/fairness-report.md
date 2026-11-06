# Fairness benchmark: full-contention (uni-158-e4-kuadrant-ceiling)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `360` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-d94zz` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-05T23:11:40Z` |
| Run end | `2026-11-05T23:18:07Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 790 | 200=780, 500=10 | 15.9 | 24.2 | 1032634.0 | 21.1% | 17.0% | -4.1 | 16.9% | -4.1 | 4.8s | 98.9% | 776.0 |
| app2 | 10.0 | 32 | 635 | 200=622, 500=13 | 24.6 | 27.4 | 810196.0 | 10.5% | 13.3% | 2.8 | 13.6% | 3.1 | 3.7s | 98.9% | 618.0 |
| end-users | 65.0 | 128 | 3246 | 200=3189, 500=57 | 15.7 | 19.4 | 4245118.0 | 68.4% | 69.7% | 1.3 | 69.5% | 1.1 | 4.2s | 98.9% | 3171.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 35114.0 | n/a | n/a | n/a | n/a | n/a | 0.1s | 98.9% | 26.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events (scheduled):**
- t+120s: live_set (target=field:tokenratelimitpolicies.kuadrant.io:maas-trlp-maas-vllm-gpu:spec.limits.models-as-a-service-app1-production-maas-vllm-gpu-tokens.rates, value=[{"limit":20000,"window":"1m"}])
- t+360s: live_restore (target=field:tokenratelimitpolicies.kuadrant.io:maas-trlp-maas-vllm-gpu:spec.limits.models-as-a-service-app1-production-maas-vllm-gpu-tokens.rates)

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

**Windows** (39 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 5386.0 | 21.1% | 18.1% | -2.9 |
| 0.0 | 10.0 | app2 | True | 4070.0 | 10.5% | 13.7% | 3.2 |
| 0.0 | 10.0 | end-users | True | 20246.0 | 68.4% | 68.2% | -0.3 |
| 10.0 | 20.0 | app1 | True | 32478.0 | 21.1% | 20.9% | -0.2 |
| 10.0 | 20.0 | app2 | True | 18944.0 | 10.5% | 12.2% | 1.7 |
| 10.0 | 20.0 | end-users | True | 104080.0 | 68.4% | 66.9% | -1.5 |
| 20.0 | 30.0 | app1 | True | 22978.0 | 21.1% | 13.5% | -7.6 |
| 20.0 | 30.0 | app2 | True | 43278.0 | 10.5% | 25.4% | 14.9 |
| 20.0 | 30.0 | end-users | True | 104242.0 | 68.4% | 61.1% | -7.3 |
| 30.0 | 40.0 | app1 | True | 25622.0 | 21.1% | 15.0% | -6.0 |
| 30.0 | 40.0 | app2 | True | 4036.0 | 10.5% | 2.4% | -8.2 |
| 30.0 | 40.0 | end-users | True | 140606.0 | 68.4% | 82.6% | 14.2 |
| 40.0 | 50.0 | app1 | True | 28440.0 | 21.1% | 18.6% | -2.5 |
| 40.0 | 50.0 | app2 | True | 14888.0 | 10.5% | 9.7% | -0.8 |
| 40.0 | 50.0 | end-users | True | 109584.0 | 68.4% | 71.7% | 3.2 |
| 50.0 | 60.0 | app1 | True | 40518.0 | 21.1% | 23.6% | 2.5 |
| 50.0 | 60.0 | app2 | True | 43292.0 | 10.5% | 25.2% | 14.7 |
| 50.0 | 60.0 | end-users | True | 87862.0 | 68.4% | 51.2% | -17.2 |
| 60.0 | 70.0 | app1 | True | 6742.0 | 21.1% | 4.0% | -17.1 |
| 60.0 | 70.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 60.0 | 70.0 | end-users | True | 163474.0 | 68.4% | 96.0% | 27.6 |
| 70.0 | 80.0 | app1 | True | 44598.0 | 21.1% | 26.0% | 4.9 |
| 70.0 | 80.0 | app2 | True | 59574.0 | 10.5% | 34.7% | 24.1 |
| 70.0 | 80.0 | end-users | True | 67648.0 | 68.4% | 39.4% | -29.0 |
| 80.0 | 90.0 | app1 | True | 36498.0 | 21.1% | 23.9% | 2.8 |
| 80.0 | 90.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 80.0 | 90.0 | end-users | True | 116230.0 | 68.4% | 76.1% | 7.7 |
| 90.0 | 100.0 | app1 | True | 1348.0 | 21.1% | 0.8% | -20.2 |
| 90.0 | 100.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 90.0 | 100.0 | end-users | True | 163642.0 | 68.4% | 99.2% | 30.8 |
| 100.0 | 110.0 | app1 | True | 51314.0 | 21.1% | 30.1% | 9.1 |
| 100.0 | 110.0 | app2 | True | 58124.0 | 10.5% | 34.1% | 23.6 |
| 100.0 | 110.0 | end-users | True | 60878.0 | 68.4% | 35.7% | -32.7 |
| 110.0 | 120.0 | app1 | True | 27104.0 | 21.1% | 16.2% | -4.9 |
| 110.0 | 120.0 | app2 | True | 1324.0 | 10.5% | 0.8% | -9.7 |
| 110.0 | 120.0 | end-users | True | 139132.0 | 68.4% | 83.0% | 14.6 |
| 120.0 | 130.0 | app1 | True | 6732.0 | 21.1% | 4.3% | -16.7 |
| 120.0 | 130.0 | app2 | True | 4062.0 | 10.5% | 2.6% | -7.9 |
| 120.0 | 130.0 | end-users | True | 144762.0 | 68.4% | 93.1% | 24.6 |
| 130.0 | 140.0 | app1 | True | 55378.0 | 21.1% | 33.3% | 12.3 |
| 130.0 | 140.0 | app2 | True | 54158.0 | 10.5% | 32.6% | 22.0 |
| 130.0 | 140.0 | end-users | True | 56724.0 | 68.4% | 34.1% | -34.3 |
| 140.0 | 150.0 | app1 | True | 13444.0 | 21.1% | 7.9% | -13.2 |
| 140.0 | 150.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 140.0 | 150.0 | end-users | True | 156704.0 | 68.4% | 92.1% | 23.7 |
| 150.0 | 160.0 | app1 | True | 40586.0 | 21.1% | 26.3% | 5.3 |
| 150.0 | 160.0 | app2 | True | 18996.0 | 10.5% | 12.3% | 1.8 |
| 150.0 | 160.0 | end-users | True | 94684.0 | 68.4% | 61.4% | -7.0 |
| 160.0 | 170.0 | app1 | True | 33790.0 | 21.1% | 20.0% | -1.1 |
| 160.0 | 170.0 | app2 | True | 39272.0 | 10.5% | 23.2% | 12.7 |
| 160.0 | 170.0 | end-users | True | 95968.0 | 68.4% | 56.8% | -11.6 |
| 170.0 | 180.0 | app1 | True | 4060.0 | 21.1% | 2.4% | -18.6 |
| 170.0 | 180.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 170.0 | 180.0 | end-users | True | 162334.0 | 68.4% | 96.8% | 28.3 |
| 180.0 | 190.0 | app1 | True | 47296.0 | 21.1% | 27.3% | 6.3 |
| 180.0 | 190.0 | app2 | True | 60824.0 | 10.5% | 35.2% | 24.6 |
| 180.0 | 190.0 | end-users | True | 64892.0 | 68.4% | 37.5% | -30.9 |
| 190.0 | 200.0 | app1 | True | 32440.0 | 21.1% | 21.6% | 0.6 |
| 190.0 | 200.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 190.0 | 200.0 | end-users | True | 117572.0 | 68.4% | 78.4% | 10.0 |
| 200.0 | 210.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 200.0 | 210.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 200.0 | 210.0 | end-users | True | 168966.0 | 68.4% | 100.0% | 31.6 |
| 210.0 | 220.0 | app1 | True | 43284.0 | 21.1% | 25.4% | 4.3 |
| 210.0 | 220.0 | app2 | True | 43256.0 | 10.5% | 25.4% | 14.9 |
| 210.0 | 220.0 | end-users | True | 83882.0 | 68.4% | 49.2% | -19.2 |
| 220.0 | 230.0 | app1 | True | 40626.0 | 21.1% | 24.6% | 3.6 |
| 220.0 | 230.0 | app2 | True | 24376.0 | 10.5% | 14.8% | 4.3 |
| 220.0 | 230.0 | end-users | True | 99904.0 | 68.4% | 60.6% | -7.8 |
| 230.0 | 240.0 | app1 | True | 27036.0 | 21.1% | 17.2% | -3.8 |
| 230.0 | 240.0 | app2 | True | 32438.0 | 10.5% | 20.7% | 10.1 |
| 230.0 | 240.0 | end-users | True | 97448.0 | 68.4% | 62.1% | -6.3 |
| 240.0 | 251.0 | app1 | True | 2716.0 | 21.1% | 1.6% | -19.4 |
| 240.0 | 251.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 240.0 | 251.0 | end-users | True | 164764.0 | 68.4% | 98.4% | 30.0 |
| 251.0 | 261.0 | app1 | True | 44606.0 | 21.1% | 27.5% | 6.4 |
| 251.0 | 261.0 | app2 | True | 59576.0 | 10.5% | 36.7% | 26.2 |
| 251.0 | 261.0 | end-users | True | 58122.0 | 68.4% | 35.8% | -32.6 |
| 261.0 | 271.0 | app1 | True | 35188.0 | 21.1% | 22.4% | 1.4 |
| 261.0 | 271.0 | app2 | True | 1348.0 | 10.5% | 0.9% | -9.7 |
| 261.0 | 271.0 | end-users | True | 120282.0 | 68.4% | 76.7% | 8.3 |
| 271.0 | 281.0 | app1 | True | 1332.0 | 21.1% | 0.8% | -20.3 |
| 271.0 | 281.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 271.0 | 281.0 | end-users | True | 167712.0 | 68.4% | 99.2% | 30.8 |
| 281.0 | 291.0 | app1 | True | 54022.0 | 21.1% | 32.3% | 11.2 |
| 281.0 | 291.0 | app2 | True | 58122.0 | 10.5% | 34.7% | 24.2 |
| 281.0 | 291.0 | end-users | True | 55340.0 | 68.4% | 33.0% | -35.4 |
| 291.0 | 301.0 | app1 | True | 27050.0 | 21.1% | 16.7% | -4.4 |
| 291.0 | 301.0 | app2 | True | 2706.0 | 10.5% | 1.7% | -8.9 |
| 291.0 | 301.0 | end-users | True | 132574.0 | 68.4% | 81.7% | 13.2 |
| 301.0 | 311.0 | app1 | True | 5404.0 | 21.1% | 3.4% | -17.6 |
| 301.0 | 311.0 | app2 | True | 1324.0 | 10.5% | 0.8% | -9.7 |
| 301.0 | 311.0 | end-users | True | 149988.0 | 68.4% | 95.7% | 27.3 |
| 311.0 | 321.0 | app1 | True | 55442.0 | 21.1% | 32.3% | 11.2 |
| 311.0 | 321.0 | app2 | True | 58168.0 | 10.5% | 33.9% | 23.3 |
| 311.0 | 321.0 | end-users | True | 58184.0 | 68.4% | 33.9% | -34.6 |
| 321.0 | 331.0 | app1 | True | 14844.0 | 21.1% | 8.9% | -12.1 |
| 321.0 | 331.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 321.0 | 331.0 | end-users | True | 151480.0 | 68.4% | 91.1% | 22.7 |
| 331.0 | 341.0 | app1 | True | 39116.0 | 21.1% | 25.0% | 3.9 |
| 331.0 | 341.0 | app2 | True | 20310.0 | 10.5% | 13.0% | 2.4 |
| 331.0 | 341.0 | end-users | True | 97338.0 | 68.4% | 62.1% | -6.3 |
| 341.0 | 351.0 | app1 | True | 32376.0 | 21.1% | 19.3% | -1.7 |
| 341.0 | 351.0 | app2 | True | 40530.0 | 10.5% | 24.2% | 13.7 |
| 341.0 | 351.0 | end-users | True | 94646.0 | 68.4% | 56.5% | -11.9 |
| 351.0 | 361.0 | app1 | True | 9484.0 | 21.1% | 5.6% | -15.5 |
| 351.0 | 361.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 351.0 | 361.0 | end-users | True | 161000.0 | 68.4% | 94.4% | 26.0 |
| 361.0 | 371.0 | app1 | False | 43356.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | 41842.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | False | 82530.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | False | 129694.0 | n/a | n/a | n/a |
| 381.0 | 387.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 387.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 387.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 959400 | 47413 | 1001648.0 | -0.5% | 1032634.0 | 1054226.0 | -2.0% | True |
| app2 | 765060 | 38105 | 798016.0 | -0.6% | 810196.0 | 841270.0 | -3.7% | True |
| end-users | 3922470 | 194386 | 4093623.0 | -0.6% | 4245118.0 | 4311242.0 | -1.5% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 790 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 635 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3246 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=4591). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 373691 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
