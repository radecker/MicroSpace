#!/bin/bash
set -e
set -o pipefail

echo "[Common] Building..."
echo "[Common] Generating new config.proto"
# Generate an updated config proto file based on yaml
python yaml_to_proto.py

echo "[Common] Compiling proto files"
# Compile protobuf messages and generate new classes
protoc -I=. --python_out=. config.proto message.proto
echo "[Common] Done!"