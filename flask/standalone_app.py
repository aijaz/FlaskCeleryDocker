from random import randint
from time import sleep

from flask import Flask
from celery import Celery

# The Flask app
app = Flask(__name__)

# Celery also has a default convention of using 'app' as the celery app.
# But we cannot do that here, because we're using 'app' to refer to the
# flask app. Celery has a secondary convention of using 'celery' as the
# name of the celery app.
#
# Create a celery app using the rabbitmq instance running on localhost
# as the broker.
celery = Celery(broker="amqp://localhost//")


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
