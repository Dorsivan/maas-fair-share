# Fairness benchmark: full-contention (uni138-g2-ledger-full-contention)

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
| Run start | `2026-11-01T19:29:29Z` |
| Run end | `2026-11-01T19:33:52Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 567 | 200=565, 500=2 | 14.8 | 23.9 | 734108.0 | 21.1% | 17.7% | -3.3 | 3.6s | 98.2% | 565.0 |
| app2 | 10.0 | 32 | 449 | 200=448, 500=1 | 24.1 | 27.4 | 581698.0 | 10.5% | 14.0% | 3.5 | 2.7s | 95.2% | 448.0 |
| end-users | 65.0 | 128 | 2155 | 200=2104, 500=51 | 14.8 | 19.5 | 2826610.0 | 68.4% | 68.2% | -0.2 | 3.3s | 98.9% | 2103.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 1358.0 | n/a | n/a | n/a | 0.0s | 65.8% | 1.0 |

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
| 0.0 | 10.0 | app1 | True | 6744.0 | 21.1% | 7.3% | -13.7 |
| 0.0 | 10.0 | app2 | True | 9426.0 | 10.5% | 10.3% | -0.3 |
| 0.0 | 10.0 | end-users | True | 75712.0 | 68.4% | 82.4% | 14.0 |
| 10.0 | 20.0 | app1 | True | 33806.0 | 21.1% | 20.0% | -1.1 |
| 10.0 | 20.0 | app2 | True | 41944.0 | 10.5% | 24.8% | 14.3 |
| 10.0 | 20.0 | end-users | True | 93356.0 | 68.4% | 55.2% | -13.2 |
| 20.0 | 31.0 | app1 | True | 8148.0 | 21.1% | 4.8% | -16.2 |
| 20.0 | 31.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 20.0 | 31.0 | end-users | True | 160904.0 | 68.4% | 95.2% | 26.8 |
| 31.0 | 41.0 | app1 | True | 50128.0 | 21.1% | 29.9% | 8.8 |
| 31.0 | 41.0 | app2 | True | 60980.0 | 10.5% | 36.3% | 25.8 |
| 31.0 | 41.0 | end-users | True | 56782.0 | 68.4% | 33.8% | -34.6 |
| 41.0 | 51.0 | app1 | True | 37836.0 | 21.1% | 22.8% | 1.7 |
| 41.0 | 51.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 41.0 | 51.0 | end-users | True | 128286.0 | 68.4% | 77.2% | 8.8 |
| 51.0 | 61.0 | app1 | True | 32468.0 | 21.1% | 20.5% | -0.5 |
| 51.0 | 61.0 | app2 | True | 16292.0 | 10.5% | 10.3% | -0.2 |
| 51.0 | 61.0 | end-users | True | 109574.0 | 68.4% | 69.2% | 0.8 |
| 61.0 | 71.0 | app1 | True | 17570.0 | 21.1% | 10.4% | -10.7 |
| 61.0 | 71.0 | app2 | True | 47376.0 | 10.5% | 28.0% | 17.5 |
| 61.0 | 71.0 | end-users | True | 104172.0 | 68.4% | 61.6% | -6.8 |
| 71.0 | 81.0 | app1 | True | 25674.0 | 21.1% | 15.2% | -5.9 |
| 71.0 | 81.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 71.0 | 81.0 | end-users | True | 143284.0 | 68.4% | 84.8% | 16.4 |
| 81.0 | 91.0 | app1 | True | 28386.0 | 21.1% | 18.6% | -2.5 |
| 81.0 | 91.0 | app2 | True | 14906.0 | 10.5% | 9.8% | -0.8 |
| 81.0 | 91.0 | end-users | True | 109540.0 | 68.4% | 71.7% | 3.3 |
| 91.0 | 101.0 | app1 | True | 40536.0 | 21.1% | 24.2% | 3.1 |
| 91.0 | 101.0 | app2 | True | 44618.0 | 10.5% | 26.6% | 16.1 |
| 91.0 | 101.0 | end-users | True | 82538.0 | 68.4% | 49.2% | -19.2 |
| 101.0 | 111.0 | app1 | True | 9458.0 | 21.1% | 5.6% | -15.5 |
| 101.0 | 111.0 | app2 | True | 1346.0 | 10.5% | 0.8% | -9.7 |
| 101.0 | 111.0 | end-users | True | 159512.0 | 68.4% | 93.7% | 25.2 |
| 111.0 | 121.0 | app1 | True | 43278.0 | 21.1% | 25.0% | 3.9 |
| 111.0 | 121.0 | app2 | True | 63560.0 | 10.5% | 36.7% | 26.2 |
| 111.0 | 121.0 | end-users | True | 66368.0 | 68.4% | 38.3% | -30.1 |
| 121.0 | 131.0 | app1 | True | 35116.0 | 21.1% | 23.6% | 2.6 |
| 121.0 | 131.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 121.0 | 131.0 | end-users | True | 113620.0 | 68.4% | 76.4% | 8.0 |
| 131.0 | 141.0 | app1 | True | 8148.0 | 21.1% | 4.9% | -16.2 |
| 131.0 | 141.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 131.0 | 141.0 | end-users | True | 158234.0 | 68.4% | 95.1% | 26.7 |
| 141.0 | 151.0 | app1 | True | 50044.0 | 21.1% | 29.8% | 8.8 |
| 141.0 | 151.0 | app2 | True | 59610.0 | 10.5% | 35.5% | 25.0 |
| 141.0 | 151.0 | end-users | True | 58128.0 | 68.4% | 34.6% | -33.8 |
| 151.0 | 161.0 | app1 | True | 31018.0 | 21.1% | 19.8% | -1.3 |
| 151.0 | 161.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 151.0 | 161.0 | end-users | True | 125750.0 | 68.4% | 80.2% | 11.8 |
| 161.0 | 171.0 | app1 | True | 5420.0 | 21.1% | 3.3% | -17.8 |
| 161.0 | 171.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 161.0 | 171.0 | end-users | True | 158232.0 | 68.4% | 95.1% | 26.7 |
| 171.0 | 181.0 | app1 | True | 55500.0 | 21.1% | 32.8% | 11.8 |
| 171.0 | 181.0 | app2 | True | 58090.0 | 10.5% | 34.4% | 23.8 |
| 171.0 | 181.0 | end-users | True | 55442.0 | 68.4% | 32.8% | -35.6 |
| 181.0 | 191.0 | app1 | True | 21594.0 | 21.1% | 13.1% | -8.0 |
| 181.0 | 191.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 181.0 | 191.0 | end-users | True | 143506.0 | 68.4% | 86.9% | 18.5 |
| 191.0 | 201.0 | app1 | True | 25742.0 | 21.1% | 16.6% | -4.5 |
| 191.0 | 201.0 | app2 | True | 12174.0 | 10.5% | 7.8% | -2.7 |
| 191.0 | 201.0 | end-users | True | 117550.0 | 68.4% | 75.6% | 7.2 |
| 201.0 | 211.0 | app1 | True | 41920.0 | 21.1% | 25.0% | 4.0 |
| 201.0 | 211.0 | app2 | True | 47284.0 | 10.5% | 28.2% | 17.7 |
| 201.0 | 211.0 | end-users | True | 78424.0 | 68.4% | 46.8% | -21.6 |
| 211.0 | 221.0 | app1 | True | 10812.0 | 21.1% | 6.4% | -14.6 |
| 211.0 | 221.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 211.0 | 221.0 | end-users | True | 156906.0 | 68.4% | 93.6% | 25.1 |
| 221.0 | 231.0 | app1 | True | 64832.0 | 21.1% | 38.4% | 17.3 |
| 221.0 | 231.0 | app2 | True | 33772.0 | 10.5% | 20.0% | 9.5 |
| 221.0 | 231.0 | end-users | True | 70440.0 | 68.4% | 41.7% | -26.8 |
| 231.0 | 241.0 | app1 | True | 6728.0 | 21.1% | 4.4% | -16.7 |
| 231.0 | 241.0 | app2 | True | 24306.0 | 10.5% | 15.8% | 5.2 |
| 231.0 | 241.0 | end-users | True | 123106.0 | 68.4% | 79.9% | 11.4 |
| 241.0 | 251.0 | app1 | False | 2702.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 4074.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 159642.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 40500.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 39224.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 17602.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 694950 | 34457 | 729407.0 | 0.0% | 734108.0 | 763864.0 | -3.9% | True |
| app2 | 551040 | 27500 | 578540.0 | 0.0% | 581698.0 | 606040.0 | -4.0% | True |
| end-users | 2587920 | 128796 | 2715422.0 | -0.0% | 2826610.0 | 2845512.0 | -0.7% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
