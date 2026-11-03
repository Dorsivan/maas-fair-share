# Fairness benchmark: full-contention (uni-154-d1-many-end-user-keys)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-8rxnq` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-03T11:26:08Z` |
| Run end | `2026-11-03T11:30:30Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 571 | 200=556, 500=15 | 13.1 | 23.2 | 727468.0 | 21.1% | 17.6% | -3.4 | 17.5% | -3.6 | 3.7s | 98.9% | 553.0 |
| app2 | 10.0 | 32 | 468 | 200=444, 500=24 | 21.6 | 27.4 | 574740.0 | 10.5% | 13.9% | 3.4 | 14.3% | 3.8 | 2.9s | 98.9% | 440.0 |
| end-users | 65.0 | 128 | 2233 | 200=2158, 500=75 | 13.7 | 19.4 | 2824554.0 | 68.4% | 68.4% | 0.0 | 68.2% | -0.2 | 3.3s | 98.9% | 2146.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 25650.0 | n/a | n/a | n/a | n/a | n/a | 0.0s | 98.9% | 19.0 |

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
| 0.0 | 10.0 | app1 | True | 14910.0 | 21.1% | 18.7% | -2.4 |
| 0.0 | 10.0 | app2 | True | 16142.0 | 10.5% | 20.2% | 9.7 |
| 0.0 | 10.0 | end-users | True | 48724.0 | 68.4% | 61.1% | -7.3 |
| 10.0 | 20.0 | app1 | True | 24340.0 | 21.1% | 14.3% | -6.8 |
| 10.0 | 20.0 | app2 | True | 18962.0 | 10.5% | 11.1% | 0.6 |
| 10.0 | 20.0 | end-users | True | 127098.0 | 68.4% | 74.6% | 6.2 |
| 20.0 | 30.0 | app1 | True | 35144.0 | 21.1% | 20.6% | -0.4 |
| 20.0 | 30.0 | app2 | True | 17608.0 | 10.5% | 10.3% | -0.2 |
| 20.0 | 30.0 | end-users | True | 117638.0 | 68.4% | 69.0% | 0.6 |
| 30.0 | 40.0 | app1 | True | 24392.0 | 21.1% | 15.0% | -6.0 |
| 30.0 | 40.0 | app2 | True | 29746.0 | 10.5% | 18.3% | 7.8 |
| 30.0 | 40.0 | end-users | True | 108254.0 | 68.4% | 66.7% | -1.8 |
| 40.0 | 50.0 | app1 | True | 29718.0 | 21.1% | 19.1% | -1.9 |
| 40.0 | 50.0 | app2 | True | 28398.0 | 10.5% | 18.3% | 7.7 |
| 40.0 | 50.0 | end-users | True | 97384.0 | 68.4% | 62.6% | -5.8 |
| 50.0 | 60.0 | app1 | True | 13542.0 | 21.1% | 8.0% | -13.0 |
| 50.0 | 60.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 50.0 | 60.0 | end-users | True | 155490.0 | 68.4% | 92.0% | 23.6 |
| 60.0 | 70.0 | app1 | True | 45994.0 | 21.1% | 27.0% | 5.9 |
| 60.0 | 70.0 | app2 | True | 60858.0 | 10.5% | 35.7% | 25.2 |
| 60.0 | 70.0 | end-users | True | 63574.0 | 68.4% | 37.3% | -31.1 |
| 70.0 | 80.0 | app1 | True | 35108.0 | 21.1% | 23.2% | 2.2 |
| 70.0 | 80.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 70.0 | 80.0 | end-users | True | 116128.0 | 68.4% | 76.8% | 8.4 |
| 80.0 | 90.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 80.0 | 90.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 80.0 | 90.0 | end-users | True | 171752.0 | 68.4% | 100.0% | 31.6 |
| 90.0 | 100.0 | app1 | True | 58192.0 | 21.1% | 34.1% | 13.1 |
| 90.0 | 100.0 | app2 | True | 59488.0 | 10.5% | 34.9% | 24.4 |
| 90.0 | 100.0 | end-users | True | 52746.0 | 68.4% | 30.9% | -37.5 |
| 100.0 | 110.0 | app1 | True | 21606.0 | 21.1% | 13.0% | -8.1 |
| 100.0 | 110.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 100.0 | 110.0 | end-users | True | 144782.0 | 68.4% | 87.0% | 18.6 |
| 110.0 | 120.0 | app1 | True | 16228.0 | 21.1% | 10.7% | -10.4 |
| 110.0 | 120.0 | app2 | True | 6780.0 | 10.5% | 4.5% | -6.1 |
| 110.0 | 120.0 | end-users | True | 128654.0 | 68.4% | 84.8% | 16.4 |
| 120.0 | 130.0 | app1 | True | 48682.0 | 21.1% | 29.3% | 8.2 |
| 120.0 | 130.0 | app2 | True | 51404.0 | 10.5% | 30.9% | 20.4 |
| 120.0 | 130.0 | end-users | True | 66314.0 | 68.4% | 39.9% | -28.6 |
| 130.0 | 140.0 | app1 | True | 12144.0 | 21.1% | 7.0% | -14.0 |
| 130.0 | 140.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 130.0 | 140.0 | end-users | True | 160988.0 | 68.4% | 93.0% | 24.6 |
| 140.0 | 150.0 | app1 | True | 43226.0 | 21.1% | 26.6% | 5.6 |
| 140.0 | 150.0 | app2 | True | 33800.0 | 10.5% | 20.8% | 10.3 |
| 140.0 | 150.0 | end-users | True | 85314.0 | 68.4% | 52.6% | -15.9 |
| 150.0 | 160.0 | app1 | True | 32466.0 | 21.1% | 20.3% | -0.7 |
| 150.0 | 160.0 | app2 | True | 24374.0 | 10.5% | 15.3% | 4.7 |
| 150.0 | 160.0 | end-users | True | 102798.0 | 68.4% | 64.4% | -4.0 |
| 160.0 | 170.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.2 |
| 160.0 | 170.0 | app2 | True | 1356.0 | 10.5% | 0.8% | -9.7 |
| 160.0 | 170.0 | end-users | True | 159568.0 | 68.4% | 98.3% | 29.9 |
| 170.0 | 180.0 | app1 | True | 47300.0 | 21.1% | 27.5% | 6.5 |
| 170.0 | 180.0 | app2 | True | 59576.0 | 10.5% | 34.7% | 24.1 |
| 170.0 | 180.0 | end-users | True | 64934.0 | 68.4% | 37.8% | -30.6 |
| 180.0 | 190.0 | app1 | True | 31026.0 | 21.1% | 20.3% | -0.8 |
| 180.0 | 190.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 180.0 | 190.0 | end-users | True | 121840.0 | 68.4% | 79.7% | 11.3 |
| 190.0 | 200.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 190.0 | 200.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 190.0 | 200.0 | end-users | True | 169072.0 | 68.4% | 100.0% | 31.6 |
| 200.0 | 210.0 | app1 | True | 55450.0 | 21.1% | 33.1% | 12.0 |
| 200.0 | 210.0 | app2 | True | 63482.0 | 10.5% | 37.9% | 27.3 |
| 200.0 | 210.0 | end-users | True | 48744.0 | 68.4% | 29.1% | -39.4 |
| 210.0 | 220.0 | app1 | True | 29764.0 | 21.1% | 18.0% | -3.0 |
| 210.0 | 220.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 210.0 | 220.0 | end-users | True | 135230.0 | 68.4% | 82.0% | 13.5 |
| 220.0 | 230.0 | app1 | True | 9500.0 | 21.1% | 6.1% | -15.0 |
| 220.0 | 230.0 | app2 | True | 6778.0 | 10.5% | 4.3% | -6.2 |
| 220.0 | 230.0 | end-users | True | 140648.0 | 68.4% | 89.6% | 21.2 |
| 230.0 | 240.0 | app1 | True | 52762.0 | 21.1% | 31.5% | 10.4 |
| 230.0 | 240.0 | app2 | True | 52672.0 | 10.5% | 31.4% | 20.9 |
| 230.0 | 240.0 | end-users | True | 62228.0 | 68.4% | 37.1% | -31.3 |
| 240.0 | 250.0 | app1 | False | 16202.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 151620.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 28414.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 43316.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 23032.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 683880 | 33962 | 713982.0 | -0.5% | 727468.0 | 751804.0 | -3.2% | True |
| app2 | 546120 | 27186 | 568130.0 | -0.9% | 574740.0 | 600492.0 | -4.3% | True |
| end-users | 2654340 | 132467 | 2771333.0 | -0.6% | 2824554.0 | 2919274.0 | -3.2% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 571 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 468 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2233 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

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
