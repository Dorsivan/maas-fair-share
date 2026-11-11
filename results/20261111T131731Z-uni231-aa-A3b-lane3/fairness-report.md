# Fairness benchmark: full-contention-2x-discriminating (uni231-aa-A3b-lane3)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-6668d94f5f-t2m5p` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-11T13:18:42Z` |
| Run end | `2026-11-11T13:26:37Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 256 | 1334 | 000=1, 200=1333 | 53.0 | 57.2 | 1715364.0 | 21.1% | 33.3% | 12.3 | 23.0% | 2.0 | 23.0% | 1.9 | 85.8s | 98.9% | 1334.0 |
| app2 | 10.0 | 256 | 805 | 000=1, 200=804 | 91.9 | 112.3 | 852798.0 | 10.5% | 33.3% | 22.8 | 11.5% | 0.9 | 13.9% | 3.3 | 85.8s | 98.9% | 805.0 |
| end-users | 65.0 | 256 | 3665 | 000=2, 200=3663 | 16.1 | 19.2 | 4876092.0 | 68.4% | 33.3% | -35.1 | 65.5% | -2.9 | 63.1% | -5.3 | 81.2s | 98.9% | 3665.0 |
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
| 0.0 | 71.0 | 71.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (48 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 10.0 | 21.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 10.0 | 21.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 10.0 | 21.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 21.0 | 31.0 | app1 | True | 27036.0 | 21.1% | 10.4% | -10.7 |
| 21.0 | 31.0 | app2 | True | 33840.0 | 10.5% | 13.0% | 2.4 |
| 21.0 | 31.0 | end-users | True | 199986.0 | 68.4% | 76.7% | 8.2 |
| 31.0 | 41.0 | app1 | True | 117604.0 | 21.1% | 38.5% | 17.5 |
| 31.0 | 41.0 | app2 | True | 5408.0 | 10.5% | 1.8% | -8.8 |
| 31.0 | 41.0 | end-users | True | 182426.0 | 68.4% | 59.7% | -8.7 |
| 41.0 | 51.0 | app1 | True | 70290.0 | 21.1% | 22.6% | 1.6 |
| 41.0 | 51.0 | app2 | True | 28414.0 | 10.5% | 9.1% | -1.4 |
| 41.0 | 51.0 | end-users | True | 212108.0 | 68.4% | 68.2% | -0.2 |
| 51.0 | 61.0 | app1 | True | 47366.0 | 21.1% | 16.4% | -4.7 |
| 51.0 | 61.0 | app2 | True | 21660.0 | 10.5% | 7.5% | -3.0 |
| 51.0 | 61.0 | end-users | True | 220262.0 | 68.4% | 76.1% | 7.7 |
| 61.0 | 71.0 | app1 | True | 28332.0 | 21.1% | 10.1% | -10.9 |
| 61.0 | 71.0 | app2 | True | 16212.0 | 10.5% | 5.8% | -4.7 |
| 61.0 | 71.0 | end-users | True | 235230.0 | 68.4% | 84.1% | 15.7 |
| 71.0 | 81.0 | app1 | True | 66268.0 | 21.1% | 21.8% | 0.7 |
| 71.0 | 81.0 | app2 | True | 33810.0 | 10.5% | 11.1% | 0.6 |
| 71.0 | 81.0 | end-users | True | 204282.0 | 68.4% | 67.1% | -1.3 |
| 81.0 | 91.0 | app1 | True | 66292.0 | 21.1% | 21.5% | 0.5 |
| 81.0 | 91.0 | app2 | True | 31116.0 | 10.5% | 10.1% | -0.4 |
| 81.0 | 91.0 | end-users | True | 210858.0 | 68.4% | 68.4% | -0.0 |
| 91.0 | 101.0 | app1 | True | 56796.0 | 21.1% | 21.2% | 0.2 |
| 91.0 | 101.0 | app2 | True | 29728.0 | 10.5% | 11.1% | 0.6 |
| 91.0 | 101.0 | end-users | True | 181098.0 | 68.4% | 67.7% | -0.8 |
| 101.0 | 111.0 | app1 | True | 66242.0 | 21.1% | 21.8% | 0.7 |
| 101.0 | 111.0 | app2 | True | 32422.0 | 10.5% | 10.7% | 0.1 |
| 101.0 | 111.0 | end-users | True | 205368.0 | 68.4% | 67.5% | -0.9 |
| 111.0 | 121.0 | app1 | True | 64696.0 | 21.1% | 21.2% | 0.1 |
| 111.0 | 121.0 | app2 | True | 30998.0 | 10.5% | 10.2% | -0.4 |
| 111.0 | 121.0 | end-users | True | 209672.0 | 68.4% | 68.7% | 0.2 |
| 121.0 | 131.0 | app1 | True | 62202.0 | 21.1% | 20.6% | -0.5 |
| 121.0 | 131.0 | app2 | True | 31120.0 | 10.5% | 10.3% | -0.2 |
| 121.0 | 131.0 | end-users | True | 209312.0 | 68.4% | 69.2% | 0.7 |
| 131.0 | 141.0 | app1 | True | 62242.0 | 21.1% | 20.5% | -0.6 |
| 131.0 | 141.0 | app2 | True | 32462.0 | 10.5% | 10.7% | 0.1 |
| 131.0 | 141.0 | end-users | True | 209518.0 | 68.4% | 68.9% | 0.4 |
| 141.0 | 151.0 | app1 | True | 63504.0 | 21.1% | 21.1% | 0.0 |
| 141.0 | 151.0 | app2 | True | 32490.0 | 10.5% | 10.8% | 0.3 |
| 141.0 | 151.0 | end-users | True | 205430.0 | 68.4% | 68.2% | -0.3 |
| 151.0 | 161.0 | app1 | True | 63528.0 | 21.1% | 20.9% | -0.2 |
| 151.0 | 161.0 | app2 | True | 32430.0 | 10.5% | 10.7% | 0.1 |
| 151.0 | 161.0 | end-users | True | 208234.0 | 68.4% | 68.5% | 0.0 |
| 161.0 | 171.0 | app1 | True | 65010.0 | 21.1% | 21.3% | 0.2 |
| 161.0 | 171.0 | app2 | True | 32414.0 | 10.5% | 10.6% | 0.1 |
| 161.0 | 171.0 | end-users | True | 208202.0 | 68.4% | 68.1% | -0.3 |
| 171.0 | 181.0 | app1 | True | 58032.0 | 21.1% | 20.7% | -0.3 |
| 171.0 | 181.0 | app2 | True | 29612.0 | 10.5% | 10.6% | 0.1 |
| 171.0 | 181.0 | end-users | True | 192164.0 | 68.4% | 68.7% | 0.3 |
| 181.0 | 191.0 | app1 | True | 64882.0 | 21.1% | 21.3% | 0.3 |
| 181.0 | 191.0 | app2 | True | 32396.0 | 10.5% | 10.7% | 0.1 |
| 181.0 | 191.0 | end-users | True | 206794.0 | 68.4% | 68.0% | -0.4 |
| 191.0 | 201.0 | app1 | True | 63484.0 | 21.1% | 20.8% | -0.3 |
| 191.0 | 201.0 | app2 | True | 31078.0 | 10.5% | 10.2% | -0.3 |
| 191.0 | 201.0 | end-users | True | 210794.0 | 68.4% | 69.0% | 0.6 |
| 201.0 | 211.0 | app1 | True | 64872.0 | 21.1% | 21.8% | 0.8 |
| 201.0 | 211.0 | app2 | True | 32490.0 | 10.5% | 10.9% | 0.4 |
| 201.0 | 211.0 | end-users | True | 200164.0 | 68.4% | 67.3% | -1.1 |
| 211.0 | 221.0 | app1 | True | 63550.0 | 21.1% | 20.8% | -0.2 |
| 211.0 | 221.0 | app2 | True | 31138.0 | 10.5% | 10.2% | -0.3 |
| 211.0 | 221.0 | end-users | True | 210802.0 | 68.4% | 69.0% | 0.6 |
| 221.0 | 232.0 | app1 | True | 58104.0 | 21.1% | 21.5% | 0.4 |
| 221.0 | 232.0 | app2 | True | 27098.0 | 10.5% | 10.0% | -0.5 |
| 221.0 | 232.0 | end-users | True | 185300.0 | 68.4% | 68.5% | 0.1 |
| 232.0 | 242.0 | app1 | True | 63698.0 | 21.1% | 20.8% | -0.2 |
| 232.0 | 242.0 | app2 | True | 33800.0 | 10.5% | 11.1% | 0.5 |
| 232.0 | 242.0 | end-users | True | 208232.0 | 68.4% | 68.1% | -0.3 |
| 242.0 | 252.0 | app1 | False | 63422.0 | n/a | n/a | n/a |
| 242.0 | 252.0 | app2 | False | 31080.0 | n/a | n/a | n/a |
| 242.0 | 252.0 | end-users | False | 208340.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | app1 | False | 102750.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | app2 | False | 52684.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | end-users | False | 151516.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | app1 | False | 185162.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | app2 | False | 112116.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app2 | False | 14782.0 | n/a | n/a | n/a |
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
| 452.0 | 463.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 463.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 452.0 | 463.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 463.0 | 473.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 463.0 | 473.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 463.0 | 473.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 473.0 | 475.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 473.0 | 475.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 473.0 | 475.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 1 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 21.0 | app1 | ok | 83 | 0ms | 334ms | 862ms |
| 10.0 | 21.0 | app2 | ok | 96 | 0ms | 520ms | 952ms |
| 10.0 | 21.0 | end-users | ok | 90 | 0ms | 404ms | 887ms |
| 21.0 | 31.0 | app1 | ok | 46 | 7500ms | 9500ms | 9950ms |
| 21.0 | 31.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 21.0 | 31.0 | end-users | ok | 176 | 2582ms | 4516ms | 4952ms |
| 31.0 | 41.0 | app1 | ok | 74 | 20000ms | 28000ms | 29800ms |
| 31.0 | 41.0 | app2 | ok | 17 | 20000ms | 28000ms | 29800ms |
| 31.0 | 41.0 | end-users | ok | 116 | 981ms | 2195ms | 2469ms |
| 41.0 | 51.0 | app1 | ok | 57 | 20000ms | 28000ms | 29800ms |
| 41.0 | 51.0 | app2 | ok | 27 | 20000ms | 28000ms | 29800ms |
| 41.0 | 51.0 | end-users | ok | 214 | 1500ms | 2674ms | 4767ms |
| 51.0 | 61.0 | app1 | ok | 26 | 20000ms | 28000ms | 29800ms |
| 51.0 | 61.0 | app2 | ok | 12 | 45000ms | 57000ms | 59700ms |
| 51.0 | 61.0 | end-users | ok | 181 | 1966ms | 4299ms | 4967ms |
| 61.0 | 71.0 | app1 | ok | 12 | 45000ms | 57000ms | 59700ms |
| 61.0 | 71.0 | app2 | ok | 8 | 45000ms | 57000ms | 59700ms |
| 61.0 | 71.0 | end-users | ok | 112 | 6456ms | 9291ms | 9929ms |
| 71.0 | 81.0 | app1 | ok | 49 | 45000ms | 57000ms | 59700ms |
| 71.0 | 81.0 | app2 | ok | 24 | 45000ms | 57000ms | 59700ms |
| 71.0 | 81.0 | end-users | ok | 155 | 7500ms | 9500ms | 9950ms |
| 81.0 | 91.0 | app1 | ok | 52 | 45000ms | 57000ms | 59700ms |
| 81.0 | 91.0 | app2 | ok | 25 | 60000ms | 60000ms | 60000ms |
| 81.0 | 91.0 | end-users | ok | 169 | 16693ms | 27339ms | 29734ms |
| 91.0 | 101.0 | app1 | ok | 52 | 45000ms | 57000ms | 59700ms |
| 91.0 | 101.0 | app2 | ok | 26 | 60000ms | 60000ms | 60000ms |
| 91.0 | 101.0 | end-users | ok | 167 | 15478ms | 27096ms | 29710ms |
| 101.0 | 111.0 | app1 | ok | 37 | 45000ms | 57000ms | 59700ms |
| 101.0 | 111.0 | app2 | ok | 19 | 60000ms | 60000ms | 60000ms |
| 101.0 | 111.0 | end-users | ok | 133 | 19609ms | 27922ms | 29792ms |
| 111.0 | 121.0 | app1 | ok | 44 | 45000ms | 57000ms | 59700ms |
| 111.0 | 121.0 | app2 | ok | 23 | 60000ms | 60000ms | 60000ms |
| 111.0 | 121.0 | end-users | ok | 134 | 20000ms | 28000ms | 29800ms |
| 121.0 | 131.0 | app1 | ok | 55 | 45000ms | 57000ms | 59700ms |
| 121.0 | 131.0 | app2 | ok | 26 | 60000ms | 60000ms | 60000ms |
| 121.0 | 131.0 | end-users | ok | 177 | 19709ms | 27942ms | 29794ms |
| 131.0 | 141.0 | app1 | ok | 45 | 45000ms | 57000ms | 59700ms |
| 131.0 | 141.0 | app2 | ok | 23 | 60000ms | 60000ms | 60000ms |
| 131.0 | 141.0 | end-users | ok | 143 | 19858ms | 27972ms | 29797ms |
| 141.0 | 151.0 | app1 | ok | 44 | 45000ms | 57000ms | 59700ms |
| 141.0 | 151.0 | app2 | ok | 22 | 60000ms | 60000ms | 60000ms |
| 141.0 | 151.0 | end-users | ok | 147 | 17105ms | 27421ms | 29742ms |
| 151.0 | 161.0 | app1 | ok | 51 | 45000ms | 57000ms | 59700ms |
| 151.0 | 161.0 | app2 | ok | 27 | 60000ms | 60000ms | 60000ms |
| 151.0 | 161.0 | end-users | ok | 166 | 19221ms | 27844ms | 29784ms |
| 161.0 | 171.0 | app1 | ok | 49 | 45000ms | 57000ms | 59700ms |
| 161.0 | 171.0 | app2 | ok | 24 | 60000ms | 60000ms | 60000ms |
| 161.0 | 171.0 | end-users | ok | 160 | 20000ms | 28000ms | 29800ms |
| 171.0 | 181.0 | app1 | ok | 52 | 45000ms | 57000ms | 59700ms |
| 171.0 | 181.0 | app2 | ok | 26 | 60000ms | 60000ms | 60000ms |
| 171.0 | 181.0 | end-users | ok | 166 | 14771ms | 26954ms | 29695ms |
| 181.0 | 191.0 | app1 | ok | 38 | 45000ms | 57000ms | 59700ms |
| 181.0 | 191.0 | app2 | ok | 19 | 60000ms | 60000ms | 60000ms |
| 181.0 | 191.0 | end-users | ok | 123 | 20000ms | 28000ms | 29800ms |
| 191.0 | 201.0 | app1 | ok | 40 | 45000ms | 57000ms | 59700ms |
| 191.0 | 201.0 | app2 | ok | 19 | 60000ms | 60000ms | 60000ms |
| 191.0 | 201.0 | end-users | ok | 125 | 19496ms | 27899ms | 29790ms |
| 201.0 | 211.0 | app1 | ok | 52 | 45000ms | 57000ms | 59700ms |
| 201.0 | 211.0 | app2 | ok | 29 | 60000ms | 60000ms | 60000ms |
| 201.0 | 211.0 | end-users | ok | 173 | 18311ms | 27662ms | 29766ms |
| 211.0 | 221.0 | app1 | ok | 51 | 45000ms | 57000ms | 59700ms |
| 211.0 | 221.0 | app2 | ok | 23 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | end-users | ok | 161 | 19810ms | 27962ms | 29796ms |
| 221.0 | 232.0 | app1 | ok | 42 | 45000ms | 57000ms | 59700ms |
| 221.0 | 232.0 | app2 | ok | 21 | 60000ms | 60000ms | 60000ms |
| 221.0 | 232.0 | end-users | ok | 142 | 17207ms | 27441ms | 29744ms |
| 232.0 | 242.0 | app1 | ok | 42 | 45000ms | 57000ms | 59700ms |
| 232.0 | 242.0 | app2 | ok | 23 | 60000ms | 60000ms | 60000ms |
| 232.0 | 242.0 | end-users | ok | 135 | 20000ms | 28000ms | 29800ms |
| 242.0 | 252.0 | app1 | ok | 50 | 45000ms | 57000ms | 59700ms |
| 242.0 | 252.0 | app2 | ok | 24 | 60000ms | 60000ms | 60000ms |
| 242.0 | 252.0 | end-users | ok | 162 | 20000ms | 28000ms | 29800ms |
| 252.0 | 262.0 | app1 | ok | 132 | 45000ms | 57000ms | 59700ms |
| 252.0 | 262.0 | app2 | ok | 66 | 60000ms | 60000ms | 60000ms |
| 252.0 | 262.0 | end-users | ok | 38 | 20000ms | 28000ms | 29800ms |
| 262.0 | 272.0 | app1 | ok | 58 | 23488ms | 48400ms | 58840ms |
| 262.0 | 272.0 | app2 | ok | 156 | 59605ms | 60000ms | 60000ms |
| 262.0 | 272.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 452.0 | 463.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 463.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 452.0 | 463.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 463.0 | 473.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 463.0 | 473.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 463.0 | 473.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 473.0 | 475.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 473.0 | 475.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 473.0 | 475.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app2 exceeded the 10% ledger tolerance: cost -21.5%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1639590 | 81130 | 1720720.0 | 0.0% | 1715364.0 | 1801850.0 | -4.8% | True |
| app2 | 988920 | 48925 | 1037845.0 | 0.0% | 852798.0 | 1086770.0 | -21.5% | False |
| end-users | 4505490 | 223105 | 4728595.0 | 0.0% | 4876092.0 | 4951700.0 | -1.5% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1334 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 805 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3665 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5804). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5804 | 0.054ms | 0.217ms | (0, 0.1]ms | (0.2, 0.5]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 432584 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1333 | 48402ms | 58840ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 804 | 77758ms | 115776ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3663 | 16082ms | 19661ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5800 | 17859ms | 89527ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (48 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 21.0 | app1 | ok | 1375ms | 2885ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 21.0 | app2 | ok | 1406ms | 2855ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 21.0 | end-users | ok | 1300ms | 2817ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 21.0 | 31.0 | app1 | ok | 5094ms | 5966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 21.0 | 31.0 | app2 | ok | 5000ms | 7800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 21.0 | 31.0 | end-users | ok | 6278ms | 8667ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 31.0 | 41.0 | app1 | ok | 15896ms | 19590ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 31.0 | 41.0 | app2 | ok | 23333ms | 29333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 31.0 | 41.0 | end-users | ok | 4816ms | 9679ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | app1 | ok | 23953ms | 29395ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | app2 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | end-users | ok | 5345ms | 7509ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app2 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | end-users | ok | 6269ms | 7846ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app2 | ok | 45000ms | 58500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | end-users | ok | 7974ms | 9863ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app1 | ok | 37989ms | 47750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app2 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | end-users | ok | 12051ms | 14705ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 38547ms | 53875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app2 | ok | 88636ms | 116864ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 13861ms | 19291ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 17734ms | 24154ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 17500ms | 19939ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 16925ms | 19692ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 16659ms | 19666ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 16696ms | 19670ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 17169ms | 19717ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 17484ms | 19748ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 17311ms | 19731ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 17429ms | 19871ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 17132ms | 19713ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 16864ms | 19686ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 232.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 232.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 232.0 | end-users | ok | 16942ms | 19694ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 232.0 | 242.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 232.0 | 242.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 232.0 | 242.0 | end-users | ok | 17567ms | 19877ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 242.0 | 252.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 242.0 | 252.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 242.0 | 252.0 | end-users | ok | 17270ms | 19727ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | app1 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | end-users | ok | 17200ms | 19720ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | app1 | ok | 38912ms | 56978ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | app2 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 272.0 | 282.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 272.0 | 282.0 | app2 | ok | 57812ms | 113588ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 452.0 | 463.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 463.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 452.0 | 463.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 463.0 | 473.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 463.0 | 473.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 463.0 | 473.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 473.0 | 475.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 473.0 | 475.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 473.0 | 475.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
