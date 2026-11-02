#!/bin/bash
# UNI-137 (B5): wraps deploy/poc/13-loadgen-poisson.sh (UNI-34's open-loop,
# Poisson-arrival generator) the way 15-fairness-benchmark.sh wraps the
# closed-loop 04-loadgen.yaml Job -- each invocation is one named benchmark
# scenario, landing in the same results/<ts>-<label>/ directory shape, scored
# by the same 15-fairness-report.py. It does NOT reuse 15-fairness-
# benchmark.sh's own flow: that script's whole mechanism is built around
# patching and polling a Job (04-loadgen.yaml), and 13-loadgen-poisson.sh is a
# local process hitting the public Route directly, not a Job -- there is no
# Job to patch or poll here. What IS reused, unmodified, is 13-loadgen-
# poisson.sh itself (key-fetch, metrics before/after snapshot, EPP container
# log capture) and 15-fairness-report.py (UNI-137 taught it to parse this
# generator's own log shape -- see OPEN_LOOP_TENANTS_LINE/OPEN_LOOP_ROW there
# -- instead of 04-loadgen.yaml's closed-loop table).
#
# Prerequisites: same as 13-loadgen-poisson.sh -- OPENSHIFT_TOKEN with read
# access to maas-fairness-poc, `oc`/`python3` on PATH, deploy/rbac.yaml
# already applied.
#
# Usage:
#   OPENSHIFT_TOKEN=... RATE_APP1=4.9 RATE_APP2=4.9 RATE_END_USERS=4.9 \
#     DURATION=240 ./17-fairness-benchmark-openloop.sh <scenario> [label]
#
# RATE_APP1/RATE_APP2/RATE_END_USERS are req/s Poisson means, passed straight
# through to 13-loadgen-poisson.py -- 0 (the default) disables that tenant.
# "Full-contention mix" (the only shape this ticket's B5 case uses) means all
# three > 0, each at the SAME rate, per UNI-34's own methodology ("every
# tenant must offer more load than its entitlement... size load so demand,
# not asymmetry, decides the split" -- docs/poc-results.md): with identical
# per-tenant demand, any split away from equal thirds is the policy's doing,
# not the traffic's.
#
# Overrides: NAMESPACE, OPENSHIFT_SERVER, EPP_SELECTOR, EPP_CONTAINER,
# BACKEND, THRESHOLD_POINTS (default 10), SEED (default 1).
#
# UNI-174 inventory: this wrapper itself creates no Job, ConfigMap, pod, or
# replica change, and starts no background process of its own -- it runs
# 13-loadgen-poisson.sh synchronously in the foreground and only reads
# cluster state (the active-Job check above, the EPP pod lookup below). There
# is nothing here for an exit trap to revert. The one piece of state a crash
# mid-run could leave behind (an orphaned `oc logs -f` against the EPP) is
# 13-loadgen-poisson.sh's own, and that script now carries its own
# EXIT/INT/TERM/HUP-trapped guarantee -- see the trap in 13-loadgen-poisson.sh
# for why -- so this script does not duplicate it.
set -euo pipefail

SCENARIO="${1:?usage: $0 <scenario> [label]; set RATE_APP1/RATE_APP2/RATE_END_USERS and DURATION}"
LABEL="${2:-$SCENARIO}"

NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
OC="oc --token=${OPENSHIFT_TOKEN:?set OPENSHIFT_TOKEN} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"
EPP_SELECTOR="${EPP_SELECTOR:-app.kubernetes.io/component=llminferenceservice-router-scheduler,app.kubernetes.io/name=maas-vllm-gpu}"
EPP_CONTAINER="${EPP_CONTAINER:-main}"
BACKEND="${BACKEND:-vllm-gpu (real)}"
THRESHOLD_POINTS="${THRESHOLD_POINTS:-10}"
DURATION="${DURATION:-240}"
SEED="${SEED:-1}"
RATE_APP1="${RATE_APP1:-0}"
RATE_APP2="${RATE_APP2:-0}"
RATE_END_USERS="${RATE_END_USERS:-0}"
JOB_NAME="maas-loadgen"

# --- Rule 1 (UNI-117 series): one benchmark on the GPU pool at a time. This
# wrapper never creates a Job itself, but a closed-loop benchmark run via
# 15-fairness-benchmark.sh (or a leftover from one) would still contend for
# the same GPU pool this generator hits directly -- refuse to start over an
# ACTIVE maas-loadgen Job. A previously-Complete Job is harmless and left
# alone (it is not re-deleted here, unlike 15-fairness-benchmark.sh, since
# this script never reuses that Job name).
ACTIVE="$($OC get job "$JOB_NAME" -n "$NAMESPACE" -o jsonpath='{.status.active}' 2>/dev/null || true)"
if [ -n "$ACTIVE" ] && [ "$ACTIVE" -ge 1 ] 2>/dev/null; then
  echo "[openloop] FATAL: job/$JOB_NAME is still Active in $NAMESPACE -- refusing to start a concurrent GPU-pool run" >&2
  exit 1
fi

python3 -I -c "
import sys
rates = [float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])]
sys.exit(0 if any(r > 0 for r in rates) else 1)
" "$RATE_APP1" "$RATE_APP2" "$RATE_END_USERS" || {
  echo "[openloop] FATAL: at least one of RATE_APP1/RATE_APP2/RATE_END_USERS must be > 0" >&2
  exit 1
}

TS="$(date -u +%Y%m%dT%H%M%SZ)"
ARTIFACT_DIR="$(pwd)/results/${TS}-${LABEL}"
mkdir -p "$ARTIFACT_DIR"
echo "[openloop] scenario: $SCENARIO  artifact dir: $ARTIFACT_DIR"
echo "[openloop] rates (req/s): app1=$RATE_APP1 app2=$RATE_APP2 end-users=$RATE_END_USERS  duration=${DURATION}s"

EPP_POD="$($OC get pods -n "$NAMESPACE" -l "$EPP_SELECTOR" -o jsonpath='{.items[0].metadata.name}')"
if [ -z "$EPP_POD" ]; then
  echo "[openloop] FATAL: no pod matched selector '$EPP_SELECTOR' in $NAMESPACE" >&2
  exit 1
fi
EPP_IMAGE_DIGEST="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath="{.status.containerStatuses[?(@.name=='$EPP_CONTAINER')].imageID}")"
echo "[openloop] target pod: $EPP_POD  image: $EPP_IMAGE_DIGEST"

LOADGEN_LOG="$ARTIFACT_DIR/loadgen.log"
REPORT_JSON="$ARTIFACT_DIR/fairness-report.json"
REPORT_MD="$ARTIFACT_DIR/fairness-report.md"

RUN_START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# --- Run the open-loop generator, unmodified. It writes metrics-before.txt,
# metrics-after.txt, epp-container.log, delta.txt and one <group>.log per
# offered tenant straight into $ARTIFACT_DIR; stdout (including the "load:
# open-loop Poisson arrivals..." header and each group's summary line that
# 15-fairness-report.py's open-loop parser needs) is tee'd into loadgen.log
# next to them. PIPESTATUS, not $?, carries the generator's own exit code
# through the pipe (pipefail would otherwise report tee's).
set +e
OPENSHIFT_TOKEN="$OPENSHIFT_TOKEN" OPENSHIFT_SERVER="${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}" \
  NAMESPACE="$NAMESPACE" EPP_POD_LABEL_SELECTOR="$EPP_SELECTOR" EPP_CONTAINER="$EPP_CONTAINER" \
  DURATION="$DURATION" SEED="$SEED" OUT="$ARTIFACT_DIR" \
  RATE_APP1="$RATE_APP1" RATE_APP2="$RATE_APP2" RATE_END_USERS="$RATE_END_USERS" \
  "$(dirname "$0")/13-loadgen-poisson.sh" 2>&1 | tee "$LOADGEN_LOG"
GEN_STATUS="${PIPESTATUS[0]}"
set -e

RUN_END="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

if [ "$GEN_STATUS" -ne 0 ]; then
  echo "[openloop] FATAL: 13-loadgen-poisson.sh exited $GEN_STATUS -- no metrics-after.txt, no report (see $LOADGEN_LOG)" >&2
  exit "$GEN_STATUS"
fi

METRICS_BEFORE="$ARTIFACT_DIR/metrics-before.txt"
METRICS_AFTER="$ARTIFACT_DIR/metrics-after.txt"
ENFORCE="$(awk '/^llm_d_epp_maas_fairness_enforcing/ {print ($2==1)?"true":"false"}' "$METRICS_BEFORE")"

set +e
python3 -I "$(dirname "$0")/15-fairness-report.py" \
  --scenario "$SCENARIO" --label "$LABEL" --enforce "$ENFORCE" \
  --duration-seconds "$DURATION" --backend "$BACKEND" \
  --epp-image-digest "$EPP_IMAGE_DIGEST" --namespace "$NAMESPACE" --epp-pod "$EPP_POD" \
  --run-start "$RUN_START" --run-end "$RUN_END" --threshold-points "$THRESHOLD_POINTS" \
  --metrics-before "$METRICS_BEFORE" --metrics-after "$METRICS_AFTER" --loadgen-log "$LOADGEN_LOG" \
  --out-json "$REPORT_JSON" --out-md "$REPORT_MD"
REPORT_EXIT=$?
set -e

echo "[openloop] report: $REPORT_JSON , $REPORT_MD"
exit "$REPORT_EXIT"
