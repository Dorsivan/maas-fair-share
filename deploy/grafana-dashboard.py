"""Source of truth for the dashboard JSON embedded in deploy/grafana-dashboard.yaml.

Edit panels here, never the YAML by hand:

    python3 -I deploy/grafana-dashboard.py --write   # rewrites the ConfigMap data block in place
    python3 -I deploy/grafana-dashboard.py           # JSON to stdout

Every metric name and label used below was checked against the live UWM Thanos
Querier on 2026-11-01 (UNI-130); see docs/runbook.md "Find a run on the fairness
dashboard" for how to read it.
"""
import json, os, sys

J = 'job="maas-vllm-gpu-epp-service"'
G = 'fairness_id=~"$group"'
JG = J + ', ' + G
NS = 'namespace="maas-fairness-poc"'
EPP_POD = NS + ', pod=~"maas-vllm-gpu-kserve-router-scheduler-.*", container="main"'
VLLM = 'llm_isvc_name="maas-vllm-gpu", llm_isvc_component="workload"'
DS = {"type": "prometheus", "uid": "$datasource"}
GROUP_COLORS = {"app1": "blue", "app2": "orange", "end-users": "green", "unclassified": "#8f8f8f"}

panels, _id, _y, _x, _rowh = [], [0], [0], [0], [0]


def nid():
    _id[0] += 1
    return _id[0]


def place(w, h):
    if _x[0] + w > 24:
        _y[0] += _rowh[0]
        _x[0], _rowh[0] = 0, 0
    pos = {"h": h, "w": w, "x": _x[0], "y": _y[0]}
    _x[0] += w
    _rowh[0] = max(_rowh[0], h)
    return pos


def row(title):
    _y[0] += _rowh[0]
    _x[0], _rowh[0] = 0, 0
    panels.append({"id": nid(), "type": "row", "title": title, "collapsed": False, "panels": [],
                   "gridPos": {"h": 1, "w": 24, "x": 0, "y": _y[0]}})
    _y[0] += 1


def tgt(expr, legend="__auto", instant=False, fmt="time_series", ref=None):
    t = {"refId": ref, "datasource": DS, "expr": expr, "legendFormat": legend}
    if instant:
        t["instant"], t["range"] = True, False
    else:
        t["range"] = True
    if fmt != "time_series":
        t["format"] = fmt
    return t


def _refs(targets):
    for i, t in enumerate(targets):
        t["refId"] = t["refId"] or chr(ord("A") + i)
    return targets


def group_overrides(extra=()):
    o = [{"matcher": {"id": "byRegexp", "options": "/^%s( |$)/" % g},
          "properties": [{"id": "color", "value": {"mode": "fixed", "fixedColor": c}}]}
         for g, c in GROUP_COLORS.items()]
    return o + list(extra)


DASHED = lambda rx: {"matcher": {"id": "byRegexp", "options": rx},
                     "properties": [{"id": "custom.lineStyle", "value": {"fill": "dash", "dash": [10, 10]}}]}


def ts(title, desc, targets, unit="short", w=8, h=8, min_=None, max_=None, stack=False,
       thresholds=None, overrides=None, per_group=True, draw="line"):
    custom = {"drawStyle": draw, "lineWidth": 2, "fillOpacity": 10 if stack else 0, "showPoints": "never",
              "spanNulls": False, "stacking": {"mode": "normal" if stack else "none", "group": "A"}}
    defaults = {"unit": unit, "custom": custom}
    if min_ is not None:
        defaults["min"] = min_
    if max_ is not None:
        defaults["max"] = max_
    if thresholds:
        defaults["thresholds"] = {"mode": "absolute", "steps": thresholds}
        custom["thresholdsStyle"] = {"mode": "line+area"}
    ov = group_overrides(overrides or ()) if per_group else list(overrides or ())
    panels.append({"id": nid(), "type": "timeseries", "title": title, "description": desc,
                   "gridPos": place(w, h), "datasource": DS, "targets": _refs(targets),
                   "fieldConfig": {"defaults": defaults, "overrides": ov},
                   "options": {"legend": {"displayMode": "table", "placement": "bottom",
                                          "calcs": ["lastNotNull", "max"]},
                               "tooltip": {"mode": "multi", "sort": "desc"}}})


def stat(title, desc, targets, unit="none", w=4, h=5, mappings=None, thresholds=None, text="value",
         no_value=None, color_mode="background", calc="lastNotNull"):
    defaults = {"unit": unit, "mappings": mappings or [],
                "thresholds": {"mode": "absolute", "steps": thresholds or [{"color": "text", "value": None}]},
                "color": {"mode": "thresholds"}}
    if no_value:
        defaults["noValue"] = no_value
    panels.append({"id": nid(), "type": "stat", "title": title, "description": desc,
                   "gridPos": place(w, h), "datasource": DS, "targets": _refs(targets),
                   "fieldConfig": {"defaults": defaults, "overrides": []},
                   "options": {"reduceOptions": {"calcs": [calc], "fields": "", "values": False},
                               "textMode": text, "colorMode": color_mode, "graphMode": "none",
                               "justifyMode": "center"}})


def vmap(d):
    return [{"type": "value", "options": {k: {"text": t, "color": c, "index": i}
                                          for i, (k, (t, c)) in enumerate(d.items())}}]


def q(quantile, metric, extra=""):
    return ("histogram_quantile(%s, sum by (fairness_id, le) (rate(%s_bucket{%s%s}[$__rate_interval])))"
            % (quantile, metric, JG, extra))


# ---------------------------------------------------------------- overview
row("Run overview -- read this row first")
stat("Enforcement mode",
     "llm_d_epp_maas_fairness_enforcing: 1 = the weighted-fairness pick is honoured; 0 = shadow mode (FCFS decides, "
     "the plugin only accounts). In shadow mode observed share is NOT expected to track expected share -- judge "
     "nothing below until this says ENFORCING. Serves: every case.",
     [tgt("llm_d_epp_maas_fairness_enforcing{%s}" % J, instant=True)],
     mappings=vmap({"0": ("SHADOW", "blue"), "1": ("ENFORCING", "green")}), no_value="EPP NOT SCRAPED", w=4)
panels.append({"id": nid(), "type": "bargauge", "title": "Live configured weights",
               "description": "llm_d_epp_maas_fairness_configured_weight -- the weights the running EPP actually loaded "
                              "(echoed by the plugin, not copied from the repo). Expected at rest: app1=20, app2=10, "
                              "end-users=65, unclassified=5. A case that patches weights must show the new values here "
                              "during the run and the originals afterwards. Serves: weight-change cases, rule 3 restore check.",
               "gridPos": place(6, 5), "datasource": DS,
               "targets": _refs([tgt("sum by (fairness_id) (llm_d_epp_maas_fairness_configured_weight{%s})" % J,
                                     "{{fairness_id}}", instant=True)]),
               "fieldConfig": {"defaults": {"unit": "none", "min": 0, "color": {"mode": "fixed", "fixedColor": "purple"}},
                               "overrides": group_overrides()},
               "options": {"orientation": "horizontal", "displayMode": "basic", "showUnfilled": True,
                           "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}}})
stat("EPP build",
     "llm_d_epp_info build_ref label of the GPU EPP. Record it with every run: a result is only comparable to another "
     "run on the same build.",
     [tgt("llm_d_epp_info{%s}" % J, "{{build_ref}}", instant=True)], text="name", color_mode="none", w=4,
     no_value="EPP NOT SCRAPED")
stat("vLLM replicas (ready / desired)",
     "kube_deployment_status_replicas_ready / kube_deployment_status_replicas for maas-vllm-gpu-kserve. The system "
     "under test is 2 replicas; anything else here invalidates a share result unless the case changed it on purpose.",
     [tgt('kube_deployment_status_replicas_ready{%s, deployment="maas-vllm-gpu-kserve"}' % NS, "ready", instant=True),
      tgt('kube_deployment_status_replicas{%s, deployment="maas-vllm-gpu-kserve"}' % NS, "desired", instant=True)],
     text="value_and_name", color_mode="none", w=4)
stat("EPP restarts in range",
     "increase(kube_pod_container_status_restarts_total) for the GPU EPP container over the selected time range. "
     "Any non-zero value means the fairness counters reset mid-run and the share numbers for this range are not "
     "trustworthy (the report flags the same thing as epp_restarted).",
     [tgt("sum(increase(kube_pod_container_status_restarts_total{%s}[$__range])) or vector(0)" % EPP_POD,
          instant=True)],
     thresholds=[{"color": "green", "value": None}, {"color": "red", "value": 1}], w=3)
stat("Loadgen now",
     "sum(kube_job_status_active) over maas-loadgen* Jobs in maas-fairness-poc. Rule 1: only one benchmark on the GPU "
     "pool at a time -- check this says IDLE before starting a run.",
     [tgt('sum(kube_job_status_active{%s, job_name=~"maas-loadgen.*"}) or vector(0)' % NS, instant=True)],
     mappings=vmap({"0": ("IDLE", "green")}),
     thresholds=[{"color": "green", "value": None}, {"color": "orange", "value": 1}], w=3)

# ---------------------------------------------------------------- alerts
row("PrometheusRule alert states (deploy/prometheusrule.yaml)")
RULE_LOADED = 'count(prometheus_rule_group_rules{rule_group=~".*maas-fairness-poc-maas-fairness-alerts.*"})'
stat("Rule loaded?",
     "Whether deploy/prometheusrule.yaml (maas-fairness-alerts) is being evaluated: counts its rule group in the "
     "user-workload Thanos Ruler's prometheus_rule_group_rules. NOT LOADED means the alert tiles to the right are "
     "blank because nothing evaluates them -- not because the system is healthy. (A rule labelled "
     "openshift.io/prometheus-rule-evaluation-scope: leaf-prometheus would be evaluated by UWM Prometheus instead "
     "and would read NOT LOADED here; the repo's rule carries no such label.)",
     [tgt(RULE_LOADED + " or vector(0)", instant=True)],
     mappings=vmap({"0": ("NOT LOADED", "red")}),
     thresholds=[{"color": "red", "value": None}, {"color": "green", "value": 1}], w=4, h=4)
for name, serves in [("MaasFairnessNotConverging", "convergence / contention cases"),
                     ("MaasFairnessClassificationBroken", "classification / unclassified-traffic cases"),
                     ("MaasFairnessBandSplit", "priority-header / band cases"),
                     ("MaasFairnessSheddingIsRealAllocator", "overload / shedding cases"),
                     ("MaasFairnessAccountingLeak", "accounting / truing cases")]:
    stat(name.replace("MaasFairness", ""),
         "ALERTS{alertname=\"%s\"}: FIRING / PENDING / OK. Shows RULE NOT LOADED when the rule group is absent (see "
         "'Rule loaded?'). Firing/pending periods also appear as dashboard annotations. Serves: %s." % (name, serves),
         [tgt('(max(ALERTS{alertname="%s", alertstate="firing"}) or 0.5 * max(ALERTS{alertname="%s", '
              'alertstate="pending"}) or vector(0)) and on() (%s > 0)' % (name, name, RULE_LOADED), instant=True)],
         mappings=vmap({"0": ("OK", "green"), "0.5": ("PENDING", "orange"), "1": ("FIRING", "red")}),
         no_value="RULE NOT LOADED", w=4, h=4)

# ---------------------------------------------------------------- share
row("Delivered share: expected vs observed (the pass criterion)")
OFFERED_RANGE = "(sum by (fairness_id) (increase(llm_d_epp_request_total{%s}[$__range])) > 0)" % J
OFFERED_WIN = "(sum by (fairness_id) (increase(llm_d_epp_request_total{%s}[$window])) > 0)" % J
W = "sum by (fairness_id) (llm_d_epp_maas_fairness_configured_weight{%s})" % J


def expected(offered):
    return "100 * (%s and on (fairness_id) %s) / scalar(sum(%s and on (fairness_id) %s))" % (W, offered, W, offered)


def observed(rng):
    m = "llm_d_epp_maas_fairness_contended_service_tokens_total{%s}" % J
    return "100 * sum by (fairness_id) (increase(%s[%s])) / scalar(sum(increase(%s[%s])))" % (m, rng, m, rng)


panels.append({
    "id": nid(), "type": "table", "title": "Expected vs observed share per group (selected time range)",
    "description": "Same arithmetic as deploy/poc/15-fairness-report.py. Expected % = weight / sum of weights of the "
                   "groups that OFFERED load in the range (had any llm_d_epp_request_total increase) -- an idle group's "
                   "weight is redistributed, as work conservation requires. Observed % = the group's share of "
                   "increase(llm_d_epp_maas_fairness_contended_service_tokens_total) over the range (the design's SLI: "
                   "service only counted while contended). Deviation = observed - expected, in points; the series pass "
                   "threshold is |deviation| <= 10. Set the time range to exactly the run (see the runbook's time-range "
                   "convention) or the numbers mix runs. Single-offered-group cases have no contention by definition and "
                   "show no observed value. Serves: every share case.",
    "gridPos": place(12, 9), "datasource": DS,
    "targets": _refs([tgt(expected(OFFERED_RANGE), instant=True, fmt="table"),
                      tgt(observed("$__range"), instant=True, fmt="table"),
                      tgt("(%s) - on (fairness_id) (%s)" % (observed("$__range"), expected(OFFERED_RANGE)),
                          instant=True, fmt="table"),
                      tgt("sum by (fairness_id) (increase(llm_d_epp_request_total{%s}[$__range]))" % J,
                          instant=True, fmt="table")]),
    "transformations": [
        {"id": "merge", "options": {}},
        {"id": "organize", "options": {"excludeByName": {"Time": True},
                                       "renameByName": {"fairness_id": "Group", "Value #A": "Expected %",
                                                        "Value #B": "Observed %", "Value #C": "Deviation (pts)",
                                                        "Value #D": "Requests"},
                                       "indexByName": {"fairness_id": 0, "Value #A": 1, "Value #B": 2, "Value #C": 3,
                                                       "Value #D": 4}}}],
    "fieldConfig": {"defaults": {"decimals": 1, "unit": "none"},
                    "overrides": [{"matcher": {"id": "byName", "options": "Deviation (pts)"},
                                   "properties": [{"id": "custom.cellOptions", "value": {"type": "color-background"}},
                                                  {"id": "thresholds", "value": {"mode": "absolute", "steps": [
                                                      {"color": "red", "value": None}, {"color": "green", "value": -10},
                                                      {"color": "red", "value": 10.0001}]}}]},
                                  {"matcher": {"id": "byName", "options": "Requests"},
                                   "properties": [{"id": "decimals", "value": 0}]}]},
    "options": {"showHeader": True, "sortBy": [{"displayName": "Group"}]}})
ts("Observed vs expected share over time (window = $window)",
   "Solid = observed contended-service share in each trailing $window; dashed = expected share for the groups that "
   "offered load in that same window. A healthy enforcing policy shows each solid line settling onto its dashed line "
   "within a few windows of contention starting. Gaps = no contention in that window (nothing to share). Serves: every "
   "share case, especially ramp / bursty / arrival-order cases where the range total hides transients.",
   [tgt("%s and on (fairness_id) sum by (fairness_id) (llm_d_epp_request_total{%s})" % (observed("$window"), G),
        "{{fairness_id}} observed"),
    tgt("(%s) and on (fairness_id) sum by (fairness_id) (llm_d_epp_request_total{%s})" % (expected(OFFERED_WIN), G),
        "{{fairness_id}} expected")],
   unit="percent", w=12, h=9, min_=0, max_=100, overrides=[DASHED("/expected/")])
ts("Deviation from expected share (points, window = $window)",
   "observed - expected per group, per trailing $window. The shaded band is the series' +/-10-point pass threshold. "
   "Serves: every share case; read with the table to the left.",
   [tgt("((%s) - on (fairness_id) (%s)) and on (fairness_id) sum by (fairness_id) (llm_d_epp_request_total{%s})"
        % (observed("$window"), expected(OFFERED_WIN), G), "{{fairness_id}}")],
   unit="none", w=12, h=8,
   thresholds=[{"color": "transparent", "value": None}, {"color": "red", "value": -1000},
               {"color": "transparent", "value": -10}, {"color": "red", "value": 10}])
ts("Dispatch (request-count) share vs token share (window = $window)",
   "Solid = share of llm_d_epp_maas_fairness_dispatch_total (requests); dashed = share of contended service tokens. "
   "They diverge when groups send different request sizes -- the policy equalises tokens, not request counts, so a "
   "group with short prompts legitimately gets more requests. Serves: mixed-request-size / long-prompt cases.",
   [tgt("100 * sum by (fairness_id) (increase(llm_d_epp_maas_fairness_dispatch_total{%s}[$window])) / "
        "scalar(sum(increase(llm_d_epp_maas_fairness_dispatch_total{%s}[$window])))" % (JG, J), "{{fairness_id}} dispatch"),
    tgt("%s and on (fairness_id) sum by (fairness_id) (llm_d_epp_request_total{%s})" % (observed("$window"), G),
        "{{fairness_id}} tokens")],
   unit="percent", w=12, h=8, min_=0, max_=100, overrides=[DASHED("/tokens/")])

# ---------------------------------------------------------------- convergence
row("Convergence: normalized_service")
ts("normalized_service per group",
   "llm_d_epp_maas_fairness_normalized_service = decayed attained service / weight. Converged = the lines of all "
   "BACKLOGGED groups meet. An idle group decays toward zero and is expected to sit below the others. A persistent "
   "outlier under contention is being starved (low) or monopolising (high). Serves: convergence, newcomer, idle-return cases.",
   [tgt("max by (fairness_id) (llm_d_epp_maas_fairness_normalized_service{%s})" % JG, "{{fairness_id}}")], w=8)
ts("normalized_service spread (max / min, configured groups)",
   "The MaasFairnessNotConverging alert's left-hand side: max/min normalized_service across non-unclassified groups "
   "(min over groups > 0). The red line is the alert's 1.5x threshold; the alert also requires pool saturation and "
   "active contention. Includes idle groups, so it is only meaningful while all configured groups are backlogged. "
   "Serves: convergence cases.",
   [tgt('max(llm_d_epp_maas_fairness_normalized_service{%s, fairness_id!="unclassified"}) / '
        'min(llm_d_epp_maas_fairness_normalized_service{%s, fairness_id!="unclassified"} > 0)' % (J, J), "max / min")],
   unit="none", w=8, min_=1, per_group=False,
   thresholds=[{"color": "transparent", "value": None}, {"color": "red", "value": 1.5}])
ts("normalized_service_observed by half-life",
   "llm_d_epp_maas_fairness_normalized_service_observed: the same tab accounted through extra half-lives (20s, 120s) "
   "that do not drive decisions. The short half-life shows transients the decision half-life smooths; the long one "
   "shows whether the split holds over minutes. Serves: half-life / bursty-traffic cases.",
   [tgt("max by (fairness_id, half_life_seconds) (llm_d_epp_maas_fairness_normalized_service_observed{%s})" % JG,
        "{{fairness_id}} hl={{half_life_seconds}}s")], w=8, overrides=[DASHED("/hl=20s/")])

# ---------------------------------------------------------------- tokens
row("Service tokens: contended vs total")
ts("Contended service per group (cost units / s)",
   "rate(llm_d_epp_maas_fairness_contended_service_tokens_total): weighted service cost charged while the group's band "
   "was contended -- the numerator of the share SLI. Flat zero for a group means it never contended, not that it was "
   "unserved. Serves: every share case.",
   [tgt("sum by (fairness_id) (rate(llm_d_epp_maas_fairness_contended_service_tokens_total{%s}[$__rate_interval]))" % JG,
        "{{fairness_id}}")], w=8, stack=True)
ts("Total raw tokens per group (tokens / s, contended or not)",
   "rate of llm_d_epp_request_input_tokens_sum (dashed) and llm_d_epp_request_output_tokens_sum (solid) per group -- "
   "all traffic, contended or not. These are raw tokens, NOT the plugin's cost units (cost weights input/output/cached "
   "differently), so compare shapes with the panel to the left, not absolute values. There is no exported "
   "total-service-cost counter. Serves: work-conservation / idle-group cases.",
   [tgt("sum by (fairness_id) (rate(llm_d_epp_request_output_tokens_sum{%s}[$__rate_interval]))" % JG,
        "{{fairness_id}} output"),
    tgt("sum by (fairness_id) (rate(llm_d_epp_request_input_tokens_sum{%s}[$__rate_interval]))" % JG,
        "{{fairness_id}} input")], w=8, overrides=[DASHED("/input/")])
ts("Fraction of time contended per group",
   "rate(llm_d_epp_maas_fairness_contended_seconds_total): 1.0 = the group was backlogged alongside another group the "
   "whole time (the share SLI's denominator). Near-zero during a run means the load never created contention and the "
   "share result is vacuous. Serves: every share case (validity check).",
   [tgt("sum by (fairness_id) (rate(llm_d_epp_maas_fairness_contended_seconds_total{%s}[$__rate_interval]))" % JG,
        "{{fairness_id}}")], unit="percentunit", w=8, min_=0)

# ---------------------------------------------------------------- accounting
row("Accounting: truing error and leak detectors")
ts("Mean truing error per request (actual - estimated cost)",
   "rate(truing_error_tokens_sum) / rate(truing_error_tokens_count) per group. Symmetric noise around 0 is fine. A "
   "persistent bias means the provisional (bytes-per-token) estimate is wrong for that group's content and its tab "
   "is mis-charged until true-up. NOTE: the provisional charge itself (groupState.provisionalTotal) is NOT exported as "
   "a metric -- it is only visible in the EPP state dump -- so in-flight provisional tokens cannot be graphed. "
   "Serves: long-prompt, CJK/multimodal, max_tokens-skew cases.",
   [tgt("sum by (fairness_id) (rate(llm_d_epp_maas_fairness_truing_error_tokens_sum{%s}[$__rate_interval])) / "
        "sum by (fairness_id) (rate(llm_d_epp_maas_fairness_truing_error_tokens_count{%s}[$__rate_interval]))" % (JG, JG),
        "{{fairness_id}}")], w=8)
panels.append({"id": nid(), "type": "bargauge", "title": "Truing error distribution (selected range)",
               "description": "Non-cumulative bucket counts of llm_d_epp_maas_fairness_truing_error_tokens over the "
                              "range, all selected groups. Mass should sit in the buckets nearest 0; a fat tail on one "
                              "side is systematic over- or under-estimation. Serves: accounting cases.",
               "gridPos": place(8, 8), "datasource": DS,
               "targets": _refs([tgt("sum by (le) (increase(llm_d_epp_maas_fairness_truing_error_tokens_bucket{%s}"
                                     "[$__range]))" % JG, "{{le}}", instant=True, fmt="heatmap")]),
               "fieldConfig": {"defaults": {"unit": "short", "min": 0, "color": {"mode": "fixed", "fixedColor": "purple"}},
                               "overrides": []},
               "options": {"orientation": "vertical", "displayMode": "basic", "showUnfilled": True,
                           "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}}})
ts("Accounting-leak detector (tab grew with zero dispatches, 15m)",
   "The MaasFairnessAccountingLeak expression evaluated live: increase in normalized_service over 15m, shown only for "
   "groups with ZERO recorded dispatches in that 15m. Expected: no data, ever. Any point here means tokens were charged "
   "to a group that dispatched nothing -- BUT an isolated single point can be the true-up of a request dispatched just before the 15m window (the alert requires 15m sustained, this panel shows the raw expression). Evaluated here even when the PrometheusRule is not loaded. Serves: accounting / "
   "cancellation / idle-group cases.",
   [tgt("((llm_d_epp_maas_fairness_normalized_service{%s} - (llm_d_epp_maas_fairness_normalized_service{%s} offset 15m)) > 0)"
        " and (increase(llm_d_epp_maas_fairness_dispatch_total{%s}[15m]) == 0)" % (JG, JG, JG), "{{fairness_id}} ({{pod}})")],
   w=8)
ts("Requests without usage (expect flat zero)",
   "increase(llm_d_epp_maas_fairness_requests_without_usage_total) per $window. Non-zero = a response carried no usage "
   "block, so that group's tab stayed at the provisional estimate with no true-up (model server missing "
   "--enable-force-include-usage, or streaming without include_usage). Serves: streaming / accounting cases.",
   [tgt("sum by (fairness_id) (increase(llm_d_epp_maas_fairness_requests_without_usage_total{%s}[$window]))" % JG,
        "{{fairness_id}}")], w=8, min_=0)
ts("Newcomer clamps per group (/ min)",
   "60 * rate(llm_d_epp_maas_fairness_newcomer_clamps_total): times a returning-idle group's tab was raised to the band "
   "minimum (so it cannot burst on banked credit). A high steady rate means halfLifeSeconds is short relative to the "
   "traffic's burstiness. Serves: idle-return / on-off / newcomer cases.",
   [tgt("60 * sum by (fairness_id) (rate(llm_d_epp_maas_fairness_newcomer_clamps_total{%s}[$__rate_interval]))" % JG,
        "{{fairness_id}}")], w=8, min_=0)
ts("Cached prompt-token ratio per group",
   "llm_d_epp_maas_fairness_prompt_tokens_cached_ratio (cumulative cached / total prompt tokens). Flat zero across all "
   "groups means --enable-prompt-tokens-details is missing, not that the cache is cold. Serves: prefix-cache cases.",
   [tgt("max by (fairness_id) (llm_d_epp_maas_fairness_prompt_tokens_cached_ratio{%s})" % JG, "{{fairness_id}}")],
   unit="percentunit", w=8, min_=0)

# ---------------------------------------------------------------- classification
row("Classification")
ts("Unclassified share of requests (window = $window)",
   "rate of llm_d_epp_request_total{fairness_id=\"unclassified\"} / all requests. Red line = the "
   "MaasFairnessClassificationBroken 5% threshold. The benchmark harness offers no unclassified load unless a case "
   "sends it on purpose, so anything above 0 in other runs is misrouted traffic. Serves: classification / unknown-subscription cases.",
   [tgt('sum(rate(llm_d_epp_request_total{%s, fairness_id="unclassified"}[$window])) / '
        'sum(rate(llm_d_epp_request_total{%s}[$window]))' % (J, J), "unclassified share")],
   unit="percentunit", w=8, min_=0, per_group=False,
   thresholds=[{"color": "transparent", "value": None}, {"color": "red", "value": 0.05}])
ts("Unmatched subscriptions (per $window, expect zero)",
   "increase(llm_d_epp_maas_fairness_unmatched_subscriptions_total): requests whose subscription matched no group rule "
   "and fell to the catch-all. Unlabelled by design (subscription strings are attacker-controlled cardinality); the "
   "values are in the EPP's rate-limited log. Serves: classification cases.",
   [tgt("sum(increase(llm_d_epp_maas_fairness_unmatched_subscriptions_total{%s}[$window]))" % J, "unmatched")],
   w=8, min_=0, per_group=False)
stat("Classification totals (selected range)",
     "Unclassified requests and unmatched subscriptions over the selected range. Both should be 0 for a harness run.",
     [tgt('sum(increase(llm_d_epp_request_total{%s, fairness_id="unclassified"}[$__range])) or vector(0)' % J,
          "unclassified requests", instant=True),
      tgt("sum(increase(llm_d_epp_maas_fairness_unmatched_subscriptions_total{%s}[$__range])) or vector(0)" % J,
          "unmatched subscriptions", instant=True)],
     text="value_and_name", thresholds=[{"color": "green", "value": None}, {"color": "red", "value": 1}], w=8, h=8)

# ---------------------------------------------------------------- flow control
row("Flow control: queue depth, queue wait, shedding")
ts("Queue depth per group",
   "llm_d_epp_flow_control_queue_size: requests waiting in the EPP's flow-control queue per group. A backlogged group is "
   "one with a non-zero line here -- only backlogged groups compete. Serves: every contention case.",
   [tgt("sum by (fairness_id) (llm_d_epp_flow_control_queue_size{%s})" % JG, "{{fairness_id}}")], w=8, min_=0)
ts("Queue wait p50 / p95 per group (dispatched)",
   "histogram_quantile over llm_d_epp_flow_control_request_queue_duration_seconds{outcome=\"Dispatched\"}. The "
   "lower-weight group should wait longer under contention; a group waiting far longer than its weight implies is "
   "being starved. Serves: latency-fairness / starvation cases.",
   [tgt(q(0.95, "llm_d_epp_flow_control_request_queue_duration_seconds", ', outcome="Dispatched"'), "{{fairness_id}} p95"),
    tgt(q(0.5, "llm_d_epp_flow_control_request_queue_duration_seconds", ', outcome="Dispatched"'), "{{fairness_id}} p50")],
   unit="s", w=8, min_=0, overrides=[DASHED("/p50/")])
ts("Shed / evicted / rejected per group (req / s)",
   "rate of llm_d_epp_flow_control_request_queue_duration_seconds_count with outcome != Dispatched, by group and "
   "outcome (EvictedTTL, EvictedContextCancelled, Rejected*, ...). Evicted requests never reach the fairness policy, so "
   "if this is non-zero, eviction order -- not the weights -- is deciding who gets served. llm_d_epp_flow_control_"
   "requests_total itself carries no group label; this histogram does. Serves: overload / timeout / client-cancel cases.",
   [tgt('sum by (fairness_id, outcome) (rate(llm_d_epp_flow_control_request_queue_duration_seconds_count{%s, '
        'outcome!="Dispatched"}[$__rate_interval]))' % JG, "{{fairness_id}} {{outcome}}")], unit="reqps", w=8, min_=0)
ts("Flow-control outcomes, whole pool (req / s)",
   "rate(llm_d_epp_flow_control_requests_total) by outcome and priority band (no group label exists on this series). "
   "More than one priority value = band split (see that alert). Serves: band-split / overload cases.",
   [tgt("sum by (outcome, priority) (rate(llm_d_epp_flow_control_requests_total{%s}[$__rate_interval]))" % J,
        "{{outcome}} p{{priority}}")], unit="reqps", w=8, min_=0, per_group=False)
ts("Pool saturation and flow-control capacity",
   "llm_d_epp_flow_control_pool_saturation{stage=\"effective\"} (>= 1 = saturated: requests are queued in the EPP "
   "instead of dispatched immediately) and capacity utilisation by requests. Fairness only acts while saturated; a run "
   "that never reaches 1 never exercised the policy. Serves: every contention case (validity check).",
   [tgt("llm_d_epp_flow_control_pool_saturation{%s}" % J, "saturation {{stage}}"),
    tgt("llm_d_epp_flow_control_capacity_utilization_requests{%s}" % J, "capacity util (requests)")],
   unit="percentunit", w=8, min_=0, per_group=False,
   thresholds=[{"color": "transparent", "value": None}, {"color": "orange", "value": 1}])
ts("Queued bytes per group",
   "llm_d_epp_flow_control_queue_bytes per group: queue depth weighted by request size. A long-prompt group shows high "
   "bytes with low count. Serves: long-prompt / mixed-size cases.",
   [tgt("sum by (fairness_id) (llm_d_epp_flow_control_queue_bytes{%s})" % JG, "{{fairness_id}}")],
   unit="bytes", w=8, min_=0)

# ---------------------------------------------------------------- traffic
row("Traffic, errors and status codes")
ts("Request rate per group (req / s)",
   "rate(llm_d_epp_request_total) per group as seen by the EPP. Compare with each case's offered load (workers / "
   "Poisson rate) to confirm the loadgen actually drove what the case says. Serves: every case.",
   [tgt("sum by (fairness_id) (rate(llm_d_epp_request_total{%s}[$__rate_interval]))" % JG, "{{fairness_id}}")],
   unit="reqps", w=8, min_=0, stack=True)
ts("EPP request errors per group by error_code (req / s)",
   "rate(llm_d_epp_request_error_total) by group and error_code (e.g. ServiceUnavailable). This is the only "
   "per-group error/status signal the stack exports; HTTP codes seen by the loadgen are in its log and the report. "
   "Serves: overload / failure-injection cases.",
   [tgt("sum by (fairness_id, error_code) (rate(llm_d_epp_request_error_total{%s}[$__rate_interval]))" % JG,
        "{{fairness_id}} {{error_code}}")], unit="reqps", w=8, min_=0)
ts("Gateway HTTP status codes to the GPU pool (req / s, NOT per group)",
   "rate(istio_requests_total) from the maas-poc-gateway to the maas-vllm-gpu InferencePool service, by response_code. "
   "Istio has no fairness-group label, so this is pool-wide; use it to spot 5xx/429 bursts and attribute them with "
   "the panel to the left. Serves: overload / failure cases.",
   [tgt('sum by (response_code) (rate(istio_requests_total{destination_service_namespace="maas-fairness-poc", '
        'destination_service_name=~"maas-vllm-gpu-inference-pool.*", reporter="source"}[$__rate_interval]))',
        "HTTP {{response_code}}")], unit="reqps", w=8, min_=0, per_group=False)

# ---------------------------------------------------------------- latency
row("Latency per group")
ts("TTFT p50 / p95 per group",
   "histogram_quantile over llm_d_epp_request_ttft_seconds (EPP-measured, includes EPP queue wait). The harness sends "
   "non-streaming requests (streaming=\"false\"), for which first token arrives with the whole body -- so TTFT "
   "approximates e2e there. Serves: latency-fairness cases.",
   [tgt(q(0.95, "llm_d_epp_request_ttft_seconds"), "{{fairness_id}} p95"),
    tgt(q(0.5, "llm_d_epp_request_ttft_seconds"), "{{fairness_id}} p50")],
   unit="s", w=8, min_=0, overrides=[DASHED("/p50/")])
ts("End-to-end latency p50 / p95 per group",
   "histogram_quantile over llm_d_epp_request_duration_seconds (EPP receive -> response complete). Serves: every case "
   "(a fair share at unusable latency is not a pass in practice).",
   [tgt(q(0.95, "llm_d_epp_request_duration_seconds"), "{{fairness_id}} p95"),
    tgt(q(0.5, "llm_d_epp_request_duration_seconds"), "{{fairness_id}} p50")],
   unit="s", w=8, min_=0, overrides=[DASHED("/p50/")])
ts("Normalized time per output token p95 per group",
   "histogram_quantile(0.95) over llm_d_epp_request_ntpot_seconds. Decode-speed per group; should be roughly equal "
   "across groups (the GPU does not know about groups). A per-group gap points at batching/prefix effects, not the "
   "policy. Serves: long-output / max_tokens cases.",
   [tgt(q(0.95, "llm_d_epp_request_ntpot_seconds"), "{{fairness_id}} p95")], unit="s", w=8, min_=0)

# ---------------------------------------------------------------- vllm
row("vLLM (GPU pool: maas-vllm-gpu-kserve)")
ts("Replicas",
   "kube_deployment_status_replicas (desired) / _ready for maas-vllm-gpu-kserve, plus count of vLLM pods actually being "
   "scraped and ready endpoints the EPP sees (llm_d_epp_ready_endpoints). All four should read 2. Serves: replica-change "
   "/ pod-loss cases.",
   [tgt('kube_deployment_status_replicas{%s, deployment="maas-vllm-gpu-kserve"}' % NS, "desired"),
    tgt('kube_deployment_status_replicas_ready{%s, deployment="maas-vllm-gpu-kserve"}' % NS, "ready"),
    tgt("count(vllm:num_requests_running{%s})" % VLLM, "vLLM pods scraped"),
    tgt("llm_d_epp_ready_endpoints{%s}" % J, "EPP ready endpoints")],
   unit="none", w=6, min_=0, per_group=False)
ts("KV-cache usage per replica",
   "vllm:kv_cache_usage_perc per pod. Sustained ~100% means the GPU itself is the bottleneck and requests queue inside "
   "vLLM (outside the EPP's control). Serves: long-context / saturation cases.",
   [tgt("vllm:kv_cache_usage_perc{%s}" % VLLM, "{{pod}}")], unit="percentunit", w=6, min_=0, max_=1, per_group=False)
ts("Running / waiting requests per replica",
   "vllm:num_requests_running (solid) and vllm:num_requests_waiting (dashed) per pod. Waiting inside vLLM is queueing the "
   "fairness policy cannot reorder -- if it is large, the EPP is over-dispatching and share is decided by vLLM FCFS. "
   "Serves: every contention case.",
   [tgt("vllm:num_requests_running{%s}" % VLLM, "{{pod}} running"),
    tgt("vllm:num_requests_waiting{%s}" % VLLM, "{{pod}} waiting")],
   unit="none", w=6, min_=0, per_group=False, overrides=[DASHED("/waiting/")])
ts("vLLM-side queue time, TTFT p95 and preemptions",
   "vLLM's own view (pool-wide, no group label): p95 vllm:request_queue_time_seconds and vllm:time_to_first_token_seconds, "
   "plus preemptions/s (right axis). Serves: saturation / KV-pressure cases.",
   [tgt("histogram_quantile(0.95, sum by (le) (rate(vllm:request_queue_time_seconds_bucket{%s}[$__rate_interval])))" % VLLM,
        "vLLM queue p95"),
    tgt("histogram_quantile(0.95, sum by (le) (rate(vllm:time_to_first_token_seconds_bucket{%s}[$__rate_interval])))" % VLLM,
        "vLLM TTFT p95"),
    tgt("sum(rate(vllm:num_preemptions_total{%s}[$__rate_interval]))" % VLLM, "preemptions / s")],
   unit="s", w=6, min_=0, per_group=False,
   overrides=[{"matcher": {"id": "byName", "options": "preemptions / s"},
               "properties": [{"id": "unit", "value": "short"}, {"id": "custom.axisPlacement", "value": "right"}]}])

# ---------------------------------------------------------------- epp health
row("EPP health (maas-vllm-gpu-kserve-router-scheduler)")
ts("EPP CPU (cores)",
   "rate(container_cpu_usage_seconds_total) for the GPU EPP's main container. A pegged EPP adds scheduling latency to "
   "every group equally and can masquerade as a fairness problem. Serves: high-rate / many-tenant cases.",
   [tgt("sum by (pod) (rate(container_cpu_usage_seconds_total{%s}[$__rate_interval]))" % EPP_POD, "{{pod}}")],
   unit="none", w=6, min_=0, per_group=False)
ts("EPP memory (working set)",
   "container_memory_working_set_bytes for the GPU EPP. Steady growth across runs = per-group state not being "
   "released. Serves: many-tenant / long-soak cases.",
   [tgt("sum by (pod) (container_memory_working_set_bytes{%s})" % EPP_POD, "{{pod}}")],
   unit="bytes", w=6, min_=0, per_group=False)
ts("EPP restarts and process starts",
   "kube_pod_container_status_restarts_total for the EPP (step up = container restart; the counters behind every "
   "fairness panel reset at that moment) and minutes since process start (drops to 0 on restart or pod replacement). "
   "Serves: every case (validity), crash/upgrade cases.",
   [tgt("sum by (pod) (kube_pod_container_status_restarts_total{%s})" % EPP_POD, "{{pod}} restarts"),
    tgt("(time() - max by (pod) (process_start_time_seconds{%s})) / 60" % J, "{{pod}} uptime (min)")],
   unit="none", w=6, min_=0, per_group=False,
   overrides=[{"matcher": {"id": "byRegexp", "options": "/uptime/"},
               "properties": [{"id": "custom.axisPlacement", "value": "right"}]}])
ts("Scheduling latency p95",
   "p95 of llm_d_epp_scheduler_e2e_duration_seconds and of the maas-weighted-fairness plugin's own extension points "
   "(llm_d_epp_plugin_duration_seconds). The fairness plugin should stay well under a millisecond. Serves: high-rate / "
   "many-tenant cases.",
   [tgt("histogram_quantile(0.95, sum by (le) (rate(llm_d_epp_scheduler_e2e_duration_seconds_bucket{%s}[$__rate_interval])))" % J,
        "scheduler e2e p95"),
    tgt('histogram_quantile(0.95, sum by (le, extension_point) (rate(llm_d_epp_plugin_duration_seconds_bucket{%s, '
        'plugin_type="maas-weighted-fairness"}[$__rate_interval])))' % J, "fairness {{extension_point}} p95")],
   unit="s", w=6, min_=0, per_group=False)

dashboard = {
    "title": "MaaS Fairness - GPU EPP (maas-vllm-gpu-kserve-router-scheduler)",
    "uid": "maas-fairness-gpu-epp",
    "description": "Edge-case series dashboard (UNI-130). Set the time range to one run: see docs/runbook.md, "
                   "'Find a run on the fairness dashboard'.",
    "tags": ["maas-fairness", "gpu", "epp"],
    "timezone": "utc",
    "schemaVersion": 39,
    "version": 2,
    "editable": True,
    "graphTooltip": 1,
    "refresh": "30s",
    "time": {"from": "now-1h", "to": "now"},
    "links": [],
    "templating": {"list": [
        {"name": "datasource", "type": "datasource", "label": "Datasource", "query": "prometheus", "current": {},
         "hide": 0, "refresh": 1},
        {"name": "group", "type": "query", "label": "Group", "datasource": DS,
         "definition": "label_values(llm_d_epp_maas_fairness_configured_weight{%s}, fairness_id)" % J,
         "query": {"query": "label_values(llm_d_epp_maas_fairness_configured_weight{%s}, fairness_id)" % J,
                   "refId": "group"},
         "refresh": 2, "multi": True, "includeAll": True, "allValue": ".*",
         "current": {"selected": True, "text": ["All"], "value": ["$__all"]}, "sort": 1, "hide": 0},
        {"name": "window", "type": "interval", "label": "Share window", "query": "1m,2m,5m,10m,15m",
         "current": {"selected": True, "text": "2m", "value": "2m"}, "auto": False, "hide": 0,
         "options": [{"selected": v == "2m", "text": v, "value": v} for v in ["1m", "2m", "5m", "10m", "15m"]]},
    ]},
    "annotations": {"list": [
        {"builtIn": 1, "datasource": {"type": "grafana", "uid": "-- Grafana --"}, "enable": True, "hide": True,
         "iconColor": "rgba(0, 211, 255, 1)", "name": "Annotations & Alerts", "type": "dashboard"},
        {"name": "Loadgen job running", "datasource": DS, "enable": True, "iconColor": "blue", "step": "15s",
         "expr": 'max by (job_name) (kube_job_status_active{%s, job_name=~"maas-loadgen.*"}) > 0' % NS,
         "titleFormat": "loadgen running", "textFormat": "Job {{job_name}}", "tagKeys": "job_name"},
        {"name": "EPP process start", "datasource": DS, "enable": True, "iconColor": "red", "step": "60s",
         "expr": "max by (pod) (process_start_time_seconds{%s}) * 1000" % J, "useValueForTime": True,
         "titleFormat": "EPP started", "textFormat": "{{pod}} -- fairness counters reset here", "tagKeys": "pod"},
        {"name": "Weights / enforcement changed", "datasource": DS, "enable": True, "iconColor": "purple",
         "step": "30s",
         "expr": "(changes(llm_d_epp_maas_fairness_configured_weight{%s}[1m]) > 0) or "
                 "(changes(llm_d_epp_maas_fairness_enforcing{%s}[1m]) > 0)" % (J, J),
         "titleFormat": "config changed", "textFormat": "{{__name__}} {{fairness_id}}", "tagKeys": "fairness_id"},
        {"name": "vLLM replica change", "datasource": DS, "enable": True, "iconColor": "orange", "step": "30s",
         "expr": 'changes(kube_deployment_status_replicas_ready{%s, deployment="maas-vllm-gpu-kserve"}[1m]) > 0' % NS,
         "titleFormat": "vLLM ready replicas changed"},
        {"name": "MaaS fairness alerts firing", "datasource": DS, "enable": True, "iconColor": "dark-red",
         "step": "30s", "expr": 'ALERTS{alertname=~"MaasFairness.*", alertstate="firing"}',
         "titleFormat": "{{alertname}} firing", "tagKeys": "alertname,severity"},
    ]},
    "panels": panels,
}
text = json.dumps(dashboard, indent=2) + "\n"
if sys.argv[1:] == ["--write"]:
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grafana-dashboard.yaml")
    marker = "  maas-fairness-gpu-epp.json: |\n"
    head = open(path).read().split(marker, 1)[0]
    body = "".join(("    " + l) if l.strip() else l for l in text.splitlines(keepends=True))
    open(path, "w").write(head + marker + body)
else:
    sys.stdout.write(text)
