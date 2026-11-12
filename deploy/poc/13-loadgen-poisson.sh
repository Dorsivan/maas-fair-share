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
#
# EPP container log (UNI-46): for the duration of the run, the GPU EPP
# container log is followed into $OUT/epp-container.log, bounded to start
# when the generator starts and stop when it exits -- this POC cluster has no
# log retention (docs/design.md "Production observability"), so a run that
# doesn't capture its own evidence loses it the moment the pod recycles.
# $OUT/epp-container-log-manifest.txt records the byte count and whether the
# pod/container restarted mid-capture, so a truncated or oversized log is
# visible instead of silently trusted. Override EPP_POD_LABEL_SELECTOR /
# EPP_CONTAINER for a different target, or set CAPTURE_EPP_LOG=0 to disable
# (e.g. a CPU-path or simulator run, which is out of this harness's scope).
set -euo pipefail

NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
GW="${GW:-https://maas-gateway-${NAMESPACE}.apps.ocp.paladinaura.com}"
MODELPATH="${MODELPATH:-/${NAMESPACE}/maas-vllm-gpu}"
DURATION="${DURATION:-240}"
RATE_APP1="${RATE_APP1:-0}"
RATE_APP2="${RATE_APP2:-0}"
RATE_END_USERS="${RATE_END_USERS:-0}"
SEED="${SEED:-1}"
OUT="${OUT:-/tmp/poisson-codes-$(date +%s)}"
MAX_WORKERS="${MAX_WORKERS:-1000}"
DRAIN_TIMEOUT="${DRAIN_TIMEOUT:-100}"
CLIENT_TIMEOUT="${CLIENT_TIMEOUT:-90}"
EPP_METRICS_SVC_IP="${EPP_METRICS_SVC_IP:-}"
CAPTURE_EPP_LOG="${CAPTURE_EPP_LOG:-1}"
EPP_POD_LABEL_SELECTOR="${EPP_POD_LABEL_SELECTOR:-app.kubernetes.io/name=maas-vllm-gpu,app.kubernetes.io/component=llminferenceservice-router-scheduler}"
EPP_CONTAINER="${EPP_CONTAINER:-main}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OC="oc --token=${OPENSHIFT_TOKEN:?set OPENSHIFT_TOKEN} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"

EPP_LOG_PID=""
cleanup() {
  rm -rf "$KEYS"
  if [ -n "$EPP_LOG_PID" ] && kill -0 "$EPP_LOG_PID" 2>/dev/null; then
    kill "$EPP_LOG_PID" 2>/dev/null || true
    wait "$EPP_LOG_PID" 2>/dev/null || true
  fi
}

KEYS="$(mktemp -d)"
# UNI-174: EXIT only used to miss SIGINT/SIGTERM/SIGHUP, leaving the
# background `oc logs -f` (and the $KEYS tempdir) to leak if this script was
# killed rather than left to finish or fail on its own -- same class of bug
# as 15-fairness-benchmark.sh's capture loop (UNI-169) and
# 14-loadgen-with-log-archive.sh's (UNI-170). cleanup() is already idempotent
# (kill -0 guards against a second kill of an already-dead PID). A trap on
# INT/TERM/HUP alone would not terminate the process once cleanup() returns
# (bash just resumes the script -- confirmed empirically on
# 15-fairness-benchmark.sh's identical pattern), so those three go to a
# separate trap that calls `exit`, which in turn fires the EXIT trap below
# exactly once. SIGKILL (-9) still cannot be trapped by any process.
trap cleanup EXIT
trap 'exit 1' INT TERM HUP
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

# UNI-157: widened from the original llm_d_epp_maas_fairness_-only grep to also pull the
# flow-control queueing metrics (llm_d_epp_flow_control_requests_total,
# llm_d_epp_flow_control_request_queue_duration_seconds_{count,sum,bucket}). docs/runbook.md's
# UNI-181 section flagged this as a known, deliberately-deferred gap: without it, a TTL-shedding
# run's before/after snapshots carry no evidence of evictions at all, and 15-fairness-report.py's
# `shed` section can only ever fall back to the client's own 429/503 tally. Checked against
# 15-fairness-report-test.py's 31 existing cases: all still pass, since every prior committed
# run's snapshot simply has no flow_control_* lines to match (nothing was ever queued/evicted on
# those runs) and the report's parser already treats an absent line as "not recorded".
#
# UNI-221: widened again to also pull the per-request TTFT/ITL/token histograms
# (llm_d_epp_request_ttft_seconds_*, llm_d_epp_request_streaming_itl_seconds_*,
# llm_d_epp_request_(input|output|cached)_tokens_*). 15-fairness-benchmark.sh's
# closed-loop scrape (used by UNI-226) already includes this prefix; the
# open-loop generator never did, so every open-loop report's "Per-tenant TTFT /
# ITL and the priority verdict (UNI-226)" section reads "not recorded" and the
# SPLIT-FAIL/PRIORITY-OK secondary verdict can never be computed for an
# open-loop run -- see docs/poc-results.md "UNI-221" for the run this gap was
# found on. Untested past a dry grep until the next open-loop run exercises it.
snapshot_metrics() {
  curl -sS -m 10 -H "Authorization: Bearer $METRICS_TOKEN" "http://${EPP_METRICS_SVC_IP}:9090/metrics" \
    | grep -E '^(llm_d_epp_maas_fairness_|llm_d_epp_flow_control_|llm_d_epp_request_(ttft|streaming_itl|input_tokens|output_tokens|cached_tokens)_)' | grep -v '^#'
}

EPP_LOG_FILE="$OUT/epp-container.log"
EPP_LOG_MANIFEST="$OUT/epp-container-log-manifest.txt"
EPP_POD=""
EPP_POD_UID=""
EPP_POD_RESTARTS_BEFORE=""
EPP_LOG_START_TIME=""

# Starts `oc logs -f` on the GPU EPP container in the background, writing
# straight to $OUT. Must run after `mkdir -p "$OUT"`.
start_epp_log_capture() {
  if [ "$CAPTURE_EPP_LOG" != "1" ]; then
    echo "=== EPP log capture disabled (CAPTURE_EPP_LOG=$CAPTURE_EPP_LOG) ==="
    return
  fi
  EPP_POD="$($OC get pods -n "$NAMESPACE" -l "$EPP_POD_LABEL_SELECTOR" \
    -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)"
  if [ -z "$EPP_POD" ]; then
    echo "WARNING: no pod matched selector '$EPP_POD_LABEL_SELECTOR' in $NAMESPACE -- EPP log capture skipped" \
      | tee "$EPP_LOG_MANIFEST" >&2
    CAPTURE_EPP_LOG=0
    return
  fi
  EPP_POD_UID="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath='{.metadata.uid}')"
  EPP_POD_RESTARTS_BEFORE="$($OC get pod "$EPP_POD" -n "$NAMESPACE" \
    -o jsonpath="{.status.containerStatuses[?(@.name==\"$EPP_CONTAINER\")].restartCount}")"
  EPP_LOG_START_TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "=== capturing EPP container log: pod=$EPP_POD container=$EPP_CONTAINER -> $EPP_LOG_FILE ==="
  : > "$EPP_LOG_FILE"
  $OC logs -f "$EPP_POD" -c "$EPP_CONTAINER" -n "$NAMESPACE" --timestamps >>"$EPP_LOG_FILE" 2>&1 &
  EPP_LOG_PID=$!
}

# Stops the follow, detects a mid-run restart, recovers what it can of a
# crashed or replaced instance's log, and writes the byte-count manifest.
stop_epp_log_capture() {
  [ "$CAPTURE_EPP_LOG" = "1" ] || return
  [ -n "$EPP_POD" ] || return
  local end_time follow_died_early uid_after restarts_after restarted reason
  end_time="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  follow_died_early=0
  if [ -n "$EPP_LOG_PID" ] && kill -0 "$EPP_LOG_PID" 2>/dev/null; then
    kill "$EPP_LOG_PID" 2>/dev/null || true
    wait "$EPP_LOG_PID" 2>/dev/null || true
  else
    follow_died_early=1   # the stream ended on its own -- almost always a restart
  fi
  EPP_LOG_PID=""

  uid_after="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath='{.metadata.uid}' 2>/dev/null || true)"
  restarts_after="$($OC get pod "$EPP_POD" -n "$NAMESPACE" \
    -o jsonpath="{.status.containerStatuses[?(@.name==\"$EPP_CONTAINER\")].restartCount}" 2>/dev/null || true)"

  restarted="no"
  if [ "$follow_died_early" = "1" ] || [ "$uid_after" != "$EPP_POD_UID" ] \
     || [ "${restarts_after:-0}" != "${EPP_POD_RESTARTS_BEFORE:-0}" ]; then
    restarted="yes"
    {
      echo "### RUN-HARNESS NOTICE: EPP pod/container restarted during the capture window ($EPP_LOG_START_TIME .. $end_time)."
      echo "### before: pod=$EPP_POD uid=$EPP_POD_UID restartCount=${EPP_POD_RESTARTS_BEFORE:-0}"
      echo "### after:  pod=$EPP_POD uid=${uid_after:-<gone>} restartCount=${restarts_after:-unknown}"
      echo "### log lines emitted around the restart may be missing from the stream above -- recovery attempt follows."
    } >>"$EPP_LOG_FILE"

    if [ "$uid_after" = "$EPP_POD_UID" ] && [ -n "${restarts_after:-}" ] \
       && [ "$restarts_after" -gt "${EPP_POD_RESTARTS_BEFORE:-0}" ] 2>/dev/null; then
      echo "### same pod, container restarted -- appending the crashed instance's log via --previous:" >>"$EPP_LOG_FILE"
      $OC logs "$EPP_POD" -c "$EPP_CONTAINER" -n "$NAMESPACE" --previous --timestamps >>"$EPP_LOG_FILE" 2>&1 \
        || echo "### --previous log unavailable (already evicted)" >>"$EPP_LOG_FILE"
    elif [ -n "$uid_after" ] && [ "$uid_after" != "$EPP_POD_UID" ]; then
      echo "### pod was recreated (new pod uid) -- appending a tail from the replacement so recent context isn't silently lost:" >>"$EPP_LOG_FILE"
      $OC logs "$EPP_POD" -c "$EPP_CONTAINER" -n "$NAMESPACE" --timestamps --tail=1000 >>"$EPP_LOG_FILE" 2>&1 \
        || echo "### replacement pod log unavailable" >>"$EPP_LOG_FILE"
    else
      echo "### pod is gone -- no replacement found to recover a tail from." >>"$EPP_LOG_FILE"
    fi
  fi

  local bytes
  bytes="$(wc -c <"$EPP_LOG_FILE" | tr -d ' ')"
  {
    echo "pod: $EPP_POD"
    echo "container: $EPP_CONTAINER"
    echo "namespace: $NAMESPACE"
    echo "capture_start: $EPP_LOG_START_TIME"
    echo "capture_end: $end_time"
    echo "pod_restarted_during_run: $restarted"
    echo "bytes_captured: $bytes"
    echo "file: $(basename "$EPP_LOG_FILE")"
  } | tee "$EPP_LOG_MANIFEST"
}

echo "=== metrics snapshot: before ==="
BEFORE="$(snapshot_metrics)"
echo "$BEFORE"

mkdir -p "$OUT"
start_epp_log_capture

set +e
python3 "$SCRIPT_DIR/13-loadgen-poisson.py" \
  --gw "$GW" --modelpath "$MODELPATH" --duration "$DURATION" \
  --rate-app1 "$RATE_APP1" --rate-app2 "$RATE_APP2" --rate-end-users "$RATE_END_USERS" \
  --key-app1 "$KEYS/app1-production" --key-app2 "$KEYS/app2-batch" \
  --key-end-alpha "$KEYS/end-user-alpha" --key-end-beta "$KEYS/end-user-beta" \
  --out "$OUT" --seed "$SEED" --max-workers "$MAX_WORKERS" --drain-timeout "$DRAIN_TIMEOUT" \
  --client-timeout "$CLIENT_TIMEOUT"
GEN_STATUS=$?
set -e

echo "=== EPP log capture summary ==="
stop_epp_log_capture

if [ "$GEN_STATUS" -ne 0 ]; then
  echo "load generator exited $GEN_STATUS -- EPP log above still reflects the attempted run" >&2
  exit "$GEN_STATUS"
fi

echo "=== metrics snapshot: after ==="
AFTER="$(snapshot_metrics)"
echo "$AFTER"

echo "$BEFORE" > "$OUT/metrics-before.txt"
echo "$AFTER" > "$OUT/metrics-after.txt"

echo "=== delta (after - before), this run's contribution ==="
python3 "$SCRIPT_DIR/13-loadgen-poisson-delta.py" "$OUT/metrics-before.txt" "$OUT/metrics-after.txt" | tee "$OUT/delta.txt"

echo "=== run output directory: $OUT ==="
