# UNI-247: over-offer bracket repeats (2x/3x/4x, three runs each)

Provenance for the UNI-247 section of `docs/poc-results.md`. Everything runs from the repo root.

- `batch.sh`: 3x `app1-flood-3x` then 3x `app1-flood-moderate` (4x), serial on instance 1, weights
  30/10/60, `ENFORCE_LIVE=true`. `batch.log` is its log.
- `2x-batch.sh`: 3x `app1-flood-2x`, same config. `2x-batch.log` is its log.
- `rebuild-report.sh <run-dir> <scenario> <label>`: rebuilds `fairness-report.{json,md}` offline
  from a run dir plus `batch.log`. This was needed for 3x rep 1-3 and 4x rep 1-2: the benchmark died
  before its report step (the UNI-224 `kvCacheUtilThreshold` grep under `pipefail`, fixed in
  `73c599e`). 4x rep 3 and all three 2x reps wrote their own reports.
- `summary.py`: one row per repeat (verdict, max deviation, per-group shares, limb, ledger), plus
  the n/mean/spread/sd for each point.
- `detail.py`: delivered tokens, app1:end-users p50 ratio, contended seconds, and non-200 tallies.

Both batch scripts restore weights to 20/10/65 at the end. They are kept as a record of what ran.
Re-running one starts real GPU load on instance 1, so check nothing else is using the pool first.

Checked 2026-11-12: re-running `rebuild-report.sh` on 3x rep 1 against current `main` reproduces
the committed report exactly, except for one added key, `"schedule_aware_groups": []`. That key
came from UNI-222's later report-script change (`6d7ce9c`). The committed reports are the originals.
