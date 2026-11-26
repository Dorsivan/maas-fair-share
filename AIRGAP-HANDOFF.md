# Air-gap handoff guide

**Audience: the agent who receives this repository inside a disconnected network and has
never seen it before.** You have the repository and nothing else. No one who built it is
reachable. This document is the single entry point: it tells you what this is, what has to
exist around it before it can run, what to carry across the boundary, how to deploy it, how
to test it the first time, and which healthy-looking outcomes are actually failures.

Read this top to bottom once before touching the cluster. The order matters more than any
individual command.

> **Status of this snapshot.** Rewritten 2026-11-25 (UNI-303), through main commit
> `7d8ed1d`, on top of
> UNI-293/UNI-299/UNI-300 (the SFQ priority stamp), UNI-302 (its decision log) and UNI-306
> (the `identityHeader` default fix). **The mechanism changed since the previous cut of this
> document (2026-11-11, commit `c8a069d`, UNI-220): read [§2](#2-how-it-works-internally)
> again even if you have read an earlier version.** Dispatch order is now decided by a
> start-time fair-queueing tag stamped into vLLM's own `priority` field, not by the EPP's
> internal queue alone — the EPP-held queue is 6-8% of in-flight requests under the load
> shapes tested here; vLLM's FIFO holds the rest, which is why the earlier, EPP-only
> ordering could not fully move the split.
>
> **The specification question is settled (board ruling, 2026-11-25): proportional share
> under contention is the product — document it as the delivered result, not as a shortfall
> against a floor that was never built.** [§2](#2-how-it-works-internally) states this
> positively, with the live headline number (0.06–0.12 percentage points off target,
> UNI-294, three repeats — `results/UNI-294-INDEX.md` has the full, precisely-sourced
> comparison). A contractual floor is out of scope for this version; it gets one line as
> scope, not a limitations section.
>
> **This repository's `main` and its deployed artifact were out of sync for two weeks**
> before this rewrite: the SFQ stamp code merged to `main` on 2026-11-25, but every deploy
> manifest, and the live cluster, were still pinned to the UNI-220-era image, and the live
> GPU and CPU EPPs were each running a *different*, uncommitted image digest found nowhere
> in this repo — evidence of manual cluster patches never written back. This rewrite
> rebuilt the EPP image from a clean clone of `main`, re-pinned all six manifests, and
> live-verified the new image on both EPP schedulers in `maas-fairness-poc`. See
> `results/20261125T231600Z-uni303-image-rebuild-and-sched-policy-check/README.md` for
> exactly what was and was not re-verified. **Treat any digest cited anywhere else in this
> repository's prose, including older parts of this file, as unverified until you check
> `git log --oneline -- deploy/llmisvc.yaml`.**
>
> `docs/poc-results.md` is the authoritative record of *measurements* made before the
> stamp (everything through UNI-230ish) and is not rewritten here. Two pre-stamp threads
> remain open: a dispatch-accounting gap under an EPP restart for a high-concurrency
> tenant ([UNI-193](/UNI/issues/UNI-193)/[UNI-194](/UNI/issues/UNI-194)), and whether the
> pre-stamp 8x-over-offer correction ceiling needs an admission-side fix. **Not re-verified
> live since the stamp shipped:** an end-to-end fairness run with `sfqPriorityStamp: true`
> and `--scheduling-policy priority` against real contended GPU traffic. The stamp's
> correctness is proven by the unit/sim suite (`sfq_sim_test.go`, `sfq_test.go`) and by an
> earlier live session (tag `uni294-sfq-live`, not reproducible from a committed manifest);
> this rewrite's own live check only confirms the image boots clean and vLLM accepts the
> scheduling flag, not that the stamp moves a live split. Do that run before trusting a
> share number against this image on your cluster.

---

## Table of contents

| § | |
|---|---|
| [1](#1-what-this-repository-is) | What this repository is |
| [2](#2-how-it-works-internally) | How it works internally |
| [3](#3-orientation--which-document-answers-which-question) | Orientation — which document answers which question |
| [4](#4-what-must-already-exist-on-your-side) | What must already exist on your side |
| [5](#5-transfer-manifest--what-crosses-the-boundary) | Transfer manifest — what crosses the boundary |
| [6](#6-blocking-items) | Blocking items |
| [7](#7-deploy-in-order) | Deploy, in order |
| [8](#8-initial-test-the-six-rung-ladder) | Initial test: the six-rung ladder |
| [9](#9-failures-that-look-like-success) | Failures that look like success |
| [10](#10-what-is-and-is-not-proven) | What is and is not proven |
| [11](#11-changing-it) | Changing it |
| [12](#the-weight-split-checker) | The weight-split checker |

---

## 1. What this repository is

A **fairness policy plugin for the llm-d Router (EPP)**. It guarantees each MaaS
subscription a minimum share of a shared model's token throughput **when the model is
saturated**, and imposes no limit at all when it is not.

The problem it solves is one a rate limiter structurally cannot. A `MaaSSubscription`
becomes a Kuadrant `TokenRateLimitPolicy`, which is a **hard ceiling that applies always** —
at 3am on an idle GPU, app1 is still cut off at its limit. What is wanted is the opposite: a
floor under contention, and no ceiling otherwise.

- A **rate limiter** says *"you may not exceed X"* — always on, wastes idle capacity.
- A **queue** says *"when there is a line, here is who goes next"* — inert until there is
  actually contention.

This repository builds the queue. **Kuadrant stays.** The two are complements: the ceiling
bounds what anyone may consume; this divides what is available when they compete for it.

What it can and cannot promise:

- ✅ "Under contention, app1 receives at least 20% of delivered throughput."
- ❌ "app1 is guaranteed 20,000 tokens/second."

Capacity loss lowers everyone's absolute throughput together — the *ratio* holds, the
*floor* does not. A tenant that sends no traffic receives nothing; capacity cannot be
reserved for requests that have not arrived.

---

## 2. How it works internally

### Where it sits in the request path

```
client
  → OpenShift Gateway (Envoy)
      → Kuadrant        authenticates, applies the MaaSSubscription ceiling
      → EPP             ← THIS PLUGIN
          → vLLM pods
```

llm-d's flow-control subsystem already maintains one queue per tenant and already decides
when a slot is free. The one thing it delegates is *which tenant's queue goes next* — a
`FairnessPolicy`. That single decision is this plugin.

### Why it ships as a whole image, not a plugin file

**EPP plugins are compiled in. There is no dynamic loading.** So `Dockerfile.epp` builds a
complete, standalone EPP — the full upstream `llm-d-router` v0.11.0 binary plus one
registered policy — and lands it at `/app/epp`, the exact path the KServe preset's templated
command invokes. Deployment overrides only `image:`, never `command`/`args`.

Two consequences you must internalise:

1. **The platform's own EPP version does not gate this.** RHOAI 3.4 ships an EPP with no
   flow-control subsystem at all, which looks like a hard blocker. It is not, because we
   replace that container wholesale.
2. **A code change means a rebuilt image.** There is no config-only path to changing policy
   behaviour. See [§11](#11-changing-it).

### The algorithm

**What decides dispatch order today: a start-time fair-queueing (SFQ) priority stamp,
not the EPP's own queue.** UNI-288 (`docs/design.md`, "UNI-293: SFQ priority stamp")
measured the EPP holding only 6-8% of in-flight requests under closed-loop load; vLLM's own FIFO
waiting queue held the other ~88-94% and decided the real dispatch order regardless of
what the EPP's internal ranking said. Reordering only the EPP's own small queue could
never move the split by more than that 6-8%. **UNI-293 fixes this by moving the decision
to where the requests actually are**: the plugin computes an SFQ start tag per request and
stamps it into the request body as vLLM's own `priority` field (`PreRequest` →
`MutatePayloadMap`). vLLM, run with `--scheduling-policy priority`, reorders its waiting
queue by that stamped integer. The EPP's internal queue ranking by the tab (below) still
runs, but on this small a queue it is now a secondary effect, not the mechanism.

**The tag.** Group `g` with weight `w` dispatching a request with estimated cost `c` gets
start tag `S = max(F_g, V)`, then `F_g += c/w`. `V` is the minimum, over currently-serving
endpoints, of each one's newest stamped start — not a wall-clock time. Equalising each
group's rate of advancing `F_g` relative to `w` *is* proportional sharing, so the ratios
converge on the configured weights without any constant describing how fast the GPUs are.
At completion, `F_g` is trued up by `(actual − charged)/w`, **undecayed** — this closes a
gaming vector where an under-estimated request would otherwise pay less than it cost, which
the plugin's older, decayed true-up could not fully close. Full derivation, the virtual-time
definition, the ceiling/rebase mechanism, and the idle-reset rule:
`docs/design.md`, "UNI-293: SFQ priority stamp" and "UNI-300" review.

**Three non-negotiables, each a silent-failure mode if missed:**

1. **`propagatePriority` must stay `false`** (`router.scheduler`'s `requestHandler` setting,
   not a `maas-fairness` plugin parameter). It runs *after* `PreRequest` and overwrites the
   stamped `priority` with the InferenceObjective's static priority, silently reverting the
   whole mechanism with no error. The plugin refuses to start if it is `true` — it re-reads
   the EPP's own `--config-file`/`--config-text` to check — **or if it cannot find the
   setting to check at all**, so do not suppress that startup check.
2. **vLLM must run `--scheduling-policy priority`.** Without it, a stamped `priority` field
   is simply ignored and dispatch stays FIFO. Verified live in this environment
   (`results/20261125T231600Z-uni303-image-rebuild-and-sched-policy-check/`) that this RH
   vLLM build (`0.24.0+rhaiv.9`) accepts the flag.
3. **The plugin, not the client, owns `priority`.** With the stamp on, every request's
   `priority` is overwritten unconditionally, including unclassified groups and a client
   that already set one — a client-supplied value is never honoured. With the stamp off, a
   client-supplied `priority` is stripped (not forwarded), so it is a no-op under plain
   FIFO either way. A request body the plugin cannot rewrite (non-JSON) is rejected (400),
   never forwarded unstamped.

**The EWMA tab still exists, underneath the stamp, for a different job: accounting.**
Each group still carries a decaying *tab* of consumed tokens, decayed `2^(-Δt/halfLife)`.
With `sfqPriorityStamp: true`, `Pick` ranks the EPP's own small queue by SFQ tag, not by
the tab — the tab is charged and decayed only for `normalized_service`, the flight
recorder, and the live state dump. Two of the three stabilising mechanisms below are
**inert** once the stamp is on, because `max(F_g, V)` already does their job exactly; they
are kept because their *absence* would reopen the vector they close if the stamp is ever
turned back off:

- **Exponential decay** — the tab measures *recent* usage, not all-time. Still active;
  shapes only the accounting series, not dispatch, once the stamp is on.
- **Newcomer clamp** — raises a returning-idle tenant to the current minimum so it goes
  first *once* rather than monopolising the pool. **Inert when `sfqPriorityStamp` is on**
  — it writes only to the tab, which no longer drives `Pick`. Leave it `true` regardless;
  it is the thing that matters if the stamp is ever disabled.
- **Provisional charge** — an estimate is charged at dispatch and trued up against the real
  `usage` block at completion. **Still load-bearing with the stamp on** — the SFQ tag's
  completion true-up (above) depends on provisional charging having happened at dispatch.
  Generations take 10–30s while scheduling decisions happen every millisecond; without
  this a tenant dispatches thousands of requests before any lands on its tag.

**The semantics, stated as the agreed product (board ruling, 2026-11-25): proportional
share under contention is what this delivers, and it is what was asked for.** Under
contention, each tenant converges to its configured weight's share of weighted token
cost — that is the promise, stated plainly, not hedged. Measured live at
**0.06–0.12 percentage points off target**, across three repeated runs, on a scenario
with equal offered worker counts per tenant — so the result tracks the policy, not the
load shape (UNI-294; `results/UNI-294-INDEX.md` has the full comparison, including a
fourth run with the same EPP-side config that missed by 32.5 points — read it before
citing these numbers). Properties that might read as caveats are the documented design,
not shortfalls:

- Share is *relative to who else is contending* — a tenant at weight 10 gets roughly 10.5%
  of the pool against two active rivals, and roughly 33% against one. It is not a quota
  carved out of the whole pool regardless of who else is running.
- The controller averages over a 60-second half-life ([§11](#11-changing-it)), so it is a
  converging guarantee over that timescale, not an instantaneous one.
- Share is measured, and only means something, over **contended** time — an idle pool
  imposes no limit on anyone, by design (that is what distinguishes this from a rate
  limiter; [§1](#1-what-this-repository-is)).
- Shares cannot be oversold: 20+10+65+5 sums to 100, unlike a set of independent SLAs.

**A contractual floor — a guarantee that holds even absent contention or across arbitrary
short windows — is an explicit non-goal for this version.** It is mentioned here once, as
scope, not as a defect or a gap to apologize for.

### How a request is attributed to a group

Grouping happens before the FlowKey. The gateway sets `x-gateway-inference-objective` per
ServiceAccount; the plugin matches it against the group table in `maas-epp-config` (exact
match beats prefix), and anything unmatched lands in `unclassified`.

**This is a security boundary, not just a lookup.** A client can forge
`x-llm-d-inference-objective`, which beats the gateway's own header unless the gateway
overwrites it too. The AuthPolicy patch in
`deploy/maas/09-objective-header-stripping.patch.yaml` is what closes that, and
[§9](#9-failures-that-look-like-success) explains why skipping it produces a cluster that
reports healthy while admitting forged priority bands.

### Source layout

```
cmd/epp/main.go           register the plugin, hand off to the upstream runner
pkg/fairness/weightedlas/ the plugin -- policy, state, grouping, cost model, metrics
cmd/gateway-header-check/ standalone conformance checker (VENDORED -- builds offline)
conformance/gatewayheaders/
                          the check's library + testdata (VENDORED)
deploy/                   EndpointPickerConfig, LLMInferenceService, PodMonitor, RBAC
deploy/poc/               the test rig: direct EPP, simulator, benchmark harnesses
deploy/maas/              Models-as-a-Service install (Kuadrant, TLS, DB, gateway)
deploy/logging/           applyable manifests for the Logging/Loki install spec
docs/                     design, results, runbook, calibration, version pinning
prototype/                FROZEN Python ext_proc prototype -- provenance, NOT a dependency
results/                  775 committed run artifacts, 282 MB (see transfer note, §5)
```

`prototype/` is design provenance only. It is not built, not deployed, and not maintained.
Do not treat anything in it as a dependency.

---

## 3. Orientation — which document answers which question

The repository carries well over 18,000 lines of documentation (check with `wc -l docs/*.md
AIRGAP-HANDOFF.md` — it grows fast and any count written here will be stale soon). You do
not need to read it all. Go to the one that answers your question:

| Your question | Document |
|---|---|
| **Is the configured split actually being honoured, right now, on my endpoint** | `deploy/poc/weight-split-check.py` ([§12](#the-weight-split-checker)) — a standalone script, run it, don't read about it first |
| Why does this exist, what are the design decisions, and what decides dispatch order **today** | `docs/design.md` — read the banner at the very top first, it tells you which sections are current and which are historical narrative |
| What was measured, on what hardware, and what the numbers were (through UNI-230ish; **not** updated for the SFQ stamp) | `docs/poc-results.md` — the pre-stamp evidence record |
| How do I actually run a thing on the cluster | `docs/runbook.md` (task-indexed, start from its headings) |
| What version is pinned, why, and how do I bump it | `docs/version-pinning.md` |
| `outputTokenWeight` is 2.0 — what do I set it to here | `docs/calibrating-output-token-weight.md` ← **you must do this** |
| How does header forgery work and how is it closed | `docs/gateway-header-stripping.md` |
| What do the EPP log lines mean, including the SFQ decision log | `docs/log-field-contract.md`, `docs/logql-queries.md` |
| How do I install Logging + LokiStack (optional) | `docs/logging-install-spec.md` |
| How do I install MaaS itself | `deploy/maas/README.md` |
| What did the Python prototype prove, and why was it replaced | `prototype/README.md` |

`docs/poc-results.md` is organised by ticket (UNI-nnn). If you are chasing why a particular
scenario behaves as it does, search that file for the scenario name
(`full-contention`, `app2-trickle`, `below-capacity`, …) rather than reading linearly.

---

## 4. What must already exist on your side

This plugin is a **component inside a stack**. It cannot be deployed standalone, and most
first-time failures are a missing layer below it, not a problem with the plugin. Confirm
each of these before you start.

### Required

| Layer | What is required | How this POC had it | Check |
|---|---|---|---|
| OpenShift | 4.20+ | 4.20.35 | `oc get clusterversion` |
| RHOAI / OpenShift AI | 3.4.x or 3.5+, with KServe and the `LLMInferenceService` CRD | operator CSV `rhods-operator.3.4.4` over a 3.5.0 KServe data plane (see note) | `oc get crd llminferenceservices.serving.kserve.io` |
| KServe LLM presets | `*-kserve-config-llm-scheduler`, `-llm-router-route`, `-llm-template` | `v3-5-0-kserve-config-*` | `oc get cm -A \| grep kserve-config-llm` |
| Gateway API | a `GatewayClass` with an Envoy-backed controller | `data-science-gateway-class`, controller `openshift.io/gateway-controller/v1` | `oc get gatewayclass` |
| Kuadrant | Kuadrant / Red Hat Connectivity Link, with Authorino + Limitador | `rhcl-operator` v1.3.4 in namespace `connectivity-link` | see trap below |
| User Workload Monitoring | enabled — MaaS reports `Degraded` without it | merged into `cluster-monitoring-config` | `oc -n openshift-monitoring get cm cluster-monitoring-config -o yaml` |
| An internal container registry | reachable from **every** node that will run a pod | OpenShift internal registry + Quay | §9, trap 2 |
| An internal model store | S3-compatible, OCI artifact, or PVC — **HuggingFace will not be reachable** | `hf://` (does not transfer — see §6) | — |

> **Kuadrant trap.** Grepping CSVs for "kuadrant" finds nothing when it is installed as
> `rhcl-operator`, which makes it look absent. Check for the CRDs and the controllers in
> `connectivity-link`, not for the name.

> **The RHOAI version note.** The cluster this was built on was not a clean install: the
> operator was 3.4.4 while the KServe control plane was left over from 3.5.0, so every
> result in `docs/poc-results.md` was produced against a **3.5.0 KServe data plane**. 3.4
> compatibility rests on a flag-level test (`deploy/poc/06-rhoai34-shape.yaml`) plus source
> and image-label inspection, not on a run against a coherent 3.4 stack. If your side is a
> real 3.4 cluster, you are testing something this POC never could — see
> [§10](#10-what-is-and-is-not-proven), items 1–3.

### Required only for the GPU path

| Layer | Note |
|---|---|
| NVIDIA GPU Operator + Node Feature Discovery | **Set `deviceLabelFields: [vendor]` on the NodeFeatureDiscovery CR.** With the default `[vendor, device]` it emits `pci-10de_20b5.present` while the GPU operator selects on the vendor-only `pci-10de.present`, so the operator logs "No GPU node found" indefinitely, creates zero daemonsets, and the cluster reports no `nvidia.com/gpu` capacity at all. This cost three weeks here and looks exactly like broken hardware. |
| ≥2 GPUs | Two replicas, one per GPU. With a single pod the endpoint picker is a no-op and any endpoint-selection bug stays hidden. |
| A vLLM build that accepts `--scheduling-policy priority` | **Required for the SFQ stamp to do anything** ([§2](#2-how-it-works-internally)). Confirmed on `registry.redhat.io/rhaii/vllm-cpu-rhel9:3.5.0` (`vllm==0.24.0+rhaiv.9`): the flag is accepted as a non-default arg and the pod boots healthy. Not yet confirmed on the GPU image from this same preset — it is the same vLLM version, but confirm on your own build before relying on it. Safe to add even before you are ready to enable the stamp: with no `priority` stamped, every request ties at the default and dispatches FIFO, identical to not setting the flag at all. |

### Optional

- **Logging + LokiStack** for the flight-recorder log tier — `docs/logging-install-spec.md`,
  which carries its own nine-image mirror set. Not required for the fairness result.
- **Grafana** for the dashboard in `deploy/grafana-dashboard.yaml`.

---

## 5. Transfer manifest — what crosses the boundary

Every external dependency, with a verdict. `mirrorable` = copyable as bytes;
`internally-replaceable` = an equivalent must exist inside and is named;
`blocking` = no internal equivalent, cannot transfer as designed.

### 5.1 Container images

| Item | Verdict | Evidence / note |
|---|---|---|
| `quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537` — **the EPP image pinned in this repo's manifests as of UNI-309** | mirrorable, **but see §6.1** | Built from commit `6e49e0c` (`main` tip at the time of the UNI-309 rebuild — includes UNI-302's decision log/rank/live-share and the UNI-290-composition merge, test-only), published via the `maas-epp-quay-publish` BuildConfig from a **clean clone**, not a working tree that may carry another session's uncommitted edits (see [§9](#9-failures-that-look-like-success), the shared-checkout item). **This digest DOES contain UNI-302**, so `sfqDecisionLog` can be set against it without crash-looping (strict decoding; see [§11](#11-changing-it)) — it is still committed `"off"` in `deploy/poc/00-config.yaml`, which also now carries `sfqPriorityStamp: true` for the first time (previously only `deploy/epp-config.yaml`'s production template had the key; the POC config never did). This is at least the seventh re-pin since UNI-29's original `fc27130` build — each code change to the plugin forces a rebuild; **check `git log --oneline -- deploy/llmisvc.yaml` before trusting any digest cited anywhere in this repository's prose, including this one, and distrust any digest you find live on the cluster that does not also appear in a commit here**. The Quay repository is **private**: an anonymous pull token is issued but the manifest GET returns `UNAUTHORIZED`, so it cannot be mirrored without the robot credential. |
| `gcr.io/distroless/static:nonroot` | mirrorable | Runtime base, via `ARG BASE_IMAGE` in `Dockerfile.epp`. **Floating tag** — resolve to a digest before mirroring. |
| `golang:1.26.8` | mirrorable | Builder image. Needed only if you rebuild. Must be **≥** the `go` directive in upstream's go.mod (currently `go 1.26.6`). **Floating tag.** |
| `registry.redhat.io/rhaii/vllm-cpu-rhel9:3.5.0` | mirrorable | CPU inference path. Version tag, not a digest. |
| `ghcr.io/llm-d/llm-d-inference-sim:v0.11.4` | mirrorable | Simulator backend for the GPU-free rig. Referenced from three manifests. Version tag, not a digest. |
| `registry.redhat.io/rhel9/postgresql-15:latest` | mirrorable | MaaS scaffolding DB. **`:latest`** — pin before mirroring. |
| `registry.access.redhat.com/ubi9/ubi:latest` | mirrorable | Load-generator and cache-profile job base. **`:latest`** — pin before mirroring. |
| The GPU vLLM runtime image | internally-replaceable | Templated by the RHOAI preset `v3-5-0-kserve-config-llm-template`, not named in this repo. It comes from your RHOAI mirror, not from here. |
| RHOAI, Kuadrant/RHCL, MetalLB, NVIDIA GPU Operator, NFD operator images + catalog | internally-replaceable | Platform layer. Mirrored by your OpenShift disconnected-install process, not by this repo. |
| Logging/Loki mirror set — nine images plus `registry.redhat.io/redhat/redhat-operator-index@sha256:12cffb23d6519909c78a175bc862cbdeae521ff6032099f3628457936c6f4119` | mirrorable | Enumerated in `docs/logging-install-spec.md`. **Optional** — skip entirely if you are not doing the log tier. |
| `python:3.11-slim`, `envoyproxy/envoy:v1.31-latest` | N/A — do not transfer | `prototype/` only. Frozen provenance, not a deliverable. |

`docs/version-pinning.md` §2.3 holds the same inventory line-referenced to each manifest,
and §4 holds the digest rule these floating tags violate. The violations are known and
tracked; they are not discoveries you need to re-report, but **you should resolve each
floating tag to a digest as you mirror it**, because on your side "latest" means "whatever
was in the tarball", which is worse than a pin — it is a pin nobody wrote down.

### 5.2 The model

| Item | Verdict | Evidence |
|---|---|---|
| `hf://Qwen/Qwen2.5-7B-Instruct` (`deploy/poc/09-vllm-gpu.yaml`, `spec.model.uri`) | **blocking as written** — see [§6.2](#62-the-model-uri-is-a-runtime-call-to-huggingface) | The KServe storage-initializer resolves this **at pod start**, over the internet. ~15 GB of weights. Open weights, no gating (Llama-3.1-8B-Instruct was tried and is gated — it fails in the storage-initializer with an opaque 401). |

### 5.3 Language packages and build tooling

| Item | Verdict | Evidence |
|---|---|---|
| Go modules for the root module — `github.com/llm-d/llm-d-router v0.11.0` + ~400 transitive | mirrorable, **action required** | **The root module is NOT vendored.** There is no `vendor/` at the repository root, so `go build ./cmd/epp` needs a populated `GOMODCACHE` or an internal Go module proxy (Artifactory/Nexus/Athens). 114 entries in the `require` blocks; ~400 in the full graph, because importing `cmd/epp/runner` pulls essentially the whole EPP graph. |
| `cmd/gateway-header-check` and `conformance/gatewayheaders` | **already mirrored** | Both carry their own `vendor/` trees and their own `go.mod`. They build with **no network and no module cache** — this is deliberate, and it is why the conformance check is usable on your side on day one. See `docs/gateway-header-stripping.md`, "Building this check air-gapped". |

Both claims above were re-verified for this transfer, on 2026-11-02 with go1.27.2:

```
# checker: builds with the proxy off, from vendor/ alone
cd cmd/gateway-header-check && GOPROXY=off GOFLAGS=-mod=vendor go build -o /tmp/ghc .
  -> succeeds, 4.7 MB binary

# root module: no vendor/ tree exists
GOFLAGS=-mod=vendor GOPROXY=off go build ./cmd/epp
  -> "inconsistent vendoring ... not marked as explicit in vendor/modules.txt"
GOPROXY=off GOMODCACHE=<empty> go build ./cmd/epp
  -> "go: downloading github.com/llm-d/llm-d-router v0.11.0 ..." and fails
```
| Go toolchain ≥ 1.26.6 | mirrorable | Only needed if you rebuild the image or the checker. A prebuilt image removes the first need; the vendored checker removes the second. |
| `fastapi`, `uvicorn`, `grpcio`, `grpcio-tools`, `pyyaml` | N/A — do not transfer | `prototype/` only. |
| `python3` + `oc` on the operator's PATH | internally-replaceable | Every harness script needs both. `deploy/poc/15-fairness-report.py` uses the standard library only — no pip install. |

### 5.4 Runtime API calls made by the deployed artifact

This is the category that decides portability, so it was walked explicitly.

| Call | Verdict | Evidence |
|---|---|---|
| EPP → Kubernetes API (watch InferencePool, EndpointSlices) | internally-replaceable | In-cluster, `kubernetes.default.svc`. RBAC in `deploy/rbac.yaml`. |
| EPP → vLLM pods | internally-replaceable | Pod-to-pod, in-cluster. |
| Envoy/Gateway → EPP (ext_proc gRPC :9002) | internally-replaceable | In-cluster. |
| Prometheus → EPP `/metrics` :9090 | internally-replaceable | In-cluster, via `deploy/podmonitor.yaml`. |
| Load generator → gateway | internally-replaceable | `deploy/poc/04-loadgen.yaml` targets the in-cluster ClusterIP: `http://maas-poc-gateway-data-science-gateway-class.maas-fairness-poc.svc.cluster.local`. Pure `curl`; no external host, no package install at job start. |
| Key minting → `maas-api` | internally-replaceable | `deploy/maas/mint-loadgen-keys.sh` hits the in-cluster ClusterIP of `svc/maas-api` in `redhat-ods-applications` on :8443. No port-forward, no external endpoint. |
| **KServe storage-initializer → `huggingface.co`** | **blocking as written** | The one runtime call that leaves the cluster. [§6.2](#62-the-model-uri-is-a-runtime-call-to-huggingface). |

**Finding: apart from the model fetch, the running artifact makes no call outside the
cluster.** The plugin itself contacts nothing external — no telemetry, no license check, no
callback. That is the substantive portability result in this review.

### 5.5 Identity and credentials

| Item | Verdict | Note |
|---|---|---|
| MaaS `sk-oai-…` API keys | internally-replaceable | Minted **on your side**, by your MaaS install, via `deploy/maas/mint-loadgen-keys.sh`. No key crosses the boundary, and none is committed. |
| Service CA / ingress CA | internally-replaceable | Cluster-local. Note the reencrypt-Route gotcha in `docs/logging-install-spec.md` §7: the Route presents the **ingress** wildcard cert, not one signed by the service CA, so `service-ca.crt` fails verification there. |
| Quay robot credential for the EPP image | **blocking for mirroring** | [§6.1](#61-the-epp-image-lives-in-a-private-quay-repository). |
| No OIDC issuer, external IdP, or token service outside the cluster | — | Walked and found none. |

### 5.6 Repository size

A clone is ~60 MB of git objects, but the working tree is 491 MB: **775 files / 282 MB
under `results/`**, mostly EPP container logs (the largest single file is 32 MB). These are
committed evidence for `docs/poc-results.md`, not inputs to anything you will run.

`results/` is listed in `.gitignore` and has been force-added on every run since UNI-128;
UNI-172 is open against that and is **not** yours to resolve. For transfer: carry the full
history if you need the evidence trail, or `git clone --depth 1` if you only need to deploy.
Nothing in `results/` is read by any script in `deploy/`.

---

## 6. Blocking items

Two. Both have a known unblock; neither is a design flaw in the plugin.

### 6.1 The EPP image lives in a private Quay repository

**Finding.** `quay.io/rh-ee-dsivan/maas-fair-share` does not permit anonymous pulls. A
registry auth token is issued, then the manifest GET for the digest currently pinned
(`sha256:d496a0cf…`, see [§5.1](#51-container-images) — **confirm the live digest with
`git log --oneline -- deploy/llmisvc.yaml` before mirroring; it has moved at least seven times
since this repository's first Quay publish and will move again**) returns `UNAUTHORIZED`. An
air-gapped mirror run without the robot credential will fail on the one image that *is*
the deliverable, and it will fail at mirror time, not at deploy time.

**Unblock — one of:**

1. **Export before transfer** (preferred). On the connected side, with the Quay robot
   credential:
   ```sh
   skopeo copy --all \
     docker://quay.io/rh-ee-dsivan/maas-fair-share@sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537 \
     dir:/transfer/maas-fair-share-epp
   ```
   Carry the directory; load it with `skopeo copy dir:… docker://<internal-registry>/…`.
   Verify the digest is unchanged after the load — that is the whole point of having one.
2. **Rebuild on your side** from this source tree. This needs the Go module cache
   ([§5.3](#53-language-packages-and-build-tooling)) and the two base images, and it
   produces a **different digest**. If you rebuild, record your digest and update the six
   manifests; do not leave them pointing at a digest your registry does not have. **Build
   from a clean clone, not a working tree someone else may be editing** — a binary
   `BuildConfig` upload sends whatever is on disk, committed or not, and this repository's
   own checkout is sometimes shared across concurrent sessions.

`docs/runbook.md`, "Rebuild and publish the EPP image", covers both the normal build and
the in-cluster BuildConfig path used when no local podman is available.

### 6.2 The model URI is a runtime call to HuggingFace

**Finding.** `deploy/poc/09-vllm-gpu.yaml` sets `spec.model.uri: hf://Qwen/Qwen2.5-7B-Instruct`.
The KServe storage-initializer resolves this **when the pod starts**, reaching
`huggingface.co`. In a disconnected network the init container fails and the model server
never starts. This is the one runtime external call in the whole artifact.

**Unblock.** Stage the weights internally and change the URI. KServe supports
`s3://`, `pvc://`, and OCI-artifact URIs; pick whichever your platform already runs — an
internal MinIO or ODF bucket is the usual answer, and this POC already ran MinIO for the
logging store, so the pattern exists here.

```yaml
# deploy/poc/09-vllm-gpu.yaml
spec:
  model:
    uri: s3://<your-internal-bucket>/Qwen2.5-7B-Instruct   # was hf://Qwen/Qwen2.5-7B-Instruct
    name: llama-3-1-8b
```

Leave `name:` alone unless you also update the group tables and the loadgen — it is the
model name clients send, and it is deliberately not the directory name.

**Any open-weights model will do.** Nothing in the plugin is model-specific; the model
only has to saturate. But two things move with the model and must be re-derived on your
side: `outputTokenWeight` ([§8](#8-initial-test-the-six-rung-ladder), rung 0) and the
saturation point your load generator must exceed.

> **Not a blocker, but adjacent:** `spec.model.name` is `llama-3-1-8b` while the weights are
> Qwen2.5-7B-Instruct. That mismatch is intentional in the source cluster and harmless, but
> it will confuse you later if you do not know it now.

---

## 7. Deploy, in order

Each phase is a prerequisite for the next. Skipping one inside 7.2 leaves MaaS `Degraded`
rather than failing loudly.

Set `NAMESPACE=maas-fairness-poc` unless you have a reason not to; the manifests hardcode
it, and changing it means editing every file in `deploy/`.

### 7.1 — Load the images

Mirror everything from [§5.1](#51-container-images) into your internal registry, resolving
each floating tag to a digest as you go. Then update the image references in `deploy/` to
point at your registry. Six manifests carry the EPP digest:

```
deploy/llmisvc.yaml                deploy/poc/02-epp.yaml
deploy/poc/05-llmisvc-sim.yaml     deploy/poc/06-rhoai34-shape.yaml
deploy/poc/07-vllm-cpu.yaml        deploy/poc/09-vllm-gpu.yaml
```

Confirm the registry is reachable **from every node that will schedule a pod**, not just
from one. See [§9](#9-failures-that-look-like-success), trap 2 — this exact check is the one
that was skipped here, and the consequence was a load run that looked perfect and measured
nothing.

### 7.2 — Install MaaS

Full detail and per-step rationale in `deploy/maas/README.md`.

```sh
oc apply -f deploy/maas/01-kuadrant.yaml      # Kuadrant CR -> Authorino + Limitador
bash     deploy/maas/02-authorino-tls.sh
oc apply -f deploy/maas/03-postgres.yaml      # throwaway DB + maas-db-config secret
oc apply -f deploy/maas/04-gateway.yaml       # maas-default-gateway
bash     deploy/maas/05-enable-maas.sh        # modelsAsService: Managed
```

Verify before continuing — `Ready=True Reconciled` on the Tenant is the real signal:

```sh
oc get crd | grep maas.opendatahub.io       # expect 5
oc get tenants.maas.opendatahub.io -A       # default-tenant
oc get dsc -o jsonpath='{.items[0].status.conditions[?(@.type=="ModelsAsServiceReady")]}'
```

> **If your Gateway sits at `EXTERNAL-IP <pending>`** it is almost certainly a missing
> MetalLB `IPAddressPool`/`L2Advertisement`. This does **not** break MaaS — the Tenant still
> reports `Ready=True`. `deploy/maas/README.md` lists four access options, cheapest first;
> the tests here used ClusterIP.

### 7.3 — Stage the model and deploy the inference service

Resolve [§6.2](#62-the-model-uri-is-a-runtime-call-to-huggingface) first, then:

```sh
oc apply -f deploy/epp-config.yaml            # ConfigMap maas-epp-config: groups + weights
oc apply -f deploy/rbac.yaml                  # incl. the /metrics reader the harnesses mint
oc apply -f deploy/poc/09-vllm-gpu.yaml       # GPU path
#   ... or deploy/poc/07-vllm-cpu.yaml        # CPU path, no GPU required
#   ... or deploy/poc/05-llmisvc-sim.yaml     # simulator, no model at all
```

**Start with the simulator if your model store is not ready.** `05-llmisvc-sim.yaml` runs
the real EPP and the real gateway against `llm-d-inference-sim`, which needs no weights and
no GPU. It will not give you a credible fairness measurement, but it proves the plugin
loads, classifies, and emits metrics — and it unblocks rungs 2 and 3 of
[§8](#8-initial-test-the-six-rung-ladder) weeks before the GPU path is ready.

Three vLLM flags are **hard prerequisites** on any real-vLLM path. All three default off.
The first two fail silently — you get a working-looking deployment whose usage accounting
is empty. The third is inert, not silent-wrong, when missing: without it a stamped
`priority` is simply not honoured and dispatch stays FIFO, which is the same behaviour as
`sfqPriorityStamp: false`, so it will not mislead you on its own — but it is required
before the SFQ stamp ([§2](#2-how-it-works-internally)) can ever do anything, so set it now
rather than rediscovering it when flipping `sfqPriorityStamp` later does nothing:

```yaml
args:
  - --enable-force-include-usage
  - --enable-prompt-tokens-details
  - --scheduling-policy
  - priority
```

Deploy manifests here already include all three. **If you are instead patching an
*existing, already-running* GPU deployment** (not a fresh install) **to add this flag,
read the warning in [§7.3b](#73b--enabling-the-sfq-priority-stamp) first** — on a GPU pool
with no spare capacity, this triggers a rolling-update deadlock.

### 7.3b — Enabling the SFQ priority stamp

Shipped **off** (`sfqPriorityStamp: false`), same shadow-first convention as `enforce`.
Turning it on is a deliberate, separate step from the base install above, not something to
do on day one. In order:

1. **Confirm `requestHandler.propagatePriority` is not set to `true`** on the
   `LLMInferenceService`'s `router.scheduler` (it is unset/`false` by default in every
   manifest here). If it is `true`, the plugin will refuse to start once you flip the next
   step — that is deliberate, not a bug to work around.
2. **Confirm `--scheduling-policy priority` is on the vLLM container** ([§7.3](#73--stage-the-model-and-deploy-the-inference-service)
   above). Flipping the plugin flag with this missing produces silence, not an error: the
   plugin stamps `priority`, vLLM ignores it, dispatch stays FIFO, and nothing in the logs
   says why.
3. **Set `sfqPriorityStamp: true`** in `maas-epp-config` (and, if you want the closed
   gaming-vector fix, `undecayedTrueUp: true` alongside it — see `docs/design.md`,
   "UNI-293: SFQ priority stamp"). **This recreates the EPP pod and zeroes its counters**,
   the same as flipping `enforce` does ([§8](#8-initial-test-the-six-rung-ladder), Rung 5)
   — take any metrics snapshot you need before this step, not after.
4. **If you are updating an existing GPU deployment rather than installing fresh, expect
   the rollout to deadlock — unless you first confirm there is really no spare GPU.** An
   LLMInferenceService edit that changes the vLLM container's args triggers the controller
   to roll its owned Deployment at the default 25%/25% surge/unavailable. On a 2-GPU pool
   already running 2 replicas with zero spare GPU *capacity*, the surge pod cannot
   schedule and the rollout hangs indefinitely with one old pod and one new, both
   counted, neither fully up.
   **"Allocated" is not the same as "needed."** On this cluster, three lanes nominally
   claimed all 6 GPUs, but checking pod age and last-loadgen timestamp
   (`oc get pods`, job history) found two of the three lanes had been idle for days —
   the capacity existed, it just was not freed. Check this before assuming you are stuck:
   a lane with no recent traffic can be scaled to 0 to free real headroom, with board
   sign-off if the lane belongs to someone else's in-progress work. **This exact
   situation — rebuilding at current `main`, re-pinning, and redeploying all three lanes
   onto the stamp — is tracked as [UNI-309](/UNI/issues/UNI-309) (critical), not owned by
   this document.** If you are doing this for the first time, check UNI-309's outcome and
   its resulting digest before repeating the work.
   If you do need the manual path: `oc get rs -n <namespace> -l <the Deployment's
   selector>`, identify the **old** ReplicaSet (lower `kubectl.kubernetes.io/revision`
   annotation), and `oc scale rs <old-rs> --replicas=<n-1>` to free a GPU for the new pod
   — do **not** patch the generated Deployment's strategy directly, the controller
   reverts it. This is a temporary capacity dip on your own deployment during the
   rollout, not a destructive action, but budget for it before doing this during a
   measurement window.
5. **Confirm the stamp is landing** before trusting any share number — [§8](#8-initial-test-the-six-rung-ladder),
   new Rung 6, below.

### 7.4 — Close the header-forgery hole

`odh-model-controller` only generates the per-Gateway AuthPolicy once an
`LLMInferenceService` referencing the Gateway exists, so this comes **after** 7.3 — there is
nothing to patch before that.

```sh
oc patch authpolicy maas-poc-gateway-authn -n maas-fairness-poc --type=merge \
  --patch-file=deploy/maas/09-objective-header-stripping.patch.yaml
```

Safe to re-run; it is a merge patch. Then prove it, with the vendored checker that needs no
network:

```sh
(cd cmd/gateway-header-check && go build -o ../../bin/gateway-header-check .)
oc get httproute,gateway,authpolicy -n maas-fairness-poc -o yaml | bin/gateway-header-check -
```

**Must print `OK` and exit 0.** If it does not, the install is not done. Do not consider
MaaS ready to serve traffic, and do not run a benchmark — every number it produces will be
attributed to a band a client could have chosen for itself.

### 7.5 — Observability

```sh
oc apply -f deploy/podmonitor.yaml
oc apply -f deploy/prometheusrule.yaml        # alerts -- never applied on the source cluster
```

`deploy/grafana-dashboard.yaml` carries the dashboard. Loading it is fiddlier than it looks
— the Grafana Deployment mounts one specific ConfigMap name, and restarting the pod wipes
its emptyDir database. Follow `docs/runbook.md`, "Load the fairness dashboard into the live
Grafana", exactly; do not restart first.

> `deploy/prometheusrule.yaml` was **never applied** on the source cluster, so the alert
> rules in it are unexercised. Applying them here is a genuinely new test, and if a rule is
> malformed you will find out, not us.

---

## 8. Initial test: the six-rung ladder

Climb in order. Each rung depends on the one below, and each tells you something different
about *where* a failure is. Resist the urge to start at the top — a failed benchmark with
no lower rungs passed is nearly impossible to localise.

### Rung 0 — calibrate `outputTokenWeight` (before anything else)

`outputTokenWeight` ships as **`2.0`, a deliberate placeholder.** It is the relative cost of
an output token versus an input token, and it moves with GPU, model, quantisation, batch
size and vLLM version. **It is not transferable, and your environment is the whole point of
this transfer.**

Two saturating runs against an otherwise idle pool, varying only the data shape:

```
A (prefill-dominated):  prompt_tokens=4096, output_tokens=1
B (decode-dominated):   prompt_tokens=64,   output_tokens=1024

outputTokenWeight ≈ (prefill tokens/sec in A) / (decode tokens/sec in B)
```

Twenty minutes of work that replaces the most arbitrary number in the config with a
measurement. Full procedure, including where to read the numbers:
`docs/calibrating-output-token-weight.md`.

**Changing it re-denominates the floors**, so re-derive the group weights in the same
change — do not adjust one and leave the other.

`cachedInputTokenWeight` is a separate matter: it now has real data behind it (hit rates
spanning 6.3%–96.4%, UNI-136) and needs a **decision**, not a measurement.

### Rung 1 — unit tests (no cluster)

```sh
go test ./... -race
```

Thirteen behavioural tests plus conformance: proportionality, unequal request sizes, work
conservation, the idle clamp (including a negative control with the clamp disabled, so the
test proves the *mechanism* rather than the absence of load), decay, grouping, spoof
resistance, provisional true-up, estimator-independence, abort handling, shadow mode,
determinism, and factory validation. `docs/design.md` §Verification describes each.

Needs the Go module cache ([§5.3](#53-language-packages-and-build-tooling)). If you cannot
populate it, you cannot run this rung — say so explicitly rather than skipping it quietly,
because it is the only rung that tests the algorithm itself rather than the deployment.

### Rung 2 — the plugin is loaded and classifying

```sh
oc get pods -n maas-fairness-poc -l app.kubernetes.io/component=router-scheduler
oc logs -n maas-fairness-poc <scheduler-pod> | grep -i maas-weighted-fairness
```

Want: pod `1/1 Running`, **0 restarts**, `maas-weighted-fairness` instantiated, zero
flag-parse errors. Then confirm the metrics endpoint is serving
`llm_d_epp_maas_fairness_*`.

A crash loop here is usually one of: a plugin registered as `StabilityAlpha` (must be
`StabilityBeta` — the KServe preset does not pass `--allow-experimental-plugins`); a
`command`/`args` override that lost the templated flags; or an image your nodes cannot pull.

### Rung 3 — classification smoke, off-GPU

```sh
PATH=/paperclip/bin:$PATH deploy/poc/20-n-group-smoke.sh
```

Proves that distinct identities authenticate through MaaS and land in **distinct EPP
queues** rather than all falling into `unclassified` — without a GPU run and without
touching the shared `maas-epp-config`. This is the cheapest test that exercises the full
auth → header → grouping chain, and misclassification is the single most common reason a
later benchmark reads as "the policy does nothing".

Needs the subscriptions and keys to exist first: `deploy/maas/08-tenants.yaml`, then
`deploy/maas/mint-loadgen-keys.sh app3 app4 …`. The mint script writes keys straight into
`secret/maas-loadgen-keys` and **never prints a key value** — keep it that way.

### Rung 4 — the fairness benchmark

The headline test. Its output *is* the fairness result — a verdict, not a metrics dump you
divide by hand.

```sh
OPENSHIFT_TOKEN=... ./deploy/poc/15-fairness-benchmark.sh full-contention first-run
```

Artifacts land in `results/<UTC-timestamp>-<label>/`: the EPP container log, before/after
snapshots of the EPP's own `llm_d_epp_maas_fairness_*` counters, and the generated report.

Start with `full-contention`. Named scenarios also include `app1-alone`, `app2-alone`,
`app2-idle`, `app1-idle`, `app2-trickle`, `end-users-idle`, `below-capacity`,
`asymmetric-demand`, and the `equal-workers-control` negative control. Each is documented
in the script header with its worker sizing and the reason for that sizing; the verdict
rules, including the asymmetric ones and the `UNCONTENDED` fourth verdict, are in
`docs/runbook.md`, "Run the fairness benchmark".

**Worker sizing is not a free parameter.** Each scenario's per-tenant worker counts are
derived from the weight ratio, and using equal counts instead is the single most effective
way to produce a healthy-looking run that measures nothing —
[§9](#9-failures-that-look-like-success), trap 1.

### Rung 5 — the A/B that proves the policy is doing it

Everything above can pass with the policy inert. This is the rung that rules that out.

The plugin ships with **`enforce: false` — shadow mode**: it classifies every request,
tracks every tab and publishes every metric, while leaving the existing dispatch order
untouched. Run your scenario as shipped, then flip `enforce: true` and run it again.

- Shadow mode must give you roughly **equal shares**.
- Enforcing mode must give you roughly the **configured weights**.

If both runs produce the same split, the policy is not the thing causing the split, and
nothing above this rung told you that. `docs/poc-results.md` §Reproducing has the exact
A/B procedure.

> **The flip recreates the EPP pod and zeroes the per-group counters.** Take your final
> metrics snapshot *before* you flip back, not after. And note that
> `maas-vllm-cpu` and `maas-vllm-gpu` **both read `maas-epp-config`** — editing it for a CPU
> test will recreate the GPU EPP too. `20-n-group-smoke.sh` avoids this by repointing only
> the CPU service at a separate ConfigMap; copy that pattern.

**Shadow mode is also the right way to start in production.** The algorithm is the part
least likely to be wrong on day one; the group matching rules, the half-life and the cost
weights are, and only real traffic knows them.

### Rung 6 — confirm the SFQ stamp is landing (only if you turned it on, [§7.3b](#73b--enabling-the-sfq-priority-stamp))

Rungs 0-5 exercise the EWMA tab and `enforce`; none of them touch
`sfqPriorityStamp`. If you turned it on, confirm the stamp independently before trusting
any share number against it — a missing `--scheduling-policy priority` flag or a
`propagatePriority: true` both fail **silently** here (the request still dispatches, just
unstamped or re-stamped by something else).

Two ways to check, neither needs a wire capture (UNI-298):

1. **The response header.** With `emitAttributionHeaders: true` (shipped default), every
   response carries `x-maas-fairness-priority` with the stamped integer. Send one request
   per tenant and confirm the header is present and the values are distinct, non-zero
   integers that grow across repeated requests from the same tenant (`F_g` only
   increases).
   ```sh
   curl -sD - -o /dev/null -H "x-maas-subscription: app1-production" \
     https://<route>/v1/completions -d '{"prompt":"hi","max_tokens":1}' \
     | grep -i x-maas-fairness-priority
   ```
2. **The metrics.** `maas_fairness_sfq_enabled` should read `1`.
   `maas_fairness_sfq_stamped_priority{fairness_id}` should be non-zero and increasing per
   tenant. `maas_fairness_client_priority_overwritten_total` increasing means a client (or
   your own load generator) is sending its own `priority` and it is correctly being
   overwritten — expected, not a bug. If you enabled `sfqDecisionLog: info`, one
   `"sfq priority"` log line per dispatch gives you the group, the stamped integer, and its
   rank among the groups' next tags directly — see `docs/design.md`, "UNI-302: the stamp
   explains itself".

**If the header is absent, or the metric is flat zero:** check, in order,
`sfqPriorityStamp` is actually `true` in the ConfigMap the running pod loaded (not just
the file on disk — confirm against the EPP's own startup log, which echoes its effective
config), then `--scheduling-policy priority` on the vLLM container, then
`propagatePriority` is not `true`. This is also precisely what
`deploy/poc/weight-split-check.py` ([below](#the-weight-split-checker)) reports as its
`contended` / `stamp_present` fields, so a single run of that tool answers all three at
once against a live tenant pair.

---

## 9. Failures that look like success

This section is the one to re-read when a result seems fine. Every item here produced a
healthy-looking run that measured nothing, on the source cluster, at least once.

**"It isn't working" — jump straight to your symptom:**

| Symptom | Most likely cause | Where |
|---|---|---|
| Split is flat / near-equal no matter the weights | Not actually contended (correct, work-conserving behaviour) — check item 1 below, and the checker's `contended` field | item 1 below |
| Split is flat / near-equal, and it IS contended | `identityHeader` mismatch (all traffic landing in `unclassified`), or `sfqPriorityStamp`/`--scheduling-policy priority`/`propagatePriority` misconfigured | [§8](#8-initial-test-the-six-rung-ladder) Rung 3 (classification) and Rung 6 (stamp) |
| EPP pod crash-looping / `0/1` | Plugin registered Alpha not Beta, a `command`/`args` override, an image the nodes can't pull, or (UNI-302) `sfqDecisionLog` set on an image without the decision-log code | [§8](#8-initial-test-the-six-rung-ladder) Rung 2, [§11](#11-changing-it) |
| Run "succeeds" but the plugin was never in the path | `FailOpen` on an `ImagePullBackOff` EPP — latencies look fine because nothing was managed | item 2 below |
| Stamp not taking effect (header/metric absent) | `--scheduling-policy priority` missing on vLLM, or `propagatePriority: true` | [§8](#8-initial-test-the-six-rung-ladder) Rung 6 |
| Pool never saturating / can't get `contended: true` | Worker count too low for the configured weight | item 1 below, worker sizing under [§8](#8-initial-test-the-six-rung-ladder) Rung 4 |

**1. Equal per-tenant concurrency makes work conservation read as a broken policy.**
A weighted split can only be observed if **every tenant offers more load than its
entitlement**. With equal concurrency the high-weight tenant runs out of work to be
favoured with, its queue drains, and the surplus correctly goes to others. You see equal
shares and conclude the policy is inert. It is not — it is working, and your load shape
cannot see it. This is kept as the named `equal-workers-control` scenario precisely so the
contrast is on the record. **This is the single most likely way you will misread your
first result.**

**2. An EPP stuck in `ImagePullBackOff` is silent, because the pool is `failureMode:
FailOpen`.** Envoy bypasses the fairness policy entirely and serves every request
unmanaged. The run completes, the latencies look fine, the tokens flow — and the plugin was
never in the path. On the source cluster this happened because freshly-joined GPU nodes
could not reach the internal registry's ClusterIP (`dial tcp 172.30.x:5000: i/o timeout`)
while the model servers pulled from `registry.redhat.io` over the node default route and
started fine. **Always confirm the EPP pod is `1/1 Running` before trusting a run**, and
check it on the specific nodes your workload lands on. `09-vllm-gpu.yaml` pins the EPP off
the GPU nodes partly for this reason.

**3. Skipping the AuthPolicy patch reports healthy while admitting a forged priority
band.** MaaS says `Ready=True`, the Tenant is fine, nothing logs an error, and a client can
set `x-llm-d-inference-objective` to pick its own band. Fairness is **intra-band only**, so
one tenant in a different band is not competing at all and the whole measurement is
meaningless. The only thing that catches this is the `gateway-header-check` run in §7.4 —
not the Tenant status. `docs/gateway-header-stripping.md` has the live proof of the
unpatched behaviour. **This patch can silently revert on its own** — it did, for an unknown
window, discovered on 2026-11-09 (UNI-210): `odh-model-controller` regenerates
`maas-poc-gateway-authn` from its template on certain `LLMInferenceService` reconciles, and
nothing was running the check automatically, so roughly thirty benchmark runs executed
against a reverted patch before anyone noticed. `deploy/poc/15-fairness-benchmark.sh` and
`deploy/poc/20-n-group-smoke.sh` now check for the override before doing anything else and
re-apply the patch automatically (aborting, not just warning, if the re-apply doesn't hold)
— but if you write a new script that drives traffic through this gateway, it does not get
that protection for free; wire in the same check.

**4. The two vLLM flags default off and fail silently.**
`--enable-force-include-usage` and `--enable-prompt-tokens-details`. Without them the
`usage` block is absent or incomplete, the provisional charge is never trued up, and every
request is charged its *estimate* forever. The standing check is that untrued requests stay
at zero — `docs/runbook.md`, "Standing checks before trusting any result".

**5. A `:latest` tag plus `imagePullPolicy: Always` means two replicas of the same
Deployment can run different binaries.** Six manifests here carry `Always`; all six now
point at a digest, which makes it harmless — a digest cannot move, so `Always` only re-pulls
the same bytes. Keep it that way. If you replace a digest with a tag while mirroring, you
reintroduce exactly this, and it is invisible until the second replica restarts.

**6. `oc get` silently omits resource types your token cannot list.** A namespace snapshot
taken with an under-privileged token looks complete and is not — the missing types produce
no error and no warning. If you are verifying "nothing else is running", verify it with a
token you know can list everything, and name fully-qualified resource types rather than
short names (a bare `inferencepool` resolves to exactly one of the two installed
InferencePool API groups and silently stops checking the other).

**7. Metrics absent from both snapshots mean zero, not unknown.** A counter that never
appears was never incremented — for the contention counters that means "never contended",
which is a *result*. Do not report it as missing data; correlate it against the other
indicators before concluding anything.

**8. A 10-second reporting window swings ±30 points on its own.** Before calling a burst or
a floor violation real, compare against an idle-phase baseline from the *same run*. For
duty-cycle scenarios, average the deviation per phase instead of reading individual windows.

**9. A client hanging ~300s on a rejected request is the gateway, not this plugin.** For
context-length rejections specifically, vLLM logs the 400 as fully sent and the EPP's
`PreRequest`/`ResponseBody` cycle completes in ~100 ms, but the client receives headers and
**zero body bytes** before the connection dies on a non-HTTP-timeout teardown. The defect
sits in Envoy/Istio's downstream reply relay, after both vLLM and the EPP have finished; a
same-shape 200 OK control request completes normally. Live-reproduced in UNI-190. If you see
this on your side, do not go looking in `pkg/fairness/weightedlas/` — and note that it is
**not** retry amplification: there is one charge per request.

**10. A metrics-scrape gap during backend overload reads exactly like an EPP restart in the
report's own verdict fields — it is not one.** The report's restart-detection field
(`verdict.epp_restarted_in_windows_but_not_snapshot_pair`) was set on a 1,350-worker run and
taken at face value as a counter reset (filed as UNI-230, uninvestigated). Reading the raw
`metrics-timeseries.txt` instead showed
the contended-token counter crossing the gap **monotonically** (no restart would preserve
that) and the k8s events log showing one unchanged EPP pod name for the whole run — what
actually happened was 2.5 minutes of the `/metrics` endpoint being unreachable while the
backend was overloaded, a real operational signal, not a measurement artifact. The report
script (`15-fairness-report.py`) now records each scrape's own exit code and reports a
`verdict.scrape_gap_in_windows` field separate from the restart flag, but **a result scored
before this fix needs the same by-hand cross-check** (monotonic counter + stable pod name)
before you treat an apparent restart as real.

**11. The checked-out working tree can be running code nobody committed, including a live
image built from it.** Found during this rewrite (UNI-303): `main` had merged the SFQ
stamp, but the deploy manifests, and the live cluster, were still on the UNI-220-era image
— and the live GPU and CPU EPPs were each running a *third and fourth* digest, found in
neither the manifests nor any commit. Separately, a repository checkout on this kind of
shared agent host can carry another session's **uncommitted** edits at any moment — this
rewrite's first image build accidentally included another session's in-progress,
uncommitted changes to `pkg/fairness/weightedlas/`, because an OpenShift `BuildConfig`
with `source.binary` uploads whatever is on disk, committed or not. The fix both times is
the same: **never trust a running artifact's provenance from its behaviour or from prose
describing it — check `git log --oneline -- deploy/llmisvc.yaml` against the digest
actually running, and build any image you need from a freshly cloned checkout, not a
working tree you did not create this session.**

**12. A rolling update on a fully-*allocated* GPU pool does not fail — it hangs, unless
the allocation is actually idle.** Changing an `LLMInferenceService`'s vLLM container args
(image, command-line flags) triggers the owning controller to roll its Deployment at the
default 25%/25% surge/unavailable. With a 2-replica pool and zero spare *schedulable* GPUs,
the surge pod cannot schedule, and the rollout sits with one old pod and one new `Pending`
pod indefinitely — no error, no event you would notice without looking, no timeout. On this
cluster, all 6 GPUs across three lanes were nominally claimed, but two of the three lanes
turned out to have been idle for days (no traffic, same pod age as creation) — the
constraint was softer than "allocated" implied. See
[§7.3b](#73b--enabling-the-sfq-priority-stamp) for the manual-scale-down fix, and
[UNI-309](/UNI/issues/UNI-309) for the actual teardown-and-redeploy this cluster needed.
It only bites an **existing** deployment; a fresh install has no old ReplicaSet to roll
and is unaffected.

---

## 10. What is and is not proven

### Proven

- **(Headline, UNI-294) The SFQ priority stamp holds the configured split to within
  0.06–0.12 percentage points, live, on real contended traffic, across three repeated
  runs** (0.057, 0.112, 0.120 pts; `results/20261125T0107/0115/0122*-uni294-arm2-run*`),
  **on a scenario with equal offered worker counts per tenant** — so the tight split
  tracks the configured *weights*, not the offered load shape, which is strong evidence.
  A fourth run with the identical EPP-side config (`sfqPriorityStamp: true`) missed by
  32.5 points (`...-arm3-isolation`) — the EPP-side config alone does not explain the
  difference, and the most likely remaining variable is whether vLLM was actually running
  `--scheduling-policy priority` for that run, consistent with the mechanism `docs/design.md`
  describes, though that specific flag was not captured in this run's own artifacts (see
  `results/UNI-294-INDEX.md` for the full, precisely-sourced comparison — read it before
  citing these numbers, it corrects a wrong first-pass labelling of the arms from this same
  rewrite). This is the result against the agreed specification
  ([§2](#2-how-it-works-internally)): proportional share under contention, not a floor.
  `docs/poc-results.md` does **not** contain this result (checked; it predates the stamp)
  — `results/UNI-294-INDEX.md` is the full run record. The live session used image tag
  `uni294-sfq-live`, not reproducible from a committed manifest as of this writing (item 12
  under "Not proven" below).
- The plugin builds into a custom EPP image, loads under both RHOAI 3.4-shaped and 3.5
  scheduler presets, and instantiates with zero flag-parse errors.
- **On two A100s with real vLLM: 20.5% / 11.6% / 67.9% against a configured 20 / 10 / 65**,
  with `normalized_service` converged to within 0.1% between app1 and end-users. Shadow
  mode on the same setup gives equal thirds. Traffic went through a real
  `LLMInferenceService` templated by RHOAI's KServe preset, over HTTPS, authenticated with
  real MaaS `sk-oai` API keys.
- On the GPU-free rig: 23.8% / 13.5% / 62.8% against the same configured 20 / 10 / 65,
  reproducible across runs, versus equal thirds in shadow mode.
- **Work conservation**: with one tenant idle the remaining two absorb the whole pool (93%
  of baseline throughput), and below capacity a second tenant costs the first no latency.
- A weight is a **floor, not a ceiling** — a trickling tenant is not throttled further, and
  its unused entitlement is redistributed in the others' own ratio.
- The header-forgery hole is real, and the AuthPolicy patch closes it. Both demonstrated
  live. The patch has been seen to revert on its own in service (UNI-210) — see
  [§9](#9-failures-that-look-like-success) item 3 — and the two benchmark harnesses now
  check and re-apply it automatically before every run.
- Unit tests pass under `-race`.
- **The live default `queueDepthThreshold` is 32, not a smaller value this plugin
  originally shipped with.** A threshold sweep (UNI-215) found no value in the 8–150 range
  that both holds the split and keeps throughput, and settled on 32 as the best tradeoff; a
  full re-run of the 131–168 edge-case series at that default (UNI-218) restored genuine
  contention for 26 of 30 previously-scored rows (up from 8 of 29 at the old default of
  150), with zero new failure modes — every row that still FAILs reproduces an
  already-documented mechanism.
- **The newcomer clamp's credit-confiscation bug is real, was fixed in two stages, and the
  fix has a measured, evidenced limit — it is not a closed, binary "fixed."** The earlier
  write-up's claim that the concern was "refuted on GPUs" because those runs were
  demand-starved did not hold up: UNI-212 found and fixed a wall-clock-idleness false
  positive, and UNI-220 found and fixed a second one (a group with a dispatched-but-not-yet-
  completed request was still treated as a returning "newcomer"). The second fix closes
  57% of the over-offer gap at a 4x over-offer ratio and 39% at 8x — a real, large,
  **partial** correction, not a full one. The residual at high ratios is structural (an 8x
  over-offer needs roughly an 8x latency spread between the flooding and starved tenant to
  fully correct, and this ordering-only mechanism does not produce that), not a remaining
  bug to patch — closing it further needs an admission-side mechanism (a per-group cap or
  backpressure), deliberately out of scope here. Treat "the over-offer problem is fixed" as
  false for ratios above ~4x.
- **A secondary, latency-based verdict backs the share verdict even where the percentage
  target is structurally unreachable (UNI-226).** The EPP's own per-tenant TTFT/ITL
  histogram metrics (`llm_d_epp_request_ttft_seconds_bucket` and the streaming-ITL
  equivalent), already emitted `fairness_id`-labelled by the upstream framework, are now
  read into a per-tenant report. On a `98/1/1` weight set under equal load, the share
  verdict FAILs as predicted
  (app1 delivered 61.8% against an unreachable 98% target) — but app1's TTFT is still
  strictly the lowest, with a 55.4s gap to the next tenant that is ~330x the same-run,
  between-tenant noise floor (167ms, measured on an equal-weight/equal-load control). The
  policy is doing its job even on a target it cannot structurally hit.
- **Most PASS verdicts elsewhere in `docs/poc-results.md` are weaker evidence than a bare
  PASS count implies, and this does not change the two headline numbers above.** Most
  scenarios size each tenant's offered worker count proportionally to its configured
  weight, so a PASS there cannot distinguish "the policy enforces the weight" from "the
  split just follows offered concurrency" — they predict the same split. Restricted to rows
  where worker share and weight share diverge by more than the 10-point pass bar (the
  "discriminating" scorecard, UNI-225/UNI-228): **2 PASS, 10 FAIL, out of 12.** The two
  headline results above are themselves discriminating (equal worker counts against
  unequal weights) and are unaffected. Equal-weight scenarios (e.g. `uni165-equal`) are
  excluded from this scorecard by board ruling (UNI-228) — under an equal weight set, equal
  load and weight-proportional load are the same configuration, so they cannot produce a
  gap without breaking the board's mandated equal-load baseline — and are kept instead as
  the TTFT noise-floor control cited above. Before citing any other PASS in this repository
  as evidence the policy works, check its own worker-vs-weight gap the same way.
- **(UNI-303, 2026-11-25) The SFQ-stamp-carrying image builds, passes its full test suite,
  and boots clean on live EPP pods with no restarts, no flag-parse errors, and
  `PropagatePriority:false` confirmed in its own logged effective config** — on both the
  GPU and CPU schedulers in `maas-fairness-poc`. **Separately, vLLM `0.24.0+rhaiv.9`
  accepts `--scheduling-policy priority` as a valid, non-default argument and boots a
  healthy model server with it** (confirmed on the CPU path; see
  `results/20261125T231600Z-uni303-image-rebuild-and-sched-policy-check/`). Neither of
  these is a fairness measurement — see item 12 under "Not proven."

### Not proven

1. **A real RHOAI 3.4 cluster.** The 3.4 test used a 3.4-shaped *preset* under a 3.5
   *controller*. Open: whether 3.4's controller validates the `EndpointPickerConfig` before
   passing it through; the InferencePool API group 3.4 creates versus what a v0.11.0 EPP
   watches; and **the tokenizer sidecar** — 3.4's preset adds a second container
   (`llm-d-uds-tokenizer:v0.7.1`) sharing a controller-injected `tokenizer-uds` volume,
   which 3.5 has no equivalent of. Untested, and the most likely surprise.
2. **`outputTokenWeight` on any hardware but the source cluster's.** It ships as a
   placeholder. [§8](#8-initial-test-the-six-rung-ladder) rung 0 is not optional.
3. **`cachedInputTokenWeight`** — evidence gathered (UNI-136), decision not taken.
4. **Scale.** Everything here is two A100s, three to six tenant groups, runs of minutes to a
   two-hour soak. Nothing about many-GPU pools, many-tenant tables, or multi-day operation.
5. **Multiple EPP replicas.** `replicas: 1` throughout. All policy state is in-process, so
   scaling out **shards** it — two replicas would each enforce fairness over their own share
   of traffic, which is not the same guarantee. Treat multi-replica as unimplemented, not
   as a tuning knob.
6. **`deploy/prometheusrule.yaml`** was never applied on the source cluster; the alert rules
   are unexercised.
7. **Small-weight groups run ~4 points rich.** A known, documented residual gap, not a
   mystery — `docs/poc-results.md`, "Residual gap".
8. **Open-loop load contradicts closed-loop on the clamp.** Under genuine Poisson arrivals
   the newcomer clamp fires constantly, and pushed past saturation its cost becomes visible
   and inverts the split. Harmless below saturation. If your production traffic is
   arrival-driven rather than concurrency-driven — and real traffic is — read
   `docs/poc-results.md` §"Open-loop (Poisson) load generation" before you size anything.
9. **Rejected requests are charged, and the ledger leaks.** Context-length rejections are
   charged ~9–10× a normal request's cost, permanently (UNI-148; the ledger's own G2
   cross-check flags it FAIL). This is by design, not a bug in the strict sense, but the
   design predates the evidence. It is an **open board policy decision**, not a defect
   waiting on a fix — do not "correct" it locally without reading UNI-148 first.
10. **EPP-restart resilience for a high-concurrency tenant.** Chaos-deleting the scheduler
    pod mid-run reproducibly leaves the highest-concurrency tenant's dispatch accounting
    broken afterward — not a simple "never re-converges." A fresh, instrumented repro
    (UNI-193, after the original E1 case's harness bugs were fixed) showed ~80% of that
    tenant's requests completing successfully at the client (`200`) while never registering
    in the EPP's own `dispatch_total`, token ledger, or `contended_*` metrics at all —
    four times the ~20% accounting loss every tenant sees around any snapshot boundary.
    Root cause needs tracing the upstream `gateway-api-inference-extension` flow-control
    path, which is imported, not vendored, and is out of scope here. Open as
    [UNI-194](/UNI/issues/UNI-194).
11. **`docs/poc-results.md`'s measurements predate the SFQ stamp and are not re-verified
    against it.** They remain the evidence record for the tab-only mechanism described
    there (through roughly UNI-230) and should be read as that, not as current-state
    proof for anything downstream of UNI-293.
12. **An end-to-end fairness run with the SFQ stamp on, against real contended GPU
    traffic, on this rebuilt image.** [§2](#2-how-it-works-internally)'s mechanism is
    proven by the unit/sim suite (`sfq_sim_test.go`, `sfq_test.go`, run as part of
    `go test ./...` on this exact commit before this rewrite) and was live-verified once
    before (tag `uni294-sfq-live`), but that verification is not reproducible from a
    committed manifest and this rewrite's own live check only confirmed the new image
    boots clean and that vLLM accepts `--scheduling-policy priority` — not that the stamp
    moves a live split on *this* image. Run [§8](#8-initial-test-the-six-rung-ladder)'s
    Rung 6, or `deploy/poc/weight-split-check.py`, before citing a share number against
    this build.
13. **`--scheduling-policy priority` on the GPU vLLM workload specifically.** Confirmed
    accepted on the CPU vLLM path (same `vllm==0.24.0+rhaiv.9`). [UNI-309](/UNI/issues/UNI-309)
    put the flag in the committed manifest (`deploy/poc/09-vllm-gpu.yaml`) and applied it
    across all three GPU lanes on the rebuilt image. **Not yet verified: that the stamp
    moves a live split on real GPU traffic.** UNI-309 only confirmed the mechanics (image
    boots, config decodes, flag accepted) — see its own report for exactly what each lane's
    pod health and `sfq_stamped_priority` check showed. The actual A/B fairness result is
    the follow-up suite's job, explicitly blocked on this ticket.
14. **Two uncommitted image digests found live on this cluster before this rewrite**
    (`sha256:617509...` on the CPU EPP, `sha256:5ddee9a...` seen there previously) were
    never traced to a source commit and are now overwritten. Whatever behaviour they
    carried relative to `main` at the time cannot be recovered.
15. **Retired by UNI-309.** The image is now built from `main` tip (`6e49e0c`, which
    contains UNI-302), re-pinned across all six manifests
    (`sha256:d496a0cf5075a1024b9f556524312653103eab14d656645dd8115d820905b537`), and
    `deploy/poc/00-config.yaml` carries `sfqPriorityStamp: true` for the first time — it
    previously had none of the UNI-293/299/300/302 keys at all, not even at their `false`
    defaults. `sfqDecisionLog` is committed `"off"`; flip it only for a single measurement
    run per its own comment.

**Roadmap beyond this document, in dependency order:** [UNI-309](/UNI/issues/UNI-309)
(rebuild at current `main`, re-pin, redeploy all three GPU lanes with the scheduling flag)
→ [UNI-308](/UNI/issues/UNI-308) (live-verify the stamp end-to-end on real contended GPU
traffic against that rebuild) → [UNI-310](/UNI/issues/UNI-310) (re-run the historical
UNI-nnn test suite on real GPUs under the stamp, scored honestly against which rows it
can and cannot speak to).

### Not examined in this transfer review

- **Platform-layer mirroring** (RHOAI, Kuadrant/RHCL, MetalLB, NVIDIA GPU Operator, NFD).
  N/A: these are your OpenShift disconnected-install process, not artifacts of this
  repository. This review covers what this repository adds on top.
- **`prototype/`.** N/A: frozen design provenance, never deployed, not a deliverable. Its
  `python:3.11-slim` and `envoyproxy/envoy:v1.31-latest` references are recorded in
  [§5.1](#51-container-images) for completeness and should not be mirrored.
- **The Logging/LokiStack image set.** N/A: already enumerated with digests and air-gap
  deltas in `docs/logging-install-spec.md`, and optional for the fairness result. Not
  re-derived here.

---

## 11. Changing it

**A behaviour change means a rebuilt image.** Plugins are compiled in; there is no dynamic
loading and no config-only path to changing policy logic. What *is* config:

| Change | Where | Rebuild? |
|---|---|---|
| Group names, prefixes, weights | ConfigMap `maas-epp-config` (`deploy/epp-config.yaml`) | no |
| `enforce`, `halfLife`, `newcomerClamp`, `outputTokenWeight`, `cachedInputTokenWeight`, `queueDepthThreshold` | same ConfigMap | no |
| `sfqPriorityStamp`, `undecayedTrueUp`, `sfqEndpointStaleSeconds`, `sfqSettleTimeoutSeconds`, `sfqUnboundedOutputTokens`, `sfqDecisionLog` | same ConfigMap — **but see the caution below** | no, with one exception |
| `--scheduling-policy priority` on vLLM, `propagatePriority` on `requestHandler` | the `LLMInferenceService` spec, not the ConfigMap | no, but patching it changes the vLLM container's args, which can trigger the rolling-update deadlock in [§7.3b](#73b--enabling-the-sfq-priority-stamp) on a GPU pool with no spare capacity |
| Policy logic, cost model, metrics | `pkg/fairness/weightedlas/` | **yes** |
| Upstream `llm-d-router` version | `go.mod` **and** `Dockerfile.epp`'s builder image, together | **yes** |

> **The one exception: `sfqDecisionLog` needs a rebuild on every scheduler reading the
> ConfigMap, even though it is itself a config key.** Plugin parameters are decoded with
> `DisallowUnknownFields`, so an EPP on an image older than UNI-302 refuses to start the
> moment this key appears in its config at all — "off" included. The GPU and CPU
> schedulers read the same `maas-epp-config`, so roll **both** to an image that has
> UNI-302 before adding the key to either.

Rules that are load-bearing, each because something broke without it:

- **Override only `image:`** (and `resources:` if needed) on the scheduler container. KServe
  templates `--pool-name`, the ports, the TLS flags, and appends `--config-text`; overriding
  `command` means re-templating all of it yourself. The container must stay named `main` or
  the strategic merge does not hit.
- **Never patch the generated Deployment directly.** The controller owns
  `<name>-kserve-router-scheduler` and reverts manual edits.
- **Register as `StabilityBeta`, not Alpha.** The runner validates plugin stability and the
  KServe preset does not pass `--allow-experimental-plugins`, so an Alpha plugin fails at
  startup.
- **Keep `USER 65532:65532`** in `Dockerfile.epp`. KServe sets `runAsNonRoot` and
  `readOnlyRootFilesystem` on the scheduler container, so a root image fails admission under
  `restricted-v2`. Keeping it means no SCC exception is needed.
- **Keep `registerDownstreamCompatFlags()`** in `cmd/epp/main.go`. Under TLS, RHOAI 3.4
  templates `--model-server-metrics-scheme=https` — a flag that exists only in Red Hat's
  downstream fork, in no upstream release. pflag treats an unknown flag as fatal, so without
  the shim the pod crash-loops on every 3.4 cluster and the failure looks like a bad image.
- **Bump `go.mod` and the builder image together.** The builder's Go version must be ≥ the
  `go` directive in upstream's go.mod, or the build fails with a toolchain error.
- **Re-pin deliberately.** `docs/version-pinning.md` §5 has the upstream-drift check, the
  re-pin procedure, and a worked v0.11.0 → v1.0.0 delta showing which upstream changes are
  silent (request attributes becoming confined would cause our writes to be dropped with no
  error). Do not float to `main`; flow-control interfaces are Alpha/Beta on a v0.x module.

### If something here is wrong

This guide was written from the repository, not from your cluster. Where your environment
contradicts it, your environment is right. Record the delta in this file as you go — the
next person across the boundary reads this one, and a correction written down beats a
correction remembered.

---

## The weight-split checker

`deploy/poc/weight-split-check.py` (UNI-303) is a **single, standalone file** — it is not
part of this POC's harness and imports nothing else from this repository. Copy it anywhere
and point it at a running deployment to get a plain PASS/FAIL/UNCONTENDED verdict on
whether the configured weights are actually being honoured, without reading any other
document first. Its own module docstring (`python3 deploy/poc/weight-split-check.py --help`)
is the complete reference — config file shape, what it needs (one API key per tenant, a
metrics-reader token, network reach to the gateway and the EPP's `:9090`), and a
troubleshooting section keyed to a flat/missing split. It reuses the plugin's own
`llm_d_epp_maas_fairness_contended_service_tokens_total` counter for the weighted-cost
share rather than recomputing the cost model client-side, so it cannot disagree with the
plugin about what "cost" means, and it uses the same 10-point pass bar and the same
`fairness_id`-keyed grouping as `deploy/poc/15-fairness-report.py`.

It is deliberately **not** a replacement for that report script: it has no phases, no
chaos-event timeline, no TTFT/ITL secondary verdict, and no comparison against a stored
benchmark baseline. It answers one question — "right now, pointed at this endpoint, is the
split correct" — standalone, from outside the harness, which is what an agent doing a
first health check on a freshly-deployed internal environment needs. Reach for
`15-fairness-report.py` for an actual scored benchmark run.

What it will tell you that a naive glance at traffic will not:
- **Whether the pool was actually contended**, and for how much of the scored window — a
  flat/near-equal split under no contention is the correct result, not a failure, and the
  tool says so (`UNCONTENDED`) instead of printing a misleading verdict either way.
- **How much of a FIFO/queue-fill warm-up it excluded**, and exactly how many requests per
  tenant had already gone out before scoring started — a shallow burst measures how fast
  a tenant repays its own queueing, not the weighted split.
- Rung 6 ([§8](#8-initial-test-the-six-rung-ladder)) is this tool's natural first use: run
  it once with `sfqPriorityStamp` off (expect a near-equal split or `UNCONTENDED`, since
  shadow mode leaves FCFS in charge) and once with it on, the same way the ladder's own
  Rung 5 A/B works for `enforce`.
