// This directory is a separate Go module from the repository root, on purpose.
//
// The root module compiles the EPP against github.com/llm-d/llm-d-router and
// deliberately does not vendor it (see docs/version-pinning.md, "we do not
// fork upstream and we do not vendor it: we compile against it") -- that pulls
// in roughly 400 modules, and `go mod vendor` at the root would vendor all of
// them.
//
// This package's only non-stdlib dependency is sigs.k8s.io/yaml, so it is
// split into its own module and vendored here. UNI-33 made this conformance
// check (cmd/gateway-header-check, which depends on this package) the
// standing defense against the gateway silently re-admitting a client-forged
// x-llm-d-inference-objective header; a defense that cannot be built without
// network access in a disconnected network is not a defense. See
// docs/gateway-header-stripping.md, "Building this check air-gapped".
module github.com/Dorsivan/maas-fair-share/conformance/gatewayheaders

go 1.26.6

require (
	github.com/stretchr/testify v1.11.1
	sigs.k8s.io/yaml v1.6.0
)

require (
	github.com/davecgh/go-spew v1.1.2-0.20180830191138-d8f796af33cc // indirect
	github.com/pmezard/go-difflib v1.0.0 // indirect
	go.yaml.in/yaml/v2 v2.4.2 // indirect
	gopkg.in/yaml.v3 v3.0.1 // indirect
)
