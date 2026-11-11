#!/usr/bin/env python3
"""Offline tests for deploy/poc/lanes.py (UNI-231). No cluster needed.

    python3 -I deploy/poc/lanes-test.py
"""
import glob
import os
import re
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.join(HERE, "lanes.py")
MANIFESTS = sorted(glob.glob(os.path.join(HERE, "*.yaml")) +
                   glob.glob(os.path.join(HERE, "epp-groups", "*.yaml")))


def run(namespace, *args, stdin=None):
    env = dict(os.environ, NAMESPACE=namespace)
    return subprocess.run([sys.executable, "-I", LANES, *args], input=stdin,
                          capture_output=True, text=True, env=env)


def read(path):
    with open(path) as fh:
        return fh.read()


def code_lines(text):
    return [l for l in text.splitlines() if not l.lstrip().startswith("#")]


class Render(unittest.TestCase):
    def test_lane1_is_identity_for_every_manifest(self):
        for path in MANIFESTS:
            src = read(path)
            r = run("maas-fairness-poc", "render", stdin=src)
            self.assertEqual(r.returncode, 0, (path, r.stderr))
            self.assertEqual(r.stdout, src, path)

    def test_lane2_leaves_no_reference_to_lane1(self):
        for path in MANIFESTS:
            r = run("poc-maas-lane2", "render", path)
            self.assertEqual(r.returncode, 0, (path, r.stderr))
            leaks = [l for l in code_lines(r.stdout) if "maas-fairness-poc" in l]
            self.assertEqual(leaks, [], path)

    def test_lane3_suffixes_every_exact_match_and_no_prefix(self):
        r = run("poc-maas-lane3", "render", os.path.join(HERE, "00-config.yaml"))
        exact = re.findall(r"exact:\s*\[([^\]]*)\]", "\n".join(code_lines(r.stdout)))
        self.assertEqual(exact, ["app1-production-l3", "app2-batch-l3"])
        # end-user-alpha-l3 must still match the unchanged prefix rule
        self.assertIn("prefix: [end-user-] ", r.stdout)

    def test_lane2_pins_model_servers_to_its_own_pair(self):
        r = run("poc-maas-lane2", "render", os.path.join(HERE, "09-vllm-gpu.yaml"))
        self.assertIn("values: [ocp-gpu-worker-2, ocp-gpu-worker-3]", r.stdout)
        self.assertNotIn("ocp-gpu-worker-0", r.stdout)

    def test_unpinned_model_server_is_refused(self):
        src = read(os.path.join(HERE, "09-vllm-gpu.yaml"))
        src = src.replace("values: [ocp-gpu-worker-0, ocp-gpu-worker-1]", "values: []")
        r = run("poc-maas-lane2", "render", stdin=src)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("unpinned", r.stderr)

    def test_each_lane_pins_its_loadgen_to_its_own_node(self):
        src = os.path.join(HERE, "04-loadgen.yaml")
        seen = set()
        for ns, node in (("maas-fairness-poc", "ocp-worker-3"),
                         ("poc-maas-lane2", "ocp-worker-0"),
                         ("poc-maas-lane3", "ocp-worker-1")):
            r = run(ns, "render", src)
            self.assertEqual(r.returncode, 0, r.stderr)
            pins = re.findall(r"values: \[(ocp-worker-\d)\]", r.stdout)
            self.assertEqual(pins, [node], ns)
            seen.add(node)
        self.assertEqual(len(seen), 3)
        self.assertNotIn("ocp-worker-2", seen)

    def test_loadgen_anti_affinity_spans_namespaces(self):
        r = run("poc-maas-lane2", "render", os.path.join(HERE, "04-loadgen.yaml"))
        anti = r.stdout[r.stdout.index("podAntiAffinity:"):]
        anti = anti[:anti.index("containers:")]
        self.assertIn("job-name: maas-loadgen", anti)
        self.assertIn("namespaceSelector: {}", anti)
        self.assertIn("topologyKey: kubernetes.io/hostname", anti)

    def test_unpinned_loadgen_is_refused(self):
        src = read(os.path.join(HERE, "04-loadgen.yaml"))
        src = src.replace("values: [ocp-worker-3]", "values: []")
        r = run("poc-maas-lane3", "render", stdin=src)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("maas-loadgen has no hostname pin", r.stderr)

    def test_unknown_namespace_never_falls_back_to_lane1(self):
        for cmd in (["env"], ["render"], ["tenants"]):
            r = run("maas-fairness-poc-typo", *cmd, stdin="kind: X\n")
            self.assertNotEqual(r.returncode, 0, cmd)
            self.assertEqual(r.stdout, "", cmd)

    def test_kind_filter(self):
        r = run("poc-maas-lane2", "render", "--kind", "Gateway",
                os.path.join(HERE, "03-gateway.yaml"))
        self.assertEqual(re.findall(r"^kind: (\S+)", r.stdout, re.M), ["Gateway"])
        self.assertIn("namespace: poc-maas-lane2", r.stdout)


class Tenants(unittest.TestCase):
    def test_lane2_tenants(self):
        r = run("poc-maas-lane2", "tenants")
        self.assertEqual(r.returncode, 0, r.stderr)
        code = "\n".join(code_lines(r.stdout))
        kinds = re.findall(r"^kind: (\S+)", code, re.M)
        self.assertEqual(kinds.count("MaaSAuthPolicy"), 1)
        self.assertEqual(kinds.count("MaaSSubscription"), 22)
        self.assertNotIn("Group\n", kinds)  # cluster-scoped, shared, untouched
        names = re.findall(r"^(?:metadata:\s*\{name:|  name:)\s*([\w.-]+)", code, re.M)
        self.assertEqual(len(names), 23)
        self.assertTrue(all(n.endswith("-l2") for n in names), names)
        self.assertIn("app1-production-l2", names)
        self.assertIn("maas-poc-access-l2", names)
        self.assertNotIn("maas-vllm-cpu", code)
        refs = re.findall(r"- name: maas-vllm-gpu\n\s+namespace: (\S+)", code)
        self.assertEqual(set(refs), {"poc-maas-lane2"})
        self.assertEqual(len(refs), 23)

    def test_lane1_tenants_refused(self):
        r = run("maas-fairness-poc", "tenants")
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "")


class UNI102(unittest.TestCase):
    def test_scheduler_has_one_template_carrying_affinity_and_image(self):
        src = read(os.path.join(HERE, "09-vllm-gpu.yaml"))
        sched = src[src.index("    scheduler:"):]
        self.assertEqual(len(re.findall(r"^      template:", sched, re.M)), 1)
        tmpl = sched[sched.index("      template:"):]
        self.assertLess(tmpl.index("affinity:"), tmpl.index("image:"))


if __name__ == "__main__":
    unittest.main()
