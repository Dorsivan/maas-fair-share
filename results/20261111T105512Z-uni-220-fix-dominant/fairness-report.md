# Fairness benchmark: six-group-board-case (uni-220-fix-dominant)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 36.9 points

## Run metadata

| field | value |
|---|---|
| Scenario | `six-group-board-case` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:c8a088203f6dc6c48c158d21b6295172a78f18646b06c334e5310a0caedb259f` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-6bc87ddfc8-k8kj4` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-11T10:56:34Z` |
| Run end | `2026-11-11T11:05:00Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 90.0 | 181 | 4765 | 000=2, 200=4437, 500=326 | 7.9 | 12.9 | 5527840.0 | 90.0% | 53.1% | -36.9 | 86.9% | -3.1 | 80.5% | -9.5 | 60.4s | 98.9% | 4385.0 |
| app2 | 2.0 | 32 | 232 | 200=182, 500=50 | 6.8 | 120.1 | 167492.0 | 2.0% | 9.4% | 7.4 | 2.6% | 0.6 | 3.9% | 1.9 | 63.8s | 98.9% | 178.0 |
| app3 | 2.0 | 32 | 242 | 200=189, 500=53 | 7.3 | 117.8 | 174358.0 | 2.0% | 9.4% | 7.4 | 2.7% | 0.7 | 4.1% | 2.1 | 63.8s | 98.9% | 178.0 |
| app4 | 2.0 | 32 | 225 | 200=180, 500=45 | 6.9 | 122.3 | 163696.0 | 2.0% | 9.4% | 7.4 | 2.6% | 0.6 | 3.8% | 1.8 | 63.9s | 98.9% | 173.0 |
| app5 | 2.0 | 32 | 229 | 200=184, 500=45 | 7.0 | 119.0 | 167768.0 | 2.0% | 9.4% | 7.4 | 2.6% | 0.6 | 3.9% | 1.9 | 63.8s | 98.9% | 177.0 |
| app6 | 2.0 | 32 | 227 | 200=173, 500=54 | 6.1 | 124.9 | 159474.0 | 2.0% | 9.4% | 7.4 | 2.5% | 0.5 | 3.8% | 1.8 | 63.9s | 98.9% | 171.0 |
| end-users | n/a | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 35196.0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 38.5s | 98.9% | 85.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- app4: active 0s-240s, no duty cycle
- app6: active 0s-240s, no duty cycle
- app3: active 0s-240s, no duty cycle
- app5: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (51 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 90.0% | 0.0% | -90.0 |
| 0.0 | 10.0 | app2 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 0.0 | 10.0 | app4 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 0.0 | 10.0 | app6 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 0.0 | 10.0 | app3 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 0.0 | 10.0 | app5 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 10.0 | 20.0 | app1 | True | 0.0 | 90.0% | 0.0% | -90.0 |
| 10.0 | 20.0 | app2 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 10.0 | 20.0 | app4 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 10.0 | 20.0 | app6 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 10.0 | 20.0 | app3 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 10.0 | 20.0 | app5 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 20.0 | 30.0 | app1 | True | 0.0 | 90.0% | 0.0% | -90.0 |
| 20.0 | 30.0 | app2 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 20.0 | 30.0 | app4 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 20.0 | 30.0 | app6 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 20.0 | 30.0 | app3 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 20.0 | 30.0 | app5 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 30.0 | 40.0 | app1 | True | 44552.0 | 90.0% | 67.3% | -22.7 |
| 30.0 | 40.0 | app2 | True | 5396.0 | 2.0% | 8.2% | 6.2 |
| 30.0 | 40.0 | app4 | True | 8118.0 | 2.0% | 12.3% | 10.3 |
| 30.0 | 40.0 | app6 | True | 4060.0 | 2.0% | 6.1% | 4.1 |
| 30.0 | 40.0 | app3 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 30.0 | 40.0 | app5 | True | 4028.0 | 2.0% | 6.1% | 4.1 |
| 40.0 | 50.0 | app1 | True | 205582.0 | 90.0% | 67.6% | -22.4 |
| 40.0 | 50.0 | app2 | True | 16248.0 | 2.0% | 5.3% | 3.3 |
| 40.0 | 50.0 | app4 | True | 21684.0 | 2.0% | 7.1% | 5.1 |
| 40.0 | 50.0 | app6 | True | 21626.0 | 2.0% | 7.1% | 5.1 |
| 40.0 | 50.0 | app3 | True | 18894.0 | 2.0% | 6.2% | 4.2 |
| 40.0 | 50.0 | app5 | True | 20292.0 | 2.0% | 6.7% | 4.7 |
| 50.0 | 60.0 | app1 | True | 227304.0 | 90.0% | 74.4% | -15.6 |
| 50.0 | 60.0 | app2 | True | 18872.0 | 2.0% | 6.2% | 4.2 |
| 50.0 | 60.0 | app4 | True | 9462.0 | 2.0% | 3.1% | 1.1 |
| 50.0 | 60.0 | app6 | True | 8134.0 | 2.0% | 2.7% | 0.7 |
| 50.0 | 60.0 | app3 | True | 25680.0 | 2.0% | 8.4% | 6.4 |
| 50.0 | 60.0 | app5 | True | 16206.0 | 2.0% | 5.3% | 3.3 |
| 60.0 | 70.0 | app1 | True | 304346.0 | 90.0% | 100.0% | 10.0 |
| 60.0 | 70.0 | app2 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 60.0 | 70.0 | app4 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 60.0 | 70.0 | app6 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 60.0 | 70.0 | app3 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 60.0 | 70.0 | app5 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 70.0 | 80.0 | app1 | True | 305632.0 | 90.0% | 100.0% | 10.0 |
| 70.0 | 80.0 | app2 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 70.0 | 80.0 | app4 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 70.0 | 80.0 | app6 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 70.0 | 80.0 | app3 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 70.0 | 80.0 | app5 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 80.0 | 90.0 | app1 | True | 260902.0 | 90.0% | 90.2% | 0.2 |
| 80.0 | 90.0 | app2 | True | 5400.0 | 2.0% | 1.9% | -0.1 |
| 80.0 | 90.0 | app4 | True | 4064.0 | 2.0% | 1.4% | -0.6 |
| 80.0 | 90.0 | app6 | True | 5402.0 | 2.0% | 1.9% | -0.1 |
| 80.0 | 90.0 | app3 | True | 8106.0 | 2.0% | 2.8% | 0.8 |
| 80.0 | 90.0 | app5 | True | 5428.0 | 2.0% | 1.9% | -0.1 |
| 90.0 | 100.0 | app1 | True | 308524.0 | 90.0% | 100.0% | 10.0 |
| 90.0 | 100.0 | app2 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 90.0 | 100.0 | app4 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 90.0 | 100.0 | app6 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 90.0 | 100.0 | app3 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 90.0 | 100.0 | app5 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 100.0 | 110.0 | app1 | True | 300356.0 | 90.0% | 100.0% | 10.0 |
| 100.0 | 110.0 | app2 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 100.0 | 110.0 | app4 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 100.0 | 110.0 | app6 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 100.0 | 110.0 | app3 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 100.0 | 110.0 | app5 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 110.0 | 120.0 | app1 | True | 246064.0 | 90.0% | 93.3% | 3.3 |
| 110.0 | 120.0 | app2 | True | 4028.0 | 2.0% | 1.5% | -0.5 |
| 110.0 | 120.0 | app4 | True | 2714.0 | 2.0% | 1.0% | -1.0 |
| 110.0 | 120.0 | app6 | True | 4068.0 | 2.0% | 1.5% | -0.5 |
| 110.0 | 120.0 | app3 | True | 4030.0 | 2.0% | 1.5% | -0.5 |
| 110.0 | 120.0 | app5 | True | 2716.0 | 2.0% | 1.0% | -1.0 |
| 120.0 | 130.0 | app1 | True | 307018.0 | 90.0% | 100.0% | 10.0 |
| 120.0 | 130.0 | app2 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 120.0 | 130.0 | app4 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 120.0 | 130.0 | app6 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 120.0 | 130.0 | app3 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 120.0 | 130.0 | app5 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 130.0 | 140.0 | app1 | True | 296272.0 | 90.0% | 100.0% | 10.0 |
| 130.0 | 140.0 | app2 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 130.0 | 140.0 | app4 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 130.0 | 140.0 | app6 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 130.0 | 140.0 | app3 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 130.0 | 140.0 | app5 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 140.0 | 150.0 | app1 | True | 296100.0 | 90.0% | 96.5% | 6.5 |
| 140.0 | 150.0 | app2 | True | 2702.0 | 2.0% | 0.9% | -1.1 |
| 140.0 | 150.0 | app4 | True | 2698.0 | 2.0% | 0.9% | -1.1 |
| 140.0 | 150.0 | app6 | True | 1358.0 | 2.0% | 0.4% | -1.6 |
| 140.0 | 150.0 | app3 | True | 1346.0 | 2.0% | 0.4% | -1.6 |
| 140.0 | 150.0 | app5 | True | 2708.0 | 2.0% | 0.9% | -1.1 |
| 150.0 | 160.0 | app1 | True | 251578.0 | 90.0% | 90.3% | 0.3 |
| 150.0 | 160.0 | app2 | True | 4014.0 | 2.0% | 1.4% | -0.6 |
| 150.0 | 160.0 | app4 | True | 4062.0 | 2.0% | 1.5% | -0.5 |
| 150.0 | 160.0 | app6 | True | 6732.0 | 2.0% | 2.4% | 0.4 |
| 150.0 | 160.0 | app3 | True | 6770.0 | 2.0% | 2.4% | 0.4 |
| 150.0 | 160.0 | app5 | True | 5422.0 | 2.0% | 1.9% | -0.1 |
| 160.0 | 170.0 | app1 | True | 273434.0 | 90.0% | 89.0% | -1.0 |
| 160.0 | 170.0 | app2 | True | 6742.0 | 2.0% | 2.2% | 0.2 |
| 160.0 | 170.0 | app4 | True | 8132.0 | 2.0% | 2.6% | 0.6 |
| 160.0 | 170.0 | app6 | True | 6762.0 | 2.0% | 2.2% | 0.2 |
| 160.0 | 170.0 | app3 | True | 5374.0 | 2.0% | 1.7% | -0.3 |
| 160.0 | 170.0 | app5 | True | 6736.0 | 2.0% | 2.2% | 0.2 |
| 170.0 | 180.0 | app1 | True | 278434.0 | 90.0% | 90.7% | 0.7 |
| 170.0 | 180.0 | app2 | True | 6776.0 | 2.0% | 2.2% | 0.2 |
| 170.0 | 180.0 | app4 | True | 5398.0 | 2.0% | 1.8% | -0.2 |
| 170.0 | 180.0 | app6 | True | 5392.0 | 2.0% | 1.8% | -0.2 |
| 170.0 | 180.0 | app3 | True | 5398.0 | 2.0% | 1.8% | -0.2 |
| 170.0 | 180.0 | app5 | True | 5418.0 | 2.0% | 1.8% | -0.2 |
| 180.0 | 191.0 | app1 | True | 281156.0 | 90.0% | 90.5% | 0.5 |
| 180.0 | 191.0 | app2 | True | 5392.0 | 2.0% | 1.7% | -0.3 |
| 180.0 | 191.0 | app4 | True | 5386.0 | 2.0% | 1.7% | -0.3 |
| 180.0 | 191.0 | app6 | True | 6780.0 | 2.0% | 2.2% | 0.2 |
| 180.0 | 191.0 | app3 | True | 6728.0 | 2.0% | 2.2% | 0.2 |
| 180.0 | 191.0 | app5 | True | 5380.0 | 2.0% | 1.7% | -0.3 |
| 191.0 | 201.0 | app1 | True | 275884.0 | 90.0% | 90.2% | 0.2 |
| 191.0 | 201.0 | app2 | True | 6764.0 | 2.0% | 2.2% | 0.2 |
| 191.0 | 201.0 | app4 | True | 8130.0 | 2.0% | 2.7% | 0.7 |
| 191.0 | 201.0 | app6 | True | 4074.0 | 2.0% | 1.3% | -0.7 |
| 191.0 | 201.0 | app3 | True | 5432.0 | 2.0% | 1.8% | -0.2 |
| 191.0 | 201.0 | app5 | True | 5418.0 | 2.0% | 1.8% | -0.2 |
| 201.0 | 211.0 | app1 | True | 147496.0 | 90.0% | 58.3% | -31.7 |
| 201.0 | 211.0 | app2 | True | 20274.0 | 2.0% | 8.0% | 6.0 |
| 201.0 | 211.0 | app4 | True | 18946.0 | 2.0% | 7.5% | 5.5 |
| 201.0 | 211.0 | app6 | True | 21616.0 | 2.0% | 8.5% | 6.5 |
| 201.0 | 211.0 | app3 | True | 21638.0 | 2.0% | 8.6% | 6.6 |
| 201.0 | 211.0 | app5 | True | 23042.0 | 2.0% | 9.1% | 7.1 |
| 211.0 | 221.0 | app1 | True | 226026.0 | 90.0% | 98.8% | 8.8 |
| 211.0 | 221.0 | app2 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 211.0 | 221.0 | app4 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 211.0 | 221.0 | app6 | True | 0.0 | 2.0% | 0.0% | -2.0 |
| 211.0 | 221.0 | app3 | True | 1358.0 | 2.0% | 0.6% | -1.4 |
| 211.0 | 221.0 | app5 | True | 1358.0 | 2.0% | 0.6% | -1.4 |
| 221.0 | 231.0 | app1 | True | 219054.0 | 90.0% | 84.4% | -5.6 |
| 221.0 | 231.0 | app2 | True | 9468.0 | 2.0% | 3.6% | 1.6 |
| 221.0 | 231.0 | app4 | True | 9466.0 | 2.0% | 3.6% | 1.6 |
| 221.0 | 231.0 | app6 | True | 8132.0 | 2.0% | 3.1% | 1.1 |
| 221.0 | 231.0 | app3 | True | 6766.0 | 2.0% | 2.6% | 0.6 |
| 221.0 | 231.0 | app5 | True | 6766.0 | 2.0% | 2.6% | 0.6 |
| 231.0 | 241.0 | app1 | True | 147448.0 | 90.0% | 69.9% | -20.1 |
| 231.0 | 241.0 | app2 | True | 12148.0 | 2.0% | 5.8% | 3.8 |
| 231.0 | 241.0 | app4 | True | 12194.0 | 2.0% | 5.8% | 3.8 |
| 231.0 | 241.0 | app6 | True | 12142.0 | 2.0% | 5.8% | 3.8 |
| 231.0 | 241.0 | app3 | True | 13566.0 | 2.0% | 6.4% | 4.4 |
| 231.0 | 241.0 | app5 | True | 13526.0 | 2.0% | 6.4% | 4.4 |
| 241.0 | 251.0 | app1 | False | 286784.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 2704.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app4 | False | 4054.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app6 | False | 2702.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | 2694.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app5 | False | 4074.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 37894.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 40564.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | False | 39188.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | False | 40494.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | False | 40578.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | False | 39250.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app5 | False | 0.0 | n/a | n/a | n/a |
| 502.0 | 506.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 502.0 | 506.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 502.0 | 506.0 | app4 | False | 0.0 | n/a | n/a | n/a |
| 502.0 | 506.0 | app6 | False | 0.0 | n/a | n/a | n/a |
| 502.0 | 506.0 | app3 | False | 0.0 | n/a | n/a | n/a |
| 502.0 | 506.0 | app5 | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 30 | 0ms | 0ms | 1ms |
| 0.0 | 10.0 | app2 | ok | 3 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app4 | ok | 6 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app6 | ok | 4 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app3 | ok | 4 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app5 | ok | 6 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 91 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app2 | ok | 14 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app4 | ok | 16 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app6 | ok | 18 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app3 | ok | 13 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app5 | ok | 14 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app1 | ok | 110 | 0ms | 0ms | 1ms |
| 20.0 | 30.0 | app2 | ok | 23 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app4 | ok | 24 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app6 | ok | 23 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app3 | ok | 20 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app5 | ok | 20 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app1 | ok | 132 | 0ms | 464ms | 934ms |
| 30.0 | 40.0 | app2 | ok | 25 | 0ms | 425ms | 875ms |
| 30.0 | 40.0 | app4 | ok | 21 | 69ms | 650ms | 965ms |
| 30.0 | 40.0 | app6 | ok | 23 | 92ms | 418ms | 492ms |
| 30.0 | 40.0 | app3 | ok | 20 | 0ms | 438ms | 900ms |
| 30.0 | 40.0 | app5 | ok | 25 | 0ms | 469ms | 938ms |
| 40.0 | 50.0 | app1 | ok | 190 | 1245ms | 2282ms | 3417ms |
| 40.0 | 50.0 | app2 | ok | 19 | 6607ms | 9321ms | 9932ms |
| 40.0 | 50.0 | app4 | ok | 14 | 2500ms | 9000ms | 9900ms |
| 40.0 | 50.0 | app6 | ok | 10 | 5833ms | 9167ms | 9917ms |
| 40.0 | 50.0 | app3 | ok | 25 | 3264ms | 4653ms | 4965ms |
| 40.0 | 50.0 | app5 | ok | 18 | 5000ms | 9000ms | 9900ms |
| 50.0 | 60.0 | app1 | ok | 177 | 1648ms | 3525ms | 4852ms |
| 50.0 | 60.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 236 | 2300ms | 4410ms | 4941ms |
| 60.0 | 70.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 219 | 2192ms | 4392ms | 4939ms |
| 70.0 | 80.0 | app2 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 70.0 | 80.0 | app4 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 70.0 | 80.0 | app6 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 70.0 | 80.0 | app3 | ok | 6 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app5 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 80.0 | 90.0 | app1 | ok | 245 | 3572ms | 4773ms | 7958ms |
| 80.0 | 90.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 208 | 2593ms | 4519ms | 4952ms |
| 90.0 | 100.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 207 | 2730ms | 4546ms | 4955ms |
| 100.0 | 110.0 | app2 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 100.0 | 110.0 | app4 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 100.0 | 110.0 | app6 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 100.0 | 110.0 | app3 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 100.0 | 110.0 | app5 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 110.0 | 120.0 | app1 | ok | 172 | 3728ms | 7034ms | 9703ms |
| 110.0 | 120.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 290 | 3051ms | 4610ms | 4961ms |
| 120.0 | 130.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 158 | 3045ms | 4609ms | 4961ms |
| 130.0 | 140.0 | app2 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 130.0 | 140.0 | app4 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 130.0 | 140.0 | app6 | ok | 1 | 60000ms | 60000ms | 60000ms |
| 130.0 | 140.0 | app3 | ok | 1 | 60000ms | 60000ms | 60000ms |
| 130.0 | 140.0 | app5 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 140.0 | 150.0 | app1 | ok | 273 | 3072ms | 4614ms | 4961ms |
| 140.0 | 150.0 | app2 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 140.0 | 150.0 | app4 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 140.0 | 150.0 | app6 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 140.0 | 150.0 | app3 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 140.0 | 150.0 | app5 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 150.0 | 160.0 | app1 | ok | 112 | 3273ms | 6889ms | 9689ms |
| 150.0 | 160.0 | app2 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 150.0 | 160.0 | app4 | ok | 1 | 60000ms | 60000ms | 60000ms |
| 150.0 | 160.0 | app6 | ok | 3 | 60000ms | 60000ms | 60000ms |
| 150.0 | 160.0 | app3 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 150.0 | 160.0 | app5 | ok | 2 | 60000ms | 60000ms | 60000ms |
| 160.0 | 170.0 | app1 | ok | 246 | 3793ms | 5080ms | 9508ms |
| 160.0 | 170.0 | app2 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 160.0 | 170.0 | app4 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 160.0 | 170.0 | app6 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 160.0 | 170.0 | app3 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 160.0 | 170.0 | app5 | ok | 7 | 60000ms | 60000ms | 60000ms |
| 170.0 | 180.0 | app1 | ok | 218 | 3701ms | 4932ms | 9359ms |
| 170.0 | 180.0 | app2 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 170.0 | 180.0 | app4 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 170.0 | 180.0 | app6 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 170.0 | 180.0 | app3 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 170.0 | 180.0 | app5 | ok | 4 | 60000ms | 60000ms | 60000ms |
| 180.0 | 191.0 | app1 | ok | 241 | 3260ms | 4946ms | 9426ms |
| 180.0 | 191.0 | app2 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 180.0 | 191.0 | app4 | ok | 5 | 60000ms | 60000ms | 60000ms |
| 180.0 | 191.0 | app6 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 180.0 | 191.0 | app3 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 180.0 | 191.0 | app5 | ok | 7 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | app1 | ok | 88 | 3350ms | 6000ms | 9600ms |
| 191.0 | 201.0 | app2 | ok | 16 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | app4 | ok | 16 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | app6 | ok | 16 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | app3 | ok | 16 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | app5 | ok | 15 | 55000ms | 60000ms | 60000ms |
| 201.0 | 211.0 | app1 | ok | 179 | 5856ms | 9171ms | 9917ms |
| 201.0 | 211.0 | app2 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 201.0 | 211.0 | app4 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 201.0 | 211.0 | app6 | ok | 2 | 45000ms | 57000ms | 59700ms |
| 201.0 | 211.0 | app3 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 201.0 | 211.0 | app5 | ok | 2 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | app1 | ok | 119 | 5395ms | 9570ms | 26600ms |
| 211.0 | 221.0 | app2 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | app4 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | app6 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | app3 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | app5 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 221.0 | 231.0 | app1 | ok | 129 | 3168ms | 7068ms | 9707ms |
| 221.0 | 231.0 | app2 | ok | 9 | 40714ms | 56143ms | 59614ms |
| 221.0 | 231.0 | app4 | ok | 10 | 38571ms | 55714ms | 59571ms |
| 221.0 | 231.0 | app6 | ok | 9 | 43125ms | 56625ms | 59662ms |
| 221.0 | 231.0 | app3 | ok | 10 | 35000ms | 55000ms | 59500ms |
| 221.0 | 231.0 | app5 | ok | 10 | 35000ms | 55000ms | 59500ms |
| 231.0 | 241.0 | app1 | ok | 186 | 7704ms | 18000ms | 28800ms |
| 231.0 | 241.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 129 | 3078ms | 4691ms | 7850ms |
| 241.0 | 251.0 | app2 | ok | 13 | 45000ms | 57000ms | 59700ms |
| 241.0 | 251.0 | app4 | ok | 13 | 45000ms | 57000ms | 59700ms |
| 241.0 | 251.0 | app6 | ok | 13 | 45000ms | 57000ms | 59700ms |
| 241.0 | 251.0 | app3 | ok | 14 | 45000ms | 57000ms | 59700ms |
| 241.0 | 251.0 | app5 | ok | 13 | 45000ms | 57000ms | 59700ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 19 | 21875ms | 41000ms | 58100ms |
| 251.0 | 261.0 | app4 | ok | 19 | 21875ms | 41000ms | 58100ms |
| 251.0 | 261.0 | app6 | ok | 19 | 22667ms | 45750ms | 58575ms |
| 251.0 | 261.0 | app3 | ok | 18 | 22000ms | 42000ms | 58200ms |
| 251.0 | 261.0 | app5 | ok | 19 | 22667ms | 45750ms | 58575ms |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 412.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 432.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 432.0 | 442.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 492.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 492.0 | 502.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 506.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 506.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 506.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 506.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 506.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 506.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -31.9%
- app3 exceeded the 10% ledger tolerance: cost -31.8%
- app4 exceeded the 10% ledger tolerance: cost -32.8%
- app5 exceeded the 10% ledger tolerance: cost -32.6%
- app6 exceeded the 10% ledger tolerance: cost -31.8%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 5457510 | 271961 | 5659727.0 | -1.2% | 5527840.0 | 6001432.0 | -7.9% | True |
| app2 | 223860 | 11047 | 229738.0 | -2.2% | 167492.0 | 245954.0 | -31.9% | False |
| app3 | 232470 | 11566 | 229819.0 | -5.8% | 174358.0 | 255602.0 | -31.8% | False |
| app4 | 221400 | 11069 | 223430.0 | -3.9% | 163696.0 | 243538.0 | -32.8% | False |
| app5 | 226320 | 11318 | 228600.0 | -3.8% | 167768.0 | 248956.0 | -32.6% | False |
| app6 | 212790 | 10529 | 220731.0 | -1.2% | 159474.0 | 233848.0 | -31.8% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 4765 | 0 | 0 | 0 (never shed) | 0.00% | 90.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 232 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 242 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |
| app4 | 225 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |
| app5 | 229 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |
| app6 | 227 | 0 | 0 | 0 (never shed) | 0.00% | 2.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5347). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5347 | 0.051ms | 0.161ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 477009 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 4383 | 7912ms | 14411ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 178 | 22500ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app3 | ok | 178 | 22000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app4 | ok | 173 | 22778ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app5 | ok | 177 | 19583ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app6 | ok | 171 | 25625ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5345 | 8010ms | 53105ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (51 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 792ms | 1239ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 800ms | 1225ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app4 | ok | 1125ms | 1469ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app6 | ok | 800ms | 1450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app3 | ok | 700ms | 790ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app5 | ok | 1000ms | 1462ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 725ms | 1162ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 743ms | 1750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app4 | ok | 729ms | 1137ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app6 | ok | 750ms | 1062ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app3 | ok | 744ms | 1338ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app5 | ok | 729ms | 1181ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 1366ms | 1942ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 1400ms | 1925ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app4 | ok | 1386ms | 1914ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app6 | ok | 1425ms | 1997ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app3 | ok | 1321ms | 2700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app5 | ok | 1365ms | 2050ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 2776ms | 3981ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 2700ms | 3986ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app4 | ok | 2571ms | 4500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app6 | ok | 3000ms | 4200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app3 | ok | 2400ms | 3600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app5 | ok | 2700ms | 3857ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 4914ms | 7189ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 5500ms | 7760ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app4 | ok | 6000ms | 7800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app6 | ok | 4778ms | 7600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app3 | ok | 5143ms | 6600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app5 | ok | 5250ms | 7750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 5708ms | 7733ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app4 | ok | 12917ms | 18250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app6 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app3 | ok | 9900ms | 14472ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app5 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 7014ms | 9438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 6990ms | 9635ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 7619ms | 9893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app4 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app6 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app3 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app5 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 8070ms | 13161ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 7492ms | 9816ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 8529ms | 13315ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 7971ms | 13280ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 7845ms | 12393ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 7836ms | 9915ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 8203ms | 12886ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 8913ms | 14010ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app4 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app6 | ok | 110000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app3 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 8942ms | 13283ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app4 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app6 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app3 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app5 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app1 | ok | 8812ms | 12636ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app4 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app6 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app3 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 191.0 | app5 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 8611ms | 14019ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app4 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app6 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app3 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app5 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 10302ms | 14530ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 75000ms | 115500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app4 | ok | 67500ms | 114750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app6 | ok | 73333ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app3 | ok | 72000ms | 115200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app5 | ok | 73636ms | 115364ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 14014ms | 19337ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app3 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app5 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 10674ms | 14770ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app4 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app6 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app3 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app5 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 13294ms | 19174ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 46500ms | 58650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app4 | ok | 46500ms | 58650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app6 | ok | 51562ms | 59156ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app3 | ok | 47500ms | 58750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app5 | ok | 47500ms | 58750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 10513ms | 18528ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 45000ms | 58500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app4 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app6 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app3 | ok | 45000ms | 58500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app5 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 9400ms | 14125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 38571ms | 58125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app4 | ok | 35357ms | 57825ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app6 | ok | 37500ms | 57955ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app3 | ok | 38571ms | 58125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app5 | ok | 35357ms | 57825ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 412.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 412.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 412.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 412.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 412.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 412.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 492.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 492.0 | 502.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 506.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 506.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 506.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 506.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 506.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 506.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
