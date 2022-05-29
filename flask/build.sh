#!/bin/bash

docker build -t aijaz_flask .
docker build -f celery.Dockerfile -t aijaz_celery .
