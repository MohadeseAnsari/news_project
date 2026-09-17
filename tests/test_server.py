import os
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)
VALID_SECRET = os.getenv("SHARED_SECRET", "my-super-secret-key-change-in-production")


def payload():
    return {
        "shared_Secret": VALID_SECRET,
        "username": "intern",
        "title": "AI Research Project",
        "abstract": "A university research team has developed a new AI method.",
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
    print("\n✅ All server tests passed.")
