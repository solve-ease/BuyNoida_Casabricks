"""
Celery application configuration
"""
from celery import Celery
from celery.schedules import crontab

from app.config.settings import settings

# Create Celery app
celery_app = Celery(
    "casabricks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.monitoring_tasks"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Configure periodic tasks
celery_app.conf.beat_schedule = {
    "check-stuck-images": {
        "task": "app.tasks.monitoring_tasks.check_stuck_images",
        "schedule": crontab(minute="*/15"),  # Every 15 minutes
    },
    "aggregate-analytics": {
        "task": "app.tasks.monitoring_tasks.aggregate_analytics",
        "schedule": crontab(minute=0),  # Every hour
    },
    "warm-cache": {
        "task": "app.tasks.monitoring_tasks.warm_cache",
        "schedule": crontab(hour=0, minute=0),  # Daily at midnight
    },
}

if __name__ == "__main__":
    celery_app.start()
