"""Unit tests for UsersResidents domain model."""
from datetime import datetime
from unittest.mock import MagicMock

import pytest


def test_users_residents_creation():
    """Test creating a UsersResidents instance."""
    from chalicelib.dddpy.users_residents.domain.residents import UsersResidents
    
    now = datetime.now()
    resident = UsersResidents(
        id=1,
        condominium_id=1,
        building_id=1,
        unity_id=1,
        type="Propietario",
        status="vigente",
        user_id=1,
        created_at=now,
        updated_at=now
    )
    
    assert resident.id == 1
    assert resident.condominium_id == 1
    assert resident.building_id == 1
    assert resident.unity_id == 1
    assert resident.type == "Propietario"
    assert resident.status == "vigente"
    assert resident.user_id == 1


def test_users_residents_to_dict():
    """Test to_dict method returns correct dictionary."""
    from chalicelib.dddpy.users_residents.domain.residents import UsersResidents
    
    now = datetime(2025, 1, 1, 12, 0, 0)
    resident = UsersResidents(
        id=1,
        condominium_id=2,
        building_id=3,
        unity_id=4,
        type="Inquilino",
        status="vigente",
        user_id=5,
        created_at=now,
        updated_at=now
    )
    
    result = resident.to_dict()
    
    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["condominium_id"] == 2
    assert result["building_id"] == 3
    assert result["unity_id"] == 4
    assert result["type"] == "Inquilino"
    assert result["status"] == "vigente"
    assert result["user_id"] == 5
    assert result["created_at"] == "2025-01-01T12:00:00"
    assert result["updated_at"] == "2025-01-01T12:00:00"


def test_users_residents_from_db():
    """Test from_db class method creates instance from DB model."""
    from chalicelib.dddpy.users_residents.domain.residents import UsersResidents
    
    now = datetime.now()
    mock_db = MagicMock()
    mock_db.id = 1
    mock_db.condominium_id = 1
    mock_db.building_id = 2
    mock_db.unity_id = 3
    mock_db.type = "Propietario"
    mock_db.status = "historico"
    mock_db.user_id = 4
    mock_db.created_at = now
    mock_db.updated_at = now
    
    resident = UsersResidents.from_db(mock_db)
    
    assert isinstance(resident, UsersResidents)
    assert resident.id == 1
    assert resident.condominium_id == 1
    assert resident.building_id == 2
    assert resident.unity_id == 3
    assert resident.type == "Propietario"
    assert resident.status == "historico"
    assert resident.user_id == 4


def test_users_residents_optional_fields():
    """Test UsersResidents with optional fields as None."""
    from chalicelib.dddpy.users_residents.domain.residents import UsersResidents
    
    resident = UsersResidents(
        id=1
    )
    
    assert resident.condominium_id is None
    assert resident.building_id is None
    assert resident.unity_id is None
    assert resident.type is None
    assert resident.status is None
    assert resident.user_id is None
    assert resident.created_at is None
    assert resident.updated_at is None


@pytest.mark.parametrize("resident_type", [
    "Propietario",
    "Inquilino",
    "Familiar",
    "Administrador"
])
def test_users_residents_resident_types(resident_type):
    """Test UsersResidents with different resident types."""
    from chalicelib.dddpy.users_residents.domain.residents import UsersResidents
    
    resident = UsersResidents(
        id=1,
        type=resident_type,
        user_id=1
    )
    assert resident.type == resident_type


# Exceptions tests - using correct exception names (Resident* not Residents*)
def test_residents_not_found_exception():
    """Test ResidentNotFoundException."""
    from chalicelib.dddpy.users_residents.domain.residents_exception import ResidentNotFoundException
    
    exc = ResidentNotFoundException()
    assert exc.message == "Resident not found"
    assert exc.status_code == 404


def test_residents_already_exists_exception():
    """Test ResidentAlreadyExistsException."""
    from chalicelib.dddpy.users_residents.domain.residents_exception import ResidentAlreadyExistsException
    
    exc = ResidentAlreadyExistsException()
    assert exc.message == "Resident already exists"
    assert exc.status_code == 409


def test_residents_validation_exception():
    """Test ResidentValidationException."""
    from chalicelib.dddpy.users_residents.domain.residents_exception import ResidentValidationException
    
    exc = ResidentValidationException()
    assert exc.message == "Resident validation failed"
    assert exc.status_code == 400


# Success messages tests
def test_success_messages():
    """Test SuccessMessages class."""
    from chalicelib.dddpy.users_residents.domain.residents_success import SuccessMessages
    
    assert SuccessMessages.RESIDENT_CREATED == "Resident created successfully"
    assert SuccessMessages.RESIDENT_UPDATED == "Resident updated successfully"
    assert SuccessMessages.RESIDENT_DELETED == "Resident deleted successfully"
    assert SuccessMessages.RESIDENT_RETRIEVED == "Resident retrieved successfully"
    assert SuccessMessages.RESIDENTS_LISTED == "Residents listed successfully"
