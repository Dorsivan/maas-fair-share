# Fairness benchmark: full-contention (uni-213-c5-rerun)

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
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:b0bc21af3ebb7889cb20b574371e53a2b33c7efd610e73db48a60bccfa6acf4d` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-d6cb4dbd5-88j48` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T18:59:40Z` |
| Run end | `2026-11-09T19:05:02Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 938 | 200=661, 500=8 | 8.4 | 8.7 | n/a | 21.1% | 0.0% | -21.1 | 16.7% | -4.3 | n/a | 98.9% | 925.0 |
| app2 | 10.0 | 32 | 937 | 200=926, 500=11 | 8.4 | 8.7 | n/a | 10.5% | 0.0% | -10.5 | 16.7% | 6.2 | n/a | 98.9% | 926.0 |
| end-users | 65.0 | 128 | 3739 | 200=3694, 500=45 | 8.4 | 8.7 | n/a | 68.4% | 0.0% | -68.4 | 66.6% | -1.8 | n/a | 98.9% | 3688.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 7.0 |

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
| 140.0 | 151.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 140.0 | 151.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 140.0 | 151.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
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
| 191.0 | 201.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 191.0 | 201.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 191.0 | 201.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 201.0 | 211.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 201.0 | 211.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 201.0 | 211.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 211.0 | 221.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 211.0 | 221.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 211.0 | 221.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 221.0 | 231.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 221.0 | 231.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 221.0 | 231.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 231.0 | 241.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 231.0 | 241.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 231.0 | 241.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 241.0 | 251.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 322.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 322.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 322.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 33 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 31 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 125 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 60 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app2 | ok | 60 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | end-users | ok | 231 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app1 | ok | 37 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app2 | ok | 38 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | end-users | ok | 151 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app1 | ok | 39 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app2 | ok | 39 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | end-users | ok | 151 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | app1 | ok | 37 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | app2 | ok | 38 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | end-users | ok | 151 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app1 | ok | 35 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app2 | ok | 38 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | end-users | ok | 153 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app1 | ok | 41 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app2 | ok | 35 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | end-users | ok | 152 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app1 | ok | 39 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app2 | ok | 39 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | end-users | ok | 148 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app1 | ok | 36 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app2 | ok | 38 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | end-users | ok | 151 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | app1 | ok | 38 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | app2 | ok | 37 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | end-users | ok | 151 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | app1 | ok | 35 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | app2 | ok | 39 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | end-users | ok | 150 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | app1 | ok | 37 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | app2 | ok | 37 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | end-users | ok | 153 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | app1 | ok | 39 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | app2 | ok | 36 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | end-users | ok | 153 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | app1 | ok | 39 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | app2 | ok | 39 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | end-users | ok | 148 | 0ms | 0ms | 0ms |
| 140.0 | 151.0 | app1 | ok | 40 | 0ms | 0ms | 0ms |
| 140.0 | 151.0 | app2 | ok | 37 | 0ms | 0ms | 0ms |
| 140.0 | 151.0 | end-users | ok | 151 | 0ms | 0ms | 0ms |
| 151.0 | 161.0 | app1 | ok | 35 | 0ms | 0ms | 0ms |
| 151.0 | 161.0 | app2 | ok | 40 | 0ms | 0ms | 0ms |
| 151.0 | 161.0 | end-users | ok | 152 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | app1 | ok | 36 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | app2 | ok | 37 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | end-users | ok | 155 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | app1 | ok | 40 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | app2 | ok | 36 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | end-users | ok | 149 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | app1 | ok | 38 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | app2 | ok | 40 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | end-users | ok | 149 | 0ms | 0ms | 0ms |
| 191.0 | 201.0 | app1 | ok | 37 | 0ms | 0ms | 0ms |
| 191.0 | 201.0 | app2 | ok | 37 | 0ms | 0ms | 0ms |
| 191.0 | 201.0 | end-users | ok | 153 | 0ms | 0ms | 0ms |
| 201.0 | 211.0 | app1 | ok | 40 | 0ms | 0ms | 1ms |
| 201.0 | 211.0 | app2 | ok | 39 | 0ms | 0ms | 0ms |
| 201.0 | 211.0 | end-users | ok | 147 | 0ms | 0ms | 0ms |
| 211.0 | 221.0 | app1 | ok | 35 | 0ms | 0ms | 0ms |
| 211.0 | 221.0 | app2 | ok | 38 | 0ms | 0ms | 0ms |
| 211.0 | 221.0 | end-users | ok | 153 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | app1 | ok | 37 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | app2 | ok | 36 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | end-users | ok | 150 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | app1 | ok | 39 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | app2 | ok | 36 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | end-users | ok | 150 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | app1 | ok | 3 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | app2 | ok | 6 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | end-users | ok | 11 | 0ms | 0ms | 0ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 322.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 322.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 322.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens +39.9%, cost n/a
- app2 exceeded the 10% ledger tolerance: cost n/a
- end-users exceeded the 10% ledger tolerance: cost n/a

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 813030 | 40432 | 1194365.0 | 39.9% | n/a | 893894.0 | n/a | False |
| app2 | 1138980 | 56397 | 1195377.0 | 0.0% | n/a | 1251774.0 | n/a | False |
| end-users | 4543620 | 225398 | 4761269.0 | -0.2% | n/a | 4994416.0 | n/a | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 938 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 937 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3739 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5546). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5546 | 0.050ms | 0.100ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 312150 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
