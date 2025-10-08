import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_profile_unauthorized():
    response = client.get("/api/profile/me")
    assert response.status_code == 401

def test_update_profile_unauthorized():
    response = client.put("/api/profile/me", json={"bio": "test"})
    assert response.status_code == 401

def test_get_public_profile_not_found():
    response = client.get("/api/profile/public/nonexistent")
    assert response.status_code == 404