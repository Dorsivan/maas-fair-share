# maas-fair-share

A fairness policy plugin for the **llm-d Router (EPP)** that guarantees each MaaS
subscription a minimum share of a shared model's token throughput **when the model is
saturated**, and imposes no limit at all when it isn't.

> ### 📦 Deploying this somewhere new — especially a disconnected network?
>
> **Start at [AIRGAP-HANDOFF.md](AIRGAP-HANDOFF.md), not here.** It is the single entry
> point for an operator who has the repository and nothing else: what must already exist
> around this plugin, what has to cross the air-gap boundary (with the two blocking items),
> the deploy order, a five-rung test ladder for the first run, and the list of
> healthy-looking outcomes that are actually failures.
>
> This README explains *what the plugin is*. That document explains *how to stand it up*.

> Status: **implemented, and validated end to end on a GPU-free OpenShift cluster.**
>
> The plugin builds into a custom EPP image, loads, and under real contention
> divides delivered tokens according to the configured weights — measured at
> 23.8% / 13.5% / 62.8% against a configured 20 / 10 / 65, reproducible across
> runs, versus equal thirds in shadow mode. Work conservation verified: with
> one tenant idle the remaining two absorb the whole pool (93% of baseline
> throughput), and below capacity a second tenant costs the first no latency.
> Unit tests pass under `-race`.
>
> **Measured on two A100s with real vLLM: 20.5% / 11.6% / 67.9% against a
> configured 20 / 10 / 65**, with `normalized_service` converged to within 0.1%
> between app1 and end-users. Shadow mode on the same setup gives equal thirds.
> Traffic went through a real LLMInferenceService templated by RHOAI's KServe
> preset, over HTTPS, authenticated with real MaaS `sk-oai` API keys.
>
> One caveat that is easy to trip over and is NOT a plugin defect: a weighted
> split can only be observed if every tenant offers MORE load than its
> entitlement. With equal per-tenant concurrency the high-weight tenant runs
> out of work to be favoured with, its queue drains, and the surplus correctly
> goes to others &mdash; work conservation, which then reads as a broken policy.
> See docs/poc-results.md.
>
> `outputTokenWeight` ships as `2.0`, a deliberate placeholder: it is an
> efficiency ratio that moves with GPU, model, quantisation, batch size and
> vLLM version, so it must be measured **per environment at commissioning**.
> The procedure is
> [docs/calibrating-output-token-weight.md](docs/calibrating-output-token-weight.md).
> Changing it re-denominates the floors, so re-derive the group weights in the
> same change. `cachedInputTokenWeight` now has
> real data behind it (hit rates spanning 6.3%–96.4%) and needs a decision, not
> a measurement. Full list in
> [docs/poc-results.md](docs/poc-results.md#outstanding-work).
>
> The earlier concern that the newcomer clamp hurt the split was **refuted** on
> GPUs; those runs were demand-starved.
>
> Full write-up, including the pitfalls that produced healthy-looking runs that
> measured nothing: **[docs/poc-results.md](docs/poc-results.md)**.

## The problem

One large model serves production applications and interactive end users. Each
consumer should be guaranteed a floor of capacity under contention — app1 20%, app2
10%, end users as a single pooled group — while anyone may burst freely into capacity
nobody else is using.

A rate limit cannot express this. A `MaaSSubscription` becomes a Kuadrant
`TokenRateLimitPolicy`, which is a **hard ceiling that applies always**: at 3am on an
idle GPU, app1 is still cut off at its limit. The requirement is the opposite.

- A **rate limiter** says *"you may not exceed X"* — always on, wastes idle capacity.
- A **queue** says *"when there's a line, here's who goes next"* — does nothing until
  there is actually contention.

This repository builds the queue. **Kuadrant stays** — the two are complements: the
ceiling bounds what anyone may consume, this divides what's available when they
compete for it.

## Where it runs

```
client
  → OpenShift Gateway (Envoy)
      → Kuadrant        authenticates, applies the MaaSSubscription ceiling
      → EPP             ← THIS PLUGIN
          → vLLM pods
```

llm-d's flow-control subsystem already maintains one queue per tenant and already
decides when a slot is free. The one thing it delegates is *which tenant's queue goes
next* — a `FairnessPolicy`. That single decision is this plugin.

EPP plugins are compiled in, so this ships as a **custom EPP image**: upstream plus
one registered plugin, pointed at by `LLMInferenceService.spec.router.scheduler`.

## The algorithm

Start-time fair queueing (SFQ). Each group has a **finish tag** that only ever moves
forward: dispatching a request of cost `c` to group `g` sets its next start tag to
`S = max(finish[g], V)`, then advances `finish[g] = S + c/weight[g]`. `V`, the
system's virtual clock, is the *minimum* over currently-serving endpoints of the
newest start tag each one has begun serving. The plugin stamps `S` into vLLM's own
`priority` field, and vLLM's priority-ordered queue — where almost all in-flight
requests actually sit, not the EPP's own small one — dispatches by that number.
Equalising the rate finish tags advance *is* proportional sharing, so the ratios
converge on the configured weights without any constant describing how fast the
GPUs are.

This replaced an earlier design (UNI-293) where the EPP ranked its *own* queue by a
decaying **tab** of recently consumed tokens, the group with the lowest `tab ÷
weight` going next. That mechanism is why the tab still exists — the finish tag is
derived from it — but it stopped deciding dispatch order once the stamp landed: UNI-288
found the EPP only ever held 6–8% of in-flight requests, with vLLM's own FIFO queue
holding the rest and deciding the real order regardless of what the tab said. Under
the stamp, the tab is accounting and metrics only; the newcomer clamp and the ratchet
that used to protect it are off the dispatch path entirely (UNI-293's "one notion of
accumulated service").

One thing from the tab-only design still matters and still runs:

- **Provisional charge** — an estimate is charged at dispatch and trued up against the
  real `usage` block at completion. Generations take 10–30s while scheduling decisions
  happen every millisecond; without this a tenant dispatches thousands of requests
  before any lands on its ledger.

The stamp only decides anything if vLLM is actually running `--scheduling-policy
priority` — with it absent, the plugin still stamps `priority`, vLLM just ignores it
and dispatches FIFO, silently. See [docs/runbook.md](docs/runbook.md#enable-the-sfq-priority-stamp-uni-293303)
for the enable procedure and [docs/design.md](docs/design.md) ("UNI-293: SFQ priority
stamp") for the full mechanism, including the bounding (rebase/idle-reset) that keeps
the tag from growing without limit.

## What it can and cannot promise

- ✅ "Under contention, app1 receives at least 20% of delivered throughput."
- ❌ "app1 is guaranteed 20,000 tokens/second."

**This is by design, not a shortfall.** The board settled (2026-11-25) that
proportional share under contention is the product this plugin ships, and a
contractual throughput floor is an explicit non-goal — not something later work is
expected to close. Capacity loss lowers everyone's absolute throughput together; the
*ratio* holds. A tenant that sends no traffic receives nothing, by the same logic:
capacity cannot be reserved for requests that have not arrived.

## Platform compatibility

**The short version: RHOAI 3.4 and 3.5 both work. The plugin ships its own EPP
binary, so the platform's own EPP version does not gate it.**

### What the dev cluster actually is (read this before citing a version)

Both "3.4.4" and "3.5" are true of this cluster, which is why the two numbers
keep colliding in our notes. It is **not** a clean 3.4.4 install:

| Layer | Version | Evidence (2026-10-29) |
|---|---|---|
| Operator / platform | **3.4.4** | CSV `rhods-operator.3.4.4`, subscription channel `stable-3.4`, `DataScienceCluster.status.release` and `DSCInitialization.status.release` both `3.4.4` |
| KServe + LLMISVC control plane | **3.5.0 artifacts** | presets named `v3-5-0-kserve-config-*`; scheduler preset image `odh-llm-d-router-endpoint-picker-rhel9` annotated `app.kubernetes.io/version: 0.10.0`; running `kserve-controller-manager` / `llmisvc-controller-manager` digests do **not** match the 3.4.4 CSV's `relatedImages` |

The 3.4.4 bundle ships `odh_llm_d_inference_scheduler_image` and carries **no**
`llm-d-router` endpoint-picker image at all, so those presets are not its work.
The KServe objects were created **2026-09-07 21:08–21:11**, before the OLM
install plans for `rhods-operator.3.4.0` and `.3.4.4` (both `2026-09-08 07:58`),
and they still carry `internal.config.kubernetes.io/previousNamespaces:
opendatahub`. They are leftovers from an earlier 3.5.0 stack.

They persist because the 3.4.4 operator **cannot overwrite them**.
`DataScienceCluster/default-dsc` reports `KserveReady: False` and
`ModelControllerReady: False`, with reconcile errors that are structurally
unfixable in place:

- `odh-model-controller`: `spec.selector … field is immutable`
- `leader-election-role`: two owner references with `controller: true`
  (`Kserve/default-kserve` and `ModelController/default-modelcontroller`)

So the 3.5.0 KServe objects stay, and every `LLMInferenceService` here —
including both of ours, `maas-vllm-cpu` and `maas-vllm-gpu` — resolves its
`baseRefs` to `v3-5-0-kserve-config-llm-scheduler`. (A `rhods-operator.3.4.5`
install plan has been sitting unapproved since 2026-10-19; approving it will not
clear this, because the blocker is the immutable field, not the operator version.)

**Consequence for this POC: every result in [docs/poc-results.md](docs/poc-results.md)
was produced against a 3.5.0 KServe data plane.** Where that document says
"RHOAI 3.4.4" it means the operator CSV, not the controller that templated the
scheduler. The 3.4 compatibility claim below rests on the flag-level test in
`deploy/poc/06-rhoai34-shape.yaml` plus source and image-label inspection — not
on a run against a coherent 3.4 KServe stack, which we have never had. The three
open unknowns in "Still unverified on a real 3.4 cluster" are therefore still
open, and item 5 of the Outstanding work ledger still needs a real 3.4 cluster.

### Why the versions diverge in the first place

That is worth stating plainly because the obvious reasoning is wrong. RHOAI 3.4
ships an EPP with **no flow-control subsystem at all** — no `FairnessPolicy`, no
`FlowKey`, no queues — which looks like a hard blocker. It isn't, because we
replace that container.

### Which EPP each release ships

The component was renamed mid-stream, which obscures the picture. `llm-d`'s
`llm-d-inference-scheduler` **became** `llm-d-router`; the repo redirects. The
rename happened at **v0.9.0**, the same release that introduced flow control.

| RHOAI | Upstream component | Version | Flow control |
|---|---|---|---|
| 3.3, **3.4.x** | `llm-d-inference-scheduler` | v0.7.x | **no** |
| **3.5**, 3.6 | `llm-d-router` | v0.10.0 | yes |
| *this plugin builds against* | `llm-d-router` | **v0.11.0** | yes |

Verified three ways: the source trees (`FairnessPolicy` absent at v0.7.1/v0.8.0,
present from v0.9.0, with positive controls proving the grep); image labels
(`version`, `url`, `vcs-ref` via `oc image info`, which is the only way to read a
version off a digest); and Red Hat's per-release branches — `rhoai-3.4` exists
only in `red-hat-data-services/llm-d-inference-scheduler`, while
`llm-d-router` starts at `rhoai-3.5`.

### Why 3.4 still works

Plugins are compiled in; there is no dynamic loading. So `Dockerfile.epp` builds
a **complete, standalone EPP** — the full upstream binary plus one registered
policy — and lands it at `/app/epp`, the exact path the KServe preset's
templated command invokes. We override only `image:`, never `command`/`args`.
Flow control therefore comes from *our* binary, not the platform's.

Both releases provide what that needs, identically:

- the scheduler container is named `main`, so the image override merges;
- `router.scheduler.config.ref` exists in both APIs (`SchedulerConfigSpec` is
  unchanged), and the controller appends our YAML as `--config-text`;
- every flag either release templates is one upstream v0.11.0 accepts.

With one exception, which is why `registerDownstreamCompatFlags()` exists in
`cmd/epp/main.go`: under TLS, **3.4 templates
`--model-server-metrics-scheme=https`** — a flag present only in Red Hat's
downstream fork, in no upstream release. pflag treats an unknown flag as fatal,
so without the shim the pod crash-loops on every 3.4 cluster and the failure
looks like a bad image.

Confirmed empirically in `deploy/poc/06-rhoai34-shape.yaml`, which runs our
image against the scheduler command copied verbatim from the `rhoai-3.4`
branch: the flag rendered, the binary parsed it
(`"model-server-metrics-scheme":"https"`), zero flag-parse errors, pod `1/1
Running` with 0 restarts, `maas-weighted-fairness` instantiated.

### Still unverified on a real 3.4 cluster

The test above used a 3.4-shaped *preset* under a 3.5 *controller*, so three
things remain open:

1. Whether 3.4's controller validates the `EndpointPickerConfig` before passing
   it through. The field is a `RawExtension`/ConfigMap ref, which suggests
   passthrough, but that is inference.
2. The InferencePool API group 3.4 creates versus what a v0.11.0 EPP watches.
   3.4's pool uses the same v1 shape (`endpointPickerRef` + `targetPorts`).
3. **The tokenizer sidecar.** 3.4's preset adds a second container
   (`llm-d-uds-tokenizer:v0.7.1`) sharing a controller-injected `tokenizer-uds`
   volume. 3.5 has no such container. Untested, and the most likely surprise.

## Layout

```
cmd/epp/              main: register the plugin, hand off to the upstream runner
pkg/fairness/weightedlas/
                      the plugin -- policy, state, grouping, cost model, metrics
deploy/               EndpointPickerConfig, LLMInferenceService, PodMonitor, RBAC
deploy/poc/           GPU-free rig: direct EPP, LLMInferenceService, 3.4-shape test
deploy/maas/          Models-as-a-Service install (Kuadrant, TLS, DB, gateway)
deploy/logging/       applyable manifests for that install spec (not applied)
docs/                 design notes, POC results, runbook, calibration procedure,
                      the Logging/LokiStack install spec
prototype/            FROZEN Python ext_proc prototype -- provenance, not a dependency
```

See [`prototype/README.md`](prototype/README.md) for what the original proved and
which parts of it the EPP architecture deletes outright.

## Rollout

Two independent switches, both shadow-first by convention — flipping one does not
flip the other, and checking one does not tell you the other's state:

- **`enforce`** governs the EPP's own pick, which only ever decided the ordering of
  the small share of in-flight requests the EPP holds directly (6–8%, per UNI-288).
  Ships `false`.
- **`sfqPriorityStamp`** governs the start-time fair-queueing tag stamped into
  vLLM's `priority` field — where the real reordering happens, since vLLM holds the
  other 90%+. The Go-level default and the production config template
  (`deploy/epp-config.yaml`) ship it `false`. The POC rig's committed config
  (`deploy/poc/00-config.yaml`) has shipped it `true` since UNI-309, so a clean
  deploy of this repo's own POC manifests is **not** shadow mode for dispatch order,
  even with `enforce: false`.

With either switch off, the plugin still classifies every request, tracks every
tab/tag and publishes every metric — the switches only decide whether that
bookkeeping is allowed to change serving order. The group matching rules, the
half-life and the cost weights are the parts most likely to be wrong on day one, and
only real traffic knows them; see
[docs/runbook.md](docs/runbook.md#enable-the-sfq-priority-stamp-uni-293303) for how
to check which state a given deployment is actually in.
