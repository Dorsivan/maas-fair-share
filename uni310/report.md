# UNI-310: the historical suite under the SFQ stamp — before/after

Runs from 2026-11-26 02:12Z to 08:31Z, on lanes 2 (`poc-maas-lane2`) and 3 (`poc-maas-lane3`). Every row ran on both lanes, one scenario per lane at a time. Lane 1 was not used: Khala has no write verbs there, and UNI-296 calibrates on it.

**Configuration compared with the UNI-218 baseline:**
- EPP image `d496a0cf…` with `sfqPriorityStamp: true`.
- vLLM `--scheduling-policy priority`.
- An extra `kv-cache-utilization-scorer` (weight 2.0).
- thr32 and halfLife 60 unchanged.

Before any result came in, each row was classified as discriminating, non-discriminating, noise floor, dynamics, or solo (`classification.md`, commit 6c61fba). Enforcement was confirmed on every row via `llm_d_epp_maas_fairness_enforcing` (1 before the row, 0 after). The driver also proved the ConfigMap restore with a server-side dry-run diff after every row.

## Headline

| group | rows | before: PASS | after: PASS |
|---|---|---|---|
| **discriminating** | 8 | 1 (F3-33/33/33) | **6** |
| weak (app3-joins, at the bar) | 1 | 1 | 1 |
| non-discriminating, uncontended, noise floor | 15 | all pass or uncontended | all pass or uncontended; **cannot speak to the policy** |
| dynamics (scored schedule-aware) | 6 | 5 | 6; harness changed, see below |
| solo / F1 | 2 | n/a | n/a |

**Fixed by the stamp, both lanes:** F3-40/20/40, app1-flood 256 and 128, uni165-dominant, uni165-pow2. These are the rows a worker-following scheduler cannot pass. They went from 12.5–31.3pt FAILs to 0.8–9.6pt PASSes.

**Not fixed:**
- **F3-98/1/1** fails at 39.7 and 41.8pt (it was 66.9). app1 gets 56–58% against a 98% target. Low-weight dispatches were almost never at the front of the queue. Filed as [UNI-314](/UNI/issues/UNI-314).
- **B5 open loop at 120%**, scored against the water-filled target: 12.2, 13.3, 9.7, 14.5 (3 of 4 FAIL, mean 12.4). The single pre-stamp run was 9.0. The split follows arrival rate (about 35/31/34 against an offered 33/33/33), not weight. Every new run lands above the old single run, but the old value is one sample and sits inside the new runs' 4.8pt spread. So: **not fixed, possibly slightly worse, regression not established.** Against the static weight target, as UNI-218 scored it, the row is ~33pt in both eras. No scheduler can reach that target, because end-users only offers ~33% of the load.

**Nothing in the discriminating group got worse, B5-120 aside.**

## Full table

`lane 2`/`lane 3` are r1. `extra runs` are the pre-registered near-bar repeats (r2) and the e1 re-run (r3). The number is max |deviation| in pts; the bar is 10.

| row | group | before (UNI-218/215) | lane 2 | lane 3 | extra runs | after verdict | Δ max dev | notes |
|---|---|---|---|---|---|---|---|---|
| f3-33-33-33 | disc | PASS 4.8 | PASS 1.5 | PASS 0.3 | — | PASS | -3.8 |  |
| f3-40-20-40 | disc | FAIL 12.5 | PASS 1.0 | PASS 0.8 | — | PASS | -11.6 |  |
| f3-98-1-1 | disc | FAIL 66.9 | FAIL 39.7 | FAIL 41.8 | — | FAIL | -26.2 |  |
| uni161-app1-flood-256 | disc | FAIL 31.3 | PASS 2.8 | PASS 9.6 | 5.5 | PASS | -25.4 |  |
| uni161-app1-flood-128 | disc | FAIL 28.6 | PASS 4.3 | PASS 2.2 | — | PASS | -25.4 |  |
| uni165-dominant | disc | FAIL 17.0 | PASS 3.4 | PASS 2.9 | — | PASS | -13.8 |  |
| uni165-pow2 | disc | FAIL 20.3 | PASS 2.7 | PASS 4.9 | — | PASS | -16.5 |  |
| b5-openloop-120pct | disc-wf | FAIL 9.0 (static 33.1) | FAIL 12.2 (static 34.7) | FAIL 13.3 (static 32.8) | 9.7, 14.5 | SPLIT | 3.4 |  |
| uni164-app3-joins | weak | PASS 2.0 | PASS 0.9 | PASS 1.4 | — | PASS | -0.9 |  |
| uni165-graded | non | PASS 4.2 | PASS 0.3 | PASS 0.2 | — | PASS | -4.0 |  |
| full-contention | non | PASS 4.1 | PASS 0.3 | PASS 0.4 | — | PASS | -3.7 |  |
| full-contention-2x | non | PASS 0.6 | PASS 0.2 | PASS 0.4 | — | PASS | -0.3 |  |
| a3-app2-idle | non | PASS 1.5 | PASS 0.1 | PASS 0.2 | — | PASS | -1.4 |  |
| a4-app1-idle | non | PASS 0.7 | PASS 0.0 | PASS 0.1 | — | PASS | -0.7 |  |
| a5-app2-trickle | non | PASS 2.1 | PASS 1.9 | PASS 1.9 | — | PASS | -0.2 |  |
| a6-below-capacity | non | UNCONTENDED 68.4 | UNCONTENDED 68.4 | UNCONTENDED 68.4 | — | UNCONTENDED | 0.0 |  |
| end-users-idle | non | PASS 0.0 | PASS 0.0 | PASS 0.0 | — | PASS | -0.0 |  |
| end-users-idle-2x | non | PASS 0.0 | PASS 0.0 | PASS 0.0 | — | PASS | -0.0 |  |
| b5-openloop-70pct | non | UNCONTENDED 68.4 | UNCONTENDED 68.4 | UNCONTENDED 68.4 | — | UNCONTENDED | 0.0 |  |
| b5-openloop-100pct | non | UNCONTENDED 68.4 | UNCONTENDED 37.3 | UNCONTENDED 68.4 | — | UNCONTENDED | -15.6 |  |
| uni165-equal | floor | PASS 0.3 | PASS 0.1 | PASS 0.1 | — | PASS | -0.1 |  |
| uni165-subset-3-idle | floor | PASS 0.1 | PASS 0.0 | PASS 0.0 | — | PASS | -0.1 |  |
| uni165-equal-2x | floor | PASS 0.2 | PASS 0.1 | PASS 0.1 | — | PASS | -0.1 |  |
| b1-cold-join | dyn | PASS 6.7 | PASS 0.8 | PASS 0.9 | — | PASS | -5.8 |  |
| b2-tenant-leaves | dyn | PASS 3.6 | PASS 0.4 | PASS 0.5 | — | PASS | -3.2 |  |
| b4-short-idle | dyn | PASS 5.3 | PASS 0.2 | PASS 0.2 | — | PASS | -5.1 |  |
| b4-long-idle | dyn | FAIL 15.6 | PASS 0.0 | PASS 0.0 | — | PASS | -15.6 |  |
| e1-epp-restart | dyn | PASS 4.7 | — | — | 0.6, 0.5 | PASS | -4.2 |  |
| e2-lose-replica | dyn | PASS 3.1 | PASS 0.1 | PASS 0.1 | — | PASS | -3.0 |  |
| a1-app2-alone | solo | PASS — | PASS — | PASS — | — | — | — |  |
| f1-shadow-mode-control | ctl | INFO 6.3 | INFO 0.1 | INFO 0.0 | — | PASS | -6.2 |  |

## Things to read before quoting this table

- **The non-discriminating PASSes are not evidence.** Their worker split is within 6.1pt of the weight split, below the bar. They tracked the weights within 0.0–0.4pt, but UNI-218 already put full-contention-2x at 20.7/11.1/68.2 before the stamp. So the closeness is not new, and it is not the stamp's doing.
- **Noise floor:** equal-weight rows came in at 0.0–0.1pt on both lanes.
- **Dynamics rows (b1, b2, b4, e1, e2) are non-discriminating on the split.** They are scored schedule-aware (UNI-222): each 10s window is scored against the weight share of the tenants active in it. On b4-long, the 207 active, contended group-windows average 1.8pt deviation; 3 exceed 10pt, all at phase edges. **b4-long-idle went from FAIL 15.6 to PASS 0.0, but the scorer also changed in between.** UNI-222/223 (babbd46) stopped scoring post-leave uncontended windows as full deviation. That improvement cannot be attributed to the stamp.
- **F1 (`enforce: false`) now scores 0.0–0.1pt; it was 6.3.** As predicted in classification.md, the stamp polices vLLM's queue whether or not `enforce` is on. So the lanes' "shadow mode" steady state is **not unpoliced** while the stamp is on.
- **The warm-up is excluded by construction.** Only contended service tokens are scored. Contended time was typically 50–66s of a 240s run, about 70% excluded. The per-row `contended_seconds` are in each report.
- **Settle-timeout hazard: does not apply here.** The longest group p95 in the suite was 98s (pow2), against `sfqSettleTimeoutSeconds: 900`. `sfq_unsettled_total` and `sfq_late_completions_total` are labelled counter vectors and never appeared, which means zero reaps. `sfq_stale_dropouts_total` was 0–2 per run.
- **Cost model:** `outputTokenWeight` is still 2.0 by assumption, pending UNI-296. The shares are weighted token cost, so absolute attribution carries that uncertainty. The relative before/after comparison uses the same weight in both eras.

## Lanes

- **Composition: interchangeable.** Lane 2 and lane 3 never disagreed by more than 6.8pt on any scored row (flood-256: 2.8 vs 9.6). B5-100 shows 37.3 vs 68.4, but both runs are UNCONTENDED, so the number means nothing. Most rows agree within 1pt.
- **Throughput: interchangeable over the suite.** Across 30 rows, lane 3 served a median of 0.998× lane 2's requests (range 0.70–1.03), with 0.91× the contended seconds. The anchor row is the 0.70 outlier: lane 3's replica on `ocp-gpu-worker-5` served only 29% of requests. My first update generalised from that single row. The suite does not support that.

## What I did not do, and what went wrong

- **flood-256 lane-3 repeat (r2) is invalid.** The harness could not fetch the loadgen log or read the live enforce value, and wrote no report. It is excluded, not counted. The row stands on 3 runs: 2.8, 9.6, 5.5.
- **e1-epp-restart was skipped on both lanes in r1.** vLLM was still 1/2 more than 3 minutes after e2 scaled a replica back. It was re-run as r3 on healthy lanes (0.6, 0.5), with the EPP pod really deleted at t+120s.
- **I did not re-run 98/1/1, and did not investigate it beyond the end-of-run SFQ metrics.** That is UNI-314.
- **`docs/poc-results.md` is not updated.** This report lives in `uni310/` and on the ticket.
- **The harness is at babbd46.** origin/main has since gained 68d8f6f (UNI-311: the per-window uncontended gate now also uses contended_seconds). That changes windowed scoring and might move dynamics-row window counts. I did not re-score.
- Both lanes were left at their 00-config steady state (default weights, `enforce: false`, vLLM 2/2), verified at 08:31Z.
