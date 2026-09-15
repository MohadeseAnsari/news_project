erDiagram
    categories --o{ fields : "دارد"
    categories --o{ main : "دسته‌بندی می‌کند"
    fields     --o{ main : "رشته‌ی پایان‌نامه"
    models     --o{ main : "پردازش با"
    prompts    ||--o{ main : "تولید با"

    categories {
        int     id           PK "شناسه"
        string  name         UK "نام دسته"
        text    description      "تعریف کوتاه"
        timestamp created_at     "زمان ایجاد"
    }

    fields {
        int     id           PK "شناسه"
        string  name         UK "نام رشته"
        int     category_id  FK "ارجاع به categories"
        timestamp created_at     "زمان ایجاد"
    }

    models {
        int     id           PK "شناسه"
        string  name             "نام مدل"
        string  provider         "سرویس‌دهنده"
        string  version          "نسخه"
        timestamp created_at     "زمان ایجاد"
    }

    prompts {
        int     id           PK "شناسه"
        string  version          "نسخه پرامپت"
        text    system_prompt    "متن پرامپت"
        timestamp created_at     "زمان ایجاد"
    }

    main {
        int     id               PK "شناسه رکورد"
        string  username             "فرستنده"
        string  title                "عنوان پایان‌نامه"
        text    abstract             "چکیده"
        string  university           "دانشگاه"
        text    table_of_contents    "فهرست مطالب"
        string  author               "نویسنده"
        string  supervisor           "استاد راهنما"
        int     field_id         FK "ارجاع به fields"
        int     category_id      FK "ارجاع به categories"
        int     model_id         FK "ارجاع به models"
        int     prompt_id        FK "ارجاع به prompts"
        string  status               "وضعیت پردازش"
        json    output_json          "خروجی خبر"
        text    error_message        "متن خطا"
        timestamp created_at         "زمان دریافت"
        timestamp updated_at         "آخرین بروزرسانی"
    }

    