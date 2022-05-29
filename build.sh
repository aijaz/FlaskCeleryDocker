#!/bin/bash

set -e

for f in flask nginx rabbitmq;
  do
    pushd $f || exit 1
    ./build.sh
    popd || exit 1
  done



docker network create --driver bridge aijaz_network || true

docker run -d -it --name aijaz_rabbitmq_container -v "$(pwd)"/document_root:/document_root -v "$(pwd)"/db:/db --network aijaz_network aijaz_rabbitmq
docker run -d -it --name aijaz_flask_container    -v "$(pwd)"/document_root:/document_root -v "$(pwd)"/db:/db --network aijaz_network aijaz_flask
docker run -d -it --name aijaz_celery_container   -v "$(pwd)"/document_root:/document_root -v "$(pwd)"/db:/db --network aijaz_network aijaz_celery
docker run -d -it --name aijaz_nginx_container    -v "$(pwd)"/document_root:/document_root -v "$(pwd)"/db:/db --network aijaz_network -p 8000:80 aijaz_nginx
