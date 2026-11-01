# Fairness benchmark: app2-trickle (uni139-app2-trickle-r5)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `app2-trickle` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T22:22:15Z` |
| Run end | `2026-11-01T22:26:38Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 646 | 200=646 | 11.3 | 18.7 | 822468.0 | 23.5% | 19.6% | -3.9 | 1.5s | 98.8% | 646.0 |
| app2 | 10.0 | 2 | 51 | 200=51 | 11.0 | 16.3 | 67676.0 | n/a | n/a | n/a | 1.5s | 97.4% | 51.0 |
| end-users | 65.0 | 104 | 2480 | 200=2453, 500=27 | 11.1 | 12.8 | 3297892.0 | 76.5% | 78.7% | 2.3 | 1.5s | 98.9% | 2451.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 2712.0 | n/a | n/a | n/a | 0.1s | 98.1% | 2.0 |

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
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 11.0 | app1 | True | 8104.0 | 21.1% | 7.1% | -13.9 |
| 0.0 | 11.0 | app2 | True | 1358.0 | 10.5% | 1.2% | -9.3 |
| 0.0 | 11.0 | end-users | True | 104040.0 | 68.4% | 91.7% | 23.2 |
| 11.0 | 21.0 | app1 | True | 56824.0 | 21.1% | 32.8% | 11.8 |
| 11.0 | 21.0 | app2 | True | 4074.0 | 10.5% | 2.4% | -8.2 |
| 11.0 | 21.0 | end-users | True | 112258.0 | 68.4% | 64.8% | -3.6 |
| 21.0 | 31.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 21.0 | 31.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 21.0 | 31.0 | end-users | True | 171962.0 | 68.4% | 99.2% | 30.8 |
| 31.0 | 41.0 | app1 | True | 60888.0 | 21.1% | 37.5% | 16.5 |
| 31.0 | 41.0 | app2 | True | 5420.0 | 10.5% | 3.3% | -7.2 |
| 31.0 | 41.0 | end-users | True | 95956.0 | 68.4% | 59.1% | -9.3 |
| 41.0 | 51.0 | app1 | True | 37936.0 | 21.1% | 22.6% | 1.5 |
| 41.0 | 51.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 41.0 | 51.0 | end-users | True | 129994.0 | 68.4% | 77.4% | 9.0 |
| 51.0 | 61.0 | app1 | True | 5426.0 | 21.1% | 3.2% | -17.8 |
| 51.0 | 61.0 | app2 | True | 2684.0 | 10.5% | 1.6% | -8.9 |
| 51.0 | 61.0 | end-users | True | 160932.0 | 68.4% | 95.2% | 26.8 |
| 61.0 | 71.0 | app1 | True | 63428.0 | 21.1% | 36.9% | 15.9 |
| 61.0 | 71.0 | app2 | True | 5432.0 | 10.5% | 3.2% | -7.4 |
| 61.0 | 71.0 | end-users | True | 102828.0 | 68.4% | 59.9% | -8.5 |
| 71.0 | 81.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.2 |
| 71.0 | 81.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 71.0 | 81.0 | end-users | True | 166472.0 | 68.4% | 99.2% | 30.8 |
| 81.0 | 91.0 | app1 | True | 62306.0 | 21.1% | 35.9% | 14.9 |
| 81.0 | 91.0 | app2 | True | 5418.0 | 10.5% | 3.1% | -7.4 |
| 81.0 | 91.0 | end-users | True | 105640.0 | 68.4% | 60.9% | -7.5 |
| 91.0 | 101.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 91.0 | 101.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 91.0 | 101.0 | end-users | True | 163728.0 | 68.4% | 100.0% | 31.6 |
| 101.0 | 111.0 | app1 | True | 62210.0 | 21.1% | 36.0% | 14.9 |
| 101.0 | 111.0 | app2 | True | 5402.0 | 10.5% | 3.1% | -7.4 |
| 101.0 | 111.0 | end-users | True | 105384.0 | 68.4% | 60.9% | -7.5 |
| 111.0 | 121.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 111.0 | 121.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 111.0 | 121.0 | end-users | True | 174510.0 | 68.4% | 100.0% | 31.6 |
| 121.0 | 131.0 | app1 | True | 62302.0 | 21.1% | 37.7% | 16.7 |
| 121.0 | 131.0 | app2 | True | 5426.0 | 10.5% | 3.3% | -7.2 |
| 121.0 | 131.0 | end-users | True | 97458.0 | 68.4% | 59.0% | -9.4 |
| 131.0 | 141.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 131.0 | 141.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 131.0 | 141.0 | end-users | True | 171786.0 | 68.4% | 100.0% | 31.6 |
| 141.0 | 151.0 | app1 | True | 62154.0 | 21.1% | 36.2% | 15.2 |
| 141.0 | 151.0 | app2 | True | 5414.0 | 10.5% | 3.2% | -7.4 |
| 141.0 | 151.0 | end-users | True | 104016.0 | 68.4% | 60.6% | -7.8 |
| 151.0 | 161.0 | app1 | True | 41900.0 | 21.1% | 24.6% | 3.6 |
| 151.0 | 161.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 151.0 | 161.0 | end-users | True | 125652.0 | 68.4% | 73.8% | 5.4 |
| 161.0 | 171.0 | app1 | True | 1342.0 | 21.1% | 0.8% | -20.3 |
| 161.0 | 171.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 161.0 | 171.0 | end-users | True | 166446.0 | 68.4% | 99.2% | 30.8 |
| 171.0 | 181.0 | app1 | True | 41898.0 | 21.1% | 25.4% | 4.3 |
| 171.0 | 181.0 | app2 | True | 2676.0 | 10.5% | 1.6% | -8.9 |
| 171.0 | 181.0 | end-users | True | 120440.0 | 68.4% | 73.0% | 4.6 |
| 181.0 | 191.0 | app1 | True | 43332.0 | 21.1% | 25.6% | 4.6 |
| 181.0 | 191.0 | app2 | True | 4072.0 | 10.5% | 2.4% | -8.1 |
| 181.0 | 191.0 | end-users | True | 121622.0 | 68.4% | 72.0% | 3.5 |
| 191.0 | 201.0 | app1 | True | 41952.0 | 21.1% | 24.8% | 3.7 |
| 191.0 | 201.0 | app2 | True | 2708.0 | 10.5% | 1.6% | -8.9 |
| 191.0 | 201.0 | end-users | True | 124530.0 | 68.4% | 73.6% | 5.2 |
| 201.0 | 211.0 | app1 | True | 14880.0 | 21.1% | 8.9% | -12.1 |
| 201.0 | 211.0 | app2 | True | 2698.0 | 10.5% | 1.6% | -8.9 |
| 201.0 | 211.0 | end-users | True | 148832.0 | 68.4% | 89.4% | 21.0 |
| 211.0 | 221.0 | app1 | True | 50060.0 | 21.1% | 29.6% | 8.5 |
| 211.0 | 221.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 211.0 | 221.0 | end-users | True | 116336.0 | 68.4% | 68.8% | 0.4 |
| 221.0 | 231.0 | app1 | True | 41928.0 | 21.1% | 25.2% | 4.1 |
| 221.0 | 231.0 | app2 | True | 2708.0 | 10.5% | 1.6% | -8.9 |
| 221.0 | 231.0 | end-users | True | 121736.0 | 68.4% | 73.2% | 4.7 |
| 231.0 | 241.0 | app1 | True | 16290.0 | 21.1% | 9.9% | -11.2 |
| 231.0 | 241.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 231.0 | 241.0 | end-users | True | 146118.0 | 68.4% | 88.5% | 20.1 |
| 241.0 | 251.0 | app1 | False | 29722.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 1322.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 139216.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 16228.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 1358.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 794580 | 39664 | 834244.0 | 0.0% | 822468.0 | 873908.0 | -5.9% | True |
| app2 | 62730 | 3145 | 65875.0 | 0.0% | 67676.0 | 69020.0 | -1.9% | True |
| end-users | 3017190 | 150499 | 3165103.0 | -0.1% | 3297892.0 | 3318188.0 | -0.6% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
