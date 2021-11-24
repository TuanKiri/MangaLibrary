from app import celery


@celery.task(name='task.email')
def send_email():
    pass