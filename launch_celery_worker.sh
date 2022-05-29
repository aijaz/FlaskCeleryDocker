#!/bin/bash

docker run -d -it  -v "$(pwd)"/document_root:/document_root -v "$(pwd)"/db:/db --network my_network amycelery
