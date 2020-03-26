from __future__ import absolute_import, unicode_literals
from celery import Celery

# app = Celery('tasks', broker="amqp://apabi:10NsS2mM@localhost:5672//",
#              backend="rpc://")

app = Celery('tasks')
# app = Celery('tasks', backend='redis://localhost:6379/1', broker='pyamqp://')

# Optional configuration, see the application user guide
app.conf.update(
    broker_url = 'pyamqp://',
    result_backend = 'db+sqlite:///results.sqlite',
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Asia/Shanghai',
    result_persistent = True,
    # enable_utc=True,
    result_expires=3600
)

if __name__ == '__main__':
    app.start()
