import pytest
from app.core.config import settings

def test_settings_loaded():
    """Test that settings are loaded correctly"""
    assert settings is not None
    assert hasattr(settings, 'SECRET_KEY')
    assert hasattr(settings, 'ACCESS_TOKEN_EXPIRE_MINUTES')

def test_secret_key_exists():
    """Test that secret key is configured"""
    assert settings.SECRET_KEY is not None
    assert len(settings.SECRET_KEY) > 0

def test_token_expiry_configured():
    """Test that token expiry is configured"""
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0
    assert isinstance(settings.ACCESS_TOKEN_EXPIRE_MINUTES, int)