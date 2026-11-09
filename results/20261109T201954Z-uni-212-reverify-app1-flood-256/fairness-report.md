# Fairness benchmark: app1-flood (uni-212-reverify-app1-flood-256)

**Verdict: FAIL** (threshold: 10 points)

- app1 deviated +41.7 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `app1-flood` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-59fc4f78c8-pjzsm` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T20:21:24Z` |
| Run end | `2026-11-09T20:25:47Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 30.0 | 256 | 4088 | 200=4074, 500=14 | 15.5 | 16.8 | 4650418.0 | 30.0% | 71.7% | 41.7 | 72.3% | 42.3 | 2.6s | 98.9% | 4072.0 |
| app2 | 10.0 | 32 | 500 | 200=497, 500=3 | 15.8 | 17.4 | 604306.0 | 10.0% | 9.3% | -0.7 | 8.8% | -1.2 | 2.1s | 98.9% | 497.0 |
| end-users | 60.0 | 64 | 1063 | 200=1060, 500=3 | 15.0 | 16.8 | 1234182.0 | 60.0% | 19.0% | -41.0 | 18.8% | -41.2 | 1.5s | 98.9% | 1060.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 2.0 |

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
| 0.0 | 10.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 0.0 | 10.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 0.0 | 10.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 10.0 | 20.0 | app1 | True | 0.0 | 30.0% | 0.0% | -30.0 |
| 10.0 | 20.0 | app2 | True | 0.0 | 10.0% | 0.0% | -10.0 |
| 10.0 | 20.0 | end-users | True | 0.0 | 60.0% | 0.0% | -60.0 |
| 20.0 | 30.0 | app1 | True | 22980.0 | 30.0% | 54.9% | 24.9 |
| 20.0 | 30.0 | app2 | True | 6750.0 | 10.0% | 16.1% | 6.1 |
| 20.0 | 30.0 | end-users | True | 12160.0 | 60.0% | 29.0% | -31.0 |
| 30.0 | 40.0 | app1 | True | 219026.0 | 30.0% | 73.0% | 43.0 |
| 30.0 | 40.0 | app2 | True | 22958.0 | 10.0% | 7.7% | -2.3 |
| 30.0 | 40.0 | end-users | True | 58114.0 | 60.0% | 19.4% | -40.6 |
| 40.0 | 50.0 | app1 | True | 225692.0 | 30.0% | 75.2% | 45.2 |
| 40.0 | 50.0 | app2 | True | 31154.0 | 10.0% | 10.4% | 0.4 |
| 40.0 | 50.0 | end-users | True | 43140.0 | 60.0% | 14.4% | -45.6 |
| 50.0 | 60.0 | app1 | True | 208240.0 | 30.0% | 69.7% | 39.7 |
| 50.0 | 60.0 | app2 | True | 33880.0 | 10.0% | 11.3% | 1.3 |
| 50.0 | 60.0 | end-users | True | 56766.0 | 60.0% | 19.0% | -41.0 |
| 60.0 | 70.0 | app1 | True | 221524.0 | 30.0% | 73.9% | 43.9 |
| 60.0 | 70.0 | app2 | True | 24348.0 | 10.0% | 8.1% | -1.9 |
| 60.0 | 70.0 | end-users | True | 54048.0 | 60.0% | 18.0% | -42.0 |
| 70.0 | 80.0 | app1 | True | 233730.0 | 30.0% | 77.2% | 47.2 |
| 70.0 | 80.0 | app2 | True | 26978.0 | 10.0% | 8.9% | -1.1 |
| 70.0 | 80.0 | end-users | True | 41914.0 | 60.0% | 13.9% | -46.1 |
| 80.0 | 90.0 | app1 | True | 204120.0 | 30.0% | 69.0% | 39.0 |
| 80.0 | 90.0 | app2 | True | 35114.0 | 10.0% | 11.9% | 1.9 |
| 80.0 | 90.0 | end-users | True | 56770.0 | 60.0% | 19.2% | -40.8 |
| 90.0 | 101.0 | app1 | True | 221542.0 | 30.0% | 73.9% | 43.9 |
| 90.0 | 101.0 | app2 | True | 21654.0 | 10.0% | 7.2% | -2.8 |
| 90.0 | 101.0 | end-users | True | 56766.0 | 60.0% | 18.9% | -41.1 |
| 101.0 | 111.0 | app1 | True | 178126.0 | 30.0% | 70.9% | 40.9 |
| 101.0 | 111.0 | app2 | True | 26980.0 | 10.0% | 10.7% | 0.7 |
| 101.0 | 111.0 | end-users | True | 46010.0 | 60.0% | 18.3% | -41.7 |
| 111.0 | 121.0 | app1 | True | 208138.0 | 30.0% | 69.7% | 39.7 |
| 111.0 | 121.0 | app2 | True | 31078.0 | 10.0% | 10.4% | 0.4 |
| 111.0 | 121.0 | end-users | True | 59610.0 | 60.0% | 19.9% | -40.1 |
| 121.0 | 131.0 | app1 | True | 207000.0 | 30.0% | 69.6% | 39.6 |
| 121.0 | 131.0 | app2 | True | 23062.0 | 10.0% | 7.7% | -2.3 |
| 121.0 | 131.0 | end-users | True | 67538.0 | 60.0% | 22.7% | -37.3 |
| 131.0 | 141.0 | app1 | True | 186662.0 | 30.0% | 75.4% | 45.4 |
| 131.0 | 141.0 | app2 | True | 25726.0 | 10.0% | 10.4% | 0.4 |
| 131.0 | 141.0 | end-users | True | 35098.0 | 60.0% | 14.2% | -45.8 |
| 141.0 | 151.0 | app1 | True | 166340.0 | 30.0% | 66.9% | 36.9 |
| 141.0 | 151.0 | app2 | True | 20286.0 | 10.0% | 8.2% | -1.8 |
| 141.0 | 151.0 | end-users | True | 62122.0 | 60.0% | 25.0% | -35.0 |
| 151.0 | 161.0 | app1 | True | 197428.0 | 30.0% | 66.7% | 36.7 |
| 151.0 | 161.0 | app2 | True | 32480.0 | 10.0% | 11.0% | 1.0 |
| 151.0 | 161.0 | end-users | True | 66128.0 | 60.0% | 22.3% | -37.7 |
| 161.0 | 171.0 | app1 | True | 200150.0 | 30.0% | 80.5% | 50.5 |
| 161.0 | 171.0 | app2 | True | 27008.0 | 10.0% | 10.9% | 0.9 |
| 161.0 | 171.0 | end-users | True | 21624.0 | 60.0% | 8.7% | -51.3 |
| 171.0 | 181.0 | app1 | True | 212264.0 | 30.0% | 71.0% | 41.0 |
| 171.0 | 181.0 | app2 | True | 22932.0 | 10.0% | 7.7% | -2.3 |
| 171.0 | 181.0 | end-users | True | 63604.0 | 60.0% | 21.3% | -38.7 |
| 181.0 | 191.0 | app1 | True | 183924.0 | 30.0% | 63.3% | 33.3 |
| 181.0 | 191.0 | app2 | True | 20280.0 | 10.0% | 7.0% | -3.0 |
| 181.0 | 191.0 | end-users | True | 86480.0 | 60.0% | 29.8% | -30.2 |
| 191.0 | 201.0 | app1 | True | 208210.0 | 30.0% | 81.5% | 51.5 |
| 191.0 | 201.0 | app2 | True | 28402.0 | 10.0% | 11.1% | 1.1 |
| 191.0 | 201.0 | end-users | True | 18950.0 | 60.0% | 7.4% | -52.6 |
| 201.0 | 211.0 | app1 | True | 200264.0 | 30.0% | 67.3% | 37.3 |
| 201.0 | 211.0 | app2 | True | 29764.0 | 10.0% | 10.0% | -0.0 |
| 201.0 | 211.0 | end-users | True | 67652.0 | 60.0% | 22.7% | -37.3 |
| 211.0 | 221.0 | app1 | True | 225934.0 | 30.0% | 76.6% | 46.6 |
| 211.0 | 221.0 | app2 | True | 27002.0 | 10.0% | 9.2% | -0.8 |
| 211.0 | 221.0 | end-users | True | 42000.0 | 60.0% | 14.2% | -45.8 |
| 221.0 | 231.0 | app1 | True | 229830.0 | 30.0% | 77.3% | 47.3 |
| 221.0 | 231.0 | app2 | True | 22996.0 | 10.0% | 7.7% | -2.3 |
| 221.0 | 231.0 | end-users | True | 44660.0 | 60.0% | 15.0% | -45.0 |
| 231.0 | 241.0 | app1 | True | 191750.0 | 30.0% | 64.2% | 34.2 |
| 231.0 | 241.0 | app2 | True | 20266.0 | 10.0% | 6.8% | -3.2 |
| 231.0 | 241.0 | end-users | True | 86524.0 | 60.0% | 29.0% | -31.0 |
| 241.0 | 251.0 | app1 | False | 254220.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 29768.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 20280.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 43324.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 13440.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 66224.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 204 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app2 | ok | 24 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 49 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 228 | 0ms | 942ms | 2329ms |
| 10.0 | 20.0 | app2 | ok | 28 | 0ms | 550ms | 2080ms |
| 10.0 | 20.0 | end-users | ok | 60 | 0ms | 900ms | 2320ms |
| 20.0 | 30.0 | app1 | ok | 162 | 755ms | 2081ms | 2458ms |
| 20.0 | 30.0 | app2 | ok | 22 | 722ms | 1950ms | 2445ms |
| 20.0 | 30.0 | end-users | ok | 42 | 731ms | 2050ms | 2455ms |
| 30.0 | 40.0 | app1 | ok | 183 | 837ms | 2102ms | 2460ms |
| 30.0 | 40.0 | app2 | ok | 22 | 1125ms | 2225ms | 2472ms |
| 30.0 | 40.0 | end-users | ok | 59 | 427ms | 1979ms | 2448ms |
| 40.0 | 50.0 | app1 | ok | 166 | 737ms | 2030ms | 2453ms |
| 40.0 | 50.0 | app2 | ok | 23 | 972ms | 2186ms | 2469ms |
| 40.0 | 50.0 | end-users | ok | 33 | 917ms | 2191ms | 2469ms |
| 50.0 | 60.0 | app1 | ok | 152 | 728ms | 2053ms | 2455ms |
| 50.0 | 60.0 | app2 | ok | 24 | 769ms | 1900ms | 2440ms |
| 50.0 | 60.0 | end-users | ok | 51 | 1029ms | 2206ms | 2471ms |
| 60.0 | 70.0 | app1 | ok | 162 | 792ms | 2088ms | 2459ms |
| 60.0 | 70.0 | app2 | ok | 18 | 750ms | 1960ms | 2446ms |
| 60.0 | 70.0 | end-users | ok | 48 | 938ms | 2187ms | 2469ms |
| 70.0 | 80.0 | app1 | ok | 175 | 778ms | 2062ms | 2456ms |
| 70.0 | 80.0 | app2 | ok | 22 | 875ms | 2133ms | 2463ms |
| 70.0 | 80.0 | end-users | ok | 33 | 281ms | 2088ms | 2459ms |
| 80.0 | 90.0 | app1 | ok | 154 | 755ms | 2064ms | 2456ms |
| 80.0 | 90.0 | app2 | ok | 26 | 750ms | 2110ms | 2461ms |
| 80.0 | 90.0 | end-users | ok | 50 | 833ms | 2105ms | 2461ms |
| 90.0 | 101.0 | app1 | ok | 161 | 785ms | 2110ms | 2461ms |
| 90.0 | 101.0 | app2 | ok | 16 | 1300ms | 2260ms | 2476ms |
| 90.0 | 101.0 | end-users | ok | 47 | 681ms | 1913ms | 2441ms |
| 101.0 | 111.0 | app1 | ok | 169 | 756ms | 2104ms | 2460ms |
| 101.0 | 111.0 | app2 | ok | 20 | 875ms | 2167ms | 2467ms |
| 101.0 | 111.0 | end-users | ok | 40 | 650ms | 1500ms | 2400ms |
| 111.0 | 121.0 | app1 | ok | 153 | 835ms | 2130ms | 2463ms |
| 111.0 | 121.0 | app2 | ok | 23 | 708ms | 2069ms | 2457ms |
| 111.0 | 121.0 | end-users | ok | 50 | 650ms | 1818ms | 2432ms |
| 121.0 | 131.0 | app1 | ok | 134 | 855ms | 2141ms | 2464ms |
| 121.0 | 131.0 | app2 | ok | 21 | 828ms | 1870ms | 2437ms |
| 121.0 | 131.0 | end-users | ok | 39 | 469ms | 1968ms | 2447ms |
| 131.0 | 141.0 | app1 | ok | 179 | 707ms | 1984ms | 2448ms |
| 131.0 | 141.0 | app2 | ok | 16 | 875ms | 2157ms | 2466ms |
| 131.0 | 141.0 | end-users | ok | 31 | 969ms | 2190ms | 2469ms |
| 141.0 | 151.0 | app1 | ok | 185 | 820ms | 2115ms | 2461ms |
| 141.0 | 151.0 | app2 | ok | 19 | 750ms | 2025ms | 2452ms |
| 141.0 | 151.0 | end-users | ok | 55 | 685ms | 1865ms | 2437ms |
| 151.0 | 161.0 | app1 | ok | 147 | 671ms | 1888ms | 2439ms |
| 151.0 | 161.0 | app2 | ok | 24 | 1115ms | 2223ms | 2472ms |
| 151.0 | 161.0 | end-users | ok | 53 | 981ms | 2194ms | 2469ms |
| 161.0 | 171.0 | app1 | ok | 193 | 811ms | 2114ms | 2461ms |
| 161.0 | 171.0 | app2 | ok | 21 | 750ms | 1870ms | 2437ms |
| 161.0 | 171.0 | end-users | ok | 15 | 536ms | 964ms | 2275ms |
| 171.0 | 181.0 | app1 | ok | 151 | 734ms | 2056ms | 2456ms |
| 171.0 | 181.0 | app2 | ok | 17 | 969ms | 2181ms | 2468ms |
| 171.0 | 181.0 | end-users | ok | 49 | 922ms | 2166ms | 2467ms |
| 181.0 | 191.0 | app1 | ok | 156 | 762ms | 2103ms | 2460ms |
| 181.0 | 191.0 | app2 | ok | 15 | 694ms | 1375ms | 2387ms |
| 181.0 | 191.0 | end-users | ok | 64 | 658ms | 1995ms | 2449ms |
| 191.0 | 201.0 | app1 | ok | 187 | 795ms | 2105ms | 2460ms |
| 191.0 | 201.0 | app2 | ok | 22 | 600ms | 1400ms | 2390ms |
| 191.0 | 201.0 | end-users | ok | 14 | 500ms | 2150ms | 2465ms |
| 201.0 | 211.0 | app1 | ok | 159 | 827ms | 2139ms | 2464ms |
| 201.0 | 211.0 | app2 | ok | 22 | 688ms | 1950ms | 2445ms |
| 201.0 | 211.0 | end-users | ok | 50 | 775ms | 2031ms | 2453ms |
| 211.0 | 221.0 | app1 | ok | 175 | 804ms | 2077ms | 2458ms |
| 211.0 | 221.0 | app2 | ok | 20 | 786ms | 2071ms | 2457ms |
| 211.0 | 221.0 | end-users | ok | 29 | 292ms | 2017ms | 2452ms |
| 221.0 | 231.0 | app1 | ok | 141 | 839ms | 2129ms | 2463ms |
| 221.0 | 231.0 | app2 | ok | 16 | 417ms | 867ms | 987ms |
| 221.0 | 231.0 | end-users | ok | 35 | 917ms | 2172ms | 2467ms |
| 231.0 | 241.0 | app1 | ok | 151 | 853ms | 2135ms | 2463ms |
| 231.0 | 241.0 | app2 | ok | 16 | 750ms | 1900ms | 2440ms |
| 231.0 | 241.0 | end-users | ok | 64 | 714ms | 2100ms | 2460ms |
| 241.0 | 251.0 | app1 | ok | 45 | 938ms | 2179ms | 2468ms |
| 241.0 | 251.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 263.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 261.0 | 263.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: cost -15.6%
- app2 exceeded the 10% ledger tolerance: cost -10.1%
- end-users exceeded the 10% ledger tolerance: cost -13.9%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 5011020 | 248072 | 5256504.0 | -0.0% | 4650418.0 | 5507164.0 | -15.6% | False |
| app2 | 611310 | 30299 | 641609.0 | 0.0% | 604306.0 | 671908.0 | -10.1% | False |
| end-users | 1303800 | 64645 | 1368445.0 | 0.0% | 1234182.0 | 1433090.0 | -13.9% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 4088 | 0 | 0 | 0 (never shed) | 0.00% | 30.0% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 500 | 0 | 0 | 0 (never shed) | 0.00% | 10.0% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 1063 | 0 | 0 | 0 (never shed) | 0.00% | 60.0% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5631). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5631 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 253594 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
