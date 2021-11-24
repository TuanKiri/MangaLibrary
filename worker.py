from app import celery
from app import create_app
from app.celery import make_celery

app = create_app('default')

make_celery(celery, app)