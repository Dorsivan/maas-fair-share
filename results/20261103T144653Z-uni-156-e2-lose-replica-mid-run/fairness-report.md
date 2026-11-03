# Fairness benchmark: full-contention (uni-156-e2-lose-replica-mid-run)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `360` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-6l4c9` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-03T14:48:05Z` |
| Run end | `2026-11-03T14:56:59Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 870 | 000=1, 200=846, 500=23 | 13.2 | 22.8 | 1116933.0 | 21.1% | 18.7% | -2.3 | 18.7% | -2.3 | 53.0s | 98.9% | 847.0 |
| app2 | 10.0 | 32 | 567 | 200=545, 500=22 | 25.5 | 27.5 | 713102.0 | 10.5% | 12.0% | 1.4 | 12.2% | 1.7 | 53.1s | 98.9% | 545.0 |
| end-users | 65.0 | 128 | 3204 | 200=3126, 500=78 | 16.5 | 17.9 | 4129656.0 | 68.4% | 69.3% | 0.9 | 69.0% | 0.6 | 53.1s | 98.9% | 3117.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 12156.0 | n/a | n/a | n/a | n/a | n/a | 0.0s | 98.9% | 9.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events (scheduled):**
- t+120s: scale_down (target=maas-vllm-gpu, to=1)
- t+360s: scale_restore (target=maas-vllm-gpu)

**Per-tenant schedule:**
- app1: active 0s-360s, no duty cycle
- app2: active 0s-360s, no duty cycle
- end-users: active 0s-360s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 120.0 | 140.0 | 20.0 |
| 360.0 | n/a (never converged in this phase) | n/a |

**Windows** (54 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 5420.0 | 21.1% | 9.8% | -11.3 |
| 0.0 | 10.0 | app2 | True | 13524.0 | 10.5% | 24.4% | 13.9 |
| 0.0 | 10.0 | end-users | True | 36474.0 | 68.4% | 65.8% | -2.6 |
| 10.0 | 20.0 | app1 | True | 22962.0 | 21.1% | 13.0% | -8.1 |
| 10.0 | 20.0 | app2 | True | 21584.0 | 10.5% | 12.2% | 1.7 |
| 10.0 | 20.0 | end-users | True | 132578.0 | 68.4% | 74.9% | 6.4 |
| 20.0 | 30.0 | app1 | True | 33722.0 | 21.1% | 20.4% | -0.6 |
| 20.0 | 30.0 | app2 | True | 18900.0 | 10.5% | 11.5% | 0.9 |
| 20.0 | 30.0 | end-users | True | 112358.0 | 68.4% | 68.1% | -0.3 |
| 30.0 | 40.0 | app1 | True | 29722.0 | 21.1% | 19.4% | -1.6 |
| 30.0 | 40.0 | app2 | True | 16240.0 | 10.5% | 10.6% | 0.1 |
| 30.0 | 40.0 | end-users | True | 106886.0 | 68.4% | 69.9% | 1.5 |
| 40.0 | 50.0 | app1 | True | 28330.0 | 21.1% | 16.6% | -4.4 |
| 40.0 | 50.0 | app2 | True | 32454.0 | 10.5% | 19.0% | 8.5 |
| 40.0 | 50.0 | end-users | True | 109656.0 | 68.4% | 64.3% | -4.1 |
| 50.0 | 60.0 | app1 | True | 33828.0 | 21.1% | 20.0% | -1.1 |
| 50.0 | 60.0 | app2 | True | 20294.0 | 10.5% | 12.0% | 1.5 |
| 50.0 | 60.0 | end-users | True | 115030.0 | 68.4% | 68.0% | -0.4 |
| 60.0 | 70.0 | app1 | True | 18950.0 | 21.1% | 10.9% | -10.2 |
| 60.0 | 70.0 | app2 | True | 21660.0 | 10.5% | 12.4% | 1.9 |
| 60.0 | 70.0 | end-users | True | 133816.0 | 68.4% | 76.7% | 8.3 |
| 70.0 | 80.0 | app1 | True | 20270.0 | 21.1% | 13.4% | -7.7 |
| 70.0 | 80.0 | app2 | True | 21638.0 | 10.5% | 14.3% | 3.8 |
| 70.0 | 80.0 | end-users | True | 109654.0 | 68.4% | 72.3% | 3.9 |
| 80.0 | 90.0 | app1 | True | 43250.0 | 21.1% | 25.2% | 4.1 |
| 80.0 | 90.0 | app2 | True | 43324.0 | 10.5% | 25.2% | 14.7 |
| 80.0 | 90.0 | end-users | True | 85130.0 | 68.4% | 49.6% | -18.8 |
| 90.0 | 100.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 90.0 | 100.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 90.0 | 100.0 | end-users | True | 166350.0 | 68.4% | 100.0% | 31.6 |
| 100.0 | 110.0 | app1 | True | 46028.0 | 21.1% | 27.6% | 6.6 |
| 100.0 | 110.0 | app2 | True | 52810.0 | 10.5% | 31.7% | 21.2 |
| 100.0 | 110.0 | end-users | True | 67686.0 | 68.4% | 40.6% | -27.8 |
| 110.0 | 120.0 | app1 | True | 27052.0 | 21.1% | 17.4% | -3.7 |
| 110.0 | 120.0 | app2 | True | 5392.0 | 10.5% | 3.5% | -7.1 |
| 110.0 | 120.0 | end-users | True | 123120.0 | 68.4% | 79.1% | 10.7 |
| 120.0 | 130.0 | app1 | True | 47324.0 | 21.1% | 19.7% | -1.4 |
| 120.0 | 130.0 | app2 | True | 13498.0 | 10.5% | 5.6% | -4.9 |
| 120.0 | 130.0 | end-users | True | 179886.0 | 68.4% | 74.7% | 6.3 |
| 130.0 | 140.0 | app1 | True | 14870.0 | 21.1% | 6.1% | -15.0 |
| 130.0 | 140.0 | app2 | True | 35212.0 | 10.5% | 14.4% | 3.8 |
| 130.0 | 140.0 | end-users | True | 194928.0 | 68.4% | 79.6% | 11.1 |
| 140.0 | 150.0 | app1 | True | 29816.0 | 21.1% | 19.9% | -1.2 |
| 140.0 | 150.0 | app2 | True | 16212.0 | 10.5% | 10.8% | 0.3 |
| 140.0 | 150.0 | end-users | True | 104088.0 | 68.4% | 69.3% | 0.9 |
| 150.0 | 160.0 | app1 | True | 32476.0 | 21.1% | 21.2% | 0.2 |
| 150.0 | 160.0 | app2 | True | 16250.0 | 10.5% | 10.6% | 0.1 |
| 150.0 | 160.0 | end-users | True | 104220.0 | 68.4% | 68.1% | -0.3 |
| 160.0 | 170.0 | app1 | True | 31074.0 | 21.1% | 20.5% | -0.5 |
| 160.0 | 170.0 | app2 | True | 16218.0 | 10.5% | 10.7% | 0.2 |
| 160.0 | 170.0 | end-users | True | 104118.0 | 68.4% | 68.8% | 0.3 |
| 170.0 | 180.0 | app1 | True | 33800.0 | 21.1% | 22.1% | 1.1 |
| 170.0 | 180.0 | app2 | True | 14918.0 | 10.5% | 9.8% | -0.8 |
| 170.0 | 180.0 | end-users | True | 104064.0 | 68.4% | 68.1% | -0.3 |
| 180.0 | 190.0 | app1 | True | 29846.0 | 21.1% | 20.0% | -1.0 |
| 180.0 | 190.0 | app2 | True | 16226.0 | 10.5% | 10.9% | 0.4 |
| 180.0 | 190.0 | end-users | True | 102844.0 | 68.4% | 69.1% | 0.6 |
| 190.0 | 200.0 | app1 | True | 32492.0 | 21.1% | 21.6% | 0.6 |
| 190.0 | 200.0 | app2 | True | 16286.0 | 10.5% | 10.8% | 0.3 |
| 190.0 | 200.0 | end-users | True | 101588.0 | 68.4% | 67.6% | -0.9 |
| 200.0 | 210.0 | app1 | True | 29716.0 | 21.1% | 19.8% | -1.3 |
| 200.0 | 210.0 | app2 | True | 17568.0 | 10.5% | 11.7% | 1.2 |
| 200.0 | 210.0 | end-users | True | 102906.0 | 68.4% | 68.5% | 0.1 |
| 210.0 | 220.0 | app1 | True | 32466.0 | 21.1% | 21.6% | 0.6 |
| 210.0 | 220.0 | app2 | True | 16284.0 | 10.5% | 10.8% | 0.3 |
| 210.0 | 220.0 | end-users | True | 101498.0 | 68.4% | 67.6% | -0.9 |
| 220.0 | 230.0 | app1 | True | 31090.0 | 21.1% | 20.2% | -0.9 |
| 220.0 | 230.0 | app2 | True | 14878.0 | 10.5% | 9.7% | -0.9 |
| 220.0 | 230.0 | end-users | True | 108146.0 | 68.4% | 70.2% | 1.8 |
| 230.0 | 240.0 | app1 | True | 32382.0 | 21.1% | 21.0% | -0.0 |
| 230.0 | 240.0 | app2 | True | 16234.0 | 10.5% | 10.5% | 0.0 |
| 230.0 | 240.0 | end-users | True | 105352.0 | 68.4% | 68.4% | 0.0 |
| 240.0 | 250.0 | app1 | True | 32502.0 | 21.1% | 21.3% | 0.2 |
| 240.0 | 250.0 | app2 | True | 16214.0 | 10.5% | 10.6% | 0.1 |
| 240.0 | 250.0 | end-users | True | 104078.0 | 68.4% | 68.1% | -0.3 |
| 250.0 | 260.0 | app1 | True | 31148.0 | 21.1% | 20.9% | -0.1 |
| 250.0 | 260.0 | app2 | True | 16226.0 | 10.5% | 10.9% | 0.4 |
| 250.0 | 260.0 | end-users | True | 101514.0 | 68.4% | 68.2% | -0.2 |
| 260.0 | 270.0 | app1 | True | 32410.0 | 21.1% | 21.0% | -0.0 |
| 260.0 | 270.0 | app2 | True | 14892.0 | 10.5% | 9.7% | -0.9 |
| 260.0 | 270.0 | end-users | True | 106906.0 | 68.4% | 69.3% | 0.9 |
| 270.0 | 280.0 | app1 | True | 32428.0 | 21.1% | 21.4% | 0.4 |
| 270.0 | 280.0 | app2 | True | 16262.0 | 10.5% | 10.7% | 0.2 |
| 270.0 | 280.0 | end-users | True | 102758.0 | 68.4% | 67.9% | -0.6 |
| 280.0 | 291.0 | app1 | True | 33786.0 | 21.1% | 22.3% | 1.3 |
| 280.0 | 291.0 | app2 | True | 16250.0 | 10.5% | 10.7% | 0.2 |
| 280.0 | 291.0 | end-users | True | 101364.0 | 68.4% | 67.0% | -1.5 |
| 291.0 | 301.0 | app1 | True | 31012.0 | 21.1% | 20.3% | -0.8 |
| 291.0 | 301.0 | app2 | True | 16244.0 | 10.5% | 10.6% | 0.1 |
| 291.0 | 301.0 | end-users | True | 105670.0 | 68.4% | 69.1% | 0.7 |
| 301.0 | 311.0 | app1 | True | 32456.0 | 21.1% | 21.2% | 0.2 |
| 301.0 | 311.0 | app2 | True | 16234.0 | 10.5% | 10.6% | 0.1 |
| 301.0 | 311.0 | end-users | True | 104116.0 | 68.4% | 68.1% | -0.3 |
| 311.0 | 321.0 | app1 | True | 31056.0 | 21.1% | 20.3% | -0.7 |
| 311.0 | 321.0 | app2 | True | 16244.0 | 10.5% | 10.6% | 0.1 |
| 311.0 | 321.0 | end-users | True | 105500.0 | 68.4% | 69.0% | 0.6 |
| 321.0 | 331.0 | app1 | True | 33720.0 | 21.1% | 22.3% | 1.2 |
| 321.0 | 331.0 | app2 | True | 14906.0 | 10.5% | 9.8% | -0.7 |
| 321.0 | 331.0 | end-users | True | 102706.0 | 68.4% | 67.9% | -0.6 |
| 331.0 | 341.0 | app1 | True | 31084.0 | 21.1% | 19.8% | -1.2 |
| 331.0 | 341.0 | app2 | True | 17588.0 | 10.5% | 11.2% | 0.7 |
| 331.0 | 341.0 | end-users | True | 108014.0 | 68.4% | 68.9% | 0.5 |
| 341.0 | 351.0 | app1 | True | 31110.0 | 21.1% | 20.9% | -0.2 |
| 341.0 | 351.0 | app2 | True | 16238.0 | 10.5% | 10.9% | 0.4 |
| 341.0 | 351.0 | end-users | True | 101538.0 | 68.4% | 68.2% | -0.2 |
| 351.0 | 361.0 | app1 | True | 33806.0 | 21.1% | 22.1% | 1.1 |
| 351.0 | 361.0 | app2 | True | 14846.0 | 10.5% | 9.7% | -0.8 |
| 351.0 | 361.0 | end-users | True | 104114.0 | 68.4% | 68.2% | -0.3 |
| 361.0 | 371.0 | app1 | False | 31100.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | 16296.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | False | 102810.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | 10808.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | 27058.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | False | 66192.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 381.0 | 391.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 391.0 | 401.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 401.0 | 411.0 | end-users | False | 0.0 | n/a | n/a | n/a |
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
| 491.0 | 501.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 511.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 511.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 501.0 | 511.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 511.0 | 521.0 | app1 | False | 1621.0 | n/a | n/a | n/a |
| 511.0 | 521.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 511.0 | 521.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 521.0 | 531.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 521.0 | 531.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 521.0 | 531.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 531.0 | 534.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 531.0 | 534.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 531.0 | 534.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 1040580 | 51594 | 1092174.0 | 0.0% | 1116933.0 | 1143768.0 | -2.3% | True |
| app2 | 670350 | 33540 | 703890.0 | 0.0% | 713102.0 | 737430.0 | -3.3% | True |
| end-users | 3844980 | 191686 | 4025053.0 | -0.3% | 4129656.0 | 4228352.0 | -2.3% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 870 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 567 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3204 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=4518). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 511842 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
