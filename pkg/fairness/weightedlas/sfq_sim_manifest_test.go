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

// UNI-305: the SFQ sim driven by the POC harness's own tenant manifests
// (deploy/poc/tenants/*.tenants, read by every load generator and checked
// against the EPP config by deploy/poc/tenants.py). Same parameters as Arm A
// -- 2 endpoints x 8 slots, closed loop -- with the tenant set, weights and
// worker counts taken from the file. A '-' workers column means Arm A's 32.
//
// default.tenants IS Arm A, so its numbers must equal TestSFQSimArmAComposition's
// to the decimal. six-unequal.tenants is six tenants at 40/20/15/10/10/5 with
// 32 workers each: the workers do not encode the weights, so hitting the
// target is the stamp's doing.

import (
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

const tenantManifestDir = "../../../deploy/poc/tenants"

// loadTenantManifest reads the group, weight and workers columns of a
// .tenants file. deploy/poc/tenants.py is the full parser; this only needs
// enough to drive the sim and fails on anything it does not understand.
func loadTenantManifest(t *testing.T, path string) ([]sfqSimTenant, map[string]int) {
	t.Helper()
	raw, err := os.ReadFile(path)
	require.NoError(t, err)
	var ts []sfqSimTenant
	workers := map[string]int{}
	for n, line := range strings.Split(string(raw), "\n") {
		if i := strings.IndexByte(line, '#'); i >= 0 {
			line = line[:i]
		}
		cols := strings.Fields(line)
		if len(cols) == 0 {
			continue
		}
		require.Len(t, cols, 7, "%s:%d: group weight match keys workers rate shape", path, n+1)
		w, err := strconv.ParseFloat(cols[1], 64)
		require.NoError(t, err, "%s:%d weight", path, n+1)
		ts = append(ts, sfqSimTenant{cols[0], w})
		workers[cols[0]] = 32
		if cols[4] != "-" {
			workers[cols[0]], err = strconv.Atoi(cols[4])
			require.NoError(t, err, "%s:%d workers", path, n+1)
		}
	}
	require.NotEmpty(t, ts, path)
	return ts, workers
}

func TestSFQSimTenantManifests(t *testing.T) {
	t.Parallel()
	paths, err := filepath.Glob(filepath.Join(tenantManifestDir, "*.tenants"))
	require.NoError(t, err)
	require.NotEmpty(t, paths, "no manifests under %s", tenantManifestDir)
	for _, path := range paths {
		ts, workers := loadTenantManifest(t, path)
		names := make([]string, len(ts))
		for i, tn := range ts {
			names[i] = tn.name
		}
		target := sfqSimTargetOf(ts)
		for s := int64(1); s <= 2; s++ {
			prm := sfqSimBase(32)
			prm.tenants, prm.workers, prm.seed = ts, workers, s
			r := runSFQSim(t, prm)
			sh := r.share(prm.warmup, prm.duration)
			name := fmt.Sprintf("%s seed %d", filepath.Base(path), s)
			t.Logf("%-58s served %s target %s dev %.1f pt, %.1f req/s", name,
				fmtShareOf(names, sh), fmtShareOf(names, target), sfqSimDev(sh, target), r.throughput)
			for _, tn := range ts {
				t.Logf("    %-10s weight %4g  workers %3d  target %5.1f%%  observed %5.1f%%  diff %+5.1f pt",
					tn.name, tn.weight, workers[tn.name], target[tn.name], sh[tn.name], sh[tn.name]-target[tn.name])
			}
			assert.Less(t, sfqSimDev(sh, target), 2.0, name)
			assert.Greater(t, r.throughput, 20.0, "%s: work conservation", name)
		}
	}
}
