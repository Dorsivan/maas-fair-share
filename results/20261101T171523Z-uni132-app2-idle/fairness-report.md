# Fairness benchmark: app2-idle (uni132-app2-idle)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app2-idle` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T17:15:24Z` |
| Run end | `2026-11-01T17:19:46Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 667 | 200=660, 500=7 | 10.9 | 18.5 | 846908.0 | 23.5% | 20.2% | -3.3 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a |
| end-users | 65.0 | 104 | 2551 | 200=2501, 500=50 | 10.8 | 12.3 | 3347938.0 | 76.5% | 79.8% | 3.3 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a |

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

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 12198.0 | 23.5% | 11.7% | -11.8 |
| 0.0 | 10.0 | end-users | True | 92108.0 | 76.5% | 88.3% | 11.8 |
| 10.0 | 20.0 | app1 | True | 51418.0 | 23.5% | 30.2% | 6.6 |
| 10.0 | 20.0 | end-users | True | 119048.0 | 76.5% | 69.8% | -6.6 |
| 20.0 | 30.0 | app1 | True | 43342.0 | 23.5% | 26.0% | 2.5 |
| 20.0 | 30.0 | end-users | True | 123252.0 | 76.5% | 74.0% | -2.5 |
| 30.0 | 40.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 30.0 | 40.0 | end-users | True | 167806.0 | 76.5% | 100.0% | 23.5 |
| 40.0 | 50.0 | app1 | True | 62240.0 | 23.5% | 36.2% | 12.7 |
| 40.0 | 50.0 | end-users | True | 109584.0 | 76.5% | 63.8% | -12.7 |
| 50.0 | 60.0 | app1 | True | 10816.0 | 23.5% | 6.3% | -17.2 |
| 50.0 | 60.0 | end-users | True | 159724.0 | 76.5% | 93.7% | 17.2 |
| 60.0 | 70.0 | app1 | True | 32500.0 | 23.5% | 19.4% | -4.2 |
| 60.0 | 70.0 | end-users | True | 135228.0 | 76.5% | 80.6% | 4.2 |
| 70.0 | 80.0 | app1 | True | 41870.0 | 23.5% | 24.6% | 1.1 |
| 70.0 | 80.0 | end-users | True | 128412.0 | 76.5% | 75.4% | -1.1 |
| 80.0 | 90.0 | app1 | True | 41910.0 | 23.5% | 23.8% | 0.3 |
| 80.0 | 90.0 | end-users | True | 133826.0 | 76.5% | 76.2% | -0.3 |
| 90.0 | 100.0 | app1 | True | 41968.0 | 23.5% | 23.0% | -0.6 |
| 90.0 | 100.0 | end-users | True | 140744.0 | 76.5% | 77.0% | 0.6 |
| 100.0 | 110.0 | app1 | True | 20318.0 | 23.5% | 12.6% | -10.9 |
| 100.0 | 110.0 | end-users | True | 140730.0 | 76.5% | 87.4% | 10.9 |
| 110.0 | 120.0 | app1 | True | 60986.0 | 23.5% | 35.5% | 11.9 |
| 110.0 | 120.0 | end-users | True | 111002.0 | 76.5% | 64.5% | -11.9 |
| 120.0 | 130.0 | app1 | True | 2714.0 | 23.5% | 1.6% | -21.9 |
| 120.0 | 130.0 | end-users | True | 168988.0 | 76.5% | 98.4% | 21.9 |
| 130.0 | 140.0 | app1 | True | 62182.0 | 23.5% | 37.4% | 13.8 |
| 130.0 | 140.0 | end-users | True | 104204.0 | 76.5% | 62.6% | -13.8 |
| 140.0 | 150.0 | app1 | True | 1334.0 | 23.5% | 0.8% | -22.7 |
| 140.0 | 150.0 | end-users | True | 167646.0 | 76.5% | 99.2% | 22.7 |
| 150.0 | 160.0 | app1 | True | 62242.0 | 23.5% | 36.6% | 13.0 |
| 150.0 | 160.0 | end-users | True | 108036.0 | 76.5% | 63.4% | -13.0 |
| 160.0 | 170.0 | app1 | True | 1324.0 | 23.5% | 0.8% | -22.8 |
| 160.0 | 170.0 | end-users | True | 169212.0 | 76.5% | 99.2% | 22.8 |
| 170.0 | 180.0 | app1 | True | 43292.0 | 23.5% | 25.8% | 2.3 |
| 170.0 | 180.0 | end-users | True | 124420.0 | 76.5% | 74.2% | -2.3 |
| 180.0 | 190.0 | app1 | True | 41958.0 | 23.5% | 25.0% | 1.5 |
| 180.0 | 190.0 | end-users | True | 125768.0 | 76.5% | 75.0% | -1.5 |
| 190.0 | 200.0 | app1 | True | 41910.0 | 23.5% | 24.8% | 1.3 |
| 190.0 | 200.0 | end-users | True | 127148.0 | 76.5% | 75.2% | -1.3 |
| 200.0 | 210.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 200.0 | 210.0 | end-users | True | 171740.0 | 76.5% | 100.0% | 23.5 |
| 210.0 | 220.0 | app1 | True | 63540.0 | 23.5% | 38.2% | 14.7 |
| 210.0 | 220.0 | end-users | True | 102874.0 | 76.5% | 61.8% | -14.7 |
| 220.0 | 230.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 220.0 | 230.0 | end-users | True | 166612.0 | 76.5% | 100.0% | 23.5 |
| 230.0 | 240.0 | app1 | True | 63566.0 | 23.5% | 36.8% | 13.2 |
| 230.0 | 240.0 | end-users | True | 109356.0 | 76.5% | 63.2% | -13.2 |
| 240.0 | 250.0 | app1 | False | 29720.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 140470.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 13560.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation.
