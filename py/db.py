"""
اتصال به دیتابیس PostgreSQL با SQLAlchemy.
این ماژول engine و SessionLocal و Base رو می‌سازه.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. "
        "Example: postgresql+psycopg2://user:pass@localhost:5432/news_db"
    )

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# Base = کلاس پایه‌ای که همه‌ی جدول‌ها ازش ارث می‌برن
Base = declarative_base()


def get_db():
    """
    FastAPI از این تابع استفاده می‌کنه تا
    به هر درخواست یه session بده و آخر ببنده.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """جداول رو می‌سازه (اگه نباشن)."""
    from py import db_models  # noqa: F401
    Base.metadata.create_all(bind=engine)
