# Fairness benchmark: full-contention (uni310-l2-r3-e1-epp-restart)

**Verdict: PASS** **(NON-DISCRIMINATING)** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 6.1 points -- below the pass bar, so this row cannot tell 'the split follows the weights' apart from 'the split follows the workers'

- NON-DISCRIMINATING (UNI-225): offered worker shares stay within 6.1 points of the configured weight shares, under the 10-point bar -- 'follows the weights' and 'follows the workers' predict the same split here, so this PASS is not evidence for weighted fairness specifically

**Caveat (UNI-230): a mid-run metrics scrape failed outright, not an EPP restart.** At least one windowed delta below was clamped to zero because its closing `/metrics` scrape itself failed (the benchmark's own recorded curl exit code was nonzero), not because a group's counter genuinely went backwards. A connection-level scrape failure and a real restart produce identical zero-line output once grepped, so this is flagged separately from `epp_restarted_in_windows_but_not_snapshot_pair` rather than folded into it or into `epp_restarted_mid_run`. The affected window's own numbers still undercount real traffic for that window, but this is evidence of a dropped scrape, not of a process restart -- check for corroborating restart evidence (pod identity change, k8s restart events, container restart count) before treating it as one.

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `360` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-8448f688f-gpklq` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T08:22:22Z` |
| Run end | `2026-11-26T08:29:31Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 40 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/40 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 70.50 | 2.2031 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 1738 | 000=9, 200=1729 | 4.3 | 8.0 | 1268478.0 | 21.1% | 16.7% | -4.4 | 20.5% | -0.6 | 21.2% | 0.1 | 4.9s | 98.9% | 988.0 |
| app2 | 10.0 | 32 | 915 | 000=20, 200=895 | 4.7 | 15.2 | 664464.0 | 10.5% | 16.7% | 6.1 | 10.7% | 0.2 | 11.1% | 0.6 | 5.1s | 98.9% | 495.0 |
| end-users | 65.0 | 128 | 5557 | 000=54, 200=5503 | 4.5 | 9.6 | 4254420.0 | 68.4% | 66.7% | -1.8 | 68.8% | 0.3 | 67.7% | -0.7 | 5.2s | 98.9% | 3211.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events (scheduled):**
- t+120s: epp_delete

**Per-tenant schedule:**
- app1: active 0s-360s, no duty cycle
- app2: active 0s-360s, no duty cycle
- end-users: active 0s-360s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 10.0 | 10.0 |
| 120.0 | 121.0 | 1.0 |
| 360.0 | n/a (never converged in this phase) | n/a |

**Windows** (43 total, a metrics scrape failed mid-window at least once (UNI-230, not a restart)):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 5420.0 | 21.1% | 66.9% | 45.8 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 10.5% | 0.0% | -10.5 |
| 0.0 | 10.0 | end-users | True | False | 2684.0 | 68.4% | 33.1% | -35.3 |
| 10.0 | 20.0 | app1 | True | False | 60788.0 | 21.1% | 22.1% | 1.1 |
| 10.0 | 20.0 | app2 | True | False | 18950.0 | 10.5% | 6.9% | -3.6 |
| 10.0 | 20.0 | end-users | True | False | 194814.0 | 68.4% | 71.0% | 2.5 |
| 20.0 | 30.0 | app1 | True | False | 63598.0 | 21.1% | 21.0% | -0.1 |
| 20.0 | 30.0 | app2 | True | False | 32514.0 | 10.5% | 10.7% | 0.2 |
| 20.0 | 30.0 | end-users | True | False | 207120.0 | 68.4% | 68.3% | -0.1 |
| 30.0 | 40.0 | app1 | True | False | 62316.0 | 21.1% | 20.5% | -0.6 |
| 30.0 | 40.0 | app2 | True | False | 31110.0 | 10.5% | 10.2% | -0.3 |
| 30.0 | 40.0 | end-users | True | False | 211024.0 | 68.4% | 69.3% | 0.9 |
| 40.0 | 50.0 | app1 | True | False | 64874.0 | 21.1% | 21.2% | 0.2 |
| 40.0 | 50.0 | app2 | True | False | 32498.0 | 10.5% | 10.6% | 0.1 |
| 40.0 | 50.0 | end-users | True | False | 208444.0 | 68.4% | 68.2% | -0.3 |
| 50.0 | 60.0 | app1 | True | False | 66192.0 | 21.1% | 21.6% | 0.5 |
| 50.0 | 60.0 | app2 | True | False | 32410.0 | 10.5% | 10.6% | 0.0 |
| 50.0 | 60.0 | end-users | True | False | 208368.0 | 68.4% | 67.9% | -0.5 |
| 60.0 | 71.0 | app1 | True | False | 63606.0 | 21.1% | 20.7% | -0.3 |
| 60.0 | 71.0 | app2 | True | False | 32414.0 | 10.5% | 10.6% | 0.0 |
| 60.0 | 71.0 | end-users | True | False | 210964.0 | 68.4% | 68.7% | 0.3 |
| 71.0 | 81.0 | app1 | True | False | 67734.0 | 21.1% | 22.8% | 1.7 |
| 71.0 | 81.0 | app2 | True | False | 31178.0 | 10.5% | 10.5% | -0.1 |
| 71.0 | 81.0 | end-users | True | False | 198778.0 | 68.4% | 66.8% | -1.6 |
| 81.0 | 91.0 | app1 | True | False | 59530.0 | 21.1% | 19.8% | -1.2 |
| 81.0 | 91.0 | app2 | True | False | 28424.0 | 10.5% | 9.5% | -1.1 |
| 81.0 | 91.0 | end-users | True | False | 212622.0 | 68.4% | 70.7% | 2.3 |
| 91.0 | 101.0 | app1 | True | False | 60818.0 | 21.1% | 20.1% | -1.0 |
| 91.0 | 101.0 | app2 | True | False | 36522.0 | 10.5% | 12.1% | 1.5 |
| 91.0 | 101.0 | end-users | True | False | 205650.0 | 68.4% | 67.9% | -0.5 |
| 101.0 | 111.0 | app1 | True | False | 65002.0 | 21.1% | 21.2% | 0.1 |
| 101.0 | 111.0 | app2 | True | False | 31106.0 | 10.5% | 10.1% | -0.4 |
| 101.0 | 111.0 | end-users | True | False | 210980.0 | 68.4% | 68.7% | 0.3 |
| 111.0 | 121.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 111.0 | 121.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 111.0 | 121.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 121.0 | 131.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 121.0 | 131.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 121.0 | 131.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 131.0 | 141.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 131.0 | 141.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 131.0 | 141.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 141.0 | 151.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 141.0 | 151.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 141.0 | 151.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 151.0 | 161.0 | app1 | True | False | 29748.0 | 21.1% | 21.3% | 0.3 |
| 151.0 | 161.0 | app2 | True | False | 14912.0 | 10.5% | 10.7% | 0.2 |
| 151.0 | 161.0 | end-users | True | False | 94728.0 | 68.4% | 68.0% | -0.5 |
| 161.0 | 171.0 | app1 | True | False | 59536.0 | 21.1% | 20.4% | -0.7 |
| 161.0 | 171.0 | app2 | True | False | 31110.0 | 10.5% | 10.6% | 0.1 |
| 161.0 | 171.0 | end-users | True | False | 201652.0 | 68.4% | 69.0% | 0.6 |
| 171.0 | 181.0 | app1 | True | False | 60858.0 | 21.1% | 20.6% | -0.4 |
| 171.0 | 181.0 | app2 | True | False | 32552.0 | 10.5% | 11.0% | 0.5 |
| 171.0 | 181.0 | end-users | True | False | 201558.0 | 68.4% | 68.3% | -0.1 |
| 181.0 | 191.0 | app1 | True | False | 60764.0 | 21.1% | 20.7% | -0.3 |
| 181.0 | 191.0 | app2 | True | False | 31160.0 | 10.5% | 10.6% | 0.1 |
| 181.0 | 191.0 | end-users | True | False | 201576.0 | 68.4% | 68.7% | 0.3 |
| 191.0 | 201.0 | app1 | True | False | 59536.0 | 21.1% | 20.1% | -1.0 |
| 191.0 | 201.0 | app2 | True | False | 31176.0 | 10.5% | 10.5% | -0.0 |
| 191.0 | 201.0 | end-users | True | False | 205664.0 | 68.4% | 69.4% | 1.0 |
| 201.0 | 211.0 | app1 | True | False | 58180.0 | 21.1% | 20.1% | -1.0 |
| 201.0 | 211.0 | app2 | True | False | 33870.0 | 10.5% | 11.7% | 1.2 |
| 201.0 | 211.0 | end-users | True | False | 197436.0 | 68.4% | 68.2% | -0.2 |
| 211.0 | 221.0 | app1 | True | False | 62112.0 | 21.1% | 20.5% | -0.5 |
| 211.0 | 221.0 | app2 | True | False | 31106.0 | 10.5% | 10.3% | -0.2 |
| 211.0 | 221.0 | end-users | True | False | 209394.0 | 68.4% | 69.2% | 0.8 |
| 221.0 | 231.0 | app1 | True | False | 56764.0 | 21.1% | 19.3% | -1.8 |
| 221.0 | 231.0 | app2 | True | False | 33834.0 | 10.5% | 11.5% | 0.9 |
| 221.0 | 231.0 | end-users | True | False | 204260.0 | 68.4% | 69.3% | 0.9 |
| 231.0 | 241.0 | app1 | True | False | 60850.0 | 21.1% | 20.4% | -0.6 |
| 231.0 | 241.0 | app2 | True | False | 31132.0 | 10.5% | 10.5% | -0.1 |
| 231.0 | 241.0 | end-users | True | False | 205654.0 | 68.4% | 69.1% | 0.7 |
| 241.0 | 251.0 | app1 | True | False | 63566.0 | 21.1% | 20.5% | -0.5 |
| 241.0 | 251.0 | app2 | True | False | 32500.0 | 10.5% | 10.5% | -0.0 |
| 241.0 | 251.0 | end-users | True | False | 213528.0 | 68.4% | 69.0% | 0.5 |
| 251.0 | 261.0 | app1 | True | False | 60916.0 | 21.1% | 20.7% | -0.3 |
| 251.0 | 261.0 | app2 | True | False | 31112.0 | 10.5% | 10.6% | 0.1 |
| 251.0 | 261.0 | end-users | True | False | 201598.0 | 68.4% | 68.7% | 0.2 |
| 261.0 | 271.0 | app1 | True | False | 62188.0 | 21.1% | 21.0% | -0.1 |
| 261.0 | 271.0 | app2 | True | False | 33794.0 | 10.5% | 11.4% | 0.9 |
| 261.0 | 271.0 | end-users | True | False | 200196.0 | 68.4% | 67.6% | -0.8 |
| 271.0 | 281.0 | app1 | True | False | 48668.0 | 21.1% | 19.4% | -1.6 |
| 271.0 | 281.0 | app2 | True | False | 25660.0 | 10.5% | 10.3% | -0.3 |
| 271.0 | 281.0 | end-users | True | False | 175936.0 | 68.4% | 70.3% | 1.9 |
| 281.0 | 291.0 | app1 | True | False | 62178.0 | 21.1% | 20.9% | -0.2 |
| 281.0 | 291.0 | app2 | True | False | 32492.0 | 10.5% | 10.9% | 0.4 |
| 281.0 | 291.0 | end-users | True | False | 202838.0 | 68.4% | 68.2% | -0.2 |
| 291.0 | 301.0 | app1 | True | False | 62196.0 | 21.1% | 20.9% | -0.2 |
| 291.0 | 301.0 | app2 | True | False | 31064.0 | 10.5% | 10.4% | -0.1 |
| 291.0 | 301.0 | end-users | True | False | 204388.0 | 68.4% | 68.7% | 0.2 |
| 301.0 | 312.0 | app1 | True | False | 62226.0 | 21.1% | 21.1% | 0.0 |
| 301.0 | 312.0 | app2 | True | False | 33924.0 | 10.5% | 11.5% | 1.0 |
| 301.0 | 312.0 | end-users | True | False | 198888.0 | 68.4% | 67.4% | -1.0 |
| 312.0 | 322.0 | app1 | True | False | 62232.0 | 21.1% | 21.2% | 0.1 |
| 312.0 | 322.0 | app2 | True | False | 29670.0 | 10.5% | 10.1% | -0.4 |
| 312.0 | 322.0 | end-users | True | False | 201758.0 | 68.4% | 68.7% | 0.3 |
| 322.0 | 332.0 | app1 | True | False | 62124.0 | 21.1% | 20.7% | -0.4 |
| 322.0 | 332.0 | app2 | True | False | 31116.0 | 10.5% | 10.4% | -0.2 |
| 322.0 | 332.0 | end-users | True | False | 207070.0 | 68.4% | 69.0% | 0.5 |
| 332.0 | 342.0 | app1 | True | False | 59596.0 | 21.1% | 20.2% | -0.8 |
| 332.0 | 342.0 | app2 | True | False | 28440.0 | 10.5% | 9.6% | -0.9 |
| 332.0 | 342.0 | end-users | True | False | 206910.0 | 68.4% | 70.2% | 1.7 |
| 342.0 | 352.0 | app1 | True | False | 59542.0 | 21.1% | 20.2% | -0.9 |
| 342.0 | 352.0 | app2 | True | False | 32534.0 | 10.5% | 11.0% | 0.5 |
| 342.0 | 352.0 | end-users | True | False | 202794.0 | 68.4% | 68.8% | 0.4 |
| 352.0 | 362.0 | app1 | True | False | 60858.0 | 21.1% | 20.6% | -0.4 |
| 352.0 | 362.0 | app2 | True | False | 32416.0 | 10.5% | 11.0% | 0.5 |
| 352.0 | 362.0 | end-users | True | False | 201544.0 | 68.4% | 68.4% | -0.1 |
| 362.0 | 372.0 | app1 | False | n/a | 33840.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | app2 | False | n/a | 18890.0 | n/a | n/a | n/a |
| 362.0 | 372.0 | end-users | False | n/a | 115050.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 372.0 | 382.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 382.0 | 392.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 392.0 | 402.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 402.0 | 412.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 412.0 | 422.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 429.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 429.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 422.0 | 429.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`, a metrics scrape failed mid-window at least once (UNI-230, not a restart)):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 46 | 0ms | 2040ms | 2454ms |
| 0.0 | 10.0 | app2 | ok | 23 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 147 | 0ms | 2099ms | 2460ms |
| 10.0 | 20.0 | app1 | ok | 54 | 1931ms | 4156ms | 4916ms |
| 10.0 | 20.0 | app2 | ok | 27 | 7500ms | 9500ms | 9950ms |
| 10.0 | 20.0 | end-users | ok | 174 | 3424ms | 4685ms | 4968ms |
| 20.0 | 30.0 | app1 | ok | 51 | 2031ms | 4292ms | 4929ms |
| 20.0 | 30.0 | app2 | ok | 26 | 7600ms | 9680ms | 24800ms |
| 20.0 | 30.0 | end-users | ok | 168 | 3489ms | 4698ms | 4970ms |
| 30.0 | 40.0 | app1 | ok | 47 | 1957ms | 4096ms | 4910ms |
| 30.0 | 40.0 | app2 | ok | 23 | 7500ms | 9500ms | 9950ms |
| 30.0 | 40.0 | end-users | ok | 152 | 3613ms | 4723ms | 4972ms |
| 40.0 | 50.0 | app1 | ok | 35 | 1829ms | 4028ms | 4903ms |
| 40.0 | 50.0 | app2 | ok | 18 | 7500ms | 9500ms | 9950ms |
| 40.0 | 50.0 | end-users | ok | 114 | 3617ms | 4723ms | 4972ms |
| 50.0 | 60.0 | app1 | ok | 57 | 1820ms | 3982ms | 4898ms |
| 50.0 | 60.0 | app2 | ok | 28 | 7500ms | 9500ms | 9950ms |
| 50.0 | 60.0 | end-users | ok | 181 | 3384ms | 4677ms | 4968ms |
| 60.0 | 71.0 | app1 | ok | 47 | 1925ms | 4021ms | 4902ms |
| 60.0 | 71.0 | app2 | ok | 24 | 7500ms | 9500ms | 9950ms |
| 60.0 | 71.0 | end-users | ok | 158 | 3558ms | 4712ms | 4971ms |
| 71.0 | 81.0 | app1 | ok | 36 | 1844ms | 4182ms | 4918ms |
| 71.0 | 81.0 | app2 | ok | 34 | 6190ms | 9429ms | 23200ms |
| 71.0 | 81.0 | end-users | ok | 137 | 2485ms | 4496ms | 4950ms |
| 81.0 | 91.0 | app1 | ok | 64 | 2385ms | 4467ms | 4947ms |
| 81.0 | 91.0 | app2 | ok | 16 | 7500ms | 9500ms | 9950ms |
| 81.0 | 91.0 | end-users | ok | 187 | 3174ms | 4635ms | 4963ms |
| 91.0 | 101.0 | app1 | ok | 42 | 1750ms | 4125ms | 4912ms |
| 91.0 | 101.0 | app2 | ok | 23 | 7500ms | 9500ms | 9950ms |
| 91.0 | 101.0 | end-users | ok | 150 | 3180ms | 4636ms | 4964ms |
| 101.0 | 111.0 | app1 | ok | 41 | 2011ms | 4212ms | 4921ms |
| 101.0 | 111.0 | app2 | ok | 19 | 7500ms | 9500ms | 9950ms |
| 101.0 | 111.0 | end-users | ok | 118 | 3495ms | 4699ms | 4970ms |
| 111.0 | 121.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 111.0 | 121.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 111.0 | 121.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 121.0 | 131.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 121.0 | 131.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 121.0 | 131.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 131.0 | 141.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 131.0 | 141.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 131.0 | 141.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 141.0 | 151.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 141.0 | 151.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 141.0 | 151.0 | end-users | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 32 | 542ms | 1540ms | 2404ms |
| 151.0 | 161.0 | app2 | ok | 17 | 550ms | 1863ms | 2436ms |
| 151.0 | 161.0 | end-users | ok | 103 | 616ms | 1985ms | 2448ms |
| 161.0 | 171.0 | app1 | ok | 51 | 583ms | 1912ms | 2441ms |
| 161.0 | 171.0 | app2 | ok | 25 | 562ms | 979ms | 2312ms |
| 161.0 | 171.0 | end-users | ok | 163 | 648ms | 1889ms | 2439ms |
| 171.0 | 181.0 | app1 | ok | 42 | 632ms | 1600ms | 2410ms |
| 171.0 | 181.0 | app2 | ok | 22 | 611ms | 1675ms | 2418ms |
| 171.0 | 181.0 | end-users | ok | 143 | 638ms | 1808ms | 2431ms |
| 181.0 | 191.0 | app1 | ok | 53 | 688ms | 1932ms | 2443ms |
| 181.0 | 191.0 | app2 | ok | 26 | 714ms | 1720ms | 2422ms |
| 181.0 | 191.0 | end-users | ok | 165 | 614ms | 1831ms | 2433ms |
| 191.0 | 201.0 | app1 | ok | 44 | 719ms | 1992ms | 2449ms |
| 191.0 | 201.0 | app2 | ok | 22 | 636ms | 1400ms | 2390ms |
| 191.0 | 201.0 | end-users | ok | 147 | 638ms | 1832ms | 2433ms |
| 201.0 | 211.0 | app1 | ok | 44 | 594ms | 1767ms | 2427ms |
| 201.0 | 211.0 | app2 | ok | 23 | 391ms | 1350ms | 2385ms |
| 201.0 | 211.0 | end-users | ok | 143 | 638ms | 1734ms | 2423ms |
| 211.0 | 221.0 | app1 | ok | 51 | 618ms | 1805ms | 2430ms |
| 211.0 | 221.0 | app2 | ok | 26 | 469ms | 1200ms | 2370ms |
| 211.0 | 221.0 | end-users | ok | 171 | 630ms | 1723ms | 2422ms |
| 221.0 | 231.0 | app1 | ok | 47 | 641ms | 1913ms | 2441ms |
| 221.0 | 231.0 | app2 | ok | 22 | 429ms | 925ms | 2170ms |
| 221.0 | 231.0 | end-users | ok | 145 | 654ms | 1841ms | 2434ms |
| 231.0 | 241.0 | app1 | ok | 50 | 553ms | 1562ms | 2406ms |
| 231.0 | 241.0 | app2 | ok | 25 | 705ms | 1875ms | 2438ms |
| 231.0 | 241.0 | end-users | ok | 164 | 617ms | 1755ms | 2425ms |
| 241.0 | 251.0 | app1 | ok | 44 | 594ms | 1767ms | 2427ms |
| 241.0 | 251.0 | app2 | ok | 22 | 625ms | 2088ms | 2459ms |
| 241.0 | 251.0 | end-users | ok | 145 | 688ms | 1879ms | 2438ms |
| 251.0 | 261.0 | app1 | ok | 51 | 566ms | 1650ms | 2415ms |
| 251.0 | 261.0 | app2 | ok | 25 | 729ms | 1875ms | 2438ms |
| 251.0 | 261.0 | end-users | ok | 162 | 597ms | 1716ms | 2422ms |
| 261.0 | 271.0 | app1 | ok | 43 | 631ms | 1425ms | 2392ms |
| 261.0 | 271.0 | app2 | ok | 22 | 750ms | 1950ms | 2445ms |
| 261.0 | 271.0 | end-users | ok | 148 | 652ms | 1866ms | 2437ms |
| 271.0 | 281.0 | app1 | ok | 53 | 685ms | 1838ms | 2434ms |
| 271.0 | 281.0 | app2 | ok | 26 | 625ms | 1525ms | 2402ms |
| 271.0 | 281.0 | end-users | ok | 164 | 640ms | 1900ms | 2440ms |
| 281.0 | 291.0 | app1 | ok | 44 | 625ms | 1840ms | 2434ms |
| 281.0 | 291.0 | app2 | ok | 22 | 667ms | 1840ms | 2434ms |
| 281.0 | 291.0 | end-users | ok | 143 | 612ms | 1734ms | 2423ms |
| 291.0 | 301.0 | app1 | ok | 51 | 583ms | 1912ms | 2441ms |
| 291.0 | 301.0 | app2 | ok | 25 | 596ms | 981ms | 2312ms |
| 291.0 | 301.0 | end-users | ok | 169 | 650ms | 1949ms | 2445ms |
| 301.0 | 312.0 | app1 | ok | 46 | 632ms | 1733ms | 2423ms |
| 301.0 | 312.0 | app2 | ok | 23 | 750ms | 2007ms | 2451ms |
| 301.0 | 312.0 | end-users | ok | 151 | 613ms | 1629ms | 2413ms |
| 312.0 | 322.0 | app1 | ok | 45 | 631ms | 1536ms | 2404ms |
| 312.0 | 322.0 | app2 | ok | 23 | 583ms | 1637ms | 2414ms |
| 312.0 | 322.0 | end-users | ok | 145 | 641ms | 1723ms | 2422ms |
| 322.0 | 332.0 | app1 | ok | 51 | 645ms | 1862ms | 2436ms |
| 322.0 | 332.0 | app2 | ok | 25 | 719ms | 2031ms | 2453ms |
| 322.0 | 332.0 | end-users | ok | 164 | 691ms | 1885ms | 2438ms |
| 332.0 | 342.0 | app1 | ok | 45 | 679ms | 1750ms | 2425ms |
| 332.0 | 342.0 | app2 | ok | 23 | 639ms | 1810ms | 2431ms |
| 332.0 | 342.0 | end-users | ok | 143 | 638ms | 1808ms | 2431ms |
| 342.0 | 352.0 | app1 | ok | 46 | 690ms | 1810ms | 2431ms |
| 342.0 | 352.0 | app2 | ok | 23 | 536ms | 1810ms | 2431ms |
| 342.0 | 352.0 | end-users | ok | 145 | 638ms | 1912ms | 2441ms |
| 352.0 | 362.0 | app1 | ok | 51 | 631ms | 1735ms | 2424ms |
| 352.0 | 362.0 | app2 | ok | 26 | 625ms | 1525ms | 2402ms |
| 352.0 | 362.0 | end-users | ok | 170 | 600ms | 1811ms | 2431ms |
| 362.0 | 372.0 | app1 | ok | 4 | 1000ms | 2200ms | 2470ms |
| 362.0 | 372.0 | app2 | ok | 2 | 500ms | 900ms | 990ms |
| 362.0 | 372.0 | end-users | ok | 18 | 833ms | 2050ms | 2455ms |
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
| 422.0 | 429.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 429.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 422.0 | 429.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens -42.9%, cost -45.8%
- app2 exceeded the 10% ledger tolerance: raw tokens -44.7%, cost -45.1%
- end-users exceeded the 10% ledger tolerance: raw tokens -41.7%, cost -42.9%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2126670 | 105894 | 1275618.0 | -42.9% | 1268478.0 | 2338458.0 | -45.8% | False |
| app2 | 1100850 | 55127 | 639366.0 | -44.7% | 664464.0 | 1211104.0 | -45.1% | False |
| end-users | 6768690 | 338000 | 4146661.0 | -41.7% | 4254420.0 | 7444690.0 | -42.9% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1738 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 915 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 5557 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=4694). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 4694 | 0.051ms | 0.105ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 259305 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 988 | 3604ms | 5708ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 495 | 4167ms | 5933ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3211 | 3656ms | 5682ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 4694 | 3707ms | 5720ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (43 windows, a metrics scrape failed mid-window at least once (UNI-230, not a restart)):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2357ms | 4517ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2000ms | 4500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2413ms | 4632ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 6643ms | 8850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 9250ms | 14438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 7354ms | 9921ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 6719ms | 8433ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 8303ms | 9851ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 6720ms | 9343ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 12738ms | 17125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 8278ms | 11100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 6788ms | 8800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 12609ms | 14957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 8433ms | 9862ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 6613ms | 8367ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 12609ms | 14957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 8203ms | 9957ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 71.0 | app1 | ok | 6806ms | 9060ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 71.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 71.0 | end-users | ok | 8074ms | 9807ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app1 | ok | 6500ms | 9286ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | app2 | ok | 12875ms | 18083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 71.0 | 81.0 | end-users | ok | 8295ms | 9991ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app1 | ok | 6886ms | 8500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | app2 | ok | 13500ms | 19125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 81.0 | 91.0 | end-users | ok | 8231ms | 13131ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app1 | ok | 7000ms | 9438ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | app2 | ok | 13472ms | 19156ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 91.0 | 101.0 | end-users | ok | 8027ms | 9876ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app1 | ok | 6500ms | 9200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 101.0 | 111.0 | end-users | ok | 8247ms | 12214ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 2577ms | 3808ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 2900ms | 4450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 2596ms | 3760ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 2703ms | 3832ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 3433ms | 4617ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 2830ms | 3875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 2920ms | 3935ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 3438ms | 4600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 2868ms | 3883ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 2828ms | 3976ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 3500ms | 4712ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 3039ms | 3927ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 2788ms | 3869ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 3792ms | 4872ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 3006ms | 3901ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 2870ms | 3882ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 3735ms | 4844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 3007ms | 3901ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 2800ms | 3867ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 3676ms | 4808ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 2994ms | 3899ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 2796ms | 3869ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 3719ms | 4844ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 3100ms | 3910ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 2846ms | 3880ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 3750ms | 4872ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 3073ms | 3918ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 2808ms | 3922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 3692ms | 4850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 3032ms | 3937ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 2788ms | 3921ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 3682ms | 4856ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 3133ms | 3993ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | ok | 3239ms | 4608ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | ok | 3731ms | 4861ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | ok | 3066ms | 3966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | ok | 3719ms | 4996ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | ok | 4438ms | 6100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | end-users | ok | 3885ms | 5057ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | ok | 4692ms | 5971ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | ok | 5100ms | 7200ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | end-users | ok | 4681ms | 5865ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | ok | 4818ms | 5879ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | ok | 4955ms | 6850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | end-users | ok | 4683ms | 5849ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 312.0 | app1 | ok | 4673ms | 5843ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 312.0 | app2 | ok | 5038ms | 5904ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 312.0 | end-users | ok | 4693ms | 5845ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | app1 | ok | 4719ms | 5840ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | app2 | ok | 4955ms | 5895ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 312.0 | 322.0 | end-users | ok | 4755ms | 5857ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app1 | ok | 4788ms | 5869ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | app2 | ok | 4846ms | 5880ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 322.0 | 332.0 | end-users | ok | 4704ms | 5835ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app1 | ok | 4685ms | 5847ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | app2 | ok | 5091ms | 5991ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 332.0 | 342.0 | end-users | ok | 4633ms | 5876ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app1 | ok | 4679ms | 5836ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | app2 | ok | 4944ms | 7167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 342.0 | 352.0 | end-users | ok | 4690ms | 5846ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app1 | ok | 4789ms | 6400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | app2 | ok | 4900ms | 7600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 352.0 | 362.0 | end-users | ok | 4825ms | 6300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app1 | ok | 5208ms | 7167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | app2 | ok | 5000ms | 7533ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 362.0 | 372.0 | end-users | ok | 4828ms | 7033ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
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
| 422.0 | 429.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 429.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 422.0 | 429.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
