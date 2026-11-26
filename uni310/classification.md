# UNI-310 row classification, written before any result

Written 2026-11-26 ~02:20Z, after both lane drivers launched and before the
first row finished. Each row's group is fixed by its sizing alone, not by
how it turns out.

**Rule (UNI-225).** A closed-loop row is *discriminating* when the offered
worker share and the weight share differ by at least the 10pt bar in some
group. Under FIFO a closed-loop tenant's token share tracks its share of
in-flight requests, which is its worker share. Below that gap, "follows the
weights" and "follows the workers" predict the same split, so a PASS there
says nothing about the policy.

**Shallow check (water-fill).** In closed loop, tenant *i* can hold at most
W_i running slots. The pool has S = 16 running slots (`--max-num-seqs 8` ×
2 replicas; that is a ceiling, and KV can only lower it). A tenant is
shallow if W_i < share_i × 16. **No closed-loop row in this suite is
shallow.** The tightest case is A6, where end-users has 26 workers against
a 10.9-slot entitlement. The static weight target is therefore the
water-filled target for every closed-loop row.

**Open loop (B5) is different.** Each tenant's demand is fixed by its
arrival rate, so the target is water-filled. With demand_i = offered rate_i
× mean cost per request_i, and C = total served cost rate in the run:
target_i = min(demand_i, the share the weights water-fill to it), with
capped surplus redistributed by weight. At 70% and 100% load nobody is
capped, so target = offered = 33/33/33, and FIFO passes too. Those rows are
**non-discriminating**. At 120% the equal-cost target is ≈ 40/20/40 against
FIFO's ≈ 33/33/33, a 13.3pt gap, so the row is **discriminating**. UNI-218
scored B5-120 against the static 21/10/68 target, which no scheduler can
reach because end-users only offers ~40% of capacity. I will report both
scorings for B5. The historical "-33pt inversion" partly reflects the wrong
target.

| row | weight % | worker % | gap | group |
|---|---|---|---|---|
| f3-33-33-33 | 33.3/33.3/33.3 | 16.7/16.7/66.7 | 33.3 | **discriminating** |
| f3-40-20-40 | 40/20/40 | 16.7/16.7/66.7 | 26.7 | **discriminating** |
| f3-98-1-1 | 98/1/1 | 16.7/16.7/66.7 | 81.3 | **discriminating** |
| uni161-app1-flood-256 | 30/10/60 | 72.7/9.1/18.2 | 42.7 | **discriminating** |
| uni161-app1-flood-128 | 30/10/60 | 57.1/14.3/28.6 | 31.4 | **discriminating** |
| uni165-dominant | 90/2×5 | 53.1/9.4×5 | 36.9 | **discriminating** |
| uni165-pow2 | 50.8/25.4/12.7/6.3/3.2/1.6 | 26.6/14.7×5 | 24.2 | **discriminating** |
| b5-openloop-120pct | water-filled ≈40/20/40 | offered 33/33/33 | ≈13.3 | **discriminating** (water-filled) |
| uni164-app3-joins | 30/10/60 post-join (75/25 pre) | 37.5/12.5/50 (75/25 pre) | 10.0 post, 0.0 pre | **weak**: at the bar, post-join only |
| uni165-graded | 40/20/15/10/10/5 | 31.9/13.6×5 | 8.6 | non-discriminating |
| full-contention | 21.1/10.5/68.4 | 16.7/16.7/66.7 | 6.1 | non-discriminating (lane anchor) |
| full-contention-2x | same | same | 6.1 | non-discriminating |
| a3 / a4 / a5 | = | = | 0.0 | non-discriminating (sized to the weights) |
| a6-below-capacity | 21.1/10.5/68.4 | 15.8/15.8/68.4 | 5.3 | non-discriminating; designed uncontended |
| end-users-idle, -2x | 66.7/33.3 | 66.7/33.3 | 0.0 | non-discriminating |
| uni165-equal, subset-3-idle, equal-2x | equal | equal | 0.0 | **noise floor** (equal weights + equal load) |
| b5-openloop-70pct / 100pct | water-filled = offered | 33/33/33 | 0.0 | non-discriminating |
| b1, b2, b4-short, b4-long, e1, e2 | full-contention sizing | | 6.1 | non-discriminating on the split. These are dynamics rows, scored schedule-aware (UNI-222) |
| a1-app2-alone | solo | | n/a | unscorable (solo carve-out) |
| f1-shadow-mode-control | 21.1/10.5/68.4 | 16.7/16.7/66.7 | 6.1 | **no longer a negative control** (see below) |

**F1 under the stamp.** `weights.go:154` says `sfqPriorityStamp` is
"Independent of Enforce: that switch governs the EPP's own pick, this one
governs vLLM's." With the stamp on and `enforce: false`, vLLM still orders
its queue by weighted share. F1 therefore cannot serve as an "unpoliced"
baseline any more. Its sizing is non-discriminating anyway (6.1pt), so it
cannot show the difference either way. The same fact means the lanes'
steady-state "shadow mode" is not unpoliced while the stamp is on.

**Pass bar:** 10pt max |deviation|, as in the report. **Near-bar:** any
discriminating row with max |dev| in 5-15pt, or a lane-2/lane-3
disagreement > 5pt, gets a third run before I call a verdict.

**Warm-up exclusion.** The harness scores only contended service tokens
(`contended_service_tokens_total`), so the uncontended FIFO prefix is
excluded by construction rather than by a fixed request count. I report
contended_seconds per row so the excluded share is visible.
