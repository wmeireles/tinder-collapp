import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_wanted_posts():
    response = client.get("/api/wanted/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_wanted_post_unauthorized():
    response = client.post("/api/wanted/posts", json={
        "title": "Test Post",
        "description": "Test Description",
        "collaboration_type": "video"
    })
    assert response.status_code == 401

def test_get_wanted_post_not_found():
    response = client.get("/api/wanted/posts/999")
    assert response.status_code == 404