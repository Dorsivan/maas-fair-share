#!/usr/bin/env python3
"""UNI-303: drop-in weight-split checker for maas-fair-share.

A single, standalone file. It is NOT part of the POC harness and imports nothing from
this repository -- copy it anywhere and run it with a config file (see --help). An agent
with no history on this project should be able to point this at a running deployment and
get back a plain yes/no on whether the configured weights are actually being honoured.

WHAT IT DOES
  1. Drives closed-loop, concurrent load against N tenants (read from --config, not
     hardcoded to any tenant names), using each tenant's own MaaS API key.
  2. Scrapes the EPP's own /metrics endpoint directly (the same endpoint
     deploy/poc/15-fairness-report.py uses) before and after a scored window, and reads
     llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id} -- the plugin's
     own weighted-cost counter (inputTokenWeight*(prompt-cached) +
     cachedInputTokenWeight*cached + outputTokenWeight*completion; see
     pkg/fairness/weightedlas/cost.go). This script does NOT recompute the cost model
     client-side -- it reads the number the plugin already computed, so it can never
     disagree with the plugin about what "cost" means.
  3. Reports each tenant's observed share of that cost, the share its configured weight
     implies, the per-tenant deviation in points, and the max absolute deviation as the
     headline number -- same units and same default 10-point bar
     deploy/poc/15-fairness-report.py uses.
  4. Reads llm_d_epp_maas_fairness_contended_seconds_total{fairness_id} over the same
     window to say whether each tenant was actually contended, and for how much of the
     window. If the pool never saturated, it says so and refuses to print a misleading
     PASS/FAIL -- it prints UNCONTENDED instead, exactly like the existing report script's
     fourth verdict.
  5. Excludes a configurable warm-up prefix (default 30s) from the scored window and
     reports exactly how much it excluded (both in seconds and in requests already sent),
     because the plugin's own request-queueing and the vLLM waiting queue both need a
     moment to fill before a split is even enforceable.

WHAT IT NEEDS
  - Python 3.9+, standard library only. No pip install, nothing to vendor.
  - One MaaS API key (sk-oai-...) per tenant, already minted (see
    deploy/maas/mint-loadgen-keys.sh in the main repo -- minting needs cluster-admin-ish
    access this script does not assume you have).
  - A bearer token that can read the EPP's /metrics endpoint (the
    maas-epp-metrics-reader-token Secret, deploy/rbac.yaml in the main repo).
  - Network reach to both the model-serving route/gateway AND the EPP's metrics port
    (9090). From outside the cluster that is normally only the gateway Route; if you
    cannot reach the EPP's metrics port directly, run this from inside the cluster
    against the in-cluster Service instead (see --epp-metrics-url). Prefer the in-cluster
    Service for long runs regardless: the public *.apps Route's load balancer drops
    idle connections at 50s, which this script's own request connections will not hit
    (each is a single short-lived request), but a long metrics-scrape loop through the
    same LB can.

CONFIG FILE (JSON; see --config)
{
  "model": "llama-3-1-8b",
  "modelpath": "/maas-fairness-poc/maas-vllm-gpu",
  "tenants": [
    {"name": "app1",      "weight": 20, "identity": "app1-production", "api_key": "sk-oai-..."},
    {"name": "app2",      "weight": 10, "identity": "app2-batch",      "api_key": "sk-oai-..."},
    {"name": "end-users", "weight": 65, "identity": "end-user-1",      "api_key": "sk-oai-..."}
  ]
}
"name" must match the fairness_id label the EPP's grouping config produces for this
tenant -- usually the group name in maas-epp-config, NOT the raw identity header value
(check with one request and `--debug-labels` if unsure; see the troubleshooting note at
the bottom of --help). Any number of tenants is accepted.

This is deliberately its own, minimal JSON schema, not the POC harness's
deploy/poc/tenants/*.tenants manifest format (UNI-305) -- this script imports nothing
from the harness, by design, so it can be copied out and run anywhere. If you already
have a .tenants file and want the numbers to match, read the weight/group fields by hand;
there is no converter.

EXAMPLE
  METRICS_TOKEN=$(oc get secret maas-epp-metrics-reader-token -n maas-fairness-poc \\
      -o jsonpath='{.data.token}' | base64 -d) \\
  python3 weight-split-check.py \\
    --config tenants.json \\
    --gateway-url https://maas-gateway-maas-fairness-poc.apps.example.com \\
    --epp-metrics-url http://maas-vllm-gpu-kserve-router-scheduler.maas-fairness-poc.svc.cluster.local:9090 \\
    --duration 180 --warmup-seconds 30 --concurrency-per-tenant 16

TROUBLESHOOTING A FLAT SPLIT (verdict says PASS when it should FAIL, or everyone gets
roughly equal shares no matter the weights):
  - Check "contended" in the output first. Equal shares under NO contention is the
    correct, work-conserving result, not a bug -- see the UNCONTENDED verdict.
  - Check `fairness_id` really matches your tenant names: if a tenant's own traffic is
    landing in "unclassified" (wrong identity header, wrong group match), this script
    will report a zero or missing share for that tenant's declared name while an
    "unclassified" entry absorbs the cost instead. Run with --debug-labels to print every
    fairness_id label the metric actually carries.
  - identityHeader's compiled-in default was wrong for most of this POC's life
    (x-maas-subscription-id instead of x-maas-subscription, fixed in UNI-306) -- confirm
    your deployed image is new enough, or that maas-epp-config sets identityHeader
    explicitly either way.
"""
import argparse
import concurrent.futures
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request

COST_METRIC = "llm_d_epp_maas_fairness_contended_service_tokens_total"
CONTENDED_SECONDS_METRIC = "llm_d_epp_maas_fairness_contended_seconds_total"
DEFAULT_THRESHOLD_POINTS = 10.0
# A tenant counts as "contended" for the window if its contended-seconds delta is at
# least this fraction of the scored window length. Below that, the window measured
# offered load more than policy, and the run gets UNCONTENDED, not PASS/FAIL. Deliberately
# looser than deploy/poc/15-fairness-report.py's UNCONTENDED_SECONDS_THRESHOLD (1.0s
# absolute, meant for a single whole-run snapshot pair): this script's scored window is
# usually much shorter than a full benchmark run, so a fixed-second bar would be too easy
# to clear by accident.
CONTENDED_FRACTION_THRESHOLD = 0.5
PROMPT = "the quick brown fox " * 300


def read_config(path):
    with open(path) as f:
        cfg = json.load(f)
    if "tenants" not in cfg or not cfg["tenants"]:
        raise SystemExit(f"{path}: no tenants listed")
    names = set()
    for t in cfg["tenants"]:
        for key in ("name", "weight", "identity", "api_key"):
            if key not in t:
                raise SystemExit(f"{path}: tenant {t!r} missing required field {key!r}")
        if t["name"] in names:
            raise SystemExit(f"{path}: duplicate tenant name {t['name']!r}")
        names.add(t["name"])
    return cfg


def fetch_metrics_text(url, token, timeout=10, insecure=False):
    req = urllib.request.Request(url.rstrip("/") + "/metrics",
                                  headers={"Authorization": f"Bearer {token}"})
    ctx = None
    if insecure:
        import ssl
        ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return resp.read().decode("utf-8", errors="replace")


_METRIC_LINE_RE = re.compile(r'^([a-zA-Z_:][a-zA-Z0-9_:]*)(\{([^}]*)\})?\s+([^\s#]+)\s*$')
_LABEL_RE = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)="((?:[^"\\]|\\.)*)"')


def parse_prometheus_text(text):
    """metric_name -> list of (labels_dict, float_value). Minimal exposition-format
    parser: no HELP/TYPE handling beyond skipping comment lines, no histogram/summary
    special-casing (this script only reads plain counters). Good enough for a direct
    /metrics scrape; if you need the full format, read deploy/poc/15-fairness-report.py's
    parse_metrics_labeled_text instead and port it in."""
    out = {}
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        m = _METRIC_LINE_RE.match(line)
        if not m:
            continue
        name, _, labelstr, value = m.groups()
        try:
            value = float(value)
        except ValueError:
            continue
        labels = dict(_LABEL_RE.findall(labelstr or ""))
        out.setdefault(name, []).append((labels, value))
    return out


def metric_by_fairness_id(parsed, metric_name):
    result = {}
    for labels, value in parsed.get(metric_name, []):
        fid = labels.get("fairness_id")
        if fid is not None:
            result[fid] = result.get(fid, 0.0) + value
    return result


def send_one_request(gateway_url, modelpath, model, api_key, timeout, insecure):
    body = json.dumps({
        "model": model,
        "max_tokens": 64,
        "messages": [{"role": "user", "content": PROMPT}],
    }).encode()
    req = urllib.request.Request(
        gateway_url.rstrip("/") + modelpath + "/v1/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    ctx = None
    if insecure:
        import ssl
        ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            resp.read()
            return resp.status
    except urllib.error.HTTPError as e:
        try:
            e.read()
        except Exception:
            pass
        return e.code
    except Exception:
        return 0


def worker_loop(tenant, args, counters, stop_event):
    """One tenant's closed-loop concurrency-N worker pool: as soon as a request
    completes, send another, until stop_event is set. counters[tenant['name']] is
    incremented on every request *sent* (not completed), so the warm-up exclusion report
    can say exactly how many requests each tenant had already sent when scoring started."""
    def one():
        while not stop_event.is_set():
            counters[tenant["name"]] += 1
            send_one_request(args.gateway_url, args.modelpath, args.model,
                              tenant["api_key"], args.request_timeout, args.insecure)

    threads = [threading.Thread(target=one, daemon=True)
               for _ in range(args.concurrency_per_tenant)]
    for t in threads:
        t.start()
    return threads


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", required=True, help="JSON tenant config, see --help")
    p.add_argument("--gateway-url", required=True,
                   help="where chat-completion requests are sent, e.g. "
                        "https://maas-gateway-<ns>.apps.<cluster>")
    p.add_argument("--epp-metrics-url", required=True,
                   help="where /metrics is scraped, e.g. http://<scheduler-svc>:9090 "
                        "(in-cluster) -- NOT the model-serving route")
    p.add_argument("--metrics-token", default=os.environ.get("METRICS_TOKEN"),
                   help="bearer token for --epp-metrics-url; defaults to $METRICS_TOKEN "
                        "so it is never a shell history / process-list argument")
    p.add_argument("--modelpath", default=None,
                   help="overrides the config file's modelpath if set")
    p.add_argument("--model", default=None, help="overrides the config file's model if set")
    p.add_argument("--duration", type=float, default=180.0,
                   help="total wall-clock seconds to run, including warm-up (default 180)")
    p.add_argument("--warmup-seconds", type=float, default=30.0,
                   help="seconds of load to run before the scored window starts "
                        "(default 30) -- not scored, but it IS what fills the EPP's and "
                        "vLLM's queues; do not set this to 0 on an otherwise-idle pool")
    p.add_argument("--concurrency-per-tenant", type=int, default=16,
                   help="closed-loop workers per tenant (default 16). This has to be "
                        "enough to actually saturate the pool for every tenant you want "
                        "scored -- see the 'contended' output field, which tells you if "
                        "it wasn't")
    p.add_argument("--threshold-points", type=float, default=DEFAULT_THRESHOLD_POINTS,
                   help=f"pass bar in percentage points (default {DEFAULT_THRESHOLD_POINTS:g}, "
                        "matching deploy/poc/15-fairness-report.py's default)")
    p.add_argument("--request-timeout", type=float, default=90.0)
    p.add_argument("--insecure", action="store_true",
                   help="skip TLS verification (self-signed/service-CA certs)")
    p.add_argument("--debug-labels", action="store_true",
                   help="print every fairness_id label seen on the cost metric and exit, "
                        "without sending any load -- use this first if shares come back "
                        "zero or missing for a tenant you expect to see")
    p.add_argument("--json", action="store_true", help="print the full result as JSON too")
    args = p.parse_args()

    if not args.metrics_token:
        raise SystemExit("no metrics token: pass --metrics-token or set $METRICS_TOKEN")

    cfg = read_config(args.config)
    modelpath = args.modelpath if args.modelpath is not None else cfg.get("modelpath")
    model = args.model or cfg.get("model")
    if modelpath is None or not model:
        raise SystemExit("modelpath/model must be set in --config or on the command line")
    args.modelpath, args.model = modelpath, model
    tenants = cfg["tenants"]
    total_weight = sum(t["weight"] for t in tenants)

    if args.debug_labels:
        text = fetch_metrics_text(args.epp_metrics_url, args.metrics_token,
                                   insecure=args.insecure)
        parsed = parse_prometheus_text(text)
        seen = metric_by_fairness_id(parsed, COST_METRIC)
        print(f"fairness_id labels currently on {COST_METRIC}:")
        for fid, val in sorted(seen.items()):
            print(f"  {fid!r}: {val:g}")
        if not seen:
            print("  (none -- the metric has not been written to since the EPP started, "
                  "or the URL/token is wrong)")
        return

    if args.warmup_seconds >= args.duration:
        raise SystemExit("--warmup-seconds must be less than --duration")

    print(f"[weight-split-check] {len(tenants)} tenant(s), total weight {total_weight:g}, "
          f"duration {args.duration:g}s (warm-up {args.warmup_seconds:g}s, "
          f"scored window {args.duration - args.warmup_seconds:g}s), "
          f"concurrency {args.concurrency_per_tenant}/tenant")

    sent_counters = {t["name"]: 0 for t in tenants}
    stop_event = threading.Event()
    all_threads = []
    start = time.monotonic()
    for t in tenants:
        all_threads += worker_loop(t, args, sent_counters, stop_event)

    while time.monotonic() - start < args.warmup_seconds:
        time.sleep(0.5)
    sent_at_warmup_end = dict(sent_counters)
    before_text = fetch_metrics_text(args.epp_metrics_url, args.metrics_token,
                                      insecure=args.insecure)
    before = parse_prometheus_text(before_text)
    scored_window_start = time.monotonic()
    print(f"[weight-split-check] warm-up done: "
          f"{', '.join(f'{k}={v}req' for k, v in sent_at_warmup_end.items())} already sent, "
          f"not scored. Scoring starts now.")

    while time.monotonic() - start < args.duration:
        time.sleep(0.5)
    scored_window_seconds = time.monotonic() - scored_window_start
    after_text = fetch_metrics_text(args.epp_metrics_url, args.metrics_token,
                                     insecure=args.insecure)
    after = parse_prometheus_text(after_text)
    stop_event.set()
    for t in all_threads:
        t.join(timeout=5)

    cost_before = metric_by_fairness_id(before, COST_METRIC)
    cost_after = metric_by_fairness_id(after, COST_METRIC)
    contended_before = metric_by_fairness_id(before, CONTENDED_SECONDS_METRIC)
    contended_after = metric_by_fairness_id(after, CONTENDED_SECONDS_METRIC)

    rows = []
    total_cost_delta = 0.0
    for t in tenants:
        fid = t["name"]
        delta = cost_after.get(fid, 0.0) - cost_before.get(fid, 0.0)
        if delta < 0:
            delta = 0.0  # a counter reset (EPP restart) during the run; see the report
        total_cost_delta += delta
        contended_delta = contended_after.get(fid, 0.0) - contended_before.get(fid, 0.0)
        rows.append({"name": fid, "weight": t["weight"], "cost_delta": delta,
                     "contended_seconds": max(contended_delta, 0.0)})

    any_scored = total_cost_delta > 0
    for r in rows:
        r["expected_pct"] = 100.0 * r["weight"] / total_weight
        r["observed_pct"] = (100.0 * r["cost_delta"] / total_cost_delta) if any_scored else None
        r["deviation_pts"] = (r["observed_pct"] - r["expected_pct"]) if any_scored else None
        r["contended_fraction"] = (r["contended_seconds"] / scored_window_seconds
                                    if scored_window_seconds > 0 else 0.0)
        r["contended"] = r["contended_fraction"] >= CONTENDED_FRACTION_THRESHOLD

    all_contended = all(r["contended"] for r in rows)
    max_abs_dev = max((abs(r["deviation_pts"]) for r in rows if r["deviation_pts"] is not None),
                       default=None)

    if not any_scored:
        verdict = "NO_DATA"
        verdict_reason = (f"{COST_METRIC} did not move for any configured tenant during the "
                           "scored window. Either no traffic reached this EPP under these "
                           "fairness_id labels (check --debug-labels), or the window was too "
                           "short.")
    elif not all_contended:
        verdict = "UNCONTENDED"
        uncontended = [r["name"] for r in rows if not r["contended"]]
        verdict_reason = (
            f"{', '.join(uncontended)} spent less than "
            f"{CONTENDED_FRACTION_THRESHOLD:g}x the scored window actually contended. "
            "This is NOT a fairness measurement -- equal (or near-equal) shares here are "
            "the correct, work-conserving result when a tenant is not backlogged, not "
            "evidence the policy is doing nothing. Raise --concurrency-per-tenant until "
            "every scored tenant shows contended=true, or check that each tenant's "
            "worker count is enough to actually backlog it at its configured weight.")
    elif max_abs_dev <= args.threshold_points:
        verdict = "PASS"
        verdict_reason = (f"max deviation {max_abs_dev:.1f} points, within the "
                           f"{args.threshold_points:g}-point bar")
    else:
        verdict = "FAIL"
        worst = max(rows, key=lambda r: abs(r["deviation_pts"]))
        verdict_reason = (f"{worst['name']}: {worst['observed_pct']:.1f}% observed vs "
                           f"{worst['expected_pct']:.1f}% expected "
                           f"({worst['deviation_pts']:+.1f} pts), exceeding the "
                           f"{args.threshold_points:g}-point bar")

    print()
    print(f"{'tenant':<16} {'weight':>7} {'target%':>8} {'observed%':>10} {'dev(pts)':>9} "
          f"{'contended':>18}")
    for r in rows:
        obs = f"{r['observed_pct']:.1f}" if r["observed_pct"] is not None else "-"
        dev = f"{r['deviation_pts']:+.1f}" if r["deviation_pts"] is not None else "-"
        cont = f"{r['contended_fraction']*100:.0f}% of window" if scored_window_seconds > 0 else "-"
        print(f"{r['name']:<16} {r['weight']:>7g} {r['expected_pct']:>8.1f} {obs:>10} "
              f"{dev:>9} {cont:>18}")

    print()
    print(f"excluded warm-up: {args.warmup_seconds:g}s "
          f"({', '.join(f'{k}={v}req' for k, v in sent_at_warmup_end.items())} already sent "
          "and not scored)")
    print(f"scored window: {scored_window_seconds:.1f}s")
    if max_abs_dev is not None:
        print(f"max |deviation|: {max_abs_dev:.1f} points (bar: {args.threshold_points:g})")
    print(f"VERDICT: {verdict} -- {verdict_reason}")

    if args.json:
        print()
        print(json.dumps({
            "verdict": verdict, "verdict_reason": verdict_reason,
            "threshold_points": args.threshold_points, "max_abs_deviation_points": max_abs_dev,
            "scored_window_seconds": scored_window_seconds,
            "warmup_seconds": args.warmup_seconds,
            "requests_sent_during_warmup": sent_at_warmup_end,
            "tenants": rows,
        }, indent=2))

    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
