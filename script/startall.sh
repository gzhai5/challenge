#!/bin/bash

# Check for the -d flag
if [ "$1" == "-d" ] ; then
    DOCKER_FLAGS="-d"
else
    DOCKER_FLAGS=""
fi

# Set the docker-compose.yml file path
DOCKER_COMPOSE_FILE_PATH="../docker/docker-compose.yml"

# Launch Docker Compose
docker-compose -f $DOCKER_COMPOSE_FILE_PATH up --build $DOCKER_FLAGS