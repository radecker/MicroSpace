#!/bin/bash

# Copy in the latest protobuf messages 
#cp ../../common/message_pb2.py .
#cp ../../common/config_pb2.py .
cp ../../common/message.proto .
cp ../../common/TCPClient.py .
cp ../../common/TCPServer.py .
cp ../../common/UDPClient.py .
cp ../../common/ConfigLoader.py .
cp ../../common/yaml_to_proto.py .

echo "[Ground System - main] Generating new config.proto"
# Generate an updated config proto file based on yaml
python yaml_to_proto.py

echo "[Ground System - main] Compiling proto files"
# Compile protobuf messages and generate new classes
protoc -I=. --python_out=. config.proto message.proto

# Build the docker image and tag it
docker build -t ground.main_service .