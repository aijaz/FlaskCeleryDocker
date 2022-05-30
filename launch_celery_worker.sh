#!/bin/bash

# Launch another docker container based off of the my_celery image.
# Note: We don't specify a name here. Let Docker choose the name.
# We don't really need to specify a name for Celery workers.

docker run -d -it  -v "$(pwd)"/document_root:/document_root -v "$(pwd)"/db:/db --network my_network my_celery
