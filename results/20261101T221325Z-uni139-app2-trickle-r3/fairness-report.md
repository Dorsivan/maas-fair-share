# Fairness benchmark: app2-trickle (uni139-app2-trickle-r3)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app2-trickle` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T22:13:26Z` |
| Run end | `2026-11-01T22:17:49Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 636 | 200=636 | 11.3 | 18.8 | 803556.0 | 23.5% | 19.8% | -3.8 | 1.5s | 98.8% | 636.0 |
| app2 | 10.0 | 2 | 49 | 200=49 | 11.3 | 16.6 | 66238.0 | n/a | n/a | n/a | 1.5s | 97.4% | 49.0 |
| end-users | 65.0 | 104 | 2466 | 200=2460, 500=6 | 11.2 | 12.8 | 3198182.0 | 76.5% | 78.6% | 2.1 | 1.5s | 98.9% | 2460.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 98.1% | 0.0 |

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
| 0.0 | 10.0 | app1 | True | 2716.0 | 21.1% | 2.7% | -18.3 |
| 0.0 | 10.0 | app2 | True | 2694.0 | 10.5% | 2.7% | -7.8 |
| 0.0 | 10.0 | end-users | True | 93452.0 | 68.4% | 94.5% | 26.1 |
| 10.0 | 20.0 | app1 | True | 29814.0 | 21.1% | 17.6% | -3.4 |
| 10.0 | 20.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 10.0 | 20.0 | end-users | True | 136446.0 | 68.4% | 80.7% | 12.3 |
| 20.0 | 30.0 | app1 | True | 33820.0 | 21.1% | 18.9% | -2.1 |
| 20.0 | 30.0 | app2 | True | 2716.0 | 10.5% | 1.5% | -9.0 |
| 20.0 | 30.0 | end-users | True | 142004.0 | 68.4% | 79.5% | 11.1 |
| 30.0 | 40.0 | app1 | True | 36530.0 | 21.1% | 22.1% | 1.1 |
| 30.0 | 40.0 | app2 | True | 2686.0 | 10.5% | 1.6% | -8.9 |
| 30.0 | 40.0 | end-users | True | 125900.0 | 68.4% | 76.2% | 7.8 |
| 40.0 | 50.0 | app1 | True | 36544.0 | 21.1% | 21.6% | 0.6 |
| 40.0 | 50.0 | app2 | True | 2682.0 | 10.5% | 1.6% | -8.9 |
| 40.0 | 50.0 | end-users | True | 129932.0 | 68.4% | 76.8% | 8.4 |
| 50.0 | 60.0 | app1 | True | 24376.0 | 21.1% | 14.7% | -6.4 |
| 50.0 | 60.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 50.0 | 60.0 | end-users | True | 139142.0 | 68.4% | 83.7% | 15.3 |
| 60.0 | 71.0 | app1 | True | 32508.0 | 21.1% | 18.5% | -2.6 |
| 60.0 | 71.0 | app2 | True | 2712.0 | 10.5% | 1.5% | -9.0 |
| 60.0 | 71.0 | end-users | True | 140662.0 | 68.4% | 80.0% | 11.6 |
| 71.0 | 81.0 | app1 | True | 62180.0 | 21.1% | 37.4% | 16.3 |
| 71.0 | 81.0 | app2 | True | 4074.0 | 10.5% | 2.5% | -8.1 |
| 71.0 | 81.0 | end-users | True | 100030.0 | 68.4% | 60.2% | -8.3 |
| 81.0 | 91.0 | app1 | True | 32422.0 | 21.1% | 19.0% | -2.0 |
| 81.0 | 91.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 81.0 | 91.0 | end-users | True | 136712.0 | 68.4% | 80.2% | 11.8 |
| 91.0 | 101.0 | app1 | True | 9470.0 | 21.1% | 5.8% | -15.3 |
| 91.0 | 101.0 | app2 | True | 2682.0 | 10.5% | 1.6% | -8.9 |
| 91.0 | 101.0 | end-users | True | 151568.0 | 68.4% | 92.6% | 24.2 |
| 101.0 | 111.0 | app1 | True | 43272.0 | 21.1% | 26.4% | 5.4 |
| 101.0 | 111.0 | app2 | True | 2702.0 | 10.5% | 1.6% | -8.9 |
| 101.0 | 111.0 | end-users | True | 117800.0 | 68.4% | 71.9% | 3.5 |
| 111.0 | 121.0 | app1 | True | 44646.0 | 21.1% | 26.6% | 5.6 |
| 111.0 | 121.0 | app2 | True | 4042.0 | 10.5% | 2.4% | -8.1 |
| 111.0 | 121.0 | end-users | True | 118978.0 | 68.4% | 71.0% | 2.5 |
| 121.0 | 131.0 | app1 | True | 5416.0 | 21.1% | 3.2% | -17.8 |
| 121.0 | 131.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 121.0 | 131.0 | end-users | True | 162242.0 | 68.4% | 96.0% | 27.6 |
| 131.0 | 141.0 | app1 | True | 43334.0 | 21.1% | 25.8% | 4.8 |
| 131.0 | 141.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 131.0 | 141.0 | end-users | True | 121790.0 | 68.4% | 72.6% | 4.1 |
| 141.0 | 151.0 | app1 | True | 43230.0 | 21.1% | 25.6% | 4.5 |
| 141.0 | 151.0 | app2 | True | 2694.0 | 10.5% | 1.6% | -8.9 |
| 141.0 | 151.0 | end-users | True | 123208.0 | 68.4% | 72.8% | 4.4 |
| 151.0 | 161.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.2 |
| 151.0 | 161.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 151.0 | 161.0 | end-users | True | 162248.0 | 68.4% | 98.4% | 29.9 |
| 161.0 | 171.0 | app1 | True | 62290.0 | 21.1% | 37.4% | 16.4 |
| 161.0 | 171.0 | app2 | True | 5418.0 | 10.5% | 3.3% | -7.3 |
| 161.0 | 171.0 | end-users | True | 98766.0 | 68.4% | 59.3% | -9.1 |
| 171.0 | 181.0 | app1 | True | 46032.0 | 21.1% | 27.5% | 6.4 |
| 171.0 | 181.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 171.0 | 181.0 | end-users | True | 120190.0 | 68.4% | 71.7% | 3.3 |
| 181.0 | 191.0 | app1 | True | 1356.0 | 21.1% | 0.8% | -20.2 |
| 181.0 | 191.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 181.0 | 191.0 | end-users | True | 165106.0 | 68.4% | 98.4% | 30.0 |
| 191.0 | 201.0 | app1 | True | 62232.0 | 21.1% | 37.1% | 16.0 |
| 191.0 | 201.0 | app2 | True | 5368.0 | 10.5% | 3.2% | -7.3 |
| 191.0 | 201.0 | end-users | True | 100132.0 | 68.4% | 59.7% | -8.7 |
| 201.0 | 211.0 | app1 | True | 44590.0 | 21.1% | 26.8% | 5.7 |
| 201.0 | 211.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 201.0 | 211.0 | end-users | True | 120594.0 | 68.4% | 72.4% | 4.0 |
| 211.0 | 221.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 211.0 | 221.0 | app2 | True | 1348.0 | 10.5% | 0.8% | -9.7 |
| 211.0 | 221.0 | end-users | True | 167892.0 | 68.4% | 99.2% | 30.8 |
| 221.0 | 231.0 | app1 | True | 60806.0 | 21.1% | 36.8% | 15.8 |
| 221.0 | 231.0 | app2 | True | 5420.0 | 10.5% | 3.3% | -7.2 |
| 221.0 | 231.0 | end-users | True | 98790.0 | 68.4% | 59.9% | -8.6 |
| 231.0 | 241.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.3 |
| 231.0 | 241.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 231.0 | 241.0 | end-users | True | 170440.0 | 68.4% | 99.2% | 30.8 |
| 241.0 | 251.0 | app1 | False | 43256.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 2704.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 54158.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 782280 | 39049 | 821329.0 | 0.0% | 803556.0 | 860378.0 | -6.6% | True |
| app2 | 60270 | 2984 | 63254.0 | 0.0% | 66238.0 | 66238.0 | 0.0% | True |
| end-users | 3025800 | 151159 | 3176959.0 | 0.0% | 3198182.0 | 3328118.0 | -3.9% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
