# Air-gap handoff guide

**Audience: the agent who receives this repository inside a disconnected network and has
never seen it before.** You have the repository and nothing else. No one who built it is
reachable. This document is the single entry point: it tells you what this is, what has to
exist around it before it can run, what to carry across the boundary, how to deploy it, how
to test it the first time, and which healthy-looking outcomes are actually failures.

Read this top to bottom once before touching the cluster. The order matters more than any
individual command.

> **Status of this snapshot.** Cut 2026-11-02 at commit `bdd9c15` (UNI-190), **while the
> edge-case test series was still running**. This is a deliberate mid-series promotion, not
> a finished POC. [§10](#10-what-is-and-is-not-proven) says exactly what that leaves open.

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
| [8](#8-initial-test-the-five-rung-ladder) | Initial test: the five-rung ladder |
| [9](#9-failures-that-look-like-success) | Failures that look like success |
| [10](#10-what-is-and-is-not-proven) | What is and is not proven |
| [11](#11-changing-it) | Changing it |

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

**Weighted least-attained-service.** Each group carries a decaying *tab* of recently
consumed tokens; the group with the lowest `tab ÷ weight` is served next. Equalising
`tab ÷ weight` *is* proportional sharing, so the ratios converge on the configured weights
without any constant describing how fast the GPUs are. That property is what makes it
portable to your hardware without re-deriving a throughput model.

Three mechanisms make it work in practice. Each exists because the naive version fails
without it, and each is a thing you can accidentally disable:

- **Exponential decay** — the tab measures *recent* usage, not all-time. One lazy
  `2^(-Δt/halfLife)` on read and write.
- **Newcomer clamp** — a returning-idle tenant is raised to the current minimum, so it goes
  first *once* rather than monopolising the pool for minutes. Without it, consuming spare
  capacity becomes a debt and work conservation is poisoned.
- **Provisional charge** — an estimate is charged at dispatch and trued up against the real
  `usage` block at completion. Generations take 10–30s while scheduling decisions happen
  every millisecond; without this a tenant dispatches thousands of requests before any
  lands on its tab.

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

The repository carries ~11,700 lines of documentation. You do not need to read it all. Go
to the one that answers your question:

| Your question | Document |
|---|---|
| Why does this exist, what are the design decisions and their rejected alternatives | `docs/design.md` (1,380 lines; Part 1 is plain-language) |
| What was measured, on what hardware, and what the numbers were | `docs/poc-results.md` (4,752 lines — the evidence record) |
| How do I actually run a thing on the cluster | `docs/runbook.md` (2,367 lines — task-indexed, start from its headings) |
| What version is pinned, why, and how do I bump it | `docs/version-pinning.md` |
| `outputTokenWeight` is 2.0 — what do I set it to here | `docs/calibrating-output-token-weight.md` ← **you must do this** |
| How does header forgery work and how is it closed | `docs/gateway-header-stripping.md` |
| What do the EPP log lines mean | `docs/log-field-contract.md`, `docs/logql-queries.md` |
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
| `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135` — **the EPP image, the actual deliverable** | mirrorable, **but see §6.1** | Built from commit `fc27130` (UNI-29). Referenced by digest from six manifests. The Quay repository is **private**: an anonymous pull token is issued but the manifest GET returns `UNAUTHORIZED`, so it cannot be mirrored without the robot credential. |
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
registry auth token is issued, then the manifest GET for digest `sha256:5ddee9a7…` returns
`UNAUTHORIZED`. An air-gapped mirror run without the robot credential will fail on the one
image that *is* the deliverable, and it will fail at mirror time, not at deploy time.

**Unblock — one of:**

1. **Export before transfer** (preferred). On the connected side, with the Quay robot
   credential:
   ```sh
   skopeo copy --all \
     docker://quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135 \
     dir:/transfer/maas-fair-share-epp
   ```
   Carry the directory; load it with `skopeo copy dir:… docker://<internal-registry>/…`.
   Verify the digest is unchanged after the load — that is the whole point of having one.
2. **Rebuild on your side** from this source tree. This needs the Go module cache
   ([§5.3](#53-language-packages-and-build-tooling)) and the two base images, and it
   produces a **different digest**. If you rebuild, record your digest and update the six
   manifests; do not leave them pointing at a digest your registry does not have.

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
side: `outputTokenWeight` ([§8](#8-initial-test-the-five-rung-ladder), rung 0) and the
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
[§8](#8-initial-test-the-five-rung-ladder) weeks before the GPU path is ready.

Two vLLM flags are **hard prerequisites** on any real-vLLM path. Both default off, and both
fail silently — you get a working-looking deployment whose usage accounting is empty:

```yaml
args:
  - --enable-force-include-usage
  - --enable-prompt-tokens-details
```

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

## 8. Initial test: the five-rung ladder

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

---

## 9. Failures that look like success

This section is the one to re-read when a result seems fine. Every item here produced a
healthy-looking run that measured nothing, on the source cluster, at least once.

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
unpatched behaviour.

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

---

## 10. What is and is not proven

### Proven

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
  live.
- Unit tests pass under `-race`.
- The earlier concern that the newcomer clamp hurt the split was **refuted** on GPUs; those
  runs were demand-starved.

### Not proven

1. **A real RHOAI 3.4 cluster.** The 3.4 test used a 3.4-shaped *preset* under a 3.5
   *controller*. Open: whether 3.4's controller validates the `EndpointPickerConfig` before
   passing it through; the InferencePool API group 3.4 creates versus what a v0.11.0 EPP
   watches; and **the tokenizer sidecar** — 3.4's preset adds a second container
   (`llm-d-uds-tokenizer:v0.7.1`) sharing a controller-injected `tokenizer-uds` volume,
   which 3.5 has no equivalent of. Untested, and the most likely surprise.
2. **`outputTokenWeight` on any hardware but the source cluster's.** It ships as a
   placeholder. [§8](#8-initial-test-the-five-rung-ladder) rung 0 is not optional.
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
10. **The edge-case series was still in flight when this version was cut.** `docs/poc-results.md`
   is complete through UNI-190; later tickets in the chain are not in this snapshot. Check
   that document's own ticket ordering before concluding a case was never examined.

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
| `enforce`, `halfLife`, `newcomerClamp`, `outputTokenWeight`, `cachedInputTokenWeight` | same ConfigMap | no |
| Policy logic, cost model, metrics | `pkg/fairness/weightedlas/` | **yes** |
| Upstream `llm-d-router` version | `go.mod` **and** `Dockerfile.epp`'s builder image, together | **yes** |

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
