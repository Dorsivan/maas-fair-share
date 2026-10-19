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
go test ./conformance/...     # the check's own unit tests, offline
```

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
  | go run ./cmd/gateway-header-check -
```

### Demonstrated failing, as the ticket requires

Against a deliberately non-stripping route
(`conformance/gatewayheaders/testdata/bad/old-header-only.yaml` — the
pre-fix shape of `maas-poc-gateway-authn`, overwriting only the deprecated
alias):

```
$ go run ./cmd/gateway-header-check conformance/gatewayheaders/testdata/bad/old-header-only.yaml
gateway-header-check: FAIL -- 1 route(s) do not overwrite x-llm-d-inference-objective:
  - bad-ns/half-fixed-route: routes to an InferencePool but no AuthPolicy on this route or its parent Gateway overwrites x-llm-d-inference-objective
exit status 1
```

Against the real, unpatched cluster, captured 2026-10-19 (`oc get
httproute,gateway,authpolicy -n maas-fairness-poc -o yaml` then the same
again for `-n openshift-ingress`, concatenated with a `---` separator):

```
$ go run ./cmd/gateway-header-check live-snapshot.yaml
gateway-header-check: FAIL -- 3 route(s) do not overwrite x-llm-d-inference-objective:
  - maas-fairness-poc/maas-poc-route: routes to an InferencePool but no AuthPolicy on this route or its parent Gateway overwrites x-llm-d-inference-objective
  - maas-fairness-poc/maas-vllm-cpu-kserve-route: routes to an InferencePool but no AuthPolicy on this route or its parent Gateway overwrites x-llm-d-inference-objective
  - maas-fairness-poc/maas-vllm-gpu-kserve-route: routes to an InferencePool but no AuthPolicy on this route or its parent Gateway overwrites x-llm-d-inference-objective
```

Applying the one-key patch above (`sed`-replicated locally into a copy of the
same snapshot, since this run had no write access to the cluster — see
"Blocked" below) and re-running flips all three to covered:

```
$ go run ./cmd/gateway-header-check live-snapshot-after-fix.yaml
gateway-header-check: OK -- every InferencePool-backed HTTPRoute overwrites x-llm-d-inference-objective
```

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

This evidence is source-level (Istio's and Envoy's own code and docs), not a
live trace — this run had no admin/exec access to the gateway pod's Envoy
instance to confirm the compiled filter chain directly (see
`deploy/poc/11-objective-header-removal.yaml`'s "NOT VERIFIED" section for the
exact commands that would close that gap). The EPP's own request-header
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
strip the header Authorino just set for them, undoing UNI-33. See that file for
the full reasoning, the exact `EnvoyFilter`, and what remains unverified
(mainly: the exact route name Istio generates for `maas-poc-route`'s one rule,
which was not read from a live config dump).

## Blocked: applying the patch and re-verifying live

This run's ServiceAccount (`system:serviceaccount:paperclip:poc-agent`) has
**read-only** access to the `maas-fairness-poc` namespace — it did not create
it, and per the project's access model only the namespace's creator gets
write access. Confirmed directly:

```
$ oc auth can-i patch authpolicies.kuadrant.io -n maas-fairness-poc
no
$ oc auth can-i create inferenceobjectives.llm-d.ai -n maas-fairness-poc
no
```

**Exact unblock needed:** `patch` (or `update`) on
`authpolicies.kuadrant.io` in namespace `maas-fairness-poc`, to apply
`deploy/maas/09-objective-header-stripping.patch.yaml` to the live
`maas-poc-gateway-authn` object and re-run the live conformance check for a
genuine (not locally-simulated) after-fix result. `create` on the
cluster-scoped `inferenceobjectives.llm-d.ai` resource would additionally let
the priority-band bypass itself be demonstrated behaviourally, though that is
a nice-to-have beyond the ticket's literal "Done when" wording.

Everything else in this document — the mechanism, the before-state live
proof, the fix, and the conformance check with its failing/passing
demonstrations — does not depend on that grant and is complete.

UNI-43 (the direct rig fix above) is blocked separately, on `create`/`update`
for `envoyfilters.networking.istio.io` in the same namespace plus read access
to the gateway pod's Envoy admin interface — see
`deploy/poc/11-objective-header-removal.yaml`'s "Blocked" section. The two
unblocks are independent; granting one does not cover the other.
