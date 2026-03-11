"""Unit tests for BuildingsTypes domain model."""
from datetime import datetime
from unittest.mock import MagicMock

import pytest


def test_building_type_creation():
    """Test creating a BuildingsTypes instance."""
    from chalicelib.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
    
    now = datetime.now()
    building_type = BuildingsTypes(
        id=1,
        name="Residential",
        code="RES",
        description="Residential building type",
        created_at=now,
        updated_at=now
    )
    
    assert building_type.id == 1
    assert building_type.name == "Residential"
    assert building_type.code == "RES"
    assert building_type.description == "Residential building type"


def test_building_type_to_dict():
    """Test to_dict method returns correct dictionary."""
    from chalicelib.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
    
    now = datetime(2025, 1, 1, 12, 0, 0)
    building_type = BuildingsTypes(
        id=1,
        name="Residential",
        code="RES",
        description="Residential building type",
        created_at=now,
        updated_at=now
    )
    
    result = building_type.to_dict()
    
    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["name"] == "Residential"
    assert result["code"] == "RES"
    assert result["description"] == "Residential building type"
    assert result["created_at"] == "2025-01-01T12:00:00"
    assert result["updated_at"] == "2025-01-01T12:00:00"


def test_building_type_from_db():
    """Test from_db class method creates instance from DB model."""
    from chalicelib.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
    
    now = datetime.now()
    mock_db = MagicMock()
    mock_db.id = 1
    mock_db.name = "Residential"
    mock_db.code = "RES"
    mock_db.description = "Residential building type"
    mock_db.created_at = now
    mock_db.updated_at = now
    
    building_type = BuildingsTypes.from_db(mock_db)
    
    assert isinstance(building_type, BuildingsTypes)
    assert building_type.id == 1
    assert building_type.name == "Residential"
    assert building_type.code == "RES"


def test_building_type_optional_fields():
    """Test BuildingsTypes with optional fields as None."""
    from chalicelib.dddpy.core_buildings_types.domain.buildings_types import BuildingsTypes
    
    building_type = BuildingsTypes(
        id=1,
        name="Commercial",
        code="COM"
    )
    
    assert building_type.description is None
    assert building_type.created_at is None
    assert building_type.updated_at is None


# Exceptions tests
def test_building_type_not_found_exception():
    """Test BuildingTypeNotFoundException."""
    from chalicelib.dddpy.core_buildings_types.domain.buildings_types_exception import BuildingTypeNotFoundException
    
    exc = BuildingTypeNotFoundException()
    assert exc.message == "Building type not found"
    assert exc.status_code == 404


def test_building_type_already_exists_exception():
    """Test BuildingTypeAlreadyExistsException."""
    from chalicelib.dddpy.core_buildings_types.domain.buildings_types_exception import BuildingTypeAlreadyExistsException
    
    exc = BuildingTypeAlreadyExistsException()
    assert exc.message == "Building type already exists"
    assert exc.status_code == 409


# Success messages tests
def test_success_messages():
    """Test SuccessMessages class."""
    from chalicelib.dddpy.core_buildings_types.domain.buildings_types_success import SuccessMessages
    
    assert SuccessMessages.BUILDING_TYPE_CREATED == "Building type created successfully"
    assert SuccessMessages.BUILDING_TYPE_UPDATED == "Building type updated successfully"
    assert SuccessMessages.BUILDING_TYPE_DELETED == "Building type deleted successfully"
    assert SuccessMessages.BUILDING_TYPE_RETRIEVED == "Building type retrieved successfully"
    assert SuccessMessages.BUILDING_TYPES_LISTED == "Building types listed successfully"
