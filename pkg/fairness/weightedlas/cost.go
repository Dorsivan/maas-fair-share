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

import fwksched "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/scheduling"

// ewmaWarmupSamples is how many completions a group must contribute before its
// observed output-length average is trusted over the configured default.
const ewmaWarmupSamples = 8

// ewmaAlphaDenominator makes the output EWMA a count-based average over roughly
// the last 64 requests from that group.
//
// Count-based, not time-based: "what a typical request from this group looks
// like" is a per-request property, so a quiet group's estimate should not decay
// toward the global default just because it went quiet.
const ewmaAlphaDenominator = 64.0

// cost converts a token triple into the unit the tab is denominated in.
//
// Everything downstream of this function is unit-agnostic: weighted LAS is
// scale-free, so no constant anywhere else assumes a magnitude. That is what
// makes the cost model a config switch rather than a refactor.
//
// prompt is the total prompt token count and cached is the subset of it the
// server skipped recomputing, so the uncached remainder is prompt-cached.
func (p *Plugin) cost(prompt, cached, completion int) float64 {
	pf, cf, of := float64(prompt), float64(cached), float64(completion)
	if cf > pf {
		// Defensive: a server reporting more cached tokens than prompt tokens
		// would otherwise make the uncached term negative.
		cf = pf
	}
	switch p.cfg.CostModel {
	case CostModelVRAMTime:
		// Token-steps of KV residency. Quadratic in output length, where the
		// token model is linear -- see docs/design.md Part 3 item 9. Cached
		// tokens still occupy their blocks, so they are not discounted here.
		return of * (pf + of/2)
	default:
		return p.cfg.InputTokenWeight*(pf-cf) + p.cfg.CachedInputTokenWeight*cf + p.cfg.OutputTokenWeight*of
	}
}

// estimateCost prices a request before it has produced anything.
//
// The tokenizer is deliberately never invoked. An already-tokenized request is
// reused opportunistically when some other plugin triggered the token producer,
// but nothing here will trigger it: the EPP is the one replicas:1 component
// every request traverses, and after output-weight calibration the prompt term
// is roughly a tenth of the cost anyway. True-up makes the whole question
// low-stakes -- the estimate affects in-flight ordering and nothing else.
func (p *Plugin) estimateCost(request *fwksched.InferenceRequest, gs *groupState) float64 {
	promptEst := p.estimatePromptTokens(request)
	outputEst := p.estimateOutputTokens(request, gs)
	// Cached tokens are unknowable at dispatch; charging zero cached means the
	// estimate is the undiscounted price, which is the conservative direction.
	return p.cost(promptEst, 0, outputEst)
}

func (p *Plugin) estimatePromptTokens(request *fwksched.InferenceRequest) int {
	if request.Body != nil && request.Body.TokenizedRequest != nil {
		if n := request.Body.TokenizedRequest.TokenCount(); n > 0 {
			return n
		}
	}
	// RequestSizeBytes includes JSON framing, so bytes/N biases slightly high.
	// That is the safe direction: over-charging makes a tenant briefly more
	// restrained, while under-charging is what permits over-dispatch.
	if request.RequestSizeBytes > 0 {
		return int(float64(request.RequestSizeBytes) / p.cfg.EstimatedBytesPerToken)
	}
	return 0
}

// estimateOutputTokens is where the estimator effort belongs: output is the
// large term and the only genuinely unknown one.
//
// The chain is: the group's configured estimatedOutputTokens, then the
// group's output EWMA once warm, then defaultEstimatedOutputTokens, all capped
// by max_tokens. UNI-299: the configured value outranks the EWMA because the
// board asked for exactly that ordering -- the operator gets the price they
// configured, predictably. The cost is that the estimate stops learning for
// that group: if its traffic drifts, the dispatch tags stay wrong until the
// config is edited. The completion true-up corrects the group's finish tag on
// every completion, so the error is bounded by what the group has in flight
// rather than accumulating (sfq_sim_test.go TestSFQSimConfiguredEstimate).
// The EWMA is still maintained and logged next to the configured value, so a
// stale estimate is visible in the state log.
func (p *Plugin) estimateOutputTokens(request *fwksched.InferenceRequest, gs *groupState) int {
	est := p.cfg.DefaultEstimatedOutputTokens
	if gs != nil {
		observed, warm := gs.outputEWMA()
		switch {
		case gs.haveConfiguredOutput && !(p.configuredEstimateSeedOnly && warm):
			est = gs.configuredOutput
		case warm:
			est = observed
		}
	}
	// max_tokens is exact as a bound and useless as a central value: clients set
	// 4096 and generate 200. Cap with it, never estimate from it. The cap applies
	// to the configured value too, so an operator estimate can never out-charge
	// what the client declared it could generate.
	if request.Body != nil && request.Body.MaxOutputTokens != nil {
		if cap := float64(*request.Body.MaxOutputTokens); cap >= 0 && cap < est {
			est = cap
		}
	}
	if est < 0 {
		return 0
	}
	return int(est)
}

// usageTokens extracts the three counts from a response usage block. ok is false
// when the server reported no usage at all, which means a vLLM flag is missing
// rather than that the request was free.
func usageTokens(prompt, completion int, cached *int) (p, c, o int, ok bool) {
	if prompt == 0 && completion == 0 {
		return 0, 0, 0, false
	}
	if cached != nil {
		c = *cached
	}
	return prompt, c, completion, true
}
