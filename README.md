# maas-fair-share

A fairness policy plugin for the **llm-d Router (EPP)** that guarantees each MaaS
subscription a minimum share of a shared model's token throughput **when the model is
saturated**, and imposes no limit at all when it isn't.

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
> Also proven: the plugin runs under a real LLMInferenceService templated by
> RHOAI's own KServe preset (deploy/poc/05-llmisvc-sim.yaml) &mdash; HTTP 200 and a
> fairness dispatch recorded.
>
> Not yet done: `outputTokenWeight` is still the uncalibrated `2.0` placeholder
> (the calibration needs GPUs), the cached-token discount path is unexercised
> (the simulator reports `cached_tokens: 0`), and the production
> `deploy/llmisvc.yaml` path has not been applied. One open question — the
> newcomer clamp measurably *hurt* the split in this environment.
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

Weighted least-attained-service. Each group carries a decaying **tab** of recently
consumed tokens; the group with the lowest `tab ÷ weight` is served next. Equalising
`tab ÷ weight` *is* proportional sharing, so the ratios converge on the configured
weights without any constant describing how fast the GPUs are.

Three things make it work in practice, and each exists because the naive version
fails without it:

- **Exponential decay** — the tab measures recent usage, not all-time. One lazy
  `2^(-Δt/halfLife)` on read and write.
- **Newcomer clamp** — a returning-idle tenant is raised to the current minimum, so it
  goes first *once* rather than monopolising the pool for minutes. Without it,
  consuming spare capacity becomes a debt and work conservation is poisoned.
- **Provisional charge** — an estimate is charged at dispatch and trued up against the
  real `usage` block at completion. Generations take 10–30s while scheduling decisions
  happen every millisecond; without this a tenant dispatches thousands of requests
  before any lands on its tab.

## What it can and cannot promise

- ✅ "Under contention, app1 receives at least 20% of delivered throughput."
- ❌ "app1 is guaranteed 20,000 tokens/second."

Capacity loss lowers everyone's absolute throughput together — the *ratio* holds, the
*floor* does not. A tenant that sends no traffic receives nothing; capacity cannot be
reserved for requests that have not arrived.

## Platform compatibility

**The short version: RHOAI 3.4 and 3.5 both work. The plugin ships its own EPP
binary, so the platform's own EPP version does not gate it.**

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
docs/                 design notes
prototype/            FROZEN Python ext_proc prototype -- provenance, not a dependency
```

See [`prototype/README.md`](prototype/README.md) for what the original proved and
which parts of it the EPP architecture deletes outright.

## Rollout

Ships with `enforce: false` — **shadow mode**. The plugin classifies every request,
tracks every tab and publishes every metric, while leaving the existing dispatch order
untouched. The algorithm is the part least likely to be wrong on day one; the group
matching rules, the half-life and the cost weights are, and only real traffic knows
them.
