# Fairness benchmark: end-users-idle (uni139-end-users-idle-r4)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `end-users-idle` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T20:23:45Z` |
| Run end | `2026-11-01T20:27:57Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 64 | 2332 | 200=2308, 500=24 | 7.2 | 8.8 | 2987044.0 | 66.7% | 69.0% | 2.4 | 1.4s | 98.6% | 2308.0 |
| app2 | 10.0 | 32 | 1027 | 200=1018, 500=9 | 7.3 | 11.2 | 1340440.0 | 33.3% | 31.0% | -2.4 | 1.4s | 97.2% | 1018.0 |
| end-users | 65.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 98.9% | 0.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 90.2% | 0.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 221.0 | 221.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 83772.0 | 66.7% | 79.5% | 12.8 |
| 0.0 | 10.0 | app2 | True | 21580.0 | 33.3% | 20.5% | -12.8 |
| 10.0 | 20.0 | app1 | True | 89288.0 | 66.7% | 50.8% | -15.9 |
| 10.0 | 20.0 | app2 | True | 86540.0 | 33.3% | 49.2% | 15.9 |
| 20.0 | 30.0 | app1 | True | 130004.0 | 66.7% | 75.6% | 8.9 |
| 20.0 | 30.0 | app2 | True | 42032.0 | 33.3% | 24.4% | -8.9 |
| 30.0 | 40.0 | app1 | True | 128438.0 | 66.7% | 67.3% | 0.7 |
| 30.0 | 40.0 | app2 | True | 62354.0 | 33.3% | 32.7% | -0.7 |
| 40.0 | 50.0 | app1 | True | 140764.0 | 66.7% | 77.0% | 10.4 |
| 40.0 | 50.0 | app2 | True | 42006.0 | 33.3% | 23.0% | -10.4 |
| 50.0 | 60.0 | app1 | True | 117656.0 | 66.7% | 64.9% | -1.7 |
| 50.0 | 60.0 | app2 | True | 63536.0 | 33.3% | 35.1% | 1.7 |
| 60.0 | 70.0 | app1 | True | 114962.0 | 66.7% | 64.4% | -2.2 |
| 60.0 | 70.0 | app2 | True | 63478.0 | 33.3% | 35.6% | 2.2 |
| 70.0 | 80.0 | app1 | True | 123188.0 | 66.7% | 66.0% | -0.7 |
| 70.0 | 80.0 | app2 | True | 63568.0 | 33.3% | 34.0% | 0.7 |
| 80.0 | 90.0 | app1 | True | 148846.0 | 66.7% | 77.5% | 10.8 |
| 80.0 | 90.0 | app2 | True | 43212.0 | 33.3% | 22.5% | -10.8 |
| 90.0 | 100.0 | app1 | True | 120430.0 | 66.7% | 73.6% | 6.9 |
| 90.0 | 100.0 | app2 | True | 43306.0 | 33.3% | 26.4% | -6.9 |
| 100.0 | 110.0 | app1 | True | 94752.0 | 66.7% | 52.2% | -14.4 |
| 100.0 | 110.0 | app2 | True | 86602.0 | 33.3% | 47.8% | 14.4 |
| 110.0 | 120.0 | app1 | True | 131114.0 | 66.7% | 68.3% | 1.6 |
| 110.0 | 120.0 | app2 | True | 60914.0 | 33.3% | 31.7% | -1.6 |
| 120.0 | 130.0 | app1 | True | 118848.0 | 66.7% | 72.7% | 6.0 |
| 120.0 | 130.0 | app2 | True | 44708.0 | 33.3% | 27.3% | -6.0 |
| 130.0 | 140.0 | app1 | True | 148896.0 | 66.7% | 77.5% | 10.8 |
| 130.0 | 140.0 | app2 | True | 43280.0 | 33.3% | 22.5% | -10.8 |
| 140.0 | 150.0 | app1 | True | 139366.0 | 66.7% | 76.3% | 9.6 |
| 140.0 | 150.0 | app2 | True | 43290.0 | 33.3% | 23.7% | -9.6 |
| 150.0 | 160.0 | app1 | True | 104256.0 | 66.7% | 61.6% | -5.1 |
| 150.0 | 160.0 | app2 | True | 64948.0 | 33.3% | 38.4% | 5.1 |
| 160.0 | 170.0 | app1 | True | 123108.0 | 66.7% | 66.4% | -0.2 |
| 160.0 | 170.0 | app2 | True | 62158.0 | 33.3% | 33.6% | 0.2 |
| 170.0 | 180.0 | app1 | True | 144710.0 | 66.7% | 77.0% | 10.3 |
| 170.0 | 180.0 | app2 | True | 43292.0 | 33.3% | 23.0% | -10.3 |
| 180.0 | 191.0 | app1 | True | 108230.0 | 66.7% | 63.5% | -3.1 |
| 180.0 | 191.0 | app2 | True | 62150.0 | 33.3% | 36.5% | 3.1 |
| 191.0 | 201.0 | app1 | True | 141970.0 | 66.7% | 76.6% | 10.0 |
| 191.0 | 201.0 | app2 | True | 43264.0 | 33.3% | 23.4% | -10.0 |
| 201.0 | 211.0 | app1 | True | 146042.0 | 66.7% | 77.2% | 10.5 |
| 201.0 | 211.0 | app2 | True | 43232.0 | 33.3% | 22.8% | -10.5 |
| 211.0 | 221.0 | app1 | True | 108130.0 | 66.7% | 56.3% | -10.3 |
| 211.0 | 221.0 | app2 | True | 83872.0 | 33.3% | 43.7% | 10.3 |
| 221.0 | 231.0 | app1 | True | 128588.0 | 66.7% | 76.6% | 10.0 |
| 221.0 | 231.0 | app2 | True | 39212.0 | 33.3% | 23.4% | -10.0 |
| 231.0 | 241.0 | app1 | True | 140840.0 | 66.7% | 75.9% | 9.3 |
| 231.0 | 241.0 | app2 | True | 44620.0 | 33.3% | 24.1% | -9.3 |
| 241.0 | 251.0 | app1 | False | 10846.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 43286.0 | n/a | n/a | n/a |
| 251.0 | 252.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 252.0 | app2 | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2838840 | 141757 | 2980597.0 | 0.0% | 2987044.0 | 3122354.0 | -4.3% | True |
| app2 | 1252140 | 62396 | 1314536.0 | 0.0% | 1340440.0 | 1376932.0 | -2.7% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
