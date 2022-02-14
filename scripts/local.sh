#!/bin/bash

#!/bin/bash

scriptPath="$( cd "$(dirname "$0")" && pwd -P )"

# shellcheck source=environment.sh
source "$scriptPath/../environment.sh"

docker run -d \
    -e "HUBITAT_ELEVATION_WEBSOCKET_URL=$HUBITAT_ELEVATION_WEBSOCKET_URL" \
    -e "INFLUXDB_URL=$INFLUXDB_URL" \
    -e "INFLUXDB_TOKEN=$INFLUXDB_TOKEN" \
    -e "INFLUXDB_BUCKET=$INFLUXDB_BUCKET" \
    -e "INFLUXDB_ORG=$INFLUXDB_ORG" \
    he_events
