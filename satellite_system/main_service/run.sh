#!/bin/bash
docker run -v /home/admin/MicroSpaceFALL2022/satellite_system/main_service/config.yaml:/usr/src/app/config.yaml:ro --network=host vehicle.main_service