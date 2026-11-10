#!/bin/bash
# UNI-228: drives the five new equal-weight `-discriminating` sibling
# scenarios 15-fairness-benchmark.sh's own usage line already understands
# (uni165-equal-discriminating, uni165-subset-3-idle-discriminating,
# uni165-equal-2x-discriminating, uni165-graded-discriminating,
# twenty-group-scale-discriminating) back-to-back, one GPU batch -- the
# equal-weight mirror of UNI-225's 22-uni225-discriminating-batch.sh.
#
# Unlike UNI-225's siblings, four of these five scenarios need a non-default
# EPP groups table (deploy/poc/epp-groups/render.py), which RECREATES BOTH
# EPPs (CPU and GPU share maas-epp-config) and zeroes their per-group
# counters -- see docs/runbook.md "EPP tables". Grouped below so the table is
# swapped only twice (equal, graded), restored to the 3-group default once at
# the very end. twenty-group-scale-discriminating needs its own 20-group
# table and is scheduled last so the 6-group table is only ever live for the
# three 6-group `equal`-table runs plus the one `graded`-table run.
#
# Usage:
#   OPENSHIFT_TOKEN=... ./23-uni228-discriminating-batch.sh
#
# Prerequisites: same as 15-fairness-benchmark.sh -- OPENSHIFT_TOKEN with
# write access to maas-fairness-poc (ENFORCE_LIVE and the table swaps below
# both patch maas-epp-config), `oc`/`python3` on PATH, deploy/rbac.yaml and
# deploy/maas/08-tenants.yaml (app3-20 subscriptions, docs/runbook.md
# "N-group identities and EPP tables") already applied, cluster at the
# documented baseline (enforce: false, queueDepthThreshold: 32, weights
# 20/10/65/5, queue-scorer/prefix-cache-scorer 3.0/3.0) before starting.
#
# Overrides: NAMESPACE (default maas-fairness-poc), DURATION (default 240,
# matching every other run in this section).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
DURATION="${DURATION:-240}"
JOB_NAME="maas-loadgen"
OC="oc --token=${OPENSHIFT_TOKEN:?} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"
GPU_SELECTOR="app.kubernetes.io/name=maas-vllm-gpu,app.kubernetes.io/component=llminferenceservice-router-scheduler"

# Scratch/log output lives under the repo working tree, not $TMPDIR -- see
# process_tmpdir_torn_down_mid_background_run / UNI-225's own batch script
# header for why that matters for a long-running batch.
LOG_DIR="${LOG_DIR:-$SCRIPT_DIR/../../results}"
mkdir -p "$LOG_DIR"
BATCH_LOG="$LOG_DIR/uni228-batch-$(date -u +%Y%m%dT%H%M%SZ).log"

log() {
  echo "[uni228-batch] $(date -u +%H:%M:%S) $*" | tee -a "$BATCH_LOG"
}

wait_for_no_active_job() {
  while true; do
    active="$($OC get job "$JOB_NAME" -n "$NAMESPACE" -o jsonpath='{.status.active}' 2>/dev/null || true)"
    if [ -z "$active" ] || [ "$active" = "0" ]; then
      return 0
    fi
    log "waiting: job/$JOB_NAME still active in $NAMESPACE (shared GPU pool, one ticket at a time)"
    sleep 15
  done
}

confirm_enforce_false() {
  current="$($OC get configmap maas-epp-config -n "$NAMESPACE" -o jsonpath='{.data.epp}' 2>/dev/null | grep -m1 'enforce:' | awk '{print $2}' || true)"
  if [ "$current" != "false" ]; then
    log "WARNING: enforce is '$current' after a run, expected 'false' -- same stuck-enforce hazard UNI-218/UNI-227 hit. Not continuing with enforce stuck on."
    log "manual fix required: oc patch configmap maas-epp-config -n $NAMESPACE --type=merge -p '{\"data\":{...enforce: false...}}' (or re-apply the live config), then re-run the remaining scenarios"
    exit 1
  fi
}

gpu_epp_pod() {
  $OC get pods -n "$NAMESPACE" -l "$GPU_SELECTOR" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true
}

# Waits for a NEW GPU EPP pod (different name from $1, the pod captured
# before the ConfigMap apply) to appear, report Ready, and expose
# configured_weight for at least $2 fairness groups. A pod-name check (not
# just a group-count check) matters because two different weight tables
# (equal vs graded) can have the identical group count -- a count-only check
# would pass instantly against the OLD pod's still-live metrics before it
# actually restarts.
wait_for_new_table() {
  local old_pod="$1" want="$2" timeout="${3:-600}"
  local deadline=$(( $(date +%s) + timeout ))
  local metrics_token gpu_ip
  metrics_token="$($OC get secret maas-epp-metrics-reader-token -n "$NAMESPACE" -o jsonpath='{.data.token}' | base64 -d)"
  gpu_ip="$($OC get svc maas-vllm-gpu-epp-service -n "$NAMESPACE" -o jsonpath='{.spec.clusterIP}')"
  while :; do
    local pod cw ready
    pod="$(gpu_epp_pod)"
    if [ -n "$pod" ] && [ "$pod" != "$old_pod" ]; then
      cw="$(curl -sS -m 10 -H "Authorization: Bearer $metrics_token" "http://$gpu_ip:9090/metrics" 2>/dev/null \
        | grep -c '^llm_d_epp_maas_fairness_configured_weight{' || true)"
      ready="$($OC get pod "$pod" -n "$NAMESPACE" -o jsonpath='{.status.containerStatuses[0].ready}' 2>/dev/null || true)"
      if [ "$cw" -ge "$want" ] && [ "$ready" = "true" ]; then
        log "table live: new pod=$pod cw=$cw ready"
        return 0
      fi
    fi
    if [ "$(date +%s)" -ge "$deadline" ]; then
      log "TIMEOUT waiting for new table (old_pod=$old_pod current_pod=$pod)"
      return 1
    fi
    sleep 10
  done
}

apply_table() {
  local desc="$1" want="$2"; shift 2
  log "=== applying EPP table: $desc ==="
  local old_pod; old_pod="$(gpu_epp_pod)"
  python3 -I "$SCRIPT_DIR/epp-groups/render.py" "$@" | $OC apply -f - | tee -a "$BATCH_LOG"
  wait_for_new_table "$old_pod" "$want" || exit 1
}

restore_default_table() {
  log "=== restoring default 3-group table ==="
  local old_pod; old_pod="$(gpu_epp_pod)"
  $OC apply -f "$SCRIPT_DIR/00-config.yaml" | tee -a "$BATCH_LOG"
  wait_for_new_table "$old_pod" 3 || log "WARNING: restore readiness check timed out -- verify maas-epp-config by hand"
}
trap restore_default_table EXIT

run() {
  local scenario="$1" label="$2"
  log "=== $label ==="
  wait_for_no_active_job
  if ! DURATION="$DURATION" ENFORCE_LIVE=true NAMESPACE="$NAMESPACE" \
      "$SCRIPT_DIR/15-fairness-benchmark.sh" "$scenario" "$label" 2>&1 | tee -a "$BATCH_LOG"; then
    log "FAIL: $label did not complete -- checking cluster state before stopping (does not re-run automatically)"
    confirm_enforce_false
    exit 1
  fi
  confirm_enforce_false
  log "=== $label done ==="
}

log "starting UNI-228 discriminating batch, ${DURATION}s per run, log: $BATCH_LOG"

# --- equal 6-group table: equal, subset-3-idle, equal-2x share it ----------
apply_table "6-group equal" 6 6
run uni165-equal-discriminating         uni-228-uni165-equal-discriminating
run uni165-subset-3-idle-discriminating uni-228-uni165-subset-3-idle-discriminating
run uni165-equal-2x-discriminating      uni-228-uni165-equal-2x-discriminating

# --- 6-group graded table ---------------------------------------------------
apply_table "6-group graded" 6 6 --weights graded
run uni165-graded-discriminating        uni-228-uni165-graded-discriminating

# --- 20-group equal table ---------------------------------------------------
apply_table "20-group equal" 20 20
run twenty-group-scale-discriminating   uni-228-twenty-group-scale-discriminating

log "batch complete"
log "confirm the final cluster state by hand (enforce: false, 3-group 20/10/65/5 table, queueDepthThreshold: 32, queue-scorer/prefix-cache-scorer 3.0/3.0) before reporting results"
