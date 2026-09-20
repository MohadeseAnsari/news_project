"""
سرور دریافت ورودی خبر.

Endpoints:
    POST /api/news  → دریافت، احراز هویت، اعتبارسنجی، نگاشت و ذخیره
    GET  /health    → بررسی سلامت سرور و دیتابیس
"""

import os
import logging

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from dotenv import load_dotenv

from py.db import get_db, init_db, engine
from py.db_models import MainRecord, Field, Category
from py.schemas import NewsRequest, NewsResponse, HealthResponse

# ---------------- Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("news_server")

load_dotenv()

SHARED_SECRET = os.getenv("SHARED_SECRET")
if not SHARED_SECRET:
    raise RuntimeError("SHARED_SECRET is not configured in .env")


# ---------------- FastAPI app ----------------
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


# ---------------- Helpers ----------------
def resolve_field(
                    db: Session, field_name: str
                 ) -> tuple[int | None, int | None]:
    """
    رشته را به field و category نگاشت می‌کند.
    اگر رشته در جدول fields نباشد، به دسته «other» برمی‌گردد.

    Returns:
        (field_id, category_id)
    """
    field = db.query(Field).filter(Field.name == field_name).first()
    if field:
        return field.id, field.category_id

    # رشته ناشناخته → other
    other = db.query(Category).filter(Category.name == "other").first()
    return None, (other.id if other else None)


# ---------------- Endpoints ----------------
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

    # 2) نگاشت رشته به field و category
    field_id, category_id = resolve_field(db, payload.field)

    # 3) ساخت رکورد
    record = MainRecord(
        username=payload.username,
        title=payload.title,
        abstract=payload.abstract,
        university=payload.university,
        table_of_contents=payload.table_of_contents,
        author=payload.author,
        supervisor=payload.supervisor,
        field_id=field_id,
        category_id=category_id,
        status="ready",
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    logger.info(
        f"Stored record id={record.id} "
        f"username={record.username} "
        f"field='{payload.field}' "
        f"category_id={category_id}"
    )

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
