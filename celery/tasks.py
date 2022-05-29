from celery import Celery

celery = Celery(broker="amqp://aijaz_rabbitmq_container//", backend='db+postgresql://postgres:mysecretpassword@aijaz_postgres_container/postgres')


@celery.task(name="heavy_task")
def do_heavy_task():
    print("This is a heavy task")
