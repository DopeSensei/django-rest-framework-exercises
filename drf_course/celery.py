import os
from celery import Celery

# Set the default Django settings module for the 'celery' program
# Neden: Celery worker Django ayarlarini (DB, CACHE, EMAIL) kullanabilsin.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_course.settings')

app = Celery('drf_course')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
# should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')  # settings.py icindeki CELERY_* anahtarlarini otomatik okur.

if __name__ == "__main__":  # Bu dosya direkt calistirilirsa celery worker'i baslatir (debug/manuel).
    app.start()
