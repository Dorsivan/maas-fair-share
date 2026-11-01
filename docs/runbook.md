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

## Restore `maas-vllm-cpu` from zero (UNI-98)

Scaled to zero on 2026-11-01 to reclaim the 4 CPU / 16Gi it held standing with
no test touching it ([UNI-88](/UNI/issues/UNI-88)). The route
(`maas-vllm-cpu-kserve-route`) and `maas-trlp-maas-vllm-cpu` were left in
place, so bringing it back is one command — no object was deleted and nothing
else needs to be recreated:

```sh
oc patch llminferenceservice maas-vllm-cpu -n maas-fairness-poc --type=merge -p '{"spec":{"replicas":2}}'
```

It comes back on `deploy/poc/07-vllm-cpu.yaml`'s current scheduler pin,
`quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135`
— the same digest the GPU path runs (UNI-97). Allow ~1-2 minutes for the two
Qwen2.5-0.5B CPU pods to become `Ready`.

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
oc secrets link maas-vllm-cpu-epp-sa quay-maas-pull --for=pull -n maas-fairness-poc
shred -u /tmp/q.json
```

Both service accounts need the link — each LLMInferenceService's router-scheduler
runs under its own `<name>-epp-sa`, and the pull secret does not transfer between
them. UNI-98 (2026-11-01) hit this directly: pinning `deploy/poc/07-vllm-cpu.yaml`'s
scheduler to the digest without this second `oc secrets link` left the CPU-path
scheduler pod in `ImagePullBackOff` — `<auth-denied>` on the private repo — even
though the GPU path, already linked, pulled the same digest fine.

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
in-cluster-registry digest like the one above instead: that image is reachable only
from inside this cluster, and this registry is known to time out from some nodes in
this pool. The digest above exists only to prove the plugin logic end to end from
inside the cluster; it is not a transferable or deployable artifact, and does not
leave this cluster.

Update, UNI-98 (2026-11-01): the CPU-path scheduler
(`maas-vllm-cpu-kserve-router-scheduler-*`) previously ran `maas-epp:latest` off
this same in-cluster registry and was seen sitting in `ImagePullBackOff` against
exactly this failure mode. It, and the two other manifests that shared that
floating tag (`deploy/poc/02-epp.yaml`, `deploy/poc/06-rhoai34-shape.yaml`), are
now pinned to the same Quay digest as the GPU path — see "Restore `maas-vllm-cpu`
from zero (UNI-98)" above.

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
comments of `deploy/poc/04-loadgen.yaml`, plus one named negative control
(UNI-103) — read those comments before touching worker counts, the sizing
reasoning there is load-bearing.

| scenario | what it sets | what it proves |
|---|---|---|
| `full-contention` | `TENANTS="app1 app2 end-users"`, per-tenant `WORKERS_APP1=32 WORKERS_APP2=32 WORKERS_END_USERS=128` | the headline weight split: 20/10/65 delivered under genuine three-way contention, with every tenant over-offering relative to its entitlement |
| `end-users-idle` | `TENANTS="app1 app2"`, per-tenant `WORKERS_APP1=64 WORKERS_APP2=32` (UNI-104; was `128/32` under UNI-103) | end-users' 65% is **absorbed** by app1/app2, not reserved while idle, with app1 over-offering relative to app2 to express their 2:1 (66.7/33.3 renormalized) ratio |
| `equal-workers-control` | `TENANTS="app1 app2 end-users"`, equal `WORKERS` (the **original** full-contention shape) | **negative control, not scored.** Kept to show what an under-offered load looks like on this backend — expected to compress toward equal thirds, not 20/10/65. See "Per-tenant worker sizing and the saturation check" below |
| `app1-alone` | `TENANTS="app1"` | a single tenant receives ~100% of the pool, not capped near its 20% weight |
| `asymmetric-demand` | `WORKERS_APP1=32 WORKERS_APP2=0 WORKERS_END_USERS=2` | app1 is not held near its weight when the highest-weight tenant (end-users) sends only a trickle — this is the YAML's own commented-out example, which also idles app2; the ticket's prose names only APP1/END_USERS but the YAML it points to is the source of truth |

`full-contention` and `end-users-idle` used to set a single global `WORKERS`
for every tenant. UNI-100 traced both scenarios' FAILs on the live
`llama-3-1-8b` backend to exactly that: equal worker counts cannot express a
weighted split once the weights differ (see below), so UNI-103 resized both
to per-tenant worker counts and kept the original equal-worker shape alive
under a new name, `equal-workers-control`, as a deliberate, documented
negative control rather than deleting the evidence of the failure mode.

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
`equal-workers-control` (run with `--control`, which `15-fairness-benchmark.sh`
sets automatically for that scenario) gets a third verdict, INFO, which also
exits 0: a control is expected to show a large deviation, and failing a
pipeline on that would be reporting the control for doing its job.

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
above. `equal-workers-control` is a third kind of special case: it offers
every group a genuine chance to compete too, but is deliberately sized so
that chance cannot be taken (see below) — so its verdict is INFO, not a PASS
or a FAIL against the symmetric threshold (`--control`; see "The PASS/FAIL
threshold" above this section for the exit-code consequence).

### Per-tenant worker sizing and the saturation check (UNI-103)

**The rule, from `deploy/poc/04-loadgen.yaml`'s own comments and
`docs/poc-results.md`'s "detour" section:** a weighted split can only be
measured if every ACTIVE tenant offers more concurrency than its
entitlement. The load generator is closed-loop — a tenant can never have
more than its configured `WORKERS_*` requests outstanding — so if a
tenant's workers are too few, the scheduler serves it faster than it can
resubmit, its queue periodically empties, and an empty queue is not a
candidate in `Pick`. The measured split then compresses toward equal shares
regardless of what the weights say, and that looks exactly like a broken
policy. It is not; it is work conservation correctly giving away capacity
nobody is asking for at that instant.

**This is exactly what broke `full-contention` and `end-users-idle` on the
`llama-3-1-8b` backend (UNI-100):** `15-fairness-benchmark.sh` set
`WORKERS=32` for every tenant in both scenarios. On this backend that is
enough to saturate the LOWEST-weight tenants but not the highest-weight one
in each scenario (`end-users` at 65% in `full-contention`, `app1` at a
renormalized 66.7% in `end-users-idle`), so both scenarios' highest-share
tenant drained its queue and the split compressed toward equal. The fix
(this ticket) is per-tenant worker counts, not a bigger single `WORKERS`:

- `full-contention`: `WORKERS_APP1=32 WORKERS_APP2=32 WORKERS_END_USERS=128`
  — copied from A4 Run 3 (`docs/poc-results.md`, UNI-29), the first config
  that reproduced the weight ordering on this exact backend/model.
- `end-users-idle`: `WORKERS_APP1=64 WORKERS_APP2=32` — app1 is this
  scenario's highest-share tenant once end-users is excluded (66.7% vs
  33.3%, the same 2:1 ratio as their raw 20:10 weights), so it gets the same
  treatment end-users got above: over-offer well past app1's own
  entitlement so its queue cannot drain mid-run. The initial UNI-103 value
  here, `128`, copied `full-contention`'s 4:1 dominant-tenant ratio and
  overshot (82.4% vs a 66.7% target); UNI-104 retuned it to a 2:1 worker
  ratio matching the pair's actual target ratio, which passes (68.4/31.6%
  vs 66.7/33.3%) — see `docs/poc-results.md`'s UNI-104 section.
- `equal-workers-control` keeps the ORIGINAL equal-`WORKERS=32` shape on
  purpose, as a named, permanent negative control — see the scenario table
  above. Its own report says plainly that it is not scored, so a future
  reader does not mistake its large deviation for a regression.

**How to check a tenant was actually saturated, so a future backend change
doesn't silently break this again:** the EPP's own
`llm_d_epp_maas_fairness_contended_seconds_total` (per `fairness_id`,
`pkg/fairness/weightedlas/metrics.go`) counts seconds during which a group
was backlogged while at least one other group in its band was too. Both
`metrics-before.txt` and `metrics-after.txt` already capture it — the
benchmark's `snapshot_metrics` greps every `llm_d_epp_maas_fairness_*`
series, not just the tokens counter used for the share calculation — so no
extra scrape is needed:

```sh
# delta for a group, from the two snapshots a run already produced
before=$(awk -F'[{} ]+' '/contended_seconds_total.*fairness_id="app1"/ {print $NF}' metrics-before.txt)
after=$(awk -F'[{} ]+'  '/contended_seconds_total.*fairness_id="app1"/ {print $NF}' metrics-after.txt)
echo "app1 backlogged ${after:-0} - ${before:-0} of the run's DURATION seconds"
```

**What the delta means — corrected against this ticket's own live numbers,
not assumed.** The first draft of this section claimed a delta close to the
run's `DURATION` means "backlogged the whole run." That is wrong, and the
live re-run (UNI-103, 2026-10-29) caught it before it shipped: even
`full-contention`'s clean PASS (16.2/12.8/71.0% against a 21.1/10.5/68.4%
target) credited each of its three genuinely-offered, genuinely-contending
tenants only ~9 of the run's 240 seconds (app1 9.3s, app2 8.8s, end-users
9.5s) — nowhere near `DURATION`. The metric only accrues per dispatch event,
and only while *that candidate's own priority band* holds more than one
backlogged flow at that exact instant (`plugin.go`'s `maxContendedStep`
additionally caps each such credit at 1 second) — a far narrower window
than "queue non-empty for the whole run." Do not compare the delta to
`DURATION`.

The comparison that IS reliable is relative, within the same run:

- Tenants that are genuinely offered and contending land in the same order
  of magnitude as each other — `full-contention`'s ~9s/~9s/~9s above is the
  reference point.
- An offered tenant whose delta sits near zero, or an order of magnitude
  below its simultaneously-offered peers, was rarely found backlogged
  alongside anyone else — distrust its measured share; resize it up and
  re-run.
- A tenant this scenario did not offer correctly shows a flat `0.0` delta
  (`end-users` in `end-users-idle`, above) — that is the scenario
  definition, not a saturation problem.

**This check's limit, also from a live number rather than a guess:**
`end-users-idle`'s original UNI-103 FAIL (128/32 workers) is a worked example
of what it does *not* catch. app1 (1.50s) and app2 (1.54s) came out almost
identical despite a 4:1 worker-count difference and a 4.7:1 delivered-share
gap (82.4% vs 17.6%, against a 66.7/33.3 target) — so two groups landing
close on this metric does not mean their delivered shares will land close.
It catches an UNDER-contended group reliably (the thing it is built to
detect); it is not a predictor of where a correctly-contending group's exact
share will fall. UNI-104 retuned the worker ratio itself (64/32) to pass,
but the two configs' near-identical `contended_seconds_total` deltas (1.46s
and 1.50s at 64/32, vs 1.50s and 1.54s at 128/32) mean this check still
can't explain *why* one worker ratio overshoots so much more than the other
undershoots — that sensitivity is unexplained, pending
[UNI-100](/UNI/issues/UNI-100)'s scope decision on root-causing it. See
`docs/poc-results.md`'s UNI-103 and UNI-104 sections. A future
backend/model change (new GPU, new model, different `--max-num-seqs`) will
shift the dispatch cadence this check depends on, so re-run it rather than
assuming the worker counts above still saturate every tenant on a different
backend.

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

# 1. Pull the JSON out of this repo's manifest. Do not read it from the
#    maas-fairness-poc ConfigMap -- see the note below this block for why.
python3 -I - deploy/grafana-dashboard.yaml > /tmp/maas-fairness-gpu-epp.json << 'PYEOF'
import re, sys
text = open(sys.argv[1]).read()
_, block = text.split('  maas-fairness-gpu-epp.json: |\n', 1)
lines = [l[4:] if l.startswith('    ') else l for l in block.splitlines(keepends=True)]
sys.stdout.write(''.join(lines))
PYEOF

# 2. Create/update the ConfigMap the grafana Deployment actually mounts.
$OC create configmap kueue-dashboard -n grafana \
  --from-file=maas-fairness-gpu-epp.json=/tmp/maas-fairness-gpu-epp.json \
  --dry-run=client -o yaml | $OC apply -f -

# 3. The volume was optional and absent when the pod last started, so confirm
#    it actually attaches rather than trusting kubelet's periodic resync —
#    restart the pod and recheck the dashboard list in the "Kueue" folder.
$OC delete pod -n grafana -l app=grafana
```

**The `maas-fairness-poc` copy of this ConfigMap must not be assumed
present.** `deploy/poc/cleanup-dead-objects.sh` section 5 deletes
`configmap/maas-fairness-dashboard` in `maas-fairness-poc` by design — the
dashboard JSON's source of truth is this repo, not the cluster — and as of
2026-11-01 it is in fact gone: a named `get` in that namespace returns
`configmaps "maas-fairness-dashboard" not found`. Step 1 above reads
`deploy/grafana-dashboard.yaml` directly so the procedure does not depend on
that object existing. If something else needs the cluster copy back,
`oc apply -f deploy/grafana-dashboard.yaml` recreates it byte-for-byte, but
this procedure does not require that.

Fallback, only if the cluster copy happens to exist and reading it directly
is more convenient than step 1:

```sh
$OC get configmap maas-fairness-dashboard -n maas-fairness-poc \
  -o jsonpath='{.data.maas-fairness-gpu-epp\.json}' > /tmp/maas-fairness-gpu-epp.json
```

As of 2026-10-25 the Engineer role has `edit` on `maas-fairness-poc` only —
`oc auth can-i create configmaps -n grafana` and
`oc auth can-i update configmaps -n grafana` both return `no`. This is the
same shape of access gap as the `maas-fairness-poc` grant itself, but on a
namespace no agent here has ever been granted. Re-run step 1 and re-apply
step 2 any time `deploy/grafana-dashboard.yaml` changes — there is no
automatic sync between the two ConfigMaps. The JSON itself is generated by
`deploy/grafana-dashboard.py` (UNI-130); regenerate before re-loading.

---

## Find a run on the fairness dashboard (UNI-130)

The dashboard (`deploy/grafana-dashboard.yaml`, uid `maas-fairness-gpu-epp`) is
built to judge one benchmark run at a time. Its JSON is generated by
`deploy/grafana-dashboard.py` -- edit that and run
`python3 -I deploy/grafana-dashboard.py --write`, never hand-edit the YAML --
then re-load it with "Load the fairness dashboard into the live Grafana" above.

**Time-range convention.** Every share number on the dashboard is only valid
over exactly one run. A run's window is the `RUN_START`/`RUN_END` pair the
benchmark prints and passes to the report (`--run-start/--run-end`; recorded as
`run_start`/`run_end` in `results/<ts>-.../fairness-report.json`). Open the dashboard on that window, padded by
one minute either side so the ramp is visible, with:

```sh
FROM=$(( $(date -u -d "$RUN_START" +%s) - 60 ))000
TO=$((   $(date -u -d "$RUN_END"   +%s) + 60 ))000
echo "https://grafana-grafana.apps.ocp.paladinaura.com/d/maas-fairness-gpu-epp/?orgId=1&from=$FROM&to=$TO&var-group=All&var-window=2m"
```

Put that exact `from`/`to` pair (epoch ms) in the ticket comment and in the
`docs/poc-results.md` section for the case -- it is the "Grafana time range of
the run" the series asks for. The headline table's numbers then use the same
arithmetic as the report (expected = weight / sum of offered groups' weights;
observed = share of `contended_service_tokens_total`), so they should agree
with the report to within scrape granularity (30 s); if they disagree by more,
the range is wrong or includes another run.

**Finding a run without its timestamps.** Leave the range wide (e.g. last 24 h)
and use the annotations, all computed from Prometheus so nobody has to write
them:

| annotation | colour | source | marks |
|---|---|---|---|
| Loadgen job running | blue | `kube_job_status_active{job_name=~"maas-loadgen.*"} > 0` | the run itself -- zoom to this region |
| EPP process start | red | `process_start_time_seconds` (value used as the timestamp) | EPP restart or pod replacement; all fairness counters reset here (E1) |
| Weights / enforcement changed | purple | `changes()` on `configured_weight` / `enforcing` | live config edits (F1, F3, F6, board weight cases) and their restore |
| vLLM replica change | orange | `changes(kube_deployment_status_replicas_ready{deployment="maas-vllm-gpu-kserve"})` | replica loss / scale (E2) and restore |
| MaaS fairness alerts firing | dark red | `ALERTS{alertname=~"MaasFairness.*", alertstate="firing"}` | alert drill (G1), classification (D2) |

**Variables.** `group` is a multi-select over the `fairness_id` values the EPP
currently exports (new groups in the app3..app6 / 20-group cases appear
automatically; only app1/app2/end-users/unclassified have fixed colours).
`window` (default 2m) is the trailing window used by every "over time" share,
deviation and unclassified-share panel -- shorten it for join/leave/idle
cases (B1-B4), lengthen it for the soak (B6).

**Read it top to bottom.** The first row says whether the rest is worth
reading: enforcement must say ENFORCING (except F1), weights must be the ones
the case intends, replicas 2/2 (except E2), EPP restarts 0 (except E1), and
"Loadgen now" must say IDLE before you start (rule 1). The alert row's first
tile says whether `deploy/prometheusrule.yaml` is evaluated at all -- **as of
2026-11-01 it is not** (`oc get prometheusrule -n maas-fairness-poc` returns
nothing), so the five alert tiles read RULE NOT LOADED rather than a reassuring
OK. The accounting-leak panel evaluates that alert's expression directly, so it
works without the rule.

**Known gaps (cannot be shown from what is exported).**
- In-flight *provisional* tokens: the plugin keeps `provisionalTotal` per group
  (`pkg/fairness/weightedlas/state.go`) but exports it only in the state dump,
  not as a metric. C5 ("provisional tokens return to zero") has to read the
  state dump or the V(4) log, not this dashboard; truing error and the leak
  detector are the closest metric proxies.
- Per-group HTTP status codes: only `llm_d_epp_request_error_total{error_code}`
  is per group. Istio's `response_code` panel is pool-wide; Kuadrant 429s
  rejected before routing may not appear in it at all (unverified -- check in E4).
- Pool-level flow-control outcomes (`llm_d_epp_flow_control_requests_total`)
  carry no `fairness_id`; per-group shedding is read from
  `llm_d_epp_flow_control_request_queue_duration_seconds_count{outcome!="Dispatched"}`,
  which does.
- vLLM series have no group label (the GPU does not know about groups).

### Panel -> metric -> cases it serves

| panel | metric(s) | cases |
|---|---|---|
| Enforcement mode | `llm_d_epp_maas_fairness_enforcing` | all; F1 (shadow), F6 |
| Live configured weights | `llm_d_epp_maas_fairness_configured_weight` | F3, F6, 30/10/60 & 6-group board cases, rule-3 restore |
| EPP build | `llm_d_epp_info{build_ref}` | all (comparability), H2 |
| vLLM replicas / Replicas | `kube_deployment_status_replicas{,_ready}`, `count(vllm:num_requests_running)`, `llm_d_epp_ready_endpoints` | E2, all (validity) |
| EPP restarts in range / restarts and process starts | `kube_pod_container_status_restarts_total`, `process_start_time_seconds` | E1, all (validity) |
| Loadgen now | `kube_job_status_active{job_name=~"maas-loadgen.*"}` | all (rule 1) |
| Rule loaded? + 5 alert tiles | `prometheus_rule_group_rules`, `ALERTS{alertname=~"MaasFairness.*"}` | G1, D2, E3, A6 |
| Expected vs observed table | `configured_weight`, `contended_service_tokens_total`, `llm_d_epp_request_total` | every scored case: A3, A4, A5, B5, D1, F3, H1, board cases |
| Observed vs expected over time / deviation | same, windowed by `$window` | B1, B2, B3, B4, B6, E1, E2, F6, board join case |
| Dispatch share vs token share | `dispatch_total`, `contended_service_tokens_total` | C1, C2, C8 |
| normalized_service / spread / observed half-lives | `normalized_service`, `normalized_service_observed` | B1, B3, B4, B6, E1, F2, NotConverging |
| Contended service / total raw tokens / fraction contended | `contended_service_tokens_total`, `request_{input,output}_tokens_sum`, `contended_seconds_total` | A1, A5, A6, B2, G2 |
| Mean truing error / truing distribution | `truing_error_tokens_{sum,count,bucket}` | C1, C2, C4, C5, G2 |
| Accounting-leak detector | `normalized_service`, `dispatch_total` | C5, C6, B2, AccountingLeak |
| Requests without usage | `requests_without_usage_total` | C3, C6 |
| Newcomer clamps | `newcomer_clamps_total` | B1, B3, B4, F2 |
| Cached prompt-token ratio | `prompt_tokens_cached_ratio` | C8 |
| Unclassified share / unmatched / totals | `llm_d_epp_request_total{fairness_id="unclassified"}`, `unmatched_subscriptions_total` | D2, D3, D5, ClassificationBroken |
| Queue depth / queued bytes | `flow_control_queue_size`, `flow_control_queue_bytes` | all contention cases; C1, C4 |
| Queue wait p50/p95 | `flow_control_request_queue_duration_seconds_bucket{outcome="Dispatched"}` | 30/10/60 join case, B5, A4 |
| Shed / evicted per group | `flow_control_request_queue_duration_seconds_count{outcome!="Dispatched"}` | E3, C4, C5, SheddingIsRealAllocator |
| Flow-control outcomes (pool) | `flow_control_requests_total` | E3, D3 (BandSplit) |
| Pool saturation and capacity | `flow_control_pool_saturation`, `flow_control_capacity_utilization_requests` | A6, B5, all (validity) |
| Request rate per group | `llm_d_epp_request_total` | all; D1, H3 |
| EPP errors per group | `llm_d_epp_request_error_total{error_code}` | C6, E2, E3 |
| Gateway HTTP status codes | `istio_requests_total{response_code}` | C6, E4 |
| TTFT / e2e / NTPOT per group | `llm_d_epp_request_{ttft,duration,ntpot}_seconds_bucket` | H2, C3, C4, board join case |
| KV-cache / running-waiting / vLLM queue+TTFT+preemptions | `vllm:kv_cache_usage_perc`, `vllm:num_requests_{running,waiting}`, `vllm:request_queue_time_seconds`, `vllm:time_to_first_token_seconds`, `vllm:num_preemptions_total` | B5, C4, C8, E2 |
| EPP CPU / memory / scheduling latency | `container_cpu_usage_seconds_total`, `container_memory_working_set_bytes`, `scheduler_e2e_duration_seconds`, `plugin_duration_seconds{plugin_type="maas-weighted-fairness"}` | H2, H3, B6 |

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
... | grep 'flow_control_requests_total.*outcome="Evicted'  # expect absent or 0 (UNI-130: there is no
                                                           # *_evicted_total series; the old grep always passed)

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
**`deploy/poc/13-loadgen-poisson.sh` captures this container's log itself now**
(UNI-46) — see "Per-run EPP log capture" below — so a load-test run no longer
depends on the pod surviving until someone thinks to look.

---

## Per-run EPP log capture (UNI-46)

There is still no log retention on this cluster (docs/design.md "Production
observability"), so `deploy/poc/13-loadgen-poisson.sh` captures the GPU EPP
container's own log for the duration of each run instead of depending on one.
No extra flags needed — it is on by default:

```sh
OPENSHIFT_TOKEN=... DURATION=90 RATE_APP1=8 RATE_APP2=8 RATE_END_USERS=8 \
  SEED=104 OUT=/tmp/run-above MAX_WORKERS=3000 DRAIN_TIMEOUT=180 \
  ./deploy/poc/13-loadgen-poisson.sh
```

produces, alongside the existing `metrics-before.txt` / `metrics-after.txt` / `delta.txt`:

- `$OUT/epp-container.log` — `oc logs -f` on
  `maas-vllm-gpu-kserve-router-scheduler`'s `main` container, started right
  before the generator and stopped right after it exits (including on a
  generator failure — the log is stopped and the manifest below is still
  written before the script re-raises the exit code).
- `$OUT/epp-container-log-manifest.txt` — pod name, container, capture
  start/end timestamps, **byte count**, and `pod_restarted_during_run:
  yes|no`. Check the byte count before assuming the file is complete; a
  multi-GB log for a short run is a sign the pod is unusually chatty
  (`-v` level, a crash loop, or a different workload sharing the pod), not
  something this harness tries to cap.
- If the pod or container restarts mid-run, `epp-container.log` gets an
  inline `### RUN-HARNESS NOTICE` block instead of silently truncating: it
  records the before/after pod UID and restart count, then appends what it
  can recover — `oc logs --previous` for a same-pod container restart, or a
  1000-line tail from the replacement pod if the pod itself was recreated.
  Either way, `pod_restarted_during_run: yes` in the manifest is the signal
  to treat the log as possibly incomplete around that point, not the log's
  absence.

Override `EPP_POD_LABEL_SELECTOR` / `EPP_CONTAINER` to point at a different
pod, or set `CAPTURE_EPP_LOG=0` to disable (e.g. a CPU-path or simulator run —
both out of this harness's GPU-only scope). A run where no pod matches the
selector logs a warning and continues without a log artifact rather than
failing the whole run.

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

---

## Namespace snapshots silently omit Forbidden resource types (UNI-122)

UNI-99's review of the UNI-96 cleanup found that `before.yaml`/`after.yaml` — a
multi-kind `oc get ... -o yaml` redirected to a file — contained **zero**
`InferencePool` objects even though `inferencepool` was in the argument list. No
agent role on this cluster can `list` `inference.networking.k8s.io`:

```
$ oc auth can-i list inferencepools.inference.networking.k8s.io -n maas-fairness-poc
no
$ echo "exit=$?"
exit=1
```

**The mechanism, established empirically (2026-11-01), is more precise than "omitted,
not errored."** A multi-kind `get` where one kind is Forbidden does two things at
once, on two different channels:

```
$ oc get deployment,service,inferencepool -n maas-fairness-poc -o yaml \
    > /tmp/snap.yaml 2>/tmp/snap.err
$ echo "exit=$?"
exit=1
$ cat /tmp/snap.err
Error from server (Forbidden): inferencepools.inference.networking.k8s.io is forbidden:
User "system:serviceaccount:paperclip:poc-agent" cannot list resource "inferencepools"
in API group "inference.networking.k8s.io" in the namespace "maas-fairness-poc"
$ wc -l /tmp/snap.yaml
1664 /tmp/snap.yaml
```

- **stdout is a complete, valid, well-formed `List`** containing every object of
  every *permitted* kind — 1664 lines, identical to running `oc get deployment,service`
  alone with `inferencepool` dropped from the argument list entirely. There is no
  error marker, placeholder, or comment inside the YAML. A reviewer who only opens
  the file sees a document that looks exhaustive.
- **The process still exits non-zero (1) and writes the Forbidden error to stderr.**
  This is the part that refines the review's framing: the capture is not silent
  end-to-end — `$?` and stderr both carry the signal — it is silent **only on the
  channel most reviewers actually look at**, which is the YAML content itself. If
  stderr was redirected to `/dev/null`, merged into the same file as stdout with
  `2>&1` (which would also corrupt the YAML), or simply not captured by whatever
  ran the original `oc get`, the only trace of the gap disappears and the file on
  disk is indistinguishable from a complete snapshot. So: **check `$?`, every
  time, before trusting a redirected capture** — it is a real, working defence
  here, not a false lead — but it is not sufficient by itself, because it is easy
  to lose track of in a pipeline or a script that doesn't check it.

A Forbidden kind requested **alone** behaves the same way, just with an empty list
instead of a partial one — still exit 1, still a valid (empty) document on stdout:

```
$ oc get inferencepool -n maas-fairness-poc -o yaml
apiVersion: v1
items: []
kind: List
metadata:
  resourceVersion: ""
$ echo "exit=$?"
exit=1
```

So mixing a Forbidden kind into a list of permitted ones does not change the
exit code or suppress the stderr message; it only changes what stdout looks like
(a plausible, non-empty document instead of an obviously-empty one). The
partial-but-plausible case is the dangerous one, because `items: []` at least
looks suspicious on inspection, where a 1664-line document of real objects does
not.

**One trap that will fool a text search of the captured YAML**: `grep -c
"kind: InferencePool"` against `/tmp/snap.yaml` above returns `3`, not `0` — but
none of the three are top-level `List` items. They are `ownerReferences` entries
on the Istio-generated `Service` objects for the pool (e.g.
`maas-pool-ip-73df004c`), which the token *can* list:

```yaml
    ownerReferences:
    - apiVersion: inference.networking.x-k8s.io/v1alpha2
      kind: InferencePool
      name: maas-pool
      uid: b440f252-353c-4e6d-9cc6-43148b1a9379
```

Checking "does the capture mention InferencePool" is not the same question as
"does the capture contain InferencePool objects." Only the latter is what a
before/after diff needs.

**Two InferencePool API groups are installed on this cluster, and a Forbidden
response does not tell you which one `maas-pool` actually lives in.** Both are
registered on `api.ocp.paladinaura.com`:

```
inference.networking.k8s.io      v1                    (preferred: v1)
inference.networking.x-k8s.io    v1alpha2, v1alpha1    (preferred: v1alpha2)
```

Every agent token gets `Forbidden` on `list` *and* on `get`-by-name for all
three (`k8s.io/v1`, `x-k8s.io/v1alpha2`, `x-k8s.io/v1alpha1`) — and the error
message just echoes back whichever group/version you asked about. A Forbidden
response is therefore not evidence that `maas-pool` exists in that group, only
that you asked about that group and were denied. The `ownerReferences` entry
quoted above is the only evidence this repo has of which group the *live*
`maas-pool` is actually in, and it says `inference.networking.x-k8s.io/v1alpha2`,
not `inference.networking.k8s.io`.

UNI-123 corrected a mistake that followed directly from this: earlier drafts of
this section and of `deploy/poc/cleanup-dead-objects.sh` attributed the
surviving pool to `inference.networking.k8s.io`, on the strength of the
Forbidden reproduction earlier on this page. That reproduction is still a
correct demonstration of the RBAC boundary — it was just never evidence for
*which* group the object lives in, and got read as if it were.

**The generalisable lesson: a Forbidden error names the group you asked about,
not the group the object is in.** Any `can-i`-style pre-flight built on a bare
short name (`inferencepool`) inherits the same ambiguity — `oc` resolves a bare
short name to exactly one group (the preferred version of whichever CRD
registered it first) silently, with no signal that a second group exists or
that the resolved one is the wrong one. The fix is the same one that applies to
`delete`: the pre-flight has to name the fully-qualified resource —
`inferencepools.v1alpha2.inference.networking.x-k8s.io` — not the bare
`inferencepool`, and if there are multiple candidate groups, check all of them
by their fully-qualified names rather than trusting whichever one the short
name happens to resolve to.

**The set of invisible kinds is a property of the token, not a fixed list.**
Both installed InferencePool groups — `inference.networking.k8s.io` and
`inference.networking.x-k8s.io` — are what's known-invisible in
`maas-fairness-poc` today, for the roles that exist today. A different role, a
changed RoleBinding, or a different namespace can all change which kinds
silently drop out — so the defence belongs in the snapshot procedure itself,
not as a one-time hardcoded exclusion list for these two API groups.

**Pre-flight: verify every kind is actually readable before trusting the
capture.** Loop `oc auth can-i list` over the exact kind list you are about to
pass to `get`, and fail loudly on any `no`:

```sh
NAMESPACE=maas-fairness-poc
# Fully-qualified, not the bare "inferencepool" short name: a bare short name
# resolves to exactly one of the two installed InferencePool groups (see
# above) and would silently stop checking the other one.
KINDS=(deployment service inferencepools.v1alpha2.inference.networking.x-k8s.io)
BLIND=()
for kind in "${KINDS[@]}"; do
  if ! oc auth can-i list "$kind" -n "$NAMESPACE" >/dev/null 2>&1; then
    BLIND+=("$kind")
  fi
done
if [ "${#BLIND[@]}" -gt 0 ]; then
  echo "REFUSING snapshot: cannot list ${BLIND[*]} in $NAMESPACE — capture would" \
       "silently omit these kinds. Get the RBAC gap addressed or drop them from" \
       "KINDS with that gap recorded in the ticket." >&2
  exit 1
fi
oc get "$(IFS=,; echo "${KINDS[*]}")" -n "$NAMESPACE" -o yaml
```

Run against the real kind list, this is what it reports today:

```
$ for kind in deployment service inferencepools.v1alpha2.inference.networking.x-k8s.io; do
    oc auth can-i list "$kind" -n maas-fairness-poc >/dev/null 2>&1 \
      && echo "$kind: ok" || echo "$kind: BLIND"
  done
deployment: ok
service: ok
inferencepools.v1alpha2.inference.networking.x-k8s.io: BLIND
```

That is the authoritative way to know a snapshot is complete — not the exit
code of `get`, and not a `grep` of the result. Keeping stderr alongside stdout
(`2> snap.err` next to `> snap.yaml`, never `2>&1` into the same file, never
`2>/dev/null`) is a cheap second line of defence, but the pre-flight is the one
that fails *before* the capture is trusted, rather than requiring someone to
remember to inspect a second file afterwards.

**Cross-reference:** `deploy/poc/cleanup-dead-objects.sh` already carries this
gap inline, at the `del inferencepools.v1alpha2.inference.networking.x-k8s.io
maas-pool` line — the comment there describes the same RBAC boundary for
*delete*, and (since UNI-123) the correct group for the live object. This
section is the *read*-side counterpart: a dry run's `del` reports its own
Forbidden loudly (see the `del()` function's own `if ! ... delete` check), but
a `get`-based snapshot used to gate that same delete does not, unless stderr
and `$?` are actually checked or the pre-flight above is run first.
[UNI-119](/UNI/issues/UNI-119), the parent of this ticket, is the pending
cluster-admin delete of `inferencepools.v1alpha2.inference.networking.x-k8s.io/maas-pool`
that this same blind spot applies to.

**UNI-124: "which group is the object in" was the wrong question — the repo
creates one in each.** The section above (UNI-123) establishes that a
Forbidden error only names the group you asked about, and corrects an earlier
assumption that `maas-pool` lived in `inference.networking.k8s.io` rather than
`inference.networking.x-k8s.io`. That correction is right as far as it goes,
but it still implies a single live pool with one wrong guess and one right
answer. It is not single. `deploy/poc/02-epp.yaml` declares `maas-pool`
**twice, deliberately**: `inference.networking.k8s.io/v1` at line 88 and
`inference.networking.x-k8s.io/v1alpha2` at line 254. `docs/poc-results.md`,
pitfall 6 ("Two InferencePool API groups, and both are needed"), records why
both have to exist: the EPP watches only the `v1` group, and this cluster's
gateway controller resolves only `x-k8s.io/v1alpha2` backendRefs and rejects a
`v1` pool outright. So the earlier "empty, alphabetically-first
`inference.networking.k8s.io` pool" framing that `deploy/poc/cleanup-dead-objects.sh`
carried before this ticket was wrong on the fact, not just imprecise about it:
that group is not empty, this repo's own manifest puts a real `maas-pool`
there. A cleanup that deletes only the `x-k8s.io` pool (the UNI-123 fix)
leaves the `k8s.io` one behind, silently, every time.

**The two pools also have a detection asymmetry worth keeping, independent of
the RBAC boundary above:**

- The **`x-k8s.io/v1alpha2`** pool is indirectly observable even while
  `get`/`list` on it are Forbidden: the gateway controller resolves it, mints
  `svc/maas-pool-ip-73df004c`, and sets an `ownerReference` back to the pool
  (quoted earlier on this page). That Service is a permitted kind, so its
  continued existence — or its disappearance — is a readable proxy for
  whether the pool it is owned by still exists.
- The **`k8s.io/v1`** pool has no such proxy. This cluster's gateway
  controller never resolves it, so it mints no Service, sets no
  ownerReference, and leaves nothing behind that a permitted kind can
  reflect. There is no garbage-collection signal and nothing to infer
  presence or absence from. Its existence in the cleanup script rests on
  `02-epp.yaml` declaring it, not on anything read from the cluster — and
  absence of evidence is not evidence of absence here: a cluster-admin run
  of the cleanup script that correctly deletes this pool and a run that
  silently no-ops on it would look identical from any token available to an
  agent.

## Restoring a mis-deleted object does not fix the automation that deleted it (UNI-125)

**UNI-96 deleted `serviceaccount/maas-epp-metrics-reader`, it was restored, and
the script that deleted it kept doing so for three more days.** UNI-88's
read-only inventory mis-categorised the SA as dead because its name shares a
prefix with `serviceaccount/maas-epp`, the genuinely-dead v1 simulator SA.
UNI-96 deleted it on that false pairing, which cascade-deleted its
long-lived `secret/maas-epp-metrics-reader-token` and broke the fairness
benchmark's metrics snapshot step (`deploy/poc/15-fairness-benchmark.sh` and
`deploy/poc/13-loadgen-poisson.sh` both read that Secret). The incident was
closed by re-applying the ServiceAccount and Secret from `deploy/rbac.yaml` --
which fixed the cluster, but not `deploy/poc/cleanup-dead-objects.sh`, which
still carried the `del serviceaccount maas-epp-metrics-reader` line that
caused the deletion in the first place.

That line survived two further editing passes on this exact file --
[UNI-123](/UNI/issues/UNI-123) and [UNI-124](/UNI/issues/UNI-124), both of
which corrected the InferencePool deletes four lines above it -- because
neither pass had a reason to look at a line outside its own scope. The restore
had made the cluster look healthy again, so there was no longer a live symptom
pointing back at the script. The next run of the script, by anyone, on any
day, would have deleted the SA again.

**The lesson: a restore closes the incident on the cluster, not in the repo.**
Fixing the live state and fixing the automation that produced it are two
separate actions, and only one of them leaves a trace a future `oc get` can
see. Before closing out an incident that involved restoring a deleted object,
grep the scripts in this repo for that object's name
(`grep -rn <name> deploy/ docs/`) and confirm nothing still targets it for
deletion or pruning. Don't rely on the next person noticing the object is
"still there" -- that is exactly what an un-fixed script and a not-yet-rerun
script both look like.
