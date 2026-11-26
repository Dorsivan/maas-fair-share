# Fairness benchmark: below-capacity (uni310-l2-r1-a6-below-capacity)

**Verdict: UNCONTENDED** -- every offered group's `contended_seconds_total` delta stayed under 1s, so the pool was never actually contended. Not scored against the 10-point weighted-split threshold; see docs/runbook.md.
Worker-share vs. weight-share gap (UNI-225): 5.3 points

- every offered group's contended_seconds_total delta stayed under 1s (app1=never contended, app2=never contended, end-users=never contended) -- an order of magnitude below the ~9s a genuinely-contending tenant accrues in a 240s full-contention run (docs/runbook.md), so nobody was ever backlogged alongside anyone else and the weighted-split deviation check does not apply

## Run metadata

| field | value |
|---|---|
| Scenario | `below-capacity` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-8448f688f-fj9qw` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T04:43:52Z` |
| Run end | `2026-11-26T04:48:10Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 27 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/27 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 11.00 | 0.3438 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 6 | 1135 | 200=1135 | 1.2 | 1.4 | n/a | 21.1% | 15.8% | -5.3 | 0.0% | -21.1 | 21.0% | -0.0 | n/a | 98.9% | 1135.0 |
| app2 | 10.0 | 6 | 570 | 200=570 | 2.5 | 2.8 | n/a | 10.5% | 15.8% | 5.3 | 0.0% | -10.5 | 10.6% | 0.0 | n/a | 98.9% | 570.0 |
| end-users | 65.0 | 26 | 3690 | 200=3690 | 1.6 | 2.0 | n/a | 68.4% | 68.4% | 0.0 | 0.0% | -68.4 | 68.4% | -0.0 | n/a | 98.9% | 3690.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

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
| 0.0 | 0.0 (uncontended -- no group delivered contended tokens from here on, nothing was being arbitrated) | 0.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (26 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 0.0 | 10.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 0.0 | 10.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 10.0 | 20.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 10.0 | 20.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 10.0 | 20.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 20.0 | 30.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 20.0 | 30.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 20.0 | 30.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 30.0 | 40.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 30.0 | 40.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 30.0 | 40.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 40.0 | 50.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 40.0 | 50.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 40.0 | 50.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 50.0 | 60.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 50.0 | 60.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 50.0 | 60.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 60.0 | 70.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 60.0 | 70.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 60.0 | 70.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 70.0 | 80.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 70.0 | 80.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 70.0 | 80.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 80.0 | 90.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 80.0 | 90.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 80.0 | 90.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 90.0 | 100.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 90.0 | 100.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 90.0 | 100.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 100.0 | 110.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 100.0 | 110.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 100.0 | 110.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 110.0 | 120.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 110.0 | 120.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 110.0 | 120.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 120.0 | 130.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 120.0 | 130.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 120.0 | 130.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 130.0 | 140.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 130.0 | 140.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 130.0 | 140.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 140.0 | 151.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 140.0 | 151.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 140.0 | 151.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 151.0 | 161.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 151.0 | 161.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 151.0 | 161.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 161.0 | 171.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 161.0 | 171.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 161.0 | 171.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 171.0 | 181.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 171.0 | 181.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 171.0 | 181.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 181.0 | 191.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 181.0 | 191.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 181.0 | 191.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 191.0 | 201.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 191.0 | 201.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 191.0 | 201.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 201.0 | 211.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 201.0 | 211.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 201.0 | 211.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 211.0 | 221.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 211.0 | 221.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 211.0 | 221.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 221.0 | 231.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 221.0 | 231.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 221.0 | 231.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 231.0 | 241.0 | app1 | True | True | 0.0 | 21.1% | n/a | n/a |
| 231.0 | 241.0 | app2 | True | True | 0.0 | 10.5% | n/a | n/a |
| 231.0 | 241.0 | end-users | True | True | 0.0 | 68.4% | n/a | n/a |
| 241.0 | 251.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 258.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 35 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 21 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 118 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 48 | 0ms | 0ms | 1ms |
| 10.0 | 20.0 | app2 | ok | 23 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | end-users | ok | 154 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app1 | ok | 48 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 20.0 | 30.0 | end-users | ok | 156 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 30.0 | 40.0 | end-users | ok | 156 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | app1 | ok | 47 | 0ms | 0ms | 1ms |
| 40.0 | 50.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 40.0 | 50.0 | end-users | ok | 154 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app1 | ok | 49 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 50.0 | 60.0 | end-users | ok | 156 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | app2 | ok | 23 | 0ms | 0ms | 0ms |
| 60.0 | 70.0 | end-users | ok | 153 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 70.0 | 80.0 | end-users | ok | 154 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | app2 | ok | 23 | 0ms | 0ms | 0ms |
| 80.0 | 90.0 | end-users | ok | 152 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | app1 | ok | 48 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 90.0 | 100.0 | end-users | ok | 157 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 100.0 | 110.0 | end-users | ok | 154 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 110.0 | 120.0 | end-users | ok | 155 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | app1 | ok | 49 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | app2 | ok | 23 | 0ms | 0ms | 0ms |
| 120.0 | 130.0 | end-users | ok | 153 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | app1 | ok | 46 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 130.0 | 140.0 | end-users | ok | 154 | 0ms | 0ms | 0ms |
| 140.0 | 151.0 | app1 | ok | 48 | 0ms | 0ms | 0ms |
| 140.0 | 151.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 140.0 | 151.0 | end-users | ok | 153 | 0ms | 0ms | 0ms |
| 151.0 | 161.0 | app1 | ok | 48 | 0ms | 0ms | 0ms |
| 151.0 | 161.0 | app2 | ok | 23 | 0ms | 0ms | 0ms |
| 151.0 | 161.0 | end-users | ok | 157 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | app2 | ok | 25 | 0ms | 0ms | 0ms |
| 161.0 | 171.0 | end-users | ok | 154 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | app1 | ok | 48 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | app2 | ok | 23 | 0ms | 0ms | 0ms |
| 171.0 | 181.0 | end-users | ok | 155 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | app2 | ok | 23 | 0ms | 0ms | 0ms |
| 181.0 | 191.0 | end-users | ok | 151 | 0ms | 0ms | 0ms |
| 191.0 | 201.0 | app1 | ok | 46 | 0ms | 0ms | 0ms |
| 191.0 | 201.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 191.0 | 201.0 | end-users | ok | 152 | 0ms | 0ms | 0ms |
| 201.0 | 211.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 201.0 | 211.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 201.0 | 211.0 | end-users | ok | 157 | 0ms | 0ms | 0ms |
| 211.0 | 221.0 | app1 | ok | 50 | 0ms | 0ms | 0ms |
| 211.0 | 221.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 211.0 | 221.0 | end-users | ok | 153 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | app1 | ok | 46 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 221.0 | 231.0 | end-users | ok | 154 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | app1 | ok | 47 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | app2 | ok | 23 | 0ms | 0ms | 0ms |
| 231.0 | 241.0 | end-users | ok | 155 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | app1 | ok | 9 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | app2 | ok | 4 | 0ms | 0ms | 0ms |
| 241.0 | 251.0 | end-users | ok | 23 | 0ms | 0ms | 0ms |
| 251.0 | 258.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 258.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost n/a
- app2 exceeded the 10% ledger tolerance: cost n/a
- end-users exceeded the 10% ledger tolerance: cost n/a

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1396050 | 69532 | 1465582.0 | 0.0% | n/a | 1535114.0 | n/a | False |
| app2 | 701100 | 35009 | 736109.0 | 0.0% | n/a | 771118.0 | n/a | False |
| end-users | 4538700 | 226206 | 4764906.0 | 0.0% | n/a | 4991112.0 | n/a | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1135 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 570 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3690 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5395). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5395 | 0.051ms | 0.153ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 245462 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1135 | 1206ms | 1479ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 570 | 2494ms | 2953ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3690 | 1658ms | 1975ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5395 | 1605ms | 2570ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (26 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 1146ms | 2275ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2389ms | 3625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 1564ms | 2922ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 1188ms | 1493ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 1615ms | 1966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 1181ms | 1467ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 1665ms | 1967ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 1194ms | 1470ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 1674ms | 1975ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 1237ms | 1474ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 1658ms | 1970ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 1197ms | 1470ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 1619ms | 1971ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 1230ms | 1473ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 1658ms | 1978ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 1255ms | 1485ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 1688ms | 1969ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 1265ms | 1476ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 2477ms | 2948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 1659ms | 1983ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 1208ms | 1483ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 1602ms | 1960ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 1178ms | 1494ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 1651ms | 1965ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 1297ms | 1480ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 1664ms | 1970ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 1203ms | 1469ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 1696ms | 1970ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 1210ms | 1471ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 1676ms | 1968ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 151.0 | app1 | ok | 1213ms | 1495ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 151.0 | app2 | ok | 2477ms | 2948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 151.0 | end-users | ok | 1642ms | 1973ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 1180ms | 1478ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 1672ms | 1975ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 1182ms | 1465ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 2479ms | 2948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 1686ms | 1980ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 1269ms | 1477ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 1613ms | 1980ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 1232ms | 1496ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 1671ms | 2235ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 1188ms | 1465ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 1677ms | 1968ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 1220ms | 1483ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 1654ms | 1969ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 1158ms | 1492ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 1655ms | 1974ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 1167ms | 1477ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 1669ms | 1983ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 1196ms | 1469ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 2500ms | 2950ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 1651ms | 1969ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 1181ms | 1462ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 2375ms | 2938ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 1676ms | 1968ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 258.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
