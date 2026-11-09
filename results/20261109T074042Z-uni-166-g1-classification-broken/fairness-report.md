# Fairness benchmark: misclassified-prefix (uni-166-g1-classification-broken)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `misclassified-prefix` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `420` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-qr7vq` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T07:41:54Z` |
| Run end | `2026-11-09T07:51:24Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 899 | 200=883, 500=16 | 16.3 | 26.6 | 1176646.0 | 21.1% | 17.1% | -3.9 | 17.1% | -4.0 | 15.3s | 98.9% | 880.0 |
| app2 | 10.0 | 32 | 724 | 200=705, 500=19 | 21.7 | 28.3 | 932266.0 | 10.5% | 13.6% | 3.1 | 13.8% | 3.2 | 14.7s | 98.9% | 702.0 |
| end-users | 65.0 | 128 | 3641 | 200=3561, 500=80 | 16.1 | 20.4 | 4755160.0 | 68.4% | 69.3% | 0.9 | 69.2% | 0.7 | 15.2s | 98.9% | 3547.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 317848.0 | n/a | n/a | n/a | n/a | n/a | 15.1s | 98.9% | 237.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-420s, no duty cycle
- app2: active 0s-420s, no duty cycle
- end-users: active 0s-420s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 420.0 | n/a (never converged in this phase) | n/a |

**Windows** (57 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 4056.0 | 21.1% | 14.3% | -6.8 |
| 0.0 | 10.0 | app2 | True | 4064.0 | 10.5% | 14.3% | 3.8 |
| 0.0 | 10.0 | end-users | True | 20276.0 | 68.4% | 71.4% | 3.0 |
| 10.0 | 20.0 | app1 | True | 33840.0 | 21.1% | 16.2% | -4.9 |
| 10.0 | 20.0 | app2 | True | 32420.0 | 10.5% | 15.5% | 5.0 |
| 10.0 | 20.0 | end-users | True | 143216.0 | 68.4% | 68.4% | -0.1 |
| 20.0 | 30.0 | app1 | True | 31194.0 | 21.1% | 19.9% | -1.2 |
| 20.0 | 30.0 | app2 | True | 16278.0 | 10.5% | 10.4% | -0.1 |
| 20.0 | 30.0 | end-users | True | 109292.0 | 68.4% | 69.7% | 1.3 |
| 30.0 | 40.0 | app1 | True | 31126.0 | 21.1% | 20.6% | -0.5 |
| 30.0 | 40.0 | app2 | True | 16238.0 | 10.5% | 10.7% | 0.2 |
| 30.0 | 40.0 | end-users | True | 104036.0 | 68.4% | 68.7% | 0.3 |
| 40.0 | 50.0 | app1 | True | 23010.0 | 21.1% | 14.2% | -6.9 |
| 40.0 | 50.0 | app2 | True | 35142.0 | 10.5% | 21.7% | 11.1 |
| 40.0 | 50.0 | end-users | True | 104008.0 | 68.4% | 64.1% | -4.3 |
| 50.0 | 60.0 | app1 | True | 36468.0 | 21.1% | 22.1% | 1.0 |
| 50.0 | 60.0 | app2 | True | 10812.0 | 10.5% | 6.6% | -4.0 |
| 50.0 | 60.0 | end-users | True | 117742.0 | 68.4% | 71.3% | 2.9 |
| 60.0 | 70.0 | app1 | True | 28398.0 | 21.1% | 18.4% | -2.6 |
| 60.0 | 70.0 | app2 | True | 5426.0 | 10.5% | 3.5% | -7.0 |
| 60.0 | 70.0 | end-users | True | 120192.0 | 68.4% | 78.0% | 9.6 |
| 70.0 | 80.0 | app1 | True | 28426.0 | 21.1% | 17.9% | -3.1 |
| 70.0 | 80.0 | app2 | True | 40564.0 | 10.5% | 25.6% | 15.1 |
| 70.0 | 80.0 | end-users | True | 89396.0 | 68.4% | 56.4% | -12.0 |
| 80.0 | 90.0 | app1 | True | 14916.0 | 21.1% | 8.8% | -12.2 |
| 80.0 | 90.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 80.0 | 90.0 | end-users | True | 154108.0 | 68.4% | 91.2% | 22.8 |
| 90.0 | 100.0 | app1 | True | 43168.0 | 21.1% | 27.1% | 6.0 |
| 90.0 | 100.0 | app2 | True | 47306.0 | 10.5% | 29.7% | 19.1 |
| 90.0 | 100.0 | end-users | True | 68964.0 | 68.4% | 43.3% | -25.2 |
| 100.0 | 110.0 | app1 | True | 31078.0 | 21.1% | 21.9% | 0.8 |
| 100.0 | 110.0 | app2 | True | 10768.0 | 10.5% | 7.6% | -2.9 |
| 100.0 | 110.0 | end-users | True | 100098.0 | 68.4% | 70.5% | 2.1 |
| 110.0 | 120.0 | app1 | True | 2708.0 | 21.1% | 1.6% | -19.5 |
| 110.0 | 120.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 110.0 | 120.0 | end-users | True | 167584.0 | 68.4% | 98.4% | 30.0 |
| 120.0 | 130.0 | app1 | True | 45980.0 | 21.1% | 29.8% | 8.8 |
| 120.0 | 130.0 | app2 | True | 63536.0 | 10.5% | 41.2% | 30.7 |
| 120.0 | 130.0 | end-users | True | 44600.0 | 68.4% | 28.9% | -39.5 |
| 130.0 | 140.0 | app1 | True | 35204.0 | 21.1% | 24.1% | 3.0 |
| 130.0 | 140.0 | app2 | True | 1358.0 | 10.5% | 0.9% | -9.6 |
| 130.0 | 140.0 | end-users | True | 109574.0 | 68.4% | 75.0% | 6.6 |
| 140.0 | 150.0 | app1 | True | 2716.0 | 21.1% | 1.6% | -19.4 |
| 140.0 | 150.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 140.0 | 150.0 | end-users | True | 164884.0 | 68.4% | 98.4% | 30.0 |
| 150.0 | 160.0 | app1 | True | 50114.0 | 21.1% | 32.2% | 11.2 |
| 150.0 | 160.0 | app2 | True | 58180.0 | 10.5% | 37.4% | 26.9 |
| 150.0 | 160.0 | end-users | True | 47210.0 | 68.4% | 30.4% | -38.1 |
| 160.0 | 170.0 | app1 | True | 29696.0 | 21.1% | 20.3% | -0.7 |
| 160.0 | 170.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 160.0 | 170.0 | end-users | True | 116324.0 | 68.4% | 79.7% | 11.2 |
| 170.0 | 180.0 | app1 | True | 4060.0 | 21.1% | 2.4% | -18.7 |
| 170.0 | 180.0 | app2 | True | 4064.0 | 10.5% | 2.4% | -8.1 |
| 170.0 | 180.0 | end-users | True | 162394.0 | 68.4% | 95.2% | 26.8 |
| 180.0 | 190.0 | app1 | True | 52748.0 | 21.1% | 34.8% | 13.8 |
| 180.0 | 190.0 | app2 | True | 55512.0 | 10.5% | 36.6% | 26.1 |
| 180.0 | 190.0 | end-users | True | 43302.0 | 68.4% | 28.6% | -39.9 |
| 190.0 | 200.0 | app1 | True | 21630.0 | 21.1% | 13.1% | -7.9 |
| 190.0 | 200.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 190.0 | 200.0 | end-users | True | 143208.0 | 68.4% | 86.9% | 18.5 |
| 200.0 | 210.0 | app1 | True | 18922.0 | 21.1% | 13.0% | -8.1 |
| 200.0 | 210.0 | app2 | True | 10818.0 | 10.5% | 7.4% | -3.1 |
| 200.0 | 210.0 | end-users | True | 116260.0 | 68.4% | 79.6% | 11.2 |
| 210.0 | 220.0 | app1 | True | 54124.0 | 21.1% | 33.6% | 12.6 |
| 210.0 | 220.0 | app2 | True | 48704.0 | 10.5% | 30.3% | 19.7 |
| 210.0 | 220.0 | end-users | True | 58108.0 | 68.4% | 36.1% | -32.3 |
| 220.0 | 230.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 220.0 | 230.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 220.0 | 230.0 | end-users | True | 163690.0 | 68.4% | 100.0% | 31.6 |
| 230.0 | 240.0 | app1 | True | 41878.0 | 21.1% | 27.2% | 6.1 |
| 230.0 | 240.0 | app2 | True | 31130.0 | 10.5% | 20.2% | 9.7 |
| 230.0 | 240.0 | end-users | True | 81204.0 | 68.4% | 52.7% | -15.8 |
| 240.0 | 250.0 | app1 | True | 29688.0 | 21.1% | 19.6% | -1.4 |
| 240.0 | 250.0 | app2 | True | 27064.0 | 10.5% | 17.9% | 7.3 |
| 240.0 | 250.0 | end-users | True | 94688.0 | 68.4% | 62.5% | -5.9 |
| 250.0 | 260.0 | app1 | True | 4060.0 | 21.1% | 2.5% | -18.6 |
| 250.0 | 260.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 250.0 | 260.0 | end-users | True | 159574.0 | 68.4% | 97.5% | 29.1 |
| 260.0 | 270.0 | app1 | True | 44652.0 | 21.1% | 27.7% | 6.7 |
| 260.0 | 270.0 | app2 | True | 56822.0 | 10.5% | 35.3% | 24.8 |
| 260.0 | 270.0 | end-users | True | 59504.0 | 68.4% | 37.0% | -31.5 |
| 270.0 | 280.0 | app1 | True | 29838.0 | 21.1% | 20.8% | -0.3 |
| 270.0 | 280.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 270.0 | 280.0 | end-users | True | 113614.0 | 68.4% | 79.2% | 10.8 |
| 280.0 | 291.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 280.0 | 291.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 280.0 | 291.0 | end-users | True | 167724.0 | 68.4% | 100.0% | 31.6 |
| 291.0 | 301.0 | app1 | True | 72942.0 | 21.1% | 46.6% | 25.5 |
| 291.0 | 301.0 | app2 | True | 58210.0 | 10.5% | 37.1% | 26.6 |
| 291.0 | 301.0 | end-users | True | 25542.0 | 68.4% | 16.3% | -52.1 |
| 301.0 | 311.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.2 |
| 301.0 | 311.0 | app2 | True | 1354.0 | 10.5% | 0.8% | -9.7 |
| 301.0 | 311.0 | end-users | True | 160922.0 | 68.4% | 98.3% | 29.9 |
| 311.0 | 321.0 | app1 | True | 13560.0 | 21.1% | 9.1% | -11.9 |
| 311.0 | 321.0 | app2 | True | 6770.0 | 10.5% | 4.6% | -6.0 |
| 311.0 | 321.0 | end-users | True | 128412.0 | 68.4% | 86.3% | 17.9 |
| 321.0 | 331.0 | app1 | True | 48668.0 | 21.1% | 30.5% | 9.4 |
| 321.0 | 331.0 | app2 | True | 51486.0 | 10.5% | 32.2% | 21.7 |
| 321.0 | 331.0 | end-users | True | 59586.0 | 68.4% | 37.3% | -31.1 |
| 331.0 | 341.0 | app1 | True | 13498.0 | 21.1% | 8.2% | -12.9 |
| 331.0 | 341.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 331.0 | 341.0 | end-users | True | 151540.0 | 68.4% | 91.8% | 23.4 |
| 341.0 | 351.0 | app1 | True | 33768.0 | 21.1% | 23.6% | 2.5 |
| 341.0 | 351.0 | app2 | True | 17592.0 | 10.5% | 12.3% | 1.8 |
| 341.0 | 351.0 | end-users | True | 91892.0 | 68.4% | 64.1% | -4.3 |
| 351.0 | 361.0 | app1 | True | 9478.0 | 21.1% | 5.5% | -15.5 |
| 351.0 | 361.0 | app2 | True | 28440.0 | 10.5% | 16.6% | 6.0 |
| 351.0 | 361.0 | end-users | True | 133860.0 | 68.4% | 77.9% | 9.5 |
| 361.0 | 371.0 | app1 | True | 48702.0 | 21.1% | 31.9% | 10.8 |
| 361.0 | 371.0 | app2 | True | 21668.0 | 10.5% | 14.2% | 3.6 |
| 361.0 | 371.0 | end-users | True | 82530.0 | 68.4% | 54.0% | -14.4 |
| 371.0 | 381.0 | app1 | True | 10810.0 | 21.1% | 6.6% | -14.5 |
| 371.0 | 381.0 | app2 | True | 20284.0 | 10.5% | 12.3% | 1.8 |
| 371.0 | 381.0 | end-users | True | 133818.0 | 68.4% | 81.1% | 12.7 |
| 381.0 | 391.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 381.0 | 391.0 | app2 | True | 21660.0 | 10.5% | 13.7% | 3.2 |
| 381.0 | 391.0 | end-users | True | 136490.0 | 68.4% | 86.3% | 17.9 |
| 391.0 | 401.0 | app1 | True | 55464.0 | 21.1% | 35.3% | 14.3 |
| 391.0 | 401.0 | app2 | True | 29720.0 | 10.5% | 18.9% | 8.4 |
| 391.0 | 401.0 | end-users | True | 71780.0 | 68.4% | 45.7% | -22.7 |
| 401.0 | 411.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.2 |
| 401.0 | 411.0 | app2 | True | 21688.0 | 10.5% | 12.8% | 2.3 |
| 401.0 | 411.0 | end-users | True | 145962.0 | 68.4% | 86.4% | 17.9 |
| 411.0 | 421.0 | app1 | True | 2684.0 | 21.1% | 1.8% | -19.3 |
| 411.0 | 421.0 | app2 | True | 33884.0 | 10.5% | 22.6% | 12.0 |
| 411.0 | 421.0 | end-users | True | 113594.0 | 68.4% | 75.6% | 7.2 |
| 421.0 | 431.0 | app1 | False | 56858.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | False | 13496.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | end-users | False | 87810.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | False | 33800.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | False | 29808.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | end-users | False | 86648.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 501.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 511.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 511.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 511.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 511.0 | 521.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 511.0 | 521.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 511.0 | 521.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 521.0 | 531.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 521.0 | 531.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 521.0 | 531.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 531.0 | 541.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 531.0 | 541.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 531.0 | 541.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 541.0 | 551.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 541.0 | 551.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 541.0 | 551.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 551.0 | 561.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 551.0 | 561.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 551.0 | 561.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 561.0 | 570.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 561.0 | 570.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 561.0 | 570.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 15 | 0ms | 1375ms | 2387ms |
| 0.0 | 10.0 | app2 | ok | 12 | 200ms | 1900ms | 2440ms |
| 0.0 | 10.0 | end-users | ok | 53 | 8ms | 850ms | 2341ms |
| 10.0 | 20.0 | app1 | ok | 44 | 1326ms | 2474ms | 4725ms |
| 10.0 | 20.0 | app2 | ok | 31 | 1469ms | 4225ms | 4922ms |
| 10.0 | 20.0 | end-users | ok | 163 | 1350ms | 3302ms | 4830ms |
| 20.0 | 30.0 | app1 | ok | 29 | 6944ms | 23556ms | 29356ms |
| 20.0 | 30.0 | app2 | ok | 18 | 19412ms | 27882ms | 29788ms |
| 20.0 | 30.0 | end-users | ok | 119 | 7067ms | 21793ms | 29179ms |
| 30.0 | 40.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 31 | 7708ms | 23800ms | 29380ms |
| 40.0 | 50.0 | app2 | ok | 29 | 12941ms | 26588ms | 29659ms |
| 40.0 | 50.0 | end-users | ok | 102 | 8158ms | 24486ms | 29449ms |
| 50.0 | 60.0 | app1 | ok | 30 | 6250ms | 20000ms | 29000ms |
| 50.0 | 60.0 | app2 | ok | 15 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | end-users | ok | 116 | 7838ms | 24476ms | 29448ms |
| 60.0 | 70.0 | app1 | ok | 32 | 8077ms | 24182ms | 29418ms |
| 60.0 | 70.0 | app2 | ok | 20 | 18235ms | 27647ms | 29765ms |
| 60.0 | 70.0 | end-users | ok | 118 | 7553ms | 23444ms | 29344ms |
| 70.0 | 80.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 32 | 6250ms | 20857ms | 29086ms |
| 80.0 | 90.0 | app2 | ok | 20 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | end-users | ok | 114 | 6538ms | 22400ms | 29240ms |
| 90.0 | 100.0 | app1 | ok | 25 | 1825ms | 4219ms | 4922ms |
| 90.0 | 100.0 | app2 | ok | 24 | 5000ms | 26000ms | 29600ms |
| 90.0 | 100.0 | end-users | ok | 111 | 10179ms | 26036ms | 29604ms |
| 100.0 | 110.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 100.0 | 110.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 100.0 | 110.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 32 | 7692ms | 23600ms | 29360ms |
| 110.0 | 120.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | end-users | ok | 114 | 6190ms | 20880ms | 29088ms |
| 120.0 | 130.0 | app1 | ok | 30 | 2350ms | 4464ms | 4946ms |
| 120.0 | 130.0 | app2 | ok | 17 | 2050ms | 4393ms | 4939ms |
| 120.0 | 130.0 | end-users | ok | 117 | 13286ms | 26657ms | 29666ms |
| 130.0 | 140.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 130.0 | 140.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 130.0 | 140.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 32 | 7083ms | 22889ms | 29289ms |
| 140.0 | 150.0 | app2 | ok | 22 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | end-users | ok | 114 | 6585ms | 22138ms | 29214ms |
| 150.0 | 160.0 | app1 | ok | 27 | 1750ms | 4156ms | 4916ms |
| 150.0 | 160.0 | app2 | ok | 22 | 4583ms | 25600ms | 29560ms |
| 150.0 | 160.0 | end-users | ok | 111 | 11803ms | 26361ms | 29636ms |
| 160.0 | 170.0 | app1 | ok | 32 | 7143ms | 22000ms | 29200ms |
| 160.0 | 170.0 | app2 | ok | 22 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | end-users | ok | 111 | 6346ms | 21778ms | 29178ms |
| 170.0 | 180.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 170.0 | 180.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 170.0 | 180.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 180.0 | 190.0 | app1 | ok | 26 | 1818ms | 4188ms | 4919ms |
| 180.0 | 190.0 | app2 | ok | 23 | 4250ms | 25400ms | 29540ms |
| 180.0 | 190.0 | end-users | ok | 114 | 10678ms | 26136ms | 29614ms |
| 190.0 | 200.0 | app1 | ok | 31 | 7885ms | 23800ms | 29380ms |
| 190.0 | 200.0 | app2 | ok | 17 | 20000ms | 28000ms | 29800ms |
| 190.0 | 200.0 | end-users | ok | 112 | 6250ms | 21385ms | 29138ms |
| 200.0 | 210.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 200.0 | 210.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 200.0 | 210.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 210.0 | 220.0 | app1 | ok | 23 | 1656ms | 4458ms | 25400ms |
| 210.0 | 220.0 | app2 | ok | 27 | 12000ms | 26400ms | 29640ms |
| 210.0 | 220.0 | end-users | ok | 113 | 9619ms | 25654ms | 29565ms |
| 220.0 | 230.0 | app1 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 220.0 | 230.0 | app2 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 220.0 | 230.0 | end-users | ok | 111 | 5179ms | 15200ms | 28520ms |
| 230.0 | 240.0 | app1 | ok | 24 | 1600ms | 4000ms | 4900ms |
| 230.0 | 240.0 | app2 | ok | 26 | 11429ms | 26286ms | 29629ms |
| 230.0 | 240.0 | end-users | ok | 115 | 9955ms | 25965ms | 29596ms |
| 240.0 | 250.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | ok | 31 | 8654ms | 24833ms | 29483ms |
| 250.0 | 260.0 | app2 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 250.0 | 260.0 | end-users | ok | 114 | 5833ms | 19636ms | 28964ms |
| 260.0 | 270.0 | app1 | ok | 24 | 1833ms | 4500ms | 25200ms |
| 260.0 | 270.0 | app2 | ok | 25 | 12143ms | 26429ms | 29643ms |
| 260.0 | 270.0 | end-users | ok | 111 | 9868ms | 25889ms | 29589ms |
| 270.0 | 280.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 280.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 280.0 | 291.0 | app1 | ok | 32 | 8333ms | 24667ms | 29467ms |
| 280.0 | 291.0 | app2 | ok | 16 | 20000ms | 28000ms | 29800ms |
| 280.0 | 291.0 | end-users | ok | 113 | 6193ms | 20174ms | 29017ms |
| 291.0 | 301.0 | app1 | ok | 23 | 1583ms | 4042ms | 4904ms |
| 291.0 | 301.0 | app2 | ok | 28 | 12500ms | 26500ms | 29650ms |
| 291.0 | 301.0 | end-users | ok | 111 | 9955ms | 25964ms | 29596ms |
| 301.0 | 311.0 | app1 | ok | 32 | 19677ms | 27935ms | 29794ms |
| 301.0 | 311.0 | app2 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 301.0 | 311.0 | end-users | ok | 111 | 5188ms | 16941ms | 28694ms |
| 311.0 | 321.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | ok | 24 | 1545ms | 3800ms | 4880ms |
| 321.0 | 331.0 | app2 | ok | 26 | 11429ms | 26286ms | 29629ms |
| 321.0 | 331.0 | end-users | ok | 114 | 10000ms | 26000ms | 29600ms |
| 331.0 | 341.0 | app1 | ok | 32 | 8333ms | 24667ms | 29467ms |
| 331.0 | 341.0 | app2 | ok | 20 | 20000ms | 28000ms | 29800ms |
| 331.0 | 341.0 | end-users | ok | 112 | 6000ms | 20667ms | 29067ms |
| 341.0 | 351.0 | app1 | ok | 25 | 1975ms | 4306ms | 4931ms |
| 341.0 | 351.0 | app2 | ok | 25 | 4688ms | 25833ms | 29583ms |
| 341.0 | 351.0 | end-users | ok | 127 | 9342ms | 25464ms | 29546ms |
| 351.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | ok | 19 | 958ms | 24571ms | 29457ms |
| 361.0 | 371.0 | app2 | ok | 20 | 15714ms | 27143ms | 29714ms |
| 361.0 | 371.0 | end-users | ok | 126 | 8673ms | 24960ms | 29496ms |
| 371.0 | 381.0 | app1 | ok | 22 | 19524ms | 27905ms | 29790ms |
| 371.0 | 381.0 | app2 | ok | 30 | 11250ms | 26250ms | 29625ms |
| 371.0 | 381.0 | end-users | ok | 114 | 5897ms | 20880ms | 29088ms |
| 381.0 | 391.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | ok | 20 | 1000ms | 26000ms | 29600ms |
| 391.0 | 401.0 | app2 | ok | 19 | 8438ms | 24571ms | 29457ms |
| 391.0 | 401.0 | end-users | ok | 123 | 8827ms | 25080ms | 29508ms |
| 401.0 | 411.0 | app1 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 401.0 | 411.0 | app2 | ok | 30 | 10000ms | 26000ms | 29600ms |
| 401.0 | 411.0 | end-users | ok | 115 | 5469ms | 13571ms | 28357ms |
| 411.0 | 421.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | ok | 21 | 950ms | 24750ms | 29475ms |
| 421.0 | 431.0 | app2 | ok | 20 | 9286ms | 25556ms | 29556ms |
| 421.0 | 431.0 | end-users | ok | 126 | 9062ms | 25333ms | 29533ms |
| 431.0 | 441.0 | app1 | ok | 24 | 20000ms | 28000ms | 29800ms |
| 431.0 | 441.0 | app2 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 431.0 | 441.0 | end-users | ok | 2 | 20000ms | 28000ms | 29800ms |
| 441.0 | 451.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 501.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 501.0 | 511.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 501.0 | 511.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 501.0 | 511.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 511.0 | 521.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 511.0 | 521.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 511.0 | 521.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 521.0 | 531.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 521.0 | 531.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 521.0 | 531.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 531.0 | 541.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 531.0 | 541.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 531.0 | 541.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 541.0 | 551.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 541.0 | 551.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 541.0 | 551.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 551.0 | 561.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 551.0 | 561.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 551.0 | 561.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 561.0 | 570.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 561.0 | 570.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 561.0 | 570.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1086090 | 54043 | 1136266.0 | -0.3% | 1176646.0 | 1194176.0 | -1.5% | True |
| app2 | 867150 | 43373 | 906656.0 | -0.4% | 932266.0 | 953896.0 | -2.3% | True |
| end-users | 4380030 | 217307 | 4579262.0 | -0.4% | 4755160.0 | 4814644.0 | -1.2% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 899 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 724 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3641 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5366). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 547493 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
