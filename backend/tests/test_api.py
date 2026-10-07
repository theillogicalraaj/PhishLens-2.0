import os
os.environ["DATABASE_URL"] = "sqlite:///./test_phishlens.db"
os.environ["JWT_SECRET"] = "test-secret"
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_register_login_and_me():
    email = "analyst-test@example.com"
    r = client.post("/api/v1/auth/register", json={"email":email,"full_name":"Test Analyst","password":"StrongPass123!"})
    assert r.status_code in (200,409)
    token = r.json()["access_token"] if r.status_code == 200 else client.post("/api/v1/auth/login", json={"email":email,"password":"StrongPass123!"}).json()["access_token"]
    me = client.get("/api/v1/auth/me", headers={"Authorization":f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == email
