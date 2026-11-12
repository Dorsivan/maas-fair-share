#!/bin/bash
# UNI-231 A/A driver. Phase name selects lanes: T3* = instance 1 + lanes 2,3; I1* = instance 1 alone;
# T* = lanes 2+3; A2* = lane 2 alone; A3* = lane 3 alone.
# No `set -e`: one transient oc failure must not kill the monitor or a phase.
# usage: deploy/poc/27-lanes-aa-driver.sh RESULTS_DIR [PHASE...]   e.g. .lane-provision/aa-3up T3a I1 T3b
# Runs full-contention-2x-discriminating (enforce on) per phase, waits for instance 1 to be idle before
# each phase, and samples shared-node CPU and lane gateway wasm counters. Results go to results/.
D_ARG="$(realpath -m "${1:?usage: $0 RESULTS_DIR [PHASE...]}")"
cd "$(git -C "$(dirname "$(realpath "$0")")" rev-parse --show-toplevel)" || exit 1
export PATH=/paperclip/bin:$PATH
D="$D_ARG"; mkdir -p "$D"
OC="oc --token=$OPENSHIFT_TOKEN --server=https://api.ocp.paladinaura.com:6443"
SCEN=full-contention-2x-discriminating
PHASE=pre; echo pre > "$D/phase"
log(){ echo "$(date -u +%FT%TZ) $*" | tee -a "$D/driver.log"; }

inst1_busy(){
  # active Job in instance 1, or a harness process on this host not aimed at a lane
  case "$(cat $D/phase 2>/dev/null)" in T3*|I1*) ;; *)
    $OC -n maas-fairness-poc get jobs -o jsonpath='{range .items[*]}{.status.active}{"\n"}{end}' 2>/dev/null | grep -q '[1-9]' && { echo job; return 0; } ;; esac
  for p in /proc/[0-9]*; do
    # another agent's run driver counts as busy even between its back-to-back runs
    c=$(tr '\0' ' ' < $p/cmdline 2>/dev/null)
    case "$c" in *-driver.sh*) case "$(readlink $p/cwd)" in "$PWD") ;; *) echo "driver$(basename $p)"; return 0;; esac;; esac
    case "$c" in *15-fairness-benchmark.sh*) ;; *) continue;; esac
    # my own tool shells run from this worktree and carry the filename in their text
    [ "$(readlink $p/cwd)" = "$PWD" ] && ! tr '\0' '\n' < $p/environ 2>/dev/null | grep -qx 'AA_DRIVER=1' && continue
    tr '\0' '\n' < $p/environ 2>/dev/null | grep -qx 'AA_DRIVER=1' && continue
    ns=$(tr '\0' '\n' < $p/environ 2>/dev/null | sed -n 's/^NAMESPACE=//p')
    case "$ns" in poc-maas-lane2|poc-maas-lane3) ;; *) echo "proc$(basename $p):${ns:-unset}"; return 0;; esac
  done; return 1; }

monitor(){ while [ ! -f "$D/DONE" ]; do
  # UNI-249: loadgens now sit on ocp-worker-3/0/1 (lanes.py), so sample every CPU worker
  n=$($OC adm top node ocp-worker-2 --no-headers 2>/dev/null | awk '{print $2,$3}'); n3=$($OC adm top node ocp-worker-3 --no-headers 2>/dev/null | awk '{print $2,$3}')
  n0=$($OC adm top node ocp-worker-0 --no-headers 2>/dev/null | awk '{print $2,$3}'); n1=$($OC adm top node ocp-worker-1 --no-headers 2>/dev/null | awk '{print $2,$3}')
  k=$($OC adm top pod -n kuadrant-system --no-headers 2>/dev/null | awk '/authorino-[0-9a-f]+-|limitador-limitador/{printf "%s=%s ", substr($1,1,12), $2}')
  b=$(inst1_busy || echo idle)
  echo "$(date -u +%FT%TZ) phase=$(cat $D/phase) worker2=[$n] worker3=[$n3] worker0=[$n0] worker1=[$n1] $k other-inst1-run=$b" >> "$D/monitor.log"; sleep 20; done; }

wasm(){ for L in maas-fairness-poc poc-maas-lane2 poc-maas-lane3; do
  $OC -n $L exec deploy/maas-poc-gateway-data-science-gateway-class -c istio-proxy -- pilot-agent request GET stats 2>/dev/null | grep -E 'wasmcustom' > "$D/wasm-$1-$L.txt"; done; }

run_phase(){ name=$1; shift
  w=0; while r=$(inst1_busy); do log "$name: instance 1 busy ($r), waiting"; sleep 30; w=$((w+30)); [ $w -ge 3600 ] && { log "$name: gave up after 60 min"; touch "$D/ABORTED"; return 1; }; done
  echo "$name" > "$D/phase"; wasm "pre-$name"; log "$name: start lanes=$*"
  pids=""
  for L in "$@"; do tag=${L#poc-maas-}; [ "$L" = maas-fairness-poc ] && tag=inst1
    ( AA_DRIVER=1 NAMESPACE=$L ENFORCE_LIVE=true ./deploy/poc/15-fairness-benchmark.sh $SCEN "uni231-aa-$name-$tag" > "$D/$name-$L.log" 2>&1; echo "EXIT $?" >> "$D/$name-$L.log" ) & pids="$pids $!"; done
  # wait on this phase's runs only; a bare `wait` also waits on the monitor loop and never returns
  wait $pids; wasm "post-$name"; log "$name: done $(grep -h '^EXIT' $D/$name-*.log | tr '\n' ' ')"; echo gap > "$D/phase"; }

monitor & MON=$!
# phases to run: args 2..n (default all), so a restart can resume mid-sequence
shift; PH="${*:-T1 A2 A3 T2}"
for ph in $PH; do
  case $ph in T3*) run_phase $ph maas-fairness-poc poc-maas-lane2 poc-maas-lane3 ;; I1*) run_phase $ph maas-fairness-poc ;; T*) run_phase $ph poc-maas-lane2 poc-maas-lane3 ;; A2*) run_phase $ph poc-maas-lane2 ;; A3*) run_phase $ph poc-maas-lane3 ;; esac || break
done
touch "$D/DONE"; wait $MON 2>/dev/null; log "driver finished"
