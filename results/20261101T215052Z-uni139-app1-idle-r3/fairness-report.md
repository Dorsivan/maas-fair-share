# Fairness benchmark: app1-idle (uni139-app1-idle-r3)

**Verdict: FAIL** (threshold: 10 points)

- app2 deviated -11.2 points from its contention-adjusted expected share, exceeding the 10-point threshold

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
| Run start | `2026-11-01T21:50:53Z` |
| Run end | `2026-11-01T21:55:27Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 98.8% | 0.0 |
| app2 | 10.0 | 32 | 127 | 200=127 | 52.1 | 117.6 | 87896.0 | 13.3% | 2.1% | -11.2 | 14.7s | 97.3% | 127.0 |
| end-users | 65.0 | 208 | 3012 | 200=3012 | 17.3 | 20.2 | 4051546.0 | 86.7% | 97.9% | 11.2 | 14.7s | 98.9% | 3012.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 95.7% | 0.0 |

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
| 0.0 | 10.0 | app2 | True | 1354.0 | 13.3% | 2.0% | -11.3 |
| 0.0 | 10.0 | end-users | True | 64900.0 | 86.7% | 98.0% | 11.3 |
| 10.0 | 20.0 | app2 | True | 2716.0 | 13.3% | 1.6% | -11.8 |
| 10.0 | 20.0 | end-users | True | 170534.0 | 86.7% | 98.4% | 11.8 |
| 20.0 | 30.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 20.0 | 30.0 | end-users | True | 167766.0 | 86.7% | 100.0% | 13.3 |
| 30.0 | 40.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 30.0 | 40.0 | end-users | True | 150204.0 | 86.7% | 100.0% | 13.3 |
| 40.0 | 50.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 40.0 | 50.0 | end-users | True | 167828.0 | 86.7% | 100.0% | 13.3 |
| 50.0 | 61.0 | app2 | True | 41890.0 | 13.3% | 24.6% | 11.2 |
| 50.0 | 61.0 | end-users | True | 128674.0 | 86.7% | 75.4% | -11.2 |
| 61.0 | 71.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 61.0 | 71.0 | end-users | True | 151434.0 | 86.7% | 100.0% | 13.3 |
| 71.0 | 81.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 71.0 | 81.0 | end-users | True | 166286.0 | 86.7% | 100.0% | 13.3 |
| 81.0 | 91.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 81.0 | 91.0 | end-users | True | 167918.0 | 86.7% | 100.0% | 13.3 |
| 91.0 | 101.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 91.0 | 101.0 | end-users | True | 151560.0 | 86.7% | 100.0% | 13.3 |
| 101.0 | 111.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 101.0 | 111.0 | end-users | True | 169188.0 | 86.7% | 100.0% | 13.3 |
| 111.0 | 121.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 111.0 | 121.0 | end-users | True | 169124.0 | 86.7% | 100.0% | 13.3 |
| 121.0 | 131.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 121.0 | 131.0 | end-users | True | 170144.0 | 86.7% | 100.0% | 13.3 |
| 131.0 | 141.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 131.0 | 141.0 | end-users | True | 152850.0 | 86.7% | 100.0% | 13.3 |
| 141.0 | 151.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 141.0 | 151.0 | end-users | True | 171742.0 | 86.7% | 100.0% | 13.3 |
| 151.0 | 161.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 151.0 | 161.0 | end-users | True | 167746.0 | 86.7% | 100.0% | 13.3 |
| 161.0 | 171.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 161.0 | 171.0 | end-users | True | 154132.0 | 86.7% | 100.0% | 13.3 |
| 171.0 | 181.0 | app2 | True | 41936.0 | 13.3% | 24.6% | 11.3 |
| 171.0 | 181.0 | end-users | True | 128488.0 | 86.7% | 75.4% | -11.3 |
| 181.0 | 191.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 181.0 | 191.0 | end-users | True | 167496.0 | 86.7% | 100.0% | 13.3 |
| 191.0 | 201.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 191.0 | 201.0 | end-users | True | 150318.0 | 86.7% | 100.0% | 13.3 |
| 201.0 | 211.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 201.0 | 211.0 | end-users | True | 167728.0 | 86.7% | 100.0% | 13.3 |
| 211.0 | 221.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 211.0 | 221.0 | end-users | True | 167752.0 | 86.7% | 100.0% | 13.3 |
| 221.0 | 231.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 221.0 | 231.0 | end-users | True | 154234.0 | 86.7% | 100.0% | 13.3 |
| 231.0 | 241.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 231.0 | 241.0 | end-users | True | 169034.0 | 86.7% | 100.0% | 13.3 |
| 241.0 | 251.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 173130.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 131336.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 274.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 274.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -48.8%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app2 | 156210 | 7737 | 163947.0 | 0.0% | 87896.0 | 171684.0 | -48.8% | False |
| end-users | 3704760 | 184919 | 3889679.0 | 0.0% | 4051546.0 | 4074598.0 | -0.6% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
