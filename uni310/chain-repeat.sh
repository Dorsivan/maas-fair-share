#!/bin/bash
# Wait for a lane's r1 pass to finish, then run rows-repeat.txt there as r2.
# Gives up (does nothing) if the r1 driver died without writing DONE.
NS="$1"; L="$2"; HERE="$(cd "$(dirname "$0")" && pwd)"
R1="$HERE/state/l$L-r1"
while [ ! -f "$R1/DONE" ]; do
  [ -d "/proc/$(cat "$R1/pid")" ] || { echo "$(date -u) r1 driver gone without DONE; not chaining" >> "$HERE/state/chain-l$L.log"; exit 1; }
  sleep 60
done
echo "$(date -u) r1 DONE; starting r2" >> "$HERE/state/chain-l$L.log"
exec "$HERE/lane-driver.sh" "$NS" "$HERE/rows-repeat.txt" r2
