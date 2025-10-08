import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_mediakit_unauthorized():
    response = client.get("/api/mediakit/")
    assert response.status_code == 401

def test_save_mediakit_unauthorized():
    response = client.post("/api/mediakit/save", json={"bio": "test"})
    assert response.status_code == 401

def test_generate_mediakit_unauthorized():
    response = client.post("/api/mediakit/generate")
    assert response.status_code == 401