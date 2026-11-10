# Fairness benchmark: app2-idle-discriminating (uni-225-app2-idle-discriminating)

**Verdict: FAIL** (threshold: 10 points)
Worker-share vs. weight-share gap (UNI-225): 31.6 points

- app1 deviated +20.0 points from its contention-adjusted expected share, exceeding the 10-point threshold

## Run metadata

| field | value |
|---|---|
| Scenario | `app2-idle-discriminating` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:617509368126be65fa398904f5c4143d967a21663e706ad21fc959cba032e091` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-85575669d6-n28df` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-10T14:41:30Z` |
| Run end | `2026-11-10T14:45:52Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output). `worker share %`/`worker-vs-weight gap (pts)` (UNI-225) compare this group's share of the offered worker count/rate against its own `expected %` (weight share) -- a small gap here means this row's sizing cannot distinguish 'the split follows the weights' from 'the split follows the workers', regardless of what the observed split did; see the verdict line above and the module docstring.

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 128 | 2474 | 200=2415, 500=59 | 12.7 | 18.1 | 3006292.0 | 23.5% | 55.2% | 31.6 | 43.5% | 20.0 | 44.5% | 21.0 | 47.6s | 98.9% | 2404.0 |
| app2 | 10.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| end-users | 65.0 | 104 | 3081 | 200=3024, 500=57 | 7.5 | 12.7 | 3900446.0 | 76.5% | 44.8% | -31.6 | 56.5% | -20.0 | 55.5% | -21.0 | 47.6s | 98.9% | 3017.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 98.9% | 18.0 |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events:** none configured for this run.

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | 230.0 | 230.0 |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (27 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 0.0 | 23.5% | 0.0% | -23.5 |
| 0.0 | 10.0 | end-users | True | 0.0 | 76.5% | 0.0% | -76.5 |
| 10.0 | 20.0 | app1 | True | 20186.0 | 23.5% | 49.9% | 26.4 |
| 10.0 | 20.0 | end-users | True | 20256.0 | 76.5% | 50.1% | -26.4 |
| 20.0 | 30.0 | app1 | True | 158208.0 | 23.5% | 51.8% | 28.2 |
| 20.0 | 30.0 | end-users | True | 147360.0 | 76.5% | 48.2% | -28.2 |
| 30.0 | 40.0 | app1 | True | 102672.0 | 23.5% | 33.5% | 9.9 |
| 30.0 | 40.0 | end-users | True | 204162.0 | 76.5% | 66.5% | -9.9 |
| 40.0 | 50.0 | app1 | True | 102854.0 | 23.5% | 33.6% | 10.1 |
| 40.0 | 50.0 | end-users | True | 202902.0 | 76.5% | 66.4% | -10.1 |
| 50.0 | 60.0 | app1 | True | 116368.0 | 23.5% | 42.0% | 18.4 |
| 50.0 | 60.0 | end-users | True | 160996.0 | 76.5% | 58.0% | -18.4 |
| 60.0 | 70.0 | app1 | True | 114762.0 | 23.5% | 37.2% | 13.7 |
| 60.0 | 70.0 | end-users | True | 193446.0 | 76.5% | 62.8% | -13.7 |
| 70.0 | 80.0 | app1 | True | 102812.0 | 23.5% | 34.2% | 10.7 |
| 70.0 | 80.0 | end-users | True | 197690.0 | 76.5% | 65.8% | -10.7 |
| 80.0 | 90.0 | app1 | True | 112260.0 | 23.5% | 37.0% | 13.5 |
| 80.0 | 90.0 | end-users | True | 190740.0 | 76.5% | 63.0% | -13.5 |
| 90.0 | 100.0 | app1 | True | 112188.0 | 23.5% | 36.7% | 13.2 |
| 90.0 | 100.0 | end-users | True | 193480.0 | 76.5% | 63.3% | -13.2 |
| 100.0 | 110.0 | app1 | True | 101484.0 | 23.5% | 33.6% | 10.1 |
| 100.0 | 110.0 | end-users | True | 200260.0 | 76.5% | 66.4% | -10.1 |
| 110.0 | 120.0 | app1 | True | 98590.0 | 23.5% | 34.7% | 11.2 |
| 110.0 | 120.0 | end-users | True | 185314.0 | 76.5% | 65.3% | -11.2 |
| 120.0 | 130.0 | app1 | True | 177192.0 | 23.5% | 60.7% | 37.1 |
| 120.0 | 130.0 | end-users | True | 114828.0 | 76.5% | 39.3% | -37.1 |
| 130.0 | 140.0 | app1 | True | 165238.0 | 23.5% | 55.0% | 31.4 |
| 130.0 | 140.0 | end-users | True | 135414.0 | 76.5% | 45.0% | -31.4 |
| 140.0 | 150.0 | app1 | True | 117498.0 | 23.5% | 38.0% | 14.5 |
| 140.0 | 150.0 | end-users | True | 191802.0 | 76.5% | 62.0% | -14.5 |
| 150.0 | 160.0 | app1 | True | 116396.0 | 23.5% | 38.9% | 15.4 |
| 150.0 | 160.0 | end-users | True | 182658.0 | 76.5% | 61.1% | -15.4 |
| 160.0 | 170.0 | app1 | True | 112212.0 | 23.5% | 38.4% | 14.9 |
| 160.0 | 170.0 | end-users | True | 179696.0 | 76.5% | 61.6% | -14.9 |
| 170.0 | 180.0 | app1 | True | 166364.0 | 23.5% | 57.2% | 33.7 |
| 170.0 | 180.0 | end-users | True | 124462.0 | 76.5% | 42.8% | -33.7 |
| 180.0 | 190.0 | app1 | True | 142132.0 | 23.5% | 48.9% | 25.3 |
| 180.0 | 190.0 | end-users | True | 148772.0 | 76.5% | 51.1% | -25.3 |
| 190.0 | 200.0 | app1 | True | 182484.0 | 23.5% | 64.9% | 41.4 |
| 190.0 | 200.0 | end-users | True | 98746.0 | 76.5% | 35.1% | -41.4 |
| 200.0 | 210.0 | app1 | True | 115008.0 | 23.5% | 38.9% | 15.3 |
| 200.0 | 210.0 | end-users | True | 181018.0 | 76.5% | 61.1% | -15.3 |
| 210.0 | 220.0 | app1 | True | 146030.0 | 23.5% | 49.5% | 26.0 |
| 210.0 | 220.0 | end-users | True | 148778.0 | 76.5% | 50.5% | -26.0 |
| 220.0 | 230.0 | app1 | True | 159618.0 | 23.5% | 52.9% | 29.4 |
| 220.0 | 230.0 | end-users | True | 141946.0 | 76.5% | 47.1% | -29.4 |
| 230.0 | 240.0 | app1 | True | 91996.0 | 23.5% | 30.0% | 6.4 |
| 230.0 | 240.0 | end-users | True | 215132.0 | 76.5% | 70.0% | -6.4 |
| 240.0 | 250.0 | app1 | False | 164960.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 137874.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 6780.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 2714.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | False | 0.0 | n/a | n/a | n/a |

**Flow-control queue wait, dispatched requests only** (`llm_d_epp_flow_control_request_queue_duration_seconds`, `outcome="Dispatched"`):

| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | ok | 72 | 0ms | 0ms | 0ms |
| 0.0 | 10.0 | end-users | ok | 53 | 0ms | 0ms | 0ms |
| 10.0 | 20.0 | app1 | ok | 166 | 0ms | 610ms | 984ms |
| 10.0 | 20.0 | end-users | ok | 139 | 0ms | 740ms | 1805ms |
| 20.0 | 30.0 | app1 | ok | 82 | 2667ms | 6846ms | 9685ms |
| 20.0 | 30.0 | end-users | ok | 123 | 2175ms | 4385ms | 4938ms |
| 30.0 | 40.0 | app1 | ok | 105 | 8547ms | 23226ms | 29323ms |
| 30.0 | 40.0 | end-users | ok | 170 | 1983ms | 4213ms | 4921ms |
| 40.0 | 50.0 | app1 | ok | 66 | 18814ms | 27763ms | 29776ms |
| 40.0 | 50.0 | end-users | ok | 137 | 1873ms | 4099ms | 4910ms |
| 50.0 | 60.0 | app1 | ok | 100 | 8968ms | 24595ms | 29459ms |
| 50.0 | 60.0 | end-users | ok | 122 | 2333ms | 4684ms | 8983ms |
| 60.0 | 70.0 | app1 | ok | 59 | 8882ms | 24381ms | 29438ms |
| 60.0 | 70.0 | end-users | ok | 134 | 1762ms | 4288ms | 8325ms |
| 70.0 | 80.0 | app1 | ok | 86 | 18219ms | 27644ms | 29764ms |
| 70.0 | 80.0 | end-users | ok | 135 | 1930ms | 4135ms | 4913ms |
| 80.0 | 90.0 | app1 | ok | 80 | 19474ms | 27895ms | 29789ms |
| 80.0 | 90.0 | end-users | ok | 172 | 2000ms | 4218ms | 4922ms |
| 90.0 | 100.0 | app1 | ok | 73 | 19861ms | 27972ms | 29797ms |
| 90.0 | 100.0 | end-users | ok | 123 | 2096ms | 4301ms | 4930ms |
| 100.0 | 110.0 | app1 | ok | 97 | 17403ms | 27481ms | 29748ms |
| 100.0 | 110.0 | end-users | ok | 176 | 2000ms | 4302ms | 4930ms |
| 110.0 | 120.0 | app1 | ok | 128 | 7639ms | 21467ms | 29147ms |
| 110.0 | 120.0 | end-users | ok | 73 | 2992ms | 6350ms | 9635ms |
| 120.0 | 130.0 | app1 | ok | 95 | 4216ms | 8362ms | 9836ms |
| 120.0 | 130.0 | end-users | ok | 104 | 6176ms | 9235ms | 9924ms |
| 130.0 | 140.0 | app1 | ok | 93 | 6941ms | 9388ms | 9939ms |
| 130.0 | 140.0 | end-users | ok | 120 | 4364ms | 8667ms | 9867ms |
| 140.0 | 150.0 | app1 | ok | 79 | 8292ms | 21684ms | 29168ms |
| 140.0 | 150.0 | end-users | ok | 148 | 2204ms | 4383ms | 4938ms |
| 150.0 | 160.0 | app1 | ok | 85 | 18667ms | 27733ms | 29773ms |
| 150.0 | 160.0 | end-users | ok | 132 | 2008ms | 4267ms | 4927ms |
| 160.0 | 170.0 | app1 | ok | 104 | 8448ms | 23882ms | 29388ms |
| 160.0 | 170.0 | end-users | ok | 103 | 1656ms | 4112ms | 4911ms |
| 170.0 | 180.0 | app1 | ok | 119 | 6591ms | 9682ms | 26600ms |
| 170.0 | 180.0 | end-users | ok | 124 | 5231ms | 9046ms | 9905ms |
| 180.0 | 190.0 | app1 | ok | 175 | 6523ms | 9705ms | 26818ms |
| 180.0 | 190.0 | end-users | ok | 116 | 3309ms | 5167ms | 9517ms |
| 190.0 | 200.0 | app1 | ok | 58 | 4333ms | 8840ms | 9884ms |
| 190.0 | 200.0 | end-users | ok | 96 | 7474ms | 9495ms | 9949ms |
| 200.0 | 210.0 | app1 | ok | 114 | 7500ms | 9500ms | 9950ms |
| 200.0 | 210.0 | end-users | ok | 132 | 1837ms | 4569ms | 9057ms |
| 210.0 | 220.0 | app1 | ok | 131 | 7104ms | 15444ms | 28544ms |
| 210.0 | 220.0 | end-users | ok | 120 | 3843ms | 7931ms | 9793ms |
| 220.0 | 230.0 | app1 | ok | 88 | 7284ms | 9457ms | 9946ms |
| 220.0 | 230.0 | end-users | ok | 104 | 4818ms | 8917ms | 9892ms |
| 230.0 | 240.0 | app1 | ok | 107 | 7972ms | 17412ms | 28741ms |
| 230.0 | 240.0 | end-users | ok | 89 | 1473ms | 3288ms | 4829ms |
| 240.0 | 250.0 | app1 | ok | 42 | 7500ms | 9500ms | 9950ms |
| 240.0 | 250.0 | end-users | ok | 72 | 4545ms | 8714ms | 9871ms |
| 250.0 | 260.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 262.0 | app1 | no dispatches in this window | 0 | n/a | n/a | n/a |
| 260.0 | 262.0 | end-users | no dispatches in this window | 0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: PASS** (tolerance: 10%, cost model: input=1 output=2 cached=1)

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 2970450 | 147847 | 3104095.0 | -0.5% | 3006292.0 | 3266144.0 | -8.0% | True |
| end-users | 3719520 | 185066 | 3895590.0 | -0.2% | 3900446.0 | 4089652.0 | -4.6% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 2474 | 0 | 0 | 0 (never shed) | 0.00% | 23.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 3081 | 0 | 0 | 0 (never shed) | 0.00% | 76.5% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=5439). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | ok | 5439 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 253013 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
