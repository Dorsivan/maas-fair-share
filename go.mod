module github.com/Dorsivan/maas-fair-share

go 1.26.6

// Pinned to a release tag, never main -- flow-control interfaces are Alpha/Beta on a
// v0.x module. Bump this and Dockerfile.epp's builder image together, then re-run the
// conformance and load tests. See docs/design.md, Part 3 "Version pinning".
require github.com/llm-d/llm-d-router v0.11.0

// Indirect dependencies are resolved by `go mod tidy` -- importing cmd/epp/runner
// pulls essentially the whole EPP graph (~400 modules). No replace directives.
