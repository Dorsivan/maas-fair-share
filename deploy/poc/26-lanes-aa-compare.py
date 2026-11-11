#!/usr/bin/env python3
"""UNI-231 A/A comparison. Reads results/*-uni231-aa-<phase>-<lane>/fairness-report.json.

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
    m = re.search(r"uni231-aa-(T1|T2|A2|A3)-(lane[23])/", path)
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
for (ph, ln), r in sorted(runs.items(), key=lambda kv: (["T1", "A2", "A3", "T2"].index(kv[0][0]), kv[0][1])):
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

print("\n### Comparisons\n")
print("| comparison | max per-group deviation gap (pts) | e2e p50 ratio range | largest TTFT p50 diff (s) | max-dev diff (pts) |")
print("|---|---|---|---|---|")
for ph in ("T1", "T2"):
    cmp((ph, "lane2"), (ph, "lane3"), f"{ph}: lane2 vs lane3 (together)")
cmp(("A2", "lane2"), ("A3", "lane3"), "solo: lane2 vs lane3")
for ph in ("T1", "T2"):
    cmp((ph, "lane2"), ("A2", "lane2"), f"lane2: {ph} vs alone")
    cmp((ph, "lane3"), ("A3", "lane3"), f"lane3: {ph} vs alone")
cmp(("T1", "lane2"), ("T2", "lane2"), "lane2: T1 vs T2 (repeat)")
cmp(("T1", "lane3"), ("T2", "lane3"), "lane3: T1 vs T2 (repeat)")

print("\n### Together-phase load overlap\n")
ts = lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").timestamp()
for ph in ("T1", "T2"):
    if (ph, "lane2") in runs and (ph, "lane3") in runs:
        a, b = runs[(ph, "lane2")], runs[(ph, "lane3")]
        lo, hi = max(ts(a["start"]), ts(b["start"])), min(ts(a["end"]), ts(b["end"]))
        span = max(ts(a["end"]), ts(b["end"])) - min(ts(a["start"]), ts(b["start"]))
        print(f"- {ph}: overlap {max(0, hi - lo):.0f}s of a {span:.0f}s combined window; start offset {ts(b['start']) - ts(a['start']):+.0f}s (lane3 minus lane2)")
print("\nimages:", sorted({r['image'] for r in runs.values()}))
for k, r in sorted(runs.items()):
    print(k, r["dir"])
