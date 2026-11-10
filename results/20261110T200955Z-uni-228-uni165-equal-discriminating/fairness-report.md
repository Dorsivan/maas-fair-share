# Fairness benchmark: uni165-equal-discriminating (uni-228-uni165-equal-discriminating)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 27.8 points

## Run metadata

| field | value |
|---|---|
| Scenario | `uni165-equal-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-699d7f96dd-mcmts` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-10T20:11:20Z` |
| Run end | `2026-11-10T20:18:40Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 16.7 | 128 | 1416 | 000=1, 200=1361, 500=54 | 24.0 | 34.4 | 1620772.0 | 16.7% | 44.4% | 27.8 | 23.6% | 6.9 | 25.5% | 8.9 | 61.0s | 98.9% | 1350.0 |
| app2 | 16.7 | 32 | 821 | 200=802, 500=19 | 8.9 | 14.0 | 1043648.0 | 16.7% | 11.1% | -5.6 | 15.2% | -1.5 | 14.8% | -1.9 | 59.9s | 98.9% | 800.0 |
| app3 | 16.7 | 32 | 846 | 000=1, 200=828, 500=17 | 8.7 | 12.8 | 1074104.0 | 16.7% | 11.1% | -5.6 | 15.6% | -1.0 | 15.3% | -1.4 | 60.9s | 98.9% | 828.0 |
| app4 | 16.7 | 32 | 834 | 200=822, 500=12 | 9.0 | 12.8 | 1062914.0 | 16.7% | 11.1% | -5.6 | 15.5% | -1.2 | 15.0% | -1.6 | 59.9s | 98.9% | 821.0 |
| app5 | 16.7 | 32 | 803 | 000=1, 200=785, 500=17 | 8.8 | 13.6 | 1015910.0 | 16.7% | 11.1% | -5.6 | 14.8% | -1.9 | 14.5% | -2.2 | 61.0s | 98.9% | 785.0 |
| app6 | 16.7 | 32 | 827 | 200=813, 500=14 | 9.0 | 12.9 | 1053536.0 | 16.7% | 11.1% | -5.6 | 15.3% | -1.3 | 14.9% | -1.8 | 61.0s | 98.9% | 812.0 |
| end-users | n/a | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 18.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- app6: active 0s-240s, no duty cycle
- app5: active 0s-240s, no duty cycle
- app3: active 0s-240s, no duty cycle
- app4: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (44 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app2 | True | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app6 | True | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app5 | True | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app3 | True | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app4 | True | 0.0 | 16.7% | 0.0% | -16.7 |
| 10.0 | 20.0 | app1 | True | 17606.0 | 16.7% | 33.4% | 16.7 |
| 10.0 | 20.0 | app2 | True | 6754.0 | 16.7% | 12.8% | -3.9 |
| 10.0 | 20.0 | app6 | True | 6732.0 | 16.7% | 12.8% | -3.9 |
| 10.0 | 20.0 | app5 | True | 5384.0 | 16.7% | 10.2% | -6.5 |
| 10.0 | 20.0 | app3 | True | 9506.0 | 16.7% | 18.0% | 1.4 |
| 10.0 | 20.0 | app4 | True | 6726.0 | 16.7% | 12.8% | -3.9 |
| 20.0 | 30.0 | app1 | True | 102664.0 | 16.7% | 33.4% | 16.8 |
| 20.0 | 30.0 | app2 | True | 40462.0 | 16.7% | 13.2% | -3.5 |
| 20.0 | 30.0 | app6 | True | 46086.0 | 16.7% | 15.0% | -1.7 |
| 20.0 | 30.0 | app5 | True | 43328.0 | 16.7% | 14.1% | -2.6 |
| 20.0 | 30.0 | app3 | True | 35166.0 | 16.7% | 11.5% | -5.2 |
| 20.0 | 30.0 | app4 | True | 39230.0 | 16.7% | 12.8% | -3.9 |
| 30.0 | 40.0 | app1 | True | 51344.0 | 16.7% | 22.2% | 5.5 |
| 30.0 | 40.0 | app2 | True | 36506.0 | 16.7% | 15.8% | -0.9 |
| 30.0 | 40.0 | app6 | True | 35192.0 | 16.7% | 15.2% | -1.5 |
| 30.0 | 40.0 | app5 | True | 35186.0 | 16.7% | 15.2% | -1.5 |
| 30.0 | 40.0 | app3 | True | 36548.0 | 16.7% | 15.8% | -0.9 |
| 30.0 | 40.0 | app4 | True | 36518.0 | 16.7% | 15.8% | -0.9 |
| 40.0 | 50.0 | app1 | True | 85248.0 | 16.7% | 31.7% | 15.0 |
| 40.0 | 50.0 | app2 | True | 31172.0 | 16.7% | 11.6% | -5.1 |
| 40.0 | 50.0 | app6 | True | 40590.0 | 16.7% | 15.1% | -1.6 |
| 40.0 | 50.0 | app5 | True | 31146.0 | 16.7% | 11.6% | -5.1 |
| 40.0 | 50.0 | app3 | True | 41900.0 | 16.7% | 15.6% | -1.1 |
| 40.0 | 50.0 | app4 | True | 39224.0 | 16.7% | 14.6% | -2.1 |
| 50.0 | 60.0 | app1 | True | 60810.0 | 16.7% | 20.3% | 3.6 |
| 50.0 | 60.0 | app2 | True | 32466.0 | 16.7% | 10.8% | -5.9 |
| 50.0 | 60.0 | app6 | True | 58076.0 | 16.7% | 19.3% | 2.7 |
| 50.0 | 60.0 | app5 | True | 33860.0 | 16.7% | 11.3% | -5.4 |
| 50.0 | 60.0 | app3 | True | 56798.0 | 16.7% | 18.9% | 2.3 |
| 50.0 | 60.0 | app4 | True | 58174.0 | 16.7% | 19.4% | 2.7 |
| 60.0 | 70.0 | app1 | True | 90546.0 | 16.7% | 30.0% | 13.4 |
| 60.0 | 70.0 | app2 | True | 48672.0 | 16.7% | 16.1% | -0.5 |
| 60.0 | 70.0 | app6 | True | 37950.0 | 16.7% | 12.6% | -4.1 |
| 60.0 | 70.0 | app5 | True | 47220.0 | 16.7% | 15.7% | -1.0 |
| 60.0 | 70.0 | app3 | True | 37906.0 | 16.7% | 12.6% | -4.1 |
| 60.0 | 70.0 | app4 | True | 39304.0 | 16.7% | 13.0% | -3.6 |
| 70.0 | 80.0 | app1 | True | 54104.0 | 16.7% | 17.6% | 1.0 |
| 70.0 | 80.0 | app2 | True | 49986.0 | 16.7% | 16.3% | -0.4 |
| 70.0 | 80.0 | app6 | True | 50010.0 | 16.7% | 16.3% | -0.4 |
| 70.0 | 80.0 | app5 | True | 51426.0 | 16.7% | 16.8% | 0.1 |
| 70.0 | 80.0 | app3 | True | 51432.0 | 16.7% | 16.8% | 0.1 |
| 70.0 | 80.0 | app4 | True | 50042.0 | 16.7% | 16.3% | -0.4 |
| 80.0 | 90.0 | app1 | True | 48694.0 | 16.7% | 16.4% | -0.2 |
| 80.0 | 90.0 | app2 | True | 50044.0 | 16.7% | 16.9% | 0.2 |
| 80.0 | 90.0 | app6 | True | 47348.0 | 16.7% | 16.0% | -0.7 |
| 80.0 | 90.0 | app5 | True | 50104.0 | 16.7% | 16.9% | 0.2 |
| 80.0 | 90.0 | app3 | True | 50038.0 | 16.7% | 16.9% | 0.2 |
| 80.0 | 90.0 | app4 | True | 49996.0 | 16.7% | 16.9% | 0.2 |
| 90.0 | 100.0 | app1 | True | 71714.0 | 16.7% | 23.8% | 7.1 |
| 90.0 | 100.0 | app2 | True | 40604.0 | 16.7% | 13.5% | -3.2 |
| 90.0 | 100.0 | app6 | True | 47434.0 | 16.7% | 15.7% | -0.9 |
| 90.0 | 100.0 | app5 | True | 41888.0 | 16.7% | 13.9% | -2.8 |
| 90.0 | 100.0 | app3 | True | 56880.0 | 16.7% | 18.8% | 2.2 |
| 90.0 | 100.0 | app4 | True | 43286.0 | 16.7% | 14.3% | -2.3 |
| 100.0 | 110.0 | app1 | True | 56790.0 | 16.7% | 19.4% | 2.8 |
| 100.0 | 110.0 | app2 | True | 58168.0 | 16.7% | 19.9% | 3.2 |
| 100.0 | 110.0 | app6 | True | 43268.0 | 16.7% | 14.8% | -1.9 |
| 100.0 | 110.0 | app5 | True | 39230.0 | 16.7% | 13.4% | -3.2 |
| 100.0 | 110.0 | app3 | True | 49990.0 | 16.7% | 17.1% | 0.4 |
| 100.0 | 110.0 | app4 | True | 44648.0 | 16.7% | 15.3% | -1.4 |
| 110.0 | 120.0 | app1 | True | 66266.0 | 16.7% | 21.9% | 5.2 |
| 110.0 | 120.0 | app2 | True | 52716.0 | 16.7% | 17.4% | 0.7 |
| 110.0 | 120.0 | app6 | True | 37902.0 | 16.7% | 12.5% | -4.2 |
| 110.0 | 120.0 | app5 | True | 40550.0 | 16.7% | 13.4% | -3.3 |
| 110.0 | 120.0 | app3 | True | 54088.0 | 16.7% | 17.9% | 1.2 |
| 110.0 | 120.0 | app4 | True | 51430.0 | 16.7% | 17.0% | 0.3 |
| 120.0 | 131.0 | app1 | True | 67588.0 | 16.7% | 22.0% | 5.3 |
| 120.0 | 131.0 | app2 | True | 41940.0 | 16.7% | 13.7% | -3.0 |
| 120.0 | 131.0 | app6 | True | 50056.0 | 16.7% | 16.3% | -0.4 |
| 120.0 | 131.0 | app5 | True | 48622.0 | 16.7% | 15.8% | -0.8 |
| 120.0 | 131.0 | app3 | True | 48816.0 | 16.7% | 15.9% | -0.8 |
| 120.0 | 131.0 | app4 | True | 50004.0 | 16.7% | 16.3% | -0.4 |
| 131.0 | 141.0 | app1 | True | 50036.0 | 16.7% | 16.5% | -0.2 |
| 131.0 | 141.0 | app2 | True | 49994.0 | 16.7% | 16.5% | -0.2 |
| 131.0 | 141.0 | app6 | True | 50054.0 | 16.7% | 16.5% | -0.1 |
| 131.0 | 141.0 | app5 | True | 50110.0 | 16.7% | 16.5% | -0.1 |
| 131.0 | 141.0 | app3 | True | 51354.0 | 16.7% | 16.9% | 0.3 |
| 131.0 | 141.0 | app4 | True | 51462.0 | 16.7% | 17.0% | 0.3 |
| 141.0 | 151.0 | app1 | True | 48620.0 | 16.7% | 16.1% | -0.6 |
| 141.0 | 151.0 | app2 | True | 50008.0 | 16.7% | 16.5% | -0.2 |
| 141.0 | 151.0 | app6 | True | 52704.0 | 16.7% | 17.4% | 0.7 |
| 141.0 | 151.0 | app5 | True | 50008.0 | 16.7% | 16.5% | -0.2 |
| 141.0 | 151.0 | app3 | True | 50034.0 | 16.7% | 16.5% | -0.1 |
| 141.0 | 151.0 | app4 | True | 51410.0 | 16.7% | 17.0% | 0.3 |
| 151.0 | 161.0 | app1 | True | 51352.0 | 16.7% | 16.7% | 0.1 |
| 151.0 | 161.0 | app2 | True | 51446.0 | 16.7% | 16.8% | 0.1 |
| 151.0 | 161.0 | app6 | True | 48644.0 | 16.7% | 15.8% | -0.8 |
| 151.0 | 161.0 | app5 | True | 51452.0 | 16.7% | 16.8% | 0.1 |
| 151.0 | 161.0 | app3 | True | 52702.0 | 16.7% | 17.2% | 0.5 |
| 151.0 | 161.0 | app4 | True | 51354.0 | 16.7% | 16.7% | 0.1 |
| 161.0 | 171.0 | app1 | True | 51432.0 | 16.7% | 17.0% | 0.3 |
| 161.0 | 171.0 | app2 | True | 51460.0 | 16.7% | 17.0% | 0.3 |
| 161.0 | 171.0 | app6 | True | 51392.0 | 16.7% | 17.0% | 0.3 |
| 161.0 | 171.0 | app5 | True | 52740.0 | 16.7% | 17.4% | 0.7 |
| 161.0 | 171.0 | app3 | True | 47422.0 | 16.7% | 15.6% | -1.0 |
| 161.0 | 171.0 | app4 | True | 48656.0 | 16.7% | 16.1% | -0.6 |
| 171.0 | 181.0 | app1 | True | 52720.0 | 16.7% | 17.2% | 0.5 |
| 171.0 | 181.0 | app2 | True | 51322.0 | 16.7% | 16.7% | 0.1 |
| 171.0 | 181.0 | app6 | True | 50054.0 | 16.7% | 16.3% | -0.4 |
| 171.0 | 181.0 | app5 | True | 48744.0 | 16.7% | 15.9% | -0.8 |
| 171.0 | 181.0 | app3 | True | 52736.0 | 16.7% | 17.2% | 0.5 |
| 171.0 | 181.0 | app4 | True | 51334.0 | 16.7% | 16.7% | 0.1 |
| 181.0 | 191.0 | app1 | True | 81104.0 | 16.7% | 30.0% | 13.3 |
| 181.0 | 191.0 | app2 | True | 39256.0 | 16.7% | 14.5% | -2.1 |
| 181.0 | 191.0 | app6 | True | 37806.0 | 16.7% | 14.0% | -2.7 |
| 181.0 | 191.0 | app5 | True | 37878.0 | 16.7% | 14.0% | -2.7 |
| 181.0 | 191.0 | app3 | True | 36538.0 | 16.7% | 13.5% | -3.2 |
| 181.0 | 191.0 | app4 | True | 37802.0 | 16.7% | 14.0% | -2.7 |
| 191.0 | 201.0 | app1 | True | 116362.0 | 16.7% | 46.0% | 29.4 |
| 191.0 | 201.0 | app2 | True | 26984.0 | 16.7% | 10.7% | -6.0 |
| 191.0 | 201.0 | app6 | True | 29734.0 | 16.7% | 11.8% | -4.9 |
| 191.0 | 201.0 | app5 | True | 25746.0 | 16.7% | 10.2% | -6.5 |
| 191.0 | 201.0 | app3 | True | 27024.0 | 16.7% | 10.7% | -6.0 |
| 191.0 | 201.0 | app4 | True | 27006.0 | 16.7% | 10.7% | -6.0 |
| 201.0 | 211.0 | app1 | True | 55392.0 | 16.7% | 18.0% | 1.3 |
| 201.0 | 211.0 | app2 | True | 49940.0 | 16.7% | 16.2% | -0.5 |
| 201.0 | 211.0 | app6 | True | 51438.0 | 16.7% | 16.7% | 0.0 |
| 201.0 | 211.0 | app5 | True | 50098.0 | 16.7% | 16.2% | -0.4 |
| 201.0 | 211.0 | app3 | True | 50082.0 | 16.7% | 16.2% | -0.4 |
| 201.0 | 211.0 | app4 | True | 51402.0 | 16.7% | 16.7% | 0.0 |
| 211.0 | 221.0 | app1 | True | 51226.0 | 16.7% | 16.8% | 0.1 |
| 211.0 | 221.0 | app2 | True | 50036.0 | 16.7% | 16.4% | -0.3 |
| 211.0 | 221.0 | app6 | True | 48602.0 | 16.7% | 15.9% | -0.8 |
| 211.0 | 221.0 | app5 | True | 52806.0 | 16.7% | 17.3% | 0.6 |
| 211.0 | 221.0 | app3 | True | 51388.0 | 16.7% | 16.8% | 0.2 |
| 211.0 | 221.0 | app4 | True | 51384.0 | 16.7% | 16.8% | 0.2 |
| 221.0 | 231.0 | app1 | True | 51330.0 | 16.7% | 16.7% | -0.0 |
| 221.0 | 231.0 | app2 | True | 52602.0 | 16.7% | 17.1% | 0.4 |
| 221.0 | 231.0 | app6 | True | 52740.0 | 16.7% | 17.1% | 0.4 |
| 221.0 | 231.0 | app5 | True | 50036.0 | 16.7% | 16.2% | -0.4 |
| 221.0 | 231.0 | app3 | True | 50034.0 | 16.7% | 16.2% | -0.4 |
| 221.0 | 231.0 | app4 | True | 51444.0 | 16.7% | 16.7% | 0.0 |
| 231.0 | 241.0 | app1 | True | 108144.0 | 16.7% | 39.6% | 22.9 |
| 231.0 | 241.0 | app2 | True | 33754.0 | 16.7% | 12.4% | -4.3 |
| 231.0 | 241.0 | app6 | True | 33776.0 | 16.7% | 12.4% | -4.3 |
| 231.0 | 241.0 | app5 | True | 32468.0 | 16.7% | 11.9% | -4.8 |
| 231.0 | 241.0 | app3 | True | 31098.0 | 16.7% | 11.4% | -5.3 |
| 231.0 | 241.0 | app4 | True | 33844.0 | 16.7% | 12.4% | -4.3 |
| 241.0 | 251.0 | app1 | False | 81032.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 47356.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app6 | False | 36514.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app5 | False | 35128.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | 35164.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app4 | False | 47234.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 48648.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | False | 9434.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | False | 10752.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | False | 9460.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 440.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 440.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 440.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 440.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 440.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 440.0 | app4 | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 62 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 16 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app6 | ok | 20 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app5 | ok | 14 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app3 | ok | 15 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app4 | ok | 19 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 116 | 0ms | 1257ms | 2376ms |
| 10.0 | 20.0 | app2 | ok | 24 | 0ms | 933ms | 2320ms |
| 10.0 | 20.0 | app6 | ok | 30 | 0ms | 833ms | 2275ms |
| 10.0 | 20.0 | app5 | ok | 34 | 0ms | 1480ms | 2398ms |
| 10.0 | 20.0 | app3 | ok | 31 | 38ms | 1338ms | 2384ms |
| 10.0 | 20.0 | app4 | ok | 31 | 0ms | 1570ms | 2407ms |
| 20.0 | 30.0 | app1 | ok | 38 | 4444ms | 8733ms | 9873ms |
| 20.0 | 30.0 | app2 | ok | 37 | 1716ms | 3679ms | 4868ms |
| 20.0 | 30.0 | app6 | ok | 34 | 1978ms | 4056ms | 4906ms |
| 20.0 | 30.0 | app5 | ok | 34 | 1889ms | 3583ms | 4858ms |
| 20.0 | 30.0 | app3 | ok | 34 | 2342ms | 4433ms | 4943ms |
| 20.0 | 30.0 | app4 | ok | 33 | 2708ms | 4542ms | 4954ms |
| 30.0 | 40.0 | app1 | ok | 82 | 11364ms | 26273ms | 29627ms |
| 30.0 | 40.0 | app2 | ok | 41 | 5900ms | 9180ms | 9918ms |
| 30.0 | 40.0 | app6 | ok | 43 | 3516ms | 8208ms | 9821ms |
| 30.0 | 40.0 | app5 | ok | 42 | 3571ms | 8385ms | 9838ms |
| 30.0 | 40.0 | app3 | ok | 43 | 3583ms | 8346ms | 9835ms |
| 30.0 | 40.0 | app4 | ok | 42 | 4038ms | 8688ms | 9869ms |
| 40.0 | 50.0 | app1 | ok | 38 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app2 | ok | 9 | 9500ms | 25500ms | 29550ms |
| 40.0 | 50.0 | app6 | ok | 31 | 3558ms | 8063ms | 9806ms |
| 40.0 | 50.0 | app5 | ok | 8 | 9000ms | 24667ms | 29467ms |
| 40.0 | 50.0 | app3 | ok | 31 | 3229ms | 7786ms | 9779ms |
| 40.0 | 50.0 | app4 | ok | 31 | 3295ms | 8063ms | 9806ms |
| 50.0 | 60.0 | app1 | ok | 71 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app2 | ok | 39 | 4196ms | 17000ms | 28700ms |
| 50.0 | 60.0 | app6 | ok | 35 | 3359ms | 7500ms | 9750ms |
| 50.0 | 60.0 | app5 | ok | 39 | 4250ms | 14400ms | 28440ms |
| 50.0 | 60.0 | app3 | ok | 33 | 2946ms | 6700ms | 9670ms |
| 50.0 | 60.0 | app4 | ok | 34 | 3077ms | 7571ms | 9757ms |
| 60.0 | 70.0 | app1 | ok | 27 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app2 | ok | 23 | 3603ms | 4956ms | 9425ms |
| 60.0 | 70.0 | app6 | ok | 21 | 6500ms | 9300ms | 9930ms |
| 60.0 | 70.0 | app5 | ok | 23 | 3583ms | 6167ms | 9617ms |
| 60.0 | 70.0 | app3 | ok | 22 | 6333ms | 9267ms | 9927ms |
| 60.0 | 70.0 | app4 | ok | 23 | 6167ms | 9233ms | 9923ms |
| 70.0 | 80.0 | app1 | ok | 49 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app2 | ok | 48 | 3309ms | 4721ms | 7600ms |
| 70.0 | 80.0 | app6 | ok | 49 | 3536ms | 4936ms | 9387ms |
| 70.0 | 80.0 | app5 | ok | 48 | 3421ms | 4684ms | 4968ms |
| 70.0 | 80.0 | app3 | ok | 48 | 3603ms | 5200ms | 9520ms |
| 70.0 | 80.0 | app4 | ok | 48 | 3362ms | 5200ms | 9520ms |
| 80.0 | 90.0 | app1 | ok | 41 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app2 | ok | 23 | 3125ms | 4768ms | 8850ms |
| 80.0 | 90.0 | app6 | ok | 24 | 3214ms | 4929ms | 9400ms |
| 80.0 | 90.0 | app5 | ok | 22 | 3036ms | 4607ms | 4961ms |
| 80.0 | 90.0 | app3 | ok | 40 | 2500ms | 4722ms | 9000ms |
| 80.0 | 90.0 | app4 | ok | 24 | 2885ms | 4731ms | 8800ms |
| 90.0 | 100.0 | app1 | ok | 37 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app2 | ok | 34 | 4306ms | 8583ms | 9858ms |
| 90.0 | 100.0 | app6 | ok | 34 | 3889ms | 8111ms | 9811ms |
| 90.0 | 100.0 | app5 | ok | 35 | 4453ms | 8750ms | 9875ms |
| 90.0 | 100.0 | app3 | ok | 27 | 3688ms | 5500ms | 9550ms |
| 90.0 | 100.0 | app4 | ok | 34 | 4048ms | 8111ms | 9811ms |
| 100.0 | 110.0 | app1 | ok | 49 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app2 | ok | 48 | 2167ms | 4500ms | 7600ms |
| 100.0 | 110.0 | app6 | ok | 30 | 3958ms | 8500ms | 9850ms |
| 100.0 | 110.0 | app5 | ok | 29 | 3661ms | 7929ms | 9793ms |
| 100.0 | 110.0 | app3 | ok | 48 | 2250ms | 7333ms | 9733ms |
| 100.0 | 110.0 | app4 | ok | 29 | 3977ms | 8550ms | 9855ms |
| 110.0 | 120.0 | app1 | ok | 58 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app2 | ok | 33 | 3542ms | 8731ms | 9873ms |
| 110.0 | 120.0 | app6 | ok | 36 | 5000ms | 9000ms | 9900ms |
| 110.0 | 120.0 | app5 | ok | 35 | 4583ms | 8833ms | 9883ms |
| 110.0 | 120.0 | app3 | ok | 36 | 1971ms | 5500ms | 9550ms |
| 110.0 | 120.0 | app4 | ok | 46 | 2833ms | 7700ms | 9770ms |
| 120.0 | 131.0 | app1 | ok | 34 | 20000ms | 28000ms | 29800ms |
| 120.0 | 131.0 | app2 | ok | 30 | 5312ms | 9062ms | 9906ms |
| 120.0 | 131.0 | app6 | ok | 31 | 3938ms | 7786ms | 9779ms |
| 120.0 | 131.0 | app5 | ok | 31 | 3819ms | 7786ms | 9779ms |
| 120.0 | 131.0 | app3 | ok | 33 | 3920ms | 7643ms | 9764ms |
| 120.0 | 131.0 | app4 | ok | 32 | 3810ms | 7333ms | 9733ms |
| 131.0 | 141.0 | app1 | ok | 45 | 20000ms | 28000ms | 29800ms |
| 131.0 | 141.0 | app2 | ok | 44 | 3581ms | 4770ms | 7800ms |
| 131.0 | 141.0 | app6 | ok | 45 | 3547ms | 4764ms | 7750ms |
| 131.0 | 141.0 | app5 | ok | 45 | 3295ms | 4659ms | 4966ms |
| 131.0 | 141.0 | app3 | ok | 43 | 3715ms | 4910ms | 9283ms |
| 131.0 | 141.0 | app4 | ok | 44 | 3603ms | 4897ms | 9267ms |
| 141.0 | 151.0 | app1 | ok | 31 | 20000ms | 28000ms | 29800ms |
| 141.0 | 151.0 | app2 | ok | 32 | 3500ms | 4780ms | 8400ms |
| 141.0 | 151.0 | app6 | ok | 30 | 3661ms | 4732ms | 4973ms |
| 141.0 | 151.0 | app5 | ok | 31 | 3315ms | 4663ms | 4966ms |
| 141.0 | 151.0 | app3 | ok | 31 | 3657ms | 4806ms | 8450ms |
| 141.0 | 151.0 | app4 | ok | 31 | 3616ms | 4723ms | 4972ms |
| 151.0 | 161.0 | app1 | ok | 41 | 20513ms | 28923ms | 53850ms |
| 151.0 | 161.0 | app2 | ok | 41 | 3598ms | 4841ms | 8975ms |
| 151.0 | 161.0 | app6 | ok | 42 | 3603ms | 4838ms | 8950ms |
| 151.0 | 161.0 | app5 | ok | 41 | 3493ms | 4699ms | 4970ms |
| 151.0 | 161.0 | app3 | ok | 41 | 3493ms | 4699ms | 4970ms |
| 151.0 | 161.0 | app4 | ok | 41 | 3682ms | 4791ms | 7950ms |
| 161.0 | 171.0 | app1 | ok | 37 | 21562ms | 37800ms | 57780ms |
| 161.0 | 171.0 | app2 | ok | 37 | 3150ms | 4630ms | 4963ms |
| 161.0 | 171.0 | app6 | ok | 37 | 3287ms | 4657ms | 4966ms |
| 161.0 | 171.0 | app5 | ok | 38 | 3021ms | 4604ms | 4960ms |
| 161.0 | 171.0 | app3 | ok | 37 | 3177ms | 4719ms | 8150ms |
| 161.0 | 171.0 | app4 | ok | 38 | 3667ms | 4933ms | 9367ms |
| 171.0 | 181.0 | app1 | ok | 50 | 20638ms | 29149ms | 55000ms |
| 171.0 | 181.0 | app2 | ok | 41 | 3259ms | 4723ms | 7950ms |
| 171.0 | 181.0 | app6 | ok | 39 | 3259ms | 4652ms | 4965ms |
| 171.0 | 181.0 | app5 | ok | 39 | 2880ms | 4576ms | 4958ms |
| 171.0 | 181.0 | app3 | ok | 40 | 3214ms | 4643ms | 4964ms |
| 171.0 | 181.0 | app4 | ok | 40 | 3214ms | 4643ms | 4964ms |
| 181.0 | 191.0 | app1 | ok | 64 | 20000ms | 28000ms | 29800ms |
| 181.0 | 191.0 | app2 | ok | 21 | 3594ms | 8250ms | 9825ms |
| 181.0 | 191.0 | app6 | ok | 23 | 3875ms | 8357ms | 9836ms |
| 181.0 | 191.0 | app5 | ok | 21 | 3594ms | 8250ms | 9825ms |
| 181.0 | 191.0 | app3 | ok | 21 | 3750ms | 8500ms | 9850ms |
| 181.0 | 191.0 | app4 | ok | 22 | 3333ms | 7800ms | 9780ms |
| 191.0 | 201.0 | app1 | ok | 74 | 17869ms | 27574ms | 29757ms |
| 191.0 | 201.0 | app2 | ok | 24 | 7609ms | 9696ms | 25200ms |
| 191.0 | 201.0 | app6 | ok | 24 | 6471ms | 9294ms | 9929ms |
| 191.0 | 201.0 | app5 | ok | 24 | 7273ms | 9455ms | 9945ms |
| 191.0 | 201.0 | app3 | ok | 24 | 7273ms | 9455ms | 9945ms |
| 191.0 | 201.0 | app4 | ok | 24 | 7273ms | 9455ms | 9945ms |
| 201.0 | 211.0 | app1 | ok | 35 | 20000ms | 28000ms | 29800ms |
| 201.0 | 211.0 | app2 | ok | 33 | 4115ms | 7938ms | 9794ms |
| 201.0 | 211.0 | app6 | ok | 33 | 3859ms | 7250ms | 9725ms |
| 201.0 | 211.0 | app5 | ok | 33 | 3618ms | 7250ms | 9725ms |
| 201.0 | 211.0 | app3 | ok | 33 | 3859ms | 7250ms | 9725ms |
| 201.0 | 211.0 | app4 | ok | 33 | 4010ms | 7643ms | 9764ms |
| 211.0 | 221.0 | app1 | ok | 46 | 20000ms | 28000ms | 29800ms |
| 211.0 | 221.0 | app2 | ok | 45 | 3651ms | 4836ms | 8875ms |
| 211.0 | 221.0 | app6 | ok | 45 | 3679ms | 4964ms | 9437ms |
| 211.0 | 221.0 | app5 | ok | 45 | 3060ms | 4612ms | 4961ms |
| 211.0 | 221.0 | app3 | ok | 45 | 3320ms | 4727ms | 7750ms |
| 211.0 | 221.0 | app4 | ok | 45 | 3547ms | 4764ms | 7750ms |
| 221.0 | 231.0 | app1 | ok | 42 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app2 | ok | 30 | 2794ms | 4559ms | 4956ms |
| 221.0 | 231.0 | app6 | ok | 31 | 2986ms | 4708ms | 8450ms |
| 221.0 | 231.0 | app5 | ok | 29 | 2583ms | 4517ms | 4952ms |
| 221.0 | 231.0 | app3 | ok | 28 | 3056ms | 4611ms | 4961ms |
| 221.0 | 231.0 | app4 | ok | 30 | 3026ms | 4605ms | 4961ms |
| 231.0 | 241.0 | app1 | ok | 76 | 20000ms | 28000ms | 29800ms |
| 231.0 | 241.0 | app2 | ok | 34 | 4583ms | 8867ms | 9887ms |
| 231.0 | 241.0 | app6 | ok | 35 | 4135ms | 8654ms | 9865ms |
| 231.0 | 241.0 | app5 | ok | 34 | 4583ms | 8867ms | 9887ms |
| 231.0 | 241.0 | app3 | ok | 34 | 4773ms | 8938ms | 9894ms |
| 231.0 | 241.0 | app4 | ok | 35 | 4327ms | 8750ms | 9875ms |
| 241.0 | 251.0 | app1 | ok | 107 | 19192ms | 27838ms | 29784ms |
| 241.0 | 251.0 | app2 | ok | 13 | 4531ms | 8700ms | 9870ms |
| 241.0 | 251.0 | app6 | ok | 10 | 7500ms | 9500ms | 9950ms |
| 241.0 | 251.0 | app5 | ok | 11 | 7500ms | 9500ms | 9950ms |
| 241.0 | 251.0 | app3 | ok | 10 | 7500ms | 9500ms | 9950ms |
| 241.0 | 251.0 | app4 | ok | 12 | 4167ms | 8000ms | 9800ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 440.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 440.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 440.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 440.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 440.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 440.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -11.9%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1674030 | 82997 | 1741514.0 | -0.9% | 1620772.0 | 1840024.0 | -11.9% | False |
| app2 | 986460 | 48869 | 1032742.0 | -0.2% | 1043648.0 | 1084198.0 | -3.7% | True |
| app3 | 1018440 | 50800 | 1067954.0 | -0.1% | 1074104.0 | 1120040.0 | -4.1% | True |
| app4 | 1011060 | 50315 | 1060081.0 | -0.1% | 1062914.0 | 1111690.0 | -4.4% | True |
| app5 | 965550 | 48158 | 1012419.0 | -0.1% | 1015910.0 | 1061866.0 | -4.3% | True |
| app6 | 999990 | 49796 | 1048492.0 | -0.1% | 1053536.0 | 1099582.0 | -4.2% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1416 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 821 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 846 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app4 | 834 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app5 | 803 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |
| app6 | 827 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5414). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5414 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 421928 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
