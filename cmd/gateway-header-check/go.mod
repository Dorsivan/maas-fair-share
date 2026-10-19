// Separate module from the repository root, for the same reason as
// conformance/gatewayheaders/go.mod: this binary only needs
// conformance/gatewayheaders and sigs.k8s.io/yaml, not the ~400-module EPP
// dependency graph the root module compiles against. The replace below
// points at the sibling module by relative path -- no network or published
// version needed to link them together.
module github.com/Dorsivan/maas-fair-share/cmd/gateway-header-check

go 1.26.6

require github.com/Dorsivan/maas-fair-share/conformance/gatewayheaders v0.0.0

replace github.com/Dorsivan/maas-fair-share/conformance/gatewayheaders => ../../conformance/gatewayheaders

require (
	go.yaml.in/yaml/v2 v2.4.2 // indirect
	sigs.k8s.io/yaml v1.6.0 // indirect
)
