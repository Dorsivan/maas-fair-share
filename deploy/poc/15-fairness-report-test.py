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


def loadgen_log(tenants, w_app1, w_app2, w_end, duration, rows, w_custom=None):
    custom_field = f"custom={w_custom} " if w_custom is not None else ""
    lines = [f"load: tenants=[{tenants}] workers app1={w_app1} app2={w_app2} end-users={w_end} {custom_field}duration={duration}s"]
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


def test_compute_windows_matches_whole_run_math_over_one_window():
    # A single window spanning the whole run must reproduce the same
    # expected/observed share the whole-run (before/after) calculation would,
    # since it's the same two snapshots and the same definitions.
    schedule = fairness_report.resolve_schedule(None, {"app1", "app2", "end-users"}, 240)
    weights = {"app1": 20.0, "app2": 10.0, "end-users": 65.0}
    timeseries = [
        (0, "t0", {"llm_d_epp_maas_fairness_contended_service_tokens_total":
                   {"app1": 1000.0, "app2": 1000.0, "end-users": 1000.0}}),
        (240, "t1", {"llm_d_epp_maas_fairness_contended_service_tokens_total":
                     {"app1": 3100.0, "app2": 2000.0, "end-users": 7900.0}}),
    ]
    windows, epp_restarted = fairness_report.compute_windows(timeseries, schedule, weights)
    assert epp_restarted is False
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
        (0, "t0", {tok: {"app1": 0.0, "app2": 0.0, "end-users": 0.0}}),
        (10, "t1", {tok: {"app1": 100.0, "app2": 100.0, "end-users": 0.0}}),
        (20, "t2", {tok: {"app1": 150.0, "app2": 150.0, "end-users": 300.0}}),
    ]
    windows, _ = fairness_report.compute_windows(timeseries, schedule, weights)
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
        (0, "t0", {tok: {"app1": 9000.0, "app2": 1000.0}}),
        (10, "t1", {tok: {"app1": 50.0, "app2": 1200.0}}),  # app1 went backwards
    ]
    windows, epp_restarted = fairness_report.compute_windows(timeseries, schedule, weights)
    assert epp_restarted is True
    by_group = {g["group"]: g for g in windows[0]["groups"]}
    assert by_group["app1"]["delivered_tokens"] == 0.0  # clamped, not negative


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
