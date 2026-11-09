# Fairness benchmark: full-contention (uni-166-g1-not-converging-attempt2)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-hbnd6` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T09:12:01Z` |
| Run end | `2026-11-09T09:27:32Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1962 | 000=5, 200=1946, 500=11 | 12.9 | 24.1 | 2056066.0 | 21.1% | 16.5% | -4.5 | 16.8% | -4.3 | 8.8s | 98.9% | 1532.0 |
| app2 | 10.0 | 32 | 1111 | 000=31, 200=1068, 500=12 | 24.5 | 28.0 | 1115208.0 | 10.5% | 9.0% | -1.6 | 9.5% | -1.0 | 6.8s | 98.9% | 840.0 |
| end-users | 65.0 | 128 | 8630 | 000=10, 200=8554, 500=53, 503=13 | 12.0 | 19.4 | 9266328.0 | 68.4% | 74.5% | 6.1 | 73.7% | 5.3 | 8.3s | 98.9% | 6881.0 |
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
| 0.0 | 10.0 | app1 | True | 14918.0 | 21.1% | 20.4% | -0.6 |
| 0.0 | 10.0 | app2 | True | 9454.0 | 10.5% | 12.9% | 2.4 |
| 0.0 | 10.0 | end-users | True | 48658.0 | 68.4% | 66.6% | -1.8 |
| 10.0 | 20.0 | app1 | True | 36560.0 | 21.1% | 22.0% | 0.9 |
| 10.0 | 20.0 | app2 | True | 28364.0 | 10.5% | 17.1% | 6.5 |
| 10.0 | 20.0 | end-users | True | 101412.0 | 68.4% | 61.0% | -7.5 |
| 20.0 | 30.0 | app1 | True | 24378.0 | 21.1% | 15.3% | -5.8 |
| 20.0 | 30.0 | app2 | True | 17580.0 | 10.5% | 11.0% | 0.5 |
| 20.0 | 30.0 | end-users | True | 117640.0 | 68.4% | 73.7% | 5.3 |
| 30.0 | 40.0 | app1 | True | 21650.0 | 21.1% | 13.0% | -8.0 |
| 30.0 | 40.0 | app2 | True | 36550.0 | 10.5% | 22.0% | 11.4 |
| 30.0 | 40.0 | end-users | True | 108212.0 | 68.4% | 65.0% | -3.4 |
| 40.0 | 51.0 | app1 | True | 21644.0 | 21.1% | 13.1% | -7.9 |
| 40.0 | 51.0 | app2 | True | 9478.0 | 10.5% | 5.8% | -4.8 |
| 40.0 | 51.0 | end-users | True | 133708.0 | 68.4% | 81.1% | 12.7 |
| 51.0 | 61.0 | app1 | True | 35144.0 | 21.1% | 22.6% | 1.6 |
| 51.0 | 61.0 | app2 | True | 18936.0 | 10.5% | 12.2% | 1.7 |
| 51.0 | 61.0 | end-users | True | 101400.0 | 68.4% | 65.2% | -3.2 |
| 61.0 | 71.0 | app1 | True | 33794.0 | 21.1% | 20.6% | -0.4 |
| 61.0 | 71.0 | app2 | True | 39230.0 | 10.5% | 24.0% | 13.4 |
| 61.0 | 71.0 | end-users | True | 90770.0 | 68.4% | 55.4% | -13.0 |
| 71.0 | 81.0 | app1 | True | 6782.0 | 21.1% | 3.9% | -17.1 |
| 71.0 | 81.0 | app2 | True | 1344.0 | 10.5% | 0.8% | -9.7 |
| 71.0 | 81.0 | end-users | True | 163664.0 | 68.4% | 95.3% | 26.8 |
| 81.0 | 91.0 | app1 | True | 47286.0 | 21.1% | 27.5% | 6.5 |
| 81.0 | 91.0 | app2 | True | 60784.0 | 10.5% | 35.4% | 24.9 |
| 81.0 | 91.0 | end-users | True | 63568.0 | 68.4% | 37.0% | -31.4 |
| 91.0 | 101.0 | app1 | True | 31184.0 | 21.1% | 20.8% | -0.3 |
| 91.0 | 101.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 91.0 | 101.0 | end-users | True | 118962.0 | 68.4% | 79.2% | 10.8 |
| 101.0 | 111.0 | app1 | True | 2712.0 | 21.1% | 1.6% | -19.5 |
| 101.0 | 111.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 101.0 | 111.0 | end-users | True | 170240.0 | 68.4% | 98.4% | 30.0 |
| 111.0 | 121.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 111.0 | 121.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 111.0 | 121.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 121.0 | 131.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 121.0 | 131.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 121.0 | 131.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 131.0 | 141.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 131.0 | 141.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 131.0 | 141.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 141.0 | 151.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 141.0 | 151.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 141.0 | 151.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 151.0 | 161.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 151.0 | 161.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 151.0 | 161.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 161.0 | 171.0 | app1 | True | 24374.0 | 21.1% | 22.8% | 1.8 |
| 161.0 | 171.0 | app2 | True | 1334.0 | 10.5% | 1.2% | -9.3 |
| 161.0 | 171.0 | end-users | True | 81098.0 | 68.4% | 75.9% | 7.5 |
| 171.0 | 181.0 | app1 | True | 21618.0 | 21.1% | 12.8% | -8.3 |
| 171.0 | 181.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 171.0 | 181.0 | end-users | True | 145924.0 | 68.4% | 86.4% | 18.0 |
| 181.0 | 191.0 | app1 | True | 29766.0 | 21.1% | 17.9% | -3.2 |
| 181.0 | 191.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 181.0 | 191.0 | end-users | True | 135144.0 | 68.4% | 81.3% | 12.9 |
| 191.0 | 201.0 | app1 | True | 25658.0 | 21.1% | 15.1% | -6.0 |
| 191.0 | 201.0 | app2 | True | 1350.0 | 10.5% | 0.8% | -9.7 |
| 191.0 | 201.0 | end-users | True | 143164.0 | 68.4% | 84.1% | 15.7 |
| 201.0 | 211.0 | app1 | True | 52772.0 | 21.1% | 31.7% | 10.7 |
| 201.0 | 211.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 201.0 | 211.0 | end-users | True | 112230.0 | 68.4% | 67.5% | -1.0 |
| 211.0 | 221.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 211.0 | 221.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 211.0 | 221.0 | end-users | True | 166296.0 | 68.4% | 100.0% | 31.6 |
| 221.0 | 231.0 | app1 | True | 36506.0 | 21.1% | 21.4% | 0.4 |
| 221.0 | 231.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 221.0 | 231.0 | end-users | True | 132484.0 | 68.4% | 77.8% | 9.4 |
| 231.0 | 241.0 | app1 | True | 16222.0 | 21.1% | 9.8% | -11.3 |
| 231.0 | 241.0 | app2 | True | 1348.0 | 10.5% | 0.8% | -9.7 |
| 231.0 | 241.0 | end-users | True | 148716.0 | 68.4% | 89.4% | 21.0 |
| 241.0 | 251.0 | app1 | True | 47312.0 | 21.1% | 28.2% | 7.2 |
| 241.0 | 251.0 | app2 | True | 2708.0 | 10.5% | 1.6% | -8.9 |
| 241.0 | 251.0 | end-users | True | 117536.0 | 68.4% | 70.1% | 1.7 |
| 251.0 | 261.0 | app1 | True | 36434.0 | 21.1% | 20.9% | -0.2 |
| 251.0 | 261.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 251.0 | 261.0 | end-users | True | 136560.0 | 68.4% | 78.3% | 9.9 |
| 261.0 | 271.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 261.0 | 271.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 261.0 | 271.0 | end-users | True | 163588.0 | 68.4% | 100.0% | 31.6 |
| 271.0 | 281.0 | app1 | True | 36578.0 | 21.1% | 21.8% | 0.8 |
| 271.0 | 281.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 271.0 | 281.0 | end-users | True | 129794.0 | 68.4% | 77.4% | 9.0 |
| 281.0 | 291.0 | app1 | True | 31174.0 | 21.1% | 18.6% | -2.5 |
| 281.0 | 291.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 281.0 | 291.0 | end-users | True | 135236.0 | 68.4% | 80.6% | 12.2 |
| 291.0 | 301.0 | app1 | True | 4074.0 | 21.1% | 2.5% | -18.6 |
| 291.0 | 301.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 291.0 | 301.0 | end-users | True | 160822.0 | 68.4% | 97.5% | 29.1 |
| 301.0 | 311.0 | app1 | True | 24368.0 | 21.1% | 15.5% | -5.5 |
| 301.0 | 311.0 | app2 | True | 1358.0 | 10.5% | 0.9% | -9.7 |
| 301.0 | 311.0 | end-users | True | 131098.0 | 68.4% | 83.6% | 15.2 |
| 311.0 | 321.0 | app1 | True | 25702.0 | 21.1% | 15.3% | -5.7 |
| 311.0 | 321.0 | app2 | True | 1356.0 | 10.5% | 0.8% | -9.7 |
| 311.0 | 321.0 | end-users | True | 140516.0 | 68.4% | 83.9% | 15.4 |
| 321.0 | 331.0 | app1 | True | 35104.0 | 21.1% | 20.5% | -0.6 |
| 321.0 | 331.0 | app2 | True | 1324.0 | 10.5% | 0.8% | -9.8 |
| 321.0 | 331.0 | end-users | True | 135082.0 | 68.4% | 78.8% | 10.3 |
| 331.0 | 341.0 | app1 | True | 8074.0 | 21.1% | 4.8% | -16.2 |
| 331.0 | 341.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 331.0 | 341.0 | end-users | True | 158186.0 | 68.4% | 94.4% | 26.0 |
| 341.0 | 351.0 | app1 | True | 28412.0 | 21.1% | 16.8% | -4.2 |
| 341.0 | 351.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 341.0 | 351.0 | end-users | True | 140620.0 | 68.4% | 83.2% | 14.8 |
| 351.0 | 361.0 | app1 | True | 36474.0 | 21.1% | 21.8% | 0.7 |
| 351.0 | 361.0 | app2 | True | 1348.0 | 10.5% | 0.8% | -9.7 |
| 351.0 | 361.0 | end-users | True | 129610.0 | 68.4% | 77.4% | 9.0 |
| 361.0 | 371.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 361.0 | 371.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 361.0 | 371.0 | end-users | True | 164962.0 | 68.4% | 100.0% | 31.6 |
| 371.0 | 381.0 | app1 | True | 36594.0 | 21.1% | 21.7% | 0.6 |
| 371.0 | 381.0 | app2 | True | 1348.0 | 10.5% | 0.8% | -9.7 |
| 371.0 | 381.0 | end-users | True | 131042.0 | 68.4% | 77.5% | 9.1 |
| 381.0 | 391.0 | app1 | True | 35204.0 | 21.1% | 20.8% | -0.2 |
| 381.0 | 391.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 381.0 | 391.0 | end-users | True | 132528.0 | 68.4% | 78.4% | 10.0 |
| 391.0 | 401.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 391.0 | 401.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 391.0 | 401.0 | end-users | True | 170522.0 | 68.4% | 100.0% | 31.6 |
| 401.0 | 411.0 | app1 | True | 48664.0 | 21.1% | 28.6% | 7.5 |
| 401.0 | 411.0 | app2 | True | 2696.0 | 10.5% | 1.6% | -8.9 |
| 401.0 | 411.0 | end-users | True | 118978.0 | 68.4% | 69.8% | 1.4 |
| 411.0 | 421.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 411.0 | 421.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 411.0 | 421.0 | end-users | True | 173204.0 | 68.4% | 100.0% | 31.6 |
| 421.0 | 431.0 | app1 | True | 55354.0 | 21.1% | 33.8% | 12.8 |
| 421.0 | 431.0 | app2 | True | 12188.0 | 10.5% | 7.4% | -3.1 |
| 421.0 | 431.0 | end-users | True | 96160.0 | 68.4% | 58.7% | -9.7 |
| 431.0 | 441.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.2 |
| 431.0 | 441.0 | app2 | True | 45998.0 | 10.5% | 27.4% | 16.9 |
| 431.0 | 441.0 | end-users | True | 120276.0 | 68.4% | 71.8% | 3.3 |
| 441.0 | 452.0 | app1 | True | 33796.0 | 21.1% | 22.1% | 1.1 |
| 441.0 | 452.0 | app2 | True | 9490.0 | 10.5% | 6.2% | -4.3 |
| 441.0 | 452.0 | end-users | True | 109582.0 | 68.4% | 71.7% | 3.3 |
| 452.0 | 462.0 | app1 | True | 9460.0 | 21.1% | 5.6% | -15.4 |
| 452.0 | 462.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 452.0 | 462.0 | end-users | True | 158138.0 | 68.4% | 94.4% | 25.9 |
| 462.0 | 472.0 | app1 | True | 49978.0 | 21.1% | 29.1% | 8.1 |
| 462.0 | 472.0 | app2 | True | 58166.0 | 10.5% | 33.9% | 23.4 |
| 462.0 | 472.0 | end-users | True | 63538.0 | 68.4% | 37.0% | -31.4 |
| 472.0 | 482.0 | app1 | True | 28446.0 | 21.1% | 17.7% | -3.4 |
| 472.0 | 482.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 472.0 | 482.0 | end-users | True | 132458.0 | 68.4% | 82.3% | 13.9 |
| 482.0 | 492.0 | app1 | True | 8118.0 | 21.1% | 5.0% | -16.0 |
| 482.0 | 492.0 | app2 | True | 4014.0 | 10.5% | 2.5% | -8.1 |
| 482.0 | 492.0 | end-users | True | 150126.0 | 68.4% | 92.5% | 24.1 |
| 492.0 | 502.0 | app1 | True | 54072.0 | 21.1% | 31.7% | 10.7 |
| 492.0 | 502.0 | app2 | True | 56894.0 | 10.5% | 33.4% | 22.9 |
| 492.0 | 502.0 | end-users | True | 59406.0 | 68.4% | 34.9% | -33.6 |
| 502.0 | 512.0 | app1 | True | 17576.0 | 21.1% | 10.7% | -10.3 |
| 502.0 | 512.0 | app2 | True | 1356.0 | 10.5% | 0.8% | -9.7 |
| 502.0 | 512.0 | end-users | True | 144712.0 | 68.4% | 88.4% | 20.0 |
| 512.0 | 522.0 | app1 | True | 25694.0 | 21.1% | 16.5% | -4.5 |
| 512.0 | 522.0 | app2 | True | 14842.0 | 10.5% | 9.6% | -1.0 |
| 512.0 | 522.0 | end-users | True | 114786.0 | 68.4% | 73.9% | 5.5 |
| 522.0 | 532.0 | app1 | True | 43230.0 | 21.1% | 25.8% | 4.7 |
| 522.0 | 532.0 | app2 | True | 47326.0 | 10.5% | 28.2% | 17.7 |
| 522.0 | 532.0 | end-users | True | 77200.0 | 68.4% | 46.0% | -22.4 |
| 532.0 | 542.0 | app1 | True | 13564.0 | 21.1% | 8.0% | -13.0 |
| 532.0 | 542.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 532.0 | 542.0 | end-users | True | 155482.0 | 68.4% | 92.0% | 23.6 |
| 542.0 | 552.0 | app1 | True | 40544.0 | 21.1% | 27.0% | 6.0 |
| 542.0 | 552.0 | app2 | True | 21546.0 | 10.5% | 14.4% | 3.8 |
| 542.0 | 552.0 | end-users | True | 87942.0 | 68.4% | 58.6% | -9.8 |
| 552.0 | 562.0 | app1 | True | 32400.0 | 21.1% | 18.9% | -2.2 |
| 552.0 | 562.0 | app2 | True | 41936.0 | 10.5% | 24.4% | 13.9 |
| 552.0 | 562.0 | end-users | True | 97244.0 | 68.4% | 56.7% | -11.7 |
| 562.0 | 572.0 | app1 | True | 10800.0 | 21.1% | 6.6% | -14.5 |
| 562.0 | 572.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 562.0 | 572.0 | end-users | True | 154076.0 | 68.4% | 93.4% | 25.0 |
| 572.0 | 582.0 | app1 | True | 43264.0 | 21.1% | 25.2% | 4.1 |
| 572.0 | 582.0 | app2 | True | 62154.0 | 10.5% | 36.2% | 25.7 |
| 572.0 | 582.0 | end-users | True | 66334.0 | 68.4% | 38.6% | -29.8 |
| 582.0 | 592.0 | app1 | True | 35030.0 | 21.1% | 23.1% | 2.1 |
| 582.0 | 592.0 | app2 | True | 2684.0 | 10.5% | 1.8% | -8.8 |
| 582.0 | 592.0 | end-users | True | 113658.0 | 68.4% | 75.1% | 6.7 |
| 592.0 | 602.0 | app1 | True | 8110.0 | 21.1% | 4.8% | -16.2 |
| 592.0 | 602.0 | app2 | True | 1342.0 | 10.5% | 0.8% | -9.7 |
| 592.0 | 602.0 | end-users | True | 158128.0 | 68.4% | 94.4% | 25.9 |
| 602.0 | 612.0 | app1 | True | 48658.0 | 21.1% | 28.8% | 7.7 |
| 602.0 | 612.0 | app2 | True | 59494.0 | 10.5% | 35.2% | 24.7 |
| 602.0 | 612.0 | end-users | True | 60824.0 | 68.4% | 36.0% | -32.4 |
| 612.0 | 622.0 | app1 | True | 32550.0 | 21.1% | 21.3% | 0.2 |
| 612.0 | 622.0 | app2 | True | 1358.0 | 10.5% | 0.9% | -9.6 |
| 612.0 | 622.0 | end-users | True | 118996.0 | 68.4% | 77.8% | 9.4 |
| 622.0 | 632.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 622.0 | 632.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 622.0 | 632.0 | end-users | True | 170250.0 | 68.4% | 100.0% | 31.6 |
| 632.0 | 642.0 | app1 | True | 56708.0 | 21.1% | 33.0% | 12.0 |
| 632.0 | 642.0 | app2 | True | 58114.0 | 10.5% | 33.9% | 23.3 |
| 632.0 | 642.0 | end-users | True | 56844.0 | 68.4% | 33.1% | -35.3 |
| 642.0 | 652.0 | app1 | True | 20230.0 | 21.1% | 12.1% | -9.0 |
| 642.0 | 652.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 642.0 | 652.0 | end-users | True | 145928.0 | 68.4% | 87.1% | 18.7 |
| 652.0 | 662.0 | app1 | True | 17512.0 | 21.1% | 11.3% | -9.8 |
| 652.0 | 662.0 | app2 | True | 9466.0 | 10.5% | 6.1% | -4.4 |
| 652.0 | 662.0 | end-users | True | 128560.0 | 68.4% | 82.7% | 14.2 |
| 662.0 | 672.0 | app1 | True | 47366.0 | 21.1% | 28.5% | 7.4 |
| 662.0 | 672.0 | app2 | True | 49942.0 | 10.5% | 30.0% | 19.5 |
| 662.0 | 672.0 | end-users | True | 68996.0 | 68.4% | 41.5% | -26.9 |
| 672.0 | 682.0 | app1 | True | 12142.0 | 21.1% | 7.1% | -14.0 |
| 672.0 | 682.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 672.0 | 682.0 | end-users | True | 159530.0 | 68.4% | 92.9% | 24.5 |
| 682.0 | 692.0 | app1 | True | 43296.0 | 21.1% | 26.9% | 5.8 |
| 682.0 | 692.0 | app2 | True | 33852.0 | 10.5% | 21.0% | 10.5 |
| 682.0 | 692.0 | end-users | True | 83842.0 | 68.4% | 52.1% | -16.3 |
| 692.0 | 702.0 | app1 | True | 32386.0 | 21.1% | 20.0% | -1.1 |
| 692.0 | 702.0 | app2 | True | 24360.0 | 10.5% | 15.0% | 4.5 |
| 692.0 | 702.0 | end-users | True | 105286.0 | 68.4% | 65.0% | -3.4 |
| 702.0 | 712.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 702.0 | 712.0 | app2 | True | 1350.0 | 10.5% | 0.8% | -9.7 |
| 702.0 | 712.0 | end-users | True | 167776.0 | 68.4% | 99.2% | 30.8 |
| 712.0 | 722.0 | app1 | True | 70264.0 | 21.1% | 41.6% | 20.6 |
| 712.0 | 722.0 | app2 | True | 55420.0 | 10.5% | 32.8% | 22.3 |
| 712.0 | 722.0 | end-users | True | 43172.0 | 68.4% | 25.6% | -42.9 |
| 722.0 | 732.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 722.0 | 732.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 722.0 | 732.0 | end-users | True | 171796.0 | 68.4% | 100.0% | 31.6 |
| 732.0 | 742.0 | app1 | True | 12204.0 | 21.1% | 8.1% | -12.9 |
| 732.0 | 742.0 | app2 | True | 6790.0 | 10.5% | 4.5% | -6.0 |
| 732.0 | 742.0 | end-users | True | 131204.0 | 68.4% | 87.4% | 18.9 |
| 742.0 | 752.0 | app1 | True | 60840.0 | 21.1% | 36.0% | 15.0 |
| 742.0 | 752.0 | app2 | True | 51296.0 | 10.5% | 30.4% | 19.8 |
| 742.0 | 752.0 | end-users | True | 56774.0 | 68.4% | 33.6% | -34.8 |
| 752.0 | 762.0 | app1 | True | 1344.0 | 21.1% | 0.8% | -20.2 |
| 752.0 | 762.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 752.0 | 762.0 | end-users | True | 163674.0 | 68.4% | 98.4% | 30.0 |
| 762.0 | 772.0 | app1 | True | 35176.0 | 21.1% | 23.0% | 2.0 |
| 762.0 | 772.0 | app2 | True | 17578.0 | 10.5% | 11.5% | 1.0 |
| 762.0 | 772.0 | end-users | True | 100050.0 | 68.4% | 65.5% | -2.9 |
| 772.0 | 782.0 | app1 | True | 37768.0 | 21.1% | 21.8% | 0.8 |
| 772.0 | 782.0 | app2 | True | 40486.0 | 10.5% | 23.4% | 12.9 |
| 772.0 | 782.0 | end-users | True | 94598.0 | 68.4% | 54.7% | -13.7 |
| 782.0 | 792.0 | app1 | True | 2716.0 | 21.1% | 1.6% | -19.4 |
| 782.0 | 792.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 782.0 | 792.0 | end-users | True | 163628.0 | 68.4% | 98.4% | 29.9 |
| 792.0 | 802.0 | app1 | True | 44660.0 | 21.1% | 26.4% | 5.4 |
| 792.0 | 802.0 | app2 | True | 60706.0 | 10.5% | 35.9% | 25.4 |
| 792.0 | 802.0 | end-users | True | 63518.0 | 68.4% | 37.6% | -30.8 |
| 802.0 | 812.0 | app1 | True | 35114.0 | 21.1% | 22.8% | 1.7 |
| 802.0 | 812.0 | app2 | True | 1348.0 | 10.5% | 0.9% | -9.7 |
| 802.0 | 812.0 | end-users | True | 117542.0 | 68.4% | 76.3% | 7.9 |
| 812.0 | 822.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.2 |
| 812.0 | 822.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 812.0 | 822.0 | end-users | True | 166180.0 | 68.4% | 99.2% | 30.8 |
| 822.0 | 832.0 | app1 | True | 55304.0 | 21.1% | 32.2% | 11.2 |
| 822.0 | 832.0 | app2 | True | 60848.0 | 10.5% | 35.5% | 25.0 |
| 822.0 | 832.0 | end-users | True | 55362.0 | 68.4% | 32.3% | -36.1 |
| 832.0 | 843.0 | app1 | True | 25698.0 | 21.1% | 16.8% | -4.2 |
| 832.0 | 843.0 | app2 | True | 1354.0 | 10.5% | 0.9% | -9.6 |
| 832.0 | 843.0 | end-users | True | 125770.0 | 68.4% | 82.3% | 13.9 |
| 843.0 | 853.0 | app1 | True | 41878.0 | 21.1% | 25.2% | 4.1 |
| 843.0 | 853.0 | app2 | True | 14822.0 | 10.5% | 8.9% | -1.6 |
| 843.0 | 853.0 | end-users | True | 109626.0 | 68.4% | 65.9% | -2.5 |
| 853.0 | 863.0 | app1 | True | 14866.0 | 21.1% | 8.8% | -12.3 |
| 853.0 | 863.0 | app2 | True | 48704.0 | 10.5% | 28.8% | 18.3 |
| 853.0 | 863.0 | end-users | True | 105406.0 | 68.4% | 62.4% | -6.0 |
| 863.0 | 873.0 | app1 | True | 28438.0 | 21.1% | 17.2% | -3.8 |
| 863.0 | 873.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 863.0 | 873.0 | end-users | True | 136718.0 | 68.4% | 82.8% | 14.4 |
| 873.0 | 883.0 | app1 | True | 27014.0 | 21.1% | 17.5% | -3.5 |
| 873.0 | 883.0 | app2 | True | 13526.0 | 10.5% | 8.8% | -1.8 |
| 873.0 | 883.0 | end-users | True | 113634.0 | 68.4% | 73.7% | 5.3 |
| 883.0 | 893.0 | app1 | True | 36548.0 | 21.1% | 21.6% | 0.6 |
| 883.0 | 893.0 | app2 | True | 51430.0 | 10.5% | 30.4% | 19.9 |
| 883.0 | 893.0 | end-users | True | 81104.0 | 68.4% | 48.0% | -20.5 |
| 893.0 | 903.0 | app1 | True | 18950.0 | 21.1% | 11.2% | -9.8 |
| 893.0 | 903.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 893.0 | 903.0 | end-users | True | 150026.0 | 68.4% | 88.8% | 20.4 |
| 903.0 | 913.0 | app1 | False | 41854.0 | n/a | n/a | n/a |
| 903.0 | 913.0 | app2 | False | 41920.0 | n/a | n/a | n/a |
| 903.0 | 913.0 | end-users | False | 82502.0 | n/a | n/a | n/a |
| 913.0 | 923.0 | app1 | False | 1346.0 | n/a | n/a | n/a |
| 913.0 | 923.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 913.0 | 923.0 | end-users | False | 73026.0 | n/a | n/a | n/a |
| 923.0 | 931.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 923.0 | 931.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 923.0 | 931.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`, EPP restart detected mid-window at least once):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 20 | 62ms | 417ms | 900ms |
| 0.0 | 10.0 | app2 | ok | 15 | 212ms | 850ms | 985ms |
| 0.0 | 10.0 | end-users | ok | 63 | 166ms | 1450ms | 2395ms |
| 10.0 | 20.0 | app1 | ok | 47 | 3393ms | 8763ms | 9876ms |
| 10.0 | 20.0 | app2 | ok | 37 | 5595ms | 9119ms | 9912ms |
| 10.0 | 20.0 | end-users | ok | 186 | 3295ms | 8808ms | 9881ms |
| 20.0 | 30.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 32 | 13158ms | 26632ms | 29663ms |
| 30.0 | 40.0 | app2 | ok | 28 | 10000ms | 26000ms | 29600ms |
| 30.0 | 40.0 | end-users | ok | 110 | 6538ms | 22143ms | 29214ms |
| 40.0 | 51.0 | app1 | ok | 30 | 6250ms | 20000ms | 29000ms |
| 40.0 | 51.0 | app2 | ok | 20 | 20000ms | 28000ms | 29800ms |
| 40.0 | 51.0 | end-users | ok | 115 | 7171ms | 23611ms | 29361ms |
| 51.0 | 61.0 | app1 | ok | 26 | 1450ms | 4625ms | 27400ms |
| 51.0 | 61.0 | app2 | ok | 25 | 4375ms | 25833ms | 29583ms |
| 51.0 | 61.0 | end-users | ok | 116 | 9098ms | 25064ms | 29506ms |
| 61.0 | 71.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 61.0 | 71.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 61.0 | 71.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 71.0 | 81.0 | app1 | ok | 32 | 7917ms | 24182ms | 29418ms |
| 71.0 | 81.0 | app2 | ok | 25 | 20000ms | 28000ms | 29800ms |
| 71.0 | 81.0 | end-users | ok | 112 | 6125ms | 21040ms | 29104ms |
| 81.0 | 91.0 | app1 | ok | 28 | 1750ms | 4222ms | 4922ms |
| 81.0 | 91.0 | app2 | ok | 21 | 2812ms | 24000ms | 29400ms |
| 81.0 | 91.0 | end-users | ok | 127 | 9330ms | 25464ms | 29546ms |
| 91.0 | 101.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 91.0 | 101.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 91.0 | 101.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 30 | 8214ms | 24000ms | 29400ms |
| 101.0 | 111.0 | app2 | ok | 29 | 20000ms | 28000ms | 29800ms |
| 101.0 | 111.0 | end-users | ok | 114 | 5682ms | 18000ms | 28800ms |
| 111.0 | 121.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 111.0 | 121.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 111.0 | 121.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 121.0 | 131.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 121.0 | 131.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 121.0 | 131.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 131.0 | 141.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 131.0 | 141.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 131.0 | 141.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 141.0 | 151.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 141.0 | 151.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 141.0 | 151.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 151.0 | 161.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 151.0 | 161.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 151.0 | 161.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 23 | 4844ms | 18500ms | 28850ms |
| 161.0 | 171.0 | app2 | ok | 1 | 7500ms | 9500ms | 9950ms |
| 161.0 | 171.0 | end-users | ok | 106 | 5673ms | 9750ms | 27350ms |
| 171.0 | 181.0 | app1 | ok | 27 | 6094ms | 9469ms | 24600ms |
| 171.0 | 181.0 | app2 | ok | 1 | 7500ms | 9500ms | 9950ms |
| 171.0 | 181.0 | end-users | ok | 105 | 5231ms | 9120ms | 9995ms |
| 181.0 | 191.0 | app1 | ok | 22 | 3929ms | 8625ms | 9862ms |
| 181.0 | 191.0 | app2 | ok | 1 | 7500ms | 9500ms | 9950ms |
| 181.0 | 191.0 | end-users | ok | 109 | 5805ms | 9500ms | 25640ms |
| 191.0 | 201.0 | app1 | ok | 24 | 4062ms | 9125ms | 25200ms |
| 191.0 | 201.0 | app2 | ok | 1 | 7500ms | 9500ms | 9950ms |
| 191.0 | 201.0 | end-users | ok | 105 | 5647ms | 9267ms | 19500ms |
| 201.0 | 211.0 | app1 | ok | 20 | 3571ms | 9000ms | 26000ms |
| 201.0 | 211.0 | app2 | ok | 1 | 7500ms | 9500ms | 9950ms |
| 201.0 | 211.0 | end-users | ok | 109 | 5927ms | 9444ms | 24550ms |
| 211.0 | 221.0 | app1 | ok | 27 | 7596ms | 9673ms | 24600ms |
| 211.0 | 221.0 | app2 | ok | 1 | 7500ms | 9500ms | 9950ms |
| 211.0 | 221.0 | end-users | ok | 103 | 4375ms | 9212ms | 24850ms |
| 221.0 | 231.0 | app1 | ok | 12 | 2500ms | 4500ms | 4950ms |
| 221.0 | 231.0 | app2 | ok | 1 | 3750ms | 4750ms | 4975ms |
| 221.0 | 231.0 | end-users | ok | 117 | 5933ms | 9425ms | 24150ms |
| 231.0 | 241.0 | app1 | ok | 24 | 6667ms | 22000ms | 29200ms |
| 231.0 | 241.0 | app2 | ok | 1 | 3750ms | 4750ms | 4975ms |
| 231.0 | 241.0 | end-users | ok | 105 | 5395ms | 9079ms | 9908ms |
| 241.0 | 251.0 | app1 | ok | 13 | 1750ms | 9250ms | 27400ms |
| 241.0 | 251.0 | app2 | ok | 1 | 3750ms | 4750ms | 4975ms |
| 241.0 | 251.0 | end-users | ok | 118 | 5846ms | 9477ms | 25280ms |
| 251.0 | 261.0 | app1 | ok | 26 | 7955ms | 17000ms | 28700ms |
| 251.0 | 261.0 | app2 | ok | 1 | 7500ms | 9500ms | 9950ms |
| 251.0 | 261.0 | end-users | ok | 103 | 4375ms | 8830ms | 9883ms |
| 261.0 | 271.0 | app1 | ok | 27 | 7500ms | 9500ms | 9950ms |
| 261.0 | 271.0 | app2 | ok | 1 | 7500ms | 9500ms | 9950ms |
| 261.0 | 271.0 | end-users | ok | 105 | 4353ms | 9207ms | 24750ms |
| 271.0 | 281.0 | app1 | ok | 13 | 625ms | 1525ms | 2402ms |
| 271.0 | 281.0 | app2 | ok | 1 | 1750ms | 2350ms | 2485ms |
| 271.0 | 281.0 | end-users | ok | 115 | 5993ms | 9375ms | 22333ms |
| 281.0 | 291.0 | app1 | ok | 14 | 8182ms | 20667ms | 29067ms |
| 281.0 | 291.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | ok | 116 | 5085ms | 9017ms | 9902ms |
| 291.0 | 301.0 | app1 | ok | 27 | 7596ms | 9673ms | 24600ms |
| 291.0 | 301.0 | app2 | ok | 1 | 7500ms | 9500ms | 9950ms |
| 291.0 | 301.0 | end-users | ok | 102 | 4375ms | 9024ms | 19800ms |
| 301.0 | 311.0 | app1 | ok | 12 | 417ms | 975ms | 2320ms |
| 301.0 | 311.0 | app2 | ok | 1 | 1750ms | 2350ms | 2485ms |
| 301.0 | 311.0 | end-users | ok | 118 | 5970ms | 9493ms | 25280ms |
| 311.0 | 321.0 | app1 | ok | 26 | 7708ms | 9875ms | 27400ms |
| 311.0 | 321.0 | app2 | ok | 1 | 7500ms | 9500ms | 9950ms |
| 311.0 | 321.0 | end-users | ok | 103 | 4476ms | 8856ms | 9886ms |
| 321.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | ok | 27 | 7500ms | 9500ms | 9950ms |
| 331.0 | 341.0 | app2 | ok | 1 | 7500ms | 9500ms | 9950ms |
| 331.0 | 341.0 | end-users | ok | 103 | 4330ms | 8919ms | 9997ms |
| 341.0 | 351.0 | app1 | ok | 15 | 679ms | 1750ms | 2425ms |
| 341.0 | 351.0 | app2 | ok | 1 | 1750ms | 2350ms | 2485ms |
| 341.0 | 351.0 | end-users | ok | 116 | 5986ms | 9254ms | 9989ms |
| 351.0 | 361.0 | app1 | ok | 13 | 8929ms | 24800ms | 29480ms |
| 351.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | ok | 118 | 5172ms | 9241ms | 22133ms |
| 361.0 | 371.0 | app1 | ok | 27 | 7700ms | 9860ms | 27300ms |
| 361.0 | 371.0 | app2 | ok | 1 | 20000ms | 28000ms | 29800ms |
| 361.0 | 371.0 | end-users | ok | 105 | 4258ms | 8779ms | 9878ms |
| 371.0 | 381.0 | app1 | ok | 12 | 583ms | 983ms | 2320ms |
| 371.0 | 381.0 | app2 | ok | 1 | 750ms | 950ms | 995ms |
| 371.0 | 381.0 | end-users | ok | 117 | 6036ms | 9379ms | 22200ms |
| 381.0 | 391.0 | app1 | ok | 15 | 7885ms | 15000ms | 28500ms |
| 381.0 | 391.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | ok | 115 | 4957ms | 8991ms | 9899ms |
| 391.0 | 401.0 | app1 | ok | 27 | 7500ms | 9500ms | 9950ms |
| 391.0 | 401.0 | app2 | ok | 1 | 7500ms | 9500ms | 9950ms |
| 391.0 | 401.0 | end-users | ok | 101 | 4471ms | 8966ms | 9999ms |
| 401.0 | 411.0 | app1 | ok | 10 | 312ms | 750ms | 975ms |
| 401.0 | 411.0 | app2 | ok | 1 | 750ms | 950ms | 995ms |
| 401.0 | 411.0 | end-users | ok | 118 | 5959ms | 9192ms | 9919ms |
| 411.0 | 421.0 | app1 | ok | 27 | 7700ms | 9860ms | 27300ms |
| 411.0 | 421.0 | app2 | ok | 1 | 7500ms | 9500ms | 9950ms |
| 411.0 | 421.0 | end-users | ok | 104 | 4333ms | 8818ms | 9882ms |
| 421.0 | 431.0 | app1 | ok | 16 | 700ms | 8400ms | 9840ms |
| 421.0 | 431.0 | app2 | ok | 23 | 7500ms | 9500ms | 9950ms |
| 421.0 | 431.0 | end-users | ok | 128 | 6299ms | 9623ms | 26343ms |
| 431.0 | 441.0 | app1 | ok | 32 | 19677ms | 27935ms | 29794ms |
| 431.0 | 441.0 | app2 | ok | 27 | 9062ms | 25500ms | 29550ms |
| 431.0 | 441.0 | end-users | ok | 109 | 6480ms | 19100ms | 28910ms |
| 441.0 | 452.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 452.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 452.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app1 | ok | 29 | 5577ms | 10667ms | 28067ms |
| 452.0 | 462.0 | app2 | ok | 26 | 20000ms | 28000ms | 29800ms |
| 452.0 | 462.0 | end-users | ok | 115 | 6607ms | 22069ms | 29207ms |
| 462.0 | 472.0 | app1 | ok | 29 | 1696ms | 10667ms | 28067ms |
| 462.0 | 472.0 | app2 | ok | 18 | 2250ms | 24000ms | 29400ms |
| 462.0 | 472.0 | end-users | ok | 120 | 9386ms | 25472ms | 29547ms |
| 472.0 | 482.0 | app1 | ok | 32 | 6786ms | 20857ms | 29086ms |
| 472.0 | 482.0 | app2 | ok | 26 | 20000ms | 28000ms | 29800ms |
| 472.0 | 482.0 | end-users | ok | 112 | 5930ms | 19333ms | 28933ms |
| 482.0 | 492.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app1 | ok | 27 | 1938ms | 4250ms | 4925ms |
| 492.0 | 502.0 | app2 | ok | 21 | 2750ms | 23000ms | 29300ms |
| 492.0 | 502.0 | end-users | ok | 123 | 9605ms | 25684ms | 29568ms |
| 502.0 | 512.0 | app1 | ok | 32 | 7857ms | 23600ms | 29360ms |
| 502.0 | 512.0 | app2 | ok | 27 | 20000ms | 28000ms | 29800ms |
| 502.0 | 512.0 | end-users | ok | 114 | 5795ms | 18600ms | 28860ms |
| 512.0 | 522.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app1 | ok | 29 | 1825ms | 4275ms | 4928ms |
| 522.0 | 532.0 | app2 | ok | 20 | 2917ms | 22000ms | 29200ms |
| 522.0 | 532.0 | end-users | ok | 125 | 9458ms | 25536ms | 29554ms |
| 532.0 | 542.0 | app1 | ok | 32 | 7308ms | 22889ms | 29289ms |
| 532.0 | 542.0 | app2 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 532.0 | 542.0 | end-users | ok | 113 | 5833ms | 18105ms | 28811ms |
| 542.0 | 552.0 | app1 | ok | 16 | 3182ms | 4636ms | 4964ms |
| 542.0 | 552.0 | app2 | ok | 18 | 2250ms | 12000ms | 28200ms |
| 542.0 | 552.0 | end-users | ok | 51 | 20000ms | 28000ms | 29800ms |
| 552.0 | 562.0 | app1 | ok | 14 | 900ms | 2150ms | 2465ms |
| 552.0 | 562.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 552.0 | 562.0 | end-users | ok | 72 | 7727ms | 16909ms | 28691ms |
| 562.0 | 572.0 | app1 | ok | 32 | 6923ms | 22000ms | 29200ms |
| 562.0 | 572.0 | app2 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 562.0 | 572.0 | end-users | ok | 113 | 5988ms | 19727ms | 28973ms |
| 572.0 | 582.0 | app1 | ok | 32 | 1750ms | 4200ms | 4920ms |
| 572.0 | 582.0 | app2 | ok | 19 | 2050ms | 11000ms | 28100ms |
| 572.0 | 582.0 | end-users | ok | 119 | 11111ms | 26222ms | 29622ms |
| 582.0 | 592.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 582.0 | 592.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 582.0 | 592.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 592.0 | 602.0 | app1 | ok | 31 | 6250ms | 17600ms | 28760ms |
| 592.0 | 602.0 | app2 | ok | 25 | 20000ms | 28000ms | 29800ms |
| 592.0 | 602.0 | end-users | ok | 114 | 6429ms | 21556ms | 29156ms |
| 602.0 | 612.0 | app1 | ok | 29 | 1825ms | 4472ms | 24200ms |
| 602.0 | 612.0 | app2 | ok | 21 | 2375ms | 24000ms | 29400ms |
| 602.0 | 612.0 | end-users | ok | 128 | 9138ms | 25259ms | 29526ms |
| 612.0 | 622.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 612.0 | 622.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 612.0 | 622.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 622.0 | 632.0 | app1 | ok | 32 | 7857ms | 23600ms | 29360ms |
| 622.0 | 632.0 | app2 | ok | 21 | 20000ms | 28000ms | 29800ms |
| 622.0 | 632.0 | end-users | ok | 112 | 5833ms | 19333ms | 28933ms |
| 632.0 | 642.0 | app1 | ok | 25 | 1525ms | 3958ms | 4896ms |
| 632.0 | 642.0 | app2 | ok | 24 | 4167ms | 25636ms | 29564ms |
| 632.0 | 642.0 | end-users | ok | 123 | 8958ms | 24980ms | 29498ms |
| 642.0 | 652.0 | app1 | ok | 32 | 8214ms | 24182ms | 29418ms |
| 642.0 | 652.0 | app2 | ok | 22 | 20000ms | 28000ms | 29800ms |
| 642.0 | 652.0 | end-users | ok | 111 | 5536ms | 17667ms | 28767ms |
| 652.0 | 662.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 652.0 | 662.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 652.0 | 662.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 662.0 | 672.0 | app1 | ok | 25 | 1341ms | 3438ms | 4844ms |
| 662.0 | 672.0 | app2 | ok | 23 | 3125ms | 25400ms | 29540ms |
| 662.0 | 672.0 | end-users | ok | 119 | 9267ms | 25333ms | 29533ms |
| 672.0 | 682.0 | app1 | ok | 32 | 8077ms | 24182ms | 29418ms |
| 672.0 | 682.0 | app2 | ok | 19 | 20000ms | 28000ms | 29800ms |
| 672.0 | 682.0 | end-users | ok | 112 | 5778ms | 17556ms | 28756ms |
| 682.0 | 692.0 | app1 | ok | 24 | 1450ms | 3800ms | 4880ms |
| 682.0 | 692.0 | app2 | ok | 26 | 5000ms | 26000ms | 29600ms |
| 682.0 | 692.0 | end-users | ok | 123 | 9025ms | 25080ms | 29508ms |
| 692.0 | 702.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 692.0 | 702.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 692.0 | 702.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 702.0 | 712.0 | app1 | ok | 31 | 8750ms | 24833ms | 29483ms |
| 702.0 | 712.0 | app2 | ok | 15 | 20000ms | 28000ms | 29800ms |
| 702.0 | 712.0 | end-users | ok | 111 | 5611ms | 16125ms | 28612ms |
| 712.0 | 722.0 | app1 | ok | 21 | 1205ms | 2350ms | 25800ms |
| 712.0 | 722.0 | app2 | ok | 26 | 14706ms | 26941ms | 29694ms |
| 712.0 | 722.0 | end-users | ok | 113 | 8664ms | 24488ms | 29449ms |
| 722.0 | 732.0 | app1 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 722.0 | 732.0 | app2 | ok | 17 | 20000ms | 28000ms | 29800ms |
| 722.0 | 732.0 | end-users | ok | 114 | 4904ms | 14800ms | 28480ms |
| 732.0 | 742.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 732.0 | 742.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 732.0 | 742.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 742.0 | 752.0 | app1 | ok | 23 | 1375ms | 3562ms | 4856ms |
| 742.0 | 752.0 | app2 | ok | 27 | 12000ms | 26400ms | 29640ms |
| 742.0 | 752.0 | end-users | ok | 123 | 8728ms | 24766ms | 29477ms |
| 752.0 | 762.0 | app1 | ok | 32 | 19677ms | 27935ms | 29794ms |
| 752.0 | 762.0 | app2 | ok | 20 | 20000ms | 28000ms | 29800ms |
| 752.0 | 762.0 | end-users | ok | 114 | 4839ms | 9360ms | 25440ms |
| 762.0 | 772.0 | app1 | ok | 24 | 1625ms | 3800ms | 4880ms |
| 762.0 | 772.0 | app2 | ok | 24 | 5000ms | 26000ms | 29600ms |
| 762.0 | 772.0 | end-users | ok | 124 | 9035ms | 25137ms | 29514ms |
| 772.0 | 782.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 772.0 | 782.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 772.0 | 782.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 782.0 | 792.0 | app1 | ok | 32 | 8571ms | 24667ms | 29467ms |
| 782.0 | 792.0 | app2 | ok | 26 | 20000ms | 28000ms | 29800ms |
| 782.0 | 792.0 | end-users | ok | 113 | 5407ms | 16706ms | 28671ms |
| 792.0 | 802.0 | app1 | ok | 28 | 1818ms | 4222ms | 4922ms |
| 792.0 | 802.0 | app2 | ok | 21 | 2750ms | 23000ms | 29300ms |
| 792.0 | 802.0 | end-users | ok | 118 | 9828ms | 25860ms | 29586ms |
| 802.0 | 812.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 802.0 | 812.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 802.0 | 812.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 812.0 | 822.0 | app1 | ok | 32 | 7143ms | 22000ms | 29200ms |
| 812.0 | 822.0 | app2 | ok | 26 | 20000ms | 28000ms | 29800ms |
| 812.0 | 822.0 | end-users | ok | 111 | 6080ms | 19429ms | 28943ms |
| 822.0 | 832.0 | app1 | ok | 29 | 1688ms | 4094ms | 4909ms |
| 822.0 | 832.0 | app2 | ok | 21 | 2750ms | 23000ms | 29300ms |
| 822.0 | 832.0 | end-users | ok | 128 | 9364ms | 25509ms | 29551ms |
| 832.0 | 843.0 | app1 | ok | 31 | 7885ms | 23800ms | 29380ms |
| 832.0 | 843.0 | app2 | ok | 19 | 20000ms | 28000ms | 29800ms |
| 832.0 | 843.0 | end-users | ok | 114 | 6000ms | 19143ms | 28914ms |
| 843.0 | 853.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 843.0 | 853.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 843.0 | 853.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 853.0 | 863.0 | app1 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 853.0 | 863.0 | app2 | ok | 29 | 9688ms | 25857ms | 29586ms |
| 853.0 | 863.0 | end-users | ok | 104 | 6327ms | 17000ms | 28700ms |
| 863.0 | 873.0 | app1 | ok | 29 | 5536ms | 9679ms | 27100ms |
| 863.0 | 873.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 863.0 | 873.0 | end-users | ok | 117 | 6534ms | 21643ms | 29164ms |
| 873.0 | 883.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 873.0 | 883.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 873.0 | 883.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 883.0 | 893.0 | app1 | ok | 32 | 2679ms | 4964ms | 27867ms |
| 883.0 | 893.0 | app2 | ok | 17 | 1750ms | 4292ms | 4929ms |
| 883.0 | 893.0 | end-users | ok | 117 | 10169ms | 26034ms | 29603ms |
| 893.0 | 903.0 | app1 | ok | 31 | 5962ms | 17600ms | 28760ms |
| 893.0 | 903.0 | app2 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 893.0 | 903.0 | end-users | ok | 112 | 6310ms | 21040ms | 29104ms |
| 903.0 | 913.0 | app1 | ok | 1 | 20000ms | 28000ms | 29800ms |
| 903.0 | 913.0 | app2 | ok | 8 | 20000ms | 28000ms | 29800ms |
| 903.0 | 913.0 | end-users | ok | 56 | 19231ms | 27846ms | 29785ms |
| 913.0 | 923.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 913.0 | 923.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 913.0 | 923.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 923.0 | 931.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 923.0 | 931.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 923.0 | 931.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens -21.3%, cost -21.9%
- app2 exceeded the 10% ledger tolerance: raw tokens -21.4%, cost -22.8%
- end-users exceeded the 10% ledger tolerance: raw tokens -19.6%, cost -19.9%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2393580 | 118743 | 1977640.0 | -21.3% | 2056066.0 | 2631066.0 | -21.9% | False |
| app2 | 1313640 | 65089 | 1084359.0 | -21.4% | 1115208.0 | 1443818.0 | -22.8% | False |
| end-users | 10521420 | 521750 | 8883216.0 | -19.6% | 9266328.0 | 11564920.0 | -19.9% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1962 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | 0.0% | 0.00 |
| app2 | 1111 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | 0.0% | 0.00 |
| end-users | 8630 | 0 | 13 | 13 | 0.15% | 68.4% | 100.0% | 1.46 |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=9253). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 747668 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
