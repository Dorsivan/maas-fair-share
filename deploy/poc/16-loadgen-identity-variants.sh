#!/bin/bash
# UNI-129 D5: probe whether a request can reach the EPP with a missing or
# empty x-maas-subscription header -- and document exactly where in the
# gateway chain that is (or is not) possible today.
#
# This is NOT a closed-loop load generator like 04-loadgen.yaml/
# 12-loadgen-route.sh. D5 is a classification/auth-boundary question, not a
# fairness-share one, so a handful of single requests is the whole test.
#
# The mechanism (see docs/runbook.md "Identity-variant harness (UNI-129)"
# for the full story -- this header is a pointer, not the source of truth):
#
#   X-MaaS-Subscription is set by the per-model AuthPolicy
#   (maas-auth-<model>) as:
#     (has(auth.metadata) && has(auth.metadata.apiKeyValidation))
#       ? auth.metadata.apiKeyValidation.subscription : ""
#   apiKeyValidation only populates when the caller authenticated with a
#   valid "Bearer sk-oai-*" key, so a request that authenticates WITHOUT one
#   -- a plain Kubernetes ServiceAccount token, via the Gateway-level
#   maas-poc-gateway-authn AuthPolicy's "kubernetes-user" rule -- reaches
#   the EPP with this header forced to the empty string, regardless of
#   anything the client itself sent (docs/gateway-header-stripping.md
#   explains why an AuthPolicy response header always overwrites, never
#   appends).
#
#   LIVE FINDING (2026-11-01, against maas-vllm-gpu-kserve-route, the SUT
#   this whole repo measures): that path is CLOSED here, not open. Unlike
#   maas-vllm-cpu-kserve-route (which has no AuthPolicy of its own and so
#   still inherits the Gateway-level kubernetes-user rule unmodified --
#   see the 2026-10-19 live proof in docs/gateway-header-stripping.md,
#   which used exactly this mechanism against the CPU path), the GPU route
#   now has its OWN AuthPolicy (maas-auth-maas-vllm-gpu) whose
#   authentication rules ATOMICALLY REPLACE the Gateway-level ones for this
#   route rather than merging with them. Its two rules are "api-keys"
#   (needs a real sk-oai- key) and "kubernetes-tokens" (a k8s token is
#   accepted, but ONLY when request.url_path matches .*/v1/models$, which
#   /v1/chat/completions never does). A bare k8s token to
#   /v1/chat/completions therefore matches neither rule and gets 401 before
#   any identity reaches the EPP at all. Sending it to /v1/models instead
#   does authenticate, but then 403s at the require-group-membership
#   authorization check, since a ServiceAccount's own OpenShift groups
#   never appear in that policy's allowed_groups list -- and /v1/models
#   isn't the inference path the fairness plugin classifies on regardless.
#   Minting a key with the subscription field omitted or empty was also
#   tried directly against maas-api: omitting it silently assigns the
#   caller's own first eligible subscription (it does not mint a
#   no-subscription key), and naming a subscription that doesn't exist is
#   rejected outright at mint time (400 invalid_subscription). So on this
#   route, in this configuration, EVERY request that actually reaches the
#   backend carries a real, non-empty X-MaaS-Subscription.
#
#   This script exists to keep re-asking that question mechanically rather
#   than trusting the 2026-11-01 answer forever -- the same
#   "keeping this from silently regressing" concern
#   docs/gateway-header-stripping.md raises for the objective header applies
#   here too: any future change that attaches maas-vllm-gpu-kserve-route to
#   a DIFFERENT AuthPolicy (or removes maas-auth-maas-vllm-gpu and falls
#   back to the Gateway-level one) could reopen exactly this gap silently.
#
# Prerequisites:
#   - OPENSHIFT_TOKEN env var -- an identity with `get llminferenceservices`
#     in the target namespace (the Engineer's token qualifies; a bare
#     namespace "default" ServiceAccount does NOT -- confirmed separately,
#     see the runbook).
#   - One real end-user-* key already minted (for the control probe) --
#     reads it from the maas-loadgen-keys Secret, same as every other script
#     here.
#
# Usage:
#   OPENSHIFT_TOKEN=... ./deploy/poc/16-loadgen-identity-variants.sh [model]
# model defaults to maas-vllm-gpu (the SUT). Pass maas-vllm-cpu to reproduce
# the OPEN case for comparison -- note maas-vllm-cpu is normally scaled to 0
# (docs/runbook.md, "Restore maas-vllm-cpu from zero"); this script does not
# scale it up or down, so a CPU probe against a 0-replica pool will fail at
# the connection level, not the auth level, and that failure mode must not be
# misread as "the path is closed" -- it means the backend isn't up, not that
# the auth boundary held.
set -euo pipefail

NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
MODEL="${1:-maas-vllm-gpu}"
GW="${GW:-https://maas-gateway-${NAMESPACE}.apps.ocp.paladinaura.com}"
MODELPATH="/${NAMESPACE}/${MODEL}"
OC="oc --token=${OPENSHIFT_TOKEN:?set OPENSHIFT_TOKEN} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"

KEYDIR="$(mktemp -d)"
trap 'rm -rf "$KEYDIR"' EXIT
$OC get secret maas-loadgen-keys -n "$NAMESPACE" -o jsonpath='{.data.end-user-alpha}' | base64 -d > "$KEYDIR/end-user-alpha"

req() {
  local label="$1" auth_header="$2"
  local code
  code=$(curl -sS -o /dev/null -m 30 -w '%{http_code}' -X POST "$GW$MODELPATH/v1/chat/completions" \
    -H 'Content-Type: application/json' \
    -H "$auth_header" \
    -d '{"model":"llama-3-1-8b","max_tokens":5,"messages":[{"role":"user","content":"UNI-129 D5 probe"}]}' \
    2>/dev/null) || code="000"
  printf '%-28s %s\n' "$label" "$code"
}

echo "D5 probe: model=$MODEL route=$MODELPATH"
echo "---"
req "control (real sk-oai key)" "Authorization: Bearer $(cat "$KEYDIR/end-user-alpha")"
req "k8s-token, /v1/chat/completions" "Authorization: Bearer $OPENSHIFT_TOKEN"
code_models=$(curl -sS -o /dev/null -m 30 -w '%{http_code}' "$GW$MODELPATH/v1/models" \
  -H "Authorization: Bearer $OPENSHIFT_TOKEN" 2>/dev/null) || code_models="000"
printf '%-28s %s\n' "k8s-token, /v1/models" "$code_models"
echo "---"
echo "Expected on maas-vllm-gpu today: control=200, chat-completions=401, models=403."
echo "200 on the k8s-token chat-completions row would mean the gap reopened --"
echo "see this script's header comment for what to check first (which"
echo "AuthPolicy is attached to ${MODEL}-kserve-route)."
