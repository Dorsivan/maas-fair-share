# Fairness benchmark: full-contention (uni-166-g1-not-converging-attempt3)

**Verdict: PASS** (threshold: 10 points)

**Caveat (UNI-163): the EPP restarted mid-run in a way this verdict did not catch.** The windowed series below shows a counter going backwards between two in-run scrapes, but the single before/after snapshot pair this verdict is built from happened to read monotonically end-to-end (a near-zero start and a lower-but-still-higher-than-zero end look the same as no restart at all). Every before/after delta above -- the verdict and the ledger cross-check below -- is computed from the post-restart pod's fresh counters alone and undercounts real traffic; read them as a measurement of the time since the restart, not the whole run.

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `900` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-cqn6s` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T09:33:33Z` |
| Run end | `2026-11-09T09:49:03Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1977 | 000=30, 200=1935, 500=12 | 9.5 | 23.8 | 1411736.0 | 21.1% | 16.8% | -4.2 | 13.8% | -7.2 | 5.4s | 98.9% | 1601.0 |
| app2 | 10.0 | 32 | 6810 | 000=14, 200=6782, 500=14 | 0.9 | 26.3 | 1148434.0 | 10.5% | 13.7% | 3.2 | 47.6% | 37.1 | 3.4s | 98.9% | 5912.0 |
| end-users | 65.0 | 128 | 5506 | 000=128, 200=5332, 500=46 | 15.2 | 19.6 | 5832494.0 | 68.4% | 69.5% | 1.1 | 38.5% | -29.9 | 4.5s | 98.9% | 4344.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events (scheduled):**
- t+120s: epp_delete

**Per-tenant schedule:**
- app1: active 0s-900s, no duty cycle
- app2: active 0s-900s, no duty cycle
- end-users: active 0s-900s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 120.0 | n/a (never converged in this phase) | n/a |
| 900.0 | n/a (never converged in this phase) | n/a |

**Windows** (93 total, EPP restart detected mid-window at least once):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 18874.0 | 21.1% | 24.5% | 3.5 |
| 0.0 | 10.0 | app2 | True | 6756.0 | 10.5% | 8.8% | -1.8 |
| 0.0 | 10.0 | end-users | True | 51376.0 | 68.4% | 66.7% | -1.7 |
| 10.0 | 20.0 | app1 | True | 32336.0 | 21.1% | 19.3% | -1.7 |
| 10.0 | 20.0 | app2 | True | 24300.0 | 10.5% | 14.5% | 4.0 |
| 10.0 | 20.0 | end-users | True | 110808.0 | 68.4% | 66.2% | -2.2 |
| 20.0 | 30.0 | app1 | True | 33796.0 | 21.1% | 19.7% | -1.4 |
| 20.0 | 30.0 | app2 | True | 20272.0 | 10.5% | 11.8% | 1.3 |
| 20.0 | 30.0 | end-users | True | 117644.0 | 68.4% | 68.5% | 0.1 |
| 30.0 | 40.0 | app1 | True | 24352.0 | 21.1% | 14.2% | -6.9 |
| 30.0 | 40.0 | app2 | True | 36484.0 | 10.5% | 21.2% | 10.7 |
| 30.0 | 40.0 | end-users | True | 110970.0 | 68.4% | 64.6% | -3.8 |
| 40.0 | 50.0 | app1 | True | 32314.0 | 21.1% | 21.2% | 0.1 |
| 40.0 | 50.0 | app2 | True | 16208.0 | 10.5% | 10.6% | 0.1 |
| 40.0 | 50.0 | end-users | True | 104176.0 | 68.4% | 68.2% | -0.2 |
| 50.0 | 60.0 | app1 | True | 10832.0 | 21.1% | 6.4% | -14.7 |
| 50.0 | 60.0 | app2 | True | 4058.0 | 10.5% | 2.4% | -8.1 |
| 50.0 | 60.0 | end-users | True | 155548.0 | 68.4% | 91.3% | 22.8 |
| 60.0 | 70.0 | app1 | True | 48658.0 | 21.1% | 28.8% | 7.7 |
| 60.0 | 70.0 | app2 | True | 55358.0 | 10.5% | 32.8% | 22.2 |
| 60.0 | 70.0 | end-users | True | 64922.0 | 68.4% | 38.4% | -30.0 |
| 70.0 | 80.0 | app1 | True | 22934.0 | 21.1% | 13.4% | -7.7 |
| 70.0 | 80.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 70.0 | 80.0 | end-users | True | 148850.0 | 68.4% | 86.6% | 18.2 |
| 80.0 | 90.0 | app1 | True | 22920.0 | 21.1% | 15.0% | -6.1 |
| 80.0 | 90.0 | app2 | True | 10848.0 | 10.5% | 7.1% | -3.4 |
| 80.0 | 90.0 | end-users | True | 119018.0 | 68.4% | 77.9% | 9.5 |
| 90.0 | 100.0 | app1 | True | 43182.0 | 21.1% | 25.8% | 4.7 |
| 90.0 | 100.0 | app2 | True | 48674.0 | 10.5% | 29.1% | 18.5 |
| 90.0 | 100.0 | end-users | True | 75602.0 | 68.4% | 45.1% | -23.3 |
| 100.0 | 110.0 | app1 | True | 13566.0 | 21.1% | 8.0% | -13.1 |
| 100.0 | 110.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 100.0 | 110.0 | end-users | True | 155616.0 | 68.4% | 91.2% | 22.8 |
| 110.0 | 120.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 110.0 | 120.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 110.0 | 120.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 120.0 | 130.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 120.0 | 130.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 120.0 | 130.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 130.0 | 140.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 130.0 | 140.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 130.0 | 140.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 140.0 | 150.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 140.0 | 150.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 140.0 | 150.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 150.0 | 160.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 150.0 | 160.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 150.0 | 160.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 160.0 | 170.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 160.0 | 170.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 160.0 | 170.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 170.0 | 180.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 170.0 | 180.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 170.0 | 180.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 180.0 | 190.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 180.0 | 190.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 180.0 | 190.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 190.0 | 200.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 190.0 | 200.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 190.0 | 200.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 200.0 | 210.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 200.0 | 210.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 200.0 | 210.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 210.0 | 220.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 210.0 | 220.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 210.0 | 220.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 220.0 | 231.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 220.0 | 231.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 220.0 | 231.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 231.0 | 241.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 231.0 | 241.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 231.0 | 241.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 241.0 | 251.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 241.0 | 251.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 241.0 | 251.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 251.0 | 261.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 251.0 | 261.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 251.0 | 261.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 261.0 | 271.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 261.0 | 271.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 261.0 | 271.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 271.0 | 281.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 271.0 | 281.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 271.0 | 281.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 281.0 | 291.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 281.0 | 291.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 281.0 | 291.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 291.0 | 301.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 291.0 | 301.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 291.0 | 301.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 301.0 | 311.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 301.0 | 311.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 301.0 | 311.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 311.0 | 321.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 311.0 | 321.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 311.0 | 321.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 321.0 | 331.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 321.0 | 331.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 321.0 | 331.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 331.0 | 341.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 331.0 | 341.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 331.0 | 341.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 341.0 | 351.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 341.0 | 351.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 341.0 | 351.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 351.0 | 361.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 351.0 | 361.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 351.0 | 361.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 361.0 | 371.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 361.0 | 371.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 361.0 | 371.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 371.0 | 381.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 371.0 | 381.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 371.0 | 381.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 381.0 | 391.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 381.0 | 391.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 381.0 | 391.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 391.0 | 401.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 391.0 | 401.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 391.0 | 401.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 401.0 | 411.0 | app1 | True | 2716.0 | 21.1% | 3.6% | -17.5 |
| 401.0 | 411.0 | app2 | True | 20274.0 | 10.5% | 26.8% | 16.3 |
| 401.0 | 411.0 | end-users | True | 52690.0 | 68.4% | 69.6% | 1.2 |
| 411.0 | 421.0 | app1 | True | 1324.0 | 21.1% | 0.8% | -20.3 |
| 411.0 | 421.0 | app2 | True | 13560.0 | 10.5% | 7.7% | -2.8 |
| 411.0 | 421.0 | end-users | True | 160988.0 | 68.4% | 91.5% | 23.1 |
| 421.0 | 431.0 | app1 | True | 20256.0 | 21.1% | 11.9% | -9.2 |
| 421.0 | 431.0 | app2 | True | 41836.0 | 10.5% | 24.6% | 14.0 |
| 421.0 | 431.0 | end-users | True | 108142.0 | 68.4% | 63.5% | -4.9 |
| 431.0 | 441.0 | app1 | True | 23040.0 | 21.1% | 13.6% | -7.4 |
| 431.0 | 441.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 431.0 | 441.0 | end-users | True | 146014.0 | 68.4% | 86.4% | 18.0 |
| 441.0 | 451.0 | app1 | True | 28340.0 | 21.1% | 18.7% | -2.3 |
| 441.0 | 451.0 | app2 | True | 14836.0 | 10.5% | 9.8% | -0.7 |
| 441.0 | 451.0 | end-users | True | 108214.0 | 68.4% | 71.5% | 3.1 |
| 451.0 | 461.0 | app1 | True | 41904.0 | 21.1% | 24.4% | 3.3 |
| 451.0 | 461.0 | app2 | True | 44674.0 | 10.5% | 26.0% | 15.5 |
| 451.0 | 461.0 | end-users | True | 85182.0 | 68.4% | 49.6% | -18.8 |
| 461.0 | 471.0 | app1 | True | 8118.0 | 21.1% | 4.9% | -16.1 |
| 461.0 | 471.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 461.0 | 471.0 | end-users | True | 156862.0 | 68.4% | 95.1% | 26.7 |
| 471.0 | 481.0 | app1 | True | 43360.0 | 21.1% | 25.8% | 4.8 |
| 471.0 | 481.0 | app2 | True | 48696.0 | 10.5% | 29.0% | 18.5 |
| 471.0 | 481.0 | end-users | True | 75718.0 | 68.4% | 45.1% | -23.3 |
| 481.0 | 491.0 | app1 | True | 33838.0 | 21.1% | 22.3% | 1.3 |
| 481.0 | 491.0 | app2 | True | 10864.0 | 10.5% | 7.2% | -3.4 |
| 481.0 | 491.0 | end-users | True | 106808.0 | 68.4% | 70.5% | 2.1 |
| 491.0 | 501.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 491.0 | 501.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 491.0 | 501.0 | end-users | True | 166232.0 | 68.4% | 100.0% | 31.6 |
| 501.0 | 511.0 | app1 | True | 51454.0 | 21.1% | 30.9% | 9.9 |
| 501.0 | 511.0 | app2 | True | 58274.0 | 10.5% | 35.0% | 24.5 |
| 501.0 | 511.0 | end-users | True | 56756.0 | 68.4% | 34.1% | -34.3 |
| 511.0 | 521.0 | app1 | True | 24350.0 | 21.1% | 15.8% | -5.3 |
| 511.0 | 521.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 511.0 | 521.0 | end-users | True | 129804.0 | 68.4% | 84.2% | 15.8 |
| 521.0 | 531.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 521.0 | 531.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 521.0 | 531.0 | end-users | True | 167658.0 | 68.4% | 100.0% | 31.6 |
| 531.0 | 541.0 | app1 | True | 58216.0 | 21.1% | 34.4% | 13.4 |
| 531.0 | 541.0 | app2 | True | 59548.0 | 10.5% | 35.2% | 24.7 |
| 531.0 | 541.0 | end-users | True | 51282.0 | 68.4% | 30.3% | -38.1 |
| 541.0 | 551.0 | app1 | True | 18896.0 | 21.1% | 11.1% | -10.0 |
| 541.0 | 551.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 541.0 | 551.0 | end-users | True | 151466.0 | 68.4% | 88.9% | 20.5 |
| 551.0 | 561.0 | app1 | True | 21664.0 | 21.1% | 14.2% | -6.9 |
| 551.0 | 561.0 | app2 | True | 10784.0 | 10.5% | 7.1% | -3.5 |
| 551.0 | 561.0 | end-users | True | 120218.0 | 68.4% | 78.7% | 10.3 |
| 561.0 | 571.0 | app1 | True | 45796.0 | 21.1% | 26.5% | 5.4 |
| 561.0 | 571.0 | app2 | True | 50066.0 | 10.5% | 29.0% | 18.4 |
| 561.0 | 571.0 | end-users | True | 76976.0 | 68.4% | 44.5% | -23.9 |
| 571.0 | 581.0 | app1 | True | 13454.0 | 21.1% | 8.1% | -13.0 |
| 571.0 | 581.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 571.0 | 581.0 | end-users | True | 152832.0 | 68.4% | 91.9% | 23.5 |
| 581.0 | 591.0 | app1 | True | 43306.0 | 21.1% | 26.7% | 5.6 |
| 581.0 | 591.0 | app2 | True | 32466.0 | 10.5% | 20.0% | 9.5 |
| 581.0 | 591.0 | end-users | True | 86552.0 | 68.4% | 53.3% | -15.1 |
| 591.0 | 601.0 | app1 | True | 32426.0 | 21.1% | 20.2% | -0.9 |
| 591.0 | 601.0 | app2 | True | 27084.0 | 10.5% | 16.8% | 6.3 |
| 591.0 | 601.0 | end-users | True | 101296.0 | 68.4% | 63.0% | -5.4 |
| 601.0 | 611.0 | app1 | True | 2716.0 | 21.1% | 1.6% | -19.5 |
| 601.0 | 611.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 601.0 | 611.0 | end-users | True | 169098.0 | 68.4% | 98.4% | 30.0 |
| 611.0 | 621.0 | app1 | True | 48680.0 | 21.1% | 29.5% | 8.4 |
| 611.0 | 621.0 | app2 | True | 60952.0 | 10.5% | 36.9% | 26.4 |
| 611.0 | 621.0 | end-users | True | 55530.0 | 68.4% | 33.6% | -34.8 |
| 621.0 | 632.0 | app1 | True | 35184.0 | 21.1% | 23.3% | 2.2 |
| 621.0 | 632.0 | app2 | True | 1358.0 | 10.5% | 0.9% | -9.6 |
| 621.0 | 632.0 | end-users | True | 114766.0 | 68.4% | 75.8% | 7.4 |
| 632.0 | 642.0 | app1 | True | 2708.0 | 21.1% | 1.6% | -19.4 |
| 632.0 | 642.0 | app2 | True | 2672.0 | 10.5% | 1.6% | -8.9 |
| 632.0 | 642.0 | end-users | True | 162350.0 | 68.4% | 96.8% | 28.4 |
| 642.0 | 652.0 | app1 | True | 51370.0 | 21.1% | 30.9% | 9.8 |
| 642.0 | 652.0 | app2 | True | 58158.0 | 10.5% | 35.0% | 24.4 |
| 642.0 | 652.0 | end-users | True | 56858.0 | 68.4% | 34.2% | -34.2 |
| 652.0 | 662.0 | app1 | True | 25708.0 | 21.1% | 15.7% | -5.4 |
| 652.0 | 662.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 652.0 | 662.0 | end-users | True | 138034.0 | 68.4% | 84.3% | 15.9 |
| 662.0 | 672.0 | app1 | True | 4016.0 | 21.1% | 2.5% | -18.5 |
| 662.0 | 672.0 | app2 | True | 2694.0 | 10.5% | 1.7% | -8.8 |
| 662.0 | 672.0 | end-users | True | 151528.0 | 68.4% | 95.8% | 27.3 |
| 672.0 | 682.0 | app1 | True | 56712.0 | 21.1% | 33.3% | 12.3 |
| 672.0 | 682.0 | app2 | True | 58144.0 | 10.5% | 34.2% | 23.7 |
| 672.0 | 682.0 | end-users | True | 55204.0 | 68.4% | 32.5% | -36.0 |
| 682.0 | 692.0 | app1 | True | 18926.0 | 21.1% | 11.6% | -9.5 |
| 682.0 | 692.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 682.0 | 692.0 | end-users | True | 144440.0 | 68.4% | 88.4% | 20.0 |
| 692.0 | 702.0 | app1 | True | 29718.0 | 21.1% | 18.2% | -2.9 |
| 692.0 | 702.0 | app2 | True | 16182.0 | 10.5% | 9.9% | -0.6 |
| 692.0 | 702.0 | end-users | True | 117632.0 | 68.4% | 71.9% | 3.5 |
| 702.0 | 712.0 | app1 | True | 39286.0 | 21.1% | 23.6% | 2.6 |
| 702.0 | 712.0 | app2 | True | 41992.0 | 10.5% | 25.2% | 14.7 |
| 702.0 | 712.0 | end-users | True | 85088.0 | 68.4% | 51.1% | -17.3 |
| 712.0 | 722.0 | app1 | True | 4062.0 | 21.1% | 2.4% | -18.6 |
| 712.0 | 722.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 712.0 | 722.0 | end-users | True | 163706.0 | 68.4% | 97.6% | 29.2 |
| 722.0 | 732.0 | app1 | True | 44680.0 | 21.1% | 26.2% | 5.2 |
| 722.0 | 732.0 | app2 | True | 59510.0 | 10.5% | 34.9% | 24.4 |
| 722.0 | 732.0 | end-users | True | 66220.0 | 68.4% | 38.9% | -29.6 |
| 732.0 | 742.0 | app1 | True | 35230.0 | 21.1% | 22.7% | 1.6 |
| 732.0 | 742.0 | app2 | True | 1342.0 | 10.5% | 0.9% | -9.7 |
| 732.0 | 742.0 | end-users | True | 118830.0 | 68.4% | 76.5% | 8.0 |
| 742.0 | 752.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 742.0 | 752.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 742.0 | 752.0 | end-users | True | 169152.0 | 68.4% | 100.0% | 31.6 |
| 752.0 | 762.0 | app1 | True | 51306.0 | 21.1% | 30.3% | 9.3 |
| 752.0 | 762.0 | app2 | True | 62310.0 | 10.5% | 36.9% | 26.3 |
| 752.0 | 762.0 | end-users | True | 55446.0 | 68.4% | 32.8% | -35.6 |
| 762.0 | 772.0 | app1 | True | 32450.0 | 21.1% | 21.2% | 0.2 |
| 762.0 | 772.0 | app2 | True | 2716.0 | 10.5% | 1.8% | -8.7 |
| 762.0 | 772.0 | end-users | True | 117638.0 | 68.4% | 77.0% | 8.6 |
| 772.0 | 782.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 772.0 | 782.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 772.0 | 782.0 | end-users | True | 167648.0 | 68.4% | 100.0% | 31.6 |
| 782.0 | 792.0 | app1 | True | 58232.0 | 21.1% | 33.9% | 12.8 |
| 782.0 | 792.0 | app2 | True | 63590.0 | 10.5% | 37.0% | 26.5 |
| 782.0 | 792.0 | end-users | True | 49976.0 | 68.4% | 29.1% | -39.3 |
| 792.0 | 802.0 | app1 | True | 28312.0 | 21.1% | 16.8% | -4.3 |
| 792.0 | 802.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 792.0 | 802.0 | end-users | True | 140564.0 | 68.4% | 83.2% | 14.8 |
| 802.0 | 812.0 | app1 | True | 21584.0 | 21.1% | 14.1% | -6.9 |
| 802.0 | 812.0 | app2 | True | 10784.0 | 10.5% | 7.1% | -3.5 |
| 802.0 | 812.0 | end-users | True | 120360.0 | 68.4% | 78.8% | 10.4 |
| 812.0 | 822.0 | app1 | True | 46022.0 | 21.1% | 27.2% | 6.2 |
| 812.0 | 822.0 | app2 | True | 48636.0 | 10.5% | 28.8% | 18.3 |
| 812.0 | 822.0 | end-users | True | 74342.0 | 68.4% | 44.0% | -24.4 |
| 822.0 | 832.0 | app1 | True | 9456.0 | 21.1% | 5.7% | -15.4 |
| 822.0 | 832.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 822.0 | 832.0 | end-users | True | 156948.0 | 68.4% | 94.3% | 25.9 |
| 832.0 | 842.0 | app1 | True | 43268.0 | 21.1% | 26.2% | 5.2 |
| 832.0 | 842.0 | app2 | True | 35170.0 | 10.5% | 21.3% | 10.8 |
| 832.0 | 842.0 | end-users | True | 86558.0 | 68.4% | 52.5% | -16.0 |
| 842.0 | 852.0 | app1 | True | 32476.0 | 21.1% | 20.2% | -0.9 |
| 842.0 | 852.0 | app2 | True | 24256.0 | 10.5% | 15.1% | 4.6 |
| 842.0 | 852.0 | end-users | True | 104048.0 | 68.4% | 64.7% | -3.7 |
| 852.0 | 862.0 | app1 | True | 2692.0 | 21.1% | 1.6% | -19.4 |
| 852.0 | 862.0 | app2 | True | 1338.0 | 10.5% | 0.8% | -9.7 |
| 852.0 | 862.0 | end-users | True | 163454.0 | 68.4% | 97.6% | 29.2 |
| 862.0 | 872.0 | app1 | True | 50068.0 | 21.1% | 29.8% | 8.8 |
| 862.0 | 872.0 | app2 | True | 59546.0 | 10.5% | 35.5% | 25.0 |
| 862.0 | 872.0 | end-users | True | 58202.0 | 68.4% | 34.7% | -33.7 |
| 872.0 | 882.0 | app1 | True | 26998.0 | 21.1% | 17.5% | -3.5 |
| 872.0 | 882.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 872.0 | 882.0 | end-users | True | 127140.0 | 68.4% | 82.5% | 14.1 |
| 882.0 | 892.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 882.0 | 892.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 882.0 | 892.0 | end-users | True | 167668.0 | 68.4% | 100.0% | 31.6 |
| 892.0 | 902.0 | app1 | True | 58182.0 | 21.1% | 34.7% | 13.6 |
| 892.0 | 902.0 | app2 | True | 60852.0 | 10.5% | 36.3% | 25.8 |
| 892.0 | 902.0 | end-users | True | 48692.0 | 68.4% | 29.0% | -39.4 |
| 902.0 | 912.0 | app1 | False | 18954.0 | n/a | n/a | n/a |
| 902.0 | 912.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 902.0 | 912.0 | end-users | False | 146062.0 | n/a | n/a | n/a |
| 912.0 | 922.0 | app1 | False | 20282.0 | n/a | n/a | n/a |
| 912.0 | 922.0 | app2 | False | 43270.0 | n/a | n/a | n/a |
| 912.0 | 922.0 | end-users | False | 17622.0 | n/a | n/a | n/a |
| 922.0 | 930.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 922.0 | 930.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 922.0 | 930.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`, EPP restart detected mid-window at least once):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 24 | 312ms | 1900ms | 2440ms |
| 0.0 | 10.0 | app2 | ok | 22 | 312ms | 2140ms | 4450ms |
| 0.0 | 10.0 | end-users | ok | 87 | 260ms | 2065ms | 2456ms |
| 10.0 | 20.0 | app1 | ok | 27 | 2266ms | 4386ms | 4939ms |
| 10.0 | 20.0 | app2 | ok | 15 | 3750ms | 4750ms | 4975ms |
| 10.0 | 20.0 | end-users | ok | 84 | 3220ms | 4644ms | 4964ms |
| 20.0 | 30.0 | app1 | ok | 28 | 5833ms | 16000ms | 28600ms |
| 20.0 | 30.0 | app2 | ok | 25 | 9792ms | 25833ms | 29583ms |
| 20.0 | 30.0 | end-users | ok | 118 | 7128ms | 22625ms | 29262ms |
| 30.0 | 40.0 | app1 | ok | 32 | 8333ms | 24667ms | 29467ms |
| 30.0 | 40.0 | app2 | ok | 25 | 9583ms | 25833ms | 29583ms |
| 30.0 | 40.0 | end-users | ok | 113 | 7679ms | 23892ms | 29389ms |
| 40.0 | 50.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 50.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 31 | 6136ms | 21143ms | 29114ms |
| 50.0 | 60.0 | app2 | ok | 26 | 17000ms | 27400ms | 29740ms |
| 50.0 | 60.0 | end-users | ok | 114 | 7179ms | 23486ms | 29349ms |
| 60.0 | 70.0 | app1 | ok | 28 | 2000ms | 7000ms | 24400ms |
| 60.0 | 70.0 | app2 | ok | 19 | 3750ms | 23667ms | 29367ms |
| 60.0 | 70.0 | end-users | ok | 121 | 9363ms | 25519ms | 29552ms |
| 70.0 | 80.0 | app1 | ok | 32 | 7308ms | 22889ms | 29289ms |
| 70.0 | 80.0 | app2 | ok | 23 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | end-users | ok | 112 | 6047ms | 19818ms | 28982ms |
| 80.0 | 90.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 27 | 1477ms | 3875ms | 4888ms |
| 90.0 | 100.0 | app2 | ok | 23 | 2917ms | 24889ms | 29489ms |
| 90.0 | 100.0 | end-users | ok | 124 | 9224ms | 25321ms | 29532ms |
| 100.0 | 110.0 | app1 | ok | 32 | 8214ms | 24182ms | 29418ms |
| 100.0 | 110.0 | app2 | ok | 32 | 19333ms | 27867ms | 29787ms |
| 100.0 | 110.0 | end-users | ok | 111 | 5852ms | 18316ms | 28832ms |
| 110.0 | 120.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 120.0 | 130.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 120.0 | 130.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 130.0 | 140.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 130.0 | 140.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 130.0 | 140.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 140.0 | 150.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 140.0 | 150.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 140.0 | 150.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 15 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | app2 | ok | 141 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 24 | 0ms | 0ms | 0ms |
| 160.0 | 170.0 | app2 | ok | 200 | 0ms | 0ms | 0ms |
| 160.0 | 170.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 20 | 0ms | 0ms | 0ms |
| 170.0 | 180.0 | app2 | ok | 203 | 0ms | 0ms | 0ms |
| 170.0 | 180.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 180.0 | 190.0 | app1 | ok | 22 | 0ms | 0ms | 0ms |
| 180.0 | 190.0 | app2 | ok | 200 | 0ms | 0ms | 0ms |
| 180.0 | 190.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 190.0 | 200.0 | app1 | ok | 22 | 0ms | 0ms | 0ms |
| 190.0 | 200.0 | app2 | ok | 198 | 0ms | 0ms | 0ms |
| 190.0 | 200.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 200.0 | 210.0 | app1 | ok | 23 | 0ms | 0ms | 0ms |
| 200.0 | 210.0 | app2 | ok | 201 | 0ms | 0ms | 0ms |
| 200.0 | 210.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 210.0 | 220.0 | app1 | ok | 21 | 0ms | 0ms | 0ms |
| 210.0 | 220.0 | app2 | ok | 200 | 0ms | 0ms | 0ms |
| 210.0 | 220.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 220.0 | 231.0 | app1 | ok | 23 | 0ms | 0ms | 0ms |
| 220.0 | 231.0 | app2 | ok | 198 | 0ms | 0ms | 0ms |
| 220.0 | 231.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 21 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | app2 | ok | 204 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 24 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | app2 | ok | 200 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 23 | 0ms | 0ms | 0ms |
| 251.0 | 261.0 | app2 | ok | 200 | 0ms | 0ms | 0ms |
| 251.0 | 261.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | ok | 23 | 0ms | 0ms | 0ms |
| 261.0 | 271.0 | app2 | ok | 200 | 0ms | 0ms | 0ms |
| 261.0 | 271.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | ok | 20 | 0ms | 0ms | 0ms |
| 271.0 | 281.0 | app2 | ok | 203 | 0ms | 0ms | 0ms |
| 271.0 | 281.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | ok | 23 | 0ms | 0ms | 0ms |
| 281.0 | 291.0 | app2 | ok | 200 | 0ms | 0ms | 0ms |
| 281.0 | 291.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | ok | 23 | 0ms | 0ms | 0ms |
| 291.0 | 301.0 | app2 | ok | 197 | 0ms | 0ms | 0ms |
| 291.0 | 301.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | ok | 22 | 0ms | 0ms | 0ms |
| 301.0 | 311.0 | app2 | ok | 203 | 0ms | 0ms | 0ms |
| 301.0 | 311.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | ok | 21 | 0ms | 0ms | 0ms |
| 311.0 | 321.0 | app2 | ok | 201 | 0ms | 0ms | 0ms |
| 311.0 | 321.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | ok | 21 | 0ms | 0ms | 0ms |
| 321.0 | 331.0 | app2 | ok | 203 | 0ms | 0ms | 0ms |
| 321.0 | 331.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | ok | 21 | 0ms | 0ms | 0ms |
| 331.0 | 341.0 | app2 | ok | 202 | 0ms | 0ms | 0ms |
| 331.0 | 341.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | ok | 21 | 0ms | 0ms | 0ms |
| 341.0 | 351.0 | app2 | ok | 187 | 0ms | 0ms | 0ms |
| 341.0 | 351.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | ok | 23 | 0ms | 0ms | 0ms |
| 351.0 | 361.0 | app2 | ok | 192 | 0ms | 0ms | 0ms |
| 351.0 | 361.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | ok | 22 | 0ms | 0ms | 0ms |
| 361.0 | 371.0 | app2 | ok | 200 | 0ms | 0ms | 0ms |
| 361.0 | 371.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | ok | 22 | 0ms | 0ms | 0ms |
| 371.0 | 381.0 | app2 | ok | 200 | 0ms | 0ms | 0ms |
| 371.0 | 381.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | ok | 22 | 0ms | 0ms | 0ms |
| 381.0 | 391.0 | app2 | ok | 199 | 0ms | 0ms | 0ms |
| 381.0 | 391.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | ok | 23 | 0ms | 0ms | 0ms |
| 391.0 | 401.0 | app2 | ok | 203 | 0ms | 0ms | 0ms |
| 391.0 | 401.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | ok | 15 | 0ms | 750ms | 2275ms |
| 401.0 | 411.0 | app2 | ok | 135 | 0ms | 425ms | 2163ms |
| 401.0 | 411.0 | end-users | ok | 103 | 647ms | 2002ms | 2450ms |
| 411.0 | 421.0 | app1 | ok | 1 | 3750ms | 4750ms | 4975ms |
| 411.0 | 421.0 | app2 | ok | 10 | 3750ms | 4750ms | 4975ms |
| 411.0 | 421.0 | end-users | ok | 105 | 2115ms | 4390ms | 4939ms |
| 421.0 | 431.0 | app1 | ok | 31 | 6630ms | 9326ms | 9933ms |
| 421.0 | 431.0 | app2 | ok | 22 | 6944ms | 9389ms | 9939ms |
| 421.0 | 431.0 | end-users | ok | 121 | 5346ms | 9069ms | 9907ms |
| 431.0 | 441.0 | app1 | ok | 32 | 6429ms | 19333ms | 28933ms |
| 431.0 | 441.0 | app2 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 431.0 | 441.0 | end-users | ok | 112 | 6111ms | 19333ms | 28933ms |
| 441.0 | 451.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app1 | ok | 26 | 1682ms | 4071ms | 4907ms |
| 451.0 | 461.0 | app2 | ok | 21 | 3438ms | 24750ms | 29475ms |
| 451.0 | 461.0 | end-users | ok | 124 | 9375ms | 25491ms | 29549ms |
| 461.0 | 471.0 | app1 | ok | 32 | 8077ms | 24182ms | 29418ms |
| 461.0 | 471.0 | app2 | ok | 21 | 20000ms | 28000ms | 29800ms |
| 461.0 | 471.0 | end-users | ok | 112 | 5682ms | 17556ms | 28756ms |
| 471.0 | 481.0 | app1 | ok | 25 | 1525ms | 3958ms | 4896ms |
| 471.0 | 481.0 | app2 | ok | 24 | 4167ms | 25636ms | 29564ms |
| 471.0 | 481.0 | end-users | ok | 113 | 9781ms | 25815ms | 29581ms |
| 481.0 | 491.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app1 | ok | 32 | 7308ms | 22889ms | 29289ms |
| 491.0 | 501.0 | app2 | ok | 20 | 20000ms | 28000ms | 29800ms |
| 491.0 | 501.0 | end-users | ok | 114 | 5833ms | 19636ms | 28964ms |
| 501.0 | 511.0 | app1 | ok | 24 | 1625ms | 3800ms | 4880ms |
| 501.0 | 511.0 | app2 | ok | 24 | 5000ms | 26000ms | 29600ms |
| 501.0 | 511.0 | end-users | ok | 127 | 8991ms | 25115ms | 29512ms |
| 511.0 | 521.0 | app1 | ok | 32 | 8929ms | 25077ms | 29508ms |
| 511.0 | 521.0 | app2 | ok | 23 | 20000ms | 28000ms | 29800ms |
| 511.0 | 521.0 | end-users | ok | 113 | 5398ms | 15875ms | 28588ms |
| 521.0 | 531.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 521.0 | 531.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 521.0 | 531.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 531.0 | 541.0 | app1 | ok | 25 | 1635ms | 3750ms | 4875ms |
| 531.0 | 541.0 | app2 | ok | 22 | 3333ms | 25111ms | 29511ms |
| 531.0 | 541.0 | end-users | ok | 126 | 9273ms | 25418ms | 29542ms |
| 541.0 | 551.0 | app1 | ok | 32 | 8846ms | 25077ms | 29508ms |
| 541.0 | 551.0 | app2 | ok | 27 | 20000ms | 28000ms | 29800ms |
| 541.0 | 551.0 | end-users | ok | 113 | 5398ms | 15875ms | 28588ms |
| 551.0 | 561.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 551.0 | 561.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 551.0 | 561.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 561.0 | 571.0 | app1 | ok | 28 | 1682ms | 4125ms | 4912ms |
| 561.0 | 571.0 | app2 | ok | 19 | 2179ms | 22400ms | 29240ms |
| 561.0 | 571.0 | end-users | ok | 123 | 9420ms | 25527ms | 29553ms |
| 571.0 | 581.0 | app1 | ok | 32 | 7500ms | 23600ms | 29360ms |
| 571.0 | 581.0 | app2 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 571.0 | 581.0 | end-users | ok | 112 | 5889ms | 18211ms | 28821ms |
| 581.0 | 591.0 | app1 | ok | 26 | 1750ms | 4071ms | 4907ms |
| 581.0 | 591.0 | app2 | ok | 21 | 2917ms | 24750ms | 29475ms |
| 581.0 | 591.0 | end-users | ok | 120 | 9643ms | 25714ms | 29571ms |
| 591.0 | 601.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 591.0 | 601.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 591.0 | 601.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 601.0 | 611.0 | app1 | ok | 32 | 7857ms | 23600ms | 29360ms |
| 601.0 | 611.0 | app2 | ok | 28 | 20000ms | 28000ms | 29800ms |
| 601.0 | 611.0 | end-users | ok | 112 | 5556ms | 16000ms | 28600ms |
| 611.0 | 621.0 | app1 | ok | 32 | 1900ms | 4333ms | 4933ms |
| 611.0 | 621.0 | app2 | ok | 21 | 2375ms | 19500ms | 28950ms |
| 611.0 | 621.0 | end-users | ok | 127 | 9871ms | 25903ms | 29590ms |
| 621.0 | 632.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 621.0 | 632.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 621.0 | 632.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 632.0 | 642.0 | app1 | ok | 32 | 6786ms | 20857ms | 29086ms |
| 632.0 | 642.0 | app2 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 632.0 | 642.0 | end-users | ok | 115 | 6012ms | 20417ms | 29042ms |
| 642.0 | 652.0 | app1 | ok | 25 | 1438ms | 3438ms | 4844ms |
| 642.0 | 652.0 | app2 | ok | 26 | 11429ms | 26286ms | 29629ms |
| 642.0 | 652.0 | end-users | ok | 118 | 9068ms | 25083ms | 29508ms |
| 652.0 | 662.0 | app1 | ok | 32 | 8077ms | 24182ms | 29418ms |
| 652.0 | 662.0 | app2 | ok | 25 | 20000ms | 28000ms | 29800ms |
| 652.0 | 662.0 | end-users | ok | 113 | 5655ms | 18700ms | 28870ms |
| 662.0 | 672.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 662.0 | 672.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 662.0 | 672.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 672.0 | 682.0 | app1 | ok | 27 | 1614ms | 4036ms | 4904ms |
| 672.0 | 682.0 | app2 | ok | 21 | 2393ms | 24000ms | 29400ms |
| 672.0 | 682.0 | end-users | ok | 125 | 9330ms | 25455ms | 29545ms |
| 682.0 | 692.0 | app1 | ok | 32 | 7692ms | 23600ms | 29360ms |
| 682.0 | 692.0 | app2 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 682.0 | 692.0 | end-users | ok | 111 | 5722ms | 16941ms | 28694ms |
| 692.0 | 702.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 692.0 | 702.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 692.0 | 702.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 702.0 | 712.0 | app1 | ok | 22 | 818ms | 2440ms | 4725ms |
| 702.0 | 712.0 | app2 | ok | 14 | 1000ms | 16000ms | 28600ms |
| 702.0 | 712.0 | end-users | ok | 120 | 8516ms | 24146ms | 29415ms |
| 712.0 | 722.0 | app1 | ok | 32 | 8929ms | 25077ms | 29508ms |
| 712.0 | 722.0 | app2 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 712.0 | 722.0 | end-users | ok | 111 | 5179ms | 15200ms | 28520ms |
| 722.0 | 732.0 | app1 | ok | 27 | 1562ms | 3875ms | 4888ms |
| 722.0 | 732.0 | app2 | ok | 22 | 2500ms | 24500ms | 29450ms |
| 722.0 | 732.0 | end-users | ok | 128 | 9375ms | 25509ms | 29551ms |
| 732.0 | 742.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 732.0 | 742.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 732.0 | 742.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 742.0 | 752.0 | app1 | ok | 32 | 8214ms | 24182ms | 29418ms |
| 742.0 | 752.0 | app2 | ok | 31 | 20000ms | 28000ms | 29800ms |
| 742.0 | 752.0 | end-users | ok | 111 | 5756ms | 18316ms | 28832ms |
| 752.0 | 762.0 | app1 | ok | 30 | 2000ms | 4318ms | 4932ms |
| 752.0 | 762.0 | app2 | ok | 18 | 1900ms | 4667ms | 26400ms |
| 752.0 | 762.0 | end-users | ok | 118 | 10656ms | 26131ms | 29613ms |
| 762.0 | 772.0 | app1 | ok | 32 | 6786ms | 20857ms | 29086ms |
| 762.0 | 772.0 | app2 | ok | 32 | 19333ms | 27867ms | 29787ms |
| 762.0 | 772.0 | end-users | ok | 113 | 6307ms | 20583ms | 29058ms |
| 772.0 | 782.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 772.0 | 782.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 772.0 | 782.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 782.0 | 792.0 | app1 | ok | 32 | 1923ms | 4273ms | 4927ms |
| 782.0 | 792.0 | app2 | ok | 16 | 1600ms | 4200ms | 4920ms |
| 782.0 | 792.0 | end-users | ok | 117 | 11429ms | 26286ms | 29629ms |
| 792.0 | 802.0 | app1 | ok | 32 | 5714ms | 14000ms | 28400ms |
| 792.0 | 802.0 | app2 | ok | 22 | 20000ms | 28000ms | 29800ms |
| 792.0 | 802.0 | end-users | ok | 113 | 6359ms | 20174ms | 29017ms |
| 802.0 | 812.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 802.0 | 812.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 802.0 | 812.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 812.0 | 822.0 | app1 | ok | 25 | 1519ms | 3438ms | 4844ms |
| 812.0 | 822.0 | app2 | ok | 23 | 3750ms | 25400ms | 29540ms |
| 812.0 | 822.0 | end-users | ok | 123 | 9125ms | 25176ms | 29518ms |
| 822.0 | 832.0 | app1 | ok | 32 | 8462ms | 24667ms | 29467ms |
| 822.0 | 832.0 | app2 | ok | 23 | 20000ms | 28000ms | 29800ms |
| 822.0 | 832.0 | end-users | ok | 112 | 5488ms | 18211ms | 28821ms |
| 832.0 | 842.0 | app1 | ok | 26 | 1625ms | 3917ms | 4892ms |
| 832.0 | 842.0 | app2 | ok | 23 | 2917ms | 24889ms | 29489ms |
| 832.0 | 842.0 | end-users | ok | 116 | 9821ms | 25857ms | 29586ms |
| 842.0 | 852.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 842.0 | 852.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 842.0 | 852.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 852.0 | 862.0 | app1 | ok | 32 | 7500ms | 22889ms | 29289ms |
| 852.0 | 862.0 | app2 | ok | 23 | 20000ms | 28000ms | 29800ms |
| 852.0 | 862.0 | end-users | ok | 113 | 5966ms | 19238ms | 28924ms |
| 862.0 | 872.0 | app1 | ok | 25 | 1750ms | 4107ms | 4911ms |
| 862.0 | 872.0 | app2 | ok | 22 | 3333ms | 25111ms | 29511ms |
| 862.0 | 872.0 | end-users | ok | 120 | 9545ms | 25636ms | 29564ms |
| 872.0 | 882.0 | app1 | ok | 32 | 8333ms | 24667ms | 29467ms |
| 872.0 | 882.0 | app2 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 872.0 | 882.0 | end-users | ok | 114 | 5761ms | 17333ms | 28733ms |
| 882.0 | 892.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 882.0 | 892.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 882.0 | 892.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 892.0 | 902.0 | app1 | ok | 25 | 1750ms | 4219ms | 4922ms |
| 892.0 | 902.0 | app2 | ok | 22 | 3125ms | 24500ms | 29450ms |
| 892.0 | 902.0 | end-users | ok | 118 | 9561ms | 25630ms | 29563ms |
| 902.0 | 912.0 | app1 | ok | 15 | 16364ms | 27273ms | 29727ms |
| 902.0 | 912.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 902.0 | 912.0 | end-users | ok | 38 | 11000ms | 26200ms | 29620ms |
| 912.0 | 922.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 912.0 | 922.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 912.0 | 922.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 922.0 | 930.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 922.0 | 930.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 922.0 | 930.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens -17.3%, cost -46.0%
- app2 exceeded the 10% ledger tolerance: raw tokens -12.8%, cost -87.5%
- end-users exceeded the 10% ledger tolerance: raw tokens -18.5%, cost -19.1%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2380050 | 118094 | 2067116.0 | -17.3% | 1411736.0 | 2616238.0 | -46.0% | False |
| app2 | 8341860 | 414270 | 7633047.0 | -12.8% | 1148434.0 | 9170400.0 | -87.5% | False |
| end-users | 6558360 | 325414 | 5608083.0 | -18.5% | 5832494.0 | 7209188.0 | -19.1% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1977 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 6810 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 5506 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=11857). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 749468 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
