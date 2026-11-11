### Runs

| phase | lane | verdict | max dev | dev app1 / app2 / eu | e2e p50 s | TTFT p50 s | TTFT p95 s | prio | non-200 / req | window |
|---|---|---|---|---|---|---|---|---|---|---|
| T1 | lane2 | FAIL | 12.7 | +7.8 / +4.9 / -12.7 | 29.6 / 57.3 / 14.1 | 27.94 / 53.96 / 12.64 | 62.39 / 113.57 / 36.65 | PRIORITY-OK | 8 / 5595 | 11:54:04-12:03:03 |
| T1 | lane3 | FAIL | 16.5 | +10.5 / +6.0 / -16.5 | 36.6 / 74.4 / 16.4 | 35.35 / 76.60 / 16.18 | 93.35 / 115.66 / 61.97 | PRIORITY-OK | 7 / 5131 | 11:54:00-12:02:28 |
| A2 | lane2 | FAIL | 10.7 | +7.0 / +3.7 / -10.7 | 41.4 / 78.0 / 16.4 | 41.49 / 73.42 / 16.52 | 76.54 / 115.34 / 39.30 | PRIORITY-OK | 5 / 5542 | 12:15:54-12:24:08 |
| A3 | lane3 | FAIL | 16.9 | +11.2 / +5.7 / -16.9 | 33.0 / 70.2 / 15.7 | 31.89 / 73.06 / 14.72 | 59.81 / 115.31 / 86.92 | PRIORITY-FAIL | 8 / 5283 | 12:26:39-12:33:51 |
| T2 | lane2 | PASS | 9.6 | +5.5 / +4.1 / -9.6 | 36.6 / 51.4 / 15.7 | 37.29 / 48.84 / 15.27 | 58.19 / 113.19 / 19.53 | N/A (share already PASS) | 2 / 5879 | 12:36:29-12:43:46 |
| T2 | lane3 | PASS | 4.0 | -1.1 / +4.0 / -2.9 | 41.9 / 56.2 / 14.3 | 42.60 / 57.24 / 13.93 | 120.00 / 120.00 / 34.80 | N/A (share already PASS) | 9 / 5353 | 12:36:21-12:42:44 |

### Comparisons

| comparison | max per-group deviation gap (pts) | e2e p50 ratio range | largest TTFT p50 diff (s) | max-dev diff (pts) |
|---|---|---|---|---|
| T1: lane2 vs lane3 (together) | 3.8 | 0.77–0.86 | -22.64 | -3.8 |
| T2: lane2 vs lane3 (together) | 6.8 | 0.87–1.09 | -8.40 | +5.6 |
| solo: lane2 vs lane3 | 6.2 | 1.04–1.26 | 9.60 | -6.2 |
| lane2: T1 vs alone | 2.0 | 0.71–0.86 | -19.45 | +2.0 |
| lane3: T1 vs alone | 0.7 | 1.05–1.11 | 3.55 | -0.4 |
| lane2: T2 vs alone | 1.5 | 0.66–0.96 | -24.57 | -1.1 |
| lane3: T2 vs alone | 14.1 | 0.80–1.27 | -15.81 | -12.9 |
| lane2: T1 vs T2 (repeat) | 3.1 | 0.81–1.11 | -9.36 | +3.1 |
| lane3: T1 vs T2 (repeat) | 13.7 | 0.87–1.32 | 19.36 | +12.6 |

### Together-phase load overlap

- T1: overlap 504s of a 543s combined window; start offset -4s (lane3 minus lane2)
- T2: overlap 375s of a 445s combined window; start offset -8s (lane3 minus lane2)

images: ['59cba032e091']
('A2', 'lane2') results/20261111T121440Z-uni231-aa-A2-lane2
('A3', 'lane3') results/20261111T122519Z-uni231-aa-A3-lane3
('T1', 'lane2') results/20261111T115246Z-uni231-aa-T1-lane2
('T1', 'lane3') results/20261111T115246Z-uni231-aa-T1-lane3
('T2', 'lane2') results/20261111T123509Z-uni231-aa-T2-lane2
('T2', 'lane3') results/20261111T123509Z-uni231-aa-T2-lane3
