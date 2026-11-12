#!/bin/bash
# UNI-226: patch all three `maas-epp-config` group weights (app1/app2/
# end-users) in a single ConfigMap edit, and wait for both EPPs that share
# it (GPU and CPU `router-scheduler`) to come back up reporting the new
# values via their own `llm_d_epp_maas_fairness_configured_weight` gauge.
#
# Why this exists: UNI-160/F3 needed exactly this ("patch the three group
# weights to an alternative set before the run starts") and did it with an
# uncommitted scratch script because none existed -- see
# docs/poc-results.md's "UNI-160: F3" section header, "Setup" paragraph:
# "[UNI-180]'s LIVE_SET_TARGET=epp-weight:<group> wrapper only ever changes
# ONE group per invocation, and this ticket needs all three changed together
# before the Job starts ... A one-off script (not committed; scratch
# orchestration only) ...". UNI-226 needs the same thing again, for the
# 98/1/1 equal-load prioritisation row, and twice more for its noise-floor
# repeat -- worth committing this time instead of re-losing it the way
# UNI-225's own batch driver was lost to an uncommitted $TMPDIR (see
# 22-uni225-discriminating-batch.sh's header).
#
# This does NOT restore the weights itself -- call it again with the
# baseline values (20 10 65) after the run, the same way the UNI-160/F3
# precedent did between cases. 15-fairness-benchmark.sh's own
# `confirm_enforce_false`-style discipline applies here too: verify the
# restore landed before starting the next ticket's run on the shared GPU
# pool.
#
# Usage:
#   OPENSHIFT_TOKEN=... ./24-patch-all-weights.sh <app1-weight> <app2-weight> <end-users-weight>
# Example (98/1/1 for UNI-226's prioritisation row):
#   OPENSHIFT_TOKEN=... ./24-patch-all-weights.sh 98 1 1
# Restore to baseline afterward:
#   OPENSHIFT_TOKEN=... ./24-patch-all-weights.sh 20 10 65
#
# Prerequisites: same as 15-fairness-benchmark.sh -- OPENSHIFT_TOKEN with
# write access to maas-fairness-poc, `oc`/`python3` on PATH, cluster
# reachable, no loadgen Job in flight (this changes live config under
# traffic exactly as unsafely as any other epp-weight edit would).
set -euo pipefail

NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
CONFIGMAP_NAME="maas-epp-config"
EPP_SELECTOR="${EPP_SELECTOR:-app.kubernetes.io/component=llminferenceservice-router-scheduler,app.kubernetes.io/name=maas-vllm-gpu}"
CPU_EPP_METRICS_SVC="${CPU_EPP_METRICS_SVC:-maas-vllm-cpu-epp-service}"
WAIT_TIMEOUT_SECONDS="${WAIT_TIMEOUT_SECONDS:-180}"
OC="${OC:-oc}"

W_APP1="${1:?usage: $0 <app1-weight> <app2-weight> <end-users-weight>}"
W_APP2="${2:?usage: $0 <app1-weight> <app2-weight> <end-users-weight>}"
W_END_USERS="${3:?usage: $0 <app1-weight> <app2-weight> <end-users-weight>}"

log() { echo "[patch-all-weights] $(date -u +%H:%M:%S) $*" >&2; }

# UNI-222: NOT $TMPDIR -- a background run's $TMPDIR is scoped to the
# launching session and can vanish out from under a backgrounded batch
# driver (nohup+disown) well before this script's own invocation runs,
# making `mktemp -d "$TMPDIR/..."` fail outright and silently skip the
# weight restore it was called to do (live on UNI-247's 4x-rep3 batch,
# 2026-11-12: "mktemp: failed to create directory ... No such file or
# directory", cluster left at 30/10/60). `results/` is already gitignored
# and lives in the repo working tree, which does not get torn down with
# any one session -- the same fix this project's standing run-hygiene rule
# already requires of every benchmark run's own scratch output.
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRATCH_DIR="$(mktemp -d "$REPO_ROOT/results/.patch-all-weights.XXXXXX")"
trap 'rm -rf "$SCRATCH_DIR"' EXIT

$OC get configmap "$CONFIGMAP_NAME" -n "$NAMESPACE" -o jsonpath='{.data.epp}' > "$SCRATCH_DIR/before.yaml"

python3 -I - "$SCRATCH_DIR/before.yaml" "$SCRATCH_DIR/after.yaml" \
  "$W_APP1" "$W_APP2" "$W_END_USERS" << 'PYEOF'
import re
import sys

src, dst, w_app1, w_app2, w_end_users = sys.argv[1:6]
text = open(src).read()

for group, val in (("app1", w_app1), ("app2", w_app2), ("end-users", w_end_users)):
    pat = re.compile(r"(\{\s*name:\s*" + re.escape(group) + r",\s*weight:\s*)[0-9.]+")
    text, n = pat.subn(lambda m: m.group(1) + val, text, count=1)
    if n == 0:
        sys.exit(f"group {group}: weight entry not found in maas-epp-config's data.epp")

open(dst, "w").write(text)
PYEOF

log "patching $CONFIGMAP_NAME: app1=$W_APP1 app2=$W_APP2 end-users=$W_END_USERS"
$OC patch configmap "$CONFIGMAP_NAME" -n "$NAMESPACE" --type=merge \
  -p "$(python3 -I -c "
import json
print(json.dumps({'data': {'epp': open('$SCRATCH_DIR/after.yaml').read()}}))
")" > /dev/null

# A ConfigMap edit to this key has no live-reload path -- both EPPs that
# mount it (GPU and CPU router-scheduler) get recreated under a new pod
# name, same mechanism UNI-174 measured for `enforce` (15-fairness-
# benchmark.sh's live_set_target_recreates_pod). Wait for the
# `configured_weight` gauge itself to read the new values on both, rather
# than just a pod-name change or Ready -- the authoritative "the new config
# is actually being served" signal, not a proxy for it.
METRICS_TOKEN="$($OC get secret maas-epp-metrics-reader-token -n "$NAMESPACE" -o jsonpath='{.data.token}' | base64 -d)"
GPU_SVC_IP="$($OC get svc maas-vllm-gpu-epp-service -n "$NAMESPACE" -o jsonpath='{.spec.clusterIP}')"
CPU_SVC_IP="$($OC get svc "$CPU_EPP_METRICS_SVC" -n "$NAMESPACE" -o jsonpath='{.spec.clusterIP}')"

read_weight() {
  # $1 = metrics ClusterIP, $2 = fairness_id. Prints the live gauge value,
  # or nothing if the scrape failed or the series is absent (fresh pod
  # still starting -- its metric registry is empty until the plugin's
  # Start() runs).
  curl -sS -m 10 -H "Authorization: Bearer $METRICS_TOKEN" "http://$1:9090/metrics" 2>/dev/null \
    | awk -v fid="$2" '$0 ~ "^llm_d_epp_maas_fairness_configured_weight\\{.*fairness_id=\"" fid "\"" {print $2}'
}

wait_for_weights() {
  local svc_ip="$1" label="$2" waited=0 a1 a2 eu
  while :; do
    a1="$(read_weight "$svc_ip" app1)"
    a2="$(read_weight "$svc_ip" app2)"
    eu="$(read_weight "$svc_ip" end-users)"
    if [ "$a1" = "$W_APP1" ] && [ "$a2" = "$W_APP2" ] && [ "$eu" = "$W_END_USERS" ]; then
      log "confirmed on $label: configured_weight app1=$a1 app2=$a2 end-users=$eu"
      return 0
    fi
    if [ "$waited" -ge "$WAIT_TIMEOUT_SECONDS" ]; then
      log "WARNING: timed out after ${WAIT_TIMEOUT_SECONDS}s waiting for $label to report app1=$W_APP1 app2=$W_APP2 end-users=$W_END_USERS (last read: app1=${a1:-?} app2=${a2:-?} end-users=${eu:-?})"
      return 1
    fi
    sleep 2
    waited=$((waited + 2))
  done
}

rc=0
wait_for_weights "$GPU_SVC_IP" "GPU EPP" || rc=1
wait_for_weights "$CPU_SVC_IP" "CPU EPP" || rc=1

if [ "$rc" -ne 0 ]; then
  log "FATAL: one or both EPPs did not confirm the new weights within ${WAIT_TIMEOUT_SECONDS}s -- not safe to start a scored run against this config"
  exit 1
fi

log "done: both EPPs confirmed app1=$W_APP1 app2=$W_APP2 end-users=$W_END_USERS"
