import os
from app import celery
from app import create_app
from app.celery import make_celery

app = create_app(os.getenv('FLASK_CONFIG') or 'production')

make_celery(celery, app)