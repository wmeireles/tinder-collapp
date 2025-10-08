import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_app_startup():
    """Test that the FastAPI app starts correctly"""
    response = client.get("/health")
    assert response.status_code == 200
    # App should be running
    assert response.json()["status"] == "healthy"

def test_404_endpoint():
    """Test 404 for non-existent endpoint"""
    response = client.get("/nonexistent")
    assert response.status_code == 404

def test_auth_register_endpoint_exists():
    """Test auth register endpoint exists"""
    response = client.post("/auth/register", json={})
    # Should not be 404 (endpoint exists)
    assert response.status_code != 404

def test_auth_login_endpoint_exists():
    """Test auth login endpoint exists"""
    response = client.post("/auth/login", json={})
    # Should not be 404 (endpoint exists)
    assert response.status_code != 404