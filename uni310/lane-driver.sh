#!/bin/bash
# UNI-310: run rows.txt, in order, one scenario at a time, on ONE lane.
#   uni310/lane-driver.sh <namespace> [rows-file] [label-tag]
# Launch one per lane (detached: nohup setsid ... &), never two per lane.
#
# Per row: put the lane's maas-epp-config into the row's config (default /
# 3-group weights / 6-group table, all rendered through lanes.py so the
# lane's -lN match suffix and the SFQ stamp settings come from 00-config.yaml),
# health-gate the lane, snapshot vLLM replica counters, run the benchmark,
# snapshot again, then restore 00-config and PROVE the restore with a
# server-side dry-run diff. A restore that does not diff clean stops the
# driver -- the next row would otherwise run on the wrong config.
#
# No `set -e` on purpose: one failed scrape must not kill a 5-hour batch.
set -uo pipefail
export PATH="/paperclip/bin:$PATH"
NS="${1:?namespace}"
HERE="$(cd "$(dirname "$0")" && pwd)"
ROWS="${2:-$HERE/rows.txt}"
TAG="${3:-r1}"
REPO="$(cd "$HERE/.." && pwd)"
cd "$REPO"
LANE="$(NAMESPACE="$NS" python3 -I deploy/poc/lanes.py env | sed -n 's/^LANE=//p')"
[ -n "$LANE" ] || { echo "unknown lane for $NS" >&2; exit 2; }
[ "$NS" != "maas-fairness-poc" ] || { echo "UNI-310 does not drive lane 1 (UNI-296 owns it)" >&2; exit 2; }
D="$HERE/state/l$LANE-$TAG"
mkdir -p "$D/tmp"
export TMPDIR="$D/tmp"          # not the session's TMPDIR: it dies with the session
LOG="$D/driver.log"
echo $$ > "$D/pid"
rm -f "$D/DONE"
OC="oc --token=${OPENSHIFT_TOKEN:?} --server=https://api.ocp.paladinaura.com:6443"
export NAMESPACE="$NS"

log() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) [l$LANE] $*" | tee -a "$LOG"; }

METRICS_TOKEN="$($OC get secret maas-epp-metrics-reader-token -n "$NS" -o jsonpath='{.data.token}' | base64 -d)"
epp_ip() { $OC get svc maas-vllm-gpu-epp-service -n "$NS" -o jsonpath='{.spec.clusterIP}'; }
read_enforcing() {
  curl -sS -m 10 -H "Authorization: Bearer $METRICS_TOKEN" "http://$(epp_ip):9090/metrics" 2>/dev/null \
    | awk '/^llm_d_epp_maas_fairness_enforcing/ {print ($2==1)?"1":"0"}'
}
wait_enforcing() {
  local want="$1" waited=0 v
  while :; do
    v="$(read_enforcing)"
    [ "$v" = "$want" ] && { log "confirmed llm_d_epp_maas_fairness_enforcing=$want"; return 0; }
    [ "$waited" -ge 240 ] && { log "TIMEOUT waiting for enforcing=$want (got '${v:-none}')"; return 1; }
    sleep 3; waited=$((waited+3))
  done
}

render_default() { python3 -I deploy/poc/lanes.py render deploy/poc/00-config.yaml > "$D/want-default.yaml"; }

config_matches_default() {
  render_default
  $OC apply --dry-run=server -f "$D/want-default.yaml" -o jsonpath='{.data.epp}' > "$D/want.epp" 2>>"$LOG" || return 1
  $OC get cm maas-epp-config -n "$NS" -o jsonpath='{.data.epp}' > "$D/live.epp" || return 1
  diff -q "$D/want.epp" "$D/live.epp" >/dev/null
}

wait_epp_ready() {
  local waited=0 r
  sleep 10
  while :; do
    r="$($OC get pods -n "$NS" -l app.kubernetes.io/component=llminferenceservice-router-scheduler \
          -o jsonpath='{range .items[*]}{.status.containerStatuses[0].ready}{" "}{.metadata.deletionTimestamp}{"\n"}{end}')"
    # exactly one pod, ready, not terminating
    if [ "$(echo "$r" | grep -c .)" = 1 ] && echo "$r" | grep -qx 'true '; then return 0; fi
    [ "$waited" -ge 300 ] && { log "TIMEOUT waiting for one ready EPP pod: $(echo $r)"; return 1; }
    sleep 5; waited=$((waited+5))
  done
}

apply_config() {
  local cfg="$1"
  case "$cfg" in
    default)
      if config_matches_default; then log "config: already default"; return 0; fi
      $OC apply -f "$D/want-default.yaml" >>"$LOG" 2>&1 ;;
    w3:*)
      local w="${cfg#w3:}"; local a b c; IFS=/ read -r a b c <<< "$w"
      render_default
      python3 -I - "$D/want-default.yaml" "$D/want-cfg.yaml" "$a" "$b" "$c" <<'PYEOF'
import sys, re
src, dst, w1, w2, w3 = sys.argv[1:6]
text = open(src).read()
for group, val in (("app1", w1), ("app2", w2), ("end-users", w3)):
    pat = re.compile(r'(\{\s*name:\s*' + re.escape(group) + r',\s*weight:\s*)[0-9.]+')
    text, n = pat.subn(lambda m: m.group(1) + val, text, count=1)
    if n != 1:
        sys.exit(f"group {group}: weight entry not found")
open(dst, "w").write(text)
PYEOF
      [ $? -eq 0 ] || return 1
      $OC apply -f "$D/want-cfg.yaml" >>"$LOG" 2>&1 ;;
    w6:*)
      python3 -I deploy/poc/epp-groups/render.py 6 --weights "${cfg#w6:}" > "$D/six.yaml" || return 1
      python3 -I deploy/poc/lanes.py render "$D/six.yaml" > "$D/want-cfg.yaml" || return 1
      $OC apply -f "$D/want-cfg.yaml" >>"$LOG" 2>&1 ;;
    *) log "unknown config $cfg"; return 1 ;;
  esac
  local rc=$?
  [ $rc -eq 0 ] || { log "apply failed for $cfg"; return 1; }
  log "config: applied $cfg; live groups: $($OC get cm maas-epp-config -n "$NS" -o jsonpath='{.data.epp}' | grep -oE 'name: (app[0-9]+|end-users), *weight: *[0-9.]+' | sed 's/name: //;s/, *weight: */=/' | tr '\n' ' ')"
  wait_epp_ready
}

lane_healthy() {
  local v e j
  v="$($OC get deployment maas-vllm-gpu-kserve -n "$NS" -o jsonpath='{.status.readyReplicas}/{.spec.replicas}')"
  j="$($OC get jobs -n "$NS" -o jsonpath='{.items[?(@.status.active==1)].metadata.name}')"
  if [ "$v" != "2/2" ] || [ -n "$j" ]; then log "lane not healthy: vllm=$v active-jobs='$j'"; return 1; fi
  wait_epp_ready
}

patch_enforce() {
  $OC get cm maas-epp-config -n "$NS" -o jsonpath='{.data.epp}' > "$D/epp-src.yaml"
  python3 -I - "$D/epp-src.yaml" "$D/epp-patch.json" "$1" <<'PYEOF'
import sys, re, json
src, dst, val = sys.argv[1:4]
text = open(src).read()
new, n = re.subn(r'(^[ \t]*enforce:[ \t]*)\S.*$', lambda m: m.group(1) + val, text, count=1, flags=re.M)
if n != 1:
    sys.exit("enforce: key not found")
json.dump({"data": {"epp": new}}, open(dst, "w"))
PYEOF
  $OC patch configmap maas-epp-config -n "$NS" --type=merge --patch-file="$D/epp-patch.json" >/dev/null
}

run_row() {
  local id="$1" mode="$2" what="$3" cfg="$4" extra="$5"
  local label="uni310-l$LANE-$TAG-$id"
  log "=== START $id mode=$mode what=$what cfg=$cfg extra=[$extra] label=$label"
  for attempt in 1 2 3; do lane_healthy && break; log "health gate failed (attempt $attempt), waiting 60s"; sleep 60; done
  lane_healthy || { log "SKIP $id: lane unhealthy"; echo "$id SKIPPED-unhealthy" >> "$D/rows-done"; return; }
  apply_config "$cfg" || { log "SKIP $id: config apply failed"; echo "$id SKIPPED-config" >> "$D/rows-done"; return; }
  deploy/poc/21-replica-split.sh snapshot "$D/tmp/rs-before.txt" >>"$LOG" 2>&1
  local status
  case "$mode" in
    bench)
      # shellcheck disable=SC2086
      env $extra ENFORCE_LIVE=true OPENSHIFT_TOKEN="$OPENSHIFT_TOKEN" \
        ./deploy/poc/15-fairness-benchmark.sh "$what" "$label" > "$D/$id.log" 2>&1; status=$? ;;
    control)
      # shellcheck disable=SC2086
      env $extra OPENSHIFT_TOKEN="$OPENSHIFT_TOKEN" \
        ./deploy/poc/15-fairness-benchmark.sh "$what" "$label" > "$D/$id.log" 2>&1; status=$? ;;
    openloop)
      patch_enforce true; wait_enforcing 1 || { log "SKIP $id: enforce never confirmed"; patch_enforce false; wait_enforcing 0; echo "$id SKIPPED-enforce" >> "$D/rows-done"; return; }
      RATE_APP1="$what" RATE_APP2="$what" RATE_END_USERS="$what" DURATION=240 OPENSHIFT_TOKEN="$OPENSHIFT_TOKEN" \
        ./deploy/poc/17-fairness-benchmark-openloop.sh "$label" "$label" > "$D/$id.log" 2>&1; status=$?
      patch_enforce false; wait_enforcing 0 ;;
  esac
  deploy/poc/21-replica-split.sh snapshot "$D/tmp/rs-after.txt" >>"$LOG" 2>&1
  local dir; dir="$(ls -dt results/*-"$label" 2>/dev/null | head -1)"
  if [ -n "$dir" ]; then
    cp "$D/tmp/rs-before.txt" "$dir/replica-counters-before.txt"
    cp "$D/tmp/rs-after.txt" "$dir/replica-counters-after.txt"
    deploy/poc/21-replica-split.sh diff "$D/tmp/rs-before.txt" "$D/tmp/rs-after.txt" > "$dir/replica-split.md" 2>>"$LOG"
    cp "$D/$id.log" "$dir/driver-row.log"
  fi
  local verdict; verdict="$(grep -m1 -oE '^\*\*Verdict: [A-Z-]+\*\*' "$dir/fairness-report.md" 2>/dev/null)"
  log "=== END $id exit=$status dir=${dir:-none} $verdict"
  echo "$id exit=$status ${dir:-none} $verdict" >> "$D/rows-done"
  # Restore and prove it, every row (ENFORCE_LIVE self-reverts enforce; this
  # catches everything else, including a weight table left behind).
  if ! config_matches_default; then
    apply_config default
    if ! config_matches_default; then log "FATAL: lane config does not diff clean against 00-config after restore -- stopping"; exit 3; fi
  fi
  [ "$(read_enforcing)" = "0" ] || { log "WARNING: enforcing!=0 after row; re-checking"; wait_enforcing 0 || { log "FATAL: lane left enforcing"; exit 3; }; }
}

log "driver start: ns=$NS lane=$LANE rows=$ROWS tag=$TAG pid=$$"
config_matches_default && log "pre-flight: config == rendered 00-config" || { log "FATAL: pre-flight config differs from 00-config"; exit 3; }
while IFS='|' read -r -u 9 id mode what cfg extra; do
  id="$(echo "$id" | xargs)"; [ -z "$id" ] && continue; case "$id" in \#*) continue;; esac
  if [ -f "$D/rows-done" ] && grep -q "^$id " "$D/rows-done"; then log "skip $id (already done)"; continue; fi
  run_row "$id" "$(echo "$mode" | xargs)" "$(echo "$what" | xargs)" "$(echo "$cfg" | xargs)" "$(echo "$extra" | xargs)"
done 9< <(grep -v '^[[:space:]]*#' "$ROWS")
log "driver done"
date -u > "$D/DONE"
