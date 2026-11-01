#!/bin/bash
# UNI-96: remove the dead v1-simulator-path objects, stale ReplicaSets, finished
# load-test residue, build residue, and the inert Grafana dashboard ConfigMap
# from maas-fairness-poc, inventoried read-only on 2026-10-29 and approved on
# UNI-88.
#
# Scope is exactly the object list in UNI-96. Nothing else in the namespace is
# touched: in particular this script never names is/maas-epp (the running GPU
# EPP pulls its image digest from that ImageStream) or any of the maas-vllm-*
# serving/routing objects.
#
# Idempotent: every delete uses --ignore-not-found, so re-running after a
# partial run (or after everything is already gone) is a no-op.
#
# Usage:
#   OPENSHIFT_TOKEN=... ./deploy/poc/cleanup-dead-objects.sh --dry-run
#   OPENSHIFT_TOKEN=... ./deploy/poc/cleanup-dead-objects.sh
set -u
set -o pipefail

NAMESPACE="maas-fairness-poc"
DRY_RUN=false
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    *) echo "unknown argument: $arg" >&2; exit 2 ;;
  esac
done

: "${OPENSHIFT_TOKEN:?OPENSHIFT_TOKEN must be set}"
OC_SERVER="${OPENSHIFT_API_SERVER:-https://api.ocp.paladinaura.com:6443}"
OC=(oc "--token=${OPENSHIFT_TOKEN}" "--server=${OC_SERVER}")

FAILURES=0

# Deletes one object. --ignore-not-found makes an already-deleted object a
# no-op; any OTHER failure (e.g. Forbidden) is reported but does not stop the
# rest of the cleanup.
del() {
  local kind="$1" name="$2"
  if $DRY_RUN; then
    echo "[dry-run] would delete ${kind}/${name} -n ${NAMESPACE}"
    return 0
  fi
  echo "deleting ${kind}/${name} -n ${NAMESPACE}"
  if ! "${OC[@]}" delete "${kind}" "${name}" -n "${NAMESPACE}" --ignore-not-found; then
    echo "FAILED to delete ${kind}/${name} (see error above)" >&2
    FAILURES=$((FAILURES + 1))
  fi
}

# Deletes every object of a kind matching a label selector. Used for the
# stale ReplicaSets and loadgen pods, where matching by selector is more
# robust than hardcoding generated names.
del_selector() {
  local kind="$1" selector="$2"
  if $DRY_RUN; then
    echo "[dry-run] would delete ${kind} -l ${selector} -n ${NAMESPACE}:"
    "${OC[@]}" get "${kind}" -l "${selector}" -n "${NAMESPACE}" \
      -o name --ignore-not-found | sed 's/^/[dry-run]   /'
    return 0
  fi
  echo "deleting ${kind} -l ${selector} -n ${NAMESPACE}"
  if ! "${OC[@]}" delete "${kind}" -l "${selector}" -n "${NAMESPACE}" --ignore-not-found; then
    echo "FAILED to delete ${kind} -l ${selector} (see error above)" >&2
    FAILURES=$((FAILURES + 1))
  fi
}

echo "=== UNI-96 cleanup: namespace ${NAMESPACE}, dry-run=${DRY_RUN} ==="

echo "--- 1. v1 simulator path (pre-KServe architecture) ---"
del deployment maas-epp
del deployment maas-sim
del service maas-epp
del service maas-sim
del httproute maas-poc-route
# deploy/poc/02-epp.yaml declares maas-pool TWICE, deliberately: as
# inference.networking.k8s.io/v1 (02-epp.yaml line 88) and as
# inference.networking.x-k8s.io/v1alpha2 (02-epp.yaml line 254).
# docs/poc-results.md, pitfall 6 ("Two InferencePool API groups, and both
# are needed"), explains why: the EPP only watches the v1 group, this
# cluster's gateway controller only resolves x-k8s.io/v1alpha2 backendRefs
# and rejects a v1 pool outright, so both objects are real and both have to
# be deleted. An earlier version of this comment (UNI-123) called the
# k8s.io/v1 group "empty" -- that was wrong, and this repo's own manifest
# is what shows it: it is not an unused group a bare `inferencepool` short
# name might land on by discovery-order accident, it is a second live pool.
#
# The two pools are not equally confirmable from here. The x-k8s.io pool's
# survival is directly observable on-cluster: it owns
# svc/maas-pool-ip-73df004c via ownerReferences (see UNI-123,
# docs/runbook.md), and that Service is readable even though the pool
# itself is not. The v1 pool has no such proxy -- the gateway controller
# never resolves it, so it mints no Service and leaves no ownerReference
# anywhere an agent token can read. Its existence here is inferred from
# 02-epp.yaml, not observed on the cluster: no agent token can `get` or
# `list` either inference group to confirm it directly (re-verified
# 2026-11-01). Absence of a visible v1 pool would look identical to one
# having already been deleted, so this script deletes it unconditionally
# rather than trying to detect it first.
#
# The Engineer role's edit grant in maas-fairness-poc does not extend to
# either inference group, so both deletes below are expected to fail with
# Forbidden rather than succeed or report not-found. Left in so the script
# does the right thing the day that grant is widened or a cluster-admin
# runs it, and so a dry run documents the gap instead of hiding it.
# del()'s --ignore-not-found already makes a missing object (either pool,
# already deleted or never created) a no-op rather than a failure; only a
# Forbidden or other real error counts against FAILURES.
#
# Both run BEFORE the service delete below: the x-k8s.io pool owns
# svc/maas-pool-ip-73df004c via ownerReferences, so deleting it
# garbage-collects the Service on its own. Deleting the Service first (as
# this script used to) just has the controller recreate it before the pool
# delete lands.
del inferencepools.v1alpha2.inference.networking.x-k8s.io maas-pool
del inferencepools.v1.inference.networking.k8s.io maas-pool
del service maas-pool-ip-73df004c
del serviceaccount maas-epp
# Deliberately NOT touched: serviceaccount/maas-epp-metrics-reader. The name
# looks like it pairs with serviceaccount/maas-epp above, but it does not --
# it is live infrastructure defined in deploy/rbac.yaml, not v1-simulator
# residue. Its long-lived secret/maas-epp-metrics-reader-token is consumed by
# deploy/poc/15-fairness-benchmark.sh and deploy/poc/13-loadgen-poisson.sh to
# snapshot the fairness counters, and is referenced by deploy/podmonitor.yaml
# for scraping. UNI-96 deleted this SA on that false pairing with
# serviceaccount/maas-epp and broke the benchmark's metrics snapshot step; it
# was restored by re-applying deploy/rbac.yaml. Deleting the SA
# cascade-deletes the token Secret, so there is no cheap undo -- do not add
# this line back.

echo "--- 2. stale ReplicaSets at 0/0 ---"
del_selector replicaset "app=maas-epp"
del_selector replicaset "app=maas-sim"
# The router-scheduler ReplicaSets carry no stable label for "not the current
# revision", so the scaled-down ones are named explicitly. Re-verify this
# list with 'oc get rs -n maas-fairness-poc' if the deployments have rolled
# since 2026-10-29 -- a new rollout adds a new stale RS this script does not
# know about.
for rs in \
  maas-vllm-cpu-kserve-router-scheduler-656c8b4dd7 \
  maas-vllm-cpu-kserve-router-scheduler-68c9fd6896 \
  maas-vllm-cpu-kserve-router-scheduler-698ffcdb5c \
  maas-vllm-cpu-kserve-router-scheduler-7b9ffb6cf5 \
  maas-vllm-cpu-kserve-router-scheduler-7f56c74698 \
  maas-vllm-cpu-kserve-router-scheduler-7ff464f784 \
  maas-vllm-cpu-kserve-router-scheduler-844b7b6894 \
  maas-vllm-cpu-kserve-router-scheduler-85c5587d54 \
  maas-vllm-cpu-kserve-router-scheduler-97565fc86 \
  maas-vllm-cpu-kserve-router-scheduler-f5bdf6b9 \
  maas-vllm-gpu-kserve-router-scheduler-58b88fcf78 \
  maas-vllm-gpu-kserve-router-scheduler-6684457c7d \
  maas-vllm-gpu-kserve-router-scheduler-686858dc66 \
  maas-vllm-gpu-kserve-router-scheduler-7848446944 \
  maas-vllm-gpu-kserve-router-scheduler-79d96577d9 \
  maas-vllm-gpu-kserve-router-scheduler-7b7c78cdd5 \
  maas-vllm-gpu-kserve-router-scheduler-7cf65f7cc8 \
  maas-vllm-gpu-kserve-router-scheduler-7d9f9d9b56 \
  maas-vllm-gpu-kserve-router-scheduler-8597f9b9d5 \
  maas-vllm-gpu-kserve-router-scheduler-d95dcd886 \
; do
  del replicaset "$rs"
done

echo "--- 2b. revisionHistoryLimit: 2 on the deployments that remain ---"
# All five remaining Deployments in this namespace are controller-generated
# (LLMInferenceService for the two kserve/router-scheduler pairs, the Gateway
# API controller for the gateway) and none is a raw Deployment manifest in
# this repo -- the repo defines the owning CRs (deploy/poc/07-vllm-cpu.yaml,
# deploy/poc/09-vllm-gpu.yaml, deploy/poc/03-gateway.yaml), not the
# Deployments themselves. No field was found on the LLMInferenceService CRD
# to pass revisionHistoryLimit through to the generated Deployment (its
# `template` blocks merge into the pod/container spec, not the Deployment
# spec), so there is no matching repo change to raise for these four; the
# patch below is applied directly and may be reverted the next time its
# owning controller reconciles the object (e.g. on an image or replica
# change). Flagging this as a known gap rather than claiming it is durable.
for d in \
  maas-vllm-cpu-kserve \
  maas-vllm-cpu-kserve-router-scheduler \
  maas-vllm-gpu-kserve \
  maas-vllm-gpu-kserve-router-scheduler \
  maas-poc-gateway-data-science-gateway-class \
; do
  if $DRY_RUN; then
    echo "[dry-run] would patch deployment/${d} -n ${NAMESPACE}: revisionHistoryLimit=2"
    continue
  fi
  echo "patching deployment/${d} -n ${NAMESPACE}: revisionHistoryLimit=2"
  if ! "${OC[@]}" patch deployment "$d" -n "${NAMESPACE}" --type=merge \
      -p '{"spec":{"revisionHistoryLimit":2}}'; then
    echo "FAILED to patch deployment/${d} (see error above)" >&2
    FAILURES=$((FAILURES + 1))
  fi
done

echo "--- 3. completed one-off load tests and their ConfigMaps ---"
for job in maas-latecomer uni27-loadgen-llmisvc uni28-loadgen-s1-long uni28-loadgen-s1-long-v2; do
  del_selector pod "job-name=${job}"
  del job "$job"
done
del configmap maas-latecomer
del configmap uni27-loadgen-llmisvc
del configmap uni28-loadgen-s1-long
del configmap maas-cacheprofile
# Deliberately NOT touched: cm/maas-loadgen and job/maas-loadgen -- the
# current benchmark run and the base run.sh that
# deploy/poc/15-fairness-benchmark.sh patches.

echo "--- 4. build residue ---"
del pod maas-epp-1-build
del pod maas-epp-3-build
del pod maas-epp-quay-publish-1-build
del build maas-epp-1
del build maas-epp-2
del build maas-epp-3
for suffix in ca global-ca sys-config; do
  del configmap "maas-epp-1-${suffix}"
  del configmap "maas-epp-3-${suffix}"
  del configmap "maas-epp-quay-publish-1-${suffix}"
done
# Deliberately NOT touched: build 4, pod/maas-epp-4-build, and
# cm/maas-epp-4-{ca,global-ca,sys-config} -- build 4's digest is what the GPU
# EPP currently runs (is/maas-epp must not be pruned either, for the same
# reason, and this script never names it).

echo "--- 5. inert Grafana dashboard ConfigMap ---"
# The dashboard JSON already lives in this repo at deploy/grafana-dashboard.yaml
# (confirmed byte-for-byte match of the panel titles on 2026-10-29), so
# deleting the cluster copy loses no unfinished work.
#
# This is also the object docs/runbook.md's "Load the fairness dashboard into
# the live Grafana" procedure names as its step-1 input (UNI-126). That
# procedure now reads deploy/grafana-dashboard.yaml directly instead, so this
# delete does not break it -- but keep that coupling in mind before changing
# this line. If the cluster copy is ever needed back for some other reason,
# `oc apply -f deploy/grafana-dashboard.yaml` recreates it byte-for-byte.
del configmap maas-fairness-dashboard

if [ "$FAILURES" -gt 0 ]; then
  echo "=== completed with ${FAILURES} failure(s) -- see FAILED lines above ===" >&2
  exit 1
fi
echo "=== done ==="
