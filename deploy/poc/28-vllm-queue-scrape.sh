#!/bin/bash
# UNI-289: sample vLLM's own num_requests_running/num_requests_waiting gauges
# (summed across replicas) on the same ~10s cadence 15-fairness-benchmark.sh's
# WINDOW_SECONDS EPP scrape loop uses (UNI-127), so the two timeseries can be
# correlated by wall-clock timestamp after the fact.
#
# UNI-288's report flagged this as the one thing that would confirm or kill
# the sim's "EPP holds only ~8% of the in-flight population" claim directly:
# "the next live run should record llm_d_epp_flow_control_queue_size per flow
# alongside vLLM num_requests_waiting." llm_d_epp_flow_control_queue_size is
# already captured by 15-fairness-benchmark.sh's own metrics-timeseries.txt
# (EPP /metrics scrape); this script is the missing vLLM-side half. It does
# not touch or replace that mechanism -- additive instrumentation, run
# alongside it, not a rebuild (see docs/runbook.md and 16-gate-correlation.py
# module docstrings for why those stay as-is).
#
# Runs standalone against wall-clock time, independent of
# 15-fairness-benchmark.sh's own artifact-dir naming, so it can be started a
# moment before that script and stopped a moment after -- correlate by the
# epoch column, not by file layout.
#
# Usage:
#   OPENSHIFT_TOKEN=... deploy/poc/28-vllm-queue-scrape.sh <duration-seconds> <outfile>
set -euo pipefail

DURATION="${1:?usage: $0 <duration-seconds> <outfile>}"
OUT="${2:?usage: $0 <duration-seconds> <outfile>}"
NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
SELECTOR="${SELECTOR:-app.kubernetes.io/component=llminferenceservice-workload,app.kubernetes.io/name=maas-vllm-gpu}"
METRICS_PORT="${METRICS_PORT:-8000}"
INTERVAL="${INTERVAL:-10}"
OC="oc --token=${OPENSHIFT_TOKEN:?set OPENSHIFT_TOKEN} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"

: > "$OUT"
end=$(( $(date +%s) + DURATION ))
while [ "$(date +%s)" -lt "$end" ]; do
  epoch="$(date +%s)"
  pods="$($OC get pods -n "$NAMESPACE" -l "$SELECTOR" -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' 2>/dev/null || true)"
  running=0
  waiting=0
  for pod in $pods; do
    metrics="$($OC get --raw "/api/v1/namespaces/$NAMESPACE/pods/https:$pod:$METRICS_PORT/proxy/metrics" 2>/dev/null || true)"
    [ -n "$metrics" ] || continue
    r="$(printf '%s\n' "$metrics" | grep -E '^vllm:num_requests_running\{' | awk '{sum+=$NF} END{print sum+0}')"
    w="$(printf '%s\n' "$metrics" | grep -E '^vllm:num_requests_waiting\{' | awk '{sum+=$NF} END{print sum+0}')"
    running=$(awk -v a="$running" -v b="$r" 'BEGIN{print a+b}')
    waiting=$(awk -v a="$waiting" -v b="$w" 'BEGIN{print a+b}')
  done
  echo "epoch=$epoch running=$running waiting=$waiting pods=$(echo "$pods" | wc -w)" >> "$OUT"
  sleep "$INTERVAL"
done
