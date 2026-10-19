# Deploying Models-as-a-Service (RHOAI 3.4)

Follows the RHOAI 3.4 guide *Govern LLM access with Models-as-a-Service*.
Apply in order; each step is a prerequisite for the next, and skipping one of
01–05 leaves MaaS `Degraded` rather than failing loudly. **Step 09 is the one
exception to "fails loudly": skip it and MaaS reports healthy while silently
admitting a client-forged priority band (UNI-33) — the
`gateway-header-check` run at the end of this sequence is what catches that,
not the Tenant status.**

```sh
oc apply -f deploy/maas/01-kuadrant.yaml      # Kuadrant CR -> Authorino + Limitador
bash     deploy/maas/02-authorino-tls.sh      # guide 1.4 steps 1-3
oc apply -f deploy/maas/03-postgres.yaml      # throwaway DB + maas-db-config secret
oc apply -f deploy/maas/04-gateway.yaml       # maas-default-gateway (guide 1.3, + TLS step 4)
bash     deploy/maas/05-enable-maas.sh        # modelsAsService: Managed

# Deploy your LLMInferenceService now (e.g. `oc apply -f deploy/llmisvc.yaml`)
# and wait for it to reconcile. odh-model-controller only generates the
# per-Gateway AuthPolicy (maas-poc-gateway-authn) once an LLMInferenceService
# referencing this Gateway exists -- step 09 has nothing to patch before that.

oc patch authpolicy maas-poc-gateway-authn -n maas-fairness-poc --type=merge \
  --patch-file=deploy/maas/09-objective-header-stripping.patch.yaml
  # Closes UNI-33: without this, a client-set x-llm-d-inference-objective
  # header wins over the gateway's own value and picks its own priority
  # band. See docs/gateway-header-stripping.md for the mechanism and the
  # live proof. Safe to re-run; it's a merge patch.

# Build the conformance check once, offline (see docs/gateway-header-stripping.md,
# "Building this check air-gapped" -- this works with no network access):
(cd cmd/gateway-header-check && go build -o ../../bin/gateway-header-check .)
oc get httproute,gateway,authpolicy -n maas-fairness-poc -o yaml | bin/gateway-header-check -
  # Must print "OK" and exit 0. If it doesn't, the install is not done --
  # do not consider MaaS ready to serve traffic until it does.
```

Plus one cluster setting that is not a file here, because it merges into an
existing ConfigMap rather than replacing it:

```sh
# User Workload Monitoring -- without it MaaS reports Degraded.
# PRESERVE the existing content; this cluster pins prometheusK8s and
# alertmanagerMain to infra nodes and overwriting that would move them.
oc -n openshift-monitoring get cm cluster-monitoring-config \
  -o jsonpath='{.data.config\.yaml}'     # read first, then prepend:
# enableUserWorkload: true
```

## What was already present on this cluster

Worth checking before assuming work is needed:

- **The Kuadrant operator is installed as `rhcl-operator`** (Red Hat
  Connectivity Link v1.3.4) in the `connectivity-link` namespace, with the
  kuadrant, authorino, limitador and dns controllers all running. Grepping
  CSVs for "kuadrant" finds nothing and makes it look absent.
- `data-science-gateway-class` (controller `openshift.io/gateway-controller/v1`)
  already exists, so no GatewayClass needs creating.
- OpenShift 4.20.35 and RHOAI 3.4.4 both satisfy the minimums.

## Verification

```sh
oc get crd | grep maas.opendatahub.io                      # expect 5
oc get tenants.maas.opendatahub.io -A                      # default-tenant
oc get dsc -o jsonpath='{.items[0].status.conditions[?(@.type=="ModelsAsServiceReady")]}'
```

`Ready=True Reconciled` on the Tenant is the real signal.

## Known caveat: no LoadBalancer address

The MetalLB operator and its `MetalLB` CR are installed, but there are **no
`IPAddressPool` or `L2Advertisement` resources**, so every LoadBalancer Service
on this cluster sits at `EXTERNAL-IP <pending>` and the Gateway reports
`Programmed=False / AddressNotAssigned`.

This does **not** break MaaS — the Tenant reports `Ready=True` and all
prerequisites satisfied. It only means there is no external VIP. Access
options, cheapest first:

1. **ClusterIP** (what the tests use):
   `maas-default-gateway-data-science-gateway-class.openshift-ingress.svc.cluster.local`
2. **NodePort**, already allocated: `http://<node-ip>:31032`
3. **An OpenShift Route** to the gateway Service — gives a real hostname under
   `apps.ocp.paladinaura.com` using the existing wildcard cert, no MetalLB.
4. **MetalLB `IPAddressPool` + `L2Advertisement`** over a reserved address on
   the node subnet (`10.241.0.0/24`). The only option that makes the Gateway
   report `Programmed=True`, and the closest to a cloud environment.
