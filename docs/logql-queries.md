# LogQL query pack (UNI-48 / D9)

Reference implementation against `docs/log-field-contract.md`. Every query
below targets the GPU EPP in the in-scope namespace:

```logql
{log_type="application",
 kubernetes_namespace_name="maas-fairness-poc",
 kubernetes_pod_name=~"maas-vllm-gpu-kserve-router-scheduler-.*"}
```

That selector is repeated in full in each query so one can be copy-pasted on
its own. Run against the LokiStack gateway's `application` tenant path exactly
as `docs/logging-install-spec.md` §7 documents (`$LOKI/api/logs/v1/application/loki/api/v1/query_range`,
bearer token, ingress CA bundle) — not re-derived here.

**Read `docs/log-field-contract.md` §1 first.** Every query below matches on
`body`, never `msg` — writing `msg="fairness state"` matches nothing, with no
error.

**Status.** These queries are written and reasoned against the field contract
and checked against this package's unit tests (which render log lines through
the same `funcr.NewJSON` shape the live `--zap-encoder json` output uses).
They have not been re-run against a live Loki instance for this ticket — see
`docs/log-field-contract.md` §6. `docs/logging-install-spec.md` §7 is the
live-verified example for the *previous* flight-recorder shape; use its
procedure (start a load run, poll while it's running, don't block on `oc wait`
first) to re-verify the shape below.

---

## 1. Who is being starved

The policy is healthy when `normalizedService` converges across backlogged
groups; a group that stays persistently low while others climb is starved,
one that stays persistently high is monopolizing. One flight-recorder line
per group (`docs/log-field-contract.md` §3.1) makes this a direct per-group
metric query instead of a parse-the-array-first query:

```logql
max_over_time(
  {log_type="application",
   kubernetes_namespace_name="maas-fairness-poc",
   kubernetes_pod_name=~"maas-vllm-gpu-kserve-router-scheduler-.*"}
    | json
    | body = "fairness state"
    | unwrap normalizedService [$__auto]
) by (group)
```

Chart this: a group whose line sits well below the others' while all are
backlogged (`inFlight > 0` on the same lines, or
`llm_d_epp_flow_control_queue_size{fairness_id=...} > 0` from Prometheus) is
the starved one. This is the same signal `docs/design.md`'s "Not converging"
alert uses, available here as a log-native query for a cluster that only has
Loki.

Prefer the Prometheus series (`..._normalized_service`,
`docs/design.md` §Metrics) for alerting — it is continuous, this is sampled at
`stateLogIntervalSeconds` and only while contended. Use this query to confirm
what the metric is showing, or when only Loki is available.

---

## 2. What failed to classify

```logql
{log_type="application",
 kubernetes_namespace_name="maas-fairness-poc",
 kubernetes_pod_name=~"maas-vllm-gpu-kserve-router-scheduler-.*"}
  | json
  | body = "subscription matched no fairness group; using catch-all"
```

Each line is one distinct subscription string's **first sighting** since the
EPP last restarted (`docs/log-field-contract.md` §3.2) — the field is
`subscription`, debug-only and bounded, never used as a label. Count
occurrences over time to see whether unmatched traffic is a one-off typo or
sustained (sustained means a real config gap, not a fluke):

```logql
count_over_time(
  {log_type="application",
   kubernetes_namespace_name="maas-fairness-poc",
   kubernetes_pod_name=~"maas-vllm-gpu-kserve-router-scheduler-.*"}
    | json
    | body = "subscription matched no fairness group; using catch-all" [1h]
)
```

Cross-check against `..._unmatched_subscriptions_total` (Prometheus) — that
counter increments on **every** unmatched request, not just first sightings,
so a growing counter with no new log lines means the same few subscriptions
are unmatched repeatedly, not that classification broke further.

---

## 3. What did the recorder see at time T

```logql
{log_type="application",
 kubernetes_namespace_name="maas-fairness-poc",
 kubernetes_pod_name=~"maas-vllm-gpu-kserve-router-scheduler-.*"}
  | json
  | body = "fairness state"
```

restricted to a window around T via `query_range`'s `start`/`end` (as
`docs/logging-install-spec.md` §7 already shows). Every group's row in that
window is one line; group the output by `tick` to reconstruct exactly one
recording pass rather than everything the recorder logged over the whole
window:

```logql
{log_type="application",
 kubernetes_namespace_name="maas-fairness-poc",
 kubernetes_pod_name=~"maas-vllm-gpu-kserve-router-scheduler-.*"}
  | json
  | body = "fairness state"
  | tick = "<tick value from one of the rows in the window>"
```

That second query's result set is the whole table as of that one pass — the
direct replacement for the old single-line-with-a-nested-array shape, without
needing to name and re-parse a `state.groups` field the way
`docs/logging-install-spec.md` §7 had to for the shape this ticket replaces.

Remember the gate: **an idle cluster emits nothing.** If T falls inside an
idle period (no two groups backlogged at once), this correctly returns zero
rows — that is not a broken collector, see `docs/log-field-contract.md` §3.1.

---

## 4. Which requests got a surprising decision

"Surprising" here means the estimator was badly wrong — a large gap between
what was charged at dispatch and what the request actually cost, which is
exactly `trueUpDelta` on the V(4) per-request tier line
(`docs/log-field-contract.md` §3.3):

```logql
{log_type="application",
 kubernetes_namespace_name="maas-fairness-poc",
 kubernetes_pod_name=~"maas-vllm-gpu-kserve-router-scheduler-.*"}
  | json
  | body = "per-request fairness tier"
  | trueUpDelta > 5000 or trueUpDelta < -5000
```

(Pick the threshold from `..._truing_error_tokens`'s histogram buckets in
`docs/design.md` §Metrics, not from the number above — `5000` is illustrative,
not a recommendation.) Each matching line carries `requestID`, so a surprising
decision is immediately traceable to one request rather than only visible in
the aggregate histogram.

A second kind of "surprising": the estimate was never trued up at all because
the response carried no usage block —

```logql
{log_type="application",
 kubernetes_namespace_name="maas-fairness-poc",
 kubernetes_pod_name=~"maas-vllm-gpu-kserve-router-scheduler-.*"}
  | json
  | body = "response completed with no usage block; check --enable-force-include-usage"
```

— which per `docs/design.md` §Metrics should be flat zero forever; any line
here at all is the regression this detector exists to catch.

**Both queries require data this GPU EPP does not currently produce for a
normal request** (see "Which of today's GPU gaps do not affect this query
pack" below): the first needs the V(4) tier, which cannot be enabled on
`maas-vllm-gpu-kserve-router-scheduler` today; the second fires on every
EPP regardless of `-v`, so it works today.

---

## 5. The headline query — given a request id off a response header, return its whole story

Per the board's 2026-10-19 direction: a caller has `x-request-id` from its own
response (`docs/log-field-contract.md` §4) and wants classification, charge,
true-up, and the flight-recorder tick it fell in.

**Step 1 — classification, charge, true-up, and the tick marker (requires the
V(4) tier):**

```logql
{log_type="application",
 kubernetes_namespace_name="maas-fairness-poc",
 kubernetes_pod_name=~"maas-vllm-gpu-kserve-router-scheduler-.*"}
  | json
  | body = "per-request fairness tier"
  | requestID = "<id from the x-request-id response header>"
```

Returns at most one line (the tier is sampled, so most requests will not have
one). When it hits: `group` is the classification, `estimateCharged` and
`trueUpDelta` are the charge and true-up, `recorderTick` is the closest
flight-recorder tick marker (`docs/log-field-contract.md` §3.3 — a recency
join, not an exact interval membership test), `band` and `enforcing` are the
remaining stable context fields.

**Step 2 — the flight-recorder tick that line names:**

```logql
{log_type="application",
 kubernetes_namespace_name="maas-fairness-poc",
 kubernetes_pod_name=~"maas-vllm-gpu-kserve-router-scheduler-.*"}
  | json
  | body = "fairness state"
  | tick = "<recorderTick value from step 1>"
```

Returns the whole group table as of the recorder's most recent pass before
this request settled — "what the recorder saw around the same time," per
§3.3's recency caveat, reassembled via the shared `tick` field from §3 above.

**This two-step query is demonstrated against the POC rig
(`deploy/poc/`), where `-v=4` can be set on the EPP container — it is not
achievable against `maas-vllm-gpu-kserve-router-scheduler` today, because the
V(4) tier cannot be turned on there** (`docs/log-field-contract.md` §3.3,
`docs/runbook.md` "On the KServe-managed scheduler"). Run step 1 against the
GPU EPP today and it will correctly return nothing for an ordinary request —
that is not a broken query, it is the gap stated plainly in
`docs/log-field-contract.md` §5.

**What *is* available on the GPU EPP today, for the same question:**

- The classification and queue time are already on the response the caller
  received (`x-maas-fairness-group`, `x-maas-fairness-queue-ms`) — zero
  queries needed, but only if the caller captured them at request time.
- If the request's subscription was this plugin's **first** sighting of an
  unmatched value, or if its response had no usage block, the matching query
  in §2 or §4 above will have a line carrying this exact `requestID`.
- Otherwise: nothing in these logs names this specific request. The
  flight-recorder lines around the response's timestamp (§3) show the group's
  tab at that time, which is time-correlated context, not an identified
  record of this one request.

Closing that last gap for the GPU/KServe-managed path is out of this ticket's
scope — see `docs/log-field-contract.md` §5.
