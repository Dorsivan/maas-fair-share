#!/bin/bash
# UNI-247: rebuild fairness-report.{json,md} for a run whose
# 15-fairness-benchmark.sh died before the report step (the UNI-224
# kvCacheUtilThreshold grep under pipefail -- fixed in the same commit).
# Every input is an artifact already in the run dir or the batch log; the
# args mirror REPORT_ARGS in 15-fairness-benchmark.sh. RUN_END is the last
# "# ts=" line of metrics-timeseries.txt (written from the same $RUN_END);
# RUN_START is approximated by its first "# ts=" line (taken seconds later).
# Usage: uni247-rebuild-report.sh <run-dir> <scenario> <label>
set -uo pipefail
cd "$(dirname "$0")/../../.."
DIR="$1" SCENARIO="$2" LABEL="$3"
LOG=deploy/poc/uni247/batch.log
TS="$DIR/metrics-timeseries.txt"
RUN_START="$(grep -m1 '^# ts=' "$TS" | sed -E 's/^# ts=([^ ]+).*/\1/')"
RUN_END="$(grep '^# ts=' "$TS" | tail -1 | sed -E 's/^# ts=([^ ]+).*/\1/')"
ENFORCE="$(awk '/^llm_d_epp_maas_fairness_enforcing/ {print ($2==1)?"true":"false"}' "$DIR/metrics-before.txt")"
# This run's block of the batch log: from its "artifact dir:" line to its END line.
BLOCK="$(awk -v d="$DIR" 'index($0, "artifact dir:") && index($0, d) {on=1} on {print} on && /^=== .* END / {exit}' "$LOG")"
EPP_POD="$(printf '%s\n' "$BLOCK" | grep -oP 'target pod is now \K\S+' | tail -1 || true)"
DIGEST="$(printf '%s\n' "$BLOCK" | grep -oP 'image: \K\S+' | head -1 || true)"
read -r IN OUT CACHED < <(printf '%s\n' "$BLOCK" | grep -oP 'ledger cost model.*input=\K\S+ output=\S+ cached=\S+' | sed 's/output=//; s/cached=//' || true)
CONTROL=()
python3 -I deploy/poc/15-fairness-report.py \
  --scenario "$SCENARIO" --label "$LABEL" --enforce "$ENFORCE" \
  --duration-seconds 240 --backend "vllm-gpu (real)" \
  --epp-image-digest "$DIGEST" --namespace maas-fairness-poc --epp-pod "$EPP_POD" \
  --run-start "$RUN_START" --run-end "$RUN_END" --threshold-points 10 \
  --metrics-before "$DIR/metrics-before.txt" --metrics-after "$DIR/metrics-after.txt" \
  --loadgen-log "$DIR/loadgen.log" --metrics-timeseries "$TS" \
  --timeline-config "$DIR/timeline-config.json" --window-seconds 10 \
  --client-record-jsonl "$DIR/client-request-summary.jsonl" \
  --input-token-weight "${IN:-1.0}" --output-token-weight "${OUT:-1.0}" \
  --cached-input-token-weight "${CACHED:-1.0}" --ledger-tolerance-pct 10 \
  --queue-depth-threshold 32 --kv-cache-util-threshold 0.8 \
  --out-json "$DIR/fairness-report.json" --out-md "$DIR/fairness-report.md"
echo "rebuilt $DIR exit=$? epp_pod=$EPP_POD start=$RUN_START end=$RUN_END enforce=$ENFORCE"
