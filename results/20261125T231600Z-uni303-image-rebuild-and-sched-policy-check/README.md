# UNI-303: EPP image rebuild + vLLM --scheduling-policy priority check

## Why this run exists

Before rewriting the docs/handoff for the internal environment, checked whether `main`'s
code (the SFQ priority stamp, UNI-293/UNI-299/UNI-300/UNI-306) actually matches what is
*deployed*. It did not: all six manifests, and the live cluster, were still pinned to the
UNI-220-era image (`sha256:c8a08820...`), built before the SFQ stamp existed. The live GPU
and CPU EPPs were additionally running two *different*, uncommitted digests
(`sha256:617509...`, `sha256:5ddee9a...`) that appear nowhere in this repository -- evidence
of manual cluster patches that were never written back.

## What was done

1. Rebuilt the EPP image from a clean clone of `origin/main` at `8968cc4` (UNI-306, the tip
   at the time), via `maas-epp-quay-publish-10` (BuildConfig, binary source, server-side
   Docker strategy -- no local podman needed). **Built from a fresh clone, not the shared
   working-tree checkout** — an earlier attempt (`maas-epp-quay-publish-9`) was discarded
   because that shared checkout had another agent's uncommitted edits to
   `pkg/fairness/weightedlas/` mixed in; its resulting digest
   (`sha256:97597dab...`) must not be used.
2. Published: `quay.io/rh-ee-dsivan/maas-fair-share@sha256:feba5e1d81143e3eee79cce12f0c8ad4a43fd3683b2b73e13befbdd52c6a4255`
   (floating tag `8968cc4`, resolve by digest).
3. Re-pinned all six manifests (`deploy/llmisvc.yaml`, `deploy/poc/{02-epp,05-llmisvc-sim,
   06-rhoai34-shape,07-vllm-cpu,09-vllm-gpu}.yaml`) to this digest.
4. Live-patched the GPU and CPU EPP scheduler deployments on the `maas-fairness-poc`
   namespace to the new digest (JSON-complete merge patch on the single-element container
   array, to avoid the known "merge patch drops the container's resource limits" trap --
   confirmed the `resources:` block survived on both). Both pods came up `1/1`, zero
   restarts, config loaded with no flag-parse errors, `PropagatePriority:false` confirmed in
   the EPP's own logged effective config.
5. **Independently confirmed UNI-292's finding at runtime** (UNI-292 itself was already
   resolved 2026-11-24 via a read-only grep of the GPU image's own vLLM source showing
   `SchedulerPolicy`/`PriorityRequestQueue` present -- this check did not re-decide that
   question, it corroborated it a different way): scaled the CPU vLLM workload
   (`maas-vllm-cpu`, which runs the same `vllm==0.24.0+rhaiv.9` family as the GPU path)
   from 0 to 1 replica with `--scheduling-policy priority` added to its args. vLLM logged
   it as an accepted non-default arg (`'scheduling_policy': 'priority'`), the model
   loaded, and the pod reached `1/1 Ready` serving `/health` and `/metrics`. **Yes, this
   build accepts the flag at runtime, matching the static finding.**
   Not tested: the GPU vLLM workload directly (see below), and whether vLLM actually
   *reorders* its queue by a stamped priority under contention (that needs
   `sfqPriorityStamp: true` and real contended traffic, out of scope for this check).
6. Restored the CPU workload to `replicas: 0` (its state before this check) -- the image
   digest and `--scheduling-policy priority` arg are left updated in both the live CR and
   the committed manifest, so the next scale-up gets them for free.
7. **Deliberately did not** add `--scheduling-policy priority` to the *live* GPU workload.
   All 6 cluster GPUs (2 each across `maas-fairness-poc`, `poc-maas-lane2`, `poc-maas-lane3`)
   are currently allocated with zero spare capacity, and changing the GPU workload's args
   triggers a rolling update that deadlocks at the default 25%/25% surge with no GPU free for
   the surge pod (a known, previously-documented trap). The manifest
   (`deploy/poc/09-vllm-gpu.yaml`) **is** updated with the flag for a *fresh* deploy, where
   there is no existing replica set to roll and therefore no deadlock risk. Applying it to
   *this* already-running GPU deployment is left as a follow-up to be done deliberately,
   during a window where the manual-scale-down procedure (deploy doc, "Rolling an existing
   GPU deployment") can be followed watching the rollout.

## Not proven by this run

- The GPU vLLm workload has not been restarted onto the new image or the new flag.
- No request was sent through the stamp path end-to-end (`sfqPriorityStamp` is still `false`
  everywhere, as shipped). This run proves the prerequisites are met, not that the stamp
  moves dispatch order on this cluster.
- The two stray, uncommitted digests found live before this check
  (`sha256:617509...` on the CPU EPP, `sha256:5ddee9a...` had been seen there before, and
  `sha256:7edc3705...` on a separate standalone `maas-epp` Deployment in the same namespace)
  were not traced to a source commit. They are gone now (overwritten by this check), so
  whatever they contained relative to `main` cannot be recovered.
