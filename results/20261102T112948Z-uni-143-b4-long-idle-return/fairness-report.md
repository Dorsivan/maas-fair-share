# Fairness benchmark: full-contention (uni-143-b4-long-idle-return)

**Verdict: FAIL** (threshold: 10 points)

- app1 deviated -15.5 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `890` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-575669c495-gv2k9` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-02T11:31:01Z` |
| Run end | `2026-11-02T11:46:14Z` |

## Per-group result

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 643 | 200=643 | 16.2 | 26.0 | 825116.0 | 21.1% | 5.5% | -15.5 | 5.9s | 98.9% | 643.0 |
| app2 | 10.0 | 32 | 1723 | 200=1722, 500=1 | 21.6 | 26.6 | 2284396.0 | 10.5% | 15.3% | 4.8 | 9.3s | 98.9% | 1722.0 |
| end-users | 65.0 | 128 | 8775 | 200=8746, 500=29 | 13.0 | 18.5 | 11778504.0 | 68.4% | 79.1% | 10.7 | 9.5s | 98.9% | 8746.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-890s, 150s on / 600s off
- app2: active 0s-890s, no duty cycle
- end-users: active 0s-890s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 150.0 | n/a (never converged in this phase) | n/a |
| 750.0 | n/a (never converged in this phase) | n/a |
| 890.0 | n/a (never converged in this phase) | n/a |

**Windows** (91 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 4050.0 | 21.1% | 3.9% | -17.1 |
| 0.0 | 10.0 | app2 | True | 28382.0 | 10.5% | 27.6% | 17.1 |
| 0.0 | 10.0 | end-users | True | 70364.0 | 68.4% | 68.5% | 0.0 |
| 10.0 | 20.0 | app1 | True | 43318.0 | 21.1% | 25.8% | 4.8 |
| 10.0 | 20.0 | app2 | True | 27060.0 | 10.5% | 16.1% | 5.6 |
| 10.0 | 20.0 | end-users | True | 97484.0 | 68.4% | 58.1% | -10.3 |
| 20.0 | 30.0 | app1 | True | 20262.0 | 21.1% | 13.4% | -7.7 |
| 20.0 | 30.0 | app2 | True | 17554.0 | 10.5% | 11.6% | 1.1 |
| 20.0 | 30.0 | end-users | True | 113656.0 | 68.4% | 75.0% | 6.6 |
| 30.0 | 40.0 | app1 | True | 5432.0 | 21.1% | 3.2% | -17.8 |
| 30.0 | 40.0 | app2 | True | 23048.0 | 10.5% | 13.7% | 3.2 |
| 30.0 | 40.0 | end-users | True | 139406.0 | 68.4% | 83.0% | 14.6 |
| 40.0 | 50.0 | app1 | True | 58120.0 | 21.1% | 34.1% | 13.0 |
| 40.0 | 50.0 | app2 | True | 39270.0 | 10.5% | 23.0% | 12.5 |
| 40.0 | 50.0 | end-users | True | 73126.0 | 68.4% | 42.9% | -25.5 |
| 50.0 | 60.0 | app1 | True | 2708.0 | 21.1% | 1.6% | -19.5 |
| 50.0 | 60.0 | app2 | True | 12144.0 | 10.5% | 7.1% | -3.4 |
| 50.0 | 60.0 | end-users | True | 155562.0 | 68.4% | 91.3% | 22.9 |
| 60.0 | 70.0 | app1 | True | 24284.0 | 21.1% | 15.5% | -5.6 |
| 60.0 | 70.0 | app2 | True | 13508.0 | 10.5% | 8.6% | -1.9 |
| 60.0 | 70.0 | end-users | True | 118998.0 | 68.4% | 75.9% | 7.5 |
| 70.0 | 80.0 | app1 | True | 43328.0 | 21.1% | 25.8% | 4.8 |
| 70.0 | 80.0 | app2 | True | 47328.0 | 10.5% | 28.2% | 17.7 |
| 70.0 | 80.0 | end-users | True | 77064.0 | 68.4% | 45.9% | -22.5 |
| 80.0 | 90.0 | app1 | True | 10850.0 | 21.1% | 6.3% | -14.8 |
| 80.0 | 90.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 80.0 | 90.0 | end-users | True | 162110.0 | 68.4% | 93.7% | 25.3 |
| 90.0 | 100.0 | app1 | True | 43236.0 | 21.1% | 25.2% | 4.1 |
| 90.0 | 100.0 | app2 | True | 55450.0 | 10.5% | 32.3% | 21.8 |
| 90.0 | 100.0 | end-users | True | 72940.0 | 68.4% | 42.5% | -25.9 |
| 100.0 | 110.0 | app1 | True | 35146.0 | 21.1% | 23.2% | 2.1 |
| 100.0 | 110.0 | app2 | True | 5408.0 | 10.5% | 3.6% | -7.0 |
| 100.0 | 110.0 | end-users | True | 110938.0 | 68.4% | 73.2% | 4.8 |
| 110.0 | 120.0 | app1 | True | 4042.0 | 21.1% | 2.4% | -18.6 |
| 110.0 | 120.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 110.0 | 120.0 | end-users | True | 163690.0 | 68.4% | 97.6% | 29.2 |
| 120.0 | 130.0 | app1 | True | 47294.0 | 21.1% | 28.2% | 7.2 |
| 120.0 | 130.0 | app2 | True | 59480.0 | 10.5% | 35.5% | 25.0 |
| 120.0 | 130.0 | end-users | True | 60856.0 | 68.4% | 36.3% | -32.1 |
| 130.0 | 140.0 | app1 | True | 33822.0 | 21.1% | 21.9% | 0.9 |
| 130.0 | 140.0 | app2 | True | 1358.0 | 10.5% | 0.9% | -9.6 |
| 130.0 | 140.0 | end-users | True | 118970.0 | 68.4% | 77.2% | 8.8 |
| 140.0 | 150.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 140.0 | 150.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 140.0 | 150.0 | end-users | True | 170470.0 | 68.4% | 100.0% | 31.6 |
| 150.0 | 160.0 | app1 | False | 43270.0 | n/a | n/a | n/a |
| 150.0 | 160.0 | app2 | True | 59464.0 | 13.3% | 48.3% | 34.9 |
| 150.0 | 160.0 | end-users | True | 63722.0 | 86.7% | 51.7% | -34.9 |
| 160.0 | 170.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 160.0 | 170.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 160.0 | 170.0 | end-users | True | 167654.0 | 86.7% | 100.0% | 13.3 |
| 170.0 | 180.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 170.0 | 180.0 | app2 | True | 60924.0 | 13.3% | 36.6% | 23.3 |
| 170.0 | 180.0 | end-users | True | 105514.0 | 86.7% | 63.4% | -23.3 |
| 180.0 | 190.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 180.0 | 190.0 | app2 | True | 1358.0 | 13.3% | 0.9% | -12.5 |
| 180.0 | 190.0 | end-users | True | 154212.0 | 86.7% | 99.1% | 12.5 |
| 190.0 | 200.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 190.0 | 200.0 | app2 | True | 4058.0 | 13.3% | 2.4% | -10.9 |
| 190.0 | 200.0 | end-users | True | 163610.0 | 86.7% | 97.6% | 10.9 |
| 200.0 | 211.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 200.0 | 211.0 | app2 | True | 60860.0 | 13.3% | 36.3% | 23.0 |
| 200.0 | 211.0 | end-users | True | 106842.0 | 86.7% | 63.7% | -23.0 |
| 211.0 | 221.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 211.0 | 221.0 | app2 | True | 42038.0 | 13.3% | 25.1% | 11.7 |
| 211.0 | 221.0 | end-users | True | 125776.0 | 86.7% | 74.9% | -11.7 |
| 221.0 | 231.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 221.0 | 231.0 | end-users | True | 163872.0 | 86.7% | 100.0% | 13.3 |
| 231.0 | 241.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app2 | True | 63520.0 | 13.3% | 37.0% | 23.7 |
| 231.0 | 241.0 | end-users | True | 108210.0 | 86.7% | 63.0% | -23.7 |
| 241.0 | 251.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 241.0 | 251.0 | end-users | True | 171668.0 | 86.7% | 100.0% | 13.3 |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | True | 18956.0 | 13.3% | 12.5% | -0.8 |
| 251.0 | 261.0 | end-users | True | 132630.0 | 86.7% | 87.5% | 0.8 |
| 261.0 | 271.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | True | 44666.0 | 13.3% | 27.1% | 13.7 |
| 261.0 | 271.0 | end-users | True | 120316.0 | 86.7% | 72.9% | -13.7 |
| 271.0 | 281.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 271.0 | 281.0 | end-users | True | 170326.0 | 86.7% | 100.0% | 13.3 |
| 281.0 | 291.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | True | 62158.0 | 13.3% | 37.4% | 24.0 |
| 281.0 | 291.0 | end-users | True | 104238.0 | 86.7% | 62.6% | -24.0 |
| 291.0 | 301.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | True | 1358.0 | 13.3% | 0.8% | -12.5 |
| 291.0 | 301.0 | end-users | True | 165140.0 | 86.7% | 99.2% | 12.5 |
| 301.0 | 311.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | True | 60778.0 | 13.3% | 35.7% | 22.4 |
| 301.0 | 311.0 | end-users | True | 109454.0 | 86.7% | 64.3% | -22.4 |
| 311.0 | 321.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | True | 2704.0 | 13.3% | 1.6% | -11.8 |
| 311.0 | 321.0 | end-users | True | 169146.0 | 86.7% | 98.4% | 11.8 |
| 321.0 | 331.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | True | 21680.0 | 13.3% | 14.3% | 1.0 |
| 321.0 | 331.0 | end-users | True | 129928.0 | 86.7% | 85.7% | -1.0 |
| 331.0 | 341.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | True | 40474.0 | 13.3% | 23.6% | 10.2 |
| 331.0 | 341.0 | end-users | True | 131234.0 | 86.7% | 76.4% | -10.2 |
| 341.0 | 351.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | True | 1358.0 | 13.3% | 0.8% | -12.5 |
| 341.0 | 351.0 | end-users | True | 167826.0 | 86.7% | 99.2% | 12.5 |
| 351.0 | 361.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | True | 43254.0 | 13.3% | 26.2% | 12.9 |
| 351.0 | 361.0 | end-users | True | 121838.0 | 86.7% | 73.8% | -12.9 |
| 361.0 | 371.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | True | 44706.0 | 13.3% | 27.1% | 13.7 |
| 361.0 | 371.0 | end-users | True | 120440.0 | 86.7% | 72.9% | -13.7 |
| 371.0 | 381.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 371.0 | 381.0 | end-users | True | 167696.0 | 86.7% | 100.0% | 13.3 |
| 381.0 | 391.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | True | 43308.0 | 13.3% | 25.0% | 11.7 |
| 381.0 | 391.0 | end-users | True | 129862.0 | 86.7% | 75.0% | -11.7 |
| 391.0 | 401.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | True | 5418.0 | 13.3% | 3.5% | -9.8 |
| 391.0 | 401.0 | end-users | True | 147426.0 | 86.7% | 96.5% | 9.8 |
| 401.0 | 411.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | True | 41930.0 | 13.3% | 25.0% | 11.7 |
| 401.0 | 411.0 | end-users | True | 125820.0 | 86.7% | 75.0% | -11.7 |
| 411.0 | 421.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 411.0 | 421.0 | end-users | True | 165152.0 | 86.7% | 100.0% | 13.3 |
| 421.0 | 431.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | True | 63434.0 | 13.3% | 37.3% | 23.9 |
| 421.0 | 431.0 | end-users | True | 106836.0 | 86.7% | 62.7% | -23.9 |
| 431.0 | 441.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 431.0 | 441.0 | end-users | True | 166402.0 | 86.7% | 100.0% | 13.3 |
| 441.0 | 451.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | True | 43282.0 | 13.3% | 25.6% | 12.3 |
| 441.0 | 451.0 | end-users | True | 125892.0 | 86.7% | 74.4% | -12.3 |
| 451.0 | 461.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | True | 29792.0 | 13.3% | 18.8% | 5.5 |
| 451.0 | 461.0 | end-users | True | 128706.0 | 86.7% | 81.2% | -5.5 |
| 461.0 | 471.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app2 | True | 13552.0 | 13.3% | 8.6% | -4.8 |
| 461.0 | 471.0 | end-users | True | 144634.0 | 86.7% | 91.4% | 4.8 |
| 471.0 | 481.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 471.0 | 481.0 | end-users | True | 169058.0 | 86.7% | 100.0% | 13.3 |
| 481.0 | 491.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app2 | True | 63598.0 | 13.3% | 37.9% | 24.6 |
| 481.0 | 491.0 | end-users | True | 104078.0 | 86.7% | 62.1% | -24.6 |
| 491.0 | 501.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app2 | True | 1358.0 | 13.3% | 0.8% | -12.5 |
| 491.0 | 501.0 | end-users | True | 164842.0 | 86.7% | 99.2% | 12.5 |
| 501.0 | 511.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 511.0 | app2 | True | 43302.0 | 13.3% | 25.4% | 12.1 |
| 501.0 | 511.0 | end-users | True | 127242.0 | 86.7% | 74.6% | -12.1 |
| 511.0 | 521.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 511.0 | 521.0 | app2 | True | 41996.0 | 13.3% | 25.0% | 11.7 |
| 511.0 | 521.0 | end-users | True | 125732.0 | 86.7% | 75.0% | -11.7 |
| 521.0 | 531.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 521.0 | 531.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 521.0 | 531.0 | end-users | True | 166296.0 | 86.7% | 100.0% | 13.3 |
| 531.0 | 541.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 531.0 | 541.0 | app2 | True | 18958.0 | 13.3% | 12.1% | -1.2 |
| 531.0 | 541.0 | end-users | True | 137812.0 | 86.7% | 87.9% | 1.2 |
| 541.0 | 551.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 541.0 | 551.0 | app2 | True | 24324.0 | 13.3% | 14.6% | 1.3 |
| 541.0 | 551.0 | end-users | True | 142030.0 | 86.7% | 85.4% | -1.3 |
| 551.0 | 561.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 551.0 | 561.0 | app2 | True | 43286.0 | 13.3% | 25.4% | 12.1 |
| 551.0 | 561.0 | end-users | True | 127190.0 | 86.7% | 74.6% | -12.1 |
| 561.0 | 571.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 561.0 | 571.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 561.0 | 571.0 | end-users | True | 170330.0 | 86.7% | 100.0% | 13.3 |
| 571.0 | 582.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 571.0 | 582.0 | app2 | True | 63532.0 | 13.3% | 37.0% | 23.7 |
| 571.0 | 582.0 | end-users | True | 108176.0 | 86.7% | 63.0% | -23.7 |
| 582.0 | 592.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 582.0 | 592.0 | app2 | True | 2696.0 | 13.3% | 1.6% | -11.7 |
| 582.0 | 592.0 | end-users | True | 166334.0 | 86.7% | 98.4% | 11.7 |
| 592.0 | 602.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 592.0 | 602.0 | app2 | True | 56822.0 | 13.3% | 32.6% | 19.2 |
| 592.0 | 602.0 | end-users | True | 117692.0 | 86.7% | 67.4% | -19.2 |
| 602.0 | 612.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 602.0 | 612.0 | app2 | True | 5416.0 | 13.3% | 3.7% | -9.6 |
| 602.0 | 612.0 | end-users | True | 140808.0 | 86.7% | 96.3% | 9.6 |
| 612.0 | 622.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 612.0 | 622.0 | app2 | True | 4062.0 | 13.3% | 2.4% | -10.9 |
| 612.0 | 622.0 | end-users | True | 163608.0 | 86.7% | 97.6% | 10.9 |
| 622.0 | 632.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 622.0 | 632.0 | app2 | True | 39284.0 | 13.3% | 23.2% | 9.9 |
| 622.0 | 632.0 | end-users | True | 129936.0 | 86.7% | 76.8% | -9.9 |
| 632.0 | 642.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 632.0 | 642.0 | app2 | True | 41932.0 | 13.3% | 24.4% | 11.1 |
| 632.0 | 642.0 | end-users | True | 129848.0 | 86.7% | 75.6% | -11.1 |
| 642.0 | 652.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 642.0 | 652.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 642.0 | 652.0 | end-users | True | 167666.0 | 86.7% | 100.0% | 13.3 |
| 652.0 | 662.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 652.0 | 662.0 | app2 | True | 63632.0 | 13.3% | 37.7% | 24.3 |
| 652.0 | 662.0 | end-users | True | 105268.0 | 86.7% | 62.3% | -24.3 |
| 662.0 | 672.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 662.0 | 672.0 | app2 | True | 1326.0 | 13.3% | 0.8% | -12.5 |
| 662.0 | 672.0 | end-users | True | 167824.0 | 86.7% | 99.2% | 12.5 |
| 672.0 | 682.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 672.0 | 682.0 | app2 | True | 32480.0 | 13.3% | 21.4% | 8.1 |
| 672.0 | 682.0 | end-users | True | 119156.0 | 86.7% | 78.6% | -8.1 |
| 682.0 | 692.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 682.0 | 692.0 | app2 | True | 31116.0 | 13.3% | 18.8% | 5.5 |
| 682.0 | 692.0 | end-users | True | 134052.0 | 86.7% | 81.2% | -5.5 |
| 692.0 | 702.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 692.0 | 702.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 692.0 | 702.0 | end-users | True | 169140.0 | 86.7% | 100.0% | 13.3 |
| 702.0 | 712.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 702.0 | 712.0 | app2 | True | 62152.0 | 13.3% | 36.8% | 23.4 |
| 702.0 | 712.0 | end-users | True | 106818.0 | 86.7% | 63.2% | -23.4 |
| 712.0 | 722.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 712.0 | 722.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 712.0 | 722.0 | end-users | True | 166320.0 | 86.7% | 100.0% | 13.3 |
| 722.0 | 732.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 722.0 | 732.0 | app2 | True | 43220.0 | 13.3% | 25.6% | 12.3 |
| 722.0 | 732.0 | end-users | True | 125710.0 | 86.7% | 74.4% | -12.3 |
| 732.0 | 742.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 732.0 | 742.0 | app2 | True | 43242.0 | 13.3% | 25.0% | 11.6 |
| 732.0 | 742.0 | end-users | True | 129978.0 | 86.7% | 75.0% | -11.6 |
| 742.0 | 752.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 742.0 | 752.0 | app2 | True | 0.0 | 13.3% | 0.0% | -13.3 |
| 742.0 | 752.0 | end-users | True | 152706.0 | 86.7% | 100.0% | 13.3 |
| 752.0 | 762.0 | app1 | True | 2716.0 | 21.1% | 1.7% | -19.4 |
| 752.0 | 762.0 | app2 | True | 1334.0 | 10.5% | 0.8% | -9.7 |
| 752.0 | 762.0 | end-users | True | 158454.0 | 68.4% | 97.5% | 29.1 |
| 762.0 | 772.0 | app1 | True | 77098.0 | 21.1% | 45.6% | 24.6 |
| 762.0 | 772.0 | app2 | True | 48642.0 | 10.5% | 28.8% | 18.3 |
| 762.0 | 772.0 | end-users | True | 43268.0 | 68.4% | 25.6% | -42.8 |
| 772.0 | 782.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 772.0 | 782.0 | app2 | True | 24326.0 | 10.5% | 14.4% | 3.9 |
| 772.0 | 782.0 | end-users | True | 144750.0 | 68.4% | 85.6% | 17.2 |
| 782.0 | 792.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 782.0 | 792.0 | app2 | True | 20248.0 | 10.5% | 13.4% | 2.8 |
| 782.0 | 792.0 | end-users | True | 131296.0 | 68.4% | 86.6% | 18.2 |
| 792.0 | 802.0 | app1 | True | 56912.0 | 21.1% | 33.9% | 12.8 |
| 792.0 | 802.0 | app2 | True | 28470.0 | 10.5% | 17.0% | 6.4 |
| 792.0 | 802.0 | end-users | True | 82530.0 | 68.4% | 49.2% | -19.3 |
| 802.0 | 812.0 | app1 | True | 4074.0 | 21.1% | 2.4% | -18.6 |
| 802.0 | 812.0 | app2 | True | 55438.0 | 10.5% | 32.8% | 22.3 |
| 802.0 | 812.0 | end-users | True | 109496.0 | 68.4% | 64.8% | -3.6 |
| 812.0 | 822.0 | app1 | True | 36542.0 | 21.1% | 23.9% | 2.9 |
| 812.0 | 822.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 812.0 | 822.0 | end-users | True | 116322.0 | 68.4% | 76.1% | 7.7 |
| 822.0 | 832.0 | app1 | True | 2716.0 | 21.1% | 1.6% | -19.4 |
| 822.0 | 832.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 822.0 | 832.0 | end-users | True | 163722.0 | 68.4% | 98.4% | 29.9 |
| 832.0 | 842.0 | app1 | True | 54130.0 | 21.1% | 32.5% | 11.5 |
| 832.0 | 842.0 | app2 | True | 55526.0 | 10.5% | 33.3% | 22.8 |
| 832.0 | 842.0 | end-users | True | 56878.0 | 68.4% | 34.2% | -34.3 |
| 842.0 | 852.0 | app1 | True | 20294.0 | 21.1% | 11.8% | -9.2 |
| 842.0 | 852.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 842.0 | 852.0 | end-users | True | 150230.0 | 68.4% | 87.4% | 19.0 |
| 852.0 | 862.0 | app1 | True | 25664.0 | 21.1% | 17.2% | -3.8 |
| 852.0 | 862.0 | app2 | True | 12208.0 | 10.5% | 8.2% | -2.3 |
| 852.0 | 862.0 | end-users | True | 111036.0 | 68.4% | 74.6% | 6.1 |
| 862.0 | 872.0 | app1 | True | 39326.0 | 21.1% | 23.8% | 2.8 |
| 862.0 | 872.0 | app2 | True | 47322.0 | 10.5% | 28.7% | 18.1 |
| 862.0 | 872.0 | end-users | True | 78486.0 | 68.4% | 47.5% | -20.9 |
| 872.0 | 882.0 | app1 | True | 12196.0 | 21.1% | 7.3% | -13.8 |
| 872.0 | 882.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 872.0 | 882.0 | end-users | True | 155494.0 | 68.4% | 92.7% | 24.3 |
| 882.0 | 892.0 | app1 | True | 43208.0 | 21.1% | 27.6% | 6.5 |
| 882.0 | 892.0 | app2 | True | 29736.0 | 10.5% | 19.0% | 8.4 |
| 882.0 | 892.0 | end-users | True | 83890.0 | 68.4% | 53.5% | -14.9 |
| 892.0 | 902.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 892.0 | 902.0 | app2 | False | 13552.0 | n/a | n/a | n/a |
| 892.0 | 902.0 | end-users | False | 144970.0 | n/a | n/a | n/a |
| 902.0 | 913.0 | app1 | False | 31078.0 | n/a | n/a | n/a |
| 902.0 | 913.0 | app2 | False | 13482.0 | n/a | n/a | n/a |
| 902.0 | 913.0 | end-users | False | 24376.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 790890 | 39456 | 830346.0 | 0.0% | 825116.0 | 869802.0 | -5.1% | True |
| app2 | 2118060 | 105529 | 2223589.0 | 0.0% | 2284396.0 | 2329118.0 | -1.9% | True |
| end-users | 10757580 | 536829 | 11294409.0 | 0.0% | 11778504.0 | 11831238.0 | -0.4% | True |

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
