# FlaskCeleryDocker

This repo contains a reference implementation of Flask running tasks using Celery.
The Flask server is invoked by `gunicorn` and sits behind an `nginx` proxy. 
The Celery workers are backed by RabbitMQ. The `flask`, `celery`, `nginx` and `rabbitmq`
processes each runs in its own Docker container.

## Why not docker-compose?

Docker compose would have been easier to use. For this example I didn't want to use it for the 
following reasons:

1. I wanted to learn how to create custom Docker networks so that containers could be named and communicate with each other.
2. I wanted a solution that would allow me to add containers on the fly - for purposes of illustration.
3. I wanted to get a deeper understanding of Docker.

## What's in this repo

There are two demos (sets of sample code) in this project: 

+ `flask/standalone_app.py` that has everything you need in one file
+ The larger docker-based example

## What's _not_ in this repo

This repo does not attempt to explain _why_ one would want to use Celery with Flask. Or what the pros 
and cons are when using RabbitMQ vs Redis. Or what purpose backends serve. This repo is to be used
as part of a one-hour demo/explanation of concepts. There are several good articles and videos about
this online. One of the best ones out there is https://youtu.be/iwxzilyxTbQ.

## The standalone version

+ `cd` into `flask`.
+ Run `pip3 install -r requirements.txt` (You may want to use venv for this).
+ Install and run rabbitmq on your local computer.
  + If you cannot/don't want to do this, then run the docker-based demo.
+ Run `python3 ./standalone_app.py`. This will launch a web server listening on port 8080.
+ In another terminal start the celery worker.
  - In the parent directory of `flask`, run `./start_local_celery.sh`
+ Now direct your browser to http://localhost:8080/flask/heavy.
  + This will kick off a celery task. You should be able to see the logs in the `start_local_celery.sh` output.

## The docker version

### Containers

There are four Docker containers in this system:

1. The `nginx` container hosts the main [Nginx](https://nginx.org/en/docs/) web page and proxy.
   1. Any request with the `/flask` URL prefix is proxied to the `flask` container
2. The `flask` container hosts the [Flask](https://flask.palletsprojects.com/en/2.1.x/) app. This is done via the [gunicorn HTTP server](https://gunicorn.org/).
3. The `rabbitmq` container runs [RabbitMQ](https://www.rabbitmq.com/) which is used as Celery's broker.
4. The `celery` container runs a [Celery](https://docs.celeryq.dev/) worker. One key point of this demo is that once can launch additional celery containers to speed up processing of the queue.

### The container network

These containers need to communicate with each other. The Nginx container needs to proxy to the 
Flask container. The Flask and the Celery containers need to use the broker running in the
RabbitMQ container. 

By default, there is no way to tell what IP address will be assigned to each container. So the 
code and config files cannot specify an IP address to refer to the flask and rabbitmq containers.

The approach this demo uses is to create a Docker bridge network named `my_network`. When the 
containers are created, they are assigned to this network, and assigned a name. Docker will then 
assign the container that name as its hostname on that bridge network. This allows us to use the 
hostname in the code and config files.

### Docker bind mounts

For illustration purposes there are two bind mounts used in this demo. The first is `/document_root`
which is the document root of the nginx server. This is used to show how nginx is used to serve
static files off the document root and also proxy more complicated requests to the Flask web
server.

The second bind mount is `/db`. This is used to host the `backend.db` sqlite3 database file. Both, 
the Flask and Celery containers need to be able to access the Celery backend. I chose to use 
sqlite3 instead of Postgres as a backend database because the former is easier to set up for the
purposes of this demo.

### Container sequence diagram

```mermaid

sequenceDiagram
    participant B as Browser
    participant N as Nginx
    participant F as Flask
    participant R as RabbitMQ
    participant C1 as Celery Worker 1
    participant C2 as Celery Worker 2
    
    B->>N: /flask/heavy
    N->>F: /flask/heavy (via gunicorn)
    F->>R: do_heavy_task.delay()
    C1->>R: <get next task>
    C2->>R: <get next task>

```

### Starting the demo

From the main directory run `build.sh`. This will do the following:

- Create the flask, nginx, celery and rabbitmq images
- Create the bridge network
- Launch each container, assigning it to the the bridge network and giving it a known container name.

### Running the demo

From your browser, visit http://localhost:8000/flask/heavy. This will enqueue a task that takes
between 1 and 3 seconds to complete.

You can view the Celery worker logs by running `docker logs -f my_celery_container`.

You can view the list of tasks in the RabbitMQ queue (that aren't picked up by a worker yet) by
running `list_queues.sh`.

You can have this list of tasks updated approxmiately every two seconds by running `monitor_queue.sh`. 

You can launch a [Locust](https://locust.io/) swarm of load-testing requests by doing the following:

1. `cd locust`
2. `./locust --host http://localhost:8000/`
3. Visit http://localhost:8089
4. Start a load test with 2 - 3 users, and a swarm rate of 1 - 4.

**_Bear in mind that within minutes you will have queued tens of thousands of requests to be
processed by Celery. End this load test quickly._**

Once the load test is stopped, you can run `monitor_queues.sh` to view how quickly the 
queue is processed. You can speed up the processing of the queue by adding more celery workers
via `launch_celery_worker.sh`.

### Task Status

When you visit http://localhost:8000/flask/heavy the Flask server returns a JSON object
that includes the task id. You can use this task id to query the status of the task using 
http://localhost:8000/flask/status?task_id=xxxxx where `xxxxx` is the task id returned by
`/flask/heavy`.

You can retrieve a list of all tasks by visiting http://localhost:8000/flask/tasks.