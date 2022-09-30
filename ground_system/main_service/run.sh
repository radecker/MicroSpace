#!/bin/bash
docker run -v /home/admin/MicroSpaceFALL2022/ground_service/main_service/config.yaml:/usr/src/app/config.yaml:ro --network=host ground.main_service