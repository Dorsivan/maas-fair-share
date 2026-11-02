#!/bin/bash
# UNI-140 (B6): companion sampler for a long (90-120 min) benchmark run.
#
# 15-fairness-benchmark.sh's snapshot_metrics() only keeps lines matching
# ^llm_d_epp_maas_fairness_ or ^llm_d_epp_request_(input|output|cached)_tokens_
# (see its own comment) -- so neither the EPP process's own memory
# (process_resident_memory_bytes, a Go client_golang default collector) nor
# the flow-control queue's eviction counter
# (llm_d_epp_flow_control_requests_evicted_total, the only real eviction
# sweep in this system -- pkg/fairness/weightedlas's own group-state table
# has none by design, see deploy/epp-config.yaml's "deliberately no eviction
# TTL" comment, because the group set is closed and bounded at
# len(groups)+1) is ever captured. Run this alongside 15-fairness-benchmark.sh
# for the same duration to get both, without touching that script's tested
# grep filter or output shape.
#
# This also re-resolves the EPP pod by selector on every sample (not once up
# front), so a mid-run restart is picked up as a pod-name change rather than
# silently sampling a gone pod.
#
# Usage:
#   OPENSHIFT_TOKEN=... ./deploy/poc/18-soak-monitor.sh <artifact-dir> <duration-seconds> [sample-interval-seconds]
#
# Writes into <artifact-dir>:
#   memory-timeseries.txt     one line per sample: ts, epoch, pod, restarts,
#                             container_memory (oc adm top, working-set,
#                             Mi), process_resident_memory_bytes (EPP's own
#                             /metrics, bytes)
#   metrics-full-before.txt   unfiltered /metrics scrape at start
#   metrics-full-after.txt    unfiltered /metrics scrape at end
set -euo pipefail

ARTIFACT_DIR="${1:?usage: $0 <artifact-dir> <duration-seconds> [sample-interval-seconds]}"
DURATION="${2:?usage: $0 <artifact-dir> <duration-seconds> [sample-interval-seconds]}"
SAMPLE_INTERVAL="${3:-60}"

NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
OC="oc --token=${OPENSHIFT_TOKEN:?set OPENSHIFT_TOKEN} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"
EPP_SELECTOR="${EPP_SELECTOR:-app.kubernetes.io/component=llminferenceservice-router-scheduler,app.kubernetes.io/name=maas-vllm-gpu}"
EPP_CONTAINER="${EPP_CONTAINER:-main}"

mkdir -p "$ARTIFACT_DIR"
MEM_TS="$ARTIFACT_DIR/memory-timeseries.txt"
echo "# ts epoch pod restarts working_set_mem resident_bytes" > "$MEM_TS"

current_pod() {
  $OC get pods -n "$NAMESPACE" -l "$EPP_SELECTOR" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true
}

METRICS_TOKEN="$($OC get secret maas-epp-metrics-reader-token -n "$NAMESPACE" -o jsonpath='{.data.token}' | base64 -d)"
EPP_METRICS_SVC_IP="${EPP_METRICS_SVC_IP:-}"
if [ -z "$EPP_METRICS_SVC_IP" ]; then
  EPP_METRICS_SVC_IP="$($OC get svc maas-vllm-gpu-epp-service -n "$NAMESPACE" -o jsonpath='{.spec.clusterIP}')"
fi

snapshot_full_metrics() {
  curl -sS -m 10 -H "Authorization: Bearer $METRICS_TOKEN" "http://${EPP_METRICS_SVC_IP}:9090/metrics"
}

resident_bytes_from_metrics() {
  awk '/^process_resident_memory_bytes/ {print $2; exit}'
}

echo "[soak-monitor] start: $(date -u +%Y-%m-%dT%H:%M:%SZ) duration=${DURATION}s interval=${SAMPLE_INTERVAL}s"
snapshot_full_metrics > "$ARTIFACT_DIR/metrics-full-before.txt"

END_EPOCH=$(( $(date +%s) + DURATION ))
while [ "$(date +%s)" -lt "$END_EPOCH" ]; do
  TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  EPOCH="$(date +%s)"
  POD="$(current_pod)"
  if [ -n "$POD" ]; then
    RESTARTS="$($OC get pod "$POD" -n "$NAMESPACE" -o jsonpath='{.status.containerStatuses[0].restartCount}' 2>/dev/null || echo "n/a")"
    WORKING_SET="$($OC adm top pod "$POD" -n "$NAMESPACE" --containers --no-headers 2>/dev/null | awk -v c="$EPP_CONTAINER" '$2==c {print $4}')"
    RESIDENT="$(snapshot_full_metrics 2>/dev/null | resident_bytes_from_metrics || echo "n/a")"
  else
    RESTARTS="n/a"; WORKING_SET="n/a"; RESIDENT="n/a"
  fi
  echo "$TS $EPOCH ${POD:-n/a} $RESTARTS ${WORKING_SET:-n/a} ${RESIDENT:-n/a}" | tee -a "$MEM_TS"
  sleep "$SAMPLE_INTERVAL"
done

snapshot_full_metrics > "$ARTIFACT_DIR/metrics-full-after.txt"
echo "[soak-monitor] done: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
