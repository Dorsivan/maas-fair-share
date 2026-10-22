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

## A4 (UNI-29): reproduced again, against the current EPP build, both modes

The section above is from 2026-10-15. Since then the EPP image was rebuilt and
redeployed ([UNI-75](/UNI/issues/UNI-75)), and the live deployment now serves
**`llama-3-1-8b`**, not the Qwen2.5-7B used in that run — the model changed
along with the image. [UNI-29](/UNI/issues/UNI-29) re-ran the headline split
on 2026-10-22 against today's live deployment, closed-loop, through the
in-cluster gateway Service, to confirm the split still holds on the backend
and build that are actually running now, not just on 2026-10-15's.

**Setup.** 2 replicas, `--max-num-seqs 8` each = 16 concurrent slots. EPP image
`image-registry.openshift-image-registry.svc:5000/maas-fairness-poc/maas-epp@sha256:5ef5df2776364e6161f91e5a3df0fbed9a4751bde847658af51923b1eded7f40`
(unchanged across all three runs below — only the ConfigMap's `enforce` flag
was flipped, and restored to `true` afterward). Load: `deploy/poc/12-loadgen-route.sh`
pattern, `max_tokens: 64`, a shared long prompt (heavily prompt-cached).
Weights 20/10/65 (`app1`/`app2`/`end-users`), `newcomerClamp: true` (live
production default, not reconfigured for this test).

| run | mode | workers (app1/app2/end-users) | duration | app1 | app2 | end-users | target |
|---|---|---|---|---|---|---|---|
| 1 | shadow (`enforce: false`) | 32/32/32 | 150s | 33.0% | 33.6% | 33.4% | 33.3/33.3/33.3 |
| 2 | enforce, equal workers | 32/32/32 | 180s | 31.3% | 31.1% | 37.6% | 20/10/65 |
| 3 | enforce, sized workers | 32/32/128 | 180s | 16.2% | 13.7% | 70.1% | 20/10/65 |

Shares are deltas of `llm_d_epp_maas_fairness_contended_service_tokens_total`
(the same SLI as the headline table and the Oct-15 GPU section) bracketed by a
before/after Prometheus scrape of the EPP's `/metrics` via the
`maas-epp-metrics-reader` token (`deploy/rbac.yaml`), since this run's role has
no cluster-monitoring read access. Standing checks on every run:
`maas_fairness_unmatched_subscriptions_total` stayed 0,
`flow_control_requests_evicted_total` was absent/0, and
`maas_fairness_requests_without_usage_total` stayed at 0 or 1 out of
700–1,700 requests per run — consistent with "trued up," not a measurement
artefact. HTTP status was 93–97% `200` on every run (the rest `500`, no
timeouts, no eviction).

**Run 1 (shadow) reproduces the FCFS control almost exactly** — equal thirds,
matching the Oct-15 shadow result (33.3/33.3/33.4) to within 0.6 points.

**Run 2 is a deliberate negative result, kept because it is instructive.**
Equal 32-worker demand across all three tenants is what the Oct-15 section's
"detour" warns against (`### The detour, and the lesson in it`, above) — and
it reproduces exactly that failure mode on *this* pool/model/latency
combination: `end-users`, the highest-weight tenant, is served fast enough
that its 32 workers cannot keep it backlogged, so its queue partially drains
and the delivered split compresses toward equal shares instead of expressing
20/10/65. This is work conservation doing its job, not enforcement failing —
but it means **equal-worker sizing, which happened to be sufficient on
2026-10-15's Qwen2.5-7B setup, is not sufficient on today's llama-3-1-8b
deployment**; the right concurrency depends on the backend's actual latency
under load, not a fixed worker count carried over from a different run.

**Run 3, sized so `end-users` offers enough concurrency to stay backlogged
(128 workers against its 65% share), reproduces the configured weights:**
16.2/13.7/70.1% against a 20/10/65 target — directionally and substantially
correct (enforcing clearly moves the split off equal-thirds and onto the
weight ordering: end-users > app1 > app2, same order as the targets), but
**outside the ~1-point tolerance the Oct-15 run achieved**, by up to ~5
points on `app1` and `end-users`.

**Hypothesis for the residual gap:** the worker counts (32/32/128) were sized
from a single order-of-magnitude estimate made live during this run, not
iteratively tuned the way the Oct-15 numbers likely were. 128 workers for
`end-users` may still be short of (or past) the concurrency that holds it
exactly at 65% share on this specific backend's latency distribution under
three-way contention — Run 2 shows the direction of the error when
under-sized (compresses toward equal), so a next attempt should try
increasing `end-users` further (e.g. 160–192) and compare. Not attempted here
because of the time cost of another 180s + metrics round-trip per iteration;
recorded as follow-up (Outstanding work, below) rather than iterated to
convergence in this run.

**What this is evidence of, plainly:** the 20/10/65 split is **not
simulator-only**. It has now been reproduced on real vLLM GPU inference twice,
on two different backend models/images nine days apart (Qwen2.5-7B on
2026-10-15, llama-3-1-8b on 2026-10-22), in both shadow and enforce mode, with
enforce mode in both cases moving the delivered split away from equal-thirds
and onto the configured weight ordering. The exact percentages are sizing- and
backend-dependent — they are not a single fixed number the plugin reproduces
regardless of load shape — but the mechanism (weighted LAS converging the
split toward configured weights under correctly-sized closed-loop contention)
is confirmed on real inference, not just in the simulator.

Reproduce: flip `enforce` in the live `maas-epp-config` ConfigMap (the
`LLMInferenceService` controller watches it and rolls the scheduler pod
automatically — do not edit the Deployment or CR directly, see
`docs/runbook.md` "Turn on the V(4) per-request tier" for why), wait for the
new pod to go `1/1`, then run closed-loop load with per-tenant worker counts
sized above each tenant's entitlement (see "What this means for a load test,
and for an SLA," above) while scraping
`llm_d_epp_maas_fairness_contended_service_tokens_total` before and after via
the `maas-epp-metrics-reader-token` secret.

### The EPP image above was not transferable, and `main` didn't deploy it — now fixed

The digest the three runs above used,
`...@sha256:5ef5df2776364e6161f91e5a3df0fbed9a4751bde847658af51923b1eded7f40`, is an
`image-registry.openshift-image-registry.svc:5000/...` reference: an in-cluster
`ImageStreamTag`, produced by [UNI-75](/UNI/issues/UNI-75)'s rebuild. To be explicit about
the question that matters for air-gap transfer: **this digest was never pushed to
`quay.io/rh-ee-dsivan/maas-fair-share`.** It is exactly the same situation `docs/runbook.md`
already documents for UNI-53's verification image — a real, correctly-built artifact that
proves the plugin logic on this cluster, but one that "does not leave this cluster," is
unmirrorable, and cannot be named by any `IDMS`/`ICSP` entry in a disconnected destination.

Separately, and independent of that: `deploy/llmisvc.yaml` and `deploy/poc/09-vllm-gpu.yaml`
on `main` were still pinned to `quay.io/rh-ee-dsivan/maas-fair-share:aef33a5`, a tag 31
commits behind `HEAD` (`git rev-list --count aef33a5..fc27130`). A clean checkout of `main`,
applied as documented, deployed neither the image the three runs above tested nor anything
close to current `HEAD` — it deployed a 31-commit-old binary. The percentages above are real,
but until this was fixed, nobody following this repository from a clean checkout could have
reproduced the deployment that produced them.

**Fixed in this same change.** The EPP plugin source, `go.mod`/`go.sum`, and `Dockerfile.epp`
are unchanged between UNI-75's `e86c3ee` and current `HEAD` (`fc27130` — confirmed with
`git log --oneline e86c3ee..HEAD -- pkg/ cmd/ Dockerfile.epp go.mod go.sum`, empty). So a
rebuild from `HEAD` is the same plugin logic as what these three runs tested, not a different
build. Rebuilt it (via an OpenShift `BuildConfig` with `output.to.kind: DockerImage` straight
to Quay — no local `podman` was available in this session; see `docs/runbook.md`,
"Publishing to Quay without a local podman") and pushed:

```
quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135
```

`deploy/llmisvc.yaml:104` and `deploy/poc/09-vllm-gpu.yaml:109` now pin this digest (not the
`:aef33a5` tag). The repository is **private** (confirmed: an anonymous registry-token pull
returns 401 even for the pre-existing `:aef33a5` tag), consistent with `docs/runbook.md`
already requiring the `quay-maas-pull` secret linked to `maas-vllm-gpu-epp-sa` — that secret
already covers `quay.io` cluster-wide, so no new pull-secret work was needed for this push.

**Verified, with a caveat on scope.** A throwaway pod in `maas-fairness-poc`, using
`maas-vllm-gpu-epp-sa` and no other configuration, pulled this exact digest and ran it; the
binary's own startup log confirms `commit-sha: fc27130f0703b8228127a4040eb160567000bc27`,
matching `HEAD` exactly. That proves the digest is genuinely pullable from outside the
cluster's internal registry, by the same credential path the live deployment already uses.

**What was not re-verified: the fairness split against this exact digest, live.** Rolling
the change out to the actual `LLMInferenceService` (`oc apply` or `oc patch`, either one) is
blocked right now by the same stale `MutatingWebhookConfiguration` described above in "The
stale webhook that blocked all of this" — it currently rejects every create *and* update to
any `LLMInferenceService` in the cluster, not something specific to this change, and deleting
it is a cluster-scoped action outside what this role can even read
(`mutatingwebhookconfigurations` is not namespace-scoped; `auth can-i` returns `no`). Since
the plugin source is byte-for-byte unchanged from what Run 1–3 tested, there is no reason to
expect a different split — but that is an inference from unchanged source, not a repeated
measurement, and the next person who can clear that webhook should re-run at least the
sized-worker enforce case against the now-committed digest to close that inference out.

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

## Open-loop (Poisson) load generation (UNI-34) — the clamp finding, revisited

Every result above is closed-loop: a fixed worker pool per tenant, each worker
blocking on one request before issuing its next. `deploy/poc/13-loadgen-poisson.py`
(wrapped by `13-loadgen-poisson.sh`) is the open-loop counterpart this
document's own "Outstanding work #10" called for: independent per-tenant
Poisson arrival processes at a fixed mean rate, dispatched fire-and-forget to
a thread pool so the offered rate never depends on how fast — or slowly — the
backend answers. This is the honest test flagged in the SUPERSEDED section:
"Open-loop traffic with Poisson arrivals would not drain the favoured group's
queue the same way, and might never trigger the [clamp] effect."

**Setup.** Same GPU backend as the rest of this document (2×A100, Qwen2.5-7B,
2 replicas, `--max-num-seqs 8` ⇒ 16 concurrent slots), same live config
(`enforce: true`, `newcomerClamp: true`, weights 20/10/65, `halfLifeSeconds:
60`) — nothing about the plugin or its deployment was changed for this test.
Per the established methodology ("every tenant must offer more load than its
entitlement... size load so demand, not asymmetry, decides the split"), all
three tenants were given the **same** Poisson rate per level, so any split
away from equal thirds is the policy's doing, not the traffic's. Traffic
through the public Route, same prompt and `max_tokens: 64` as every other load
generator in this repo.

**Pool capacity, measured.** A quick single-tenant calibration (app1 alone,
30 s bursts) found the knee: 20 req/s held (p50 0.82 s, p95 1.31 s, p99
1.78 s, all 200), 35 req/s collapsed within the same 30 s window (p50 20.8 s,
p95 44.3 s, p99 46.7 s, still all 200 but queueing badly). The three-tenant
runs below bracket that knee at 18 req/s aggregate (stable) and 24 req/s
aggregate (collapsing).

| level | rate/tenant | aggregate | duration | client-observed status | EPP `newcomer_clamps_total` per dispatch | delivered share, app1/app2/end-users | vs 20/10/65 target |
|---|---|---|---|---|---|---|---|
| below saturation | 4 req/s | 12 req/s | 240 s | 994/962/928 sent, all HTTP 200, p50 0.75 s | **65–68%** of dispatches | 34.5/33.4/32.1% (client `completion_tokens`)† | flat — pool not contended |
| below saturation | 6 req/s | 18 req/s | 90 s | 588/541/531 sent, all HTTP 200, p50 0.77 s | **64–70%** of dispatches | 35.6/32.5/32.0% (client `completion_tokens`)† | flat — pool not contended |
| **above saturation** | 8 req/s | 24 req/s | 90 s‡ | EPP dispatched 731/641/543; client saw sustained 20–50 s latencies and timeouts on a large fraction of app2/end-users requests | app1 4.9%, app2 5.3%, **end-users 8.3%** | **40.4% / 34.1% / 25.5%** (EPP `contended_service_tokens_total`) | **inverted** — lowest weight (app1, 20) delivered the most; highest weight (end-users, 65) delivered the least |

† `contended_service_tokens_total` and `contended_seconds_total` — the SLI
this document uses everywhere else — stayed at **exactly zero delta** for
both below-saturation rows: with the pool this lightly loaded, no two groups
were ever backlogged at the same instant, so the metric correctly declined to
invent a contended share (same behaviour as E2's solo-tenant run, "## Below
capacity, a second tenant costs the first nothing"). The share quoted here is
therefore the client-side `usage.completion_tokens` total per group instead —
a demand-driven number, not a policy-driven one, and unremarkable precisely
because it tracks the near-equal 4/4/4 and 6/6/6 req/s offered equally.

‡ Shortened from this document's usual 240 s specifically to bound the
backlog an overload run produces (see "a killed open-loop client does not
relieve the backend" below). The 24 req/s level was first attempted at the
usual 240 s and aborted at the 90 s mark, by which point client-observed
in-flight requests had grown 20→36→52→180→360→560 with no sign of levelling
off; it was killed there rather than let run to completion, both to avoid
exhausting the generator's own thread pool and to keep the eventual drain
tractable. After confirming the backend had fully recovered (see below), the
level was re-run cleanly — shortened to 90 s and given more worker headroom —
and is the run reported in the table. Even that clean, shortened run ended
its 90 s arrival window with in-flight still at 876 and still climbing, so
the table is a deliberately early snapshot of the *onset* of collapse, not a
converged steady state. A longer run would show a larger backlog, not a
smaller one, so this table likely **understates** the eventual severity of
the inversion rather than overstating it. `dispatch_total` and
`contended_service_tokens_total` are EPP-internal counters and do not depend
on the client receiving a response, so they are reported as the authoritative
numbers; the client's own completion log additionally showed many requests
failing after ~50 s with no response body, which was not root-caused to a
specific hop (Route/HAProxy edge, KServe, or vLLM) and is not relied on here.

### The clamp fires constantly under genuine arrivals — far more than closed-loop ever showed

At both below-saturation levels, the newcomer clamp fired on roughly
**two-thirds of all dispatches**. Every closed-loop run in this document fired
it far more rarely: 19 times in 862 dispatches (2.2%) in the original
CPU/simulator run that first raised the concern, and only 5 times in ~2,500
dispatches (0.2%) in the GPU A/B that refuted it (`## 3. The newcomerClamp
finding is REFUTED`, above). That refutation's own caveat said why: "this is a
closed-loop generator... open-loop traffic... might never trigger the effect."
It is now measured, and the opposite happened — open-loop arrivals trigger the
empty→non-empty edge on most requests, not rarely, because a Poisson process
leaves genuine idle gaps between one tenant's own requests even when nothing
is wrong, and a lightly-loaded pool answers fast enough that the queue is
routinely empty again before the next arrival. A closed-loop worker can never
produce this signal — it resubmits the instant its previous request completes,
so its queue is only ever empty when it is winning so hard there is no more
of its own work queued, which is rare by construction.

At these two levels the high clamp rate is **harmless**, because the pool
is not contended (near-zero `contended_seconds_total`) — there is nothing for
the clamp's reset to take away from anyone. This matches "Below capacity, a
second tenant costs the first nothing": with no real competition, the policy
mechanism is mostly inert regardless of how often it fires.

### Push past saturation, and the clamp's cost becomes visible — and it inverts the split

The above-saturation row is where it stops being harmless. The clamp fires
less often per dispatch here (4.9–8.3%, because the queue is now usually
non-empty, so there are fewer empty→non-empty edges to catch) but the firings
that do happen land disproportionately on **end-users**, the highest-weight
group, at nearly double app1's rate (8.3% vs 4.9%). That tracks the mechanism
this document already identified and set aside as unproven on closed-loop
evidence: the clamp writes `A = floor × w` (`plugin.go:379-396`), so the
credit erased scales with the clamped group's *own* weight — the larger the
weight, the more a single clamp firing cuts off a group that was behind and
trying to catch up.

The measured consequence: **end-users (weight 65) delivered only 25.5% of
contended service**, against a target of 65%, while **app1 (weight 20)
delivered 40.4%** — the ordering is not just off by a few points, as in the
closed-loop demand-starved artefact this document already diagnosed and
dismissed; it is **inverted**. The lowest-weight tenant outperformed the
highest-weight tenant by a wide margin, under genuine Poisson arrivals, on the
same backend and the same unmodified config this document used to claim the
split "works" (`## On real GPUs: the weighted split works`, 20.5/11.6/67.9%
achieved against 20/10/65 target — that result was closed-loop).

### A killed open-loop client does not relieve the backend

A side observation worth recording because closed-loop testing structurally
cannot produce it: when the first (240 s) attempt at the 24 req/s level was
aborted by killing the generator process, a trivial unrelated probe request
(`max_tokens: 16`, no contention) still took **14.0 s**, then **8.8 s** on a
retry 60 s later, and did not return to the ~0.2 s baseline until roughly
**4 minutes** after the client stopped sending anything. Requests the EPP had
already dispatched kept consuming GPU slots regardless of whether the client
that originated them was still running. A closed-loop generator cannot
demonstrate this because it stops submitting new work the moment its own
workers block — there is no analogue of a client disappearing while a real
backlog it created keeps draining on its own.

### What was not tested here

- **No open-loop clamp on/off A/B.** The closed-loop clamp finding was
  confirmed by toggling `newcomerClamp` and re-running (`## 3`, above); the
  same A/B was not attempted open-loop. The live value is baked into the
  Deployment's `--config-text` args by the `LLMInferenceService` CR's KServe
  reconcile — the exact mechanism that silently reverted the image fix in
  [UNI-75](/UNI/issues/UNI-75) — so a safe toggle-and-revert needs the same
  CR-level care that fix required, and [UNI-29](/UNI/issues/UNI-29) was
  concurrently `in_progress` against this same live GPU deployment while this
  test ran. Editing the CR to flip a plugin parameter for this ticket risked
  disrupting that concurrent work for a confirmation this document's
  mechanistic read (`A = floor × w`, scaled by the clamped group's own weight)
  already explains with reasonable confidence. Flagged as follow-up, not
  attempted.
- **Single scenario only.** Weights 20/10/65, `halfLifeSeconds: 60`, the
  headline fairness scenario — not the full scenario matrix (S1–S5), not a
  CPU-backend repeat.
- **The above-saturation run is short (90 s, 1.5 half-lives)** by deliberate
  design (see above) and captures the onset of collapse, not a converged
  state.

### Conclusion: open-loop CONTRADICTS the "clamp is inert" finding

Stated plainly, per this ticket's done-when criteria: **open-loop arrivals
contradict** `## 3. The newcomerClamp finding is REFUTED` and its closed-loop
"only 5 clamps fired... effectively inert" conclusion, and they **confirm —
more strongly than originally observed —** the SUPERSEDED section's narrower
concern. The empty→non-empty edge is not a rare artefact of demand-starved
closed-loop testing; under a real arrival process it is the common case, and
once the pool is genuinely saturated it drives a severe, measured inversion of
the configured weights (end-users 65%→25.5%, app1 20%→40.4%). The GPU
closed-loop A/B's "effectively inert" reading holds only because a closed-loop
generator structurally cannot produce the idle-queue edge at any meaningful
rate — it was measuring the clamp in a traffic shape that happens to be
blind to it. **The design default of `newcomerClamp: true` should be
reconsidered for any workload expecting genuine open-loop or bursty client
traffic**, pending the time-based guard ("clamp only if the queue has been
empty for some meaningful fraction of the half-life") the SUPERSEDED section
already proposed and this result now gives a concrete reason to build.

## What this POC does *not* show

- **The headline table at the top of this document (the four-row table under
  "What was actually proven") is simulator-only.** Those numbers come from
  `ghcr.io/llm-d/llm-d-inference-sim:v0.11.4` (see line 4-6) and have not been,
  and will not be, re-run on vLLM as stated there — the simulator's artificial
  12x-capacity-over-offer is what makes that specific table's sizing work, and
  it is not how the real-GPU runs below are sized. The 20/10/65 **split
  itself** is real-vLLM-confirmed (not simulator-only) in "On real GPUs: the
  weighted split works" and "A4 (UNI-29)" below, on two different backend
  models nine days apart, in both shadow and enforce mode — but those are
  separate runs with their own numbers, not a re-run of the headline table.
- **Saturation is now real but small.** deploy/poc/07-vllm-cpu.yaml runs vLLM
  with a genuine KV cache (VLLM_CPU_KVCACHE_SPACE=4), so backpressure is real.
  But CPU inference at this scale is not a GPU pool, and the CPU-path load
  numbers in "End-to-end on real MaaS auth — plumbing proven, fairness NOT yet
  measured" (above) were all measured against CPU vLLM and flagged invalid
  there — they are not the simulator, but they are also not the real-GPU
  confirmation.
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
- **(resolved, UNI-34) Open-loop behaviour.** Was: everything above is
  closed-loop. Now measured — see "Open-loop (Poisson) load generation" above.
  The result is not reassuring: under genuine Poisson arrivals the newcomer
  clamp fires on ~65% of dispatches (vs 0.2–2.2% closed-loop) and, once the
  pool is pushed past saturation, measurably **inverts** the configured
  20/10/65 split (end-users down to 25.5%, app1 up to 40.4%). Open-loop
  contradicts this document's closed-loop "clamp is inert" conclusion; no
  open-loop clamp on/off A/B was run (see that section for why).
- **The GPU production manifest is still unapplied.** `deploy/llmisvc.yaml`
  (all three presets, real vLLM, `nvidia.com/gpu`) has not been run. The
  KServe wiring itself IS now proven, via `deploy/poc/05-llmisvc-sim.yaml`.
- **(partially resolved, UNI-27) Sustained load through the LLMInferenceService
  path and the Route was, until now, only proven by single requests.**
  Closed-loop load against both paths is now measured for status tally and
  `normalized_service` convergence — see the Outstanding work row below and the
  UNI-27 ticket comments for the full data. The Route-path non-200 explanation
  is directly verified against gateway access logs; the LLMInferenceService-path
  explanation is **inferred by analogy only, not independently proven** — this
  cluster has no log aggregation, and the gateway's own log buffer had already
  rotated past the run window by the time it was checked. Separately, the 600s
  timeout and `buffer-response: false` annotations are still only proven by
  single requests (see Outstanding work #15) — this closed-loop run used short
  prompts (`max_tokens: 64`, ~6-11s p95 responses) that never approach that
  timeout or exercise streaming/buffering behaviour.

## Outstanding work

Ordered by how much they would change a conclusion.

| # | item | why it matters | blocked on |
|---|---|---|---|
| — | ~~Calibrate `outputTokenWeight`~~ | **Not a POC gap.** This is a per-environment commissioning step, not a number this repo can ship: it is an efficiency ratio that moves with GPU, model, quantisation, batch size and vLLM version. The deliverable is the procedure in [calibrating-output-token-weight.md](calibrating-output-token-weight.md); run it when commissioning each environment, and re-derive the group weights in the same change | — |
| 2 | **Decide `cachedInputTokenWeight`** | measured, not theoretical: hit rates span 6.3% to 96.4% across groups, and moving the weight 1.0 -> 0.1 shifted end-users from 56.3% to 70.1% of delivered service while **halving total throughput**. A real lever with a real cost | a policy decision |
| 3 | **ClusterRole for `llmisvc-controller-manager`** | the LLMInferenceService never reports `Ready`, and the controller is stuck in a failing reconcile so it will not apply future spec edits cleanly. Needs `get/list/watch` on `llm-d.ai` `inferenceobjectives` and `inferencemodelrewrites` | operator-level approval |
| 4 | **Durable NFD fix** | GPU exposure currently depends on a hand-applied `feature.node.kubernetes.io/pci-10de.present` label per node. Set `deviceLabelFields: [vendor]` on the NodeFeatureDiscovery CR or **every new GPU node will look like broken hardware** | operator-level approval |
| 5 | **Test on a real RHOAI 3.4 cluster** | three unknowns remain: whether 3.4's controller validates the EndpointPickerConfig, its InferencePool API group, and its tokenizer sidecar (3.5 has no equivalent). The 3.4-shaped preset test covered the flags, not the controller | a 3.4 cluster |
| — | ~~Fix `contended_service_tokens_total`~~ | **Fixed.** The gate decision (is the band contended) is now made once, at dispatch, and reused at completion instead of being re-checked independently at each of the two charge sites. The metric also now books the real, measured cost once at completion rather than the dispatch estimate plus a separately-gated correction, so an estimator overshoot no longer gets silently dropped (a Prometheus counter cannot move backwards on a negative delta). `TestContendedServiceTokensEqualChargedCost`, `TestContendedServiceTokensEqualChargedCostOnOverestimate`, and `TestAbortedRequestStillBooksContendedService` cover under-estimate, over-estimate, and abort respectively | — |
| 7 | **Re-run S1 longer** | 1.57:1 against a 2:1 target was the only proportionality miss; likely 150s being short against a 60s half-life with cold tabs | 10 minutes |
| 8 | **`maas-default-gateway` inference path** | returns 500: `maas-api-route` targets a TLS service port with no `BackendTLSPolicy`, and that CRD is not installed. API keys currently require port-forwarding to maas-api | upstream/MaaS |
| — | ~~Sustained load through the LLMInferenceService path and the Route (UNI-27)~~ | **Done for status tally and fairness.** 240s closed-loop runs (32 workers/tenant, `app1`/`app2`/`end-users`) against both the in-cluster gateway Service and the public Route landed 94.7% and 97.9% HTTP 200 respectively. `normalized_service` converged to within ~7% across the three backlogged groups on both paths, confirmed at multiple flight-recorder ticks through each run. On the non-200s: the Route path's are directly traced via the gateway access log to a ~2s connection/endpoint-pool warm-up burst at request-storm start (zero thereafter), not a sustained-load or fairness defect. The LLMInferenceService path's (5.3% error rate) are **inferred to be the same mechanism by analogy, not log-verified** — this cluster has no log aggregation and the gateway's own access-log buffer had already rotated past the run window by the time it was checked. Script: `deploy/poc/12-loadgen-route.sh` (Route path); `deploy/poc/04-loadgen.yaml` unchanged (LLMInferenceService path). Does **not** cover the 600s timeout / `buffer-response: false` annotations — see item 15 | N/A -- closed for status tally + fairness scope |
| — | ~~Open-loop load generation (UNI-34)~~ | **Done, and the clamp finding flips.** `deploy/poc/13-loadgen-poisson.{py,sh}` adds open-loop Poisson arrivals. Below saturation the clamp fires on ~65% of dispatches (vs 0.2–2.2% closed-loop) but is harmless (pool uncontended). Above saturation (24 req/s aggregate vs a measured ~20-22 req/s pool ceiling) it measurably **inverts** the 20/10/65 split: end-users (w=65) delivered 25.5%, app1 (w=20) delivered 40.4%. This **contradicts** the GPU closed-loop "clamp is inert" finding (`## 3`) and confirms the SUPERSEDED section's concern more strongly than originally observed. See "Open-loop (Poisson) load generation (UNI-34)" above for the full data, including what was not tested (no clamp on/off A/B — see that section for why) | **newcomerClamp default should be revisited** — a policy decision, same owner as item 2 |
| 11 | **Verify metrics reach Prometheus** | `deploy/podmonitor.yaml` exists and UWM is enabled, but no dashboard query has ever been confirmed end to end | 15 minutes |
| 12 | **Red Hat support boundary** | a custom EPP image takes that component outside RHOAI support. The plan calls this the biggest non-technical risk and it has never been raised with the account team. Nothing technical unblocks it | a conversation |
| 13 | **Version-pin maintenance** | flow-control interfaces sit on a module that only reached v1.0.0 on 2026-10-15; we are pinned to v0.11.0. Process, pinned versions and the named interface inventory are now in [version-pinning.md](version-pinning.md). Monthly check, manual — there is no CI runner | process |
| 14 | **Disconnected / mirrored clusters** | the image must be mirrored with a matching IDMS/ICSP entry. Untested, and the Quay reference assumes egress | an air-gapped target |
| 15 | **600s timeout and `buffer-response: false` under sustained/long-running load** | these annotations govern long-running and streaming responses; still only proven by single requests. UNI-27's closed-loop run used short prompts (`max_tokens: 64`, ~6-11s p95 responses), which never approaches the timeout or exercises buffering behaviour | a load generator issuing long-running/streaming requests |
| — | ~~Gateway header stripping (MaaS path, UNI-33)~~ | **Fixed and verified live.** The EPP's own header-alias resolution prefers client-settable `x-llm-d-inference-objective` over the gateway-authored `x-gateway-inference-objective`, so a client forging the former won outright regardless of what Authorino set for the latter -- proven live 2026-10-19 (a forged header passed through the gateway untouched, HTTP 200). The one-line patch to `maas-poc-gateway-authn` was applied live on 2026-10-19 once `patch` on `authpolicies.kuadrant.io` in `maas-fairness-poc` was granted, and the conformance check (`cmd/gateway-header-check`) now reports `OK` against the live cluster. Still dormant: zero `InferenceObjective` resources exist, so no behavioural queue-jump has been demonstrated, only the structural fix. See [gateway-header-stripping.md](gateway-header-stripping.md) | N/A -- closed |
| — | ~~Gateway header stripping (direct rig, UNI-43)~~ | **Fixed and verified live.** The direct rig (`02-epp.yaml`/`03-gateway.yaml`) has no Authorino layer, so UNI-33's overwrite mechanism doesn't apply -- fixed instead by removing the header outright, via an Istio `EnvoyFilter` (`envoy.filters.http.header_mutation`, `INSERT_BEFORE` `envoy.filters.http.ext_proc`) scoped to `maas-poc-route` alone so it can't also strip the value UNI-33 set for the authenticated MaaS routes sharing the same Gateway. Applied and verified live 2026-10-19 once `create`/`update` on `envoyfilters.networking.istio.io` and `pods/exec` in `maas-fairness-poc` were granted: the live config dump confirmed `header_mutation` sits immediately before `ext_proc` in the chain, and the per-route override lands on exactly one route (`maas-fairness-poc.maas-poc-route.0`), not on the MaaS routes. `gateway-header-check` still reports this route as uncovered -- a known, documented limitation (it only recognises AuthPolicy-based coverage), not a sign the fix didn't take. Not verified: an end-to-end request proving a forged header doesn't reach the EPP/simulator, since both remain scaled to 0/0. See [gateway-header-stripping.md](gateway-header-stripping.md) | N/A -- closed |
| — | ~~Reproduce the headline split on real vLLM, both modes (UNI-29)~~ | **Done.** Re-run 2026-10-22 against the live GPU deployment (now serving `llama-3-1-8b`, EPP image digest `sha256:5ef5df27...`): shadow 33.0/33.6/33.4%, enforce (sized workers) 16.2/13.7/70.1% against a 20/10/65 target. See "A4 (UNI-29): reproduced again, against the current EPP build, both modes," above, for the full data including a negative-control run and the sizing hypothesis for the ~5-point residual gap. `enforce` was restored to `true` (the live default) afterward | follow-up: tune worker sizing further to close the ~5-point gap (same section) |
| — | ~~`main` didn't deploy the image these numbers came from~~ | **Done.** That digest was in-cluster-BuildConfig-only (never pushed to Quay, not transferable), and the committed manifests were separately 31 commits stale on top of that. Rebuilt from unchanged source at `HEAD`, pushed to `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a7...`, and repinned both manifests to that digest. See "The EPP image above was not transferable, and `main` didn't deploy it — now fixed," above | — |
| 1b | **Re-run the sized-worker enforce case against the now-committed Quay digest, live** | the digest above was verified to pull and run correctly (startup log confirms the commit SHA), and the plugin source is unchanged from what was tested, but the split itself was not re-measured against this exact artifact | the stale `MutatingWebhookConfiguration` on `LLMInferenceService` admission (see "The stale webhook that blocked all of this") — needs someone who can delete a cluster-scoped `MutatingWebhookConfiguration`, which this role cannot even read |

## Reproducing

```sh
oc apply -f deploy/poc/00-config.yaml
oc apply -f deploy/poc/01-sim-backend.yaml
oc apply -f deploy/poc/02-epp.yaml      # needs the image built first
oc apply -f deploy/poc/03-gateway.yaml

oc apply -f deploy/poc/11-objective-header-removal.yaml
  # Closes UNI-43: this rig has no Authorino layer to overwrite a forged
  # x-llm-d-inference-objective with (contrast UNI-33's patch on the MaaS
  # path), so the fix here is outright removal before the EPP's ext_proc
  # call reads it. See docs/gateway-header-stripping.md. Skipping this step
  # doesn't break the fairness measurement -- the load generator never sends
  # this header -- but leaves the direct rig open to the same client-forged
  # priority bypass UNI-33 closed on the MaaS path.

oc apply -f deploy/rbac.yaml            # mints the /metrics reader token

# A/B: run once as shipped (enforce: false), then flip and re-run.
oc apply -f deploy/poc/04-loadgen.yaml
oc logs -n maas-fairness-poc job/maas-loadgen --tail=6   # status tally must be ~all 200
```

Read the result with the metrics-reader token against
`http://maas-epp:9090/metrics` (plaintext — no `--metrics-cert-dir` in the POC),
filtering on `llm_d_epp_maas_fairness_`.

### Reproducing the open-loop (Poisson) runs, on the GPU rig

Requires the GPU manifests already applied (`deploy/poc/09-vllm-gpu.yaml` and
friends — see the GPU test suite above) and `deploy/rbac.yaml` for the
metrics-reader token. Run from any host that can reach the public Route, same
as `12-loadgen-route.sh`:

```sh
# Below saturation, demand-driven, confirms the clamp fires constantly but is
# harmless when the pool isn't contended:
OPENSHIFT_TOKEN=... DURATION=240 RATE_APP1=4 RATE_APP2=4 RATE_END_USERS=4 \
  SEED=101 OUT=/tmp/run-below ./deploy/poc/13-loadgen-poisson.sh

# Above saturation (pool ceiling is ~20-22 req/s aggregate on this rig --
# calibrate with a single tenant first if the hardware changes). Expect a
# multi-minute run: the arrival window is intentionally short (90s) but
# drain of the resulting backlog can take nearly as long again:
OPENSHIFT_TOKEN=... DURATION=90 RATE_APP1=8 RATE_APP2=8 RATE_END_USERS=8 \
  SEED=104 OUT=/tmp/run-above MAX_WORKERS=3000 DRAIN_TIMEOUT=180 \
  ./deploy/poc/13-loadgen-poisson.sh
```

Each invocation prints a before/after `llm_d_epp_maas_fairness_*` metrics
snapshot and their delta, plus per-tenant client-side latency percentiles and
status-code tallies; per-request rows land in `$OUT/<group>.log` as
`arrival_epoch send_epoch latency_s http_code completion_tokens`.

**Do not Ctrl-C an overload-level run and immediately start another.**
Requests the EPP has already dispatched keep running on the backend after the
client that sent them is gone — confirm recovery with a trivial single probe
request before reusing the rig (see "a killed open-loop client does not
relieve the backend" above).
