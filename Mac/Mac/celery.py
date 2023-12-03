import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mac.settings')

app = Celery('Mac')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'action_every_30_seconds': {
#         'task': 'tasks.action',
#         'schedule': 30,
#         'args': ("some_arg"),
#     },
# }

# В качестве более реального, пусть и абсолютно бесполезного, примера посмотрим,
# как можно запустить счетчик от 1 до N как периодическую задачу.

app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'rest.tasks.printer',
        'schedule': 5,
        'args': (5,),
    },
}
