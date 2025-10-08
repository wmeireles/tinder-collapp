import pytest
from fastapi.testclient import TestClient

def test_discover_creators(client: TestClient, auth_headers):
    response = client.get("/matching/discover", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_swipe_like(client: TestClient, auth_headers, test_user_2):
    response = client.post(
        "/matching/swipe",
        json={"swiped_user_id": test_user_2["id"], "action": "like"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "match" in data

def test_swipe_dislike(client: TestClient, auth_headers, test_user_2):
    response = client.post(
        "/matching/swipe",
        json={"swiped_user_id": test_user_2["id"], "action": "dislike"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["match"] is False

def test_get_matches(client: TestClient, auth_headers):
    response = client.get("/matching/matches", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_swipe_already_swiped(client: TestClient, auth_headers, test_user_2):
    # First swipe
    client.post(
        "/matching/swipe",
        json={"swiped_user_id": test_user_2["id"], "action": "like"},
        headers=auth_headers
    )
    # Second swipe on same user
    response = client.post(
        "/matching/swipe",
        json={"swiped_user_id": test_user_2["id"], "action": "like"},
        headers=auth_headers
    )
    assert response.status_code == 400
    assert "Already swiped" in response.json()["detail"]