# UNI-152: D5, missing/empty identity header

Run: 2026-11-03T10:57:42Z, against `maas-vllm-gpu` (live SUT), via
`deploy/poc/16-loadgen-identity-variants.sh` (built by UNI-129, re-run fresh
under this ticket; no harness changes needed).

## Files

- `probe-output.txt` — raw stdout of the three-request probe (control,
  k8s-token to `/v1/chat/completions`, k8s-token to `/v1/models`).
- `epp-metrics-snapshot.txt` — `llm_d_epp_maas_fairness_dispatch_total` and
  `llm_d_epp_maas_fairness_unmatched_subscriptions_total` scraped directly
  from the GPU EPP's metrics ClusterIP immediately after the probe.

## Reading the evidence

`dispatch_total{fairness_id="end-users"}=1` is exactly the control request
(a real `sk-oai-` key against `end-user-alpha`) — the two k8s-token requests
(401, 403) left no trace in the EPP's dispatch counters at all, confirming
they never reached the EPP's classification logic, not merely that they
were classified as unclassified. `unmatched_subscriptions_total=0` backs
this the same way.

Pod restart counts, checked immediately after the probe (all `0`):

```
maas-vllm-gpu-kserve-74d8dd69bd-69gqk                    0
maas-vllm-gpu-kserve-74d8dd69bd-bbhg4                    0
maas-vllm-gpu-kserve-router-scheduler-575669c495-vww7h   0
```

See `docs/poc-results.md`'s `## UNI-152` section for the full writeup,
including why the setup as literally stated could not be produced on this
SUT and what that implies for the ticket's pass criteria.
