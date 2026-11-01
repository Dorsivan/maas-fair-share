# Fairness benchmark: asymmetric-demand (uni139-asymmetric-demand-r2)

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
| Run start | `2026-11-01T21:02:37Z` |
| Run end | `2026-11-01T21:06:49Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 5090 | 200=5090 | 1.5 | 1.8 | 5057610.0 | 23.5% | 93.9% | 70.4 | 1.0s | 98.8% | 5090.0 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 97.3% | 0.0 |
| end-users | 65.0 | 2 | 280 | 200=280 | 1.7 | 2.0 | 327416.0 | 76.5% | 6.1% | -70.4 | 1.0s | 98.9% | 280.0 |
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
| 0.0 | 10.0 | app1 | True | 127084.0 | 23.5% | 95.0% | 71.4 |
| 0.0 | 10.0 | end-users | True | 6758.0 | 76.5% | 5.0% | -71.4 |
| 10.0 | 20.0 | app1 | True | 182462.0 | 23.5% | 93.1% | 69.6 |
| 10.0 | 20.0 | end-users | True | 13554.0 | 76.5% | 6.9% | -69.6 |
| 20.0 | 30.0 | app1 | True | 140520.0 | 23.5% | 92.8% | 69.3 |
| 20.0 | 30.0 | end-users | True | 10850.0 | 76.5% | 7.2% | -69.3 |
| 30.0 | 40.0 | app1 | True | 256956.0 | 23.5% | 93.6% | 70.1 |
| 30.0 | 40.0 | end-users | True | 17582.0 | 76.5% | 6.4% | -70.1 |
| 40.0 | 50.0 | app1 | True | 269296.0 | 23.5% | 94.3% | 70.8 |
| 40.0 | 50.0 | end-users | True | 16214.0 | 76.5% | 5.7% | -70.8 |
| 50.0 | 60.0 | app1 | True | 221852.0 | 23.5% | 94.3% | 70.7 |
| 50.0 | 60.0 | end-users | True | 13488.0 | 76.5% | 5.7% | -70.7 |
| 60.0 | 70.0 | app1 | True | 206930.0 | 23.5% | 92.7% | 69.2 |
| 60.0 | 70.0 | end-users | True | 16214.0 | 76.5% | 7.3% | -69.2 |
| 70.0 | 80.0 | app1 | True | 202916.0 | 23.5% | 93.8% | 70.2 |
| 70.0 | 80.0 | end-users | True | 13526.0 | 76.5% | 6.2% | -70.2 |
| 80.0 | 90.0 | app1 | True | 227140.0 | 23.5% | 94.4% | 70.9 |
| 80.0 | 90.0 | end-users | True | 13504.0 | 76.5% | 5.6% | -70.9 |
| 90.0 | 100.0 | app1 | True | 186710.0 | 23.5% | 93.9% | 70.4 |
| 90.0 | 100.0 | end-users | True | 12124.0 | 76.5% | 6.1% | -70.4 |
| 100.0 | 110.0 | app1 | True | 220342.0 | 23.5% | 93.7% | 70.1 |
| 100.0 | 110.0 | end-users | True | 14912.0 | 76.5% | 6.3% | -70.1 |
| 110.0 | 120.0 | app1 | True | 180028.0 | 23.5% | 93.0% | 69.5 |
| 110.0 | 120.0 | end-users | True | 13562.0 | 76.5% | 7.0% | -69.5 |
| 120.0 | 130.0 | app1 | True | 189680.0 | 23.5% | 94.0% | 70.4 |
| 120.0 | 130.0 | end-users | True | 12196.0 | 76.5% | 6.0% | -70.4 |
| 130.0 | 140.0 | app1 | True | 263724.0 | 23.5% | 94.2% | 70.7 |
| 130.0 | 140.0 | end-users | True | 16210.0 | 76.5% | 5.8% | -70.7 |
| 140.0 | 150.0 | app1 | True | 175782.0 | 23.5% | 93.5% | 70.0 |
| 140.0 | 150.0 | end-users | True | 12202.0 | 76.5% | 6.5% | -70.0 |
| 150.0 | 160.0 | app1 | True | 202962.0 | 23.5% | 94.3% | 70.8 |
| 150.0 | 160.0 | end-users | True | 12168.0 | 76.5% | 5.7% | -70.8 |
| 160.0 | 170.0 | app1 | True | 236706.0 | 23.5% | 93.6% | 70.1 |
| 160.0 | 170.0 | end-users | True | 16216.0 | 76.5% | 6.4% | -70.1 |
| 170.0 | 180.0 | app1 | True | 262486.0 | 23.5% | 94.2% | 70.6 |
| 170.0 | 180.0 | end-users | True | 16282.0 | 76.5% | 5.8% | -70.6 |
| 180.0 | 190.0 | app1 | True | 137796.0 | 23.5% | 94.5% | 70.9 |
| 180.0 | 190.0 | end-users | True | 8094.0 | 76.5% | 5.5% | -70.9 |
| 190.0 | 200.0 | app1 | True | 236730.0 | 23.5% | 94.1% | 70.6 |
| 190.0 | 200.0 | end-users | True | 14892.0 | 76.5% | 5.9% | -70.6 |
| 200.0 | 210.0 | app1 | True | 205690.0 | 23.5% | 95.0% | 71.5 |
| 200.0 | 210.0 | end-users | True | 10844.0 | 76.5% | 5.0% | -71.5 |
| 210.0 | 220.0 | app1 | True | 273194.0 | 23.5% | 94.4% | 70.9 |
| 210.0 | 220.0 | end-users | True | 16240.0 | 76.5% | 5.6% | -70.9 |
| 220.0 | 230.0 | app1 | True | 175904.0 | 23.5% | 94.2% | 70.7 |
| 220.0 | 230.0 | end-users | True | 10820.0 | 76.5% | 5.8% | -70.7 |
| 230.0 | 240.0 | app1 | True | 244918.0 | 23.5% | 93.8% | 70.2 |
| 230.0 | 240.0 | end-users | True | 16264.0 | 76.5% | 6.2% | -70.2 |
| 240.0 | 250.0 | app1 | False | 29802.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 2700.0 | n/a | n/a | n/a |
| 250.0 | 252.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 252.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -26.5%
- end-users exceeded the 10% ledger tolerance: cost -13.6%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 6260700 | 312502 | 6573202.0 | 0.0% | 5057610.0 | 6885704.0 | -26.5% | False |
| end-users | 344400 | 17196 | 361596.0 | 0.0% | 327416.0 | 378792.0 | -13.6% | False |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
