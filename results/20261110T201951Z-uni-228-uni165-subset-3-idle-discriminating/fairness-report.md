# Fairness benchmark: uni165-subset-3-idle-discriminating (uni-228-uni165-subset-3-idle-discriminating)

**Verdict: FAIL** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 33.3 points

- app1 deviated +32.2 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `uni165-subset-3-idle-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-699d7f96dd-2cmfc` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-10T20:21:03Z` |
| Run end | `2026-11-10T20:29:16Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 16.7 | 128 | 3593 | 200=3555, 500=38 | 8.5 | 11.6 | 4603704.0 | 33.3% | 66.7% | 33.3 | 65.6% | 32.2 | 65.7% | 32.4 | 38.4s | 98.9% | 3548.0 |
| app2 | 16.7 | 32 | 952 | 200=944, 500=8 | 8.1 | 11.8 | 1228288.0 | 33.3% | 16.7% | -16.7 | 17.5% | -15.8 | 17.4% | -15.9 | 38.1s | 98.9% | 942.0 |
| app3 | 16.7 | 32 | 924 | 000=2, 200=912, 500=10 | 7.8 | 11.7 | 1188596.0 | 33.3% | 16.7% | -16.7 | 16.9% | -16.4 | 16.9% | -16.4 | 37.2s | 98.9% | 912.0 |
| app4 | 16.7 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| app5 | 16.7 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| app6 | 16.7 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| end-users | n/a | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 11.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- app3: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (50 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 0.0 | 10.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 0.0 | 10.0 | app3 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 10.0 | 20.0 | app1 | True | 115040.0 | 33.3% | 60.7% | 27.4 |
| 10.0 | 20.0 | app2 | True | 35166.0 | 33.3% | 18.6% | -14.8 |
| 10.0 | 20.0 | app3 | True | 39178.0 | 33.3% | 20.7% | -12.6 |
| 20.0 | 30.0 | app1 | True | 194560.0 | 33.3% | 63.1% | 29.8 |
| 20.0 | 30.0 | app2 | True | 58208.0 | 33.3% | 18.9% | -14.4 |
| 20.0 | 30.0 | app3 | True | 55384.0 | 33.3% | 18.0% | -15.4 |
| 30.0 | 40.0 | app1 | True | 169012.0 | 33.3% | 55.6% | 22.2 |
| 30.0 | 40.0 | app2 | True | 62232.0 | 33.3% | 20.5% | -12.9 |
| 30.0 | 40.0 | app3 | True | 73004.0 | 33.3% | 24.0% | -9.3 |
| 40.0 | 50.0 | app1 | True | 197454.0 | 33.3% | 69.2% | 35.9 |
| 40.0 | 50.0 | app2 | True | 48628.0 | 33.3% | 17.0% | -16.3 |
| 40.0 | 50.0 | app3 | True | 39228.0 | 33.3% | 13.7% | -19.6 |
| 50.0 | 60.0 | app1 | True | 198856.0 | 33.3% | 66.5% | 33.2 |
| 50.0 | 60.0 | app2 | True | 50080.0 | 33.3% | 16.7% | -16.6 |
| 50.0 | 60.0 | app3 | True | 50072.0 | 33.3% | 16.7% | -16.6 |
| 60.0 | 70.0 | app1 | True | 217898.0 | 33.3% | 73.5% | 40.2 |
| 60.0 | 70.0 | app2 | True | 40594.0 | 33.3% | 13.7% | -19.6 |
| 60.0 | 70.0 | app3 | True | 37852.0 | 33.3% | 12.8% | -20.6 |
| 70.0 | 80.0 | app1 | True | 201486.0 | 33.3% | 69.0% | 35.6 |
| 70.0 | 80.0 | app2 | True | 45984.0 | 33.3% | 15.7% | -17.6 |
| 70.0 | 80.0 | app3 | True | 44648.0 | 33.3% | 15.3% | -18.0 |
| 80.0 | 90.0 | app1 | True | 190598.0 | 33.3% | 69.1% | 35.8 |
| 80.0 | 90.0 | app2 | True | 43324.0 | 33.3% | 15.7% | -17.6 |
| 80.0 | 90.0 | app3 | True | 41944.0 | 33.3% | 15.2% | -18.1 |
| 90.0 | 100.0 | app1 | True | 186816.0 | 33.3% | 61.4% | 28.1 |
| 90.0 | 100.0 | app2 | True | 56740.0 | 33.3% | 18.6% | -14.7 |
| 90.0 | 100.0 | app3 | True | 60760.0 | 33.3% | 20.0% | -13.4 |
| 100.0 | 110.0 | app1 | True | 201530.0 | 33.3% | 67.7% | 34.4 |
| 100.0 | 110.0 | app2 | True | 51460.0 | 33.3% | 17.3% | -16.0 |
| 100.0 | 110.0 | app3 | True | 44730.0 | 33.3% | 15.0% | -18.3 |
| 110.0 | 120.0 | app1 | True | 182436.0 | 33.3% | 66.1% | 32.8 |
| 110.0 | 120.0 | app2 | True | 47404.0 | 33.3% | 17.2% | -16.1 |
| 110.0 | 120.0 | app3 | True | 45994.0 | 33.3% | 16.7% | -16.7 |
| 120.0 | 130.0 | app1 | True | 223122.0 | 33.3% | 72.7% | 39.4 |
| 120.0 | 130.0 | app2 | True | 43232.0 | 33.3% | 14.1% | -19.2 |
| 120.0 | 130.0 | app3 | True | 40588.0 | 33.3% | 13.2% | -20.1 |
| 130.0 | 140.0 | app1 | True | 207002.0 | 33.3% | 68.6% | 35.3 |
| 130.0 | 140.0 | app2 | True | 48722.0 | 33.3% | 16.1% | -17.2 |
| 130.0 | 140.0 | app3 | True | 45998.0 | 33.3% | 15.2% | -18.1 |
| 140.0 | 151.0 | app1 | True | 195866.0 | 33.3% | 64.7% | 31.4 |
| 140.0 | 151.0 | app2 | True | 54208.0 | 33.3% | 17.9% | -15.4 |
| 140.0 | 151.0 | app3 | True | 52728.0 | 33.3% | 17.4% | -15.9 |
| 151.0 | 161.0 | app1 | True | 194874.0 | 33.3% | 64.3% | 31.0 |
| 151.0 | 161.0 | app2 | True | 54062.0 | 33.3% | 17.8% | -15.5 |
| 151.0 | 161.0 | app3 | True | 54108.0 | 33.3% | 17.9% | -15.5 |
| 161.0 | 171.0 | app1 | True | 200154.0 | 33.3% | 67.0% | 33.6 |
| 161.0 | 171.0 | app2 | True | 48772.0 | 33.3% | 16.3% | -17.0 |
| 161.0 | 171.0 | app3 | True | 49988.0 | 33.3% | 16.7% | -16.6 |
| 171.0 | 181.0 | app1 | True | 206998.0 | 33.3% | 68.6% | 35.3 |
| 171.0 | 181.0 | app2 | True | 48630.0 | 33.3% | 16.1% | -17.2 |
| 171.0 | 181.0 | app3 | True | 46042.0 | 33.3% | 15.3% | -18.1 |
| 181.0 | 191.0 | app1 | True | 170426.0 | 33.3% | 55.8% | 22.4 |
| 181.0 | 191.0 | app2 | True | 70316.0 | 33.3% | 23.0% | -10.3 |
| 181.0 | 191.0 | app3 | True | 64932.0 | 33.3% | 21.2% | -12.1 |
| 191.0 | 201.0 | app1 | True | 216410.0 | 33.3% | 71.1% | 37.8 |
| 191.0 | 201.0 | app2 | True | 41964.0 | 33.3% | 13.8% | -19.5 |
| 191.0 | 201.0 | app3 | True | 45900.0 | 33.3% | 15.1% | -18.2 |
| 201.0 | 211.0 | app1 | True | 183890.0 | 33.3% | 61.0% | 27.7 |
| 201.0 | 211.0 | app2 | True | 62170.0 | 33.3% | 20.6% | -12.7 |
| 201.0 | 211.0 | app3 | True | 55448.0 | 33.3% | 18.4% | -14.9 |
| 211.0 | 221.0 | app1 | True | 190632.0 | 33.3% | 68.4% | 35.1 |
| 211.0 | 221.0 | app2 | True | 44678.0 | 33.3% | 16.0% | -17.3 |
| 211.0 | 221.0 | app3 | True | 43254.0 | 33.3% | 15.5% | -17.8 |
| 221.0 | 231.0 | app1 | True | 186716.0 | 33.3% | 60.6% | 27.2 |
| 221.0 | 231.0 | app2 | True | 64814.0 | 33.3% | 21.0% | -12.3 |
| 221.0 | 231.0 | app3 | True | 56672.0 | 33.3% | 18.4% | -14.9 |
| 231.0 | 241.0 | app1 | True | 185234.0 | 33.3% | 61.1% | 27.8 |
| 231.0 | 241.0 | app2 | True | 60904.0 | 33.3% | 20.1% | -13.2 |
| 231.0 | 241.0 | app3 | True | 56834.0 | 33.3% | 18.8% | -14.6 |
| 241.0 | 251.0 | app1 | False | 186694.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 45996.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | 43310.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 493.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 493.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 493.0 | app3 | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 135 | 0ms | 88ms | 246ms |
| 0.0 | 10.0 | app2 | ok | 34 | 0ms | 0ms | 224ms |
| 0.0 | 10.0 | app3 | ok | 33 | 0ms | 126ms | 238ms |
| 10.0 | 20.0 | app1 | ok | 167 | 1362ms | 4114ms | 8330ms |
| 10.0 | 20.0 | app2 | ok | 58 | 1975ms | 4882ms | 9420ms |
| 10.0 | 20.0 | app3 | ok | 48 | 1300ms | 4654ms | 9200ms |
| 20.0 | 30.0 | app1 | ok | 107 | 4172ms | 8019ms | 9802ms |
| 20.0 | 30.0 | app2 | ok | 40 | 1522ms | 3000ms | 4800ms |
| 20.0 | 30.0 | app3 | ok | 42 | 1900ms | 4192ms | 4919ms |
| 30.0 | 40.0 | app1 | ok | 161 | 3981ms | 8128ms | 9813ms |
| 30.0 | 40.0 | app2 | ok | 36 | 2000ms | 4357ms | 4936ms |
| 30.0 | 40.0 | app3 | ok | 42 | 1840ms | 3950ms | 4895ms |
| 40.0 | 50.0 | app1 | ok | 130 | 3388ms | 5938ms | 9594ms |
| 40.0 | 50.0 | app2 | ok | 34 | 2300ms | 4571ms | 8300ms |
| 40.0 | 50.0 | app3 | ok | 33 | 3125ms | 4625ms | 4962ms |
| 50.0 | 60.0 | app1 | ok | 173 | 3277ms | 4836ms | 9135ms |
| 50.0 | 60.0 | app2 | ok | 39 | 3155ms | 5125ms | 9512ms |
| 50.0 | 60.0 | app3 | ok | 38 | 3182ms | 4909ms | 9367ms |
| 60.0 | 70.0 | app1 | ok | 93 | 2223ms | 4388ms | 4939ms |
| 60.0 | 70.0 | app2 | ok | 32 | 4265ms | 8545ms | 9855ms |
| 60.0 | 70.0 | app3 | ok | 31 | 4191ms | 8450ms | 9845ms |
| 70.0 | 80.0 | app1 | ok | 207 | 2979ms | 4914ms | 9391ms |
| 70.0 | 80.0 | app2 | ok | 45 | 3011ms | 5500ms | 9550ms |
| 70.0 | 80.0 | app3 | ok | 44 | 2656ms | 6857ms | 9686ms |
| 80.0 | 90.0 | app1 | ok | 155 | 3297ms | 6630ms | 9663ms |
| 80.0 | 90.0 | app2 | ok | 23 | 2946ms | 4589ms | 4959ms |
| 80.0 | 90.0 | app3 | ok | 24 | 2857ms | 4571ms | 4957ms |
| 90.0 | 100.0 | app1 | ok | 114 | 3984ms | 6833ms | 9683ms |
| 90.0 | 100.0 | app2 | ok | 41 | 1911ms | 4771ms | 9317ms |
| 90.0 | 100.0 | app3 | ok | 39 | 1792ms | 4719ms | 9350ms |
| 100.0 | 110.0 | app1 | ok | 120 | 4706ms | 8846ms | 9885ms |
| 100.0 | 110.0 | app2 | ok | 39 | 1750ms | 3607ms | 4861ms |
| 100.0 | 110.0 | app3 | ok | 39 | 1829ms | 4114ms | 4911ms |
| 110.0 | 120.0 | app1 | ok | 153 | 2793ms | 6175ms | 9618ms |
| 110.0 | 120.0 | app2 | ok | 42 | 3026ms | 6500ms | 9650ms |
| 110.0 | 120.0 | app3 | ok | 40 | 3026ms | 6000ms | 9600ms |
| 120.0 | 130.0 | app1 | ok | 197 | 2183ms | 4399ms | 4940ms |
| 120.0 | 130.0 | app2 | ok | 20 | 6429ms | 9286ms | 9929ms |
| 120.0 | 130.0 | app3 | ok | 19 | 6042ms | 9208ms | 9921ms |
| 130.0 | 140.0 | app1 | ok | 117 | 3688ms | 4858ms | 9025ms |
| 130.0 | 140.0 | app2 | ok | 38 | 3409ms | 8417ms | 9842ms |
| 130.0 | 140.0 | app3 | ok | 37 | 3365ms | 8150ms | 9815ms |
| 140.0 | 151.0 | app1 | ok | 176 | 3582ms | 7333ms | 9733ms |
| 140.0 | 151.0 | app2 | ok | 30 | 1682ms | 4167ms | 4917ms |
| 140.0 | 151.0 | app3 | ok | 30 | 1500ms | 4167ms | 4917ms |
| 151.0 | 161.0 | app1 | ok | 134 | 3636ms | 4855ms | 9043ms |
| 151.0 | 161.0 | app2 | ok | 38 | 3824ms | 8273ms | 9827ms |
| 151.0 | 161.0 | app3 | ok | 38 | 3235ms | 7286ms | 9729ms |
| 161.0 | 171.0 | app1 | ok | 121 | 3939ms | 7479ms | 9748ms |
| 161.0 | 171.0 | app2 | ok | 49 | 2656ms | 4698ms | 8775ms |
| 161.0 | 171.0 | app3 | ok | 47 | 2398ms | 4663ms | 8825ms |
| 171.0 | 181.0 | app1 | ok | 156 | 3430ms | 6750ms | 9675ms |
| 171.0 | 181.0 | app2 | ok | 45 | 2837ms | 4567ms | 4957ms |
| 171.0 | 181.0 | app3 | ok | 43 | 2989ms | 4859ms | 9283ms |
| 181.0 | 191.0 | app1 | ok | 158 | 4004ms | 7531ms | 9753ms |
| 181.0 | 191.0 | app2 | ok | 38 | 2235ms | 4406ms | 4941ms |
| 181.0 | 191.0 | app3 | ok | 38 | 2342ms | 4441ms | 4944ms |
| 191.0 | 201.0 | app1 | ok | 140 | 3333ms | 4943ms | 9417ms |
| 191.0 | 201.0 | app2 | ok | 45 | 2015ms | 4338ms | 4934ms |
| 191.0 | 201.0 | app3 | ok | 45 | 1984ms | 4338ms | 4934ms |
| 201.0 | 211.0 | app1 | ok | 151 | 3939ms | 6980ms | 9698ms |
| 201.0 | 211.0 | app2 | ok | 37 | 2266ms | 4422ms | 4942ms |
| 201.0 | 211.0 | app3 | ok | 33 | 3125ms | 4625ms | 4962ms |
| 211.0 | 221.0 | app1 | ok | 186 | 3537ms | 5571ms | 9557ms |
| 211.0 | 221.0 | app2 | ok | 40 | 2738ms | 4643ms | 8000ms |
| 211.0 | 221.0 | app3 | ok | 38 | 2406ms | 4472ms | 4947ms |
| 221.0 | 231.0 | app1 | ok | 104 | 3804ms | 4935ms | 9350ms |
| 221.0 | 231.0 | app2 | ok | 35 | 3098ms | 4620ms | 4962ms |
| 221.0 | 231.0 | app3 | ok | 47 | 3164ms | 4633ms | 4963ms |
| 231.0 | 241.0 | app1 | ok | 144 | 3818ms | 6400ms | 9640ms |
| 231.0 | 241.0 | app2 | ok | 34 | 3095ms | 4714ms | 8300ms |
| 231.0 | 241.0 | app3 | ok | 27 | 2125ms | 4575ms | 8650ms |
| 241.0 | 251.0 | app1 | ok | 49 | 3806ms | 4894ms | 9183ms |
| 241.0 | 251.0 | app2 | ok | 30 | 4130ms | 7857ms | 9786ms |
| 241.0 | 251.0 | app3 | ok | 17 | 2250ms | 7167ms | 9717ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 493.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 493.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 493.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 4372650 | 217656 | 4581249.0 | -0.2% | 4603704.0 | 4807962.0 | -4.2% | True |
| app2 | 1161120 | 57934 | 1216466.0 | -0.2% | 1228288.0 | 1276988.0 | -3.8% | True |
| app3 | 1121760 | 55734 | 1174906.0 | -0.2% | 1188596.0 | 1233228.0 | -3.6% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 3593 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 952 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 924 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5413). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5413 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 471146 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
