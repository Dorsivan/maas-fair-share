#!/bin/bash
# Open-loop Poisson-arrival load generator for UNI-34 (C3).
#
# Wraps 13-loadgen-poisson.py: fetches the MaaS subscription keys and the EPP
# metrics-reader token from the cluster, runs the generator against the
# public Route (same path UNI-27 validated), and snapshots
# llm_d_epp_maas_fairness_* before and after so the run's OWN contribution
# (dispatch_total, contended_service_tokens_total, newcomer_clamps_total
# deltas) can be read off, not just the cumulative total.
#
# Prerequisites:
#   - OPENSHIFT_TOKEN env var with read access to maas-fairness-poc.
#   - `oc` and `python3` on PATH.
#   - deploy/rbac.yaml already applied (mints the /metrics reader token).
#
# Usage:
#   OPENSHIFT_TOKEN=... RATE_APP1=4 RATE_APP2=4 RATE_END_USERS=4 DURATION=240 \
#     ./13-loadgen-poisson.sh
#
# Overrides: GW, MODELPATH, DURATION, RATE_APP1, RATE_APP2, RATE_END_USERS,
# SEED, OUT, NAMESPACE.
set -euo pipefail

NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
GW="${GW:-https://maas-gateway-${NAMESPACE}.apps.ocp.paladinaura.com}"
MODELPATH="${MODELPATH:-/maas-fairness-poc/maas-vllm-gpu}"
DURATION="${DURATION:-240}"
RATE_APP1="${RATE_APP1:-0}"
RATE_APP2="${RATE_APP2:-0}"
RATE_END_USERS="${RATE_END_USERS:-0}"
SEED="${SEED:-1}"
OUT="${OUT:-/tmp/poisson-codes-$(date +%s)}"
MAX_WORKERS="${MAX_WORKERS:-1000}"
DRAIN_TIMEOUT="${DRAIN_TIMEOUT:-100}"
EPP_METRICS_SVC_IP="${EPP_METRICS_SVC_IP:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OC="oc --token=${OPENSHIFT_TOKEN:?set OPENSHIFT_TOKEN} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"

KEYS="$(mktemp -d)"
trap 'rm -rf "$KEYS"' EXIT
for k in app1-production app2-batch end-user-alpha end-user-beta; do
  $OC get secret maas-loadgen-keys -n "$NAMESPACE" -o jsonpath="{.data.$k}" | base64 -d > "$KEYS/$k"
done

METRICS_TOKEN="$($OC get secret maas-epp-metrics-reader-token -n "$NAMESPACE" -o jsonpath='{.data.token}' | base64 -d)"
if [ -z "$EPP_METRICS_SVC_IP" ]; then
  EPP_METRICS_SVC_IP="$($OC get svc -n "$NAMESPACE" -l app.kubernetes.io/name=maas-vllm-gpu -o jsonpath='{.items[0].spec.clusterIP}' 2>/dev/null || true)"
fi
if [ -z "$EPP_METRICS_SVC_IP" ]; then
  EPP_METRICS_SVC_IP="$($OC get svc maas-vllm-gpu-epp-service -n "$NAMESPACE" -o jsonpath='{.spec.clusterIP}')"
fi

snapshot_metrics() {
  curl -sS -m 10 -H "Authorization: Bearer $METRICS_TOKEN" "http://${EPP_METRICS_SVC_IP}:9090/metrics" \
    | grep '^llm_d_epp_maas_fairness_' | grep -v '^#'
}

echo "=== metrics snapshot: before ==="
BEFORE="$(snapshot_metrics)"
echo "$BEFORE"

mkdir -p "$OUT"
python3 "$SCRIPT_DIR/13-loadgen-poisson.py" \
  --gw "$GW" --modelpath "$MODELPATH" --duration "$DURATION" \
  --rate-app1 "$RATE_APP1" --rate-app2 "$RATE_APP2" --rate-end-users "$RATE_END_USERS" \
  --key-app1 "$KEYS/app1-production" --key-app2 "$KEYS/app2-batch" \
  --key-end-alpha "$KEYS/end-user-alpha" --key-end-beta "$KEYS/end-user-beta" \
  --out "$OUT" --seed "$SEED" --max-workers "$MAX_WORKERS" --drain-timeout "$DRAIN_TIMEOUT"

echo "=== metrics snapshot: after ==="
AFTER="$(snapshot_metrics)"
echo "$AFTER"

echo "$BEFORE" > "$OUT/metrics-before.txt"
echo "$AFTER" > "$OUT/metrics-after.txt"

echo "=== delta (after - before), this run's contribution ==="
python3 "$SCRIPT_DIR/13-loadgen-poisson-delta.py" "$OUT/metrics-before.txt" "$OUT/metrics-after.txt" | tee "$OUT/delta.txt"

echo "=== run output directory: $OUT ==="
