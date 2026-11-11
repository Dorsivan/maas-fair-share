#!/bin/bash
# UNI-187: mint one sk-oai- key per named subscription straight into
# secret/maas-loadgen-keys, using the direct-ClusterIP form of docs/runbook.md
# "Mint a MaaS API key".
#
#   PATH=/paperclip/bin:$PATH deploy/maas/mint-loadgen-keys.sh app3 app4 ... app20
#
# The key file is named after the subscription (the loadgen's rule for any
# group it has no built-in for). Names already present in the secret are
# skipped, so a re-run only mints what is missing.
#
# THE MINT RESPONSE CONTAINS THE RAW KEY. It goes to a 0600 file in a 0700
# temp dir, the secret patch is built from files in that dir, and the dir is
# removed on exit. Only id/name/subscription/expiresAt are ever printed.
# If a value is ever exposed anyway, revoke it: DELETE /v1/api-keys/<id> with
# the same X-MaaS-Username / X-MaaS-Group headers used here.
#
# UNI-231 lanes: always pass the CANONICAL names (app1-production, app3, ...).
# On lane 2 (NAMESPACE=poc-maas-lane2) the key is minted against the lane's own
# subscription, app1-production-l2, but stored under the canonical name, so the
# loadgen finds it exactly where it does on lane 1. See deploy/poc/lanes.py.
set -euo pipefail

[ "$#" -ge 1 ] || { echo "usage: $0 <subscription>..." >&2; exit 2; }
NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
SECRET="maas-loadgen-keys"
MAAS_USER="${MAAS_USER:-dorsi}"
# Must be an owner group of every subscription minted in one call; app3..app20
# are owned by maas-poc-users (08-tenants.yaml).
MAAS_GROUP="${MAAS_GROUP:-maas-poc-users}"
EXPIRES_IN="${EXPIRES_IN:-30d}"
# a bare eval "$(...)" would swallow an unknown-lane error under set -e
LANE_ENV="$(NAMESPACE="$NAMESPACE" python3 -I "$(dirname "$0")/../poc/lanes.py" env)"
eval "$LANE_ENV"
OC="oc --token=${OPENSHIFT_TOKEN:?} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"

umask 077
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "identity: $($OC whoami)"
MAAS_API="https://$($OC get svc maas-api -n redhat-ods-applications -o jsonpath='{.spec.clusterIP}'):8443"
# A new lane starts with no secret; create it empty so the skip-list read and
# the final merge patch below work the same as on lane 1.
$OC get secret "$SECRET" -n "$NAMESPACE" >/dev/null 2>&1 \
  || $OC create secret generic "$SECRET" -n "$NAMESPACE" >/dev/null
$OC get secret "$SECRET" -n "$NAMESPACE" \
  -o go-template='{{range $k, $v := .data}}{{$k}}{{"\n"}}{{end}}' > "$TMP/existing"

minted=0
failed=0
for sub in "$@"; do
  if grep -qx "$sub" "$TMP/existing"; then
    echo "skip  $sub: already in secret/$SECRET"; continue
  fi
  lane_sub="$sub$LANE_SUFFIX"
  code="$(curl -sSk -o "$TMP/resp.json" -w '%{http_code}' -X POST "$MAAS_API/v1/api-keys" \
    -H "Authorization: Bearer $OPENSHIFT_TOKEN" \
    -H "Content-Type: application/json" \
    -H "X-MaaS-Username: $MAAS_USER" \
    -H "X-MaaS-Group: [\"$MAAS_GROUP\"]" \
    -d "{\"name\":\"loadgen-$lane_sub\",\"subscription\":\"$lane_sub\",\"expiresIn\":\"$EXPIRES_IN\"}")" || code=000
  # Writes the key to $TMP/key.<sub> and prints only the metadata. A non-2xx
  # body is an error message, not a key, but it is still not echoed raw.
  if ! python3 -I - "$TMP/resp.json" "$TMP/key.$sub" "$code" "$lane_sub" << 'PYEOF'
import json, sys
resp, keyfile, code, sub = sys.argv[1:5]
try:
    d = json.load(open(resp))
except Exception:
    d = {}
k = d.get("key", "")
if not code.startswith("2") or not k.startswith("sk-oai-"):
    print(f"FAIL  {sub}: HTTP {code}, fields={sorted(d)} -- see maas-api log")
    sys.exit(1)
open(keyfile, "w").write(k)
print(f"mint  {sub}: id={d.get('id')} name={d.get('name')} "
      f"subscription={d.get('subscription')} expiresAt={d.get('expiresAt')}")
PYEOF
  then
    # Stop, but still store whatever was already minted below -- a key that
    # exists in maas-api but in no secret is live and unaccounted for.
    rm -f "$TMP/resp.json"; failed=1; break
  fi
  rm -f "$TMP/resp.json"
  minted=$((minted + 1))
done

[ "$minted" -gt 0 ] || { echo "nothing minted"; exit "$failed"; }
python3 -I - "$TMP" > "$TMP/patch.json" << 'PYEOF'
import base64, glob, json, os, sys
data = {}
for p in glob.glob(os.path.join(sys.argv[1], "key.*")):
    data[os.path.basename(p)[4:]] = base64.b64encode(open(p, "rb").read()).decode()
json.dump({"data": data}, sys.stdout)
PYEOF
$OC patch secret "$SECRET" -n "$NAMESPACE" --type=merge --patch-file="$TMP/patch.json" >/dev/null
echo "patched secret/$SECRET with $minted key(s)"
exit "$failed"
