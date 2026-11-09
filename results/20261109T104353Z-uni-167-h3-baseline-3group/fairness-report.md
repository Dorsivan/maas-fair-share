# Fairness benchmark: full-contention (uni-167-h3-baseline-3group)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-nvwvv` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T10:45:07Z` |
| Run end | `2026-11-09T10:49:29Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 535 | 200=531, 500=4 | 14.8 | 23.8 | 707172.0 | 21.1% | 17.1% | -4.0 | 17.0% | -4.0 | 2.6s | 98.9% | 531.0 |
| app2 | 10.0 | 32 | 434 | 200=430, 500=4 | 24.1 | 27.4 | 559806.0 | 10.5% | 13.5% | 3.0 | 13.8% | 3.3 | 2.0s | 98.9% | 430.0 |
| end-users | 65.0 | 128 | 2173 | 200=2154, 500=19 | 14.9 | 19.4 | 2872698.0 | 68.4% | 69.4% | 1.0 | 69.2% | 0.7 | 2.3s | 98.9% | 2154.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

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

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 14884.0 | 21.1% | 17.8% | -3.3 |
| 0.0 | 10.0 | app2 | True | 10836.0 | 10.5% | 12.9% | 2.4 |
| 0.0 | 10.0 | end-users | True | 58068.0 | 68.4% | 69.3% | 0.9 |
| 10.0 | 20.0 | app1 | True | 24344.0 | 21.1% | 14.2% | -6.9 |
| 10.0 | 20.0 | app2 | True | 21608.0 | 10.5% | 12.6% | 2.1 |
| 10.0 | 20.0 | end-users | True | 125564.0 | 68.4% | 73.2% | 4.8 |
| 20.0 | 30.0 | app1 | True | 35132.0 | 21.1% | 20.8% | -0.3 |
| 20.0 | 30.0 | app2 | True | 35108.0 | 10.5% | 20.8% | 10.2 |
| 20.0 | 30.0 | end-users | True | 98802.0 | 68.4% | 58.4% | -10.0 |
| 30.0 | 40.0 | app1 | True | 31120.0 | 21.1% | 20.5% | -0.5 |
| 30.0 | 40.0 | app2 | True | 16196.0 | 10.5% | 10.7% | 0.2 |
| 30.0 | 40.0 | end-users | True | 104120.0 | 68.4% | 68.8% | 0.3 |
| 40.0 | 50.0 | app1 | True | 5386.0 | 21.1% | 3.2% | -17.9 |
| 40.0 | 50.0 | app2 | True | 5432.0 | 10.5% | 3.2% | -7.3 |
| 40.0 | 50.0 | end-users | True | 159270.0 | 68.4% | 93.6% | 25.2 |
| 50.0 | 60.0 | app1 | True | 49942.0 | 21.1% | 28.9% | 7.8 |
| 50.0 | 60.0 | app2 | True | 55424.0 | 10.5% | 32.0% | 21.5 |
| 50.0 | 60.0 | end-users | True | 67586.0 | 68.4% | 39.1% | -29.3 |
| 60.0 | 70.0 | app1 | True | 27100.0 | 21.1% | 17.7% | -3.3 |
| 60.0 | 70.0 | app2 | True | 5408.0 | 10.5% | 3.5% | -7.0 |
| 60.0 | 70.0 | end-users | True | 120456.0 | 68.4% | 78.7% | 10.3 |
| 70.0 | 80.0 | app1 | True | 2716.0 | 21.1% | 1.6% | -19.5 |
| 70.0 | 80.0 | app2 | True | 2716.0 | 10.5% | 1.6% | -8.9 |
| 70.0 | 80.0 | end-users | True | 164990.0 | 68.4% | 96.8% | 28.4 |
| 80.0 | 90.0 | app1 | True | 56782.0 | 21.1% | 33.9% | 12.8 |
| 80.0 | 90.0 | app2 | True | 55478.0 | 10.5% | 33.1% | 22.6 |
| 80.0 | 90.0 | end-users | True | 55374.0 | 68.4% | 33.0% | -35.4 |
| 90.0 | 100.0 | app1 | True | 17514.0 | 21.1% | 10.2% | -10.8 |
| 90.0 | 100.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 90.0 | 100.0 | end-users | True | 152714.0 | 68.4% | 89.0% | 20.6 |
| 100.0 | 110.0 | app1 | True | 33712.0 | 21.1% | 22.1% | 1.0 |
| 100.0 | 110.0 | app2 | True | 17532.0 | 10.5% | 11.5% | 1.0 |
| 100.0 | 110.0 | end-users | True | 101458.0 | 68.4% | 66.4% | -2.0 |
| 110.0 | 120.0 | app1 | True | 35200.0 | 21.1% | 21.3% | 0.3 |
| 110.0 | 120.0 | app2 | True | 47370.0 | 10.5% | 28.7% | 18.2 |
| 110.0 | 120.0 | end-users | True | 82484.0 | 68.4% | 50.0% | -18.4 |
| 120.0 | 130.0 | app1 | True | 17594.0 | 21.1% | 10.2% | -10.9 |
| 120.0 | 130.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 120.0 | 130.0 | end-users | True | 153966.0 | 68.4% | 89.0% | 20.6 |
| 130.0 | 140.0 | app1 | True | 43288.0 | 21.1% | 26.0% | 5.0 |
| 130.0 | 140.0 | app2 | True | 50084.0 | 10.5% | 30.1% | 19.6 |
| 130.0 | 140.0 | end-users | True | 72960.0 | 68.4% | 43.9% | -24.6 |
| 140.0 | 150.0 | app1 | True | 32522.0 | 21.1% | 21.3% | 0.2 |
| 140.0 | 150.0 | app2 | True | 9458.0 | 10.5% | 6.2% | -4.3 |
| 140.0 | 150.0 | end-users | True | 110822.0 | 68.4% | 72.5% | 4.1 |
| 150.0 | 160.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 150.0 | 160.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 150.0 | 160.0 | end-users | True | 171692.0 | 68.4% | 100.0% | 31.6 |
| 160.0 | 170.0 | app1 | True | 50038.0 | 21.1% | 29.6% | 8.6 |
| 160.0 | 170.0 | app2 | True | 63492.0 | 10.5% | 37.6% | 27.0 |
| 160.0 | 170.0 | end-users | True | 55450.0 | 68.4% | 32.8% | -35.6 |
| 170.0 | 180.0 | app1 | True | 31106.0 | 21.1% | 20.5% | -0.5 |
| 170.0 | 180.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 170.0 | 180.0 | end-users | True | 120434.0 | 68.4% | 79.5% | 11.1 |
| 180.0 | 190.0 | app1 | True | 1348.0 | 21.1% | 0.8% | -20.3 |
| 180.0 | 190.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 180.0 | 190.0 | end-users | True | 167728.0 | 68.4% | 99.2% | 30.8 |
| 190.0 | 200.0 | app1 | True | 56798.0 | 21.1% | 33.9% | 12.8 |
| 190.0 | 200.0 | app2 | True | 58210.0 | 10.5% | 34.7% | 24.2 |
| 190.0 | 200.0 | end-users | True | 52642.0 | 68.4% | 31.4% | -37.0 |
| 200.0 | 210.0 | app1 | True | 16206.0 | 21.1% | 9.8% | -11.2 |
| 200.0 | 210.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 200.0 | 210.0 | end-users | True | 148738.0 | 68.4% | 90.2% | 21.8 |
| 210.0 | 220.0 | app1 | True | 22920.0 | 21.1% | 14.6% | -6.4 |
| 210.0 | 220.0 | app2 | True | 12164.0 | 10.5% | 7.8% | -2.8 |
| 210.0 | 220.0 | end-users | True | 121674.0 | 68.4% | 77.6% | 9.2 |
| 220.0 | 230.0 | app1 | True | 44686.0 | 21.1% | 26.6% | 5.6 |
| 220.0 | 230.0 | app2 | True | 48714.0 | 10.5% | 29.0% | 18.5 |
| 220.0 | 230.0 | end-users | True | 74426.0 | 68.4% | 44.3% | -24.1 |
| 230.0 | 240.0 | app1 | True | 13532.0 | 21.1% | 7.9% | -13.1 |
| 230.0 | 240.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 230.0 | 240.0 | end-users | True | 156688.0 | 68.4% | 92.1% | 23.6 |
| 240.0 | 250.0 | app1 | False | 43302.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 32372.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 82648.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 9488.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 91944.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 29 | 175ms | 1775ms | 2428ms |
| 0.0 | 10.0 | app2 | ok | 28 | 556ms | 1800ms | 2430ms |
| 0.0 | 10.0 | end-users | ok | 109 | 391ms | 1916ms | 2442ms |
| 10.0 | 20.0 | app1 | ok | 32 | 6190ms | 9238ms | 9924ms |
| 10.0 | 20.0 | app2 | ok | 21 | 7237ms | 9447ms | 9945ms |
| 10.0 | 20.0 | end-users | ok | 119 | 6186ms | 9237ms | 9924ms |
| 20.0 | 30.0 | app1 | ok | 28 | 5833ms | 16000ms | 28600ms |
| 20.0 | 30.0 | app2 | ok | 25 | 10769ms | 26154ms | 29615ms |
| 20.0 | 30.0 | end-users | ok | 121 | 7938ms | 24500ms | 29450ms |
| 30.0 | 40.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 32 | 7917ms | 24182ms | 29418ms |
| 40.0 | 50.0 | app2 | ok | 24 | 18571ms | 27714ms | 29771ms |
| 40.0 | 50.0 | end-users | ok | 112 | 6548ms | 21704ms | 29170ms |
| 50.0 | 60.0 | app1 | ok | 26 | 1643ms | 5667ms | 9567ms |
| 50.0 | 60.0 | app2 | ok | 22 | 4167ms | 24500ms | 29450ms |
| 50.0 | 60.0 | end-users | ok | 117 | 9227ms | 25320ms | 29532ms |
| 60.0 | 70.0 | app1 | ok | 32 | 7917ms | 24182ms | 29418ms |
| 60.0 | 70.0 | app2 | ok | 21 | 20000ms | 28000ms | 29800ms |
| 60.0 | 70.0 | end-users | ok | 113 | 6062ms | 20960ms | 29096ms |
| 70.0 | 80.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 25 | 1477ms | 3750ms | 4875ms |
| 80.0 | 90.0 | app2 | ok | 24 | 4167ms | 25636ms | 29564ms |
| 80.0 | 90.0 | end-users | ok | 116 | 9492ms | 25538ms | 29554ms |
| 90.0 | 100.0 | app1 | ok | 32 | 8077ms | 24182ms | 29418ms |
| 90.0 | 100.0 | app2 | ok | 32 | 18966ms | 27793ms | 29779ms |
| 90.0 | 100.0 | end-users | ok | 114 | 6000ms | 19143ms | 28914ms |
| 100.0 | 110.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 100.0 | 110.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 100.0 | 110.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 32 | 2227ms | 4429ms | 4943ms |
| 110.0 | 120.0 | app2 | ok | 18 | 2000ms | 4357ms | 4936ms |
| 110.0 | 120.0 | end-users | ok | 118 | 10968ms | 26194ms | 29619ms |
| 120.0 | 130.0 | app1 | ok | 32 | 5833ms | 19333ms | 28933ms |
| 120.0 | 130.0 | app2 | ok | 22 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | end-users | ok | 111 | 6453ms | 21120ms | 29112ms |
| 130.0 | 140.0 | app1 | ok | 24 | 1600ms | 4000ms | 4900ms |
| 130.0 | 140.0 | app2 | ok | 23 | 3750ms | 25400ms | 29540ms |
| 130.0 | 140.0 | end-users | ok | 124 | 8947ms | 25040ms | 29504ms |
| 140.0 | 150.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 32 | 8571ms | 24667ms | 29467ms |
| 150.0 | 160.0 | app2 | ok | 29 | 20000ms | 28000ms | 29800ms |
| 150.0 | 160.0 | end-users | ok | 112 | 5465ms | 16824ms | 28682ms |
| 160.0 | 170.0 | app1 | ok | 29 | 1886ms | 4275ms | 4928ms |
| 160.0 | 170.0 | app2 | ok | 19 | 2350ms | 17333ms | 28733ms |
| 160.0 | 170.0 | end-users | ok | 119 | 9875ms | 25897ms | 29590ms |
| 170.0 | 180.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 170.0 | 180.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 170.0 | 180.0 | end-users | ok | 23 | 19545ms | 27909ms | 29791ms |
| 180.0 | 190.0 | app1 | ok | 31 | 7115ms | 22250ms | 29225ms |
| 180.0 | 190.0 | app2 | ok | 19 | 20000ms | 28000ms | 29800ms |
| 180.0 | 190.0 | end-users | ok | 89 | 4830ms | 8965ms | 9897ms |
| 190.0 | 200.0 | app1 | ok | 23 | 1614ms | 4188ms | 25400ms |
| 190.0 | 200.0 | app2 | ok | 25 | 10769ms | 26154ms | 29615ms |
| 190.0 | 200.0 | end-users | ok | 121 | 8904ms | 24958ms | 29496ms |
| 200.0 | 210.0 | app1 | ok | 32 | 8929ms | 25077ms | 29508ms |
| 200.0 | 210.0 | app2 | ok | 26 | 20000ms | 28000ms | 29800ms |
| 200.0 | 210.0 | end-users | ok | 115 | 5407ms | 17222ms | 28722ms |
| 210.0 | 220.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 210.0 | 220.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 210.0 | 220.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 220.0 | 230.0 | app1 | ok | 28 | 1900ms | 4300ms | 4930ms |
| 220.0 | 230.0 | app2 | ok | 20 | 3000ms | 23333ms | 29333ms |
| 220.0 | 230.0 | end-users | ok | 117 | 9788ms | 25821ms | 29582ms |
| 230.0 | 240.0 | app1 | ok | 32 | 7308ms | 22889ms | 29289ms |
| 230.0 | 240.0 | app2 | ok | 26 | 20000ms | 28000ms | 29800ms |
| 230.0 | 240.0 | end-users | ok | 114 | 6000ms | 19143ms | 28914ms |
| 240.0 | 250.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | ok | 6 | 20000ms | 28000ms | 29800ms |
| 240.0 | 250.0 | end-users | ok | 70 | 17719ms | 27544ms | 29754ms |
| 250.0 | 260.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 653130 | 32445 | 685575.0 | 0.0% | 707172.0 | 718020.0 | -1.5% | True |
| app2 | 528900 | 26279 | 555179.0 | 0.0% | 559806.0 | 581458.0 | -3.7% | True |
| end-users | 2649420 | 131254 | 2780674.0 | 0.0% | 2872698.0 | 2911928.0 | -1.3% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 535 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 434 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2173 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=3115). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 3115 | 0.050ms | 0.100ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 252216 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
