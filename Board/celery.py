import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Board.settings')

app = Celery('Board')
app.config_from_object('django.conf.settings', namespace='CELERY')

app.conf.beat_schedule = {
    """Рассылка новостей в 0 часов каждый день"""
    'add-weekly-mailings': {
        'task': 'bill_board.tasks.periodic_mailing',
        'schedule': crontab(hour=0, minute=0),
    },
}


app.autodiscover_tasks()
