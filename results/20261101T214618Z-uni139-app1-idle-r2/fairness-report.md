# Fairness benchmark: app1-idle (uni139-app1-idle-r2)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-idle` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T21:46:19Z` |
| Run end | `2026-11-01T21:50:52Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 98.8% | 0.0 |
| app2 | 10.0 | 32 | 138 | 200=136, 500=2 | 20.2 | 201.0 | 144770.0 | 13.3% | 3.5% | -9.8 | 18.0s | 97.3% | 136.0 |
| end-users | 65.0 | 208 | 3036 | 200=3012, 500=24 | 17.4 | 20.6 | 3954628.0 | 86.7% | 96.5% | 9.8 | 18.0s | 98.9% | 3012.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 95.7% | 0.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app2: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 200.0 | 200.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (28 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 0.0 | 10.0 | end-users | True | 9506.0 | 86.7% | 100.0% | 13.3 |
| 10.0 | 20.0 | app2 | True | 24386.0 | 13.3% | 15.3% | 1.9 |
| 10.0 | 20.0 | end-users | True | 135246.0 | 86.7% | 84.7% | -1.9 |
| 20.0 | 30.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 20.0 | 30.0 | end-users | True | 155606.0 | 86.7% | 100.0% | 13.3 |
| 30.0 | 40.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 30.0 | 40.0 | end-users | True | 173294.0 | 86.7% | 100.0% | 13.3 |
| 40.0 | 50.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 40.0 | 50.0 | end-users | True | 169024.0 | 86.7% | 100.0% | 13.3 |
| 50.0 | 60.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 50.0 | 60.0 | end-users | True | 166570.0 | 86.7% | 100.0% | 13.3 |
| 60.0 | 70.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 60.0 | 70.0 | end-users | True | 151598.0 | 86.7% | 100.0% | 13.3 |
| 70.0 | 80.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 70.0 | 80.0 | end-users | True | 174348.0 | 86.7% | 100.0% | 13.3 |
| 80.0 | 90.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 80.0 | 90.0 | end-users | True | 165156.0 | 86.7% | 100.0% | 13.3 |
| 90.0 | 100.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 90.0 | 100.0 | end-users | True | 152836.0 | 86.7% | 100.0% | 13.3 |
| 100.0 | 110.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 100.0 | 110.0 | end-users | True | 169138.0 | 86.7% | 100.0% | 13.3 |
| 110.0 | 120.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 110.0 | 120.0 | end-users | True | 168854.0 | 86.7% | 100.0% | 13.3 |
| 120.0 | 130.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 120.0 | 130.0 | end-users | True | 169012.0 | 86.7% | 100.0% | 13.3 |
| 130.0 | 140.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 130.0 | 140.0 | end-users | True | 151662.0 | 86.7% | 100.0% | 13.3 |
| 140.0 | 150.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 140.0 | 150.0 | end-users | True | 170370.0 | 86.7% | 100.0% | 13.3 |
| 150.0 | 160.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 150.0 | 160.0 | end-users | True | 168982.0 | 86.7% | 100.0% | 13.3 |
| 160.0 | 170.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 160.0 | 170.0 | end-users | True | 152934.0 | 86.7% | 100.0% | 13.3 |
| 170.0 | 180.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 170.0 | 180.0 | end-users | True | 169140.0 | 86.7% | 100.0% | 13.3 |
| 180.0 | 190.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 180.0 | 190.0 | end-users | True | 166366.0 | 86.7% | 100.0% | 13.3 |
| 190.0 | 200.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 190.0 | 200.0 | end-users | True | 174484.0 | 86.7% | 100.0% | 13.3 |
| 200.0 | 210.0 | app2 | True | 14808.0 | 13.3% | 9.8% | -3.6 |
| 200.0 | 210.0 | end-users | True | 136786.0 | 86.7% | 90.2% | 3.6 |
| 210.0 | 220.0 | app2 | True | 21630.0 | 13.3% | 12.7% | -0.6 |
| 210.0 | 220.0 | end-users | True | 148714.0 | 86.7% | 87.3% | 0.6 |
| 220.0 | 230.0 | app2 | True | 20308.0 | 13.3% | 13.5% | 0.2 |
| 220.0 | 230.0 | end-users | True | 130038.0 | 86.7% | 86.5% | -0.2 |
| 230.0 | 240.0 | app2 | True | 21644.0 | 13.3% | 13.1% | -0.2 |
| 230.0 | 240.0 | end-users | True | 143478.0 | 86.7% | 86.9% | 0.2 |
| 240.0 | 250.0 | app2 | False | 29790.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 131246.0 | n/a | n/a | n/a |
| 250.0 | 261.0 | app2 | False | 12204.0 | n/a | n/a | n/a |
| 250.0 | 261.0 | end-users | False | 146166.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 4074.0 | n/a | n/a | n/a |
| 271.0 | 273.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 273.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -21.3%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app2 | 167280 | 8374 | 175654.0 | 0.0% | 144770.0 | 184028.0 | -21.3% | False |
| end-users | 3704760 | 185101 | 3889861.0 | 0.0% | 3954628.0 | 4074962.0 | -3.0% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
