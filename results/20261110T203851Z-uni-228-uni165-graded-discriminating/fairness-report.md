# Fairness benchmark: uni165-graded-discriminating (uni-228-uni165-graded-discriminating)

**Verdict: FAIL** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 33.7 points

- app6 deviated +10.8 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `uni165-graded-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-778f74c767-7fk9q` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-10T20:40:03Z` |
| Run end | `2026-11-10T20:48:15Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 40.0 | 75 | 1847 | 000=7, 200=1804, 500=36 | 8.5 | 15.3 | 2357370.0 | 40.0% | 22.7% | -17.3 | 34.7% | -5.3 | 33.7% | -6.3 | 61.5s | 98.9% | 1808.0 |
| app2 | 20.0 | 32 | 665 | 200=652, 500=13 | 10.3 | 20.2 | 834620.0 | 20.0% | 9.7% | -10.3 | 12.3% | -7.7 | 12.1% | -7.9 | 59.1s | 98.9% | 649.0 |
| app3 | 15.0 | 32 | 746 | 000=1, 200=734, 500=11 | 9.4 | 16.9 | 950900.0 | 15.0% | 9.7% | -5.3 | 14.0% | -1.0 | 13.6% | -1.4 | 60.5s | 98.9% | 735.0 |
| app4 | 10.0 | 32 | 628 | 200=617, 500=11 | 11.6 | 19.7 | 793734.0 | 10.0% | 9.7% | -0.3 | 11.7% | 1.7 | 11.5% | 1.5 | 60.5s | 98.9% | 616.0 |
| app5 | 10.0 | 32 | 620 | 200=610, 500=10 | 11.9 | 20.0 | 780234.0 | 10.0% | 9.7% | -0.3 | 11.5% | 1.5 | 11.3% | 1.3 | 60.5s | 98.9% | 608.0 |
| app6 | 5.0 | 128 | 968 | 000=1, 200=910, 500=57 | 26.5 | 65.7 | 1073248.0 | 5.0% | 38.7% | 33.7 | 15.8% | 10.8 | 17.7% | 12.7 | 61.9s | 98.9% | 903.0 |
| end-users | n/a | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 8074.0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 17.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- app6: active 0s-240s, no duty cycle
- app3: active 0s-240s, no duty cycle
- app5: active 0s-240s, no duty cycle
- app4: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (50 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 0.0 | 10.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 0.0 | 10.0 | app6 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app3 | True | 0.0 | 15.0% | 0.0% | -15.0 |
| 0.0 | 10.0 | app5 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 0.0 | 10.0 | app4 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 10.0 | 20.0 | app1 | True | 12182.0 | 40.0% | 22.5% | -17.5 |
| 10.0 | 20.0 | app2 | True | 2716.0 | 20.0% | 5.0% | -15.0 |
| 10.0 | 20.0 | app6 | True | 22954.0 | 5.0% | 42.4% | 37.4 |
| 10.0 | 20.0 | app3 | True | 6790.0 | 15.0% | 12.5% | -2.5 |
| 10.0 | 20.0 | app5 | True | 1358.0 | 10.0% | 2.5% | -7.5 |
| 10.0 | 20.0 | app4 | True | 8128.0 | 10.0% | 15.0% | 5.0 |
| 20.0 | 30.0 | app1 | True | 78472.0 | 40.0% | 27.9% | -12.1 |
| 20.0 | 30.0 | app2 | True | 29756.0 | 20.0% | 10.6% | -9.4 |
| 20.0 | 30.0 | app6 | True | 86654.0 | 5.0% | 30.8% | 25.8 |
| 20.0 | 30.0 | app3 | True | 27092.0 | 15.0% | 9.6% | -5.4 |
| 20.0 | 30.0 | app5 | True | 29792.0 | 10.0% | 10.6% | 0.6 |
| 20.0 | 30.0 | app4 | True | 29746.0 | 10.0% | 10.6% | 0.6 |
| 30.0 | 40.0 | app1 | True | 112330.0 | 40.0% | 36.7% | -3.3 |
| 30.0 | 40.0 | app2 | True | 56844.0 | 20.0% | 18.6% | -1.4 |
| 30.0 | 40.0 | app6 | True | 31158.0 | 5.0% | 10.2% | 5.2 |
| 30.0 | 40.0 | app3 | True | 43272.0 | 15.0% | 14.1% | -0.9 |
| 30.0 | 40.0 | app5 | True | 31108.0 | 10.0% | 10.2% | 0.2 |
| 30.0 | 40.0 | app4 | True | 31108.0 | 10.0% | 10.2% | 0.2 |
| 40.0 | 50.0 | app1 | True | 124570.0 | 40.0% | 41.1% | 1.1 |
| 40.0 | 50.0 | app2 | True | 60892.0 | 20.0% | 20.1% | 0.1 |
| 40.0 | 50.0 | app6 | True | 14922.0 | 5.0% | 4.9% | -0.1 |
| 40.0 | 50.0 | app3 | True | 43268.0 | 15.0% | 14.3% | -0.7 |
| 40.0 | 50.0 | app5 | True | 29740.0 | 10.0% | 9.8% | -0.2 |
| 40.0 | 50.0 | app4 | True | 29770.0 | 10.0% | 9.8% | -0.2 |
| 50.0 | 60.0 | app1 | True | 134984.0 | 40.0% | 44.2% | 4.2 |
| 50.0 | 60.0 | app2 | True | 29690.0 | 20.0% | 9.7% | -10.3 |
| 50.0 | 60.0 | app6 | True | 18968.0 | 5.0% | 6.2% | 1.2 |
| 50.0 | 60.0 | app3 | True | 54234.0 | 15.0% | 17.7% | 2.7 |
| 50.0 | 60.0 | app5 | True | 33836.0 | 10.0% | 11.1% | 1.1 |
| 50.0 | 60.0 | app4 | True | 33876.0 | 10.0% | 11.1% | 1.1 |
| 60.0 | 70.0 | app1 | True | 105478.0 | 40.0% | 35.0% | -5.0 |
| 60.0 | 70.0 | app2 | True | 54118.0 | 20.0% | 17.9% | -2.1 |
| 60.0 | 70.0 | app6 | True | 29794.0 | 5.0% | 9.9% | 4.9 |
| 60.0 | 70.0 | app3 | True | 40550.0 | 15.0% | 13.4% | -1.6 |
| 60.0 | 70.0 | app5 | True | 36538.0 | 10.0% | 12.1% | 2.1 |
| 60.0 | 70.0 | app4 | True | 35190.0 | 10.0% | 11.7% | 1.7 |
| 70.0 | 80.0 | app1 | True | 116284.0 | 40.0% | 38.2% | -1.8 |
| 70.0 | 80.0 | app2 | True | 8108.0 | 20.0% | 2.7% | -17.3 |
| 70.0 | 80.0 | app6 | True | 46030.0 | 5.0% | 15.1% | 10.1 |
| 70.0 | 80.0 | app3 | True | 48660.0 | 15.0% | 16.0% | 1.0 |
| 70.0 | 80.0 | app5 | True | 39190.0 | 10.0% | 12.9% | 2.9 |
| 70.0 | 80.0 | app4 | True | 45890.0 | 10.0% | 15.1% | 5.1 |
| 80.0 | 90.0 | app1 | True | 132670.0 | 40.0% | 43.6% | 3.6 |
| 80.0 | 90.0 | app2 | True | 39176.0 | 20.0% | 12.9% | -7.1 |
| 80.0 | 90.0 | app6 | True | 14916.0 | 5.0% | 4.9% | -0.1 |
| 80.0 | 90.0 | app3 | True | 52832.0 | 15.0% | 17.4% | 2.4 |
| 80.0 | 90.0 | app5 | True | 33830.0 | 10.0% | 11.1% | 1.1 |
| 80.0 | 90.0 | app4 | True | 31072.0 | 10.0% | 10.2% | 0.2 |
| 90.0 | 100.0 | app1 | True | 86464.0 | 40.0% | 32.1% | -7.9 |
| 90.0 | 100.0 | app2 | True | 40664.0 | 20.0% | 15.1% | -4.9 |
| 90.0 | 100.0 | app6 | True | 23030.0 | 5.0% | 8.6% | 3.6 |
| 90.0 | 100.0 | app3 | True | 29804.0 | 15.0% | 11.1% | -3.9 |
| 90.0 | 100.0 | app5 | True | 44596.0 | 10.0% | 16.6% | 6.6 |
| 90.0 | 100.0 | app4 | True | 44604.0 | 10.0% | 16.6% | 6.6 |
| 100.0 | 110.0 | app1 | True | 124434.0 | 40.0% | 41.1% | 1.1 |
| 100.0 | 110.0 | app2 | True | 52736.0 | 20.0% | 17.4% | -2.6 |
| 100.0 | 110.0 | app6 | True | 46104.0 | 5.0% | 15.2% | 10.2 |
| 100.0 | 110.0 | app3 | True | 52728.0 | 15.0% | 17.4% | 2.4 |
| 100.0 | 110.0 | app5 | True | 13470.0 | 10.0% | 4.4% | -5.6 |
| 100.0 | 110.0 | app4 | True | 13558.0 | 10.0% | 4.5% | -5.5 |
| 110.0 | 120.0 | app1 | True | 97366.0 | 40.0% | 31.9% | -8.1 |
| 110.0 | 120.0 | app2 | True | 43332.0 | 20.0% | 14.2% | -5.8 |
| 110.0 | 120.0 | app6 | True | 29700.0 | 5.0% | 9.7% | 4.7 |
| 110.0 | 120.0 | app3 | True | 41978.0 | 15.0% | 13.7% | -1.3 |
| 110.0 | 120.0 | app5 | True | 47312.0 | 10.0% | 15.5% | 5.5 |
| 110.0 | 120.0 | app4 | True | 45962.0 | 10.0% | 15.0% | 5.0 |
| 120.0 | 130.0 | app1 | True | 117716.0 | 40.0% | 38.7% | -1.3 |
| 120.0 | 130.0 | app2 | True | 36460.0 | 20.0% | 12.0% | -8.0 |
| 120.0 | 130.0 | app6 | True | 28440.0 | 5.0% | 9.3% | 4.3 |
| 120.0 | 130.0 | app3 | True | 59420.0 | 15.0% | 19.5% | 4.5 |
| 120.0 | 130.0 | app5 | True | 28378.0 | 10.0% | 9.3% | -0.7 |
| 120.0 | 130.0 | app4 | True | 33876.0 | 10.0% | 11.1% | 1.1 |
| 130.0 | 140.0 | app1 | True | 113748.0 | 40.0% | 37.7% | -2.3 |
| 130.0 | 140.0 | app2 | True | 32502.0 | 20.0% | 10.8% | -9.2 |
| 130.0 | 140.0 | app6 | True | 29772.0 | 5.0% | 9.9% | 4.9 |
| 130.0 | 140.0 | app3 | True | 28404.0 | 15.0% | 9.4% | -5.6 |
| 130.0 | 140.0 | app5 | True | 49968.0 | 10.0% | 16.6% | 6.6 |
| 130.0 | 140.0 | app4 | True | 47340.0 | 10.0% | 15.7% | 5.7 |
| 140.0 | 150.0 | app1 | True | 121732.0 | 40.0% | 40.4% | 0.4 |
| 140.0 | 150.0 | app2 | True | 58150.0 | 20.0% | 19.3% | -0.7 |
| 140.0 | 150.0 | app6 | True | 13540.0 | 5.0% | 4.5% | -0.5 |
| 140.0 | 150.0 | app3 | True | 45972.0 | 15.0% | 15.2% | 0.2 |
| 140.0 | 150.0 | app5 | True | 29742.0 | 10.0% | 9.9% | -0.1 |
| 140.0 | 150.0 | app4 | True | 32434.0 | 10.0% | 10.8% | 0.8 |
| 150.0 | 160.0 | app1 | True | 147218.0 | 40.0% | 47.6% | 7.6 |
| 150.0 | 160.0 | app2 | True | 13546.0 | 20.0% | 4.4% | -15.6 |
| 150.0 | 160.0 | app6 | True | 20320.0 | 5.0% | 6.6% | 1.6 |
| 150.0 | 160.0 | app3 | True | 54078.0 | 15.0% | 17.5% | 2.5 |
| 150.0 | 160.0 | app5 | True | 37810.0 | 10.0% | 12.2% | 2.2 |
| 150.0 | 160.0 | app4 | True | 36472.0 | 10.0% | 11.8% | 1.8 |
| 160.0 | 170.0 | app1 | True | 70280.0 | 40.0% | 27.9% | -12.1 |
| 160.0 | 170.0 | app2 | True | 29796.0 | 20.0% | 11.8% | -8.2 |
| 160.0 | 170.0 | app6 | True | 48800.0 | 5.0% | 19.4% | 14.4 |
| 160.0 | 170.0 | app3 | True | 31126.0 | 15.0% | 12.4% | -2.6 |
| 160.0 | 170.0 | app5 | True | 36542.0 | 10.0% | 14.5% | 4.5 |
| 160.0 | 170.0 | app4 | True | 35110.0 | 10.0% | 14.0% | 4.0 |
| 170.0 | 180.0 | app1 | True | 135312.0 | 40.0% | 44.1% | 4.1 |
| 170.0 | 180.0 | app2 | True | 13444.0 | 20.0% | 4.4% | -15.6 |
| 170.0 | 180.0 | app6 | True | 28434.0 | 5.0% | 9.3% | 4.3 |
| 170.0 | 180.0 | app3 | True | 52670.0 | 15.0% | 17.2% | 2.2 |
| 170.0 | 180.0 | app5 | True | 36536.0 | 10.0% | 11.9% | 1.9 |
| 170.0 | 180.0 | app4 | True | 40516.0 | 10.0% | 13.2% | 3.2 |
| 180.0 | 191.0 | app1 | True | 60850.0 | 40.0% | 20.9% | -19.1 |
| 180.0 | 191.0 | app2 | True | 43242.0 | 20.0% | 14.9% | -5.1 |
| 180.0 | 191.0 | app6 | True | 27054.0 | 5.0% | 9.3% | 4.3 |
| 180.0 | 191.0 | app3 | True | 54130.0 | 15.0% | 18.6% | 3.6 |
| 180.0 | 191.0 | app5 | True | 54030.0 | 10.0% | 18.6% | 8.6 |
| 180.0 | 191.0 | app4 | True | 51432.0 | 10.0% | 17.7% | 7.7 |
| 191.0 | 201.0 | app1 | True | 47326.0 | 40.0% | 31.0% | -9.0 |
| 191.0 | 201.0 | app2 | True | 6770.0 | 20.0% | 4.4% | -15.6 |
| 191.0 | 201.0 | app6 | True | 75686.0 | 5.0% | 49.5% | 44.5 |
| 191.0 | 201.0 | app3 | True | 8114.0 | 15.0% | 5.3% | -9.7 |
| 191.0 | 201.0 | app5 | True | 5400.0 | 10.0% | 3.5% | -6.5 |
| 191.0 | 201.0 | app4 | True | 9464.0 | 10.0% | 6.2% | -3.8 |
| 201.0 | 211.0 | app1 | True | 59548.0 | 40.0% | 24.3% | -15.7 |
| 201.0 | 211.0 | app2 | True | 46002.0 | 20.0% | 18.8% | -1.2 |
| 201.0 | 211.0 | app6 | True | 86530.0 | 5.0% | 35.3% | 30.3 |
| 201.0 | 211.0 | app3 | True | 27046.0 | 15.0% | 11.0% | -4.0 |
| 201.0 | 211.0 | app5 | True | 13552.0 | 10.0% | 5.5% | -4.5 |
| 201.0 | 211.0 | app4 | True | 12142.0 | 10.0% | 5.0% | -5.0 |
| 211.0 | 221.0 | app1 | True | 62240.0 | 40.0% | 25.7% | -14.3 |
| 211.0 | 221.0 | app2 | True | 5406.0 | 20.0% | 2.2% | -17.8 |
| 211.0 | 221.0 | app6 | True | 59530.0 | 5.0% | 24.6% | 19.6 |
| 211.0 | 221.0 | app3 | True | 23006.0 | 15.0% | 9.5% | -5.5 |
| 211.0 | 221.0 | app5 | True | 45990.0 | 10.0% | 19.0% | 9.0 |
| 211.0 | 221.0 | app4 | True | 45978.0 | 10.0% | 19.0% | 9.0 |
| 221.0 | 231.0 | app1 | True | 102708.0 | 40.0% | 35.3% | -4.7 |
| 221.0 | 231.0 | app2 | True | 44674.0 | 20.0% | 15.4% | -4.6 |
| 221.0 | 231.0 | app6 | True | 69064.0 | 5.0% | 23.7% | 18.7 |
| 221.0 | 231.0 | app3 | True | 41950.0 | 15.0% | 14.4% | -0.6 |
| 221.0 | 231.0 | app5 | True | 14896.0 | 10.0% | 5.1% | -4.9 |
| 221.0 | 231.0 | app4 | True | 17606.0 | 10.0% | 6.1% | -3.9 |
| 231.0 | 241.0 | app1 | True | 82472.0 | 40.0% | 28.0% | -12.0 |
| 231.0 | 241.0 | app2 | True | 43278.0 | 20.0% | 14.7% | -5.3 |
| 231.0 | 241.0 | app6 | True | 44680.0 | 5.0% | 15.2% | 10.2 |
| 231.0 | 241.0 | app3 | True | 41894.0 | 15.0% | 14.2% | -0.8 |
| 231.0 | 241.0 | app5 | True | 43360.0 | 10.0% | 14.7% | 4.7 |
| 231.0 | 241.0 | app4 | True | 39226.0 | 10.0% | 13.3% | 3.3 |
| 241.0 | 251.0 | app1 | False | 62250.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 43318.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app6 | False | 68982.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | 41882.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app5 | False | 43260.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app4 | False | 43234.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 48736.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | False | 108186.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 492.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 492.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 492.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 492.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 492.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 492.0 | app4 | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 32 | 0ms | 4ms | 84ms |
| 0.0 | 10.0 | app2 | ok | 16 | 0ms | 35ms | 226ms |
| 0.0 | 10.0 | app6 | ok | 59 | 0ms | 39ms | 228ms |
| 0.0 | 10.0 | app3 | ok | 20 | 0ms | 10ms | 220ms |
| 0.0 | 10.0 | app5 | ok | 21 | 0ms | 0ms | 89ms |
| 0.0 | 10.0 | app4 | ok | 19 | 0ms | 155ms | 240ms |
| 10.0 | 20.0 | app1 | ok | 59 | 0ms | 508ms | 951ms |
| 10.0 | 20.0 | app2 | ok | 25 | 0ms | 583ms | 958ms |
| 10.0 | 20.0 | app6 | ok | 99 | 0ms | 455ms | 945ms |
| 10.0 | 20.0 | app3 | ok | 22 | 0ms | 80ms | 217ms |
| 10.0 | 20.0 | app5 | ok | 23 | 18ms | 617ms | 962ms |
| 10.0 | 20.0 | app4 | ok | 23 | 0ms | 67ms | 215ms |
| 20.0 | 30.0 | app1 | ok | 65 | 1993ms | 4188ms | 4919ms |
| 20.0 | 30.0 | app2 | ok | 29 | 2015ms | 4194ms | 4919ms |
| 20.0 | 30.0 | app6 | ok | 45 | 2219ms | 6786ms | 9679ms |
| 20.0 | 30.0 | app3 | ok | 25 | 2596ms | 4519ms | 4952ms |
| 20.0 | 30.0 | app5 | ok | 18 | 2333ms | 4438ms | 4944ms |
| 20.0 | 30.0 | app4 | ok | 23 | 2179ms | 4425ms | 4942ms |
| 30.0 | 40.0 | app1 | ok | 105 | 3569ms | 4834ms | 8950ms |
| 30.0 | 40.0 | app2 | ok | 54 | 2589ms | 4518ms | 4952ms |
| 30.0 | 40.0 | app6 | ok | 17 | 11111ms | 26222ms | 29622ms |
| 30.0 | 40.0 | app3 | ok | 40 | 5238ms | 9048ms | 9905ms |
| 30.0 | 40.0 | app5 | ok | 27 | 7125ms | 9825ms | 27300ms |
| 30.0 | 40.0 | app4 | ok | 27 | 7024ms | 9595ms | 24600ms |
| 40.0 | 50.0 | app1 | ok | 84 | 3250ms | 4650ms | 4965ms |
| 40.0 | 50.0 | app2 | ok | 40 | 1789ms | 4091ms | 4909ms |
| 40.0 | 50.0 | app6 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app3 | ok | 32 | 4405ms | 8545ms | 9855ms |
| 40.0 | 50.0 | app5 | ok | 21 | 8750ms | 24000ms | 29400ms |
| 40.0 | 50.0 | app4 | ok | 22 | 8056ms | 19000ms | 28900ms |
| 50.0 | 60.0 | app1 | ok | 101 | 2109ms | 4336ms | 4934ms |
| 50.0 | 60.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app6 | ok | 13 | 35625ms | 55125ms | 59512ms |
| 50.0 | 60.0 | app3 | ok | 38 | 3438ms | 5250ms | 9525ms |
| 50.0 | 60.0 | app5 | ok | 26 | 7708ms | 9875ms | 27400ms |
| 50.0 | 60.0 | app4 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 60.0 | 70.0 | app1 | ok | 68 | 3036ms | 7167ms | 9717ms |
| 60.0 | 70.0 | app2 | ok | 46 | 12308ms | 26462ms | 29646ms |
| 60.0 | 70.0 | app6 | ok | 39 | 45000ms | 57000ms | 59700ms |
| 60.0 | 70.0 | app3 | ok | 30 | 3167ms | 6250ms | 9625ms |
| 60.0 | 70.0 | app5 | ok | 31 | 4205ms | 8708ms | 9871ms |
| 60.0 | 70.0 | app4 | ok | 31 | 4062ms | 8591ms | 9859ms |
| 70.0 | 80.0 | app1 | ok | 96 | 2885ms | 8154ms | 9815ms |
| 70.0 | 80.0 | app2 | ok | 9 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app6 | ok | 17 | 45000ms | 57000ms | 59700ms |
| 70.0 | 80.0 | app3 | ok | 37 | 3618ms | 7688ms | 9769ms |
| 70.0 | 80.0 | app5 | ok | 25 | 7159ms | 9432ms | 9943ms |
| 70.0 | 80.0 | app4 | ok | 27 | 6786ms | 9357ms | 9936ms |
| 80.0 | 90.0 | app1 | ok | 120 | 2887ms | 4577ms | 4958ms |
| 80.0 | 90.0 | app2 | ok | 50 | 4545ms | 25652ms | 29565ms |
| 80.0 | 90.0 | app6 | ok | 19 | 45833ms | 58500ms | 60000ms |
| 80.0 | 90.0 | app3 | ok | 48 | 3603ms | 5200ms | 9520ms |
| 80.0 | 90.0 | app5 | ok | 38 | 7031ms | 9406ms | 9941ms |
| 80.0 | 90.0 | app4 | ok | 36 | 7097ms | 9419ms | 9942ms |
| 90.0 | 100.0 | app1 | ok | 29 | 5469ms | 9094ms | 9909ms |
| 90.0 | 100.0 | app2 | ok | 14 | 5000ms | 9000ms | 9900ms |
| 90.0 | 100.0 | app6 | ok | 27 | 60000ms | 60000ms | 60000ms |
| 90.0 | 100.0 | app3 | ok | 11 | 6071ms | 9214ms | 9921ms |
| 90.0 | 100.0 | app5 | ok | 18 | 5500ms | 9100ms | 9910ms |
| 90.0 | 100.0 | app4 | ok | 20 | 5455ms | 9091ms | 9909ms |
| 100.0 | 110.0 | app1 | ok | 131 | 2304ms | 7741ms | 9774ms |
| 100.0 | 110.0 | app2 | ok | 30 | 4000ms | 8846ms | 9885ms |
| 100.0 | 110.0 | app6 | ok | 24 | 45000ms | 57000ms | 59700ms |
| 100.0 | 110.0 | app3 | ok | 54 | 3261ms | 7545ms | 9755ms |
| 100.0 | 110.0 | app5 | ok | 20 | 18235ms | 27647ms | 29765ms |
| 100.0 | 110.0 | app4 | ok | 19 | 18125ms | 27625ms | 29762ms |
| 110.0 | 120.0 | app1 | ok | 56 | 7500ms | 9500ms | 9950ms |
| 110.0 | 120.0 | app2 | ok | 43 | 5326ms | 9065ms | 9907ms |
| 110.0 | 120.0 | app6 | ok | 22 | 45000ms | 57000ms | 59700ms |
| 110.0 | 120.0 | app3 | ok | 22 | 7381ms | 9476ms | 9948ms |
| 110.0 | 120.0 | app5 | ok | 28 | 4167ms | 25333ms | 29533ms |
| 110.0 | 120.0 | app4 | ok | 30 | 4167ms | 25385ms | 29538ms |
| 120.0 | 130.0 | app1 | ok | 43 | 4018ms | 8656ms | 9866ms |
| 120.0 | 130.0 | app2 | ok | 33 | 7054ms | 9411ms | 9941ms |
| 120.0 | 130.0 | app6 | ok | 18 | 45000ms | 57000ms | 59700ms |
| 120.0 | 130.0 | app3 | ok | 27 | 2250ms | 7300ms | 9730ms |
| 120.0 | 130.0 | app5 | ok | 24 | 7500ms | 9500ms | 9950ms |
| 120.0 | 130.0 | app4 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 130.0 | 140.0 | app1 | ok | 116 | 3833ms | 8067ms | 9807ms |
| 130.0 | 140.0 | app2 | ok | 23 | 7500ms | 9500ms | 9950ms |
| 130.0 | 140.0 | app6 | ok | 17 | 45000ms | 57000ms | 59700ms |
| 130.0 | 140.0 | app3 | ok | 33 | 6700ms | 9340ms | 9934ms |
| 130.0 | 140.0 | app5 | ok | 32 | 4833ms | 8933ms | 9893ms |
| 130.0 | 140.0 | app4 | ok | 32 | 4667ms | 8857ms | 9886ms |
| 140.0 | 150.0 | app1 | ok | 105 | 2848ms | 4570ms | 4957ms |
| 140.0 | 150.0 | app2 | ok | 32 | 2812ms | 8222ms | 9822ms |
| 140.0 | 150.0 | app6 | ok | 13 | 45000ms | 57000ms | 59700ms |
| 140.0 | 150.0 | app3 | ok | 39 | 4076ms | 8227ms | 9823ms |
| 140.0 | 150.0 | app5 | ok | 27 | 7500ms | 9500ms | 9950ms |
| 140.0 | 150.0 | app4 | ok | 26 | 7600ms | 9680ms | 24800ms |
| 150.0 | 160.0 | app1 | ok | 99 | 1809ms | 4048ms | 4905ms |
| 150.0 | 160.0 | app2 | ok | 16 | 16667ms | 27333ms | 29733ms |
| 150.0 | 160.0 | app6 | ok | 21 | 45000ms | 57000ms | 59700ms |
| 150.0 | 160.0 | app3 | ok | 41 | 2865ms | 4573ms | 4957ms |
| 150.0 | 160.0 | app5 | ok | 37 | 5978ms | 9196ms | 9920ms |
| 150.0 | 160.0 | app4 | ok | 39 | 5761ms | 9152ms | 9915ms |
| 160.0 | 170.0 | app1 | ok | 43 | 6019ms | 9204ms | 9920ms |
| 160.0 | 170.0 | app2 | ok | 16 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | app6 | ok | 31 | 59062ms | 60000ms | 60000ms |
| 160.0 | 170.0 | app3 | ok | 16 | 6000ms | 9200ms | 9920ms |
| 160.0 | 170.0 | app5 | ok | 11 | 6071ms | 9214ms | 9921ms |
| 160.0 | 170.0 | app4 | ok | 11 | 5417ms | 9083ms | 9908ms |
| 170.0 | 180.0 | app1 | ok | 87 | 3015ms | 8550ms | 9855ms |
| 170.0 | 180.0 | app2 | ok | 19 | 19444ms | 27889ms | 29789ms |
| 170.0 | 180.0 | app6 | ok | 21 | 45000ms | 57000ms | 59700ms |
| 170.0 | 180.0 | app3 | ok | 49 | 3750ms | 8250ms | 9825ms |
| 170.0 | 180.0 | app5 | ok | 35 | 7266ms | 9453ms | 9945ms |
| 170.0 | 180.0 | app4 | ok | 35 | 6875ms | 9375ms | 9938ms |
| 180.0 | 191.0 | app1 | ok | 75 | 5192ms | 9038ms | 9904ms |
| 180.0 | 191.0 | app2 | ok | 26 | 2500ms | 26000ms | 29600ms |
| 180.0 | 191.0 | app6 | ok | 127 | 26250ms | 52811ms | 59281ms |
| 180.0 | 191.0 | app3 | ok | 30 | 1231ms | 3125ms | 4812ms |
| 180.0 | 191.0 | app5 | ok | 29 | 3068ms | 7583ms | 9758ms |
| 180.0 | 191.0 | app4 | ok | 30 | 3125ms | 7500ms | 9750ms |
| 191.0 | 201.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 68 | 10000ms | 26000ms | 29600ms |
| 201.0 | 211.0 | app2 | ok | 27 | 16500ms | 27300ms | 29730ms |
| 201.0 | 211.0 | app6 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 201.0 | 211.0 | app3 | ok | 24 | 16667ms | 27333ms | 29733ms |
| 201.0 | 211.0 | app5 | ok | 21 | 20000ms | 28000ms | 29800ms |
| 201.0 | 211.0 | app4 | ok | 22 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app1 | ok | 38 | 3077ms | 7889ms | 9789ms |
| 211.0 | 221.0 | app2 | ok | 26 | 7500ms | 9500ms | 9950ms |
| 211.0 | 221.0 | app6 | ok | 44 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app3 | ok | 19 | 5682ms | 9136ms | 9914ms |
| 211.0 | 221.0 | app5 | ok | 21 | 8125ms | 25333ms | 29533ms |
| 211.0 | 221.0 | app4 | ok | 20 | 8750ms | 25556ms | 29556ms |
| 221.0 | 231.0 | app1 | ok | 90 | 4122ms | 8710ms | 12000ms |
| 221.0 | 231.0 | app2 | ok | 43 | 4926ms | 15667ms | 28567ms |
| 221.0 | 231.0 | app6 | ok | 74 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app3 | ok | 47 | 6083ms | 9217ms | 9922ms |
| 221.0 | 231.0 | app5 | ok | 43 | 12800ms | 26560ms | 29656ms |
| 221.0 | 231.0 | app4 | ok | 43 | 13462ms | 26692ms | 29669ms |
| 231.0 | 241.0 | app1 | ok | 46 | 6806ms | 9361ms | 9936ms |
| 231.0 | 241.0 | app2 | ok | 15 | 2656ms | 4531ms | 4953ms |
| 231.0 | 241.0 | app6 | ok | 25 | 20000ms | 28000ms | 29800ms |
| 231.0 | 241.0 | app3 | ok | 12 | 2500ms | 4500ms | 4950ms |
| 231.0 | 241.0 | app5 | ok | 8 | 4500ms | 8667ms | 9867ms |
| 231.0 | 241.0 | app4 | ok | 8 | 4500ms | 8667ms | 9867ms |
| 241.0 | 251.0 | app1 | ok | 52 | 6389ms | 9278ms | 9928ms |
| 241.0 | 251.0 | app2 | ok | 17 | 5750ms | 9150ms | 9915ms |
| 241.0 | 251.0 | app6 | ok | 110 | 17640ms | 27528ms | 29753ms |
| 241.0 | 251.0 | app3 | ok | 19 | 4861ms | 8944ms | 9894ms |
| 241.0 | 251.0 | app5 | ok | 24 | 7273ms | 9455ms | 9945ms |
| 241.0 | 251.0 | app4 | ok | 23 | 7500ms | 9500ms | 9950ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 492.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 492.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 492.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 492.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 492.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 492.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app6 exceeded the 10% ledger tolerance: cost -12.9%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2218920 | 110448 | 2325514.0 | -0.2% | 2357370.0 | 2439816.0 | -3.4% | True |
| app2 | 801960 | 39968 | 838058.0 | -0.5% | 834620.0 | 881896.0 | -5.4% | True |
| app3 | 902820 | 44950 | 947770.0 | 0.0% | 950900.0 | 992720.0 | -4.2% | True |
| app4 | 758910 | 37714 | 795337.0 | -0.2% | 793734.0 | 834338.0 | -4.9% | True |
| app5 | 750300 | 37362 | 785074.0 | -0.3% | 780234.0 | 825024.0 | -5.4% | True |
| app6 | 1119300 | 56101 | 1165097.0 | -0.9% | 1073248.0 | 1231502.0 | -12.9% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1847 | 0 | 0 | 0 (never shed) | 0.00% | 40.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 665 | 0 | 0 | 0 (never shed) | 0.00% | 20.0% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 746 | 0 | 0 | 0 (never shed) | 0.00% | 15.0% | n/a (nothing shed) | n/a (nothing shed) |
| app4 | 628 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| app5 | 620 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| app6 | 968 | 0 | 0 | 0 (never shed) | 0.00% | 5.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5336). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5336 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 470610 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
