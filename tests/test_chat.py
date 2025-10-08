import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_chats_unauthorized():
    response = client.get("/api/chat/chats")
    assert response.status_code == 401

def test_get_chat_messages_unauthorized():
    response = client.get("/api/chat/chat/123/messages")
    assert response.status_code == 401

def test_send_message_unauthorized():
    response = client.post("/api/chat/chat/123/messages", json={"content": "test"})
    assert response.status_code == 401