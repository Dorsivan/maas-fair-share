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

It comes back on `deploy/poc/07-vllm-cpu.yaml`'s current scheduler pin —
the same digest the GPU path runs, kept in lockstep since UNI-97/UNI-212. That pin has
moved several times since this note was written (most recently to
`sha256:c8a088203f6dc6c48c158d21b6295172a78f18646b06c334e5310a0caedb259f` at UNI-220); check
`git log --oneline -- deploy/poc/07-vllm-cpu.yaml` for the live value rather than trusting
a digest printed in prose. Allow ~1-2 minutes for the two Qwen2.5-0.5B CPU pods to become
`Ready`.

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

Digest produced from `fc27130` and referenced by `deploy/llmisvc.yaml` and
`deploy/poc/09-vllm-gpu.yaml` as of UNI-29 (2026-10-22):

```
quay.io/rh-ee-dsivan/maas-fair-share@sha256:5ddee9a790480658854cb99fc254f71cbc5db949990641adca8dfbdf8a9ce135
```

This closes the drift described in the next section: `main`, checked out clean, now
deploys an image built from its own `HEAD`, published somewhere a different cluster
could also reach it from (subject to the private-repo pull-secret note above).

**This digest is historical, not current — it has moved four times since.** Every code
change to the plugin forces a rebuild (see [§11](../AIRGAP-HANDOFF.md#11-changing-it)'s
rule), and each of UNI-213 (twice), UNI-212, and UNI-220 re-pinned all six manifests, not
just the two UNI-29 fixed. The live digest as of UNI-220 is
`sha256:c8a088203f6dc6c48c158d21b6295172a78f18646b06c334e5310a0caedb259f` — but do not trust
that value either without checking `git log --oneline -- deploy/llmisvc.yaml` first; by the
time you read this it may have moved again.

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
useful to pin than this now-stale one. Both manifests referenced the UNI-29 digest as of
2026-10-22; the discipline "re-run the procedure and bump every manifest in the same
commit" held across each subsequent re-pin (UNI-213 twice, UNI-212, UNI-220 — now six
manifests, not two, since UNI-98 extended it to the rest). It is the discipline that
matters, not this specific digest: check `git log --oneline -- deploy/llmisvc.yaml` for
whichever one is live now.

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
| `app2-alone` | `TENANTS="app2"` (UNI-131) | mirror of `app1-alone` for the lowest-weight tenant: a single tenant receives ~100% of the pool regardless of which weight it carries |
| `app2-idle` | `TENANTS="app1 end-users"`, per-tenant `WORKERS_APP1=32 WORKERS_END_USERS=104` (UNI-132) | promotes the by-hand "S3" check (`docs/poc-results.md`) into the benchmark: app2 excluded entirely (not just idle-but-offered), pair target renormalizes to 23.5/76.5 (20:65), worker ratio sized to match that ratio directly per the UNI-104 lesson |
| `app1-idle` | `TENANTS="app2 end-users"`, per-tenant `WORKERS_APP2=32 WORKERS_END_USERS=208` (UNI-133) | A4 in the same series: app1 excluded entirely, pair target renormalizes to 13.3/86.7 (10:65) -- the most extreme pair ratio (6.5:1) of the three, worker ratio sized to match directly per the same UNI-104 lesson |
| `app2-trickle` | `TENANTS="app1 app2 end-users"`, per-tenant `WORKERS_APP1=32 WORKERS_APP2=2 WORKERS_END_USERS=104` (UNI-134) | A5, promoting the by-hand "S2"/"S4" checks (`docs/poc-results.md`) into the benchmark: unlike `app2-idle`/`app1-idle`, app2 is offered but trickles (2 workers, well under its weight entitlement) alongside two HARD tenants. A weight is a floor, not a ceiling: app2 is not throttled further (it gets ~100% of what it asks for, scored on its own success-rate check in `15-fairness-report.py`'s `capped_groups`), and its unused entitlement goes to app1/end-users, who split it 23.5/76.5 (20:65) -- app2's weight is excluded from that pair's expected-share denominator, same renormalized target as `app2-idle` |
| `asymmetric-demand` | `WORKERS_APP1=32 WORKERS_APP2=0 WORKERS_END_USERS=2` | app1 is not held near its weight when the highest-weight tenant (end-users) sends only a trickle — this is the YAML's own commented-out example, which also idles app2; the ticket's prose names only APP1/END_USERS but the YAML it points to is the source of truth |
| `below-capacity` | `TENANTS="app1 app2 end-users"`, per-tenant `WORKERS_APP1=6 WORKERS_APP2=6 WORKERS_END_USERS=26` (UNI-135) | A6 "below capacity, everyone light": each tenant at ~20% of `full-contention`'s saturating ceiling (32/32/128). Nobody is ever backlogged alongside anyone else, so the policy has nothing to do -- `15-fairness-report.py` reports a fourth verdict, UNCONTENDED, instead of scoring a weighted-split deviation that would only be noise |

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
`below-capacity` (UNI-135) gets a fourth verdict, UNCONTENDED, which also
exits 0 -- see "A fourth verdict: UNCONTENDED" below.

### Per-replica split (UNI-214)

The report says nothing about *which* vLLM replica served each request. The
EPP has no per-endpoint request counter, and `llm_d_epp_per_endpoint_queue_size`
only shows whether a replica had a backlog. When one replica can sit idle for a
whole run (UNI-211 Mechanism B), wrap the run with `deploy/poc/21-replica-split.sh`.
It reads each vLLM pod's own counters through the API-server pod proxy:

```sh
deploy/poc/21-replica-split.sh snapshot /tmp/before.txt
OPENSHIFT_TOKEN=... ./deploy/poc/15-fairness-benchmark.sh full-contention my-label
deploy/poc/21-replica-split.sh snapshot /tmp/after.txt
deploy/poc/21-replica-split.sh diff /tmp/before.txt /tmp/after.txt
```

The diff prints requests finished, share, prompt tokens and prefix-cache hit
ratio per replica. Requests finished should equal the report's total `200`
count. A replica at ~0% share means the scheduling profile has locked onto
the other one; see `docs/poc-results.md` "UNI-214".

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

### A fourth verdict: UNCONTENDED (UNI-135)

`below-capacity` is a fourth kind of special case, and it needed a fourth
verdict rather than reusing `solo`'s or `control`'s: every tenant is offered
(unlike `solo`), and the load is not deliberately mis-sized as a known-bad
negative example (unlike `control`) — it is sized deliberately *light*, well
under what any of them needs to saturate the pool, because this is the
"nobody is actually competing for anything" case the plan's A6 asks for.

The rule is read straight from the EPP's own evidence, the same
`contended_seconds_total` metric "How to check a tenant was actually
saturated" above already uses to *distrust* an under-contended tenant's
share: if every offered group's `contended_seconds_total` delta stays under
`UNCONTENDED_SECONDS_THRESHOLD` (1.0s in `15-fairness-report.py`, an order of
magnitude below the ~9s a genuinely-contending tenant accrues in a 240s
full-contention run), the run is classified UNCONTENDED instead of being
scored against the symmetric weighted-split threshold — that threshold would
only measure noise with nobody backlogged to share against. A genuinely
uncontended run also, correctly, scrapes a near-zero
`contended_service_tokens_total` delta (both SLIs share the same contention
gate in `pkg/fairness/weightedlas/metrics.go`); the report does not read
that near-zero total as "the EPP accounted nothing," the structural FAIL it
is everywhere else, when the run is already classified UNCONTENDED.

This check is skipped for `solo` and for a named `control` — both are
already special-cased above for their own, different reasons, and forcing
either through the UNCONTENDED rule as well would blur two genuinely
different situations ("nobody to contend against" vs. "deliberately
under-offered as a known-bad example" vs. "offered, but too lightly to ever
contend") into one label.

**Correction (UNI-137):** a *missing* `contended_seconds_total` line for a
group (not present in either the before or after snapshot) is read the same
way as a present delta under the threshold, not as disqualifying. The EPP's
Prometheus client only registers a counter for a label on its first
increment, so a group that has never once been contended has no line at
all — stronger evidence of zero contention than a present-but-flat delta,
not weaker. This is only trusted when corroborated by an equally
missing/zero `contended_service_tokens_total` delta for the same group
(the two SLIs share one contention gate, so real contention cannot produce
tokens without seconds); this keeps an older test fixture that defines only
`contended_service_tokens_total` and never bothers with
`contended_seconds_total` from being misread as uncontended too. See
"UNI-137: B5, open-loop (Poisson) below / at / above saturation" in
`docs/poc-results.md` for the live run this was found on.

The ticket's other expectation — p50/p95 latency per tenant close to that
tenant's own *solo* latency — is not an automated gate in this report: a
true per-tenant solo-latency baseline does not exist for all three groups
(`app1-alone`/`app2-alone` exist; there is no `end-users-alone` scenario in
this suite), so comparing against an incomplete reference set would be
comparing against prose, not evidence. See `docs/poc-results.md`'s UNI-135
section for the by-hand comparison against the two solo baselines that do
exist, and what is explicitly not proven for `end-users`.

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
- `app2-idle` (UNI-132): `WORKERS_APP1=32 WORKERS_END_USERS=104` — app1
  anchored at the usual baseline 32, end-users scaled to 32*(65/20)=104 so
  the offered-worker ratio matches the pair's actual 20:65 target ratio
  directly, applying the UNI-104 lesson (match the ratio to the target, don't
  copy another scenario's dominant-tenant ratio verbatim) from the start
  instead of discovering an overshoot first.

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

### Timeline, chaos, and windowed reporting (UNI-127)

The scenarios above all offer a fixed set of tenants for the whole run and
score one before/after delta. The board's edge-case plan ([UNI-117](/UNI/issues/UNI-117))
needs more than that: a tenant joining mid-run, a tenant flapping on and off,
and the system surviving an EPP pod delete or a vLLM replica scale-down
without the split falling apart. UNI-127 is the harness work those cases
need — **it does not itself run or score a case**; it adds the capability and
proves it does not change any existing scenario's verdict.

**Per-tenant timeline.** `deploy/poc/04-loadgen.yaml`'s `run.sh` now takes, per
tenant, a `START`/`STOP` offset (seconds from the Job's own start; default:
active for the whole run) and an optional `DUTY` on/off cycle (`"<on>/<off>"`
seconds; default: no cycling). `15-fairness-benchmark.sh` passes these through
unchanged when you set them in the environment — note no unit suffix once it
reaches the Job, but the ticket's `120s` shorthand is accepted at the shell:

```sh
END_USERS_START=120s APP1_DUTY=30s/30s \
  OPENSHIFT_TOKEN=... ./deploy/poc/15-fairness-benchmark.sh full-contention app3-joins-smoke
```

Unset (the default for every scenario above), nothing changes — that is the
regression bar this ticket has to clear, not a suggestion.

**Chaos hooks.** Two independent, one-shot hooks, each a seconds-offset from
run start:

- `CHAOS_EPP_DELETE_AT=<seconds>` — deletes the EPP scheduler pod
  (`$EPP_POD`, resolved the same way the rest of the script already does).
  The Deployment recreates it; what it does NOT do is keep
  `epp-container.log` continuous across the delete — the log-capture loop
  re-attaches to the same pod NAME by design (UNI-46), and a deleted pod's
  replacement has a different one. That gap is a known, accepted limitation
  of this ticket, not something it claims to solve; the chaos event itself
  (what happened, when) is still recorded in `chaos-events.log`.
- `CHAOS_SCALE_AT=<seconds>` (hold `CHAOS_SCALE_HOLD`, default `30s`) —
  patches `LLMISVC_NAME` (default `maas-vllm-gpu`) from its live replica
  count down to 1, then back, via `spec.replicas` on the
  LLMInferenceService CR (the model replicas, not the EPP scheduler's — see
  `deploy/poc/09-vllm-gpu.yaml`).

Both are logged, with a UTC timestamp, to `chaos-events.log` in the run's
results directory. The scale-down/restore also has a second, independent
safety net beyond the chaos loop itself: the script reads the LLMISVC's
*actual* replica count before doing anything (not a hardcoded 2), and both
the normal end-of-run path and the `EXIT` trap compare the live count against
it and patch back if the chaos loop did not get to finish — rule 3 ("leave
the cluster as you found it") applies to a chaos run same as any other.

**Windowed reporting.** Every run — with or without timeline/chaos knobs —
now also scrapes `/metrics` every `WINDOW_SECONDS` (default 10) into
`metrics-timeseries.txt`, not just before and after. The report turns
consecutive scrapes into windows: delivered-token delta, and (for whichever
tenants `timeline-config.json` says were actually scheduled active at that
window's midpoint) expected/observed share and deviation, using the exact
same definitions as the whole-run numbers — see `deploy/poc/15-fairness-report.py`'s
module docstring. A plain scenario with no timeline overrides gets a
`timeline-config.json` with an empty tenant map, which means "every offered
tenant active the whole run" — the one, prior assumption — so the windows for
an old-style run should track the whole-run before/after numbers closely.

**Time-to-converge.** A "phase edge" is any second-offset where something
about the run's shape changes: a tenant's start/stop/duty transition, or a
chaos event (run start, `t=0`, is always one too). For each edge, the report
finds the first window from which every active tenant's deviation stays
within `THRESHOLD_POINTS` for the rest of that phase (a single in-threshold
window surrounded by out-of-threshold ones does not count) and reports how
many seconds that took. A phase that never settles reports `n/a`, not a
guessed number.

**The existing whole-run `verdict` is untouched.** All of the above lives
under a new, separate `report["timeline"]` key (`null` when
`--metrics-timeseries` is not passed, e.g. an older caller). Nothing in
`build_report`'s PASS/FAIL/INFO logic reads it. The regression evidence for
this is a `full-contention` re-run with no timeline/chaos overrides,
recorded under `docs/poc-results.md`'s UNI-127 section — same scenario, same
script invocation shape, verdict unchanged from the prior `full-contention`
runs in this file.

Unit coverage for the windowed and convergence maths (schedule resolution,
phase-edge enumeration, per-window share/deviation, and both the
"converges-and-stays" and "never converges" convergence cases) lives
alongside the existing tests:

```sh
python3 -I deploy/poc/15-fairness-report-test.py
```

---

### Request-shape profiles (UNI-128)

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan needs more than a fixed
request shape: C1-C6 each exercise a different dimension of what a single
request can look like -- short vs. long prompts, missing or huge
`max_tokens`, `stream: true`, a client that disappears mid-generation, a
prompt too big for the context window, and generations that run for
minutes. UNI-128 is the harness work those cases need -- **it does not
itself run or score a case**, same scope boundary as UNI-127. Every knob
below defaults to the single fixed shape `deploy/poc/04-loadgen.yaml` sent
before this ticket (a 1200-word prompt, `max_tokens: 64`, no streaming, no
client aborts, no oversized prompts), so a plain scenario invocation is
unaffected.

**The knobs**, all per-tenant-profile, independently rolled per request (not
mutually exclusive buckets -- see `send_one()`'s precedence note for what
happens when more than one fires on the same request):

| env var | default | what it does |
|---|---|---|
| `PROMPT_WORDS_MIN` / `PROMPT_WORDS_MAX` | `1200` / `1200` | prompt length distribution, in words (uniform between the two; equal = fixed, the prior behaviour) |
| `MAX_TOKENS_DEFAULT` | `64` | `max_tokens` sent on an otherwise-unmodified request |
| `MAX_TOKENS_OMIT_FRACTION` | `0` | fraction of requests that omit `max_tokens` entirely (C2) |
| `MAX_TOKENS_HUGE_FRACTION` / `MAX_TOKENS_HUGE_VALUE` | `0` / `32000` | fraction of requests that ask for a very large `max_tokens` (C2) |
| `STREAM_FRACTION` | `0` | fraction of requests sent with `"stream": true` (C3) |
| `ABORT_FRACTION` | `0` | fraction of requests the client cancels mid-flight, at a random point (C5) |
| `ABORT_MIN_FRACTION` / `ABORT_MAX_FRACTION` | `0.1` / `0.6` | that cancel point, as a fraction of `REQUEST_TIMEOUT_SECONDS` (e.g. default: cancel somewhere between 10% and 60% of the way to the timeout) |
| `OVERSIZED_FRACTION` / `OVERSIZED_PROMPT_WORDS` | `0` / `12000` | fraction of requests that send a prompt deliberately larger than the backend's context window, expecting a 400 (C6) |
| `LONG_GEN_FRACTION` / `LONG_GEN_MAX_TOKENS` | `0` / `2000` | fraction of requests that ask for a long generation (C4); size `LONG_GEN_MAX_TOKENS` and `REQUEST_TIMEOUT_SECONDS` together for your target wall-clock duration -- see the note below |
| `REQUEST_TIMEOUT_SECONDS` | `300` | per-request `curl -m` timeout; also the window `ABORT_MIN/MAX_FRACTION` are relative to |

`15-fairness-benchmark.sh` passes all of these through unchanged when set in
the environment, the same mechanism as UNI-127's timeline vars
(`PROFILE_VARS`, next to `TIMELINE_VARS`):

```sh
STREAM_FRACTION=0.3 MAX_TOKENS_OMIT_FRACTION=0.1 MAX_TOKENS_HUGE_FRACTION=0.1 \
ABORT_FRACTION=0.05 OVERSIZED_FRACTION=0.02 \
  OPENSHIFT_TOKEN=... ./deploy/poc/15-fairness-benchmark.sh full-contention profile-smoke
```

**Long generations, concretely.** "5-9 minutes" is a wall-clock target, not a
token count -- this backend's actual tokens/sec depends on contention, batch
size, and the model, so `LONG_GEN_MAX_TOKENS` has to be sized empirically for
whatever scenario uses it, and `REQUEST_TIMEOUT_SECONDS` (the `curl -m` on
every request, long-generation or not) has to be raised to clear your target
plus a buffer, or the client kills its own long requests before the backend
finishes them. [UNI-150](/UNI/issues/UNI-150) (C4, "near the 600s timeout")
is exactly where that sizing gets pinned down against the real backend; this
ticket only has to prove the knob moves generation length in the right
direction, not calibrate it.

**UNI-150's pinned-down numbers, for the next person sizing this knob.**
Per-sequence decode throughput on this backend is governed far more by how
many *concurrent* long-gen sequences share the decode budget than by token
count in isolation: 8 concurrent long-gen workers cleared `max_tokens: 4000`
in ~51s median (too fast for 5-9 minutes within the 8192-token context
window at that concurrency -- 8150 max completion tokens / ~80 tok/s ≈
102s), while 104 concurrent ones took ~280s at the same token target but
pushed KV-cache usage into a regime that produced a 20-30% HTTP 500 rate
(resource exhaustion, not a timeout artifact). The `near-timeout-long-generations`
scenario added by this ticket lands in between: 48 concurrent long-gen
workers at `LONG_GEN_MAX_TOKENS=8100` (near this backend's real context
ceiling) measured **p50 297.9s / p95 402.8s** -- squarely inside the 5-9
minute band -- with `REQUEST_TIMEOUT_SECONDS=900` giving enough headroom to
observe real completions rather than client-side cutoffs. Treat these as
specific to this backend/model/replica-count, not a portable constant.

**Usage, streamed or not, from one grep path.** `deploy/poc/09-vllm-gpu.yaml`
already sets `--enable-force-include-usage`, which makes vLLM put the usage
block in the final chunk of a streamed response the same as it would in a
whole, non-streamed one. `send_one()` never parses JSON (this image ships
neither `jq` nor `python3`) -- it greps the raw response body for
`"prompt_tokens"`/`"completion_tokens"` and takes the last match, which is
the right (and only) occurrence either way. A client abort has no usage to
read (the fields never arrived), so `send_one()` skips the grep and records
`-1`/`-1` for both, distinct from "the field was present and zero."

**The client-side record.** Every request appends one line to its tenant's
raw log inside the pod (`code latency prompt_tokens completion_tokens
aborted max_tokens_value max_tokens_kind stream`) -- columns 1-2 are exactly
the original "code time_total" shape the closing table and
`15-fairness-report.py`'s `STATUS_PAIR` regex already parse by position, so
that existing parsing is untouched. At the end of the run, `run.sh` also
emits one `CLIENT_RECORD_JSON {...}` line per tenant to stdout: requests
sent, status tally, total prompt/completion tokens actually received,
aborts, and errors. `15-fairness-benchmark.sh` pulls those lines out of the
pod's log and writes them to `client-request-summary.jsonl` in the run's
results directory, so G2 (ledger cross-check) can diff client-recorded
tokens against the EPP's own before/after counters without the pod needing
to still exist. **Known gap:** the printed STATUSES column in the closing
table includes `ABORT` as a literal code, but `15-fairness-report.py`'s
`STATUS_PAIR` regex (`\d+=\d+`) only extracts digit-coded pairs into its
structured `status_tally`, so an abort is visible in
`client-request-summary.jsonl` and in the raw per-request log, but not in
that report field. Out of this ticket's scope to change.

**The regression bar.** A plain scenario invocation with none of the above
set must produce the identical request shape this script sent before this
ticket -- same 1200-word prompt (300 repeats of the 4-word phrase), same
fixed `max_tokens: 64`, no streaming, no aborts. Evidence for this (a
`full-contention` re-run, verdict and magnitude compared against the
UNI-103/UNI-127 baselines) is in `docs/poc-results.md`'s UNI-128 section.

---

### Identity-variant harness (UNI-129)

[UNI-117](/UNI/issues/UNI-117)'s edge-case plan also needs variants in HOW a
request proves its identity, not just what the request contains: many keys
per tenant, an arbitrary/mistyped subscription name, a forged classification
header, and a request that reaches the EPP with no subscription identity at
all. UNI-129 is the harness work those cases (D1, D2, D3, D5) need -- **it
does not itself run or score a case**, same scope boundary as UNI-127/128.
Every knob defaults to this script's pre-UNI-129 behaviour, so a plain
scenario invocation is unaffected.

**D1 -- key rotation.** `END_USERS_KEYS` (default: `"end-user-alpha
end-user-beta"`, the original two) is a space-separated list of `/keys/<name>`
files; the end-users tenant's workers round-robin across however many are
listed, instead of alternating a fixed pair. Every name must resolve to a
real, already-minted key in the `maas-loadgen-keys` Secret -- this widens the
number of distinct CREDENTIALS, not identities, since every one of them
still has to be a valid `end-user-*` MaaSSubscription for the prefix rule to
mean anything. The key inventory below adds 20 (`end-user-gen01` ..
`end-user-gen20`) for this case.

**D2 -- arbitrary/custom subscription identity.** A new `custom` pseudo-tenant
(add it to `TENANTS`) sends load under `CUSTOM_SUBSCRIPTION_NAME` (no
default -- there is no one arbitrary name to default to), with
`WORKERS_CUSTOM`/`CUSTOM_START`/`CUSTOM_STOP`/`CUSTOM_DUTY` following the same
pattern as the three built-in tenants. This is the generic mechanism the
case needs; the mechanism itself was first smoke-tested against an existing
identity (`CUSTOM_SUBSCRIPTION_NAME=app1-production`): live on 2026-11-01,
34 `custom`-tenant requests all returned 200 and the EPP's own
`llm_d_epp_flow_control_request_enqueue_duration_seconds_count{
fairness_id="app1"}` showed exactly 34 -- the generic plumbing classifies
correctly end to end. **The specific identity the ticket names, `enduser-foo`
(no hyphen after "end," so it deliberately falls outside the `end-user-`
prefix match and lands in `unclassified`), was provisioned once the board
granted this role `create` on `maassubscriptions` (2026-11-02) -- see "D2,
resolved" below** for the grant, the identity gotcha that briefly hid it,
and the live classification proof (`CUSTOM_SUBSCRIPTION_NAME=enduser-foo`,
70/70 requests `200`, all 70 counted by the EPP's own
`unmatched_subscriptions_total` regression detector).

**D3 -- forged fairness-id header.** `FORGE_FAIRNESS_ID_FRACTION` (default
`0`) and `FORGE_FAIRNESS_ID_VALUE` (default `app1`) add
`x-llm-d-inference-fairness-id: <value>` to that fraction of requests, **on
top of** the request's real key -- the point is to confirm the plugin's
unconditional `PreRequest` overwrite (design.md, "Security: headers must be
stripped at the gateway") holds even when a legitimately-authenticated
end-user mixes in a forged header, not to find a new hole. The per-request
log gets a 9th column (`forged`, 0/1) and `CLIENT_RECORD_JSON` gets a
`forged_fairness_id` count, so a later pass can confirm the forged requests
didn't move. **Live proof, 2026-11-01:** 68 end-users requests with
`FORGE_FAIRNESS_ID_FRACTION=0.5` (36 of them forged to `app1`) against 34
real `custom`-tenant (`app1-production`) requests with none forged -- the
EPP's own counters still showed exactly 34 under `fairness_id="app1"` and 68
under `fairness_id="end-users"`. Zero of the 36 forged requests crossed over;
the defense holds.

**D5 -- a path with no/empty `x-maas-subscription`.** This is not a
`04-loadgen.yaml` knob -- it is an auth-boundary question, not a
fairness-share one, so `deploy/poc/16-loadgen-identity-variants.sh` is a
small standalone probe instead (same style as `12-loadgen-route.sh`: a few
single requests, not a closed-loop generator). The mechanism: the per-model
AuthPolicy sets `X-MaaS-Subscription` to `(has(auth.metadata.apiKeyValidation)
? subscription : "")`, and `apiKeyValidation` only populates for a request
that authenticated with a real `sk-oai-` key -- so a request that
authenticates some OTHER way (a plain Kubernetes ServiceAccount token, via
the Gateway-level `kubernetes-user` AuthPolicy rule) reaches the EPP with
this header forced empty, regardless of anything the client sent.
`docs/gateway-header-stripping.md`'s 2026-10-19 live proof against
`maas-vllm-cpu` used exactly this mechanism (for a different header).

**Live finding, 2026-11-01, against the actual SUT
(`maas-vllm-gpu-kserve-route`): this path is CLOSED, not open.** Unlike the
CPU route (no AuthPolicy of its own, still inherits the unrestricted
Gateway-level rule), the GPU route now has its own `maas-auth-maas-vllm-gpu`
AuthPolicy, and its `authentication` rules **atomically replace** the
Gateway-level ones for this route rather than merging with them --
confirmed live, not inferred:

| probe | result |
|---|---|
| real `sk-oai-` key, `/v1/chat/completions` (control) | `200` |
| k8s token, `/v1/chat/completions` | `401` -- neither of this route's own authn rules matches (`api-keys` needs an `sk-oai-` key; `kubernetes-tokens` is scoped to `.*/v1/models$`) |
| k8s token, `/v1/models` | `403` -- this path DOES match `kubernetes-tokens` and authenticates, but then fails `require-group-membership` (a ServiceAccount's OpenShift groups are never in `allowed_groups`) -- and `/v1/models` isn't the inference path the fairness plugin classifies on regardless |

Minting a key was also tried both ways directly against `maas-api`: omitting
`subscription` from the mint request silently assigns the caller's own first
eligible subscription (it does not mint a subscription-less key), and
naming a subscription that doesn't exist is rejected outright at mint time
(`400 invalid_subscription`). So on this route, today, **every request that
actually reaches the backend carries a real, non-empty subscription** -- D5
does not currently reproduce against the GPU SUT. Run
`./deploy/poc/16-loadgen-identity-variants.sh maas-vllm-gpu` to re-check this
mechanically rather than trusting this date forever: any future change that
re-attaches the route to a different (or no) AuthPolicy could reopen it
silently, the same "keeps this from silently regressing" concern
`docs/gateway-header-stripping.md` raises for the objective header. Passing
`maas-vllm-cpu` reproduces the OPEN case for comparison -- but only while
that LLMInferenceService is scaled above 0 replicas (it is normally scaled
to zero, see "Restore `maas-vllm-cpu` from zero" above); a 0-replica probe
fails at the connection level, which must not be misread as "the path is
closed."

**D2, resolved (2026-11-02).** Minting the `enduser-foo` key needed the
subscription `enduser-foo` to exist as a real `MaaSSubscription` object
(confirmed by testing the mint call directly: naming a non-existent
subscription returns `400 invalid_subscription`, not a silently-accepted
key). Creating one needed `create` on `maassubscriptions.maas.opendatahub.io`
in the `models-as-a-service` namespace, which this role did not have --
raised to the board (approval
[710871b2](/UNI/approvals/710871b2-3030-44c1-a6cb-21386b04a216)) rather than
worked around.

The board granted it: `Role`/`RoleBinding` `poc-agent-maassubscriptions` in
`models-as-a-service`, scoped to `maassubscriptions.maas.opendatahub.io`
only, `create`/`get`/`list`/`watch` (no `update`/`patch`/`delete` -- the five
pre-existing subscriptions back live keys, so write access to them was
deliberately withheld), bound to `ServiceAccount paperclip/poc-agent`.
**Gotcha that cost a round trip:** this environment's default `oc` context
authenticates as `system:serviceaccount:paperclip:poc-viewer`, a different
identity from `poc-agent` -- so a bare `oc auth can-i create maassubscriptions
-n models-as-a-service` kept returning `no` even after the grant landed.
Always run `oc whoami` first; here, re-running the same check with
`--token="$OPENSHIFT_TOKEN"` (which authenticates as `poc-agent`) explicitly
confirmed `yes`. For a subresource check use `can-i create
pods --subresource=exec`, not `can-i create pods/exec` -- the slash form
parses as TYPE/NAME ("may I create a pod *named* exec") and silently
misleads in both directions; did not come up here but is the same class of
identity/permission-checking trap.

With the grant confirmed against the right identity, `MaaSSubscription
enduser-foo` was created directly (`oc create -f -`, owner group
`maas-end-users` -- reusing an existing group already permitted on
`maas-vllm-gpu`, rather than creating a new `Group` or touching
`MaaSAuthPolicy`, neither of which this role can do: `oc auth can-i create
groups.user.openshift.io` is `no`, and `maasauthpolicies` is not even
listable by this role). A key was minted against it the same direct way as
D1's keys (see "Mint a MaaS API key" above) and stored in
`secret/maas-loadgen-keys` as `enduser-foo`. Live-verified: a 25s/2-worker
smoke run sent 70 requests, all `200`, and the EPP's own
`llm_d_epp_maas_fairness_unmatched_subscriptions_total` counter moved `0` ->
`70` -- the exact regression-detector metric design.md calls out for "a typo
silently falls into `unclassified`" -- confirming `enduser-foo` lands in
`unclassified`, not some accidental match.

**Key inventory (names and subscriptions only -- never values).** All keys
live in `secret/maas-loadgen-keys` in `maas-fairness-poc`:

| key name | bound subscription | minted | expires |
|---|---|---|---|
| `app1-production` | `app1-production` | pre-existing (UNI-29 era) | not re-verified this ticket |
| `app2-batch` | `app2-batch` | pre-existing (UNI-29 era) | not re-verified this ticket |
| `end-user-alpha` | `end-user-alpha` | pre-existing (UNI-29 era) | not re-verified this ticket |
| `end-user-beta` | `end-user-beta` | pre-existing (UNI-29 era) | not re-verified this ticket |
| `end-user-gen01` .. `end-user-gen20` | alternating `end-user-alpha`/`end-user-beta` (odd=alpha, even=beta) | 2026-11-01 (this ticket) | 2026-12-01 (30d) |
| `enduser-foo` | `enduser-foo` (new `MaaSSubscription`, owner group `maas-end-users`, deliberately outside the `end-user-` prefix match) | 2026-11-02 (this ticket) | 2026-12-02 (30d) |
| `app3` .. `app20` | `app3` .. `app20` (one key each, key name = subscription name; owner group `maas-poc-users`; UNI-187) | 2026-11-02 (UNI-189) | 2026-12-02 (30d) |

`end-user-gen01`..`20` are 20 distinct `sk-oai-` credentials for D1 -- 20
keys, 2 real subscriptions, which is what API key *rotation* actually means
(same identity, different credential). Minting them the direct way (see
"Mint a MaaS API key" above) does not need `oc port-forward`: this
environment has direct pod-network reachability to the `maas-api` Service's
ClusterIP (`oc get svc maas-api -n redhat-ods-applications -o
jsonpath='{.spec.clusterIP}'`), which answers the same `POST .../v1/api-keys`
call without a forwarding tunnel. **The mint response body contains the raw
key in plaintext** (`{"key":"sk-oai-...", ...}`) -- always redirect it to a
file (`curl ... -o <file>`) and extract only non-sensitive fields
(`id`/`name`/`subscription`/`expiresAt`) for any inventory record; never let
the body reach stdout, a variable that gets echoed, or a committed file. If
a value is ever exposed, revoke it immediately: `DELETE
.../v1/api-keys/<id>` with the same `X-MaaS-Username`/`X-MaaS-Group` headers
the mint call used (a bare `Authorization`-only `DELETE` 500s).

---

### Cache-shape profile harness (UNI-136)

C8 needs two tenants in the *same* run with deliberately different cache-hit
profiles -- every scenario before this ticket deliberately sent every tenant
the identical prompt shape, so cache effects would not confound the
weighted-split measurement (see "Scenario matrix" and "Per-group
cache-hit profile" in `docs/poc-results.md`). `CACHE_SHAPE_APP1` /
`CACHE_SHAPE_APP2` / `CACHE_SHAPE_END_USERS` (unset = unchanged, the global
`PROMPT_WORDS_MIN`/`MAX` shape applies to that tenant as before) add that:

| value | what it sends |
|---|---|
| `hot` | a byte-identical 160-word shared prefix plus a short unique tail -- same construction as `deploy/poc/10-cache-profile.yaml`'s app1 "fixed" shape |
| `cold` | a fully unique 40-word body every request, no shared prefix at all -- that file's app2/control shape |

`15-fairness-benchmark.sh`'s `cache-heavy-vs-cache-cold` scenario sets
`CACHE_SHAPE_APP1=hot CACHE_SHAPE_APP2=cold` via the same
`PER_TENANT_OVERRIDES` mechanism as `WORKERS_APP1`/`APP2` (no new
pass-through env list needed -- these are scenario-fixed, not meant to be
overridden ad hoc at invocation time the way the UNI-128 profile knobs are).

**Restart the EPP pod before the run, not during.**
`llm_d_epp_maas_fairness_prompt_tokens_cached_ratio` is a cumulative Gauge
(`groupState.cachedRatio()`, `pkg/fairness/weightedlas/state.go`) --
cached/total prompt tokens since the EPP **process** started, not scoped to
one run. Any prior run that sent the same highly-cacheable prompt to every
tenant (every scenario before this ticket did) leaves the ratio reading
high for every group, `cold` included, until the process restarts. Delete
the EPP scheduler pod and wait for `Ready` *before* invoking the benchmark
script -- `15-fairness-benchmark.sh` resolves `EPP_POD` fresh at its own
start, so a restart done first is invisible to its mid-run restart
detection (which would otherwise mark the run's deltas invalid). A restart
also resets `configured_weight`/`enforcing`, which the EPP re-populates
from the live config immediately on startup -- confirm they read correctly
again before starting the run, same as any other config-touching step.

**`oc` must be on `PATH`** before invoking `15-fairness-benchmark.sh`/
`13-loadgen-poisson.sh` directly: both scripts build `$OC` as `oc
--token=...`, a bare `oc` as the first word, so whatever shell runs them
needs the real binary on `PATH` (e.g. `PATH=/paperclip/bin:$PATH` in this
environment). Without it, the script fails loudly with "command not found"
on its own first `$OC` call (clearing out any stale Job from a prior run),
`set -euo pipefail` stops it there, and nothing on the cluster is touched
for this attempt -- but it is still easy to misread as "`oc` isn't
installed" rather than "not on `PATH` for this shell."

**Reading the result.** `15-fairness-report.py` added two fields to each
group's row: `prompt_tokens_cached_ratio` (an `after`-snapshot read, not a
before/after delta -- it is already run-scoped once the EPP was freshly
restarted, per above) and `dispatch_total` (a normal before/after delta,
same mechanism as `contended_seconds`) -- the latter because the panel
table above already names `dispatch_total` as this case's own metric for
"request count," as an EPP-side cross-check independent of the loadgen's
own `requests_total`/`delivered_tokens`/share, which were already in every
report. Run
this case with `--control` (`15-fairness-benchmark.sh` sets this
automatically for `cache-heavy-vs-cache-cold`): the ticket asks for a
characterisation (split by charged tokens, request count, and cache ratio),
not a PASS/FAIL, and the weighted-split threshold is not the question this
case is answering. See `docs/poc-results.md`'s UNI-136 section for the full
result and what it says about the `cachedInputTokenWeight` decision.

### Per-group configuration (UNI-179)

Before this ticket `deploy/poc/04-loadgen.yaml` hardcoded three groups
(`app1`, `app2`, `end-users`), and every UNI-128 request-shape knob applied to
all of them at once. That meant C1 could not give app1 short prompts and long
outputs while app2 did the reverse, and C3/C5/C6 could not stream, abort or
oversize one tenant while the others stayed clean. UNI-179 swaps the
hardcoded ladder for a group table. Like UNI-127/128 it is **harness work
only and does not run or score a case**. Unset, the table is exactly the old
three groups, so existing scenarios are unchanged (see "The regression bar"
below).

**The group table.** `LOADGEN_GROUPS` is a space-separated list, one entry per
group:

    <name>[:<workers>[:<key>,<key>,...]]

It defaults to `TENANTS`, so a scenario that only sets `TENANTS` runs the
same groups as before. `<name>` is also the label the run records the group
under: the closing TENANT table row, the `CLIENT_RECORD_JSON` `"group"`, and
the report's rows. `15-fairness-report.py` joins those to the EPP's
per-group metrics by name, so **the name must be the fairness id the group's
keys classify to.** Names are lowercase letters, digits and `-`. The variable
is not called `GROUPS` because that is a bash special variable, and bash
silently drops any value assigned to it.

**Per-group overrides.** Each setting resolves in this order: the group's own
env var, then the inline field, then the global/built-in default. The env var
name is built from the group's TOKEN, which is the name upper-cased with `-`
turned into `_` (`end-users` -> `END_USERS`, `app3` -> `APP3`):

| setting | per-group env var | fallback |
|---|---|---|
| worker count | `WORKERS_<TOKEN>` | inline `<workers>`, then `WORKERS` |
| keys | `<TOKEN>_KEYS` (space-separated) | inline `<key>,...`, then built-in (below) |
| timeline (UNI-127) | `<TOKEN>_START` / `_STOP` / `_DUTY` | `0` / `DURATION` / no cycling |
| every request-shape knob | `<KNOB>_<TOKEN>` | the global `<KNOB>` |

The request-shape knobs that can be set per group are all of the UNI-128
table above, plus the two that were already per-group, plus the D3 forge pair:
`PROMPT_WORDS_MIN/MAX`, `MAX_TOKENS_DEFAULT`, `MAX_TOKENS_OMIT_FRACTION`,
`MAX_TOKENS_HUGE_FRACTION/VALUE`, `LONG_GEN_FRACTION`, `LONG_GEN_MAX_TOKENS`,
`STREAM_FRACTION`, `ABORT_FRACTION`, `ABORT_MIN/MAX_FRACTION`,
`OVERSIZED_FRACTION`, `OVERSIZED_PROMPT_WORDS`, `REQUEST_TIMEOUT_SECONDS`,
`FORGE_FAIRNESS_ID_FRACTION/VALUE`, `CACHE_SHAPE` and `MAX_TOKENS_MODE`. The
authoritative list is `GROUP_KNOBS` in `run.sh`. The older per-group names
(`WORKERS_APP1`, `END_USERS_KEYS`, `APP2_DUTY`, `CACHE_SHAPE_END_USERS`,
`MAX_TOKENS_MODE_APP2`, ...) are now ordinary instances of this rule and work
as before. `CACHE_SHAPE` and `MAX_TOKENS_MODE` also gained a global form; it
is unset by default, so no group gets those shapes unless asked.

Built-in keys: `app1` -> `app1-production`, `app2` -> `app2-batch`,
`end-users` -> `end-user-alpha end-user-beta`, `custom` ->
`CUSTOM_SUBSCRIPTION_NAME` (required). Any other group defaults to a key
file with the group's own name (`/keys/app3`). When a group has several keys
they are round-robined across its workers, which is UNI-129 D1's end-users
model. Every key must collapse to the one group by the prefix rule. A missing
key file now **fails the run at start-up** with the file named, where it used
to show up as a column of 401s.

Examples:

```sh
# C1 shape: app1 short prompts / long outputs, app2 the reverse
PROMPT_WORDS_MIN_APP1=100 PROMPT_WORDS_MAX_APP1=200 MAX_TOKENS_DEFAULT_APP1=512 \
PROMPT_WORDS_MIN_APP2=3000 PROMPT_WORDS_MAX_APP2=3000 MAX_TOKENS_DEFAULT_APP2=16 \
  OPENSHIFT_TOKEN=... ./deploy/poc/15-fairness-benchmark.sh full-contention c1-shape

# C3/C5: only end-users streams and aborts; app1/app2 stay clean
STREAM_FRACTION_END_USERS=1 ABORT_FRACTION_END_USERS=0.2 ...

# six groups, app3 on two keys, app4 oversizes half its prompts, app5 joins at 10s
LOADGEN_GROUPS="app1 app2 end-users app3:16:app3-key-a,app3-key-b app4:16 app5:16" \
OVERSIZED_FRACTION_APP4=0.5 APP5_START=10 APP5_STOP=30 ...
```

**Through `15-fairness-benchmark.sh`.** The benchmark forwards
`LOADGEN_GROUPS` and, for every declared group, any `WORKERS_<TOKEN>`,
`<TOKEN>_KEYS`, `<TOKEN>_START/STOP/DUTY` and `<KNOB>_<TOKEN>` that is set in
its environment. For a group `04-loadgen.yaml` has no placeholder for, it
adds the env entry to the Job. Two caveats:

- **The scenario still owns the built-ins' worker counts.** Every scenario
  sets `WORKERS_APP1/APP2/END_USERS` through `PER_TENANT_OVERRIDES`. An env
  var beats an inline count, so in `LOADGEN_GROUPS="app1:6 ..."` run
  through a scenario, app1 still gets the scenario's count, not 6. The same
  goes for `WORKERS_APP1` etc. set in your shell: the scenario's value is
  used, the same as before this ticket. Inline counts take full effect only
  for `app3`+ groups (or when you run `run.sh` directly).
- Overrides are only forwarded for **declared** groups.
  `STREAM_FRACTION_APP9=1` with no `app9` in `LOADGEN_GROUPS` is quietly
  dropped. A misspelt knob name is also dropped quietly, because it is simply
  never looked up. Check the `load: UNI-179 group ...` lines (below) to
  confirm what each group actually resolved to.

**What the run logs.** The first five `load:` lines are unchanged for a
3-group run, because the report parses the first one. After them come one
`load: UNI-179 groups=[app1=12 app2=12 ...] total-workers=N` line, one
`load: UNI-179 group <name> token=... workers=... keys=[...] timeline=...
overrides=[...]` line per group (`overrides` lists only knobs that differ
from the global value, so a default run says `overrides=[]`), and
`load: UNI-179 dispatched N workers in Xs`. `15-fairness-report.py` reads the
`groups=` line to add `app3`..`appN` to its table rows and to the G2 ledger.
An `appN` that was offered load but has no client record therefore FAILs the
ledger instead of vanishing. `custom` is never added from that line, because
its fairness id belongs to its subscription, not to the literal name.

**Start barrier.** Every worker blocks on a FIFO until the dispatcher has
forked them all, then all of them read the same run clock and start
together. At 1000 workers in a CPU-limited pod, forking is slow enough that
early groups would otherwise get a head start, which looks exactly like
unfairness. Note that `<TOKEN>_START` still has 1-second resolution (the
integer `date +%s` clock, unchanged from UNI-127), so a group can start up to
about 1s before its nominal offset.

**For 6 and 20 groups on the GPU** the extra groups need real MaaS keys and
subscriptions for `app3`+. That provisioning belongs to
[UNI-165](/UNI/issues/UNI-165), not to this harness.

**The regression bar, and the evidence.** These were checked against a
host-side OpenAI-compatible stub, which logs each request's key, prompt
length and hash, `max_tokens`, `stream` and forged header. It is **not** the
llm-d simulator image: the agent host has no container runtime. For
pre-UNI-179 vs post-UNI-179 `run.sh` with no knobs set, the first five log
lines are byte-identical, every request was the same 1200-word prompt
(same hash) with `max_tokens: 64` and no stream, and `end-users` alternated
alpha/beta. The same holds with the legacy knobs set (`TENANTS` subset,
`WORKERS_*`, 3-key `END_USERS_KEYS`, `CACHE_SHAPE_APP1=hot`,
`MAX_TOKENS_MODE_END_USERS=huge`, global stream/abort/oversize/forge,
`APP1_DUTY`) and for a `custom` tenant: the shape mix and the start lines
matched. The pre-UNI-179 `15-fairness-report.py` parses all of these logs
identically to the new one, and the offline tests pass. N-group runs: 3
groups with per-group shapes (only the targeted group changed shape), 6
groups (2-key app3, oversize on app4 only, app5 inside its 10-30s window), and
20 groups x 50 workers = 960 workers. That last run dispatched in 0.32s, all
200s, and the 19 identically-sized groups landed within ±2.3% of each other
in requests sent. Full numbers are in the UNI-179 closing comment.

### N-group identities and EPP tables (UNI-187)

UNI-179 made the loadgen take any number of groups, but `app3`+ also need two
things on the cluster side. UNI-187 provides both, so the 6-group (UNI-165)
and 20-group (UNI-167) cases only have to run and measure.

**One name, four places.** For `appN` (N >= 3), the `MaaSSubscription` name,
the key file in `secret/maas-loadgen-keys`, the EPP `groups:` exact-match value
and the `LOADGEN_GROUPS` group name are all the bare string `appN`. The loadgen
maps a group with no built-in to `/keys/<group>`, and the EPP matches the
subscription name MaaS injects, so a single string leaves nothing to keep in
step. `app1`/`app2` keep their historical `app1-production`/`app2-batch`.

**Subscriptions.** `app3`..`app20` live in `deploy/maas/08-tenants.yaml` with the
label `maas-fair-share/tenant-set=n-group`. Apply only those:

```sh
oc apply -f deploy/maas/08-tenants.yaml -l maas-fair-share/tenant-set=n-group
```

A whole-file apply would also touch the Groups and the `MaaSAuthPolicy`, and
`poc-agent` can write neither. The same limit is why the owner group is the
existing `maas-poc-users` (already a subject of the AuthPolicy) and not a new
group per tenant: `poc-agent` can create `MaaSSubscription`s but not
`user.openshift.io` Groups. Each new subscription references both
`maas-vllm-gpu` and `maas-vllm-cpu`, so it can be smoke-tested off the GPU. The
four original subscriptions reference only the GPU model. Adding subscriptions
makes `maas-controller` regenerate `maas-trlp-maas-vllm-{gpu,cpu}`, which is a
live Kuadrant change, so apply with no benchmark running.

**Keys.** `deploy/maas/mint-loadgen-keys.sh app3 app4 ... app20` mints one key
per subscription into `secret/maas-loadgen-keys`, named after the subscription.
It skips names already present. The raw mint response stays in a 0600 temp
file and never reaches stdout, and only `id`/`name`/`subscription`/`expiresAt`
are printed. Record those, names only, in the key inventory above.

**EPP tables.** `deploy/poc/00-config.yaml` stays the 3-group default that
every case restores to. `deploy/poc/epp-groups/render.py` prints a copy of it
with only the `groups:` list swapped, so every other parameter matches the
default at the moment you render:

```sh
deploy/poc/epp-groups/render.py 6  --weights graded | oc apply -f -   # UNI-165
deploy/poc/epp-groups/render.py 20                  | oc apply -f -   # UNI-167
oc apply -f deploy/poc/00-config.yaml                                 # restore
deploy/poc/epp-groups/render.py --verify    # committed renders still match 00-config.yaml
```

The weight sets are `equal` (default), `graded` 40/20/15/10/10/5, `dominant`
90/2/2/2/2/2 and `pow2` 32/16/8/4/2/1. Only `equal` exists for 20 groups. The
equal renders for 6 and 20 groups are committed beside the script for review.
Between runs, one weight in a live table can be moved with the benchmark's
`epp-weight:<group>` target (UNI-180); its regex matches `name: app1,` exactly,
so it never also hits `app10`..`app19`. **Applying a table to `maas-epp-config`
recreates BOTH EPPs, because the CPU and GPU LLMISVCs read the same
ConfigMap,** and zeroes their per-group counters. So apply a table only from
the case that owns the GPU queue, before its run and never during one.

**Off-GPU smoke.** `deploy/poc/20-n-group-smoke.sh`, run as `poc-agent`:

1. Refuses to start if any Job in the namespace is active, or if any of
   `app3`..`app8` has no key.
2. Repoints only `maas-vllm-cpu`'s scheduler at its own `maas-epp-config-smoke`,
   which carries `app3`..`app8` at equal weight. It uses `app3`..`app8` because
   `app1-production`/`app2-batch` are not authorised on the CPU model.
3. Scales `maas-vllm-cpu` from 0 to 1 and runs a short `maas-loadgen-smoke` Job
   against `/maas-fairness-poc/maas-vllm-cpu`.
4. Quotes the `load: UNI-179` lines and passes only if every group has a
   configured weight and a non-zero `dispatch_total` delta, with zero
   `unclassified` dispatches and zero `unmatched_subscriptions_total` delta.
5. An exit trap restores the LLMISVC's `config.ref` and replica count and
   deletes the smoke ConfigMap and Job.

The GPU workers carry no taint, so the CPU pod (2 CPU / 8Gi request) may
schedule onto one. That is harmless with the pool idle and is the reason for
the active-Job check.

### Ledger cross-check (UNI-138)

G2 asks a different question from every other case above: not "does the
split match the configured weights," but "does the EPP's own accounting
agree with what the client actually sent and received." `15-fairness-
report.py` answers it with a `ledger` section -- additive, like the timeline
section above, with its own `ledger.verdict` that never touches the
top-level `verdict`.

Two things had to be added to make the comparison possible, both already
wired into `15-fairness-benchmark.sh`:

- `snapshot_metrics()` now also captures `llm_d_epp_request_(input|output|
  cached)_tokens_(sum|count)` -- the EPP's core, per-request token
  histograms, `fairness_id`-labelled but owned by the framework, not the
  fairness plugin (`pkg/fairness/weightedlas/metrics.go`'s own comment says
  not to duplicate them). These are observed only from a real response
  `Usage` block, never from the plugin's dispatch-time estimate, and are
  **not** contention-gated -- the most direct check against the client's raw
  totals. Before this ticket they were invisible to every report; a snapshot
  taken by the pre-UNI-138 script still works, it just produces a report
  with no `ledger` section (same "omit the flag, get the old shape" contract
  as `--metrics-timeseries`).
- The cost-model weights (`inputTokenWeight`/`outputTokenWeight`/
  `cachedInputTokenWeight`) are read live from the `maas-epp-config`
  ConfigMap and passed to the report as `--input-token-weight`/
  `--output-token-weight`/`--cached-input-token-weight`. No metric exposes
  these, and `contended_service_tokens_total` is denominated in that cost
  unit, not raw tokens -- comparing it to raw client tokens directly would
  read a deliberate cost-model choice (`outputTokenWeight: 2.0` live) as a
  bug.

Pass `--client-record-jsonl` (`15-fairness-benchmark.sh` always does, using
the `client-request-summary.jsonl` the UNI-128 mechanism already produces)
to get the section; omit it for the pre-UNI-138 report shape.
`--ledger-tolerance-pct` (default 10, same default `15-fairness-benchmark.sh`
sets via `LEDGER_TOLERANCE_PCT`) is the max absolute percent difference
allowed, per tenant, on either of two checks:

1. **Raw tokens**: EPP's `llm_d_epp_request_input_tokens_sum` +
   `_output_tokens_sum` delta vs. the client's `prompt_tokens_total` +
   `completion_tokens_total`. Both sides read the same real usage-block
   values through independent code paths, so this should track to within
   rounding **for an all-non-streaming run**; a real divergence here means a
   regression (a model server missing `--enable-force-include-usage`, or the
   two accounting paths drifting out of sync).

   **Does not hold if any tenant in the run streams.** [UNI-186](/UNI/issues/UNI-186)
   confirmed live against `maas-vllm-gpu` that `--enable-force-include-usage`
   makes vLLM emit a real, non-null, cumulatively-growing `usage` block on
   *every* SSE chunk of a streamed response rather than only the final one;
   the EPP observes each chunk's value, so the raw sum for a streaming
   tenant inflates by roughly its chunk count (~58x on the UNI-147
   full-contention benchmark). Expect this check to FAIL for a streaming
   tenant regardless of regression status, and do not raise
   `--ledger-tolerance-pct` to paper over it — the **cost** check below is
   unaffected and is the one that should gate `ledger.verdict` for a
   streaming scenario.
2. **Cost**: EPP's `contended_service_tokens_total` delta vs. the client's
   prompt/completion totals run through the live cost formula (the client
   has no way to see cache hits, so the EPP's own measured
   `_cached_tokens_sum` delta stands in for that term). Only meaningful for a
   scenario shaped like full contention for (almost) the whole run, since
   the gate and the client's whole-run total are treated as covering the
   same set of requests.

   **Expect this check to FAIL for a tenant sending context-length-rejected
   (oversized) prompts.** [UNI-148](/UNI/issues/UNI-148) found that a request
   the backend never usefully answers still gets charged: `PreRequest`
   books a provisional estimate from the request's own (here, huge) size at
   dispatch, and if no usage block ever arrives, `ResponseBody`'s no-usage
   branch (`plugin.go:576-594`) makes that estimate the permanent cost by
   design -- there is no "the backend rejected this, refund it" path. On the
   UNI-148 run this meant ~13,238 cost-units charged per rejected request
   (~9-10x a normal served request) against zero client-recorded tokens, an
   infinite percent deviation. This is a real, reproducible ledger gap, not
   a cost-model nuance like the streaming one above -- see
   `docs/poc-results.md`'s UNI-148 section and the policy question filed as
   [UNI-190](/UNI/issues/UNI-190).

**Picking X=10%, from the live full-contention run:** raw tokens agreed to
within 0.05% across all three tenants; the cost check carried a real,
explained, persistent bias of -3.9% to -4.0% for the two lower-request-count
tenants and -0.66% for the highest-volume one -- not the ticket's suspected
"4-bytes-per-token estimate" (ruled out directly:
`requests_without_usage_total` stayed at flat zero for the whole run, so no
completed request was ever left on its dispatch-time estimate), but the
contention gate's own startup transient: `isContended` only turns true once
the EPP has observed the first cross-group backlog overlap, and the
requests dispatched before that moment are real, fully measured, and
correctly excluded from the gated cost counter by design, while still
counted in a whole-run client total. That fixed-size startup window is a
much bigger fraction of a low-volume tenant's total than a high-volume one's
-- see `docs/poc-results.md`'s UNI-138 section for the full numbers and
reasoning. 10% was picked to clear that explained bias with ~2.5x margin
while still being tight enough to catch a real regression on the raw-token
check.

Only validated for full-contention; do not wire `--client-record-jsonl` into
a `solo`/`capped`/demand-light/UNCONTENDED scenario without first re-deriving
the cost-check formula for a run where the contended fraction is not close
to 1.0.

### Shed rate, EPP pick latency, and alert fire/clear (UNI-181)

Three more additive report sections, for E3/E4 (UNI-157/158), H2/H3
(UNI-168/167) and G1 (UNI-166). None of them touches `verdict`, `groups` or
`sources`; a report built from the same inputs as before UNI-181 has
byte-identical values in every pre-existing field (checked by rebuilding all
54 committed `results/` runs with the old and new script). Each section
always says which kind of empty it is: **never happened** (a measured
zero) vs **not recorded** (unknown).

**`shed`** -- always present; no new flag. Per offered group: client-observed
429 and 503 counts from the loadgen status tally, shed rate, the group's
weight share over offered groups, its share of everything shed, and shed
share / weight share (above 1 = lost more of the shed than its weight). No
PASS/FAIL: E3 and E4 judge it. A group with no 429/503 reads
`0 (never shed)`; a group missing from the loadgen table reads `not recorded`.
Per-group shed is client-side because the live EPP has no
`fairness_id`-labelled shed counter: `llm_d_epp_flow_control_requests_total`
has `outcome` but not `fairness_id`, and the per-`fairness_id`
`flow_control_request_queue_duration_seconds` histogram in the v0.11.0
source was absent from the live full scrape (uni140 soak). When that
pool-wide counter is in the snapshots, the section adds the EPP's own shed
total and splits the client's 429s: at most `RejectedCapacity + EvictedTTL`
came from the EPP, so the rest came from elsewhere (Kuadrant, for E4).

**`pick_latency`** -- p50/p99 over the run (after minus before, per bucket)
of `llm_d_epp_scheduler_e2e_duration_seconds` (the scheduler's own
per-request pick) and `llm_d_epp_flow_control_dispatch_cycle_duration_seconds`
(one flow-control dispatch cycle, where the weighted-LAS policy runs). Both
are unlabelled. States: `ok`, `no_observations` (captured, count did not
move), `not_recorded` (absent from both snapshots).

- `--pick-latency-baseline <fairness-report.json>`: express p50/p99 as a
  ratio of another run's (use the 3-group full-contention run).
- **Resolution caveat for H3:** buckets are 0.1/0.2/0.5/1/2/5/10/20/50/100 ms.
  On the live uni140 soak both p50 and p99 fell inside the first bucket,
  (0, 0.1 ms], so the printed 0.050/0.099 ms are interpolation, not
  measurement. Read the bucket columns. A p99 above 100 ms prints as
  `>= 100ms (above top bucket)`.
- **Not captured by the benchmark yet.** `15-fairness-benchmark.sh`'s
  `snapshot_metrics()` grep does not include either histogram (or
  `flow_control_requests_total`), so today every benchmark report shows them
  `not recorded`. Widening that grep is a separate change that needs a
  sim-backend regression run.

**`alerts`** -- needs an export, because nothing reads alert state live:
`maas-fairness-alerts` was not applied to the cluster as of 2026-11-02
(UNI-130, re-checked for UNI-181; UNI-49 owns the rule).

- `--alerts-json <file>`: a Prometheus `/api/v1/query_range` result for
  `ALERTS{alertname=~"MaasFairness.*"}` covering the run, either the raw
  response or `{"result": [...], "end": <epoch>, "step_seconds": <s>,
  "query": "..."}`. Omit it and the report says alert state is **unknown**,
  not "none fired".
- `--alert-rules deploy/prometheusrule.yaml`: every alert in the file gets
  a row, so one that never appears in the export reads `never fired`.
- `--alerts-step-seconds` (default 30): the query step, unless the file
  carries `step_seconds`. Samples more than 1.5 steps apart start a new
  episode. An episode clears one step after its last sample. An episode
  whose last sample is the end of the export reads
  `still active at export end` and has no clear time. Times are seconds from
  `--run-start`. An episode that started after `--run-end` is flagged.

---

### Live enforce flip, and unconditional cleanup (UNI-174)

Before this ticket, moving `maas-epp-config`'s `enforce` key from `false` to
`true` for an enforce-mode run was a manual `oc` step the operator did around
`15-fairness-benchmark.sh` (see `docs/poc-results.md`'s "Reproduce:"
paragraph) -- the script only read whatever state it found, for the report's
`--enforce` label. Nothing reverted that edit if the run died first, and a
dead run with enforce stuck `true` makes every subsequent shadow-mode
measurement meaningless until someone notices and flips it back by hand --
exactly what blocked [UNI-143](/UNI/issues/UNI-143)'s first two recovery
attempts.

**Mechanism chosen: a flag plus one trap, inside `15-fairness-benchmark.sh`
itself, not a separate flip/revert wrapper script.** `ENFORCE_LIVE=true`
makes the script patch the ConfigMap, wait for both EPPs to confirm
`llm_d_epp_maas_fairness_enforcing=1`, and revert it through the same
`on_exit` function that already restores the chaos-scale replica count
(UNI-127) and kills the background capture/timeseries/chaos loops. One
trap owning every piece of this run's live cluster state was preferred over
a second script with its own trap: two traps racing to own the same
ConfigMap on the same crash is a new way to get this wrong, not a
simplification. Default (`ENFORCE_LIVE` unset) is unchanged from before this
ticket -- a plain invocation only observes.

**Why both EPPs:** `deploy/poc/09-vllm-gpu.yaml` and `deploy/poc/07-vllm-cpu.yaml`
both point `scheduler.config.ref` at the same `{name: maas-epp-config, key:
epp}` (`docs/design.md` "the KServe controller watches ConfigMaps ...
re-resolves `scheduler.config.ref`... and rolls the pod automatically" --
same section as "Turn on the V(4) per-request tier" above). One ConfigMap
edit reaches both `maas-vllm-gpu-kserve-router-scheduler-*` and
`maas-vllm-cpu-kserve-router-scheduler-*`, and both roll themselves
automatically -- no manual pod restart, same as that section documents.
Verify the flip (and the revert) against
`llm_d_epp_maas_fairness_enforcing` on **both** EPPs' `/metrics`
(`maas-vllm-gpu-epp-service` and `maas-vllm-cpu-epp-service`,
`maas-epp-metrics-reader-token` as the bearer), never against the ConfigMap
alone -- the ConfigMap says what was requested, the metric says what is
actually in force, and nothing mounts this ConfigMap as a volume or env var
for a process restart to prove the point instead.

**What the trap covers, and what it cannot:** `on_exit` is registered on
`EXIT INT TERM HUP` before the first cluster-mutating call in the script, and
is never unregistered (`trap - EXIT` doesn't appear in this script anymore --
removing it was half of this fix) -- the only way it skips is **SIGKILL
(`-9`)**, which no process, trapped or not, can catch, and an unattended OOM
kill behaves identically. Both leave `enforce: true` live with nothing to
revert it automatically; after either, confirm and flip back by hand the
same way this ticket describes under "Reproduce:" in `docs/poc-results.md`,
then re-check `llm_d_epp_maas_fairness_enforcing=0` on both EPPs before
starting the next run.

**A run that didn't cause the enabled state doesn't revert it.** If
`ENFORCE_LIVE=true` finds `enforce` already `true` when it starts, it does
not flip anything and will not touch it on exit -- only a flip this run
itself performed is this run's obligation to undo.

**Kill-test evidence (2026-11-02):** ran `ENFORCE_LIVE=true DURATION=180
15-fairness-benchmark.sh app1-alone`, let it flip and confirm, then
`kill -TERM` the script mid-run (while `maas-loadgen` was actively
`Running`), with `llm_d_epp_maas_fairness_enforcing` read independently via
`curl` at each step (not taken from the script's own log):

| when | gpu | cpu | timestamp (UTC) |
|---|---|---|---|
| before the flip | 0 | 0 | 2026-11-02T09:53:08Z |
| during the run (enforcing) | 1 | 1 | 2026-11-02T09:54:50Z |
| after `kill -TERM` (self-reverted) | 0 | 0 | 2026-11-02T09:56:30Z |

`kill -TERM` was sent at 09:54:50Z; the script's own `enforce-events.log`
shows it logged the safety-net revert immediately and confirmed
`enforcing=0` on both EPPs at 09:56:13Z (the gap is the ConfigMap-triggered
pod roll taking ~80s for both EPPs, not a delay in the revert being
*issued*) -- consistent with the independent reading above. An earlier
attempt at this same test exposed a real bug in the first cut of this
mechanism: trapping `INT TERM HUP` with a handler that doesn't itself call
`exit` runs the cleanup correctly but then lets bash resume the rest of the
script instead of terminating (confirmed live -- the script kept polling the
Job for a full minute after the signal). The fix is the separate `trap 'exit
1' INT TERM HUP` now in all three scripts that register one of these traps;
see the comment next to it in each script.

---

### Generic live-config set/restore wrapper (UNI-180)

ENFORCE_LIVE, CHAOS_EPP_DELETE_AT and CHAOS_SCALE_AT (above) were three
hand-rolled patch/compare/revert pairs, each touching the same ConfigMap and
the same `on_exit` trap. The edge-case board needs more of these: weights and
`newcomerClamp` ([UNI-158](/UNI/issues/UNI-158), [UNI-159](/UNI/issues/UNI-159)),
a Kuadrant `TokenRateLimitPolicy` ([UNI-160](/UNI/issues/UNI-160),
[UNI-162](/UNI/issues/UNI-162)), and a generic "patch something at t+N and
observe whether it applies without a restart" hook
([UNI-163](/UNI/issues/UNI-163), F6). Three more bespoke pairs was the most
likely way one of them leaves the cluster dirty, so `15-fairness-benchmark.sh`
now has one mechanism underneath all of it: `live_config_set`/
`live_config_restore`. **This ticket is the harness work alone** — it does not
itself run or score any of the cases above, same scope boundary as UNI-127/
UNI-128/UNI-129.

**Target specs.** A target is a string naming WHAT to change:

| Spec | Meaning | Used by |
|---|---|---|
| `epp-key:<key>` | A scalar key in `maas-epp-config`'s `data.epp` (e.g. `enforce`, `newcomerClamp`, `halfLifeSeconds`) | ENFORCE_LIVE |
| `epp-weight:<group>` | That group's `weight:` in the same file's `groups:` list (`app1`, `app2`, `end-users`), or `defaultGroup` for `unclassified` | future: UNI-158 |
| `field:<resource>:<name>:<dotted-path>` | A JSON field on any named namespaced resource, applied via `oc patch --type=merge` (e.g. `field:llmisvc:maas-vllm-gpu:spec.replicas`, or a `TokenRateLimitPolicy`'s `spec.limits.<name>.rates`) | CHAOS_SCALE_AT; future: UNI-160/162 |

`live_config_set <id> <spec> <new-value>` reads the target's CURRENT scalar
value (never a whole resource body, so before/applied/current are always
comparable like-for-like), writes it to
`results/<run>/live-config/<id>.before`, applies the change, and records what
it applied to `<id>.applied`. `live_config_restore <id>` re-reads the live
value: if it still equals what this wrapper applied, it patches the `before`
value back; if not (an earlier restore — explicit call, a held `field:`
target's own chaos-loop restore, or the `on_exit` trap — already happened),
it is a no-op. Either way it writes `<id>.post-restore.yaml`
(`oc get <resource> -o yaml`) — the proof the edge-case series' "leave the
cluster as you found it" rule asks for, so a case's closing comment can cite
a file instead of re-deriving the state by hand.

**Why files, not bash variables, for this state.** CHAOS_SCALE_AT and the new
LIVE_SET_AT (below) fire from the `chaos_loop` background subshell
(`chaos_loop &`), and a subshell's variables never make it back to the parent
shell that runs the `on_exit` trap — but its writes to `$ARTIFACT_DIR` do. The
same idempotency check `live_config_restore` uses (re-read the live value,
compare to what was applied) is exactly the "query, don't trust a flag"
pattern the pre-UNI-180 `revert_enforce_live`/`restore_chaos_scale` already
used for the same reason; this ticket generalizes that pattern instead of
replacing it.

**ENFORCE_LIVE and CHAOS_SCALE_AT are unchanged from the outside.** Both env
vars keep their names and semantics; internally they now call
`live_config_set`/`live_config_restore` with `epp-key:enforce` and
`field:llmisvc:$LLMISVC_NAME:spec.replicas` respectively. CHAOS_EPP_DELETE_AT
is untouched — a pod delete has no value to restore, so it does not fit the
set/restore shape and stays its own one-shot `oc delete pod`.

**The new generic hook:**

| Var | Meaning |
|---|---|
| `LIVE_SET_AT` | Seconds-offset to apply `LIVE_SET_TARGET`/`LIVE_SET_VALUE` (same `"120s"` or bare `120` shorthand as the chaos hooks). Unset (default): fires nothing. |
| `LIVE_SET_TARGET` | A target spec, as above. |
| `LIVE_SET_VALUE` | The new value — a bare scalar for `epp-key:`/`epp-weight:`; for `field:`, tried as JSON first (so `1`, `"a-string"`, `[{"a":1}]` all work) and used literally if that fails. |
| `LIVE_SET_HOLD` | Optional seconds-offset AFTER `LIVE_SET_AT` to restore at, like `CHAOS_SCALE_HOLD`. |

All four are unset by default, so a plain invocation of any existing scenario
is unaffected — this is the regression bar this ticket has to clear, not a
suggestion.

**LIVE_SET_HOLD is only honored for a `field:` target.** An `epp-key:`/
`epp-weight:` target recreates the EPP pod on restore, exactly like
ENFORCE_LIVE's own revert does (see "Live enforce flip" above) — restoring
one WHILE the Job is still running would zero the run's fairness counters
*mid-measurement* instead of just starting a fresh run at zero, which is
strictly worse than the hazard UNI-143 (B4) already found for ENFORCE_LIVE.
So that kind always waits for the same post-metrics-after point
`revert_enforce_live` uses, `LIVE_SET_HOLD` or not; the script logs this
explicitly at startup (`LIVE_SET_HOLD is ignored for an epp-key/epp-weight
target`) rather than silently doing something different from what was asked.
A `field:` target (e.g. a mid-run LLMISVC field, not metrics-bearing) restores
at `LIVE_SET_AT + LIVE_SET_HOLD` from inside the chaos loop, same timing as
CHAOS_SCALE_AT/CHAOS_SCALE_HOLD.

**Recorded on the timeline the same way the chaos events are.** `live_set`/
`live_restore` entries land in `timeline-config.json`'s `chaos_events` list
next to `epp_delete`/`scale_down`/`scale_restore`, each with the same generic
`at_seconds` key. `15-fairness-report.py`'s phase-edge maths
(`compute_phase_edges`) only ever reads that one key — it needed no change
for this ticket, and the markdown render already lists any event's extra
fields (`target`, `value`) generically.

**Known gap, not claimed as solved.** If `LIVE_SET_TARGET` is an
`epp-key:`/`epp-weight:` target, applying it mid-run recreates the EPP pod
exactly like ENFORCE_LIVE's flip does at run start — but ENFORCE_LIVE's call
site re-resolves `$EPP_POD` (and re-points the log-capture loop and the
restart detector at it) immediately afterward, in the SAME process, before
the Job starts. A `LIVE_SET_AT` firing *during* the run does this from the
`chaos_loop` background subshell, which cannot update `$EPP_POD` in the
parent process's (or the capture loop's own, separately-forked) view — so the
log-capture loop keeps following the OLD pod name, which the EPP delete chaos
hook already documents as a known limitation (UNI-127's note above), not
something this ticket silently fixes. F6 (UNI-163) needs to either accept
that gap, target a `field:` resource instead, or close it itself.

**Verified (2026-11-02), without a GPU or a loadgen Job.** Rule 1 of this
ticket's own harness-set context forbids applying `04-loadgen.yaml`, and a
real edge-case-chain GPU benchmark (`TENANTS="app1 end-users"`,
`ENFORCE_LIVE=true`) happened to be running against this same cluster for
part of this work, which made it doubly off-limits (applying
`04-loadgen.yaml` would have deleted that run's `maas-loadgen` Job — the name
is not scenario-qualified). Two separate things were verified instead, both
without touching `04-loadgen.yaml`:

*Set/restore/trap mechanics*, against the real cluster's already-live
resources (no new provisioning) via a standalone driver script that sourced
the wrapper functions directly out of `15-fairness-benchmark.sh`:

- `field:llmisvc:maas-vllm-cpu:spec.replicas` (CPU LLMISVC was already idle at
  0 replicas, so this touches nothing GPU-serving) — set 0→1, confirmed live,
  then `kill -TERM` the driver mid-hold to prove the `EXIT`/`TERM` trap
  restores it to 0 without an explicit restore call.
- `epp-key:newcomerClamp` — set `true`→`false`, confirmed live, explicit
  restore, confirmed back to `true` via `oc get configmap maas-epp-config -o
  yaml`.
- `epp-weight:app2` — set `10`→`11`, confirmed live, explicit restore,
  confirmed back to `10` the same way.

This caught a real bug before it reached anyone: the first cut of
`extract_epp_key`/`extract_epp_weight` piped the ConfigMap's text into
`python3 -I - "$key" << 'PYEOF'` and had the script read it via
`sys.stdin.read()`. That pipe and that heredoc both target the SAME fd —
the heredoc wins, so python's own script source consumes it and
`sys.stdin.read()` inside the script sees EOF, never the piped ConfigMap
text. The live symptom: `extract_epp_key newcomerClamp` reported "key not
found" for a key that was plainly present, and worse, `live_config_restore`'s
idempotency check read that failure as an already-empty "current" value,
concluded nothing needed reverting, and left `newcomerClamp` stuck at `false`
on the real cluster instead of restoring it to `true`. Fixed by writing the
ConfigMap text to a file and passing the file path as an argv argument
instead (the same pattern `patch_configmap_epp` already used) — never piping
into a command that also has a heredoc attached to its stdin. The cluster was
restored by hand (`live_config_apply "epp-key:newcomerClamp" "true"`, the
corrected code path) and the fixed version was re-verified end to end before
moving on; see the restore function's own comment for the detail. The sim
backend (`deploy/poc/01-sim-backend.yaml` + `02-epp.yaml`) was NOT used for
this verification: it is not currently deployed, and `02-epp.yaml` provisions
a `ClusterRoleBinding`, which rule 6 of this ticket's context forbids
provisioning fresh. The EPP ConfigMap is shared across every backend (GPU,
CPU, and the sim's own `maas-epp` Deployment alike — see
`deploy/poc/02-epp.yaml`'s header comment), so the `epp-key`/`epp-weight`
mechanism verified above against the already-live GPU/CPU EPPs is the same
mechanism a sim-backed run would exercise; only the pod-recreation path
(KServe-managed roll vs. a plain Deployment with no live-reload) differs, and
that distinction is exactly the "known gap" two paragraphs up.

*Rule 4 regression (default behaviour unchanged)*, done entirely offline with
no `oc` calls at all, since no Job could safely be applied while the chain's
GPU run was in flight: both `origin/main`'s pre-UNI-180
`15-fairness-benchmark.sh` and this branch's version were each truncated
right before their first `$OC` call (the same technique UNI-179 used in
`artifacts/uni-179/bench/bench-trunc.sh`), then run for all twelve scenarios
with no extra env vars against the same, unmodified `04-loadgen.yaml`. Every
scenario's patched manifest (`04-loadgen.patched.yaml`) and
`timeline-config.json` came out byte-identical between the two versions —
the default behaviour this ticket must not change literally produces the
same bytes, not just "the same shape." `LIVE_SET_AT`/`TARGET`/`VALUE`/`HOLD`
were also exercised through the same offline harness: confirmed a
`field:`-kind target restores at `AT + HOLD` while an `epp-key:`-kind target
ignores `HOLD` and restores at `DURATION` instead (per the hazard rule
above), and confirmed both FATAL validation branches (`LIVE_SET_AT` without
a target/value, and a target/value without `LIVE_SET_AT`) actually fire.

---

### Shadow-mode control, F1 (UNI-159)

The edge-case plan's second named negative control (the first is
`equal-workers-control`, UNI-103): run `full-contention`'s own proven sizing
(`TENANTS="app1 app2 end-users"`, `WORKERS_APP1=32 WORKERS_APP2=32
WORKERS_END_USERS=128`) with `maas-epp-config`'s `enforce` key flipped to
`false` for the whole run instead of its live `true`. In shadow mode the
plugin still observes and accounts every request (the
`llm_d_epp_maas_fairness_*` counters still move) but never reorders the
queue by weight, so a correct implementation should show the same
work-conservation compression toward equal thirds that `equal-workers-control`
shows for a different reason (under-offered load there; no enforcement here).

```sh
OPENSHIFT_TOKEN=... ./deploy/poc/15-fairness-benchmark.sh shadow-mode-control
```

No extra env vars are needed or should be passed — the scenario's own
case-statement branch sets `SHADOW_MODE="true"` (and `IS_CONTROL="true"`)
itself, exactly as the ticket asks ("add it to the benchmark as a scenario
that sets and restores the mode itself").

**`SHADOW_MODE`, the mirror of `ENFORCE_LIVE`.** UNI-174's `ENFORCE_LIVE` only
ever confirms and flips TOWARD `enforce=true` (`wait_for_enforcing("1")`) —
it has no notion of flipping the other way, and generalizing its boolean to
mean "whatever direction the live value isn't" would have made every existing
`ENFORCE_LIVE=true` invocation (UNI-151/156/157/158, this chain's own prior
tickets) silently context-dependent on whatever `enforce` happened to be live
at the time, instead of the explicit "make it true" it is documented and
relied on to mean. `SHADOW_MODE="${SHADOW_MODE:-false}"` is a separate,
explicit boolean instead, built on the same UNI-180 `live_config_set`/
`live_config_restore` wrapper ENFORCE_LIVE itself now sits on:

- Already `false`: logs `enforce already false in maas-epp-config -- nothing
  to flip; this run will NOT revert it on exit` and leaves `SHADOW_FLIPPED`
  unset — same "did this run actually cause the state" guard `ENFORCE_LIVE`
  uses, so a run that happens to start during someone else's shadow-mode
  window doesn't clobber it on exit.
- Otherwise: `live_config_set shadow-mode "epp-key:enforce" "false"`, confirms
  `llm_d_epp_maas_fairness_enforcing=0` on both EPPs (GPU and CPU share the
  one ConfigMap — see the UNI-174 section above) via the same
  `wait_for_enforcing` helper, FATALs before the Job ever starts if that
  timed out, and re-resolves `$EPP_POD`/`$EPP_IMAGE_DIGEST`/`$START_RESTARTS`
  afterward — same no-live-reload, pod-gets-recreated mechanism UNI-174's own
  flip has, so the log-capture loop and the mid-run restart detector don't
  silently end up watching a pod that is already gone.
- Reverts at the exact same point `revert_enforce_live` does — AFTER the
  after-snapshot, not before, for the identical reason (a ConfigMap edit
  recreates the EPP pod and zeroes its Prometheus registry; reverting earlier
  would silently zero every `contended_*`/`dispatch_total` series this run's
  own report depends on). `on_exit`'s trap calls it unconditionally as a
  backstop, same shape as `revert_enforce_live`/`restore_live_set`.

**`ENFORCE_LIVE=true` and `SHADOW_MODE=true` together are a hard FATAL**,
checked right after the scenario's case statement runs (so a scenario that
sets one of them itself, like `shadow-mode-control`, is still caught if an
operator also passes the other by hand): both target the one `enforce` key in
opposite directions, and there is no combined outcome to converge on.

**Verified (2026-11-06), via the same offline technique UNI-180 used**: both
`origin/main`'s pre-UNI-159 `15-fairness-benchmark.sh` and this branch's
version, each truncated right before their first `$OC` call, produced
byte-identical patched manifests and `timeline-config.json` for every
existing scenario with no extra env vars — `shadow-mode-control` is additive,
not a behaviour change to anything before it. The FATAL branch for
`ENFORCE_LIVE=true SHADOW_MODE=true` together was exercised the same way and
confirmed to fire before any `$OC` call.

---

### Per-tenant TTFT/ITL and the SPLIT-FAIL / PRIORITY-OK secondary verdict (UNI-226)

A share-split FAIL used to be reported as a bare failure with no record of
whether the policy was nonetheless doing the right thing — see UNI-103's
`equal-workers-control`, where app1/app2/end-users' end-to-end latencies
(7.5s/7.4s/5.9s) showed correct prioritisation underneath a split that missed
its target badly. This section covers the fix: per-tenant TTFT/ITL, scored as
a second, independent verdict.

**Source metrics — no client-side instrumentation needed.** The deployed
`llm-d-router` EPP already emits both, `fairness_id`-labelled, from its own
framework code (not this repo's): `llm_d_epp_request_ttft_seconds_bucket`
(every request, streaming or not — non-streaming TTFT equals total duration)
and `llm_d_epp_request_streaming_itl_seconds_bucket` (streaming requests
only). Both were already listed in the metrics catalog table above, just
never wired into a report or a verdict before this ticket.

**GuideLLM was evaluated and rejected for this ask.** The board asked for it
(2026-11-10) as the load generator, on the reasoning that it reports
TTFT/ITL per customer. It does, but only for traffic it generates itself,
and the EPP's own histograms already give the same numbers, natively
`fairness_id`-labelled, measured at the actual enforcement point rather than
a separate client process — no per-tenant aggregation problem to solve, no
new air-gap dependency (GuideLLM + its dependency tree would have been a
third blocker alongside the private Quay image and the `hf://` model URI),
and no need to reconcile a second client-record schema against the G2
ledger. GuideLLM may still be the right choice later for UNI-221's
rate-based open-loop generation; it is not used anywhere in this ticket's
implementation. The existing `deploy/poc/04-loadgen.yaml` closed-loop
generator (per-group `STREAM_FRACTION`) is what every run in this section
used.

**Streaming fraction for scored runs: 100%, identical across every offered
group.** TTFT is only observable on streamed requests, and a fraction that
differs by group would make the comparison meaningless. Confirmed
accounting-safe under UNI-186's "58x inflation" finding: that finding is in
the framework's raw per-chunk token counters
(`llm_d_epp_request_{input,output}_tokens_sum`), which feed the G2 ledger's
informational raw-tokens cross-check only (already documented above as an
expected-FAIL-under-streaming, non-gating check). The fairness plugin's own
cost settlement is gated on `response.EndOfStream` — it books cost once,
from the final cumulative usage block — so `contended_service_tokens_total`,
what every share verdict in this doc is actually scored on, is unaffected by
turning streaming on.

**The secondary verdict's gate is "no rank inversion between distinctly-weighted
groups," not raw Spearman correlation == 1.0.** The board's literal phrasing
asked for rank correlation, but a genuine weight tie (e.g. `98/1/1`'s
`app2 == end-users`) makes exact correlation 1.0 unreachable by construction
even when the ordering is otherwise perfect — confirmed numerically (a
correctly-ordered `98/1/1` run scores correlation 0.87, not 1.0, purely
because of the tie). The report still shows raw correlation for reference,
but the gate is: the top-weighted group's TTFT p50 and p95 are both strictly
the lowest among distinctly-weighted groups, and no two distinctly-weighted
groups are inverted relative to their weight order. This reduces to
correlation == 1.0 whenever every weight in the row is distinct (every row
in the suite except `98/1/1`-style ties), so it is a generalization, not a
loosening.

**ITL is expected to be flat, by construction.** Once a request is
dispatched, vLLM decodes the whole resident batch in lockstep — every
sequence advances one token per step — so the EPP has no influence after
dispatch. Confirmed on every run in this section: ITL p50/p95 sit at
14-16ms/35-39ms for every tenant regardless of weight, including the
`98/1/1` row where TTFT differs by 55 seconds between app1 and the other two.
Do not read flat ITL as a prioritisation failure; it is the predicted,
correct result. TTFT is the metric this verdict is built on.

**The noise floor is a same-run, between-tenant control, not a same-config
repeat.** The margin the `98/1/1` row is scored against is between-tenant
drift *within one run* — two tenants sharing a batch, a replica set and a
scrape window have correlated errors a separate repeat run can't see, even
with tight run-to-run reproducibility. The control actually used: the
`98/1/1` row's own sizing (`full-contention-2x-discriminating`'s 256/256/256
equal workers, `STREAM_FRACTION=1`, `DURATION=240`), weights patched to
equal (1/1/1) via `deploy/poc/24-patch-all-weights.sh`, same replica pool,
same tenant set, only the weights differ. Result
(`results/20261110T224209Z-uni226-equal-weight-equal-load-noise-floor/`):

| group | TTFT p50 | TTFT p95 |
|---|---|---|
| app1 | 36267ms | 54032ms |
| app2 | 36141ms | 53563ms |
| end-users | 36100ms | 53540ms |

Max between-tenant gap: **167ms p50 / 492ms p95**. Share verdict PASS,
correctly flagged NON-DISCRIMINATING (0.0pt worker-vs-weight gap) — this row
is a control and is never scored on share.

**`98/1/1` under equal load is a named, scored prioritisation row, not a
skip.** The share target is genuinely unreachable (app1 can't absorb 98% of
throughput from a third of the concurrency), but that extremity makes this
the sharpest prioritisation test in the suite: if the policy can't produce
an obvious ordering here, it can't anywhere. It had only ever run at
`full-contention-2x`'s unequal 64/64/256 sizing before this ticket; the
equal 256/256/256 sizing (`full-contention-2x-discriminating`'s own default)
is the one used for this row, same as the noise floor. Weights patched with
`24-patch-all-weights.sh 98 1 1`.

**Result** (`results/20261110T231158Z-uni226-98-1-1-equal-load-priority-v2/`;
`ENFORCE_LIVE=true` is required for this — see the operational note below):

- Primary (share): **FAIL**, as predicted — app1 delivered 61.8% against its
  98% target (-36.2pt), still far above its 33.3% worker share, i.e. the
  policy visibly pulled share toward app1 without reaching the structurally
  unreachable target. Reported, not scored as a policy defect.
- Secondary (priority): **PRIORITY-OK**. app1 TTFT p50 14459ms / p95
  39258ms, strictly lowest of the three; app2 and app3(end-users) both
  ~70000ms/~118000ms (consistent with their tied weight). Separation from
  the next distinctly-weighted group: **55381ms** — roughly 330x the noise
  floor's p50 gap and 110x its p95 gap, not a hair's width.
- Shedding was negligible (1/3086 requests on app1, a single transient 503;
  app2/end-users shed zero) — the board's prediction that low-weight
  tenants would be pushed back far enough to hit the 300s flow-control TTL
  did not materialize at this `DURATION=240`. Not investigated further:
  the prioritisation signal was already unambiguous without it.

**Pool-level cross-check against vLLM's own `vllm:time_to_first_token_seconds`
(2026-11-10, against live Prometheus via the Grafana anonymous-Viewer
proxy — see "Find a run on the fairness dashboard" above for why that path
and not a direct Thanos route):** pool EPP-side TTFT was p50 17189ms / p95
109758ms over the same run window; vLLM's own pool-level histogram gave p50
6.42s / p95 19.29s. The EPP number is larger in both quantiles, as expected:
EPP TTFT measures from request arrival at the EPP (including its own
admission-hold queueing, where the weighted-fairness policy actually acts)
to first byte, while vLLM's own metric is engine-internal prefill time
after dispatch. A smaller vLLM number confirms the gap is admission-hold
time, not gateway buffering or some other unaccounted overhead — the
client/EPP-side TTFT this verdict is built on is measuring real policy
behaviour.

**Operational note: `ENFORCE_LIVE` defaults to `false`.** The first `98/1/1`
attempt under this ticket was run without `ENFORCE_LIVE=true` after an
unrelated `PATH` fix, and came back with flat TTFT across all three groups
and secondary verdict `PRIORITY-FAIL` — a dramatic-looking negative result
that was actually just the fairness plugin never gating anything (shadow
mode is the cluster's standing default; see "Shadow-mode control" above).
That run is not part of the results above and was not scored. Always check
the report's own `Enforce` metadata field before trusting a verdict run
through a fresh invocation of `15-fairness-benchmark.sh`.

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

# 3. Do NOT restart first. Poll until the dashboard shows as provisioned in
#    the "Kueue" folder (anonymous read is enough):
G=https://grafana-grafana.apps.ocp.paladinaura.com
curl -sk "$G/api/dashboards/uid/maas-fairness-gpu-epp" | python3 -c 'import json,sys
d=json.load(sys.stdin); m=d["meta"]
print(len(d["dashboard"]["panels"]), "panels, provisioned:", m.get("provisioned"), "folder:", m.get("folderTitle"))'
#    Expect "63 panels, provisioned: True folder: Kueue" (51 panels + 12 rows).
# 4. Only if it is still not provisioned after ~2 minutes, restart the pod.
#    This costs ~30-60 s of Grafana downtime and wipes its emptyDir database.
$OC delete pod -n grafana -l app=grafana
```

Observed on the first live load (UNI-130, 2026-11-02): the optional volume was
absent when the pod started 41 days earlier, but kubelet attached it once the
ConfigMap existed. The file provisioner then took over the existing uid
`maas-fairness-gpu-epp` within ~20 s of the create, with no restart. That uid
was a 6-panel API import from UNI-50 in the General folder; it went from v1 to
v2 and moved into Kueue. Step 4 was not needed. The first load used plain
`oc create configmap ... --from-file` (no `last-applied` annotation). The
JSON is ~150 KB, so step 2's `apply` still fits under the 256 KB annotation
limit; it warns about the missing annotation once, then works.

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
`oc auth can-i update configmaps -n grafana` both return `no`. Writing to
`grafana` takes the Khala's break-glass role, granted by the board operator
for a limited time. That is how the 2026-11-02 load was done. Re-run step 1 and re-apply
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

### A scored, named-scenario wrapper for the open-loop generator (UNI-137)

`13-loadgen-poisson.sh` above is the generator itself — one invocation, one
`$OUT` directory, no verdict. `deploy/poc/17-fairness-benchmark-openloop.sh`
wraps it the way `15-fairness-benchmark.sh` wraps the closed-loop
`04-loadgen.yaml` Job: one named scenario in, a `results/<ts>-<label>/`
directory and a PASS/FAIL/UNCONTENDED verdict out, scored by the same
`15-fairness-report.py` (which gained an open-loop log parser for this).
It does not create or poll a Job — this generator is a local process — so
its only concurrency guard is refusing to start while a `maas-loadgen` Job
from a closed-loop run is still `Active`.

```sh
OPENSHIFT_TOKEN=... RATE_APP1=4.9 RATE_APP2=4.9 RATE_END_USERS=4.9 \
  DURATION=240 ./deploy/poc/17-fairness-benchmark-openloop.sh \
  b5-open-loop-below-saturation my-label
```

See "UNI-137: B5, open-loop (Poisson) below / at / above saturation" in
`docs/poc-results.md` for a worked set of three scenarios (70/100/120% of
UNI-34's measured pool ceiling) and the UNCONTENDED-verdict fix this ticket
needed (see also the "Correction (UNI-137)" note above).

**`CLIENT_TIMEOUT` (UNI-157, default 90, matches the pre-existing hardcoded
value)** overrides `13-loadgen-poisson.py`'s `urlopen` timeout. Needed for any
scenario testing `flowControl.defaultRequestTTL` specifically (currently
300s live): left at the 90s default, the client gives up before the TTL
does, and the EPP records `EvictedContextCancelled` instead of `EvictedTTL`,
silently never exercising the mechanism under test. Set it above the TTL and
below the Route's `haproxy.router.openshift.io/timeout` (600s). Pass `DRAIN_TIMEOUT`
comfortably above whatever `CLIENT_TIMEOUT` you pick, for the same reason.
`13-loadgen-poisson.sh`'s `snapshot_metrics()` also now greps
`^llm_d_epp_flow_control_` in addition to `^llm_d_epp_maas_fairness_`, so a
shedding run's before/after snapshots carry real eviction-outcome deltas —
see "UNI-157: E3, queue TTL shedding" in `docs/poc-results.md` for a worked
run and a load-bearing caveat about this rig's Gateway connection capacity
under the concurrency a real TTL test requires.

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
