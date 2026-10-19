/*
Copyright 2026 The maas-fair-share Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package weightedlas

import (
	"context"
	"testing"
)

// BenchmarkPick measures the cost of the function the UNI-47 V(4) per-request
// tier does not touch. Pick runs on a ~1ms ticker (see docs/design.md "Logs"),
// so per-decision logging is out of scope there, always -- the V(4) tier logs
// from ResponseBody instead, once per request at settlement, never from Pick.
//
// Six contended groups keeps every candidate backlogged for the whole run (the
// regime IterateQueues actually visits under load), so this measures the
// newcomer-clamp and scoring loops at a realistic candidate-set size, not an
// idle band with nothing to compare.
//
// This file adds a benchmark; it does not change Pick's body (see the UNI-47
// diff: the only edits in plugin.go are the Plugin struct, ResponseBody, and
// two new unexported methods after dump() -- Pick itself is byte-for-byte
// unmodified). The cost of the V(4) tier's disabled path on Pick is therefore
// exactly zero, not merely small; this benchmark exists as a regression guard
// for Pick's own baseline, both now and if anyone is ever tempted to wire V(4)
// sampling into Pick directly.
func BenchmarkPick(b *testing.B) {
	cfg := testConfig()
	cfg.Enforce = true
	p, err := newPlugin("bench", cfg)
	if err != nil {
		b.Fatal(err)
	}

	band := newSimBand(p,
		&simFlow{id: "app1-production", depth: 1000, promptIn: 500, output: 100},
		&simFlow{id: "app2-batch", depth: 1000, promptIn: 500, output: 100},
		&simFlow{id: "end-user-1", depth: 1000, promptIn: 500, output: 100},
		&simFlow{id: "end-user-2", depth: 1000, promptIn: 500, output: 100},
		&simFlow{id: "end-user-3", depth: 1000, promptIn: 500, output: 100},
		&simFlow{id: "unclassified", depth: 1000, promptIn: 500, output: 100},
	)
	accessor := band.accessor()
	ctx := context.Background()

	b.ReportAllocs()
	b.ResetTimer()
	for range b.N {
		if _, err := p.Pick(ctx, accessor); err != nil {
			b.Fatal(err)
		}
	}
}
