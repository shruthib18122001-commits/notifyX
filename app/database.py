from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session

# SQLite database URL (file-based DB for simplicity)
DATABASE_URL = "sqlite:///./notifyx.db"

# Create the SQLAlchemy engine
# check_same_thread=False is required for SQLite with FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session factory for database interactions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models
Base = declarative_base()

# Dependency used by FastAPI endpoints
# Ensures DB sessions are opened and closed safely per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
