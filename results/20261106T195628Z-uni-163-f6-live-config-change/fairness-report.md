# Fairness benchmark: full-contention (uni-163-f6-live-config-change)

**Verdict: UNCONTENDED** -- every offered group's `contended_seconds_total` delta stayed under 1s, so the pool was never actually contended. Not scored against the 10-point weighted-split threshold; see docs/runbook.md.

- every offered group's contended_seconds_total delta stayed under 1s (app1=0.21s, app2=0.48s, end-users=0.49s) -- an order of magnitude below the ~9s a genuinely-contending tenant accrues in a 240s full-contention run (docs/runbook.md), so nobody was ever backlogged alongside anyone else and the weighted-split deviation check does not apply

**Caveat (UNI-163): the EPP restarted mid-run in a way this verdict did not catch.** The windowed series below shows a counter going backwards between two in-run scrapes, but the single before/after snapshot pair this verdict is built from happened to read monotonically end-to-end (a near-zero start and a lower-but-still-higher-than-zero end look the same as no restart at all). Every before/after delta above -- the verdict and the ledger cross-check below -- is computed from the post-restart pod's fresh counters alone and undercounts real traffic; read them as a measurement of the time since the restart, not the whole run.

## Run metadata

| field | value |
|---|---|
| Scenario | `full-contention` |
| Generator | `closed-loop` |
| Enforce | `True` |
| Duration (s) | `240` |
| Backend | `vllm-gpu (real)` |
| EPP image digest | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` |
| EPP pod | `maas-vllm-gpu-kserve-router-scheduler-656748bc54-n6kvf` |
| Namespace | `maas-fairness-poc` |
| Run start | `2026-11-06T19:57:38Z` |
| Run end | `2026-11-06T20:04:47Z` |

## Per-group result

`observed %`/`deviation (pts)` are the scored split, by weighted tokens (`contended_service_tokens_total`). `request-count %`/`request-count deviation (pts)` (UNI-146) are the same expected-share target scored against plain request COUNT instead -- informational only, never part of the verdict below. The two agree when every offered group sends uniform requests (every scenario before UNI-146) and are expected to diverge whenever request cost is asymmetric across groups (e.g. long-prompt/short-output vs. short-prompt/long-output).

| group | weight | offered workers | requests | statuses | p50s | p95s | delivered tokens | expected % | observed % | deviation (pts) | request-count % | request-count deviation (pts) | contended_seconds | cached ratio | dispatch_total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| app1 | 40.0 | 32 | 440 | 000=27, 200=399, 500=14 | 7.9 | 300.0 | 64822.0 | 40.0% | 6.8% | -33.2 | 11.0% | -29.0 | 0.2s | 98.9% | 49.0 |
| app2 | 20.0 | 32 | 1090 | 200=1034, 500=23, 503=33 | 5.7 | 25.3 | 324384.0 | 20.0% | 34.1% | 14.1 | 27.2% | 7.2 | 0.5s | 98.9% | 248.0 |
| end-users | 40.0 | 128 | 2476 | 000=78, 200=2338, 500=60 | 6.6 | 19.8 | 561262.0 | 40.0% | 59.1% | 19.1 | 61.8% | 21.8 | 0.5s | 98.9% | 417.0 |
| unclassified | 5.0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Timeline (UNI-127)

Window size: 10s (actual window durations vary slightly with scrape latency; see each window's own start/end below).

**Chaos events (scheduled):**
- t+120s: live_set (target=field:configmap:maas-epp-config:data.epp, value=apiVersion: llm-d.ai/v1alpha1
kind: EndpointPickerConfig
featureGates: [flowControl]
plugins:
  - type: maas-weighted-fairness
    name: maas-fairness
    parameters:
      # x-maas-subscription, NOT x-maas-subscription-id.
      #
      # This was wrong for most of the POC and the failure is silent: with
      # the id suffix the header simply never matches, every request falls
      # to defaultGroup, and unmatched_subscriptions_total stays at ZERO --
      # because nothing was mis-matched, the header was absent. The only
      # symptom is all traffic quietly sharing the `unclassified` weight.
      #
      # Verified against the AuthPolicy MaaS generates per model
      # (maas-auth-<model> in the model namespace), whose success response
      # injects exactly:
      #     X-MaaS-Subscription: auth.metadata.apiKeyValidation.subscription
      # i.e. the MaaSSubscription NAME from the validated sk-oai API key.
      # It also blanks Authorization before forwarding upstream.
      #
      # CONSEQUENCE FOR `groups` BELOW: the match values must be
      # MaaSSubscription names, not invented tenant strings. Confirm with
      #     oc get maassubscriptions -A
      # before trusting any weight in this file.
      identityHeader: x-maas-subscription
      groups:
        - { name: app1,      weight: 40, match: { exact:  [app1-production] } }
        - { name: app2,      weight: 20, match: { exact:  [app2-batch] } }
        - { name: end-users, weight: 40, match: { prefix: [end-user-] } }
      defaultGroup: { name: unclassified, weight: 5 }

      enforce: true
      stateLogIntervalSeconds: 5

      halfLifeSeconds: 60
      observedHalfLivesSeconds: [20, 120]

      costModel: tokens
      inputTokenWeight: 1.0
      outputTokenWeight: 2.0       # PLACEHOLDER until calibrated
      cachedInputTokenWeight: 1.0

      # Left at the production default, but see docs/poc-results.md: in this
      # POC, turning the clamp ON measurably moved the split AWAY from the
      # configured weights (end-users 62.8% -> 45.1%), and it did so while
      # firing only 19 times in 862 dispatches. The highest-weight group is
      # hit hardest, because it is served fastest, so its queue is the one
      # that momentarily drains -- and the clamp writes A = floor * w, so
      # the largest weight loses the most credit per clamp.
      #
      # Unresolved: whether the empty -> non-empty edge is simply a poor
      # proxy for "returning from idle" when a tenant is being served so
      # well that its queue keeps draining. Do not change the default on
      # this evidence alone; the closed-loop generator may drain queues in
      # ways real traffic does not.
      newcomerClamp: true
      provisionalCharge: true
      defaultEstimatedOutputTokens: 512
      estimatedBytesPerToken: 4
      agingTokensPerSecond: 0

      # x-request-id, x-maas-fairness-group, x-maas-fairness-queue-ms on the
      # response -- see docs/design.md "Per-request attribution" (UNI-53).
      # Defaults to true; set false to suppress if this is considered
      # internal detail leakage.
      emitAttributionHeaders: true

      # V(4) per-request tier -- see docs/design.md "V(4) is off Pick's hot
      # path" (UNI-47). Off by default; also requires -v=4 on the EPP
      # process. Neither this file nor -v reload without a redeploy.
      # Enabling needs BOTH this and a second edit to deploy/poc/02-epp.yaml,
      # or emission stays silently off -- see docs/runbook.md "Turn on the
      # V(4) per-request tier" for the exact steps and how to undo them.
      # requestTierV4SampleEvery: 100
      # requestTierV4TimeBoxSeconds: 900

  - type: single-profile-handler
  - type: queue-scorer
  - type: kv-cache-utilization-scorer
  - type: prefix-cache-scorer
  - type: max-score-picker

flowControl:
  # 300s here, against 60s in deploy/epp-config.yaml, and this is the one
  # POC deviation that is NOT a simplification.
  #
  # The load generator deliberately over-offers ~12x the pool's capacity so
  # the queues are deep enough for the weights to be expressible. The flip
  # side is that the throttled group waits a long time by design: at a 10%
  # share with 32 closed-loop workers, app2's queue wait approaches a
  # minute. With TTL at 60s those requests would be EVICTED rather than
  # served late -- and then the shed rate, not the fairness policy, is what
  # allocates the pool. The measurement would show app2 "receiving" its
  # share while most of its traffic was quietly dropped.
  #
  # Production keeps TTL within ~2x of halfLifeSeconds precisely so that
  # shedding stays a backstop. Do not copy 300s into a real deployment; it
  # is compensating for a synthetic over-offer that real traffic will not
  # reproduce. Watch llm_d_epp_flow_control_requests_evicted_total: if it
  # is non-zero in a run, that run measured shedding, not fairness.
  defaultRequestTTL: 300s
  defaultPriorityBand:
    fairnessPolicyRef: maas-fairness
    orderingPolicyRef: fcfs-ordering-policy
  priorityBands:
    - priority: 0
      fairnessPolicyRef: maas-fairness
      maxRequests: "5000"

schedulingProfiles:
  - name: default
    plugins:
      - { pluginRef: queue-scorer, weight: 2.0 }
      - { pluginRef: kv-cache-utilization-scorer, weight: 2.0 }
      - { pluginRef: prefix-cache-scorer, weight: 3.0 }
      - { pluginRef: max-score-picker })
- t+240s: live_restore (target=field:configmap:maas-epp-config:data.epp)

**Per-tenant schedule:**
- app1: active 0s-240s, no duty cycle
- app2: active 0s-240s, no duty cycle
- end-users: active 0s-240s, no duty cycle

**Time-to-converge** (seconds from a phase edge until every active tenant is within 10 points and stays there):

| phase edge (s) | converged at (s) | seconds to converge |
|---|---|---|
| 0.0 | n/a (never converged in this phase) | n/a |
| 120.0 | n/a (never converged in this phase) | n/a |
| 240.0 | n/a (never converged in this phase) | n/a |

**Windows** (43 total, EPP restart detected mid-window at least once):

| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|---|---|
| 0.0 | 10.0 | app1 | True | 13442.0 | 40.0% | 18.8% | -21.2 |
| 0.0 | 10.0 | app2 | True | 8136.0 | 20.0% | 11.4% | -8.6 |
| 0.0 | 10.0 | end-users | True | 50070.0 | 40.0% | 69.9% | 29.9 |
| 10.0 | 20.0 | app1 | True | 14906.0 | 40.0% | 8.9% | -31.1 |
| 10.0 | 20.0 | app2 | True | 21672.0 | 20.0% | 12.9% | -7.1 |
| 10.0 | 20.0 | end-users | True | 130980.0 | 40.0% | 78.2% | 38.2 |
| 20.0 | 30.0 | app1 | True | 31050.0 | 40.0% | 20.1% | -19.9 |
| 20.0 | 30.0 | app2 | True | 14836.0 | 20.0% | 9.6% | -10.4 |
| 20.0 | 30.0 | end-users | True | 108316.0 | 40.0% | 70.2% | 30.2 |
| 30.0 | 40.0 | app1 | True | 43316.0 | 40.0% | 25.8% | -14.2 |
| 30.0 | 40.0 | app2 | True | 36546.0 | 20.0% | 21.8% | 1.8 |
| 30.0 | 40.0 | end-users | True | 87848.0 | 40.0% | 52.4% | 12.4 |
| 40.0 | 50.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 40.0 | 50.0 | app2 | True | 8122.0 | 20.0% | 4.8% | -15.2 |
| 40.0 | 50.0 | end-users | True | 159602.0 | 40.0% | 95.2% | 55.2 |
| 50.0 | 60.0 | app1 | True | 43232.0 | 40.0% | 26.4% | -13.6 |
| 50.0 | 60.0 | app2 | True | 41880.0 | 20.0% | 25.6% | 5.6 |
| 50.0 | 60.0 | end-users | True | 78402.0 | 40.0% | 47.9% | 7.9 |
| 60.0 | 70.0 | app1 | True | 33828.0 | 40.0% | 21.2% | -18.8 |
| 60.0 | 70.0 | app2 | True | 20262.0 | 20.0% | 12.7% | -7.3 |
| 60.0 | 70.0 | end-users | True | 105460.0 | 40.0% | 66.1% | 26.1 |
| 70.0 | 80.0 | app1 | True | 8126.0 | 40.0% | 4.8% | -35.2 |
| 70.0 | 80.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 70.0 | 80.0 | end-users | True | 159602.0 | 40.0% | 95.2% | 55.2 |
| 80.0 | 90.0 | app1 | True | 50040.0 | 40.0% | 29.1% | -10.9 |
| 80.0 | 90.0 | app2 | True | 59600.0 | 20.0% | 34.7% | 14.7 |
| 80.0 | 90.0 | end-users | True | 62216.0 | 40.0% | 36.2% | -3.8 |
| 90.0 | 100.0 | app1 | True | 26920.0 | 40.0% | 17.8% | -22.2 |
| 90.0 | 100.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 90.0 | 100.0 | end-users | True | 124558.0 | 40.0% | 82.2% | 42.2 |
| 100.0 | 110.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 100.0 | 110.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 100.0 | 110.0 | end-users | True | 170298.0 | 40.0% | 100.0% | 60.0 |
| 110.0 | 120.0 | app1 | True | 58150.0 | 40.0% | 34.7% | -5.3 |
| 110.0 | 120.0 | app2 | True | 60854.0 | 20.0% | 36.3% | 16.3 |
| 110.0 | 120.0 | end-users | True | 48742.0 | 40.0% | 29.1% | -10.9 |
| 120.0 | 130.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 120.0 | 130.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 120.0 | 130.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 130.0 | 140.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 130.0 | 140.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 130.0 | 140.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 140.0 | 150.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 140.0 | 150.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 140.0 | 150.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 150.0 | 160.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 150.0 | 160.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 150.0 | 160.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 160.0 | 170.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 160.0 | 170.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 160.0 | 170.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 170.0 | 180.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 170.0 | 180.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 170.0 | 180.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 180.0 | 190.0 | app1 | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 180.0 | 190.0 | app2 | True | 0.0 | 20.0% | 0.0% | -20.0 |
| 180.0 | 190.0 | end-users | True | 0.0 | 40.0% | 0.0% | -40.0 |
| 190.0 | 200.0 | app1 | True | 4018.0 | 40.0% | 5.4% | -34.6 |
| 190.0 | 200.0 | app2 | True | 24342.0 | 20.0% | 32.8% | 12.8 |
| 190.0 | 200.0 | end-users | True | 45936.0 | 40.0% | 61.8% | 21.8 |
| 200.0 | 210.0 | app1 | True | 13542.0 | 40.0% | 7.3% | -32.7 |
| 200.0 | 210.0 | app2 | True | 68934.0 | 20.0% | 37.0% | 17.0 |
| 200.0 | 210.0 | end-users | True | 104038.0 | 40.0% | 55.8% | 15.8 |
| 210.0 | 220.0 | app1 | True | 13490.0 | 40.0% | 7.4% | -32.6 |
| 210.0 | 220.0 | app2 | True | 55472.0 | 20.0% | 30.4% | 10.4 |
| 210.0 | 220.0 | end-users | True | 113636.0 | 40.0% | 62.2% | 22.2 |
| 220.0 | 230.0 | app1 | True | 13466.0 | 40.0% | 7.1% | -32.9 |
| 220.0 | 230.0 | app2 | True | 59468.0 | 20.0% | 31.2% | 11.2 |
| 220.0 | 230.0 | end-users | True | 117646.0 | 40.0% | 61.7% | 21.7 |
| 230.0 | 240.0 | app1 | True | 13518.0 | 40.0% | 7.2% | -32.8 |
| 230.0 | 240.0 | app2 | True | 60806.0 | 20.0% | 32.6% | 12.6 |
| 230.0 | 240.0 | end-users | True | 112292.0 | 40.0% | 60.2% | 20.2 |
| 240.0 | 250.0 | app1 | False | 6788.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | app2 | False | 55362.0 | n/a | n/a | n/a |
| 240.0 | 250.0 | end-users | False | 67714.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 250.0 | 260.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 260.0 | 270.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 270.0 | 280.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 280.0 | 290.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 290.0 | 300.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 300.0 | 310.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 310.0 | 320.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 331.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 331.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 320.0 | 331.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 331.0 | 341.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 341.0 | 351.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 351.0 | 361.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 361.0 | 371.0 | end-users | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 371.0 | 381.0 | end-users | False | 0.0 | n/a | n/a | n/a |
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
| 421.0 | 429.0 | app1 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 429.0 | app2 | False | 0.0 | n/a | n/a | n/a |
| 421.0 | 429.0 | end-users | False | 0.0 | n/a | n/a | n/a |

## Ledger cross-check (UNI-138/G2)

**Ledger verdict: FAIL** (tolerance: 10%, cost model: input=1 output=2 cached=1)

- app1 exceeded the 10% ledger tolerance: raw tokens -87.7%, cost -88.0%
- app2 exceeded the 10% ledger tolerance: raw tokens -76.0%, cost -76.8%
- end-users exceeded the 10% ledger tolerance: raw tokens -82.2%, cost -82.2%

| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (from client) | cost diff % | within tolerance |
|---|---|---|---|---|---|---|---|---|
| app1 | 490770 | 24313 | 63225.0 | -87.7% | 64822.0 | 539396.0 | -88.0% | False |
| app2 | 1271820 | 63072 | 320133.0 | -76.0% | 324384.0 | 1397964.0 | -76.8% | False |
| end-users | 2875740 | 142974 | 538444.0 | -82.2% | 561262.0 | 3161688.0 | -82.2% | False |

## Shed rate vs weight (UNI-181)

Shed = client-observed HTTP 429/503. Weight share is over offered groups. Shed share / weight share above 1 means the group lost more of the shed than its weight; no PASS/FAIL is applied here.

| group | requests | 429 | 503 | shed | shed rate % | weight share % | shed share % | shed share / weight share |
|---|---|---|---|---|---|---|---|---|
| app1 | 440 | 0 | 0 | 0 (never shed) | 0.00% | 40.0% | 0.0% | 0.00 |
| app2 | 1090 | 0 | 33 | 33 | 3.03% | 20.0% | 100.0% | 5.00 |
| end-users | 2476 | 0 | 0 | 0 (never shed) | 0.00% | 40.0% | 0.0% | 0.00 |

**EPP-side shed (pool-wide, no per-group label exists):** 0 requests refused by the EPP (Dispatched=714). Client saw 0 x 429; at most 0 came from the EPP, so at least 0 came from elsewhere (e.g. Kuadrant).

## EPP pick latency (UNI-181)

| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | p50 vs baseline | p99 vs baseline |
|---|---|---|---|---|---|---|---|---|
| `scheduler_e2e` | not recorded (absent from both snapshots) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `flow_control_dispatch_cycle` | ok | 226549 | 0.050ms | 0.099ms | (0, 0.1]ms | (0, 0.1]ms | n/a | n/a |

Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); the bucket bounds are the real precision.

## Alerts (UNI-181)

Not recorded: no `--alerts-json` was supplied, so whether any alert fired during this run is unknown (not "none fired").

## Sources

- **delivered_tokens_and_observed_share**: llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly from the EPP's /metrics immediately before and after the run (same mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own accounting -- the generator cannot see token usage. Reused unmodified from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; this report does not invent a second definition of delivered share.
- **offered_and_delivered_requests**: deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table for delivered requests, status tally, and latency.
- **expected_share**: each offered group's configured_weight divided by the sum of configured_weight over OFFERED groups only (excludes the never-offered 'unclassified' catch-all and any group this scenario left idle), so a work-conserving policy absorbing an idle group's share is not scored as a deviation. Also excludes any 'capped_groups' entry (UNI-134's app2-trickle): a group offered but structurally unable to reach a weight-proportional share at its own worker count is scored on a dedicated 'did it get served' check instead, not folded into the other groups' expected-share denominator.
- **request_share_pct**: UNI-146 (C1): the SAME expected_share target above, scored against requests_total (plain request count, from the loadgen log) instead of delivered weighted tokens -- informational only, never part of the verdict. Equal to observed_share_pct when every offered group's requests are uniform cost (every scenario before this ticket); expected to diverge when request cost is asymmetric across groups.
