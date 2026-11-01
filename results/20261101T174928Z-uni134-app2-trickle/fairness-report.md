# Fairness benchmark: app2-trickle (uni134-app2-trickle)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app2-trickle` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T17:49:30Z` |
| Run end | `2026-11-01T17:53:47Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 618 | 200=618 | 11.2 | 19.0 | 780454.0 | 23.5% | 18.8% | -4.7 |
| app2 | 10.0 | 2 | 46 | 200=46 | 11.2 | 17.6 | 59510.0 | n/a | n/a | n/a |
| end-users | 65.0 | 104 | 2504 | 200=2487, 500=17 | 11.0 | 12.5 | 3304630.0 | 76.5% | 79.7% | 3.3 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 1328.0 | n/a | n/a | n/a |

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
| 0.0 | 220.0 | 220.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 8092.0 | 21.1% | 10.3% | -10.7 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 70392.0 | 68.4% | 89.7% | 21.3 |
| 10.0 | 20.0 | app1 | True | 33828.0 | 21.1% | 19.9% | -1.2 |
| 10.0 | 20.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 10.0 | 20.0 | end-users | True | 133854.0 | 68.4% | 78.6% | 10.1 |
| 20.0 | 30.0 | app1 | True | 43224.0 | 21.1% | 24.2% | 3.2 |
| 20.0 | 30.0 | app2 | True | 2692.0 | 10.5% | 1.5% | -9.0 |
| 20.0 | 30.0 | end-users | True | 132548.0 | 68.4% | 74.3% | 5.9 |
| 30.0 | 40.0 | app1 | True | 43380.0 | 21.1% | 26.5% | 5.4 |
| 30.0 | 40.0 | app2 | True | 2712.0 | 10.5% | 1.7% | -8.9 |
| 30.0 | 40.0 | end-users | True | 117698.0 | 68.4% | 71.9% | 3.4 |
| 40.0 | 50.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 40.0 | 50.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 40.0 | 50.0 | end-users | True | 171884.0 | 68.4% | 99.2% | 30.8 |
| 50.0 | 60.0 | app1 | True | 60854.0 | 21.1% | 36.0% | 14.9 |
| 50.0 | 60.0 | app2 | True | 5418.0 | 10.5% | 3.2% | -7.3 |
| 50.0 | 60.0 | end-users | True | 102916.0 | 68.4% | 60.8% | -7.6 |
| 60.0 | 70.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.2 |
| 60.0 | 70.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 60.0 | 70.0 | end-users | True | 165112.0 | 68.4% | 99.2% | 30.8 |
| 70.0 | 80.0 | app1 | True | 43328.0 | 21.1% | 25.6% | 4.6 |
| 70.0 | 80.0 | app2 | True | 2700.0 | 10.5% | 1.6% | -8.9 |
| 70.0 | 80.0 | end-users | True | 123154.0 | 68.4% | 72.8% | 4.4 |
| 80.0 | 90.0 | app1 | True | 41952.0 | 21.1% | 25.0% | 4.0 |
| 80.0 | 90.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 80.0 | 90.0 | end-users | True | 122988.0 | 68.4% | 73.4% | 4.9 |
| 90.0 | 100.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.3 |
| 90.0 | 100.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 90.0 | 100.0 | end-users | True | 173016.0 | 68.4% | 99.2% | 30.8 |
| 100.0 | 110.0 | app1 | True | 43222.0 | 21.1% | 26.0% | 4.9 |
| 100.0 | 110.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 100.0 | 110.0 | end-users | True | 120342.0 | 68.4% | 72.4% | 4.0 |
| 110.0 | 120.0 | app1 | True | 43286.0 | 21.1% | 25.6% | 4.6 |
| 110.0 | 120.0 | app2 | True | 4074.0 | 10.5% | 2.4% | -8.1 |
| 110.0 | 120.0 | end-users | True | 121656.0 | 68.4% | 72.0% | 3.6 |
| 120.0 | 130.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 120.0 | 130.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 120.0 | 130.0 | end-users | True | 163688.0 | 68.4% | 100.0% | 31.6 |
| 130.0 | 140.0 | app1 | True | 63546.0 | 21.1% | 36.8% | 15.7 |
| 130.0 | 140.0 | app2 | True | 5368.0 | 10.5% | 3.1% | -7.4 |
| 130.0 | 140.0 | end-users | True | 103984.0 | 68.4% | 60.1% | -8.3 |
| 140.0 | 150.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 140.0 | 150.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 140.0 | 150.0 | end-users | True | 167784.0 | 68.4% | 100.0% | 31.6 |
| 150.0 | 160.0 | app1 | True | 43320.0 | 21.1% | 26.0% | 5.0 |
| 150.0 | 160.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 150.0 | 160.0 | end-users | True | 120442.0 | 68.4% | 72.3% | 3.9 |
| 160.0 | 170.0 | app1 | True | 43268.0 | 21.1% | 25.4% | 4.3 |
| 160.0 | 170.0 | app2 | True | 4074.0 | 10.5% | 2.4% | -8.1 |
| 160.0 | 170.0 | end-users | True | 123084.0 | 68.4% | 72.2% | 3.8 |
| 170.0 | 180.0 | app1 | True | 43216.0 | 21.1% | 25.8% | 4.7 |
| 170.0 | 180.0 | app2 | True | 2706.0 | 10.5% | 1.6% | -8.9 |
| 170.0 | 180.0 | end-users | True | 121816.0 | 68.4% | 72.6% | 4.2 |
| 180.0 | 190.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 180.0 | 190.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 180.0 | 190.0 | end-users | True | 166318.0 | 68.4% | 100.0% | 31.6 |
| 190.0 | 200.0 | app1 | True | 43368.0 | 21.1% | 26.1% | 5.0 |
| 190.0 | 200.0 | app2 | True | 2684.0 | 10.5% | 1.6% | -8.9 |
| 190.0 | 200.0 | end-users | True | 120406.0 | 68.4% | 72.3% | 3.9 |
| 200.0 | 210.0 | app1 | True | 45930.0 | 21.1% | 27.2% | 6.1 |
| 200.0 | 210.0 | app2 | True | 4044.0 | 10.5% | 2.4% | -8.1 |
| 200.0 | 210.0 | end-users | True | 118994.0 | 68.4% | 70.4% | 2.0 |
| 210.0 | 220.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 210.0 | 220.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 210.0 | 220.0 | end-users | True | 167734.0 | 68.4% | 100.0% | 31.6 |
| 220.0 | 230.0 | app1 | True | 43258.0 | 21.1% | 26.0% | 4.9 |
| 220.0 | 230.0 | app2 | True | 2704.0 | 10.5% | 1.6% | -8.9 |
| 220.0 | 230.0 | end-users | True | 120482.0 | 68.4% | 72.4% | 4.0 |
| 230.0 | 240.0 | app1 | True | 48734.0 | 21.1% | 29.1% | 8.0 |
| 230.0 | 240.0 | app2 | True | 5418.0 | 10.5% | 3.2% | -7.3 |
| 230.0 | 240.0 | end-users | True | 113582.0 | 68.4% | 67.7% | -0.7 |
| 240.0 | 250.0 | app1 | False | 41932.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 2694.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 120434.0 | n/a | n/a | n/a |
| 250.0 | 257.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 257.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 257.0 | end-users | False | 20322.0 | n/a | n/a | n/a |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
