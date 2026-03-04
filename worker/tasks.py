import time
from worker.celery_app import celery_app
from app.database import SessionLocal
from app.models import Notification

@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3}
)
def send_notification_task(self, notification_id: int):
    """
    Background task that delivers a notification.
    Automatically retries on failure.
    """

    # Create DB session manually (workers are not FastAPI)
    db = SessionLocal()

    try:
        # Fetch notification by ID
        notification = db.query(Notification).get(notification_id)

        if not notification:
            return

        # Mark as processing
        notification.status = "PROCESSING"
        db.commit()

        # Simulate notification delivery
        # (email / push provider would go here)
        print(
            f"Sending notification to {notification.recipient}: "
            f"{notification.message}"
        )

        # Simulate network delay
        time.sleep(2)

        # Mark as successfully sent
        notification.status = "SENT"
        db.commit()

    except Exception as e:
        # Update failure state
        notification.status = "FAILED"
        notification.retry_count += 1
        db.commit()

        # Re-raise exception so Celery retries
        raise e

    finally:
        # Always close DB session
        db.close()
