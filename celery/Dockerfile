FROM python:3.10

WORKDIR /
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir app
COPY . app
CMD ["celery", "-A app.tasks.celery", "worker", "--loglevel=info"]

