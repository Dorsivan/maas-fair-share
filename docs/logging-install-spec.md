# Install spec: OpenShift Logging 6.6 + LokiStack for the fairness POC

**Status: specification only. Nothing in this document has been applied.** No
agent on this POC holds the permissions it needs (see *Access request* below),
so this document and the manifests beside it in `deploy/logging/` are the
handover artifact: they are written so that whoever administers
`ocp.paladinaura.com` can apply them in one pass without asking a follow-up
question.

What it buys us: the flight-recorder line the EPP already emits
(`pkg/fairness/weightedlas/plugin.go`, `runFlightRecorder`) becomes *queryable*
instead of something you catch with `oc logs` and a stopwatch. "Group `b` was
starved at 14:02" turns into a LogQL query with a timestamp on it.

Everything below was checked against this cluster on **2026-10-19** with the
read-only `poc-viewer` token. Where a value came from the cluster, the command
that produced it is shown.

## Apply it from the files, not from this prose

Every manifest in §4–§6 is also committed as an applyable file, so nothing has
to be transcribed out of markdown:

| File | Contents | Section |
|---|---|---|
| `deploy/logging/01-operators.yaml` | 2 Namespaces, 2 OperatorGroups, 2 Subscriptions | §4 |
| `deploy/logging/02-lokistack.yaml` | the `LokiStack` | §5 |
| `deploy/logging/03-collector.yaml` | ServiceAccount, 2 ClusterRoleBindings, reader ClusterRole, `ClusterLogForwarder` | §6 |
| `deploy/logging/04-reader-binding.yaml` | **optional** — binds the reader role to `poc-viewer` so an agent can verify | §8 item 7 |

The YAML in the sections below is identical to those files; it is inlined here
so the document reads on its own and so each block can carry the explanation of
what goes wrong without it. If the two ever disagree, **the files are
authoritative** — they are what gets applied. `04-reader-binding.yaml` is split
out precisely so that declining item 7 means not applying one file, rather than
editing one.

There is deliberately no file for the object-storage Secret (§4): it carries a
credential, and nothing credential-bearing belongs in this repository.

What has been checked about those files, on 2026-10-19:

- All four parse; 13 objects total, and every one of them is semantically
  identical to the inline block in this document (compared as parsed YAML, not
  as text).
- `01-operators.yaml` validates clean against the live API server:
  `oc apply --dry-run=client` accepts all six objects.
- `02-lokistack.yaml` and the `ClusterLogForwarder` in `03-collector.yaml`
  cannot be validated yet — `no matches for kind "LokiStack" in version
  "loki.grafana.com/v1"`, because the CRDs arrive with the operators. Re-run
  `--dry-run=server` on both after item 4 and before item 5.
- The ClusterRoleBindings return `Forbidden` under `poc-viewer` even in a
  dry run, since the dry run still reads current state at cluster scope. That
  is the permission ceiling, not a defect in the file.

---

## 1. What is already here, and what is missing

```sh
OC="oc --token=$OPENSHIFT_TOKEN --server=https://api.ocp.paladinaura.com:6443"
$OC get crd | grep -iE 'loki|clusterlog'      # -> nothing
$OC get ns  | grep -iE 'logging|loki'         # -> nothing
```

Nothing is installed. The catalogs are present and carry what we need:

```sh
$OC get packagemanifests -n openshift-marketplace | grep -iE 'cluster-logging|loki-operator'
# cluster-logging   Red Hat Operators
# loki-operator     Red Hat Operators      <- the one we want
# loki-operator     Community Operators    <- NOT this one
```

> **`loki-operator` is ambiguous.** There are two package manifests with that
> exact name. `oc get packagemanifest loki-operator` returns the *Community*
> one (`v0.12.0`, image `docker.io/grafana/loki-operator`), which is not the
> Red Hat build, does not ship the `1x.*` t-shirt sizes the way the supported
> operator does, and is not what the `stable-6.6` channel below refers to.
> Always pin `source: redhat-operators` in the Subscription, which the
> manifests in this document do.

**One genuinely good surprise: an S3-compatible store already exists on the
cluster**, so the bucket is not a procurement item. See §3.

---

## 2. Operator versions

Both operators must be on the **same minor**. Red Hat does not support a Loki
Operator and a Cluster Logging Operator from different 6.x minors, and the
failure mode is a `LokiStack` that reconciles into a state the collector cannot
write to.

| Component | Package | Catalog | Channel | CSV | Operator image (digest-pinned) |
|---|---|---|---|---|---|
| Cluster Logging Operator | `cluster-logging` | `redhat-operators` | `stable-6.6` | `cluster-logging.v6.6.1` | `registry.redhat.io/openshift-logging/cluster-logging-rhel9-operator@sha256:fc00b142087d15065ec8cdca58a59acf30733772b86272fe952646501cb7fe88` |
| Loki Operator | `loki-operator` | `redhat-operators` | `stable-6.6` | `loki-operator.v6.6.1` | `registry.redhat.io/openshift-logging/loki-rhel9-operator@sha256:ab1ca5984df61deec69d8ebf2f9c52df45778beff841fd5758dd1678a7632c56` |

Produced by:

```sh
$OC get packagemanifests -n openshift-marketplace -l catalog=redhat-operators -o json \
  | jq -r '.items[] | select(.metadata.name=="loki-operator" or .metadata.name=="cluster-logging")
           | .metadata.name + " default=" + .status.defaultChannel,
             (.status.channels[] | "  " + .name + " -> " + .currentCSV
              + "  " + .currentCSVDesc.annotations.containerImage)'
```

`stable-6.6` is the default channel for both. Older channels present if a
downgrade is ever needed: `stable-6.2` (6.2.13), `stable-6.3` (6.3.4),
`stable-6.4` (6.4.7), `stable-6.5` (6.5.3).

The digests are recorded here because they are an air-gap input. These two are
the *operator* images only — the complete mirror set is **nine** images and is
enumerated in full in §9. Do not build a mirror from this table. Set
`installPlanApproval: Manual` as below so the pinned CSV cannot drift out from
under a mirrored registry.

> **Logging 6.x removed the `ClusterLogging` CR.** If you have installed
> logging on OpenShift before, the muscle memory is wrong: there is no
> `ClusterLogging` object in 6.x. The collector is defined entirely by a
> `ClusterLogForwarder` (`observability.openshift.io/v1`) plus a ServiceAccount
> you create and bind yourself. §6 does it that way.

---

## 3. Object storage

### What exists

A MinIO deployment is already running on this cluster and is reachable
in-cluster without an egress path:

```sh
$OC get deploy,svc,route -n minio
# deployment.apps/minio                    1/1
# service/minio-api                        ClusterIP 172.30.215.188  9000/TCP,9001/TCP
# route/minio-api       minio-api-minio.apps.ocp.paladinaura.com     edge
# route/minio-console   minio-console-minio.apps.ocp.paladinaura.com edge
```

Use it. The S3 endpoint for Loki is the **Service**, not the Route — the Route
is edge-terminated at the ingress and routing Loki's object traffic out to the
ingress and back is pointless latency:

```
http://minio-api.minio.svc.cluster.local:9000
```

### What is needed

1. A bucket named **`maas-fairness-loki`**.
2. An access key / secret pair scoped to that bucket.

Creating both, from a machine that can reach the MinIO console or API:

```sh
mc alias set poc http://minio-api-minio.apps.ocp.paladinaura.com <root-user> <root-pass>
mc mb poc/maas-fairness-loki
mc admin user svcacct add poc <root-user>     # prints an access key + secret key
```

> Credentials must **not** be pasted into this repository, a ticket comment, or
> a log line. Hand them over through the Paperclip secret path named in the
> access request; the agent driving the install will propose them as a Paperclip
> secret on receipt and never echo them. If the administrator prefers not to
> share them at all, that is fine — they can create the Kubernetes Secret in §4
> themselves and no agent ever sees the value. **That is the preferred option.**

### MinIO caveats that will bite

- MinIO's deployment here runs `quay.io/minio/minio:latest` — a floating tag.
  That is fine for a POC on a cluster that already has it, and is **not**
  acceptable in the air-gap transfer: a disconnected destination must pin a
  digest or substitute ODF/NooBaa. Recorded in §9.
- The endpoint is plain `http://`. The Loki Operator accepts this for
  S3-compatible endpoints. Do not add `insecure: true` anywhere; the scheme in
  the `endpoint` key is what decides it.
- `region` is **optional** here, and the reason is worth stating because it is
  easy to assume otherwise: the operator's `validateS3Endpoint` returns early
  for non-AWS hosts, so region is only mandatory for STS modes and
  `*.amazonaws.com` endpoints. §4 includes `us-east-1` anyway as conventional
  filler — harmless, and it keeps the secret shape identical to the AWS case.
- `forcepathstyle: "true"` is likewise not strictly required — the operator
  derives it as `!strings.HasSuffix(endpoint, ".amazonaws.com")`, which is
  already `true` for this endpoint — but Red Hat's documented recipe for
  S3-compatible backends includes it, so §4 sets it explicitly rather than
  relying on a derived default.

---

## 4. Namespaces, secret, and operator subscriptions

```sh
$OC apply -f deploy/logging/01-operators.yaml
```

Order matters only in that the namespaces must exist first, which `oc apply` of
a single multi-document file handles. Contents, for reading:

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: openshift-logging
  labels:
    openshift.io/cluster-monitoring: "true"
---
apiVersion: v1
kind: Namespace
metadata:
  name: openshift-operators-redhat
  labels:
    openshift.io/cluster-monitoring: "true"
---
# Cluster Logging Operator. Logging 6.x uses an AllNamespaces-mode
# OperatorGroup -- note the absence of targetNamespaces, which is deliberate
# and is NOT the same as the OwnNamespace group used by logging 5.x.
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: openshift-logging
  namespace: openshift-logging
spec:
  upgradeStrategy: Default
---
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: cluster-logging
  namespace: openshift-logging
spec:
  channel: stable-6.6
  name: cluster-logging
  source: redhat-operators
  sourceNamespace: openshift-marketplace
  startingCSV: cluster-logging.v6.6.1
  installPlanApproval: Manual        # pin; approve the InstallPlan explicitly
---
# Loki Operator. Must go in openshift-operators-redhat, not openshift-operators:
# the latter is the community/global group and installing here alongside other
# operators has produced dependency conflicts.
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: openshift-operators-redhat
  namespace: openshift-operators-redhat
spec: {}
---
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: loki-operator
  namespace: openshift-operators-redhat
spec:
  channel: stable-6.6
  name: loki-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
  startingCSV: loki-operator.v6.6.1
  installPlanApproval: Manual
```

With `installPlanApproval: Manual`, nothing installs until the InstallPlans are
approved:

```sh
$OC get installplan -A | grep -E 'openshift-logging|openshift-operators-redhat'
$OC patch installplan <name> -n <ns> --type merge -p '{"spec":{"approved":true}}'
# then wait for both:
$OC get csv -n openshift-logging           # cluster-logging.v6.6.1  Succeeded
$OC get csv -n openshift-operators-redhat  # loki-operator.v6.6.1    Succeeded
```

### The object-storage Secret — exact shape

Name and namespace are referenced by the `LokiStack` in §5 and must match
exactly. The key names below are the Loki Operator's S3 contract; a typo in a
key name produces a `LokiStack` stuck in `Pending` with a degraded condition
rather than a clear error.

```sh
$OC create secret generic logging-loki-s3 \
  -n openshift-logging \
  --from-literal=bucketnames="maas-fairness-loki" \
  --from-literal=endpoint="http://minio-api.minio.svc.cluster.local:9000" \
  --from-literal=region="us-east-1" \
  --from-literal=forcepathstyle="true" \
  --from-literal=access_key_id="<access key>" \
  --from-literal=access_key_secret="<secret key>"
```

Equivalent declarative form, for the record — **do not commit a populated copy
of this**:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: logging-loki-s3
  namespace: openshift-logging
type: Opaque
stringData:
  bucketnames: maas-fairness-loki
  endpoint: http://minio-api.minio.svc.cluster.local:9000
  region: us-east-1
  forcepathstyle: "true"
  access_key_id: "<access key>"
  access_key_secret: "<secret key>"
```

---

## 5. LokiStack

```sh
$OC apply -f deploy/logging/02-lokistack.yaml
```

```yaml
apiVersion: loki.grafana.com/v1
kind: LokiStack
metadata:
  name: logging-loki
  namespace: openshift-logging
spec:
  size: 1x.demo
  storage:
    schemas:
      - version: v13
        effectiveDate: "2026-10-01"
    secret:
      name: logging-loki-s3
      type: s3
  storageClassName: nfs
  tenants:
    mode: openshift-logging
  limits:
    global:
      retention:
        days: 7
```

Notes, each of which is a thing that goes wrong:

- **`name: logging-loki` is load-bearing.** The `lokiStack` output type in the
  `ClusterLogForwarder` (§6) and the OpenShift console log plugin both resolve
  the stack by name. Renaming it means editing §6 too.
- **`schemas` must be set explicitly, with an `effectiveDate` that is already
  current.** Both failure modes here are loud, which is good news: `schemas` is
  in `spec.storage.required` with `minItems: 1`, so omitting it is rejected at
  admission, and the validating webhook's `ValidateSchemas` requires at least
  one schema whose effective date has already passed, so an all-future list is
  rejected too. `v13` is the current schema for 6.x. If this is applied after
  2026-11-01, move `effectiveDate` back, not forward.
- **`storageClassName: nfs` is the only option on this cluster** and it is the
  weakest part of this design:

  ```sh
  $OC get sc
  # nfs (default)   cluster.local/nfs-provisioner-nfs-subdir-external-provisioner
  ```

  Loki's ingester WAL and index are many-small-file workloads, which is exactly
  what the `openshift-conventions` note warns about for this StorageClass.
  Expect NFS to be the dominant latency. **Treat this as the most likely thing
  to fail outright**, not merely to be slow: Loki ingesters on NFS also hit
  file-locking and `mmap` problems, so the failure can be a crash-looping
  ingester rather than a sluggish one. If that happens, it is the StorageClass,
  not the spec — report it and stop rather than tuning around it. Adequate to
  attempt at demo scale; must be called out as a difference in any production
  or air-gap target.
- **Retention on `1x.demo` is best-effort.** The compactor that enforces
  `retention.days` is present but the demo size is not a configuration Red Hat
  makes retention guarantees about. 7 days is a request, not a contract. For
  the POC that is fine — we need hours, not days.

### A correction worth recording about `1x.demo`

The ticket describes `1x.demo` as "the smallest supported size". It is the
smallest size, but Red Hat documents it as **demonstration-only and not
supported**: single replica per component, no HA, no retention guarantee. The
smallest *supported* size in the 6.x operator is `1x.pico`.

I am specifying `1x.demo` anyway, because it is right for this POC: one
EPP emitting one structured line every five seconds while contended is a
rounding error of ingest volume, and `1x.demo` is the only size that fits
comfortably on a cluster whose sole StorageClass is NFS. But the production
story the board wants to validate should be written against `1x.pico` or
larger, and **the handover must not imply that what we demonstrate on
`1x.demo` is a supported production configuration.** Before applying, confirm
the size enum against the installed CRD rather than trusting this document:

```sh
$OC get crd lokistacks.loki.grafana.com -o jsonpath='{.spec.versions[0].schema.openAPIV3Schema.properties.spec.properties.size.enum}'
```

Wait for the stack before continuing:

```sh
$OC get lokistack logging-loki -n openshift-logging -o json \
  | jq -r '.status.conditions[] | .type + "=" + .status + "  " + (.message // "")'
# want: Ready=True
$OC get pods -n openshift-logging
# expect: distributor, ingester, querier, query-frontend, compactor,
#         index-gateway, and logging-loki-gateway (2/2 containers -- the
#         second is the opa-openshift sidecar that enforces tenancy)
```

The operator also creates the gateway **Route** itself, named after the stack
(`logging-loki`), `termination: reencrypt`, targeting
`logging-loki-gateway-http`. It is suppressed only by
`spec.tenants.disableIngress: true`, which this spec does not set. Nobody needs
to create it by hand:

```sh
$OC get route logging-loki -n openshift-logging
```

---

## 6. Collector: ServiceAccount, RBAC, ClusterLogForwarder

```sh
$OC apply -f deploy/logging/03-collector.yaml
```

In 6.x the collector runs under a ServiceAccount **you** create, and its
permission to read container logs comes from ClusterRoleBindings **you** create.
The operator does not do this for you.

If you omit them, the failure is at least loud and in a known place: the
operator runs a SubjectAccessReview against the ServiceAccount before deploying
anything, and on failure sets `Authorized=False` with reason
`ClusterRoleMissing` on the `ClusterLogForwarder` and deploys **no collector
DaemonSet at all** (deleting an existing one). So if no collector pods appear,
do not go looking for a silently idle daemon — read
`.status.conditions` first.

```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: maas-log-collector
  namespace: openshift-logging
---
# Read application container logs. This is the only one strictly required for
# this POC; infrastructure and audit are deliberately left out (§7).
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: maas-log-collector-application-logs
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: collect-application-logs
subjects:
  - kind: ServiceAccount
    name: maas-log-collector
    namespace: openshift-logging
---
# Write into the LokiStack through its gateway as the "application" tenant.
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: maas-log-collector-logging-application-write
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: logging-collector-logs-writer
subjects:
  - kind: ServiceAccount
    name: maas-log-collector
    namespace: openshift-logging
---
# READ side, for whoever verifies the result (§7).
#
# Do NOT reach for `cluster-logging-application-view`. That ClusterRole is a
# trap: it is not shipped by either operator. It is created at runtime by the
# Cluster Observability Operator's Logging UIPlugin controller, which this
# spec treats as optional -- so on a cluster without the UIPlugin, a
# ClusterRoleBinding naming it is accepted by the API server and grants
# precisely nothing, with no error anywhere. Define the role explicitly:
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: maas-fairness-application-logs-reader
rules:
  - apiGroups: ["loki.grafana.com"]
    resources: ["application"]
    resourceNames: ["logs"]
    verbs: ["get"]
```

```yaml
apiVersion: observability.openshift.io/v1
kind: ClusterLogForwarder
metadata:
  name: maas-fairness
  namespace: openshift-logging
spec:
  managementState: Managed
  serviceAccount:
    name: maas-log-collector
  outputs:
    - name: default-lokistack
      type: lokiStack
      lokiStack:
        target:
          name: logging-loki
          namespace: openshift-logging
        authentication:
          token:
            from: serviceAccount
      tls:
        ca:
          key: service-ca.crt
          configMapName: openshift-service-ca.crt
  inputs:
    - name: maas-fairness-app
      type: application
      application:
        includes:
          - namespace: maas-fairness-poc
  pipelines:
    - name: maas-fairness-to-loki
      inputRefs:
        - maas-fairness-app
      outputRefs:
        - default-lokistack
```

The input is scoped to `maas-fairness-poc`, which is the ticket's stated
minimum and also the right default: collecting the whole cluster into a
`1x.demo` stack backed by NFS is how you discover the NFS limit the hard way.
Widening later is a one-line change — add namespaces to `includes`, or drop
`inputs` and use the built-in `application` input for everything.

```sh
$OC get clusterlogforwarder maas-fairness -n openshift-logging -o json \
  | jq -r '.status.conditions[] | .type + "=" + .status + "  " + (.reason // "") + "  " + (.message // "")'
$OC get pods -n openshift-logging -l app.kubernetes.io/component=collector
```

### Optional: the console log view

Makes the query runnable from the OpenShift web console instead of curl. Needs
the Cluster Observability Operator (`cluster-observability-operator`, present
in `redhat-operators`) and:

```yaml
apiVersion: observability.openshift.io/v1alpha1
kind: UIPlugin
metadata:
  name: logging
spec:
  type: Logging
  logging:
    lokiStack:
      name: logging-loki
```

Nice to have, not required by the done-criteria. Skip it if the administrator
would rather not add a third operator — §6 defines its own reader ClusterRole
precisely so that nothing in this spec depends on the UIPlugin being present.
(Installing it is also what would create the `cluster-logging-<tenant>-view`
roles that people expect to find and do not.)

---

## 7. Verification: the flight-recorder line, end to end

### What the line actually looks like

This is the part most likely to be got wrong by someone writing the query from
the Go source, so it is recorded from the live pod rather than inferred.

The EPP emits **OTel-style JSON**, not the `{"level","ts","msg"}` zap shape.
Sampled on 2026-10-19 from the GPU EPP:

```sh
$OC logs maas-vllm-gpu-kserve-router-scheduler-d95dcd886-4b6lg -n maas-fairness-poc --tail=1
```

```json
{"severity_text":"DEBUG","timestamp":"2026-10-19T12:16:02.229624009Z",
 "caller":"controller/inferencepool_reconciler.go:49",
 "body":"Reconciling InferencePool","service.name":"llm-d-epp",
 "namespace":"maas-fairness-poc","severity_number":5}
```

> **The message is in `body`, not `msg`.** A LogQL query written as
> `| json | msg="fairness state"` matches nothing, silently, forever. This is
> the single biggest trap in the query pack and is the main thing this ticket
> hands to the log field contract / LogQL query pack work (ticket D9).

`runFlightRecorder` calls `log.FromContext(ctx).Info("fairness state", "plugin",
p.name, "state", p.dump())`, so the emitted line is the same envelope with
`"body":"fairness state"`, `"severity_text":"INFO"`, a `"plugin"` field holding
the configured plugin name (`maas-fairness` on this cluster), and a `"state"`
object carrying the `dumpState` struct: `enforcing`, `halfLifeSeconds`,
`costModel`, `groups[]`, `unmatchedSubscriptionsTotal`,
`recentUnmatchedSubscriptions[]`, `truncated`.

### The recorder is gated — you must create contention to see anything

```go
last := p.lastContendedUnixNano.Load()
if last == 0 || p.now().Sub(time.Unix(0, last)) > interval { continue }
```

An idle cluster emits **zero** flight-recorder lines by design. Confirmed:
across the full retained log of both the GPU and CPU EPP pods on 2026-10-19,
`grep -c '"fairness state"'` returns `0`, because nothing has contended in
24 hours. Anyone who installs this stack, looks at an idle cluster and
concludes the collector is broken will be wrong.

The live GPU EPP config has `stateLogIntervalSeconds: 5`
(`$OC get cm maas-epp-config -n maas-fairness-poc -o yaml`), so during a load
run the line lands every 5 seconds.

### Procedure

**Read steps 2–4 before starting.** The query has to overlap the load run, so
do not block on `oc wait` first — that is the one ordering mistake that makes
this procedure fail while looking correct.

1. Bring the GPU nodes up if they are down — `docs/runbook.md`, *Bring the GPU
   nodes back up*. They were **up** on 2026-10-19
   (`maas-vllm-gpu-kserve` 2/2 on `ocp-gpu-worker-0`/`-1`).

2. Start the load — **do not wait for it**:

   ```sh
   $OC apply -f deploy/poc/04-loadgen.yaml
   ```

   The generator's committed settings are already what we want: all three
   tenants, 32 workers each (~12x over-offer against 8 backend slots), and
   `DURATION: "240"` — four minutes. Do not reduce them; a merely saturating
   load produces an equal split and no sustained contention.

   > `180` appears in that file, but only as the `DURATION="${DURATION:-180}"`
   > shell fallback (`deploy/poc/04-loadgen.yaml:35`). The Job sets `240`
   > explicitly (`deploy/poc/04-loadgen.yaml:168`), which is what actually
   > runs. Budget the query window against 240s, not 180s.

3. **While the Job is still running**, poll Loki with the query below. The
   recorder stops within one `stateLogIntervalSeconds` (5s on this cluster) of
   the last contended dispatch, so the live window is roughly those four
   minutes:

   ```sh
   for i in $(seq 1 16); do
     <the curl from "The query", below>
     sleep 15
   done
   ```

   If you would rather run it once after the fact, that works too — but then
   the `query_range` window must explicitly reach back over the whole run
   rather than relying on the default (`now-1h`..`now` is usually fine, but
   say so rather than assuming):

   ```sh
   START=$(( ($(date -u +%s) - 900) ))000000000   # 15 min back, ns
   END=$(date -u +%s)000000000
   # ...and add to the curl:  --data-urlencode "start=$START" --data-urlencode "end=$END"
   ```

4. **Only then** wait on the Job, as a tail-end check that the run itself was
   healthy rather than as a gate on step 3:

   ```sh
   $OC wait --for=condition=complete job/maas-loadgen -n maas-fairness-poc --timeout=10m
   $OC logs job/maas-loadgen -n maas-fairness-poc --tail=20
   ```

   `backoffLimit: 0`, so a failed run does not retry — if the Job fails, delete
   it and re-apply rather than waiting for a retry that will not come.

### The query

```logql
{log_type="application",
 kubernetes_namespace_name="maas-fairness-poc",
 kubernetes_pod_name=~"maas-vllm-gpu-kserve-router-scheduler-.*"}
  |= "fairness state"
  | json
  | body = "fairness state"
```

Narrowed to one group's normalized service, which is the form D9 will want:

```logql
{log_type="application",
 kubernetes_namespace_name="maas-fairness-poc",
 kubernetes_pod_name=~"maas-vllm-gpu-kserve-router-scheduler-.*"}
  |= "fairness state"
  | json plugin="plugin", groups="state.groups"
  | line_format "{{ .groups }}"
```

> Parameterless `| json` flattens nested **objects** with `_` and **skips
> arrays entirely** — it does not stringify them. So a bare `| json` produces
> *no label at all* for `state.groups`, not a truncated or awkward one. You
> only get it by naming it explicitly as above, in which case the array is
> assigned to the label serialized as JSON. Writing
> `| json | state_groups_0_name="b"` does not work and never will.

Run it against the LokiStack gateway. The `application` tenant path is not
optional in the URL:

```sh
LOKI=https://$($OC get route logging-loki -n openshift-logging -o jsonpath='{.spec.host}')

# The Route is reencrypt, so it is terminated at the ingress router and
# presents the router's wildcard cert -- which is NOT signed by the service CA.
# Using /var/run/secrets/.../service-ca.crt here fails verification (and that
# path only exists inside a pod anyway). Use the ingress CA:
$OC extract configmap/default-ingress-cert -n openshift-config-managed \
  --keys=ca-bundle.crt --to=/tmp --confirm

curl -sG --cacert /tmp/ca-bundle.crt \
  -H "Authorization: Bearer $OPENSHIFT_TOKEN" \
  "$LOKI/api/logs/v1/application/loki/api/v1/query_range" \
  --data-urlencode 'query={log_type="application",kubernetes_namespace_name="maas-fairness-poc"} |= "fairness state"' \
  --data-urlencode 'limit=5' | jq '.data.result[].values[][1]'
```

**Pass condition:** that command returns at least one line whose `body` is
`fairness state` and whose `state.groups` contains the four configured groups
(`app1`, `app2`, `end-users`, `unclassified`), with a timestamp inside the load
window. Paste the query and the returned line into the ticket. A line found by
`oc logs` does **not** satisfy this — the whole point is that it came back
through LogQL.

### What the verifying agent needs in order to run that

The read-only `poc-viewer` ServiceAccount cannot read from the gateway today.
Note the resource string carefully — the tenant is a **resource name**, not
part of the API group:

```sh
# correct form: resource `application` in group loki.grafana.com, resourceName `logs`
$OC auth can-i get application.loki.grafana.com/logs -n maas-fairness-poc   # no
$OC auth can-i create pods/portforward -n openshift-logging                 # no
$OC auth can-i get routes -n openshift-logging                              # yes
```

> Writing it as `application.logs.loki.grafana.com` — which is the natural
> guess — parses as resource `application` in a group called
> `logs.loki.grafana.com`, which does not exist. That check returns `no`
> whether or not the grant is actually in place, so it will cheerfully tell you
> the grant failed after a successful one.

One read-only grant closes the gap — §8, item 7.

---

## 8. Access request — what the cluster administrator must do

Nothing here asks for an agent to be given cluster-admin, and nothing here asks
for an agent to be able to install an operator. Items 1–6 are administrator
actions; item 7 is a single read-only grant so the result can be verified and
written up.

| # | Action | Object / scope |
|---|---|---|
| 1 | Create the two namespaces | `oc apply -f deploy/logging/01-operators.yaml` — `openshift-logging`, `openshift-operators-redhat`, both labelled `openshift.io/cluster-monitoring: "true"` (§4) |
| 2 | Create a MinIO bucket and a scoped access key | bucket `maas-fairness-loki` on the existing `minio` deployment (§3). No file — nothing credential-bearing is committed. |
| 3 | Create the object-storage Secret | `logging-loki-s3` in `openshift-logging`, exact key names in §4. **Preferred: you create it, no agent ever sees the value.** |
| 4 | Approve the InstallPlans | same file as item 1 creates the Subscriptions; `installPlanApproval: Manual` means nothing installs until you approve. `cluster-logging.v6.6.1` (`openshift-logging`) and `loki-operator.v6.6.1` (`openshift-operators-redhat`), both from `redhat-operators`, channel `stable-6.6` (§4) |
| 5 | Apply the LokiStack | `oc apply -f deploy/logging/02-lokistack.yaml` — `logging-loki` in `openshift-logging`, size `1x.demo`, `storageClassName: nfs` (§5) |
| 6 | Apply the collector | `oc apply -f deploy/logging/03-collector.yaml` — ServiceAccount, 2 ClusterRoleBindings, reader ClusterRole, `ClusterLogForwarder` (§6). The ClusterRole and the two bindings are the cluster-scoped part. |
| 7 | Bind the reader role to the POC's read-only SA | `oc apply -f deploy/logging/04-reader-binding.yaml` — binds `maas-fairness-application-logs-reader` (defined in §6) to `system:serviceaccount:paperclip:poc-viewer`. Grants exactly `get` on `application` / resourceName `logs` in `loki.grafana.com`, and nothing else. **Optional — see below.** |

No Route request: **the Loki Operator creates the `logging-loki` Route itself**
(§5). Nothing to do there beyond confirming it appeared.

Item 7 in full — it is three lines of substance and it is the only thing in
`deploy/logging/` that grants anything to an agent identity:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: maas-fairness-application-logs-reader-poc-viewer
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: maas-fairness-application-logs-reader
subjects:
  - kind: ServiceAccount
    name: poc-viewer
    namespace: paperclip
```

**If item 7 is refused**, that is a fine answer and we do not need it: the
administrator can run the §7 curl themselves and paste the output into the
ticket, and the POC records "LogQL verification performed by the cluster
administrator" as its evidence. Say so rather than leaving it pending.

**If item 7 is granted and the query still returns
`You don't have permission to access this tenant`:** this is a known wrinkle
with *ServiceAccount* tokens at the gateway — a cluster-wide application-read
grant can still be rejected on the `application` tenant while `infrastructure`
and `audit` succeed. Either add the SA's group to
`spec.tenants.openshift.adminGroups` on the LokiStack, or fall back to the
administrator-runs-the-query option above. Do not spend an afternoon on it.

**Credentials:** if a bucket credential is handed over despite item 3's
preference, the receiving agent proposes it as a Paperclip secret on receipt
and never writes it to a comment, document, commit, or log.

---

## 9. What this proves, and what it does not

**Proves (once applied and verified):** that the flight-recorder line the
plugin already emits survives collection, parses as JSON on the Loki side, and
is retrievable by a LogQL query that a reviewer can re-run — which is the
production observability claim in `docs/design.md` ("a flight recorder in Loki
even without Prometheus") actually tested rather than asserted.

**Does not prove:**

- *Anything about scale.* One EPP, one 5-second line while contended, a
  `1x.demo` stack. No statement about ingest rate, cardinality, or query
  latency at production volume.
- *A supported configuration.* `1x.demo` is demonstration-only (§5) and NFS is
  the wrong StorageClass for Loki (§5). Both are deliberate POC compromises.
- *Retention.* 7 days is requested; on `1x.demo` it is not guaranteed and will
  not be measured here.
- *The CPU-served deployments or the simulator.* Out of scope by board
  direction (2026-10-19); the input is scoped to the namespace, so their logs
  would be collected incidentally, but nothing about them is verified.
- *Audit or infrastructure logs.* Deliberately not collected (§6).

**Air-gap deltas** (feeds the transfer report):

### Mirror set — complete, nine images

Enumerated from the packagemanifests on **2026-10-19**, *before* install.
This matters: on this ticket the install is the thing most likely never to
happen, so a mirror list deferred to "read the CSVs after install" would have
been deferred permanently, inside the one document meant to survive the POC.
It does not need deferring — `relatedImages` is already in the catalog:

```sh
$OC get packagemanifests -n openshift-marketplace -l catalog=redhat-operators -o json \
  | jq -r '.items[] | select(.metadata.name=="cluster-logging" or .metadata.name=="loki-operator")
           | .metadata.name as $n | .status.channels[] | select(.name=="stable-6.6")
           | ($n + "  CSV=" + .currentCSV), (.currentCSVDesc.relatedImages[] | "    " + .)'
```

| # | Operator | Image (digest-pinned) | Role | Compressed size |
|---|---|---|---|---|
| 1 | cluster-logging | `registry.redhat.io/openshift-logging/cluster-logging-rhel9-operator@sha256:fc00b142087d15065ec8cdca58a59acf30733772b86272fe952646501cb7fe88` | operator | unknown — obtain at mirror time |
| 2 | cluster-logging | `registry.redhat.io/openshift-logging/vector-rhel9@sha256:5fe87d1d26c62c813a2dbb06a6ee63ab962a2ffbeef899ed62743a158288b759` | the collector itself (§6) | unknown — obtain at mirror time |
| 3 | cluster-logging | `registry.redhat.io/openshift-logging/log-file-metric-exporter-rhel9@sha256:66825aaf4b9aaca6ca2ee73593019392590c5c2e947af1f8b22bc8e9e4071c79` | collector metrics sidecar | unknown — obtain at mirror time |
| 4 | cluster-logging | `registry.redhat.io/openshift-logging/cluster-logging-operator-bundle@sha256:b70b971f9692763a3941e2bd6b14f0c42da9ea1463611c580ab97dd35a2d05d6` | OLM bundle | unknown — obtain at mirror time |
| 5 | loki-operator | `registry.redhat.io/openshift-logging/loki-rhel9-operator@sha256:ab1ca5984df61deec69d8ebf2f9c52df45778beff841fd5758dd1678a7632c56` | operator | unknown — obtain at mirror time |
| 6 | loki-operator | `registry.redhat.io/openshift-logging/logging-loki-rhel9@sha256:e6993daf1b7287afd67fb348dc9c9cae08955869f95578b95c3eb99fbc4be263` | every LokiStack component pod (§5) | unknown — obtain at mirror time |
| 7 | loki-operator | `registry.redhat.io/openshift-logging/lokistack-gateway-rhel9@sha256:243d0dd213621bc8c37aaa345c29f633d1440545ef9af431b092f4a9f28e27ed` | **the gateway §7 queries through** | unknown — obtain at mirror time |
| 8 | loki-operator | `registry.redhat.io/openshift-logging/opa-openshift-rhel9@sha256:b5a936ad84333ffacab0cb970716c759b2a147ea1428ecf06ba8e8096318071c` | **tenancy sidecar in the gateway pod** | unknown — obtain at mirror time |
| 9 | loki-operator | `registry.redhat.io/openshift-logging/loki-operator-bundle@sha256:04bcd8f7bc94a504e7b0f60d4f68a047c1ede64c5cb45a78971bdb0b33ceb53d` | OLM bundle | unknown — obtain at mirror time |

> **Do not build this list from a wildcard.** An earlier draft of this section
> sketched the operands as "`logging-loki-*`, `vector`,
> `log-file-metric-exporter`". That pattern misses rows **7 and 8** — neither
> `lokistack-gateway-rhel9` nor `opa-openshift-rhel9` matches it. A mirror
> built that way yields a LokiStack whose `logging-loki-gateway` pod (the 2/2
> pod §5 tells you to expect) cannot start, and the gateway is exactly the
> component the §7 verification query talks to. The failure would surface at
> the last step of the install, not the first.

**On the size column.** Sizes are a required field of the transfer report and
they are genuinely not obtainable from here: `poc-viewer` has no
`registry.redhat.io` pull secret, and an anonymous manifest request returns
`401` (verified 2026-10-19). `unknown — obtain at mirror time` is recorded
rather than left blank, because a blank cell is indistinguishable from a cell
nobody looked at. Fill them from a host that holds a pull secret:

```sh
# per image, with a registry.redhat.io pull secret present:
oc image info --filter-by-os=linux/amd64 <image>            # prints "Image Size"
# or:
skopeo inspect --raw docker://<image> | jq '[.layers[].size] | add'
```

### The rest of the air-gap deltas

- **The optional console UIPlugin (§6) is excluded from the mirror set above,
  deliberately.** It is not required by this spec or by the done-criteria, and
  it is not cheap: it needs `cluster-observability-operator` (`v1.5.3` in this
  cluster's `redhat-operators` catalog), whose `relatedImages` is **25 further
  images** under `registry.redhat.io/cluster-observability-operator/*` —
  Prometheus, Thanos, Alertmanager, Perses, korrel8r and a set of console
  plugins, almost all of which have nothing to do with logging. If a
  disconnected destination does want the console log view, enumerate them with
  the same `jq` above against `cluster-observability-operator`; the three that
  are actually about logging are `cluster-observability-rhel9-operator`,
  `logging-console-plugin-rhel9` and its `-pf4`/`-pf5` variants. Nine images
  versus thirty-four is the reason §6 defines its own reader ClusterRole and
  depends on no third operator.
- `installPlanApproval: Manual` plus `startingCSV` is what keeps the mirrored
  digest and the installed CSV in agreement. Do not switch to `Automatic`.
- The object store must be re-pointed. MinIO here runs a floating
  `quay.io/minio/minio:latest` tag and is not a transferable artifact; the
  destination supplies its own S3 (ODF/NooBaa or equivalent) and only the
  `logging-loki-s3` Secret contents change.
- A disconnected cluster needs the `redhat-operators` catalog mirrored, or an
  `ImageDigestMirrorSet` pointing `registry.redhat.io/openshift-logging/*` at
  the local mirror.
