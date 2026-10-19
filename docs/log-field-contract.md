# Log field contract (UNI-48 / D9)

**Audience:** whoever points a different collector at these lines later. This
plugin's log output is one of the things the production logging team inherits
verbatim — they will not re-read `pkg/fairness/weightedlas`, they will read
this document. Field names below are the contract; renaming or dropping a
**stable** field is a breaking change for anyone who built a dashboard or
alert against it.

**Scope.** This contract describes `pkg/fairness/weightedlas`'s own log
output as emitted by the GPU EPP, `maas-vllm-gpu-kserve-router-scheduler`, in
namespace `maas-fairness-poc` — the in-scope target per the board's 2026-10-19
GPU-only direction on [UNI-19](/UNI/issues/UNI-19). The CPU-served deployments
and the simulator run the identical plugin code and ConfigMap
(`maas-epp-config`, referenced by both `deploy/poc/09-vllm-gpu.yaml` and
`deploy/llmisvc.yaml`), so the field shapes below apply there unchanged if
they are ever back in scope — but this document was written and checked
against the GPU path only.

---

## 1. The envelope — read this before writing a single query

The EPP emits **OTel-style JSON**, not the `{"level","ts","msg"}` zap shape the
`--zap-encoder json` flag name suggests. Sampled live from the GPU EPP on
2026-10-19 (see `docs/logging-install-spec.md` §7):

```json
{"severity_text":"DEBUG","timestamp":"2026-10-19T12:16:02.229624009Z",
 "caller":"controller/inferencepool_reconciler.go:49",
 "body":"Reconciling InferencePool","service.name":"llm-d-epp",
 "namespace":"maas-fairness-poc","severity_number":5}
```

| If you want... | ...the field is | not |
|---|---|---|
| the log message | `body` | `msg` |
| the level | `severity_text` | `level` |
| the time | `timestamp` | `ts` |

**This is the single biggest trap in writing a query against this EPP.** A
LogQL or Elastic query written as `msg="fairness state"` or `level="info"`
matches nothing, silently, forever — there is no error, the query is simply
empty. Every query in `docs/logql-queries.md` matches on `body`, never `msg`.

This is a property of `llm-d-router`'s logging setup, not of this plugin —
`--zap-encoder json` does not change it, and this plugin does not control the
envelope. Fields this plugin adds (everything in §3 below) are flattened
alongside `body`/`severity_text`/`timestamp` in the same JSON object, not
nested under it.

---

## 2. Stable vs debug-only

**Stable** fields are the ones a different collector, dashboard, or alert
should be able to key on without re-reading this plugin's source — renaming
or removing one is a breaking change.

**Debug-only** fields are diagnostic detail: useful for an engineer reading a
specific incident, but their presence, name, or type may change without
notice. Do not alert on them directly; the equivalent is almost always also a
Prometheus series (see `docs/design.md` "Production observability" §Metrics),
which is the authoritative source for alerting.

| Field | Stable? | Present on |
|---|---|---|
| `plugin` | Stable | every line |
| `requestID` | **Stable, required API** (board direction 2026-10-19, see [UNI-53](/UNI/issues/UNI-53)) | every request-scoped line |
| `traceId` | Stable, optional (present only when the inbound `traceparent` parsed) | every request-scoped line, when available |
| `group` | Stable | every line |
| `band` | Stable | every request-scoped line (see §4's caveat for why the flight recorder does not carry it) |
| `enforcing` | Stable | every line |
| `tick` | Stable | flight-recorder lines only |
| `recorderTick` | Stable | V(4) per-request tier line only |
| `estimateCharged`, `trueUpDelta` | Debug-only | V(4) per-request tier line only |
| `weight`, `attainedService`, `normalizedService`, `inFlight`, `provisionalCharge`, `ewmaOutputTokens`, `ewmaWarm` | Debug-only | flight-recorder lines only (each also has a Prometheus equivalent — see `docs/design.md` §Metrics) |
| `subscription` | Debug-only, client-controlled, bounded sample | the unmatched-subscription event line only |

`requestID` is never empty on a request-scoped line: it is `x-request-id`
from the inbound request, the framework's own backfilled id, or a
plugin-generated `generated-<hex>` fallback, in that preference order — see
`pkg/fairness/weightedlas/correlation.go`.

`band` is read directly off that request's own
`InferenceRequest.Objectives.Priority` — the flow-control priority band the
request was classified into, after [UNI-33](/UNI/issues/UNI-33)'s gateway-side
stripping of the client-settable objective header. On this cluster's
configuration there is exactly one priority band (`priority: 0` in
`deploy/poc/00-config.yaml`'s `flowControl.priorityBands`), so today every
line reads `"band":0`; the field exists so a future multi-band configuration
does not need a contract change, only a different number.

---

## 3. The three tiers

### 3.1 Flight recorder — periodic, one line per group

Emitted on `cfg.stateLogIntervalSeconds`'s cadence (`5` on the live GPU
config), **only while contention is recent** — an idle cluster emits zero
flight-recorder lines by design (`maxContendedStep`-gated; confirmed empty
across 24h of idle GPU/CPU logs in `docs/logging-install-spec.md` §7).

**This ticket's required fix.** Before this change, one line carried the
*whole* per-group table as a JSON array under a `state` key:

```json
{"body":"fairness state","plugin":"maas-fairness",
 "state":{"enforcing":true,"halfLifeSeconds":60,"groups":[{"name":"app1",...},{"name":"app2",...}]}}
```

A JSON array inside one log field does not unroll into a time series. Loki's
parameterless `| json` flattens nested **objects** with `_` and **skips
arrays entirely** (you only get the array back by naming it explicitly, as a
serialized string — see `docs/logging-install-spec.md` §7, "narrowed to one
group's normalized service"), and Elasticsearch's default dynamic mapping has
the same problem with an array of objects. Either way, a per-group trend —
app2's `normalizedService` climbing while app1's falls — was not directly
queryable; a query had to pull the array out as a string and re-parse it
downstream.

**The fix:** `logFlightRecorderTick`
(`pkg/fairness/weightedlas/plugin.go`) now emits one `"fairness state"` line
per configured group:

```json
{"body":"fairness state","plugin":"maas-fairness","tick":42,
 "group":"app1","enforcing":true,"weight":20,"attainedService":964268,
 "normalizedService":48213.4,"inFlight":12,"provisionalCharge":8600,
 "ewmaOutputTokens":180.3,"ewmaWarm":true}
{"body":"fairness state","plugin":"maas-fairness","tick":42,
 "group":"app2","enforcing":true,"weight":10,"attainedService":...}
```

`group`, `normalizedService`, `attainedService`, etc. are now first-class
fields a LogQL/Elastic query can select, filter, and chart on directly — see
"who is being starved" in `docs/logql-queries.md`.

`tick` is the field that answers "keeping a run/snapshot id so the lines of
one tick can be reassembled": every group's line from the same recording pass
shares one `tick` value (a per-plugin-instance monotonic counter, not a wall
clock), so `{tick="42"}` reconstructs the whole table as of that pass. See
`TestFlightRecorderLinesShareTickIDAcrossGroupsAndAdvanceBetweenTicks` in
`pkg/fairness/weightedlas/flight_recorder_test.go`.

**Why this tier has no `band` field.** `band` is meaningful per *request*: it
is read off that one request's own classification. A group's accounting
state (`groupState`) is not scoped to a band at all — it is shared across
whatever priority bands route requests into it, because this plugin's `Pick`
is a Flyweight singleton and `groupState` lives independent of
`PriorityBandAccessor`. On this POC's single-band configuration every group's
state is implicitly "band 0", but asserting a `band` field on this tier would
be encoding that single-band assumption into the contract rather than
describing what the code tracks. Recorded here as a documented gap, not
silently assumed away: a deployment that configures more than one priority
band would need `groupState` itself split per band before this field could
be added honestly.

**Not included on this tier:** `unmatchedSubscriptionsTotal` /
`recentUnmatchedSubscriptions` (present on the `DumpState()` debug-endpoint
JSON, `pkg/fairness/weightedlas/plugin.go`'s `dumpState` struct, which is
unaffected by this change). These are already a Prometheus counter
(`..._unmatched_subscriptions_total`) and a dedicated rate-limited log line
(§3.2) with its own `requestID` — duplicating the aggregate count into every
periodic tick added nothing a trend query needed.

### 3.2 Events, rate-limited

Two lines, each first-sighting-gated or otherwise naturally rare, both
request-scoped:

- **`"subscription matched no fairness group; using catch-all"`** — a
  subscription ID matched no configured group rule. Logged once per distinct
  subscription string (the value is client-controlled, so logging every
  occurrence is a log-flood primitive — see
  `pkg/fairness/weightedlas/plugin.go`'s `recordUnmatched`), carrying the
  `requestID`/`traceId` of whichever request's first sighting triggered it,
  plus `group` (always the catch-all name), `band`, and `enforcing`.
- **`"response completed with no usage block; check --enable-force-include-usage"`**
  (V(1)) — a response carried no usage block, so no true-up was possible.
  Carries `requestID`/`traceId`, `group`, `band`, `enforcing`. This is a
  regression detector (`docs/design.md` §Metrics,
  `..._requests_without_usage_total`): with
  `--enable-force-include-usage` set on every model server, this line and its
  counter should be flat zero forever.

### 3.3 V(4) per-request tier — sampled, time-boxed, off by default

`"per-request fairness tier"`, emitted from `ResponseBody` at settlement —
see `docs/design.md` "V(4) is off Pick's hot path" for the three independent
switches that gate it (config sample rate, config time box, process `-v`
flag). Fields:

```json
{"body":"per-request fairness tier","plugin":"maas-fairness",
 "group":"app1","band":0,"enforcing":true,
 "estimateCharged":512,"trueUpDelta":-38,"recorderTick":42,
 "requestID":"...","traceId":"..."}
```

`recorderTick` is new in this ticket: it echoes
`flightRecorderTick`'s current value at settlement — the most recently
*completed* flight-recorder tick, read with a single atomic load, never
written from this path. It is a **recency marker, not an exact interval
join**: a request can settle between two ticks, so the matching
`{tick="<recorderTick>"}` row is "the recorder's most recent view as of this
request," not a guarantee the request was in flight for that exact tick. See
"the whole story" query in `docs/logql-queries.md`.

**This is the only line that carries `estimateCharged` and `trueUpDelta`
together with a correlation id — and it is not available on the GPU EPP
today.** The config half of the gate (`requestTierV4SampleEvery` /
`requestTierV4TimeBoxSeconds` in `maas-epp-config`) applies equally to GPU and
CPU, since both reference the same ConfigMap. The verbosity half
(`-v=4` on the EPP container) does **not**: it can only be added to the
POC-rig Deployment's static args (`deploy/poc/02-epp.yaml`). The GPU
scheduler, `maas-vllm-gpu-kserve-router-scheduler`, is owned and templated by
the `LLMInferenceService` controller, which reverts manual Deployment edits —
see `docs/runbook.md` "On the KServe-managed scheduler," which already
records this as "an open problem, not a documented one." **This ticket does
not solve that problem**; it is restated here because it directly limits
what the field contract below can promise on the in-scope target. See §5.

---

## 4. Correlation id — required, stable API

Per the board's 2026-10-19 direction on this ticket: the correlation id is no
longer "where one is available," it is the field every request-scoped line
must carry, full stop. It already was, as of [UNI-53](/UNI/issues/UNI-53) —
this ticket changes its status from "good practice" to "contract": `requestID`
on a request-scoped line that omits it, or renames it, is a breaking change
against this document, not a refactor.

Resolution order (`pkg/fairness/weightedlas/correlation.go`,
`resolveCorrelation`): inbound `x-request-id` header, else the framework's own
already-resolved `InferenceRequest.RequestID` (itself backfilled from a
generated uuid by `llm-d-router`'s ext_proc server if the client sent
neither), else this plugin's own `generated-<hex>` fallback. Never empty.
`traceId` (the `trace-id` field of an inbound W3C `traceparent`) is included
only when present and well-formed — never generated, since a fabricated trace
id would not correlate with anything real.

The same id is echoed to the caller on the response (`x-request-id`,
alongside `x-maas-fairness-group` and `x-maas-fairness-queue-ms`) — see
`docs/design.md` "Per-request attribution." That response header is what lets
someone take a request id **out of a response** and look for its story in
these logs, which is exactly the shape of the board's headline query (§5
below and `docs/logql-queries.md`).

---

## 5. What this does and does not let you trace today

**Response headers are the primary, zero-log-volume "trace a request" path**
— `x-request-id`, `x-maas-fairness-group`, `x-maas-fairness-queue-ms`, read by
the caller at request time (`docs/design.md` "Per-request attribution",
[UNI-53](/UNI/issues/UNI-53)). This was a deliberate design choice to avoid
per-request log volume on `Pick`'s ~1ms hot path (`docs/design.md` "Logs").

**From logs, after the fact, on the in-scope GPU target today:** a
successfully classified, normally-completed request produces **zero**
plugin-specific log lines. §3.2's two event lines only fire on an exception
(unmatched subscription, missing usage block); §3.3's V(4) tier — the one
line that would carry `group`, `estimateCharged`, and `trueUpDelta` together
with the request's own `requestID` for an ordinary request — cannot be turned
on for `maas-vllm-gpu-kserve-router-scheduler` today (§3.3, `docs/runbook.md`
"On the KServe-managed scheduler").

So the honest answer to "given a request id taken off a response header,
return that request's whole story," run against the GPU EPP's current
configuration, is: **the classification and queue time are on the response
the caller already received; the charge and true-up are not retrievable from
GPU logs today for a request that didn't hit an exception path; the
flight-recorder ticks around the same time show the group's tab, not the
individual request.** `docs/logql-queries.md`'s headline query demonstrates
the full join as it works on the POC rig (where `-v=4` can be set), and
documents this exact gap for the GPU path rather than presenting a query that
would silently return nothing there.

Closing that gap — making per-request charge/true-up traceable by id on the
KServe-managed scheduler — is outside this ticket's scope (it is a
Deployment-templating problem, not a logging-contract one) and is recorded as
a backlog idea rather than attempted here.

---

## 6. What was and was not proven (this ticket)

**Proven:** the flight recorder's wire shape (one line per group, shared
`tick`), the field names and their stable/debug-only split, and that every
line this plugin emits now carries `band` and `enforcing` in addition to
whatever correlation fields it already had — verified by
`pkg/fairness/weightedlas/flight_recorder_test.go` and
`pkg/fairness/weightedlas/log_field_contract_test.go` against the real
`funcr.NewJSON` renderer the existing test suite already uses to match the
live `--zap-encoder json` shape.

**Not proven here (ticket scope was code + docs, no cluster/GPU session):**
that these exact lines survive collection and come back through a live LogQL
query. `docs/logging-install-spec.md` §7 captured a **raw pod log sample**
(`oc logs ... --tail=1`) of the old flight-recorder shape on 2026-10-19, and
wrote the LogQL that would query it — but re-checked directly against the
cluster while writing this ticket (`oc get lokistack -n openshift-logging`,
`oc get clusterlogforwarder -A`), neither the namespace nor either CRD exists.
`docs/logging-install-spec.md`'s own header already says this plainly —
**"Status: specification only. Nothing in this document has been applied."**
— the LogQL in that document and in `docs/logql-queries.md` has never actually
been run against a live Loki. The GPU scheduler pod itself was also not
running at the time of this check (`oc get pods -n maas-fairness-poc -l
kserve.io/component=router-scheduler` returned nothing) — consistent with the
GPU nodes being stopped between sessions, and a separate reason a live check
was not attempted here even if Loki had been installed.

**Not decided:** what logging stack production will actually run, or even
whether this POC cluster's own Loki install will proceed —
`docs/logging-install-spec.md` ([UNI-51](/UNI/issues/UNI-51)) is written and
committed but not yet applied by a cluster administrator. Per this ticket's
"open question, not blocking": the field contract above (§2–§4) is the
portable artifact regardless of which stack lands; `docs/logql-queries.md`
ships LogQL as the reference implementation because that is the stack this
POC's install spec targets, not because it has been confirmed running. A
production team on Elastic or any other collector re-implements against the
field names and the §1 envelope note, not against `docs/logql-queries.md`
itself. If `docs/logging-install-spec.md` is ever applied, its §7 should be
re-run against this ticket's new per-group shape, not the one it currently
documents.
