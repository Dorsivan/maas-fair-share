# Gateway control: `x-llm-d-inference-objective` is overwritten, not trusted from the client

Closes outstanding-work item 15 in [poc-results.md](poc-results.md#outstanding-work).
See also [design.md, "Security: headers must be stripped at the
gateway"](design.md), which flagged this header as "the sneaky one" when the
fairness-id spoofing defenses were designed, but left it unaddressed.

## The vulnerability

`x-llm-d-inference-objective` selects a request's **priority band**.
Fairness (the weighted split this whole repo measures) is enforced **only
within a band** — a request in a higher band is served ahead of every
request in ours, entirely bypassing the weights. A client that can set this
header to the name of a high-priority `InferenceObjective` gets head-of-line
treatment for free.

The EPP resolves it with an alias table, in this order
(`github.com/llm-d/llm-d-router` v0.11.0,
`pkg/epp/metadata/consts.go:44-47,77-107`):

| Order | Header | Who sets it |
|---|---|---|
| 1st (wins if present) | `x-llm-d-inference-objective` | **nobody, on this cluster — a client can set it directly** |
| 2nd (fallback only) | `x-gateway-inference-objective` | Authorino, from the authenticated identity (`maas-poc-gateway-authn`) |

```go
// GetLowerCaseHeaderValue returns a header value from a lower-case header
// map using the current name first, then deprecated aliases.
func GetLowerCaseHeaderValue(headers map[string]string, key string) (string, bool) {
	key = strings.ToLower(key)
	if aliases, ok := headerAliases[key]; ok {
		for _, alias := range aliases {
			if value, ok := headers[alias]; ok {
				return value, true
			}
		}
		return "", false
	}
	...
}
```

pinned by the upstream test `TestGetLowerCaseHeaderValuePrefersCurrentName`
in the same package. The EPP never learns whether a header came from the
client or from Authorino — it only ever sees one flattened map — so setting
the *old* alias (which is all `maas-poc-gateway-authn` does today) defends
nothing: a client that sets the *new* name wins outright.

This is structurally different from the fairness-ID spoofing risk the design
already defends against. For `FairnessID`, `pkg/fairness/weightedlas`'s
`PreRequest` overwrites the value unconditionally from the authenticated
`X-MaaS-Subscription` header, regardless of what alias the EPP's own
resolution picked — see `plugin.go:210` and design.md. There is no equivalent
plugin seam for the objective/priority header: `director.go:177`
(`getInferenceObjective`) resolves it and sets `reqCtx.Priority` **before**
any configured plugin runs. The only point left to intervene is upstream of
the EPP, in the gateway.

## Live proof (2026-10-19, against `maas-gateway-maas-fairness-poc.apps.ocp.paladinaura.com`)

Authenticated as `system:serviceaccount:paperclip:poc-agent` (a plain
Kubernetes token — it passes `maas-poc-gateway-authn`'s
`kubernetesTokenReview` authentication rule and its
`inference-access` SubjectAccessReview, since this service account can
`get llminferenceservices` in `maas-fairness-poc`; no MaaS `sk-oai` API key
was needed or used).

**Baseline**, no forged header:

```sh
curl -sSk -X POST \
  "https://maas-gateway-maas-fairness-poc.apps.ocp.paladinaura.com/maas-fairness-poc/maas-vllm-cpu/v1/chat/completions" \
  -H "Authorization: Bearer $OPENSHIFT_TOKEN" -H "Content-Type: application/json" \
  -d '{"model":"llama-3-1-8b","messages":[{"role":"user","content":"baseline, no forged header"}],"max_tokens":5}'
# HTTP 200, usage.prompt_tokens: 34
```

**Forged header**, same request plus `x-llm-d-inference-objective:
exploit-high-priority`:

```sh
curl -sSk -X POST \
  "https://maas-gateway-maas-fairness-poc.apps.ocp.paladinaura.com/maas-fairness-poc/maas-vllm-cpu/v1/chat/completions" \
  -H "Authorization: Bearer $OPENSHIFT_TOKEN" -H "Content-Type: application/json" \
  -H "x-llm-d-inference-objective: exploit-high-priority" \
  -d '{"model":"llama-3-1-8b","messages":[{"role":"user","content":"forged objective header"}],"max_tokens":5}'
# HTTP 200, usage.prompt_tokens: 33 -- served identically, nothing in the
# chain inspected, rejected, or stripped the header.
```

Both requests return 200 with no observable difference in treatment, which is
exactly the "fails open silently" risk named in the ticket: there is no
error, no log line visible at this cluster's configured log level
(`DEFAULT`, V=2 — the line that would show the resolved `objectiveKey` and
`priority`, `director.go:237`'s `"LLM request assembled"`, is logged at
`DEBUG`, V=4, and this ServiceAccount cannot raise the EPP's verbosity; see
"What was not verified" below), and no metric that distinguishes the two
requests. The only way to have caught this before the ticket was filed was to
read the header-alias table in the vendored dependency.

Confirmed by static inspection that nothing in the request path references
the new header name at all, which independently explains why neither curl
call above behaved differently:

```sh
$ grep -ri "x-llm-d-inference-objective" <(oc get httproute,gateway,authpolicy -n maas-fairness-poc -o yaml)
# (no output)
```

## The fix

Add one key to the **existing** Gateway-scoped `maas-poc-gateway-authn`
AuthPolicy's `response.success.headers`, mirroring the rule already there for
the deprecated alias:

```yaml
x-llm-d-inference-objective:
  metrics: false
  plain:
    expression: auth.identity.objective
  priority: 0
```

The full patch, the exact `oc patch` invocation, and why this must be a
merge patch rather than a new resource (Kuadrant allows one AuthPolicy per
`targetRef`, and this one is controller-owned) are in
[`deploy/maas/09-objective-header-stripping.patch.yaml`](../deploy/maas/09-objective-header-stripping.patch.yaml).

Because the policy is attached to the **Gateway**, not to any one
`HTTPRoute`, this one patch covers every route that currently sits behind
`maas-poc-gateway` (`maas-poc-route`, `maas-vllm-cpu-kserve-route`,
`maas-vllm-gpu-kserve-route`) and every route KServe generates for it later.

**Why overwriting the header is safe to do unconditionally, not just when
absent:** `response.success.headers` entries are sent to Envoy as
`OkHttpResponse.headers` (`envoy.service.auth.v3`), which — unlike the
similarly-named `response_headers_to_add` field used for the downstream
client response — defaults `append` to **false**, i.e. override, when the
`HeaderValueOption.append_action` is left unset. Authorino's
`buildResponseHeaders` (`pkg/service/auth.go`,
`Kuadrant/authorino@main`) does exactly that: it builds each
`HeaderValueOption{Header: {Key, Value}}` without ever setting an append
action. So a value set here always replaces a same-named header already on
the request, including one supplied by the client, before Envoy's ext_proc
filter (the EPP) ever reads it. This is the same mechanism
`x-gateway-inference-fairness-id` already relies on, and which
[poc-results.md](poc-results.md#maas-now-governs-the-gateway-and-it-validates-a-design-decision)
already observed in practice ("the gateway always sets that header, and to
the same constant for every caller").

## The conformance check

[`conformance/gatewayheaders`](../conformance/gatewayheaders) scans a set of
Gateway API / Kuadrant manifests and fails loudly — one line per offending
route, non-zero exit — if any `HTTPRoute` with an `InferencePool` backendRef
is not covered by an `AuthPolicy`, attached to that route or its parent
`Gateway`, that overwrites `x-llm-d-inference-objective`. A route reachable
only through a plain `Service` backendRef never passes through the EPP and is
correctly ignored.

```sh
(cd conformance/gatewayheaders && go test ./...)     # the check's own unit tests, offline
```

### Building this check air-gapped

`conformance/gatewayheaders` and `cmd/gateway-header-check` are each their
own Go module, separate from the repository root. The root module compiles
the EPP against `github.com/llm-d/llm-d-router` and deliberately does not
vendor it (`docs/version-pinning.md`: "we do not fork upstream and we do not
vendor it: we compile against it") — that pulls in roughly 400 modules, and
`go mod vendor` at the root would vendor all of them, reopening a decision
this repo made on purpose.

This checker's only non-stdlib dependency is `sigs.k8s.io/yaml` (plus
`testify` in its own tests), so it gets its own small `go.mod` and a
committed `vendor/` directory instead. The root `.gitignore` excludes
`vendor/` everywhere, with an explicit carve-out for these two paths — see
the comment there. Because each module has its own `go.mod`, `go build`
and `go test` run from inside either directory pick up `vendor/`
automatically (Go does this whenever `vendor/modules.txt` is present and
consistent — no flags needed), and need no network or module proxy:

```sh
(cd conformance/gatewayheaders && GOPROXY=off go test ./...)                              # ok
(cd cmd/gateway-header-check && GOPROXY=off go build -o ../../bin/gateway-header-check .)  # builds
```

`GOPROXY=off` above is there to prove the point, not because it is required
day to day. The nested module boundary is also why this is the one place in
the repository where `go run ./cmd/gateway-header-check` does **not** work
from the repository root — `cmd/gateway-header-check` is not part of the
root module from the root module's point of view. Build the binary once as
shown above; every other command in this document and the rest of the repo
runs it as `bin/gateway-header-check` from the repository root (that path is
git-ignored, same as any other Go build output — rebuild it after a clean
checkout).

### Why this has to run against a live snapshot to mean anything here

The real `HTTPRoute`s on this cluster
(`maas-vllm-cpu-kserve-route`, `maas-vllm-gpu-kserve-route`) and the
`AuthPolicy` that protects them (`maas-poc-gateway-authn`) are generated by
`odh-model-controller`/KServe when an `LLMInferenceService` is reconciled —
**none of them are checked into this repository**. Scanning `deploy/*.yaml`
alone would only ever see `deploy/poc/03-gateway.yaml`'s pre-MaaS direct rig,
which predates the AuthPolicy integration entirely and genuinely has no
header-stripping control of any kind (see "What this does not cover" below).
Run the check against the cluster, not just the repo:

```sh
oc --token="$OPENSHIFT_TOKEN" --server=https://api.ocp.paladinaura.com:6443 \
  get httproute,gateway,authpolicy -n maas-fairness-poc -o yaml \
  | bin/gateway-header-check -
```

### Demonstrated failing, as the ticket requires

Against a deliberately non-stripping route
(`conformance/gatewayheaders/testdata/bad/old-header-only.yaml` — the
pre-fix shape of `maas-poc-gateway-authn`, overwriting only the deprecated
alias):

```
$ bin/gateway-header-check conformance/gatewayheaders/testdata/bad/old-header-only.yaml
gateway-header-check: FAIL -- 1 route(s) do not overwrite x-llm-d-inference-objective:
  - bad-ns/half-fixed-route: routes to an InferencePool but no AuthPolicy on this route or its parent Gateway overwrites x-llm-d-inference-objective
exit status 1
```

Against the real, unpatched cluster, captured 2026-10-19 (`oc get
httproute,gateway,authpolicy -n maas-fairness-poc -o yaml` then the same
again for `-n openshift-ingress`, concatenated with a `---` separator):

```
$ bin/gateway-header-check live-snapshot.yaml
gateway-header-check: FAIL -- 3 route(s) do not overwrite x-llm-d-inference-objective:
  - maas-fairness-poc/maas-poc-route: routes to an InferencePool but no AuthPolicy on this route or its parent Gateway overwrites x-llm-d-inference-objective
  - maas-fairness-poc/maas-vllm-cpu-kserve-route: routes to an InferencePool but no AuthPolicy on this route or its parent Gateway overwrites x-llm-d-inference-objective
  - maas-fairness-poc/maas-vllm-gpu-kserve-route: routes to an InferencePool but no AuthPolicy on this route or its parent Gateway overwrites x-llm-d-inference-objective
```

Applying the one-key patch above with
`oc patch authpolicy maas-poc-gateway-authn -n maas-fairness-poc --type=merge
--patch-file=deploy/maas/09-objective-header-stripping.patch.yaml` (done live
on 2026-10-19, once `patch`/`update` on `authpolicies.kuadrant.io` in
`maas-fairness-poc` was granted — see "Applied and verified live" below) and
re-running against a fresh snapshot of the real cluster flips all three to
covered:

```
$ oc get httproute,gateway,authpolicy -n maas-fairness-poc -o yaml > live-snapshot-after.yaml
$ oc get httproute,gateway,authpolicy -n openshift-ingress -o yaml >> live-snapshot-after.yaml
$ bin/gateway-header-check live-snapshot-after.yaml
gateway-header-check: OK -- every InferencePool-backed HTTPRoute overwrites x-llm-d-inference-objective
```

This is a genuine live re-verification, not a local simulation — `maas-poc-gateway-authn`'s
`resourceVersion` was confirmed unchanged (no odh-model-controller reconcile reverted it) ten
seconds after the patch, and `status.conditions` still reads `Accepted=True`, `Enforced=True`.

### Keeping this from silently regressing

Because `maas-poc-gateway-authn` is controller-owned (see the patch file's
"Risk" section), the guarantee is not "patched once" but "still patched" —
run the live-snapshot command above:

- before trusting any fairness measurement run in `docs/poc-results.md`
  (add it next to the existing standing checks in `docs/runbook.md`,
  "Standing checks before trusting any result"),
- after any change to `deploy/llmisvc.yaml`, an RHOAI upgrade, or anything
  else that could cause KServe/odh-model-controller to regenerate the policy,
- and whenever a new route is added anywhere in front of an `InferencePool`
  on this cluster, which is the scenario the ticket is actually about.

## UNI-210: the patch regressed live, undetected, for an unknown window

On 2026-11-09, while running UNI-166's alert drill, `oc get authpolicy
maas-poc-gateway-authn -n maas-fairness-poc -o yaml | grep -i objective`
showed only the deprecated `x-gateway-inference-objective` alias overwritten
— the exact pre-UNI-33 shape. A forged-header `curl` against the real GPU
route (`app1-production` key, `x-llm-d-inference-objective:
exploit-high-priority`) returned `HTTP 200`, identical to baseline: the
mechanism this document closed on 2026-10-19 was gone.

**What actually reverted it was not pinned down**, and this is itself the
finding. OpenShift's event retention on this cluster only reaches back about
an hour (`oc get events -n maas-fairness-poc` on 2026-11-09 returned nothing
earlier than the same day), and `maas-poc-gateway-authn`'s
`managedFields` carried no field-manager history to read. Its `Enforced`
condition's `lastTransitionTime` read `2026-11-04T23:39:42Z` — five days
before discovery — but a condition timestamp updating is not proof the
*content* changed then; it is circumstantial at best, not cited as the
cause.

What is provable: between UNI-33 closing (2026-10-19) and this discovery
(2026-11-09), roughly thirty scenario runs of
[`deploy/poc/15-fairness-benchmark.sh`](../deploy/poc/15-fairness-benchmark.sh)
(UNI-139 through UNI-168) and at least one run of
[`deploy/poc/20-n-group-smoke.sh`](../deploy/poc/20-n-group-smoke.sh)
patched `spec.replicas` / `spec.router.scheduler.config.ref` on
`maas-vllm-gpu` or `maas-vllm-cpu` — chaos-scale, `ENFORCE_LIVE`,
`LIVE_SET_*`, `twenty-group-scale`, and the smoke test's config-ref swap all
do this. Each of those is exactly the kind of `LLMInferenceService`
reconcile the patch file's own "RISK" section named as the thing that could
regenerate `maas-poc-gateway-authn` from its template. Any one of those
thirty-odd runs could have been the one that reverted it — **and none of
them would have noticed**, because the "standing check" this document and
`docs/runbook.md` prescribed was a command a human was supposed to remember
to run before trusting a result, not something either script actually ran.
`grep -rln gateway-header-check deploy/poc/*.sh` returned nothing before this
incident: the conformance tool UNI-33 built was never wired into anything
that runs automatically. That gap — not the specific revert — is what
[[process_restore_does_not_fix_the_automation]] means by fixing the
automation, not just the object.

**Restored and reverified live, 2026-11-09**, by re-running the exact
command in `deploy/maas/09-objective-header-stripping.patch.yaml`:
`x-llm-d-inference-objective` is back in `maas-poc-gateway-authn`'s
`spec.rules.response.success.headers` (confirmed by direct manifest
inspection — the Go toolchain was not available in this session to rebuild
`bin/gateway-header-check`, so the check was done by hand against the same
criteria `conformance/gatewayheaders.Check` applies: both
`maas-vllm-cpu-kserve-route` and `maas-vllm-gpu-kserve-route` parent
`Gateway/maas-poc-gateway`, route to an `InferencePool` backend, and
`maas-poc-gateway-authn` — targeting that Gateway — now overwrites the
header). The before/after forged-header `curl` against the GPU route still
returns `HTTP 200` either way, for the same reason UNI-33's original proof
did: zero `InferenceObjective` resources exist on this cluster, so there is
still no behavioral queue-jump to show either way — the fix is proven at the
manifest/mechanism level, not behaviorally, exactly as it was in October.

**Made harder to silently recur**: both `15-fairness-benchmark.sh` and
`20-n-group-smoke.sh` now check `maas-poc-gateway-authn` for the header
override before doing anything else, and re-apply
`09-objective-header-stripping.patch.yaml` automatically if it is missing,
aborting the run (not just warning) if the re-apply does not hold. This
turns "standing check" from a sentence a human has to remember into a gate
every run that can trigger the underlying revert actually passes through.
It does not stop `odh-model-controller` from reverting the patch — that is
still outside this repo's control — it stops a reverted patch from being
invisible to the next hour-long measurement run the way it was for three
weeks here. The manual live-snapshot command above is still worth running
before trusting `docs/poc-results.md` numbers from any run *not* launched
through one of those two scripts.

## What this does not cover

- **`deploy/poc/02-epp.yaml` / `deploy/poc/03-gateway.yaml`, the pre-MaaS
  direct rig.** It has no Authorino/Kuadrant layer at all — nothing
  authenticates the caller, so there is no trusted identity to overwrite the
  header *with*. The conformance check correctly flags
  `maas-poc-route` as uncovered today. This rig is explicitly described in
  its own header comment as superseded by the production shape
  (`deploy/llmisvc.yaml`) and is still in active use for isolated
  fairness-algorithm testing (per the ticket's instruction to coordinate with
  A2-A4 before touching gateway config mid-measurement-run), so it was left
  unchanged rather than bolting on authentication machinery as a side effect
  of this ticket. The candidate control named here originally — a
  `RequestHeaderModifier` `remove` filter on the `HTTPRoute` — was filed as a
  backlog idea rather than built, since whether that filter runs before or
  after the inference extension's `ext_proc` filter in this cluster's filter
  chain was not verified. **UNI-43 verified it: it runs after, so that
  candidate does not work.** See the next section for the evidence and the
  corrected fix.
- **The priority-band bypass is still dormant on this cluster.** As recorded
  in `docs/poc-results.md`, there are zero `InferenceObjective` resources, so
  every objective name — forged or not — resolves to the default priority.
  Demonstrating an actual *behavioural* difference (a forged objective
  jumping a real priority queue) would need a non-default `InferenceObjective`
  created for the test, which needs `create` on a cluster-scoped
  `inferenceobjectives.llm-d.ai` resource — not available to this run (see
  "Blocked" below). What was verified instead is the mechanism: the header
  alias precedence in the vendored dependency, and that nothing in the
  request path currently inspects or strips the header (both proven above).

## UNI-43: the `RequestHeaderModifier` candidate does not protect the EPP's read

The direct rig (`deploy/poc/02-epp.yaml` / `03-gateway.yaml`) has no trusted
identity to overwrite the header with, so the UNI-33 mechanism (Authorino
overwriting a response header via `ext_authz`) doesn't apply here. The only
option is to remove the header outright, and the candidate named when this gap
was first recorded was a Gateway API `RequestHeaderModifier` `remove` filter on
the `HTTPRoute`. This does not work, and applying it would have been worse than
doing nothing: it would make the conformance posture *look* fixed while leaving
the actual exploit (a client picking its own priority band) intact.

### Why: Envoy applies route-level header removal in the Router filter, which runs last

A Gateway API `RequestHeaderModifier` compiles, on Istio, to Envoy's native
route-level `request_headers_to_add` / `request_headers_to_remove` fields —
confirmed directly in Istio's route builder
(`pilot/pkg/networking/core/route/route.go`, `TranslateHeadersOperations` /
`TranslateRoute`), which is a *different* mechanism from a registered HTTP
filter with a position in the chain. Envoy's own `header_mutation` filter docs
(`envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/header_mutation_filter`)
recommend it over the route-level fields specifically because it "provides
complete control over the position and ordering of mutations" — implying the
route-level fields do not.

Confirmed in Envoy's source (`source/common/router/router.cc`,
`Router::Filter::decodeHeaders`): the route-level header mutations are applied
by `route_entry_->finalizeRequestHeaders(...)`, called from inside the
**Router** filter, immediately before host selection and dispatch to the
upstream connection pool. The Router filter is always the last filter in the
HTTP decoder chain — it is the filter that forwards the request upstream, by
definition nothing else in the chain runs after it. So route-level
`request_headers_to_remove` only ever changes what the *upstream backend*
receives; every decoder filter positioned earlier in the chain already saw —
and, for `ext_proc`, already acted on — the original, un-stripped headers.

The inference extension's `ext_proc` filter is exactly such an earlier filter.
Istio registers it under Envoy's well-known name
`envoy.filters.http.ext_proc` (`pilot/pkg/xds/filters/filters.go`,
`InferencePoolExtProc`, via `wellknown.HTTPExternalProcessing`) as an ordinary
HTTP filter in the chain — it is not, and cannot be, positioned after Router.
And Istio explicitly turns on request-header processing for InferencePool
routes: `buildExtProcPerRoute` (`route.go`) sets
`ProcessingMode.RequestHeaderMode: SEND`, so the EPP receives the full,
original request headers via `ext_proc` before Router ever gets a chance to
apply the route's removal rule.

Putting those two facts together: a `RequestHeaderModifier` `remove` filter on
`maas-poc-route` would strip `x-llm-d-inference-objective` from the copy of the
request Envoy forwards to the simulator backend, but the EPP's `ext_proc` call
— which is what actually resolves the priority band — happens earlier in the
same request's processing and would still see the client's forged value
unchanged. This is precisely the risk flagged when this candidate was first
written down: the filter runs *after* `ext_proc`, not before.

This evidence was originally source-level only (Istio's and Envoy's own code
and docs); it has since been confirmed by a live trace. With `pods/exec`
granted (UNI-52), `oc exec ... -c istio-proxy -- pilot-agent request GET
config_dump` against the gateway pod's own loopback admin interface showed
`envoy.filters.http.ext_proc` at a fixed position in listener `0.0.0.0_80`'s
HTTP filter chain, ahead of `envoy.filters.http.router` — see
`deploy/poc/11-objective-header-removal.yaml`'s "VERIFIED LIVE" section for the
full chain order. The EPP's own request-header
processing offers no alternative seam either: as already established above,
`director.go:177`'s `getInferenceObjective` resolves the header before any
configured plugin runs, for every request regardless of authentication, so
there is nothing inside the EPP's own plugin chain to intervene on. The fix has
to be upstream of `ext_proc`, in Envoy's filter chain.

### The corrected fix

[`deploy/poc/11-objective-header-removal.yaml`](../deploy/poc/11-objective-header-removal.yaml)
installs Envoy's `envoy.filters.http.header_mutation` filter via an Istio
`EnvoyFilter`, `INSERT_BEFORE` `envoy.filters.http.ext_proc`, with the removal
itself scoped to `maas-poc-route` alone via a per-route override — not a
chain-wide removal, because `maas-poc-gateway` is shared with the two
authenticated MaaS routes, and the same filter instance would otherwise also
strip the header Authorino just set for them, undoing UNI-33. The route-name
assumption this patch depends on was checked against a live config dump before
applying — and was wrong (Istio names the generated route
`maas-fairness-poc.maas-poc-route.0`, not after the HTTPRoute rule's `name`
field as originally guessed) and corrected. See that file for the full
reasoning, the exact `EnvoyFilter`, and the live verification evidence.

## Applied and verified live

On 2026-10-19, `patch`/`update` on `authpolicies.kuadrant.io` in
`maas-fairness-poc` was granted to the `poc-agent` ServiceAccount (tracked as
UNI-52). Verified before touching anything, with a `SelfSubjectAccessReview`
(not just `auth can-i`, for an auditable record):

```
$ oc auth can-i patch authpolicies.kuadrant.io -n maas-fairness-poc
yes
```

```json
{"apiVersion":"authorization.k8s.io/v1","kind":"SelfSubjectAccessReview",
 "spec":{"resourceAttributes":{"namespace":"maas-fairness-poc","verb":"patch",
 "group":"kuadrant.io","resource":"authpolicies"}}}
```
→ `status.allowed: true`, `reason: RBAC: allowed by RoleBinding
"poc-agent-edit/maas-fairness-poc" of ClusterRole "edit" to ServiceAccount
"poc-agent/paperclip"`.

Checked for an in-flight measurement run first (per the ticket's
coordinate-with-A2-A4 instruction): `oc get jobs -n maas-fairness-poc` showed
both `maas-latecomer` and `maas-loadgen` `Complete`, the latter having
finished ~15 minutes earlier — no run in progress.

Applied the patch with the exact command recorded in
`deploy/maas/09-objective-header-stripping.patch.yaml`, confirmed
`x-llm-d-inference-objective` now present in
`spec.rules.response.success.headers` alongside the old alias, and re-ran the
live conformance check — see the passing output above. Before/after `curl`
requests against `maas-gateway-maas-fairness-poc.apps.ocp.paladinaura.com`
both still return `HTTP 200` for baseline and forged-header requests alike,
with or without the patch: that is expected, not a gap in the fix, because
there are zero `InferenceObjective` resources on this cluster today (see
"What this does not cover" below) — nothing currently assigns different
priority bands for a forged value to jump, so there is no client-observable
status-code or latency difference to show either way. The fix is proven at
the level the ticket asks for: the gateway's AuthPolicy, not the client, now
authors the value the EPP reads, and the conformance check holds the cluster
to that mechanically.

`create` on the cluster-scoped `inferenceobjectives.llm-d.ai` resource
remains ungranted and would additionally let the priority-band bypass be
demonstrated *behaviourally* (an actual queue-jump) rather than
structurally — a nice-to-have beyond the ticket's literal "Done when"
wording, not attempted here.

Everything in this document — the mechanism, the before-state live proof,
the fix, its live application, and the conformance check's
failing/passing/now-passing-live demonstrations — is complete.

UNI-43 (the direct rig fix above) was blocked on a separate grant —
`create`/`update` for `envoyfilters.networking.istio.io` in the same namespace
plus `pods/exec` for the gateway's Envoy admin interface — which UNI-52 also
added. Both were verified with `oc auth can-i` before use, the EnvoyFilter was
applied, and the live config dump confirmed both the filter-chain position and
the per-route scoping match what the manifest specifies — see
`deploy/poc/11-objective-header-removal.yaml`'s "HOW THIS WAS VERIFIED LIVE"
section. Not verified: an end-to-end request showing the forged header fails
to reach the EPP or simulator, since both remain scaled to 0/0 on this
cluster and scaling either up was out of scope for this ticket.
