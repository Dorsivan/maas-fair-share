#!/usr/bin/env python3
"""UNI-282: correlate per-tenant dispatch composition against the saturation
gate's open/closed state, within a single run's own metrics-timeseries.txt
(deploy/poc/15-fairness-benchmark.sh's WINDOW_SECONDS scrape loop, UNI-127).

This is the decisive comparison the UNI-282 plan asks for: if composition
tracks the configured weight ratio while the gate is CLOSED (saturated --
utilization-detector's own roofline score >= its usageLimit) and tracks the
offered-worker ratio while the gate is OPEN (unsaturated, requests pass
through closer to arrival order), the bypass hypothesis is confirmed -- the
fairness policy is only actually deciding dispatches during the closed-gate
windows, and the worker-count leak documented across this project's
discriminating rows (UNI-225) is an admission-side gap, not a fairness-maths
bug. If composition tracks workers in BOTH buckets, the bypass hypothesis is
dead and the problem is inside the policy itself.

Gate state uses llm_d_epp_flow_control_pool_saturation{stage="effective"} --
the utilization-detector's own already-normalized roofline score (max of
queue-depth-ratio and kv-cache-ratio against their configured thresholds),
NOT llm_d_epp_flow_control_queue_size (that is the flow-control plugin's own
per-tenant PENDING queue depth -- a result of the gate's behaviour, not the
gate's own open/closed signal) and NOT llm_d_epp_average_queue_size (the raw
un-normalized backend queue depth 15-fairness-report.py's
compute_saturation_limb reconstructs a ratio from for a different purpose --
attributing which limb bound at peak, not classifying every window).
pool_saturation is pool-wide, confirming the "total depth check, not
per-tenant" framing structurally: there is exactly one signal, not one per
fairness_id.

Dispatch composition uses llm_d_epp_maas_fairness_dispatch_total{fairness_id},
a raw per-tenant dispatch COUNT -- deliberately not the token-weighted
contended_service_tokens_total 15-fairness-report.py's own share numbers use
(see that file's module docstring for why token-weighting is the right unit
for a fairness VERDICT). This diagnostic asks a different question -- which
tenant's requests got waved through the gate -- where a raw count of dispatch
events is the more direct signal and worker counts are themselves a count,
not a token quantity, so the two sides of the comparison share a unit.

Pure function of its input file -- no cluster access, matching
15-fairness-report.py's module contract. Not merged into that file: this
script answers one standalone question with its own CLI and own small
parser, not a new column on every existing report (and compute_windows'
schedule/weights machinery there is built for whole-run and phase-aware
share tables, not a two-bucket gate-state split).
"""
import argparse
import os
import re
import sys

METRIC_LINE = re.compile(r'^([^{\s]+)(?:\{(.*)\})?\s+([^\s]+)$')
LABEL = re.compile(r'(\w+)="((?:[^"\\]|\\.)*)"')
TIMESERIES_HEADER = re.compile(r'^#\s*ts=(?P<ts>\S+)\s+epoch=(?P<epoch>\d+)\s*$')
SCRAPE_EXIT = re.compile(r'^#\s*scrape_exit=(?P<rc>\d+)\s*$')

POOL_SATURATION_METRIC = "llm_d_epp_flow_control_pool_saturation"
DISPATCH_TOTAL_METRIC = "llm_d_epp_maas_fairness_dispatch_total"
REQUESTS_TOTAL_METRIC = "llm_d_epp_flow_control_requests_total"

# Same exclusion 15-fairness-report.py's EPP_SHED_OUTCOMES uses:
# EvictedContextCancelled is the client giving up, not the EPP shedding, so
# it is not EPP-originated TTL/capacity eviction and is left out here too.
EVICTED_OUTCOMES = ("EvictedTTL", "EvictedNoEndpoints", "EvictedOther")

MIN_WINDOWS_PER_BUCKET = 3


def parse_metrics_labeled_text(text):
    """{metric_name: [(labels: dict, value: float)]} -- every label kept
    (same shape 15-fairness-report.py's parse_metrics_labeled_text uses)."""
    series = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        m = METRIC_LINE.match(line)
        if not m:
            continue
        try:
            value = float(m.group(3))
        except ValueError:
            continue
        series.setdefault(m.group(1), []).append((dict(LABEL.findall(m.group(2) or '')), value))
    return series


def split_timeseries_blocks(text):
    """(epoch, iso_ts, block_text, scrape_failed) tuples, sorted by epoch --
    same contract as 15-fairness-report.py's _split_timeseries_blocks."""
    entries = []
    epoch = ts = None
    block_lines = []

    def flush():
        if epoch is not None:
            scrape_failed = False
            for line in block_lines:
                m = SCRAPE_EXIT.match(line)
                if m:
                    scrape_failed = m.group('rc') != '0'
                    break
            entries.append((epoch, ts, '\n'.join(block_lines), scrape_failed))

    for line in text.splitlines():
        m = TIMESERIES_HEADER.match(line)
        if m:
            flush()
            epoch, ts, block_lines = float(m.group('epoch')), m.group('ts'), []
        else:
            block_lines.append(line)
    flush()
    entries.sort(key=lambda e: e[0])
    return entries


def parse_timeseries(path):
    text = open(path).read()
    return [(epoch, ts, parse_metrics_labeled_text(block), scrape_failed)
            for epoch, ts, block, scrape_failed in split_timeseries_blocks(text)]


def metric_values(series, name, filters=None):
    lines = series.get(name, [])
    if not filters:
        return lines
    return [(labels, v) for labels, v in lines
            if all(labels.get(k) == v2 for k, v2 in filters.items())]


def pool_saturation(series):
    """Max across whatever inference_pool labels are present -- every run on
    file has exactly one pool, so this is a defensive combine, not a real
    aggregation choice. None if the gauge has no sample this snapshot."""
    vals = metric_values(series, POOL_SATURATION_METRIC, {"stage": "effective"})
    if not vals:
        return None
    return max(v for _, v in vals)


def dispatch_totals(series):
    out = {}
    for labels, v in metric_values(series, DISPATCH_TOTAL_METRIC):
        gid = labels.get("fairness_id")
        if gid:
            out[gid] = out.get(gid, 0.0) + v
    return out


def evicted_total(series):
    """(total, {outcome: value}) for EVICTED_OUTCOMES, read from a single
    snapshot's own cumulative counter values -- callers pass the LAST
    snapshot, never sum this across snapshots (that would double-count a
    monotonic counter)."""
    total = 0.0
    per_outcome = {}
    for labels, v in metric_values(series, REQUESTS_TOTAL_METRIC):
        outcome = labels.get("outcome")
        if outcome in EVICTED_OUTCOMES:
            per_outcome[outcome] = per_outcome.get(outcome, 0.0) + v
            total += v
    return total, per_outcome


def parse_kv_list(s):
    out = {}
    if not s:
        return out
    for part in s.split(","):
        k, _, v = part.partition("=")
        k = k.strip()
        if k:
            out[k] = float(v)
    return out


def to_pct(d):
    total = sum(d.values())
    if total <= 0:
        return {k: 0.0 for k in d}
    return {k: 100.0 * v / total for k, v in d.items()}


def l1_distance_pct(a, b, groups):
    return sum(abs((a.get(g) or 0.0) - (b.get(g) or 0.0)) for g in groups)


def fmt_pct(pct, groups):
    return ", ".join(f"{g}={pct[g]:.1f}%" for g in groups) if pct else "n/a"


def classify(pct, weights_pct, workers_pct, groups):
    """True if `pct` sits closer to the weight ratio than the worker ratio,
    False if closer to worker, None if no worker ratio was given to compare."""
    if workers_pct is None:
        return None
    d_w = l1_distance_pct(pct, weights_pct, groups)
    d_k = l1_distance_pct(pct, workers_pct, groups)
    return d_w < d_k


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results_dir",
                    help="a deploy/poc/15-fairness-benchmark.sh results/<ts>-<label>/ "
                         "directory containing metrics-timeseries.txt")
    ap.add_argument("--threshold", type=float, default=1.0,
                    help="pool_saturation roofline score at/above which the gate is "
                         "CLOSED (actively holding/picking), matching "
                         "utilization-detector's own saturation>=usageLimit test. "
                         "Default 1.0 -- the gauge is already normalized against "
                         "queueDepthThreshold/kv threshold, this is NOT a raw queue "
                         "depth number.")
    ap.add_argument("--weights", default="app1=20,app2=10,end-users=65",
                    help="comma-separated group=weight, default matches "
                         "deploy/poc/00-config.yaml's 3-group config")
    ap.add_argument("--workers", default=None,
                    help="comma-separated group=workers offered this run. No default "
                         "-- required to get an explicit bypass-confirmed/dead verdict; "
                         "omit to get bucket compositions and weight-distance only")
    args = ap.parse_args()

    ts_path = os.path.join(args.results_dir, "metrics-timeseries.txt")
    if not os.path.exists(ts_path):
        sys.exit(f"error: {ts_path} not found -- is this a results dir from "
                 f"deploy/poc/15-fairness-benchmark.sh (metrics-timeseries.txt is "
                 f"captured by every run since UNI-127, no extra flag needed)?")

    timeseries = parse_timeseries(ts_path)
    if len(timeseries) < 2:
        sys.exit(f"error: {ts_path} has fewer than 2 snapshots ({len(timeseries)}) -- "
                 f"no windows to correlate")

    weights = parse_kv_list(args.weights)
    workers = parse_kv_list(args.workers) if args.workers else None
    groups = sorted(weights)

    closed_bucket = {g: 0.0 for g in groups}
    open_bucket = {g: 0.0 for g in groups}
    closed_windows = 0
    open_windows = 0
    skipped_scrape_gap = 0
    skipped_no_gate_signal = 0
    skipped_no_dispatch = 0

    for (_, _, s0, f0), (_, _, s1, f1) in zip(timeseries, timeseries[1:]):
        if f0 or f1:
            # A scrape failure leaves the block empty, so a counter delta
            # across it reads as a drop or a spurious jump -- not a real
            # window, same reasoning 15-fairness-report.py's compute_windows
            # applies to any_scrape_gap.
            skipped_scrape_gap += 1
            continue
        sat0, sat1 = pool_saturation(s0), pool_saturation(s1)
        if sat0 is None or sat1 is None:
            skipped_no_gate_signal += 1
            continue
        gate_closed = ((sat0 + sat1) / 2.0) >= args.threshold
        d0, d1 = dispatch_totals(s0), dispatch_totals(s1)
        delta = {g: max(0.0, d1.get(g, 0.0) - d0.get(g, 0.0)) for g in groups}
        if sum(delta.values()) <= 0:
            skipped_no_dispatch += 1
            continue
        bucket = closed_bucket if gate_closed else open_bucket
        for g in groups:
            bucket[g] += delta[g]
        if gate_closed:
            closed_windows += 1
        else:
            open_windows += 1

    evicted, per_outcome = evicted_total(timeseries[-1][2])

    lines = [f"# UNI-282 gate-correlation report: {args.results_dir}", ""]
    lines.append(
        f"Windows: {len(timeseries) - 1} total, {closed_windows} gate-closed, "
        f"{open_windows} gate-open, {skipped_no_dispatch} skipped (no dispatch), "
        f"{skipped_no_gate_signal} skipped (no gate signal), "
        f"{skipped_scrape_gap} skipped (scrape gap)")

    if closed_windows == 0 and open_windows == 0:
        lines.append("")
        lines.append("INCONCLUSIVE: no window had both a usable gate-saturation "
                     "reading and at least one dispatch -- nothing to correlate.")
    else:
        closed_pct = to_pct(closed_bucket) if closed_windows else None
        open_pct = to_pct(open_bucket) if open_windows else None
        weights_pct = to_pct(weights)
        workers_pct = to_pct(workers) if workers else None

        lines.append("")
        lines.append(f"gate-closed composition ({closed_windows} windows): {fmt_pct(closed_pct, groups)}")
        lines.append(f"gate-open composition   ({open_windows} windows): {fmt_pct(open_pct, groups)}")
        lines.append(f"configured weight ratio:                 {fmt_pct(weights_pct, groups)}")
        if workers_pct:
            lines.append(f"offered worker ratio:                    {fmt_pct(workers_pct, groups)}")

        for label, pct in (("gate-closed bucket", closed_pct), ("gate-open bucket", open_pct)):
            if pct is None:
                lines.append(f"{label}: no windows in this bucket")
                continue
            d_w = l1_distance_pct(pct, weights_pct, groups)
            if workers_pct:
                d_k = l1_distance_pct(pct, workers_pct, groups)
                closer = "weight" if d_w < d_k else "worker"
                lines.append(f"{label}: {d_w:.1f}pt from weight ratio, "
                             f"{d_k:.1f}pt from worker ratio -> closer to {closer} ratio")
            else:
                lines.append(f"{label}: {d_w:.1f}pt from weight ratio "
                             f"(no --workers given to compare against worker ratio)")

        lines.append("")
        if closed_windows < MIN_WINDOWS_PER_BUCKET or open_windows < MIN_WINDOWS_PER_BUCKET:
            lines.append(
                f"INCONCLUSIVE: fewer than {MIN_WINDOWS_PER_BUCKET} windows in one bucket -- "
                f"not enough samples on that side of the gate to trust the bucket average. "
                f"Lengthen the run, or this run's gate genuinely sits almost entirely on one "
                f"side of --threshold (print the pool_saturation series to check which).")
        elif workers_pct is None:
            lines.append("NOTE: pass --workers to get an explicit bypass-confirmed/dead "
                         "verdict; without it this report only shows closeness to the "
                         "weight ratio.")
        else:
            closed_is_weight = classify(closed_pct, weights_pct, workers_pct, groups)
            open_is_weight = classify(open_pct, weights_pct, workers_pct, groups)
            if closed_is_weight and not open_is_weight:
                lines.append(
                    "VERDICT: BYPASS HYPOTHESIS CONFIRMED -- composition tracks the "
                    "configured weight ratio while the gate is closed and the offered "
                    "worker ratio while the gate is open. The fairness policy is only "
                    "actually deciding dispatches during the closed-gate windows; the fix "
                    "for the worker leak is per-tenant admission, not the fairness maths.")
            elif (not closed_is_weight) and (not open_is_weight):
                lines.append(
                    "VERDICT: BYPASS HYPOTHESIS DEAD -- composition tracks the offered "
                    "worker ratio in BOTH buckets, including while the gate is reported "
                    "closed. The policy is being consulted but computing the wrong answer, "
                    "or this gate signal does not gate what this run assumed it gates. The "
                    "worker leak is inside the policy, not an admission bypass.")
            elif closed_is_weight and open_is_weight:
                lines.append(
                    "VERDICT: NO BYPASS, POLICY HONORED THROUGHOUT -- composition tracks "
                    "the configured weight ratio in both buckets, including while the gate "
                    "is reported open. This diagnostic's specific bypass mechanism does not "
                    "explain the worker-count leak seen in whole-run numbers elsewhere in "
                    "this project; look for a different mechanism (e.g. an averaging or "
                    "accounting effect across the whole run, not a per-window dispatch "
                    "decision).")
            else:
                lines.append(
                    "VERDICT: ANOMALOUS -- composition tracks WORKERS while the gate is "
                    "closed and WEIGHTS while the gate is open, the opposite of the bypass "
                    "hypothesis's predicted direction. Treat as inconclusive and inspect the "
                    "raw buckets by hand before drawing a conclusion; this pattern was not "
                    "anticipated by the plan.")

    lines.append("")
    lines.append(
        f"evicted (EPP-originated TTL/capacity shedding, cumulative at last snapshot): "
        f"{evicted:g}" + (f" -- {per_outcome}" if evicted else ""))
    if evicted:
        lines.append(
            "** NON-ZERO EVICTED COUNT: per the UNI-282 plan, this run measured shedding, "
            "not fairness -- do not treat its composition numbers as a clean result. **")

    report = "\n".join(lines) + "\n"
    print(report)
    out_path = os.path.join(args.results_dir, "gate-correlation-report.md")
    with open(out_path, "w") as f:
        f.write(report)


if __name__ == "__main__":
    main()
