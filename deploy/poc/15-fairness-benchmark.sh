#!/bin/bash
# UNI-54: a named, repeatable fairness benchmark whose output IS the fairness
# result, instead of a human reading Prometheus after the fact and doing the
# division by hand (see docs/poc-results.md's 1.57:1-against-2:1 detour).
#
# This wraps 04-loadgen.yaml the same way 14-loadgen-with-log-archive.sh
# (UNI-46) does -- same patched-copy-of-the-manifest mechanism, same
# restart-tolerant EPP container log capture -- and adds the two things that
# script does not: an exact before/after snapshot of the EPP's own
# llm_d_epp_maas_fairness_* counters (same mechanism as UNI-34's
# 13-loadgen-poisson.sh), and the per-run report (15-fairness-report.py) that
# turns both into a verdict. All three artifacts land in the same
# results/<timestamp>-<label>/ directory UNI-46 introduced, next to the EPP
# log, so a run ships with its own numbers next to its own evidence.
#
# This script does not duplicate 14's code by sourcing it (its EPP-log-follow
# loop and Job-polling loop are written as a single top-level flow, not
# functions, and 14 is independently reviewed and merged -- forking it here
# would create two copies to keep in sync). The capture and polling logic
# below is deliberately the same shape.
#
# Scope: GPU path only (board direction, 2026-10-19). EPP_SELECTOR targets
# the LLMInferenceService-managed scheduler pod
# (maas-vllm-gpu-kserve-router-scheduler-*), not the simulator's 02-epp.yaml
# Deployment. Passing a different EPP_SELECTOR/BACKEND is possible (the
# metrics-snapshot and log-capture mechanisms are backend-agnostic) but is
# out of this ticket's scope -- see --backend below, which only labels
# whatever you point it at, and does not validate it.
#
# Prerequisites:
#   - OPENSHIFT_TOKEN env var with edit access to maas-fairness-poc.
#   - `oc` and `python3` on PATH.
#   - deploy/rbac.yaml already applied (mints the /metrics reader token used
#     by the snapshot step, same as 13-loadgen-poisson.sh).
#
# Usage:
#   OPENSHIFT_TOKEN=... ./deploy/poc/15-fairness-benchmark.sh <scenario> [label]
#
# Scenarios (named per the four experiments already described in the
# comments of 04-loadgen.yaml, plus one negative control -- UNI-103):
#   full-contention        TENANTS="app1 app2 end-users", per-tenant workers
#                          32/32/128 (app1/app2/end-users) -- the weight-split
#                          headline test. Sized, not equal: see "Per-tenant
#                          worker sizing" below for why equal WORKERS=32
#                          failed on this backend (UNI-100/UNI-103) and where
#                          32/32/128 comes from (A4 Run 3, UNI-29).
#   end-users-idle         TENANTS="app1 app2", per-tenant workers 128/32
#                          (app1/app2) -- end-users' 65% must be absorbed by
#                          app1/app2, not reserved. app1 over-offers relative
#                          to app2 for the same reason end-users does in
#                          full-contention: app1 is the higher-share tenant
#                          once end-users is out of the pool (66.7% vs 33.3%),
#                          so it needs more concurrency to stay backlogged.
#   equal-workers-control  TENANTS="app1 app2 end-users", equal WORKERS (the
#                          ORIGINAL full-contention shape, kept as a named
#                          negative control -- UNI-103). Expected to NOT show
#                          the weighted split on this backend (work
#                          conservation drains the high-weight tenant's
#                          queue); the report marks it INFO, not PASS/FAIL,
#                          and it does not count toward this script's exit
#                          code or the suite's pass/fail bar.
#   app1-alone             TENANTS="app1" -- must receive ~100% of the pool.
#   asymmetric-demand      WORKERS_APP1=32, WORKERS_APP2=0,
#                          WORKERS_END_USERS=2 -- the exact commented-out
#                          example in 04-loadgen.yaml's per-tenant-override
#                          block. Note this sets app2 idle too (0 workers),
#                          which is that block's own documented example; the
#                          ticket prose only names APP1/END_USERS but the
#                          YAML comment it points to is the source of truth
#                          here.
#
# Per-tenant worker sizing (see docs/runbook.md "Per-tenant worker sizing
# and the saturation check" for the full method): every ACTIVE tenant in a
# scored scenario must offer more concurrency than its entitlement, or its
# queue periodically drains and the measured split compresses toward equal
# shares no matter what the weights say (docs/poc-results.md, "The detour,
# and the lesson in it", and the 2026-10-29 UNI-100 finding that reproduced
# it on full-contention/end-users-idle). That is why full-contention and
# end-users-idle now set PER_TENANT_OVERRIDES instead of relying on a single
# global WORKERS for every tenant -- WORKERS alone cannot express "this
# tenant needs more offered load than that one," which is exactly what a
# weighted split requires once the weights differ.
#
# Overrides: WORKERS, DURATION, NAMESPACE, OPENSHIFT_SERVER, EPP_SELECTOR,
# EPP_CONTAINER, BACKEND, THRESHOLD_POINTS (default 10 -- see
# docs/runbook.md "Run the fairness benchmark" for how that number was
# chosen).
set -euo pipefail

SCENARIO="${1:?usage: $0 <scenario> [label]; scenarios: full-contention end-users-idle equal-workers-control app1-alone asymmetric-demand}"
LABEL="${2:-$SCENARIO}"

NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
OC="oc --token=${OPENSHIFT_TOKEN:?set OPENSHIFT_TOKEN} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"
EPP_SELECTOR="${EPP_SELECTOR:-app.kubernetes.io/component=llminferenceservice-router-scheduler,app.kubernetes.io/name=maas-vllm-gpu}"
EPP_CONTAINER="${EPP_CONTAINER:-main}"
BACKEND="${BACKEND:-vllm-gpu (real)}"
THRESHOLD_POINTS="${THRESHOLD_POINTS:-10}"
JOB_NAME="maas-loadgen"
DURATION="${DURATION:-240}"

# UNI-103: is this scenario scored, or a named negative control that is
# expected not to show the weighted split? Read by the report step below --
# a control still runs for real and still produces a report, it just isn't
# held to the symmetric PASS/FAIL threshold or counted in this script's exit
# code.
IS_CONTROL="false"

case "$SCENARIO" in
  full-contention)
    # Sized from A4 Run 3 (docs/poc-results.md, UNI-29), the first config on
    # this backend/model (llama-3-1-8b) that put every tenant above its
    # entitlement and reproduced the weight ordering end-users > app1 > app2.
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=32 WORKERS_APP2=32 WORKERS_END_USERS=128)
    ;;
  end-users-idle)
    # app1 is the higher-share tenant once end-users is excluded (66.7% vs
    # app2's 33.3%), so it needs to over-offer relative to app2 for the same
    # reason end-users over-offers relative to app1/app2 in full-contention
    # above -- see docs/runbook.md "Per-tenant worker sizing and the
    # saturation check".
    TENANTS="app1 app2"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=128 WORKERS_APP2=32)
    ;;
  equal-workers-control)
    # UNI-103: the ORIGINAL full-contention shape (equal WORKERS for every
    # tenant), kept on purpose as a named negative control -- it is expected
    # to compress toward equal thirds on this backend (work conservation
    # draining end-users' queue, the same mechanism docs/poc-results.md's
    # "detour" section documents), not to show 20/10/65. See
    # docs/runbook.md for why this is scored INFO, not PASS/FAIL.
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=()
    IS_CONTROL="true"
    ;;
  app1-alone)
    TENANTS="app1"
    PER_TENANT_OVERRIDES=()
    ;;
  asymmetric-demand)
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=32 WORKERS_APP2=0 WORKERS_END_USERS=2)
    ;;
  *)
    echo "unknown scenario: $SCENARIO (expected one of: full-contention end-users-idle equal-workers-control app1-alone asymmetric-demand)" >&2
    exit 1
    ;;
esac

TS="$(date -u +%Y%m%dT%H%M%SZ)"
ARTIFACT_DIR="$(pwd)/results/${TS}-${LABEL}"
mkdir -p "$ARTIFACT_DIR"
echo "[benchmark] scenario: $SCENARIO  artifact dir: $ARTIFACT_DIR"

METRICS_BEFORE="$ARTIFACT_DIR/metrics-before.txt"
METRICS_AFTER="$ARTIFACT_DIR/metrics-after.txt"
EPP_LOG="$ARTIFACT_DIR/epp-container.log"
LOADGEN_LOG="$ARTIFACT_DIR/loadgen.log"
REPORT_JSON="$ARTIFACT_DIR/fairness-report.json"
REPORT_MD="$ARTIFACT_DIR/fairness-report.md"

# --- Resolve manifest with this scenario's overrides -----------------------
SRC="$(dirname "$0")/04-loadgen.yaml"
PATCHED="$ARTIFACT_DIR/04-loadgen.patched.yaml"
cp "$SRC" "$PATCHED"

set_override() {
  local var="$1" val="$2"
  python3 -I - "$PATCHED" "$var" "$val" << 'PYEOF'
import sys, re
path, var, val = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(path).read()

# Already-uncommented entry (TENANTS, WORKERS, DURATION ship this way).
active = re.compile(r'(- name: ' + re.escape(var) + r'\n(?:\s*#[^\n]*\n)*\s*value: ")[^"]*(")')
new_text, n = active.subn(lambda m: m.group(1) + val + m.group(2), text, count=1)
if n == 0:
    # Per-tenant overrides (WORKERS_APP1/APP2/END_USERS) ship commented out.
    commented = re.compile(
        r'(?P<indent>[ \t]*)# - name: ' + re.escape(var) + r'\n'
        r'[ \t]*#[ \t]+value: "[^"]*"\n'
    )
    def repl(m):
        indent = m.group('indent')
        return f'{indent}- name: {var}\n{indent}  value: "{val}"\n'
    new_text, n = commented.subn(repl, text, count=1)
if n == 0:
    sys.exit(f"override target not found for {var} in {path}")
open(path, "w").write(new_text)
PYEOF
  echo "[benchmark] override: $var=$val"
}

set_override TENANTS "$TENANTS"
set_override WORKERS "${WORKERS:-32}"
set_override DURATION "$DURATION"
for kv in "${PER_TENANT_OVERRIDES[@]+"${PER_TENANT_OVERRIDES[@]}"}"; do
  set_override "${kv%%=*}" "${kv#*=}"
done

# --- Clean up any previous run of the same Job name -------------------------
$OC delete job "$JOB_NAME" -n "$NAMESPACE" --ignore-not-found --wait=true >/dev/null

# --- Resolve target EPP pod, its restart count, and its metrics endpoint ---
EPP_POD="$($OC get pods -n "$NAMESPACE" -l "$EPP_SELECTOR" -o jsonpath='{.items[0].metadata.name}')"
if [ -z "$EPP_POD" ]; then
  echo "[benchmark] FATAL: no pod matched selector '$EPP_SELECTOR' in $NAMESPACE" >&2
  exit 1
fi
EPP_IMAGE_DIGEST="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath="{.status.containerStatuses[?(@.name=='$EPP_CONTAINER')].imageID}")"
START_RESTARTS="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath='{.status.containerStatuses[0].restartCount}')"
echo "[benchmark] target pod: $EPP_POD  image: $EPP_IMAGE_DIGEST  (restarts so far: $START_RESTARTS)"

METRICS_TOKEN="$($OC get secret maas-epp-metrics-reader-token -n "$NAMESPACE" -o jsonpath='{.data.token}' | base64 -d)"
EPP_METRICS_SVC_IP="${EPP_METRICS_SVC_IP:-}"
if [ -z "$EPP_METRICS_SVC_IP" ]; then
  EPP_METRICS_SVC_IP="$($OC get svc maas-vllm-gpu-epp-service -n "$NAMESPACE" -o jsonpath='{.spec.clusterIP}')"
fi
snapshot_metrics() {
  curl -sS -m 10 -H "Authorization: Bearer $METRICS_TOKEN" "http://${EPP_METRICS_SVC_IP}:9090/metrics" \
    | grep '^llm_d_epp_maas_fairness_' | grep -v '^#'
}

echo "[benchmark] metrics snapshot: before"
snapshot_metrics > "$METRICS_BEFORE"
ENFORCE="$(awk '/^llm_d_epp_maas_fairness_enforcing/ {print ($2==1)?"true":"false"}' "$METRICS_BEFORE")"
RUN_START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# --- Log-capture loop: restarts -f if the stream ends early (UNI-46 shape) --
capture_loop() {
  local since="$RUN_START"
  while true; do
    echo "--- [benchmark] (re)attaching oc logs -f at $since ---" >> "$EPP_LOG"
    $OC logs -f "$EPP_POD" -n "$NAMESPACE" -c "$EPP_CONTAINER" --since-time="$since" >> "$EPP_LOG" 2>>"$EPP_LOG.capture-stderr" || true
    since="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "--- [benchmark] oc logs -f exited at $since; checking for a pod restart ---" >> "$EPP_LOG"
  done
}
capture_loop &
CAPTURE_PID=$!
trap '
  kill "$CAPTURE_PID" 2>/dev/null || true
  wait "$CAPTURE_PID" 2>/dev/null || true
' EXIT

# --- Apply the patched Job and poll to completion ---------------------------
$OC apply -f "$PATCHED" -n "$NAMESPACE"
echo "[benchmark] job applied, polling for completion..."
PHASE=""
RESTART_EVENTS=0
for i in $(seq 1 240); do
  SUCCEEDED="$($OC get job "$JOB_NAME" -n "$NAMESPACE" -o jsonpath='{.status.succeeded}' 2>/dev/null || true)"
  FAILED="$($OC get job "$JOB_NAME" -n "$NAMESPACE" -o jsonpath='{.status.failed}' 2>/dev/null || true)"
  CUR_RESTARTS="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath='{.status.containerStatuses[0].restartCount}' 2>/dev/null || echo "$START_RESTARTS")"
  if [ "$CUR_RESTARTS" != "$START_RESTARTS" ] && [ "$RESTART_EVENTS" -eq 0 ]; then
    RESTART_EVENTS=1
    echo "[benchmark] WARNING: EPP pod restart detected mid-run ($START_RESTARTS -> $CUR_RESTARTS)"
  fi
  echo "[benchmark] [$i] job=$JOB_NAME succeeded=${SUCCEEDED:-0} failed=${FAILED:-0} epp_restarts=$CUR_RESTARTS"
  if [ "${SUCCEEDED:-0}" = "1" ] || [ "${FAILED:-0}" -ge 1 ] 2>/dev/null; then
    PHASE="done"
    break
  fi
  sleep 10
done
if [ "$PHASE" != "done" ]; then
  echo "[benchmark] WARNING: polling timed out before the Job reported completion" >&2
fi

# --- Stop capture, collect loadgen's own log, snapshot metrics after -------
kill "$CAPTURE_PID" 2>/dev/null || true
wait "$CAPTURE_PID" 2>/dev/null || true
trap - EXIT

LOADGEN_POD="$($OC get pods -n "$NAMESPACE" -l job-name="$JOB_NAME" -o jsonpath='{.items[0].metadata.name}')"
$OC logs "$LOADGEN_POD" -n "$NAMESPACE" > "$LOADGEN_LOG" 2>&1 || echo "[benchmark] WARNING: could not fetch loadgen pod log" >&2

echo "[benchmark] metrics snapshot: after"
snapshot_metrics > "$METRICS_AFTER"
RUN_END="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# --- Build the report; its exit code becomes this script's exit code -------
set +e
REPORT_ARGS=(
  --scenario "$SCENARIO" --label "$LABEL" --enforce "$ENFORCE"
  --duration-seconds "$DURATION" --backend "$BACKEND"
  --epp-image-digest "$EPP_IMAGE_DIGEST" --namespace "$NAMESPACE" --epp-pod "$EPP_POD"
  --run-start "$RUN_START" --run-end "$RUN_END" --threshold-points "$THRESHOLD_POINTS"
  --metrics-before "$METRICS_BEFORE" --metrics-after "$METRICS_AFTER" --loadgen-log "$LOADGEN_LOG"
  --out-json "$REPORT_JSON" --out-md "$REPORT_MD"
)
if [ "$IS_CONTROL" = "true" ]; then
  REPORT_ARGS+=(--control)
fi
python3 -I "$(dirname "$0")/15-fairness-report.py" "${REPORT_ARGS[@]}"
REPORT_EXIT=$?
set -e

echo "[benchmark] report: $REPORT_JSON , $REPORT_MD"
exit "$REPORT_EXIT"
