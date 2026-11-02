# Fairness benchmark: full-contention (uni-143-b4-short-idle-return)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `320` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-02T01:06:45Z` |
| Run end | `2026-11-02T01:12:33Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 665 | 200=665 | 15.6 | 24.9 | 857786.0 | 21.1% | 15.8% | -5.3 | 4.9s | 98.8% | 665.0 |
| app2 | 10.0 | 32 | 606 | 200=598, 500=8 | 16.9 | 28.5 | 767078.0 | 10.5% | 14.1% | 3.6 | 4.8s | 98.1% | 597.0 |
| end-users | 65.0 | 128 | 2882 | 200=2833, 500=49 | 15.1 | 20.0 | 3803610.0 | 68.4% | 70.1% | 1.6 | 5.4s | 98.9% | 2831.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 4074.0 | n/a | n/a | n/a | 0.0s | 98.3% | 3.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-320s, 150s on / 30s off
- app2: active 0s-320s, no duty cycle
- end-users: active 0s-320s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 141.0 | 141.0 |
| 150.0 | n/a (never converged in this phase) | n/a |
| 180.0 | n/a (never converged in this phase) | n/a |
| 320.0 | n/a (never converged in this phase) | n/a |

**Windows** (35 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 6758.0 | 21.1% | 7.9% | -13.1 |
| 0.0 | 10.0 | app2 | True | 8136.0 | 10.5% | 9.5% | -1.0 |
| 0.0 | 10.0 | end-users | True | 70314.0 | 68.4% | 82.5% | 14.1 |
| 10.0 | 20.0 | app1 | True | 60926.0 | 21.1% | 33.9% | 12.8 |
| 10.0 | 20.0 | app2 | True | 27052.0 | 10.5% | 15.0% | 4.5 |
| 10.0 | 20.0 | end-users | True | 91926.0 | 68.4% | 51.1% | -17.3 |
| 20.0 | 30.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 20.0 | 30.0 | app2 | True | 22994.0 | 10.5% | 13.4% | 2.9 |
| 20.0 | 30.0 | end-users | True | 148676.0 | 68.4% | 86.6% | 18.2 |
| 30.0 | 40.0 | app1 | True | 43172.0 | 21.1% | 26.6% | 5.6 |
| 30.0 | 40.0 | app2 | True | 31172.0 | 10.5% | 19.2% | 8.7 |
| 30.0 | 40.0 | end-users | True | 87918.0 | 68.4% | 54.2% | -14.2 |
| 40.0 | 50.0 | app1 | True | 20306.0 | 21.1% | 12.5% | -8.5 |
| 40.0 | 50.0 | app2 | True | 18936.0 | 10.5% | 11.7% | 1.1 |
| 40.0 | 50.0 | end-users | True | 123012.0 | 68.4% | 75.8% | 7.4 |
| 50.0 | 60.0 | app1 | True | 17610.0 | 21.1% | 10.3% | -10.7 |
| 50.0 | 60.0 | app2 | True | 48688.0 | 10.5% | 28.6% | 18.0 |
| 50.0 | 60.0 | end-users | True | 104176.0 | 68.4% | 61.1% | -7.3 |
| 60.0 | 70.0 | app1 | True | 25750.0 | 21.1% | 15.3% | -5.7 |
| 60.0 | 70.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 60.0 | 70.0 | end-users | True | 140662.0 | 68.4% | 83.8% | 15.4 |
| 70.0 | 81.0 | app1 | True | 33770.0 | 21.1% | 22.1% | 1.0 |
| 70.0 | 81.0 | app2 | True | 17610.0 | 10.5% | 11.5% | 1.0 |
| 70.0 | 81.0 | end-users | True | 101428.0 | 68.4% | 66.4% | -2.0 |
| 81.0 | 91.0 | app1 | True | 32468.0 | 21.1% | 19.4% | -1.7 |
| 81.0 | 91.0 | app2 | True | 46004.0 | 10.5% | 27.4% | 16.9 |
| 81.0 | 91.0 | end-users | True | 89246.0 | 68.4% | 53.2% | -15.2 |
| 91.0 | 101.0 | app1 | True | 16262.0 | 21.1% | 9.7% | -11.3 |
| 91.0 | 101.0 | app2 | True | 1350.0 | 10.5% | 0.8% | -9.7 |
| 91.0 | 101.0 | end-users | True | 149948.0 | 68.4% | 89.5% | 21.1 |
| 101.0 | 111.0 | app1 | True | 41962.0 | 21.1% | 27.4% | 6.4 |
| 101.0 | 111.0 | app2 | True | 22980.0 | 10.5% | 15.0% | 4.5 |
| 101.0 | 111.0 | end-users | True | 88008.0 | 68.4% | 57.5% | -10.9 |
| 111.0 | 121.0 | app1 | True | 32544.0 | 21.1% | 19.1% | -2.0 |
| 111.0 | 121.0 | app2 | True | 40544.0 | 10.5% | 23.8% | 13.3 |
| 111.0 | 121.0 | end-users | True | 97378.0 | 68.4% | 57.1% | -11.3 |
| 121.0 | 131.0 | app1 | True | 10838.0 | 21.1% | 6.6% | -14.5 |
| 121.0 | 131.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 121.0 | 131.0 | end-users | True | 154352.0 | 68.4% | 93.4% | 25.0 |
| 131.0 | 141.0 | app1 | True | 43298.0 | 21.1% | 26.5% | 5.4 |
| 131.0 | 141.0 | app2 | True | 47278.0 | 10.5% | 28.9% | 18.4 |
| 131.0 | 141.0 | end-users | True | 73024.0 | 68.4% | 44.6% | -23.8 |
| 141.0 | 151.0 | app1 | True | 33798.0 | 21.1% | 21.2% | 0.1 |
| 141.0 | 151.0 | app2 | True | 17652.0 | 10.5% | 11.1% | 0.5 |
| 141.0 | 151.0 | end-users | True | 108088.0 | 68.4% | 67.8% | -0.7 |
| 151.0 | 161.0 | app1 | False | 9504.0 | n/a | n/a | n/a |
| 151.0 | 161.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 151.0 | 161.0 | end-users | True | 155658.0 | 86.7% | 100.0% | 13.3 |
| 161.0 | 171.0 | app1 | False | 36496.0 | n/a | n/a | n/a |
| 161.0 | 171.0 | app2 | True | 43240.0 | 13.3% | 33.7% | 20.3 |
| 161.0 | 171.0 | end-users | True | 85192.0 | 86.7% | 66.3% | -20.3 |
| 171.0 | 181.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 171.0 | 181.0 | app2 | True | 44616.0 | 13.3% | 25.8% | 12.4 |
| 171.0 | 181.0 | end-users | True | 128504.0 | 86.7% | 74.2% | -12.4 |
| 181.0 | 191.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 181.0 | 191.0 | app2 | True | 1358.0 | 10.5% | 0.9% | -9.6 |
| 181.0 | 191.0 | end-users | True | 147524.0 | 68.4% | 99.1% | 30.7 |
| 191.0 | 201.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 191.0 | 201.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 191.0 | 201.0 | end-users | True | 167690.0 | 68.4% | 100.0% | 31.6 |
| 201.0 | 211.0 | app1 | True | 43298.0 | 21.1% | 25.2% | 4.2 |
| 201.0 | 211.0 | app2 | True | 39144.0 | 10.5% | 22.8% | 12.3 |
| 201.0 | 211.0 | end-users | True | 89306.0 | 68.4% | 52.0% | -16.4 |
| 211.0 | 221.0 | app1 | True | 45992.0 | 21.1% | 27.0% | 5.9 |
| 211.0 | 221.0 | app2 | True | 23000.0 | 10.5% | 13.5% | 3.0 |
| 211.0 | 221.0 | end-users | True | 101376.0 | 68.4% | 59.5% | -8.9 |
| 221.0 | 231.0 | app1 | True | 2700.0 | 21.1% | 1.8% | -19.3 |
| 221.0 | 231.0 | app2 | True | 18974.0 | 10.5% | 12.5% | 2.0 |
| 221.0 | 231.0 | end-users | True | 129944.0 | 68.4% | 85.7% | 17.3 |
| 231.0 | 241.0 | app1 | True | 41940.0 | 21.1% | 25.0% | 4.0 |
| 231.0 | 241.0 | app2 | True | 31146.0 | 10.5% | 18.6% | 8.0 |
| 231.0 | 241.0 | end-users | True | 94620.0 | 68.4% | 56.4% | -12.0 |
| 241.0 | 251.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 241.0 | 251.0 | app2 | True | 17602.0 | 10.5% | 10.7% | 0.1 |
| 241.0 | 251.0 | end-users | True | 147418.0 | 68.4% | 89.3% | 20.9 |
| 251.0 | 261.0 | app1 | True | 28422.0 | 21.1% | 18.6% | -2.5 |
| 251.0 | 261.0 | app2 | True | 14904.0 | 10.5% | 9.7% | -0.8 |
| 251.0 | 261.0 | end-users | True | 109746.0 | 68.4% | 71.7% | 3.3 |
| 261.0 | 271.0 | app1 | True | 39256.0 | 21.1% | 23.4% | 2.4 |
| 261.0 | 271.0 | app2 | True | 50056.0 | 10.5% | 29.8% | 19.3 |
| 261.0 | 271.0 | end-users | True | 78396.0 | 68.4% | 46.7% | -21.7 |
| 271.0 | 281.0 | app1 | True | 17550.0 | 21.1% | 10.6% | -10.4 |
| 271.0 | 281.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 271.0 | 281.0 | end-users | True | 147464.0 | 68.4% | 89.4% | 20.9 |
| 281.0 | 291.0 | app1 | True | 39188.0 | 21.1% | 25.2% | 4.1 |
| 281.0 | 291.0 | app2 | True | 20270.0 | 10.5% | 13.0% | 2.5 |
| 281.0 | 291.0 | end-users | True | 96072.0 | 68.4% | 61.8% | -6.7 |
| 291.0 | 301.0 | app1 | True | 32468.0 | 21.1% | 19.2% | -1.9 |
| 291.0 | 301.0 | app2 | True | 46042.0 | 10.5% | 27.2% | 16.7 |
| 291.0 | 301.0 | end-users | True | 90686.0 | 68.4% | 53.6% | -14.8 |
| 301.0 | 311.0 | app1 | True | 14882.0 | 21.1% | 8.9% | -12.2 |
| 301.0 | 311.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 301.0 | 311.0 | end-users | True | 152962.0 | 68.4% | 91.1% | 22.7 |
| 311.0 | 321.0 | app1 | True | 43308.0 | 21.1% | 28.6% | 7.5 |
| 311.0 | 321.0 | app2 | True | 28438.0 | 10.5% | 18.8% | 8.2 |
| 311.0 | 321.0 | end-users | True | 79868.0 | 68.4% | 52.7% | -15.7 |
| 321.0 | 331.0 | app1 | False | 31118.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | 36534.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | False | 101264.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | 12202.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | False | 71764.0 | n/a | n/a | n/a |
| 341.0 | 348.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 348.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 348.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 817950 | 40915 | 858865.0 | 0.0% | 857786.0 | 899780.0 | -4.7% | True |
| app2 | 735540 | 36758 | 771004.0 | -0.2% | 767078.0 | 809056.0 | -5.2% | True |
| end-users | 3484590 | 173726 | 3655728.0 | -0.1% | 3803610.0 | 3832042.0 | -0.7% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
