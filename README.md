# News Generation Pipeline

پروژه‌ی تولید خبر خودکار از چکیده پایان‌نامه، مبتنی بر Python، FastAPI، PostgreSQL و PydanticAI.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=flat-square&logo=pydantic&logoColor=white)

---

## فهرست مطالب

- [معماری کلی](#معماری-کلی)
- [ساختار پروژه](#ساختار-پروژه)
- [مدل داده (ERD)](#مدل-داده-erd)
- [پیش‌نیازها](#پیشنیازها)
- [نصب و راه‌اندازی](#نصب-و-راهاندازی)
- [API Endpoints](#api-endpoints)
- [تست](#تست)
- [مستندات بیشتر](#مستندات-بیشتر)

---

## معماری کلی

```text
JSON Input
    |
    v
API Server (FastAPI)
    |-- Auth (shared_secret)
    |-- Validation (Pydantic)
    |-- Field -> Category Mapping
    |
    v
PostgreSQL  [status = 'ready']
    |
    v
Worker
    |-- Preprocess
    |-- Classify
    |-- LLM Generation
    |
    v
output_json
    |
    v
WebUI / Telegram / Bale / Web
```

---

## ساختار پروژه

```text
news_project/
├── py/
│   ├── db.py                   # اتصال SQLAlchemy
│   ├── db_models.py            # ۵ جدول دیتابیس
│   ├── models.py               # NewsInput, GeneratedNews
│   ├── schemas.py              # Pydantic schemas برای API
│   └── agent.py                # Agent تولید خبر
│
├── server/
│   └── main.py                 # FastAPI app
│
├── scripts/
│   ├── build_field_mapping.py
│   ├── seed_categories.py
│   ├── seed_fields.py
│   ├── seed_prompts.py
│   ├── check_data.py
│   └── compare_prompts.py
│
├── migrations/
│   └── 001_create_tables.sql
│
├── data/
│   ├── categories.json
│   ├── field_mapping.csv
│   ├── fields.xlsx
│   └── sample_input_*.json
│
├── docs/
│   ├── erd.md
│   ├── erd.png
│   ├── prompt_v1.txt
│   ├── prompt_v2.txt
│
├── tests/
│   └── test_server.py
│
├── .env.example
├── requirements.txt
└── README.md
```

---

## مدل داده (ERD)

نمودار رابطه‌ی جداول:

```text
categories --o{ fields    : دارد
categories --o{ main      : دسته‌بندی می‌کند
fields     --o{ main      : رشته‌ی پایان‌نامه
models     --o{ main      : پردازش با
prompts    ||--o{ main    : تولید با
```

تصویر کامل نمودار: [`docs/erd.png`](docs/erd.png)

کد Mermaid: [`docs/erd.md`](docs/erd.md)

### جداول اصلی

| جدول | توضیح |
|:---|:---|
| `categories` | دسته‌بندی موضوعی کلی (۱۵ دسته) |
| `fields` | رشته‌های تخصصی نگاشت‌شده به دسته‌ها |
| `models` | مدل‌های LLM استفاده‌شده |
| `prompts` | نسخه‌های مختلف پرامپت |
| `main` | رکوردهای دریافتی و خروجی خبر |

---

## پیش‌نیازها

| نیازمندی | نسخه |
|:---|:---|
| Python | 3.11+ |
| PostgreSQL | 14+ |
| AvalAI API Key | الزامی |

---

## نصب و راه‌اندازی

### ۱. کلون کردن پروژه

```bash
git clone <https://github.com/MohadeseAnsari/news_project>
cd news_project
```

### ۲. ساخت محیط مجازی

ویندوز:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

لینوکس / مک:

```bash
python -m venv .venv
source .venv/bin/activate
```

### ۳. نصب پکیج‌ها

```bash
pip install -r requirements.txt
```

### ۴. پیکربندی محیط

فایل `.env` را از روی `.env.example` بسازید و مقادیر زیر را تنظیم کنید:

```env
AVALAI_API_KEY=your-avalai-key
SHARED_SECRET=your-secret-key
DATABASE_URL=postgresql+psycopg2://news_user:news_pass@localhost:5432/news_db
```

### ۵. راه‌اندازی دیتابیس

ورود به PostgreSQL:

```bash
psql -U postgres
```

اجرای دستورات زیر در محیط psql:

```sql
CREATE DATABASE news_db;
CREATE USER news_user WITH PASSWORD 'news_pass';
GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;
\c news_db
GRANT ALL ON SCHEMA public TO news_user;
\q
```

جداول هنگام بالا آمدن سرور به‌صورت خودکار ساخته می‌شوند. برای ساخت دستی:

```bash
python -c "from py.db import init_db; init_db()"
```

### ۶. بارگذاری داده‌های مرجع

```bash
python -m scripts.seed_categories
python -m scripts.seed_fields
```

### ۷. اجرای سرور

```bash
uvicorn server.main:app --reload
```

Swagger UI در آدرس زیر در دسترس خواهد بود:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### POST /api/news

دریافت اطلاعات پایان‌نامه و ذخیره در دیتابیس.

**Request Body:**

```json
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
```

**Response (201 Created):**

```json
{
  "id": 1,
  "status": "ready",
  "message": "Record stored successfully"
}
```

---

### GET /health

بررسی سلامت سرور و اتصال به دیتابیس.

**Response:**

```json
{
  "status": "ok",
  "db": "ok"
}
```

---

### کدهای وضعیت HTTP

| کد | معنی | زمان |
|:---:|:---|:---|
| 201 | Created | ثبت موفق رکورد |
| 401 | Unauthorized | `shared_Secret` اشتباه یا غایب |
| 422 | Unprocessable Entity | اعتبارسنجی Pydantic رد شد |
| 500 | Internal Server Error | خطای داخلی سرور |

---

## رفتار با رشته ناشناخته

اگر مقدار `field` در درخواست، در جدول `fields` موجود نباشد:

- رکورد همچنان ذخیره می‌شود (برای جلوگیری از از دست رفتن داده)
- مقدار `field_id` برابر `NULL` می‌شود
- مقدار `category_id` به دسته‌ی `other` نگاشت می‌شود

این رفتار با هدف حفظ داده و امکان بازبینی دستی در مرحله‌ی بعد طراحی شده است.

---

## انتخاب دیتابیس

پروژه بر پایه‌ی PostgreSQL ساخته شده است (طبق نیازمندی تکلیف). کد با SQLAlchemy نوشته شده و در صورت نیاز با تغییر مقدار `DATABASE_URL` می‌توان به SQLite مهاجرت کرد.

---

## تست

اجرای تست‌های سرور:

```bash
python -m tests.test_server
```

---

## مستندات بیشتر

| فایل | توضیح |
|:---|:---|
| [`docs/erd.md`](docs/erd.md) | نمودار ERD با فرمت Mermaid |
| [`docs/erd.png`](docs/erd.png) | تصویر نمودار ERD |
| [`docs/framework_choice.md`](docs/framework_choice.md) | دلیل انتخاب فریم‌ورک‌ها |
| [`docs/prompt_v1.txt`](docs/prompt_v1.txt) | پرامپت نسخه اول |
| [`docs/prompt_v2.txt`](docs/prompt_v2.txt) | پرامپت بهبودیافته نسخه دوم |
| [`docs/prompt_comparison.md`](docs/prompt_comparison.md) | مقایسه تفصیلی v1 و v2 |
| [`migrations/001_create_tables.sql`](migrations/001_create_tables.sql) | SQL ساخت جداول |