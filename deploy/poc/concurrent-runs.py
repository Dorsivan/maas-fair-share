#!/usr/bin/env python3
"""UNI-231: which other POC instances had a loadgen Job during this run.

usage: concurrent-runs.py ARTIFACT_DIR "OWN_JOB_START OWN_JOB_COMPLETION" RUN_END

Reads other-instance-jobs-{start,end}.txt (lines: namespace job startTime
[completionTime]) written by 15-fairness-benchmark.sh and writes
concurrent-runs.txt. Prints a WARNING line when any window overlaps.
"""
import sys
from datetime import datetime


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").timestamp()


def main(d, own_window, run_end):
    own = own_window.split()
    lines = []
    if not own:
        lines.append("unknown: own loadgen Job window not readable")
    else:
        start, end = ts(own[0]), ts(own[1] if len(own) > 1 else run_end)
        seen, hits, unverified = set(), [], []
        for phase in ("start", "end"):
            try:
                rows = open(f"{d}/other-instance-jobs-{phase}.txt").read().splitlines()
            except OSError:
                unverified.append(f"other-instance-jobs-{phase}.txt missing")
                continue
            for row in rows:
                if row.startswith("#"):
                    unverified.append(row.lstrip("# "))
                    continue
                p = row.split()
                if len(p) < 3 or tuple(p[:3]) in seen:
                    continue
                seen.add(tuple(p[:3]))
                done = p[3] if len(p) > 3 else None
                overlap = min(end, ts(done or run_end)) - max(start, ts(p[2]))
                if overlap > 0:
                    hits.append(f"{p[0]}/{p[1]} {p[2]}..{done or 'running'} overlap {overlap:.0f}s")
        lines.append(f"own loadgen Job {own[0]}..{own[1] if len(own) > 1 else run_end}")
        lines += hits or ["no other instance had a loadgen Job during this run"]
        lines += [f"unverified: {u}" for u in sorted(set(unverified))]
        if hits:
            print("[benchmark] WARNING: other instances had load during this run "
                  "(see concurrent-runs.txt): " + "; ".join(hits))
    with open(f"{d}/concurrent-runs.txt", "w") as out:
        out.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main(*sys.argv[1:4])
