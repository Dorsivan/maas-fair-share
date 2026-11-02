# Soak run full-window backfill

Recomputed from cluster-side Prometheus (Thanos via Grafana anonymous Viewer proxy, UNI-130 mechanism) because the local capture driver stopped before the run finished. Covers the full window: `2026-11-01T22:42:18Z` to `2026-11-02T00:17:38Z` (5720s).

**Windowed-share verdict: PASS** (threshold 10.0 pts; max |deviation| 6.19 pts at window (14, 4200.0, 4500.0, 'app1'))

| window start (s) | window end (s) | app1 obs% (dev) | app2 obs% (dev) | end-users obs% (dev) |
|---|---|---|---|---|
| 0 | 300 | 17.4% (-3.7) | 14.4% (+3.9) | 68.2% (-0.2) |
| 300 | 600 | 16.2% (-4.9) | 14.3% (+3.8) | 69.5% (+1.1) |
| 600 | 900 | 16.9% (-4.2) | 13.4% (+2.8) | 69.8% (+1.3) |
| 900 | 1200 | 17.7% (-3.3) | 13.9% (+3.4) | 68.3% (-0.1) |
| 1200 | 1500 | 16.5% (-4.6) | 14.1% (+3.6) | 69.4% (+1.0) |
| 1500 | 1800 | 16.5% (-4.6) | 12.8% (+2.2) | 70.8% (+2.4) |
| 1800 | 2100 | 17.2% (-3.8) | 13.3% (+2.8) | 69.5% (+1.1) |
| 2100 | 2400 | 16.4% (-4.7) | 15.2% (+4.6) | 68.5% (+0.0) |
| 2400 | 2700 | 17.4% (-3.6) | 13.2% (+2.7) | 69.4% (+0.9) |
| 2700 | 3000 | 17.9% (-3.1) | 13.8% (+3.3) | 68.3% (-0.2) |
| 3000 | 3300 | 15.6% (-5.4) | 13.2% (+2.7) | 71.2% (+2.8) |
| 3300 | 3600 | 17.9% (-3.2) | 15.0% (+4.4) | 67.2% (-1.3) |
| 3600 | 3900 | 16.9% (-4.2) | 13.9% (+3.4) | 69.2% (+0.8) |
| 3900 | 4200 | 17.4% (-3.6) | 14.4% (+3.8) | 68.2% (-0.2) |
| 4200 | 4500 | 14.9% (-6.2) | 14.1% (+3.6) | 71.0% (+2.6) |
| 4500 | 4800 | 16.8% (-4.2) | 13.7% (+3.2) | 69.5% (+1.0) |
| 4800 | 5100 | 16.7% (-4.3) | 13.8% (+3.3) | 69.5% (+1.0) |
| 5100 | 5400 | 17.1% (-3.9) | 14.3% (+3.8) | 68.6% (+0.2) |
| 5400 | 5700 | 16.8% (-4.3) | 13.4% (+2.8) | 69.9% (+1.5) |

## Whole-run totals

| group | delivered tokens (delta) | observed % | expected % | deviation (pts) |
|---|---|---|---|---|
| app1 | 15643042 | 16.85% | 21.05% | -4.20 |
| app2 | 12899952 | 13.90% | 10.53% | +3.37 |
| end-users | 64291880 | 69.25% | 68.42% | +0.83 |

## Memory

- container working-set (container=main): 96 samples, 313.4MB (start) -> 316.8MB (end), range [289.0, 318.0]MB
- EPP process_resident_memory_bytes: 96 samples, 322.2MB (start) -> 324.7MB (end), range [298.4, 326.5]MB

## Restarts

- `kube_pod_container_status_restarts_total` samples across the window: [0]

## Flow-control outcomes (shedding check)

Per `deploy/epp-config.yaml`'s own comment: a non-zero/growing evicted outcome during a run means that run measured shedding, not the fairness policy.

- `Dispatched`: 154830 -> 223900 (delta 69070)
- `EvictedContextCancelled`: 111 -> 111 (delta 0)

