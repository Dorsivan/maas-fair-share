# Fairness benchmark: asymmetric-demand (uni139-asymmetric-demand-r3)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `asymmetric-demand` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T21:06:51Z` |
| Run end | `2026-11-01T21:11:03Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 5071 | 200=5070, 503=1 | 1.5 | 1.9 | 5428173.0 | 23.5% | 94.1% | 70.6 | 1.2s | 98.8% | 5071.0 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 97.3% | 0.0 |
| end-users | 65.0 | 2 | 280 | 200=280 | 1.7 | 2.0 | 340898.0 | 76.5% | 5.9% | -70.6 | 1.2s | 98.9% | 280.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 90.2% | 0.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 151518.0 | 23.5% | 94.9% | 71.4 |
| 0.0 | 10.0 | end-users | True | 8124.0 | 76.5% | 5.1% | -71.4 |
| 10.0 | 20.0 | app1 | True | 156948.0 | 23.5% | 92.8% | 69.3 |
| 10.0 | 20.0 | end-users | True | 12184.0 | 76.5% | 7.2% | -69.3 |
| 20.0 | 30.0 | app1 | True | 213722.0 | 23.5% | 93.5% | 70.0 |
| 20.0 | 30.0 | end-users | True | 14846.0 | 76.5% | 6.5% | -70.0 |
| 30.0 | 40.0 | app1 | True | 223176.0 | 23.5% | 94.3% | 70.7 |
| 30.0 | 40.0 | end-users | True | 13544.0 | 76.5% | 5.7% | -70.7 |
| 40.0 | 50.0 | app1 | True | 236754.0 | 23.5% | 94.6% | 71.1 |
| 40.0 | 50.0 | end-users | True | 13548.0 | 76.5% | 5.4% | -71.1 |
| 50.0 | 60.0 | app1 | True | 234078.0 | 23.5% | 94.0% | 70.5 |
| 50.0 | 60.0 | end-users | True | 14882.0 | 76.5% | 6.0% | -70.5 |
| 60.0 | 70.0 | app1 | True | 262266.0 | 23.5% | 94.6% | 71.1 |
| 60.0 | 70.0 | end-users | True | 14894.0 | 76.5% | 5.4% | -71.1 |
| 70.0 | 80.0 | app1 | True | 204174.0 | 23.5% | 93.8% | 70.3 |
| 70.0 | 80.0 | end-users | True | 13534.0 | 76.5% | 6.2% | -70.3 |
| 80.0 | 90.0 | app1 | True | 267990.0 | 23.5% | 94.7% | 71.2 |
| 80.0 | 90.0 | end-users | True | 14882.0 | 76.5% | 5.3% | -71.2 |
| 90.0 | 100.0 | app1 | True | 230080.0 | 23.5% | 94.5% | 70.9 |
| 90.0 | 100.0 | end-users | True | 13518.0 | 76.5% | 5.5% | -70.9 |
| 100.0 | 110.0 | app1 | True | 228516.0 | 23.5% | 93.9% | 70.3 |
| 100.0 | 110.0 | end-users | True | 14922.0 | 76.5% | 6.1% | -70.3 |
| 110.0 | 120.0 | app1 | True | 288060.0 | 23.5% | 94.7% | 71.1 |
| 110.0 | 120.0 | end-users | True | 16262.0 | 76.5% | 5.3% | -71.1 |
| 120.0 | 130.0 | app1 | True | 273252.0 | 23.5% | 94.4% | 70.9 |
| 120.0 | 130.0 | end-users | True | 16190.0 | 76.5% | 5.6% | -70.9 |
| 130.0 | 140.0 | app1 | True | 197732.0 | 23.5% | 92.4% | 68.9 |
| 130.0 | 140.0 | end-users | True | 16262.0 | 76.5% | 7.6% | -68.9 |
| 140.0 | 150.0 | app1 | True | 247508.0 | 23.5% | 93.8% | 70.3 |
| 140.0 | 150.0 | end-users | True | 16256.0 | 76.5% | 6.2% | -70.3 |
| 150.0 | 160.0 | app1 | True | 194882.0 | 23.5% | 95.4% | 71.8 |
| 150.0 | 160.0 | end-users | True | 9492.0 | 76.5% | 4.6% | -71.8 |
| 160.0 | 170.0 | app1 | True | 206888.0 | 23.5% | 93.3% | 69.8 |
| 160.0 | 170.0 | end-users | True | 14902.0 | 76.5% | 6.7% | -69.8 |
| 170.0 | 180.0 | app1 | True | 224698.0 | 23.5% | 94.3% | 70.8 |
| 170.0 | 180.0 | end-users | True | 13496.0 | 76.5% | 5.7% | -70.8 |
| 180.0 | 190.0 | app1 | True | 238058.0 | 23.5% | 93.6% | 70.1 |
| 180.0 | 190.0 | end-users | True | 16198.0 | 76.5% | 6.4% | -70.1 |
| 190.0 | 200.0 | app1 | True | 217964.0 | 23.5% | 93.1% | 69.6 |
| 190.0 | 200.0 | end-users | True | 16198.0 | 76.5% | 6.9% | -69.6 |
| 200.0 | 210.0 | app1 | True | 209868.0 | 23.5% | 93.9% | 70.4 |
| 200.0 | 210.0 | end-users | True | 13528.0 | 76.5% | 6.1% | -70.4 |
| 210.0 | 220.0 | app1 | True | 218029.0 | 23.5% | 94.2% | 70.6 |
| 210.0 | 220.0 | end-users | True | 13510.0 | 76.5% | 5.8% | -70.6 |
| 220.0 | 230.0 | app1 | True | 202850.0 | 23.5% | 94.3% | 70.8 |
| 220.0 | 230.0 | end-users | True | 12172.0 | 76.5% | 5.7% | -70.8 |
| 230.0 | 240.0 | app1 | True | 259948.0 | 23.5% | 94.6% | 71.1 |
| 230.0 | 240.0 | end-users | True | 14870.0 | 76.5% | 5.4% | -71.1 |
| 240.0 | 250.0 | app1 | False | 39214.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 2684.0 | n/a | n/a | n/a |
| 250.0 | 252.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 252.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -20.9%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 6236100 | 311433 | 6547533.0 | 0.0% | 5428173.0 | 6858966.0 | -20.9% | False |
| end-users | 344400 | 17185 | 361585.0 | 0.0% | 340898.0 | 378770.0 | -10.0% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
