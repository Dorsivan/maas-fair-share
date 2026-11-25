# Weighted fair-share across MaaS Subscriptions in the llm-d Router

> **Part 1** explains what we're building and why, assuming no Go or llm-d knowledge.
> **Part 2** is the implementation detail for whoever writes the code.
> **Part 3** is what you need to decide or accept.

> **If you have never seen this project, start at [`AIRGAP-HANDOFF.md`](../AIRGAP-HANDOFF.md)
> instead of here.** That document is the current-state entry point; this one is the design
> **history** — real decisions, in the order they were made, including ones since
> superseded. It is long (1,900+ lines) and reads front-to-back as a narrative, not as a
> reference you can dip into at a random heading.
>
> **The one thing worth knowing before you read linearly:** everything below from here
> through "The algorithm: a running tab" describes dispatch order as decided by an
> **EPP-held queue ranked by a weighted least-attained-service tab**. That stopped being
> true once [UNI-293](#uni-293-sfq-priority-stamp) shipped. UNI-288 (search this file)
> found the EPP only ever held 6-8% of in-flight requests — vLLM's own FIFO
> queue held the other ~90-94% and decided the real order, which is why the tab-only
> mechanism was only partially effective. **UNI-293 ("SFQ priority stamp") is what
> actually decides dispatch order today**: the plugin still runs the tab for accounting
> and metrics, but ranks and dispatches by a start-time fair-queueing tag stamped into
> vLLM's own `priority` field, so vLLM's queue (where the requests actually are) sorts by
> the same number the EPP would have used. [UNI-302](#uni-302-the-stamp-explains-itself)
> added a decision log and two metrics for reading that stamp's effect live. Everything
> about *why* the earlier, tab-only version was built the way it was is still accurate
> and still the reason the tab exists at all (it is now the thing the stamp is derived
> from) — it only stops being the *ordering* mechanism at UNI-293.
>
> The "## Config" section (Part 2) is kept current and does include the SFQ fields —
> read it, not the narrative prose, for what to actually put in a ConfigMap.

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

**A measurement-design caveat on the evidence itself (UNI-225).** Most of the benchmark
suite's scored scenarios size each tenant's offered worker count proportionally to its
configured weight. When offered workers already track weights 1:1, a PASS on that row
cannot distinguish "the split follows the weights" from "the split follows the workers" —
both predict the same number. Restricting the check to rows where the worker ratio is
deliberately different from the weight ratio — the only rows that can actually tell the
two apart — currently stands at 2 PASS, 10 FAIL out of 12 across this project's settled
config (updated by [UNI-227](/UNI/issues/UNI-227)'s re-run, which added one more FAIL to this
count after this section was first written). Treat that, not the suite's overall PASS/FAIL
tally, as the headline evidence count for weighted fairness specifically; the tally overstates
support because most of its rows can't distinguish the claim from the alternative at all.

**That FAIL majority has a cause, and it is the one thing in this list worth leading
with: contended-window duration, not worker-ratio mismatch on its own, is what decides the
outcome.** Every discriminating row measured at 69.0s or more of per-group contended time
converges on the configured weights; every one at 66.3s or less tracks the offered worker
ratio instead — a clean but thin 2.7-second boundary (an earlier draft of this section said
"roughly a minute" versus "under ten seconds," which understates how close several FAILs sit
to the boundary; see `docs/poc-results.md`'s UNI-225 section for the corrected figures). The
cleanest evidence holds the scenario, the weight set, and
the gap size fixed and varies only the contended window: the same `33/33/33` weight set
with the same ~33-point worker-vs-weight gap lands on the weights at 69s of contention and
on the worker ratio at 8-9s. This is a strong association across every discriminating row
measured so far plus one controlled within-scenario comparison — not yet an independently
randomized duration sweep — but it means the right reading of a short-window FAIL is "the
mechanism hasn't had time to converge yet," not "the mechanism doesn't hold." See
`docs/poc-results.md`'s UNI-225 section for the full scorecard, the duration evidence, and
what still isn't covered (the equal-weight scenarios, and the saturation-limb instrumentation
and KV-cache-reachability finding — now done, Part 3 item 14 below).

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
  **Caveat ([UNI-186](/UNI/issues/UNI-186)):** `_input_tokens_sum`/`_output_tokens_sum`
  are **not trustworthy as a per-tenant raw-usage audit trail for any tenant that
  streams any of its traffic.** Confirmed live against `maas-vllm-gpu`: with
  `--enable-force-include-usage`, vLLM puts a real, non-null, cumulatively-growing
  `usage` block on *every* SSE chunk of a streamed response, not just the final one.
  The router observes that chunk's value on every chunk it's non-nil
  (`pkg/epp/handlers/response.go:90-95` — correct under the OpenAI contract that
  usage appears once; wrong under what vLLM actually sends), so a single streamed
  response's token counts get summed into the histogram dozens of times over,
  inflating the raw sum by roughly the chunk count (~58x observed on the UNI-147
  benchmark). This does **not** affect `contended_service_tokens_total` or the
  fairness policy itself — this repo's own true-up is gated on `!response.EndOfStream`
  and is unaffected. It only affects these two raw, un-gated upstream counters.
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

### UNI-212: the backlog edge was Pick-cadence-blind, not time-blind

[UNI-161](/UNI/issues/UNI-161), [UNI-160](/UNI/issues/UNI-160) and
[UNI-104](/UNI/issues/UNI-104) found the delivered split tracking offered
worker count / concurrency, not the configured weight, under closed-loop
over-offer: varying the weight set at a fixed 32:32:128 worker ratio always
converged on 32:32:128 (UNI-160), and varying app1's own worker count at a
fixed 30/10/60 weight set changed the overshoot almost in proportion to that
worker count, not the weight (UNI-161).

**Diagnosis**, backed by live evidence already in this repo plus a fresh read
of UNI-161's raw metrics:

- This file's own `00-config.yaml` carries a prior calibration finding:
  turning `newcomerClamp` on moved end-users from 62.8% to 45.1% while firing
  only 19 times in 862 dispatches, and "the highest-weight group is hit
  hardest, because it is served fastest, so its queue is the one that
  momentarily drains." That comment flagged the mechanism and left it
  unresolved; UNI-212 resolves it.
- `results/20261106T171509Z-uni-161-app1-flood-256-32-64/metrics-after.txt`
  shows `flow_control_request_queue_duration_seconds` with genuine,
  multi-second mean FlowController queueing for every group (app1 23.3s over
  n=2031, app2 13.7s over n=353, end-users 9.1s over n=903) — the
  FlowController really does hold a deep backlog, so `Pick` is genuinely the
  arbiter of most of each request's latency. This rules out "FlowControl
  never backs up" as the mechanism.
- `flow_control_queue_size`'s time series in the same run shows app2 and
  end-users (the two non-flooding groups) repeatedly cycling all the way down
  to **0** and back up to their full worker count throughout the 240s run
  (end-users: ...,64,0,2,36,11,64,19,32,...), while app1's climbs
  monotonically and never returns to 0. Every one of those drops to 0 is an
  `isBacklogEdge` the instant the group's next request arrives.
- `isBacklogEdge` (`pkg/fairness/weightedlas/state.go`) keyed "was this group
  a Pick candidate last time" to `seq`, a counter shared across the *whole
  band* and incremented on every `Pick` call. `Pick` is invoked from
  `dispatchCycle` (`llm-d-router`
  `pkg/epp/flowcontrol/controller/internal/processor.go`), which the
  processor's `Run` loop calls on a ~1ms ticker **and** synchronously on every
  enqueue from *any* group — not once per this specific group's own request.
  So a group's own inter-arrival gap only had to exceed roughly one Pick
  cycle — a millisecond, or however long it took some *other* group to
  enqueue something — to register as "away." That is far below the gap a
  return-from-genuine-idle clamp should fire on; one half-life is 60s.
- The effect is exactly the self-undermining asymmetry the config-comment's
  "largest weight loses the most credit" observation describes: a
  higher-weight group is *correctly* favored by `Pick` when it competes,
  which drains its own queue to empty faster, which produces more backlog
  edges for itself, each of which overwrites its earned (favorably low)
  `normalizedService` with the current floor — discarding exactly the credit
  its weight just bought it. A continuously-flooding group never empties its
  queue, so it is never edge-clamped at all, and accumulates (and is
  correctly penalized for) its tab normally. Net effect: any group that
  cannot sustain a literally-always-nonempty queue gets repeatedly reset to
  parity with the flooder instead of carrying forward the deficit its weight
  entitles it to — so the realized split tracks each group's own ability to
  keep a queue backlogged (worker count / offered concurrency), not the
  configured weight.

**Fix:** `isBacklogEdge` gains a wall-clock gate. A group present on the
*literal* immediately-preceding `Pick` call is still never an edge
(unchanged — the continuously-backlogged case costs nothing extra to check).
Otherwise, it is an edge only if **at least `newcomerClampIdleSeconds` of real
wall-clock time** elapsed since the group was last a candidate — not merely
"at least one Pick call since." New config field `newcomerClampIdleSeconds`
(default 2s): comfortably above normal dispatch-churn gaps (milliseconds),
comfortably below the tens-of-seconds absence the clamp exists to catch (see
`TestReturningIdleTenant`'s 10s Phase 1). `<= 0` reproduces the previous
(buggy) behavior exactly, kept as an explicit escape hatch rather than
removed outright.

**Expected effect:** a group that cannot sustain a continuously non-empty
queue stops losing its earned deficit every time its queue transiently
drains from being served promptly, so weighted sharing should hold closer to
the configured weights under UNI-161/UNI-160's own worker sizings. This does
not touch `TestWorkConservation` (an idle group still gets nothing — it has
no deficit to lose) or `TestReturningIdleTenant`'s genuine-absence case (10s
of simulated idle is 5x the 2s default gate), and it keeps `newcomerClamp:
true` as [UNI-162](/UNI/issues/UNI-162) already recommended — this is a
timing-precision fix to the existing mechanism, not a reversal of that
decision. New tests: `TestNewcomerClampIdleGate` (direct, deterministic
coverage of the gate itself) and `TestNewcomerClampGateImprovesBurstyShare`
(shows the fix measurably moves a bursty group's share up from the legacy
baseline and eliminates spurious clamps on a 20ms inter-burst gap, without
asserting a specific equilibrium number — a group's own duty cycle still caps
how much of the pool it can claim, independent of this fix).

**Not expected to fully close the UNI-161/UNI-160 gap on its own:**
[UNI-211](/UNI/issues/UNI-211) separately found an independent
scheduling-profile bug (prefix-cache-scorer endpoint lock-in,
[UNI-214](/UNI/issues/UNI-214), since fixed by giving `queue-scorer` and
`prefix-cache-scorer` equal weight). This plugin's own `contended_seconds_total`
accounting (`bandState.contendedDelta`) also resets its single, band-shared
timer to zero on *any* Pick call with only one candidate, which looks like a
second, separate undercount of true contention — worth a follow-up, but it
affects the SLI denominator, not dispatch order, so it is out of scope here.
UNI-161 and UNI-160 are re-run after this fix (below, with workers **not**
sized to the weights) to measure how much of the gap it actually closes, not
assumed to close it outright.

### UNI-220: the clamp was still firing on a tenant that never left, just because it was concurrency-limited

[UNI-215](/UNI/issues/UNI-215) swept `queueDepthThreshold` across {8, 16, 32,
64, 150} against `app1-flood` (weights 30/10/60, offered workers
256/32/64) and found every value FAILs in a 31-39 point band — moving the
threshold 18x moved the deviation by only 8 points, non-monotonically. This
is the one gap in the fairness POC that touches the core claim, and it is not
the threshold, the clamp being on vs. off as a binary, `enforce` being off, or
a stale image (all ruled out live — see [UNI-220](/UNI/issues/UNI-220)).

**Diagnosis**, built on UNI-212's fix above plus one targeted live
experiment:

- The policy is ordering correctly — per-request latency at the settled
  config has the flooder (app1) at the *highest* p50 and the starved tenant
  (end-users) at the *lowest*. Any design premised on "the ordering is
  wrong" is aimed at the wrong thing; see UNI-220's addendum for the full
  Little's-law accounting (`share_i ∝ workers_i / L_i`): the observed split
  is fully explained by offered workers and delivered latency, with no
  unexplained residual.
- The newcomer-clamp counters are the tell: at the settled config, the clamp
  fires 28 times on the starved end-users group and 0 times on the
  continuously-flooding app1, over one 240s run. It is firing almost
  exclusively on the group it is supposed to be protecting.
- UNI-212's wall-clock idle gate (`newcomerClampIdleSeconds`, default 2s)
  fixes the *millisecond*-scale false edge (a high-weight group draining its
  own queue between bursts a few Pick calls apart) but does not fix a
  different false edge: a tenant whose own **offered concurrency is below
  the pool's effective capacity** does not keep its FlowQueue continuously
  non-empty even while it has real, continuous demand — the single request
  each of its workers has outstanding is still being served, so the queue
  genuinely empties for longer than 2 seconds at a time, purely as a
  function of that request's latency, not because the tenant stopped
  wanting service. Every one of those drains, once past the 2s gate, is an
  `isBacklogEdge` the instant its next request arrives — and each one
  overwrites its earned (favorably low) `normalizedService` with the
  current floor, exactly the credit-confiscation UNI-212 diagnosed, just
  from a second root cause the wall-clock-only gate cannot see: elapsed
  time since last candidacy does not distinguish "gone" from "still being
  served."
- **Live confirmation (2026-11-11), the experiment the ticket's addendum
  specified before any code change:** `app1-flood` re-run at the live
  settled config (`queueDepthThreshold: 32`, weights 30/10/60, image
  `sha256:617509368126…`) with only `newcomerClamp` flipped to `false` for
  the run. End-users' deviation closed from **-31.3 points to -12.9
  points** — 59% of the gap, with several 10s windows mid-run landing
  inside the 10-point bar outright (e.g. t+130-140s: 0.0pt). This rules out
  pure work-conservation as the dominant mechanism (an admission-side fix
  would have been required instead) and rules in the clamp: disabling it
  outright gets most of the way to the bar on its own.

**Fix:** add a second, independent condition to the clamp, alongside the
existing wall-clock idle gate — a group with a dispatched-but-not-yet-completed
request (`groupState.inFlight > 0`) is never treated as a returning newcomer,
regardless of how long its FlowQueue has been empty, because it has not
actually left the system: it is still holding capacity and still earning (or
spending) its tab normally. `groupState.hasInFlight()`
(`pkg/fairness/weightedlas/state.go`) exposes this; `Pick`
(`pkg/fairness/weightedlas/plugin.go`) checks it alongside the existing edge
test before clamping. This is additive, not a relaxation: a genuinely idle
tenant (zero queue depth **and** zero in-flight, e.g. B1's cold join at
t=120s or a tenant that stopped sending traffic entirely) still clamps exactly
as before — `TestWorkConservation` and `TestReturningIdleTenant`'s
zero-in-flight newcomer case are unaffected. New test:
`TestNewcomerClampDoesNotFireWhileInFlight` demonstrates the gate directly —
an edge with in-flight work present leaves `normalizedService` untouched; the
identical absence shape with in-flight cleared still clamps.

**Why not just disable the clamp, since that closed 59% of the gap on its
own?** UNI-162 already found clamp-off shrinks the UNI-161-family failure but
does not clear it, and costs that scenario (B5, open-loop) more than 60%
throughput — the clamp is doing real, necessary work for a genuine cold
start (B1's 120s-late join), which an outright disable would also break. The
in-flight gate is the narrower fix: it stops firing on exactly the false case
(a concurrency-limited tenant that never really left) while leaving the
clamp fully intact for the case it exists for.

**Not expected to fully close the gap on its own:** -12.9 points with the
clamp fully *disabled* is itself still 2.9 points over the 10-point bar, so
even a perfect version of this fix is not guaranteed to cross the line by
itself — the remaining residual is consistent with the work-conservation
ceiling UNI-220's addendum derives from Little's law (`share_i ∝
workers_i / L_i`): admission-side holding can reorder and pace work that is
already queued, but the achievable latency spread between a 256-worker
flooder and a 64-worker starved tenant is bounded below by the starved
tenant's own floor latency (~1.7s, measured below-capacity), and the
required 8x spread for `app1-flood` specifically may sit above what any
*ordering-only* mechanism can deliver without an explicit per-group
admission cap or backpressure, both deliberately not implemented here
pending this fix's own re-measurement — seeing how much of the residual
in-flight gate alone removes is the point of re-running the four FAIL rows
before deciding whether a second mechanism is needed. See
`docs/poc-results.md` "UNI-220" for the full re-run and the final
ceiling/ratio disclosure.

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
  O_est = min( max_tokens ?? ∞ ,
               estimatedOutputTokens[group] ?? ewma[group] ?? defaultEstimatedOutputTokens )
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

### UNI-222: B4's "long idle return" FAIL is a scoring artifact, not a policy defect

[UNI-143](/UNI/issues/UNI-143)'s original B4 case (`full-contention`, app1
duty-cycling 150s on / 600s off / 140s on, 890s total) and its exact
reproduction at `queueDepthThreshold: 32` ([UNI-218](/UNI/issues/UNI-218))
both FAILed the same way: app1's **whole-run** delivered share came in at
5.5%, 15.5–15.6 points under its flat 21.1% target, while app2 and
end-users came in correspondingly over (+4.8/+10.7pt). Taken at face value
this reads as "a tenant returning after a long idle does not land on its
entitled share" — [UNI-222](/UNI/issues/UNI-222) was opened to find out
whether that is a real defect in the returning-from-idle clamp
(`### Returning-from-idle clamp` / UNI-212 / UNI-220, above) or a problem
with how the number itself is computed.

**It is the number.** The flat formula (`deploy/poc/15-fairness-report.py`'s
"Expected share" — each offered group's weight over the sum of every offered
group's weight) is applied uniformly across the run's *entire* duration,
which is only correct when every offered group is actually contending for
the whole run. B4 violates that by construction: app1 is idle for 600 of
890 seconds (67% of the run) by design, and work conservation — the
intentional, already-documented behaviour this project scores as *correct*
for `end-users-idle`/`app1-alone` (see "Expected share" at the top of
`15-fairness-report.py`) — correctly gives app1's unclaimed weight to app2
and end-users for that entire window. The flat formula has no way to tell
"app1 is being starved while contending" apart from "app1 wasn't
contending for most of the run and the other two correctly absorbed its
share while it wasn't" — it scores both as the same kind of deviation from
a target app1 was never actually entitled to for the idle 67% of the run.
[UNI-143](/UNI/issues/UNI-143) and [UNI-144](/UNI/issues/UNI-144) (B2/B3)
both already named this in prose ("the naive whole-run expected-% assumes
full-time offering it never had ... not the right number to judge this
case by") without ever fixing the number itself; UNI-143's own windowed,
post-return-only analysis (settling to within ±10pt noise in ~131s, a
similar noise band to the short-idle run) was already the better signal,
it just never fed back into the scored `verdict`.

**The fix: `schedule_aware_whole_run_shares`.** When a scenario provides
both `--timeline-config` (the declared per-tenant join/leave/duty-cycle
schedule) and `--metrics-timeseries`, and that schedule is non-trivial for
at least one offered group (`schedule_has_partial_offering`), the whole-run
`expected_share_pct`/`observed_share_pct`/`deviation_pts` fed into `verdict`
are recomputed as a token-volume-weighted aggregate of the same per-window
values UNI-127's `timeline.windows` already compute (the ones that already
correctly renormalize each window's expected share among only the groups
active *in that window*):

```
for each window:
    active_total = sum(delivered_tokens for groups active in this window)
    if active_total <= 0: skip (nothing to attribute -- including a window
                                 where every scheduled group is between its
                                 own stop time and the run's tail, draining
                                 in-flight requests with nobody left
                                 "eligible" to be scored against)
    denominator += active_total
    for each active group g:
        observed_numerator[g] += delivered_tokens[g]
        expected_numerator[g] += (expected_share_pct[g] / 100) * active_total
expected_share_pct[g] = 100 * expected_numerator[g] / denominator
observed_share_pct[g] = 100 * observed_numerator[g]   / denominator
```

A scenario with no declared schedule, or where every offered group is
active for the entire run, is completely unaffected: every window's active
set is then "everyone," so the per-window expected share equals the flat
global ratio in every window, and the volume-weighted average of a constant
is that same constant — mathematically identical to the pre-UNI-222
formula, confirmed byte-for-byte on a real `full-contention` run with no
`--timeline-config` tenants declared. `worker_share_pct`/
`worker_vs_weight_gap_pts` (UNI-225) and `request_share_pct`/
`request_share_deviation_pts` (UNI-146/C1) deliberately keep the flat
definition — both are about the scenario's *configured* sizing, not about
how long a group happened to be present, so a schedule change should not
move them.

**Re-run under the corrected formula, same raw artifacts** (re-fed through
the fixed report generator, not re-executed against the cluster — the
underlying EPP behaviour is unchanged, only how it is scored):

| case | flat whole-run (pre-UNI-222) | schedule-aware (UNI-222) |
|---|---|---|
| B4 long idle return (UNI-143 run) | **FAIL**, app1 −15.5pt | **PASS**, max 3.0pt (app2) |
| B4 long idle return (UNI-218 thr32 run) | **FAIL**, app1 −15.6pt | **PASS** (re-run live under UNI-222, see docs/poc-results.md) |
| B4 short idle return (UNI-143 run) | PASS, app1 −5.3pt | PASS, max 4.2pt (app2) — tighter, same verdict |
| B1 cold join (UNI-245 thr32 confirm — the named regression control) | PASS, app1 −7.8pt | PASS, max 8.2pt (end-users) — same verdict, closer to the bar |
| `full-contention` (no declared schedule — the other named regression control) | PASS, 4.0pt | **identical**, 4.0pt, `schedule_aware_groups: []` |

B1 cold-join is the interesting near-miss: end-users joins at t=120 of a
~240s run, and because essentially none of that run's volume was
*contended* before the join (app1/app2 alone never backed up the queue —
the same `A1 app2-alone`/`A6 below-capacity` pattern), excluding the
pre-join window from the denominator barely moves the number (7.8→8.2pt).
It stays a clear PASS, but it is close enough to the 10-point bar that a
scenario shaped like "a late joiner that's already somewhat over-served
once it does arrive" could flip under this formula where it would not have
under the flat one — a real, intended consequence of scoring entitlement
against actual presence, not a bug to work around.

**Verdict for UNI-222: test-expectation problem, not a defect in the
clamp/decay mechanism.** The returning tenant's post-return behaviour was
already measured as converging (UNI-143's windowed analysis); the whole-run
FAIL was entirely an artifact of blending a correctly-zero-demand idle
period into a uniform-weight average. No change to
`pkg/fairness/weightedlas` was needed or made for this ticket — the
clamp/decay mechanism (`### Returning-from-idle clamp`, UNI-212, UNI-220,
above) is unchanged. **Correct behaviour on return, stated plainly:** a
tenant idle long enough for its decayed tab to reach the newcomer-clamp
floor returns on equal footing with whoever it finds already contending
(by design — see `### Returning-from-idle clamp` above), is low-latency for
its first dispatch, and converges back toward its configured weight share
within roughly one settling period (~110–132s measured across
UNI-141/142/143/144) once it is actually contending again; it earns no
credit for having been away, and is not expected to make up the
tokens/share it would have received had it been contending the whole time
it chose to be idle. A scoring methodology that expects the latter (the
pre-UNI-222 flat whole-run ratio, for any case with a declared idle/join
schedule) is checking the wrong thing.

**Known, deliberate side effect, flagged for the reviewer rather than
silently absorbed:** the same correction applies to every other scenario in
this repo with a declared `--timeline-config` schedule that isn't trivial —
notably B2 (`tenant-leaves-mid-run`, UNI-141), B3 (`on/off duty cycle`,
UNI-144), and `app3-joins-at-saturation` (UNI-164) — whose own whole-run
`verdict` fields will also change on their next re-run (B2/B3 both already
carry the same "not the right number" caveat in prose; UNI-164's own
whole-run ratio is similarly distorted by its staggered join, per
[UNI-201](/UNI/issues/UNI-201)). Retroactively re-scoring their *historical*
docs/poc-results.md rows is out of scope for this ticket — filed as a
follow-up so it is tracked rather than silently left stale.

### UNI-293: SFQ priority stamp

**Why.** UNI-288 found that under closed-loop load the EPP holds ~8 requests
and vLLM's FIFO waiting queue holds ~88, so FIFO, not this policy, orders
most dispatches. UNI-290 round 2 showed that stamping a start-time fair
queueing (SFQ) tag as vLLM's `priority` composes Arm A exactly, with nothing
held at the EPP. UNI-291 confirmed the stamp path exists (`PreRequest` ->
`MutatePayloadMap` -> the director's `repackage`) and that vLLM 0.24 reorders
its waiting queue on the tag without preempting on it.

**The tag.** A group g with weight w dispatching a request with estimated
cost c gets start tag `S = max(F_g, V)`, then `F_g = S + c/w`. At completion,
`F_g += (actual - charged)/w`. A tag never decays, so the true-up is
undecayed by construction. The estimate is the same `min(max_tokens, EWMA)`
the tab uses, which is exactly what the UNI-283 tight-`max_tokens` vector
drives low. Without the true-up the gamer takes 50.1% against a 21.1% target.
With it, 21.1%. The `sfq_sim_test.go` case `TestSFQSimGamingVector`
measures this in CI.

**The tab's version of the same fix: `undecayedTrueUp`.** The vector is
also live on the tab in today's build, with or without the stamp. The tab
decays, and the existing true-up decays its correction by
`2^(-inflight/H)`, so by the time a long request completes most of its
under-estimate has gone. With `undecayedTrueUp: true`, an under-estimate
lands at full weight on completion. Over-estimates are still refunded
decayed, so a refund can never exceed what is left of the hold. It has its
own flag, so it can be reviewed and shipped without the stamp.

**V.** The virtual clock is the **minimum, over serving endpoints, of the
newest start tag each one has begun serving**, not the max. With uneven
endpoint speeds, the max definition's error grows ~1.5 pt per doubling of N
(5.3 at N=8, 9.3 at N=64). The min definition measured 0.0 at every N
(UNI-291). "Begun serving" means the first response byte reached the EPP:
the first token for a stream, the completion for a non-streaming request.
UNI-290 found the "V from completions" variant equally robust.

**What "serving" means, and why idle endpoints are excluded.** An endpoint
counts toward the min only while it has a request in flight **and** has been
seen to start one within `sfqEndpointStaleSeconds`. Otherwise V freezes: an
endpoint that starts nothing pins the min at its last start, every new tag
collapses to its own group's F_g, and a group returning from idle restarts
at its old F_g and takes every queue slot until it catches up. The two cases
that trip this are an endpoint with no traffic (idle) and one whose
responses never come back (stale). Stale is an expected mode on this
cluster: PreStop fails every time, and UNI-193 lost ~80% of dispatch
accounting on one path. An endpoint that goes idle forgets its last start,
so on return it rejoins the min only once it starts something new. V is
monotone, so excluding an endpoint can never move it back. A stale window
set too short drops slow but healthy endpoints between starts and drifts
toward the max definition's error. Set too long, it lets a wedged endpoint
hold V for that long. Either way the freeze is bounded.

**When completion is never observed.** Any ticket with no completion after
`sfqSettleTimeoutSeconds` is presumed lost. It is charged its **worst-case**
cost (prompt plus all of `max_tokens`, or `sfqUnboundedOutputTokens` with no
`max_tokens`) and taken off its endpoint's in-flight count. A group whose
completions are lost therefore pays at least as much as any completion
could have cost. Keeping the low estimate would be the failure the gaming
vector exploits. If the completion turns up later, it is trued down to the
measured cost. Reaping runs on dispatch, so it costs nothing while the pool
is idle. `maas_fairness_sfq_unsettled_total` counts how often the ledger runs
on presumption. A completion **without** a usage block (error status, reset,
cancel) keeps its tag charge. That deliberately differs from the tab's
UNI-213 refund: refunding the tag would let a client read most of a stream,
disconnect, and get its queue position back.

**What the stamp retires.** With `sfqPriorityStamp` on, there is one notion
of accumulated service, the finish tag, and the code says so in `Pick`:

- *The EWMA tab (`halfLifeSeconds`)* is no longer an input to any dispatch
  decision. `Pick` ranks the EPP-held queue by each group's next start tag,
  `max(F_g, V)`, so the EPP and vLLM's waiting queue rank by the same number.
  The tab is still charged and decayed, for `maas_fairness_normalized_service`,
  the flight recorder and the state dump only. `halfLifeSeconds` and
  `undecayedTrueUp` then shape only that series. Behind an EPP hold of 4,
  ranking by the tab instead lets the gaming vector back in: ~23.7% against
  the 21.1% target, versus ~21.4% by tag (`TestSFQSimHoldOneNotionOfService`).
- *`newcomerClamp`* does not run. `max(F_g, V)` is the exact form of the same
  rule. The clamp writes only to the tab, so with both on it would change
  nothing `Pick` decides. Skipping it keeps the clamp counter from reporting
  firings that did nothing. `TestSFQSimHoldReturnNeedsNoClamp` shows a return
  from idle and a new join behind an EPP hold with no burst by tag
  (dev ≤0.4 pt in the first 30 s), against ~30-37% for a 10.5% target on the
  tab with no clamp. UNI-283's joiner delay via the ratchet (315 s vs 77 s)
  did **not** reproduce in this model in either arm. The redundancy is
  measured; the misbehaviour is not.
- *The `virtualTime` ratchet* (`bandState.virtualTime`) is not advanced. Its
  only reader was the clamp floor. `sfqState.v` is the one V.
- *`agingTokensPerSecond`* is in tab units, so a non-zero value is rejected at
  startup when the stamp is on.

**Estimate versus true-up.** The dispatch estimate fixes *this* request's
tag. The completion true-up corrects the group's *future* tags. The gaming
vector lives entirely in the second. The cost inputs are unchanged
(`inputTokenWeight: 1.0`, `outputTokenWeight: 2.0`), but `outputTokenWeight`
is still uncalibrated. It now sets the tag step directly rather than feeding a
decaying average, so a mis-set value is a standing bias, not a transient.
Calibration is out of scope here.

**The three non-negotiables.**

1. *The `priority` field is always the plugin's.* With
   `propagatePriority` off, nothing else in the EPP touches it, so a client's
   own value reaches vLLM unchanged. Under fcfs it is ignored. Under priority
   scheduling it is a queue jump: the same class as the client-controlled
   fairness ID flagged on upstream PR #3471. With the stamp on, it is
   overwritten on every path, including provisional charging off, unknown
   groups and an empty fairness ID. A body the plugin cannot rewrite (raw or
   proto payload) is **rejected** (400), not forwarded. With the stamp off, a
   client `priority` is deleted, which is a no-op under today's fcfs.
   `maas_fairness_client_priority_overwritten_total` counts both.
2. *Integer tags only.* vLLM answers `3.5` with 400 `int_from_float`. Tags
   are stamped as `int64` milli-cost-units (`round(S * 1000)`), clamped to
   `[0, 2^53]`. `TestStampedPriorityIsNeverFractional` checks the
   marshalled bytes.
3. *`propagatePriority` must be off.* It runs after `PreRequest` and
   overwrites the tag with the objective's static priority, which would
   disable fairness silently. The plugin `Handle` does not expose it, so
   `Factory` re-reads the EPP's own `--config-file` / `--config-text` from the
   already-parsed flag set. It refuses to start if the setting is on, **or if
   it cannot find the config to check**.

**Bounding the stamp: rebase and idle reset (UNI-300).** V only ever
increases, and the stamp is V-scale times 1000, so something has to stop it
reaching a ceiling. The ceiling was measured, not assumed. vLLM 0.24.0+rhaiv.9
declares `priority: int` with `le=2^63-1`: 2^63-1 is served, 2^63 is a 400.
Integer literals arrive exact at the scheduler's heap compare, 2^53+1
included (in-pod check of vLLM's own parse, msgpack and compare path). The
one silent failure is a *float-formatted* value above 2^53, which rounds.
The stamp is an `int64` marshalled as an integer literal, so that does not
happen on this path.

The failure being prevented is silent. A clamped stamp ties with every other
clamped stamp, ties go by arrival, and arrival order is FIFO. No error is
raised. Time to reach the ceiling under continuous saturation, with V's rate
taken as pool cost rate over the contending weight. The token-model
anchor was measured: 320 tag units/s live on 16 slots at weights
20/10/65, where C/Σw predicts 326. Large requests assume 50k-token
prompts, 4k-token outputs at ~30 tok/s per sequence.

| cost model, sizes | slots | Σw contending | to 2^53 (before) | to 2^63-1 (now) |
|---|---|---|---|---|
| token, today's | 800 | 95 / 15 | 18 y / 3 y | 17,900 y / 2,800 y |
| token, 50k / 4k | 800 | 95 / 15 | 81 y / 13 y | 82,800 y / 13,000 y |
| vramtime, today's | 800 | 95 / 15 | 113 d / 18 d | 317 y / 50 y |
| vramtime, 50k / 4k | 800 | 95 / 15 | **8 d / 31 h** | 23 y / 4 y |

Weights are not normalised, so V's rate scales with 1/Σw: the same shares
written as 0.2/0.1/0.65 run the clock 100 times faster. In the token model,
larger requests make V *slower*, not faster. Cost is linear in tokens, so its
rate is bounded by token throughput, and long decodes have less of that than
today's prefill-heavy traffic.

Two mechanisms, for two different jobs:

- **Threshold rebase** (`sfqState.rebase`, at V >= 2^30 tag units).
  Subtracts the integer part of V from V, every F_g and every endpoint's
  newest start, and adds it to `wireBase`. The stamp is `wireBase` plus the
  quantised internal tag, so **no stamp moves**. That is the requirement,
  not a nicety. vLLM already holds requests stamped on the old numbering
  and cannot renumber them. A rebase that let the stamp drop would sort
  every later request ahead of all of them.
  `TestSFQSimRebaseIsInvisible` rebases every 50 tag units, hundreds of
  times a run, and the stamped priorities match the no-rebase run request
  for request. Its power check drops the stamp instead: in the flood that
  took max e2e from 110 s to 257 s and app2 to 5% against 10.5%. What the
  rebase buys is internal tags that stay small and exact, so the stamp can
  use vLLM's whole range, 1024 times the old headroom.
- **Idle reset** (`sfqState.resetIfIdle`). Once no endpoint has a request
  in flight, the next dispatch starts a new epoch: V, every F_g and the
  stamp go back to 0. This is SFQ's published busy-period rule (Goyal, Vin
  and Cheng 1996: at the end of a busy period V is set to the largest finish
  tag, which levels every flow). It is the board's "numbers go back to 0".
  Without it, V froze across the idle, and `max(F_g, V)` erased stale credit
  but kept stale debt. `TestSFQSimIdleResetsTheLedger` measures that debt.
  With fixed-size requests a tenant goes idle about one request ahead, and
  nothing measurable follows. With variable output lengths, the requests
  still running when traffic stops are the long, under-estimated ones,
  trued up after V stopped. In the sim app1 went idle 709 tag units
  ahead, then waited 13.3 s for its first request after the idle (others
  ~0.6 s) and got 0% of the first 10 s. With the reset it waited 0.17 s.
  The delay is debt over V's rate, so it is bounded and does not grow with
  the idle. It does grow with request duration and with Σw over the
  tenant's weight, and it recurred every episode.
  A request presumed lost (reaped) holds the reset off for one more
  `sfqSettleTimeoutSeconds`. It may still be queued in vLLM with an old
  stamp, and its worst-case charge should not vanish across a short idle.

Under saturation that never idles, only the threshold rebase runs, and the
stamp's headroom is the right-hand column. An EPP restart also resets the
ledger (see Limits). `_sfq_rebases_total{reason="threshold"|"idle"}`
counts both. `_sfq_stamped_priority` approaching 9.2e18 is the alert.

**Sizing the stale window and the settle timeout (UNI-300 review).** Both
defaults (60 s, 900 s) were set against 5-25 s requests.

- *Stale window.* An endpoint's mean gap between starts is S/N_eff: mean
  service time over the concurrency it actually runs. N_eff is KV-derived
  and can sit far below `max_num_seqs`. With 50k-token prompts an 8B model
  on one 80 GB GPU fits ~8 sequences, whatever `max_num_seqs` says. Gaps
  are near-exponential, so a healthy endpoint drops out of the min with
  probability ~exp(-k) per gap, where k = staleAfter·N_eff/S.
  `TestSFQSimStaleWindowRule` confirms the gap to within 2%. The cost is
  smaller than the rule suggests, because the error needs the whole slow
  cohort out at once. With half of 8 endpoints slow: k 0.67 within noise,
  0.5 costs ~2.5 pt, 0.25 costs 4-7 pt (as bad as max-tag). At N=64, k 0.25
  is within noise: the error falls with fleet size.
  **Guidance: staleAfter >= 3·S/N_eff.** That is ~5% drop-out per gap and
  ~4x margin on the measured threshold. For 720 s requests that is 270 s at
  N_eff 8 and 17 s at N_eff 128. The price of a longer window: a wedged
  endpoint pins V for that long.
  `_sfq_stale_dropouts_total` counts drop-outs live.
- *Settle timeout.* Measured from dispatch, so it counts vLLM queue wait
  as well as service, and under the stamp that wait is long for whoever
  is behind. `TestSFQSimSettleTimeoutCountsQueueWait`, behind an EPP gate
  of 8 on 16 slots, service spread sigma 0.6: 1.25 S reaps 52% of
  legitimate requests and moves the composition 6-7 pt. 2 S reaps 20%
  (2-3 pt). 2.8 S reaps 5% and is clean. With no gate (vLLM holding ~80),
  the low-weight tenant's median dispatch-to-completion is ~19 S, and even
  4 S costs 5-7 pt. **Guidance: settle >= 1.5x the p99 of
  dispatch-to-completion.** By Little's law that is a group's in-flight
  count over its completion rate. 900 s against 6-12 min requests is
  inside the danger band. `_sfq_late_completions_total` /
  `_sfq_unsettled_total` is the live share of reaps that were not lost
  at all.
- *Why not derive them at startup.* S, N_eff and queue depth are not known
  at startup: they depend on traffic and prompt length. Deriving them at
  runtime is feasible: per endpoint from the observed gap, per group from
  observed dispatch-to-completion. That is filed as UNI-304, not built here.

**Observability.** Metrics `maas_fairness_sfq_enabled`, `_sfq_virtual_time`,
`_sfq_serving_endpoints`, `_sfq_finish_tag{fairness_id}`,
`_sfq_lag{fairness_id}` (F - V), `_sfq_stamped_priority{fairness_id}`,
`_sfq_unsettled_total`, `_sfq_late_completions_total`, `_sfq_stale_dropouts_total`, `_sfq_rebases_total{reason}`, `_sfq_unstampable_total`. Response header
`x-maas-fairness-priority` (when `emitAttributionHeaders`). Flight-recorder
fields `sfqVirtualTime` and `sfqFinishTag`. V(4) fields `sfqPriority` and
`sfqStartTag`. A `sfq` section in the `StateDumper` output with every
endpoint's in-flight count, newest start and serving flag.

**Limits, stated plainly.**
- One EPP replica is one clock. Two replicas would stamp tags that cannot
  be compared. The EPP is `replicas: 1` today.
- An EPP restart resets every tag to 0 while requests stamped by the old
  process may still be queued in vLLM. New requests sort ahead of them, and
  under sustained saturation they wait until the new stamps climb back to
  theirs, roughly as long as V took to get there, or until the saturation
  ends. That is the mechanism of the rejected rebase arm in
  `TestSFQSimRebaseIsInvisible`. UNI-300 corrected an earlier "one queue
  drain" estimate here. The idle reset bounds it to the current busy
  period, but does not remove it.
- Nothing here changes vLLM. The stamp does nothing until the pool runs
  `--scheduling-policy priority`. **UNI-292** (resolved 2026-11-24, a read-only grep of
  the shipped RH vLLM image's own `arg_utils.py`/`scheduler.py`/`request_queue.py`)
  found `SchedulerPolicy` and a `PriorityRequestQueue` branch present. **UNI-303**
  (2026-11-25) independently confirmed this at runtime: the shipped RH vLLM build
  (`0.24.0+rhaiv.9`) accepts `--scheduling-policy priority` as a non-default arg and
  boots healthy -- on the CPU vLLM path
  (`results/20261125T231600Z-uni303-image-rebuild-and-sched-policy-check/`). Not yet
  confirmed at runtime on the GPU path specifically (same vLLM version, different
  container).
- The CI sim (`sfq_sim_test.go`) drives the real plugin's stamp into a
  model of vLLM's priority queue. It is a model, not a live run.

### Three vLLM flags are hard prerequisites

All three go on the **vLLM container** (`spec.template` in the LLMInferenceService), not
the scheduler. The first two default to **off** and fail silently. The third
(`--scheduling-policy priority`, added for UNI-293) defaults to vLLM's own FCFS and is
inert rather than silent-wrong when missing: with no `priority` stamped, FCFS and
"priority with everyone tied" dispatch identically, so this one is safe to add any time,
including before `sfqPriorityStamp` is ever turned on -- see
[AIRGAP-HANDOFF.md §7.3](../AIRGAP-HANDOFF.md#73--stage-the-model-and-deploy-the-inference-service).

```
--enable-force-include-usage     # "including usage on every request"
--enable-prompt-tokens-details   # populates usage.prompt_tokens_details
--scheduling-policy priority     # required for the SFQ stamp (UNI-293) to do anything
```

**Why the first.** OpenAI streaming only emits a usage block when the client sets
`stream_options: {"include_usage": true}`. The EPP parser documents this
(`parsers/openai/openai.go:599`: *"If include_usage is not included in the request,
`data: [DONE]` is returned separately"*) and nothing in the EPP injects it. Without
the flag, any streaming client that doesn't opt in never triggers a true-up and is
charged the provisional estimate permanently — and interactive end users, the largest
group, are the most likely to be streaming. (This case stays charged — a real
completion happened and real GPU time was spent, so refunding it would
undercharge, not correct a leak. See UNI-190/UNI-213 below for the no-usage
cases that are exempted instead: an error status, a stream reset, or a
cancelled context, none of which ever delivered anything.)

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

### UNI-299: per-group estimatedOutputTokens

A group may set `estimatedOutputTokens` next to its weight. When set, it is
that group's output estimate at dispatch: ahead of the group's EWMA and the
global `defaultEstimatedOutputTokens`, and still capped by the request's
`max_tokens`, so an operator value never out-charges what the client said it
could generate. Omitted means the EWMA-then-default chain as before. `0` is
honoured as zero, not as unset.

The board chose this ordering (UNI-299, 2026-11-25) over using the value only
as a cold-start seed. The consequence is that the estimate does not learn for a
configured group. The EWMA is still kept and appears in the state log as
`ewmaOutputTokens` next to `estimatedOutputTokens`, so a stale value shows as a
gap between the two.

What a wrong value costs, under the SFQ stamp with the completion true-up
(`sfq_sim_test.go` `TestSFQSimConfiguredEstimate`, app1 wrong by 10x, other
groups exact):

- **No standing error.** The true-up fixes the finish tag on every completion,
  so after a transient the split is within 1 pt of target in both directions.
  With the true-up off the same error is permanent (~37 pt for an under-estimate,
  ~18 pt for an over-estimate).
- **A transient on every entry.** Requests already stamped keep their tags, so
  each time the group starts sending -- EPP restart, ConfigMap edit, or return
  from idle -- its in-flight set carries in-flight × |estimate − real| tokens
  of error, repaid at its fair rate. Under-estimate (real 10x): app1 bursts to
  ~28% (target 21%) for ~5 s at 32 workers, ~61% for ~30 s at 256. Over-estimate
  (real 1/10): app1 is starved to ~3% for ~60 s at 32 workers and ~400 s at 256.
  A seed-only value would have learned by the group's second burst; this one
  repeats the transient on every burst (measured: 3.0% vs 20.8% in the first 30 s
  after a return).
- **Over-estimating is the expensive direction**, by the same ratio as the error
  in tokens: 10x over is 576 tokens per request of debt, 10x under is 57.6 of
  credit. It mostly hurts the configured group itself.

Gaming: a low value is not a standing advantage while the true-up is on. It
buys a burst on each entry of at most in-flight × (real − estimate) tokens,
which the group repays straight after. A floor is not needed for that. If the
true-up is ever turned off, a low value becomes a permanent advantage, and a
floor (or seed-only) would be needed.

## Config

```yaml
apiVersion: llm-d.ai/v1
kind: EndpointPickerConfig
featureGates: [flowControl]
plugins:
  - type: maas-weighted-fairness
    name: maas-fairness
    parameters:
      identityHeader: x-maas-subscription   # lowercase; set by Kuadrant AuthPolicy.
      # CORRECTION (UNI-129, 2026-11-01): this example originally read
      # "x-maas-subscription-id", which is not the header MaaS actually
      # injects and was never matched by the live config -- see
      # deploy/epp-config.yaml's own comment and docs/runbook.md's
      # "Identity-variant harness (UNI-129)" for the live-confirmed name and
      # what silently broke while this was wrong.

      # Weights sum to 100 so each number reads as a guaranteed floor.
      # First match wins: explicit applications before the prefix catch-all.
      groups:
        - { name: app1,      weight: 20, match: { exact:  [app1-production] } }
        - { name: app2,      weight: 10, match: { exact:  [app2-batch] } }
        - { name: end-users, weight: 65, match: { prefix: [end-user-] } }
      # Optional per group: estimatedOutputTokens (UNI-299), e.g.
      #   - { name: app1, weight: 20, estimatedOutputTokens: 4000, match: {...} }
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
      # Inert when sfqPriorityStamp is on: the SFQ start tag does the same job exactly.
      newcomerClamp: true
      provisionalCharge: true
      # UNI-293, off by default. An under-estimate's true-up lands at full weight
      # on completion rather than decayed by 2^(-inflight/H). That closes the
      # tight-max_tokens vector, where tiny requests drag the output EWMA down
      # and long ones under-pay. Over-estimates are still refunded decayed. See
      # "UNI-293: SFQ priority stamp" above.
      undecayedTrueUp: false
      # UNI-293, off by default. Stamps every request's vLLM `priority` with its
      # SFQ start tag. That only does anything on a pool running
      # --scheduling-policy priority. Independent of `enforce`. When on, the EPP
      # refuses to start if requestHandler.propagatePriority is on. Even when
      # off, a client-supplied `priority` is stripped. See "UNI-293: SFQ
      # priority stamp" above for the three tuning knobs.
      sfqPriorityStamp: false
      sfqEndpointStaleSeconds: 60     # bounds how long a wedged endpoint can freeze V
      sfqSettleTimeoutSeconds: 900    # no completion by then = lost, charged worst case
      sfqUnboundedOutputTokens: 4096  # worst-case length for a lost request with no max_tokens
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

  # scheduling profile: KServe default plugins, re-weighted below (UNI-214)
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
      - { pluginRef: queue-scorer, weight: 3.0 }   # KServe default is 2.0 -- see below
      - { pluginRef: kv-cache-utilization-scorer, weight: 2.0 }
      - { pluginRef: prefix-cache-scorer, weight: 3.0 }
      - { pluginRef: max-score-picker }
```

**`queue-scorer` and `prefix-cache-scorer` carry equal weight** (UNI-214). At
the KServe default (queue 2.0, prefix 3.0), a replica holding a near-complete
prefix match keeps a constant +1.0 lead no matter how long its queue grows,
because `queue-scorer` is min-max normalized across the candidates and so can
never swing by more than its own weight. With traffic that shares one prefix,
the other replica then sits idle indefinitely: one of two replicas took zero
requests for whole 240s runs in UNI-211, and the board saw the same in the
field. With equal weights, the cold replica wins as soon as the warm one's
queue is longer, warms its own cache, and from then on the shorter queue wins.
Prefix affinity still decides between equal queues. Verified live: both
replicas ~50/50 at a 98.9% hit ratio each, and no cache-hit regression for a
cache-hot tenant (docs/poc-results.md "UNI-214").

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

If any of A/B/C stream, the first query is unreliable — see the
[UNI-186](/UNI/issues/UNI-186) caveat above — and `_contended_service_tokens_total`
(gated, this plugin's own metric) should be used for the share instead.

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
| `..._identity_header_missing_total{reason}` | Counter | `reason` is `absent` or `empty`. The blind spot of the row above: a request with no identity header has nothing to mis-match. `absent` ≈ all traffic means `identityHeader` names a header the gateway never sends, and fairness is silently doing nothing (UNI-306); the plugin also logs a once-per-minute warning when ≥90% of a window's requests (≥20) miss it |
| `..._truing_error_tokens{fairness_id}` | Histogram | `actual − estimate`. Symmetric noise is fine and self-correcting; a persistent per-group **bias** is the signal — it means `bytes/4` is wrong for that group's content (CJK runs ~1–2 bytes/token and under-charges 2–4×; multimodal token counts have no relation to JSON size at all). That, and only that, justifies a per-group `estimatedBytesPerToken` override or finally reaching for the tokenizer |
| `..._requests_without_usage_total{fairness_id}` | Counter | **regression detector.** With `--enable-force-include-usage` set this is flat zero; non-zero means a model server shipped without the flag and that tenant's tab is estimate, not measurement. Alert on `> 0` |
| `..._prompt_tokens_cached_ratio{fairness_id}` | Gauge | **the headline shadow-mode reading.** Per-group cache hit rate — decides whether `cachedInputTokenWeight` is a real lever or a no-op, and in whose favour. Also guards the second vLLM flag: a flat zero here means `--enable-prompt-tokens-details` is missing, not that the cache is cold |
| `..._enforcing` | Gauge 0/1 | enforcing, or shadow mode |
| `..._sfq_charged_cost_total{fairness_id}` | Counter | UNI-302. Cost booked to the group's SFQ finish tag, counted at settlement (measured actual, else the estimate) or at reap (worst case). `rate()` over `sum(rate())` is the live composition — see "UNI-302: the stamp explains itself" for the PromQL and why it means nothing outside contended time |
| `..._sfq_dispatched_at_front_total{fairness_id}` | Counter | UNI-302. Dispatches stamped at rank 1 (no other group's next tag lower). Over `dispatch_total`, how often the group is at the front; a heavily weighted group should sit near 1 under contention |

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

### No log retention yet — the load harness captures its own (UNI-46)

This cluster has no log aggregation or retention window, so a flight-recorder line
(above) that scrolled off the pod's own buffer before anyone looked is gone — there is
nothing else holding it. Until a retention window exists, `deploy/poc/13-loadgen-poisson.sh`
closes that gap per-run rather than per-cluster: it follows the GPU EPP container's log
for exactly the run's duration into the same output directory as its metrics snapshots,
and records the byte count and any mid-run restart in a manifest next to it. See
docs/runbook.md "Per-run EPP log capture" for the mechanics. This is a stopgap scoped to
measured load-test runs, not a substitute for real retention (Loki, per "Then:" above) —
it captures nothing about traffic outside a harness invocation.

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

### UNI-302: the stamp explains itself

One switch, `sfqDecisionLog` (`off` by default, `info`, `debug`), read only with
`sfqPriorityStamp` on. Field-by-field shape is in `docs/log-field-contract.md` §3.4.

- `info`: one `"sfq priority"` line per dispatched request — group, weight, the stamped
  integer, its tag, its **rank** among the groups' next tags (`"rank":"2/4"`), `V`, and
  how far above `V` the tag and the group's finish tag sit.
- `debug`: the info line, plus one `"sfq decision"` record per dispatch (every input to
  the stamp: `est`, `worst`, `V` before and after with the endpoint that supplied the
  min, `start = max(F_g, V)`, `F_g` before and after, the quantised tag and `wireBase`,
  **every group's finish tag**, every endpoint's `inFlight` / last-start age / `serving`,
  and the tickets `reap()` charged this call) and one `"sfq settle"` record per
  completion (`charged` vs `actual`, the `F_g` correction, `F_g` before and after).

**Why config alone, not `-v`.** The V(4) tier above also needs `-v=4`, which the
KServe-managed scheduler cannot be given (runbook, "On the KServe-managed
scheduler"). These lines are emitted at the process's default verbosity and gated by
the plugin config only, so `maas-epp-config` is enough to turn them on. Off, nothing
new is logged.

**Hot-path cost.** `dispatch` and `settle` return a record by value. With the log off it
holds scalars only: `V`, `F_g`, the tag, the rank (one pass over the group map, no
allocation) and any reaped tickets (allocated only when one is reaped, as before). The
`finishTags` and `endpoints` copies are taken only at `debug`. Nothing is formatted or
written under `sfqState.mu`: the record is a snapshot, and
`TestSFQDecisionLogWrittenOutsideTheLock` fails if any line is written with the lock
held. `Pick` is unchanged.

**Rollout order — this can stop an EPP from starting.** llm-d-router decodes plugin
`parameters` with `DisallowUnknownFields`. An EPP on an image older than this change
fails to start if `sfqDecisionLog` appears in its config. The GPU and CPU schedulers
read the same `maas-epp-config`, so roll the new image to **every** scheduler that
reads it before adding the key.

**Verification.** `TestSFQDecisionLogReproducesTheStamp` runs Arm A (and a variant
where completions true up) with `debug` on, and checks every dispatch: `start =
max(F_g, V)`, `F_g' = start + est/w`, `tag = round(start × 1000)`, `stamp = wireBase +
tag`, the stamp equals the integer in the body, and the rank matches the logged
`finishTags`. It also rebuilds every `F_g` from the log alone (decision and settle
records), so a missing or wrong true-up record fails it. `TestSFQChargedCostConvergesInArmA`
shows the counter's share over 30 s windows sits within 0.8 pt of 20/10/65, and within
0.2 pt of the sim's own slot-second scoring.

#### Reading the live distribution (Grafana)

Set `$ns` to the scheduler's namespace. On the three-lane cluster every instance uses
the same names, so the namespace filter is what keeps the lanes apart.

Observed share, per group:

```promql
sum by (fairness_id) (rate(llm_d_epp_maas_fairness_sfq_charged_cost_total{namespace="$ns"}[5m]))
  / ignoring (fairness_id) group_left
sum (rate(llm_d_epp_maas_fairness_sfq_charged_cost_total{namespace="$ns"}[5m]))
```

Target share, normalised over the groups that had any traffic in the window:

```promql
(max by (fairness_id) (llm_d_epp_maas_fairness_configured_weight{namespace="$ns"})
   and on (fairness_id) (sum by (fairness_id) (rate(llm_d_epp_maas_fairness_sfq_charged_cost_total{namespace="$ns"}[5m])) > 0))
  / ignoring (fairness_id) group_left
sum (max by (fairness_id) (llm_d_epp_maas_fairness_configured_weight{namespace="$ns"})
   and on (fairness_id) (sum by (fairness_id) (rate(llm_d_epp_maas_fairness_sfq_charged_cost_total{namespace="$ns"}[5m])) > 0))
```

Contended fraction of the window (put it on the same panel):

```promql
avg_over_time((sum (vllm:num_requests_waiting{namespace="$ns"}) > bool 0)[5m:15s])
```

To blank the share outside contention, append
`and on () (sum (vllm:num_requests_waiting{namespace="$ns"}) > 0)` to the observed query.

Read it with three caveats:

1. **Contended time only.** With no queue, every group gets what it asks for and the
   share tracks offered load, not the policy. Trust the share only while the contended
   fraction is near 1. The gate uses vLLM's waiting queue rather than this plugin's
   `contended_seconds_total`, because with the stamp on and no EPP hold, flow control
   holds nothing and that counter can read 0 under full saturation.
2. **"Had traffic" is not "backlogged".** A group sending less than its weighted share
   is served in full and correctly sits below the target line. That is water-filling,
   not starvation. Only a group that is persistently backlogged and still below target
   is a defect.
3. **The counter lags.** Cost is booked at completion, so a 5 m window over requests
   that run for minutes is mostly earlier dispatches. Use a window several times the
   pool's p95 request duration. It is in the plugin's cost unit (input + 2 × output,
   with `outputTokenWeight` still uncalibrated), not GPU time.

Rank at a glance:
`sum by (fairness_id) (rate(llm_d_epp_maas_fairness_sfq_dispatched_at_front_total{namespace="$ns"}[5m])) / sum by (fairness_id) (rate(llm_d_epp_maas_fairness_dispatch_total{namespace="$ns"}[5m]))`.
Tag spread: `llm_d_epp_maas_fairness_sfq_lag{namespace="$ns"}` (`F_g − V`, per group) and
`..._sfq_virtual_time`. After an idle reset or threshold rebase every group's
`sfq_finish_tag` / `sfq_lag` gauge is refreshed, not only the dispatching group's.

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

   Secondary: `prefix-cache-scorer` carries the joint-highest profile weight (3.0,
   tied with `queue-scorer` since UNI-214), so the router actively manufactures
   these hits. Hit rates will be high by construction, and
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

   **This POC's own backend never reaches either bucket.** `--max-num-seqs 8` caps
   resident KV at a small, fixed fraction of the pool's real capacity regardless of
   request shape — confirmed, with the exact numbers and what it would take to change,
   in item 14 below.

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

14. **The saturation detector's KV-cache limb has never engaged on this backend, and
    `--max-num-seqs 8` is why — not a scenario-design gap ([UNI-224](/UNI/issues/UNI-224)).**

    `flowControl.saturationDetector`'s `utilization-detector` (`llm-d-router@v0.11.0`'s
    `saturationdetector/utilization/detector.go:160`) is a **roofline over two signals**,
    not queue depth alone:

    ```go
    qRatio  := WaitingQueueSize / QueueDepthThreshold        // we set 32
    kvRatio := KVCacheUsagePercent / KVCacheUtilThreshold    // never set; framework default 0.8
    totalScore := max(qRatio, kvRatio)                       // whichever resource is closer to exhausted
    ```

    Every PASS/FAIL in this POC, and the entire `queueDepthThreshold: 32` calibration
    (item 9's own diagnostic criteria, and [UNI-215](/UNI/issues/UNI-215)/
    [UNI-220](/UNI/issues/UNI-220) above), was decided on the queue limb alone. Measured
    live from Prometheus across the full ~7-hour window covering every UNI-215/UNI-218 run
    (2026-11-10, 411 samples at 60s): `vllm:kv_cache_usage_perc` peaked at **0.0017**
    (ratio to its 0.8 threshold: 0.002) while `vllm:num_requests_waiting` peaked at 178
    (ratio to its 32 threshold: 5.6) — queue wins the `max()` by roughly **1000×**, in
    every run ever scored.

    **Instrumented, not just measured once.** Both ratios are now reconstructed and
    attributed per run in `deploy/poc/15-fairness-report.py`'s `compute_saturation_limb`
    (its own "Saturation limb" report section), from the EPP's own pool-level gauges —
    `llm_d_epp_average_queue_size` and `llm_d_epp_average_kv_cache_utilization`. Both were
    already covered by `snapshot_metrics()`'s `average_` prefix match and already landing
    in every run's `metrics-before.txt`/`metrics-after.txt`/`metrics-timeseries.txt` — the
    gap was that nothing ever divided them by their thresholds or said which one bound.
    `15-fairness-benchmark.sh` now reads both thresholds live from `maas-epp-config` (same
    pattern as the ledger's token weights) and passes them through
    `--queue-depth-threshold`/`--kv-cache-util-threshold`.

    **Is it reachable at all on this backend? No — confirmed, not assumed.** vLLM's own
    engine-startup log states the real number this POC runs against:

    ```
    GPU KV cache size: 1,074,224 tokens
    Maximum concurrency for 8,192 tokens per request: 131.13x
    ```

    With `--max-num-seqs 8` and `--max-model-len 8192` (`deploy/poc/09-vllm-gpu.yaml`), the
    hardest possible resident-KV ceiling is `8 × 8192 = 65,536` tokens — **6.1% of the pool's
    real capacity**, regardless of request shape, prompt length, or output length.
    `kvCacheUtilThreshold`'s default is 0.8: this config cannot reach even a tenth of the
    way there.

    Confirmed live, not just computed: the `kv-cache-fill` scenario
    (`deploy/poc/15-fairness-benchmark.sh`) is a dedicated capacity probe, not a fairness
    scenario — single tenant, 8 workers (exactly `--max-num-seqs`, so no HTTP-side queueing
    dilutes it), a 30-word prompt, and `MAX_TOKENS_MODE=longgen` forcing every request to
    generate the full 8,000 tokens via `min_tokens`/`ignore_eos` rather than stopping at the
    model's own EOS — the combination deliberately engineered to push KV usage as high as
    this config structurally allows. Result (`results/20261112T084754Z-uni-224-kv-cache-fill/`,
    24 requests, 24/24 `200`, 192,000 completion tokens, p50 90.1s/p95 94.9s):

    | signal | peak |
    |---|---|
    | per-replica `vllm:gpu_cache_usage_perc` | 3.7% / 2.7% |
    | pool `llm_d_epp_average_kv_cache_utilization` (EPP's own gauge) | 3.0% |
    | `kvRatio` (peak KV ÷ 0.8 threshold) | **0.0375** |
    | `qRatio` (queue stayed at 0 — no HTTP-side queueing at `workers == max-num-seqs`) | 0.0 |

    3.0-3.7% measured against a 6.1% structural ceiling — the shortfall from theoretical
    maximum is the two replicas' uneven split (5 vs 3 of the 8 workers) and sampling gaps
    in a 10s-interval scrape, not evidence the ceiling is wrong. Either way, **0.0375 is
    roughly 20× below the 1.0 gating value**, and every real contention scenario's queue
    ratio measured so far starts above 1.0 (UNI-215/220's app1-flood: 5.6). On this
    backend, at this config, **the queue limb will always bind first** — this is not a gap
    in scenario design (`max-tokens-skew`/C2 and `near-timeout-long-generations`/C4 were
    never going to show otherwise; UNI-150's own near-timeout notes already record that
    higher concurrency than `--max-num-seqs` allows produces client-side queueing and
    errors, not more resident KV).

    **What would make it reachable.** Reaching `kvRatio = 0.8` needs ~859,000 resident
    tokens. Options, independent of each other:
    - Raise `--max-num-seqs` toward the engine's own reported safe concurrency (131 at
      8,192 tokens/request) — concretely, `--max-num-seqs ~105` at the current
      `--max-model-len 8192` gets there if all slots stay full of max-length requests.
      This is the only one of the three that is also a *production-realistic* tuning
      knob — it directly trades off against the queue limb's own calibration (item 9's
      "Diagnose from vLLM's own metrics, not GPU util" guidance applies directly here:
      watch both ratios together when changing this).
    - Shrink the KV pool itself (`--gpu-memory-utilization` below the live 0.92) so the
      same absolute usage is a larger fraction — cheap to try, but makes queue bind even
      sooner, not a realistic path to isolating the KV limb.
    - Raise `--max-model-len` — needs ~107,000 tokens/request at the current
      `max-num-seqs 8`, technically inside Qwen2.5-7B-Instruct's YaRN-extended range but
      impractical for a benchmark prompt corpus.
    None of these were applied — changing the production-realistic one
    (`--max-num-seqs`) is a scheduling-profile/capacity decision for the board, not a
    unilateral benchmark-harness edit, per this ticket's own instructions.

    **The cost-model comparison stays blocked, as the ticket that raised it already
    expected.** `vramtime` vs. `tokens` (item 9 above) can only diverge from the token
    proxy where KV residency diverges across tenants — at a confirmed sub-4% pool-wide
    peak, no tenant's memory footprint is distinguishable from any other's, so running
    the comparison now would show "no difference" for the wrong reason (nothing bound
    memory) rather than the right one (the models agree). Unblocking it needs the
    `--max-num-seqs` change above applied and re-validated as a real multi-tenant
    scenario, not just this single-tenant capacity probe.

## Worth doing upstream (small, unblocks deleting local copies)

- Export `runPickConformanceTests` into a non-test `fairness/conformance` package.
- Add a `RegisterStrategy` seam to `program-aware` so weighted LAS can be a strategy
  rather than a fork-by-copy.
- Add `metricsutil.PinFairnessID(string)` so configured tenant IDs can't be spilled
  from the label cap.
