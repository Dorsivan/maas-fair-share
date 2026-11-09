#!/bin/bash
# UNI-214: per-replica dispatch split and prefix-cache hit ratio for one run.
#
# The EPP exposes no per-endpoint request counter (llm_d_epp_per_endpoint_queue_size
# is a gauge, and only says whether a replica had a backlog, not how many
# requests it served). Each vLLM replica does count its own work, so this reads
# every maas-vllm-gpu workload pod's /metrics through the API-server pod proxy
# (no port-forward, no pod-IP reachability needed) before and after a run and
# diffs the counters:
#   vllm:request_success_total        -> requests finished on that replica
#   vllm:prefix_cache_{hits,queries}_total -> token-level prefix-cache hit ratio
#   vllm:prompt_tokens_total          -> prompt tokens prefilled there
#
# Usage:
#   OPENSHIFT_TOKEN=... deploy/poc/21-replica-split.sh snapshot <file>
#   deploy/poc/21-replica-split.sh diff <before-file> <after-file>
#
# Typical wrap of a benchmark run:
#   deploy/poc/21-replica-split.sh snapshot /tmp/before.txt
#   deploy/poc/15-fairness-benchmark.sh full-contention my-label
#   deploy/poc/21-replica-split.sh snapshot /tmp/after.txt
#   deploy/poc/21-replica-split.sh diff /tmp/before.txt /tmp/after.txt
#
# Counters are cumulative since each vLLM process started, so a replica that
# restarts between the two snapshots makes its row meaningless; the diff marks
# any negative delta as RESTARTED instead of printing it.
set -euo pipefail

NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
SELECTOR="${SELECTOR:-app.kubernetes.io/component=llminferenceservice-workload,app.kubernetes.io/name=maas-vllm-gpu}"
METRICS_PORT="${METRICS_PORT:-8000}"

case "${1:-}" in
  snapshot)
    out="${2:?usage: $0 snapshot <file>}"
    OC="oc --token=${OPENSHIFT_TOKEN:?set OPENSHIFT_TOKEN} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"
    pods="$($OC get pods -n "$NAMESPACE" -l "$SELECTOR" -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}')"
    [ -n "$pods" ] || { echo "no pods match $SELECTOR in $NAMESPACE" >&2; exit 1; }
    : > "$out"
    for pod in $pods; do
      $OC get --raw "/api/v1/namespaces/$NAMESPACE/pods/https:$pod:$METRICS_PORT/proxy/metrics" \
        | grep -E '^vllm:(request_success_total|prefix_cache_hits_total|prefix_cache_queries_total|prompt_tokens_total)\{' \
        | sed "s/^/$pod /" >> "$out"
    done
    echo "# taken $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$out"
    ;;
  diff)
    before="${2:?usage: $0 diff <before> <after>}"
    after="${3:?usage: $0 diff <before> <after>}"
    python3 -I - "$before" "$after" <<'PY'
import sys
from collections import defaultdict

def load(path):
    vals = defaultdict(float)
    for line in open(path):
        if line.startswith("#") or not line.strip():
            continue
        pod, series, value = line.split()
        name = series.split("{", 1)[0].removeprefix("vllm:")
        vals[(pod, name)] += float(value)  # sums request_success_total across finished_reason
    return vals

b, a = load(sys.argv[1]), load(sys.argv[2])
pods = sorted({p for p, _ in a})
rows, total = [], 0.0
for pod in pods:
    d = {n: a[(pod, n)] - b[(pod, n)] for n in
         ("request_success_total", "prefix_cache_hits_total", "prefix_cache_queries_total", "prompt_tokens_total")}
    restarted = any(v < 0 for v in d.values())
    rows.append((pod, d, restarted))
    if not restarted:
        total += d["request_success_total"]

print("| replica | requests finished | share | prompt tokens | prefix-cache hit ratio |")
print("|---|---|---|---|---|")
for pod, d, restarted in rows:
    if restarted:
        print(f"| `{pod}` | RESTARTED | - | - | - |")
        continue
    req = d["request_success_total"]
    share = f"{100 * req / total:.1f}%" if total else "-"
    q = d["prefix_cache_queries_total"]
    hit = f"{100 * d['prefix_cache_hits_total'] / q:.1f}%" if q else "-"
    print(f"| `{pod}` | {int(req)} | {share} | {int(d['prompt_tokens_total'])} | {hit} |")
print(f"| **total** | {int(total)} | | | |")
PY
    ;;
  *)
    sed -n '2,26p' "$0" >&2
    exit 2
    ;;
esac
