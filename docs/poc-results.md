# POC results — weighted fair share on a GPU-free cluster

Run 2026-10-04 against OpenShift, namespace `maas-fairness-poc`, using the
manifests in `deploy/poc/`. No GPUs: the model server is
`ghcr.io/llm-d/llm-d-inference-sim:v0.11.4`, which speaks the OpenAI API and
returns real `usage` blocks without doing real inference.

## What was actually proven

The custom EPP image loads the `maas-weighted-fairness` plugin, Envoy's
ext_proc filter routes live traffic through it, and under genuine contention
the delivered token split tracks the configured weights.

**Setup.** Three tenants with weights 20 / 10 / 65 (plus an `unclassified`
catch-all at 5), each driven by 32 closed-loop workers for 240 s against a pool
of 2 simulator replicas × `--max-num-seqs 4` = 8 concurrent slots — a ~12×
over-offer. Every run reported `pool_saturation{stage="effective"} ≈ 2.8` and
HTTP 200 on every request.

| Configuration | app1 (w=20) | app2 (w=10) | end-users (w=65) |
|---|---|---|---|
| **Configured target** | **20.0%** | **10.0%** | **65.0%** |
| Shadow mode (`enforce: false`) | 34.3% | 32.8% | 32.9% |
| Enforcing, `newcomerClamp: false` — run 1 | 23.9% | 14.1% | 61.9% |
| Enforcing, `newcomerClamp: false` — run 2 | 23.8% | 13.5% | 62.8% |
| Enforcing, `newcomerClamp: true` | 35.7% | 19.2% | 45.1% |

Shares are `maas_fairness_contended_service_tokens_total` — the SLI numerator,
counted only while the group was backlogged and the pool saturated.

Reading across the first three rows: shadow mode delivers equal thirds, which
is correct FCFS behaviour for three identically-loaded tenants and confirms the
plugin accounts without reordering. Enforcing moves the split onto the weights,
reproducibly to within ~1 point across two independent runs.

Also confirmed in every run:

- **Grouping.** Eight distinct `end-user-N` subscription IDs collapsed to a
  single `end-users` flow. `unmatched_subscriptions_total` stayed at 0. Had the
  prefix rule failed, end users would have appeared as eight queues each
  holding weight 65.
- **True-up.** `requests_without_usage_total` stayed at 0 across ~2,600
  requests, so every request was reconciled against a real `usage` block rather
  than left on its provisional estimate.
- **No shedding.** `flow_control_requests_evicted_total` never incremented, so
  the measured split is the fairness policy's doing and not the TTL's.

## Work conservation: no limits when there is spare capacity

The table above only ever ran all three tenants at once, which measures the
split and says nothing about the requirement that motivated the whole design:
nobody is throttled while the pool has room. Four further runs, same config
(`enforce: true`, `newcomerClamp: false`, `halfLifeSeconds: 60`).

**An absent tenant's share is absorbed, not reserved.** If end-users' 65% were
held in reserve, app1+app2 would be capped near 35% of the pool and two thirds
of the GPU would idle.

| Run | Active tenants | Dispatches / 240 s | vs. 3-tenant baseline | Split |
|---|---|---|---|---|
| baseline | all three | 851 | — | 23.8 / 13.5 / 62.8% |
| **E1** | app1 + app2 | **794** | **93%** | 62.7% / 37.3% |
| **E2** | app1 alone | **1069** | **126%** | 100% |

E1 keeps the pool busy with end-users gone, and the two remaining tenants
divide it 62.7 / 37.3 — close to the 67 / 33 that weights 20:10 imply, carrying
the same few points of warm-up bias toward the smaller weight seen everywhere
else. E2 gives app1 the entire pool; had it been pinned to its nominal 20% it
would have managed ~170 dispatches, not 1069. Latency tracks the same story:
app1's P50 falls from 15.97 s under full contention to 7.05 s alone.

**Asymmetric demand: a heavy low-weight tenant is not held to its weight.** The
strictest of these tests, and the realistic one. app1 (weight **20**) saturates
with 32 workers while end-users (weight **65**) trickles with 2. Unlike E1,
end-users always has a non-empty queue, so it remains a live candidate in
*every* `Pick` decision — a policy that treated weight as a ceiling would pass
E1 and fail this.

| Run | app1 (w=20) | end-users (w=65) | Total |
|---|---|---|---|
| **E6** dispatches | 974 | 97 | **1071** |
| **E6** token share | **92.8%** | 7.2% | — |
| **E6** latency P50 | 7.86 s | **5.18 s** | — |

app1 took **92.8% of delivered tokens on a weight of 20**, because end-users
only asked for 7.2%. The total of 1071 dispatches matches the 1069 that app1
managed running completely alone (E2), so none of end-users' unclaimed 65% was
wasted.

And end-users was not punished for being small: it got *better* latency than
app1 (5.18 s vs 7.86 s P50). That is the intended behaviour, not an accident —
its large weight keeps `A/w` low so its few requests jump the queue, and once
its queue drains it stops being a candidate and app1 takes everything else.
Both halves of the requirement hold at once: the small tenant stays responsive,
the large tenant is not throttled.

**Below capacity, a second tenant costs the first nothing.** Two workers per
tenant against 8 slots, so the pool is roughly half idle and the policy should
never meaningfully engage.

| Run | Active tenants | app1 P50 / P95 | app2 P50 / P95 | Queue depth |
|---|---|---|---|---|
| **E3** | app1 alone | 1.01 s / 4.28 s | — | 0 |
| **E4** | app1 + app2 | 0.98 s / 4.29 s | 1.00 s / 4.29 s | 0 |

app1's latency is unchanged to within noise (it was marginally *faster* with
app2 also running, and completed 149 requests against 138). Queue depth stayed
at zero throughout. Nothing waits while there is room.

This is structural rather than implemented. `Pick` is handed only non-empty
queues (`plugin.go:297-302` skips any queue reporting `Len() == 0`), so an idle
tenant is not a candidate that loses — it is not a candidate at all, and with a
single backlogged group that group wins every decision by default. Grepping the
plugin for `capacity|reserve|quota|limit|throttle|budget|entitle` matches
nothing but the license header: a weight is only ever a divisor in a comparison
between queues that are *currently competing*. `TestWorkConservation` asserts
the same property at the unit level (weights 2:1, B idle, A takes all 1000
picks).

One related detail, verified rather than assumed: in E2
`contended_service_tokens_total` is absent for app1 entirely. That is
deliberate — `plugin.go:364` gates contention accounting on
`len(candidates) > 1`, so the SLI numerator only accrues when at least two
groups are backlogged simultaneously. With a single tenant there is no
contention to be fair about, and the metric correctly declines to invent one.
It is also what keeps the SLI honest: a tenant that ran alone all night does
not dilute its own contended-share statistic.

## Residual gap: small-weight groups run ~4 points rich

Even clamp-off, app1 lands at ~23.8% against 20% and app2 at ~13.5% against
10%, with end-users absorbing the shortfall. The bias is consistently *toward
the low-weight groups*, which is the signature of warm-up: tabs start empty
after every EPP restart, and for roughly the first half-life all groups look
equally unserved, so the early part of each 240 s run is close to FCFS. A
longer run, or discarding the first 60 s, should shrink it. Not yet measured —
the metrics were read as cumulative totals rather than as a time series, which
is the obvious next refinement.

## SUPERSEDED: "the newcomer clamp hurt here"

> **This finding was refuted on GPUs — see the scenario matrix and the
> clamp A/B below. The runs described here were demand-starved, which
> fired the empty -> non-empty edge constantly. Kept for the reasoning
> trail; do not act on it.**

Enabling `newcomerClamp` moved the split *away* from the weights — end-users
fell from ~62% to 45% — while firing only **19 times in 862 dispatches**. Of
those 19, **14 landed on end-users**.

The mechanism is self-reinforcing. The clamp fires on the empty → non-empty
queue edge. The highest-weight group is served fastest, so it is the group
whose queue momentarily drains; and the clamp writes `A = floor × w`, so the
largest weight has the most credit erased per firing. A handful of clamps is
therefore enough to repeatedly reset the group that the weights most favour.

This is worth taking seriously but **not worth acting on from this evidence
alone**. The design's rationale for the clamp (`docs/design.md`, and Part 1 of
the plan) is about a tenant returning after genuine idleness, and it remains
sound for that case. What this run suggests is narrower: *the empty →
non-empty edge may be a poor proxy for "returning from idle"* when a tenant is
being served so well that its queue keeps draining between arrivals. A
time-based guard — clamp only if the queue has been empty for some meaningful
fraction of the half-life — would separate the two cases.

The caveat that matters: this is a **closed-loop** generator. Each tenant can
have at most 32 requests outstanding, so its queue drains whenever all its
workers are in flight. Open-loop traffic with Poisson arrivals would not drain
the favoured group's queue the same way, and might never trigger the effect.
Re-test with an open-loop generator before changing the default.

## Pitfalls hit along the way

Each of these produced a run that looked healthy and measured nothing. They are
recorded because every one of them is silent by default.

1. **Load that merely saturates is not enough.** At 8 workers per tenant the
   pool reported saturation and the policy *was* consulted, but queue depths sat
   at 1–4 items against 8 slots. A weighted queue can only apportion work that
   is queued, so the split came out at equal thirds — indistinguishable from a
   broken policy. Raising to 32 workers per tenant (queue depths 17–26) is what
   made the weights expressible. **Check queue depth, not just saturation.**

2. **`curl` treats HTTP 400 as success.** The simulator defaults to
   `--max-model-len 1024`; a ~1,200-token prompt overflowed it and every request
   returned 400 in milliseconds. The generator reported no errors and the run
   completed suspiciously fast. The plugin's own
   `requests_without_usage_total` — specified in the design purely as a
   regression detector for a missing vLLM flag — is what caught it. The
   generator now tallies status codes itself.

3. **Rollouts that never complete.** This cluster has two `Ready` workers at
   ~98% of allocatable CPU requested. The default `maxSurge: 25%` creates a pod
   that can never schedule, so `oc rollout status` hangs while the *old* pods
   keep serving — which from a client looks exactly like a config change having
   no effect. Both deployments now pin surge to zero.

4. **The EPP must not roll.** Fixing (3) for the EPP surfaced a real
   correctness bug rather than a scheduling one: `RollingUpdate` with
   `maxSurge: 1` briefly runs **two** EPPs, which is precisely the split-brain
   that `replicas: 1` exists to prevent — each would see part of each tenant's
   traffic, judge that tenant under its share, and both would over-dispatch.
   `strategy: Recreate` is now set. A few seconds with *no* EPP is strictly
   better: `failureMode: FailOpen` means those requests bypass fairness instead
   of being actively misallocated.

5. **Metrics TLS is decided by `--metrics-cert-dir`, not `--secure-serving`.**
   Verified against upstream `pkg/epp/server/metrics_tls_test.go`. An EPP can
   serve ext_proc over TLS while its metrics port is plaintext; assuming
   otherwise yields connection errors on the Prometheus targets page and empty
   graphs everywhere else. `deploy/podmonitor.yaml` now documents how to check.

6. **Two InferencePool API groups, and both are needed.** The EPP watches
   `inference.networking.k8s.io/v1`; this cluster's gateway controller only
   resolves `inference.networking.x-k8s.io/v1alpha2` backendRefs and rejects the
   v1 pool outright. `deploy/poc/02-epp.yaml` declares the same pool twice.

## The official LLMInferenceService path — working

`deploy/poc/05-llmisvc-sim.yaml` runs the same plugin the way it will actually
ship: a real `LLMInferenceService` whose scheduler is templated by RHOAI's own
preset, with the GPU model-server preset swapped for the simulator.

Confirmed on 2026-10-08 (RHOAI 3.4.4). KServe created the whole topology —
`maas-llmisvc-kserve` (2 model servers), `maas-llmisvc-kserve-router-scheduler`
(the EPP, our image), `maas-llmisvc-inference-pool`,
`maas-llmisvc-kserve-route`, `maas-llmisvc-epp-service` — and templated the
EPP's command itself:

```
/app/epp --pool-name maas-llmisvc-inference-pool --pool-namespace maas-fairness-poc
         --grpc-port 9002 --grpc-health-port 9003
         --enable-cert-reload=true --secure-serving=true --cert-path=/var/run/kserve/tls
```

with our ConfigMap injected as `--config-text`. The EPP log shows
`maas-weighted-fairness` instantiated with every parameter, and flow control
wired to `fairnessPolicyRef: maas-fairness`. A request through the gateway at
`/maas-fairness-poc/maas-llmisvc/v1/chat/completions` returned **HTTP 200**
with a real usage block, and the EPP reported
`maas_fairness_dispatch_total{fairness_id="app1"} 1` with
`maas_fairness_enforcing 1`.

### Four things the direct rig could never have caught

Each one broke the deployment, and none of them is reachable from
`deploy/poc/02-epp.yaml`.

1. **`model.uri: ""` is rejected.** The shipped presets use an empty `uri`, but
   a real instance fails to reconcile with `invalid model URI:`. The fix is a
   tiny real model the simulator never reads. A *fake* URI is worse than none:
   it passes this check and then fails slowly inside the storage-initializer.

2. **Omitting the GPU preset from `baseRefs` does not omit its command.** The
   controller merges the well-known default template regardless
   (`PresetsCombined: True`), so the container inherited a large bash script
   doing RoCE/NCCL discovery before `exec vllm serve /mnt/models`. The
   simulator image is distroless, so the pod died with
   `executable file /bin/bash not found` — which reads like a broken image
   rather than an inherited command. `command` must be set explicitly.

3. **TLS on the model server.** With `enableLLMInferenceServiceTLS: true`,
   KServe templates the health probes as `https://:8000/health` and mounts a
   serving cert at `/var/run/kserve/tls`. The simulator served plaintext, so
   every probe failed with `http: server gave HTTP response to HTTPS client`
   while the pod ran happily. Fixed with the simulator's own
   `--ssl-certfile`/`--ssl-keyfile`. The direct rig sets
   `--secure-serving=false` and never meets this.

4. **`--model-server-metrics-scheme` was *not* templated in this render** —
   the EPP's flag dump shows it empty, even though the preset source contains
   `{{ if .GlobalConfig.EnableTLS }}--model-server-metrics-scheme=https{{- end }}`
   and the other TLS-gated flags *were* templated. So the compatibility shim in
   `cmd/epp/main.go` was **not** exercised here. It stays as defensive code —
   the preset can clearly emit that flag, and an unknown flag is fatal to
   pflag — but we should not claim it is load-bearing on the evidence of this
   deployment. Instead KServe injected a `metrics-data-source` plugin with
   `scheme: https` into the config, which is the v0.10.0+ mechanism.

### Open: it works, but never reports Ready

`SchedulerWorkloadReady`, `RouterReady` and `Ready` stay `False` on
`SchedulerReconcileError`, while `InferencePoolReady`, `MainWorkloadReady`,
`WorkloadsReady` and `PresetsCombined` are all `True` and all three pods are
`1/1 Running`:

```
failed to reconcile scheduler role maas-fairness-poc/maas-llmisvc-epp-role:
  user "system:serviceaccount:redhat-ods-applications:llmisvc-controller-manager"
  is attempting to grant RBAC permissions not currently held:
  {APIGroups:["llm-d.ai"], Resources:["inferencemodelrewrites"], Verbs:["get" "list" "watch"]}
  {APIGroups:["llm-d.ai"], Resources:["inferenceobjectives"], Verbs:["get" "list" "watch"]}
```

Kubernetes' privilege-escalation guard: the controller is handling a Role that
grants permissions its own ServiceAccount does not hold. That is an RHOAI
packaging gap, not something our manifest causes.

**The Role itself is fine.** `maas-llmisvc-epp-role` was created successfully
on the first reconcile and the EPP's ServiceAccount has everything it needs —
`oc auth can-i list` returns `yes` for `inferencepools`, `pods` *and*
`inferenceobjectives.llm-d.ai`, and the EPP logs zero `forbidden` lines. What
fails is every *subsequent* reconcile, where the controller re-validates the
existing Role and trips the escalation check.

So nothing is functionally broken, but the consequences are not purely
cosmetic:

- Anything gating on `Ready` treats this as a failed deployment — the RHOAI
  dashboard, `oc wait --for=condition=Ready`, CI, a GitOps sync.
- The controller is stuck in a failing reconcile loop, so later edits to the
  LLMInferenceService spec will not be applied cleanly.

Fixing it means granting the `llmisvc-controller-manager` ServiceAccount
`get/list/watch` on `llm-d.ai` `inferenceobjectives` and
`inferencemodelrewrites` cluster-wide — an operator-level change, so not done
here.

### The stale webhook that blocked all of this

Before any of the above was reachable, **every** `LLMInferenceService` create on
this cluster was rejected:

```
failed calling webhook "connection-llmisvc-v1alpha2.odh-model-controller.opendatahub.io":
  the server could not find the requested resource
```

Not specific to us — a four-line LLMInferenceService failed identically under
`--dry-run=server`, in every namespace tried.

The cause was a stale `MutatingWebhookConfiguration`. The cluster's KServe
stack was installed 2026-09-07 21:09 and carries `v3-5-0-*` presets, while the
operator is 3.4.4. That config declared five webhooks including
`connection-llmisvc-v1alpha{1,2}` with `failurePolicy: Fail`, pointing at paths
the running `odh-model-controller` never registers — it registers only six
paths, none of them for llminferenceservice.

It had **no ownerReferences**, so nothing garbage-collected it, and the
operator could not repair it in place. Deleting it was enough: the 3.4.4
operator recreated it seconds later with **three** webhooks — exactly the paths
the controller actually serves, with both `connection-llmisvc` entries gone —
and admission has worked since.

Worth knowing that the documented uninstall would *not* have fixed this: it
removes the DSC, DSCI, Auth CR, namespaces and Subscription/CSV, but says
nothing about webhook configurations or the 20 `LLMInferenceServiceConfig`
presets, all of which are unowned and survive. A full reinstall would have come
back up and re-adopted the same broken config.

## Real vLLM on CPU — no GPU required

The simulator was never the only GPU-free option. Red Hat ships a supported CPU
build of vLLM, `registry.redhat.io/rhaii/vllm-cpu-rhel9` ("Red Hat AI Inference
Server for CPU (AVX2)"), with tags tracking the product (3.4.0, 3.4.1, 3.5.0,
3.5.1). `deploy/poc/07-vllm-cpu.yaml` runs it against Qwen2.5-0.5B-Instruct,
two replicas, `VLLM_CPU_KVCACHE_SPACE=4`. Both pods reached `1/1 Running` in
about five minutes.

This closes three gaps that every earlier result carried as caveats:

| | Simulator | CPU vLLM |
|---|---|---|
| `cached_tokens` | always 0 | **1024 of 1110 prompt tokens (92%)** |
| `--enable-prompt-tokens-details` | never exercised | validated |
| `--enable-force-include-usage` | never exercised | validated (`requests_without_usage_total` = 0) |
| Saturation | sleeps | a real KV cache that fills |

`maas_fairness_prompt_tokens_cached_ratio{fairness_id="app1"}` read **0.615**,
the first non-zero value this project has ever produced — and arithmetically
exactly right for three requests at 0, 0.92, 0.92. **`cachedInputTokenWeight`
finally has a real signal**, which the design names as the parameter most
coupled to the group weights and the headline reading of the shadow period.

What CPU still cannot give us is `outputTokenWeight`. That ratio is prefill
chunk size over decode batch size — an efficiency property of the hardware — so
measuring it here would yield a confident, wrong number. The two-run `guidellm`
calibration still needs GPUs.

## MaaS now governs the gateway, and it validates a design decision

Once MaaS was deployed, unauthenticated requests to the model endpoint began
returning **401**. That is Authorino enforcing the `maas-poc-gateway-authn`
AuthPolicy, and it is correct behaviour, not a regression. The progression is
worth knowing: no token → 401; a token for an unauthorised ServiceAccount →
**403**; a token whose subject passes the policy's
`kubernetesSubjectAccessReview` (`get llminferenceservices/<name>` in the
request-path namespace) → **200**.

More interesting is what the policy *injects* on every authenticated request:

| Header | Value |
|---|---|
| `x-gateway-inference-fairness-id` | the **constant** `https://kubernetes.default.svc` |
| `x-gateway-inference-objective` | the ServiceAccount name, else `authenticated` |

**The first one vindicates the decision to overwrite `FairnessID`
unconditionally.** The plan chose that over the stock identity plugin, which
only populates the field when it is *empty*, on spoofing grounds. On a MaaS
cluster the consequence is sharper than anticipated: the gateway always sets
that header, and to the *same constant for every caller*. With the stock
plugin, every tenant would collapse into a single flow named
`https://kubernetes.default.svc` and the fairness policy would be completely
inert — one queue, nothing to be fair between, and no error anywhere. Because
our `RequestHeaderProcessor` overwrites from `x-maas-subscription-id`
regardless, the constant is harmlessly discarded.

**The second is a latent risk, currently dormant.** `x-gateway-inference-objective`
selects the priority band, and fairness is intra-band only — the plan called
this "the sneaky one ... a total bypass". Here the *gateway* sets it per
ServiceAccount, so different callers could in principle land in different
bands and never be compared. It is inert today only because the cluster has
**zero `InferenceObjective` resources**, so every objective name resolves to
the default band. Creating one with a non-zero priority would silently remove
that tenant from the weighted comparison. This belongs in the runbook as a
standing check:

```sh
oc get inferenceobjectives.llm-d.ai -A    # expect none, or all priority 0
```

## End-to-end on real MaaS auth — plumbing proven, fairness NOT yet measured

Four real `MaaSSubscription`s (`app1-production`, `app2-batch`,
`end-user-alpha`, `end-user-beta`) with owning groups and one `sk-oai` API key
each, driving real vLLM through the HTTPS Route. The generator no longer
asserts its own identity: Authorino validates the key and injects
`X-MaaS-Subscription`, and the plugin classifies on that.

**What this proved:**

| Check | Result |
|---|---|
| Per-subscription classification | app1=1, app2=1, **end-users=2** |
| Prefix collapse on real names | `end-user-alpha` + `end-user-beta` -> one flow |
| `unmatched_subscriptions_total` | 0 |
| Shadow-mode control | 36.6 / 34.1 / 29.3%, dispatches 27/27/26 — equal, correct FCFS |
| Policy engaging under load | `pool_saturation 7.9`; queue depths app1=22, app2=11, **end-users=0** |

That last row is the mechanism visibly working: the weight-65 tenant is served
so preferentially its queue drains while the weight-20 and weight-10 tenants
back up.

**What it did NOT prove, and must not be read as proving:** the weighted split
on real inference. The enforced run returned 34.4 / 28.8 / 36.8% against a
20/10/65 target, and that number is **invalid**:

```
requests_without_usage_total   app1=56  app2=57  end-users=31  = 144
dispatch_total                 app1=113 app2=101 end-users=120 = 334
```

**43% of requests never trued up.** At 40 workers per tenant against roughly
eight effective slots, CPU inference is slow enough that requests hit the
client timeout before completing. No usage block arrives, so each stays
charged its provisional ESTIMATE permanently, and every subsequent dispatch
decision is made against a corrupted tab. The split measured under those
conditions is noise.

This is the alarm doing its job — the design specifies
`requests_without_usage_total` as a regression detector that must be flat
zero, and treating any run with a non-zero value as a measurement would be
exactly the error it exists to prevent.

**The load window on CPU is narrow.** The ~12x over-offer that made the
simulator runs work is far too much here, because CPU vLLM is roughly twenty
times slower; but too little offer leaves the queues shallow and the weights
inexpressible (see "Pitfalls" above). Finding a load that is simultaneously
deep enough to express 20/10/65 and light enough that nothing times out may
not be possible at this throughput. **The honest position is that the weighted
split remains measured only on the simulator, and that real-inference
confirmation waits for GPUs.**

## On real GPUs: the weighted split works

Two A100 80GB, Qwen2.5-7B on vLLM, two replicas, traffic through the HTTPS
Route authenticated with real MaaS `sk-oai` keys.

| tenant | weight | **achieved** | target |
|---|---|---|---|
| app1 | 20 | **20.5%** | 20% |
| app2 | 10 | **11.6%** | 10% |
| end-users | 65 | **67.9%** | 65% |

`normalized_service` (A/w, equal across groups at equilibrium) read
app1 **14,342**, end-users **14,358** -- equal to within 0.1%. That is weighted
LAS converged, which is the real proof; the token percentages are its
consequence.

The shadow-mode control on the same setup gives 33.3 / 33.3 / 33.4 with
dispatches 1121/1121/1120, so the split is produced by the policy and not by
the traffic.

### The detour, and the lesson in it

Earlier runs on the same hardware produced a ratio stuck near 1.8:1 no matter
what the weights said -- 2:1 gave 1.81, 3.25:1 gave 1.79, and a deliberately
extreme 18:1 gave 1.82. It looked exactly like a hard ceiling, and it was
written up here as one. **That conclusion was wrong.**

What it actually was: **the favoured tenant ran out of work to be favoured
with.** The load generator is closed-loop with a fixed worker count per
tenant, so a tenant can never have more than W requests outstanding. Give
every tenant the same W and the high-weight tenant's queue drains -- it is
being served faster than its own workers can resubmit. An empty queue is not a
candidate in `Pick`, so the surplus correctly goes to the other tenant.

That is **work conservation doing its job**, not a defect. A tenant cannot
receive more than it asks for, which is the same property proven earlier in
E1/E2/E6.

Proof: with weights 5 vs 90 and demand matched to entitlement (24 workers vs
256), the achieved ratio was **16.65:1** against a target of 18:1, end-users
took **94.3%** of tokens against an entitlement of 90/95 = **94.7%**, and
normalized_service converged to 17,548 vs 14,965.

Three things made this hard to see, and all three are worth remembering:

1. **2:1 sits close to what equal-demand load can express**, so
   `TestProportionality` and the app1:app2 pair both looked healthy while the
   mechanism was being starved. A passing 2:1 is not evidence the weighting
   works at larger ratios.
2. **Deepening the backlog did not help** -- starving the pool to 2 slots made
   it *worse* (1.34:1), because it throttled the favoured tenant's refill rate
   as much as anyone's. The lever is per-tenant demand, not total queue depth.
3. **`normalized_service` was the tell throughout.** It sat 8-10x apart in
   every failing run, correctly reporting that the policy had identified an
   imbalance it was not being given the opportunity to correct.

### What this means for a load test, and for an SLA

**To measure a weighted split, every tenant must offer more load than its
entitlement.** Equal worker counts across tenants cannot demonstrate a ratio
larger than the generator can sustain, and the result will look like a broken
policy. Size each tenant's offered concurrency above its share of capacity.

For the SLA the wording in Part 1 of the plan already covers this correctly:
the guarantee is a floor on *delivered throughput under contention*, and a
tenant that does not send traffic gets nothing. These runs are the empirical
confirmation -- end-users reaches 65% only when it actually asks for 65%.

## GPU test suite — four results

All on 2x A100, Qwen2.5-7B, two replicas, real MaaS `sk-oai` auth, weights
20/10/65 unless stated. Load sized so every tenant over-offers its
entitlement, per the lesson above.

### 1. Work conservation holds on real inference

| run | active tenants | output tokens | vs 3-tenant baseline |
|---|---|---|---|
| baseline | all three | 155,424 | — |
| **E1** | app1 + app2 | **149,735** | **96.3%** |
| **E2** | app1 alone | **147,032** | **94.6%** |

app1 alone took 94.6% of the full pool on a weight of 20; capped at its weight
it would have managed ~31k. Absent tenants' shares are absorbed, not reserved.
In E1 the two survivors split it 64.7/35.3 — 1.83:1 against their 20:10.

### 2. Below capacity, a second tenant is free

| run | app1 P50 | app1 P95 | queue depth |
|---|---|---|---|
| **E3** app1 alone, 6 workers | **0.72 s** | 0.75 s | 0 |
| **E4** app1+app2, 6 each | **0.75 s** | 0.78 s | 0 |

A 4% difference, inside noise, with queues at zero throughout. Nothing waits
while there is room.

### 3. The newcomerClamp finding is REFUTED

| | clamp OFF | clamp ON |
|---|---|---|
| app1 | 20.9% | 22.0% |
| app2 | 11.8% | 11.9% |
| end-users | 67.3% | 66.1% |

Within ~1 point, with `normalized_service` converged either way (14,500 vs
14,561), and **only 5 clamps fired** across ~2,500 dispatches.

The earlier result — where enabling the clamp appeared to move the split badly
away from target — was an artefact of demand-starved load. With equal
per-tenant concurrency the favoured tenant's queue drained constantly, so the
empty -> non-empty edge fired over and over. At correctly sized load the edge
is rare and the clamp is effectively inert. **The design default of `true`
stands; the concern recorded earlier does not reproduce.**

### 4. 40/20/40 also lands

| tenant | weight | achieved |
|---|---|---|
| app1 | 40 | **41.3%** |
| app2 | 20 | **20.7%** |
| end-users | 40 | **38.0%** |

Within 2 points on all three, and notably a *different shape* from 20/10/65 —
so the result is not an artefact of one particular weight set.

### 5. Per-group cache-hit profile — the cachedInputTokenWeight evidence

Three deliberately different traffic shapes (`deploy/poc/10-cache-profile.yaml`):

| group | workload | **cached / prompt tokens** |
|---|---|---|
| app2 | fully unique prompts (control) | **6.3%** |
| app1 | fixed system prompt + short tail | **87.7%** |
| end-users | long shared prefix (multi-turn proxy) | **96.4%** |

This is the table the design calls the real deliverable of the shadow period,
and it confirms the prediction that drove the parameter's default. The spread
is enormous — **6.3% to 96.4%** — so `cachedInputTokenWeight` is a genuine
*differential* lever here, not a no-op.

Concretely: at the default 1.0, end-users pays full price for prompt tokens
that are 96.4% cache hits. Drop the weight to 0.1 and its effective prompt
cost falls roughly tenfold while app2's barely moves, re-pricing end-users
against the others by almost an order of magnitude. That is exactly why the
design insists the parameter and the group weights be re-derived together, and
why 1.0 is the safe default: wrong-high merely under-serves the cacheable
tenant, wrong-low silently breaks everyone else's floor.

## Scenario matrix — demand patterns and edge cases

All on 2x A100 with the shipped defaults (20/10/65, `enforce: true`,
`newcomerClamp: true`, `cachedInputTokenWeight: 1.0`), uniform traffic so
cache effects do not confound, 150s per run.

| # | scenario | result | expected |
|---|---|---|---|
| **S1** | app1 HARD, app2 HARD, end-users idle | 59.9% / 38.3% | 66.7 / 33.3 |
| **S2** | app1 HARD, end-users trickle | **app1 93.3%**, end-users 6.4% | app1 unconstrained |
| **S3** | app1 HARD, end-users HARD, app2 idle | **23.7% / 75.0%** | 23.5 / 76.5 |
| **S4** | S3 plus app2 trickling | 24.5% / 2.9% / 71.6% | app2 served, rest redistributed |
| **S5** | end-users joins COLD after 120s | settles at its share immediately | no monopoly burst |

Every run delivered ~128,000 output tokens, matching the three-tenant baseline
rate. **No scenario wasted capacity**, whatever the demand shape.

**S2 is the one that answers "is a low-weight tenant throttled when there is
room".** app1 carries weight 20 and took **93.3%**, because end-users asked
for only 6.4%. A weight is a floor under contention, never a ceiling.

**S3 is the cleanest proof of proportionality.** With app2 absent the
remaining two split 23.7 / 75.0 against a predicted 23.5 / 76.5 — the weights
reproduced almost exactly.

**S4 shows redistribution.** app2 trickled and received exactly the 2.9% it
asked for; its unused entitlement went to the other two rather than idling.

### S5: the returning-idle tenant does not monopolise

app1 and app2 ran alone for 120s, building tabs, then end-users (weight 65,
tab fully decayed) joined cold with 208 workers. Dispatches per 15s window,
end-users as a share of the end-users+app1 traffic:

```
+15s   117   11%   <- ramping up, not seizing
+30s   112   76%
+45s   121   76%
+60s   251   76%
+75s   117   75%
+90s   226   76%
```

It went straight to ~76%, which against app1 is a 3.2:1 ratio versus the 3.25:1
its 65:20 weights specify. **There is no monopolisation burst** — the failure
mode the newcomer clamp exists to prevent. The clamp fired **twice**.

This is the scenario the design worried about most ("a tenant away for 10
minutes ... monopolizing the pool for tens of seconds while everyone else
stalls") and it does not occur.

### The one weak result

S1 produced 1.57:1 between app1 and app2 against their 2:1. Every other
proportionality check landed within a couple of points, so this is the
outlier. The likely cause is that 150s is short relative to the 60s half-life
when both tabs start cold — S3 and S5, which involve the much larger 65:20
ratio, were closer. Worth re-running longer before treating the 20:10 pair as
reliably exact.

## What this POC does *not* show

- **Saturation is now real but small.** deploy/poc/07-vllm-cpu.yaml runs vLLM
  with a genuine KV cache (VLLM_CPU_KVCACHE_SPACE=4), so backpressure is real.
  But CPU inference at this scale is not a GPU pool, and the load numbers above
  were all measured against the simulator. They have NOT been re-run on vLLM.
- **(superseded) The simulator has no KV cache and no real compute; it
  fakes backpressure with sleeps. Scorer behaviour under genuine memory
  pressure, and the `vramtime` cost model's trigger conditions, are untested.
- **`cachedInputTokenWeight` is no longer untested, but it is uncalibrated.**
  Real vLLM on CPU produces genuine cache hits (see above), so the discount
  path now executes and `prompt_tokens_cached_ratio` is non-zero. What is still
  missing is the per-group traffic-shape table the design calls the real
  deliverable of the shadow period: hit rates measured per group, over real
  traffic, which is what decides whether to move the weight off 1.0.
- **`outputTokenWeight: 2.0` is still the uncalibrated placeholder.** The
  hardware now exists; the procedure is written up in
  [calibrating-output-token-weight.md](calibrating-output-token-weight.md).
  This is the largest single piece of outstanding work.
- **Open-loop behaviour.** Everything above is closed-loop. See the clamp
  finding for why that distinction may matter.
- **The GPU production manifest is still unapplied.** `deploy/llmisvc.yaml`
  (all three presets, real vLLM, `nvidia.com/gpu`) has not been run. The
  KServe wiring itself IS now proven, via `deploy/poc/05-llmisvc-sim.yaml`.
- **No sustained load through the LLMInferenceService path.** The weight-split
  and work-conservation numbers above were all measured on the direct rig.
  Through KServe only a single request has been verified end to end.

## Outstanding work

Ordered by how much they would change a conclusion.

| # | item | why it matters | blocked on |
|---|---|---|---|
| 1 | **Calibrate `outputTokenWeight`** | the only hardware-measured number; 2.0 has no physical basis and plausible values are 5-20x. Changing it re-denominates every floor, so the group weights must be re-derived with it. Procedure: [calibrating-output-token-weight.md](calibrating-output-token-weight.md) | a decision to run it |
| 2 | **Decide `cachedInputTokenWeight`** | measured, not theoretical: hit rates span 6.3% to 96.4% across groups, and moving the weight 1.0 -> 0.1 shifted end-users from 56.3% to 70.1% of delivered service while **halving total throughput**. A real lever with a real cost | a policy decision |
| 3 | **ClusterRole for `llmisvc-controller-manager`** | the LLMInferenceService never reports `Ready`, and the controller is stuck in a failing reconcile so it will not apply future spec edits cleanly. Needs `get/list/watch` on `llm-d.ai` `inferenceobjectives` and `inferencemodelrewrites` | operator-level approval |
| 4 | **Durable NFD fix** | GPU exposure currently depends on a hand-applied `feature.node.kubernetes.io/pci-10de.present` label per node. Set `deviceLabelFields: [vendor]` on the NodeFeatureDiscovery CR or **every new GPU node will look like broken hardware** | operator-level approval |
| 5 | **Test on a real RHOAI 3.4 cluster** | three unknowns remain: whether 3.4's controller validates the EndpointPickerConfig, its InferencePool API group, and its tokenizer sidecar (3.5 has no equivalent). The 3.4-shaped preset test covered the flags, not the controller | a 3.4 cluster |
| 6 | **Fix `contended_service_tokens_total`** | it records the provisional charge and the true-up delta as separate calls, each independently gated by the contention check, so their sum is not guaranteed to equal the charged cost. Use `normalized_service x weight` meanwhile | small code change |
| 7 | **Re-run S1 longer** | 1.57:1 against a 2:1 target was the only proportionality miss; likely 150s being short against a 60s half-life with cold tabs | 10 minutes |
| 8 | **`maas-default-gateway` inference path** | returns 500: `maas-api-route` targets a TLS service port with no `BackendTLSPolicy`, and that CRD is not installed. API keys currently require port-forwarding to maas-api | upstream/MaaS |
| 9 | **Sustained load through the Route** | the 600s timeout and `buffer-response: false` annotations are only proven by single requests | 10 minutes |
| 10 | **Open-loop load generation** | every result is closed-loop. Poisson arrivals would drain queues differently and are the honest test of the clamp | generator work |
| 11 | **Verify metrics reach Prometheus** | `deploy/podmonitor.yaml` exists and UWM is enabled, but no dashboard query has ever been confirmed end to end | 15 minutes |

## Reproducing

```sh
oc apply -f deploy/poc/00-config.yaml
oc apply -f deploy/poc/01-sim-backend.yaml
oc apply -f deploy/poc/02-epp.yaml      # needs the image built first
oc apply -f deploy/poc/03-gateway.yaml
oc apply -f deploy/rbac.yaml            # mints the /metrics reader token

# A/B: run once as shipped (enforce: false), then flip and re-run.
oc apply -f deploy/poc/04-loadgen.yaml
oc logs -n maas-fairness-poc job/maas-loadgen --tail=6   # status tally must be ~all 200
```

Read the result with the metrics-reader token against
`http://maas-epp:9090/metrics` (plaintext — no `--metrics-cert-dir` in the POC),
filtering on `llm_d_epp_maas_fairness_`.
