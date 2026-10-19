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
	"encoding/json"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// logFieldNumber is logFieldString (attribution_test.go) for a numeric field --
// funcr.NewJSON renders every Go number as a JSON number, never a string.
func logFieldNumber(t *testing.T, line, key string) float64 {
	t.Helper()
	var obj map[string]any
	require.NoError(t, json.Unmarshal([]byte(line), &obj))
	v, ok := obj[key]
	require.True(t, ok, "field %q not present in log line: %s", key, line)
	n, ok := v.(float64)
	require.True(t, ok, "field %q is not a number in log line: %s", key, line)
	return n
}

func linesContaining(lines []string, substr string) []string {
	var out []string
	for _, l := range lines {
		if strings.Contains(l, substr) {
			out = append(out, l)
		}
	}
	return out
}

// Done-when: "One line per group ... is merged, with a test asserting the
// shape." The flight recorder used to emit the whole table as a single line
// with a nested `groups` array, which does not unroll into a time series in
// Loki or Elasticsearch (see docs/logging-install-spec.md §7 and
// docs/log-field-contract.md). This asserts the replacement: one "fairness
// state" line per configured group, each with its own `group` field a query
// can select on directly.
func TestFlightRecorderEmitsOneLinePerGroup(t *testing.T) {
	t.Parallel()
	p, clock := newTestPlugin(t, testConfig()) // app1, app2, end-users, unclassified
	ctx, lines := capturingContext()
	p.lastContendedUnixNano.Store(clock.now().UnixNano())

	p.logFlightRecorderTick(ctx)

	stateLines := linesContaining(*lines, "fairness state")
	require.Len(t, stateLines, 4, "expected exactly one line per configured group, got: %v", *lines)

	seen := make(map[string]bool, 4)
	for _, l := range stateLines {
		seen[logFieldString(t, l, "group")] = true
		// The old shape nested the whole table under a "state" key; the new
		// shape has no such field at all.
		assert.NotContains(t, l, `"state"`, "must not carry the old nested-table field: %s", l)
	}
	for _, name := range []string{"app1", "app2", "end-users", "unclassified"} {
		assert.True(t, seen[name], "expected a line for group %q, got: %v", name, stateLines)
	}
}

// Done-when (reassembly): "keeping a run/snapshot id so the lines of one tick
// can be reassembled." Every line from one recording pass must share a `tick`
// value, and a later pass must use a different one.
func TestFlightRecorderLinesShareTickIDAcrossGroupsAndAdvanceBetweenTicks(t *testing.T) {
	t.Parallel()
	p, clock := newTestPlugin(t, testConfig())
	ctx, lines := capturingContext()
	p.lastContendedUnixNano.Store(clock.now().UnixNano())

	p.logFlightRecorderTick(ctx)
	firstTick := len(*lines)
	require.NotZero(t, firstTick)
	tick1 := logFieldNumber(t, (*lines)[0], "tick")
	for _, l := range *lines {
		assert.Equal(t, tick1, logFieldNumber(t, l, "tick"), "every line in one tick must share the same id: %s", l)
	}

	p.logFlightRecorderTick(ctx)
	tick2 := logFieldNumber(t, (*lines)[len(*lines)-1], "tick")
	assert.NotEqual(t, tick1, tick2, "a later recording pass must use a different tick id")
}

// Done-when (field contract): every flight-recorder line carries `group` and
// `enforcing` -- the stable fields docs/log-field-contract.md promises for
// this tier -- plus the per-group numbers the old single-line table carried.
// It must not carry a correlation id: the line is a periodic aggregate, not
// scoped to any one request, exactly as docs/design.md's "Logs" section
// already says ("Not request-scoped, so no single requestID applies").
func TestFlightRecorderLineCarriesStableFieldsAndNoCorrelationID(t *testing.T) {
	t.Parallel()
	cfg := testConfig()
	cfg.Enforce = true
	p, clock := newTestPlugin(t, cfg)
	ctx, lines := capturingContext()
	p.lastContendedUnixNano.Store(clock.now().UnixNano())

	p.logFlightRecorderTick(ctx)

	line, ok := findLine(*lines, `"group":"app1"`)
	require.True(t, ok, "expected an app1 line, got: %v", *lines)
	assert.Equal(t, "test", logFieldString(t, line, "plugin"))
	assert.True(t, logFieldBool(t, line, "enforcing"))
	assert.Contains(t, line, `"weight"`)
	assert.Contains(t, line, `"attainedService"`)
	assert.Contains(t, line, `"normalizedService"`)
	assert.Contains(t, line, `"inFlight"`)
	assert.Contains(t, line, `"provisionalCharge"`)
	assert.Contains(t, line, `"ewmaOutputTokens"`)
	assert.Contains(t, line, `"ewmaWarm"`)
	assert.NotContains(t, line, `"requestID"`, "a periodic aggregate line must not claim a single request's correlation id")
}

func logFieldBool(t *testing.T, line, key string) bool {
	t.Helper()
	var obj map[string]any
	require.NoError(t, json.Unmarshal([]byte(line), &obj))
	v, ok := obj[key]
	require.True(t, ok, "field %q not present in log line: %s", key, line)
	b, ok := v.(bool)
	require.True(t, ok, "field %q is not a bool in log line: %s", key, line)
	return b
}
