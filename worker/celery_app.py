from celery import Celery

# Create Celery application
celery_app = Celery(
    "notifyx",

    # Redis acts as the message broker
    broker="redis://localhost:6379/0",

    # Redis also stores task results and retry metadata
    backend="redis://localhost:6379/0"
)

# Route all notification tasks to a dedicated queue
celery_app.conf.task_routes = {
    "worker.tasks.*": {"queue": "notifications"}
}
