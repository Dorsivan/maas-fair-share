# Fairness benchmark: full-contention (uni-168-stock)

**Verdict: FAIL** -- named negative control, not scored against the 10-point threshold. Expected to NOT reproduce the configured weights; see docs/runbook.md.

- offered groups delivered zero contended service tokens -- the EPP accounted nothing for this run

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `False` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real, stock upstream EPP)` |
| EPP image digest | `ghcr.io/llm-d/llm-d-router-endpoint-picker@sha256:39257d24552d16d8f215d3de25cc734fd44af3b282b67032db01aff900c610cf` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-599f477bb9-5gsh9` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T13:50:08Z` |
| Run end | `2026-11-09T13:54:30Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | n/a | 32 | 944 | 200=929, 500=15 | 8.4 | 8.7 | n/a | n/a | 0.0% | n/a | 16.7% | n/a | n/a | n/a | n/a |
| app2 | n/a | 32 | 941 | 200=924, 500=17 | 8.4 | 8.7 | n/a | n/a | 0.0% | n/a | 16.7% | n/a | n/a | n/a | n/a |
| end-users | n/a | 128 | 3766 | 200=3669, 500=97 | 8.4 | 8.7 | n/a | n/a | 0.0% | n/a | 66.6% | n/a | n/a | n/a | n/a |

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
| 0.0 | 10.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 0.0 | 10.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 0.0 | 10.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 10.0 | 20.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 10.0 | 20.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 10.0 | 20.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 20.0 | 30.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 20.0 | 30.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 20.0 | 30.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 30.0 | 40.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 30.0 | 40.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 30.0 | 40.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 40.0 | 50.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 40.0 | 50.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 40.0 | 50.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 50.0 | 60.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 50.0 | 60.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 50.0 | 60.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 60.0 | 70.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 60.0 | 70.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 60.0 | 70.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 70.0 | 80.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 70.0 | 80.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 70.0 | 80.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 80.0 | 90.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 80.0 | 90.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 80.0 | 90.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 90.0 | 100.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 90.0 | 100.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 90.0 | 100.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 100.0 | 110.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 100.0 | 110.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 100.0 | 110.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 110.0 | 120.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 110.0 | 120.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 110.0 | 120.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 120.0 | 130.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 120.0 | 130.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 120.0 | 130.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 130.0 | 140.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 130.0 | 140.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 130.0 | 140.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 140.0 | 150.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 140.0 | 150.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 140.0 | 150.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 150.0 | 160.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 150.0 | 160.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 150.0 | 160.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 160.0 | 170.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 160.0 | 170.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 160.0 | 170.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 170.0 | 180.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 170.0 | 180.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 170.0 | 180.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 180.0 | 190.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 180.0 | 190.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 180.0 | 190.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 190.0 | 200.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 190.0 | 200.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 190.0 | 200.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 200.0 | 210.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 200.0 | 210.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 200.0 | 210.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 210.0 | 220.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 210.0 | 220.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 210.0 | 220.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 220.0 | 230.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 220.0 | 230.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 220.0 | 230.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
| 230.0 | 240.0 | app1 | True | 0.0 | n/a | 0.0% | n/a |
| 230.0 | 240.0 | app2 | True | 0.0 | n/a | 0.0% | n/a |
| 230.0 | 240.0 | end-users | True | 0.0 | n/a | 0.0% | n/a |
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
| 0.0 | 10.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 20.0 | 30.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 20.0 | 30.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 20.0 | 30.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 30.0 | 40.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 30.0 | 40.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 40.0 | 50.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 40.0 | 50.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 50.0 | 60.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 50.0 | 60.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 50.0 | 60.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 60.0 | 70.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 60.0 | 70.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 60.0 | 70.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 70.0 | 80.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 70.0 | 80.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 70.0 | 80.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 80.0 | 90.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 80.0 | 90.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 80.0 | 90.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 90.0 | 100.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 90.0 | 100.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 90.0 | 100.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 100.0 | 110.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 100.0 | 110.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 100.0 | 110.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 110.0 | 120.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 110.0 | 120.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 110.0 | 120.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 120.0 | 130.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 120.0 | 130.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 130.0 | 140.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 130.0 | 140.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 130.0 | 140.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 140.0 | 150.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 140.0 | 150.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 140.0 | 150.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 150.0 | 160.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 150.0 | 160.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 150.0 | 160.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 160.0 | 170.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 160.0 | 170.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 160.0 | 170.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 170.0 | 180.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 170.0 | 180.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 170.0 | 180.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 180.0 | 190.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 180.0 | 190.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 180.0 | 190.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 190.0 | 200.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 190.0 | 200.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 190.0 | 200.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 200.0 | 210.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 200.0 | 210.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 200.0 | 210.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 210.0 | 220.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 210.0 | 220.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 210.0 | 220.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 220.0 | 230.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 220.0 | 230.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 220.0 | 230.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 230.0 | 240.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 230.0 | 240.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 230.0 | 240.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 240.0 | 250.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 260.0 | 262.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=1 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens n/a, cost n/a
- app2 exceeded the 10% ledger tolerance: raw tokens n/a, cost n/a
- end-users exceeded the 10% ledger tolerance: raw tokens n/a, cost n/a

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1142670 | 56585 | n/a | n/a | n/a | 1199255.0 | n/a | False |
| app2 | 1136520 | 56004 | n/a | n/a | n/a | 1192524.0 | n/a | False |
| end-users | 4512870 | 223592 | n/a | n/a | n/a | 4736462.0 | n/a | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 944 | 0 | 0 | 0 (never shed) | 0.00% | n/a | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 941 | 0 | 0 | 0 (never shed) | 0.00% | n/a | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3766 | 0 | 0 | 0 (never shed) | 0.00% | n/a | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide):** not recorded -- `llm_d_epp_flow_control_requests_total` is absent from both snapshots, so whether the EPP or something in front of it (Kuadrant) produced the client's 429s is unknown.

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5522 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
