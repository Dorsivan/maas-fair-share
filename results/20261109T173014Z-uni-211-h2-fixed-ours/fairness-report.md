# Fairness benchmark: full-contention (uni-211-h2-fixed-ours)

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
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-5796f788b4-vw8gn` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T17:31:30Z` |
| Run end | `2026-11-09T17:35:52Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 499 | 200=480, 500=19 | 17.0 | 17.3 | n/a | 21.1% | 0.0% | -21.1 | 16.8% | -4.2 | n/a | 98.9% | 476.0 |
| app2 | 10.0 | 32 | 490 | 200=474, 500=16 | 17.0 | 17.3 | n/a | 10.5% | 0.0% | -10.5 | 16.5% | 6.0 | n/a | 98.9% | 470.0 |
| end-users | 65.0 | 128 | 1980 | 200=1903, 500=77 | 17.0 | 17.3 | n/a | 68.4% | 0.0% | -68.4 | 66.7% | -1.7 | n/a | 98.9% | 1893.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 18.0 |

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
| 260.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 36 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 34 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 142 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 25 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app2 | ok | 25 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | end-users | ok | 96 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app1 | ok | 21 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app2 | ok | 17 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | end-users | ok | 77 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app1 | ok | 18 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app2 | ok | 20 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | end-users | ok | 74 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | app1 | ok | 17 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | app2 | ok | 19 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | end-users | ok | 78 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app1 | ok | 19 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app2 | ok | 15 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | end-users | ok | 78 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app1 | ok | 20 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app2 | ok | 20 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | end-users | ok | 72 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app1 | ok | 21 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app2 | ok | 20 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | end-users | ok | 74 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app1 | ok | 15 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app2 | ok | 19 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | end-users | ok | 78 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | app1 | ok | 20 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | app2 | ok | 20 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | end-users | ok | 74 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | app1 | ok | 19 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | app2 | ok | 17 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | end-users | ok | 75 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | app1 | ok | 20 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | app2 | ok | 20 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | end-users | ok | 70 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | app1 | ok | 19 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | app2 | ok | 17 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | end-users | ok | 78 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | app1 | ok | 16 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | app2 | ok | 21 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | end-users | ok | 74 | 0ms | 0ms | 0ms |
| 140.0 | 150.0 | app1 | ok | 20 | 0ms | 0ms | 0ms |
| 140.0 | 150.0 | app2 | ok | 19 | 0ms | 0ms | 0ms |
| 140.0 | 150.0 | end-users | ok | 74 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | app1 | ok | 18 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | app2 | ok | 18 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | end-users | ok | 78 | 0ms | 0ms | 0ms |
| 160.0 | 170.0 | app1 | ok | 17 | 0ms | 0ms | 0ms |
| 160.0 | 170.0 | app2 | ok | 20 | 0ms | 0ms | 0ms |
| 160.0 | 170.0 | end-users | ok | 72 | 0ms | 0ms | 0ms |
| 170.0 | 180.0 | app1 | ok | 20 | 0ms | 0ms | 0ms |
| 170.0 | 180.0 | app2 | ok | 13 | 0ms | 0ms | 0ms |
| 170.0 | 180.0 | end-users | ok | 79 | 0ms | 0ms | 0ms |
| 180.0 | 190.0 | app1 | ok | 19 | 0ms | 0ms | 0ms |
| 180.0 | 190.0 | app2 | ok | 22 | 0ms | 0ms | 0ms |
| 180.0 | 190.0 | end-users | ok | 71 | 0ms | 0ms | 0ms |
| 190.0 | 200.0 | app1 | ok | 21 | 0ms | 0ms | 0ms |
| 190.0 | 200.0 | app2 | ok | 18 | 0ms | 0ms | 0ms |
| 190.0 | 200.0 | end-users | ok | 75 | 0ms | 0ms | 0ms |
| 200.0 | 210.0 | app1 | ok | 15 | 0ms | 0ms | 0ms |
| 200.0 | 210.0 | app2 | ok | 20 | 0ms | 0ms | 0ms |
| 200.0 | 210.0 | end-users | ok | 78 | 0ms | 0ms | 0ms |
| 210.0 | 220.0 | app1 | ok | 20 | 0ms | 0ms | 0ms |
| 210.0 | 220.0 | app2 | ok | 20 | 0ms | 0ms | 0ms |
| 210.0 | 220.0 | end-users | ok | 74 | 0ms | 0ms | 0ms |
| 220.0 | 230.0 | app1 | ok | 19 | 0ms | 0ms | 0ms |
| 220.0 | 230.0 | app2 | ok | 16 | 0ms | 0ms | 0ms |
| 220.0 | 230.0 | end-users | ok | 77 | 0ms | 0ms | 0ms |
| 230.0 | 240.0 | app1 | ok | 21 | 0ms | 0ms | 0ms |
| 230.0 | 240.0 | app2 | ok | 20 | 0ms | 0ms | 0ms |
| 230.0 | 240.0 | end-users | ok | 73 | 0ms | 0ms | 0ms |
| 240.0 | 250.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | ok | 2 | 0ms | 0ms | 0ms |
| 250.0 | 260.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost n/a
- app2 exceeded the 10% ledger tolerance: cost n/a
- end-users exceeded the 10% ledger tolerance: cost n/a

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 590400 | 29431 | 614671.0 | -0.8% | n/a | 649262.0 | n/a | False |
| app2 | 583020 | 28813 | 606664.0 | -0.8% | n/a | 640646.0 | n/a | False |
| end-users | 2340690 | 116422 | 2444175.0 | -0.5% | n/a | 2573534.0 | n/a | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 499 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 490 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1980 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=2857). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 2857 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 251815 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
