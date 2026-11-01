# Fairness benchmark: cache-heavy-vs-cache-cold (uni136-cache-heavy-vs-cache-cold)

**Verdict: INFO** -- named negative control, not scored against the 10-point threshold. Expected to NOT reproduce the configured weights; see docs/runbook.md.

- negative control, not scored against the 10-point threshold: max deviation was 1.5 points. This scenario is expected to compress toward equal shares, not reproduce the configured weights -- see docs/runbook.md's 'Per-tenant worker sizing and the saturation check'

## Run metadata

| field | value |
|---|---|
| Scenario | `cache-heavy-vs-cache-cold` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T18:30:25Z` |
| Run end | `2026-11-01T18:34:37Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 64 | 2383 | 200=2373, 500=10 | 6.9 | 8.6 | 727921.0 | 66.7% | 65.1% | -1.5 | 2.0s | 87.6% | 2372.0 |
| app2 | 10.0 | 32 | 1047 | 200=1040, 500=7 | 7.3 | 10.8 | 389716.0 | 33.3% | 34.9% | 1.5 | 2.0s | 6.2% | 1037.0 |
| end-users | 65.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 1460.0 | n/a | n/a | n/a | 0.0s | 23.3% | 4.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 181.0 | 181.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 13589.0 | 66.7% | 62.7% | -3.9 |
| 0.0 | 10.0 | app2 | True | 8069.0 | 33.3% | 37.3% | 3.9 |
| 10.0 | 20.0 | app1 | True | 27067.0 | 66.7% | 60.6% | -6.1 |
| 10.0 | 20.0 | app2 | True | 17597.0 | 33.3% | 39.4% | 6.1 |
| 20.0 | 30.0 | app1 | True | 29284.0 | 66.7% | 61.0% | -5.7 |
| 20.0 | 30.0 | app2 | True | 18747.0 | 33.3% | 39.0% | 5.7 |
| 30.0 | 40.0 | app1 | True | 32211.0 | 66.7% | 68.3% | 1.6 |
| 30.0 | 40.0 | app2 | True | 14958.0 | 33.3% | 31.7% | -1.6 |
| 40.0 | 50.0 | app1 | True | 28539.0 | 66.7% | 62.9% | -3.8 |
| 40.0 | 50.0 | app2 | True | 16834.0 | 33.3% | 37.1% | 3.8 |
| 50.0 | 60.0 | app1 | True | 29669.0 | 66.7% | 66.5% | -0.2 |
| 50.0 | 60.0 | app2 | True | 14970.0 | 33.3% | 33.5% | 0.2 |
| 60.0 | 70.0 | app1 | True | 32566.0 | 66.7% | 68.5% | 1.8 |
| 60.0 | 70.0 | app2 | True | 14967.0 | 33.3% | 31.5% | -1.8 |
| 70.0 | 80.0 | app1 | True | 31123.0 | 66.7% | 65.9% | -0.7 |
| 70.0 | 80.0 | app2 | True | 16070.0 | 33.3% | 34.1% | 0.7 |
| 80.0 | 90.0 | app1 | True | 27902.0 | 66.7% | 60.7% | -6.0 |
| 80.0 | 90.0 | app2 | True | 18054.0 | 33.3% | 39.3% | 6.0 |
| 90.0 | 100.0 | app1 | True | 29208.0 | 66.7% | 64.5% | -2.2 |
| 90.0 | 100.0 | app2 | True | 16099.0 | 33.3% | 35.5% | 2.2 |
| 100.0 | 110.0 | app1 | True | 33009.0 | 66.7% | 71.7% | 5.0 |
| 100.0 | 110.0 | app2 | True | 13018.0 | 33.3% | 28.3% | -5.0 |
| 110.0 | 121.0 | app1 | True | 23413.0 | 66.7% | 52.2% | -14.5 |
| 110.0 | 121.0 | app2 | True | 21447.0 | 33.3% | 47.8% | 14.5 |
| 121.0 | 131.0 | app1 | True | 34869.0 | 66.7% | 79.1% | 12.5 |
| 121.0 | 131.0 | app2 | True | 9195.0 | 33.3% | 20.9% | -12.5 |
| 131.0 | 141.0 | app1 | True | 23001.0 | 66.7% | 49.2% | -17.5 |
| 131.0 | 141.0 | app2 | True | 23777.0 | 33.3% | 50.8% | 17.5 |
| 141.0 | 151.0 | app1 | True | 30289.0 | 66.7% | 63.7% | -3.0 |
| 141.0 | 151.0 | app2 | True | 17268.0 | 33.3% | 36.3% | 3.0 |
| 151.0 | 161.0 | app1 | True | 33004.0 | 66.7% | 72.9% | 6.2 |
| 151.0 | 161.0 | app2 | True | 12291.0 | 33.3% | 27.1% | -6.2 |
| 161.0 | 171.0 | app1 | True | 32820.0 | 66.7% | 72.8% | 6.1 |
| 161.0 | 171.0 | app2 | True | 12291.0 | 33.3% | 27.2% | -6.1 |
| 171.0 | 181.0 | app1 | True | 23705.0 | 66.7% | 49.4% | -17.2 |
| 171.0 | 181.0 | app2 | True | 24251.0 | 33.3% | 50.6% | 17.2 |
| 181.0 | 191.0 | app1 | True | 34877.0 | 66.7% | 74.0% | 7.4 |
| 181.0 | 191.0 | app2 | True | 12240.0 | 33.3% | 26.0% | -7.4 |
| 191.0 | 201.0 | app1 | True | 34038.0 | 66.7% | 73.5% | 6.8 |
| 191.0 | 201.0 | app2 | True | 12297.0 | 33.3% | 26.5% | -6.8 |
| 201.0 | 211.0 | app1 | True | 26988.0 | 66.7% | 60.4% | -6.2 |
| 201.0 | 211.0 | app2 | True | 17665.0 | 33.3% | 39.6% | 6.2 |
| 211.0 | 221.0 | app1 | True | 34951.0 | 66.7% | 74.0% | 7.3 |
| 211.0 | 221.0 | app2 | True | 12292.0 | 33.3% | 26.0% | -7.3 |
| 221.0 | 231.0 | app1 | True | 34476.0 | 66.7% | 73.7% | 7.0 |
| 221.0 | 231.0 | app2 | True | 12305.0 | 33.3% | 26.3% | -7.0 |
| 231.0 | 241.0 | app1 | True | 24582.0 | 66.7% | 57.7% | -9.0 |
| 231.0 | 241.0 | app2 | True | 18041.0 | 33.3% | 42.3% | 9.0 |
| 241.0 | 251.0 | app1 | False | 22741.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 14973.0 | n/a | n/a | n/a |
| 251.0 | 252.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 252.0 | app2 | False | 0.0 | n/a | n/a | n/a |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
