#!/bin/bash
# Final step: turn MaaS on in the DataScienceCluster.
#
# RHOAI 3.4 uses spec.components.kserve.modelsAsService.managementState.
# NOTE the upstream opendatahub docs show a DSC v2 field
# (spec.components.aigateway.modelsAsAService) -- that is NOT what this
# product version reads. Confirm against the live object before copying either:
#   oc get dsc -o jsonpath='{.items[0].spec.components.kserve}'
#
# Everything this depends on must already be in place, or MaaS comes up
# Degraded: Kuadrant CR (01), Authorino TLS (02), the database secret (03),
# the gateway (04), and User Workload Monitoring.
set -euo pipefail
DSC=$(oc get dsc -o jsonpath='{.items[0].metadata.name}')
oc patch dsc "$DSC" --type=merge -p \
  '{"spec":{"components":{"kserve":{"modelsAsService":{"managementState":"Managed"}}}}}'
