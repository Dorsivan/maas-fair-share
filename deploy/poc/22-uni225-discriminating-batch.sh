#!/bin/bash
# UNI-225 (F5, Zeratul review): drives the six `-discriminating` sibling
# scenarios 15-fairness-benchmark.sh's own usage line already understands
# (app1-idle-discriminating, app2-idle-discriminating, app2-trickle-
# discriminating, end-users-idle-discriminating, full-contention-
# discriminating, full-contention-2x-discriminating) back-to-back, one GPU
# batch, restoring `enforce` to its steady-state `false` between runs and
# waiting for any in-flight `maas-loadgen` Job before starting the next so
# this never overlaps another ticket's use of the shared GPU pool.
#
# This is a reconstruction, not the literal script the original UNI-225 run
# used. That script wrote its log under a session-scoped $TMPDIR, which was
# torn down when the launching session ended before the script could be
# committed -- the exact "$TMPDIR can vanish when the launching session
# ends" hazard docs/poc-results.md's UNI-218 section already documents for a
# different run in this same series. The six runs' own results (reported in
# docs/poc-results.md's UNI-225 section) are unaffected -- only the driver
# script itself was lost. This version fixes that by living in the repo
# working tree from the start, per this chain's standing run-hygiene
# instruction ("write scratch files under the repo working tree, never
# $TMPDIR").
#
# Usage:
#   OPENSHIFT_TOKEN=... ./22-uni225-discriminating-batch.sh
#
# Prerequisites: same as 15-fairness-benchmark.sh -- OPENSHIFT_TOKEN with
# write access to maas-fairness-poc (ENFORCE_LIVE patches maas-epp-config),
# `oc`/`python3` on PATH, deploy/rbac.yaml already applied, cluster at the
# documented baseline (enforce: false, queueDepthThreshold: 32, weights
# 20/10/65/5, queue-scorer/prefix-cache-scorer 3.0/3.0) before starting.
#
# Overrides: NAMESPACE (default maas-fairness-poc), DURATION (default 240,
# matching every other run in this section), SCENARIOS (default the six
# below, space-separated "scenario:label" pairs, override to re-run a subset).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
DURATION="${DURATION:-240}"
JOB_NAME="maas-loadgen"

# Scratch/log output lives under the repo working tree, not $TMPDIR -- see
# the header comment above for why that matters for a long-running batch.
LOG_DIR="${LOG_DIR:-$SCRIPT_DIR/../../results}"
mkdir -p "$LOG_DIR"
BATCH_LOG="$LOG_DIR/uni225-batch-$(date -u +%Y%m%dT%H%M%SZ).log"

SCENARIOS="${SCENARIOS:-app1-idle-discriminating:app1-idle-discriminating app2-idle-discriminating:app2-idle-discriminating app2-trickle-discriminating:app2-trickle-discriminating end-users-idle-discriminating:end-users-idle-discriminating full-contention-discriminating:full-contention-discriminating full-contention-2x-discriminating:full-contention-2x-discriminating}"

log() {
  echo "[uni225-batch] $(date -u +%H:%M:%S) $*" | tee -a "$BATCH_LOG"
}

wait_for_no_active_job() {
  while true; do
    active="$(oc get job "$JOB_NAME" -n "$NAMESPACE" -o jsonpath='{.status.active}' 2>/dev/null || true)"
    if [ -z "$active" ] || [ "$active" = "0" ]; then
      return 0
    fi
    log "waiting: job/$JOB_NAME still active in $NAMESPACE (shared GPU pool, UNI-225 chain runs one ticket at a time)"
    sleep 15
  done
}

confirm_enforce_false() {
  current="$(oc get configmap maas-epp-config -n "$NAMESPACE" -o jsonpath='{.data.epp}' 2>/dev/null | grep -m1 'enforce:' | awk '{print $2}' || true)"
  if [ "$current" != "false" ]; then
    log "WARNING: enforce is '$current' after a run, expected 'false' -- this is the same \$TMPDIR-scoped-restore hazard UNI-218 hit. Not continuing the batch with enforce stuck on."
    log "manual fix required: oc edit configmap maas-epp-config -n $NAMESPACE, set enforce: false, then re-run the remaining scenarios"
    exit 1
  fi
}

log "starting UNI-225 discriminating batch, ${DURATION}s per run, log: $BATCH_LOG"

for pair in $SCENARIOS; do
  scenario="${pair%%:*}"
  label="${pair##*:}"
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
done

log "batch complete: ${SCENARIOS}"
log "confirm the final cluster state by hand (enforce: false, queueDepthThreshold: 32, weights 20/10/65/5, queue-scorer/prefix-cache-scorer 3.0/3.0) before reporting results"
