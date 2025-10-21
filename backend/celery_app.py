# Celery configuration
from celery import Celery
from app.config import settings

# Initialize Celery
celery = Celery('clique')

# Celery configuration
celery.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Task routes
celery.conf.task_routes = {
    'workers.import_historical_data': {'queue': 'setup'},
    'workers.setup_ai_cold_start': {'queue': 'setup'},
    'workers.create_baseline_metrics': {'queue': 'setup'},
    'workers.detect_trends': {'queue': 'trends'},
    'workers.run_diagnostics': {'queue': 'analysis'},
    'workers.train_ai_models': {'queue': 'ai'},
    'workers.cleanup_old_data': {'queue': 'maintenance'},
    'workers.process_shopify_order_webhook': {'queue': 'webhooks'},
    'workers.process_meta_ad_webhook': {'queue': 'webhooks'},
    'workers.sync_data_task': {'queue': 'sync'},
}

# Beat schedule
celery.conf.beat_schedule = {
    'detect-trends': {
        'task': 'workers.detect_trends',
        'schedule': 15 * 60,  # Every 15 minutes
    },
    'run-diagnostics': {
        'task': 'workers.run_diagnostics',
        'schedule': 2 * 60 * 60,  # Every 2 hours
    },
    'train-ai-models': {
        'task': 'workers.train_ai_models',
        'schedule': 24 * 60 * 60,  # Daily
    },
    'cleanup-old-data': {
        'task': 'workers.cleanup_old_data',
        'schedule': 7 * 24 * 60 * 60,  # Weekly
    },
}

# Error handling
@celery.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

if __name__ == '__main__':
    celery.start()
