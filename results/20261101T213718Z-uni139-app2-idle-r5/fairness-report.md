# Fairness benchmark: app2-idle (uni139-app2-idle-r5)

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
| Run start | `2026-11-01T21:37:19Z` |
| Run end | `2026-11-01T21:41:43Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 680 | 200=680 | 10.9 | 18.4 | 866762.0 | 23.5% | 20.6% | -2.9 | 1.3s | 98.8% | 680.0 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 97.3% | 0.0 |
| end-users | 65.0 | 104 | 2483 | 200=2483 | 10.9 | 12.3 | 3334378.0 | 76.5% | 79.4% | 2.9 | 1.3s | 98.9% | 2483.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 91.3% | 0.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 231.0 | 231.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 5432.0 | 23.5% | 5.1% | -18.4 |
| 0.0 | 10.0 | end-users | True | 101332.0 | 76.5% | 94.9% | 18.4 |
| 10.0 | 20.0 | app1 | True | 58184.0 | 23.5% | 34.4% | 10.9 |
| 10.0 | 20.0 | end-users | True | 110992.0 | 76.5% | 65.6% | -10.9 |
| 20.0 | 30.0 | app1 | True | 44666.0 | 23.5% | 26.4% | 2.9 |
| 20.0 | 30.0 | end-users | True | 124644.0 | 76.5% | 73.6% | -2.9 |
| 30.0 | 40.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 30.0 | 40.0 | end-users | True | 166462.0 | 76.5% | 100.0% | 23.5 |
| 40.0 | 51.0 | app1 | True | 62256.0 | 23.5% | 36.2% | 12.7 |
| 40.0 | 51.0 | end-users | True | 109556.0 | 76.5% | 63.8% | -12.7 |
| 51.0 | 61.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 51.0 | 61.0 | end-users | True | 170492.0 | 76.5% | 100.0% | 23.5 |
| 61.0 | 71.0 | app1 | True | 62202.0 | 23.5% | 37.4% | 13.8 |
| 61.0 | 71.0 | end-users | True | 104236.0 | 76.5% | 62.6% | -13.8 |
| 71.0 | 81.0 | app1 | True | 41900.0 | 23.5% | 24.6% | 1.1 |
| 71.0 | 81.0 | end-users | True | 128312.0 | 76.5% | 75.4% | -1.1 |
| 81.0 | 91.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 81.0 | 91.0 | end-users | True | 167670.0 | 76.5% | 100.0% | 23.5 |
| 91.0 | 101.0 | app1 | True | 64812.0 | 23.5% | 37.4% | 13.9 |
| 91.0 | 101.0 | end-users | True | 108282.0 | 76.5% | 62.6% | -13.9 |
| 101.0 | 111.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 101.0 | 111.0 | end-users | True | 166504.0 | 76.5% | 100.0% | 23.5 |
| 111.0 | 121.0 | app1 | True | 64802.0 | 23.5% | 38.1% | 14.5 |
| 111.0 | 121.0 | end-users | True | 105386.0 | 76.5% | 61.9% | -14.5 |
| 121.0 | 131.0 | app1 | True | 41902.0 | 23.5% | 24.8% | 1.3 |
| 121.0 | 131.0 | end-users | True | 127184.0 | 76.5% | 75.2% | -1.3 |
| 131.0 | 141.0 | app1 | True | 16244.0 | 23.5% | 9.7% | -13.8 |
| 131.0 | 141.0 | end-users | True | 151316.0 | 76.5% | 90.3% | 13.8 |
| 141.0 | 151.0 | app1 | True | 47338.0 | 23.5% | 27.6% | 4.1 |
| 141.0 | 151.0 | end-users | True | 124272.0 | 76.5% | 72.4% | -4.1 |
| 151.0 | 161.0 | app1 | True | 41940.0 | 23.5% | 25.0% | 1.5 |
| 151.0 | 161.0 | end-users | True | 125848.0 | 76.5% | 75.0% | -1.5 |
| 161.0 | 171.0 | app1 | True | 46038.0 | 23.5% | 26.2% | 2.7 |
| 161.0 | 171.0 | end-users | True | 129798.0 | 76.5% | 73.8% | -2.7 |
| 171.0 | 181.0 | app1 | True | 37842.0 | 23.5% | 21.2% | -2.3 |
| 171.0 | 181.0 | end-users | True | 140788.0 | 76.5% | 78.8% | 2.3 |
| 181.0 | 191.0 | app1 | True | 20250.0 | 23.5% | 12.1% | -11.5 |
| 181.0 | 191.0 | end-users | True | 147416.0 | 76.5% | 87.9% | 11.5 |
| 191.0 | 201.0 | app1 | True | 59530.0 | 23.5% | 35.5% | 12.0 |
| 191.0 | 201.0 | end-users | True | 108222.0 | 76.5% | 64.5% | -12.0 |
| 201.0 | 211.0 | app1 | True | 2692.0 | 23.5% | 1.6% | -21.9 |
| 201.0 | 211.0 | end-users | True | 166448.0 | 76.5% | 98.4% | 21.9 |
| 211.0 | 221.0 | app1 | True | 63614.0 | 23.5% | 37.0% | 13.5 |
| 211.0 | 221.0 | end-users | True | 108310.0 | 76.5% | 63.0% | -13.5 |
| 221.0 | 231.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 221.0 | 231.0 | end-users | True | 163642.0 | 76.5% | 100.0% | 23.5 |
| 231.0 | 241.0 | app1 | True | 43268.0 | 23.5% | 25.4% | 1.9 |
| 231.0 | 241.0 | end-users | True | 127084.0 | 76.5% | 74.6% | -1.9 |
| 241.0 | 251.0 | app1 | False | 41850.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 129912.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 20270.0 | n/a | n/a | n/a |
| 261.0 | 264.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 264.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 836400 | 41583 | 877983.0 | 0.0% | 866762.0 | 919566.0 | -5.7% | True |
| end-users | 3054090 | 152328 | 3206418.0 | 0.0% | 3334378.0 | 3358746.0 | -0.7% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
