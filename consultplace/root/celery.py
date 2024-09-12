from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

app = Celery('account', broker='redis://194.67.86.225:6379')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
