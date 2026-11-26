#!/usr/bin/env python3
"""UNI-310 before/after table: UNI-218 thr32 baseline vs live runs under the stamp.

    python3 -I uni310/score.py [--md OUT]

Reads only fairness-report.json / enforce-events.log / metrics files the
harness wrote; computes nothing about the policy beyond what the report
already scored, except the open-loop water-filled target (classification.md).
"""
import glob
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BASE = os.path.dirname(REPO)
U218 = os.path.join(BASE, "repo-uni218", "results")
U215 = os.path.join(BASE, "repo-uni211", "results")

# row id -> (baseline glob, group). Groups fixed in classification.md before results.
ROWS = [
    ("f3-33-33-33", U215 + "/*-uni-215-confirm-f3-33-33-33", "disc"),
    ("f3-40-20-40", U215 + "/*-uni-215-confirm-f3-40-20-40", "disc"),
    ("f3-98-1-1", U215 + "/*-uni-215-confirm-f3-98-1-1", "disc"),
    ("uni161-app1-flood-256", U215 + "/*-uni-215-thr32-app1-flood", "disc"),
    ("uni161-app1-flood-128", U218 + "/*-uni-218-uni161-app1-flood-128", "disc"),
    ("uni165-dominant", U218 + "/*-uni-218-uni165-dominant", "disc"),
    ("uni165-pow2", U218 + "/*-uni-218-uni165-pow2", "disc"),
    ("b5-openloop-120pct", U218 + "/*-uni-218-b5-openloop-120pct", "disc-wf"),
    ("uni164-app3-joins", U218 + "/*-uni-218-uni164-app3-joins", "weak"),
    ("uni165-graded", U218 + "/*-uni-218-uni165-graded", "non"),
    ("full-contention", U215 + "/*-uni-215-confirm-h2-thr32", "non"),
    ("full-contention-2x", U218 + "/*-uni-218-full-contention-2x", "non"),
    ("a3-app2-idle", U218 + "/*-uni-218-a3-app2-idle", "non"),
    ("a4-app1-idle", U218 + "/*-uni-218-a4-app1-idle", "non"),
    ("a5-app2-trickle", U218 + "/*-uni-218-a5-app2-trickle", "non"),
    ("a6-below-capacity", U218 + "/*-uni-218-a6-below-capacity", "non"),
    ("end-users-idle", U218 + "/*-uni-218-end-users-idle", "non"),
    ("end-users-idle-2x", U218 + "/*-uni-218-end-users-idle-2x", "non"),
    ("b5-openloop-70pct", U218 + "/*-uni-218-b5-openloop-70pct", "non"),
    ("b5-openloop-100pct", U218 + "/*-uni-218-b5-openloop-100pct", "non"),
    ("uni165-equal", U218 + "/*-uni-218-uni165-equal", "floor"),
    ("uni165-subset-3-idle", U218 + "/*-uni-218-uni165-subset-3-idle", "floor"),
    ("uni165-equal-2x", U218 + "/*-uni-218-uni165-equal-2x", "floor"),
    ("b1-cold-join", U218 + "/*-uni-218-b1-cold-join", "dyn"),
    ("b2-tenant-leaves", U218 + "/*-uni-218-b2-tenant-leaves", "dyn"),
    ("b4-short-idle", U218 + "/*-uni-218-b4-short-idle", "dyn"),
    ("b4-long-idle", U218 + "/*-uni-218-b4-long-idle", "dyn"),
    ("e1-epp-restart", U218 + "/*-uni-218-e1-epp-restart", "dyn"),
    ("e2-lose-replica", U218 + "/*-uni-218-e2-lose-replica", "dyn"),
    ("a1-app2-alone", U218 + "/*-uni-218-a1-app2-alone", "solo"),
    ("f1-shadow-mode-control", U218 + "/*-uni-218-f1-shadow-mode-control", "ctl"),
]


def load(d):
    try:
        return json.load(open(os.path.join(d, "fairness-report.json")))
    except Exception:
        return None


def metric_sum(path, name):
    tot, seen = 0.0, False
    try:
        for line in open(path):
            if line.startswith(name) and (line[len(name)] in " {"):
                tot += float(line.rsplit(None, 1)[1]); seen = True
    except (OSError, IndexError, ValueError):
        pass
    return tot if seen else 0.0  # absent counter == never incremented


def water_fill(weights, demand):
    """Share each group gets when demand-capped groups give surplus back by weight."""
    share = {g: 0.0 for g in weights}
    active = set(weights)
    left = 1.0
    while active and left > 1e-12:
        wsum = sum(weights[g] for g in active)
        alloc = {g: left * weights[g] / wsum for g in active}
        capped = {g for g in active if share[g] + alloc[g] >= demand[g]}
        if not capped:
            for g in active:
                share[g] += alloc[g]
            break
        for g in capped:
            left -= demand[g] - share[g]
            share[g] = demand[g]
        active -= capped
    return share


def busy_seconds(d, groups):
    """First arrival to last completion, from the open-loop generator's own
    per-request logs (<group>.log: arrival, send, latency, code, tokens). The
    pool is saturated across that span in an overloaded run, so served cost /
    busy span is the measured capacity."""
    t0, t1 = None, None
    for g in groups:
        try:
            for line in open(os.path.join(d, g + ".log")):
                f = line.split()
                if len(f) < 3:
                    continue
                a, lat = float(f[0]), float(f[2])
                t0 = a if t0 is None else min(t0, a)
                t1 = a + lat if t1 is None else max(t1, a + lat)
        except (OSError, ValueError):
            return None
    return (t1 - t0) if t0 is not None else None


def wf_maxdev(rep, d):
    """Open-loop: score observed share against the demand-capped (water-filled) target."""
    gs = [g for g in rep["groups"] if g.get("offered")]
    dur = rep["run"]["duration_seconds"]
    busy = busy_seconds(d, [g["group"] for g in gs])
    if not busy:
        return None, None
    cap = sum(g["delivered_tokens"] or 0 for g in gs) / busy
    if cap <= 0:
        return None, None
    demand = {}
    for g in gs:
        n = g["requests_total"] or 0          # every arrival, served or not
        ok = (g.get("status_tally") or {}).get("200", 0)
        mean = (g["delivered_tokens"] or 0) / ok if ok else 0
        demand[g["group"]] = n * mean / dur / cap
    weights = {g["group"]: g["configured_weight"] for g in gs}
    tgt = water_fill(weights, demand)
    devs = {g["group"]: (g["observed_share_pct"] or 0) - 100 * tgt[g["group"]] for g in gs}
    return max(abs(v) for v in devs.values()), {k: round(100 * v, 1) for k, v in tgt.items()}


def summarize(d):
    rep = load(d)
    if not rep:
        return None
    v = rep["verdict"]
    groups = [g for g in rep["groups"] if g.get("offered")]
    ma = os.path.join(d, "metrics-after.txt")
    mb = os.path.join(d, "metrics-before.txt")
    late = metric_sum(ma, "llm_d_epp_maas_fairness_sfq_late_completions_total") - metric_sum(mb, "llm_d_epp_maas_fairness_sfq_late_completions_total")
    unset = metric_sum(ma, "llm_d_epp_maas_fairness_sfq_unsettled_total") - metric_sum(mb, "llm_d_epp_maas_fairness_sfq_unsettled_total")
    enf = ""
    try:
        enf = "Y" if re.search(r"confirmed: llm_d_epp_maas_fairness_enforcing=1", open(os.path.join(d, "enforce-events.log")).read()) else "?"
    except OSError:
        enf = "Y" if metric_sum(mb, "llm_d_epp_maas_fairness_enforcing") == 1 else "n"
    out = {
        "dir": os.path.basename(d),
        "verdict": v.get("result"),
        "maxdev": v.get("max_abs_deviation_points"),
        "disc": v.get("discriminating"),
        "contended_s": min((g.get("contended_seconds") or 0) for g in groups) if groups else 0,
        "requests": sum(g.get("requests_total") or 0 for g in groups),
        "tokens": sum(g.get("delivered_tokens") or 0 for g in groups),
        "late": late, "unsettled": unset, "enforce": enf,
        "obs": {g["group"]: round(g["observed_share_pct"], 1) if g.get("observed_share_pct") is not None else None for g in groups},
        "exp": {g["group"]: round(g["expected_share_pct"], 1) if g.get("expected_share_pct") is not None else None for g in groups},
        "stamp": metric_sum(mb, "llm_d_epp_maas_fairness_sfq_enabled"),
    }
    if rep["run"].get("generator") == "open-loop":
        out["wf_maxdev"], out["wf_target"] = wf_maxdev(rep, d)
    return out


def fmt(x, nd=1):
    return "—" if x is None else f"{x:.{nd}f}"


def main():
    lines = ["| row | group | before (UNI-218/215) | lane 2 | lane 3 | extra runs | after verdict | Δ max dev | notes |",
             "|---|---|---|---|---|---|---|---|---|"]
    detail = {}
    for rid, bglob, grp in ROWS:
        bd = sorted(glob.glob(bglob))
        b = summarize(bd[-1]) if bd else None
        runs = {}
        for d in sorted(glob.glob(os.path.join(REPO, "results", f"*-uni310-l[23]-*-{rid}"))):
            m = re.search(r"uni310-(l[23])-([a-z0-9]+)-" + re.escape(rid) + "$", d)
            if m:
                s = summarize(d)
                if s:
                    runs.setdefault(m.group(2), {})[m.group(1)] = s
        detail[rid] = {"before": b, "runs": runs}
        r1 = runs.get("r1", {})
        extra = [s for tag, ls in runs.items() if tag != "r1" and not tag.startswith("off") for s in ls.values()]
        allr = list(r1.values()) + extra
        key = "wf_maxdev" if grp == "disc-wf" else "maxdev"
        devs = [s[key] for s in allr if s.get(key) is not None]
        mean = statistics.mean(devs) if devs else None
        bdev = b.get(key) if b else None
        if grp == "disc-wf" and b:
            bdev = b.get("wf_maxdev")
        def cell(s):
            if not s:
                return "—"
            k = s.get(key)
            return f"{s['verdict']} {fmt(k)}" + (f" (static {fmt(s['maxdev'])})" if grp == "disc-wf" else "")
        after = None
        if devs:
            after = "PASS" if all(x < 10 for x in devs) else ("FAIL" if all(x >= 10 for x in devs) else "SPLIT")
            vs = {s["verdict"] for s in allr}
            if vs & {"UNCONTENDED"}:
                after = "/".join(sorted(vs))
        notes = []
        for s in allr:
            if s["late"] or s["unsettled"]:
                notes.append(f"late={s['late']:.0f} unsettled={s['unsettled']:.0f}")
            if s["enforce"] != "Y" and grp not in ("ctl",):
                notes.append(f"enforce?={s['enforce']}")
        lines.append(
            f"| {rid} | {grp} | {cell(b)} | {cell(r1.get('l2'))} | {cell(r1.get('l3'))} | "
            f"{', '.join(fmt(s.get(key)) for s in extra) or '—'} | {after or '—'} | "
            f"{fmt(mean - bdev) if (mean is not None and bdev is not None) else '—'} | {'; '.join(sorted(set(notes)))} |")
    md = "\n".join(lines)
    print(md)
    if "--json" in sys.argv:
        json.dump(detail, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
