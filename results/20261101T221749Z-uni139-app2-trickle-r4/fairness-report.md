# Fairness benchmark: app2-trickle (uni139-app2-trickle-r4)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app2-trickle` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T22:17:51Z` |
| Run end | `2026-11-01T22:22:14Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 641 | 200=641 | 11.2 | 18.7 | 816970.0 | 23.5% | 19.7% | -3.8 | 1.6s | 98.8% | 641.0 |
| app2 | 10.0 | 2 | 50 | 200=50 | 11.0 | 15.2 | 64918.0 | n/a | n/a | n/a | 1.6s | 97.4% | 50.0 |
| end-users | 65.0 | 104 | 2445 | 200=2445 | 11.1 | 12.0 | 3263076.0 | 76.5% | 78.7% | 2.3 | 1.6s | 98.9% | 2445.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 98.1% | 0.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 2716.0 | 21.1% | 2.9% | -18.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 90490.0 | 68.4% | 97.1% | 28.7 |
| 10.0 | 20.0 | app1 | True | 40464.0 | 21.1% | 23.6% | 2.5 |
| 10.0 | 20.0 | app2 | True | 2692.0 | 10.5% | 1.6% | -9.0 |
| 10.0 | 20.0 | end-users | True | 128452.0 | 68.4% | 74.9% | 6.4 |
| 20.0 | 30.0 | app1 | True | 43328.0 | 21.1% | 26.1% | 5.0 |
| 20.0 | 30.0 | app2 | True | 4030.0 | 10.5% | 2.4% | -8.1 |
| 20.0 | 30.0 | end-users | True | 118968.0 | 68.4% | 71.5% | 3.1 |
| 30.0 | 40.0 | app1 | True | 40610.0 | 21.1% | 24.0% | 3.0 |
| 30.0 | 40.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 30.0 | 40.0 | end-users | True | 127144.0 | 68.4% | 75.2% | 6.8 |
| 40.0 | 50.0 | app1 | True | 5422.0 | 21.1% | 3.2% | -17.8 |
| 40.0 | 50.0 | app2 | True | 2702.0 | 10.5% | 1.6% | -8.9 |
| 40.0 | 50.0 | end-users | True | 159466.0 | 68.4% | 95.2% | 26.7 |
| 50.0 | 60.0 | app1 | True | 43280.0 | 21.1% | 26.0% | 4.9 |
| 50.0 | 60.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 50.0 | 60.0 | end-users | True | 120466.0 | 68.4% | 72.4% | 3.9 |
| 60.0 | 70.0 | app1 | True | 44616.0 | 21.1% | 26.8% | 5.8 |
| 60.0 | 70.0 | app2 | True | 4074.0 | 10.5% | 2.5% | -8.1 |
| 60.0 | 70.0 | end-users | True | 117590.0 | 68.4% | 70.7% | 2.3 |
| 70.0 | 80.0 | app1 | True | 2716.0 | 21.1% | 1.6% | -19.4 |
| 70.0 | 80.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 70.0 | 80.0 | end-users | True | 160906.0 | 68.4% | 97.5% | 29.1 |
| 80.0 | 90.0 | app1 | True | 43246.0 | 21.1% | 25.0% | 3.9 |
| 80.0 | 90.0 | app2 | True | 2666.0 | 10.5% | 1.5% | -9.0 |
| 80.0 | 90.0 | end-users | True | 127200.0 | 68.4% | 73.5% | 5.1 |
| 90.0 | 100.0 | app1 | True | 47448.0 | 21.1% | 27.6% | 6.6 |
| 90.0 | 100.0 | app2 | True | 4066.0 | 10.5% | 2.4% | -8.2 |
| 90.0 | 100.0 | end-users | True | 120274.0 | 68.4% | 70.0% | 1.6 |
| 100.0 | 110.0 | app1 | True | 43278.0 | 21.1% | 26.2% | 5.2 |
| 100.0 | 110.0 | app2 | True | 1346.0 | 10.5% | 0.8% | -9.7 |
| 100.0 | 110.0 | end-users | True | 120312.0 | 68.4% | 72.9% | 4.5 |
| 110.0 | 120.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 110.0 | 120.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 110.0 | 120.0 | end-users | True | 164958.0 | 68.4% | 98.4% | 30.0 |
| 120.0 | 130.0 | app1 | True | 43238.0 | 21.1% | 25.6% | 4.5 |
| 120.0 | 130.0 | app2 | True | 2712.0 | 10.5% | 1.6% | -8.9 |
| 120.0 | 130.0 | end-users | True | 123076.0 | 68.4% | 72.8% | 4.4 |
| 130.0 | 140.0 | app1 | True | 46042.0 | 21.1% | 27.7% | 6.6 |
| 130.0 | 140.0 | app2 | True | 5418.0 | 10.5% | 3.3% | -7.3 |
| 130.0 | 140.0 | end-users | True | 114908.0 | 68.4% | 69.1% | 0.6 |
| 140.0 | 150.0 | app1 | True | 43328.0 | 21.1% | 25.6% | 4.6 |
| 140.0 | 150.0 | app2 | True | 2696.0 | 10.5% | 1.6% | -8.9 |
| 140.0 | 150.0 | end-users | True | 123012.0 | 68.4% | 72.8% | 4.4 |
| 150.0 | 160.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 150.0 | 160.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 150.0 | 160.0 | end-users | True | 164972.0 | 68.4% | 100.0% | 31.6 |
| 160.0 | 170.0 | app1 | True | 43310.0 | 21.1% | 25.8% | 4.8 |
| 160.0 | 170.0 | app2 | True | 2678.0 | 10.5% | 1.6% | -8.9 |
| 160.0 | 170.0 | end-users | True | 121720.0 | 68.4% | 72.6% | 4.2 |
| 170.0 | 180.0 | app1 | True | 47378.0 | 21.1% | 28.5% | 7.4 |
| 170.0 | 180.0 | app2 | True | 5432.0 | 10.5% | 3.3% | -7.3 |
| 170.0 | 180.0 | end-users | True | 113634.0 | 68.4% | 68.3% | -0.1 |
| 180.0 | 190.0 | app1 | True | 41912.0 | 21.1% | 25.4% | 4.3 |
| 180.0 | 190.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 180.0 | 190.0 | end-users | True | 120520.0 | 68.4% | 73.0% | 4.6 |
| 190.0 | 200.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 190.0 | 200.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 190.0 | 200.0 | end-users | True | 170400.0 | 68.4% | 100.0% | 31.6 |
| 200.0 | 210.0 | app1 | True | 43244.0 | 21.1% | 25.2% | 4.2 |
| 200.0 | 210.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 200.0 | 210.0 | end-users | True | 125622.0 | 68.4% | 73.2% | 4.8 |
| 210.0 | 220.0 | app1 | True | 43216.0 | 21.1% | 25.6% | 4.5 |
| 210.0 | 220.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 210.0 | 220.0 | end-users | True | 123082.0 | 68.4% | 72.8% | 4.4 |
| 220.0 | 230.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 220.0 | 230.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 220.0 | 230.0 | end-users | True | 166408.0 | 68.4% | 99.2% | 30.8 |
| 230.0 | 240.0 | app1 | True | 64882.0 | 21.1% | 38.4% | 17.4 |
| 230.0 | 240.0 | app2 | True | 4036.0 | 10.5% | 2.4% | -8.1 |
| 230.0 | 240.0 | end-users | True | 100028.0 | 68.4% | 59.2% | -9.2 |
| 240.0 | 250.0 | app1 | False | 22970.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 2716.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 139468.0 | n/a | n/a | n/a |
| 250.0 | 261.0 | app1 | False | 20326.0 | n/a | n/a | n/a |
| 250.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 261.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 788430 | 39274 | 827704.0 | 0.0% | 816970.0 | 866978.0 | -5.8% | True |
| app2 | 61500 | 3061 | 64561.0 | 0.0% | 64918.0 | 67622.0 | -4.0% | True |
| end-users | 3007350 | 149516 | 3156866.0 | 0.0% | 3263076.0 | 3306382.0 | -1.3% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
