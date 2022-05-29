from random import randint
from time import sleep

from flask import Flask, jsonify,  request
from celery import Celery
from celery.result import AsyncResult

app = Flask(__name__)
celery = Celery(broker="amqp://aijaz_rabbitmq_container//", backend='db+sqlite:///db/backend.db')


@app.route("/flask")
def hello_world():
    return json_response({"message": "Hello from flask."})


@app.route("/flask/heavy")
def accept_heavy_task_request():
    sleep_time = randint(20, 30)
    new_task = do_heavy_task.delay(sleep_time)
    return json_response({"message": f"Started task with id {new_task.id}"})


@app.route("/flask/status")
def status():
    if task_id := request.args.get('task_id'):
        if res := AsyncResult(task_id):
            if res.status != 'PENDING':
                res.get()
            return json_response({"task_id": task_id, "status": res.status, "result": res.result})
        else:
            return json_response({}, 404)
    return json_response({"error": "No task_id specified"})


@celery.task(name="heavy_task", bind=True)
def do_heavy_task(self, sleep_time):
    print(f"{self.request.id}: This is a heavy task. Sleeping for {sleep_time} seconds.")
    sleep(sleep_time)
    print(f"{self.request.id}: I'm awake.")
    return f"This task took {sleep_time} seconds."


def json_response(the_dict, status_code=200, headers=None):
    if headers is None:
        headers = {}
    resp = jsonify(the_dict)
    resp.status_code = status_code
    for header in headers.keys():
        resp.headers[header] = headers[header]
    return resp
