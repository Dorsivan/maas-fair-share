#!/usr/bin/env python3
"""Tests for 15-fairness-report.py against synthetic metrics snapshots and a
synthetic loadgen.log -- no cluster, no GPU session. This is what UNI-54's
"done when" bar means by "a test shows the FAIL path actually fails": feed a
deliberately skewed input and confirm the verdict is FAIL with a non-zero
process exit, not just that the happy path parses.

Run: python3 -I 15-fairness-report-test.py
"""
import importlib.util
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


def loadgen_log(tenants, w_app1, w_app2, w_end, duration, rows):
    lines = [f"load: tenants=[{tenants}] workers app1={w_app1} app2={w_app2} end-users={w_end} duration={duration}s"]
    lines.append("load: done.")
    lines.append(f"{'TENANT':<12} {'TOTAL':<7} {'P50_SEC':<9} {'P95_SEC':<9} STATUSES")
    for group, total, p50, p95, statuses in rows:
        lines.append(f"{group:<12} {total:<7} {p50:<9} {p95:<9} {statuses}")
    lines.append("A run is only meaningful if the statuses are overwhelmingly 200.")
    return "\n".join(lines) + "\n"


def run_build(tmp, *, tokens_before, tokens_after, tenants, w_app1, w_app2, w_end,
              rows, threshold_points=10.0, duration=240, scenario="test-scenario",
              control=False):
    before = write(tmp, "before.txt", CONFIGURED_WEIGHT + ENFORCING_ON + tokens_before)
    after = write(tmp, "after.txt", CONFIGURED_WEIGHT + ENFORCING_ON + tokens_after)
    log = write(tmp, "loadgen.log", loadgen_log(tenants, w_app1, w_app2, w_end, duration, rows))
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
