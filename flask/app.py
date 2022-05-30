from random import randint
from time import sleep
import sqlite3

from flask import Flask, jsonify,  request, current_app
from celery import Celery
from celery.result import AsyncResult

# The flask app
app = Flask(__name__)

# Celery also has a default convention of using 'app' as the celery app.
# But we cannot do that here, because we're using 'app' to refer to the
# flask app. Celery has a secondary convention of using 'celery' as the
# name of the celery app.
#
# Create a celery app using the rabbitmq instance running on
# my_rabbitmq_container as the broker. Use the SQLite3 database located
# at /db/backend.db as the Celery backend.
celery = Celery(broker="amqp://my_rabbitmq_container//", backend='db+sqlite:///db/backend.db')


@app.route("/flask")
def hello_world():
    return {"message": "Hello from flask."}


@app.route("/flask/heavy")
def accept_heavy_task_request():
    """
    Simulate a request to perform a time-consuming task

    :return: a JSON object containing the task_id
    """

    # First, determine a random length for this fake task.
    # Then, call delay() on the task.
    # Finally, extract the task id from return value of delay() and return it.
    #
    # Calling delay() on a task is a shortcut for apply_async.
    # delay() looks more 'natural' when you're starting off.
    #
    # Normally we would calculate the sleep time inside the task. But
    # we're doing it here to illustrate how to pass arguments to delay().
    #
    # NOTE: what's returned here is not the return value of the task.
    # The task has likely not even started yet.
    # That's the point of this example: Return quickly and let the task
    # run later.

    sleep_time = randint(1, 3)

    new_task = do_heavy_task.delay(sleep_time)

    return {"task_id": new_task.id}


@app.route("/flask/status")
def status():
    """
    Get the status of a task
    :return: A JSON object containing the task id, status and result
    """

    # If the task has completed, call get() on the task result to release resources
    # at the backend. See the Celery documentation for more info on this.

    if task_id := request.args.get('task_id'):
        if res := AsyncResult(task_id):
            if res.status != 'PENDING':
                res.get()
            return {"task_id": task_id, "status": res.status, "result": res.result}
        else:
            return "Not Found", 404
    return "No task_id specified", 400


@app.route("/flask/tasks")
def tasks():
    """
    Get the status of all pending or completed tasks.
    :return: a JSON object containing a list of all tasks that made it to the backend
    """

    # Create a connection. The row factory returns each row as a dictionary.

    con = sqlite3.connect('/db/backend.db')
    con.row_factory = lambda cursor, rw: {cursor.description[idx][0]: value for idx, value in enumerate(rw)}
    cur = con.cursor()
    cur.execute('select task_id, status, date_done from celery_taskmeta')  # noqa
    rows = cur.fetchall()
    for row in rows:
        row['result'] = AsyncResult(row['task_id']).result
    current_app.logger.info(rows)
    cur.close()
    con.close()
    return {"data": rows}


@celery.task(name="heavy_task", bind=True)
def do_heavy_task(self, sleep_time):
    """
    A time-consuming task. This is the task called by the Celery worker because it
    takes too much time to be part of the HTTP request life-cycle. It is decorated
    with the @celery.task decorator, where celery is the name of the celery app
    defined earlier in the file. It's a good practice to name the task explicitly

    The 'bind' flag indicates the first parameter of the task should be 'self' - the task.
    This is useful if you want to query the task, to get its ID, for example,
    as we're doing here.

    :param self: The celery task
    :param sleep_time: The number of seconds to sleep (simulating a long-running task)
    :return: A status string
    """

    print(f"{self.request.id}: This is a heavy task. Sleeping for {sleep_time} seconds.")
    sleep(sleep_time)
    print(f"{self.request.id}: I'm awake.")
    return f"This task took {sleep_time} seconds."
