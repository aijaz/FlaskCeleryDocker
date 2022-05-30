#!/bin/bash

# build the my_flask image
docker build -t my_flask .

# build the image of the celery worker using a different Dockerfile
docker build -f celery.Dockerfile -t my_celery .
