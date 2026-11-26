# UNI-294: SFQ priority stamp, live verification — evidence index

Headline result cited throughout `AIRGAP-HANDOFF.md` and `docs/design.md`: the SFQ
priority stamp holds the configured split to within **0.06-0.12 percentage points**,
live, on real contended traffic. Preserved here because the live session's working
directory was a worktree (`uni293-work`) that is not a permanent fixture, and this is
the only copy of the raw evidence behind the strongest claim in the documentation
rewrite (UNI-303).

Run with image tag `uni294-sfq-live` (not reproducible from a committed manifest as of
this writing — see AIRGAP-HANDOFF.md section 5.1 and "Not proven" item 12).

**Configs actually used, read from each run's own `.enforce-patch.json`** (do not trust
the directory names alone — they are session labels, not a verified experiment design):

| Directory | Arm | `sfqPriorityStamp` | `enforce` | Max \|deviation\| | Notes |
|---|---|---|---|---|---|
| `20261125T003317Z-uni294-arm1-baseline` | Arm 1 | **absent (= false)** | false | 31.8 pts | Stamp off. Scenario is `equal-workers-control` (equal offered worker counts per tenant), so a large miss here is the *expected* result with the stamp off, not a defect — see AIRGAP-HANDOFF.md section 9, item 1. |
| `20261125T005702Z-uni294-arm2-run1` | Arm 2, run 1 | — | — | — | Early/short attempt (156K), superseded by the 010711Z run below |
| `20261125T010642Z-uni294-arm2-run1` | Arm 2, run 1 | — | — | — | Second short attempt (64K), also superseded |
| `20261125T010711Z-uni294-arm2-run1` | Arm 2, run 1 | **true** | false | **0.057 pts** | Full run used in the headline number. Same `equal-workers-control` scenario as Arm 1 -- equal offered worker counts, but the observed split still tracks the **configured weights**, not the equal worker counts. That is the strong form of evidence: the split follows the policy, not the offered load shape. |
| `20261125T011507Z-uni294-arm2-run2` | Arm 2, run 2 | true | false | **0.112 pts** | Repeat |
| `20261125T012201Z-uni294-arm2-run3` | Arm 2, run 3 | true | false | **0.120 pts** | Repeat |
| `20261125T021428Z-uni294-arm3-isolation` | Arm 3 | **true** | false | 32.5 pts | Same EPP-side config as Arm 2 (stamp on), but misses the target by as much as Arm 1 (stamp off entirely). **The config captured in this run's artifacts does not record the vLLM container's own `--scheduling-policy priority` flag**, so the most likely explanation -- that vLLM was not running in priority mode for this arm, isolating that the stamp alone (without vLLM honouring it) does nothing, exactly as design.md's "three non-negotiables" require -- is inferred from the design's documented mechanism, not independently confirmed from a deployment snapshot in this evidence. Treat the *contrast* (large miss despite the EPP-side stamp being on) as solid; treat the specific causal explanation as the best available inference, not a verified fact. |

**Reading the result:** Arm 1 and Arm 3 both miss the weighted target by ~32 points
despite one having the stamp off entirely and the other having it on at the EPP;
Arm 2's three repeats, same scenario, land within 0.06-0.12 points. The only
difference `.enforce-patch.json` records between Arm 2 and Arm 3 is none at all on the
EPP side -- so whatever actually changed between them was outside the EPP's own config,
most plausibly the vLLM scheduling flag. This evidence proves the headline number is
real and reproducible (three repeats, tight spread) and is *consistent with* (but does
not, from these artifacts alone, prove) the specific mechanism described in
`docs/design.md`.

The two short Arm 2 run-1 attempts are kept, not deleted, per this repo's standing
practice of preserving abandoned/short attempts alongside the run that superseded
them — see the top-level POC delivery standard's "honest scope reporting."

Each directory follows the same shape as other `results/` entries in this repository:
`fairness-report.{json,md}` for the scored verdict, `metrics-before.txt` /
`metrics-after.txt` / `metrics-timeseries.txt` for the raw Prometheus snapshots,
`epp-container.log` for the EPP's own log capture, and `client-request-summary.jsonl`
for the load generator's per-request record. No credential values are embedded —
request scripts reference `$KEYS_DIR`, not literal keys.
