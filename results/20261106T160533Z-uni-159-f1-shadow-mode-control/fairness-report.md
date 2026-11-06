# Fairness benchmark: shadow-mode-control (uni-159-f1-shadow-mode-control)

**Verdict: INFO** -- named negative control, not scored against the 10-point threshold. Expected to NOT reproduce the configured weights; see docs/runbook.md.

- negative control, not scored against the 10-point threshold: max deviation was 6.1 points. This scenario is expected to compress toward equal shares, not reproduce the configured weights -- see docs/runbook.md's 'Per-tenant worker sizing and the saturation check'

## Run metadata

| field | value |
|---|---|
| Scenario | `shadow-mode-control` |
| Generator | `closed-loop` |
| Enforce | `False` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-575669c495-gr7bq` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-06T16:06:45Z` |
| Run end | `2026-11-06T16:11:07Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 535 | 200=526, 500=9 | 15.7 | 16.1 | 704146.0 | 21.1% | 16.9% | -4.1 | 16.8% | -4.2 | 15.1s | 98.9% | 526.0 |
| app2 | 10.0 | 32 | 530 | 200=520, 500=10 | 15.7 | 16.1 | 693554.0 | 10.5% | 16.7% | 6.1 | 16.7% | 6.1 | 15.1s | 98.9% | 517.0 |
| end-users | 65.0 | 128 | 2115 | 200=2074, 500=41 | 15.7 | 16.1 | 2762276.0 | 68.4% | 66.4% | -2.0 | 66.5% | -1.9 | 15.1s | 98.9% | 2066.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 14876.0 | n/a | n/a | n/a | n/a | n/a | 0.1s | 98.9% | 11.0 |

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
| 0.0 | 0.0 | 0.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 14796.0 | 21.1% | 24.9% | 3.8 |
| 0.0 | 10.0 | app2 | True | 8138.0 | 10.5% | 13.7% | 3.2 |
| 0.0 | 10.0 | end-users | True | 36516.0 | 68.4% | 61.4% | -7.0 |
| 10.0 | 20.0 | app1 | True | 27018.0 | 21.1% | 16.9% | -4.1 |
| 10.0 | 20.0 | app2 | True | 25670.0 | 10.5% | 16.1% | 5.6 |
| 10.0 | 20.0 | end-users | True | 106856.0 | 68.4% | 67.0% | -1.4 |
| 20.0 | 30.0 | app1 | True | 27050.0 | 21.1% | 16.0% | -5.0 |
| 20.0 | 30.0 | app2 | True | 28404.0 | 10.5% | 16.8% | 6.3 |
| 20.0 | 30.0 | end-users | True | 113534.0 | 68.4% | 67.2% | -1.2 |
| 30.0 | 40.0 | app1 | True | 31066.0 | 21.1% | 18.1% | -3.0 |
| 30.0 | 40.0 | app2 | True | 29772.0 | 10.5% | 17.3% | 6.8 |
| 30.0 | 40.0 | end-users | True | 110898.0 | 68.4% | 64.6% | -3.8 |
| 40.0 | 50.0 | app1 | True | 22942.0 | 21.1% | 14.9% | -6.2 |
| 40.0 | 50.0 | app2 | True | 22998.0 | 10.5% | 14.9% | 4.4 |
| 40.0 | 50.0 | end-users | True | 108188.0 | 68.4% | 70.2% | 1.8 |
| 50.0 | 60.0 | app1 | True | 31020.0 | 21.1% | 18.4% | -2.7 |
| 50.0 | 60.0 | app2 | True | 31164.0 | 10.5% | 18.4% | 7.9 |
| 50.0 | 60.0 | end-users | True | 106842.0 | 68.4% | 63.2% | -5.2 |
| 60.0 | 70.0 | app1 | True | 31134.0 | 21.1% | 18.1% | -2.9 |
| 60.0 | 70.0 | app2 | True | 29794.0 | 10.5% | 17.3% | 6.8 |
| 60.0 | 70.0 | end-users | True | 110924.0 | 68.4% | 64.5% | -3.9 |
| 70.0 | 80.0 | app1 | True | 22986.0 | 21.1% | 13.4% | -7.7 |
| 70.0 | 80.0 | app2 | True | 22886.0 | 10.5% | 13.3% | 2.8 |
| 70.0 | 80.0 | end-users | True | 125794.0 | 68.4% | 73.3% | 4.9 |
| 80.0 | 90.0 | app1 | True | 28364.0 | 21.1% | 18.9% | -2.2 |
| 80.0 | 90.0 | app2 | True | 27122.0 | 10.5% | 18.1% | 7.5 |
| 80.0 | 90.0 | end-users | True | 94618.0 | 68.4% | 63.0% | -5.4 |
| 90.0 | 100.0 | app1 | True | 25688.0 | 21.1% | 15.4% | -5.6 |
| 90.0 | 100.0 | app2 | True | 28478.0 | 10.5% | 17.1% | 6.6 |
| 90.0 | 100.0 | end-users | True | 112210.0 | 68.4% | 67.4% | -1.0 |
| 100.0 | 110.0 | app1 | True | 24286.0 | 21.1% | 14.3% | -6.8 |
| 100.0 | 110.0 | app2 | True | 28388.0 | 10.5% | 16.7% | 6.1 |
| 100.0 | 110.0 | end-users | True | 117558.0 | 68.4% | 69.1% | 0.6 |
| 110.0 | 120.0 | app1 | True | 31098.0 | 21.1% | 20.2% | -0.9 |
| 110.0 | 120.0 | app2 | True | 24320.0 | 10.5% | 15.8% | 5.3 |
| 110.0 | 120.0 | end-users | True | 98730.0 | 68.4% | 64.0% | -4.4 |
| 120.0 | 130.0 | app1 | True | 27064.0 | 21.1% | 16.0% | -5.0 |
| 120.0 | 130.0 | app2 | True | 28384.0 | 10.5% | 16.8% | 6.3 |
| 120.0 | 130.0 | end-users | True | 113538.0 | 68.4% | 67.2% | -1.2 |
| 130.0 | 140.0 | app1 | True | 27002.0 | 21.1% | 15.4% | -5.7 |
| 130.0 | 140.0 | app2 | True | 28354.0 | 10.5% | 16.1% | 5.6 |
| 130.0 | 140.0 | end-users | True | 120300.0 | 68.4% | 68.5% | 0.1 |
| 140.0 | 150.0 | app1 | True | 32514.0 | 21.1% | 19.1% | -2.0 |
| 140.0 | 150.0 | app2 | True | 29770.0 | 10.5% | 17.5% | 6.9 |
| 140.0 | 150.0 | end-users | True | 108130.0 | 68.4% | 63.5% | -5.0 |
| 150.0 | 160.0 | app1 | True | 21614.0 | 21.1% | 14.4% | -6.6 |
| 150.0 | 160.0 | app2 | True | 24316.0 | 10.5% | 16.2% | 5.7 |
| 150.0 | 160.0 | end-users | True | 104026.0 | 68.4% | 69.4% | 0.9 |
| 160.0 | 170.0 | app1 | True | 31078.0 | 21.1% | 18.0% | -3.1 |
| 160.0 | 170.0 | app2 | True | 29672.0 | 10.5% | 17.2% | 6.6 |
| 160.0 | 170.0 | end-users | True | 112252.0 | 68.4% | 64.9% | -3.5 |
| 170.0 | 180.0 | app1 | True | 32410.0 | 21.1% | 19.2% | -1.9 |
| 170.0 | 180.0 | app2 | True | 29812.0 | 10.5% | 17.6% | 7.1 |
| 170.0 | 180.0 | end-users | True | 106840.0 | 68.4% | 63.2% | -5.2 |
| 180.0 | 190.0 | app1 | True | 18932.0 | 21.1% | 12.1% | -9.0 |
| 180.0 | 190.0 | app2 | True | 21614.0 | 10.5% | 13.8% | 3.3 |
| 180.0 | 190.0 | end-users | True | 116268.0 | 68.4% | 74.1% | 5.7 |
| 190.0 | 200.0 | app1 | True | 32466.0 | 21.1% | 19.4% | -1.7 |
| 190.0 | 200.0 | app2 | True | 31072.0 | 10.5% | 18.5% | 8.0 |
| 190.0 | 200.0 | end-users | True | 104126.0 | 68.4% | 62.1% | -6.3 |
| 200.0 | 210.0 | app1 | True | 28392.0 | 21.1% | 16.7% | -4.4 |
| 200.0 | 210.0 | app2 | True | 30998.0 | 10.5% | 18.2% | 7.7 |
| 200.0 | 210.0 | end-users | True | 110924.0 | 68.4% | 65.1% | -3.3 |
| 210.0 | 220.0 | app1 | True | 24374.0 | 21.1% | 14.1% | -7.0 |
| 210.0 | 220.0 | app2 | True | 24320.0 | 10.5% | 14.1% | 3.5 |
| 210.0 | 220.0 | end-users | True | 124324.0 | 68.4% | 71.9% | 3.4 |
| 220.0 | 230.0 | app1 | True | 32438.0 | 21.1% | 21.4% | 0.4 |
| 220.0 | 230.0 | app2 | True | 26988.0 | 10.5% | 17.8% | 7.3 |
| 220.0 | 230.0 | end-users | True | 91998.0 | 68.4% | 60.8% | -7.7 |
| 230.0 | 240.0 | app1 | True | 22936.0 | 21.1% | 13.5% | -7.6 |
| 230.0 | 240.0 | app2 | True | 28418.0 | 10.5% | 16.7% | 6.2 |
| 230.0 | 240.0 | end-users | True | 118994.0 | 68.4% | 69.9% | 1.4 |
| 240.0 | 250.0 | app1 | False | 25700.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 28306.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 116104.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 29778.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 24396.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 71784.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 646980 | 31970 | 678950.0 | 0.0% | 704146.0 | 710920.0 | -1.0% | True |
| app2 | 639600 | 31702 | 667442.0 | -0.6% | 693554.0 | 703004.0 | -1.3% | True |
| end-users | 2551020 | 126572 | 2667249.0 | -0.4% | 2762276.0 | 2804164.0 | -1.5% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 535 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 530 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2115 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=3120). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 253030 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
