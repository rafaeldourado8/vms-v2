"""Tests for JWT Authentication"""
import pytest
from uuid import UUID
from src.shared_kernel.infrastructure.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_hash_password():
    """Test password hashing"""
    password = "test123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert len(hashed) > 0


def test_verify_password():
    """Test password verification"""
    password = "test123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True
    assert verify_password("wrong", hashed) is False


def test_create_access_token():
    """Test access token creation"""
    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    email = "test@example.com"
    role = "admin"
    
    token = create_access_token(user_id, email, role)
    
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_refresh_token():
    """Test refresh token creation"""
    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    
    token = create_refresh_token(user_id)
    
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_token():
    """Test token decoding"""
    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    email = "test@example.com"
    role = "admin"
    
    token = create_access_token(user_id, email, role)
    token_data = decode_token(token)
    
    assert token_data is not None
    assert token_data.user_id == user_id
    assert token_data.email == email
    assert token_data.role == role


def test_decode_invalid_token():
    """Test decoding invalid token"""
    token_data = decode_token("invalid_token")
    
    assert token_data is None
