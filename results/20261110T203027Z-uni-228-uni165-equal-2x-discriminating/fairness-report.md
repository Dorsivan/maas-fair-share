# Fairness benchmark: uni165-equal-2x-discriminating (uni-228-uni165-equal-2x-discriminating)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 27.8 points

## Run metadata

| field | value |
|---|---|
| Scenario | `uni165-equal-2x-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-699d7f96dd-nmr9b` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-10T20:31:41Z` |
| Run end | `2026-11-10T20:36:24Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 16.7 | 256 | 1301 | 200=1249, 403=1, 500=51 | 57.9 | 74.5 | 1310312.0 | 16.7% | 44.4% | 27.8 | 18.9% | 2.2 | 23.1% | 6.4 | 63.1s | 98.9% | 1245.0 |
| app2 | 16.7 | 64 | 879 | 200=868, 500=11 | 17.4 | 21.2 | 1141308.0 | 16.7% | 11.1% | -5.6 | 16.5% | -0.2 | 15.6% | -1.1 | 63.1s | 98.9% | 867.0 |
| app3 | 16.7 | 64 | 845 | 200=831, 500=14 | 17.6 | 22.9 | 1095612.0 | 16.7% | 11.1% | -5.6 | 15.8% | -0.9 | 15.0% | -1.7 | 63.1s | 98.9% | 831.0 |
| app4 | 16.7 | 64 | 874 | 200=863, 500=11 | 17.3 | 21.0 | 1143308.0 | 16.7% | 11.1% | -5.6 | 16.5% | -0.2 | 15.5% | -1.1 | 63.0s | 98.9% | 862.0 |
| app5 | 16.7 | 64 | 850 | 200=839, 500=11 | 17.5 | 22.8 | 1100930.0 | 16.7% | 11.1% | -5.6 | 15.9% | -0.8 | 15.1% | -1.6 | 63.0s | 98.9% | 839.0 |
| app6 | 16.7 | 64 | 882 | 200=871, 500=10, 503=1 | 17.3 | 21.2 | 1144296.0 | 16.7% | 11.1% | -5.6 | 16.5% | -0.2 | 15.7% | -1.0 | 63.0s | 98.9% | 871.0 |
| end-users | n/a | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 9474.0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.1s | 98.9% | 7.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- app5: active 0s-240s, no duty cycle
- app6: active 0s-240s, no duty cycle
- app4: active 0s-240s, no duty cycle
- app3: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 40.0 | 40.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (29 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app2 | True | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app5 | True | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app6 | True | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app4 | True | 0.0 | 16.7% | 0.0% | -16.7 |
| 0.0 | 10.0 | app3 | True | 0.0 | 16.7% | 0.0% | -16.7 |
| 10.0 | 20.0 | app1 | True | 35158.0 | 16.7% | 26.5% | 9.9 |
| 10.0 | 20.0 | app2 | True | 16208.0 | 16.7% | 12.2% | -4.4 |
| 10.0 | 20.0 | app5 | True | 21718.0 | 16.7% | 16.4% | -0.3 |
| 10.0 | 20.0 | app6 | True | 20272.0 | 16.7% | 15.3% | -1.4 |
| 10.0 | 20.0 | app4 | True | 22984.0 | 16.7% | 17.3% | 0.7 |
| 10.0 | 20.0 | app3 | True | 16194.0 | 16.7% | 12.2% | -4.4 |
| 20.0 | 30.0 | app1 | True | 127044.0 | 16.7% | 42.9% | 26.2 |
| 20.0 | 30.0 | app2 | True | 41878.0 | 16.7% | 14.1% | -2.5 |
| 20.0 | 30.0 | app5 | True | 27020.0 | 16.7% | 9.1% | -7.5 |
| 20.0 | 30.0 | app6 | True | 35204.0 | 16.7% | 11.9% | -4.8 |
| 20.0 | 30.0 | app4 | True | 35204.0 | 16.7% | 11.9% | -4.8 |
| 20.0 | 30.0 | app3 | True | 29808.0 | 16.7% | 10.1% | -6.6 |
| 30.0 | 40.0 | app1 | True | 87838.0 | 16.7% | 28.4% | 11.7 |
| 30.0 | 40.0 | app2 | True | 46052.0 | 16.7% | 14.9% | -1.8 |
| 30.0 | 40.0 | app5 | True | 47400.0 | 16.7% | 15.3% | -1.4 |
| 30.0 | 40.0 | app6 | True | 45990.0 | 16.7% | 14.8% | -1.8 |
| 30.0 | 40.0 | app4 | True | 37882.0 | 16.7% | 12.2% | -4.4 |
| 30.0 | 40.0 | app3 | True | 44658.0 | 16.7% | 14.4% | -2.3 |
| 40.0 | 50.0 | app1 | True | 39202.0 | 16.7% | 17.5% | 0.9 |
| 40.0 | 50.0 | app2 | True | 31208.0 | 16.7% | 14.0% | -2.7 |
| 40.0 | 50.0 | app5 | True | 36514.0 | 16.7% | 16.3% | -0.3 |
| 40.0 | 50.0 | app6 | True | 39284.0 | 16.7% | 17.6% | 0.9 |
| 40.0 | 50.0 | app4 | True | 39328.0 | 16.7% | 17.6% | 0.9 |
| 40.0 | 50.0 | app3 | True | 37888.0 | 16.7% | 17.0% | 0.3 |
| 50.0 | 60.0 | app1 | True | 54042.0 | 16.7% | 22.0% | 5.3 |
| 50.0 | 60.0 | app2 | True | 51376.0 | 16.7% | 20.9% | 4.2 |
| 50.0 | 60.0 | app5 | True | 20286.0 | 16.7% | 8.2% | -8.4 |
| 50.0 | 60.0 | app6 | True | 50050.0 | 16.7% | 20.3% | 3.7 |
| 50.0 | 60.0 | app4 | True | 52640.0 | 16.7% | 21.4% | 4.7 |
| 50.0 | 60.0 | app3 | True | 17586.0 | 16.7% | 7.1% | -9.5 |
| 60.0 | 70.0 | app1 | True | 41928.0 | 16.7% | 17.4% | 0.7 |
| 60.0 | 70.0 | app2 | True | 40602.0 | 16.7% | 16.9% | 0.2 |
| 60.0 | 70.0 | app5 | True | 36546.0 | 16.7% | 15.2% | -1.5 |
| 60.0 | 70.0 | app6 | True | 44624.0 | 16.7% | 18.5% | 1.9 |
| 60.0 | 70.0 | app4 | True | 41942.0 | 16.7% | 17.4% | 0.7 |
| 60.0 | 70.0 | app3 | True | 35184.0 | 16.7% | 14.6% | -2.1 |
| 70.0 | 80.0 | app1 | True | 45954.0 | 16.7% | 16.9% | 0.2 |
| 70.0 | 80.0 | app2 | True | 45922.0 | 16.7% | 16.9% | 0.2 |
| 70.0 | 80.0 | app5 | True | 44636.0 | 16.7% | 16.4% | -0.2 |
| 70.0 | 80.0 | app6 | True | 43284.0 | 16.7% | 15.9% | -0.7 |
| 70.0 | 80.0 | app4 | True | 45968.0 | 16.7% | 16.9% | 0.3 |
| 70.0 | 80.0 | app3 | True | 45932.0 | 16.7% | 16.9% | 0.2 |
| 80.0 | 90.0 | app1 | True | 48674.0 | 16.7% | 16.1% | -0.5 |
| 80.0 | 90.0 | app2 | True | 50072.0 | 16.7% | 16.6% | -0.1 |
| 80.0 | 90.0 | app5 | True | 52752.0 | 16.7% | 17.5% | 0.8 |
| 80.0 | 90.0 | app6 | True | 50104.0 | 16.7% | 16.6% | -0.1 |
| 80.0 | 90.0 | app4 | True | 48768.0 | 16.7% | 16.2% | -0.5 |
| 80.0 | 90.0 | app3 | True | 51416.0 | 16.7% | 17.0% | 0.4 |
| 90.0 | 100.0 | app1 | True | 50058.0 | 16.7% | 16.5% | -0.1 |
| 90.0 | 100.0 | app2 | True | 54050.0 | 16.7% | 17.8% | 1.2 |
| 90.0 | 100.0 | app5 | True | 47354.0 | 16.7% | 15.6% | -1.0 |
| 90.0 | 100.0 | app6 | True | 51460.0 | 16.7% | 17.0% | 0.3 |
| 90.0 | 100.0 | app4 | True | 51410.0 | 16.7% | 17.0% | 0.3 |
| 90.0 | 100.0 | app3 | True | 48676.0 | 16.7% | 16.1% | -0.6 |
| 100.0 | 110.0 | app1 | True | 53924.0 | 16.7% | 17.6% | 1.0 |
| 100.0 | 110.0 | app2 | True | 47390.0 | 16.7% | 15.5% | -1.2 |
| 100.0 | 110.0 | app5 | True | 52782.0 | 16.7% | 17.3% | 0.6 |
| 100.0 | 110.0 | app6 | True | 48650.0 | 16.7% | 15.9% | -0.7 |
| 100.0 | 110.0 | app4 | True | 51382.0 | 16.7% | 16.8% | 0.1 |
| 100.0 | 110.0 | app3 | True | 51472.0 | 16.7% | 16.8% | 0.2 |
| 110.0 | 120.0 | app1 | True | 49984.0 | 16.7% | 16.3% | -0.4 |
| 110.0 | 120.0 | app2 | True | 51458.0 | 16.7% | 16.8% | 0.1 |
| 110.0 | 120.0 | app5 | True | 51340.0 | 16.7% | 16.7% | 0.1 |
| 110.0 | 120.0 | app6 | True | 52800.0 | 16.7% | 17.2% | 0.5 |
| 110.0 | 120.0 | app4 | True | 50012.0 | 16.7% | 16.3% | -0.4 |
| 110.0 | 120.0 | app3 | True | 51404.0 | 16.7% | 16.7% | 0.1 |
| 120.0 | 130.0 | app1 | True | 50068.0 | 16.7% | 16.6% | -0.1 |
| 120.0 | 130.0 | app2 | True | 52764.0 | 16.7% | 17.5% | 0.8 |
| 120.0 | 130.0 | app5 | True | 50018.0 | 16.7% | 16.6% | -0.1 |
| 120.0 | 130.0 | app6 | True | 48670.0 | 16.7% | 16.1% | -0.5 |
| 120.0 | 130.0 | app4 | True | 51420.0 | 16.7% | 17.0% | 0.4 |
| 120.0 | 130.0 | app3 | True | 48720.0 | 16.7% | 16.2% | -0.5 |
| 130.0 | 140.0 | app1 | True | 51426.0 | 16.7% | 16.8% | 0.2 |
| 130.0 | 140.0 | app2 | True | 50008.0 | 16.7% | 16.4% | -0.3 |
| 130.0 | 140.0 | app5 | True | 49988.0 | 16.7% | 16.4% | -0.3 |
| 130.0 | 140.0 | app6 | True | 52720.0 | 16.7% | 17.2% | 0.6 |
| 130.0 | 140.0 | app4 | True | 48710.0 | 16.7% | 15.9% | -0.7 |
| 130.0 | 140.0 | app3 | True | 52798.0 | 16.7% | 17.3% | 0.6 |
| 140.0 | 150.0 | app1 | True | 50060.0 | 16.7% | 16.4% | -0.3 |
| 140.0 | 150.0 | app2 | True | 51334.0 | 16.7% | 16.8% | 0.1 |
| 140.0 | 150.0 | app5 | True | 51348.0 | 16.7% | 16.8% | 0.1 |
| 140.0 | 150.0 | app6 | True | 51400.0 | 16.7% | 16.8% | 0.2 |
| 140.0 | 150.0 | app4 | True | 51406.0 | 16.7% | 16.8% | 0.2 |
| 140.0 | 150.0 | app3 | True | 49926.0 | 16.7% | 16.3% | -0.3 |
| 150.0 | 160.0 | app1 | True | 48754.0 | 16.7% | 16.7% | 0.0 |
| 150.0 | 160.0 | app2 | True | 47260.0 | 16.7% | 16.2% | -0.5 |
| 150.0 | 160.0 | app5 | True | 48684.0 | 16.7% | 16.7% | 0.0 |
| 150.0 | 160.0 | app6 | True | 47336.0 | 16.7% | 16.2% | -0.5 |
| 150.0 | 160.0 | app4 | True | 50036.0 | 16.7% | 17.1% | 0.5 |
| 150.0 | 160.0 | app3 | True | 50004.0 | 16.7% | 17.1% | 0.5 |
| 160.0 | 170.0 | app1 | True | 41898.0 | 16.7% | 16.5% | -0.2 |
| 160.0 | 170.0 | app2 | True | 43276.0 | 16.7% | 17.0% | 0.3 |
| 160.0 | 170.0 | app5 | True | 40592.0 | 16.7% | 16.0% | -0.7 |
| 160.0 | 170.0 | app6 | True | 43284.0 | 16.7% | 17.0% | 0.3 |
| 160.0 | 170.0 | app4 | True | 43336.0 | 16.7% | 17.0% | 0.4 |
| 160.0 | 170.0 | app3 | True | 41988.0 | 16.7% | 16.5% | -0.2 |
| 170.0 | 180.0 | app1 | True | 52800.0 | 16.7% | 17.9% | 1.2 |
| 170.0 | 180.0 | app2 | True | 49980.0 | 16.7% | 16.9% | 0.3 |
| 170.0 | 180.0 | app5 | True | 50150.0 | 16.7% | 17.0% | 0.3 |
| 170.0 | 180.0 | app6 | True | 48686.0 | 16.7% | 16.5% | -0.2 |
| 170.0 | 180.0 | app4 | True | 45944.0 | 16.7% | 15.6% | -1.1 |
| 170.0 | 180.0 | app3 | True | 47352.0 | 16.7% | 16.1% | -0.6 |
| 180.0 | 190.0 | app1 | True | 39206.0 | 16.7% | 15.6% | -1.1 |
| 180.0 | 190.0 | app2 | True | 41930.0 | 16.7% | 16.7% | 0.0 |
| 180.0 | 190.0 | app5 | True | 41910.0 | 16.7% | 16.7% | -0.0 |
| 180.0 | 190.0 | app6 | True | 41888.0 | 16.7% | 16.7% | -0.0 |
| 180.0 | 190.0 | app4 | True | 43308.0 | 16.7% | 17.2% | 0.6 |
| 180.0 | 190.0 | app3 | True | 43274.0 | 16.7% | 17.2% | 0.5 |
| 190.0 | 200.0 | app1 | True | 47346.0 | 16.7% | 16.1% | -0.5 |
| 190.0 | 200.0 | app2 | True | 48620.0 | 16.7% | 16.6% | -0.1 |
| 190.0 | 200.0 | app5 | True | 50046.0 | 16.7% | 17.0% | 0.4 |
| 190.0 | 200.0 | app6 | True | 47398.0 | 16.7% | 16.1% | -0.5 |
| 190.0 | 200.0 | app4 | True | 50088.0 | 16.7% | 17.1% | 0.4 |
| 190.0 | 200.0 | app3 | True | 50138.0 | 16.7% | 17.1% | 0.4 |
| 200.0 | 210.0 | app1 | True | 52790.0 | 16.7% | 17.3% | 0.6 |
| 200.0 | 210.0 | app2 | True | 49938.0 | 16.7% | 16.3% | -0.3 |
| 200.0 | 210.0 | app5 | True | 51338.0 | 16.7% | 16.8% | 0.1 |
| 200.0 | 210.0 | app6 | True | 51314.0 | 16.7% | 16.8% | 0.1 |
| 200.0 | 210.0 | app4 | True | 50094.0 | 16.7% | 16.4% | -0.3 |
| 200.0 | 210.0 | app3 | True | 50002.0 | 16.7% | 16.4% | -0.3 |
| 210.0 | 220.0 | app1 | True | 51388.0 | 16.7% | 16.9% | 0.2 |
| 210.0 | 220.0 | app2 | True | 51380.0 | 16.7% | 16.9% | 0.2 |
| 210.0 | 220.0 | app5 | True | 48700.0 | 16.7% | 16.0% | -0.7 |
| 210.0 | 220.0 | app6 | True | 51372.0 | 16.7% | 16.9% | 0.2 |
| 210.0 | 220.0 | app4 | True | 51484.0 | 16.7% | 16.9% | 0.2 |
| 210.0 | 220.0 | app3 | True | 50030.0 | 16.7% | 16.4% | -0.2 |
| 220.0 | 230.0 | app1 | True | 40562.0 | 16.7% | 16.4% | -0.3 |
| 220.0 | 230.0 | app2 | True | 40642.0 | 16.7% | 16.4% | -0.2 |
| 220.0 | 230.0 | app5 | True | 41954.0 | 16.7% | 17.0% | 0.3 |
| 220.0 | 230.0 | app6 | True | 41912.0 | 16.7% | 16.9% | 0.3 |
| 220.0 | 230.0 | app4 | True | 40550.0 | 16.7% | 16.4% | -0.3 |
| 220.0 | 230.0 | app3 | True | 41850.0 | 16.7% | 16.9% | 0.2 |
| 230.0 | 240.0 | app1 | True | 48758.0 | 16.7% | 17.3% | 0.7 |
| 230.0 | 240.0 | app2 | True | 47356.0 | 16.7% | 16.8% | 0.2 |
| 230.0 | 240.0 | app5 | True | 46000.0 | 16.7% | 16.3% | -0.3 |
| 230.0 | 240.0 | app6 | True | 47306.0 | 16.7% | 16.8% | 0.1 |
| 230.0 | 240.0 | app4 | True | 47340.0 | 16.7% | 16.8% | 0.2 |
| 230.0 | 240.0 | app3 | True | 44654.0 | 16.7% | 15.9% | -0.8 |
| 240.0 | 250.0 | app1 | False | 45994.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 47366.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app5 | False | 48634.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app6 | False | 48728.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app4 | False | 47366.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app3 | False | 48682.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 55456.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 43238.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app5 | False | 43220.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app6 | False | 40560.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app4 | False | 44706.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app3 | False | 45976.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 283.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 283.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 283.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 283.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 283.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 283.0 | app3 | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 52 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 15 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app5 | ok | 14 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app6 | ok | 13 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app4 | ok | 10 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app3 | ok | 11 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 113 | 515ms | 3513ms | 4851ms |
| 10.0 | 20.0 | app2 | ok | 35 | 542ms | 2275ms | 4562ms |
| 10.0 | 20.0 | app5 | ok | 41 | 469ms | 2214ms | 4487ms |
| 10.0 | 20.0 | app6 | ok | 40 | 611ms | 2125ms | 4000ms |
| 10.0 | 20.0 | app4 | ok | 40 | 1088ms | 2500ms | 4750ms |
| 10.0 | 20.0 | app3 | ok | 38 | 583ms | 2114ms | 4525ms |
| 20.0 | 30.0 | app1 | ok | 76 | 4259ms | 8273ms | 9827ms |
| 20.0 | 30.0 | app2 | ok | 32 | 1281ms | 2481ms | 4733ms |
| 20.0 | 30.0 | app5 | ok | 23 | 1422ms | 2284ms | 2478ms |
| 20.0 | 30.0 | app6 | ok | 27 | 1938ms | 3875ms | 4888ms |
| 20.0 | 30.0 | app4 | ok | 19 | 1688ms | 3417ms | 4842ms |
| 20.0 | 30.0 | app3 | ok | 18 | 1333ms | 2750ms | 4775ms |
| 30.0 | 40.0 | app1 | ok | 55 | 7784ms | 16250ms | 28625ms |
| 30.0 | 40.0 | app2 | ok | 32 | 2500ms | 4500ms | 4950ms |
| 30.0 | 40.0 | app5 | ok | 35 | 3350ms | 4750ms | 8250ms |
| 30.0 | 40.0 | app6 | ok | 37 | 2898ms | 4580ms | 4958ms |
| 30.0 | 40.0 | app4 | ok | 38 | 3790ms | 5250ms | 9525ms |
| 30.0 | 40.0 | app3 | ok | 38 | 3696ms | 7286ms | 9729ms |
| 40.0 | 50.0 | app1 | ok | 23 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app2 | ok | 22 | 3036ms | 4607ms | 4961ms |
| 40.0 | 50.0 | app5 | ok | 24 | 2250ms | 7000ms | 9700ms |
| 40.0 | 50.0 | app6 | ok | 23 | 1938ms | 4425ms | 4942ms |
| 40.0 | 50.0 | app4 | ok | 23 | 3472ms | 8083ms | 9808ms |
| 40.0 | 50.0 | app3 | ok | 23 | 3125ms | 8357ms | 9836ms |
| 50.0 | 60.0 | app1 | ok | 63 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app2 | ok | 62 | 8108ms | 22706ms | 29271ms |
| 50.0 | 60.0 | app5 | ok | 34 | 14545ms | 26909ms | 29691ms |
| 50.0 | 60.0 | app6 | ok | 62 | 7581ms | 22250ms | 29225ms |
| 50.0 | 60.0 | app4 | ok | 62 | 7188ms | 20462ms | 29046ms |
| 50.0 | 60.0 | app3 | ok | 33 | 15000ms | 27000ms | 29700ms |
| 60.0 | 70.0 | app1 | ok | 31 | 42778ms | 56556ms | 59656ms |
| 60.0 | 70.0 | app2 | ok | 31 | 15909ms | 27182ms | 29718ms |
| 60.0 | 70.0 | app5 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app6 | ok | 31 | 15909ms | 27182ms | 29718ms |
| 60.0 | 70.0 | app4 | ok | 32 | 15455ms | 27091ms | 29709ms |
| 60.0 | 70.0 | app3 | ok | 31 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app1 | ok | 17 | 45000ms | 57000ms | 59700ms |
| 70.0 | 80.0 | app2 | ok | 17 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app5 | ok | 17 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app6 | ok | 17 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app4 | ok | 16 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app3 | ok | 17 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app1 | ok | 32 | 45000ms | 57000ms | 59700ms |
| 80.0 | 90.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app5 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app6 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app4 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app3 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app1 | ok | 49 | 45000ms | 57000ms | 59700ms |
| 90.0 | 100.0 | app2 | ok | 51 | 19149ms | 27830ms | 29783ms |
| 90.0 | 100.0 | app5 | ok | 49 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app6 | ok | 49 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app4 | ok | 49 | 19792ms | 27958ms | 29796ms |
| 90.0 | 100.0 | app3 | ok | 48 | 19787ms | 27957ms | 29796ms |
| 100.0 | 110.0 | app1 | ok | 30 | 60000ms | 60000ms | 60000ms |
| 100.0 | 110.0 | app2 | ok | 28 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app5 | ok | 31 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app6 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app4 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app3 | ok | 30 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app1 | ok | 34 | 60000ms | 60000ms | 60000ms |
| 110.0 | 120.0 | app2 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app5 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app6 | ok | 34 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app4 | ok | 34 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app3 | ok | 33 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app1 | ok | 39 | 60000ms | 60000ms | 60000ms |
| 120.0 | 130.0 | app2 | ok | 40 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app5 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app6 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app4 | ok | 38 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app3 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 130.0 | 140.0 | app1 | ok | 42 | 60000ms | 60000ms | 60000ms |
| 130.0 | 140.0 | app2 | ok | 41 | 20000ms | 28000ms | 29800ms |
| 130.0 | 140.0 | app5 | ok | 41 | 20000ms | 28000ms | 29800ms |
| 130.0 | 140.0 | app6 | ok | 42 | 20000ms | 28000ms | 29800ms |
| 130.0 | 140.0 | app4 | ok | 41 | 20000ms | 28000ms | 29800ms |
| 130.0 | 140.0 | app3 | ok | 41 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app1 | ok | 39 | 60000ms | 60000ms | 60000ms |
| 140.0 | 150.0 | app2 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app5 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app6 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app4 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app3 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 150.0 | 160.0 | app1 | ok | 30 | 60000ms | 60000ms | 60000ms |
| 150.0 | 160.0 | app2 | ok | 31 | 17083ms | 27417ms | 29742ms |
| 150.0 | 160.0 | app5 | ok | 32 | 17200ms | 27440ms | 29744ms |
| 150.0 | 160.0 | app6 | ok | 31 | 18077ms | 27615ms | 29762ms |
| 150.0 | 160.0 | app4 | ok | 32 | 17692ms | 27538ms | 29754ms |
| 150.0 | 160.0 | app3 | ok | 32 | 17692ms | 27538ms | 29754ms |
| 160.0 | 170.0 | app1 | ok | 29 | 60000ms | 60000ms | 60000ms |
| 160.0 | 170.0 | app2 | ok | 29 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | app5 | ok | 29 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | app6 | ok | 29 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | app4 | ok | 29 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | app3 | ok | 29 | 20000ms | 28000ms | 29800ms |
| 170.0 | 180.0 | app1 | ok | 43 | 60000ms | 60000ms | 60000ms |
| 170.0 | 180.0 | app2 | ok | 44 | 18718ms | 27744ms | 29774ms |
| 170.0 | 180.0 | app5 | ok | 43 | 18378ms | 27676ms | 29768ms |
| 170.0 | 180.0 | app6 | ok | 44 | 18421ms | 27684ms | 29768ms |
| 170.0 | 180.0 | app4 | ok | 43 | 18378ms | 27676ms | 29768ms |
| 170.0 | 180.0 | app3 | ok | 43 | 18684ms | 27737ms | 29774ms |
| 180.0 | 190.0 | app1 | ok | 23 | 60000ms | 60000ms | 60000ms |
| 180.0 | 190.0 | app2 | ok | 22 | 16250ms | 27250ms | 29725ms |
| 180.0 | 190.0 | app5 | ok | 22 | 15333ms | 27067ms | 29707ms |
| 180.0 | 190.0 | app6 | ok | 21 | 13846ms | 26769ms | 29677ms |
| 180.0 | 190.0 | app4 | ok | 22 | 15333ms | 27067ms | 29707ms |
| 180.0 | 190.0 | app3 | ok | 22 | 15333ms | 27067ms | 29707ms |
| 190.0 | 200.0 | app1 | ok | 42 | 60000ms | 60000ms | 60000ms |
| 190.0 | 200.0 | app2 | ok | 42 | 20000ms | 28000ms | 29800ms |
| 190.0 | 200.0 | app5 | ok | 42 | 20000ms | 28000ms | 29800ms |
| 190.0 | 200.0 | app6 | ok | 43 | 20000ms | 28000ms | 29800ms |
| 190.0 | 200.0 | app4 | ok | 43 | 20000ms | 28000ms | 29800ms |
| 190.0 | 200.0 | app3 | ok | 43 | 20000ms | 28000ms | 29800ms |
| 200.0 | 210.0 | app1 | ok | 42 | 60000ms | 60000ms | 60000ms |
| 200.0 | 210.0 | app2 | ok | 42 | 18333ms | 27667ms | 29767ms |
| 200.0 | 210.0 | app5 | ok | 42 | 18649ms | 27730ms | 29773ms |
| 200.0 | 210.0 | app6 | ok | 42 | 18333ms | 27667ms | 29767ms |
| 200.0 | 210.0 | app4 | ok | 41 | 18611ms | 27722ms | 29772ms |
| 200.0 | 210.0 | app3 | ok | 41 | 18286ms | 27657ms | 29766ms |
| 210.0 | 220.0 | app1 | ok | 31 | 60000ms | 60000ms | 60000ms |
| 210.0 | 220.0 | app2 | ok | 32 | 17692ms | 27538ms | 29754ms |
| 210.0 | 220.0 | app5 | ok | 31 | 17600ms | 27520ms | 29752ms |
| 210.0 | 220.0 | app6 | ok | 31 | 18519ms | 27704ms | 29770ms |
| 210.0 | 220.0 | app4 | ok | 31 | 18077ms | 27615ms | 29762ms |
| 210.0 | 220.0 | app3 | ok | 32 | 17692ms | 27538ms | 29754ms |
| 220.0 | 230.0 | app1 | ok | 28 | 60000ms | 60000ms | 60000ms |
| 220.0 | 230.0 | app2 | ok | 27 | 15000ms | 27000ms | 29700ms |
| 220.0 | 230.0 | app5 | ok | 29 | 13889ms | 26778ms | 29678ms |
| 220.0 | 230.0 | app6 | ok | 28 | 14444ms | 26889ms | 29689ms |
| 220.0 | 230.0 | app4 | ok | 28 | 15263ms | 27053ms | 29705ms |
| 220.0 | 230.0 | app3 | ok | 28 | 13529ms | 26706ms | 29671ms |
| 230.0 | 240.0 | app1 | ok | 40 | 60000ms | 60000ms | 60000ms |
| 230.0 | 240.0 | app2 | ok | 41 | 19487ms | 27897ms | 29790ms |
| 230.0 | 240.0 | app5 | ok | 40 | 19744ms | 27949ms | 29795ms |
| 230.0 | 240.0 | app6 | ok | 41 | 19487ms | 27897ms | 29790ms |
| 230.0 | 240.0 | app4 | ok | 41 | 19487ms | 27897ms | 29790ms |
| 230.0 | 240.0 | app3 | ok | 40 | 19744ms | 27949ms | 29795ms |
| 240.0 | 250.0 | app1 | ok | 29 | 60000ms | 60000ms | 60000ms |
| 240.0 | 250.0 | app2 | ok | 29 | 19643ms | 27929ms | 29793ms |
| 240.0 | 250.0 | app5 | ok | 29 | 18846ms | 27769ms | 29777ms |
| 240.0 | 250.0 | app6 | ok | 28 | 19231ms | 27846ms | 29785ms |
| 240.0 | 250.0 | app4 | ok | 29 | 19259ms | 27852ms | 29785ms |
| 240.0 | 250.0 | app3 | ok | 29 | 17917ms | 27583ms | 29758ms |
| 250.0 | 260.0 | app1 | ok | 159 | 52083ms | 60000ms | 60000ms |
| 250.0 | 260.0 | app2 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 250.0 | 260.0 | app5 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 250.0 | 260.0 | app6 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 250.0 | 260.0 | app4 | ok | 19 | 20000ms | 28000ms | 29800ms |
| 250.0 | 260.0 | app3 | ok | 20 | 20000ms | 28000ms | 29800ms |
| 260.0 | 270.0 | app1 | ok | 54 | 24211ms | 49875ms | 58988ms |
| 260.0 | 270.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 280.0 | 283.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 280.0 | 283.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 280.0 | 283.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 280.0 | 283.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 280.0 | 283.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 280.0 | 283.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -22.4%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1536270 | 76122 | 1607224.0 | -0.3% | 1310312.0 | 1688514.0 | -22.4% | False |
| app2 | 1067640 | 53041 | 1119387.0 | -0.1% | 1141308.0 | 1173722.0 | -2.8% | True |
| app3 | 1022130 | 50965 | 1073095.0 | 0.0% | 1095612.0 | 1124060.0 | -2.5% | True |
| app4 | 1061490 | 53097 | 1113293.0 | -0.1% | 1143308.0 | 1167684.0 | -2.1% | True |
| app5 | 1031970 | 51376 | 1083346.0 | 0.0% | 1100930.0 | 1134722.0 | -3.0% | True |
| app6 | 1071330 | 53370 | 1123414.0 | -0.1% | 1144296.0 | 1178070.0 | -2.9% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1301 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | 0.0% | 0.00 |
| app2 | 879 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | 0.0% | 0.00 |
| app3 | 845 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | 0.0% | 0.00 |
| app4 | 874 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | 0.0% | 0.00 |
| app5 | 850 | 0 | 0 | 0 (never shed) | 0.00% | 16.7% | 0.0% | 0.00 |
| app6 | 882 | 0 | 1 | 1 | 0.11% | 16.7% | 100.0% | 6.00 |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5522). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5522 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 273215 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
