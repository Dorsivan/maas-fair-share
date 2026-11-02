# Fairness benchmark: full-contention (b1-cold-join)

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
| Run start | `2026-11-02T00:53:27Z` |
| Run end | `2026-11-02T00:57:49Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1607 | 200=1584, 500=23 | 1.6 | 25.2 | 504728.0 | 21.1% | 20.2% | -0.9 | 4.1s | 98.8% | 1583.0 |
| app2 | 10.0 | 32 | 1560 | 200=1550, 500=10 | 1.6 | 25.3 | 453126.0 | 10.5% | 18.1% | 7.6 | 4.2s | 98.1% | 1550.0 |
| end-users | 65.0 | 128 | 1185 | 200=1185 | 10.7 | 18.8 | 1543170.0 | 68.4% | 61.7% | -6.7 | 4.1s | 98.9% | 1185.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 98.3% | 1.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- end-users: active 120s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 120.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 16234.0 | 66.7% | 49.9% | -16.7 |
| 0.0 | 10.0 | app2 | True | 16268.0 | 33.3% | 50.1% | 16.7 |
| 0.0 | 10.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | True | 12212.0 | 66.7% | 45.1% | -21.5 |
| 10.0 | 20.0 | app2 | True | 14836.0 | 33.3% | 54.9% | 21.5 |
| 10.0 | 20.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 20.0 | 30.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 20.0 | 30.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 30.0 | 40.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 30.0 | 40.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 40.0 | 50.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 40.0 | 50.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 50.0 | 60.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 50.0 | 60.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 60.0 | 70.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 60.0 | 70.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | True | 12188.0 | 66.7% | 50.2% | -16.5 |
| 70.0 | 80.0 | app2 | True | 12106.0 | 33.3% | 49.8% | 16.5 |
| 70.0 | 80.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | True | 2708.0 | 66.7% | 66.6% | -0.1 |
| 80.0 | 90.0 | app2 | True | 1358.0 | 33.3% | 33.4% | 0.1 |
| 80.0 | 90.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app1 | True | 0.0 | 66.7% | 0.0% | -66.7 |
| 90.0 | 100.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 90.0 | 100.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 100.0 | 110.0 | app1 | True | 51364.0 | 66.7% | 51.4% | -15.3 |
| 100.0 | 110.0 | app2 | True | 48598.0 | 33.3% | 48.6% | 15.3 |
| 100.0 | 110.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app1 | True | 35250.0 | 66.7% | 48.2% | -18.5 |
| 110.0 | 120.0 | app2 | True | 37898.0 | 33.3% | 51.8% | 18.5 |
| 110.0 | 120.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | True | 48686.0 | 21.1% | 29.0% | 8.0 |
| 120.0 | 130.0 | app2 | True | 42016.0 | 10.5% | 25.0% | 14.5 |
| 120.0 | 130.0 | end-users | True | 77112.0 | 68.4% | 46.0% | -22.5 |
| 130.0 | 140.0 | app1 | True | 2716.0 | 21.1% | 1.6% | -19.5 |
| 130.0 | 140.0 | app2 | True | 1348.0 | 10.5% | 0.8% | -9.7 |
| 130.0 | 140.0 | end-users | True | 166244.0 | 68.4% | 97.6% | 29.2 |
| 140.0 | 150.0 | app1 | True | 68970.0 | 21.1% | 41.5% | 20.4 |
| 140.0 | 150.0 | app2 | True | 55508.0 | 10.5% | 33.4% | 22.8 |
| 140.0 | 150.0 | end-users | True | 41888.0 | 68.4% | 25.2% | -43.2 |
| 150.0 | 160.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 150.0 | 160.0 | app2 | True | 2706.0 | 10.5% | 1.7% | -8.8 |
| 150.0 | 160.0 | end-users | True | 156960.0 | 68.4% | 98.3% | 29.9 |
| 160.0 | 170.0 | app1 | True | 5432.0 | 21.1% | 3.4% | -17.6 |
| 160.0 | 170.0 | app2 | True | 3994.0 | 10.5% | 2.5% | -8.0 |
| 160.0 | 170.0 | end-users | True | 148954.0 | 68.4% | 94.0% | 25.6 |
| 170.0 | 180.0 | app1 | True | 62238.0 | 21.1% | 36.5% | 15.5 |
| 170.0 | 180.0 | app2 | True | 51410.0 | 10.5% | 30.2% | 19.7 |
| 170.0 | 180.0 | end-users | True | 56700.0 | 68.4% | 33.3% | -35.1 |
| 180.0 | 190.0 | app1 | True | 1356.0 | 21.1% | 0.8% | -20.3 |
| 180.0 | 190.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 180.0 | 190.0 | end-users | True | 168896.0 | 68.4% | 98.4% | 30.0 |
| 190.0 | 200.0 | app1 | True | 44550.0 | 21.1% | 27.4% | 6.4 |
| 190.0 | 200.0 | app2 | True | 20318.0 | 10.5% | 12.5% | 2.0 |
| 190.0 | 200.0 | end-users | True | 97452.0 | 68.4% | 60.0% | -8.4 |
| 200.0 | 210.0 | app1 | True | 25702.0 | 21.1% | 16.5% | -4.5 |
| 200.0 | 210.0 | app2 | True | 36514.0 | 10.5% | 23.5% | 12.9 |
| 200.0 | 210.0 | end-users | True | 93396.0 | 68.4% | 60.0% | -8.4 |
| 210.0 | 220.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 210.0 | 220.0 | app2 | True | 6778.0 | 10.5% | 3.9% | -6.6 |
| 210.0 | 220.0 | end-users | True | 167750.0 | 68.4% | 96.1% | 27.7 |
| 220.0 | 230.0 | app1 | True | 43392.0 | 21.1% | 26.3% | 5.2 |
| 220.0 | 230.0 | app2 | True | 55480.0 | 10.5% | 33.6% | 23.1 |
| 220.0 | 230.0 | end-users | True | 66306.0 | 68.4% | 40.1% | -28.3 |
| 230.0 | 240.0 | app1 | True | 28412.0 | 21.1% | 18.0% | -3.1 |
| 230.0 | 240.0 | app2 | True | 1354.0 | 10.5% | 0.9% | -9.7 |
| 230.0 | 240.0 | end-users | True | 128260.0 | 68.4% | 81.2% | 12.7 |
| 240.0 | 250.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 165106.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 43318.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 43278.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 8146.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -76.4%
- app2 exceeded the 10% ledger tolerance: cost -78.4%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1948320 | 97377 | 2044405.0 | -0.1% | 504728.0 | 2143074.0 | -76.4% | False |
| app2 | 1906500 | 94858 | 2001358.0 | 0.0% | 453126.0 | 2096216.0 | -78.4% | False |
| end-users | 1457550 | 72580 | 1530130.0 | 0.0% | 1543170.0 | 1602710.0 | -3.7% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
