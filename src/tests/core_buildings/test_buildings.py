"""Unit tests for Buildings domain model."""
from datetime import datetime
from unittest.mock import MagicMock

import pytest


def test_building_creation():
    """Test creating a Buildings instance."""
    from chalicelib.dddpy.core_buildings.domain.buildings import Buildings
    
    now = datetime.now()
    building = Buildings(
        id=1,
        name="Building A",
        code="BLD-A",
        description="Test building",
        size=500.75,
        percentage=2.5,
        type="residential",
        condominium_id=1,
        building_type_id=1,
        created_at=now,
        updated_at=now
    )
    
    assert building.id == 1
    assert building.name == "Building A"
    assert building.code == "BLD-A"
    assert building.description == "Test building"
    assert building.size == 500.75
    assert building.percentage == 2.5
    assert building.type == "residential"
    assert building.condominium_id == 1
    assert building.building_type_id == 1


def test_building_to_dict():
    """Test to_dict method returns correct dictionary."""
    from chalicelib.dddpy.core_buildings.domain.buildings import Buildings
    
    now = datetime(2025, 1, 1, 12, 0, 0)
    building = Buildings(
        id=1,
        name="Building A",
        code="BLD-A",
        description="Test building",
        size=500.75,
        percentage=2.5,
        type="residential",
        condominium_id=1,
        building_type_id=1,
        created_at=now,
        updated_at=now
    )
    
    result = building.to_dict()
    
    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["name"] == "Building A"
    assert result["code"] == "BLD-A"
    assert result["description"] == "Test building"
    assert result["size"] == 500.75
    assert result["percentage"] == 2.5
    assert result["type"] == "residential"
    assert result["condominium_id"] == 1
    assert result["building_type_id"] == 1
    assert result["created_at"] == "2025-01-01T12:00:00"
    assert result["updated_at"] == "2025-01-01T12:00:00"


def test_building_from_db():
    """Test from_db class method creates instance from DB model."""
    from chalicelib.dddpy.core_buildings.domain.buildings import Buildings
    
    now = datetime.now()
    # Create a simple object instead of using MagicMock with spec
    mock_db = MagicMock()
    mock_db.id = 1
    mock_db.name = "Building A"
    mock_db.code = "BLD-A"
    mock_db.description = "Test building"
    mock_db.size = 500.75
    mock_db.percentage = 2.5
    mock_db.type = "residential"
    mock_db.condominium_id = 1
    mock_db.building_type_id = 1
    mock_db.created_at = now
    mock_db.updated_at = now
    
    building = Buildings.from_db(mock_db)
    
    assert isinstance(building, Buildings)
    assert building.id == 1
    assert building.name == "Building A"
    assert building.code == "BLD-A"


def test_building_optional_fields():
    """Test Buildings with optional fields as None."""
    from chalicelib.dddpy.core_buildings.domain.buildings import Buildings
    
    building = Buildings(
        id=1,
        name="Minimal Building",
        code="MB001"
    )
    
    assert building.description is None
    assert building.size is None
    assert building.percentage is None
    assert building.type is None
    assert building.condominium_id is None
    assert building.building_type_id is None
    assert building.created_at is None
    assert building.updated_at is None


def test_building_size_conversion_from_db():
    """Test that size is properly converted from DB (string to float)."""
    from chalicelib.dddpy.core_buildings.domain.buildings import Buildings
    
    mock_db = MagicMock()
    mock_db.id = 1
    mock_db.name = "Building A"
    mock_db.code = "BLD-A"
    mock_db.description = None
    mock_db.size = "500.75"  # String from DECIMAL column
    mock_db.percentage = "2.5"  # String from DECIMAL column
    mock_db.type = None
    mock_db.condominium_id = None
    mock_db.building_type_id = None
    mock_db.created_at = None
    mock_db.updated_at = None
    
    building = Buildings.from_db(mock_db)
    
    assert building.size == 500.75
    assert building.percentage == 2.5


# Exceptions tests
def test_building_not_found_exception():
    """Test BuildingNotFoundException."""
    from chalicelib.dddpy.core_buildings.domain.buildings_exception import BuildingNotFoundException
    
    exc = BuildingNotFoundException()
    assert exc.message == "Building not found"
    assert exc.status_code == 404


def test_building_already_exists_exception():
    """Test BuildingAlreadyExistsException."""
    from chalicelib.dddpy.core_buildings.domain.buildings_exception import BuildingAlreadyExistsException
    
    exc = BuildingAlreadyExistsException()
    assert exc.message == "Building already exists"
    assert exc.status_code == 409


def test_building_validation_exception():
    """Test BuildingValidationException."""
    from chalicelib.dddpy.core_buildings.domain.buildings_exception import BuildingValidationException
    
    exc = BuildingValidationException()
    assert exc.message == "Building validation failed"
    assert exc.status_code == 400


# Success messages tests
def test_success_messages():
    """Test SuccessMessages class."""
    from chalicelib.dddpy.core_buildings.domain.buildings_success import SuccessMessages
    
    assert SuccessMessages.BUILDING_CREATED == "Building created successfully"
    assert SuccessMessages.BUILDING_UPDATED == "Building updated successfully"
    assert SuccessMessages.BUILDING_DELETED == "Building deleted successfully"
    assert SuccessMessages.BUILDING_RETRIEVED == "Building retrieved successfully"
    assert SuccessMessages.BUILDINGS_LISTED == "Buildings listed successfully"
