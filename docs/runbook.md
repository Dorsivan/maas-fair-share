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

## Standing checks before trusting any result

```sh
# No tenant silently in a different priority band -- fairness is intra-band only,
# and MaaS sets x-gateway-inference-objective per ServiceAccount.
oc get inferenceobjectives.llm-d.ai -A            # expect none, or all priority 0

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
