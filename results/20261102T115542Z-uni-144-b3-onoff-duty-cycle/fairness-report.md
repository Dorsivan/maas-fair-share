# Fairness benchmark: full-contention (uni-144-b3-onoff-duty-cycle)

**Verdict: FAIL** (threshold: 10 points)

- app1 deviated -10.5 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `360` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-575669c495-xp5s8` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-02T11:56:55Z` |
| Run end | `2026-11-02T12:03:23Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 517 | 200=507, 500=10 | 14.4 | 22.5 | 646748.0 | 21.1% | 10.5% | -10.5 | 4.7s | 98.9% | 507.0 |
| app2 | 10.0 | 32 | 714 | 200=713, 500=1 | 18.7 | 27.0 | 938760.0 | 10.5% | 15.3% | 4.8 | 4.7s | 98.9% | 713.0 |
| end-users | 65.0 | 128 | 3395 | 200=3383, 500=12 | 13.6 | 18.9 | 4551466.0 | 68.4% | 74.2% | 5.7 | 5.1s | 98.9% | 3383.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-360s, 30s on / 30s off
- app2: active 0s-360s, no duty cycle
- end-users: active 0s-360s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 10.0 | 10.0 |
| 30.0 | 50.0 | 20.0 |
| 60.0 | n/a (never converged in this phase) | n/a |
| 90.0 | n/a (never converged in this phase) | n/a |
| 120.0 | n/a (never converged in this phase) | n/a |
| 150.0 | n/a (never converged in this phase) | n/a |
| 180.0 | n/a (never converged in this phase) | n/a |
| 210.0 | 230.0 | 20.0 |
| 240.0 | n/a (never converged in this phase) | n/a |
| 270.0 | n/a (never converged in this phase) | n/a |
| 300.0 | 320.0 | 20.0 |
| 330.0 | n/a (never converged in this phase) | n/a |
| 360.0 | n/a (never converged in this phase) | n/a |

**Windows** (39 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 1358.0 | 21.1% | 3.9% | -17.2 |
| 0.0 | 10.0 | app2 | True | 10834.0 | 10.5% | 30.8% | 20.3 |
| 0.0 | 10.0 | end-users | True | 23002.0 | 68.4% | 65.4% | -3.1 |
| 10.0 | 20.0 | app1 | True | 35124.0 | 21.1% | 15.5% | -5.5 |
| 10.0 | 20.0 | app2 | True | 35242.0 | 10.5% | 15.6% | 5.1 |
| 10.0 | 20.0 | end-users | True | 155690.0 | 68.4% | 68.9% | 0.5 |
| 20.0 | 30.0 | app1 | True | 32466.0 | 21.1% | 19.0% | -2.0 |
| 20.0 | 30.0 | app2 | True | 28452.0 | 10.5% | 16.7% | 6.2 |
| 20.0 | 30.0 | end-users | True | 109598.0 | 68.4% | 64.3% | -4.1 |
| 30.0 | 40.0 | app1 | False | 14864.0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app2 | True | 23060.0 | 13.3% | 14.8% | 1.5 |
| 30.0 | 40.0 | end-users | True | 132566.0 | 86.7% | 85.2% | -1.5 |
| 40.0 | 50.0 | app1 | False | 39318.0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app2 | True | 40514.0 | 13.3% | 30.6% | 17.3 |
| 40.0 | 50.0 | end-users | True | 91888.0 | 86.7% | 69.4% | -17.3 |
| 50.0 | 60.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app2 | True | 17606.0 | 13.3% | 11.2% | -2.1 |
| 50.0 | 60.0 | end-users | True | 139200.0 | 86.7% | 88.8% | 2.1 |
| 60.0 | 70.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 60.0 | 70.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 60.0 | 70.0 | end-users | True | 165066.0 | 68.4% | 100.0% | 31.6 |
| 70.0 | 80.0 | app1 | True | 21666.0 | 21.1% | 12.7% | -8.3 |
| 70.0 | 80.0 | app2 | True | 62198.0 | 10.5% | 36.5% | 26.0 |
| 70.0 | 80.0 | end-users | True | 86624.0 | 68.4% | 50.8% | -17.6 |
| 80.0 | 90.0 | app1 | True | 21626.0 | 21.1% | 12.6% | -8.5 |
| 80.0 | 90.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 80.0 | 90.0 | end-users | True | 150094.0 | 68.4% | 87.4% | 19.0 |
| 90.0 | 100.0 | app1 | False | 35240.0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app2 | True | 17564.0 | 13.3% | 15.3% | 2.0 |
| 90.0 | 100.0 | end-users | True | 97272.0 | 86.7% | 84.7% | -2.0 |
| 100.0 | 110.0 | app1 | False | 8136.0 | n/a | n/a | n/a |
| 100.0 | 110.0 | app2 | True | 47266.0 | 13.3% | 28.9% | 15.6 |
| 100.0 | 110.0 | end-users | True | 116302.0 | 86.7% | 71.1% | -15.6 |
| 110.0 | 120.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 110.0 | 120.0 | end-users | True | 172978.0 | 86.7% | 100.0% | 13.3 |
| 120.0 | 130.0 | app1 | True | 16180.0 | 21.1% | 9.7% | -11.3 |
| 120.0 | 130.0 | app2 | True | 62298.0 | 10.5% | 37.4% | 26.9 |
| 120.0 | 130.0 | end-users | True | 88020.0 | 68.4% | 52.9% | -15.6 |
| 130.0 | 140.0 | app1 | True | 27052.0 | 21.1% | 15.9% | -5.2 |
| 130.0 | 140.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 130.0 | 140.0 | end-users | True | 140562.0 | 68.4% | 82.5% | 14.1 |
| 140.0 | 150.0 | app1 | True | 18970.0 | 21.1% | 12.6% | -8.4 |
| 140.0 | 150.0 | app2 | True | 10826.0 | 10.5% | 7.2% | -3.3 |
| 140.0 | 150.0 | end-users | True | 120274.0 | 68.4% | 80.1% | 11.7 |
| 150.0 | 160.0 | app1 | False | 47404.0 | n/a | n/a | n/a |
| 150.0 | 160.0 | app2 | True | 48624.0 | 13.3% | 39.1% | 25.8 |
| 150.0 | 160.0 | end-users | True | 75736.0 | 86.7% | 60.9% | -25.8 |
| 160.0 | 170.0 | app1 | False | 10864.0 | n/a | n/a | n/a |
| 160.0 | 170.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 160.0 | 170.0 | end-users | True | 155580.0 | 86.7% | 100.0% | 13.3 |
| 170.0 | 180.0 | app1 | False | 8136.0 | n/a | n/a | n/a |
| 170.0 | 180.0 | app2 | True | 43174.0 | 13.3% | 27.1% | 13.7 |
| 170.0 | 180.0 | end-users | True | 116388.0 | 86.7% | 72.9% | -13.7 |
| 180.0 | 190.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 180.0 | 190.0 | app2 | True | 24350.0 | 10.5% | 15.2% | 4.7 |
| 180.0 | 190.0 | end-users | True | 135434.0 | 68.4% | 84.8% | 16.3 |
| 190.0 | 200.0 | app1 | True | 33680.0 | 21.1% | 20.8% | -0.3 |
| 190.0 | 200.0 | app2 | True | 18958.0 | 10.5% | 11.7% | 1.2 |
| 190.0 | 200.0 | end-users | True | 109566.0 | 68.4% | 67.5% | -0.9 |
| 200.0 | 210.0 | app1 | True | 9498.0 | 21.1% | 5.6% | -15.4 |
| 200.0 | 210.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 200.0 | 210.0 | end-users | True | 158014.0 | 68.4% | 93.6% | 25.2 |
| 210.0 | 220.0 | app1 | False | 43312.0 | n/a | n/a | n/a |
| 210.0 | 220.0 | app2 | True | 59540.0 | 13.3% | 46.3% | 33.0 |
| 210.0 | 220.0 | end-users | True | 68994.0 | 86.7% | 53.7% | -33.0 |
| 220.0 | 230.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 220.0 | 230.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 220.0 | 230.0 | end-users | True | 159668.0 | 86.7% | 100.0% | 13.3 |
| 230.0 | 240.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 230.0 | 240.0 | app2 | True | 16276.0 | 13.3% | 10.2% | -3.1 |
| 230.0 | 240.0 | end-users | True | 143256.0 | 86.7% | 89.8% | 3.1 |
| 240.0 | 250.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 240.0 | 250.0 | app2 | True | 47304.0 | 10.5% | 27.8% | 17.2 |
| 240.0 | 250.0 | end-users | True | 123050.0 | 68.4% | 72.2% | 3.8 |
| 250.0 | 260.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 250.0 | 260.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 250.0 | 260.0 | end-users | True | 169064.0 | 68.4% | 100.0% | 31.6 |
| 260.0 | 270.0 | app1 | True | 51356.0 | 21.1% | 30.6% | 9.6 |
| 260.0 | 270.0 | app2 | True | 60868.0 | 10.5% | 36.3% | 25.8 |
| 260.0 | 270.0 | end-users | True | 55488.0 | 68.4% | 33.1% | -35.3 |
| 270.0 | 280.0 | app1 | False | 32454.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app2 | True | 1358.0 | 13.3% | 1.1% | -12.2 |
| 270.0 | 280.0 | end-users | True | 117642.0 | 86.7% | 98.9% | 12.2 |
| 280.0 | 290.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 280.0 | 290.0 | end-users | True | 169154.0 | 86.7% | 100.0% | 13.3 |
| 290.0 | 300.0 | app1 | False | 17626.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app2 | True | 63592.0 | 13.3% | 41.9% | 28.6 |
| 290.0 | 300.0 | end-users | True | 88010.0 | 86.7% | 58.1% | -28.6 |
| 300.0 | 310.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 300.0 | 310.0 | app2 | True | 2682.0 | 10.5% | 1.6% | -8.9 |
| 300.0 | 310.0 | end-users | True | 162254.0 | 68.4% | 98.4% | 30.0 |
| 310.0 | 320.0 | app1 | True | 43238.0 | 21.1% | 25.6% | 4.5 |
| 310.0 | 320.0 | app2 | True | 50094.0 | 10.5% | 29.6% | 19.1 |
| 310.0 | 320.0 | end-users | True | 75756.0 | 68.4% | 44.8% | -23.6 |
| 320.0 | 330.0 | app1 | True | 32508.0 | 21.1% | 21.7% | 0.6 |
| 320.0 | 330.0 | app2 | True | 10800.0 | 10.5% | 7.2% | -3.3 |
| 320.0 | 330.0 | end-users | True | 106828.0 | 68.4% | 71.2% | 2.7 |
| 330.0 | 340.0 | app1 | False | 1342.0 | n/a | n/a | n/a |
| 330.0 | 340.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 330.0 | 340.0 | end-users | True | 163780.0 | 86.7% | 100.0% | 13.3 |
| 340.0 | 350.0 | app1 | False | 41972.0 | n/a | n/a | n/a |
| 340.0 | 350.0 | app2 | True | 43310.0 | 13.3% | 33.0% | 19.7 |
| 340.0 | 350.0 | end-users | True | 87918.0 | 86.7% | 67.0% | -19.7 |
| 350.0 | 361.0 | app1 | False | 1358.0 | n/a | n/a | n/a |
| 350.0 | 361.0 | app2 | True | 43280.0 | 13.3% | 26.4% | 13.1 |
| 350.0 | 361.0 | end-users | True | 120352.0 | 86.7% | 73.6% | -13.1 |
| 361.0 | 371.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | 1358.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | False | 150350.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | 43258.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | False | 50048.0 | n/a | n/a | n/a |
| 381.0 | 388.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 388.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 388.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 623610 | 31193 | 654803.0 | 0.0% | 646748.0 | 685996.0 | -5.7% | True |
| app2 | 876990 | 43758 | 920748.0 | 0.0% | 938760.0 | 964506.0 | -2.7% | True |
| end-users | 4161090 | 207378 | 4368468.0 | 0.0% | 4551466.0 | 4575846.0 | -0.5% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
