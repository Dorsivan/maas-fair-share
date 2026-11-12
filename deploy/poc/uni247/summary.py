"""UNI-247: one row per repeat from each run's fairness-report.json."""
import glob, json, statistics, sys
rows = {}
for p in sorted(glob.glob("results/*uni-247-*/fairness-report.json")):
    r = json.load(open(p))
    v, s = r["verdict"], r["saturation"]
    lab = r["run"].get("label") or p.split("/")[1]
    pt = next(k for k in ("2x", "3x", "4x") if f"-{k}-" in lab)
    g = {x["group"]: x for x in r["groups"] if x.get("offered")}
    rows.setdefault(pt, []).append(v["max_abs_deviation_points"])
    print(f"{lab:16} {v['result']:5} maxdev={v['max_abs_deviation_points']:5.1f} "
          + " ".join(f"{k}={g[k]['observed_share_pct']:.1f}({g[k]['deviation_pts']:+.1f})" for k in ("app1", "app2", "end-users"))
          + f" limb={s.get('bound_at_peak')} peakQ={s.get('peak_average_queue_size')} peakKV={s.get('peak_average_kv_cache_utilization')}"
          + f" restart={v['epp_restarted_mid_run']} ledger={r['ledger'].get('result', r['ledger'].get('verdict'))}"
          + f" discr={v.get('discriminating')} window={r['run']['run_start']}..{r['run']['run_end']}")
for pt, d in rows.items():
    print(f"{pt}: n={len(d)} devs={[round(x,1) for x in d]} spread={max(d)-min(d):.1f} mean={statistics.mean(d):.1f}"
          + (f" sd={statistics.stdev(d):.1f}" if len(d) > 1 else ""))
