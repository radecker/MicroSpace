#!/bin/bash

# Copy in the latest protobuf messages 
cp ../../common/message_pb2.py .
cp ../../common/config_pb2.py .
cp ../../common/BaseApp.py .
cp ../../common/TCPClient.py .
cp ../../common/UDPClient.py .

# Build the docker image and tag it
docker build -t ground.logger_service .