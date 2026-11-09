# Fairness benchmark: full-contention (uni-212-reverify-f3-40-20-40)

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
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-85b4699458-8xjzr` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T20:47:22Z` |
| Run end | `2026-11-09T20:51:45Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 40.0 | 32 | 497 | 200=482, 500=15 | 16.8 | 17.1 | n/a | 40.0% | 0.0% | -40.0 | 16.5% | -23.5 | n/a | 98.9% | 476.0 |
| app2 | 20.0 | 32 | 503 | 200=482, 500=21 | 16.8 | 17.1 | n/a | 20.0% | 0.0% | -20.0 | 16.7% | -3.3 | n/a | 98.9% | 478.0 |
| end-users | 40.0 | 128 | 2008 | 200=1916, 500=92 | 16.8 | 17.1 | n/a | 40.0% | 0.0% | -40.0 | 66.8% | 26.8 | n/a | 98.9% | 1902.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 24.0 |

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
| 0.0 | 10.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 0.0 | 10.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 0.0 | 10.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 10.0 | 20.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 10.0 | 20.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 10.0 | 20.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 20.0 | 31.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 20.0 | 31.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 20.0 | 31.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 31.0 | 41.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 31.0 | 41.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 31.0 | 41.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 41.0 | 51.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 41.0 | 51.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 41.0 | 51.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 51.0 | 61.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 51.0 | 61.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 51.0 | 61.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 61.0 | 71.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 61.0 | 71.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 61.0 | 71.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 71.0 | 81.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 71.0 | 81.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 71.0 | 81.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 81.0 | 91.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 81.0 | 91.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 81.0 | 91.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 91.0 | 101.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 91.0 | 101.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 91.0 | 101.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 101.0 | 111.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 101.0 | 111.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 101.0 | 111.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 111.0 | 121.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 111.0 | 121.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 111.0 | 121.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 121.0 | 131.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 121.0 | 131.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 121.0 | 131.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 131.0 | 141.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 131.0 | 141.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 131.0 | 141.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 141.0 | 151.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 141.0 | 151.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 141.0 | 151.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 151.0 | 161.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 151.0 | 161.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 151.0 | 161.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 161.0 | 171.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 161.0 | 171.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 161.0 | 171.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 171.0 | 181.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 171.0 | 181.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 171.0 | 181.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 181.0 | 191.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 181.0 | 191.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 181.0 | 191.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 191.0 | 201.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 191.0 | 201.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 191.0 | 201.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 201.0 | 211.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 201.0 | 211.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 201.0 | 211.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 211.0 | 221.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 211.0 | 221.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 211.0 | 221.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 221.0 | 231.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 221.0 | 231.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 221.0 | 231.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 231.0 | 241.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 231.0 | 241.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 231.0 | 241.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 241.0 | 251.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 26 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 30 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 111 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 28 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app2 | ok | 30 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | end-users | ok | 120 | 0ms | 0ms | 0ms |
| 20.0 | 31.0 | app1 | ok | 23 | 0ms | 0ms | 0ms |
| 20.0 | 31.0 | app2 | ok | 16 | 0ms | 0ms | 0ms |
| 20.0 | 31.0 | end-users | ok | 75 | 0ms | 0ms | 0ms |
| 31.0 | 41.0 | app1 | ok | 21 | 0ms | 0ms | 0ms |
| 31.0 | 41.0 | app2 | ok | 21 | 0ms | 0ms | 0ms |
| 31.0 | 41.0 | end-users | ok | 73 | 0ms | 0ms | 0ms |
| 41.0 | 51.0 | app1 | ok | 16 | 0ms | 0ms | 0ms |
| 41.0 | 51.0 | app2 | ok | 19 | 0ms | 0ms | 0ms |
| 41.0 | 51.0 | end-users | ok | 81 | 0ms | 0ms | 0ms |
| 51.0 | 61.0 | app1 | ok | 19 | 0ms | 0ms | 0ms |
| 51.0 | 61.0 | app2 | ok | 17 | 0ms | 0ms | 0ms |
| 51.0 | 61.0 | end-users | ok | 78 | 0ms | 0ms | 0ms |
| 61.0 | 71.0 | app1 | ok | 17 | 0ms | 0ms | 0ms |
| 61.0 | 71.0 | app2 | ok | 21 | 0ms | 0ms | 0ms |
| 61.0 | 71.0 | end-users | ok | 76 | 0ms | 0ms | 0ms |
| 71.0 | 81.0 | app1 | ok | 22 | 0ms | 0ms | 0ms |
| 71.0 | 81.0 | app2 | ok | 17 | 0ms | 0ms | 0ms |
| 71.0 | 81.0 | end-users | ok | 74 | 0ms | 0ms | 0ms |
| 81.0 | 91.0 | app1 | ok | 20 | 0ms | 0ms | 0ms |
| 81.0 | 91.0 | app2 | ok | 21 | 0ms | 0ms | 0ms |
| 81.0 | 91.0 | end-users | ok | 73 | 0ms | 0ms | 0ms |
| 91.0 | 101.0 | app1 | ok | 18 | 0ms | 0ms | 0ms |
| 91.0 | 101.0 | app2 | ok | 19 | 0ms | 0ms | 0ms |
| 91.0 | 101.0 | end-users | ok | 75 | 0ms | 0ms | 0ms |
| 101.0 | 111.0 | app1 | ok | 19 | 0ms | 0ms | 0ms |
| 101.0 | 111.0 | app2 | ok | 16 | 0ms | 0ms | 0ms |
| 101.0 | 111.0 | end-users | ok | 78 | 0ms | 0ms | 0ms |
| 111.0 | 121.0 | app1 | ok | 15 | 0ms | 0ms | 0ms |
| 111.0 | 121.0 | app2 | ok | 23 | 0ms | 0ms | 0ms |
| 111.0 | 121.0 | end-users | ok | 75 | 0ms | 0ms | 0ms |
| 121.0 | 131.0 | app1 | ok | 23 | 0ms | 0ms | 0ms |
| 121.0 | 131.0 | app2 | ok | 16 | 0ms | 0ms | 0ms |
| 121.0 | 131.0 | end-users | ok | 77 | 0ms | 0ms | 0ms |
| 131.0 | 141.0 | app1 | ok | 19 | 0ms | 0ms | 0ms |
| 131.0 | 141.0 | app2 | ok | 21 | 0ms | 0ms | 0ms |
| 131.0 | 141.0 | end-users | ok | 73 | 0ms | 0ms | 0ms |
| 141.0 | 151.0 | app1 | ok | 19 | 0ms | 0ms | 0ms |
| 141.0 | 151.0 | app2 | ok | 17 | 0ms | 0ms | 0ms |
| 141.0 | 151.0 | end-users | ok | 76 | 0ms | 0ms | 0ms |
| 151.0 | 161.0 | app1 | ok | 20 | 0ms | 0ms | 0ms |
| 151.0 | 161.0 | app2 | ok | 19 | 0ms | 0ms | 0ms |
| 151.0 | 161.0 | end-users | ok | 76 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | app1 | ok | 15 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | app2 | ok | 22 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | end-users | ok | 77 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | app1 | ok | 23 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | app2 | ok | 16 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | end-users | ok | 74 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | app1 | ok | 18 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | app2 | ok | 22 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | end-users | ok | 78 | 0ms | 0ms | 0ms |
| 191.0 | 201.0 | app1 | ok | 19 | 0ms | 0ms | 0ms |
| 191.0 | 201.0 | app2 | ok | 16 | 0ms | 0ms | 0ms |
| 191.0 | 201.0 | end-users | ok | 76 | 0ms | 0ms | 0ms |
| 201.0 | 211.0 | app1 | ok | 20 | 0ms | 0ms | 0ms |
| 201.0 | 211.0 | app2 | ok | 20 | 0ms | 0ms | 0ms |
| 201.0 | 211.0 | end-users | ok | 74 | 0ms | 0ms | 0ms |
| 211.0 | 221.0 | app1 | ok | 14 | 0ms | 0ms | 0ms |
| 211.0 | 221.0 | app2 | ok | 22 | 0ms | 0ms | 0ms |
| 211.0 | 221.0 | end-users | ok | 79 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | app1 | ok | 24 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | app2 | ok | 15 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | end-users | ok | 76 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | app1 | ok | 17 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | app2 | ok | 22 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | end-users | ok | 77 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | app1 | ok | 1 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost n/a
- app2 exceeded the 10% ledger tolerance: cost n/a
- end-users exceeded the 10% ledger tolerance: cost n/a

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 592860 | 29377 | 614493.0 | -1.2% | n/a | 651614.0 | n/a | False |
| app2 | 592860 | 29341 | 617040.0 | -0.8% | n/a | 651542.0 | n/a | False |
| end-users | 2356680 | 116208 | 2454857.0 | -0.7% | n/a | 2589096.0 | n/a | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 497 | 0 | 0 | 0 (never shed) | 0.00% | 40.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 503 | 0 | 0 | 0 (never shed) | 0.00% | 20.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2008 | 0 | 0 | 0 (never shed) | 0.00% | 40.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=2880). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 2880 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 250937 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
