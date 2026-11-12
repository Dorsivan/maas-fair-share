# Fairness benchmark: full-contention-2x-discriminating (uni231-aa-T3a-inst1)

**Verdict: FAIL** (threshold: 10 points)
**Secondary (priority) verdict: PRIORITY-FAIL** -- see "Per-tenant TTFT / ITL and the priority verdict (UNI-226)" below for detail.
Worker-share vs. weight-share gap (UNI-225): 35.1 points

- end-users deviated -33.5 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention-2x-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:c8a088203f6dc6c48c158d21b6295172a78f18646b06c334e5310a0caedb259f` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5fbdd988df-zwm5d` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-11T14:14:00Z` |
| Run end | `2026-11-11T14:19:33Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 256 | 1756 | 000=1, 200=1705, 500=50 | 9.6 | 16.4 | 208274.0 | 21.1% | 33.3% | 12.3 | 33.6% | 12.6 | 33.4% | 12.4 | 1.4s | 98.9% | 1705.0 |
| app2 | 10.0 | 256 | 1756 | 200=1719, 401=1, 500=36 | 9.6 | 16.8 | 194898.0 | 10.5% | 33.3% | 22.8 | 31.5% | 20.9 | 33.4% | 22.9 | 1.4s | 98.9% | 1719.0 |
| end-users | 65.0 | 256 | 1743 | 200=1694, 500=48, 503=1 | 9.8 | 15.7 | 216362.0 | 68.4% | 33.3% | -35.1 | 34.9% | -33.5 | 33.2% | -35.3 | 1.2s | 98.9% | 1694.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 1.0 |

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

**Windows** (34 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 10.0 | 20.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 10.0 | 20.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 10.0 | 20.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 20.0 | 31.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 20.0 | 31.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 20.0 | 31.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 31.0 | 41.0 | app1 | True | 32452.0 | 21.1% | 30.4% | 9.3 |
| 31.0 | 41.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 31.0 | 41.0 | end-users | True | 74390.0 | 68.4% | 69.6% | 1.2 |
| 41.0 | 51.0 | app1 | True | 63558.0 | 21.1% | 38.2% | 17.2 |
| 41.0 | 51.0 | app2 | True | 87942.0 | 10.5% | 52.9% | 42.3 |
| 41.0 | 51.0 | end-users | True | 14856.0 | 68.4% | 8.9% | -59.5 |
| 51.0 | 61.0 | app1 | True | 8120.0 | 21.1% | 24.0% | 3.0 |
| 51.0 | 61.0 | app2 | True | 14886.0 | 10.5% | 44.0% | 33.5 |
| 51.0 | 61.0 | end-users | True | 10806.0 | 68.4% | 32.0% | -36.5 |
| 61.0 | 71.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 61.0 | 71.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 61.0 | 71.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 71.0 | 81.0 | app1 | True | 44624.0 | 21.1% | 35.4% | 14.4 |
| 71.0 | 81.0 | app2 | True | 28430.0 | 10.5% | 22.6% | 12.1 |
| 71.0 | 81.0 | end-users | True | 52828.0 | 68.4% | 42.0% | -26.5 |
| 81.0 | 91.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 81.0 | 91.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 81.0 | 91.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 91.0 | 101.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 91.0 | 101.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 91.0 | 101.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 101.0 | 111.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 101.0 | 111.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 101.0 | 111.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 111.0 | 121.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 111.0 | 121.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 111.0 | 121.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 121.0 | 131.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 121.0 | 131.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 121.0 | 131.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 131.0 | 141.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 131.0 | 141.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 131.0 | 141.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 141.0 | 151.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 141.0 | 151.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 141.0 | 151.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 151.0 | 161.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 151.0 | 161.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 151.0 | 161.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 161.0 | 171.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 161.0 | 171.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 161.0 | 171.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 171.0 | 181.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 171.0 | 181.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 171.0 | 181.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 181.0 | 191.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 181.0 | 191.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 181.0 | 191.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 191.0 | 202.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 191.0 | 202.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 191.0 | 202.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 202.0 | 212.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 202.0 | 212.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 202.0 | 212.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 212.0 | 222.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 212.0 | 222.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 212.0 | 222.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 222.0 | 232.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 222.0 | 232.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 222.0 | 232.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 232.0 | 242.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 232.0 | 242.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 232.0 | 242.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 242.0 | 252.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 242.0 | 252.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 242.0 | 252.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | app1 | False | 59520.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | app2 | False | 63640.0 | n/a | n/a | n/a |
| 252.0 | 262.0 | end-users | False | 63482.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 262.0 | 272.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 272.0 | 282.0 | app2 | False | 0.0 | n/a | n/a | n/a |
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
| 332.0 | 333.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 332.0 | 333.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 332.0 | 333.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 30 | 0ms | 0ms | 5ms |
| 10.0 | 20.0 | app2 | ok | 31 | 0ms | 0ms | 1ms |
| 10.0 | 20.0 | end-users | ok | 34 | 0ms | 0ms | 1ms |
| 20.0 | 31.0 | app1 | ok | 81 | 0ms | 0ms | 13ms |
| 20.0 | 31.0 | app2 | ok | 97 | 0ms | 0ms | 8ms |
| 20.0 | 31.0 | end-users | ok | 77 | 0ms | 0ms | 4ms |
| 31.0 | 41.0 | app1 | ok | 99 | 1068ms | 4705ms | 9175ms |
| 31.0 | 41.0 | app2 | ok | 60 | 25ms | 1955ms | 8500ms |
| 31.0 | 41.0 | end-users | ok | 103 | 882ms | 4046ms | 4905ms |
| 41.0 | 51.0 | app1 | ok | 22 | 0ms | 0ms | 445ms |
| 41.0 | 51.0 | app2 | ok | 51 | 5887ms | 9177ms | 9918ms |
| 41.0 | 51.0 | end-users | ok | 20 | 0ms | 0ms | 2200ms |
| 51.0 | 61.0 | app1 | ok | 85 | 0ms | 0ms | 12ms |
| 51.0 | 61.0 | app2 | ok | 93 | 0ms | 0ms | 22ms |
| 51.0 | 61.0 | end-users | ok | 71 | 0ms | 0ms | 9ms |
| 61.0 | 71.0 | app1 | ok | 80 | 0ms | 62ms | 300ms |
| 61.0 | 71.0 | app2 | ok | 75 | 0ms | 46ms | 222ms |
| 61.0 | 71.0 | end-users | ok | 101 | 0ms | 33ms | 174ms |
| 71.0 | 81.0 | app1 | ok | 46 | 0ms | 0ms | 385ms |
| 71.0 | 81.0 | app2 | ok | 53 | 0ms | 2ms | 735ms |
| 71.0 | 81.0 | end-users | ok | 52 | 0ms | 246ms | 870ms |
| 81.0 | 91.0 | app1 | ok | 84 | 0ms | 0ms | 6ms |
| 81.0 | 91.0 | app2 | ok | 85 | 0ms | 0ms | 3ms |
| 81.0 | 91.0 | end-users | ok | 59 | 0ms | 0ms | 4ms |
| 91.0 | 101.0 | app1 | ok | 66 | 0ms | 0ms | 2ms |
| 91.0 | 101.0 | app2 | ok | 66 | 0ms | 0ms | 1ms |
| 91.0 | 101.0 | end-users | ok | 51 | 0ms | 0ms | 0ms |
| 101.0 | 111.0 | app1 | ok | 59 | 0ms | 0ms | 0ms |
| 101.0 | 111.0 | app2 | ok | 56 | 0ms | 0ms | 1ms |
| 101.0 | 111.0 | end-users | ok | 93 | 0ms | 0ms | 1ms |
| 111.0 | 121.0 | app1 | ok | 76 | 0ms | 0ms | 2ms |
| 111.0 | 121.0 | app2 | ok | 65 | 0ms | 0ms | 0ms |
| 111.0 | 121.0 | end-users | ok | 64 | 0ms | 0ms | 2ms |
| 121.0 | 131.0 | app1 | ok | 76 | 0ms | 0ms | 6ms |
| 121.0 | 131.0 | app2 | ok | 91 | 0ms | 0ms | 0ms |
| 121.0 | 131.0 | end-users | ok | 63 | 0ms | 0ms | 2ms |
| 131.0 | 141.0 | app1 | ok | 69 | 0ms | 0ms | 2ms |
| 131.0 | 141.0 | app2 | ok | 68 | 0ms | 0ms | 2ms |
| 131.0 | 141.0 | end-users | ok | 72 | 0ms | 0ms | 2ms |
| 141.0 | 151.0 | app1 | ok | 64 | 0ms | 0ms | 4ms |
| 141.0 | 151.0 | app2 | ok | 56 | 0ms | 0ms | 0ms |
| 141.0 | 151.0 | end-users | ok | 78 | 0ms | 0ms | 2ms |
| 151.0 | 161.0 | app1 | ok | 70 | 0ms | 0ms | 4ms |
| 151.0 | 161.0 | app2 | ok | 78 | 0ms | 0ms | 0ms |
| 151.0 | 161.0 | end-users | ok | 63 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | app1 | ok | 65 | 0ms | 0ms | 2ms |
| 161.0 | 171.0 | app2 | ok | 68 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | end-users | ok | 59 | 0ms | 0ms | 4ms |
| 171.0 | 181.0 | app1 | ok | 71 | 0ms | 0ms | 1ms |
| 171.0 | 181.0 | app2 | ok | 66 | 0ms | 0ms | 1ms |
| 171.0 | 181.0 | end-users | ok | 69 | 0ms | 0ms | 1ms |
| 181.0 | 191.0 | app1 | ok | 68 | 0ms | 0ms | 2ms |
| 181.0 | 191.0 | app2 | ok | 71 | 0ms | 0ms | 2ms |
| 181.0 | 191.0 | end-users | ok | 79 | 0ms | 0ms | 0ms |
| 191.0 | 202.0 | app1 | ok | 70 | 0ms | 0ms | 0ms |
| 191.0 | 202.0 | app2 | ok | 78 | 0ms | 0ms | 2ms |
| 191.0 | 202.0 | end-users | ok | 69 | 0ms | 0ms | 2ms |
| 202.0 | 212.0 | app1 | ok | 72 | 0ms | 0ms | 2ms |
| 202.0 | 212.0 | app2 | ok | 58 | 0ms | 1ms | 4ms |
| 202.0 | 212.0 | end-users | ok | 53 | 0ms | 0ms | 1ms |
| 212.0 | 222.0 | app1 | ok | 83 | 0ms | 0ms | 1ms |
| 212.0 | 222.0 | app2 | ok | 78 | 0ms | 0ms | 1ms |
| 212.0 | 222.0 | end-users | ok | 89 | 0ms | 0ms | 0ms |
| 222.0 | 232.0 | app1 | ok | 66 | 0ms | 0ms | 1ms |
| 222.0 | 232.0 | app2 | ok | 80 | 0ms | 0ms | 1ms |
| 222.0 | 232.0 | end-users | ok | 78 | 0ms | 0ms | 1ms |
| 232.0 | 242.0 | app1 | ok | 65 | 0ms | 0ms | 1ms |
| 232.0 | 242.0 | app2 | ok | 60 | 0ms | 0ms | 0ms |
| 232.0 | 242.0 | end-users | ok | 57 | 0ms | 0ms | 1ms |
| 242.0 | 252.0 | app1 | ok | 96 | 0ms | 0ms | 76ms |
| 242.0 | 252.0 | app2 | ok | 92 | 0ms | 0ms | 77ms |
| 242.0 | 252.0 | end-users | ok | 95 | 0ms | 0ms | 179ms |
| 252.0 | 262.0 | app1 | ok | 42 | 577ms | 1870ms | 2437ms |
| 252.0 | 262.0 | app2 | ok | 43 | 446ms | 1425ms | 2392ms |
| 252.0 | 262.0 | end-users | ok | 45 | 328ms | 1150ms | 2365ms |
| 262.0 | 272.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 262.0 | 272.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
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
| 332.0 | 333.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 333.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 332.0 | 333.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -91.0%
- app2 exceeded the 10% ledger tolerance: cost -91.6%
- end-users exceeded the 10% ledger tolerance: cost -90.6%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2097150 | 103892 | 2201042.0 | 0.0% | 208274.0 | 2304934.0 | -91.0% | False |
| app2 | 2114370 | 105286 | 2219656.0 | 0.0% | 194898.0 | 2324942.0 | -91.6% | False |
| end-users | 2083620 | 103671 | 2186004.0 | -0.1% | 216362.0 | 2290962.0 | -90.6% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1756 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | 0.0% | 0.00 |
| app2 | 1756 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | 0.0% | 0.00 |
| end-users | 1743 | 0 | 1 | 1 | 0.06% | 68.4% | 100.0% | 1.46 |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5119). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5119 | 0.055ms | 0.470ms | (0, 0.1]ms | (0.2, 0.5]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 272133 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1705 | 1454ms | 4852ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1719 | 1501ms | 5337ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 1693 | 1517ms | 4280ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5118 | 1488ms | 4707ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: PRIORITY-FAIL** -- the share verdict above is FAIL, so this is the board's second, independent success criterion (2026-11-10): did the policy nonetheless order tenants by weight? Top-weighted group: `end-users` (TTFT p50 1517ms, p95 4280ms, strictly lowest among distinctly-weighted groups: p50=False/p95=True; no rank inversion among any distinctly-weighted pair: False -- this, not raw rank correlation, is what gates the verdict, since a genuine weight tie (e.g. 98/1/1's app2==end-users) makes exact correlation 1.0 unreachable by construction even when ordering is otherwise perfect). Rank correlation -0.50 (1.00 = exact agreement, informational only) shown for reference. Separation from the next distinctly-weighted group: -62ms against a noise floor of not given (separation check skipped).

**Windowed TTFT/ITL** (34 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 747ms | 1146ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 771ms | 1177ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 747ms | 1196ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 31.0 | app1 | ok | 2432ms | 4270ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 31.0 | app2 | ok | 2630ms | 4580ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 31.0 | end-users | ok | 2421ms | 3937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 31.0 | 41.0 | app1 | ok | 4000ms | 7725ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 31.0 | 41.0 | app2 | ok | 2676ms | 4861ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 31.0 | 41.0 | end-users | ok | 4256ms | 5980ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | app1 | ok | 7600ms | 9780ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | app2 | ok | 11050ms | 14605ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 41.0 | 51.0 | end-users | ok | 3250ms | 7940ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app1 | ok | 797ms | 1245ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | app2 | ok | 850ms | 1405ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 51.0 | 61.0 | end-users | ok | 768ms | 1303ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app1 | ok | 2561ms | 3794ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | app2 | ok | 2636ms | 3830ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 61.0 | 71.0 | end-users | ok | 2917ms | 3892ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app1 | ok | 3310ms | 3967ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app2 | ok | 3242ms | 4704ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | end-users | ok | 3404ms | 4556ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 917ms | 1825ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app2 | ok | 1100ms | 1811ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 1042ms | 1681ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 1521ms | 2230ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 1485ms | 2487ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 1611ms | 1986ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 1467ms | 2567ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 1432ms | 2325ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 1550ms | 2386ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 971ms | 1450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 1047ms | 1482ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 980ms | 1665ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 960ms | 1841ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 915ms | 1646ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 883ms | 1786ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 1188ms | 1888ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 1257ms | 1956ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 1178ms | 1878ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 1163ms | 1796ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 1240ms | 1891ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 1156ms | 1949ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 2266ms | 3210ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 2260ms | 2962ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 2095ms | 2934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 1133ms | 1992ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 1288ms | 2493ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 1238ms | 2492ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 1442ms | 2550ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 1490ms | 2408ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 1356ms | 2290ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 1516ms | 2400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 1635ms | 2493ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 1531ms | 2600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 202.0 | app1 | ok | 956ms | 1941ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 202.0 | app2 | ok | 900ms | 1945ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 202.0 | end-users | ok | 1094ms | 1948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 202.0 | 212.0 | app1 | ok | 1033ms | 1630ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 202.0 | 212.0 | app2 | ok | 1058ms | 1737ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 202.0 | 212.0 | end-users | ok | 796ms | 1479ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 212.0 | 222.0 | app1 | ok | 1362ms | 2615ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 212.0 | 222.0 | app2 | ok | 1382ms | 2733ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 212.0 | 222.0 | end-users | ok | 1332ms | 2561ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 222.0 | 232.0 | app1 | ok | 2365ms | 2954ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 222.0 | 232.0 | app2 | ok | 2331ms | 2979ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 222.0 | 232.0 | end-users | ok | 2422ms | 2956ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 232.0 | 242.0 | app1 | ok | 1014ms | 2310ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 232.0 | 242.0 | app2 | ok | 1181ms | 2706ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 232.0 | 242.0 | end-users | ok | 1175ms | 2594ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 242.0 | 252.0 | app1 | ok | 1880ms | 3075ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 242.0 | 252.0 | app2 | ok | 1682ms | 3260ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 242.0 | 252.0 | end-users | ok | 1722ms | 3240ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | app1 | ok | 4171ms | 5500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | app2 | ok | 4500ms | 7382ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 252.0 | 262.0 | end-users | ok | 3486ms | 6560ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 262.0 | 272.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 272.0 | 282.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 272.0 | 282.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 332.0 | 333.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 333.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 333.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
