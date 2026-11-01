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

UNI-127 adds a second, purely additive layer on top of the above -- it never
changes `verdict`, only adds a `timeline` section:

  --metrics-timeseries  periodic /metrics scrapes taken throughout the run
      (deploy/poc/15-fairness-benchmark.sh's timeseries_loop), not just
      before/after. Consecutive scrapes become "windows": delivered-token
      deltas and observed/expected share over that slice of the run, instead
      of one number for the whole thing.
  --timeline-config     which tenants were scheduled active (join/leave
      offsets, on/off duty cycling) and which chaos events were scheduled
      (EPP pod delete, vLLM replica scale-down/restore), each as a seconds
      offset from run start. Tenants this run never gave an explicit
      schedule to fall back to "active for the whole run" -- the one, prior
      behaviour -- so a report built without this file, or for a scenario
      that sets none of these knobs, has an unchanged `timeline.windows`
      membership even though the windows themselves are new.

A "phase edge" is any second offset where something about the run's shape
changes: a tenant's start/stop/duty transition, or a chaos event. Time-to-
converge is measured from each edge: how many seconds until every tenant
active in that window is within `threshold_points` of its expected share,
and STAYS within it for every window up to the next edge (a single window
that happens to land close, surrounded by windows that do not, is noise, not
convergence).

UNI-135 adds a fourth verdict, UNCONTENDED (neither PASS nor FAIL), for a run
where every offered group is genuinely light -- below-capacity, not just
excluded or demand-capped like the `solo`/`capped_groups` cases above. The
rule is explicit and reuses the EPP's own evidence rather than inventing a
new metric: every offered group's
`llm_d_epp_maas_fairness_contended_seconds_total` delta must stay under
UNCONTENDED_SECONDS_THRESHOLD, an order of magnitude below the ~9s a
genuinely-contending tenant accrues in a 240s full-contention run
(docs/runbook.md). When that holds, the symmetric weighted-split deviation
check is skipped (it would only measure noise -- nobody was ever backlogged
alongside anyone else to share against), the same way it is already skipped
for `solo` and for a named `control`.
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
    r'(?:custom=\d+ )?'  # UNI-129 added this field to 04-loadgen.yaml's run.sh;
                         # it is not a GROUPS member, so it is skipped, not captured.
    r'duration=(?P<duration>\d+)s'
)
TABLE_ROW = re.compile(r'^(\S+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(.+)$')
STATUS_PAIR = re.compile(r'(\d+)=(\d+)')

# UNI-137 (B5): deploy/poc/13-loadgen-poisson.py is a second, OPEN-LOOP
# generator (Poisson arrivals at a fixed rate, run as a local process, not a
# Job) with its own log shape -- a rate, not a worker count, and a per-group
# summary line instead of the TENANT/TOTAL/P50/P95/STATUSES table. Recognized
# as an alternative to TENANTS_LINE/TABLE_ROW, never instead of them: a
# closed-loop log that matches TENANTS_LINE is tried first (see
# parse_loadgen_log), so every scenario before this ticket is byte-for-byte
# unaffected.
OPEN_LOOP_TENANTS_LINE = re.compile(
    r'load: open-loop Poisson arrivals rate app1=(?P<app1>[\d.]+)/s app2=(?P<app2>[\d.]+)/s '
    r'end-users=(?P<end_users>[\d.]+)/s duration=(?P<duration>[\d.]+)s'
)
OPEN_LOOP_ROW = re.compile(
    r'^(?P<group>\S+)\s+sent=(?P<sent>\d+)\s+completion_tokens=(?P<tok>-?\d+)\s+'
    r'p50=(?P<p50>[\d.]+)s\s+p95=(?P<p95>[\d.]+)s\s+p99=(?P<p99>[\d.]+)s\s+codes=\[(?P<codes>.*)\]$'
)

GROUPS = ("app1", "app2", "end-users")


def parse_metrics_text(text):
    """{metric_name: {fairness_id_or_None: value}} from a Prometheus text
    scrape (comment lines are harmless here; they never match METRIC_LINE)."""
    series = {}
    for raw in text.splitlines():
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


def parse_metrics(path):
    with open(path) as f:
        return parse_metrics_text(f.read())


TIMESERIES_HEADER = re.compile(r'^#\s*ts=(?P<ts>\S+)\s+epoch=(?P<epoch>\d+)\s*$')


def parse_timeseries(path):
    """A sequence of (epoch_seconds: float, iso_ts: str, series: dict) from
    deploy/poc/15-fairness-benchmark.sh's metrics-timeseries.txt: blocks of
    Prometheus text, each preceded by a '# ts=<iso> epoch=<unix seconds>'
    header. Returns entries sorted by epoch (they are written in order, but a
    clock that is not monotonic -- NTP step, not a backend restart -- would
    otherwise silently produce a negative-duration window)."""
    text = open(path).read()
    entries = []
    epoch = None
    ts = None
    block_lines = []

    def flush():
        if epoch is not None:
            entries.append((epoch, ts, parse_metrics_text('\n'.join(block_lines))))

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


def parse_loadgen_log(path):
    """Returns (offered_workers: {group: int|float}, rows: {group: {total,
    p50_sec, p95_sec, statuses}}, duration_seconds_from_log_or_None,
    generator: "closed-loop"|"open-loop").

    "offered_workers" holds a worker COUNT for the closed-loop generator and
    a Poisson RATE in req/s for the open-loop one (UNI-137/B5) -- the caller
    (build_report) only ever compares it to zero to decide whether a group
    was offered any load, which both units support identically; render_markdown
    labels the column correctly for whichever generator produced the log."""
    text = open(path).read()
    m = TENANTS_LINE.search(text)
    offered_workers = {g: 0 for g in GROUPS}
    duration = None
    generator = "closed-loop"
    if m:
        tenants = set(m.group('tenants').split())
        by_name = {"app1": m.group('app1'), "app2": m.group('app2'), "end-users": m.group('end_users')}
        for g in GROUPS:
            if g in tenants:
                offered_workers[g] = int(by_name[g])
        duration = int(m.group('duration'))
    else:
        m = OPEN_LOOP_TENANTS_LINE.search(text)
        if m:
            generator = "open-loop"
            by_name = {"app1": m.group('app1'), "app2": m.group('app2'), "end-users": m.group('end_users')}
            for g in GROUPS:
                rate = float(by_name[g])
                if rate > 0:
                    offered_workers[g] = rate
            duration = float(m.group('duration'))

    rows = {}
    if generator == "closed-loop":
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
    else:
        for line in text.splitlines():
            row = OPEN_LOOP_ROW.match(line.strip())
            if not row:
                continue
            group = row.group('group')
            if group not in GROUPS:
                continue
            rows[group] = {
                "total": int(row.group('sent')),
                "p50_sec": float(row.group('p50')),
                "p95_sec": float(row.group('p95')),
                "statuses": {code: int(count) for code, count in STATUS_PAIR.findall(row.group('codes'))},
            }
    return offered_workers, rows, duration, generator


# --- UNI-127: timeline/windowed/convergence maths ---------------------------
# Pure functions of (schedule, timeseries, weights) -- same no-cluster-access
# contract as the rest of this file. See the module docstring for the shape
# of a schedule entry and what a "phase edge" is.

def default_schedule_entry(run_duration):
    return {"start": 0.0, "stop": float(run_duration), "duty_on": None, "duty_off": None}


def resolve_schedule(timeline_tenants, offered_groups, run_duration):
    """Merge this run's explicit per-tenant timeline (deploy/poc/04-loadgen.yaml's
    START/STOP/DUTY, as recorded in timeline-config.json) with the fallback for
    every OTHER offered group: active for the whole run. A group this run
    never offered at all (TENANTS excluded it) has no schedule entry -- it was
    never a candidate, so it cannot have a phase edge or a window membership
    either."""
    schedule = {}
    timeline_tenants = timeline_tenants or {}
    for g in GROUPS:
        if g in timeline_tenants:
            e = timeline_tenants[g]
            stop = e.get("stop")
            schedule[g] = {
                "start": float(e.get("start", 0) or 0),
                "stop": float(stop) if stop is not None else float(run_duration),
                "duty_on": float(e["duty_on"]) if e.get("duty_on") else None,
                "duty_off": float(e["duty_off"]) if e.get("duty_off") else None,
            }
        elif g in offered_groups:
            schedule[g] = default_schedule_entry(run_duration)
    return schedule


def tenant_active_at(entry, t):
    """Mirrors deploy/poc/04-loadgen.yaml's tenant_active() exactly -- the
    report's idea of "active" must agree with the generator's, or a window's
    expected-share denominator would not match what was actually offered."""
    start = entry.get("start", 0) or 0
    stop = entry.get("stop")
    if stop is None:
        stop = float("inf")
    if t < start or t >= stop:
        return False
    duty_on = entry.get("duty_on")
    if not duty_on:
        return True
    duty_off = entry.get("duty_off") or 0
    cycle = duty_on + duty_off
    if cycle <= 0:
        return True
    phase = (t - start) % cycle
    return phase < duty_on


def compute_phase_edges(schedule, chaos_events, run_duration):
    """Every second-offset, within [0, run_duration], where some tenant's
    active/inactive state changes or a chaos event fires. Always includes 0
    (run start is itself the first phase)."""
    edges = {0.0}
    for entry in schedule.values():
        start, stop = entry["start"], entry["stop"]
        edges.add(max(0.0, min(start, run_duration)))
        edges.add(max(0.0, min(stop, run_duration)))
        duty_on, duty_off = entry.get("duty_on"), entry.get("duty_off")
        if duty_on:
            t, on = start, True
            while t < stop and t <= run_duration:
                edges.add(max(0.0, min(t, run_duration)))
                t += duty_on if on else (duty_off or duty_on)
                on = not on
    for ev in chaos_events or []:
        edges.add(max(0.0, min(float(ev["at_seconds"]), run_duration)))
    return sorted(e for e in edges if 0.0 <= e <= run_duration)


def compute_windows(timeseries, schedule, weights):
    """One row per consecutive pair of time-series snapshots: per-group
    delivered-token delta, which groups were active at the window's midpoint,
    and (for active groups) expected/observed share and deviation -- the same
    definitions build_report uses for the whole-run numbers, just applied to a
    slice instead of the whole run. A counter going backwards within a window
    means the EPP restarted between those two scrapes; clamp to zero and flag
    it, same as the whole-run calculation does, rather than reporting a
    negative delivered-tokens number."""
    if len(timeseries) < 2:
        return [], False
    t0 = timeseries[0][0]
    windows = []
    any_restart = False
    for (e0, _, s0), (e1, _, s1) in zip(timeseries, timeseries[1:]):
        tok0 = s0.get("llm_d_epp_maas_fairness_contended_service_tokens_total", {})
        tok1 = s1.get("llm_d_epp_maas_fairness_contended_service_tokens_total", {})
        start_s, end_s = e0 - t0, e1 - t0
        mid_s = (start_s + end_s) / 2.0
        deltas = {}
        for gid in schedule:
            b, a = tok0.get(gid, 0.0), tok1.get(gid, 0.0)
            d = a - b
            if d < 0:
                any_restart = True
                d = 0.0
            deltas[gid] = d
        active = [g for g in schedule if tenant_active_at(schedule[g], mid_s)]
        weight_total = sum(weights.get(g) or 0.0 for g in active)
        tokens_total = sum(deltas.get(g, 0.0) for g in active)
        groups = []
        for gid in schedule:
            is_active = gid in active
            expected_pct = 100.0 * weights.get(gid, 0.0) / weight_total if is_active and weight_total > 0 else None
            if is_active:
                observed_pct = 100.0 * deltas.get(gid, 0.0) / tokens_total if tokens_total > 0 else 0.0
            else:
                observed_pct = None
            deviation = (observed_pct - expected_pct) if (expected_pct is not None and observed_pct is not None) else None
            groups.append({
                "group": gid,
                "active": is_active,
                "delivered_tokens": deltas.get(gid, 0.0),
                "expected_share_pct": expected_pct,
                "observed_share_pct": observed_pct,
                "deviation_pts": deviation,
            })
        windows.append({"start_s": start_s, "end_s": end_s, "groups": groups})
    return windows, any_restart


def compute_convergence(windows, phase_edges, threshold_points):
    """For each phase edge, the first window at/after it from which every
    active group's deviation stays within threshold_points for the rest of
    that phase (up to the next edge). A single in-threshold window surrounded
    by out-of-threshold ones does not count -- "converges and stays there" is
    the literal bar this ticket sets."""
    edges_sorted = sorted(phase_edges)
    results = []
    for i, edge in enumerate(edges_sorted):
        next_edge = edges_sorted[i + 1] if i + 1 < len(edges_sorted) else float("inf")
        segment = [w for w in windows if w["start_s"] >= edge - 1e-9 and w["start_s"] < next_edge]
        converged_at = None
        for j, w in enumerate(segment):
            rest = segment[j:]

            def in_threshold(win):
                devs = [g["deviation_pts"] for g in win["groups"] if g["active"] and g["deviation_pts"] is not None]
                return bool(devs) and all(abs(d) <= threshold_points for d in devs)

            if all(in_threshold(w2) for w2 in rest):
                converged_at = w["start_s"]
                break
        results.append({
            "phase_edge_s": edge,
            "converged_at_s": converged_at,
            "seconds_to_converge": (converged_at - edge) if converged_at is not None else None,
        })
    return results


def build_report(*, scenario, enforce, duration_seconds, backend, epp_image_digest,
                  namespace, epp_pod, run_start, run_end, threshold_points,
                  metrics_before_path, metrics_after_path, loadgen_log_path,
                  label=None, control=False,
                  metrics_timeseries_path=None, timeline_config_path=None,
                  window_seconds=10.0):
    before = parse_metrics(metrics_before_path)
    after = parse_metrics(metrics_after_path)
    offered_workers, loadgen_rows, logged_duration, generator = parse_loadgen_log(loadgen_log_path)

    weight_before = before.get("llm_d_epp_maas_fairness_configured_weight", {})
    weight_after = after.get("llm_d_epp_maas_fairness_configured_weight", {})
    tokens_before = before.get("llm_d_epp_maas_fairness_contended_service_tokens_total", {})
    tokens_after = after.get("llm_d_epp_maas_fairness_contended_service_tokens_total", {})
    contended_seconds_before = before.get("llm_d_epp_maas_fairness_contended_seconds_total", {})
    contended_seconds_after = after.get("llm_d_epp_maas_fairness_contended_seconds_total", {})
    # UNI-136 (C8): the EPP's own dispatch-opportunity count, per
    # docs/runbook.md's panel table ("Dispatch share vs token share ... C8")
    # -- an independent, EPP-side cross-check of requests_total (the
    # client's own count, from the loadgen log) for the "split by request
    # count" deliverable. Same before/after delta mechanism as
    # contended_service_tokens_total above.
    dispatch_before = before.get("llm_d_epp_maas_fairness_dispatch_total", {})
    dispatch_after = after.get("llm_d_epp_maas_fairness_dispatch_total", {})
    # UNI-136 (C8): a Gauge, not a Counter -- cumulative cached/total prompt
    # tokens since the EPP process started (pkg/fairness/weightedlas/state.go
    # groupState.cachedRatio()), not scoped to this run. Reading it straight
    # from the "after" snapshot is only a clean per-run figure when the EPP
    # was restarted immediately before this run started (so the cumulative
    # window IS this run); 15-fairness-benchmark.sh does not do this
    # automatically, so the caller must restart the EPP pod first and record
    # that it did. A report built without that precondition still shows the
    # value -- it is just contaminated by whatever traffic preceded it.
    cached_ratio_after = after.get("llm_d_epp_maas_fairness_prompt_tokens_cached_ratio", {})

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

    # UNI-135: same before/after delta mechanism as contended_service_tokens
    # above, for contended_seconds_total -- the "was this group ever actually
    # backlogged alongside anyone else" evidence the UNCONTENDED verdict
    # reads below. A backwards counter here means the same EPP restart the
    # tokens counter would also have caught; fold into the same flag rather
    # than inventing a second one.
    contended_seconds_deltas = {}
    for gid in all_group_ids:
        b = contended_seconds_before.get(gid)
        a = contended_seconds_after.get(gid)
        if a is None:
            contended_seconds_deltas[gid] = None
            continue
        b = b if b is not None else 0.0
        d = a - b
        if d < 0:
            epp_restarted = True
            d = 0.0
        contended_seconds_deltas[gid] = d

    # UNI-136 (C8): same before/after delta mechanism as contended_seconds
    # above, for dispatch_total.
    dispatch_deltas = {}
    for gid in all_group_ids:
        b = dispatch_before.get(gid)
        a = dispatch_after.get(gid)
        if a is None:
            dispatch_deltas[gid] = None
            continue
        b = b if b is not None else 0.0
        d = a - b
        if d < 0:
            epp_restarted = True
            d = 0.0
        dispatch_deltas[gid] = d

    offered_groups = [g for g in GROUPS if offered_workers.get(g, 0) > 0]
    # A single offered group is never "contended" by definition (metrics.go:
    # contended_service_tokens_total only accrues while another group in the
    # same band is also backlogged), so it legitimately scrapes at a flat
    # zero delta with a correctly-working policy. Share/deviation is not a
    # meaningful question with nobody to share against -- app1-alone's own
    # bar ("must receive ~100% of the pool") is a request-success-rate
    # question instead, judged against SOLO_SUCCESS_THRESHOLD below.
    solo = offered_groups[0] if len(offered_groups) == 1 else None
    # UNI-134: app2-trickle offers app2 alongside two HARD tenants, but at a
    # demand (2 workers) well under its own weight entitlement -- the same
    # "structurally capped by its own worker count" situation
    # asymmetric-demand already handles for a single dominant tenant, except
    # here TWO other tenants (app1, end-users) are both HARD and need to be
    # scored against EACH OTHER's weights, not against a 3-way split that
    # still counts app2's unreachable entitlement in the denominator. Exclude
    # app2 from offered_weight_total so app1/end-users' expected share
    # renormalizes to 23.5/76.5 (20:65) exactly as app2-idle's pair, and give
    # app2 its own demand-capped check below instead of the symmetric
    # deviation threshold.
    capped_groups = {"app2"} if scenario == "app2-trickle" and len(offered_groups) == 3 else set()
    offered_weight_total = sum(
        (weight_after.get(g) if weight_after.get(g) is not None else weight_before.get(g)) or 0.0
        for g in offered_groups
        if g not in capped_groups
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
        if is_offered and gid != solo and gid not in capped_groups:
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
            "contended_seconds": contended_seconds_deltas.get(gid),
            "prompt_tokens_cached_ratio": cached_ratio_after.get(gid),
            "dispatch_total": dispatch_deltas.get(gid),
        })

    # UNI-135: A6 "below capacity, everyone light" -- every tenant offered at
    # well under its own saturating concurrency (deploy/poc/15-fairness-
    # benchmark.sh's below-capacity scenario), so nobody is ever backlogged
    # alongside anyone else. docs/runbook.md's own reference point: a
    # genuinely-contending tenant in full-contention accrues ~9s of
    # contended_seconds_total over a 240s run; UNCONTENDED_SECONDS_THRESHOLD
    # is set an order of magnitude below that, the same "order of magnitude
    # below its peers" margin the runbook already uses to distrust an
    # under-contended tenant's measured share. Excluded from this check the
    # same way they are excluded from the deviation check: `solo` (its own,
    # already-documented reason nobody can be contended against it) and a
    # named `control` (deliberately under-offered for a different, already-
    # scored reason).
    #
    # UNI-137 (B5): a MISSING contended_seconds_total delta (the EPP's
    # Prometheus client lazily registers each label, so a group never once
    # contended has no line in either snapshot) is only trustworthy as
    # "zero contention" when corroborated by an equally missing/zero
    # contended_service_tokens_total delta -- both SLIs share the same
    # contention gate in metrics.go, so a group that was genuinely contended
    # cannot have tokens without seconds. Requiring that correlation (rather
    # than treating every missing-seconds group as uncontended outright)
    # keeps this from misreading a test fixture or a metrics-scrape gap that
    # only omitted contended_seconds_total as "uncontended" when
    # contended_service_tokens_total shows real, measured contention. The
    # live below-saturation run (b5-open-loop-below-saturation) hit the
    # correlated case for a fresh group (end-users) that was genuinely never
    # contended: both deltas were missing, and a `None`-disqualifies reading
    # scored it FAIL ("the EPP accounted nothing for this run") when the
    # correct verdict is UNCONTENDED; see
    # test_open_loop_below_saturation_reports_uncontended_when_metric_never_materialized.
    UNCONTENDED_SECONDS_THRESHOLD = 1.0
    def _group_uncontended(g):
        seconds = contended_seconds_deltas.get(g)
        if seconds is not None:
            return seconds < UNCONTENDED_SECONDS_THRESHOLD
        tokens = deltas.get(g)
        return tokens is None or tokens <= 0
    is_uncontended = (
        solo is None
        and not control
        and len(offered_groups) >= 2
        and all(_group_uncontended(g) for g in offered_groups)
    )

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
    elif is_uncontended:
        # A genuinely uncontended run legitimately scrapes near-zero
        # contended_service_tokens_total too -- that counter only accrues
        # under the same contention contended_seconds_total measures (both
        # metrics.go SLIs share the same gate). Flagging this as "the EPP
        # accounted nothing" would fail a run that is behaving exactly as
        # this scenario intends.
        pass
    elif offered_tokens_total <= 0 and offered_groups:
        verdict = "FAIL"
        reasons.append("offered groups delivered zero contended service tokens -- the EPP accounted nothing for this run")

    # UNI-134: app2-trickle's capped group (app2) is excluded from the
    # weighted-split comparison above -- it structurally cannot reach a
    # weight-proportional share at 2 workers, by design. The only thing this
    # scenario can check for that group is "did a weight floor throttle it
    # BELOW what it asked for", the same success-rate proxy app1-alone/
    # app2-alone use for "receives ~100% of the pool" (no independent
    # uncontended baseline is captured in-run to compare latency against).
    CAPPED_SUCCESS_THRESHOLD = 0.90
    for cg in sorted(capped_groups):
        gen_row = loadgen_rows.get(cg, {"total": 0, "statuses": {}})
        total = gen_row["total"]
        ok = sum(v for k, v in gen_row["statuses"].items() if k.startswith("2"))
        success_frac = (ok / total) if total > 0 else 0.0
        if total <= 0 or success_frac < CAPPED_SUCCESS_THRESHOLD:
            verdict = "FAIL"
            reasons.append(
                f"{cg} is this scenario's demand-capped trickle group ({offered_workers.get(cg, 0)} "
                f"workers, well under its own weight entitlement) but only {success_frac:.1%} of "
                f"its {total} requests succeeded, short of the {CAPPED_SUCCESS_THRESHOLD:.0%} bar "
                "for 'gets everything it asks for'"
            )

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
    if is_uncontended:
        if verdict != "FAIL":
            verdict = "UNCONTENDED"
        reasons.append(
            "every offered group's contended_seconds_total delta stayed under "
            f"{UNCONTENDED_SECONDS_THRESHOLD:g}s (" +
            ", ".join(
                f"{g}={'never contended' if contended_seconds_deltas.get(g) is None else f'{contended_seconds_deltas[g]:.2f}s'}"
                for g in offered_groups
            ) +
            f") -- an order of magnitude below the ~9s a genuinely-contending tenant "
            "accrues in a 240s full-contention run (docs/runbook.md), so nobody was ever "
            "backlogged alongside anyone else and the weighted-split deviation check does "
            "not apply"
        )
    elif is_demand_capped_scenario:
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

    # UNI-127: purely additive. Never reads or writes `verdict` above -- a run
    # with no timeseries/timeline-config, or one that doesn't use any of the
    # timeline/chaos knobs, gets timeline=None or an empty-schedule timeline,
    # and the verdict this report's "done when" is graded on is identical
    # either way.
    timeline_section = None
    if metrics_timeseries_path:
        run_duration = duration_seconds if duration_seconds is not None else (logged_duration or 0)
        timeline_cfg = {}
        if timeline_config_path:
            with open(timeline_config_path) as f:
                timeline_cfg = json.load(f)
        schedule = resolve_schedule(timeline_cfg.get("tenants"), set(offered_groups), run_duration)
        chaos_events = timeline_cfg.get("chaos_events", [])
        weights = {g: (weight_after.get(g) if weight_after.get(g) is not None else weight_before.get(g)) or 0.0
                   for g in schedule}
        timeseries = parse_timeseries(metrics_timeseries_path)
        windows, windows_epp_restarted = compute_windows(timeseries, schedule, weights)
        phase_edges = compute_phase_edges(schedule, chaos_events, run_duration)
        convergence = compute_convergence(windows, phase_edges, threshold_points)
        timeline_section = {
            "window_seconds": window_seconds,
            "schedule": schedule,
            "chaos_events": chaos_events,
            "phase_edges": phase_edges,
            "windows": windows,
            "convergence": convergence,
            "epp_restarted_during_windows": windows_epp_restarted,
        }

    report = {
        "schema": "uni54.fairness_benchmark_report.v1",
        "run": {
            "scenario": scenario,
            "label": label,
            "control": control,
            "generator": generator,
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
            "capped_groups": sorted(capped_groups),
            "uncontended_threshold_seconds": UNCONTENDED_SECONDS_THRESHOLD,
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
            ) if generator == "closed-loop" else (
                "deploy/poc/13-loadgen-poisson.py's own stdout (UNI-137/B5): the "
                "'load: open-loop Poisson arrivals rate ...' line for each offered group's "
                "Poisson arrival rate in req/s -- NOT a worker count, this generator is "
                "open-loop -- and each group's own 'sent=... completion_tokens=... p50=...s "
                "p95=...s p99=...s codes=[...]' summary line for delivered requests, status "
                "tally, and latency."
            ),
            "expected_share": (
                "each offered group's configured_weight divided by the sum of configured_weight "
                "over OFFERED groups only (excludes the never-offered 'unclassified' catch-all "
                "and any group this scenario left idle), so a work-conserving policy absorbing "
                "an idle group's share is not scored as a deviation. Also excludes any "
                "'capped_groups' entry (UNI-134's app2-trickle): a group offered but "
                "structurally unable to reach a weight-proportional share at its own worker "
                "count is scored on a dedicated 'did it get served' check instead, not folded "
                "into the other groups' expected-share denominator."
            ),
        },
        "timeline": timeline_section,
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
    elif v["result"] == "UNCONTENDED":
        lines.append(
            f"**Verdict: UNCONTENDED** -- every offered group's `contended_seconds_total` "
            f"delta stayed under {v['uncontended_threshold_seconds']:g}s, so the pool was "
            f"never actually contended. Not scored against the {v['threshold_points']:g}-point "
            "weighted-split threshold; see docs/runbook.md."
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
        ("scenario", "Scenario"), ("generator", "Generator"), ("enforce", "Enforce"),
        ("duration_seconds", "Duration (s)"), ("backend", "Backend"),
        ("epp_image_digest", "EPP image digest"), ("epp_pod", "EPP pod"),
        ("namespace", "Namespace"), ("run_start", "Run start"), ("run_end", "Run end"),
    ]:
        lines.append(f"| {label} | `{r.get(key)}` |")
    lines.append("")
    lines.append("## Per-group result")
    lines.append("")
    offered_col = "offered req/s" if r.get("generator") == "open-loop" else "offered workers"
    lines.append(
        f"| group | weight | {offered_col} | requests | statuses | p50s | p95s | "
        "delivered tokens | expected % | observed % | deviation (pts) | contended_seconds | "
        "cached ratio | dispatch_total |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for g in report["groups"]:
        def fmt(v, suffix=""):
            return "n/a" if v is None else f"{v:.1f}{suffix}" if isinstance(v, float) else f"{v}{suffix}"
        statuses = ", ".join(f"{k}={v}" for k, v in sorted(g["status_tally"].items())) or "n/a"
        cached_pct = g["prompt_tokens_cached_ratio"]
        cached_pct = None if cached_pct is None else cached_pct * 100.0
        lines.append(
            f"| {g['group']} | {fmt(g['configured_weight'])} | {fmt(g['offered_workers'])} | "
            f"{g['requests_total']} | {statuses} | {fmt(g['p50_sec'])} | {fmt(g['p95_sec'])} | "
            f"{fmt(g['delivered_tokens'])} | {fmt(g['expected_share_pct'], '%')} | "
            f"{fmt(g['observed_share_pct'], '%')} | {fmt(g['deviation_pts'])} | "
            f"{fmt(g['contended_seconds'], 's')} | {fmt(cached_pct, '%')} | "
            f"{fmt(g['dispatch_total'])} |"
        )
    lines.append("")
    lines.append("## Timeline (UNI-127)")
    lines.append("")
    t = report.get("timeline")
    if not t:
        lines.append("N/A: no `--metrics-timeseries` recorded for this run (older report, or the "
                      "benchmark script predates UNI-127).")
    else:
        lines.append(f"Window size: {t['window_seconds']:g}s (actual window durations vary slightly "
                      "with scrape latency; see each window's own start/end below).")
        lines.append("")
        if t["chaos_events"]:
            lines.append("**Chaos events (scheduled):**")
            for ev in t["chaos_events"]:
                detail = ", ".join(f"{k}={v}" for k, v in ev.items() if k not in ("type", "at_seconds"))
                lines.append(f"- t+{ev['at_seconds']:g}s: {ev['type']}" + (f" ({detail})" if detail else ""))
        else:
            lines.append("**Chaos events:** none configured for this run.")
        lines.append("")
        lines.append("**Per-tenant schedule:**")
        for gid, e in t["schedule"].items():
            duty = f"{e['duty_on']:g}s on / {e['duty_off']:g}s off" if e.get("duty_on") else "no duty cycle"
            lines.append(f"- {gid}: active {e['start']:g}s-{e['stop']:g}s, {duty}")
        lines.append("")
        lines.append("**Time-to-converge** (seconds from a phase edge until every active tenant is "
                      f"within {report['verdict']['threshold_points']:g} points and stays there):")
        lines.append("")
        lines.append("| phase edge (s) | converged at (s) | seconds to converge |")
        lines.append("|---|---|---|")
        for c in t["convergence"]:
            conv = "n/a (never converged in this phase)" if c["converged_at_s"] is None else f"{c['converged_at_s']:.1f}"
            secs = "n/a" if c["seconds_to_converge"] is None else f"{c['seconds_to_converge']:.1f}"
            lines.append(f"| {c['phase_edge_s']:.1f} | {conv} | {secs} |")
        lines.append("")
        lines.append(f"**Windows** ({len(t['windows'])} total" +
                      (", EPP restart detected mid-window at least once" if t["epp_restarted_during_windows"] else "") +
                      "):")
        lines.append("")
        lines.append("| start (s) | end (s) | group | active | delivered tokens | expected % | observed % | deviation (pts) |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for w in t["windows"]:
            for g in w["groups"]:
                def wfmt(v, suffix=""):
                    return "n/a" if v is None else f"{v:.1f}{suffix}"
                lines.append(
                    f"| {w['start_s']:.1f} | {w['end_s']:.1f} | {g['group']} | {g['active']} | "
                    f"{wfmt(g['delivered_tokens'])} | {wfmt(g['expected_share_pct'], '%')} | "
                    f"{wfmt(g['observed_share_pct'], '%')} | {wfmt(g['deviation_pts'])} |"
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
    p.add_argument(
        "--metrics-timeseries", default=None,
        help="UNI-127: path to the periodic /metrics scrape file "
             "(deploy/poc/15-fairness-benchmark.sh's metrics-timeseries.txt). Omit to get a "
             "report with no 'timeline' section -- the pre-UNI-127 shape.",
    )
    p.add_argument(
        "--timeline-config", default=None,
        help="UNI-127: path to timeline-config.json (per-tenant START/STOP/DUTY and chaos "
             "events). Omit to treat every offered group as active the whole run.",
    )
    p.add_argument("--window-seconds", type=float, default=10.0)
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
        metrics_timeseries_path=args.metrics_timeseries,
        timeline_config_path=args.timeline_config,
        window_seconds=args.window_seconds,
    )

    with open(args.out_json, "w") as f:
        json.dump(report, f, indent=2, sort_keys=False)
        f.write("\n")
    with open(args.out_md, "w") as f:
        f.write(render_markdown(report))

    print(f"verdict: {report['verdict']['result']}")
    for reason in report["verdict"]["reasons"]:
        print(f"  - {reason}")
    return 0 if report["verdict"]["result"] in ("PASS", "INFO", "UNCONTENDED") else 1


if __name__ == "__main__":
    sys.exit(main())
