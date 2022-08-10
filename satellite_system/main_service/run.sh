#!/bin/bash
docker run -v /home/jhu-ep/InSECTS-Vehicle-Testbed/main_service/config.yaml:/usr/src/app/config.yaml:ro --network=host vehicle.main_service