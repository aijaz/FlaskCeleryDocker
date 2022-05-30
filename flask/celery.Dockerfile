FROM python:3.10

# This is the Dockerfile for the celery worker. It's uses the same
# code base as the image for the Flask app, but invokes a different
# CMD.
#
# Note that the CMD specifies app.app.celery, because in app.py the
# name of the Celery object is 'celery', not 'app'.

WORKDIR /
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir app
COPY . app
CMD ["celery", "-A", "app.app.celery", "worker", "--loglevel=info"]
