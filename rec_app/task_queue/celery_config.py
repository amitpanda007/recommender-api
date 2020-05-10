from celery import Celery

from rec_app import settings


def make_celery(app_name=__name__):
    backend = settings.CELERY_RESULT_BACKEND
    broker = settings.CELERY_BROKER_URL
    return Celery(app_name, backend=backend, broker=broker)


celery = make_celery()


def init_celery(celery, app):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
