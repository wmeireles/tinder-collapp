import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_linkinbio_unauthorized():
    response = client.get("/api/linkinbio/")
    assert response.status_code == 401

def test_save_linkinbio_unauthorized():
    response = client.post("/api/linkinbio/save", json={"title": "test"})
    assert response.status_code == 401

def test_get_public_linkinbio_not_found():
    response = client.get("/api/linkinbio/public/nonexistent")
    assert response.status_code == 404