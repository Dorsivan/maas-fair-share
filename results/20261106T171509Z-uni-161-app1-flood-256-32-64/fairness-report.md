# Fairness benchmark: app1-flood (uni-161-app1-flood-256-32-64)

**Verdict: FAIL** (threshold: 10 points)

- end-users deviated -32.4 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-flood` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-796bc55c4b-75gt8` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-06T17:16:21Z` |
| Run end | `2026-11-06T17:21:05Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 30.0 | 256 | 2067 | 200=2031, 500=36 | 32.9 | 40.1 | 2699926.0 | 30.0% | 61.6% | 31.6 | 61.8% | 31.8 | 18.1s | 98.9% | 2031.0 |
| app2 | 10.0 | 32 | 359 | 200=353, 500=6 | 25.5 | 30.5 | 473106.0 | 10.0% | 10.8% | 0.8 | 10.7% | 0.7 | 16.8s | 98.9% | 353.0 |
| end-users | 60.0 | 64 | 917 | 200=904, 500=13 | 20.6 | 26.1 | 1209660.0 | 60.0% | 27.6% | -32.4 | 27.4% | -32.6 | 17.6s | 98.9% | 903.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 1352.0 | n/a | n/a | n/a | n/a | n/a | 0.0s | 98.9% | 1.0 |

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

**Windows** (29 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 49976.0 | 30.0% | 71.2% | 41.2 |
| 0.0 | 10.0 | app2 | True | 8100.0 | 10.0% | 11.5% | 1.5 |
| 0.0 | 10.0 | end-users | True | 12116.0 | 60.0% | 17.3% | -42.7 |
| 10.0 | 20.0 | app1 | True | 147138.0 | 30.0% | 79.5% | 49.5 |
| 10.0 | 20.0 | app2 | True | 10846.0 | 10.0% | 5.9% | -4.1 |
| 10.0 | 20.0 | end-users | True | 27016.0 | 60.0% | 14.6% | -45.4 |
| 20.0 | 30.0 | app1 | True | 47318.0 | 30.0% | 31.3% | 1.3 |
| 20.0 | 30.0 | app2 | True | 17526.0 | 10.0% | 11.6% | 1.6 |
| 20.0 | 30.0 | end-users | True | 86566.0 | 60.0% | 57.2% | -2.8 |
| 30.0 | 40.0 | app1 | True | 143068.0 | 30.0% | 84.8% | 54.8 |
| 30.0 | 40.0 | app2 | True | 25726.0 | 10.0% | 15.2% | 5.2 |
| 30.0 | 40.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 40.0 | 50.0 | app1 | True | 62220.0 | 30.0% | 40.0% | 10.0 |
| 40.0 | 50.0 | app2 | True | 13472.0 | 10.0% | 8.7% | -1.3 |
| 40.0 | 50.0 | end-users | True | 79824.0 | 60.0% | 51.3% | -8.7 |
| 50.0 | 60.0 | app1 | True | 94716.0 | 30.0% | 56.0% | 26.0 |
| 50.0 | 60.0 | app2 | True | 28344.0 | 10.0% | 16.8% | 6.8 |
| 50.0 | 60.0 | end-users | True | 45992.0 | 60.0% | 27.2% | -32.8 |
| 60.0 | 70.0 | app1 | True | 98526.0 | 30.0% | 57.0% | 27.0 |
| 60.0 | 70.0 | app2 | True | 32430.0 | 10.0% | 18.8% | 8.8 |
| 60.0 | 70.0 | end-users | True | 41932.0 | 60.0% | 24.3% | -35.7 |
| 70.0 | 80.0 | app1 | True | 64940.0 | 30.0% | 42.5% | 12.5 |
| 70.0 | 80.0 | app2 | True | 16246.0 | 10.0% | 10.6% | 0.6 |
| 70.0 | 80.0 | end-users | True | 71644.0 | 60.0% | 46.9% | -13.1 |
| 80.0 | 90.0 | app1 | True | 155426.0 | 30.0% | 91.3% | 61.3 |
| 80.0 | 90.0 | app2 | True | 4032.0 | 10.0% | 2.4% | -7.6 |
| 80.0 | 90.0 | end-users | True | 10830.0 | 60.0% | 6.4% | -53.6 |
| 90.0 | 100.0 | app1 | True | 64970.0 | 30.0% | 37.8% | 7.8 |
| 90.0 | 100.0 | app2 | True | 14924.0 | 10.0% | 8.7% | -1.3 |
| 90.0 | 100.0 | end-users | True | 91840.0 | 60.0% | 53.5% | -6.5 |
| 100.0 | 110.0 | app1 | True | 91934.0 | 30.0% | 56.2% | 26.2 |
| 100.0 | 110.0 | app2 | True | 29686.0 | 10.0% | 18.2% | 8.2 |
| 100.0 | 110.0 | end-users | True | 41926.0 | 60.0% | 25.6% | -34.4 |
| 110.0 | 120.0 | app1 | True | 101268.0 | 30.0% | 63.5% | 33.5 |
| 110.0 | 120.0 | app2 | True | 35176.0 | 10.0% | 22.1% | 12.1 |
| 110.0 | 120.0 | end-users | True | 22936.0 | 60.0% | 14.4% | -45.6 |
| 120.0 | 130.0 | app1 | True | 67586.0 | 30.0% | 39.1% | 9.1 |
| 120.0 | 130.0 | app2 | True | 1358.0 | 10.0% | 0.8% | -9.2 |
| 120.0 | 130.0 | end-users | True | 103990.0 | 60.0% | 60.1% | 0.1 |
| 130.0 | 140.0 | app1 | True | 135196.0 | 30.0% | 78.8% | 48.8 |
| 130.0 | 140.0 | app2 | True | 18902.0 | 10.0% | 11.0% | 1.0 |
| 130.0 | 140.0 | end-users | True | 17562.0 | 60.0% | 10.2% | -49.8 |
| 140.0 | 150.0 | app1 | True | 87906.0 | 30.0% | 58.0% | 28.0 |
| 140.0 | 150.0 | app2 | True | 29778.0 | 10.0% | 19.7% | 9.7 |
| 140.0 | 150.0 | end-users | True | 33760.0 | 60.0% | 22.3% | -37.7 |
| 150.0 | 160.0 | app1 | True | 79690.0 | 30.0% | 46.1% | 16.1 |
| 150.0 | 160.0 | app2 | True | 1358.0 | 10.0% | 0.8% | -9.2 |
| 150.0 | 160.0 | end-users | True | 91868.0 | 60.0% | 53.1% | -6.9 |
| 160.0 | 170.0 | app1 | True | 140534.0 | 30.0% | 83.2% | 53.2 |
| 160.0 | 170.0 | app2 | True | 28370.0 | 10.0% | 16.8% | 6.8 |
| 160.0 | 170.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 170.0 | 180.0 | app1 | True | 94462.0 | 30.0% | 55.5% | 25.5 |
| 170.0 | 180.0 | app2 | True | 20294.0 | 10.0% | 11.9% | 1.9 |
| 170.0 | 180.0 | end-users | True | 55504.0 | 60.0% | 32.6% | -27.4 |
| 180.0 | 190.0 | app1 | True | 86484.0 | 30.0% | 56.7% | 26.7 |
| 180.0 | 190.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 180.0 | 190.0 | end-users | True | 66170.0 | 60.0% | 43.3% | -16.7 |
| 190.0 | 200.0 | app1 | True | 135116.0 | 30.0% | 78.1% | 48.1 |
| 190.0 | 200.0 | app2 | True | 36442.0 | 10.0% | 21.1% | 11.1 |
| 190.0 | 200.0 | end-users | True | 1358.0 | 60.0% | 0.8% | -59.2 |
| 200.0 | 210.0 | app1 | True | 90562.0 | 30.0% | 52.8% | 22.8 |
| 200.0 | 210.0 | app2 | True | 12154.0 | 10.0% | 7.1% | -2.9 |
| 200.0 | 210.0 | end-users | True | 68752.0 | 60.0% | 40.1% | -19.9 |
| 210.0 | 220.0 | app1 | True | 116202.0 | 30.0% | 70.4% | 40.4 |
| 210.0 | 220.0 | app2 | True | 4072.0 | 10.0% | 2.5% | -7.5 |
| 210.0 | 220.0 | end-users | True | 44676.0 | 60.0% | 27.1% | -32.9 |
| 220.0 | 230.0 | app1 | True | 121640.0 | 30.0% | 76.3% | 46.3 |
| 220.0 | 230.0 | app2 | True | 37852.0 | 10.0% | 23.7% | 13.7 |
| 220.0 | 230.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 230.0 | 240.0 | app1 | True | 70130.0 | 30.0% | 40.9% | 10.9 |
| 230.0 | 240.0 | app2 | True | 2716.0 | 10.0% | 1.6% | -8.4 |
| 230.0 | 240.0 | end-users | True | 98708.0 | 60.0% | 57.5% | -2.5 |
| 240.0 | 250.0 | app1 | False | 136538.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 8110.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 21714.0 | n/a | n/a | n/a |
| 250.0 | 261.0 | app1 | False | 116366.0 | n/a | n/a | n/a |
| 250.0 | 261.0 | app2 | False | 35192.0 | n/a | n/a | n/a |
| 250.0 | 261.0 | end-users | False | 1358.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 97298.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 71618.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 2716.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 284.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 284.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 284.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2498130 | 123172 | 2621302.0 | 0.0% | 2699926.0 | 2744474.0 | -1.6% | True |
| app2 | 434190 | 21490 | 455680.0 | 0.0% | 473106.0 | 477170.0 | -0.9% | True |
| end-users | 1111920 | 54961 | 1165590.0 | -0.1% | 1209660.0 | 1221842.0 | -1.0% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2067 | 0 | 0 | 0 (never shed) | 0.00% | 30.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 359 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 917 | 0 | 0 | 0 (never shed) | 0.00% | 60.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=3288). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 272421 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
