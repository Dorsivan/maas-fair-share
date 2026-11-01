# Fairness benchmark: app1-idle (uni139-app1-idle-r1)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-idle` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T21:41:44Z` |
| Run end | `2026-11-01T21:46:18Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 98.8% | 0.0 |
| app2 | 10.0 | 32 | 183 | 200=183 | 33.8 | 101.1 | 217904.0 | 13.3% | 5.2% | -8.1 | 14.9s | 97.3% | 183.0 |
| end-users | 65.0 | 208 | 2999 | 200=2964, 500=35 | 17.3 | 20.3 | 3949312.0 | 86.7% | 94.8% | 8.1 | 14.9s | 98.9% | 2953.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 14896.0 | n/a | n/a | n/a | 0.1s | 95.7% | 11.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
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
| 0.0 | 10.0 | app2 | True | 9440.0 | 13.3% | 10.6% | -2.8 |
| 0.0 | 10.0 | end-users | True | 79816.0 | 86.7% | 89.4% | 2.8 |
| 10.0 | 20.0 | app2 | True | 13564.0 | 13.3% | 8.7% | -4.6 |
| 10.0 | 20.0 | end-users | True | 141804.0 | 86.7% | 91.3% | 4.6 |
| 20.0 | 30.0 | app2 | True | 20330.0 | 13.3% | 13.3% | -0.0 |
| 20.0 | 30.0 | end-users | True | 132538.0 | 86.7% | 86.7% | 0.0 |
| 30.0 | 40.0 | app2 | True | 22956.0 | 13.3% | 13.7% | 0.3 |
| 30.0 | 40.0 | end-users | True | 144830.0 | 86.7% | 86.3% | -0.3 |
| 40.0 | 50.0 | app2 | True | 21720.0 | 13.3% | 14.3% | 1.0 |
| 40.0 | 50.0 | end-users | True | 129890.0 | 86.7% | 85.7% | -1.0 |
| 50.0 | 60.0 | app2 | True | 1356.0 | 13.3% | 0.8% | -12.5 |
| 50.0 | 60.0 | end-users | True | 163654.0 | 86.7% | 99.2% | 12.5 |
| 60.0 | 70.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 60.0 | 70.0 | end-users | True | 171704.0 | 86.7% | 100.0% | 13.3 |
| 70.0 | 80.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 70.0 | 80.0 | end-users | True | 173216.0 | 86.7% | 100.0% | 13.3 |
| 80.0 | 90.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 80.0 | 90.0 | end-users | True | 151602.0 | 86.7% | 100.0% | 13.3 |
| 90.0 | 100.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 90.0 | 100.0 | end-users | True | 171616.0 | 86.7% | 100.0% | 13.3 |
| 100.0 | 110.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 100.0 | 110.0 | end-users | True | 171750.0 | 86.7% | 100.0% | 13.3 |
| 110.0 | 120.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 110.0 | 120.0 | end-users | True | 163696.0 | 86.7% | 100.0% | 13.3 |
| 120.0 | 130.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 120.0 | 130.0 | end-users | True | 152858.0 | 86.7% | 100.0% | 13.3 |
| 130.0 | 140.0 | app2 | True | 41970.0 | 13.3% | 24.8% | 11.5 |
| 130.0 | 140.0 | end-users | True | 127140.0 | 86.7% | 75.2% | -11.5 |
| 140.0 | 150.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 140.0 | 150.0 | end-users | True | 152828.0 | 86.7% | 100.0% | 13.3 |
| 150.0 | 160.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 150.0 | 160.0 | end-users | True | 169234.0 | 86.7% | 100.0% | 13.3 |
| 160.0 | 170.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 160.0 | 170.0 | end-users | True | 170330.0 | 86.7% | 100.0% | 13.3 |
| 170.0 | 180.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 170.0 | 180.0 | end-users | True | 167674.0 | 86.7% | 100.0% | 13.3 |
| 180.0 | 190.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 180.0 | 190.0 | end-users | True | 152836.0 | 86.7% | 100.0% | 13.3 |
| 190.0 | 200.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 190.0 | 200.0 | end-users | True | 168974.0 | 86.7% | 100.0% | 13.3 |
| 200.0 | 210.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 200.0 | 210.0 | end-users | True | 172912.0 | 86.7% | 100.0% | 13.3 |
| 210.0 | 220.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 210.0 | 220.0 | end-users | True | 151558.0 | 86.7% | 100.0% | 13.3 |
| 220.0 | 230.0 | app2 | True | 43258.0 | 13.3% | 26.0% | 12.7 |
| 220.0 | 230.0 | end-users | True | 123118.0 | 86.7% | 74.0% | -12.7 |
| 230.0 | 241.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 230.0 | 241.0 | end-users | True | 162340.0 | 86.7% | 100.0% | 13.3 |
| 241.0 | 251.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 159656.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 43310.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 121738.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 274.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 274.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -12.0%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app2 | 225090 | 11260 | 236350.0 | 0.0% | 217904.0 | 247610.0 | -12.0% | False |
| end-users | 3645720 | 181519 | 3813026.0 | -0.4% | 3949312.0 | 4008758.0 | -1.5% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
