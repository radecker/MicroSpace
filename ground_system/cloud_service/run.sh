#!/bin/bash
docker run -v /home/jhu-ep/.aws/credentials:/root/.aws/credentials:ro --network=host ground.cloud_service