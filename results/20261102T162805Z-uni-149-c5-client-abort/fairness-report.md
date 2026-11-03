# Fairness benchmark: full-contention (uni-149-c5-client-abort)

**Verdict: PASS** (threshold: 10 points)

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-676fd97cd-k8zb9` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-02T16:29:16Z` |
| Run end | `2026-11-02T16:34:39Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 20.0 | 32 | 544 | 200=371, 500=7 | 15.4 | 25.1 | 710232.0 | 21.1% | 17.1% | -3.9 | 16.9% | -4.1 | 3.6s | 98.9% | 533.0 |
| app2 | 10.0 | 32 | 454 | 200=439, 500=15 | 22.7 | 27.3 | 576008.0 | 10.5% | 13.9% | 3.3 | 14.1% | 3.6 | 3.0s | 98.9% | 439.0 |
| end-users | 65.0 | 128 | 2213 | 200=2168, 500=45 | 14.3 | 19.3 | 2866206.0 | 68.4% | 69.0% | 0.6 | 68.9% | 0.5 | 3.2s | 98.9% | 2166.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | 2716.0 | n/a | n/a | n/a | n/a | n/a | 0.0s | 98.9% | 2.0 |

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

**Windows** (33 total):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 17598.0 | 21.1% | 17.1% | -3.9 |
| 0.0 | 10.0 | app2 | True | 16232.0 | 10.5% | 15.8% | 5.3 |
| 0.0 | 10.0 | end-users | True | 69014.0 | 68.4% | 67.1% | -1.3 |
| 10.0 | 20.0 | app1 | True | 31138.0 | 21.1% | 16.7% | -4.4 |
| 10.0 | 20.0 | app2 | True | 36556.0 | 10.5% | 19.6% | 9.1 |
| 10.0 | 20.0 | end-users | True | 118882.0 | 68.4% | 63.7% | -4.7 |
| 20.0 | 30.0 | app1 | True | 31150.0 | 21.1% | 20.4% | -0.7 |
| 20.0 | 30.0 | app2 | True | 17560.0 | 10.5% | 11.5% | 1.0 |
| 20.0 | 30.0 | end-users | True | 104046.0 | 68.4% | 68.1% | -0.3 |
| 30.0 | 41.0 | app1 | True | 16272.0 | 21.1% | 9.6% | -11.4 |
| 30.0 | 41.0 | app2 | True | 6708.0 | 10.5% | 4.0% | -6.6 |
| 30.0 | 41.0 | end-users | True | 146148.0 | 68.4% | 86.4% | 18.0 |
| 41.0 | 51.0 | app1 | True | 41914.0 | 21.1% | 24.6% | 3.5 |
| 41.0 | 51.0 | app2 | True | 56914.0 | 10.5% | 33.4% | 22.9 |
| 41.0 | 51.0 | end-users | True | 71662.0 | 68.4% | 42.0% | -26.4 |
| 51.0 | 61.0 | app1 | True | 32394.0 | 21.1% | 21.0% | -0.0 |
| 51.0 | 61.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 51.0 | 61.0 | end-users | True | 121738.0 | 68.4% | 79.0% | 10.6 |
| 61.0 | 71.0 | app1 | True | 1358.0 | 21.1% | 0.8% | -20.3 |
| 61.0 | 71.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 61.0 | 71.0 | end-users | True | 167866.0 | 68.4% | 99.2% | 30.8 |
| 71.0 | 81.0 | app1 | True | 58174.0 | 21.1% | 33.9% | 12.8 |
| 71.0 | 81.0 | app2 | True | 59506.0 | 10.5% | 34.6% | 24.1 |
| 71.0 | 81.0 | end-users | True | 54060.0 | 68.4% | 31.5% | -36.9 |
| 81.0 | 91.0 | app1 | True | 17616.0 | 21.1% | 10.7% | -10.4 |
| 81.0 | 91.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 81.0 | 91.0 | end-users | True | 147540.0 | 68.4% | 89.3% | 20.9 |
| 91.0 | 101.0 | app1 | True | 29728.0 | 21.1% | 19.3% | -1.8 |
| 91.0 | 101.0 | app2 | True | 14816.0 | 10.5% | 9.6% | -0.9 |
| 91.0 | 101.0 | end-users | True | 109676.0 | 68.4% | 71.1% | 2.7 |
| 101.0 | 111.0 | app1 | True | 39278.0 | 21.1% | 23.0% | 2.0 |
| 101.0 | 111.0 | app2 | True | 48710.0 | 10.5% | 28.6% | 18.0 |
| 101.0 | 111.0 | end-users | True | 82530.0 | 68.4% | 48.4% | -20.0 |
| 111.0 | 121.0 | app1 | True | 17588.0 | 21.1% | 10.7% | -10.4 |
| 111.0 | 121.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 111.0 | 121.0 | end-users | True | 147556.0 | 68.4% | 89.3% | 20.9 |
| 121.0 | 131.0 | app1 | True | 41960.0 | 21.1% | 25.8% | 4.8 |
| 121.0 | 131.0 | app2 | True | 32472.0 | 10.5% | 20.0% | 9.5 |
| 121.0 | 131.0 | end-users | True | 88080.0 | 68.4% | 54.2% | -14.2 |
| 131.0 | 141.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 131.0 | 141.0 | app2 | True | 10810.0 | 10.5% | 6.7% | -3.8 |
| 131.0 | 141.0 | end-users | True | 150222.0 | 68.4% | 93.3% | 24.9 |
| 141.0 | 151.0 | app1 | True | 58156.0 | 21.1% | 34.4% | 13.3 |
| 141.0 | 151.0 | app2 | True | 51414.0 | 10.5% | 30.4% | 19.9 |
| 141.0 | 151.0 | end-users | True | 59498.0 | 68.4% | 35.2% | -33.2 |
| 151.0 | 161.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 151.0 | 161.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 151.0 | 161.0 | end-users | True | 167744.0 | 68.4% | 100.0% | 31.6 |
| 161.0 | 171.0 | app1 | True | 28388.0 | 21.1% | 18.4% | -2.6 |
| 161.0 | 171.0 | app2 | True | 14848.0 | 10.5% | 9.6% | -0.9 |
| 161.0 | 171.0 | end-users | True | 110798.0 | 68.4% | 71.9% | 3.5 |
| 171.0 | 181.0 | app1 | True | 41910.0 | 21.1% | 24.8% | 3.8 |
| 171.0 | 181.0 | app2 | True | 44588.0 | 10.5% | 26.4% | 15.9 |
| 171.0 | 181.0 | end-users | True | 82404.0 | 68.4% | 48.8% | -19.6 |
| 181.0 | 191.0 | app1 | True | 6786.0 | 21.1% | 3.9% | -17.1 |
| 181.0 | 191.0 | app2 | True | 1358.0 | 10.5% | 0.8% | -9.7 |
| 181.0 | 191.0 | end-users | True | 164880.0 | 68.4% | 95.3% | 26.9 |
| 191.0 | 201.0 | app1 | True | 43270.0 | 21.1% | 25.6% | 4.6 |
| 191.0 | 201.0 | app2 | True | 59424.0 | 10.5% | 35.2% | 24.6 |
| 191.0 | 201.0 | end-users | True | 66258.0 | 68.4% | 39.2% | -29.2 |
| 201.0 | 211.0 | app1 | True | 33814.0 | 21.1% | 22.3% | 1.3 |
| 201.0 | 211.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 201.0 | 211.0 | end-users | True | 117708.0 | 68.4% | 77.7% | 9.3 |
| 211.0 | 221.0 | app1 | True | 0.0 | 21.1% | 0.0% | -21.1 |
| 211.0 | 221.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 211.0 | 221.0 | end-users | True | 171558.0 | 68.4% | 100.0% | 31.6 |
| 221.0 | 231.0 | app1 | True | 52758.0 | 21.1% | 31.5% | 10.4 |
| 221.0 | 231.0 | app2 | True | 60874.0 | 10.5% | 36.3% | 25.8 |
| 221.0 | 231.0 | end-users | True | 54092.0 | 68.4% | 32.3% | -36.2 |
| 231.0 | 241.0 | app1 | True | 25748.0 | 21.1% | 15.5% | -5.6 |
| 231.0 | 241.0 | app2 | True | 0.0 | 10.5% | 0.0% | -10.5 |
| 231.0 | 241.0 | end-users | True | 140558.0 | 68.4% | 84.5% | 16.1 |
| 241.0 | 251.0 | app1 | False | 4056.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | app2 | False | 17596.0 | n/a | n/a | n/a |
| 241.0 | 251.0 | end-users | False | 147618.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app1 | False | 39178.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | app2 | False | 25622.0 | n/a | n/a | n/a |
| 251.0 | 261.0 | end-users | False | 4070.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 261.0 | 271.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 271.0 | 281.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 281.0 | 291.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 291.0 | 301.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 301.0 | 311.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 311.0 | 321.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 323.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 323.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 321.0 | 323.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens +43.7%, cost +41.5%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 456330 | 22745 | 688304.0 | 43.7% | 710232.0 | 501820.0 | 41.5% | False |
| app2 | 539970 | 26811 | 566781.0 | 0.0% | 576008.0 | 593592.0 | -3.0% | True |
| end-users | 2666640 | 132887 | 2796939.0 | -0.1% | 2866206.0 | 2932414.0 | -2.3% | True |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 544 | 0 | 0 | 0 (never shed) | 0.00% | 21.1% | n/a (nothing shed) | n/a (nothing shed) |
| app2 | 454 | 0 | 0 | 0 (never shed) | 0.00% | 10.5% | n/a (nothing shed) | n/a (nothing shed) |
| end-users | 2213 | 0 | 0 | 0 (never shed) | 0.00% | 68.4% | n/a (nothing shed) | n/a (nothing shed) |

**EPP-side shed (pool-wide):** not recorded -- `llm_d_epp_flow_control_requests_total` is absent from both snapshots, so whether the EPP or something in front of it (Kuadrant) produced the client's 429s is unknown.

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
