import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_subscription_unauthorized():
    response = client.get("/api/subscriptions/current")
    assert response.status_code == 401

def test_create_checkout_session_unauthorized():
    response = client.post("/api/subscriptions/create-checkout-session", json={
        "plan": "pro"
    })
    assert response.status_code == 401

def test_cancel_subscription_unauthorized():
    response = client.post("/api/subscriptions/cancel")
    assert response.status_code == 401