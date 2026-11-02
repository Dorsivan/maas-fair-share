# Read this first

This run's local capture (`15-fairness-benchmark.sh` + `18-soak-monitor.sh`,
both launched 2026-11-01T22:42:18Z) stopped writing at ~2026-11-01T23:24Z --
42 minutes into a configured 5700s (95-minute) run -- most likely the same
control-plane hiccup noted on the issue around that time. The `maas-loadgen`
Kubernetes Job and the EPP itself were unaffected and the Job ran to its full
duration, completing at 2026-11-02T00:17:38Z.

Consequence: `fairness-report.md`/`fairness-report.json` and
`memory-timeseries.txt` in this directory only cover the first 42 of 95
minutes. They are kept as-produced (real evidence of what the local tooling
captured, unedited) but **do not use them for this ticket's verdict** --
they understate the window by more than half.

**`full-run-backfill.md` / `full-run-backfill.json` cover the complete
95-minute run** and are the basis for the verdict recorded in
`docs/poc-results.md` and the closing comment on UNI-140. They were produced
by `deploy/poc/19-soak-prometheus-backfill.py`, which re-reads the same EPP
counters and platform memory/restart series from cluster-side Prometheus
(Thanos, via the live Grafana's anonymous-Viewer `/api/ds/query` proxy --
confirmed working in UNI-130) for the run's actual start/end timestamps, independent
of whether the local driver survived. See that script's module docstring for
the full rationale and its limitation (Thanos retention bounds how far back
this can reach).
