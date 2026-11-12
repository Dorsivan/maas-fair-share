#!/bin/bash
# UNI-247 follow-on: the 3x repeats came out mixed (9.7 PASS / 10.5 FAIL /
# 8.8 PASS), which is the ticket's own trigger for adding app1-flood-2x as a
# lower point. Three repeats, same settled config as uni247-batch.sh, serial
# on instance 1. Waits for uni247-batch.sh to exit first so nothing overlaps
# and its baseline restore has already run. No -e, same reason as there.
set -uo pipefail
export PATH="/paperclip/bin:$PATH"
cd "$(dirname "$0")/../../.."
LOG="deploy/poc/uni247/2x-batch.log"
: > "$LOG"
NAMESPACE=maas-fairness-poc
OC="oc --token=${OPENSHIFT_TOKEN}"

# uni247-batch.sh finished at 10:35:45Z. The original /proc wait for it
# deadlocked: it matched its own still-alive launcher shell, whose cmdline
# held this file's heredoc text. Relaunched (UNI-247, 11:2xZ) without that
# wait, and with TMPDIR under results/ (the launching session's TMPDIR is gone).
mkdir -p results/.tmp-uni247
export TMPDIR="$PWD/results/.tmp-uni247"
grep -q 'UNI247 BATCH COMPLETE' deploy/poc/uni247/batch.log || { echo "FATAL: uni247-batch.sh exited without completing -- not starting 2x" | tee -a "$LOG"; exit 1; }

while $OC get jobs -n "$NAMESPACE" -o jsonpath='{.items[?(@.status.active==1)].metadata.name}' 2>/dev/null | grep -q .; do
  echo "a loadgen job is still active, waiting..." | tee -a "$LOG"
  sleep 15
done

echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) patching weights to 30/10/60 ===" | tee -a "$LOG"
if ! ./deploy/poc/24-patch-all-weights.sh 30 10 60 >>"$LOG" 2>&1; then
  echo "FATAL: weight patch to 30/10/60 failed -- aborting, NOT restoring (unknown partial state)" | tee -a "$LOG"
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
  env ENFORCE_LIVE=true ./deploy/poc/15-fairness-benchmark.sh "$scenario" "$label" >>"$LOG" 2>&1
  local status=$?
  local dir
  dir="$(ls -dt results/*-"${label}" 2>/dev/null | head -1)"
  check_run "$dir"
  echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) END $label exit=$status dir=$dir ===" | tee -a "$LOG"
}

do_run app1-flood-2x uni-247-2x-rep1
do_run app1-flood-2x uni-247-2x-rep2
do_run app1-flood-2x uni-247-2x-rep3

echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) restoring baseline weights 20/10/65 ===" | tee -a "$LOG"
if ! ./deploy/poc/24-patch-all-weights.sh 20 10 65 >>"$LOG" 2>&1; then
  echo "WARNING: baseline weight restore to 20/10/65 FAILED -- cluster left at 30/10/60, needs manual fix" | tee -a "$LOG"
fi
echo "=== UNI247-2X BATCH COMPLETE $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee -a "$LOG"
