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

## Layout

```
cmd/epp/              main: register the plugin, hand off to the upstream runner
pkg/fairness/weightedlas/
                      the plugin -- policy, state, grouping, cost model, metrics
deploy/               EndpointPickerConfig, LLMInferenceService, PodMonitor, RBAC
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
