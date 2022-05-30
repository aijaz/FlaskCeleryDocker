#!/bin/bash

# Run the rabbitmqctl list_queues command on the my_rabbitmq_container container.

docker exec my_rabbitmq_container rabbitmqctl list_queues

