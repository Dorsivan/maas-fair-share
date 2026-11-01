# Fairness benchmark: app1-idle (uni139-app1-idle-r4)

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
| Run start | `2026-11-01T21:55:28Z` |
| Run end | `2026-11-01T22:00:02Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 98.8% | 0.0 |
| app2 | 10.0 | 32 | 212 | 200=212 | 33.0 | 87.1 | 248876.0 | 13.3% | 6.0% | -7.3 | 11.4s | 97.4% | 212.0 |
| end-users | 65.0 | 208 | 2943 | 200=2911, 500=32 | 17.4 | 21.2 | 3900976.0 | 86.7% | 94.0% | 7.3 | 11.4s | 98.9% | 2910.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 1324.0 | n/a | n/a | n/a | 0.1s | 95.9% | 1.0 |

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
| 0.0 | 10.0 | app2 | True | 4062.0 | 13.3% | 5.5% | -7.9 |
| 0.0 | 10.0 | end-users | True | 70352.0 | 86.7% | 94.5% | 7.9 |
| 10.0 | 20.0 | app2 | True | 5424.0 | 13.3% | 3.2% | -10.1 |
| 10.0 | 20.0 | end-users | True | 163850.0 | 86.7% | 96.8% | 10.1 |
| 20.0 | 30.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 20.0 | 30.0 | end-users | True | 151504.0 | 86.7% | 100.0% | 13.3 |
| 30.0 | 40.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 30.0 | 40.0 | end-users | True | 167668.0 | 86.7% | 100.0% | 13.3 |
| 40.0 | 50.0 | app2 | True | 41850.0 | 13.3% | 24.2% | 10.8 |
| 40.0 | 50.0 | end-users | True | 131208.0 | 86.7% | 75.8% | -10.8 |
| 50.0 | 60.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 50.0 | 60.0 | end-users | True | 150112.0 | 86.7% | 100.0% | 13.3 |
| 60.0 | 70.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 60.0 | 70.0 | end-users | True | 171906.0 | 86.7% | 100.0% | 13.3 |
| 70.0 | 80.0 | app2 | True | 9482.0 | 13.3% | 6.3% | -7.1 |
| 70.0 | 80.0 | end-users | True | 142098.0 | 86.7% | 93.7% | 7.1 |
| 80.0 | 90.0 | app2 | True | 54156.0 | 13.3% | 32.8% | 19.5 |
| 80.0 | 90.0 | end-users | True | 110804.0 | 86.7% | 67.2% | -19.5 |
| 90.0 | 100.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 90.0 | 100.0 | end-users | True | 170546.0 | 86.7% | 100.0% | 13.3 |
| 100.0 | 110.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 100.0 | 110.0 | end-users | True | 170492.0 | 86.7% | 100.0% | 13.3 |
| 110.0 | 120.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 110.0 | 120.0 | end-users | True | 150100.0 | 86.7% | 100.0% | 13.3 |
| 120.0 | 130.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 120.0 | 130.0 | end-users | True | 167824.0 | 86.7% | 100.0% | 13.3 |
| 130.0 | 140.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 130.0 | 140.0 | end-users | True | 170384.0 | 86.7% | 100.0% | 13.3 |
| 140.0 | 150.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 140.0 | 150.0 | end-users | True | 155590.0 | 86.7% | 100.0% | 13.3 |
| 150.0 | 161.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 150.0 | 161.0 | end-users | True | 166582.0 | 86.7% | 100.0% | 13.3 |
| 161.0 | 171.0 | app2 | True | 44714.0 | 13.3% | 26.8% | 13.5 |
| 161.0 | 171.0 | end-users | True | 121862.0 | 86.7% | 73.2% | -13.5 |
| 171.0 | 181.0 | app2 | True | 1358.0 | 13.3% | 0.9% | -12.4 |
| 171.0 | 181.0 | end-users | True | 151586.0 | 86.7% | 99.1% | 12.4 |
| 181.0 | 191.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 181.0 | 191.0 | end-users | True | 166414.0 | 86.7% | 100.0% | 13.3 |
| 191.0 | 201.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 191.0 | 201.0 | end-users | True | 174598.0 | 86.7% | 100.0% | 13.3 |
| 201.0 | 211.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 201.0 | 211.0 | end-users | True | 152884.0 | 86.7% | 100.0% | 13.3 |
| 211.0 | 221.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 211.0 | 221.0 | end-users | True | 167778.0 | 86.7% | 100.0% | 13.3 |
| 221.0 | 231.0 | app2 | True | 41914.0 | 13.3% | 25.4% | 12.0 |
| 221.0 | 231.0 | end-users | True | 123258.0 | 86.7% | 74.6% | -12.0 |
| 231.0 | 241.0 | app2 | True | 2706.0 | 13.3% | 1.8% | -11.6 |
| 231.0 | 241.0 | end-users | True | 151364.0 | 86.7% | 98.2% | 11.6 |
| 241.0 | 251.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 169210.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 43210.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 111002.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 274.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 274.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -13.2%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app2 | 260760 | 12996 | 273756.0 | 0.0% | 248876.0 | 286752.0 | -13.2% | False |
| end-users | 3580530 | 179136 | 3758389.0 | -0.0% | 3900976.0 | 3938802.0 | -1.0% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
