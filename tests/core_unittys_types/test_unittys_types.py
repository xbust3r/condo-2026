"""Unit tests for UnitysTypes domain model."""
import unittest
from datetime import datetime
from unittest.mock import MagicMock


class TestUnitysTypes(unittest.TestCase):
    """Test cases for UnitysTypes domain class."""

    def test_unitys_types_creation(self):
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
        
        self.assertEqual(unity_type.id, 1)
        self.assertEqual(unity_type.name, "Apartamento")
        self.assertEqual(unity_type.code, "APT")
        self.assertEqual(unity_type.description, "Unidad habitacional tipo apartamento")

    def test_unitys_types_to_dict(self):
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
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Penthouse")
        self.assertEqual(result["code"], "PH")
        self.assertEqual(result["description"], "Unidad de lujo en la azotea")
        self.assertEqual(result["created_at"], "2025-01-01T12:00:00")
        self.assertEqual(result["updated_at"], "2025-01-01T12:00:00")

    def test_unitys_types_from_db(self):
        """Test from_db class method creates instance from DB model."""
        from chalicelib.dddpy.core_unittys_types.domain.unittys_types import UnitysTypes
        from chalicelib.dddpy.core_unittys_types.infrastructure.unittys_types import DBUnitysTypes
        
        now = datetime.now()
        mock_db = MagicMock(spec=DBUnitysTypes)
        mock_db.id = 1
        mock_db.name = "Local Commercial"
        mock_db.code = "LC"
        mock_db.description = "Espacio comercial"
        mock_db.created_at = now
        mock_db.updated_at = now
        
        unity_type = UnitysTypes.from_db(mock_db)
        
        self.assertIsInstance(unity_type, UnitysTypes)
        self.assertEqual(unity_type.id, 1)
        self.assertEqual(unity_type.name, "Local Commercial")
        self.assertEqual(unity_type.code, "LC")

    def test_unitys_types_optional_fields(self):
        """Test UnitysTypes with optional fields as None."""
        from chalicelib.dddpy.core_unittys_types.domain.unittys_types import UnitysTypes
        
        unity_type = UnitysTypes(
            id=1,
            name="Estacionamiento",
            code="EST"
        )
        
        self.assertIsNone(unity_type.description)
        self.assertIsNone(unity_type.created_at)
        self.assertIsNone(unity_type.updated_at)


class TestUnitysTypesExceptions(unittest.TestCase):
    """Test cases for UnitysTypes exceptions."""

    def test_unitys_types_not_found_exception(self):
        """Test UnitysTypesNotFoundException."""
        from chalicelib.dddpy.core_unittys_types.domain.unittys_types_exception import (
            UnitysTypesNotFoundException
        )
        
        exc = UnitysTypesNotFoundException()
        self.assertEqual(exc.message, "Unitys Types not found")
        self.assertEqual(exc.status_code, 404)

    def test_unitys_types_already_exists_exception(self):
        """Test UnitysTypesAlreadyExistsException."""
        from chalicelib.dddpy.core_unittys_types.domain.unittys_types_exception import (
            UnitysTypesAlreadyExistsException
        )
        
        exc = UnitysTypesAlreadyExistsException()
        self.assertEqual(exc.message, "Unitys Types already exists")
        self.assertEqual(exc.status_code, 409)

    def test_unitys_types_validation_exception(self):
        """Test UnitysTypesValidationException."""
        from chalicelib.dddpy.core_unittys_types.domain.unittys_types_exception import (
            UnitysTypesValidationException
        )
        
        exc = UnitysTypesValidationException()
        self.assertEqual(exc.message, "Unitys Types validation failed")
        self.assertEqual(exc.status_code, 400)


class TestUnitysTypesSuccessMessages(unittest.TestCase):
    """Test cases for UnitysTypes success messages."""

    def test_success_messages(self):
        """Test SuccessMessages class."""
        from chalicelib.dddpy.core_unittys_types.domain.unittys_types_success import SuccessMessages
        
        self.assertEqual(SuccessMessages.UNITYS_TYPES_CREATED, "Unitys Types created successfully")
        self.assertEqual(SuccessMessages.UNITYS_TYPES_UPDATED, "Unitys Types updated successfully")
        self.assertEqual(SuccessMessages.UNITYS_TYPES_DELETED, "Unitys Types deleted successfully")
        self.assertEqual(SuccessMessages.UNITYS_TYPES_RETRIEVED, "Unitys Types retrieved successfully")
        self.assertEqual(SuccessMessages.UNITYS_TYPES_LISTED, "Unitys Types listed successfully")


if __name__ == "__main__":
    unittest.main()
