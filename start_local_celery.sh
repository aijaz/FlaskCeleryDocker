#!/bin/bash

cd flask
celery -A standalone_app.celery worker --loglevel=info