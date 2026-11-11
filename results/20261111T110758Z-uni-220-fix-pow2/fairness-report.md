# Fairness benchmark: six-group-board-case (uni-220-fix-pow2)

**Verdict: FAIL** (threshold: 10 points)
**Secondary (priority) verdict: PRIORITY-FAIL** -- see "Per-tenant TTFT / ITL and the priority verdict (UNI-226)" below for detail.
Worker-share vs. weight-share gap (UNI-225): 24.2 points

- app1 deviated -12.2 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `six-group-board-case` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:c8a088203f6dc6c48c158d21b6295172a78f18646b06c334e5310a0caedb259f` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-74c6487bc8-kftx8` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-11T11:08:48Z` |
| Run end | `2026-11-11T11:15:27Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 32.0 | 58 | 2126 | 200=2019, 500=107 | 5.6 | 12.1 | 2582692.0 | 50.8% | 26.6% | -24.2 | 38.6% | -12.2 | 36.9% | -13.9 | 67.4s | 98.9% | 2009.0 |
| app2 | 16.0 | 32 | 1062 | 200=1009, 500=53 | 6.0 | 16.6 | 1279344.0 | 25.4% | 14.7% | -10.7 | 19.1% | -6.3 | 18.4% | -7.0 | 65.3s | 98.9% | 1003.0 |
| app3 | 8.0 | 32 | 1147 | 000=1, 200=1082, 500=64 | 6.0 | 10.7 | 1375152.0 | 12.7% | 14.7% | 2.0 | 20.6% | 7.9 | 19.9% | 7.2 | 63.0s | 98.9% | 1080.0 |
| app4 | 4.0 | 32 | 614 | 200=557, 500=57 | 12.7 | 20.7 | 676110.0 | 6.3% | 14.7% | 8.3 | 10.1% | 3.8 | 10.7% | 4.3 | 67.6s | 98.9% | 551.0 |
| app5 | 2.0 | 32 | 482 | 200=429, 500=53 | 8.7 | 56.3 | 497420.0 | 3.2% | 14.7% | 11.5 | 7.4% | 4.3 | 8.4% | 5.2 | 68.6s | 98.9% | 423.0 |
| app6 | 1.0 | 32 | 334 | 200=279, 500=55 | 9.4 | 112.8 | 277068.0 | 1.6% | 14.7% | 13.1 | 4.1% | 2.6 | 5.8% | 4.2 | 68.9s | 98.9% | 277.0 |
| end-users | n/a | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 5430.0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 27.8s | 98.9% | 33.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- app3: active 0s-240s, no duty cycle
- app4: active 0s-240s, no duty cycle
- app6: active 0s-240s, no duty cycle
- app5: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (40 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 50.8% | 0.0% | -50.8 |
| 0.0 | 10.0 | app2 | True | 0.0 | 25.4% | 0.0% | -25.4 |
| 0.0 | 10.0 | app3 | True | 0.0 | 12.7% | 0.0% | -12.7 |
| 0.0 | 10.0 | app4 | True | 0.0 | 6.3% | 0.0% | -6.3 |
| 0.0 | 10.0 | app6 | True | 0.0 | 1.6% | 0.0% | -1.6 |
| 0.0 | 10.0 | app5 | True | 0.0 | 3.2% | 0.0% | -3.2 |
| 10.0 | 20.0 | app1 | True | 0.0 | 50.8% | 0.0% | -50.8 |
| 10.0 | 20.0 | app2 | True | 0.0 | 25.4% | 0.0% | -25.4 |
| 10.0 | 20.0 | app3 | True | 0.0 | 12.7% | 0.0% | -12.7 |
| 10.0 | 20.0 | app4 | True | 0.0 | 6.3% | 0.0% | -6.3 |
| 10.0 | 20.0 | app6 | True | 0.0 | 1.6% | 0.0% | -1.6 |
| 10.0 | 20.0 | app5 | True | 0.0 | 3.2% | 0.0% | -3.2 |
| 20.0 | 30.0 | app1 | True | 40620.0 | 50.8% | 26.3% | -24.5 |
| 20.0 | 30.0 | app2 | True | 20320.0 | 25.4% | 13.2% | -12.2 |
| 20.0 | 30.0 | app3 | True | 22994.0 | 12.7% | 14.9% | 2.2 |
| 20.0 | 30.0 | app4 | True | 31082.0 | 6.3% | 20.2% | 13.8 |
| 20.0 | 30.0 | app6 | True | 22992.0 | 1.6% | 14.9% | 13.3 |
| 20.0 | 30.0 | app5 | True | 16212.0 | 3.2% | 10.5% | 7.3 |
| 30.0 | 40.0 | app1 | True | 68918.0 | 50.8% | 22.5% | -28.3 |
| 30.0 | 40.0 | app2 | True | 63434.0 | 25.4% | 20.7% | -4.7 |
| 30.0 | 40.0 | app3 | True | 77134.0 | 12.7% | 25.1% | 12.4 |
| 30.0 | 40.0 | app4 | True | 36504.0 | 6.3% | 11.9% | 5.5 |
| 30.0 | 40.0 | app6 | True | 21666.0 | 1.6% | 7.1% | 5.5 |
| 30.0 | 40.0 | app5 | True | 39150.0 | 3.2% | 12.8% | 9.6 |
| 40.0 | 50.0 | app1 | True | 132704.0 | 50.8% | 43.4% | -7.4 |
| 40.0 | 50.0 | app2 | True | 82568.0 | 25.4% | 27.0% | 1.6 |
| 40.0 | 50.0 | app3 | True | 56836.0 | 12.7% | 18.6% | 5.9 |
| 40.0 | 50.0 | app4 | True | 18904.0 | 6.3% | 6.2% | -0.2 |
| 40.0 | 50.0 | app6 | True | 14852.0 | 1.6% | 4.9% | 3.3 |
| 40.0 | 50.0 | app5 | True | 0.0 | 3.2% | 0.0% | -3.2 |
| 50.0 | 60.0 | app1 | True | 139392.0 | 50.8% | 46.0% | -4.8 |
| 50.0 | 60.0 | app2 | True | 70356.0 | 25.4% | 23.2% | -2.2 |
| 50.0 | 60.0 | app3 | True | 64978.0 | 12.7% | 21.4% | 8.7 |
| 50.0 | 60.0 | app4 | True | 24296.0 | 6.3% | 8.0% | 1.7 |
| 50.0 | 60.0 | app6 | True | 0.0 | 1.6% | 0.0% | -1.6 |
| 50.0 | 60.0 | app5 | True | 4040.0 | 3.2% | 1.3% | -1.8 |
| 60.0 | 70.0 | app1 | True | 147440.0 | 50.8% | 48.7% | -2.1 |
| 60.0 | 70.0 | app2 | True | 71760.0 | 25.4% | 23.7% | -1.7 |
| 60.0 | 70.0 | app3 | True | 48734.0 | 12.7% | 16.1% | 3.4 |
| 60.0 | 70.0 | app4 | True | 35126.0 | 6.3% | 11.6% | 5.2 |
| 60.0 | 70.0 | app6 | True | 0.0 | 1.6% | 0.0% | -1.6 |
| 60.0 | 70.0 | app5 | True | 0.0 | 3.2% | 0.0% | -3.2 |
| 70.0 | 80.0 | app1 | True | 160744.0 | 50.8% | 51.9% | 1.1 |
| 70.0 | 80.0 | app2 | True | 79750.0 | 25.4% | 25.8% | 0.4 |
| 70.0 | 80.0 | app3 | True | 44644.0 | 12.7% | 14.4% | 1.7 |
| 70.0 | 80.0 | app4 | True | 24348.0 | 6.3% | 7.9% | 1.5 |
| 70.0 | 80.0 | app6 | True | 0.0 | 1.6% | 0.0% | -1.6 |
| 70.0 | 80.0 | app5 | True | 0.0 | 3.2% | 0.0% | -3.2 |
| 80.0 | 90.0 | app1 | True | 128626.0 | 50.8% | 42.6% | -8.2 |
| 80.0 | 90.0 | app2 | True | 62276.0 | 25.4% | 20.6% | -4.8 |
| 80.0 | 90.0 | app3 | True | 60892.0 | 12.7% | 20.2% | 7.5 |
| 80.0 | 90.0 | app4 | True | 40642.0 | 6.3% | 13.5% | 7.1 |
| 80.0 | 90.0 | app6 | True | 0.0 | 1.6% | 0.0% | -1.6 |
| 80.0 | 90.0 | app5 | True | 9460.0 | 3.2% | 3.1% | -0.0 |
| 90.0 | 100.0 | app1 | True | 121576.0 | 50.8% | 40.0% | -10.8 |
| 90.0 | 100.0 | app2 | True | 75648.0 | 25.4% | 24.9% | -0.5 |
| 90.0 | 100.0 | app3 | True | 73110.0 | 12.7% | 24.0% | 11.3 |
| 90.0 | 100.0 | app4 | True | 21678.0 | 6.3% | 7.1% | 0.8 |
| 90.0 | 100.0 | app6 | True | 0.0 | 1.6% | 0.0% | -1.6 |
| 90.0 | 100.0 | app5 | True | 12186.0 | 3.2% | 4.0% | 0.8 |
| 100.0 | 110.0 | app1 | True | 148842.0 | 50.8% | 52.2% | 1.4 |
| 100.0 | 110.0 | app2 | True | 66248.0 | 25.4% | 23.2% | -2.2 |
| 100.0 | 110.0 | app3 | True | 40512.0 | 12.7% | 14.2% | 1.5 |
| 100.0 | 110.0 | app4 | True | 20332.0 | 6.3% | 7.1% | 0.8 |
| 100.0 | 110.0 | app6 | True | 0.0 | 1.6% | 0.0% | -1.6 |
| 100.0 | 110.0 | app5 | True | 9454.0 | 3.2% | 3.3% | 0.1 |
| 110.0 | 120.0 | app1 | True | 121702.0 | 50.8% | 40.2% | -10.6 |
| 110.0 | 120.0 | app2 | True | 56772.0 | 25.4% | 18.7% | -6.7 |
| 110.0 | 120.0 | app3 | True | 41934.0 | 12.7% | 13.8% | 1.1 |
| 110.0 | 120.0 | app4 | True | 43262.0 | 6.3% | 14.3% | 7.9 |
| 110.0 | 120.0 | app6 | True | 8082.0 | 1.6% | 2.7% | 1.1 |
| 110.0 | 120.0 | app5 | True | 31154.0 | 3.2% | 10.3% | 7.1 |
| 120.0 | 130.0 | app1 | True | 140460.0 | 50.8% | 45.8% | -5.0 |
| 120.0 | 130.0 | app2 | True | 74348.0 | 25.4% | 24.2% | -1.2 |
| 120.0 | 130.0 | app3 | True | 58044.0 | 12.7% | 18.9% | 6.2 |
| 120.0 | 130.0 | app4 | True | 25766.0 | 6.3% | 8.4% | 2.1 |
| 120.0 | 130.0 | app6 | True | 2702.0 | 1.6% | 0.9% | -0.7 |
| 120.0 | 130.0 | app5 | True | 5400.0 | 3.2% | 1.8% | -1.4 |
| 130.0 | 140.0 | app1 | True | 147406.0 | 50.8% | 48.0% | -2.8 |
| 130.0 | 140.0 | app2 | True | 70338.0 | 25.4% | 22.9% | -2.5 |
| 130.0 | 140.0 | app3 | True | 62088.0 | 12.7% | 20.2% | 7.5 |
| 130.0 | 140.0 | app4 | True | 16206.0 | 6.3% | 5.3% | -1.1 |
| 130.0 | 140.0 | app6 | True | 2716.0 | 1.6% | 0.9% | -0.7 |
| 130.0 | 140.0 | app5 | True | 8148.0 | 3.2% | 2.7% | -0.5 |
| 140.0 | 150.0 | app1 | True | 132450.0 | 50.8% | 43.4% | -7.4 |
| 140.0 | 150.0 | app2 | True | 69072.0 | 25.4% | 22.6% | -2.8 |
| 140.0 | 150.0 | app3 | True | 56642.0 | 12.7% | 18.5% | 5.8 |
| 140.0 | 150.0 | app4 | True | 27028.0 | 6.3% | 8.8% | 2.5 |
| 140.0 | 150.0 | app6 | True | 6786.0 | 1.6% | 2.2% | 0.6 |
| 140.0 | 150.0 | app5 | True | 13530.0 | 3.2% | 4.4% | 1.3 |
| 150.0 | 160.0 | app1 | True | 154000.0 | 50.8% | 50.4% | -0.3 |
| 150.0 | 160.0 | app2 | True | 79814.0 | 25.4% | 26.1% | 0.7 |
| 150.0 | 160.0 | app3 | True | 37776.0 | 12.7% | 12.4% | -0.3 |
| 150.0 | 160.0 | app4 | True | 18866.0 | 6.3% | 6.2% | -0.2 |
| 150.0 | 160.0 | app6 | True | 5394.0 | 1.6% | 1.8% | 0.2 |
| 150.0 | 160.0 | app5 | True | 9426.0 | 3.2% | 3.1% | -0.1 |
| 160.0 | 170.0 | app1 | True | 102736.0 | 50.8% | 40.9% | -9.9 |
| 160.0 | 170.0 | app2 | True | 37880.0 | 25.4% | 15.1% | -10.3 |
| 160.0 | 170.0 | app3 | True | 40550.0 | 12.7% | 16.1% | 3.4 |
| 160.0 | 170.0 | app4 | True | 40584.0 | 6.3% | 16.1% | 9.8 |
| 160.0 | 170.0 | app6 | True | 9430.0 | 1.6% | 3.8% | 2.2 |
| 160.0 | 170.0 | app5 | True | 20238.0 | 3.2% | 8.0% | 4.9 |
| 170.0 | 180.0 | app1 | True | 50084.0 | 50.8% | 17.6% | -33.2 |
| 170.0 | 180.0 | app2 | True | 23014.0 | 25.4% | 8.1% | -17.3 |
| 170.0 | 180.0 | app3 | True | 67560.0 | 12.7% | 23.7% | 11.0 |
| 170.0 | 180.0 | app4 | True | 45916.0 | 6.3% | 16.1% | 9.8 |
| 170.0 | 180.0 | app6 | True | 39108.0 | 1.6% | 13.7% | 12.1 |
| 170.0 | 180.0 | app5 | True | 59510.0 | 3.2% | 20.9% | 17.7 |
| 180.0 | 190.0 | app1 | True | 35218.0 | 50.8% | 12.3% | -38.5 |
| 180.0 | 190.0 | app2 | True | 63488.0 | 25.4% | 22.1% | -3.2 |
| 180.0 | 190.0 | app3 | True | 82492.0 | 12.7% | 28.8% | 16.1 |
| 180.0 | 190.0 | app4 | True | 0.0 | 6.3% | 0.0% | -6.3 |
| 180.0 | 190.0 | app6 | True | 51352.0 | 1.6% | 17.9% | 16.3 |
| 180.0 | 190.0 | app5 | True | 54104.0 | 3.2% | 18.9% | 15.7 |
| 190.0 | 200.0 | app1 | True | 110860.0 | 50.8% | 39.6% | -11.2 |
| 190.0 | 200.0 | app2 | True | 0.0 | 25.4% | 0.0% | -25.4 |
| 190.0 | 200.0 | app3 | True | 64932.0 | 12.7% | 23.2% | 10.5 |
| 190.0 | 200.0 | app4 | True | 39246.0 | 6.3% | 14.0% | 7.7 |
| 190.0 | 200.0 | app6 | True | 17630.0 | 1.6% | 6.3% | 4.7 |
| 190.0 | 200.0 | app5 | True | 47198.0 | 3.2% | 16.9% | 13.7 |
| 200.0 | 210.0 | app1 | True | 112116.0 | 50.8% | 36.2% | -14.6 |
| 200.0 | 210.0 | app2 | True | 10854.0 | 25.4% | 3.5% | -21.9 |
| 200.0 | 210.0 | app3 | True | 94650.0 | 12.7% | 30.6% | 17.9 |
| 200.0 | 210.0 | app4 | True | 36476.0 | 6.3% | 11.8% | 5.4 |
| 200.0 | 210.0 | app6 | True | 9476.0 | 1.6% | 3.1% | 1.5 |
| 200.0 | 210.0 | app5 | True | 45938.0 | 3.2% | 14.8% | 11.7 |
| 210.0 | 221.0 | app1 | True | 150126.0 | 50.8% | 49.1% | -1.7 |
| 210.0 | 221.0 | app2 | True | 43316.0 | 25.4% | 14.2% | -11.2 |
| 210.0 | 221.0 | app3 | True | 81134.0 | 12.7% | 26.5% | 13.9 |
| 210.0 | 221.0 | app4 | True | 16190.0 | 6.3% | 5.3% | -1.1 |
| 210.0 | 221.0 | app6 | True | 2698.0 | 1.6% | 0.9% | -0.7 |
| 210.0 | 221.0 | app5 | True | 12142.0 | 3.2% | 4.0% | 0.8 |
| 221.0 | 231.0 | app1 | True | 104034.0 | 50.8% | 35.0% | -15.8 |
| 221.0 | 231.0 | app2 | True | 59446.0 | 25.4% | 20.0% | -5.4 |
| 221.0 | 231.0 | app3 | True | 85296.0 | 12.7% | 28.7% | 16.0 |
| 221.0 | 231.0 | app4 | True | 27044.0 | 6.3% | 9.1% | 2.7 |
| 221.0 | 231.0 | app6 | True | 8112.0 | 1.6% | 2.7% | 1.1 |
| 221.0 | 231.0 | app5 | True | 13548.0 | 3.2% | 4.6% | 1.4 |
| 231.0 | 241.0 | app1 | True | 54184.0 | 50.8% | 18.0% | -32.7 |
| 231.0 | 241.0 | app2 | True | 55358.0 | 25.4% | 18.4% | -7.0 |
| 231.0 | 241.0 | app3 | True | 71678.0 | 12.7% | 23.9% | 11.2 |
| 231.0 | 241.0 | app4 | True | 43266.0 | 6.3% | 14.4% | 8.1 |
| 231.0 | 241.0 | app6 | True | 32472.0 | 1.6% | 10.8% | 9.2 |
| 231.0 | 241.0 | app5 | True | 43266.0 | 3.2% | 14.4% | 11.2 |
| 241.0 | 251.0 | app1 | False | 78454.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 43284.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | 40542.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app4 | False | 43348.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app6 | False | 21600.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app5 | False | 43316.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 399.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 399.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 399.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 399.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 399.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 399.0 | app5 | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 17 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 8 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app3 | ok | 13 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app4 | ok | 13 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app6 | ok | 12 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app5 | ok | 11 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 66 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app2 | ok | 41 | 0ms | 0ms | 1ms |
| 10.0 | 20.0 | app3 | ok | 39 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app4 | ok | 36 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app6 | ok | 40 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app5 | ok | 38 | 0ms | 0ms | 1ms |
| 20.0 | 30.0 | app1 | ok | 72 | 175ms | 1669ms | 2417ms |
| 20.0 | 30.0 | app2 | ok | 42 | 357ms | 1450ms | 2395ms |
| 20.0 | 30.0 | app3 | ok | 32 | 312ms | 1900ms | 2440ms |
| 20.0 | 30.0 | app4 | ok | 35 | 212ms | 1625ms | 2412ms |
| 20.0 | 30.0 | app6 | ok | 36 | 556ms | 1960ms | 2446ms |
| 20.0 | 30.0 | app5 | ok | 36 | 500ms | 2085ms | 2458ms |
| 30.0 | 40.0 | app1 | ok | 62 | 3214ms | 4986ms | 9483ms |
| 30.0 | 40.0 | app2 | ok | 44 | 2269ms | 4450ms | 4945ms |
| 30.0 | 40.0 | app3 | ok | 76 | 1523ms | 3100ms | 4810ms |
| 30.0 | 40.0 | app4 | ok | 17 | 1477ms | 2405ms | 4575ms |
| 30.0 | 40.0 | app6 | ok | 12 | 1000ms | 3500ms | 4850ms |
| 30.0 | 40.0 | app5 | ok | 11 | 1562ms | 4083ms | 4908ms |
| 40.0 | 50.0 | app1 | ok | 111 | 1465ms | 3679ms | 4868ms |
| 40.0 | 50.0 | app2 | ok | 69 | 962ms | 3562ms | 4856ms |
| 40.0 | 50.0 | app3 | ok | 41 | 1489ms | 2950ms | 4795ms |
| 40.0 | 50.0 | app4 | ok | 32 | 7500ms | 9500ms | 9950ms |
| 40.0 | 50.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app5 | ok | 3 | 20000ms | 28000ms | 29800ms |
| 50.0 | 60.0 | app1 | ok | 103 | 1262ms | 2293ms | 3712ms |
| 50.0 | 60.0 | app2 | ok | 56 | 1250ms | 2370ms | 4533ms |
| 50.0 | 60.0 | app3 | ok | 44 | 1818ms | 4083ms | 4908ms |
| 50.0 | 60.0 | app4 | ok | 22 | 7250ms | 9450ms | 9945ms |
| 50.0 | 60.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 109 | 1191ms | 2299ms | 4092ms |
| 60.0 | 70.0 | app2 | ok | 53 | 1341ms | 2305ms | 3675ms |
| 60.0 | 70.0 | app3 | ok | 48 | 1703ms | 3286ms | 4829ms |
| 60.0 | 70.0 | app4 | ok | 22 | 7500ms | 22667ms | 29267ms |
| 60.0 | 70.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 118 | 1315ms | 2456ms | 4705ms |
| 70.0 | 80.0 | app2 | ok | 57 | 1375ms | 2625ms | 4762ms |
| 70.0 | 80.0 | app3 | ok | 32 | 1750ms | 4200ms | 4920ms |
| 70.0 | 80.0 | app4 | ok | 17 | 13000ms | 26600ms | 29660ms |
| 70.0 | 80.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app5 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 80.0 | 90.0 | app1 | ok | 78 | 1562ms | 3607ms | 4861ms |
| 80.0 | 90.0 | app2 | ok | 45 | 1510ms | 3125ms | 4812ms |
| 80.0 | 90.0 | app3 | ok | 41 | 1725ms | 2950ms | 4795ms |
| 80.0 | 90.0 | app4 | ok | 22 | 8333ms | 25111ms | 29511ms |
| 80.0 | 90.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app5 | ok | 9 | 45000ms | 57000ms | 59700ms |
| 90.0 | 100.0 | app1 | ok | 114 | 1452ms | 2808ms | 4781ms |
| 90.0 | 100.0 | app2 | ok | 62 | 1622ms | 2786ms | 4779ms |
| 90.0 | 100.0 | app3 | ok | 50 | 1158ms | 3438ms | 4844ms |
| 90.0 | 100.0 | app4 | ok | 22 | 9231ms | 25111ms | 29511ms |
| 90.0 | 100.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app5 | ok | 11 | 50625ms | 60000ms | 60000ms |
| 100.0 | 110.0 | app1 | ok | 78 | 1422ms | 4364ms | 9220ms |
| 100.0 | 110.0 | app2 | ok | 32 | 3158ms | 4842ms | 9200ms |
| 100.0 | 110.0 | app3 | ok | 39 | 3125ms | 4625ms | 4962ms |
| 100.0 | 110.0 | app4 | ok | 32 | 3333ms | 8778ms | 23600ms |
| 100.0 | 110.0 | app6 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 100.0 | 110.0 | app5 | ok | 23 | 25455ms | 60000ms | 60000ms |
| 110.0 | 120.0 | app1 | ok | 88 | 2389ms | 4476ms | 4948ms |
| 110.0 | 120.0 | app2 | ok | 46 | 2700ms | 4540ms | 4954ms |
| 110.0 | 120.0 | app3 | ok | 31 | 1513ms | 2492ms | 4742ms |
| 110.0 | 120.0 | app4 | ok | 19 | 7361ms | 9472ms | 9947ms |
| 110.0 | 120.0 | app6 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 110.0 | 120.0 | app5 | ok | 4 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app1 | ok | 127 | 1536ms | 3620ms | 4862ms |
| 120.0 | 130.0 | app2 | ok | 61 | 1521ms | 2821ms | 4782ms |
| 120.0 | 130.0 | app3 | ok | 31 | 839ms | 2317ms | 4613ms |
| 120.0 | 130.0 | app4 | ok | 10 | 18889ms | 27778ms | 29778ms |
| 120.0 | 130.0 | app6 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 120.0 | 130.0 | app5 | ok | 5 | 20000ms | 28000ms | 29800ms |
| 130.0 | 140.0 | app1 | ok | 120 | 1463ms | 2692ms | 4769ms |
| 130.0 | 140.0 | app2 | ok | 60 | 1259ms | 2500ms | 4750ms |
| 130.0 | 140.0 | app3 | ok | 55 | 1094ms | 2469ms | 4725ms |
| 130.0 | 140.0 | app4 | ok | 15 | 18462ms | 27692ms | 29769ms |
| 130.0 | 140.0 | app6 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 130.0 | 140.0 | app5 | ok | 8 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app1 | ok | 66 | 1355ms | 2397ms | 4588ms |
| 140.0 | 150.0 | app2 | ok | 43 | 1539ms | 2345ms | 3925ms |
| 140.0 | 150.0 | app3 | ok | 33 | 2350ms | 4942ms | 9450ms |
| 140.0 | 150.0 | app4 | ok | 17 | 20000ms | 28000ms | 29800ms |
| 140.0 | 150.0 | app6 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 140.0 | 150.0 | app5 | ok | 8 | 42857ms | 56571ms | 59657ms |
| 150.0 | 160.0 | app1 | ok | 146 | 1136ms | 2274ms | 3783ms |
| 150.0 | 160.0 | app2 | ok | 63 | 1345ms | 2366ms | 4475ms |
| 150.0 | 160.0 | app3 | ok | 39 | 3681ms | 8050ms | 9805ms |
| 150.0 | 160.0 | app4 | ok | 36 | 13636ms | 26727ms | 29673ms |
| 150.0 | 160.0 | app6 | ok | 33 | 50625ms | 60000ms | 60000ms |
| 150.0 | 160.0 | app5 | ok | 34 | 22500ms | 50727ms | 59073ms |
| 160.0 | 170.0 | app1 | ok | 57 | 5403ms | 9081ms | 9908ms |
| 160.0 | 170.0 | app2 | ok | 32 | 5294ms | 9059ms | 9906ms |
| 160.0 | 170.0 | app3 | ok | 28 | 4167ms | 8833ms | 9883ms |
| 160.0 | 170.0 | app4 | ok | 17 | 3438ms | 8583ms | 9858ms |
| 160.0 | 170.0 | app6 | ok | 4 | 2500ms | 8000ms | 9800ms |
| 160.0 | 170.0 | app5 | ok | 9 | 2312ms | 8500ms | 9850ms |
| 170.0 | 180.0 | app1 | ok | 20 | 7500ms | 9500ms | 9950ms |
| 170.0 | 180.0 | app2 | ok | 9 | 679ms | 936ms | 994ms |
| 170.0 | 180.0 | app3 | ok | 53 | 2740ms | 4779ms | 9117ms |
| 170.0 | 180.0 | app4 | ok | 15 | 7115ms | 9423ms | 9942ms |
| 170.0 | 180.0 | app6 | ok | 28 | 2219ms | 5333ms | 9533ms |
| 170.0 | 180.0 | app5 | ok | 44 | 2500ms | 6333ms | 9633ms |
| 180.0 | 190.0 | app1 | ok | 53 | 16053ms | 27211ms | 29721ms |
| 180.0 | 190.0 | app2 | ok | 23 | 1984ms | 4042ms | 4904ms |
| 180.0 | 190.0 | app3 | ok | 31 | 979ms | 2190ms | 2469ms |
| 180.0 | 190.0 | app4 | ok | 26 | 7500ms | 9500ms | 9950ms |
| 180.0 | 190.0 | app6 | ok | 20 | 3750ms | 4861ms | 9000ms |
| 180.0 | 190.0 | app5 | ok | 18 | 1273ms | 2255ms | 2475ms |
| 190.0 | 200.0 | app1 | ok | 67 | 2162ms | 4823ms | 9330ms |
| 190.0 | 200.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 190.0 | 200.0 | app3 | ok | 64 | 3167ms | 6800ms | 9680ms |
| 190.0 | 200.0 | app4 | ok | 22 | 2269ms | 22667ms | 29267ms |
| 190.0 | 200.0 | app6 | ok | 7 | 12500ms | 26500ms | 29650ms |
| 190.0 | 200.0 | app5 | ok | 60 | 2380ms | 8571ms | 9857ms |
| 200.0 | 210.0 | app1 | ok | 105 | 1562ms | 3688ms | 4869ms |
| 200.0 | 210.0 | app2 | ok | 33 | 19688ms | 27938ms | 29794ms |
| 200.0 | 210.0 | app3 | ok | 83 | 1463ms | 3847ms | 4885ms |
| 200.0 | 210.0 | app4 | ok | 17 | 4861ms | 8938ms | 9894ms |
| 200.0 | 210.0 | app6 | ok | 5 | 20000ms | 28000ms | 29800ms |
| 200.0 | 210.0 | app5 | ok | 12 | 3750ms | 8500ms | 9850ms |
| 210.0 | 221.0 | app1 | ok | 88 | 1000ms | 2228ms | 2800ms |
| 210.0 | 221.0 | app2 | ok | 32 | 2778ms | 4556ms | 4956ms |
| 210.0 | 221.0 | app3 | ok | 62 | 1667ms | 2493ms | 4742ms |
| 210.0 | 221.0 | app4 | ok | 16 | 8077ms | 19333ms | 28933ms |
| 210.0 | 221.0 | app6 | ok | 4 | 20000ms | 28000ms | 29800ms |
| 210.0 | 221.0 | app5 | ok | 10 | 17500ms | 27500ms | 29750ms |
| 221.0 | 231.0 | app1 | ok | 86 | 1574ms | 3464ms | 4846ms |
| 221.0 | 231.0 | app2 | ok | 37 | 886ms | 2230ms | 8150ms |
| 221.0 | 231.0 | app3 | ok | 37 | 1489ms | 2454ms | 4692ms |
| 221.0 | 231.0 | app4 | ok | 32 | 10000ms | 26000ms | 29600ms |
| 221.0 | 231.0 | app6 | ok | 13 | 45000ms | 57000ms | 59700ms |
| 221.0 | 231.0 | app5 | ok | 27 | 17727ms | 27545ms | 29755ms |
| 231.0 | 241.0 | app1 | ok | 31 | 2847ms | 4569ms | 4957ms |
| 231.0 | 241.0 | app2 | ok | 48 | 2167ms | 7333ms | 9733ms |
| 231.0 | 241.0 | app3 | ok | 62 | 3385ms | 4677ms | 4968ms |
| 231.0 | 241.0 | app4 | ok | 14 | 3750ms | 4750ms | 4975ms |
| 231.0 | 241.0 | app6 | ok | 17 | 25455ms | 51500ms | 59150ms |
| 231.0 | 241.0 | app5 | ok | 7 | 8750ms | 25333ms | 29533ms |
| 241.0 | 251.0 | app1 | ok | 27 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | app2 | ok | 7 | 1875ms | 3250ms | 4825ms |
| 241.0 | 251.0 | app3 | ok | 16 | 929ms | 2157ms | 2466ms |
| 241.0 | 251.0 | app4 | ok | 25 | 4083ms | 8214ms | 9821ms |
| 241.0 | 251.0 | app6 | ok | 28 | 7917ms | 16000ms | 28600ms |
| 241.0 | 251.0 | app5 | ok | 32 | 5000ms | 9000ms | 9900ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 399.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 399.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 399.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 399.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 399.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 399.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app4 exceeded the 10% ledger tolerance: cost -10.2%
- app5 exceeded the 10% ledger tolerance: cost -14.2%
- app6 exceeded the 10% ledger tolerance: cost -26.5%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2483370 | 123326 | 2593782.0 | -0.5% | 2582692.0 | 2730022.0 | -5.4% | True |
| app2 | 1241070 | 61750 | 1295066.0 | -0.6% | 1279344.0 | 1364570.0 | -6.2% | True |
| app3 | 1330860 | 66077 | 1393062.0 | -0.3% | 1375152.0 | 1463014.0 | -6.0% | True |
| app4 | 685110 | 33973 | 711337.0 | -1.1% | 676110.0 | 753056.0 | -10.2% | False |
| app5 | 527670 | 26149 | 546069.0 | -1.4% | 497420.0 | 579968.0 | -14.2% | False |
| app6 | 343170 | 16999 | 357588.0 | -0.7% | 277068.0 | 377168.0 | -26.5% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2126 | 0 | 0 | 0 (never shed) | 0.00% | 50.8% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1062 | 0 | 0 | 0 (never shed) | 0.00% | 25.4% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 1147 | 0 | 0 | 0 (never shed) | 0.00% | 12.7% | n/a (nothing shed) | n/a (nothing shed) |
| app4 | 614 | 0 | 0 | 0 (never shed) | 0.00% | 6.3% | n/a (nothing shed) | n/a (nothing shed) |
| app5 | 482 | 0 | 0 | 0 (never shed) | 0.00% | 3.2% | n/a (nothing shed) | n/a (nothing shed) |
| app6 | 334 | 0 | 0 | 0 (never shed) | 0.00% | 1.6% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5376). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5376 | 0.051ms | 0.147ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 373122 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 2009 | 5679ms | 13182ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1003 | 6014ms | 16975ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app3 | ok | 1079 | 6187ms | 11451ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app4 | ok | 551 | 13554ms | 23878ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app5 | ok | 423 | 9623ms | 56338ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app6 | ok | 277 | 11480ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5375 | 6363ms | 21990ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: PRIORITY-FAIL** -- the share verdict above is FAIL, so this is the board's second, independent success criterion (2026-11-10): did the policy nonetheless order tenants by weight? Top-weighted group: `app1` (TTFT p50 5679ms, p95 13182ms, strictly lowest among distinctly-weighted groups: p50=True/p95=False; no rank inversion among any distinctly-weighted pair: False -- this, not raw rank correlation, is what gates the verdict, since a genuine weight tie (e.g. 98/1/1's app2==end-users) makes exact correlation 1.0 unreachable by construction even when ordering is otherwise perfect). Rank correlation 0.83 (1.00 = exact agreement, informational only) shown for reference. Separation from the next distinctly-weighted group: 334ms against a noise floor of not given (separation check skipped).

**Windowed TTFT/ITL** (40 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 1021ms | 1575ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 1000ms | 1225ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app3 | ok | 1036ms | 1229ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app4 | ok | 920ms | 1350ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app6 | ok | 1062ms | 1438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app5 | ok | 1031ms | 1431ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 1000ms | 1922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 1146ms | 1954ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app3 | ok | 900ms | 1865ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app4 | ok | 1146ms | 1865ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app6 | ok | 1146ms | 2125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app5 | ok | 925ms | 2325ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 3661ms | 5370ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 3567ms | 4835ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app3 | ok | 3225ms | 4383ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app4 | ok | 3528ms | 4806ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app6 | ok | 4000ms | 7300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app5 | ok | 3450ms | 5910ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 6786ms | 7879ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 5393ms | 7687ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app3 | ok | 3948ms | 4963ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app4 | ok | 8412ms | 9841ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app6 | ok | 8250ms | 11000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app5 | ok | 8273ms | 13550ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 8133ms | 14300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 5633ms | 7829ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app3 | ok | 6000ms | 7989ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app4 | ok | 14375ms | 19417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app6 | ok | 11944ms | 14694ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 5293ms | 7458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 5733ms | 7711ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app3 | ok | 8000ms | 11000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app4 | ok | 14091ms | 19357ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app5 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 5326ms | 6183ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 5625ms | 7592ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app3 | ok | 8364ms | 9836ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app4 | ok | 14333ms | 19409ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 5246ms | 6017ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 5662ms | 7653ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app3 | ok | 7737ms | 9764ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app4 | ok | 14091ms | 19357ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 5109ms | 7780ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 5467ms | 7693ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app3 | ok | 7206ms | 13594ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app4 | ok | 16053ms | 19605ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app5 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 5909ms | 7795ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 5667ms | 7776ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app3 | ok | 6400ms | 13500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app4 | ok | 15556ms | 19556ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app5 | ok | 58500ms | 113250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 6136ms | 7814ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 6292ms | 8775ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app3 | ok | 6778ms | 13125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app4 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 6500ms | 9125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 7357ms | 9650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app3 | ok | 9069ms | 11125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app4 | ok | 13636ms | 19667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app5 | ok | 32500ms | 108500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 5500ms | 7711ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 6233ms | 7883ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app3 | ok | 7483ms | 9823ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app4 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app5 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 5304ms | 7738ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 5750ms | 7948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app3 | ok | 7167ms | 9646ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app4 | ok | 18333ms | 28000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app5 | ok | 27500ms | 42750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 5857ms | 8775ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 5643ms | 9150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app3 | ok | 6625ms | 12900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app4 | ok | 19167ms | 28750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app5 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 4903ms | 7050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 5685ms | 7719ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app3 | ok | 9286ms | 14222ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app4 | ok | 22222ms | 29222ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app6 | ok | 100000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app5 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 5457ms | 9300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 6267ms | 7947ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app3 | ok | 10000ms | 14500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app4 | ok | 18056ms | 28125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app6 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app5 | ok | 38654ms | 54375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 7682ms | 9879ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app3 | ok | 7333ms | 14306ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app4 | ok | 10588ms | 15750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app6 | ok | 43500ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app5 | ok | 13000ms | 27800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app1 | ok | 13824ms | 19278ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app2 | ok | 7516ms | 19096ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app3 | ok | 5000ms | 7800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app6 | ok | 9226ms | 13643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app5 | ok | 6720ms | 9000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app1 | ok | 9714ms | 21800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app3 | ok | 6286ms | 7829ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app4 | ok | 17788ms | 25167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app6 | ok | 14062ms | 19350ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app5 | ok | 9316ms | 14205ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app1 | ok | 6983ms | 9427ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app3 | ok | 4743ms | 7643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app4 | ok | 9688ms | 25500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app6 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app5 | ok | 7176ms | 9844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 221.0 | app1 | ok | 5776ms | 7975ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 221.0 | app2 | ok | 23333ms | 29333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 221.0 | app3 | ok | 4304ms | 5846ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 221.0 | app4 | ok | 13333ms | 19000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 221.0 | app6 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 221.0 | app5 | ok | 13214ms | 18875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 5659ms | 7939ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 7412ms | 14312ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app3 | ok | 5981ms | 7797ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app4 | ok | 18125ms | 27500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app6 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app5 | ok | 18125ms | 27500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 6000ms | 7800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 7154ms | 9992ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app3 | ok | 5386ms | 6940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app4 | ok | 13158ms | 27333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app6 | ok | 38571ms | 54000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app5 | ok | 22353ms | 37000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 14531ms | 19442ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 7273ms | 9829ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app3 | ok | 4938ms | 5962ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app4 | ok | 11667ms | 14667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app6 | ok | 13158ms | 27000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app5 | ok | 8800ms | 14385ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app6 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 399.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 399.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 399.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 399.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 399.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 399.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
