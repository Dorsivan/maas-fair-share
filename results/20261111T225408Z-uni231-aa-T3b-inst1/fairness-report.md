# Fairness benchmark: full-contention-2x-discriminating (uni231-aa-T3b-inst1)

**Verdict: FAIL** (threshold: 10 points)
**Secondary (priority) verdict: PRIORITY-OK** -- see "Per-tenant TTFT / ITL and the priority verdict (UNI-226)" below for detail.
Worker-share vs. weight-share gap (UNI-225): 35.1 points

- end-users deviated -11.6 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:c8a088203f6dc6c48c158d21b6295172a78f18646b06c334e5310a0caedb259f` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5fbdd988df-cws6x` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-11T22:55:19Z` |
| Run end | `2026-11-11T23:03:35Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 256 | 1269 | 000=2, 200=1242, 500=25 | 56.3 | 78.1 | 1601230.0 | 21.1% | 33.3% | 12.3 | 26.9% | 5.8 | 26.5% | 5.4 | 34.4s | 98.9% | 1244.0 |
| app2 | 10.0 | 256 | 933 | 000=1, 200=911, 500=21 | 67.0 | 142.8 | 970090.0 | 10.5% | 33.3% | 22.8 | 16.3% | 5.8 | 19.5% | 8.9 | 34.4s | 98.9% | 912.0 |
| end-users | 65.0 | 256 | 2591 | 000=13, 200=2553, 500=25 | 17.0 | 56.5 | 3386080.0 | 68.4% | 33.3% | -35.1 | 56.8% | -11.6 | 54.1% | -14.4 | 29.1s | 98.9% | 2566.0 |
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
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (50 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 10.0 | 20.0 | app1 | True | 35198.0 | 21.1% | 20.6% | -0.4 |
| 10.0 | 20.0 | app2 | True | 29800.0 | 10.5% | 17.5% | 6.9 |
| 10.0 | 20.0 | end-users | True | 105524.0 | 68.4% | 61.9% | -6.5 |
| 20.0 | 30.0 | app1 | True | 75794.0 | 21.1% | 24.6% | 3.5 |
| 20.0 | 30.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 20.0 | 30.0 | end-users | True | 232506.0 | 68.4% | 75.4% | 7.0 |
| 30.0 | 40.0 | app1 | True | 29784.0 | 21.1% | 10.2% | -10.8 |
| 30.0 | 40.0 | app2 | True | 13490.0 | 10.5% | 4.6% | -5.9 |
| 30.0 | 40.0 | end-users | True | 248638.0 | 68.4% | 85.2% | 16.8 |
| 40.0 | 51.0 | app1 | True | 66366.0 | 21.1% | 41.5% | 20.5 |
| 40.0 | 51.0 | app2 | True | 43318.0 | 10.5% | 27.1% | 16.6 |
| 40.0 | 51.0 | end-users | True | 50078.0 | 68.4% | 31.3% | -37.1 |
| 51.0 | 61.0 | app1 | True | 50130.0 | 21.1% | 33.3% | 12.3 |
| 51.0 | 61.0 | app2 | True | 21718.0 | 10.5% | 14.4% | 3.9 |
| 51.0 | 61.0 | end-users | True | 78586.0 | 68.4% | 52.2% | -16.2 |
| 61.0 | 71.0 | app1 | True | 93394.0 | 21.1% | 61.7% | 40.6 |
| 61.0 | 71.0 | app2 | True | 36486.0 | 10.5% | 24.1% | 13.6 |
| 61.0 | 71.0 | end-users | True | 21560.0 | 68.4% | 14.2% | -54.2 |
| 71.0 | 81.0 | app1 | True | 81148.0 | 21.1% | 53.1% | 32.1 |
| 71.0 | 81.0 | app2 | True | 56794.0 | 10.5% | 37.2% | 26.6 |
| 71.0 | 81.0 | end-users | True | 14858.0 | 68.4% | 9.7% | -58.7 |
| 81.0 | 91.0 | app1 | True | 25676.0 | 21.1% | 14.0% | -7.1 |
| 81.0 | 91.0 | app2 | True | 117744.0 | 10.5% | 64.0% | 53.5 |
| 81.0 | 91.0 | end-users | True | 40590.0 | 68.4% | 22.1% | -46.4 |
| 91.0 | 101.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 91.0 | 101.0 | app2 | True | 58174.0 | 10.5% | 27.4% | 16.9 |
| 91.0 | 101.0 | end-users | True | 154136.0 | 68.4% | 72.6% | 4.2 |
| 101.0 | 111.0 | app1 | True | 9494.0 | 21.1% | 3.8% | -17.2 |
| 101.0 | 111.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 101.0 | 111.0 | end-users | True | 239394.0 | 68.4% | 96.2% | 27.8 |
| 111.0 | 121.0 | app1 | True | 67574.0 | 21.1% | 21.7% | 0.7 |
| 111.0 | 121.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 111.0 | 121.0 | end-users | True | 243182.0 | 68.4% | 78.3% | 9.8 |
| 121.0 | 131.0 | app1 | True | 70312.0 | 21.1% | 23.0% | 1.9 |
| 121.0 | 131.0 | app2 | True | 8140.0 | 10.5% | 2.7% | -7.9 |
| 121.0 | 131.0 | end-users | True | 227230.0 | 68.4% | 74.3% | 5.9 |
| 131.0 | 141.0 | app1 | True | 64840.0 | 21.1% | 21.4% | 0.4 |
| 131.0 | 141.0 | app2 | True | 29744.0 | 10.5% | 9.8% | -0.7 |
| 131.0 | 141.0 | end-users | True | 208214.0 | 68.4% | 68.8% | 0.3 |
| 141.0 | 151.0 | app1 | True | 60872.0 | 21.1% | 26.5% | 5.4 |
| 141.0 | 151.0 | app2 | True | 20276.0 | 10.5% | 8.8% | -1.7 |
| 141.0 | 151.0 | end-users | True | 148908.0 | 68.4% | 64.7% | -3.7 |
| 151.0 | 161.0 | app1 | True | 29722.0 | 21.1% | 19.1% | -1.9 |
| 151.0 | 161.0 | app2 | True | 20276.0 | 10.5% | 13.0% | 2.5 |
| 151.0 | 161.0 | end-users | True | 105420.0 | 68.4% | 67.8% | -0.6 |
| 161.0 | 171.0 | app1 | True | 47320.0 | 21.1% | 31.3% | 10.2 |
| 161.0 | 171.0 | app2 | True | 21648.0 | 10.5% | 14.3% | 3.8 |
| 161.0 | 171.0 | end-users | True | 82436.0 | 68.4% | 54.4% | -14.0 |
| 171.0 | 181.0 | app1 | True | 92014.0 | 21.1% | 42.3% | 21.2 |
| 171.0 | 181.0 | app2 | True | 52660.0 | 10.5% | 24.2% | 13.7 |
| 171.0 | 181.0 | end-users | True | 73042.0 | 68.4% | 33.5% | -34.9 |
| 181.0 | 191.0 | app1 | True | 25760.0 | 21.1% | 9.2% | -11.8 |
| 181.0 | 191.0 | app2 | True | 13540.0 | 10.5% | 4.9% | -5.7 |
| 181.0 | 191.0 | end-users | True | 239336.0 | 68.4% | 85.9% | 17.5 |
| 191.0 | 201.0 | app1 | True | 62182.0 | 21.1% | 19.9% | -1.1 |
| 191.0 | 201.0 | app2 | True | 32446.0 | 10.5% | 10.4% | -0.1 |
| 191.0 | 201.0 | end-users | True | 217726.0 | 68.4% | 69.7% | 1.3 |
| 201.0 | 211.0 | app1 | True | 58186.0 | 21.1% | 19.2% | -1.9 |
| 201.0 | 211.0 | app2 | True | 77144.0 | 10.5% | 25.5% | 14.9 |
| 201.0 | 211.0 | end-users | True | 167698.0 | 68.4% | 55.3% | -13.1 |
| 211.0 | 221.0 | app1 | True | 31110.0 | 21.1% | 15.0% | -6.0 |
| 211.0 | 221.0 | app2 | True | 69038.0 | 10.5% | 33.4% | 22.8 |
| 211.0 | 221.0 | end-users | True | 106858.0 | 68.4% | 51.6% | -16.8 |
| 221.0 | 231.0 | app1 | True | 78386.0 | 21.1% | 50.8% | 29.8 |
| 221.0 | 231.0 | app2 | True | 36594.0 | 10.5% | 23.7% | 13.2 |
| 221.0 | 231.0 | end-users | True | 39226.0 | 68.4% | 25.4% | -43.0 |
| 231.0 | 241.0 | app1 | True | 94430.0 | 21.1% | 59.8% | 38.7 |
| 231.0 | 241.0 | app2 | True | 50022.0 | 10.5% | 31.7% | 21.1 |
| 231.0 | 241.0 | end-users | True | 13532.0 | 68.4% | 8.6% | -59.9 |
| 241.0 | 252.0 | app1 | False | 83842.0 | n/a | n/a | n/a |
| 241.0 | 252.0 | app2 | False | 55396.0 | n/a | n/a | n/a |
| 241.0 | 252.0 | end-users | False | 100158.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | app1 | False | 48640.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | end-users | False | 227244.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | app1 | False | 214984.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | app2 | False | 70488.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app1 | False | 4072.0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app2 | False | 35154.0 | n/a | n/a | n/a |
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
| 452.0 | 462.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 462.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 462.0 | 472.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 472.0 | 482.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 493.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 493.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 482.0 | 493.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 493.0 | 496.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 493.0 | 496.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 493.0 | 496.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 56 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 50 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 42 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 84 | 625ms | 2118ms | 2462ms |
| 10.0 | 20.0 | app2 | ok | 25 | 28ms | 312ms | 875ms |
| 10.0 | 20.0 | end-users | ok | 214 | 2145ms | 4741ms | 9177ms |
| 20.0 | 30.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 122 | 7500ms | 9500ms | 9950ms |
| 30.0 | 40.0 | app1 | ok | 257 | 17402ms | 27480ms | 29748ms |
| 30.0 | 40.0 | app2 | ok | 257 | 19961ms | 27992ms | 29799ms |
| 30.0 | 40.0 | end-users | ok | 234 | 3088ms | 8957ms | 24800ms |
| 40.0 | 51.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 51.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 51.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 51.0 | 61.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 51.0 | 61.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 51.0 | 61.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 61.0 | 71.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 61.0 | 71.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 61.0 | 71.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 71.0 | 81.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 71.0 | 81.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 71.0 | 81.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 81.0 | 91.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 81.0 | 91.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 202 | 45000ms | 57000ms | 59700ms |
| 91.0 | 101.0 | app1 | ok | 20 | 60000ms | 60000ms | 60000ms |
| 91.0 | 101.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 150 | 9407ms | 46364ms | 58636ms |
| 101.0 | 111.0 | app1 | ok | 23 | 60000ms | 60000ms | 60000ms |
| 101.0 | 111.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 93 | 8370ms | 22250ms | 29225ms |
| 111.0 | 121.0 | app1 | ok | 40 | 60000ms | 60000ms | 60000ms |
| 111.0 | 121.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 133 | 13165ms | 26633ms | 29663ms |
| 121.0 | 131.0 | app1 | ok | 48 | 60000ms | 60000ms | 60000ms |
| 121.0 | 131.0 | app2 | ok | 16 | 60000ms | 60000ms | 60000ms |
| 121.0 | 131.0 | end-users | ok | 169 | 9747ms | 25775ms | 29578ms |
| 131.0 | 141.0 | app1 | ok | 45 | 60000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | app2 | ok | 22 | 60000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | end-users | ok | 128 | 18037ms | 27607ms | 29761ms |
| 141.0 | 151.0 | app1 | ok | 164 | 38571ms | 60000ms | 60000ms |
| 141.0 | 151.0 | app2 | ok | 81 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | end-users | ok | 202 | 6400ms | 21404ms | 29140ms |
| 151.0 | 161.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 151.0 | 161.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 151.0 | 161.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 161.0 | 171.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 161.0 | 171.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 161.0 | 171.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 171.0 | 181.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 171.0 | 181.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 156 | 27931ms | 53217ms | 59322ms |
| 181.0 | 191.0 | app1 | ok | 27 | 45000ms | 57000ms | 59700ms |
| 181.0 | 191.0 | app2 | ok | 15 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | end-users | ok | 143 | 16509ms | 27302ms | 29730ms |
| 191.0 | 201.0 | app1 | ok | 270 | 29394ms | 56471ms | 60000ms |
| 191.0 | 201.0 | app2 | ok | 144 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | end-users | ok | 308 | 6861ms | 14976ms | 28498ms |
| 201.0 | 211.0 | app1 | ok | 12 | 1214ms | 2243ms | 2474ms |
| 201.0 | 211.0 | app2 | ok | 83 | 38700ms | 58620ms | 60000ms |
| 201.0 | 211.0 | end-users | ok | 30 | 1000ms | 2200ms | 2470ms |
| 211.0 | 221.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 211.0 | 221.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 211.0 | 221.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 252.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 252.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 252.0 | end-users | ok | 160 | 43893ms | 56779ms | 59678ms |
| 252.0 | 262.0 | app1 | ok | 124 | 43966ms | 56793ms | 59679ms |
| 252.0 | 262.0 | app2 | ok | 23 | 60000ms | 60000ms | 60000ms |
| 252.0 | 262.0 | end-users | ok | 80 | 39661ms | 55932ms | 59593ms |
| 262.0 | 272.0 | app1 | ok | 74 | 21385ms | 35333ms | 57533ms |
| 262.0 | 272.0 | app2 | ok | 187 | 47422ms | 60000ms | 60000ms |
| 262.0 | 272.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app2 | ok | 9 | 45000ms | 57000ms | 59700ms |
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
| 452.0 | 462.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 462.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 462.0 | 472.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 472.0 | 482.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 493.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 493.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 482.0 | 493.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 493.0 | 496.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 493.0 | 496.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 493.0 | 496.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -21.3%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1527660 | 76017 | 1603677.0 | 0.0% | 1601230.0 | 1679694.0 | -4.7% | True |
| app2 | 1120530 | 56038 | 1176568.0 | 0.0% | 970090.0 | 1232606.0 | -21.3% | False |
| end-users | 3140190 | 156099 | 3296289.0 | 0.0% | 3386080.0 | 3452388.0 | -1.9% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1269 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 933 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2591 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=4722). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 4722 | 0.055ms | 0.289ms | (0, 0.1]ms | (0.2, 0.5]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 460050 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1242 | 54883ms | 112821ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 911 | 75904ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 2553 | 18178ms | 53282ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 4706 | 33512ms | 112002ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: PRIORITY-OK** -- the share verdict above is FAIL, so this is the board's second, independent success criterion (2026-11-10): did the policy nonetheless order tenants by weight? Top-weighted group: `end-users` (TTFT p50 18178ms, p95 53282ms, strictly lowest among distinctly-weighted groups: p50=True/p95=True; no rank inversion among any distinctly-weighted pair: True -- this, not raw rank correlation, is what gates the verdict, since a genuine weight tie (e.g. 98/1/1's app2==end-users) makes exact correlation 1.0 unreachable by construction even when ordering is otherwise perfect). Rank correlation 1.00 (1.00 = exact agreement, informational only) shown for reference. Separation from the next distinctly-weighted group: 36705ms against a noise floor of not given (separation check skipped).

**Windowed TTFT/ITL** (50 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 780ms | 1221ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 733ms | 1150ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 730ms | 1169ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 3917ms | 7383ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 3929ms | 7608ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 4542ms | 7500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 12021ms | 14702ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 9077ms | 14232ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 24500ms | 29450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 12523ms | 18783ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 51.0 | app1 | ok | 27903ms | 42958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 51.0 | app2 | ok | 34565ms | 43957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 51.0 | end-users | ok | 12643ms | 20750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app2 | ok | 40000ms | 57000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | end-users | ok | 26905ms | 42281ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app1 | ok | 51078ms | 59108ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app2 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app2 | ok | 58125ms | 113000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | end-users | ok | 49688ms | 58969ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 34792ms | 57926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 14639ms | 19568ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 13818ms | 19276ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 16031ms | 19603ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 83514ms | 116351ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 17277ms | 19728ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 23810ms | 29381ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 55408ms | 109263ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 55962ms | 110500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 32821ms | 43782ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 13797ms | 26500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 80909ms | 116091ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 68400ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 15888ms | 19589ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 87143ms | 116714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 39808ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 24275ms | 29428ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 89565ms | 116957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 120000ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 252.0 | app1 | ok | 55109ms | 108375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 252.0 | app2 | ok | 115909ms | 120000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 252.0 | end-users | ok | 40817ms | 57554ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | app1 | ok | 50357ms | 59036ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | end-users | ok | 39823ms | 57200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | app1 | ok | 37431ms | 55230ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 272.0 | 282.0 | app1 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 272.0 | 282.0 | app2 | ok | 58404ms | 113571ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 452.0 | 462.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 462.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 462.0 | 472.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 472.0 | 482.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 493.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 493.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 482.0 | 493.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 493.0 | 496.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 493.0 | 496.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 493.0 | 496.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
