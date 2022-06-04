from flask import Flask
from random import randint
from time import sleep
from celery import Celery


app = Flask(__name__)
celery = Celery(broker="amqp://localhost//")


@app.route("/flask/heavy")
def accept_heavy_task_request():
    sleep_time = randint(5, 10)
    task = do_heavy_task.delay(sleep_time)
    return {"result": task.task_id}


@celery.task(name="heavy_task", bind=True)
def do_heavy_task(self, sleep_time):
    sleep(sleep_time)
    return f"This task ({self.request.id}) took {sleep_time} seconds."


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999)
