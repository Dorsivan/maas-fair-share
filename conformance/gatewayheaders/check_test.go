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

package gatewayheaders

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func loadDir(t *testing.T, dir string) []object {
	t.Helper()
	entries, err := os.ReadDir(dir)
	require.NoError(t, err)

	var docs []object
	for _, e := range entries {
		if e.IsDir() || filepath.Ext(e.Name()) != ".yaml" {
			continue
		}
		data, err := os.ReadFile(filepath.Join(dir, e.Name()))
		require.NoError(t, err)
		parsed, err := ParseYAML(data)
		require.NoError(t, err, "parsing %s", e.Name())
		docs = append(docs, parsed...)
	}
	return docs
}

// TestGoodFixturesPass is the "this is what correct looks like" half of the
// conformance check: every inference route in testdata/good is covered,
// whether by a Gateway-scoped policy, a route-scoped policy, a
// cross-namespace parentRef, or a differently-cased header key -- and a
// Service-backed route with zero AuthPolicy coverage is correctly ignored.
func TestGoodFixturesPass(t *testing.T) {
	docs := loadDir(t, "testdata/good")
	violations, err := Check(docs)
	require.NoError(t, err)
	assert.Empty(t, violations)
}

// TestBadFixturesFailLoudly is the required demonstration from UNI-33: run
// the check against a deliberately non-stripping route and confirm it fails,
// by name, rather than passing silently.
func TestBadFixturesFailLoudly(t *testing.T) {
	testCases := []struct {
		name       string
		file       string
		wantRoute  string
		wantNS     string
		wantReason string
	}{
		{
			name:       "route with no AuthPolicy at all",
			file:       "no-authpolicy.yaml",
			wantNS:     "bad-ns",
			wantRoute:  "bare-route",
			wantReason: "no AuthPolicy on this route or its parent Gateway",
		},
		{
			name:       "AuthPolicy strips only the deprecated alias",
			file:       "old-header-only.yaml",
			wantNS:     "bad-ns",
			wantRoute:  "half-fixed-route",
			wantReason: "no AuthPolicy on this route or its parent Gateway",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			data, err := os.ReadFile(filepath.Join("testdata/bad", tc.file))
			require.NoError(t, err)
			docs, err := ParseYAML(data)
			require.NoError(t, err)

			violations, err := Check(docs)
			require.NoError(t, err)

			require.Len(t, violations, 1, "expected exactly one violation for %s", tc.file)
			assert.Equal(t, tc.wantNS, violations[0].Namespace)
			assert.Equal(t, tc.wantRoute, violations[0].Name)
			assert.Contains(t, violations[0].Reason, tc.wantReason)
		})
	}
}

// TestOldHeaderAloneIsNotEnough pins the exact regression this ticket closes:
// an AuthPolicy that already overwrites x-gateway-inference-objective (as
// maas-poc-gateway-authn did before this change) must still be flagged, since
// the EPP prefers the newer x-llm-d-inference-objective header whenever a
// client sets it.
func TestOldHeaderAloneIsNotEnough(t *testing.T) {
	data, err := os.ReadFile("testdata/bad/old-header-only.yaml")
	require.NoError(t, err)
	docs, err := ParseYAML(data)
	require.NoError(t, err)

	for _, doc := range docs {
		if isKind(doc, "AuthPolicy") {
			assert.False(t, authPolicyStripsObjective(doc),
				"fixture must only strip the deprecated alias, or this test is not exercising the regression")
		}
	}

	violations, err := Check(docs)
	require.NoError(t, err)
	assert.Len(t, violations, 1)
}

// TestParseYAMLExpandsList covers the `oc get <kinds> -A -o yaml` shape,
// which wraps multiple resources in a single `kind: List` rather than
// separating them with `---`. This is the format the live conformance run
// (docs/gateway-header-stripping.md) actually feeds into this package.
func TestParseYAMLExpandsList(t *testing.T) {
	data := []byte(`
apiVersion: v1
kind: List
items:
- apiVersion: gateway.networking.k8s.io/v1
  kind: HTTPRoute
  metadata:
    name: from-list
    namespace: ns
  spec:
    parentRefs:
    - kind: Gateway
      name: gw
    rules:
    - backendRefs:
      - group: inference.networking.k8s.io
        kind: InferencePool
        name: pool
`)
	docs, err := ParseYAML(data)
	require.NoError(t, err)
	require.Len(t, docs, 1)
	assert.True(t, isKind(docs[0], "HTTPRoute"))

	violations, err := Check(docs)
	require.NoError(t, err)
	require.Len(t, violations, 1)
	assert.Equal(t, "from-list", violations[0].Name)
}
