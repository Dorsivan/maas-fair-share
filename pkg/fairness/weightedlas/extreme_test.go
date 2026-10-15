/*
Copyright 2026 The maas-fair-share Authors.
Licensed under the Apache License, Version 2.0.
*/

package weightedlas

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

// TestExtremeRatioLocal pins down WHERE a weight ratio can fail to materialise.
//
// On a live cluster the achieved token ratio between two continuously
// backlogged flows saturated near 1.8:1 no matter what the weights asked for:
// 2:1 produced 1.81, 3.25:1 produced 1.79, and 18:1 produced 1.82. The
// policy's own normalized_service showed it had correctly identified the
// imbalance (125,265 vs 13,229 at 18:1) and simply could not act on it.
//
// This test drives Pick directly, bypassing the flow controller's dispatch
// loop, and asserts the ratio is exact at all three. It passing while the
// cluster caps at 1.8 localises the ceiling to the DISPATCH PATH rather than
// to this plugin's arithmetic.
//
// It is kept as a regression test for two reasons. First, if a future change
// breaks weighting at large ratios, TestProportionality will not catch it --
// 2:1 happens to sit close to the observed cluster ceiling, so it passes in
// both a healthy and an unhealthy world. Second, if the dispatch-path cause
// is ever fixed, this is the statement of what the policy was always capable
// of.
func TestExtremeRatioLocal(t *testing.T) {
	t.Parallel()
	for _, tc := range []struct {
		name    string
		wa, wb  float64
		want    float64
	}{
		{"2:1 -- what TestProportionality covers", 2, 1, 2.0},
		{"3.25:1 -- the end-users:app1 ratio in deploy/", 65, 20, 3.25},
		{"18:1 -- deliberately beyond anything configured", 90, 5, 18.0},
	} {
		tc := tc
		t.Run(tc.name, func(t *testing.T) {
			t.Parallel()
			cfg := twoGroupConfig(tc.wa, tc.wb)
			cfg.Enforce = true
			// Off so the assertion is about ordering, not estimator quality.
			cfg.ProvisionalCharge = false
			p, clock := newTestPlugin(t, cfg)

			// Depth far exceeds the pick count: both flows stay backlogged for
			// the whole run, which is the only regime where a ratio is defined.
			band := newSimBand(p,
				&simFlow{id: "a-group", depth: 100000, promptIn: 500, output: 100},
				&simFlow{id: "b-group", depth: 100000, promptIn: 500, output: 100},
			)
			res := band.run(t, p, 40000, time.Millisecond, clock)

			got := res.tokens["a-group"] / res.tokens["b-group"]
			t.Logf("weights %.0f:%.0f  want %.2f  got %.3f", tc.wa, tc.wb, tc.want, got)
			assert.InEpsilon(t, tc.want, got, 0.05,
				"token ratio must track the weight ratio at any magnitude")
		})
	}
}
