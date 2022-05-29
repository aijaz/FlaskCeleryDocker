#!/bin/bash

set -e

for f in flask nginx rabbitmq postgres;
  do
    pushd $f || exit 1
    ./build.sh
    popd || exit 1
  done



docker network create --driver bridge aijaz_network || true

docker run -d -it --name aijaz_postgres_container -v "$(pwd)"/document_root:/document_root -e POSTGRES_PASSWORD=mysecretpassword --network aijaz_network aijaz_postgres

docker run -d -it --name aijaz_rabbitmq_container -v "$(pwd)"/document_root:/document_root --network aijaz_network aijaz_rabbitmq

docker run -d -it --name aijaz_flask_container -v "$(pwd)"/document_root:/document_root -p 8001:8001 --network aijaz_network aijaz_flask

docker run -d -it --name aijaz_nginx_container -v "$(pwd)"/document_root:/document_root -p 8000:80 --network aijaz_network aijaz_nginx

