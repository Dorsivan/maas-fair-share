# Fairness benchmark: app2-idle (uni139-app2-idle-r2)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app2-idle` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T21:24:07Z` |
| Run end | `2026-11-01T21:28:30Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 662 | 200=662 | 10.9 | 18.5 | 819666.0 | 23.5% | 19.5% | -4.0 | 1.6s | 98.8% | 662.0 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 97.3% | 0.0 |
| end-users | 65.0 | 104 | 2568 | 200=2518, 500=50 | 10.8 | 12.3 | 3381282.0 | 76.5% | 80.5% | 4.0 | 1.6s | 98.9% | 2517.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 1358.0 | n/a | n/a | n/a | 0.0s | 91.3% | 1.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 201.0 | 201.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 40646.0 | 23.5% | 34.5% | 11.0 |
| 0.0 | 10.0 | end-users | True | 77162.0 | 76.5% | 65.5% | -11.0 |
| 10.0 | 20.0 | app1 | True | 2716.0 | 23.5% | 1.6% | -21.9 |
| 10.0 | 20.0 | end-users | True | 169130.0 | 76.5% | 98.4% | 21.9 |
| 20.0 | 30.0 | app1 | True | 62118.0 | 23.5% | 36.8% | 13.2 |
| 20.0 | 30.0 | end-users | True | 106778.0 | 76.5% | 63.2% | -13.2 |
| 30.0 | 40.0 | app1 | True | 21584.0 | 23.5% | 12.6% | -11.0 |
| 30.0 | 40.0 | end-users | True | 150120.0 | 76.5% | 87.4% | 11.0 |
| 40.0 | 50.0 | app1 | True | 25732.0 | 23.5% | 15.6% | -7.9 |
| 40.0 | 50.0 | end-users | True | 139406.0 | 76.5% | 84.4% | 7.9 |
| 50.0 | 60.0 | app1 | True | 50044.0 | 23.5% | 27.8% | 4.3 |
| 50.0 | 60.0 | end-users | True | 129826.0 | 76.5% | 72.2% | -4.3 |
| 60.0 | 70.0 | app1 | True | 32452.0 | 23.5% | 18.6% | -4.9 |
| 60.0 | 70.0 | end-users | True | 142010.0 | 76.5% | 81.4% | 4.9 |
| 70.0 | 80.0 | app1 | True | 43336.0 | 23.5% | 25.4% | 1.9 |
| 70.0 | 80.0 | end-users | True | 127024.0 | 76.5% | 74.6% | -1.9 |
| 80.0 | 90.0 | app1 | True | 41958.0 | 23.5% | 24.6% | 1.1 |
| 80.0 | 90.0 | end-users | True | 128496.0 | 76.5% | 75.4% | -1.1 |
| 90.0 | 100.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 90.0 | 100.0 | end-users | True | 173090.0 | 76.5% | 100.0% | 23.5 |
| 100.0 | 110.0 | app1 | True | 63530.0 | 23.5% | 37.6% | 14.0 |
| 100.0 | 110.0 | end-users | True | 105630.0 | 76.5% | 62.4% | -14.0 |
| 110.0 | 120.0 | app1 | True | 1354.0 | 23.5% | 0.8% | -22.7 |
| 110.0 | 120.0 | end-users | True | 162386.0 | 76.5% | 99.2% | 22.7 |
| 120.0 | 131.0 | app1 | True | 63530.0 | 23.5% | 37.0% | 13.5 |
| 120.0 | 131.0 | end-users | True | 108128.0 | 76.5% | 63.0% | -13.5 |
| 131.0 | 141.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 131.0 | 141.0 | end-users | True | 170326.0 | 76.5% | 100.0% | 23.5 |
| 141.0 | 151.0 | app1 | True | 62196.0 | 23.5% | 36.2% | 12.7 |
| 141.0 | 151.0 | end-users | True | 109502.0 | 76.5% | 63.8% | -12.7 |
| 151.0 | 161.0 | app1 | True | 43318.0 | 23.5% | 26.4% | 2.9 |
| 151.0 | 161.0 | end-users | True | 120490.0 | 76.5% | 73.6% | -2.9 |
| 161.0 | 171.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 161.0 | 171.0 | end-users | True | 170436.0 | 76.5% | 100.0% | 23.5 |
| 171.0 | 181.0 | app1 | True | 43362.0 | 23.5% | 25.2% | 1.7 |
| 171.0 | 181.0 | end-users | True | 128488.0 | 76.5% | 74.8% | -1.7 |
| 181.0 | 191.0 | app1 | True | 45934.0 | 23.5% | 27.8% | 4.3 |
| 181.0 | 191.0 | end-users | True | 119064.0 | 76.5% | 72.2% | -4.3 |
| 191.0 | 201.0 | app1 | True | 2664.0 | 23.5% | 1.6% | -22.0 |
| 191.0 | 201.0 | end-users | True | 167766.0 | 76.5% | 98.4% | 22.0 |
| 201.0 | 211.0 | app1 | True | 40654.0 | 23.5% | 24.6% | 1.1 |
| 201.0 | 211.0 | end-users | True | 124466.0 | 76.5% | 75.4% | -1.1 |
| 211.0 | 221.0 | app1 | True | 43276.0 | 23.5% | 25.6% | 2.1 |
| 211.0 | 221.0 | end-users | True | 125798.0 | 76.5% | 74.4% | -2.1 |
| 221.0 | 231.0 | app1 | True | 25678.0 | 23.5% | 15.0% | -8.6 |
| 221.0 | 231.0 | end-users | True | 145954.0 | 76.5% | 85.0% | 8.6 |
| 231.0 | 241.0 | app1 | True | 32426.0 | 23.5% | 18.9% | -4.7 |
| 231.0 | 241.0 | end-users | True | 139358.0 | 76.5% | 81.1% | 4.7 |
| 241.0 | 251.0 | app1 | False | 29800.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 136388.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 1358.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 4060.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 814260 | 40602 | 854862.0 | 0.0% | 819666.0 | 895464.0 | -8.5% | True |
| end-users | 3097140 | 154264 | 3250110.0 | -0.0% | 3381282.0 | 3405668.0 | -0.7% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
