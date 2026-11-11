# Fairness benchmark: app1-flood (uni-220-diag-clamp-off-app1-flood)

**Verdict: FAIL** (threshold: 10 points)
**Secondary (priority) verdict: PRIORITY-FAIL** -- see "Per-tenant TTFT / ITL and the priority verdict (UNI-226)" below for detail.
Worker-share vs. weight-share gap (UNI-225): 42.7 points

- end-users deviated -12.9 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-flood` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-74bd76b5d4-ltwdt` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-11T10:03:59Z` |
| Run end | `2026-11-11T10:13:05Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 30.0 | 256 | 3256 | 000=2, 200=2761, 500=493 | 12.6 | 33.8 | 1945376.0 | 30.0% | 72.7% | 42.7 | 40.5% | 10.5 | 54.2% | 24.2 | 37.2s | 98.9% | 1587.0 |
| app2 | 10.0 | 32 | 656 | 000=1, 200=590, 500=65 | 11.0 | 15.7 | 596688.0 | 10.0% | 9.1% | -0.9 | 12.4% | 2.4 | 10.9% | 0.9 | 37.2s | 98.9% | 442.0 |
| end-users | 60.0 | 64 | 2095 | 200=1991, 500=104 | 5.9 | 12.0 | 2259564.0 | 60.0% | 18.2% | -41.8 | 47.1% | -12.9 | 34.9% | -25.1 | 35.8s | 98.9% | 1677.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 1358.0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.0s | 98.9% | 1.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events (scheduled):**
- t+0s: live_set (target=epp-key:newcomerClamp, value=false)
- t+240s: live_restore (target=epp-key:newcomerClamp)

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (55 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 0.0 | 10.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 10.0 | 20.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 10.0 | 20.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 10.0 | 20.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 20.0 | 30.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 20.0 | 30.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 20.0 | 30.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 30.0 | 40.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 30.0 | 40.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 30.0 | 40.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 40.0 | 50.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 40.0 | 50.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 40.0 | 50.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 50.0 | 60.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 50.0 | 60.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 50.0 | 60.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 60.0 | 70.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 60.0 | 70.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 60.0 | 70.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 70.0 | 80.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 70.0 | 80.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 70.0 | 80.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 80.0 | 90.0 | app1 | True | 100024.0 | 30.0% | 38.1% | 8.1 |
| 80.0 | 90.0 | app2 | True | 35178.0 | 10.0% | 13.4% | 3.4 |
| 80.0 | 90.0 | end-users | True | 127018.0 | 60.0% | 48.4% | -11.6 |
| 90.0 | 100.0 | app1 | True | 100100.0 | 30.0% | 35.2% | 5.2 |
| 90.0 | 100.0 | app2 | True | 32390.0 | 10.0% | 11.4% | 1.4 |
| 90.0 | 100.0 | end-users | True | 151504.0 | 60.0% | 53.3% | -6.7 |
| 100.0 | 110.0 | app1 | True | 93314.0 | 30.0% | 38.3% | 8.3 |
| 100.0 | 110.0 | app2 | True | 31164.0 | 10.0% | 12.8% | 2.8 |
| 100.0 | 110.0 | end-users | True | 118992.0 | 60.0% | 48.9% | -11.1 |
| 110.0 | 120.0 | app1 | True | 114980.0 | 30.0% | 46.2% | 16.2 |
| 110.0 | 120.0 | app2 | True | 37956.0 | 10.0% | 15.2% | 5.2 |
| 110.0 | 120.0 | end-users | True | 95984.0 | 60.0% | 38.6% | -21.4 |
| 120.0 | 130.0 | app1 | True | 118974.0 | 30.0% | 38.9% | 8.9 |
| 120.0 | 130.0 | app2 | True | 39188.0 | 10.0% | 12.8% | 2.8 |
| 120.0 | 130.0 | end-users | True | 147432.0 | 60.0% | 48.2% | -11.8 |
| 130.0 | 140.0 | app1 | True | 91892.0 | 30.0% | 30.2% | 0.2 |
| 130.0 | 140.0 | app2 | True | 29778.0 | 10.0% | 9.8% | -0.2 |
| 130.0 | 140.0 | end-users | True | 182636.0 | 60.0% | 60.0% | 0.0 |
| 140.0 | 150.0 | app1 | True | 121710.0 | 30.0% | 39.8% | 9.8 |
| 140.0 | 150.0 | app2 | True | 40572.0 | 10.0% | 13.3% | 3.3 |
| 140.0 | 150.0 | end-users | True | 143292.0 | 60.0% | 46.9% | -13.1 |
| 150.0 | 160.0 | app1 | True | 101344.0 | 30.0% | 33.0% | 3.0 |
| 150.0 | 160.0 | app2 | True | 32454.0 | 10.0% | 10.6% | 0.6 |
| 150.0 | 160.0 | end-users | True | 173118.0 | 60.0% | 56.4% | -3.6 |
| 160.0 | 170.0 | app1 | True | 97406.0 | 30.0% | 31.9% | 1.9 |
| 160.0 | 170.0 | app2 | True | 32464.0 | 10.0% | 10.6% | 0.6 |
| 160.0 | 170.0 | end-users | True | 175634.0 | 60.0% | 57.5% | -2.5 |
| 170.0 | 180.0 | app1 | True | 104002.0 | 30.0% | 33.9% | 3.9 |
| 170.0 | 180.0 | app2 | True | 37864.0 | 10.0% | 12.3% | 2.3 |
| 170.0 | 180.0 | end-users | True | 165004.0 | 60.0% | 53.8% | -6.2 |
| 180.0 | 190.0 | app1 | True | 98640.0 | 30.0% | 32.0% | 2.0 |
| 180.0 | 190.0 | app2 | True | 29718.0 | 10.0% | 9.6% | -0.4 |
| 180.0 | 190.0 | end-users | True | 179864.0 | 60.0% | 58.4% | -1.6 |
| 190.0 | 201.0 | app1 | True | 104116.0 | 30.0% | 34.4% | 4.4 |
| 190.0 | 201.0 | app2 | True | 36566.0 | 10.0% | 12.1% | 2.1 |
| 190.0 | 201.0 | end-users | True | 162332.0 | 60.0% | 53.6% | -6.4 |
| 201.0 | 211.0 | app1 | True | 132494.0 | 30.0% | 48.0% | 18.0 |
| 201.0 | 211.0 | app2 | True | 43298.0 | 10.0% | 15.7% | 5.7 |
| 201.0 | 211.0 | end-users | True | 100052.0 | 60.0% | 36.3% | -23.7 |
| 211.0 | 221.0 | app1 | True | 143264.0 | 30.0% | 92.2% | 62.2 |
| 211.0 | 221.0 | app2 | True | 12188.0 | 10.0% | 7.8% | -2.2 |
| 211.0 | 221.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 221.0 | 231.0 | app1 | True | 112092.0 | 30.0% | 45.0% | 15.0 |
| 221.0 | 231.0 | app2 | True | 41978.0 | 10.0% | 16.9% | 6.9 |
| 221.0 | 231.0 | end-users | True | 94776.0 | 60.0% | 38.1% | -21.9 |
| 231.0 | 241.0 | app1 | True | 119032.0 | 30.0% | 43.4% | 13.4 |
| 231.0 | 241.0 | app2 | True | 37812.0 | 10.0% | 13.8% | 3.8 |
| 231.0 | 241.0 | end-users | True | 117562.0 | 60.0% | 42.8% | -17.2 |
| 241.0 | 251.0 | app1 | False | 118918.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 35272.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 106764.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 73074.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 10848.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 17600.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 452.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 452.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 452.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 512.0 | 522.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 522.0 | 532.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 532.0 | 542.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 542.0 | 546.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 20.0 | 30.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 20.0 | 30.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 30.0 | 40.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 30.0 | 40.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 40.0 | 50.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 40.0 | 50.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 50.0 | 60.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 50.0 | 60.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 60.0 | 70.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 60.0 | 70.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 70.0 | 80.0 | app2 | ok | 9 | 7500ms | 9500ms | 9950ms |
| 70.0 | 80.0 | end-users | ok | 50 | 5536ms | 9107ms | 9911ms |
| 80.0 | 90.0 | app1 | ok | 101 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app2 | ok | 33 | 6250ms | 19000ms | 28900ms |
| 80.0 | 90.0 | end-users | ok | 104 | 1909ms | 4333ms | 4933ms |
| 90.0 | 100.0 | app1 | ok | 81 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app2 | ok | 25 | 6094ms | 9219ms | 9922ms |
| 90.0 | 100.0 | end-users | ok | 78 | 969ms | 2192ms | 2469ms |
| 100.0 | 110.0 | app1 | ok | 89 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app2 | ok | 17 | 6458ms | 9292ms | 9929ms |
| 100.0 | 110.0 | end-users | ok | 63 | 3350ms | 7900ms | 9790ms |
| 110.0 | 120.0 | app1 | ok | 96 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app2 | ok | 45 | 3281ms | 8676ms | 9868ms |
| 110.0 | 120.0 | end-users | ok | 128 | 4682ms | 8877ms | 9888ms |
| 120.0 | 130.0 | app1 | ok | 52 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app2 | ok | 18 | 5909ms | 9182ms | 9918ms |
| 120.0 | 130.0 | end-users | ok | 116 | 1702ms | 4121ms | 4912ms |
| 130.0 | 140.0 | app1 | ok | 58 | 20000ms | 28000ms | 29800ms |
| 130.0 | 140.0 | app2 | ok | 19 | 7361ms | 9472ms | 9947ms |
| 130.0 | 140.0 | end-users | ok | 93 | 950ms | 2183ms | 2468ms |
| 140.0 | 150.0 | app1 | ok | 83 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app2 | ok | 27 | 7065ms | 9413ms | 9941ms |
| 140.0 | 150.0 | end-users | ok | 144 | 1500ms | 3200ms | 4820ms |
| 150.0 | 160.0 | app1 | ok | 72 | 20435ms | 28783ms | 52800ms |
| 150.0 | 160.0 | app2 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 150.0 | 160.0 | end-users | ok | 125 | 1080ms | 2216ms | 2472ms |
| 160.0 | 170.0 | app1 | ok | 87 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | app2 | ok | 28 | 7083ms | 9417ms | 9942ms |
| 160.0 | 170.0 | end-users | ok | 134 | 1450ms | 3139ms | 4814ms |
| 170.0 | 180.0 | app1 | ok | 85 | 20241ms | 28434ms | 47250ms |
| 170.0 | 180.0 | app2 | ok | 29 | 7100ms | 9420ms | 9942ms |
| 170.0 | 180.0 | end-users | ok | 123 | 1059ms | 2212ms | 2471ms |
| 180.0 | 190.0 | app1 | ok | 57 | 20000ms | 28000ms | 29800ms |
| 180.0 | 190.0 | app2 | ok | 19 | 7361ms | 9472ms | 9947ms |
| 180.0 | 190.0 | end-users | ok | 123 | 898ms | 2635ms | 4763ms |
| 190.0 | 201.0 | app1 | ok | 97 | 20000ms | 28000ms | 29800ms |
| 190.0 | 201.0 | app2 | ok | 37 | 6146ms | 9229ms | 9923ms |
| 190.0 | 201.0 | end-users | ok | 122 | 1407ms | 2453ms | 4695ms |
| 201.0 | 211.0 | app1 | ok | 218 | 15563ms | 27113ms | 29711ms |
| 201.0 | 211.0 | app2 | ok | 18 | 2250ms | 8714ms | 9871ms |
| 201.0 | 211.0 | end-users | ok | 21 | 2614ms | 4523ms | 4952ms |
| 211.0 | 221.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 211.0 | 221.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 211.0 | 221.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 132 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app2 | ok | 59 | 4375ms | 24870ms | 29487ms |
| 221.0 | 231.0 | end-users | ok | 128 | 10000ms | 26000ms | 29600ms |
| 231.0 | 241.0 | app1 | ok | 71 | 20000ms | 28000ms | 29800ms |
| 231.0 | 241.0 | app2 | ok | 27 | 1288ms | 5500ms | 9550ms |
| 231.0 | 241.0 | end-users | ok | 64 | 4722ms | 8897ms | 9890ms |
| 241.0 | 251.0 | app1 | ok | 99 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | app2 | ok | 7 | 5625ms | 9125ms | 9912ms |
| 241.0 | 251.0 | end-users | ok | 61 | 5643ms | 9129ms | 9913ms |
| 251.0 | 261.0 | app1 | ok | 84 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 452.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 452.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 452.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 522.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 522.0 | 532.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 542.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 532.0 | 542.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 542.0 | 546.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 542.0 | 546.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens -42.6%, cost -47.9%
- app2 exceeded the 10% ledger tolerance: raw tokens -25.2%, cost -25.2%
- end-users exceeded the 10% ledger tolerance: raw tokens -15.8%, cost -16.1%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 3396030 | 168885 | 2046202.0 | -42.6% | 1945376.0 | 3733800.0 | -47.9% | False |
| app2 | 725700 | 36226 | 569559.0 | -25.2% | 596688.0 | 798152.0 | -25.2% | False |
| end-users | 2448930 | 121515 | 2165196.0 | -15.8% | 2259564.0 | 2691960.0 | -16.1% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 3256 | 0 | 0 | 0 (never shed) | 0.00% | 30.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 656 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2095 | 0 | 0 | 0 (never shed) | 0.00% | 60.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=3707). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 3707 | 0.051ms | 0.141ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 434125 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1585 | 31598ms | 43660ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 441 | 12273ms | 18742ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 1677 | 5877ms | 13015ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 3704 | 12744ms | 41868ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: PRIORITY-FAIL** -- the share verdict above is FAIL, so this is the board's second, independent success criterion (2026-11-10): did the policy nonetheless order tenants by weight? Top-weighted group: `end-users` (TTFT p50 5877ms, p95 13015ms, strictly lowest among distinctly-weighted groups: p50=True/p95=True; no rank inversion among any distinctly-weighted pair: False -- this, not raw rank correlation, is what gates the verdict, since a genuine weight tie (e.g. 98/1/1's app2==end-users) makes exact correlation 1.0 unreachable by construction even when ordering is otherwise perfect). Rank correlation 0.50 (1.00 = exact agreement, informational only) shown for reference. Separation from the next distinctly-weighted group: 6396ms against a noise floor of not given (separation check skipped).

**Windowed TTFT/ITL** (55 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 16652ms | 19665ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 12955ms | 18375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 10104ms | 14510ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 23833ms | 29383ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 12273ms | 14727ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 5547ms | 7703ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 28214ms | 43083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 13026ms | 18562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 7187ms | 9469ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 8875ms | 9888ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 10972ms | 14597ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 6088ms | 7809ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 36356ms | 44136ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 5023ms | 5973ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | end-users | ok | 4923ms | 7337ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | end-users | ok | 5200ms | 7680ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | end-users | ok | 4954ms | 6818ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | end-users | ok | 5432ms | 7661ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | end-users | ok | 4827ms | 7507ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 201.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 201.0 | app2 | ok | 12875ms | 18650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 201.0 | end-users | ok | 5583ms | 7733ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 36037ms | 44104ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 11818ms | 16000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 6103ms | 7810ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 27681ms | 42851ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 11250ms | 14625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 19500ms | 28893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 17188ms | 19719ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 8240ms | 9824ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 26471ms | 41700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 8571ms | 16750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 8904ms | 9890ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 23440ms | 39210ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 11000ms | 14600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 9000ms | 9900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 431.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 431.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 431.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 431.0 | 441.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 431.0 | 441.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 431.0 | 441.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 441.0 | 452.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 441.0 | 452.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 441.0 | 452.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 522.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 522.0 | 532.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 532.0 | 542.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 546.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 546.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 542.0 | 546.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
