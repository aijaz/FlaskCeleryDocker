from flask import Flask
from random import randint
from time import sleep


app = Flask(__name__)


@app.route("/flask/heavy")
def accept_heavy_task_request():

    sleep_time = randint(5, 10)
    result = do_heavy_task(sleep_time)
    return {"result": result}


def do_heavy_task(sleep_time):
    sleep(sleep_time)
    return f"This task took {sleep_time} seconds."


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999)
