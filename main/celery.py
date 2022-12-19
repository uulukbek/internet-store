import os
import django
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()
app = Celery('main')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



app.conf.beat_schedule = {
    'send-spam': {
        'task': 'main.tasks.spam_message',
        'schedule': crontab(minute='*/1')
    }
}