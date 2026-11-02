#!/bin/bash
# UNI-187: off-GPU smoke test for the N-group EPP tables.
#
# Proves, without a GPU run and without touching the shared maas-epp-config,
# that six NEW identities (app3..app8) authenticate through MaaS and land in
# six distinct EPP queues rather than in `unclassified`.
#
# Why it looks the way it does:
#   - maas-vllm-cpu and maas-vllm-gpu BOTH read ConfigMap maas-epp-config, so
#     loading a 6-group table there would recreate the GPU EPP and zero its
#     counters mid-chain. Instead this repoints ONLY maas-vllm-cpu's scheduler
#     at a separate ConfigMap (maas-epp-config-smoke, rendered from
#     00-config.yaml by epp-groups/render.py) and puts it back afterwards.
#   - app3..app8, not app1..app6: the pre-UNI-187 subscriptions
#     (app1-production, app2-batch) reference only maas-vllm-gpu, so their keys
#     are not authorised on the CPU route. The new ones reference both.
#   - maas-vllm-cpu sits at replicas 0 (UNI-88/98). It is raised to 1 for the
#     run and returned to whatever it was. The GPU workers carry no taint, so
#     the CPU pod (2 CPU / 8Gi request) may land on one -- harmless with the
#     GPU pool idle, which is why the preflight refuses to start otherwise.
#
# Run as the engineer identity (paperclip:poc-agent); needs llminferenceservice
# patch, configmap/job create+delete and secret get in maas-fairness-poc.
#   PATH=/paperclip/bin:$PATH deploy/poc/20-n-group-smoke.sh
# Artifacts: results/<UTC>-uni-187-n-group-smoke/ (never contains key values).
set -euo pipefail

NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
LLMISVC="maas-vllm-cpu"
SMOKE_CM="maas-epp-config-smoke"
JOB="maas-loadgen-smoke"
GROUPS_UNDER_TEST="app3 app4 app5 app6 app7 app8"
WORKERS_PER_GROUP="${WORKERS_PER_GROUP:-2}"
DURATION="${DURATION:-60}"
READY_TIMEOUT="${READY_TIMEOUT:-600}"
OC="oc --token=${OPENSHIFT_TOKEN:?} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${OUT:-$HERE/../../results/$(date -u +%Y%m%dT%H%M%SZ)-uni-187-n-group-smoke}"
mkdir -p "$OUT"
log() { echo "[smoke] $*" | tee -a "$OUT/smoke.log"; }

log "identity: $($OC whoami)"

# --- preflight: nothing else on the pool, every key present -----------------
active="$($OC get jobs -n "$NAMESPACE" -o jsonpath='{range .items[?(@.status.active)]}{.metadata.name}{" "}{end}')"
if [ -n "$active" ]; then
  log "ABORT: active job(s) in $NAMESPACE: $active -- one load run at a time"; exit 1
fi
# Names only -- the template never dereferences a value.
$OC get secret maas-loadgen-keys -n "$NAMESPACE" \
  -o go-template='{{range $k, $v := .data}}{{$k}}{{"\n"}}{{end}}' > "$OUT/key-names.txt"
for g in $GROUPS_UNDER_TEST; do
  grep -qx "$g" "$OUT/key-names.txt" || { log "ABORT: no key '$g' in secret/maas-loadgen-keys"; exit 1; }
done

ORIG_REF="$($OC get llminferenceservice "$LLMISVC" -n "$NAMESPACE" -o jsonpath='{.spec.router.scheduler.config.ref.name}')"
ORIG_REPLICAS="$($OC get llminferenceservice "$LLMISVC" -n "$NAMESPACE" -o jsonpath='{.spec.replicas}')"
ORIG_REPLICAS="${ORIG_REPLICAS:-0}"
log "before: $LLMISVC config.ref=$ORIG_REF replicas=$ORIG_REPLICAS"
$OC get llminferenceservice "$LLMISVC" -n "$NAMESPACE" -o yaml > "$OUT/llmisvc-before.yaml"

restore() {
  set +e
  log "restoring: $LLMISVC config.ref=$ORIG_REF replicas=$ORIG_REPLICAS; deleting job/$JOB cm/$SMOKE_CM"
  $OC patch llminferenceservice "$LLMISVC" -n "$NAMESPACE" --type=merge -p \
    "{\"spec\":{\"replicas\":$ORIG_REPLICAS,\"router\":{\"scheduler\":{\"config\":{\"ref\":{\"name\":\"$ORIG_REF\"}}}}}}" >/dev/null
  $OC delete job "$JOB" -n "$NAMESPACE" --ignore-not-found --wait=false >/dev/null
  $OC delete configmap "$SMOKE_CM" -n "$NAMESPACE" --ignore-not-found >/dev/null
  $OC get llminferenceservice "$LLMISVC" -n "$NAMESPACE" \
    -o jsonpath='{"after: config.ref="}{.spec.router.scheduler.config.ref.name}{" replicas="}{.spec.replicas}{"\n"}' \
    | tee -a "$OUT/smoke.log"
}
trap restore EXIT

# --- point the CPU EPP at the 6-group table ---------------------------------
python3 -I "$HERE/epp-groups/render.py" --verify >/dev/null \
  || { log "ABORT: epp-groups renders are stale vs 00-config.yaml"; exit 1; }
$OC apply -f "$HERE/epp-groups/smoke-6-group.yaml" >/dev/null
$OC patch llminferenceservice "$LLMISVC" -n "$NAMESPACE" --type=merge -p \
  "{\"spec\":{\"replicas\":1,\"router\":{\"scheduler\":{\"config\":{\"ref\":{\"name\":\"$SMOKE_CM\"}}}}}}" >/dev/null
log "patched $LLMISVC -> config.ref=$SMOKE_CM replicas=1"

METRICS_TOKEN="$($OC get secret maas-epp-metrics-reader-token -n "$NAMESPACE" -o jsonpath='{.data.token}' | base64 -d)"
EPP_IP="$($OC get svc maas-vllm-cpu-epp-service -n "$NAMESPACE" -o jsonpath='{.spec.clusterIP}')"
scrape() { curl -sS -m 10 -H "Authorization: Bearer $METRICS_TOKEN" "http://$EPP_IP:9090/metrics" 2>/dev/null | grep '^llm_d_epp_maas_fairness_' || true; }

# Ready = the CPU EPP reports a configured weight for every group under test
# (i.e. the NEW config is the one loaded) AND the model pod is Ready.
deadline=$(( $(date +%s) + READY_TIMEOUT ))
while :; do
  cw="$(scrape | grep -c '^llm_d_epp_maas_fairness_configured_weight{fairness_id="app[3-8]"}' || true)"
  ready="$($OC get pods -n "$NAMESPACE" -l app.kubernetes.io/name=$LLMISVC,app.kubernetes.io/component=llminferenceservice-workload \
    -o jsonpath='{range .items[*]}{.status.containerStatuses[0].ready}{" "}{end}' 2>/dev/null || true)"
  [ "$cw" -ge 6 ] && [[ "$ready" == *true* ]] && break
  if [ "$(date +%s)" -ge "$deadline" ]; then
    log "ABORT: not ready after ${READY_TIMEOUT}s (configured_weight rows for app3..8=$cw, model ready=[$ready])"
    $OC get pods -n "$NAMESPACE" -l app.kubernetes.io/name=$LLMISVC -o wide >> "$OUT/smoke.log" 2>&1
    exit 1
  fi
  sleep 5
done
$OC get pods -n "$NAMESPACE" -l app.kubernetes.io/name=$LLMISVC -o wide >> "$OUT/smoke.log" 2>&1
log "CPU EPP loaded the smoke table and the model is Ready"
scrape > "$OUT/metrics-before.txt"

# --- the load: same run.sh as 04-loadgen.yaml, different Job name -----------
lg=""; for g in $GROUPS_UNDER_TEST; do lg="$lg $g:$WORKERS_PER_GROUP"; done
$OC apply -f - >/dev/null << EOF
apiVersion: batch/v1
kind: Job
metadata: {name: $JOB, namespace: $NAMESPACE}
spec:
  backoffLimit: 0
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: loadgen
          image: registry.access.redhat.com/ubi9/ubi:latest
          command: ["/bin/bash", "/script/run.sh"]
          env:
            - {name: LOADGEN_GROUPS, value: "${lg# }"}
            - {name: MODELPATH, value: "/maas-fairness-poc/$LLMISVC"}
            - {name: DURATION, value: "$DURATION"}
          volumeMounts:
            - {name: script, mountPath: /script}
            - {name: keys, mountPath: /keys, readOnly: true}
          resources:
            requests: {cpu: 100m, memory: 256Mi}
            limits: {cpu: "1", memory: 1Gi}
          securityContext:
            allowPrivilegeEscalation: false
            capabilities: {drop: ["ALL"]}
            runAsNonRoot: true
            seccompProfile: {type: RuntimeDefault}
      volumes:
        - {name: script, configMap: {name: maas-loadgen, defaultMode: 0755}}
        - {name: keys, secret: {secretName: maas-loadgen-keys}}
EOF
log "started job/$JOB: LOADGEN_GROUPS='${lg# }' DURATION=$DURATION"
$OC wait --for=condition=complete "job/$JOB" -n "$NAMESPACE" --timeout=$(( DURATION + 300 ))s >/dev/null \
  || log "WARN: job/$JOB did not report Complete -- reading what it produced anyway"
$OC logs "job/$JOB" -n "$NAMESPACE" > "$OUT/loadgen.log" 2>&1 || true
scrape > "$OUT/metrics-after.txt"

# --- verdict ----------------------------------------------------------------
grep '^load: UNI-179' "$OUT/loadgen.log" | tee -a "$OUT/smoke.log" || true
python3 -I - "$OUT/metrics-before.txt" "$OUT/metrics-after.txt" $GROUPS_UNDER_TEST << 'PYEOF' | tee -a "$OUT/smoke.log"
import re, sys
def load(p):
    d = {}
    for line in open(p):
        m = re.match(r'(llm_d_epp_maas_fairness_\w+)(\{[^}]*\})?\s+(\S+)', line)
        if m:
            d[(m.group(1), m.group(2) or "")] = float(m.group(3))
    return d
b, a = load(sys.argv[1]), load(sys.argv[2])
groups = sys.argv[3:]
def delta(name, labels=""):
    return a.get((name, labels), 0.0) - b.get((name, labels), 0.0)
ok = True
print("group         configured_weight  dispatch_delta")
for g in groups + ["unclassified"]:
    lab = '{fairness_id="%s"}' % g
    w = a.get(("llm_d_epp_maas_fairness_configured_weight", lab))
    dd = delta("llm_d_epp_maas_fairness_dispatch_total", lab)
    print(f"{g:<13} {str(w):>17}  {dd:>14.0f}")
    if g != "unclassified" and (w is None or dd <= 0):
        ok = False
    if g == "unclassified" and dd != 0:
        ok = False
um = sum(v for (n, _), v in a.items() if n == "llm_d_epp_maas_fairness_unmatched_subscriptions_total") \
   - sum(v for (n, _), v in b.items() if n == "llm_d_epp_maas_fairness_unmatched_subscriptions_total")
print(f"unmatched_subscriptions_total delta: {um:.0f}")
ok = ok and um == 0
if ok:
    print(f"SMOKE PASS: {len(groups)} groups each dispatched in their own queue, none in unclassified")
else:
    print("SMOKE FAIL: a group with no weight/dispatches, or unclassified/unmatched traffic -- see table")
sys.exit(0 if ok else 1)
PYEOF
