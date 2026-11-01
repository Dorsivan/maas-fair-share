# Fairness benchmark: full-contention (uni139-full-contention-r4)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-01T19:56:16Z` |
| Run end | `2026-11-01T20:00:39Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 549 | 200=549 | 12.4 | 24.5 | 700842.0 | 21.1% | 17.0% | -4.1 | 3.5s | 98.4% | 549.0 |
| app2 | 10.0 | 32 | 441 | 200=441 | 24.4 | 27.4 | 565416.0 | 10.5% | 13.7% | 3.2 | 2.7s | 96.1% | 441.0 |
| end-users | 65.0 | 128 | 2145 | 200=2145 | 16.4 | 19.6 | 2867654.0 | 68.4% | 69.4% | 0.9 | 3.1s | 98.9% | 2145.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | n/a | n/a | 0.0s | 88.7% | 0.0 |

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
| 0.0 | 231.0 | 231.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 1358.0 | 21.1% | 1.4% | -19.7 |
| 0.0 | 10.0 | app2 | True | 13538.0 | 10.5% | 13.5% | 3.0 |
| 0.0 | 10.0 | end-users | True | 85134.0 | 68.4% | 85.1% | 16.7 |
| 10.0 | 20.0 | app1 | True | 39304.0 | 21.1% | 24.2% | 3.2 |
| 10.0 | 20.0 | app2 | True | 20290.0 | 10.5% | 12.5% | 2.0 |
| 10.0 | 20.0 | end-users | True | 102794.0 | 68.4% | 63.3% | -5.1 |
| 20.0 | 30.0 | app1 | True | 22952.0 | 21.1% | 14.4% | -6.7 |
| 20.0 | 30.0 | app2 | True | 33862.0 | 10.5% | 21.2% | 10.7 |
| 20.0 | 30.0 | end-users | True | 102794.0 | 68.4% | 64.4% | -4.0 |
| 30.0 | 40.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 30.0 | 40.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 30.0 | 40.0 | end-users | True | 167862.0 | 68.4% | 100.0% | 31.6 |
| 40.0 | 50.0 | app1 | True | 47264.0 | 21.1% | 28.9% | 7.8 |
| 40.0 | 50.0 | app2 | True | 60910.0 | 10.5% | 37.2% | 26.7 |
| 40.0 | 50.0 | end-users | True | 55578.0 | 68.4% | 33.9% | -34.5 |
| 50.0 | 60.0 | app1 | True | 32442.0 | 21.1% | 21.0% | -0.0 |
| 50.0 | 60.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 50.0 | 60.0 | end-users | True | 121858.0 | 68.4% | 79.0% | 10.6 |
| 60.0 | 70.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 60.0 | 70.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 60.0 | 70.0 | end-users | True | 166444.0 | 68.4% | 100.0% | 31.6 |
| 70.0 | 81.0 | app1 | True | 56782.0 | 21.1% | 33.9% | 12.8 |
| 70.0 | 81.0 | app2 | True | 58094.0 | 10.5% | 34.7% | 24.1 |
| 70.0 | 81.0 | end-users | True | 52764.0 | 68.4% | 31.5% | -36.9 |
| 81.0 | 91.0 | app1 | True | 20338.0 | 21.1% | 12.0% | -9.0 |
| 81.0 | 91.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 81.0 | 91.0 | end-users | True | 148860.0 | 68.4% | 88.0% | 19.6 |
| 91.0 | 101.0 | app1 | True | 20284.0 | 21.1% | 13.3% | -7.8 |
| 91.0 | 101.0 | app2 | True | 12166.0 | 10.5% | 8.0% | -2.6 |
| 91.0 | 101.0 | end-users | True | 120298.0 | 68.4% | 78.8% | 10.3 |
| 101.0 | 111.0 | app1 | True | 47326.0 | 21.1% | 27.8% | 6.7 |
| 101.0 | 111.0 | app2 | True | 47336.0 | 10.5% | 27.8% | 17.3 |
| 101.0 | 111.0 | end-users | True | 75670.0 | 68.4% | 44.4% | -24.0 |
| 111.0 | 121.0 | app1 | True | 10798.0 | 21.1% | 6.3% | -14.7 |
| 111.0 | 121.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 111.0 | 121.0 | end-users | True | 159528.0 | 68.4% | 93.7% | 25.2 |
| 121.0 | 131.0 | app1 | True | 43246.0 | 21.1% | 26.5% | 5.4 |
| 121.0 | 131.0 | app2 | True | 41900.0 | 10.5% | 25.6% | 15.1 |
| 121.0 | 131.0 | end-users | True | 78342.0 | 68.4% | 47.9% | -20.5 |
| 131.0 | 141.0 | app1 | True | 31132.0 | 21.1% | 20.4% | -0.7 |
| 131.0 | 141.0 | app2 | True | 17604.0 | 10.5% | 11.5% | 1.0 |
| 131.0 | 141.0 | end-users | True | 104192.0 | 68.4% | 68.1% | -0.3 |
| 141.0 | 151.0 | app1 | True | 2708.0 | 21.1% | 1.6% | -19.5 |
| 141.0 | 151.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 141.0 | 151.0 | end-users | True | 167788.0 | 68.4% | 98.4% | 30.0 |
| 151.0 | 161.0 | app1 | True | 48738.0 | 21.1% | 29.3% | 8.2 |
| 151.0 | 161.0 | app2 | True | 64986.0 | 10.5% | 39.0% | 28.5 |
| 151.0 | 161.0 | end-users | True | 52740.0 | 68.4% | 31.7% | -36.7 |
| 161.0 | 171.0 | app1 | True | 36576.0 | 21.1% | 23.3% | 2.3 |
| 161.0 | 171.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 161.0 | 171.0 | end-users | True | 120344.0 | 68.4% | 76.7% | 8.3 |
| 171.0 | 181.0 | app1 | True | 14870.0 | 21.1% | 8.9% | -12.2 |
| 171.0 | 181.0 | app2 | True | 6706.0 | 10.5% | 4.0% | -6.5 |
| 171.0 | 181.0 | end-users | True | 145910.0 | 68.4% | 87.1% | 18.7 |
| 181.0 | 191.0 | app1 | True | 39246.0 | 21.1% | 23.8% | 2.7 |
| 181.0 | 191.0 | app2 | True | 55362.0 | 10.5% | 33.6% | 23.0 |
| 181.0 | 191.0 | end-users | True | 70330.0 | 68.4% | 42.6% | -25.8 |
| 191.0 | 201.0 | app1 | True | 24368.0 | 21.1% | 14.8% | -6.3 |
| 191.0 | 201.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 191.0 | 201.0 | end-users | True | 140748.0 | 68.4% | 85.2% | 16.8 |
| 201.0 | 211.0 | app1 | True | 9464.0 | 21.1% | 6.0% | -15.0 |
| 201.0 | 211.0 | app2 | True | 5428.0 | 10.5% | 3.5% | -7.1 |
| 201.0 | 211.0 | end-users | True | 141990.0 | 68.4% | 90.5% | 22.1 |
| 211.0 | 221.0 | app1 | True | 51520.0 | 21.1% | 30.9% | 9.9 |
| 211.0 | 221.0 | app2 | True | 54176.0 | 10.5% | 32.5% | 22.0 |
| 211.0 | 221.0 | end-users | True | 60866.0 | 68.4% | 36.5% | -31.9 |
| 221.0 | 231.0 | app1 | True | 17596.0 | 21.1% | 10.6% | -10.5 |
| 221.0 | 231.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 221.0 | 231.0 | end-users | True | 148820.0 | 68.4% | 89.4% | 21.0 |
| 231.0 | 241.0 | app1 | True | 33768.0 | 21.1% | 21.7% | 0.7 |
| 231.0 | 241.0 | app2 | True | 17558.0 | 10.5% | 11.3% | 0.8 |
| 231.0 | 241.0 | end-users | True | 104126.0 | 68.4% | 67.0% | -1.4 |
| 241.0 | 251.0 | app1 | False | 37958.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 40634.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 89280.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 10804.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 14866.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 82594.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 675270 | 33750 | 709020.0 | 0.0% | 700842.0 | 742770.0 | -5.6% | True |
| app2 | 542430 | 27039 | 569469.0 | 0.0% | 565416.0 | 596508.0 | -5.2% | True |
| end-users | 2638350 | 131533 | 2769883.0 | 0.0% | 2867654.0 | 2901416.0 | -1.2% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
