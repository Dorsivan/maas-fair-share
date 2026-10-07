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

// Command maas-epp is the stock llm-d Endpoint Picker plus one registered
// fairness policy.
//
// EPP plugins are compiled in -- there is no dynamic loading -- so adding one
// means building a binary that imports the upstream runner, registers the
// plugin with the global registry, and hands off. Everything upstream behaves
// identically; this adds, it does not replace.
package main

import (
	"os"

	"github.com/spf13/pflag"
	ctrl "sigs.k8s.io/controller-runtime"

	"github.com/llm-d/llm-d-router/cmd/epp/runner"
	fwkplugin "github.com/llm-d/llm-d-router/pkg/epp/framework/interface/plugin"

	"github.com/Dorsivan/maas-fair-share/pkg/fairness/weightedlas"
)

// registerDownstreamCompatFlags accepts flags that Red Hat's KServe scheduler
// preset templates into the container but that upstream llm-d-router does not
// define.
//
// This is not defensive programming, it is a measured incompatibility. The
// RHOAI 3.4.0 preset (LLMInferenceServiceConfig v3-5-0-kserve-config-llm-scheduler
// -- the v3-5-0 prefix is the well-known-config name, not the product version)
// appends --model-server-metrics-scheme=https whenever the cluster's
// inferenceservice-config has enableLLMInferenceServiceTLS: true. That flag
// exists only in Red Hat's downstream EPP fork; it is absent from upstream
// v0.10.0 AND v0.11.0, where the setting moved into the metrics-data-source
// plugin's `scheme` parameter. pflag treats an unknown flag as fatal, so
// without this the pod crash-loops before it parses a line of configuration.
//
// The value is deliberately ignored rather than translated: the ConfigMap sets
// `scheme` on metrics-data-source directly, which is the mechanism that
// actually works on this version. The runner logs every flag it parsed, so the
// ignored value still shows up in the startup log.
//
// The alternative is overriding the container's `command`, which forfeits the
// rest of KServe's templating (--pool-name, --pool-namespace, ports, TLS
// paths) and has to be re-synced by hand on every preset bump. This is the
// smaller liability. Re-check it whenever re-pinning llm-d-router or moving to
// a new RHOAI release: if upstream ever adds a real flag by this name, delete
// this shim or the duplicate registration will panic.
func registerDownstreamCompatFlags() {
	var ignored string
	pflag.StringVar(&ignored, "model-server-metrics-scheme", "",
		"Accepted for compatibility with the RHOAI KServe scheduler preset; ignored. "+
			"Set `scheme` on the metrics-data-source plugin in the EndpointPickerConfig instead.")
}

func main() {
	os.Exit(run())
}

func run() int {
	ctx := ctrl.SetupSignalHandler()

	// Registered Beta, not Alpha. The runner calls ValidatePluginStability and
	// the KServe scheduler preset does not pass --allow-experimental-plugins, so
	// an Alpha plugin would fail at startup rather than at review time.
	//
	// Declaring the type in the config's top-level `plugins:` list is enough to
	// wire RequestHeader, PreRequest and ResponseBody as well: the requestcontrol
	// config type-asserts every instantiated plugin against each extension point.
	fwkplugin.Register(weightedlas.PluginType, fwkplugin.StabilityBeta, weightedlas.Factory)

	// Must happen before Run: the runner calls opts.AddFlags(pflag.CommandLine)
	// and then pflag.Parse() on the same global FlagSet, so anything registered
	// here is parsed alongside the upstream flags.
	registerDownstreamCompatFlags()

	// Upstream's built-in plugins register themselves when the runner parses the
	// configuration, so nothing else is needed here.
	if err := runner.NewRunner().
		WithExecutableName("maas-epp").
		Run(ctx); err != nil {
		return 1
	}
	return 0
}
