from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EducationalPortal.settings')

app = Celery('EducationalPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-mail-every-day': {
        'task': 'courses.tasks.send_beat_email',
        'schedule': crontab(minute=0, hour=0),
    },
}
