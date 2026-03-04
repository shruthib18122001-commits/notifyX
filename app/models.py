from sqlalchemy import Column, Integer, String
from app.database import Base

# Notification table tracks delivery lifecycle
class Notification(Base):
    __tablename__ = "notifications"

    # Unique identifier for each notification
    id = Column(Integer, primary_key=True, index=True)

    # Who the notification is sent to (email / user id)
    recipient = Column(String, index=True)

    # Notification message content
    message = Column(String)

    # Current delivery status:
    # PENDING → PROCESSING → SENT / FAILED
    status = Column(String, default="PENDING")

    # Number of retry attempts made by the worker
    retry_count = Column(Integer, default=0)
