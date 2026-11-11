#!/bin/bash
# UNI-54: a named, repeatable fairness benchmark whose output IS the fairness
# result, instead of a human reading Prometheus after the fact and doing the
# division by hand (see docs/poc-results.md's 1.57:1-against-2:1 detour).
#
# This wraps 04-loadgen.yaml the same way 14-loadgen-with-log-archive.sh
# (UNI-46) does -- same patched-copy-of-the-manifest mechanism, same
# restart-tolerant EPP container log capture -- and adds the two things that
# script does not: an exact before/after snapshot of the EPP's own
# llm_d_epp_maas_fairness_* counters (same mechanism as UNI-34's
# 13-loadgen-poisson.sh), and the per-run report (15-fairness-report.py) that
# turns both into a verdict. All three artifacts land in the same
# results/<timestamp>-<label>/ directory UNI-46 introduced, next to the EPP
# log, so a run ships with its own numbers next to its own evidence.
#
# This script does not duplicate 14's code by sourcing it (its EPP-log-follow
# loop and Job-polling loop are written as a single top-level flow, not
# functions, and 14 is independently reviewed and merged -- forking it here
# would create two copies to keep in sync). The capture and polling logic
# below is deliberately the same shape.
#
# Scope: GPU path only (board direction, 2026-10-19). EPP_SELECTOR targets
# the LLMInferenceService-managed scheduler pod
# (maas-vllm-gpu-kserve-router-scheduler-*), not the simulator's 02-epp.yaml
# Deployment. Passing a different EPP_SELECTOR/BACKEND is possible (the
# metrics-snapshot and log-capture mechanisms are backend-agnostic) but is
# out of this ticket's scope -- see --backend below, which only labels
# whatever you point it at, and does not validate it.
#
# Prerequisites:
#   - OPENSHIFT_TOKEN env var with edit access to maas-fairness-poc.
#   - `oc` and `python3` on PATH.
#   - deploy/rbac.yaml already applied (mints the /metrics reader token used
#     by the snapshot step, same as 13-loadgen-poisson.sh).
#
# Usage:
#   OPENSHIFT_TOKEN=... ./deploy/poc/15-fairness-benchmark.sh <scenario> [label]
#
# Scenarios (named per the four experiments already described in the
# comments of 04-loadgen.yaml, plus one negative control -- UNI-103):
#   full-contention        TENANTS="app1 app2 end-users", per-tenant workers
#                          32/32/128 (app1/app2/end-users) -- the weight-split
#                          headline test. Sized, not equal: see "Per-tenant
#                          worker sizing" below for why equal WORKERS=32
#                          failed on this backend (UNI-100/UNI-103) and where
#                          32/32/128 comes from (A4 Run 3, UNI-29).
#   end-users-idle         TENANTS="app1 app2", per-tenant workers 128/32
#                          (app1/app2) -- end-users' 65% must be absorbed by
#                          app1/app2, not reserved. app1 over-offers relative
#                          to app2 for the same reason end-users does in
#                          full-contention: app1 is the higher-share tenant
#                          once end-users is out of the pool (66.7% vs 33.3%),
#                          so it needs more concurrency to stay backlogged.
#   equal-workers-control  TENANTS="app1 app2 end-users", equal WORKERS (the
#                          ORIGINAL full-contention shape, kept as a named
#                          negative control -- UNI-103). Expected to NOT show
#                          the weighted split on this backend (work
#                          conservation drains the high-weight tenant's
#                          queue); the report marks it INFO, not PASS/FAIL,
#                          and it does not count toward this script's exit
#                          code or the suite's pass/fail bar.
#   app1-alone             TENANTS="app1" -- must receive ~100% of the pool.
#   app2-alone             TENANTS="app2" -- must receive ~100% of the pool.
#                          UNI-131: app1-alone only shows the highest-weight
#                          tenant is uncapped when alone; this is the same
#                          check for the lowest-weight tenant.
#   app2-idle              TENANTS="app1 end-users", per-tenant workers 32/104
#                          (app1/end-users) -- UNI-132: promotes the old
#                          by-hand "S3" check (docs/poc-results.md) into the
#                          automated benchmark. app2 is excluded entirely, so
#                          the pair's renormalized target is 23.5/76.5
#                          (20/(20+65), 65/(20+65)), and per the UNI-104
#                          lesson the offered-worker ratio is sized to match
#                          that target ratio (20:65) rather than reusing
#                          either existing scenario's ratio verbatim: app1
#                          anchored at the usual 32, end-users scaled to
#                          32*65/20=104.
#   app1-idle              TENANTS="app2 end-users", per-tenant workers
#                          32/208 (app2/end-users) -- UNI-133: fourth and
#                          hardest case in this A-series (A1 app2-alone/
#                          UNI-131, A3 app2-idle/UNI-132, this is A4). app1 is
#                          excluded entirely, leaving the pair with the most
#                          extreme ratio of the three possible pairs (10:65,
#                          6.5:1 -- vs. 2:1 for app1:app2 and 1:3.25 for
#                          app1:end-users), so renormalized target is
#                          13.3/86.7 (10/(10+65), 65/(10+65)). Same UNI-104
#                          sizing lesson as app2-idle: anchor the smaller
#                          weight (app2) at the usual 32, scale the larger
#                          (end-users) to match the ratio exactly rather than
#                          reusing another scenario's figure --
#                          32*65/10=208.
#   app2-trickle           TENANTS="app1 app2 end-users" (all three offered,
#                          unlike app2-idle/app1-idle which exclude one
#                          entirely), per-tenant workers 32/2/104
#                          (app1/app2/end-users) -- UNI-134: A5, promoting the
#                          by-hand "S2"/"S4" checks (docs/poc-results.md
#                          "Scenario matrix") into the benchmark. app1 and
#                          end-users are HARD (over-offered); app2 trickles at
#                          2 workers, well under its own weight entitlement.
#                          Expected: app2's weight is a floor, not a ceiling,
#                          so it is not throttled further -- it gets ~100% of
#                          what it asks for -- and its unused entitlement goes
#                          to app1/end-users, who split it in their own 20:65
#                          ratio, renormalized to 23.5/76.5 exactly as
#                          app2-idle's pair (the ratio BETWEEN app1 and
#                          end-users is unaffected by app2's presence). Same
#                          sizing as app2-idle for app1/end-users; app2's 2
#                          workers is the literal S2/S4 trickle figure, not
#                          derived from a ratio.
#   asymmetric-demand      WORKERS_APP1=32, WORKERS_APP2=0,
#                          WORKERS_END_USERS=2 -- the exact commented-out
#                          example in 04-loadgen.yaml's per-tenant-override
#                          block. Note this sets app2 idle too (0 workers),
#                          which is that block's own documented example; the
#                          ticket prose only names APP1/END_USERS but the
#                          YAML comment it points to is the source of truth
#                          here.
#   below-capacity         TENANTS="app1 app2 end-users", per-tenant workers
#                          6/6/26 (app1/app2/end-users) -- UNI-135: A6 "below
#                          capacity, everyone light." Each tenant is sized to
#                          ~20% of the same per-tenant ceiling full-contention
#                          uses to saturate the pool (32/32/128 -- the most
#                          recent determined saturating config, UNI-29/A4 Run
#                          3): 32*0.2=6.4->6, 32*0.2=6.4->6, 128*0.2=25.6->26.
#                          Expected: nobody is ever backlogged alongside
#                          anyone else at this concurrency --
#                          15-fairness-report.py's "UNCONTENDED" verdict
#                          (neither PASS nor FAIL) is this scenario's correct
#                          result, not a weighted-split score.
#   cache-heavy-vs-cache-cold
#                          TENANTS="app1 app2", per-tenant workers 64/32 --
#                          UNI-136: C8, cache-heavy vs cache-cold tenant, the
#                          evidence for the cachedInputTokenWeight decision
#                          (Outstanding item 2, docs/poc-results.md).
#                          CACHE_SHAPE_APP1=hot (a byte-identical shared
#                          prefix, deploy/poc/10-cache-profile.yaml's app1
#                          shape) vs CACHE_SHAPE_APP2=cold (fully unique
#                          prompts every request, that file's app2/control
#                          shape) -- both run at the live default
#                          cachedInputTokenWeight: 1.0, so neither is
#                          discounted for its cache hits. Same 64/32 (2:1)
#                          sizing as end-users-idle's app1:app2 pair, the only
#                          existing scenario already proven to over-offer both
#                          sides of this exact pairing (20:10 weight ratio).
#                          Run this scenario with the EPP pod freshly
#                          restarted (so prompt_tokens_cached_ratio -- a
#                          cumulative-since-process-start Gauge, not scoped to
#                          one run -- reads clean); 15-fairness-benchmark.sh
#                          does not do this automatically. This is a
#                          characterisation, not a scored case (the ticket
#                          asks for the split by charged tokens/request
#                          count/cache ratio, not a PASS/FAIL), so it runs
#                          with --control to report the numbers without
#                          scoring them against the weighted-split threshold.
#   shadow-mode-control    TENANTS="app1 app2 end-users", same 32/32/128
#                          sizing as full-contention -- UNI-159: F1, the
#                          second negative control in this series (the first
#                          is equal-workers-control above, UNI-103). This
#                          scenario owns its own live-config flip: it sets
#                          maas-epp-config's `enforce` key to false (shadow
#                          mode -- the plugin observes and scores dispatch
#                          but never reorders the queue) before the run and
#                          restores whatever `enforce` was before at the same
#                          restore point/hazard ENFORCE_LIVE uses (see
#                          SHADOW_MODE below); an operator does not pass
#                          SHADOW_MODE=true by hand for this scenario, it is
#                          hardcoded in the case block. Expected: close to
#                          equal thirds, the same work-conservation
#                          compression equal-workers-control shows, because
#                          nothing is left to enforce the weighted split.
#                          Scored INFO, like every other named negative
#                          control, not PASS/FAIL.
#   app1-flood             TENANTS="app1 app2 end-users", per-tenant workers
#                          256/32/64 (app1/app2/end-users) -- UNI-161: board
#                          case, end-users standing in for "app3" at a
#                          reweighted 30/10/60 (the operator patches
#                          maas-epp-config's three group weights to 30/10/60
#                          before invoking this scenario and restores
#                          20/10/65 after; this script does not own that
#                          weight patch itself, same division of
#                          responsibility UNI-160/F3 used for its own
#                          alternative weight sets). app1 deliberately
#                          over-offers far harder than its own entitlement
#                          needs (8x full-contention's usual 32, against a
#                          weight that only doubled from 20 to 30) --
#                          UNI-104 found that heavy over-offering by the
#                          dominant tenant can push its measured share past
#                          its configured weight (82% vs 67%); this sizing
#                          is deliberately chosen to re-expose that same
#                          failure mode at a different ratio, not to avoid
#                          it. app2/end-users keep roughly full-contention's
#                          own over-offering discipline (32, and 64 -- half
#                          of full-contention's 128, since 60 is roughly
#                          full-contention's 65 scaled by this scenario's
#                          own total offered weight) so neither is the
#                          reason for any deviation seen in app1.
#
# Per-tenant worker sizing (see docs/runbook.md "Per-tenant worker sizing
# and the saturation check" for the full method): every ACTIVE tenant in a
# scored scenario must offer more concurrency than its entitlement, or its
# queue periodically drains and the measured split compresses toward equal
# shares no matter what the weights say (docs/poc-results.md, "The detour,
# and the lesson in it", and the 2026-10-29 UNI-100 finding that reproduced
# it on full-contention/end-users-idle). That is why full-contention and
# end-users-idle now set PER_TENANT_OVERRIDES instead of relying on a single
# global WORKERS for every tenant -- WORKERS alone cannot express "this
# tenant needs more offered load than that one," which is exactly what a
# weighted split requires once the weights differ.
#
# Overrides: WORKERS, DURATION, NAMESPACE, OPENSHIFT_SERVER, EPP_SELECTOR,
# EPP_CONTAINER, BACKEND, THRESHOLD_POINTS (default 10 -- see
# docs/runbook.md "Run the fairness benchmark" for how that number was
# chosen).
#
# UNI-127 harness additions (see docs/runbook.md "Timeline, chaos, and
# windowed reporting" for the full story -- this header is a pointer, not the
# source of truth):
#   WINDOW_SECONDS           time-series snapshot interval, default 10.
#   APP1_START/STOP/DUTY, APP2_START/STOP/DUTY, END_USERS_START/STOP/DUTY
#                             per-tenant timeline, e.g. END_USERS_START=120s.
#                             Unset (the default) = active the whole run, same
#                             as every scenario before this ticket.
#   CHAOS_EPP_DELETE_AT       delete the EPP scheduler pod at t+<seconds>.
#   CHAOS_SCALE_AT            scale LLMISVC_NAME (default maas-vllm-gpu) to 1
#                             replica at t+<seconds>, restored after
#                             CHAOS_SCALE_HOLD (default 30s).
# UNI-128 harness additions (see docs/runbook.md "Request-shape profiles
# (UNI-128)" for the full story -- this header is a pointer, not the source
# of truth): PROMPT_WORDS_MIN/MAX, MAX_TOKENS_DEFAULT/OMIT_FRACTION/
# HUGE_FRACTION/HUGE_VALUE, STREAM_FRACTION, ABORT_FRACTION/MIN_FRACTION/
# MAX_FRACTION, OVERSIZED_FRACTION/PROMPT_WORDS, LONG_GEN_FRACTION/
# MAX_TOKENS, REQUEST_TIMEOUT_SECONDS -- passed through to the Job unchanged
# when set. All default to the single fixed request shape this benchmark
# sent before this ticket; a plain scenario invocation is unaffected.
# UNI-129 harness additions (see docs/runbook.md "Identity-variant harness
# (UNI-129)" for the full story -- this header is a pointer, not the source
# of truth): END_USERS_KEYS (D1 key-rotation list), FORGE_FAIRNESS_ID_FRACTION/
# FORGE_FAIRNESS_ID_VALUE (D3 forged header), CUSTOM_SUBSCRIPTION_NAME/
# WORKERS_CUSTOM/CUSTOM_START/CUSTOM_STOP/CUSTOM_DUTY (D2 arbitrary identity,
# needs TENANTS to include "custom"). All default to this benchmark's
# pre-UNI-129 behaviour when unset. D5 (a path reaching the EPP with a
# missing/empty x-maas-subscription) is NOT a 04-loadgen.yaml knob -- see
# deploy/poc/16-loadgen-identity-variants.sh and the runbook section above.
# UNI-138 harness addition (see docs/runbook.md "The client-side record" and
# "G2: ledger cross-check" for the full story): LEDGER_TOLERANCE_PCT (default
# 10) is the max absolute percent difference the report's ledger section
# allows between the EPP's own accounting and 04-loadgen.yaml's client-side
# CLIENT_RECORD_JSON before a group fails that cross-check. The cost-model
# weights the ledger needs to compare against contended_service_tokens_total
# (inputTokenWeight/outputTokenWeight/cachedInputTokenWeight) are not a
# benchmark override -- they are read live from the maas-epp-config
# ConfigMap below, since no metric exposes them and hardcoding them here
# would silently go stale the next time that ConfigMap is retuned.
# UNI-174 harness addition: ENFORCE_LIVE (default false). Until this ticket,
# flipping the live maas-epp-config ConfigMap's `enforce` key from false to
# true was a manual `oc` step the operator did around the run (see
# docs/poc-results.md's "Reproduce:" paragraph) -- which meant nothing ever
# reverted it if the run died first. ENFORCE_LIVE=true brings that flip under
# this script's own ownership: it patches the ConfigMap, confirms both EPPs
# (maas-vllm-gpu AND maas-vllm-cpu share this one ConfigMap -- see
# deploy/poc/09-vllm-gpu.yaml and 07-vllm-cpu.yaml's identical
# scheduler.config.ref) report llm_d_epp_maas_fairness_enforcing=1 before
# proceeding, and reverts it -- checked via the same metric, not the
# ConfigMap -- on every exit path this script has: normal completion, any
# `exit`, and SIGINT/SIGTERM/SIGHUP. It CANNOT revert on SIGKILL (-9): that
# signal is not trappable by any process, bash included, so a `kill -9` on
# this script (or its unattended death, e.g. an OOM) still leaves the
# cluster enforcing with nothing to fix it automatically. Default (unset) is
# unaffected: a plain invocation only ever reads the live ConfigMap's current
# state for the report, exactly as before this ticket. See docs/runbook.md
# "Live enforce flip (UNI-174)" for the full mechanism and why a flag+trap
# in this script was chosen over a separate flip/revert wrapper.
# UNI-179 harness additions (see docs/runbook.md "Per-group configuration
# (UNI-179)" -- this header is a pointer, not the source of truth):
# LOADGEN_GROUPS (the group table, any N; unset = the scenario's TENANTS),
# and per-group WORKERS_<TOKEN>, <TOKEN>_KEYS, <TOKEN>_START/STOP/DUTY and
# <KNOB>_<TOKEN> for every 04-loadgen.yaml GROUP_KNOBS knob (e.g.
# STREAM_FRACTION_APP2=1), passed through when set. The names that already
# existed before UNI-179 keep their old route (scenario-owned or one of the
# lists above), so a plain scenario invocation is unaffected.
#
# UNI-180 harness addition: ENFORCE_LIVE, CHAOS_EPP_DELETE_AT and
# CHAOS_SCALE_AT (above) were three hand-rolled patch/compare/revert pairs
# touching the same ConfigMap and the same `on_exit` trap -- UNI-158/159/160/
# 162 each needing their own flip for a DIFFERENT live value (weights,
# newcomerClamp, a Kuadrant TokenRateLimitPolicy) would have made that four
# or five, each with its own chance to leave the cluster dirty. All three now
# sit on top of one generic set/restore wrapper (`live_config_set`/
# `live_config_restore`, defined below) instead -- same env var names, same
# behaviour, just one mechanism underneath. The wrapper also backs a new,
# generic mid-run hook for anything that isn't already a named knob:
#   LIVE_SET_AT       seconds-offset to apply LIVE_SET_TARGET/LIVE_SET_VALUE,
#                      same "120s or bare 120" shorthand as the chaos hooks.
#   LIVE_SET_TARGET   what to change -- one of:
#                        epp-key:<key>             scalar key in
#                                                   maas-epp-config's data.epp
#                                                   (e.g. newcomerClamp,
#                                                   halfLifeSeconds)
#                        epp-weight:<group>        that group's `weight:` in
#                                                   the same file's `groups:`
#                                                   list (app1, app2,
#                                                   end-users) or
#                                                   `defaultGroup`
#                                                   (unclassified)
#                        field:<res>:<name>:<path>  a dotted JSON field on any
#                                                   named namespaced resource,
#                                                   via `oc patch --type=merge`
#                                                   (e.g.
#                                                   field:llmisvc:maas-vllm-gpu:spec.replicas,
#                                                   or a Kuadrant
#                                                   TokenRateLimitPolicy's
#                                                   spec.limits.<name>.rates)
#   LIVE_SET_VALUE    the new value (a bare scalar for epp-key/epp-weight; a
#                      JSON scalar/array/object, or a bare string, for
#                      field: -- it is tried as JSON first and used literally
#                      if that fails).
#   LIVE_SET_HOLD     optional seconds-offset AFTER LIVE_SET_AT to restore at,
#                      like CHAOS_SCALE_HOLD. Only honored for a `field:`
#                      target -- an epp-key/epp-weight target recreates the
#                      EPP pod and zeroes its fairness counters (the same
#                      hazard ENFORCE_LIVE's own revert avoids), so restoring
#                      one WHILE the Job is still running would corrupt a
#                      live measurement instead of just starting one at zero.
#                      That kind always restores at the same post-metrics-after
#                      point ENFORCE_LIVE's revert uses, LIVE_SET_HOLD or not.
# All four are unset by default, so a plain invocation is unaffected. Every
# live-config change this wrapper makes is also recorded as a `live_set`/
# `live_restore` entry in timeline-config.json's chaos_events, the same list
# CHAOS_EPP_DELETE_AT/CHAOS_SCALE_AT already populate -- 15-fairness-report.py's
# phase-edge maths only ever reads an event's generic `at_seconds`, so this
# needed no report-side change. See docs/runbook.md "Generic live-config
# set/restore wrapper (UNI-180)" for the full mechanism and its known gaps.
# UNI-163 fix: firing LIVE_SET_AT mid-run against an epp-key/epp-weight target,
# or a field: target that happens to be this same ConfigMap's epp key, was a
# gap UNI-180 shared with CHAOS_EPP_DELETE_AT before UNI-193 fixed it there --
# chaos_loop now calls the same resolve_replacement_pod_async after applying
# such a target, so capture_loop and the mid-run restart detector follow the
# EPP pod's replacement instead of silently watching the one just recreated.
# See live_set_target_recreates_pod below.
#
# UNI-159 harness addition: SHADOW_MODE (default false), the mirror image of
# ENFORCE_LIVE for the opposite direction. ENFORCE_LIVE only ever confirms and
# flips TOWARD enforce=true (UNI-174's own wait_for_enforcing("1")); F1 (the
# shadow-mode-control scenario, see above) needs the opposite -- flip the live
# `enforce` key to false, run full-contention sizing, and restore whatever it
# was before. SHADOW_MODE=true does exactly that: flips maas-epp-config's
# enforce to false before the run (no-op, and not reverted on exit, if it was
# already false -- same "did this run actually cause the state" guard
# ENFORCE_LIVE uses), confirms llm_d_epp_maas_fairness_enforcing=0 on both
# EPPs via the same wait_for_enforcing helper, and reverts at the same
# post-after-snapshot point revert_enforce_live uses (same pod-recreate/
# zeroed-counters hazard -- see the UNI-143 note on revert_enforce_live
# below). ENFORCE_LIVE=true and SHADOW_MODE=true together are rejected: they
# name opposite target values for the same key, so there is no "both" to
# converge on. This scenario sets SHADOW_MODE itself in its case-statement
# branch -- an operator does not need to (and should not) pass it by hand for
# any other scenario. Unset (every scenario before this ticket, and every
# scenario except shadow-mode-control after it) leaves this knob's entire
# code path untouched.
# UNI-149 harness addition: SETTLE_SECONDS (default 0, no-op). The Job-poll
# loop below only proves the loadgen stopped SENDING requests -- it says
# nothing about whether the EPP has finished accounting for the ones already
# in flight (a client abort has to propagate through the gateway before the
# plugin's ResponseBody hook fires and releases that request's hold). Setting
# SETTLE_SECONDS keeps capture_loop/timeseries_loop/chaos_loop running for
# that many extra seconds after the Job completes, before the after-snapshot
# and ENFORCE_LIVE/LIVE_SET_AT revert -- so a claim like "provisional tokens
# return to zero once traffic stops" is read off the live epp-container.log
# flight recorder instead of inferred from the before/after delta. 0 leaves
# every scenario before this ticket byte-for-byte unaffected.
set -euo pipefail

SCENARIO="${1:?usage: $0 <scenario> [label]; scenarios: full-contention full-contention-discriminating full-contention-2x full-contention-2x-discriminating end-users-idle end-users-idle-discriminating equal-workers-control app1-alone app2-alone app2-idle app2-idle-discriminating app1-idle app1-idle-discriminating app2-trickle app2-trickle-discriminating asymmetric-demand below-capacity cache-heavy-vs-cache-cold max-tokens-skew asymmetric-request-shapes near-timeout-long-generations shadow-mode-control app1-flood app1-flood-moderate app1-flood-light app3-joins-at-saturation six-group-board-case twenty-group-scale uni165-equal-discriminating uni165-graded-discriminating uni165-subset-3-idle-discriminating uni165-equal-2x-discriminating twenty-group-scale-discriminating}"
LABEL="${2:-$SCENARIO}"

# UNI-174: computed this early (rather than just before the manifest-resolve
# step, where it used to live) so the exit trap registered below -- and the
# enforce-flip/revert functions it owns -- have a results directory to write
# their log and scratch files into no matter how early a crash happens.
TS="$(date -u +%Y%m%dT%H%M%SZ)"
ARTIFACT_DIR="$(pwd)/results/${TS}-${LABEL}"
mkdir -p "$ARTIFACT_DIR"
ENFORCE_LOG="$ARTIFACT_DIR/enforce-events.log"
: > "$ENFORCE_LOG"
enforce_log() {
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $1" | tee -a "$ENFORCE_LOG"
}

NAMESPACE="${NAMESPACE:-maas-fairness-poc}"
OC="oc --token=${OPENSHIFT_TOKEN:?set OPENSHIFT_TOKEN} --server=${OPENSHIFT_SERVER:-https://api.ocp.paladinaura.com:6443}"

# UNI-210: maas-poc-gateway-authn is controller-owned (odh-model-controller/
# KServe regenerates it when an LLMInferenceService reconciles) and this
# script's scenarios routinely patch spec.replicas / scheduler.config.ref on
# exactly the LLMInferenceServices that trigger that reconcile -- chaos-scale,
# ENFORCE_LIVE, LIVE_SET_*, twenty-group-scale all do. The UNI-33 header-
# stripping patch (deploy/maas/09-objective-header-stripping.patch.yaml) was
# found silently reverted live on 2026-11-09 after three weeks of such runs
# with nothing re-checking it -- see docs/gateway-header-stripping.md and
# UNI-210. Re-check and, if needed, re-apply before any run touches the
# LLMInferenceServices, instead of trusting the last manual verification.
objective_header_stripped() {
  $OC get authpolicy maas-poc-gateway-authn -n "$NAMESPACE" -o json 2>/dev/null \
    | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(1)
headers = (d.get("spec", {}).get("rules", {}).get("response", {})
            .get("success", {}).get("headers", {}))
entry = headers.get("x-llm-d-inference-objective")
sys.exit(0 if isinstance(entry, dict) and entry.get("plain", {}).get("expression") else 1)
'
}

gateway_header_gate() {
  if objective_header_stripped; then
    enforce_log "UNI-210 gate: x-llm-d-inference-objective is stripped at maas-poc-gateway-authn"
    return
  fi
  echo "[benchmark] WARNING: x-llm-d-inference-objective is NOT stripped at maas-poc-gateway-authn (UNI-210 regression) -- re-applying deploy/maas/09-objective-header-stripping.patch.yaml" >&2
  enforce_log "UNI-210 gate: objective header NOT stripped at run start -- re-applying patch"
  $OC patch authpolicy maas-poc-gateway-authn -n "$NAMESPACE" --type=merge \
    --patch-file=deploy/maas/09-objective-header-stripping.patch.yaml >/dev/null
  if objective_header_stripped; then
    enforce_log "UNI-210 gate: re-applied patch, objective header now stripped"
  else
    echo "[benchmark] FATAL: x-llm-d-inference-objective is still not stripped at maas-poc-gateway-authn after re-applying the patch -- a measurement run now would be against a gateway where a forged header can jump every priority band. See docs/gateway-header-stripping.md and UNI-210." >&2
    exit 1
  fi
}
gateway_header_gate

EPP_SELECTOR="${EPP_SELECTOR:-app.kubernetes.io/component=llminferenceservice-router-scheduler,app.kubernetes.io/name=maas-vllm-gpu}"
EPP_CONTAINER="${EPP_CONTAINER:-main}"
BACKEND="${BACKEND:-vllm-gpu (real)}"
THRESHOLD_POINTS="${THRESHOLD_POINTS:-10}"
# UNI-138 (G2): default picked and justified in docs/poc-results.md's G2
# section from this ticket's own full-contention run -- not a guess.
LEDGER_TOLERANCE_PCT="${LEDGER_TOLERANCE_PCT:-10}"
JOB_NAME="maas-loadgen"
DURATION="${DURATION:-240}"

# UNI-127: windowed time-series reporting (default on for every run) and the
# optional timeline/chaos harness. None of these change a single thing about
# an invocation that does not set them -- that is the regression bar this
# ticket has to clear.
WINDOW_SECONDS="${WINDOW_SECONDS:-10}"
LLMISVC_NAME="${LLMISVC_NAME:-maas-vllm-gpu}"
# Seconds-offset chaos hooks, accepting the ticket's "120s" shorthand or a
# bare integer. Empty (the default) means that hook never fires.
CHAOS_EPP_DELETE_AT="${CHAOS_EPP_DELETE_AT:-}"
CHAOS_EPP_DELETE_AT="${CHAOS_EPP_DELETE_AT//s/}"
CHAOS_SCALE_AT="${CHAOS_SCALE_AT:-}"
CHAOS_SCALE_AT="${CHAOS_SCALE_AT//s/}"
CHAOS_SCALE_HOLD="${CHAOS_SCALE_HOLD:-30s}"
CHAOS_SCALE_HOLD="${CHAOS_SCALE_HOLD//s/}"

# UNI-180: generic mid-run live-config hook -- see the header comment above
# for what each knob means. Empty LIVE_SET_AT (the default) means this fires
# nothing, same as the chaos hooks above.
LIVE_SET_AT="${LIVE_SET_AT:-}"
LIVE_SET_AT="${LIVE_SET_AT//s/}"
LIVE_SET_TARGET="${LIVE_SET_TARGET:-}"
LIVE_SET_VALUE="${LIVE_SET_VALUE:-}"
LIVE_SET_HOLD="${LIVE_SET_HOLD:-}"
LIVE_SET_HOLD="${LIVE_SET_HOLD//s/}"
if [ -n "$LIVE_SET_AT" ] && { [ -z "$LIVE_SET_TARGET" ] || [ -z "$LIVE_SET_VALUE" ]; }; then
  echo "[benchmark] FATAL: LIVE_SET_AT requires both LIVE_SET_TARGET and LIVE_SET_VALUE to be set" >&2
  exit 1
fi
if [ -z "$LIVE_SET_AT" ] && { [ -n "$LIVE_SET_TARGET" ] || [ -n "$LIVE_SET_VALUE" ] || [ -n "$LIVE_SET_HOLD" ]; }; then
  echo "[benchmark] FATAL: LIVE_SET_TARGET/LIVE_SET_VALUE/LIVE_SET_HOLD have no effect without LIVE_SET_AT -- set all of LIVE_SET_AT/LIVE_SET_TARGET/LIVE_SET_VALUE together" >&2
  exit 1
fi

# UNI-174: live `enforce` flip, owned end-to-end by this script -- see the
# header comment above. false/unset leaves this run purely observational
# (reads whatever `enforce` currently is, same as every invocation before
# this ticket).
# 180s default: measured on 2026-11-02 against this cluster's real
# LLMInferenceService-managed scheduler Deployment, a ConfigMap-triggered
# roll (new pod, not an in-place config reload) took ~50-90s end to end
# (old pod Terminating -> new pod Running -> Service endpoints updated ->
# scrapeable) for a SINGLE EPP, and this waits on both. 60s timed out on that
# measurement run even though the flip itself was correct -- see
# docs/runbook.md "Live enforce flip (UNI-174)" for the full kill-test
# evidence. Not tunable down safely without re-measuring this cluster's
# rollout latency.
ENFORCE_LIVE="${ENFORCE_LIVE:-false}"
# UNI-159: mirror of ENFORCE_LIVE for the opposite flip direction -- see the
# header comment above. Read here (before shadow-mode-control's case-block
# branch can set it) so an operator-supplied SHADOW_MODE=true on a DIFFERENT
# scenario is still honored instead of silently ignored.
SHADOW_MODE="${SHADOW_MODE:-false}"
ENFORCE_WAIT_TIMEOUT_SECONDS="${ENFORCE_WAIT_TIMEOUT_SECONDS:-180}"
CONFIGMAP_NAME="maas-epp-config"
CPU_EPP_METRICS_SVC="${CPU_EPP_METRICS_SVC:-maas-vllm-cpu-epp-service}"
CPU_LLMISVC_NAME="${CPU_LLMISVC_NAME:-maas-vllm-cpu}"

# --- UNI-174: every variable the exit trap below can reference must already
# exist by the time the trap is registered -- `set -u` turns a reference to
# an as-yet-unset one into a hard failure, which is exactly the kind of crash
# this ticket is about making survivable, not a second way to cause it. The
# trap is registered a few lines down, before anything that actually mutates
# cluster state (the Job delete right after this block is the first mutation
# in the script), so it is live for the entire run -- including a crash
# inside the mutating calls themselves, not just the window after them.
CAPTURE_PID=""
CAPTURE_OC_PIDFILE=""
EVENTS_PID=""
TS_PID=""
CHAOS_PID=""
ORIGINAL_REPLICAS=""
ENFORCE_FLIPPED="false"
SHADOW_FLIPPED="false"
METRICS_TOKEN=""
EPP_METRICS_SVC_IP=""
CPU_EPP_METRICS_SVC_IP=""
CPU_EPP_ABSENT="false"

read_enforcing() {
  # $1 = EPP metrics ClusterIP. Prints 0/1, or nothing if the scrape failed
  # (treated as "not yet confirmed", never as a success).
  curl -sS -m 10 -H "Authorization: Bearer $METRICS_TOKEN" "http://$1:9090/metrics" 2>/dev/null \
    | awk '/^llm_d_epp_maas_fairness_enforcing/ {print ($2==1)?"1":"0"}'
}

wait_for_enforcing() {
  # $1 = desired value, "1" or "0". Polls both EPPs (they share one
  # ConfigMap -- see the UNI-174 header note) every 2s up to
  # ENFORCE_WAIT_TIMEOUT_SECONDS. Logs the outcome either way; the caller
  # decides whether a timeout is fatal.
  local want="$1" gpu_val cpu_val waited=0
  while :; do
    gpu_val="$(read_enforcing "$EPP_METRICS_SVC_IP")"
    if [ "$CPU_EPP_ABSENT" = "true" ]; then
      cpu_val="absent"
      if [ "$gpu_val" = "$want" ]; then
        enforce_log "confirmed: llm_d_epp_maas_fairness_enforcing=$want on the GPU EPP, the only EPP in $NAMESPACE (gpu=$gpu_val cpu=absent)"
        return 0
      fi
    else
      cpu_val="$(read_enforcing "$CPU_EPP_METRICS_SVC_IP")"
      if [ "$gpu_val" = "$want" ] && [ "$cpu_val" = "$want" ]; then
        enforce_log "confirmed: llm_d_epp_maas_fairness_enforcing=$want on both EPPs (gpu=$gpu_val cpu=$cpu_val)"
        return 0
      fi
    fi
    if [ "$waited" -ge "$ENFORCE_WAIT_TIMEOUT_SECONDS" ]; then
      enforce_log "WARNING: timed out after ${ENFORCE_WAIT_TIMEOUT_SECONDS}s waiting for enforcing=$want (gpu=${gpu_val:-?} cpu=${cpu_val:-?})"
      return 1
    fi
    sleep 2
    waited=$((waited + 2))
  done
}

resolve_cpu_epp() {
  # UNI-231: lanes 2 and 3 run no CPU LLMInferenceService, so their
  # maas-epp-config has one reader, not two. Keyed on the LLMISVC (the thing
  # that actually reads the ConfigMap), not on its Service. --ignore-not-found
  # turns only NotFound into an empty answer; Forbidden or an API error still
  # fails under set -e, so lane 1 cannot silently lose its second
  # confirmation.
  if [ -z "$($OC get llminferenceservice "$CPU_LLMISVC_NAME" -n "$NAMESPACE" --ignore-not-found -o name)" ]; then
    CPU_EPP_ABSENT="true"
    enforce_log "no llminferenceservice/$CPU_LLMISVC_NAME in $NAMESPACE -- maas-epp-config has one reader here; confirming the GPU EPP only"
  else
    CPU_EPP_METRICS_SVC_IP="$($OC get svc "$CPU_EPP_METRICS_SVC" -n "$NAMESPACE" -o jsonpath='{.spec.clusterIP}')"
  fi
}

patch_configmap_epp() {
  # $1 = file containing the new data.epp value. Merge-patches only that one
  # key (confirmed the ONLY key in this ConfigMap's .data, but a merge patch
  # leaves any others alone regardless) via a file so python owns the JSON
  # string-escaping of a multi-line YAML blob instead of shell quoting it.
  local body_file="$1" patch_file="$ARTIFACT_DIR/.enforce-patch.json"
  python3 -I - "$body_file" "$patch_file" << 'PYEOF'
import sys, json
body_file, patch_file = sys.argv[1], sys.argv[2]
body = open(body_file).read()
json.dump({"data": {"epp": body}}, open(patch_file, "w"))
PYEOF
  $OC patch configmap "$CONFIGMAP_NAME" -n "$NAMESPACE" --type=merge --patch-file="$patch_file" >/dev/null
}

# --- UNI-180: generic live-config set/restore wrapper -----------------------
# One mechanism for "patch something live, remember what it was, put it back"
# used by ENFORCE_LIVE, CHAOS_SCALE_AT and LIVE_SET_AT alike -- see the header
# comment above for the target-spec grammar (epp-key:/epp-weight:/field:).
#
# State lives in files under $ARTIFACT_DIR/live-config/, not bash variables,
# on purpose: LIVE_SET_AT and CHAOS_SCALE_AT fire from the chaos_loop
# background subshell (`chaos_loop &` below), and a subshell's variables never
# make it back to the parent shell that runs the `on_exit` trap -- but its
# writes to $ARTIFACT_DIR do. live_config_restore is therefore idempotent by
# re-reading the live value and comparing it to what it last applied, the same
# "query, don't trust a flag" pattern the pre-UNI-180 revert_enforce_live/
# restore_chaos_scale already used -- it is safe to call from the chaos-loop
# subshell, the explicit post-run call, AND the on_exit trap without
# double-reverting.
live_config_dir() {
  mkdir -p "$ARTIFACT_DIR/live-config"
  echo "$ARTIFACT_DIR/live-config"
}

LIVE_CONFIG_LOG="$ARTIFACT_DIR/live-config-events.log"
: > "$LIVE_CONFIG_LOG"
live_config_log() {
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $1" | tee -a "$LIVE_CONFIG_LOG"
}

extract_epp_key() {
  # $1 = key. Current scalar value of that key, read fresh from the LIVE
  # ConfigMap every call (never cached) so a restore computed against a stale
  # blob can't clobber an unrelated concurrent edit. Deliberately captures the
  # REST OF THE LINE verbatim, including a trailing inline comment if the key
  # has one (e.g. deploy/epp-config.yaml's `outputTokenWeight: 2.0   #
  # PLACEHOLDER until calibrated`) -- that is what round-trips losslessly
  # through live_config_set/_restore's before/apply/restore cycle. It does
  # mean a `LIVE_SET_VALUE` for such a key is compared against (and, while
  # applied, replaces) a value WITH that comment text; write LIVE_SET_VALUE
  # without a comment of your own and this still restores the original
  # comment correctly, it just won't be live while the new value is.
  # The ConfigMap text goes into a FILE, read by argv path, not piped into
  # this python call's own stdin -- `cmd | python3 -I - << 'EOF'` would make
  # the heredoc BOTH the script python reads itself from AND (once that read
  # hits EOF) what sys.stdin.read() sees inside the script, i.e. nothing ever
  # arrives from the pipe. Confirmed live on 2026-11-02: an earlier version of
  # this function that piped into the heredoc always read an empty string,
  # which made extract_epp_key report "key not found" for a key that was
  # plainly present, and worse, made live_config_restore's idempotency check
  # treat "could not read" the same as "nothing to revert" -- a real run left
  # newcomerClamp stuck at the SET value instead of restoring it. Every other
  # oc-output-into-python call in this script already uses this file-argv
  # pattern (see patch_configmap_epp); this just brings extract_epp_key/
  # extract_epp_weight in line with it instead of introducing a second one.
  local tmp
  tmp="$(live_config_dir)/.scratch-read.yaml"
  $OC get configmap "$CONFIGMAP_NAME" -n "$NAMESPACE" -o jsonpath='{.data.epp}' > "$tmp"
  python3 -I - "$tmp" "$1" << 'PYEOF'
import sys, re
path, key = sys.argv[1], sys.argv[2]
text = open(path).read()
m = re.search(r'^[ \t]*' + re.escape(key) + r':[ \t]*(\S.*)$', text, re.MULTILINE)
if not m:
    sys.exit(f"{key}: key not found in maas-epp-config's data.epp")
print(m.group(1))
PYEOF
}

extract_epp_weight() {
  # $1 = group name. Current `weight:` number for that group's entry in the
  # live ConfigMap's `groups:` list, or its `defaultGroup:` mapping if the
  # name is "unclassified" -- see deploy/epp-config.yaml.
  # See extract_epp_key's comment: file-argv, never piped into this command's
  # own heredoc stdin.
  local tmp
  tmp="$(live_config_dir)/.scratch-read.yaml"
  $OC get configmap "$CONFIGMAP_NAME" -n "$NAMESPACE" -o jsonpath='{.data.epp}' > "$tmp"
  python3 -I - "$tmp" "$1" << 'PYEOF'
import sys, re
path, group = sys.argv[1], sys.argv[2]
text = open(path).read()
m = re.search(r'\{\s*name:\s*' + re.escape(group) + r',\s*weight:\s*([0-9.]+)', text)
if not m:
    m = re.search(r'defaultGroup:\s*\{\s*name:\s*' + re.escape(group) + r',\s*weight:\s*([0-9.]+)', text)
if not m:
    sys.exit(f"group {group}: weight entry not found in maas-epp-config's data.epp")
print(m.group(1))
PYEOF
}

patch_epp_text_key() {
  # $1=src $2=dst $3=key $4=value. Generalizes the pre-UNI-180
  # flip_enforce_value to any scalar key, not just `enforce`.
  python3 -I - "$1" "$2" "$3" "$4" << 'PYEOF'
import sys, re
src, dst, key, val = sys.argv[1:5]
text = open(src).read()
pat = re.compile(r'(^[ \t]*' + re.escape(key) + r':[ \t]*)\S.*$', re.MULTILINE)
new, n = pat.subn(lambda m: m.group(1) + val, text, count=1)
if n == 0:
    sys.exit(f"{key}: key not found in maas-epp-config's data.epp")
open(dst, "w").write(new)
PYEOF
}

patch_epp_text_weight() {
  # $1=src $2=dst $3=group-name $4=new-weight
  python3 -I - "$1" "$2" "$3" "$4" << 'PYEOF'
import sys, re
src, dst, group, val = sys.argv[1:5]
text = open(src).read()
pat = re.compile(r'(\{\s*name:\s*' + re.escape(group) + r',\s*weight:\s*)[0-9.]+')
new, n = pat.subn(lambda m: m.group(1) + val, text, count=1)
if n == 0:
    pat2 = re.compile(r'(defaultGroup:\s*\{\s*name:\s*' + re.escape(group) + r',\s*weight:\s*)[0-9.]+')
    new, n = pat2.subn(lambda m: m.group(1) + val, text, count=1)
if n == 0:
    sys.exit(f"group {group}: weight entry not found in maas-epp-config's data.epp")
open(dst, "w").write(new)
PYEOF
}

# $1 = target spec. Prints the CURRENT scalar value named by the spec --
# never a whole resource body, so before/applied/current are always
# comparable like-for-like regardless of target kind.
live_config_read() {
  local spec="$1" kind="${1%%:*}" rest="${1#*:}" res name path
  case "$kind" in
    epp-key) extract_epp_key "$rest" ;;
    epp-weight) extract_epp_weight "$rest" ;;
    field)
      IFS=: read -r res name path <<<"$rest"
      $OC get "$res" "$name" -n "$NAMESPACE" -o jsonpath="{.${path}}"
      ;;
    *)
      echo "live_config_read: unknown target kind '$kind' in spec '$spec'" >&2
      return 1
      ;;
  esac
}

# $1 = target spec, $2 = new value. Applies it; does no before/after
# bookkeeping of its own -- live_config_set/live_config_restore own that.
live_config_apply() {
  local spec="$1" new_value="$2" kind="${1%%:*}" rest="${1#*:}" dir res name path patch_file
  dir="$(live_config_dir)"
  case "$kind" in
    epp-key)
      $OC get configmap "$CONFIGMAP_NAME" -n "$NAMESPACE" -o jsonpath='{.data.epp}' > "$dir/.scratch-src.yaml"
      patch_epp_text_key "$dir/.scratch-src.yaml" "$dir/.scratch-dst.yaml" "$rest" "$new_value"
      patch_configmap_epp "$dir/.scratch-dst.yaml"
      ;;
    epp-weight)
      $OC get configmap "$CONFIGMAP_NAME" -n "$NAMESPACE" -o jsonpath='{.data.epp}' > "$dir/.scratch-src.yaml"
      patch_epp_text_weight "$dir/.scratch-src.yaml" "$dir/.scratch-dst.yaml" "$rest" "$new_value"
      patch_configmap_epp "$dir/.scratch-dst.yaml"
      ;;
    field)
      IFS=: read -r res name path <<<"$rest"
      patch_file="$dir/.scratch-field-patch.json"
      python3 -I - "$path" "$new_value" "$patch_file" << 'PYEOF'
import sys, json
path, value, out = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    value = json.loads(value)
except (json.JSONDecodeError, ValueError):
    pass
body = value
for key in reversed(path.split(".")):
    body = {key: body}
json.dump(body, open(out, "w"))
PYEOF
      $OC patch "$res" "$name" -n "$NAMESPACE" --type=merge --patch-file="$patch_file" >/dev/null
      ;;
    *)
      echo "live_config_apply: unknown target kind '$kind' in spec '$spec'" >&2
      return 1
      ;;
  esac
}

# $1=id $2=target-spec $3=new-value. Records the pre-change value, applies
# the change, and remembers both (plus the spec) under $id so
# live_config_restore can put it back later from anywhere -- the explicit
# post-run call, the chaos-loop subshell (for a held field: target), or the
# on_exit trap.
live_config_set() {
  local id="$1" spec="$2" new_value="$3" dir before
  dir="$(live_config_dir)"
  before="$(live_config_read "$spec")"
  printf '%s' "$before" > "$dir/$id.before"
  printf '%s' "$spec" > "$dir/$id.spec"
  live_config_apply "$spec" "$new_value"
  printf '%s' "$new_value" > "$dir/$id.applied"
  live_config_log "set $id ($spec): ${before:0:80} -> $new_value"
}

# $1=id. No-op if $id was never set (no .before file) -- the common case for
# every id this script knows about when its matching env var is unset. Also
# a no-op, but NOT an error, if the live value no longer matches what this
# wrapper last applied for $id: that means an earlier restore (explicit call,
# chaos-loop hold, or trap) already happened, and reverting again would
# clobber whatever is live now. Either way, (re)writes the id's post-restore
# `oc get` proof -- the one the edge-case series' "leave the cluster as you
# found it" rule asks for -- so a case's closing comment can cite a file
# instead of re-deriving the state by hand.
live_config_restore() {
  local id="$1" dir spec before applied current
  dir="$(live_config_dir)"
  [ -f "$dir/$id.before" ] || return 0
  spec="$(cat "$dir/$id.spec")"
  before="$(cat "$dir/$id.before")"
  applied="$(cat "$dir/$id.applied")"
  # A read failure (resource gone, API hiccup) is NOT the same as "already
  # restored" -- log it distinctly rather than letting it fall through to the
  # generic "nothing to do" branch below as an empty string that happens not
  # to match $applied.
  if ! current="$(live_config_read "$spec" 2>/dev/null)"; then
    live_config_log "restore $id ($spec): could not read the current live value -- not re-patching blind; treating as already-restored or gone"
    current=""
  fi
  if [ "$current" = "$applied" ]; then
    live_config_apply "$spec" "$before"
    live_config_log "restored $id ($spec) -> ${before:0:80}"
  else
    live_config_log "restore $id ($spec): already at ${current:0:80}, nothing to do"
  fi
  live_config_proof "$id" "$spec"
}

# $1=id $2=target spec. `oc get -o yaml` on whatever resource that spec
# names, written once per id.
live_config_proof() {
  local id="$1" spec="$2" dir kind="${2%%:*}" rest="${2#*:}" res name
  dir="$(live_config_dir)"
  case "$kind" in
    epp-key|epp-weight) res="configmap"; name="$CONFIGMAP_NAME" ;;
    field) IFS=: read -r res name _ <<<"$rest" ;;
  esac
  $OC get "$res" "$name" -n "$NAMESPACE" -o yaml > "$dir/$id.post-restore.yaml" 2>&1 || true
}

# Only a `field:` target is safe to restore WHILE the Job is still running --
# see the LIVE_SET_HOLD note in the header comment above.
live_set_restore_at_hold() {
  case "$LIVE_SET_TARGET" in
    field:*) return 0 ;;
    *) return 1 ;;
  esac
}

# UNI-163: does applying $1 (a LIVE_SET_TARGET spec) edit $CONFIGMAP_NAME's
# data.epp? That ConfigMap has no live-reload path (same hazard documented on
# revert_enforce_live below), so the controller recreates the EPP pod under a
# new name every time -- epp-key:/epp-weight: always, and a field: target only
# if it happens to point at this same ConfigMap's epp key (e.g. a blob
# replacement used to change more than one epp-weight atomically in a single
# patch). Every prior LIVE_SET_AT case (C2, C5 -- see
# [[project_llmisvc_patch_path_works_and_edge_case_series]]) used an
# epp-key/epp-weight target applied before traffic started or restored only
# after it stopped, so chaos_loop firing this mid-run with capture_loop still
# attached was never actually exercised until UNI-163 (F6) first did. Used by
# chaos_loop below to decide whether to kick off resolve_replacement_pod_async
# the same way CHAOS_EPP_DELETE_AT already does -- without it, capture_loop and
# the mid-run restart detector silently keep watching the pod that is about to
# be gone, exactly the bug UNI-193 fixed for the chaos-delete path.
live_set_target_recreates_pod() {
  case "$1" in
    epp-key:*|epp-weight:*) return 0 ;;
    "field:configmap:$CONFIGMAP_NAME:"*) return 0 ;;
    *) return 1 ;;
  esac
}

revert_enforce_live() {
  # Idempotent and self-contained: safe to call more than once (the explicit
  # post-run call below, and again from the trap as a backstop) and safe to
  # call even if the flip never happened (ENFORCE_FLIPPED stays "false").
  # ENFORCE_FLIPPED guards WHETHER this run owns the revert at all (a run
  # that found enforce already true never flips it and must not touch it);
  # live_config_restore's own current-vs-applied check guards against
  # double-reverting once this run does own it.
  [ "$ENFORCE_FLIPPED" = "true" ] || return 0
  live_config_restore enforce-live
  # Best-effort verification: log it either way, but never let a slow/dead
  # EPP keep a dying script from actually exiting.
  wait_for_enforcing "0" || true
  ENFORCE_FLIPPED="false"
}

revert_shadow_mode() {
  # UNI-159: mirror of revert_enforce_live, opposite direction. Same
  # SHADOW_FLIPPED/live_config_restore idempotency split as that function --
  # see its comment above.
  [ "$SHADOW_FLIPPED" = "true" ] || return 0
  live_config_restore shadow-mode
  wait_for_enforcing "1" || true
  SHADOW_FLIPPED="false"
}

restore_chaos_scale() {
  [ -n "$CHAOS_SCALE_AT" ] || return 0
  live_config_restore chaos-scale
}

restore_live_set() {
  # Deliberately NOT called until after the final metrics snapshot (see the
  # explicit post-run call site below) -- an epp-key/epp-weight LIVE_SET_AT
  # target recreates the EPP pod on restore exactly like ENFORCE_LIVE's own
  # revert does, so reverting any earlier would zero the run's fairness
  # counters before they are read, same hazard UNI-143 (B4) found for
  # ENFORCE_LIVE. A `field:` target with LIVE_SET_HOLD set has usually
  # already been restored by the chaos loop by this point; this call is then
  # just the idempotent backstop, same as restore_chaos_scale.
  [ -n "$LIVE_SET_AT" ] || return 0
  live_config_restore live-set
}

stop_background_loops() {
  kill "$CAPTURE_PID" "$(cat "$CAPTURE_OC_PIDFILE" 2>/dev/null)" "$EVENTS_PID" "$TS_PID" "$CHAOS_PID" 2>/dev/null || true
  wait "$CAPTURE_PID" "$EVENTS_PID" "$TS_PID" "$CHAOS_PID" 2>/dev/null || true
}

# UNI-174: the single, unconditional owner of every piece of live cluster
# state this run can leave behind. Registered now, before the first mutating
# `oc` call below, and NEVER cleared (no `trap - EXIT` anywhere in this
# script anymore) -- it stays armed through Job polling, log/metrics
# collection, and report generation alike, so none of that ~100-line
# post-processing tail runs without a safety net. Each piece it restores
# (stop_background_loops, restore_chaos_scale, restore_live_set,
# revert_enforce_live, revert_shadow_mode -- UNI-159) is idempotent and
# checks live cluster state before acting, so calling this again at actual
# process exit after the explicit mid-script call below (see "Stop capture/
# timeseries/chaos" further down) is always a safe no-op, not a
# double-revert. SIGKILL (-9) cannot be trapped by this or any process, so a
# `kill -9` or an OOM-kill still leaves the cluster enforcing (or whatever
# LIVE_SET_AT/SHADOW_MODE last touched) with no automatic recovery -- that
# gap is real and is not closed by anything below.
on_exit() {
  stop_background_loops
  restore_chaos_scale
  restore_live_set
  revert_enforce_live
  revert_shadow_mode
}
trap on_exit EXIT
# A trap registered on INT/TERM/HUP alone only RUNS its command when the
# signal arrives -- unlike letting the signal's default disposition kill the
# process, bash does NOT terminate on its own afterward, so a handler that
# just called on_exit here would clean up correctly and then silently resume
# running the rest of the script (confirmed live during this ticket's own
# kill-test: the first attempt kept polling the Job for a full minute after
# SIGTERM). `exit` inside the handler is what actually ends the process; that
# in turn fires the EXIT trap above, so on_exit still runs exactly once per
# signal, not zero and not twice.
trap 'exit 1' INT TERM HUP

# Per-tenant timeline (START/STOP/DUTY), passed straight through to the
# loadgen Job when set -- see deploy/poc/04-loadgen.yaml's tenant_active() for
# what they mean. Unset (the default) reproduces the one, prior behaviour:
# every offered tenant active for the whole run.
TIMELINE_VARS="APP1_START APP1_STOP APP1_DUTY APP2_START APP2_STOP APP2_DUTY END_USERS_START END_USERS_STOP END_USERS_DUTY"

# UNI-128: per-request shape profile knobs, passed straight through to the
# Job when set -- see deploy/poc/04-loadgen.yaml's send_one()/pick_prompt()/
# pick_max_tokens() for what each one means. Unset (the default for every
# scenario above) reproduces the one, prior request shape: a fixed
# 1200-word prompt, max_tokens=64, no streaming, no client aborts, no
# oversized prompts.
PROFILE_VARS="PROMPT_WORDS_MIN PROMPT_WORDS_MAX MAX_TOKENS_DEFAULT MAX_TOKENS_OMIT_FRACTION MAX_TOKENS_HUGE_FRACTION MAX_TOKENS_HUGE_VALUE STREAM_FRACTION ABORT_FRACTION ABORT_MIN_FRACTION ABORT_MAX_FRACTION OVERSIZED_FRACTION OVERSIZED_PROMPT_WORDS LONG_GEN_FRACTION LONG_GEN_MAX_TOKENS REQUEST_TIMEOUT_SECONDS"

# UNI-129: identity-variant knobs (D1/D2/D3), passed straight through to the
# Job when set -- see deploy/poc/04-loadgen.yaml's tenant dispatch and
# send_one() for what each one means. Unset (the default for every scenario
# above) reproduces the one, prior identity shape: two end-user keys, no
# custom tenant, no forged header.
IDENTITY_VARS="END_USERS_KEYS FORGE_FAIRNESS_ID_FRACTION FORGE_FAIRNESS_ID_VALUE CUSTOM_SUBSCRIPTION_NAME WORKERS_CUSTOM CUSTOM_START CUSTOM_STOP CUSTOM_DUTY"

# UNI-103: is this scenario scored, or a named negative control that is
# expected not to show the weighted split? Read by the report step below --
# a control still runs for real and still produces a report, it just isn't
# held to the symmetric PASS/FAIL threshold or counted in this script's exit
# code.
IS_CONTROL="false"

case "$SCENARIO" in
  full-contention)
    # Sized from A4 Run 3 (docs/poc-results.md, UNI-29), the first config on
    # this backend/model (llama-3-1-8b) that put every tenant above its
    # entitlement and reproduced the weight ordering end-users > app1 > app2.
    #
    # UNI-212: since UNI-211 raised maas-saturation's queueDepthThreshold
    # from 5 to 150 (calibrated against this backend's genuine steady-state
    # vLLM-side queue depth), this sizing's 192 total offered workers no
    # longer backs up llm_d_epp_flow_control_request_queue_duration_seconds
    # at all -- every request is admitted immediately (confirmed live,
    # 2026-11-09: p50/p99 queue wait 0ms in every 10s window of a 240s run,
    # despite 16.8s end-to-end latency, and contended_seconds_total/
    # contended_service_tokens_total never incremented -- UNCONTENDED, not a
    # metrics bug: see docs/poc-results.md "UNI-212"). The bottleneck moved
    # entirely inside vLLM's own request queue, which this EPP's
    # weighted-fairness policy cannot see or influence, so this sizing can no
    # longer exercise that policy. Use full-contention-2x below for any
    # re-run that needs genuine EPP-level contention post-UNI-211.
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=32 WORKERS_APP2=32 WORKERS_END_USERS=128)
    ;;
  full-contention-discriminating)
    # UNI-225: full-contention's own 1:1:4 worker ratio (16.7/16.7/66.7%)
    # sits only 6.1 points from this scenario's 21.1/10.5/68.4% weight
    # share -- under the 10-point threshold, so a PASS there cannot tell
    # "the split follows the weights" apart from "the split follows the
    # workers" (see the module's own UNI-225 finding and
    # 15-fairness-report.py's worker_vs_weight_gap_pts). This variant keeps
    # end-users -- the dominant, already-proven-sufficient tenant -- at its
    # unchanged 128 workers (never reduce the group that needs the most
    # concurrency to stay backlogged; docs/runbook.md "Per-tenant worker
    # sizing and the saturation check") and instead boosts BOTH minority
    # tenants 4x past their own already-over-offering 32 baseline, to 128
    # each. Over-offering a tenant further is always safe -- the existing
    # 32-worker baseline already over-offers app1/app2's 20%/10% shares
    # without breaking anything -- so this cannot introduce a new
    # saturation-floor artifact, only a larger worker-share-vs-weight-share
    # gap: all three tenants now offer an EQUAL 128 workers (33.3% each)
    # against the unchanged 21.1/10.5/68.4% weight target, a 35.1-point gap.
    # Keep full-contention itself running too -- this is a sibling, not a
    # replacement (UNI-225 asks for at least one discriminating sizing per
    # scenario, not a removal of the proportional one).
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=128 WORKERS_APP2=128 WORKERS_END_USERS=128)
    ;;
  full-contention-2x)
    # UNI-212: full-contention's own 1:1:4 ratio, offered workers doubled
    # (64/64/256, 384 total) to clear UNI-211's new queueDepthThreshold=150
    # and reproduce genuine EPP-level FlowControl backlog again -- see the
    # full-contention case above for why the un-scaled sizing stopped
    # working. 384 total is close to app1-flood's already-confirmed-working
    # 352 (256+32+64).
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=64 WORKERS_APP2=64 WORKERS_END_USERS=256)
    ;;
  full-contention-2x-discriminating)
    # UNI-225: same confounding as full-contention-discriminating above
    # (6.1-point gap, under the 10-point bar), same fix -- keep end-users at
    # its proven-sufficient 256 workers, boost both minority tenants 4x past
    # their own 64-worker baseline to 256 each, so all three offer an EQUAL
    # 256 workers (33.3% each) against the unchanged 21.1/10.5/68.4% weight
    # target (same 35.1-point gap as the 1x variant). 768 total offered
    # workers is double full-contention-discriminating's 384, the same
    # doubling relationship full-contention/full-contention-2x themselves
    # already have (192 -> 384) -- not a new scale this backend hasn't
    # already run load at (full-contention-2x's own 384 already passed).
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=256 WORKERS_APP2=256 WORKERS_END_USERS=256)
    ;;
  end-users-idle)
    # app1 is the higher-share tenant once end-users is excluded (66.7% vs
    # app2's 33.3%), so it needs to over-offer relative to app2 for the same
    # reason end-users over-offers relative to app1/app2 in full-contention
    # above -- see docs/runbook.md "Per-tenant worker sizing and the
    # saturation check". UNI-104: the 4:1 ratio copied from full-contention's
    # end-users overshot (82.4% vs a 66.7% target); try a ratio closer to the
    # actual 2:1 app1:app2 target instead.
    TENANTS="app1 app2"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=64 WORKERS_APP2=32)
    ;;
  end-users-idle-discriminating)
    # UNI-225: end-users-idle's own worker ratio (66.7/33.3%) is an exact
    # copy of its 20:10 weight ratio (0.0-point gap) -- "the split follows
    # the weights" and "the split follows the workers" predict the identical
    # number here, so its PASS is not evidence for weighted fairness
    # specifically. Keep app1 -- the dominant, already-proven-sufficient
    # tenant once end-users is excluded -- at its unchanged 64 workers, and
    # boost app2 4x past its own already-over-offering 32-worker baseline to
    # 128, the same boost factor and same "never reduce the dominant
    # tenant's proven sizing" rule full-contention-discriminating uses
    # above. New worker share is 33.3/66.7% -- app2 now offers MORE workers
    # than app1 despite having half app1's weight -- against an unchanged
    # 66.7/33.3% weight target: a 33.4-point gap.
    TENANTS="app1 app2"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=64 WORKERS_APP2=128)
    ;;
  equal-workers-control)
    # UNI-103: the ORIGINAL full-contention shape (equal WORKERS for every
    # tenant), kept on purpose as a named negative control -- it is expected
    # to compress toward equal thirds on this backend (work conservation
    # draining end-users' queue, the same mechanism docs/poc-results.md's
    # "detour" section documents), not to show 20/10/65. See
    # docs/runbook.md for why this is scored INFO, not PASS/FAIL.
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=()
    IS_CONTROL="true"
    ;;
  app1-alone)
    TENANTS="app1"
    PER_TENANT_OVERRIDES=()
    ;;
  app2-alone)
    # UNI-131: mirror of app1-alone for the lowest-weight tenant. Same
    # default WORKERS (32, the "usual over-offering" count every solo
    # scenario uses), no per-tenant override needed with only one tenant
    # offered.
    TENANTS="app2"
    PER_TENANT_OVERRIDES=()
    ;;
  app2-idle)
    # UNI-132: promotes the by-hand "S3" check (docs/poc-results.md,
    # "Scenario matrix") into the automated benchmark. app2 is excluded, so
    # the pair's renormalized target is 20/(20+65)=23.5% / 65/(20+65)=76.5%.
    # Per the UNI-104 lesson, the offered-worker ratio is sized to match that
    # target ratio (20:65) directly rather than copying full-contention's or
    # end-users-idle's ratio: app1 anchored at the usual 32, end-users scaled
    # to 32*(65/20)=104.
    TENANTS="app1 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=32 WORKERS_END_USERS=104)
    ;;
  app2-idle-discriminating)
    # UNI-225: app2-idle's worker ratio (32:104) is sized to match its 20:65
    # weight ratio exactly -- the pair's worker share (23.5/76.5%) and
    # weight share (23.5/76.5%) are identical, a 0.0-point gap, so a PASS
    # here cannot distinguish "follows the weights" from "follows the
    # workers." Keep end-users -- the dominant, already-proven-sufficient
    # tenant -- at its unchanged 104 workers, and boost app1 4x past its own
    # already-over-offering 32-worker baseline to 128, same rule and boost
    # factor as the other UNI-225 variants above. New worker share is
    # 55.2/44.8% against the unchanged 23.5/76.5% weight target: a
    # 31.7-point gap.
    TENANTS="app1 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=128 WORKERS_END_USERS=104)
    ;;
  app1-idle)
    # UNI-133: A4 in the same series as app2-alone (A1, UNI-131) and app2-idle
    # (A3, UNI-132). app1 is excluded, so the pair's renormalized target is
    # 10/(10+65)=13.3% / 65/(10+65)=86.7% -- the most extreme ratio (6.5:1) of
    # the three possible pairs. Same UNI-104 sizing lesson as app2-idle: anchor
    # the smaller weight (app2) at the usual 32, scale the larger (end-users)
    # to match the ratio exactly: 32*(65/10)=208.
    TENANTS="app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP2=32 WORKERS_END_USERS=208)
    ;;
  app1-idle-discriminating)
    # UNI-225: app1-idle's worker ratio (32:208) is sized to match its 10:65
    # weight ratio exactly (0.0-point gap), same confound as app2-idle
    # above. Keep end-users at its unchanged, proven-sufficient 208 workers,
    # boost app2 4x past its own 32-worker baseline to 128. New worker share
    # is 38.1/61.9% against the unchanged 13.3/86.7% weight target: a
    # 24.8-point gap.
    TENANTS="app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP2=128 WORKERS_END_USERS=208)
    ;;
  app2-trickle)
    # UNI-134: A5, promoting the by-hand "S2"/"S4" checks (docs/poc-results.md
    # "Scenario matrix") into the benchmark. Unlike app2-idle/app1-idle, all
    # three tenants are offered here -- app2 is not excluded, it trickles at
    # the literal S2/S4 figure of 2 workers, well under its own weight
    # entitlement. app1/end-users are sized identically to app2-idle (32/104)
    # since the ratio BETWEEN them (20:65, renormalized 23.5/76.5) is
    # unaffected by app2's presence -- 15-fairness-report.py excludes app2
    # from the weight total used to score that pair, and scores app2 itself
    # on a dedicated "did it get served" check instead of the symmetric
    # deviation threshold (see the "app2-trickle" branch there).
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=32 WORKERS_APP2=2 WORKERS_END_USERS=104)
    ;;
  app2-trickle-discriminating)
    # UNI-225: the scored app1/end-users pair here is sized identically to
    # app2-idle's 32/104 (0.0-point gap), same confound. app2's own 2-worker
    # trickle is untouched -- it is scored on a dedicated "did it get
    # served" check (15-fairness-report.py's capped_groups path), not the
    # symmetric deviation threshold this variant targets, so there is
    # nothing to make discriminating there. Same fix as
    # app2-idle-discriminating: keep end-users at its proven-sufficient 104,
    # boost app1 4x to 128. 15-fairness-report.py's capped_groups exclusion
    # keys off the literal scenario name "app2-trickle", so this variant is
    # matched there explicitly rather than inferred from TENANTS.
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=128 WORKERS_APP2=2 WORKERS_END_USERS=104)
    ;;
  asymmetric-demand)
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=32 WORKERS_APP2=0 WORKERS_END_USERS=2)
    ;;
  below-capacity)
    # UNI-135: A6 "below capacity, everyone light" -- each tenant at ~20% of
    # full-contention's saturating per-tenant ceiling (32/32/128):
    # 32*0.2=6.4->6, 32*0.2=6.4->6, 128*0.2=25.6->26. All three offered, none
    # over its own entitlement, so nobody should ever be backlogged alongside
    # anyone else -- see 15-fairness-report.py's UNCONTENDED verdict.
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=6 WORKERS_APP2=6 WORKERS_END_USERS=26)
    ;;
  max-tokens-skew)
    # UNI-145: C2, "no max_tokens / huge max_tokens". Same app1/app2 pairing
    # and 64/32 worker sizing as end-users-idle -- already proven to
    # over-offer this exact 20:10 weight ratio -- with the new UNI-145
    # per-tenant knob forcing app1's requests to omit max_tokens entirely
    # (exercises the 512/per-group-EWMA fallback) and app2's to always send
    # a large-but-serveable max_tokens (exercises the min(max_tokens, ewma)
    # cap and over-charge truing on whichever side the provisional estimate
    # misses).
    #
    # MAX_TOKENS_HUGE_VALUE's own default (32000) is NOT usable here: this
    # cluster's real GPU backend is started with `--max-model-len 8192`
    # (deploy/poc/09-vllm-gpu.yaml), and vLLM 400s any request whose
    # prompt_tokens + max_tokens exceeds that -- confirmed live on
    # 2026-11-02, every app2 request got "400 Bad Request" with 32000, zero
    # completions. 4096 leaves ~4000 tokens of headroom under the 1200-word
    # default prompt (~1650 tokens at this plugin's own 4-bytes/token
    # estimate) and is still a large, over-offering cap relative to this
    # corpus's typical ~70-token completions (see docs/poc-results.md's C2
    # section), so the over-charge-truing mechanism this case exists to
    # exercise still fires.
    TENANTS="app1 app2"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=64 WORKERS_APP2=32 MAX_TOKENS_MODE_APP1=omit MAX_TOKENS_MODE_APP2=huge MAX_TOKENS_HUGE_VALUE=4096)
    ;;
  cache-heavy-vs-cache-cold)
    # UNI-136: C8. Same app1:app2 pairing and 64/32 sizing as end-users-idle
    # (the only existing scenario already proven to over-offer both sides of
    # this exact 20:10 weight ratio) -- the only new thing is each tenant's
    # cache-hit shape, not its worker count. See the header comment above for
    # the full rationale, including why this runs as a control.
    TENANTS="app1 app2"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=64 WORKERS_APP2=32 CACHE_SHAPE_APP1=hot CACHE_SHAPE_APP2=cold)
    IS_CONTROL="true"
    ;;
  asymmetric-request-shapes)
    # UNI-146: C1, "asymmetric request shapes -- split by weighted tokens,
    # not request count". Same app1/end-users pairing and 32/104 worker
    # sizing as app2-idle -- already proven to over-offer this exact 20:65
    # weight ratio -- with the "longgen" MAX_TOKENS_MODE_* value
    # (04-loadgen.yaml, this ticket) paired with the per-group
    # PROMPT_WORDS_MIN/MAX_<TOKEN> knob (GROUP_KNOBS, UNI-179) to give the
    # two tenants opposite request shapes: app1 sends this script's long,
    # 1200-word default prompt with a short (MAX_TOKENS_DEFAULT=64)
    # completion; end-users sends a short, fixed 30-word prompt with a long
    # (LONG_GEN_MAX_TOKENS) completion. Both over-offer the pool at these
    # worker counts regardless of per-request duration -- a closed-loop
    # worker that is mid-generation on a long completion is still occupying
    # a concurrent slot, which is exactly the backlog this benchmark needs.
    #
    # LONG_GEN_MAX_TOKENS=1500 (not the 2000 UNI-128 default, and nowhere
    # near C4/UNI-150's near-timeout target): just needs to be "long"
    # relative to app1's 64-token completions so the two cost models
    # (request count vs. weighted tokens) visibly disagree, same headroom
    # reasoning as UNI-145's MAX_TOKENS_HUGE_VALUE=4096 -- 1500 completion
    # tokens plus a 30-word (~40-token) prompt stays comfortably under this
    # cluster's real --max-model-len 8192, with REQUEST_TIMEOUT_SECONDS'
    # default 300s giving ample margin to actually finish generating it
    # under contention.
    TENANTS="app1 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=32 WORKERS_END_USERS=104 PROMPT_WORDS_MIN_END_USERS=30 PROMPT_WORDS_MAX_END_USERS=30 MAX_TOKENS_MODE_END_USERS=longgen LONG_GEN_MAX_TOKENS=1500)
    ;;
  near-timeout-long-generations)
    # UNI-150: C4, "long-running requests near the 600s timeout" -- the case
    # this chain's own runbook note (docs/runbook.md, "Long generations,
    # concretely") flagged as where LONG_GEN_MAX_TOKENS/REQUEST_TIMEOUT_SECONDS
    # sizing against the real backend finally gets pinned down. A first
    # attempt reused asymmetric-request-shapes' full 104-worker end-users
    # sizing with LONG_GEN_MAX_TOKENS scaled up to 4000 (discarded, not in
    # results/): 104 concurrent ~4000-token completions blew through this
    # backend's KV-cache capacity, producing a ~32%/~19% HTTP 500 rate on
    # app1/end-users respectively (resource exhaustion, not a timeout
    # artifact) and pinning p95 latency at the REQUEST_TIMEOUT_SECONDS=650
    # client-side cutoff rather than a real completion time.
    #
    # This case keeps full-contention's proven app1/app2 sizing (32/32, real
    # short-request background contention for the whole run). A second
    # attempt at WORKERS_END_USERS=8 (also discarded, not in results/) swung
    # the other way: with only 8 concurrent long-gen sequences, this
    # backend's decode throughput per sequence is fast enough (~80
    # tokens/sec) that even LONG_GEN_MAX_TOKENS=4000 finished in ~51s median
    # -- nowhere near 5-9 minutes, and the model's 8192-token context window
    # rules out reaching that target by raising the token count alone at
    # this concurrency (8150 max completion tokens / 80 tok/s =~ 102s).
    # Generation wall-clock time on this backend is governed by how many
    # concurrent long-gen sequences dilute the shared decode budget, not by
    # token count in isolation: 104 workers measured 5.6x slower per
    # sequence than 8 workers at the same token target (280s vs 51s for
    # 4000 tokens) but also pushed KV-cache usage into the regime that
    # produced the first attempt's HTTP 500s. WORKERS_END_USERS=48 is the
    # empirical middle point this ticket settled on: enough concurrent
    # long-gen sequences to meaningfully dilute decode throughput toward the
    # 5-9 minute band, while staying under half of the 104-worker count that
    # produced resource-exhaustion errors.
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=32 WORKERS_APP2=32 WORKERS_END_USERS=48 PROMPT_WORDS_MIN_END_USERS=30 PROMPT_WORDS_MAX_END_USERS=30 MAX_TOKENS_MODE_END_USERS=longgen)
    ;;
  misclassified-prefix)
    # UNI-153: D2, scored run of the edge-case plan's "misclassified
    # prefix" case. UNI-129 built the `custom` pseudo-tenant mechanism and
    # already smoke-tested this exact identity ad hoc (25s/2-worker Job,
    # 70/70 200s, unmatched_subscriptions_total 0->70 -- see
    # docs/runbook.md "D2, resolved"); this scenario promotes that into a
    # proper scored benchmark run instead of a one-off Job. Background
    # contention is full-contention's own proven sizing (app1/app2/
    # end-users, 32/32/128) so the claim is demonstrated under real
    # multi-tenant load, not in isolation, and so the run doubles as
    # evidence the misclassified traffic doesn't disturb the other three
    # groups' weighted split either. `custom` is pinned to
    # CUSTOM_SUBSCRIPTION_NAME=enduser-foo -- no hyphen after "end," so it
    # deliberately misses both the end-user- prefix match and the two
    # apps' exact-name match, and free-rides the unclassified catch-all
    # (weight 5). WORKERS_CUSTOM=8 is a light closed-loop trickle: this
    # case is about WHERE the traffic is classified, not about saturating
    # the custom tenant's own throughput, so it does not need
    # full-contention's over-offering discipline.
    TENANTS="app1 app2 end-users custom"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=32 WORKERS_APP2=32 WORKERS_END_USERS=128 WORKERS_CUSTOM=8 CUSTOM_SUBSCRIPTION_NAME=enduser-foo)
    ;;
  shadow-mode-control)
    # UNI-159: F1, the second named negative control in this series (the
    # first is equal-workers-control, UNI-103). Same TENANTS/PER_TENANT_OVERRIDES
    # as full-contention -- the per-tenant over-offering discipline is kept
    # exactly as-is, because the thing being tested here is NOT whether the
    # offered load saturates the pool (it already does, full-contention
    # proved that), it's whether the weighted split still shows up once
    # nothing is left to enforce it. SHADOW_MODE="true" makes this scenario
    # own its own live-config flip end to end (set up, confirm, restore) --
    # see the UNI-159 header comment and SHADOW_MODE's declaration above for
    # the mechanism. IS_CONTROL="true" for the same reason
    # equal-workers-control sets it: a large deviation from the configured
    # weights is the expected, correct result here, not a policy failure.
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=32 WORKERS_APP2=32 WORKERS_END_USERS=128)
    IS_CONTROL="true"
    SHADOW_MODE="true"
    ;;
  app1-flood)
    # UNI-161: board case, 30/10/60 (end-users standing in for "app3"), app1
    # flooding far harder than the other two -- see the header comment above
    # for the full sizing rationale. This scenario does NOT touch
    # maas-epp-config's weights itself (unlike shadow-mode-control's `enforce`
    # self-ownership) -- the operator patches the three group weights to
    # 30/10/60 before invoking this scenario, the same division of labor
    # UNI-160/F3 used for its own alternative weight sets, so this case block
    # only owns the per-tenant worker sizing.
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=256 WORKERS_APP2=32 WORKERS_END_USERS=64)
    ;;
  app1-flood-moderate)
    # UNI-161: "watch for" follow-up -- if app1-flood's 256 workers overshoot
    # its 30% weight (the UNI-104 pattern), this halves app1's worker count to
    # locate where the overshoot starts easing, holding app2/end-users and the
    # 30/10/60 weights fixed so app1's own sizing is the only variable.
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=128 WORKERS_APP2=32 WORKERS_END_USERS=64)
    ;;
  app1-flood-light)
    # UNI-161: second "watch for" follow-up -- app1 worker count brought down
    # to full-contention's own usual 32 (still over-offering its 30% weight,
    # just not by 8x), the other end of the bracket from app1-flood's 256.
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=32 WORKERS_APP2=32 WORKERS_END_USERS=64)
    ;;
  app3-joins-at-saturation)
    # UNI-164: board case, 30/10/60 (end-users standing in for "app3", same
    # substitution UNI-161 used -- see that ticket's writeup and
    # [[project_ngroup_support_stops_at_the_loadgen]] for why a real app3
    # group/MaaSSubscription is out of reach under rule 5). Unlike
    # app1-flood*, app1 and app2 are NOT flooding here -- the ticket wants a
    # clean, trackable two-tenant 75/25 (30:10 = 3:1) split BEFORE end-users
    # joins, so worker counts are sized to that 3:1 ratio (mirroring how
    # end-users-idle's 64:32 tracks its own 2:1 weight ratio) rather than
    # reused from any app1-flood* run, which deliberately over-offers app1
    # far past its weight.  WORKERS_END_USERS=128 reuses full-contention's
    # own dominant-tenant sizing, since weight 60 here is close to
    # full-contention's 65. This scenario does NOT touch maas-epp-config's
    # weights or own the join timing itself -- same division of labor as
    # app1-flood: the operator patches weights to 30/10/60 before the run and
    # restores 20/10/65 after, and invokes this scenario with
    # END_USERS_START=<join offset> (a TIMELINE_VARS knob, see the header
    # comment above) so end-users is silent until the join instant while
    # app1/app2 run for the whole DURATION.
    TENANTS="app1 app2 end-users"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=96 WORKERS_APP2=32 WORKERS_END_USERS=128)
    ;;
  six-group-board-case)
    # UNI-165: board case, app1..app6. Unlike UNI-161/164, these are real
    # MaaSSubscriptions as of UNI-187 (ConfigMap/loadgen tables)/UNI-189
    # (subscriptions+keys applied) -- no end-users substitution needed.
    #
    # This single scenario runs against FOUR different weight sets (equal,
    # graded 40/20/15/10/10/5, dominant 90/2/2/2/2/2, pow2 32/16/8/4/2/1) plus
    # a subset run, in one ticket. A flat worker count that over-offers one
    # weight set would under-offer another -- the app1-flood "watch for"
    # lesson (UNI-161) -- so this block owns NO fixed sizing at all. Every
    # per-group count is the caller's WORKERS_APPn env var, chosen to track
    # whichever weight set maas-epp-config currently holds (same
    # operator-owns-the-ConfigMap division of labor as app1-flood/
    # app3-joins-at-saturation -- this block never touches the ConfigMap).
    # Idling a group for the subset run is WORKERS_APPn=0, not removing it
    # from TENANTS, so it stays on the client-side ledger as an offered-zero
    # group rather than silently dropping out of the report.
    TENANTS="app1 app2 app3 app4 app5 app6"
    PER_TENANT_OVERRIDES=(
      WORKERS_APP1="${WORKERS_APP1:?six-group-board-case requires WORKERS_APP1..APP6}"
      WORKERS_APP2="${WORKERS_APP2:?six-group-board-case requires WORKERS_APP1..APP6}"
    )
    ;;
  uni165-equal-discriminating)
    # UNI-228: six-group-board-case's `equal` weight set (16.7% each) was run
    # with all six groups floored to the same 32-worker baseline (worker
    # share == weight share, 0.0pt gap, docs/poc-results.md's UNI-165
    # section) -- an equal split predicted by the weights and an equal split
    # predicted by the workers are the same split, so a PASS there is not
    # evidence for weighted fairness specifically (the same UNI-225 confound,
    # just with an equal rather than unequal weight set). Unlike the UNI-225
    # siblings, there is no "dominant" tenant to hold fixed by weight here --
    # every weight share is identical -- so this applies the same "boost past
    # an already-proven-sufficient baseline, never reduce it" rule to
    # ONE arbitrarily chosen group (app1) instead: app2-6 stay at the
    # unchanged, already-over-offering 32-worker baseline, app1 is boosted 4x
    # to 128, the same boost factor UNI-225's siblings use. New worker share
    # is 44.4% (app1) / 11.1% each (app2-6) against the unchanged 16.7% each
    # weight target -- a 27.7-point gap, comfortably clear of the 10-point
    # bar. This is the equal-weight mirror image of
    # `full-contention-discriminating` (equal workers against unequal
    # weights there; unequal workers against equal weights here).
    #
    # app1/app2 have a pre-existing commented-out placeholder in
    # 04-loadgen.yaml (set_override's "active or commented" regex), so they
    # go through PER_TENANT_OVERRIDES like every other scenario above. app3-6
    # do not -- same as six-group-board-case, they only reach the Job spec
    # via the later UNI-179 generic per-group pass-through loop, which reads
    # them as plain env vars already present when that loop runs, not
    # through PER_TENANT_OVERRIDES's own set_override call (confirmed the
    # hard way: putting them in PER_TENANT_OVERRIDES fails with "override
    # target not found" because GROUP_VAR_PREFIXES, which the UNI-179
    # fallback needs, is not built yet at that point in the script).
    TENANTS="app1 app2 app3 app4 app5 app6"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=128 WORKERS_APP2=32)
    WORKERS_APP3=32 WORKERS_APP4=32 WORKERS_APP5=32 WORKERS_APP6=32
    ;;
  uni165-graded-discriminating)
    # UNI-228: six-group-board-case's `graded` weight set (40/20/15/10/10/5)
    # used the same 2-point linear-fit sizing (20%->32, 65%->128, floored at
    # 32 below 20%) as `equal`/`dominant`/`pow2` -- app1(40%)=75,
    # app2(20%)=32, app3-6(15/10/10/5%, all <20%)=32 each -- which tracks the
    # weight ratio closely enough (0.0-8.6pt per the UNI-225 review finding)
    # that it cannot discriminate either. Same fix as the `equal` sibling
    # above: keep app1 -- the one group already sized past the fit's floor,
    # and the dominant weight here -- at its unchanged 75 workers, and boost
    # the smallest-weight group (app6, 5%) 4x past its own 32-worker floor to
    # 128. New worker share is app1 22.7% (vs 40.0% weight, -17.3pt) and app6
    # 38.7% (vs 5.0% weight, +33.7pt) -- both clear of the 10-point bar, the
    # larger taken for the scenario's own max-gap scoring
    # (worker_vs_weight_gap_pts in 15-fairness-report.py already takes the
    # max absolute gap across all offered groups, so no report-side change is
    # needed here). app3-5 are plain env vars for the same reason the `equal`
    # sibling above documents (no pre-existing PER_TENANT_OVERRIDES route for
    # app3+); app6 is boosted so it goes through the same mechanism too.
    TENANTS="app1 app2 app3 app4 app5 app6"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=75 WORKERS_APP2=32)
    WORKERS_APP3=32 WORKERS_APP4=32 WORKERS_APP5=32 WORKERS_APP6=128
    ;;
  uni165-subset-3-idle-discriminating)
    # UNI-228: `subset-3-idle` runs the `equal` weight table with app4/5/6
    # idled (WORKERS_APP{4,5,6}=0, kept in TENANTS so they stay on the
    # client-side ledger as offered-zero groups rather than silently
    # dropping out of the report -- see the six-group-board-case comment
    # above). The three active groups (app1/2/3) share the same confound as
    # `equal`: 32 workers each against an equal, renormalized 33.3% weight
    # share apiece, 0.0pt gap. Same fix: boost app1 4x to 128, keep app2/app3
    # at the unchanged 32-worker baseline, leave app4-6 idled at 0 (idle
    # groups are excluded from offered_groups entirely, so they do not
    # participate in the gap computation either way). New worker share is
    # 66.7% (app1) / 16.7% each (app2/app3) against the unchanged,
    # renormalized 33.3% each weight target -- a 33.4-point gap. app3 (active,
    # unchanged) and app4-6 (idled, unchanged) are plain env vars for the
    # same reason the `equal` sibling above documents.
    TENANTS="app1 app2 app3 app4 app5 app6"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=128 WORKERS_APP2=32)
    WORKERS_APP3=32 WORKERS_APP4=0 WORKERS_APP5=0 WORKERS_APP6=0
    ;;
  uni165-equal-2x-discriminating)
    # UNI-228: `equal-2x` doubled every group's worker count to 64 (the one
    # UNI-165-family `-2x` follow-up the sizing rule calls for), still an
    # equal split against an equal weight set -- 0.2pt gap, same confound.
    # Same fix, scaled: boost app1 4x past its own 64-worker baseline to 256,
    # keep app2-6 at the unchanged 64-worker baseline. Because the boost
    # factor is relative to each scenario's own baseline, the resulting gap
    # is identical to the 1x sibling's by construction -- 44.4% (app1) /
    # 11.1% each (app2-6) against 16.7% each, a 27.7-point gap -- the same
    # 1x->2x doubling relationship `full-contention`/`full-contention-2x`
    # and their own `-discriminating` siblings already have. app3-6 are plain
    # env vars for the same reason the `equal` sibling above documents.
    TENANTS="app1 app2 app3 app4 app5 app6"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=256 WORKERS_APP2=64)
    WORKERS_APP3=64 WORKERS_APP4=64 WORKERS_APP5=64 WORKERS_APP6=64
    ;;
  twenty-group-scale)
    # UNI-167: H3, scale -- 20 configured groups (app1..app20), extending
    # six-group-board-case's (UNI-165) multi-group tooling the same way that
    # scenario extended app1-flood's. app3..app20 are the real
    # MaaSSubscriptions UNI-187/189 already applied (no end-users
    # substitution). Only the `equal` weight table is rendered for 20 groups
    # (deploy/poc/epp-groups/render.py 20 -- no graded/dominant/pow2 variant
    # exists at this N), so unlike six-group-board-case this block owns a
    # fixed, equal sizing: every group is identical, so a single flat worker
    # count cannot over-offer one share while under-offering another the way
    # it would across unequal weights. 50 is comfortably above the 32-worker
    # count that already saturated six-group-board-case's larger 16.7% equal
    # share (UNI-165), and matches the exact count UNI-179's own loadgen-only
    # dry run used at this N (docs/runbook.md: "20 groups x 50 workers").
    # 20x50 = 1000, the ticket's own target. The EPP groups table is the
    # operator's responsibility, same division of labor as
    # six-group-board-case (render.py 20 | oc apply -f -- before this
    # scenario, restored to 00-config.yaml after) -- this block never touches
    # the ConfigMap.
    TENANTS="app1 app2 app3 app4 app5 app6 app7 app8 app9 app10 app11 app12 app13 app14 app15 app16 app17 app18 app19 app20"
    PER_TENANT_OVERRIDES=()
    WORKERS="${WORKERS:-50}"
    ;;
  twenty-group-scale-discriminating)
    # UNI-228: twenty-group-scale's flat 50-workers-per-group sizing against
    # its flat 5%-per-group equal weight table is a 0.0pt gap by
    # construction (every group gets an identical worker count AND an
    # identical weight, so there is no pair of numbers that could diverge) --
    # the one row in this family that cannot even be made marginally
    # confounded, it is non-discriminating by definition. Same fix as the
    # six-group `uni165-equal-discriminating` sibling: hold 19 of the 20
    # groups at the unchanged 50-worker baseline (WORKERS_APP2..APP20 fall
    # through to the scenario's own WORKERS="${WORKERS:-50}" default, exactly
    # as twenty-group-scale's own PER_TENANT_OVERRIDES=() relies on already)
    # and boost app1 past it. A plain 4x boost (to 200) only clears the
    # 10-point bar by 2.4pt (12.4pt gap) -- each baseline group here holds
    # just 5% weight instead of the six-group family's 16.7-40%, so the same
    # multiple buys far less separation once renormalized over 20 groups.
    # Boost 8x instead, to 400: new worker share is 29.6% (app1) / 3.7% each
    # (app2-20) against the unchanged 5.0% each weight target -- a 24.6-point
    # gap, back in line with this ticket's other four siblings (27.7-33.7pt).
    # 1350 total offered workers (950 + 400) is a new high for this suite,
    # but not a new order of magnitude -- `full-contention-2x-discriminating`
    # already ran 768, and this scenario's own 1x sizing already proved 1000
    # workers safe against this backend.
    TENANTS="app1 app2 app3 app4 app5 app6 app7 app8 app9 app10 app11 app12 app13 app14 app15 app16 app17 app18 app19 app20"
    PER_TENANT_OVERRIDES=(WORKERS_APP1=400)
    WORKERS="${WORKERS:-50}"
    ;;
  *)
    echo "unknown scenario: $SCENARIO (expected one of: full-contention full-contention-discriminating full-contention-2x full-contention-2x-discriminating end-users-idle end-users-idle-discriminating equal-workers-control app1-alone app2-alone app2-idle app2-idle-discriminating app1-idle app1-idle-discriminating app2-trickle app2-trickle-discriminating asymmetric-demand below-capacity cache-heavy-vs-cache-cold max-tokens-skew asymmetric-request-shapes near-timeout-long-generations misclassified-prefix shadow-mode-control app1-flood app1-flood-moderate app1-flood-light app3-joins-at-saturation six-group-board-case twenty-group-scale uni165-equal-discriminating uni165-graded-discriminating uni165-subset-3-idle-discriminating uni165-equal-2x-discriminating twenty-group-scale-discriminating)" >&2
    exit 1
    ;;
esac

if [ "$ENFORCE_LIVE" = "true" ] && [ "$SHADOW_MODE" = "true" ]; then
  # UNI-159: both flip the same maas-epp-config `enforce` key, to opposite
  # target values -- there is no combined outcome to converge on, and
  # whichever one's live_config_set ran second would just clobber the
  # other's .before/.applied bookkeeping for the same ConfigMap key.
  echo "[benchmark] FATAL: ENFORCE_LIVE=true and SHADOW_MODE=true both target maas-epp-config's enforce key in opposite directions -- set at most one" >&2
  exit 1
fi

echo "[benchmark] scenario: $SCENARIO  artifact dir: $ARTIFACT_DIR"

METRICS_BEFORE="$ARTIFACT_DIR/metrics-before.txt"
METRICS_AFTER="$ARTIFACT_DIR/metrics-after.txt"
EPP_LOG="$ARTIFACT_DIR/epp-container.log"
LOADGEN_LOG="$ARTIFACT_DIR/loadgen.log"
REPORT_JSON="$ARTIFACT_DIR/fairness-report.json"
REPORT_MD="$ARTIFACT_DIR/fairness-report.md"
CLIENT_RECORD_JSONL="$ARTIFACT_DIR/client-request-summary.jsonl"

# --- Resolve manifest with this scenario's overrides -----------------------
SRC="$(dirname "$0")/04-loadgen.yaml"
PATCHED="$ARTIFACT_DIR/04-loadgen.patched.yaml"
# UNI-231: rendered for this lane, not copied -- the manifest names
# maas-fairness-poc, and `oc apply -n` refuses a namespace mismatch.
NAMESPACE="$NAMESPACE" python3 -I "$(dirname "$0")/lanes.py" render "$SRC" > "$PATCHED"

set_override() {
  local var="$1" val="$2"
  python3 -I - "$PATCHED" "$var" "$val" "${GROUP_VAR_PREFIXES:-}" << 'PYEOF'
import sys, re
path, var, val = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(path).read()

# Already-uncommented entry (TENANTS, WORKERS, DURATION ship this way).
active = re.compile(r'(- name: ' + re.escape(var) + r'\n(?:\s*#[^\n]*\n)*\s*value: ")[^"]*(")')
new_text, n = active.subn(lambda m: m.group(1) + val + m.group(2), text, count=1)
if n == 0:
    # Per-tenant overrides (WORKERS_APP1/APP2/END_USERS) ship commented out.
    commented = re.compile(
        r'(?P<indent>[ \t]*)# - name: ' + re.escape(var) + r'\n'
        r'[ \t]*#[ \t]+value: "[^"]*"\n'
    )
    def repl(m):
        indent = m.group('indent')
        return f'{indent}- name: {var}\n{indent}  value: "{val}"\n'
    new_text, n = commented.subn(repl, text, count=1)
if n == 0 and re.fullmatch(r'[A-Z0-9_]+', var) and var.startswith(tuple(sys.argv[4].split())):
    # UNI-179: a per-group knob for a group 04-loadgen.yaml has no
    # placeholder for (app3..appN, or a new <KNOB>_<TOKEN> name). Only names
    # that start with a declared group token or a per-group knob prefix get
    # here; anything else still fails loudly as a typo.
    envline = re.compile(r'^(?P<indent>[ \t]*)env:\n', re.M)
    m = envline.search(text)
    if m:
        indent = m.group('indent') + '  '
        insert = f'{indent}- name: {var}\n{indent}  value: "{val}"\n'
        new_text = text[:m.end()] + insert + text[m.end():]
        n = 1
if n == 0:
    sys.exit(f"override target not found for {var} in {path}")
open(path, "w").write(new_text)
PYEOF
  echo "[benchmark] override: $var=$val"
}

set_override TENANTS "$TENANTS"
set_override WORKERS "${WORKERS:-32}"
set_override DURATION "$DURATION"
for kv in "${PER_TENANT_OVERRIDES[@]+"${PER_TENANT_OVERRIDES[@]}"}"; do
  set_override "${kv%%=*}" "${kv#*=}"
done

# --- UNI-127 timeline pass-through: only touches the Job (and the report's
# phase-edge math below) when one of these env vars is actually set. A plain
# invocation of an existing scenario sets none of them, so TIMELINE_JSON_ENTRIES
# stays empty and behaviour is unchanged. ----------------------------------
TIMELINE_JSON_ENTRIES=()
for v in $TIMELINE_VARS; do
  val="${!v-}"
  val="${val//s/}"
  if [ -n "$val" ]; then
    set_override "$v" "$val"
    TIMELINE_JSON_ENTRIES+=("$v=$val")
  fi
done
# UNI-128 profile pass-through: same shape as the timeline loop above, no
# JSON side-channel needed -- the Job records what it actually did per
# request itself (see the client-record extraction after the Job completes).
for v in $PROFILE_VARS; do
  val="${!v-}"
  if [ -n "$val" ]; then
    set_override "$v" "$val"
  fi
done
# UNI-129 identity-variant pass-through: same shape as the profile loop above.
for v in $IDENTITY_VARS; do
  val="${!v-}"
  if [ -n "$val" ]; then
    set_override "$v" "$val"
  fi
done

# --- UNI-179 per-group pass-through, for any declared group set. The loadgen
# resolves every group's settings from <KNOB>_<TOKEN> / WORKERS_<TOKEN> /
# <TOKEN>_KEYS / <TOKEN>_START|STOP|DUTY env vars (see 04-loadgen.yaml's
# group table); this forwards whichever of those are set in the caller's
# environment. Names that already had a route before UNI-179 are skipped so
# they keep it: the built-ins' WORKERS_/CACHE_SHAPE_/MAX_TOKENS_MODE_ (a
# scenario's PER_TENANT_OVERRIDES owns those -- forwarding a stray env copy
# would silently change an existing scenario) and the TIMELINE_VARS/
# IDENTITY_VARS lists above (already forwarded). LOADGEN_GROUPS itself is
# forwarded as-is; unset, the loadgen falls back to TENANTS. -------------
GROUP_KNOBS="$(grep -oP '^    GROUP_KNOBS="\K[^"]+' "$SRC")"
PREEXISTING_GROUP_VARS="WORKERS_APP1 WORKERS_APP2 WORKERS_END_USERS CACHE_SHAPE_APP1 CACHE_SHAPE_APP2 CACHE_SHAPE_END_USERS MAX_TOKENS_MODE_APP1 MAX_TOKENS_MODE_APP2 MAX_TOKENS_MODE_END_USERS $TIMELINE_VARS $IDENTITY_VARS"
BENCH_GROUPS="${LOADGEN_GROUPS:-$TENANTS}"
TIMELINE_TOKMAP="APP1=app1 APP2=app2 END_USERS=end-users"
GROUP_VAR_PREFIXES="WORKERS_"
for k in $GROUP_KNOBS; do GROUP_VAR_PREFIXES="$GROUP_VAR_PREFIXES ${k}_"; done
for spec in $BENCH_GROUPS; do
  g="${spec%%:*}"
  tok="$(printf '%s' "$g" | tr 'a-z' 'A-Z' | sed 's/[^A-Z0-9]/_/g')"
  GROUP_VAR_PREFIXES="$GROUP_VAR_PREFIXES ${tok}_"
  case " $TIMELINE_TOKMAP " in *" $tok="*) ;; *) TIMELINE_TOKMAP="$TIMELINE_TOKMAP $tok=$g" ;; esac
done
if [ -n "${LOADGEN_GROUPS-}" ]; then
  set_override LOADGEN_GROUPS "$LOADGEN_GROUPS"
fi
for spec in $BENCH_GROUPS; do
  g="${spec%%:*}"
  tok="$(printf '%s' "$g" | tr 'a-z' 'A-Z' | sed 's/[^A-Z0-9]/_/g')"
  for v in "WORKERS_$tok" "${tok}_KEYS" $(for k in $GROUP_KNOBS; do printf '%s ' "${k}_$tok"; done) \
           "${tok}_START" "${tok}_STOP" "${tok}_DUTY"; do
    case " $PREEXISTING_GROUP_VARS " in *" $v "*) continue ;; esac
    val="${!v-}"
    [ -n "$val" ] || continue
    case "$v" in
      *_START|*_STOP|*_DUTY)
        val="${val//s/}"
        TIMELINE_JSON_ENTRIES+=("$v=$val") ;;
    esac
    set_override "$v" "$val"
  done
done

TIMELINE_CONFIG="$ARTIFACT_DIR/timeline-config.json"
TIMELINE_TOKMAP="$TIMELINE_TOKMAP" python3 -I - "$TIMELINE_CONFIG" "${TIMELINE_JSON_ENTRIES[@]+"${TIMELINE_JSON_ENTRIES[@]}"}" << 'PYEOF'
import json, os, sys
out_path, entries = sys.argv[1], sys.argv[2:]
# UNI-179: TOKEN=group pairs for every declared group (the built-ins plus
# whatever LOADGEN_GROUPS adds), longest token first so END_USERS_ is never
# mistaken for a shorter token's prefix.
tokmap = dict(kv.split("=", 1) for kv in os.environ["TIMELINE_TOKMAP"].split())
by_tenant = {}
for e in entries:
    var, val = e.split("=", 1)
    tenant = field = None
    for tok in sorted(tokmap, key=len, reverse=True):
        if var.startswith(tok + "_") and var[len(tok) + 1:] in ("START", "STOP", "DUTY"):
            tenant, field = tokmap[tok], var[len(tok) + 1:]
            break
    if tenant is None:
        sys.exit(f"timeline var {var} matches no declared group")
    entry = by_tenant.setdefault(tenant, {})
    if field == "START":
        entry["start"] = float(val)
    elif field == "STOP":
        entry["stop"] = float(val)
    elif field == "DUTY":
        on, off = val.split("/", 1)
        entry["duty_on"] = float(on)
        entry["duty_off"] = float(off)
json.dump({"tenants": by_tenant, "chaos_events": []}, open(out_path, "w"), indent=2)
PYEOF

# --- UNI-127 chaos hooks (plus UNI-180's generic LIVE_SET_AT hook): queue up
# what this run will do to the live system, for the trap/chaos loop below and
# for the report's phase-edge math. Empty unless CHAOS_EPP_DELETE_AT /
# CHAOS_SCALE_AT / LIVE_SET_AT are set. --------------------
CHAOS_RESTORE_AT=""
if [ -n "$CHAOS_SCALE_AT" ]; then
  CHAOS_RESTORE_AT=$(( CHAOS_SCALE_AT + CHAOS_SCALE_HOLD ))
fi
# UNI-180: if LIVE_SET_HOLD applies (field: target only -- see
# live_set_restore_at_hold), the restore fires at that offset; otherwise it
# fires at run end, after the final metrics snapshot, which DURATION is the
# nearest known offset for -- see restore_live_set's own comment for why that
# can't be an exact live-measured second ahead of time.
LIVE_SET_RESTORE_AT=""
if [ -n "$LIVE_SET_AT" ]; then
  if [ -n "$LIVE_SET_HOLD" ] && live_set_restore_at_hold; then
    LIVE_SET_RESTORE_AT=$(( LIVE_SET_AT + LIVE_SET_HOLD ))
  else
    LIVE_SET_RESTORE_AT="$DURATION"
  fi
fi
python3 -I - "$TIMELINE_CONFIG" "$CHAOS_EPP_DELETE_AT" "$CHAOS_SCALE_AT" "$CHAOS_RESTORE_AT" "$LLMISVC_NAME" \
  "$LIVE_SET_AT" "$LIVE_SET_TARGET" "$LIVE_SET_VALUE" "$LIVE_SET_RESTORE_AT" << 'PYEOF'
import json, sys
path, delete_at, scale_at, restore_at, llmisvc, live_at, live_target, live_value, live_restore_at = sys.argv[1:10]
cfg = json.load(open(path))
events = []
if delete_at:
    events.append({"type": "epp_delete", "at_seconds": float(delete_at)})
if scale_at:
    events.append({"type": "scale_down", "at_seconds": float(scale_at), "target": llmisvc, "to": 1})
    events.append({"type": "scale_restore", "at_seconds": float(restore_at), "target": llmisvc})
if live_at:
    events.append({"type": "live_set", "at_seconds": float(live_at), "target": live_target, "value": live_value})
    events.append({"type": "live_restore", "at_seconds": float(live_restore_at), "target": live_target})
cfg["chaos_events"] = events
json.dump(cfg, open(path, "w"), indent=2)
PYEOF

# --- Clean up any previous run of the same Job name -------------------------
$OC delete job "$JOB_NAME" -n "$NAMESPACE" --ignore-not-found --wait=true >/dev/null

# --- Resolve target EPP pod, its restart count, and its metrics endpoint ---
EPP_POD="$($OC get pods -n "$NAMESPACE" -l "$EPP_SELECTOR" -o jsonpath='{.items[0].metadata.name}')"
if [ -z "$EPP_POD" ]; then
  echo "[benchmark] FATAL: no pod matched selector '$EPP_SELECTOR' in $NAMESPACE" >&2
  exit 1
fi
EPP_IMAGE_DIGEST="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath="{.status.containerStatuses[?(@.name=='$EPP_CONTAINER')].imageID}")"
START_RESTARTS="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath='{.status.containerStatuses[0].restartCount}')"
echo "[benchmark] target pod: $EPP_POD  image: $EPP_IMAGE_DIGEST  (restarts so far: $START_RESTARTS)"

# UNI-193: single source of truth for "which pod is the log-capture loop and
# the mid-run restart detector currently watching". Both of those run as
# their own background subshells (capture_loop) or read the variable from a
# stale fork (the restart detector in the Job-poll loop below) -- a plain
# `EPP_POD=...` reassignment in the main script body is invisible to a
# subshell that already captured the old value when it was backgrounded, so
# a pod-name change has to go through a file both sides poll/re-read.
# CHAOS_EPP_DELETE_AT was the gap: the enforce-flip path (below) already
# re-resolved EPP_POD, but the chaos-delete path never did, so after a chaos
# delete capture_loop retried "oc logs -f <gone-pod-name>" every second for
# the rest of the run (confirmed on UNI-155's E1 runs: 100%
# "(re)attaching/exited" scaffolding, zero real EPP log content, after the
# chaos delete in both the pass and the fail run) and the restart detector's
# "|| echo $START_RESTARTS" fallback made a gone pod look identical to a
# steady one.
EPP_POD_FILE="$ARTIFACT_DIR/.epp-pod-name"
printf '%s\n' "$EPP_POD" > "$EPP_POD_FILE"

# UNI-127: capture the LLMInferenceService's current replica count before any
# chaos runs, so a scale-down can be restored to what was actually there --
# not a hardcoded 2 -- whether or not the chaos loop gets to do it itself.
if [ -n "$CHAOS_SCALE_AT" ]; then
  ORIGINAL_REPLICAS="$($OC get llmisvc "$LLMISVC_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.replicas}')"
  echo "[benchmark] chaos: will scale $LLMISVC_NAME $ORIGINAL_REPLICAS -> 1 -> $ORIGINAL_REPLICAS at t+${CHAOS_SCALE_AT}s (hold ${CHAOS_SCALE_HOLD}s)"
fi
if [ -n "$CHAOS_EPP_DELETE_AT" ]; then
  echo "[benchmark] chaos: will delete EPP pod $EPP_POD at t+${CHAOS_EPP_DELETE_AT}s"
fi
if [ -n "$LIVE_SET_AT" ]; then
  if [ -n "$LIVE_SET_HOLD" ] && live_set_restore_at_hold; then
    echo "[benchmark] live-config: will set $LIVE_SET_TARGET -> $LIVE_SET_VALUE at t+${LIVE_SET_AT}s, restore after ${LIVE_SET_HOLD}s hold"
  elif [ -n "$LIVE_SET_HOLD" ]; then
    echo "[benchmark] live-config: will set $LIVE_SET_TARGET -> $LIVE_SET_VALUE at t+${LIVE_SET_AT}s -- LIVE_SET_HOLD is ignored for an epp-key/epp-weight target (always restores after the final metrics snapshot, never mid-run); restoring at run end"
  else
    echo "[benchmark] live-config: will set $LIVE_SET_TARGET -> $LIVE_SET_VALUE at t+${LIVE_SET_AT}s, restore at run end (after the final metrics snapshot)"
  fi
fi

METRICS_TOKEN="$($OC get secret maas-epp-metrics-reader-token -n "$NAMESPACE" -o jsonpath='{.data.token}' | base64 -d)"
EPP_METRICS_SVC_IP="${EPP_METRICS_SVC_IP:-}"
if [ -z "$EPP_METRICS_SVC_IP" ]; then
  EPP_METRICS_SVC_IP="$($OC get svc maas-vllm-gpu-epp-service -n "$NAMESPACE" -o jsonpath='{.spec.clusterIP}')"
fi

if [ "$ENFORCE_LIVE" = "true" ]; then
  # UNI-174: both EPPs resolve scheduler.config.ref to this same ConfigMap
  # (see the header note), so confirming the flip means confirming it on
  # both, not just the one this run's own EPP_SELECTOR targets. Resolved only
  # in this branch -- an invocation that doesn't set ENFORCE_LIVE must not
  # gain a new way to fail (or a new RBAC/topology dependency) just because
  # some other environment lacks a CPU EPP Service.
  resolve_cpu_epp
  CUR_EPP_YAML="$($OC get configmap "$CONFIGMAP_NAME" -n "$NAMESPACE" -o jsonpath='{.data.epp}')"
  if printf '%s' "$CUR_EPP_YAML" | grep -qE '^[[:space:]]*enforce:[[:space:]]*true'; then
    enforce_log "enforce already true in $CONFIGMAP_NAME -- nothing to flip; this run will NOT revert it on exit (it did not cause the enabled state)"
  else
    # UNI-180: re-expressed on top of live_config_set -- same ConfigMap edit,
    # same before-value capture, same merge-patch, just the shared mechanism
    # instead of a dedicated flip_enforce_value/patch_configmap_epp pair.
    live_config_set enforce-live "epp-key:enforce" "true"
    enforce_log "flipping $CONFIGMAP_NAME enforce false -> true"
    # Set BEFORE waiting: if the patch above succeeded but this script dies
    # on the next line, on_exit must still know to revert it. A successful
    # patch call, not a confirmed metric read, is what creates the
    # obligation to revert.
    ENFORCE_FLIPPED="true"
    if ! wait_for_enforcing "1"; then
      echo "[benchmark] FATAL: enforce flip did not take effect on both EPPs within ${ENFORCE_WAIT_TIMEOUT_SECONDS}s -- aborting before a shadow-mode measurement gets mislabeled as enforcing (the exit trap will still revert the ConfigMap edit)" >&2
      exit 1
    fi
    # UNI-145: this plugin has no live-reload path (see the note on
    # revert_enforce_live below) -- the flip just confirmed above deleted
    # $EPP_POD and replaced it with a new pod under a new name. Every use of
    # $EPP_POD from here on (the log-capture loop, the mid-run restart
    # detector) silently targeted a pod that no longer existed until this
    # re-resolve was added: "oc logs -f" against a gone pod fails in under a
    # second and the capture loop's own retry-forever design (UNI-169) just
    # masked it as an empty log file instead of an error, and the restart
    # detector's "|| echo $START_RESTARTS" fallback made a gone pod look
    # identical to a steady one. Confirmed live on 2026-11-02: an
    # ENFORCE_LIVE=true run's epp-container.log was 100% "(re)attaching /
    # exited" scaffolding, zero actual EPP lines, for its entire duration.
    EPP_POD="$($OC get pods -n "$NAMESPACE" -l "$EPP_SELECTOR" -o jsonpath='{.items[0].metadata.name}')"
    EPP_IMAGE_DIGEST="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath="{.status.containerStatuses[?(@.name=='$EPP_CONTAINER')].imageID}")"
    START_RESTARTS="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath='{.status.containerStatuses[0].restartCount}')"
    printf '%s\n' "$EPP_POD" > "$EPP_POD_FILE"
    echo "[benchmark] enforce flip replaced the EPP pod (no live-reload): target pod is now $EPP_POD (restarts so far: $START_RESTARTS)"
  fi
fi

if [ "$SHADOW_MODE" = "true" ]; then
  # UNI-159: mirror of the ENFORCE_LIVE block above, flipping the opposite
  # direction (true -> false) -- see that block's comments for why both EPPs
  # are resolved/confirmed and why the pod is re-resolved after the flip.
  # Mutually exclusive with ENFORCE_LIVE (checked before the scenario even
  # starts, see above), so this never runs in the same invocation as that
  # block.
  resolve_cpu_epp
  CUR_EPP_YAML="$($OC get configmap "$CONFIGMAP_NAME" -n "$NAMESPACE" -o jsonpath='{.data.epp}')"
  if printf '%s' "$CUR_EPP_YAML" | grep -qE '^[[:space:]]*enforce:[[:space:]]*false'; then
    enforce_log "enforce already false in $CONFIGMAP_NAME -- nothing to flip; this run will NOT revert it on exit (it did not cause the shadow state)"
  else
    live_config_set shadow-mode "epp-key:enforce" "false"
    enforce_log "flipping $CONFIGMAP_NAME enforce true -> false (shadow mode)"
    # Same ordering reason as ENFORCE_FLIPPED above: set before waiting, so a
    # death on the next line still leaves on_exit knowing to revert it.
    SHADOW_FLIPPED="true"
    if ! wait_for_enforcing "0"; then
      echo "[benchmark] FATAL: shadow-mode flip did not take effect on both EPPs within ${ENFORCE_WAIT_TIMEOUT_SECONDS}s -- aborting before an enforcing measurement gets mislabeled as shadow mode (the exit trap will still revert the ConfigMap edit)" >&2
      exit 1
    fi
    # Same no-live-reload pod-recreate hazard as the ENFORCE_LIVE flip above.
    EPP_POD="$($OC get pods -n "$NAMESPACE" -l "$EPP_SELECTOR" -o jsonpath='{.items[0].metadata.name}')"
    EPP_IMAGE_DIGEST="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath="{.status.containerStatuses[?(@.name=='$EPP_CONTAINER')].imageID}")"
    START_RESTARTS="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath='{.status.containerStatuses[0].restartCount}')"
    printf '%s\n' "$EPP_POD" > "$EPP_POD_FILE"
    echo "[benchmark] shadow-mode flip replaced the EPP pod (no live-reload): target pod is now $EPP_POD (restarts so far: $START_RESTARTS)"
  fi
fi

snapshot_metrics() {
  # UNI-138 (G2): also capture the core, un-gated, un-weighted per-request
  # token histograms' _sum/_count lines (fairness_id-labelled, but owned by
  # the framework, not the fairness plugin -- see pkg/fairness/weightedlas/
  # metrics.go's own "do not duplicate these" comment). The ledger
  # cross-check needs them next to llm_d_epp_maas_fairness_* in the same
  # before/after snapshot; omitting --client-record-jsonl downstream still
  # works against a snapshot that only has the old prefix, so this is purely
  # additive.
  #
  # UNI-193: also capture the upstream gateway-api-inference-extension's own
  # endpoint/flow-control metrics -- llm_d_epp_flow_control_* (including
  # stale_endpoints, pool_saturation, capacity_utilization, dispatch-cycle
  # duration) and llm_d_epp_ready_endpoints/per_endpoint_queue_size. UNI-155's
  # E1 runs showed every llm_d_epp_maas_fairness_*{fairness_id="end-users"}
  # series (dispatch_total, contended_*, normalized_service -- everything
  # except the static configured_weight gauge) go completely MISSING from
  # the after-snapshot in the run that starved, not merely zero, while the
  # same labels were present and nonzero in the run that recovered -- i.e.
  # end-users' traffic never reached the fairness plugin's own dispatch loop
  # at all after the chaos-deleted pod's replacement came up. That is
  # upstream of this plugin, in the picker's endpoint/queue bookkeeping, and
  # this benchmark was never scraping that layer to see it.
  # UNI-167 (H3): also capture the EPP's own scheduling-latency histograms --
  # scheduler_e2e (the pick itself) and plugin_duration (per-plugin, includes
  # plugin_type="maas-weighted-fairness") -- neither matched any prefix above,
  # so 15-fairness-report.py's compute_pick_latency() read "not_recorded" out
  # of every prior snapshot regardless of what the live EPP was doing
  # (confirmed against results/20261101T224216Z-uni140-b6-full-contention-soak/
  # metrics-full-before.txt, the one full un-grepped scrape on file: both
  # families are present and well-formed there, just outside this filter).
  # Purely additive, same as every prefix UNI-193 added before it.
  #
  # UNI-230: emit the curl call's own exit code as a leading `# scrape_exit=`
  # comment line, ahead of the grepped metric lines. A Prometheus text scrape
  # and a connection-level scrape failure (curl exit 7 during an overloaded
  # run, observed live on twenty-group-scale-discriminating) both end up as
  # zero matching lines once grepped -- indistinguishable to a downstream
  # consumer that only sees the grepped body. A real EPP restart also empties
  # every llm_d_epp_maas_fairness_* series (fresh process, fresh metric
  # registry), so "zero lines" alone can never tell "the scrape never reached
  # the EPP" apart from "the EPP really did restart." Recording curl's own
  # exit code is the only way to tell them apart after the fact; the `#`
  # prefix keeps this a no-op for parse_metrics_text/parse_metrics_labeled_text,
  # which already skip comment lines, so older callers and older captured
  # files are unaffected.
  #
  # UNI-226: also capture the upstream llm-d-router framework's own
  # per-tenant TTFT/ITL histograms -- llm_d_epp_request_ttft_seconds
  # (fairness_id-labelled, recorded for EVERY request in
  # pkg/epp/handlers/response.go's HandleResponseBody at endOfStream via
  # metrics.RecordRequestTTFT, streaming or not -- for a non-streaming
  # request this equals total duration) and
  # llm_d_epp_request_streaming_itl_seconds (fairness_id-labelled, recorded
  # per response chunk for streaming requests only, via
  # metrics.RecordInterTokenLatency). Neither was ever captured before this
  # ticket despite already being listed in docs/runbook.md's metrics
  # catalog table -- confirmed by grepping deploy/poc/*.py|*.sh and this
  # file itself for the metric names before UNI-226, zero hits. Purely
  # additive, same as every prefix before it.
  local raw rc=0
  raw="$(curl -sS -m 10 -H "Authorization: Bearer $METRICS_TOKEN" "http://${EPP_METRICS_SVC_IP}:9090/metrics")" || rc=$?
  echo "# scrape_exit=$rc"
  printf '%s\n' "$raw" \
    | grep -E '^llm_d_epp_maas_fairness_|^llm_d_epp_request_(input|output|cached)_tokens_(sum|count)\{|^llm_d_epp_request_(ttft|streaming_itl)_seconds_|^llm_d_epp_flow_control_|^llm_d_epp_scheduler_e2e_|^llm_d_epp_plugin_duration_|^llm_d_epp_(ready_endpoints|per_endpoint_queue_size|average_|std_dev_)' \
    | grep -v '^#' || true
}

echo "[benchmark] metrics snapshot: before"
snapshot_metrics > "$METRICS_BEFORE"
ENFORCE="$(awk '/^llm_d_epp_maas_fairness_enforcing/ {print ($2==1)?"true":"false"}' "$METRICS_BEFORE")"
RUN_START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_START_EPOCH="$(date +%s)"

# --- Log-capture loop: restarts -f if the stream ends early (UNI-46 shape) --
# UNI-127 note: CHAOS_EPP_DELETE_AT means $EPP_POD can go permanently NotFound
# partway through the run (the Deployment's replacement pod gets a new name --
# see docs/runbook.md's "Timeline, chaos, and windowed reporting"). Without
# the sleep below, "oc logs -f" against a gone pod fails instantly and this
# loop would hammer the API server every iteration for the rest of the run.
# UNI-169: $CAPTURE_PID below is the PID of the capture_loop *function's*
# subshell, not of the "oc logs -f" it execs -- bash does not propagate
# signals from a non-interactive shell to children it already forked, so
# killing $CAPTURE_PID alone leaves "oc logs -f" running and orphaned,
# reparented, and still appending to $EPP_LOG forever. Backgrounding the oc
# invocation itself and recording its own PID (refreshed on every re-attach,
# since a pod restart gets a new oc process) lets the trap/stop code below
# reach the actual log-streaming process.
CAPTURE_OC_PIDFILE="$ARTIFACT_DIR/.capture-oc.pid"
rm -f "$CAPTURE_OC_PIDFILE"
capture_loop() {
  local since="$RUN_START" pod="" last_pod=""
  while kill -0 "$$" 2>/dev/null; do
    # UNI-193: re-read the watched pod name every iteration -- this subshell
    # forked with its own copy of $EPP_POD and never sees a later
    # reassignment in the main script body (chaos_loop is a *different*
    # subshell too, so even its own reassignment wouldn't reach here). The
    # file is the only channel both sides actually observe.
    pod="$(cat "$EPP_POD_FILE" 2>/dev/null || echo "$EPP_POD")"
    if [ "$pod" != "$last_pod" ]; then
      echo "--- [benchmark] (re)attaching oc logs -f to $pod at $since ---" >> "$EPP_LOG"
      last_pod="$pod"
    else
      echo "--- [benchmark] (re)attaching oc logs -f at $since ---" >> "$EPP_LOG"
    fi
    $OC logs -f "$pod" -n "$NAMESPACE" -c "$EPP_CONTAINER" --since-time="$since" >> "$EPP_LOG" 2>>"$EPP_LOG.capture-stderr" &
    echo "$!" > "$CAPTURE_OC_PIDFILE"
    wait "$!" || true
    since="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "--- [benchmark] oc logs -f exited at $since; checking for a pod restart ---" >> "$EPP_LOG"
    sleep 1
  done
}
capture_loop &
CAPTURE_PID=$!

# --- UNI-127 time-series loop: snapshot the same /metrics endpoint every
# WINDOW_SECONDS, so the report can turn before/after into a sequence of
# windows instead of one whole-run delta. Runs for every invocation, not just
# ones using the timeline/chaos knobs -- this is the harness capability the
# ticket asks be available by default. First entry mirrors metrics-before.txt
# exactly, so the first window starts at t=0 with no extra scrape needed.
METRICS_TS="$ARTIFACT_DIR/metrics-timeseries.txt"
{ echo "# ts=$RUN_START epoch=$RUN_START_EPOCH"; cat "$METRICS_BEFORE"; } > "$METRICS_TS"
timeseries_loop() {
  # UNI-193: this whole script runs under `set -euo pipefail` (line 303),
  # which this background subshell inherits. snapshot_metrics' curl hits a
  # Service with zero ready endpoints for a few seconds around any pod
  # replacement (chaos delete, enforce flip, the end-of-run revert) and
  # fails with a real nonzero exit -- under -e/pipefail, in the foreground
  # of this subshell (not backgrounded, not `|| true`-guarded) that one
  # transient failure terminated the *entire loop* for the rest of the run,
  # not just that one window. Confirmed live on UNI-155's E1 runs and on a
  # same-scenario repro for this ticket: all three showed metrics-timeseries
  # go completely silent for ~300s starting at the first post-chaos-delete
  # scrape, in the PASS run and the FAIL run alike -- a harness artifact,
  # not evidence of anything the EPP did differently between them.
  set +e
  while kill -0 "$$" 2>/dev/null; do
    sleep "$WINDOW_SECONDS"
    { echo "# ts=$(date -u +%Y-%m-%dT%H:%M:%SZ) epoch=$(date +%s)"; snapshot_metrics; } >> "$METRICS_TS"
  done
}
timeseries_loop &
TS_PID=$!

# UNI-193: periodic namespace Events snapshot. UNI-155's E1 runs showed
# FailedPreStopHook/Unhealthy readiness-probe events on the chaos-deleted pod
# that this harness never recorded anywhere -- that evidence only existed
# live via `oc get events` and expires with the default ~1h Event TTL, so a
# run investigated more than an hour later has nothing to go on. Namespace
# Events (not just the EPP pod's own) because the chaos window also produces
# Gateway/InferencePool/LLMInferenceService events that bear on recovery.
# Appends a full sorted snapshot every WINDOW_SECONDS rather than following a
# single object with --watch: a watch stream dies/reattaches exactly like
# capture_loop's "oc logs -f" does (same NotFound-on-a-deleted-object
# failure mode), and duplicating a cheap snapshot is simpler than rebuilding
# that whole retry apparatus for a second object kind.
K8S_EVENTS_LOG="$ARTIFACT_DIR/k8s-events-timeseries.log"
snapshot_events() {
  # UNI-193: Events have no equivalent of `--since-time` server-side, and a
  # namespace accumulates them for its ~1h TTL regardless of this run's own
  # start time -- an unfiltered snapshot re-dumps that whole rolling hour on
  # every single WINDOW_SECONDS tick, so a 6-7 minute run produced a 1.3MB
  # log that was >95% the same old lines repeated ~40 times (confirmed live
  # on this ticket's own repro run: entries from 2+ hours before RUN_START
  # were still present at the last tick). Filter to lastTimestamp >= this
  # run's own start so each tick only adds what actually happened during
  # the run -- ISO8601 Z-format timestamps compare correctly as plain
  # strings, so a plain field compare is enough, no date parsing needed.
  $OC get events -n "$NAMESPACE" --sort-by='.lastTimestamp' \
    -o custom-columns='TIME:.lastTimestamp,TYPE:.type,REASON:.reason,KIND:.involvedObject.kind,NAME:.involvedObject.name,MESSAGE:.message' \
    --no-headers 2>/dev/null | awk -v start="$RUN_START" '$1 >= start'
}
{ echo "# ts=$RUN_START epoch=$RUN_START_EPOCH"; snapshot_events; } > "$K8S_EVENTS_LOG"
events_loop() {
  # UNI-193: same `set -e` exposure as timeseries_loop above -- a transient
  # `oc get events` failure (API server hiccup, token refresh, etc.) would
  # otherwise kill this loop for the rest of the run instead of just
  # skipping one window.
  set +e
  while kill -0 "$$" 2>/dev/null; do
    sleep "$WINDOW_SECONDS"
    { echo "# ts=$(date -u +%Y-%m-%dT%H:%M:%SZ) epoch=$(date +%s)"; snapshot_events; } >> "$K8S_EVENTS_LOG"
  done
}
events_loop &
EVENTS_PID=$!

# --- UNI-127 chaos loop: fires the configured hooks at their t+offset and
# logs each one, with a timestamp, to chaos-events.log. A no-op loop (nothing
# configured) still runs but never does anything -- simpler than conditionally
# starting it, and it exits the moment the trap kills it.
CHAOS_LOG="$ARTIFACT_DIR/chaos-events.log"
: > "$CHAOS_LOG"
chaos_log() {
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $1" | tee -a "$CHAOS_LOG"
}
# UNI-193: poll for the Deployment's replacement pod after a chaos delete and
# publish its name to $EPP_POD_FILE, which capture_loop and the mid-run
# restart detector now re-read every iteration instead of trusting the
# $EPP_POD value each of them forked with. Runs detached from chaos_loop's
# own 1s cadence so a slow-to-schedule replacement doesn't delay the other
# chaos hooks (CHAOS_SCALE_AT/LIVE_SET_AT) sharing that loop. Bounded at 60
# attempts (~60s): past that, something other than a normal reschedule is
# wrong and hammering forever is exactly the bug being fixed here.
resolve_replacement_pod_async() {
  local old_pod="$1" new_pod="" tries=0
  while [ "$tries" -lt 60 ]; do
    tries=$(( tries + 1 ))
    new_pod="$($OC get pods -n "$NAMESPACE" -l "$EPP_SELECTOR" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)"
    if [ -n "$new_pod" ] && [ "$new_pod" != "$old_pod" ]; then
      printf '%s\n' "$new_pod" > "$EPP_POD_FILE"
      chaos_log "chaos: replacement EPP pod for $old_pod is $new_pod (found after ${tries}s)"
      return 0
    fi
    sleep 1
  done
  chaos_log "chaos: WARNING no replacement pod found for $old_pod after ${tries}s -- capture/restart-detection still watching the deleted pod"
}
chaos_loop() {
  local delete_done=false scale_down_done=false scale_up_done=false \
        live_set_done=false live_restore_done=false elapsed
  while kill -0 "$$" 2>/dev/null; do
    elapsed=$(( $(date +%s) - RUN_START_EPOCH ))
    if [ -n "$CHAOS_EPP_DELETE_AT" ] && [ "$delete_done" = false ] && [ "$elapsed" -ge "$CHAOS_EPP_DELETE_AT" ]; then
      $OC delete pod "$EPP_POD" -n "$NAMESPACE" --wait=false >/dev/null 2>&1 || true
      chaos_log "chaos: deleted EPP scheduler pod $EPP_POD (t+${elapsed}s, target was t+${CHAOS_EPP_DELETE_AT}s)"
      resolve_replacement_pod_async "$EPP_POD" &
      delete_done=true
    fi
    # UNI-180: re-expressed on top of live_config_set/live_config_restore --
    # same scale-to-1-and-back, same ORIGINAL_REPLICAS, just the shared
    # mechanism instead of two bespoke `oc patch` calls.
    if [ -n "$CHAOS_SCALE_AT" ] && [ "$scale_down_done" = false ] && [ "$elapsed" -ge "$CHAOS_SCALE_AT" ]; then
      live_config_set chaos-scale "field:llmisvc:$LLMISVC_NAME:spec.replicas" "1"
      chaos_log "chaos: scaled $LLMISVC_NAME replicas $ORIGINAL_REPLICAS -> 1 (t+${elapsed}s, target was t+${CHAOS_SCALE_AT}s)"
      scale_down_done=true
    fi
    if [ "$scale_down_done" = true ] && [ "$scale_up_done" = false ] && [ "$elapsed" -ge "$CHAOS_RESTORE_AT" ]; then
      live_config_restore chaos-scale
      chaos_log "chaos: restored $LLMISVC_NAME replicas 1 -> $ORIGINAL_REPLICAS (t+${elapsed}s, target was t+${CHAOS_RESTORE_AT}s)"
      scale_up_done=true
    fi
    # UNI-180: the generic mid-run hook. Restoring here (rather than waiting
    # for restore_live_set after the run) only happens for a `field:` target
    # with LIVE_SET_HOLD set -- see live_set_restore_at_hold.
    if [ -n "$LIVE_SET_AT" ] && [ "$live_set_done" = false ] && [ "$elapsed" -ge "$LIVE_SET_AT" ]; then
      # UNI-163: read the pre-patch pod name from the same file CHAOS_EPP_DELETE_AT
      # keeps current, not the $EPP_POD this subshell forked with -- see the
      # UNI-193 comment above resolve_replacement_pod_async for why.
      local pre_set_pod
      pre_set_pod="$(cat "$EPP_POD_FILE" 2>/dev/null || echo "$EPP_POD")"
      live_config_set live-set "$LIVE_SET_TARGET" "$LIVE_SET_VALUE"
      chaos_log "live-config: set $LIVE_SET_TARGET -> $LIVE_SET_VALUE (t+${elapsed}s, target was t+${LIVE_SET_AT}s)"
      if live_set_target_recreates_pod "$LIVE_SET_TARGET"; then
        resolve_replacement_pod_async "$pre_set_pod" &
      fi
      live_set_done=true
    fi
    if [ "$live_set_done" = true ] && [ "$live_restore_done" = false ] && [ -n "$LIVE_SET_HOLD" ] \
       && live_set_restore_at_hold && [ "$elapsed" -ge "$LIVE_SET_RESTORE_AT" ]; then
      live_config_restore live-set
      chaos_log "live-config: restored $LIVE_SET_TARGET (t+${elapsed}s, target was t+${LIVE_SET_RESTORE_AT}s)"
      live_restore_done=true
    fi
    sleep 1
  done
}
chaos_loop &
CHAOS_PID=$!

# UNI-174: the EXIT/INT/TERM/HUP trap registered earlier (on_exit, before the
# first cluster mutation in this script) already covers stop_background_loops
# and restore_chaos_scale -- CAPTURE_PID/TS_PID/CHAOS_PID and ORIGINAL_REPLICAS
# are now all set, so from this point on that trap is fully armed for a crash
# during Job polling, not just for the post-processing tail below. No
# second, narrower trap is registered here anymore.

# --- Apply the patched Job and poll to completion ---------------------------
$OC apply -f "$PATCHED" -n "$NAMESPACE"
echo "[benchmark] job applied, polling for completion..."
PHASE=""
RESTART_EVENTS=0
for i in $(seq 1 240); do
  SUCCEEDED="$($OC get job "$JOB_NAME" -n "$NAMESPACE" -o jsonpath='{.status.succeeded}' 2>/dev/null || true)"
  FAILED="$($OC get job "$JOB_NAME" -n "$NAMESPACE" -o jsonpath='{.status.failed}' 2>/dev/null || true)"
  # UNI-193: a chaos delete updates $EPP_POD_FILE from chaos_loop's own
  # subshell, which this (main-shell, foreground) loop never sees via the
  # $EPP_POD variable itself -- re-read the file each iteration so a chaos
  # delete doesn't make this detector silently watch a pod that is gone for
  # the rest of the run.
  EPP_POD="$(cat "$EPP_POD_FILE" 2>/dev/null || echo "$EPP_POD")"
  CUR_RESTARTS="$($OC get pod "$EPP_POD" -n "$NAMESPACE" -o jsonpath='{.status.containerStatuses[0].restartCount}' 2>/dev/null || echo "$START_RESTARTS")"
  if [ "$CUR_RESTARTS" != "$START_RESTARTS" ] && [ "$RESTART_EVENTS" -eq 0 ]; then
    RESTART_EVENTS=1
    echo "[benchmark] WARNING: EPP pod restart detected mid-run ($START_RESTARTS -> $CUR_RESTARTS)"
  fi
  echo "[benchmark] [$i] job=$JOB_NAME succeeded=${SUCCEEDED:-0} failed=${FAILED:-0} epp_restarts=$CUR_RESTARTS"
  if [ "${SUCCEEDED:-0}" = "1" ] || [ "${FAILED:-0}" -ge 1 ] 2>/dev/null; then
    PHASE="done"
    break
  fi
  sleep 10
done
if [ "$PHASE" != "done" ]; then
  echo "[benchmark] WARNING: polling timed out before the Job reported completion" >&2
fi

# UNI-149 (C5): optional idle-observation window. Traffic has fully stopped
# (the Job above reported done) but capture_loop/timeseries_loop/chaos_loop
# are still running below this point -- that keeps the EPP container log and
# the periodic metrics snapshot flowing for SETTLE_SECONDS before the next
# block silences them, so a claim like "provisional tokens return to zero
# once traffic stops" has live evidence instead of being inferred. UNI-145's
# C2 section (docs/poc-results.md) hit exactly this gap and recommended this
# knob. 0 (default) is a no-op -- every scenario before this ticket keeps its
# existing immediate-stop behavior.
SETTLE_SECONDS="${SETTLE_SECONDS:-0}"
if [ "$SETTLE_SECONDS" -gt 0 ] 2>/dev/null; then
  echo "[benchmark] settling: traffic stopped, waiting ${SETTLE_SECONDS}s before snapshotting/reverting (capture+timeseries stay live)"
  chaos_log "settle: traffic stopped, waiting ${SETTLE_SECONDS}s before after-snapshot/revert"
  sleep "$SETTLE_SECONDS"
  chaos_log "settle: ${SETTLE_SECONDS}s window elapsed"
fi

# --- Stop capture/timeseries/chaos now (promptly, rather than leaving them
# running through report-building below) and restore a drifted replica
# count, via the SAME functions the on_exit trap uses, called explicitly
# here for the common (non-crash) case. restore_live_set/revert_enforce_live
# are deliberately NOT called yet -- see the note below the metrics-after
# snapshot.
stop_background_loops
restore_chaos_scale

LOADGEN_POD="$($OC get pods -n "$NAMESPACE" -l job-name="$JOB_NAME" -o jsonpath='{.items[0].metadata.name}')"
$OC logs "$LOADGEN_POD" -n "$NAMESPACE" > "$LOADGEN_LOG" 2>&1 || echo "[benchmark] WARNING: could not fetch loadgen pod log" >&2

# UNI-128: pull this run's per-tenant client-side record (requests sent,
# status tally, prompt/completion tokens actually received, aborts, errors)
# out of the pod's own stdout and into the results directory, so G2 (ledger
# cross-check) has it next to the EPP's before/after metric snapshots
# without needing the pod to still exist.
grep '^CLIENT_RECORD_JSON ' "$LOADGEN_LOG" | sed 's/^CLIENT_RECORD_JSON //' > "$CLIENT_RECORD_JSONL" || true

echo "[benchmark] metrics snapshot: after"
snapshot_metrics > "$METRICS_AFTER"
RUN_END="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
{ echo "# ts=$RUN_END epoch=$(date +%s)"; cat "$METRICS_AFTER"; } >> "$METRICS_TS"

# UNI-143 (B4 investigation): these three reverts are called here -- AFTER
# the after-snapshot, not before. This plugin's config has no live-reload
# path (pkg/fairness/weightedlas/plugin.go's v4Logger comment: "Factory
# decodes it once, at construction"), so every maas-epp-config edit this
# script makes, including a revert, is actually applied by the
# LLMInferenceService controller DELETING AND RECREATING the EPP pod -- same
# Deployment/ReplicaSet, new pod, fresh Prometheus registry. The pod's
# container restartCount is unaffected (it is a new pod, not a restarted
# container), so the mid-run-restart check above cannot see this. Reverting
# before this snapshot silently zeroes every llm_d_epp_maas_fairness_contended_*
# and dispatch_total series the report depends on -- the run still completes
# and a report still gets written, but every group's contended_seconds comes
# back null and the verdict reads UNCONTENDED regardless of what actually
# happened. Caught on uni-143-b4-long-idle-return's first attempt: the
# timeseries capture showed real, growing contended_seconds_total through
# the run, and both metrics-before.txt/metrics-after.txt dropped to the same
# 6 static lines the instant enforce flipped. Confirmed via `oc get pods`:
# the pod on record for that run no longer existed afterward; a new pod
# under the same ReplicaSet hash had replaced it, age-zero at revert time.
#
# UNI-163 fix: restore_live_set MUST run before revert_enforce_live/
# revert_shadow_mode, not after -- this call site had them in the opposite
# order from on_exit's (correct) sequence above, and that divergence was
# latent until UNI-163 (F6) first combined ENFORCE_LIVE=true with a LIVE_SET_AT
# target that edits this same ConfigMap's data.epp. live_config_restore's
# idempotency check compares the CURRENT live value against what THIS id
# applied; running revert_enforce_live first flips `enforce` back on top of
# the live-set id's still-applied text (not the pre-run text), so when
# restore_live_set runs next, the live value no longer matches what live-set
# applied (enforce now differs) and it logs "nothing to do" -- silently
# leaving the live-set change (here, three re-weighted groups) live after the
# run, in violation of this series' own "leave the cluster as you found it"
# rule. Confirmed live on UNI-163's first run: maas-epp-config was left at
# app1/app2/end-users weight 40/20/40 (enforce correctly back to false) until
# caught by the post-run `oc get` check and corrected by hand. Restoring
# live-set first means its own idempotency check runs against the untouched
# post-run live value, exactly like on_exit already does it.
restore_live_set
revert_enforce_live
# UNI-159: revert_shadow_mode shares the exact same hazard (and the exact
# same reason it must run AFTER the after-snapshot, not before) as
# revert_enforce_live just above -- it is the same pod-recreate-on-ConfigMap-
# edit mechanism, just restoring the opposite flip direction.
revert_shadow_mode

# UNI-138 (G2): the ledger cross-check's cost formula needs the EPP's live
# cost-model weights to translate the client's raw token counts into the
# same unit contended_service_tokens_total is denominated in (pkg/fairness/
# weightedlas/cost.go). No metric exposes these (metrics.go deliberately
# ships only series that are not configuration), so read them straight out
# of the ConfigMap rather than hardcoding deploy/epp-config.yaml's committed
# defaults, which could have drifted from what is actually live. Fall back
# to 1.0 (plain token sum) if a key is absent, same as the report script's
# own CLI defaults.
EPP_CONFIG_YAML="$($OC get configmap maas-epp-config -n "$NAMESPACE" -o jsonpath='{.data.epp}')"
INPUT_TOKEN_WEIGHT="$(printf '%s\n' "$EPP_CONFIG_YAML" | grep -oP '^\s*inputTokenWeight:\s*\K[0-9.]+' | head -1)"
OUTPUT_TOKEN_WEIGHT="$(printf '%s\n' "$EPP_CONFIG_YAML" | grep -oP '^\s*outputTokenWeight:\s*\K[0-9.]+' | head -1)"
CACHED_INPUT_TOKEN_WEIGHT="$(printf '%s\n' "$EPP_CONFIG_YAML" | grep -oP '^\s*cachedInputTokenWeight:\s*\K[0-9.]+' | head -1)"
INPUT_TOKEN_WEIGHT="${INPUT_TOKEN_WEIGHT:-1.0}"
OUTPUT_TOKEN_WEIGHT="${OUTPUT_TOKEN_WEIGHT:-1.0}"
CACHED_INPUT_TOKEN_WEIGHT="${CACHED_INPUT_TOKEN_WEIGHT:-1.0}"
echo "[benchmark] ledger cost model (live from maas-epp-config): input=$INPUT_TOKEN_WEIGHT output=$OUTPUT_TOKEN_WEIGHT cached=$CACHED_INPUT_TOKEN_WEIGHT"

# --- Build the report; its exit code becomes this script's exit code -------
set +e
REPORT_ARGS=(
  --scenario "$SCENARIO" --label "$LABEL" --enforce "$ENFORCE"
  --duration-seconds "$DURATION" --backend "$BACKEND"
  --epp-image-digest "$EPP_IMAGE_DIGEST" --namespace "$NAMESPACE" --epp-pod "$EPP_POD"
  --run-start "$RUN_START" --run-end "$RUN_END" --threshold-points "$THRESHOLD_POINTS"
  --metrics-before "$METRICS_BEFORE" --metrics-after "$METRICS_AFTER" --loadgen-log "$LOADGEN_LOG"
  --metrics-timeseries "$METRICS_TS" --timeline-config "$TIMELINE_CONFIG" --window-seconds "$WINDOW_SECONDS"
  --client-record-jsonl "$CLIENT_RECORD_JSONL"
  --input-token-weight "$INPUT_TOKEN_WEIGHT" --output-token-weight "$OUTPUT_TOKEN_WEIGHT"
  --cached-input-token-weight "$CACHED_INPUT_TOKEN_WEIGHT" --ledger-tolerance-pct "$LEDGER_TOLERANCE_PCT"
  --out-json "$REPORT_JSON" --out-md "$REPORT_MD"
)
if [ "$IS_CONTROL" = "true" ]; then
  REPORT_ARGS+=(--control)
fi
python3 -I "$(dirname "$0")/15-fairness-report.py" "${REPORT_ARGS[@]}"
REPORT_EXIT=$?
set -e

echo "[benchmark] report: $REPORT_JSON , $REPORT_MD"
echo "[benchmark] client-side request record: $CLIENT_RECORD_JSONL"
exit "$REPORT_EXIT"
