#!/bin/bash

# shellcheck disable=SC2046
# shellcheck disable=SC2160
while [ true ] ; do echo $(date) $(./list_queues.sh | grep -e '^celery\t'); sleep 1; done