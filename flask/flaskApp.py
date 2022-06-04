from flask import Flask

app = Flask(__name__)


@app.route("/flask/heavy")
def accept_heavy_task_request():

    result = do_heavy_task()
    return {"result": result}


def do_heavy_task():
    return "This task is done."


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999)
