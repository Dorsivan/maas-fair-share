# Weighted fair-share across MaaS Subscriptions in the llm-d Router

> **Part 1** explains what we're building and why, assuming no Go or llm-d knowledge.
> **Part 2** is the implementation detail for whoever writes the code.
> **Part 3** is what you need to decide or accept.

## Execution order

The sequencing matters more than it looks — several parameters can't be chosen until
earlier steps produce data, and getting this backwards means reading dashboards
denominated in a unit you're about to change.

1. **Create the repo** — private `github.com/Dorsivan/maas-fair-share`, Go module at
   root, Python prototype copied into `prototype/` frozen (see Repository layout).
2. **Settle the support-boundary question** (Part 3 item 1) before writing much code.
3. **Calibrate `outputTokenWeight`** with the two-run `guidellm` experiment (Part 2).
   Twenty minutes, and it replaces the most arbitrary number in the config.
   *Before* shadow mode, because it changes the unit every later number is read in.
4. **Set the vLLM flags** and the gateway header stripping — both are silent
   prerequisites that live outside this plugin (Part 3 items 4 and 10).
5. **Build and deploy in shadow mode** (`enforce: false`) with the PodMonitor and RBAC
   in place; verify metrics actually arrive before trusting any graph.
6. **Read the per-group traffic shape table** — prompt tokens, cached fraction, output
   tokens, *with distributions*. This single table decides `cachedInputTokenWeight`,
   confirms or rejects `costModel: vramtime`, and validates the group-matching rules.
   It is the real deliverable of the shadow period, not the convergence graphs.
7. **Set the group weights** from that data, summing to 100.
8. **Run the load test**, including P4 with `newcomerClamp` both ways.
9. **Flip `enforce: true`** and compare the same graphs across the cut.

---

# Part 1 — What we're building, in plain terms

## The problem

One big model serves everyone: production applications and interactive end users. You
want each consumer guaranteed a minimum share of capacity when the model is busy
(app1 20%, app2 10%, …), and **no limits at all** when it isn't.

That second half is what makes this hard. A normal rate limit can't do it.

## Why MaaS alone can't solve it

A `MaaSSubscription` turns into a Kuadrant `TokenRateLimitPolicy` — a hard ceiling,
e.g. "app1 may use 200k tokens/minute." That ceiling applies **always**. At 3am with
an idle GPU, app1 still gets cut off at 200k. You asked for the opposite.

The distinction that matters:

- A **rate limiter** says *"you may not exceed X"* — always on, wastes idle capacity.
- A **queue** says *"when there's a line, here's who goes next"* — only does anything
  when there's actually contention.

You need a queue. Rate limiters live at the gateway; the queue lives further down, in
the component that decides which GPU serves each request.

**These are complements, not alternatives.** Keep Kuadrant for the ceiling (nobody
exceeds what they paid for) and add the queue for the split (when the pool is short,
the available capacity is divided by weight). Worth stating that way in the design doc,
because it's the clearest one-line summary of the architecture.

## Where the code goes: the request path

```
client
  → OpenShift Gateway (Envoy)
      → Kuadrant        — authenticates, applies the MaaSSubscription ceiling
      → EPP ("Endpoint Picker")   ← OUR CODE GOES HERE
          → vLLM pods (the actual GPUs)
```

The **EPP** — part of the llm-d Router, deployed by KServe as a pod next to your model
— is a smart load balancer. For every request, Envoy pauses and asks the EPP "which
pod should serve this?" The EPP knows each vLLM pod's KV-cache usage and queue depth,
so it answers better than round-robin could.

Critically, the EPP can also answer **"not yet — wait."** That's the waiting room, and
that's the feature we're using.

## What "writing a plugin" actually means here

This is the single most important practical consequence, and it's unintuitive.

The EPP's plugins are **compiled into the binary**. There's no dynamic loading — no
dropping a file into a running pod, no sidecar, no config flag that pulls in new code.
A plugin is Go source that gets built into the EPP executable.

So "add a plugin" really means:

1. Create a small Go project that imports the upstream llm-d router as a library.
2. Add your plugin code, and ~10 lines of `main` that register it and then hand off to
   the upstream startup routine.
3. Build a **container image** from that.
4. Tell KServe to run *your* image instead of the stock one.

Your image is the stock EPP plus one extra plugin. Everything upstream still works
identically; you're adding, not replacing.

Two consequences:
- **Config changes that aren't just YAML require a rebuild.** Weights are YAML (fine).
  Algorithm changes are a rebuild and redeploy.
- **Red Hat support.** A custom image puts the EPP outside RHOAI's support boundary.
  This is a real conversation to have, not a footnote.

## The waiting room: flow control

llm-d has a subsystem called **flow control** (off by default; enabled with a feature
gate). When the pool is saturated, incoming requests don't fail — they queue inside the
EPP.

The important structural fact: **there is one queue per tenant**, keyed by something
called a `FlowKey`. The EPP already builds these queues, tracks how long things have
waited, expires stale requests, and sheds load. All of that exists.

What it doesn't have is a good answer to one question: **when a slot frees up, which
tenant's queue goes next?** That decision is a pluggable interface called a
`FairnessPolicy`. Upstream ships a few (round-robin, strict priority, and an
equal-share one).

**Our plugin is an implementation of that one decision.** That's the whole thing. It is
a much smaller piece of work than it sounds, because all the queueing machinery is
already built.

## Why "no limits when idle" requires no code

This is the nicest property of the design and it's worth internalizing.

The EPP only calls our policy when (a) a slot is free and (b) there are **non-empty**
queues to choose between. If only one tenant is sending traffic, there's only one
non-empty queue, so our policy picks it every single time. It gets 100% of the pool.

If nobody is queued at all, our code is never called.

So the "don't limit anyone when there's spare capacity" requirement isn't a feature we
implement — it's a consequence of only ever being asked when there's a line. Your
Python prototype needed an explicit `if total_used >= max_tokens_per_window` gate and
a guess at the pool's capacity. Both disappear here. **Don't write a saturation check;
it would be wrong.**

## The algorithm: a running tab

Think of each tenant having a **tab** of tokens they've recently consumed.

1. **Track the tab.** When a request finishes, the response tells us exactly how many
   tokens it used. Add that to the tenant's tab. Output tokens count double, because
   generating is roughly twice as expensive as reading the prompt. Prompt tokens the
   GPU didn't have to recompute (because an earlier request left them cached) *could*
   be discounted — but we start **without** that discount. It's a far bigger and more
   group-specific lever than it looks; see Part 3.

2. **Divide by weight.** This is the whole trick. Compare tenants on
   `tab ÷ weight`, not on `tab`. A tenant with weight 20 can run a tab four times
   bigger than one with weight 5 before it's considered "ahead."

3. **Lowest adjusted tab goes next.**

4. **Forgive the tab over time.** Every 60 seconds, half of each tab evaporates
   (exponential decay). So it measures *recent* usage, not all-time. **That 60 seconds
   is your tightness knob** — the single most important number to tune, and it's YAML.

Why this converges exactly: if everyone stays busy, always serving the lowest
`tab ÷ weight` pushes all of those values toward being equal. And "equal `tab ÷ weight`"
means tabs are in proportion to weights — which is exactly proportional sharing. This
is a standard, well-studied result (Weighted Fair Queueing, used in network routers
since the '90s), not something we're inventing.

It's also **scale-free**: no constant anywhere describes how fast your GPUs are. Add
replicas, change models, change request sizes — the ratios still hold. That's the main
thing it buys over the Python prototype, which had to be told `max_tokens_per_window`.

### Worked example

Weights: app1 = 20, app2 = 10, end-users = 5. All three saturating the pool.

| Tenant | Weight | Tab (tokens) | Tab ÷ weight |
|---|---|---|---|
| app1 | 20 | 40,000 | 2,000 |
| app2 | 10 | 18,000 | 1,800 |
| end-users | 5 | 11,000 | **2,200** |

app2 has the lowest adjusted tab → **app2 goes next**. Note end-users has by far the
smallest raw tab but is served *last*, because relative to its small weight it's
already ahead. Left running, this settles at tabs of 20 : 10 : 5.

## Weights are relative — and this changes your mental model

You said "20%". Weights aren't percentages; they're ratios among **whoever is currently
busy**. With weights 20 / 10 / 5, if only app1 and app2 are active, app1 gets
20/(20+10) = **67%**, not 20%. That's correct and desirable — app1 is absorbing
end-users' unused share.

So where does the 20% guarantee come from? **Make the weights sum to 100** across every
group including the catch-all:

```
app1 20  +  app2 10  +  end-users 65  +  unclassified 5   =  100
```

Now each group's weight *is* its guaranteed floor when everyone is busy, and anything
above that is a bonus from idle neighbors. This maps directly onto how you described
the requirement, and it makes the config self-documenting. I'd adopt it as the
convention.

## Two things that break naive implementations

These are the parts most likely to be gotten wrong, and both are invisible until
production.

**1. The returning-idle tenant.** A tenant away for 10 minutes has had its tab decay to
roughly zero. It comes back with a clean slate, is the lowest for everyone, and wins
*every* decision until it catches up — monopolizing the pool for tens of seconds while
everyone else stalls. Note the decay *causes* this; it doesn't help.

The fix is standard in fair queueing: **when you rejoin the line, your tab is raised to
at least the lowest tab currently in the line.** You still go first — a returning
tenant should get low latency, that's the point — but you go first *once*, not a
thousand times. No tuning parameter required.

> **"Isn't the burst intended? They're under their share."** Reasonable, but three
> things break it.
>
> **(a) It doesn't actually implement that intent.** `A_i` decays toward zero and
> *stops*. Idle 10 minutes, 10 hours, or a week all return at `A ≈ 0` and produce an
> **identical** burst. There's no deficit being tracked, just a counter that bottomed
> out — so it isn't proportional repayment, it's unbounded credit. Real accumulated
> fairness needs an explicit deficit and a repayment horizon, and that horizon is
> already the half-life. The clamp just stops credit accruing beyond it.
>
> **(b) It violates the floors you did promise.** app2's 10% floor is broken for the
> ~1–2 minutes of catch-up, to over-deliver on a guarantee nobody made. The SLA is
> *"at least 20% of delivered throughput **under contention**"* — a floor, not a quota
> over wall-clock time including the hours app1 was asleep.
>
> **(c) It poisons work conservation — the headline feature.** app2 consuming app1's
> unused capacity is exactly the intended behaviour, but it drives app2's `A` to a
> high steady state, so app2 is starved later *because* it used the free capacity.
> Had it sat idle it would have returned even. **Spare capacity stops being free and
> becomes a loan, and the rational play becomes not to use it.** Work conservation and
> accumulated-deficit fairness are structurally incompatible; the clamp is what
> protects the requirement you stated first.
>
> **Where the intuition is right:** "unused entitlement is spendable later" is *quota*
> semantics, and it belongs one layer up — Kuadrant's `TokenRateLimitPolicy` counts
> over a billing window and genuinely can carry a balance. The EPP divides contention
> *now*. Mixing the two breaks the lower layer.
>
> And the clamp is gentler than it sounds: it fires only on the **empty → non-empty**
> queue edge (a tenant trickling traffic is never clamped), it's a floor rather than a
> reset (`if S_i < floor`), and it targets the *minimum*, so a returning tenant still
> leads the pack — it just can't lap it.

**2. We're blind while requests are in flight.** We only learn the real token count
when a response completes, which for a long generation is 10–40 seconds. The scheduler
makes decisions every millisecond. So between a tenant's first dispatch and its first
completed response, its tab doesn't move, and we'd happily dispatch it **thousands**
more times. Under a burst, that's a complete loss of the guarantee for the first
half-minute.

The fix: charge an **estimate** up front (from the request's `max_tokens` and size),
then correct it when the real number arrives — like a hold on a credit card that's
settled later. I expect this to be the single largest effect in the whole design, and
the upstream equal-share plugin doesn't do it.

## What we can and cannot promise

**Be careful how you write this into an SLA.** When the pool is completely saturated,
the EPP dispatches *nobody* for a moment — there's no per-tenant decision to be fair
about. What our policy controls is the **order the backlog drains** in the moments
between.

- ✅ "Under contention, app1 receives at least 20% of delivered throughput."
- ❌ "app1 is guaranteed 20,000 tokens/second."

If a GPU node dies, everyone's absolute throughput drops together — the *ratio* holds,
the *floor* doesn't. And a tenant that doesn't send traffic gets nothing; we can't
reserve capacity for requests that haven't arrived. Pair the ratio guarantee with
ordinary capacity planning: the sum of promised floors should fit inside measured
capacity with margin.

## How you'll know it works in production

Three layers, because the bench test won't tell you anything at 3am.

**The measurement trap, first.** You cannot judge this from a raw throughput ratio.
Real tenants don't send equal load. app1 holding weight 20 but using 5% of tokens is
*correct* if it only sent 5% of the requests. A dashboard comparing delivered share to
configured weight will show a permanent, meaningless violation and be ignored within a
week. The share is only meaningful **over periods where that tenant had a queue AND the
pool was saturated** — so the plugin will count those seconds explicitly and use them
as the denominator. That conditional number is the real health metric.

**Shadow mode — the answer to "how do we test this in production."** The plugin gets an
`enforce: false` setting. It classifies every request, tracks every tab, and publishes
every metric — but lets the existing first-come-first-served order stand. Nothing about
live traffic changes.

Deploy that way first. After a week of real traffic you'll know which tenants actually
contend, whether your group-matching rules match reality, how much traffic falls into
the catch-all, and what half-life your traffic pattern wants. Then flip `enforce: true`
and compare the same graphs across the cut. The thing most likely to be wrong on day
one isn't the algorithm — it's the matching rules and the half-life, and only real
traffic knows those.

**Then:** Prometheus metrics (per-tenant share, convergence, misclassification), a live
`/debug/plugins/state` endpoint that dumps the current tab table as JSON on demand, and
a periodic structured log line that records the same table but only while contended —
so there's a flight recorder in Loki even without Prometheus.

One gap to close: KServe exposes the EPP's metrics port but **creates nothing that
scrapes it**, and the endpoint requires authentication by default. Without adding a
PodMonitor and RBAC, all these metrics go into a vacuum.

## Grouping end users

End users span many subscriptions but must share one weight. If we keyed queues by
subscription ID, `end-user-a` and `end-user-b` would each get weight 5 as *separate*
queues — so end users collectively get 10, and it grows with every subscription added.
Wrong.

Instead we collapse subscription IDs to a group name *before* the queue is chosen:
exact matches for applications, a prefix rule (`end-user-`) for everyone else, and a
catch-all. All end users land in one queue holding one weight, no matter how many
subscriptions exist. This also keeps the design flat — no nested queues-within-queues.

The fragility: a typo like `enduser-foo` silently falls into the catch-all. The plugin
counts those and we alert on them, because nothing else would catch it.

## Security: headers must be stripped at the gateway

The EPP lets a request name its own queue via the header
`x-llm-d-inference-fairness-id`. Left alone, any client could send
`x-llm-d-inference-fairness-id: app1` and inherit app1's weight.

Two defenses, both needed:
- Our plugin **overwrites** that value from the authenticated subscription, so a spoof
  is ignored even if it reaches us. (This is why we set it ourselves rather than using
  the stock identity plugin, which only fills it in when it's *empty* — that one is
  spoofable.)
- The gateway must still strip it, plus `x-gateway-inference-fairness-id`, plus
  **`x-llm-d-inference-objective`**. That last one is the sneaky one: it sets the
  request's *priority band*, and tenants in a higher band are served ahead of our
  weighted band entirely rather than weighted within it. Total bypass. Easiest to miss.
  See [gateway-header-stripping.md](gateway-header-stripping.md) for the fix and the
  conformance check that keeps a later route addition from reopening it silently.

---

# Part 2 — Implementation

## Decisions

| Decision | Choice |
|---|---|
| Resource divided | Token throughput (weighted Least-Attained-Service) |
| Flow granularity | Subscription **group** — many subscriptions collapse to one flow |
| Weight source | Static `parameters` in the EndpointPickerConfig |
| EPP replicas | 1 (exact accounting; no distributed state ships in-tree) |
| Tightness | 60s half-life, tunable by config |
| Config changes | Accept an EPP restart |
| Placement | Out-of-tree Go plugin in a custom EPP image |
| Rollout | Shadow mode (`enforce: false`) first, then enforce |

## What already exists (reuse, do not rebuild)

- **`FlowKey{ID, Priority}`** — `ID` is documented as "tenant ID or a model name".
  Each unique key already gets its own queue.
- **Work conservation is structural.** `PriorityBandAccessor.IterateQueues` visits only
  *non-empty* queues.
- **Token accounting** — `ResponseBodyProcessor` receives
  `Usage{PromptTokens, CompletionTokens, PromptTokenDetails.CachedTokens}`.
  No tokenizer and no render sidecar needed.
- **`program-aware-fairness`** (`pkg/epp/framework/plugins/flowcontrol/fairness/program-aware/`)
  — the structural template: factory, `sync.Map` tenant state, lazy `exp2` decay,
  `enqueueTimeKey` stashed in `Pick` and read in `PreRequest`, TTL eviction sweeper on
  `handle.Context()`, `GetCollectors`/`DeleteSharedSeries`.
- **Per-tenant metrics already labelled `fairness_id`** — `llm_d_epp_request_input_tokens`,
  `_output_tokens`, `_cached_tokens`, `llm_d_epp_flow_control_queue_size`,
  `_request_queue_duration_seconds`. Do not duplicate these.
- **`/debug/plugins/state`** (`pkg/epp/server/plugin_state_debug.go`, documented in
  `docs/plugin_debug.md`) — implement `StateDumper` and the live table is served on the
  admin port under existing auth.
- **`metricsutil.BoundFairnessID`** (`pkg/common/observability/metrics/cardinality.go`,
  limit 1000) — route every label through it. `program-aware` does *not*, which is a
  cardinality gap; don't copy that.

**Cannot be reused — verified, don't waste time trying:**

- **program-aware's `Strategy` seam is closed.** `newStrategy` is unexported and is a
  literal switch over `"las"`/`"turn-priority"`; there is no `RegisterStrategy`.
  `programMetrics` is unexported, so embedding and overriding `Pick` can't reach the
  state either. Write a standalone plugin that copies the structure, not the code path.
- **The conformance suite is not importable.** `fairness/functional_test.go` is a
  `_test.go` file, so `runPickConformanceTests` can't cross a module boundary. Copy it
  (~120 lines; it depends only on the importable `.../flowcontrol/mocks` package).

## Grouping before the FlowKey

Confirmed in `pkg/epp/requestcontrol/director.go` (~line 238): `runRequestHeaderProcessors`
runs **before** the FairnessID fallback, and the fallback is guarded by
`if FairnessID == ""`. So a `RequestHeaderProcessor` can write `request.FairnessID` and
the director honours it:

```go
sub := request.Headers[p.cfg.IdentityHeader]   // headers are lowercased
request.FairnessID = p.groups.Resolve(sub)     // overwrite unconditionally
```

Unconditional overwrite is what defeats header spoofing (see Part 1).

## Weighted LAS

Let `A_i` be time-decayed attained service in weighted tokens and `w_i` the weight.
Pick `argmin S_i` where `S_i = A_i / w_i`.

Store `A_i` **raw** and divide on read, so editing a weight doesn't retroactively
rewrite history. Decay commutes with the division, so one lazy
`A_i *= exp2(-Δt/halfLife)` on read and write covers both.

```
cost      = wIn*(prompt - cached) + wCached*cached + wOut*completion
S_i       = decay(A_i) / w_i
score_i   = S_i - agingTokensPerSecond * headWaitSeconds
pick argmin(score_i)
```

Keep `cost` behind a `costModel` switch with one function per model, so the unit being
divided is a config change rather than a refactor (`tokens` is the only one shipping;
`vramtime` = `O*(P+O/2)` is specified in Part 3 item 9 and gated behind a measured
trigger). Everything downstream of `cost` is unit-agnostic — weighted LAS is
scale-free, so no constant elsewhere assumes a magnitude.

Use raw units for the aging term, not `program-aware`'s double `rangeNormalize`.
Range-normalizing rescales against the currently-backlogged set, so the mapping changes
every cycle and the equilibrium has no fixed point corresponding to any allocation
ratio. Default `agingTokensPerSecond: 0` = pure proportional ordering.

Sort candidates by ID before scoring — `IterateQueues` order is unspecified and
`program-aware` ranges a Go map, so its tie-breaking is nondeterministic run to run.

### Returning-from-idle clamp

Implement as `bandState` returned from `NewState` (program-aware returns `nil` here, so
this is genuinely new):

```go
floor := max(bandState.virtualTime, min S over current candidates)
// on the false->true backlogged edge only:
if S_i < floor { setService(floor * w_i); S_i = floor }
// after choosing the winner:
bandState.virtualTime = S_winner
```

Both terms are needed: `virtualTime` is the textbook `V(t)` and handles a cold start
where everyone legitimately begins at 0; `min over backlogged` handles a band that went
fully empty leaving `virtualTime` stale.

### Provisional charge at dispatch

**Never invoke the tokenizer.** Use `Body.TokenizedRequest.TokenCount()` *only* if the
token-producer already ran for another plugin's benefit — opportunistic reuse, never a
triggered cost. Three reasons: (a) after wOut calibration the cost is ~`P + 8×O`, so
precision on `P` refines the ~10% term while `O` — the ~90% term — stays a guess;
(b) it is milliseconds of CPU per request on the one `replicas: 1` component every
request traverses, which fails open when it stalls; (c) true-up makes the whole
question low-stakes. `bytes/4` is also most accurate exactly where `P` matters most —
the chars-per-token ratio converges with prompt length, so long prompts estimate well
and short noisy ones contribute little. At the default `cachedInputTokenWeight: 1.0`
the cached term drops out of the formula entirely and `C` needs no estimate at all.

- **Input:** `TokenizedRequest.TokenCount()` if already present, else
  `RequestSizeBytes / estimatedBytesPerToken`.
  `RequestSizeBytes` includes JSON framing, so this biases slightly **high** — the
  safe direction, since over-charging only makes a tenant briefly more restrained
  while under-charging is what permits over-dispatch.
- **Output — where the effort belongs.**

  ```
  O_est = min( max_tokens ?? ∞ , ewma[group] ?? defaultEstimatedOutputTokens )
  ewma += (actual_O - ewma) / 64        # updated at every true-up
  ```

  **Count-based, not time-based** — "what a typical request from this group looks
  like" is a per-request property; a quiet group's estimate shouldn't decay.
  **Mean, not median** — output lengths are right-skewed and often bimodal (short
  errors + long generations); we're estimating *expected cost*, so the mean is
  unbiased and a median would systematically under-charge the tail.
  **`max_tokens` as a cap, never as the estimate** — clients set 4096 and generate
  200, so it is exact as a bound and useless as a central value.
  Warm-up: require ≥8 samples before trusting the EWMA. Nearly free — the true count
  is already observed at every true-up and per-group state already exists. Gaming
  exposure (depress your own EWMA with short requests, then send long ones) is bounded
  to one request duration by the true-up.

**Worked trace.** `RequestSizeBytes=8400`, `max_tokens=2048`, group `end-users` with
`ewma=380`; `wIn=1`, `wOut=8`, `bytesPerToken=4`, `H=60`:

```
P_est    = 8400 / 4       = 2100
O_est    = min(2048, 380) =  380
cost_est = 2100 + 8*380   = 5140     -> charged; stash {charged: 5140, at: t0}

...completes 25s later, usage {prompt_tokens: 1987, completion_tokens: 642}

cost_actual = 1987 + 8*642    = 7123
delta       = 7123 - 5140     = 1983
A          += 1983 * 2^(-25/60) = 1983 * 0.749 = 1485
ewma        = 380 + (642-380)/64 = 384.1
```

`P_est` landed 5.7% high (bytes/4 + JSON overhead, as expected); the output estimate
was 41% low and contributed essentially all of the correction. That asymmetry is the
whole argument for spending effort on `O` and none on `P`.

**Failure modes.** A request that never completes (client disconnect, no final
`ResponseBody` hook) leaves its charge on the tab to decay away over a few half-lives
— conservative, self-healing, and caught by the accounting-leak alert. Concurrent
requests from one tenant each carry their own `{charged, at}` attribute and reconcile
independently, which is precisely why the charge is stashed per-request rather than in
a per-tenant counter.

- All fields already on `fwksched.InferenceRequest`.
- Stash the charged estimate **on the request** via a `plugin.NewDataKey("provisional-cost", …)`
  attribute, not a per-tenant counter — concurrent requests need per-request
  reconciliation, and attribute lifetime tracks the request so it can't leak.
- True up in `ResponseBody` gated on `resp.EndOfStream` (the final hook for both
  streaming and non-streaming); earlier chunks are no-ops.
- **Decay the correction — do not add the raw delta.** The provisional charge has been
  decaying for the whole generation (at `H=60` a 30s request's charge is down to 71%
  by completion). Adding `actual − charged` undecayed attributes the estimate to
  dispatch time and the correction to completion time, so the final tab depends on how
  wrong the estimate was. Store the dispatch timestamp beside the charge and apply:

  ```
  A += (actual − charged) * exp2(-inflightSeconds / halfLifeSeconds)
  ```

  This makes the result **exactly identical to having charged the true value at
  dispatch**, so the accumulated tab is independent of estimator quality and
  estimation affects only in-flight ordering — which is all it should ever affect.
- On an aborted stream with zero `Usage`, **keep the estimate — do not refund.**
  Refunding lets a tenant abort-spam for free.
- **Estimator quality scales with `outputTokenWeight`.** The output estimate is the
  guessed quantity and wOut is its multiplier, so calibrating wOut upward (likely —
  see Part 2 calibration) amplifies estimate error proportionally. If wOut lands
  near 5–10, invest in the estimator (`max_tokens`, then per-tenant observed history)
  before tuning anything else.

### Two vLLM flags are hard prerequisites

Both default to **off**, both fail silently, and both go on the **vLLM container**
(`spec.template` in the LLMInferenceService), not the scheduler:

```
--enable-force-include-usage     # "including usage on every request"
--enable-prompt-tokens-details   # populates usage.prompt_tokens_details
```

**Why the first.** OpenAI streaming only emits a usage block when the client sets
`stream_options: {"include_usage": true}`. The EPP parser documents this
(`parsers/openai/openai.go:599`: *"If include_usage is not included in the request,
`data: [DONE]` is returned separately"*) and nothing in the EPP injects it. Without
the flag, any streaming client that doesn't opt in never triggers a true-up and is
charged the provisional estimate permanently — and interactive end users, the largest
group, are the most likely to be streaming.

**Why the second.** `cached_tokens` lives inside `prompt_tokens_details`. Without this
flag the field is absent, the code reads zero, and `cachedInputTokenWeight` silently
never applies — every prefix hit is charged full input price. Nothing errors; the
policy just meters a different cost model than the one in the ConfigMap.

Both conditions are detectable, so make them alarms rather than hopes:

- `..._requests_without_usage_total{fairness_id}` — with the flag set this should be
  flat zero forever, making it a **regression detector**: non-zero means a model server
  was deployed without the flag or a new backend doesn't support it. Alert on `> 0`.
- **Cached-token sanity** — if observed cached tokens are zero across all traffic for
  an extended window, assume the missing flag rather than a real 0% hit rate. llm-d
  actively routes for prefix affinity (`prefix-cache-scorer`, profile weight 3.0), so
  a genuine zero would itself be alarming. This holds even though the discount starts
  disabled at `cachedInputTokenWeight: 1.0` — the hit-rate data is the *input* to the
  decision about whether to enable it, so it must be trustworthy from day one.

Residual: forcing usage appends a final streaming chunk with an empty `choices` array.
Standard SDKs handle it, hand-rolled clients sometimes don't — smoke-test real
consumers.

## Config

```yaml
apiVersion: llm-d.ai/v1
kind: EndpointPickerConfig
featureGates: [flowControl]
plugins:
  - type: maas-weighted-fairness
    name: maas-fairness
    parameters:
      identityHeader: x-maas-subscription-id   # lowercase; set by Kuadrant AuthPolicy

      # Weights sum to 100 so each number reads as a guaranteed floor.
      # First match wins: explicit applications before the prefix catch-all.
      groups:
        - { name: app1,      weight: 20, match: { exact:  [app1-production] } }
        - { name: app2,      weight: 10, match: { exact:  [app2-batch] } }
        - { name: end-users, weight: 65, match: { prefix: [end-user-] } }
      defaultGroup: { name: unclassified, weight: 5 }

      # false = account + emit every metric, but let FCFS decide. Deploy this way first.
      enforce: false
      stateLogIntervalSeconds: 30    # flight-recorder log cadence; 0 disables

      # The averaging window. NOT the tightness dial -- see the estimator note below.
      # A half-life is not a window: 60s still remembers 25% of two minutes ago.
      # Matching a hard W-second sliding window would give H ~= W/3 (so the
      # prototype's "1 minute" is ~20s), BUT that loses to the duration floor:
      # requests take 10-30s here, and at H=20 a 30s request's provisional charge
      # decays to 35% before it even completes. 60 is near the FLOOR of the sane
      # range, not the middle. If shadow data looks noisy, move UP to 120.
      # Keep defaultRequestTTL within ~2x of this: if requests are shed before the
      # policy can rebalance toward them, the shed rate becomes the real allocator.
      halfLifeSeconds: 60
      # Additional half-lives to ACCOUNT AND REPORT but not act on. These observe the
      # ACTUAL request stream through a different smoothing window -- they are NOT a
      # counterfactual simulation of what that window would have decided. Useful for
      # reading the shape of demand (burstiness, idle gaps) and picking a window
      # without restarting. Read them during shadow mode, when the stream is unshaped
      # by any half-life. One float per tenant per entry. Empty = just halfLifeSeconds.
      # 120 is the live alternative if 60 proves noisy. 20 is kept as a CONTROL:
      # it is the number someone will re-propose ("weren't we targeting a minute?"),
      # and having data showing it is twitchy settles that once.
      observedHalfLivesSeconds: [20, 120]
      # Which resource the tab is denominated in. "tokens" matches the Kuadrant
      # ceiling and every vLLM dashboard. "vramtime" (= O*(P+O/2), KV residency)
      # is specified but NOT enabled -- see Part 3 item 9 for its trigger.
      costModel: tokens
      inputTokenWeight: 1.0
      # CALIBRATE THIS, don't inherit it. 2.0 is a convention with no physical
      # basis: prefill and decode cost ~the same FLOPs/token, and the real ratio
      # is an EFFICIENCY ratio (prefill chunk size / decode batch size), plausibly
      # 5-20x at typical batch sizes. Commercial APIs price output at 3-5x.
      # Measure it with the two-run experiment in "Calibrating outputTokenWeight"
      # below, before shadow mode. Also the cheap linear approximation of the
      # vramtime model -- see Part 3 item 9.
      outputTokenWeight: 2.0   # PLACEHOLDER until calibrated
      # START AT 1.0. See "The cached-token discount" in Part 3 for the full
      # reasoning and the decision rule for lowering it. Short version:
      #   - It sets the UNIT the 20% floor is denominated in, not the floor itself.
      #   - It only matters where groups' hit rates DIFFER; uniform rates cancel out.
      #   - It is coupled to the group weights above -- changing one invalidates
      #     the other, so they must be re-derived together.
      #   - 1.0 matches Kuadrant's ceiling, which does not discount cached tokens.
      #   - Wrong-low breaks other tenants' floors; wrong-high only under-serves
      #     the cacheable tenant. Fail in the second direction.
      # NEVER 0: that is an exemption, not a discount.
      cachedInputTokenWeight: 1.0
      # Stops a returning-idle tenant claiming retroactive credit. Exposed as a flag
      # ONLY so P4 can be run both ways and the question settled with data -- read
      # the OTHER tenants' throughput during the transition, not the newcomer's.
      # Turning it off re-couples fairness to idleness and breaks work conservation.
      newcomerClamp: true
      provisionalCharge: true
      # Fallback only. The real output estimate is min(max_tokens, per-group EWMA
      # of observed output tokens); this applies when neither is available.
      defaultEstimatedOutputTokens: 512
      # ~4 chars/token holds for Latin-script prose. CJK is ~1-2 and multimodal is
      # unrelated to byte size -- both show up as a PERSISTENT BIAS (not noise) in
      # truing_error_tokens. We deliberately never invoke the tokenizer; see above.
      estimatedBytesPerToken: 4
      agingTokensPerSecond: 0
      evictionTtlSeconds: 3600
      evictionSweepSeconds: 300

  # scheduling profile unchanged from the KServe default
  - type: single-profile-handler
  - type: queue-scorer
  - type: kv-cache-utilization-scorer
  - type: prefix-cache-scorer
  - type: max-score-picker

flowControl:
  defaultRequestTTL: 60s
  defaultPriorityBand:
    fairnessPolicyRef: maas-fairness
    orderingPolicyRef: fcfs-ordering-policy
  priorityBands:
    - priority: 0                     # all weighted tenants share ONE band
      fairnessPolicyRef: maas-fairness
      maxRequests: "5000"

schedulingProfiles:
  - name: default
    plugins:
      - { pluginRef: queue-scorer, weight: 2.0 }
      - { pluginRef: kv-cache-utilization-scorer, weight: 2.0 }
      - { pluginRef: prefix-cache-scorer, weight: 3.0 }
      - { pluginRef: max-score-picker }
```

Fairness is **intra-band only**, so every weighted tenant must share one priority. Set
both `defaultPriorityBand` and the explicit `priorityBands[0]` so stray traffic on
another priority still gets weighted within its band.

Deliberately **no `usageLimitPolicyPluginRef`.** `UsageLimitPolicy.ComputeLimit`
produces a ceiling *per band*, and the dispatch loop gates whole bands — with every
tenant in one band it can only gate all of them or none, never "throttle app2 not
app1." It becomes relevant only if you later add a sheddable free tier at a negative
priority.

Keep `defaultRequestTTL` within ~2× of `halfLifeSeconds`. If the TTL is much shorter,
requests are shed before the policy can rebalance toward them and the *shed rate*
becomes the real allocator.

Factory validation: all weights > 0, `halfLifeSeconds >= 0`, token weights >= 0. The
framework hands you a `DisallowUnknownFields` decoder, so a typo in a key is a startup
failure rather than a silent default — keep that.

## Repository layout

**Decided:** one new **private** repo at `github.com/Dorsivan/maas-fair-share`, Go
module at the root, Python prototype preserved inside it.

**`~/repos/wfq` is not a git repository** — it's an untracked directory holding the
Python prototype, which is why a repo gets created rather than added to. One repo, not
two, with the Go module at the root and the prototype frozen inside it.

*Why one:* same problem, same reviewers, and the prototype is the design's
**provenance** — the artifact showing why the saturation gate, `max_tokens_per_window`
and the 429 path were deleted. That's wanted within reach for the support
conversation and design review, and it is precisely what gets lost sitting untracked
on one laptop. It goes in **frozen, as reference, not kept in sync**: the Go plugin is
not a port. The Python service is an ext_proc sidecar doing its own admission control;
this is a fairness policy inside the EPP where queueing and work conservation are
structural. Most of `wfq.py` is deleted by the new design, not translated.

*Why Go at the root:* the import path is then just the repo URL with no subdirectory
suffix, `go build ./cmd/epp` works from the root, the Dockerfile context is the whole
repo, and the upstreaming items below are far easier to carve out of a clean
standalone module. Nesting it (`wfq/epp/`) is legal but yields
`github.com/<org>/wfq/epp` and implies the Python service is still primary.

New module importing `github.com/llm-d/llm-d-router` pinned to a **release tag**
(`v0.11.0`), never `main`. Match upstream's `go` directive (`go 1.26.6`); importing
`cmd/epp/runner` pulls essentially the whole EPP graph (~400 modules). No `replace`
directives.

```
go.mod                               # module github.com/<org>/<name>  (root)
cmd/epp/main.go                      # Register(...) then runner.NewRunner().Run(ctx)
pkg/fairness/weightedlas/
  plugin.go      # FairnessPolicy + RequestHeaderProcessor + PreRequest
                 #   + ResponseBodyProcessor + StateDumper, factory, eviction sweeper
  state.go       # tenantState (decayed service, backlogged edge, provisional)
                 #   + bandState (virtual time)
  weights.go     # group matching (exact then prefix), weight lookup, validation
  cost.go        # token cost model + provisional estimate
  metrics.go
Dockerfile.epp                       # derived from upstream
deploy/{epp-config.yaml,llmisvc.yaml,podmonitor.yaml,rbac.yaml}
docs/
prototype/                           # FROZEN. README: what it was, why it was replaced
  wfq_service/ mock_llm/ envoy.yaml docker-compose.yaml Dockerfile.* test_wfq.py
```

### Bootstrap steps

1. `gh repo create Dorsivan/maas-fair-share --private` and clone to
   `~/repos/maas-fair-share`.
2. **`.gitignore` before the first commit** — `__pycache__/`, `*.pyc`, and
   `wfq_service/generated/` (compiled protobufs, regenerated by `compile_protos.sh`;
   don't commit them). Also `results/` if any load-test output lands here.
3. **Copy** `~/repos/wfq/*` into `prototype/` — copy, don't move, until the new repo
   is pushed and verified. The source is untracked and unbacked; there is no undo.
4. `prototype/README.md` — what it was, what it proved, and why the architecture
   changed (ext_proc sidecar with its own admission control → fairness policy inside
   the EPP where queueing and work conservation are structural). State plainly that it
   is **frozen reference, not maintained**.
5. Root `README.md` pointing at this plan, then `go mod init` and the skeleton above.

The repo name deliberately drops `wfq`: the algorithm is weighted
**least-attained-service**, not classic WFQ, and `wfq` named neither MaaS nor llm-d.

```go
fwkplugin.Register(weightedlas.PluginType, fwkplugin.StabilityBeta, weightedlas.Factory)
if err := runner.NewRunner().WithExecutableName("maas-epp").Run(ctx); err != nil { return 1 }
```

**Register as `StabilityBeta`, not Alpha.** `runner.go:471` calls
`ValidatePluginStability(handle, opts.AllowExperimentalPlugins)`, and the KServe preset
does not pass `--allow-experimental-plugins`, so an Alpha plugin fails at startup.

Declaring the type in the top-level `plugins:` list is enough to wire `RequestHeader`,
`PreRequest` and `ResponseBody` — `(*requestcontrol.Config).AddPlugins` type-asserts
every instantiated plugin against each extension point. Register collectors from the
factory via `handle.Metrics().MustRegister`, so `WithCustomCollectors` isn't needed.

Dockerfile: copy upstream's two-stage build, but `go build ./cmd/epp` (package, not
file), drop the `apix/ internal/ version/` copies (upstream module dirs; `version`
still resolves as a dependency so the `-X` ldflags paths keep working), and keep
`USER 65532:65532` — KServe sets `runAsNonRoot` and `readOnlyRootFilesystem`, and this
satisfies `restricted-v2` with no SCC exception.

## Deployment

```yaml
spec:
  router:
    scheduler:
      replicas: 1                  # all state is in-process; scaling out shards it
      config:
        ref: { name: maas-epp-config, key: epp }
      template:
        containers:
          - name: main             # must be "main" for the strategic merge to hit
            image: quay.io/<org>/maas-epp:v0.11.0-1
```

Override **only** `image` (and `resources` if needed). KServe templates `--pool-name`,
ports, TLS flags and appends `--config-text`; overriding `command` means re-templating
all of that. Do not patch the Deployment directly — the controller owns
`<name>-kserve-router-scheduler` and reverts manual edits.

No PDB: with `replicas: 1`, `maxUnavailable: 0` would block node drains.

## Verification

### Unit tests

Use `pkg/epp/framework/interface/flowcontrol/mocks` — a real non-test package, so it
imports out of tree. Inject a clock (`func() time.Time`) rather than sleeping.

1. **Proportionality** — weights 2:1, both permanently backlogged, 10k picks → 2:1 ±2%.
2. **Unequal request sizes** — weights 1:1, A charges 100/req and B charges 1000;
   *token* ratio → 1:1 and *request* ratio → 10:1. This distinguishes token-LAS from
   round-robin.
3. **Work conservation** — weights 2:1 with B idle → A gets 100%, not 66%.
4. **Idle clamp** — A backlogged to `A=50000`, B absent for 10 half-lives then returns;
   B's consecutive-win streak ≤ 1+ε. Then run the same scenario with
   `newcomerClamp: false` and assert it *fails*, so the test proves the mechanism
   rather than the absence of load. Assert on **A's** starvation duration too — that
   is where the cost of no-clamp actually lands.
5. **Decay** — charge 1000, advance one half-life, assert ≈500.
6. **Grouping** — `end-user-a` and `end-user-b` resolve to the *same* `FairnessID`;
   unmatched → `unclassified`; exact beats prefix.
7. **Spoof resistance** — request carrying `x-llm-d-inference-fairness-id: app1` plus a
   low-weight subscription header resolves to the low-weight group.
8. **Provisional true-up** — `MaxOutputTokens=1000` then `CompletionTokens=100`; net
   service equals actual, and mid-flight service reflects the estimate.
8b. **Estimator-independence** — the decisive test for the decayed correction. Run the
   same request twice with wildly different estimates (say 10× over and 10× under),
   advancing the clock ~0.5 half-lives in flight each time. Final `A` must be
   **identical** in both runs and equal to charging the true value at dispatch. This
   fails loudly if the correction is added undecayed.
9. **Abort** — `EndOfStream` with zero `Usage`: estimate retained, not refunded.
10. **Non-final chunks** (`EndOfStream=false`) must not move service.
11. **Shadow mode** — `enforce: false` emits identical metrics but returns the FCFS pick.
12. **Determinism** — 100 runs, identical pick sequence.
13. **Factory validation** — negative weight, unknown parameter key → error.

### Conformance (copied, with attribution)

The four upstream cases are exactly the ones a new policy gets wrong, all returning
`(nil, nil)` with no error: nil accessor; empty band; a band whose single queue reports
`Len()==0` despite being visited; multiple empty queues. Add two: `PolicyState()` of
the wrong concrete type → error not panic, and `Pick` from 50 goroutines under `-race`.

### Calibrating `outputTokenWeight` (do this FIRST, before shadow mode)

Two saturating `guidellm` runs against an otherwise idle pool, varying only the data
shape — `run-concurrent.sh` already parameterizes it:

```
A (prefill-dominated):  --data kind=synthetic_text,prompt_tokens=4096,output_tokens=1
B (decode-dominated):   --data kind=synthetic_text,prompt_tokens=64,output_tokens=1024

outputTokenWeight ≈ (prefill tokens/sec in A) / (decode tokens/sec in B)
```

That ratio *is* the relative cost of the two token types on this hardware, model and
batch size. Twenty minutes of work that replaces the most arbitrary number in the
config with a measurement. Re-run it whenever the model or GPU type changes — the
ratio is hardware-specific, so it does not survive a pool migration.

### Load test

Two `guidellm` runs off `~/repos/guidellm-example/scripts/run-concurrent.sh`, one per
tenant with its own subscription-bound `RHOAI_TOKEN`. The script already parameterizes
`STREAMS` and `DURATION`; it needs one addition — passing `x-maas-subscription-id` via
guidellm's `--request-headers`. Give both tenants **identical and individually
pool-saturating** load, or the result is confounded by work conservation.

| Phase | Load | Expected |
|---|---|---|
| P0 | A alone, under capacity | baseline TTFT |
| P1 | A+B, total under capacity | **both unthrottled**, within 5% of P0 — the "no limits when idle" requirement, and the phase most likely to expose a bad aging term |
| P2 | A+B both saturating | **token ratio → configured ratio** |
| P3 | A saturating, B idle | A gets ~100%, not its weighted fraction |
| P4 | P3 for 10 min, then B returns | B's 10s share never exceeds ~0.85; ratio restored within 3 min. **Run twice, `newcomerClamp` on and off**, and measure **A's** throughput through the transition — the cost of no-clamp lands on the incumbent, not the newcomer |
| P5 | A+B+C (unlisted) | → 20:10:5 |

**Measure from EPP metrics, not guidellm** — client-side numbers fold in queueing and
shedding. The `fairness_id` label is already on the core series:

```promql
sum by (fairness_id) (rate(llm_d_epp_request_output_tokens_sum[2m]))   # the share
llm_d_epp_flow_control_pool_saturation{stage="effective"}              # confirm P2 saturates
sum by (fairness_id) (llm_d_epp_flow_control_queue_size)               # confirm a backlog exists
rate(llm_d_epp_flow_control_request_queue_duration_seconds_count[2m])  # if shedding, TTL rations, not us
```

Two controls: run P2 with `fairnessPolicyRef: globalstrict` (expect ~1:1 — proves the
plugin does something), and with `provisionalCharge: false` (quantifies what the
dispatch-time charge bought). Automate as `make loadtest` or it gets run once and rots.

## Production observability

### Metrics

Only what isn't derivable from the existing `fairness_id`-labelled core series, all
labels through `BoundFairnessID`, subsystem `llm_d_epp`:

| Metric | Type | Answers |
|---|---|---|
| `..._contended_service_tokens_total{fairness_id}` | Counter | the SLI numerator |
| `..._contended_seconds_total{fairness_id}` | Counter | the SLI denominator — was this group even competing? |
| `..._normalized_service{fairness_id}` | Gauge | `A_i/w_i`. Converges across backlogged groups when healthy; a persistent outlier is starved or monopolizing |
| `..._normalized_service_observed{fairness_id,half_life}` | Gauge | the same value at each `observedHalfLivesSeconds` entry — pick the window from data instead of by restarting |
| `..._configured_weight{fairness_id}` | Gauge | echoes the ConfigMap so dashboards compute expected-vs-observed without hand-copying weights |
| `..._dispatch_total{fairness_id}` | Counter | dispatch-opportunity share; divergence from token share diagnoses the ordering-vs-floor caveat |
| `..._newcomer_clamps_total{fairness_id}` | Counter | high steady rate ⇒ `halfLifeSeconds` too short |
| `..._unmatched_subscriptions_total` | Counter | a typo silently falls into `unclassified` otherwise |
| `..._truing_error_tokens{fairness_id}` | Histogram | `actual − estimate`. Symmetric noise is fine and self-correcting; a persistent per-group **bias** is the signal — it means `bytes/4` is wrong for that group's content (CJK runs ~1–2 bytes/token and under-charges 2–4×; multimodal token counts have no relation to JSON size at all). That, and only that, justifies a per-group `estimatedBytesPerToken` override or finally reaching for the tokenizer |
| `..._requests_without_usage_total{fairness_id}` | Counter | **regression detector.** With `--enable-force-include-usage` set this is flat zero; non-zero means a model server shipped without the flag and that tenant's tab is estimate, not measurement. Alert on `> 0` |
| `..._prompt_tokens_cached_ratio{fairness_id}` | Gauge | **the headline shadow-mode reading.** Per-group cache hit rate — decides whether `cachedInputTokenWeight` is a real lever or a no-op, and in whose favour. Also guards the second vLLM flag: a flat zero here means `--enable-prompt-tokens-details` is missing, not that the cache is cold |
| `..._enforcing` | Gauge 0/1 | enforcing, or shadow mode |

Do **not** label `unmatched_subscriptions_total` with the raw subscription string —
that is attacker-controlled cardinality. Count it; put the values in the rate-limited
log line and the state dump.

### Closing the scrape gap

`config/llmisvcconfig/config-llm-scheduler.yaml` exposes `containerPort: 9090` named
`metrics` but creates **no ServiceMonitor or PodMonitor**, and `--metrics-endpoint-auth`
defaults to `true` (TokenReview/SubjectAccessReview). Required:

1. Enable user-workload monitoring (`cluster-monitoring-config`, `enableUserWorkload: true`).
2. A `PodMonitor` in the serving namespace selecting the scheduler pod, port `metrics`,
   with `bearerTokenSecret` pointing at a ServiceAccount token.
3. A `ClusterRole` with `nonResourceURLs: ["/metrics"], verbs: ["get"]` bound to that SA.
4. Verify with a `/debug/plugins/state` curl and a PromQL query for
   `..._configured_weight` *before* trusting any dashboard.

Resist `--metrics-endpoint-auth=false` — it makes per-tenant token consumption readable
by anything that can reach the pod IP.

### Live state via `StateDumper`

```json
{"plugins": {"maas-fairness": {"state": {
  "enforcing": true, "halfLifeSeconds": 60, "bandVirtualTime": {"0": 48213.4},
  "groups": [
    {"name": "app1", "weight": 20, "attainedService": 964268, "normalizedService": 48213.4,
     "queueDepth": 37, "inFlight": 12, "backlogged": true},
    {"name": "end-users", "weight": 65, "attainedService": 3133871, "normalizedService": 48213.4,
     "queueDepth": 9, "inFlight": 3, "backlogged": true}],
  "recentUnmatchedSubscriptions": ["enduser-foo"], "truncated": false
}}}}
```

Equal `normalizedService` across backlogged groups is the whole policy working, visible
at a glance. `docs/plugin_debug.md` requires dumps to exclude credentials and payloads
and stay bounded — cap the group list, include `truncated`, cap the unmatched list.

### Correlation

Every request-scoped log line in this package carries two fields, resolved once in
`RequestHeader` and reused by every later hook (`PreRequest`, `ResponseBody`,
`ResponseHeader`) rather than re-derived — see `pkg/fairness/weightedlas/correlation.go`:

- **`requestID`** — `x-request-id` from the inbound request. The llm-d-router ext_proc
  server already extracts this header and backfills a generated uuid if the client sent
  none (`pkg/epp/handlers/server.go`); this plugin re-derives it from the header
  independently rather than depending on that upstream detail — falling back to the
  upstream-populated `InferenceRequest.RequestID`, then to its own generated id, in that
  order. Never empty: a request-scoped line with no key is a line nobody can find.
- **`traceId`** — the trace-id field of an inbound `traceparent` header, included only
  when present. Never generated — a fabricated trace id would not correlate with
  anything, and this POC runs no collector to send spans to anyway (see "Explicitly out
  of scope" in UNI-53; a malformed or absent header simply omits the field).

### Logs

`Pick` runs on a 1ms ticker, so per-decision logging is out. Three tiers; `requestID`
(and `traceId`, when present) is attached to every one of them that is request-scoped,
`enforcing` is attached to every tier, request-scoped or not, and `band` is attached to
the request-scoped tiers only — the flight recorder carries no `band` (see below). Full
field list, stable-vs-debug-only split, and the LogQL query pack:
`docs/log-field-contract.md` and `docs/logql-queries.md` (UNI-48 / D9).

- **Flight recorder (INFO, every `stateLogIntervalSeconds`)** — **one line per
  configured group**, sharing a `tick` id so the lines of one recording pass can be
  reassembled, emitted **only while contended**. Silent on an idle cluster; works with
  only Loki. Not request-scoped, so no single `requestID` applies, and no `band` either
  (`groupState` is not itself scoped to a priority band — see
  `docs/log-field-contract.md` §3.1). **Changed in UNI-48 (D9)**: previously one line
  carried the whole table as a nested `groups[]` array, which does not unroll into a
  time series in Loki or Elasticsearch.
- **Events, rate-limited** — clamp fired; unmatched subscription (log the value, first
  N then sampled, now carrying the `requestID`/`traceId` of the request whose first
  sighting triggered the line, plus `band` and `enforcing` as of D9); active flows on
  more than one priority band. The no-usage-block warning in `ResponseBody` (V(1)) is
  the same tier and carries the same fields.
- **V(4) per-request** — group resolved, estimate charged, true-up delta, `band`,
  `enforcing`, a `recorderTick` linking to the nearest flight-recorder tick (D9), and the
  `requestID`/`traceId` identifying which request the pick belongs to. **Implemented**
  (UNI-47) in `ResponseBody`, the one point in the request lifecycle where a group, an
  estimate and a true-up delta all exist together — not in `Pick`, which this tier never
  touches (see "V(4) is off Pick's hot path" below). **Cannot be enabled on the
  KServe-managed GPU scheduler today** — see `docs/runbook.md` "On the KServe-managed
  scheduler" and `docs/log-field-contract.md` §3.3, §5.

### V(4) is off Pick's hot path

The per-request tier is gated by three independent config/runtime switches, all of which
default to off:

- `requestTierV4SampleEvery` (plugin config) — 0 disables the tier outright; N emits one
  line per N eligible settlements.
- `requestTierV4TimeBoxSeconds` (plugin config) — required once sampling is on. The
  window opens on this plugin's first eligible check (in practice, pod start) and the
  tier goes silent once it elapses, even if the two other switches are still open — so
  raising verbosity for a debugging session cannot be left on by accident.
- The EPP process's own `-v` flag — the tier additionally requires `log.V(4).Enabled()`
  from the ambient logger.

This plugin's `parameters` block is decoded once at construction (`Factory`) with no
watch or reload, and `-v` is parsed once at process start with no exposed dynamic
endpoint (`pkg/common/observability/logging.Options` in llm-d-router v0.11.0) — so
**neither switch can be changed without a redeploy**. Per the ticket, the fallback for
"no live-reload path" is to gate on the existing verbosity flag plus the sample rate,
which is exactly what the three switches above do.

`Pick` runs on a ~1ms ticker and is unconditionally out of scope for unsampled
per-request logging (see "Logs" above). This tier's code reads none of `Pick`'s state and
adds nothing to its call path: the only edits this ticket makes to `plugin.go` are the
`Plugin` struct, `ResponseBody`, and two new unexported methods declared after `dump()`.
`Pick` itself is byte-for-byte unmodified, so the cost of the disabled (and the enabled)
V(4) path on `Pick` is exactly zero, not merely small — see `BenchmarkPick` in
`pkg/fairness/weightedlas/pick_bench_test.go` for the regression guard and
UNI-47's closing comment for the measured numbers.

### Per-request attribution

**Implemented** (UNI-53): `x-request-id`, `x-maas-fairness-group` and
`x-maas-fairness-queue-ms` are set on the response in `Plugin.ResponseHeader`
(`pkg/fairness/weightedlas/plugin.go`), a `requestcontrol.ResponseHeaderProcessor`. A
tenant reads its own classification from a response header at zero log volume and with
no cluster access.

The mechanism this doc previously flagged **unverified** is confirmed working on
llm-d-router v0.11.0: `response.Headers`, as seen inside `ResponseHeader`, is the same
map as `reqCtx.Response.Headers`, which the director writes unconditionally into the
ext_proc `HeaderMutation` for any key not matched by `request.IsSystemOwnedHeader`
(`pkg/epp/util/request/headers.go`) — none of the three keys below are on that list.
The session-affinity plugin shipped with llm-d-router
(`pkg/epp/framework/plugins/scheduling/util/sessionaffinity/header.go`) already relies
on the identical path to set its own response header, so this is a supported extension
point, not an undocumented side channel.

| Header | Value | Meaning |
|---|---|---|
| `x-request-id` | the resolved correlation id (see "Correlation" above) | ties the response to the matching EPP log line for this request |
| `x-maas-fairness-group` | `request.FairnessID` after classification | the group this request was billed against |
| `x-maas-fairness-queue-ms` | elapsed time between `RequestHeader` and `PreRequest`, in ms | an **approximation** of time spent under flow-control admission — measured end to end across this plugin's own hooks, not read from flow-control's internal clock. Omitted if the request never reached dispatch (e.g. rejected at admission) |

Suppressible: `emitAttributionHeaders: false` in the plugin's `parameters` block turns
all three off in one switch. Default is `true`.

### Alerts

- **Not converging** — spread of `normalized_service` across groups with increasing
  `contended_seconds` exceeds a threshold for 10 min while saturation ≥ 1.
- **Classification broken** — `unclassified` share > 5%, or
  `unmatched_subscriptions_total` increasing at all (should be flat zero).
- **Band split** — more than one priority band has active flows (objective header leak).
- **Shedding is the real allocator** — sustained evictions on the queue-duration metric.
- **Accounting leak** — provisional tokens nonzero while traffic is zero.

---

# Part 3 — What to consider before committing

Things that are your call, not the implementation's:

1. **Red Hat support boundary.** A custom EPP image takes that component outside RHOAI
   support. Confirm with the account team. This is the biggest non-technical risk.
2. **Single replica is a SPOF** on the routing path. On restart all tabs reset and the
   first 2–3 minutes are roughly FIFO. Don't build persistence — the warm-up is bounded
   by the half-life, which is the horizon the guarantee is defined over anyway. The
   worse exposure is that `failureMode: FailOpen` means requests *during* the restart
   bypass the EPP entirely: seconds of no fairness, not minutes of cold fairness.
3. **Every weight change is an EPP restart** (a few seconds of unfair routing). Fine
   for occasional tuning, not for anything automated.
4. **Gateway header stripping is a hard prerequisite**, and it lives in Kuadrant/Envoy
   config, not in this plugin. It silently fails open if someone adds a route later.
   Put it in the runbook with a conformance check.
5. **The SLA wording** (Part 1): relative share under contention, not absolute
   tokens/sec. Get agreement on this before anyone writes it into a contract.
6. **Weights sum to 100** as a convention, so each number reads as a guaranteed floor.
7. **Half-life tuning — and how to make it cheap.** 60s to start. Short (10–30s)
   adapts fast but the window is shorter than many generations, so long-output tenants
   get a free ride. Long (300s+) tracks the ratio tightly but penalizes a tenant
   returning from legitimate idleness. Never 0 (cumulative since process start — this
   morning's heavy tenant starves all afternoon).

   **A half-life is not a window.** At 60s the tab is half gone at one minute, a
   quarter gone at two, negligible only after ~5 half-lives. Reproducing a hard
   W-second sliding window would mean matching mean age — uniform averages W/2,
   exponential averages H/ln2 ≈ 1.44H, giving **H ≈ W/3**, so the prototype's "1
   minute" is ~20s.

   **That rule loses to the duration floor, and it matters here.** Requests take
   10–30s. The provisional charge is placed at dispatch and decays for the whole
   generation, so what remains on the tab at completion is:

   | Half-life | 10s request | 30s request |
   |---|---|---|
   | 20s | 71% | **35%** |
   | 60s | 89% | 71% |
   | 120s | 94% | 84% |

   At H=20 a long generation's hold melts before it finishes. The general principle:
   **H must be large enough that it doesn't matter whether cost is attributed to
   request start or request completion** — the cost is really incurred continuously,
   and neither endpoint is right. H ≫ D makes the choice irrelevant; H ≈ D makes the
   fairness numbers depend on an arbitrary modeling decision. 60 gives 2× the worst
   case (marginal), 120 gives 4× (comfortable). **Treat 60 as the floor and move up,
   never down.**

   **Tightness is a different dial.** There is real tension between the stated "about
   a minute" and an effective averaging window of a few minutes — but what's actually
   wanted is *accuracy* (app1 really gets 20%), not a short window. Shortening the
   half-life buys twitchiness, and at these durations it buys inaccuracy. The dial
   that buys accuracy is the **in-flight estimator**: a better output-token guess
   (reading `max_tokens`, or per-tenant observed history) tightens enforcement with
   none of the noise cost. Spend effort there if 60s feels loose.

   Changing it is one line in the ConfigMap: the KServe controller watches ConfigMaps
   (`llmisvc/controller.go:453`), re-resolves `scheduler.config.ref` into the
   `--config-text` arg, and rolls the pod automatically. No rebuild, no manual bounce.
   **Confirm this empirically once** — edit the ConfigMap, watch the pod roll — rather
   than trusting the code read.

   But each change restarts the EPP, which resets all tabs (2–3 min warm-up) and briefly
   sends traffic past the EPP under `FailOpen`. Cheap once, expensive to sweep. So
   **don't sweep by restarting** — use `observedHalfLivesSeconds` to report several
   windows simultaneously while only one drives decisions, then change the number once
   from data.

   **Be precise about what that buys.** The observed windows smooth the *actual*
   request stream; they do not simulate what decisions a different window would have
   made, since that would have changed the stream itself. What they legitimately
   measure is the shape of demand — burstiness, idle-gap length, how much a tenant's
   tab swings at each timescale. That is the question "is 60s right?" actually reduces
   to. Read them during shadow mode, where FCFS leaves the stream unshaped by any
   half-life; once enforcing, the active window shapes what the others observe.

   A true counterfactual ("what fairness would 15s have produced") needs a replay
   harness: log the request stream, re-run the policy offline per setting. Only build
   it if the observational read leaves a genuine tie.

   Keep it a real knob: inject the clock (`func() time.Time`) so decay tests advance
   time instantly instead of sleeping, and let no other parameter derive from the
   half-life — the moment something reads `halfLife * 5`, it stops being tunable.
> **The governing principle for items 8–9, and for `outputTokenWeight`.**
> Every cost-model parameter is a **differential lever**: it re-prices groups against
> each other exactly in proportion to how much their traffic *shapes* differ. If all
> groups send the same shape, the parameter is a no-op no matter how wrong it is; if
> shapes differ sharply, it can dominate the configured weights.
>
> Two consequences. **(a)** None of these can be set from first principles — they are
> empirical, and the evidence is the same evidence in all three cases. **(b)** The
> shadow period's real deliverable is therefore *one* table, not three measurements:
> a **per-group traffic shape profile** — prompt tokens, cached fraction, output
> tokens, with distributions rather than means. From that single table every cost
> parameter can be set *and* any alternative cost model replayed offline. The
> convergence graphs are secondary.

8. **The cached-token discount (`cachedInputTokenWeight`) — start at 1.0.**

   `cached_tokens` is **not** the KV-occupancy measurement we abandoned. It counts
   prompt tokens the GPU *skipped recomputing* because an earlier request left their
   blocks resident. Work skipped, not memory held — and unlike occupancy it is exactly
   attributable, because it arrives in the response body.

   **What the number does.** It sets the *unit* your 20% floor is denominated in, not
   the floor itself. A 10k-prompt / 9k-cached / 500-output request charges 11,000 at
   1.0 and 2,900 at 0.1 — nearly 4x. Lowering it lets a cacheable tenant push ~4x the
   raw tokens for the same share of the tab.

   **It only matters where hit rates differ.** Uniform hit rates shrink every tab by
   the same factor and the ratios barely move. So the first thing to read in shadow
   mode is per-group `cached_tokens / prompt_tokens`, not the convergence graphs.

   **And they will differ, in a direction that matters.** Multi-turn chat is the
   extreme case: every turn re-sends the conversation, so turn N is ~(N−1)/N cached —
   95% by turn 20 — and total prompt tokens grow *quadratically* with turn count. A
   20-turn chat bills ~10x its actual new content. That is the **end-user** workload.
   Apps with a fixed system prompt are cacheable too, but at a bounded ratio. So this
   parameter systematically re-prices one group against the others.

   **Therefore it is coupled to the group weights.** 20/10/65 were chosen with an
   intuition about volume; changing the cost model by 4x for one group invalidates
   that intuition. Fix the cost model first, measure, then set weights — never tune
   this afterwards in isolation.

   **Why 1.0 to start, despite the compute argument.** The failure is asymmetric. Too
   low and a high-cache tenant escapes accounting ~10x while everyone else's floor
   silently breaks. Too high and that tenant is merely under-served — conservative and
   visible. 1.0 also matches Kuadrant's ceiling, which counts raw tokens and does not
   discount; diverging means a tenant can be "well inside its fair share" and "rate
   limited" at once.

   **Decision rule for lowering it**, in order: (a) confirm the pool is compute-bound
   at saturation (see item 9 — `vllm:gpu_cache_usage_perc` with headroom); if KV is
   pegged with a non-empty waiting queue you are VRAM-limited and the discount isn't
   clearly justified; (b) confirm hit rates actually differ between groups; (c) replay the
   alternative cost model offline from logged prompt/cached/completion counts — unlike
   the half-life this counterfactual *is* computable, because the cost model doesn't
   change which requests arrive; (d) move to ~0.1–0.2 **and re-derive the group weights
   in the same change**. Don't pick a value in between — 1.0 means "tokens are tokens"
   and 0.1 means "we price compute"; 0.5 means nothing and can't be defended.

   **Never 0.** That's an exemption, not a discount: unlimited cached-prefix traffic at
   zero tab cost. Prefill slots are real even when the compute is skipped.

   **The memory-bound argument, stated correctly.** Not "cached blocks occupy the same
   memory as fresh ones" — prefix caching *shares* blocks, so 100 concurrent requests
   on a common 9k prefix hold one copy, which is a memory *win*. The real concern is
   narrower: a tenant maintaining a **large working set of distinct prefixes** pins a
   lot of KV memory to sustain its hit rate and evicts other tenants' blocks to do it.
   The discount rewards precisely that at a tenth of the price.

   **And under VRAM binding the answer gets *more* ambiguous, not less.** Sharing
   reduces pressure (argues for the discount); a large distinct-prefix working set
   increases it (argues against). The difference is whether a group's hits come from
   **concurrent sharing** or **long-lived retention** — and that is not distinguishable
   from the response body. A real limit of the signal, not a gap more analysis closes.
   One more reason to leave this at 1.0 absent a positive reason to move.

   Secondary: `prefix-cache-scorer` carries the highest profile weight (3.0), so the
   router actively manufactures these hits. Hit rates will be high by construction, and
   a discount feeds back — cheaper tab ⇒ more dispatches ⇒ better locality ⇒ cheaper
   still. Bounded (hit rate caps at 100%, output still costs 2.0) but real.

9. **Which resource actually binds — and how good a proxy tokens are for it.**

   We dropped per-tenant KV occupancy early because it isn't *attributable*, not
   because it's the wrong resource. If VRAM is what binds, tokens are a **proxy** for
   the scarce thing and the proxy's error is worth knowing.

   **"Compute vs memory" is the wrong dichotomy — there are three resources.**
   KV capacity (VRAM) caps concurrent sequences; memory *bandwidth* caps decode speed
   (every step reads all weights plus the batch's KV); FLOPs cap prefill. Decode is
   bandwidth-bound, so the GPU is routinely saturated in bandwidth while showing
   modest FLOPs utilisation — people read that as "we have compute headroom," which is
   true and irrelevant.

   Diagnose from vLLM's own metrics, not from GPU util:
   - `vllm:gpu_cache_usage_perc` ≈ 100% + `vllm:num_requests_waiting` > 0 +
     `vllm:num_requests_running` plateaued ⇒ **VRAM-limited**.
   - cache usage with headroom + waiting > 0 ⇒ bandwidth/compute limited; more VRAM
     buys nothing.

   Long-context and multi-turn traffic lands in the first bucket most of the time.

   **Where the token proxy diverges.** A tenant's real VRAM consumption is token-
   *seconds* of residency. For one request:

   ```
   VRAM-time ≈ O × (P + O/2)     # QUADRATIC in output length
   our cost  = P + 2×O           # LINEAR in output length
   ```

   Output tokens track residency well — each one both does work and extends residency
   by a step — which is why the proxy holds at all. It breaks for long generations.
   Three tenants each producing 100,000 output tokens, P=500:

   | Shape | VRAM-time | Charged |
   |---|---|---|
   | 1,000 × 100 out | 55M | same |
   | 100 × 1,000 out | 100M (1.8×) | same |
   | 10 × 10,000 out | 550M (**10×**) | same |

   So **long-generation tenants under-pay in VRAM terms**. Like the cached-token
   issue this is *differential*: harmless if groups generate similar-length outputs,
   significant across an order-of-magnitude difference.

   **The fix is in reach and should be deferred.** `O × (P + O/2)` needs only prompt
   and completion counts — data we already have, no vLLM internals. So it's a third
   selectable cost model, not a design problem:

   ```
   tokens:   wIn×(P−C) + wCached×C + wOut×O    # default; matches the Kuadrant ceiling
   vramtime: O × (P + O/2)                      # token-steps of KV residency
   ```

   Don't enable it now: it inflates the tab by ~O, which is harmless for fairness
   (scale-free) but makes every number unrecognisable against Kuadrant and the vLLM
   dashboards. Ship it as a documented option with a measured trigger — **groups'
   median output lengths differ by >5× AND the pool is confirmed VRAM-limited.**
   Add `..._output_tokens` percentiles per group to the shadow-mode reading list so
   that trigger is observable.

   **Reach for `outputTokenWeight` first.** Output tokens are what drive KV residency,
   so raising wOut is the cheap *linear* approximation of `vramtime` — it recovers
   most of the under-charging, keeps units recognisable, and stays a ConfigMap edit
   rather than a rebuild. Correct order: calibrate wOut empirically (Part 2), check
   whether a residual still matters, only then consider the quadratic model.
   `vramtime` is for the extreme tail, not the first response.

10. **Two vLLM server flags are a hard prerequisite, and they live outside this plugin.**
   `--enable-force-include-usage` and `--enable-prompt-tokens-details`, both default
   off, both set on the model-server container rather than the scheduler. Without the
   first, streaming requests never true up; without the second, the prefix-cache
   discount silently never applies. Neither fails loudly — same class of risk as the
   gateway header stripping in item 4, and it belongs in the same runbook check. Any
   new model server added to the pool must carry both.
11. **Version pinning.** Flow-control interfaces are Alpha/Beta on a v0.x module. Budget
   a quarterly re-pin: bump `go.mod` and the Dockerfile builder together, re-read the
   `plugins.go` diff, rerun conformance + load tests. Add a Dependabot rule scoped to
   `llm-d-router`. See `docs/version-pinning.md` for the authoritative process; the
   quarterly cadence proposed above has been superseded by a monthly check.
12. **Disconnected clusters** need the image mirrored with a matching IDMS/ICSP entry.
13. **Metric label cardinality.** The 1000-ID cap is far above your tenant count, but
    values are admitted first-come and never evicted. Ensure anonymous traffic collapses
    to one default group and no per-session header can mint unique IDs.

## Worth doing upstream (small, unblocks deleting local copies)

- Export `runPickConformanceTests` into a non-test `fairness/conformance` package.
- Add a `RegisterStrategy` seam to `program-aware` so weighted LAS can be a strategy
  rather than a fork-by-copy.
- Add `metricsutil.PinFairnessID(string)` so configured tenant IDs can't be spilled
  from the label cap.
