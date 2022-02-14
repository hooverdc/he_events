#!/bin/bash

scriptPath="$( cd "$(dirname "$0")" && pwd -P )"

docker build -t he_events "$scriptPath/../."