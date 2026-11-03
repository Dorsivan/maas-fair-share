# Fairness benchmark: near-timeout-long-generations (uni-150-c4-near-timeout-v3)

**Verdict: UNCONTENDED** -- every offered group's `contended_seconds_total` delta stayed under 1s, so the pool was never actually contended. Not scored against the 10-point weighted-split threshold; see docs/runbook.md.

- every offered group's contended_seconds_total delta stayed under 1s (app1=0.13s, app2=0.16s, end-users=0.11s) -- an order of magnitude below the ~9s a genuinely-contending tenant accrues in a 240s full-contention run (docs/runbook.md), so nobody was ever backlogged alongside anyone else and the weighted-split deviation check does not apply

## Run metadata

| field | value |
|---|---|
| Scenario | `near-timeout-long-generations` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `300` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-md5qv` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-03T10:20:18Z` |
| Run end | `2026-11-03T10:32:09Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 90 | 200=65, 500=25 | 103.3 | 594.3 | 85224.0 | 21.1% | 8.2% | -12.9 | 34.1% | 13.0 | 0.1s | 98.9% | 64.0 |
| app2 | 10.0 | 32 | 81 | 200=59, 500=22 | 199.6 | 593.6 | 75752.0 | 10.5% | 7.3% | -3.2 | 30.7% | 20.2 | 0.2s | 98.9% | 58.0 |
| end-users | 65.0 | 48 | 93 | 200=84, 500=9 | 297.9 | 402.8 | 878148.0 | 68.4% | 84.5% | 16.1 | 35.2% | -33.2 | 0.1s | 77.4% | 81.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 51494.0 | n/a | n/a | n/a | n/a | n/a | 0.0s | 97.4% | 5.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-300s, no duty cycle
- app2: active 0s-300s, no duty cycle
- end-users: active 0s-300s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 300.0 | n/a (never converged in this phase) | n/a |

**Windows** (71 total):

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
| 100.0 | 110.0 | app1 | True | 27038.0 | 21.1% | 68.9% | 47.9 |
| 100.0 | 110.0 | app2 | True | 12188.0 | 10.5% | 31.1% | 20.5 |
| 100.0 | 110.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 110.0 | 120.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 110.0 | 120.0 | app2 | True | 1334.0 | 10.5% | 100.0% | 89.5 |
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
| 190.0 | 200.0 | app1 | True | 1358.0 | 21.1% | 7.7% | -13.3 |
| 190.0 | 200.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 190.0 | 200.0 | end-users | True | 16262.0 | 68.4% | 92.3% | 23.9 |
| 200.0 | 210.0 | app1 | True | 13550.0 | 21.1% | 14.3% | -6.8 |
| 200.0 | 210.0 | app2 | True | 16230.0 | 10.5% | 17.1% | 6.6 |
| 200.0 | 210.0 | end-users | True | 65048.0 | 68.4% | 68.6% | 0.2 |
| 210.0 | 220.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 210.0 | 220.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 210.0 | 220.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 220.0 | 230.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 220.0 | 230.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 220.0 | 230.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 230.0 | 240.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 230.0 | 240.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 230.0 | 240.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 240.0 | 250.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 240.0 | 250.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 240.0 | 250.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 250.0 | 260.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 250.0 | 260.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 250.0 | 260.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 260.0 | 270.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 260.0 | 270.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 260.0 | 270.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 270.0 | 280.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 270.0 | 280.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 270.0 | 280.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 280.0 | 290.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 280.0 | 290.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 280.0 | 290.0 | end-users | True | 0.0 | 68.4% | 0.0% | -68.4 |
| 290.0 | 300.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 290.0 | 300.0 | app2 | True | 2678.0 | 10.5% | 7.6% | -2.9 |
| 290.0 | 300.0 | end-users | True | 32524.0 | 68.4% | 92.4% | 24.0 |
| 300.0 | 310.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app2 | False | 9492.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | end-users | False | 97572.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 330.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 330.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 330.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 330.0 | 340.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 330.0 | 340.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 330.0 | 340.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 340.0 | 351.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 340.0 | 351.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 340.0 | 351.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | False | 16262.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | end-users | False | 113834.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 501.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 491.0 | 501.0 | end-users | False | 162620.0 | n/a | n/a | n/a |
| 501.0 | 511.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 511.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 511.0 | end-users | False | 81310.0 | n/a | n/a | n/a |
| 511.0 | 521.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 511.0 | 521.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 511.0 | 521.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 521.0 | 531.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 521.0 | 531.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 521.0 | 531.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 531.0 | 541.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 531.0 | 541.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 531.0 | 541.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 541.0 | 551.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 541.0 | 551.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 541.0 | 551.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 551.0 | 561.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 551.0 | 561.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 551.0 | 561.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 561.0 | 571.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 561.0 | 571.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 561.0 | 571.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 571.0 | 581.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 571.0 | 581.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 571.0 | 581.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 581.0 | 591.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 581.0 | 591.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 581.0 | 591.0 | end-users | False | 32524.0 | n/a | n/a | n/a |
| 591.0 | 601.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 591.0 | 601.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 591.0 | 601.0 | end-users | False | 130096.0 | n/a | n/a | n/a |
| 601.0 | 611.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 601.0 | 611.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 601.0 | 611.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 611.0 | 621.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 611.0 | 621.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 611.0 | 621.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 621.0 | 631.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 621.0 | 631.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 621.0 | 631.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 631.0 | 641.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 631.0 | 641.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 631.0 | 641.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 641.0 | 651.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 641.0 | 651.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 641.0 | 651.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 651.0 | 661.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 651.0 | 661.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 651.0 | 661.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 661.0 | 671.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 661.0 | 671.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 661.0 | 671.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 671.0 | 681.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 671.0 | 681.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 671.0 | 681.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 681.0 | 691.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 681.0 | 691.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 681.0 | 691.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 691.0 | 701.0 | app1 | False | 43278.0 | n/a | n/a | n/a |
| 691.0 | 701.0 | app2 | False | 33830.0 | n/a | n/a | n/a |
| 691.0 | 701.0 | end-users | False | 130096.0 | n/a | n/a | n/a |
| 701.0 | 711.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 701.0 | 711.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 701.0 | 711.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- end-users exceeded the 10% ledger tolerance: cost -35.7%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 79950 | 3991 | 82651.0 | -1.5% | 85224.0 | 87932.0 | -3.1% | True |
| app2 | 72570 | 3603 | 74879.0 | -1.7% | 75752.0 | 79776.0 | -5.0% | True |
| end-users | 5208 | 680400 | 661122.0 | -3.6% | 878148.0 | 1366008.0 | -35.7% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 90 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 81 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 93 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide):** not recorded -- `llm_d_epp_flow_control_requests_total` is absent from both snapshots, so whether the EPP or something in front of it (Kuadrant) produced the client's 429s is unknown.

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
