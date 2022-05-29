#!/bin/bash

docker run -d -it  -v "$(pwd)"/document_root:/document_root -v "$(pwd)"/db:/db --network aijaz_network aijaz_celery
