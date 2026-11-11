# Fairness benchmark: full-contention-2x-discriminating (uni226-equal-weight-equal-load-noise-floor)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 0.0 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 0.0 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-689fd95c45-rwxj6` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-10T22:43:22Z` |
| Run end | `2026-11-10T22:50:53Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 1.0 | 256 | 1739 | 000=1, 200=1713, 500=25 | 38.4 | 49.1 | 2219472.0 | 33.3% | 33.3% | 0.0 | 33.5% | 0.1 | 33.2% | -0.1 | 42.0s | 0.0% | 1704.0 |
| app2 | 1.0 | 256 | 1742 | 000=3, 200=1715, 500=24 | 38.2 | 49.1 | 2195880.0 | 33.3% | 33.3% | 0.0 | 33.1% | -0.2 | 33.3% | -0.0 | 42.0s | 0.0% | 1711.0 |
| end-users | 1.0 | 256 | 1752 | 000=3, 200=1724, 500=25 | 38.2 | 49.1 | 2213764.0 | 33.3% | 33.3% | 0.0 | 33.4% | 0.1 | 33.5% | 0.1 | 42.0s | 0.0% | 1717.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 36486.0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.1s | 0.0% | 27.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 20.0 | 20.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (45 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 0.0 | 10.0 | app2 | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 0.0 | 10.0 | end-users | True | 0.0 | 33.3% | 0.0% | -33.3 |
| 10.0 | 20.0 | app1 | True | 32372.0 | 33.3% | 55.7% | 22.4 |
| 10.0 | 20.0 | app2 | True | 6758.0 | 33.3% | 11.6% | -21.7 |
| 10.0 | 20.0 | end-users | True | 18966.0 | 33.3% | 32.6% | -0.7 |
| 20.0 | 30.0 | app1 | True | 67580.0 | 33.3% | 30.7% | -2.6 |
| 20.0 | 30.0 | app2 | True | 72832.0 | 33.3% | 33.1% | -0.2 |
| 20.0 | 30.0 | end-users | True | 79676.0 | 33.3% | 36.2% | 2.9 |
| 30.0 | 40.0 | app1 | True | 79756.0 | 33.3% | 32.1% | -1.3 |
| 30.0 | 40.0 | app2 | True | 85122.0 | 33.3% | 34.2% | 0.9 |
| 30.0 | 40.0 | end-users | True | 83870.0 | 33.3% | 33.7% | 0.4 |
| 40.0 | 50.0 | app1 | True | 90442.0 | 33.3% | 33.8% | 0.5 |
| 40.0 | 50.0 | app2 | True | 91866.0 | 33.3% | 34.4% | 1.0 |
| 40.0 | 50.0 | end-users | True | 84986.0 | 33.3% | 31.8% | -1.5 |
| 50.0 | 60.0 | app1 | True | 96036.0 | 33.3% | 33.3% | 0.0 |
| 50.0 | 60.0 | app2 | True | 94684.0 | 33.3% | 32.9% | -0.5 |
| 50.0 | 60.0 | end-users | True | 97300.0 | 33.3% | 33.8% | 0.4 |
| 60.0 | 70.0 | app1 | True | 104010.0 | 33.3% | 33.6% | 0.3 |
| 60.0 | 70.0 | app2 | True | 104008.0 | 33.3% | 33.6% | 0.3 |
| 60.0 | 70.0 | end-users | True | 101496.0 | 33.3% | 32.8% | -0.5 |
| 70.0 | 80.0 | app1 | True | 98510.0 | 33.3% | 32.9% | -0.5 |
| 70.0 | 80.0 | app2 | True | 99910.0 | 33.3% | 33.3% | 0.0 |
| 70.0 | 80.0 | end-users | True | 101306.0 | 33.3% | 33.8% | 0.5 |
| 80.0 | 90.0 | app1 | True | 56824.0 | 33.3% | 33.3% | 0.0 |
| 80.0 | 90.0 | app2 | True | 56880.0 | 33.3% | 33.4% | 0.0 |
| 80.0 | 90.0 | end-users | True | 56730.0 | 33.3% | 33.3% | -0.0 |
| 90.0 | 100.0 | app1 | True | 51396.0 | 33.3% | 33.4% | 0.0 |
| 90.0 | 100.0 | app2 | True | 51342.0 | 33.3% | 33.3% | -0.0 |
| 90.0 | 100.0 | end-users | True | 51364.0 | 33.3% | 33.3% | -0.0 |
| 100.0 | 111.0 | app1 | True | 81130.0 | 33.3% | 33.7% | 0.4 |
| 100.0 | 111.0 | app2 | True | 78348.0 | 33.3% | 32.6% | -0.8 |
| 100.0 | 111.0 | end-users | True | 81084.0 | 33.3% | 33.7% | 0.4 |
| 111.0 | 121.0 | app1 | True | 74478.0 | 33.3% | 34.0% | 0.7 |
| 111.0 | 121.0 | app2 | True | 72974.0 | 33.3% | 33.3% | -0.0 |
| 111.0 | 121.0 | end-users | True | 71508.0 | 33.3% | 32.7% | -0.7 |
| 121.0 | 131.0 | app1 | True | 82472.0 | 33.3% | 33.0% | -0.4 |
| 121.0 | 131.0 | app2 | True | 82406.0 | 33.3% | 32.9% | -0.4 |
| 121.0 | 131.0 | end-users | True | 85290.0 | 33.3% | 34.1% | 0.8 |
| 131.0 | 141.0 | app1 | True | 84972.0 | 33.3% | 33.1% | -0.2 |
| 131.0 | 141.0 | app2 | True | 86440.0 | 33.3% | 33.7% | 0.4 |
| 131.0 | 141.0 | end-users | True | 85108.0 | 33.3% | 33.2% | -0.2 |
| 141.0 | 151.0 | app1 | True | 101374.0 | 33.3% | 32.8% | -0.5 |
| 141.0 | 151.0 | app2 | True | 102362.0 | 33.3% | 33.1% | -0.2 |
| 141.0 | 151.0 | end-users | True | 105476.0 | 33.3% | 34.1% | 0.8 |
| 151.0 | 161.0 | app1 | True | 101404.0 | 33.3% | 33.2% | -0.1 |
| 151.0 | 161.0 | app2 | True | 104034.0 | 33.3% | 34.1% | 0.7 |
| 151.0 | 161.0 | end-users | True | 99900.0 | 33.3% | 32.7% | -0.6 |
| 161.0 | 171.0 | app1 | True | 103972.0 | 33.3% | 34.4% | 1.1 |
| 161.0 | 171.0 | app2 | True | 98094.0 | 33.3% | 32.5% | -0.8 |
| 161.0 | 171.0 | end-users | True | 99798.0 | 33.3% | 33.1% | -0.3 |
| 171.0 | 181.0 | app1 | True | 87490.0 | 33.3% | 33.4% | 0.1 |
| 171.0 | 181.0 | app2 | True | 87642.0 | 33.3% | 33.5% | 0.2 |
| 171.0 | 181.0 | end-users | True | 86452.0 | 33.3% | 33.0% | -0.3 |
| 181.0 | 191.0 | app1 | True | 80878.0 | 33.3% | 33.1% | -0.2 |
| 181.0 | 191.0 | app2 | True | 82424.0 | 33.3% | 33.8% | 0.4 |
| 181.0 | 191.0 | end-users | True | 80800.0 | 33.3% | 33.1% | -0.2 |
| 191.0 | 201.0 | app1 | True | 81112.0 | 33.3% | 33.5% | 0.2 |
| 191.0 | 201.0 | app2 | True | 81194.0 | 33.3% | 33.6% | 0.2 |
| 191.0 | 201.0 | end-users | True | 79556.0 | 33.3% | 32.9% | -0.4 |
| 201.0 | 211.0 | app1 | True | 102734.0 | 33.3% | 34.0% | 0.6 |
| 201.0 | 211.0 | app2 | True | 94484.0 | 33.3% | 31.2% | -2.1 |
| 201.0 | 211.0 | end-users | True | 105356.0 | 33.3% | 34.8% | 1.5 |
| 211.0 | 221.0 | app1 | True | 56644.0 | 33.3% | 32.5% | -0.8 |
| 211.0 | 221.0 | app2 | True | 63526.0 | 33.3% | 36.4% | 3.1 |
| 211.0 | 221.0 | end-users | True | 54190.0 | 33.3% | 31.1% | -2.3 |
| 221.0 | 231.0 | app1 | True | 75704.0 | 33.3% | 32.6% | -0.8 |
| 221.0 | 231.0 | app2 | True | 77042.0 | 33.3% | 33.1% | -0.2 |
| 221.0 | 231.0 | end-users | True | 79692.0 | 33.3% | 34.3% | 1.0 |
| 231.0 | 241.0 | app1 | True | 82318.0 | 33.3% | 34.1% | 0.7 |
| 231.0 | 241.0 | app2 | True | 78294.0 | 33.3% | 32.4% | -0.9 |
| 231.0 | 241.0 | end-users | True | 80974.0 | 33.3% | 33.5% | 0.2 |
| 241.0 | 251.0 | app1 | False | 78476.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 85104.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 79704.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 80914.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 79692.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 80676.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 82490.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 82406.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 81126.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 101270.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 91946.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | False | 98696.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | 2714.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | 4066.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | False | 2684.0 | n/a | n/a | n/a |
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
| 371.0 | 382.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 382.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 382.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 442.0 | 451.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 442.0 | 451.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 442.0 | 451.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 11 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 19 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 27 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 92 | 0ms | 1120ms | 2362ms |
| 10.0 | 20.0 | app2 | ok | 96 | 0ms | 1060ms | 2356ms |
| 10.0 | 20.0 | end-users | ok | 90 | 0ms | 1375ms | 2387ms |
| 20.0 | 30.0 | app1 | ok | 101 | 5570ms | 9114ms | 9911ms |
| 20.0 | 30.0 | app2 | ok | 101 | 5720ms | 9144ms | 9914ms |
| 20.0 | 30.0 | end-users | ok | 103 | 4526ms | 8880ms | 9888ms |
| 30.0 | 40.0 | app1 | ok | 57 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | app2 | ok | 57 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | end-users | ok | 57 | 13235ms | 26647ms | 29665ms |
| 40.0 | 50.0 | app1 | ok | 43 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app2 | ok | 43 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | end-users | ok | 43 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app1 | ok | 86 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app2 | ok | 86 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | end-users | ok | 87 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app1 | ok | 44 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | app2 | ok | 43 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | end-users | ok | 42 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app1 | ok | 156 | 23000ms | 47000ms | 58700ms |
| 70.0 | 80.0 | app2 | ok | 156 | 22893ms | 46629ms | 58663ms |
| 70.0 | 80.0 | end-users | ok | 155 | 23362ms | 48077ms | 58808ms |
| 80.0 | 90.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 100.0 | 111.0 | app1 | ok | 75 | 45000ms | 57000ms | 59700ms |
| 100.0 | 111.0 | app2 | ok | 76 | 45000ms | 57000ms | 59700ms |
| 100.0 | 111.0 | end-users | ok | 76 | 45000ms | 57000ms | 59700ms |
| 111.0 | 121.0 | app1 | ok | 57 | 45000ms | 57000ms | 59700ms |
| 111.0 | 121.0 | app2 | ok | 57 | 45000ms | 57000ms | 59700ms |
| 111.0 | 121.0 | end-users | ok | 58 | 45000ms | 57000ms | 59700ms |
| 121.0 | 131.0 | app1 | ok | 58 | 45000ms | 57000ms | 59700ms |
| 121.0 | 131.0 | app2 | ok | 58 | 45000ms | 57000ms | 59700ms |
| 121.0 | 131.0 | end-users | ok | 57 | 45000ms | 57000ms | 59700ms |
| 131.0 | 141.0 | app1 | ok | 77 | 45000ms | 57000ms | 59700ms |
| 131.0 | 141.0 | app2 | ok | 76 | 45000ms | 57000ms | 59700ms |
| 131.0 | 141.0 | end-users | ok | 77 | 45000ms | 57000ms | 59700ms |
| 141.0 | 151.0 | app1 | ok | 52 | 41860ms | 56372ms | 59637ms |
| 141.0 | 151.0 | app2 | ok | 52 | 41860ms | 56372ms | 59637ms |
| 141.0 | 151.0 | end-users | ok | 51 | 41341ms | 56268ms | 59627ms |
| 151.0 | 161.0 | app1 | ok | 74 | 42381ms | 56476ms | 59648ms |
| 151.0 | 161.0 | app2 | ok | 73 | 42339ms | 56468ms | 59647ms |
| 151.0 | 161.0 | end-users | ok | 74 | 41500ms | 56300ms | 59630ms |
| 161.0 | 171.0 | app1 | ok | 86 | 23651ms | 48783ms | 58878ms |
| 161.0 | 171.0 | app2 | ok | 86 | 23030ms | 47100ms | 58710ms |
| 161.0 | 171.0 | end-users | ok | 86 | 23030ms | 47100ms | 58710ms |
| 171.0 | 181.0 | app1 | ok | 55 | 22791ms | 46250ms | 58625ms |
| 171.0 | 181.0 | app2 | ok | 56 | 22444ms | 44727ms | 58473ms |
| 171.0 | 181.0 | end-users | ok | 55 | 23415ms | 48214ms | 58821ms |
| 181.0 | 191.0 | app1 | ok | 59 | 25946ms | 51955ms | 59195ms |
| 181.0 | 191.0 | app2 | ok | 60 | 26667ms | 52500ms | 59250ms |
| 181.0 | 191.0 | end-users | ok | 59 | 26857ms | 52625ms | 59262ms |
| 191.0 | 201.0 | app1 | ok | 93 | 43193ms | 56639ms | 59664ms |
| 191.0 | 201.0 | app2 | ok | 92 | 41096ms | 56219ms | 59622ms |
| 191.0 | 201.0 | end-users | ok | 93 | 41883ms | 56377ms | 59638ms |
| 201.0 | 211.0 | app1 | ok | 71 | 37812ms | 55562ms | 59556ms |
| 201.0 | 211.0 | app2 | ok | 72 | 37500ms | 55500ms | 59550ms |
| 201.0 | 211.0 | end-users | ok | 73 | 38100ms | 55620ms | 59562ms |
| 211.0 | 221.0 | app1 | ok | 77 | 40424ms | 56085ms | 59608ms |
| 211.0 | 221.0 | app2 | ok | 76 | 39643ms | 55929ms | 59593ms |
| 211.0 | 221.0 | end-users | ok | 75 | 39167ms | 55833ms | 59583ms |
| 221.0 | 231.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 57 | 45000ms | 57000ms | 59700ms |
| 231.0 | 241.0 | app2 | ok | 57 | 45000ms | 57000ms | 59700ms |
| 231.0 | 241.0 | end-users | ok | 58 | 45000ms | 57000ms | 59700ms |
| 241.0 | 251.0 | app1 | ok | 56 | 45000ms | 57000ms | 59700ms |
| 241.0 | 251.0 | app2 | ok | 57 | 45000ms | 57000ms | 59700ms |
| 241.0 | 251.0 | end-users | ok | 56 | 45000ms | 57000ms | 59700ms |
| 251.0 | 261.0 | app1 | ok | 56 | 45000ms | 57000ms | 59700ms |
| 251.0 | 261.0 | app2 | ok | 55 | 45000ms | 57000ms | 59700ms |
| 251.0 | 261.0 | end-users | ok | 56 | 45000ms | 57000ms | 59700ms |
| 261.0 | 271.0 | app1 | ok | 96 | 44516ms | 56903ms | 59690ms |
| 261.0 | 271.0 | app2 | ok | 97 | 43833ms | 56767ms | 59677ms |
| 261.0 | 271.0 | end-users | ok | 96 | 44176ms | 56835ms | 59684ms |
| 271.0 | 281.0 | app1 | ok | 15 | 45000ms | 57000ms | 59700ms |
| 271.0 | 281.0 | app2 | ok | 10 | 45000ms | 57000ms | 59700ms |
| 271.0 | 281.0 | end-users | ok | 13 | 45000ms | 57000ms | 59700ms |
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
| 371.0 | 382.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 382.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 382.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 382.0 | 392.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 392.0 | 402.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 402.0 | 412.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 451.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 451.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 451.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens +4501.5%
- app2 exceeded the 10% ledger tolerance: raw tokens +4539.5%
- end-users exceeded the 10% ledger tolerance: raw tokens +4535.6%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2106990 | 104779 | 101774889.0 | 4501.5% | 2219472.0 | 2316548.0 | -4.2% | False |
| app2 | 2109450 | 104761 | 102727762.0 | 4539.5% | 2195880.0 | 2318972.0 | -5.3% | False |
| end-users | 2120520 | 105351 | 103183103.0 | 4535.6% | 2213764.0 | 2331222.0 | -5.0% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1739 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1742 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1752 | 0 | 0 | 0 (never shed) | 0.00% | 33.3% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5159). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5159 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 433266 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1703 | 36267ms | 54032ms | ok | 78978 | 15ms | 36ms |
| app2 | ok | 1708 | 36141ms | 53563ms | ok | 79732 | 15ms | 36ms |
| end-users | ok | 1714 | 36100ms | 53540ms | ok | 80091 | 15ms | 36ms |
| **pool (all groups)** | ok | 5152 | 36108ms | 53686ms | ok | 239979 | 15ms | 36ms |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (45 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 45ms | 520ms | ok | 13ms | 20ms |
| 0.0 | 10.0 | app2 | ok | 57ms | 260ms | ok | 14ms | 22ms |
| 0.0 | 10.0 | end-users | ok | 73ms | 397ms | ok | 13ms | 21ms |
| 10.0 | 20.0 | app1 | ok | 1750ms | 4240ms | ok | 16ms | 39ms |
| 10.0 | 20.0 | app2 | ok | 940ms | 3544ms | ok | 16ms | 40ms |
| 10.0 | 20.0 | end-users | ok | 1425ms | 3825ms | ok | 16ms | 40ms |
| 20.0 | 30.0 | app1 | ok | 7778ms | 13611ms | ok | 15ms | 38ms |
| 20.0 | 30.0 | app2 | ok | 7636ms | 12300ms | ok | 15ms | 38ms |
| 20.0 | 30.0 | end-users | ok | 6647ms | 10083ms | ok | 14ms | 37ms |
| 30.0 | 40.0 | app1 | ok | 13782ms | 19262ms | ok | 15ms | 37ms |
| 30.0 | 40.0 | app2 | ok | 13631ms | 19212ms | ok | 15ms | 37ms |
| 30.0 | 40.0 | end-users | ok | 12500ms | 16900ms | ok | 15ms | 37ms |
| 40.0 | 50.0 | app1 | ok | 19085ms | 28712ms | ok | 15ms | 37ms |
| 40.0 | 50.0 | app2 | ok | 18953ms | 28640ms | ok | 15ms | 36ms |
| 40.0 | 50.0 | end-users | ok | 17318ms | 19895ms | ok | 15ms | 37ms |
| 50.0 | 60.0 | app1 | ok | 25000ms | 29500ms | ok | 15ms | 36ms |
| 50.0 | 60.0 | app2 | ok | 25000ms | 29500ms | ok | 15ms | 36ms |
| 50.0 | 60.0 | end-users | ok | 24627ms | 29463ms | ok | 15ms | 36ms |
| 60.0 | 70.0 | app1 | ok | 26111ms | 40875ms | ok | 15ms | 38ms |
| 60.0 | 70.0 | app2 | ok | 26638ms | 41961ms | ok | 15ms | 37ms |
| 60.0 | 70.0 | end-users | ok | 26148ms | 40982ms | ok | 15ms | 38ms |
| 70.0 | 80.0 | app1 | ok | 37500ms | 44250ms | ok | 15ms | 37ms |
| 70.0 | 80.0 | app2 | ok | 37500ms | 44250ms | ok | 15ms | 37ms |
| 70.0 | 80.0 | end-users | ok | 37500ms | 44250ms | ok | 15ms | 37ms |
| 80.0 | 90.0 | app1 | ok | 37500ms | 44250ms | ok | 14ms | 20ms |
| 80.0 | 90.0 | app2 | ok | 37500ms | 44250ms | ok | 14ms | 20ms |
| 80.0 | 90.0 | end-users | ok | 37500ms | 44250ms | ok | 14ms | 20ms |
| 90.0 | 100.0 | app1 | ok | 37500ms | 44250ms | ok | 14ms | 19ms |
| 90.0 | 100.0 | app2 | ok | 37500ms | 44250ms | ok | 14ms | 19ms |
| 90.0 | 100.0 | end-users | ok | 37500ms | 44250ms | ok | 14ms | 19ms |
| 100.0 | 111.0 | app1 | ok | 40465ms | 57353ms | ok | 15ms | 35ms |
| 100.0 | 111.0 | app2 | ok | 40116ms | 57100ms | ok | 14ms | 33ms |
| 100.0 | 111.0 | end-users | ok | 39184ms | 55909ms | ok | 15ms | 35ms |
| 111.0 | 121.0 | app1 | ok | 51406ms | 59141ms | ok | 14ms | 33ms |
| 111.0 | 121.0 | app2 | ok | 51000ms | 59100ms | ok | 14ms | 34ms |
| 111.0 | 121.0 | end-users | ok | 51359ms | 59136ms | ok | 14ms | 34ms |
| 121.0 | 131.0 | app1 | ok | 52500ms | 59250ms | ok | 14ms | 34ms |
| 121.0 | 131.0 | app2 | ok | 52500ms | 59250ms | ok | 14ms | 34ms |
| 121.0 | 131.0 | end-users | ok | 52500ms | 59250ms | ok | 14ms | 34ms |
| 131.0 | 141.0 | app1 | ok | 48476ms | 58848ms | ok | 14ms | 33ms |
| 131.0 | 141.0 | app2 | ok | 48837ms | 58884ms | ok | 14ms | 33ms |
| 131.0 | 141.0 | end-users | ok | 48750ms | 58875ms | ok | 14ms | 34ms |
| 141.0 | 151.0 | app1 | ok | 37601ms | 44443ms | ok | 14ms | 36ms |
| 141.0 | 151.0 | app2 | ok | 37600ms | 44440ms | ok | 15ms | 37ms |
| 141.0 | 151.0 | end-users | ok | 37500ms | 44250ms | ok | 15ms | 37ms |
| 151.0 | 161.0 | app1 | ok | 37500ms | 44250ms | ok | 15ms | 37ms |
| 151.0 | 161.0 | app2 | ok | 37500ms | 44250ms | ok | 16ms | 37ms |
| 151.0 | 161.0 | end-users | ok | 37500ms | 44250ms | ok | 16ms | 37ms |
| 161.0 | 171.0 | app1 | ok | 37500ms | 44250ms | ok | 16ms | 38ms |
| 161.0 | 171.0 | app2 | ok | 37500ms | 44250ms | ok | 16ms | 39ms |
| 161.0 | 171.0 | end-users | ok | 37500ms | 44250ms | ok | 16ms | 39ms |
| 171.0 | 181.0 | app1 | ok | 37500ms | 44250ms | ok | 15ms | 38ms |
| 171.0 | 181.0 | app2 | ok | 37500ms | 44250ms | ok | 15ms | 38ms |
| 171.0 | 181.0 | end-users | ok | 37500ms | 44250ms | ok | 15ms | 38ms |
| 181.0 | 191.0 | app1 | ok | 37500ms | 44250ms | ok | 15ms | 37ms |
| 181.0 | 191.0 | app2 | ok | 37500ms | 44250ms | ok | 15ms | 38ms |
| 181.0 | 191.0 | end-users | ok | 37500ms | 44250ms | ok | 15ms | 37ms |
| 191.0 | 201.0 | app1 | ok | 37500ms | 44250ms | ok | 14ms | 35ms |
| 191.0 | 201.0 | app2 | ok | 37500ms | 44250ms | ok | 15ms | 35ms |
| 191.0 | 201.0 | end-users | ok | 37500ms | 44250ms | ok | 15ms | 36ms |
| 201.0 | 211.0 | app1 | ok | 37500ms | 44250ms | ok | 17ms | 39ms |
| 201.0 | 211.0 | app2 | ok | 37500ms | 44250ms | ok | 16ms | 39ms |
| 201.0 | 211.0 | end-users | ok | 37500ms | 44250ms | ok | 17ms | 39ms |
| 211.0 | 221.0 | app1 | ok | 37500ms | 44250ms | ok | 14ms | 26ms |
| 211.0 | 221.0 | app2 | ok | 37500ms | 44250ms | ok | 14ms | 28ms |
| 211.0 | 221.0 | end-users | ok | 37500ms | 44250ms | ok | 14ms | 24ms |
| 221.0 | 231.0 | app1 | ok | 37778ms | 44778ms | ok | 14ms | 33ms |
| 221.0 | 231.0 | app2 | ok | 37500ms | 44250ms | ok | 14ms | 32ms |
| 221.0 | 231.0 | end-users | ok | 37500ms | 44250ms | ok | 14ms | 32ms |
| 231.0 | 241.0 | app1 | ok | 39337ms | 56187ms | ok | 14ms | 34ms |
| 231.0 | 241.0 | app2 | ok | 37768ms | 44759ms | ok | 14ms | 35ms |
| 231.0 | 241.0 | end-users | ok | 37895ms | 45000ms | ok | 14ms | 33ms |
| 241.0 | 251.0 | app1 | ok | 38878ms | 55167ms | ok | 15ms | 34ms |
| 241.0 | 251.0 | app2 | ok | 39844ms | 56850ms | ok | 14ms | 31ms |
| 241.0 | 251.0 | end-users | ok | 39219ms | 55977ms | ok | 15ms | 33ms |
| 251.0 | 261.0 | app1 | ok | 41538ms | 57857ms | ok | 14ms | 32ms |
| 251.0 | 261.0 | app2 | ok | 40536ms | 57397ms | ok | 14ms | 32ms |
| 251.0 | 261.0 | end-users | ok | 42162ms | 58043ms | ok | 14ms | 30ms |
| 261.0 | 271.0 | app1 | ok | 37754ms | 44733ms | ok | 14ms | 29ms |
| 261.0 | 271.0 | app2 | ok | 37500ms | 44250ms | ok | 14ms | 29ms |
| 261.0 | 271.0 | end-users | ok | 37500ms | 44250ms | ok | 14ms | 28ms |
| 271.0 | 281.0 | app1 | ok | 37500ms | 44250ms | ok | 14ms | 31ms |
| 271.0 | 281.0 | app2 | ok | 37500ms | 44250ms | ok | 14ms | 34ms |
| 271.0 | 281.0 | end-users | ok | 37500ms | 44250ms | ok | 14ms | 33ms |
| 281.0 | 291.0 | app1 | ok | 37500ms | 44250ms | ok | 15ms | 19ms |
| 281.0 | 291.0 | app2 | ok | 37500ms | 44250ms | ok | 15ms | 19ms |
| 281.0 | 291.0 | end-users | ok | 37500ms | 44250ms | ok | 15ms | 20ms |
| 291.0 | 301.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 291.0 | 301.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 291.0 | 301.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 301.0 | 311.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 301.0 | 311.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 301.0 | 311.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 311.0 | 321.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 311.0 | 321.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 311.0 | 321.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 321.0 | 331.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 321.0 | 331.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 321.0 | 331.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 331.0 | 341.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 331.0 | 341.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 331.0 | 341.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 341.0 | 351.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 341.0 | 351.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 341.0 | 351.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 351.0 | 361.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 351.0 | 361.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 351.0 | 361.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 361.0 | 371.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 361.0 | 371.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 361.0 | 371.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 371.0 | 382.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 371.0 | 382.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 371.0 | 382.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 382.0 | 392.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 382.0 | 392.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 382.0 | 392.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 392.0 | 402.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 392.0 | 402.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 392.0 | 402.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 402.0 | 412.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 402.0 | 412.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 402.0 | 412.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 412.0 | 422.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 412.0 | 422.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 412.0 | 422.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 422.0 | 432.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 422.0 | 432.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 422.0 | 432.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 432.0 | 442.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 432.0 | 442.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 432.0 | 442.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 442.0 | 451.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 442.0 | 451.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |
| 442.0 | 451.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
