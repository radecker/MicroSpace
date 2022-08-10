#!/bin/bash

echo "[autonomy_app] Building..."
# Copy in the latest protobuf messages 
echo "[autonomy_app] Copying dependencies"
cp ../common/message_pb2.py .
cp ../common/config_pb2.py .
cp ../common/BaseApp.py .
cp ../common/TCPClient.py .
cp ../common/TCPServer.py .
cp ../common/UDPClient.py .

# Build the docker image and tag it
docker build -t vehicle.autonomy_app .
echo "[autonomy_app] Done!"