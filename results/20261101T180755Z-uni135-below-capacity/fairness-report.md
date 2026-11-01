# Fairness benchmark: below-capacity (uni135-below-capacity)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `below-capacity` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T18:07:56Z` |
| Run end | `2026-11-01T18:12:09Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 6 | 806 | 200=803, 500=3 | 1.8 | 2.2 | 1072764.0 | 21.1% | 14.9% | -6.1 | 2.4s |
| app2 | 10.0 | 6 | 784 | 200=784 | 1.9 | 2.3 | 1050682.0 | 10.5% | 14.6% | 4.1 | 2.3s |
| end-users | 65.0 | 26 | 3796 | 200=3789, 500=7 | 1.6 | 2.0 | 5069178.0 | 68.4% | 70.5% | 2.1 | 2.5s |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s |

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
| 0.0 | 0.0 | 0.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 29816.0 | 21.1% | 15.2% | -5.9 |
| 0.0 | 10.0 | app2 | True | 27074.0 | 10.5% | 13.8% | 3.3 |
| 0.0 | 10.0 | end-users | True | 139444.0 | 68.4% | 71.0% | 2.6 |
| 10.0 | 20.0 | app1 | True | 43384.0 | 21.1% | 14.4% | -6.7 |
| 10.0 | 20.0 | app2 | True | 44668.0 | 10.5% | 14.8% | 4.3 |
| 10.0 | 20.0 | end-users | True | 213822.0 | 68.4% | 70.8% | 2.4 |
| 20.0 | 30.0 | app1 | True | 44584.0 | 21.1% | 15.0% | -6.1 |
| 20.0 | 30.0 | app2 | True | 47364.0 | 10.5% | 15.9% | 5.4 |
| 20.0 | 30.0 | end-users | True | 205600.0 | 68.4% | 69.1% | 0.7 |
| 30.0 | 40.0 | app1 | True | 41996.0 | 21.1% | 14.0% | -7.1 |
| 30.0 | 40.0 | app2 | True | 42016.0 | 10.5% | 14.0% | 3.5 |
| 30.0 | 40.0 | end-users | True | 216366.0 | 68.4% | 72.0% | 3.6 |
| 40.0 | 50.0 | app1 | True | 44634.0 | 21.1% | 14.5% | -6.6 |
| 40.0 | 50.0 | app2 | True | 44602.0 | 10.5% | 14.5% | 3.9 |
| 40.0 | 50.0 | end-users | True | 218978.0 | 68.4% | 71.0% | 2.6 |
| 50.0 | 60.0 | app1 | True | 44634.0 | 21.1% | 14.9% | -6.2 |
| 50.0 | 60.0 | app2 | True | 43254.0 | 10.5% | 14.4% | 3.9 |
| 50.0 | 60.0 | end-users | True | 212450.0 | 68.4% | 70.7% | 2.3 |
| 60.0 | 70.0 | app1 | True | 44616.0 | 21.1% | 14.6% | -6.5 |
| 60.0 | 70.0 | app2 | True | 41964.0 | 10.5% | 13.7% | 3.2 |
| 60.0 | 70.0 | end-users | True | 218974.0 | 68.4% | 71.7% | 3.2 |
| 70.0 | 80.0 | app1 | True | 43308.0 | 21.1% | 14.4% | -6.7 |
| 70.0 | 80.0 | app2 | True | 43190.0 | 10.5% | 14.3% | 3.8 |
| 70.0 | 80.0 | end-users | True | 215106.0 | 68.4% | 71.3% | 2.9 |
| 80.0 | 90.0 | app1 | True | 44610.0 | 21.1% | 14.8% | -6.3 |
| 80.0 | 90.0 | app2 | True | 46008.0 | 10.5% | 15.3% | 4.7 |
| 80.0 | 90.0 | end-users | True | 211060.0 | 68.4% | 70.0% | 1.5 |
| 90.0 | 100.0 | app1 | True | 48746.0 | 21.1% | 16.0% | -5.0 |
| 90.0 | 100.0 | app2 | True | 49924.0 | 10.5% | 16.4% | 5.9 |
| 90.0 | 100.0 | end-users | True | 205716.0 | 68.4% | 67.6% | -0.8 |
| 100.0 | 110.0 | app1 | True | 43326.0 | 21.1% | 14.4% | -6.7 |
| 100.0 | 110.0 | app2 | True | 41950.0 | 10.5% | 13.9% | 3.4 |
| 100.0 | 110.0 | end-users | True | 216452.0 | 68.4% | 71.7% | 3.3 |
| 110.0 | 120.0 | app1 | True | 44558.0 | 21.1% | 14.7% | -6.3 |
| 110.0 | 120.0 | app2 | True | 44538.0 | 10.5% | 14.7% | 4.2 |
| 110.0 | 120.0 | end-users | True | 213626.0 | 68.4% | 70.6% | 2.1 |
| 120.0 | 130.0 | app1 | True | 41890.0 | 21.1% | 13.6% | -7.4 |
| 120.0 | 130.0 | app2 | True | 45974.0 | 10.5% | 15.0% | 4.4 |
| 120.0 | 130.0 | end-users | True | 219200.0 | 68.4% | 71.4% | 3.0 |
| 130.0 | 140.0 | app1 | True | 48690.0 | 21.1% | 16.1% | -4.9 |
| 130.0 | 140.0 | app2 | True | 43218.0 | 10.5% | 14.3% | 3.8 |
| 130.0 | 140.0 | end-users | True | 209654.0 | 68.4% | 69.5% | 1.1 |
| 140.0 | 150.0 | app1 | True | 46016.0 | 21.1% | 15.3% | -5.7 |
| 140.0 | 150.0 | app2 | True | 43240.0 | 10.5% | 14.4% | 3.9 |
| 140.0 | 150.0 | end-users | True | 211152.0 | 68.4% | 70.3% | 1.9 |
| 150.0 | 160.0 | app1 | True | 46050.0 | 21.1% | 15.8% | -5.3 |
| 150.0 | 160.0 | app2 | True | 44636.0 | 10.5% | 15.3% | 4.7 |
| 150.0 | 160.0 | end-users | True | 201616.0 | 68.4% | 69.0% | 0.6 |
| 160.0 | 170.0 | app1 | True | 45952.0 | 21.1% | 15.0% | -6.0 |
| 160.0 | 170.0 | app2 | True | 44636.0 | 10.5% | 14.6% | 4.1 |
| 160.0 | 170.0 | end-users | True | 215174.0 | 68.4% | 70.4% | 2.0 |
| 170.0 | 180.0 | app1 | True | 44626.0 | 21.1% | 14.7% | -6.4 |
| 170.0 | 180.0 | app2 | True | 40544.0 | 10.5% | 13.3% | 2.8 |
| 170.0 | 180.0 | end-users | True | 219130.0 | 68.4% | 72.0% | 3.6 |
| 180.0 | 190.0 | app1 | True | 44660.0 | 21.1% | 15.0% | -6.0 |
| 180.0 | 190.0 | app2 | True | 41874.0 | 10.5% | 14.1% | 3.5 |
| 180.0 | 190.0 | end-users | True | 211006.0 | 68.4% | 70.9% | 2.5 |
| 190.0 | 200.0 | app1 | True | 47370.0 | 21.1% | 15.6% | -5.5 |
| 190.0 | 200.0 | app2 | True | 44644.0 | 10.5% | 14.7% | 4.1 |
| 190.0 | 200.0 | end-users | True | 212558.0 | 68.4% | 69.8% | 1.4 |
| 200.0 | 210.0 | app1 | True | 44604.0 | 21.1% | 14.7% | -6.3 |
| 200.0 | 210.0 | app2 | True | 47376.0 | 10.5% | 15.6% | 5.1 |
| 200.0 | 210.0 | end-users | True | 211060.0 | 68.4% | 69.6% | 1.2 |
| 210.0 | 220.0 | app1 | True | 45972.0 | 21.1% | 15.4% | -5.7 |
| 210.0 | 220.0 | app2 | True | 47410.0 | 10.5% | 15.9% | 5.3 |
| 210.0 | 220.0 | end-users | True | 205666.0 | 68.4% | 68.8% | 0.4 |
| 220.0 | 230.0 | app1 | True | 45998.0 | 21.1% | 15.0% | -6.0 |
| 220.0 | 230.0 | app2 | True | 41946.0 | 10.5% | 13.7% | 3.2 |
| 220.0 | 230.0 | end-users | True | 217708.0 | 68.4% | 71.2% | 2.8 |
| 230.0 | 241.0 | app1 | True | 44598.0 | 21.1% | 14.8% | -6.3 |
| 230.0 | 241.0 | app2 | True | 40566.0 | 10.5% | 13.4% | 2.9 |
| 230.0 | 241.0 | end-users | True | 216518.0 | 68.4% | 71.8% | 3.3 |
| 241.0 | 251.0 | app1 | False | 8126.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 8066.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 31142.0 | n/a | n/a | n/a |
| 251.0 | 253.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 253.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 253.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
