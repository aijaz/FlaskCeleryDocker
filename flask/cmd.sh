#!/bin/bash

celery -A app.app.celery worker --loglevel=info --detach

gunicorn -w 4 -b 0.0.0.0:8001 app.app:app