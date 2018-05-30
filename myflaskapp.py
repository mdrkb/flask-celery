from flask import Flask
from celery import Celery
from datetime import timedelta

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    CELERYBEAT_SCHEDULE = {
        'run-every-1-minute': {
            'task': 'myflaskapp.print_hello',
            'schedule': timedelta(seconds=60)
        },
    }
)
celery = make_celery(app)

@celery.task()
def add_together(a, b):
    return a + b

@celery.task()
def print_hello():
    print('Hello World!')

@app.route('/')
def home():
    result = add_together.delay(10, 20)
    print(result.wait())
    return 'Welcome to my app!'