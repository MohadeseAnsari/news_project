# News Generation Pipeline

پروژه‌ی تولید خبر خودکار از چکیده پایان‌نامه، با Python، FastAPI، PostgreSQL و PydanticAI.

## معماری کلی

JSON Input
↓
API Server (FastAPI)
↓ Auth (shared_secret)
↓ Validation (Pydantic)
↓ Field → Category Mapping
↓
PostgreSQL
↓ status = 'ready'
↓
Worker
↓ Preprocess → Classify → LLM Generation
↓ output_json
↓
WebUI / Telegram / Bale / Web

## ERD (نمودار رابطه جدول‌ها)

![ERD](docs/erd.png)

[MermaidCode](docs/erd.md)

## پیش‌نیازها

- Python 3.11+
- PostgreSQL 14+
- کلید API از AvalAI

## نصب

bash

git clone <repo-url>
cd news_project

python -m venv .venv
# Windows:
.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt


## پیکربندی

.env file

AVALAI_API_KEY=your-avalai-key
SHARED_SECRET=your-secret-key
DATABASE_URL=postgresql+psycopg2://news_user:news_pass@localhost:5432/news_db

## راه‌اندازی دیتابیس

bash

psql -U postgres

sql

CREATE DATABASE news_db;
CREATE USER news_user WITH PASSWORD 'news_pass';
GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;
\c news_db
GRANT ALL ON SCHEMA public TO news_user;
\q

جداول خودکار هنگام بالا آمدن سرور ساخته می‌شوند. برای ساخت دستی:

bash

python -c "from py.db import init_db; init_db()"

## بارگذاری داده‌های مرجع

bash

python -m scripts.seed_categories
python -m scripts.seed_fields

## اجرای سرور

bash

uvicorn server.main:app --reload

Swagger UI: http://127.0.0.1:8000/docs

## API Endpoints

POST /api/news
دریافت اطلاعات پایان‌نامه و ذخیره در دیتابیس.

## Request:

json

{
  "shared_Secret": "your-secret-key",
  "username": "intern",
  "title": "AI Research Project",
  "abstract": "A university research team has developed...",
  "field": "technology",
  "university": "Example University",
  "table_of_contents": "Introduction, Method, Results",
  "author": "Research Team",
  "supervisor": "Dr. Example"
}

## Response (201 Created):

json

{
  "id": 1,
  "status": "ready",
  "message": "Record stored successfully"
}

## GET /health

بررسی سلامت سرور و اتصال به دیتابیس.

## Response:

json

{
  "status": "ok",
  "db": "ok"
}

## کدهای HTTP

Code	Meaning	When
201	Created	ثبت موفق رکورد
401	Unauthorized	shared_Secret اشتباه یا غایب
422	Unprocessable Entity	اعتبارسنجی Pydantic رد شد
500	Internal Server Error	خطای داخلی سرور

## رفتار با رشته ناشناخته


اگر فیلد field در درخواست، در جدول fields وجود نداشته باشد:

رکورد همچنان ذخیره می‌شود (برای اینکه داده‌ای از دست نرود)

field_id مقدار NULL می‌گیرد

category_id به دسته other نگاشت می‌شود

این رفتار با هدف حفظ داده و امکان بازبینی دستی در مرحله بعد طراحی شده است

## انتخاب دیتابیس

 PostgreSQL استفاده می‌کنیم (انتخاب اصلی طبق تکلیف). کد با SQLAlchemy نوشته شده و در صورت نیازی‌توان با تغییر DATABASE_URL به SQLite مهاجرت کرد.

 ## ساختار پروژه

 news_project/
├── py/
│   ├── db.py               # اتصال SQLAlchemy
│   ├── db_models.py        # ۵ جدول
│   ├── models.py           # NewsInput, GeneratedNews
│   ├── schemas.py          # Pydantic schemas برای API
│   └── agent.py            # Agent تولید خبر
├── server/
│   └── main.py             # FastAPI app
├── scripts/
│   ├── build_field_mapping.py
│   ├── seed_categories.py
│   ├── seed_fields.py
│   ├── seed_prompts.py
│   ├── check_data.py
│   └── compare_prompts.py
├── migrations/
│   └── 001_create_tables.sql
├── data/
│   ├── categories.json
│   ├── field_mapping.csv
│   ├── fields.xlsx
│   └── sample_input_*.json
├── docs/
│   ├── erd.md
│   ├── erd.png
│   ├── framework_choice.md
│   ├── prompt_v1.txt
│   ├── prompt_v2.txt
│   └── prompt_comparison.md
├── tests/
│   └── test_server.py
├── .env.example
├── requirements.txt
└── README.md

## تست

bash

python -m tests.test_server

