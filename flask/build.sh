#!/bin/bash

docker build -t my_flask .
docker build -f celery.Dockerfile -t my_celery .
