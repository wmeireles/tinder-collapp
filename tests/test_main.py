import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Collapp Auth API is running"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register_user():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "TestPass123"}
    )
    assert response.status_code in [200, 400]  # 400 if user already exists

def test_invalid_email_registration():
    response = client.post(
        "/auth/register",
        json={"email": "invalid-email", "password": "TestPass123"}
    )
    assert response.status_code == 422

def test_weak_password_registration():
    response = client.post(
        "/auth/register",
        json={"email": "test2@example.com", "password": "123"}
    )
    assert response.status_code == 422