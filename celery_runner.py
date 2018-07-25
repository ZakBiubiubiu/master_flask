import os
from webapp import create_app
from celery import Celery


def make_celery(app):
    celery=Celery(
        app.import_name,  # 这个是什么玩意？
        broker='amqp://guest:guest@localhost:5672//',
        backend='rpc://',
        include='webapp.tasks'
    )

    #  将task和flask上下文绑定
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


env = os.environ.get('WEBAPP_ENV', 'dev')
flask_app = create_app(
    'webapp.config.%sConfig' % env.capitalize()
)

celery = make_celery(flask_app)