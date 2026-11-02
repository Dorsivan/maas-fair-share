#!/usr/bin/env python3
"""UNI-140 (B6): recompute a soak run's verdict from cluster-side Prometheus
(Thanos, via the UWM querier) instead of the local capture files, for the
case where the local driver (15-fairness-benchmark.sh / 18-soak-monitor.sh)
dies partway through a long run but the Kubernetes Job and the EPP itself
keep going unaffected.

Why this is needed: on the UNI-140 run (2026-11-01T22:42:18Z -
2026-11-02T00:17:38Z, 95 minutes), both local driver processes stopped
writing at ~23:24Z -- 42 minutes in -- while `maas-loadgen`'s Job object
kept running on the cluster for the full configured 5700s and only completed
at 00:17:38Z. The local results (fairness-report.md, memory-timeseries.txt)
therefore only cover the first 42 of 95 minutes; silently treating that as
"the soak" would understate the window by more than half.

The EPP's own counters and the platform's memory/restart series are not
local state -- they live in Prometheus for as long as its retention window
covers, independent of whether the sandbox process that was going to read
them survived. This script re-reads them for an arbitrary past window and
reproduces the same two judgements 15-fairness-report.py and
18-soak-monitor.sh make (windowed share vs threshold; memory flat; restart
count), using the SAME source metrics so the numbers are comparable:
  - `llm_d_epp_maas_fairness_contended_service_tokens_total` for delivered
    share, per fairness_id (matches 15-fairness-report.py's own choice of
    SLI -- see that file's module docstring for why, deliberately not
    redefined here).
  - `container_memory_working_set_bytes` (container=main) and
    `process_resident_memory_bytes`, both already scraped by platform
    monitoring without needing the EPP's custom ServiceMonitor.
  - `kube_pod_container_status_restarts_total`.
  - `llm_d_epp_flow_control_requests_total` by `outcome`, to show whether
    the run measured fairness or shedding (see deploy/epp-config.yaml's
    `flowControl` comment: a non-zero/growing evicted outcome during a run
    means that run measured shedding, not the fairness policy).

Access: the live Grafana (namespace `grafana`) runs with anonymous Viewer
enabled and proxies `POST /api/ds/query` to its one Prometheus datasource
(Thanos Querier, UID PBFA97CFB590B2093) with no credentials -- confirmed
working in UNI-130. This script talks to that endpoint directly rather than
assuming an OPENSHIFT_TOKEN-authenticated route into Thanos exists, since
none of poc-viewer, poc-agent, or the metrics-reader SA used elsewhere in
this repo have read access to the cluster's UWM Thanos route.

Limitation: Thanos retention determines how far back this can reach. This
recovers data from *this* run because it was run within hours of the gap;
it is not a substitute for the local capture succeeding, and cannot recover
anything predating UWM's retention window.

Usage:
  python3 -I deploy/poc/19-soak-prometheus-backfill.py \\
      --start 2026-11-01T22:42:18Z --end 2026-11-02T00:17:38Z \\
      --namespace maas-fairness-poc \\
      --pod maas-vllm-gpu-kserve-router-scheduler-58fd8c459d-bsl76 \\
      --job maas-vllm-gpu-epp-service \\
      --weights app1=20,app2=10,end-users=65 \\
      --threshold-pts 10 --window-seconds 300 \\
      --out-json results/<dir>/full-run-backfill.json \\
      --out-md results/<dir>/full-run-backfill.md
"""
import argparse
import bisect
import json
import subprocess
import sys
from datetime import datetime, timezone

GRAFANA_URL = "https://grafana-grafana.apps.ocp.paladinaura.com/api/ds/query"
PROM_DATASOURCE_UID = "PBFA97CFB590B2093"


def parse_ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def query_range(expr, start_epoch, end_epoch, step_s=30):
    body = {
        "queries": [{
            "refId": "A",
            "datasource": {"uid": PROM_DATASOURCE_UID},
            "expr": expr,
            "interval": f"{step_s}s",
            "intervalMs": step_s * 1000,
        }],
        "from": str(int(start_epoch * 1000)),
        "to": str(int(end_epoch * 1000)),
    }
    proc = subprocess.run(
        ["curl", "-sS", "-m", "60", "-X", "POST", GRAFANA_URL,
         "-H", "Content-Type: application/json", "-d", json.dumps(body)],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(proc.stdout)
    result = data["results"]["A"]
    if result.get("error"):
        raise RuntimeError(f"query failed: {expr!r}: {result['error']}")
    return result.get("frames", [])


def series_by_label(frames, label):
    out = {}
    for f in frames:
        key = f["schema"]["fields"][1]["labels"].get(label)
        values = f["data"]["values"]
        ts = [t / 1000.0 for t in values[0]]
        ys = values[1]
        out[key] = list(zip(ts, ys))
    return out


def value_at_or_before(series, t):
    ts = [p[0] for p in series]
    idx = bisect.bisect_right(ts, t) - 1
    idx = max(0, min(idx, len(series) - 1))
    return series[idx][1]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", required=True, help="run start, UTC, e.g. 2026-11-01T22:42:18Z")
    ap.add_argument("--end", required=True, help="run end, UTC")
    ap.add_argument("--namespace", required=True)
    ap.add_argument("--pod", required=True, help="EPP pod name at run time")
    ap.add_argument("--job", required=True, help="Prometheus job label for the EPP's /metrics scrape")
    ap.add_argument("--weights", required=True, help="comma-separated group=weight for OFFERED groups only, e.g. app1=20,app2=10,end-users=65")
    ap.add_argument("--threshold-pts", type=float, default=10.0)
    ap.add_argument("--window-seconds", type=int, default=300)
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--out-md", required=True)
    args = ap.parse_args()

    start = parse_ts(args.start)
    end = parse_ts(args.end)
    weights = dict(kv.split("=") for kv in args.weights.split(","))
    weights = {k: float(v) for k, v in weights.items()}
    active = list(weights.keys())
    total_weight = sum(weights.values())
    expected_pct = {g: 100.0 * w / total_weight for g, w in weights.items()}

    tokens_frames = query_range(
        f'llm_d_epp_maas_fairness_contended_service_tokens_total{{job="{args.job}"}}', start, end)
    tokens = series_by_label(tokens_frames, "fairness_id")

    mem_ws_frames = query_range(
        f'container_memory_working_set_bytes{{namespace="{args.namespace}",pod="{args.pod}",container="main"}}',
        start, end)
    mem_ws = mem_ws_frames[0]["data"]["values"] if mem_ws_frames else None

    rss_frames = query_range(f'process_resident_memory_bytes{{job="{args.job}"}}', start, end)
    rss = rss_frames[0]["data"]["values"] if rss_frames else None

    restarts_frames = query_range(
        f'kube_pod_container_status_restarts_total{{namespace="{args.namespace}",pod="{args.pod}"}}',
        start, end)
    restarts = restarts_frames[0]["data"]["values"] if restarts_frames else None

    flow_frames = query_range(f'llm_d_epp_flow_control_requests_total{{job="{args.job}"}}', start, end)
    flow_by_outcome = series_by_label(flow_frames, "outcome")

    def delivered(g, t0, t1):
        return value_at_or_before(tokens[g], t1) - value_at_or_before(tokens[g], t0)

    n_windows = int((end - start) // args.window_seconds)
    windows = []
    max_abs_dev = 0.0
    max_abs_dev_window = None
    for i in range(n_windows + 1):
        t0 = start + i * args.window_seconds
        t1 = min(start + (i + 1) * args.window_seconds, end)
        if t1 - t0 < 0.2 * args.window_seconds:
            continue  # negligible tail window
        deltas = {g: delivered(g, t0, t1) for g in active}
        total = sum(deltas.values())
        row = {"window_start_s": t0 - start, "window_end_s": t1 - start, "groups": {}}
        for g in active:
            obs = 100.0 * deltas[g] / total if total > 0 else None
            dev = (obs - expected_pct[g]) if obs is not None else None
            row["groups"][g] = {"delivered_tokens_delta": deltas[g], "observed_pct": obs, "deviation_pts": dev}
            if dev is not None and abs(dev) > max_abs_dev:
                max_abs_dev = abs(dev)
                max_abs_dev_window = (i, t0 - start, t1 - start, g)
        windows.append(row)

    whole_run = {}
    whole_total = sum(delivered(g, start, end) for g in active)
    for g in active:
        d = delivered(g, start, end)
        obs = 100.0 * d / whole_total if whole_total > 0 else None
        whole_run[g] = {
            "delivered_tokens_delta": d,
            "observed_pct": obs,
            "expected_pct": expected_pct[g],
            "deviation_pts": (obs - expected_pct[g]) if obs is not None else None,
        }

    def summarize_series(vv, divisor=1e6):
        if not vv:
            return None
        ts, ys = vv[0], vv[1]
        n = len(ys)
        k = max(1, min(10, n // 4))
        return {
            "n_samples": n,
            "min_mb": min(ys) / divisor,
            "max_mb": max(ys) / divisor,
            "first_k_avg_mb": sum(ys[:k]) / k / divisor,
            "last_k_avg_mb": sum(ys[-k:]) / k / divisor,
        }

    restart_values = restarts[1] if restarts else []
    flow_outcomes = {}
    for outcome, series in flow_by_outcome.items():
        if not series:
            continue
        flow_outcomes[outcome] = {"first": series[0][1], "last": series[-1][1], "delta": series[-1][1] - series[0][1]}

    verdict_windowed_share = "PASS" if max_abs_dev <= args.threshold_pts else "FAIL"

    report = {
        "run_start": args.start,
        "run_end": args.end,
        "duration_seconds": end - start,
        "namespace": args.namespace,
        "pod": args.pod,
        "job_label": args.job,
        "expected_pct": expected_pct,
        "threshold_pts": args.threshold_pts,
        "windows": windows,
        "max_abs_deviation_pts": max_abs_dev,
        "max_abs_deviation_window": max_abs_dev_window,
        "verdict_windowed_share": verdict_windowed_share,
        "whole_run": whole_run,
        "container_working_set_memory": summarize_series(mem_ws),
        "process_resident_memory": summarize_series(rss),
        "restart_count_samples": sorted(set(restart_values)) if restart_values else None,
        "flow_control_outcomes": flow_outcomes,
    }

    with open(args.out_json, "w") as f:
        json.dump(report, f, indent=2)

    lines = []
    lines.append("# Soak run full-window backfill")
    lines.append("")
    lines.append(f"Recomputed from cluster-side Prometheus (Thanos via Grafana anonymous Viewer proxy, "
                 f"UNI-130 mechanism) because the local capture driver stopped before the run finished. "
                 f"Covers the full window: `{args.start}` to `{args.end}` ({end - start:.0f}s).")
    lines.append("")
    lines.append(f"**Windowed-share verdict: {verdict_windowed_share}** "
                 f"(threshold {args.threshold_pts} pts; max |deviation| {max_abs_dev:.2f} pts "
                 f"at window {max_abs_dev_window})")
    lines.append("")
    lines.append(f"| window start (s) | window end (s) | " + " | ".join(f"{g} obs% (dev)" for g in active) + " |")
    lines.append("|---|---|" + "---|" * len(active))
    for row in windows:
        cells = []
        for g in active:
            gg = row["groups"][g]
            if gg["observed_pct"] is None:
                cells.append("n/a")
            else:
                cells.append(f"{gg['observed_pct']:.1f}% ({gg['deviation_pts']:+.1f})")
        lines.append(f"| {row['window_start_s']:.0f} | {row['window_end_s']:.0f} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("## Whole-run totals")
    lines.append("")
    lines.append("| group | delivered tokens (delta) | observed % | expected % | deviation (pts) |")
    lines.append("|---|---|---|---|---|")
    for g in active:
        w = whole_run[g]
        lines.append(f"| {g} | {w['delivered_tokens_delta']:.0f} | {w['observed_pct']:.2f}% | "
                     f"{w['expected_pct']:.2f}% | {w['deviation_pts']:+.2f} |")
    lines.append("")
    lines.append("## Memory")
    lines.append("")
    for label, s in [("container working-set (container=main)", report["container_working_set_memory"]),
                      ("EPP process_resident_memory_bytes", report["process_resident_memory"])]:
        if s is None:
            lines.append(f"- {label}: no data")
            continue
        lines.append(f"- {label}: {s['n_samples']} samples, "
                     f"{s['first_k_avg_mb']:.1f}MB (start) -> {s['last_k_avg_mb']:.1f}MB (end), "
                     f"range [{s['min_mb']:.1f}, {s['max_mb']:.1f}]MB")
    lines.append("")
    lines.append("## Restarts")
    lines.append("")
    lines.append(f"- `kube_pod_container_status_restarts_total` samples across the window: "
                 f"{report['restart_count_samples']}")
    lines.append("")
    lines.append("## Flow-control outcomes (shedding check)")
    lines.append("")
    lines.append("Per `deploy/epp-config.yaml`'s own comment: a non-zero/growing evicted outcome during a "
                 "run means that run measured shedding, not the fairness policy.")
    lines.append("")
    for outcome, vals in flow_outcomes.items():
        lines.append(f"- `{outcome}`: {vals['first']:.0f} -> {vals['last']:.0f} (delta {vals['delta']:.0f})")
    lines.append("")

    with open(args.out_md, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"wrote {args.out_json} and {args.out_md}", file=sys.stderr)
    print(f"verdict_windowed_share={verdict_windowed_share} max_abs_deviation_pts={max_abs_dev:.2f}", file=sys.stderr)


if __name__ == "__main__":
    main()
