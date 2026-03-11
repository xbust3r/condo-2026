"""Unit tests for UnitysTypes domain model."""
from datetime import datetime
from unittest.mock import MagicMock

import pytest


def test_unitys_types_creation():
    """Test creating a UnitysTypes instance."""
    from chalicelib.dddpy.core_unittys_types.domain.unittys_types import UnitysTypes
    
    now = datetime.now()
    unity_type = UnitysTypes(
        id=1,
        name="Apartamento",
        code="APT",
        description="Unidad habitacional tipo apartamento",
        created_at=now,
        updated_at=now
    )
    
    assert unity_type.id == 1
    assert unity_type.name == "Apartamento"
    assert unity_type.code == "APT"
    assert unity_type.description == "Unidad habitacional tipo apartamento"


def test_unitys_types_to_dict():
    """Test to_dict method returns correct dictionary."""
    from chalicelib.dddpy.core_unittys_types.domain.unittys_types import UnitysTypes
    
    now = datetime(2025, 1, 1, 12, 0, 0)
    unity_type = UnitysTypes(
        id=1,
        name="Penthouse",
        code="PH",
        description="Unidad de lujo en la azotea",
        created_at=now,
        updated_at=now
    )
    
    result = unity_type.to_dict()
    
    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["name"] == "Penthouse"
    assert result["code"] == "PH"
    assert result["description"] == "Unidad de lujo en la azotea"
    assert result["created_at"] == "2025-01-01T12:00:00"
    assert result["updated_at"] == "2025-01-01T12:00:00"


def test_unitys_types_from_db():
    """Test from_db class method creates instance from DB model."""
    from chalicelib.dddpy.core_unittys_types.domain.unittys_types import UnitysTypes
    
    now = datetime.now()
    mock_db = MagicMock()
    mock_db.id = 1
    mock_db.name = "Local Commercial"
    mock_db.code = "LC"
    mock_db.description = "Espacio comercial"
    mock_db.created_at = now
    mock_db.updated_at = now
    
    unity_type = UnitysTypes.from_db(mock_db)
    
    assert isinstance(unity_type, UnitysTypes)
    assert unity_type.id == 1
    assert unity_type.name == "Local Commercial"
    assert unity_type.code == "LC"


def test_unitys_types_optional_fields():
    """Test UnitysTypes with optional fields as None."""
    from chalicelib.dddpy.core_unittys_types.domain.unittys_types import UnitysTypes
    
    unity_type = UnitysTypes(
        id=1,
        name="Estacionamiento",
        code="EST"
    )
    
    assert unity_type.description is None
    assert unity_type.created_at is None
    assert unity_type.updated_at is None


# Exceptions tests - using correct exception names
def test_unitys_types_not_found_exception():
    """Test UnityTypeNotFoundException."""
    from chalicelib.dddpy.core_unittys_types.domain.unittys_types_exception import UnityTypeNotFoundException
    
    exc = UnityTypeNotFoundException()
    assert exc.message == "Unity type not found"
    assert exc.status_code == 404


def test_unitys_types_already_exists_exception():
    """Test UnityTypeAlreadyExistsException."""
    from chalicelib.dddpy.core_unittys_types.domain.unittys_types_exception import UnityTypeAlreadyExistsException
    
    exc = UnityTypeAlreadyExistsException()
    assert exc.message == "Unity type already exists"
    assert exc.status_code == 409


def test_unitys_types_validation_exception():
    """Test UnityTypeValidationException."""
    from chalicelib.dddpy.core_unittys_types.domain.unittys_types_exception import UnityTypeValidationException
    
    exc = UnityTypeValidationException()
    assert exc.message == "Unity type validation failed"
    assert exc.status_code == 400


# Success messages tests
def test_success_messages():
    """Test SuccessMessages class."""
    from chalicelib.dddpy.core_unittys_types.domain.unittys_types_success import SuccessMessages
    
    assert SuccessMessages.UNITY_TYPE_CREATED == "Unity type created successfully"
    assert SuccessMessages.UNITY_TYPE_UPDATED == "Unity type updated successfully"
    assert SuccessMessages.UNITY_TYPE_DELETED == "Unity type deleted successfully"
    assert SuccessMessages.UNITY_TYPE_RETRIEVED == "Unity type retrieved successfully"
    assert SuccessMessages.UNITY_TYPES_LISTED == "Unity types listed successfully"
