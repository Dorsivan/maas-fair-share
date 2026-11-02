# Fairness benchmark: max-tokens-skew (uni145-c2-max-tokens-skew)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `max-tokens-skew` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-8tmdm` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-02T12:47:32Z` |
| Run end | `2026-11-02T12:51:55Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 64 | 1937 | 200=1922, 500=15 | 8.5 | 10.2 | 2573324.0 | 66.7% | 70.2% | 3.5 | 1.5s | 98.9% | 1922.0 |
| app2 | 10.0 | 32 | 821 | 200=806, 500=15 | 9.3 | 13.8 | 1094148.0 | 33.3% | 29.8% | -3.5 | 1.5s | 98.9% | 806.0 |
| end-users | 65.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 190.0 | 190.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 60770.0 | 66.7% | 70.9% | 4.2 |
| 0.0 | 10.0 | app2 | True | 24924.0 | 33.3% | 29.1% | -4.2 |
| 10.0 | 20.0 | app1 | True | 104478.0 | 66.7% | 71.6% | 5.0 |
| 10.0 | 20.0 | app2 | True | 41378.0 | 33.3% | 28.4% | -5.0 |
| 20.0 | 30.0 | app1 | True | 100786.0 | 66.7% | 65.4% | -1.3 |
| 20.0 | 30.0 | app2 | True | 53436.0 | 33.3% | 34.6% | 1.3 |
| 30.0 | 40.0 | app1 | True | 122724.0 | 66.7% | 78.0% | 11.3 |
| 30.0 | 40.0 | app2 | True | 34608.0 | 33.3% | 22.0% | -11.3 |
| 40.0 | 50.0 | app1 | True | 92398.0 | 66.7% | 63.8% | -2.8 |
| 40.0 | 50.0 | app2 | True | 52366.0 | 33.3% | 36.2% | 2.8 |
| 50.0 | 60.0 | app1 | True | 118408.0 | 66.7% | 73.0% | 6.3 |
| 50.0 | 60.0 | app2 | True | 43902.0 | 33.3% | 27.0% | -6.3 |
| 60.0 | 70.0 | app1 | True | 90526.0 | 66.7% | 59.0% | -7.7 |
| 60.0 | 70.0 | app2 | True | 62950.0 | 33.3% | 41.0% | 7.7 |
| 70.0 | 80.0 | app1 | True | 122878.0 | 66.7% | 73.8% | 7.1 |
| 70.0 | 80.0 | app2 | True | 43654.0 | 33.3% | 26.2% | -7.1 |
| 80.0 | 90.0 | app1 | True | 101904.0 | 66.7% | 68.6% | 1.9 |
| 80.0 | 90.0 | app2 | True | 46690.0 | 33.3% | 31.4% | -1.9 |
| 90.0 | 100.0 | app1 | True | 121062.0 | 66.7% | 76.6% | 9.9 |
| 90.0 | 100.0 | app2 | True | 36952.0 | 33.3% | 23.4% | -9.9 |
| 100.0 | 110.0 | app1 | True | 105888.0 | 66.7% | 67.5% | 0.8 |
| 100.0 | 110.0 | app2 | True | 51032.0 | 33.3% | 32.5% | -0.8 |
| 110.0 | 120.0 | app1 | True | 105654.0 | 66.7% | 70.7% | 4.0 |
| 110.0 | 120.0 | app2 | True | 43776.0 | 33.3% | 29.3% | -4.0 |
| 120.0 | 130.0 | app1 | True | 121094.0 | 66.7% | 73.4% | 6.7 |
| 120.0 | 130.0 | app2 | True | 43976.0 | 33.3% | 26.6% | -6.7 |
| 130.0 | 140.0 | app1 | True | 93252.0 | 66.7% | 64.4% | -2.2 |
| 130.0 | 140.0 | app2 | True | 51484.0 | 33.3% | 35.6% | 2.2 |
| 140.0 | 150.0 | app1 | True | 111650.0 | 66.7% | 72.3% | 5.6 |
| 140.0 | 150.0 | app2 | True | 42864.0 | 33.3% | 27.7% | -5.6 |
| 150.0 | 160.0 | app1 | True | 101960.0 | 66.7% | 67.9% | 1.3 |
| 150.0 | 160.0 | app2 | True | 48148.0 | 33.3% | 32.1% | -1.3 |
| 160.0 | 170.0 | app1 | True | 125566.0 | 66.7% | 89.3% | 22.6 |
| 160.0 | 170.0 | app2 | True | 15050.0 | 33.3% | 10.7% | -22.6 |
| 170.0 | 180.0 | app1 | True | 86676.0 | 66.7% | 54.4% | -12.3 |
| 170.0 | 180.0 | app2 | True | 72622.0 | 33.3% | 45.6% | 12.3 |
| 180.0 | 190.0 | app1 | True | 120054.0 | 66.7% | 86.1% | 19.4 |
| 180.0 | 190.0 | app2 | True | 19426.0 | 33.3% | 13.9% | -19.4 |
| 190.0 | 200.0 | app1 | True | 84934.0 | 66.7% | 65.7% | -1.0 |
| 190.0 | 200.0 | app2 | True | 44400.0 | 33.3% | 34.3% | 1.0 |
| 200.0 | 210.0 | app1 | True | 113954.0 | 66.7% | 71.6% | 4.9 |
| 200.0 | 210.0 | app2 | True | 45234.0 | 33.3% | 28.4% | -4.9 |
| 210.0 | 220.0 | app1 | True | 86544.0 | 66.7% | 67.5% | 0.8 |
| 210.0 | 220.0 | app2 | True | 41654.0 | 33.3% | 32.5% | -0.8 |
| 220.0 | 230.0 | app1 | True | 89284.0 | 66.7% | 65.5% | -1.1 |
| 220.0 | 230.0 | app2 | True | 46980.0 | 33.3% | 34.5% | 1.1 |
| 230.0 | 240.0 | app1 | True | 96084.0 | 66.7% | 69.2% | 2.5 |
| 230.0 | 240.0 | app2 | True | 42824.0 | 33.3% | 30.8% | -2.5 |
| 240.0 | 250.0 | app1 | False | 94796.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 43818.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 263.0 | app2 | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2364060 | 147449 | 2511509.0 | 0.0% | 2573324.0 | 2658958.0 | -3.2% | True |
| app2 | 991380 | 58940 | 1050320.0 | 0.0% | 1094148.0 | 1109260.0 | -1.4% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
