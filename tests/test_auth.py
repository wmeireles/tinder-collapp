import pytest
from fastapi.testclient import TestClient
from app.core.security import verify_password, get_password_hash, create_access_token, verify_token

def test_register_user(client: TestClient):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_register_duplicate_email(client: TestClient):
    # First registration
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    # Second registration with same email
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_register_invalid_password(client: TestClient):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "123"}
    )
    assert response.status_code == 422

def test_login_success(client: TestClient):
    # Register user first
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    # Login
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client: TestClient):
    # Register user first
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    # Login with wrong password
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_login_nonexistent_user(client: TestClient):
    response = client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "testpassword123"}
    )
    assert response.status_code == 401

def test_protected_route_with_token(client: TestClient):
    # Register and login
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    login_response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    token = login_response.json()["access_token"]
    
    # Access protected route
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"

def test_protected_route_without_token(client: TestClient):
    response = client.get("/auth/me")
    assert response.status_code == 403

def test_password_hashing():
    password = "testpassword123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_jwt_token_creation_and_verification():
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    assert token is not None
    
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "test@example.com"

def test_integration_create_and_authenticate_user(client: TestClient):
    # Complete flow: register -> login -> access protected route
    email = "integration@example.com"
    password = "integrationtest123"
    
    # Register
    register_response = client.post(
        "/auth/register",
        json={"email": email, "password": password}
    )
    assert register_response.status_code == 200
    
    # Login
    login_response = client.post(
        "/auth/login",
        json={"email": email, "password": password}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Access protected route
    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == email