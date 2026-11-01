# Fairness benchmark: app2-trickle (uni139-app2-trickle-r1)

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
| Run start | `2026-11-01T22:04:38Z` |
| Run end | `2026-11-01T22:09:00Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 620 | 200=619, 500=1 | 11.3 | 18.9 | 781632.0 | 23.5% | 19.8% | -3.7 | 1.6s | 98.8% | 619.0 |
| app2 | 10.0 | 2 | 50 | 200=50 | 11.2 | 15.9 | 64966.0 | n/a | n/a | n/a | 1.6s | 97.4% | 50.0 |
| end-users | 65.0 | 104 | 2490 | 200=2465, 500=25 | 11.1 | 12.5 | 3091428.0 | 76.5% | 78.5% | 2.0 | 1.6s | 98.9% | 2461.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 2716.0 | n/a | n/a | n/a | 0.1s | 98.1% | 4.0 |

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
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 31072.0 | 68.4% | 100.0% | 31.6 |
| 10.0 | 20.0 | app1 | True | 43246.0 | 21.1% | 25.8% | 4.7 |
| 10.0 | 20.0 | app2 | True | 2694.0 | 10.5% | 1.6% | -8.9 |
| 10.0 | 20.0 | end-users | True | 121664.0 | 68.4% | 72.6% | 4.2 |
| 20.0 | 30.0 | app1 | True | 47366.0 | 21.1% | 28.0% | 7.0 |
| 20.0 | 30.0 | app2 | True | 5374.0 | 10.5% | 3.2% | -7.3 |
| 20.0 | 30.0 | end-users | True | 116206.0 | 68.4% | 68.8% | 0.4 |
| 30.0 | 40.0 | app1 | True | 41890.0 | 21.1% | 25.4% | 4.3 |
| 30.0 | 40.0 | app2 | True | 2708.0 | 10.5% | 1.6% | -8.9 |
| 30.0 | 40.0 | end-users | True | 120508.0 | 68.4% | 73.0% | 4.6 |
| 40.0 | 50.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 40.0 | 50.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 40.0 | 50.0 | end-users | True | 170320.0 | 68.4% | 100.0% | 31.6 |
| 50.0 | 60.0 | app1 | True | 43236.0 | 21.1% | 26.2% | 5.1 |
| 50.0 | 60.0 | app2 | True | 2708.0 | 10.5% | 1.6% | -8.9 |
| 50.0 | 60.0 | end-users | True | 119112.0 | 68.4% | 72.2% | 3.7 |
| 60.0 | 70.0 | app1 | True | 47344.0 | 21.1% | 28.4% | 7.4 |
| 60.0 | 70.0 | app2 | True | 5432.0 | 10.5% | 3.3% | -7.3 |
| 60.0 | 70.0 | end-users | True | 113672.0 | 68.4% | 68.3% | -0.1 |
| 70.0 | 80.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.2 |
| 70.0 | 80.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 70.0 | 80.0 | end-users | True | 166368.0 | 68.4% | 99.2% | 30.8 |
| 80.0 | 90.0 | app1 | True | 41980.0 | 21.1% | 25.6% | 4.6 |
| 80.0 | 90.0 | app2 | True | 2702.0 | 10.5% | 1.6% | -8.9 |
| 80.0 | 90.0 | end-users | True | 119164.0 | 68.4% | 72.7% | 4.3 |
| 90.0 | 100.0 | app1 | True | 47288.0 | 21.1% | 27.8% | 6.7 |
| 90.0 | 100.0 | app2 | True | 5432.0 | 10.5% | 3.2% | -7.3 |
| 90.0 | 100.0 | end-users | True | 117620.0 | 68.4% | 69.1% | 0.6 |
| 100.0 | 110.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 100.0 | 110.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 100.0 | 110.0 | end-users | True | 165202.0 | 68.4% | 100.0% | 31.6 |
| 110.0 | 120.0 | app1 | True | 62168.0 | 21.1% | 35.9% | 14.9 |
| 110.0 | 120.0 | app2 | True | 5402.0 | 10.5% | 3.1% | -7.4 |
| 110.0 | 120.0 | end-users | True | 105478.0 | 68.4% | 61.0% | -7.5 |
| 120.0 | 130.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 120.0 | 130.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 120.0 | 130.0 | end-users | True | 169198.0 | 68.4% | 100.0% | 31.6 |
| 130.0 | 140.0 | app1 | True | 62160.0 | 21.1% | 37.4% | 16.3 |
| 130.0 | 140.0 | app2 | True | 5414.0 | 10.5% | 3.3% | -7.3 |
| 130.0 | 140.0 | end-users | True | 98796.0 | 68.4% | 59.4% | -9.0 |
| 140.0 | 150.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 140.0 | 150.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 140.0 | 150.0 | end-users | True | 171848.0 | 68.4% | 100.0% | 31.6 |
| 150.0 | 160.0 | app1 | True | 43272.0 | 21.1% | 26.9% | 5.8 |
| 150.0 | 160.0 | app2 | True | 2716.0 | 10.5% | 1.7% | -8.8 |
| 150.0 | 160.0 | end-users | True | 115110.0 | 68.4% | 71.5% | 3.0 |
| 160.0 | 170.0 | app1 | True | 29740.0 | 21.1% | 17.6% | -3.5 |
| 160.0 | 170.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 160.0 | 170.0 | end-users | True | 136578.0 | 68.4% | 80.8% | 12.4 |
| 170.0 | 180.0 | app1 | True | 46002.0 | 21.1% | 27.9% | 6.8 |
| 170.0 | 180.0 | app2 | True | 4052.0 | 10.5% | 2.5% | -8.1 |
| 170.0 | 180.0 | end-users | True | 115084.0 | 68.4% | 69.7% | 1.3 |
| 180.0 | 190.0 | app1 | True | 41882.0 | 21.1% | 25.0% | 3.9 |
| 180.0 | 190.0 | app2 | True | 4058.0 | 10.5% | 2.4% | -8.1 |
| 180.0 | 190.0 | end-users | True | 121792.0 | 68.4% | 72.6% | 4.2 |
| 190.0 | 200.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 190.0 | 200.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 190.0 | 200.0 | end-users | True | 166422.0 | 68.4% | 100.0% | 31.6 |
| 200.0 | 210.0 | app1 | True | 43304.0 | 21.1% | 26.2% | 5.2 |
| 200.0 | 210.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 200.0 | 210.0 | end-users | True | 119038.0 | 68.4% | 72.1% | 3.7 |
| 210.0 | 220.0 | app1 | True | 52764.0 | 21.1% | 30.7% | 9.7 |
| 210.0 | 220.0 | app2 | True | 5432.0 | 10.5% | 3.2% | -7.4 |
| 210.0 | 220.0 | end-users | True | 113484.0 | 68.4% | 66.1% | -2.3 |
| 220.0 | 230.0 | app1 | True | 43318.0 | 21.1% | 26.5% | 5.4 |
| 220.0 | 230.0 | app2 | True | 2716.0 | 10.5% | 1.7% | -8.9 |
| 220.0 | 230.0 | end-users | True | 117726.0 | 68.4% | 71.9% | 3.5 |
| 230.0 | 240.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 230.0 | 240.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 230.0 | 240.0 | end-users | True | 169148.0 | 68.4% | 100.0% | 31.6 |
| 240.0 | 250.0 | app1 | False | 43314.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 2694.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 10818.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 761370 | 37840 | 799210.0 | 0.0% | 781632.0 | 837050.0 | -6.6% | True |
| app2 | 61500 | 3067 | 64567.0 | 0.0% | 64966.0 | 67634.0 | -3.9% | True |
| end-users | 3031950 | 151381 | 3178182.0 | -0.2% | 3091428.0 | 3334712.0 | -7.3% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
