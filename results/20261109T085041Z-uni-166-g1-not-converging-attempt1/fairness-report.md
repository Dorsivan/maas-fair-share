# Fairness benchmark: full-contention (uni-166-g1-not-converging-attempt1)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-7hcxt` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T08:51:53Z` |
| Run end | `2026-11-09T09:07:13Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 2080 | 000=3, 200=2065, 500=12 | 12.1 | 22.8 | 2164636.0 | 21.1% | 17.4% | -3.7 | 17.7% | -3.3 | 7.2s | 98.9% | 1607.0 |
| app2 | 10.0 | 32 | 1098 | 000=32, 200=1055, 500=11 | 24.8 | 28.1 | 1100284.0 | 10.5% | 8.8% | -1.7 | 9.4% | -1.2 | 3.2s | 98.9% | 832.0 |
| end-users | 65.0 | 128 | 8552 | 000=18, 200=8478, 500=56 | 11.6 | 19.6 | 9173924.0 | 68.4% | 73.8% | 5.3 | 72.9% | 4.5 | 6.5s | 98.9% | 6814.0 |
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

**Windows** (92 total, EPP restart detected mid-window at least once):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 17582.0 | 21.1% | 19.7% | -1.4 |
| 0.0 | 10.0 | app2 | True | 14860.0 | 10.5% | 16.6% | 6.1 |
| 0.0 | 10.0 | end-users | True | 56820.0 | 68.4% | 63.7% | -4.8 |
| 10.0 | 20.0 | app1 | True | 35166.0 | 21.1% | 22.8% | 1.7 |
| 10.0 | 20.0 | app2 | True | 14932.0 | 10.5% | 9.7% | -0.8 |
| 10.0 | 20.0 | end-users | True | 104132.0 | 68.4% | 67.5% | -0.9 |
| 20.0 | 30.0 | app1 | True | 17558.0 | 21.1% | 10.2% | -10.8 |
| 20.0 | 30.0 | app2 | True | 20292.0 | 10.5% | 11.8% | 1.3 |
| 20.0 | 30.0 | end-users | True | 133788.0 | 68.4% | 77.9% | 9.5 |
| 30.0 | 40.0 | app1 | True | 43364.0 | 21.1% | 25.2% | 4.2 |
| 30.0 | 40.0 | app2 | True | 39204.0 | 10.5% | 22.8% | 12.3 |
| 30.0 | 40.0 | end-users | True | 89264.0 | 68.4% | 51.9% | -16.5 |
| 40.0 | 50.0 | app1 | True | 18924.0 | 21.1% | 11.7% | -9.4 |
| 40.0 | 50.0 | app2 | True | 13520.0 | 10.5% | 8.3% | -2.2 |
| 40.0 | 50.0 | end-users | True | 129720.0 | 68.4% | 80.0% | 11.6 |
| 50.0 | 60.0 | app1 | True | 8104.0 | 21.1% | 5.1% | -15.9 |
| 50.0 | 60.0 | app2 | True | 5414.0 | 10.5% | 3.4% | -7.1 |
| 50.0 | 60.0 | end-users | True | 144480.0 | 68.4% | 91.4% | 23.0 |
| 60.0 | 70.0 | app1 | True | 54088.0 | 21.1% | 32.0% | 10.9 |
| 60.0 | 70.0 | app2 | True | 52780.0 | 10.5% | 31.2% | 20.7 |
| 60.0 | 70.0 | end-users | True | 62238.0 | 68.4% | 36.8% | -31.6 |
| 70.0 | 80.0 | app1 | True | 16252.0 | 21.1% | 9.5% | -11.6 |
| 70.0 | 80.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 70.0 | 80.0 | end-users | True | 155482.0 | 68.4% | 90.5% | 22.1 |
| 80.0 | 90.0 | app1 | True | 39128.0 | 21.1% | 25.2% | 4.1 |
| 80.0 | 90.0 | app2 | True | 20254.0 | 10.5% | 13.0% | 2.5 |
| 80.0 | 90.0 | end-users | True | 95962.0 | 68.4% | 61.8% | -6.6 |
| 90.0 | 100.0 | app1 | True | 33802.0 | 21.1% | 20.2% | -0.9 |
| 90.0 | 100.0 | app2 | True | 39150.0 | 10.5% | 23.4% | 12.8 |
| 90.0 | 100.0 | end-users | True | 94662.0 | 68.4% | 56.5% | -11.9 |
| 100.0 | 110.0 | app1 | True | 4074.0 | 21.1% | 2.4% | -18.7 |
| 100.0 | 110.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 100.0 | 110.0 | end-users | True | 167544.0 | 68.4% | 97.6% | 29.2 |
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
| 160.0 | 170.0 | app1 | True | 22972.0 | 21.1% | 22.7% | 1.6 |
| 160.0 | 170.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 160.0 | 170.0 | end-users | True | 78362.0 | 68.4% | 77.3% | 8.9 |
| 170.0 | 180.0 | app1 | True | 31124.0 | 21.1% | 18.5% | -2.5 |
| 170.0 | 180.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 170.0 | 180.0 | end-users | True | 136700.0 | 68.4% | 81.5% | 13.0 |
| 180.0 | 190.0 | app1 | True | 47350.0 | 21.1% | 28.2% | 7.2 |
| 180.0 | 190.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 180.0 | 190.0 | end-users | True | 120430.0 | 68.4% | 71.8% | 3.4 |
| 190.0 | 201.0 | app1 | True | 13534.0 | 21.1% | 8.1% | -13.0 |
| 190.0 | 201.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 190.0 | 201.0 | end-users | True | 154066.0 | 68.4% | 91.9% | 23.5 |
| 201.0 | 211.0 | app1 | True | 35120.0 | 21.1% | 21.0% | -0.1 |
| 201.0 | 211.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 201.0 | 211.0 | end-users | True | 132424.0 | 68.4% | 79.0% | 10.6 |
| 211.0 | 221.0 | app1 | True | 20290.0 | 21.1% | 12.2% | -8.9 |
| 211.0 | 221.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 211.0 | 221.0 | end-users | True | 146166.0 | 68.4% | 87.8% | 19.4 |
| 221.0 | 231.0 | app1 | True | 32504.0 | 21.1% | 18.9% | -2.1 |
| 221.0 | 231.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 221.0 | 231.0 | end-users | True | 139204.0 | 68.4% | 81.1% | 12.6 |
| 231.0 | 241.0 | app1 | True | 20248.0 | 21.1% | 12.0% | -9.1 |
| 231.0 | 241.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 231.0 | 241.0 | end-users | True | 148740.0 | 68.4% | 88.0% | 19.6 |
| 241.0 | 251.0 | app1 | True | 28432.0 | 21.1% | 17.5% | -3.5 |
| 241.0 | 251.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 241.0 | 251.0 | end-users | True | 133952.0 | 68.4% | 82.5% | 14.1 |
| 251.0 | 261.0 | app1 | True | 47284.0 | 21.1% | 27.5% | 6.5 |
| 251.0 | 261.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 251.0 | 261.0 | end-users | True | 124372.0 | 68.4% | 72.5% | 4.0 |
| 261.0 | 271.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 261.0 | 271.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 261.0 | 271.0 | end-users | True | 166368.0 | 68.4% | 100.0% | 31.6 |
| 271.0 | 281.0 | app1 | True | 39164.0 | 21.1% | 23.4% | 2.3 |
| 271.0 | 281.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 271.0 | 281.0 | end-users | True | 128238.0 | 68.4% | 76.6% | 8.2 |
| 281.0 | 291.0 | app1 | True | 43220.0 | 21.1% | 25.4% | 4.3 |
| 281.0 | 291.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 281.0 | 291.0 | end-users | True | 127046.0 | 68.4% | 74.6% | 6.2 |
| 291.0 | 301.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 291.0 | 301.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 291.0 | 301.0 | end-users | True | 167668.0 | 68.4% | 100.0% | 31.6 |
| 301.0 | 311.0 | app1 | True | 39128.0 | 21.1% | 23.2% | 2.1 |
| 301.0 | 311.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 301.0 | 311.0 | end-users | True | 129722.0 | 68.4% | 76.8% | 8.4 |
| 311.0 | 321.0 | app1 | True | 39192.0 | 21.1% | 23.2% | 2.1 |
| 311.0 | 321.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 311.0 | 321.0 | end-users | True | 129734.0 | 68.4% | 76.8% | 8.4 |
| 321.0 | 331.0 | app1 | True | 1326.0 | 21.1% | 0.8% | -20.3 |
| 321.0 | 331.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 321.0 | 331.0 | end-users | True | 169040.0 | 68.4% | 99.2% | 30.8 |
| 331.0 | 341.0 | app1 | True | 52744.0 | 21.1% | 31.4% | 10.4 |
| 331.0 | 341.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 331.0 | 341.0 | end-users | True | 115030.0 | 68.4% | 68.6% | 0.1 |
| 341.0 | 351.0 | app1 | True | 10838.0 | 21.1% | 6.4% | -14.6 |
| 341.0 | 351.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 341.0 | 351.0 | end-users | True | 158244.0 | 68.4% | 93.6% | 25.2 |
| 351.0 | 361.0 | app1 | True | 43268.0 | 21.1% | 25.8% | 4.7 |
| 351.0 | 361.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 351.0 | 361.0 | end-users | True | 124492.0 | 68.4% | 74.2% | 5.8 |
| 361.0 | 371.0 | app1 | True | 37834.0 | 21.1% | 22.8% | 1.7 |
| 361.0 | 371.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 361.0 | 371.0 | end-users | True | 128398.0 | 68.4% | 77.2% | 8.8 |
| 371.0 | 381.0 | app1 | True | 14868.0 | 21.1% | 8.9% | -12.2 |
| 371.0 | 381.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 371.0 | 381.0 | end-users | True | 152684.0 | 68.4% | 91.1% | 22.7 |
| 381.0 | 391.0 | app1 | True | 24340.0 | 21.1% | 14.3% | -6.8 |
| 381.0 | 391.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 381.0 | 391.0 | end-users | True | 145906.0 | 68.4% | 85.7% | 17.3 |
| 391.0 | 401.0 | app1 | True | 39088.0 | 21.1% | 23.3% | 2.3 |
| 391.0 | 401.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 391.0 | 401.0 | end-users | True | 128454.0 | 68.4% | 76.7% | 8.2 |
| 401.0 | 411.0 | app1 | True | 21626.0 | 21.1% | 12.8% | -8.3 |
| 401.0 | 411.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 401.0 | 411.0 | end-users | True | 147346.0 | 68.4% | 87.2% | 18.8 |
| 411.0 | 421.0 | app1 | True | 18976.0 | 21.1% | 11.4% | -9.6 |
| 411.0 | 421.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 411.0 | 421.0 | end-users | True | 147366.0 | 68.4% | 88.6% | 20.2 |
| 421.0 | 431.0 | app1 | True | 50096.0 | 21.1% | 29.4% | 8.4 |
| 421.0 | 431.0 | app2 | True | 17568.0 | 10.5% | 10.3% | -0.2 |
| 421.0 | 431.0 | end-users | True | 102696.0 | 68.4% | 60.3% | -8.1 |
| 431.0 | 441.0 | app1 | True | 10852.0 | 21.1% | 6.5% | -14.6 |
| 431.0 | 441.0 | app2 | True | 52628.0 | 10.5% | 31.4% | 20.9 |
| 431.0 | 441.0 | end-users | True | 104114.0 | 68.4% | 62.1% | -6.3 |
| 441.0 | 451.0 | app1 | True | 32438.0 | 21.1% | 19.4% | -1.7 |
| 441.0 | 451.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 441.0 | 451.0 | end-users | True | 135160.0 | 68.4% | 80.6% | 12.2 |
| 451.0 | 461.0 | app1 | True | 10838.0 | 21.1% | 6.9% | -14.2 |
| 451.0 | 461.0 | app2 | True | 6762.0 | 10.5% | 4.3% | -6.2 |
| 451.0 | 461.0 | end-users | True | 140490.0 | 68.4% | 88.9% | 20.4 |
| 461.0 | 471.0 | app1 | True | 51322.0 | 21.1% | 30.6% | 9.6 |
| 461.0 | 471.0 | app2 | True | 52834.0 | 10.5% | 31.5% | 21.0 |
| 461.0 | 471.0 | end-users | True | 63404.0 | 68.4% | 37.8% | -30.6 |
| 471.0 | 481.0 | app1 | True | 16262.0 | 21.1% | 9.8% | -11.3 |
| 471.0 | 481.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 471.0 | 481.0 | end-users | True | 150250.0 | 68.4% | 90.2% | 21.8 |
| 481.0 | 491.0 | app1 | True | 39244.0 | 21.1% | 24.8% | 3.8 |
| 481.0 | 491.0 | app2 | True | 20320.0 | 10.5% | 12.9% | 2.3 |
| 481.0 | 491.0 | end-users | True | 98526.0 | 68.4% | 62.3% | -6.1 |
| 491.0 | 501.0 | app1 | True | 33820.0 | 21.1% | 20.0% | -1.0 |
| 491.0 | 501.0 | app2 | True | 40556.0 | 10.5% | 24.0% | 13.5 |
| 491.0 | 501.0 | end-users | True | 94662.0 | 68.4% | 56.0% | -12.4 |
| 501.0 | 511.0 | app1 | True | 4042.0 | 21.1% | 2.4% | -18.7 |
| 501.0 | 511.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 501.0 | 511.0 | end-users | True | 166172.0 | 68.4% | 97.6% | 29.2 |
| 511.0 | 521.0 | app1 | True | 48702.0 | 21.1% | 29.0% | 8.0 |
| 511.0 | 521.0 | app2 | True | 58216.0 | 10.5% | 34.7% | 24.2 |
| 511.0 | 521.0 | end-users | True | 60750.0 | 68.4% | 36.2% | -32.2 |
| 521.0 | 531.0 | app1 | True | 29680.0 | 21.1% | 19.1% | -2.0 |
| 521.0 | 531.0 | app2 | True | 1358.0 | 10.5% | 0.9% | -9.7 |
| 521.0 | 531.0 | end-users | True | 124444.0 | 68.4% | 80.0% | 11.6 |
| 531.0 | 541.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 531.0 | 541.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 531.0 | 541.0 | end-users | True | 169098.0 | 68.4% | 99.2% | 30.8 |
| 541.0 | 551.0 | app1 | True | 56702.0 | 21.1% | 33.6% | 12.5 |
| 541.0 | 551.0 | app2 | True | 59492.0 | 10.5% | 35.2% | 24.7 |
| 541.0 | 551.0 | end-users | True | 52766.0 | 68.4% | 31.2% | -37.2 |
| 551.0 | 561.0 | app1 | True | 24356.0 | 21.1% | 14.4% | -6.6 |
| 551.0 | 561.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 551.0 | 561.0 | end-users | True | 143298.0 | 68.4% | 84.8% | 16.4 |
| 561.0 | 571.0 | app1 | True | 14852.0 | 21.1% | 9.6% | -11.4 |
| 561.0 | 571.0 | app2 | True | 8100.0 | 10.5% | 5.3% | -5.3 |
| 561.0 | 571.0 | end-users | True | 131108.0 | 68.4% | 85.1% | 16.7 |
| 571.0 | 581.0 | app1 | True | 48722.0 | 21.1% | 29.8% | 8.7 |
| 571.0 | 581.0 | app2 | True | 51290.0 | 10.5% | 31.3% | 20.8 |
| 571.0 | 581.0 | end-users | True | 63610.0 | 68.4% | 38.9% | -29.5 |
| 581.0 | 592.0 | app1 | True | 16212.0 | 21.1% | 9.5% | -11.5 |
| 581.0 | 592.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 581.0 | 592.0 | end-users | True | 154160.0 | 68.4% | 90.5% | 22.1 |
| 592.0 | 602.0 | app1 | True | 37874.0 | 21.1% | 24.4% | 3.3 |
| 592.0 | 602.0 | app2 | True | 18970.0 | 10.5% | 12.2% | 1.7 |
| 592.0 | 602.0 | end-users | True | 98640.0 | 68.4% | 63.4% | -5.0 |
| 602.0 | 612.0 | app1 | True | 35198.0 | 21.1% | 21.0% | -0.1 |
| 602.0 | 612.0 | app2 | True | 41948.0 | 10.5% | 25.0% | 14.5 |
| 602.0 | 612.0 | end-users | True | 90654.0 | 68.4% | 54.0% | -14.4 |
| 612.0 | 622.0 | app1 | True | 8096.0 | 21.1% | 4.8% | -16.3 |
| 612.0 | 622.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 612.0 | 622.0 | end-users | True | 160812.0 | 68.4% | 95.2% | 26.8 |
| 622.0 | 632.0 | app1 | True | 44546.0 | 21.1% | 26.4% | 5.3 |
| 622.0 | 632.0 | app2 | True | 63576.0 | 10.5% | 37.6% | 27.1 |
| 622.0 | 632.0 | end-users | True | 60788.0 | 68.4% | 36.0% | -32.4 |
| 632.0 | 642.0 | app1 | True | 36550.0 | 21.1% | 23.7% | 2.6 |
| 632.0 | 642.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 632.0 | 642.0 | end-users | True | 117792.0 | 68.4% | 76.3% | 7.9 |
| 642.0 | 652.0 | app1 | True | 5390.0 | 21.1% | 3.2% | -17.9 |
| 642.0 | 652.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 642.0 | 652.0 | end-users | True | 163582.0 | 68.4% | 96.8% | 28.4 |
| 652.0 | 662.0 | app1 | True | 51366.0 | 21.1% | 29.9% | 8.8 |
| 652.0 | 662.0 | app2 | True | 63576.0 | 10.5% | 37.0% | 26.5 |
| 652.0 | 662.0 | end-users | True | 56860.0 | 68.4% | 33.1% | -35.3 |
| 662.0 | 672.0 | app1 | True | 33894.0 | 21.1% | 22.8% | 1.7 |
| 662.0 | 672.0 | app2 | True | 2716.0 | 10.5% | 1.8% | -8.7 |
| 662.0 | 672.0 | end-users | True | 112294.0 | 68.4% | 75.4% | 7.0 |
| 672.0 | 682.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.2 |
| 672.0 | 682.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 672.0 | 682.0 | end-users | True | 165042.0 | 68.4% | 99.2% | 30.8 |
| 682.0 | 692.0 | app1 | True | 55398.0 | 21.1% | 32.0% | 11.0 |
| 682.0 | 692.0 | app2 | True | 60810.0 | 10.5% | 35.1% | 24.6 |
| 682.0 | 692.0 | end-users | True | 56812.0 | 68.4% | 32.8% | -35.6 |
| 692.0 | 702.0 | app1 | True | 25732.0 | 21.1% | 15.8% | -5.2 |
| 692.0 | 702.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 692.0 | 702.0 | end-users | True | 136616.0 | 68.4% | 84.2% | 15.7 |
| 702.0 | 712.0 | app1 | True | 8116.0 | 21.1% | 5.2% | -15.8 |
| 702.0 | 712.0 | app2 | True | 2704.0 | 10.5% | 1.7% | -8.8 |
| 702.0 | 712.0 | end-users | True | 144748.0 | 68.4% | 93.0% | 24.6 |
| 712.0 | 722.0 | app1 | True | 50168.0 | 21.1% | 30.4% | 9.3 |
| 712.0 | 722.0 | app2 | True | 62152.0 | 10.5% | 37.6% | 27.1 |
| 712.0 | 722.0 | end-users | True | 52870.0 | 68.4% | 32.0% | -36.4 |
| 722.0 | 732.0 | app1 | True | 27104.0 | 21.1% | 16.3% | -4.8 |
| 722.0 | 732.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 722.0 | 732.0 | end-users | True | 139488.0 | 68.4% | 83.7% | 15.3 |
| 732.0 | 742.0 | app1 | True | 18946.0 | 21.1% | 12.5% | -8.5 |
| 732.0 | 742.0 | app2 | True | 10748.0 | 10.5% | 7.1% | -3.4 |
| 732.0 | 742.0 | end-users | True | 121836.0 | 68.4% | 80.4% | 12.0 |
| 742.0 | 752.0 | app1 | True | 45930.0 | 21.1% | 27.9% | 6.8 |
| 742.0 | 752.0 | app2 | True | 49950.0 | 10.5% | 30.3% | 19.8 |
| 742.0 | 752.0 | end-users | True | 68996.0 | 68.4% | 41.8% | -26.6 |
| 752.0 | 762.0 | app1 | True | 16182.0 | 21.1% | 9.2% | -11.8 |
| 752.0 | 762.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.8 |
| 752.0 | 762.0 | end-users | True | 158144.0 | 68.4% | 90.0% | 21.6 |
| 762.0 | 772.0 | app1 | True | 41834.0 | 21.1% | 25.8% | 4.7 |
| 762.0 | 772.0 | app2 | True | 33816.0 | 10.5% | 20.9% | 10.3 |
| 762.0 | 772.0 | end-users | True | 86514.0 | 68.4% | 53.3% | -15.1 |
| 772.0 | 782.0 | app1 | True | 32486.0 | 21.1% | 20.4% | -0.7 |
| 772.0 | 782.0 | app2 | True | 25666.0 | 10.5% | 16.1% | 5.6 |
| 772.0 | 782.0 | end-users | True | 101374.0 | 68.4% | 63.5% | -4.9 |
| 782.0 | 792.0 | app1 | True | 2716.0 | 21.1% | 1.6% | -19.5 |
| 782.0 | 792.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 782.0 | 792.0 | end-users | True | 167442.0 | 68.4% | 98.4% | 30.0 |
| 792.0 | 802.0 | app1 | True | 48654.0 | 21.1% | 28.3% | 7.3 |
| 792.0 | 802.0 | app2 | True | 63546.0 | 10.5% | 37.0% | 26.5 |
| 792.0 | 802.0 | end-users | True | 59528.0 | 68.4% | 34.7% | -33.8 |
| 802.0 | 812.0 | app1 | True | 35138.0 | 21.1% | 23.2% | 2.2 |
| 802.0 | 812.0 | app2 | True | 1358.0 | 10.5% | 0.9% | -9.6 |
| 802.0 | 812.0 | end-users | True | 114844.0 | 68.4% | 75.9% | 7.5 |
| 812.0 | 822.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 812.0 | 822.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 812.0 | 822.0 | end-users | True | 171690.0 | 68.4% | 100.0% | 31.6 |
| 822.0 | 832.0 | app1 | True | 54094.0 | 21.1% | 32.5% | 11.5 |
| 822.0 | 832.0 | app2 | True | 60738.0 | 10.5% | 36.5% | 26.0 |
| 822.0 | 832.0 | end-users | True | 51380.0 | 68.4% | 30.9% | -37.5 |
| 832.0 | 842.0 | app1 | True | 28412.0 | 21.1% | 17.8% | -3.2 |
| 832.0 | 842.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 832.0 | 842.0 | end-users | True | 131108.0 | 68.4% | 82.2% | 13.8 |
| 842.0 | 852.0 | app1 | True | 13532.0 | 21.1% | 8.3% | -12.7 |
| 842.0 | 852.0 | app2 | True | 6756.0 | 10.5% | 4.2% | -6.4 |
| 842.0 | 852.0 | end-users | True | 141846.0 | 68.4% | 87.5% | 19.1 |
| 852.0 | 862.0 | app1 | True | 50006.0 | 21.1% | 29.6% | 8.5 |
| 852.0 | 862.0 | app2 | True | 54116.0 | 10.5% | 32.0% | 21.5 |
| 852.0 | 862.0 | end-users | True | 64852.0 | 68.4% | 38.4% | -30.0 |
| 862.0 | 872.0 | app1 | True | 18920.0 | 21.1% | 11.1% | -9.9 |
| 862.0 | 872.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 862.0 | 872.0 | end-users | True | 150132.0 | 68.4% | 88.1% | 19.7 |
| 872.0 | 882.0 | app1 | True | 36472.0 | 21.1% | 24.1% | 3.0 |
| 872.0 | 882.0 | app2 | True | 17558.0 | 10.5% | 11.6% | 1.1 |
| 872.0 | 882.0 | end-users | True | 97446.0 | 68.4% | 64.3% | -4.1 |
| 882.0 | 892.0 | app1 | True | 33824.0 | 21.1% | 20.3% | -0.7 |
| 882.0 | 892.0 | app2 | True | 43236.0 | 10.5% | 26.0% | 15.5 |
| 882.0 | 892.0 | end-users | True | 89298.0 | 68.4% | 53.7% | -14.7 |
| 892.0 | 902.0 | app1 | True | 10792.0 | 21.1% | 6.3% | -14.8 |
| 892.0 | 902.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 892.0 | 902.0 | end-users | True | 160896.0 | 68.4% | 93.7% | 25.3 |
| 902.0 | 912.0 | app1 | False | 43298.0 | n/a | n/a | n/a |
| 902.0 | 912.0 | app2 | False | 41788.0 | n/a | n/a | n/a |
| 902.0 | 912.0 | end-users | False | 83858.0 | n/a | n/a | n/a |
| 912.0 | 920.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 912.0 | 920.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 912.0 | 920.0 | end-users | False | 60882.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`, EPP restart detected mid-window at least once):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 25 | 156ms | 625ms | 4375ms |
| 0.0 | 10.0 | app2 | ok | 20 | 50ms | 2000ms | 4500ms |
| 0.0 | 10.0 | end-users | ok | 83 | 206ms | 1675ms | 4585ms |
| 10.0 | 20.0 | app1 | ok | 28 | 1375ms | 2425ms | 4650ms |
| 10.0 | 20.0 | app2 | ok | 13 | 2679ms | 4536ms | 4954ms |
| 10.0 | 20.0 | end-users | ok | 85 | 1898ms | 3819ms | 4882ms |
| 20.0 | 30.0 | app1 | ok | 31 | 5694ms | 9139ms | 9914ms |
| 20.0 | 30.0 | app2 | ok | 24 | 15882ms | 27176ms | 29718ms |
| 20.0 | 30.0 | end-users | ok | 114 | 6957ms | 22138ms | 29214ms |
| 30.0 | 40.0 | app1 | ok | 21 | 4688ms | 9389ms | 25800ms |
| 30.0 | 40.0 | app2 | ok | 27 | 10714ms | 26143ms | 29614ms |
| 30.0 | 40.0 | end-users | ok | 115 | 8841ms | 25208ms | 29521ms |
| 40.0 | 50.0 | app1 | ok | 32 | 9615ms | 25733ms | 29573ms |
| 40.0 | 50.0 | app2 | ok | 23 | 18500ms | 27700ms | 29770ms |
| 40.0 | 50.0 | end-users | ok | 113 | 6188ms | 21308ms | 29131ms |
| 50.0 | 60.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 26 | 1625ms | 3917ms | 4892ms |
| 60.0 | 70.0 | app2 | ok | 21 | 3750ms | 25333ms | 29533ms |
| 60.0 | 70.0 | end-users | ok | 121 | 9057ms | 25061ms | 29506ms |
| 70.0 | 80.0 | app1 | ok | 32 | 8077ms | 24182ms | 29418ms |
| 70.0 | 80.0 | app2 | ok | 22 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | end-users | ok | 111 | 5893ms | 19429ms | 28943ms |
| 80.0 | 90.0 | app1 | ok | 25 | 1562ms | 3750ms | 4875ms |
| 80.0 | 90.0 | app2 | ok | 22 | 4167ms | 25600ms | 29560ms |
| 80.0 | 90.0 | end-users | ok | 120 | 9068ms | 25102ms | 29510ms |
| 90.0 | 100.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 32 | 8077ms | 24182ms | 29418ms |
| 100.0 | 110.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | end-users | ok | 112 | 5889ms | 18211ms | 28821ms |
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
| 150.0 | 160.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 150.0 | 160.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 150.0 | 160.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 28 | 3500ms | 8727ms | 9873ms |
| 160.0 | 170.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 160.0 | 170.0 | end-users | ok | 96 | 5636ms | 9127ms | 9913ms |
| 170.0 | 180.0 | app1 | ok | 27 | 4792ms | 8962ms | 9896ms |
| 170.0 | 180.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 170.0 | 180.0 | end-users | ok | 96 | 5472ms | 9094ms | 9909ms |
| 180.0 | 190.0 | app1 | ok | 23 | 3906ms | 8562ms | 9856ms |
| 180.0 | 190.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 180.0 | 190.0 | end-users | ok | 102 | 5678ms | 9136ms | 9914ms |
| 190.0 | 201.0 | app1 | ok | 28 | 7200ms | 9440ms | 9944ms |
| 190.0 | 201.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 190.0 | 201.0 | end-users | ok | 95 | 4241ms | 8782ms | 9878ms |
| 201.0 | 211.0 | app1 | ok | 16 | 3125ms | 6000ms | 9600ms |
| 201.0 | 211.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 107 | 5685ms | 9137ms | 9914ms |
| 211.0 | 221.0 | app1 | ok | 26 | 5000ms | 9000ms | 9900ms |
| 211.0 | 221.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 99 | 5240ms | 9048ms | 9905ms |
| 221.0 | 231.0 | app1 | ok | 15 | 3125ms | 7500ms | 9750ms |
| 221.0 | 231.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 108 | 5500ms | 9100ms | 9910ms |
| 231.0 | 241.0 | app1 | ok | 24 | 5714ms | 9143ms | 9914ms |
| 231.0 | 241.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 101 | 5049ms | 9010ms | 9901ms |
| 241.0 | 251.0 | app1 | ok | 18 | 1750ms | 8200ms | 9820ms |
| 241.0 | 251.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 108 | 5645ms | 9129ms | 9913ms |
| 251.0 | 261.0 | app1 | ok | 18 | 5909ms | 9182ms | 9918ms |
| 251.0 | 261.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 106 | 5093ms | 9019ms | 9902ms |
| 261.0 | 271.0 | app1 | ok | 29 | 7500ms | 9500ms | 9950ms |
| 261.0 | 271.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | ok | 96 | 4052ms | 8703ms | 9870ms |
| 271.0 | 281.0 | app1 | ok | 18 | 625ms | 1600ms | 2410ms |
| 271.0 | 281.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | ok | 108 | 5909ms | 9182ms | 9918ms |
| 281.0 | 291.0 | app1 | ok | 15 | 6591ms | 9318ms | 9932ms |
| 281.0 | 291.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | ok | 110 | 5000ms | 9000ms | 9900ms |
| 291.0 | 301.0 | app1 | ok | 29 | 7315ms | 9463ms | 9946ms |
| 291.0 | 301.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 291.0 | 301.0 | end-users | ok | 96 | 4135ms | 8769ms | 9877ms |
| 301.0 | 311.0 | app1 | ok | 15 | 656ms | 1375ms | 2387ms |
| 301.0 | 311.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 301.0 | 311.0 | end-users | ok | 108 | 5846ms | 9169ms | 9917ms |
| 311.0 | 321.0 | app1 | ok | 14 | 7500ms | 9500ms | 9950ms |
| 311.0 | 321.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | ok | 108 | 4643ms | 8920ms | 9892ms |
| 321.0 | 331.0 | app1 | ok | 29 | 7500ms | 9500ms | 9950ms |
| 321.0 | 331.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | ok | 93 | 4181ms | 8743ms | 9874ms |
| 331.0 | 341.0 | app1 | ok | 12 | 450ms | 975ms | 2320ms |
| 331.0 | 341.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | ok | 110 | 5769ms | 9154ms | 9915ms |
| 341.0 | 351.0 | app1 | ok | 29 | 7500ms | 9500ms | 9950ms |
| 341.0 | 351.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 341.0 | 351.0 | end-users | ok | 93 | 4028ms | 8708ms | 9871ms |
| 351.0 | 361.0 | app1 | ok | 13 | 458ms | 970ms | 2305ms |
| 351.0 | 361.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | ok | 110 | 5769ms | 9154ms | 9915ms |
| 361.0 | 371.0 | app1 | ok | 28 | 7407ms | 9481ms | 9948ms |
| 361.0 | 371.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | ok | 98 | 4196ms | 8775ms | 9878ms |
| 371.0 | 381.0 | app1 | ok | 29 | 7500ms | 9500ms | 9950ms |
| 371.0 | 381.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | ok | 94 | 3952ms | 8618ms | 9862ms |
| 381.0 | 391.0 | app1 | ok | 29 | 2250ms | 8964ms | 9896ms |
| 381.0 | 391.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | ok | 129 | 6206ms | 9241ms | 9924ms |
| 391.0 | 401.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | ok | 160 | 4426ms | 8788ms | 9879ms |
| 401.0 | 411.0 | app1 | ok | 29 | 7500ms | 9500ms | 9950ms |
| 401.0 | 411.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 401.0 | 411.0 | end-users | ok | 32 | 786ms | 2131ms | 2463ms |
| 411.0 | 421.0 | app1 | ok | 22 | 3281ms | 4656ms | 4966ms |
| 411.0 | 421.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 411.0 | 421.0 | end-users | ok | 102 | 6077ms | 9215ms | 9922ms |
| 421.0 | 431.0 | app1 | ok | 16 | 2500ms | 8857ms | 9886ms |
| 421.0 | 431.0 | app2 | ok | 29 | 3550ms | 4710ms | 4971ms |
| 421.0 | 431.0 | end-users | ok | 128 | 5616ms | 9123ms | 9912ms |
| 431.0 | 441.0 | app1 | ok | 32 | 19677ms | 27935ms | 29794ms |
| 431.0 | 441.0 | app2 | ok | 24 | 7143ms | 24000ms | 29400ms |
| 431.0 | 441.0 | end-users | ok | 117 | 6250ms | 18857ms | 28886ms |
| 441.0 | 451.0 | app1 | ok | 31 | 5893ms | 14500ms | 28450ms |
| 441.0 | 451.0 | app2 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 441.0 | 451.0 | end-users | ok | 113 | 6193ms | 20174ms | 29017ms |
| 451.0 | 461.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app1 | ok | 27 | 1614ms | 4292ms | 24600ms |
| 461.0 | 471.0 | app2 | ok | 21 | 2917ms | 24750ms | 29475ms |
| 461.0 | 471.0 | end-users | ok | 119 | 9440ms | 25509ms | 29551ms |
| 471.0 | 481.0 | app1 | ok | 32 | 7500ms | 23600ms | 29360ms |
| 471.0 | 481.0 | app2 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 471.0 | 481.0 | end-users | ok | 113 | 5944ms | 18700ms | 28870ms |
| 481.0 | 491.0 | app1 | ok | 25 | 1688ms | 3958ms | 4896ms |
| 481.0 | 491.0 | app2 | ok | 22 | 2500ms | 24500ms | 29450ms |
| 481.0 | 491.0 | end-users | ok | 115 | 9612ms | 25660ms | 29566ms |
| 491.0 | 501.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 501.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 501.0 | 511.0 | app1 | ok | 32 | 7692ms | 23600ms | 29360ms |
| 501.0 | 511.0 | app2 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 501.0 | 511.0 | end-users | ok | 113 | 5756ms | 18700ms | 28870ms |
| 511.0 | 521.0 | app1 | ok | 26 | 1545ms | 3917ms | 4892ms |
| 511.0 | 521.0 | app2 | ok | 22 | 2500ms | 24500ms | 29450ms |
| 511.0 | 521.0 | end-users | ok | 123 | 9342ms | 25444ms | 29544ms |
| 521.0 | 531.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 521.0 | 531.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 521.0 | 531.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 531.0 | 541.0 | app1 | ok | 32 | 8077ms | 24182ms | 29418ms |
| 531.0 | 541.0 | app2 | ok | 26 | 20000ms | 28000ms | 29800ms |
| 531.0 | 541.0 | end-users | ok | 112 | 5714ms | 18800ms | 28880ms |
| 541.0 | 551.0 | app1 | ok | 28 | 1625ms | 4000ms | 4900ms |
| 541.0 | 551.0 | app2 | ok | 20 | 2286ms | 23333ms | 29333ms |
| 541.0 | 551.0 | end-users | ok | 123 | 9518ms | 25607ms | 29561ms |
| 551.0 | 561.0 | app1 | ok | 32 | 7308ms | 22889ms | 29289ms |
| 551.0 | 561.0 | app2 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 551.0 | 561.0 | end-users | ok | 113 | 5988ms | 19727ms | 28973ms |
| 561.0 | 571.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 561.0 | 571.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 561.0 | 571.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 571.0 | 581.0 | app1 | ok | 27 | 1635ms | 3875ms | 4888ms |
| 571.0 | 581.0 | app2 | ok | 21 | 2917ms | 24750ms | 29475ms |
| 571.0 | 581.0 | end-users | ok | 122 | 9464ms | 25564ms | 29556ms |
| 581.0 | 592.0 | app1 | ok | 32 | 7692ms | 23600ms | 29360ms |
| 581.0 | 592.0 | app2 | ok | 26 | 20000ms | 28000ms | 29800ms |
| 581.0 | 592.0 | end-users | ok | 113 | 5756ms | 18700ms | 28870ms |
| 592.0 | 602.0 | app1 | ok | 16 | 2500ms | 4500ms | 4950ms |
| 592.0 | 602.0 | app2 | ok | 20 | 3000ms | 23333ms | 29333ms |
| 592.0 | 602.0 | end-users | ok | 49 | 20000ms | 28000ms | 29800ms |
| 602.0 | 612.0 | app1 | ok | 12 | 625ms | 1900ms | 2440ms |
| 602.0 | 612.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 602.0 | 612.0 | end-users | ok | 70 | 7500ms | 9914ms | 27667ms |
| 612.0 | 622.0 | app1 | ok | 32 | 7308ms | 22889ms | 29289ms |
| 612.0 | 622.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 612.0 | 622.0 | end-users | ok | 111 | 5915ms | 19909ms | 28991ms |
| 622.0 | 632.0 | app1 | ok | 32 | 1875ms | 4273ms | 4927ms |
| 622.0 | 632.0 | app2 | ok | 16 | 2200ms | 4429ms | 4943ms |
| 622.0 | 632.0 | end-users | ok | 121 | 10484ms | 26097ms | 29610ms |
| 632.0 | 642.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 632.0 | 642.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 632.0 | 642.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 642.0 | 652.0 | app1 | ok | 32 | 6154ms | 19333ms | 28933ms |
| 642.0 | 652.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 642.0 | 652.0 | end-users | ok | 112 | 6477ms | 21040ms | 29104ms |
| 652.0 | 662.0 | app1 | ok | 32 | 2227ms | 4429ms | 4943ms |
| 652.0 | 662.0 | app2 | ok | 18 | 1750ms | 4250ms | 4925ms |
| 652.0 | 662.0 | end-users | ok | 127 | 10156ms | 26031ms | 29603ms |
| 662.0 | 672.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 662.0 | 672.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 662.0 | 672.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 672.0 | 682.0 | app1 | ok | 32 | 6538ms | 20857ms | 29086ms |
| 672.0 | 682.0 | app2 | ok | 27 | 20000ms | 28000ms | 29800ms |
| 672.0 | 682.0 | end-users | ok | 111 | 6488ms | 21462ms | 29146ms |
| 682.0 | 692.0 | app1 | ok | 28 | 1692ms | 4000ms | 4900ms |
| 682.0 | 692.0 | app2 | ok | 19 | 2375ms | 22400ms | 29240ms |
| 682.0 | 692.0 | end-users | ok | 126 | 9464ms | 25579ms | 29558ms |
| 692.0 | 702.0 | app1 | ok | 32 | 7857ms | 23600ms | 29360ms |
| 692.0 | 702.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 692.0 | 702.0 | end-users | ok | 113 | 5756ms | 18700ms | 28870ms |
| 702.0 | 712.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 702.0 | 712.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 702.0 | 712.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 712.0 | 722.0 | app1 | ok | 31 | 2212ms | 4404ms | 4940ms |
| 712.0 | 722.0 | app2 | ok | 17 | 1964ms | 4292ms | 4929ms |
| 712.0 | 722.0 | end-users | ok | 117 | 11429ms | 26286ms | 29629ms |
| 722.0 | 732.0 | app1 | ok | 32 | 6538ms | 20857ms | 29086ms |
| 722.0 | 732.0 | app2 | ok | 25 | 20000ms | 28000ms | 29800ms |
| 722.0 | 732.0 | end-users | ok | 114 | 6548ms | 21857ms | 29186ms |
| 732.0 | 742.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 732.0 | 742.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 732.0 | 742.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 742.0 | 752.0 | app1 | ok | 28 | 1750ms | 4222ms | 4922ms |
| 742.0 | 752.0 | app2 | ok | 22 | 3000ms | 23714ms | 29371ms |
| 742.0 | 752.0 | end-users | ok | 120 | 9474ms | 25556ms | 29556ms |
| 752.0 | 762.0 | app1 | ok | 31 | 7500ms | 23111ms | 29311ms |
| 752.0 | 762.0 | app2 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 752.0 | 762.0 | end-users | ok | 112 | 6047ms | 19818ms | 28982ms |
| 762.0 | 772.0 | app1 | ok | 26 | 1625ms | 4200ms | 24800ms |
| 762.0 | 772.0 | app2 | ok | 21 | 2917ms | 24750ms | 29475ms |
| 762.0 | 772.0 | end-users | ok | 119 | 9420ms | 25509ms | 29551ms |
| 772.0 | 782.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 772.0 | 782.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 772.0 | 782.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 782.0 | 792.0 | app1 | ok | 32 | 8077ms | 24182ms | 29418ms |
| 782.0 | 792.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 782.0 | 792.0 | end-users | ok | 113 | 5944ms | 18700ms | 28870ms |
| 792.0 | 802.0 | app1 | ok | 30 | 2038ms | 4318ms | 4932ms |
| 792.0 | 802.0 | app2 | ok | 17 | 1750ms | 4292ms | 4929ms |
| 792.0 | 802.0 | end-users | ok | 125 | 9956ms | 25968ms | 29597ms |
| 802.0 | 812.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 802.0 | 812.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 802.0 | 812.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 812.0 | 822.0 | app1 | ok | 32 | 6923ms | 22000ms | 29200ms |
| 812.0 | 822.0 | app2 | ok | 25 | 20000ms | 28000ms | 29800ms |
| 812.0 | 822.0 | end-users | ok | 112 | 6000ms | 18800ms | 28880ms |
| 822.0 | 832.0 | app1 | ok | 29 | 1614ms | 4094ms | 4909ms |
| 822.0 | 832.0 | app2 | ok | 21 | 3250ms | 24000ms | 29400ms |
| 822.0 | 832.0 | end-users | ok | 118 | 9750ms | 25786ms | 29579ms |
| 832.0 | 842.0 | app1 | ok | 32 | 6923ms | 22000ms | 29200ms |
| 832.0 | 842.0 | app2 | ok | 27 | 20000ms | 28000ms | 29800ms |
| 832.0 | 842.0 | end-users | ok | 113 | 6131ms | 20583ms | 29058ms |
| 842.0 | 852.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 842.0 | 852.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 842.0 | 852.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 852.0 | 862.0 | app1 | ok | 29 | 1917ms | 4341ms | 4934ms |
| 852.0 | 862.0 | app2 | ok | 20 | 2500ms | 22000ms | 29200ms |
| 852.0 | 862.0 | end-users | ok | 119 | 9619ms | 25673ms | 29567ms |
| 862.0 | 872.0 | app1 | ok | 32 | 6923ms | 22000ms | 29200ms |
| 862.0 | 872.0 | app2 | ok | 27 | 20000ms | 28000ms | 29800ms |
| 862.0 | 872.0 | end-users | ok | 112 | 6364ms | 20667ms | 29067ms |
| 872.0 | 882.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 872.0 | 882.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 872.0 | 882.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 882.0 | 892.0 | app1 | ok | 28 | 1625ms | 4000ms | 4900ms |
| 882.0 | 892.0 | app2 | ok | 19 | 2750ms | 22400ms | 29240ms |
| 882.0 | 892.0 | end-users | ok | 128 | 9298ms | 25429ms | 29543ms |
| 892.0 | 902.0 | app1 | ok | 32 | 8077ms | 24182ms | 29418ms |
| 892.0 | 902.0 | app2 | ok | 25 | 20000ms | 28000ms | 29800ms |
| 892.0 | 902.0 | end-users | ok | 113 | 5872ms | 19238ms | 28924ms |
| 902.0 | 912.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 902.0 | 912.0 | app2 | ok | 7 | 20000ms | 28000ms | 29800ms |
| 902.0 | 912.0 | end-users | ok | 50 | 20000ms | 28000ms | 29800ms |
| 912.0 | 920.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 912.0 | 920.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 912.0 | 920.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens -22.2%, cost -22.5%
- app2 exceeded the 10% ledger tolerance: raw tokens -21.1%, cost -22.8%
- end-users exceeded the 10% ledger tolerance: raw tokens -19.6%, cost -20.0%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2539950 | 125901 | 2074674.0 | -22.2% | 2164636.0 | 2791752.0 | -22.5% | False |
| app2 | 1297650 | 64243 | 1073980.0 | -21.1% | 1100284.0 | 1426136.0 | -22.8% | False |
| end-users | 10427940 | 517337 | 8797175.0 | -19.6% | 9173924.0 | 11462614.0 | -20.0% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2080 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1098 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 8552 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=9253). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 736286 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
