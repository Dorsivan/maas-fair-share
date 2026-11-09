# Fairness benchmark: full-contention (uni-166-g1-accounting-leak)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-cd4d4` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T09:52:49Z` |
| Run end | `2026-11-09T09:58:11Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 549 | 200=367, 500=12 | 15.8 | 22.8 | 706072.0 | 21.1% | 16.7% | -4.4 | 16.6% | -4.5 | 2.6s | 98.9% | 528.0 |
| app2 | 10.0 | 32 | 475 | 200=457, 500=18 | 15.9 | 28.3 | 599102.0 | 10.5% | 14.1% | 3.6 | 14.4% | 3.8 | 2.0s | 98.9% | 453.0 |
| end-users | 65.0 | 128 | 2284 | 200=2221, 500=63 | 13.2 | 19.6 | 2930632.0 | 68.4% | 69.2% | 0.8 | 69.0% | 0.6 | 2.2s | 98.9% | 2206.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 32418.0 | n/a | n/a | n/a | n/a | n/a | 0.0s | 98.9% | 24.0 |

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
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (33 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 8112.0 | 21.1% | 15.4% | -5.7 |
| 0.0 | 10.0 | app2 | True | 5416.0 | 10.5% | 10.3% | -0.3 |
| 0.0 | 10.0 | end-users | True | 39184.0 | 68.4% | 74.3% | 5.9 |
| 10.0 | 20.0 | app1 | True | 35098.0 | 21.1% | 17.1% | -4.0 |
| 10.0 | 20.0 | app2 | True | 41986.0 | 10.5% | 20.4% | 9.9 |
| 10.0 | 20.0 | end-users | True | 128464.0 | 68.4% | 62.5% | -5.9 |
| 20.0 | 30.0 | app1 | True | 33838.0 | 21.1% | 20.9% | -0.2 |
| 20.0 | 30.0 | app2 | True | 21660.0 | 10.5% | 13.4% | 2.8 |
| 20.0 | 30.0 | end-users | True | 106746.0 | 68.4% | 65.8% | -2.6 |
| 30.0 | 40.0 | app1 | True | 6774.0 | 21.1% | 4.0% | -17.0 |
| 30.0 | 40.0 | app2 | True | 4036.0 | 10.5% | 2.4% | -8.1 |
| 30.0 | 40.0 | end-users | True | 158158.0 | 68.4% | 93.6% | 25.2 |
| 40.0 | 50.0 | app1 | True | 50086.0 | 21.1% | 29.4% | 8.3 |
| 40.0 | 50.0 | app2 | True | 55458.0 | 10.5% | 32.5% | 22.0 |
| 40.0 | 50.0 | end-users | True | 65058.0 | 68.4% | 38.1% | -30.3 |
| 50.0 | 60.0 | app1 | True | 26988.0 | 21.1% | 17.7% | -3.4 |
| 50.0 | 60.0 | app2 | True | 2716.0 | 10.5% | 1.8% | -8.7 |
| 50.0 | 60.0 | end-users | True | 123054.0 | 68.4% | 80.6% | 12.1 |
| 60.0 | 70.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 60.0 | 70.0 | app2 | True | 9448.0 | 10.5% | 5.3% | -5.3 |
| 60.0 | 70.0 | end-users | True | 170388.0 | 68.4% | 94.7% | 26.3 |
| 70.0 | 80.0 | app1 | True | 43358.0 | 21.1% | 17.8% | -3.2 |
| 70.0 | 80.0 | app2 | True | 32460.0 | 10.5% | 13.3% | 2.8 |
| 70.0 | 80.0 | end-users | True | 167474.0 | 68.4% | 68.8% | 0.4 |
| 80.0 | 90.0 | app1 | True | 8070.0 | 21.1% | 5.2% | -15.9 |
| 80.0 | 90.0 | app2 | True | 4056.0 | 10.5% | 2.6% | -7.9 |
| 80.0 | 90.0 | end-users | True | 143418.0 | 68.4% | 92.2% | 23.8 |
| 90.0 | 100.0 | app1 | True | 35126.0 | 21.1% | 20.5% | -0.6 |
| 90.0 | 100.0 | app2 | True | 39204.0 | 10.5% | 22.8% | 12.3 |
| 90.0 | 100.0 | end-users | True | 97326.0 | 68.4% | 56.7% | -11.7 |
| 100.0 | 110.0 | app1 | True | 43246.0 | 21.1% | 25.8% | 4.8 |
| 100.0 | 110.0 | app2 | True | 48656.0 | 10.5% | 29.0% | 18.5 |
| 100.0 | 110.0 | end-users | True | 75674.0 | 68.4% | 45.2% | -23.3 |
| 110.0 | 120.0 | app1 | True | 29766.0 | 21.1% | 19.6% | -1.4 |
| 110.0 | 120.0 | app2 | True | 8148.0 | 10.5% | 5.4% | -5.2 |
| 110.0 | 120.0 | end-users | True | 113658.0 | 68.4% | 75.0% | 6.6 |
| 120.0 | 130.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 120.0 | 130.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 120.0 | 130.0 | end-users | True | 166402.0 | 68.4% | 100.0% | 31.6 |
| 130.0 | 140.0 | app1 | True | 48668.0 | 21.1% | 28.2% | 7.1 |
| 130.0 | 140.0 | app2 | True | 62176.0 | 10.5% | 36.0% | 25.4 |
| 130.0 | 140.0 | end-users | True | 62002.0 | 68.4% | 35.9% | -32.5 |
| 140.0 | 150.0 | app1 | True | 36554.0 | 21.1% | 23.9% | 2.9 |
| 140.0 | 150.0 | app2 | True | 2716.0 | 10.5% | 1.8% | -8.7 |
| 140.0 | 150.0 | end-users | True | 113372.0 | 68.4% | 74.3% | 5.9 |
| 150.0 | 160.0 | app1 | True | 21654.0 | 21.1% | 12.7% | -8.3 |
| 150.0 | 160.0 | app2 | True | 43248.0 | 10.5% | 25.4% | 14.9 |
| 150.0 | 160.0 | end-users | True | 105344.0 | 68.4% | 61.9% | -6.5 |
| 160.0 | 170.0 | app1 | True | 22940.0 | 21.1% | 13.6% | -7.5 |
| 160.0 | 170.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 160.0 | 170.0 | end-users | True | 145988.0 | 68.4% | 86.4% | 18.0 |
| 170.0 | 180.0 | app1 | True | 39244.0 | 21.1% | 25.7% | 4.6 |
| 170.0 | 180.0 | app2 | True | 20282.0 | 10.5% | 13.3% | 2.7 |
| 170.0 | 180.0 | end-users | True | 93352.0 | 68.4% | 61.1% | -7.4 |
| 180.0 | 190.0 | app1 | True | 31110.0 | 21.1% | 18.6% | -2.5 |
| 180.0 | 190.0 | app2 | True | 44550.0 | 10.5% | 26.6% | 16.1 |
| 180.0 | 190.0 | end-users | True | 91968.0 | 68.4% | 54.9% | -13.6 |
| 190.0 | 200.0 | app1 | True | 12208.0 | 21.1% | 7.2% | -13.8 |
| 190.0 | 200.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 190.0 | 200.0 | end-users | True | 156778.0 | 68.4% | 92.8% | 24.4 |
| 200.0 | 211.0 | app1 | True | 43338.0 | 21.1% | 26.2% | 5.2 |
| 200.0 | 211.0 | app2 | True | 46054.0 | 10.5% | 27.9% | 17.4 |
| 200.0 | 211.0 | end-users | True | 75710.0 | 68.4% | 45.9% | -22.6 |
| 211.0 | 221.0 | app1 | True | 32372.0 | 21.1% | 20.3% | -0.7 |
| 211.0 | 221.0 | app2 | True | 20292.0 | 10.5% | 12.7% | 2.2 |
| 211.0 | 221.0 | end-users | True | 106654.0 | 68.4% | 66.9% | -1.5 |
| 221.0 | 231.0 | app1 | True | 10800.0 | 21.1% | 6.5% | -14.5 |
| 221.0 | 231.0 | app2 | True | 1340.0 | 10.5% | 0.8% | -9.7 |
| 221.0 | 231.0 | end-users | True | 152954.0 | 68.4% | 92.6% | 24.2 |
| 231.0 | 241.0 | app1 | True | 43346.0 | 21.1% | 25.0% | 4.0 |
| 231.0 | 241.0 | app2 | True | 43252.0 | 10.5% | 25.0% | 14.5 |
| 231.0 | 241.0 | end-users | True | 86486.0 | 68.4% | 50.0% | -18.5 |
| 241.0 | 251.0 | app1 | False | 2716.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 151220.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 40660.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 41948.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 33800.0 | n/a | n/a | n/a |
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
| 321.0 | 322.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 322.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 322.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 17 | 38ms | 650ms | 2245ms |
| 0.0 | 10.0 | app2 | ok | 15 | 194ms | 1938ms | 2444ms |
| 0.0 | 10.0 | end-users | ok | 76 | 25ms | 1464ms | 2396ms |
| 10.0 | 20.0 | app1 | ok | 51 | 2188ms | 7167ms | 9717ms |
| 10.0 | 20.0 | app2 | ok | 42 | 2050ms | 7667ms | 9767ms |
| 10.0 | 20.0 | end-users | ok | 196 | 2750ms | 7200ms | 9720ms |
| 20.0 | 30.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 32 | 7273ms | 23600ms | 29360ms |
| 30.0 | 40.0 | app2 | ok | 21 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | end-users | ok | 113 | 6731ms | 22710ms | 29271ms |
| 40.0 | 50.0 | app1 | ok | 25 | 1562ms | 3750ms | 4875ms |
| 40.0 | 50.0 | app2 | ok | 23 | 4583ms | 25818ms | 29582ms |
| 40.0 | 50.0 | end-users | ok | 125 | 9079ms | 25192ms | 29519ms |
| 50.0 | 60.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 32 | 8571ms | 24667ms | 29467ms |
| 60.0 | 70.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | end-users | ok | 224 | 5104ms | 9771ms | 27511ms |
| 70.0 | 80.0 | app1 | ok | 32 | 6522ms | 9304ms | 9930ms |
| 70.0 | 80.0 | app2 | ok | 32 | 6923ms | 9385ms | 9938ms |
| 70.0 | 80.0 | end-users | ok | 115 | 4708ms | 8935ms | 9894ms |
| 80.0 | 90.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 32 | 2227ms | 4429ms | 4943ms |
| 90.0 | 100.0 | app2 | ok | 18 | 2200ms | 4438ms | 4944ms |
| 90.0 | 100.0 | end-users | ok | 127 | 9784ms | 25836ms | 29584ms |
| 100.0 | 110.0 | app1 | ok | 22 | 1346ms | 2362ms | 4450ms |
| 100.0 | 110.0 | app2 | ok | 25 | 12143ms | 26429ms | 29643ms |
| 100.0 | 110.0 | end-users | ok | 128 | 8448ms | 24435ms | 29443ms |
| 110.0 | 120.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 32 | 9643ms | 25733ms | 29573ms |
| 120.0 | 130.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | end-users | ok | 113 | 5305ms | 17444ms | 28744ms |
| 130.0 | 140.0 | app1 | ok | 32 | 2227ms | 4429ms | 4943ms |
| 130.0 | 140.0 | app2 | ok | 19 | 1625ms | 4208ms | 4921ms |
| 130.0 | 140.0 | end-users | ok | 127 | 9784ms | 25836ms | 29584ms |
| 140.0 | 150.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 32 | 6923ms | 22000ms | 29200ms |
| 150.0 | 160.0 | app2 | ok | 31 | 19310ms | 27862ms | 29786ms |
| 150.0 | 160.0 | end-users | ok | 112 | 6395ms | 21040ms | 29104ms |
| 160.0 | 170.0 | app1 | ok | 31 | 5536ms | 9964ms | 27933ms |
| 160.0 | 170.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | end-users | ok | 114 | 6364ms | 20880ms | 29088ms |
| 170.0 | 180.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 170.0 | 180.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 170.0 | 180.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 180.0 | 190.0 | app1 | ok | 30 | 2125ms | 4545ms | 24000ms |
| 180.0 | 190.0 | app2 | ok | 17 | 1625ms | 4150ms | 4915ms |
| 180.0 | 190.0 | end-users | ok | 128 | 9821ms | 25871ms | 29587ms |
| 190.0 | 200.0 | app1 | ok | 32 | 7500ms | 22889ms | 29289ms |
| 190.0 | 200.0 | app2 | ok | 32 | 20000ms | 28000ms | 29800ms |
| 190.0 | 200.0 | end-users | ok | 113 | 5756ms | 18700ms | 28870ms |
| 200.0 | 211.0 | app1 | ok | 32 | 2000ms | 4333ms | 4933ms |
| 200.0 | 211.0 | app2 | ok | 18 | 1750ms | 4250ms | 4925ms |
| 200.0 | 211.0 | end-users | ok | 128 | 9915ms | 25937ms | 29594ms |
| 211.0 | 221.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 211.0 | 221.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 211.0 | 221.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 32 | 6786ms | 20857ms | 29086ms |
| 221.0 | 231.0 | app2 | ok | 32 | 19333ms | 27867ms | 29787ms |
| 221.0 | 231.0 | end-users | ok | 115 | 6221ms | 20800ms | 29080ms |
| 231.0 | 241.0 | app1 | ok | 31 | 2295ms | 4446ms | 4945ms |
| 231.0 | 241.0 | app2 | ok | 17 | 2375ms | 4469ms | 4947ms |
| 231.0 | 241.0 | end-users | ok | 127 | 9781ms | 25836ms | 29584ms |
| 241.0 | 251.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 1 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app2 | ok | 15 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | end-users | ok | 25 | 20000ms | 28000ms | 29800ms |
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
| 321.0 | 322.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 322.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 322.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens +43.9%, cost +42.2%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 451410 | 22545 | 681814.0 | 43.9% | 706072.0 | 496500.0 | 42.2% | False |
| app2 | 562110 | 27962 | 584908.0 | -0.9% | 599102.0 | 618034.0 | -3.1% | True |
| end-users | 2731830 | 135246 | 2847725.0 | -0.7% | 2930632.0 | 3002322.0 | -2.4% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 549 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 475 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2284 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=3211). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 310266 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
