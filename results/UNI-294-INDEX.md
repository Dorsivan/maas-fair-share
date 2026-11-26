# UNI-294: SFQ priority stamp, live verification — evidence index

Headline result cited throughout `AIRGAP-HANDOFF.md` and `docs/design.md`: the SFQ
priority stamp holds the configured split to within **0.06-0.12 percentage points**,
live, on real contended traffic. Preserved here because the live session's working
directory was a worktree (`uni293-work`) that is not a permanent fixture, and this is
the only copy of the raw evidence behind the strongest claim in the documentation
rewrite (UNI-303).

Run with image tag `uni294-sfq-live` (not reproducible from a committed manifest as of
this writing — see AIRGAP-HANDOFF.md section 5.1 and "Not proven" item 12).

| Directory | Arm | Notes |
|---|---|---|
| `20261125T003317Z-uni294-arm1-baseline` | Arm 1 | Baseline, stamp present |
| `20261125T005702Z-uni294-arm2-run1` | Arm 2, run 1 | Early/short attempt (156K) |
| `20261125T010642Z-uni294-arm2-run1` | Arm 2, run 1 | Second short attempt (64K) |
| `20261125T010711Z-uni294-arm2-run1` | Arm 2, run 1 | Full run used in the headline number |
| `20261125T011507Z-uni294-arm2-run2` | Arm 2, run 2 | Repeat |
| `20261125T012201Z-uni294-arm2-run3` | Arm 2, run 3 | Repeat |
| `20261125T021428Z-uni294-arm3-isolation` | Arm 3 | **Control** — stamp disabled, same load. This is the run that proves the mechanism rather than the outcome: without it, a tight split could be coincidence rather than cause. |

The two short Arm 2 run-1 attempts are kept, not deleted, per this repo's standing
practice of preserving abandoned/short attempts alongside the run that superseded
them — see the top-level POC delivery standard's "honest scope reporting."

Each directory follows the same shape as other `results/` entries in this repository:
`fairness-report.{json,md}` for the scored verdict, `metrics-before.txt` /
`metrics-after.txt` / `metrics-timeseries.txt` for the raw Prometheus snapshots,
`epp-container.log` for the EPP's own log capture, and `client-request-summary.jsonl`
for the load generator's per-request record. No credential values are embedded —
request scripts reference `$KEYS_DIR`, not literal keys.
