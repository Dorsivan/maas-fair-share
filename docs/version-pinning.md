# Version pinning and upstream-drift maintenance

This repository builds a complete, standalone Endpoint Picker binary out of
`github.com/llm-d/llm-d-router` and registers one extra plugin into it. We do not
fork upstream and we do not vendor it: we compile against it. That makes every
upstream release a potential source of silent breakage, and this document is the
process for noticing it before a cluster does.

It covers three things:

1. **What is pinned today**, exactly — module versions, build toolchain, container images.
2. **What upstream surface we actually depend on**, by name, so a reader can diff it
   against a future release without reading our source first.
3. **The maintenance process** — who looks, how often, what forces a re-pin, and how a
   breaking change becomes a ticket.

Owners are named by role throughout. The roles are CTO, Engineer, Reviewer/QA, and the
board operator.

---

## 1. Correcting the premise

The POC write-ups (`docs/design.md` item 11, `docs/poc-results.md` outstanding item 13)
say "the flow-control interfaces are Alpha/Beta". That is not quite what upstream means,
and the difference changes what you have to watch.

Upstream's stability levels are a property of a **registered plugin type**, not of a Go
interface. `pkg/epp/framework/interface/plugin/stability.go` defines
`StabilityAlpha`/`StabilityBeta`/`StabilityStable`, and
`pkg/epp/framework/plugins/README.md` states the contract:

| Level | Guarantee | CLI requirement |
|---|---|---|
| Alpha | No backwards-compatibility guarantee at all | needs `--allow-experimental-plugins` |
| Beta | Backwards compatible within the current version; +2 minor deprecation policy before removal | allowed by default |
| Stable | Backwards compatible across minor releases; breaking changes only on a major bump | allowed by default |

`cmd/epp/runner/runner.go` is upstream's single source of truth for in-tree plugin
stability. **We** register `maas-weighted-fairness` at `StabilityBeta`
(`cmd/epp/main.go`, in `run`) because `ValidatePluginStability` rejects Alpha plugins unless
`--allow-experimental-plugins` is passed, and the RHOAI KServe scheduler preset does not
pass it.

The Go **interfaces** we compile against carry no stability annotation whatsoever. Their
only contract is the module's semantic version. So the two statements that actually
govern us are:

- Our plugin registration is Beta, which buys a +2 minor deprecation window **for the
  plugin mechanism**, not for the types in its method signatures.
- Until the module reached v1.0.0 there was no compatibility promise on any exported
  symbol. **Upstream tagged v1.0.0 on 2026-10-15.** From that tag forward, exported API
  is covered by Go semver and a breaking change requires a v2 module path. That is a
  large reduction in risk and it is the single strongest argument for moving off the
  v0.11.0 pin — see §6.

There is one more thing the "interfaces" framing hides, and it is the one that bites: a
change can break us without changing any signature we reference. §6 is a worked example.

---

## 2. What is pinned today

### 2.1 Go modules

`go.mod` requires exactly one upstream module directly. Everything else in the EPP graph
arrives as an indirect dependency resolved by `go mod tidy`: **107 `// indirect` requires**
in `go.mod` (113 require lines in total), resolving to **147 distinct module paths** in
`go.sum`. There are no `replace` directives.

| Module | Pin | Upstream commit | Released |
|---|---|---|---|
| `github.com/llm-d/llm-d-router` | `v0.11.0` | `a5cbe600ebade00cf3e9885beaf2bfacddeabce1` | 2026-09-19 |

The authoritative pin is the `go.sum` checksum, not the tag — a tag can be moved, a
checksum cannot:

```
github.com/llm-d/llm-d-router v0.11.0 h1:1z1n0ZoM+c2eMC6dewDYaZfVUFbRbIAvD65iXBUsZ7I=
github.com/llm-d/llm-d-router v0.11.0/go.mod h1:hpfxqMtD3CW5/I24TNzORPvDios0c/N5dnAJDO/+n88=
```

Verify the commit behind the tag without cloning:

```sh
curl -sSfL https://proxy.golang.org/github.com/llm-d/llm-d-router/@v/v0.11.0.info
# {"Version":"v0.11.0","Time":"2026-09-19T10:51:54Z",
#  "Origin":{"VCS":"git","URL":"https://github.com/llm-d/llm-d-router",
#            "Hash":"a5cbe600ebade00cf3e9885beaf2bfacddeabce1","Ref":"refs/tags/v0.11.0"}}
```

Three other direct requires, and one indirect, move **with** the upstream pin and must not
be bumped independently — they are upstream's own transitive versions surfaced into our
`go.mod`, and a mismatch produces the kind of error that looks like a bad image:

| Module | Pin | Why it is coupled |
|---|---|---|
| `k8s.io/component-base` | `v0.36.4` | supplies `compbasemetrics.StabilityLevel`, passed into upstream's `metricsutil.HelpMsgWithStability` |
| `sigs.k8s.io/controller-runtime` | `v0.24.1` | `ctrl.SetupSignalHandler` in `cmd/epp/main.go`; must match upstream's client-go generation |
| `sigs.k8s.io/gateway-api-inference-extension` | `v1.5.0` (indirect) | the InferencePool API group the EPP resolves; drives the `v1alpha2` vs `v1` choice in `deploy/poc/02-epp.yaml` and `deploy/poc/03-gateway.yaml` |
| `github.com/prometheus/client_golang` | `v1.23.2` | our collectors register into upstream's registry; a registry type mismatch fails at init |

### 2.2 Build toolchain

| Thing | Pin | Rule |
|---|---|---|
| `go` directive in our `go.mod` | `go 1.26.6` | must match upstream's `go` directive |
| Builder image in `Dockerfile.epp` | `golang:1.26.8` | must be **>=** upstream's `go` directive, or the build fails with a toolchain error |
| Runtime base | `gcr.io/distroless/static:nonroot` | floating tag — see §4 |

`Dockerfile.epp` is derived from upstream's `Dockerfile.epp` at v0.11.0 with three
deliberate differences, documented in the file header. Those differences are re-validated
on every re-pin, because they are statements about upstream's layout, not ours.

### 2.3 Container images

Every image reference in the repository outside `prototype/`, and whether it satisfies the
digest rule in §4. (`prototype/` is frozen and out of scope — see §7. For the record it
carries `python:3.11-slim` in `Dockerfile.mock` and `Dockerfile.wfq`, and
`envoyproxy/envoy:v1.31-latest` in `docker-compose.yaml`; none is a deliverable.)

| File | Reference | State |
|---|---|---|
| `deploy/poc/02-epp.yaml:145` | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a7...` | **satisfies** — fixed for UNI-98, same digest UNI-29/UNI-97 landed on |
| `deploy/poc/05-llmisvc-sim.yaml:185` | same digest | **satisfies** — fixed for UNI-98 |
| `deploy/poc/06-rhoai34-shape.yaml:79` | same digest | **satisfies** — fixed for UNI-98 |
| `deploy/poc/07-vllm-cpu.yaml:150` | same digest | **satisfies** — fixed for UNI-98 |
| `deploy/llmisvc.yaml:106` | `quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a7...` | **satisfies** — fixed for UNI-29; see `docs/runbook.md`'s "Publishing to Quay without a local podman" note for how this one was built |
| `deploy/poc/09-vllm-gpu.yaml:111` | same digest | **satisfies** |
| `deploy/poc/01-sim-backend.yaml:45` | `ghcr.io/llm-d/llm-d-inference-sim:v0.11.4` | version tag, not a digest — **violates**, lower risk |
| `deploy/poc/05-llmisvc-sim.yaml:70`, `deploy/poc/06-rhoai34-shape.yaml:152` | same inference-sim tag | **violates**, lower risk |
| `deploy/poc/07-vllm-cpu.yaml:59` | `registry.redhat.io/rhaii/vllm-cpu-rhel9:3.5.0` | **violates**, lower risk |
| `deploy/maas/03-postgres.yaml:57` | `registry.redhat.io/rhel9/postgresql-15:latest` | **violates** — support scaffolding, not a deliverable |
| `deploy/poc/04-loadgen.yaml:146`, `deploy/poc/10-cache-profile.yaml:83` | `registry.access.redhat.com/ubi9/ubi:latest` | **violates** — test scaffolding, not a deliverable |
| `Dockerfile.epp:51` | `gcr.io/distroless/static:nonroot` (via `BASE_IMAGE`) | **violates** — runtime base |
| `Dockerfile.epp:22` | `golang:1.26.8` | **violates** — builder image, and a build input §4 explicitly covers |
| `docs/runbook.md:103-108` | builds and pushes `:latest` **and** `:$SHA` | **violates** — the procedure itself teaches the bad habit |
| `docs/design.md:814` | `quay.io/<org>/maas-epp:v0.11.0-1` | **violates** — a printed command, also covered by §4 |

Six of these manifests also carry `imagePullPolicy: Always` (`deploy/poc/02-epp.yaml:146`,
`05-llmisvc-sim.yaml:186`, `06-rhoai34-shape.yaml:80`, `07-vllm-cpu.yaml:151`,
`deploy/llmisvc.yaml:107`, `deploy/poc/09-vllm-gpu.yaml:112`). All six now point at a digest
(fixed for UNI-98), so `Always` is harmless on every one of them — a digest cannot move,
so `Always` only re-pulls the same bytes. Before UNI-98, four of the six were `:latest`,
where the same setting made the problem worse instead: it guaranteed a restarted pod picked
up whatever the tag pointed at *now*, so two replicas of the "same" deployment could run
different binaries. That contrast was the argument for the rule in §4 in one line.

Nothing in this table is fixed by this document. It is the inventory the enforcement rule
in §4 is written against, and the per-manifest changes belong to their own tickets.

---

## 3. The upstream surface we depend on

Every exported upstream symbol this repository references, at `v0.11.0`. The **Side**
column is the one that matters for predicting breakage:

- **implement** — we satisfy this interface. Upstream *adding a method* breaks us.
- **consume** — we call it or hold a value of it. Upstream *removing or changing* it
  breaks us; adding to it does not.

**On citations.** Upstream file references carry a line number and are exact at `v0.11.0`;
they are stable for the life of the pin, which is what makes them worth checking. Our own
files are cited by **function or declaration name, not line number**, on purpose: our line
numbers move on every commit we make to `plugin.go`, so a line-pinned citation here is
wrong within days and the §5 re-pin trigger — which fires on *upstream* change — would
never catch it. An earlier revision of this document did pin our line numbers and all eight
were stale within three commits.

### 3.1 `pkg/epp/framework/interface/flowcontrol`

| Symbol | Upstream file | Side | Used at |
|---|---|---|---|
| `FairnessPolicy` | `plugins.go:51` | implement | `plugin.go` — `Pick`, `NewState` |
| `FlowQueueAccessor` | `accessors.go:29` | consume | `plugin.go`, tests |
| `PriorityBandAccessor` | `accessors.go:54` | consume | `plugin.go` |
| `FlowKey` | `flow.go:31` | consume | `plugin.go` |

The `mocks` sub-package is part of this surface too, and it is the one most likely to break
loudly:

| Symbol | Upstream file | Side | Used at |
|---|---|---|---|
| `MockFlowQueueAccessor`, `MockPriorityBandAccessor`, `MockQueueItemAccessor` (and their exported fields and func-fields) | `flowcontrol/mocks/` | consume | `conformance_test.go:43`, `harness_test.go:27` |

This is a test-only dependency, but it is an *imported* one, not a copied one (§3.8 covers
the copied case). Upstream has no stability promise on a mocks package at all, and a change
to a func-field signature is a compile break in our test suite. Walk it on every re-pin.

### 3.2 `pkg/epp/framework/interface/requestcontrol`

| Symbol | Upstream file | Side | Used at |
|---|---|---|---|
| `PreRequest` | `plugins.go:70` | implement | `plugin.go` — `PreRequest` |
| `ResponseBodyProcessor` | `plugins.go:98` | implement | `plugin.go` — `ResponseBody` |
| `RequestHeaderProcessor` | `plugins.go:130` | implement | `plugin.go` — `RequestHeader` |
| `Response` | `types.go:52` | consume | `plugin.go` |
| `TerminationCauseNatural` | `types.go:36` | consume | `plugin.go` |
| `TerminationCauseClientDisconnect` | `types.go:42` | consume | `plugin.go` |

These three extension points are **not** named in the EPP config. `(*requestcontrol.Config).AddPlugins`
type-asserts every instantiated plugin against each extension point, so declaring the
type once in the top-level `plugins:` list wires all of them. A rename of any of these
interfaces therefore does not fail the build — it silently stops wiring the hook. That is
the highest-severity drift class in this table.

### 3.3 `pkg/epp/framework/interface/scheduling`

| Symbol | Upstream file | Side | Used at |
|---|---|---|---|
| `InferenceRequest` | `types.go:47` | consume | throughout — 23 references |
| `SchedulingResult` | `types.go:177` | consume | `plugin.go` — `PreRequest` signature |
| `ReadRequestAttribute[T]` | `attributes.go:75` | consume | `plugin.go` — `ResponseBody`, `RequestHeader` |

### 3.4 `pkg/epp/framework/interface/requesthandling`

| Symbol | Upstream file | Side | Used at |
|---|---|---|---|
| `Usage` | `types.go:816` | consume | `plugin.go` true-up, reached through `fwkrc.Response.Usage` |
| `InferenceRequestBody` | `types.go:96` | consume | `harness_test.go`, `plugin_test.go` |
| `PromptTokenDetails` | `types.go:823` | consume | `plugin.go` cached-token discount, via `Response.Usage.PromptTokenDetails`; `harness_test.go` |

`plugin.go` does not import `requesthandling` directly — it reaches all three of these
through the `fwkrc.Response` value handed to `ResponseBody`. The tests are the only direct
importers. That matters for the re-pin walk: a `grep` for the import path will not find
these uses.

### 3.5 `pkg/epp/framework/interface/plugin`

| Symbol | Upstream file | Side | Used at |
|---|---|---|---|
| `Plugin` | `plugins.go:24` | implement | `plugin.go` |
| `StateDumper` | `plugins.go:67` | implement | `plugin.go` — `DumpState` |
| `TypedName` | `typedname.go:24` | consume | `plugin.go` — `TypedName` |
| `Handle` | `handle.go:28` | consume | factory |
| `Register` | `registry.go:52` | consume | `cmd/epp/main.go` — `run` |
| `StabilityBeta` | `stability.go:26` | consume | `cmd/epp/main.go` — `run` |
| `StrictDecoder` | `registry.go:42` | consume | factory |
| `NewDataKey` | `datakey.go:29` | consume | `plugin.go` — package-level data keys |

We do **not** implement `ProducerPlugin` (`plugins.go:84`) or `ConsumerPlugin`
(`plugins.go:75`), both of which exist at v0.11.0 and are optional there. §6 explains why
that omission becomes a defect at v1.0.0.

### 3.6 `pkg/epp/framework/interface/datalayer`

| Symbol | Upstream file | Side | Used at |
|---|---|---|---|
| `EndpointMetadata` | `endpoint_metadata.go:33` | consume | `plugin.go` |

### 3.7 Outside the `interface/` tree — higher risk

The packages above are upstream's declared extension surface. The four below are not: they
are ordinary internal-facing packages that happen to be exported, with no stability intent
behind them at all. Treat any change here as expected rather than exceptional.

| Symbol | Upstream file | Side | Used at |
|---|---|---|---|
| `runner.NewRunner` | `cmd/epp/runner/runner.go:168` | consume | `cmd/epp/main.go` — `run` |
| `metricsutil.HelpMsgWithStability` | `pkg/common/observability/metrics/metrics.go:32` | consume | `metrics.go` — `help` |
| `metricsutil.BoundFairnessID` | `pkg/common/observability/metrics/cardinality.go:124` | consume | `metrics.go` — `boundID` |
| `eppmetrics.LLMDRouterEndpointPickerSubsystem` | `pkg/epp/metrics/llm_d_router_metrics.go:28` | consume | `metrics.go` — all 12 collectors |

Importing `cmd/epp/runner` is what makes this a standalone EPP rather than a library, and
it is also what pulls the whole 107-module indirect graph. It is the single most
consequential import in the repository.

### 3.8 Copied, not imported

`pkg/fairness/weightedlas/conformance_test.go` contains four table cases **adapted** from
upstream `pkg/epp/framework/plugins/flowcontrol/fairness/functional_test.go` — adapted, not
copied byte-for-byte, which is what the file header says and which makes a mechanical diff
useless. They are
copied because `runPickConformanceTests` lives in a `_test.go` file and cannot cross a
module boundary. **Nothing detects drift in a copy.** Re-reading that upstream file is a
mandatory step of the re-pin procedure in §5.

### 3.9 Configuration surface

Not Go API, but it breaks the same way and from the same release:

| Thing | Current value | Where |
|---|---|---|
| Config API group | `llm-d.ai/v1alpha1` | `deploy/epp-config.yaml:17`, `deploy/poc/00-config.yaml:20` |
| Feature gate | `flowControl` — constant at `pkg/epp/flowcontrol/config.go:28`, **disabled by default** (`cmd/epp/runner/runner.go:748` registers it `false`) | `deploy/epp-config.yaml:19` |
| Compat flag shim | `--model-server-metrics-scheme`, absent upstream, templated by the RHOAI 3.4 preset | `cmd/epp/main.go` — `registerDownstreamCompatFlags` |

`featureGates: [flowControl]` in our ConfigMap is **load-bearing**. The gate is off by
default in both v0.11.0 and v1.0.0. Drop that line and the EPP still starts, still loads
the config, logs one `WARNING: the flowControl config section is set but the flowControl
feature gate is disabled` line, and runs with no flow control at all — our plugin is never
consulted. Watch this value on every re-pin: if upstream flips the default to on, or
renames the gate, the symptom in both directions is a fairness policy that appears healthy
and does nothing.

**Two config API groups, and both have already moved at v1.0.0.** At our pin, the
`inference.networking.x-k8s.io/v1alpha1` group still loads: it is registered as
`deprecatedSchemeGroupVersion` (`pkg/epp/config/loader/configloader.go:54`, already carrying
upstream's `// TODO: deprecated should be clean up`) and logs a deprecation line on every
startup. **v1.0.0 removes it outright** — the symbol is gone from the loader and upstream's
own test asserts the new behaviour, ``no kind "EndpointPickerConfig" is registered for
version "inference.networking.x-k8s.io/v1alpha1"``. That is a **hard load error, not a
silent failure**; the EPP will not start. We are unaffected, because our manifests use
`llm-d.ai/v1alpha1`, but anyone who copied an older upstream example is not.

Our own group is on the same path one release behind. v1.0.0 introduces `llm-d.ai/v1`
(`apix/config/v1`) as the canonical config API and keeps `llm-d.ai/v1alpha1`
(`apix/config/v1alpha1`) installed but deprecated — the loader logs `DEPRECATION: ... is
deprecated and is removed in a later release` and names `llm-d.ai/v1` as the replacement.
So the value in `deploy/epp-config.yaml:17` and `deploy/poc/00-config.yaml:20` has a
removal announced against it. Migrating to `llm-d.ai/v1` is part of the v1.0.0 re-pin, not
a separate decision.

The compat shim has an explicit failure mode on re-pin: **if upstream ever adds a real
flag named `--model-server-metrics-scheme`, the duplicate pflag registration panics at
startup.** Checking for it is a step in §5.

---

## 4. Image-tag discipline

### The rule

**Every image reference in a deliverable is a digest.** `name@sha256:...`, never
`name:tag`. This applies to manifests under `deploy/`, to build inputs in
`Dockerfile.epp`, and to commands printed in `docs/`.

A tag is a mutable pointer. A commit-named tag such as `:aef33a5` is still mutable — it
records the *intent* that this is commit `aef33a5`, it does not guarantee it. Upstream's
own `docs/verifying-releases.md` makes the same point for the opposite reason: their build
workflow repoints a tag seconds before the attestation for the new digest is published, so
tag-based verification has a window in which it is simply wrong.

Three consequences specific to this POC:

- `imagePullPolicy: Always` on a floating tag means a pod restart can change the running
  binary with no manifest change and no audit trail. Six of our manifests set `Always`;
  all six are now digest-pinned (fixed for UNI-98), where `Always` is inert. Before
  UNI-98, four of them sat on a `:latest` tag and were exposed to this. See the §2.3
  inventory for the list.
- The in-cluster reference `image-registry.openshift-image-registry.svc:5000/.../maas-epp:latest`
  cannot be transferred at all. It names a registry that does not exist outside this
  cluster, and the GPU nodes cannot reach it even inside this one
  (`dial tcp 172.30.x:5000: i/o timeout`), which is why the GPU manifests point at Quay.
  No manifest in this repository references it any longer (UNI-98).
- An air-gapped mirror is populated by digest. A manifest that names a tag cannot be
  matched to an `IDMS`/`ICSP` entry deterministically, which makes the POC's stated
  air-gap goal unverifiable rather than merely untested.

### Getting a digest

After a push, read the digest back from the registry rather than trusting local state:

```sh
# from a workstation with registry credentials
skopeo inspect docker://quay.io/rh-ee-dsivan/maas-fair-share:$SHA --format '{{.Digest}}'

# or, from the cluster, for an image already referenced by a running pod
oc image info quay.io/rh-ee-dsivan/maas-fair-share:$SHA --output json | jq -r .digest
```

`oc image info` is also the only way to read the `version`/`url`/`vcs-ref` labels off a
digest, which is how the RHOAI-to-upstream version mapping in `README.md` was established.

Then pin the manifest to `name@sha256:...` and record the tag it came from in a comment
beside it, so a human can still tell which build it was.

### Who enforces it, and where

| Gate | Owner | Action |
|---|---|---|
| Change review | **Reviewer/QA** | Reject any change introducing or retaining a non-digest image reference in `deploy/` or `Dockerfile.epp`. This is the enforcement point; there is no CI to do it (§7). |
| Rebuild procedure | **Engineer** | `docs/runbook.md` must print the digest after push and the manifest edit must use it. The current procedure pushes `:latest` and must stop. |
| Re-pin | **Engineer** | Every image touched by a re-pin is re-pinned by digest in the same commit. |
| Exception | **CTO** | A non-digest reference ships only with an inline comment giving the reason and a linked ticket to remove it. Test scaffolding (`ubi9/ubi`, `postgresql-15`) is the expected case. |

The exception carve-out is deliberate: a rule with no exception path gets ignored
wholesale. A `ubi9` loadgen image is not an air-gap deliverable and pretending otherwise
costs credibility for the references that are.

---

## 5. The maintenance process

### Owner and cadence

| | |
|---|---|
| Accountable | **CTO** |
| Performs the check | **Engineer** |
| Reviews the result | **Reviewer/QA** |
| Cadence | **Monthly**, and on any trigger in the list below |

Monthly, not quarterly. The quarterly figure in `docs/design.md` item 11 predates evidence.
Observed upstream minor-release intervals:

| From | To | Days |
|---|---|---|
| v0.9.0 (2026-06-16) | v0.10.0 (2026-08-17) | 62 |
| v0.10.0 | v0.11.0 (2026-09-19) | 33 |
| v0.11.0 | v1.0.0 (2026-10-15) | 26 |

The cadence is accelerating and already runs under a month. A 90-day cycle would skip two
to three minor releases per pass, which defeats the purpose: the value of the check is
reviewing one diff at a time, not a quarter of accumulated change. A monthly check that
finds nothing costs about fifteen minutes.

**The check is a calendar obligation on a named role, not an automated job.** No automation
exists to do it — see §7. The CTO is accountable for the check happening whether or not a
tool ever reminds anyone.

### What the check is

Not "is there a new release". That question is answered by one command. The check is:
**does the delta between our pin and upstream HEAD touch anything in §3?**

```sh
# 1. Is there anything newer than the pin?
curl -sSfL https://proxy.golang.org/github.com/llm-d/llm-d-router/@v/list | sort -V | tail -5

# 2. Fetch both module zips and diff the declared extension surface.
#    Needs no clone, no credentials, and no Go toolchain.
for V in v0.11.0 <new>; do
  curl -sSfL -o "$V.zip" "https://proxy.golang.org/github.com/llm-d/llm-d-router/@v/$V.zip"
  mkdir -p "x$V" && (cd "x$V" && unzip -q "../$V.zip")
done
diff -r "xv0.11.0/github.com/llm-d/llm-d-router@v0.11.0/pkg/epp/framework/interface" \
        "x<new>/github.com/llm-d/llm-d-router@<new>/pkg/epp/framework/interface"
```

Record the answer even when it is "no change". An unrecorded check is indistinguishable
from one that never happened.

### Triggers that force a check regardless of cadence

1. A new upstream **minor or major** release. Patch releases are checked but rarely act.
2. A **RHOAI release bump** on the target cluster. The preset templates the scheduler
   command line, so a preset change can break us without upstream changing at all — this
   is how `--model-server-metrics-scheme` was found.
3. A **CVE** in the module graph or either base image.
4. **Any build failure** attributed to a toolchain or dependency version.
5. Pod `CrashLoopBackOff` at startup **before the first config line is parsed** — the
   signature of an unknown-flag or plugin-stability rejection.
6. The EPP starting cleanly but a fairness metric going flat — the signature of a hook
   that silently stopped being wired (§3.2) or an attribute write being silently dropped
   (§6).

### The re-pin procedure

A re-pin is one commit. If any step cannot be completed, the re-pin does not land.

1. **Bump together.** `go.mod` require, `go.sum`, and the `Dockerfile.epp` builder image.
   The builder's Go version must be >= upstream's `go` directive. They are never bumped
   separately.
2. **Diff the extension surface.** The `diff -r` above, over
   `pkg/epp/framework/interface/`. Read every hunk, not just the ones that fail to compile.
3. **Diff the five `plugins.go` files** specifically —
   `flowcontrol/`, `plugin/`, `requestcontrol/`, `requesthandling/`, `scheduling/`. These
   define the extension points we are type-asserted against.
4. **Walk the §3 inventory.** For each symbol, confirm it still exists with a compatible
   shape, and check the **Side** column: an added method breaks what we implement, a
   removed field breaks what we consume.
5. **Diff the four non-interface symbols in §3.7.** They have no stability promise.
6. **Re-read the copied conformance cases** against upstream
   `pkg/epp/framework/plugins/flowcontrol/fairness/functional_test.go` and sync them (§3.8).
7. **Check the compat shim.** If upstream has added a real `--model-server-metrics-scheme`
   flag, delete `registerDownstreamCompatFlags()` — leaving it panics at startup.
8. **Check the config surface.** Feature gate name and default; the config API group our
   manifests declare, and whether it is still current or newly deprecated; and whether the
   deprecated `inference.networking.x-k8s.io` group still loads. For v1.0.0 this step is
   already answered — see §3.9 and §6 Finding 4 — and it is the step that produced the
   answer, which is the argument for keeping it in the list.
9. **Re-run the tests.** `go test ./...` — conformance, proportionality, work conservation,
   idle clamp, decay, grouping.
10. **Rebuild and re-pin by digest.** Per §4. Every manifest the new image touches.
11. **Re-run the scenario matrix** on a cluster, and compare against the numbers in
    `docs/poc-results.md`. A re-pin that compiles and unit-tests clean can still change
    behaviour — step 9 would not have caught the §6 example.
12. **Update this document.** §2 and §3 are version-specific and go stale the moment the
    pin moves.

A re-pin is not the only thing that makes this document stale. §2.3's file-and-line image
inventory and §3's "Used at" column describe *our* tree, so they drift on our own commits
with no upstream change at all — and the triggers above will not fire. Any change to
`deploy/`, `Dockerfile.epp`, or `pkg/fairness/weightedlas/plugin.go` should refresh the
affected rows in the same commit; Reviewer/QA checks for it at the same gate that enforces
§4. This is why §3 cites our code by name rather than by line.

### Routing a breaking change into a ticket

When a check finds something, the Engineer files one ticket per break, not one per release.
Each ticket states:

- the upstream version that introduced it and the commit;
- the §3 symbol or behaviour affected, by name;
- whether it is a **compile** break, a **silent wiring** break, or a **silent behavioural**
  break — in ascending order of severity, because the last one survives our test suite;
- what in this repository must change;
- whether the current pin is still safe to run meanwhile.

The ticket blocks the re-pin. The re-pin does not land with a known break outstanding, and
the pin stays where it is until the ticket closes. A pin that is old and understood is
safer than one that is current and unexamined.

If the check finds nothing, record that: version checked, date, checker, "no change to the
§3 surface". One line.

---

## 6. Worked example: the v0.11.0 → v1.0.0 delta

This procedure was run once against upstream v1.0.0 while writing this document. It is
recorded here both as evidence that the process produces something and as the reference for
how a finding is written up.

**Outcome: five findings, one of them a silent behavioural break that our test suite does
not catch.**

### Finding 1 — `plugin.Handle` gained a method. Does not affect us.

`Handle` gained `RefreshMetricsInterval() time.Duration`
(`pkg/epp/framework/interface/plugin/handle.go`). Adding a method to an interface breaks
every implementer. §3.5 records `Handle` as **consume** — we receive one in the factory and
never implement it — so this is invisible to us. This is exactly the distinction the Side
column exists to make, and the reason the column is worth maintaining.

### Finding 2 — new extension points, and some removals. No action, but not "all additive".

Additions: `requestcontrol` gained `Responder`, `RequestLine`, `LocalResponse`.
`requesthandling` gained `RequestFieldError` and a `JSONValidated` field on `ParseResult`.
`flowcontrol` gained `DispatchReservationTracker`, `BandSelectionPolicy` and
`BandSelectionParameters`.

Removals and changes, which the first pass over this delta missed by reading only for new
symbols:

- `scheduling.Modality` and `scheduling.ModalityImage` are **removed** (they were aliases
  at `scheduling/types.go:33,35`).
- `requesthandling.Modality`, `ModalityImage`, `ModalityAudio` and `ModalityVideo` are
  **removed** and relocated to `pkg/common/request` (`modality.go`).
- `AnthropicContentBlock.Source` changes type from `*AnthropicImageSource` to
  `json.RawMessage`.

We reference none of them, so there is still no action. The correction matters anyway: a
removal reported as an addition tells the next reader the wrong thing about what this
release did, and the next person to reach for a `Modality` constant would follow a stale
table. **Read a delta for what left, not only for what arrived.**

There is also one behavioural change with no signature change at all: `UsageLimitPolicy`'s
contract moved from "the dispatch loop visits bands highest-to-lowest and **stops at the
first gated band**" (`flowcontrol/plugins.go:169-180` at v0.11.0) to gating decided **per
band, independently** (`plugins.go:186-196` at v1.0.0). We do not implement
`UsageLimitPolicy`, but it governs the band loop that feeds our `FairnessPolicy`, so the
order in which our `Pick` is offered bands changes. Nothing to fix; something to know
before reading a fairness metric after a re-pin.

### Finding 3 — request attributes are now confined, and our writes would be silently dropped

This is the one that matters.

v1.0.0 adds `AttributeScope` to `pkg/epp/framework/interface/scheduling/attributes.go`.
`InferenceRequest.PutAttribute` now consults a scope, and:

```go
func (r *InferenceRequest) PutAttribute(key fwkplugin.DataKey, value any) {
	if r.scope != nil && !r.scope.AllowPut(key) {
		return
	}
	...
```

The scope is built by `buildScopeSpec` in `pkg/epp/datalayer/endpoint_scope.go:239`. A
plugin that implements neither `ProducerPlugin` nor `ConsumerPlugin` gets **empty** allow
sets — every write is dropped, every read resolves as absent. Upstream's own comment
settles the obvious objection: *"A plugin that declares nothing reaches nothing: an absent
declaration is a statement that the plugin exchanges no data, not a request to be exempt."*

`datalayer.ScopeRequest` is called at three places in v1.0.0, but only one of them applies
to a registered plugin like ours: `pkg/epp/requestcontrol/director.go:704`, the
**`PreRequest`** extension point. The other two (`pkg/epp/scheduling/scheduler.go:89` and
`:133`) scope the scheduler's own profile handler.

Our plugin:

- writes `provisionalChargeKey` inside `PreRequest` (`plugin.go`, the `PutAttribute` call
  in `PreRequest`);
- reads it back in `ResponseBody` to reverse the provisional charge at true-up (the
  `ReadRequestAttribute[provisionalCharge]` call);
- declares neither `Produces()` nor `Consumes()` — neither method appears anywhere in the
  repository (§3.5).

The same pattern applies to `correlationKey`, which `RequestHeader` also writes through
`PutAttribute`. `RequestHeader` is not a scoped extension point, so that write survives —
but it survives by accident, not by design. Upstream has three `ScopeRequest` call sites at
v1.0.0 where v0.11.0 had none; the direction of travel is more scoping, not less. Fixing
Finding 3 by declaring `Produces()` fixes this one at the same time.

So on v1.0.0 the write is dropped, the true-up finds no provisional charge, and every
request is accounted at its estimate with no correction. Token-weighted fairness quietly
degrades to estimate-weighted fairness.

Classify it precisely:

| | |
|---|---|
| Compile break | **No.** `PutAttribute` keeps its signature. |
| Test break | **No.** `harness_test.go` and `conformance_test.go` construct `InferenceRequest` values directly, so no scope is ever attached and the write succeeds in tests. |
| Runtime break | **Yes, silent.** Upstream logs a violation and increments a counter; nothing in our code notices. |

A re-pin that did steps 1, 2 and 9 of §5 and stopped would have shipped this. It is caught
by step 4 — walking the inventory and reading the semantics, not only the signatures — and
would have been caught by step 11.

**The code fix is small**: implement `ProducerPlugin` and declare `provisionalChargeKey`
(and `correlationKey`) in `Produces()`. The *re-pin* it sits inside is not small — see
Finding 5. It is not made here. This document is a process deliverable and changing plugin
behaviour is not in its scope; the finding is routed into its own ticket exactly as §5
prescribes. Until that ticket lands, **v0.11.0 remains the correct pin** and v1.0.0 must
not be adopted.

### Finding 4 — config API groups moved. One hard break, one deprecation aimed at us.

v1.0.0 removes the `inference.networking.x-k8s.io/v1alpha1` group entirely, and adds
`llm-d.ai/v1` while deprecating the `llm-d.ai/v1alpha1` our ConfigMaps declare. Details in
§3.9. Classification: **compile break, no. Config load break, yes — but loud**, which makes
it the least dangerous of these five. We are not hit by the removal; we are hit by the
deprecation, one release out.

This is the finding the first pass over the delta missed, and §5 step 8 is the step that
mandates looking for it. A procedure is only worth writing down if it catches something its
author would otherwise have skipped; this is that case, recorded rather than quietly fixed.

### Finding 5 — the Go toolchain moves with the pin

Upstream's `go` directive goes **`1.26.6` → `1.27.2`**. By §2.2's own rules — our `go.mod`
must match upstream's directive, and the `Dockerfile.epp` builder must be `>=` it —
adopting v1.0.0 forces a `go.mod` bump *and* a builder bump above the current
`golang:1.26.8`, in the same commit, per §5 step 1.

Worth stating because it is the step most likely to be discovered late: the symptom of
missing it is a toolchain error at build time that reads like a broken base image rather
than a version mismatch.

### What this says about the pin

v1.0.0 is desirable — it converts the whole exported API from "no promise" to Go semver,
which is the largest single reduction available in the risk this document exists to manage.
It is also the first release that can break us silently. Both facts argue for the same
thing: move to it deliberately, through the §5 procedure, with the Finding 3 ticket closed
first.

The size of that move is now visible, and it is not a one-line bump. A v1.0.0 re-pin is a
single commit carrying: the `Produces()` declaration (Finding 3), the `go.mod` and
`Dockerfile.epp` toolchain bump (Finding 5), the `llm-d.ai/v1alpha1` → `llm-d.ai/v1` config
migration (Finding 4), a re-read of the adapted conformance cases (§3.8), and a cluster
re-run of the scenario matrix, because Finding 3 is exactly the class of change that
compiles and unit-tests clean. Scope it as that, not as a dependency bump.

---

## 7. What this process does not cover

Stated plainly, because a gap that is not written down reads as a gap nobody looked for.

- **There is no automation, and standing any up is a board request.** The repository has
  no `.gitlab-ci.yml` at any commit to date, including current `main`. Whether the company
  GitLab has a runner available at
  all is *unverified* — the CTO's read token is clone-scoped and the instance API returns
  `403 insufficient_scope` — so treat runner availability as an open question rather than
  a known no. The
  Dependabot rule proposed in `docs/design.md` item 11 and `docs/poc-results.md` item 13 is
  not available: Dependabot is a GitHub product, this repository lives on the company's
  self-hosted GitLab, and that instance is reachable only from the cluster subnet and the
  operator's workstation. GitLab's own dependency scanning and Renovate both need a CI
  runner plus egress to `proxy.golang.org`. **Standing up a runner with controlled egress
  is an infrastructure request for the board, not something to assume.** Until then the
  monthly check in §5 is manual and the calendar obligation on the CTO is the only control.
- **Nothing here verifies supply-chain provenance.** Upstream publishes SLSA attestations
  and SBOMs for `ghcr.io/llm-d/llm-d-router-*` images from v0.11.0 onward
  (`docs/verifying-releases.md`), but we build our own image and do not consume theirs, and
  we produce neither attestation nor SBOM for `maas-epp`. For an air-gapped target that is
  likely to be a requirement rather than a nicety. Out of scope here; worth its own ticket.
- **The 107 indirect modules are not individually tracked.** They move as one block with
  the upstream pin. A CVE in one of them is trigger 3 in §5 and is handled reactively. We
  have no SCA tooling, for the same no-runner reason.
- **No process can cover the RHOAI preset.** Red Hat's downstream scheduler preset is
  templated by the cluster's operator version, not by anything in this repository. Trigger
  2 exists for it, but the only real detection is running `deploy/poc/06-rhoai34-shape.yaml`
  against the new preset.
- **`prototype/` is frozen and deliberately unmaintained.** Its pins are not in scope and
  should not be bumped.

---

## 8. Quick reference

| Question | Answer |
|---|---|
| What are we pinned to? | `llm-d-router v0.11.0`, commit `a5cbe600`, released 2026-09-19 |
| What is the newest upstream? | `v1.0.0`, commit `b9393d1a`, released 2026-10-15 — **do not adopt yet**, see §6. Adopting it is a five-part commit, not a bump |
| Who checks, how often? | Engineer performs, CTO accountable, Reviewer/QA reviews. Monthly, plus the §5 triggers |
| What is the check? | `diff -r` of `pkg/epp/framework/interface/` between pin and HEAD, then walk §3 |
| What breaks us silently? | A renamed `requestcontrol` extension point (§3.2); a behavioural change behind an unchanged signature (§6) |
| Image rule | Digests everywhere. Reviewer/QA enforces at change review; CTO signs exceptions |
| Where is the automation? | There is none, and there cannot be until a CI runner exists (§7) |
