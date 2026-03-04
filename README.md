# NotifyX – Asynchronous Notification Delivery Service

NotifyX is a backend infrastructure service that decouples notification
delivery from user-facing APIs using background workers and a Redis-backed queue.
It ensures reliable, non-blocking notification processing with retry support.

---

## 🚀 Overview

In production systems, sending emails or push notifications directly inside
API requests can slow down user responses and reduce reliability.

NotifyX solves this by:

- Accepting notification requests via FastAPI
- Persisting them to a database
- Enqueuing delivery jobs to Redis
- Processing them asynchronously using Celery workers
- Retrying failed deliveries with exponential backoff
- Tracking delivery status in the database

---

## 🏗 Architecture

Client Request
    ↓
FastAPI API (POST /notifications)
    ↓
SQLite Database (status = PENDING)
    ↓
Redis Queue
    ↓
Celery Worker
    ↓
Delivery Simulation (Email / Push)
    ↓
Database Update (SENT / FAILED)

---

## ⚙ Tech Stack

- Python
- FastAPI (API layer)
- Celery (background worker)
- Redis (message broker)
- SQLite + SQLAlchemy (persistence)
- Uvicorn (ASGI server)

---

## 🔄 Notification Lifecycle

PENDING → PROCESSING → SENT  
            ↓  
         FAILED (auto-retry, max 3 attempts)

---

## 🛠 How to Run Locally

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt