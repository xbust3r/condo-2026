"""Unit tests for Unitys domain model - pytest version."""
import sys
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

# Ensure src in path
sys.path.insert(0, '/home/miguel/servers/condo-py/src')


class TestUnitys:
    """Test cases for Unitys domain class."""

    def test_unitys_creation(self):
        """Test creating a Unitys instance."""
        from chalicelib.dddpy.core_unitys.domain.unitys import Unitys

        now = datetime.now()
        unity = Unitys(
            id=1,
            name="Apartamento 101",
            code="APT101",
            description="Apartamento de 2 habitaciones",
            size=85.50,
            percentage=2.5,
            type="residencial",
            floor=1,
            unit="101",
            building_id=1,
            unity_type_id=1,
            created_at=now,
            updated_at=now
        )

        assert unity.id == 1
        assert unity.name == "Apartamento 101"
        assert unity.code == "APT101"
        assert unity.description == "Apartamento de 2 habitaciones"
        assert unity.size == 85.50
        assert unity.percentage == 2.5
        assert unity.type == "residencial"
        assert unity.floor == 1
        assert unity.unit == "101"
        assert unity.building_id == 1
        assert unity.unity_type_id == 1

    def test_unitys_to_dict(self):
        """Test to_dict method returns correct dictionary."""
        from chalicelib.dddpy.core_unitys.domain.unitys import Unitys

        now = datetime(2025, 1, 1, 12, 0, 0)
        unity = Unitys(
            id=1,
            name="Penthouse 501",
            code="PH501",
            description="Penthouse de lujo",
            size=150.75,
            percentage=5.0,
            type="residencial",
            floor=5,
            unit="501",
            building_id=2,
            unity_type_id=3,
            created_at=now,
            updated_at=now
        )

        result = unity.to_dict()

        assert isinstance(result, dict)
        assert result["id"] == 1
        assert result["name"] == "Penthouse 501"
        assert result["code"] == "PH501"
        assert result["description"] == "Penthouse de lujo"
        assert result["size"] == 150.75
        assert result["percentage"] == 5.0
        assert result["type"] == "residencial"
        assert result["floor"] == 5
        assert result["unit"] == "501"
        assert result["building_id"] == 2
        assert result["unity_type_id"] == 3
        assert result["created_at"] == "2025-01-01T12:00:00"
        assert result["updated_at"] == "2025-01-01T12:00:00"

    def test_unitys_from_db(self):
        """Test from_db class method creates instance from DB model."""
        from chalicelib.dddpy.core_unitys.domain.unitys import Unitys

        now = datetime.now()
        
        # Create a mock DB object with required attributes
        mock_db = MagicMock()
        mock_db.id = 1
        mock_db.name = "Local 101"
        mock_db.code = "LC101"
        mock_db.description = "Local comercial"
        mock_db.size = 45.00
        mock_db.percentage = 1.5
        mock_db.type = "comercial"
        mock_db.floor = 1
        mock_db.unit = "101"
        mock_db.building_id = 1
        mock_db.unity_type_id = 2
        mock_db.created_at = now
        mock_db.updated_at = now

        unity = Unitys.from_db(mock_db)

        assert isinstance(unity, Unitys)
        assert unity.id == 1
        assert unity.name == "Local 101"
        assert unity.code == "LC101"
        assert unity.size == 45.00

    def test_unitys_optional_fields(self):
        """Test Unitys with optional fields as None."""
        from chalicelib.dddpy.core_unitys.domain.unitys import Unitys

        unity = Unitys(
            id=1,
            name="Minimal Unity",
            code="MIN001"
        )

        assert unity.description is None
        assert unity.size is None
        assert unity.percentage is None
        assert unity.type is None
        assert unity.floor is None
        assert unity.unit is None
        assert unity.building_id is None
        assert unity.unity_type_id is None
        assert unity.created_at is None
        assert unity.updated_at is None

    @pytest.mark.parametrize("size_input,expected", [
        (50.0, 50.0),
        (100, 100.0),
    ])
    def test_unitys_size_numeric_types(self, size_input, expected):
        """Test Unitys size field handles numeric types."""
        from chalicelib.dddpy.core_unitys.domain.unitys import Unitys

        unity = Unitys(
            id=1,
            name="Test Unity",
            code="TEST001",
            size=size_input
        )

        assert unity.size == expected


class TestUnitysExceptions:
    """Test cases for Unitys exceptions."""

    def test_unity_not_found_exception(self):
        """Test UnityNotFoundException."""
        from chalicelib.dddpy.core_unitys.domain.unitys_exception import UnityNotFoundException

        exc = UnityNotFoundException()
        assert exc.message == "Unity not found"
        assert exc.status_code == 404

    def test_unity_already_exists_exception(self):
        """Test UnityAlreadyExistsException."""
        from chalicelib.dddpy.core_unitys.domain.unitys_exception import UnityAlreadyExistsException

        exc = UnityAlreadyExistsException()
        assert exc.message == "Unity already exists"
        assert exc.status_code == 409

    def test_unity_validation_exception(self):
        """Test UnityValidationException."""
        from chalicelib.dddpy.core_unitys.domain.unitys_exception import UnityValidationException

        exc = UnityValidationException()
        assert exc.message == "Unity validation failed"
        assert exc.status_code == 400


class TestUnitysSuccessMessages:
    """Test cases for Unitys success messages."""

    def test_success_messages(self):
        """Test SuccessMessages class."""
        from chalicelib.dddpy.core_unitys.domain.unitys_success import SuccessMessages

        assert SuccessMessages.UNITY_CREATED == "Unity created successfully"
        assert SuccessMessages.UNITY_UPDATED == "Unity updated successfully"
        assert SuccessMessages.UNITY_DELETED == "Unity deleted successfully"
        assert SuccessMessages.UNITY_RETRIEVED == "Unity retrieved successfully"
