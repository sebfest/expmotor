import sys

from celery import Celery

sys.path.append('/expmotor/apps')

app = Celery('expmotor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
