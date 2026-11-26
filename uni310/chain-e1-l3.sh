#!/bin/bash
# Run rows-e1.txt on lane 3 once its r2 pass writes DONE.
HERE="$(cd "$(dirname "$0")" && pwd)"
while [ ! -f "$HERE/state/l3-r2/DONE" ]; do [ -d "/proc/$(cat "$HERE/state/l3-r2/pid")" ] || exit 1; sleep 60; done
exec "$HERE/lane-driver.sh" poc-maas-lane3 "$HERE/rows-e1.txt" r3
