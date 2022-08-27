#!/bin/bash

echo "[cloud_service] Building..."
# Copy in the latest protobuf messages 
echo "[cloud_service] Copying dependencies"
cp ../../common/message_pb2.py .
cp ../../common/config_pb2.py .
cp ../../common/BaseApp.py .
cp ../../common/TCPClient.py .
cp ../../common/TCPServer.py .
cp ../../common/UDPClient.py .

# Build the docker image and tag it
docker build -t ground.cloud_service .
echo "[cloud_service] Done!"