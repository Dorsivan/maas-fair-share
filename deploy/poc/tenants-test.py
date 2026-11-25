#!/usr/bin/env python3
"""Tests for the UNI-305 tenant manifest and the harness scripts that read it.
No cluster: `oc` and `curl` are stubbed where a script needs them.

Run: python3 -I tenants-test.py
"""
import glob
import importlib.util
import os
import re
import stat
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("tenants", os.path.join(HERE, "tenants.py"))
tenants = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tenants)

DEFAULT = os.path.join(HERE, "tenants", "default.tenants")
SIX = os.path.join(HERE, "tenants", "six-unequal.tenants")


def run(*args, env=None, **kw):
    return subprocess.run(list(args), capture_output=True, text=True, env=env, **kw)


def raises(text, fragment):
    try:
        tenants.parse_manifest(text)
    except tenants.ManifestError as e:
        assert fragment in str(e), str(e)
        return
    raise AssertionError(f"no ManifestError for {text!r}")


def test_default_manifest_is_the_three_tenant_baseline():
    ts = tenants.load_manifest(DEFAULT)
    assert [(t["group"], t["weight"]) for t in ts] == [("app1", 20), ("app2", 10), ("end-users", 65)]
    assert ts[2]["match"] == ("prefix", ("end-user-",))
    assert ts[2]["keys"] == ("end-user-alpha", "end-user-beta")


def test_committed_epp_config_agrees_with_default_manifest():
    r = run(sys.executable, "-I", os.path.join(HERE, "tenants.py"), "check")
    assert r.returncode == 0, r.stderr


def test_every_manifest_renders_a_config_that_checks():
    src = open(tenants.DEFAULT_CONFIG).read()
    for path in glob.glob(os.path.join(HERE, "tenants", "*.tenants")):
        ts = tenants.load_manifest(path)
        out = tenants.render_config(src, ts)
        assert tenants.compare(ts, tenants.parse_config_groups(out)) == [], path
        # Only the groups list moves.
        strip = lambda t: re.sub(r"(?m)^\s*(- \{ name:|# UNI-305: rendered).*\n", "", t)
        assert strip(out) == strip(src), path


def test_check_reports_each_kind_of_drift():
    ts = tenants.load_manifest(SIX)
    cfg = tenants.parse_config_groups(open(tenants.DEFAULT_CONFIG).read())
    problems = "\n".join(tenants.compare(ts, cfg))
    assert "app1: weight manifest=40 config=20" in problems
    assert "app3: in the manifest, not in the EPP config" in problems
    assert "end-users: in the EPP config, not in the manifest" in problems


def test_config_groups_accept_estimated_output_tokens():
    # UNI-299: a group's estimatedOutputTokens must not make preflight fail.
    cfg = ("        groups:\n"
           "          - { name: app1, weight: 20, estimatedOutputTokens: 4000, match: { exact: [a] } }\n"
           "          - { name: app2, weight: 10, match: { prefix: [b-] } }\n")
    assert tenants.parse_config_groups(cfg) == [
        ("app1", 20.0, ("exact", ("a",))), ("app2", 10.0, ("prefix", ("b-",)))]


def test_manifest_rejects_keys_that_would_classify_elsewhere():
    raises("a 1 exact:a b - - -\n", "does not classify")
    raises("a 1 exact:a a - - -\na 1 exact:b b - - -\n", "listed twice")
    raises("p 1 prefix:end- end-x - - -\nq 1 exact:end-y end-y - - -\n", "claimed first by 'p'")
    raises("A 1 exact:a a - - -\n", "bad group name")
    raises("a 1 exact:a a - - wide\n", "shape")
    raises("a 1 exact:a a\n", "expected 7 columns")


def test_cache_profile_default_matches_default_manifest():
    yaml = open(os.path.join(HERE, "10-cache-profile.yaml")).read()
    m = re.search(r'PROFILE_TENANTS="\$\{PROFILE_TENANTS:-([^}]*)\}"', yaml)
    r = run(sys.executable, "-I", os.path.join(HERE, "tenants.py"), "cache-profile")
    assert r.returncode == 0, r.stderr
    assert m.group(1) == r.stdout.strip(), (m.group(1), r.stdout)


def test_n_group_renders_are_current():
    r = run(sys.executable, "-I", os.path.join(HERE, "epp-groups", "render.py"), "--verify")
    assert r.returncode == 0, r.stdout


def test_poisson_tenant_flags_equal_legacy_flags():
    with tempfile.TemporaryDirectory() as tmp:
        for k in ("a", "b", "c", "d"):
            open(os.path.join(tmp, k), "w").write(k)
        common = ["--gw", "http://127.0.0.1:9", "--duration", "0.001", "--drain-timeout", "1", "--seed", "1"]
        py = os.path.join(HERE, "13-loadgen-poisson.py")
        legacy = run(sys.executable, "-I", py, *common, "--out", os.path.join(tmp, "o1"),
                     "--rate-app1", "4", "--rate-end-users", "2",
                     "--key-app1", f"{tmp}/a", "--key-app2", f"{tmp}/b",
                     "--key-end-alpha", f"{tmp}/c", "--key-end-beta", f"{tmp}/d")
        new = run(sys.executable, "-I", py, *common, "--out", os.path.join(tmp, "o2"),
                  "--tenant", f"app1=4=/{tmp}/a", "--tenant", f"app2=0=/{tmp}/b",
                  "--tenant", f"end-users=2={tmp}/c,{tmp}/d")
        assert legacy.returncode == new.returncode == 0, (legacy.stderr, new.stderr)
        head = lambda out: out.splitlines()[0]
        assert head(legacy.stdout) == head(new.stdout), (legacy.stdout, new.stdout)
        assert head(new.stdout).startswith("load: open-loop Poisson arrivals rate app1=4.0/s app2=0.0/s end-users=2.0/s ")
        six = run(sys.executable, "-I", py, *common, "--out", os.path.join(tmp, "o3"),
                  *[a for g in ("app1", "app3", "app10") for a in ("--tenant", f"{g}=1={tmp}/a")])
        assert "rate app1=1.0/s app3=1.0/s app10=1.0/s duration=" in head(six.stdout), six.stdout


def stub_bin(tmp):
    """`oc get secret ... jsonpath={.data.<key>}` prints base64(<key>); curl
    records which key file's content each request carried."""
    b = os.path.join(tmp, "bin")
    os.makedirs(b)
    open(os.path.join(b, "oc"), "w").write(
        '#!/bin/bash\nfor a in "$@"; do case "$a" in jsonpath=*) k="${a#*.data.}"; k="${k%\\}}";'
        ' printf "%s" "$k" | base64 ;; esac; done\n')
    open(os.path.join(b, "curl"), "w").write(
        '#!/bin/bash\nfor a in "$@"; do case "$a" in "Authorization: Bearer "*) echo "${a#*Bearer }" >> "$CURL_LOG";; esac; done\n'
        'sleep 0.2; printf "200 0.01"\n')
    for f in ("oc", "curl"):
        os.chmod(os.path.join(b, f), 0o755)
    return b


def route(tmp, **env_extra):
    b = stub_bin(tmp) if not os.path.isdir(os.path.join(tmp, "bin")) else os.path.join(tmp, "bin")
    log = os.path.join(tmp, f"curl-{len(os.listdir(tmp))}.log")
    open(log, "w").close()
    env = dict(os.environ, PATH=b + ":" + os.environ["PATH"], OPENSHIFT_TOKEN="x", DURATION="1",
               WORKERS="4", OUT=os.path.join(tmp, f"out-{len(os.listdir(tmp))}"), CURL_LOG=log, **env_extra)
    r = run("bash", os.path.join(HERE, "12-loadgen-route.sh"), env=env)
    return r, open(log).read().split()


def test_route_loadgen_default_is_the_three_tenant_run():
    with tempfile.TemporaryDirectory() as tmp:
        r, sent = route(tmp)
        assert r.returncode == 0, r.stderr
        assert "tenants=[app1 app2 end-users] workers app1=4 app2=4 end-users=4 duration=1s" in r.stdout, r.stdout
        # end-users' four workers split evenly across alpha and beta.
        assert set(sent) == {"app1-production", "app2-batch", "end-user-alpha", "end-user-beta"}, set(sent)
        r2, _ = route(tmp, TENANTS="app1", WORKERS_END_USERS="9")
        assert "tenants=[app1] workers app1=4 app2=4 end-users=9 " in r2.stdout, r2.stdout


def test_route_loadgen_runs_a_six_tenant_manifest():
    with tempfile.TemporaryDirectory() as tmp:
        r, sent = route(tmp, TENANT_MANIFEST=SIX, WORKERS_APP6="1")
        assert r.returncode == 0, r.stderr
        assert "workers app1=32 app2=32 app3=32 app4=32 app5=32 app6=1 duration=1s" in r.stdout, r.stdout
        assert {"app3", "app6"} <= set(sent), set(sent)
        r2, _ = route(tmp, TENANT_MANIFEST=SIX, TENANTS="end-users")
        assert r2.returncode != 0 and "unknown tenant: end-users" in r2.stderr, r2.stderr


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
