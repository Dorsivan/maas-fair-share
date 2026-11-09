# Fairness benchmark: twenty-group-scale (uni-167-h3-20group)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `twenty-group-scale` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-66847d4868-9rmdc` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-09T10:53:47Z` |
| Run end | `2026-11-09T10:54:42Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 5.0 | 50 | 0 | n/a | n/a | n/a | 29259.0 | 5.0% | 3.8% | -1.2 | 0.0% | -5.0 | 2.6s | 98.9% | 23.0 |
| app10 | 5.0 | 50 | 0 | n/a | n/a | n/a | 33303.0 | 5.0% | 4.3% | -0.7 | 0.0% | -5.0 | 2.6s | 98.9% | 27.0 |
| app11 | 5.0 | 50 | 0 | n/a | n/a | n/a | 40096.0 | 5.0% | 5.1% | 0.1 | 0.0% | -5.0 | 2.7s | 98.9% | 35.0 |
| app12 | 5.0 | 50 | 0 | n/a | n/a | n/a | 43512.0 | 5.0% | 5.6% | 0.6 | 0.0% | -5.0 | 2.7s | 98.9% | 33.0 |
| app13 | 5.0 | 50 | 0 | n/a | n/a | n/a | 36806.0 | 5.0% | 4.7% | -0.3 | 0.0% | -5.0 | 2.5s | 98.9% | 32.0 |
| app14 | 5.0 | 50 | 0 | n/a | n/a | n/a | 30325.0 | 5.0% | 3.9% | -1.1 | 0.0% | -5.0 | 2.5s | 98.9% | 23.0 |
| app15 | 5.0 | 50 | 0 | n/a | n/a | n/a | 48196.0 | 5.0% | 6.2% | 1.2 | 0.0% | -5.0 | 2.7s | 98.9% | 36.0 |
| app16 | 5.0 | 50 | 0 | n/a | n/a | n/a | 45193.0 | 5.0% | 5.8% | 0.8 | 0.0% | -5.0 | 2.5s | 98.9% | 36.0 |
| app17 | 5.0 | 50 | 0 | n/a | n/a | n/a | 38329.0 | 5.0% | 4.9% | -0.1 | 0.0% | -5.0 | 2.6s | 98.9% | 33.0 |
| app18 | 5.0 | 50 | 0 | n/a | n/a | n/a | 43805.0 | 5.0% | 5.6% | 0.6 | 0.0% | -5.0 | 2.5s | 98.9% | 39.0 |
| app19 | 5.0 | 50 | 0 | n/a | n/a | n/a | 41001.0 | 5.0% | 5.3% | 0.3 | 0.0% | -5.0 | 2.5s | 98.9% | 33.0 |
| app2 | 5.0 | 50 | 0 | n/a | n/a | n/a | 38682.0 | 5.0% | 5.0% | -0.0 | 0.0% | -5.0 | 2.6s | 98.9% | 28.0 |
| app20 | 5.0 | 50 | 0 | n/a | n/a | n/a | 44050.0 | 5.0% | 5.7% | 0.7 | 0.0% | -5.0 | 2.7s | 98.9% | 39.0 |
| app3 | 5.0 | 50 | 0 | n/a | n/a | n/a | 38756.0 | 5.0% | 5.0% | -0.0 | 0.0% | -5.0 | 2.6s | 98.9% | 29.0 |
| app4 | 5.0 | 50 | 0 | n/a | n/a | n/a | 37023.0 | 5.0% | 4.8% | -0.2 | 0.0% | -5.0 | 2.6s | 98.9% | 27.0 |
| app5 | 5.0 | 50 | 0 | n/a | n/a | n/a | 36961.0 | 5.0% | 4.7% | -0.3 | 0.0% | -5.0 | 2.5s | 98.9% | 32.0 |
| app6 | 5.0 | 50 | 0 | n/a | n/a | n/a | 37055.0 | 5.0% | 4.8% | -0.2 | 0.0% | -5.0 | 2.5s | 98.9% | 29.0 |
| app7 | 5.0 | 50 | 0 | n/a | n/a | n/a | 38297.0 | 5.0% | 4.9% | -0.1 | 0.0% | -5.0 | 2.5s | 98.9% | 29.0 |
| app8 | 5.0 | 50 | 0 | n/a | n/a | n/a | 35749.0 | 5.0% | 4.6% | -0.4 | 0.0% | -5.0 | 2.5s | 98.9% | 29.0 |
| app9 | 5.0 | 50 | 0 | n/a | n/a | n/a | 42786.0 | 5.0% | 5.5% | 0.5 | 0.0% | -5.0 | 2.7s | 98.9% | 33.0 |
| end-users | n/a | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 6756.0 | n/a | n/a | n/a | n/a | n/a | 0.1s | 98.9% | 5.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- app19: active 0s-240s, no duty cycle
- app8: active 0s-240s, no duty cycle
- app13: active 0s-240s, no duty cycle
- app10: active 0s-240s, no duty cycle
- app3: active 0s-240s, no duty cycle
- app4: active 0s-240s, no duty cycle
- app18: active 0s-240s, no duty cycle
- app14: active 0s-240s, no duty cycle
- app12: active 0s-240s, no duty cycle
- app17: active 0s-240s, no duty cycle
- app7: active 0s-240s, no duty cycle
- app20: active 0s-240s, no duty cycle
- app9: active 0s-240s, no duty cycle
- app15: active 0s-240s, no duty cycle
- app16: active 0s-240s, no duty cycle
- app6: active 0s-240s, no duty cycle
- app5: active 0s-240s, no duty cycle
- app11: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 0.0 | 0.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (6 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app2 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app19 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app8 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app13 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app10 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app3 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app4 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app18 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app14 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app12 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app17 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app7 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app20 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app9 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app15 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app16 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app6 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app5 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 0.0 | 10.0 | app11 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 10.0 | 20.0 | app1 | True | 6778.0 | 5.0% | 5.4% | 0.4 |
| 10.0 | 20.0 | app2 | True | 2716.0 | 5.0% | 2.2% | -2.8 |
| 10.0 | 20.0 | app19 | True | 9440.0 | 5.0% | 7.5% | 2.5 |
| 10.0 | 20.0 | app8 | True | 4062.0 | 5.0% | 3.2% | -1.8 |
| 10.0 | 20.0 | app13 | True | 5406.0 | 5.0% | 4.3% | -0.7 |
| 10.0 | 20.0 | app10 | True | 9492.0 | 5.0% | 7.5% | 2.5 |
| 10.0 | 20.0 | app3 | True | 5384.0 | 5.0% | 4.3% | -0.7 |
| 10.0 | 20.0 | app4 | True | 5400.0 | 5.0% | 4.3% | -0.7 |
| 10.0 | 20.0 | app18 | True | 10810.0 | 5.0% | 8.6% | 3.6 |
| 10.0 | 20.0 | app14 | True | 2716.0 | 5.0% | 2.2% | -2.8 |
| 10.0 | 20.0 | app12 | True | 8098.0 | 5.0% | 6.4% | 1.4 |
| 10.0 | 20.0 | app17 | True | 6774.0 | 5.0% | 5.4% | 0.4 |
| 10.0 | 20.0 | app7 | True | 9426.0 | 5.0% | 7.5% | 2.5 |
| 10.0 | 20.0 | app20 | True | 6754.0 | 5.0% | 5.4% | 0.4 |
| 10.0 | 20.0 | app9 | True | 4074.0 | 5.0% | 3.2% | -1.8 |
| 10.0 | 20.0 | app15 | True | 9458.0 | 5.0% | 7.5% | 2.5 |
| 10.0 | 20.0 | app16 | True | 10860.0 | 5.0% | 8.6% | 3.6 |
| 10.0 | 20.0 | app6 | True | 1342.0 | 5.0% | 1.1% | -3.9 |
| 10.0 | 20.0 | app5 | True | 4068.0 | 5.0% | 3.2% | -1.8 |
| 10.0 | 20.0 | app11 | True | 2716.0 | 5.0% | 2.2% | -2.8 |
| 20.0 | 30.0 | app1 | True | 9506.0 | 5.0% | 5.5% | 0.5 |
| 20.0 | 30.0 | app2 | True | 10822.0 | 5.0% | 6.3% | 1.3 |
| 20.0 | 30.0 | app19 | True | 6756.0 | 5.0% | 3.9% | -1.1 |
| 20.0 | 30.0 | app8 | True | 6750.0 | 5.0% | 3.9% | -1.1 |
| 20.0 | 30.0 | app13 | True | 6774.0 | 5.0% | 3.9% | -1.1 |
| 20.0 | 30.0 | app10 | True | 12172.0 | 5.0% | 7.0% | 2.0 |
| 20.0 | 30.0 | app3 | True | 6776.0 | 5.0% | 3.9% | -1.1 |
| 20.0 | 30.0 | app4 | True | 6736.0 | 5.0% | 3.9% | -1.1 |
| 20.0 | 30.0 | app18 | True | 8146.0 | 5.0% | 4.7% | -0.3 |
| 20.0 | 30.0 | app14 | True | 2712.0 | 5.0% | 1.6% | -3.4 |
| 20.0 | 30.0 | app12 | True | 9434.0 | 5.0% | 5.5% | 0.5 |
| 20.0 | 30.0 | app17 | True | 5358.0 | 5.0% | 3.1% | -1.9 |
| 20.0 | 30.0 | app7 | True | 4028.0 | 5.0% | 2.3% | -2.7 |
| 20.0 | 30.0 | app20 | True | 10840.0 | 5.0% | 6.3% | 1.3 |
| 20.0 | 30.0 | app9 | True | 12192.0 | 5.0% | 7.0% | 2.0 |
| 20.0 | 30.0 | app15 | True | 12200.0 | 5.0% | 7.1% | 2.1 |
| 20.0 | 30.0 | app16 | True | 10776.0 | 5.0% | 6.2% | 1.2 |
| 20.0 | 30.0 | app6 | True | 10818.0 | 5.0% | 6.3% | 1.3 |
| 20.0 | 30.0 | app5 | True | 9408.0 | 5.0% | 5.4% | 0.4 |
| 20.0 | 30.0 | app11 | True | 10832.0 | 5.0% | 6.3% | 1.3 |
| 30.0 | 40.0 | app1 | True | 8130.0 | 5.0% | 5.4% | 0.4 |
| 30.0 | 40.0 | app2 | True | 6732.0 | 5.0% | 4.4% | -0.6 |
| 30.0 | 40.0 | app19 | True | 8088.0 | 5.0% | 5.3% | 0.3 |
| 30.0 | 40.0 | app8 | True | 8116.0 | 5.0% | 5.4% | 0.4 |
| 30.0 | 40.0 | app13 | True | 6764.0 | 5.0% | 4.5% | -0.5 |
| 30.0 | 40.0 | app10 | True | 6758.0 | 5.0% | 4.5% | -0.5 |
| 30.0 | 40.0 | app3 | True | 6790.0 | 5.0% | 4.5% | -0.5 |
| 30.0 | 40.0 | app4 | True | 6734.0 | 5.0% | 4.4% | -0.6 |
| 30.0 | 40.0 | app18 | True | 8116.0 | 5.0% | 5.4% | 0.4 |
| 30.0 | 40.0 | app14 | True | 6774.0 | 5.0% | 4.5% | -0.5 |
| 30.0 | 40.0 | app12 | True | 8090.0 | 5.0% | 5.3% | 0.3 |
| 30.0 | 40.0 | app17 | True | 8060.0 | 5.0% | 5.3% | 0.3 |
| 30.0 | 40.0 | app7 | True | 6744.0 | 5.0% | 4.5% | -0.5 |
| 30.0 | 40.0 | app20 | True | 9486.0 | 5.0% | 6.3% | 1.3 |
| 30.0 | 40.0 | app9 | True | 9486.0 | 5.0% | 6.3% | 1.3 |
| 30.0 | 40.0 | app15 | True | 6762.0 | 5.0% | 4.5% | -0.5 |
| 30.0 | 40.0 | app16 | True | 6758.0 | 5.0% | 4.5% | -0.5 |
| 30.0 | 40.0 | app6 | True | 8116.0 | 5.0% | 5.4% | 0.4 |
| 30.0 | 40.0 | app5 | True | 6790.0 | 5.0% | 4.5% | -0.5 |
| 30.0 | 40.0 | app11 | True | 8122.0 | 5.0% | 5.4% | 0.4 |
| 40.0 | 50.0 | app1 | True | 4845.0 | 5.0% | 1.5% | -3.5 |
| 40.0 | 50.0 | app2 | True | 18412.0 | 5.0% | 5.6% | 0.6 |
| 40.0 | 50.0 | app19 | True | 16717.0 | 5.0% | 5.1% | 0.1 |
| 40.0 | 50.0 | app8 | True | 16821.0 | 5.0% | 5.1% | 0.1 |
| 40.0 | 50.0 | app13 | True | 17862.0 | 5.0% | 5.4% | 0.4 |
| 40.0 | 50.0 | app10 | True | 4881.0 | 5.0% | 1.5% | -3.5 |
| 40.0 | 50.0 | app3 | True | 19806.0 | 5.0% | 6.0% | 1.0 |
| 40.0 | 50.0 | app4 | True | 18153.0 | 5.0% | 5.5% | 0.5 |
| 40.0 | 50.0 | app18 | True | 16733.0 | 5.0% | 5.1% | 0.1 |
| 40.0 | 50.0 | app14 | True | 18123.0 | 5.0% | 5.5% | 0.5 |
| 40.0 | 50.0 | app12 | True | 17890.0 | 5.0% | 5.4% | 0.4 |
| 40.0 | 50.0 | app17 | True | 18137.0 | 5.0% | 5.5% | 0.5 |
| 40.0 | 50.0 | app7 | True | 18099.0 | 5.0% | 5.5% | 0.5 |
| 40.0 | 50.0 | app20 | True | 16970.0 | 5.0% | 5.2% | 0.2 |
| 40.0 | 50.0 | app9 | True | 17034.0 | 5.0% | 5.2% | 0.2 |
| 40.0 | 50.0 | app15 | True | 19776.0 | 5.0% | 6.0% | 1.0 |
| 40.0 | 50.0 | app16 | True | 16799.0 | 5.0% | 5.1% | 0.1 |
| 40.0 | 50.0 | app6 | True | 16779.0 | 5.0% | 5.1% | 0.1 |
| 40.0 | 50.0 | app5 | True | 16695.0 | 5.0% | 5.1% | 0.1 |
| 40.0 | 50.0 | app11 | True | 18426.0 | 5.0% | 5.6% | 0.6 |
| 50.0 | 55.0 | app1 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app2 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app19 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app8 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app13 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app10 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app3 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app4 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app18 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app14 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app12 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app17 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app7 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app20 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app9 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app15 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app16 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app6 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app5 | True | 0.0 | 5.0% | 0.0% | -5.0 |
| 50.0 | 55.0 | app11 | True | 0.0 | 5.0% | 0.0% | -5.0 |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app2 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app19 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app8 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app13 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app10 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app3 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app4 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app18 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app14 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app12 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app17 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app7 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app20 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app9 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app15 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app16 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app6 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 0.0 | 10.0 | app5 | ok | 1 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | app11 | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a |
| 10.0 | 20.0 | app1 | ok | 11 | 62ms | 975ms | 2335ms |
| 10.0 | 20.0 | app2 | ok | 9 | 175ms | 1825ms | 2432ms |
| 10.0 | 20.0 | app19 | ok | 14 | 100ms | 800ms | 2290ms |
| 10.0 | 20.0 | app8 | ok | 10 | 50ms | 1750ms | 2425ms |
| 10.0 | 20.0 | app13 | ok | 13 | 75ms | 675ms | 967ms |
| 10.0 | 20.0 | app10 | ok | 16 | 375ms | 1900ms | 2440ms |
| 10.0 | 20.0 | app3 | ok | 7 | 138ms | 412ms | 491ms |
| 10.0 | 20.0 | app4 | ok | 8 | 175ms | 1900ms | 2440ms |
| 10.0 | 20.0 | app18 | ok | 20 | 0ms | 500ms | 2350ms |
| 10.0 | 20.0 | app14 | ok | 4 | 0ms | 8ms | 10ms |
| 10.0 | 20.0 | app12 | ok | 13 | 145ms | 850ms | 2305ms |
| 10.0 | 20.0 | app17 | ok | 13 | 0ms | 1525ms | 2402ms |
| 10.0 | 20.0 | app7 | ok | 10 | 100ms | 250ms | 475ms |
| 10.0 | 20.0 | app20 | ok | 19 | 38ms | 1788ms | 2429ms |
| 10.0 | 20.0 | app9 | ok | 13 | 312ms | 963ms | 2305ms |
| 10.0 | 20.0 | app15 | ok | 16 | 175ms | 1700ms | 2420ms |
| 10.0 | 20.0 | app16 | ok | 17 | 125ms | 1990ms | 2449ms |
| 10.0 | 20.0 | app6 | ok | 10 | 0ms | 750ms | 975ms |
| 10.0 | 20.0 | app5 | ok | 12 | 25ms | 950ms | 2320ms |
| 10.0 | 20.0 | app11 | ok | 15 | 175ms | 2050ms | 2455ms |
| 20.0 | 30.0 | app1 | ok | 9 | 3438ms | 7750ms | 9775ms |
| 20.0 | 30.0 | app2 | ok | 8 | 6000ms | 9200ms | 9920ms |
| 20.0 | 30.0 | app19 | ok | 9 | 4375ms | 8500ms | 9850ms |
| 20.0 | 30.0 | app8 | ok | 9 | 5500ms | 9100ms | 9910ms |
| 20.0 | 30.0 | app13 | ok | 9 | 6250ms | 9250ms | 9925ms |
| 20.0 | 30.0 | app10 | ok | 8 | 2500ms | 8000ms | 9800ms |
| 20.0 | 30.0 | app3 | ok | 10 | 5000ms | 9000ms | 9900ms |
| 20.0 | 30.0 | app4 | ok | 8 | 7500ms | 9500ms | 9950ms |
| 20.0 | 30.0 | app18 | ok | 9 | 3906ms | 5500ms | 9550ms |
| 20.0 | 30.0 | app14 | ok | 8 | 7500ms | 9500ms | 9950ms |
| 20.0 | 30.0 | app12 | ok | 9 | 4688ms | 8875ms | 9888ms |
| 20.0 | 30.0 | app17 | ok | 9 | 4107ms | 7750ms | 9775ms |
| 20.0 | 30.0 | app7 | ok | 8 | 6000ms | 9200ms | 9920ms |
| 20.0 | 30.0 | app20 | ok | 9 | 4375ms | 8500ms | 9850ms |
| 20.0 | 30.0 | app9 | ok | 9 | 4750ms | 8875ms | 9888ms |
| 20.0 | 30.0 | app15 | ok | 9 | 4107ms | 7750ms | 9775ms |
| 20.0 | 30.0 | app16 | ok | 9 | 4375ms | 8500ms | 9850ms |
| 20.0 | 30.0 | app6 | ok | 9 | 4688ms | 8875ms | 9888ms |
| 20.0 | 30.0 | app5 | ok | 9 | 7188ms | 9438ms | 9944ms |
| 20.0 | 30.0 | app11 | ok | 9 | 6786ms | 9357ms | 9936ms |
| 30.0 | 40.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app19 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app8 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app13 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app10 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app18 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app14 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app12 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app17 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app7 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app20 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app9 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app15 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app16 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 30.0 | 40.0 | app11 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 40.0 | 50.0 | app1 | ok | 3 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app2 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app19 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app8 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app13 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app10 | ok | 3 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app3 | ok | 12 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app4 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app18 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app14 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app12 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app17 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app7 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app20 | ok | 11 | 19000ms | 27800ms | 29780ms |
| 40.0 | 50.0 | app9 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app15 | ok | 11 | 19000ms | 27800ms | 29780ms |
| 40.0 | 50.0 | app16 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app6 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app5 | ok | 10 | 20000ms | 28000ms | 29800ms |
| 40.0 | 50.0 | app11 | ok | 11 | 20000ms | 28000ms | 29800ms |
| 50.0 | 55.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app2 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app19 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app8 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app13 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app10 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app3 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app4 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app18 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app14 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app12 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app17 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app7 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app20 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app9 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app15 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app16 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app6 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app5 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 50.0 | 55.0 | app11 | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app2 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app3 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app4 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app5 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app6 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app7 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app8 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app9 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app10 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app11 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app12 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app13 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app14 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app15 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app16 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app17 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app18 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app19 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)
- app20 was offered load but has no client-side record (client-request-summary.jsonl is missing its line)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | n/a | n/a | n/a | n/a | 29259.0 | n/a | n/a | None |
| app2 | n/a | n/a | n/a | n/a | 38682.0 | n/a | n/a | None |
| app3 | n/a | n/a | n/a | n/a | 38756.0 | n/a | n/a | None |
| app4 | n/a | n/a | n/a | n/a | 37023.0 | n/a | n/a | None |
| app5 | n/a | n/a | n/a | n/a | 36961.0 | n/a | n/a | None |
| app6 | n/a | n/a | n/a | n/a | 37055.0 | n/a | n/a | None |
| app7 | n/a | n/a | n/a | n/a | 38297.0 | n/a | n/a | None |
| app8 | n/a | n/a | n/a | n/a | 35749.0 | n/a | n/a | None |
| app9 | n/a | n/a | n/a | n/a | 42786.0 | n/a | n/a | None |
| app10 | n/a | n/a | n/a | n/a | 33303.0 | n/a | n/a | None |
| app11 | n/a | n/a | n/a | n/a | 40096.0 | n/a | n/a | None |
| app12 | n/a | n/a | n/a | n/a | 43512.0 | n/a | n/a | None |
| app13 | n/a | n/a | n/a | n/a | 36806.0 | n/a | n/a | None |
| app14 | n/a | n/a | n/a | n/a | 30325.0 | n/a | n/a | None |
| app15 | n/a | n/a | n/a | n/a | 48196.0 | n/a | n/a | None |
| app16 | n/a | n/a | n/a | n/a | 45193.0 | n/a | n/a | None |
| app17 | n/a | n/a | n/a | n/a | 38329.0 | n/a | n/a | None |
| app18 | n/a | n/a | n/a | n/a | 43805.0 | n/a | n/a | None |
| app19 | n/a | n/a | n/a | n/a | 41001.0 | n/a | n/a | None |
| app20 | n/a | n/a | n/a | n/a | 44050.0 | n/a | n/a | None |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app2 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app3 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app4 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app5 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app6 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app7 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app8 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app9 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app10 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app11 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app12 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app13 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app14 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app15 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app16 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app17 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app18 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app19 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |
| app20 | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | 5.0% | n/a | n/a |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=630, EvictedContextCancelled=763). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 630 | 0.050ms | 0.100ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 53262 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
