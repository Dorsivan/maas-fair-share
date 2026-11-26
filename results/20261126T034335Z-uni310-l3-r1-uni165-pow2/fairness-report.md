# Fairness benchmark: six-group-board-case (uni310-l3-r1-uni165-pow2)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 24.2 points

## Run metadata

| field | value |
|---|---|
| Scenario | `six-group-board-case` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-6b84c87f55-k7dh2` |
| Namespace | `poc-maas-lane3` |
| Run start | `2026-11-26T03:44:57Z` |
| Run end | `2026-11-26T03:50:51Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 37 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/37 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 86.50 | 2.7031 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 32.0 | 58 | 2463 | 000=1, 200=2462 | 5.3 | 8.3 | 3293264.0 | 50.8% | 26.6% | -24.2 | 45.9% | -4.9 | 45.4% | -5.4 | 70.9s | 98.9% | 2463.0 |
| app2 | 16.0 | 32 | 1271 | 200=1271 | 5.8 | 8.8 | 1692212.0 | 25.4% | 14.7% | -10.7 | 23.6% | -1.8 | 23.4% | -2.0 | 71.0s | 98.9% | 1271.0 |
| app3 | 8.0 | 32 | 781 | 200=781 | 10.0 | 13.5 | 1032216.0 | 12.7% | 14.7% | 2.0 | 14.4% | 1.7 | 14.4% | 1.7 | 70.6s | 98.9% | 781.0 |
| app4 | 4.0 | 32 | 466 | 200=466 | 15.3 | 30.2 | 618106.0 | 6.3% | 14.7% | 8.3 | 8.6% | 2.3 | 8.6% | 2.2 | 73.1s | 98.9% | 466.0 |
| app5 | 2.0 | 32 | 275 | 200=275 | 25.4 | 56.5 | 344712.0 | 3.2% | 14.7% | 11.5 | 4.8% | 1.6 | 5.1% | 1.9 | 73.3s | 98.9% | 275.0 |
| app6 | 1.0 | 32 | 166 | 200=166 | 53.3 | 83.0 | 196106.0 | 1.6% | 14.7% | 13.1 | 2.7% | 1.1 | 3.1% | 1.5 | 73.3s | 98.9% | 166.0 |
| end-users | n/a | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- app3: active 0s-240s, no duty cycle
- app4: active 0s-240s, no duty cycle
- app5: active 0s-240s, no duty cycle
- app6: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 160.0 | 160.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (36 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 39158.0 | 50.8% | 63.1% | 12.3 |
| 0.0 | 10.0 | app2 | True | False | 16192.0 | 25.4% | 26.1% | 0.7 |
| 0.0 | 10.0 | app3 | True | False | 4056.0 | 12.7% | 6.5% | -6.2 |
| 0.0 | 10.0 | app4 | True | False | 2674.0 | 6.3% | 4.3% | -2.0 |
| 0.0 | 10.0 | app5 | True | False | 0.0 | 3.2% | 0.0% | -3.2 |
| 0.0 | 10.0 | app6 | True | False | 0.0 | 1.6% | 0.0% | -1.6 |
| 10.0 | 20.0 | app1 | True | False | 152776.0 | 50.8% | 54.3% | 3.5 |
| 10.0 | 20.0 | app2 | True | False | 75830.0 | 25.4% | 27.0% | 1.6 |
| 10.0 | 20.0 | app3 | True | False | 35156.0 | 12.7% | 12.5% | -0.2 |
| 10.0 | 20.0 | app4 | True | False | 17570.0 | 6.3% | 6.2% | -0.1 |
| 10.0 | 20.0 | app5 | True | False | 0.0 | 3.2% | 0.0% | -3.2 |
| 10.0 | 20.0 | app6 | True | False | 0.0 | 1.6% | 0.0% | -1.6 |
| 20.0 | 30.0 | app1 | True | False | 127076.0 | 50.8% | 41.9% | -8.8 |
| 20.0 | 30.0 | app2 | True | False | 64950.0 | 25.4% | 21.4% | -4.0 |
| 20.0 | 30.0 | app3 | True | False | 62232.0 | 12.7% | 20.5% | 7.8 |
| 20.0 | 30.0 | app4 | True | False | 36550.0 | 6.3% | 12.1% | 5.7 |
| 20.0 | 30.0 | app5 | True | False | 8096.0 | 3.2% | 2.7% | -0.5 |
| 20.0 | 30.0 | app6 | True | False | 4062.0 | 1.6% | 1.3% | -0.2 |
| 30.0 | 40.0 | app1 | True | False | 162194.0 | 50.8% | 52.6% | 1.8 |
| 30.0 | 40.0 | app2 | True | False | 79870.0 | 25.4% | 25.9% | 0.5 |
| 30.0 | 40.0 | app3 | True | False | 36504.0 | 12.7% | 11.8% | -0.9 |
| 30.0 | 40.0 | app4 | True | False | 18962.0 | 6.3% | 6.2% | -0.2 |
| 30.0 | 40.0 | app5 | True | False | 6754.0 | 3.2% | 2.2% | -1.0 |
| 30.0 | 40.0 | app6 | True | False | 4034.0 | 1.6% | 1.3% | -0.3 |
| 40.0 | 50.0 | app1 | True | False | 151362.0 | 50.8% | 49.5% | -1.3 |
| 40.0 | 50.0 | app2 | True | False | 78466.0 | 25.4% | 25.7% | 0.3 |
| 40.0 | 50.0 | app3 | True | False | 39278.0 | 12.7% | 12.9% | 0.2 |
| 40.0 | 50.0 | app4 | True | False | 18924.0 | 6.3% | 6.2% | -0.2 |
| 40.0 | 50.0 | app5 | True | False | 12184.0 | 3.2% | 4.0% | 0.8 |
| 40.0 | 50.0 | app6 | True | False | 5406.0 | 1.6% | 1.8% | 0.2 |
| 50.0 | 60.0 | app1 | True | False | 155374.0 | 50.8% | 51.6% | 0.8 |
| 50.0 | 60.0 | app2 | True | False | 78422.0 | 25.4% | 26.0% | 0.6 |
| 50.0 | 60.0 | app3 | True | False | 36502.0 | 12.7% | 12.1% | -0.6 |
| 50.0 | 60.0 | app4 | True | False | 18940.0 | 6.3% | 6.3% | -0.1 |
| 50.0 | 60.0 | app5 | True | False | 8080.0 | 3.2% | 2.7% | -0.5 |
| 50.0 | 60.0 | app6 | True | False | 4074.0 | 1.6% | 1.4% | -0.2 |
| 60.0 | 70.0 | app1 | True | False | 110756.0 | 50.8% | 40.4% | -10.4 |
| 60.0 | 70.0 | app2 | True | False | 66300.0 | 25.4% | 24.2% | -1.2 |
| 60.0 | 70.0 | app3 | True | False | 47354.0 | 12.7% | 17.3% | 4.6 |
| 60.0 | 70.0 | app4 | True | False | 28366.0 | 6.3% | 10.3% | 4.0 |
| 60.0 | 70.0 | app5 | True | False | 13530.0 | 3.2% | 4.9% | 1.8 |
| 60.0 | 70.0 | app6 | True | False | 8120.0 | 1.6% | 3.0% | 1.4 |
| 70.0 | 80.0 | app1 | True | False | 60850.0 | 50.8% | 25.3% | -25.5 |
| 70.0 | 80.0 | app2 | True | False | 29818.0 | 25.4% | 12.4% | -13.0 |
| 70.0 | 80.0 | app3 | True | False | 40634.0 | 12.7% | 16.9% | 4.2 |
| 70.0 | 80.0 | app4 | True | False | 36502.0 | 6.3% | 15.2% | 8.8 |
| 70.0 | 80.0 | app5 | True | False | 40594.0 | 3.2% | 16.9% | 13.7 |
| 70.0 | 80.0 | app6 | True | False | 32468.0 | 1.6% | 13.5% | 11.9 |
| 80.0 | 90.0 | app1 | True | False | 114766.0 | 50.8% | 37.9% | -12.9 |
| 80.0 | 90.0 | app2 | True | False | 62202.0 | 25.4% | 20.6% | -4.8 |
| 80.0 | 90.0 | app3 | True | False | 52714.0 | 12.7% | 17.4% | 4.7 |
| 80.0 | 90.0 | app4 | True | False | 43294.0 | 6.3% | 14.3% | 8.0 |
| 80.0 | 90.0 | app5 | True | False | 26944.0 | 3.2% | 8.9% | 5.7 |
| 80.0 | 90.0 | app6 | True | False | 2708.0 | 1.6% | 0.9% | -0.7 |
| 90.0 | 100.0 | app1 | True | False | 123134.0 | 50.8% | 41.2% | -9.6 |
| 90.0 | 100.0 | app2 | True | False | 63656.0 | 25.4% | 21.3% | -4.1 |
| 90.0 | 100.0 | app3 | True | False | 46004.0 | 12.7% | 15.4% | 2.7 |
| 90.0 | 100.0 | app4 | True | False | 36482.0 | 6.3% | 12.2% | 5.9 |
| 90.0 | 100.0 | app5 | True | False | 22956.0 | 3.2% | 7.7% | 4.5 |
| 90.0 | 100.0 | app6 | True | False | 6762.0 | 1.6% | 2.3% | 0.7 |
| 100.0 | 110.0 | app1 | True | False | 117762.0 | 50.8% | 41.2% | -9.6 |
| 100.0 | 110.0 | app2 | True | False | 63654.0 | 25.4% | 22.3% | -3.1 |
| 100.0 | 110.0 | app3 | True | False | 37904.0 | 12.7% | 13.3% | 0.6 |
| 100.0 | 110.0 | app4 | True | False | 32480.0 | 6.3% | 11.4% | 5.0 |
| 100.0 | 110.0 | app5 | True | False | 20208.0 | 3.2% | 7.1% | 3.9 |
| 100.0 | 110.0 | app6 | True | False | 13540.0 | 1.6% | 4.7% | 3.2 |
| 110.0 | 120.0 | app1 | True | False | 167672.0 | 50.8% | 54.4% | 3.6 |
| 110.0 | 120.0 | app2 | True | False | 81070.0 | 25.4% | 26.3% | 0.9 |
| 110.0 | 120.0 | app3 | True | False | 29748.0 | 12.7% | 9.7% | -3.0 |
| 110.0 | 120.0 | app4 | True | False | 17592.0 | 6.3% | 5.7% | -0.6 |
| 110.0 | 120.0 | app5 | True | False | 8088.0 | 3.2% | 2.6% | -0.6 |
| 110.0 | 120.0 | app6 | True | False | 4074.0 | 1.6% | 1.3% | -0.3 |
| 120.0 | 130.0 | app1 | True | False | 171506.0 | 50.8% | 56.6% | 5.8 |
| 120.0 | 130.0 | app2 | True | False | 88020.0 | 25.4% | 29.1% | 3.7 |
| 120.0 | 130.0 | app3 | True | False | 41920.0 | 12.7% | 13.8% | 1.1 |
| 120.0 | 130.0 | app4 | True | False | 0.0 | 6.3% | 0.0% | -6.3 |
| 120.0 | 130.0 | app5 | True | False | 0.0 | 3.2% | 0.0% | -3.2 |
| 120.0 | 130.0 | app6 | True | False | 1358.0 | 1.6% | 0.4% | -1.1 |
| 130.0 | 140.0 | app1 | True | False | 123028.0 | 50.8% | 43.7% | -7.0 |
| 130.0 | 140.0 | app2 | True | False | 66230.0 | 25.4% | 23.5% | -1.8 |
| 130.0 | 140.0 | app3 | True | False | 52752.0 | 12.7% | 18.8% | 6.1 |
| 130.0 | 140.0 | app4 | True | False | 21660.0 | 6.3% | 7.7% | 1.4 |
| 130.0 | 140.0 | app5 | True | False | 12154.0 | 3.2% | 4.3% | 1.1 |
| 130.0 | 140.0 | app6 | True | False | 5420.0 | 1.6% | 1.9% | 0.3 |
| 140.0 | 150.0 | app1 | True | False | 127146.0 | 50.8% | 41.6% | -9.2 |
| 140.0 | 150.0 | app2 | True | False | 60764.0 | 25.4% | 19.9% | -5.5 |
| 140.0 | 150.0 | app3 | True | False | 35024.0 | 12.7% | 11.5% | -1.2 |
| 140.0 | 150.0 | app4 | True | False | 32450.0 | 6.3% | 10.6% | 4.3 |
| 140.0 | 150.0 | app5 | True | False | 33876.0 | 3.2% | 11.1% | 7.9 |
| 140.0 | 150.0 | app6 | True | False | 16224.0 | 1.6% | 5.3% | 3.7 |
| 150.0 | 160.0 | app1 | True | False | 123052.0 | 50.8% | 40.6% | -10.2 |
| 150.0 | 160.0 | app2 | True | False | 67574.0 | 25.4% | 22.3% | -3.1 |
| 150.0 | 160.0 | app3 | True | False | 55520.0 | 12.7% | 18.3% | 5.6 |
| 150.0 | 160.0 | app4 | True | False | 41998.0 | 6.3% | 13.9% | 7.5 |
| 150.0 | 160.0 | app5 | True | False | 10848.0 | 3.2% | 3.6% | 0.4 |
| 150.0 | 160.0 | app6 | True | False | 4058.0 | 1.6% | 1.3% | -0.2 |
| 160.0 | 170.0 | app1 | True | False | 127228.0 | 50.8% | 46.6% | -4.2 |
| 160.0 | 170.0 | app2 | True | False | 60808.0 | 25.4% | 22.3% | -3.1 |
| 160.0 | 170.0 | app3 | True | False | 29768.0 | 12.7% | 10.9% | -1.8 |
| 160.0 | 170.0 | app4 | True | False | 14854.0 | 6.3% | 5.4% | -0.9 |
| 160.0 | 170.0 | app5 | True | False | 27014.0 | 3.2% | 9.9% | 6.7 |
| 160.0 | 170.0 | app6 | True | False | 13514.0 | 1.6% | 4.9% | 3.4 |
| 170.0 | 181.0 | app1 | True | False | 129852.0 | 50.8% | 42.1% | -8.7 |
| 170.0 | 181.0 | app2 | True | False | 75654.0 | 25.4% | 24.5% | -0.9 |
| 170.0 | 181.0 | app3 | True | False | 46030.0 | 12.7% | 14.9% | 2.2 |
| 170.0 | 181.0 | app4 | True | False | 39222.0 | 6.3% | 12.7% | 6.4 |
| 170.0 | 181.0 | app5 | True | False | 10836.0 | 3.2% | 3.5% | 0.3 |
| 170.0 | 181.0 | app6 | True | False | 6790.0 | 1.6% | 2.2% | 0.6 |
| 181.0 | 191.0 | app1 | True | False | 156730.0 | 50.8% | 51.5% | 0.7 |
| 181.0 | 191.0 | app2 | True | False | 78504.0 | 25.4% | 25.8% | 0.4 |
| 181.0 | 191.0 | app3 | True | False | 50062.0 | 12.7% | 16.5% | 3.8 |
| 181.0 | 191.0 | app4 | True | False | 16266.0 | 6.3% | 5.3% | -1.0 |
| 181.0 | 191.0 | app5 | True | False | 1338.0 | 3.2% | 0.4% | -2.7 |
| 181.0 | 191.0 | app6 | True | False | 1340.0 | 1.6% | 0.4% | -1.1 |
| 191.0 | 201.0 | app1 | True | False | 159280.0 | 50.8% | 52.9% | 2.1 |
| 191.0 | 201.0 | app2 | True | False | 81246.0 | 25.4% | 27.0% | 1.6 |
| 191.0 | 201.0 | app3 | True | False | 27056.0 | 12.7% | 9.0% | -3.7 |
| 191.0 | 201.0 | app4 | True | False | 8108.0 | 6.3% | 2.7% | -3.7 |
| 191.0 | 201.0 | app5 | True | False | 17596.0 | 3.2% | 5.8% | 2.7 |
| 191.0 | 201.0 | app6 | True | False | 8086.0 | 1.6% | 2.7% | 1.1 |
| 201.0 | 211.0 | app1 | True | False | 151562.0 | 50.8% | 49.8% | -1.0 |
| 201.0 | 211.0 | app2 | True | False | 73008.0 | 25.4% | 24.0% | -1.4 |
| 201.0 | 211.0 | app3 | True | False | 46044.0 | 12.7% | 15.1% | 2.4 |
| 201.0 | 211.0 | app4 | True | False | 33722.0 | 6.3% | 11.1% | 4.7 |
| 201.0 | 211.0 | app5 | True | False | 0.0 | 3.2% | 0.0% | -3.2 |
| 201.0 | 211.0 | app6 | True | False | 0.0 | 1.6% | 0.0% | -1.6 |
| 211.0 | 221.0 | app1 | True | False | 152894.0 | 50.8% | 50.9% | 0.1 |
| 211.0 | 221.0 | app2 | True | False | 82552.0 | 25.4% | 27.5% | 2.1 |
| 211.0 | 221.0 | app3 | True | False | 43286.0 | 12.7% | 14.4% | 1.7 |
| 211.0 | 221.0 | app4 | True | False | 16256.0 | 6.3% | 5.4% | -0.9 |
| 211.0 | 221.0 | app5 | True | False | 2716.0 | 3.2% | 0.9% | -2.3 |
| 211.0 | 221.0 | app6 | True | False | 2716.0 | 1.6% | 0.9% | -0.7 |
| 221.0 | 231.0 | app1 | True | False | 140518.0 | 50.8% | 46.4% | -4.4 |
| 221.0 | 231.0 | app2 | True | False | 66330.0 | 25.4% | 21.9% | -3.5 |
| 221.0 | 231.0 | app3 | True | False | 46094.0 | 12.7% | 15.2% | 2.5 |
| 221.0 | 231.0 | app4 | True | False | 28402.0 | 6.3% | 9.4% | 3.0 |
| 221.0 | 231.0 | app5 | True | False | 14920.0 | 3.2% | 4.9% | 1.7 |
| 221.0 | 231.0 | app6 | True | False | 6790.0 | 1.6% | 2.2% | 0.7 |
| 231.0 | 241.0 | app1 | True | False | 158286.0 | 50.8% | 51.8% | 1.0 |
| 231.0 | 241.0 | app2 | True | False | 83698.0 | 25.4% | 27.4% | 2.0 |
| 231.0 | 241.0 | app3 | True | False | 45978.0 | 12.7% | 15.0% | 2.3 |
| 231.0 | 241.0 | app4 | True | False | 13562.0 | 6.3% | 4.4% | -1.9 |
| 231.0 | 241.0 | app5 | True | False | 2682.0 | 3.2% | 0.9% | -2.3 |
| 231.0 | 241.0 | app6 | True | False | 1358.0 | 1.6% | 0.4% | -1.1 |
| 241.0 | 251.0 | app1 | False | n/a | 89302.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 47394.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app3 | False | n/a | 44596.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app4 | False | n/a | 43270.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app5 | False | n/a | 33836.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app6 | False | n/a | 16220.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | False | n/a | 9462.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | False | n/a | 26984.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 354.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 354.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 354.0 | app3 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 354.0 | app4 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 354.0 | app5 | False | n/a | 0.0 | n/a | n/a | n/a |
| 351.0 | 354.0 | app6 | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 93 | 706ms | 2003ms | 4419ms |
| 0.0 | 10.0 | app2 | ok | 55 | 592ms | 1886ms | 3625ms |
| 0.0 | 10.0 | app3 | ok | 42 | 1750ms | 4417ms | 4942ms |
| 0.0 | 10.0 | app4 | ok | 22 | 2500ms | 4500ms | 4950ms |
| 0.0 | 10.0 | app5 | ok | 20 | 0ms | 0ms | 4ms |
| 0.0 | 10.0 | app6 | ok | 21 | 0ms | 0ms | 4ms |
| 10.0 | 20.0 | app1 | ok | 130 | 1443ms | 3523ms | 4852ms |
| 10.0 | 20.0 | app2 | ok | 65 | 1586ms | 3750ms | 4875ms |
| 10.0 | 20.0 | app3 | ok | 37 | 3173ms | 7944ms | 9794ms |
| 10.0 | 20.0 | app4 | ok | 34 | 9286ms | 25467ms | 29547ms |
| 10.0 | 20.0 | app5 | ok | 21 | 20000ms | 28000ms | 29800ms |
| 10.0 | 20.0 | app6 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app1 | ok | 66 | 2938ms | 4588ms | 4959ms |
| 20.0 | 30.0 | app2 | ok | 33 | 3125ms | 4625ms | 4962ms |
| 20.0 | 30.0 | app3 | ok | 21 | 3359ms | 4672ms | 4967ms |
| 20.0 | 30.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 20.0 | 30.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 119 | 1213ms | 2278ms | 3513ms |
| 30.0 | 40.0 | app2 | ok | 62 | 1486ms | 2492ms | 4742ms |
| 30.0 | 40.0 | app3 | ok | 33 | 6562ms | 9312ms | 9931ms |
| 30.0 | 40.0 | app4 | ok | 16 | 14000ms | 26800ms | 29680ms |
| 30.0 | 40.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 135 | 1212ms | 2891ms | 4789ms |
| 40.0 | 50.0 | app2 | ok | 67 | 1425ms | 3604ms | 4860ms |
| 40.0 | 50.0 | app3 | ok | 37 | 3812ms | 7944ms | 9794ms |
| 40.0 | 50.0 | app4 | ok | 20 | 18235ms | 27647ms | 29765ms |
| 40.0 | 50.0 | app5 | ok | 4 | 45000ms | 57000ms | 59700ms |
| 40.0 | 50.0 | app6 | ok | 3 | 45000ms | 57000ms | 59700ms |
| 50.0 | 60.0 | app1 | ok | 71 | 1604ms | 3732ms | 4873ms |
| 50.0 | 60.0 | app2 | ok | 36 | 1375ms | 3500ms | 4850ms |
| 50.0 | 60.0 | app3 | ok | 27 | 2417ms | 4646ms | 8650ms |
| 50.0 | 60.0 | app4 | ok | 27 | 9583ms | 25846ms | 29585ms |
| 50.0 | 60.0 | app5 | ok | 26 | 23333ms | 51333ms | 59133ms |
| 50.0 | 60.0 | app6 | ok | 12 | 45000ms | 57000ms | 59700ms |
| 60.0 | 70.0 | app1 | ok | 77 | 2962ms | 4636ms | 6150ms |
| 60.0 | 70.0 | app2 | ok | 42 | 2614ms | 4523ms | 4952ms |
| 60.0 | 70.0 | app3 | ok | 32 | 3750ms | 8000ms | 9800ms |
| 60.0 | 70.0 | app4 | ok | 22 | 2500ms | 6333ms | 9633ms |
| 60.0 | 70.0 | app5 | ok | 15 | 3438ms | 15000ms | 28500ms |
| 60.0 | 70.0 | app6 | ok | 18 | 35455ms | 55091ms | 59509ms |
| 70.0 | 80.0 | app1 | ok | 81 | 6680ms | 9336ms | 9934ms |
| 70.0 | 80.0 | app2 | ok | 40 | 6429ms | 9286ms | 9929ms |
| 70.0 | 80.0 | app3 | ok | 32 | 2300ms | 6800ms | 9680ms |
| 70.0 | 80.0 | app4 | ok | 15 | 750ms | 8500ms | 9850ms |
| 70.0 | 80.0 | app5 | ok | 5 | 1750ms | 8750ms | 9875ms |
| 70.0 | 80.0 | app6 | ok | 9 | 9375ms | 25500ms | 29550ms |
| 80.0 | 90.0 | app1 | ok | 91 | 2679ms | 4536ms | 4954ms |
| 80.0 | 90.0 | app2 | ok | 49 | 2812ms | 4562ms | 4956ms |
| 80.0 | 90.0 | app3 | ok | 30 | 3281ms | 6250ms | 9625ms |
| 80.0 | 90.0 | app4 | ok | 22 | 5769ms | 9154ms | 9915ms |
| 80.0 | 90.0 | app5 | ok | 21 | 5357ms | 19500ms | 28950ms |
| 80.0 | 90.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 98 | 2333ms | 4595ms | 8367ms |
| 90.0 | 100.0 | app2 | ok | 53 | 3008ms | 4664ms | 7350ms |
| 90.0 | 100.0 | app3 | ok | 53 | 3413ms | 7350ms | 9735ms |
| 90.0 | 100.0 | app4 | ok | 29 | 4028ms | 8682ms | 9868ms |
| 90.0 | 100.0 | app5 | ok | 23 | 2406ms | 22333ms | 29233ms |
| 90.0 | 100.0 | app6 | ok | 7 | 20000ms | 28000ms | 29800ms |
| 100.0 | 110.0 | app1 | ok | 70 | 3265ms | 4694ms | 6500ms |
| 100.0 | 110.0 | app2 | ok | 35 | 2812ms | 4562ms | 4956ms |
| 100.0 | 110.0 | app3 | ok | 3 | 3125ms | 4625ms | 4962ms |
| 100.0 | 110.0 | app4 | ok | 31 | 4904ms | 9958ms | 27933ms |
| 100.0 | 110.0 | app5 | ok | 26 | 6429ms | 23500ms | 29350ms |
| 100.0 | 110.0 | app6 | ok | 13 | 20000ms | 28000ms | 29800ms |
| 110.0 | 120.0 | app1 | ok | 131 | 1462ms | 3798ms | 7817ms |
| 110.0 | 120.0 | app2 | ok | 68 | 1700ms | 4056ms | 4906ms |
| 110.0 | 120.0 | app3 | ok | 37 | 5978ms | 9196ms | 9920ms |
| 110.0 | 120.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 110.0 | 120.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 133 | 1330ms | 2394ms | 4584ms |
| 120.0 | 130.0 | app2 | ok | 67 | 1236ms | 2384ms | 4581ms |
| 120.0 | 130.0 | app3 | ok | 39 | 3938ms | 8227ms | 9823ms |
| 120.0 | 130.0 | app4 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 120.0 | 130.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 120.0 | 130.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 99 | 2862ms | 7088ms | 9709ms |
| 130.0 | 140.0 | app2 | ok | 53 | 2679ms | 6214ms | 9621ms |
| 130.0 | 140.0 | app3 | ok | 37 | 2159ms | 4696ms | 9075ms |
| 130.0 | 140.0 | app4 | ok | 29 | 14737ms | 26947ms | 29695ms |
| 130.0 | 140.0 | app5 | ok | 19 | 22222ms | 50500ms | 59050ms |
| 130.0 | 140.0 | app6 | ok | 11 | 45000ms | 57000ms | 59700ms |
| 140.0 | 150.0 | app1 | ok | 97 | 1588ms | 4067ms | 4907ms |
| 140.0 | 150.0 | app2 | ok | 47 | 1625ms | 4096ms | 4910ms |
| 140.0 | 150.0 | app3 | ok | 32 | 2125ms | 8222ms | 9822ms |
| 140.0 | 150.0 | app4 | ok | 28 | 6957ms | 9391ms | 9939ms |
| 140.0 | 150.0 | app5 | ok | 26 | 8095ms | 19600ms | 28960ms |
| 140.0 | 150.0 | app6 | ok | 11 | 45000ms | 57000ms | 59700ms |
| 150.0 | 160.0 | app1 | ok | 71 | 3097ms | 4710ms | 8225ms |
| 150.0 | 160.0 | app2 | ok | 37 | 3317ms | 4740ms | 8150ms |
| 150.0 | 160.0 | app3 | ok | 18 | 3500ms | 4700ms | 4970ms |
| 150.0 | 160.0 | app4 | ok | 5 | 6875ms | 9375ms | 9938ms |
| 150.0 | 160.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 150.0 | 160.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 100 | 1682ms | 4239ms | 8333ms |
| 160.0 | 170.0 | app2 | ok | 54 | 2143ms | 4476ms | 7300ms |
| 160.0 | 170.0 | app3 | ok | 43 | 4271ms | 8806ms | 9881ms |
| 160.0 | 170.0 | app4 | ok | 38 | 7593ms | 17333ms | 28733ms |
| 160.0 | 170.0 | app5 | ok | 22 | 11667ms | 26333ms | 29633ms |
| 160.0 | 170.0 | app6 | ok | 12 | 30000ms | 54000ms | 59400ms |
| 170.0 | 181.0 | app1 | ok | 106 | 2275ms | 4436ms | 4944ms |
| 170.0 | 181.0 | app2 | ok | 59 | 2139ms | 4359ms | 4936ms |
| 170.0 | 181.0 | app3 | ok | 27 | 5179ms | 9036ms | 9904ms |
| 170.0 | 181.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 170.0 | 181.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 170.0 | 181.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 108 | 1462ms | 2458ms | 4700ms |
| 181.0 | 191.0 | app2 | ok | 52 | 1341ms | 3556ms | 4856ms |
| 181.0 | 191.0 | app3 | ok | 29 | 3977ms | 8550ms | 9855ms |
| 181.0 | 191.0 | app4 | ok | 12 | 9286ms | 25200ms | 29520ms |
| 181.0 | 191.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 181.0 | 191.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 99 | 1460ms | 3697ms | 4870ms |
| 191.0 | 201.0 | app2 | ok | 50 | 1420ms | 3214ms | 4821ms |
| 191.0 | 201.0 | app3 | ok | 23 | 3203ms | 4641ms | 4964ms |
| 191.0 | 201.0 | app4 | ok | 29 | 15500ms | 27100ms | 29710ms |
| 191.0 | 201.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 191.0 | 201.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 130 | 1568ms | 3289ms | 4829ms |
| 201.0 | 211.0 | app2 | ok | 65 | 1588ms | 3375ms | 4837ms |
| 201.0 | 211.0 | app3 | ok | 48 | 1750ms | 4462ms | 8800ms |
| 201.0 | 211.0 | app4 | ok | 11 | 7500ms | 9944ms | 27800ms |
| 201.0 | 211.0 | app5 | ok | 2 | 45000ms | 57000ms | 59700ms |
| 201.0 | 211.0 | app6 | ok | 1 | 60000ms | 60000ms | 60000ms |
| 211.0 | 221.0 | app1 | ok | 71 | 1507ms | 3635ms | 4863ms |
| 211.0 | 221.0 | app2 | ok | 37 | 1574ms | 3844ms | 4884ms |
| 211.0 | 221.0 | app3 | ok | 22 | 929ms | 2170ms | 2467ms |
| 211.0 | 221.0 | app4 | ok | 23 | 6167ms | 9233ms | 9923ms |
| 211.0 | 221.0 | app5 | ok | 23 | 38438ms | 55688ms | 59569ms |
| 211.0 | 221.0 | app6 | ok | 11 | 57500ms | 60000ms | 60000ms |
| 221.0 | 231.0 | app1 | ok | 132 | 2159ms | 4411ms | 4941ms |
| 221.0 | 231.0 | app2 | ok | 70 | 2086ms | 4352ms | 4935ms |
| 221.0 | 231.0 | app3 | ok | 30 | 5312ms | 9062ms | 9906ms |
| 221.0 | 231.0 | app4 | ok | 1 | 20000ms | 28000ms | 29800ms |
| 221.0 | 231.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 221.0 | 231.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 133 | 1096ms | 2236ms | 2493ms |
| 231.0 | 241.0 | app2 | ok | 68 | 1203ms | 2305ms | 4150ms |
| 231.0 | 241.0 | app3 | ok | 32 | 4808ms | 8933ms | 9893ms |
| 231.0 | 241.0 | app4 | ok | 16 | 20000ms | 28000ms | 29800ms |
| 231.0 | 241.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 231.0 | 241.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 22 | 1711ms | 2405ms | 4450ms |
| 241.0 | 251.0 | app2 | ok | 7 | 1450ms | 2290ms | 2479ms |
| 241.0 | 251.0 | app3 | ok | 17 | 2917ms | 4806ms | 9150ms |
| 241.0 | 251.0 | app4 | ok | 24 | 15000ms | 27000ms | 29700ms |
| 241.0 | 251.0 | app5 | ok | 22 | 23846ms | 50571ms | 59057ms |
| 241.0 | 251.0 | app6 | ok | 27 | 53571ms | 60000ms | 60000ms |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 321.0 | 331.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 354.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 354.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 354.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 354.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 354.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 351.0 | 354.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app6 exceeded the 10% ledger tolerance: cost -12.7%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 3028260 | 150073 | 3178333.0 | 0.0% | 3293264.0 | 3328406.0 | -1.1% | True |
| app2 | 1563330 | 77943 | 1641273.0 | 0.0% | 1692212.0 | 1719216.0 | -1.6% | True |
| app3 | 960630 | 47951 | 1008581.0 | 0.0% | 1032216.0 | 1056532.0 | -2.3% | True |
| app4 | 573180 | 28555 | 601735.0 | 0.0% | 618106.0 | 630290.0 | -1.9% | True |
| app5 | 338250 | 16754 | 355004.0 | 0.0% | 344712.0 | 371758.0 | -7.3% | True |
| app6 | 204180 | 10191 | 214371.0 | 0.0% | 196106.0 | 224562.0 | -12.7% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2463 | 0 | 0 | 0 (never shed) | 0.00% | 50.8% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 1271 | 0 | 0 | 0 (never shed) | 0.00% | 25.4% | n/a (nothing shed) | n/a (nothing shed) |
| app3 | 781 | 0 | 0 | 0 (never shed) | 0.00% | 12.7% | n/a (nothing shed) | n/a (nothing shed) |
| app4 | 466 | 0 | 0 | 0 (never shed) | 0.00% | 6.3% | n/a (nothing shed) | n/a (nothing shed) |
| app5 | 275 | 0 | 0 | 0 (never shed) | 0.00% | 3.2% | n/a (nothing shed) | n/a (nothing shed) |
| app6 | 166 | 0 | 0 | 0 (never shed) | 0.00% | 1.6% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5422). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5422 | 0.051ms | 0.143ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 334172 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 2462 | 5271ms | 8625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 1271 | 5770ms | 9073ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app3 | ok | 781 | 9978ms | 14591ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app4 | ok | 466 | 15208ms | 31558ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app5 | ok | 275 | 25956ms | 56734ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app6 | ok | 166 | 50233ms | 110945ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5421 | 6308ms | 29334ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (36 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2750ms | 5100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 2333ms | 4900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app3 | ok | 2300ms | 5475ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app4 | ok | 2375ms | 5450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app5 | ok | 3400ms | 4800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app6 | ok | 4188ms | 4919ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 5179ms | 7557ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 5667ms | 7720ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app3 | ok | 9333ms | 14278ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app4 | ok | 9800ms | 14458ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app5 | ok | 12143ms | 14714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app6 | ok | 17083ms | 19708ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 6226ms | 7823ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 6545ms | 7855ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app3 | ok | 8000ms | 14500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app4 | ok | 16346ms | 26625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app5 | ok | 22500ms | 29250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app6 | ok | 23333ms | 29333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 5000ms | 7600ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 5548ms | 8820ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app3 | ok | 9000ms | 14156ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app4 | ok | 14375ms | 19417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app5 | ok | 32500ms | 43750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app6 | ok | 33750ms | 43875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 4812ms | 6756ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 5529ms | 7554ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app3 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app4 | ok | 19375ms | 28833ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app5 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app6 | ok | 40000ms | 57000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 4890ms | 7042ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 5400ms | 7586ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app3 | ok | 12300ms | 14730ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app4 | ok | 24167ms | 29417ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app5 | ok | 51000ms | 59100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app6 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 6000ms | 9414ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 5812ms | 8775ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app3 | ok | 9318ms | 14125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app4 | ok | 18611ms | 28688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app5 | ok | 38333ms | 52500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app6 | ok | 54000ms | 102000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 11250ms | 14625ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 11562ms | 14656ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app3 | ok | 8963ms | 9963ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app4 | ok | 13214ms | 18875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app5 | ok | 24444ms | 42750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app6 | ok | 51000ms | 108000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 6984ms | 13208ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 7161ms | 13850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app3 | ok | 11389ms | 14639ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app4 | ok | 12963ms | 18400ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app5 | ok | 13846ms | 20000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app6 | ok | 30000ms | 43500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 6553ms | 9494ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 6739ms | 9478ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app3 | ok | 9444ms | 14292ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app4 | ok | 11447ms | 14645ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app5 | ok | 14250ms | 19393ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app6 | ok | 32500ms | 43750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app1 | ok | 6265ms | 7863ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app2 | ok | 6875ms | 9753ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app3 | ok | 12083ms | 14708ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app4 | ok | 12857ms | 18000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app5 | ok | 13125ms | 18750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 110.0 | app6 | ok | 27143ms | 42500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app1 | ok | 5391ms | 7990ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app2 | ok | 5867ms | 7786ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app3 | ok | 10714ms | 18900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app4 | ok | 12708ms | 23500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app5 | ok | 18750ms | 28500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 110.0 | 120.0 | app6 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app1 | ok | 4430ms | 5843ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app2 | ok | 4948ms | 5925ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app3 | ok | 10441ms | 14544ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 120.0 | 130.0 | app6 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app1 | ok | 4904ms | 6989ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app2 | ok | 5712ms | 7712ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app3 | ok | 9750ms | 14426ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app4 | ok | 26667ms | 42000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app5 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 130.0 | 140.0 | app6 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app1 | ok | 6625ms | 9739ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app2 | ok | 7632ms | 9763ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app3 | ok | 10667ms | 14567ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app4 | ok | 33000ms | 43800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app5 | ok | 36848ms | 44185ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 140.0 | 150.0 | app6 | ok | 68571ms | 114857ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app1 | ok | 5809ms | 7767ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app2 | ok | 6148ms | 7815ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app3 | ok | 7462ms | 14212ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app4 | ok | 13654ms | 19354ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app5 | ok | 23333ms | 29333ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 150.0 | 160.0 | app6 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app1 | ok | 6091ms | 8120ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app2 | ok | 6600ms | 9100ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app3 | ok | 9714ms | 14450ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app4 | ok | 11071ms | 14607ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app5 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 160.0 | 170.0 | app6 | ok | 77143ms | 115714ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 181.0 | app1 | ok | 5920ms | 9040ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 181.0 | app2 | ok | 6621ms | 9300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 181.0 | app3 | ok | 11364ms | 14841ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 181.0 | app4 | ok | 16528ms | 22750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 181.0 | app5 | ok | 30000ms | 43500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 170.0 | 181.0 | app6 | ok | 52500ms | 112500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 4579ms | 8067ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 5269ms | 8067ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app3 | ok | 9938ms | 14486ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app4 | ok | 18000ms | 27000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app5 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app6 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 4714ms | 7631ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 5091ms | 8000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app3 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app4 | ok | 25000ms | 29500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app5 | ok | 26500ms | 41750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app6 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 5021ms | 6880ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 5474ms | 7682ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app3 | ok | 10588ms | 15750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app4 | ok | 25769ms | 42321ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 4784ms | 7647ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 5620ms | 7710ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app3 | ok | 7882ms | 14467ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app4 | ok | 17500ms | 28500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app5 | ok | 52500ms | 59250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 5793ms | 7855ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 5886ms | 7777ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app3 | ok | 7545ms | 9717ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app4 | ok | 13750ms | 19250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app5 | ok | 54167ms | 103500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 4616ms | 5934ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 5179ms | 7225ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app3 | ok | 12069ms | 14707ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app4 | ok | 18125ms | 27500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app5 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 4826ms | 6900ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 6158ms | 7816ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app3 | ok | 9357ms | 14312ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app4 | ok | 21579ms | 29158ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app5 | ok | 49821ms | 95000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app6 | ok | 90000ms | 117000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app5 | ok | 23000ms | 29300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app6 | ok | 70000ms | 115000ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 271.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 271.0 | 281.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 281.0 | 291.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 291.0 | 301.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 301.0 | 311.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 311.0 | 321.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 321.0 | 331.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 331.0 | 341.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 341.0 | 351.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 354.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 354.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 354.0 | app3 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 354.0 | app4 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 354.0 | app5 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 351.0 | 354.0 | app6 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
