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

// UNI-302: the stamp explains itself. These tests hold the decision log to
// the arithmetic it claims to show, and the charged-cost counter to the
// composition the sim measures.

import (
	"context"
	"encoding/json"
	"fmt"
	"math"
	"strings"
	"testing"
	"time"

	"github.com/go-logr/logr/funcr"
	"github.com/prometheus/client_golang/prometheus/testutil"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"sigs.k8s.io/controller-runtime/pkg/log"

	fwkrc "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requestcontrol"
	fwkrh "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/requesthandling"
	fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"
)

func completeResp(prompt, completion int) *fwkrc.Response {
	return &fwkrc.Response{
		EndOfStream: true, TerminationCause: fwkrc.TerminationCauseNatural,
		Usage: fwkrh.Usage{PromptTokens: prompt, CompletionTokens: completion, TotalTokens: prompt + completion},
	}
}

func decodeLine(t *testing.T, line string) map[string]any {
	t.Helper()
	var obj map[string]any
	require.NoError(t, json.Unmarshal([]byte(line), &obj))
	return obj
}

func sfqLogConfig(level string) Config {
	cfg := testConfig()
	cfg.SFQPriorityStamp = true
	cfg.SFQDecisionLog = level
	return cfg
}

func dispatchOne(t *testing.T, ctx context.Context, p *Plugin, sub, endpoint string) *fwksched.InferenceRequest {
	t.Helper()
	req := &fwksched.InferenceRequest{Body: &fwkrh.InferenceRequestBody{Payload: fwkrh.PayloadMap{"model": "m"}}}
	req.Headers = map[string]string{"x-maas-subscription": sub}
	require.NoError(t, p.RequestHeader(ctx, req))
	require.NoError(t, p.PreRequest(ctx, req, onEndpoint(endpoint)))
	return req
}

func TestSFQDecisionLogOffByDefault(t *testing.T) {
	t.Parallel()
	assert.Equal(t, "", DefaultConfig().SFQDecisionLog)
	p, _ := newTestPlugin(t, sfqLogConfig(""))
	ctx, lines := capturingContextV(10)
	req := dispatchOne(t, ctx, p, "app1-production", "e0")
	complete(p, req, 100, 50)
	for _, l := range *lines {
		assert.NotContains(t, l, `"sfq `, "default config must log nothing new")
	}

	// And the full snapshot is not taken.
	_, rec := p.sfq.dispatch(p.now(), "", "app1", "ns/e0", 20, 10, 10)
	assert.Nil(t, rec.FinishTags)
	assert.Nil(t, rec.Endpoints)
}

func TestSFQDecisionLogRejectsUnknownLevel(t *testing.T) {
	t.Parallel()
	_, err := newPlugin("x", sfqLogConfig("verbose"))
	require.Error(t, err)
	assert.Contains(t, err.Error(), "sfqDecisionLog")
}

func TestSFQDecisionLogInfoLine(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, sfqLogConfig("info"))
	ctx, lines := capturingContext()
	dispatchOne(t, ctx, p, "app2-batch", "e0")
	dispatchOne(t, ctx, p, "app1-production", "e0")
	dispatchOne(t, ctx, p, "app2-batch", "e0")

	infos := linesContaining(*lines, `"sfq priority"`)
	require.Len(t, infos, 3)
	assert.Empty(t, linesContaining(*lines, `"sfq decision"`), "info must not emit the debug record")
	last := decodeLine(t, infos[2])
	assert.Equal(t, "app2", last["group"])
	assert.Equal(t, float64(10), last["weight"])
	// app2's second request starts at its own finish tag, above app1's next
	// start (V = 0, nothing has started): one group ahead of it.
	assert.Equal(t, "2/2", last["rank"])
	assert.NotEmpty(t, last["requestID"])
	assert.Equal(t, last["tag"], last["tagAboveV"], "V is 0 before anything starts")
	assert.Equal(t, decodeLine(t, infos[1])["rank"], "1/2")
}

// The decision log must never be written with the ledger lock held. A sink
// that tries the lock proves it, line by line.
func TestSFQDecisionLogWrittenOutsideTheLock(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, sfqLogConfig("debug"))
	var lines []string
	held := 0
	logger := funcr.NewJSON(func(obj string) {
		if strings.Contains(obj, `"sfq `) {
			if p.sfq.mu.TryLock() {
				p.sfq.mu.Unlock()
			} else {
				held++
			}
		}
		lines = append(lines, obj)
	}, funcr.Options{})
	ctx := log.IntoContext(context.Background(), logger)
	req := dispatchOne(t, ctx, p, "app1-production", "e0")
	p.ResponseBody(ctx, req, &fwkrc.Response{}, nil) // first byte
	p.ResponseBody(ctx, req, completeResp(100, 50), nil)
	require.Len(t, linesContaining(lines, `"sfq decision"`), 1)
	require.Len(t, linesContaining(lines, `"sfq settle"`), 1)
	assert.Zero(t, held)
}

// The settle record shows the true-up as arithmetic: finishAfter =
// finishBefore + (actual - charged)/weight.
func TestSFQDecisionLogSettleRecord(t *testing.T) {
	t.Parallel()
	p, _ := newTestPlugin(t, sfqLogConfig("debug"))
	ctx, lines := capturingContext()
	req := dispatchOne(t, ctx, p, "app1-production", "e0")
	p.ResponseBody(ctx, req, completeResp(100, 50), nil)

	d := decodeLine(t, linesContaining(*lines, `"sfq decision"`)[0])
	st := decodeLine(t, linesContaining(*lines, `"sfq settle"`)[0])
	assert.Equal(t, d["requestID"], st["requestID"])
	assert.Equal(t, d["est"], st["charged"])
	assert.Equal(t, d["finishAfter"], st["finishBefore"])
	actual := 100*1.0 + 50*2.0
	assert.Equal(t, actual, st["actual"])
	assert.InDelta(t, (actual-st["charged"].(float64))/20, st["finishCorrection"], 1e-9)
	assert.InDelta(t, st["finishBefore"].(float64)+st["finishCorrection"].(float64), st["finishAfter"], 1e-9)
}

// A reaped ticket shows up on the next dispatch's record, with its reason
// and correction.
func TestSFQDecisionLogNamesReapedTickets(t *testing.T) {
	t.Parallel()
	cfg := sfqLogConfig("debug")
	cfg.SFQSettleTimeoutSeconds = 10
	p, clock := newTestPlugin(t, cfg)
	ctx, lines := capturingContext()
	lost := dispatchOne(t, ctx, p, "app2-batch", "e0")
	clock.advance(11 * time.Second)
	dispatchOne(t, ctx, p, "app1-production", "e0")

	recs := linesContaining(*lines, `"sfq decision"`)
	require.Len(t, recs, 2)
	d := decodeLine(t, recs[1])
	assert.Equal(t, float64(1), d["reapedTimeout"])
	reaped := d["reaped"].([]any)
	require.Len(t, reaped, 1)
	r := reaped[0].(map[string]any)
	corr, _ := fwksched.ReadRequestAttribute[correlation](lost, correlationKey)
	assert.Equal(t, corr.requestID, r["requestID"])
	assert.Equal(t, "app2", r["group"])
	assert.InDelta(t, (r["worst"].(float64)-r["charged"].(float64))/10, r["finishCorrection"], 1e-9)
	assert.InDelta(t, d["finishTags"].(map[string]any)["app2"],
		decodeLine(t, recs[0])["finishAfter"].(float64)+r["finishCorrection"].(float64), 1e-9)
}

// An idle reset zeroes every finish tag, so every group's gauge is refreshed,
// not only the dispatching group's.
func TestSFQIdleResetRefreshesEveryGroupGauge(t *testing.T) {
	cfg := sfqLogConfig("")
	cfg.Groups = []GroupConfig{
		{Name: "uni302-a", Weight: 1, Match: GroupMatch{Exact: []string{"a"}}},
		{Name: "uni302-b", Weight: 1, Match: GroupMatch{Exact: []string{"b"}}},
	}
	p, clock := newTestPlugin(t, cfg)
	ctx := context.Background()
	a := dispatchOne(t, ctx, p, "a", "e0")
	complete(p, a, 100, 50)
	require.Greater(t, testutil.ToFloat64(sfqFinishTag.WithLabelValues("uni302-a")), 0.0)
	clock.advance(time.Second)
	dispatchOne(t, ctx, p, "b", "e0") // the pool was idle: new epoch
	assert.Zero(t, testutil.ToFloat64(sfqFinishTag.WithLabelValues("uni302-a")))
}

type sfqLogDecision struct {
	group                                         string
	weight, est, v, finishBefore, start, finishAf float64
	tag, wireBase, priority                       int64
	rank, rankOf                                  int
	finishTags                                    map[string]float64
	idleReset                                     bool
}

func parseDecision(t *testing.T, line string) sfqLogDecision {
	o := decodeLine(t, line)
	d := sfqLogDecision{
		group: o["group"].(string), weight: o["weight"].(float64), est: o["est"].(float64),
		v: o["virtualTime"].(float64), finishBefore: o["finishBefore"].(float64),
		start: o["start"].(float64), finishAf: o["finishAfter"].(float64),
		tag: int64(o["quantisedTag"].(float64)), wireBase: int64(o["wireBase"].(float64)),
		priority: int64(o["priority"].(float64)),
		rank:     int(o["rankPos"].(float64)), rankOf: int(o["rankOf"].(float64)),
		idleReset: o["idleReset"].(bool), finishTags: map[string]float64{},
	}
	for g, f := range o["finishTags"].(map[string]any) {
		d.finishTags[g] = f.(float64)
	}
	return d
}

// The board's verification, part 1: run Arm A with the debug log on, and
// show the logged start/finish/tag arithmetic reproduces the integer
// actually stamped. Every dispatch is checked; a sample is printed for the
// ticket. Part of the check is that the log alone carries each group's
// finish tag from one dispatch to the next: finishBefore must equal the
// group's previous finishAfter plus every logged true-up since.
//
// Arm A as shipped has max_tokens equal to the output, so every true-up is
// zero. The second case raises max_tokens to 128, so dispatches made before
// the output-length estimate warms are over-charged and their completions
// true F_g down.
func TestSFQDecisionLogReproducesTheStamp(t *testing.T) {
	t.Parallel()
	for _, maxTokens := range []int64{64, 128} {
		t.Run(fmt.Sprintf("max_tokens=%d", maxTokens), func(t *testing.T) {
			t.Parallel()
			reproduceStamp(t, maxTokens)
		})
	}
}

func reproduceStamp(t *testing.T, maxTokens int64) {
	var lines []string
	logger := funcr.NewJSON(func(obj string) { lines = append(lines, obj) }, funcr.Options{})
	prm := sfqSimBase(32)
	prm.duration = 60
	prm.maxTokens = maxTokens
	prm.decisionLog = SFQDecisionLogDebug
	prm.ctx = log.IntoContext(context.Background(), logger)
	r := runSFQSim(t, prm)

	var decisions []sfqLogDecision
	ledger := map[string]float64{} // F_g, rebuilt from the log alone
	settles, corrected := 0, 0
	for _, l := range lines {
		switch {
		case strings.Contains(l, `"msg":"sfq decision"`):
			d := parseDecision(t, l)
			if d.idleReset {
				ledger = map[string]float64{}
			}
			require.InDelta(t, ledger[d.group], d.finishBefore, 1e-9, "F_%s carried by the log", d.group)
			ledger[d.group] = d.finishAf
			decisions = append(decisions, d)
		case strings.Contains(l, `"msg":"sfq settle"`):
			o := decodeLine(t, l)
			g := o["group"].(string)
			require.InDelta(t, ledger[g], o["finishBefore"].(float64), 1e-9)
			ledger[g] += o["finishCorrection"].(float64)
			if o["finishCorrection"].(float64) != 0 {
				corrected++
			}
			require.InDelta(t, ledger[g], o["finishAfter"].(float64), 1e-9)
			settles++
		}
	}
	require.Len(t, decisions, len(r.prios), "one decision record per dispatch")
	require.Positive(t, settles)
	if maxTokens > int64(prm.outToks) {
		// Until the output-length EWMA warms, the estimate leans on
		// max_tokens, so the early completions true down.
		require.Positive(t, corrected, "some completions must true up")
	}

	for i, d := range decisions {
		start := math.Max(d.finishBefore, d.v)
		require.Equal(t, start, d.start, "dispatch %d: start = max(F_g, V)", i)
		require.Equal(t, start+d.est/d.weight, d.finishAf, "dispatch %d: F_g = start + est/w", i)
		require.Equal(t, int64(math.Round(start*sfqTagScale)), d.tag, "dispatch %d: tag = round(start x 1000)", i)
		require.Equal(t, d.wireBase+d.tag, d.priority, "dispatch %d", i)
		require.Equal(t, r.prios[i], d.priority, "dispatch %d: the integer actually in the body", i)
		require.Equal(t, d.finishAf, d.finishTags[d.group])
		rank := 1
		for g, f := range d.finishTags {
			if g != d.group && math.Max(f, d.v) < start {
				rank++
			}
		}
		require.Equal(t, rank, d.rank, "dispatch %d: rank", i)
		require.Equal(t, len(d.finishTags), d.rankOf)
	}

	// The printed sample: past warm-up, so V has moved and every group has
	// history, cycling the three groups.
	t.Logf("%d dispatches, %d settles (%d with a nonzero true-up), all reproduced. Sample (tag units; stamp = wireBase + round(start x 1000)):", len(decisions), settles, corrected)
	t.Logf("%-4s %-9s %4s %6s %10s %10s %10s %10s %10s %8s %4s  %s", "#", "group", "w", "est", "F_before", "V", "start", "F_after", "stamped", "rank", "", "other groups' F")
	seen := map[string]int{}
	shown := 0
	for i, d := range decisions {
		if i < len(decisions)/2 || seen[d.group] >= 4 || shown >= 12 {
			continue
		}
		if shown > 0 && decisions[i-1].group == d.group {
			continue
		}
		seen[d.group]++
		shown++
		var others []string
		for _, g := range sfqSimTenants {
			if g != d.group {
				others = append(others, fmt.Sprintf("%s=%.4f", g, d.finishTags[g]))
			}
		}
		t.Logf("%-4d %-9s %4.0f %6.0f %10.4f %10.4f %10.4f %10.4f %10d %5d/%d       %s", i, d.group, d.weight, d.est,
			d.finishBefore, d.v, d.start, d.finishAf, d.priority, d.rank, d.rankOf, strings.Join(others, " "))
	}
}

// The board's verification, part 2: the live-distribution counter converges
// to the configured weights in Arm A. Not parallel: the counter is a
// process-wide series, and the sim's groups are shared with other sim tests.
// Go runs every parallel test only after the sequential ones finish.
func TestSFQChargedCostConvergesInArmA(t *testing.T) {
	target := sfqSimTarget(sfqSimTenants)
	read := func() map[string]float64 {
		out := map[string]float64{}
		for _, tn := range sfqSimTenants {
			out[tn] = testutil.ToFloat64(sfqChargedCost.WithLabelValues(tn))
		}
		return out
	}
	share := func(a, b map[string]float64) map[string]float64 {
		tot := 0.0
		for _, tn := range sfqSimTenants {
			tot += b[tn] - a[tn]
		}
		out := map[string]float64{}
		for _, tn := range sfqSimTenants {
			if tot > 0 {
				out[tn] = 100 * (b[tn] - a[tn]) / tot
			}
		}
		return out
	}

	prm := sfqSimBase(32)
	base := read()
	var marks []float64
	snaps := []map[string]float64{}
	next := 0.0
	var warm map[string]float64
	prm.onEvent = func(at float64) {
		if warm == nil && at >= prm.warmup {
			warm = read()
		}
		for at >= next {
			marks = append(marks, next)
			snaps = append(snaps, read())
			next += 30
		}
	}
	r := runSFQSim(t, prm)
	end := read()

	t.Logf("charged-cost share over 30 s windows, target %s:", fmtShare(target))
	for i := 1; i < len(snaps); i++ {
		w := share(snaps[i-1], snaps[i])
		t.Logf("  [%3.0f,%3.0f) s  %s  dev %.1f pt", marks[i-1], marks[i], fmtShare(w), sfqSimDev(w, target))
	}
	cum := share(warm, end)
	served := r.share(prm.warmup, prm.duration)
	t.Logf("after warm-up: counter %s dev %.1f pt; sim slot-seconds %s dev %.1f pt",
		fmtShare(cum), sfqSimDev(cum, target), fmtShare(served), sfqSimDev(served, target))
	assert.Less(t, sfqSimDev(cum, target), 2.0)
	// The counter books cost at settlement, so it agrees with the sim's own
	// slot-second scoring, not just with the target.
	assert.Less(t, sfqSimDev(cum, served), 1.5)
	assert.Positive(t, share(base, end)["app1"])
}
