# Fairness benchmark: full-contention (uni-211-h2-shadow-baseline)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `False` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-575669c495-cwt7g` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T17:19:36Z` |
| Run end | `2026-11-09T17:23:58Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 554 | 200=533, 500=21 | 15.7 | 16.1 | 702848.0 | 21.1% | 16.9% | -4.2 | 16.8% | -4.2 | 18.0s | 98.9% | 532.0 |
| app2 | 10.0 | 32 | 549 | 200=530, 500=19 | 15.7 | 16.1 | 697668.0 | 10.5% | 16.8% | 6.2 | 16.7% | 6.1 | 18.1s | 98.9% | 529.0 |
| end-users | 65.0 | 128 | 2194 | 200=2130, 500=64 | 15.7 | 16.1 | 2761996.0 | 68.4% | 66.4% | -2.1 | 66.5% | -1.9 | 18.1s | 98.9% | 2125.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 9480.0 | n/a | n/a | n/a | n/a | n/a | 1.1s | 98.9% | 7.0 |

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
| 0.0 | 10.0 | 10.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 13540.0 | 21.1% | 20.9% | -0.2 |
| 0.0 | 10.0 | app2 | True | 14886.0 | 10.5% | 22.9% | 12.4 |
| 0.0 | 10.0 | end-users | True | 36504.0 | 68.4% | 56.2% | -12.2 |
| 10.0 | 20.0 | app1 | True | 31132.0 | 21.1% | 17.7% | -3.3 |
| 10.0 | 20.0 | app2 | True | 29690.0 | 10.5% | 16.9% | 6.4 |
| 10.0 | 20.0 | end-users | True | 114860.0 | 68.4% | 65.4% | -3.0 |
| 20.0 | 30.0 | app1 | True | 28426.0 | 21.1% | 16.6% | -4.5 |
| 20.0 | 30.0 | app2 | True | 29710.0 | 10.5% | 17.3% | 6.8 |
| 20.0 | 30.0 | end-users | True | 113570.0 | 68.4% | 66.1% | -2.3 |
| 30.0 | 40.0 | app1 | True | 24348.0 | 21.1% | 15.9% | -5.1 |
| 30.0 | 40.0 | app2 | True | 24332.0 | 10.5% | 15.9% | 5.4 |
| 30.0 | 40.0 | end-users | True | 104172.0 | 68.4% | 68.2% | -0.3 |
| 40.0 | 50.0 | app1 | True | 33758.0 | 21.1% | 19.7% | -1.4 |
| 40.0 | 50.0 | app2 | True | 29704.0 | 10.5% | 17.3% | 6.8 |
| 40.0 | 50.0 | end-users | True | 108146.0 | 68.4% | 63.0% | -5.4 |
| 50.0 | 60.0 | app1 | True | 21658.0 | 21.1% | 12.6% | -8.4 |
| 50.0 | 60.0 | app2 | True | 27060.0 | 10.5% | 15.8% | 5.2 |
| 50.0 | 60.0 | end-users | True | 122862.0 | 68.4% | 71.6% | 3.2 |
| 60.0 | 70.0 | app1 | True | 32478.0 | 21.1% | 18.5% | -2.6 |
| 60.0 | 70.0 | app2 | True | 29808.0 | 10.5% | 17.0% | 6.4 |
| 60.0 | 70.0 | end-users | True | 113474.0 | 68.4% | 64.6% | -3.9 |
| 70.0 | 80.0 | app1 | True | 28344.0 | 21.1% | 18.6% | -2.5 |
| 70.0 | 80.0 | app2 | True | 25642.0 | 10.5% | 16.8% | 6.3 |
| 70.0 | 80.0 | end-users | True | 98748.0 | 68.4% | 64.7% | -3.8 |
| 80.0 | 90.0 | app1 | True | 22996.0 | 21.1% | 13.7% | -7.3 |
| 80.0 | 90.0 | app2 | True | 24380.0 | 10.5% | 14.5% | 4.0 |
| 80.0 | 90.0 | end-users | True | 120290.0 | 68.4% | 71.7% | 3.3 |
| 90.0 | 100.0 | app1 | True | 33746.0 | 21.1% | 19.8% | -1.3 |
| 90.0 | 100.0 | app2 | True | 31130.0 | 10.5% | 18.3% | 7.7 |
| 90.0 | 100.0 | end-users | True | 105536.0 | 68.4% | 61.9% | -6.5 |
| 100.0 | 110.0 | app1 | True | 28380.0 | 21.1% | 16.4% | -4.6 |
| 100.0 | 110.0 | app2 | True | 29746.0 | 10.5% | 17.2% | 6.7 |
| 100.0 | 110.0 | end-users | True | 114872.0 | 68.4% | 66.4% | -2.0 |
| 110.0 | 120.0 | app1 | True | 20332.0 | 21.1% | 13.4% | -7.6 |
| 110.0 | 120.0 | app2 | True | 22904.0 | 10.5% | 15.1% | 4.6 |
| 110.0 | 120.0 | end-users | True | 108156.0 | 68.4% | 71.4% | 3.0 |
| 120.0 | 130.0 | app1 | True | 32356.0 | 21.1% | 19.0% | -2.0 |
| 120.0 | 130.0 | app2 | True | 31106.0 | 10.5% | 18.3% | 7.8 |
| 120.0 | 130.0 | end-users | True | 106734.0 | 68.4% | 62.7% | -5.7 |
| 130.0 | 140.0 | app1 | True | 28440.0 | 21.1% | 16.6% | -4.5 |
| 130.0 | 140.0 | app2 | True | 29770.0 | 10.5% | 17.3% | 6.8 |
| 130.0 | 140.0 | end-users | True | 113456.0 | 68.4% | 66.1% | -2.3 |
| 140.0 | 150.0 | app1 | True | 21634.0 | 21.1% | 14.1% | -7.0 |
| 140.0 | 150.0 | app2 | True | 22984.0 | 10.5% | 14.9% | 4.4 |
| 140.0 | 150.0 | end-users | True | 109302.0 | 68.4% | 71.0% | 2.6 |
| 150.0 | 160.0 | app1 | True | 32346.0 | 21.1% | 18.7% | -2.4 |
| 150.0 | 160.0 | app2 | True | 29770.0 | 10.5% | 17.2% | 6.7 |
| 150.0 | 160.0 | end-users | True | 110868.0 | 68.4% | 64.1% | -4.3 |
| 160.0 | 170.0 | app1 | True | 27042.0 | 21.1% | 15.9% | -5.2 |
| 160.0 | 170.0 | app2 | True | 28338.0 | 10.5% | 16.6% | 6.1 |
| 160.0 | 170.0 | end-users | True | 115062.0 | 68.4% | 67.5% | -0.9 |
| 170.0 | 181.0 | app1 | True | 26994.0 | 21.1% | 16.2% | -4.8 |
| 170.0 | 181.0 | app2 | True | 27082.0 | 10.5% | 16.3% | 5.8 |
| 170.0 | 181.0 | end-users | True | 112264.0 | 68.4% | 67.5% | -0.9 |
| 181.0 | 191.0 | app1 | True | 28354.0 | 21.1% | 18.4% | -2.6 |
| 181.0 | 191.0 | app2 | True | 27028.0 | 10.5% | 17.5% | 7.0 |
| 181.0 | 191.0 | end-users | True | 98662.0 | 68.4% | 64.0% | -4.4 |
| 191.0 | 201.0 | app1 | True | 24288.0 | 21.1% | 14.3% | -6.8 |
| 191.0 | 201.0 | app2 | True | 27024.0 | 10.5% | 15.9% | 5.3 |
| 191.0 | 201.0 | end-users | True | 119014.0 | 68.4% | 69.9% | 1.5 |
| 201.0 | 211.0 | app1 | True | 32430.0 | 21.1% | 18.6% | -2.5 |
| 201.0 | 211.0 | app2 | True | 29746.0 | 10.5% | 17.1% | 6.5 |
| 201.0 | 211.0 | end-users | True | 112176.0 | 68.4% | 64.3% | -4.1 |
| 211.0 | 221.0 | app1 | True | 28386.0 | 21.1% | 16.9% | -4.1 |
| 211.0 | 221.0 | app2 | True | 28404.0 | 10.5% | 16.9% | 6.4 |
| 211.0 | 221.0 | end-users | True | 110960.0 | 68.4% | 66.1% | -2.3 |
| 221.0 | 231.0 | app1 | True | 21652.0 | 21.1% | 14.4% | -6.6 |
| 221.0 | 231.0 | app2 | True | 24400.0 | 10.5% | 16.2% | 5.7 |
| 221.0 | 231.0 | end-users | True | 104188.0 | 68.4% | 69.3% | 0.9 |
| 231.0 | 241.0 | app1 | True | 31110.0 | 21.1% | 18.5% | -2.5 |
| 231.0 | 241.0 | app2 | True | 28438.0 | 10.5% | 16.9% | 6.4 |
| 231.0 | 241.0 | end-users | True | 108282.0 | 68.4% | 64.5% | -3.9 |
| 241.0 | 251.0 | app1 | False | 27040.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 29726.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 112186.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 21638.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 14860.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 67652.0 | n/a | n/a | n/a |
| 261.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 21 | 0ms | 325ms | 482ms |
| 0.0 | 10.0 | app2 | ok | 21 | 14ms | 245ms | 474ms |
| 0.0 | 10.0 | end-users | ok | 100 | 0ms | 150ms | 438ms |
| 10.0 | 20.0 | app1 | ok | 36 | 889ms | 4182ms | 4918ms |
| 10.0 | 20.0 | app2 | ok | 39 | 964ms | 4188ms | 4919ms |
| 10.0 | 20.0 | end-users | ok | 154 | 1871ms | 4398ms | 4940ms |
| 20.0 | 30.0 | app1 | ok | 30 | 8750ms | 25000ms | 29500ms |
| 20.0 | 30.0 | app2 | ok | 28 | 7500ms | 23000ms | 29300ms |
| 20.0 | 30.0 | end-users | ok | 109 | 6862ms | 21280ms | 29128ms |
| 30.0 | 40.0 | app1 | ok | 28 | 8636ms | 24909ms | 29491ms |
| 30.0 | 40.0 | app2 | ok | 28 | 8889ms | 25333ms | 29533ms |
| 30.0 | 40.0 | end-users | ok | 111 | 7986ms | 24585ms | 29459ms |
| 40.0 | 50.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 50.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 28 | 8214ms | 23778ms | 29378ms |
| 50.0 | 60.0 | app2 | ok | 28 | 7692ms | 23000ms | 29300ms |
| 50.0 | 60.0 | end-users | ok | 108 | 8065ms | 24857ms | 29486ms |
| 60.0 | 70.0 | app1 | ok | 30 | 6818ms | 22500ms | 29250ms |
| 60.0 | 70.0 | app2 | ok | 29 | 7045ms | 22750ms | 29275ms |
| 60.0 | 70.0 | end-users | ok | 111 | 8456ms | 25067ms | 29507ms |
| 70.0 | 80.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 28 | 6250ms | 23000ms | 29300ms |
| 80.0 | 90.0 | app2 | ok | 28 | 7143ms | 24400ms | 29440ms |
| 80.0 | 90.0 | end-users | ok | 111 | 8598ms | 24955ms | 29495ms |
| 90.0 | 100.0 | app1 | ok | 27 | 6786ms | 24000ms | 29400ms |
| 90.0 | 100.0 | app2 | ok | 27 | 7188ms | 24000ms | 29400ms |
| 90.0 | 100.0 | end-users | ok | 118 | 8049ms | 24512ms | 29451ms |
| 100.0 | 110.0 | app1 | ok | 28 | 7143ms | 24400ms | 29440ms |
| 100.0 | 110.0 | app2 | ok | 28 | 8125ms | 24909ms | 29491ms |
| 100.0 | 110.0 | end-users | ok | 119 | 7722ms | 23897ms | 29390ms |
| 110.0 | 120.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 27 | 9167ms | 25500ms | 29550ms |
| 120.0 | 130.0 | app2 | ok | 28 | 9000ms | 25333ms | 29533ms |
| 120.0 | 130.0 | end-users | ok | 116 | 7703ms | 24341ms | 29434ms |
| 130.0 | 140.0 | app1 | ok | 29 | 9722ms | 25857ms | 29586ms |
| 130.0 | 140.0 | app2 | ok | 29 | 9062ms | 25538ms | 29554ms |
| 130.0 | 140.0 | end-users | ok | 113 | 7115ms | 23353ms | 29335ms |
| 140.0 | 150.0 | app1 | ok | 29 | 8750ms | 25167ms | 29517ms |
| 140.0 | 150.0 | app2 | ok | 29 | 9167ms | 25538ms | 29554ms |
| 140.0 | 150.0 | end-users | ok | 108 | 7692ms | 24000ms | 29400ms |
| 150.0 | 160.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 150.0 | 160.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 150.0 | 160.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 28 | 7692ms | 23000ms | 29300ms |
| 160.0 | 170.0 | app2 | ok | 27 | 7885ms | 23250ms | 29325ms |
| 160.0 | 170.0 | end-users | ok | 108 | 8286ms | 24857ms | 29486ms |
| 170.0 | 181.0 | app1 | ok | 28 | 7500ms | 23000ms | 29300ms |
| 170.0 | 181.0 | app2 | ok | 29 | 8125ms | 24200ms | 29420ms |
| 170.0 | 181.0 | end-users | ok | 111 | 8309ms | 24955ms | 29495ms |
| 181.0 | 191.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 181.0 | 191.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 181.0 | 191.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 29 | 7045ms | 22750ms | 29275ms |
| 191.0 | 201.0 | app2 | ok | 28 | 7500ms | 23778ms | 29378ms |
| 191.0 | 201.0 | end-users | ok | 113 | 8500ms | 25087ms | 29509ms |
| 201.0 | 211.0 | app1 | ok | 26 | 7857ms | 24800ms | 29480ms |
| 201.0 | 211.0 | app2 | ok | 28 | 7500ms | 24400ms | 29440ms |
| 201.0 | 211.0 | end-users | ok | 109 | 8476ms | 24810ms | 29481ms |
| 211.0 | 221.0 | app1 | ok | 27 | 8214ms | 25091ms | 29509ms |
| 211.0 | 221.0 | app2 | ok | 25 | 8214ms | 25000ms | 29500ms |
| 211.0 | 221.0 | end-users | ok | 115 | 8125ms | 24390ms | 29439ms |
| 221.0 | 231.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 27 | 9722ms | 25846ms | 29585ms |
| 231.0 | 241.0 | app2 | ok | 29 | 9062ms | 25538ms | 29554ms |
| 231.0 | 241.0 | end-users | ok | 113 | 7688ms | 24053ms | 29405ms |
| 241.0 | 251.0 | app1 | ok | 26 | 10000ms | 26000ms | 29600ms |
| 241.0 | 251.0 | app2 | ok | 21 | 10909ms | 26182ms | 29618ms |
| 241.0 | 251.0 | end-users | ok | 78 | 9487ms | 25543ms | 29554ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 262.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 262.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 262.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 655590 | 32420 | 686716.0 | -0.2% | 702848.0 | 720430.0 | -2.4% | True |
| app2 | 651900 | 32363 | 682969.0 | -0.2% | 697668.0 | 716626.0 | -2.6% | True |
| end-users | 2619900 | 129887 | 2743330.0 | -0.2% | 2761996.0 | 2879674.0 | -4.1% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 554 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 549 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2194 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=3193). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 3193 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 252212 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
