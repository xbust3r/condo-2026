"""Unit tests for Users domain model."""
from datetime import datetime
from unittest.mock import MagicMock

import pytest


def test_users_creation():
    """Test creating a Users instance."""
    from chalicelib.dddpy.users.domain.users import Users
    
    now = datetime.now()
    user = Users(
        id=1,
        first_name="Juan",
        last_name="Perez",
        email="juan.perez@example.com",
        password="hashed_password",
        doc_identity="12345678",
        phone="+1234567890",
        status="activo",
        created_at=now,
        updated_at=now
    )
    
    assert user.id == 1
    assert user.first_name == "Juan"
    assert user.last_name == "Perez"
    assert user.email == "juan.perez@example.com"
    assert user.password == "hashed_password"
    assert user.doc_identity == "12345678"
    assert user.phone == "+1234567890"
    assert user.status == "activo"


def test_users_to_dict():
    """Test to_dict method returns correct dictionary."""
    from chalicelib.dddpy.users.domain.users import Users
    
    now = datetime(2025, 1, 1, 12, 0, 0)
    user = Users(
        id=1,
        first_name="Maria",
        last_name="Garcia",
        email="maria.garcia@example.com",
        password="hashed_password",
        doc_identity="87654321",
        phone="+1987654321",
        status="activo",
        created_at=now,
        updated_at=now
    )
    
    result = user.to_dict()
    
    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["first_name"] == "Maria"
    assert result["last_name"] == "Garcia"
    assert result["email"] == "maria.garcia@example.com"
    assert result["doc_identity"] == "87654321"
    assert result["phone"] == "+1987654321"
    assert result["status"] == "activo"
    assert result["created_at"] == "2025-01-01T12:00:00"
    assert result["updated_at"] == "2025-01-01T12:00:00"


def test_users_to_dict_excludes_password():
    """Test to_dict method excludes password for security."""
    from chalicelib.dddpy.users.domain.users import Users
    
    user = Users(
        id=1,
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password="secret_password"
    )
    
    result = user.to_dict()
    
    assert "password" not in result
    assert "password" not in result.keys()


def test_users_from_db():
    """Test from_db class method creates instance from DB model."""
    from chalicelib.dddpy.users.domain.users import Users
    
    now = datetime.now()
    mock_db = MagicMock()
    mock_db.id = 1
    mock_db.first_name = "Carlos"
    mock_db.last_name = "Lopez"
    mock_db.email = "carlos.lopez@example.com"
    mock_db.password = "hashed_pwd"
    mock_db.doc_identity = "11223344"
    mock_db.phone = "+5511223344"
    mock_db.status = "inactivo"
    mock_db.created_at = now
    mock_db.updated_at = now
    
    user = Users.from_db(mock_db)
    
    assert isinstance(user, Users)
    assert user.id == 1
    assert user.first_name == "Carlos"
    assert user.last_name == "Lopez"
    assert user.email == "carlos.lopez@example.com"


def test_users_optional_fields():
    """Test Users with optional fields as None."""
    from chalicelib.dddpy.users.domain.users import Users
    
    user = Users(
        id=1,
        first_name="Minimal",
        last_name="User",
        email="minimal@example.com"
    )
    
    assert user.password is None
    assert user.doc_identity is None
    assert user.phone is None
    assert user.status is None
    assert user.created_at is None
    assert user.updated_at is None


# Exceptions tests - using correct exception names (User* not Users*)
def test_users_not_found_exception():
    """Test UserNotFoundException."""
    from chalicelib.dddpy.users.domain.users_exception import UserNotFoundException
    
    exc = UserNotFoundException()
    assert exc.message == "User not found"
    assert exc.status_code == 404


def test_users_already_exists_exception():
    """Test UserAlreadyExistsException."""
    from chalicelib.dddpy.users.domain.users_exception import UserAlreadyExistsException
    
    exc = UserAlreadyExistsException()
    assert exc.message == "User already exists"
    assert exc.status_code == 409


def test_users_validation_exception():
    """Test UserValidationException."""
    from chalicelib.dddpy.users.domain.users_exception import UserValidationException
    
    exc = UserValidationException()
    assert exc.message == "User validation failed"
    assert exc.status_code == 400


# Success messages tests
def test_success_messages():
    """Test SuccessMessages class."""
    from chalicelib.dddpy.users.domain.users_success import SuccessMessages
    
    assert SuccessMessages.USER_CREATED == "User created successfully"
    assert SuccessMessages.USER_UPDATED == "User updated successfully"
    assert SuccessMessages.USER_DELETED == "User deleted successfully"
    assert SuccessMessages.USER_RETRIEVED == "User retrieved successfully"
    assert SuccessMessages.USERS_LISTED == "Users listed successfully"
