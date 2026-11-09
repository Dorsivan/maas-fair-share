# Fairness benchmark: full-contention (uni-213-c6-rerun3)

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
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-d6cb4dbd5-hbrxz` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T18:49:14Z` |
| Run end | `2026-11-09T18:54:39Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1111 | 200=1104, 500=7 | 7.0 | 7.3 | n/a | 21.1% | 0.0% | -21.1 | 19.8% | -1.2 | n/a | 98.9% | 1104.0 |
| app2 | 10.0 | 32 | 53 | 000=32, 400=2, 500=19 | 300.4 | 300.9 | n/a | 10.5% | 0.0% | -10.5 | 0.9% | -9.6 | n/a | n/a | 32.0 |
| end-users | 65.0 | 128 | 4444 | 200=4380, 500=64 | 7.0 | 7.3 | n/a | 68.4% | 0.0% | -68.4 | 79.2% | 10.8 | n/a | 98.9% | 4378.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 4.0 |

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
| 10.0 | 21.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 10.0 | 21.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 10.0 | 21.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 21.0 | 31.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 21.0 | 31.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 21.0 | 31.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 31.0 | 41.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 31.0 | 41.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 31.0 | 41.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 41.0 | 51.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 41.0 | 51.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 41.0 | 51.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 51.0 | 61.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 51.0 | 61.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 51.0 | 61.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 61.0 | 71.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 61.0 | 71.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 61.0 | 71.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 71.0 | 81.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 71.0 | 81.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 71.0 | 81.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
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
| 321.0 | 325.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 325.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 325.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 26 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 11 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 73 | 0ms | 0ms | 0ms |
| 10.0 | 21.0 | app1 | ok | 70 | 0ms | 0ms | 0ms |
| 10.0 | 21.0 | app2 | ok | 21 | 0ms | 0ms | 0ms |
| 10.0 | 21.0 | end-users | ok | 300 | 0ms | 0ms | 0ms |
| 21.0 | 31.0 | app1 | ok | 52 | 0ms | 0ms | 0ms |
| 21.0 | 31.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 21.0 | 31.0 | end-users | ok | 176 | 0ms | 0ms | 0ms |
| 31.0 | 41.0 | app1 | ok | 41 | 0ms | 0ms | 0ms |
| 31.0 | 41.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 31.0 | 41.0 | end-users | ok | 188 | 0ms | 0ms | 0ms |
| 41.0 | 51.0 | app1 | ok | 49 | 0ms | 0ms | 0ms |
| 41.0 | 51.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 41.0 | 51.0 | end-users | ok | 177 | 0ms | 0ms | 0ms |
| 51.0 | 61.0 | app1 | ok | 44 | 0ms | 0ms | 0ms |
| 51.0 | 61.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 51.0 | 61.0 | end-users | ok | 182 | 0ms | 0ms | 0ms |
| 61.0 | 71.0 | app1 | ok | 43 | 0ms | 0ms | 0ms |
| 61.0 | 71.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 61.0 | 71.0 | end-users | ok | 184 | 0ms | 0ms | 0ms |
| 71.0 | 81.0 | app1 | ok | 50 | 0ms | 0ms | 0ms |
| 71.0 | 81.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 71.0 | 81.0 | end-users | ok | 176 | 0ms | 0ms | 0ms |
| 81.0 | 91.0 | app1 | ok | 38 | 0ms | 0ms | 0ms |
| 81.0 | 91.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 188 | 0ms | 0ms | 0ms |
| 91.0 | 101.0 | app1 | ok | 52 | 0ms | 0ms | 0ms |
| 91.0 | 101.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 174 | 0ms | 0ms | 0ms |
| 101.0 | 111.0 | app1 | ok | 42 | 0ms | 0ms | 0ms |
| 101.0 | 111.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 185 | 0ms | 0ms | 0ms |
| 111.0 | 121.0 | app1 | ok | 46 | 0ms | 0ms | 0ms |
| 111.0 | 121.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 179 | 0ms | 0ms | 0ms |
| 121.0 | 131.0 | app1 | ok | 46 | 0ms | 0ms | 0ms |
| 121.0 | 131.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 179 | 0ms | 0ms | 0ms |
| 131.0 | 141.0 | app1 | ok | 39 | 0ms | 0ms | 0ms |
| 131.0 | 141.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 185 | 0ms | 0ms | 0ms |
| 141.0 | 151.0 | app1 | ok | 53 | 0ms | 0ms | 0ms |
| 141.0 | 151.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 172 | 0ms | 0ms | 0ms |
| 151.0 | 161.0 | app1 | ok | 40 | 0ms | 0ms | 0ms |
| 151.0 | 161.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 185 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | app1 | ok | 46 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 181 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 180 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | app1 | ok | 40 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 185 | 0ms | 0ms | 0ms |
| 191.0 | 201.0 | app1 | ok | 53 | 0ms | 0ms | 0ms |
| 191.0 | 201.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 174 | 0ms | 0ms | 0ms |
| 201.0 | 211.0 | app1 | ok | 40 | 0ms | 0ms | 0ms |
| 201.0 | 211.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 186 | 0ms | 0ms | 0ms |
| 211.0 | 221.0 | app1 | ok | 48 | 0ms | 0ms | 0ms |
| 211.0 | 221.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 178 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | app1 | ok | 44 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 184 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | app1 | ok | 44 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 184 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | app1 | ok | 11 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 23 | 0ms | 0ms | 0ms |
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
| 321.0 | 325.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 325.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 325.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost n/a
- app2 exceeded the 10% ledger tolerance: raw tokens n/a, cost n/a
- end-users exceeded the 10% ledger tolerance: cost n/a

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1357920 | 67179 | 1425099.0 | 0.0% | n/a | 1492278.0 | n/a | False |
| app2 | 0 | 0 | n/a | n/a | n/a | 0.0 | n/a | False |
| end-users | 5387400 | 267615 | 5652430.0 | -0.0% | n/a | 5922630.0 | n/a | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1111 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 53 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 4444 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5518). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5518 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 315474 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
