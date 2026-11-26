# Fairness benchmark: app1-flood (uni310-l2-r1-uni161-app1-flood-256)

**Verdict: PASS** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 42.7 points

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-flood` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-85c4448547-pkq7m` |
| Namespace | `poc-maas-lane2` |
| Run start | `2026-11-26T02:57:33Z` |
| Run end | `2026-11-26T03:02:01Z` |

## Saturation limb (UNI-224)

Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` (32) and `llm_d_epp_average_kv_cache_utilization` / `kvCacheUtilThreshold` (0.8) across 28 timeseries samples -- see docs/design.md's saturation-detector section for the roofline formula this reconstructs.

**Bound at this run's peak roofline score: `queue`** (0/28 samples had the KV limb ahead of the queue limb).

| signal | peak value | peak ratio to threshold |
|---|---|---|
| `average_queue_size` | 67.00 | 2.0938 |
| `average_kv_cache_utilization` | 0.0000 | 0.0000 |

The KV-cache limb stayed near zero this run; every verdict above was decided on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable at all.

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 30.0 | 256 | 1952 | 200=1952 | 35.5 | 40.0 | 2327954.0 | 30.0% | 72.7% | 42.7 | 31.9% | 1.9 | 34.5% | 4.5 | 78.4s | 98.9% | 1952.0 |
| app2 | 10.0 | 32 | 598 | 200=598 | 13.3 | 16.5 | 790808.0 | 10.0% | 9.1% | -0.9 | 10.8% | 0.8 | 10.6% | 0.6 | 78.4s | 98.9% | 598.0 |
| end-users | 60.0 | 64 | 3107 | 200=3107 | 4.8 | 7.2 | 4172804.0 | 60.0% | 18.2% | -41.8 | 57.2% | -2.8 | 54.9% | -5.1 | 75.1s | 98.9% | 3107.0 |
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
| 0.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | uncontended | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | False | 0.0 | 30.0% | 0.0% | -30.0 |
| 0.0 | 10.0 | app2 | True | False | 0.0 | 10.0% | 0.0% | -10.0 |
| 0.0 | 10.0 | end-users | True | False | 35078.0 | 60.0% | 100.0% | 40.0 |
| 10.0 | 20.0 | app1 | True | False | 70246.0 | 30.0% | 28.1% | -1.9 |
| 10.0 | 20.0 | app2 | True | False | 43256.0 | 10.0% | 17.3% | 7.3 |
| 10.0 | 20.0 | end-users | True | False | 136502.0 | 60.0% | 54.6% | -5.4 |
| 20.0 | 30.0 | app1 | True | False | 70302.0 | 30.0% | 22.9% | -7.1 |
| 20.0 | 30.0 | app2 | True | False | 27078.0 | 10.0% | 8.8% | -1.2 |
| 20.0 | 30.0 | end-users | True | False | 209478.0 | 60.0% | 68.3% | 8.3 |
| 30.0 | 40.0 | app1 | True | False | 86532.0 | 30.0% | 28.1% | -1.9 |
| 30.0 | 40.0 | app2 | True | False | 28414.0 | 10.0% | 9.2% | -0.8 |
| 30.0 | 40.0 | end-users | True | False | 193234.0 | 60.0% | 62.7% | 2.7 |
| 40.0 | 50.0 | app1 | True | False | 93290.0 | 30.0% | 30.1% | 0.1 |
| 40.0 | 50.0 | app2 | True | False | 31120.0 | 10.0% | 10.0% | 0.0 |
| 40.0 | 50.0 | end-users | True | False | 185374.0 | 60.0% | 59.8% | -0.2 |
| 50.0 | 60.0 | app1 | True | False | 90620.0 | 30.0% | 29.5% | -0.5 |
| 50.0 | 60.0 | app2 | True | False | 29788.0 | 10.0% | 9.7% | -0.3 |
| 50.0 | 60.0 | end-users | True | False | 186562.0 | 60.0% | 60.8% | 0.8 |
| 60.0 | 70.0 | app1 | True | False | 93242.0 | 30.0% | 31.2% | 1.2 |
| 60.0 | 70.0 | app2 | True | False | 30974.0 | 10.0% | 10.4% | 0.4 |
| 60.0 | 70.0 | end-users | True | False | 174534.0 | 60.0% | 58.4% | -1.6 |
| 70.0 | 80.0 | app1 | True | False | 110852.0 | 30.0% | 36.1% | 6.1 |
| 70.0 | 80.0 | app2 | True | False | 40564.0 | 10.0% | 13.2% | 3.2 |
| 70.0 | 80.0 | end-users | True | False | 155650.0 | 60.0% | 50.7% | -9.3 |
| 80.0 | 90.0 | app1 | True | False | 100062.0 | 30.0% | 33.6% | 3.6 |
| 80.0 | 90.0 | app2 | True | False | 31090.0 | 10.0% | 10.4% | 0.4 |
| 80.0 | 90.0 | end-users | True | False | 166384.0 | 60.0% | 55.9% | -4.1 |
| 90.0 | 100.0 | app1 | True | False | 102822.0 | 30.0% | 33.9% | 3.9 |
| 90.0 | 100.0 | app2 | True | False | 32446.0 | 10.0% | 10.7% | 0.7 |
| 90.0 | 100.0 | end-users | True | False | 167834.0 | 60.0% | 55.4% | -4.6 |
| 100.0 | 111.0 | app1 | True | False | 83790.0 | 30.0% | 27.5% | -2.5 |
| 100.0 | 111.0 | app2 | True | False | 27006.0 | 10.0% | 8.9% | -1.1 |
| 100.0 | 111.0 | end-users | True | False | 193536.0 | 60.0% | 63.6% | 3.6 |
| 111.0 | 121.0 | app1 | True | False | 79768.0 | 30.0% | 26.1% | -3.9 |
| 111.0 | 121.0 | app2 | True | False | 28414.0 | 10.0% | 9.3% | -0.7 |
| 111.0 | 121.0 | end-users | True | False | 197446.0 | 60.0% | 64.6% | 4.6 |
| 121.0 | 131.0 | app1 | True | False | 112200.0 | 30.0% | 35.9% | 5.9 |
| 121.0 | 131.0 | app2 | True | False | 37888.0 | 10.0% | 12.1% | 2.1 |
| 121.0 | 131.0 | end-users | True | False | 162290.0 | 60.0% | 52.0% | -8.0 |
| 131.0 | 141.0 | app1 | True | False | 81138.0 | 30.0% | 26.9% | -3.1 |
| 131.0 | 141.0 | app2 | True | False | 24382.0 | 10.0% | 8.1% | -1.9 |
| 131.0 | 141.0 | end-users | True | False | 196226.0 | 60.0% | 65.0% | 5.0 |
| 141.0 | 151.0 | app1 | True | False | 108136.0 | 30.0% | 36.6% | 6.6 |
| 141.0 | 151.0 | app2 | True | False | 35096.0 | 10.0% | 11.9% | 1.9 |
| 141.0 | 151.0 | end-users | True | False | 152530.0 | 60.0% | 51.6% | -8.4 |
| 151.0 | 161.0 | app1 | True | False | 63594.0 | 30.0% | 21.3% | -8.7 |
| 151.0 | 161.0 | app2 | True | False | 22914.0 | 10.0% | 7.7% | -2.3 |
| 151.0 | 161.0 | end-users | True | False | 212264.0 | 60.0% | 71.0% | 11.0 |
| 161.0 | 171.0 | app1 | True | False | 129814.0 | 30.0% | 41.9% | 11.9 |
| 161.0 | 171.0 | app2 | True | False | 43312.0 | 10.0% | 14.0% | 4.0 |
| 161.0 | 171.0 | end-users | True | False | 136540.0 | 60.0% | 44.1% | -15.9 |
| 171.0 | 181.0 | app1 | True | False | 97286.0 | 30.0% | 31.9% | 1.9 |
| 171.0 | 181.0 | app2 | True | False | 33816.0 | 10.0% | 11.1% | 1.1 |
| 171.0 | 181.0 | end-users | True | False | 174316.0 | 60.0% | 57.1% | -2.9 |
| 181.0 | 191.0 | app1 | True | False | 95820.0 | 30.0% | 31.5% | 1.5 |
| 181.0 | 191.0 | app2 | True | False | 31084.0 | 10.0% | 10.2% | 0.2 |
| 181.0 | 191.0 | end-users | True | False | 177118.0 | 60.0% | 58.3% | -1.7 |
| 191.0 | 201.0 | app1 | True | False | 82576.0 | 30.0% | 26.9% | -3.1 |
| 191.0 | 201.0 | app2 | True | False | 28444.0 | 10.0% | 9.3% | -0.7 |
| 191.0 | 201.0 | end-users | True | False | 196022.0 | 60.0% | 63.8% | 3.8 |
| 201.0 | 211.0 | app1 | True | False | 83880.0 | 30.0% | 27.3% | -2.7 |
| 201.0 | 211.0 | app2 | True | False | 27046.0 | 10.0% | 8.8% | -1.2 |
| 201.0 | 211.0 | end-users | True | False | 195934.0 | 60.0% | 63.9% | 3.9 |
| 211.0 | 221.0 | app1 | True | False | 101312.0 | 30.0% | 33.8% | 3.8 |
| 211.0 | 221.0 | app2 | True | False | 36430.0 | 10.0% | 12.1% | 2.1 |
| 211.0 | 221.0 | end-users | True | False | 162164.0 | 60.0% | 54.1% | -5.9 |
| 221.0 | 231.0 | app1 | True | False | 115052.0 | 30.0% | 39.0% | 9.0 |
| 221.0 | 231.0 | app2 | True | False | 36418.0 | 10.0% | 12.4% | 2.4 |
| 221.0 | 231.0 | end-users | True | False | 143308.0 | 60.0% | 48.6% | -11.4 |
| 231.0 | 241.0 | app1 | True | False | 116248.0 | 30.0% | 39.2% | 9.2 |
| 231.0 | 241.0 | app2 | True | False | 37938.0 | 10.0% | 12.8% | 2.8 |
| 231.0 | 241.0 | end-users | True | False | 142062.0 | 60.0% | 48.0% | -12.0 |
| 241.0 | 251.0 | app1 | False | n/a | 116184.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | n/a | 39116.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | n/a | 120418.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | n/a | 43188.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | n/a | 6774.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 268.0 | app1 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 268.0 | app2 | False | n/a | 0.0 | n/a | n/a | n/a |
| 261.0 | 268.0 | end-users | False | n/a | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 122 | 0ms | 1962ms | 2446ms |
| 0.0 | 10.0 | app2 | ok | 39 | 239ms | 919ms | 1915ms |
| 0.0 | 10.0 | end-users | ok | 81 | 507ms | 933ms | 2095ms |
| 10.0 | 20.0 | app1 | ok | 56 | 7642ms | 9755ms | 26267ms |
| 10.0 | 20.0 | app2 | ok | 20 | 3333ms | 7500ms | 9750ms |
| 10.0 | 20.0 | end-users | ok | 115 | 2865ms | 4635ms | 7125ms |
| 20.0 | 30.0 | app1 | ok | 67 | 20000ms | 28000ms | 29800ms |
| 20.0 | 30.0 | app2 | ok | 22 | 6333ms | 9267ms | 9927ms |
| 20.0 | 30.0 | end-users | ok | 145 | 1265ms | 2326ms | 4275ms |
| 30.0 | 40.0 | app1 | ok | 66 | 20476ms | 28857ms | 53400ms |
| 30.0 | 40.0 | app2 | ok | 23 | 7500ms | 9690ms | 25400ms |
| 30.0 | 40.0 | end-users | ok | 153 | 1298ms | 2404ms | 4618ms |
| 40.0 | 50.0 | app1 | ok | 64 | 44000ms | 56800ms | 59680ms |
| 40.0 | 50.0 | app2 | ok | 22 | 7500ms | 9500ms | 9950ms |
| 40.0 | 50.0 | end-users | ok | 142 | 1196ms | 2430ms | 4677ms |
| 50.0 | 60.0 | app1 | ok | 60 | 45000ms | 57000ms | 59700ms |
| 50.0 | 60.0 | app2 | ok | 19 | 7500ms | 9500ms | 9950ms |
| 50.0 | 60.0 | end-users | ok | 131 | 1207ms | 2241ms | 2474ms |
| 60.0 | 70.0 | app1 | ok | 116 | 24872ms | 50842ms | 59084ms |
| 60.0 | 70.0 | app2 | ok | 37 | 5595ms | 9119ms | 9912ms |
| 60.0 | 70.0 | end-users | ok | 102 | 1462ms | 3938ms | 4894ms |
| 70.0 | 80.0 | app1 | ok | 52 | 20000ms | 28000ms | 29800ms |
| 70.0 | 80.0 | app2 | ok | 19 | 6042ms | 9208ms | 9921ms |
| 70.0 | 80.0 | end-users | ok | 134 | 1938ms | 4440ms | 8325ms |
| 80.0 | 90.0 | app1 | ok | 108 | 20000ms | 28000ms | 29800ms |
| 80.0 | 90.0 | app2 | ok | 37 | 4125ms | 8767ms | 9877ms |
| 80.0 | 90.0 | end-users | ok | 146 | 2114ms | 4348ms | 4935ms |
| 90.0 | 100.0 | app1 | ok | 28 | 20000ms | 28000ms | 29800ms |
| 90.0 | 100.0 | app2 | ok | 8 | 5000ms | 9000ms | 9900ms |
| 90.0 | 100.0 | end-users | ok | 96 | 1909ms | 4368ms | 5200ms |
| 100.0 | 111.0 | app1 | ok | 50 | 35806ms | 55161ms | 59516ms |
| 100.0 | 111.0 | app2 | ok | 17 | 8036ms | 18667ms | 28867ms |
| 100.0 | 111.0 | end-users | ok | 165 | 1308ms | 2350ms | 4411ms |
| 111.0 | 121.0 | app1 | ok | 98 | 32778ms | 54556ms | 59456ms |
| 111.0 | 121.0 | app2 | ok | 34 | 7000ms | 9720ms | 26600ms |
| 111.0 | 121.0 | end-users | ok | 142 | 1106ms | 2306ms | 4290ms |
| 121.0 | 131.0 | app1 | ok | 56 | 40909ms | 56182ms | 59618ms |
| 121.0 | 131.0 | app2 | ok | 18 | 7000ms | 9400ms | 9940ms |
| 121.0 | 131.0 | end-users | ok | 107 | 1486ms | 3426ms | 4843ms |
| 131.0 | 141.0 | app1 | ok | 78 | 23000ms | 47000ms | 58700ms |
| 131.0 | 141.0 | app2 | ok | 27 | 5500ms | 9100ms | 9910ms |
| 131.0 | 141.0 | end-users | ok | 128 | 1484ms | 3545ms | 4855ms |
| 141.0 | 151.0 | app1 | ok | 63 | 20678ms | 29220ms | 55275ms |
| 141.0 | 151.0 | app2 | ok | 20 | 5000ms | 9000ms | 9900ms |
| 141.0 | 151.0 | end-users | ok | 149 | 2045ms | 4335ms | 4933ms |
| 151.0 | 161.0 | app1 | ok | 63 | 44250ms | 56850ms | 59685ms |
| 151.0 | 161.0 | app2 | ok | 21 | 7500ms | 9500ms | 9950ms |
| 151.0 | 161.0 | end-users | ok | 161 | 1132ms | 2269ms | 3658ms |
| 161.0 | 171.0 | app1 | ok | 74 | 23962ms | 49429ms | 58943ms |
| 161.0 | 171.0 | app2 | ok | 22 | 2500ms | 8429ms | 9843ms |
| 161.0 | 171.0 | end-users | ok | 80 | 3362ms | 4741ms | 8000ms |
| 171.0 | 181.0 | app1 | ok | 83 | 21067ms | 29920ms | 56888ms |
| 171.0 | 181.0 | app2 | ok | 30 | 5833ms | 9167ms | 9917ms |
| 171.0 | 181.0 | end-users | ok | 150 | 1533ms | 3558ms | 4856ms |
| 181.0 | 191.0 | app1 | ok | 75 | 20714ms | 29286ms | 55500ms |
| 181.0 | 191.0 | app2 | ok | 25 | 7500ms | 9881ms | 27500ms |
| 181.0 | 191.0 | end-users | ok | 126 | 1254ms | 2318ms | 4212ms |
| 191.0 | 201.0 | app1 | ok | 56 | 25135ms | 51158ms | 59116ms |
| 191.0 | 201.0 | app2 | ok | 19 | 7500ms | 9500ms | 9950ms |
| 191.0 | 201.0 | end-users | ok | 144 | 1175ms | 2297ms | 4100ms |
| 201.0 | 211.0 | app1 | ok | 54 | 44118ms | 56824ms | 59682ms |
| 201.0 | 211.0 | app2 | ok | 17 | 7500ms | 9500ms | 9950ms |
| 201.0 | 211.0 | end-users | ok | 122 | 1353ms | 2429ms | 4661ms |
| 211.0 | 221.0 | app1 | ok | 69 | 40833ms | 56167ms | 59617ms |
| 211.0 | 221.0 | app2 | ok | 23 | 7262ms | 9452ms | 9945ms |
| 211.0 | 221.0 | end-users | ok | 115 | 1041ms | 2295ms | 4281ms |
| 221.0 | 231.0 | app1 | ok | 100 | 23889ms | 49286ms | 58929ms |
| 221.0 | 231.0 | app2 | ok | 34 | 3676ms | 7875ms | 9787ms |
| 221.0 | 231.0 | end-users | ok | 121 | 3186ms | 4662ms | 4994ms |
| 231.0 | 241.0 | app1 | ok | 79 | 20000ms | 28000ms | 29800ms |
| 231.0 | 241.0 | app2 | ok | 26 | 4000ms | 8556ms | 9856ms |
| 231.0 | 241.0 | end-users | ok | 126 | 2617ms | 4586ms | 6850ms |
| 241.0 | 251.0 | app1 | ok | 197 | 20000ms | 28000ms | 29800ms |
| 241.0 | 251.0 | app2 | ok | 19 | 6607ms | 9321ms | 9932ms |
| 241.0 | 251.0 | end-users | ok | 26 | 1107ms | 2221ms | 2472ms |
| 251.0 | 261.0 | app1 | ok | 18 | 20000ms | 28000ms | 29800ms |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 268.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 268.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 268.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -11.8%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2400960 | 118957 | 2519917.0 | 0.0% | 2327954.0 | 2638874.0 | -11.8% | False |
| app2 | 735540 | 36437 | 771977.0 | 0.0% | 790808.0 | 808414.0 | -2.2% | True |
| end-users | 3821610 | 189768 | 4011378.0 | 0.0% | 4172804.0 | 4201146.0 | -0.7% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 1952 | 0 | 0 | 0 (never shed) | 0.00% | 30.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 598 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3107 | 0 | 0 | 0 (never shed) | 0.00% | 60.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5657). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5657 | 0.051ms | 0.115ms | (0, 0.1]ms | (0.1, 0.2]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 254017 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Per-tenant TTFT / ITL and the priority verdict (UNI-226)

`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming requests only) from the EPP's own framework-level histograms, fairness_id-labelled. Whole-run, from the same before/after snapshot pair the verdict above uses.

| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| app1 | ok | 1952 | 35381ms | 44038ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| app2 | ok | 598 | 12970ms | 18893ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| end-users | ok | 3107 | 4758ms | 7411ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |
| **pool (all groups)** | ok | 5657 | 6520ms | 42212ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a | n/a |

The pool row is the EPP-side number to compare against vLLM's own pool-level `vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, against live Prometheus, not by this script) -- a large gap between the two would point at EPP/gateway-added overhead, not vLLM's own prefill time.

**Secondary (priority) verdict: N/A (share already PASS)** -- secondary verdict only rescues a FAIL; primary verdict was not FAIL

**Windowed TTFT/ITL** (27 windows):

| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 2361ms | 3881ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | app2 | ok | 1000ms | 2700ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 0.0 | 10.0 | end-users | ok | 1917ms | 3633ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 10163ms | 14516ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | app2 | ok | 9154ms | 14250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 10.0 | 20.0 | end-users | ok | 5431ms | 7271ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app1 | ok | 17000ms | 26750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | app2 | ok | 10833ms | 14583ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 20.0 | 30.0 | end-users | ok | 4425ms | 7684ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app1 | ok | 27619ms | 42818ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | app2 | ok | 15625ms | 19562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 30.0 | 40.0 | end-users | ok | 4102ms | 5761ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | app2 | ok | 13026ms | 18562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 40.0 | 50.0 | end-users | ok | 4755ms | 5875ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | app2 | ok | 13667ms | 19214ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 50.0 | 60.0 | end-users | ok | 4615ms | 5863ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | app2 | ok | 12738ms | 17125ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 60.0 | 70.0 | end-users | ok | 4743ms | 5863ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 70.0 | 80.0 | end-users | ok | 6188ms | 7819ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | app2 | ok | 12875ms | 18083ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 80.0 | 90.0 | end-users | ok | 4658ms | 5850ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 90.0 | 100.0 | end-users | ok | 5583ms | 7541ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | app2 | ok | 15455ms | 19545ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 100.0 | 111.0 | end-users | ok | 4138ms | 5404ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | app2 | ok | 15625ms | 19562ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 111.0 | 121.0 | end-users | ok | 4875ms | 5948ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | app2 | ok | 13571ms | 19300ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 121.0 | 131.0 | end-users | ok | 4690ms | 7478ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | app2 | ok | 12647ms | 15500ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 131.0 | 141.0 | end-users | ok | 4733ms | 6188ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | app2 | ok | 14333ms | 19409ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 141.0 | 151.0 | end-users | ok | 5325ms | 7294ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | app2 | ok | 15278ms | 19528ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 151.0 | 161.0 | end-users | ok | 3899ms | 5817ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | app2 | ok | 14667ms | 19467ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 161.0 | 171.0 | end-users | ok | 5229ms | 7684ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | app2 | ok | 11618ms | 14926ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 171.0 | 181.0 | end-users | ok | 5324ms | 7862ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | app2 | ok | 13594ms | 19179ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 181.0 | 191.0 | end-users | ok | 4885ms | 7591ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | app2 | ok | 13088ms | 18688ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 191.0 | 201.0 | end-users | ok | 4595ms | 7532ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | app2 | ok | 14167ms | 19375ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 201.0 | 211.0 | end-users | ok | 4462ms | 5835ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | app2 | ok | 14821ms | 19481ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 211.0 | 221.0 | end-users | ok | 4432ms | 6800ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | app2 | ok | 13068ms | 18650ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 221.0 | 231.0 | end-users | ok | 5906ms | 7788ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app1 | ok | 37500ms | 44250ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 231.0 | 241.0 | end-users | ok | 5500ms | 8675ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app1 | ok | 32461ms | 43746ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | app2 | ok | 12100ms | 14710ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 241.0 | 251.0 | end-users | ok | 4450ms | 7772ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app1 | ok | 22714ms | 29271ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | app2 | ok | 12500ms | 14750ms | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 251.0 | 261.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 268.0 | app1 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 268.0 | app2 | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |
| 261.0 | 268.0 | end-users | no observations (e.g. ITL with STREAM_FRACTION=0 for this group) | n/a | n/a | not recorded (absent from both snapshots -- check the benchmark's scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`) | n/a | n/a |

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
