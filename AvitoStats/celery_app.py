import os
from datetime import timedelta

from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AvitoStats.settings')

app = Celery('AvitoStats')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'parsing-every-1-hour': {
        'task': 'main.tasks.periodic_parsing',
        'schedule': timedelta(hours=1.0),
    },
}
