from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Notification
from worker.tasks import send_notification_task
from fastapi import HTTPException

# Create FastAPI app
app = FastAPI(title="NotifyX")

# Create DB tables at startup
# (in production this is handled via migrations)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    # Health check endpoint for monitoring / load balancers
    return {"status": "ok"}

@app.post("/notifications")
def create_notification(
    recipient: str,
    message: str,
    db: Session = Depends(get_db)
):
    """
    Accepts a notification request and enqueues it
    for asynchronous delivery.
    """

    # Create a new notification record
    notification = Notification(
        recipient=recipient,
        message=message,
        status="PENDING"
    )

    # Persist to database
    db.add(notification)
    db.commit()
    db.refresh(notification)

    # Enqueue background task (non-blocking)
    # The API returns immediately after this
    send_notification_task.delay(notification.id)

    # Respond quickly to the client
    return {
        "id": notification.id,
        "status": notification.status
    }

@app.get("/notifications/{notification_id}")
def get_notification_status(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """
    Fetch the current status of a notification.
    Used by clients to track async delivery.
    """

    # Query notification by ID
    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()

    # If not found, return 404
    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    # Return relevant status information
    return {
        "id": notification.id,
        "recipient": notification.recipient,
        "message": notification.message,
        "status": notification.status,
        "retry_count": notification.retry_count
    }