# Fairness benchmark: app1-flood-light (uni-212-reverify-app1-flood-32)

**Verdict: UNCONTENDED** -- every offered group's `contended_seconds_total` delta stayed under 1s, so the pool was never actually contended. Not scored against the 10-point weighted-split threshold; see docs/runbook.md.

- every offered group's contended_seconds_total delta stayed under 1s (app1=never contended, app2=never contended, end-users=never contended) -- an order of magnitude below the ~9s a genuinely-contending tenant accrues in a 240s full-contention run (docs/runbook.md), so nobody was ever backlogged alongside anyone else and the weighted-split deviation check does not apply

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-flood-light` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-59fc4f78c8-vbvnj` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T20:37:55Z` |
| Run end | `2026-11-09T20:42:17Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 30.0 | 32 | 731 | 200=712, 500=19 | 11.2 | 11.4 | n/a | 30.0% | 0.0% | -30.0 | 25.0% | -5.0 | n/a | 98.9% | 709.0 |
| app2 | 10.0 | 32 | 731 | 200=706, 500=25 | 11.2 | 11.4 | n/a | 10.0% | 0.0% | -10.0 | 25.0% | 15.0 | n/a | 98.9% | 704.0 |
| end-users | 60.0 | 64 | 1466 | 200=1416, 500=50 | 11.2 | 11.4 | n/a | 60.0% | 0.0% | -60.0 | 50.1% | -9.9 | n/a | 98.9% | 1410.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 11.0 |

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
| 0.0 | 10.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 0.0 | 10.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 10.0 | 20.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 10.0 | 20.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 10.0 | 20.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 20.0 | 30.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 20.0 | 30.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 20.0 | 30.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 30.0 | 40.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 30.0 | 40.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 30.0 | 40.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 40.0 | 50.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 40.0 | 50.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 40.0 | 50.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 50.0 | 60.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 50.0 | 60.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 50.0 | 60.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 60.0 | 70.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 60.0 | 70.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 60.0 | 70.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 70.0 | 80.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 70.0 | 80.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 70.0 | 80.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 80.0 | 90.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 80.0 | 90.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 80.0 | 90.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 90.0 | 100.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 90.0 | 100.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 90.0 | 100.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 100.0 | 110.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 100.0 | 110.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 100.0 | 110.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 110.0 | 120.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 110.0 | 120.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 110.0 | 120.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 120.0 | 130.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 120.0 | 130.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 120.0 | 130.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 130.0 | 140.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 130.0 | 140.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 130.0 | 140.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 140.0 | 150.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 140.0 | 150.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 140.0 | 150.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 150.0 | 160.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 150.0 | 160.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 150.0 | 160.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 160.0 | 170.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 160.0 | 170.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 160.0 | 170.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 170.0 | 180.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 170.0 | 180.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 170.0 | 180.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 180.0 | 190.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 180.0 | 190.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 180.0 | 190.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 190.0 | 200.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 190.0 | 200.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 190.0 | 200.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 200.0 | 210.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 200.0 | 210.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 200.0 | 210.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 210.0 | 220.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 210.0 | 220.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 210.0 | 220.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 220.0 | 230.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 220.0 | 230.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 220.0 | 230.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 230.0 | 240.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 230.0 | 240.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 230.0 | 240.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
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
| 0.0 | 10.0 | app1 | ok | 49 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 47 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 91 | 0ms | 0ms | 1ms |
| 10.0 | 20.0 | app1 | ok | 29 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app2 | ok | 28 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | end-users | ok | 58 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app1 | ok | 26 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app2 | ok | 29 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | end-users | ok | 57 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app1 | ok | 31 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app2 | ok | 28 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | end-users | ok | 57 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | app1 | ok | 30 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | app2 | ok | 27 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | end-users | ok | 57 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app1 | ok | 28 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app2 | ok | 30 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | end-users | ok | 53 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app1 | ok | 24 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app2 | ok | 30 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | end-users | ok | 62 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app1 | ok | 30 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app2 | ok | 28 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | end-users | ok | 55 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app1 | ok | 29 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app2 | ok | 26 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | end-users | ok | 59 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | app1 | ok | 28 | 0ms | 0ms | 1ms |
| 90.0 | 100.0 | app2 | ok | 30 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | end-users | ok | 54 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | app1 | ok | 31 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | app2 | ok | 28 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | end-users | ok | 57 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | app1 | ok | 25 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | app2 | ok | 28 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | end-users | ok | 58 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | app1 | ok | 31 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | app2 | ok | 29 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | end-users | ok | 54 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | app1 | ok | 28 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | app2 | ok | 27 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | end-users | ok | 60 | 0ms | 0ms | 0ms |
| 140.0 | 150.0 | app1 | ok | 29 | 0ms | 0ms | 0ms |
| 140.0 | 150.0 | app2 | ok | 30 | 0ms | 0ms | 0ms |
| 140.0 | 150.0 | end-users | ok | 54 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | app1 | ok | 25 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | app2 | ok | 29 | 0ms | 0ms | 0ms |
| 150.0 | 160.0 | end-users | ok | 60 | 0ms | 0ms | 0ms |
| 160.0 | 170.0 | app1 | ok | 30 | 0ms | 0ms | 0ms |
| 160.0 | 170.0 | app2 | ok | 28 | 0ms | 0ms | 0ms |
| 160.0 | 170.0 | end-users | ok | 57 | 0ms | 0ms | 0ms |
| 170.0 | 180.0 | app1 | ok | 29 | 0ms | 0ms | 0ms |
| 170.0 | 180.0 | app2 | ok | 27 | 0ms | 0ms | 0ms |
| 170.0 | 180.0 | end-users | ok | 58 | 0ms | 0ms | 0ms |
| 180.0 | 190.0 | app1 | ok | 29 | 0ms | 0ms | 0ms |
| 180.0 | 190.0 | app2 | ok | 30 | 0ms | 0ms | 0ms |
| 180.0 | 190.0 | end-users | ok | 54 | 0ms | 0ms | 0ms |
| 190.0 | 200.0 | app1 | ok | 30 | 0ms | 0ms | 0ms |
| 190.0 | 200.0 | app2 | ok | 28 | 0ms | 0ms | 0ms |
| 190.0 | 200.0 | end-users | ok | 58 | 0ms | 0ms | 0ms |
| 200.0 | 210.0 | app1 | ok | 25 | 0ms | 0ms | 0ms |
| 200.0 | 210.0 | app2 | ok | 30 | 0ms | 0ms | 0ms |
| 200.0 | 210.0 | end-users | ok | 59 | 0ms | 0ms | 0ms |
| 210.0 | 220.0 | app1 | ok | 31 | 0ms | 0ms | 0ms |
| 210.0 | 220.0 | app2 | ok | 27 | 0ms | 0ms | 0ms |
| 210.0 | 220.0 | end-users | ok | 56 | 0ms | 0ms | 0ms |
| 220.0 | 230.0 | app1 | ok | 30 | 0ms | 0ms | 0ms |
| 220.0 | 230.0 | app2 | ok | 28 | 0ms | 0ms | 0ms |
| 220.0 | 230.0 | end-users | ok | 56 | 0ms | 0ms | 0ms |
| 230.0 | 240.0 | app1 | ok | 27 | 0ms | 0ms | 0ms |
| 230.0 | 240.0 | app2 | ok | 29 | 0ms | 0ms | 0ms |
| 230.0 | 240.0 | end-users | ok | 56 | 0ms | 0ms | 0ms |
| 240.0 | 250.0 | app1 | ok | 5 | 0ms | 0ms | 0ms |
| 240.0 | 250.0 | app2 | ok | 3 | 0ms | 0ms | 0ms |
| 240.0 | 250.0 | end-users | ok | 10 | 0ms | 0ms | 0ms |
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
| app1 | 875760 | 43274 | 915167.0 | -0.4% | n/a | 962308.0 | n/a | False |
| app2 | 868380 | 42963 | 908755.0 | -0.3% | n/a | 954306.0 | n/a | False |
| end-users | 1741680 | 86028 | 1819966.0 | -0.4% | n/a | 1913736.0 | n/a | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 731 | 0 | 0 | 0 (never shed) | 0.00% | 30.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 731 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1466 | 0 | 0 | 0 (never shed) | 0.00% | 60.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=2834). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 2834 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 251074 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
