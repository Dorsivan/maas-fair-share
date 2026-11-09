# Fairness benchmark: full-contention (uni-213-c6-rerun2)

**Verdict: UNCONTENDED** -- every offered group's `contended_seconds_total` delta stayed under 1s, so the pool was never actually contended. Not scored against the 10-point weighted-split threshold; see docs/runbook.md.

- every offered group's contended_seconds_total delta stayed under 1s (app1=never contended, app2=never contended, end-users=never contended) -- an order of magnitude below the ~9s a genuinely-contending tenant accrues in a 240s full-contention run (docs/runbook.md), so nobody was ever backlogged alongside anyone else and the weighted-split deviation check does not apply

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:6918308df0e1c8f3b6b5b9af3b1b341205ccbd1da4a3e55f82d6330a354c8bbf` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-775699b69c-pq62t` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T18:29:58Z` |
| Run end | `2026-11-09T18:35:23Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1108 | 200=1105, 500=3 | 7.0 | 7.3 | n/a | 21.1% | 0.0% | -21.1 | 19.8% | -1.2 | n/a | 98.9% | 1101.0 |
| app2 | 10.0 | 32 | 45 | 000=32, 400=1, 500=12 | 300.5 | 301.0 | n/a | 10.5% | 0.0% | -10.5 | 0.8% | -9.7 | n/a | n/a | 32.0 |
| end-users | 65.0 | 128 | 4441 | 200=4402, 500=39 | 7.0 | 7.3 | n/a | 68.4% | 0.0% | -68.4 | 79.4% | 11.0 | n/a | 98.9% | 4384.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 23.0 |

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
| 0.0 | 10.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 10.0 | 20.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 10.0 | 20.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 10.0 | 20.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 20.0 | 30.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 20.0 | 30.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 20.0 | 30.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 30.0 | 40.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 30.0 | 40.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 30.0 | 40.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 40.0 | 50.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 40.0 | 50.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 40.0 | 50.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 50.0 | 60.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 50.0 | 60.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 50.0 | 60.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 60.0 | 70.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 60.0 | 70.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 60.0 | 70.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 70.0 | 80.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 70.0 | 80.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 70.0 | 80.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 80.0 | 90.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 80.0 | 90.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 80.0 | 90.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 90.0 | 100.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 90.0 | 100.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 90.0 | 100.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 100.0 | 110.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 100.0 | 110.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 100.0 | 110.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 110.0 | 120.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 110.0 | 120.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 110.0 | 120.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 120.0 | 130.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 120.0 | 130.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 120.0 | 130.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 130.0 | 140.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 130.0 | 140.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 130.0 | 140.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 140.0 | 150.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 140.0 | 150.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 140.0 | 150.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 150.0 | 160.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 150.0 | 160.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 150.0 | 160.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 160.0 | 170.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 160.0 | 170.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 160.0 | 170.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 170.0 | 180.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 170.0 | 180.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 170.0 | 180.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 180.0 | 190.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 180.0 | 190.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 180.0 | 190.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 190.0 | 200.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 190.0 | 200.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 190.0 | 200.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 200.0 | 210.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 200.0 | 210.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 200.0 | 210.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 210.0 | 220.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 210.0 | 220.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 210.0 | 220.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 220.0 | 230.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 220.0 | 230.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 220.0 | 230.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 230.0 | 240.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 230.0 | 240.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 230.0 | 240.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 240.0 | 250.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 325.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 325.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 325.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 52 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app2 | ok | 32 | 0ms | 0ms | 4ms |
| 10.0 | 20.0 | end-users | ok | 193 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app1 | ok | 61 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 236 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app1 | ok | 46 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 184 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | app1 | ok | 44 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 181 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app1 | ok | 44 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 180 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 183 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app1 | ok | 44 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 181 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app1 | ok | 46 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 182 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | app1 | ok | 46 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 177 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | app1 | ok | 45 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 181 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | app1 | ok | 46 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 179 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | app1 | ok | 43 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 185 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | app1 | ok | 48 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 178 | 0ms | 0ms | 0ms |
| 140.0 | 150.0 | app1 | ok | 43 | 0ms | 0ms | 0ms |
| 140.0 | 150.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 140.0 | 150.0 | end-users | ok | 186 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | app1 | ok | 46 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 150.0 | 160.0 | end-users | ok | 177 | 0ms | 0ms | 0ms |
| 160.0 | 170.0 | app1 | ok | 46 | 0ms | 0ms | 0ms |
| 160.0 | 170.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 160.0 | 170.0 | end-users | ok | 185 | 0ms | 0ms | 0ms |
| 170.0 | 180.0 | app1 | ok | 42 | 0ms | 0ms | 0ms |
| 170.0 | 180.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 170.0 | 180.0 | end-users | ok | 180 | 0ms | 0ms | 0ms |
| 180.0 | 190.0 | app1 | ok | 50 | 0ms | 0ms | 0ms |
| 180.0 | 190.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 180.0 | 190.0 | end-users | ok | 177 | 0ms | 0ms | 0ms |
| 190.0 | 200.0 | app1 | ok | 41 | 0ms | 0ms | 0ms |
| 190.0 | 200.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 190.0 | 200.0 | end-users | ok | 184 | 0ms | 0ms | 0ms |
| 200.0 | 210.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 200.0 | 210.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 200.0 | 210.0 | end-users | ok | 180 | 0ms | 0ms | 0ms |
| 210.0 | 220.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 210.0 | 220.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 210.0 | 220.0 | end-users | ok | 179 | 0ms | 0ms | 0ms |
| 220.0 | 230.0 | app1 | ok | 46 | 0ms | 0ms | 0ms |
| 220.0 | 230.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 220.0 | 230.0 | end-users | ok | 181 | 0ms | 0ms | 0ms |
| 230.0 | 240.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 230.0 | 240.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 230.0 | 240.0 | end-users | ok | 183 | 0ms | 0ms | 0ms |
| 240.0 | 250.0 | app1 | ok | 34 | 0ms | 0ms | 0ms |
| 240.0 | 250.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | ok | 152 | 0ms | 0ms | 0ms |
| 250.0 | 260.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 270.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 270.0 | 280.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 280.0 | 290.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 290.0 | 300.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 300.0 | 310.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 310.0 | 320.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 320.0 | 325.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 320.0 | 325.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 320.0 | 325.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost n/a
- app2 exceeded the 10% ledger tolerance: raw tokens n/a, cost n/a
- end-users exceeded the 10% ledger tolerance: cost n/a

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1359150 | 67366 | 1421357.0 | -0.4% | n/a | 1493882.0 | n/a | False |
| app2 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | False |
| end-users | 5414460 | 268257 | 5659493.0 | -0.4% | n/a | 5950974.0 | n/a | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1108 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 45 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 4441 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5540). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5540 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 313200 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
