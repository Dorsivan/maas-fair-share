#!/bin/bash
# UNI-231 A/A 2-up driver. Phases: T1 (lane2+lane3), A2 (lane2), A3 (lane3), T2 (lane2+lane3).
# No `set -e`: one transient oc failure must not kill the monitor or a phase.
cd /paperclip/instances/default/projects/abb0e14d-6458-4361-ad97-ffd1c150d818/4b213b86-6c56-46d7-aae6-65182ff9685d/_default/uni231-work || exit 1
export PATH=/paperclip/bin:$PATH
D="$1"; mkdir -p "$D"
OC="oc --token=$OPENSHIFT_TOKEN --server=https://api.ocp.paladinaura.com:6443"
SCEN=full-contention-2x-discriminating
PHASE=pre; echo pre > "$D/phase"
log(){ echo "$(date -u +%FT%TZ) $*" | tee -a "$D/driver.log"; }

inst1_busy(){
  # active Job in instance 1, or a harness process on this host not aimed at a lane
  $OC -n maas-fairness-poc get jobs -o jsonpath='{range .items[*]}{.status.active}{"\n"}{end}' 2>/dev/null | grep -q '[1-9]' && { echo job; return 0; }
  for p in /proc/[0-9]*; do
    tr '\0' ' ' < $p/cmdline 2>/dev/null | grep -q '15-fairness-benchmark.sh' || continue
    ns=$(tr '\0' '\n' < $p/environ 2>/dev/null | sed -n 's/^NAMESPACE=//p')
    case "$ns" in poc-maas-lane2|poc-maas-lane3) ;; *) echo "proc$(basename $p):${ns:-unset}"; return 0;; esac
  done; return 1; }

monitor(){ while [ ! -f "$D/DONE" ]; do
  n=$($OC adm top node ocp-worker-2 --no-headers 2>/dev/null | awk '{print $2,$3}')
  k=$($OC adm top pod -n kuadrant-system --no-headers 2>/dev/null | awk '/authorino-[0-9a-f]+-|limitador-limitador/{printf "%s=%s ", substr($1,1,12), $2}')
  b=$(inst1_busy || echo idle)
  echo "$(date -u +%FT%TZ) phase=$(cat $D/phase) worker2=[$n] $k inst1=$b" >> "$D/monitor.log"; sleep 20; done; }

wasm(){ for L in poc-maas-lane2 poc-maas-lane3; do
  $OC -n $L exec deploy/maas-poc-gateway-data-science-gateway-class -c istio-proxy -- pilot-agent request GET stats 2>/dev/null | grep -E 'wasmcustom' > "$D/wasm-$1-$L.txt"; done; }

run_phase(){ name=$1; shift
  w=0; while r=$(inst1_busy); do log "$name: instance 1 busy ($r), waiting"; sleep 30; w=$((w+30)); [ $w -ge 3600 ] && { log "$name: gave up after 60 min"; touch "$D/ABORTED"; return 1; }; done
  echo "$name" > "$D/phase"; wasm "pre-$name"; log "$name: start lanes=$*"
  pids=""
  for L in "$@"; do ( NAMESPACE=$L ENFORCE_LIVE=true ./deploy/poc/15-fairness-benchmark.sh $SCEN "uni231-aa-$name-${L#poc-maas-}" > "$D/$name-$L.log" 2>&1; echo "EXIT $?" >> "$D/$name-$L.log" ) & pids="$pids $!"; done
  # wait on this phase's runs only; a bare `wait` also waits on the monitor loop and never returns
  wait $pids; wasm "post-$name"; log "$name: done $(grep -h '^EXIT' $D/$name-*.log | tr '\n' ' ')"; echo gap > "$D/phase"; }

monitor & MON=$!
# phases to run: args 2..n (default all), so a restart can resume mid-sequence
shift; PH="${*:-T1 A2 A3 T2}"
for ph in $PH; do
  case $ph in T1|T2) run_phase $ph poc-maas-lane2 poc-maas-lane3 ;; A2) run_phase A2 poc-maas-lane2 ;; A3) run_phase A3 poc-maas-lane3 ;; esac || break
done
touch "$D/DONE"; wait $MON 2>/dev/null; log "driver finished"
