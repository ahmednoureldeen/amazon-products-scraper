import os
from datetime import timedelta

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

CELERY_BROKER_URL = 'pyamqp://guest@localhost:5672//'

app = Celery('main', broker=CELERY_BROKER_URL)

app.conf.broker_connection_retry_on_startup = True

# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'trigger-scraper-every-24-hours': {
        'task': 'scraper.tasks.scrape',
        'schedule': timedelta(hours=6),
    },
}