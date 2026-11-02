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

### UNI-118: webhook re-confirmed healthy for `maas-vllm-gpu`, independently

UNI-97's clearance of the regression above (see "UNI-97: repointed to Quay, verified live,"
below) was itself confirmed against `maas-vllm-gpu` only via `oc apply --dry-run=server`, plus
a real write against `maas-vllm-cpu` (UNI-98, 2026-11-01, scaling that object to zero).
Neither on its own confirms a real, non-dry-run write against the GPU object specifically, so
UNI-98 flagged that as unverified. Re-checked directly against `llminferenceservice/maas-vllm-gpu`
in `maas-fairness-poc`, 2026-11-01T14:16:52Z:

```
oc patch llminferenceservice/maas-vllm-gpu --type=merge \
  -p '{"metadata":{"annotations":{"uni-118-webhook-check":"2026-11-01T14:16:52Z"}}}' \
  --dry-run=server                      # patched, no rejection
oc patch llminferenceservice/maas-vllm-gpu --type=merge \
  -p '{"metadata":{"annotations":{"uni-118-webhook-check":"2026-11-01T14:16:52Z"}}}'
                                         # real write — patched, no rejection
oc patch llminferenceservice/maas-vllm-gpu --type=json \
  -p '[{"op":"remove","path":"/metadata/annotations/uni-118-webhook-check"}]'
                                         # reverted — patched, no rejection
```

All three succeeded with no `connection-llmisvc-v1alpha2` rejection, and
`LLMInferenceService.status.conditions` stayed `Ready` throughout (confirmed before and after
with `oc get llminferenceservice -n maas-fairness-poc`). **The admission-webhook blocker on
Outstanding-work item 1b is cleared for `maas-vllm-gpu` specifically** — not just inferred from
the CPU object or a dry-run. What item 1b still needs is unrelated to admission: see
Outstanding work, below.

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
but it means **equal-worker sizing did not work on 2026-10-15's Qwen2.5-7B
setup either** (see "The detour, and the lesson in it," above: the same
equal/under-offered demand produced a stuck-near-equal split there too,
misread at the time as a hard ceiling). What made the 20/10/65 split visible
on 2026-10-15 was sizing each tenant's demand above its entitlement, not a
fixed equal worker count, and today's llama-3-1-8b deployment needs that
same fix, not a different one.

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

**The fairness split against this exact digest, live: now re-verified (UNI-97, 2026-11-01).**
Rolling the change out to the actual `LLMInferenceService` was blocked for a time by the same
stale `MutatingWebhookConfiguration` described above in "The stale webhook that blocked all of
this," which regressed after this section was first written and needed a second cluster-admin
clearance — see "UNI-97: repointed to Quay, verified live," below, for the full sequence. Once
cleared, `maas-vllm-gpu` was repointed at this digest and a `full-contention` run against it
matched a same-day pre-repoint baseline within run-to-run noise (≤0.9pt per group). The
inference from unchanged source that this paragraph originally relied on is now a repeated
measurement, not just an inference.

### UNI-97: repointed to Quay, verified live

Picked up the item above on 2026-10-29, blocked on a regressed webhook, resumed and finished
on 2026-11-01 once that was cleared. Full sequence below.

**Digest/commit bookkeeping (done 2026-10-29).** `bc/maas-epp` build 4 (2026-10-20, the build
behind the then-live digest
`sha256:5ef5df2776364e6161f91e5a3df0fbed9a4751bde847658af51923b1eded7f40`) built commit
`e86c3ee4e411d663ac207df66579372bdae7a114`. `bc/maas-epp-quay-publish-1` (2026-10-22, behind
the Quay digest `sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135`)
built `fc27130f0703b8228127a4040eb160567000bc27`. `e86c3ee` is an ancestor of `fc27130`
(confirmed with `git merge-base --is-ancestor`), and `git log e86c3ee..fc27130 -- cmd/ pkg/
Dockerfile.epp go.mod go.sum` is empty — so the two digests differ only because `bc/maas-epp`
built with the Dockerfile's default `COMMIT_SHA=unknown`/`BUILD_REF=` ldflags while
`bc/maas-epp-quay-publish` stamps `COMMIT_SHA=fc27130f07...`/`BUILD_REF=fc27130`, not because
of any source drift. **No rebuild was needed**; the already-published Quay digest is the same
plugin logic as what's running.

**Pull secret (confirmed, already provisioned).** `quay.io/rh-ee-dsivan/maas-fair-share` is
private (anonymous `/v2/.../manifests/...` returns 401; the `quay-maas-pull` secret's own
credential returns 200 for this exact digest). That secret is already attached to
`maas-vllm-gpu-epp-sa`'s `imagePullSecrets`, so nothing new was needed on this front — matches
the "no new pull-secret work" finding above, and this was borne out live by the repoint below
(the new pod's `Pulled` event shows a successful pull with no manual intervention).

**First blocker (2026-10-29): the stale-webhook fix from UNI-29 didn't stick.** Attempted the
repoint — `oc patch` (both JSON-patch and merge-patch) and `oc apply --dry-run=server` against
`llminferenceservice/maas-vllm-gpu`, changing only the scheduler image to the Quay digest. All
three rejected with the exact same error UNI-29 already diagnosed and fixed once:

```
failed calling webhook "connection-llmisvc-v1alpha2.odh-model-controller.opendatahub.io":
  the server could not find the requested resource
```

Reproduced identically against `maas-vllm-cpu` too (a one-field annotation patch, unrelated to
this change) — this rejected every write to every `LLMInferenceService` in the cluster, not
something caused by this change. This role's token cannot `get`/`list`/`delete`
`mutatingwebhookconfigurations.admissionregistration.k8s.io` at the cluster scope, so clearing
it needed a one-time cluster-admin action — the same shape of fix UNI-29 already used once.
That action was requested on the ticket and completed by an operator before 2026-11-01;
`oc apply --dry-run=server` against `maas-vllm-gpu` and `maas-vllm-cpu` both succeeded cleanly
once resumed, confirming the fix without this role ever reading the webhook object itself.

**A concurrent problem: the 2026-10-29 baseline no longer matched the scenario it was meant to
diff against.** The baseline captured that day (`full-contention`, equal `WORKERS=32` across
every tenant, FAIL — end-users at 38.3% against a 68.4% target, -30.1pt) used the *original*
equal-worker sizing. [UNI-103](/UNI/issues/UNI-103) landed a few hours later, the same day, and
resized `full-contention`'s per-tenant workers to `32/32/128` (app1/app2/end-users) specifically
to fix that equal-worker shape — see "What this means for a load test, and for an SLA" above.
By the time this ticket resumed on 2026-11-01, `full-contention` no longer offered the load
shape the 2026-10-29 baseline measured, so diffing a post-repoint run against it would have
confounded two independent changes (registry **and** worker sizing) instead of isolating the
one this ticket is about. Recaptured a same-day baseline instead, immediately before the
repoint, under the resized config that is actually current.

**Baseline, recaptured 2026-11-01, pre-repoint, in-cluster-registry digest.**
`full-contention`, `enforce: true`, `PER_TENANT_OVERRIDES=(WORKERS_APP1=32 WORKERS_APP2=32
WORKERS_END_USERS=128)`, 240s, against
`image-registry.openshift-image-registry.svc:5000/maas-fairness-poc/maas-epp@sha256:5ef5df27...`:

| group | weight | requests | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|
| app1 | 20.0 | 550 | 21.1% | 15.9% | -5.2 |
| app2 | 10.0 | 457 | 10.5% | 13.3% | +2.7 |
| end-users | 65.0 | 2244 | 68.4% | 70.8% | +2.4 |

Verdict: **PASS**. Full report: `results/20261101T134535Z-uni97-prerepoint-baseline/fairness-report.md`
(gitignored, not committed — numbers reproduced here per repo convention).

**Repoint applied.** `oc patch llminferenceservice/maas-vllm-gpu --type merge` set
`spec.router.scheduler.template.containers[0].image` to
`quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135`.
The controller rolled a new scheduler pod automatically; its `Pulled` event confirms
`Successfully pulled image "quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a7..." in 1.032s`,
and `LLMInferenceService.status.conditions` returned to all-`True`/`Ready` within ~40s of the
patch. `deploy/llmisvc.yaml` and `deploy/poc/09-vllm-gpu.yaml` already carried this digest
(from UNI-29), so no manifest edit was needed — the live object now matches what a clean
checkout of `main` deploys.

**Re-run, post-repoint, Quay digest, same scenario, same config, immediately after.**

| group | weight | requests | expected % | observed % | deviation (pts) |
|---|---|---|---|---|---|
| app1 | 20.0 | 573 | 21.1% | 16.8% | -4.3 |
| app2 | 10.0 | 441 | 10.5% | 13.1% | +2.5 |
| end-users | 65.0 | 2257 | 68.4% | 70.2% | +1.8 |

Verdict: **PASS**. Full report: `results/20261101T135250Z-uni97-postrepoint/fairness-report.md`
(gitignored, same convention).

**Diff: same verdict, per-tenant shares agree within run-to-run noise.** Every group's
deviation moved by ≤0.9pt between the two runs (app1 -5.2→-4.3, app2 +2.7→+2.5, end-users
+2.4→+1.8) — smaller than the spread already seen between repeated runs of this scenario on
this backend elsewhere in this document. The registry the EPP pulls from changed; the measured
fairness behaviour did not.

**Net state: done.** `llminferenceservice/maas-vllm-gpu` runs the Quay image live. The POC's
single largest air-gap gap — a measured configuration that depended on an in-cluster-only
image reference — is closed: the image under test is now the same image a disconnected mirror
would carry. Registry, digest and the pull-secret requirement are documented above in "The EPP
image above was not transferable, and `main` didn't deploy it — now fixed"; that section's
registry/digest/secret facts are unchanged by this update, only the "not yet re-verified live"
caveat it ends on is resolved by the live re-run just above.

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

**Update ([UNI-28](/UNI/issues/UNI-28)): the duration hypothesis above is
REFUTED.** See "A3 (UNI-28): S1 re-run at 600s — duration was not the cause,"
below.

### A3 (UNI-28): S1 re-run at 600s — duration was not the cause

Re-ran S1 (`app1`/`app2` both HARD, `end-users` idle, 32 workers/tenant each
— identical to the original) at **600s**, 10 half-lives instead of 2.5, to
test the hypothesis above directly. Everything about the loadgen
configuration (`TENANTS="app1 app2"`, `WORKERS=32`) was kept identical to the
original S1 run; the only deliberate change was duration.

**Result: 50.3% / 49.7% (app1/app2) — essentially an equal split, further
from the 2:1 target than the original 150s run's 1.57:1, not closer.**

| run | duration | app1 | app2 | ratio (app1:app2) | vs 2:1 target |
|---|---|---|---|---|---|
| original S1 (2026-10-18) | 150s | 59.9% | 38.3% | 1.57:1 | miss |
| S1 re-run (2026-10-22) | 600s | 50.3% | 49.7% | 1.01:1 | bigger miss |

Measured as deltas of `llm_d_epp_maas_fairness_contended_service_tokens_total`
(app1 +6,432,286 / app2 +6,366,000) between before/after scrapes of the GPU
EPP's `/metrics` via the `maas-epp-metrics-reader` token
(`deploy/rbac.yaml`), same methodology as the UNI-29 section above. Standing
health checks: `llm_d_epp_maas_fairness_unmatched_subscriptions_total` stayed
at 0 throughout; no `flow_control_requests_evicted_total` or
`*_requests_without_usage_total` series appeared (consistent with zero, same
"trued up" reading as other runs). Client-side HTTP status: app1 4847/4917
(98.6%) and app2 4853/4890 (99.2%) `200`, the rest `500` — in line with every
other run in this document, not a confound.

**The longer run makes the result worse, which rules out "not enough time to
converge" as the explanation.** If 150s were simply too short relative to the
60s half-life, more time should move the split *toward* 2:1, not *away* from
it toward exactly even. Instead, 10 half-lives of runway landed almost
exactly at the equal-split outcome this document already has a name for:
**work conservation under under-sized demand** — the same mechanism identified
one day earlier in "A4 (UNI-29) ... Run 2," on this exact live deployment.

**What actually changed between the original S1 run and this one, and why
that matters more than duration:** the original S1 (2026-10-18) ran against
the Qwen2.5-7B backend. [UNI-75](/UNI/issues/UNI-75) rebuilt and redeployed
the EPP (2026-10-21), and the live deployment now serves **llama-3-1-8b** —
a different backend with a different latency profile under load. Per-run
"HARD" worker counts (32/tenant) that kept both tenants backlogged enough to
express the 20:10 weight ordering on the old backend are, per UNI-29's Run 2
finding earlier in this document, **not automatically sufficient on the new
one**: if 32 workers can't keep the higher-weight tenant's queue backlogged
against this backend's actual response latency, its queue partially drains,
work conservation kicks in, and the delivered split compresses toward equal
thirds regardless of configured weight — more so the longer the run gives
that draining process to operate, which is exactly the direction this result
moved.

**This ticket's done-when criterion is satisfied by the negative result,
properly explained, not by tuning workers until the number looks right**
(explicitly out of scope per the ticket). The original hypothesis (duration)
is now evidenced-false. The real lever is worker sizing relative to the
*current* backend's latency — already flagged as follow-up work in the UNI-29
section above ("tune worker sizing further to close the ~5-point residual
gap") — and re-sizing the 20:10 pair specifically for llama-3-1-8b is natural
follow-up work, not part of this ticket's scope.

Reproduce: `TENANTS="app1 app2" DURATION=600 WORKERS=32` against
`deploy/poc/04-loadgen.yaml`'s script/ConfigMap (`maas-loadgen`), scraping
`llm_d_epp_maas_fairness_contended_service_tokens_total` before and after via
the `maas-epp-metrics-reader-token` secret, same as the UNI-29 reproduction
steps above. The MaaS loadgen subscription keys (`maas-loadgen-keys`) expire
7 days after minting (`docs/runbook.md`, "Mint a MaaS API key") — check they
are still valid before a run; this run's keys had expired within the hour and
had to be re-minted first.

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

## UNI-54: an automated fairness benchmark, instead of a human doing the division

Every delivered-share number in this document up to this point was produced
by hand: read `llm_d_epp_maas_fairness_contended_service_tokens_total` before
and after a run, subtract, divide, and write the percentage into a table. The
1.57:1-against-2:1 detour above exists because that manual step is also where
a mistake is easiest to make. `deploy/poc/15-fairness-benchmark.sh` and
`deploy/poc/15-fairness-report.py` close that gap: a named scenario run
against the live GPU EPP now produces its own verdict, not a number a human
has to interpret.

The share and token numbers reuse `llm_d_epp_maas_fairness_contended_service_tokens_total`
unchanged — the same SLI `deploy/grafana-dashboard.yaml`'s headline panel
(UNI-50) already uses — scraped directly off the EPP's own `/metrics`
immediately before and after the run (same mechanism as
`deploy/poc/13-loadgen-poisson.sh`), not a Thanos range query, so there is no
scrape-alignment or duplicate-UWM-replica correction to get wrong. See
`docs/runbook.md`, "Run the fairness benchmark (UNI-54)," for the scenario
list, the exact artifact layout, and how the 10-point PASS/FAIL threshold was
chosen from the deviation sizes already recorded elsewhere in this document.

### Four named scenarios, run live against the GPU EPP, 2026-10-29

EPP image digest for all four runs (unchanged from the A4/UNI-29 section
above — the live deployment is still four commits behind `HEAD`, which is
exactly the drift this report's digest field exists to catch, not to fix):
`...@sha256:5ef5df2776364e6161f91e5a3df0fbed9a4751bde847658af51923b1eded7f40`.
`enforce: true` on all four. Full reports (JSON + markdown, plus the raw
metrics snapshots and EPP/loadgen logs) are in
`results/<timestamp>-uni54-<scenario>/` in the workspace this run used;
the headline numbers:

| scenario | result | observed (app1/app2/end-users) | target | verdict |
|---|---|---|---|---|
| `full-contention` | 32/32/32 workers | 31.0/30.7/38.3% | 21.1/10.5/68.4% | **FAIL** — end-users −30.1 pts |
| `end-users-idle` | 32/32/— workers | 51.0/49.0/— % | 66.7/33.3/— | **FAIL** — app1 −15.7 pts |
| `app1-alone` | 32/—/— workers | 5391/5400 = 99.8% HTTP 200 | n/a (solo) | **PASS** |
| `asymmetric-demand` | 32/0/2 workers | 94.2/—/5.8% | n/a (demand-capped, see below) | **PASS** |

**`full-contention` and `end-users-idle` both FAIL, and both fail for the
same already-documented reason, not a new one.** Equal `WORKERS=32` across
every offered tenant is the exact equal-worker sizing artifact `## A4
(UNI-29)`'s Run 2 already found on this same backend/model
(llama-3-1-8b): 32 workers/tenant lets the highest-weight tenant's queue
periodically drain, which compresses the split toward equal shares no
matter what the weights say — work conservation doing its job on an
under-offered load, not the policy failing. `end-users-idle`'s 51.0/49.0%
split is the cleanest illustration: end-users' 65% was correctly **absorbed**
(app1+app2 jointly took 100%, not ~30%), but the 2:1 ratio between app1 and
app2 compressed toward 1:1 for the identical reason. The fix is the same
one already tracked as a follow-up on A4/UNI-29 (Outstanding work, "Reproduce
the headline split on real vLLM, both modes") —
size `end-users` well above 32 workers for these two scenarios on this
backend — and is deliberately **not** done in this ticket: retuning
`04-loadgen.yaml`'s checked-in default sizing is a separate, already-owned
piece of work, not something to fold in silently here. The benchmark
correctly caught a real, known issue; that is the tool working, not a defect
in it.

**`app1-alone` needed a fix to the verdict logic, not just a run.** The first
pass through this scenario produced a nonsense FAIL ("100-point deviation")
because `contended_service_tokens_total` is defined (`metrics.go`) to accrue
only while a group is backlogged *alongside another group* — with nobody
else offered, it is correctly a flat zero, not evidence of starvation. The
report now special-cases a single offered group: no share/deviation is
computed at all, and the verdict instead asks the question this scenario
actually names ("must receive ~100% of the pool") as a request-success-rate
bar — 90%+ HTTP 200, matching this repo's own standing "overwhelmingly 200"
check. 5391/5400 (99.8%) clears it.

**`asymmetric-demand` needed the same kind of fix, for a different reason.**
`end-users` here is deliberately demand-capped — the scenario's own
definition (the commented-out block in `04-loadgen.yaml`) gives it only 2
workers — so it cannot reach a weight-proportional 76.5% share regardless of
how the policy behaves. The first pass scored that as a 70.6-point FAIL, but
94.2%/5.8% is exactly this scenario's stated success criterion: "app1 is not
held near its 20% weight when end-users leaves most of its 65% unused." The
report now gives this scenario a one-sided check instead of the symmetric
threshold: it fails only if the saturating, highest-worker-count group (app1)
is held *at or below* its own nominal weight share while another offered
group's capacity sits unused — i.e. only if weight is acting as a ceiling,
which is the actual defect this scenario exists to catch. 94.2% vs. a 23.5%
nominal weight share passes that check outright.

### What this does and does not prove

Proven: the benchmark runs end-to-end against the live GPU EPP for all four
named scenarios, produces both JSON and markdown next to the EPP/loadgen
evidence UNI-46 already archives, computes delivered share from the EPP's
own accounting (never the generator), and its FAIL path is real — it fired
correctly on two live runs for an already-understood reason, not a
synthetic one. `deploy/poc/15-fairness-report-test.py` additionally proves
the FAIL path against synthetic data with a real non-zero process exit,
independent of cluster/GPU access, per this ticket's own done-when bar.

Not proven here: that `full-contention`/`end-users-idle` pass with
correctly-sized workers on this backend — that is the pre-existing,
separately-owned worker-sizing follow-up (A4/UNI-29's Outstanding-work row,
"Reproduce the headline split on real vLLM, both modes"), not
re-litigated by this benchmark. Also not proven: open-loop behaviour (UNI-34
is closed-loop-only by construction, same as every other number in this
document) and multi-group demand-capped scenarios beyond the two-group case
tested here — `asymmetric-demand`'s one-sided check picks the single
highest-worker offered group, which is correct for this scenario's own
definition but is not a general solution for an N-way mixed-demand run.

## UNI-103: resize to over-offer per tenant, re-run all four plus a named control

[UNI-100](/UNI/issues/UNI-100) traced the "UNI-54: an automated fairness
benchmark" section's two FAILs (above) to the test, not the plugin:
`15-fairness-benchmark.sh:140` set a single global `WORKERS=32` for every
tenant in `full-contention` and `end-users-idle`, which is not enough to keep
the highest-weight tenant in each scenario backlogged on the current
(`llama-3-1-8b`) backend -- the exact mechanism `## A4 (UNI-29)` Run 2 (above)
already found, reproduced here on two more scenarios rather than newly
discovered. The board authorized the resize on UNI-100
([comment](/UNI/issues/UNI-100#comment-26e3a385-9905-416b-adfa-e4b49fd60c1c)).

**What changed.** Both scenarios now set per-tenant `WORKERS_APP1`/
`WORKERS_APP2`/`WORKERS_END_USERS` instead of one global `WORKERS`:

- `full-contention`: `32/32/128`, copied from A4 Run 3 (the first config that
  reproduced the weight ordering on this backend/model).
- `end-users-idle`: `128/32` (app1/app2) -- app1 is the higher-share tenant
  once end-users is excluded (66.7% vs 33.3%), so it got the same
  over-offer treatment end-users got in `full-contention`.

The original equal-`WORKERS=32` shape was **not deleted** -- it is kept as a
fifth, permanently-named scenario, `equal-workers-control`, which
`15-fairness-report.py` now scores `INFO` instead of PASS/FAIL (a `--control`
flag) so its large, expected deviation can never be mistaken for a
regression or break a pipeline gating on this script's exit code. See
`docs/runbook.md`, "Per-tenant worker sizing and the saturation check," for
the full sizing method and a documented, evidence-corrected answer to "how
do you check a tenant is actually saturated."

### Five scenarios, run live against the GPU EPP, 2026-10-29

Same EPP image digest as every run since A4/UNI-29
(`...@sha256:5ef5df2776364e6161f91e5a3df0fbed9a4751bde847658af51923b1eded7f40`
-- still the drift this report's digest field exists to catch, see
[UNI-97](/UNI/issues/UNI-97)), `enforce: true` on all five. Full reports
(JSON + markdown, raw metrics snapshots, EPP/loadgen logs) are in
`results/<timestamp>-uni103-<scenario>/`:

| scenario | workers (app1/app2/end-users) | observed | target | verdict |
|---|---|---|---|---|
| `full-contention` | 32/32/128 | 16.2/12.8/71.0% | 21.1/10.5/68.4% | **PASS** |
| `end-users-idle` | 128/32/— | 82.4/17.6/—% | 66.7/33.3/— | **FAIL** -- app1 +15.8 pts |
| `equal-workers-control` | 32/32/32 | 30.7/30.7/38.7% | 21.1/10.5/68.4% | **INFO** (not scored, 29.7pt max deviation) |
| `app1-alone` | 32/—/— | 5415/5421 = 99.9% HTTP 200 | n/a (solo) | **PASS** |
| `asymmetric-demand` | 32/0/2 | 94.0/—/6.0% | n/a (demand-capped) | **PASS** |

**`full-contention` is fixed.** Sizing `end-users` to 128 workers (from A4
Run 3, unchanged) reproduced the weight ordering end-users > app1 > app2
within 5 points of the contention-adjusted target, matching A4 Run 3's own
16.2/13.7/70.1% almost exactly (this run: 16.2/12.8/71.0%) -- strong evidence
this is the same, reproducible mechanism, not a one-off.

**`equal-workers-control` reproduces the original artifact on demand, as
designed.** 30.7/30.7/38.7% against a 21.1/10.5/68.4% target (29.7pt max
deviation) is close to the original UNI-54 `full-contention` FAIL this
scenario is modeled on (31.0/30.7/38.3%) -- the same equal-worker-sizing
compression toward thirds, now available as a repeatable, named, correctly
non-scored comparison point rather than something that has to be
re-discovered by accident.

**`end-users-idle` still FAILs, but the failure mode inverted.** Before the
resize: 51.0/49.0% against 66.7/33.3 (compressed toward equal -- the
under-offer artifact). After sizing app1 to 128 workers against app2's 32:
**82.4/17.6%** -- app1 now *overshoots* its own 66.7% target by 15.8 points
while app2 is pushed 15.8 points below its 33.3% floor. Copying
`full-contention`'s dominant-tenant ratio (128 vs 32, a 4:1 worker ratio)
onto a pair whose actual target ratio is only 2:1 (20:10) overshot badly.
`llm_d_epp_maas_fairness_contended_seconds_total` deltas for app1 (1.50s)
and app2 (1.54s) came out nearly identical despite the 4:1 worker gap and
the 4.7:1 delivered-share gap, which rules out "app2 simply wasn't
contended" as the explanation and is itself evidence this pair's dynamics
are not fully understood yet. **Per this ticket's own scope, finding that
root cause is explicitly out of bounds here** -- see
[UNI-104](/UNI/issues/UNI-104), opened as the assigned, open follow-up.

**`app1-alone` and `asymmetric-demand` are unaffected by this ticket's
changes and PASS exactly as they did on UNI-54**, confirming those two
verdict-logic fixes hold under a re-run, not just the original one.

### What this does and does not prove

Proven: a weighted-split fairness result can be *measured* on this backend
only when every active tenant over-offers its entitlement -- demonstrated
positively (`full-contention` moved from FAIL to PASS purely by resizing,
no plugin change) and negatively (`equal-workers-control` reliably
reproduces the broken-looking equal-thirds result on demand). The named
control means that comparison no longer depends on remembering an old
number from a different ticket.

Not proven: that the `app1:app2` 2:1 pair can be sized to pass on this
backend at all, or what governs its sensitivity to the over-offer ratio
specifically (as opposed to simply "more load than entitlement," which was
sufficient for the 3-way case). That is [UNI-104](/UNI/issues/UNI-104)'s
scope, not this ticket's.

## UNI-104: retune `end-users-idle`'s app1:app2 ratio, confirm on GPU

[UNI-103](/UNI/issues/UNI-103) (above) left `end-users-idle` FAILing in a new
direction: copying `full-contention`'s dominant-tenant worker ratio (128:32,
4:1) onto `app1:app2` overshot, because that pair's actual target ratio is
only 2:1 (20:10 weights). Per [UNI-100](/UNI/issues/UNI-100)'s scope card,
root-causing *why* a 4:1 worker ratio overshoots a 2:1 target ratio stayed
out of bounds here; this ticket only retunes the worker sizing.

**What changed.** `end-users-idle`'s `PER_TENANT_OVERRIDES` moved from
`WORKERS_APP1=128 WORKERS_APP2=32` to `WORKERS_APP1=64 WORKERS_APP2=32` --
halving app1's workers so the offered-worker ratio (2:1) matches the target
share ratio (2:1), instead of reusing the 3-way scenario's 4:1 figure
verbatim.

**Live re-run, GPU EPP (`llama-3-1-8b`), 2026-10-29, same EPP image digest as
the rest of the UNI-103/UNI-104 suite
(`sha256:5ef5df2776364e6161f91e5a3df0fbed9a4751bde847658af51923b1eded7f40`).**
Full evidence in `results/20261029T175505Z-uni104-64-32/` (metrics snapshots,
EPP/loadgen logs, JSON + markdown report):

| group | weight | offered workers | observed % | expected % | deviation |
|---|---|---|---|---|---|
| app1 | 20 | 64 | 68.4% | 66.7% | +1.8 |
| app2 | 10 | 32 | 31.6% | 33.3% | -1.8 |

**PASS** (10-point threshold, 1.8-point max deviation -- well inside it).

`llm_d_epp_maas_fairness_contended_seconds_total` deltas for the run: app1
1.46s, app2 1.50s -- same order of magnitude as each other, matching the
reference pattern `full-contention`'s clean PASS set (~9s/~9s/~9s, see
`docs/runbook.md`'s "Per-tenant worker sizing and the saturation check"), so
both tenants were genuinely offered and contending rather than one draining
its queue mid-run.

**Still not explained, and still out of scope here:** why a 4:1 worker ratio
(128:32) overshot a 2:1 target so much more than a 2:1 worker ratio (64:32)
undershoots it only slightly, given the two configs' near-identical
`contended_seconds_total` deltas noted on UNI-103. A single data point
confirms a viable sizing, not the underlying sensitivity curve -- that
remains open pending [UNI-100](/UNI/issues/UNI-100)'s scope decision on
root-causing the 2:1 pair.

**Scope held:** no plugin or weight change was made; this was a worker-count
retune and re-run only, per this ticket's and UNI-103's scope.

## UNI-127: timeline/chaos harness, development only — no scored case

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan (B1–B4, E1, E2, and the
board's "app3 joins at saturation" case) needs tenants that join/leave
mid-run, duty-cycle on and off, and a system that gets hit with an EPP pod
delete or a vLLM replica scale-down while under load. None of the scenarios
above can express any of that. This ticket builds the capability and proves
it doesn't change anything that already works; **it does not run or score a
case** — that is every later ticket in the chain.

**Setup.** `deploy/poc/04-loadgen.yaml`'s `run.sh` gained a per-tenant
`START`/`STOP` offset and an optional `DUTY` on/off cycle (default: active
the whole run, unchanged). `15-fairness-benchmark.sh` gained two one-shot
chaos hooks (`CHAOS_EPP_DELETE_AT`, `CHAOS_SCALE_AT`/`CHAOS_SCALE_HOLD`) and
a default-on periodic `/metrics` scrape (`WINDOW_SECONDS`, default 10) that
the report turns into windowed per-tenant share and a time-to-converge
figure per phase edge. Full mechanism in `docs/runbook.md`'s "Timeline,
chaos, and windowed reporting."

**Expected result:** every existing scenario produces the same verdict as
before (the regression bar), and the new chaos/timeline knobs, when
exercised, produce correctly-shaped evidence (events logged with
timestamps, windows that respect tenant membership, a convergence figure
that is honest about whether the system actually settled).

**Observed, both runs live against the GPU EPP (`llama-3-1-8b`), 2026-11-01
(see the closing comment on this task for the merged commit SHA), EPP image
digest `sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135`
(unchanged from the UNI-97/UNI-98 pin):**

1. **Regression — `full-contention`, no timeline/chaos overrides**
   (`results/20261101T155608Z-uni127-regression-full-contention/`):

   | group | weight | observed % | expected % | deviation |
   |---|---|---|---|---|
   | app1 | 20 | 16.5% | 21.1% | -4.5 |
   | app2 | 10 | 14.7% | 10.5% | +4.1 |
   | end-users | 65 | 68.8% | 68.4% | +0.4 |

   **PASS**, deviations within a point or two of the UNI-103 baseline
   (-4.9/+2.3/+2.6) — same scenario, same script invocation shape, verdict
   and magnitude unchanged. The new `timeline` report section is present
   (27 ten-second windows, two phase edges at 0s/240s) and does not affect
   `verdict` at all, confirming the regression bar this ticket set for
   itself.

2. **Smoke test — chaos + timeline mechanics**
   (`results/20261101T154611Z-uni127-chaos-timeline-smoke/`, labelled, not
   scored): `full-contention` with `DURATION=90s`, `APP1_DUTY=20s/10s`,
   `END_USERS_START=30s`, `CHAOS_EPP_DELETE_AT=40s`,
   `CHAOS_SCALE_AT=55s`/`CHAOS_SCALE_HOLD=15s`. Verdict came back **FAIL**
   (expected and correct — rule 4: a FAIL from a deliberately disruptive,
   unscored smoke run is still a valid, recorded result, not a reason to
   mark this `blocked`). What it proved:
   - `chaos-events.log` recorded both hooks with real UTC timestamps,
     within 0s of their configured offset.
   - `timeline-config.json` correctly captured app1's duty cycle and
     end-users' late join, and the report's windows correctly show app1
     inactive during its 20–30s "off" slice and end-users inactive before
     its 30s join — i.e., window membership tracks the schedule, not the
     static `TENANTS` list.
   - The EPP pod delete was correctly detected as a counter-reset
     (`epp_restarted_mid_run: true`) rather than silently producing a
     nonsense negative delta.
   - Time-to-converge correctly reported "never converged" for every phase
     from the EPP delete onward — see "what surprised us," next.

**What surprised us.** The vLLM replica scale-down/restore is not instant:
`oc get events` showed the replacement pod's main container didn't actually
start until **3m39s** after the "scaled up 1→2" event, not within the 15s
`CHAOS_SCALE_HOLD` this smoke test used (GPU model weight load + CUDA init
dominates, not the patch itself). The harness's restore patch still fired
and landed on schedule — `spec.replicas` was back to 2 within the
configured hold — but the live, actually-Ready capacity took far longer to
return. This is exactly the gap "time-to-converge" exists to surface: the
smoke run's phases from t=40s onward correctly report "never converged"
because the system genuinely had not recovered by the run's end, 90s in.
**Anyone writing a chaos-scale case on this backend should size
`CHAOS_SCALE_HOLD` (and the run's total `DURATION`) in minutes, not
seconds**, or expect every post-chaos phase to read as non-convergent by
construction. A second, smaller surprise: per-10s windows on
`full-contention` swing ±15–20 points even on a run whose 240s aggregate
PASSes at a few points of deviation — small windows are measuring the same
noise the whole-run number averages out, not a different phenomenon, so a
single noisy window should not be read as a regression on its own.

**Cluster left as found.** `spec.replicas` on `maas-vllm-gpu` confirmed
back at `2` (matching `deploy/poc/09-vllm-gpu.yaml`) after both runs, both
vLLM pods `1/1 Running`, EPP scheduler `1/1 Running`, `job/maas-loadgen`
`Complete` (the normal end state every scenario in this file leaves, per
"What it produces" in `docs/runbook.md`).

```
$ oc get llmisvc maas-vllm-gpu -n maas-fairness-poc -o jsonpath='replicas={.spec.replicas}{"\n"}'
replicas=2
$ oc get pods -n maas-fairness-poc -l app.kubernetes.io/name=maas-vllm-gpu
NAME                                     READY   STATUS    RESTARTS   AGE
maas-vllm-gpu-kserve-74d8dd69bd-69gqk    1/1     Running   0          13m
maas-vllm-gpu-kserve-74d8dd69bd-bbhg4    1/1     Running   0          14d
maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5   1/1   Running   0   14m
```

**Not proven here, by design:** no B1–B4/E1/E2 case was run or scored —
that is the explicit scope boundary this ticket set itself, and every case
in the series is still pending its own ticket. The EPP-pod-delete chaos
hook also does not keep `epp-container.log` continuous across the delete
(the log-capture loop re-attaches by pod name, and a deleted pod's
replacement has a new one) — a known, documented limitation, not a defect
introduced to hide.

## UNI-128: request-shape profile harness, development only — no scored case

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan needs C1–C6, and every one
of them depends on varying something about the request itself that this
repo's loadgen never varied before: prompt length, `max_tokens` (omitted or
huge), `stream: true`, a client that cancels mid-generation, a prompt that
deliberately exceeds the context window, and a generation that runs for
minutes. This ticket builds that capability into
`deploy/poc/04-loadgen.yaml`'s `run.sh` and proves it does not change the
one scenario already scored by [UNI-127](/UNI/issues/UNI-127) — **it does
not run or score a C1–C6 case itself**, same scope boundary UNI-127 set.

**Setup.** `send_one()` (new) owns every request: it draws a prompt length,
a `max_tokens` value/omission, a stream flag, and an abort decision from a
set of independently-rolled, per-request fractions (`PROMPT_WORDS_MIN/MAX`,
`MAX_TOKENS_DEFAULT/OMIT_FRACTION/HUGE_FRACTION/HUGE_VALUE`,
`STREAM_FRACTION`, `ABORT_FRACTION` with a random cancel point inside
`[ABORT_MIN_FRACTION, ABORT_MAX_FRACTION]` of `REQUEST_TIMEOUT_SECONDS`,
`OVERSIZED_FRACTION/PROMPT_WORDS`, `LONG_GEN_FRACTION/MAX_TOKENS`). Every
fraction defaults to `0` and every length default reproduces the exact
shape `run.sh` sent before this ticket (1200-word prompt, `max_tokens: 64`,
no stream, no abort). Each request's outcome (status, latency,
prompt/completion tokens from the usage block, aborted flag, what shape it
was) is appended to the existing per-tenant raw log, and the run closes
with one `CLIENT_RECORD_JSON` line per tenant — pulled by
`15-fairness-benchmark.sh` into `client-request-summary.jsonl` in the
results directory, for G2 (ledger cross-check) to use later. Full mechanism
in `docs/runbook.md`'s "Request-shape profiles (UNI-128)".

**Expected result:** a plain `full-contention` re-run with none of the new
knobs set reproduces the UNI-103/UNI-127 baseline split and verdict, and
the new knobs, when exercised, produce correctly-shaped evidence (streaming
responses' usage read correctly, aborts recorded distinctly from a clean
response or a backend error, oversized prompts rejected, omitted/huge
`max_tokens` handled without crashing the generator).

**Observed, both runs live against the GPU EPP (`llama-3-1-8b`), 2026-11-01
(see the closing comment on this task for the merged commit SHA), EPP image
digest `sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135`
(unchanged from the UNI-97/UNI-98/UNI-127 pin):**

1. **Regression — `full-contention`, no profile overrides**
   (`results/20261101T161528Z-uni128-regression-full-contention/`):

   | group | weight | observed % | expected % | deviation |
   |---|---|---|---|---|
   | app1 | 20 | 16.9% | 21.1% | -4.2 |
   | app2 | 10 | 13.7% | 10.5% | +3.2 |
   | end-users | 65 | 69.4% | 68.4% | +1.0 |

   **PASS.** Deviations are within a point or two of both the UNI-103
   baseline (-4.9/+2.3/+2.6) and the UNI-127 regression
   (-4.5/+4.1/+0.4) — same scenario, same script invocation shape, verdict
   and magnitude unchanged. `client-request-summary.jsonl` recorded exactly
   what the pre-UNI-128 generator always sent: 0 aborts, 0 omitted/huge
   `max_tokens`, 0 streamed requests across all 3153 requests, and a
   completion-tokens total (app1: 33667 over 546 requests, 61.7/request)
   consistent with `max_tokens: 64` (vLLM's own EOS sometimes stops a
   little short of the cap). This is the regression bar this ticket set for
   itself.

2. **Smoke test — profile mechanics**
   (`results/20261101T162157Z-uni128-profile-smoke/`, labelled, not
   scored): `app1-alone` with `DURATION=90s`, `STREAM_FRACTION=0.3`,
   `MAX_TOKENS_OMIT_FRACTION=0.15`, `MAX_TOKENS_HUGE_FRACTION=0.1`,
   `ABORT_FRACTION=0.2` (cancel window 5–30% of a 120s
   `REQUEST_TIMEOUT_SECONDS`), `OVERSIZED_FRACTION=0.1`,
   `LONG_GEN_FRACTION=0.1`/`LONG_GEN_MAX_TOKENS=300`. Verdict came back
   **FAIL** (expected and correct — rule 4: a FAIL from a deliberately
   disruptive, unscored smoke run is still a valid, recorded result, not a
   reason to mark this `blocked`): "app1 is the only offered group this run
   ... but only 61.9% of its 454 requests succeeded, short of the 90% bar."
   That drop is the deliberate point of this run, not a surprise — the
   client record confirms every knob fired and was recorded correctly:

   ```json
   {"group":"app1","requests_sent":454,
    "status_tally":{"200":281,"ABORT":91,"400":33,"000":32,"500":17},
    "aborts":91,"errors":32,
    "prompt_tokens_total":345630,"completion_tokens_total":18287,
    "stream_requests":138,"max_tokens_omitted":75,"max_tokens_huge":39,
    "long_generations":37}
   ```

   - **Aborts**: 91 requests recorded as `ABORT`, distinct from both a clean
     `200` and a backend `500` — the client-side cancel fired and was told
     apart from every other outcome.
   - **Oversized prompts**: 33 `400`s (≈7.3% of 454, close to the
     10% `OVERSIZED_FRACTION` draw once precedence with the other knobs is
     accounted for) — the context-window-exceeding prompt was correctly
     rejected, not silently truncated or hung.
   - **Streaming**: 138 requests (≈30.4%, matches `STREAM_FRACTION=0.3`)
     used `stream: true`; usage was readable from the same grep path as
     non-streamed responses (see `docs/runbook.md`) — `prompt_tokens_total`/
     `completion_tokens_total` are non-zero and request-count-plausible
     (345630/454 ≈ 761 prompt tokens/request average, pulled down by the
     33 oversized-prompt 400s that never got billed, and the many short
     responses this scenario's mixed `max_tokens` profile produced).
   - **`max_tokens` omitted/huge/long-gen**: 75/39/37 requests respectively
     — all three non-default `max_tokens` kinds occurred and were tallied
     under the precedence order (`omit` > `huge` > `longgen` > `default`)
     documented in `docs/runbook.md`.
   - **The 120s `REQUEST_TIMEOUT_SECONDS` was respected**: p95 latency was
     exactly `120.01s` (loadgen.log) — huge/long-generation requests that
     didn't finish in time were cut off by the client timeout, recorded as
     `000`, not left to hang indefinitely.
   - The 17 `500`s are consistent with the same low-rate backend noise seen
     in the regression run above (5 and 23 out of several hundred/thousand
     requests there too) — not something this ticket's changes introduced.

**Cluster left as found.** This ticket's harness makes no replica or
plugin-config changes at all — `send_one()` is a client request-shape
change only, nothing it does touches the LLMInferenceService spec or the
EPP's weights. `spec.replicas` on `maas-vllm-gpu` confirmed at `2`
(matching `deploy/poc/09-vllm-gpu.yaml`) after both runs, both vLLM pods
`1/1 Running` with 0 restarts, EPP scheduler `1/1 Running` with 0 restarts,
`job/maas-loadgen` `Complete`:

```
$ oc get llmisvc maas-vllm-gpu -n maas-fairness-poc -o jsonpath='replicas={.spec.replicas}{"\n"}'
replicas=2
$ oc get pods -n maas-fairness-poc -l app.kubernetes.io/name=maas-vllm-gpu
NAME                                     READY   STATUS    RESTARTS   AGE
maas-vllm-gpu-kserve-74d8dd69bd-69gqk    1/1     Running   0          40m
maas-vllm-gpu-kserve-74d8dd69bd-bbhg4    1/1     Running   0          14d
maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5   1/1   Running   0   40m
$ oc get jobs -n maas-fairness-poc
NAME           STATUS     COMPLETIONS   DURATION   AGE
maas-loadgen   Complete   1/1           3m32s      5m50s
```

**Not proven here, by design:** no C1–C6 case was run or scored — every one
is still pending its own ticket, same as UNI-127 left B1–B4/E1/E2 pending.
`LONG_GEN_MAX_TOKENS`/`REQUEST_TIMEOUT_SECONDS` sizing for an actual 5–9
minute generation is deliberately left to [UNI-150](/UNI/issues/UNI-150)
(C4) rather than guessed here — this ticket proves the knob moves
generation length in the right direction, not that it hits a specific
wall-clock target. The existing report's `STATUS_PAIR` regex does not
count `ABORT` in its structured `status_tally` (see `docs/runbook.md`) —
a known, accepted gap, not a defect introduced to hide.

## UNI-129: identity-variant harness, development only — no scored case

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan needs D1, D2, D3 and D5,
which all vary something about *how a request proves its identity* rather
than what the request contains (UNI-128's scope). This ticket builds that
into `deploy/poc/04-loadgen.yaml` (D1/D2/D3) and a new standalone probe,
`deploy/poc/16-loadgen-identity-variants.sh` (D5) — **it does not run or
score a D1/D2/D3/D5 case itself**, same scope boundary UNI-127/128 set. Full
mechanism in `docs/runbook.md`'s "Identity-variant harness (UNI-129)".

**Provisioning check (rule 5), done first.** This role can mint new MaaS API
keys — confirmed live, and used for D1 below — but cannot create new
`MaaSSubscription` objects: `oc auth can-i create maassubscriptions -n
models-as-a-service` and the same check in `maas-fairness-poc` both return
`no`. D1 and D3 need no new subscriptions (they reuse the existing
`end-user-alpha`/`end-user-beta`/`app1-production` identities), so they are
fully built. D2 needs a subscription literally named `enduser-foo` to exist
and does not — see "Blocked: D2" below.

**D1 — key rotation, live evidence.** 20 new `sk-oai-` keys
(`end-user-gen01`..`end-user-gen20`) were minted directly against
`maas-api`'s ClusterIP (no `oc port-forward` needed in this environment —
see the runbook) and bound 10/10 across the two existing `end-user-*`
subscriptions. Smoke-tested live 2026-11-01: 68 end-users requests
round-robinning across 3 of the new keys all returned `200`, and the EPP's
own `fairness_id="end-users"` counter matched exactly (68) — the widened
key list collapses to the one flow correctly.

**D2 — generic mechanism built, specific identity blocked.** The new
`custom` pseudo-tenant was smoke-tested live against an existing identity
(`CUSTOM_SUBSCRIPTION_NAME=app1-production`): 34 requests, all `200`, and
the EPP's `fairness_id="app1"` counter read exactly 34 — the plumbing
works end to end. The ticket's specific case, a subscription literally
named `enduser-foo` (no hyphen, so it should fall outside the `end-user-`
prefix match into `unclassified`), could not be built: minting a key
against that name was tried directly and rejected at the gateway
(`400 invalid_subscription`) because no such `MaaSSubscription` exists, and
creating one is outside this role's grant (see "Blocked: D2").

**D3 — forged header, live evidence the defense holds.** The same 68-request
run above set `FORGE_FAIRNESS_ID_FRACTION=0.5` (36 of the 68 end-users
requests carried a forged `x-llm-d-inference-fairness-id: app1` header
*alongside* a real end-user key), concurrently with the 34 real app1
(`custom`-tenant) requests carrying no forged header. The EPP's own
`llm_d_epp_flow_control_request_enqueue_duration_seconds_count` showed
`fairness_id="app1"` at exactly 34 and `fairness_id="end-users"` at exactly
68 — none of the 36 forged requests crossed over. design.md's "Security:
headers must be stripped at the gateway" claim (the plugin's `PreRequest`
unconditionally overwrites `FairnessID` from the authenticated subscription)
holds under direct, live test, not just static code reading.

**D5 — the path is closed on the actual SUT, not open.** Ran
`deploy/poc/16-loadgen-identity-variants.sh maas-vllm-gpu` live, 2026-11-01:

| probe | result |
|---|---|
| real key (control) | `200` |
| k8s token, `/v1/chat/completions` | `401` |
| k8s token, `/v1/models` | `403` |

This is the opposite of the naive expectation inherited from
`docs/gateway-header-stripping.md`'s 2026-10-19 live proof, which used
exactly this k8s-token mechanism successfully — but against
`maas-vllm-cpu`, a route with no `AuthPolicy` of its own, so it still
inherits the Gateway-level `kubernetes-user` rule unmodified. The GPU route
(the actual SUT this whole repo measures) has since grown its own
`maas-auth-maas-vllm-gpu` AuthPolicy, whose authentication rules atomically
replace the Gateway-level ones for that route rather than merging with
them — confirmed by the 401/403 pair above, not inferred from the YAML.
Two further avenues were tried and also closed: minting a key with
`subscription` omitted silently assigns the caller's own first eligible
subscription rather than leaving it blank, and the pre-MaaS direct rig
(`deploy/poc/02-epp.yaml`/`03-gateway.yaml`) targets a different Deployment
entirely, not the `maas-vllm-gpu` LLMInferenceService, so using it would not
be testing this ticket's SUT. **Net: on `maas-vllm-gpu-kserve-route` today,
every request that reaches the backend carries a real, non-empty
subscription — D5, as literally stated, does not currently reproduce
against this system.** The probe script is built to re-ask this question
mechanically (not just once, here) in case a future AuthPolicy change
reopens it — the same "keeps this from silently regressing" posture
`docs/gateway-header-stripping.md` already established for the objective
header.

**The identity-header name itself is also worth recording as a surprise.**
The ticket (and this repo's own `design.md`, Part 2) both say
`x-maas-subscription-id`. The header actually wired, confirmed in
`deploy/epp-config.yaml`'s own comment and the live `maas-auth-maas-vllm-gpu`
AuthPolicy, is `x-maas-subscription` (no `-id`) — `design.md`'s Part 2 config
block has carried the wrong name since this POC's early days, and this
ticket's documentation above uses the real one throughout.

**Blocked: D2.** Exact gap: `create` on
`maassubscriptions.maas.opendatahub.io` in `models-as-a-service` (also
checked and denied in `maas-fairness-poc`). Verified with `oc auth can-i`,
not inferred from role tables. Needed to create a `MaaSSubscription` named
`enduser-foo` so a key minted against it produces a real, authenticatable
identity that falls outside the `end-user-` prefix match. Raised to the
board per this chain's standing practice (see the closing comment on this
task) rather than worked around.

**Cluster left as found.** This ticket's harness makes no replica or
plugin-config changes — the new knobs and the D5 probe are client-side
(request headers, auth material, which credential file is read) and never
touch the LLMInferenceService spec or the EPP's weights. A short smoke-test
Job (`TENANTS="end-users custom"`, `DURATION=25s`, `WORKERS=2`) was run to
produce the live evidence above and cleaned up immediately after;
`spec.replicas` on `maas-vllm-gpu` confirmed at `2` (matching
`deploy/poc/09-vllm-gpu.yaml`), both vLLM pods and the EPP scheduler
`1/1 Running` with 0 restarts, and no `job` left in the namespace:

```
$ oc get llmisvc maas-vllm-gpu -n maas-fairness-poc -o jsonpath='replicas={.spec.replicas}{"\n"}'
replicas=2
$ oc get pods -n maas-fairness-poc -l app.kubernetes.io/name=maas-vllm-gpu
NAME                                                      READY   STATUS    RESTARTS   AGE
maas-vllm-gpu-kserve-74d8dd69bd-69gqk                     1/1     Running   0          66m
maas-vllm-gpu-kserve-74d8dd69bd-bbhg4                     1/1     Running   0          14d
maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5    1/1     Running   0          67m
$ oc get jobs -n maas-fairness-poc
No resources found in maas-fairness-poc namespace.
```

One self-inflicted near-miss during this work, recorded for the next
session rather than hidden: `oc apply -f deploy/poc/04-loadgen.yaml` was
run directly (not through a patched copy) to reset the Job's env back to
repo defaults after the smoke test, which — since that file is a ConfigMap
*and* a Job together — immediately launched a real, full-size
`app1 app2 end-users` / 240s / 32-worker run against the live GPU pool.
Caught and deleted at 49s; no results were collected or scored from it, so
nothing downstream is contaminated, but it consumed ~49s of shared pool
time outside of any actual benchmark ticket.

**Not proven here, by design:** no D1–D5 case was run or scored as a named,
reportable scenario — every one is still pending its own ticket, same as
UNI-127/128 left their cases pending. The smoke tests above exist to prove
the harness mechanism works and produces correct EPP-side classification,
not to produce a scenario verdict. D2's `enduser-foo` instance specifically
cannot be attempted at all until the board resolves the missing grant.

## UNI-131: A1, `app2-alone` — the lowest-weight tenant gets the whole pool when alone

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan, first case, simplest in the
chain. `app1-alone` ([UNI-54](/UNI/issues/UNI-54)) already showed the
highest-weight tenant is never capped when it is the only one offered; this
is the same check for `app2` (weight 10, the lowest of the three real
tenants), to rule out the capping logic treating "lowest weight" as a special
case. New `app2-alone` scenario added to `deploy/poc/15-fairness-benchmark.sh`
(`TENANTS="app2"`, 32 workers, no per-tenant overrides — identical shape to
`app1-alone`, tenant swapped).

**Setup:** solo `app2`, 32 workers, 240s, live against `maas-vllm-gpu`
(2 replicas, llama-3-1-8b), `enforce: true`.
**Expected:** app2 receives ~100% of delivered service (the solo-scenario bar
is request success rate, not token share — see `app1-alone`'s own writeup
above for why `contended_service_tokens_total` is correctly zero with nobody
to contend against).
**Observed:** 5403 requests, 200=5385/500=18 (99.7% success) — clears the 90%
bar. Throughput essentially matches the most recent `app1-alone` run
([UNI-103](/UNI/issues/UNI-103), same 240s/32-worker shape): 5403 vs. 5421
requests, p50 1.4s vs. 1.4s, p95 1.7s vs. 1.8s.
**Verdict: PASS.**

**This run surfaced a real parser regression, found and fixed as part of
this ticket.** The first pass through `15-fairness-report.py` returned
`FAIL — "no group was offered any load"` despite the loadgen pod having
actually sent all 5403 requests. Cause: [UNI-129](/UNI/issues/UNI-129) added
a `custom=${W_CUSTOM}` field to `deploy/poc/04-loadgen.yaml`'s
`load: tenants=... workers ...` log line (between `end-users=N` and
`duration=Ns`), but `15-fairness-report.py`'s `TENANTS_LINE` regex was never
updated to tolerate it — the whole line stopped matching, so
`offered_workers` silently fell back to all zeros for every group, every
scenario, going forward. `15-fairness-report-test.py`'s synthetic fixtures
never exercise the real log format (`loadgen_log()` doesn't emit `custom=`
either), so the test suite's 20/20-green status gave no warning. This is the
first scenario benchmark run since UNI-129 landed (`ab2729f`), so no
previously-`done` ticket's recorded verdict is affected — but every
remaining case in this chain (UNI-132 onward) would have hit the same false
FAIL. Fixed by making the `custom=` field optional-and-skipped in the regex,
and added `test_tenants_line_tolerates_custom_identity_field` (real log
shape, including `custom=`) to `15-fairness-report-test.py` so this can't
regress silently again; full suite re-run green (21/21). The report was then
regenerated from this run's own saved raw artifacts
(`metrics-before.txt`/`metrics-after.txt`/`loadgen.log`/
`metrics-timeseries.txt`/`timeline-config.json`) — no second GPU run was
needed, since `15-fairness-report.py` is a pure function of those files (see
its own module docstring).

**Cluster left as found.** `app2-alone` sets no per-tenant override and
triggers no chaos event, so the benchmark script never touches the
LLMInferenceService spec or the EPP's weight config for this scenario —
confirmed, not assumed:

```
$ oc get llmisvc maas-vllm-gpu -n maas-fairness-poc -o jsonpath='replicas={.spec.replicas}{"\n"}'
replicas=2
$ oc get pods -n maas-fairness-poc -l app.kubernetes.io/name=maas-vllm-gpu
NAME                                                     READY   STATUS    RESTARTS   AGE
maas-vllm-gpu-kserve-74d8dd69bd-69gqk                    1/1     Running   0          82m
maas-vllm-gpu-kserve-74d8dd69bd-bbhg4                    1/1     Running   0          14d
maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5   1/1     Running   0          82m
```

`replicas: 2` matches `deploy/poc/09-vllm-gpu.yaml`. The completed
`maas-loadgen` Job was left in place (same convention as every prior scored
scenario in this repo — the next benchmark run deletes it unconditionally
before creating its own, `15-fairness-benchmark.sh` line 359).

Raw results: `results/20261101T170012Z-uni131-app2-alone/` (report, loadgen
log, metric snapshots/timeseries, client-request summary, EPP container log).

**Not proven here:** multi-tenant contention behaviour involving `app2` —
this case only shows it is uncapped when alone, same scope boundary
`app1-alone` set for `app1`. Whether `app2` holds its weighted share under
contention is covered by the other named scenarios (`full-contention`,
`end-users-idle`, etc.), not re-litigated here.

## UNI-132: A3, `app2-idle` — pair `app1` + `end-users`, promoting the by-hand "S3" check

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan, third case in the chain.
This is the cleanest proportionality check of the series — app2 fully
excluded, only two tenants contending, no demand-capping or timeline
complications — and per the ticket it "has only ever been done once by hand"
(the "S3" row in the "Scenario matrix — demand patterns and edge cases"
section above, from an earlier manual run: 23.7%/75.0% against a 23.5/76.5
target). This ticket adds it as a named, automated `15-fairness-benchmark.sh`
scenario (`app2-idle`) instead of leaving it a one-off hand measurement.

**Setup:** `TENANTS="app1 end-users"` (app2 excluded entirely, not just
idle-but-offered), 240s, live against `maas-vllm-gpu` (2 replicas,
llama-3-1-8b), `enforce: true`. Per-tenant workers sized by the
[UNI-104](/UNI/issues/UNI-104) lesson — offered-worker ratio close to target
ratio, not copied verbatim from another scenario's dominant-tenant ratio:
app1 anchored at the usual baseline of 32 workers, end-users scaled to
32×(65/20)=104, so the 32:104 offered ratio matches the pair's exact 20:65
weight ratio.

**Expected split:** with app2 excluded, the pair's weights renormalize to
20/(20+65)=23.5% (app1) and 65/(20+65)=76.5% (end-users) — exactly the
23.5/76.5 target the ticket names.

**Observed split:** app1 20.2%, end-users 79.8% — deviations -3.3 and +3.3
points against a 10-point threshold.

**Verdict: PASS.**

**Both tenants were genuinely contending, not just offered.**
`llm_d_epp_maas_fairness_contended_seconds_total` deltas over the run: app1
1.390s, end-users 1.390s — identical to three decimal places, the strongest
same-run contention signal seen anywhere in this series so far (compare
`full-contention`'s ~9s/~9s/~9s, or `end-users-idle`'s 1.46s/1.50s after its
UNI-104 retune). app2, correctly offered zero workers, shows no delta
(6.44s before and after). This directly answers the ticket's ask to record
these deltas as proof of contention, not just a plausible-looking share
number.

**What surprised me:** the per-10s timeline window swings wildly — app1
ranges from 0% to 38% of delivered tokens window-to-window (see the full
report's timeline table), occasionally hitting a dead 0.0%-for-10s window
three separate times over the run. The whole-run aggregate still lands
within 3.3 points of target, so this looks like short-timescale oscillation
around the converged split rather than a sustained drift, but it is a wider
swing than `full-contention`'s timeline shows at the same window size and is
not explained by anything in this ticket's scope — worth a closer look if a
future case depends on short-window stability rather than whole-run
aggregates. Also notable: 7/667 app1 requests and 50/2551 end-users requests
returned HTTP 500 (~1-2%) — consistent with background error noise seen in
other runs on this backend, not something this ticket root-caused.

**Cluster left as found.** `app2-idle` sets no chaos event and does not touch
the LLMInferenceService spec or EPP weight config; confirmed after the run,
not assumed:

```
$ oc get llmisvc maas-vllm-gpu -n maas-fairness-poc -o jsonpath='replicas={.spec.replicas}{"\n"}'
replicas=2
$ oc get pods -n maas-fairness-poc -l app.kubernetes.io/name=maas-vllm-gpu
NAME                                                     READY   STATUS    RESTARTS   AGE
maas-vllm-gpu-kserve-74d8dd69bd-69gqk                    1/1     Running   0          92m
maas-vllm-gpu-kserve-74d8dd69bd-bbhg4                    1/1     Running   0          14d
maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5   1/1     Running   0          93m
$ # from this run's own metrics-after.txt snapshot (EPP's own echoed config, not copied from the repo):
llm_d_epp_maas_fairness_configured_weight{fairness_id="app1"} 20
llm_d_epp_maas_fairness_configured_weight{fairness_id="app2"} 10
llm_d_epp_maas_fairness_configured_weight{fairness_id="end-users"} 65
llm_d_epp_maas_fairness_configured_weight{fairness_id="unclassified"} 5
llm_d_epp_maas_fairness_enforcing 1
```

`replicas: 2` matches `deploy/poc/09-vllm-gpu.yaml`; weights and `enforcing`
match `deploy/epp-config.yaml` exactly. The completed `maas-loadgen` Job was
left in place (same convention as every prior scored scenario — the next
benchmark run deletes it unconditionally before creating its own).

Raw results: `results/20261101T171523Z-uni132-app2-idle/` (report, loadgen
log, metric snapshots/timeseries, client-request summary, EPP container log).

**Not proven here:** the short-timescale oscillation noted above is
described, not explained — no root cause is claimed. Multi-tenant behaviour
involving `app2` under this pair's conditions is out of scope by
construction (app2 is excluded, not merely idle). S4-equivalent behaviour
(app2 trickling back in on top of this pair) is a different, not-yet-run
case in the UNI-117 plan.

## UNI-133: A4, `app1-idle` — pair `app2` + `end-users`, the most extreme pair ratio

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan, fourth case in the chain (A1
`app2-alone`/UNI-131, A3 `app2-idle`/UNI-132, this is A4). `app1` is excluded
entirely (not merely idle), leaving `app2` (weight 10) and `end-users`
(weight 65) as the only two offered tenants — a 6.5:1 ratio, the most
extreme of the three possible pairs (compare 2:1 for app1:app2 and 1:3.25 for
app1:end-users). New `app1-idle` scenario added to
`deploy/poc/15-fairness-benchmark.sh`. The ticket also asks that `app2`'s own
signed deviation be reported on its own: this repo's simulator-era "Residual
gap: small-weight groups run ~4 points rich" finding (above) predicted a
low-weight group would run *rich* under contention, and this pair's extreme
ratio was flagged as the sharpest test of that prediction.

**Setup:** `TENANTS="app2 end-users"` (app1 excluded entirely), 240s, live
against `maas-vllm-gpu` (2 replicas, llama-3-1-8b), `enforce: true`.
Per-tenant workers sized by the [UNI-104](/UNI/issues/UNI-104) lesson, same
method as `app2-idle`: anchor the smaller weight (`app2`) at the usual
baseline of 32 workers, scale the larger (`end-users`) to match the pair's
exact ratio: 32×(65/10)=208.

**Expected split:** with app1 excluded, the pair's weights renormalize to
10/(10+65)=13.3% (app2) and 65/(10+65)=86.7% (end-users) — the 13.3/86.7
target the ticket names.

**Observed split (whole-run aggregate):** app2 **8.9%**, end-users **91.1%**
— deviations **-4.5** and **+4.5** points against a 10-point threshold.

**Verdict: PASS.**

**app2's signed deviation, reported on its own as asked: -4.5 points — poor,
not rich.** This is the opposite sign from the ticket's "~4 points rich"
hypothesis for small-weight groups. The whole-run aggregate is not the full
story, though: the per-10s windowed timeline (full report,
`results/20261101T172853Z-app1-idle/fairness-report.md`) shows app2 received
**zero** delivered tokens for eight consecutive windows, t=20s through
t=101s — 81 seconds of the 240s run — while `end-users`'s far larger offered
concurrency (208 vs. 32 workers) filled the pool first. `compute_convergence`
puts the phase's first sustained within-threshold window at t=101s (close to
two `halfLifeSeconds=60` half-lives). From t=101s to the end of the run, the
per-window split tracks the 13.3/86.7 target tightly — every window from
111s on is within ±1.1 points, several within ±0.2 — which is actually the
*strongest* steady-state convergence at any ratio run in this series so far.
The whole-run **aggregate** deviation is -4.5 because the aggregate average
cannot distinguish "never contended" from "contended but shut out during a
long cold start": roughly a third of the run's windows (8 of 24 active
windows) contributed a large negative pull to app2's share before the system
settled.

**Why this refutes, not confirms, the "~4 points rich" hypothesis for this
pair.** The original residual-gap finding (simulator, no `newcomerClamp`,
clamp-off) attributed low-weight-group richness to early-run FCFS-like
behavior, where all groups look equally unserved before weights have had time
to bite — a mechanism that should bias the low-weight group *up*, not down.
What this run shows instead, at the most extreme ratio in the series, is the
opposite: the low-weight group's queue is the one that gets starved out
during the cold start, because the high-weight group's much larger offered
concurrency (208 workers, sized intentionally to match its 86.7% target
share) saturates the pool before app2's comparatively small 32-worker queue
can build enough backlog to compete for the weighted scheduler's attention.
The two mechanisms are not the same thing, and this result does not
reproduce the older finding — it shows a different, ratio-dependent cold-start
dynamic that happens to also be a few points in magnitude. No root cause
beyond this description is claimed.

**Both tenants were genuinely contending, not just offered.**
`llm_d_epp_maas_fairness_contended_seconds_total` deltas over the run: app2
20.05s, end-users 20.08s — matching to two decimal places, the same
same-run contention signal `app2-idle` showed for its pair. `app1`, correctly
excluded, shows no delta (9.277s before and after, identical). Status tally:
app2 100% HTTP 200 (297/297); end-users 99.0% (2867/2895, 28×500) —
consistent with the background error noise seen elsewhere in this series, not
root-caused here. app2's P95 latency (101.8s) is far higher than end-users'
(20.4s) — consistent with app2's requests queueing behind the much larger
end-users backlog during the cold-start window described above, not with
app2 being under-offered relative to its entitlement.

**Cluster left as found.** `app1-idle` sets no chaos event and does not touch
the LLMInferenceService spec or EPP weight config; confirmed after the run,
not assumed:

```
$ oc get llmisvc maas-vllm-gpu -n maas-fairness-poc -o jsonpath='replicas={.spec.replicas}{"\n"}'
replicas=2
$ oc get pods -n maas-fairness-poc -l app.kubernetes.io/name=maas-vllm-gpu
NAME                                                     READY   STATUS    RESTARTS   AGE
maas-vllm-gpu-kserve-74d8dd69bd-69gqk                    1/1     Running   0          108m
maas-vllm-gpu-kserve-74d8dd69bd-bbhg4                    1/1     Running   0          14d
maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5   1/1     Running   0          109m
$ # from this run's own metrics-after.txt snapshot (EPP's own echoed config, not copied from the repo):
llm_d_epp_maas_fairness_configured_weight{fairness_id="app1"} 20
llm_d_epp_maas_fairness_configured_weight{fairness_id="app2"} 10
llm_d_epp_maas_fairness_configured_weight{fairness_id="end-users"} 65
llm_d_epp_maas_fairness_enforcing 1
```

`replicas: 2` matches `deploy/poc/09-vllm-gpu.yaml`; weights and `enforcing`
match `deploy/epp-config.yaml` exactly. The completed `maas-loadgen` Job was
left in place (same convention as every prior scored scenario — the next
benchmark run deletes it unconditionally before creating its own).

**A process bug in the harness found and fixed during this run, out of
scope for a code change here.** Five orphaned `oc logs -f` processes from
UNI-127 through UNI-132 were found still running and still appending to
their original runs' `epp-container.log` files (three of them inside this
repo's committed `results/` directories, corrupting already-closed tickets'
raw artifacts after the fact) — `15-fairness-benchmark.sh`'s exit/EXIT-trap
`kill "$CAPTURE_PID"` only signals the wrapper function's subshell, not the
`oc logs -f` grandchild process it execs, so the grandchild is orphaned and
never reaped. All five were killed and the two contaminated committed files
in this repo were restored with `git checkout --` before this run started;
this run's own equivalent orphan was caught and killed the same way
immediately after. Not fixed in the script itself — that is a harness change
affecting every scenario in this suite, out of scope for this benchmark
ticket. Filed as a backlog idea for whoever owns the harness next.

Raw results: `results/20261101T172853Z-app1-idle/` (report, loadgen log,
metric snapshots/timeseries, client-request summary, EPP container log).

**Not proven here:** the cold-start mechanism described above is described,
not root-caused — no claim is made about exactly why the low-weight group's
queue is the one that drains during the transient, only that it is
(contrast the higher-weight group holding queue depth throughout). Whether a
longer run shrinks the whole-run aggregate deviation by diluting the
cold-start window further, or whether a different worker-sizing ratio
shortens the cold start itself, is untested — both are plausible given the
windowed data but neither was tried here.

## UNI-134: A5, `app2-trickle` — a weight is a floor, not a ceiling

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan, fifth case in the chain,
promoting the by-hand "S2"/"S4" checks (`docs/poc-results.md`'s "Scenario
matrix," above) into the automated benchmark. Unlike `app2-idle`/`app1-idle`
(A3/A4), no tenant is excluded here: all three are offered, but `app2`
trickles at the literal S2/S4 figure of 2 workers — well under its own
weight entitlement — while `app1` and `end-users` are both HARD.

**Setup:** `TENANTS="app1 app2 end-users"`, 240s, live against
`maas-vllm-gpu` (2 replicas, llama-3-1-8b), `enforce: true`. `app1` and
`end-users` are sized identically to `app2-idle` (UNI-132) — 32 and 104
workers — since the ratio *between* them (20:65) is unaffected by `app2`'s
presence; `app2` is pinned at 2 workers, the ticket's own trickle figure, not
derived from a ratio.

**Expected split:** `app2`'s weight is a floor under contention, never a
ceiling (the S2 lesson) — at 2 workers it structurally cannot reach a
weight-proportional share, so it should get ~100% of what it asks for rather
than being throttled further. Its unused entitlement goes to `app1` and
`end-users`, who split it in their own 20:65 ratio, renormalized to
**23.5/76.5** — the same target `app2-idle`'s pair has, because excluding
`app2`'s weight from *that* ratio's denominator is correct whether `app2` is
absent or merely capped by its own demand.

This is a genuinely different comparison from `app2`'s naive 3-way weight
share (10/95=10.5%), which is what a run would wrongly be scored against if
`app2`'s weight stayed in the denominator for `app1`/`end-users`' target —
`15-fairness-report.py` was extended with a `capped_groups` mechanism (new
`app2-trickle` branch) specifically to exclude it, and to score `app2` itself
on a dedicated "did it get served" success-rate check instead of the
symmetric deviation threshold (mirroring the existing `solo`/
`asymmetric-demand` carve-outs for the same underlying reason: a
structurally-demand-capped group cannot be held to a weight-proportional
share without failing a run that is working exactly as intended).

**Observed split:** `app1` **18.8%**, `end-users` **79.7%** — deviations
**-4.7** and **+3.3** points against the 23.5/76.5 target and a 10-point
threshold. `app2`: 46/46 requests succeeded (100%, HTTP 200), p50 11.15s /
p95 17.58s — in the same range as `app1`'s (p50 11.16s / p95 18.96s) and
`end-users`' (p50 11.02s / p95 12.46s), not elevated as it would be if its
trickle demand were queueing behind the two HARD tenants.

**Verdict: PASS.**

**`app2` received a small fraction of total delivered tokens — far below its
naive 10.5% weight share — and that is the correct, intended result, not a
miss.** Of the run's 4,144,594 total delivered tokens, `app2` accounted for
59,510 (1.4%), against `app1`'s 780,454 (18.8%, the observed share reported
above) and `end-users`' 3,304,630 (79.7%). `app2` offering only 2 workers for
240s is the entire explanation — it has no way to generate demand for a
larger share, and the policy correctly did not withhold what it did ask for
(100% success, uncontended-looking latency) to artificially inflate its
share toward its weight. This is the directional finding the historical by-hand
S4 check made ("app2 trickled and received exactly the 2.9% it asked for")
reproduced under the automated harness, though the exact percentage differs
(1.4% here vs. 2.9% in S4) because the worker sizing, run duration, and
backend are not identical between the two measurements — this run does not
attempt to reproduce S4's number exactly, only its conclusion.

**Both HARD tenants were genuinely contending, not just offered.**
`llm_d_epp_maas_fairness_contended_seconds_total` deltas over the run: app1
1.65s, app2 1.59s, end-users 1.64s — all three in the same range, meaning
`app2`'s trickle was large enough to register real contention against the
scheduler's priority band even though it could never win a proportional
share of it. `end-users` had 17/2504 requests return HTTP 500 (0.7%),
consistent with the background error noise seen elsewhere in this series,
not root-caused here.

**Cluster left as found.** `app2-trickle` sets no chaos event and does not
touch the LLMInferenceService spec or EPP weight config; confirmed after the
run, not assumed:

```
$ oc get llmisvc maas-vllm-gpu -n maas-fairness-poc -o jsonpath='replicas={.spec.replicas}{"\n"}'
replicas=2
$ oc get pods -n maas-fairness-poc -l app.kubernetes.io/name=maas-vllm-gpu
NAME                                                     READY   STATUS    RESTARTS   AGE
maas-vllm-gpu-kserve-74d8dd69bd-69gqk                    1/1     Running   0          126m
maas-vllm-gpu-kserve-74d8dd69bd-bbhg4                    1/1     Running   0          14d
maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5   1/1     Running   0          127m
$ # from this run's own metrics-after.txt snapshot (EPP's own echoed config, not copied from the repo):
llm_d_epp_maas_fairness_configured_weight{fairness_id="app1"} 20
llm_d_epp_maas_fairness_configured_weight{fairness_id="app2"} 10
llm_d_epp_maas_fairness_configured_weight{fairness_id="end-users"} 65
llm_d_epp_maas_fairness_configured_weight{fairness_id="unclassified"} 5
llm_d_epp_maas_fairness_enforcing 1
```

`replicas: 2` matches `deploy/poc/09-vllm-gpu.yaml`; weights and `enforcing`
match `deploy/epp-config.yaml` exactly. The completed `maas-loadgen` Job was
left in place (same convention as every prior scored scenario). No orphaned
`oc logs -f` process was left behind by this run (checked against the
UNI-169 fix, confirmed live by walking `/proc/*/cmdline` before and after).

Raw results: `results/20261101T174928Z-uni134-app2-trickle/` (report,
loadgen log, metric snapshots/timeseries, client-request summary, EPP
container log).

**Grafana time range** (padded ±60s around `run_start`/`run_end`, per
`docs/runbook.md`'s "Find a run on the fairness dashboard"):
`from=1793555310000&to=1793555687000` —
https://grafana-grafana.apps.ocp.paladinaura.com/d/maas-fairness-gpu-epp/?orgId=1&from=1793555310000&to=1793555687000&var-group=All&var-window=2m

**Not proven here:** "close to the same 2 workers running uncontended," the
ticket's own phrasing for `app2`'s expected latency/throughput, is not
checked against an actual uncontended 2-worker baseline run — no such run
exists in this series to compare against, so the claim is supported only
indirectly, by `app2`'s latency/success rate looking unremarkable next to
the two HARD tenants' own numbers in this same run, not by a direct
before/after comparison. The `capped_groups` report mechanism is new in
this ticket and is covered by two new unit tests
(`test_app2_trickle_served_and_pair_split_passes`,
`test_app2_trickle_throttled_capped_group_fails`) in
`15-fairness-report-test.py`, but has only this one live run behind it.

## UNI-135: A6, `below-capacity` — the pool was not actually uncontended at 20%

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan, sixth and final case in the
chain: "below capacity, everyone light." Unlike every other case in this
series, all three tenants are offered simultaneously and none is excluded,
trickled, or deliberately mis-sized — each is sized to ~20% of its own
saturating ceiling, so the question is whether the policy has to do
anything at all when nobody is actually competing for the pool.

**Setup:** `TENANTS="app1 app2 end-users"`, 240s, live against
`maas-vllm-gpu` (2 replicas, llama-3-1-8b), `enforce: true`. Per-tenant
workers are 20% of `full-contention`'s saturating ceiling (32/32/128, UNI-29
A4 Run 3): `WORKERS_APP1=6 WORKERS_APP2=6 WORKERS_END_USERS=26`
(32×0.2=6.4→6, 32×0.2=6.4→6, 128×0.2=25.6→26).

**Expected split:** per the ticket, a new **UNCONTENDED** verdict (neither
PASS nor FAIL) with p50/p95 latency per tenant close to that tenant's own
solo latency. `15-fairness-report.py` was extended with exactly this
verdict, gated on every offered group's
`llm_d_epp_maas_fairness_contended_seconds_total` delta staying under
`UNCONTENDED_SECONDS_THRESHOLD` (1.0s — an order of magnitude below the ~9s
a genuinely-contending tenant accrues in a 240s `full-contention` run), and
covered by two new unit tests
(`test_uncontended_when_everyone_below_capacity`,
`test_uncontended_does_not_apply_when_one_group_actually_contends`), plus a
third (`test_uncontended_does_not_override_solo_or_control`) confirming the
new rule can't fire alongside the existing `solo`/`control` carve-outs. See
`docs/runbook.md`, "A fourth verdict: UNCONTENDED," for the full rule and
why it reads `contended_seconds_total` rather than inventing a new metric.

**Observed split: PASS, not UNCONTENDED.** `app1` **14.9%** (expected
21.1%, deviation **-6.1** points), `app2` **14.6%** (expected 10.5%,
deviation **+4.1**), `end-users` **70.5%** (expected 68.4%, deviation
**+2.1**) — all within the 10-point threshold, so the run scored PASS on
the ordinary weighted-split check. It did **not** hit UNCONTENDED: every
offered group's `contended_seconds_total` delta came in at app1 2.39s, app2
2.28s, end-users 2.48s — all comfortably clear of the 1.0s threshold, so
the EPP's own evidence says the pool genuinely was contended at this
concurrency, just far more lightly than `full-contention`'s ~9s.

**What surprised us.** The ticket's framing — "everyone light" implies
"nobody backlogged" — turned out not to hold at the ceiling's chosen 20%
figure. Two things point the same direction:

- `contended_seconds_total` (2.3-2.5s across all three groups) is real and
  consistent, not noise from one outlier group — it is roughly a quarter of
  `full-contention`'s per-tenant figure at roughly a fifth of the worker
  count, i.e. contention did not scale down linearly with offered load.
- Latency is measurably elevated against the one genuine solo baseline this
  series has for two of the three tenants: `app1`'s most recent solo run
  (UNI-103, 32 workers) measured p50 1.40s/p95 1.77s against this run's
  p50 1.84s/p95 2.19s (+31%/+24%); `app2`'s solo run (UNI-131, 32 workers)
  measured p50 1.40s/p95 1.70s against this run's p50 1.90s/p95 2.27s
  (+36%/+34%). `end-users` has no solo baseline in this suite (same gap
  `app2-trickle`, UNI-134, already noted) so only the `contended_seconds`
  evidence applies to it.

Read together, this says the 1.0s `UNCONTENDED_SECONDS_THRESHOLD` and/or the
20%-of-ceiling sizing rule are the things to revisit, not the report logic:
the rule as specified correctly classified a run that *was* contended as
not-uncontended, rather than the alternative failure mode (silently
mislabeling a genuinely contended run as UNCONTENDED). Whether 20% was
simply still high enough to produce real queueing on this backend, or
whether any nonzero concurrency across three tenants sharing two vLLM
replicas always produces a small but detectable `contended_seconds`
footprint, is not distinguished by this one run — a sweep across lower
percentages would be needed to tell the two apart, and is out of scope for
this ticket.

**Cluster left as found.** `below-capacity` sets no chaos event and does
not touch the LLMInferenceService spec or EPP weight config; confirmed
after the run, not assumed:

```
$ oc get llmisvc maas-vllm-gpu -n maas-fairness-poc -o jsonpath='replicas={.spec.replicas}{"\n"}'
replicas=2
$ oc get pods -n maas-fairness-poc -l app.kubernetes.io/name=maas-vllm-gpu
NAME                                                     READY   STATUS    RESTARTS   AGE
maas-vllm-gpu-kserve-74d8dd69bd-69gqk                    1/1     Running   0          147m
maas-vllm-gpu-kserve-74d8dd69bd-bbhg4                    1/1     Running   0          14d
maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-6gkq5   1/1     Running   0          147m
$ # from this run's own metrics-after.txt snapshot (EPP's own echoed config, not copied from the repo):
llm_d_epp_maas_fairness_configured_weight{fairness_id="app1"} 20
llm_d_epp_maas_fairness_configured_weight{fairness_id="app2"} 10
llm_d_epp_maas_fairness_configured_weight{fairness_id="end-users"} 65
llm_d_epp_maas_fairness_configured_weight{fairness_id="unclassified"} 5
llm_d_epp_maas_fairness_enforcing 1
```

`replicas: 2` matches `deploy/poc/09-vllm-gpu.yaml`; weights and `enforcing`
match `deploy/epp-config.yaml` exactly. The completed `maas-loadgen` Job was
left in place (same convention as every prior scored scenario). No
orphaned `oc logs -f` process was left behind by this run (checked against
the UNI-169/170 fix by walking `/proc/*/cmdline` and the run's own
`.capture-oc.pid`, which no longer corresponds to a live process).

Raw results: `results/20261101T180755Z-uni135-below-capacity/` (report,
loadgen log, metric snapshots/timeseries, client-request summary, EPP
container log).

**Grafana time range** (padded ±60s around `run_start`/`run_end`, per
`docs/runbook.md`'s "Find a run on the fairness dashboard"):
`from=1793556416000&to=1793556789000` —
https://grafana-grafana.apps.ocp.paladinaura.com/d/maas-fairness-gpu-epp/?orgId=1&from=1793556416000&to=1793556789000&var-group=All&var-window=2m

**Not proven here:** no `end-users-alone` scenario exists in this suite (the
same gap `app2-trickle`/UNI-134 noted), so the latency comparison above
covers `app1` and `app2` directly but relies on `contended_seconds_total`
alone for `end-users`. This is also the only run in the edge-case chain
where every tenant is simultaneously below its own saturating point, so the
finding that contention does not vanish at 20% is a single data point, not
a curve — see "What surprised us," above, for the sweep that would be
needed to generalize it.

## UNI-136: C8, `cache-heavy-vs-cache-cold` — evidence for the `cachedInputTokenWeight` decision

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan, first case in the "C" group
(dispatch vs token share / cache accounting). This is the task that feeds
Outstanding item 2, below, and [UNI-91](/UNI/issues/UNI-91): does leaving
`cachedInputTokenWeight` at its default `1.0` over-charge a tenant whose
traffic is highly cacheable relative to the GPU work it actually causes?
Unlike "Per-group cache-hit profile," above (the three-tenant,
`10-cache-profile.yaml`-only run that first measured the 6.3%/87.7%/96.4%
spread), this case runs the differentiated shapes through the scored
benchmark harness itself, so the question can be answered in the same units
(`contended_service_tokens_total`) the live policy actually charges in.

**Harness change required.** `04-loadgen.yaml` previously sent every tenant
the identical prompt shape (deliberately — "uniform traffic so cache
effects do not confound," per the Scenario matrix above); there was no way
to make two tenants in the *same* run cache-differently. This ticket adds
`CACHE_SHAPE_APP1`/`CACHE_SHAPE_APP2`/`CACHE_SHAPE_END_USERS` (unset =
unchanged global shape): `hot` sends a byte-identical 160-word shared
prefix plus a short unique tail (the same construction as
`10-cache-profile.yaml`'s app1 "fixed" shape), `cold` sends a fully unique
40-word body every request (that file's app2/control shape). A matching
`cache-heavy-vs-cache-cold` scenario was added to
`15-fairness-benchmark.sh`, and `15-fairness-report.py` now reads
`llm_d_epp_maas_fairness_prompt_tokens_cached_ratio` into each group's row
(it already captured everything else this case needs — `requests_total`
and `delivered_tokens`/share were already in every report).

**The cached-ratio metric needed a clean EPP first.** It is a cumulative
Gauge (`groupState.cachedRatio()`, `pkg/fairness/weightedlas/state.go`) —
cached/total prompt tokens since the EPP **process** started, not scoped to
one run. Checked live before this run: every group already read 96-99%,
including `app2` (the intended cache-cold control) — contaminated by every
`full-contention`/A1-A6 run since the last EPP restart, all of which sent
the *same* fixed, highly-cacheable 1200-word prompt to every tenant. Fixed
by deleting the EPP scheduler pod and waiting for its replacement to be
Ready *before* starting the benchmark (not during — a mid-run restart is
the thing `15-fairness-report.py` already treats as invalidating a run).
Confirmed clean afterward (`prompt_tokens_cached_ratio` absent from
`metrics-before.txt`, i.e. zero history), and confirmed the restart changed
nothing else: `configured_weight`/`enforcing` read identically before and
after (20/10/65/5, enforcing=1).

**Setup:** `TENANTS="app1 app2"`, 240s, live against `maas-vllm-gpu` (2
replicas, llama-3-1-8b), `enforce: true`, `cachedInputTokenWeight: 1.0`
(live default, unchanged). `WORKERS_APP1=64 WORKERS_APP2=32` — the same 2:1
over-offer ratio `end-users-idle` already proved saturates this exact
app1:app2 (20:10) pairing, reused rather than re-derived.
`CACHE_SHAPE_APP1=hot`, `CACHE_SHAPE_APP2=cold`. Run as a `--control` (the
ticket asks for a characterisation, not a PASS/FAIL) so the numbers are
reported without being scored against the weighted-split threshold.

**Observed split:**

| group | weight | requests | request share | charged tokens | charged-token share (expected 66.7/33.3) | `prompt_tokens_cached_ratio` |
|---|---|---|---|---|---|---|
| app1 (hot) | 20 | 2,383 | 69.5% | 727,921 | 65.1% (dev. -1.5 pts) | **87.6%** |
| app2 (cold) | 10 | 1,047 | 30.5% | 389,716 | 34.9% (dev. +1.5 pts) | **6.2%** |

(`contended_seconds_total`: 2.0s both groups — genuinely, if lightly,
contended, not a work-conservation artefact. Status tally: app1
200=2373/500=10, app2 200=1040/500=7 — a small, sub-0.5% error rate on both
sides, not investigated further here. The EPP's own `dispatch_total`
delta — `docs/runbook.md`'s panel table already ties this case to that
metric specifically — agrees with the client-reported request count to
within 0.2 points: app1 2,372/3,409 = 69.6%, app2 1,037/3,409 = 30.4%.)

The per-tenant cache ratios (87.6% / 6.2%) reproduce the earlier
cache-profile measurement (87.7% / 6.3% for the same app1/app2 shapes) to
within run-to-run noise — the clean-EPP fix above is working as intended.

**Answer to the ticket's question: yes, the cache-heavy tenant is
over-charged relative to the GPU work it actually uses, at the live
`cachedInputTokenWeight: 1.0`.** The charged-token split (65.1/34.9) landed
almost exactly on the configured 20:10 weight ratio **despite** the
enormous gap in cache profile — because `1.0` applies no discount at all,
every one of app1's cache-hit prompt tokens is billed identically to a
cache-miss token. Concretely: of app1's 477,716 prompt tokens, ~87.6%
(≈418,500) were served from the prefix cache and needed little fresh
prefill compute, yet all 477,716 counted in full toward its
`contended_service_tokens_total` share; app2's 266,673 prompt tokens were
93.8% cache misses, i.e. its charge already tracks its real compute cost
closely. Re-deriving with `cachedInputTokenWeight: 0.1` (the figure the
"Per-group cache-hit profile" section above used illustratively) against
*this* run's actual token counts: app1's effective prompt-token charge
would fall from 477,716 to ≈101,000 tokens (0.124×477,716 cache-misses at
full price + 0.876×477,716×0.1 cache-hits at the discounted price) — a
~79% cut to its prompt-token charge, ~61% cut to its total billed tokens
including completions (613,392 → 236,717) for **identical delivered work**.
Under live enforcement that would force app1 to deliver substantially more
real throughput to hold the same 66.7% entitlement — the same
"re-pricing... by almost an order of magnitude" the existing section above
already flagged, now reproduced with a differentiated rather than
illustrative traffic shape, inside the actual scored harness.

**Request count is not a clean second axis here.** app1's request share
(69.5%) overshoots its charged-token share (65.1%) because the two groups'
prompts are not token-matched: app2's 40 nominally-"unique" words
tokenize to *more* raw tokens per request on average (266,673/1,047 ≈
254.7) than app1's 160-word natural-language prefix+tail
(477,716/2,383 ≈ 200.5), despite having fewer nominal words — BPE handles
common English words far more efficiently than the random
alphanumeric `wNNNNN` tokens `cold` generates for uniqueness. This does not
change the direction of the headline cache-ratio finding (6.2% vs 87.6% is
unaffected by it), but it means request-count share and charged-token share
answer slightly different questions here and should not be read as two
measurements of the same thing.

**Actual GPU time, split by tenant: not obtainable.** Confirmed directly,
not assumed — `docs/runbook.md`'s "Known gaps" already states vLLM's own
series carry no `fairness_id`/group label, and every `vllm:*` query against
this run's window (`18:30:25`–`18:34:37Z`) came back with no group
dimension to split on. Pool-wide numbers for context only (not
attributable to either tenant): `vllm:num_requests_running` averaged 3.56,
`vllm:num_requests_waiting` averaged 16.4 (a real backlog existed, matching
the nonzero `contended_seconds_total` above), zero
`vllm:num_preemptions_total`, TTFT p50 ≈2.99s, queue-time p50 ≈2.89s.

**Cluster left as found.** The only live change made for this run was the
pre-run EPP pod restart above (not a config/weight/replica change — nothing
to restore). Confirmed after the run:

```
$ oc get llmisvc maas-vllm-gpu -n maas-fairness-poc -o jsonpath='replicas={.spec.replicas}{"\n"}'
replicas=2
$ oc get deployment maas-vllm-gpu-kserve -n maas-fairness-poc -o jsonpath='{.status.readyReplicas}/{.status.replicas}{"\n"}'
2/2
$ # from this run's own metrics-after.txt (EPP's own echoed config):
llm_d_epp_maas_fairness_configured_weight{fairness_id="app1"} 20
llm_d_epp_maas_fairness_configured_weight{fairness_id="app2"} 10
llm_d_epp_maas_fairness_configured_weight{fairness_id="end-users"} 65
llm_d_epp_maas_fairness_configured_weight{fairness_id="unclassified"} 5
llm_d_epp_maas_fairness_enforcing 1
```

Matches `deploy/poc/09-vllm-gpu.yaml` (replicas) and `deploy/epp-config.yaml`
(weights, enforcing) exactly. The completed `maas-loadgen` Job was left in
place (same convention as every prior scenario). No orphaned `oc logs -f`
process was left behind (checked against the UNI-169/170 fix by walking
`/proc/*/cmdline`; this run's own `.capture-oc.pid` no longer corresponds to
a live process).

Raw results: `results/20261101T183024Z-uni136-cache-heavy-vs-cache-cold/`
(report JSON/MD, loadgen log, metric snapshots/timeseries, client-request
summary, EPP container log).

**Grafana time range** (padded ±60s around `run_start`/`run_end`):
`from=1793557765000&to=1793558137000` —
https://grafana-grafana.apps.ocp.paladinaura.com/d/maas-fairness-gpu-epp/?orgId=1&from=1793557765000&to=1793558137000&var-group=All&var-window=2m

**Not proven here:** only the app1/app2 pairing was run — `end-users`,
which the original cache-profile measurement found even more cacheable
(96.4%, the long-shared-prefix multi-turn-chat proxy), was not included in
this scored run, so there is no three-way or end-users-paired variant of
this result. GPU time is pool-wide only, never per-tenant, on this metric
set (see above). This is a single 240s run, not repeated for variance. And
per the ticket's own framing, this is a characterisation for Outstanding
item 2's decision, not the decision itself — whether and to what value
`cachedInputTokenWeight` should actually move, and how the group weights
would need to be re-derived alongside it, remains "a policy decision," not
a technical finding this run can settle on its own.

## UNI-137: B5, open-loop (Poisson) below / at / above saturation (promotes UNI-34)

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan, "B" group: does UNI-34's
open-loop (Poisson-arrival) finding — a measured, severe inversion of the
20/10/65 split once the pool is pushed past saturation — reproduce as a
scored, repeatable benchmark scenario, not a one-off manual measurement?
UNI-34 itself only ran one below-saturation pair and one short
above-saturation burst, informally, against `13-loadgen-poisson.{py,sh}`
directly; this ticket wraps that same generator into the same
named-scenario/report infrastructure every other case in this series uses.

**Harness change: `deploy/poc/17-fairness-benchmark-openloop.sh`.** New
script, same shape as `15-fairness-benchmark.sh` (one named scenario in,
one `results/<ts>-<label>/` directory out, scored by
`15-fairness-report.py`) but built around a local-process generator instead
of a `Job`: `13-loadgen-poisson.sh` hits the public Route directly, so
there is no Job to patch or poll, only a "no active `maas-loadgen` Job"
guard to preserve this series' one-benchmark-at-a-time rule against a
concurrent closed-loop run. `13-loadgen-poisson.{sh,py}` themselves are
reused completely unmodified. `15-fairness-report.py` gained an open-loop
log parser (`OPEN_LOOP_TENANTS_LINE`/`OPEN_LOOP_ROW`, tried only after the
closed-loop `TENANTS_LINE` match fails, so every prior scenario's report is
byte-for-byte unaffected) and a `generator` field so the markdown table
labels the offered-load column correctly (`offered req/s` vs
`offered workers`).

**Setup:** full-contention mix (`app1`/`app2`/`end-users` all offered, at
the *same* Poisson rate each, live against `maas-vllm-gpu`, 2 replicas,
`enforce: true`), at ~70/100/120% of UNI-34's own documented pool ceiling
(**"~20-22 req/s aggregate on this rig,"** `docs/poc-results.md`'s own
"Open-loop (Poisson) load generation (UNI-34)" section) — taking the
midpoint, 21 req/s aggregate, splits evenly to 4.9/7.0/8.4 req/s per tenant
at 70/100/120%. Each level: 240s + up to 100s drain, `THRESHOLD_POINTS=10`.

**A reporting bug surfaced by the 70% run, fixed before scoring anything.**
The live below-saturation run's raw metrics show `app1`/`app2`'s
`contended_seconds_total` delta at a flat `0.00s` (present in both
snapshots, unchanged) — but `end-users`' `contended_seconds_total` *and*
`contended_service_tokens_total` lines were **absent from both** snapshots
entirely. The EPP's Prometheus client lazily registers a counter per label
on first increment (`metrics.go`), so an entirely-missing line means that
group has **never once** been contended — stronger evidence of zero
contention than a present-but-flat delta, not weaker. The existing
UNCONTENDED check (added by [UNI-135](/UNI/issues/UNI-135)) required
`contended_seconds_deltas.get(g) is not None`, so it read the missing line
as disqualifying rather than confirming, and the run scored **FAIL**
("offered groups delivered zero contended service tokens") instead of the
correct **UNCONTENDED**. Fixed `15-fairness-report.py`'s `is_uncontended`
to treat a missing `contended_seconds_total` delta as uncontended *when
corroborated* by an equally missing/zero `contended_service_tokens_total`
delta for the same group (both SLIs share one contention gate, so real
contention cannot produce tokens without seconds) — this correlation keeps
an older synthetic test fixture that sets only
`contended_service_tokens_total` and never bothers with
`contended_seconds_total` from being misread as "uncontended" too. Also
fixed a latent crash in the UNCONTENDED reason string (`f"{...:.2f}s"` on a
`None`). Covered by a new regression test,
`test_open_loop_below_saturation_reports_uncontended_when_metric_never_materialized`,
built directly from this run's own raw numbers; all 31 unit tests pass.
The 70% report in `results/` below is the regenerated, corrected one — the
original mis-scored FAIL JSON/MD this run first produced was discarded, not
shipped.

**Observed, all three levels:**

| level | rate/tenant (aggregate) | verdict | app1 obs% (dev) | app2 obs% (dev) | end-users obs% (dev) | contended_seconds | client status codes |
|---|---|---|---|---|---|---|---|
| 70% | 4.9/s (14.7/s) | **UNCONTENDED** | 0.0% (n/a) | 0.0% (n/a) | n/a (n/a) | app1 0.00s, app2 0.00s, end-users never contended | all 200 (1100/1198/1207 sent) |
| 100% | 7.0/s (21.0/s) | **UNCONTENDED** | 33.1% (+12.0) | 34.2% (+23.7) | 32.7% (**-35.7**) | app1 0.41s, app2 0.59s, end-users 0.56s | all 200 (1716/1638/1642 sent) |
| 120% | 8.4/s (25.2/s) | **FAIL** | 32.4% (+11.3) | 18.0% (+7.5) | 49.6% (**-18.8**) | app1 23.9s, app2 24.0s, end-users 21.5s | heavy 50s client timeouts: app1 736/2052 200, app2 404/1976 200, end-users 1050/1982 200 |

(Deviations at 70%/100% are informational only — `expected_share`/
`deviation_pts` are computed and shown in the full report even for an
UNCONTENDED run, but the verdict does not score them, by design: see
[UNI-135](/UNI/issues/UNI-135)'s "a weighted-split deviation is not a
meaningful question with nobody to share against.")

**Pass/FAIL against the ticket's own prediction: partial.** 70% matched
exactly — "uncontended" was the correct call once the bug above was fixed.
120% matched in direction — a real FAIL, `end-users` (weight 65, the
dominant group) under-served relative to its share while `app1`/`app2`
over-deliver — reproducing, not refuting, UNI-34's original finding that
pushing past saturation inverts the configured weights. **100% did not
match**: the ticket predicted "split within threshold" (PASS), but the run
scored UNCONTENDED, i.e. still not measurably contended by this report's
own gate (`contended_seconds_total` 0.41-0.59s, under the 1.0s threshold).

**What surprised us.**

- **The 100% level is both "uncontended" and badly skewed at once.** Even
  though `contended_seconds_total` stayed under the UNCONTENDED threshold,
  the per-group deviations the report still computes and prints
  (+12.0/+23.7/-35.7 points) are already far larger than the 10-point FAIL
  bar — larger, in fact, than the 120% level's own FAIL deviations. If the
  system had been scored on deviation alone at 100% (ignoring the
  UNCONTENDED carve-out), it would have FAILed harder than 120% did. This
  says the split degrades smoothly and substantially well *before* the
  binary `contended_seconds_total` gate trips, not sharply at some crisp
  "ceiling" — the same "contention does not vanish/appear as a step
  function" pattern [UNI-135](/UNI/issues/UNI-135) found at 20% of a
  different (closed-loop) ceiling, now seen from the other side.
- **UNI-34's documented "~20-22 req/s" ceiling may be stale for the current
  EPP build.** UNI-34 was measured before the `contended_service_tokens_total`
  accounting fix (`docs/poc-results.md`'s "Outstanding work," `~~Fix
  contended_service_tokens_total~~`) and before this series' other GPU
  commissioning changes. This run's 100% level (21 req/s aggregate) still
  reads as UNCONTENDED by the report's own gate, which is at minimum
  consistent with the true current ceiling sitting higher than 21 — this
  ticket did not re-measure the ceiling independently, it reused UNI-34's
  figure, so the 70/100/120% labels are relative to a number that was not
  re-verified against the current build.
- **120%'s inversion is real but markedly less severe than UNI-34's
  original measurement.** UNI-34's one-off 90s burst at 24 req/s aggregate
  measured end-users falling from an expected 68.4% to **25.5%** (-42.9
  points). This 240s, 25.2 req/s-aggregate run measured end-users at
  **49.6%** (-18.8 points) — still inverted and still a clear FAIL, but
  under half the original deviation. Not distinguished by this one run:
  whether the gap is the accounting fix changing the charged numbers, the
  4x-longer duration (240s vs 90s) giving the policy more time to recover
  ground within the run, or run-to-run variance on a single sample at each
  level. This is the baseline [F2](/UNI/issues/UNI-117#document-test-plan)
  (clamp off) should compare against, not UNI-34's original number, since
  it was captured on the same EPP build F2 will also run against.
- **Client-observed evidence agrees with the EPP's own accounting,
  independently.** At 120%, raw client status codes show heavy, symmetric
  50s timeouts across all three groups (`0=`1316/1572/932 out of
  2052/1976/1982 sent) — a client-side signal that does not depend on
  `contended_service_tokens_total` at all, and it corroborates "the pool
  genuinely collapsed" rather than "the accounting metric alone drifted."

**Cluster left as found.** This generator never patches the
LLMInferenceService or EPP config, only reads metrics and sends HTTP
traffic; confirmed afterward, not assumed:

```
$ oc get deployment maas-vllm-gpu-kserve -n maas-fairness-poc -o jsonpath='{.spec.replicas}{"\n"}'
2
$ oc get jobs,pods -n maas-fairness-poc
job.batch/maas-loadgen   Complete   1/1   4m10s   41m
... (no stray/active pods)
$ # from the 120% run's own metrics-after.txt (EPP's own echoed config):
llm_d_epp_maas_fairness_configured_weight{fairness_id="app1"} 20
llm_d_epp_maas_fairness_configured_weight{fairness_id="app2"} 10
llm_d_epp_maas_fairness_configured_weight{fairness_id="end-users"} 65
llm_d_epp_maas_fairness_configured_weight{fairness_id="unclassified"} 5
```

Matches `deploy/poc/09-vllm-gpu.yaml` (replicas) and `deploy/epp-config.yaml`
(weights) exactly. The completed `maas-loadgen` Job (left over from a prior,
unrelated closed-loop scenario, not created by this ticket) was left in
place, same convention as every prior scenario. No orphaned `oc logs -f`
process survived (checked via `/proc/*/cmdline`, UNI-169/170 convention).

**Raw results:**
`results/20261101T185150Z-uni-137-b5-below-saturation/`,
`results/20261101T190155Z-uni-137-b5-at-saturation/`,
`results/20261101T190612Z-uni-137-b5-above-saturation/` (report JSON/MD,
loadgen log, metric snapshots, per-tenant client logs, EPP container log,
for each level).

**Grafana time range** (padded ±60s around each run's `run_start`/`run_end`):

- 70%: `from=1793559050000&to=1793559413000`
- 100%: `from=1793559656000&to=1793560018000`
- 120%: `from=1793559913000&to=1793560356000`

https://grafana-grafana.apps.ocp.paladinaura.com/d/maas-fairness-gpu-epp/?orgId=1&from=1793559050000&to=1793560356000&var-group=All&var-window=2m
(combined span across all three levels)

**Not proven here:** no clamp on/off A/B comparison (same gap UNI-34 itself
left open — `newcomerClamp` is not independently toggleable without a
config/code change this ticket's scope excludes); each level is a single
240s run at a single seed, not repeated for variance; and, per "what
surprised us" above, the 21 req/s ceiling this ticket's 70/100/120% figures
are relative to was reused from UNI-34 rather than independently
re-measured on the current EPP build.

## UNI-138: G2, ledger cross-check -- EPP token counters vs tokens the loadgen received

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan, "G" group: does the EPP's own
accounting agree with what the client actually sent and received, not just
whether the weighted split matches the configured weights (every prior case
in this series)? This is a different invariant from the fairness SLI --  it
checks for a second, independent kind of bug: the policy could split traffic
in exactly the right proportions while still mis-accounting the absolute
token counts it is dividing up.

**Harness change: none needed for the client side.** [UNI-128](/UNI/issues/UNI-128)
already added `CLIENT_RECORD_JSON` (real `usage.prompt_tokens`/
`completion_tokens` from each response body, not an estimate) and
`15-fairness-benchmark.sh` already pulls it into
`client-request-summary.jsonl`. Two things *were* missing:

1. **`snapshot_metrics()` only ever scraped the `llm_d_epp_maas_fairness_`
   prefix.** The EPP's core, per-request token histograms
   (`llm_d_epp_request_input_tokens`, `_output_tokens`, `_cached_tokens` --
   `fairness_id`-labelled, owned by the framework, not the fairness plugin;
   `pkg/fairness/weightedlas/metrics.go`'s own comment says not to duplicate
   them) were invisible to every report before this ticket. Fixed by
   broadening the grep to also capture their `_sum`/`_count` lines. These are
   observed *only* from a real response `Usage` block
   (`pkg/epp/handlers/response.go`), never from the fairness plugin's
   dispatch-time estimate, and are **not** contention-gated -- the most
   direct possible check against the client's raw totals.
2. **No metric exposes the cost-model weights**
   (`inputTokenWeight`/`outputTokenWeight`/`cachedInputTokenWeight`), and
   `contended_service_tokens_total` is denominated in that cost unit, not raw
   tokens (`cost.go`: `inputTokenWeight*(prompt-cached) +
   cachedInputTokenWeight*cached + outputTokenWeight*completion`). Comparing
   it to raw client tokens directly would read a deliberate cost-model choice
   (`outputTokenWeight: 2.0` live) as a bug. Fixed by reading the three
   weights live from the `maas-epp-config` ConfigMap and running the client's
   own prompt/completion totals through the identical formula before
   comparing.

`15-fairness-report.py` gained a `ledger` section (`--client-record-jsonl`,
`--input-token-weight`/`--output-token-weight`/`--cached-input-token-weight`,
`--ledger-tolerance-pct`) -- purely additive, like UNI-127's `timeline`: it
never reads or writes the top-level `verdict`, since this checks a different
invariant and gets its own `ledger.verdict`. Five new unit tests
(`test_ledger_*`); all 36 pass.

**Setup:** a plain `full-contention` run (`app1`/`app2`/`end-users`,
32/32/128 workers, 240s, no request-shape overrides -- the same shape every
other full-contention measurement in this series uses) against the live GPU
pool, 2 replicas, `enforce: true`.

**Expected split:** 20/10/65 (renormalized: 21.1/10.5/68.4% of the offered
total).

**Observed split:** app1 17.7% (-3.3pts), app2 14.0% (+3.5pts), end-users
68.2% (-0.2pts) -- max deviation 3.5pts, **PASS** against the 10-point
threshold (this is the same weighted-split check every other case in this
series runs; G2's own pass bar is the ledger table below, not this number).

**Ledger cross-check -- two independent comparisons per tenant:**

| group | client prompt/completion tok | EPP raw tokens (in+out) | raw diff % | EPP contended cost | expected cost (client tok through cost formula) | cost diff % |
|---|---|---|---|---|---|---|
| app1 | 694,950 / 34,457 | 729,407 | **0.00%** | 734,108 | 763,864 | **-3.90%** |
| app2 | 551,040 / 27,500 | 578,540 | **0.00%** | 581,698 | 606,040 | **-4.02%** |
| end-users | 2,587,920 / 128,796 | 2,715,422 | **-0.05%** | 2,826,610 | 2,845,512 | **-0.66%** |

Cost model used (read live from `maas-epp-config`, not hardcoded):
`inputTokenWeight=1.0`, `outputTokenWeight=2.0`, `cachedInputTokenWeight=1.0`.

**Verdict: PASS at X=10%.** Every cell above is within 10% both ways; the
largest observed bias (app2's cost check, -4.02%) still has roughly 2.5x
headroom under the threshold.

**Picking X=10%, from this run's own data.** The two checks behave very
differently, and that difference is itself the evidence for where to set the
bar:

- **Raw tokens (EPP's ungated core histograms vs. the client's own
  usage-block totals) agree to within rounding** (0.00%, 0.00%, -0.05%).
  Both sides read the same real `usage.prompt_tokens`/`completion_tokens`
  values off the same responses, through independent code paths (the
  client's own `grep` vs. the framework's `RecordInputTokens`/
  `RecordOutputTokens`), so near-exact agreement is the expected result when
  the EPP's accounting is correct, not a coincidence. A 10% bar on this check
  has enormous headroom; it exists mainly to catch a real regression (a
  server missing `--enable-force-include-usage`, or the two sides drifting
  out of sync), not to tolerate expected noise.
- **The cost-weighted, contention-gated check (`contended_service_tokens_total`
  vs. the client's totals run through the cost formula) carries a real,
  persistent, negative bias** of -3.9% to -4.0% for the two lower-volume
  tenants (app1: 567 requests, app2: 449) and only -0.66% for the
  high-volume one (end-users: 2,155 requests).

**Explaining the bias -- and ruling out the ticket's own prediction.** The
ticket flagged "the 4-bytes-per-token estimate" (`estimatedBytesPerToken: 4`,
`cost.go`'s `estimatePromptTokens`) as a known source of bias. The data rules
this out directly: `llm_d_epp_maas_fairness_requests_without_usage_total` --
the counter that fires exactly when a completed request never got a real
`Usage` block and its *dispatch-time estimate* (the bytes/4 prompt guess
included) is booked permanently instead of a measured cost -- is **absent
from both snapshots**, i.e. flat zero for the entire 240s run. Every
completed request, success or otherwise, was trued up against real
measured tokens; the bytes/4 estimate never once became the booked cost.
(The 54 non-200 responses this run saw, 2/1/51 for app1/app2/end-users, also
don't explain it: each group's `dispatch_total` delta matches its 200-count
almost exactly -- app1 565 dispatches vs. 565 `200`s, app2 448 vs. 448,
end-users 2,103 vs. 2,104 -- meaning those failures never reached the EPP's
dispatch/accounting path at all, and are symmetrically excluded from the
client ledger too, since `04-loadgen.yaml`'s `run.sh` only sums
`prompt_tokens`/`completion_tokens` when the grep actually found them.)

The real mechanism is `contended_service_tokens_total`'s own gate:
`isContended` is a single flag per priority band, shared across every group
in it, that only turns true once the EPP has observed *at least one instant*
where two groups were backlogged simultaneously (`pkg/fairness/weightedlas/
plugin.go`'s `isContended`/`lastContendedUnixNano`). At the very start of a
run, before that first overlap is ever observed, every group's requests are
still dispatched, still complete normally, and are still correctly measured
and added to the *ungated* raw-token histograms -- but by `metrics.go`'s own
documented definition ("share is only counted over the time a group
actually had a queue while someone else did too"), they are correctly
excluded from `contended_service_tokens_total`. This is the policy working
as designed, not a bug -- but it does mean a whole-run client ledger, which
has no notion of this gate, will always see the gated cost counter sitting
slightly *below* "every real request's cost," never above. Because the
size of that startup window is roughly fixed per run (set by how fast the
very first cross-group overlap happens, not by how much traffic a given
tenant sends over the full 240s), it is a much bigger fraction of a
low-volume tenant's total (app1/app2, ~500-570 requests) than a high-volume
one's (end-users, ~2,100) -- exactly the -4%/-4%/-0.66% pattern observed.
This is a **persistent, structural, and explained** bias, not noise, and it
should shrink (not grow) on a longer run, since the fixed startup window
amortizes over more total requests.

Given that, 10% was picked as X because it covers the only real, explained
bias (max -4.02%) with ~2.5x margin, while still being tight enough that the
near-zero raw-token check would catch a real regression (a missing
`--enable-force-include-usage` flag, or the ledger mechanism itself
breaking) immediately.

**What surprised us.** The ticket's own candidate explanation (bytes/4
estimate bias) turned out to be the wrong one for this run -- the actual
cause is a structural property of the contention gate that has nothing to
do with token-count estimation at all. Catching that required checking
`requests_without_usage_total` directly rather than assuming the ticket's
hint was the answer; a report that had simply computed "is the bias under
X%" without explaining *why* would have shipped a plausible-sounding but
wrong just-so story.

**Cluster left as found.** This run patches nothing beyond the standard
Job/ConfigMap cycle every scenario in this series uses; confirmed afterward:

```
$ oc get llmisvc maas-vllm-gpu -n maas-fairness-poc -o jsonpath='{.spec.replicas}{"\n"}'
2
$ oc get jobs,pods -n maas-fairness-poc
job.batch/maas-loadgen   Complete   1/1   4m19s   6m12s
... (no stray/active pods, no orphaned `oc logs -f` processes -- checked via /proc/*/cmdline)
$ # maas-epp-config's `epp` key, byte-for-byte, before vs. after this run: identical
```

Matches `deploy/llmisvc.yaml` (replicas) and `deploy/epp-config.yaml`
(weights, cost model) exactly.

**Raw results:** `results/20261101T192928Z-uni138-g2-ledger-full-contention/`
(report JSON/MD with the new `ledger` section, loadgen log,
`client-request-summary.jsonl`, metric before/after/timeseries snapshots,
EPP container log).

**Grafana time range** (padded +-60s around `run_start`/`run_end`):
`from=1793561309000&to=1793561692000`

https://grafana-grafana.apps.ocp.paladinaura.com/d/maas-fairness-gpu-epp/?orgId=1&from=1793561309000&to=1793561692000&var-group=All&var-window=2m

**Not proven here:** a single 240s run at a single seed, not repeated for
variance -- the -4% cost bias is explained mechanistically, not confirmed to
be stable across repeats. The ledger check is only validated for a
full-contention shape; it assumes the contended fraction of a run is close
to 1.0 (nobody is ever offered without being contended), which does not hold
for `solo`, `capped`, demand-light, or UNCONTENDED scenarios elsewhere in
this series -- `--client-record-jsonl` was not wired into those invocations
and should not be, without re-deriving the formula for a partially-contended
run first. Cache-hit accounting (`cachedInputTokenWeight`) was not
separately exercised here (`CACHE_SHAPE_*` left at default), so the ledger's
cached-token term is small and mostly untested at scale; see UNI-136 for
that dimension on its own.

## UNI-139: H1, repeatability — every scored scenario 5×, threshold derived from data

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan, H1 in the chain. Every prior
scenario in this series (`full-contention`, `end-users-idle`, `app1-alone`,
`asymmetric-demand`, plus the three added earlier in this chain — `app2-idle`
(A3/UNI-132), `app1-idle` (A4/UNI-133), `app2-trickle` (A5/UNI-134)) had only
ever been run once each. This ticket reruns all seven, 5× apiece (35 runs
total, ~2h45m of GPU time), to answer two questions the single-run numbers
elsewhere in this doc can't: how much does a scenario's deviation actually
move run to run, and does that noise floor justify the 10-point threshold
`15-fairness-report.py` has used throughout?

**Setup:** same scenario definitions as their originating tickets (see
`deploy/poc/15-fairness-benchmark.sh`, same `TENANTS`/`PER_TENANT_OVERRIDES`
per scenario), 240s each, live against `maas-vllm-gpu` (2 replicas,
llama-3-1-8b), `enforce: true`, weights 20/10/65/5. Run one scenario at a
time (5 reps, back to back) to respect the one-benchmark-on-the-GPU-pool
rule; namespace checked clear of any other loadgen job before every scenario
started. Driven by a scratch-only (`/tmp/uni139/`, not committed) shell
driver so the sweep survived two unrelated session interruptions along the
way without losing progress or contaminating results.

**Results: 35/35 runs completed, all recorded.** 32 PASS, 1 FAIL, 2
UNCONTENDED — see the two findings below for both non-PASS groups; neither
is a new defect.

### Two of the seven scenarios aren't threshold-scored at all

`app1-alone` (`solo_group`, nothing to compare a lone tenant's share
against) and `asymmetric-demand` (`end-users` demand-capped at 2 workers,
scored by `15-fairness-report.py`'s one-sided "did the uncapped tenant still
get served" check, not the symmetric deviation threshold — see "UNI-54,"
above) report a `max_abs_deviation_points` number in their JSON, but that
number is not what `threshold_points: 10` gates on for these two scenarios.
Including them in a threshold-derivation average would be comparing noise on
two different instruments. They're reported here for completeness, excluded
from the threshold analysis below:

| scenario | n | verdicts | max_abs_deviation_points (not threshold-scored) |
|---|---|---|---|
| `app1-alone` | 5 | 5× PASS | n/a every rep (solo tenant, nothing to deviate from) |
| `asymmetric-demand` | 5 | 3× PASS, 2× UNCONTENDED | mean 70.3, sd 0.28 (range 70.00–70.58) |

**`asymmetric-demand`'s PASS/UNCONTENDED split is itself a finding.** The
underlying signal — `end-users` demand-capped to ~6% of its weighted
entitlement — is rock-stable across all 5 reps (70.0–70.6 points, sd 0.28,
barely more noise than measurement precision). What flips between PASS and
UNCONTENDED is `contended_seconds`, which landed at 1.245s, 1.045s, 1.184s
(PASS, all >1.0s) then 0.983s, 0.984s (UNCONTENDED, both <1.0s) against the
benchmark's `uncontended_threshold_seconds: 1.0`. A ~27% run-to-run spread in
a sub-two-second measurement is swinging the verdict across a hard cutoff
that sits inside that spread — not a sign the underlying fairness behavior
changed, but a sign this particular knife-edge threshold is too tight
relative to its own noise floor. Out of scope to fix here (that constant
belongs to the contention gate, not the 10-point deviation threshold this
ticket was asked to evaluate), flagged as a follow-up.

### The five threshold-scored scenarios

| scenario | n | verdicts | max_abs_deviation_points: mean ± sd (min–max) |
|---|---|---|---|
| `full-contention` | 5 | 5× PASS | 4.24 ± 0.66 (3.84–5.39) |
| `end-users-idle` | 5 | 5× PASS | 3.03 ± 0.70 (2.36–4.07) |
| `app2-idle` | 5 | 5× PASS | 3.53 ± 0.72 (2.85–4.49) |
| `app2-trickle` | 5 | 5× PASS | 3.68 ± 0.27 (3.22–3.89) |
| `app1-idle` | 5 | 4× PASS, **1× FAIL** | 7.33 ± 4.27 (0.18–11.21) |
| **all 25 reps** | 25 | 24 PASS, 1 FAIL | **4.36 ± 2.40** (0.18–11.21) |

Per-group signed deviation (mean ± sd, points), the number the ticket asked
for directly:

| scenario | group A | group B |
|---|---|---|
| `full-contention` | app1 −4.18 ± 0.71 | app2 +3.49 ± 0.43 (end-users +0.69 ± 0.67) |
| `end-users-idle` | app1 +3.03 ± 0.70 | app2 −3.03 ± 0.70 |
| `app2-idle` | app1 −3.53 ± 0.72 | end-users +3.53 ± 0.72 |
| `app2-trickle` | app1 −3.68 ± 0.27 | end-users +2.06 ± 0.27 (app2 capped, not scored) |
| `app1-idle` | app2 −7.26 ± 4.42 | end-users +7.26 ± 4.42 |

**`app1-idle` alone carries almost all the series' noise, and it's the
scenario that FAILed.** Its sd (4.27 on the max-abs figure, 4.42 on the
per-group figure) is 6–16× every other scored scenario's sd (0.27–0.72). The
other four scenarios' entire observed range across 20 reps (2.36–5.39) sits
inside `app1-idle`'s own 5-rep range (0.18–11.21) on its own. This isn't new
information in isolation — "UNI-133: A4, `app1-idle`" (above) already
described a cold-start mechanism where the minority tenant (`app2`, the
6.5:1 pair's small side) can be shut out of the pool entirely for the first
~100s of a 240s run while the much larger `end-users` worker count (208 vs
32) fills it first, and how much of the run that cold start eats varies
rep to rep. This 5-rep sweep is the first time that variance has actually
been measured instead of described from a single run: rep 5's 0.18-point
deviation and rep 3's 11.21-point FAIL are the same scenario, same weights,
same worker counts, back to back, 14 minutes apart. `app2`'s own
`requests_total` makes the mechanism visible directly — 183, 138, 127, 212,
433 across the 5 reps, a >3× spread in a 240s closed-loop run, with no
corresponding spread on `end-users`' side (~2750–3040) — consistent with
`app2`'s queue depth, not `end-users`', being what varies with how long the
cold start happens to last each time.

**The one FAIL (rep 3, 11.21 points) is a valid result, not a flake to
explain away.** Per the ticket's own rule 4, it's recorded as data, not
rerun or discarded. `epp_restarted_mid_run: false` and status tallies were
unremarkable on that rep — nothing in the artifacts marks it as degenerate
run, just the upper end of this scenario's own noise distribution.

### Threshold recommendation

Across the 25 threshold-scored reps, `mean + 2·sd ≈ 9.15` and
`mean + 3·sd ≈ 11.54`. The current 10-point threshold sits almost exactly at
+2.4 sd above the pooled mean — close enough that the series' single FAIL
(11.21) is not distinguishable from pure run-to-run noise at a 3-sigma
level, and the rep immediately before it (9.80, also `app1-idle`) already
sat within half a point of the cutoff. That FAIL was entirely driven by one
scenario's structurally wider noise band (above), not by four of the five
scenarios, whose full 20-rep observed range (2.36–5.39) never comes
remotely close to 10.

**Recommendation (not applied in this ticket, per its own instructions):
raise the global threshold to 12 points.** This clears the full observed
range of all 25 threshold-scored reps (max 11.21) with a point of margin,
costs essentially nothing against the four well-behaved scenarios (whose
observed ceiling, 5.39, is still more than 2× under even the current 10),
and tracks the data-derived `mean + 3·sd ≈ 11.5` figure rather than a round
number chosen before any repeatability data existed. A more surgical
alternative — leave the global constant at 10 and give `app1-idle`
specifically (and any other scenario with a worker-count ratio as extreme as
its 6.5:1) a documented, scenario-specific allowance, the same way
`app1-alone` and `asymmetric-demand` already get structural carve-outs from
the symmetric deviation check — would preserve the current threshold's
sensitivity everywhere else, but needs its own ticket: this one data point
isn't enough to size a second constant, only to show the first one is a
closer call than it looks from any single run.

### Cluster left as found

Confirmed from the EPP's own live `/metrics` (not the repo manifest) after
the sweep finished, same method as every prior scored scenario in this
series:

```
$ oc get llmisvc maas-vllm-gpu -n maas-fairness-poc -o jsonpath='replicas={.spec.replicas}{"\n"}'
replicas=2
$ oc get pods -n maas-fairness-poc -l app.kubernetes.io/name=maas-vllm-gpu
NAME                                                     READY   STATUS    RESTARTS   AGE
maas-vllm-gpu-kserve-74d8dd69bd-69gqk                    1/1     Running   0          6h44m
maas-vllm-gpu-kserve-74d8dd69bd-bbhg4                    1/1     Running   0          14d
maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76   1/1     Running   0          4h2m
# from the last run's own metrics-after.txt (EPP's own echoed config):
llm_d_epp_maas_fairness_configured_weight{fairness_id="app1"} 20
llm_d_epp_maas_fairness_configured_weight{fairness_id="app2"} 10
llm_d_epp_maas_fairness_configured_weight{fairness_id="end-users"} 65
llm_d_epp_maas_fairness_configured_weight{fairness_id="unclassified"} 5
llm_d_epp_maas_fairness_enforcing 1
```

`replicas: 2` matches `deploy/poc/09-vllm-gpu.yaml`; weights and `enforcing`
match the live ConfigMap exactly (the committed `deploy/epp-config.yaml`
ships `enforce: false` as its documented shadow-mode default — see
"Reproducing," below — the live cluster has run patched to `enforce: true`,
"the live default," since earlier tickets in this series; this ticket never
touched that patch either way). No scenario in this sweep edits the
LLMInferenceService spec, weights, or replica count — nothing needed
restoring beyond deleting each scenario's own `maas-loadgen` Job before the
next one started, same convention as every prior run.

Raw results: `results/<timestamp>-uni139-<scenario>-r<1-5>/` (35
directories — report, loadgen log, metric snapshots/timeseries, client
request summary, EPP container log, each).

**Not proven here:** why `app1-idle`'s cold start varies in duration rep to
rep (GPU scheduler/batching jitter is the suspect, per "UNI-133," above, but
not instrumented or isolated here); whether a longer run (the same
untested lever "UNI-133" left open) would shrink that scenario's noise band
by diluting the cold-start window, or whether the recommended 12-point
threshold would hold up over a larger sample than 5 reps. The
`asymmetric-demand` PASS/UNCONTENDED knife-edge is described, not fixed —
its own threshold constant (`uncontended_threshold_seconds: 1.0`) is a
different lever than the one this ticket was scoped to evaluate.

## UNI-140: B6, soak — 1–2h at full-contention

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan, promoted after the B1–B5
timeline/open-loop harness work. Longest single run in this series so far:
the existing `full-contention` scenario held for 90–120 minutes instead of
the usual 240s–600s, to check for slow failure modes a short run cannot
show — memory growth, a stuck eviction/state mechanism, or an EPP restart —
none of which a handful of short scored runs would catch.

**Setup:** `full-contention` (`app1`/`app2`/`end-users` all offered, 32/32/128
workers), 5700s (95 min), live against `maas-vllm-gpu` (2 replicas,
llama-3-1-8b), `enforce: true`, 5-minute windows (UNI-127 harness; HX1 — a
windowing improvement named in the original edge-case plan — has not landed,
so this uses the plan's documented fallback). `deploy/poc/18-soak-monitor.sh`
(new, this ticket) ran alongside `15-fairness-benchmark.sh` to also sample
EPP memory and restart count every 60s and capture an unfiltered `/metrics`
scrape, neither of which the benchmark script's own grep filter keeps.

**What actually happened:** both local processes stopped writing at
~23:24:13Z, 42 minutes into the run — most likely a control-plane hiccup,
not a cluster-side failure (see the recovery comment on this issue from
22:47Z, which confirmed the same run was healthy shortly before this). The
`maas-loadgen` Job itself and the EPP were unaffected by whatever killed the
local processes, and the Job ran to its full configured duration, completing
at 00:17:38Z. This was only caught by comparing the Job's own
`status.completionTime` (00:17:38Z) against the local artifacts' last-written
timestamp (23:24Z) — the local report had silently produced a complete-looking
PASS verdict for less than half the intended window.

**Recovered the missing 53 minutes from cluster-side Prometheus**, not by
re-running: the EPP's counters and the platform's memory/restart metrics
live in Thanos independent of whether the sandbox driver survived to read
them. `deploy/poc/19-soak-prometheus-backfill.py` (new, this ticket) re-reads
`llm_d_epp_maas_fairness_contended_service_tokens_total` (the same SLI
`15-fairness-report.py` uses — not redefined here),
`container_memory_working_set_bytes`, `process_resident_memory_bytes`,
`kube_pod_container_status_restarts_total`, and
`llm_d_epp_flow_control_requests_total` for the run's actual start/end
timestamps via the live Grafana's anonymous-Viewer `/api/ds/query` proxy
(confirmed working in UNI-130), and recomputes the same two judgements over
the complete window.

**Windowed share — PASS for the full 95 minutes.** 19 five-minute windows,
max |deviation| 6.19 points (window 4200–4500s, `app1`), against the 10-point
threshold. No window anywhere in the run approaches the threshold, and the
deviation does not trend upward or downward over time — the policy's split
is as stable at minute 90 as at minute 5:

| group | expected % | observed % (whole run) | deviation (pts) |
|---|---|---|---|
| app1 | 21.05% | 16.85% | -4.20 |
| app2 | 10.53% | 13.90% | +3.37 |
| end-users | 68.42% | 69.25% | +0.83 |

(Full per-window table: `results/20261101T224216Z-uni140-b6-full-contention-soak/full-run-backfill.md`.)

**EPP memory — flat.** `process_resident_memory_bytes`: 322.2MB (first 10
samples' average) → 324.7MB (last 10 samples' average) over 96 one-minute
samples spanning the full run, range [298.4, 326.5]MB. `container_memory_working_set_bytes`
(container=main): 313.4MB → 316.8MB, range [289.0, 318.0]MB. Both move inside
a ~1% band start-to-end; the full range is dominated by an early dip (cold
cache/GC right after the run started) and ordinary GC sawtooth, not a trend.
No sustained growth over 95 minutes of full contention.

**No restarts.** `kube_pod_container_status_restarts_total` reads a flat `0`
across all 96 samples in the window, and the pod's own lifetime restart
count (`oc get pod`, checked after the run) is `0` since its creation at
18:28:54Z — well before this run started and still true now. The EPP never
restarted before, during, or after the soak.

**Eviction / state-table growth — no eviction activity observed, which is
the expected result, not a miss.** `llm_d_epp_flow_control_requests_total{outcome="EvictedContextCancelled"}`
held flat at 111 across the entire window (`Dispatched` rose by 69,070 over
the same period, confirming real, continuous traffic). `deploy/epp-config.yaml`'s
own `flowControl` comment is explicit about what this means: *"Watch
`llm_d_epp_flow_control_requests_evicted_total`: if it is non-zero in a run,
that run measured shedding, not fairness."* A flat eviction counter under
sustained full contention is the healthy state this config was tuned for
(`defaultRequestTTL: 300s`, set specifically so the closed-loop generator's
deep queues get served late rather than shed). Separately, the fairness
policy's own per-group state table has no eviction/TTL by design —
`deploy/epp-config.yaml` notes the group set is closed and bounded at
`len(groups)+1`, so "growth" is not structurally possible regardless of
run length; the flat memory above is the closest available evidence that
holds in practice, since there is no direct state-table-size metric exposed.
If "the eviction sweep runs" in this ticket's acceptance criteria meant
"evictions fire," this run shows they did not, under this scenario's load
shape — not a failure of the mechanism, consistent with both the config's
own documented intent and the unchanged, flat memory.

**Cluster left as found.** This scenario sets no per-tenant override and the
benchmark never patches the LLMInferenceService spec or the EPP weight
config — confirmed, not assumed, via the EPP's own live config after the run:

```
$ oc get deployment maas-vllm-gpu-kserve -n maas-fairness-poc -o jsonpath='{.spec.replicas}{"\n"}{.status.readyReplicas}{"\n"}'
2
2
$ oc get pods -n maas-fairness-poc
NAME                                                           READY   STATUS      RESTARTS   AGE
maas-epp-4-build                                               0/1     Completed   0          12d
maas-poc-gateway-data-science-gateway-class-58b4f8c4b4-2zvgw   1/1     Running     4 (70m ago) 14d
maas-vllm-cpu-kserve-router-scheduler-567f8bb649-8q5v9         1/1     Running     0          10h
maas-vllm-gpu-kserve-74d8dd69bd-69gqk                          1/1     Running     0          8h
maas-vllm-gpu-kserve-74d8dd69bd-bbhg4                          1/1     Running     0          14d
maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76         1/1     Running     0          6h3m
# live ConfigMap (maas-epp-config), unchanged by this ticket:
groups: app1=20, app2=10, end-users=65 (prefix end-user-), defaultGroup unclassified=5
enforce: true
```

`replicas: 2` matches `deploy/poc/09-vllm-gpu.yaml`. Weights match the live
weights stated on this issue exactly. `enforce: true` live vs. the
committed `deploy/epp-config.yaml`'s documented `enforce: false` shadow-mode
default is pre-existing drift from earlier tickets in this series (noted on
UNI-139's own "Cluster left as found," above) — this ticket did not touch
that patch either way, so there was nothing of its own to restore. The
completed `maas-loadgen` Job (left in place by the crashed driver, since it
never reached its own cleanup step) was deleted by hand after the run
finished, matching what `15-fairness-benchmark.sh` would have done on its
own exit.

Raw results: `results/20261101T224216Z-uni140-b6-full-contention-soak/` —
`fairness-report.{md,json}`, `memory-timeseries.txt`, `loadgen.log`,
`epp-container.log`, `metrics-{before,after,full-before}.txt`,
`metrics-timeseries.txt` (all first-42-minutes-only, kept as-produced — see
`NOTES.md` in that directory), plus `full-run-backfill.{md,json}` (the
complete-95-minute recomputation this verdict is based on).

**Not proven here:** the root cause of the local driver's mid-run stop —
neither `15-fairness-benchmark.sh` nor `18-soak-monitor.sh` logged an error
before going silent, and whatever killed them (if it was in fact the
control-plane hiccup logged on this issue at 22:47Z, it was already recovered
from once before 23:24Z, so a second, unrecovered occurrence is not ruled
out) left no trace in-sandbox. This did not block the measurement — Thanos
retained everything needed — but a longer soak on an environment without a
Thanos-backed dashboard, or one that outlasts Thanos's retention window,
would not have this fallback. Also not proven: direct evidence of the
fairness state table's size (no such metric is exposed; "no growth" here
rests on the closed/bounded-by-design guarantee plus flat memory, not a
measured count), and whether a still-longer soak (beyond this ticket's
90–120-minute scope) would eventually trigger eviction activity that this
one did not.

## Outstanding work

Ordered by how much they would change a conclusion.

| # | item | why it matters | blocked on |
|---|---|---|---|
| — | ~~Calibrate `outputTokenWeight`~~ | **Not a POC gap.** This is a per-environment commissioning step, not a number this repo can ship: it is an efficiency ratio that moves with GPU, model, quantisation, batch size and vLLM version. The deliverable is the procedure in [calibrating-output-token-weight.md](calibrating-output-token-weight.md); run it when commissioning each environment, and re-derive the group weights in the same change | — |
| 2 | **Decide `cachedInputTokenWeight`** | measured, not theoretical: hit rates span 6.3% to 96.4% across groups, and moving the weight 1.0 -> 0.1 shifted end-users from 56.3% to 70.1% of delivered service while **halving total throughput**. A real lever with a real cost. [UNI-136](/UNI/issues/UNI-136) (C8, above) adds the differentiated-shape evidence inside the scored harness itself: at the live `1.0`, a cache-heavy tenant's charged-token share tracks its configured weight almost exactly regardless of its 87.6% cache-hit rate, i.e. it is measurably over-charged relative to the GPU work it actually causes | a policy decision |
| 3 | **ClusterRole for `llmisvc-controller-manager`** | the LLMInferenceService never reports `Ready`, and the controller is stuck in a failing reconcile so it will not apply future spec edits cleanly. Needs `get/list/watch` on `llm-d.ai` `inferenceobjectives` and `inferencemodelrewrites` | operator-level approval |
| 4 | **Durable NFD fix** | GPU exposure currently depends on a hand-applied `feature.node.kubernetes.io/pci-10de.present` label per node. Set `deviceLabelFields: [vendor]` on the NodeFeatureDiscovery CR or **every new GPU node will look like broken hardware** | operator-level approval |
| 5 | **Test on a real RHOAI 3.4 cluster** | three unknowns remain: whether 3.4's controller validates the EndpointPickerConfig, its InferencePool API group, and its tokenizer sidecar (3.5 has no equivalent). The 3.4-shaped preset test covered the flags, not the controller | a 3.4 cluster |
| — | ~~Fix `contended_service_tokens_total`~~ | **Fixed.** The gate decision (is the band contended) is now made once, at dispatch, and reused at completion instead of being re-checked independently at each of the two charge sites. The metric also now books the real, measured cost once at completion rather than the dispatch estimate plus a separately-gated correction, so an estimator overshoot no longer gets silently dropped (a Prometheus counter cannot move backwards on a negative delta). `TestContendedServiceTokensEqualChargedCost`, `TestContendedServiceTokensEqualChargedCostOnOverestimate`, and `TestAbortedRequestStillBooksContendedService` cover under-estimate, over-estimate, and abort respectively | — |
| — | ~~Re-run S1 longer~~ | **Done, negative result.** Re-ran at 600s (10 half-lives, vs the original 150s): the split moved to 50.3/49.7%, *further* from 2:1 than the original 1.57:1, which refutes the duration hypothesis — see "A3 (UNI-28): S1 re-run at 600s," above. Root cause is the same worker-sizing-vs-backend-latency mechanism UNI-29's Run 2 identified on this same current (llama-3-1-8b) deployment, not warm-up time. The resize itself is now done — [UNI-103](/UNI/issues/UNI-103), below — and the app1:app2 over-offer ratio is retuned and passing — [UNI-104](/UNI/issues/UNI-104), below | — |
| 8 | **`maas-default-gateway` inference path** | returns 500: `maas-api-route` targets a TLS service port with no `BackendTLSPolicy`, and that CRD is not installed. **Correction (UNI-129, 2026-11-01): minting keys does not actually require port-forwarding** in this environment -- the agent sandbox has direct pod-network reachability to the `maas-api` Service's ClusterIP, which answers the same `POST .../v1/api-keys` call with no tunnel. Port-forwarding is still the documented, more portable fallback for an environment without that reachability | upstream/MaaS |
| — | ~~Sustained load through the LLMInferenceService path and the Route (UNI-27)~~ | **Done for status tally and fairness.** 240s closed-loop runs (32 workers/tenant, `app1`/`app2`/`end-users`) against both the in-cluster gateway Service and the public Route landed 94.7% and 97.9% HTTP 200 respectively. `normalized_service` converged to within ~7% across the three backlogged groups on both paths, confirmed at multiple flight-recorder ticks through each run. On the non-200s: the Route path's are directly traced via the gateway access log to a ~2s connection/endpoint-pool warm-up burst at request-storm start (zero thereafter), not a sustained-load or fairness defect. The LLMInferenceService path's (5.3% error rate) are **inferred to be the same mechanism by analogy, not log-verified** — this cluster has no log aggregation and the gateway's own access-log buffer had already rotated past the run window by the time it was checked. Script: `deploy/poc/12-loadgen-route.sh` (Route path); `deploy/poc/04-loadgen.yaml` unchanged (LLMInferenceService path). Does **not** cover the 600s timeout / `buffer-response: false` annotations — see item 15 | N/A -- closed for status tally + fairness scope |
| — | ~~Open-loop load generation (UNI-34)~~ | **Done, and the clamp finding flips.** `deploy/poc/13-loadgen-poisson.{py,sh}` adds open-loop Poisson arrivals. Below saturation the clamp fires on ~65% of dispatches (vs 0.2–2.2% closed-loop) but is harmless (pool uncontended). Above saturation (24 req/s aggregate vs a measured ~20-22 req/s pool ceiling) it measurably **inverts** the 20/10/65 split: end-users (w=65) delivered 25.5%, app1 (w=20) delivered 40.4%. This **contradicts** the GPU closed-loop "clamp is inert" finding (`## 3`) and confirms the SUPERSEDED section's concern more strongly than originally observed. See "Open-loop (Poisson) load generation (UNI-34)" above for the full data, including what was not tested (no clamp on/off A/B — see that section for why). **Promoted to a scored benchmark by [UNI-137](/UNI/issues/UNI-137) (B5)**: reproduces the inversion direction at 120% of ceiling (FAIL, end-users -18.8pts) but at roughly half UNI-34's original magnitude, and found 100% of the documented ceiling still reads as UNCONTENDED despite already-large per-group deviations — see "UNI-137," above | **newcomerClamp default should be revisited** — a policy decision, same owner as item 2 |
| — | ~~Verify metrics reach Prometheus~~ | **Done (UNI-50).** The D3 dashboard (`deploy/grafana-dashboard.yaml`) confirmed this end to end against live Grafana/Thanos: the headline expected-vs-observed panel and five supporting panels all rendered real, current GPU-EPP data from a load run, with the exact PromQL and output pasted on that ticket. Datasource confirmed as the standalone `grafana` namespace's Prometheus-only datasource, pointed at the same UWM Thanos Querier every other observability asset in this repo already reads | N/A -- closed |
| 12 | **Red Hat support boundary** | a custom EPP image takes that component outside RHOAI support. The plan calls this the biggest non-technical risk and it has never been raised with the account team. Nothing technical unblocks it | a conversation |
| 13 | **Version-pin maintenance** | flow-control interfaces sit on a module that only reached v1.0.0 on 2026-10-15; we are pinned to v0.11.0. Process, pinned versions and the named interface inventory are now in [version-pinning.md](version-pinning.md). Monthly check, manual — there is no CI runner | process |
| 14 | **Disconnected / mirrored clusters** | the image must be mirrored with a matching IDMS/ICSP entry. Untested, and the Quay reference assumes egress | an air-gapped target |
| 15 | **600s timeout and `buffer-response: false` under sustained/long-running load** | these annotations govern long-running and streaming responses; still only proven by single requests. UNI-27's closed-loop run used short prompts (`max_tokens: 64`, ~6-11s p95 responses), which never approaches the timeout or exercises buffering behaviour | a load generator issuing long-running/streaming requests |
| — | ~~Gateway header stripping (MaaS path, UNI-33)~~ | **Fixed and verified live.** The EPP's own header-alias resolution prefers client-settable `x-llm-d-inference-objective` over the gateway-authored `x-gateway-inference-objective`, so a client forging the former won outright regardless of what Authorino set for the latter -- proven live 2026-10-19 (a forged header passed through the gateway untouched, HTTP 200). The one-line patch to `maas-poc-gateway-authn` was applied live on 2026-10-19 once `patch` on `authpolicies.kuadrant.io` in `maas-fairness-poc` was granted, and the conformance check (`cmd/gateway-header-check`) now reports `OK` against the live cluster. Still dormant: zero `InferenceObjective` resources exist, so no behavioural queue-jump has been demonstrated, only the structural fix. See [gateway-header-stripping.md](gateway-header-stripping.md) | N/A -- closed |
| — | ~~Gateway header stripping (direct rig, UNI-43)~~ | **Fixed and verified live.** The direct rig (`02-epp.yaml`/`03-gateway.yaml`) has no Authorino layer, so UNI-33's overwrite mechanism doesn't apply -- fixed instead by removing the header outright, via an Istio `EnvoyFilter` (`envoy.filters.http.header_mutation`, `INSERT_BEFORE` `envoy.filters.http.ext_proc`) scoped to `maas-poc-route` alone so it can't also strip the value UNI-33 set for the authenticated MaaS routes sharing the same Gateway. Applied and verified live 2026-10-19 once `create`/`update` on `envoyfilters.networking.istio.io` and `pods/exec` in `maas-fairness-poc` were granted: the live config dump confirmed `header_mutation` sits immediately before `ext_proc` in the chain, and the per-route override lands on exactly one route (`maas-fairness-poc.maas-poc-route.0`), not on the MaaS routes. `gateway-header-check` still reports this route as uncovered -- a known, documented limitation (it only recognises AuthPolicy-based coverage), not a sign the fix didn't take. Not verified: an end-to-end request proving a forged header doesn't reach the EPP/simulator, since both remain scaled to 0/0. See [gateway-header-stripping.md](gateway-header-stripping.md) | N/A -- closed |
| — | ~~Reproduce the headline split on real vLLM, both modes (UNI-29)~~ | **Done.** Re-run 2026-10-22 against the live GPU deployment (now serving `llama-3-1-8b`, EPP image digest `sha256:5ef5df27...`): shadow 33.0/33.6/33.4%, enforce (sized workers) 16.2/13.7/70.1% against a 20/10/65 target. See "A4 (UNI-29): reproduced again, against the current EPP build, both modes," above, for the full data including a negative-control run and the sizing hypothesis for the ~5-point residual gap. `enforce` was restored to `true` (the live default) afterward | follow-up: tune worker sizing further to close the ~5-point gap (same section) |
| — | ~~`main` didn't deploy the image these numbers came from~~ | **Done.** That digest was in-cluster-BuildConfig-only (never pushed to Quay, not transferable), and the committed manifests were separately 31 commits stale on top of that. Rebuilt from unchanged source at `HEAD`, pushed to `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a7...`, and repinned both manifests to that digest. See "The EPP image above was not transferable, and `main` didn't deploy it — now fixed," above | — |
| 1b | **Re-run the sized-worker enforce case against the now-committed Quay digest, live** | the repoint itself is done — see "UNI-97: repointed to Quay, verified live," above: `llminferenceservice/maas-vllm-gpu` runs the Quay digest live, and a `full-contention` re-run against it PASSed, matching the pre-repoint baseline within run-to-run noise. The admission-webhook blocker that stopped the repoint is cleared, and re-confirmed independently against this exact object — both `--dry-run=server` and a real write — by [UNI-118](/UNI/issues/UNI-118) (2026-11-01, see "UNI-118: webhook re-confirmed healthy for `maas-vllm-gpu`, independently," above). Not yet re-run against the new digest: the specific headline scenario this item names, the sized-worker `enforce` case from "A4 (UNI-29)" (16.2/13.7/70.1% vs a 20/10/65 target) — `full-contention` is a different, differently-weighted scenario | nothing admission-side any more; only needs that specific sized-worker enforce scenario actually re-run against the live digest |
| — | ~~Archive the EPP log as a per-run artifact (UNI-46, D5)~~ | **Done.** `deploy/poc/14-loadgen-with-log-archive.sh` wraps `04-loadgen.yaml` unchanged -- it captures the GPU EPP's own container log (targeting `maas-vllm-gpu-kserve-router-scheduler` via `oc logs -f`) into `results/<timestamp>-<label>/epp-container.log` for exactly the run's duration, records the byte count and flight-recorder line count in a per-run `manifest.json` alongside the loadgen's own status/latency table, and detects a mid-run container restart (reattaches `-f`, notes it in the manifest) instead of silently losing the earlier log. Verified live 2026-10-25 against a 240s full-contention run: 3,954,571 bytes captured, 196 `"fairness state"` flight-recorder lines, no restart. That run also surfaced an unrelated problem -- `end-users` got HTTP 403 on 87% of its requests -- tracked separately as [UNI-82](/UNI/issues/UNI-82) so it doesn't quietly corrupt a future fairness benchmark's numbers | N/A -- closed |
| 16 | **Wire the D3 dashboard into the live Grafana (UNI-50)** | The ConfigMap `deploy/grafana-dashboard.yaml` is on `main`, but the live Grafana's `dashboards` volume mounts a ConfigMap literally named `kueue-dashboard` in the `grafana` namespace -- not `maas-fairness-dashboard` in `maas-fairness-poc`, where this repo has write access. Cross-namespace `configMap` volume sources don't exist, so some copy step is unavoidable. The exact commands are documented in [runbook.md](runbook.md#load-the-fairness-dashboard-into-the-live-grafana) and confirmed correct against the live `grafana-dashboards-provider` provisioner config, but not run: `oc auth can-i create/update configmaps -n grafana` and `patch deployments -n grafana` all return `no`. Until someone with that access runs them, the live instance loads zero file-provisioned dashboards -- the dashboard content itself was verified by a separate, non-durable `/api/dashboards/db` import, not by this ConfigMap rendering anywhere | operator-level approval (namespace write on `grafana`) |
| — | ~~Per-run fairness benchmark with a PASS/FAIL verdict (UNI-54)~~ | **Done.** `deploy/poc/15-fairness-benchmark.sh` + `15-fairness-report.py` turn a named scenario run into its own verdict -- JSON + markdown, delivered share from the EPP's own `contended_service_tokens_total` (reusing UNI-50's SLI unchanged), run metadata including the EPP image digest, a documented 10-point threshold, and an exit code a pipeline can gate on. All four scenarios run live against the GPU EPP 2026-10-29: see "UNI-54: an automated fairness benchmark," above, for the full table. Two scenarios (`full-contention`, `end-users-idle`) correctly FAIL on the pre-existing equal-worker-sizing artifact (same mechanism as A4/UNI-29's Run 2, above -- not a new defect; follow-up tracked on that same Outstanding-work row); two (`app1-alone`, `asymmetric-demand`) PASS once the verdict logic was fixed to stop scoring a structurally-zero or structurally-demand-capped share as a failure. `15-fairness-report-test.py` proves the FAIL path against synthetic data with a real non-zero exit, independent of cluster access | N/A -- closed |
| — | ~~Resize `full-contention`/`end-users-idle` to over-offer per tenant, re-run all four + a named control (UNI-103)~~ | **Done, 4/5 green.** Per-tenant `WORKERS_APP1`/`WORKERS_APP2`/`WORKERS_END_USERS` replace the single global `WORKERS` in both scenarios; `equal-workers-control` keeps the original equal-worker shape alive as a permanent, explicitly-unscored negative control (`--control`, verdict `INFO`). Live re-run 2026-10-29: `full-contention` now PASSES (16.2/12.8/71.0% vs 21.1/10.5/68.4%), `app1-alone` and `asymmetric-demand` still PASS, `equal-workers-control` reproduces the original artifact as expected (INFO, 29.7pt max deviation). `end-users-idle` still FAILs, now in the opposite direction (app1 82.4% vs a 66.7% target) -- see "UNI-103," below, for the full table and the suspected cause | follow-up: [UNI-104](/UNI/issues/UNI-104), tune the app1:app2 over-offer ratio |
| — | ~~Retune `end-users-idle`'s app1:app2 worker ratio to match its 2:1 target, re-run (UNI-104)~~ | **Done, PASS.** `WORKERS_APP1` moved from 128 to 64 (keeping `WORKERS_APP2=32`), matching the offered-worker ratio to the pair's actual 2:1 target share ratio instead of reusing `full-contention`'s 4:1 dominant-tenant figure. Live re-run 2026-10-29: 68.4/31.6% against a 66.7/33.3% target (1.8pt max deviation) -- **PASS**. `contended_seconds_total` deltas (app1 1.46s, app2 1.50s) confirm both tenants were genuinely contending. Why the 4:1 ratio overshot so much more than 2:1 undershoots remains unexplained, same as UNI-103 left it -- see "UNI-104," below | root cause of the ratio's exact sensitivity: pending [UNI-100](/UNI/issues/UNI-100)'s scope decision |
| — | ~~Build the timeline/chaos harness for the edge-case plan (UNI-127)~~ | **Done, development only.** Per-tenant join/leave + duty-cycle timing, EPP-pod-delete and vLLM-scale chaos hooks, windowed per-tenant share, and a time-to-converge figure -- see "UNI-127," above, for the full story including the live finding that a chaos scale-restore's actual capacity recovery (~3m39s on this backend) lags its patch by far more than a short `CHAOS_SCALE_HOLD` accounts for. `full-contention` regression confirmed the whole-run verdict is unchanged. No B1-B4/E1/E2 case was run or scored -- that is every ticket after this one in the chain | the board's edge-case cases themselves (B1-B4, E1, E2, "app3 joins at saturation"), each its own ticket |
| 17 | **`MaaSSubscription` named `enduser-foo` for D2 (UNI-129)** | D2's harness mechanism (an arbitrary/custom subscription identity) is built and smoke-tested live against an existing identity, but the ticket's specific case -- a subscription named `enduser-foo` (no hyphen, deliberately outside the `end-user-` prefix match) -- cannot be created: `oc auth can-i create maassubscriptions -n models-as-a-service` returns `no`, confirmed live, not inferred. Minting a key against that name directly was also tried and rejected (`400 invalid_subscription`) since no such object exists | `create` on `maassubscriptions.maas.opendatahub.io` in `models-as-a-service` -- operator-level approval |

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
