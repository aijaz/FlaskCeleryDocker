#!/bin/bash

set -e

# Delete all data from the backend (start fresh)
echo "delete from celery_taskmeta; delete from celery_tasksetmeta;" | sqlite3 db/backend.db

# Build the images in each of the 3 directories below
for f in flask nginx rabbitmq;
  do
    pushd $f || exit 1
    ./build.sh
    popd || exit 1
  done

# Create a docker network named my_network if one doesn't already exist.
docker network create --driver bridge my_network || true

# Create and launch the four docker containers.
#
# TECHNICALLY we don't need the -it options here. I include them anyway because
# having them means that the output of docker logs is colorized.

docker run -d -it --name my_rabbitmq_container -v "$(pwd)"/document_root:/document_root -v "$(pwd)"/db:/db --network my_network my_rabbitmq
docker run -d -it --name my_flask_container    -v "$(pwd)"/document_root:/document_root -v "$(pwd)"/db:/db --network my_network my_flask
docker run -d -it --name my_celery_container   -v "$(pwd)"/document_root:/document_root -v "$(pwd)"/db:/db --network my_network my_celery
docker run -d -it --name my_nginx_container    -v "$(pwd)"/document_root:/document_root -v "$(pwd)"/db:/db --network my_network -p 8000:80 my_nginx
