#!/bin/bash

scriptPath="$( cd "$(dirname "$0")" && pwd -P )"

source "$scriptPath/../environment.sh"

docker run -p 8086:8086 \
      -v influxdb2:/var/lib/influxdb2 \
      -e DOCKER_INFLUXDB_INIT_USERNAME="$INFLUXDB_INIT_USERNAME" \
      -e DOCKER_INFLUXDB_INIT_PASSWORD="$INFLUXDB_INIT_USERNAME" \
      -e DOCKER_INFLUXDB_INIT_ORG="$INFLUXDB_INIT_ORG" \
      -e DOCKER_INFLUXDB_INIT_BUCKET="$INFLUXDB_INIT_BUCKET" \
      influxdb:2.0
