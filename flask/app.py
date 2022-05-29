from flask import Flask
from celery import Celery

app = Flask(__name__)
# celery = Celery(broker="amqp://aijaz_rabbitmq_container//", backend='db+postgresql://postgres:mysecretpassword@aijaz_postgres_container/postgres')
celery = Celery(broker="amqp://aijaz_rabbitmq_container//")


@app.route("/flask")
def hello_world():
    return "<p>Hello, World! This is Flask</p>"


@app.route("/flask/upload_image")
def upload():
    do_heavy_task.delay()
    return "Uploading"


@app.route("/flask/list_uploads")
def list_uploads():
    return "OK"


@celery.task(name="heavy_task")
def do_heavy_task():
    with open("/document_root/baz", "w") as f:
        f.write("This is a heavy task.")
    print("This is a heavy task")
