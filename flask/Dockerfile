FROM python:3.10

# This is the Dockerfile for the flask app. It's uses the same code
# base as the image for the Celery app, but invokes a different CMD.
#
# The CMD invokes gunicorn listening on port 8001 using the app object
# in app.py in the app directory (hence app.app:app).

WORKDIR /
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir app
COPY . app
CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8001", "app.app:app"]
EXPOSE 8001
