from .celery import app as celery_app

__all__ = ('celery_app')  # Bu modulden disariya sadece celery_app export edilir; Django startup'ta Celery app yuklensin diye.
