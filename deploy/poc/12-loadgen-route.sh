#!/bin/bash
# Route-path closed-loop load generator for UNI-27 (A2).
#
# 04-loadgen.yaml drives load through the in-cluster gateway Service --
# the "LLMInferenceService path". This script drives the SAME closed-loop
# generator through the public Route instead:
#   https://maas-gateway-<namespace>.apps.ocp.paladinaura.com
# so the fairness behaviour is exercised end-to-end the way an external
# caller actually reaches it (HAProxy edge termination -> Service -> Envoy
# gateway -> EPP ext_proc -> backend), not just the in-cluster hop.
#
# Run from any host that can reach the Route (inside the cluster subnet, or
# the operator's workstation). It is NOT a Job manifest because the whole
# point is to originate from outside the gateway Service's ClusterIP.
#
# Prerequisites:
#   - OPENSHIFT_TOKEN env var with read access to maas-fairness-poc.
#   - `oc` on PATH.
#
# Usage:
#   OPENSHIFT_TOKEN=... ./12-loadgen-route.sh
# Overrides (same semantics as 04-loadgen.yaml):
#   GW, MODELPATH, DURATION, WORKERS, WORKERS_<TOKEN> (WORKERS_APP1,
#   WORKERS_END_USERS, ...), TENANTS, OUT
# Tenants (UNI-305): TENANT_MANIFEST names the tenant set, default
# deploy/poc/tenants/default.tenants (app1/app2/end-users). TENANTS picks a
# subset of it; unset = all of it. A group's worker count is WORKERS_<TOKEN>,
# else the manifest's workers column, else WORKERS.
set -euo pipefail

NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
GW="${GW:-https://maas-gateway-${NAMESPACE}.apps.ocp.paladinaura.com}"
MODELPATH="${MODELPATH:-/${NAMESPACE}/maas-vllm-gpu}"
DURATION="${DURATION:-240}"
WORKERS="${WORKERS:-32}"
OUT="${OUT:-/tmp/route-codes}"

OC="oc --token=${OPENSHIFT_TOKEN:?set OPENSHIFT_TOKEN} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"
TENANT_MANIFEST="${TENANT_MANIFEST:-$(dirname "$0")/tenants/default.tenants}"
TENANTS_PY="$(dirname "$0")/tenants.py"

# group -> "workers keys" from the manifest, workers resolved per the header.
declare -A G_WORKERS G_KEYS
ALL_GROUPS=()
SPECS="$(python3 -I "$TENANTS_PY" loadgen-groups "$TENANT_MANIFEST")"   # a bad manifest exits here
for spec in $SPECS; do
  IFS=: read -r g w keys <<< "$spec"
  tok="${g^^}"; tok="${tok//[^A-Z0-9]/_}"
  v="WORKERS_$tok"
  ALL_GROUPS+=("$g")
  G_WORKERS[$g]="${!v:-${w:-$WORKERS}}"
  G_KEYS[$g]="${keys//,/ }"
done
TENANTS="${TENANTS:-${ALL_GROUPS[*]}}"
for t in $TENANTS; do
  [ -n "${G_KEYS[$t]+set}" ] || { echo "unknown tenant: $t (not in $TENANT_MANIFEST)" >&2; exit 1; }
done

KEYS="$(mktemp -d)"
trap 'rm -rf "$KEYS"' EXIT
for k in $(for t in $TENANTS; do echo ${G_KEYS[$t]}; done | awk '!seen[$0]++'); do
  $OC get secret maas-loadgen-keys -n "$NAMESPACE" -o jsonpath="{.data.$k}" | base64 -d > "$KEYS/$k"
done

END=$(( $(date +%s) + DURATION ))
PROMPT=""
for _ in $(seq 1 300); do PROMPT="${PROMPT}the quick brown fox "; done
mkdir -p "$OUT"

worker() {
  local sub="$1" group="$2" out
  while [ "$(date +%s)" -lt "$END" ]; do
    out=$(curl -sS -o /dev/null -m 300 -w '%{http_code} %{time_total}' -X POST "$GW$MODELPATH/v1/chat/completions" \
      -H 'Content-Type: application/json' \
      -H "Authorization: Bearer $(cat "$KEYS/$sub")" \
      -d "{\"model\":\"llama-3-1-8b\",\"max_tokens\":64,\"messages\":[{\"role\":\"user\",\"content\":\"$PROMPT\"}]}" \
      2>/dev/null) || out="000 0"
    echo "$out" >> "$OUT/$group"
  done
}

WORKERS_LINE=""
for g in "${ALL_GROUPS[@]}"; do WORKERS_LINE="$WORKERS_LINE $g=${G_WORKERS[$g]}"; done
echo "load: GW=$GW tenants=[${TENANTS}] workers${WORKERS_LINE} duration=${DURATION}s"

# A group with several keys round-robins them across its workers: worker i
# sends with key (i mod n) -- for end-users' alpha,beta that is the original
# even=alpha / odd=beta split.
for t in $TENANTS; do
  read -r -a keys <<< "${G_KEYS[$t]}"
  for i in $(seq 1 "${G_WORKERS[$t]}"); do
    worker "${keys[$(( i % ${#keys[@]} ))]}" "$t" &
  done
done
wait

echo "load: done."
printf '%-12s %-7s %-9s %-9s %s\n' TENANT TOTAL P50_SEC P95_SEC STATUSES
for f in "$OUT"/*; do
  n=$(wc -l < "$f")
  stats=$(awk '{print $2}' "$f" | sort -n | awk -v n="$n" '
    {a[NR]=$1}
    END{ p50=a[int(NR*0.50)+0>0?int(NR*0.50):1]; p95=a[int(NR*0.95)+0>0?int(NR*0.95):1];
         printf "%.2f %.2f", p50, p95 }')
  codes=$(awk '{print $1}' "$f" | sort | uniq -c | sort -rn | awk '{printf "%s=%s ", $2, $1}')
  printf '%-12s %-7s %-9s %-9s %s\n' "$(basename "$f")" "$n" $stats "$codes"
done
echo "A run is only meaningful if the statuses are overwhelmingly 200."
