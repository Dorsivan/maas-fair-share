# Fairness benchmark: app1-flood-moderate (uni310-l3-r1-uni161-app1-flood-128)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 31.4 points

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-flood-moderate` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-6bdbdf5bf6-b4gnb` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T03:16:08Z` |
| Run end | `2026-11-26T03:24:42Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 53 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/53 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 77.00 | 2.4062 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 30.0 | 128 | 1752 | 000=1, 200=1751 | 18.5 | 21.6 | 2285908.0 | 30.0% | 57.1% | 27.1 | 31.6% | 1.6 | 32.2% | 2.2 | 79.3s | 98.9% | 1752.0 |
| app2 | 10.0 | 32 | 574 | 200=574 | 13.9 | 17.4 | 761358.0 | 10.0% | 14.3% | 4.3 | 10.5% | 0.5 | 10.5% | 0.5 | 79.3s | 98.9% | 574.0 |
| end-users | 60.0 | 64 | 3121 | 200=3121 | 4.8 | 7.4 | 4178134.0 | 60.0% | 28.6% | -31.4 | 57.8% | -2.2 | 57.3% | -2.7 | 77.1s | 98.9% | 3121.0 |
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
| 0.0 | 10.0 | 10.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (52 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 0.0 | 30.0% | 0.0% | -30.0 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 10.0% | 0.0% | -10.0 |
| 0.0 | 10.0 | end-users | True | False | 44598.0 | 60.0% | 100.0% | 40.0 |
| 10.0 | 20.0 | app1 | True | False | 63536.0 | 30.0% | 24.5% | -5.5 |
| 10.0 | 20.0 | app2 | True | False | 36558.0 | 10.0% | 14.1% | 4.1 |
| 10.0 | 20.0 | end-users | True | False | 159670.0 | 60.0% | 61.5% | 1.5 |
| 20.0 | 30.0 | app1 | True | False | 98688.0 | 30.0% | 32.3% | 2.3 |
| 20.0 | 30.0 | app2 | True | False | 31070.0 | 10.0% | 10.2% | 0.2 |
| 20.0 | 30.0 | end-users | True | False | 175816.0 | 60.0% | 57.5% | -2.5 |
| 30.0 | 40.0 | app1 | True | False | 94704.0 | 30.0% | 31.0% | 1.0 |
| 30.0 | 40.0 | app2 | True | False | 31148.0 | 10.0% | 10.2% | 0.2 |
| 30.0 | 40.0 | end-users | True | False | 179898.0 | 60.0% | 58.8% | -1.2 |
| 40.0 | 50.0 | app1 | True | False | 86660.0 | 30.0% | 28.4% | -1.6 |
| 40.0 | 50.0 | app2 | True | False | 29698.0 | 10.0% | 9.7% | -0.3 |
| 40.0 | 50.0 | end-users | True | False | 189310.0 | 60.0% | 61.9% | 1.9 |
| 50.0 | 60.0 | app1 | True | False | 102792.0 | 30.0% | 33.5% | 3.5 |
| 50.0 | 60.0 | app2 | True | False | 33796.0 | 10.0% | 11.0% | 1.0 |
| 50.0 | 60.0 | end-users | True | False | 170390.0 | 60.0% | 55.5% | -4.5 |
| 60.0 | 70.0 | app1 | True | False | 85252.0 | 30.0% | 27.9% | -2.1 |
| 60.0 | 70.0 | app2 | True | False | 26988.0 | 10.0% | 8.8% | -1.2 |
| 60.0 | 70.0 | end-users | True | False | 193524.0 | 60.0% | 63.3% | 3.3 |
| 70.0 | 80.0 | app1 | True | False | 87884.0 | 30.0% | 28.9% | -1.1 |
| 70.0 | 80.0 | app2 | True | False | 31108.0 | 10.0% | 10.2% | 0.2 |
| 70.0 | 80.0 | end-users | True | False | 185372.0 | 60.0% | 60.9% | 0.9 |
| 80.0 | 90.0 | app1 | True | False | 94692.0 | 30.0% | 32.1% | 2.1 |
| 80.0 | 90.0 | app2 | True | False | 31106.0 | 10.0% | 10.6% | 0.6 |
| 80.0 | 90.0 | end-users | True | False | 168974.0 | 60.0% | 57.3% | -2.7 |
| 90.0 | 100.0 | app1 | True | False | 111114.0 | 30.0% | 36.7% | 6.7 |
| 90.0 | 100.0 | app2 | True | False | 37792.0 | 10.0% | 12.5% | 2.5 |
| 90.0 | 100.0 | end-users | True | False | 154216.0 | 60.0% | 50.9% | -9.1 |
| 100.0 | 110.0 | app1 | True | False | 79768.0 | 30.0% | 26.1% | -3.9 |
| 100.0 | 110.0 | app2 | True | False | 25724.0 | 10.0% | 8.4% | -1.6 |
| 100.0 | 110.0 | end-users | True | False | 200090.0 | 60.0% | 65.5% | 5.5 |
| 110.0 | 120.0 | app1 | True | False | 91926.0 | 30.0% | 30.0% | -0.0 |
| 110.0 | 120.0 | app2 | True | False | 31114.0 | 10.0% | 10.1% | 0.1 |
| 110.0 | 120.0 | end-users | True | False | 183658.0 | 60.0% | 59.9% | -0.1 |
| 120.0 | 130.0 | app1 | True | False | 96062.0 | 30.0% | 31.8% | 1.8 |
| 120.0 | 130.0 | app2 | True | False | 31118.0 | 10.0% | 10.3% | 0.3 |
| 120.0 | 130.0 | end-users | True | False | 174650.0 | 60.0% | 57.9% | -2.1 |
| 130.0 | 140.0 | app1 | True | False | 104130.0 | 30.0% | 33.9% | 3.9 |
| 130.0 | 140.0 | app2 | True | False | 33784.0 | 10.0% | 11.0% | 1.0 |
| 130.0 | 140.0 | end-users | True | False | 169102.0 | 60.0% | 55.1% | -4.9 |
| 140.0 | 150.0 | app1 | True | False | 101478.0 | 30.0% | 33.6% | 3.6 |
| 140.0 | 150.0 | app2 | True | False | 36550.0 | 10.0% | 12.1% | 2.1 |
| 140.0 | 150.0 | end-users | True | False | 163788.0 | 60.0% | 54.3% | -5.7 |
| 150.0 | 160.0 | app1 | True | False | 101356.0 | 30.0% | 36.5% | 6.5 |
| 150.0 | 160.0 | app2 | True | False | 31148.0 | 10.0% | 11.2% | 1.2 |
| 150.0 | 160.0 | end-users | True | False | 144860.0 | 60.0% | 52.2% | -7.8 |
| 160.0 | 170.0 | app1 | True | False | 100100.0 | 30.0% | 33.2% | 3.2 |
| 160.0 | 170.0 | app2 | True | False | 33812.0 | 10.0% | 11.2% | 1.2 |
| 160.0 | 170.0 | end-users | True | False | 167732.0 | 60.0% | 55.6% | -4.4 |
| 170.0 | 180.0 | app1 | True | False | 90486.0 | 30.0% | 29.4% | -0.6 |
| 170.0 | 180.0 | app2 | True | False | 32430.0 | 10.0% | 10.5% | 0.5 |
| 170.0 | 180.0 | end-users | True | False | 185342.0 | 60.0% | 60.1% | 0.1 |
| 180.0 | 190.0 | app1 | True | False | 89176.0 | 30.0% | 28.9% | -1.1 |
| 180.0 | 190.0 | app2 | True | False | 28464.0 | 10.0% | 9.2% | -0.8 |
| 180.0 | 190.0 | end-users | True | False | 190706.0 | 60.0% | 61.8% | 1.8 |
| 190.0 | 200.0 | app1 | True | False | 94662.0 | 30.0% | 31.1% | 1.1 |
| 190.0 | 200.0 | app2 | True | False | 31104.0 | 10.0% | 10.2% | 0.2 |
| 190.0 | 200.0 | end-users | True | False | 178458.0 | 60.0% | 58.7% | -1.3 |
| 200.0 | 210.0 | app1 | True | False | 78474.0 | 30.0% | 25.7% | -4.3 |
| 200.0 | 210.0 | app2 | True | False | 27008.0 | 10.0% | 8.8% | -1.2 |
| 200.0 | 210.0 | end-users | True | False | 200142.0 | 60.0% | 65.5% | 5.5 |
| 210.0 | 220.0 | app1 | True | False | 92042.0 | 30.0% | 30.1% | 0.1 |
| 210.0 | 220.0 | app2 | True | False | 29790.0 | 10.0% | 9.7% | -0.3 |
| 210.0 | 220.0 | end-users | True | False | 183950.0 | 60.0% | 60.2% | 0.2 |
| 220.0 | 230.0 | app1 | True | False | 92106.0 | 30.0% | 30.3% | 0.3 |
| 220.0 | 230.0 | app2 | True | False | 31112.0 | 10.0% | 10.2% | 0.2 |
| 220.0 | 230.0 | end-users | True | False | 181188.0 | 60.0% | 59.5% | -0.5 |
| 230.0 | 240.0 | app1 | True | False | 74418.0 | 30.0% | 31.4% | 1.4 |
| 230.0 | 240.0 | app2 | True | False | 24236.0 | 10.0% | 10.2% | 0.2 |
| 230.0 | 240.0 | end-users | True | False | 137986.0 | 60.0% | 58.3% | -1.7 |
| 240.0 | 251.0 | app1 | False | n/a | 81146.0 | n/a | n/a | n/a |
| 240.0 | 251.0 | app2 | False | n/a | 28456.0 | n/a | n/a | n/a |
| 240.0 | 251.0 | end-users | False | n/a | 82536.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 93256.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 16244.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | n/a | 12178.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 411.0 | 421.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 421.0 | 431.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 431.0 | 441.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 441.0 | 451.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 451.0 | 461.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 461.0 | 471.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 471.0 | 481.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 481.0 | 491.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 491.0 | 502.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 491.0 | 502.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 491.0 | 502.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 502.0 | 512.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 514.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 514.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 512.0 | 514.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 111 | 0ms | 889ms | 989ms |
| 0.0 | 10.0 | app2 | ok | 35 | 562ms | 912ms | 991ms |
| 0.0 | 10.0 | end-users | ok | 73 | 348ms | 870ms | 987ms |
| 10.0 | 20.0 | app1 | ok | 49 | 7988ms | 17750ms | 28775ms |
| 10.0 | 20.0 | app2 | ok | 19 | 5250ms | 9050ms | 9905ms |
| 10.0 | 20.0 | end-users | ok | 144 | 2173ms | 6000ms | 9600ms |
| 20.0 | 30.0 | app1 | ok | 77 | 19000ms | 27800ms | 29780ms |
| 20.0 | 30.0 | app2 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 20.0 | 30.0 | end-users | ok | 147 | 1216ms | 2424ms | 4666ms |
| 30.0 | 40.0 | app1 | ok | 65 | 20000ms | 28000ms | 29800ms |
| 30.0 | 40.0 | app2 | ok | 22 | 7500ms | 9500ms | 9950ms |
| 30.0 | 40.0 | end-users | ok | 140 | 1229ms | 2396ms | 4611ms |
| 40.0 | 50.0 | app1 | ok | 63 | 18333ms | 27667ms | 29767ms |
| 40.0 | 50.0 | app2 | ok | 21 | 7375ms | 9475ms | 9948ms |
| 40.0 | 50.0 | end-users | ok | 105 | 1184ms | 2373ms | 4563ms |
| 50.0 | 60.0 | app1 | ok | 73 | 19861ms | 27972ms | 29797ms |
| 50.0 | 60.0 | app2 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 50.0 | 60.0 | end-users | ok | 153 | 1430ms | 2386ms | 4522ms |
| 60.0 | 70.0 | app1 | ok | 76 | 19589ms | 27918ms | 29792ms |
| 60.0 | 70.0 | app2 | ok | 25 | 7283ms | 9457ms | 9946ms |
| 60.0 | 70.0 | end-users | ok | 139 | 1170ms | 2434ms | 4684ms |
| 70.0 | 80.0 | app1 | ok | 47 | 19318ms | 27864ms | 29786ms |
| 70.0 | 80.0 | app2 | ok | 17 | 7167ms | 9433ms | 9943ms |
| 70.0 | 80.0 | end-users | ok | 127 | 1475ms | 2883ms | 4788ms |
| 80.0 | 90.0 | app1 | ok | 127 | 14699ms | 26940ms | 29694ms |
| 80.0 | 90.0 | app2 | ok | 40 | 6042ms | 9375ms | 22000ms |
| 80.0 | 90.0 | end-users | ok | 146 | 1360ms | 2719ms | 4772ms |
| 90.0 | 100.0 | app1 | ok | 33 | 8056ms | 19000ms | 28900ms |
| 90.0 | 100.0 | app2 | ok | 12 | 3438ms | 4938ms | 9400ms |
| 90.0 | 100.0 | end-users | ok | 95 | 2909ms | 4736ms | 8812ms |
| 100.0 | 110.0 | app1 | ok | 65 | 14884ms | 26977ms | 29698ms |
| 100.0 | 110.0 | app2 | ok | 22 | 7750ms | 9950ms | 27800ms |
| 100.0 | 110.0 | end-users | ok | 171 | 1383ms | 2452ms | 4695ms |
| 110.0 | 120.0 | app1 | ok | 57 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app2 | ok | 19 | 7500ms | 9500ms | 9950ms |
| 110.0 | 120.0 | end-users | ok | 112 | 1344ms | 2446ms | 4689ms |
| 120.0 | 130.0 | app1 | ok | 64 | 16939ms | 27388ms | 29739ms |
| 120.0 | 130.0 | app2 | ok | 20 | 6154ms | 9231ms | 9923ms |
| 120.0 | 130.0 | end-users | ok | 119 | 1361ms | 3513ms | 4851ms |
| 130.0 | 140.0 | app1 | ok | 70 | 18525ms | 27705ms | 29770ms |
| 130.0 | 140.0 | app2 | ok | 24 | 7391ms | 9478ms | 9948ms |
| 130.0 | 140.0 | end-users | ok | 151 | 1534ms | 3427ms | 4843ms |
| 140.0 | 150.0 | app1 | ok | 97 | 9755ms | 25783ms | 29578ms |
| 140.0 | 150.0 | app2 | ok | 33 | 5875ms | 9175ms | 9918ms |
| 140.0 | 150.0 | end-users | ok | 99 | 1783ms | 4116ms | 4912ms |
| 150.0 | 160.0 | app1 | ok | 56 | 7895ms | 20667ms | 29067ms |
| 150.0 | 160.0 | app2 | ok | 16 | 4286ms | 8667ms | 9867ms |
| 150.0 | 160.0 | end-users | ok | 116 | 2863ms | 4734ms | 8840ms |
| 160.0 | 170.0 | app1 | ok | 107 | 9385ms | 25348ms | 29535ms |
| 160.0 | 170.0 | app2 | ok | 38 | 5682ms | 9136ms | 9914ms |
| 160.0 | 170.0 | end-users | ok | 147 | 1627ms | 3815ms | 4881ms |
| 170.0 | 180.0 | app1 | ok | 62 | 10625ms | 26125ms | 29612ms |
| 170.0 | 180.0 | app2 | ok | 20 | 7222ms | 9444ms | 9944ms |
| 170.0 | 180.0 | end-users | ok | 123 | 1238ms | 2468ms | 4720ms |
| 180.0 | 190.0 | app1 | ok | 54 | 18261ms | 27652ms | 29765ms |
| 180.0 | 190.0 | app2 | ok | 18 | 7500ms | 9500ms | 9950ms |
| 180.0 | 190.0 | end-users | ok | 133 | 1574ms | 3769ms | 4877ms |
| 190.0 | 200.0 | app1 | ok | 68 | 20000ms | 28000ms | 29800ms |
| 190.0 | 200.0 | app2 | ok | 23 | 7614ms | 9705ms | 25400ms |
| 190.0 | 200.0 | end-users | ok | 153 | 1371ms | 2426ms | 4652ms |
| 200.0 | 210.0 | app1 | ok | 53 | 19808ms | 27962ms | 29796ms |
| 200.0 | 210.0 | app2 | ok | 19 | 7500ms | 9500ms | 9950ms |
| 200.0 | 210.0 | end-users | ok | 119 | 1176ms | 2291ms | 4008ms |
| 210.0 | 220.0 | app1 | ok | 70 | 19394ms | 27879ms | 29788ms |
| 210.0 | 220.0 | app2 | ok | 22 | 7105ms | 9421ms | 9942ms |
| 210.0 | 220.0 | end-users | ok | 151 | 1222ms | 2498ms | 4748ms |
| 220.0 | 230.0 | app1 | ok | 76 | 20000ms | 28000ms | 29800ms |
| 220.0 | 230.0 | app2 | ok | 25 | 7500ms | 9500ms | 9950ms |
| 220.0 | 230.0 | end-users | ok | 147 | 1320ms | 2396ms | 4592ms |
| 230.0 | 240.0 | app1 | ok | 89 | 9632ms | 25762ms | 29576ms |
| 230.0 | 240.0 | app2 | ok | 30 | 5385ms | 10000ms | 28000ms |
| 230.0 | 240.0 | end-users | ok | 70 | 1545ms | 3750ms | 4875ms |
| 240.0 | 251.0 | app1 | ok | 43 | 16970ms | 27394ms | 29739ms |
| 240.0 | 251.0 | app2 | ok | 4 | 8333ms | 22000ms | 29200ms |
| 240.0 | 251.0 | end-users | ok | 41 | 7929ms | 16333ms | 28633ms |
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
| 321.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 401.0 | 411.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 411.0 | 421.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 421.0 | 431.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 431.0 | 441.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 441.0 | 451.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 451.0 | 461.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 461.0 | 471.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 471.0 | 481.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 481.0 | 491.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 502.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 502.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 491.0 | 502.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 502.0 | 512.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 514.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 514.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 512.0 | 514.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2153730 | 107383 | 2261113.0 | 0.0% | 2285908.0 | 2368496.0 | -3.5% | True |
| app2 | 706020 | 35075 | 741095.0 | 0.0% | 761358.0 | 776170.0 | -1.9% | True |
| end-users | 3838830 | 191274 | 4030104.0 | 0.0% | 4178134.0 | 4221378.0 | -1.0% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1752 | 0 | 0 | 0 (never shed) | 0.00% | 30.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 574 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3121 | 0 | 0 | 0 (never shed) | 0.00% | 60.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5447). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5447 | 0.051ms | 0.144ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 486427 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1751 | 17923ms | 27534ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 574 | 13102ms | 18905ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3121 | 4738ms | 7644ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5446 | 6100ms | 22330ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (52 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 3423ms | 5558ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2333ms | 3833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 2176ms | 4483ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 9944ms | 14491ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 8400ms | 14300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 6141ms | 7814ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 12614ms | 14966ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 4740ms | 5856ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 17536ms | 19819ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 4593ms | 5825ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 17623ms | 19984ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 12750ms | 17250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 4701ms | 5851ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 18065ms | 27286ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 13289ms | 18958ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 4540ms | 7259ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 17864ms | 26062ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 12778ms | 17500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 4798ms | 5885ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 18125ms | 27500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 13194ms | 18850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 4575ms | 6858ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 17823ms | 25625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 13026ms | 18562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 4632ms | 5855ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 18154ms | 27588ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 13043ms | 18600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 5750ms | 7791ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 17634ms | 20167ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 12361ms | 14736ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | end-users | ok | 4075ms | 7720ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 21905ms | 29190ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 14792ms | 19477ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | end-users | ok | 4684ms | 5879ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 17731ms | 24083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 12738ms | 17125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | end-users | ok | 4786ms | 5944ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 18008ms | 27038ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 14167ms | 19375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | end-users | ok | 4304ms | 7306ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 17463ms | 19945ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | end-users | ok | 5490ms | 8487ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | end-users | ok | 5791ms | 7730ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 16471ms | 19735ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 12396ms | 14740ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | end-users | ok | 5217ms | 7718ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app1 | ok | 18138ms | 27906ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | app2 | ok | 13333ms | 19143ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 180.0 | end-users | ok | 4967ms | 7751ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app1 | ok | 18235ms | 27800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | app2 | ok | 13088ms | 18688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 180.0 | 190.0 | end-users | ok | 4461ms | 5997ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app1 | ok | 20278ms | 29028ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | app2 | ok | 15893ms | 19589ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 190.0 | 200.0 | end-users | ok | 4414ms | 6680ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app1 | ok | 19531ms | 28885ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | app2 | ok | 15000ms | 19500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 200.0 | 210.0 | end-users | ok | 4480ms | 5993ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 220.0 | app1 | ok | 17742ms | 24333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 220.0 | app2 | ok | 13438ms | 19083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 210.0 | 220.0 | end-users | ok | 4645ms | 5877ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 220.0 | 230.0 | app1 | ok | 18148ms | 27571ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 220.0 | 230.0 | app2 | ok | 12875ms | 18083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 220.0 | 230.0 | end-users | ok | 4607ms | 5851ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 230.0 | 240.0 | app1 | ok | 21406ms | 29141ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 230.0 | 240.0 | app2 | ok | 15500ms | 19550ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 230.0 | 240.0 | end-users | ok | 5444ms | 7717ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 240.0 | 251.0 | app1 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 240.0 | 251.0 | app2 | ok | 17500ms | 19750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 240.0 | 251.0 | end-users | ok | 10234ms | 14523ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 18207ms | 28083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 16250ms | 19625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | ok | 10500ms | 14550ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 361.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 361.0 | 371.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 371.0 | 381.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 381.0 | 391.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 391.0 | 401.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 401.0 | 411.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 411.0 | 421.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 431.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 431.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 421.0 | 431.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 431.0 | 441.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 431.0 | 441.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 431.0 | 441.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 441.0 | 451.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 441.0 | 451.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 441.0 | 451.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 451.0 | 461.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 451.0 | 461.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 451.0 | 461.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 461.0 | 471.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 461.0 | 471.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 461.0 | 471.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 471.0 | 481.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 471.0 | 481.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 471.0 | 481.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 481.0 | 491.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 481.0 | 491.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 481.0 | 491.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 491.0 | 502.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 491.0 | 502.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 491.0 | 502.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 502.0 | 512.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 514.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 514.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 512.0 | 514.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
