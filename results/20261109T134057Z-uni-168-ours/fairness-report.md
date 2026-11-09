# Fairness benchmark: full-contention (uni-168-ours)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-6vkbb` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T13:42:09Z` |
| Run end | `2026-11-09T13:46:42Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 547 | 200=535, 500=12 | 15.6 | 24.2 | 712310.0 | 21.1% | 17.1% | -3.9 | 16.9% | -4.2 | 5.5s | 98.9% | 531.0 |
| app2 | 10.0 | 32 | 455 | 200=444, 500=11 | 21.3 | 27.7 | 577096.0 | 10.5% | 13.9% | 3.3 | 14.0% | 3.5 | 5.1s | 98.9% | 439.0 |
| end-users | 65.0 | 128 | 2239 | 200=2168, 500=71 | 15.2 | 19.3 | 2873226.0 | 68.4% | 69.0% | 0.6 | 69.1% | 0.7 | 5.3s | 98.9% | 2159.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 6776.0 | n/a | n/a | n/a | n/a | n/a | 0.0s | 98.9% | 18.0 |

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

**Windows** (28 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 4070.0 | 21.1% | 20.1% | -0.9 |
| 0.0 | 10.0 | app2 | True | 2688.0 | 10.5% | 13.3% | 2.8 |
| 0.0 | 10.0 | end-users | True | 13480.0 | 68.4% | 66.6% | -1.8 |
| 10.0 | 20.0 | app1 | True | 32438.0 | 21.1% | 16.5% | -4.5 |
| 10.0 | 20.0 | app2 | True | 25628.0 | 10.5% | 13.1% | 2.5 |
| 10.0 | 20.0 | end-users | True | 137942.0 | 68.4% | 70.4% | 2.0 |
| 20.0 | 30.0 | app1 | True | 33800.0 | 21.1% | 20.2% | -0.9 |
| 20.0 | 30.0 | app2 | True | 16222.0 | 10.5% | 9.7% | -0.9 |
| 20.0 | 30.0 | end-users | True | 117668.0 | 68.4% | 70.2% | 1.7 |
| 30.0 | 40.0 | app1 | True | 31176.0 | 21.1% | 19.9% | -1.2 |
| 30.0 | 40.0 | app2 | True | 17624.0 | 10.5% | 11.2% | 0.7 |
| 30.0 | 40.0 | end-users | True | 108068.0 | 68.4% | 68.9% | 0.5 |
| 40.0 | 50.0 | app1 | True | 29618.0 | 21.1% | 17.1% | -3.9 |
| 40.0 | 50.0 | app2 | True | 39220.0 | 10.5% | 22.7% | 12.1 |
| 40.0 | 50.0 | end-users | True | 104256.0 | 68.4% | 60.2% | -8.2 |
| 50.0 | 60.0 | app1 | True | 14894.0 | 21.1% | 8.7% | -12.4 |
| 50.0 | 60.0 | app2 | True | 4074.0 | 10.5% | 2.4% | -8.2 |
| 50.0 | 60.0 | end-users | True | 152590.0 | 68.4% | 88.9% | 20.5 |
| 60.0 | 70.0 | app1 | True | 40604.0 | 21.1% | 25.0% | 3.9 |
| 60.0 | 70.0 | app2 | True | 54062.0 | 10.5% | 33.3% | 22.8 |
| 60.0 | 70.0 | end-users | True | 67736.0 | 68.4% | 41.7% | -26.7 |
| 70.0 | 80.0 | app1 | True | 35132.0 | 21.1% | 22.4% | 1.4 |
| 70.0 | 80.0 | app2 | True | 6722.0 | 10.5% | 4.3% | -6.2 |
| 70.0 | 80.0 | end-users | True | 114948.0 | 68.4% | 73.3% | 4.9 |
| 80.0 | 90.0 | app1 | True | 2674.0 | 21.1% | 1.6% | -19.5 |
| 80.0 | 90.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 80.0 | 90.0 | end-users | True | 166268.0 | 68.4% | 98.4% | 30.0 |
| 90.0 | 100.0 | app1 | True | 43224.0 | 21.1% | 25.2% | 4.1 |
| 90.0 | 100.0 | app2 | True | 37868.0 | 10.5% | 22.1% | 11.5 |
| 90.0 | 100.0 | end-users | True | 90578.0 | 68.4% | 52.8% | -15.7 |
| 100.0 | 110.0 | app1 | True | 16224.0 | 21.1% | 10.6% | -10.4 |
| 100.0 | 110.0 | app2 | True | 22944.0 | 10.5% | 15.0% | 4.5 |
| 100.0 | 110.0 | end-users | True | 113520.0 | 68.4% | 74.3% | 5.9 |
| 110.0 | 120.0 | app1 | True | 36480.0 | 21.1% | 21.6% | 0.5 |
| 110.0 | 120.0 | app2 | True | 17636.0 | 10.5% | 10.4% | -0.1 |
| 110.0 | 120.0 | end-users | True | 114900.0 | 68.4% | 68.0% | -0.4 |
| 120.0 | 130.0 | app1 | True | 16224.0 | 21.1% | 9.6% | -11.5 |
| 120.0 | 130.0 | app2 | True | 51326.0 | 10.5% | 30.4% | 19.8 |
| 120.0 | 130.0 | end-users | True | 101444.0 | 68.4% | 60.0% | -8.4 |
| 130.0 | 140.0 | app1 | True | 28380.0 | 21.1% | 16.9% | -4.1 |
| 130.0 | 140.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 130.0 | 140.0 | end-users | True | 139380.0 | 68.4% | 83.1% | 14.7 |
| 140.0 | 150.0 | app1 | True | 14884.0 | 21.1% | 9.7% | -11.3 |
| 140.0 | 150.0 | app2 | True | 8116.0 | 10.5% | 5.3% | -5.2 |
| 140.0 | 150.0 | end-users | True | 129762.0 | 68.4% | 84.9% | 16.5 |
| 150.0 | 160.0 | app1 | True | 49878.0 | 21.1% | 29.1% | 8.0 |
| 150.0 | 160.0 | app2 | True | 54094.0 | 10.5% | 31.5% | 21.0 |
| 150.0 | 160.0 | end-users | True | 67490.0 | 68.4% | 39.4% | -29.1 |
| 160.0 | 170.0 | app1 | True | 17518.0 | 21.1% | 10.5% | -10.5 |
| 160.0 | 170.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 160.0 | 170.0 | end-users | True | 148754.0 | 68.4% | 89.5% | 21.0 |
| 170.0 | 180.0 | app1 | True | 31168.0 | 21.1% | 20.2% | -0.9 |
| 170.0 | 180.0 | app2 | True | 14868.0 | 10.5% | 9.6% | -0.9 |
| 170.0 | 180.0 | end-users | True | 108262.0 | 68.4% | 70.2% | 1.7 |
| 180.0 | 190.0 | app1 | True | 39182.0 | 21.1% | 23.0% | 2.0 |
| 180.0 | 190.0 | app2 | True | 45946.0 | 10.5% | 27.0% | 16.5 |
| 180.0 | 190.0 | end-users | True | 85170.0 | 68.4% | 50.0% | -18.4 |
| 190.0 | 200.0 | app1 | True | 9460.0 | 21.1% | 5.6% | -15.5 |
| 190.0 | 200.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 190.0 | 200.0 | end-users | True | 160864.0 | 68.4% | 94.4% | 26.0 |
| 200.0 | 210.0 | app1 | True | 66316.0 | 21.1% | 39.5% | 18.5 |
| 200.0 | 210.0 | app2 | True | 33804.0 | 10.5% | 20.2% | 9.6 |
| 200.0 | 210.0 | end-users | True | 67592.0 | 68.4% | 40.3% | -28.1 |
| 210.0 | 220.0 | app1 | True | 6778.0 | 21.1% | 4.3% | -16.8 |
| 210.0 | 220.0 | app2 | True | 24258.0 | 10.5% | 15.4% | 4.8 |
| 210.0 | 220.0 | end-users | True | 126978.0 | 68.4% | 80.4% | 11.9 |
| 220.0 | 230.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 220.0 | 230.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 220.0 | 230.0 | end-users | True | 167788.0 | 68.4% | 100.0% | 31.6 |
| 230.0 | 240.0 | app1 | True | 55440.0 | 21.1% | 32.8% | 11.8 |
| 230.0 | 240.0 | app2 | True | 56692.0 | 10.5% | 33.6% | 23.0 |
| 230.0 | 240.0 | end-users | True | 56838.0 | 68.4% | 33.6% | -34.8 |
| 240.0 | 250.0 | app1 | False | 16192.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 152862.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 40556.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 43304.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 58088.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 273.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 273.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 273.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 10 | 50ms | 833ms | 983ms |
| 0.0 | 10.0 | app2 | ok | 13 | 75ms | 392ms | 489ms |
| 0.0 | 10.0 | end-users | ok | 45 | 0ms | 241ms | 925ms |
| 10.0 | 20.0 | app1 | ok | 39 | 2150ms | 4391ms | 4939ms |
| 10.0 | 20.0 | app2 | ok | 25 | 2375ms | 4479ms | 4948ms |
| 10.0 | 20.0 | end-users | ok | 158 | 2093ms | 4373ms | 4937ms |
| 20.0 | 30.0 | app1 | ok | 30 | 6429ms | 24000ms | 29400ms |
| 20.0 | 30.0 | app2 | ok | 23 | 17222ms | 27444ms | 29744ms |
| 20.0 | 30.0 | end-users | ok | 118 | 6545ms | 18762ms | 28876ms |
| 30.0 | 40.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 32 | 7500ms | 23600ms | 29360ms |
| 40.0 | 50.0 | app2 | ok | 25 | 9583ms | 25833ms | 29583ms |
| 40.0 | 50.0 | end-users | ok | 113 | 7812ms | 24205ms | 29421ms |
| 50.0 | 60.0 | app1 | ok | 30 | 6250ms | 20000ms | 29000ms |
| 50.0 | 60.0 | app2 | ok | 25 | 19130ms | 27826ms | 29783ms |
| 50.0 | 60.0 | end-users | ok | 114 | 6875ms | 22875ms | 29288ms |
| 60.0 | 70.0 | app1 | ok | 28 | 1955ms | 4750ms | 27200ms |
| 60.0 | 70.0 | app2 | ok | 21 | 2812ms | 24000ms | 29400ms |
| 60.0 | 70.0 | end-users | ok | 121 | 9398ms | 25519ms | 29552ms |
| 70.0 | 80.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 32 | 7000ms | 20857ms | 29086ms |
| 80.0 | 90.0 | app2 | ok | 23 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | end-users | ok | 112 | 5652ms | 16000ms | 28600ms |
| 90.0 | 100.0 | app1 | ok | 22 | 2091ms | 4312ms | 4931ms |
| 90.0 | 100.0 | app2 | ok | 22 | 3750ms | 25111ms | 29511ms |
| 90.0 | 100.0 | end-users | ok | 127 | 9167ms | 25296ms | 29530ms |
| 100.0 | 110.0 | app1 | ok | 19 | 11000ms | 26200ms | 29620ms |
| 100.0 | 110.0 | app2 | ok | 32 | 8750ms | 25429ms | 29543ms |
| 100.0 | 110.0 | end-users | ok | 128 | 7245ms | 23081ms | 29308ms |
| 110.0 | 120.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 32 | 18148ms | 27630ms | 29763ms |
| 120.0 | 130.0 | app2 | ok | 20 | 6429ms | 22000ms | 29200ms |
| 120.0 | 130.0 | end-users | ok | 120 | 6771ms | 21724ms | 29172ms |
| 130.0 | 140.0 | app1 | ok | 32 | 6154ms | 19333ms | 28933ms |
| 130.0 | 140.0 | app2 | ok | 26 | 20000ms | 28000ms | 29800ms |
| 130.0 | 140.0 | end-users | ok | 112 | 6279ms | 20667ms | 29067ms |
| 140.0 | 150.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 29 | 1750ms | 4094ms | 4909ms |
| 150.0 | 160.0 | app2 | ok | 21 | 2750ms | 23000ms | 29300ms |
| 150.0 | 160.0 | end-users | ok | 128 | 9310ms | 25429ms | 29543ms |
| 160.0 | 170.0 | app1 | ok | 32 | 7500ms | 22889ms | 29289ms |
| 160.0 | 170.0 | app2 | ok | 23 | 20000ms | 28000ms | 29800ms |
| 160.0 | 170.0 | end-users | ok | 112 | 5682ms | 17556ms | 28756ms |
| 170.0 | 180.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 170.0 | 180.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 170.0 | 180.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 180.0 | 190.0 | app1 | ok | 27 | 1562ms | 3875ms | 4888ms |
| 180.0 | 190.0 | app2 | ok | 22 | 3333ms | 25111ms | 29511ms |
| 180.0 | 190.0 | end-users | ok | 122 | 9554ms | 25643ms | 29564ms |
| 190.0 | 200.0 | app1 | ok | 32 | 7692ms | 23600ms | 29360ms |
| 190.0 | 200.0 | app2 | ok | 17 | 20000ms | 28000ms | 29800ms |
| 190.0 | 200.0 | end-users | ok | 111 | 5872ms | 18900ms | 28890ms |
| 200.0 | 210.0 | app1 | ok | 22 | 1136ms | 2336ms | 4450ms |
| 200.0 | 210.0 | app2 | ok | 26 | 12667ms | 26533ms | 29653ms |
| 200.0 | 210.0 | end-users | ok | 119 | 8922ms | 24936ms | 29494ms |
| 210.0 | 220.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 210.0 | 220.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 210.0 | 220.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 220.0 | 230.0 | app1 | ok | 32 | 19677ms | 27935ms | 29794ms |
| 220.0 | 230.0 | app2 | ok | 17 | 20000ms | 28000ms | 29800ms |
| 220.0 | 230.0 | end-users | ok | 112 | 4828ms | 9756ms | 27511ms |
| 230.0 | 240.0 | app1 | ok | 21 | 1068ms | 2214ms | 2471ms |
| 230.0 | 240.0 | app2 | ok | 26 | 12667ms | 26533ms | 29653ms |
| 230.0 | 240.0 | end-users | ok | 128 | 8571ms | 24667ms | 29467ms |
| 240.0 | 250.0 | app1 | ok | 30 | 11250ms | 26250ms | 29625ms |
| 240.0 | 250.0 | app2 | ok | 32 | 19677ms | 27935ms | 29794ms |
| 240.0 | 250.0 | end-users | ok | 59 | 8032ms | 19273ms | 28927ms |
| 250.0 | 260.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 270.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 273.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 273.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 273.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 658050 | 32554 | 685428.0 | -0.7% | 712310.0 | 723158.0 | -1.5% | True |
| app2 | 546120 | 26976 | 566655.0 | -1.1% | 577096.0 | 600072.0 | -3.8% | True |
| end-users | 2666640 | 132397 | 2787424.0 | -0.4% | 2873226.0 | 2931434.0 | -2.0% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 547 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 455 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2239 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=3147). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 3147 | 0.050ms | 0.100ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 262749 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
