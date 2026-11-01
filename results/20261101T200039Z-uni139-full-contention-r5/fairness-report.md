# Fairness benchmark: full-contention (uni139-full-contention-r5)

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
| Run start | `2026-11-01T20:00:41Z` |
| Run end | `2026-11-01T20:05:03Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 552 | 200=552 | 14.6 | 23.6 | 710026.0 | 21.1% | 17.2% | -3.9 | 2.5s | 98.4% | 552.0 |
| app2 | 10.0 | 32 | 452 | 200=448, 500=4 | 24.3 | 27.5 | 579052.0 | 10.5% | 14.0% | 3.5 | 1.6s | 96.3% | 448.0 |
| end-users | 65.0 | 128 | 2137 | 200=2117, 500=20 | 14.9 | 19.7 | 2839466.0 | 68.4% | 68.8% | 0.4 | 2.3s | 98.9% | 2117.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 88.7% | 0.0 |

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
| 0.0 | 10.0 | app1 | True | 4050.0 | 21.1% | 4.7% | -16.4 |
| 0.0 | 10.0 | app2 | True | 4056.0 | 10.5% | 4.7% | -5.8 |
| 0.0 | 10.0 | end-users | True | 78486.0 | 68.4% | 90.6% | 22.2 |
| 10.0 | 20.0 | app1 | True | 27048.0 | 21.1% | 16.1% | -4.9 |
| 10.0 | 20.0 | app2 | True | 46006.0 | 10.5% | 27.4% | 16.9 |
| 10.0 | 20.0 | end-users | True | 94764.0 | 68.4% | 56.5% | -12.0 |
| 20.0 | 30.0 | app1 | True | 17592.0 | 21.1% | 10.6% | -10.5 |
| 20.0 | 30.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 20.0 | 30.0 | end-users | True | 148840.0 | 68.4% | 89.4% | 21.0 |
| 30.0 | 40.0 | app1 | True | 43314.0 | 21.1% | 26.5% | 5.4 |
| 30.0 | 40.0 | app2 | True | 33822.0 | 10.5% | 20.7% | 10.1 |
| 30.0 | 40.0 | end-users | True | 86500.0 | 68.4% | 52.9% | -15.6 |
| 40.0 | 50.0 | app1 | True | 31162.0 | 21.1% | 19.7% | -1.4 |
| 40.0 | 50.0 | app2 | True | 27096.0 | 10.5% | 17.1% | 6.6 |
| 40.0 | 50.0 | end-users | True | 100208.0 | 68.4% | 63.2% | -5.2 |
| 50.0 | 60.0 | app1 | True | 5422.0 | 21.1% | 3.2% | -17.8 |
| 50.0 | 60.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 50.0 | 60.0 | end-users | True | 163618.0 | 68.4% | 96.8% | 28.4 |
| 60.0 | 70.0 | app1 | True | 45876.0 | 21.1% | 27.2% | 6.1 |
| 60.0 | 70.0 | app2 | True | 59548.0 | 10.5% | 35.2% | 24.7 |
| 60.0 | 70.0 | end-users | True | 63536.0 | 68.4% | 37.6% | -30.8 |
| 70.0 | 80.0 | app1 | True | 29780.0 | 21.1% | 19.5% | -1.6 |
| 70.0 | 80.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 70.0 | 80.0 | end-users | True | 123044.0 | 68.4% | 80.5% | 12.1 |
| 80.0 | 90.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 80.0 | 90.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 80.0 | 90.0 | end-users | True | 169056.0 | 68.4% | 100.0% | 31.6 |
| 90.0 | 100.0 | app1 | True | 55508.0 | 21.1% | 33.9% | 12.8 |
| 90.0 | 100.0 | app2 | True | 60822.0 | 10.5% | 37.1% | 26.6 |
| 90.0 | 100.0 | end-users | True | 47408.0 | 68.4% | 29.0% | -39.5 |
| 100.0 | 110.0 | app1 | True | 25706.0 | 21.1% | 15.0% | -6.1 |
| 100.0 | 110.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 100.0 | 110.0 | end-users | True | 146176.0 | 68.4% | 85.0% | 16.6 |
| 110.0 | 120.0 | app1 | True | 13468.0 | 21.1% | 8.9% | -12.2 |
| 110.0 | 120.0 | app2 | True | 8072.0 | 10.5% | 5.3% | -5.2 |
| 110.0 | 120.0 | end-users | True | 129868.0 | 68.4% | 85.8% | 17.4 |
| 120.0 | 130.0 | app1 | True | 51486.0 | 21.1% | 30.2% | 9.2 |
| 120.0 | 130.0 | app2 | True | 51328.0 | 10.5% | 30.1% | 19.6 |
| 120.0 | 130.0 | end-users | True | 67644.0 | 68.4% | 39.7% | -28.7 |
| 130.0 | 140.0 | app1 | True | 55394.0 | 21.1% | 32.8% | 11.7 |
| 130.0 | 140.0 | app2 | True | 1344.0 | 10.5% | 0.8% | -9.7 |
| 130.0 | 140.0 | end-users | True | 112356.0 | 68.4% | 66.4% | -2.0 |
| 140.0 | 150.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 140.0 | 150.0 | app2 | True | 20294.0 | 10.5% | 13.2% | 2.7 |
| 140.0 | 150.0 | end-users | True | 133714.0 | 68.4% | 86.8% | 18.4 |
| 150.0 | 160.0 | app1 | True | 27074.0 | 21.1% | 16.0% | -5.1 |
| 150.0 | 160.0 | app2 | True | 42006.0 | 10.5% | 24.8% | 14.3 |
| 150.0 | 160.0 | end-users | True | 100178.0 | 68.4% | 59.2% | -9.2 |
| 160.0 | 170.0 | app1 | True | 16214.0 | 21.1% | 9.8% | -11.2 |
| 160.0 | 170.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 160.0 | 170.0 | end-users | True | 148812.0 | 68.4% | 90.2% | 21.8 |
| 170.0 | 180.0 | app1 | True | 40566.0 | 21.1% | 24.2% | 3.1 |
| 170.0 | 180.0 | app2 | True | 58268.0 | 10.5% | 34.7% | 24.2 |
| 170.0 | 180.0 | end-users | True | 68956.0 | 68.4% | 41.1% | -27.3 |
| 180.0 | 190.0 | app1 | True | 35166.0 | 21.1% | 23.0% | 1.9 |
| 180.0 | 190.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 180.0 | 190.0 | end-users | True | 117846.0 | 68.4% | 77.0% | 8.6 |
| 190.0 | 200.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 190.0 | 200.0 | app2 | True | 1356.0 | 10.5% | 0.8% | -9.7 |
| 190.0 | 200.0 | end-users | True | 170240.0 | 68.4% | 99.2% | 30.8 |
| 200.0 | 210.0 | app1 | True | 54058.0 | 21.1% | 32.0% | 10.9 |
| 200.0 | 210.0 | app2 | True | 59556.0 | 10.5% | 35.2% | 24.7 |
| 200.0 | 210.0 | end-users | True | 55426.0 | 68.4% | 32.8% | -35.6 |
| 210.0 | 220.0 | app1 | True | 25676.0 | 21.1% | 15.8% | -5.2 |
| 210.0 | 220.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 210.0 | 220.0 | end-users | True | 136554.0 | 68.4% | 84.2% | 15.8 |
| 220.0 | 230.0 | app1 | True | 8130.0 | 21.1% | 5.2% | -15.9 |
| 220.0 | 230.0 | app2 | True | 4042.0 | 10.5% | 2.6% | -8.0 |
| 220.0 | 230.0 | end-users | True | 144912.0 | 68.4% | 92.3% | 23.8 |
| 230.0 | 240.0 | app1 | True | 52672.0 | 21.1% | 31.7% | 10.6 |
| 230.0 | 240.0 | app2 | True | 58120.0 | 10.5% | 34.9% | 24.4 |
| 230.0 | 240.0 | end-users | True | 55566.0 | 68.4% | 33.4% | -35.0 |
| 240.0 | 250.0 | app1 | False | 23050.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 143290.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 21614.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 43316.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 32468.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 678960 | 33768 | 712728.0 | 0.0% | 710026.0 | 746496.0 | -4.9% | True |
| app2 | 551040 | 27568 | 578608.0 | 0.0% | 579052.0 | 606176.0 | -4.5% | True |
| end-users | 2603910 | 129929 | 2733839.0 | 0.0% | 2839466.0 | 2863768.0 | -0.8% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
