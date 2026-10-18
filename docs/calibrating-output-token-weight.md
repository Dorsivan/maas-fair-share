# Calibrating `outputTokenWeight`

`outputTokenWeight` is the only number in the configuration that is a
**measurement of your hardware**, not a policy choice. It ships as `2.0`,
which is a convention with no physical basis, and it must be measured per
environment.

This document is the procedure.

## What the number is

The cost model charges each request:

```
cost = inputTokenWeight x (prompt - cached)
     + cachedInputTokenWeight x cached
     + outputTokenWeight x output
```

`outputTokenWeight` is **how much more expensive one generated token is than
one prompt token, on your hardware, for your model, at your batch size.**

It is not a billing preference. Price output tokens too cheaply and a
decode-heavy tenant quietly consumes more of the GPU than its weight allows,
while prefill-heavy tenants are starved; price them too dearly and the reverse.
Either way the configured floors stop meaning what they say.

## Why it is not 2.0, and why it is not transferable

2.0 is folklore borrowed from commercial API pricing (typically 3-5x). It has
no mechanical basis: **prefill and decode cost roughly the same FLOPs per
token.** The real ratio is an *efficiency* ratio, and it comes from how
differently the two phases use the hardware:

- **Prefill** processes the whole prompt as one large matrix multiply. It
  saturates compute and is highly parallel.
- **Decode** produces one token per step, and every step must re-read the
  entire model's weights plus the batch's KV cache from memory. It is
  **memory-bandwidth bound**, and the per-token cost falls as batch size rises
  because the weight read is amortised across the batch.

So the ratio is approximately

```
outputTokenWeight ~ (prefill tokens/sec) / (decode tokens/sec)
```

and it moves with **every one of these**:

| Changing this | Moves the ratio because |
|---|---|
| **GPU model** (A100 -> H100 -> H200) | compute and memory bandwidth scale differently; HBM generation matters most for decode |
| **Model size / architecture** | weight-read volume per decode step; GQA/MQA cut KV traffic sharply |
| **Quantisation** (FP16 -> FP8 -> INT4) | shrinks the weight read, which helps decode far more than prefill |
| **`--max-num-seqs` / batch size** | decode amortises weight reads across the batch; prefill barely cares |
| **Tensor parallelism** | adds collective communication per decode step |
| **vLLM version** | chunked prefill, CUDA graphs and scheduler changes all shift it |
| **Typical sequence length** | long contexts make KV reads dominate decode |

Plausible range is roughly **5-20x** at realistic batch sizes. If your
measurement lands near 2.0, be suspicious: check that both runs actually
saturated the pool.

**Re-measure whenever any row above changes.** A ratio measured on an A100 does
not describe an H200, and the number does not survive a model swap.

## The procedure

Two saturating runs against an **otherwise idle pool**, varying only the shape
of the data.

### Prerequisites

- The pool genuinely idle. Any other tenant's traffic corrupts both numbers.
- A **single** model-server replica, or divide by replica count consistently.
  Mixed replica counts between the runs invalidate the comparison.
- Fairness enforcement irrelevant here: this measures the *server*, not the
  policy. Run with `enforce: false` to be sure the EPP is not reordering.

### Run A — prefill-dominated

```
prompt_tokens  = 4096
output_tokens  = 1
```

One output token means essentially all the work is prefill. Record
**prompt tokens/sec** sustained at saturation.

### Run B — decode-dominated

```
prompt_tokens  = 64
output_tokens  = 1024
```

A negligible prompt means essentially all the work is decode. Record
**output tokens/sec** sustained at saturation.

### Compute

```
outputTokenWeight = (prefill tokens/sec from A) / (decode tokens/sec from B)
```

### Where to read the numbers

Prefer the **server's own metrics** over the client's. Client-side figures fold
in queueing and any shedding, which is exactly what you are trying to exclude:

```promql
rate(vllm:prompt_tokens_total[2m])        # run A numerator
rate(vllm:generation_tokens_total[2m])    # run B numerator
```

Confirm both runs actually saturated before trusting either:

```promql
vllm:num_requests_waiting > 0             # a real queue existed
vllm:num_requests_running                 # plateaued, not still climbing
```

If `num_requests_waiting` is zero you measured an idle server and the ratio is
meaningless.

## Running it here

`deploy/poc/04-loadgen.yaml` sends a fixed shape, so for calibration either
drive `guidellm` directly (it parameterises the data shape, which is why the
plan specifies it):

```
--data kind=synthetic_text,prompt_tokens=4096,output_tokens=1     # A
--data kind=synthetic_text,prompt_tokens=64,output_tokens=1024    # B
```

or copy `deploy/poc/10-cache-profile.yaml`, which already demonstrates
per-tenant prompt shaping, and set `max_tokens` per run.

Two environment-specific traps, both learned the hard way in this POC:

1. **Offer enough load.** Both runs must saturate. Under-offered load measures
   the generator, not the server. See the sizing note in
   `deploy/poc/04-loadgen.yaml`.
2. **Check the gateway is `1/1`, not merely `Running`.** A gateway whose
   istio-proxy has lost its xDS connection serves nothing while looking
   healthy, and the run silently returns no data.

## After measuring

**Changing `outputTokenWeight` invalidates the group weights.** It changes the
unit the floors are denominated in, so a tenant mix that was balanced at 2.0
will not be at 12.0. Re-derive the weights in the same change, and re-read the
per-group traffic-shape table before trusting them.

Then check whether the estimator still holds up. `outputTokenWeight` multiplies
the one quantity the plugin *estimates* rather than measures at dispatch, so
raising it amplifies estimator error proportionally. Watch:

```promql
llm_d_epp_maas_fairness_truing_error_tokens    # should stay symmetric around 0
```

A persistent per-group bias after recalibration means the output estimate needs
work (`max_tokens` capping, or per-group EWMA warm-up) before the new weight
can be trusted.

## Recording the result

Note alongside the value: GPU model, model name and quantisation,
`--max-num-seqs`, tensor-parallel size, vLLM version, and the two measured
token rates. Without those the number is unreproducible and nobody will know
when it has gone stale.

| field | example |
|---|---|
| GPU | NVIDIA A100 80GB PCIe |
| model | Qwen2.5-7B-Instruct, FP16 |
| `--max-num-seqs` | 8 |
| TP size | 1 |
| vLLM | (from the server's `/version`) |
| prefill tok/s (A) | *measured* |
| decode tok/s (B) | *measured* |
| **outputTokenWeight** | **A / B** |
