#!/usr/bin/env python3
"""Tests for 15-fairness-report.py against synthetic metrics snapshots and a
synthetic loadgen.log -- no cluster, no GPU session. This is what UNI-54's
"done when" bar means by "a test shows the FAIL path actually fails": feed a
deliberately skewed input and confirm the verdict is FAIL with a non-zero
process exit, not just that the happy path parses.

Run: python3 -I 15-fairness-report-test.py
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("fairness_report", os.path.join(HERE, "15-fairness-report.py"))
fairness_report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fairness_report)

CONFIGURED_WEIGHT = (
    'llm_d_epp_maas_fairness_configured_weight{fairness_id="app1"} 20\n'
    'llm_d_epp_maas_fairness_configured_weight{fairness_id="app2"} 10\n'
    'llm_d_epp_maas_fairness_configured_weight{fairness_id="end-users"} 65\n'
    'llm_d_epp_maas_fairness_configured_weight{fairness_id="unclassified"} 5\n'
)
ENFORCING_ON = 'llm_d_epp_maas_fairness_enforcing 1\n'


def write(tmp, name, content):
    path = os.path.join(tmp, name)
    with open(path, "w") as f:
        f.write(content)
    return path


def loadgen_log(tenants, w_app1, w_app2, w_end, duration, rows, w_custom=None, groups_line=None):
    custom_field = f"custom={w_custom} " if w_custom is not None else ""
    lines = [f"load: tenants=[{tenants}] workers app1={w_app1} app2={w_app2} end-users={w_end} {custom_field}duration={duration}s"]
    if groups_line is not None:
        lines.append(groups_line)
    lines.append("load: done.")
    lines.append(f"{'TENANT':<12} {'TOTAL':<7} {'P50_SEC':<9} {'P95_SEC':<9} STATUSES")
    for group, total, p50, p95, statuses in rows:
        lines.append(f"{group:<12} {total:<7} {p50:<9} {p95:<9} {statuses}")
    lines.append("A run is only meaningful if the statuses are overwhelmingly 200.")
    return "\n".join(lines) + "\n"


def run_build(tmp, *, tokens_before, tokens_after, tenants, w_app1, w_app2, w_end,
              rows, threshold_points=10.0, duration=240, scenario="test-scenario",
              control=False, w_custom=None):
    before = write(tmp, "before.txt", CONFIGURED_WEIGHT + ENFORCING_ON + tokens_before)
    after = write(tmp, "after.txt", CONFIGURED_WEIGHT + ENFORCING_ON + tokens_after)
    log = write(tmp, "loadgen.log", loadgen_log(tenants, w_app1, w_app2, w_end, duration, rows, w_custom=w_custom))
    return fairness_report.build_report(
        scenario=scenario,
        enforce=True,
        duration_seconds=duration,
        backend="vllm-gpu",
        epp_image_digest="sha256:deadbeef",
        namespace="maas-fairness-poc",
        epp_pod="maas-vllm-gpu-kserve-router-scheduler-test",
        run_start="2026-10-29T00:00:00Z",
        run_end="2026-10-29T00:04:00Z",
        threshold_points=threshold_points,
        metrics_before_path=before,
        metrics_after_path=after,
        loadgen_log_path=log,
        control=control,
    )


# UNI-137 (B5): deploy/poc/13-loadgen-poisson.py's own log shape -- a Poisson
# rate (req/s) per group, not a worker count, and a "sent=... codes=[...]"
# summary line per group instead of the closed-loop TENANT/TOTAL/.../STATUSES
# table. See parse_loadgen_log's OPEN_LOOP_TENANTS_LINE/OPEN_LOOP_ROW.
def open_loop_loadgen_log(rate_app1, rate_app2, rate_end, duration, rows, seed=1):
    lines = [
        f"load: open-loop Poisson arrivals rate app1={rate_app1}/s app2={rate_app2}/s "
        f"end-users={rate_end}/s duration={duration}s seed={seed}"
    ]
    lines.append("load: done.")
    for group, sent, completion_tokens, p50, p95, p99, codes in rows:
        lines.append(
            f"{group:12s} sent={sent:<6d} completion_tokens={completion_tokens:<8d} "
            f"p50={p50:.2f}s p95={p95:.2f}s p99={p99:.2f}s codes=[{codes}]"
        )
    return "\n".join(lines) + "\n"


def run_build_open_loop(tmp, *, tokens_before, tokens_after, rate_app1, rate_app2, rate_end,
                         rows, threshold_points=10.0, duration=240, scenario="b5-open-loop",
                         contended_seconds_before="", contended_seconds_after=""):
    before = write(tmp, "before.txt", CONFIGURED_WEIGHT + ENFORCING_ON + tokens_before + contended_seconds_before)
    after = write(tmp, "after.txt", CONFIGURED_WEIGHT + ENFORCING_ON + tokens_after + contended_seconds_after)
    log = write(tmp, "loadgen.log", open_loop_loadgen_log(rate_app1, rate_app2, rate_end, duration, rows))
    return fairness_report.build_report(
        scenario=scenario,
        enforce=True,
        duration_seconds=duration,
        backend="vllm-gpu (real)",
        epp_image_digest="sha256:deadbeef",
        namespace="maas-fairness-poc",
        epp_pod="maas-vllm-gpu-kserve-router-scheduler-test",
        run_start="2026-11-01T00:00:00Z",
        run_end="2026-11-01T00:04:00Z",
        threshold_points=threshold_points,
        metrics_before_path=before,
        metrics_after_path=after,
        loadgen_log_path=log,
    )


def test_converged_run_passes():
    with tempfile.TemporaryDirectory() as tmp:
        # Delivered shares land within ~1 point of the contention-adjusted
        # target (20/10/65, all three offered and contending).
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 1000\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 1000\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 1000\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 3100\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 2000\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 7900\n'
        )
        rows = [
            ("app1", 500, "1.20", "2.40", "200=500"),
            ("app2", 480, "1.30", "2.50", "200=480"),
            ("end-users", 510, "1.10", "2.30", "200=510"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 app2 end-users", w_app1=32, w_app2=32, w_end=32, rows=rows,
        )
        assert report["verdict"]["result"] == "PASS", report["verdict"]
        by_group = {g["group"]: g for g in report["groups"]}
        # offered weight total is 20+10+65=95, so expected shares are
        # 21.05/10.53/68.42, not the raw 20/10/65.
        assert abs(by_group["app1"]["expected_share_pct"] - (2000 / 9500 * 100)) < 1e-6
        assert by_group["app1"]["deviation_pts"] is not None
        assert abs(by_group["app1"]["deviation_pts"]) < 2
        assert abs(by_group["end-users"]["deviation_pts"]) < 2
        # unclassified was never offered: no expected/observed share, present
        # in the row list for completeness.
        assert by_group["unclassified"]["offered"] is False
        assert by_group["unclassified"]["expected_share_pct"] is None
        assert by_group["unclassified"]["observed_share_pct"] is None


def test_worker_sizing_proportional_to_weights_is_non_discriminating():
    # UNI-225: app2-idle's actual historical sizing (20:65 weight ratio,
    # workers sized 32:104 -- exactly the same ratio) landed close to its own
    # target, which is a PASS by the symmetric threshold but cannot tell "the
    # split follows the weights" apart from "the split follows the workers"
    # -- the two hypotheses predict the identical split here. Mirrors A3 from
    # the ticket's own table (worker share == weight share, 0.0pt gap).
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
        )
        # app1:end-users delivered 2350:7650 (the 20:65 renormalized target,
        # 23.5%/76.5%), landing on expected_share_pct almost exactly.
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 2350\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 7650\n'
        )
        rows = [
            ("app1", 235, "1.20", "2.40", "200=235"),
            ("end-users", 765, "1.10", "2.30", "200=765"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 end-users", w_app1=32, w_app2=0, w_end=104, rows=rows,
        )
        assert report["verdict"]["result"] == "PASS", report["verdict"]
        assert report["verdict"]["discriminating"] is False, report["verdict"]
        assert report["verdict"]["max_worker_vs_weight_gap_points"] < 1.0, report["verdict"]
        assert any("NON-DISCRIMINATING" in r for r in report["verdict"]["reasons"]), report["verdict"]["reasons"]
        by_group = {g["group"]: g for g in report["groups"]}
        assert abs(by_group["app1"]["worker_share_pct"] - by_group["app1"]["expected_share_pct"]) < 1e-6
        assert abs(by_group["app1"]["worker_vs_weight_gap_pts"]) < 1e-6


def test_worker_sizing_divergent_from_weights_is_discriminating():
    # UNI-225: same 20:65 weight pair as above, but sized with EQUAL workers
    # (32:32) instead of proportionally -- a worker-share prediction of
    # 50/50 against a weight-share target of 23.5/76.5 is a 26.5pt gap, well
    # over the 10pt bar. The observed split still lands on the configured
    # weights (PASS), and -- unlike the proportional sizing above -- that
    # PASS is now real evidence weights, not worker count, drove the split.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 2350\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 7650\n'
        )
        rows = [
            ("app1", 235, "1.20", "2.40", "200=235"),
            ("end-users", 765, "1.10", "2.30", "200=765"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 end-users", w_app1=32, w_app2=0, w_end=32, rows=rows,
        )
        assert report["verdict"]["result"] == "PASS", report["verdict"]
        assert report["verdict"]["discriminating"] is True, report["verdict"]
        assert report["verdict"]["max_worker_vs_weight_gap_points"] > 10.0, report["verdict"]
        assert not any("NON-DISCRIMINATING" in r for r in report["verdict"]["reasons"]), report["verdict"]["reasons"]
        by_group = {g["group"]: g for g in report["groups"]}
        assert abs(by_group["app1"]["worker_share_pct"] - 50.0) < 1e-6


def test_discriminating_is_none_for_solo_control_and_uncontended():
    # UNI-225: there is no weights-vs-workers question to ask about a run
    # that never reaches the symmetric deviation check in the first place --
    # mirrors the same three carve-outs (solo, control, UNCONTENDED) the
    # deviation check itself already has.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = 'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
        tokens_after = 'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 1000\n'
        rows = [("app1", 500, "1.20", "2.40", "200=500")]
        solo_report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1", w_app1=32, w_app2=0, w_end=0, rows=rows,
        )
        assert solo_report["verdict"]["discriminating"] is None, solo_report["verdict"]

    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 3100\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 3070\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 3830\n'
        )
        rows = [
            ("app1", 500, "1.20", "2.40", "200=500"),
            ("app2", 490, "1.30", "2.50", "200=490"),
            ("end-users", 510, "1.10", "2.30", "200=510"),
        ]
        control_report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 app2 end-users", w_app1=32, w_app2=32, w_end=32, rows=rows,
            scenario="equal-workers-control", control=True,
        )
        assert control_report["verdict"]["discriminating"] is None, control_report["verdict"]

    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app1"} 10.0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app2"} 10.0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="end-users"} 10.0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 40\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 35\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 90\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app1"} 10.2\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app2"} 10.1\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="end-users"} 10.3\n'
        )
        rows = [
            ("app1", 180, "0.80", "1.00", "200=180"),
            ("app2", 180, "0.80", "1.00", "200=180"),
            ("end-users", 780, "0.80", "1.00", "200=780"),
        ]
        uncontended_report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 app2 end-users", w_app1=6, w_app2=6, w_end=26, rows=rows,
        )
        assert uncontended_report["verdict"]["result"] == "UNCONTENDED", uncontended_report["verdict"]
        assert uncontended_report["verdict"]["discriminating"] is None, uncontended_report["verdict"]


def test_request_share_pct_matches_token_share_when_requests_are_uniform():
    # UNI-146 (C1): when every group's per-request token cost is the same
    # (every scenario before this ticket), request count and delivered
    # tokens scale together, so the request-count split and the
    # weighted-token split should be the same number. 100 tokens/request for
    # all three groups: token deltas 2100/1000/6900 (sum 10000) imply
    # requests 21/10/69 (sum 100).
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 2100\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 1000\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 6900\n'
        )
        rows = [
            ("app1", 21, "1.20", "2.40", "200=21"),
            ("app2", 10, "1.30", "2.50", "200=10"),
            ("end-users", 69, "1.10", "2.30", "200=69"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 app2 end-users", w_app1=32, w_app2=32, w_end=32, rows=rows,
        )
        assert report["verdict"]["result"] == "PASS", report["verdict"]
        by_group = {g["group"]: g for g in report["groups"]}
        for gid in ("app1", "app2", "end-users"):
            assert by_group[gid]["request_share_pct"] is not None
            assert abs(by_group[gid]["request_share_pct"] - by_group[gid]["observed_share_pct"]) < 1.0
            assert abs(by_group[gid]["request_share_deviation_pts"] - by_group[gid]["deviation_pts"]) < 1.0


def test_request_share_pct_diverges_from_token_share_on_asymmetric_requests():
    # UNI-146's actual case: app1 sends few, expensive (long-prompt) requests
    # and end-users sends many, cheap-looking (short-prompt) requests, but
    # end-users' completions are long enough that it still earns the
    # majority of weighted tokens. Request count alone would say the split
    # went the other way -- exactly the cost-model error this ticket exists
    # to catch, and exactly why a report that only showed request count
    # would hide it.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
        )
        # app1: weight 20, end-users: weight 65 -- renormalized target
        # 23.5%/76.5%. Token delta matches that target closely.
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 2350\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 7650\n'
        )
        # But app1 sent far MORE requests than end-users (short completions,
        # fast turnaround) while delivering fewer weighted tokens -- request
        # count alone would say app1 dominates (90%), the opposite of the
        # token-weighted truth.
        rows = [
            ("app1", 900, "0.40", "0.80", "200=900"),
            ("end-users", 100, "6.00", "9.00", "200=100"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 end-users", w_app1=32, w_app2=0, w_end=104, rows=rows,
        )
        assert report["verdict"]["result"] == "PASS", report["verdict"]
        by_group = {g["group"]: g for g in report["groups"]}
        # Token-weighted split meets the target within a couple of points.
        assert abs(by_group["app1"]["deviation_pts"]) < 2
        assert abs(by_group["end-users"]["deviation_pts"]) < 2
        # Request-count split tells a completely different, and wrong, story.
        assert by_group["app1"]["request_share_pct"] == 90.0
        assert by_group["end-users"]["request_share_pct"] == 10.0
        assert by_group["app1"]["request_share_deviation_pts"] > 60
        assert by_group["end-users"]["request_share_deviation_pts"] < -60
        # The two methods must actually disagree here, which is the point.
        assert abs(by_group["app1"]["request_share_pct"] - by_group["app1"]["observed_share_pct"]) > 50


def test_skewed_run_fails_and_cli_exits_nonzero():
    # Deliberately skewed input: app1 (weight 20) captures almost everything,
    # end-users (weight 65) is nearly starved -- the kind of result that
    # would mean the policy is not enforcing, or enforcing backwards.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 9000\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 500\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 500\n'
        )
        rows = [
            ("app1", 900, "0.50", "0.90", "200=900"),
            ("app2", 480, "1.30", "2.50", "200=480"),
            ("end-users", 490, "4.10", "9.30", "200=490"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 app2 end-users", w_app1=32, w_app2=32, w_end=32, rows=rows,
        )
        assert report["verdict"]["result"] == "FAIL", report["verdict"]
        assert report["verdict"]["max_abs_deviation_points"] > 10
        assert report["verdict"]["reasons"], "FAIL verdict must say why"

        # And the actual CLI, not just the library function, must exit
        # non-zero on this input -- that is the literal done-when bar.
        before = write(tmp, "before.txt", CONFIGURED_WEIGHT + ENFORCING_ON + tokens_before)
        after = write(tmp, "after.txt", CONFIGURED_WEIGHT + ENFORCING_ON + tokens_after)
        log = write(tmp, "loadgen.log", loadgen_log("app1 app2 end-users", 32, 32, 32, 240, rows))
        out_json = os.path.join(tmp, "report.json")
        out_md = os.path.join(tmp, "report.md")
        proc = subprocess.run(
            [sys.executable, "-I", os.path.join(HERE, "15-fairness-report.py"),
             "--scenario", "full-contention", "--enforce", "true",
             "--backend", "vllm-gpu", "--epp-image-digest", "sha256:deadbeef",
             "--namespace", "maas-fairness-poc", "--epp-pod", "test-pod",
             "--run-start", "2026-10-29T00:00:00Z", "--run-end", "2026-10-29T00:04:00Z",
             "--metrics-before", before, "--metrics-after", after, "--loadgen-log", log,
             "--out-json", out_json, "--out-md", out_md],
            capture_output=True, text=True,
        )
        assert proc.returncode != 0, f"expected non-zero exit, got {proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"
        assert "FAIL" in proc.stdout
        assert os.path.exists(out_json) and os.path.exists(out_md), "report must still be written on FAIL"


def test_end_users_idle_absorbed_not_reserved_passes():
    # The work-conservation scenario this ticket names explicitly: end-users
    # sends no load at all. app1:app2 should split close to their 2:1 weight
    # ratio over the FULL pool (66.7/33.3), not be held near 20%/10% with the
    # rest going nowhere. A naive "share of all configured weight" target
    # would wrongly flag this as a huge deviation; the contention-adjusted
    # target must not.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 6650\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 3350\n'
        )
        rows = [
            ("app1", 500, "1.20", "2.40", "200=500"),
            ("app2", 490, "1.30", "2.50", "200=490"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 app2", w_app1=32, w_app2=32, w_end=0, rows=rows,
        )
        assert report["verdict"]["result"] == "PASS", report["verdict"]
        by_group = {g["group"]: g for g in report["groups"]}
        assert abs(by_group["app1"]["expected_share_pct"] - (20 / 30 * 100)) < 1e-6
        assert by_group["end-users"]["offered"] is False
        assert by_group["end-users"]["expected_share_pct"] is None


def test_solo_group_passes_on_success_rate_not_token_share():
    # app1-alone: nobody else is offered, so contended_service_tokens_total
    # is correctly a flat zero delta (metrics.go -- it only accrues under
    # contention). That must NOT be scored as a 100-point deviation; the
    # solo scenario's bar is "overwhelmingly 200", not a token share.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = 'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 500\n'
        tokens_after = 'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 500\n'
        rows = [("app1", 5400, "1.40", "1.80", "200=5391 500=9")]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1", w_app1=32, w_app2=0, w_end=0, rows=rows,
        )
        assert report["verdict"]["result"] == "PASS", report["verdict"]
        assert report["verdict"]["solo_group"] == "app1"
        by_group = {g["group"]: g for g in report["groups"]}
        assert by_group["app1"]["delivered_tokens"] == 0.0
        assert by_group["app1"]["expected_share_pct"] is None
        assert by_group["app1"]["observed_share_pct"] is None
        assert by_group["app1"]["deviation_pts"] is None


def test_tenants_line_tolerates_custom_identity_field():
    # UNI-129 added a `custom=N` field to 04-loadgen.yaml's run.sh log line,
    # between `end-users=N` and `duration=Ns`. Found on UNI-131: the real
    # loadgen.log (which always includes this field now) stopped matching
    # TENANTS_LINE entirely, so offered_workers silently fell back to all
    # zeros and every run reported "no group was offered any load" instead
    # of the correct verdict. This must parse exactly like the no-custom-
    # field case.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = 'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 500\n'
        tokens_after = 'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 500\n'
        rows = [("app2", 5403, "1.40", "1.70", "200=5385 500=18")]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app2", w_app1=32, w_app2=32, w_end=32, rows=rows, w_custom=32,
        )
        assert report["verdict"]["result"] == "PASS", report["verdict"]
        assert report["verdict"]["solo_group"] == "app2"
        by_group = {g["group"]: g for g in report["groups"]}
        assert by_group["app2"]["offered_workers"] == 32


def test_solo_group_fails_on_low_success_rate():
    # Same uncontended shape, but this time the solo tenant is mostly
    # failing -- that must still FAIL, on the success-rate bar.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = 'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
        tokens_after = 'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
        rows = [("app1", 1000, "1.40", "9.80", "200=400 500=600")]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1", w_app1=32, w_app2=0, w_end=0, rows=rows,
        )
        assert report["verdict"]["result"] == "FAIL", report["verdict"]
        assert any("success" in r or "200" in r for r in report["verdict"]["reasons"]) or report["verdict"]["reasons"]


def test_asymmetric_demand_saturating_group_above_nominal_passes():
    # app1 saturates (32 workers), app2 is idle, end-users trickles (2
    # workers) and is structurally incapable of reaching a weight-
    # proportional 76.5% share. app1 taking the lion's share (far above its
    # own 23.5% nominal weight) is the CORRECT, intended outcome for this
    # scenario, not a huge deviation to fail on. (Real numbers from a live
    # GPU run, 2026-10-29.)
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 5557384\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 343636\n'
        )
        rows = [
            ("app1", 5164, "1.50", "1.90", "200=5103 500=61"),
            ("end-users", 269, "1.80", "2.10", "200=267 500=2"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 end-users", w_app1=32, w_app2=0, w_end=2, rows=rows,
            scenario="asymmetric-demand",
        )
        assert report["verdict"]["result"] == "PASS", report["verdict"]
        by_group = {g["group"]: g for g in report["groups"]}
        assert by_group["app1"]["deviation_pts"] > 50  # far above nominal -- expected and fine here


def test_asymmetric_demand_saturating_group_capped_fails():
    # Same shape, but this time app1 (32 workers, idle app2, trickling
    # end-users) delivers LESS than its own nominal weight share -- weight is
    # acting as a ceiling on the group with spare demand, which is the actual
    # defect this scenario exists to catch, and must still FAIL.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
        )
        tokens_after = (
            # app1 (nominal 23.5%) held to 10%; end-users's queue drained far
            # past what its 2 workers should earn, which is implausible for a
            # genuinely demand-capped group and indicates app1 is being capped.
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 1000\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 9000\n'
        )
        rows = [
            ("app1", 5164, "1.50", "1.90", "200=5103 500=61"),
            ("end-users", 269, "1.80", "2.10", "200=267 500=2"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 end-users", w_app1=32, w_app2=0, w_end=2, rows=rows,
            scenario="asymmetric-demand",
        )
        assert report["verdict"]["result"] == "FAIL", report["verdict"]
        assert report["verdict"]["reasons"]


def test_app2_trickle_served_and_pair_split_passes():
    # UNI-134: A5. app1/end-users are HARD (32/104 workers) and split the
    # pool in their own 20:65 ratio, renormalized to 23.5/76.5 -- app2's
    # weight (10) must NOT be folded into that denominator even though app2
    # is offered (2 workers), or the target would wrongly become 21.1/68.4.
    # app2 itself is mostly 200s (served, not throttled below its own
    # trickle demand).
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 2350000\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 150000\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 7650000\n'
        )
        rows = [
            ("app1", 5000, "1.50", "1.90", "200=4950 500=50"),
            ("app2", 300, "0.90", "1.10", "200=297 500=3"),
            ("end-users", 16000, "1.60", "2.00", "200=15840 500=160"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 app2 end-users", w_app1=32, w_app2=2, w_end=104, rows=rows,
            scenario="app2-trickle",
        )
        assert report["verdict"]["result"] == "PASS", report["verdict"]
        assert report["verdict"]["capped_groups"] == ["app2"]
        by_group = {g["group"]: g for g in report["groups"]}
        assert abs(by_group["app1"]["expected_share_pct"] - 23.529) < 0.01
        assert abs(by_group["end-users"]["expected_share_pct"] - 76.470) < 0.01
        assert by_group["app2"]["expected_share_pct"] is None  # excluded, not scored as a share


def test_app2_trickle_throttled_capped_group_fails():
    # Same pair split (still a clean 23.5/76.5), but app2's own requests are
    # now mostly failing -- its weight floor did not protect its trickle
    # demand. The pair passing its own check must not mask this.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 2350000\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 20000\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 7650000\n'
        )
        rows = [
            ("app1", 5000, "1.50", "1.90", "200=4950 500=50"),
            ("app2", 300, "5.90", "9.10", "200=90 500=210"),
            ("end-users", 16000, "1.60", "2.00", "200=15840 500=160"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 app2 end-users", w_app1=32, w_app2=2, w_end=104, rows=rows,
            scenario="app2-trickle",
        )
        assert report["verdict"]["result"] == "FAIL", report["verdict"]
        assert any("app2" in r for r in report["verdict"]["reasons"]), report["verdict"]["reasons"]


def test_control_scenario_reports_info_not_scored():
    # UNI-103: equal-workers-control reuses the exact equal-worker shape that
    # produced the pre-resize FAIL (31/30.7/38.3 against 20/10/65 on this
    # backend -- docs/poc-results.md). Run as --control, that large deviation
    # must NOT become a FAIL or a PASS -- it is the control's expected,
    # correct-for-its-purpose result, so the verdict is INFO and the reasons
    # say so without claiming the weighted split held.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 3100\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 3070\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 3830\n'
        )
        rows = [
            ("app1", 500, "1.20", "2.40", "200=500"),
            ("app2", 490, "1.30", "2.50", "200=490"),
            ("end-users", 510, "1.10", "2.30", "200=510"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 app2 end-users", w_app1=32, w_app2=32, w_end=32, rows=rows,
            scenario="equal-workers-control", control=True,
        )
        assert report["verdict"]["result"] == "INFO", report["verdict"]
        assert report["verdict"]["max_abs_deviation_points"] > 10
        assert any("not scored" in r for r in report["verdict"]["reasons"]), report["verdict"]["reasons"]

        # The CLI must exit 0 for a control even though the deviation would
        # FAIL a scored scenario -- it must not break a pipeline gating on
        # this script's exit code.
        before = write(tmp, "before2.txt", CONFIGURED_WEIGHT + ENFORCING_ON + tokens_before)
        after = write(tmp, "after2.txt", CONFIGURED_WEIGHT + ENFORCING_ON + tokens_after)
        log = write(tmp, "loadgen2.log", loadgen_log("app1 app2 end-users", 32, 32, 32, 240, rows))
        out_json = os.path.join(tmp, "control-report.json")
        out_md = os.path.join(tmp, "control-report.md")
        proc = subprocess.run(
            [sys.executable, "-I", os.path.join(HERE, "15-fairness-report.py"),
             "--scenario", "equal-workers-control", "--enforce", "true", "--control",
             "--backend", "vllm-gpu", "--epp-image-digest", "sha256:deadbeef",
             "--namespace", "maas-fairness-poc", "--epp-pod", "test-pod",
             "--run-start", "2026-10-29T00:00:00Z", "--run-end", "2026-10-29T00:04:00Z",
             "--metrics-before", before, "--metrics-after", after, "--loadgen-log", log,
             "--out-json", out_json, "--out-md", out_md],
            capture_output=True, text=True,
        )
        assert proc.returncode == 0, f"expected zero exit for a control, got {proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"
        assert "INFO" in proc.stdout


def test_uncontended_when_everyone_below_capacity():
    # UNI-135: A6 "below capacity, everyone light" -- all three tenants
    # offered at well under their own saturating worker counts (6/6/26 vs.
    # full-contention's 32/32/128). Nobody is ever backlogged alongside
    # anyone else, so contended_seconds_total stays near zero for every
    # offered group -- and so does contended_service_tokens_total, since both
    # metrics share the same contention gate (metrics.go). That near-zero
    # tokens total must NOT be read as "the EPP accounted nothing" (a
    # structural FAIL elsewhere in this file); it is this scenario's correct,
    # expected signature.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app1"} 10.0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app2"} 10.0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="end-users"} 10.0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 40\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 35\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 90\n'
            # Deltas of 0.1-0.3s -- an order of magnitude below the ~9s a
            # genuinely-contending tenant accrues in full-contention.
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app1"} 10.2\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app2"} 10.1\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="end-users"} 10.3\n'
        )
        rows = [
            ("app1", 180, "0.80", "1.00", "200=180"),
            ("app2", 180, "0.80", "1.00", "200=180"),
            ("end-users", 780, "0.80", "1.00", "200=780"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 app2 end-users", w_app1=6, w_app2=6, w_end=26, rows=rows,
            scenario="below-capacity",
        )
        assert report["verdict"]["result"] == "UNCONTENDED", report["verdict"]
        assert not report["verdict"]["reasons"][0].startswith("offered groups delivered zero")
        assert any("contended_seconds_total" in r for r in report["verdict"]["reasons"])
        by_group = {g["group"]: g for g in report["groups"]}
        assert abs(by_group["app1"]["contended_seconds"] - 0.2) < 1e-6
        assert abs(by_group["app2"]["contended_seconds"] - 0.1) < 1e-6
        assert abs(by_group["end-users"]["contended_seconds"] - 0.3) < 1e-6

        # The CLI must exit 0 for UNCONTENDED, same as PASS/INFO.
        before = write(tmp, "before2.txt", CONFIGURED_WEIGHT + ENFORCING_ON + tokens_before)
        after = write(tmp, "after2.txt", CONFIGURED_WEIGHT + ENFORCING_ON + tokens_after)
        log = write(tmp, "loadgen2.log", loadgen_log("app1 app2 end-users", 6, 6, 26, 240, rows))
        out_json = os.path.join(tmp, "uncontended-report.json")
        out_md = os.path.join(tmp, "uncontended-report.md")
        proc = subprocess.run(
            [sys.executable, "-I", os.path.join(HERE, "15-fairness-report.py"),
             "--scenario", "below-capacity", "--enforce", "true",
             "--backend", "vllm-gpu", "--epp-image-digest", "sha256:deadbeef",
             "--namespace", "maas-fairness-poc", "--epp-pod", "test-pod",
             "--run-start", "2026-10-29T00:00:00Z", "--run-end", "2026-10-29T00:04:00Z",
             "--metrics-before", before, "--metrics-after", after, "--loadgen-log", log,
             "--out-json", out_json, "--out-md", out_md],
            capture_output=True, text=True,
        )
        assert proc.returncode == 0, f"expected zero exit for UNCONTENDED, got {proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"
        assert "UNCONTENDED" in proc.stdout


def test_uncontended_does_not_apply_when_one_group_actually_contends():
    # Same light-weight shape as above, but app1's contended_seconds delta
    # (8.5s) is in full-contention's genuinely-contending range while app2/
    # end-users stay near zero -- "below capacity, everyone light" does not
    # hold (app1 is NOT light here), so this must fall through to the normal
    # symmetric deviation scoring instead of being misclassified UNCONTENDED.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app1"} 0.0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app2"} 0.0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="end-users"} 0.0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 2105\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 1038\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 6857\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app1"} 8.5\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app2"} 0.2\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="end-users"} 0.3\n'
        )
        rows = [
            ("app1", 180, "0.80", "1.00", "200=180"),
            ("app2", 180, "0.80", "1.00", "200=180"),
            ("end-users", 780, "0.80", "1.00", "200=780"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 app2 end-users", w_app1=6, w_app2=6, w_end=26, rows=rows,
            scenario="below-capacity",
        )
        assert report["verdict"]["result"] != "UNCONTENDED", report["verdict"]


def test_uncontended_does_not_override_solo_or_control():
    # A solo group's contended_seconds_total is correctly, always zero
    # (nobody to contend against) -- that must still be judged on the
    # success-rate bar the `solo` case already uses, not relabelled
    # UNCONTENDED just because it clears the same threshold. A named control
    # similarly keeps its own INFO verdict rather than being reclassified.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = 'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
        tokens_after = 'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
        rows = [("app1", 500, "1.40", "1.80", "200=495 500=5")]
        solo_report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1", w_app1=32, w_app2=0, w_end=0, rows=rows,
            scenario="app1-alone",
        )
        assert solo_report["verdict"]["result"] == "PASS", solo_report["verdict"]

    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app1"} 0.0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app2"} 0.0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="end-users"} 0.0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 40\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 35\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 90\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app1"} 0.2\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app2"} 0.1\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="end-users"} 0.3\n'
        )
        rows = [
            ("app1", 180, "0.80", "1.00", "200=180"),
            ("app2", 180, "0.80", "1.00", "200=180"),
            ("end-users", 780, "0.80", "1.00", "200=780"),
        ]
        control_report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 app2 end-users", w_app1=6, w_app2=6, w_end=26, rows=rows,
            scenario="equal-workers-control", control=True,
        )
        assert control_report["verdict"]["result"] == "INFO", control_report["verdict"]


def test_epp_restart_mid_run_fails():
    # A counter going backwards between snapshots means the EPP restarted
    # and the delta is meaningless -- must FAIL, not silently clamp and pass.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 9000\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 1000\n'
        )
        tokens_after = (
            # app1 reset to near-zero: counter went backwards.
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 50\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 1200\n'
        )
        rows = [
            ("app1", 500, "1.20", "2.40", "200=500"),
            ("app2", 490, "1.30", "2.50", "200=490"),
        ]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1 app2", w_app1=32, w_app2=32, w_end=0, rows=rows,
        )
        assert report["verdict"]["result"] == "FAIL", report["verdict"]
        assert report["verdict"]["epp_restarted_mid_run"] is True


def metrics_block(deltas_from_zero):
    return "".join(
        f'llm_d_epp_maas_fairness_contended_service_tokens_total{{fairness_id="{g}"}} {v}\n'
        for g, v in deltas_from_zero.items()
    )


def write_timeseries(tmp, name, snapshots):
    """snapshots: list of (epoch, {group: cumulative_value})."""
    lines = []
    for epoch, values in snapshots:
        lines.append(f"# ts=2026-11-01T00:00:{epoch:02d}Z epoch={epoch}")
        lines.append(metrics_block(values).rstrip("\n"))
    return write(tmp, name, "\n".join(lines) + "\n")


def write_timeseries_raw(tmp, name, snapshots):
    """snapshots: list of (epoch, raw_prometheus_text_block) -- for fixtures
    that need labels write_timeseries' plain {group: value} shape can't carry
    (UNI-164: a histogram's le/outcome labels alongside fairness_id)."""
    lines = []
    for epoch, block in snapshots:
        lines.append(f"# ts=2026-11-01T00:00:{epoch:02d}Z epoch={epoch}")
        lines.append(block.rstrip("\n"))
    return write(tmp, name, "\n".join(lines) + "\n")


def queue_wait_bucket_lines(fairness_id, outcome, cumulative):
    """Prometheus text for llm_d_epp_flow_control_request_queue_duration_seconds,
    labelled the way llm-d-router v0.11.0 actually emits it (fairness_id,
    priority, outcome, inference_pool, model_name, target_model_name --
    only fairness_id/outcome vary across these fixtures, the rest are fixed
    so _histogram_buckets' "sum across any other label" path is exercised
    the same way a real multi-pool scrape would). `cumulative` is
    [(le, count)], with le="+Inf" last."""
    name = "llm_d_epp_flow_control_request_queue_duration_seconds"
    lines = "".join(
        f'{name}_bucket{{fairness_id="{fairness_id}",priority="0",outcome="{outcome}",'
        f'inference_pool="maas-vllm-gpu-inference-pool",model_name="llama-3-1-8b",'
        f'target_model_name="llama-3-1-8b",le="{le}"}} {c}\n'
        for le, c in cumulative
    )
    return lines + f'{name}_count{{fairness_id="{fairness_id}",priority="0",outcome="{outcome}"}} {cumulative[-1][1]}\n'


def write_timeline_config(tmp, name, tenants=None, chaos_events=None):
    return write(tmp, name, json.dumps({"tenants": tenants or {}, "chaos_events": chaos_events or []}))


# --- UNI-127: windowed and convergence maths --------------------------------

def test_tenant_active_at_respects_start_stop_and_duty():
    always_on = fairness_report.default_schedule_entry(240)
    assert fairness_report.tenant_active_at(always_on, 0) is True
    assert fairness_report.tenant_active_at(always_on, 239.9) is True
    assert fairness_report.tenant_active_at(always_on, 240) is False

    joins_late = {"start": 120.0, "stop": 240.0, "duty_on": None, "duty_off": None}
    assert fairness_report.tenant_active_at(joins_late, 119) is False
    assert fairness_report.tenant_active_at(joins_late, 120) is True
    assert fairness_report.tenant_active_at(joins_late, 239) is True
    assert fairness_report.tenant_active_at(joins_late, 240) is False

    duty = {"start": 0.0, "stop": 240.0, "duty_on": 30.0, "duty_off": 30.0}
    assert fairness_report.tenant_active_at(duty, 0) is True
    assert fairness_report.tenant_active_at(duty, 29) is True
    assert fairness_report.tenant_active_at(duty, 30) is False
    assert fairness_report.tenant_active_at(duty, 59) is False
    assert fairness_report.tenant_active_at(duty, 60) is True
    assert fairness_report.tenant_active_at(duty, 90) is False


def test_resolve_schedule_merges_explicit_timeline_with_full_run_fallback():
    # end-users has an explicit late join; app1/app2 never got a timeline
    # entry at all, so they fall back to "active the whole run" -- the one,
    # prior behaviour every existing scenario relies on.
    schedule = fairness_report.resolve_schedule(
        {"end-users": {"start": 120, "stop": 240, "duty_on": None, "duty_off": None}},
        offered_groups={"app1", "app2", "end-users"},
        run_duration=240,
    )
    assert schedule["app1"] == {"start": 0.0, "stop": 240.0, "duty_on": None, "duty_off": None}
    assert schedule["app2"] == {"start": 0.0, "stop": 240.0, "duty_on": None, "duty_off": None}
    assert schedule["end-users"]["start"] == 120.0
    # A group this run never offered at all gets no schedule entry -- it was
    # never a candidate for a window or a phase edge.
    assert "unclassified" not in schedule


def test_compute_phase_edges_covers_start_stop_duty_and_chaos():
    schedule = {
        "app1": {"start": 0.0, "stop": 240.0, "duty_on": 30.0, "duty_off": 30.0},
        "end-users": {"start": 120.0, "stop": 240.0, "duty_on": None, "duty_off": None},
    }
    edges = fairness_report.compute_phase_edges(
        schedule, chaos_events=[{"type": "epp_delete", "at_seconds": 90}], run_duration=240,
    )
    assert edges[0] == 0.0
    assert 120.0 in edges  # end-users joins
    assert 240.0 in edges  # run end / stop
    assert 90.0 in edges  # chaos event
    assert 30.0 in edges and 60.0 in edges  # app1's duty toggles
    assert edges == sorted(set(edges))


def test_compute_phase_edges_treats_live_set_events_like_any_other_chaos_event():
    # UNI-180: 15-fairness-benchmark.sh's generic LIVE_SET_AT hook records
    # "live_set"/"live_restore" timeline entries with the same `at_seconds`
    # key the existing "epp_delete"/"scale_down"/"scale_restore" events use --
    # compute_phase_edges never switches on `type`, so a new event type needs
    # no report-side change to be picked up as a phase edge. This test is the
    # evidence for that claim, not a new capability.
    schedule = {"app1": {"start": 0.0, "stop": 240.0}}
    edges = fairness_report.compute_phase_edges(
        schedule,
        chaos_events=[
            {"type": "live_set", "at_seconds": 60, "target": "epp-key:newcomerClamp", "value": "false"},
            {"type": "live_restore", "at_seconds": 180, "target": "epp-key:newcomerClamp"},
        ],
        run_duration=240,
    )
    assert 60.0 in edges
    assert 180.0 in edges


def test_compute_windows_matches_whole_run_math_over_one_window():
    # A single window spanning the whole run must reproduce the same
    # expected/observed share the whole-run (before/after) calculation would,
    # since it's the same two snapshots and the same definitions.
    schedule = fairness_report.resolve_schedule(None, {"app1", "app2", "end-users"}, 240)
    weights = {"app1": 20.0, "app2": 10.0, "end-users": 65.0}
    timeseries = [
        (0, "t0", {"llm_d_epp_maas_fairness_contended_service_tokens_total":
                   {"app1": 1000.0, "app2": 1000.0, "end-users": 1000.0}}, False),
        (240, "t1", {"llm_d_epp_maas_fairness_contended_service_tokens_total":
                     {"app1": 3100.0, "app2": 2000.0, "end-users": 7900.0}}, False),
    ]
    windows, epp_restarted, scrape_gap = fairness_report.compute_windows(timeseries, schedule, weights)
    assert epp_restarted is False
    assert scrape_gap is False
    assert len(windows) == 1
    w = windows[0]
    assert w["start_s"] == 0.0 and w["end_s"] == 240.0
    by_group = {g["group"]: g for g in w["groups"]}
    assert abs(by_group["app1"]["expected_share_pct"] - (20 / 95 * 100)) < 1e-6
    assert abs(by_group["app1"]["observed_share_pct"] - (2100 / 10000 * 100)) < 1e-6
    assert by_group["app1"]["deviation_pts"] is not None


def test_compute_windows_respects_schedule_membership_per_window():
    # end-users joins at t=10 (midpoint of the second window). The first
    # window must show it inactive with no share computed; the second must
    # show it active and re-split the expected share between all three.
    schedule = fairness_report.resolve_schedule(
        {"end-users": {"start": 10, "stop": 20, "duty_on": None, "duty_off": None}},
        offered_groups={"app1", "app2", "end-users"}, run_duration=20,
    )
    weights = {"app1": 20.0, "app2": 10.0, "end-users": 65.0}
    tok = "llm_d_epp_maas_fairness_contended_service_tokens_total"
    timeseries = [
        (0, "t0", {tok: {"app1": 0.0, "app2": 0.0, "end-users": 0.0}}, False),
        (10, "t1", {tok: {"app1": 100.0, "app2": 100.0, "end-users": 0.0}}, False),
        (20, "t2", {tok: {"app1": 150.0, "app2": 150.0, "end-users": 300.0}}, False),
    ]
    windows, _, _ = fairness_report.compute_windows(timeseries, schedule, weights)
    assert len(windows) == 2
    w0 = {g["group"]: g for g in windows[0]["groups"]}
    assert w0["end-users"]["active"] is False
    assert w0["end-users"]["expected_share_pct"] is None
    assert w0["end-users"]["observed_share_pct"] is None
    # app1/app2 split 50/50 by weight while end-users is absent (20/30, 10/30).
    assert abs(w0["app1"]["expected_share_pct"] - (20 / 30 * 100)) < 1e-6

    w1 = {g["group"]: g for g in windows[1]["groups"]}
    assert w1["end-users"]["active"] is True
    assert abs(w1["end-users"]["expected_share_pct"] - (65 / 95 * 100)) < 1e-6
    # delivered: app1=50, app2=50, end-users=300 -> end-users observed 75%.
    assert abs(w1["end-users"]["observed_share_pct"] - 75.0) < 1e-6


def test_compute_windows_flags_counter_going_backwards():
    schedule = fairness_report.resolve_schedule(None, {"app1", "app2"}, 20)
    weights = {"app1": 20.0, "app2": 10.0}
    tok = "llm_d_epp_maas_fairness_contended_service_tokens_total"
    timeseries = [
        (0, "t0", {tok: {"app1": 9000.0, "app2": 1000.0}}, False),
        (10, "t1", {tok: {"app1": 50.0, "app2": 1200.0}}, False),  # app1 went backwards
    ]
    windows, epp_restarted, scrape_gap = fairness_report.compute_windows(timeseries, schedule, weights)
    assert epp_restarted is True
    assert scrape_gap is False
    by_group = {g["group"]: g for g in windows[0]["groups"]}
    assert by_group["app1"]["delivered_tokens"] == 0.0  # clamped, not negative


def test_compute_windows_treats_failed_scrape_as_scrape_gap_not_restart():
    # UNI-230: a window's closing scrape failing outright (curl exit != 0)
    # looks exactly like app1's counter "going backwards" to zero once
    # grepped -- the only thing that tells it apart from a real restart is
    # the closing snapshot's own recorded scrape_failed flag.
    schedule = fairness_report.resolve_schedule(None, {"app1", "app2"}, 20)
    weights = {"app1": 20.0, "app2": 10.0}
    tok = "llm_d_epp_maas_fairness_contended_service_tokens_total"
    timeseries = [
        (0, "t0", {tok: {"app1": 9000.0, "app2": 1000.0}}, False),
        (10, "t1", {}, True),  # scrape failed outright: empty snapshot, not a reset
    ]
    windows, epp_restarted, scrape_gap = fairness_report.compute_windows(timeseries, schedule, weights)
    assert epp_restarted is False
    assert scrape_gap is True
    by_group = {g["group"]: g for g in windows[0]["groups"]}
    assert by_group["app1"]["delivered_tokens"] == 0.0  # still clamped: true value unknown


def test_compute_convergence_finds_first_window_that_stays_in_threshold():
    # Deviation starts large (30pts), drops to 15pts (still over a 10pt
    # threshold), then settles at 2pts and stays there -- convergence must be
    # reported at the START of the settled run, not the first dip.
    def window(start, end, dev):
        return {"start_s": start, "end_s": end, "groups": [
            {"group": "app1", "active": True, "deviation_pts": dev},
        ]}
    windows = [
        window(0, 10, 30.0),
        window(10, 20, 15.0),
        window(20, 30, -12.0),
        window(30, 40, 2.0),
        window(40, 50, -1.5),
        window(50, 60, 1.0),
    ]
    results = fairness_report.compute_convergence(windows, phase_edges=[0.0], threshold_points=10.0)
    assert len(results) == 1
    assert results[0]["phase_edge_s"] == 0.0
    assert results[0]["converged_at_s"] == 30.0
    assert results[0]["seconds_to_converge"] == 30.0


def test_compute_convergence_reports_none_when_it_never_settles():
    def window(start, end, dev):
        return {"start_s": start, "end_s": end, "groups": [
            {"group": "app1", "active": True, "deviation_pts": dev},
        ]}
    # Alternates in and out of threshold right up to the end -- never "stays".
    windows = [window(i * 10, i * 10 + 10, 2.0 if i % 2 == 0 else 20.0) for i in range(6)]
    results = fairness_report.compute_convergence(windows, phase_edges=[0.0], threshold_points=10.0)
    assert results[0]["converged_at_s"] is None
    assert results[0]["seconds_to_converge"] is None


def test_compute_windows_uncontended_window_reports_none_not_zero_deviation():
    # UNI-223: app1/app2 stop delivering ANY contended tokens for a window
    # (e.g. remaining demand dropped below the admission threshold once
    # another tenant left) while both are still active/offered. The old
    # behaviour forced observed_share_pct to 0.0 for both, manufacturing a
    # full-magnitude deviation from a state where nothing was measured.
    schedule = fairness_report.resolve_schedule(None, {"app1", "app2"}, 20)
    weights = {"app1": 66.7, "app2": 33.3}
    tok = "llm_d_epp_maas_fairness_contended_service_tokens_total"
    timeseries = [
        (0, "t0", {tok: {"app1": 5000.0, "app2": 5000.0}}, False),
        (10, "t1", {tok: {"app1": 5000.0, "app2": 5000.0}}, False),  # flat: nobody delivered anything
    ]
    windows, _, _ = fairness_report.compute_windows(timeseries, schedule, weights)
    assert len(windows) == 1
    w = windows[0]
    assert w["uncontended"] is True
    by_group = {g["group"]: g for g in w["groups"]}
    for gid in ("app1", "app2"):
        assert by_group[gid]["active"] is True
        assert by_group[gid]["expected_share_pct"] is not None  # the target is still known
        assert by_group[gid]["observed_share_pct"] is None      # but nothing was observed
        assert by_group[gid]["deviation_pts"] is None            # so no deviation is claimed either way


def test_compute_windows_a_group_actually_getting_zero_share_is_not_uncontended():
    # Contrast case: app2 is active and gets genuinely 0% of a nonzero pool
    # (app1 took everything) -- that IS a real, scoreable deviation and must
    # stay distinct from the "nobody got anything" uncontended case above.
    schedule = fairness_report.resolve_schedule(None, {"app1", "app2"}, 20)
    weights = {"app1": 50.0, "app2": 50.0}
    tok = "llm_d_epp_maas_fairness_contended_service_tokens_total"
    timeseries = [
        (0, "t0", {tok: {"app1": 0.0, "app2": 0.0}}, False),
        (10, "t1", {tok: {"app1": 1000.0, "app2": 0.0}}, False),
    ]
    windows, _, _ = fairness_report.compute_windows(timeseries, schedule, weights)
    w = windows[0]
    assert w["uncontended"] is False
    by_group = {g["group"]: g for g in w["groups"]}
    assert by_group["app2"]["observed_share_pct"] == 0.0
    assert by_group["app2"]["deviation_pts"] == -50.0


def test_compute_windows_restart_window_is_unknown_not_uncontended():
    # UNI-311 (review of UNI-223's fix): tokens_total hitting zero because a
    # counter went backwards (an EPP restart) looks identical, on the tokens
    # signal alone, to a genuinely quiet window -- that ambiguity is exactly
    # what let a restart read as "converged, uncontended" before this fix.
    # The window's true value is unobservable, not zero, so it must come back
    # unknown (None), not True.
    schedule = fairness_report.resolve_schedule(None, {"app1", "app2"}, 20)
    weights = {"app1": 66.7, "app2": 33.3}
    tok = "llm_d_epp_maas_fairness_contended_service_tokens_total"
    timeseries = [
        (0, "t0", {tok: {"app1": 9000.0, "app2": 1000.0}}, False),
        (10, "t1", {tok: {"app1": 50.0, "app2": 1200.0}}, False),  # app1 went backwards: restart
    ]
    windows, epp_restarted, scrape_gap = fairness_report.compute_windows(timeseries, schedule, weights)
    assert epp_restarted is True
    assert scrape_gap is False
    assert windows[0]["uncontended"] is None


def test_compute_windows_failed_scrape_window_is_unknown_not_uncontended():
    # Same ambiguity as the restart case above, but for UNI-230's other
    # clamp cause: the closing scrape itself failed outright, not a process
    # restart. Either way the window's true value is unknown, not quiet.
    schedule = fairness_report.resolve_schedule(None, {"app1", "app2"}, 20)
    weights = {"app1": 66.7, "app2": 33.3}
    tok = "llm_d_epp_maas_fairness_contended_service_tokens_total"
    timeseries = [
        (0, "t0", {tok: {"app1": 9000.0, "app2": 1000.0}}, False),
        (10, "t1", {}, True),  # scrape failed outright: empty snapshot, not a reset
    ]
    windows, epp_restarted, scrape_gap = fairness_report.compute_windows(timeseries, schedule, weights)
    assert epp_restarted is False
    assert scrape_gap is True
    assert windows[0]["uncontended"] is None


def test_compute_windows_tokens_flat_while_contended_seconds_advancing_is_not_uncontended():
    # The long-request regime (UNI-283/UNI-146): a 10s window can legitimately
    # deliver zero contended tokens while the band is still heavily
    # backlogged -- requests are in flight but none finished this slice. That
    # is active non-convergence, not quiet, so it must NOT be corroborated as
    # uncontended just because contended_service_tokens_total is flat.
    schedule = fairness_report.resolve_schedule(None, {"app1", "app2"}, 20)
    weights = {"app1": 66.7, "app2": 33.3}
    tok = "llm_d_epp_maas_fairness_contended_service_tokens_total"
    secs = "llm_d_epp_maas_fairness_contended_seconds_total"
    timeseries = [
        (0, "t0", {
            tok: {"app1": 5000.0, "app2": 5000.0},
            secs: {"app1": 100.0, "app2": 100.0},
        }, False),
        (10, "t1", {
            tok: {"app1": 5000.0, "app2": 5000.0},  # flat: nobody finished this window
            secs: {"app1": 105.0, "app2": 105.0},   # but both groups kept accruing contended time
        }, False),
    ]
    windows, epp_restarted, scrape_gap = fairness_report.compute_windows(timeseries, schedule, weights)
    assert epp_restarted is False
    assert scrape_gap is False
    assert windows[0]["uncontended"] is False


def test_compute_convergence_unknown_tail_does_not_count_as_converged():
    # UNI-311: contrast with test_compute_convergence_treats_uncontended_tail_
    # as_converged below -- a clamped window (restart/scrape-gap) still
    # carries the same manufactured full-magnitude deviation a clamp has
    # always produced (every delta forced to 0.0). `uncontended=None` must
    # NOT short-circuit that away the way `True` does; it has to fall through
    # to the ordinary, disqualifying deviation check.
    def window(start, end, dev, uncontended=False):
        return {"start_s": start, "end_s": end, "uncontended": uncontended, "groups": [
            {"group": "app1", "active": True, "deviation_pts": dev},
            {"group": "app2", "active": True, "deviation_pts": -dev},
        ]}
    windows = [
        window(0, 10, 15.2),
        window(10, 20, 10.3),
        window(20, 30, 25.0, uncontended=None),  # a restart/scrape-gap window: unknown, not quiet
        window(30, 40, 25.0, uncontended=None),
    ]
    results = fairness_report.compute_convergence(windows, phase_edges=[0.0], threshold_points=10.0)
    assert results[0]["converged_at_s"] is None
    assert results[0]["converged_because_uncontended"] is None


def test_compute_convergence_treats_uncontended_tail_as_converged():
    # UNI-223: mirrors the live b2-tenant-leaves finding at queueDepthThreshold
    # 32 -- a tenant leaves, the remaining two settle briefly with real
    # (bounded) deviations, then the pool drops out of contention entirely
    # for the rest of the phase (nobody delivers any more contended tokens).
    # That tail must read as "converged, uncontended," not "never converged."
    def window(start, end, dev, uncontended=False):
        return {"start_s": start, "end_s": end, "uncontended": uncontended, "groups": [
            {"group": "app1", "active": True, "deviation_pts": None if uncontended else dev},
            {"group": "app2", "active": True, "deviation_pts": None if uncontended else -dev},
        ]}
    windows = [
        window(0, 10, 15.2),
        window(10, 20, 10.3),
        window(20, 30, 0.0, uncontended=True),
        window(30, 40, 0.0, uncontended=True),
        window(40, 50, 0.0, uncontended=True),
    ]
    results = fairness_report.compute_convergence(windows, phase_edges=[0.0], threshold_points=10.0)
    assert results[0]["converged_at_s"] == 20.0
    assert results[0]["converged_because_uncontended"] is True


def test_compute_convergence_uncontended_does_not_mask_real_divergence_after_it():
    # An uncontended lull followed by a real out-of-threshold window must
    # still report "never converged" -- going quiet once doesn't retroactively
    # excuse a later genuine deviation.
    def window(start, end, dev=None, uncontended=False):
        return {"start_s": start, "end_s": end, "uncontended": uncontended, "groups": [
            {"group": "app1", "active": True, "deviation_pts": dev},
        ]}
    windows = [
        window(0, 10, uncontended=True),
        window(10, 20, dev=25.0),  # genuinely diverges again, right up to the end
    ]
    results = fairness_report.compute_convergence(windows, phase_edges=[0.0], threshold_points=10.0)
    assert results[0]["converged_at_s"] is None
    assert results[0]["converged_because_uncontended"] is None


def test_compute_convergence_real_settle_is_not_mislabeled_uncontended():
    # A genuine, bounded settle (never uncontended) must keep
    # converged_because_uncontended False, not None/True -- the UNI-223 flag
    # should only ever fire when the tail it found really was quiet.
    def window(start, end, dev):
        return {"start_s": start, "end_s": end, "uncontended": False, "groups": [
            {"group": "app1", "active": True, "deviation_pts": dev},
        ]}
    windows = [window(0, 10, 30.0), window(10, 20, 2.0), window(20, 30, -1.0)]
    results = fairness_report.compute_convergence(windows, phase_edges=[0.0], threshold_points=10.0)
    assert results[0]["converged_at_s"] == 10.0
    assert results[0]["converged_because_uncontended"] is False


def test_compute_convergence_per_phase_edge_resets_the_window():
    # Two phases: [0,20) settles immediately; a chaos event at t=20 knocks it
    # back out of threshold, and it re-settles at t=40. Convergence for the
    # second edge must be measured from t=20, not from run start.
    def window(start, end, dev):
        return {"start_s": start, "end_s": end, "groups": [
            {"group": "app1", "active": True, "deviation_pts": dev},
        ]}
    windows = [
        window(0, 10, 1.0), window(10, 20, 1.0),
        window(20, 30, 25.0), window(30, 40, 25.0),
        window(40, 50, 1.0), window(50, 60, 1.0),
    ]
    results = fairness_report.compute_convergence(windows, phase_edges=[0.0, 20.0], threshold_points=10.0)
    by_edge = {r["phase_edge_s"]: r for r in results}
    assert by_edge[0.0]["converged_at_s"] == 0.0
    assert by_edge[20.0]["converged_at_s"] == 40.0
    assert by_edge[20.0]["seconds_to_converge"] == 20.0


def test_build_report_timeline_section_absent_without_timeseries_arg():
    # Regression guard: a caller that doesn't pass the new UNI-127 args (every
    # existing call site, until 15-fairness-benchmark.sh is updated) must get
    # exactly the pre-UNI-127 report shape back, with the same verdict.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = 'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 1000\n'
        tokens_after = 'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 1500\n'
        rows = [("app1", 500, "1.20", "2.40", "200=500")]
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1", w_app1=32, w_app2=0, w_end=0, rows=rows,
        )
        assert report["timeline"] is None
        assert report["verdict"]["result"] == "PASS"


def test_build_report_timeline_section_populated_with_timeseries_and_config():
    with tempfile.TemporaryDirectory() as tmp:
        before = write(tmp, "before.txt", CONFIGURED_WEIGHT + ENFORCING_ON +
                       'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
                       'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n')
        after = write(tmp, "after.txt", CONFIGURED_WEIGHT + ENFORCING_ON +
                      'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 2000\n'
                      'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 1000\n')
        log = write(tmp, "loadgen.log", loadgen_log("app1 app2", 32, 32, 0, 20, [
            ("app1", 500, "1.20", "2.40", "200=500"),
            ("app2", 480, "1.30", "2.50", "200=480"),
        ]))
        ts = write_timeseries(tmp, "ts.txt", [
            (0, {"app1": 0.0, "app2": 0.0}),
            (10, {"app1": 1000.0, "app2": 500.0}),
            (20, {"app1": 2000.0, "app2": 1000.0}),
        ])
        cfg = write_timeline_config(tmp, "timeline.json")
        out_json = os.path.join(tmp, "report.json")
        out_md = os.path.join(tmp, "report.md")
        report = fairness_report.build_report(
            scenario="test-scenario", enforce=True, duration_seconds=20, backend="vllm-gpu",
            epp_image_digest="sha256:deadbeef", namespace="maas-fairness-poc",
            epp_pod="test-pod", run_start="2026-11-01T00:00:00Z", run_end="2026-11-01T00:00:20Z",
            threshold_points=10.0, metrics_before_path=before, metrics_after_path=after,
            loadgen_log_path=log, metrics_timeseries_path=ts, timeline_config_path=cfg,
            window_seconds=10.0,
        )
        assert report["verdict"]["result"] == "PASS"  # unchanged by adding timeline data
        tl = report["timeline"]
        assert tl is not None
        assert tl["window_seconds"] == 10.0
        assert len(tl["windows"]) == 2
        # Both app1 and app2 fall back to "active the whole run" (no explicit
        # timeline entry), so their start (0) and stop (20, the run duration)
        # are the only phase edges here.
        assert tl["phase_edges"] == [0.0, 20.0]
        assert len(tl["convergence"]) == 2
        # Rendering must not blow up with a populated timeline section.
        md = fairness_report.render_markdown(report)
        assert "## Timeline (UNI-127)" in md
        assert "n/a" not in md.split("## Timeline (UNI-127)")[1].split("## Sources")[0].split("\n")[0]

        # And the CLI must accept the new flags end to end.
        proc = subprocess.run(
            [sys.executable, "-I", os.path.join(HERE, "15-fairness-report.py"),
             "--scenario", "test-scenario", "--enforce", "true", "--duration-seconds", "20",
             "--backend", "vllm-gpu", "--epp-image-digest", "sha256:deadbeef",
             "--namespace", "maas-fairness-poc", "--epp-pod", "test-pod",
             "--run-start", "2026-11-01T00:00:00Z", "--run-end", "2026-11-01T00:00:20Z",
             "--metrics-before", before, "--metrics-after", after, "--loadgen-log", log,
             "--metrics-timeseries", ts, "--timeline-config", cfg, "--window-seconds", "10",
             "--out-json", out_json, "--out-md", out_md],
            capture_output=True, text=True,
        )
        assert proc.returncode == 0, f"stdout={proc.stdout}\nstderr={proc.stderr}"
        with open(out_json) as f:
            cli_report = json.load(f)
        assert cli_report["timeline"] is not None


# --- UNI-222: schedule-aware whole-run expected/observed share --------------

def _window(groups):
    """groups: {gid: (active, delivered_tokens, expected_share_pct)}."""
    return {
        "start_s": 0.0, "end_s": 10.0,
        "groups": [
            {"group": g, "active": a, "delivered_tokens": tok, "expected_share_pct": exp,
             "observed_share_pct": None, "deviation_pts": None}
            for g, (a, tok, exp) in groups.items()
        ],
    }


def test_schedule_has_partial_offering_true_only_for_non_default_entries():
    trivial = {"app1": fairness_report.default_schedule_entry(240), "app2": fairness_report.default_schedule_entry(240)}
    assert fairness_report.schedule_has_partial_offering(trivial, 240) is False

    joins_late = dict(trivial, **{"app2": {"start": 120.0, "stop": 240.0, "duty_on": None, "duty_off": None}})
    assert fairness_report.schedule_has_partial_offering(joins_late, 240) is True

    leaves_early = dict(trivial, **{"app2": {"start": 0.0, "stop": 180.0, "duty_on": None, "duty_off": None}})
    assert fairness_report.schedule_has_partial_offering(leaves_early, 240) is True

    duty_cycles = dict(trivial, **{"app1": {"start": 0.0, "stop": 240.0, "duty_on": 30.0, "duty_off": 30.0}})
    assert fairness_report.schedule_has_partial_offering(duty_cycles, 240) is True


def test_schedule_aware_whole_run_shares_matches_flat_formula_when_trivial():
    # Every group active every window (the common case) -- the time-weighted
    # average of a constant is that constant, so this must reproduce exactly
    # what offered_weight_total/offered_tokens_total would have given.
    windows = [
        _window({"app1": (True, 200.0, 21.05), "app2": (True, 100.0, 10.53), "end-users": (True, 650.0, 68.42)}),
        _window({"app1": (True, 200.0, 21.05), "app2": (True, 100.0, 10.53), "end-users": (True, 650.0, 68.42)}),
    ]
    shares = fairness_report.schedule_aware_whole_run_shares(windows, ["app1", "app2", "end-users"])
    assert abs(shares["app1"]["expected_share_pct"] - 21.05) < 0.01
    assert abs(shares["app1"]["observed_share_pct"] - 21.05) < 0.01


def test_schedule_aware_whole_run_shares_excludes_windows_with_no_group_active():
    # UNI-245/UNI-222 live finding: once every scheduled group's `stop` offset
    # has passed, a window can still show real delivered tokens (in-flight
    # requests draining) with every group marked inactive. That volume must
    # not inflate the denominator for a target nobody was scored against --
    # the degenerate case of the general "a window's pool only counts toward
    # the groups eligible to contend for it" rule schedule_aware_whole_run_shares
    # implements.
    windows = [
        _window({"app1": (True, 100.0, 50.0), "app2": (True, 100.0, 50.0)}),
        _window({"app1": (False, 999.0, None), "app2": (False, 999.0, None)}),  # drain tail
    ]
    shares = fairness_report.schedule_aware_whole_run_shares(windows, ["app1", "app2"])
    assert abs(shares["app1"]["expected_share_pct"] - 50.0) < 0.01
    assert abs(shares["app1"]["observed_share_pct"] - 50.0) < 0.01


def test_schedule_aware_whole_run_shares_returns_empty_with_no_contended_windows():
    windows = [_window({"app1": (False, 0.0, None), "app2": (False, 0.0, None)})]
    assert fairness_report.schedule_aware_whole_run_shares(windows, ["app1", "app2"]) == {}
    assert fairness_report.schedule_aware_whole_run_shares([], ["app1", "app2"]) == {}


def test_build_report_long_idle_return_whole_run_fail_becomes_pass_schedule_aware():
    # UNI-222 (B4): app1 is active 0-30s then idle for the rest of a 150s
    # run (never returns within this run -- the shape that originally FAILed
    # UNI-143/UNI-218 at -15.5/-15.6pt). While active, app1/app2/end-users
    # split exactly on weight (20/10/65); while idle, app2/end-users correctly
    # absorb app1's share (work conservation) and also split exactly on
    # their own renormalized weight (10/65 -> 13.33/86.67). A flat whole-run
    # ratio scores this "perfect policy" run as a severe FAIL anyway, purely
    # because app1 is 0% for 80% of the run against a flat 21.05% target;
    # the schedule-aware correction must read it as the PASS it actually is.
    with tempfile.TemporaryDirectory() as tmp:
        # app1: 3 active windows x 200 tokens = 600 total, then silent.
        # app2/end-users: 100/650 per active window (3x), then 100/650 per
        # idle window (12x) -- same per-window volume throughout, just
        # renormalized among whoever is still active.
        app1_cum, app2_cum, eu_cum = [0.0], [0.0], [0.0]
        for i in range(3):
            app1_cum.append(app1_cum[-1] + 200.0)
            app2_cum.append(app2_cum[-1] + 100.0)
            eu_cum.append(eu_cum[-1] + 650.0)
        for i in range(12):
            app1_cum.append(app1_cum[-1])
            app2_cum.append(app2_cum[-1] + 100.0)
            eu_cum.append(eu_cum[-1] + 650.0)
        snapshots = [
            (t * 10, {"app1": app1_cum[t], "app2": app2_cum[t], "end-users": eu_cum[t]})
            for t in range(16)
        ]
        before = write(tmp, "before.txt", CONFIGURED_WEIGHT + ENFORCING_ON + metrics_block({"app1": 0.0, "app2": 0.0, "end-users": 0.0}))
        after = write(tmp, "after.txt", CONFIGURED_WEIGHT + ENFORCING_ON + metrics_block(
            {"app1": app1_cum[-1], "app2": app2_cum[-1], "end-users": eu_cum[-1]}
        ))
        log = write(tmp, "loadgen.log", loadgen_log("app1 app2 end-users", 32, 32, 128, 150, [
            ("app1", 100, "1.00", "2.00", "200=100"),
            ("app2", 400, "1.00", "2.00", "200=400"),
            ("end-users", 2000, "1.00", "2.00", "200=2000"),
        ]))
        ts = write_timeseries(tmp, "ts.txt", snapshots)
        cfg = write_timeline_config(tmp, "timeline.json", tenants={"app1": {"duty_on": 30, "duty_off": 120}})

        # Sanity check: without the schedule, this exact data is the FAIL
        # UNI-143/UNI-218 actually hit (app1's flat whole-run share crushed
        # by its own idle time).
        flat = fairness_report.build_report(
            scenario="b4-long-idle", enforce=True, duration_seconds=150, backend="vllm-gpu",
            epp_image_digest="sha256:deadbeef", namespace="maas-fairness-poc", epp_pod="test-pod",
            run_start="2026-11-01T00:00:00Z", run_end="2026-11-01T00:02:30Z", threshold_points=10.0,
            metrics_before_path=before, metrics_after_path=after, loadgen_log_path=log,
        )
        assert flat["verdict"]["result"] == "FAIL", flat["verdict"]
        flat_app1 = next(g for g in flat["groups"] if g["group"] == "app1")
        assert flat_app1["deviation_pts"] < -10.0

        # With the schedule + timeseries, the same run reads PASS.
        report = fairness_report.build_report(
            scenario="b4-long-idle", enforce=True, duration_seconds=150, backend="vllm-gpu",
            epp_image_digest="sha256:deadbeef", namespace="maas-fairness-poc", epp_pod="test-pod",
            run_start="2026-11-01T00:00:00Z", run_end="2026-11-01T00:02:30Z", threshold_points=10.0,
            metrics_before_path=before, metrics_after_path=after, loadgen_log_path=log,
            metrics_timeseries_path=ts, timeline_config_path=cfg, window_seconds=10.0,
        )
        assert report["verdict"]["result"] == "PASS", report["verdict"]
        assert sorted(report["verdict"]["schedule_aware_groups"]) == ["app1", "app2", "end-users"]
        for g in report["groups"]:
            if g["group"] in ("app1", "app2", "end-users"):
                assert abs(g["deviation_pts"]) < 1.0, g
        md = fairness_report.render_markdown(report)
        assert "Schedule-aware expected share (UNI-222)" in md


def test_mid_run_restart_invisible_to_snapshot_pair_is_flagged_from_windows():
    # UNI-163 (F6): found live on a run that patched maas-epp-config mid-run
    # (any edit recreates the EPP pod -- no live-reload path -- so its
    # counters reset to zero). before=~0 and after=the post-reset pod's own
    # modest cumulative total is STILL a monotonic rise end to end, so the
    # before/after-only epp_restarted check (test_epp_restart_mid_run_fails,
    # above) never fires -- only the windowed series, which scrapes through
    # the actual reset, sees the backwards step. Before this ticket that
    # signal was "purely additive" (UNI-127's own description of the timeline
    # section) and never reached the verdict: a run that reset mid-flight and
    # undercounted every delta as a result rendered as a clean, unremarkable
    # verdict with no indication anything was wrong.
    with tempfile.TemporaryDirectory() as tmp:
        before = write(tmp, "before.txt", CONFIGURED_WEIGHT + ENFORCING_ON +
                       'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n')
        # Lower than the mid-run peak (9000) but still higher than `before` --
        # reads as ordinary, modest growth unless you have the windowed data.
        after = write(tmp, "after.txt", CONFIGURED_WEIGHT + ENFORCING_ON +
                      'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 50\n')
        log = write(tmp, "loadgen.log", loadgen_log("app1", 32, 0, 0, 30, [
            ("app1", 500, "1.20", "2.40", "200=500"),
        ]))
        ts = write_timeseries(tmp, "ts.txt", [
            (0, {"app1": 0.0}),
            (10, {"app1": 9000.0}),
            (20, {"app1": 20.0}),   # the reset the before/after pair never sees
            (30, {"app1": 50.0}),
        ])
        cfg = write_timeline_config(tmp, "timeline.json")
        report = fairness_report.build_report(
            scenario="test-scenario", enforce=True, duration_seconds=30, backend="vllm-gpu",
            epp_image_digest="sha256:deadbeef", namespace="maas-fairness-poc",
            epp_pod="test-pod", run_start="2026-11-01T00:00:00Z", run_end="2026-11-01T00:00:30Z",
            threshold_points=10.0, metrics_before_path=before, metrics_after_path=after,
            loadgen_log_path=log, metrics_timeseries_path=ts, timeline_config_path=cfg,
            window_seconds=10.0,
        )
        v = report["verdict"]
        # The before/after-only check still reads this as monotonic growth --
        # confirming the gap exists, not asserting that's correct.
        assert v["epp_restarted_mid_run"] is False, v
        assert v["epp_restarted_in_windows_but_not_snapshot_pair"] is True, v
        # write_timeseries' blocks carry no `# scrape_exit=` marker at all,
        # same as every run captured before UNI-230 -- the real restart this
        # run simulates must still read as a restart, not a scrape gap.
        assert v["scrape_gap_in_windows"] is False, v
        md = fairness_report.render_markdown(report)
        assert "Caveat (UNI-163)" in md
        assert "Caveat (UNI-230)" not in md


def test_epp_restarted_in_windows_but_not_snapshot_pair_is_false_when_consistent():
    # Regression guard: an ordinary run (no mid-run reset at all, or one the
    # before/after pair already caught on its own) must not get the new
    # caveat -- it is additive signal for exactly the gap above, not a
    # second, redundant restart flag.
    with tempfile.TemporaryDirectory() as tmp:
        before = write(tmp, "before.txt", CONFIGURED_WEIGHT + ENFORCING_ON +
                       'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n')
        after = write(tmp, "after.txt", CONFIGURED_WEIGHT + ENFORCING_ON +
                      'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 2000\n')
        log = write(tmp, "loadgen.log", loadgen_log("app1", 32, 0, 0, 20, [
            ("app1", 500, "1.20", "2.40", "200=500"),
        ]))
        ts = write_timeseries(tmp, "ts.txt", [
            (0, {"app1": 0.0}),
            (10, {"app1": 1000.0}),
            (20, {"app1": 2000.0}),
        ])
        cfg = write_timeline_config(tmp, "timeline.json")
        report = fairness_report.build_report(
            scenario="test-scenario", enforce=True, duration_seconds=20, backend="vllm-gpu",
            epp_image_digest="sha256:deadbeef", namespace="maas-fairness-poc",
            epp_pod="test-pod", run_start="2026-11-01T00:00:00Z", run_end="2026-11-01T00:00:20Z",
            threshold_points=10.0, metrics_before_path=before, metrics_after_path=after,
            loadgen_log_path=log, metrics_timeseries_path=ts, timeline_config_path=cfg,
            window_seconds=10.0,
        )
        v = report["verdict"]
        assert v["epp_restarted_mid_run"] is False, v
        assert v["epp_restarted_in_windows_but_not_snapshot_pair"] is False, v
        assert v["scrape_gap_in_windows"] is False, v
        assert "Caveat (UNI-163)" not in fairness_report.render_markdown(report)


def test_failed_scrape_mid_run_is_flagged_as_scrape_gap_not_restart():
    # UNI-230: found on twenty-group-scale-discriminating's run (the heaviest
    # in the suite, 1350 total offered workers) -- the windowed restart
    # detector (UNI-163's mechanism) tripped with none of the usual
    # corroborating restart evidence (no pod-identity change, no k8s restart
    # event, container restart count 0, no panic/restart marker in the EPP's
    # own stderr capture). The run also logged sustained
    # `curl: (7) Failed to connect ... port 9090` against the EPP's metrics
    # port during the load. This reproduces that mechanism directly: a
    # mid-run scrape whose own recorded exit code is nonzero, sandwiched
    # between two successful scrapes that keep growing -- the same "counter
    # went backwards, then recovered" shape the real run's raw evidence
    # couldn't explain.
    with tempfile.TemporaryDirectory() as tmp:
        before = write(tmp, "before.txt", CONFIGURED_WEIGHT + ENFORCING_ON +
                       'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n')
        after = write(tmp, "after.txt", CONFIGURED_WEIGHT + ENFORCING_ON +
                      'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 9000\n')
        log = write(tmp, "loadgen.log", loadgen_log("app1", 32, 0, 0, 30, [
            ("app1", 500, "1.20", "2.40", "200=500"),
        ]))
        ts = write_timeseries_raw(tmp, "ts.txt", [
            (0, "# scrape_exit=0\n" + metrics_block({"app1": 0.0})),
            (10, "# scrape_exit=0\n" + metrics_block({"app1": 4000.0})),
            (20, "# scrape_exit=7\n"),  # curl: (7) Failed to connect -- empty body, not a reset
            (30, "# scrape_exit=0\n" + metrics_block({"app1": 9000.0})),
        ])
        cfg = write_timeline_config(tmp, "timeline.json")
        report = fairness_report.build_report(
            scenario="test-scenario", enforce=True, duration_seconds=30, backend="vllm-gpu",
            epp_image_digest="sha256:deadbeef", namespace="maas-fairness-poc",
            epp_pod="test-pod", run_start="2026-11-01T00:00:00Z", run_end="2026-11-01T00:00:30Z",
            threshold_points=10.0, metrics_before_path=before, metrics_after_path=after,
            loadgen_log_path=log, metrics_timeseries_path=ts, timeline_config_path=cfg,
            window_seconds=10.0,
        )
        v = report["verdict"]
        assert v["epp_restarted_mid_run"] is False, v
        # The fix: a scrape that failed outright must not be read as a
        # restart, even though it leaves the same zero-line snapshot a real
        # restart would.
        assert v["epp_restarted_in_windows_but_not_snapshot_pair"] is False, v
        assert v["scrape_gap_in_windows"] is True, v
        md = fairness_report.render_markdown(report)
        assert "Caveat (UNI-230)" in md
        assert "Caveat (UNI-163)" not in md
        assert "a metrics scrape failed mid-window at least once (UNI-230, not a restart)" in md


# UNI-164: per-group, per-window flow-control queue-wait distribution, from
# the upstream llm-d-router v0.11.0 Flow Control layer's own fairness_id-
# labelled histogram (already scraped by 15-fairness-benchmark.sh's
# snapshot_metrics since UNI-193 -- no EPP or benchmark-script change here,
# report-side only).

def test_compute_queue_wait_windows_computes_quantiles_per_window():
    schedule = {"app1": fairness_report.default_schedule_entry(20)}
    block0 = queue_wait_bucket_lines("app1", "Dispatched", [("0.01", 0), ("0.1", 0), ("1", 0), ("+Inf", 0)])
    block1 = queue_wait_bucket_lines("app1", "Dispatched", [("0.01", 50), ("0.1", 90), ("1", 100), ("+Inf", 100)])
    ts = [
        (0.0, "t0", fairness_report.parse_metrics_labeled_text(block0), False),
        (10.0, "t1", fairness_report.parse_metrics_labeled_text(block1), False),
    ]
    windows, restarted, scrape_gap = fairness_report.compute_queue_wait_windows(ts, schedule)
    assert restarted is False
    assert scrape_gap is False
    assert len(windows) == 1
    g = windows[0]["groups"][0]
    assert g["group"] == "app1" and g["state"] == "ok" and g["observations"] == 100
    assert abs(g["p50_seconds"] - 0.01) < 1e-9
    # Cross-check against the same Prometheus-quantile semantics the pick
    # latency section already tests, rather than a hand-derived constant.
    expected_p99, _ = fairness_report.histogram_quantile(
        0.99, {0.01: 50.0, 0.1: 90.0, 1.0: 100.0, float("inf"): 100.0})
    assert abs(g["p99_seconds"] - expected_p99) < 1e-9


def test_compute_queue_wait_windows_filters_outcome_dispatched_only():
    # A request evicted after a long TTL wait is not "served late" the way a
    # dispatched one is (see the Shed section for eviction accounting) -- its
    # queue time must not leak into the Dispatched quantiles for the same
    # fairness_id.
    schedule = {"app1": fairness_report.default_schedule_entry(20)}
    block0 = (queue_wait_bucket_lines("app1", "Dispatched", [("0.1", 0), ("+Inf", 0)]) +
              queue_wait_bucket_lines("app1", "EvictedTTL", [("0.1", 0), ("+Inf", 0)]))
    block1 = (queue_wait_bucket_lines("app1", "Dispatched", [("0.1", 10), ("+Inf", 10)]) +
              queue_wait_bucket_lines("app1", "EvictedTTL", [("0.1", 0), ("+Inf", 500)]))
    ts = [
        (0.0, "t0", fairness_report.parse_metrics_labeled_text(block0), False),
        (10.0, "t1", fairness_report.parse_metrics_labeled_text(block1), False),
    ]
    windows, _, _ = fairness_report.compute_queue_wait_windows(ts, schedule)
    g = windows[0]["groups"][0]
    assert g["observations"] == 10


def test_compute_queue_wait_windows_distinguishes_not_recorded_from_no_observations():
    schedule = {"app1": fairness_report.default_schedule_entry(20), "app2": fairness_report.default_schedule_entry(20)}
    block0 = queue_wait_bucket_lines("app1", "Dispatched", [("0.1", 20), ("+Inf", 20)])
    block1 = queue_wait_bucket_lines("app1", "Dispatched", [("0.1", 20), ("+Inf", 20)])  # unchanged
    ts = [
        (0.0, "t0", fairness_report.parse_metrics_labeled_text(block0), False),
        (10.0, "t1", fairness_report.parse_metrics_labeled_text(block1), False),
    ]
    windows, _, _ = fairness_report.compute_queue_wait_windows(ts, schedule)
    by_group = {g["group"]: g for g in windows[0]["groups"]}
    assert by_group["app1"]["state"] == "no_observations"
    assert by_group["app2"]["state"] == "not_recorded"


def test_compute_queue_wait_windows_flags_epp_restart_and_uses_post_restart_snapshot():
    schedule = {"app1": fairness_report.default_schedule_entry(20)}
    block0 = queue_wait_bucket_lines("app1", "Dispatched", [("0.1", 5000), ("+Inf", 5000)])
    block1 = queue_wait_bucket_lines("app1", "Dispatched", [("0.1", 8), ("+Inf", 10)])
    ts = [
        (0.0, "t0", fairness_report.parse_metrics_labeled_text(block0), False),
        (10.0, "t1", fairness_report.parse_metrics_labeled_text(block1), False),
    ]
    windows, restarted, scrape_gap = fairness_report.compute_queue_wait_windows(ts, schedule)
    assert restarted is True
    assert scrape_gap is False
    assert windows[0]["groups"][0]["observations"] == 10


def test_compute_queue_wait_windows_treats_failed_scrape_as_scrape_gap_not_restart():
    # UNI-230 sibling of the compute_windows case above: the same loop shape
    # (an "after" snapshot that scraped empty) appears here too.
    schedule = {"app1": fairness_report.default_schedule_entry(20)}
    block0 = queue_wait_bucket_lines("app1", "Dispatched", [("0.1", 5000), ("+Inf", 5000)])
    ts = [
        (0.0, "t0", fairness_report.parse_metrics_labeled_text(block0), False),
        (10.0, "t1", {}, True),  # scrape failed outright
    ]
    windows, restarted, scrape_gap = fairness_report.compute_queue_wait_windows(ts, schedule)
    assert restarted is False
    assert scrape_gap is True


def test_compute_queue_wait_windows_excludes_groups_without_schedule_entry():
    schedule = {"app1": fairness_report.default_schedule_entry(20)}
    block0 = (queue_wait_bucket_lines("app1", "Dispatched", [("0.1", 0), ("+Inf", 0)]) +
              queue_wait_bucket_lines("app2", "Dispatched", [("0.1", 0), ("+Inf", 0)]))
    block1 = (queue_wait_bucket_lines("app1", "Dispatched", [("0.1", 5), ("+Inf", 5)]) +
              queue_wait_bucket_lines("app2", "Dispatched", [("0.1", 50), ("+Inf", 50)]))
    ts = [
        (0.0, "t0", fairness_report.parse_metrics_labeled_text(block0), False),
        (10.0, "t1", fairness_report.parse_metrics_labeled_text(block1), False),
    ]
    windows, _, _ = fairness_report.compute_queue_wait_windows(ts, schedule)
    assert [g["group"] for g in windows[0]["groups"]] == ["app1"]


def test_queue_wait_integrates_into_timeline_section_and_markdown():
    with tempfile.TemporaryDirectory() as tmp:
        before = write(tmp, "before.txt", CONFIGURED_WEIGHT + ENFORCING_ON +
                       'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n')
        after = write(tmp, "after.txt", CONFIGURED_WEIGHT + ENFORCING_ON +
                      'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 2000\n')
        log = write(tmp, "loadgen.log", loadgen_log("app1", 32, 0, 0, 10, [
            ("app1", 500, "1.20", "2.40", "200=500"),
        ]))
        qw0 = queue_wait_bucket_lines("app1", "Dispatched", [("0.1", 0), ("+Inf", 0)])
        qw1 = queue_wait_bucket_lines("app1", "Dispatched", [("0.1", 40), ("+Inf", 50)])
        ts = write_timeseries_raw(tmp, "ts.txt", [
            (0, metrics_block({"app1": 0.0}) + qw0),
            (10, metrics_block({"app1": 2000.0}) + qw1),
        ])
        cfg = write_timeline_config(tmp, "timeline.json")
        report = fairness_report.build_report(
            scenario="test-scenario", enforce=True, duration_seconds=10, backend="vllm-gpu",
            epp_image_digest="sha256:deadbeef", namespace="maas-fairness-poc",
            epp_pod="test-pod", run_start="2026-11-01T00:00:00Z", run_end="2026-11-01T00:00:10Z",
            threshold_points=10.0, metrics_before_path=before, metrics_after_path=after,
            loadgen_log_path=log, metrics_timeseries_path=ts, timeline_config_path=cfg,
            window_seconds=10.0,
        )
        tl = report["timeline"]
        assert tl is not None
        qww = tl["queue_wait_windows"]
        assert len(qww) == 1
        g = qww[0]["groups"][0]
        assert g["group"] == "app1" and g["state"] == "ok" and g["observations"] == 50
        md = fairness_report.render_markdown(report)
        assert "Flow-control queue wait" in md
        json.dumps(report, allow_nan=False)


# UNI-137 (B5): open-loop (Poisson) generator support in parse_loadgen_log.
def test_parse_loadgen_log_detects_open_loop_generator():
    with tempfile.TemporaryDirectory() as tmp:
        log = write(tmp, "loadgen.log", open_loop_loadgen_log(
            4.0, 4.0, 4.0, 240,
            rows=[
                ("app1", 960, 72000, 0.75, 1.10, 1.50, "200=960"),
                ("app2", 958, 71800, 0.76, 1.12, 1.55, "200=958"),
                ("end-users", 961, 72100, 0.74, 1.09, 1.48, "200=961"),
            ],
        ))
        offered, rows, duration, generator = fairness_report.parse_loadgen_log(log)
        assert generator == "open-loop", generator
        assert offered == {"app1": 4.0, "app2": 4.0, "end-users": 4.0}, offered
        assert duration == 240.0, duration
        assert rows["app1"]["total"] == 960
        assert rows["app1"]["statuses"] == {"200": 960}
        assert abs(rows["end-users"]["p95_sec"] - 1.09) < 1e-9


def test_open_loop_below_saturation_reports_uncontended():
    # Mirrors UNI-34's own measured below-saturation levels: the clamp may
    # fire often, but contended_seconds_total stays near zero because the
    # pool is never actually backlogged -- same UNCONTENDED signature as
    # test_uncontended_when_everyone_below_capacity, reached via the
    # open-loop log shape instead of the closed-loop one.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app1"} 5.0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app2"} 5.0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="end-users"} 5.0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app1"} 5.1\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app2"} 5.1\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="end-users"} 5.1\n'
        )
        rows = [
            ("app1", 960, 72000, 0.75, 1.10, 1.50, "200=960"),
            ("app2", 958, 71800, 0.76, 1.12, 1.55, "200=958"),
            ("end-users", 961, 72100, 0.74, 1.09, 1.48, "200=961"),
        ]
        report = run_build_open_loop(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            rate_app1=4.0, rate_app2=4.0, rate_end=4.0, rows=rows,
            scenario="b5-open-loop-below-saturation",
        )
        assert report["run"]["generator"] == "open-loop", report["run"]
        assert report["verdict"]["result"] == "UNCONTENDED", report["verdict"]


def test_open_loop_below_saturation_reports_uncontended_when_metric_never_materialized():
    # Regression for the live UNI-137/B5 run (results/20261101T185150Z-uni-
    # 137-b5-below-saturation): a FRESH fairness_id's contended_seconds_total
    # and contended_service_tokens_total counters are lazily registered by
    # the EPP's Prometheus client and only appear once that group has been
    # contended at least once. A group offered at well under saturation (like
    # this scenario's end-users) can go an entire run without ever being
    # contended, which means its counter line is ABSENT from both
    # metrics-before.txt and metrics-after.txt -- not merely flat at the
    # before value. That is stronger evidence of zero contention than a
    # present, sub-threshold delta (test_open_loop_below_saturation_reports_
    # uncontended above), not weaker, so it must also score UNCONTENDED, not
    # FAIL ("offered groups delivered zero contended service tokens").
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 727921\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 389716\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app1"} 1.9654517519999992\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app2"} 1.9654517519999992\n'
        )
        tokens_after = (
            # end-users has no contended_service_tokens_total/contended_seconds_total
            # line at all -- never contended, so the EPP never registered the label.
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 727921\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 389716\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app1"} 1.9654517519999992\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app2"} 1.9654517519999992\n'
        )
        rows = [
            ("app1", 1100, 0, 0.8, 1.0, 1.2, "200=1100"),
            ("app2", 1198, 0, 0.8, 0.9, 1.1, "200=1198"),
            ("end-users", 1207, 0, 0.8, 1.0, 1.2, "200=1207"),
        ]
        report = run_build_open_loop(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            rate_app1=4.9, rate_app2=4.9, rate_end=4.9, rows=rows,
            scenario="b5-open-loop-below-saturation",
        )
        assert report["verdict"]["result"] == "UNCONTENDED", report["verdict"]


def test_open_loop_above_saturation_inverted_split_fails():
    # Mirrors UNI-34's own measured above-saturation result: end-users
    # (weight 65) delivered far less contended service than app1 (weight 20)
    # -- an inverted, not just skewed, split that must FAIL the symmetric
    # threshold check.
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="end-users"} 0\n'
        )
        tokens_after = (
            # 40.4% / 34.1% / 25.5% split -- UNI-34's own above-saturation numbers.
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 4040\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 3410\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 2550\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app1"} 12.0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="app2"} 13.0\n'
            'llm_d_epp_maas_fairness_contended_seconds_total{fairness_id="end-users"} 15.0\n'
        )
        rows = [
            ("app1", 731, 54000, 0.90, 25.0, 40.0, "200=731"),
            ("app2", 641, 48000, 0.95, 28.0, 42.0, "200=641"),
            ("end-users", 543, 40000, 1.10, 30.0, 45.0, "200=543"),
        ]
        report = run_build_open_loop(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            rate_app1=8.0, rate_app2=8.0, rate_end=8.0, rows=rows,
            scenario="b5-open-loop-above-saturation", duration=90,
        )
        assert report["verdict"]["result"] == "FAIL", report["verdict"]
        by_group = {g["group"]: g for g in report["groups"]}
        assert by_group["end-users"]["deviation_pts"] < -10
        assert by_group["app1"]["deviation_pts"] > 10


def test_render_markdown_labels_open_loop_rate_column():
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 0\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 0\n'
        )
        tokens_after = (
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 2000\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 1000\n'
            'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 6500\n'
        )
        rows = [
            ("app1", 100, 7500, 0.80, 1.00, 1.30, "200=100"),
            ("app2", 100, 7400, 0.80, 1.00, 1.30, "200=100"),
            ("end-users", 100, 7600, 0.80, 1.00, 1.30, "200=100"),
        ]
        report = run_build_open_loop(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            rate_app1=7.0, rate_app2=7.0, rate_end=7.0, rows=rows,
            scenario="b5-open-loop-at-saturation",
        )
        md = fairness_report.render_markdown(report)
        assert "offered req/s" in md
        assert "offered workers" not in md
        assert "| Generator | `open-loop` |" in md


# UNI-138 (G2): ledger cross-check -- client-recorded tokens vs the EPP's
# own core (ungated, unweighted) token histograms and the fairness plugin's
# (gated, cost-weighted) contended_service_tokens_total.
def client_record_jsonl(records):
    return "\n".join(json.dumps(r) for r in records) + "\n"


def run_build_with_ledger(tmp, *, tenants, w_app1, w_app2, w_end, rows,
                           contended_cost, input_tokens, output_tokens, cached_tokens,
                           client_records, input_token_weight=1.0, output_token_weight=2.0,
                           cached_input_token_weight=1.0, ledger_tolerance_pct=10.0,
                           duration=240, scenario="full-contention",
                           groups_line=None, extra_weights=""):
    def series(name, values):
        return "".join(f'{name}{{fairness_id="{g}"}} {v}\n' for g, v in values.items())

    before = write(tmp, "before.txt", CONFIGURED_WEIGHT + extra_weights + ENFORCING_ON)
    after = write(tmp, "after.txt", CONFIGURED_WEIGHT + extra_weights + ENFORCING_ON
                  + series("llm_d_epp_maas_fairness_contended_service_tokens_total", contended_cost)
                  + series("llm_d_epp_request_input_tokens_sum", input_tokens)
                  + series("llm_d_epp_request_output_tokens_sum", output_tokens)
                  + series("llm_d_epp_request_cached_tokens_sum", cached_tokens))
    log = write(tmp, "loadgen.log", loadgen_log(tenants, w_app1, w_app2, w_end, duration, rows,
                                                groups_line=groups_line))
    client_path = write(tmp, "client-request-summary.jsonl", client_record_jsonl(client_records))
    return fairness_report.build_report(
        scenario=scenario,
        enforce=True,
        duration_seconds=duration,
        backend="vllm-gpu (real)",
        epp_image_digest="sha256:deadbeef",
        namespace="maas-fairness-poc",
        epp_pod="maas-vllm-gpu-kserve-router-scheduler-test",
        run_start="2026-11-01T00:00:00Z",
        run_end="2026-11-01T00:04:00Z",
        threshold_points=10.0,
        metrics_before_path=before,
        metrics_after_path=after,
        loadgen_log_path=log,
        client_record_jsonl_path=client_path,
        input_token_weight=input_token_weight,
        output_token_weight=output_token_weight,
        cached_input_token_weight=cached_input_token_weight,
        ledger_tolerance_pct=ledger_tolerance_pct,
    )


LEDGER_TENANTS = "app1 app2 end-users"
LEDGER_ROWS = [
    ("app1", 1000, 0.80, 1.00, "200=1000"),
    ("app2", 1000, 0.80, 1.00, "200=1000"),
    ("end-users", 1000, 0.80, 1.00, "200=1000"),
]
# Chosen so expected cost (input*prompt + output*2*completion, cached=0) comes
# out exact: app1 100000+2*20000=140000, app2 90000+2*18000=126000,
# end-users 80000+2*16000=112000 -- see the module docstring's cost formula.
LEDGER_CLIENT_RECORDS = [
    {"group": "app1", "requests_sent": 1000, "status_tally": {"200": 1000}, "aborts": 0,
     "errors": 0, "prompt_tokens_total": 100000, "completion_tokens_total": 20000,
     "stream_requests": 0, "max_tokens_omitted": 0, "max_tokens_huge": 0,
     "long_generations": 0, "forged_fairness_id": 0},
    {"group": "app2", "requests_sent": 1000, "status_tally": {"200": 1000}, "aborts": 0,
     "errors": 0, "prompt_tokens_total": 90000, "completion_tokens_total": 18000,
     "stream_requests": 0, "max_tokens_omitted": 0, "max_tokens_huge": 0,
     "long_generations": 0, "forged_fairness_id": 0},
    {"group": "end-users", "requests_sent": 1000, "status_tally": {"200": 1000}, "aborts": 0,
     "errors": 0, "prompt_tokens_total": 80000, "completion_tokens_total": 16000,
     "stream_requests": 0, "max_tokens_omitted": 0, "max_tokens_huge": 0,
     "long_generations": 0, "forged_fairness_id": 0},
]
LEDGER_INPUT_TOKENS = {"app1": 100000, "app2": 90000, "end-users": 80000}
LEDGER_OUTPUT_TOKENS = {"app1": 20000, "app2": 18000, "end-users": 16000}
LEDGER_CACHED_TOKENS = {"app1": 0, "app2": 0, "end-users": 0}
LEDGER_CONTENDED_COST = {"app1": 140000, "app2": 126000, "end-users": 112000}


def test_ledger_section_absent_without_client_record_arg():
    with tempfile.TemporaryDirectory() as tmp:
        tokens_before = 'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 0\n'
        tokens_after = 'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 100\n'
        report = run_build(
            tmp, tokens_before=tokens_before, tokens_after=tokens_after,
            tenants="app1", w_app1=32, w_app2=0, w_end=0,
            rows=[("app1", 10, 0.8, 1.0, "200=10")],
        )
        assert report["ledger"] is None
        md = fairness_report.render_markdown(report)
        assert "N/A: no `--client-record-jsonl`" in md


def test_ledger_passes_when_epp_accounting_matches_client():
    with tempfile.TemporaryDirectory() as tmp:
        report = run_build_with_ledger(
            tmp, tenants=LEDGER_TENANTS, w_app1=32, w_app2=32, w_end=128, rows=LEDGER_ROWS,
            contended_cost=LEDGER_CONTENDED_COST, input_tokens=LEDGER_INPUT_TOKENS,
            output_tokens=LEDGER_OUTPUT_TOKENS, cached_tokens=LEDGER_CACHED_TOKENS,
            client_records=LEDGER_CLIENT_RECORDS,
        )
        ledger = report["ledger"]
        assert ledger["verdict"]["result"] == "PASS", ledger["verdict"]["reasons"]
        for row in ledger["rows"]:
            assert row["within_tolerance"] is True, row
            assert abs(row["raw_tokens_pct_diff"]) < 1e-6
            assert abs(row["cost_pct_diff"]) < 1e-6
        # Unaffected: the weighted-split verdict is a different check.
        assert report["verdict"]["result"] in ("PASS", "FAIL")
        md = fairness_report.render_markdown(report)
        assert "Ledger verdict: PASS" in md


def test_ledger_fails_on_raw_token_mismatch_but_not_cost():
    with tempfile.TemporaryDirectory() as tmp:
        skewed_input = dict(LEDGER_INPUT_TOKENS, **{"end-users": 200000})
        report = run_build_with_ledger(
            tmp, tenants=LEDGER_TENANTS, w_app1=32, w_app2=32, w_end=128, rows=LEDGER_ROWS,
            contended_cost=LEDGER_CONTENDED_COST, input_tokens=skewed_input,
            output_tokens=LEDGER_OUTPUT_TOKENS, cached_tokens=LEDGER_CACHED_TOKENS,
            client_records=LEDGER_CLIENT_RECORDS,
        )
        ledger = report["ledger"]
        assert ledger["verdict"]["result"] == "FAIL"
        assert any("end-users" in r and "raw tokens" in r for r in ledger["verdict"]["reasons"])
        app1_row = next(r for r in ledger["rows"] if r["group"] == "app1")
        assert app1_row["within_tolerance"] is True


def test_ledger_fails_on_contended_cost_mismatch_but_not_raw_tokens():
    with tempfile.TemporaryDirectory() as tmp:
        skewed_cost = dict(LEDGER_CONTENDED_COST, **{"app1": 50000})
        report = run_build_with_ledger(
            tmp, tenants=LEDGER_TENANTS, w_app1=32, w_app2=32, w_end=128, rows=LEDGER_ROWS,
            contended_cost=skewed_cost, input_tokens=LEDGER_INPUT_TOKENS,
            output_tokens=LEDGER_OUTPUT_TOKENS, cached_tokens=LEDGER_CACHED_TOKENS,
            client_records=LEDGER_CLIENT_RECORDS,
        )
        ledger = report["ledger"]
        assert ledger["verdict"]["result"] == "FAIL"
        assert any("app1" in r and "cost" in r for r in ledger["verdict"]["reasons"])
        app1_row = next(r for r in ledger["rows"] if r["group"] == "app1")
        assert abs(app1_row["raw_tokens_pct_diff"]) < 1e-6
        assert app1_row["within_tolerance"] is False


def test_ledger_fails_when_offered_group_has_no_client_record():
    with tempfile.TemporaryDirectory() as tmp:
        partial_records = [r for r in LEDGER_CLIENT_RECORDS if r["group"] != "end-users"]
        report = run_build_with_ledger(
            tmp, tenants=LEDGER_TENANTS, w_app1=32, w_app2=32, w_end=128, rows=LEDGER_ROWS,
            contended_cost=LEDGER_CONTENDED_COST, input_tokens=LEDGER_INPUT_TOKENS,
            output_tokens=LEDGER_OUTPUT_TOKENS, cached_tokens=LEDGER_CACHED_TOKENS,
            client_records=partial_records,
        )
        ledger = report["ledger"]
        assert ledger["verdict"]["result"] == "FAIL"
        assert any("end-users" in r and "no client-side record" in r for r in ledger["verdict"]["reasons"])
        missing_row = next(r for r in ledger["rows"] if r["group"] == "end-users")
        assert missing_row["within_tolerance"] is None


# --- UNI-181: shed rate, EPP pick latency, alert fire/clear ------------------

CONVERGED_TOKENS_BEFORE = (
    'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 1000\n'
    'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 1000\n'
    'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 1000\n'
)
CONVERGED_TOKENS_AFTER = (
    'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app1"} 3100\n'
    'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="app2"} 2000\n'
    'llm_d_epp_maas_fairness_contended_service_tokens_total{fairness_id="end-users"} 7900\n'
)


def histogram_lines(name, cumulative):
    """Prometheus text for an unlabelled histogram. `cumulative` is
    [(le, count)], with le="+Inf" last."""
    out = "".join(f'{name}_bucket{{le="{le}"}} {c}\n' for le, c in cumulative)
    return out + f"{name}_count {cumulative[-1][1]}\n"


def flow_outcomes(counts):
    return "".join(
        f'llm_d_epp_flow_control_requests_total{{inference_pool="maas-vllm-gpu-inference-pool",'
        f'outcome="{o}",priority="0"}} {v}\n' for o, v in counts.items()
    )


def run_build_uni181(tmp, *, rows, extra_before="", extra_after="", tenants="app1 app2 end-users",
                     **kwargs):
    before = write(tmp, "before.txt", CONFIGURED_WEIGHT + ENFORCING_ON + CONVERGED_TOKENS_BEFORE + extra_before)
    after = write(tmp, "after.txt", CONFIGURED_WEIGHT + ENFORCING_ON + CONVERGED_TOKENS_AFTER + extra_after)
    log = write(tmp, "loadgen.log", loadgen_log(tenants, 32, 32, 32, 240, rows))
    return fairness_report.build_report(
        scenario="full-contention", enforce=True, duration_seconds=240, backend="vllm-gpu",
        epp_image_digest="sha256:deadbeef", namespace="maas-fairness-poc",
        epp_pod="maas-vllm-gpu-kserve-router-scheduler-test",
        run_start="2026-11-01T00:00:00Z", run_end="2026-11-01T00:04:00Z", threshold_points=10.0,
        metrics_before_path=before, metrics_after_path=after, loadgen_log_path=log, **kwargs,
    )


CLEAN_ROWS = [
    ("app1", 500, "1.20", "2.40", "200=500"),
    ("app2", 480, "1.30", "2.50", "200=480"),
    ("end-users", 510, "1.10", "2.30", "200=510"),
]


def test_uni181_sections_are_additive_and_leave_existing_fields_unchanged():
    with tempfile.TemporaryDirectory() as tmp:
        report = run_build_uni181(tmp, rows=CLEAN_ROWS)
        with tempfile.TemporaryDirectory() as tmp2:
            baseline = run_build(
                tmp2, tokens_before=CONVERGED_TOKENS_BEFORE, tokens_after=CONVERGED_TOKENS_AFTER,
                tenants="app1 app2 end-users", w_app1=32, w_app2=32, w_end=32, rows=CLEAN_ROWS,
                scenario="full-contention",
            )
        assert report["verdict"] == baseline["verdict"]
        assert report["groups"] == baseline["groups"]
        assert report["sources"] == baseline["sources"]
        assert {"shed", "pick_latency", "alerts"} <= set(report)
        for g in report["groups"]:
            assert not any(k.startswith("shed") for k in g), g


def test_shed_rate_per_group_against_weight_share():
    with tempfile.TemporaryDirectory() as tmp:
        rows = [
            ("app1", 500, "1.20", "2.40", "200=470 429=30"),
            ("app2", 480, "1.30", "2.50", "200=420 429=50 503=10"),
            ("end-users", 510, "1.10", "2.30", "200=510"),
        ]
        report = run_build_uni181(tmp, rows=rows)
        s = report["shed"]
        by = {r["group"]: r for r in s["rows"]}
        assert s["total_shed"] == 90
        assert by["app1"]["shed"] == 30 and by["app1"]["state"] == "shed"
        assert abs(by["app1"]["shed_rate_pct"] - 6.0) < 1e-9
        assert by["app2"]["status_429"] == 50 and by["app2"]["status_503"] == 10
        # offered weight total 95: app2 weight share 10.53%, shed share 66.67% -> ~6.3x its weight
        assert abs(by["app2"]["weight_share_pct"] - 100 * 10 / 95) < 1e-9
        assert abs(by["app2"]["shed_share_pct"] - 100 * 60 / 90) < 1e-9
        assert abs(by["app2"]["shed_share_vs_weight_share"] - (60 / 90) / (10 / 95)) < 1e-9
        # Degenerate: a group with no shed events at all is a measured zero, not unknown.
        assert by["end-users"]["state"] == "never_shed"
        assert by["end-users"]["shed"] == 0 and by["end-users"]["shed_share_pct"] == 0.0
        md = fairness_report.render_markdown(report)
        assert "| end-users | 510 | 0 | 0 | 0 (never shed) |" in md, md
        # The verdict stays the weighted-split verdict -- shed adds no PASS/FAIL.
        assert report["verdict"]["result"] == "PASS"


def test_shed_run_with_nothing_shed_says_so_rather_than_dividing_by_zero():
    with tempfile.TemporaryDirectory() as tmp:
        report = run_build_uni181(tmp, rows=CLEAN_ROWS)
        s = report["shed"]
        assert s["total_shed"] == 0
        assert all(r["state"] == "never_shed" and r["shed_share_pct"] is None for r in s["rows"])
        md = fairness_report.render_markdown(report)
        assert "n/a (nothing shed)" in md


def test_shed_group_missing_from_loadgen_table_is_not_recorded_not_zero():
    with tempfile.TemporaryDirectory() as tmp:
        report = run_build_uni181(tmp, rows=CLEAN_ROWS[:2])
        by = {r["group"]: r for r in report["shed"]["rows"]}
        assert by["end-users"]["state"] == "not_recorded"
        assert by["end-users"]["shed"] is None
        md = fairness_report.render_markdown(report)
        assert "| end-users | not recorded (no loadgen row) |" in md


def test_shed_epp_pool_wide_splits_epp_429_from_non_epp_429():
    with tempfile.TemporaryDirectory() as tmp:
        rows = [
            ("app1", 500, "1.20", "2.40", "200=470 429=30"),
            ("app2", 480, "1.30", "2.50", "200=430 429=50"),
            ("end-users", 510, "1.10", "2.30", "200=510"),
        ]
        report = run_build_uni181(
            tmp, rows=rows,
            extra_before=flow_outcomes({"Dispatched": 1000}),
            # RejectedCapacity materialized during the run; EvictedTTL never did,
            # so it is absent from both snapshots -- that must read as 0.
            extra_after=flow_outcomes({"Dispatched": 2400, "RejectedCapacity": 20,
                                       "EvictedContextCancelled": 7}),
        )
        e = report["shed"]["epp_pool_wide"]
        assert e["state"] == "ok"
        assert e["outcome_deltas"]["RejectedCapacity"] == 20
        assert e["outcome_deltas"].get("EvictedTTL", 0) == 0
        # Client cancellations are not the EPP shedding.
        assert e["epp_shed_total"] == 20
        assert e["client_429_total"] == 80
        assert e["epp_429_upper_bound"] == 20
        assert e["non_epp_429_lower_bound"] == 60
        md = fairness_report.render_markdown(report)
        assert "at least 60 came from elsewhere" in md


def test_shed_epp_pool_wide_not_recorded_when_family_absent():
    with tempfile.TemporaryDirectory() as tmp:
        report = run_build_uni181(tmp, rows=CLEAN_ROWS)
        e = report["shed"]["epp_pool_wide"]
        assert e["state"] == "not_recorded" and e["epp_shed_total"] is None
        assert "not recorded" in fairness_report.render_markdown(report)


def test_histogram_quantile_matches_prometheus_interpolation():
    inf = float("inf")
    buckets = {0.001: 50.0, 0.002: 90.0, 0.005: 100.0, inf: 100.0}
    v, b = fairness_report.histogram_quantile(0.5, buckets)
    assert abs(v - 0.001) < 1e-12 and b == (0.0, 0.001)
    v, b = fairness_report.histogram_quantile(0.7, buckets)
    assert abs(v - 0.0015) < 1e-12 and b == (0.001, 0.002)
    v, b = fairness_report.histogram_quantile(0.99, buckets)
    assert abs(v - (0.002 + 0.003 * 9 / 10)) < 1e-12
    # Rank in +Inf: highest finite bound, as Prometheus returns.
    v, b = fairness_report.histogram_quantile(0.99, {0.001: 10.0, inf: 100.0})
    assert v == 0.001 and b == (0.001, inf)
    assert fairness_report.histogram_quantile(0.5, {0.001: 0.0, inf: 0.0}) == (None, None)


SCHED = "llm_d_epp_scheduler_e2e_duration_seconds"
CYCLE = "llm_d_epp_flow_control_dispatch_cycle_duration_seconds"


def test_pick_latency_p50_p99_from_before_after_delta():
    with tempfile.TemporaryDirectory() as tmp:
        before = histogram_lines(SCHED, [("0.0001", 100), ("0.0002", 100), ("0.0005", 100), ("+Inf", 100)])
        # This run adds 1000 picks: 500 <=0.1ms, 400 in (0.1,0.2], 100 in (0.2,0.5].
        after = histogram_lines(SCHED, [("0.0001", 600), ("0.0002", 1000), ("0.0005", 1100), ("+Inf", 1100)])
        report = run_build_uni181(tmp, rows=CLEAN_ROWS, extra_before=before, extra_after=after)
        h = report["pick_latency"]["histograms"]["scheduler_e2e"]
        assert h["state"] == "ok" and h["observations"] == 1000
        assert abs(h["p50_seconds"] - 0.0001) < 1e-12
        assert abs(h["p99_seconds"] - (0.0002 + 0.0003 * 90 / 100)) < 1e-12
        assert h["p99_bucket"] == [0.0002, 0.0005] and h["p99_at_histogram_ceiling"] is False
        # The other histogram was not in either snapshot: unknown, not zero.
        assert report["pick_latency"]["histograms"]["flow_control_dispatch_cycle"]["state"] == "not_recorded"
        json.dumps(report, allow_nan=False)  # +Inf bucket bounds must stay valid JSON


def test_pick_latency_missing_histogram_says_not_recorded():
    with tempfile.TemporaryDirectory() as tmp:
        report = run_build_uni181(tmp, rows=CLEAN_ROWS)
        for h in report["pick_latency"]["histograms"].values():
            assert h["state"] == "not_recorded" and h["p50_seconds"] is None
        md = fairness_report.render_markdown(report)
        assert "not recorded (absent from both snapshots)" in md


def test_pick_latency_no_observations_during_run_is_distinct_from_missing():
    with tempfile.TemporaryDirectory() as tmp:
        same = histogram_lines(CYCLE, [("0.0001", 50), ("+Inf", 50)])
        report = run_build_uni181(tmp, rows=CLEAN_ROWS, extra_before=same, extra_after=same)
        h = report["pick_latency"]["histograms"]["flow_control_dispatch_cycle"]
        assert h["state"] == "no_observations" and h["observations"] == 0
        assert "no picks during the run" in fairness_report.render_markdown(report)


def test_pick_latency_flags_p99_above_top_bucket_and_compares_to_baseline():
    with tempfile.TemporaryDirectory() as tmp:
        base_after = histogram_lines(SCHED, [("0.0001", 900), ("0.0002", 1000), ("0.1", 1000), ("+Inf", 1000)])
        base = run_build_uni181(tmp, rows=CLEAN_ROWS, extra_after=base_after)
        base_path = write(tmp, "baseline.json", json.dumps(base))
        slow_after = histogram_lines(SCHED, [("0.0001", 100), ("0.0002", 500), ("0.1", 900), ("+Inf", 1000)])
        report = run_build_uni181(tmp, rows=CLEAN_ROWS, extra_after=slow_after,
                                  pick_latency_baseline_path=base_path)
        h = report["pick_latency"]["histograms"]["scheduler_e2e"]
        assert h["p99_at_histogram_ceiling"] is True and h["p99_seconds"] == 0.1
        assert h["p99_bucket"] == [0.1, "+Inf"]
        b = base["pick_latency"]["histograms"]["scheduler_e2e"]
        assert abs(h["p50_vs_baseline"] - h["p50_seconds"] / b["p50_seconds"]) < 1e-12
        assert report["pick_latency"]["baseline_has_pick_latency"] is True
        assert "(above top bucket)" in fairness_report.render_markdown(report)


def test_pick_latency_counter_reset_uses_post_restart_histogram():
    with tempfile.TemporaryDirectory() as tmp:
        before = histogram_lines(SCHED, [("0.0001", 5000), ("+Inf", 5000)])
        after = histogram_lines(SCHED, [("0.0001", 10), ("0.0002", 20), ("+Inf", 20)])
        report = run_build_uni181(tmp, rows=CLEAN_ROWS, extra_before=before, extra_after=after)
        assert report["pick_latency"]["epp_restarted"] is True
        assert report["pick_latency"]["histograms"]["scheduler_e2e"]["observations"] == 20


RUN0 = 1793491200  # 2026-11-01T00:00:00Z, run_build_uni181's run_start


def alert_series(name, state, offsets, **labels):
    return {"metric": {"__name__": "ALERTS", "alertname": name, "alertstate": state, **labels},
            "values": [[RUN0 + o, "1"] for o in offsets]}


def test_alerts_absent_means_unknown_not_none_fired():
    with tempfile.TemporaryDirectory() as tmp:
        report = run_build_uni181(tmp, rows=CLEAN_ROWS)
        assert report["alerts"] is None
        assert "unknown (not \"none fired\")" in fairness_report.render_markdown(report)


def test_alerts_run_with_no_alerts_lists_every_rule_as_never_fired():
    with tempfile.TemporaryDirectory() as tmp:
        alerts = write(tmp, "alerts.json", json.dumps({"status": "success",
                                                       "data": {"resultType": "matrix", "result": []}}))
        rules = os.path.join(HERE, "..", "prometheusrule.yaml")
        report = run_build_uni181(tmp, rows=CLEAN_ROWS, alerts_path=alerts, alert_rules_path=rules)
        a = report["alerts"]
        assert a["episodes"] == []
        names = [r["alertname"] for r in a["summary"]]
        assert names == ["MaasFairnessNotConverging", "MaasFairnessClassificationBroken",
                         "MaasFairnessBandSplit", "MaasFairnessSheddingIsRealAllocator",
                         "MaasFairnessAccountingLeak"], names
        assert all(r["status"] == "never_fired" for r in a["summary"])
        assert "- MaasFairnessBandSplit: never fired" in fairness_report.render_markdown(report)


def test_alerts_fire_and_clear_relative_to_run_start():
    with tempfile.TemporaryDirectory() as tmp:
        doc = {
            "query": 'ALERTS{alertname=~"MaasFairness.*"}', "step_seconds": 30, "end": RUN0 + 600,
            "result": [
                alert_series("MaasFairnessBandSplit", "pending", [60, 90, 120]),
                alert_series("MaasFairnessBandSplit", "firing", [150, 180, 210]),
                # Two separate episodes: a gap wider than 1.5 steps between them.
                alert_series("MaasFairnessNotConverging", "firing", [300, 330, 450, 480, 510]),
                # Still firing at the last sample of the export: no clear time.
                alert_series("MaasFairnessAccountingLeak", "firing", [540, 570, 600], fairness_id="app2"),
                alert_series("MaasFairnessClassificationBroken", "pending", [200, 230]),
            ],
        }
        alerts = write(tmp, "alerts.json", json.dumps(doc))
        report = run_build_uni181(tmp, rows=CLEAN_ROWS, alerts_path=alerts)
        eps = report["alerts"]["episodes"]
        band = [e for e in eps if e["alertname"] == "MaasFairnessBandSplit" and e["alertstate"] == "firing"]
        assert len(band) == 1 and band[0]["started_s"] == 150 and band[0]["cleared_s"] == 240
        assert band[0]["duration_s"] == 90
        nc = [e for e in eps if e["alertname"] == "MaasFairnessNotConverging"]
        assert [(e["started_s"], e["cleared_s"]) for e in nc] == [(300, 360), (450, 540)]
        leak = next(e for e in eps if e["alertname"] == "MaasFairnessAccountingLeak")
        assert leak["still_active_at_export_end"] is True and leak["cleared_s"] is None
        assert leak["labels"] == {"fairness_id": "app2"}
        # 600s is past the 240s run end -- a fire after the run is flagged, not hidden.
        assert leak["started_after_run_end"] is True
        status = {r["alertname"]: r["status"] for r in report["alerts"]["summary"]}
        assert status["MaasFairnessClassificationBroken"] == "pending_only"
        assert status["MaasFairnessBandSplit"] == "fired"
        md = fairness_report.render_markdown(report)
        assert "still active at export end" in md
        assert "MaasFairnessClassificationBroken: pending, never fired" in md


def test_alerts_raw_query_range_response_uses_step_flag():
    with tempfile.TemporaryDirectory() as tmp:
        raw = {"status": "success", "data": {"resultType": "matrix", "result": [
            alert_series("MaasFairnessBandSplit", "firing", [0, 15, 30]),
            alert_series("MaasFairnessBandSplit", "firing", [100, 115], fairness_id="x"),
        ]}}
        alerts = write(tmp, "alerts.json", json.dumps(raw))
        report = run_build_uni181(tmp, rows=CLEAN_ROWS, alerts_path=alerts, alerts_step_seconds=15)
        first = next(e for e in report["alerts"]["episodes"] if not e["labels"])
        # Without an explicit "end", the export's last sample (115) bounds it; this one cleared.
        assert first["cleared_s"] == 45 and first["still_active_at_export_end"] is False


def test_cli_accepts_uni181_flags_end_to_end():
    with tempfile.TemporaryDirectory() as tmp:
        before = write(tmp, "before.txt", CONFIGURED_WEIGHT + ENFORCING_ON + CONVERGED_TOKENS_BEFORE)
        after = write(tmp, "after.txt", CONFIGURED_WEIGHT + ENFORCING_ON + CONVERGED_TOKENS_AFTER
                      + histogram_lines(SCHED, [("0.0001", 10), ("+Inf", 10)]))
        log = write(tmp, "loadgen.log", loadgen_log("app1 app2 end-users", 32, 32, 32, 240, CLEAN_ROWS))
        alerts = write(tmp, "alerts.json", json.dumps({"result": [], "step_seconds": 30}))
        out_json, out_md = os.path.join(tmp, "r.json"), os.path.join(tmp, "r.md")
        proc = subprocess.run(
            [sys.executable, "-I", os.path.join(HERE, "15-fairness-report.py"),
             "--scenario", "full-contention", "--enforce", "true", "--backend", "sim",
             "--epp-image-digest", "sha256:x", "--namespace", "ns", "--epp-pod", "p",
             "--run-start", "2026-11-01T00:00:00Z", "--run-end", "2026-11-01T00:04:00Z",
             "--metrics-before", before, "--metrics-after", after, "--loadgen-log", log,
             "--alerts-json", alerts, "--alert-rules", os.path.join(HERE, "..", "prometheusrule.yaml"),
             "--alerts-step-seconds", "15", "--out-json", out_json, "--out-md", out_md],
            capture_output=True, text=True,
        )
        assert proc.returncode == 0, proc.stderr
        report = json.load(open(out_json))
        assert report["pick_latency"]["histograms"]["scheduler_e2e"]["state"] == "ok"
        assert len(report["alerts"]["summary"]) == 5


# UNI-179: 04-loadgen.yaml's run.sh logs "load: UNI-179 groups=[...]" for
# any declared group set. For the default three groups that line must change
# nothing; for N groups it must bring app3..appN into the table rows and the
# G2 ledger, and must never bring in "custom" (its fairness id is its
# subscription's, not the literal name).
def test_default_groups_line_changes_nothing():
    with tempfile.TemporaryDirectory() as tmp:
        kwargs = dict(tenants=LEDGER_TENANTS, w_app1=32, w_app2=32, w_end=128, rows=LEDGER_ROWS,
                      contended_cost=LEDGER_CONTENDED_COST, input_tokens=LEDGER_INPUT_TOKENS,
                      output_tokens=LEDGER_OUTPUT_TOKENS, cached_tokens=LEDGER_CACHED_TOKENS,
                      client_records=LEDGER_CLIENT_RECORDS)
        without = run_build_with_ledger(tmp, **kwargs)
        with_line = run_build_with_ledger(
            tmp, groups_line="load: UNI-179 groups=[app1=32 app2=32 end-users=128] total-workers=192", **kwargs)
        assert json.dumps(without, sort_keys=True) == json.dumps(with_line, sort_keys=True)
        assert fairness_report.render_markdown(without) == fairness_report.render_markdown(with_line)


def test_n_groups_line_extends_rows_and_ledger_but_not_custom():
    extra = ["app3", "app4", "app5"]
    rows = LEDGER_ROWS + [(g, 1000, 0.80, 1.00, "200=1000") for g in extra] + [("custom", 50, 0.8, 1.0, "200=50")]
    records = list(LEDGER_CLIENT_RECORDS) + [
        dict(LEDGER_CLIENT_RECORDS[0], group=g) for g in extra
    ] + [dict(LEDGER_CLIENT_RECORDS[0], group="custom", requests_sent=50)]
    per = lambda base, v: dict(base, **{g: v for g in extra})
    weights = "".join(f'llm_d_epp_maas_fairness_configured_weight{{fairness_id="{g}"}} 20\n' for g in extra)
    with tempfile.TemporaryDirectory() as tmp:
        report = run_build_with_ledger(
            tmp, tenants="app1 app2 end-users app3 app4 app5 custom", w_app1=32, w_app2=32, w_end=128,
            rows=rows,
            contended_cost=per(LEDGER_CONTENDED_COST, 140000),
            input_tokens=per(LEDGER_INPUT_TOKENS, 100000),
            output_tokens=per(LEDGER_OUTPUT_TOKENS, 20000),
            cached_tokens=per(LEDGER_CACHED_TOKENS, 0),
            client_records=records,
            groups_line="load: UNI-179 groups=[app1=32 app2=32 end-users=128 app3=16 app4=16 app5=16 custom=4] total-workers=244",
            extra_weights=weights,
        )
        ledger_groups = [r["group"] for r in report["ledger"]["rows"]]
        assert ledger_groups == ["app1", "app2", "end-users", "app3", "app4", "app5"], ledger_groups
        assert report["ledger"]["verdict"]["result"] == "PASS", report["ledger"]["verdict"]["reasons"]
        md = fairness_report.render_markdown(report)
        for g in extra:
            assert g in md, g
        assert "custom" not in ledger_groups


def test_n_groups_line_missing_client_record_fails_ledger():
    # The point of extending the group set: an app4 that was offered load but
    # whose client record went missing must FAIL the ledger, not vanish.
    extra = ["app3", "app4"]
    rows = LEDGER_ROWS + [(g, 1000, 0.80, 1.00, "200=1000") for g in extra]
    records = list(LEDGER_CLIENT_RECORDS) + [dict(LEDGER_CLIENT_RECORDS[0], group="app3")]
    per = lambda base, v: dict(base, **{g: v for g in extra})
    with tempfile.TemporaryDirectory() as tmp:
        report = run_build_with_ledger(
            tmp, tenants="app1 app2 end-users app3 app4", w_app1=32, w_app2=32, w_end=128, rows=rows,
            contended_cost=per(LEDGER_CONTENDED_COST, 140000),
            input_tokens=per(LEDGER_INPUT_TOKENS, 100000),
            output_tokens=per(LEDGER_OUTPUT_TOKENS, 20000),
            cached_tokens=per(LEDGER_CACHED_TOKENS, 0),
            client_records=records,
            groups_line="load: UNI-179 groups=[app1=32 app2=32 end-users=128 app3=16 app4=16] total-workers=224",
        )
        assert report["ledger"]["verdict"]["result"] == "FAIL"
        assert any("app4" in r for r in report["ledger"]["verdict"]["reasons"]), report["ledger"]["verdict"]["reasons"]


# UNI-226: per-tenant TTFT/ITL, from the upstream llm-d-router v0.11.0
# framework's own fairness_id-labelled histograms (already scraped by
# 15-fairness-benchmark.sh's snapshot_metrics since this ticket -- report-side
# tests only, same split as the UNI-164 queue-wait tests above).

def ttft_bucket_lines(fairness_id, cumulative, streaming="true"):
    """Prometheus text for llm_d_epp_request_ttft_seconds, labelled the way
    llm-d-router v0.11.0 actually emits it (model_name, target_model_name,
    fairness_id, priority, streaming). `cumulative` is [(le, count)], with
    le="+Inf" last."""
    name = "llm_d_epp_request_ttft_seconds"
    return "".join(
        f'{name}_bucket{{model_name="llama-3-1-8b",target_model_name="llama-3-1-8b",'
        f'fairness_id="{fairness_id}",priority="0",streaming="{streaming}",le="{le}"}} {c}\n'
        for le, c in cumulative
    )


def itl_bucket_lines(fairness_id, cumulative):
    """Prometheus text for llm_d_epp_request_streaming_itl_seconds -- same
    label set as TTFT minus `streaming` (ITL is streaming-only by
    definition, so the metric carries no such label)."""
    name = "llm_d_epp_request_streaming_itl_seconds"
    return "".join(
        f'{name}_bucket{{model_name="llama-3-1-8b",target_model_name="llama-3-1-8b",'
        f'fairness_id="{fairness_id}",priority="0",le="{le}"}} {c}\n'
        for le, c in cumulative
    )


def test_compute_ttft_itl_whole_run_ok_not_recorded_no_observations():
    same_itl = itl_bucket_lines("app1", [("0.01", 40), ("+Inf", 40)])  # identical both sides: no new streaming
    before = ttft_bucket_lines("app1", [("0.1", 0), ("1", 0), ("+Inf", 0)]) + same_itl
    after = ttft_bucket_lines("app1", [("0.1", 50), ("1", 100), ("+Inf", 100)]) + same_itl
    before_labeled = fairness_report.parse_metrics_labeled_text(before)
    after_labeled = fairness_report.parse_metrics_labeled_text(after)
    result = fairness_report.compute_ttft_itl_whole_run(before_labeled, after_labeled, ["app1", "app2"])
    app1 = result["groups"]["app1"]
    assert app1["ttft"]["state"] == "ok" and app1["ttft"]["observations"] == 100
    assert abs(app1["ttft"]["p50_seconds"] - 0.1) < 1e-9
    # ITL count did not move between the two snapshots: captured, but no
    # streaming happened in this run for app1.
    assert app1["itl"]["state"] == "no_observations"
    # app2 was never in either snapshot at all: unknown, not zero.
    app2 = result["groups"]["app2"]
    assert app2["ttft"]["state"] == "not_recorded"
    assert app2["itl"]["state"] == "not_recorded"
    # Pool level sums across fairness_id.
    assert result["pool"]["ttft"]["observations"] == 100


def test_compute_ttft_itl_whole_run_pool_sums_across_groups():
    before = ttft_bucket_lines("app1", [("0.1", 0), ("+Inf", 0)]) + ttft_bucket_lines("app2", [("0.1", 0), ("+Inf", 0)])
    after = ttft_bucket_lines("app1", [("0.1", 30), ("+Inf", 30)]) + ttft_bucket_lines("app2", [("0.1", 70), ("+Inf", 70)])
    result = fairness_report.compute_ttft_itl_whole_run(
        fairness_report.parse_metrics_labeled_text(before),
        fairness_report.parse_metrics_labeled_text(after),
        ["app1", "app2"],
    )
    assert result["pool"]["ttft"]["observations"] == 100


def test_compute_ttft_itl_windows_mirrors_queue_wait_window_shape():
    schedule = {"app1": fairness_report.default_schedule_entry(20)}
    block0 = ttft_bucket_lines("app1", [("0.1", 0), ("1", 0), ("+Inf", 0)]) + itl_bucket_lines("app1", [("0.01", 0), ("+Inf", 0)])
    block1 = ttft_bucket_lines("app1", [("0.1", 50), ("1", 100), ("+Inf", 100)]) + itl_bucket_lines("app1", [("0.01", 400), ("+Inf", 400)])
    ts = [
        (0.0, "t0", fairness_report.parse_metrics_labeled_text(block0), False),
        (10.0, "t1", fairness_report.parse_metrics_labeled_text(block1), False),
    ]
    windows, restarted, scrape_gap = fairness_report.compute_ttft_itl_windows(ts, schedule)
    assert restarted is False and scrape_gap is False
    assert len(windows) == 1
    g = windows[0]["groups"][0]
    assert g["group"] == "app1"
    assert g["ttft"]["state"] == "ok" and g["ttft"]["observations"] == 100
    assert abs(g["ttft"]["p50_seconds"] - 0.1) < 1e-9
    assert g["itl"]["state"] == "ok" and g["itl"]["observations"] == 400


def test_compute_ttft_itl_windows_flags_restart_like_queue_wait():
    schedule = {"app1": fairness_report.default_schedule_entry(20)}
    block0 = ttft_bucket_lines("app1", [("0.1", 5000), ("+Inf", 5000)])
    block1 = ttft_bucket_lines("app1", [("0.1", 8), ("+Inf", 10)])
    ts = [
        (0.0, "t0", fairness_report.parse_metrics_labeled_text(block0), False),
        (10.0, "t1", fairness_report.parse_metrics_labeled_text(block1), False),
    ]
    windows, restarted, scrape_gap = fairness_report.compute_ttft_itl_windows(ts, schedule)
    assert restarted is True and scrape_gap is False
    assert windows[0]["groups"][0]["ttft"]["observations"] == 10


def mk_ttft(p50, p95, observations=1000):
    return {
        "ttft": {"state": "ok", "observations": observations, "p50_seconds": p50, "p95_seconds": p95},
        "itl": {"state": "no_observations", "observations": 0, "p50_seconds": None, "p95_seconds": None},
    }


def test_priority_verdict_not_applicable_when_primary_passed():
    pv = fairness_report.compute_priority_verdict(
        "PASS", ["app1", "app2"], {"app1": 20, "app2": 10},
        {"app1": mk_ttft(0.1, 0.2), "app2": mk_ttft(0.5, 0.6)},
    )
    assert pv["applicable"] is False
    assert pv["result"] == "N/A (share already PASS)"


def test_priority_verdict_not_evaluated_when_ttft_missing():
    ttft = {"app1": mk_ttft(0.1, 0.2), "app2": {"ttft": {"state": "not_recorded"}, "itl": {}}}
    pv = fairness_report.compute_priority_verdict("FAIL", ["app1", "app2"], {"app1": 20, "app2": 10}, ttft)
    assert pv["result"] == "not_evaluated"
    assert "app2" in pv["reason"]


def test_priority_verdict_ok_when_weights_distinct_and_order_correct():
    groups = ["app1", "app2", "end-users"]
    weights = {"app1": 20, "app2": 10, "end-users": 65}
    ttft = {
        "app1": mk_ttft(0.50, 0.60),
        "app2": mk_ttft(0.60, 0.70),
        "end-users": mk_ttft(0.10, 0.15),  # highest weight, lowest TTFT
    }
    pv = fairness_report.compute_priority_verdict("FAIL", groups, weights, ttft, noise_floor_seconds=0.05)
    assert pv["result"] == "PRIORITY-OK", pv
    assert pv["top_weighted_group"] == "end-users"
    assert pv["no_inversions_among_distinct_weights"] is True
    assert pv["rank_correlation"] == 1.0


def test_priority_verdict_fails_on_a_genuine_inversion():
    groups = ["app1", "app2", "end-users"]
    weights = {"app1": 20, "app2": 10, "end-users": 65}
    ttft = {
        "app1": mk_ttft(0.10, 0.15),  # lower weight than end-users, but faster: wrong order
        "app2": mk_ttft(0.20, 0.30),
        "end-users": mk_ttft(0.50, 0.60),
    }
    pv = fairness_report.compute_priority_verdict("FAIL", groups, weights, ttft, noise_floor_seconds=0.05)
    assert pv["result"] == "PRIORITY-FAIL"
    assert pv["no_inversions_among_distinct_weights"] is False


def test_priority_verdict_fails_on_insufficient_separation():
    groups = ["app1", "app2", "end-users"]
    weights = {"app1": 20, "app2": 10, "end-users": 65}
    ttft = {
        "app1": mk_ttft(0.50, 0.60),
        "app2": mk_ttft(0.52, 0.62),
        "end-users": mk_ttft(0.48, 0.58),  # correctly ordered, but barely
    }
    pv = fairness_report.compute_priority_verdict("FAIL", groups, weights, ttft, noise_floor_seconds=0.05)
    assert pv["no_inversions_among_distinct_weights"] is True
    assert pv["separation_state"] == "insufficient"
    assert pv["result"] == "PRIORITY-FAIL"


def test_priority_verdict_without_noise_floor_skips_separation_check():
    groups = ["app1", "end-users"]
    weights = {"app1": 20, "end-users": 65}
    ttft = {"app1": mk_ttft(0.50, 0.60), "end-users": mk_ttft(0.499, 0.599)}
    pv = fairness_report.compute_priority_verdict("FAIL", groups, weights, ttft, noise_floor_seconds=None)
    assert pv["separation_state"] == "not_evaluated"
    assert pv["result"] == "PRIORITY-OK"


def test_priority_verdict_handles_weight_tie_without_false_failure():
    # UNI-226 board direction (2026-11-10): 98/1/1 under equal load is a
    # named, scored prioritisation row. app2 and end-users are BOTH weight 1
    # -- a genuine tie this fixture reproduces. app1 (weight 98) is clearly,
    # strictly fastest; app2 and end-users differ from each other by pure
    # noise that the board does not ask to be ordered. This must read as
    # PRIORITY-OK, not get penalised by the app2-vs-end-users noise the way
    # a raw (uncorrected) rank-correlation-only gate would (confirmed as a
    # real bug during implementation: tie-aware Spearman alone gives 0.866,
    # not 1.0, for this exact fixture -- see compute_priority_verdict's own
    # comment for the derivation).
    groups = ["app1", "app2", "end-users"]
    weights = {"app1": 98, "app2": 1, "end-users": 1}
    ttft = {
        "app1": mk_ttft(0.10, 0.15),
        "app2": mk_ttft(0.50, 0.70),
        "end-users": mk_ttft(0.60, 0.80),
    }
    pv = fairness_report.compute_priority_verdict("FAIL", groups, weights, ttft, noise_floor_seconds=0.1)
    assert pv["rank_correlation"] is not None and pv["rank_correlation"] < 1.0, (
        "fixture should reproduce the raw-correlation-under-1.0 artifact from a weight tie"
    )
    assert pv["no_inversions_among_distinct_weights"] is True
    assert pv["top_group_strictly_lowest_p50"] is True
    assert pv["top_group_strictly_lowest_p95"] is True
    assert pv["result"] == "PRIORITY-OK", pv

    # Swapping app2/end-users' relative order against EACH OTHER (both still
    # tied on weight, so this must not change the verdict) confirms the gate
    # really does ignore their mutual ordering, only app1's.
    ttft_swapped = dict(ttft)
    ttft_swapped["app2"], ttft_swapped["end-users"] = ttft["end-users"], ttft["app2"]
    pv2 = fairness_report.compute_priority_verdict("FAIL", groups, weights, ttft_swapped, noise_floor_seconds=0.1)
    assert pv2["result"] == "PRIORITY-OK", pv2


def test_ttft_itl_integrates_into_report_and_markdown():
    with tempfile.TemporaryDirectory() as tmp:
        extra_before = ttft_bucket_lines("app1", [("0.1", 0), ("+Inf", 0)]) \
            + ttft_bucket_lines("app2", [("0.1", 0), ("+Inf", 0)]) \
            + ttft_bucket_lines("end-users", [("0.1", 0), ("+Inf", 0)])
        extra_after = ttft_bucket_lines("app1", [("0.1", 20), ("0.6", 500), ("+Inf", 500)]) \
            + ttft_bucket_lines("app2", [("0.1", 5), ("0.7", 480), ("+Inf", 480)]) \
            + ttft_bucket_lines("end-users", [("0.05", 500), ("+Inf", 510)])
        report = run_build_uni181(tmp, rows=CLEAN_ROWS, extra_before=extra_before, extra_after=extra_after)
        assert "ttft_itl" in report
        groups = report["ttft_itl"]["groups"]
        assert set(groups) == {"app1", "app2", "end-users"}
        assert groups["end-users"]["ttft"]["state"] == "ok"
        pv = report["ttft_itl"]["priority_verdict"]
        # CLEAN_ROWS' shares (500/480/510, weights 20/10/65 via CONFIGURED_WEIGHT)
        # are a share FAIL at these worker counts -- exercised here as "the
        # section renders end-to-end", not asserting a specific verdict value.
        assert pv["applicable"] in (True, False)
        md = fairness_report.render_markdown(report)
        assert "Per-tenant TTFT / ITL and the priority verdict (UNI-226)" in md
        assert "pool (all groups)" in md


# --- UNI-224: saturation-limb attribution -----------------------------------

def saturation_sample_block(queue_size, kv_util, pool_saturation):
    return (
        f'llm_d_epp_average_queue_size{{name="maas-vllm-gpu-inference-pool"}} {queue_size}\n'
        f'llm_d_epp_average_kv_cache_utilization{{name="maas-vllm-gpu-inference-pool"}} {kv_util}\n'
        f'llm_d_epp_flow_control_pool_saturation{{inference_pool="maas-vllm-gpu-inference-pool",'
        f'stage="effective"}} {pool_saturation}\n'
    )


def test_saturation_limb_none_without_timeseries():
    assert fairness_report.compute_saturation_limb(None, 32.0, 0.8) is None
    assert fairness_report.compute_saturation_limb("/no/such/file", 32.0, 0.8) is None


def test_saturation_limb_identifies_kv_cache_as_bound():
    with tempfile.TemporaryDirectory() as tmp:
        # Sample 0: queue-bound (16/32=0.5 vs 0.08/0.8=0.1). Sample 1: the
        # run's peak roofline score, and it is KV-bound (0.68/0.8=0.85 vs
        # 8/32=0.25) -- the case the saturation detector's own
        # `max(qRatio, kvRatio)` would gate dispatch on.
        ts = write_timeseries_raw(tmp, "ts.txt", [
            (0, saturation_sample_block(16, 0.08, 0.5)),
            (10, saturation_sample_block(8, 0.68, 0.85)),
        ])
        sat = fairness_report.compute_saturation_limb(ts, 32.0, 0.8)
        assert sat["state"] == "ok" and sat["sample_count"] == 2
        assert abs(sat["peak_queue_ratio"] - 0.5) < 1e-12
        assert abs(sat["peak_kv_ratio"] - 0.85) < 1e-12
        assert sat["bound_at_peak"] == "kv_cache"
        assert sat["kv_binding_sample_count"] == 1
        assert sat["samples"][0]["bound"] == "queue"
        assert sat["samples"][1]["bound"] == "kv_cache"


def test_saturation_limb_tie_favors_queue_and_skips_failed_scrapes():
    with tempfile.TemporaryDirectory() as tmp:
        lines = [
            "# ts=2026-11-01T00:00:00Z epoch=0",
            saturation_sample_block(0, 0, 0).rstrip("\n"),  # 0/0 tie
            "# ts=2026-11-01T00:00:05Z epoch=5",
            "# scrape_exit=7",  # connection-level failure -- must not count as a sample
            "# ts=2026-11-01T00:00:10Z epoch=10",
            saturation_sample_block(4, 0.4, 0.5).rstrip("\n"),  # kv-bound: 0.4/0.8=0.5 > 4/32=0.125
        ]
        ts = write(tmp, "ts.txt", "\n".join(lines) + "\n")
        sat = fairness_report.compute_saturation_limb(ts, 32.0, 0.8)
        assert sat["sample_count"] == 2  # the failed-scrape block is excluded
        assert sat["samples"][0]["bound"] == "queue"  # 0/0 tie favors queue
        assert sat["bound_at_peak"] == "kv_cache"


def test_saturation_limb_reflects_uni224_live_finding():
    # UNI-224's own measured numbers (2026-11-10, Prometheus, 411 samples):
    # kv_cache peaked at 0.0017 against an 0.8 threshold (ratio 0.00213),
    # queue peaked at 178 against a 32 threshold (ratio 5.5625) -- the queue
    # limb wins by ~1000x, reproduced here as a regression fixture so a
    # future change to the ratio math can't silently flip this conclusion.
    with tempfile.TemporaryDirectory() as tmp:
        ts = write_timeseries_raw(tmp, "ts.txt", [
            (0, saturation_sample_block(178, 0.0017, 5.5625)),
        ])
        sat = fairness_report.compute_saturation_limb(ts, 32.0, 0.8)
        assert sat["bound_at_peak"] == "queue"
        assert sat["peak_queue_ratio"] > 1000 * sat["peak_kv_ratio"]


def test_saturation_section_renders_markdown_and_handles_missing_timeseries():
    with tempfile.TemporaryDirectory() as tmp:
        report = run_build_uni181(tmp, rows=CLEAN_ROWS)
        assert report["saturation"] is None
        md = fairness_report.render_markdown(report)
        assert "## Saturation limb (UNI-224)" in md
        assert "Not evaluated" in md

        ts = write_timeseries_raw(tmp, "ts2.txt", [(0, saturation_sample_block(2, 0.001, 0.0625))])
        report2 = run_build_uni181(tmp, rows=CLEAN_ROWS, metrics_timeseries_path=ts)
        md2 = fairness_report.render_markdown(report2)
        assert "Bound at this run's peak roofline score: `queue`" in md2



# --- UNI-305: N-tenant logs ----------------------------------------------------

def test_open_loop_rates_line_reads_any_group_set():
    # 13-loadgen-poisson.py given a six-tenant manifest: the rates line names
    # whatever groups it was given, rate-0 groups included.
    with tempfile.TemporaryDirectory() as tmp:
        log = write(tmp, "loadgen.log", "\n".join([
            "load: open-loop Poisson arrivals rate app1=4.0/s app2=2.0/s app3=0.0/s app10=1.5/s duration=240.0s seed=1",
            "load: done.",
            "app1         sent=960    completion_tokens=72000    p50=0.75s p95=1.10s p99=1.50s codes=[200=960]",
            "app2         sent=480    completion_tokens=36000    p50=0.75s p95=1.10s p99=1.50s codes=[200=480]",
            "app3         sent=0",
            "app10        sent=360    completion_tokens=27000    p50=0.75s p95=1.10s p99=1.50s codes=[200=360]",
        ]) + "\n")
        offered, rows, duration, generator = fairness_report.parse_loadgen_log(log)
        assert generator == "open-loop", generator
        assert offered == {"app1": 4.0, "app2": 2.0, "app3": 0, "app10": 1.5}, offered
        assert list(offered) == ["app1", "app2", "app3", "app10"], "manifest order kept"
        assert sorted(rows) == ["app1", "app10", "app2"], rows
        assert rows["app10"]["total"] == 360


def test_closed_loop_workers_field_reads_any_group_set():
    # 12-loadgen-route.sh given a manifest without app1/app2/end-users at all.
    with tempfile.TemporaryDirectory() as tmp:
        log = write(tmp, "loadgen.log", "\n".join([
            "load: GW=x tenants=[app3 app4] workers app3=32 app4=8 app5=16 duration=240s",
            "load: done.",
            "TENANT       TOTAL   P50_SEC   P95_SEC   STATUSES",
            "app3         1000    0.80      1.00      200=1000",
            "app4         250     0.80      1.00      200=250",
        ]) + "\n")
        offered, rows, duration, generator = fairness_report.parse_loadgen_log(log)
        assert generator == "closed-loop"
        assert offered == {"app3": 32, "app4": 8, "app5": 0}, offered
        assert sorted(rows) == ["app3", "app4"], rows
        assert duration == 240


def test_three_tenant_log_parses_as_before():
    # The legacy closed-loop line, custom field included: same dict, same
    # order, custom skipped -- the baseline every scored run used.
    with tempfile.TemporaryDirectory() as tmp:
        log = write(tmp, "loadgen.log", loadgen_log("app1 end-users", 32, 32, 128, 240, CLEAN_ROWS, w_custom=4))
        offered, _, _, _ = fairness_report.parse_loadgen_log(log)
        assert list(offered.items()) == [("app1", 32), ("app2", 0), ("end-users", 128)], offered


def test_resolve_schedule_follows_offered_order_not_set_order():
    groups = ["app1", "app2"] + [f"app{n}" for n in range(3, 21)]
    orders = {tuple(fairness_report.resolve_schedule(None, groups, 240)) for _ in range(5)}
    assert orders == {tuple(groups)}, orders


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"ok   {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e}")
    print(f"{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
