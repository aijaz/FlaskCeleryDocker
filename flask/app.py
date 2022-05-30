from random import randint
from time import sleep
import sqlite3

from flask import Flask, jsonify,  request, current_app
from celery import Celery
from celery.result import AsyncResult

# The flask app
app = Flask(__name__)

# Celery also has a default convention of using 'app' as the celery app.
# But we cannot do that here, because we're using 'app' to refer to the flask app.
# Celery has a secondary convention of using 'celery' as the name of the celery app.
# Create a celery app using the rabbitmq instance running on my_rabbitmq_container as the broker.
# Use the SQLite3 database located at /db/backend.db as the Celery backend.
celery = Celery(broker="amqp://my_rabbitmq_container//", backend='db+sqlite:///db/backend.db')


@app.route("/flask")
def hello_world():
    return json_response({"message": "Hello from flask."})


@app.route("/flask/heavy")
def accept_heavy_task_request():
    sleep_time = randint(1, 3)
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


@app.route("/flask/tasks")
def tasks():
    con = sqlite3.connect('/db/backend.db')
    con.row_factory = lambda cursor, row: {cursor.description[idx][0]: value for idx, value in enumerate(row)}
    cur = con.cursor()
    cur.execute('select task_id, status, date_done from celery_taskmeta')
    rows = cur.fetchall()
    for row in rows:
        row['result'] = AsyncResult(row['task_id']).result
    current_app.logger.info(rows)
    cur.close()
    con.close()
    return json_response({"result": rows})


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
