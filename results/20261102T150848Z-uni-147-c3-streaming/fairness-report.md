# Fairness benchmark: full-contention (uni-147-c3-streaming)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-wshqk` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-02T15:10:02Z` |
| Run end | `2026-11-02T15:14:24Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 573 | 200=559, 500=14 | 13.5 | 22.0 | 742998.0 | 21.1% | 18.2% | -2.8 | 18.2% | -2.9 | 2.7s | 98.9% | 557.0 |
| app2 | 10.0 | 32 | 462 | 200=452, 500=10 | 23.9 | 28.1 | 586090.0 | 10.5% | 14.4% | 3.8 | 14.6% | 4.1 | 1.8s | 98.9% | 449.0 |
| end-users | 65.0 | 128 | 2121 | 200=2078, 500=43 | 14.5 | 20.1 | 2750388.0 | 68.4% | 67.4% | -1.0 | 67.2% | -1.2 | 2.3s | 0.0% | 2070.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 17580.0 | n/a | n/a | n/a | n/a | n/a | 0.1s | 38.0% | 13.0 |

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
| 0.0 | 230.0 | 230.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 5370.0 | 21.1% | 8.6% | -12.4 |
| 0.0 | 10.0 | app2 | True | 10804.0 | 10.5% | 17.4% | 6.9 |
| 0.0 | 10.0 | end-users | True | 45934.0 | 68.4% | 74.0% | 5.5 |
| 10.0 | 20.0 | app1 | True | 31128.0 | 21.1% | 18.1% | -3.0 |
| 10.0 | 20.0 | app2 | True | 20320.0 | 10.5% | 11.8% | 1.3 |
| 10.0 | 20.0 | end-users | True | 120528.0 | 68.4% | 70.1% | 1.7 |
| 20.0 | 30.0 | app1 | True | 32540.0 | 21.1% | 20.9% | -0.1 |
| 20.0 | 30.0 | app2 | True | 16236.0 | 10.5% | 10.4% | -0.1 |
| 20.0 | 30.0 | end-users | True | 106868.0 | 68.4% | 68.7% | 0.2 |
| 30.0 | 40.0 | app1 | True | 33874.0 | 21.1% | 19.9% | -1.2 |
| 30.0 | 40.0 | app2 | True | 41952.0 | 10.5% | 24.6% | 14.1 |
| 30.0 | 40.0 | end-users | True | 94512.0 | 68.4% | 55.5% | -12.9 |
| 40.0 | 50.0 | app1 | True | 12160.0 | 21.1% | 7.2% | -13.9 |
| 40.0 | 50.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 40.0 | 50.0 | end-users | True | 157008.0 | 68.4% | 92.8% | 24.4 |
| 50.0 | 60.0 | app1 | True | 43298.0 | 21.1% | 25.8% | 4.7 |
| 50.0 | 60.0 | app2 | True | 59514.0 | 10.5% | 35.5% | 24.9 |
| 50.0 | 60.0 | end-users | True | 65018.0 | 68.4% | 38.7% | -29.7 |
| 60.0 | 70.0 | app1 | True | 36466.0 | 21.1% | 23.7% | 2.6 |
| 60.0 | 70.0 | app2 | True | 5432.0 | 10.5% | 3.5% | -7.0 |
| 60.0 | 70.0 | end-users | True | 112146.0 | 68.4% | 72.8% | 4.4 |
| 70.0 | 80.0 | app1 | True | 6766.0 | 21.1% | 4.0% | -17.1 |
| 70.0 | 80.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 70.0 | 80.0 | end-users | True | 162332.0 | 68.4% | 96.0% | 27.6 |
| 80.0 | 90.0 | app1 | True | 51380.0 | 21.1% | 30.4% | 9.3 |
| 80.0 | 90.0 | app2 | True | 60952.0 | 10.5% | 36.0% | 25.5 |
| 80.0 | 90.0 | end-users | True | 56832.0 | 68.4% | 33.6% | -34.8 |
| 90.0 | 100.0 | app1 | True | 31078.0 | 21.1% | 20.5% | -0.5 |
| 90.0 | 100.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 90.0 | 100.0 | end-users | True | 120412.0 | 68.4% | 79.5% | 11.1 |
| 100.0 | 110.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.3 |
| 100.0 | 110.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 100.0 | 110.0 | end-users | True | 169058.0 | 68.4% | 99.2% | 30.8 |
| 110.0 | 120.0 | app1 | True | 55556.0 | 21.1% | 34.2% | 13.1 |
| 110.0 | 120.0 | app2 | True | 63666.0 | 10.5% | 39.2% | 28.6 |
| 110.0 | 120.0 | end-users | True | 43322.0 | 68.4% | 26.7% | -41.8 |
| 120.0 | 130.0 | app1 | True | 28492.0 | 21.1% | 17.4% | -3.7 |
| 120.0 | 130.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 120.0 | 130.0 | end-users | True | 133934.0 | 68.4% | 81.8% | 13.4 |
| 130.0 | 140.0 | app1 | True | 5372.0 | 21.1% | 3.5% | -17.6 |
| 130.0 | 140.0 | app2 | True | 2700.0 | 10.5% | 1.7% | -8.8 |
| 130.0 | 140.0 | end-users | True | 146258.0 | 68.4% | 94.8% | 26.3 |
| 140.0 | 150.0 | app1 | True | 55508.0 | 21.1% | 32.5% | 11.5 |
| 140.0 | 150.0 | app2 | True | 59560.0 | 10.5% | 34.9% | 24.4 |
| 140.0 | 150.0 | end-users | True | 55490.0 | 68.4% | 32.5% | -35.9 |
| 150.0 | 160.0 | app1 | True | 22972.0 | 21.1% | 13.9% | -7.1 |
| 150.0 | 160.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 150.0 | 160.0 | end-users | True | 141974.0 | 68.4% | 86.1% | 17.7 |
| 160.0 | 170.0 | app1 | True | 31130.0 | 21.1% | 20.5% | -0.5 |
| 160.0 | 170.0 | app2 | True | 14884.0 | 10.5% | 9.8% | -0.7 |
| 160.0 | 170.0 | end-users | True | 105618.0 | 68.4% | 69.7% | 1.2 |
| 170.0 | 180.0 | app1 | True | 37938.0 | 21.1% | 22.8% | 1.7 |
| 170.0 | 180.0 | app2 | True | 48766.0 | 10.5% | 29.3% | 18.8 |
| 170.0 | 180.0 | end-users | True | 79718.0 | 68.4% | 47.9% | -20.5 |
| 180.0 | 190.0 | app1 | True | 16248.0 | 21.1% | 9.7% | -11.4 |
| 180.0 | 190.0 | app2 | True | 2712.0 | 10.5% | 1.6% | -8.9 |
| 180.0 | 190.0 | end-users | True | 148926.0 | 68.4% | 88.7% | 20.3 |
| 190.0 | 200.0 | app1 | True | 41980.0 | 21.1% | 26.1% | 5.0 |
| 190.0 | 200.0 | app2 | True | 43200.0 | 10.5% | 26.8% | 16.3 |
| 190.0 | 200.0 | end-users | True | 75798.0 | 68.4% | 47.1% | -21.3 |
| 200.0 | 210.0 | app1 | True | 32466.0 | 21.1% | 20.2% | -0.9 |
| 200.0 | 210.0 | app2 | True | 27084.0 | 10.5% | 16.8% | 6.3 |
| 200.0 | 210.0 | end-users | True | 101430.0 | 68.4% | 63.0% | -5.4 |
| 210.0 | 220.0 | app1 | True | 5412.0 | 21.1% | 3.3% | -17.7 |
| 210.0 | 220.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 210.0 | 220.0 | end-users | True | 158256.0 | 68.4% | 96.7% | 28.3 |
| 220.0 | 230.0 | app1 | True | 44672.0 | 21.1% | 26.8% | 5.8 |
| 220.0 | 230.0 | app2 | True | 62254.0 | 10.5% | 37.4% | 26.9 |
| 220.0 | 230.0 | end-users | True | 59528.0 | 68.4% | 35.8% | -32.7 |
| 230.0 | 240.0 | app1 | True | 35212.0 | 21.1% | 23.4% | 2.4 |
| 230.0 | 240.0 | app2 | True | 1334.0 | 10.5% | 0.9% | -9.6 |
| 230.0 | 240.0 | end-users | True | 113646.0 | 68.4% | 75.7% | 7.2 |
| 240.0 | 250.0 | app1 | False | 6768.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 1358.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 160962.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 37854.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 42004.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 14880.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- end-users exceeded the 10% ledger tolerance: raw tokens +5743.2%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 687570 | 34455 | 719446.0 | -0.4% | 742998.0 | 756480.0 | -1.8% | True |
| app2 | 555960 | 27950 | 580039.0 | -0.7% | 586090.0 | 611860.0 | -4.2% | True |
| end-users | 2555940 | 127719 | 156810883.0 | 5743.2% | 2750388.0 | 2811378.0 | -2.2% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 573 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 462 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2121 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

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
