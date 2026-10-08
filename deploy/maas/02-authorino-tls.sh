#!/bin/bash
# Authorino TLS bootstrap -- RHOAI MaaS guide section 1.4.
#
# MaaS requires TLS between the Gateway/Envoy and Authorino. These are
# imperative patches rather than manifests because they mutate objects the
# Kuadrant operator owns; re-applying a full YAML would fight the operator.
#
# Idempotent: every step uses --overwrite or a merge patch.
set -euo pipefail

# 1. Ask the service-ca-operator to mint a serving cert for Authorino.
oc annotate service authorino-authorino-authorization \
  -n kuadrant-system \
  service.beta.openshift.io/serving-cert-secret-name=authorino-server-cert \
  --overwrite

# 2. Point Authorino's listener at that cert.
oc patch authorino authorino -n kuadrant-system --type=merge --patch '
{
  "spec": {
    "listener": {
      "tls": {
        "enabled": true,
        "certSecretRef": { "name": "authorino-server-cert" }
      }
    }
  }
}'

# 3. Trust the cluster service CA, so Authorino can validate the peers it talks
#    to. The bundle is populated by the service-ca-operator.
oc -n kuadrant-system set env deployment/authorino \
  SSL_CERT_FILE=/etc/ssl/certs/openshift-service-ca/service-ca-bundle.crt \
  REQUESTS_CA_BUNDLE=/etc/ssl/certs/openshift-service-ca/service-ca-bundle.crt

# Step 4 of the guide -- annotating the Gateway with
# security.opendatahub.io/authorino-tls-bootstrap=true -- lives in
# 03-gateway.yaml, since the Gateway is a declarative resource we own.
