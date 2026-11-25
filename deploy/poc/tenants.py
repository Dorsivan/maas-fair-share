#!/usr/bin/env python3
"""The POC harness's single tenant manifest (UNI-305).

The fairness plugin has no tenant names in it -- groups are a config list and N
is unbounded. Everything that used to pin the POC to app1/app2/end-users lived
in deploy/poc/, and every one of those places now reads a manifest instead:
deploy/poc/tenants/default.tenants unless TENANT_MANIFEST (bash) or
--tenants (python) names another.

Manifest format -- one tenant per line, whitespace-separated, '#' comments,
'-' means "not set here, use the script's own default":

    group      weight  match                  keys                          workers  rate  shape
    app1       20      exact:app1-production  app1-production               -        -     fixed
    end-users  65      prefix:end-user-       end-user-alpha,end-user-beta  -        -     long

  group    the fairness group name (EPP `groups[].name`, the fairness_id label,
           the loadgen group). Lowercase letters, digits, '-'.
  weight   relative weight, as in 00-config.yaml.
  match    exact:<sub>[,<sub>...] or prefix:<p>[,<p>...] -- the EPP match rule
           over MaaSSubscription names (x-maas-subscription).
  keys     comma list of /keys/<name> credential files the loadgen sends with,
           round-robined across the group's workers. Each must classify into
           this group under `match` -- checked here, because a key that
           classifies elsewhere is a silently wrong share.
  workers  closed-loop worker count (04-loadgen.yaml, 12-loadgen-route.sh).
  rate     open-loop Poisson req/s (13-loadgen-poisson.py).
  shape    cache shape for 10-cache-profile.yaml: fixed | unique | long.

Identity convention is UNI-187's (epp-groups/render.py, deploy/maas/
08-tenants.yaml): app1 -> app1-production, app2 -> app2-batch, app3+ use the
bare group name for subscription, key file and match value alike.

CLI (all read-only; nothing here touches the cluster):

    tenants.py check [MANIFEST] [--config FILE]   EPP groups == manifest, else exit 1
    tenants.py render-config MANIFEST [--src FILE] [--name CM]
    tenants.py names|weights|workers|rates|keys|loadgen-groups|cache-profile [MANIFEST]

`check` against 00-config.yaml (the default) is what keeps the committed EPP
config and the default manifest from drifting; 15-fairness-benchmark.sh runs
the same comparison against the LIVE maas-epp-config before a manifest run.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MANIFEST = os.path.join(HERE, "tenants", "default.tenants")
DEFAULT_CONFIG = os.path.join(HERE, "00-config.yaml")

COLUMNS = ("group", "weight", "match", "keys", "workers", "rate", "shape")
SHAPES = ("fixed", "unique", "long")
GROUP_NAME = re.compile(r"^[a-z0-9-]+$")


class ManifestError(Exception):
    pass


def _num(text, what, where, cast=float):
    try:
        v = cast(text)
    except ValueError:
        raise ManifestError(f"{where}: {what} {text!r} is not a number")
    if v < 0:
        raise ManifestError(f"{where}: {what} {text!r} is negative")
    return v


def classifies(match, subscription):
    kind, values = match
    if kind == "exact":
        return subscription in values
    return any(subscription.startswith(p) for p in values)


def parse_manifest(text, source="<manifest>"):
    """Returns an ordered list of tenant dicts. Order is the file's order and
    is kept everywhere downstream (report rows, loadgen fork order)."""
    tenants = []
    seen = set()
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        where = f"{source}:{n}"
        cols = line.split()
        if len(cols) != len(COLUMNS):
            raise ManifestError(f"{where}: expected {len(COLUMNS)} columns "
                                f"({' '.join(COLUMNS)}), got {len(cols)}")
        group, weight, match, keys, workers, rate, shape = cols
        if not GROUP_NAME.match(group):
            raise ManifestError(f"{where}: bad group name {group!r} (lowercase letters, digits, '-')")
        if group in seen:
            raise ManifestError(f"{where}: group {group!r} listed twice")
        seen.add(group)
        kind, _, vals = match.partition(":")
        if kind not in ("exact", "prefix") or not vals:
            raise ManifestError(f"{where}: match must be exact:<a,b> or prefix:<p>, got {match!r}")
        t = {
            "group": group,
            "weight": _num(weight, "weight", where),
            "match": (kind, tuple(vals.split(","))),
            "keys": tuple(keys.split(",")),
            "workers": None if workers == "-" else _num(workers, "workers", where, int),
            "rate": None if rate == "-" else _num(rate, "rate", where),
            "shape": None if shape == "-" else shape,
        }
        if t["shape"] is not None and t["shape"] not in SHAPES:
            raise ManifestError(f"{where}: shape must be one of {'/'.join(SHAPES)} or '-', got {shape!r}")
        for k in t["keys"]:
            if not classifies(t["match"], k):
                raise ManifestError(f"{where}: key {k!r} does not classify into {group!r} under {match}")
        tenants.append(t)
    if not tenants:
        raise ManifestError(f"{source}: no tenants")
    # A key that also matches an EARLIER group's rule lands there, not here --
    # the plugin takes the first matching group.
    for i, t in enumerate(tenants):
        for k in t["keys"]:
            for earlier in tenants[:i]:
                if classifies(earlier["match"], k):
                    raise ManifestError(f"{source}: key {k!r} of {t['group']!r} is claimed first "
                                        f"by {earlier['group']!r}'s match rule")
    return tenants


def load_manifest(path=None):
    path = path or os.environ.get("TENANT_MANIFEST") or DEFAULT_MANIFEST
    with open(path) as f:
        return parse_manifest(f.read(), path)


def token(group):
    """Same env-token rule as 04-loadgen.yaml's group_token: upper-case,
    non-alphanumerics -> '_' (end-users -> END_USERS)."""
    return re.sub(r"[^A-Z0-9]", "_", group.upper())


def fmt_num(v):
    return str(int(v)) if float(v).is_integer() else str(v)


# --- EPP config side ---------------------------------------------------------

GROUPS_BLOCK = re.compile(r"^([ \t]*)groups:[ \t]*\n((?:\1[ \t]+(?:#.*|- \{.*\})[ \t]*\n)+)", re.MULTILINE)
GROUP_ITEM = re.compile(
    r"-\s*\{\s*name:\s*(?P<name>[^,\s]+)\s*,\s*weight:\s*(?P<weight>[\d.]+)\s*,\s*"
    # UNI-299: a group may carry its own output estimate. The manifest has no
    # column for it, so it is accepted here and not compared.
    r"(?:estimatedOutputTokens:\s*[\d.]+\s*,\s*)?"
    r"match:\s*\{\s*(?P<kind>exact|prefix):\s*\[(?P<vals>[^\]]*)\]\s*\}\s*\}")


def parse_config_groups(text):
    """[(name, weight, (kind, values))] from an EndpointPickerConfig's
    flow-style `groups:` list -- the only style any file or patch helper in
    this repo writes."""
    m = GROUPS_BLOCK.search(text)
    if not m:
        raise ManifestError("no flow-style `groups:` list found in the EPP config")
    out = []
    for line in m.group(2).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        g = GROUP_ITEM.match(line)
        if not g:
            raise ManifestError(f"unparseable groups entry: {line}")
        vals = tuple(v.strip() for v in g.group("vals").split(",") if v.strip())
        out.append((g.group("name"), float(g.group("weight")), (g.group("kind"), vals)))
    return out


def compare(tenants, config_groups):
    """Every difference between a manifest and an EPP groups list, as
    human-readable lines. Empty means they agree."""
    problems = []
    cfg = {name: (w, match) for name, w, match in config_groups}
    for t in tenants:
        if t["group"] not in cfg:
            problems.append(f"{t['group']}: in the manifest, not in the EPP config "
                            f"(its traffic would fall to defaultGroup)")
            continue
        w, match = cfg[t["group"]]
        if abs(w - t["weight"]) > 1e-9:
            problems.append(f"{t['group']}: weight manifest={fmt_num(t['weight'])} config={fmt_num(w)}")
        if match != t["match"]:
            problems.append(f"{t['group']}: match manifest={t['match'][0]}:{','.join(t['match'][1])} "
                            f"config={match[0]}:{','.join(match[1])}")
    names = {t["group"] for t in tenants}
    for name, _, _ in config_groups:
        if name not in names:
            problems.append(f"{name}: in the EPP config, not in the manifest")
    if not problems and [t["group"] for t in tenants] != [n for n, _, _ in config_groups]:
        # Order matters for first-match classification when rules overlap.
        problems.append("group order differs: manifest=" + ",".join(t["group"] for t in tenants)
                        + " config=" + ",".join(n for n, _, _ in config_groups))
    return problems


def render_config(src_text, tenants, cm_name=None, banner=None):
    """src_text with ONLY its `groups:` list replaced by the manifest's, the
    same splice epp-groups/render.py does."""
    m = GROUPS_BLOCK.search(src_text)
    if not m:
        raise ManifestError("no flow-style `groups:` list found in the source")
    item_indent = m.group(1) + "  "
    width = max(len(t["group"]) for t in tenants) + 1
    lines = [f"{item_indent}# {banner}\n"] if banner else []
    for t in tenants:
        kind, vals = t["match"]
        lines.append(f"{item_indent}- {{ name: {(t['group'] + ',').ljust(width)} "
                     f"weight: {fmt_num(t['weight'])}, match: {{ {kind}: [{', '.join(vals)}] }} }}\n")
    out = src_text[:m.start(2)] + "".join(lines) + src_text[m.end(2):]
    if cm_name:
        out, n = re.subn(r"^(metadata:\n  name: )maas-epp-config$", r"\g<1>" + cm_name,
                         out, count=1, flags=re.MULTILINE)
        if n != 1:
            raise ManifestError("could not find `metadata.name: maas-epp-config` in the source")
    return out


# --- CLI ---------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("manifest", nargs="?")
    c.add_argument("--config", default=DEFAULT_CONFIG,
                   help="file holding the EndpointPickerConfig (00-config.yaml, or the live "
                        "ConfigMap's .data.epp); '-' reads stdin")
    r = sub.add_parser("render-config")
    r.add_argument("manifest")
    r.add_argument("--src", default=DEFAULT_CONFIG)
    r.add_argument("--name", default=None)
    for name in ("names", "weights", "workers", "rates", "keys", "loadgen-groups", "cache-profile"):
        sub.add_parser(name).add_argument("manifest", nargs="?")
    a = ap.parse_args(argv)

    try:
        tenants = load_manifest(a.manifest)
        if a.cmd == "check":
            text = sys.stdin.read() if a.config == "-" else open(a.config).read()
            problems = compare(tenants, parse_config_groups(text))
            for p in problems:
                print(f"MISMATCH {p}", file=sys.stderr)
            if problems:
                return 1
            print(f"ok: {len(tenants)} tenants agree with {a.config}")
        elif a.cmd == "render-config":
            src = open(a.src).read()
            sys.stdout.write(render_config(
                src, tenants, a.name,
                f"UNI-305: rendered from {os.path.relpath(a.manifest, os.path.join(HERE, '..', '..'))} "
                "by deploy/poc/tenants.py -- do not hand-edit."))
        elif a.cmd == "names":
            print(" ".join(t["group"] for t in tenants))
        elif a.cmd == "weights":
            print(",".join(f"{t['group']}={fmt_num(t['weight'])}" for t in tenants))
        elif a.cmd == "workers":
            unset = [t["group"] for t in tenants if t["workers"] is None]
            if unset:
                raise ManifestError(f"workers not set in the manifest for: {' '.join(unset)}")
            print(",".join(f"{t['group']}={t['workers']}" for t in tenants))
        elif a.cmd == "rates":
            # One "group rate" line per tenant; an unset rate is 0 (not offered).
            for t in tenants:
                print(t["group"], fmt_num(t["rate"]) if t["rate"] is not None else 0)
        elif a.cmd == "keys":
            seen = []
            for t in tenants:
                seen += [k for k in t["keys"] if k not in seen]
            print(" ".join(seen))
        elif a.cmd == "loadgen-groups":
            # 04-loadgen.yaml's LOADGEN_GROUPS: name:workers:keys, an empty
            # workers field falls back to WORKERS / WORKERS_<TOKEN>.
            print(" ".join(f"{t['group']}:{'' if t['workers'] is None else t['workers']}:{','.join(t['keys'])}"
                           for t in tenants))
        elif a.cmd == "cache-profile":
            unset = [t["group"] for t in tenants if t["shape"] is None]
            if unset:
                raise ManifestError(f"shape not set in the manifest for: {' '.join(unset)}")
            print(" ".join(f"{','.join(t['keys'])}:{t['group']}:{t['shape']}" for t in tenants))
    except (ManifestError, OSError) as e:
        print(f"tenants.py: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
