# Fairness benchmark: asymmetric-demand (uni139-asymmetric-demand-r1)

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
| Run start | `2026-11-01T20:58:23Z` |
| Run end | `2026-11-01T21:02:35Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 5113 | 200=5099, 500=14 | 1.5 | 1.9 | 5731404.0 | 23.5% | 94.1% | 70.6 | 1.2s | 98.8% | 5099.0 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 97.3% | 0.0 |
| end-users | 65.0 | 2 | 280 | 200=279, 500=1 | 1.7 | 2.0 | 358598.0 | 76.5% | 5.9% | -70.6 | 1.2s | 98.9% | 279.0 |
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
| 0.0 | 10.0 | app1 | True | 127156.0 | 23.5% | 92.2% | 68.6 |
| 0.0 | 10.0 | end-users | True | 10818.0 | 76.5% | 7.8% | -68.6 |
| 10.0 | 20.0 | app1 | True | 257056.0 | 23.5% | 94.5% | 71.0 |
| 10.0 | 20.0 | end-users | True | 14908.0 | 76.5% | 5.5% | -71.0 |
| 20.0 | 30.0 | app1 | True | 268232.0 | 23.5% | 94.3% | 70.8 |
| 20.0 | 30.0 | end-users | True | 16230.0 | 76.5% | 5.7% | -70.8 |
| 30.0 | 40.0 | app1 | True | 250164.0 | 23.5% | 94.4% | 70.9 |
| 30.0 | 40.0 | end-users | True | 14880.0 | 76.5% | 5.6% | -70.9 |
| 40.0 | 50.0 | app1 | True | 244876.0 | 23.5% | 93.8% | 70.2 |
| 40.0 | 50.0 | end-users | True | 16274.0 | 76.5% | 6.2% | -70.2 |
| 50.0 | 60.0 | app1 | True | 205572.0 | 23.5% | 94.4% | 70.9 |
| 50.0 | 60.0 | end-users | True | 12102.0 | 76.5% | 5.6% | -70.9 |
| 60.0 | 70.0 | app1 | True | 256980.0 | 23.5% | 94.5% | 71.0 |
| 60.0 | 70.0 | end-users | True | 14862.0 | 76.5% | 5.5% | -71.0 |
| 70.0 | 80.0 | app1 | True | 275890.0 | 23.5% | 94.9% | 71.4 |
| 70.0 | 80.0 | end-users | True | 14852.0 | 76.5% | 5.1% | -71.4 |
| 80.0 | 90.0 | app1 | True | 244850.0 | 23.5% | 94.3% | 70.7 |
| 80.0 | 90.0 | end-users | True | 14886.0 | 76.5% | 5.7% | -70.7 |
| 90.0 | 100.0 | app1 | True | 258344.0 | 23.5% | 94.5% | 71.0 |
| 90.0 | 100.0 | end-users | True | 14918.0 | 76.5% | 5.5% | -71.0 |
| 100.0 | 110.0 | app1 | True | 240992.0 | 23.5% | 93.7% | 70.2 |
| 100.0 | 110.0 | end-users | True | 16234.0 | 76.5% | 6.3% | -70.2 |
| 110.0 | 120.0 | app1 | True | 244634.0 | 23.5% | 94.3% | 70.7 |
| 110.0 | 120.0 | end-users | True | 14922.0 | 76.5% | 5.7% | -70.7 |
| 120.0 | 130.0 | app1 | True | 231286.0 | 23.5% | 93.4% | 69.9 |
| 120.0 | 130.0 | end-users | True | 16280.0 | 76.5% | 6.6% | -69.9 |
| 130.0 | 140.0 | app1 | True | 240826.0 | 23.5% | 94.2% | 70.7 |
| 130.0 | 140.0 | end-users | True | 14872.0 | 76.5% | 5.8% | -70.7 |
| 140.0 | 150.0 | app1 | True | 155384.0 | 23.5% | 94.3% | 70.7 |
| 140.0 | 150.0 | end-users | True | 9470.0 | 76.5% | 5.7% | -70.7 |
| 150.0 | 160.0 | app1 | True | 259756.0 | 23.5% | 94.1% | 70.6 |
| 150.0 | 160.0 | end-users | True | 16240.0 | 76.5% | 5.9% | -70.6 |
| 160.0 | 170.0 | app1 | True | 260930.0 | 23.5% | 94.6% | 71.1 |
| 160.0 | 170.0 | end-users | True | 14898.0 | 76.5% | 5.4% | -71.1 |
| 170.0 | 180.0 | app1 | True | 281498.0 | 23.5% | 94.5% | 71.0 |
| 170.0 | 180.0 | end-users | True | 16252.0 | 76.5% | 5.5% | -71.0 |
| 180.0 | 190.0 | app1 | True | 246176.0 | 23.5% | 94.3% | 70.8 |
| 180.0 | 190.0 | end-users | True | 14866.0 | 76.5% | 5.7% | -70.8 |
| 190.0 | 200.0 | app1 | True | 271896.0 | 23.5% | 94.8% | 71.3 |
| 190.0 | 200.0 | end-users | True | 14918.0 | 76.5% | 5.2% | -71.3 |
| 200.0 | 210.0 | app1 | True | 274448.0 | 23.5% | 94.4% | 70.9 |
| 200.0 | 210.0 | end-users | True | 16186.0 | 76.5% | 5.6% | -70.9 |
| 210.0 | 220.0 | app1 | True | 178750.0 | 23.5% | 93.0% | 69.4 |
| 210.0 | 220.0 | end-users | True | 13550.0 | 76.5% | 7.0% | -69.4 |
| 220.0 | 230.0 | app1 | True | 206898.0 | 23.5% | 92.7% | 69.2 |
| 220.0 | 230.0 | end-users | True | 16252.0 | 76.5% | 7.3% | -69.2 |
| 230.0 | 240.0 | app1 | True | 212370.0 | 23.5% | 92.9% | 69.4 |
| 230.0 | 240.0 | end-users | True | 16212.0 | 76.5% | 7.1% | -69.4 |
| 240.0 | 250.0 | app1 | False | 36440.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 2716.0 | n/a | n/a | n/a |
| 250.0 | 252.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 252.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -16.9%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 6271770 | 313033 | 6584803.0 | 0.0% | 5731404.0 | 6897836.0 | -16.9% | False |
| end-users | 343170 | 17179 | 360349.0 | 0.0% | 358598.0 | 377528.0 | -5.0% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
