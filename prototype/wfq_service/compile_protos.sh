#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROTO_DIR="$SCRIPT_DIR/protos"
OUT_DIR="$SCRIPT_DIR/generated"

mkdir -p "$OUT_DIR"

python -m grpc_tools.protoc \
    -I"$PROTO_DIR" \
    --python_out="$OUT_DIR" \
    --grpc_python_out="$OUT_DIR" \
    envoy/service/ext_proc/v3/external_processor.proto \
    envoy/config/core/v3/base.proto \
    envoy/type/v3/http_status.proto

# Fix imports in generated files: protoc generates absolute imports
# that don't work without the proto path on sys.path. Rewrite them
# to be relative to the generated directory.
find "$OUT_DIR" -name '*.py' -exec sed -i \
    's/^from envoy\./from envoy./; s/^import envoy\./import envoy./' {} +

# Create __init__.py files for all packages
find "$OUT_DIR" -type d -exec touch {}/__init__.py \;

# Create convenience re-exports at the top level of generated/
cat > "$OUT_DIR/ext_proc_pb2.py" << 'EOF'
from envoy.service.ext_proc.v3.external_processor_pb2 import *  # noqa: F401,F403
EOF

cat > "$OUT_DIR/ext_proc_pb2_grpc.py" << 'EOF'
from envoy.service.ext_proc.v3.external_processor_pb2_grpc import *  # noqa: F401,F403
EOF

echo "Proto compilation complete. Output in $OUT_DIR"
