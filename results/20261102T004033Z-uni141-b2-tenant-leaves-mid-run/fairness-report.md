# Fairness benchmark: full-contention (uni141-b2-tenant-leaves-mid-run)

**Verdict: FAIL** (threshold: 10 points)

- end-users deviated -34.0 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-02T00:40:34Z` |
| Run end | `2026-11-02T00:44:47Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1155 | 200=1154, 500=1 | 4.3 | 21.2 | 1504400.0 | 21.1% | 33.9% | 12.8 | 5.0s | 98.8% | 1154.0 |
| app2 | 10.0 | 32 | 1080 | 200=1072, 500=8 | 4.4 | 25.2 | 1407096.0 | 10.5% | 31.7% | 21.2 | 4.8s | 98.1% | 1072.0 |
| end-users | 65.0 | 128 | 1207 | 200=1146, 500=61 | 14.5 | 17.4 | 1529012.0 | 68.4% | 34.4% | -34.0 | 4.4s | 98.9% | 1144.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 2712.0 | n/a | n/a | n/a | 0.0s | 98.2% | 2.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- end-users: active 0s-120s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 110.0 | 110.0 |
| 120.0 | 230.0 | 110.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 10856.0 | 21.1% | 12.3% | -8.7 |
| 0.0 | 10.0 | app2 | True | 13510.0 | 10.5% | 15.4% | 4.8 |
| 0.0 | 10.0 | end-users | True | 63550.0 | 68.4% | 72.3% | 3.9 |
| 10.0 | 20.0 | app1 | True | 44540.0 | 21.1% | 25.9% | 4.9 |
| 10.0 | 20.0 | app2 | True | 17602.0 | 10.5% | 10.3% | -0.3 |
| 10.0 | 20.0 | end-users | True | 109566.0 | 68.4% | 63.8% | -4.6 |
| 20.0 | 30.0 | app1 | True | 2694.0 | 21.1% | 1.6% | -19.4 |
| 20.0 | 30.0 | app2 | True | 23032.0 | 10.5% | 13.7% | 3.2 |
| 20.0 | 30.0 | end-users | True | 141988.0 | 68.4% | 84.7% | 16.2 |
| 30.0 | 40.0 | app1 | True | 39280.0 | 21.1% | 23.8% | 2.7 |
| 30.0 | 40.0 | app2 | True | 29834.0 | 10.5% | 18.1% | 7.5 |
| 30.0 | 40.0 | end-users | True | 96054.0 | 68.4% | 58.2% | -10.3 |
| 40.0 | 50.0 | app1 | True | 4074.0 | 21.1% | 2.6% | -18.5 |
| 40.0 | 50.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 40.0 | 50.0 | end-users | True | 153014.0 | 68.4% | 97.4% | 29.0 |
| 50.0 | 60.0 | app1 | True | 43222.0 | 21.1% | 25.8% | 4.7 |
| 50.0 | 60.0 | app2 | True | 47366.0 | 10.5% | 28.3% | 17.7 |
| 50.0 | 60.0 | end-users | True | 77050.0 | 68.4% | 46.0% | -22.5 |
| 60.0 | 70.0 | app1 | True | 12156.0 | 21.1% | 7.1% | -14.0 |
| 60.0 | 70.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 60.0 | 70.0 | end-users | True | 158266.0 | 68.4% | 92.1% | 23.7 |
| 70.0 | 80.0 | app1 | True | 43302.0 | 21.1% | 25.8% | 4.7 |
| 70.0 | 80.0 | app2 | True | 21612.0 | 10.5% | 12.9% | 2.3 |
| 70.0 | 80.0 | end-users | True | 102950.0 | 68.4% | 61.3% | -7.1 |
| 80.0 | 90.0 | app1 | True | 22974.0 | 21.1% | 15.6% | -5.5 |
| 80.0 | 90.0 | app2 | True | 16240.0 | 10.5% | 11.0% | 0.5 |
| 80.0 | 90.0 | end-users | True | 108340.0 | 68.4% | 73.4% | 5.0 |
| 90.0 | 100.0 | app1 | True | 14904.0 | 21.1% | 8.8% | -12.2 |
| 90.0 | 100.0 | app2 | True | 48764.0 | 10.5% | 28.8% | 18.3 |
| 90.0 | 100.0 | end-users | True | 105588.0 | 68.4% | 62.4% | -6.0 |
| 100.0 | 110.0 | app1 | True | 40576.0 | 21.1% | 23.4% | 2.4 |
| 100.0 | 110.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 100.0 | 110.0 | end-users | True | 132574.0 | 68.4% | 76.6% | 8.1 |
| 110.0 | 120.0 | app1 | True | 22952.0 | 21.1% | 15.2% | -5.9 |
| 110.0 | 120.0 | app2 | True | 21542.0 | 10.5% | 14.2% | 3.7 |
| 110.0 | 120.0 | end-users | True | 106876.0 | 68.4% | 70.6% | 2.2 |
| 120.0 | 130.0 | app1 | True | 31102.0 | 66.7% | 43.4% | -23.3 |
| 120.0 | 130.0 | app2 | True | 40570.0 | 33.3% | 56.6% | 23.3 |
| 120.0 | 130.0 | end-users | False | 100108.0 | n/a | n/a | n/a |
| 130.0 | 140.0 | app1 | True | 54100.0 | 66.7% | 52.0% | -14.7 |
| 130.0 | 140.0 | app2 | True | 50028.0 | 33.3% | 48.0% | 14.7 |
| 130.0 | 140.0 | end-users | False | 73088.0 | n/a | n/a | n/a |
| 140.0 | 150.0 | app1 | True | 114948.0 | 66.7% | 53.4% | -13.2 |
| 140.0 | 150.0 | app2 | True | 100134.0 | 33.3% | 46.6% | 13.2 |
| 140.0 | 150.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 150.0 | 160.0 | app1 | True | 97434.0 | 66.7% | 48.7% | -18.0 |
| 150.0 | 160.0 | app2 | True | 102756.0 | 33.3% | 51.3% | 18.0 |
| 150.0 | 160.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 160.0 | 170.0 | app1 | True | 104200.0 | 66.7% | 45.3% | -21.3 |
| 160.0 | 170.0 | app2 | True | 125732.0 | 33.3% | 54.7% | 21.3 |
| 160.0 | 170.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 170.0 | 180.0 | app1 | True | 98832.0 | 66.7% | 49.3% | -17.3 |
| 170.0 | 180.0 | app2 | True | 101536.0 | 33.3% | 50.7% | 17.3 |
| 170.0 | 180.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 180.0 | 190.0 | app1 | True | 106858.0 | 66.7% | 50.6% | -16.0 |
| 180.0 | 190.0 | app2 | True | 104148.0 | 33.3% | 49.4% | 16.0 |
| 180.0 | 190.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 190.0 | 200.0 | app1 | True | 132654.0 | 66.7% | 59.7% | -6.9 |
| 190.0 | 200.0 | app2 | True | 89382.0 | 33.3% | 40.3% | 6.9 |
| 190.0 | 200.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 200.0 | 210.0 | app1 | True | 100202.0 | 66.7% | 50.4% | -16.3 |
| 200.0 | 210.0 | app2 | True | 98762.0 | 33.3% | 49.6% | 16.3 |
| 200.0 | 210.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 210.0 | 220.0 | app1 | True | 87994.0 | 66.7% | 42.5% | -24.2 |
| 210.0 | 220.0 | app2 | True | 119082.0 | 33.3% | 57.5% | 24.2 |
| 210.0 | 220.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 220.0 | 230.0 | app1 | True | 113622.0 | 66.7% | 51.9% | -14.8 |
| 220.0 | 230.0 | app2 | True | 105484.0 | 33.3% | 48.1% | 14.8 |
| 220.0 | 230.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 230.0 | 240.0 | app1 | True | 117630.0 | 66.7% | 57.6% | -9.1 |
| 230.0 | 240.0 | app2 | True | 86636.0 | 33.3% | 42.4% | 9.1 |
| 230.0 | 240.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 251.0 | app1 | False | 43294.0 | n/a | n/a | n/a |
| 240.0 | 251.0 | app2 | False | 41986.0 | n/a | n/a | n/a |
| 240.0 | 251.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 253.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 253.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 253.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1419420 | 70870 | 1490290.0 | 0.0% | 1504400.0 | 1561160.0 | -3.6% | True |
| app2 | 1318560 | 65916 | 1384476.0 | 0.0% | 1407096.0 | 1450392.0 | -3.0% | True |
| end-users | 1409580 | 70553 | 1477547.0 | -0.2% | 1529012.0 | 1550686.0 | -1.4% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
