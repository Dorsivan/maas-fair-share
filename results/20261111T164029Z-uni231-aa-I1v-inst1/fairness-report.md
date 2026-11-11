# Fairness benchmark: full-contention-2x-discriminating (uni231-aa-I1v-inst1)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 35.1 points

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:c8a088203f6dc6c48c158d21b6295172a78f18646b06c334e5310a0caedb259f` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5fbdd988df-jh647` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-11T16:41:45Z` |
| Run end | `2026-11-11T16:49:26Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 256 | 1290 | 000=1, 200=1289 | 54.7 | 66.4 | 1672328.0 | 21.1% | 33.3% | 12.3 | 23.4% | 2.4 | 23.5% | 2.4 | 66.6s | 98.9% | 1290.0 |
| app2 | 10.0 | 256 | 781 | 200=781 | 96.6 | 124.8 | 889636.0 | 10.5% | 33.3% | 22.8 | 12.5% | 1.9 | 14.2% | 3.7 | 66.6s | 98.9% | 781.0 |
| end-users | 65.0 | 256 | 3428 | 000=4, 200=3424 | 16.5 | 32.9 | 4573802.0 | 68.4% | 33.3% | -35.1 | 64.1% | -4.3 | 62.3% | -6.1 | 61.1s | 98.9% | 3428.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

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
| 0.0 | 151.0 | 151.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (46 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 10.0 | 21.0 | app1 | True | 29740.0 | 21.1% | 15.4% | -5.7 |
| 10.0 | 21.0 | app2 | True | 33836.0 | 10.5% | 17.5% | 7.0 |
| 10.0 | 21.0 | end-users | True | 129706.0 | 68.4% | 67.1% | -1.3 |
| 21.0 | 31.0 | app1 | True | 41984.0 | 21.1% | 14.1% | -6.9 |
| 21.0 | 31.0 | app2 | True | 4068.0 | 10.5% | 1.4% | -9.2 |
| 21.0 | 31.0 | end-users | True | 251606.0 | 68.4% | 84.5% | 16.1 |
| 31.0 | 41.0 | app1 | True | 67704.0 | 21.1% | 21.8% | 0.7 |
| 31.0 | 41.0 | app2 | True | 16210.0 | 10.5% | 5.2% | -5.3 |
| 31.0 | 41.0 | end-users | True | 227098.0 | 68.4% | 73.0% | 4.6 |
| 41.0 | 51.0 | app1 | True | 63614.0 | 21.1% | 21.2% | 0.1 |
| 41.0 | 51.0 | app2 | True | 32456.0 | 10.5% | 10.8% | 0.3 |
| 41.0 | 51.0 | end-users | True | 204256.0 | 68.4% | 68.0% | -0.4 |
| 51.0 | 61.0 | app1 | True | 64912.0 | 21.1% | 20.9% | -0.2 |
| 51.0 | 61.0 | app2 | True | 33852.0 | 10.5% | 10.9% | 0.4 |
| 51.0 | 61.0 | end-users | True | 212360.0 | 68.4% | 68.3% | -0.2 |
| 61.0 | 71.0 | app1 | True | 64854.0 | 21.1% | 21.2% | 0.2 |
| 61.0 | 71.0 | app2 | True | 32488.0 | 10.5% | 10.6% | 0.1 |
| 61.0 | 71.0 | end-users | True | 208376.0 | 68.4% | 68.2% | -0.3 |
| 71.0 | 81.0 | app1 | True | 62228.0 | 21.1% | 20.1% | -0.9 |
| 71.0 | 81.0 | app2 | True | 33764.0 | 10.5% | 10.9% | 0.4 |
| 71.0 | 81.0 | end-users | True | 213462.0 | 68.4% | 69.0% | 0.6 |
| 81.0 | 91.0 | app1 | True | 69026.0 | 21.1% | 22.9% | 1.8 |
| 81.0 | 91.0 | app2 | True | 32518.0 | 10.5% | 10.8% | 0.3 |
| 81.0 | 91.0 | end-users | True | 200108.0 | 68.4% | 66.3% | -2.1 |
| 91.0 | 101.0 | app1 | True | 51368.0 | 21.1% | 21.1% | 0.1 |
| 91.0 | 101.0 | app2 | True | 21604.0 | 10.5% | 8.9% | -1.6 |
| 91.0 | 101.0 | end-users | True | 170322.0 | 68.4% | 70.0% | 1.6 |
| 101.0 | 111.0 | app1 | True | 26950.0 | 21.1% | 17.3% | -3.7 |
| 101.0 | 111.0 | app2 | True | 18890.0 | 10.5% | 12.2% | 1.6 |
| 101.0 | 111.0 | end-users | True | 109514.0 | 68.4% | 70.5% | 2.1 |
| 111.0 | 121.0 | app1 | True | 74278.0 | 21.1% | 47.0% | 26.0 |
| 111.0 | 121.0 | app2 | True | 32336.0 | 10.5% | 20.5% | 10.0 |
| 111.0 | 121.0 | end-users | True | 51304.0 | 68.4% | 32.5% | -35.9 |
| 121.0 | 131.0 | app1 | True | 91922.0 | 21.1% | 53.1% | 32.1 |
| 121.0 | 131.0 | app2 | True | 48598.0 | 10.5% | 28.1% | 17.6 |
| 121.0 | 131.0 | end-users | True | 32488.0 | 68.4% | 18.8% | -49.6 |
| 131.0 | 141.0 | app1 | True | 41854.0 | 21.1% | 15.1% | -6.0 |
| 131.0 | 141.0 | app2 | True | 20286.0 | 10.5% | 7.3% | -3.2 |
| 131.0 | 141.0 | end-users | True | 215000.0 | 68.4% | 77.6% | 9.2 |
| 141.0 | 151.0 | app1 | True | 37816.0 | 21.1% | 12.1% | -8.9 |
| 141.0 | 151.0 | app2 | True | 20244.0 | 10.5% | 6.5% | -4.0 |
| 141.0 | 151.0 | end-users | True | 254142.0 | 68.4% | 81.4% | 13.0 |
| 151.0 | 161.0 | app1 | True | 62206.0 | 21.1% | 20.9% | -0.1 |
| 151.0 | 161.0 | app2 | True | 31092.0 | 10.5% | 10.5% | -0.1 |
| 151.0 | 161.0 | end-users | True | 204228.0 | 68.4% | 68.6% | 0.2 |
| 161.0 | 171.0 | app1 | True | 50024.0 | 21.1% | 20.8% | -0.3 |
| 161.0 | 171.0 | app2 | True | 25622.0 | 10.5% | 10.6% | 0.1 |
| 161.0 | 171.0 | end-users | True | 165076.0 | 68.4% | 68.6% | 0.2 |
| 171.0 | 181.0 | app1 | True | 45980.0 | 21.1% | 21.1% | 0.1 |
| 171.0 | 181.0 | app2 | True | 23034.0 | 10.5% | 10.6% | 0.1 |
| 171.0 | 181.0 | end-users | True | 148758.0 | 68.4% | 68.3% | -0.1 |
| 181.0 | 191.0 | app1 | True | 56792.0 | 21.1% | 21.5% | 0.5 |
| 181.0 | 191.0 | app2 | True | 27028.0 | 10.5% | 10.2% | -0.3 |
| 181.0 | 191.0 | end-users | True | 179938.0 | 68.4% | 68.2% | -0.2 |
| 191.0 | 201.0 | app1 | True | 60776.0 | 21.1% | 20.3% | -0.7 |
| 191.0 | 201.0 | app2 | True | 33818.0 | 10.5% | 11.3% | 0.8 |
| 191.0 | 201.0 | end-users | True | 204448.0 | 68.4% | 68.4% | -0.1 |
| 201.0 | 211.0 | app1 | True | 66286.0 | 21.1% | 21.8% | 0.7 |
| 201.0 | 211.0 | app2 | True | 31170.0 | 10.5% | 10.2% | -0.3 |
| 201.0 | 211.0 | end-users | True | 206912.0 | 68.4% | 68.0% | -0.4 |
| 211.0 | 221.0 | app1 | True | 63534.0 | 21.1% | 21.2% | 0.1 |
| 211.0 | 221.0 | app2 | True | 32452.0 | 10.5% | 10.8% | 0.3 |
| 211.0 | 221.0 | end-users | True | 204232.0 | 68.4% | 68.0% | -0.4 |
| 221.0 | 231.0 | app1 | True | 68926.0 | 21.1% | 22.4% | 1.3 |
| 221.0 | 231.0 | app2 | True | 29800.0 | 10.5% | 9.7% | -0.9 |
| 221.0 | 231.0 | end-users | True | 209478.0 | 68.4% | 68.0% | -0.5 |
| 231.0 | 242.0 | app1 | True | 59498.0 | 21.1% | 19.4% | -1.7 |
| 231.0 | 242.0 | app2 | True | 35184.0 | 10.5% | 11.5% | 0.9 |
| 231.0 | 242.0 | end-users | True | 212300.0 | 68.4% | 69.2% | 0.7 |
| 242.0 | 252.0 | app1 | False | 64816.0 | n/a | n/a | n/a |
| 242.0 | 252.0 | app2 | False | 32432.0 | n/a | n/a | n/a |
| 242.0 | 252.0 | end-users | False | 207078.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | app1 | False | 102808.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | app2 | False | 50050.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | end-users | False | 151612.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | app1 | False | 182432.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | app2 | False | 105494.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app2 | False | 51310.0 | n/a | n/a | n/a |
| 272.0 | 282.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 282.0 | 292.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 282.0 | 292.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 282.0 | 292.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 292.0 | 302.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 292.0 | 302.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 292.0 | 302.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 302.0 | 312.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 302.0 | 312.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 302.0 | 312.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 312.0 | 322.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 312.0 | 322.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 312.0 | 322.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 322.0 | 332.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 332.0 | 342.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 342.0 | 352.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 352.0 | 362.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | end-users | False | 0.0 | n/a | n/a | n/a |
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
| 442.0 | 452.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 442.0 | 452.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 461.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 461.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 461.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 52 | 0ms | 0ms | 1ms |
| 0.0 | 10.0 | app2 | ok | 42 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 42 | 0ms | 0ms | 1ms |
| 10.0 | 21.0 | app1 | ok | 22 | 325ms | 725ms | 973ms |
| 10.0 | 21.0 | app2 | ok | 28 | 354ms | 800ms | 980ms |
| 10.0 | 21.0 | end-users | ok | 170 | 2665ms | 4533ms | 4953ms |
| 21.0 | 31.0 | app1 | ok | 60 | 11818ms | 26364ms | 29636ms |
| 21.0 | 31.0 | app2 | ok | 4 | 20000ms | 28000ms | 29800ms |
| 21.0 | 31.0 | end-users | ok | 208 | 8171ms | 20545ms | 29055ms |
| 31.0 | 41.0 | app1 | ok | 39 | 20000ms | 28000ms | 29800ms |
| 31.0 | 41.0 | app2 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 31.0 | 41.0 | end-users | ok | 129 | 10154ms | 26031ms | 29603ms |
| 41.0 | 51.0 | app1 | ok | 56 | 40909ms | 56182ms | 59618ms |
| 41.0 | 51.0 | app2 | ok | 28 | 40909ms | 56182ms | 59618ms |
| 41.0 | 51.0 | end-users | ok | 181 | 19944ms | 27989ms | 29799ms |
| 51.0 | 61.0 | app1 | ok | 49 | 45000ms | 57000ms | 59700ms |
| 51.0 | 61.0 | app2 | ok | 24 | 45000ms | 57000ms | 59700ms |
| 51.0 | 61.0 | end-users | ok | 160 | 20000ms | 28000ms | 29800ms |
| 61.0 | 71.0 | app1 | ok | 35 | 45000ms | 57000ms | 59700ms |
| 61.0 | 71.0 | app2 | ok | 24 | 45000ms | 57000ms | 59700ms |
| 61.0 | 71.0 | end-users | ok | 115 | 20000ms | 28000ms | 29800ms |
| 71.0 | 81.0 | app1 | ok | 56 | 45000ms | 57000ms | 59700ms |
| 71.0 | 81.0 | app2 | ok | 22 | 60000ms | 60000ms | 60000ms |
| 71.0 | 81.0 | end-users | ok | 177 | 19943ms | 27989ms | 29799ms |
| 81.0 | 91.0 | app1 | ok | 82 | 45000ms | 57000ms | 59700ms |
| 81.0 | 91.0 | app2 | ok | 41 | 60000ms | 60000ms | 60000ms |
| 81.0 | 91.0 | end-users | ok | 270 | 10435ms | 26087ms | 29609ms |
| 91.0 | 101.0 | app1 | ok | 157 | 25104ms | 51436ms | 59144ms |
| 91.0 | 101.0 | app2 | ok | 78 | 60000ms | 60000ms | 60000ms |
| 91.0 | 101.0 | end-users | ok | 66 | 1960ms | 4312ms | 4931ms |
| 101.0 | 111.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 101.0 | 111.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 101.0 | 111.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 111.0 | 121.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 111.0 | 121.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 111.0 | 121.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 121.0 | 131.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 121.0 | 131.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 154 | 38807ms | 55761ms | 59576ms |
| 131.0 | 141.0 | app1 | ok | 11 | 45000ms | 57000ms | 59700ms |
| 131.0 | 141.0 | app2 | ok | 6 | 60000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | end-users | ok | 138 | 18539ms | 37000ms | 57700ms |
| 141.0 | 151.0 | app1 | ok | 48 | 45000ms | 57000ms | 59700ms |
| 141.0 | 151.0 | app2 | ok | 24 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | end-users | ok | 175 | 7589ms | 9660ms | 24167ms |
| 151.0 | 161.0 | app1 | ok | 33 | 45000ms | 57000ms | 59700ms |
| 151.0 | 161.0 | app2 | ok | 17 | 60000ms | 60000ms | 60000ms |
| 151.0 | 161.0 | end-users | ok | 101 | 17051ms | 27410ms | 29741ms |
| 161.0 | 171.0 | app1 | ok | 47 | 45000ms | 57000ms | 59700ms |
| 161.0 | 171.0 | app2 | ok | 24 | 60000ms | 60000ms | 60000ms |
| 161.0 | 171.0 | end-users | ok | 156 | 9221ms | 25273ms | 29527ms |
| 171.0 | 181.0 | app1 | ok | 35 | 45000ms | 57000ms | 59700ms |
| 171.0 | 181.0 | app2 | ok | 18 | 60000ms | 60000ms | 60000ms |
| 171.0 | 181.0 | end-users | ok | 111 | 20000ms | 28000ms | 29800ms |
| 181.0 | 191.0 | app1 | ok | 51 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | app2 | ok | 26 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | end-users | ok | 163 | 18440ms | 27688ms | 29769ms |
| 191.0 | 201.0 | app1 | ok | 37 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | app2 | ok | 18 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | end-users | ok | 124 | 17600ms | 27520ms | 29752ms |
| 201.0 | 211.0 | app1 | ok | 42 | 45000ms | 57000ms | 59700ms |
| 201.0 | 211.0 | app2 | ok | 20 | 60000ms | 60000ms | 60000ms |
| 201.0 | 211.0 | end-users | ok | 136 | 17523ms | 27505ms | 29750ms |
| 211.0 | 221.0 | app1 | ok | 48 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | app2 | ok | 24 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | end-users | ok | 155 | 15648ms | 27130ms | 29713ms |
| 221.0 | 231.0 | app1 | ok | 45 | 45000ms | 57000ms | 59700ms |
| 221.0 | 231.0 | app2 | ok | 23 | 60000ms | 60000ms | 60000ms |
| 221.0 | 231.0 | end-users | ok | 147 | 18692ms | 27738ms | 29774ms |
| 231.0 | 242.0 | app1 | ok | 48 | 45000ms | 57000ms | 59700ms |
| 231.0 | 242.0 | app2 | ok | 23 | 60000ms | 60000ms | 60000ms |
| 231.0 | 242.0 | end-users | ok | 155 | 18519ms | 27704ms | 29770ms |
| 242.0 | 252.0 | app1 | ok | 51 | 45000ms | 57000ms | 59700ms |
| 242.0 | 252.0 | app2 | ok | 26 | 60000ms | 60000ms | 60000ms |
| 242.0 | 252.0 | end-users | ok | 164 | 19686ms | 27937ms | 29794ms |
| 252.0 | 262.0 | app1 | ok | 105 | 45000ms | 57000ms | 59700ms |
| 252.0 | 262.0 | app2 | ok | 52 | 60000ms | 60000ms | 60000ms |
| 252.0 | 262.0 | end-users | ok | 31 | 20000ms | 28000ms | 29800ms |
| 262.0 | 272.0 | app1 | ok | 81 | 29286ms | 53769ms | 59377ms |
| 262.0 | 272.0 | app2 | ok | 147 | 60000ms | 60000ms | 60000ms |
| 262.0 | 272.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app2 | ok | 24 | 43636ms | 56727ms | 59673ms |
| 272.0 | 282.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 282.0 | 292.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 282.0 | 292.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 282.0 | 292.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 292.0 | 302.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 292.0 | 302.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 292.0 | 302.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 302.0 | 312.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 302.0 | 312.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 302.0 | 312.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 312.0 | 322.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 312.0 | 322.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 312.0 | 322.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 322.0 | 332.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 342.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 342.0 | 352.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 352.0 | 362.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 362.0 | 372.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 372.0 | 382.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 442.0 | 452.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 442.0 | 452.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 461.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 461.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 461.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -15.8%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1585470 | 78534 | 1664004.0 | 0.0% | 1672328.0 | 1742538.0 | -4.0% | True |
| app2 | 960630 | 47709 | 1008339.0 | 0.0% | 889636.0 | 1056048.0 | -15.8% | False |
| end-users | 4211520 | 209537 | 4421057.0 | 0.0% | 4573802.0 | 4630594.0 | -1.2% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1290 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 781 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3428 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5499). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5499 | 0.055ms | 0.218ms | (0, 0.1]ms | (0.2, 0.5]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 420849 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1289 | 52083ms | 108317ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 781 | 84868ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3424 | 17023ms | 33536ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5494 | 19279ms | 110996ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (46 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 738ms | 1250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 757ms | 1196ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 825ms | 1287ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 21.0 | app1 | ok | 3857ms | 7743ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 21.0 | app2 | ok | 4000ms | 9775ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 21.0 | end-users | ok | 4950ms | 8656ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 21.0 | 31.0 | app1 | ok | 15921ms | 19592ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 21.0 | 31.0 | app2 | ok | 9500ms | 14250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 21.0 | 31.0 | end-users | ok | 12061ms | 14889ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 31.0 | 41.0 | app1 | ok | 24681ms | 29468ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 31.0 | 41.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 31.0 | 41.0 | end-users | ok | 14330ms | 19408ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | app1 | ok | 36402ms | 44140ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | app2 | ok | 36818ms | 44182ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | end-users | ok | 16370ms | 19637ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app1 | ok | 39730ms | 56727ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app2 | ok | 41719ms | 57917ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | end-users | ok | 17156ms | 19716ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app2 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | end-users | ok | 17061ms | 19706ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app1 | ok | 53023ms | 74000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app2 | ok | 85909ms | 116591ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | end-users | ok | 17179ms | 19718ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 16917ms | 19692ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 16881ms | 19688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 52895ms | 60000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 21900ms | 29190ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 81628ms | 116163ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 53226ms | 86000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 37453ms | 44245ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 14896ms | 41643ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 98333ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 14339ms | 19410ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 59605ms | 113833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 95625ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 17222ms | 19764ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 56591ms | 111500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 22029ms | 29203ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 24267ms | 29427ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 18341ms | 28013ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 86591ms | 116659ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 17424ms | 21500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 67778ms | 114778ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 16537ms | 19654ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 55929ms | 110437ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 115000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 17232ms | 19723ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 242.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 242.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 242.0 | end-users | ok | 16824ms | 19719ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 242.0 | 252.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 242.0 | 252.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 242.0 | 252.0 | end-users | ok | 16458ms | 19646ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | app1 | ok | 50656ms | 59066ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | app2 | ok | 115500ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | end-users | ok | 16923ms | 19692ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | app1 | ok | 38218ms | 55950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | app2 | ok | 87143ms | 116714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 272.0 | 282.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 272.0 | 282.0 | app2 | ok | 53958ms | 111711ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 272.0 | 282.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 282.0 | 292.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 282.0 | 292.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 282.0 | 292.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 292.0 | 302.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 292.0 | 302.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 292.0 | 302.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 302.0 | 312.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 302.0 | 312.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 302.0 | 312.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 372.0 | 382.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 382.0 | 392.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 392.0 | 402.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 402.0 | 412.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 412.0 | 422.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 432.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 432.0 | 442.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 442.0 | 452.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 461.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 461.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 461.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
