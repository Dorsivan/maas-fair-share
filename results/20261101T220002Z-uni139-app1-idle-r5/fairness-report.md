# Fairness benchmark: app1-idle (uni139-app1-idle-r5)

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
| Run start | `2026-11-01T22:00:03Z` |
| Run end | `2026-11-01T22:04:36Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 98.8% | 0.0 |
| app2 | 10.0 | 32 | 433 | 200=433 | 19.8 | 20.6 | 551806.0 | 13.3% | 13.5% | 0.2 | 19.0s | 97.4% | 433.0 |
| end-users | 65.0 | 208 | 2754 | 200=2694, 500=60 | 19.9 | 20.5 | 3532006.0 | 86.7% | 86.5% | -0.2 | 19.0s | 98.9% | 2638.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 74452.0 | n/a | n/a | n/a | 0.1s | 98.1% | 56.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app2: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 0.0 | 0.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (28 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app2 | True | 8130.0 | 13.3% | 12.0% | -1.3 |
| 0.0 | 10.0 | end-users | True | 59526.0 | 86.7% | 88.0% | 1.3 |
| 10.0 | 20.0 | app2 | True | 18918.0 | 13.3% | 20.5% | 7.2 |
| 10.0 | 20.0 | end-users | True | 73144.0 | 86.7% | 79.5% | -7.2 |
| 20.0 | 30.0 | app2 | True | 20234.0 | 13.3% | 13.4% | 0.0 |
| 20.0 | 30.0 | end-users | True | 131270.0 | 86.7% | 86.6% | -0.0 |
| 30.0 | 40.0 | app2 | True | 24352.0 | 13.3% | 14.6% | 1.3 |
| 30.0 | 40.0 | end-users | True | 142176.0 | 86.7% | 85.4% | -1.3 |
| 40.0 | 50.0 | app2 | True | 21650.0 | 13.3% | 12.8% | -0.5 |
| 40.0 | 50.0 | end-users | True | 147476.0 | 86.7% | 87.2% | 0.5 |
| 50.0 | 60.0 | app2 | True | 20220.0 | 13.3% | 13.4% | 0.0 |
| 50.0 | 60.0 | end-users | True | 131180.0 | 86.7% | 86.6% | -0.0 |
| 60.0 | 70.0 | app2 | True | 22978.0 | 13.3% | 13.2% | -0.2 |
| 60.0 | 70.0 | end-users | True | 151420.0 | 86.7% | 86.8% | 0.2 |
| 70.0 | 80.0 | app2 | True | 22990.0 | 13.3% | 13.6% | 0.3 |
| 70.0 | 80.0 | end-users | True | 146180.0 | 86.7% | 86.4% | -0.3 |
| 80.0 | 90.0 | app2 | True | 21564.0 | 13.3% | 13.4% | 0.1 |
| 80.0 | 90.0 | end-users | True | 139276.0 | 86.7% | 86.6% | -0.1 |
| 90.0 | 100.0 | app2 | True | 20330.0 | 13.3% | 12.7% | -0.6 |
| 90.0 | 100.0 | end-users | True | 139424.0 | 86.7% | 87.3% | 0.6 |
| 100.0 | 110.0 | app2 | True | 23024.0 | 13.3% | 13.6% | 0.3 |
| 100.0 | 110.0 | end-users | True | 146150.0 | 86.7% | 86.4% | -0.3 |
| 110.0 | 120.0 | app2 | True | 23042.0 | 13.3% | 13.6% | 0.3 |
| 110.0 | 120.0 | end-users | True | 146082.0 | 86.7% | 86.4% | -0.3 |
| 120.0 | 130.0 | app2 | True | 20304.0 | 13.3% | 13.4% | 0.1 |
| 120.0 | 130.0 | end-users | True | 131192.0 | 86.7% | 86.6% | -0.1 |
| 130.0 | 140.0 | app2 | True | 21664.0 | 13.3% | 13.1% | -0.2 |
| 130.0 | 140.0 | end-users | True | 143364.0 | 86.7% | 86.9% | 0.2 |
| 140.0 | 150.0 | app2 | True | 20268.0 | 13.3% | 12.8% | -0.5 |
| 140.0 | 150.0 | end-users | True | 137912.0 | 86.7% | 87.2% | 0.5 |
| 150.0 | 161.0 | app2 | True | 22930.0 | 13.3% | 13.9% | 0.6 |
| 150.0 | 161.0 | end-users | True | 142192.0 | 86.7% | 86.1% | -0.6 |
| 161.0 | 171.0 | app2 | True | 22986.0 | 13.3% | 13.3% | -0.0 |
| 161.0 | 171.0 | end-users | True | 150008.0 | 86.7% | 86.7% | 0.0 |
| 171.0 | 181.0 | app2 | True | 21680.0 | 13.3% | 13.0% | -0.3 |
| 171.0 | 181.0 | end-users | True | 144718.0 | 86.7% | 87.0% | 0.3 |
| 181.0 | 191.0 | app2 | True | 21638.0 | 13.3% | 14.0% | 0.7 |
| 181.0 | 191.0 | end-users | True | 132580.0 | 86.7% | 86.0% | -0.7 |
| 191.0 | 201.0 | app2 | True | 21682.0 | 13.3% | 13.0% | -0.3 |
| 191.0 | 201.0 | end-users | True | 144730.0 | 86.7% | 87.0% | 0.3 |
| 201.0 | 211.0 | app2 | True | 20296.0 | 13.3% | 13.1% | -0.3 |
| 201.0 | 211.0 | end-users | True | 135198.0 | 86.7% | 86.9% | 0.3 |
| 211.0 | 221.0 | app2 | True | 22972.0 | 13.3% | 13.6% | 0.3 |
| 211.0 | 221.0 | end-users | True | 146120.0 | 86.7% | 86.4% | -0.3 |
| 221.0 | 231.0 | app2 | True | 22998.0 | 13.3% | 13.6% | 0.3 |
| 221.0 | 231.0 | end-users | True | 146000.0 | 86.7% | 86.4% | -0.3 |
| 231.0 | 241.0 | app2 | True | 22976.0 | 13.3% | 13.3% | -0.1 |
| 231.0 | 241.0 | end-users | True | 150006.0 | 86.7% | 86.7% | 0.1 |
| 241.0 | 251.0 | app2 | False | 20290.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 131228.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 21690.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 143454.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 273.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 273.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app2 | 532590 | 26540 | 559130.0 | 0.0% | 551806.0 | 585670.0 | -5.8% | True |
| end-users | 3313620 | 165335 | 3406620.0 | -2.1% | 3532006.0 | 3644290.0 | -3.1% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
