# Fairness benchmark: asymmetric-demand (uni139-asymmetric-demand-r5)

**Verdict: UNCONTENDED** -- every offered group's `contended_seconds_total` delta stayed under 1s, so the pool was never actually contended. Not scored against the 10-point weighted-split threshold; see docs/runbook.md.

- every offered group's contended_seconds_total delta stayed under 1s (app1=0.98s, end-users=0.98s) -- an order of magnitude below the ~9s a genuinely-contending tenant accrues in a 240s full-contention run (docs/runbook.md), so nobody was ever backlogged alongside anyone else and the weighted-split deviation check does not apply

## Run metadata

| field | value |
|---|---|
| Scenario | `asymmetric-demand` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T21:15:18Z` |
| Run end | `2026-11-01T21:19:41Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 5015 | 200=5000, 500=15 | 1.5 | 1.9 | 4517876.0 | 23.5% | 93.5% | 70.0 | 1.0s | 98.8% | 5000.0 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 97.3% | 0.0 |
| end-users | 65.0 | 2 | 274 | 200=273, 500=1 | 1.7 | 2.1 | 312460.0 | 76.5% | 6.5% | -70.0 | 1.0s | 98.9% | 273.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 90.2% | 0.0 |

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
| 0.0 | 10.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 76.5% | 0.0% | -76.5 |
| 10.0 | 20.0 | app1 | True | 24338.0 | 23.5% | 90.0% | 66.5 |
| 10.0 | 20.0 | end-users | True | 2704.0 | 76.5% | 10.0% | -66.5 |
| 20.0 | 31.0 | app1 | True | 211042.0 | 23.5% | 94.0% | 70.4 |
| 20.0 | 31.0 | end-users | True | 13526.0 | 76.5% | 6.0% | -70.4 |
| 31.0 | 41.0 | app1 | True | 216582.0 | 23.5% | 94.1% | 70.6 |
| 31.0 | 41.0 | end-users | True | 13522.0 | 76.5% | 5.9% | -70.6 |
| 41.0 | 51.0 | app1 | True | 132572.0 | 23.5% | 92.5% | 68.9 |
| 41.0 | 51.0 | end-users | True | 10826.0 | 76.5% | 7.5% | -68.9 |
| 51.0 | 61.0 | app1 | True | 178452.0 | 23.5% | 93.0% | 69.4 |
| 51.0 | 61.0 | end-users | True | 13530.0 | 76.5% | 7.0% | -69.4 |
| 61.0 | 71.0 | app1 | True | 173064.0 | 23.5% | 92.8% | 69.2 |
| 61.0 | 71.0 | end-users | True | 13524.0 | 76.5% | 7.2% | -69.2 |
| 71.0 | 81.0 | app1 | True | 177130.0 | 23.5% | 92.2% | 68.7 |
| 71.0 | 81.0 | end-users | True | 14896.0 | 76.5% | 7.8% | -68.7 |
| 81.0 | 91.0 | app1 | True | 187914.0 | 23.5% | 93.3% | 69.8 |
| 81.0 | 91.0 | end-users | True | 13530.0 | 76.5% | 6.7% | -69.8 |
| 91.0 | 101.0 | app1 | True | 194748.0 | 23.5% | 94.1% | 70.6 |
| 91.0 | 101.0 | end-users | True | 12188.0 | 76.5% | 5.9% | -70.6 |
| 101.0 | 111.0 | app1 | True | 170270.0 | 23.5% | 93.3% | 69.8 |
| 101.0 | 111.0 | end-users | True | 12170.0 | 76.5% | 6.7% | -69.8 |
| 111.0 | 121.0 | app1 | True | 140836.0 | 23.5% | 90.4% | 66.9 |
| 111.0 | 121.0 | end-users | True | 14884.0 | 76.5% | 9.6% | -66.9 |
| 121.0 | 131.0 | app1 | True | 227202.0 | 23.5% | 95.4% | 71.9 |
| 121.0 | 131.0 | end-users | True | 10836.0 | 76.5% | 4.6% | -71.9 |
| 131.0 | 141.0 | app1 | True | 78372.0 | 23.5% | 92.1% | 68.5 |
| 131.0 | 141.0 | end-users | True | 6742.0 | 76.5% | 7.9% | -68.5 |
| 141.0 | 151.0 | app1 | True | 178470.0 | 23.5% | 92.9% | 69.4 |
| 141.0 | 151.0 | end-users | True | 13538.0 | 76.5% | 7.1% | -69.4 |
| 151.0 | 161.0 | app1 | True | 259834.0 | 23.5% | 95.1% | 71.5 |
| 151.0 | 161.0 | end-users | True | 13488.0 | 76.5% | 4.9% | -71.5 |
| 161.0 | 171.0 | app1 | True | 221888.0 | 23.5% | 94.2% | 70.7 |
| 161.0 | 171.0 | end-users | True | 13570.0 | 76.5% | 5.8% | -70.7 |
| 171.0 | 181.0 | app1 | True | 204208.0 | 23.5% | 95.0% | 71.4 |
| 171.0 | 181.0 | end-users | True | 10798.0 | 76.5% | 5.0% | -71.4 |
| 181.0 | 191.0 | app1 | True | 242002.0 | 23.5% | 94.2% | 70.7 |
| 181.0 | 191.0 | end-users | True | 14840.0 | 76.5% | 5.8% | -70.7 |
| 191.0 | 201.0 | app1 | True | 141938.0 | 23.5% | 92.9% | 69.4 |
| 191.0 | 201.0 | end-users | True | 10814.0 | 76.5% | 7.1% | -69.4 |
| 201.0 | 211.0 | app1 | True | 224342.0 | 23.5% | 93.2% | 69.7 |
| 201.0 | 211.0 | end-users | True | 16252.0 | 76.5% | 6.8% | -69.7 |
| 211.0 | 221.0 | app1 | True | 221710.0 | 23.5% | 93.7% | 70.2 |
| 211.0 | 221.0 | end-users | True | 14898.0 | 76.5% | 6.3% | -70.2 |
| 221.0 | 231.0 | app1 | True | 182486.0 | 23.5% | 93.1% | 69.6 |
| 221.0 | 231.0 | end-users | True | 13524.0 | 76.5% | 6.9% | -69.6 |
| 231.0 | 241.0 | app1 | True | 147324.0 | 23.5% | 93.2% | 69.6 |
| 231.0 | 241.0 | end-users | True | 10814.0 | 76.5% | 6.8% | -69.6 |
| 241.0 | 251.0 | app1 | False | 229880.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 16184.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 151272.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 10862.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -33.2%
- end-users exceeded the 10% ledger tolerance: cost -15.4%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 6150000 | 306134 | 6456134.0 | 0.0% | 4517876.0 | 6762268.0 | -33.2% | False |
| end-users | 335790 | 16743 | 352533.0 | 0.0% | 312460.0 | 369276.0 | -15.4% | False |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
