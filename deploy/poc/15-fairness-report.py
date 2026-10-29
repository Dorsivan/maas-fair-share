#!/usr/bin/env python3
"""Turn a benchmark run's raw evidence into the per-run fairness result
(UNI-54): one row per group, an explicit PASS/FAIL verdict, and run metadata
that makes the numbers attributable. Pure function of its inputs -- no
cluster access here, so it is testable against synthetic data (see
15-fairness-report-test.py) without a GPU session.

Inputs, each already collected by 15-fairness-benchmark.sh:
  --metrics-before / --metrics-after   Prometheus text-format scrapes of the
      EPP's own /metrics, taken immediately before the Job is created and
      immediately after it completes (same mechanism as
      13-loadgen-poisson.sh). This is the EPP's own accounting -- the
      generator cannot see token usage and must not be allowed to guess it.
  --loadgen-log                        The loadgen pod's stdout: the
      "load: tenants=... workers ..." line and the final
      TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES table from 04-loadgen.yaml's
      run.sh. This is the generator's own view -- offered concurrency,
      delivered requests, status tally, latency -- and is kept separate from
      the EPP's token accounting rather than conflated with it.

"Delivered tokens" and "observed share" both come from
llm_d_epp_maas_fairness_contended_service_tokens_total, the same SLI
deploy/grafana-dashboard.yaml's headline panel uses (UNI-50) -- deliberately
reused rather than redefined. A group's delta is its delivered tokens; a
group's delta divided by the sum of every OFFERED group's delta (as a
percentage) is its observed share.

"Expected share" is each offered group's configured weight divided by the
sum of every OFFERED group's configured weight -- not by the sum of every
CONFIGURED group's weight. The difference matters for the work-conservation
scenarios this benchmark names (end-users-idle, app1-alone): when a group
sends no load, a healthy policy gives its weight to whoever is still asking,
rather than holding it in reserve. Dividing by the full configured total
would score that correct, intended behaviour as a deviation. The
unclassified catch-all (weight 5, never offered by this harness) is excluded
from both sums for the same reason. See docs/poc-results.md for why this
differs by a few points from the "20/10/65" shorthand used loosely elsewhere
in this repo's prose -- those numbers are the raw ConfigMap weights, not
divided by anything.

A SOLO offered group (the app1-alone scenario) is a special case, not an
instance of the above: contended_service_tokens_total only accrues while a
group is backlogged alongside another group in the same band (metrics.go),
so a single offered group scrapes at a flat zero delta even when the policy
is working perfectly -- there is no one to share against. Share/deviation is
therefore not computed for a solo group, and the verdict for that case falls
back to a request-success-rate bar instead (see SOLO_SUCCESS_THRESHOLD
below): "receives ~100% of the pool" is judged by HTTP status, not by a
token-share metric that cannot move in a single-tenant run.
"""
import argparse
import json
import re
import sys

METRIC_LINE = re.compile(r'^([^{\s]+)(?:\{(.*)\})?\s+([^\s]+)$')
LABEL = re.compile(r'(\w+)="((?:[^"\\]|\\.)*)"')
TENANTS_LINE = re.compile(
    r'load: tenants=\[(?P<tenants>.*?)\] '
    r'workers app1=(?P<app1>\d+) app2=(?P<app2>\d+) end-users=(?P<end_users>\d+) '
    r'duration=(?P<duration>\d+)s'
)
TABLE_ROW = re.compile(r'^(\S+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(.+)$')
STATUS_PAIR = re.compile(r'(\d+)=(\d+)')

GROUPS = ("app1", "app2", "end-users")


def parse_metrics(path):
    """{metric_name: {fairness_id_or_None: value}} from a Prometheus text
    scrape (comment lines are harmless here; they never match METRIC_LINE)."""
    series = {}
    with open(path) as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            m = METRIC_LINE.match(line)
            if not m:
                continue
            name, labelstr, val = m.group(1), m.group(2) or '', m.group(3)
            try:
                value = float(val)
            except ValueError:
                continue
            labels = dict(LABEL.findall(labelstr))
            series.setdefault(name, {})[labels.get('fairness_id')] = value
    return series


def parse_loadgen_log(path):
    """Returns (offered_workers: {group: int}, rows: {group: {total, p50_sec,
    p95_sec, statuses}}, duration_seconds_from_log_or_None)."""
    text = open(path).read()
    m = TENANTS_LINE.search(text)
    offered_workers = {g: 0 for g in GROUPS}
    duration = None
    if m:
        tenants = set(m.group('tenants').split())
        by_name = {"app1": m.group('app1'), "app2": m.group('app2'), "end-users": m.group('end_users')}
        for g in GROUPS:
            if g in tenants:
                offered_workers[g] = int(by_name[g])
        duration = int(m.group('duration'))

    rows = {}
    for line in text.splitlines():
        row = TABLE_ROW.match(line.strip())
        if not row or row.group(1) == "TENANT":
            continue
        group, total, p50, p95, statuses_raw = row.groups()
        if group not in GROUPS:
            continue
        rows[group] = {
            "total": int(total),
            "p50_sec": float(p50),
            "p95_sec": float(p95),
            "statuses": {code: int(count) for code, count in STATUS_PAIR.findall(statuses_raw)},
        }
    return offered_workers, rows, duration


def build_report(*, scenario, enforce, duration_seconds, backend, epp_image_digest,
                  namespace, epp_pod, run_start, run_end, threshold_points,
                  metrics_before_path, metrics_after_path, loadgen_log_path,
                  label=None, control=False):
    before = parse_metrics(metrics_before_path)
    after = parse_metrics(metrics_after_path)
    offered_workers, loadgen_rows, logged_duration = parse_loadgen_log(loadgen_log_path)

    weight_before = before.get("llm_d_epp_maas_fairness_configured_weight", {})
    weight_after = after.get("llm_d_epp_maas_fairness_configured_weight", {})
    tokens_before = before.get("llm_d_epp_maas_fairness_contended_service_tokens_total", {})
    tokens_after = after.get("llm_d_epp_maas_fairness_contended_service_tokens_total", {})

    all_group_ids = sorted(
        g for g in set(weight_before) | set(weight_after) | set(GROUPS)
        if g is not None
    )

    epp_restarted = False
    deltas = {}
    for gid in all_group_ids:
        b = tokens_before.get(gid)
        a = tokens_after.get(gid)
        if a is None:
            deltas[gid] = None
            continue
        b = b if b is not None else 0.0
        d = a - b
        if d < 0:
            epp_restarted = True
            d = 0.0
        deltas[gid] = d

    offered_groups = [g for g in GROUPS if offered_workers.get(g, 0) > 0]
    # A single offered group is never "contended" by definition (metrics.go:
    # contended_service_tokens_total only accrues while another group in the
    # same band is also backlogged), so it legitimately scrapes at a flat
    # zero delta with a correctly-working policy. Share/deviation is not a
    # meaningful question with nobody to share against -- app1-alone's own
    # bar ("must receive ~100% of the pool") is a request-success-rate
    # question instead, judged against SOLO_SUCCESS_THRESHOLD below.
    solo = offered_groups[0] if len(offered_groups) == 1 else None
    offered_weight_total = sum(
        (weight_after.get(g) if weight_after.get(g) is not None else weight_before.get(g)) or 0.0
        for g in offered_groups
    )
    offered_tokens_total = sum(deltas.get(g) or 0.0 for g in offered_groups)

    rows = []
    deviations_for_verdict = []
    for gid in all_group_ids:
        weight = weight_after.get(gid)
        if weight is None:
            weight = weight_before.get(gid)
        is_offered = gid in offered_groups
        expected_pct = None
        observed_pct = None
        deviation_pts = None
        if is_offered and gid != solo:
            if offered_weight_total > 0 and weight is not None:
                expected_pct = 100.0 * weight / offered_weight_total
            delivered_tokens_for_pct = deltas.get(gid)
            if offered_tokens_total > 0 and delivered_tokens_for_pct is not None:
                observed_pct = 100.0 * delivered_tokens_for_pct / offered_tokens_total
            else:
                observed_pct = 0.0
            if expected_pct is not None and observed_pct is not None:
                deviation_pts = observed_pct - expected_pct
                deviations_for_verdict.append((gid, deviation_pts))

        delivered_tokens = deltas.get(gid)
        gen_row = loadgen_rows.get(gid, {"total": 0, "p50_sec": None, "p95_sec": None, "statuses": {}})
        rows.append({
            "group": gid,
            "configured_weight": weight,
            "offered": is_offered,
            "offered_workers": offered_workers.get(gid, 0),
            "requests_total": gen_row["total"],
            "status_tally": gen_row["statuses"],
            "p50_sec": gen_row["p50_sec"],
            "p95_sec": gen_row["p95_sec"],
            "delivered_tokens": delivered_tokens,
            "expected_share_pct": expected_pct,
            "observed_share_pct": observed_pct,
            "deviation_pts": deviation_pts,
        })

    SOLO_SUCCESS_THRESHOLD = 0.90  # "overwhelmingly 200" -- docs/runbook.md's own standing check
    verdict = "PASS"
    reasons = []
    if not offered_groups:
        verdict = "FAIL"
        reasons.append("no group was offered any load (empty TENANTS or unparseable loadgen.log)")
    if epp_restarted:
        verdict = "FAIL"
        reasons.append("a contended_service_tokens_total counter went backwards between snapshots -- the EPP restarted mid-run, invalidating the delta")

    if solo is not None:
        gen_row = loadgen_rows.get(solo, {"total": 0, "statuses": {}})
        total = gen_row["total"]
        ok = sum(v for k, v in gen_row["statuses"].items() if k.startswith("2"))
        success_frac = (ok / total) if total > 0 else 0.0
        if total <= 0 or success_frac < SOLO_SUCCESS_THRESHOLD:
            verdict = "FAIL"
            reasons.append(
                f"{solo} is the only offered group this run (no contention is possible, so "
                f"contended_service_tokens_total is correctly zero -- not evaluated as a share) "
                f"but only {success_frac:.1%} of its {total} requests succeeded, short of the "
                f"{SOLO_SUCCESS_THRESHOLD:.0%} bar for 'receives ~100% of the pool'"
            )
    elif offered_tokens_total <= 0 and offered_groups:
        verdict = "FAIL"
        reasons.append("offered groups delivered zero contended service tokens -- the EPP accounted nothing for this run")

    max_abs_dev = max((abs(d) for _, d in deviations_for_verdict), default=None)
    # asymmetric-demand's low-worker group is capped by its OWN worker count,
    # not by the policy -- it structurally cannot reach a weight-proportional
    # share regardless of how well fairness is enforced (this scenario's
    # whole point, per 04-loadgen.yaml, is that a correct policy gives the
    # saturating group MORE than its nominal weight when another group's
    # share goes unused). Scoring that group's huge, expected deviation
    # against the symmetric threshold would fail a run that is working
    # exactly as intended. The only thing this scenario can actually check
    # is whether the saturating group was held AT OR BELOW its own nominal
    # weight share -- i.e. whether weight acted as a ceiling instead of a
    # floor -- so it gets a dedicated, one-sided check instead of the
    # symmetric deviation threshold used by the other scenarios.
    is_demand_capped_scenario = (
        scenario == "asymmetric-demand" and solo is None and len(offered_groups) >= 2
    )
    if is_demand_capped_scenario:
        ASYMMETRIC_DEMAND_CAP_MARGIN_POINTS = 2.0  # slack for sampling noise
        dominant = max(offered_groups, key=lambda g: offered_workers.get(g, 0))
        dominant_row = next(r for r in rows if r["group"] == dominant)
        dev = dominant_row["deviation_pts"]
        if dev is None or dev < -ASYMMETRIC_DEMAND_CAP_MARGIN_POINTS:
            verdict = "FAIL"
            reasons.append(
                f"{dominant} is this scenario's saturating, highest-worker-count offered group "
                f"({dominant_row['offered_workers']} workers) but delivered "
                + (
                    "no measurable share"
                    if dev is None
                    else f"{dev:+.1f} points vs. its own nominal weight share"
                )
                + " -- its configured weight appears to be acting as a ceiling, not a floor, "
                "while another offered group's capacity went unused"
            )
    elif control:
        # UNI-103: a named negative control (e.g. equal-workers-control) is
        # run deliberately WITHOUT per-tenant over-offered sizing, so a large
        # deviation from the weighted split is the expected, correct result
        # -- work conservation draining the highest-weight tenant's queue,
        # not the policy failing. Scoring that against the symmetric
        # threshold would FAIL a run that is behaving exactly as designed, so
        # a control never reaches FAIL/PASS on the deviation check; it still
        # fails above on structural problems (no load offered, EPP restart,
        # zero tokens accounted) because those indicate the run itself was
        # invalid, control or not.
        if verdict != "FAIL":
            verdict = "INFO"
        if max_abs_dev is not None:
            reasons.append(
                f"negative control, not scored against the {threshold_points:g}-point "
                f"threshold: max deviation was {max_abs_dev:.1f} points. This scenario is "
                "expected to compress toward equal shares, not reproduce the configured "
                "weights -- see docs/runbook.md's 'Per-tenant worker sizing and the "
                "saturation check'"
            )
    elif max_abs_dev is not None and max_abs_dev > threshold_points:
        verdict = "FAIL"
        worst = max(deviations_for_verdict, key=lambda kv: abs(kv[1]))
        reasons.append(
            f"{worst[0]} deviated {worst[1]:+.1f} points from its contention-adjusted expected "
            f"share, exceeding the {threshold_points:g}-point threshold"
        )

    report = {
        "schema": "uni54.fairness_benchmark_report.v1",
        "run": {
            "scenario": scenario,
            "label": label,
            "control": control,
            "namespace": namespace,
            "enforce": enforce,
            "duration_seconds": duration_seconds if duration_seconds is not None else logged_duration,
            "backend": backend,
            "epp_image_digest": epp_image_digest,
            "epp_pod": epp_pod,
            "run_start": run_start,
            "run_end": run_end,
        },
        "groups": rows,
        "verdict": {
            "result": verdict,
            "threshold_points": threshold_points,
            "max_abs_deviation_points": max_abs_dev,
            "reasons": reasons,
            "epp_restarted_mid_run": epp_restarted,
            "solo_group": solo,
        },
        "sources": {
            "delivered_tokens_and_observed_share": (
                "llm_d_epp_maas_fairness_contended_service_tokens_total, scraped directly "
                "from the EPP's /metrics immediately before and after the run (same "
                "mechanism as deploy/poc/13-loadgen-poisson.sh). This is the EPP's own "
                "accounting -- the generator cannot see token usage. Reused unmodified "
                "from the SLI deploy/grafana-dashboard.yaml (UNI-50) already defines; "
                "this report does not invent a second definition of delivered share."
            ),
            "offered_and_delivered_requests": (
                "deploy/poc/04-loadgen.yaml's own run.sh: the 'load: tenants=...' line "
                "for offered worker counts, and the TENANT/TOTAL/P50_SEC/P95_SEC/STATUSES "
                "table for delivered requests, status tally, and latency."
            ),
            "expected_share": (
                "each offered group's configured_weight divided by the sum of configured_weight "
                "over OFFERED groups only (excludes the never-offered 'unclassified' catch-all "
                "and any group this scenario left idle), so a work-conserving policy absorbing "
                "an idle group's share is not scored as a deviation."
            ),
        },
    }
    return report


def render_markdown(report):
    r = report["run"]
    v = report["verdict"]
    lines = []
    lines.append(f"# Fairness benchmark: {r['scenario']}" + (f" ({r['label']})" if r.get('label') else ""))
    lines.append("")
    if r.get("control"):
        lines.append(
            f"**Verdict: {v['result']}** -- named negative control, not scored against the "
            f"{v['threshold_points']:g}-point threshold. Expected to NOT reproduce the "
            "configured weights; see docs/runbook.md."
        )
    else:
        lines.append(f"**Verdict: {v['result']}** (threshold: {v['threshold_points']:g} points)")
    if v["reasons"]:
        lines.append("")
        for reason in v["reasons"]:
            lines.append(f"- {reason}")
    lines.append("")
    lines.append("## Run metadata")
    lines.append("")
    lines.append("| field | value |")
    lines.append("|---|---|")
    for key, label in [
        ("scenario", "Scenario"), ("enforce", "Enforce"),
        ("duration_seconds", "Duration (s)"), ("backend", "Backend"),
        ("epp_image_digest", "EPP image digest"), ("epp_pod", "EPP pod"),
        ("namespace", "Namespace"), ("run_start", "Run start"), ("run_end", "Run end"),
    ]:
        lines.append(f"| {label} | `{r.get(key)}` |")
    lines.append("")
    lines.append("## Per-group result")
    lines.append("")
    lines.append(
        "| group | weight | offered workers | requests | statuses | p50s | p95s | "
        "delivered tokens | expected % | observed % | deviation (pts) |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for g in report["groups"]:
        def fmt(v, suffix=""):
            return "n/a" if v is None else f"{v:.1f}{suffix}" if isinstance(v, float) else f"{v}{suffix}"
        statuses = ", ".join(f"{k}={v}" for k, v in sorted(g["status_tally"].items())) or "n/a"
        lines.append(
            f"| {g['group']} | {fmt(g['configured_weight'])} | {g['offered_workers']} | "
            f"{g['requests_total']} | {statuses} | {fmt(g['p50_sec'])} | {fmt(g['p95_sec'])} | "
            f"{fmt(g['delivered_tokens'])} | {fmt(g['expected_share_pct'], '%')} | "
            f"{fmt(g['observed_share_pct'], '%')} | {fmt(g['deviation_pts'])} |"
        )
    lines.append("")
    lines.append("## Sources")
    lines.append("")
    for key, text in report["sources"].items():
        lines.append(f"- **{key}**: {text}")
    lines.append("")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--scenario", required=True)
    p.add_argument("--label", default=None)
    p.add_argument("--enforce", required=True, choices=["true", "false"])
    p.add_argument("--duration-seconds", type=int, default=None)
    p.add_argument("--backend", required=True)
    p.add_argument("--epp-image-digest", required=True)
    p.add_argument("--namespace", required=True)
    p.add_argument("--epp-pod", required=True)
    p.add_argument("--run-start", required=True)
    p.add_argument("--run-end", required=True)
    p.add_argument("--threshold-points", type=float, default=10.0)
    p.add_argument("--metrics-before", required=True)
    p.add_argument("--metrics-after", required=True)
    p.add_argument("--loadgen-log", required=True)
    p.add_argument("--out-json", required=True)
    p.add_argument("--out-md", required=True)
    p.add_argument(
        "--control", action="store_true",
        help="Named negative control (UNI-103): report the numbers but never score the "
             "weighted-split deviation as PASS/FAIL -- verdict is INFO instead, and the exit "
             "code stays 0 unless a structural problem (no load, EPP restart, zero tokens "
             "accounted) makes the run itself invalid.",
    )
    args = p.parse_args()

    report = build_report(
        scenario=args.scenario,
        label=args.label,
        enforce=(args.enforce == "true"),
        duration_seconds=args.duration_seconds,
        backend=args.backend,
        epp_image_digest=args.epp_image_digest,
        namespace=args.namespace,
        epp_pod=args.epp_pod,
        run_start=args.run_start,
        run_end=args.run_end,
        threshold_points=args.threshold_points,
        metrics_before_path=args.metrics_before,
        metrics_after_path=args.metrics_after,
        loadgen_log_path=args.loadgen_log,
        control=args.control,
    )

    with open(args.out_json, "w") as f:
        json.dump(report, f, indent=2, sort_keys=False)
        f.write("\n")
    with open(args.out_md, "w") as f:
        f.write(render_markdown(report))

    print(f"verdict: {report['verdict']['result']}")
    for reason in report["verdict"]["reasons"]:
        print(f"  - {reason}")
    return 0 if report["verdict"]["result"] in ("PASS", "INFO") else 1


if __name__ == "__main__":
    sys.exit(main())
