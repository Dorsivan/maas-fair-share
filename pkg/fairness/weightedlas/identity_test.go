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
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"testing"
	"time"

	"github.com/prometheus/client_golang/prometheus/testutil"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

// UNI-306: the compiled-in default was the known-broken "-id" name, and only
// the ConfigMaps' override kept fairness working. Every identityHeader set
// anywhere under deploy/ must equal the default, so a config that omits the
// field behaves exactly like the ones we have measured -- and the two cannot
// drift apart again without this test failing.
func TestDefaultIdentityHeaderMatchesDeployedConfigs(t *testing.T) {
	t.Parallel()
	assert.Equal(t, DefaultIdentityHeader, DefaultConfig().IdentityHeader)

	re := regexp.MustCompile(`(?m)^\s*identityHeader:\s*"?([^"\s#]+)`)
	root := filepath.Join("..", "..", "..", "deploy")
	found := map[string]string{}
	err := filepath.WalkDir(root, func(path string, d os.DirEntry, err error) error {
		if err != nil || d.IsDir() || !(strings.HasSuffix(path, ".yaml") || strings.HasSuffix(path, ".yml")) {
			return err
		}
		b, err := os.ReadFile(path)
		if err != nil {
			return err
		}
		for _, m := range re.FindAllStringSubmatch(string(b), -1) {
			found[path] = m[1]
			assert.Equal(t, DefaultIdentityHeader, m[1], "%s sets identityHeader %q", path, m[1])
		}
		return nil
	})
	require.NoError(t, err)
	// Guard against the walk silently matching nothing (moved dir, changed
	// key spelling) and the test passing vacuously.
	require.Contains(t, found, filepath.Join(root, "epp-config.yaml"))
	require.Contains(t, found, filepath.Join(root, "poc", "00-config.yaml"))
}

// A request without the identity header lands in the catch-all, increments the
// miss counter under the right reason, and -- unlike a mis-matched value --
// does not touch unmatched_subscriptions_total. Not parallel: the counters are
// process-global, and non-parallel tests finish before parallel ones resume,
// so the deltas here are exact.
func TestMissingIdentityHeaderCountsAndFallsToDefaultGroup(t *testing.T) {
	p, _ := newTestPlugin(t, testConfig())
	ctx, _ := capturingContext()

	absent0 := testutil.ToFloat64(identityHeaderMissing.WithLabelValues("absent"))
	empty0 := testutil.ToFloat64(identityHeaderMissing.WithLabelValues("empty"))
	unmatched0 := testutil.ToFloat64(unmatchedSubscriptions)

	// The old default name: the header the gateway never sends.
	absent := &fwksched.InferenceRequest{Headers: map[string]string{"x-maas-subscription-id": "app1-production"}}
	require.NoError(t, p.RequestHeader(ctx, absent))
	assert.Equal(t, "unclassified", absent.FairnessID)

	empty := &fwksched.InferenceRequest{Headers: map[string]string{"x-maas-subscription": "  "}}
	require.NoError(t, p.RequestHeader(ctx, empty))
	assert.Equal(t, "unclassified", empty.FairnessID)

	matched := &fwksched.InferenceRequest{Headers: map[string]string{"x-maas-subscription": "app1-production"}}
	require.NoError(t, p.RequestHeader(ctx, matched))
	assert.Equal(t, "app1", matched.FairnessID)

	assert.Equal(t, 1.0, testutil.ToFloat64(identityHeaderMissing.WithLabelValues("absent"))-absent0)
	assert.Equal(t, 1.0, testutil.ToFloat64(identityHeaderMissing.WithLabelValues("empty"))-empty0)
	assert.Equal(t, 0.0, testutil.ToFloat64(unmatchedSubscriptions)-unmatched0)
}

const identityWarning = "identity header missing from most requests"

// driveWindow sends n requests, the first `missing` of them without the
// identity header, spread inside one window; then one more request after the
// window expires, which closes it.
func driveWindow(t *testing.T, p *Plugin, clock *fakeClock, n, missing int) []string {
	t.Helper()
	ctx, lines := capturingContext()
	for i := 0; i < n; i++ {
		h := map[string]string{"x-maas-subscription": "app1-production"}
		if i < missing {
			h = map[string]string{"x-maas-subscription-id": "app1-production"}
		}
		require.NoError(t, p.RequestHeader(ctx, &fwksched.InferenceRequest{Headers: h}))
		clock.advance(time.Second)
	}
	clock.advance(identityMissWindow)
	require.NoError(t, p.RequestHeader(ctx, &fwksched.InferenceRequest{
		Headers: map[string]string{"x-maas-subscription": "app1-production"}}))
	return *lines
}

func TestIdentityMissWarning(t *testing.T) {
	t.Parallel()
	cases := []struct {
		name       string
		n, missing int
		warn       bool
	}{
		{"misnamed header: every request missing", 30, 30, true},
		{"at the share threshold", 30, 27, true},
		{"below the share threshold", 30, 26, false},
		{"healthy traffic", 30, 0, false},
		{"too few requests to judge", identityMissMinRequests - 1, identityMissMinRequests - 1, false},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			t.Parallel()
			p, clock := newTestPlugin(t, testConfig())
			lines := driveWindow(t, p, clock, tc.n, tc.missing)
			line, ok := findLine(lines, identityWarning)
			require.Equal(t, tc.warn, ok, "lines: %v", lines)
			if ok {
				assert.Equal(t, float64(tc.n), logFieldNumber(t, line, "requests"))
				assert.Equal(t, float64(tc.missing), logFieldNumber(t, line, "missing"))
				assert.Equal(t, float64(tc.missing), logFieldNumber(t, line, "absent"))
				assert.Equal(t, "x-maas-subscription", logFieldString(t, line, "identityHeader"))
			}
		})
	}
}

// One line per window, not per request: the warning has to survive a cluster
// sending thousands of requests a second with a misnamed header.
func TestIdentityMissWarningIsRateLimited(t *testing.T) {
	t.Parallel()
	p, clock := newTestPlugin(t, testConfig())
	ctx, lines := capturingContext()
	bad := map[string]string{"x-maas-subscription-id": "app1-production"}
	// Three full windows of 1000 requests each, then a closing request.
	for w := 0; w < 3; w++ {
		for i := 0; i < 1000; i++ {
			require.NoError(t, p.RequestHeader(ctx, &fwksched.InferenceRequest{Headers: bad}))
			clock.advance(identityMissWindow / 1000)
		}
	}
	clock.advance(time.Millisecond)
	require.NoError(t, p.RequestHeader(ctx, &fwksched.InferenceRequest{Headers: bad}))
	n := 0
	for _, l := range *lines {
		if strings.Contains(l, identityWarning) {
			n++
		}
	}
	assert.Equal(t, 3, n)
}
