# Fairness benchmark: asymmetric-request-shapes (uni-146-c1-asymmetric-request-shapes-enforced)

**Verdict: UNCONTENDED** -- every offered group's `contended_seconds_total` delta stayed under 1s, so the pool was never actually contended. Not scored against the 10-point weighted-split threshold; see docs/runbook.md.

- every offered group's contended_seconds_total delta stayed under 1s (app1=0.20s, end-users=0.20s) -- an order of magnitude below the ~9s a genuinely-contending tenant accrues in a 240s full-contention run (docs/runbook.md), so nobody was ever backlogged alongside anyone else and the weighted-split deviation check does not apply

## Run metadata

| field | value |
|---|---|
| Scenario | `asymmetric-request-shapes` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-k6dfc` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-02T14:34:23Z` |
| Run end | `2026-11-02T14:41:54Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 92 | 000=17, 200=72, 500=3 | 100.9 | 300.0 | 102071.0 | 23.5% | 13.8% | -9.7 | 25.4% | 1.9 | 0.2s | 98.9% | 89.0 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| end-users | 65.0 | 104 | 270 | 200=239, 500=31 | 169.8 | 202.9 | 636896.0 | 76.5% | 86.2% | 9.7 | 74.6% | -1.9 | 0.2s | 77.4% | 239.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (45 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 1358.0 | 23.5% | 100.0% | 76.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 76.5% | 0.0% | -76.5 |
| 10.0 | 20.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 10.0 | 20.0 | end-users | True | 0.0 | 76.5% | 0.0% | -76.5 |
| 20.0 | 30.0 | app1 | True | 2710.0 | 23.5% | 11.2% | -12.3 |
| 20.0 | 30.0 | end-users | True | 21434.0 | 76.5% | 88.8% | 12.3 |
| 30.0 | 40.0 | app1 | True | 5432.0 | 23.5% | 18.2% | -5.4 |
| 30.0 | 40.0 | end-users | True | 24496.0 | 76.5% | 81.8% | 5.4 |
| 40.0 | 50.0 | app1 | True | 1358.0 | 23.5% | 100.0% | 76.5 |
| 40.0 | 50.0 | end-users | True | 0.0 | 76.5% | 0.0% | -76.5 |
| 50.0 | 60.0 | app1 | True | 4036.0 | 23.5% | 14.1% | -9.4 |
| 50.0 | 60.0 | end-users | True | 24496.0 | 76.5% | 85.9% | 9.4 |
| 60.0 | 70.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 60.0 | 70.0 | end-users | True | 0.0 | 76.5% | 0.0% | -76.5 |
| 70.0 | 80.0 | app1 | True | 5428.0 | 23.5% | 10.6% | -13.0 |
| 70.0 | 80.0 | end-users | True | 45930.0 | 76.5% | 89.4% | 13.0 |
| 80.0 | 90.0 | app1 | True | 5406.0 | 23.5% | 16.4% | -7.1 |
| 80.0 | 90.0 | end-users | True | 27558.0 | 76.5% | 83.6% | 7.1 |
| 90.0 | 100.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 90.0 | 100.0 | end-users | True | 0.0 | 76.5% | 0.0% | -76.5 |
| 100.0 | 110.0 | app1 | True | 8110.0 | 23.5% | 24.9% | 1.3 |
| 100.0 | 110.0 | end-users | True | 24496.0 | 76.5% | 75.1% | -1.3 |
| 110.0 | 120.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 110.0 | 120.0 | end-users | True | 0.0 | 76.5% | 0.0% | -76.5 |
| 120.0 | 130.0 | app1 | True | 8134.0 | 23.5% | 24.9% | 1.4 |
| 120.0 | 130.0 | end-users | True | 24496.0 | 76.5% | 75.1% | -1.4 |
| 130.0 | 140.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 130.0 | 140.0 | end-users | True | 15310.0 | 76.5% | 100.0% | 23.5 |
| 140.0 | 150.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 140.0 | 150.0 | end-users | True | 9186.0 | 76.5% | 100.0% | 23.5 |
| 150.0 | 160.0 | app1 | True | 5422.0 | 23.5% | 18.1% | -5.4 |
| 150.0 | 160.0 | end-users | True | 24496.0 | 76.5% | 81.9% | 5.4 |
| 160.0 | 170.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 160.0 | 170.0 | end-users | True | 0.0 | 76.5% | 0.0% | -76.5 |
| 170.0 | 180.0 | app1 | True | 2684.0 | 23.5% | 9.9% | -13.7 |
| 170.0 | 180.0 | end-users | True | 24496.0 | 76.5% | 90.1% | 13.7 |
| 180.0 | 190.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 180.0 | 190.0 | end-users | True | 9186.0 | 76.5% | 100.0% | 23.5 |
| 190.0 | 200.0 | app1 | True | 1358.0 | 23.5% | 8.1% | -15.4 |
| 190.0 | 200.0 | end-users | True | 15310.0 | 76.5% | 91.9% | 15.4 |
| 200.0 | 210.0 | app1 | True | 2706.0 | 23.5% | 9.9% | -13.6 |
| 200.0 | 210.0 | end-users | True | 24496.0 | 76.5% | 90.1% | 13.6 |
| 210.0 | 220.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 210.0 | 220.0 | end-users | True | 0.0 | 76.5% | 0.0% | -76.5 |
| 220.0 | 230.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 220.0 | 230.0 | end-users | True | 24496.0 | 76.5% | 100.0% | 23.5 |
| 230.0 | 240.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 230.0 | 240.0 | end-users | True | 27558.0 | 76.5% | 100.0% | 23.5 |
| 240.0 | 250.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 18372.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 30620.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | end-users | False | 24496.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | end-users | False | 24496.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | end-users | False | 24496.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 330.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 330.0 | end-users | False | 24496.0 | n/a | n/a | n/a |
| 330.0 | 340.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 330.0 | 340.0 | end-users | False | 24496.0 | n/a | n/a | n/a |
| 340.0 | 351.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 340.0 | 351.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | False | 4875.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | False | 24496.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | 6500.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | False | 24496.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | 6500.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | False | 24496.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | False | 30054.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | end-users | False | 24496.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- end-users exceeded the 10% ledger tolerance: cost -13.0%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 88560 | 4440 | 93000.0 | 0.0% | 102071.0 | 97440.0 | 4.8% | True |
| end-users | 14818 | 358500 | 373318.0 | 0.0% | 636896.0 | 731818.0 | -13.0% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 92 | 0 | 0 | 0 (never shed) | 0.00% | 23.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 270 | 0 | 0 | 0 (never shed) | 0.00% | 76.5% | n/a (nothing shed) | n/a (nothing shed) |

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
