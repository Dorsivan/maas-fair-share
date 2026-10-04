# Python prototype — FROZEN REFERENCE, NOT MAINTAINED

This directory is the original weighted-fair-queueing prototype: an **Envoy
`ext_proc` sidecar** written in Python, with a mock LLM and a `docker-compose`
harness. It is preserved for provenance. It is **not** the thing being built in this
repository, and it is not kept in sync.

Run it if you want to see the idea move. Do not extend it.

## What it is

```
wfq_service/wfq.py       WeightedFairQueue -- virtual-time scheduling, sliding window
wfq_service/server.py    ExternalProcessorServicer -- Envoy ext_proc gRPC servicer
wfq_service/config.py    group -> {weight, api_keys} mapping
config.yaml              premium 50 / standard 30 / free 20
envoy.yaml               Envoy wired to the ext_proc filter
mock_llm/server.py       stand-in model server
docker-compose.yaml      the whole thing, locally
```

Requests are classified by API key, admitted or queued by weighted fair queueing,
and token usage is read back from the response body (`usage.total_tokens`) to
advance each group's virtual time.

## What it proved

- **Virtual-time scheduling is the right core.** `virtual_time += tokens / weight`
  (`wfq.py:160`) is the service-tag rule, and it survives into the real design
  essentially unchanged.
- **Token usage is readable from the response body.** `server.py:127` parses
  `usage` out of the response and trues up the group's accounting. This is the
  mechanism the production design depends on.
- **Charging an estimate at admission is mandatory.** `DEFAULT_REQUEST_TOKEN_ESTIMATE`
  (`wfq.py:12`) exists because without it a tenant dispatches thousands of requests
  before the first completes. That finding is load-bearing in the new design.

## Why the architecture changed

The production version is **not a port of this**. It is a `FairnessPolicy` plugin
compiled into the llm-d Router (EPP), which sits below the gateway and already owns
the queueing machinery. That moves the component and deletes most of this code:

| Here | In the EPP | Why |
|---|---|---|
| `max_tokens_per_window: 1000000` (`config.py:27`) | *gone* | The EPP never asks "is the pool full?" — it asks "a slot freed, who's next?" No capacity constant is needed, so the design is scale-free. |
| `_can_admit_group` saturation gate (`wfq.py:138`) | *gone* | Work conservation is **structural**: `IterateQueues` only visits non-empty queues, so an idle pool can't throttle anyone. Writing a saturation check would be a bug. |
| queue, `max_queue_depth`, `_drain_loop` (`wfq.py:194`) | *gone* | Flow control already queues, ages, sheds, and expires. |
| 429 + `retry-after` (`server.py:194`) | *gone* | Hard ceilings belong to Kuadrant's `TokenRateLimitPolicy`. This layer divides contention; it does not reject. |
| sliding window, 10 sub-buckets (`wfq.py:85`) | exponential decay | Lazy, O(1), no bucket array, and composable. |
| API key → group | subscription ID → group | Identity arrives authenticated from Kuadrant; the plugin overwrites `FairnessID` rather than trusting a client header. |
| flat token count | weighted cost model | Input, output and cached tokens are priced differently, and the weights are calibrated rather than assumed. |

What carries over: virtual-time scheduling, group/weight config shape, reading
usage from the response body, and the provisional-charge insight.

## Running it

```bash
docker compose up --build
python test_wfq.py
```

`wfq_service/generated/` is gitignored — regenerate with
`wfq_service/compile_protos.sh` before running outside the container.
