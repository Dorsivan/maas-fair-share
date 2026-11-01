# Fairness benchmark: full-contention (uni139-full-contention-r2)

**Verdict: PASS** (threshold: 10 points)

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
| Run start | `2026-11-01T19:47:27Z` |
| Run end | `2026-11-01T19:51:49Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 557 | 200=557 | 12.6 | 23.8 | 719798.0 | 21.1% | 17.5% | -3.5 | 2.6s | 98.3% | 557.0 |
| app2 | 10.0 | 32 | 459 | 200=454, 500=5 | 24.3 | 27.6 | 590892.0 | 10.5% | 14.4% | 3.8 | 1.6s | 95.7% | 454.0 |
| end-users | 65.0 | 128 | 2134 | 200=2105, 500=29 | 15.9 | 19.6 | 2801628.0 | 68.4% | 68.1% | -0.3 | 2.2s | 98.9% | 2102.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 4058.0 | n/a | n/a | n/a | 0.1s | 88.7% | 3.0 |

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
| 0.0 | 10.0 | app1 | True | 8114.0 | 21.1% | 9.4% | -11.7 |
| 0.0 | 10.0 | app2 | True | 13544.0 | 10.5% | 15.6% | 5.1 |
| 0.0 | 10.0 | end-users | True | 64898.0 | 68.4% | 75.0% | 6.6 |
| 10.0 | 20.0 | app1 | True | 32418.0 | 21.1% | 20.3% | -0.7 |
| 10.0 | 20.0 | app2 | True | 48666.0 | 10.5% | 30.5% | 20.0 |
| 10.0 | 20.0 | end-users | True | 78478.0 | 68.4% | 49.2% | -19.2 |
| 20.0 | 30.0 | app1 | True | 27018.0 | 21.1% | 15.6% | -5.4 |
| 20.0 | 30.0 | app2 | True | 1344.0 | 10.5% | 0.8% | -9.7 |
| 20.0 | 30.0 | end-users | True | 144762.0 | 68.4% | 83.6% | 15.2 |
| 30.0 | 40.0 | app1 | True | 14884.0 | 21.1% | 9.7% | -11.3 |
| 30.0 | 40.0 | app2 | True | 8118.0 | 10.5% | 5.3% | -5.2 |
| 30.0 | 40.0 | end-users | True | 129720.0 | 68.4% | 84.9% | 16.5 |
| 40.0 | 50.0 | app1 | True | 47366.0 | 21.1% | 28.2% | 7.2 |
| 40.0 | 50.0 | app2 | True | 52824.0 | 10.5% | 31.5% | 21.0 |
| 40.0 | 50.0 | end-users | True | 67584.0 | 68.4% | 40.3% | -28.1 |
| 50.0 | 60.0 | app1 | True | 21648.0 | 21.1% | 13.0% | -8.0 |
| 50.0 | 60.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 50.0 | 60.0 | end-users | True | 143380.0 | 68.4% | 86.2% | 17.8 |
| 60.0 | 70.0 | app1 | True | 35196.0 | 21.1% | 23.2% | 2.2 |
| 60.0 | 70.0 | app2 | True | 16208.0 | 10.5% | 10.7% | 0.2 |
| 60.0 | 70.0 | end-users | True | 100110.0 | 68.4% | 66.1% | -2.3 |
| 70.0 | 80.0 | app1 | True | 35158.0 | 21.1% | 20.8% | -0.2 |
| 70.0 | 80.0 | app2 | True | 45844.0 | 10.5% | 27.1% | 16.6 |
| 70.0 | 80.0 | end-users | True | 87990.0 | 68.4% | 52.1% | -16.4 |
| 80.0 | 90.0 | app1 | True | 13580.0 | 21.1% | 8.0% | -13.0 |
| 80.0 | 90.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 80.0 | 90.0 | end-users | True | 154240.0 | 68.4% | 91.2% | 22.7 |
| 90.0 | 100.0 | app1 | True | 43262.0 | 21.1% | 26.0% | 4.9 |
| 90.0 | 100.0 | app2 | True | 47368.0 | 10.5% | 28.5% | 17.9 |
| 90.0 | 100.0 | end-users | True | 75820.0 | 68.4% | 45.6% | -22.9 |
| 100.0 | 110.0 | app1 | True | 32404.0 | 21.1% | 21.8% | 0.7 |
| 100.0 | 110.0 | app2 | True | 12170.0 | 10.5% | 8.2% | -2.3 |
| 100.0 | 110.0 | end-users | True | 104116.0 | 68.4% | 70.0% | 1.6 |
| 110.0 | 120.0 | app1 | True | 2716.0 | 21.1% | 1.6% | -19.4 |
| 110.0 | 120.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 110.0 | 120.0 | end-users | True | 165188.0 | 68.4% | 98.4% | 30.0 |
| 120.0 | 130.0 | app1 | True | 47382.0 | 21.1% | 28.2% | 7.2 |
| 120.0 | 130.0 | app2 | True | 60866.0 | 10.5% | 36.3% | 25.7 |
| 120.0 | 130.0 | end-users | True | 59592.0 | 68.4% | 35.5% | -32.9 |
| 130.0 | 140.0 | app1 | True | 33844.0 | 21.1% | 22.2% | 1.1 |
| 130.0 | 140.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 130.0 | 140.0 | end-users | True | 118948.0 | 68.4% | 77.8% | 9.4 |
| 140.0 | 150.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 140.0 | 150.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 140.0 | 150.0 | end-users | True | 169206.0 | 68.4% | 100.0% | 31.6 |
| 150.0 | 160.0 | app1 | True | 56794.0 | 21.1% | 33.3% | 12.3 |
| 150.0 | 160.0 | app2 | True | 59454.0 | 10.5% | 34.9% | 24.4 |
| 150.0 | 160.0 | end-users | True | 54104.0 | 68.4% | 31.8% | -36.7 |
| 160.0 | 170.0 | app1 | True | 21678.0 | 21.1% | 12.7% | -8.3 |
| 160.0 | 170.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 160.0 | 170.0 | end-users | True | 148524.0 | 68.4% | 87.3% | 18.8 |
| 170.0 | 180.0 | app1 | True | 17618.0 | 21.1% | 11.7% | -9.3 |
| 170.0 | 180.0 | app2 | True | 8084.0 | 10.5% | 5.4% | -5.1 |
| 170.0 | 180.0 | end-users | True | 124612.0 | 68.4% | 82.9% | 14.5 |
| 180.0 | 190.0 | app1 | True | 47412.0 | 21.1% | 28.0% | 7.0 |
| 180.0 | 190.0 | app2 | True | 51380.0 | 10.5% | 30.4% | 19.8 |
| 180.0 | 190.0 | end-users | True | 70382.0 | 68.4% | 41.6% | -26.8 |
| 190.0 | 200.0 | app1 | True | 13540.0 | 21.1% | 8.2% | -12.8 |
| 190.0 | 200.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 190.0 | 200.0 | end-users | True | 151484.0 | 68.4% | 91.8% | 23.4 |
| 200.0 | 210.0 | app1 | True | 43300.0 | 21.1% | 26.6% | 5.6 |
| 200.0 | 210.0 | app2 | True | 36572.0 | 10.5% | 22.5% | 12.0 |
| 200.0 | 210.0 | end-users | True | 82610.0 | 68.4% | 50.8% | -17.6 |
| 210.0 | 220.0 | app1 | True | 31148.0 | 21.1% | 20.0% | -1.0 |
| 210.0 | 220.0 | app2 | True | 23000.0 | 10.5% | 14.8% | 4.2 |
| 210.0 | 220.0 | end-users | True | 101516.0 | 68.4% | 65.2% | -3.2 |
| 220.0 | 230.0 | app1 | True | 2704.0 | 21.1% | 1.6% | -19.5 |
| 220.0 | 230.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 220.0 | 230.0 | end-users | True | 169026.0 | 68.4% | 98.4% | 30.0 |
| 230.0 | 240.0 | app1 | True | 47266.0 | 21.1% | 27.8% | 6.7 |
| 230.0 | 240.0 | app2 | True | 59424.0 | 10.5% | 34.9% | 24.4 |
| 230.0 | 240.0 | end-users | True | 63504.0 | 68.4% | 37.3% | -31.1 |
| 240.0 | 250.0 | app1 | False | 28424.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 121760.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 14924.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 43310.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 50074.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 685110 | 34249 | 719359.0 | 0.0% | 719798.0 | 753608.0 | -4.5% | True |
| app2 | 558420 | 27745 | 586165.0 | 0.0% | 590892.0 | 613910.0 | -3.7% | True |
| end-users | 2589150 | 129267 | 2714543.0 | -0.1% | 2801628.0 | 2847684.0 | -1.6% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
