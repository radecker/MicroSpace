#!/bin/bash
set -e
set -o pipefail

# Run the common library build first
cd ../common/
./build.sh
cd ../satellite_system/hal_service/

# Build the critical infrastructure (i.e. any service)
#cd ../hal_service/
./build.sh
cd ../logger_service/
./build.sh
cd ../main_service/
./build.sh
cd ../sdr_app/
./build.sh

# Build the custom apps
cd ../autonomy_app/
./build.sh
cd ../demo_app/
./build.sh

# Remove the old dangling images to reduce disk usage (TODO: Make this work)
# docker rmi $(docker images -qa -f 'dangling=true') 