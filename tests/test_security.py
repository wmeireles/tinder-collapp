import pytest
from app.core.security import create_access_token, verify_password, get_password_hash

def test_password_hashing():
    """Test password hashing and verification"""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    # Hash should be different from original
    assert hashed != password
    
    # Verification should work
    assert verify_password(password, hashed) == True
    
    # Wrong password should fail
    assert verify_password("wrongpassword", hashed) == False

def test_access_token_creation():
    """Test JWT token creation"""
    user_id = "test-user-id"
    token = create_access_token(data={"sub": user_id})
    
    # Token should be a string
    assert isinstance(token, str)
    
    # Token should not be empty
    assert len(token) > 0
    
    # Token should contain dots (JWT format)
    assert "." in token