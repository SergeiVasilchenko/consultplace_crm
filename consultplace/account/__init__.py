default_app_config = 'account.apps.AccountConfig'

# from .root import app as celery_app
from root.celery import app as celery_app

__all__ = ('celery_app',)
