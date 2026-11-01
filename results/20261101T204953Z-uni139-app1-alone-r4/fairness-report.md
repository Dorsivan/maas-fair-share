# Fairness benchmark: app1-alone (uni139-app1-alone-r4)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-alone` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T20:49:54Z` |
| Run end | `2026-11-01T20:54:07Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 5382 | 200=5382 | 1.4 | 1.7 | 0.0 | n/a | n/a | n/a | 0.0s | 98.8% | 5382.0 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 97.3% | 0.0 |
| end-users | 65.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 98.9% | 0.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 90.2% | 0.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 10.0 | 20.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 20.0 | 30.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 30.0 | 41.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 41.0 | 51.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 51.0 | 61.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 61.0 | 71.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 71.0 | 81.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 81.0 | 91.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 91.0 | 101.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 101.0 | 111.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 111.0 | 121.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 121.0 | 131.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 131.0 | 141.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 141.0 | 151.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 151.0 | 161.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 161.0 | 171.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 171.0 | 181.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 181.0 | 191.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 191.0 | 201.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 201.0 | 211.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 211.0 | 221.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 221.0 | 231.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 231.0 | 241.0 | app1 | True | 0.0 | 100.0% | 0.0% | -100.0 |
| 241.0 | 251.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 253.0 | app1 | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -100.0%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 6619860 | 330350 | 6950210.0 | 0.0% | 0.0 | 7280560.0 | -100.0% | False |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
