"""
ثبت رشته‌ها در دیتابیس از فایل CSV.
اجرا: python -m scripts.seed_fields
"""

import csv
from pathlib import Path

from py.db import SessionLocal, init_db
from py.db_models import Category, Field

CSV_FILE = Path(__file__).parent.parent / "data" / "field_mapping.csv"


def seed():
    if not CSV_FILE.exists():
        print(f" فایل پیدا نشد: {CSV_FILE}")
        print("اول این را اجرا کن: python -m scripts.build_field_mapping")
        return

    init_db()
    db = SessionLocal()

    try:
        # ۱. خواندن همه دسته‌ها به صورت dict
        categories = {c.name: c.id for c in db.query(Category).all()}
        if not categories:
            print(" هیچ دسته‌ای در دیتابیس نیست.")
            print("اول این را اجرا کن: python -m scripts.seed_categories")
            return

        print(f"تعداد دسته‌های موجود: {len(categories)}")

        # ۲. خواندن CSV و درج رشته‌ها
        inserted = 0
        skipped = 0
        no_category = 0

        # utf-8-sig چون فایل با BOM ذخیره شده
        with CSV_FILE.open("r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                field_name = row["field_name"].strip()
                cat_name = row["category_name"].strip()

                # چک کن دسته وجود دارد
                if cat_name not in categories:
                    print(f" دسته ناشناخته '{cat_name}' برای رشته '{field_name}'")
                    no_category += 1
                    continue

                # چک کن رشته قبلاً ثبت نشده
                exists = db.query(Field).filter_by(name=field_name).first()
                if exists:
                    skipped += 1
                    continue

                db.add(Field(
                    name=field_name,
                    category_id=categories[cat_name],
                ))
                inserted += 1

        db.commit()

        print()
        print("=" * 50)
        print(f"رشته‌های ثبت‌شده: {inserted}")
        print(f"رشته‌های موجود (رد شده): {skipped}")
        print(f"رشته‌های بدون دسته: {no_category}")
        print(f" مجموع رشته‌ها در دیتابیس: {db.query(Field).count()}")
        print("=" * 50)

    except Exception as e:
        db.rollback()
        print(f" خطا: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
