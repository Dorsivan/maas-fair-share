#!/bin/bash
# UNI-247: three repeats each of app1-flood-3x and app1-flood-moderate (4x),
# same settled config UNI-245 used (weights 30/10/60, queueDepthThreshold 32,
# ENFORCE_LIVE=true, EPP image sha256:c8a0882..., DURATION default 240s),
# run serially on instance 1 (this repo's deployment) per Khala's UNI-231/
# UNI-252 caution -- parallel scored runs across lanes aren't trusted yet.
# Scratch output goes under this repo working tree (results/ is gitignored),
# not $TMPDIR -- see process_tmpdir_torn_down_mid_background_run. No -e: one
# transient failure must not kill the rest of the batch (see
# process_set_minus_e_kills_backgrounded_loops_on_first_failure).
set -uo pipefail
export PATH="/paperclip/bin:$PATH"
cd "$(dirname "$0")/../../.."
LOG="deploy/poc/uni247/batch.log"
: > "$LOG"
NAMESPACE=maas-fairness-poc
OC="oc --token=${OPENSHIFT_TOKEN}"

while $OC get jobs -n "$NAMESPACE" -o jsonpath='{.items[?(@.status.active==1)].metadata.name}' 2>/dev/null | grep -q .; do
  echo "a loadgen job is still active, waiting..." | tee -a "$LOG"
  sleep 15
done

echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) patching weights to 30/10/60 ===" | tee -a "$LOG"
if ! OPENSHIFT_TOKEN="$OPENSHIFT_TOKEN" ./deploy/poc/24-patch-all-weights.sh 30 10 60 >>"$LOG" 2>&1; then
  echo "FATAL: weight patch to 30/10/60 failed -- aborting batch, NOT running benchmarks, NOT restoring (unknown partial state)" | tee -a "$LOG"
  exit 1
fi

check_run() {
  local dir="$1"
  if [ -z "$dir" ] || [ ! -f "$dir/metrics-before.txt" ]; then
    echo "CHECK FAIL: no metrics-before.txt found for $dir" | tee -a "$LOG"
    return
  fi
  local weights enforcing
  weights="$(grep '^llm_d_epp_maas_fairness_configured_weight' "$dir/metrics-before.txt" | sort | tr '\n' ' ')"
  enforcing="$(awk '/^llm_d_epp_maas_fairness_enforcing/ {print $2}' "$dir/metrics-before.txt")"
  echo "CHECK $dir: enforcing=$enforcing weights: $weights" | tee -a "$LOG"
}

do_run() {
  local scenario="$1" label="$2"
  echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) START $label ($scenario) ===" | tee -a "$LOG"
  env ENFORCE_LIVE=true OPENSHIFT_TOKEN="$OPENSHIFT_TOKEN" \
    ./deploy/poc/15-fairness-benchmark.sh "$scenario" "$label" >>"$LOG" 2>&1
  local status=$?
  local dir
  dir="$(ls -dt results/*-"${label}" 2>/dev/null | head -1)"
  check_run "$dir"
  echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) END $label exit=$status dir=$dir ===" | tee -a "$LOG"
}

do_run app1-flood-3x uni-247-3x-rep1
do_run app1-flood-3x uni-247-3x-rep2
do_run app1-flood-3x uni-247-3x-rep3
do_run app1-flood-moderate uni-247-4x-rep1
do_run app1-flood-moderate uni-247-4x-rep2
do_run app1-flood-moderate uni-247-4x-rep3

echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) restoring baseline weights 20/10/65 ===" | tee -a "$LOG"
if ! OPENSHIFT_TOKEN="$OPENSHIFT_TOKEN" ./deploy/poc/24-patch-all-weights.sh 20 10 65 >>"$LOG" 2>&1; then
  echo "WARNING: baseline weight restore to 20/10/65 FAILED -- cluster left at 30/10/60, needs manual fix" | tee -a "$LOG"
fi

echo "=== UNI247 BATCH COMPLETE $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee -a "$LOG"
