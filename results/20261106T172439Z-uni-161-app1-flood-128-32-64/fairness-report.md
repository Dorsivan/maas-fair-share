# Fairness benchmark: app1-flood-moderate (uni-161-app1-flood-128-32-64)

**Verdict: FAIL** (threshold: 10 points)

- end-users deviated -30.2 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-flood-moderate` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-796bc55c4b-snmfw` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-06T17:25:50Z` |
| Run end | `2026-11-06T17:30:23Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 30.0 | 128 | 1895 | 200=1831, 500=64 | 17.1 | 22.0 | 2426664.0 | 30.0% | 58.2% | 28.2 | 58.0% | 28.0 | 18.0s | 98.9% | 1824.0 |
| app2 | 10.0 | 32 | 403 | 200=379, 500=24 | 20.0 | 29.9 | 500390.0 | 10.0% | 12.0% | 2.0 | 12.3% | 2.3 | 17.8s | 98.9% | 376.0 |
| end-users | 60.0 | 64 | 972 | 200=935, 500=37 | 19.7 | 25.2 | 1242820.0 | 60.0% | 29.8% | -30.2 | 29.7% | -30.3 | 17.3s | 98.9% | 930.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 20292.0 | n/a | n/a | n/a | n/a | n/a | 0.1s | 98.9% | 15.0 |

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

**Windows** (28 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 29736.0 | 30.0% | 50.0% | 20.0 |
| 0.0 | 10.0 | app2 | True | 1358.0 | 10.0% | 2.3% | -7.7 |
| 0.0 | 10.0 | end-users | True | 28404.0 | 60.0% | 47.7% | -12.3 |
| 10.0 | 20.0 | app1 | True | 82464.0 | 30.0% | 53.0% | 23.0 |
| 10.0 | 20.0 | app2 | True | 24362.0 | 10.0% | 15.7% | 5.7 |
| 10.0 | 20.0 | end-users | True | 48640.0 | 60.0% | 31.3% | -28.7 |
| 20.0 | 30.0 | app1 | True | 70248.0 | 30.0% | 41.6% | 11.6 |
| 20.0 | 30.0 | app2 | True | 13492.0 | 10.0% | 8.0% | -2.0 |
| 20.0 | 30.0 | end-users | True | 85260.0 | 60.0% | 50.4% | -9.6 |
| 30.0 | 40.0 | app1 | True | 127040.0 | 30.0% | 74.6% | 44.6 |
| 30.0 | 40.0 | app2 | True | 43260.0 | 10.0% | 25.4% | 15.4 |
| 30.0 | 40.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 40.0 | 50.0 | app1 | True | 66188.0 | 30.0% | 37.9% | 7.9 |
| 40.0 | 50.0 | app2 | True | 21682.0 | 10.0% | 12.4% | 2.4 |
| 40.0 | 50.0 | end-users | True | 86632.0 | 60.0% | 49.6% | -10.4 |
| 50.0 | 60.0 | app1 | True | 59516.0 | 30.0% | 40.0% | 10.0 |
| 50.0 | 60.0 | app2 | True | 20320.0 | 10.0% | 13.7% | 3.7 |
| 50.0 | 60.0 | end-users | True | 68980.0 | 60.0% | 46.4% | -13.6 |
| 60.0 | 70.0 | app1 | True | 122988.0 | 30.0% | 71.6% | 41.6 |
| 60.0 | 70.0 | app2 | True | 39240.0 | 10.0% | 22.9% | 12.9 |
| 60.0 | 70.0 | end-users | True | 9484.0 | 60.0% | 5.5% | -54.5 |
| 70.0 | 80.0 | app1 | True | 62208.0 | 30.0% | 40.7% | 10.7 |
| 70.0 | 80.0 | app2 | True | 12142.0 | 10.0% | 8.0% | -2.0 |
| 70.0 | 80.0 | end-users | True | 78346.0 | 60.0% | 51.3% | -8.7 |
| 80.0 | 90.0 | app1 | True | 136502.0 | 30.0% | 80.1% | 50.1 |
| 80.0 | 90.0 | app2 | True | 5412.0 | 10.0% | 3.2% | -6.8 |
| 80.0 | 90.0 | end-users | True | 28406.0 | 60.0% | 16.7% | -43.3 |
| 90.0 | 100.0 | app1 | True | 64916.0 | 30.0% | 37.8% | 7.8 |
| 90.0 | 100.0 | app2 | True | 14926.0 | 10.0% | 8.7% | -1.3 |
| 90.0 | 100.0 | end-users | True | 91950.0 | 60.0% | 53.5% | -6.5 |
| 100.0 | 111.0 | app1 | True | 111018.0 | 30.0% | 64.6% | 34.6 |
| 100.0 | 111.0 | app2 | True | 37828.0 | 10.0% | 22.0% | 12.0 |
| 100.0 | 111.0 | end-users | True | 22986.0 | 60.0% | 13.4% | -46.6 |
| 111.0 | 121.0 | app1 | True | 83932.0 | 30.0% | 55.4% | 25.4 |
| 111.0 | 121.0 | app2 | True | 27050.0 | 10.0% | 17.8% | 7.8 |
| 111.0 | 121.0 | end-users | True | 40648.0 | 60.0% | 26.8% | -33.2 |
| 121.0 | 131.0 | app1 | True | 81088.0 | 30.0% | 48.4% | 18.4 |
| 121.0 | 131.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 121.0 | 131.0 | end-users | True | 86570.0 | 60.0% | 51.6% | -8.4 |
| 131.0 | 141.0 | app1 | True | 140442.0 | 30.0% | 80.6% | 50.6 |
| 131.0 | 141.0 | app2 | True | 32436.0 | 10.0% | 18.6% | 8.6 |
| 131.0 | 141.0 | end-users | True | 1348.0 | 60.0% | 0.8% | -59.2 |
| 141.0 | 151.0 | app1 | True | 89218.0 | 30.0% | 54.1% | 24.1 |
| 141.0 | 151.0 | app2 | True | 20282.0 | 10.0% | 12.3% | 2.3 |
| 141.0 | 151.0 | end-users | True | 55466.0 | 60.0% | 33.6% | -26.4 |
| 151.0 | 161.0 | app1 | True | 86512.0 | 30.0% | 55.7% | 25.7 |
| 151.0 | 161.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 151.0 | 161.0 | end-users | True | 68838.0 | 60.0% | 44.3% | -15.7 |
| 161.0 | 171.0 | app1 | True | 133944.0 | 30.0% | 78.0% | 48.0 |
| 161.0 | 171.0 | app2 | True | 37848.0 | 10.0% | 22.0% | 12.0 |
| 161.0 | 171.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 171.0 | 181.0 | app1 | True | 81014.0 | 30.0% | 46.8% | 16.8 |
| 171.0 | 181.0 | app2 | True | 12144.0 | 10.0% | 7.0% | -3.0 |
| 171.0 | 181.0 | end-users | True | 79814.0 | 60.0% | 46.1% | -13.9 |
| 181.0 | 191.0 | app1 | True | 102778.0 | 30.0% | 68.5% | 38.5 |
| 181.0 | 191.0 | app2 | True | 4072.0 | 10.0% | 2.7% | -7.3 |
| 181.0 | 191.0 | end-users | True | 43280.0 | 60.0% | 28.8% | -31.2 |
| 191.0 | 201.0 | app1 | True | 129826.0 | 30.0% | 77.4% | 47.4 |
| 191.0 | 201.0 | app2 | True | 37886.0 | 10.0% | 22.6% | 12.6 |
| 191.0 | 201.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 201.0 | 211.0 | app1 | True | 70352.0 | 30.0% | 41.3% | 11.3 |
| 201.0 | 211.0 | app2 | True | 5418.0 | 10.0% | 3.2% | -6.8 |
| 201.0 | 211.0 | end-users | True | 94638.0 | 60.0% | 55.5% | -4.5 |
| 211.0 | 221.0 | app1 | True | 139244.0 | 30.0% | 79.9% | 49.9 |
| 211.0 | 221.0 | app2 | True | 14842.0 | 10.0% | 8.5% | -1.5 |
| 211.0 | 221.0 | end-users | True | 20262.0 | 60.0% | 11.6% | -48.4 |
| 221.0 | 231.0 | app1 | True | 106912.0 | 30.0% | 69.9% | 39.9 |
| 221.0 | 231.0 | app2 | True | 31060.0 | 10.0% | 20.3% | 10.3 |
| 221.0 | 231.0 | end-users | True | 14900.0 | 60.0% | 9.7% | -50.3 |
| 231.0 | 241.0 | app1 | True | 68942.0 | 30.0% | 40.5% | 10.5 |
| 231.0 | 241.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 231.0 | 241.0 | end-users | True | 101472.0 | 60.0% | 59.5% | -0.5 |
| 241.0 | 251.0 | app1 | False | 151340.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 16208.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 1358.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 28296.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 27122.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 85138.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 273.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 273.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 273.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2252130 | 111616 | 2354698.0 | -0.4% | 2426664.0 | 2475362.0 | -2.0% | True |
| app2 | 466170 | 23210 | 485503.0 | -0.8% | 500390.0 | 512590.0 | -2.4% | True |
| end-users | 1150050 | 57211 | 1200815.0 | -0.5% | 1242820.0 | 1264472.0 | -1.7% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1895 | 0 | 0 | 0 (never shed) | 0.00% | 30.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 403 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 972 | 0 | 0 | 0 (never shed) | 0.00% | 60.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=3145). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 261989 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
