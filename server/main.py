"""
سرور دریافت ورودی خبر.
- POST /api/news  → دریافت، auth، validate، ذخیره
- GET  /health    → بررسی سلامت
"""

import os
import logging

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from dotenv import load_dotenv

from py.db import get_db, init_db, engine
from py.db_models import MainRecord
from py.schemas import NewsRequest, NewsResponse, HealthResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("news_server")

load_dotenv()

SHARED_SECRET = os.getenv("SHARED_SECRET")
if not SHARED_SECRET:
    raise RuntimeError("SHARED_SECRET is not configured in .env")


app = FastAPI(
    title="News Intake Server",
    description="دریافت اطلاعات پایان‌نامه و ذخیره در دیتابیس",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup():
    try:
        init_db()
        logger.info("Database initialized.")
    except Exception as e:
        logger.error(f"Failed to init DB: {e}")
        raise


@app.post(
    "/api/news",
    response_model=NewsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="دریافت و ذخیره اطلاعات پایان‌نامه",
)
def receive_news(payload: NewsRequest, db: Session = Depends(get_db)):
    # 1) احراز هویت
    if payload.shared_Secret != SHARED_SECRET:
        logger.warning(f"Auth failed for username={payload.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid shared secret",
        )

    # 2) ذخیره (بدون shared_Secret)
    record = MainRecord(
        username=payload.username,
        title=payload.title,
        abstract=payload.abstract,
        university=payload.university,
        table_of_contents=payload.table_of_contents,
        author=payload.author,
        supervisor=payload.supervisor,
        status="ready",
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    logger.info(f"Stored record id={record.id} username={record.username}")

    return NewsResponse(
        id=record.id,
        status=record.status,
        message="Record stored successfully",
    )


@app.get("/health", response_model=HealthResponse)
def health():
    db_status = "ok"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"DB health check failed: {e}")
        db_status = "error"

    return HealthResponse(status="ok", db=db_status)
