#!/bin/bash
# UNI-231: stand up one ADDITIONAL POC lane (lane 2 or 3) -- the same stack as
# maas-fairness-poc, under the same object names, in its own namespace and on
# its own pair of GPU nodes. Lane table and naming rules: deploy/poc/lanes.py.
#
#   NAMESPACE=poc-maas-lane2 deploy/poc/25-provision-lane.sh
#
# Idempotent: every step checks before it creates, so a re-run after fixing
# whatever stopped it continues from there. It refuses lane 1 outright --
# instance 1 is never (re)provisioned from here.
#
# What it needs, and from whom (verified by SubjectAccessReview, UNI-231):
#   * the namespace itself                  operator (Khala never creates one)
#   * `edit` in the namespace               everything below except...
#   * gateways create in the namespace      ...the Gateway (poc-agent, per the
#                                           board's UNI-231 decision)
#   * maassubscriptions/maasauthpolicies    the lane's tenants, CREATE only --
#     create in models-as-a-service         never patch: lane 1's live policies
#                                           are compiled from the existing ones
#   * get on secret/quay-maas-pull in       the private EPP image's pull
#     maas-fairness-poc (read only)         secret, copied once per lane
# A step whose permission is missing stops the script with the exact command
# for whoever holds it; nothing is worked around.
#
# Remediation is a load event: creating the LLMInferenceService starts two
# ~15 GB model downloads over the cluster's egress. Run it between instance-1
# measurement runs, not during one.
set -euo pipefail

: "${NAMESPACE:?set NAMESPACE to the lane to provision (poc-maas-lane2 or poc-maas-lane3)}"
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
OC="oc --token=${OPENSHIFT_TOKEN:?} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"
# a bare eval "$(...)" would swallow an unknown-lane error under set -e
LANE_ENV="$(NAMESPACE="$NAMESPACE" python3 -I "$HERE/lanes.py" env)"
eval "$LANE_ENV"
[ "$LANE" != 1 ] || { echo "refusing: $NAMESPACE is lane 1 (instance 1); this script only builds new lanes" >&2; exit 2; }
WORK="$REPO/.lane-provision/$NAMESPACE"   # repo tree, never $TMPDIR (UNI-218)
mkdir -p "$WORK"
TENANTS="$WORK/tenants.yaml"
render() { NAMESPACE="$NAMESPACE" python3 -I "$HERE/lanes.py" render "$@"; }
log() { echo "$(date -u +%H:%M:%SZ) [lane$LANE] $*"; }
stop() { log "STOP: $1"; [ -n "${2:-}" ] && echo "    needs: $2"; exit 3; }
can() { $OC auth can-i "$@" >/dev/null 2>&1; }

log "identity: $($OC whoami) | namespace: $NAMESPACE | GPU nodes: $LANE_GPU_NODES | tenant suffix: $LANE_SUFFIX"
$OC get namespace "$NAMESPACE" >/dev/null 2>&1 \
  || stop "namespace $NAMESPACE does not exist" "operator: create namespace $NAMESPACE"
can create llminferenceservices.serving.kserve.io -n "$NAMESPACE" \
  || stop "no write access in $NAMESPACE" "operator: RoleBinding $($OC whoami) -> ClusterRole edit in $NAMESPACE"

# 1. Gateway: same spec as lane 1's (03-gateway.yaml), its own Envoy pods and
#    MetalLB address. The LLMInferenceService's HTTPRoute attaches to it.
if $OC get gateway.gateway.networking.k8s.io maas-poc-gateway -n "$NAMESPACE" >/dev/null 2>&1; then
  log "gateway: present"
elif can create gateways.gateway.networking.k8s.io -n "$NAMESPACE"; then
  render --kind Gateway "$HERE/03-gateway.yaml" | $OC create -n "$NAMESPACE" -f - >/dev/null
  log "gateway: created"
else
  stop "gateway maas-poc-gateway missing, and this identity cannot create it" \
    "poc-agent: NAMESPACE=$NAMESPACE python3 -I deploy/poc/lanes.py render --kind Gateway deploy/poc/03-gateway.yaml | oc create -n $NAMESPACE -f -"
fi

# 2. Pull secret for the private EPP image. Copied (data only) from lane 1;
#    the link to the EPP's ServiceAccount is step 5 -- it is per-SA.
if $OC get secret quay-maas-pull -n "$NAMESPACE" >/dev/null 2>&1; then
  log "pull secret: present"
elif can get secrets -n maas-fairness-poc; then
  $OC get secret quay-maas-pull -n maas-fairness-poc -o json | python3 -I -c '
import json, sys
s = json.load(sys.stdin)
print(json.dumps({"apiVersion": "v1", "kind": "Secret", "type": s["type"],
                  "metadata": {"name": "quay-maas-pull"}, "data": s["data"]}))
' | $OC create -n "$NAMESPACE" -f - >/dev/null
  log "pull secret: copied from maas-fairness-poc"
else
  stop "secret quay-maas-pull missing, and this identity cannot read lane 1's copy" \
    "a break-glass window (secret read), or the Engineer: docs/runbook.md 'Rebuild and publish the EPP image' -n $NAMESPACE"
fi

# 3. The lane's OWN maas-epp-config, at the committed baseline (enforce false,
#    threshold 32, 20/10/65/5) with this lane's suffixed match values.
render "$HERE/00-config.yaml" | $OC apply -n "$NAMESPACE" -f - >/dev/null
log "maas-epp-config: applied (baseline)"

# 4. The model server + EPP, pinned to this lane's GPU pair.
render "$HERE/09-vllm-gpu.yaml" | $OC apply -n "$NAMESPACE" -f - >/dev/null
log "llminferenceservice maas-vllm-gpu: applied"

# 5. Link the pull secret to the EPP's auto-created ServiceAccount. Until it
#    exists there is nothing to link; poll, printing each time.
for i in $(seq 1 30); do
  $OC get sa maas-vllm-gpu-epp-sa -n "$NAMESPACE" >/dev/null 2>&1 && break
  log "[$i/30] waiting for sa/maas-vllm-gpu-epp-sa"; sleep 10
done
if $OC get sa maas-vllm-gpu-epp-sa -n "$NAMESPACE" -o jsonpath='{.imagePullSecrets[*].name}' | grep -qw quay-maas-pull; then
  log "pull secret: already linked to maas-vllm-gpu-epp-sa"
else
  $OC secrets link maas-vllm-gpu-epp-sa quay-maas-pull --for=pull -n "$NAMESPACE"
  # An EPP pod created before the link is stuck in ImagePullBackOff; the
  # Deployment recreates it with the secret.
  $OC delete pod -n "$NAMESPACE" -l app.kubernetes.io/component=llminferenceservice-router-scheduler --ignore-not-found >/dev/null
  log "pull secret: linked; EPP pod recycled"
fi

# 6. Route -> maas-gateway-$NAMESPACE.apps... (the harness derives this host).
render "$HERE/08-route.yaml" | $OC apply -n "$NAMESPACE" -f - >/dev/null
log "route maas-gateway: applied"

# 7. MaaSModelRef, same spec as lane 1's live object.
$OC apply -n "$NAMESPACE" -f - >/dev/null << 'EOF'
apiVersion: maas.opendatahub.io/v1alpha1
kind: MaaSModelRef
metadata: {name: maas-vllm-gpu}
spec:
  modelRef: {kind: LLMInferenceService, name: maas-vllm-gpu}
EOF
log "maasmodelref maas-vllm-gpu: applied"

# 8. This lane's tenants. CREATE only: an existing object is left alone, so a
#    re-run can never modify a subscription some other lane depends on.
if can create maassubscriptions.maas.opendatahub.io -n models-as-a-service; then
  NAMESPACE="$NAMESPACE" python3 -I "$HERE/lanes.py" tenants > "$TENANTS"
  # oc exits non-zero if ANY object already exists; judge line by line.
  $OC create -f "$TENANTS" > "$TENANTS.out" 2>&1 || true
  sed -E 's/^Error from server \(AlreadyExists\).*"([^"]+)".*/present: \1/' "$TENANTS.out" \
    | while read -r l; do log "tenants: $l"; done
  if grep -v AlreadyExists "$TENANTS.out" | grep -q '^Error'; then
    stop "a tenant object failed to create (see above)"
  fi
else
  stop "cannot create MaaSSubscriptions in models-as-a-service" \
    "operator: Role (maassubscriptions, maasauthpolicies: get,list,watch,create) in models-as-a-service for $($OC whoami)"
fi

# 9. UNI-33/UNI-210: the controller generates maas-poc-gateway-authn once an
#    LLMInferenceService references the Gateway; strip the client-settable
#    objective header there, exactly as on lane 1.
for i in $(seq 1 30); do
  $OC get authpolicy maas-poc-gateway-authn -n "$NAMESPACE" >/dev/null 2>&1 && break
  log "[$i/30] waiting for authpolicy/maas-poc-gateway-authn"; sleep 10
done
$OC patch authpolicy maas-poc-gateway-authn -n "$NAMESPACE" --type=merge \
  --patch-file="$REPO/deploy/maas/09-objective-header-stripping.patch.yaml" >/dev/null
log "authpolicy maas-poc-gateway-authn: objective-header stripping applied"

# 10. Placement check -- the whole point of a lane. Model servers on this
#     lane's pair only; EPP and gateway on no GPU node at all.
log "placement:"
$OC get pods -n "$NAMESPACE" -o custom-columns=POD:.metadata.name,NODE:.spec.nodeName,PHASE:.status.phase --no-headers \
  | while read -r pod node phase; do
      verdict=ok
      case "$pod" in
        maas-vllm-gpu-kserve-router-scheduler*|maas-poc-gateway*) [[ "$node" == ocp-gpu-worker-* ]] && verdict="WRONG: on a GPU node" ;;
        maas-vllm-gpu-kserve-*) [[ " $LANE_GPU_NODES " == *" $node "* ]] || verdict="WRONG: not on $LANE_GPU_NODES" ;;
      esac
      log "  $pod  $node  $phase  $verdict"
    done
log "done. Next: mint keys (canonical names; stored per lane):"
echo "    NAMESPACE=$NAMESPACE MAAS_GROUP=maas-app1      deploy/maas/mint-loadgen-keys.sh app1-production"
echo "    NAMESPACE=$NAMESPACE MAAS_GROUP=maas-app2      deploy/maas/mint-loadgen-keys.sh app2-batch"
echo "    NAMESPACE=$NAMESPACE MAAS_GROUP=maas-end-users deploy/maas/mint-loadgen-keys.sh end-user-alpha end-user-beta"
echo "    NAMESPACE=$NAMESPACE MAAS_GROUP=maas-poc-users deploy/maas/mint-loadgen-keys.sh app3 app4 ... app20"
