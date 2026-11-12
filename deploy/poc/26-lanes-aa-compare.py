#!/usr/bin/env python3
"""UNI-231 A/A comparison. Reads results/*-uni231-aa-<phase>-<lane>/fairness-report.json.

Phase names: T* = run together with other lanes, anything else (A2, A3b, I1 ...) = alone.
Lanes: lane2, lane3, inst1. Runs are only compared with runs on the same EPP image.

Prints, as markdown:
  1. one row per run: verdict, max |dev|, per-group deviation, e2e p50, TTFT p50, errors
  2. lane vs lane within each phase (the A/A question)
  3. together vs alone per lane (does running two at once slow a lane down)
  4. T1 vs T2 per lane (run-to-run noise on the same lane)
  5. load-window overlap of the two lanes in each together phase
"""
import glob, json, os, re, sys
from datetime import datetime

ROOT = sys.argv[1] if len(sys.argv) > 1 else "results"
GROUPS = ["app1", "app2", "end-users"]
runs = {}
for path in sorted(glob.glob(f"{ROOT}/*-uni231-aa-*/fairness-report.json")):
    m = re.search(r"uni231-aa-([A-Za-z0-9]+)-(lane[23]|inst1)/", path)
    if not m:
        continue
    rep = json.load(open(path))
    g = {x["group"]: x for x in rep["groups"]}
    tt = (rep.get("ttft_itl") or {}).get("groups") or {}
    errs = sum(v for x in rep["groups"] for k, v in (x.get("status_tally") or {}).items() if str(k) != "200")
    reqs = sum(x.get("requests_total") or 0 for x in rep["groups"])
    runs[(m.group(1), m.group(2))] = {
        "dir": os.path.dirname(path),
        "verdict": rep["verdict"]["result"],
        "maxdev": rep["verdict"]["max_abs_deviation_points"],
        "dev": {k: g[k]["deviation_pts"] for k in GROUPS if k in g},
        "p50": {k: g[k]["p50_sec"] for k in GROUPS if k in g},
        "p95": {k: g[k]["p95_sec"] for k in GROUPS if k in g},
        "contended": {k: g[k].get("contended_seconds") for k in GROUPS if k in g},
        "ttft50": {k: ((tt.get(k) or {}).get("ttft") or {}).get("p50_seconds") for k in GROUPS},
        "ttft95": {k: ((tt.get(k) or {}).get("ttft") or {}).get("p95_seconds") for k in GROUPS},
        "prio": ((rep.get("ttft_itl") or {}).get("priority_verdict") or {}).get("result"),
        "errs": errs, "reqs": reqs,
        "start": rep["run"]["run_start"], "end": rep["run"]["run_end"],
        "image": rep["run"]["epp_image_digest"][-12:],
    }

def f(v, nd=1):
    return "n/a" if v is None else f"{v:.{nd}f}"

print("### Runs\n")
print("| phase | lane | verdict | max dev | dev app1 / app2 / eu | e2e p50 s | TTFT p50 s | TTFT p95 s | prio | non-200 / req | window |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for (ph, ln), r in sorted(runs.items(), key=lambda kv: (kv[1]["start"], kv[0][1])):
    print(f"| {ph} | {ln} | {r['verdict']} | {f(r['maxdev'])} | "
          + " / ".join(f"{r['dev'].get(k, 0):+.1f}" for k in GROUPS) + " | "
          + " / ".join(f(r['p50'].get(k)) for k in GROUPS) + " | "
          + " / ".join(f(r['ttft50'].get(k), 2) for k in GROUPS) + " | "
          + " / ".join(f(r['ttft95'].get(k), 2) for k in GROUPS) + " | "
          + f"{r['prio']} | {r['errs']} / {r['reqs']} | {r['start'][11:19]}-{r['end'][11:19]} |")

def cmp(a, b, label):
    if a not in runs or b not in runs:
        print(f"| {label} | missing run |"); return
    x, y = runs[a], runs[b]
    ddev = max(abs(x["dev"][k] - y["dev"][k]) for k in GROUPS)
    p50r = max(x["p50"][k] / y["p50"][k] for k in GROUPS if y["p50"].get(k))
    p50r_min = min(x["p50"][k] / y["p50"][k] for k in GROUPS if y["p50"].get(k))
    tt = [x["ttft50"][k] - y["ttft50"][k] for k in GROUPS if x["ttft50"].get(k) is not None and y["ttft50"].get(k) is not None]
    ttd = max(tt, key=abs) if tt else None
    print(f"| {label} | {ddev:.1f} | {p50r_min:.2f}–{p50r:.2f} | {f(ttd, 2)} | {x['maxdev'] - y['maxdev']:+.1f} |")

print("\n### Comparisons (same EPP image only)\n")
print("| comparison | max per-group deviation gap (pts) | e2e p50 ratio range | largest TTFT p50 diff (s) | max-dev diff (pts) |")
print("|---|---|---|---|---|")
together = lambda k: k[0].startswith("T")
for img in sorted({r["image"] for r in runs.values()}):
    keys = sorted((k for k, r in runs.items() if r["image"] == img), key=lambda k: runs[k]["start"])
    print(f"| **image …{img}** | | | | |")
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if a[0] == b[0] and together(a):
                cmp(a, b, f"{a[0]}: {a[1]} vs {b[1]} (together)")
            elif not together(a) and not together(b) and a[1] != b[1]:
                cmp(a, b, f"alone: {a[1]} ({a[0]}) vs {b[1]} ({b[0]})")
            elif a[1] == b[1] and together(a) != together(b):
                t, al = (a, b) if together(a) else (b, a)
                cmp(t, al, f"{t[1]}: {t[0]} vs alone ({al[0]})")
            elif a[1] == b[1]:
                cmp(a, b, f"{a[1]}: {a[0]} vs {b[0]} (repeat)")

print("\n### Together-phase load overlap\n")
ts = lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").timestamp()
for ph in sorted({k[0] for k in runs if together(k)}):
    lanes = [k for k in runs if k[0] == ph]
    for i, ka in enumerate(lanes):
      for kb in lanes[i + 1:]:
        a, b = runs[ka], runs[kb]
        lo, hi = max(ts(a["start"]), ts(b["start"])), min(ts(a["end"]), ts(b["end"]))
        span = max(ts(a["end"]), ts(b["end"])) - min(ts(a["start"]), ts(b["start"]))
        print(f"- {ph} {ka[1]}+{kb[1]}: overlap {max(0, hi - lo):.0f}s of a {span:.0f}s combined window; start offset {ts(b['start']) - ts(a['start']):+.0f}s")
print("\nimages:", sorted({r['image'] for r in runs.values()}))
for k, r in sorted(runs.items()):
    print(k, r["dir"])
