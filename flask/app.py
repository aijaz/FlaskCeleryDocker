from flask import Flask
from celery import Celery

app = Flask(__name__)
celery = Celery(broker="amqp://aijaz_rabbitmq_container//", backend='db+postgresql://postgres:mysecretpassword@aijaz_postgres_container/postgres')


@app.route("/flask")
def hello_world():
    return "<p>Hello, World! This is Flask</p>"


@app.route("/flask/upload_image")
def upload():
    return "OK"


@app.route("/flask/list_uploads")
def list_uploads():
    return "OK"