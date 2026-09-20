import os
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)
VALID_SECRET = os.getenv("SHARED_SECRET",
                         "my-super-secret-key-change-in-production")


def payload():
    return {
        "shared_Secret": VALID_SECRET,
        "username": "intern",
        "title": "AI Research Project",
        "abstract":
        "A university research team has developed a new AI method.",
        "field": "technology",
        "university": "Example University",
        "table_of_contents": "Introduction, Method",
        "author": "Research Team",
        "supervisor": "Supervisor",
    }


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    print("PASS: health")


def test_valid_request():
    r = client.post("/api/news", json=payload())
    assert r.status_code == 201, r.text
    assert r.json()["status"] == "ready"
    print(f"PASS: valid request id={r.json()['id']}")


def test_invalid_secret():
    p = payload()
    p["shared_Secret"] = "wrong"
    r = client.post("/api/news", json=p)
    assert r.status_code == 401
    print("PASS: invalid secret rejected")


def test_missing_field():
    p = payload()
    del p["abstract"]
    r = client.post("/api/news", json=p)
    assert r.status_code == 422
    print("PASS: missing field rejected")


def test_blank_field():
    p = payload()
    p["title"] = "   "
    r = client.post("/api/news", json=p)
    assert r.status_code == 422
    print("PASS: blank field rejected")


if __name__ == "__main__":
    test_health()
    test_valid_request()
    test_invalid_secret()
    test_missing_field()
    test_blank_field()
    print("\nAll server tests passed.")


"""
قدم ۴: تست چهار حالت (نمایش در جلسه)
حالت ۱: درخواست معتبر 
powershell
curl -X POST http://127.0.0.1:8000/api/news `
  -H "Content-Type: application/json" `
  -d '{
    "shared_Secret": "my-super-secret-key-change-in-production",
    "username": "intern",
    "title": "AI Research Project",
    "abstract": "A university research team has developed...",
    "field": "بیماری‌های داخلی",
    "university": "Example University",
    "table_of_contents": "Introduction, Method",
    "author": "Research Team",
    "supervisor": "Dr. Example"
  }'
انتظار: 201 + {"id": 1, "status": "ready", ...}

حالت ۲: کلید غلط → 401
powershell
curl -X POST http://127.0.0.1:8000/api/news `
  -H "Content-Type: application/json" `
  -d '{
    "shared_Secret": "wrong-key",
    ...
  }'
انتظار: 401 + {"detail": "Invalid shared secret"}

حالت ۳: فیلد خالی → 422
powershell
curl -X POST http://127.0.0.1:8000/api/news `
  -H "Content-Type: application/json" `
  -d '{
    "shared_Secret": "my-super-secret-key-change-in-production",
    "title": "   ",
    ...
  }'
انتظار: 422 + پیام field cannot be empty or whitespace

حالت ۴: رشته ناشناخته → 201 با category=other
powershell
curl -X POST http://127.0.0.1:8000/api/news `
  -H "Content-Type: application/json" `
  -d '{
    "shared_Secret": "my-super-secret-key-change-in-production",
    "field": "رشته‌ی ناموجود",
    ...
  }'
انتظار: 201 + {"id": 4, "status": "ready", ...}

سپس در psql چک کن:

sql
SELECT id, field_id, category_id, status
FROM main
ORDER BY id DESC
LIMIT 5;
باید ببینی رکورد آخر field_id = NULL و category_id برابر id دسته other است.

 چک لیست تست
□ حالت ۱ پاس شد (201)
□ حالت ۲ پاس شد (401)
□ حالت ۳ پاس شد (422)
□ حالت ۴ پاس شد (201 با other)

"""
