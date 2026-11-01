# Fairness benchmark: asymmetric-demand (uni139-asymmetric-demand-r4)

**Verdict: UNCONTENDED** -- every offered group's `contended_seconds_total` delta stayed under 1s, so the pool was never actually contended. Not scored against the 10-point weighted-split threshold; see docs/runbook.md.

- every offered group's contended_seconds_total delta stayed under 1s (app1=0.98s, end-users=0.98s) -- an order of magnitude below the ~9s a genuinely-contending tenant accrues in a 240s full-contention run (docs/runbook.md), so nobody was ever backlogged alongside anyone else and the weighted-split deviation check does not apply

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
| Run start | `2026-11-01T21:11:05Z` |
| Run end | `2026-11-01T21:15:17Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 5109 | 200=5109 | 1.5 | 1.8 | 4922332.0 | 23.5% | 93.6% | 70.0 | 1.0s | 98.8% | 5109.0 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 97.3% | 0.0 |
| end-users | 65.0 | 2 | 282 | 200=282 | 1.7 | 2.0 | 338268.0 | 76.5% | 6.4% | -70.0 | 1.0s | 98.9% | 282.0 |
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
| 0.0 | 10.0 | app1 | True | 104122.0 | 23.5% | 92.8% | 69.2 |
| 0.0 | 10.0 | end-users | True | 8124.0 | 76.5% | 7.2% | -69.2 |
| 10.0 | 20.0 | app1 | True | 217740.0 | 23.5% | 94.1% | 70.6 |
| 10.0 | 20.0 | end-users | True | 13542.0 | 76.5% | 5.9% | -70.6 |
| 20.0 | 30.0 | app1 | True | 201504.0 | 23.5% | 93.1% | 69.6 |
| 20.0 | 30.0 | end-users | True | 14902.0 | 76.5% | 6.9% | -69.6 |
| 30.0 | 40.0 | app1 | True | 162270.0 | 23.5% | 92.3% | 68.8 |
| 30.0 | 40.0 | end-users | True | 13552.0 | 76.5% | 7.7% | -68.8 |
| 40.0 | 50.0 | app1 | True | 235280.0 | 23.5% | 94.0% | 70.5 |
| 40.0 | 50.0 | end-users | True | 14902.0 | 76.5% | 6.0% | -70.5 |
| 50.0 | 60.0 | app1 | True | 220538.0 | 23.5% | 94.2% | 70.7 |
| 50.0 | 60.0 | end-users | True | 13524.0 | 76.5% | 5.8% | -70.7 |
| 60.0 | 70.0 | app1 | True | 271948.0 | 23.5% | 94.4% | 70.8 |
| 60.0 | 70.0 | end-users | True | 16258.0 | 76.5% | 5.6% | -70.8 |
| 70.0 | 80.0 | app1 | True | 242024.0 | 23.5% | 93.7% | 70.2 |
| 70.0 | 80.0 | end-users | True | 16230.0 | 76.5% | 6.3% | -70.2 |
| 80.0 | 90.0 | app1 | True | 179906.0 | 23.5% | 93.0% | 69.5 |
| 80.0 | 90.0 | end-users | True | 13528.0 | 76.5% | 7.0% | -69.5 |
| 90.0 | 100.0 | app1 | True | 193578.0 | 23.5% | 92.9% | 69.3 |
| 90.0 | 100.0 | end-users | True | 14904.0 | 76.5% | 7.1% | -69.3 |
| 100.0 | 110.0 | app1 | True | 157058.0 | 23.5% | 92.8% | 69.3 |
| 100.0 | 110.0 | end-users | True | 12178.0 | 76.5% | 7.2% | -69.3 |
| 110.0 | 120.0 | app1 | True | 221762.0 | 23.5% | 93.2% | 69.7 |
| 110.0 | 120.0 | end-users | True | 16182.0 | 76.5% | 6.8% | -69.7 |
| 120.0 | 130.0 | app1 | True | 215134.0 | 23.5% | 93.6% | 70.0 |
| 120.0 | 130.0 | end-users | True | 14828.0 | 76.5% | 6.4% | -70.0 |
| 130.0 | 140.0 | app1 | True | 185308.0 | 23.5% | 93.8% | 70.3 |
| 130.0 | 140.0 | end-users | True | 12172.0 | 76.5% | 6.2% | -70.3 |
| 140.0 | 150.0 | app1 | True | 193492.0 | 23.5% | 92.9% | 69.3 |
| 140.0 | 150.0 | end-users | True | 14880.0 | 76.5% | 7.1% | -69.3 |
| 150.0 | 160.0 | app1 | True | 261178.0 | 23.5% | 95.1% | 71.5 |
| 150.0 | 160.0 | end-users | True | 13550.0 | 76.5% | 4.9% | -71.5 |
| 160.0 | 170.0 | app1 | True | 216496.0 | 23.5% | 93.0% | 69.5 |
| 160.0 | 170.0 | end-users | True | 16214.0 | 76.5% | 7.0% | -69.5 |
| 170.0 | 180.0 | app1 | True | 214932.0 | 23.5% | 94.1% | 70.5 |
| 170.0 | 180.0 | end-users | True | 13546.0 | 76.5% | 5.9% | -70.5 |
| 180.0 | 190.0 | app1 | True | 201548.0 | 23.5% | 93.7% | 70.2 |
| 180.0 | 190.0 | end-users | True | 13548.0 | 76.5% | 6.3% | -70.2 |
| 190.0 | 200.0 | app1 | True | 206968.0 | 23.5% | 92.7% | 69.2 |
| 190.0 | 200.0 | end-users | True | 16246.0 | 76.5% | 7.3% | -69.2 |
| 200.0 | 210.0 | app1 | True | 216522.0 | 23.5% | 94.1% | 70.6 |
| 200.0 | 210.0 | end-users | True | 13542.0 | 76.5% | 5.9% | -70.6 |
| 210.0 | 220.0 | app1 | True | 227192.0 | 23.5% | 93.3% | 69.8 |
| 210.0 | 220.0 | end-users | True | 16222.0 | 76.5% | 6.7% | -69.8 |
| 220.0 | 230.0 | app1 | True | 240594.0 | 23.5% | 94.2% | 70.7 |
| 220.0 | 230.0 | end-users | True | 14862.0 | 76.5% | 5.8% | -70.7 |
| 230.0 | 240.0 | app1 | True | 128524.0 | 23.5% | 92.2% | 68.7 |
| 230.0 | 240.0 | end-users | True | 10832.0 | 76.5% | 7.8% | -68.7 |
| 240.0 | 250.0 | app1 | False | 6714.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 252.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 252.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -28.8%
- end-users exceeded the 10% ledger tolerance: cost -11.4%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 6284070 | 313008 | 6597078.0 | 0.0% | 4922332.0 | 6910086.0 | -28.8% | False |
| end-users | 346860 | 17370 | 364230.0 | 0.0% | 338268.0 | 381600.0 | -11.4% | False |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
