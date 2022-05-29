from random import randint
from time import sleep

from flask import Flask
from celery import Celery

app = Flask(__name__)
celery = Celery(broker="amqp://localhost//")


@app.route("/flask/heavy")
def accept_heavy_task_request():
    sleep_time = randint(1, 3)
    new_task = do_heavy_task.delay(sleep_time)
    return {"message": f"Started task with id {new_task.id}"}


@celery.task(name="heavy_task", bind=True)
def do_heavy_task(self, sleep_time):
    print(f"{self.request.id}: This is a heavy task. Sleeping for {sleep_time} seconds.")
    sleep(sleep_time)
    print(f"{self.request.id}: I'm awake.")
    return f"This task took {sleep_time} seconds."


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
