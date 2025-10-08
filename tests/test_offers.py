import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_offers():
    response = client.get("/api/offers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_offer_unauthorized():
    response = client.post("/api/offers/", json={
        "title": "Test Offer",
        "description": "Test Description",
        "price": 100.0
    })
    assert response.status_code == 401

def test_get_offer_not_found():
    response = client.get("/api/offers/999")
    assert response.status_code == 404