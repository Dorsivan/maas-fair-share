# Fairness benchmark: app1-idle (app1-idle)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-idle` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T17:28:54Z` |
| Run end | `2026-11-01T17:33:27Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a |
| app2 | 10.0 | 32 | 297 | 200=297 | 19.9 | 101.8 | 374652.0 | 13.3% | 8.9% | -4.5 |
| end-users | 65.0 | 208 | 2895 | 200=2867, 500=28 | 18.8 | 20.4 | 3845988.0 | 86.7% | 91.1% | 4.5 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 4050.0 | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app2: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 101.0 | 101.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (28 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app2 | True | 21618.0 | 13.3% | 21.0% | 7.7 |
| 0.0 | 10.0 | end-users | True | 81108.0 | 86.7% | 79.0% | -7.7 |
| 10.0 | 20.0 | app2 | True | 5414.0 | 13.3% | 3.2% | -10.1 |
| 10.0 | 20.0 | end-users | True | 163776.0 | 86.7% | 96.8% | 10.1 |
| 20.0 | 30.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 20.0 | 30.0 | end-users | True | 151406.0 | 86.7% | 100.0% | 13.3 |
| 30.0 | 40.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 30.0 | 40.0 | end-users | True | 173114.0 | 86.7% | 100.0% | 13.3 |
| 40.0 | 51.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 40.0 | 51.0 | end-users | True | 167738.0 | 86.7% | 100.0% | 13.3 |
| 51.0 | 61.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 51.0 | 61.0 | end-users | True | 163780.0 | 86.7% | 100.0% | 13.3 |
| 61.0 | 71.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 61.0 | 71.0 | end-users | True | 158358.0 | 86.7% | 100.0% | 13.3 |
| 71.0 | 81.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 71.0 | 81.0 | end-users | True | 171860.0 | 86.7% | 100.0% | 13.3 |
| 81.0 | 91.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 81.0 | 91.0 | end-users | True | 173042.0 | 86.7% | 100.0% | 13.3 |
| 91.0 | 101.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 91.0 | 101.0 | end-users | True | 152644.0 | 86.7% | 100.0% | 13.3 |
| 101.0 | 111.0 | app2 | True | 18922.0 | 13.3% | 11.2% | -2.1 |
| 101.0 | 111.0 | end-users | True | 150128.0 | 86.7% | 88.8% | 2.1 |
| 111.0 | 121.0 | app2 | True | 21566.0 | 13.3% | 12.6% | -0.8 |
| 111.0 | 121.0 | end-users | True | 150178.0 | 86.7% | 87.4% | 0.8 |
| 121.0 | 131.0 | app2 | True | 21674.0 | 13.3% | 12.9% | -0.4 |
| 121.0 | 131.0 | end-users | True | 146294.0 | 86.7% | 87.1% | 0.4 |
| 131.0 | 141.0 | app2 | True | 21706.0 | 13.3% | 14.2% | 0.9 |
| 131.0 | 141.0 | end-users | True | 131176.0 | 86.7% | 85.8% | -0.9 |
| 141.0 | 151.0 | app2 | True | 21652.0 | 13.3% | 12.8% | -0.5 |
| 141.0 | 151.0 | end-users | True | 147518.0 | 86.7% | 87.2% | 0.5 |
| 151.0 | 161.0 | app2 | True | 23014.0 | 13.3% | 13.6% | 0.3 |
| 151.0 | 161.0 | end-users | True | 145994.0 | 86.7% | 86.4% | -0.3 |
| 161.0 | 171.0 | app2 | True | 22980.0 | 13.3% | 13.6% | 0.3 |
| 161.0 | 171.0 | end-users | True | 146112.0 | 86.7% | 86.4% | -0.3 |
| 171.0 | 181.0 | app2 | True | 20300.0 | 13.3% | 13.2% | -0.2 |
| 171.0 | 181.0 | end-users | True | 133834.0 | 86.7% | 86.8% | 0.2 |
| 181.0 | 191.0 | app2 | True | 24360.0 | 13.3% | 14.4% | 1.1 |
| 181.0 | 191.0 | end-users | True | 144794.0 | 86.7% | 85.6% | -1.1 |
| 191.0 | 201.0 | app2 | True | 21626.0 | 13.3% | 12.8% | -0.6 |
| 191.0 | 201.0 | end-users | True | 147568.0 | 86.7% | 87.2% | 0.6 |
| 201.0 | 211.0 | app2 | True | 20290.0 | 13.3% | 13.5% | 0.2 |
| 201.0 | 211.0 | end-users | True | 129994.0 | 86.7% | 86.5% | -0.2 |
| 211.0 | 221.0 | app2 | True | 21634.0 | 13.3% | 13.0% | -0.3 |
| 211.0 | 221.0 | end-users | True | 144764.0 | 86.7% | 87.0% | 0.3 |
| 221.0 | 231.0 | app2 | True | 23030.0 | 13.3% | 13.4% | 0.1 |
| 221.0 | 231.0 | end-users | True | 148836.0 | 86.7% | 86.6% | -0.1 |
| 231.0 | 241.0 | app2 | True | 20266.0 | 13.3% | 13.3% | -0.1 |
| 231.0 | 241.0 | end-users | True | 132516.0 | 86.7% | 86.7% | 0.1 |
| 241.0 | 251.0 | app2 | False | 22998.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 144778.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 21602.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 144678.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 273.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 273.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation.
