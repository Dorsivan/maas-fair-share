# Reconcile-timing diagnostic (UNI-158 follow-up probe)

Run separately from the benchmark, after it completed, with no loadgen or
other job running in the namespace -- an isolated check of how fast
`maas-controller` reconciles `maas-trlp-maas-vllm-gpu`'s `spec.limits` back
after a direct `oc patch`.

Patch applied (merge patch, same `field:` mechanism the benchmark's
`LIVE_SET_AT`/`LIVE_SET_TARGET`/`LIVE_SET_VALUE` wrapper uses):

```
$ oc patch tokenratelimitpolicies.kuadrant.io maas-trlp-maas-vllm-gpu \
    -n maas-fairness-poc --type=merge --patch-file=/tmp/trlp-test-patch.json
# patch-file body:
# {"spec":{"limits":{"models-as-a-service-app1-production-maas-vllm-gpu-tokens":
#   {"rates":[{"limit":12345,"window":"1m"}]}}}}
tokenratelimitpolicy.kuadrant.io/maas-trlp-maas-vllm-gpu patched
```

Before: `rates=[{"limit":100000000,"window":"1m"}]`, generation 13.

Polled every 1s for 20s immediately after the patch:

```
t+1s gen=14 rates=[{"limit":100000000,"window":"1m"}]
t+2s gen=14 rates=[{"limit":100000000,"window":"1m"}]
... (unchanged through t+20s, all gen=14, all reverted)
```

**Finding:** the controller reconciled the object back to
`limit:100000000` in under one second -- the very first poll already shows
the reverted value and the bumped `metadata.generation` (13→14, i.e. the
controller's own write, not ours re-read). No window of even a few seconds
exists during which a direct `spec.limits` edit survives. This explains why
the benchmark run immediately before this diagnostic (`LIVE_SET_AT=120`,
same patch mechanism, held nominally for the 240s "capped" phase) produced
zero 429s on app1: the live enforcement layer (Limitador, behind Kuadrant's
own TokenRateLimitPolicy controller) never saw the lowered value long
enough -- if at all -- to act on it.
