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
#
# UNI-127 harness additions (see docs/runbook.md "Timeline, chaos, and
# windowed reporting" for the full story -- this header is a pointer, not the
# source of truth):
#   WINDOW_SECONDS           time-series snapshot interval, default 10.
#   APP1_START/STOP/DUTY, APP2_START/STOP/DUTY, END_USERS_START/STOP/DUTY
#                             per-tenant timeline, e.g. END_USERS_START=120s.
#                             Unset (the default) = active the whole run, same
#                             as every scenario before this ticket.
#   CHAOS_EPP_DELETE_AT       delete the EPP scheduler pod at t+<seconds>.
#   CHAOS_SCALE_AT            scale LLMISVC_NAME (default maas-vllm-gpu) to 1
#                             replica at t+<seconds>, restored after
#                             CHAOS_SCALE_HOLD (default 30s).
# UNI-128 harness additions (see docs/runbook.md "Request-shape profiles
# (UNI-128)" for the full story -- this header is a pointer, not the source
# of truth): PROMPT_WORDS_MIN/MAX, MAX_TOKENS_DEFAULT/OMIT_FRACTION/
# HUGE_FRACTION/HUGE_VALUE, STREAM_FRACTION, ABORT_FRACTION/MIN_FRACTION/
# MAX_FRACTION, OVERSIZED_FRACTION/PROMPT_WORDS, LONG_GEN_FRACTION/
# MAX_TOKENS, REQUEST_TIMEOUT_SECONDS -- passed through to the Job unchanged
# when set. All default to the single fixed request shape this benchmark
# sent before this ticket; a plain scenario invocation is unaffected.
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

# UNI-127: windowed time-series reporting (default on for every run) and the
# optional timeline/chaos harness. None of these change a single thing about
# an invocation that does not set them -- that is the regression bar this
# ticket has to clear.
WINDOW_SECONDS="${WINDOW_SECONDS:-10}"
LLMISVC_NAME="${LLMISVC_NAME:-maas-vllm-gpu}"
# Seconds-offset chaos hooks, accepting the ticket's "120s" shorthand or a
# bare integer. Empty (the default) means that hook never fires.
CHAOS_EPP_DELETE_AT="${CHAOS_EPP_DELETE_AT:-}"
CHAOS_EPP_DELETE_AT="${CHAOS_EPP_DELETE_AT//s/}"
CHAOS_SCALE_AT="${CHAOS_SCALE_AT:-}"
CHAOS_SCALE_AT="${CHAOS_SCALE_AT//s/}"
CHAOS_SCALE_HOLD="${CHAOS_SCALE_HOLD:-30s}"
CHAOS_SCALE_HOLD="${CHAOS_SCALE_HOLD//s/}"
# Per-tenant timeline (START/STOP/DUTY), passed straight through to the
# loadgen Job when set -- see deploy/poc/04-loadgen.yaml's tenant_active() for
# what they mean. Unset (the default) reproduces the one, prior behaviour:
# every offered tenant active for the whole run.
TIMELINE_VARS="APP1_START APP1_STOP APP1_DUTY APP2_START APP2_STOP APP2_DUTY END_USERS_START END_USERS_STOP END_USERS_DUTY"

# UNI-128: per-request shape profile knobs, passed straight through to the
# Job when set -- see deploy/poc/04-loadgen.yaml's send_one()/pick_prompt()/
# pick_max_tokens() for what each one means. Unset (the default for every
# scenario above) reproduces the one, prior request shape: a fixed
# 1200-word prompt, max_tokens=64, no streaming, no client aborts, no
# oversized prompts.
PROFILE_VARS="PROMPT_WORDS_MIN PROMPT_WORDS_MAX MAX_TOKENS_DEFAULT MAX_TOKENS_OMIT_FRACTION MAX_TOKENS_HUGE_FRACTION MAX_TOKENS_HUGE_VALUE STREAM_FRACTION ABORT_FRACTION ABORT_MIN_FRACTION ABORT_MAX_FRACTION OVERSIZED_FRACTION OVERSIZED_PROMPT_WORDS LONG_GEN_FRACTION LONG_GEN_MAX_TOKENS REQUEST_TIMEOUT_SECONDS"

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
    # saturation check". UNI-104: the 4:1 ratio copied from full-contention's
    # end-users overshot (82.4% vs a 66.7% target); try a ratio closer to the
    # actual 2:1 app1:app2 target instead.
    TENANTS="app1 app2"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=64 WORKERS_APP2=32)
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
CLIENT_RECORD_JSONL="$ARTIFACT_DIR/client-request-summary.jsonl"

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

# --- UNI-127 timeline pass-through: only touches the Job (and the report's
# phase-edge math below) when one of these env vars is actually set. A plain
# invocation of an existing scenario sets none of them, so TIMELINE_JSON_ENTRIES
# stays empty and behaviour is unchanged. ----------------------------------
TIMELINE_JSON_ENTRIES=()
for v in $TIMELINE_VARS; do
  val="${!v-}"
  val="${val//s/}"
  if [ -n "$val" ]; then
    set_override "$v" "$val"
    TIMELINE_JSON_ENTRIES+=("$v=$val")
  fi
done
# UNI-128 profile pass-through: same shape as the timeline loop above, no
# JSON side-channel needed -- the Job records what it actually did per
# request itself (see the client-record extraction after the Job completes).
for v in $PROFILE_VARS; do
  val="${!v-}"
  if [ -n "$val" ]; then
    set_override "$v" "$val"
  fi
done

TIMELINE_CONFIG="$ARTIFACT_DIR/timeline-config.json"
python3 -I - "$TIMELINE_CONFIG" "${TIMELINE_JSON_ENTRIES[@]+"${TIMELINE_JSON_ENTRIES[@]}"}" << 'PYEOF'
import json, sys
out_path, entries = sys.argv[1], sys.argv[2:]
by_tenant = {}
for e in entries:
    var, val = e.split("=", 1)
    if var.startswith("APP1_"):
        tenant, field = "app1", var[len("APP1_"):]
    elif var.startswith("APP2_"):
        tenant, field = "app2", var[len("APP2_"):]
    else:
        tenant, field = "end-users", var[len("END_USERS_"):]
    entry = by_tenant.setdefault(tenant, {})
    if field == "START":
        entry["start"] = float(val)
    elif field == "STOP":
        entry["stop"] = float(val)
    elif field == "DUTY":
        on, off = val.split("/", 1)
        entry["duty_on"] = float(on)
        entry["duty_off"] = float(off)
json.dump({"tenants": by_tenant, "chaos_events": []}, open(out_path, "w"), indent=2)
PYEOF

# --- UNI-127 chaos hooks: queue up what this run will do to the live system,
# for the trap/chaos loop below and for the report's phase-edge math. Empty
# unless CHAOS_EPP_DELETE_AT / CHAOS_SCALE_AT are set. --------------------
CHAOS_RESTORE_AT=""
if [ -n "$CHAOS_SCALE_AT" ]; then
  CHAOS_RESTORE_AT=$(( CHAOS_SCALE_AT + CHAOS_SCALE_HOLD ))
fi
python3 -I - "$TIMELINE_CONFIG" "$CHAOS_EPP_DELETE_AT" "$CHAOS_SCALE_AT" "$CHAOS_RESTORE_AT" "$LLMISVC_NAME" << 'PYEOF'
import json, sys
path, delete_at, scale_at, restore_at, llmisvc = sys.argv[1:6]
cfg = json.load(open(path))
events = []
if delete_at:
    events.append({"type": "epp_delete", "at_seconds": float(delete_at)})
if scale_at:
    events.append({"type": "scale_down", "at_seconds": float(scale_at), "target": llmisvc, "to": 1})
    events.append({"type": "scale_restore", "at_seconds": float(restore_at), "target": llmisvc})
cfg["chaos_events"] = events
json.dump(cfg, open(path, "w"), indent=2)
PYEOF

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

# UNI-127: capture the LLMInferenceService's current replica count before any
# chaos runs, so a scale-down can be restored to what was actually there --
# not a hardcoded 2 -- whether or not the chaos loop gets to do it itself.
ORIGINAL_REPLICAS=""
if [ -n "$CHAOS_SCALE_AT" ]; then
  ORIGINAL_REPLICAS="$($OC get llmisvc "$LLMISVC_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.replicas}')"
  echo "[benchmark] chaos: will scale $LLMISVC_NAME $ORIGINAL_REPLICAS -> 1 -> $ORIGINAL_REPLICAS at t+${CHAOS_SCALE_AT}s (hold ${CHAOS_SCALE_HOLD}s)"
fi
if [ -n "$CHAOS_EPP_DELETE_AT" ]; then
  echo "[benchmark] chaos: will delete EPP pod $EPP_POD at t+${CHAOS_EPP_DELETE_AT}s"
fi

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
RUN_START_EPOCH="$(date +%s)"

# --- Log-capture loop: restarts -f if the stream ends early (UNI-46 shape) --
# UNI-127 note: CHAOS_EPP_DELETE_AT means $EPP_POD can go permanently NotFound
# partway through the run (the Deployment's replacement pod gets a new name --
# see docs/runbook.md's "Timeline, chaos, and windowed reporting"). Without
# the sleep below, "oc logs -f" against a gone pod fails instantly and this
# loop would hammer the API server every iteration for the rest of the run.
capture_loop() {
  local since="$RUN_START"
  while true; do
    echo "--- [benchmark] (re)attaching oc logs -f at $since ---" >> "$EPP_LOG"
    $OC logs -f "$EPP_POD" -n "$NAMESPACE" -c "$EPP_CONTAINER" --since-time="$since" >> "$EPP_LOG" 2>>"$EPP_LOG.capture-stderr" || true
    since="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "--- [benchmark] oc logs -f exited at $since; checking for a pod restart ---" >> "$EPP_LOG"
    sleep 1
  done
}
capture_loop &
CAPTURE_PID=$!

# --- UNI-127 time-series loop: snapshot the same /metrics endpoint every
# WINDOW_SECONDS, so the report can turn before/after into a sequence of
# windows instead of one whole-run delta. Runs for every invocation, not just
# ones using the timeline/chaos knobs -- this is the harness capability the
# ticket asks be available by default. First entry mirrors metrics-before.txt
# exactly, so the first window starts at t=0 with no extra scrape needed.
METRICS_TS="$ARTIFACT_DIR/metrics-timeseries.txt"
{ echo "# ts=$RUN_START epoch=$RUN_START_EPOCH"; cat "$METRICS_BEFORE"; } > "$METRICS_TS"
timeseries_loop() {
  while true; do
    sleep "$WINDOW_SECONDS"
    { echo "# ts=$(date -u +%Y-%m-%dT%H:%M:%SZ) epoch=$(date +%s)"; snapshot_metrics; } >> "$METRICS_TS"
  done
}
timeseries_loop &
TS_PID=$!

# --- UNI-127 chaos loop: fires the configured hooks at their t+offset and
# logs each one, with a timestamp, to chaos-events.log. A no-op loop (nothing
# configured) still runs but never does anything -- simpler than conditionally
# starting it, and it exits the moment the trap kills it.
CHAOS_LOG="$ARTIFACT_DIR/chaos-events.log"
: > "$CHAOS_LOG"
chaos_log() {
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $1" | tee -a "$CHAOS_LOG"
}
chaos_loop() {
  local delete_done=false scale_down_done=false scale_up_done=false elapsed
  while true; do
    elapsed=$(( $(date +%s) - RUN_START_EPOCH ))
    if [ -n "$CHAOS_EPP_DELETE_AT" ] && [ "$delete_done" = false ] && [ "$elapsed" -ge "$CHAOS_EPP_DELETE_AT" ]; then
      $OC delete pod "$EPP_POD" -n "$NAMESPACE" --wait=false >/dev/null 2>&1 || true
      chaos_log "chaos: deleted EPP scheduler pod $EPP_POD (t+${elapsed}s, target was t+${CHAOS_EPP_DELETE_AT}s)"
      delete_done=true
    fi
    if [ -n "$CHAOS_SCALE_AT" ] && [ "$scale_down_done" = false ] && [ "$elapsed" -ge "$CHAOS_SCALE_AT" ]; then
      $OC patch llmisvc "$LLMISVC_NAME" -n "$NAMESPACE" --type=merge -p '{"spec":{"replicas":1}}' >/dev/null
      chaos_log "chaos: scaled $LLMISVC_NAME replicas $ORIGINAL_REPLICAS -> 1 (t+${elapsed}s, target was t+${CHAOS_SCALE_AT}s)"
      scale_down_done=true
    fi
    if [ "$scale_down_done" = true ] && [ "$scale_up_done" = false ] && [ "$elapsed" -ge "$CHAOS_RESTORE_AT" ]; then
      $OC patch llmisvc "$LLMISVC_NAME" -n "$NAMESPACE" --type=merge -p "{\"spec\":{\"replicas\":$ORIGINAL_REPLICAS}}" >/dev/null
      chaos_log "chaos: restored $LLMISVC_NAME replicas 1 -> $ORIGINAL_REPLICAS (t+${elapsed}s, target was t+${CHAOS_RESTORE_AT}s)"
      scale_up_done=true
    fi
    sleep 1
  done
}
chaos_loop &
CHAOS_PID=$!

trap '
  kill "$CAPTURE_PID" "$TS_PID" "$CHAOS_PID" 2>/dev/null || true
  wait "$CAPTURE_PID" "$TS_PID" "$CHAOS_PID" 2>/dev/null || true
  if [ -n "$CHAOS_SCALE_AT" ]; then
    CUR_REPLICAS="$($OC get llmisvc "$LLMISVC_NAME" -n "$NAMESPACE" -o jsonpath="{.spec.replicas}" 2>/dev/null || true)"
    if [ -n "$CUR_REPLICAS" ] && [ "$CUR_REPLICAS" != "$ORIGINAL_REPLICAS" ]; then
      echo "[benchmark] safety-net restore: $LLMISVC_NAME replicas $CUR_REPLICAS -> $ORIGINAL_REPLICAS (chaos loop did not finish)" >&2
      $OC patch llmisvc "$LLMISVC_NAME" -n "$NAMESPACE" --type=merge -p "{\"spec\":{\"replicas\":$ORIGINAL_REPLICAS}}" >/dev/null 2>&1 || true
    fi
  fi
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

# --- Stop capture/timeseries/chaos, collect loadgen's own log, snapshot
# metrics after. Run the same restore check the EXIT trap would, THEN clear
# the trap -- clearing it first would leave a misconfigured chaos run with no
# safety net at all, since the run ends normally from here, not via the trap.
kill "$CAPTURE_PID" "$TS_PID" "$CHAOS_PID" 2>/dev/null || true
wait "$CAPTURE_PID" "$TS_PID" "$CHAOS_PID" 2>/dev/null || true
if [ -n "$CHAOS_SCALE_AT" ]; then
  CUR_REPLICAS="$($OC get llmisvc "$LLMISVC_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.replicas}' 2>/dev/null || true)"
  if [ -n "$CUR_REPLICAS" ] && [ "$CUR_REPLICAS" != "$ORIGINAL_REPLICAS" ]; then
    echo "[benchmark] safety-net restore: $LLMISVC_NAME replicas $CUR_REPLICAS -> $ORIGINAL_REPLICAS (chaos loop did not finish before the Job did)" >&2
    $OC patch llmisvc "$LLMISVC_NAME" -n "$NAMESPACE" --type=merge -p "{\"spec\":{\"replicas\":$ORIGINAL_REPLICAS}}" >/dev/null
    chaos_log "chaos: safety-net restore $LLMISVC_NAME replicas $CUR_REPLICAS -> $ORIGINAL_REPLICAS"
  fi
fi
trap - EXIT

LOADGEN_POD="$($OC get pods -n "$NAMESPACE" -l job-name="$JOB_NAME" -o jsonpath='{.items[0].metadata.name}')"
$OC logs "$LOADGEN_POD" -n "$NAMESPACE" > "$LOADGEN_LOG" 2>&1 || echo "[benchmark] WARNING: could not fetch loadgen pod log" >&2

# UNI-128: pull this run's per-tenant client-side record (requests sent,
# status tally, prompt/completion tokens actually received, aborts, errors)
# out of the pod's own stdout and into the results directory, so G2 (ledger
# cross-check) has it next to the EPP's before/after metric snapshots
# without needing the pod to still exist.
grep '^CLIENT_RECORD_JSON ' "$LOADGEN_LOG" | sed 's/^CLIENT_RECORD_JSON //' > "$CLIENT_RECORD_JSONL" || true

echo "[benchmark] metrics snapshot: after"
snapshot_metrics > "$METRICS_AFTER"
RUN_END="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
{ echo "# ts=$RUN_END epoch=$(date +%s)"; cat "$METRICS_AFTER"; } >> "$METRICS_TS"

# --- Build the report; its exit code becomes this script's exit code -------
set +e
REPORT_ARGS=(
  --scenario "$SCENARIO" --label "$LABEL" --enforce "$ENFORCE"
  --duration-seconds "$DURATION" --backend "$BACKEND"
  --epp-image-digest "$EPP_IMAGE_DIGEST" --namespace "$NAMESPACE" --epp-pod "$EPP_POD"
  --run-start "$RUN_START" --run-end "$RUN_END" --threshold-points "$THRESHOLD_POINTS"
  --metrics-before "$METRICS_BEFORE" --metrics-after "$METRICS_AFTER" --loadgen-log "$LOADGEN_LOG"
  --metrics-timeseries "$METRICS_TS" --timeline-config "$TIMELINE_CONFIG" --window-seconds "$WINDOW_SECONDS"
  --out-json "$REPORT_JSON" --out-md "$REPORT_MD"
)
if [ "$IS_CONTROL" = "true" ]; then
  REPORT_ARGS+=(--control)
fi
python3 -I "$(dirname "$0")/15-fairness-report.py" "${REPORT_ARGS[@]}"
REPORT_EXIT=$?
set -e

echo "[benchmark] report: $REPORT_JSON , $REPORT_MD"
echo "[benchmark] client-side request record: $CLIENT_RECORD_JSONL"
exit "$REPORT_EXIT"
