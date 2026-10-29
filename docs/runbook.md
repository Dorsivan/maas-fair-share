# Runbook

Procedures that were worked out the hard way and are not obvious from the
manifests. Each one cost real time to discover.

---

## Bring the GPU nodes back up

They are stopped between test sessions to save cost. Three steps, and
**skipping step 2 makes a healthy node look like broken hardware**.

```sh
ibmcloud is instance-start ocp-gpu-worker-0
ibmcloud is instance-start ocp-gpu-worker-1
```

**2. Approve CSRs — TWO rounds.** UPI clusters do not auto-approve the
kubelet-serving CSR, so a node whose certs rotated while it was stopped sits
`NotReady` forever. The client cert comes first; kubelet-serving follows about
45 seconds later.

```sh
# run twice, ~45s apart
oc get csr --no-headers | awk '$NF=="Pending"{print $1}' | xargs -r oc adm certificate approve
oc get node ocp-gpu-worker-0        # expect Ready within ~3 min
```

**3. Check the GPU is actually exposed.**

```sh
oc get node ocp-gpu-worker-0 -o jsonpath='{.status.allocatable.nvidia\.com/gpu}{"\n"}'
```

Empty means NFD mislabelled it. This cluster's NodeFeatureDiscovery uses
`deviceLabelFields: [vendor, device]`, emitting
`feature.node.kubernetes.io/pci-10de_20b5.present`, while the NVIDIA GPU
operator selects on the **vendor-only** `pci-10de.present`. Workaround:

```sh
oc label node ocp-gpu-worker-0 feature.node.kubernetes.io/pci-10de.present=true --overwrite
```

Driver, device plugin and capacity appear ~6 minutes later. The durable fix is
`deviceLabelFields: [vendor]` on the NodeFeatureDiscovery CR — see the
outstanding-work table.

Then `oc apply -f deploy/poc/09-vllm-gpu.yaml` and allow ~8 minutes for the
model download and vLLM startup.

---

## Mint a MaaS API key

Inference endpoints accept **only** keys with the `sk-oai-` prefix. Kubernetes
tokens authenticate but are authorised solely for `/v1/models`, so they cannot
run inference.

The documented path is `POST /maas-api/v1/api-keys` through the gateway. **That
returns 500 on this cluster**: `maas-api-route` targets `Service/maas-api` on
port 8443, which serves TLS from an OpenShift service-serving cert, and there
is no `BackendTLSPolicy` — the CRD is not installed — so Envoy speaks plaintext
to a TLS port.

Workaround: talk to maas-api directly and supply the two headers Authorino
would normally inject.

```sh
oc port-forward -n redhat-ods-applications svc/maas-api 18443:8443 &

curl -sSk -X POST https://localhost:18443/v1/api-keys \
  -H "Authorization: Bearer $(oc whoami -t)" \
  -H "Content-Type: application/json" \
  -H 'X-MaaS-Username: dorsi' \
  -H 'X-MaaS-Group: ["maas-app1"]' \
  -d '{"name":"key-app1","subscription":"app1-production","expiresIn":"7d"}'
```

Three traps, each of which returns the same opaque
`AUTH_FAILURE / Exception thrown while generating token`:

- **`X-MaaS-Username` is required.** Without it: *"Missing or empty username header"*.
- **The header is `X-MaaS-Group`, singular.** `X-MaaS-Groups` is ignored.
- **Its value must be a JSON array**, not a bare string. A bare string gives
  *"failed to parse header as JSON array"*.

The real error is only ever visible in the maas-api log, never in the response:

```sh
oc logs -n redhat-ods-applications deploy/maas-api --tail=40 | grep -v '"/health"'
```

---

## Rebuild and publish the EPP image

Plugins are compiled in, so changing the plugin means rebuilding the image.

```sh
SHA=$(git rev-parse --short HEAD)
podman build -f Dockerfile.epp \
  --build-arg COMMIT_SHA="$(git rev-parse HEAD)" --build-arg BUILD_REF="$SHA" \
  -t quay.io/rh-ee-dsivan/maas-fair-share:latest \
  -t "quay.io/rh-ee-dsivan/maas-fair-share:$SHA" .

podman login quay.io
podman push quay.io/rh-ee-dsivan/maas-fair-share:latest
podman push "quay.io/rh-ee-dsivan/maas-fair-share:$SHA"
```

The repo is **private**, so the cluster needs a pull secret linked to the
LLMInferenceService's service account:

```sh
# extract ONLY the quay.io entry from the local podman auth
python3 -c "import json;d=json.load(open('$XDG_RUNTIME_DIR/containers/auth.json'));\
json.dump({'auths':{k:v for k,v in d['auths'].items() if 'quay.io' in k}},open('/tmp/q.json','w'))"

oc create secret generic quay-maas-pull -n maas-fairness-poc \
  --from-file=.dockerconfigjson=/tmp/q.json --type=kubernetes.io/dockerconfigjson
oc secrets link maas-vllm-gpu-epp-sa quay-maas-pull --for=pull -n maas-fairness-poc
shred -u /tmp/q.json
```

Quay rather than the in-cluster registry is deliberate: **the GPU nodes cannot
reach the internal registry's ClusterIP** (`dial tcp 172.30.x:5000: i/o
timeout`) even though pod-to-pod networking works, so an internal reference
leaves the EPP in `ImagePullBackOff` there. A Quay reference is also the only
one meaningful on a different cluster.

### Publishing to Quay without a local podman (used for UNI-29)

The steps above assume a workstation with `podman` and a container-capable kernel. An
agent session on this cluster may have neither. An OpenShift `BuildConfig` can do the
same push: it runs the Docker-strategy build server-side and can emit straight to an
external registry with `output.to.kind: DockerImage` plus a `pushSecret`, so no local
build tool is needed at all.

```sh
# one-time: a push credential for the robot account, in the namespace holding the build
oc create secret docker-registry quay-maas-push -n maas-fairness-poc \
  --docker-server=quay.io --docker-username="$QUAY_USERNAME" --docker-password="$QUAY_TOKEN"

SHA=$(git rev-parse --short HEAD)
cat <<YAML | oc apply -n maas-fairness-poc -f -
apiVersion: build.openshift.io/v1
kind: BuildConfig
metadata:
  name: maas-epp-quay-publish
spec:
  runPolicy: Serial
  source:
    binary: {}
    type: Binary
  strategy:
    type: Docker
    dockerStrategy:
      dockerfilePath: Dockerfile.epp
      buildArgs:
        - {name: COMMIT_SHA, value: "$(git rev-parse HEAD)"}
        - {name: BUILD_REF, value: "$SHA"}
  output:
    to: {kind: DockerImage, name: "quay.io/rh-ee-dsivan/maas-fair-share:$SHA"}
    pushSecret: {name: quay-maas-push}
YAML

oc start-build maas-epp-quay-publish --from-dir=. -n maas-fairness-poc   # no --follow; poll instead
# poll oc get build <name> -n maas-fairness-poc -o jsonpath='{.status.phase}' until Complete
oc get build <name> -n maas-fairness-poc -o jsonpath='{.status.output.imageDigest}{"\n"}'
```

The pushed digest still needs the same `quay-maas-pull` secret on the consuming
service account as above — this only replaces the build/push step, not the pull side.
`maas-vllm-gpu-epp-sa` already carries it, so an image pushed this way to the same
repository needs no further pull-secret work.

Digest produced from `fc27130` and now referenced by `deploy/llmisvc.yaml` and
`deploy/poc/09-vllm-gpu.yaml` (UNI-29, 2026-10-22):

```
quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135
```

This closes the drift described in the next section: `main`, checked out clean, now
deploys an image built from its own `HEAD`, published somewhere a different cluster
could also reach it from (subject to the private-repo pull-secret note above).

### Interim in-cluster build used to verify UNI-53 — superseded by UNI-29's Quay publish

The role that verified UNI-53 does not hold the quay.io push credential above, so the
image used for that verification was **not** built or published through the steps
above. It came from an in-cluster `BuildConfig` named `maas-epp` that already exists in
`maas-fairness-poc` (binary source, `dockerfilePath: Dockerfile.epp`, output to
`ImageStreamTag maas-epp:latest` — the same mechanism that produced the
`maas-epp:latest` images `deploy/poc/02-epp.yaml`, `05-llmisvc-sim.yaml`,
`06-rhoai34-shape.yaml` and `07-vllm-cpu.yaml` already reference). It predates this
ticket and is not itself checked into this repository — that gap is worth closing, but
doing so was not part of UNI-53.

```sh
oc start-build maas-epp --from-dir=. --follow -n maas-fairness-poc
oc get imagestreamtag maas-epp:latest -n maas-fairness-poc \
  -o jsonpath='{.image.dockerImageReference}{"\n"}'
```

Digest produced from `d7e4d58` and used for UNI-53's live verification (2026-10-19):

```
image-registry.openshift-image-registry.svc:5000/maas-fairness-poc/maas-epp@sha256:7849fa523ce98e1b01de6864650df86dac123d51264d4fd73e62dbfe27834e2e
```

**`deploy/poc/09-vllm-gpu.yaml` and `deploy/llmisvc.yaml` did not reference this image,
and applying them from `main` at the time did not deploy UNI-53.** They were pinned to
`quay.io/rh-ee-dsivan/maas-fair-share:aef33a5`, which fell further behind with every
commit that touched the EPP (14 commits as of UNI-53, 31 by the time UNI-29 caught it).

That gap is now closed, but not by publishing *this* digest — see "Publishing to Quay
without a local podman" above. UNI-29 rebuilt from a later `HEAD` (`fc27130`, after
UNI-75's EPP rebuild) and pushed *that* to Quay instead, since a current build is more
useful to pin than this now-stale one. Both manifests reference the UNI-29 digest as of
2026-10-22. If the EPP changes again, re-run that procedure and bump both manifests in
the same commit — do not let the pin drift a third time.

Do **not** "fix" a future drift like this by repointing those two manifests at an
in-cluster-registry digest like the one above instead:
that image is reachable only from inside this cluster, and this registry is known to
time out from some nodes in this pool — the CPU-path EPP deployment
(`maas-vllm-cpu-kserve-router-scheduler-*`, same internal registry, different tag) is
sitting in `ImagePullBackOff` against exactly this failure mode as of this writing. The
digest above exists only to prove the plugin logic end to end from inside the cluster;
it is not a transferable or deployable artifact, and does not leave this cluster.

---

## A load run returned nothing / looks broken

In order of how often it was the cause:

**1. The gateway is `Running` but not `1/1`.** Its istio-proxy can lose its
xDS connection to istiod and never recover — readiness fails, the pod still
reports `Running`, and it serves nothing. Symptom in the pod log:
`keepalive ping failed to receive ACK` and
`DeltaAggregatedResources gRPC config stream to xds-grpc closed: 13`.

```sh
oc get pods -n maas-fairness-poc | grep gateway        # must be 1/1
oc delete pod -n maas-fairness-poc <gateway-pod>       # restart re-establishes xDS
```

**2. The load is under-offered.** Each tenant must offer **more** than its
entitlement or you measure the generator, not the policy. See the sizing note
in `deploy/poc/04-loadgen.yaml`. Symptom: the split collapses toward equal
shares whatever the weights say.

**3. The EPP is not actually in the path.** The pool is `failureMode: FailOpen`,
so an EPP in `ImagePullBackOff` means Envoy silently bypasses fairness and
every request succeeds while measuring nothing.

```sh
oc get pods -n maas-fairness-poc | grep router-scheduler   # must be 1/1
```

**4. HTTP errors are invisible to curl.** `curl -sS` treats 400/500 as a
successful transfer. The generator tallies status codes for this reason — a
run is only meaningful if they are overwhelmingly 200.

---

## Run the fairness benchmark (UNI-54)

Before this, "delivered share" was a number a human produced by reading two
Prometheus scrapes and doing the division by hand — see the 1.57:1-against-2:1
detour in `docs/poc-results.md`. `deploy/poc/15-fairness-benchmark.sh` makes a
named scenario, run against the live GPU EPP, produce that number itself.

```sh
OPENSHIFT_TOKEN=... ./deploy/poc/15-fairness-benchmark.sh <scenario> [label]
```

### Scenarios

These are the four work-conservation experiments already described in the
comments of `deploy/poc/04-loadgen.yaml` — read those comments before
touching worker counts, the sizing reasoning there is load-bearing.

| scenario | what it sets | what it proves |
|---|---|---|
| `full-contention` | `TENANTS="app1 app2 end-users"`, equal `WORKERS` | the headline weight split: 20/10/65 delivered under genuine three-way contention |
| `end-users-idle` | `TENANTS="app1 app2"` | end-users' 65% is **absorbed** by app1/app2, not reserved while idle |
| `app1-alone` | `TENANTS="app1"` | a single tenant receives ~100% of the pool, not capped near its 20% weight |
| `asymmetric-demand` | `WORKERS_APP1=32 WORKERS_APP2=0 WORKERS_END_USERS=2` | app1 is not held near its weight when the highest-weight tenant (end-users) sends only a trickle — this is the YAML's own commented-out example, which also idles app2; the ticket's prose names only APP1/END_USERS but the YAML it points to is the source of truth |

### What it produces

Everything lands in `results/<timestamp>-<label>/`, the same per-run artifact
directory `14-loadgen-with-log-archive.sh` (UNI-46) writes the EPP container
log into:

- `fairness-report.json`, `fairness-report.md` — one row per group: configured
  weight, offered workers, delivered requests/status tally/p50/p95 (from the
  generator), delivered tokens and observed share (from the EPP's own
  `llm_d_epp_maas_fairness_contended_service_tokens_total`, scraped directly
  off its `/metrics` immediately before and after the run — **not** a Thanos
  query over a range, so there is no scrape-alignment or duplicate-replica
  concern to correct for), deviation in points, and run metadata (scenario,
  `enforce`, duration, EPP image **digest**, backend, start/end timestamps).
- `metrics-before.txt` / `metrics-after.txt` — the raw snapshots the report
  was computed from, so a reviewer can redo the arithmetic by hand.
- `epp-container.log`, `loadgen.log`, `04-loadgen.patched.yaml` — same as
  UNI-46, for the same reason (archived evidence, not a log-retention bet).

The script's own exit code is the report's verdict: 0 on PASS, 1 on FAIL —
wire it into anything that should break a pipeline on a regression.

### Expected share, and why it is not just "the configured weight"

The report's "expected %" divides each **offered** group's weight by the sum
of weight over offered groups only — not by the sum of every configured
weight (which includes the never-offered `unclassified` catch-all, weight 5).
For `end-users-idle`, that means app1/app2's target is 66.7%/33.3% (their 2:1
ratio over the whole pool), not 20%/10% with the remaining 65% unaccounted
for. Scoring against the full-weight denominator would flag a policy that is
correctly absorbing idle capacity as a large deviation, which is backwards.
This differs by a few points from the "20/10/65" shorthand used loosely
elsewhere in this repo's prose for the full-contention case — those are the
raw ConfigMap numbers, not divided by anything (they happen to sum to 95, not
100, because `unclassified` is excluded).

"Delivered tokens" and "observed share" are both the same SLI
`deploy/grafana-dashboard.yaml`'s headline panel already uses (UNI-50) — this
benchmark does not invent a second definition of delivered share.

### Two scenarios get a different verdict rule, not the symmetric threshold

`app1-alone` and `asymmetric-demand` found a real gap in the first version of
this logic, live against the GPU EPP on 2026-10-29 — see the "UNI-54" section
of `docs/poc-results.md` for the full before/after numbers:

- **`app1-alone`** has nobody for the single offered group to be *contended*
  against, and `contended_service_tokens_total` (`pkg/fairness/weightedlas/metrics.go`)
  is specifically defined to accrue only under contention. A solo run
  therefore scrapes a correct, flat-zero delta — not starvation. The report
  does not compute a share or deviation for a solo group at all; instead it
  checks the thing this scenario actually names ("must receive ~100% of the
  pool") as a request-success-rate bar: 90%+ HTTP 200, the same
  "overwhelmingly 200" bar this runbook's standing checks already use.
- **`asymmetric-demand`** deliberately demand-caps `end-users` to 2 workers
  (the YAML's own commented-out example), so it cannot reach a
  weight-proportional share no matter how well the policy behaves — scoring
  that as a symmetric deviation would fail the scenario's own success case
  (app1 correctly taking far more than its nominal weight while end-users'
  unused share goes to it, not reserved). This scenario instead gets a
  one-sided check: FAIL only if the saturating, highest-worker-count offered
  group is held *at or below* its own nominal weight share — i.e. only if
  weight acted as a ceiling, which is the actual defect this scenario exists
  to catch.

`full-contention` and `end-users-idle` are not special-cased — every group
they offer is genuinely able to compete for the pool, so the symmetric
`|observed % − expected %| ≤ threshold` check applies to both as described
above.

### The PASS/FAIL threshold: 10 points, on evidence

`THRESHOLD_POINTS` (default 10) is the maximum allowed `|observed % -
expected %|` for any offered group. Chosen from this repo's own real-GPU
results in `docs/poc-results.md`:

- A correctly-sized run landed within **~1 point** of target.
- A run sized close but not iteratively tuned still called "directionally and
  substantially correct" reached **~5 points**.
- The under-offered equal-worker artifact (work conservation draining a
  high-weight tenant's queue, not enforcement failing) produced **~20–28
  points** of compression toward equal thirds.
- The open-loop newcomer-clamp finding that **inverted** the weight ordering
  reached **~40 points**.

10 points sits above realistic sizing noise and below anything that is
actually broken, misconfigured, or inverted. It is a starting point, not a
law — if a future well-tuned run on different hardware lands outside it for a
reason that is not a regression, revise the number here and say why, rather
than silently loosening it in the script.

### Testing the FAIL path without a cluster

`deploy/poc/15-fairness-report.py` (the report/verdict logic) takes no
cluster access — it is a pure function of two metrics snapshots and a loadgen
log. `deploy/poc/15-fairness-report-test.py` exercises it against synthetic
data, including a deliberately skewed input that must FAIL with a non-zero
exit, and an EPP-mid-run-restart case that must also FAIL rather than
silently clamp the negative delta to zero and pass:

```sh
python3 -I deploy/poc/15-fairness-report-test.py
```

---

## Load the fairness dashboard into the live Grafana

`deploy/grafana-dashboard.yaml` ships the dashboard JSON as a ConfigMap
(`maas-fairness-dashboard`, namespace `maas-fairness-poc`) because that is the
only namespace the Engineer role can write to. It does **not** auto-load into
the live Grafana from there — Kubernetes `configMap` volume sources cannot
cross namespaces, and the live Grafana Deployment (`grafana`, namespace
`grafana`) mounts exactly one file-provisioned dashboards ConfigMap, by name:

```sh
oc get deployment grafana -n grafana -o yaml | grep -A3 'name: kueue-dashboard'
#   configMap:
#     defaultMode: 420
#     name: kueue-dashboard     <- must be this literal name
#     optional: true            <- true, so it's silently absent, not an error, when missing
#   name: dashboards
```

mounted at `/var/lib/grafana/dashboards`, which `grafana-dashboards-provider`
(the `dashboards-provider` ConfigMap, type `file`) scans for any `*.json` file
and loads into the "Kueue" folder. So making this dashboard render requires a
**second object, with a different name, in a different namespace**, copied
from the one in this repo. Someone with write access to the `grafana`
namespace needs to run:

```sh
OC="oc --token=$OPENSHIFT_TOKEN --server=https://api.ocp.paladinaura.com:6443"

# 1. Pull the JSON out of the repo's ConfigMap (already applied in maas-fairness-poc).
$OC get configmap maas-fairness-dashboard -n maas-fairness-poc \
  -o jsonpath='{.data.maas-fairness-gpu-epp\.json}' > /tmp/maas-fairness-gpu-epp.json

# 2. Create/update the ConfigMap the grafana Deployment actually mounts.
$OC create configmap kueue-dashboard -n grafana \
  --from-file=maas-fairness-gpu-epp.json=/tmp/maas-fairness-gpu-epp.json \
  --dry-run=client -o yaml | $OC apply -f -

# 3. The volume was optional and absent when the pod last started, so confirm
#    it actually attaches rather than trusting kubelet's periodic resync —
#    restart the pod and recheck the dashboard list in the "Kueue" folder.
$OC delete pod -n grafana -l app=grafana
```

As of 2026-10-25 the Engineer role has `edit` on `maas-fairness-poc` only —
`oc auth can-i create configmaps -n grafana` and
`oc auth can-i update configmaps -n grafana` both return `no`. This is the
same shape of access gap as the `maas-fairness-poc` grant itself, but on a
namespace no agent here has ever been granted. Re-run step 1 and re-apply
step 2 any time `deploy/grafana-dashboard.yaml` changes — there is no
automatic sync between the two ConfigMaps.

---

## Standing checks before trusting any result

```sh
# No tenant silently in a different priority band -- fairness is intra-band only,
# and MaaS sets x-gateway-inference-objective per ServiceAccount.
oc get inferenceobjectives.llm-d.ai -A            # expect none, or all priority 0

# A client can still forge the band wholesale: x-llm-d-inference-objective
# beats the gateway's own x-gateway-inference-objective unless the gateway
# overwrites it too. See docs/gateway-header-stripping.md.
# Build the checker once, offline -- see "Building this check air-gapped" there:
#   (cd cmd/gateway-header-check && go build -o ../../bin/gateway-header-check .)
oc get httproute,gateway,authpolicy -n maas-fairness-poc -o yaml \
  | bin/gateway-header-check -                     # expect "OK", exit 0

# Every request trued up. Non-zero means requests are charged their ESTIMATE forever.
... | grep maas_fairness_requests_without_usage_total      # expect absent or 0

# Shedding is not doing the allocating.
... | grep flow_control_requests_evicted_total             # expect absent or 0

# Classification is working.
... | grep maas_fairness_unmatched_subscriptions_total     # expect 0
```

And the one that tells you the policy converged, which matters more than the
token percentages: `normalized_service` should be **equal across backlogged
groups**. Persistent spread means it has identified an imbalance it is not
being given the chance to correct — usually under-offered load.

---

## Find a request's story from its response header

Every response from the GPU path carries `x-request-id`, `x-maas-fairness-group`
and `x-maas-fairness-queue-ms` (UNI-53; suppressible via `emitAttributionHeaders`
in `deploy/poc/00-config.yaml`) — **once the EPP image includes `d7e4d58` or later**.
As committed, `deploy/poc/09-vllm-gpu.yaml` and `deploy/llmisvc.yaml` do not yet pull
that image; see "Interim in-cluster build used to verify UNI-53" under "Rebuild and
publish the EPP image" above before assuming a freshly-applied cluster has this.

Given the `x-request-id` value from a response, two commands get that request's own
log lines back:

```sh
POD=$(oc get pods -n maas-fairness-poc \
  -l app.kubernetes.io/name=maas-vllm-gpu,app.kubernetes.io/component=llminferenceservice-router-scheduler \
  -o jsonpath='{.items[0].metadata.name}')

ID=<the x-request-id value from the response>
oc logs -n maas-fairness-poc "$POD" | grep "$ID"
```

Grep the bare id, not `"requestID":"<id>"` — the llm-d-router framework's own
request-lifecycle lines key it as `x-request-id` and appear on every request, while
this plugin's own lines key it as `requestID` and, **in the default configuration**,
only appear on the two exception paths (the unmatched-subscription notice and the
no-usage-block warning). A healthy, matched request today produces zero plugin lines,
only framework ones — the bare-id grep still finds those; the `"requestID":"` form
matches nothing for it. `requestID` also carries `traceId` when the request came in
with a `traceparent` header. See UNI-48's query pack for the field contract those
lines use.

UNI-47's V(4) per-request tier adds a third case — a sampled line on every settled
request, healthy or not — but it ships off by default and needs two separate edits to
turn on; see "Turn on the V(4) per-request tier" below before assuming it is available.

If the pod has since restarted, that log is gone -- this POC cluster has no log
aggregation or retention window (see docs/design.md "Production observability").

---

## Turn on the V(4) per-request tier

This recipe is for the **POC rig** (`deploy/poc/`). Off by default, and both of the
following edits are required — either one alone leaves the tier **silently**
disabled, with no error and no log line saying why. See "On the KServe-managed
scheduler" below before applying any of this to the GPU/production path — step 2
does not transfer as written.

**1. Uncomment the two ConfigMap keys** — `deploy/poc/00-config.yaml` for the POC,
`deploy/epp-config.yaml` for production — under the `maas-weighted-fairness` plugin's
`parameters`:

```yaml
requestTierV4SampleEvery: 100       # emit 1 line per 100 settlements
requestTierV4TimeBoxSeconds: 900    # self-disables 15 minutes after the first check
```

**2. Add `-v=4` to the EPP container's args** in `deploy/poc/02-epp.yaml`, alongside
the existing `--zap-encoder` etc.:

```yaml
args:
  - --pool-name
  - maas-pool
  # ... existing args unchanged ...
  - -v
  - "4"
```

This step is the one that's easy to skip, and skipping it is invisible: the plugin's
own gate (`cfg.RequestTierV4SampleEvery`) only gets you halfway — emission also
requires `log.FromContext(ctx).V(4).Enabled()` to be true, and the EPP's default
verbosity is V(2) (`logging.DEFAULT` in
`llm-d-router@v0.11.0/pkg/common/observability/logging/const.go`). Uncomment only the
ConfigMap keys and the tier stays silent, with nothing in the logs to say why.

**If `--zap-log-level` is ever added to this args list, it silently overrides `-v`,**
and the tier goes dark again — `Complete()` in the same module only derives the zap
level from `-v` when `--zap-log-level` was not explicitly set, and that flag also
accepts a plain integer. Today's manifest does not set `--zap-log-level`, so `-v`
governs; if a later change adds `--zap-log-level`, set it to `4` directly instead of
relying on `-v`.

**On the KServe-managed scheduler (the GPU/production path), step 2 does not
transfer — do not attempt it.** `maas-vllm-gpu-kserve-router-scheduler` is owned by
the `LLMInferenceService` controller, which reverts manual edits to the Deployment
(docs/design.md, "Override **only** `image`... Do not patch the Deployment directly —
the controller owns `<name>-kserve-router-scheduler` and reverts manual edits.").
Editing the `LLMInferenceService` itself is no safer: KServe templates
`--pool-name`, the ports, the TLS flags, and the whole `--config-text` argument (the
fairness ConfigMap, serialized) into that container's `command`/`args` from the
preset — `deploy/llmisvc.yaml` says to override **only** `image` for exactly this
reason. There is no field on either object that adds `-v=4` without re-deriving that
templated command/args by hand, which this ticket has not attempted and does not
recommend. Enabling the V(4) tier on the KServe-managed path is an open problem, not
a documented one.

**3. Apply both and restart** — the Deployment uses `strategy: Recreate`, so an
`oc apply` on it is enough to cycle the pod, but a ConfigMap-only edit needs an
explicit nudge. This restart step is also POC-only:

```sh
oc apply -f deploy/poc/00-config.yaml -f deploy/poc/02-epp.yaml -n maas-fairness-poc
oc delete pod -n maas-fairness-poc -l app=maas-epp
```

On the KServe-managed path there is no pod to nudge by hand: the `LLMInferenceService`
controller watches the ConfigMap that `scheduler.config.ref` points at and rolls the
scheduler itself once it changes (docs/design.md, "the KServe controller watches
ConfigMaps ... re-resolves `scheduler.config.ref` into the `--config-text` arg, and
rolls the pod automatically"). Step 1 (the ConfigMap edit) does reach that path —
`maas-vllm-gpu` resolves `scheduler.config.ref` to the same `{name: maas-epp-config,
key: epp}` that `deploy/poc/00-config.yaml` ships — only step 2 (the `-v=4` arg) has
no equivalent there.

Then find a request the same way as "Find a request's story from its response
header" above — a healthy, matched request can now also produce a `"per-request
fairness tier"` line, not just the two exception paths.

**Turn it back off** by reverting either edit — re-commenting the two ConfigMap keys,
or dropping `-v`/`"4"` from the args — and re-applying. Note that the time box
re-arms on every EPP restart: a crashlooping or rescheduled pod keeps re-emitting for
up to `requestTierV4TimeBoxSeconds` after each restart even if nobody touched the
config, so reverting the ConfigMap (not just waiting out the box once) is what
actually ends it.
