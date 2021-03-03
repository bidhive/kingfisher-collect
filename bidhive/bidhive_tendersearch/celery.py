from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", os.path.join("bidhive_tendersearch.settings")
)
app = Celery("bidhive_tendersearch")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
