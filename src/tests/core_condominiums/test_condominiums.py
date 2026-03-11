"""Unit tests for Condominiums domain model."""
from datetime import datetime
from unittest.mock import MagicMock

import pytest


def test_condominium_creation():
    """Test creating a Condominium instance."""
    from chalicelib.dddpy.core_condominiums.domain.condominiums import Condominiums
    
    now = datetime.now()
    condo = Condominiums(
        id=1,
        name="Test Condo",
        code="TC001",
        description="A test condominium",
        size=1000.50,
        percentage=5.5,
        created_at=now,
        updated_at=now
    )
    
    assert condo.id == 1
    assert condo.name == "Test Condo"
    assert condo.code == "TC001"
    assert condo.description == "A test condominium"
    assert condo.size == 1000.50
    assert condo.percentage == 5.5


def test_condominium_to_dict():
    """Test to_dict method returns correct dictionary."""
    from chalicelib.dddpy.core_condominiums.domain.condominiums import Condominiums
    
    now = datetime(2025, 1, 1, 12, 0, 0)
    condo = Condominiums(
        id=1,
        name="Test Condo",
        code="TC001",
        description="A test condominium",
        size=1000.50,
        percentage=5.5,
        created_at=now,
        updated_at=now
    )
    
    result = condo.to_dict()
    
    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["name"] == "Test Condo"
    assert result["code"] == "TC001"
    assert result["description"] == "A test condominium"
    assert result["size"] == 1000.50
    assert result["percentage"] == 5.5
    assert result["created_at"] == "2025-01-01T12:00:00"
    assert result["updated_at"] == "2025-01-01T12:00:00"


def test_condominium_from_db():
    """Test from_db class method creates instance from DB model."""
    from chalicelib.dddpy.core_condominiums.domain.condominiums import Condominiums
    
    now = datetime.now()
    mock_db = MagicMock()
    mock_db.id = 1
    mock_db.name = "Test Condo"
    mock_db.code = "TC001"
    mock_db.description = "A test condominium"
    mock_db.size = 1000.50
    mock_db.percentage = 5.5
    mock_db.created_at = now
    mock_db.updated_at = now
    
    condo = Condominiums.from_db(mock_db)
    
    assert isinstance(condo, Condominiums)
    assert condo.id == 1
    assert condo.name == "Test Condo"
    assert condo.code == "TC001"


def test_condominium_optional_fields():
    """Test Condominium with optional fields as None."""
    from chalicelib.dddpy.core_condominiums.domain.condominiums import Condominiums
    
    condo = Condominiums(
        id=1,
        name="Minimal Condo",
        code="MC001"
    )
    
    assert condo.description is None
    assert condo.size is None
    assert condo.percentage is None
    assert condo.created_at is None
    assert condo.updated_at is None


# Exceptions tests
def test_condominium_not_found_exception():
    """Test CondominiumNotFoundException."""
    from chalicelib.dddpy.core_condominiums.domain.condominiums_exception import CondominiumNotFoundException
    
    exc = CondominiumNotFoundException()
    assert exc.message == "Condominium not found"
    assert exc.status_code == 404


def test_condominium_already_exists_exception():
    """Test CondominiumAlreadyExistsException."""
    from chalicelib.dddpy.core_condominiums.domain.condominiums_exception import CondominiumAlreadyExistsException
    
    exc = CondominiumAlreadyExistsException()
    assert exc.message == "Condominium already exists"
    assert exc.status_code == 409


def test_condominium_validation_exception():
    """Test CondominiumValidationException."""
    from chalicelib.dddpy.core_condominiums.domain.condominiums_exception import CondominiumValidationException
    
    exc = CondominiumValidationException()
    assert exc.message == "Condominium validation failed"
    assert exc.status_code == 400


# Success messages tests
def test_success_messages():
    """Test SuccessMessages class."""
    from chalicelib.dddpy.core_condominiums.domain.condominiums_success import SuccessMessages
    
    assert SuccessMessages.CONDOMINIUM_CREATED == "Condominium created successfully"
    assert SuccessMessages.CONDOMINIUM_UPDATED == "Condominium updated successfully"
    assert SuccessMessages.CONDOMINIUM_DELETED == "Condominium deleted successfully"
    assert SuccessMessages.CONDOMINIUM_RETRIEVED == "Condominium retrieved successfully"
    assert SuccessMessages.CONDOMINIUMS_LISTED == "Condominiums listed successfully"
