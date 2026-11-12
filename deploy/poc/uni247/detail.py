"""UNI-247: error regime, throughput, latency spread and contended time per repeat."""
import glob, json
for p in sorted(glob.glob("results/*uni-24[57]-*flood*/fairness-report.json") + glob.glob("results/*uni-247-*/fairness-report.json")):
    r = json.load(open(p))
    g = {x["group"]: x for x in r["groups"] if x.get("offered")}
    lab = p.split("/")[1]
    bad = {k: {s: n for s, n in g[k]["status_tally"].items() if s != "200"} for k in g}
    tok = sum(x["delivered_tokens"] for x in g.values())
    ratio = g["app1"]["p50_sec"] / g["end-users"]["p50_sec"]
    cs = "/".join(f"{g[k]['contended_seconds']:.1f}" for k in ("app1", "app2", "end-users"))
    print(f"{lab:42} tok={tok/1e6:.2f}M p50 app1/eu={g['app1']['p50_sec']:.2f}/{g['end-users']['p50_sec']:.2f}={ratio:.2f} contended={cs} non200={bad}")
