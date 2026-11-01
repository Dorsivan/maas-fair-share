# Fairness benchmark: app2-idle (uni139-app2-idle-r1)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app2-idle` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T21:19:43Z` |
| Run end | `2026-11-01T21:24:06Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 626 | 200=626 | 11.0 | 18.6 | 799034.0 | 23.5% | 19.0% | -4.5 | 1.6s | 98.8% | 626.0 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 97.3% | 0.0 |
| end-users | 65.0 | 104 | 2533 | 200=2533 | 10.8 | 12.3 | 3398144.0 | 76.5% | 81.0% | 4.5 | 1.6s | 98.9% | 2533.0 |
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
| 0.0 | 230.0 | 230.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 5428.0 | 23.5% | 5.0% | -18.5 |
| 0.0 | 10.0 | end-users | True | 102896.0 | 76.5% | 95.0% | 18.5 |
| 10.0 | 20.0 | app1 | True | 43262.0 | 23.5% | 25.8% | 2.3 |
| 10.0 | 20.0 | end-users | True | 124512.0 | 76.5% | 74.2% | -2.3 |
| 20.0 | 30.0 | app1 | True | 1348.0 | 23.5% | 0.8% | -22.7 |
| 20.0 | 30.0 | end-users | True | 166416.0 | 76.5% | 99.2% | 22.7 |
| 30.0 | 40.0 | app1 | True | 41820.0 | 23.5% | 24.7% | 1.2 |
| 30.0 | 40.0 | end-users | True | 127162.0 | 76.5% | 75.3% | -1.2 |
| 40.0 | 50.0 | app1 | True | 43204.0 | 23.5% | 25.4% | 1.9 |
| 40.0 | 50.0 | end-users | True | 126940.0 | 76.5% | 74.6% | -1.9 |
| 50.0 | 60.0 | app1 | True | 23002.0 | 23.5% | 13.6% | -9.9 |
| 50.0 | 60.0 | end-users | True | 146018.0 | 76.5% | 86.4% | 9.9 |
| 60.0 | 70.0 | app1 | True | 41922.0 | 23.5% | 23.8% | 0.3 |
| 60.0 | 70.0 | end-users | True | 133934.0 | 76.5% | 76.2% | -0.3 |
| 70.0 | 80.0 | app1 | True | 55318.0 | 23.5% | 31.0% | 7.5 |
| 70.0 | 80.0 | end-users | True | 123238.0 | 76.5% | 69.0% | -7.5 |
| 80.0 | 90.0 | app1 | True | 8118.0 | 23.5% | 4.8% | -18.7 |
| 80.0 | 90.0 | end-users | True | 161124.0 | 76.5% | 95.2% | 18.7 |
| 90.0 | 100.0 | app1 | True | 43274.0 | 23.5% | 25.0% | 1.4 |
| 90.0 | 100.0 | end-users | True | 129972.0 | 76.5% | 75.0% | -1.4 |
| 100.0 | 110.0 | app1 | True | 41892.0 | 23.5% | 26.0% | 2.5 |
| 100.0 | 110.0 | end-users | True | 118974.0 | 76.5% | 74.0% | -2.5 |
| 110.0 | 120.0 | app1 | True | 1358.0 | 23.5% | 0.8% | -22.7 |
| 110.0 | 120.0 | end-users | True | 170428.0 | 76.5% | 99.2% | 22.7 |
| 120.0 | 130.0 | app1 | True | 43288.0 | 23.5% | 25.2% | 1.7 |
| 120.0 | 130.0 | end-users | True | 128552.0 | 76.5% | 74.8% | -1.7 |
| 130.0 | 140.0 | app1 | True | 41962.0 | 23.5% | 24.8% | 1.3 |
| 130.0 | 140.0 | end-users | True | 127228.0 | 76.5% | 75.2% | -1.3 |
| 140.0 | 150.0 | app1 | True | 41944.0 | 23.5% | 25.0% | 1.5 |
| 140.0 | 150.0 | end-users | True | 125818.0 | 76.5% | 75.0% | -1.5 |
| 150.0 | 160.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 150.0 | 160.0 | end-users | True | 167926.0 | 76.5% | 100.0% | 23.5 |
| 160.0 | 170.0 | app1 | True | 43348.0 | 23.5% | 25.2% | 1.7 |
| 160.0 | 170.0 | end-users | True | 128436.0 | 76.5% | 74.8% | -1.7 |
| 170.0 | 180.0 | app1 | True | 41962.0 | 23.5% | 25.2% | 1.7 |
| 170.0 | 180.0 | end-users | True | 124412.0 | 76.5% | 74.8% | -1.7 |
| 180.0 | 190.0 | app1 | True | 43294.0 | 23.5% | 25.2% | 1.7 |
| 180.0 | 190.0 | end-users | True | 128452.0 | 76.5% | 74.8% | -1.7 |
| 190.0 | 200.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 190.0 | 200.0 | end-users | True | 169062.0 | 76.5% | 100.0% | 23.5 |
| 200.0 | 210.0 | app1 | True | 43324.0 | 23.5% | 25.2% | 1.7 |
| 200.0 | 210.0 | end-users | True | 128300.0 | 76.5% | 74.8% | -1.7 |
| 210.0 | 220.0 | app1 | True | 43238.0 | 23.5% | 25.6% | 2.1 |
| 210.0 | 220.0 | end-users | True | 125686.0 | 76.5% | 74.4% | -2.1 |
| 220.0 | 230.0 | app1 | True | 13502.0 | 23.5% | 8.1% | -15.4 |
| 220.0 | 230.0 | end-users | True | 152848.0 | 76.5% | 91.9% | 15.4 |
| 230.0 | 240.0 | app1 | True | 49982.0 | 23.5% | 29.8% | 6.3 |
| 230.0 | 240.0 | end-users | True | 117822.0 | 76.5% | 70.2% | -6.3 |
| 240.0 | 250.0 | app1 | False | 28340.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 140636.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 14904.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 1352.0 | n/a | n/a | n/a |
| 260.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 769980 | 38197 | 808177.0 | 0.0% | 799034.0 | 846374.0 | -5.6% | True |
| end-users | 3115590 | 155464 | 3271054.0 | 0.0% | 3398144.0 | 3426518.0 | -0.8% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
