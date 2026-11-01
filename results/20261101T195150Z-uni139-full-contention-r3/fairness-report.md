# Fairness benchmark: full-contention (uni139-full-contention-r3)

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
| Run start | `2026-11-01T19:51:51Z` |
| Run end | `2026-11-01T19:56:14Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 507 | 200=504, 500=3 | 16.3 | 26.7 | 645090.0 | 21.1% | 15.7% | -5.4 | 6.2s | 98.3% | 504.0 |
| app2 | 10.0 | 32 | 466 | 200=459, 500=7 | 18.4 | 26.4 | 597678.0 | 10.5% | 14.5% | 4.0 | 6.1s | 95.9% | 459.0 |
| end-users | 65.0 | 128 | 2164 | 200=2143, 500=21 | 15.2 | 19.3 | 2876882.0 | 68.4% | 69.8% | 1.4 | 6.5s | 98.9% | 2143.0 |
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
| 0.0 | 10.0 | app1 | True | 21566.0 | 21.1% | 26.1% | 5.1 |
| 0.0 | 10.0 | app2 | True | 12202.0 | 10.5% | 14.8% | 4.3 |
| 0.0 | 10.0 | end-users | True | 48726.0 | 68.4% | 59.1% | -9.4 |
| 10.0 | 20.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 10.0 | 20.0 | app2 | True | 10796.0 | 10.5% | 6.3% | -4.2 |
| 10.0 | 20.0 | end-users | True | 159564.0 | 68.4% | 93.7% | 25.2 |
| 20.0 | 30.0 | app1 | True | 43364.0 | 21.1% | 25.8% | 4.8 |
| 20.0 | 30.0 | app2 | True | 56778.0 | 10.5% | 33.8% | 23.3 |
| 20.0 | 30.0 | end-users | True | 67726.0 | 68.4% | 40.3% | -28.1 |
| 30.0 | 40.0 | app1 | True | 31016.0 | 21.1% | 20.7% | -0.4 |
| 30.0 | 40.0 | app2 | True | 1358.0 | 10.5% | 0.9% | -9.6 |
| 30.0 | 40.0 | end-users | True | 117730.0 | 68.4% | 78.4% | 10.0 |
| 40.0 | 50.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 40.0 | 50.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 40.0 | 50.0 | end-users | True | 165270.0 | 68.4% | 100.0% | 31.6 |
| 50.0 | 60.0 | app1 | True | 52700.0 | 21.1% | 31.2% | 10.1 |
| 50.0 | 60.0 | app2 | True | 62306.0 | 10.5% | 36.9% | 26.3 |
| 50.0 | 60.0 | end-users | True | 54026.0 | 68.4% | 32.0% | -36.5 |
| 60.0 | 70.0 | app1 | True | 31172.0 | 21.1% | 19.2% | -1.8 |
| 60.0 | 70.0 | app2 | True | 1350.0 | 10.5% | 0.8% | -9.7 |
| 60.0 | 70.0 | end-users | True | 129674.0 | 68.4% | 79.9% | 11.5 |
| 70.0 | 80.0 | app1 | True | 8140.0 | 21.1% | 5.1% | -16.0 |
| 70.0 | 80.0 | app2 | True | 4074.0 | 10.5% | 2.5% | -8.0 |
| 70.0 | 80.0 | end-users | True | 148820.0 | 68.4% | 92.4% | 24.0 |
| 80.0 | 90.0 | app1 | True | 52820.0 | 21.1% | 32.0% | 11.0 |
| 80.0 | 90.0 | app2 | True | 54044.0 | 10.5% | 32.8% | 22.2 |
| 80.0 | 90.0 | end-users | True | 58082.0 | 68.4% | 35.2% | -33.2 |
| 90.0 | 100.0 | app1 | True | 13500.0 | 21.1% | 7.9% | -13.1 |
| 90.0 | 100.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 90.0 | 100.0 | end-users | True | 156788.0 | 68.4% | 92.1% | 23.7 |
| 100.0 | 110.0 | app1 | True | 43350.0 | 21.1% | 28.3% | 7.3 |
| 100.0 | 110.0 | app2 | True | 24378.0 | 10.5% | 15.9% | 5.4 |
| 100.0 | 110.0 | end-users | True | 85202.0 | 68.4% | 55.7% | -12.7 |
| 110.0 | 120.0 | app1 | True | 30998.0 | 21.1% | 18.5% | -2.5 |
| 110.0 | 120.0 | app2 | True | 39274.0 | 10.5% | 23.4% | 12.9 |
| 110.0 | 120.0 | end-users | True | 97248.0 | 68.4% | 58.1% | -10.4 |
| 120.0 | 130.0 | app1 | True | 9432.0 | 21.1% | 5.5% | -15.6 |
| 120.0 | 130.0 | app2 | True | 16238.0 | 10.5% | 9.5% | -1.1 |
| 120.0 | 130.0 | end-users | True | 146000.0 | 68.4% | 85.0% | 16.6 |
| 130.0 | 140.0 | app1 | True | 41930.0 | 21.1% | 24.6% | 3.6 |
| 130.0 | 140.0 | app2 | True | 32426.0 | 10.5% | 19.0% | 8.5 |
| 130.0 | 140.0 | end-users | True | 96028.0 | 68.4% | 56.4% | -12.1 |
| 140.0 | 150.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 140.0 | 150.0 | app2 | True | 18934.0 | 10.5% | 12.1% | 1.5 |
| 140.0 | 150.0 | end-users | True | 137856.0 | 68.4% | 87.9% | 19.5 |
| 150.0 | 160.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 150.0 | 160.0 | app2 | True | 22946.0 | 10.5% | 14.0% | 3.5 |
| 150.0 | 160.0 | end-users | True | 140852.0 | 68.4% | 86.0% | 17.6 |
| 160.0 | 170.0 | app1 | True | 54062.0 | 21.1% | 32.2% | 11.2 |
| 160.0 | 170.0 | app2 | True | 29768.0 | 10.5% | 17.8% | 7.2 |
| 160.0 | 170.0 | end-users | True | 83856.0 | 68.4% | 50.0% | -18.4 |
| 170.0 | 180.0 | app1 | True | 2716.0 | 21.1% | 1.6% | -19.4 |
| 170.0 | 180.0 | app2 | True | 21588.0 | 10.5% | 13.1% | 2.6 |
| 170.0 | 180.0 | end-users | True | 140760.0 | 68.4% | 85.3% | 16.9 |
| 180.0 | 190.0 | app1 | True | 2716.0 | 21.1% | 1.8% | -19.3 |
| 180.0 | 190.0 | app2 | True | 35160.0 | 10.5% | 22.8% | 12.3 |
| 180.0 | 190.0 | end-users | True | 116384.0 | 68.4% | 75.4% | 7.0 |
| 190.0 | 200.0 | app1 | True | 54004.0 | 21.1% | 32.2% | 11.2 |
| 190.0 | 200.0 | app2 | True | 16218.0 | 10.5% | 9.7% | -0.8 |
| 190.0 | 200.0 | end-users | True | 97348.0 | 68.4% | 58.1% | -10.3 |
| 200.0 | 210.0 | app1 | True | 9468.0 | 21.1% | 5.7% | -15.4 |
| 200.0 | 210.0 | app2 | True | 51408.0 | 10.5% | 30.9% | 20.4 |
| 200.0 | 210.0 | end-users | True | 105504.0 | 68.4% | 63.4% | -5.0 |
| 210.0 | 220.0 | app1 | True | 40650.0 | 21.1% | 23.3% | 2.2 |
| 210.0 | 220.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 210.0 | 220.0 | end-users | True | 133888.0 | 68.4% | 76.7% | 8.3 |
| 220.0 | 230.0 | app1 | True | 31104.0 | 21.1% | 20.5% | -0.5 |
| 220.0 | 230.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 220.0 | 230.0 | end-users | True | 120282.0 | 68.4% | 79.5% | 11.0 |
| 230.0 | 240.0 | app1 | True | 25730.0 | 21.1% | 15.6% | -5.5 |
| 230.0 | 240.0 | app2 | True | 43254.0 | 10.5% | 26.2% | 15.7 |
| 230.0 | 240.0 | end-users | True | 96144.0 | 68.4% | 58.2% | -10.2 |
| 240.0 | 250.0 | app1 | False | 17594.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 1344.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 150148.0 | n/a | n/a | n/a |
| 250.0 | 261.0 | app1 | False | 27058.0 | n/a | n/a | n/a |
| 250.0 | 261.0 | app2 | False | 41834.0 | n/a | n/a | n/a |
| 250.0 | 261.0 | end-users | False | 22976.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 619920 | 30823 | 650743.0 | 0.0% | 645090.0 | 681566.0 | -5.4% | True |
| app2 | 564570 | 28041 | 592611.0 | 0.0% | 597678.0 | 620652.0 | -3.7% | True |
| end-users | 2635890 | 131325 | 2767215.0 | 0.0% | 2876882.0 | 2898540.0 | -0.7% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
