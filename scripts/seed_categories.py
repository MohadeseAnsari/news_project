"""
ثبت دسته‌های موضوعی در دیتابیس.
اجرا: python -m scripts.seed_categories
"""

import json
from pathlib import Path

from py.db import SessionLocal, init_db
from py.db_models import Category

DATA_FILE = Path(__file__).parent.parent / "data" / "categories.json"


def seed():
    if not DATA_FILE.exists():
        print(f" فایل پیدا نشد: {DATA_FILE}")
        return

    init_db()
    db = SessionLocal()

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            categories = json.load(f)

        inserted = 0
        skipped = 0

        for cat in categories:
            exists = db.query(Category).filter_by(name=cat["name"]).first()
            if exists:
                skipped += 1
                continue
            db.add(Category(
                name=cat["name"],
                description=cat["description"],
            ))
            inserted += 1

        db.commit()
        print(f" دسته‌های ثبت‌شده: {inserted}")
        print(f"  دسته‌های موجود (رد شده): {skipped}")
        print(f" مجموع دسته‌ها: {db.query(Category).count()}")

    except Exception as e:
        db.rollback()
        print(f" خطا: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
