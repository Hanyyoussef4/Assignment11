# tests/auth/test_dependencies.py

import pytest
from unittest.mock import MagicMock, patch, ANY
from fastapi import HTTPException, status
from app.auth.dependencies import get_current_user, get_current_active_user
from app.schemas.user import UserResponse
from app.models.user import User
from uuid import uuid4
from datetime import datetime

# Sample user data for testing
sample_user = User(
    id=uuid4(),
    username="testuser",
    email="test@example.com",
    first_name="Test",
    last_name="User",
    is_active=True,
    is_verified=True,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)

inactive_user = User(
    id=uuid4(),
    username="inactiveuser",
    email="inactive@example.com",
    first_name="Inactive",
    last_name="User",
    is_active=False,
    is_verified=False,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)

# Fixture for mocking the database session
@pytest.fixture
def mock_db():
    return MagicMock()

# Fixture for mocking token verification
@pytest.fixture
def mock_verify_token():
    with patch.object(User, 'verify_token') as mock:
        yield mock

# Test get_current_user with valid token and existing user
def test_get_current_user_valid_token_existing_user(mock_db, mock_verify_token):
    mock_verify_token.return_value = sample_user.id
    mock_db.query.return_value.filter.return_value.first.return_value = sample_user

    user_response = get_current_user(db=mock_db, token="validtoken")

    assert isinstance(user_response, UserResponse)
    assert user_response.id == sample_user.id
    assert user_response.username == sample_user.username
    assert user_response.email == sample_user.email
    assert user_response.first_name == sample_user.first_name
    assert user_response.last_name == sample_user.last_name
    assert user_response.is_active == sample_user.is_active
    assert user_response.is_verified == sample_user.is_verified
    assert user_response.created_at == sample_user.created_at
    assert user_response.updated_at == sample_user.updated_at

    mock_verify_token.assert_called_once_with("validtoken")
    mock_db.query.assert_called_once_with(User)
    # Use ANY to ignore the specific BinaryExpression instance
    mock_db.query.return_value.filter.assert_called_once_with(ANY)
    mock_db.query.return_value.filter.return_value.first.assert_called_once()

# Test get_current_user with invalid token
def test_get_current_user_invalid_token(mock_db, mock_verify_token):
    mock_verify_token.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(db=mock_db, token="invalidtoken")

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"

    mock_verify_token.assert_called_once_with("invalidtoken")
    mock_db.query.assert_not_called()

# Test get_current_user with valid token but non-existent user
def test_get_current_user_valid_token_nonexistent_user(mock_db, mock_verify_token):
    mock_verify_token.return_value = sample_user.id
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(db=mock_db, token="validtoken")

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"

    mock_verify_token.assert_called_once_with("validtoken")
    mock_db.query.assert_called_once_with(User)
    mock_db.query.return_value.filter.assert_called_once_with(ANY)
    mock_db.query.return_value.filter.return_value.first.assert_called_once()

# Test get_current_active_user with active user
def test_get_current_active_user_active(mock_db, mock_verify_token):
    mock_verify_token.return_value = sample_user.id
    mock_db.query.return_value.filter.return_value.first.return_value = sample_user

    current_user = get_current_user(db=mock_db, token="validtoken")
    active_user = get_current_active_user(current_user=current_user)

    assert isinstance(active_user, UserResponse)
    assert active_user.is_active is True

# Test get_current_active_user with inactive user
def test_get_current_active_user_inactive(mock_db, mock_verify_token):
    mock_verify_token.return_value = inactive_user.id
    mock_db.query.return_value.filter.return_value.first.return_value = inactive_user

    current_user = get_current_user(db=mock_db, token="validtoken")

    with pytest.raises(HTTPException) as exc_info:
        get_current_active_user(current_user=current_user)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "Inactive user"
