#!/bin/bash
# D5 (UNI-46): archive the GPU EPP's own container log as a per-run artifact
# alongside the load harness's own status/latency table, instead of depending
# on a log retention window this cluster does not have.
#
# This wraps 04-loadgen.yaml; it does not change what it sends. Read the
# comments there before touching TENANTS/WORKERS -- the sizing reasoning is
# load-bearing (under-offered load produces a confident wrong answer, see
# docs/poc-results.md).
#
# Capture is bounded: it starts right before the Job is created and stops
# right after the Job finishes. If the target pod restarts mid-run, `oc logs
# -f` silently stops following -- the old container's stream ended, it does
# not reconnect to the new one. This script detects that (the follow process
# exits before the run is over), records the restart in the manifest instead
# of losing it silently, and reattaches -f to pick up the rest of the run.
#
# Scope: GPU path only (board direction, 2026-10-19). EPP_SELECTOR below
# targets the LLMInferenceService-managed scheduler pod
# (maas-vllm-gpu-kserve-router-scheduler-*), not the simulator's 02-epp.yaml
# Deployment.
#
# Prerequisites:
#   - OPENSHIFT_TOKEN env var with edit access to maas-fairness-poc.
#   - `oc` on PATH.
#
# Usage:
#   OPENSHIFT_TOKEN=... ./deploy/poc/14-loadgen-with-log-archive.sh [label]
#
# Overrides (same semantics and defaults as 04-loadgen.yaml; applied to a
# patched copy of the manifest -- the checked-in file is never modified):
#   TENANTS, WORKERS, DURATION
# The per-tenant WORKERS_APP1/APP2/END_USERS overrides are commented out in
# the base manifest (asymmetric-demand etc.) -- naming and selecting those
# scenarios is UNI-54's job, not this one. Edit 04-loadgen.yaml directly for
# those runs, same as before this script existed.
#
# UNI-174: the log-capture cleanup trap now covers SIGINT/SIGTERM/SIGHUP, not
# just normal/EXIT, and stays armed for the whole script (no more `trap -
# EXIT` partway through) -- see the trap registration below for why. This
# script has no other live-cluster state to revert: it leaves the completed
# Job in place (deleted by the next invocation's own `--ignore-not-found`
# cleanup, same as before) and never touches maas-epp-config or replica
# counts.
set -euo pipefail

NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
OC="oc --token=${OPENSHIFT_TOKEN:?set OPENSHIFT_TOKEN} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"
EPP_SELECTOR="${EPP_SELECTOR:-app.kubernetes.io/component=llminferenceservice-router-scheduler,app.kubernetes.io/name=maas-vllm-gpu}"
EPP_CONTAINER="${EPP_CONTAINER:-main}"
JOB_NAME="maas-loadgen"
LABEL="${1:-run}"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
ARTIFACT_DIR="$(pwd)/results/${TS}-${LABEL}"
MANIFEST_FILE="$ARTIFACT_DIR/manifest.json"
EPP_LOG="$ARTIFACT_DIR/epp-container.log"
LOADGEN_LOG="$ARTIFACT_DIR/loadgen.log"
mkdir -p "$ARTIFACT_DIR"
echo "[archive] artifact dir: $ARTIFACT_DIR"

# --- Resolve manifest with any env overrides ------------------------------
SRC="$(dirname "$0")/04-loadgen.yaml"
PATCHED="$ARTIFACT_DIR/04-loadgen.patched.yaml"
cp "$SRC" "$PATCHED"
for var in TENANTS WORKERS DURATION; do
  val="${!var:-}"
  [ -z "$val" ] && continue
  python3 -I - "$PATCHED" "$var" "$val" << 'PYEOF'
import sys, re
path, var, val = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(path).read()
pattern = re.compile(
    r'(- name: ' + re.escape(var) + r'\n(?:\s*#[^\n]*\n)*\s*value: ")[^"]*(")'
)
new_text, n = pattern.subn(lambda m: m.group(1) + val + m.group(2), text, count=1)
if n == 0:
    sys.exit(f"override target not found for {var} in {path}")
open(path, "w").write(new_text)
PYEOF
  echo "[archive] override: $var=$val"
done

# --- Clean up any previous run of the same Job name ------------------------
$OC delete job "$JOB_NAME" -n "$NAMESPACE" --ignore-not-found --wait=true >/dev/null

# --- Resolve target EPP pod and its starting restart count -----------------
EPP_POD="$($OC get pods -n "$NAMESPACE" -l "$EPP_SELECTOR" -o jsonpath='{.items[0].metadata.name}')"
if [ -z "$EPP_POD" ]; then
  echo "[archive] FATAL: no pod matched selector '$EPP_SELECTOR' in $NAMESPACE" >&2
  exit 1
fi
START_RESTARTS="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath='{.status.containerStatuses[0].restartCount}')"
START_UID="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath='{.metadata.uid}')"
echo "[archive] target pod: $EPP_POD (restarts so far: $START_RESTARTS, uid: $START_UID)"

RUN_START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RESTART_EVENTS=0

# --- Log-capture loop: restarts -f if the stream ends early -----------------
# Runs in the background for the whole script; killed in the trap below.
# UNI-170: $CAPTURE_PID below is the PID of the capture_loop *function's*
# subshell, not of the "oc logs -f" it execs -- bash does not propagate
# signals from a non-interactive shell to children it already forked, so
# killing $CAPTURE_PID alone leaves "oc logs -f" running and orphaned,
# reparented, and still appending to $EPP_LOG forever (see UNI-169, the same
# bug in 15-fairness-benchmark.sh). Backgrounding the oc invocation itself and
# recording its own PID (refreshed on every re-attach, since a pod restart
# gets a new oc process) lets the trap/stop code below reach the actual
# log-streaming process.
CAPTURE_OC_PIDFILE="$ARTIFACT_DIR/.capture-oc.pid"
rm -f "$CAPTURE_OC_PIDFILE"
capture_loop() {
  local since="$RUN_START"
  while true; do
    echo "--- [archive] (re)attaching oc logs -f at $since ---" >> "$EPP_LOG"
    $OC logs -f "$EPP_POD" -n "$NAMESPACE" -c "$EPP_CONTAINER" --since-time="$since" >> "$EPP_LOG" 2>>"$EPP_LOG.capture-stderr" &
    echo "$!" > "$CAPTURE_OC_PIDFILE"
    wait "$!" || true
    # oc logs -f returned: either the run is over (parent will kill us) or the
    # container restarted mid-run. Check which, and say so in the log rather
    # than silently losing whatever comes next.
    since="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "--- [archive] oc logs -f exited at $since; checking for a pod restart ---" >> "$EPP_LOG"
  done
}
capture_loop &
CAPTURE_PID=$!
# UNI-174: EXIT only (as this trap used to be) misses SIGINT/SIGTERM/SIGHUP --
# a killed run left this exact orphan every time, which is how the
# five-process pileup in [[process_capture_loop_leaks_orphaned_oc_logs]] was
# found. stop_capture is idempotent (safe to call twice), so it is never
# unregistered either -- unlike the old `trap - EXIT` below, it now stays
# armed through the loadgen-log-fetch/manifest-write tail, too. SIGKILL (-9)
# still cannot be trapped by any process; an orphan from that path is not
# prevented by anything here.
stop_capture() {
  kill "$CAPTURE_PID" "$(cat "$CAPTURE_OC_PIDFILE" 2>/dev/null)" 2>/dev/null || true
  wait "$CAPTURE_PID" 2>/dev/null || true
}
trap stop_capture EXIT
# A trap on INT/TERM/HUP alone does not terminate the process once its
# command returns -- bash just resumes the script (confirmed empirically
# while testing this exact pattern in 15-fairness-benchmark.sh for UNI-174).
# `exit` is what actually ends it; that still fires the EXIT trap above, so
# stop_capture runs once per signal either way.
trap 'exit 1' INT TERM HUP

# --- Apply the (possibly patched) Job and poll to completion ----------------
$OC apply -f "$PATCHED" -n "$NAMESPACE"
echo "[archive] job applied, polling for completion..."
PHASE=""
for i in $(seq 1 240); do
  SUCCEEDED="$($OC get job "$JOB_NAME" -n "$NAMESPACE" -o jsonpath='{.status.succeeded}' 2>/dev/null || true)"
  FAILED="$($OC get job "$JOB_NAME" -n "$NAMESPACE" -o jsonpath='{.status.failed}' 2>/dev/null || true)"
  CUR_RESTARTS="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath='{.status.containerStatuses[0].restartCount}' 2>/dev/null || echo "$START_RESTARTS")"
  if [ "$CUR_RESTARTS" != "$START_RESTARTS" ] && [ "$RESTART_EVENTS" -eq 0 ]; then
    RESTART_EVENTS=1
    echo "[archive] WARNING: EPP pod restart detected mid-run ($START_RESTARTS -> $CUR_RESTARTS)"
  fi
  echo "[archive] [$i] job=$JOB_NAME succeeded=${SUCCEEDED:-0} failed=${FAILED:-0} epp_restarts=$CUR_RESTARTS"
  if [ "${SUCCEEDED:-0}" = "1" ] || [ "${FAILED:-0}" -ge 1 ] 2>/dev/null; then
    PHASE="done"
    break
  fi
  sleep 10
done
RUN_END="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if [ "$PHASE" != "done" ]; then
  echo "[archive] WARNING: polling timed out before the Job reported completion" >&2
fi

# --- Stop capture, collect loadgen's own log, finalize manifest ------------
# Calls the same idempotent function the trap above uses; the trap is left
# armed (no `trap - EXIT`) as a backstop for the manifest-write tail below.
stop_capture

LOADGEN_POD="$($OC get pods -n "$NAMESPACE" -l job-name="$JOB_NAME" -o jsonpath='{.items[0].metadata.name}')"
$OC logs "$LOADGEN_POD" -n "$NAMESPACE" > "$LOADGEN_LOG" 2>&1 || echo "[archive] WARNING: could not fetch loadgen pod log" >&2

END_RESTARTS="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath='{.status.containerStatuses[0].restartCount}' 2>/dev/null || echo "$START_RESTARTS")"
BYTE_COUNT="$(wc -c < "$EPP_LOG" | tr -d ' ')"
# Matched on the quoted message text, not a specific field name: this EPP's
# zap encoding uses OpenTelemetry-shaped keys ("body" / "severity_text"), not
# the classic "msg" / "level" -- matching the literal value is robust to that
# and to any future encoder change.
FLIGHT_RECORDER_LINES="$(grep -c '"fairness state"' "$EPP_LOG" || true)"

cat > "$MANIFEST_FILE" << JSON
{
  "label": "$LABEL",
  "namespace": "$NAMESPACE",
  "job": "$JOB_NAME",
  "runStart": "$RUN_START",
  "runEnd": "$RUN_END",
  "eppPod": "$EPP_POD",
  "eppPodUidAtStart": "$START_UID",
  "eppContainerRestartsAtStart": $START_RESTARTS,
  "eppContainerRestartsAtEnd": $END_RESTARTS,
  "eppPodRestartedMidRun": $([ "$START_RESTARTS" != "$END_RESTARTS" ] && echo true || echo false),
  "eppLogFile": "epp-container.log",
  "eppLogByteCount": $BYTE_COUNT,
  "eppLogFlightRecorderLineCount": $FLIGHT_RECORDER_LINES,
  "loadgenLogFile": "loadgen.log",
  "manifestFile": "manifest.json"
}
JSON

echo "[archive] done. byte_count=$BYTE_COUNT flight_recorder_lines=$FLIGHT_RECORDER_LINES restarted_mid_run=$([ "$START_RESTARTS" != "$END_RESTARTS" ] && echo true || echo false)"
echo "[archive] manifest: $MANIFEST_FILE"
