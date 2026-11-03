# Fairness benchmark: full-contention (uni-155-e1-epp-restart-mid-run)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-hzf92` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-03T13:32:13Z` |
| Run end | `2026-11-03T13:39:23Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 962 | 000=1, 200=948, 500=13 | 11.8 | 21.8 | 730634.0 | 21.1% | 20.9% | -0.2 | 18.9% | -2.1 | 2.3s | 98.9% | 542.0 |
| app2 | 10.0 | 32 | 642 | 000=13, 200=613, 500=16 | 13.8 | 25.8 | 424614.0 | 10.5% | 12.1% | 1.6 | 12.6% | 2.1 | 1.7s | 98.9% | 323.0 |
| end-users | 65.0 | 128 | 3476 | 000=35, 200=3358, 500=83 | 11.6 | 18.4 | 2347576.0 | 68.4% | 67.0% | -1.4 | 68.4% | 0.0 | 2.0s | 98.9% | 1745.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events (scheduled):**
- t+120s: epp_delete

**Per-tenant schedule:**
- app1: active 0s-360s, no duty cycle
- app2: active 0s-360s, no duty cycle
- end-users: active 0s-360s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 120.0 | 121.0 | 1.0 |
| 360.0 | n/a (never converged in this phase) | n/a |

**Windows** (13 total, EPP restart detected mid-window at least once):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 16200.0 | 21.1% | 19.6% | -1.4 |
| 0.0 | 10.0 | app2 | True | 17574.0 | 10.5% | 21.3% | 10.8 |
| 0.0 | 10.0 | end-users | True | 48708.0 | 68.4% | 59.1% | -9.4 |
| 10.0 | 20.0 | app1 | True | 32458.0 | 21.1% | 19.5% | -1.6 |
| 10.0 | 20.0 | app2 | True | 23056.0 | 10.5% | 13.9% | 3.3 |
| 10.0 | 20.0 | end-users | True | 110928.0 | 68.4% | 66.6% | -1.8 |
| 20.0 | 30.0 | app1 | True | 36494.0 | 21.1% | 21.1% | 0.0 |
| 20.0 | 30.0 | app2 | True | 20260.0 | 10.5% | 11.7% | 1.2 |
| 20.0 | 30.0 | end-users | True | 116286.0 | 68.4% | 67.2% | -1.2 |
| 30.0 | 40.0 | app1 | True | 14848.0 | 21.1% | 8.8% | -12.3 |
| 30.0 | 40.0 | app2 | True | 20306.0 | 10.5% | 12.0% | 1.5 |
| 30.0 | 40.0 | end-users | True | 133720.0 | 68.4% | 79.2% | 10.8 |
| 40.0 | 50.0 | app1 | True | 25736.0 | 21.1% | 16.8% | -4.2 |
| 40.0 | 50.0 | app2 | True | 20298.0 | 10.5% | 13.3% | 2.7 |
| 40.0 | 50.0 | end-users | True | 106992.0 | 68.4% | 69.9% | 1.5 |
| 50.0 | 60.0 | app1 | True | 40594.0 | 21.1% | 24.2% | 3.1 |
| 50.0 | 60.0 | app2 | True | 33848.0 | 10.5% | 20.2% | 9.6 |
| 50.0 | 60.0 | end-users | True | 93472.0 | 68.4% | 55.7% | -12.8 |
| 60.0 | 70.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 60.0 | 70.0 | app2 | True | 5430.0 | 10.5% | 3.2% | -7.3 |
| 60.0 | 70.0 | end-users | True | 163678.0 | 68.4% | 96.8% | 28.4 |
| 70.0 | 80.0 | app1 | True | 46066.0 | 21.1% | 27.9% | 6.9 |
| 70.0 | 80.0 | app2 | True | 55368.0 | 10.5% | 33.6% | 23.0 |
| 70.0 | 80.0 | end-users | True | 63578.0 | 68.4% | 38.5% | -29.9 |
| 80.0 | 90.0 | app1 | True | 32446.0 | 21.1% | 20.5% | -0.5 |
| 80.0 | 90.0 | app2 | True | 5432.0 | 10.5% | 3.4% | -7.1 |
| 80.0 | 90.0 | end-users | True | 120356.0 | 68.4% | 76.1% | 7.6 |
| 90.0 | 101.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 90.0 | 101.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 90.0 | 101.0 | end-users | True | 173010.0 | 68.4% | 100.0% | 31.6 |
| 101.0 | 111.0 | app1 | True | 56872.0 | 21.1% | 34.2% | 13.1 |
| 101.0 | 111.0 | app2 | True | 59622.0 | 10.5% | 35.8% | 25.3 |
| 101.0 | 111.0 | end-users | True | 49998.0 | 68.4% | 30.0% | -38.4 |
| 111.0 | 121.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 111.0 | 121.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 111.0 | 121.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 121.0 | 430.0 | app1 | True | 730634.0 | 21.1% | 20.9% | -0.2 |
| 121.0 | 430.0 | app2 | True | 424614.0 | 10.5% | 12.1% | 1.6 |
| 121.0 | 430.0 | end-users | True | 2347576.0 | 68.4% | 67.0% | -1.4 |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens -42.8%, cost -43.0%
- app2 exceeded the 10% ledger tolerance: raw tokens -47.3%, cost -48.8%
- end-users exceeded the 10% ledger tolerance: raw tokens -48.0%, cost -48.3%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1166040 | 58361 | 700005.0 | -42.8% | 730634.0 | 1282762.0 | -43.0% | False |
| app2 | 753990 | 37620 | 417029.0 | -47.3% | 424614.0 | 829230.0 | -48.8% | False |
| end-users | 4130340 | 206266 | 2253710.0 | -48.0% | 2347576.0 | 4542872.0 | -48.3% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 962 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 642 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3476 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

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
