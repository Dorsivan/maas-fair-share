#!/usr/bin/env python3
"""Three isolated POC lanes on one cluster, selected by NAMESPACE (UNI-231).

Every lane is the same stack under the same object names, in its own
namespace, on its own pair of GPU nodes:

    lane  namespace           GPU nodes                            suffix  loadgen node
    1     maas-fairness-poc   ocp-gpu-worker-0, ocp-gpu-worker-1   (none)  ocp-worker-3
    2     poc-maas-lane2      ocp-gpu-worker-2, ocp-gpu-worker-3   -l2     ocp-worker-0
    3     poc-maas-lane3      ocp-gpu-worker-4, ocp-gpu-worker-5   -l3     ocp-worker-1

Each lane's load generator gets its own CPU node too (UNI-249), none of them
ocp-worker-2, which carries every gateway, Authorino and maas-api.

The one thing that cannot be identical is the MaaS tenant identity. A
MaaSSubscription's name IS the identity the EPP groups on (MaaS injects it as
X-MaaS-Subscription), and every subscription lives in the one shared
`models-as-a-service` namespace -- there can only be one `app1-production`.
The board chose per-lane subscription names (UNI-231, option B), so lane 2's
app1 tenant is `app1-production-l2`. It is a SUFFIX on purpose: the end-users
group matches `prefix: [end-user-]`, which `end-user-alpha-l2` still does.

Everything else stays canonical. The loadgen reads keys from
secret/maas-loadgen-keys in $NAMESPACE by canonical tenant name, and
deploy/maas/mint-loadgen-keys.sh stores a lane's `-l2` key under that
canonical name -- so no loadgen or report code knows which lane it is on.
Only the EPP's group match values carry the suffix, and this script adds it.

    lanes.py env                         shell assignments for $NAMESPACE
    lanes.py render [--kind K] [FILE..]  manifests rewritten for $NAMESPACE
    lanes.py tenants                     this lane's MaaSSubscriptions and
                                         MaaSAuthPolicy, from 08-tenants.yaml

`render` on lane 1 is the identity transform (it is how the files are
written), so piping a manifest through it is always safe. An unknown
NAMESPACE is an error, never a silent fall-back to lane 1 -- a run that
believes it is on lane 2 while configuring lane 1 would corrupt someone
else's measurement.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TENANTS_SRC = os.path.join(HERE, "..", "maas", "08-tenants.yaml")

CANONICAL_NAMESPACE = "maas-fairness-poc"

LANES = {
    "maas-fairness-poc": {"lane": 1, "suffix": "",
                          "nodes": ["ocp-gpu-worker-0", "ocp-gpu-worker-1"],
                          "loadgen_node": "ocp-worker-3"},
    "poc-maas-lane2": {"lane": 2, "suffix": "-l2",
                       "nodes": ["ocp-gpu-worker-2", "ocp-gpu-worker-3"],
                       "loadgen_node": "ocp-worker-0"},
    "poc-maas-lane3": {"lane": 3, "suffix": "-l3",
                       "nodes": ["ocp-gpu-worker-4", "ocp-gpu-worker-5"],
                       "loadgen_node": "ocp-worker-1"},
}

# 09-vllm-gpu.yaml pins the model servers with exactly this line; render
# swaps the node list. Kept literal so `oc apply -f 09-vllm-gpu.yaml` alone
# is still a correct lane-1 manifest.
CANONICAL_NODES = "values: [ocp-gpu-worker-0, ocp-gpu-worker-1]"

# 04-loadgen.yaml pins the maas-loadgen Job with exactly this line (UNI-249).
CANONICAL_LOADGEN_NODE = "values: [ocp-worker-3]"

# A lane has no CPU model; subscriptions keep only their GPU modelRef.
LANE_MODEL = "maas-vllm-gpu"


def lane_for(namespace):
    if namespace not in LANES:
        sys.exit(f"lanes.py: NAMESPACE={namespace!r} is not a known lane "
                 f"({', '.join(LANES)})")
    return LANES[namespace]


def split_docs(text):
    """Split on `---` document separators, keeping each doc's own text."""
    docs, cur = [], []
    for line in text.splitlines(keepends=True):
        if line.rstrip("\n") == "---":
            docs.append("".join(cur))
            cur = []
        else:
            cur.append(line)
    docs.append("".join(cur))
    return docs


def doc_kind(doc):
    m = re.search(r"^kind:\s*(\S+)", doc, re.M)
    return m.group(1) if m else None


def is_comment(line):
    return line.lstrip().startswith("#")


def suffix_exact(line, suffix):
    def repl(m):
        items = [s.strip() for s in m.group(2).split(",") if s.strip()]
        return m.group(1) + ", ".join(i + suffix for i in items) + m.group(3)
    return re.sub(r"(exact:\s*\[)([^\]]*)(\])", repl, line)


def render_doc(doc, namespace, lane):
    out = []
    for line in doc.splitlines(keepends=True):
        if not is_comment(line):
            line = line.replace(CANONICAL_NAMESPACE, namespace)
            if lane["suffix"]:
                line = suffix_exact(line, lane["suffix"])
        out.append(line)
    doc = "".join(out)
    if doc_kind(doc) == "LLMInferenceService" and \
            re.search(r"^  name:\s*maas-vllm-gpu\s*$", doc, re.M):
        if CANONICAL_NODES not in doc:
            sys.exit("lanes.py: maas-vllm-gpu has no hostname pin "
                     f"({CANONICAL_NODES!r}) to rewrite -- refusing to render "
                     "an unpinned model server onto a shared cluster")
        doc = doc.replace(CANONICAL_NODES,
                          f"values: [{', '.join(lane['nodes'])}]")
    if doc_kind(doc) == "Job" and \
            re.search(r"^  name:\s*maas-loadgen\s*$", doc, re.M):
        if CANONICAL_LOADGEN_NODE not in doc:
            sys.exit("lanes.py: maas-loadgen has no hostname pin "
                     f"({CANONICAL_LOADGEN_NODE!r}) to rewrite -- refusing to "
                     "render a loadgen the scheduler could put on a shared "
                     "node")
        doc = doc.replace(CANONICAL_LOADGEN_NODE,
                          f"values: [{lane['loadgen_node']}]")
    return doc


def render(text, namespace, kind=None):
    lane = lane_for(namespace)
    docs = [render_doc(d, namespace, lane) for d in split_docs(text)]
    if kind:
        docs = [d for d in docs if doc_kind(d) == kind]
        if not docs:
            sys.exit(f"lanes.py: no {kind} document in the input")
        docs = [""] + docs  # leading separator keeps every doc self-delimited
    return "---\n".join(docs)


def drop_model_refs(doc, keep):
    """Drop every modelRefs list item whose `- name:` is not `keep`."""
    out, skipping, item_indent = [], False, None
    for line in doc.splitlines(keepends=True):
        m = re.match(r"^(\s*)- name:\s*(\S+)", line)
        if m and item_indent is not None and len(m.group(1)) == item_indent:
            skipping = m.group(2) != keep
        elif m and re.match(r"^\s*modelRefs:", out[-1] if out else ""):
            item_indent = len(m.group(1))
            skipping = m.group(2) != keep
        elif item_indent is not None and line.strip() and \
                len(line) - len(line.lstrip()) <= item_indent and \
                not line.lstrip().startswith("- "):
            item_indent, skipping = None, False
        if not skipping:
            out.append(line)
    return "".join(out)


def tenants(namespace, src=TENANTS_SRC):
    lane = lane_for(namespace)
    if not lane["suffix"]:
        sys.exit("lanes.py tenants: lane 1's subscriptions already exist and "
                 "instance 1's live policies are compiled from them -- this "
                 "command only creates NEW lanes' tenants")
    keep = []
    for doc in split_docs(open(src).read()):
        kind = doc_kind(doc)
        if kind not in ("MaaSSubscription", "MaaSAuthPolicy"):
            continue  # Groups are cluster-scoped and shared by every lane
        doc = drop_model_refs(doc, LANE_MODEL)
        if not re.search(rf"name:\s*{LANE_MODEL}\b", doc):
            continue  # e.g. a CPU-only subscription: nothing to serve here
        doc = re.sub(r"^(metadata:\s*\{name:\s*)([\w.-]+)",
                     lambda m: m.group(1) + m.group(2) + lane["suffix"],
                     doc, count=1, flags=re.M)
        doc = re.sub(r"^(  name:\s*)([\w.-]+)",
                     lambda m: m.group(1) + m.group(2) + lane["suffix"],
                     doc, count=1, flags=re.M)
        doc = "".join(l if is_comment(l) else
                      l.replace(CANONICAL_NAMESPACE, namespace)
                      for l in doc.splitlines(keepends=True))
        keep.append(doc)
    return "---\n" + "---\n".join(keep)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("env")
    r = sub.add_parser("render")
    r.add_argument("--kind")
    r.add_argument("files", nargs="*")
    sub.add_parser("tenants")
    a = ap.parse_args()
    namespace = os.environ.get("NAMESPACE", CANONICAL_NAMESPACE)

    if a.cmd == "env":
        lane = lane_for(namespace)
        print(f"LANE={lane['lane']}")
        print(f"LANE_SUFFIX={lane['suffix']}")
        print(f"LANE_GPU_NODES=\"{' '.join(lane['nodes'])}\"")
        print(f"LANE_LOADGEN_NODE={lane['loadgen_node']}")
    elif a.cmd == "render":
        text = "\n---\n".join(open(f).read() for f in a.files) if a.files \
            else sys.stdin.read()
        sys.stdout.write(render(text, namespace, a.kind))
    else:
        sys.stdout.write(tenants(namespace))


if __name__ == "__main__":
    main()
