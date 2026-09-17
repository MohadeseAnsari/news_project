"""
بررسی داده‌های ثبت‌شده و گزارش آماری.
اجرا: python -m scripts.check_data
"""

from sqlalchemy import func
from py.db import SessionLocal
from py.db_models import Category, Field


def main():
    db = SessionLocal()
    try:
        total_cats = db.query(Category).count()
        total_fields = db.query(Field).count()

        print("=" * 60)
        print(f"📊 تعداد دسته‌ها: {total_cats}")
        print(f"📊 تعداد رشته‌ها: {total_fields}")
        print("=" * 60)

        # توزیع رشته‌ها در دسته‌ها
        results = (
            db.query(Category.name, func.count(Field.id))
            .outerjoin(Field, Field.category_id == Category.id)
            .group_by(Category.name)
            .order_by(func.count(Field.id).desc())
            .all()
        )

        print("\n📈 توزیع رشته‌ها در دسته‌ها:")
        print("-" * 60)
        for name, count in results:
            pct = (count / total_fields * 100) if total_fields else 0
            bar = "█" * int(pct / 2)
            print(f"  {name:20s} {count:4d}  ({pct:5.1f}%)  {bar}")
        print("-" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()
