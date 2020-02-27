from __future__ import absolute_import, unicode_literals
from celery import Celery

# app = Celery('tasks', broker="amqp://apabi:10NsS2mM@localhost:5672//",
#              backend="rpc://")

# app = Celery('tasks', backend='rpc://', broker='pyamqp://')
app = Celery('tasks', backend='redis://localhost', broker='pyamqp://')

# Optional configuration, see the application user guide
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Asia/Shanghai',
    # enable_utc=True,
    result_expires=3600
)

if __name__ == '__main__':
    app.start()
