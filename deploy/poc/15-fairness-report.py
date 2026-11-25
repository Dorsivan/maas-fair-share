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

UNI-222 (B4, "long idle return"): the "expected share" above is still a flat
ratio applied uniformly across the run's *entire* duration, which silently
assumes every offered group was present the whole time. For a group with a
declared join/leave offset or duty cycle (--timeline-config, below), that
assumption is wrong for whatever fraction of the run it was absent --
scoring the group's whole-run average against a target it was never even
offered for double-penalizes an idle-then-return scenario for the idle
period itself, on top of whatever its actual return behaviour earns or
loses it. When --metrics-timeseries is also given,
schedule_aware_whole_run_shares replaces the flat ratio for exactly the
groups affected by a non-trivial schedule with a time-weighted entitlement
built from the same per-window renormalization UNI-127's `timeline` section
below already computes (see docs/design.md "Whole-run scoring with a
declared schedule" for the full writeup and a worked example). A scenario
with no declared schedule, or where every offered group is active for the
whole run, is completely unaffected -- the two formulas are mathematically
identical in that case.

UNI-127 adds a second layer on top of the above -- mostly additive (it never
changes `verdict` on its own), but see the UNI-222 paragraph just above for
the one way `windows` now feeds back into it. It always adds a `timeline`
section:

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

UNI-225 adds one more per-group number and a verdict-level flag, computed
purely from numbers this report already has -- no new input, no new cluster
access. Most of this benchmark's scenarios size each offered group's workers
(or, for the open-loop generator, its offered rate) to track its configured
weight as closely as possible, on purpose: that is how a group is made to
genuinely over-offer its own entitlement without accidentally under-offering
the pool as a whole (see docs/runbook.md "Per-tenant worker sizing and the
saturation check"). The side effect is that on those rows, "the split follows
the configured weights" and "the split just follows how many workers each
group happened to run" predict the identical number -- a PASS there confirms
the policy did not BREAK, but is not evidence that it is weights, specifically,
doing the enforcing. `worker_share_pct` is each offered group's share of the
total OFFERED worker count/rate (same denominator convention as
`expected_share_pct` above: offered groups only, excluding `solo` and any
`capped_groups`), so it is directly comparable to `expected_share_pct`.
`worker_vs_weight_gap_pts` is `worker_share_pct - expected_share_pct` per
group; the verdict's `max_worker_vs_weight_gap_points` is the largest absolute
value of that across the run's groups. When that gap stays under
`threshold_points` -- the same bar the weighted-split deviation check itself
uses -- the run cannot distinguish the two hypotheses, and `verdict.
discriminating` is set to `False` (`render_markdown` prints this as a
**(NON-DISCRIMINATING)** qualifier next to the verdict, in the same spirit as
the UNCONTENDED carve-out above). `discriminating` is left `None` for a
`solo`, `control`, UNCONTENDED, or demand-capped run, the same four cases
already excluded from the symmetric deviation check -- there is no weights-
vs-workers question to ask about a run that never reaches that check in the
first place.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

METRIC_LINE = re.compile(r'^([^{\s]+)(?:\{(.*)\})?\s+([^\s]+)$')
LABEL = re.compile(r'(\w+)="((?:[^"\\]|\\.)*)"')
# UNI-305: the workers field is read as whatever group=N pairs it carries.
# 04-loadgen.yaml's run.sh always writes app1/app2/end-users/custom there (its
# built-ins; app3..appN come from GROUPS_LINE below), 12-loadgen-route.sh
# writes its manifest's groups. "custom" is skipped, never captured (UNI-129:
# its fairness id is whatever its arbitrary subscription classifies to).
TENANTS_LINE = re.compile(
    r'load: (?:GW=\S+ )?tenants=\[(?P<tenants>.*?)\] '  # GW=: 12-loadgen-route.sh's form
    r'workers (?P<workers>(?:[a-z0-9-]+=\d+ )+)'
    r'duration=(?P<duration>\d+)s'
)
WORKERS_PAIR = re.compile(r'(?P<name>[a-z0-9-]+)=(?P<n>[\d.]+)')
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
# UNI-305: one group=rate/s pair per tenant the generator was given --
# app1/app2/end-users for every run before it, any manifest's groups after.
OPEN_LOOP_TENANTS_LINE = re.compile(
    r'load: open-loop Poisson arrivals rate (?P<rates>(?:[a-z0-9-]+=[\d.]+/s )+)'
    r'duration=(?P<duration>[\d.]+)s'
)
OPEN_LOOP_ROW = re.compile(
    r'^(?P<group>\S+)\s+sent=(?P<sent>\d+)\s+completion_tokens=(?P<tok>-?\d+)\s+'
    r'p50=(?P<p50>[\d.]+)s\s+p95=(?P<p95>[\d.]+)s\s+p99=(?P<p99>[\d.]+)s\s+codes=\[(?P<codes>.*)\]$'
)


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
# UNI-230: 15-fairness-benchmark.sh's snapshot_metrics() emits this as the
# first line of its own output, ahead of the grepped metric lines, so a
# connection-level scrape failure (curl exit != 0) can be told apart from a
# real EPP restart even though both leave zero metric lines in the block --
# see that function's own comment for why the distinction isn't otherwise
# recoverable after the fact. Absent entirely in files captured before this
# change; treated as a successful scrape for backward compatibility.
SCRAPE_EXIT = re.compile(r'^#\s*scrape_exit=(?P<rc>\d+)\s*$')


def _split_timeseries_blocks(text):
    """A sequence of (epoch_seconds: float, iso_ts: str, block_text: str,
    scrape_failed: bool) from deploy/poc/15-fairness-benchmark.sh's
    metrics-timeseries.txt: blocks of Prometheus text, each preceded by a
    '# ts=<iso> epoch=<unix seconds>' header. Returns entries sorted by epoch
    (they are written in order, but a clock that is not monotonic -- NTP
    step, not a backend restart -- would otherwise silently produce a
    negative-duration window). `scrape_failed` is True only when the block's
    own `# scrape_exit=` marker (see SCRAPE_EXIT) is present and nonzero --
    never inferred from the block being empty, since a real restart produces
    an equally empty block."""
    entries = []
    epoch = None
    ts = None
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
    """A sequence of (epoch_seconds, iso_ts, series, scrape_failed) -- series
    as parse_metrics_text returns it (one value per fairness_id, other labels
    dropped). See _split_timeseries_blocks for the block format and for
    scrape_failed's meaning."""
    text = open(path).read()
    return [(epoch, ts, parse_metrics_text(block), scrape_failed)
            for epoch, ts, block, scrape_failed in _split_timeseries_blocks(text)]


def parse_timeseries_labeled(path):
    """Same blocks as parse_timeseries, but series as parse_metrics_labeled_text
    returns it (every label kept) -- needed for a histogram metric like
    llm_d_epp_flow_control_request_queue_duration_seconds, where collapsing
    to a single fairness_id key per metric would silently overwrite one `le`
    bucket with another."""
    text = open(path).read()
    return [(epoch, ts, parse_metrics_labeled_text(block), scrape_failed)
            for epoch, ts, block, scrape_failed in _split_timeseries_blocks(text)]


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
    offered_workers = {}
    duration = None
    generator = "closed-loop"
    if m:
        tenants = set(m.group('tenants').split())
        for pair in WORKERS_PAIR.finditer(m.group('workers')):
            g = pair.group('name')
            if g != "custom":
                offered_workers[g] = int(pair.group('n')) if g in tenants else 0
        duration = int(m.group('duration'))
        gm = GROUPS_LINE.search(text)
        if gm:
            for entry in GROUPS_ENTRY.finditer(gm.group('groups')):
                name = entry.group('name')
                if name not in offered_workers and name != "custom":
                    offered_workers[name] = int(entry.group('workers'))
    else:
        m = OPEN_LOOP_TENANTS_LINE.search(text)
        if m:
            generator = "open-loop"
            for pair in WORKERS_PAIR.finditer(m.group('rates')):
                rate = float(pair.group('n'))
                offered_workers[pair.group('name')] = rate if rate > 0 else 0
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
            if group not in offered_workers:
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

def parse_metrics_labeled_text(text):
    """{metric_name: [(labels: dict, value: float)]} -- every label kept."""
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


def parse_metrics_labeled(path):
    with open(path) as f:
        return parse_metrics_labeled_text(f.read())


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


def _histogram_buckets(labeled, name, filters=None):
    """{le: cumulative_count} for `name`, summed across any non-`le` labels,
    or None if the histogram has no _bucket line at all in this snapshot.
    `filters`, when given, restricts to lines whose labels match every
    key/value in it (e.g. {"fairness_id": "app1", "outcome": "Dispatched"})
    before summing -- the rest of this function's "sum across any other
    label" behaviour is unchanged for whatever labels are left unfiltered."""
    lines = labeled.get(name + "_bucket")
    if not lines:
        return None
    buckets = {}
    for labels, value in lines:
        if filters and any(labels.get(k) != v for k, v in filters.items()):
            continue
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
        -- the benchmark's snapshot filter did not capture the family (true
        for every run between UNI-181 and UNI-167; snapshot_metrics() did not
        grep scheduler_e2e/plugin_duration at all until UNI-167 added them),
        or the EPP never scheduled anything in its lifetime.
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


def compute_saturation_limb(metrics_timeseries_path, queue_depth_threshold, kv_cache_util_threshold):
    """UNI-224: the utilization-detector saturation gate is a roofline over
    TWO signals, not queue depth alone (llm-d-router@v0.11.0's
    saturationdetector/utilization/detector.go:160):

        qRatio  := average_queue_size  / queueDepthThreshold
        kvRatio := average_kv_cache_utilization / kvCacheUtilThreshold
        totalScore := max(qRatio, kvRatio)

    Neither ratio is exposed directly -- the EPP's own
    llm_d_epp_flow_control_pool_saturation gauge reports only the combined
    totalScore, not which resource produced it. This reconstructs both
    ratios from the two pool-level gauges the EPP already exports
    (llm_d_epp_average_queue_size, llm_d_epp_average_kv_cache_utilization --
    both already covered by snapshot_metrics()'s `average_` prefix match,
    just never surfaced or attributed to a limb before this ticket) and
    reports, for every timeseries sample, which limb was larger -- plus the
    run's peak of each ratio, which is the number that matters for "did this
    run ever threaten the gate." `pool_saturation_reported` is the detector's
    own gauge at the same sample, kept alongside as a cross-check that this
    reconstruction tracks the real gating value (it will not match exactly
    when stalenessPolicy=saturated scores a stale endpoint at 1.0 -- that
    case is surfaced via flow_control_stale_endpoints elsewhere in the report,
    not here).

    Returns None if no timeseries was captured (pre-UNI-224 shape, or a
    caller that omitted --metrics-timeseries)."""
    if not metrics_timeseries_path or not os.path.exists(metrics_timeseries_path):
        return None
    samples = []
    for epoch, ts, series, scrape_failed in parse_timeseries(metrics_timeseries_path):
        if scrape_failed:
            continue
        q = series.get("llm_d_epp_average_queue_size", {}).get(None)
        kv = series.get("llm_d_epp_average_kv_cache_utilization", {}).get(None)
        if q is None and kv is None:
            continue
        q = q or 0.0
        kv = kv or 0.0
        q_ratio = (q / queue_depth_threshold) if queue_depth_threshold else None
        kv_ratio = (kv / kv_cache_util_threshold) if kv_cache_util_threshold else None
        roofline = max(v for v in (q_ratio, kv_ratio) if v is not None) if (q_ratio is not None or kv_ratio is not None) else None
        # Tie (including both zero) attributes to "queue" -- an explicit
        # tie-break reads clearer than an arbitrary float comparison
        # silently picking one, and every run on file ties at zero/zero.
        bound = None
        if q_ratio is not None and kv_ratio is not None:
            bound = "kv_cache" if kv_ratio > q_ratio else "queue"
        samples.append({
            "epoch": epoch, "ts": ts,
            "average_queue_size": q, "average_kv_cache_utilization": kv,
            "queue_ratio": q_ratio, "kv_ratio": kv_ratio,
            "roofline_score": roofline, "bound": bound,
            "pool_saturation_reported": series.get("llm_d_epp_flow_control_pool_saturation", {}).get(None),
        })
    if not samples:
        return {
            "queue_depth_threshold": queue_depth_threshold,
            "kv_cache_util_threshold": kv_cache_util_threshold,
            "state": "no_samples", "samples": [],
        }
    peak_queue_ratio = max(s["queue_ratio"] for s in samples)
    peak_kv_ratio = max(s["kv_ratio"] for s in samples)
    kv_binding_samples = sum(1 for s in samples if s["bound"] == "kv_cache")
    return {
        "queue_depth_threshold": queue_depth_threshold,
        "kv_cache_util_threshold": kv_cache_util_threshold,
        "state": "ok",
        "sample_count": len(samples),
        "peak_queue_ratio": peak_queue_ratio,
        "peak_kv_ratio": peak_kv_ratio,
        "peak_average_kv_cache_utilization": max(s["average_kv_cache_utilization"] for s in samples),
        "peak_average_queue_size": max(s["average_queue_size"] for s in samples),
        "kv_binding_sample_count": kv_binding_samples,
        # The limb that bound AT THIS RUN'S OWN PEAK roofline score, i.e. the
        # one the detector actually gated dispatch on when it mattered most --
        # not which limb won on a plurality of samples, most of which are
        # near-idle between-request gaps.
        "bound_at_peak": max(samples, key=lambda s: s["roofline_score"])["bound"],
        "samples": samples,
    }


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
    # In offered order (the loadgen log's), so a manifest's tenants print in
    # the manifest's order. Was app1/app2/end-users then set order, which
    # shuffled app3..appN between two scorings of the same run.
    for g in offered_groups:
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
    means either the EPP restarted between those two scrapes, or the window's
    closing scrape itself failed outright (UNI-230: a connection-level curl
    failure and a real restart both leave zero matching metric lines in the
    closing snapshot, so the two are only distinguishable via that snapshot's
    own `scrape_failed` flag -- see _split_timeseries_blocks). Either way the
    true delta for this window is unknown, so it is clamped to zero the same
    as before, but only a real restart sets any_restart; a failed scrape sets
    any_scrape_gap instead, so a flaky scrape doesn't get misread as a process
    restart with no corroborating pod/container evidence. Returns (windows,
    any_restart, any_scrape_gap)."""
    if len(timeseries) < 2:
        return [], False, False
    t0 = timeseries[0][0]
    windows = []
    any_restart = False
    any_scrape_gap = False
    for (e0, _, s0, _scrape_failed0), (e1, _, s1, scrape_failed1) in zip(timeseries, timeseries[1:]):
        tok0 = s0.get("llm_d_epp_maas_fairness_contended_service_tokens_total", {})
        tok1 = s1.get("llm_d_epp_maas_fairness_contended_service_tokens_total", {})
        start_s, end_s = e0 - t0, e1 - t0
        mid_s = (start_s + end_s) / 2.0
        deltas = {}
        for gid in schedule:
            b, a = tok0.get(gid, 0.0), tok1.get(gid, 0.0)
            d = a - b
            if d < 0:
                if scrape_failed1:
                    any_scrape_gap = True
                else:
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
    return windows, any_restart, any_scrape_gap


def schedule_has_partial_offering(schedule, run_duration):
    """True if any group in `schedule` is not simply "active for the whole
    run" -- a join/leave offset inside [0, run_duration) or a duty cycle.
    UNI-222's whole-run expected-share gate below only has work to do when
    this is true; when every group's schedule is the default full-run entry,
    schedule_aware_whole_run_shares collapses to the exact same answer as the
    flat weight-ratio formula anyway (see its own docstring), so callers skip
    it there to keep every non-idle/non-join scenario's output byte-identical
    to before this existed."""
    for entry in schedule.values():
        if entry.get("duty_on"):
            return True
        if (entry.get("start") or 0.0) > 0.0:
            return True
        stop = entry.get("stop")
        if stop is not None and stop < run_duration:
            return True
    return False


def schedule_aware_whole_run_shares(windows, offered_groups):
    """UNI-222 (B4, "long idle return"): the flat whole-run `expected_share_pct`
    (each offered group's weight over the sum of every OFFERED group's weight,
    applied uniformly for the run's entire duration) silently assumes every
    offered group was contending the whole time. For a group with a declared
    join/leave or duty-cycle schedule, that assumption is simply false for
    whatever fraction of the run it was absent -- and the project's own
    intentional, documented behaviour during an absence is work conservation:
    an idle group's weight is given to whoever is still asking (see this
    module's "Expected share" docstring above), not held in reserve. Scoring
    that correct behaviour against a target that still expects the absent
    group's full-time share double-penalizes it for being away at all,
    on top of (not instead of) whatever its own return behaviour earns or
    loses it -- exactly what UNI-143/UNI-144 found and flagged in prose
    ("the naive whole-run expected-% assumes full-time offering it never had
    -- not the right number to judge this case by") without ever fixing the
    number itself. docs/design.md "Whole-run scoring with a declared
    schedule" has the full writeup and the worked long-idle example.

    This reuses the exact per-window expected/observed shares
    compute_windows already computes (same renormalization-among-currently-
    active-groups definition, just not fed back into the whole-run verdict
    until now) and aggregates them token-weighted across the run: each
    window's contribution to both the expected and observed numerator, and
    to the shared denominator, is scaled by that window's own total
    delivered tokens among the groups active *in that window* -- so a
    quiet window (little volume) cannot swamp a busy one, and a window
    where every candidate group is between its stop time and the run's
    tail (every group inactive, e.g. draining in-flight requests after a
    shared "stop" offset) contributes to no group's numerator or the
    denominator at all, rather than counting as "zero credit, but still
    judged against a positive target" the way a naive include-everything
    sum would.

    Returns {group: {"expected_share_pct": ..., "observed_share_pct": ...}}
    for every group that accumulated a nonzero denominator; a group entirely
    absent from every window's active set (never actually contended) is
    omitted, same as the flat path leaves it at None via offered_tokens_total
    <= 0. Returns {} if there is nothing to aggregate (no windows, or every
    window's active set is empty/zero-volume) -- callers fall back to the
    flat formula in that case."""
    offered = set(offered_groups)
    exp_num = {}
    obs_num = {}
    denom = 0.0
    for w in windows:
        active_entries = [e for e in w["groups"] if e.get("active") and e["group"] in offered]
        window_active_total = sum((e.get("delivered_tokens") or 0.0) for e in active_entries)
        if window_active_total <= 0:
            continue
        denom += window_active_total
        for e in active_entries:
            gid = e["group"]
            obs_num[gid] = obs_num.get(gid, 0.0) + (e.get("delivered_tokens") or 0.0)
            exp_num[gid] = exp_num.get(gid, 0.0) + (e.get("expected_share_pct") or 0.0) / 100.0 * window_active_total
    if denom <= 0:
        return {}
    return {
        gid: {
            "expected_share_pct": 100.0 * exp_num.get(gid, 0.0) / denom,
            "observed_share_pct": 100.0 * obs_num.get(gid, 0.0) / denom,
        }
        for gid in exp_num
    }


# UNI-164: per-group, per-window queue-wait distribution from the upstream
# llm-d-router Flow Control layer's own histogram (fairness_id-labelled since
# v0.11.0, llm-d-router docs/metrics.md "Flow control") -- already scraped by
# 15-fairness-benchmark.sh's snapshot_metrics (the `^llm_d_epp_flow_control_`
# grep predates this ticket, UNI-193), so this is a report-side-only change:
# no EPP code, no new scrape, no new benchmark-script flag. Restricted to
# outcome="Dispatched" -- a request that was rejected or evicted never
# produced a real "time until served" wait the same way a dispatched one did,
# and mixing the two would conflate shedding (already covered by the Shed
# section) with queueing.
QUEUE_WAIT_HISTOGRAM = "llm_d_epp_flow_control_request_queue_duration_seconds"


def compute_queue_wait_windows(timeseries_labeled, schedule):
    """One row per consecutive pair of labeled time-series snapshots, per
    scheduled group: p50/p90/p99 queue wait (seconds) for requests that
    reached outcome=Dispatched in that window, bucket-diffed the same way
    compute_pick_latency diffs its histograms. A bucket going backwards means
    either the EPP restarted between the two scrapes, or the window's closing
    scrape itself failed outright (UNI-230 -- see compute_windows, the same
    failure mode applies to this histogram); the post-restart/post-gap
    snapshot alone is used for that window either way, same fallback
    compute_pick_latency uses, but only a real restart sets any_restart -- a
    failed scrape sets any_scrape_gap instead. A group with no schedule entry
    (never offered this run) is absent, not zeroed -- the same "never
    happened" vs. "not recorded" distinction every other histogram-backed
    section in this report makes."""
    if len(timeseries_labeled) < 2:
        return [], False, False
    t0 = timeseries_labeled[0][0]
    windows = []
    any_restart = False
    any_scrape_gap = False
    for (e0, _, s0, _scrape_failed0), (e1, _, s1, scrape_failed1) in zip(timeseries_labeled, timeseries_labeled[1:]):
        start_s, end_s = e0 - t0, e1 - t0
        groups = []
        for gid in schedule:
            filters = {"fairness_id": gid, "outcome": "Dispatched"}
            b = _histogram_buckets(s0, QUEUE_WAIT_HISTOGRAM, filters)
            a = _histogram_buckets(s1, QUEUE_WAIT_HISTOGRAM, filters)
            entry = {"group": gid, "state": None, "observations": None,
                     "p50_seconds": None, "p90_seconds": None, "p99_seconds": None}
            if a is None and b is None:
                entry["state"] = "not_recorded"
                groups.append(entry)
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
                if scrape_failed1:
                    any_scrape_gap = True
                else:
                    any_restart = True
                delta = dict(a)
            count = delta.get(float("inf"), 0.0)
            entry["observations"] = count
            if count <= 0:
                entry["state"] = "no_observations"
                groups.append(entry)
                continue
            p50, _ = histogram_quantile(0.50, delta)
            p90, _ = histogram_quantile(0.90, delta)
            p99, _ = histogram_quantile(0.99, delta)
            entry.update({"state": "ok", "p50_seconds": p50, "p90_seconds": p90, "p99_seconds": p99})
            groups.append(entry)
        windows.append({"start_s": start_s, "end_s": end_s, "groups": groups})
    return windows, any_restart, any_scrape_gap


# UNI-226: per-tenant TTFT and ITL, from the upstream llm-d-router
# framework's own histograms -- fairness_id-labelled since v0.11.0
# (pkg/epp/handlers/response.go), not something this report or the loadgen
# has ever had to measure client-side. TTFT is recorded for EVERY request
# (streaming or not -- a non-streaming request's TTFT equals its total
# duration, which is why it is only a useful *distinct* signal from
# P50_SEC/P95_SEC under streaming); ITL is recorded per response chunk for
# streaming requests only, so a run with STREAM_FRACTION=0 for a group
# produces "no_observations" for that group here, not an error. Neither
# histogram carries an `outcome` label (unlike queue-wait) -- there is
# nothing to filter beyond fairness_id itself.
TTFT_HISTOGRAM = "llm_d_epp_request_ttft_seconds"
ITL_HISTOGRAM = "llm_d_epp_request_streaming_itl_seconds"


def compute_ttft_itl_whole_run(before_labeled, after_labeled, group_ids):
    """Whole-run p50/p95 TTFT and ITL per group, from the same single
    before/after snapshot pair compute_pick_latency reads, via the same
    _histogram_buckets/histogram_quantile bucket-diff compute_queue_wait_windows
    uses. Same three-state contract as every other histogram section in this
    file: "not_recorded" (no _bucket line in either snapshot -- the scrape
    filter didn't capture this family, or the EPP never saw this group),
    "no_observations" (captured, but the count did not move -- e.g. ITL for a
    group that never streamed), "ok" (p50/p95 computed). Also returns a
    pool-level entry (no fairness_id filter) for the vLLM cross-check."""
    def one(histogram, filters):
        b = _histogram_buckets(before_labeled, histogram, filters)
        a = _histogram_buckets(after_labeled, histogram, filters)
        entry = {"state": None, "observations": None, "p50_seconds": None, "p95_seconds": None}
        if a is None and b is None:
            entry["state"] = "not_recorded"
            return entry
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
            delta = dict(a)
        count = delta.get(float("inf"), 0.0)
        entry["observations"] = count
        if count <= 0:
            entry["state"] = "no_observations"
            return entry
        p50, _ = histogram_quantile(0.50, delta)
        p95, _ = histogram_quantile(0.95, delta)
        entry.update({"state": "ok", "p50_seconds": p50, "p95_seconds": p95})
        return entry

    groups = {}
    for gid in group_ids:
        groups[gid] = {
            "ttft": one(TTFT_HISTOGRAM, {"fairness_id": gid}),
            "itl": one(ITL_HISTOGRAM, {"fairness_id": gid}),
        }
    pool = {
        "ttft": one(TTFT_HISTOGRAM, None),
        "itl": one(ITL_HISTOGRAM, None),
    }
    return {"groups": groups, "pool": pool}


def compute_ttft_itl_windows(timeseries_labeled, schedule):
    """Windowed p50/p95 TTFT and ITL per group -- same shape, same
    restart/scrape-gap handling, same per-window structure as
    compute_queue_wait_windows above, just without that function's
    outcome="Dispatched" filter (TTFT/ITL carry no `outcome` label)."""
    if len(timeseries_labeled) < 2:
        return [], False, False
    t0 = timeseries_labeled[0][0]
    windows = []
    any_restart = False
    any_scrape_gap = False
    for (e0, _, s0, _scrape_failed0), (e1, _, s1, scrape_failed1) in zip(timeseries_labeled, timeseries_labeled[1:]):
        start_s, end_s = e0 - t0, e1 - t0
        groups = []
        for gid in schedule:
            entry = {"group": gid}
            for key, histogram in (("ttft", TTFT_HISTOGRAM), ("itl", ITL_HISTOGRAM)):
                filters = {"fairness_id": gid}
                b = _histogram_buckets(s0, histogram, filters)
                a = _histogram_buckets(s1, histogram, filters)
                sub = {"state": None, "observations": None, "p50_seconds": None, "p95_seconds": None}
                if a is None and b is None:
                    sub["state"] = "not_recorded"
                    entry[key] = sub
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
                    if scrape_failed1:
                        any_scrape_gap = True
                    else:
                        any_restart = True
                    delta = dict(a)
                count = delta.get(float("inf"), 0.0)
                sub["observations"] = count
                if count <= 0:
                    sub["state"] = "no_observations"
                    entry[key] = sub
                    continue
                p50, _ = histogram_quantile(0.50, delta)
                p95, _ = histogram_quantile(0.95, delta)
                sub.update({"state": "ok", "p50_seconds": p50, "p95_seconds": p95})
                entry[key] = sub
            groups.append(entry)
        windows.append({"start_s": start_s, "end_s": end_s, "groups": groups})
    return windows, any_restart, any_scrape_gap


def _average_ranks(values):
    """Standard tie-aware ranking: equal values get the average of the rank
    positions they'd occupy if broken arbitrarily (e.g. two values tied for
    2nd/3rd both get rank 2.5). Ascending order (rank 1 = smallest value).
    Used for Spearman correlation so a genuine weight tie (e.g. 98/1/1's
    app2==end-users) never gets forced into an arbitrary strict order --
    the two tied entries share a rank, so their relative order against each
    other cannot affect the correlation either way."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1
    return ranks


def _spearman(xs, ys):
    """Pearson correlation of the two rank vectors -- the standard
    tie-corrected Spearman rank correlation. Returns None if either side has
    zero variance (e.g. every weight equal, or every TTFT identical), since
    rank correlation is undefined there, not 0 or 1."""
    n = len(xs)
    if n < 2:
        return None
    rx, ry = _average_ranks(xs), _average_ranks(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = sum((a - mx) ** 2 for a in rx)
    vy = sum((b - my) ** 2 for b in ry)
    if vx <= 0 or vy <= 0:
        return None
    return cov / (vx * vy) ** 0.5


def compute_priority_verdict(primary_verdict, offered_groups, weights, ttft_whole_run, noise_floor_seconds=None):
    """The SPLIT-FAIL / PRIORITY-OK secondary verdict (UNI-226, board
    direction 2026-11-10): when the primary share verdict FAILs, check
    whether per-tenant TTFT was nonetheless ordered the way the configured
    weights predict -- "the policy was prioritising correctly even though
    the share target wasn't met" is a materially different, more favourable
    outcome than a bare FAIL, and UNI-103's equal-workers-control run (app1
    30.7%/+9.6, app2 30.7%/+20.1, end-users 38.7%/-29.7 on share, but
    app1 7.5s/app2 7.4s/end-users 5.9s on latency -- the highest-weight
    tenant served fastest) is exactly the case this exists to stop silently
    discarding.

    Only meaningful when the primary verdict is FAIL -- a PASS already means
    the policy achieved the target split, so there is nothing for a
    secondary ordering check to rescue. Ties in `weights` are handled via
    tie-aware rank correlation (see _average_ranks/_spearman): two tenants
    configured with equal weight are never forced into an arbitrary order
    against each other, only against a tenant with a genuinely different
    weight.
    """
    if primary_verdict != "FAIL":
        return {
            "applicable": False,
            "result": "N/A (share already PASS)",
            "reason": "secondary verdict only rescues a FAIL; primary verdict was not FAIL",
        }

    missing = [g for g in offered_groups if ttft_whole_run.get(g, {}).get("ttft", {}).get("state") != "ok"]
    if missing:
        return {
            "applicable": True,
            "result": "not_evaluated",
            "reason": f"TTFT not available (state != ok) for: {', '.join(missing)}",
            "groups": offered_groups,
        }

    weight_values = [weights[g] for g in offered_groups]
    ttft_p50_values = [ttft_whole_run[g]["ttft"]["p50_seconds"] for g in offered_groups]
    ttft_p95_values = [ttft_whole_run[g]["ttft"]["p95_seconds"] for g in offered_groups]

    # Rank by weight descending == rank by TTFT ascending, for a correctly
    # prioritising policy (higher weight -> lower TTFT). Spearman on
    # (weight, -TTFT) reported as a continuous, informational summary of how
    # close the two orderings are -- but NOT used as the pass/fail gate.
    #
    # Why not gate on correlation == 1.0, despite that being the board's own
    # literal phrasing (2026-11-10): tie-aware (average-rank) Spearman does
    # NOT make a weight tie "not count" the way a reader might expect. Two
    # groups tied on weight still get compared against each other through
    # their TTFT ranks' deviation from the shared average rank, so an
    # otherwise-perfect result (the only distinctly-weighted group correctly
    # fastest) scores well under 1.0 purely from noise between two tenants
    # whose weights are equal and whose relative order the board does not
    # care about -- confirmed numerically: weights (98,1,1) with TTFT
    # correctly ordered (0.1s, 0.5s, 0.6s) gives correlation 0.866, not 1.0,
    # for exactly this reason. 98/1/1 is precisely the row this matters for
    # (app2 and end-users both weight 1).
    #
    # The gate actually used is the direct statement of what "the orderings
    # agree" should mean under ties: no pairwise inversion between any two
    # groups with GENUINELY DIFFERENT weights (equal-weight pairs are
    # excluded from the pairwise check, same as they are mathematically
    # inert in a tie-aware correlation of a fully-distinct ranking). This
    # reduces to correlation == 1.0 exactly when every weight is distinct
    # (the common case -- e.g. 20/10/65), and is strictly more correct than
    # the raw correlation gate whenever any weight tie exists.
    correlation = _spearman(weight_values, [-v for v in ttft_p50_values])
    no_inversions = True
    for i, gi in enumerate(offered_groups):
        for j, gj in enumerate(offered_groups):
            if i >= j or weight_values[i] == weight_values[j]:
                continue
            higher, lower = (gi, gj) if weight_values[i] > weight_values[j] else (gj, gi)
            higher_p50 = ttft_whole_run[higher]["ttft"]["p50_seconds"]
            lower_p50 = ttft_whole_run[lower]["ttft"]["p50_seconds"]
            if not (higher_p50 < lower_p50):
                no_inversions = False

    top_group = max(offered_groups, key=lambda g: weights[g])
    top_p50 = ttft_whole_run[top_group]["ttft"]["p50_seconds"]
    top_p95 = ttft_whole_run[top_group]["ttft"]["p95_seconds"]
    strictly_lowest_p50 = all(
        top_p50 < ttft_p50_values[i] for i, g in enumerate(offered_groups)
        if g != top_group and weights[g] != weights[top_group]
    )
    strictly_lowest_p95 = all(
        top_p95 < ttft_p95_values[i] for i, g in enumerate(offered_groups)
        if g != top_group and weights[g] != weights[top_group]
    )

    next_best_p50 = min(
        (v for g, v in zip(offered_groups, ttft_p50_values) if g != top_group and weights[g] != weights[top_group]),
        default=None,
    )
    separation_seconds = (next_best_p50 - top_p50) if next_best_p50 is not None else None
    separation_state = "not_evaluated"
    separation_ok = None
    if noise_floor_seconds is not None and separation_seconds is not None:
        separation_ok = separation_seconds > noise_floor_seconds
        separation_state = "ok" if separation_ok else "insufficient"

    rank_ok = no_inversions and strictly_lowest_p50 and strictly_lowest_p95
    if rank_ok and (noise_floor_seconds is None or separation_ok):
        result = "PRIORITY-OK"
    else:
        result = "PRIORITY-FAIL"

    return {
        "applicable": True,
        "result": result,
        "top_weighted_group": top_group,
        "top_group_ttft_p50_seconds": top_p50,
        "top_group_ttft_p95_seconds": top_p95,
        "top_group_strictly_lowest_p50": strictly_lowest_p50,
        "top_group_strictly_lowest_p95": strictly_lowest_p95,
        "no_inversions_among_distinct_weights": no_inversions,
        "rank_correlation": correlation,
        "separation_from_next_seconds": separation_seconds,
        "noise_floor_seconds": noise_floor_seconds,
        "separation_state": separation_state,
        "groups": offered_groups,
        "weights": weights,
    }


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
                  alerts_path=None, alert_rules_path=None, alerts_step_seconds=30.0,
                  priority_noise_floor_seconds=None,
                  queue_depth_threshold=32.0, kv_cache_util_threshold=0.8):
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
    capped_groups = (
        {"app2"}
        # UNI-225: app2-trickle-discriminating reuses app2-trickle's own
        # 2-worker trickle/capped-group scoring unchanged -- only the scored
        # app1/end-users pair's sizing differs between the two scenarios
        # (see 15-fairness-benchmark.sh).
        if scenario in ("app2-trickle", "app2-trickle-discriminating") and len(offered_groups) == 3
        else set()
    )
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
    # UNI-225: same denominator convention as offered_weight_total (offered
    # groups only, minus any capped_groups) so worker_share_pct is directly
    # comparable to expected_share_pct -- see the module docstring's UNI-225
    # paragraph. offered_workers holds a rate, not a count, under the
    # open-loop generator, but the share computation is unit-agnostic.
    offered_workers_total = sum(
        offered_workers.get(g, 0) or 0.0
        for g in offered_groups
        if g not in capped_groups
    )

    # UNI-222: resolve the schedule -- and, when timeseries is available, the
    # per-window data -- before the whole-run expected/observed share
    # computation below, so a group with a declared join/leave or duty-cycle
    # schedule can be scored against its own time-weighted entitlement
    # instead of the flat weight ratio applied uniformly for the run's whole
    # duration. See schedule_aware_whole_run_shares above and
    # docs/design.md "Whole-run scoring with a declared schedule". windows/
    # timeseries are computed whenever timeseries is available at all --
    # the UNI-127 timeline section further below wants them regardless of
    # whether the schedule is actually non-trivial; only the whole-run
    # correction itself is gated on schedule_has_partial_offering, so a
    # plain full-run scenario's expected_share_pct/deviation_pts/verdict
    # stay byte-identical to before this existed.
    run_duration = duration_seconds if duration_seconds is not None else (logged_duration or 0)
    timeline_cfg = {}
    if timeline_config_path:
        with open(timeline_config_path) as f:
            timeline_cfg = json.load(f)
    schedule = resolve_schedule(timeline_cfg.get("tenants"), offered_groups, run_duration)
    chaos_events = timeline_cfg.get("chaos_events", [])
    windows, windows_epp_restarted, windows_scrape_gap = [], False, False
    schedule_aware_shares = {}
    if metrics_timeseries_path:
        timeline_weights = {g: (weight_after.get(g) if weight_after.get(g) is not None else weight_before.get(g)) or 0.0
                             for g in schedule}
        timeseries = parse_timeseries(metrics_timeseries_path)
        windows, windows_epp_restarted, windows_scrape_gap = compute_windows(timeseries, schedule, timeline_weights)
        if schedule_has_partial_offering(schedule, run_duration):
            schedule_aware_shares = schedule_aware_whole_run_shares(windows, offered_groups)

    rows = []
    deviations_for_verdict = []
    worker_vs_weight_gaps = []
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
        worker_share_pct = None
        worker_vs_weight_gap_pts = None
        if is_offered and gid != solo and gid not in capped_groups:
            if offered_weight_total > 0 and weight is not None:
                expected_pct = 100.0 * weight / offered_weight_total
            # UNI-225's worker-vs-weight question ("does this scenario's
            # worker sizing alone predict the split") and UNI-146 (C1)'s
            # request-count share below are both about the configured
            # whole-run sizing, not about how long a group was actually
            # present -- they keep this flat definition even for a group
            # UNI-222's schedule-aware correction below overrides
            # expected_pct/deviation_pts for.
            flat_expected_pct = expected_pct
            delivered_tokens_for_pct = deltas.get(gid)
            if offered_tokens_total > 0 and delivered_tokens_for_pct is not None:
                observed_pct = 100.0 * delivered_tokens_for_pct / offered_tokens_total
            else:
                observed_pct = 0.0
            # UNI-222: a group with a declared join/leave or duty-cycle
            # schedule is scored against its time-weighted entitlement
            # instead of the flat one above, whenever the timeline data
            # needed to compute it is available -- see
            # schedule_aware_whole_run_shares.
            if gid in schedule_aware_shares:
                expected_pct = schedule_aware_shares[gid]["expected_share_pct"]
                observed_pct = schedule_aware_shares[gid]["observed_share_pct"]
            if expected_pct is not None and observed_pct is not None:
                deviation_pts = observed_pct - expected_pct
                deviations_for_verdict.append((gid, deviation_pts))
            if offered_workers_total > 0:
                worker_share_pct = 100.0 * (offered_workers.get(gid, 0) or 0.0) / offered_workers_total
            if flat_expected_pct is not None and worker_share_pct is not None:
                worker_vs_weight_gap_pts = worker_share_pct - flat_expected_pct
                worker_vs_weight_gaps.append((gid, worker_vs_weight_gap_pts))
            # UNI-146 (C1): same flat_expected_pct target, but against this
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
            if flat_expected_pct is not None:
                request_share_deviation_pts = request_share_pct - flat_expected_pct

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
            "worker_share_pct": worker_share_pct,
            "worker_vs_weight_gap_pts": worker_vs_weight_gap_pts,
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

    # UNI-225: does this run's own sizing let the weighted-split verdict above
    # actually distinguish "the split follows the configured weights" from
    # "the split follows however many workers each group happened to run"?
    # See the module docstring's UNI-225 paragraph for the full rationale.
    # `None` (not applicable) for the same four cases already excluded from
    # the symmetric deviation check -- solo, control, UNCONTENDED, and the
    # demand-capped scenario never reach a weights-vs-workers question in the
    # first place.
    max_worker_vs_weight_gap = max((abs(g) for _, g in worker_vs_weight_gaps), default=None)
    is_discriminating = None
    if (
        solo is None
        and not control
        and not is_uncontended
        and not is_demand_capped_scenario
        and max_worker_vs_weight_gap is not None
    ):
        is_discriminating = max_worker_vs_weight_gap >= threshold_points
        if not is_discriminating:
            reasons.append(
                f"NON-DISCRIMINATING (UNI-225): offered worker shares stay within "
                f"{max_worker_vs_weight_gap:.1f} points of the configured weight shares, under "
                f"the {threshold_points:g}-point bar -- 'follows the weights' and 'follows the "
                f"workers' predict the same split here, so this {verdict} is not evidence for "
                "weighted fairness specifically"
            )

    # UNI-127: additive -- except that, as of UNI-222, `schedule`/`windows`
    # computed above already fed the whole-run expected/observed shares (and
    # therefore `verdict`) above when schedule_has_partial_offering was true.
    # What's purely additive here is everything specific to this section:
    # phase_edges, convergence, and the queue-wait windows. A run with no
    # timeseries/timeline-config, or a schedule with nothing non-trivial in
    # it, leaves timeline=None or an empty-schedule timeline with `verdict`
    # computed exactly as before UNI-222 either way.
    timeline_section = None
    if metrics_timeseries_path:
        phase_edges = compute_phase_edges(schedule, chaos_events, run_duration)
        convergence = compute_convergence(windows, phase_edges, threshold_points)
        # UNI-164: same metrics-timeseries.txt file, parsed a second time with
        # every label kept (see parse_timeseries_labeled) -- needed because
        # the queue-wait histogram has a `le` label per bucket, which
        # parse_timeseries' single-fairness_id-key dict would collapse.
        timeseries_labeled = parse_timeseries_labeled(metrics_timeseries_path)
        queue_wait_windows, queue_wait_epp_restarted, queue_wait_scrape_gap = compute_queue_wait_windows(timeseries_labeled, schedule)
        timeline_section = {
            "window_seconds": window_seconds,
            "schedule": schedule,
            "chaos_events": chaos_events,
            "phase_edges": phase_edges,
            "windows": windows,
            "convergence": convergence,
            "epp_restarted_during_windows": windows_epp_restarted,
            # UNI-230: a window's closing scrape failing outright (curl exit
            # != 0) looks identical to a restart once grepped (zero matching
            # lines either way) -- compute_windows/compute_queue_wait_windows
            # only tell them apart via that scrape's own recorded exit code,
            # so this stays a separate flag rather than folding into
            # *_epp_restarted above.
            "windows_scrape_gap": windows_scrape_gap,
            "queue_wait_windows": queue_wait_windows,
            "queue_wait_epp_restarted": queue_wait_epp_restarted,
            "queue_wait_scrape_gap": queue_wait_scrape_gap,
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

    # UNI-224: which saturation-detector limb (queue depth vs KV cache) bound,
    # reconstructed from the EPP's own pool-level gauges -- see
    # compute_saturation_limb's docstring for why neither ratio is exposed
    # directly.
    saturation_section = compute_saturation_limb(
        metrics_timeseries_path, queue_depth_threshold, kv_cache_util_threshold
    )

    # UNI-226: per-tenant TTFT/ITL plus the SPLIT-FAIL/PRIORITY-OK secondary
    # verdict -- purely additive like ledger/shed/pick_latency above, never
    # reads or writes `verdict` itself (compute_priority_verdict only
    # consumes its already-final value to decide whether the secondary
    # verdict is applicable). Windowed TTFT/ITL needs the same
    # --metrics-timeseries input the queue-wait/dispatch-share windows above
    # do; omit it and the whole-run numbers and priority verdict still work,
    # same "omit the flag, get the old shape" contract every other optional
    # section in this report follows.
    ttft_itl_whole_run = compute_ttft_itl_whole_run(before_labeled, after_labeled, offered_groups)
    ttft_itl_windows = None
    ttft_itl_epp_restarted = False
    ttft_itl_scrape_gap = False
    if metrics_timeseries_path:
        ttft_itl_windows, ttft_itl_epp_restarted, ttft_itl_scrape_gap = compute_ttft_itl_windows(
            timeseries_labeled, schedule
        )
    priority_verdict = compute_priority_verdict(
        verdict, offered_groups, weights_for_shed, ttft_itl_whole_run["groups"],
        noise_floor_seconds=priority_noise_floor_seconds,
    )
    ttft_itl_section = {
        "window_seconds": window_seconds,
        "groups": ttft_itl_whole_run["groups"],
        "pool": ttft_itl_whole_run["pool"],
        "windows": ttft_itl_windows,
        "epp_restarted_during_windows": ttft_itl_epp_restarted,
        "scrape_gap_in_windows": ttft_itl_scrape_gap,
        "priority_verdict": priority_verdict,
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
            # UNI-163: the before/after snapshot pair this report is built from only
            # sees two points on the line -- it flags epp_restarted_mid_run above only
            # when a GROUP'S OWN after-value is lower than its before-value. A restart
            # strictly between a near-zero before and a lower (but still positive)
            # after reads as a normal monotonic rise and is invisible to it, even
            # though the windowed series (compute_windows, scraped every
            # WINDOW_SECONDS through the run) crosses the reset directly and catches
            # it. This field surfaces that gap rather than silently trusting whichever
            # check happened to fire: True means the windowed series saw a restart
            # this snapshot pair did not, so every before/after delta above --
            # including the verdict and the ledger cross-check below -- undercounts
            # real traffic and should be read with that in mind. Deliberately does
            # NOT change `result`/`reasons` itself: a scenario that intentionally
            # recreates the EPP mid-run (e.g. a CHAOS_EPP_DELETE_AT resilience case)
            # may already score that correctly through its own path, and retroactively
            # forcing FAIL here could silently change past scoring conventions this
            # report doesn't have visibility into. See UNI-163's writeup in
            # docs/poc-results.md for the run this was found on.
            "epp_restarted_in_windows_but_not_snapshot_pair": bool(
                timeline_section
                and timeline_section.get("epp_restarted_during_windows")
                and not epp_restarted
            ),
            # UNI-230: a window's delivered-tokens counter going backwards
            # because its closing /metrics scrape failed outright (curl
            # exit != 0), not because the EPP actually restarted. Unlike
            # epp_restarted_in_windows_but_not_snapshot_pair above, this is
            # never folded into epp_restarted_mid_run or into that field --
            # it is a harness data-collection gap, not process evidence, and
            # treating it as a restart signal is exactly the false positive
            # that misdiagnosed twenty-group-scale-discriminating's run (see
            # UNI-230: no pod-identity change, no k8s restart event, and a
            # container restart count of 0 all corroborated "no restart
            # happened" against a report that nonetheless set the restart
            # flag). True means at least one window's delta was clamped to
            # zero because its closing scrape failed, not because a group's
            # counter genuinely reset -- that window's numbers still
            # undercount real traffic for the same reason a real restart's
            # would, but it is not evidence of an EPP process restart.
            "scrape_gap_in_windows": bool(
                timeline_section
                and (timeline_section.get("windows_scrape_gap") or timeline_section.get("queue_wait_scrape_gap"))
            ),
            "solo_group": solo,
            "capped_groups": sorted(capped_groups),
            "uncontended_threshold_seconds": UNCONTENDED_SECONDS_THRESHOLD,
            # UNI-225: see the module docstring's UNI-225 paragraph.
            "max_worker_vs_weight_gap_points": max_worker_vs_weight_gap,
            "discriminating": is_discriminating,
            # UNI-222: which offered groups' expected_share_pct/observed_share_pct/
            # deviation_pts above (in `groups`) used the time-weighted,
            # declared-schedule-aware definition instead of the flat
            # whole-run weight ratio -- see schedule_aware_whole_run_shares
            # and docs/design.md "Whole-run scoring with a declared
            # schedule". Empty for the overwhelming majority of scenarios
            # (no declared schedule, or every offered group active for the
            # whole run), which get the exact pre-UNI-222 numbers.
            "schedule_aware_groups": sorted(schedule_aware_shares.keys()),
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
        "ttft_itl": ttft_itl_section,
        "saturation": saturation_section,
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
    lines.append("## Per-tenant TTFT / ITL and the priority verdict (UNI-226)")
    lines.append("")
    ti = report.get("ttft_itl")
    if not ti:
        lines.append("N/A: report predates UNI-226.")
    else:
        ti_state_label = {
            "not_recorded": "not recorded (absent from both snapshots -- check the benchmark's "
                             "scrape filter includes `llm_d_epp_request_(ttft|streaming_itl)_seconds_`)",
            "no_observations": "no observations (e.g. ITL with STREAM_FRACTION=0 for this group)",
        }

        def tfmt(v):
            return "n/a" if v is None else f"{v * 1000:.0f}ms"

        lines.append(
            "`llm_d_epp_request_ttft_seconds` (every request, streaming or not -- non-streaming "
            "TTFT equals total duration) and `llm_d_epp_request_streaming_itl_seconds` (streaming "
            "requests only) from the EPP's own framework-level histograms, fairness_id-labelled. "
            "Whole-run, from the same before/after snapshot pair the verdict above uses."
        )
        lines.append("")
        lines.append("| group | TTFT state | TTFT obs | TTFT p50 | TTFT p95 | ITL state | ITL obs | ITL p50 | ITL p95 |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for gid, g in ti["groups"].items():
            t_, i_ = g["ttft"], g["itl"]
            t_state = ti_state_label.get(t_["state"], "ok")
            i_state = ti_state_label.get(i_["state"], "ok")
            lines.append(
                f"| {gid} | {t_state} | {fmt(t_['observations'], '', '.0f')} | {tfmt(t_['p50_seconds'])} | "
                f"{tfmt(t_['p95_seconds'])} | {i_state} | {fmt(i_['observations'], '', '.0f')} | "
                f"{tfmt(i_['p50_seconds'])} | {tfmt(i_['p95_seconds'])} |"
            )
        pool_t, pool_i = ti["pool"]["ttft"], ti["pool"]["itl"]
        lines.append(
            f"| **pool (all groups)** | {ti_state_label.get(pool_t['state'], 'ok')} | "
            f"{fmt(pool_t['observations'], '', '.0f')} | {tfmt(pool_t['p50_seconds'])} | "
            f"{tfmt(pool_t['p95_seconds'])} | {ti_state_label.get(pool_i['state'], 'ok')} | "
            f"{fmt(pool_i['observations'], '', '.0f')} | {tfmt(pool_i['p50_seconds'])} | {tfmt(pool_i['p95_seconds'])} |"
        )
        lines.append("")
        lines.append(
            "The pool row is the EPP-side number to compare against vLLM's own pool-level "
            "`vllm:time_to_first_token_seconds` for the UNI-226 cross-check (done externally, "
            "against live Prometheus, not by this script) -- a large gap between the two would "
            "point at EPP/gateway-added overhead, not vLLM's own prefill time."
        )

        pv = ti["priority_verdict"]
        lines.append("")
        if not pv["applicable"]:
            lines.append(f"**Secondary (priority) verdict: {pv['result']}** -- {pv['reason']}")
        elif pv["result"] == "not_evaluated":
            lines.append(f"**Secondary (priority) verdict: not evaluated** -- {pv['reason']}")
        else:
            sep = "n/a" if pv["separation_from_next_seconds"] is None else f"{pv['separation_from_next_seconds'] * 1000:.0f}ms"
            floor = "not given (separation check skipped)" if pv["noise_floor_seconds"] is None else f"{pv['noise_floor_seconds'] * 1000:.0f}ms"
            corr = "n/a" if pv["rank_correlation"] is None else f"{pv['rank_correlation']:.2f}"
            lines.append(
                f"**Secondary (priority) verdict: {pv['result']}** -- the share verdict above is "
                "FAIL, so this is the board's second, independent success criterion (2026-11-10): "
                "did the policy nonetheless order tenants by weight? Top-weighted group: "
                f"`{pv['top_weighted_group']}` (TTFT p50 {tfmt(pv['top_group_ttft_p50_seconds'])}, "
                f"p95 {tfmt(pv['top_group_ttft_p95_seconds'])}, strictly lowest among "
                f"distinctly-weighted groups: p50={pv['top_group_strictly_lowest_p50']}/"
                f"p95={pv['top_group_strictly_lowest_p95']}; no rank inversion among any "
                f"distinctly-weighted pair: {pv['no_inversions_among_distinct_weights']} -- this, "
                "not raw rank correlation, is what gates the verdict, since a genuine weight tie "
                "(e.g. 98/1/1's app2==end-users) makes exact correlation 1.0 unreachable by "
                f"construction even when ordering is otherwise perfect). Rank correlation {corr} "
                "(1.00 = exact agreement, informational only) shown for reference. Separation from "
                f"the next distinctly-weighted group: {sep} against a noise floor of {floor}."
            )
        if ti.get("windows") is not None:
            lines.append("")
            lines.append(
                "**Windowed TTFT/ITL** "
                f"({len(ti['windows'])} windows" +
                (", EPP restart detected mid-window at least once" if ti.get("epp_restarted_during_windows") else "") +
                (", a metrics scrape failed mid-window at least once (UNI-230, not a restart)" if ti.get("scrape_gap_in_windows") else "") +
                "):"
            )
            lines.append("")
            lines.append("| start (s) | end (s) | group | TTFT state | TTFT p50 | TTFT p95 | ITL state | ITL p50 | ITL p95 |")
            lines.append("|---|---|---|---|---|---|---|---|---|")
            for w in ti["windows"]:
                for g in w["groups"]:
                    t_, i_ = g["ttft"], g["itl"]
                    lines.append(
                        f"| {w['start_s']:.1f} | {w['end_s']:.1f} | {g['group']} | "
                        f"{ti_state_label.get(t_['state'], 'ok')} | {tfmt(t_['p50_seconds'])} | "
                        f"{tfmt(t_['p95_seconds'])} | {ti_state_label.get(i_['state'], 'ok')} | "
                        f"{tfmt(i_['p50_seconds'])} | {tfmt(i_['p95_seconds'])} |"
                    )
        else:
            lines.append("")
            lines.append("N/A: no `--metrics-timeseries` recorded for this run, whole-run numbers above only.")

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
        # UNI-225: a PASS/FAIL that cannot distinguish weights-vs-workers (see
        # the module docstring) is flagged right next to the verdict itself,
        # not buried in the reasons list below.
        discriminating_note = " **(NON-DISCRIMINATING)**" if v.get("discriminating") is False else ""
        lines.append(f"**Verdict: {v['result']}**{discriminating_note} (threshold: {v['threshold_points']:g} points)")
        # UNI-226: a share FAIL is not the whole story -- point straight at the
        # secondary verdict (full detail in "Per-tenant TTFT / ITL" below)
        # instead of leaving a reader to assume this row is a flat failure.
        pv_top = (report.get("ttft_itl") or {}).get("priority_verdict")
        if v["result"] == "FAIL" and pv_top and pv_top.get("applicable"):
            lines.append(
                f"**Secondary (priority) verdict: {pv_top['result']}** -- see \"Per-tenant TTFT / "
                "ITL and the priority verdict (UNI-226)\" below for detail."
            )
    if v.get("max_worker_vs_weight_gap_points") is not None:
        lines.append(
            f"Worker-share vs. weight-share gap (UNI-225): "
            f"{v['max_worker_vs_weight_gap_points']:.1f} points"
            + (
                " -- below the pass bar, so this row cannot tell 'the split follows the "
                "weights' apart from 'the split follows the workers'"
                if v.get("discriminating") is False
                else ""
            )
        )
    if v.get("schedule_aware_groups"):
        lines.append(
            f"Schedule-aware expected share (UNI-222): {', '.join(v['schedule_aware_groups'])} "
            "scored against a time-weighted entitlement from the declared join/leave or "
            "duty-cycle schedule, not the flat whole-run weight ratio -- see "
            "docs/design.md \"Whole-run scoring with a declared schedule\"."
        )
    if v["reasons"]:
        lines.append("")
        for reason in v["reasons"]:
            lines.append(f"- {reason}")
    if v.get("epp_restarted_in_windows_but_not_snapshot_pair"):
        lines.append("")
        lines.append(
            "**Caveat (UNI-163): the EPP restarted mid-run in a way this verdict did not "
            "catch.** The windowed series below shows a counter going backwards between "
            "two in-run scrapes, but the single before/after snapshot pair this verdict is "
            "built from happened to read monotonically end-to-end (a near-zero start and a "
            "lower-but-still-higher-than-zero end look the same as no restart at all). "
            "Every before/after delta above -- the verdict and the ledger cross-check below "
            "-- is computed from the post-restart pod's fresh counters alone and undercounts "
            "real traffic; read them as a measurement of the time since the restart, not the "
            "whole run."
        )
    if v.get("scrape_gap_in_windows"):
        lines.append("")
        lines.append(
            "**Caveat (UNI-230): a mid-run metrics scrape failed outright, not an EPP "
            "restart.** At least one windowed delta below was clamped to zero because its "
            "closing `/metrics` scrape itself failed (the benchmark's own recorded curl exit "
            "code was nonzero), not because a group's counter genuinely went backwards. A "
            "connection-level scrape failure and a real restart produce identical zero-line "
            "output once grepped, so this is flagged separately from "
            "`epp_restarted_in_windows_but_not_snapshot_pair` rather than folded into it or "
            "into `epp_restarted_mid_run`. The affected window's own numbers still undercount "
            "real traffic for that window, but this is evidence of a dropped scrape, not of a "
            "process restart -- check for corroborating restart evidence (pod identity change, "
            "k8s restart events, container restart count) before treating it as one."
        )
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
    lines.append("## Saturation limb (UNI-224)")
    lines.append("")
    sat = report.get("saturation")
    if sat is None:
        lines.append(
            "Not evaluated: no `--metrics-timeseries` was captured for this run (pre-UNI-224 "
            "shape)."
        )
    elif sat["state"] == "no_samples":
        lines.append(
            "No usable timeseries samples (every scrape either failed or carried neither "
            "`llm_d_epp_average_queue_size` nor `llm_d_epp_average_kv_cache_utilization`)."
        )
    else:
        lines.append(
            f"Reconstructed from `llm_d_epp_average_queue_size` / `queueDepthThreshold` "
            f"({sat['queue_depth_threshold']:g}) and `llm_d_epp_average_kv_cache_utilization` / "
            f"`kvCacheUtilThreshold` ({sat['kv_cache_util_threshold']:g}) across "
            f"{sat['sample_count']} timeseries samples -- see docs/design.md's saturation-"
            "detector section for the roofline formula this reconstructs."
        )
        lines.append("")
        lines.append(
            f"**Bound at this run's peak roofline score: `{sat['bound_at_peak']}`** "
            f"({sat['kv_binding_sample_count']}/{sat['sample_count']} samples had the KV limb "
            "ahead of the queue limb)."
        )
        lines.append("")
        lines.append("| signal | peak value | peak ratio to threshold |")
        lines.append("|---|---|---|")
        lines.append(
            f"| `average_queue_size` | {sat['peak_average_queue_size']:.2f} | "
            f"{sat['peak_queue_ratio']:.4f} |"
        )
        lines.append(
            f"| `average_kv_cache_utilization` | {sat['peak_average_kv_cache_utilization']:.4f} | "
            f"{sat['peak_kv_ratio']:.4f} |"
        )
        lines.append("")
        if sat["peak_kv_ratio"] < 0.05 and sat["peak_queue_ratio"] >= 0.05:
            lines.append(
                "The KV-cache limb stayed near zero this run; every verdict above was decided "
                "on queue depth alone. See [UNI-224](/UNI/issues/UNI-224) for whether this "
                "backend's `--max-num-seqs`/`--max-model-len` caps make the KV limb reachable "
                "at all."
            )
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
        "short-prompt/long-output). `worker share %`/`worker-vs-weight gap "
        "(pts)` (UNI-225) compare this group's share of the offered worker "
        "count/rate against its own `expected %` (weight share) -- a small "
        "gap here means this row's sizing cannot distinguish 'the split "
        "follows the weights' from 'the split follows the workers', "
        "regardless of what the observed split did; see the verdict line "
        "above and the module docstring."
    )
    lines.append("")
    offered_col = "offered req/s" if r.get("generator") == "open-loop" else "offered workers"
    lines.append(
        f"| group | weight | {offered_col} | requests | statuses | p50s | p95s | "
        "delivered tokens | expected % | worker share % | worker-vs-weight gap (pts) | "
        "observed % | deviation (pts) | "
        "request-count % | request-count deviation (pts) | contended_seconds | "
        "cached ratio | dispatch_total |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
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
            f"{fmt(g['worker_share_pct'], '%')} | {fmt(g['worker_vs_weight_gap_pts'])} | "
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
                      (", a metrics scrape failed mid-window at least once (UNI-230, not a restart)" if t.get("windows_scrape_gap") else "") +
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
        lines.append(
            "**Flow-control queue wait, dispatched requests only** "
            f"(`{QUEUE_WAIT_HISTOGRAM}`, `outcome=\"Dispatched\"`" +
            (", EPP restart detected mid-window at least once" if t.get("queue_wait_epp_restarted") else "") +
            (", a metrics scrape failed mid-window at least once (UNI-230, not a restart)" if t.get("queue_wait_scrape_gap") else "") +
            "):"
        )
        lines.append("")
        lines.append("| start (s) | end (s) | group | state | observations | p50 wait | p90 wait | p99 wait |")
        lines.append("|---|---|---|---|---|---|---|---|")
        qw_state_label = {
            "not_recorded": "not recorded (absent from both snapshots)",
            "no_observations": "no dispatches in this window",
        }

        def qwfmt(v):
            return "n/a" if v is None else f"{v * 1000:.0f}ms"

        for w in t.get("queue_wait_windows", []):
            for g in w["groups"]:
                state = qw_state_label.get(g["state"], "ok")
                obs = "n/a" if g["observations"] is None else f"{g['observations']:.0f}"
                lines.append(
                    f"| {w['start_s']:.1f} | {w['end_s']:.1f} | {g['group']} | {state} | {obs} | "
                    f"{qwfmt(g['p50_seconds'])} | {qwfmt(g['p90_seconds'])} | {qwfmt(g['p99_seconds'])} |"
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
    p.add_argument(
        "--priority-noise-floor-seconds", type=float, default=None,
        help="UNI-226: minimum TTFT p50 separation (seconds) the top-weighted group must beat "
             "the next group by for the secondary SPLIT-FAIL/PRIORITY-OK verdict to count the "
             "separation check as satisfied, established from a same-config repeat run -- not "
             "asserted. Omit to compute rank correlation only and leave the separation check "
             "'not_evaluated' rather than defaulting to an unjustified number.",
    )
    p.add_argument(
        "--queue-depth-threshold", type=float, default=32.0,
        help="UNI-224: live EPP ConfigMap's maas-saturation queueDepthThreshold -- no metric "
             "exposes this, so the caller must read it from maas-epp-config and pass it "
             "through, same as --input-token-weight.",
    )
    p.add_argument(
        "--kv-cache-util-threshold", type=float, default=0.8,
        help="UNI-224: live EPP ConfigMap's maas-saturation kvCacheUtilThreshold. Defaults to "
             "0.8 to match llm-d-router@v0.11.0's own hardcoded default for an unset key -- "
             "this POC has never set it explicitly.",
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
        priority_noise_floor_seconds=args.priority_noise_floor_seconds,
        queue_depth_threshold=args.queue_depth_threshold,
        kv_cache_util_threshold=args.kv_cache_util_threshold,
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
