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

UNI-138 (G2) adds a second, purely additive layer -- like UNI-127's timeline,
it never changes `verdict`, only adds a `ledger` section. It checks a
different invariant than the weighted-split SLI: does the EPP's own
accounting agree with what the client actually sent and received, not just
whether the split matches the configured weights.

  --client-record-jsonl   deploy/poc/04-loadgen.yaml's CLIENT_RECORD_JSON
      lines (one per offered tenant), pulled out of the loadgen pod's stdout
      by 15-fairness-benchmark.sh into client-request-summary.jsonl. Real
      usage-block prompt/completion token counts the client itself observed
      -- independent of the EPP's internal accounting, since it comes from
      the client's own HTTP responses.

Two EPP-side numbers are cross-checked against that client ledger, per
offered tenant:

  - `llm_d_epp_request_input_tokens_sum` + `_output_tokens_sum` (the "total"
    raw-token counters): these are core framework histograms, observed only
    from a real response Usage block (pkg/epp/handlers/response.go), never
    from the fairness plugin's dispatch-time estimate, and are NOT gated on
    contention -- every completed request with a usage block counts. This is
    the most direct check: raw tokens in should equal raw tokens out,
    regardless of cost model.
  - `llm_d_epp_maas_fairness_contended_service_tokens_total` (the "cost"
    counter already used for the weighted-split SLI above): this one IS
    gated on contention, and is denominated in the configured cost unit
    (inputTokenWeight*(prompt-cached) + cachedInputTokenWeight*cached +
    outputTokenWeight*completion -- see pkg/fairness/weightedlas/cost.go),
    not raw tokens. Comparing it to raw client tokens directly would read a
    deliberate cost-model choice (outputTokenWeight=2.0 live) as a bug, so
    the client's own prompt/completion totals are run through the same
    formula first (using the EPP's own measured cached-token delta, since
    the client has no way to see cache hits) before the two are compared.
    Caller-supplied --input-token-weight/--output-token-weight/
    --cached-input-token-weight (no metric exposes these; the caller reads
    them from the live EPP ConfigMap) select the formula; they default to
    1.0/1.0/1.0 (plain token sum) so an older report is unaffected. This
    check is only meaningful for a scenario shaped like "full contention for
    (almost) the whole run" -- the contention gate and the client's
    whole-run total are treated as covering the same set of requests, which
    only holds when nobody is ever offered without being contended.

`--ledger-tolerance-pct` (default 10.0, independent of --threshold-points)
is the max absolute percent difference allowed on either check before a
group fails the ledger cross-check. The result lives in
`report["ledger"]["verdict"]`, separate from the top-level `verdict` --
these are different invariants and a run can fail one without the other.

UNI-181 adds three more purely additive sections, none of which reads or
writes `verdict`:

  - `shed`: per offered group, client-observed 429/503 counts and shed rate
      set against the group's weight share; plus, when the snapshots carry
      llm_d_epp_flow_control_requests_total, the EPP's own pool-wide shed
      count and how many of the client's 429s it can account for.
  - `pick_latency`: p50/p99 of the EPP's scheduler_e2e and flow-control
      dispatch-cycle histograms over the run, optionally against a baseline
      report (--pick-latency-baseline).
  - `alerts`: fire/clear episodes, relative to run start, from an ALERTS
      range-query export (--alerts-json), with every rule named in
      --alert-rules listed even when it never fired.

Every one of them distinguishes "never happened" (a measured zero) from "not
recorded" (unknown) rather than printing a blank. See docs/runbook.md
"Shed rate, EPP pick latency, and alert fire/clear (UNI-181)".
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone

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

# UNI-179: 04-loadgen.yaml's run.sh now dispatches any declared group set
# (LOADGEN_GROUPS) and logs it as one extra line. TENANTS_LINE above still
# carries the three built-ins (byte-identical for a 3-group run); this line is
# how a 6- or 20-group run tells the report about app3..appN, so their table
# rows and G2 ledger rows are not silently dropped. "custom" is never added
# from it: that group's fairness id is whatever its arbitrary subscription
# classifies to, not the literal name, so it stays out exactly as before.
GROUPS_LINE = re.compile(r'load: UNI-179 groups=\[(?P<groups>[^\]]*)\]')
GROUPS_ENTRY = re.compile(r'(?P<name>[a-z0-9-]+)=(?P<workers>\d+)')


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
        gm = GROUPS_LINE.search(text)
        if gm:
            for entry in GROUPS_ENTRY.finditer(gm.group('groups')):
                name = entry.group('name')
                if name not in GROUPS and name != "custom":
                    offered_workers[name] = int(entry.group('workers'))
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
            if group not in offered_workers:
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


def parse_client_record(path):
    """{group: {...}} from deploy/poc/15-fairness-benchmark.sh's
    client-request-summary.jsonl -- one CLIENT_RECORD_JSON line per tenant,
    emitted by deploy/poc/04-loadgen.yaml's run.sh and already pulled out of
    the loadgen pod's own stdout. These are real usage-block token counts the
    client itself sent/received (see docs/runbook.md "The client-side
    record"), independent evidence from the client's own HTTP responses, not
    the EPP's internal accounting."""
    records = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            records[rec["group"]] = rec
    return records


def _counter_deltas(before_map, after_map, group_ids):
    """Per-group delta of a cumulative Counter/Histogram-sum metric between
    two snapshots, with the same backwards-counter EPP-restart detection the
    contended_service_tokens_total/contended_seconds_total/dispatch_total
    deltas in build_report use. Returns (deltas, restarted)."""
    deltas = {}
    restarted = False
    for gid in group_ids:
        b = before_map.get(gid)
        a = after_map.get(gid)
        if a is None:
            deltas[gid] = None
            continue
        b = b if b is not None else 0.0
        d = a - b
        if d < 0:
            restarted = True
            d = 0.0
        deltas[gid] = d
    return deltas, restarted


# --- UNI-181: shed rate, EPP pick latency, alert fire/clear ------------------
# parse_metrics_text above keeps only the fairness_id label, which collapses a
# histogram's `le` buckets and an `outcome`-labelled counter into one value.
# These three sections need the other labels, so they use their own parser
# rather than changing the one every pre-existing section is built on.

def parse_metrics_labeled(path):
    """{metric_name: [(labels: dict, value: float)]} -- every label kept."""
    series = {}
    with open(path) as f:
        for raw in f:
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


# The EPP's own scheduling cost, separate from inference cost. Both are
# unlabelled histograms in llm-d-router v0.11.0 (pkg/epp/metrics/
# llm_d_router_metrics.go); names confirmed against a live full /metrics
# scrape (results/20261101T224216Z-uni140-b6-full-contention-soak/
# metrics-full-before.txt). scheduler_e2e is the pick itself (scheduler.go:
# filter/score/pick for one request); dispatch_cycle is one flow-control
# dispatch cycle, which is where the weighted-LAS fairness policy runs.
PICK_LATENCY_HISTOGRAMS = (
    ("scheduler_e2e", "llm_d_epp_scheduler_e2e_duration_seconds"),
    ("flow_control_dispatch_cycle", "llm_d_epp_flow_control_dispatch_cycle_duration_seconds"),
)

# Pool-wide (no fairness_id label) flow-control outcome counter. Outcomes
# that end in the EPP refusing the request, per pkg/epp/flowcontrol/types/
# outcomes.go. EvictedContextCancelled is excluded: that is the client giving
# up, not the EPP shedding. EPP_429_OUTCOMES is the subset translated to 429
# rather than 503 (requestcontrol/admission.go translateFlowControlError);
# EvictedTTL is 503 instead when the pool has no endpoints at that moment, so
# treat their sum as an upper bound on EPP-originated 429s.
FLOW_CONTROL_REQUESTS_TOTAL = "llm_d_epp_flow_control_requests_total"
EPP_SHED_OUTCOMES = ("RejectedCapacity", "RejectedNoEndpoints", "RejectedOther",
                     "EvictedTTL", "EvictedNoEndpoints", "EvictedOther")
EPP_429_OUTCOMES = ("RejectedCapacity", "EvictedTTL")

SHED_STATUSES = ("429", "503")


def _histogram_buckets(labeled, name):
    """{le: cumulative_count} for `name`, summed across any non-`le` labels,
    or None if the histogram has no _bucket line at all in this snapshot."""
    lines = labeled.get(name + "_bucket")
    if not lines:
        return None
    buckets = {}
    for labels, value in lines:
        le = labels.get("le")
        if le is None:
            continue
        bound = float("inf") if le == "+Inf" else float(le)
        buckets[bound] = buckets.get(bound, 0.0) + value
    return buckets or None


def histogram_quantile(q, buckets):
    """Prometheus histogram_quantile semantics over {upper_bound: cumulative
    count}: linear interpolation inside the bucket the rank falls in, lower
    bound 0 for the first bucket, and the highest finite bound when the rank
    falls in +Inf. Returns (value, (lower, upper)) or (None, None) when the
    histogram holds no observations."""
    bounds = sorted(buckets)
    if not bounds or bounds[-1] != float("inf"):
        return None, None
    total = buckets[float("inf")]
    if total <= 0:
        return None, None
    rank = q * total
    prev_bound, prev_count = 0.0, 0.0
    for b in bounds:
        count = buckets[b]
        if count >= rank:
            if b == float("inf"):
                finite = [x for x in bounds if x != float("inf")]
                top = finite[-1] if finite else None
                return top, (top, b)
            if count == prev_count:
                return b, (prev_bound, b)
            return prev_bound + (b - prev_bound) * (rank - prev_count) / (count - prev_count), (prev_bound, b)
        prev_bound, prev_count = b, count
    return None, None


def _bucket_json(bucket):
    # JSON has no infinity; spell the +Inf bucket the way Prometheus does.
    if not bucket:
        return None
    return ["+Inf" if b == float("inf") else b for b in bucket]


def compute_pick_latency(before_labeled, after_labeled, baseline=None):
    """p50/p99 of each PICK_LATENCY_HISTOGRAMS entry over this run (after
    minus before, bucket by bucket). Each entry says which of three states it
    is in, never a bare blank:
      - "not_recorded": no _bucket line in either snapshot. Unknown, not zero
        -- the benchmark's snapshot filter did not capture the family (as of
        UNI-181 15-fairness-benchmark.sh's snapshot_metrics does not), or the
        EPP never scheduled anything in its lifetime.
      - "no_observations": captured, but the count did not move during the run.
      - "ok": p50/p99 computed.
    `baseline` is another report's pick_latency section (UNI-181: the 3-group
    run is the reference); when given, each ok entry also carries p50/p99 as
    a ratio of the baseline's."""
    histograms = {}
    restarted = False
    for key, name in PICK_LATENCY_HISTOGRAMS:
        b = _histogram_buckets(before_labeled, name)
        a = _histogram_buckets(after_labeled, name)
        entry = {"metric": name, "state": None, "observations": None,
                 "p50_seconds": None, "p99_seconds": None,
                 "p50_bucket": None, "p99_bucket": None, "p99_at_histogram_ceiling": None,
                 "baseline_p50_seconds": None, "baseline_p99_seconds": None,
                 "p50_vs_baseline": None, "p99_vs_baseline": None}
        if a is None and b is None:
            entry["state"] = "not_recorded"
            histograms[key] = entry
            continue
        a = a or {}
        b = b or {}
        delta = {}
        went_backwards = False
        for bound in set(a) | set(b):
            d = a.get(bound, 0.0) - b.get(bound, 0.0)
            if d < 0:
                went_backwards = True
                d = 0.0
            delta[bound] = d
        if went_backwards:
            restarted = True
            # A backwards bucket means the EPP restarted between snapshots, so
            # the "after" histogram alone is this run's tail. Using it beats
            # reporting a run-spanning subtraction that mixes two processes.
            delta = dict(a)
        count = delta.get(float("inf"), 0.0)
        entry["observations"] = count
        if count <= 0:
            entry["state"] = "no_observations"
            histograms[key] = entry
            continue
        p50, p50_bucket = histogram_quantile(0.50, delta)
        p99, p99_bucket = histogram_quantile(0.99, delta)
        finite = sorted(x for x in delta if x != float("inf"))
        entry.update({
            "state": "ok",
            "p50_seconds": p50, "p99_seconds": p99,
            "p50_bucket": _bucket_json(p50_bucket),
            "p99_bucket": _bucket_json(p99_bucket),
            # Above the top finite bucket the histogram can only say "at
            # least this much" -- flag it rather than print a fake ceiling.
            "p99_at_histogram_ceiling": bool(finite) and p99_bucket is not None and p99_bucket[1] == float("inf"),
        })
        base = (baseline or {}).get("histograms", {}).get(key)
        if base and base.get("state") == "ok":
            entry["baseline_p50_seconds"] = base.get("p50_seconds")
            entry["baseline_p99_seconds"] = base.get("p99_seconds")
            if base.get("p50_seconds"):
                entry["p50_vs_baseline"] = p50 / base["p50_seconds"]
            if base.get("p99_seconds"):
                entry["p99_vs_baseline"] = p99 / base["p99_seconds"]
        histograms[key] = entry
    return {"histograms": histograms, "epp_restarted": restarted}


def _outcome_deltas(before_labeled, after_labeled):
    """{outcome: delta} for FLOW_CONTROL_REQUESTS_TOTAL summed over its other
    labels, or None when the family is in neither snapshot. Once the family is
    present, an outcome absent from both snapshots is 0 -- Prometheus only
    materializes a label set on its first increment, so absent means it never
    happened."""
    b_lines = before_labeled.get(FLOW_CONTROL_REQUESTS_TOTAL)
    a_lines = after_labeled.get(FLOW_CONTROL_REQUESTS_TOTAL)
    if not b_lines and not a_lines:
        return None, False

    def by_outcome(lines):
        out = {}
        for labels, value in lines or []:
            o = labels.get("outcome", "")
            out[o] = out.get(o, 0.0) + value
        return out

    b, a = by_outcome(b_lines), by_outcome(a_lines)
    deltas, restarted = {}, False
    for o in set(a) | set(b):
        d = a.get(o, 0.0) - b.get(o, 0.0)
        if d < 0:
            restarted = True
            d = 0.0
        deltas[o] = d
    return deltas, restarted


def compute_shed(offered_groups, loadgen_rows, weights, before_labeled, after_labeled):
    """Per offered group: how many of its requests came back 429/503 and how
    its share of all shed requests compares with its share of the configured
    weight. No PASS/FAIL here -- what "shed fairly" means differs per edge
    case (UNI-157 E3 vs UNI-158 E4's Kuadrant 429), so the consumers judge it.

    Per-group shed comes from the client's own status tally because the live
    EPP exposes no fairness_id-labelled shed counter (flow_control_requests_
    total has outcome but no fairness_id). The EPP's pool-wide outcome counts
    are reported alongside as a cross-check: client 429s beyond the EPP's own
    429-producing outcomes did not come from the EPP (e.g. Kuadrant)."""
    weight_total = sum(weights.get(g) or 0.0 for g in offered_groups)
    rows = []
    for g in offered_groups:
        gen = loadgen_rows.get(g)
        w = weights.get(g)
        weight_share = 100.0 * w / weight_total if w is not None and weight_total > 0 else None
        if gen is None:
            rows.append({"group": g, "state": "not_recorded", "requests_total": None,
                         "status_429": None, "status_503": None, "shed": None,
                         "shed_rate_pct": None, "weight_share_pct": weight_share,
                         "shed_share_pct": None, "shed_share_vs_weight_share": None})
            continue
        st = gen.get("statuses", {})
        s429, s503 = st.get("429", 0), st.get("503", 0)
        shed = s429 + s503
        total = gen.get("total", 0)
        rows.append({"group": g, "state": "shed" if shed > 0 else "never_shed",
                     "requests_total": total, "status_429": s429, "status_503": s503,
                     "shed": shed, "shed_rate_pct": 100.0 * shed / total if total > 0 else None,
                     "weight_share_pct": weight_share,
                     "shed_share_pct": None, "shed_share_vs_weight_share": None})
    shed_total = sum(r["shed"] for r in rows if r["shed"] is not None)
    for r in rows:
        if r["shed"] is not None and shed_total > 0:
            r["shed_share_pct"] = 100.0 * r["shed"] / shed_total
            if r["weight_share_pct"]:
                r["shed_share_vs_weight_share"] = r["shed_share_pct"] / r["weight_share_pct"]

    outcomes, restarted = _outcome_deltas(before_labeled, after_labeled)
    client_429 = sum(r["status_429"] for r in rows if r["status_429"] is not None)
    epp = {"state": "not_recorded", "outcome_deltas": None, "epp_shed_total": None,
           "epp_429_upper_bound": None, "client_429_total": client_429,
           "non_epp_429_lower_bound": None, "epp_restarted": restarted}
    if outcomes is not None:
        epp_shed = sum(outcomes.get(o, 0.0) for o in EPP_SHED_OUTCOMES)
        epp_429 = sum(outcomes.get(o, 0.0) for o in EPP_429_OUTCOMES)
        epp.update({"state": "ok", "outcome_deltas": dict(sorted(outcomes.items())),
                    "epp_shed_total": epp_shed, "epp_429_upper_bound": epp_429,
                    "non_epp_429_lower_bound": max(0.0, client_429 - epp_429)})
    return {"shed_statuses": list(SHED_STATUSES), "total_shed": shed_total,
            "rows": rows, "epp_pool_wide": epp}


ALERT_RULE_LINE = re.compile(r'^\s*-\s*alert:\s*(\S+)\s*$')


def parse_alert_rule_names(path):
    """Alert names in a PrometheusRule manifest (deploy/prometheusrule.yaml),
    in file order. Line-matched rather than YAML-parsed: this file must keep
    running with nothing beyond the standard library."""
    names = []
    with open(path) as f:
        for line in f:
            m = ALERT_RULE_LINE.match(line)
            if m and m.group(1) not in names:
                names.append(m.group(1))
    return names


def _iso_to_epoch(ts):
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()
    except (TypeError, ValueError):
        return None


def compute_alerts(alerts_path, rule_names, run_start, run_end, step_seconds):
    """Fire/clear episodes from a Prometheus range query over the ALERTS
    series, relative to run start.

    `alerts_path` is either the raw /api/v1/query_range response, or that
    response's data.result list wrapped as {"result": [...], "end": <epoch>,
    "step_seconds": <s>, "query": "..."}; the wrapper fields are optional and
    override --alerts-step-seconds and the export end. ALERTS emits one sample
    per evaluation while an alert is pending or firing and nothing once it
    resolves, so an episode is a run of samples no more than 1.5 steps apart;
    it cleared one step after its last sample, unless that sample is the
    export's last one, in which case it was still firing when the export
    ended and no clear time exists.

    `rule_names` (from --alert-rules) lists every alert the run could have
    seen; one that has no sample anywhere in the export gets a "never_fired"
    row, so a run with no alerts says so instead of printing an empty table."""
    with open(alerts_path) as f:
        doc = json.load(f)
    if isinstance(doc, dict) and isinstance(doc.get("data"), dict):
        result = doc["data"].get("result", [])
        export_end, step, query = None, step_seconds, None
    else:
        result = doc.get("result", []) if isinstance(doc, dict) else doc
        export_end = doc.get("end") if isinstance(doc, dict) else None
        step = (doc.get("step_seconds") if isinstance(doc, dict) else None) or step_seconds
        query = doc.get("query") if isinstance(doc, dict) else None
    step = float(step)
    t0 = _iso_to_epoch(run_start)
    t1 = _iso_to_epoch(run_end)
    last_sample = max((float(v[0]) for s in result for v in s.get("values", [])), default=None)
    end = float(export_end) if export_end is not None else last_sample

    def rel(t):
        return None if t is None or t0 is None else t - t0

    episodes = []
    for s in result:
        metric = dict(s.get("metric", {}))
        name = metric.pop("alertname", None)
        state = metric.pop("alertstate", None)
        metric.pop("__name__", None)
        ts = sorted(float(v[0]) for v in s.get("values", []))
        start = prev = None
        runs = []
        for t in ts:
            if start is None:
                start = prev = t
            elif t - prev > 1.5 * step:
                runs.append((start, prev))
                start = prev = t
            else:
                prev = t
        if start is not None:
            runs.append((start, prev))
        for a, b in runs:
            still = end is not None and b >= end - 1e-9
            cleared = None if still else b + step
            episodes.append({
                "alertname": name, "alertstate": state, "labels": metric,
                "started_epoch": a, "cleared_epoch": cleared,
                "started_s": rel(a), "cleared_s": rel(cleared),
                "duration_s": (cleared - a) if cleared is not None else None,
                "still_active_at_export_end": still,
                "started_after_run_end": t1 is not None and a > t1,
            })
    episodes.sort(key=lambda e: (e["started_epoch"], e["alertname"] or "", e["alertstate"] or ""))

    seen = {e["alertname"] for e in episodes}
    fired = {e["alertname"] for e in episodes if e["alertstate"] == "firing"}
    summary = []
    for name in list(rule_names or []) + sorted(n for n in seen if n not in (rule_names or [])):
        if name in fired:
            status = "fired"
        elif name in seen:
            status = "pending_only"
        else:
            status = "never_fired"
        summary.append({"alertname": name, "status": status,
                        "in_rule_file": name in (rule_names or [])})
    return {"query": query, "step_seconds": step, "export_end_epoch": end,
            "run_start_epoch": t0, "episodes": episodes, "summary": summary}


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
    for g in list(GROUPS) + [g for g in offered_groups if g not in GROUPS]:
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
                  window_seconds=10.0,
                  client_record_jsonl_path=None,
                  input_token_weight=1.0, output_token_weight=1.0,
                  cached_input_token_weight=1.0, ledger_tolerance_pct=10.0,
                  pick_latency_baseline_path=None,
                  alerts_path=None, alert_rules_path=None, alerts_step_seconds=30.0):
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
    # UNI-138 (G2): the EPP's core, un-gated, un-weighted token histograms
    # (pkg/epp/handlers/response.go -- observed only from a real response
    # Usage block, same source the fairness plugin's own true-up reads, but
    # NOT contention-gated and NOT run through the cost formula). Missing
    # entirely from a snapshot taken by a benchmark script that predates
    # UNI-138 (it only scraped the `llm_d_epp_maas_fairness_` prefix) --
    # every delta below comes back None in that case, same as any other
    # metric this report reads defensively via .get().
    input_tokens_before = before.get("llm_d_epp_request_input_tokens_sum", {})
    input_tokens_after = after.get("llm_d_epp_request_input_tokens_sum", {})
    output_tokens_before = before.get("llm_d_epp_request_output_tokens_sum", {})
    output_tokens_after = after.get("llm_d_epp_request_output_tokens_sum", {})
    cached_tokens_before = before.get("llm_d_epp_request_cached_tokens_sum", {})
    cached_tokens_after = after.get("llm_d_epp_request_cached_tokens_sum", {})

    all_group_ids = sorted(
        g for g in set(weight_before) | set(weight_after) | set(offered_workers)
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

    # UNI-138 (G2): same before/after delta mechanism as the three series
    # above, for the core un-gated token histograms. A restart detected here
    # folds into the same epp_restarted flag -- it invalidates every delta in
    # this report equally, not just the ledger section.
    input_tokens_deltas, _restarted_in = _counter_deltas(input_tokens_before, input_tokens_after, all_group_ids)
    output_tokens_deltas, _restarted_out = _counter_deltas(output_tokens_before, output_tokens_after, all_group_ids)
    cached_tokens_deltas, _restarted_cached = _counter_deltas(cached_tokens_before, cached_tokens_after, all_group_ids)
    if _restarted_in or _restarted_out or _restarted_cached:
        epp_restarted = True

    offered_groups = [g for g in offered_workers if offered_workers[g] > 0]
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
    # UNI-146 (C1): the same share question as expected_pct/observed_pct
    # above, but against the client's own request COUNT instead of the EPP's
    # weighted-token accounting -- every scenario before this ticket used
    # uniform requests, where the two splits are identical by construction
    # and this number would add nothing. It is reported for comparison only;
    # the scored verdict below is the weighted-token split, never this one.
    offered_requests_total = sum(
        loadgen_rows.get(g, {"total": 0}).get("total", 0) for g in offered_groups
    )

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
        request_share_pct = None
        request_share_deviation_pts = None
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
            # UNI-146 (C1): same expected_pct target, but against this
            # group's share of total REQUEST COUNT rather than weighted
            # tokens -- informational only, never fed into
            # deviations_for_verdict/the scored verdict below. A scenario
            # with asymmetric per-request cost (long-vs-short prompt/output)
            # is exactly where this is expected to diverge from
            # observed_share_pct; a scenario with uniform requests should
            # show the two numbers agree.
            requests_for_pct = loadgen_rows.get(gid, {"total": 0}).get("total", 0)
            if offered_requests_total > 0:
                request_share_pct = 100.0 * requests_for_pct / offered_requests_total
            else:
                request_share_pct = 0.0
            if expected_pct is not None:
                request_share_deviation_pts = request_share_pct - expected_pct

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
            "request_share_pct": request_share_pct,
            "request_share_deviation_pts": request_share_deviation_pts,
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

    # UNI-138 (G2): purely additive, like the timeline section above -- never
    # reads or writes `verdict`. This checks a different invariant (does the
    # EPP's accounting agree with what the client actually sent/received?),
    # not the weighted-split SLI the main verdict already covers, so it gets
    # its own `ledger.verdict` rather than folding into or overriding the
    # top-level one.
    ledger_section = None
    if client_record_jsonl_path:
        client_records = parse_client_record(client_record_jsonl_path)
        ledger_rows = []
        ledger_reasons = []
        ledger_ok = True
        for gid in offered_groups:
            rec = client_records.get(gid)
            epp_in = input_tokens_deltas.get(gid)
            epp_out = output_tokens_deltas.get(gid)
            epp_cached = cached_tokens_deltas.get(gid)
            contended_cost = deltas.get(gid)
            if rec is None:
                ledger_ok = False
                ledger_reasons.append(
                    f"{gid} was offered load but has no client-side record "
                    "(client-request-summary.jsonl is missing its line)"
                )
                ledger_rows.append({
                    "group": gid,
                    "client_prompt_tokens": None, "client_completion_tokens": None,
                    "client_requests_sent": None, "client_aborts": None, "client_errors": None,
                    "epp_total_input_tokens_delta": epp_in, "epp_total_output_tokens_delta": epp_out,
                    "epp_total_cached_tokens_delta": epp_cached, "epp_total_raw_tokens_delta": None,
                    "raw_tokens_pct_diff": None, "epp_contended_cost_delta": contended_cost,
                    "expected_cost_from_client": None, "cost_pct_diff": None, "within_tolerance": None,
                })
                continue

            client_prompt = rec.get("prompt_tokens_total", 0)
            client_completion = rec.get("completion_tokens_total", 0)
            client_raw_total = client_prompt + client_completion
            epp_raw_total = (epp_in + epp_out) if (epp_in is not None and epp_out is not None) else None
            raw_pct_diff = (
                100.0 * (epp_raw_total - client_raw_total) / client_raw_total
                if epp_raw_total is not None and client_raw_total > 0 else None
            )

            # The client cannot see cache hits, so the EPP's own (measured,
            # not estimated) cached-token delta stands in for that term --
            # clamped to the client's prompt total defensively, the same
            # direction cost.go's own cf>pf guard takes.
            cached_for_cost = min(epp_cached, client_prompt) if epp_cached is not None else 0.0
            expected_cost = (
                input_token_weight * (client_prompt - cached_for_cost)
                + cached_input_token_weight * cached_for_cost
                + output_token_weight * client_completion
            )
            cost_pct_diff = (
                100.0 * (contended_cost - expected_cost) / expected_cost
                if contended_cost is not None and expected_cost > 0 else None
            )

            within = (
                raw_pct_diff is not None and abs(raw_pct_diff) <= ledger_tolerance_pct
                and cost_pct_diff is not None and abs(cost_pct_diff) <= ledger_tolerance_pct
            )
            if not within:
                ledger_ok = False
                detail = []
                if raw_pct_diff is None or abs(raw_pct_diff) > ledger_tolerance_pct:
                    detail.append(f"raw tokens {'n/a' if raw_pct_diff is None else f'{raw_pct_diff:+.1f}%'}")
                if cost_pct_diff is None or abs(cost_pct_diff) > ledger_tolerance_pct:
                    detail.append(f"cost {'n/a' if cost_pct_diff is None else f'{cost_pct_diff:+.1f}%'}")
                ledger_reasons.append(
                    f"{gid} exceeded the {ledger_tolerance_pct:g}% ledger tolerance: " + ", ".join(detail)
                )

            ledger_rows.append({
                "group": gid,
                "client_prompt_tokens": client_prompt,
                "client_completion_tokens": client_completion,
                "client_requests_sent": rec.get("requests_sent"),
                "client_aborts": rec.get("aborts"),
                "client_errors": rec.get("errors"),
                "epp_total_input_tokens_delta": epp_in,
                "epp_total_output_tokens_delta": epp_out,
                "epp_total_cached_tokens_delta": epp_cached,
                "epp_total_raw_tokens_delta": epp_raw_total,
                "raw_tokens_pct_diff": raw_pct_diff,
                "epp_contended_cost_delta": contended_cost,
                "expected_cost_from_client": expected_cost,
                "cost_pct_diff": cost_pct_diff,
                "within_tolerance": within,
            })

        ledger_section = {
            "tolerance_pct": ledger_tolerance_pct,
            "cost_model": {
                "input_token_weight": input_token_weight,
                "output_token_weight": output_token_weight,
                "cached_input_token_weight": cached_input_token_weight,
            },
            "rows": ledger_rows,
            "verdict": {
                "result": "PASS" if ledger_ok else "FAIL",
                "reasons": ledger_reasons,
            },
        }

    # UNI-181: purely additive, like timeline/ledger above -- never reads or
    # writes `verdict`, and adds no key to `groups`/`sources`, so every field
    # a pre-UNI-181 report had is unchanged. Shed is always computed (its
    # input, the loadgen status tally, is already required); pick latency
    # reads the same before/after snapshots; alerts need --alerts-json.
    before_labeled = parse_metrics_labeled(metrics_before_path)
    after_labeled = parse_metrics_labeled(metrics_after_path)
    weights_for_shed = {g: (weight_after.get(g) if weight_after.get(g) is not None else weight_before.get(g))
                        for g in offered_groups}
    shed_section = compute_shed(offered_groups, loadgen_rows, weights_for_shed, before_labeled, after_labeled)
    baseline_pick = None
    if pick_latency_baseline_path:
        with open(pick_latency_baseline_path) as f:
            baseline_pick = json.load(f).get("pick_latency")
    pick_latency_section = compute_pick_latency(before_labeled, after_labeled, baseline_pick)
    pick_latency_section["baseline_report"] = pick_latency_baseline_path
    pick_latency_section["baseline_has_pick_latency"] = (
        None if not pick_latency_baseline_path else baseline_pick is not None
    )
    alerts_section = None
    if alerts_path:
        rule_names = parse_alert_rule_names(alert_rules_path) if alert_rules_path else []
        alerts_section = compute_alerts(alerts_path, rule_names, run_start, run_end, alerts_step_seconds)
        alerts_section["rule_file"] = alert_rules_path

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
            "request_share_pct": (
                "UNI-146 (C1): the SAME expected_share target above, scored against "
                "requests_total (plain request count, from the loadgen log) instead of "
                "delivered weighted tokens -- informational only, never part of the verdict. "
                "Equal to observed_share_pct when every offered group's requests are uniform "
                "cost (every scenario before this ticket); expected to diverge when request "
                "cost is asymmetric across groups."
            ),
        },
        "timeline": timeline_section,
        "ledger": ledger_section,
        "shed": shed_section,
        "pick_latency": pick_latency_section,
        "alerts": alerts_section,
    }
    return report


def _render_uni181_sections(report):
    """Shed / pick latency / alerts. Every empty case says which kind of
    empty it is -- never happened vs. not recorded -- instead of a blank."""
    def fmt(v, suffix="", spec=".1f"):
        return "n/a" if v is None else f"{v:{spec}}{suffix}" if isinstance(v, float) else f"{v}{suffix}"

    lines = [""]
    lines.append("## Shed rate vs weight (UNI-181)")
    lines.append("")
    s = report.get("shed")
    if not s:
        lines.append("N/A: report predates UNI-181.")
    else:
        lines.append(
            f"Shed = client-observed HTTP {'/'.join(s['shed_statuses'])}. Weight share is over offered "
            "groups. Shed share / weight share above 1 means the group lost more of the shed than "
            "its weight; no PASS/FAIL is applied here."
        )
        lines.append("")
        if not s["rows"]:
            lines.append("No group was offered load, so there is nothing to shed.")
        else:
            lines.append("| group | requests | 429 | 503 | shed | shed rate % | weight share % | "
                         "shed share % | shed share / weight share |")
            lines.append("|---|---|---|---|---|---|---|---|---|")
            for r in s["rows"]:
                if r["state"] == "not_recorded":
                    lines.append(f"| {r['group']} | not recorded (no loadgen row) | n/a | n/a | n/a | n/a | "
                                 f"{fmt(r['weight_share_pct'], '%')} | n/a | n/a |")
                    continue
                shed = "0 (never shed)" if r["state"] == "never_shed" else str(r["shed"])
                share = fmt(r["shed_share_pct"], "%") if s["total_shed"] > 0 else "n/a (nothing shed)"
                ratio = fmt(r["shed_share_vs_weight_share"], "", ".2f") if s["total_shed"] > 0 else "n/a (nothing shed)"
                lines.append(
                    f"| {r['group']} | {r['requests_total']} | {r['status_429']} | {r['status_503']} | "
                    f"{shed} | {fmt(r['shed_rate_pct'], '%', '.2f')} | {fmt(r['weight_share_pct'], '%')} | "
                    f"{share} | {ratio} |"
                )
        lines.append("")
        e = s["epp_pool_wide"]
        if e["state"] == "not_recorded":
            lines.append(f"**EPP-side shed (pool-wide):** not recorded -- `{FLOW_CONTROL_REQUESTS_TOTAL}` is "
                         "absent from both snapshots, so whether the EPP or something in front of it "
                         "(Kuadrant) produced the client's 429s is unknown.")
        else:
            nonzero = ", ".join(f"{o}={v:g}" for o, v in e["outcome_deltas"].items() if v) or "no outcomes moved"
            lines.append(
                f"**EPP-side shed (pool-wide, no per-group label exists):** {e['epp_shed_total']:g} "
                f"requests refused by the EPP ({nonzero}). Client saw {e['client_429_total']} x 429; at "
                f"most {e['epp_429_upper_bound']:g} came from the EPP, so at least "
                f"{e['non_epp_429_lower_bound']:g} came from elsewhere (e.g. Kuadrant)."
                + (" EPP counter went backwards: restart mid-run, figures unreliable." if e["epp_restarted"] else "")
            )

    lines.append("")
    lines.append("## EPP pick latency (UNI-181)")
    lines.append("")
    p = report.get("pick_latency")
    if not p:
        lines.append("N/A: report predates UNI-181.")
    else:
        if p.get("baseline_report"):
            lines.append(f"Baseline: `{p['baseline_report']}`" +
                         ("" if p.get("baseline_has_pick_latency") else " (has no pick_latency section)"))
            lines.append("")
        lines.append("| histogram | state | observations | p50 | p99 | p50 bucket | p99 bucket | "
                     "p50 vs baseline | p99 vs baseline |")
        lines.append("|---|---|---|---|---|---|---|---|---|")

        def ms(v):
            return "n/a" if v is None else f"{v * 1000:.3f}ms"

        def bucket(b):
            if not b:
                return "n/a"
            lo, hi = (x if x == "+Inf" else f"{x * 1000:g}" for x in b)
            return f"({lo}, {hi}]ms"

        for key, h in p["histograms"].items():
            state = {
                "not_recorded": "not recorded (absent from both snapshots)",
                "no_observations": "no picks during the run",
            }.get(h["state"], "ok")
            p99 = ms(h["p99_seconds"])
            if h.get("p99_at_histogram_ceiling"):
                p99 = f">= {p99} (above top bucket)"
            lines.append(
                f"| `{key}` | {state} | {fmt(h['observations'], '', '.0f')} | {ms(h['p50_seconds'])} | {p99} | "
                f"{bucket(h['p50_bucket'])} | {bucket(h['p99_bucket'])} | "
                f"{fmt(h['p50_vs_baseline'], 'x', '.2f')} | {fmt(h['p99_vs_baseline'], 'x', '.2f')} |"
            )
        lines.append("")
        lines.append("Quantiles interpolate linearly inside a bucket (Prometheus `histogram_quantile`); "
                     "the bucket bounds are the real precision.")
        if p.get("epp_restarted"):
            lines.append("")
            lines.append("A histogram bucket went backwards between snapshots (EPP restart): quantiles "
                         "use the post-restart histogram only.")

    lines.append("")
    lines.append("## Alerts (UNI-181)")
    lines.append("")
    a = report.get("alerts")
    if not a:
        lines.append("Not recorded: no `--alerts-json` was supplied, so whether any alert fired during "
                     "this run is unknown (not \"none fired\").")
    else:
        lines.append(f"Source: ALERTS range export, step {a['step_seconds']:g}s"
                     + (f", rules from `{a['rule_file']}`" if a.get("rule_file") else "")
                     + (f", query `{a['query']}`" if a.get("query") else "") + ".")
        lines.append("")
        if not a["summary"]:
            lines.append("No alert appeared in the export, and no rule file was given to list "
                         "the alerts that could have fired.")
        else:
            label = {"fired": "fired", "pending_only": "pending, never fired", "never_fired": "never fired"}
            for row in a["summary"]:
                extra = "" if row["in_rule_file"] or not a.get("rule_file") else " (not in rule file)"
                lines.append(f"- {row['alertname']}: {label[row['status']]}{extra}")
        if a["episodes"]:
            lines.append("")
            lines.append("| alert | state | labels | started (s from run start) | cleared (s) | duration (s) |")
            lines.append("|---|---|---|---|---|---|")
            for ep in a["episodes"]:
                labels = ", ".join(f"{k}={v}" for k, v in sorted(ep["labels"].items())) or "-"
                cleared = ("still active at export end" if ep["still_active_at_export_end"]
                           else fmt(ep["cleared_s"]))
                started = fmt(ep["started_s"]) + (" (after run end)" if ep["started_after_run_end"] else "")
                lines.append(f"| {ep['alertname']} | {ep['alertstate']} | {labels} | {started} | "
                             f"{cleared} | {fmt(ep['duration_s'])} |")
    return lines


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
    lines.append(
        "`observed %`/`deviation (pts)` are the scored split, by weighted "
        "tokens (`contended_service_tokens_total`). `request-count %`/"
        "`request-count deviation (pts)` (UNI-146) are the same expected-"
        "share target scored against plain request COUNT instead -- "
        "informational only, never part of the verdict below. The two agree "
        "when every offered group sends uniform requests (every scenario "
        "before UNI-146) and are expected to diverge whenever request cost "
        "is asymmetric across groups (e.g. long-prompt/short-output vs. "
        "short-prompt/long-output)."
    )
    lines.append("")
    offered_col = "offered req/s" if r.get("generator") == "open-loop" else "offered workers"
    lines.append(
        f"| group | weight | {offered_col} | requests | statuses | p50s | p95s | "
        "delivered tokens | expected % | observed % | deviation (pts) | "
        "request-count % | request-count deviation (pts) | contended_seconds | "
        "cached ratio | dispatch_total |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
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
            f"{fmt(g['request_share_pct'], '%')} | {fmt(g['request_share_deviation_pts'])} | "
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
    lines.append("## Ledger cross-check (UNI-138/G2)")
    lines.append("")
    l = report.get("ledger")
    if not l:
        lines.append("N/A: no `--client-record-jsonl` recorded for this run (older report, or the "
                      "benchmark script predates UNI-138).")
    else:
        cm = l["cost_model"]
        lines.append(
            f"**Ledger verdict: {l['verdict']['result']}** (tolerance: {l['tolerance_pct']:g}%, "
            f"cost model: input={cm['input_token_weight']:g} output={cm['output_token_weight']:g} "
            f"cached={cm['cached_input_token_weight']:g})"
        )
        if l["verdict"]["reasons"]:
            lines.append("")
            for reason in l["verdict"]["reasons"]:
                lines.append(f"- {reason}")
        lines.append("")
        lines.append(
            "| group | client prompt tok | client completion tok | EPP raw tokens (in+out) | "
            "raw diff % | EPP contended cost | expected cost (from client) | cost diff % | "
            "within tolerance |"
        )
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for row in l["rows"]:
            def lfmt(v, suffix=""):
                return "n/a" if v is None else f"{v:.1f}{suffix}" if isinstance(v, float) else f"{v}{suffix}"
            lines.append(
                f"| {row['group']} | {lfmt(row['client_prompt_tokens'])} | "
                f"{lfmt(row['client_completion_tokens'])} | {lfmt(row['epp_total_raw_tokens_delta'])} | "
                f"{lfmt(row['raw_tokens_pct_diff'], '%')} | {lfmt(row['epp_contended_cost_delta'])} | "
                f"{lfmt(row['expected_cost_from_client'])} | {lfmt(row['cost_pct_diff'], '%')} | "
                f"{row['within_tolerance']} |"
            )
    lines.extend(_render_uni181_sections(report))
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
    p.add_argument(
        "--client-record-jsonl", default=None,
        help="UNI-138 (G2): path to client-request-summary.jsonl (deploy/poc/15-fairness-"
             "benchmark.sh's pull of 04-loadgen.yaml's CLIENT_RECORD_JSON lines). Omit to get "
             "a report with no 'ledger' section -- the pre-UNI-138 shape.",
    )
    p.add_argument(
        "--input-token-weight", type=float, default=1.0,
        help="UNI-138 (G2): live EPP ConfigMap's inputTokenWeight -- no metric exposes this, "
             "so the caller must read it from maas-epp-config and pass it through.",
    )
    p.add_argument("--output-token-weight", type=float, default=1.0)
    p.add_argument("--cached-input-token-weight", type=float, default=1.0)
    p.add_argument(
        "--ledger-tolerance-pct", type=float, default=10.0,
        help="UNI-138 (G2): max absolute percent difference between the EPP's accounting and "
             "the client-recorded ledger before a group fails the ledger cross-check.",
    )
    p.add_argument(
        "--pick-latency-baseline", default=None,
        help="UNI-181: a previous run's fairness-report.json (the 3-group full-contention run is "
             "the reference) to express this run's EPP pick latency p50/p99 against.",
    )
    p.add_argument(
        "--alerts-json", default=None,
        help="UNI-181: Prometheus /api/v1/query_range export of the ALERTS series covering the "
             "run (raw response, or {\"result\": [...], \"end\": epoch, \"step_seconds\": s}). "
             "Omit and the report says alert state is unknown for this run.",
    )
    p.add_argument(
        "--alert-rules", default=None,
        help="UNI-181: PrometheusRule manifest (deploy/prometheusrule.yaml) whose alert names "
             "get an explicit 'never fired' row when absent from --alerts-json.",
    )
    p.add_argument(
        "--alerts-step-seconds", type=float, default=30.0,
        help="UNI-181: the query_range step used for --alerts-json (ignored if the file carries "
             "its own step_seconds). Samples more than 1.5 steps apart start a new episode.",
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
        metrics_timeseries_path=args.metrics_timeseries,
        timeline_config_path=args.timeline_config,
        window_seconds=args.window_seconds,
        client_record_jsonl_path=args.client_record_jsonl,
        input_token_weight=args.input_token_weight,
        output_token_weight=args.output_token_weight,
        cached_input_token_weight=args.cached_input_token_weight,
        ledger_tolerance_pct=args.ledger_tolerance_pct,
        pick_latency_baseline_path=args.pick_latency_baseline,
        alerts_path=args.alerts_json,
        alert_rules_path=args.alert_rules,
        alerts_step_seconds=args.alerts_step_seconds,
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
