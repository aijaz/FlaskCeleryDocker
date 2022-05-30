#!/bin/bash

# shellcheck disable=SC2164
cd flask

# Invoke a celery worker for the celery app in standalone_app.celery
celery -A standalone_app.celery worker --loglevel=info