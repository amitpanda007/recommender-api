from rec_app.app import app
from rec_app.task_queue.celery_config import init_celery, celery

init_celery(celery, app)