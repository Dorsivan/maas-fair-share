# Fairness benchmark: full-contention (uni140-b6-full-contention-soak)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `5700` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T22:42:18Z` |
| Run end | `2026-11-01T23:24:13Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 0 | n/a | n/a | n/a | 6942392.0 | 21.1% | 16.9% | -4.1 | 63.4s | 98.8% | 5173.0 |
| app2 | 10.0 | 32 | 0 | n/a | n/a | n/a | 5691444.0 | 10.5% | 13.9% | 3.3 | 58.3s | 97.8% | 4274.0 |
| end-users | 65.0 | 128 | 0 | n/a | n/a | n/a | 28415620.0 | 68.4% | 69.2% | 0.8 | 63.2s | 98.9% | 21134.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 14834.0 | n/a | n/a | n/a | 0.0s | 98.2% | 12.0 |

## Timeline (UNI-127)

Window size: 300s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-5700s, no duty cycle
- app2: active 0s-5700s, no duty cycle
- end-users: active 0s-5700s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 0.0 | 0.0 |
| 5700.0 | n/a (never converged in this phase) | n/a |

**Windows** (9 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 300.0 | app1 | True | 849426.0 | 21.1% | 17.5% | -3.5 |
| 0.0 | 300.0 | app2 | True | 698964.0 | 10.5% | 14.4% | 3.9 |
| 0.0 | 300.0 | end-users | True | 3304028.0 | 68.4% | 68.1% | -0.3 |
| 300.0 | 600.0 | app1 | True | 794206.0 | 21.1% | 16.2% | -4.9 |
| 300.0 | 600.0 | app2 | True | 668258.0 | 10.5% | 13.6% | 3.1 |
| 300.0 | 600.0 | end-users | True | 3441004.0 | 68.4% | 70.2% | 1.8 |
| 600.0 | 900.0 | app1 | True | 833314.0 | 21.1% | 17.0% | -4.1 |
| 600.0 | 900.0 | app2 | True | 699218.0 | 10.5% | 14.3% | 3.7 |
| 600.0 | 900.0 | end-users | True | 3369090.0 | 68.4% | 68.7% | 0.3 |
| 900.0 | 1200.0 | app1 | True | 840082.0 | 21.1% | 17.2% | -3.9 |
| 900.0 | 1200.0 | app2 | True | 664336.0 | 10.5% | 13.6% | 3.1 |
| 900.0 | 1200.0 | end-users | True | 3387728.0 | 68.4% | 69.2% | 0.8 |
| 1200.0 | 1500.0 | app1 | True | 815808.0 | 21.1% | 16.6% | -4.4 |
| 1200.0 | 1500.0 | app2 | True | 658770.0 | 10.5% | 13.4% | 2.9 |
| 1200.0 | 1500.0 | end-users | True | 3430254.0 | 68.4% | 69.9% | 1.5 |
| 1500.0 | 1800.0 | app1 | True | 838996.0 | 21.1% | 17.1% | -3.9 |
| 1500.0 | 1800.0 | app2 | True | 676224.0 | 10.5% | 13.8% | 3.3 |
| 1500.0 | 1800.0 | end-users | True | 3386674.0 | 68.4% | 69.1% | 0.7 |
| 1800.0 | 2100.0 | app1 | True | 812918.0 | 21.1% | 16.5% | -4.5 |
| 1800.0 | 2100.0 | app2 | True | 655756.0 | 10.5% | 13.3% | 2.8 |
| 1800.0 | 2100.0 | end-users | True | 3451452.0 | 68.4% | 70.1% | 1.7 |
| 2100.0 | 2400.0 | app1 | True | 818116.0 | 21.1% | 16.7% | -4.4 |
| 2100.0 | 2400.0 | app2 | True | 731766.0 | 10.5% | 14.9% | 4.4 |
| 2100.0 | 2400.0 | end-users | True | 3350636.0 | 68.4% | 68.4% | -0.0 |
| 2400.0 | 2515.0 | app1 | True | 339526.0 | 21.1% | 18.1% | -2.9 |
| 2400.0 | 2515.0 | app2 | True | 238152.0 | 10.5% | 12.7% | 2.2 |
| 2400.0 | 2515.0 | end-users | True | 1294754.0 | 68.4% | 69.1% | 0.7 |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app2 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- end-users was offered load but has no client-side record (client-request-summary.jsonl is missing its line)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | n/a | n/a | n/a | n/a | 6942392.0 | n/a | n/a | None |
| app2 | n/a | n/a | n/a | n/a | 5691444.0 | n/a | n/a | None |
| end-users | n/a | n/a | n/a | n/a | 28415620.0 | n/a | n/a | None |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
